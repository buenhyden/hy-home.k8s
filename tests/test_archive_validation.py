#!/usr/bin/env python3
"""Focused RED/GREEN fixtures for ARWB-002 archive validation interfaces."""

from __future__ import annotations

import dataclasses
import hashlib
import io
import importlib.util
import json
import re
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
    require_commits_reachable_from_durable_refs,
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


def _migration_declared_paths(root: Path) -> set[str]:
    """Return every path the archive migration ledgers declare as evidence.

    Recovering a declared row is bounded evidence, so those reads belong beside
    the archived originals rather than counting as an unbounded tree walk. Each
    ledger carries several JSON blocks - rows, partial-content dispositions, and
    historical reference evidence - and every one of them names sources.
    """

    paths: set[str] = set()
    directory = root / "docs/98.archive/migrations"
    for candidate in sorted(directory.glob("*.md")):
        for block in re.findall(
            r"```json\n(.*?)\n```", candidate.read_text(encoding="utf-8"), re.S
        ):
            try:
                records = json.loads(block)
            except json.JSONDecodeError:
                continue
            for record in records if isinstance(records, list) else [records]:
                if not isinstance(record, dict):
                    continue
                for key, value in record.items():
                    if key == "paths" and isinstance(value, list):
                        paths.update(item for item in value if isinstance(item, str))
                    elif key.endswith(("_path", "_paths")) or key == "replacement":
                        if isinstance(value, str):
                            paths.add(value)
    return paths


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

    def test_requirement_package_is_a_current_markdown_profile(self) -> None:
        document = CurrentMarkdownDocument(
            path="docs/01.requirements/0001-fixture.md",
            markdown="# Requirement package\n",
            profile="sdlc/requirement-package",
            status="active",
        )

        report = validate_current_archive_authority(
            (document,), individual_archive_paths=frozenset({self.archive_path})
        )

        self.assertEqual(self.codes(report), ())

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
        current_path = (
            "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md"
        )
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

    def test_mig0004_is_the_only_direct_current_migration_control(self) -> None:
        current = CurrentMarkdownDocument(
            path="docs/03.specs/0054-document-authority-convergence/README.md",
            markdown=(
                "[recovery](../../98.archive/migrations/"
                "0004-document-authority-convergence.md)\n"
            ),
            profile="readme/collection-index",
            status="active",
        )
        wrong_control = dataclasses.replace(
            current,
            markdown=(
                "[wrong](../../98.archive/migrations/"
                "mig-0003-agent-governance-control-plane-consolidation.md)\n"
            ),
        )

        self.assertEqual(
            self.codes(
                validate_current_archive_authority(
                    (current,),
                    individual_archive_paths=frozenset({self.archive_path}),
                )
            ),
            (),
        )
        self.assertEqual(
            self.codes(
                validate_current_archive_authority(
                    (wrong_control,),
                    individual_archive_paths=frozenset({self.archive_path}),
                )
            ),
            ("ARCHIVE-DIRECT-CURRENT-LINK",),
        )

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
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )

        report = archive_validation.validate_repository_archive(ROOT, registry)

        self.assertTrue(report.valid, report.diagnostics)
        self.assertEqual(report.record_count, report.index_record_count)
        self.assertEqual(
            sum(count for _namespace, count in report.namespace_counts),
            report.record_count,
        )
        self.assertEqual(
            {namespace for namespace, _count in report.namespace_counts},
            set(archive_validation._NAMESPACE_IDS),  # noqa: SLF001
        )

    def test_repository_inventory_separates_exact_archive_migration_controls(
        self,
    ) -> None:
        records, diagnostics = archive_validation._repository_archive_records(  # noqa: SLF001
            ROOT
        )

        self.assertEqual(diagnostics, [])
        self.assertTrue(records)
        self.assertTrue(
            all(
                path.startswith(
                    ("docs/98.archive/changes/", "docs/98.archive/tombstones/")
                )
                for path in records
            )
        )
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
                    ROOT / "docs/98.archive/migrations/"
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

    def test_mig0004_recovery_is_integrated_sealed_and_semantic(self) -> None:
        migration_path = (
            "docs/98.archive/migrations/0004-document-authority-convergence.md"
        )
        migration_bytes = (ROOT / migration_path).read_bytes()

        rows = archive_validation.validate_pinned_migration_recovery(
            ROOT,
            migration_path,
            migration_bytes,
        )

        self.assertEqual(
            {
                str(row["legacy_path"])
                for row in rows
                if str(row["legacy_path"]).startswith("docs/99.templates/")
            },
            set(archive_validation.MIG0004_STAGE99_ACTION_TARGETS),
        )
        self.assertEqual(
            [
                row
                for row in rows
                if row["legacy_path"] == archive_validation.MIG0004_SPEC0054_LEDGER
            ],
            [
                next(
                    row
                    for row in rows
                    if row["legacy_path"] == archive_validation.MIG0004_SPEC0054_LEDGER
                )
            ],
        )
        for changed in (
            migration_bytes + b"\nAdditional recovery guidance.\n",
            migration_bytes.replace(
                b"This atomic ledger seals", b"This altered ledger seals", 1
            ),
        ):
            with (
                self.subTest(changed=changed[-32:]),
                self.assertRaisesRegex(
                    archive_validation.ArchiveContractError,
                    "ARCHIVE-MIGRATION-PROFILE",
                ),
            ):
                archive_validation.parse_pinned_migration_control(
                    migration_path, changed
                )
        invalid_status = migration_bytes.replace(
            b'status: "sealed"', b'status: "accepted"', 1
        )
        with self.assertRaisesRegex(
            archive_validation.ArchiveContractError,
            "ARCHIVE-MIGRATION-PROFILE",
        ):
            archive_validation.parse_pinned_migration_control(
                migration_path,
                invalid_status,
            )

    def test_recovery_rejects_a_full_but_unreachable_commit(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="unreachable-migration-commit-"
        ) as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            reachable, _blobs = fixture.commit_many({"reachable.md": b"reachable\n"})
            durable_branch = (
                fixture.run("symbolic-ref", "--short", "HEAD").decode("ascii").strip()
            )
            fixture.run("checkout", "--quiet", "--orphan", "detached-source")
            unreachable, _blobs = fixture.commit_many(
                {"reachable.md": b"reachable\n", "legacy.md": b"legacy\n"}
            )
            fixture.run("checkout", "--quiet", durable_branch)

            archive_validation._require_commits_reachable(  # noqa: SLF001
                root.resolve(),
                (reachable,),
            )
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-OBJECT-UNREACHABLE",
            ):
                archive_validation._require_commits_reachable(  # noqa: SLF001
                    root.resolve(),
                    (unreachable,),
                )

    def test_recovery_requires_an_allowed_named_durable_ref(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-ref-recovery-") as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            source, _blobs = fixture.commit_many({"legacy.md": b"legacy\n"})
            short_branch = (
                fixture.run("symbolic-ref", "--short", "HEAD").decode("ascii").strip()
            )
            durable_ref = f"refs/heads/{short_branch}"

            require_commits_reachable_from_durable_refs(
                root.resolve(),
                (source,),
                (durable_ref,),
            )
            fixture.run("checkout", "--quiet", "--detach", source)

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-DURABLE-REF",
            ):
                archive_validation._require_commits_reachable(  # noqa: SLF001
                    root.resolve(),
                    (source,),
                )

            fixture.run("branch", "-D", short_branch)
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-DURABLE-REF",
            ):
                require_commits_reachable_from_durable_refs(
                    root.resolve(),
                    (source,),
                    (durable_ref,),
                )

    def test_recovery_rejects_wrong_or_untrusted_ref_namespaces(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wrong-durable-ref-") as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            source, _blobs = fixture.commit_many({"legacy.md": b"legacy\n"})
            source_branch = (
                fixture.run("symbolic-ref", "--short", "HEAD").decode("ascii").strip()
            )
            fixture.run("checkout", "--quiet", "--orphan", "unrelated")
            fixture.commit_many({"unrelated.md": b"unrelated\n"})

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-OBJECT-UNREACHABLE",
            ):
                require_commits_reachable_from_durable_refs(
                    root.resolve(),
                    (source,),
                    ("refs/heads/unrelated",),
                )
            for candidate in ("HEAD", f"refs/tags/{source_branch}"):
                with (
                    self.subTest(candidate=candidate),
                    self.assertRaisesRegex(
                        archive_validation.ArchiveContractError,
                        "RECOVERY-DURABLE-REF",
                    ),
                ):
                    require_commits_reachable_from_durable_refs(
                        root.resolve(),
                        (source,),
                        (candidate,),
                    )

    @staticmethod
    def _mig0004_current_fixture(
        root: Path,
    ) -> tuple[GitFixture, tuple[dict[str, object], ...]]:
        migration_path = (
            "docs/98.archive/migrations/0004-document-authority-convergence.md"
        )
        rows = archive_validation.parse_pinned_migration_control(
            migration_path,
            (ROOT / migration_path).read_bytes(),
        )
        files: dict[str, bytes] = {}
        for row in rows:
            target = (
                row["stable_path"] if row["action"] == "moved" else row["replacement"]
            )
            assert isinstance(target, str)
            files[target] = (ROOT / target).read_bytes()
        for task in ROOT.glob("docs/03.specs/*/tasks/tsk-*.md"):
            files[task.relative_to(ROOT).as_posix()] = task.read_bytes()
        fixture = GitFixture(root)
        for relative, payload in files.items():
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
        fixture.run("--literal-pathspecs", "add", "--", *files)
        return fixture, rows

    def test_mig0004_targets_and_tasks_are_bound_to_stage_zero(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mig0004-stage-zero-") as temporary:
            root = Path(temporary)
            fixture, rows = self._mig0004_current_fixture(root)
            archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                root.resolve(), rows
            )

            target = str(rows[0]["replacement"])
            fixture.run("rm", "--cached", "--quiet", "--", target)
            self.assertTrue((root / target).is_file())
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-TARGET",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), rows
                )

    def test_mig0004_stage99_targets_are_index_bound_and_worktree_identical(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="mig0004-stage99-index-") as temporary:
            root = Path(temporary)
            fixture, rows = self._mig0004_current_fixture(root)
            moved = next(
                row
                for row in rows
                if row["legacy_path"]
                in archive_validation.MIG0004_STAGE99_ACTION_TARGETS
                and row["action"] == "moved"
            )
            replaced = next(
                row
                for row in rows
                if row["legacy_path"]
                in archive_validation.MIG0004_STAGE99_ACTION_TARGETS
                and row["action"] == "replaced"
                and row["replacement"] == "docs/99.templates/registry.json"
            )

            moved_target = str(moved["stable_path"])
            fixture.run("rm", "--cached", "--quiet", "--", moved_target)
            self.assertTrue((root / moved_target).is_file())
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-TARGET",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), rows
                )

            fixture.run("add", "--", moved_target)
            replaced_target = root / str(replaced["replacement"])
            replaced_target.write_bytes(
                replaced_target.read_bytes() + b"\nworktree drift\n"
            )
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-TARGET",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), rows
                )

    def test_mig0004_stage99_target_rejects_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="mig0004-stage99-symlink-"
        ) as temporary:
            root = Path(temporary)
            _fixture, rows = self._mig0004_current_fixture(root)
            row = next(
                item
                for item in rows
                if item["legacy_path"]
                in archive_validation.MIG0004_STAGE99_ACTION_TARGETS
                and item["action"] == "replaced"
                and item["replacement"] == "docs/99.templates/registry.json"
            )
            target = root / str(row["replacement"])
            outside = root / "outside.json"
            outside.write_bytes(target.read_bytes())
            target.unlink()
            target.symlink_to(outside)

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-TARGET",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), rows
                )

    def test_mig0004_rejects_non_terminal_row_growth(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mig0004-growth-") as temporary:
            root = Path(temporary)
            fixture, rows = self._mig0004_current_fixture(root)
            target = "docs/03.specs/9999-semantic-growth/README.md"
            destination = root / target
            destination.parent.mkdir(parents=True)
            destination.write_text("# Semantic growth\n", encoding="utf-8")
            fixture.run("add", "--", target)
            added = {
                "legacy_path": "docs/03.specs/9999-semantic-growth/tasks.md",
                "stable_path": None,
                "artifact_id": None,
                "action": "replaced",
                "replacement": target,
                "source_commit": "a" * 40,
                "source_blob": "b" * 40,
                "content_sha256": "c" * 64,
                "reason": "Canonical future task-ledger convergence.",
            }
            grown = tuple(
                sorted((*rows, added), key=lambda row: str(row["legacy_path"]))
            )

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-ROW",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), grown
                )

    def test_mig0004_requires_exact_stage99_and_sole_spec0054_rows(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mig0004-required-") as temporary:
            root = Path(temporary)
            _fixture, rows = self._mig0004_current_fixture(root)
            missing_stage99 = tuple(
                row
                for row in rows
                if row["legacy_path"]
                != next(iter(archive_validation.MIG0004_STAGE99_ACTION_TARGETS))
            )
            missing_spec0054 = tuple(
                row
                for row in rows
                if row["legacy_path"] != archive_validation.MIG0004_SPEC0054_LEDGER
            )
            for candidate in (missing_stage99, missing_spec0054):
                with self.subTest(rows=len(candidate)):
                    with self.assertRaisesRegex(
                        archive_validation.ArchiveContractError,
                        "RECOVERY-MIGRATION-ROW",
                    ):
                        archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                            root.resolve(), candidate
                        )

    def test_mig0004_required_cutover_rows_reject_a_reachable_wrong_commit(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="mig0004-wrong-boundary-") as temporary:
            root = Path(temporary)
            fixture, rows = self._mig0004_current_fixture(root)
            fixture.run("commit", "--quiet", "-m", "reachable wrong boundary")
            reachable = fixture.run("rev-parse", "HEAD").decode("ascii").strip()
            self.assertNotEqual(
                reachable,
                archive_validation.MIG0004_TERMINAL_SOURCE_COMMIT,
            )
            changed = [dict(row) for row in rows]
            index = next(
                offset
                for offset, row in enumerate(changed)
                if row["legacy_path"]
                in archive_validation.MIG0004_STAGE99_ACTION_TARGETS
            )
            changed[index]["source_commit"] = reachable

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-ROW",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), tuple(changed)
                )

    def test_mig0004_rejects_tampered_stage99_digest_and_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mig0004-tamper-") as temporary:
            root = Path(temporary)
            _fixture, rows = self._mig0004_current_fixture(root)
            moved_index = next(
                index
                for index, row in enumerate(rows)
                if row["legacy_path"]
                in archive_validation.MIG0004_STAGE99_ACTION_TARGETS
                and row["action"] == "moved"
            )
            replaced_index = next(
                index
                for index, row in enumerate(rows)
                if row["legacy_path"]
                in archive_validation.MIG0004_STAGE99_ACTION_TARGETS
                and row["action"] == "replaced"
            )
            digest_rows = [dict(row) for row in rows]
            digest_rows[moved_index]["content_sha256"] = "0" * 64
            target_rows = [dict(row) for row in rows]
            target_rows[replaced_index]["replacement"] = (
                "docs/99.templates/registry.json"
            )
            for candidate, rule_id in (
                (tuple(digest_rows), "RECOVERY-MIGRATION-TARGET"),
                (tuple(target_rows), "RECOVERY-MIGRATION-ROW"),
            ):
                with self.subTest(rule_id=rule_id):
                    with self.assertRaisesRegex(
                        archive_validation.ArchiveContractError,
                        rule_id,
                    ):
                        archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                            root.resolve(), candidate
                        )
                        archive_validation.validate_mig0004_historical_targets(
                            ROOT, candidate
                        )

    def test_mig0004_rejects_an_index_deleted_untracked_task(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mig0004-untracked-task-") as temporary:
            root = Path(temporary)
            fixture, rows = self._mig0004_current_fixture(root)
            task = sorted(root.glob("docs/03.specs/*/tasks/tsk-*.md"))[0]
            relative = task.relative_to(root).as_posix()
            fixture.run("rm", "--cached", "--quiet", "--", relative)
            self.assertTrue(task.is_file())

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-TASK",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), rows
                )

    def test_mig0004_rejects_oversized_current_consumers_before_reading(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="mig0004-oversize-consumer-"
        ) as temporary:
            root = Path(temporary)
            fixture, rows = self._mig0004_current_fixture(root)
            consumer = root / "docs/03.specs/9999-oversized.md"
            consumer.write_bytes(
                b"x" * (archive_validation.CURRENT_MARKDOWN_MAX_BYTES + 1)
            )
            fixture.run("add", "--", consumer.relative_to(root).as_posix())

            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-RESOURCE-LIMIT",
            ):
                archive_validation._validate_mig0004_rows_and_targets(  # noqa: SLF001
                    root.resolve(), rows
                )

    def test_bounded_current_reader_rejects_symlinks_and_replacement_race(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bounded-current-reader-") as temporary:
            root = Path(temporary).resolve()
            parent = root / "docs" / "pkg"
            parent.mkdir(parents=True)
            target = parent / "record.md"
            target.write_bytes(b"stable\n")

            self.assertEqual(
                archive_validation.read_worktree_regular_bounded(
                    root, "docs/pkg/record.md", max_bytes=32
                ),
                b"stable\n",
            )
            target.unlink()
            target.symlink_to(root / "outside.md")
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-TARGET",
            ):
                archive_validation.read_worktree_regular_bounded(
                    root, "docs/pkg/record.md", max_bytes=32
                )

            target.unlink()
            target.write_bytes(b"stable\n")
            real_parent = root / "real-pkg"
            parent.rename(real_parent)
            parent.symlink_to(real_parent, target_is_directory=True)
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-MIGRATION-TARGET",
            ):
                archive_validation.read_worktree_regular_bounded(
                    root, "docs/pkg/record.md", max_bytes=32
                )

            parent.unlink()
            real_parent.rename(parent)
            original_read = archive_validation.os.read
            replaced = False

            def replace_after_read(descriptor: int, size: int) -> bytes:
                nonlocal replaced
                chunk = original_read(descriptor, size)
                if chunk and not replaced:
                    replacement = parent / "replacement.md"
                    replacement.write_bytes(b"changed\n")
                    replacement.replace(target)
                    replaced = True
                return chunk

            with (
                mock.patch.object(
                    archive_validation.os,
                    "read",
                    side_effect=replace_after_read,
                ),
                self.assertRaisesRegex(
                    archive_validation.ArchiveContractError,
                    "RECOVERY-MIGRATION-TARGET",
                ),
            ):
                archive_validation.read_worktree_regular_bounded(
                    root, "docs/pkg/record.md", max_bytes=32
                )

    def test_stage_zero_markdown_inventory_has_file_and_utf8_budgets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="staged-markdown-budget-") as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            invalid = "docs/03.specs/9999-invalid/spec.md"
            target = root / invalid
            target.parent.mkdir(parents=True)
            target.write_bytes(b"# invalid\n\xff")
            fixture.run("add", "--", invalid)
            inventory = archive_validation._staged_regular_blob_inventory(  # noqa: SLF001
                root.resolve()
            )
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-NON-UTF8",
            ):
                archive_validation._staged_markdown_documents(  # noqa: SLF001
                    root.resolve(), inventory, (invalid,)
                )

        with tempfile.TemporaryDirectory(prefix="staged-markdown-count-") as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            paths = tuple(
                f"docs/03.specs/9999-count/{index:04d}.md"
                for index in range(archive_validation.CURRENT_MARKDOWN_MAX_FILES + 1)
            )
            for relative in paths:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"# bounded\n")
            fixture.run("add", "--", *paths)
            with self.assertRaisesRegex(
                archive_validation.ArchiveContractError,
                "RECOVERY-RESOURCE-LIMIT",
            ):
                archive_validation._staged_regular_blob_inventory(  # noqa: SLF001
                    root.resolve()
                )

    def test_staged_markdown_batches_share_one_global_byte_budget(self) -> None:
        with tempfile.TemporaryDirectory(prefix="staged-global-budget-") as temporary:
            root = Path(temporary)
            fixture = GitFixture(root)
            paths: list[str] = []
            for index, marker in enumerate((b"a", b"b", b"c", b"d"), start=1):
                relative = f"docs/03.specs/9999-budget/{index:04d}.md"
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(marker * 30)
                paths.append(relative)
            fixture.run("add", "--", *paths)
            inventory = archive_validation._staged_regular_blob_inventory(  # noqa: SLF001
                root.resolve()
            )
            real_reader = archive_validation._read_git_blob_batch  # noqa: SLF001
            aggregate_limits: list[int] = []

            def read_batch(*args, **kwargs):
                aggregate_limits.append(kwargs["aggregate_limit"])
                return real_reader(*args, **kwargs)

            with (
                mock.patch.object(
                    archive_validation,
                    "MAX_GIT_BATCH_OBJECTS",
                    2,
                ),
                mock.patch.object(
                    archive_validation,
                    "CURRENT_MARKDOWN_TOTAL_BYTES",
                    100,
                ),
                mock.patch.object(
                    archive_validation,
                    "_read_git_blob_batch",
                    side_effect=read_batch,
                ),
                self.assertRaisesRegex(
                    archive_validation.ArchiveContractError,
                    "RECOVERY-RESOURCE-LIMIT",
                ),
            ):
                archive_validation._staged_markdown_documents(  # noqa: SLF001
                    root.resolve(), inventory, tuple(paths)
                )

            self.assertEqual(aggregate_limits, [100, 40])

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
            with (
                self.subTest(name=name),
                tempfile.TemporaryDirectory(
                    prefix="archive-migration-profile-"
                ) as temporary,
            ):
                root = Path(temporary)
                target = root / relative
                target.parent.mkdir(parents=True)
                target.write_bytes(content)

                records, diagnostics = archive_validation._repository_archive_records(
                    root
                )  # noqa: SLF001

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
            with (
                self.subTest(name=name),
                self.assertRaises(archive_validation.ArchiveContractError),
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

    def test_repository_archive_ignores_retired_stage99_namespace_projection(
        self,
    ) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        injected = dict(registry)
        injected["archiveNamespaces"] = [
            {
                "id": "retired-stage99-projection",
                "policy": "not-an-archive-owner",
                "records": ["docs/98.archive/untrusted.md"],
            }
        ]

        report = archive_validation.validate_repository_archive(ROOT, injected)

        self.assertTrue(report.valid, report.diagnostics)
        self.assertNotIn("ARCHIVE-NAMESPACE-CONTRACT", self.codes(report))

    def test_repository_archive_rejects_index_and_envelope_membership_drift(
        self,
    ) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        records, diagnostics = archive_validation._repository_archive_records(  # noqa: SLF001
            ROOT
        )
        missing_member = dict(records)
        missing_member.pop(next(iter(sorted(missing_member))))

        with mock.patch.object(
            archive_validation,
            "_repository_archive_records",
            return_value=(missing_member, diagnostics),
        ):
            report = archive_validation.validate_repository_archive(ROOT, registry)

        self.assertIn("ARCHIVE-MIGRATION-PARITY", self.codes(report))
        self.assertIn("ARCHIVE-INDEX-PARITY", self.codes(report))

    def test_repository_archive_binds_reviewed_manifest_metadata(self) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
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
        _rows, _total, diagnostics = archive_validation._parse_repository_index(  # noqa: SLF001
            invalid_null
        )
        self.assertIn(
            "ARCHIVE-INDEX-STRUCTURE",
            self.codes(types.SimpleNamespace(diagnostics=diagnostics)),
        )

        registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
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
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        real_popen = subprocess.Popen
        git_calls = 0
        # The budget bounds process startup, not reading: every batch is one
        # process regardless of how many objects it carries. MIG-0005 roughly
        # doubled the declared evidence, so the cap is sized for the current
        # corpus rather than the one it was first calibrated against.
        budget = 160

        def bounded_popen(*args, **kwargs):
            nonlocal git_calls
            command = args[0] if args else kwargs.get("args", ())
            if command and command[0] == "git":
                git_calls += 1
                if git_calls > budget:
                    raise AssertionError(
                        "repository archive exceeded Git subprocess budget"
                    )
            return real_popen(*args, **kwargs)

        started = time.monotonic()
        # Every subprocess.run call creates exactly one Popen. Count that shared
        # process boundary once instead of double-counting run plus its Popen.
        with mock.patch.object(subprocess, "Popen", side_effect=bounded_popen):
            report = archive_validation.validate_repository_archive(ROOT, registry)
        elapsed = time.monotonic() - started

        self.assertTrue(report.valid, report.diagnostics)
        # The power-of-two process budget covers staged authority inventory,
        # named-ref reachability, exact commit:path, and batched content reads
        # without introducing per-row subprocesses or a current count pin.
        self.assertLessEqual(git_calls, budget)
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
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        expected = {
            "docs/03.specs",
            "docs/03.specs/001-wsl-k3d-argocd-platform/spec.md",
            "docs/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md",
            "docs/03.specs/003-platform-expansion/spec.md",
            "docs/03.specs/README.md",
        }
        records, inventory_diagnostics = archive_validation._repository_archive_records(
            ROOT
        )  # noqa: SLF001
        self.assertEqual(inventory_diagnostics, [])
        original_paths = {
            str(
                archive_validation.parse_archive_envelope(content).metadata[
                    "original_path"
                ]
            )
            for content in records.values()
        }
        # Generic migration controls declare their own source paths; recovering
        # those rows is declared evidence, not an unbounded walk.
        original_paths |= _migration_declared_paths(ROOT)
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
        "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md"
    )
    archived_source = PurePosixPath(
        "docs/04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md"
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
            (edge.source.as_posix(), edge.target.as_posix()) for edge in handoff.edges
        )

        self.assertEqual(actual, ())
        self.assertEqual(
            handoff.navigation_boundary,
            "docs/98.archive/README.md#document-index",
        )

    def test_terminal_current_owners_are_derived_from_stage_owners(self) -> None:
        governance = self.context.governance_current_paths
        reference = self.context.reference_current_packs

        self.assertTrue(governance)
        self.assertEqual(self.context.governance_current_states, ("active",))
        self.assertTrue(
            all(
                self.context.profiles[path].profile_id == "governance/reference"
                and self.context.profiles[path].mode == "authored"
                and self.context.metadata[path].get("status") == "active"
                for path in governance
            )
        )
        self.assertEqual(
            [pack.id for pack in reference.packs], ["audits/2026-08-09-wgia"]
        )
        self.assertEqual(reference.profile_id, "content/reference")
        self.assertEqual(reference.packs[0].allowed_states, ("draft",))
        self.assertEqual(len(reference.packs[0].members), 9)

    def test_terminal_current_owner_derivation_fails_closed_on_missing_ria_owner(
        self,
    ) -> None:
        with (
            mock.patch.object(
                self.validator,
                "load_ria_contract",
                return_value={"currentPackBaselines": {}},
                create=True,
            ),
            self.assertRaises(self.validator.ConfigurationError),
        ):
            self.validator._build_context(ROOT)

    def test_mig0004_link_projection_accepts_semantically_valid_row_growth(
        self,
    ) -> None:
        path = self.validator.WORK054_WP004B_MIGRATION_PATH
        rows = self.validator.validate_pinned_migration_recovery(
            self.context.root,
            path.as_posix(),
            self.context.texts[path].encode("utf-8"),
        )
        legacy = "docs/03.specs/9999-semantic-growth/tasks.md"
        target = "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/README.md"
        added = {
            "legacy_path": legacy,
            "stable_path": None,
            "artifact_id": None,
            "action": "replaced",
            "replacement": target,
            "source_commit": "a" * 40,
            "source_blob": "b" * 40,
            "content_sha256": "c" * 64,
            "reason": "Canonical semantic growth fixture.",
        }

        with mock.patch.object(
            self.validator,
            "validate_pinned_migration_recovery",
            return_value=(*rows, added),
        ):
            targets = self.validator._work054_wp004b_targets(self.context)

        self.assertEqual(
            targets[PurePosixPath(legacy)],
            PurePosixPath(target),
        )

    def test_mig0004_link_projection_fails_closed_on_recovery_proof_error(
        self,
    ) -> None:
        with (
            mock.patch.object(
                self.validator,
                "validate_pinned_migration_recovery",
                side_effect=self.validator.ArchiveContractError(
                    "RECOVERY-MIGRATION-BLOB",
                    "fixture proof differs",
                ),
            ),
            self.assertRaisesRegex(
                self.validator.ConfigurationError,
                "migration recovery proof differs",
            ),
        ):
            self.validator._work054_wp004b_targets(self.context)

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

    def _predecessor_disposition_table(self) -> str:
        ledger = self.context.texts[self.validator.LEDGER_PATH]
        start = ledger.index("| Old path |")
        end = ledger.index("\n### Section-level split dispositions", start)
        return ledger[start:end]

    def _source_deleted_merge_history_table(self) -> str:
        ledger = self.context.texts[self.validator.LEDGER_PATH]
        start = ledger.index("### Source-deleted merge history")
        start = ledger.index("| path |", start)
        end = ledger.index("\n<!-- WERPC-007-HISTORICAL-ADM-TABLE -->", start)
        return ledger[start:end]

    def _terminal_ledger_context(self, ledger: str) -> object:
        return dataclasses.replace(
            self.context,
            route_state="terminal",
            ria_contract_text=None,
            ledger_bytes=ledger.encode("utf-8"),
            texts={**self.context.texts, self.validator.LEDGER_PATH: ledger},
        )

    def test_terminal_ledger_accepts_source_deleted_merge_history_only(
        self,
    ) -> None:
        diagnostics = self.validator._ledger_diagnostics(
            self._terminal_ledger_context(self._source_deleted_merge_history_table())
        )

        self.assertEqual(diagnostics, [])

    def test_terminal_ledger_does_not_consult_the_retired_inventory_parser(
        self,
    ) -> None:
        context = self._terminal_ledger_context(
            self._source_deleted_merge_history_table()
        )

        with mock.patch.object(
            self.validator,
            "_ledger_rows",
            side_effect=AssertionError("terminal route parsed retired inventory"),
        ):
            diagnostics = self.validator._ledger_diagnostics(context)

        self.assertEqual(diagnostics, [])

    def test_terminal_ledger_missing_path_or_text_still_fails(self) -> None:
        for name, paths, texts in (
            (
                "path",
                tuple(
                    path
                    for path in self.context.paths
                    if path != self.validator.LEDGER_PATH
                ),
                self.context.texts,
            ),
            (
                "text",
                self.context.paths,
                {
                    path: text
                    for path, text in self.context.texts.items()
                    if path != self.validator.LEDGER_PATH
                },
            ),
        ):
            with self.subTest(name=name):
                context = dataclasses.replace(
                    self.context,
                    route_state="terminal",
                    ria_contract_text=None,
                    ledger_bytes=None,
                    paths=paths,
                    texts=texts,
                )

                diagnostics = self.validator._ledger_diagnostics(context)

                self.assertEqual(
                    [item.rule_id for item in diagnostics], ["LEDGER-MISSING"]
                )

    def test_terminal_ledger_protection_control_and_drift_precede_return(
        self,
    ) -> None:
        ledger = self.context.texts[self.validator.LEDGER_PATH]
        settlement = {
            "id": self.validator.LEDGER_SETTLEMENT_ID,
            "packId": self.validator.LEDGER_SETTLEMENT_PACK_ID,
            "fromCommit": self.validator.LEDGER_SETTLEMENT_FROM_COMMIT,
            "subject": self.validator.LEDGER_SETTLEMENT_SUBJECT,
            "targetSha256": hashlib.sha256(ledger.encode("utf-8")).hexdigest(),
            "targetByteLength": len(ledger.encode("utf-8")),
            "reason": self.validator.LEDGER_SETTLEMENT_REASON,
            "transitionCommit": "git-sha1:" + "a" * 40,
        }
        contract = {
            "baselineTransitions": [],
            "baselineSettlements": [settlement],
            "currentPackBaselines": {
                self.validator.LEDGER_SETTLEMENT_PACK_ID: settlement["transitionCommit"]
            },
        }
        with mock.patch.object(
            self.validator,
            "load_agent_cutover_projections",
            return_value={},
        ):
            control = dataclasses.replace(
                self.context,
                route_state="terminal",
                ria_contract_text=json.dumps(contract),
                ledger_bytes=ledger.encode("utf-8"),
            )
            self.assertEqual(self.validator._ledger_diagnostics(control), [])

            for name, changed_contract, changed_ledger in (
                (
                    "metadata",
                    {
                        **contract,
                        "baselineSettlements": [{**settlement, "reason": "tampered"}],
                    },
                    ledger,
                ),
                ("bytes", contract, ledger + "\nTampered."),
            ):
                with self.subTest(name=name):
                    context = dataclasses.replace(
                        self.context,
                        route_state="terminal",
                        ria_contract_text=json.dumps(changed_contract),
                        ledger_bytes=changed_ledger.encode("utf-8"),
                        texts={
                            **self.context.texts,
                            self.validator.LEDGER_PATH: changed_ledger,
                        },
                    )

                    diagnostics = self.validator._ledger_diagnostics(context)

                    self.assertEqual(
                        [item.rule_id for item in diagnostics],
                        ["LEDGER-PROTECTED-DRIFT"],
                    )

    def test_predecessor_disposition_validation_stays_complete_and_exact(self) -> None:
        table = self._predecessor_disposition_table()
        first_row = next(
            line for line in table.splitlines() if line.startswith("| `docs/")
        )
        invalid_commit = first_row.replace(
            "`147b27badd56e4ec10f8725c59e312a6d12c63f4`",
            "`not-a-commit`",
            1,
        )
        invalid_disposition = first_row.replace(
            self.validator.WERPC_DELETION_DISPOSITION,
            "Retained",
            1,
        )
        missing_row = table.replace(first_row + "\n", "", 1)
        duplicate_row = table.rstrip() + "\n" + first_row

        self.assertEqual(
            len(self.validator._werpc_predecessor_disposition_map(table)),
            len(self.validator.WERPC_PREDECESSOR_PATHS),
        )
        for name, changed in (
            ("missing", missing_row),
            ("duplicate", duplicate_row),
            ("commit", table.replace(first_row, invalid_commit, 1)),
            ("disposition", table.replace(first_row, invalid_disposition, 1)),
        ):
            with self.subTest(name=name):
                self.assertIsNone(
                    self.validator._werpc_predecessor_disposition_map(changed)
                )

    def test_nonterminal_ledger_keeps_retired_inventory_shape_rejection(self) -> None:
        context = dataclasses.replace(
            self._terminal_ledger_context(self._predecessor_disposition_table()),
            route_state="transition",
        )

        diagnostics = self.validator._ledger_diagnostics(context)

        self.assertEqual([item.rule_id for item in diagnostics], ["LEDGER-INCOMPLETE"])

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

    def _work054_edges(self, context: object) -> dict[object, PurePosixPath]:
        _aliases, move_targets, _replacements = (
            self.validator._document_taxonomy_transition_manifest(context)
        )
        return self.validator._reviewed_work054_historical_owner_edges(
            context,
            move_targets,
        )

    def test_terminal_route_does_not_project_an_active_stale_owner_edge(self) -> None:
        source = PurePosixPath(
            "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md"
        )
        retired = PurePosixPath(
            "docs/00.agent-governance/" + "common-" + "governance.md"
        )
        raw = self.validator.posixpath.relpath(retired, source.parent)
        context = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: self.context.texts[source] + f"\n[retired]({raw})\n",
            },
        )

        projected = self._work054_edges(context)
        self.assertNotIn(
            self.validator.ArchiveTransitionEdge(source, retired),
            projected,
        )
        self.assertEqual(
            self.validator._reviewed_immutable_historical_alias_edges(context, {}),
            {},
        )
        self.assertEqual(
            self.validator._reviewed_completed_history_alias_edges(context, {}),
            {},
        )

    def test_removed_directory_link_needs_every_file_proved(self) -> None:
        """A directory link resolves only when each file it held moved to an owner."""

        source = PurePosixPath("docs/90.references/audits/2099-01-01-dir/report.md")
        profile = self.validator.ProfileView(
            "content/reference", "common", "classification-only"
        )
        removed = PurePosixPath(".agents/workflows")
        unproved = PurePosixPath(".agents/never-existed")
        body = "\n".join(
            f"[{target.name}]({self.validator.posixpath.relpath(target, source.parent)})"
            for target in (removed, unproved)
        )
        context = dataclasses.replace(
            self.context,
            paths=(*self.context.paths, source),
            profiles={**self.context.profiles, source: profile},
            texts={**self.context.texts, source: body + "\n"},
            metadata={**self.context.metadata, source: {"status": "draft"}},
            tracked_regular_paths=self.context.tracked_regular_paths | {source},
        )

        broken = {
            item.actual
            for item in self.validator._link_diagnostics(context)
            if item.rule_id == "LINK-BROKEN" and item.path == source
        }

        # Every file the directory held has a proved replacement, so the link stands.
        self.assertNotIn(removed.as_posix(), broken)
        # A directory with no disposition at all stays broken; the rule fails closed.
        self.assertIn(unproved.as_posix(), broken)

    def test_active_source_cannot_use_declared_migration_or_tasks_aliases(
        self,
    ) -> None:
        source = PurePosixPath("docs/00.agent-governance/current-stale-link.md")
        profile = self.validator.ProfileView(
            "governance/reference", "governance", "authored"
        )
        targets = (
            PurePosixPath("docs/99.templates/support/document-contract.md"),
            PurePosixPath(
                "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
            ),
        )
        links = "\n".join(
            f"[retired {index}]({self.validator.posixpath.relpath(target, source.parent)})"
            for index, target in enumerate(targets, start=1)
        )
        context = dataclasses.replace(
            self.context,
            paths=(*self.context.paths, source),
            profiles={**self.context.profiles, source: profile},
            texts={**self.context.texts, source: links + "\n"},
            metadata={**self.context.metadata, source: {"status": "active"}},
            tracked_regular_paths=self.context.tracked_regular_paths | {source},
        )

        diagnostics = self.validator._link_diagnostics(context)

        broken = {
            item.actual
            for item in diagnostics
            if item.rule_id == "LINK-BROKEN" and item.path == source
        }
        self.assertEqual(broken, {target.as_posix() for target in targets})

    def test_future_done_task_cannot_enter_historical_migration_waiver(
        self,
    ) -> None:
        source = PurePosixPath(
            "docs/03.specs/9999-future-change/tasks/tsk-0001-future.md"
        )
        retired = PurePosixPath("docs/99.templates/support/document-contract.md")
        raw = self.validator.posixpath.relpath(retired, source.parent)
        context = dataclasses.replace(
            self.context,
            paths=(*self.context.paths, source),
            profiles={
                **self.context.profiles,
                source: self.validator.ProfileView("sdlc/task", "sdlc", "authored"),
            },
            texts={**self.context.texts, source: f"[retired]({raw})\n"},
            metadata={**self.context.metadata, source: {"status": "done"}},
            tracked_regular_paths=self.context.tracked_regular_paths | {source},
        )

        projected = self._work054_edges(context)

        self.assertNotIn(
            self.validator.ArchiveTransitionEdge(source, retired),
            projected,
        )

    def test_future_accepted_adr_cannot_enter_historical_migration_waiver(
        self,
    ) -> None:
        source = PurePosixPath("docs/02.architecture/decisions/9999-future-decision.md")
        retired = PurePosixPath("docs/99.templates/support/document-contract.md")
        raw = self.validator.posixpath.relpath(retired, source.parent)
        context = dataclasses.replace(
            self.context,
            paths=(*self.context.paths, source),
            profiles={
                **self.context.profiles,
                source: self.validator.ProfileView("sdlc/adr", "sdlc", "authored"),
            },
            texts={**self.context.texts, source: f"[retired]({raw})\n"},
            metadata={**self.context.metadata, source: {"status": "accepted"}},
            tracked_regular_paths=self.context.tracked_regular_paths | {source},
        )

        projected = self._work054_edges(context)

        self.assertNotIn(
            self.validator.ArchiveTransitionEdge(source, retired),
            projected,
        )

    def test_terminal_current_progress_uses_no_historical_projection(
        self,
    ) -> None:
        source = PurePosixPath("docs/00.agent-governance/memory/progress.md")
        target = PurePosixPath(
            "docs/03.specs/009-workspace-harness-research-pack/tasks.md"
        )
        edge = self.validator.ArchiveTransitionEdge(source, target)

        projected = self.validator._reviewed_work054_historical_owner_edges(
            self.context,
            {},
        )

        self.assertNotIn(edge, projected)

    def test_terminal_history_composes_taxonomy_mig0002_and_mig0004_edges(
        self,
    ) -> None:
        source = PurePosixPath(
            "docs/90.references/audits/2026-07-02-whia/"
            "harness-loop-implementation-audit.md"
        )
        target = PurePosixPath(
            "docs/04.execution/tasks/"
            "2026-07-02-workspace-harness-implementation-audit-pack.md"
        )
        expected = PurePosixPath(
            "docs/03.specs/0010-workspace-harness-implementation-audit-pack/README.md"
        )
        _move_blobs, move_targets, _archive_sources = (
            self.validator._document_taxonomy_transition_manifest(self.context)
        )

        projected = self.validator._reviewed_work054_historical_owner_edges(
            self.context,
            move_targets,
        )

        self.assertEqual(
            projected[self.validator.ArchiveTransitionEdge(source, target)],
            expected,
        )

    def test_terminal_history_uses_ria_retired_pack_profile_and_path_scope(
        self,
    ) -> None:
        source = PurePosixPath("docs/90.references/audits/2026-07-11-weia/README.md")
        target = PurePosixPath(
            "docs/99.templates/templates/common/reference.template.md"
        )
        expected = PurePosixPath(
            "docs/99.templates/templates/references/reference.template.md"
        )

        projected = self.validator._reviewed_work054_historical_owner_edges(
            self.context,
            {},
        )

        self.assertEqual(
            projected[self.validator.ArchiveTransitionEdge(source, target)],
            expected,
        )

    def test_terminal_historical_source_rejects_pinned_blob_drift(self) -> None:
        source = PurePosixPath("docs/90.references/audits/2026-07-11-weia/README.md")
        drifted = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: self.context.texts[source] + "\n",
            },
        )

        self.assertFalse(
            self.validator._terminal_frozen_manifest_source(drifted, source)
        )

    def test_terminal_history_keeps_exact_frozen_cloud_manifest_source(
        self,
    ) -> None:
        source = PurePosixPath("docs/90.references/cloud-examples/README.md")
        target = PurePosixPath("docs/03.specs/030-authored-document-migration/spec.md")
        expected = PurePosixPath(
            "docs/03.specs/0030-authored-document-migration/spec.md"
        )

        projected = self.validator._reviewed_work054_historical_owner_edges(
            self.context,
            {},
        )

        self.assertEqual(
            projected[self.validator.ArchiveTransitionEdge(source, target)],
            expected,
        )

    def test_work054_historical_projection_rejects_undeclared_retired_edge(
        self,
    ) -> None:
        source = PurePosixPath("fixture.md")
        undeclared = PurePosixPath(
            "docs/00.agent-governance/retired-without-migration.md"
        )
        raw = self.validator.posixpath.relpath(undeclared, source.parent)
        fixture_profile = next(iter(self.context.profiles.values()))
        context = dataclasses.replace(
            self.context,
            paths=(*self.context.paths, source),
            profiles={**self.context.profiles, source: fixture_profile},
            texts={
                **self.context.texts,
                source: f"[retired]({raw})\n",
            },
            metadata={**self.context.metadata, source: {}},
            tracked_regular_paths=self.context.tracked_regular_paths | {source},
        )

        diagnostics = self.validator._link_diagnostics(context)

        self.assertTrue(
            any(
                item.rule_id == "LINK-BROKEN" and item.path == source
                for item in diagnostics
            )
        )

    def test_standalone_approval_statements_are_relation_specific(self) -> None:
        statements = self.validator.STANDALONE_APPROVAL_STATEMENTS

        self.assertEqual(
            set(statements),
            # 0055-0061 are the renumbered successors the consolidation
            # merge introduced alongside the original three, and 0062 is the
            # standalone execution the same merge declared in the registry.
            {
                "0043",
                "0053",
                "0054",
                "0062",
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
            "source-blob": lambda rows: rows[0].__setitem__("source_blob", "0" * 40),
            "stable-target": lambda rows: rows[0].__setitem__(
                "stable_path", "docs/01.requirements/9999-unreviewed.md"
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                context = self._mutated_work109_context(mutate)
                with self.assertRaises(self.validator.ConfigurationError):
                    self.validator._work109_four_digit_aliases(context)

    def test_terminal_route_skips_transition_only_source_pins(self) -> None:
        source = next(
            iter(sorted(self.validator.IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS))
        )
        drifted_context = dataclasses.replace(
            self.context,
            texts={
                **self.context.texts,
                source: self.context.texts[source] + "\n",
            },
        )

        self.assertEqual(
            self.validator._reviewed_immutable_historical_alias_edges(
                drifted_context,
                {},
            ),
            {},
        )
        self.assertEqual(
            self.validator._reviewed_completed_history_alias_edges(
                drifted_context,
                {},
            ),
            {},
        )

    def test_work107_stable_archive_aliases_are_exact_and_tracked(self) -> None:
        aliases = self.validator._work107_stable_archive_aliases(self.context)

        self.assertTrue(aliases)
        self.assertEqual(len(set(aliases.values())), len(aliases))
        self.assertTrue(
            all(
                target in self.context.tracked_regular_paths
                for target in aliases.values()
            )
        )

    def test_terminal_archive_index_uses_current_semantic_targets(self) -> None:
        source = PurePosixPath("docs/98.archive/README.md")
        text = self.context.texts[source]
        local_targets = {
            target
            for raw in self.validator._extract_links(text)
            for kind, target in [self.validator._local_destination(source, raw)]
            if kind == "local" and target is not None
        }

        self.assertFalse(
            self.validator._work107_stable_archive_index_source(
                self.context,
                source,
            )
        )
        self.assertTrue(
            {
                PurePosixPath(
                    "docs/01.requirements/0004-current-local-gitops-platform.md"
                ),
                PurePosixPath(
                    "docs/02.architecture/descriptions/"
                    "0007-current-local-gitops-platform.md"
                ),
                PurePosixPath(
                    "docs/03.specs/0008-current-local-gitops-platform/spec.md"
                ),
            }.issubset(local_targets)
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

    def test_terminal_handoff_does_not_consume_transition_manifest(self) -> None:
        with mock.patch.object(
            self.validator,
            "_reviewed_taxonomy_manifest",
            side_effect=self.validator.ConfigurationError(
                "archive transition manifest worktree/index differs"
            ),
        ):
            handoff = self.validator._archive_transition_handoff(self.context)

        self.assertEqual(handoff.edges, ())


if __name__ == "__main__":
    unittest.main()
