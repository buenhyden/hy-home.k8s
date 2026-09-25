#!/usr/bin/env python3
"""ADR-0039 full-lane re-verification of every Retention Catalog row."""

from __future__ import annotations

import dataclasses
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import archive_cutover as cutover  # noqa: E402
import archive_dispositions as dispositions  # noqa: E402
from document_contracts import load_registry  # noqa: E402


REGISTRY = load_registry(ROOT)
DOCUMENT = "docs/05.operations/runbooks/0009-example.md"
DOCUMENT_RECORD = "docs/98.archive/retired/05.operations/runbooks/0009-example.md"
PACKAGE = "docs/03.specs/0090-example"
PACKAGE_RECORD = "docs/98.archive/completed/03.specs/0090-example"


def catalog(*rows: tuple[str, str]) -> str:
    lines = [
        "# Archive",
        "",
        dispositions.CATALOG_HEADER,
        dispositions.CATALOG_SEPARATOR,
    ]
    for record, envelope in rows:
        relative = record.removeprefix("docs/98.archive/")
        lines.append(f"| [`{relative}`](./{relative}) | `{envelope}` |")
    return "\n".join(lines) + "\n"


class CatalogReverificationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="adr0039-catalog-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Catalog Fixture")
        self.write(DOCUMENT, b"# Example\n\n[Guide](../guides/x.md)\n")
        self.write(f"{PACKAGE}/spec.md", b"# Spec\n")
        self.write(f"{PACKAGE}/tasks/tsk-0001-x.md", b"# Task\n")
        self.source = self.commit("source")

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", *arguments],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.stdout.strip()

    def write(self, path: str, content: bytes) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    def commit(self, message: str) -> str:
        self.git("add", "-A", "--", ".")
        self.git("commit", "--quiet", "-m", message)
        return self.git("rev-parse", "HEAD")

    def retain(self) -> None:
        (self.root / DOCUMENT_RECORD).parent.mkdir(parents=True, exist_ok=True)
        self.git("mv", DOCUMENT, DOCUMENT_RECORD)
        (self.root / PACKAGE_RECORD).parent.mkdir(parents=True, exist_ok=True)
        self.git("mv", PACKAGE, PACKAGE_RECORD)
        self.commit("retain")

    def codes(self, index_text: str, root: Path | None = None) -> set[tuple[str, str]]:
        return {
            (item.code, item.path)
            for item in cutover.catalog_envelope_diagnostics(
                root or self.root, REGISTRY, index_text
            )
        }

    def test_exact_rows_reverify(self) -> None:
        self.retain()
        text = catalog(
            (DOCUMENT_RECORD, f"{self.source}:{DOCUMENT}"),
            (PACKAGE_RECORD, f"{self.source}:{PACKAGE}"),
        )
        self.assertEqual(self.codes(text), set())

    def test_a_missing_object_fails(self) -> None:
        self.retain()
        text = catalog((DOCUMENT_RECORD, f"{'0' * 40}:{DOCUMENT}"))
        self.assertIn(("ARCHIVE-CATALOG-OBJECT", DOCUMENT_RECORD), self.codes(text))

    def test_an_unreachable_commit_fails(self) -> None:
        self.retain()
        tree = self.git("rev-parse", f"{self.source}^{{tree}}")
        dangling = self.git("commit-tree", tree, "-m", "unreachable")
        text = catalog((DOCUMENT_RECORD, f"{dangling}:{DOCUMENT}"))
        self.assertIn(("ARCHIVE-CATALOG-OBJECT", DOCUMENT_RECORD), self.codes(text))

    def test_a_unit_row_must_name_a_tree(self) -> None:
        self.retain()
        text = catalog((PACKAGE_RECORD, f"{self.source}:{PACKAGE}/spec.md"))
        self.assertIn(("ARCHIVE-CATALOG-OBJECT", PACKAGE_RECORD), self.codes(text))

    def test_a_document_row_must_name_a_blob(self) -> None:
        self.retain()
        text = catalog((DOCUMENT_RECORD, f"{self.source}:{PACKAGE}"))
        self.assertIn(("ARCHIVE-CATALOG-OBJECT", DOCUMENT_RECORD), self.codes(text))

    def test_retained_bytes_must_equal_the_envelope(self) -> None:
        self.retain()
        self.write(f"{PACKAGE_RECORD}/tasks/tsk-0001-x.md", b"# Task\n\nEdited.\n")
        self.commit("edit")
        text = catalog((PACKAGE_RECORD, f"{self.source}:{PACKAGE}"))
        self.assertIn(("ARCHIVE-CATALOG-RETENTION", PACKAGE_RECORD), self.codes(text))

    def test_a_mode_change_fails(self) -> None:
        self.retain()
        target = self.root / PACKAGE_RECORD / "spec.md"
        target.chmod(target.stat().st_mode | 0o111)
        self.git("update-index", "--chmod=+x", f"{PACKAGE_RECORD}/spec.md")
        self.commit("mode-change")
        text = catalog((PACKAGE_RECORD, f"{self.source}:{PACKAGE}"))
        self.assertIn(("ARCHIVE-CATALOG-RETENTION", PACKAGE_RECORD), self.codes(text))

    def test_a_symlink_change_fails(self) -> None:
        self.retain()
        target = self.root / PACKAGE_RECORD / "spec.md"
        target.unlink()
        target.symlink_to("tasks/tsk-0001-x.md")
        self.commit("symlink-change")
        text = catalog((PACKAGE_RECORD, f"{self.source}:{PACKAGE}"))
        self.assertIn(("ARCHIVE-CATALOG-RETENTION", PACKAGE_RECORD), self.codes(text))

    def test_a_missing_native_member_fails(self) -> None:
        self.retain()
        (self.root / PACKAGE_RECORD / "tasks" / "tsk-0001-x.md").unlink()
        self.commit("missing-member")
        text = catalog((PACKAGE_RECORD, f"{self.source}:{PACKAGE}"))
        self.assertIn(("ARCHIVE-CATALOG-RETENTION", PACKAGE_RECORD), self.codes(text))

    def test_an_empty_source_tree_fails_rather_than_vacuously_matches(self) -> None:
        """Git tracks no empty directory, so a removed unit's old path resolves
        to no tree object at all. That must still fail, never read as a match."""

        self.git("rm", "-r", "--quiet", "--", PACKAGE)
        empty_source = self.commit("empty-package")
        text = catalog((PACKAGE_RECORD, f"{empty_source}:{PACKAGE}"))
        self.assertIn(("ARCHIVE-CATALOG-OBJECT", PACKAGE_RECORD), self.codes(text))

    def test_unreadable_entries_fail_rather_than_match(self) -> None:
        self.retain()
        text = catalog((PACKAGE_RECORD, f"{self.source}:{PACKAGE}"))
        with (
            mock.patch.object(cutover, "index_entries", return_value=None),
            mock.patch.object(cutover, "commit_entries", return_value=None),
        ):
            self.assertIn(
                ("ARCHIVE-CATALOG-RETENTION", PACKAGE_RECORD), self.codes(text)
            )

    def test_repository_catalog_reverifies_against_its_history(self) -> None:
        """Every row re-verifies, and each disposition adds one more of them."""

        index = (ROOT / dispositions.archive_ledger_path(REGISTRY)).read_text(
            encoding="utf-8"
        )
        rows, errors = dispositions.parse_catalog(index)
        self.assertEqual(errors, ())
        legacy = REGISTRY.legacy_rebased_retained_paths
        self.assertEqual(len(legacy), 16)
        self.assertLessEqual(legacy, frozenset(rows))
        self.assertGreaterEqual(len(rows), len(legacy))
        self.assertEqual(self.codes(index, ROOT), set())

    def test_a_commit_off_the_default_branch_fails_even_from_current_head(
        self,
    ) -> None:
        """ADR-0040: reachability is judged from the default branch, not `HEAD`.

        A commit the current checkout has, but the default branch never
        receives, must fail even though it is trivially its own ancestor.
        """

        self.retain()
        self.git("checkout", "--quiet", "-b", "topic")
        self.write(DOCUMENT_RECORD, b"# Example\n\nOff-branch edit.\n")
        off_branch = self.commit("off-branch")
        self.assertEqual(self.git("symbolic-ref", "--short", "HEAD"), "topic")
        text = catalog((DOCUMENT_RECORD, f"{off_branch}:{DOCUMENT_RECORD}"))
        self.assertIn(("ARCHIVE-CATALOG-OBJECT", DOCUMENT_RECORD), self.codes(text))

    def test_an_unresolvable_default_branch_fails(self) -> None:
        self.retain()
        text = catalog((DOCUMENT_RECORD, f"{self.source}:{DOCUMENT}"))
        ghost_assessment = dataclasses.replace(
            REGISTRY.archive_assessment, default_branch="no-such-branch"
        )
        ghost_registry = dataclasses.replace(
            REGISTRY, archive_assessment=ghost_assessment
        )
        codes = {
            (item.code, item.path)
            for item in cutover.catalog_envelope_diagnostics(
                self.root, ghost_registry, text
            )
        }
        self.assertIn(("ARCHIVE-CATALOG-OBJECT", DOCUMENT_RECORD), codes)

    def test_a_shallow_clone_fails(self) -> None:
        self.retain()
        retained = self.git("rev-parse", "HEAD")
        text = catalog((DOCUMENT_RECORD, f"{retained}:{DOCUMENT_RECORD}"))
        # The full repository verifies this trivially-reachable envelope.
        self.assertEqual(self.codes(text), set())
        with tempfile.TemporaryDirectory(prefix="adr0039-shallow-") as clone_name:
            clone_root = Path(clone_name) / "clone"
            subprocess.run(
                [
                    "git",
                    "-c",
                    "core.hooksPath=/dev/null",
                    "clone",
                    "--quiet",
                    "--depth=1",
                    "--no-local",
                    "--branch",
                    "main",
                    str(self.root),
                    str(clone_root),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertIn(
                ("ARCHIVE-CATALOG-OBJECT", DOCUMENT_RECORD),
                self.codes(text, clone_root),
            )


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
