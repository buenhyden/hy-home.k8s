#!/usr/bin/env python3
"""Focused RED/GREEN fixtures for ARWB-002 archive validation interfaces."""

from __future__ import annotations

import dataclasses
import hashlib
import io
import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import types
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.archive_recovery import (  # noqa: E402
    ARCHIVE_ENVELOPE_MARKER,
    recover_git_blob,
    render_fixture_archive_envelope,
)
from scripts import archive_validation  # noqa: E402
from scripts.archive_validation import (  # noqa: E402
    ArchiveRecord,
    CurrentMarkdownDocument,
    validate_archive_immutability,
    validate_archive_records,
    validate_current_archive_authority,
)


class GitFixture:
    """Create a bounded source-history fixture without production corpus reads."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.run("init", "--quiet")
        self.run("config", "user.email", "archive-validator@example.invalid")
        self.run("config", "user.name", "Archive Validator")

    def run(self, *args: str) -> bytes:
        completed = subprocess.run(
            ["git", *args],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"fixture Git command failed: {completed.stderr.decode(errors='replace')}"
            )
        return completed.stdout

    def commit_many(self, files: dict[str, bytes]) -> tuple[str, dict[str, str]]:
        for relative_path, payload in files.items():
            destination = self.root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
        self.run("--literal-pathspecs", "add", "--", *files)
        self.run("commit", "--quiet", "-m", "source fixture")
        commit = self.run("rev-parse", "HEAD").decode("ascii").strip()
        blobs = {
            path: self.run("rev-parse", f"HEAD:{path}").decode("ascii").strip()
            for path in files
        }
        return commit, blobs


class ArchiveValidationTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="archive-validation-")
        self.root = Path(self.temporary.name)
        self.git = GitFixture(self.root)
        self.original_path = "docs/03.specs/900-fixture/spec.md"
        self.target_path = "docs/03.specs/900-fixture/target[*].md"
        self.payload = (
            b"# Historical fixture\n\n"
            b"[target](target%5B*%5D.md)\n\n"
            b"```markdown\n[not rendered](missing-in-code.md)\n```\n"
        )
        self.commit, blobs = self.git.commit_many(
            {
                self.original_path: self.payload,
                self.target_path: b"# Historical target\n",
            }
        )
        self.blob = blobs[self.original_path]
        self.archive_path = "docs/98.archive/03.specs/900-fixture/spec.md"
        self.recovered = recover_git_blob(self.root, self.original_path, self.commit)
        self.metadata = {
            "title": "Archive: Historical fixture",
            "type": "content/archive",
            "status": "archived",
            "owner": "platform",
            "updated": "2026-07-18",
            "original_type": "sdlc/spec",
            "original_path": self.original_path,
            "archived_on": "2026-07-18",
            "archive_reason": "superseded",
            "replacement": "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
            "source_commit": self.commit,
            "source_blob": self.blob,
            "content_sha256": hashlib.sha256(self.payload).hexdigest(),
        }
        self.archive_bytes = render_fixture_archive_envelope(
            self.metadata, self.recovered, self.payload
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def record(
        self,
        *,
        archive_path: str | None = None,
        archive_bytes: bytes | None = None,
    ) -> ArchiveRecord:
        return ArchiveRecord(
            path=archive_path or self.archive_path,
            content=self.archive_bytes if archive_bytes is None else archive_bytes,
        )

    @staticmethod
    def codes(report: object) -> tuple[str, ...]:
        return tuple(diagnostic.code for diagnostic in report.diagnostics)

    def test_red_metadata_order_and_type_fail_closed(self) -> None:
        wrong_type = self.archive_bytes.replace(
            b'type: "content/archive"', b'type: "content/invalid"', 1
        )
        owner_line = b'owner: "platform"\n'
        updated_line = b'updated: "2026-07-18"\n'
        wrong_order = self.archive_bytes.replace(
            owner_line + updated_line, updated_line + owner_line, 1
        )

        type_report = validate_archive_records(
            self.root, (self.record(archive_bytes=wrong_type),)
        )
        order_report = validate_archive_records(
            self.root, (self.record(archive_bytes=wrong_order),)
        )

        self.assertEqual(self.codes(type_report), ("ARCHIVE-METADATA-TYPE",))
        self.assertEqual(self.codes(order_report), ("ARCHIVE-METADATA-KEYS",))

    def test_red_blob_digest_mismatch_and_payload_mutation_fail_closed(self) -> None:
        wrong_blob = self.archive_bytes.replace(
            self.blob.encode("ascii"), b"0" * len(self.blob), 1
        )
        payload_mutation = self.archive_bytes[:-1] + b"!"

        blob_report = validate_archive_records(
            self.root, (self.record(archive_bytes=wrong_blob),)
        )
        mutation_report = validate_archive_records(
            self.root, (self.record(archive_bytes=payload_mutation),)
        )

        self.assertEqual(self.codes(blob_report), ("ARCHIVE-METADATA-PROVENANCE",))
        self.assertEqual(self.codes(mutation_report), ("ARCHIVE-PAYLOAD-DIGEST",))

    def test_red_wrong_mirror_fails_closed(self) -> None:
        report = validate_archive_records(
            self.root,
            (
                self.record(
                    archive_path="docs/98.archive/03.specs/900-fixture/wrong.md"
                ),
            ),
        )

        self.assertEqual(self.codes(report), ("ARCHIVE-MIRROR-MISMATCH",))

    def test_red_source_tree_miss_ignores_current_tree(self) -> None:
        missing_payload = b"# Historical\n\n[current only](current-only.md)\n"
        source_commit, _ = self.git.commit_many({self.original_path: missing_payload})
        recovered = recover_git_blob(self.root, self.original_path, source_commit)
        metadata = dict(self.metadata)
        metadata.update(
            {
                "source_commit": source_commit,
                "source_blob": recovered.source_blob,
                "content_sha256": recovered.content_sha256,
            }
        )
        archive_bytes = render_fixture_archive_envelope(
            metadata, recovered, missing_payload
        )
        current_only = self.root / "docs/03.specs/900-fixture/current-only.md"
        current_only.write_text(
            "# Exists only in the current worktree\n", encoding="utf-8"
        )

        report = validate_archive_records(
            self.root, (self.record(archive_bytes=archive_bytes),)
        )

        self.assertEqual(self.codes(report), ("ARCHIVE-HISTORICAL-LINK-MISSING",))
        self.assertEqual(report.historical_link_count, 1)

    def test_green_historical_links_use_rendered_commonmark_source_view(self) -> None:
        report = validate_archive_records(self.root, (self.record(),))

        self.assertEqual(self.codes(report), ())
        self.assertEqual(report.historical_link_count, 1)

    def test_red_archive_record_reactivation_is_inventory_independent(self) -> None:
        record_document = CurrentMarkdownDocument(
            path=self.archive_path,
            markdown="# Must remain historical\n",
            profile="sdlc/spec",
            status="active",
        )
        index_document = CurrentMarkdownDocument(
            path="docs/98.archive/README.md",
            markdown="# Current archive index\n",
            profile="readme/stage-index",
            status="accepted",
        )

        report = validate_current_archive_authority(
            (record_document, index_document),
            individual_archive_paths=frozenset(
                {"docs/98.archive/03.specs/999-other/spec.md"}
            ),
        )

        self.assertEqual(self.codes(report), ("ARCHIVE-REACTIVATED",))

    def test_red_missing_empty_and_invalid_archive_inventory_fail_closed(self) -> None:
        empty = validate_current_archive_authority(())
        invalid_container = validate_current_archive_authority(
            (),
            individual_archive_paths=None,  # type: ignore[arg-type]
        )
        invalid_members = validate_current_archive_authority(
            (), individual_archive_paths=frozenset({1, "docs/98.archive/README.md"})
        )

        self.assertEqual(self.codes(empty), ("ARCHIVE-INVENTORY-MISSING",))
        self.assertEqual(self.codes(invalid_container), ("ARCHIVE-INVENTORY-CONTRACT",))
        self.assertEqual(
            self.codes(invalid_members),
            ("ARCHIVE-INVENTORY-PATH-INVALID",) * 2,
        )

    def test_red_current_status_profile_markdown_and_path_contracts_fail_closed(
        self,
    ) -> None:
        current_path = "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md"
        cases = (
            (
                "uppercase-status",
                CurrentMarkdownDocument(
                    current_path, "# Current\n", "sdlc/spec", "ACTIVE"
                ),
                "ARCHIVE-CURRENT-STATUS-INVALID",
            ),
            (
                "unknown-status",
                CurrentMarkdownDocument(
                    current_path, "# Current\n", "sdlc/spec", "other"
                ),
                "ARCHIVE-CURRENT-STATUS-INVALID",
            ),
            (
                "none-status",
                CurrentMarkdownDocument(current_path, "# Current\n", "sdlc/spec", None),  # type: ignore[arg-type]
                "ARCHIVE-CURRENT-STATUS-INVALID",
            ),
            (
                "unhashable-status",
                CurrentMarkdownDocument(current_path, "# Current\n", "sdlc/spec", []),  # type: ignore[arg-type]
                "ARCHIVE-CURRENT-STATUS-INVALID",
            ),
            (
                "none-profile",
                CurrentMarkdownDocument(current_path, "# Current\n", None, "done"),  # type: ignore[arg-type]
                "ARCHIVE-CURRENT-PROFILE-INVALID",
            ),
            (
                "unknown-profile",
                CurrentMarkdownDocument(
                    current_path, "# Current\n", "unknown/profile", "done"
                ),
                "ARCHIVE-CURRENT-PROFILE-INVALID",
            ),
            (
                "non-text-markdown",
                CurrentMarkdownDocument(current_path, None, "sdlc/spec", "active"),  # type: ignore[arg-type]
                "ARCHIVE-CURRENT-CONTENT-TYPE",
            ),
            (
                "dot-path",
                CurrentMarkdownDocument(
                    "docs/./current.md", "# Current\n", "sdlc/spec", "active"
                ),
                "ARCHIVE-CURRENT-PATH-INVALID",
            ),
            (
                "root-dot-path",
                CurrentMarkdownDocument(".", "# Current\n", "sdlc/spec", "active"),
                "ARCHIVE-CURRENT-PATH-INVALID",
            ),
            (
                "repeated-separator",
                CurrentMarkdownDocument(
                    "docs//current.md", "# Current\n", "sdlc/spec", "active"
                ),
                "ARCHIVE-CURRENT-PATH-INVALID",
            ),
            (
                "non-string-path",
                CurrentMarkdownDocument([], "# Current\n", "sdlc/spec", "active"),  # type: ignore[arg-type]
                "ARCHIVE-CURRENT-PATH-INVALID",
            ),
        )
        inventory = frozenset({self.archive_path})
        for name, document, expected_code in cases:
            with self.subTest(name=name):
                report = validate_current_archive_authority(
                    (document,), individual_archive_paths=inventory
                )
                self.assertEqual(self.codes(report), (expected_code,))

    def test_red_public_sequence_inputs_and_elements_fail_closed(self) -> None:
        invalid_record_containers = (None, "records", b"records", {}, object())
        for value in invalid_record_containers:
            with self.subTest(api="records", value_type=type(value).__name__):
                report = validate_archive_records(self.root, value)  # type: ignore[arg-type]
                self.assertEqual(self.codes(report), ("ARCHIVE-RECORDS-CONTRACT",))
        report = validate_archive_records(self.root, [object()])  # type: ignore[list-item]
        self.assertEqual(self.codes(report), ("ARCHIVE-RECORD-CONTRACT",))
        malformed_records = validate_archive_records(
            self.root,
            (
                self.record(),
                ArchiveRecord(path=None, content=self.archive_bytes),  # type: ignore[arg-type]
                ArchiveRecord(path=[], content=self.archive_bytes),  # type: ignore[arg-type]
            ),
        )
        self.assertEqual(self.codes(malformed_records), ("ARCHIVE-PATH-INVALID",) * 2)

        invalid_root = validate_archive_records(None, (self.record(),))  # type: ignore[arg-type]
        self.assertEqual(self.codes(invalid_root), ("ARCHIVE-REPOSITORY-CONTRACT",))

        canonical_adapter = archive_validation._load_canonical_link_module()
        with self.assertRaisesRegex(
            ValueError,
            r"^source_path must be a canonical repository-relative POSIX path$",
        ):
            canonical_adapter.rendered_local_links("# Current\n", ".")

        invalid_document_containers = (None, "documents", b"documents", {}, object())
        for value in invalid_document_containers:
            with self.subTest(api="documents", value_type=type(value).__name__):
                report = validate_current_archive_authority(
                    value,  # type: ignore[arg-type]
                    individual_archive_paths=frozenset({self.archive_path}),
                )
                self.assertEqual(
                    self.codes(report), ("ARCHIVE-CURRENT-DOCUMENTS-CONTRACT",)
                )
        report = validate_current_archive_authority(
            [object()],  # type: ignore[list-item]
            individual_archive_paths=frozenset({self.archive_path}),
        )
        self.assertEqual(self.codes(report), ("ARCHIVE-CURRENT-DOCUMENT-CONTRACT",))

    def test_red_immutability_mapping_keys_and_values_fail_closed(self) -> None:
        invalid_mappings = (None, [], "mapping")
        for value in invalid_mappings:
            with self.subTest(side="baseline", value_type=type(value).__name__):
                report = validate_archive_immutability(value, {})  # type: ignore[arg-type]
                self.assertEqual(self.codes(report), ("ARCHIVE-BASELINE-CONTRACT",))
            with self.subTest(side="proposed", value_type=type(value).__name__):
                report = validate_archive_immutability({}, value)  # type: ignore[arg-type]
                self.assertEqual(self.codes(report), ("ARCHIVE-PROPOSED-CONTRACT",))

        malformed = (
            ({"docs/98.archive/./bad.md": b"payload"}, {}, "ARCHIVE-PATH-INVALID"),
            ({self.archive_path: []}, {}, "ARCHIVE-CONTENT-TYPE"),
            ({}, {"docs/98.archive//bad.md": b"payload"}, "ARCHIVE-PATH-INVALID"),
            ({}, {self.archive_path: []}, "ARCHIVE-CONTENT-TYPE"),
        )
        for baseline, proposed, expected_code in malformed:
            with self.subTest(expected_code=expected_code):
                report = validate_archive_immutability(  # type: ignore[arg-type]
                    baseline, proposed
                )
                self.assertEqual(self.codes(report), (expected_code,))

    def test_red_poisoned_predictable_module_cache_is_not_trusted(self) -> None:
        poison_name = "_archive_canonical_links_and_owners"
        poison = types.ModuleType(poison_name)
        poison.rendered_local_links = lambda *_args: ()
        previous = sys.modules.get(poison_name)
        sys.modules[poison_name] = poison
        archive_validation._load_canonical_link_module.cache_clear()
        try:
            report = validate_archive_records(self.root, (self.record(),))
        finally:
            archive_validation._load_canonical_link_module.cache_clear()
            if previous is None:
                sys.modules.pop(poison_name, None)
            else:
                sys.modules[poison_name] = previous

        self.assertEqual(self.codes(report), ())
        self.assertEqual(report.historical_link_count, 1)

    def test_red_adapter_import_and_call_exceptions_are_payload_free(self) -> None:
        sentinel = "SENSITIVE-ADAPTER-DETAIL-DO-NOT-PRINT"
        archive_validation._load_canonical_link_module.cache_clear()
        with mock.patch.object(
            archive_validation.importlib.util,
            "spec_from_file_location",
            side_effect=OSError(sentinel),
        ):
            import_report = validate_archive_records(self.root, (self.record(),))
        archive_validation._load_canonical_link_module.cache_clear()

        def raise_key_error(*_args: object) -> object:
            raise KeyError(sentinel)

        with mock.patch.object(
            archive_validation,
            "_rendered_link_adapter",
            return_value=raise_key_error,
        ):
            call_report = validate_archive_records(self.root, (self.record(),))

        for report in (import_report, call_report):
            self.assertEqual(self.codes(report), ("ARCHIVE-LINK-ADAPTER-FAILURE",))
            self.assertNotIn(sentinel, repr(report))
            self.assertNotIn(sentinel, " ".join(map(str, report.diagnostics)))

    def test_red_malformed_adapter_return_and_link_shapes_fail_closed(self) -> None:
        sentinel = "SENSITIVE-MALFORMED-LINK-DO-NOT-PRINT"
        malformed_returns = (
            {"kind": "local"},
            "links",
            (object(),),
            (types.SimpleNamespace(kind="surprise", target=None, raw_target=sentinel),),
            (
                types.SimpleNamespace(
                    kind="local", target=sentinel, raw_target=sentinel
                ),
            ),
        )
        for returned in malformed_returns:
            with self.subTest(return_type=type(returned).__name__):
                with mock.patch.object(
                    archive_validation,
                    "_rendered_link_adapter",
                    return_value=lambda *_args: returned,
                ):
                    report = validate_archive_records(self.root, (self.record(),))
                self.assertEqual(self.codes(report), ("ARCHIVE-LINK-ADAPTER-FAILURE",))
                self.assertNotIn(sentinel, repr(report))

    def test_red_archive_reactivation_fails_closed(self) -> None:
        report = validate_current_archive_authority(
            (
                CurrentMarkdownDocument(
                    path=self.archive_path,
                    markdown="# Incorrectly active archive\n",
                    profile="content/archive",
                    status="active",
                ),
            ),
            individual_archive_paths=frozenset({self.archive_path}),
        )

        self.assertEqual(self.codes(report), ("ARCHIVE-REACTIVATED",))

    def test_red_active_direct_link_fails_but_archive_index_is_permitted(self) -> None:
        direct = CurrentMarkdownDocument(
            path="docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
            markdown=(
                "# Current\n\n[record](../../98.archive/03.specs/900-fixture/spec.md)\n"
            ),
            profile="sdlc/spec",
            status="active",
        )
        via_index = CurrentMarkdownDocument(
            path="docs/03.specs/0037-active-corpus-and-execution-retention/spec.md",
            markdown="# Current\n\n[archive index](../../98.archive/README.md)\n",
            profile="sdlc/spec",
            status="active",
        )

        report = validate_current_archive_authority(
            (direct, via_index),
            individual_archive_paths=frozenset({self.archive_path}),
        )

        self.assertEqual(self.codes(report), ("ARCHIVE-DIRECT-CURRENT-LINK",))

    def test_green_noncurrent_direct_link_does_not_claim_current_authority(
        self,
    ) -> None:
        document = CurrentMarkdownDocument(
            path="docs/98.archive/README.md",
            markdown=f"[record]({self.archive_path.removeprefix('docs/98.archive/')})\n",
            profile="readme/stage-index",
            status="archived",
        )

        report = validate_current_archive_authority(
            (document,), individual_archive_paths=frozenset({self.archive_path})
        )

        self.assertEqual(self.codes(report), ())

    def test_red_duplicate_original_path_authority_fails_closed(self) -> None:
        report = validate_archive_records(
            self.root,
            (
                self.record(),
                self.record(
                    archive_path="docs/98.archive/03.specs/900-fixture/duplicate.md"
                ),
            ),
        )

        self.assertIn("ARCHIVE-DUPLICATE-ORIGINAL-PATH", self.codes(report))

    def test_red_existing_archive_mutation_and_deletion_fail_closed(self) -> None:
        baseline = {self.archive_path: self.archive_bytes}

        mutation = validate_archive_immutability(
            baseline,
            {self.archive_path: self.archive_bytes[:-1] + b"!"},
        )
        deletion = validate_archive_immutability(baseline, {})

        self.assertEqual(self.codes(mutation), ("ARCHIVE-IMMUTABLE-MUTATION",))
        self.assertEqual(self.codes(deletion), ("ARCHIVE-IMMUTABLE-DELETION",))

    def test_green_archive_addition_preserves_existing_records(self) -> None:
        baseline = {self.archive_path: self.archive_bytes}
        proposed = dict(baseline)
        proposed["docs/98.archive/03.specs/901-new/spec.md"] = b"new fixture"

        report = validate_archive_immutability(baseline, proposed)

        self.assertEqual(self.codes(report), ())

    def test_red_diagnostics_and_dataclass_repr_do_not_disclose_payload_values(
        self,
    ) -> None:
        sentinel = "SENSITIVE-LINK-TARGET-DO-NOT-PRINT.md"
        payload = f"# Historical\n\n[private]({sentinel})\n".encode()
        source_commit, _ = self.git.commit_many({self.original_path: payload})
        recovered = recover_git_blob(self.root, self.original_path, source_commit)
        metadata = dict(self.metadata)
        metadata.update(
            {
                "source_commit": source_commit,
                "source_blob": recovered.source_blob,
                "content_sha256": recovered.content_sha256,
            }
        )
        content = render_fixture_archive_envelope(metadata, recovered, payload)
        record = self.record(archive_bytes=content)

        report = validate_archive_records(self.root, (record,))

        rendered = repr(record) + repr(report) + " ".join(map(str, report.diagnostics))
        self.assertNotIn(sentinel, rendered)
        self.assertNotIn("Historical", rendered)
        self.assertNotIn("archive-envelope", rendered)

    def test_green_validator_module_is_import_only(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/archive_validation.py")],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, b"")
        self.assertEqual(completed.stderr, b"")

    def test_green_marker_like_payload_remains_opaque_to_envelope_parser(self) -> None:
        marker_payload = b"# Historical\n\n" + ARCHIVE_ENVELOPE_MARKER + b"\n"
        source_commit, _ = self.git.commit_many({self.original_path: marker_payload})
        recovered = recover_git_blob(self.root, self.original_path, source_commit)
        metadata = dict(self.metadata)
        metadata.update(
            {
                "source_commit": source_commit,
                "source_blob": recovered.source_blob,
                "content_sha256": recovered.content_sha256,
            }
        )
        archive_bytes = render_fixture_archive_envelope(
            metadata, recovered, marker_payload
        )

        report = validate_archive_records(
            self.root, (self.record(archive_bytes=archive_bytes),)
        )

        self.assertEqual(self.codes(report), ())

    def test_repository_archive_v2_has_closed_namespace_and_index_parity(self) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )

        report = archive_validation.validate_repository_archive(ROOT, registry)

        self.assertTrue(report.valid, report.diagnostics)
        self.assertEqual(report.record_count, 93)
        self.assertEqual(report.index_record_count, 93)
        self.assertEqual(
            dict(report.namespace_counts),
            {
                "arwb-base": 31,
                "acer-additive": 12,
                "wdtc-execution": 50,
                "progress-snapshot": 0,
            },
        )

    def test_repository_inventory_separates_exact_archive_migration_controls(
        self,
    ) -> None:
        records, diagnostics = archive_validation._repository_archive_records(  # noqa: SLF001
            ROOT
        )

        self.assertEqual(diagnostics, [])
        self.assertEqual(len(records), 93)
        self.assertNotIn(
            "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md",
            records,
        )
        self.assertNotIn(
            "docs/98.archive/migrations/"
            "mig-0002-sdlc-document-and-governance-consolidation.md",
            records,
        )
        self.assertNotIn(
            "docs/98.archive/migrations/"
            "mig-0003-agent-governance-control-plane-consolidation.md",
            records,
        )

    def test_mig0003_recovery_is_integrated_and_source_pinned(self) -> None:
        migration_path = (
            "docs/98.archive/migrations/"
            "mig-0003-agent-governance-control-plane-consolidation.md"
        )
        migration_bytes = (ROOT / migration_path).read_bytes()

        rows = archive_validation.validate_pinned_migration_recovery(
            ROOT,
            migration_path,
            migration_bytes,
        )

        self.assertEqual(len(rows), 3)
        with self.assertRaisesRegex(
            archive_validation.ArchiveContractError,
            "ARCHIVE-MIGRATION-PROFILE",
        ):
            archive_validation.validate_pinned_migration_recovery(
                ROOT,
                "docs/98.archive/migrations/"
                "mig-0002-sdlc-document-and-governance-consolidation.md",
                (
                    ROOT
                    / "docs/98.archive/migrations/"
                    "mig-0002-sdlc-document-and-governance-consolidation.md"
                ).read_bytes(),
            )

        with tempfile.TemporaryDirectory(prefix="mig0003-recovery-") as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            target = root / migration_path
            target.parent.mkdir(parents=True)
            target.write_bytes(migration_bytes)
            fixture.run("add", "--", migration_path)

            records, diagnostics = archive_validation._repository_archive_records(  # noqa: SLF001
                root
            )

            self.assertEqual(records, {})
            self.assertIn(
                "RECOVERY-OBJECT-NOT-COMMIT",
                self.codes(types.SimpleNamespace(diagnostics=diagnostics)),
            )

    def test_repository_inventory_rejects_unknown_or_drifted_migration_profiles(
        self,
    ) -> None:
        migration_path = (
            "docs/98.archive/migrations/"
            "mig-0002-sdlc-document-and-governance-consolidation.md"
        )
        migration_bytes = (ROOT / migration_path).read_bytes()
        cases = (
            (
                "unknown-control",
                "docs/98.archive/migrations/mig-9999-unreviewed.md",
                migration_bytes,
                "ARCHIVE-MIGRATION-CONTROL",
            ),
            (
                "profile-drift",
                migration_path,
                migration_bytes.replace(
                    b'type: "content/archive-migration"',
                    b'type: "content/archive"',
                    1,
                ),
                "ARCHIVE-MIGRATION-PROFILE",
            ),
        )
        for name, relative, content, expected_code in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="archive-migration-profile-"
            ) as temporary:
                root = Path(temporary)
                target = root / relative
                target.parent.mkdir(parents=True)
                target.write_bytes(content)

                records, diagnostics = (
                    archive_validation._repository_archive_records(root)  # noqa: SLF001
                )

                self.assertEqual(records, {})
                self.assertIn(
                    expected_code,
                    self.codes(types.SimpleNamespace(diagnostics=diagnostics)),
                )

    def test_mig0002_control_pins_full_document_and_resource_envelope(self) -> None:
        migration_path = (
            "docs/98.archive/migrations/"
            "mig-0002-sdlc-document-and-governance-consolidation.md"
        )
        migration_bytes = (ROOT / migration_path).read_bytes()

        rows = archive_validation.parse_pinned_migration_control(
            migration_path, migration_bytes
        )

        self.assertEqual(len(rows), 154)
        self.assertEqual(
            hashlib.sha256(migration_bytes).hexdigest(),
            archive_validation.MIG0002_DOCUMENT_SHA256,
        )
        for name, candidate in (
            ("trailing-prose", migration_bytes + b"\nUnreviewed trailing prose.\n"),
            (
                "oversize",
                migration_bytes
                + b"x"
                * (
                    archive_validation.MIGRATION_DOCUMENT_MAX_BYTES
                    + 1
                    - len(migration_bytes)
                ),
            ),
        ):
            with self.subTest(name=name), self.assertRaises(
                archive_validation.ArchiveContractError
            ):
                archive_validation.parse_pinned_migration_control(
                    migration_path, candidate
                )

    def test_staged_migration_blob_read_is_index_only_and_bounded(self) -> None:
        migration_path = (
            "docs/98.archive/migrations/"
            "mig-0002-sdlc-document-and-governance-consolidation.md"
        )
        valid = (ROOT / migration_path).read_bytes()
        with tempfile.TemporaryDirectory(prefix="mig0002-index-boundary-") as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            target = root / migration_path
            target.parent.mkdir(parents=True)
            staged = valid + b"\ninvalid staged suffix\n"
            target.write_bytes(staged)
            fixture.run("add", "--", migration_path)
            target.write_bytes(valid)

            self.assertEqual(
                archive_validation.read_staged_blob_bounded(
                    root,
                    migration_path,
                    max_bytes=archive_validation.MIGRATION_DOCUMENT_MAX_BYTES,
                ),
                staged,
            )

            target.write_bytes(valid)
            fixture.run("add", "--", migration_path)
            target.write_bytes(staged)
            self.assertEqual(
                archive_validation.read_staged_blob_bounded(
                    root,
                    migration_path,
                    max_bytes=archive_validation.MIGRATION_DOCUMENT_MAX_BYTES,
                ),
                valid,
            )

    def test_current_archive_authority_accepts_declared_migration_profile(
        self,
    ) -> None:
        migration_path = (
            "docs/98.archive/migrations/"
            "mig-0002-sdlc-document-and-governance-consolidation.md"
        )
        report = validate_current_archive_authority(
            (
                CurrentMarkdownDocument(
                    path=migration_path,
                    markdown=(ROOT / migration_path).read_text(encoding="utf-8"),
                    profile="content/archive-migration",
                    status="accepted",
                ),
            ),
            individual_archive_paths=frozenset({self.archive_path}),
        )

        self.assertEqual(self.codes(report), ())

    def test_repository_archive_rejects_open_or_overlapping_namespaces(self) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        open_registry = dict(registry)
        open_registry["archiveNamespaces"] = [
            *registry["archiveNamespaces"],
            {"id": "rogue", "policy": "exact-immutable", "records": []},
        ]
        overlapping = json.loads(json.dumps(registry))
        overlapping["archiveNamespaces"][1]["records"][0] = (
            overlapping["archiveNamespaces"][0]["records"][0]
        )

        open_report = archive_validation.validate_repository_archive(ROOT, open_registry)
        overlap_report = archive_validation.validate_repository_archive(
            ROOT, overlapping
        )

        self.assertIn("ARCHIVE-NAMESPACE-CONTRACT", self.codes(open_report))
        self.assertIn("ARCHIVE-NAMESPACE-OVERLAP", self.codes(overlap_report))

    def test_repository_archive_rejects_index_and_envelope_membership_drift(self) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        missing_member = json.loads(json.dumps(registry))
        missing_member["archiveNamespaces"][2]["records"].pop()

        report = archive_validation.validate_repository_archive(ROOT, missing_member)

        self.assertIn("ARCHIVE-NAMESPACE-PARITY", self.codes(report))

    def test_repository_archive_binds_reviewed_namespace_paths_and_metadata(self) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        substituted = json.loads(json.dumps(registry))
        acer_path = substituted["archiveNamespaces"][1]["records"][0]
        wdtc_path = substituted["archiveNamespaces"][2]["records"][0]
        substituted["archiveNamespaces"][1]["records"][0] = wdtc_path
        substituted["archiveNamespaces"][2]["records"][0] = acer_path

        path_report = archive_validation.validate_repository_archive(ROOT, substituted)

        self.assertIn("ARCHIVE-NAMESPACE-REVIEWED", self.codes(path_report))

        reviewed = archive_validation._reviewed_manifest_records(ROOT)  # noqa: SLF001
        first_path, second_path = tuple(sorted(reviewed))[:2]
        metadata_substitution = dict(reviewed)
        metadata_substitution[first_path] = dataclasses.replace(
            metadata_substitution[first_path],
            source_blob=metadata_substitution[second_path].source_blob,
        )
        with mock.patch.object(
            archive_validation,
            "_reviewed_manifest_records",
            return_value=metadata_substitution,
        ):
            metadata_report = archive_validation.validate_repository_archive(
                ROOT, registry
            )

        self.assertIn("ARCHIVE-NAMESPACE-METADATA", self.codes(metadata_report))

    def test_repository_archive_rejects_noncanonical_replacement_and_per_record_link_swap(
        self,
    ) -> None:
        index_text = (ROOT / "docs/98.archive/README.md").read_text(encoding="utf-8")
        invalid_null = index_text.replace("| `null` |", "| `NULL` |", 1)
        rows, _total, diagnostics = archive_validation._parse_repository_index(  # noqa: SLF001
            invalid_null
        )
        self.assertLess(len(rows), 93)
        self.assertIn(
            "ARCHIVE-INDEX-STRUCTURE",
            self.codes(types.SimpleNamespace(diagnostics=diagnostics)),
        )

        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        parsed_rows, link_total, parse_diagnostics = (
            archive_validation._parse_repository_index(index_text)  # noqa: SLF001
        )
        self.assertEqual(parse_diagnostics, [])
        counts = {path: int(row[-1]) for path, row in parsed_rows.items()}
        positive = next(path for path, count in counts.items() if count > 0)
        other = next(path for path in counts if path != positive)
        counts[positive] -= 1
        counts[other] += 1
        fake_report = archive_validation.ArchiveValidationReport(
            historical_link_count=link_total,
            record_link_counts=tuple(sorted(counts.items())),
        )
        with mock.patch.object(
            archive_validation, "validate_archive_records", return_value=fake_report
        ):
            report = archive_validation.validate_repository_archive(ROOT, registry)

        self.assertIn("ARCHIVE-INDEX-LINKS", self.codes(report))

    def test_repository_archive_git_snapshot_is_bounded_and_under_sixty_seconds(
        self,
    ) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        real_popen = subprocess.Popen
        git_calls = 0

        def bounded_popen(*args, **kwargs):
            nonlocal git_calls
            command = args[0] if args else kwargs.get("args", ())
            if command and command[0] == "git":
                git_calls += 1
                if git_calls > 29:
                    raise AssertionError("repository archive exceeded Git subprocess budget")
            return real_popen(*args, **kwargs)

        started = time.monotonic()
        # Every subprocess.run call creates exactly one Popen. Count that shared
        # process boundary once instead of double-counting run plus its Popen.
        with mock.patch.object(subprocess, "Popen", side_effect=bounded_popen):
            report = archive_validation.validate_repository_archive(ROOT, registry)
        elapsed = time.monotonic() - started

        self.assertTrue(report.valid, report.diagnostics)
        # MIG-0003 adds five bounded calls: repository identity (2), commit
        # types, exact commit:path members, and one three-blob content batch.
        self.assertLessEqual(git_calls, 29)
        self.assertLess(elapsed, 60.0)

    def test_work107_stable_ledger_digest_is_pinned_without_git_reconstruction(
        self,
    ) -> None:
        source = ROOT / archive_validation.WORK107_MIGRATION_PATH
        with tempfile.TemporaryDirectory(prefix="archive-ledger-digest-") as temporary:
            root = Path(temporary)
            target = root / archive_validation.WORK107_MIGRATION_PATH
            target.parent.mkdir(parents=True)
            target.write_bytes(
                source.read_bytes().replace(
                    b"Reviewed stable Stage 98 rehome",
                    b"Unreviewed stable Stage 98 rehome",
                    1,
                )
            )

            with self.assertRaisesRegex(
                RuntimeError,
                r"^WORK-107 stable ledger is unavailable$",
            ):
                archive_validation._work107_stable_rows(root)  # noqa: SLF001

    def test_repository_index_read_is_descriptor_bounded(self) -> None:
        with tempfile.TemporaryDirectory(prefix="archive-index-limit-") as temporary:
            root = Path(temporary)
            index = root / "docs/98.archive/README.md"
            index.parent.mkdir(parents=True)
            index.write_bytes(b"x" * (archive_validation._ARCHIVE_INDEX_LIMIT + 1))  # noqa: SLF001

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                r"^ARCHIVE-INDEX-SIZE:",
            ):
                archive_validation._read_repository_index(root)  # noqa: SLF001

    def test_tree_parser_enforces_output_and_entry_budgets_without_disclosure(
        self,
    ) -> None:
        object_id = "0" * 40
        sentinel = "SECRET-TREE-PATH-SENTINEL"
        record = f"{object_id} blob 7\n".encode("ascii")
        with self.assertRaisesRegex(
            archive_validation.ArchiveContractError,
            r"^RECOVERY-RESOURCE-LIMIT:",
        ) as entries:
            archive_validation._parse_git_path_batch_output(  # noqa: SLF001
                record + record,
                paths=(sentinel, f"{sentinel}-2"),
                object_id_length=40,
                entry_limit=1,
            )
        self.assertNotIn(sentinel, str(entries.exception))

        oversized = io.BytesIO(
            b"x" * (archive_validation._GIT_TREE_OUTPUT_LIMIT + 1)  # noqa: SLF001
        )
        with self.assertRaisesRegex(
            archive_validation.ArchiveContractError,
            r"^RECOVERY-RESOURCE-LIMIT:",
        ):
            archive_validation._read_stream_bounded(  # noqa: SLF001
                oversized,
                archive_validation._GIT_TREE_OUTPUT_LIMIT,  # noqa: SLF001
            )

    def test_exact_membership_does_not_expand_requested_ancestor(self) -> None:
        source = "docs/04.execution/tasks/exact-source.md"
        ancestor = "docs/03.specs/910-exact-membership"
        child = f"{ancestor}/requested.md"
        nested = f"{ancestor}/nested/requested.md"
        files = {
            source: b"# Exact source\n",
            child: b"# Requested child\n",
            nested: b"# Requested nested child\n",
        }
        files.update(
            {
                f"{ancestor}/unrelated-{index:02d}-with-a-long-name.md": b"# Unrelated\n"
                for index in range(12)
            }
        )
        commit, blobs = self.git.commit_many(files)

        with mock.patch.object(archive_validation, "_GIT_TREE_OUTPUT_LIMIT", 512):
            members = archive_validation._commit_tree_members(  # noqa: SLF001
                self.root,
                commit,
                original_paths=(source,),
                historical_paths=(ancestor, child, nested),
                object_id_length=len(commit),
            )

        self.assertEqual(set(members), {source, ancestor, child, nested})
        self.assertEqual(members[source].mode, "100644")
        self.assertEqual(members[source].object_id, blobs[source])
        self.assertEqual(members[ancestor].kind, "tree")
        self.assertEqual(members[child].kind, "blob")
        self.assertEqual(members[nested].kind, "blob")
        self.assertFalse(any("unrelated-" in path for path in members))

    def test_repository_four_spec_overlaps_use_only_exact_batch_evidence(
        self,
    ) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        expected = {
            "docs/03.specs",
            "docs/03.specs/001-wsl-k3d-argocd-platform/spec.md",
            "docs/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md",
            "docs/03.specs/003-platform-expansion/spec.md",
            "docs/03.specs/README.md",
        }
        records, inventory_diagnostics = (
            archive_validation._repository_archive_records(ROOT)  # noqa: SLF001
        )
        self.assertEqual(inventory_diagnostics, [])
        original_paths = {
            str(
                archive_validation.parse_archive_envelope(content).metadata[
                    "original_path"
                ]
            )
            for content in records.values()
        }
        ls_tree_paths: set[str] = set()
        exact_batch_paths: set[str] = set()
        real_git_command = archive_validation._git_command  # noqa: SLF001

        def capture_git_command(root: Path, *args: str, **kwargs):
            if args[:1] == ("ls-tree",) and "--" in args:
                ls_tree_paths.update(args[args.index("--") + 1 :])
            if args[:1] == ("cat-file",) and args[1:2] == (
                "--batch-check=%(objectname) %(objecttype) %(objectsize)",
            ):
                for request in kwargs.get("input_bytes", b"").splitlines():
                    exact_batch_paths.add(
                        request.decode("utf-8", errors="strict").split(":", 1)[1]
                    )
            return real_git_command(root, *args, **kwargs)

        with mock.patch.object(
            archive_validation, "_git_command", side_effect=capture_git_command
        ):
            report = archive_validation.validate_repository_archive(ROOT, registry)

        self.assertTrue(report.valid, report.diagnostics)
        self.assertLessEqual(ls_tree_paths, original_paths)
        self.assertNotIn("docs/03.specs", ls_tree_paths)
        self.assertLessEqual(expected, exact_batch_paths)


class ArchiveTransitionLinkTest(unittest.TestCase):
    """Close the deferred archive-edge handoff after the 82 current moves."""

    moved_source = PurePosixPath(
        "docs/04.execution/tasks/"
        "2026-07-05-workspace-engineering-implementation-audit-pack.md"
    )
    moved_target = PurePosixPath(
        "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks.md"
    )
    archived_source = PurePosixPath(
        "docs/04.execution/plans/"
        "2026-05-24-p3-gitops-secret-runtime-remediation.md"
    )

    @classmethod
    def setUpClass(cls) -> None:
        script_path = ROOT / "scripts" / "validate-links-and-owners.py"
        scripts = str(script_path.parent)
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        spec = importlib.util.spec_from_file_location(
            "archive_transition_link_fixture", script_path
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("link validator is unavailable")
        validator = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = validator
        spec.loader.exec_module(validator)
        cls.validator = validator
        cls.context = validator._build_context(ROOT)

    def test_exact_manifest_edges_route_to_collection_index(self) -> None:
        handoff = self.validator._archive_transition_handoff(self.context)
        actual = tuple(
            (edge.source.as_posix(), edge.target.as_posix())
            for edge in handoff.edges
        )

        self.assertEqual(actual, ())
        self.assertEqual(
            handoff.navigation_boundary,
            "docs/98.archive/README.md#document-index",
        )

    def _mutated_work109_context(self, mutate) -> object:
        path = self.validator.WORK109_MIGRATION_PATH
        text = self.context.texts[path]
        marker = "<!-- archive-migration-ledger:v1 format=json -->\n\n```json\n"
        prefix, payload = text.split(marker, 1)
        raw, suffix = payload.split("\n```", 1)
        rows = json.loads(raw)
        mutate(rows)
        changed = (
            prefix
            + marker
            + json.dumps(rows, indent=2, ensure_ascii=False)
            + "\n```"
            + suffix
        )
        return dataclasses.replace(
            self.context,
            texts={**self.context.texts, path: changed},
        )

    def test_work109_manifest_targets_compose_through_exact_mig0002(self) -> None:
        aliases = self.validator._work109_four_digit_aliases(self.context)

        self.assertEqual(len(aliases), 141)
        self.assertEqual(
            aliases[
                PurePosixPath(
                    "docs/03.specs/018-workspace-engineering-implementation-audit-pack/tasks.md"
                )
            ],
            self.moved_target,
        )

    def test_declared_spec_index_accepts_only_four_digit_work_units(self) -> None:
        pattern = self.validator.DECLARED_INDEXES[0].target_pattern

        self.assertIsNotNone(
            pattern.fullmatch(
                "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md"
            )
        )
        self.assertIsNone(
            pattern.fullmatch(
                "docs/03.specs/054-sdlc-document-and-agent-governance-consolidation/spec.md"
            )
        )

    def test_stage90_ledger_projects_only_source_pinned_work109_paths(
        self,
    ) -> None:
        diagnostics = self.validator._ledger_diagnostics(self.context)

        self.assertNotIn(
            "LEDGER-UNKNOWN-PATH",
            {item.rule_id for item in diagnostics},
        )

    def test_work054_mig0003_historical_projection_is_byte_exact(self) -> None:
        projection = self.validator._work054_wp003_owner_merges(self.context)
        self.assertEqual(len(projection), 3)

        path = self.validator.WORK054_MIGRATION_PATH
        original = self.context.texts[path]
        for name, changed in (
            ("document-sha", original + "\n"),
            (
                "replacement",
                original.replace(
                    '"replacement": "docs/00.agent-governance/providers/codex.md"',
                    '"replacement": "docs/00.agent-governance/harness-catalog.md"',
                    1,
                ),
            ),
        ):
            with self.subTest(name=name):
                context = dataclasses.replace(
                    self.context,
                    texts={**self.context.texts, path: changed},
                )
                with self.assertRaises(self.validator.ConfigurationError):
                    self.validator._work054_wp003_owner_merges(context)

    def test_work054_historical_edges_are_limited_to_mig0003_merges(self) -> None:
        _aliases, move_targets, _replacements = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        edges = self.validator._reviewed_work054_historical_owner_edges(
            self.context,
            move_targets,
        )

        self.assertEqual(self.validator.WORK054_HISTORICAL_OCCURRENCE_COUNT, 41)
        self.assertEqual(len(edges), 15)
        self.assertEqual(len({edge.source for edge in edges}), 10)
        self.assertEqual(
            {edge.target for edge in edges},
            set(self.validator._work054_wp003_owner_merges(self.context)),
        )
        self.assertNotIn(
            self.validator.ArchiveTransitionEdge(
                PurePosixPath(
                    "docs/03.specs/0015-agent-governance-contract-normalization/spec.md"
                ),
                PurePosixPath("docs/99.templates/support/template-routing.md"),
            ),
            edges,
        )

    def test_standalone_approval_statements_are_relation_specific(self) -> None:
        statements = self.validator.STANDALONE_APPROVAL_STATEMENTS

        self.assertEqual(
            set(statements),
            # 0055-0061 are the renumbered successors the consolidation
            # merge introduced alongside the original three.
            {
                "0043",
                "0053",
                "0054",
                "0055",
                "0056",
                "0057",
                "0058",
                "0059",
                "0060",
                "0061",
            },
        )
        self.assertIn("2026-08-08", statements["0053"][0])
        self.assertIn("2026-08-13", statements["0054"][0])
        self.assertNotEqual(statements["0053"], statements["0054"])

    def test_work109_mig0002_source_commit_blob_and_target_drift_fail_closed(
        self,
    ) -> None:
        mutations = {
            "source-commit": lambda rows: rows[0].__setitem__(
                "source_commit", "0" * 40
            ),
            "source-blob": lambda rows: rows[0].__setitem__(
                "source_blob", "0" * 40
            ),
            "stable-target": lambda rows: rows[0].__setitem__(
                "stable_path", "docs/01.requirements/9999-unreviewed.md"
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                context = self._mutated_work109_context(mutate)
                with self.assertRaises(self.validator.ConfigurationError):
                    self.validator._work109_four_digit_aliases(context)

    def test_immutable_history_aliases_are_exact_source_and_edge_sets(self) -> None:
        _, move_targets, _ = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        edges = self.validator._reviewed_immutable_historical_alias_edges(
            self.context,
            move_targets,
        )

        self.assertEqual(len({edge.source for edge in edges}), 27)
        self.assertEqual(len(edges), 93)
        self.assertTrue(
            all(
                replacement in self.context.tracked_regular_paths
                for replacement in edges.values()
            )
        )

    def test_immutable_history_source_blob_and_target_drift_fail_closed(
        self,
    ) -> None:
        _, move_targets, _ = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        source = next(
            iter(
                sorted(
                    self.validator.IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS
                )
            )
        )
        drifted_context = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: self.context.texts[source] + "\n",
            },
        )
        with self.assertRaises(self.validator.ConfigurationError):
            self.validator._reviewed_immutable_historical_alias_edges(
                drifted_context,
                move_targets,
            )

        redirects = self.validator._immutable_historical_redirects(
            self.context,
            move_targets,
        )
        edges = self.validator._reviewed_immutable_historical_alias_edges(
            self.context,
            move_targets,
        )
        target = next(iter(sorted(edges))).target
        drifted_redirects = {
            **redirects,
            target: PurePosixPath("docs/99.templates/unreviewed-target.md"),
        }
        with (
            mock.patch.object(
                self.validator,
                "_immutable_historical_redirects",
                return_value=drifted_redirects,
            ),
            self.assertRaises(self.validator.ConfigurationError),
        ):
            self.validator._reviewed_immutable_historical_alias_edges(
                self.context,
                move_targets,
            )

    def test_immutable_history_research_accepts_only_exact_insertion_slices(
        self,
    ) -> None:
        _, move_targets, _ = self.validator._document_taxonomy_transition_manifest(
            self.context
        )
        insertion_marker = b"\n### 2026-08-20 full-corpus reverification\n"
        insertion_slices = {
            PurePosixPath(
                "docs/90.references/research/2026-08-08-wer/"
                "documentation-architecture-and-diataxis.md"
            ): (27_688, 358, insertion_marker),
            PurePosixPath(
                "docs/90.references/research/2026-08-08-wer/"
                "spec-driven-sdlc-and-document-contracts.md"
            ): (48_521, 415, insertion_marker),
        }

        self.assertEqual(
            self.validator.IMMUTABLE_HISTORICAL_INSERTION_SLICES,
            insertion_slices,
        )
        self.assertEqual(
            self.validator.IMMUTABLE_HISTORICAL_ALIAS_OCCURRENCE_COUNT,
            169,
        )
        for source, (
            frozen_prefix_size,
            frozen_suffix_size,
            expected_marker,
        ) in insertion_slices.items():
            with self.subTest(source=source):
                content = self.context.texts[source].encode("utf-8")
                gap_end = len(content) - frozen_suffix_size
                gap = content[frozen_prefix_size:gap_end]
                self.assertTrue(gap.startswith(expected_marker))
                self.assertEqual(
                    self.validator._git_sha1_blob_bytes(
                        content[:frozen_prefix_size] + content[gap_end:]
                    ),
                    self.validator.IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS[source],
                )

        edges = self.validator._reviewed_immutable_historical_alias_edges(
            self.context,
            move_targets,
        )
        self.assertEqual(len({edge.source for edge in edges}), 27)
        self.assertEqual(len(edges), 93)

        source = next(iter(insertion_slices))
        _prefix_size, suffix_size, _marker = insertion_slices[source]
        insertion_point = len(self.context.texts[source].encode("utf-8")) - suffix_size
        current = self.context.texts[source].encode("utf-8")
        appended_context = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: (
                    current[:insertion_point]
                    + b"\n<!-- approved gap fixture -->\n"
                    + current[insertion_point:]
                ).decode("utf-8"),
            },
        )
        self.assertEqual(
            self.validator._reviewed_immutable_historical_alias_edges(
                appended_context,
                move_targets,
            ),
            edges,
        )

    def test_immutable_history_research_slice_and_other_sources_fail_closed(
        self,
    ) -> None:
        _, move_targets, _ = self.validator._document_taxonomy_transition_manifest(
            self.context
        )
        insertion_marker = b"\n### 2026-08-20 full-corpus reverification\n"
        insertion_slices = {
            PurePosixPath(
                "docs/90.references/research/2026-08-08-wer/"
                "documentation-architecture-and-diataxis.md"
            ): (27_688, 358, insertion_marker),
            PurePosixPath(
                "docs/90.references/research/2026-08-08-wer/"
                "spec-driven-sdlc-and-document-contracts.md"
            ): (48_521, 415, insertion_marker),
        }
        for source, (prefix_size, suffix_size, _marker) in insertion_slices.items():
            content = self.context.texts[source].encode("utf-8")
            gap_end = len(content) - suffix_size
            mutated_prefix = bytearray(content)
            mutated_prefix[0] = ord("!")
            mutated_suffix = bytearray(content)
            mutated_suffix[-1] = ord("!")
            mutated_marker = (
                content[:prefix_size]
                + content[prefix_size:gap_end].replace(
                    insertion_marker,
                    b"\n### unreviewed increment\n",
                    1,
                )
                + content[gap_end:]
            )
            suffix_state_mask = (
                content[:gap_end]
                + b"\n[fixture](../../../99.templates/support/template-routing.md)\n"
                + b"\n```\n"
                + content[gap_end:]
            )

            for name, changed_text in (
                ("frozen-prefix-mutation", mutated_prefix.decode("utf-8")),
                ("frozen-suffix-mutation", mutated_suffix.decode("utf-8")),
                ("gap-marker-mutation", mutated_marker.decode("utf-8")),
                ("suffix-state-mask", suffix_state_mask.decode("utf-8")),
                ("truncation", content[: prefix_size - 1].decode("utf-8")),
                (
                    "insertion-outside-boundary",
                    (content + b"\n<!-- outside boundary -->\n").decode("utf-8"),
                ),
            ):
                with self.subTest(source=source, name=name):
                    drifted_context = dataclasses.replace(
                        self.context,
                        texts={
                            **self.context.texts,
                            source: changed_text,
                        },
                    )
                    with self.assertRaises(self.validator.ConfigurationError):
                        self.validator._reviewed_immutable_historical_alias_edges(
                            drifted_context,
                            move_targets,
                        )

        other_source = next(
            iter(
                sorted(
                    set(self.validator.IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS)
                    - set(insertion_slices)
                )
            )
        )
        with self.subTest(source=other_source, name="other-source-append"):
            drifted_context = dataclasses.replace(
                self.context,
                texts={
                    **self.context.texts,
                    other_source: self.context.texts[other_source] + "\n",
                },
            )
            with self.assertRaises(self.validator.ConfigurationError):
                self.validator._reviewed_immutable_historical_alias_edges(
                    drifted_context,
                    move_targets,
                )

    def test_completed_history_aliases_are_exact_source_and_edge_sets(
        self,
    ) -> None:
        _, move_targets, _ = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        edges = self.validator._reviewed_completed_history_alias_edges(
            self.context,
            move_targets,
        )

        self.assertEqual(len({edge.source for edge in edges}), 46)
        self.assertEqual(len(edges), 186)
        self.assertTrue(
            all(
                replacement in self.context.tracked_regular_paths
                for replacement in edges.values()
            )
        )
        self.assertTrue(
            {
                PurePosixPath("docs/00.agent-governance/scopes/product.md"),
                PurePosixPath("docs/01.requirements/README.md"),
                PurePosixPath("docs/03.specs/README.md"),
            }.isdisjoint(
                self.validator.COMPLETED_HISTORY_ALIAS_SOURCE_BLOBS
            )
        )

    def test_completed_history_progress_accepts_only_exact_frozen_prefix(
        self,
    ) -> None:
        _, move_targets, _ = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        source = PurePosixPath(
            "docs/00.agent-governance/memory/progress.md"
        )
        expected_blob = self.validator.COMPLETED_HISTORY_ALIAS_SOURCE_BLOBS[
            source
        ]
        prefix_size = (
            self.validator.COMPLETED_HISTORY_APPEND_ONLY_PREFIX_BYTES[source]
        )
        current = self.context.texts[source]
        current_bytes = current.encode("utf-8")

        # The ledger is append-only, so it may be longer than the frozen
        # prefix. Only the prefix itself is pinned, which the next assertion
        # checks byte for byte.
        self.assertGreaterEqual(len(current_bytes), prefix_size)
        self.assertEqual(
            self.validator._git_sha1_blob_bytes(current_bytes[:prefix_size]),
            expected_blob,
        )

        appended_context = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: current + "\n<!-- append-only fixture -->\n",
            },
        )
        edges = self.validator._reviewed_completed_history_alias_edges(
            appended_context,
            move_targets,
        )
        self.assertEqual(len(edges), 186)

        mutated_prefix = bytearray(current_bytes)
        mutated_prefix[0] = ord("!")
        drifted_context = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: mutated_prefix.decode("utf-8"),
            },
        )
        with self.assertRaises(self.validator.ConfigurationError):
            self.validator._reviewed_completed_history_alias_edges(
                drifted_context,
                move_targets,
            )

    def test_completed_history_source_blob_and_target_drift_fail_closed(
        self,
    ) -> None:
        _, move_targets, _ = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        source = next(
            iter(
                sorted(
                    set(
                        self.validator.COMPLETED_HISTORY_ALIAS_SOURCE_BLOBS
                    )
                    - set(
                        self.validator.COMPLETED_HISTORY_APPEND_ONLY_PREFIX_BYTES
                    )
                )
            )
        )
        drifted_context = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: self.context.texts[source] + "\n",
            },
        )
        with self.assertRaises(self.validator.ConfigurationError):
            self.validator._reviewed_completed_history_alias_edges(
                drifted_context,
                move_targets,
            )

        redirects = self.validator._immutable_historical_redirects(
            self.context,
            move_targets,
        )
        edges = self.validator._reviewed_completed_history_alias_edges(
            self.context,
            move_targets,
        )
        target = next(iter(sorted(edges))).target
        drifted_redirects = {
            **redirects,
            target: PurePosixPath("docs/99.templates/unreviewed-target.md"),
        }
        with (
            mock.patch.object(
                self.validator,
                "_immutable_historical_redirects",
                return_value=drifted_redirects,
            ),
            self.assertRaises(self.validator.ConfigurationError),
        ):
            self.validator._reviewed_completed_history_alias_edges(
                self.context,
                move_targets,
            )

    def test_work107_stable_archive_aliases_are_exact_and_tracked(self) -> None:
        aliases = self.validator._work107_stable_archive_aliases(self.context)

        self.assertEqual(len(aliases), 93)
        self.assertEqual(len(set(aliases.values())), 93)
        self.assertTrue(
            all(target in self.context.tracked_regular_paths for target in aliases.values())
        )

    def test_work107_archive_index_is_only_the_reviewed_stable_projection(self) -> None:
        self.assertTrue(
            self.validator._work107_stable_archive_index_source(
                self.context,
                PurePosixPath("docs/98.archive/README.md"),
            )
        )

    def test_non_manifest_current_source_is_not_deferred(self) -> None:
        source = PurePosixPath(
            "docs/01.requirements/0004-current-local-gitops-platform.md"
        )
        target = self.archived_source

        self.assertIsNone(
            self.validator._archive_transition_target(self.context, source, target)
        )

    def test_moved_manifest_source_is_absent_and_target_is_current(self) -> None:
        self.assertNotIn(self.moved_source, self.context.texts)
        self.assertIn(self.moved_target, self.context.texts)

    def test_unknown_archived_target_is_not_deferred(self) -> None:
        source = self.moved_target
        target = PurePosixPath(
            "docs/04.execution/tasks/2099-01-01-unknown-archive-source.md"
        )

        self.assertIsNone(
            self.validator._archive_transition_target(self.context, source, target)
        )

    def test_terminal_route_rejects_transition_residue(self) -> None:
        terminal = dataclasses.replace(self.context, route_state="terminal")

        handoff = self.validator._archive_transition_handoff(terminal)
        self.assertEqual(handoff.edges, ())

    def test_source_commit_drift_and_manifest_index_drift_fail_closed(self) -> None:
        snapshot = self.validator._reviewed_taxonomy_manifest(self.context.root)
        drifted = dataclasses.replace(snapshot, source_commit="0" * 40)
        with mock.patch.object(
            self.validator, "_reviewed_taxonomy_manifest", return_value=drifted
        ), self.assertRaises(self.validator.ConfigurationError):
            self.validator._archive_transition_handoff(self.context)

        with mock.patch.object(
            self.validator,
            "_reviewed_taxonomy_manifest",
            side_effect=self.validator.ConfigurationError(
                "archive transition manifest worktree/index differs"
            ),
        ), self.assertRaises(self.validator.ConfigurationError):
            self.validator._archive_transition_handoff(self.context)

    def test_added_post_move_deferred_edge_is_rejected(self) -> None:
        source = self.moved_target
        original_text = self.context.texts[source]
        _move_blobs, move_targets, archive_sources = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        extra_target = next(target for target in sorted(archive_sources))

        added_text = original_text + f"\n[unexpected]({self.validator.posixpath.relpath(extra_target.as_posix(), source.parent.as_posix())})\n"
        added_context = dataclasses.replace(
            self.context, texts={**self.context.texts, source: added_text}
        )
        with mock.patch.object(
            self.validator,
            "_document_taxonomy_transition_manifest",
            return_value=(
                {source: self.validator._git_sha1_blob(added_text)},
                move_targets,
                archive_sources,
            ),
        ), self.assertRaises(self.validator.ConfigurationError):
            self.validator._archive_transition_handoff(added_context)

    def _assert_added_legacy_move_edge_is_rejected(
        self, source: PurePosixPath
    ) -> None:
        _move_blobs, move_targets, _archive_sources = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )
        legacy_target = next(iter(sorted(move_targets)))
        raw_target = self.validator.posixpath.relpath(
            legacy_target.as_posix(), source.parent.as_posix()
        )
        added_text = self.context.texts[source] + f"\n[unexpected legacy]({raw_target})\n"
        added_context = dataclasses.replace(
            self.context, texts={**self.context.texts, source: added_text}
        )

        try:
            diagnostics = self.validator._link_diagnostics(added_context)
        except self.validator.ConfigurationError:
            return
        self.assertTrue(
            any(
                item.rule_id == "LINK-BROKEN" and item.path == source
                for item in diagnostics
            )
        )

    def test_stage05_does_not_waive_injected_legacy_move_edge(self) -> None:
        self._assert_added_legacy_move_edge_is_rejected(
            PurePosixPath(
                "docs/05.operations/policies/"
                "0004-rollouts-notifications-headlamp-policy.md"
            )
        )

    def test_stage90_does_not_waive_injected_legacy_move_edge(self) -> None:
        self._assert_added_legacy_move_edge_is_rejected(
            PurePosixPath("docs/90.references/README.md")
        )


if __name__ == "__main__":
    unittest.main()
