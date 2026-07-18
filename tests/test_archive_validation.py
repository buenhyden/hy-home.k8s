#!/usr/bin/env python3
"""Focused RED/GREEN fixtures for ARWB-002 archive validation interfaces."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
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
            "replacement": "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",
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
        current_path = "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md"
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
            path="docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",
            markdown=(
                "# Current\n\n[record](../../98.archive/03.specs/900-fixture/spec.md)\n"
            ),
            profile="sdlc/spec",
            status="active",
        )
        via_index = CurrentMarkdownDocument(
            path="docs/03.specs/037-active-corpus-and-execution-retention/spec.md",
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


if __name__ == "__main__":
    unittest.main()
