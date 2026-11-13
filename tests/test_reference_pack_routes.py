#!/usr/bin/env python3
"""Focused Stage 90 semantic pack route tests."""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
REGISTRY_VALIDATOR_PATH = ROOT / "scripts/validate-document-contract-registry.py"

from document_contracts import (  # noqa: E402
    DocumentContractError,
    classify_path,
    load_registry,
)


def load_registry_validator():
    specification = importlib.util.spec_from_file_location(
        "reference_pack_registry_validator", REGISTRY_VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("document registry validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def git_blob_id(content: bytes) -> str:
    payload = f"blob {len(content)}\0".encode("ascii") + content
    return hashlib.sha1(payload).hexdigest()


class ReferencePackRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)
        cls.validator = load_registry_validator()

    def test_each_category_selects_its_matching_pack_template(self) -> None:
        for category, singular in (
            ("audits", "audit"),
            ("data", "data"),
            ("research", "research"),
        ):
            with self.subTest(category=category):
                profile = classify_path(
                    self.registry,
                    PurePosixPath(
                        f"docs/90.references/{category}/0001-example/README.md"
                    ),
                )
                self.assertEqual(profile.profile_id, f"reference/{singular}-pack")
                self.assertEqual(profile.mode, "authored")
                self.assertEqual(profile.document_role, "reference-pack-readme")
                self.assertIsNotNone(profile.lifecycle_domain)
                self.assertEqual(profile.lifecycle_domain.family, "reference")
                self.assertEqual(
                    profile.lifecycle_domain.validation_class("published"), "current"
                )
                self.assertEqual(
                    profile.template,
                    PurePosixPath(
                        f"docs/99.templates/templates/references/{singular}-pack.template.md"
                    ),
                )

    def test_pack_templates_name_the_pack_contract_and_the_pack_index(self) -> None:
        for kind in ("audit", "data", "research"):
            template = (
                ROOT / f"docs/99.templates/templates/references/{kind}-pack.template.md"
            )
            headings = [
                line
                for line in template.read_text("utf-8").splitlines()
                if line.startswith("## ")
            ]
            with self.subTest(kind=kind):
                self.assertIn("## Pack Contract", headings)
                self.assertIn("## Pack Index", headings)
                self.assertEqual(
                    [h for h in headings if h.endswith(("Contract", "Index"))],
                    ["## Pack Contract", "## Pack Index"],
                )

    def test_pack_members_use_the_reference_profile(self) -> None:
        for category in ("audits", "data", "research"):
            with self.subTest(category=category):
                profile = classify_path(
                    self.registry,
                    PurePosixPath(
                        f"docs/90.references/{category}/0001-example/m0001-report.md"
                    ),
                )
                singular = category.removesuffix("s")
                self.assertEqual(profile.profile_id, f"reference/{singular}")

    def test_date_based_and_loose_reference_paths_are_uncovered(self) -> None:
        for category in ("audits", "data", "research"):
            for path in (
                f"docs/90.references/{category}/2026-08-31-example/README.md",
                f"docs/90.references/{category}/example.md",
            ):
                with (
                    self.subTest(path=path),
                    self.assertRaises(DocumentContractError) as raised,
                ):
                    classify_path(self.registry, PurePosixPath(path))
                self.assertEqual(
                    {item.rule_id for item in raised.exception.diagnostics},
                    {"REGISTRY_ROUTE_UNCOVERED"},
                )

    def test_existing_reference_material_uses_numbered_pack_routes(self) -> None:
        stage_root = ROOT / "docs/90.references"
        for category in ("audits", "data", "research"):
            category_root = stage_root / category
            self.assertFalse(category_root.is_symlink())
            self.assertTrue(category_root.is_dir())
            for path in category_root.rglob("*"):
                if not path.is_file() or path == category_root / "README.md":
                    continue
                relative = PurePosixPath(path.relative_to(ROOT).as_posix())
                profile = classify_path(self.registry, relative)
                self.assertIn(
                    profile.profile_id,
                    {
                        f"reference/{category.removesuffix('s')}",
                        f"reference/{category.removesuffix('s')}-pack",
                    },
                )

    def test_existing_reference_pack_topology_is_canonical(self) -> None:
        self.validator._assert_reference_pack_topology(ROOT, self.registry)

    def test_empty_collections_require_all_three_directories(self) -> None:
        for missing in (None, "audits", "data", "research"):
            with (
                self.subTest(missing=missing),
                tempfile.TemporaryDirectory(prefix="reference-collections-") as raw,
            ):
                root = Path(raw)
                stage = root / "docs/90.references"
                stage.mkdir(parents=True)
                (stage / "README.md").write_text("stage\n", encoding="utf-8")
                for category in ("audits", "data", "research"):
                    if category == missing:
                        continue
                    directory = stage / category
                    directory.mkdir()
                    (directory / "README.md").write_text("router\n", encoding="utf-8")
                inventory = {
                    PurePosixPath(path.relative_to(root).as_posix()): git_blob_id(
                        path.read_bytes()
                    )
                    for path in stage.rglob("*.md")
                }
                with mock.patch.object(
                    self.validator, "_staged_reference_files", return_value=inventory
                ):
                    if missing is None:
                        self.validator._assert_reference_pack_topology(
                            root, self.registry
                        )
                    else:
                        with self.assertRaisesRegex(
                            AssertionError, "REFERENCE_PACK_DIRECTORY"
                        ):
                            self.validator._assert_reference_pack_topology(
                                root, self.registry
                            )

    def test_pack_topology_rejects_duplicate_missing_and_non_regular_entries(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="reference-topology-") as raw:
            root = Path(raw)
            stage = root / "docs/90.references"
            research = stage / "research"
            research.mkdir(parents=True)
            (stage / "README.md").write_text("stage\n", encoding="utf-8")
            (research / "README.md").write_text("category\n", encoding="utf-8")
            for category in ("audits", "data"):
                (stage / category).mkdir()
                (stage / category / "README.md").write_text(
                    "category\n", encoding="utf-8"
                )
            (research / "loose.md").write_text("loose\n", encoding="utf-8")
            first = research / "0001-alpha"
            first.mkdir()
            (first / "README.md").write_text("pack\n", encoding="utf-8")
            second = research / "0001-beta"
            second.mkdir()
            (second / "payload.md").write_text("payload\n", encoding="utf-8")
            (first / "nested").mkdir()
            staged_files = {
                PurePosixPath(path.relative_to(root).as_posix()): git_blob_id(
                    path.read_bytes()
                )
                for path in stage.rglob("*")
                if path.is_file()
            }

            with (
                mock.patch.object(
                    self.validator,
                    "_staged_reference_files",
                    return_value=staged_files,
                ),
                self.assertRaises(AssertionError) as raised,
            ):
                self.validator._assert_reference_pack_topology(root, self.registry)

        message = str(raised.exception)
        self.assertIn("REFERENCE_PACK_ENTRY", message)
        self.assertIn("REFERENCE_PACK_NUMBER", message)
        self.assertIn("REFERENCE_PACK_README", message)
        self.assertIn("REFERENCE_PACK_MEMBER", message)

    def test_pack_topology_rejects_staged_index_worktree_divergence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reference-index-drift-") as raw:
            root = Path(raw)
            stage = root / "docs/90.references"
            research = stage / "research"
            pack = research / "0001-alpha"
            pack.mkdir(parents=True)
            worktree_paths = (
                "docs/90.references/README.md",
                "docs/90.references/audits/README.md",
                "docs/90.references/data/README.md",
                "docs/90.references/research/README.md",
                "docs/90.references/research/0001-alpha/README.md",
            )
            for relative in worktree_paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("reference\n", encoding="utf-8")
            staged_paths = (
                *worktree_paths,
                "docs/90.references/research/0001-beta/README.md",
            )
            stdout = b"".join(
                f"100644 {'0' * 40} 0\t{relative}\0".encode("utf-8")
                for relative in staged_paths
            )
            completed = subprocess.CompletedProcess(["git", "ls-files"], 0, stdout, b"")

            with (
                mock.patch.object(
                    self.validator, "run_bounded_process", return_value=completed
                ),
                self.assertRaisesRegex(AssertionError, "REFERENCE_PACK_INDEX_DRIFT"),
            ):
                self.validator._assert_reference_pack_topology(root, self.registry)

    def test_pack_topology_rejects_same_path_staged_content_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reference-content-drift-") as raw:
            root = Path(raw)
            worktree_contents = {
                "docs/90.references/README.md": b"stage\n",
                "docs/90.references/audits/README.md": b"category\n",
                "docs/90.references/data/README.md": b"category\n",
                "docs/90.references/research/README.md": b"category\n",
                "docs/90.references/research/0001-alpha/README.md": b"valid\n",
            }
            for relative, content in worktree_contents.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            staged_contents = {
                **worktree_contents,
                "docs/90.references/research/0001-alpha/README.md": b"invalid\n",
            }
            stdout = b"".join(
                (f"100644 {git_blob_id(content)} 0\t{relative}\0").encode("utf-8")
                for relative, content in staged_contents.items()
            )
            completed = subprocess.CompletedProcess(["git", "ls-files"], 0, stdout, b"")

            with (
                mock.patch.object(
                    self.validator, "run_bounded_process", return_value=completed
                ),
                self.assertRaisesRegex(AssertionError, "REFERENCE_PACK_INDEX_DRIFT"),
            ):
                self.validator._assert_reference_pack_topology(root, self.registry)

    def test_preserved_research_does_not_claim_retired_llm_wiki_as_current(
        self,
    ) -> None:
        pack = ROOT / "docs/90.references/research/0001-workspace-engineering"
        offenders: list[str] = []
        for path in sorted(pack.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if "The current generator" in text:
                offenders.append(path.relative_to(ROOT).as_posix())
            lines = text.splitlines()
            for index, line in enumerate(lines):
                if "docs/90.references/llm-wiki/" not in line:
                    continue
                context = " ".join(lines[max(0, index - 2) : index + 2]).casefold()
                if not any(
                    marker in context
                    for marker in ("histor", "observation", "retired", "then-")
                ):
                    offenders.append(f"{path.relative_to(ROOT).as_posix()}:{index + 1}")
        self.assertEqual(offenders, [])


class PublishedMemberFreezeTest(unittest.TestCase):
    """SPEC-0150: a published Stage 90 member is not rewritten."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)
        cls.validator = load_registry_validator()

    MEMBER = PurePosixPath("docs/90.references/audits/0001-example/m0001-example.md")
    PACK = PurePosixPath("docs/90.references/audits/0001-example/README.md")

    @staticmethod
    def member(status: str, body: str) -> bytes:
        return (
            f'---\ntitle: "Example"\nversion: "0.1.0"\ntype: "reference/audit"\n'
            f'status: "{status}"\nowner: "platform"\nupdated: "2026-11-01"\n---\n'
            f"\n# Reference: Example\n\n{body}\n"
        ).encode("utf-8")

    def errors(self, base: bytes | None, staged: bytes, path=MEMBER) -> list[str]:
        bases = {} if base is None else {path: base}
        return self.validator.published_rewrite_errors(
            self.registry, bases, {path: staged}
        )

    def test_body_rewrite_of_a_published_member_is_refused(self) -> None:
        base = self.member("published", "Observed [AD](../a.md) once.")
        for staged in (
            self.member("published", "Observed [AD](../a.md) twice."),
            self.member("published", "Observed [AD-0006](../a.md) once."),
            self.member("published", 'Observed [AD](../a.md "new prose") once.'),
            self.member("published", "Observed [AD](new sentence here) once."),
        ):
            with self.subTest(staged=staged):
                (error,) = self.errors(base, staged)
                self.assertIn("REFERENCE_PUBLISHED_REWRITE", error)

    def test_lifecycle_values_and_link_destinations_may_change(self) -> None:
        base = self.member("published", "Observed [AD](../a.md) once.")
        staged = self.member("retired", "Observed [AD](../b.md#anchor) once.")
        staged = staged.replace(b'version: "0.1.0"', b'version: "0.2.0"')
        staged = staged.replace(b'updated: "2026-11-01"', b'updated: "2026-11-06"')
        self.assertEqual(self.errors(base, staged), [])

    def test_draft_new_and_pack_files_are_not_frozen(self) -> None:
        draft = self.member("draft", "Before.")
        self.assertEqual(self.errors(draft, self.member("draft", "After.")), [])
        self.assertEqual(self.errors(None, self.member("published", "New.")), [])
        published = self.member("published", "Index one.")
        self.assertEqual(
            self.errors(published, self.member("published", "Index two."), self.PACK),
            [],
        )


if __name__ == "__main__":
    unittest.main()
