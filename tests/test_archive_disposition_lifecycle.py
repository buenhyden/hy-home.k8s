#!/usr/bin/env python3
"""ADR-0039 dispositions admitted by the lifecycle gate without a path ledger."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "validate-document-lifecycle.py"
SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_dispositions_tested", MODULE_PATH
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError(f"cannot load lifecycle validator from {MODULE_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

import archive_dispositions as dispositions  # noqa: E402
from document_contracts import load_registry  # noqa: E402


REGISTRY_PATH = "docs/99.templates/registry.json"
INDEX = "docs/98.archive/README.md"
ADR = "docs/02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md"
RUNBOOK = "docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md"
RUNBOOK_TARGET = "docs/05.operations/runbooks/0001-argocd-bootstrap-runbook.md"
MIGRATION = "docs/98.archive/migrations/0024-runbook-rename.md"
PACKAGE = "docs/03.specs/0080-adr-0032-retention-pilot"
# The seed package is retained in `completed/`. Exact retention keeps its bytes,
# so the fixture still builds a Stage 03 source out of the same document.
PACKAGE_SEED = "docs/98.archive/completed/03.specs/0080-adr-0032-retention-pilot"
PACKAGE_MEMBERS = ("spec.md", "plan.md", "tasks/tsk-0001-retain-adr-0032.md")
TASK = f"{PACKAGE}/tasks/tsk-0001-retain-adr-0032.md"
BUNDLE = "docs/05.operations/incidents/2026/inc-0001-example"
INDEX_TEXT = "---\ntitle: Archive\n---\n\n# Archive\n"


def original_bytes(path: str) -> bytes:
    """Return a decision at its original path, rebuilt from its retained body."""

    source = PurePosixPath(path)
    retained = dispositions.retained_body_path(source, "superseded")
    text = (ROOT / retained).read_text(encoding="utf-8")
    return dispositions.rebase_relative_links(text, retained, source).encode("utf-8")


def catalog(*rows: tuple[str, str]) -> str:
    lines = [INDEX_TEXT, "## Retention Catalog", "", dispositions.CATALOG_HEADER]
    lines.append(dispositions.CATALOG_SEPARATOR)
    for record, envelope in rows:
        relative = record.removeprefix("docs/98.archive/")
        lines.append(f"| [`{relative}`](./{relative}) | `{envelope}` |")
    return "\n".join(lines) + "\n"


def scope_migration(moved_scope: str, current_owner: str) -> str:
    return (
        "---\n"
        'title: "Runbook Rename"\n'
        'version: "1.0.0"\n'
        'type: "archive/scope-migration"\n'
        'status: "recorded"\n'
        'owner: "platform"\n'
        'updated: "2026-09-15"\n'
        'layer: "archive"\n'
        'artifact_id: "MIG-0024"\n'
        f'moved_scope: "{moved_scope}"\n'
        f'current_owner: "{current_owner}"\n'
        "---\n"
    )


def operation_document(profile: str, status: str, artifact_id: str) -> bytes:
    return (
        f'---\ntitle: "Example"\nversion: "1.0.0"\ntype: "{profile}"\n'
        f'status: "{status}"\nowner: "platform"\nupdated: "2026-09-15"\n'
        f'layer: "operations"\nartifact_id: "{artifact_id}"\n---\n\n# Example\n'
    ).encode()


class DispositionLifecycleTest(unittest.TestCase):
    registry = load_registry(ROOT)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="adr0039-lifecycle-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Disposition Fixture")
        for path in (REGISTRY_PATH, RUNBOOK):
            self.write(path, (ROOT / path).read_bytes())
        for member in PACKAGE_MEMBERS:
            self.write(
                f"{PACKAGE}/{member}", (ROOT / PACKAGE_SEED / member).read_bytes()
            )
        self.write(ADR, original_bytes(ADR))
        self.write(INDEX, INDEX_TEXT.encode())
        self.git("add", "--", ".")
        self.git("commit", "--quiet", "-m", "base")
        self.base = self.git("rev-parse", "HEAD")

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

    def evaluate(self) -> list[tuple[str, str]]:
        self.git("add", "-A", "--", ".")
        diagnostics = VALIDATOR._evaluate_comparison(
            self.root, self.registry, mode="staged"
        )
        return sorted((item.rule_id, item.path.as_posix()) for item in diagnostics)

    def gaps(self) -> list[str]:
        self.git("add", "-A", "--", ".")
        return [
            item.evidence_gap
            for item in VALIDATOR._evaluate_comparison(
                self.root, self.registry, mode="staged"
            )
        ]

    def retain(self, class_name: str, source: str) -> str:
        """Move one document into its retention class byte for byte."""

        record = dispositions.retained_body_path(PurePosixPath(source), class_name)
        self.write(record.as_posix(), (self.root / source).read_bytes())
        (self.root / source).unlink()
        return record.as_posix()

    def retain_unit(self, class_name: str, source_root: str) -> str:
        """Move a whole unit directory, keeping every entry's bytes and mode."""

        record = dispositions.retained_body_path(PurePosixPath(source_root), class_name)
        (self.root / record).parent.mkdir(parents=True, exist_ok=True)
        self.git("mv", source_root, record.as_posix())
        return record.as_posix()

    def set_status(self, path: str, status: str) -> str:
        text = (self.root / path).read_bytes()
        self.write(
            path,
            re.sub(
                rb'(?m)^status: "[^"]+"$', f'status: "{status}"'.encode(), text, count=1
            ),
        )
        return self.commit(status)

    # A document unit keeps its exact bytes.

    def test_retained_copy_keeps_its_links_as_they_were(self) -> None:
        source = PurePosixPath(ADR)
        record = dispositions.retained_body_path(source, "superseded")
        original = (self.root / ADR).read_text(encoding="utf-8")
        rebased = dispositions.rebase_relative_links(original, source, record)
        self.assertNotEqual(rebased, original)
        self.write(record.as_posix(), rebased.encode("utf-8"))
        (self.root / ADR).unlink()
        self.write(INDEX, catalog((record.as_posix(), f"{self.base}:{ADR}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", record.as_posix()), self.evaluate())

    def test_retained_copy_may_not_rewrite_its_body(self) -> None:
        record = self.retain("superseded", ADR)
        body = (self.root / record).read_bytes()
        self.write(record, body.replace(b"## Context", b"## Context\n\nAdded.", 1))
        self.write(INDEX, catalog((record, f"{self.base}:{ADR}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", record), self.evaluate())

    def test_catalog_envelope_admits_a_superseded_decision_leaving_the_log(
        self,
    ) -> None:
        record = self.retain("superseded", ADR)
        self.write(INDEX, catalog((record, f"{self.base}:{ADR}")).encode())
        self.assertEqual(self.evaluate(), [])

    def test_retained_body_without_a_catalog_row_is_not_admitted(self) -> None:
        self.retain("superseded", ADR)
        self.assertTrue(self.evaluate())

    def test_envelope_must_name_the_source_object_the_base_holds(self) -> None:
        record = self.retain("superseded", ADR)
        self.write(INDEX, catalog((record, f"{'0' * 40}:{ADR}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", record), self.evaluate())

    def test_class_must_admit_the_source_terminal_state(self) -> None:
        record = self.retain("retired", ADR)
        self.write(INDEX, catalog((record, f"{self.base}:{ADR}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", record), self.evaluate())

    def test_retained_body_cannot_change_after_its_disposition(self) -> None:
        record = self.retain("superseded", ADR)
        self.write(INDEX, catalog((record, f"{self.base}:{ADR}")).encode())
        self.assertEqual(self.evaluate(), [])
        self.git("commit", "--quiet", "-m", "retain")
        body = (self.root / record).read_bytes()
        self.write(record, body.replace(b"## Context", b"## Context\n\nRewritten.", 1))
        self.assertIn(("LIFECYCLE-EVIDENCE", record), self.evaluate())

    def test_frozen_completed_body_cannot_change(self) -> None:
        completed = (
            "docs/98.archive/completed/03.specs/"
            "0067-artifact-identity-and-filename-normalization/spec.md"
        )
        self.write(completed, (ROOT / completed).read_bytes())
        self.git("add", "--", completed)
        self.git("commit", "--quiet", "-m", "frozen body")
        self.write(completed, (ROOT / completed).read_bytes() + b"\nEdited.\n")
        self.assertIn(("LIFECYCLE-EVIDENCE", completed), self.evaluate())

    # A spec package is retained as one tree.

    def retain_package(
        self, class_name: str = "completed", *, envelope: str = ""
    ) -> str:
        record = self.retain_unit(class_name, PACKAGE)
        commit = envelope or self.base
        self.write(INDEX, catalog((record, f"{commit}:{PACKAGE}")).encode())
        return record

    def test_package_is_retained_as_its_exact_tree(self) -> None:
        self.retain_package()
        self.assertEqual(self.evaluate(), [])

    def test_package_member_bytes_cannot_change(self) -> None:
        record = self.retain_package()
        task = f"{record}/tasks/tsk-0001-retain-adr-0032.md"
        self.write(task, (self.root / task).read_bytes() + b"\nEdited.\n")
        self.assertIn(("LIFECYCLE-EVIDENCE", f"{record}/spec.md"), self.evaluate())

    def test_package_cannot_gain_a_member(self) -> None:
        record = self.retain_package()
        self.write(f"{record}/notes.txt", b"not in the source tree\n")
        self.assertIn(("LIFECYCLE-EVIDENCE", f"{record}/spec.md"), self.evaluate())

    def test_package_cannot_drop_a_member(self) -> None:
        record = self.retain_package()
        (self.root / record / "tasks/tsk-0001-retain-adr-0032.md").unlink()
        self.assertIn(("LIFECYCLE-EVIDENCE", f"{record}/spec.md"), self.evaluate())

    def test_package_file_mode_cannot_change(self) -> None:
        record = self.retain_package()
        (self.root / record / "plan.md").chmod(0o755)
        self.assertIn(("LIFECYCLE-EVIDENCE", f"{record}/spec.md"), self.evaluate())

    def test_a_package_member_is_not_retained_alone(self) -> None:
        record = self.retain("completed", f"{PACKAGE}/spec.md")
        self.write(INDEX, catalog((record, f"{self.base}:{PACKAGE}/spec.md")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", record), self.evaluate())

    def test_completed_package_may_retain_a_cancelled_task(self) -> None:
        head = self.set_status(TASK, "cancelled")
        self.retain_package(envelope=head)
        self.assertEqual(self.evaluate(), [])

    def test_withdrawn_package_is_not_completed(self) -> None:
        head = self.set_status(f"{PACKAGE}/spec.md", "withdrawn")
        record = self.retain_package(envelope=head)
        self.assertIn(("LIFECYCLE-EVIDENCE", f"{record}/spec.md"), self.evaluate())

    def test_withdrawn_package_is_retired(self) -> None:
        head = self.set_status(f"{PACKAGE}/spec.md", "withdrawn")
        self.retain_package("retired", envelope=head)
        self.assertEqual(self.evaluate(), [])

    def test_package_with_an_open_task_is_not_retained(self) -> None:
        head = self.set_status(TASK, "in-progress")
        record = self.retain_package(envelope=head)
        self.assertIn(("LIFECYCLE-EVIDENCE", f"{record}/spec.md"), self.evaluate())

    def test_retained_package_is_frozen(self) -> None:
        record = self.retain_package()
        self.assertEqual(self.evaluate(), [])
        self.git("commit", "--quiet", "-m", "retain")
        self.write(f"{record}/notes.txt", b"added after the disposition\n")
        self.assertIn(("LIFECYCLE-EVIDENCE", f"{record}/spec.md"), self.evaluate())

    # An Incident bundle is retained with its published Postmortem.

    def retain_bundle(self, *documents: tuple[str, bytes]) -> list[str]:
        for name, content in documents:
            self.write(f"{BUNDLE}/{name}", content)
        head = self.commit("incident")
        record = self.retain_unit("resolved", BUNDLE)
        self.write(INDEX, catalog((record, f"{head}:{BUNDLE}")).encode())
        return self.gaps()

    def test_resolved_bundle_needs_its_postmortem(self) -> None:
        gaps = self.retain_bundle(
            (
                "incident.md",
                operation_document("operation/incident", "closed", "INC-0001"),
            )
        )
        self.assertTrue(any("postmortem.md" in gap for gap in gaps), gaps)

    def test_resolved_bundle_needs_a_published_postmortem(self) -> None:
        gaps = self.retain_bundle(
            (
                "incident.md",
                operation_document("operation/incident", "closed", "INC-0001"),
            ),
            (
                "postmortem.md",
                operation_document("operation/postmortem", "draft", "PM-0001"),
            ),
        )
        self.assertTrue(any("postmortem.md" in gap for gap in gaps), gaps)

    # A move between active stages keeps its identity without a Stage 98 record.

    def test_identity_preserving_move_needs_no_stage98_record(self) -> None:
        self.write(RUNBOOK_TARGET, (self.root / RUNBOOK).read_bytes())
        (self.root / RUNBOOK).unlink()
        self.assertEqual(self.evaluate(), [])

    def test_identity_arriving_at_two_paths_is_not_a_move(self) -> None:
        copy = "docs/05.operations/runbooks/0001-argocd-bootstrap-runbook-copy.md"
        body = (self.root / RUNBOOK).read_bytes()
        self.write(RUNBOOK_TARGET, body)
        self.write(copy, body)
        (self.root / RUNBOOK).unlink()
        paths = {path for _rule, path in self.evaluate()}
        self.assertTrue(paths & {RUNBOOK_TARGET, copy}, paths)

    def test_move_that_changes_its_identity_is_not_admitted(self) -> None:
        body = (self.root / RUNBOOK).read_bytes()
        self.write(
            RUNBOOK_TARGET,
            body.replace(b'artifact_id: "RUN-0001"', b'artifact_id: "RUN-0002"', 1),
        )
        (self.root / RUNBOOK).unlink()
        self.assertIn(("LIFECYCLE-CREATE", RUNBOOK_TARGET), self.evaluate())

    # A scope migration stays for consumers outside the repository.

    def test_scope_migration_admits_a_current_document_move(self) -> None:
        self.write(RUNBOOK_TARGET, (self.root / RUNBOOK).read_bytes())
        (self.root / RUNBOOK).unlink()
        self.write(MIGRATION, scope_migration(RUNBOOK, RUNBOOK_TARGET).encode())
        self.write(INDEX, catalog((MIGRATION, f"{self.base}:{RUNBOOK}")).encode())
        self.assertEqual(self.evaluate(), [])

    def test_scope_migration_rejects_a_rewritten_body(self) -> None:
        self.write(
            RUNBOOK_TARGET, (self.root / RUNBOOK).read_bytes() + b"\nNew step.\n"
        )
        (self.root / RUNBOOK).unlink()
        self.write(MIGRATION, scope_migration(RUNBOOK, RUNBOOK_TARGET).encode())
        self.write(INDEX, catalog((MIGRATION, f"{self.base}:{RUNBOOK}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", MIGRATION), self.evaluate())

    def test_scope_migration_must_match_its_catalog_envelope(self) -> None:
        self.write(RUNBOOK_TARGET, (self.root / RUNBOOK).read_bytes())
        (self.root / RUNBOOK).unlink()
        self.write(MIGRATION, scope_migration(RUNBOOK, RUNBOOK_TARGET).encode())
        self.write(INDEX, catalog((MIGRATION, f"{self.base}:{ADR}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", MIGRATION), self.evaluate())

    def test_scope_migration_envelope_must_name_the_base_object(self) -> None:
        original = (self.root / RUNBOOK).read_bytes()
        self.write(RUNBOOK, original + b"\nEarlier revision.\n")
        earlier = self.commit("earlier")
        self.write(RUNBOOK, original)
        self.commit("current")
        self.write(RUNBOOK_TARGET, original)
        (self.root / RUNBOOK).unlink()
        self.write(MIGRATION, scope_migration(RUNBOOK, RUNBOOK_TARGET).encode())
        self.write(INDEX, catalog((MIGRATION, f"{earlier}:{RUNBOOK}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", MIGRATION), self.evaluate())


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
