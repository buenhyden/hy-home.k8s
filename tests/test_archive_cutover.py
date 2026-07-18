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
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from scripts import archive_cutover  # noqa: E402
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
            "PASS archive cutover records=35 historical_links=233 secret_clean=35\n",
        )
        self.assertEqual(completed.stderr, "")

    def test_finite_base_proof_remains_exact_inside_the_aggregate(self) -> None:
        text = (ROOT / archive_cutover.ARCHIVE_INDEX).read_text(encoding="utf-8")

        rows, structure_failure = archive_cutover._parse_archive_index(text)
        base_rows = {
            path: rows[path]
            for path in archive_cutover.EXPECTED_ARCHIVE_PATHS
            if path in rows
        }

        self.assertFalse(structure_failure)
        self.assertEqual(len(base_rows), 31)
        self.assertEqual(
            sum(row.historical_links for row in base_rows.values()),
            archive_cutover.EXPECTED_HISTORICAL_LINKS,
        )
        self.assertEqual(archive_cutover.EXPECTED_HISTORICAL_LINKS, 202)
        self.assertEqual(len(rows), 35)
        self.assertEqual(sum(row.historical_links for row in rows.values()), 233)

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
                return text.replace(
                    "<!-- archive-manifest:v1 records=35 historical-links=233 -->",
                    "",
                )
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
        registry_path = (
            ROOT / "docs/99.templates/support/document-profiles.json"
        ).resolve()
        original_read_text = Path.read_text

        def registry_text(value):
            def read(path: Path, *args, **kwargs):
                if path.resolve() == registry_path:
                    if isinstance(value, BaseException):
                        raise value
                    return value
                return original_read_text(path, *args, **kwargs)

            return read

        cases = (
            "[]",
            UnicodeDecodeError("utf-8", b"x", 0, 1, "sentinel-decode"),
        )
        for value in cases:
            with self.subTest(value=type(value).__name__):
                with (
                    patch.object(Path, "read_text", new=registry_text(value)),
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
            ("docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",),
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
        first_path, second_path = archive_cutover.EXPECTED_ARCHIVE_PATHS[:2]
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
        first_path = archive_cutover.EXPECTED_ARCHIVE_PATHS[0]
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


if __name__ == "__main__":
    unittest.main()
