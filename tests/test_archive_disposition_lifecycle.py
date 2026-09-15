#!/usr/bin/env python3
"""ADR-0038 dispositions admitted by the lifecycle gate without a path ledger."""

from __future__ import annotations

import importlib.util
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
ADR = "docs/02.architecture/decisions/0032-completed-and-terminal-document-retention.md"
RUNBOOK = "docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md"
RUNBOOK_TARGET = "docs/05.operations/runbooks/0001-argocd-bootstrap-runbook.md"
MIGRATION = "docs/98.archive/migrations/0024-runbook-rename.md"
INDEX_TEXT = "---\ntitle: Archive\n---\n\n# Archive\n"


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


class DispositionLifecycleTest(unittest.TestCase):
    registry = load_registry(ROOT)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="adr0038-lifecycle-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Disposition Fixture")
        for path in (REGISTRY_PATH, ADR, RUNBOOK):
            self.write(path, (ROOT / path).read_bytes())
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

    def evaluate(self) -> list[tuple[str, str]]:
        self.git("add", "-A", "--", ".")
        diagnostics = VALIDATOR._evaluate_comparison(
            self.root, self.registry, mode="staged"
        )
        return sorted((item.rule_id, item.path.as_posix()) for item in diagnostics)

    def retain(self, class_name: str, source: str) -> str:
        record = dispositions.retained_body_path(PurePosixPath(source), class_name)
        self.write(record.as_posix(), (self.root / source).read_bytes())
        (self.root / source).unlink()
        return record.as_posix()

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

    def test_scope_migration_admits_a_current_document_move(self) -> None:
        self.write(RUNBOOK_TARGET, (self.root / RUNBOOK).read_bytes())
        (self.root / RUNBOOK).unlink()
        self.write(MIGRATION, scope_migration(RUNBOOK, RUNBOOK_TARGET).encode())
        self.write(INDEX, catalog((MIGRATION, f"{self.base}:{RUNBOOK}")).encode())
        self.assertEqual(self.evaluate(), [])

    def test_move_without_a_scope_migration_is_still_a_rename(self) -> None:
        self.write(RUNBOOK_TARGET, (self.root / RUNBOOK).read_bytes())
        (self.root / RUNBOOK).unlink()
        self.assertIn(("LIFECYCLE-RENAME", RUNBOOK_TARGET), self.evaluate())

    def test_scope_migration_must_match_its_catalog_envelope(self) -> None:
        self.write(RUNBOOK_TARGET, (self.root / RUNBOOK).read_bytes())
        (self.root / RUNBOOK).unlink()
        self.write(MIGRATION, scope_migration(RUNBOOK, RUNBOOK_TARGET).encode())
        self.write(INDEX, catalog((MIGRATION, f"{self.base}:{ADR}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", MIGRATION), self.evaluate())

    def gaps(self) -> list[str]:
        self.git("add", "-A", "--", ".")
        return [
            item.evidence_gap
            for item in VALIDATOR._evaluate_comparison(
                self.root, self.registry, mode="staged"
            )
        ]

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

    def test_scope_migration_envelope_must_name_the_base_object(self) -> None:
        original = (self.root / RUNBOOK).read_bytes()
        self.write(RUNBOOK, original + b"\nEarlier revision.\n")
        self.git("add", "--", RUNBOOK)
        self.git("commit", "--quiet", "-m", "earlier")
        earlier = self.git("rev-parse", "HEAD")
        self.write(RUNBOOK, original)
        self.git("add", "--", RUNBOOK)
        self.git("commit", "--quiet", "-m", "current")
        self.write(RUNBOOK_TARGET, original)
        (self.root / RUNBOOK).unlink()
        self.write(MIGRATION, scope_migration(RUNBOOK, RUNBOOK_TARGET).encode())
        self.write(INDEX, catalog((MIGRATION, f"{earlier}:{RUNBOOK}")).encode())
        self.assertIn(("LIFECYCLE-EVIDENCE", MIGRATION), self.evaluate())

    def test_resolved_incident_is_retained_with_its_postmortem(self) -> None:
        incident = "docs/05.operations/incidents/2026/inc-0001-example/incident.md"
        self.write(
            incident,
            b'---\ntitle: "Example"\nversion: "1.0.0"\ntype: "operation/incident"\n'
            b'status: "closed"\nowner: "platform"\nupdated: "2026-09-15"\n'
            b'layer: "operations"\nartifact_id: "inc-2026-0001"\n---\n\n# Example\n',
        )
        self.git("add", "--", incident)
        self.git("commit", "--quiet", "-m", "incident")
        head = self.git("rev-parse", "HEAD")
        record = self.retain("resolved", incident)
        self.write(INDEX, catalog((record, f"{head}:{incident}")).encode())
        self.assertTrue(any("Postmortem" in gap for gap in self.gaps()))


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
