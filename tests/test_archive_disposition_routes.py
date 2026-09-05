"""ADR-0032 record routing must preserve lifecycle and Git recovery evidence."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
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
    ReviewedManifestRecord,
    validate_archive_records,
    validate_current_archive_authority,
)
import archive_validation  # noqa: E402
import archive_cutover  # noqa: E402
from document_contracts import load_registry  # noqa: E402
from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    LifecycleEvidenceContext,
    _archive_creation_evidence,
    document_from_text,
)
from test_archive_recovery import GitFixture  # noqa: E402


class ArchiveDispositionRoutesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load_registry(ROOT)
        self.source = PurePosixPath("docs/01.requirements/9000-fixture.md")
        self.successor = PurePosixPath("docs/01.requirements/9001-successor.md")

    def creation(
        self, category: str, status: str, reason: str, *, record_status="archived"
    ):
        target = PurePosixPath("docs/98.archive", category, *self.source.parts[1:])
        replacement = self.successor.as_posix() if reason == "superseded" else None
        text = (
            "---\n"
            "type: archive/tombstone\n"
            f"status: {record_status}\n"
            f"original_path: {self.source}\n"
            f"archive_reason: {reason}\n"
            f"replacement: {replacement if replacement else 'null'}\n"
            "---\n"
        )
        record = document_from_text(self.registry, target, text)
        base = {self.source: LifecycleDocument(self.source, "sdlc/requirement", status)}
        proposed = {
            target: record,
            self.successor: LifecycleDocument(
                self.successor, "sdlc/requirement", "active"
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
        commit, blob = GitFixture(self.root).commit(self.source, self.payload)
        self.recovered = recover_git_blob(self.root, self.source, commit)
        GitFixture(self.root).commit(
            "docs/01.requirements/9001-successor.md",
            b"---\ntype: sdlc/requirement\nstatus: active\n---\n# Successor\n",
        )
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
        self.metadata.update(archive_reason="retired", replacement=None)
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
                proposed_registry=load_registry(ROOT),
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
                archive_validation, "_reviewed_manifest_records", return_value={}
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

    def cutover_report(
        self,
        *,
        identity=True,
        blob=None,
        status="superseded",
        valid=True,
        profile="sdlc/architecture-decision",
        historical_link=True,
    ):
        path = "docs/98.archive/superseded/01.requirements/9000-fixture.md"
        adr = "docs/02.architecture/decisions/9000-fixture.md"
        content = render_fixture_archive_envelope(
            self.metadata, self.recovered, self.payload
        )
        row = ReviewedManifestRecord(
            path,
            self.source,
            self.metadata["source_commit"],
            blob or self.metadata["source_blob"],
        )
        report = SimpleNamespace(
            diagnostics=(),
            valid=valid,
            record_link_counts=((path, 0),),
            record_count=1,
            historical_link_count=0,
            reviewed_manifest_records=(),
            additive_record_sources=(row,) if identity else (),
        )
        text = f"---\ntype: {profile}\nstatus: {status}\n---\n" + (
            "[Historical requirement](../../98.archive/superseded/01.requirements/9000-fixture.md)\n"
            if historical_link
            else "# Current work\n"
        )
        read_bytes = Path.read_bytes
        read_text = Path.read_text
        with (
            mock.patch.object(
                archive_cutover, "_finite_cutover_base_diagnostics", return_value=()
            ),
            mock.patch.object(
                archive_cutover, "load_registry", return_value=load_registry(ROOT)
            ),
            mock.patch.object(
                archive_cutover, "validate_repository_archive", return_value=report
            ),
            mock.patch.object(
                archive_cutover, "_tracked_regular_blobs", return_value={}
            ),
            mock.patch.object(
                archive_cutover, "build_work107_migration_rows", return_value=()
            ),
            mock.patch.object(
                archive_cutover, "_sealed_staged_ledgers", return_value=()
            ),
            mock.patch.object(archive_cutover, "_git_paths", return_value=(adr,)),
            mock.patch.object(
                archive_cutover,
                "_regular_file",
                side_effect=lambda root, value: value in {path, adr},
            ),
            mock.patch.object(archive_cutover, "_secret_classifier", return_value=None),
            mock.patch.object(
                Path,
                "read_bytes",
                lambda current: (
                    content if current == self.root / path else read_bytes(current)
                ),
            ),
            mock.patch.object(
                Path,
                "read_text",
                lambda current, *args, **kwargs: (
                    text
                    if current == self.root / adr
                    else read_text(current, *args, **kwargs)
                ),
            ),
        ):
            return archive_cutover.validate_repository_cutover(self.root)

    def test_cutover_consumes_only_validated_additive_source_identity(self) -> None:
        report = self.cutover_report()
        self.assertNotIn(
            "ARCHIVE-SOURCE-OWNERSHIP", {d.code for d in report.diagnostics}
        )

    def test_cutover_rejects_unvalidated_or_mismatched_additive_source(self) -> None:
        for options in ({"identity": False}, {"blob": "0" * 40}, {"valid": False}):
            with self.subTest(options=options):
                report = self.cutover_report(**options)
                self.assertIn(
                    "ARCHIVE-SOURCE-OWNERSHIP", {d.code for d in report.diagnostics}
                )

    def test_cutover_preserves_terminal_historical_link_status(self) -> None:
        report = self.cutover_report(status="superseded")
        self.assertNotIn(
            "ARCHIVE-DIRECT-CURRENT-LINK", {d.code for d in report.diagnostics}
        )
        self.assertNotIn(
            "ARCHIVE-CURRENT-STATUS-INVALID", {d.code for d in report.diagnostics}
        )

    def test_cutover_admits_registry_work_states_without_record_authority(self) -> None:
        for status in ("queued", "blocked", "in-progress", "cancelled"):
            with self.subTest(status=status):
                report = self.cutover_report(
                    profile="sdlc/task", status=status, historical_link=False
                )
                self.assertNotIn(
                    "ARCHIVE-CURRENT-STATUS-INVALID",
                    {d.code for d in report.diagnostics},
                )

    def test_cutover_uses_registry_current_class_for_work_record_links(self) -> None:
        for status in ("blocked", "in-progress"):
            with self.subTest(status=status):
                report = self.cutover_report(profile="sdlc/task", status=status)
                self.assertIn(
                    "ARCHIVE-DIRECT-CURRENT-LINK", {d.code for d in report.diagnostics}
                )

    def test_cutover_rejects_unknown_and_wrong_family_status(self) -> None:
        for status in ("invented", "active"):
            with self.subTest(status=status):
                report = self.cutover_report(
                    profile="sdlc/task", status=status, historical_link=False
                )
                self.assertIn(
                    "ARCHIVE-CURRENT-STATUS-INVALID",
                    {d.code for d in report.diagnostics},
                )

    def test_cutover_still_rejects_accepted_adr_record_authority(self) -> None:
        report = self.cutover_report(status="accepted")
        self.assertIn(
            "ARCHIVE-DIRECT-CURRENT-LINK", {d.code for d in report.diagnostics}
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
