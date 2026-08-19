"""ARWB-003 production atomic-cutover tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from dataclasses import replace
from io import StringIO
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from scripts import archive_cutover, archive_recovery, archive_validation  # noqa: E402
from scripts.archive_recovery import parse_archive_envelope  # noqa: E402
from scripts.archive_validation import (  # noqa: E402
    ArchiveDiagnostic,
    ArchiveValidationReport,
)
from scripts.document_contracts import load_registry  # noqa: E402
from scripts.document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    LifecycleEvidenceContext,
    compare_lifecycle,
    document_from_text,
)


class ArchiveCutoverTest(unittest.TestCase):
    def _validate_without_repeating_secret_classification(
        self,
    ) -> archive_cutover.CutoverReport:
        with patch.object(archive_cutover, "_secret_classifier", return_value=None):
            return archive_cutover.validate_repository_cutover(ROOT)

    def _assert_named_partial(
        self,
        report: archive_cutover.CutoverReport,
        expected_code: str,
    ) -> None:
        codes = {diagnostic.code for diagnostic in report.diagnostics}
        self.assertIn("ARCHIVE-CUTOVER-INCOMPLETE", codes)
        self.assertIn(expected_code, codes)

    def _report_with_index_mutation(self, mutate) -> archive_cutover.CutoverReport:
        original_read_text = Path.read_text
        index_path = (ROOT / archive_cutover.ARCHIVE_INDEX).resolve()

        def mutated_index(path: Path, *args, **kwargs) -> str:
            text = original_read_text(path, *args, **kwargs)
            return mutate(text) if path.resolve() == index_path else text

        with patch.object(Path, "read_text", new=mutated_index):
            return self._validate_without_repeating_secret_classification()

    @staticmethod
    def _manifest_rows(text: str) -> tuple[list[str], list[int]]:
        lines = text.splitlines(keepends=True)
        return lines, [
            offset for offset, line in enumerate(lines) if line.startswith("| [`")
        ]

    @staticmethod
    def _cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    @staticmethod
    def _row(cells: list[str]) -> str:
        return "| " + " | ".join(cells) + " |\n"

    def test_repository_snapshot_is_complete_and_atomic(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/archive_cutover.py",
                "--root",
                ".",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(
            completed.returncode,
            0,
            completed.stdout or completed.stderr,
        )
        self.assertEqual(
            completed.stdout,
            "PASS archive cutover records=93 historical_links=711 secret_clean=93\n",
        )
        self.assertEqual(completed.stderr, "")

    def test_work107_repository_is_exact_stable_93_to_93(self) -> None:
        migration_path = ROOT / archive_recovery.WORK107_MIGRATION_PATH
        rows = archive_recovery.parse_work107_migration_document(
            migration_path.read_bytes()
        )
        rows = archive_recovery.validate_work107_migration_rows(ROOT, rows)
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        namespace_paths = {
            path
            for namespace in registry["archiveNamespaces"]
            for path in namespace["records"]
        }
        self.assertEqual(namespace_paths, {row["stable_path"] for row in rows})

        for row in rows:
            with self.subTest(stable=row["stable_path"]):
                self.assertFalse((ROOT / row["legacy_path"]).exists())
                stable = ROOT / row["stable_path"]
                self.assertTrue(stable.is_file())
                terminal = parse_archive_envelope(stable.read_bytes())
                legacy = archive_recovery.recover_work107_legacy_envelope(ROOT, row)
                self.assertEqual(terminal.payload, legacy.payload)
                for key in ("source_commit", "source_blob", "content_sha256"):
                    self.assertEqual(terminal.metadata[key], row[key])
                if row["record_kind"].startswith("change-"):
                    expected_change = row["artifact_id"].split("-", 1)[1]
                    self.assertEqual(terminal.metadata["change_id"], expected_change)
                else:
                    self.assertNotIn("change_id", terminal.metadata)

    def test_work107_index_has_only_stable_record_links(self) -> None:
        rows = archive_recovery.build_work107_migration_rows(ROOT)
        index = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")
        for row in rows:
            with self.subTest(stable=row["stable_path"]):
                relative = row["stable_path"].removeprefix("docs/98.archive/")
                self.assertIn(f"](./{relative})", index)
                legacy_relative = row["legacy_path"].removeprefix("docs/98.archive/")
                self.assertNotIn(f"](./{legacy_relative})", index)

    def test_finite_base_proof_remains_exact_inside_the_aggregate(self) -> None:
        text = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")

        rows, structure_failure = archive_cutover._parse_archive_index(text)
        stable_by_legacy = {
            str(row["legacy_path"]): str(row["stable_path"])
            for row in archive_recovery.build_work107_migration_rows(ROOT)
        }
        base_rows = {
            stable_by_legacy[path]: rows[stable_by_legacy[path]]
            for path in archive_cutover.EXPECTED_ARCHIVE_PATHS
            if stable_by_legacy[path] in rows
        }

        self.assertFalse(structure_failure)
        self.assertEqual(len(base_rows), 31)
        self.assertEqual(
            sum(row.historical_links for row in base_rows.values()),
            archive_cutover.EXPECTED_HISTORICAL_LINKS,
        )
        self.assertEqual(archive_cutover.EXPECTED_HISTORICAL_LINKS, 202)
        self.assertEqual(len(rows), 93)
        self.assertEqual(sum(row.historical_links for row in rows.values()), 711)

    def test_repository_cutover_calls_generic_v2_boundary(self) -> None:
        index_text = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")
        index_rows, structure_failure = archive_cutover._parse_archive_index(index_text)
        self.assertFalse(structure_failure)
        generic = ArchiveValidationReport(
            historical_link_count=711,
            record_count=93,
            index_record_count=93,
            namespace_counts=(
                ("arwb-base", 31),
                ("acer-additive", 12),
                ("wdtc-execution", 50),
                ("progress-snapshot", 0),
            ),
            record_link_counts=tuple(
                (path, row.historical_links)
                for path, row in sorted(index_rows.items())
            ),
            reviewed_manifest_records=tuple(
                archive_validation._reviewed_manifest_records(ROOT).values()  # noqa: SLF001
            ),
        )
        with (
            patch.object(archive_cutover, "validate_repository_archive", return_value=generic) as validate,
            patch.object(
                archive_cutover, "_secret_classifier", return_value=None
            ) as secret_classifier,
        ):
            report = archive_cutover.validate_repository_cutover(ROOT)

        self.assertTrue(report.valid, report.diagnostics)
        validate.assert_called_once()
        secret_classifier.assert_called_once()

    def test_secret_classifier_failure_is_redacted_for_new_namespace(self) -> None:
        sentinel = "PAYLOAD-SENTINEL-MUST-NOT-LEAK"

        with patch.object(
            archive_cutover,
            "_secret_classifier",
            return_value=archive_cutover.CutoverDiagnostic(
                "ARCHIVE-SECRET-DETECTED",
                "docs/98.archive/04.execution/plans/fixture.md",
            ),
        ):
            report = archive_cutover.validate_repository_cutover(ROOT)

        rendered = repr(report) + " ".join(map(str, report.diagnostics))
        self.assertIn("ARCHIVE-SECRET-DETECTED", rendered)
        self.assertNotIn(sentinel, rendered)

    def test_partial_projection_emits_named_red_without_payload(self) -> None:
        report = archive_cutover.CutoverReport(
            diagnostics=(
                archive_cutover.CutoverDiagnostic(
                    code="ARCHIVE-CUTOVER-INCOMPLETE",
                    path="<repository>",
                ),
            ),
            record_count=30,
            historical_link_count=201,
            secret_clean_count=30,
        )
        output = StringIO()
        with (
            patch.object(
                archive_cutover,
                "validate_repository_cutover",
                return_value=report,
            ),
            redirect_stdout(output),
        ):
            return_code = archive_cutover.main(["--root", "."])

        self.assertEqual(return_code, 1)
        self.assertEqual(
            output.getvalue(),
            "FAIL ARCHIVE-CUTOVER-INCOMPLETE path=<repository>\n",
        )

    def test_partial_manifest_is_rejected(self) -> None:
        original_read_text = Path.read_text
        index_path = (ROOT / archive_cutover.ARCHIVE_INDEX).resolve()

        def without_manifest(path: Path, *args, **kwargs) -> str:
            text = original_read_text(path, *args, **kwargs)
            if path.resolve() == index_path:
                return archive_cutover._INDEX_MANIFEST.sub("", text, count=1)
            return text

        with patch.object(Path, "read_text", new=without_manifest):
            report = self._validate_without_repeating_secret_classification()
        self._assert_named_partial(report, "ARCHIVE-INDEX-MANIFEST")

    def test_index_manifest_rejects_missing_duplicate_and_extra_rows(self) -> None:
        def missing(text: str) -> str:
            lines, rows = self._manifest_rows(text)
            lines.pop(rows[0])
            return "".join(lines)

        def duplicate(text: str) -> str:
            lines, rows = self._manifest_rows(text)
            lines.insert(rows[0], lines[rows[0]])
            return "".join(lines)

        def extra(text: str) -> str:
            lines, rows = self._manifest_rows(text)
            cells = self._cells(lines[rows[0]])
            cells[0] = cells[0].replace(".md`", "-extra.md`")
            lines.insert(rows[-1] + 1, self._row(cells))
            return "".join(lines)

        for label, mutation in (
            ("missing", missing),
            ("duplicate", duplicate),
            ("extra", extra),
        ):
            with self.subTest(label=label):
                report = self._report_with_index_mutation(mutation)
                self._assert_named_partial(report, "ARCHIVE-INDEX-STRUCTURE")

    def test_index_manifest_rejects_column_swap(self) -> None:
        def swap_columns(text: str) -> str:
            lines, rows = self._manifest_rows(text)
            cells = self._cells(lines[rows[0]])
            cells[2], cells[3] = cells[3], cells[2]
            lines[rows[0]] = self._row(cells)
            return "".join(lines)

        report = self._report_with_index_mutation(swap_columns)
        self._assert_named_partial(report, "ARCHIVE-INDEX-MEMBER")

    def test_index_manifest_rejects_two_row_digest_swap(self) -> None:
        def swap_digests(text: str) -> str:
            lines, rows = self._manifest_rows(text)
            first = self._cells(lines[rows[0]])
            second = self._cells(lines[rows[1]])
            first[5], second[5] = second[5], first[5]
            lines[rows[0]] = self._row(first)
            lines[rows[1]] = self._row(second)
            return "".join(lines)

        report = self._report_with_index_mutation(swap_digests)
        self._assert_named_partial(report, "ARCHIVE-INDEX-MEMBER")

    def test_index_only_replacement_evolution_preserves_immutable_envelope(
        self,
    ) -> None:
        replacement = "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md"

        def evolve_replacement(text: str) -> str:
            lines, rows = self._manifest_rows(text)
            cells = self._cells(lines[rows[0]])
            cells[7] = (
                f"[`{replacement}`](../03.specs/0036-archive-record-and-workspace-boundary/spec.md)"
            )
            lines[rows[0]] = self._row(cells)
            return "".join(lines)

        report = self._report_with_index_mutation(evolve_replacement)

        self.assertTrue(report.valid, report.diagnostics)

    def test_index_archive_to_archive_replacement_is_rejected(self) -> None:
        target = archive_cutover.EXPECTED_ARCHIVE_PATHS[1]
        target_label = target.removeprefix("docs/98.archive/")

        def point_to_archive(text: str) -> str:
            lines, rows = self._manifest_rows(text)
            cells = self._cells(lines[rows[0]])
            cells[7] = f"[`{target}`](./{target_label})"
            lines[rows[0]] = self._row(cells)
            return "".join(lines)

        report = self._report_with_index_mutation(point_to_archive)

        self._assert_named_partial(report, "ARCHIVE-REPLACEMENT-ARCHIVE")

    def test_replacement_target_authority_fails_closed(self) -> None:
        registry = load_registry(ROOT)
        tracked = archive_cutover._tracked_regular_blobs(ROOT)
        current = "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md"
        template = "docs/99.templates/templates/common/archive-record.template.md"

        self.assertEqual(
            archive_cutover._replacement_target_diagnostic(
                ROOT,
                registry,
                archive_cutover.EXPECTED_ARCHIVE_PATHS[0],
                tracked,
            ),
            "ARCHIVE-REPLACEMENT-ARCHIVE",
        )
        self.assertEqual(
            archive_cutover._replacement_target_diagnostic(
                ROOT,
                registry,
                "docs/03.specs/999-missing/spec.md",
                tracked,
            ),
            "ARCHIVE-REPLACEMENT-MISSING",
        )
        with patch.object(
            archive_cutover,
            "classify_path",
            side_effect=archive_cutover.DocumentContractError(()),
        ):
            self.assertEqual(
                archive_cutover._replacement_target_diagnostic(
                    ROOT,
                    registry,
                    current,
                    tracked,
                ),
                "ARCHIVE-REPLACEMENT-UNSELECTED",
            )
        self.assertEqual(
            archive_cutover._replacement_target_diagnostic(
                ROOT,
                registry,
                template,
                tracked,
            ),
            "ARCHIVE-REPLACEMENT-PROFILE",
        )
        for status in ("draft", "archived"):
            with self.subTest(status=status):
                with patch.object(
                    archive_cutover,
                    "document_from_text",
                    return_value=LifecycleDocument(
                        PurePosixPath(current), "sdlc/spec", status
                    ),
                ):
                    self.assertEqual(
                        archive_cutover._replacement_target_diagnostic(
                            ROOT,
                            registry,
                            current,
                            tracked,
                        ),
                        "ARCHIVE-REPLACEMENT-NONCURRENT",
                    )

    def test_work054_mig0002_projection_is_exact_and_current(self) -> None:
        tracked = archive_cutover._tracked_regular_blobs(ROOT)

        projection = archive_cutover._work054_migration_projection(ROOT, tracked)

        self.assertEqual(len(projection.current_by_legacy), 154)
        self.assertEqual(
            projection.action_counts,
            (("merged", 10), ("moved", 141), ("replaced", 3)),
        )
        self.assertEqual(
            projection.current_by_legacy[
                "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md"
            ],
            "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
        )
        self.assertEqual(
            projection.current_by_legacy[
                "docs/00.agent-governance/rules/document-stage-routing.md"
            ],
            "docs/00.agent-governance/rules/document-authoring.md",
        )
        self.assertEqual(
            projection.current_by_legacy["docs/04.execution/plans/README.md"],
            "docs/99.templates/templates/sdlc/execution/plan.template.md",
        )

    def test_work054_mig0002_projection_rejects_any_byte_drift(self) -> None:
        migration_path = (ROOT / archive_cutover.WORK054_MIGRATION_PATH).resolve()
        original_read_bytes = Path.read_bytes

        def drift_migration(path: Path) -> bytes:
            content = original_read_bytes(path)
            return content + b"\n" if path.resolve() == migration_path else content

        with patch.object(Path, "read_bytes", new=drift_migration):
            with self.assertRaisesRegex(
                RuntimeError,
                "^WORK-054 migration ledger is unavailable$",
            ):
                archive_cutover._work054_migration_projection(
                    ROOT,
                    archive_cutover._tracked_regular_blobs(ROOT),
                )

    def test_work105_legacy_ad_replacement_alias_is_exact_and_fails_closed(
        self,
    ) -> None:
        index_text = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")
        index_rows, structure_failure = archive_cutover._parse_archive_index(index_text)
        self.assertFalse(structure_failure)

        legacy_paths = (
            "docs/98.archive/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md",
            "docs/98.archive/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md",
            "docs/98.archive/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md",
        )
        legacy_replacement = (
            "docs/02.architecture/requirements/0007-current-local-gitops-platform.md"
        )
        current_replacement = (
            "docs/02.architecture/descriptions/ad-0007-current-local-gitops-platform.md"
        )
        stable_by_legacy = {
            str(row["legacy_path"]): str(row["stable_path"])
            for row in archive_recovery.build_work107_migration_rows(ROOT)
        }

        for archive_path in legacy_paths:
            with self.subTest(archive_path=archive_path):
                stable_path = stable_by_legacy[archive_path]
                metadata = parse_archive_envelope((ROOT / stable_path).read_bytes()).metadata
                index_row = replace(
                    index_rows[stable_path], archive_path=archive_path
                )
                self.assertEqual(index_row.replacement, legacy_replacement)
                self.assertEqual(
                    archive_cutover._work105_replacement_target(
                        archive_path,
                        index_row,
                        metadata,
                    ),
                    current_replacement,
                )

        first_path = legacy_paths[0]
        first_stable = stable_by_legacy[first_path]
        first_row = replace(index_rows[first_stable], archive_path=first_path)
        first_metadata = parse_archive_envelope(
            (ROOT / first_stable).read_bytes()
        ).metadata
        rejected = (
            (
                "unknown archive row",
                "docs/98.archive/02.architecture/requirements/0004-unapproved.md",
                replace(
                    first_row,
                    archive_path=(
                        "docs/98.archive/02.architecture/requirements/0004-unapproved.md"
                    ),
                ),
                first_metadata,
            ),
            (
                "replacement path drift",
                first_path,
                replace(first_row, replacement=f"{legacy_replacement}.extra"),
                first_metadata,
            ),
            (
                "source blob drift",
                first_path,
                replace(first_row, source_blob="f" * 40),
                first_metadata,
            ),
            (
                "index original path drift",
                first_path,
                replace(first_row, original_path=f"{first_row.original_path}.extra"),
                first_metadata,
            ),
            (
                "archive envelope proof drift",
                first_path,
                first_row,
                {**first_metadata, "source_blob": "f" * 40},
            ),
        )
        for label, archive_path, index_row, metadata in rejected:
            with self.subTest(label=label):
                self.assertEqual(
                    archive_cutover._work105_replacement_target(
                        archive_path,
                        index_row,
                        metadata,
                    ),
                    index_row.replacement,
                )

    def test_replacement_target_status_comes_from_index_blob(self) -> None:
        registry = load_registry(ROOT)
        target = "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md"
        path = PurePosixPath(target)
        staged_draft = "---\ntype: sdlc/spec\nstatus: draft\n---\n\n# Staged draft\n"
        worktree_done = staged_draft.replace("status: draft", "status: done")

        with TemporaryDirectory(prefix="archive-cutover-index-authority-") as raw:
            repository = Path(raw)
            subprocess.run(
                ["git", "init", "--quiet"],
                cwd=repository,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
            target_path = repository / target
            target_path.parent.mkdir(parents=True)
            target_path.write_text(staged_draft, encoding="utf-8")
            subprocess.run(
                ["git", "add", "--", target],
                cwd=repository,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
            target_path.write_text(worktree_done, encoding="utf-8")

            tracked = archive_cutover._tracked_regular_blobs(repository)
            worktree_document = document_from_text(
                registry,
                path,
                target_path.read_text(encoding="utf-8"),
            )

            self.assertEqual(worktree_document.status, "done")
            self.assertEqual(
                archive_cutover._replacement_target_diagnostic(
                    repository,
                    registry,
                    target,
                    tracked,
                ),
                "ARCHIVE-REPLACEMENT-NONCURRENT",
            )

            target_path.write_text(worktree_done, encoding="utf-8")
            subprocess.run(
                ["git", "add", "--", target],
                cwd=repository,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
            target_path.unlink()
            tracked = archive_cutover._tracked_regular_blobs(repository)
            self.assertIsNone(
                archive_cutover._replacement_target_diagnostic(
                    repository,
                    registry,
                    target,
                    tracked,
                )
            )

            target_path.write_bytes(b"\xff")
            subprocess.run(
                ["git", "add", "--", target],
                cwd=repository,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
            target_path.write_text(worktree_done, encoding="utf-8")
            tracked = archive_cutover._tracked_regular_blobs(repository)
            self.assertEqual(
                archive_cutover._replacement_target_diagnostic(
                    repository,
                    registry,
                    target,
                    tracked,
                ),
                "ARCHIVE-REPLACEMENT-NONCURRENT",
            )
            self.assertEqual(
                archive_cutover._replacement_target_diagnostic(
                    repository,
                    registry,
                    target,
                    {target: "f" * 40},
                ),
                "ARCHIVE-REPLACEMENT-NONCURRENT",
            )

    def test_index_blob_reads_use_bounded_sanitized_git(self) -> None:
        object_id = "a" * 40
        payload = b"index blob"
        calls = []

        def fake_git(argv, **kwargs):
            calls.append((tuple(argv), dict(kwargs)))
            stdout = (
                f"{len(payload)}\n".encode("ascii") if argv[-2] == "-s" else payload
            )
            return subprocess.CompletedProcess(argv, 0, stdout, b"")

        hostile = {
            "GIT_CONFIG_GLOBAL": "sentinel-global",
            "GIT_OBJECT_DIRECTORY": "sentinel-object",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "sentinel-alternate",
            "GIT_TERMINAL_PROMPT": "1",
        }
        with (
            patch.dict(os.environ, hostile, clear=False),
            patch.object(archive_cutover.subprocess, "run", side_effect=fake_git),
        ):
            self.assertEqual(
                archive_cutover._index_blob_bytes(ROOT, object_id), payload
            )

        self.assertEqual(
            [call[0][-3:] for call in calls],
            [("cat-file", "-s", object_id), ("cat-file", "blob", object_id)],
        )
        for _argv, kwargs in calls:
            environment = kwargs["env"]
            self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
            self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)
            self.assertEqual(kwargs["timeout"], archive_cutover.SECRET_TIMEOUT_SECONDS)
            self.assertNotIn("GIT_OBJECT_DIRECTORY", environment)
            self.assertNotIn("GIT_ALTERNATE_OBJECT_DIRECTORIES", environment)
            self.assertEqual(environment["GIT_CONFIG_GLOBAL"], os.devnull)
            self.assertEqual(environment["GIT_CONFIG_SYSTEM"], os.devnull)
            self.assertEqual(environment["GIT_GRAFT_FILE"], os.devnull)
            self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
            self.assertEqual(environment["GIT_NO_REPLACE_OBJECTS"], "1")
            self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")

    def test_index_blob_read_errors_and_bounds_are_stable(self) -> None:
        object_id = "a" * 40
        failures = (
            FileNotFoundError("sentinel-startup"),
            subprocess.TimeoutExpired(("git",), 10, stderr=b"sentinel-timeout"),
        )
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                with patch.object(
                    archive_cutover.subprocess,
                    "run",
                    side_effect=failure,
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "^replacement target blob is unavailable$"
                    ):
                        archive_cutover._index_blob_bytes(ROOT, object_id)

        oversized = subprocess.CompletedProcess(
            ("git",),
            0,
            f"{archive_cutover.MAX_REPLACEMENT_BLOB_BYTES + 1}\n".encode("ascii"),
            b"",
        )
        with patch.object(archive_cutover.subprocess, "run", return_value=oversized):
            with self.assertRaisesRegex(
                RuntimeError, "^replacement target blob is unavailable$"
            ):
                archive_cutover._index_blob_bytes(ROOT, object_id)

        wrong_length = (
            subprocess.CompletedProcess(("git",), 0, b"2\n", b""),
            subprocess.CompletedProcess(("git",), 0, b"x", b""),
        )
        with patch.object(
            archive_cutover.subprocess,
            "run",
            side_effect=wrong_length,
        ):
            with self.assertRaisesRegex(
                RuntimeError, "^replacement target blob is unavailable$"
            ):
                archive_cutover._index_blob_bytes(ROOT, object_id)

    def test_index_rejects_archive_row_after_prose(self) -> None:
        text = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")
        lines, rows = self._manifest_rows(text)
        mutated = "".join(lines) + "\nPost-manifest note.\n" + lines[rows[0]]

        _parsed, structure_failure = archive_cutover._parse_archive_index(mutated)

        self.assertTrue(structure_failure)

    def test_index_rejects_archive_row_after_table_break(self) -> None:
        text = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")
        lines, rows = self._manifest_rows(text)
        lines.insert(rows[-1] + 1, "\n" + lines[rows[0]])

        _parsed, structure_failure = archive_cutover._parse_archive_index(
            "".join(lines)
        )

        self.assertTrue(structure_failure)

    def test_index_rejects_second_markdown_table(self) -> None:
        text = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")
        mutated = text + "\n| Extra | Value |\n| --- | --- |\n| duplicate | row |\n"

        _parsed, structure_failure = archive_cutover._parse_archive_index(mutated)

        self.assertTrue(structure_failure)

    def test_git_calls_use_recovery_grade_sanitized_environment(self) -> None:
        hostile = {
            "GIT_CONFIG_GLOBAL": "sentinel-global",
            "GIT_OBJECT_DIRECTORY": "sentinel-object",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "sentinel-alternate",
            "GIT_TERMINAL_PROMPT": "1",
        }
        calls = []
        finite_payload = (
            b"---\ntype: content/archive-tombstone\nstatus: archived\n---\n"
        )

        def fake_git(argv, **kwargs):
            calls.append((tuple(argv), dict(kwargs)))
            stdout = b"docs/README.md\0" if "ls-files" in argv else finite_payload
            return subprocess.CompletedProcess(argv, 0, stdout, b"")

        archive_cutover._finite_cutover_base_diagnostics.cache_clear()
        try:
            with (
                patch.dict(os.environ, hostile, clear=False),
                patch.object(archive_cutover.subprocess, "run", side_effect=fake_git),
            ):
                self.assertEqual(archive_cutover._git_paths(ROOT), ("docs/README.md",))
                self.assertEqual(
                    archive_cutover._finite_cutover_base_diagnostics(ROOT), ()
                )
        finally:
            archive_cutover._finite_cutover_base_diagnostics.cache_clear()

        self.assertEqual(len(calls), 32)
        for argv, kwargs in calls:
            environment = kwargs["env"]
            self.assertNotIn("GIT_OBJECT_DIRECTORY", environment)
            self.assertNotIn("GIT_ALTERNATE_OBJECT_DIRECTORIES", environment)
            self.assertEqual(environment["GIT_CONFIG_GLOBAL"], os.devnull)
            self.assertEqual(environment["GIT_CONFIG_SYSTEM"], os.devnull)
            self.assertEqual(environment["GIT_GRAFT_FILE"], os.devnull)
            self.assertEqual(environment["GIT_CONFIG_NOSYSTEM"], "1")
            self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
            self.assertEqual(environment["GIT_NO_REPLACE_OBJECTS"], "1")
            self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
            self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")
            self.assertEqual(environment["LC_ALL"], "C")
            self.assertIn("--no-replace-objects", argv)

    def test_inventory_startup_and_timeout_are_stable(self) -> None:
        failures = (
            FileNotFoundError("sentinel-startup"),
            subprocess.TimeoutExpired(("git",), 10, stderr=b"sentinel-timeout"),
        )
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                with patch.object(
                    archive_cutover.subprocess, "run", side_effect=failure
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "^tracked document inventory is unavailable$"
                    ):
                        archive_cutover._git_paths(ROOT)
        failed = subprocess.CompletedProcess(("git",), 1, b"", b"sentinel-git-failure")
        with patch.object(archive_cutover.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(
                RuntimeError, "^tracked document inventory is unavailable$"
            ):
                archive_cutover._git_paths(ROOT)

    def test_missing_root_returns_stable_payload_free_diagnostic(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            return_code = archive_cutover.main(
                ["--root", str(ROOT / "sentinel-missing-root")]
            )

        self.assertEqual(return_code, 1)
        self.assertIn(
            "FAIL ARCHIVE-CUTOVER-INCOMPLETE path=<repository>\n", output.getvalue()
        )
        self.assertIn(
            "FAIL ARCHIVE-ROOT-UNAVAILABLE path=<repository>\n", output.getvalue()
        )
        self.assertNotIn("sentinel", output.getvalue())

    def test_registry_non_object_and_decode_failure_are_stable(self) -> None:
        # The authority now arrives through the projection rather than through a
        # single file read, so the unreadable and not-an-object cases are
        # injected at that seam.
        def payload(value):
            def load(root):
                if isinstance(value, BaseException):
                    raise value
                return value

            return load

        cases = (
            [],
            UnicodeDecodeError("utf-8", b"x", 0, 1, "sentinel-decode"),
        )
        for value in cases:
            with self.subTest(value=type(value).__name__):
                with (
                    patch.object(
                        archive_cutover, "load_internal_payload", new=payload(value)
                    ),
                    patch.object(
                        archive_cutover, "_secret_classifier", return_value=None
                    ),
                ):
                    report = archive_cutover.validate_repository_cutover(ROOT)
                self._assert_named_partial(report, "ARCHIVE-AUTHORITY-INCOMPLETE")
                self.assertNotIn(
                    "sentinel", "\n".join(item.path for item in report.diagnostics)
                )

    def test_registry_declares_archive_source_removal_evidence(self) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        contracts = registry["documentContracts"]
        admission = next(
            item
            for item in contracts["admissionPolicies"]
            if item["id"] == "archive-envelope-only"
        )
        self.assertEqual(
            admission["create"]["evidencePredicateId"],
            "archive-source-removal",
        )
        predicate = next(
            item
            for item in contracts["evidencePredicates"]
            if item["id"] == "archive-source-removal"
        )
        self.assertEqual(predicate["relationship"], "archive-source")
        self.assertEqual(predicate["sameDiff"], "source-removed-and-mirror-created")

    def test_future_archive_creation_requires_mirrored_source_removal(self) -> None:
        registry = load_registry(ROOT)
        source_path = PurePosixPath("docs/03.specs/900-example/spec.md")
        archive_path = PurePosixPath("docs/98.archive/03.specs/900-example/spec.md")
        source = LifecycleDocument(source_path, "sdlc/spec", "done")
        archive = LifecycleDocument(
            archive_path,
            "content/archive",
            "archived",
            original_path=source_path,
        )
        proposed_archive = {
            archive_path: archive,
        }
        evidence = LifecycleEvidenceContext(
            base_documents={source_path: source},
            proposed_documents={},
            changed_paths=frozenset({source_path, archive_path}),
            status_changed_paths=frozenset(),
            body_changed_paths=frozenset(),
            created_paths=frozenset({archive_path}),
        )
        accepted = compare_lifecycle(
            registry,
            {source_path: source},
            proposed_archive,
            base_mode="staged",
            evidence_context=evidence,
        )
        self.assertEqual(accepted, ())

        missing_source = compare_lifecycle(
            registry,
            {},
            proposed_archive,
            base_mode="staged",
            evidence_context=replace(evidence, base_documents={}),
        )
        self.assertIn(
            "LIFECYCLE-EVIDENCE",
            {diagnostic.rule_id for diagnostic in missing_source},
        )

        retained_source = compare_lifecycle(
            registry,
            {source_path: source},
            {source_path: source, archive_path: archive},
            base_mode="staged",
            evidence_context=replace(
                evidence,
                proposed_documents={},
                created_paths=frozenset({archive_path}),
            ),
        )
        self.assertIn(
            "LIFECYCLE-EVIDENCE",
            {diagnostic.rule_id for diagnostic in retained_source},
        )

    def test_partial_finite_cutover_base_is_rejected(self) -> None:
        diagnostic = archive_cutover.CutoverDiagnostic(
            code="ARCHIVE-FINITE-ADMISSION",
            path=archive_cutover.EXPECTED_ARCHIVE_PATHS[0],
        )
        with patch.object(
            archive_cutover,
            "_finite_cutover_base_diagnostics",
            return_value=(diagnostic,),
        ):
            report = self._validate_without_repeating_secret_classification()
        self._assert_named_partial(report, "ARCHIVE-FINITE-ADMISSION")

    def test_partial_stale_role_is_rejected(self) -> None:
        with patch.object(
            archive_cutover,
            "STALE_CONTRACT_SURFACES",
            ("docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",),
        ):
            report = self._validate_without_repeating_secret_classification()
        self._assert_named_partial(report, "ARCHIVE-RETIRED-AUTHORITY")

    def test_partial_direct_current_link_is_rejected(self) -> None:
        current_report = ArchiveValidationReport(
            diagnostics=(
                ArchiveDiagnostic(
                    code="ARCHIVE-CURRENT-DIRECT-LINK",
                    path="docs/current-probe.md",
                ),
            ),
        )
        with patch.object(
            archive_cutover,
            "validate_current_archive_authority",
            return_value=current_report,
        ):
            report = self._validate_without_repeating_secret_classification()
        self._assert_named_partial(report, "ARCHIVE-CURRENT-DIRECT-LINK")

    def test_partial_duplicate_original_owner_is_rejected(self) -> None:
        stable_by_legacy = {
            str(row["legacy_path"]): str(row["stable_path"])
            for row in archive_recovery.build_work107_migration_rows(ROOT)
        }
        first_legacy, second_legacy = archive_cutover.EXPECTED_ARCHIVE_PATHS[:2]
        first_path = stable_by_legacy[first_legacy]
        second_path = stable_by_legacy[second_legacy]
        first_bytes = (ROOT / first_path).read_bytes()
        duplicate_original = parse_archive_envelope(
            (ROOT / second_path).read_bytes()
        ).metadata["original_path"]
        original_parse = archive_cutover.parse_archive_envelope

        def duplicate_first(content: bytes):
            parsed = original_parse(content)
            if content == first_bytes:
                metadata = dict(parsed.metadata)
                metadata["original_path"] = duplicate_original
                return replace(parsed, metadata=metadata)
            return parsed

        with patch.object(
            archive_cutover,
            "parse_archive_envelope",
            side_effect=duplicate_first,
        ):
            report = self._validate_without_repeating_secret_classification()
        self._assert_named_partial(report, "ARCHIVE-ORIGINAL-OWNER-DUPLICATE")

    def test_partial_missing_replacement_is_rejected(self) -> None:
        stable_by_legacy = {
            str(row["legacy_path"]): str(row["stable_path"])
            for row in archive_recovery.build_work107_migration_rows(ROOT)
        }
        first_path = stable_by_legacy[archive_cutover.EXPECTED_ARCHIVE_PATHS[0]]
        first_bytes = (ROOT / first_path).read_bytes()
        original_parse = archive_cutover.parse_archive_envelope

        def remove_first_replacement(content: bytes):
            parsed = original_parse(content)
            if content == first_bytes:
                metadata = dict(parsed.metadata)
                metadata["replacement"] = None
                return replace(parsed, metadata=metadata)
            return parsed

        with patch.object(
            archive_cutover,
            "parse_archive_envelope",
            side_effect=remove_first_replacement,
        ):
            report = self._validate_without_repeating_secret_classification()
        self._assert_named_partial(report, "ARCHIVE-REPLACEMENT-MISSING")

    def test_wdtc_source_commit_cannot_self_validate(self) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        wdtc_path = registry["archiveNamespaces"][2]["records"][0]
        record_bytes = (ROOT / wdtc_path).read_bytes()
        original_parse = archive_cutover.parse_archive_envelope

        def drift_wdtc_commit(content: bytes):
            parsed = original_parse(content)
            if content == record_bytes:
                metadata = dict(parsed.metadata)
                metadata["source_commit"] = archive_cutover.FIRST_SOURCE_COMMIT
                return replace(parsed, metadata=metadata)
            return parsed

        with patch.object(
            archive_cutover,
            "parse_archive_envelope",
            side_effect=drift_wdtc_commit,
        ):
            report = self._validate_without_repeating_secret_classification()

        self._assert_named_partial(report, "ARCHIVE-SOURCE-OWNERSHIP")


if __name__ == "__main__":
    unittest.main()
