"""ADR-0032 record routing must preserve lifecycle and Git recovery evidence."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from archive_recovery import (  # noqa: E402
    recover_git_blob,
    render_fixture_archive_envelope,
    validate_archive_metadata,
)
from archive_validation import (  # noqa: E402
    ArchiveRecord,
    CurrentMarkdownDocument,
    MigrationDisposition,
    MigrationProof,
    validate_archive_records,
    validate_current_archive_authority,
)
import archive_validation  # noqa: E402
from document_contracts import load_registry  # noqa: E402
from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    LifecycleEvidenceContext,
    _archive_creation_evidence,
    document_from_text,
)
from tests.archive_generation_fixture import (  # noqa: E402
    REGISTRY_PATH,
    legacy_registry,
    legacy_registry_bytes,
)
from tests.git_fixture import GitFixture  # noqa: E402


class ArchiveDispositionRoutesTest(unittest.TestCase):
    def setUp(self) -> None:
        # ADR-0032 record routing is the frozen generation's own contract.
        self.registry = legacy_registry()
        self.source = PurePosixPath("docs/01.requirements/9000-fixture.md")
        self.successor = PurePosixPath("docs/01.requirements/9001-successor.md")

    def creation(
        self, category: str, status: str, reason: str, *, record_status="archived"
    ):
        target = PurePosixPath("docs/98.archive", category, *self.source.parts[1:])
        replacement = self.successor.as_posix() if reason == "superseded" else "none"
        text = (
            "---\n"
            "version: 1.0.0\n"
            "type: archive/tombstone\n"
            "layer: archive\n"
            f"status: {record_status}\n"
            f"original_path: {self.source}\n"
            f"archive_reason: {reason}\n"
            f"replacement: {replacement}\n"
            "---\n"
        )
        record = document_from_text(self.registry, target, text)
        base = {self.source: LifecycleDocument(self.source, "sdlc/requirement", status)}
        proposed = {
            target: record,
            self.successor: document_from_text(
                self.registry,
                self.successor,
                "---\ntype: sdlc/requirement\nstatus: active\n---\n",
            ),
        }
        evidence = LifecycleEvidenceContext(
            base,
            {},
            frozenset({self.source, target}),
            frozenset(),
            frozenset({target}),
            frozenset({target}),
        )
        return _archive_creation_evidence(
            self.registry, [record], base, proposed, evidence, base_mode="staged"
        )

    def test_superseded_source_uses_superseded_stage_mirror(self) -> None:
        diagnostics, removals = self.creation("superseded", "superseded", "superseded")
        self.assertEqual(diagnostics, [])
        self.assertEqual(removals, {self.source})

    def test_retired_source_uses_tombstones_stage_mirror(self) -> None:
        diagnostics, removals = self.creation("tombstones", "retired", "retired")
        self.assertEqual(diagnostics, [])
        self.assertEqual(removals, {self.source})

    def test_record_reason_cannot_select_the_wrong_retention_class(self) -> None:
        diagnostics, removals = self.creation("tombstones", "superseded", "superseded")
        self.assertTrue(diagnostics)
        self.assertEqual(removals, set())

    def test_active_source_must_have_a_declared_terminal_edge(self) -> None:
        diagnostics, removals = self.creation("superseded", "active", "superseded")
        self.assertEqual(diagnostics, [])
        self.assertEqual(removals, {self.source})

    def test_draft_cannot_skip_activation_to_superseded(self) -> None:
        diagnostics, removals = self.creation("superseded", "draft", "superseded")
        self.assertTrue(diagnostics)
        self.assertEqual(removals, set())

    def test_adr_body_cannot_leave_the_decision_log(self) -> None:
        self.source = PurePosixPath("docs/02.architecture/decisions/9000-fixture.md")
        diagnostics, removals = self.creation("superseded", "superseded", "superseded")
        self.assertTrue(diagnostics)
        self.assertEqual(removals, set())

    def test_nonarchived_record_cannot_admit_source_removal(self) -> None:
        diagnostics, removals = self.creation(
            "superseded", "active", "superseded", record_status="active"
        )
        self.assertTrue(diagnostics)
        self.assertEqual(removals, set())

    def test_nonstring_reason_is_a_diagnostic_not_an_exception(self) -> None:
        diagnostics, removals = self.creation("superseded", "active", "[superseded]")
        self.assertTrue(diagnostics)
        self.assertEqual(removals, set())


class ArchiveDispositionRecoveryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="archive-disposition-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = "docs/01.requirements/9000-fixture.md"
        self.payload = b"---\ntype: sdlc/requirement\nstatus: active\n---\n# Exact source fixture\n"
        commit, blobs = GitFixture(self.root).commit_many(
            {
                REGISTRY_PATH: legacy_registry_bytes(),
                self.source: self.payload,
                "docs/01.requirements/9001-successor.md": (
                    b"---\ntype: sdlc/requirement\nstatus: active\n---\n# Successor\n"
                ),
            }
        )
        # Keep historical Git evidence separate from this standalone current tree.
        (self.root / REGISTRY_PATH).unlink()
        blob = blobs[self.source]
        self.recovered = recover_git_blob(self.root, self.source, commit)
        self.metadata = {
            "title": "Archive fixture",
            "version": "1.0.0",
            "type": "archive/tombstone",
            "layer": "archive",
            "status": "archived",
            "owner": "platform",
            "updated": "2026-09-05",
            "artifact_id": "tomb-PRD-9000",
            "original_artifact_id": "REQ-9000",
            "original_type": "sdlc/requirement",
            "original_path": self.source,
            "archived_on": "2026-09-05",
            "archive_reason": "superseded",
            "replacement": "docs/01.requirements/9001-successor.md",
            "source_commit": commit,
            "source_blob": blob,
            "content_sha256": hashlib.sha256(self.payload).hexdigest(),
        }

    def check_record(self, category: str):
        record = ArchiveRecord(
            f"docs/98.archive/{category}/01.requirements/9000-fixture.md",
            render_fixture_archive_envelope(
                self.metadata, self.recovered, self.payload
            ),
        )
        return validate_archive_records(self.root, [record])

    def test_superseded_record_recovery_accepts_exact_classified_mirror(self) -> None:
        report = self.check_record("superseded")
        self.assertEqual(report.diagnostics, ())

    def test_tombstone_recovery_accepts_exact_classified_mirror(self) -> None:
        self.metadata.update(archive_reason="retired", replacement="none")
        report = self.check_record("tombstones")
        self.assertEqual(report.diagnostics, ())

    def test_wrong_record_class_still_fails_recovery(self) -> None:
        report = self.check_record("tombstones")
        self.assertIn("ARCHIVE-MIRROR-MISMATCH", {d.code for d in report.diagnostics})

    def test_current_template_metadata_order_is_accepted(self) -> None:
        keys = (
            "title",
            "version",
            "type",
            "status",
            "owner",
            "updated",
            "layer",
            "artifact_id",
            "original_artifact_id",
            "original_type",
            "original_path",
            "archived_on",
            "archive_reason",
            "replacement",
            "source_commit",
            "source_blob",
            "content_sha256",
        )
        metadata = {key: self.metadata[key] for key in keys}
        self.assertIsNotNone(validate_archive_metadata(metadata))

    def test_requirement_record_uses_current_req_identity(self) -> None:
        self.metadata["artifact_id"] = "tomb-REQ-9000"
        self.assertEqual(self.check_record("superseded").diagnostics, ())

    def test_frontmatter_and_profile_admit_the_same_requirement_record_ids(
        self,
    ) -> None:
        schema = json.loads(
            (ROOT / "docs/99.templates/contracts/frontmatter.schema.json").read_text()
        )
        validator = Draft202012Validator(schema)
        profile = next(
            p
            for p in load_registry(ROOT).profiles
            if p.profile_id == "archive/tombstone"
        )
        for identity, valid in (
            ("tomb-REQ-9000", True),
            ("tomb-PRD-9000", True),
            ("TOMB-REQ-9000", False),
            ("tomb-req-9000", False),
            ("tomb-REQ-900", False),
            ("tomb-REQ-90000", False),
        ):
            with self.subTest(identity=identity):
                metadata = dict(self.metadata, artifact_id=identity)
                self.assertEqual(not list(validator.iter_errors(metadata)), valid)
                self.assertEqual(
                    re.fullmatch(profile.artifact_id_pattern, identity) is not None,
                    valid,
                )

    def test_registry_admits_req_record_without_retiring_prd_identity(self) -> None:
        profile = next(
            p
            for p in load_registry(ROOT).profiles
            if p.profile_id == "archive/tombstone"
        )
        for identity in ("tomb-REQ-9000", "tomb-PRD-9000"):
            with self.subTest(identity=identity):
                self.assertIsNotNone(
                    re.fullmatch(profile.artifact_id_pattern, identity)
                )
        for identity in ("TOMB-REQ-9000", "tomb-REQ-90", "tomb-UNKNOWN-9000"):
            with self.subTest(identity=identity):
                self.assertIsNone(re.fullmatch(profile.artifact_id_pattern, identity))

    def additive_report(self, *, category="superseded", proof=True, source_blob=None):
        path = f"docs/98.archive/{category}/01.requirements/9000-fixture.md"
        content = render_fixture_archive_envelope(
            self.metadata, self.recovered, self.payload
        )
        disposition = MigrationDisposition(
            "docs/98.archive/migrations/9000-fixture.md",
            self.metadata["source_commit"],
            source_blob or self.metadata["source_blob"],
            self.payload,
            "replaced",
            self.metadata["replacement"],
        )
        proved = (
            None
            if proof is None
            else MigrationProof(
                {self.source: disposition.target},
                {},
                dispositions={self.source: disposition} if proof else {},
                proposed_registry=legacy_registry(),
            )
        )
        with (
            mock.patch.object(
                archive_validation,
                "_repository_archive_records",
                return_value=({path: content}, [], proved),
            ),
            mock.patch.object(
                archive_validation,
                "_work107_stable_rows",
                return_value={
                    "docs/98.archive/legacy.md": {
                        "legacy_path": "docs/01.requirements/8999-legacy.md"
                    }
                },
            ),
            mock.patch.object(
                archive_validation, "_read_repository_index", return_value=""
            ),
            mock.patch.object(
                archive_validation,
                "repository_migration_proof",
                side_effect=AssertionError("inventory proof must not be rediscovered"),
            ),
        ):
            return archive_validation.validate_repository_archive(self.root, {})

    def test_additive_record_uses_its_own_sealed_disposition_not_work107_census(
        self,
    ) -> None:
        report = self.additive_report()
        self.assertNotIn(
            "ARCHIVE-MIGRATION-PARITY", {d.code for d in report.diagnostics}
        )

    def test_addition_without_sealed_disposition_still_fails_parity(self) -> None:
        report = self.additive_report(proof=False)
        self.assertIn("ARCHIVE-MIGRATION-PARITY", {d.code for d in report.diagnostics})

    def test_addition_without_valid_inventory_proof_still_fails_parity(self) -> None:
        report = self.additive_report(proof=None)
        self.assertIn("ARCHIVE-MIGRATION-PARITY", {d.code for d in report.diagnostics})
        self.assertEqual(report.additive_record_sources, ())

    def test_wrong_class_addition_still_fails_parity(self) -> None:
        report = self.additive_report(category="tombstones")
        self.assertIn("ARCHIVE-MIGRATION-PARITY", {d.code for d in report.diagnostics})

    def test_wrong_disposition_source_identity_still_fails_parity(self) -> None:
        report = self.additive_report(source_blob="0" * 40)
        self.assertIn("ARCHIVE-MIGRATION-PARITY", {d.code for d in report.diagnostics})

    def test_additive_record_requires_the_source_terminal_edge(self) -> None:
        self.payload = self.payload.replace(b"status: active", b"status: draft")
        commit, blob = GitFixture(self.root).commit(self.source, self.payload)
        self.recovered = recover_git_blob(self.root, self.source, commit)
        self.metadata.update(
            source_commit=commit,
            source_blob=blob,
            content_sha256=hashlib.sha256(self.payload).hexdigest(),
        )
        report = self.additive_report()
        self.assertIn("ARCHIVE-MIGRATION-PARITY", {d.code for d in report.diagnostics})

    def authority_report(
        self,
        *,
        status: str,
        profile: str = "sdlc/architecture-decision",
        historical_link: bool = True,
    ):
        archive = "docs/98.archive/superseded/01.requirements/9000-fixture.md"
        markdown = (
            "[Historical requirement](../../98.archive/superseded/01.requirements/9000-fixture.md)\n"
            if historical_link
            else "# Current work\n"
        )
        document = CurrentMarkdownDocument(
            "docs/02.architecture/decisions/9000-fixture.md",
            markdown,
            profile,
            status,
        )
        return validate_current_archive_authority(
            [document],
            individual_archive_paths=frozenset({archive}),
            registry=load_registry(ROOT),
        )

    def test_terminal_historical_link_is_not_current_authority(self) -> None:
        report = self.authority_report(status="superseded")
        codes = {item.code for item in report.diagnostics}
        self.assertNotIn("ARCHIVE-DIRECT-CURRENT-LINK", codes)
        self.assertNotIn("ARCHIVE-CURRENT-STATUS-INVALID", codes)

    def test_registry_task_states_are_admitted_without_record_authority(self) -> None:
        for status in ("draft", "ready", "blocked", "in-progress", "cancelled"):
            with self.subTest(status=status):
                report = self.authority_report(
                    status=status,
                    profile="sdlc/task",
                    historical_link=False,
                )
                self.assertNotIn(
                    "ARCHIVE-CURRENT-STATUS-INVALID",
                    {item.code for item in report.diagnostics},
                )

    def test_current_task_states_cannot_cite_record_as_authority(self) -> None:
        for status in ("blocked", "in-progress"):
            with self.subTest(status=status):
                report = self.authority_report(status=status, profile="sdlc/task")
                self.assertIn(
                    "ARCHIVE-DIRECT-CURRENT-LINK",
                    {item.code for item in report.diagnostics},
                )

    def test_invalid_task_states_and_accepted_adr_boundary(self) -> None:
        for status in ("invented", "active"):
            with self.subTest(status=status):
                report = self.authority_report(
                    status=status,
                    profile="sdlc/task",
                    historical_link=False,
                )
                self.assertIn(
                    "ARCHIVE-CURRENT-STATUS-INVALID",
                    {item.code for item in report.diagnostics},
                )
        report = self.authority_report(status="accepted")
        self.assertIn(
            "ARCHIVE-DIRECT-CURRENT-LINK", {item.code for item in report.diagnostics}
        )

    def test_active_owner_cannot_use_a_superseded_record_as_authority(self) -> None:
        archive = "docs/98.archive/superseded/01.requirements/9000-fixture.md"
        document = CurrentMarkdownDocument(
            "docs/01.requirements/9001-successor.md",
            "[source](../98.archive/superseded/01.requirements/9000-fixture.md)\n",
            "sdlc/requirement",
            "active",
        )
        report = validate_current_archive_authority(
            [document], individual_archive_paths=frozenset({archive})
        )
        self.assertIn(
            "ARCHIVE-DIRECT-CURRENT-LINK", {d.code for d in report.diagnostics}
        )


if __name__ == "__main__":
    unittest.main()
