"""Current Archive integrity checks, independent of the completed cutover."""

from __future__ import annotations

from contextlib import nullcontext
import subprocess
import tempfile
import unittest
import os
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from scripts import archive_validation
from scripts.archive_recovery import ArchiveContractError
from scripts.archive_validation import ArchiveRecord


class ArchivePayloadSecretScanTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="archive-integrity-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / ".gitleaks.toml").write_text("title = 'fixture'\n")
        self.records = (
            ArchiveRecord("docs/98.archive/completed/fixture.md", b"envelope"),
        )

    def scan(
        self,
        returncode: int | None,
        *,
        executable: str | None = "/usr/bin/gitleaks",
        preserve_override: bool = False,
    ):
        result = subprocess.CompletedProcess([executable or "gitleaks"], returncode)
        hint = (
            nullcontext()
            if preserve_override
            else mock.patch.dict(
                os.environ, {"HY_HOME_K8S_GITLEAKS_EXECUTABLE": executable or ""}
            )
        )
        with (
            hint,
            mock.patch.object(
                archive_validation,
                "parse_archive_envelope",
                return_value=SimpleNamespace(payload=b"safe fixture\n"),
            ),
            mock.patch.object(
                archive_validation, "_trusted_gitleaks", return_value=executable
            ),
            mock.patch.object(
                archive_validation.subprocess, "run", return_value=result
            ) as run,
        ):
            diagnostics = archive_validation._scan_archive_payloads(
                self.root, self.records
            )
        return diagnostics, run

    def test_clean_payload_uses_stdin_and_hides_classifier_output(self) -> None:
        diagnostics, run = self.scan(0)
        self.assertEqual(diagnostics, ())
        args, kwargs = run.call_args
        self.assertEqual(args[0][1], "stdin")
        self.assertEqual(kwargs["input"], b"safe fixture\n")
        self.assertEqual(kwargs["stdout"], subprocess.DEVNULL)
        self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)
        self.assertLessEqual(kwargs["timeout"], 20)

    def test_detected_secret_fails_with_only_rule_and_path(self) -> None:
        diagnostics, _ = self.scan(17)
        self.assertEqual(
            [(item.code, item.path) for item in diagnostics],
            [("ARCHIVE-SECRET-DETECTED", "docs/98.archive/README.md")],
        )

    def test_missing_classifier_and_unexpected_exit_fail_closed(self) -> None:
        missing, run = self.scan(None, executable=None)
        self.assertFalse(run.called)
        self.assertEqual(missing[0].code, "ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE")
        failed, _ = self.scan(2)
        self.assertEqual(failed[0].code, "ARCHIVE-SECRET-CLASSIFIER-ERROR")

    def test_aggregate_payload_budget_fails_before_subprocess(self) -> None:
        with (
            mock.patch.object(
                archive_validation,
                "parse_archive_envelope",
                return_value=SimpleNamespace(payload=b"x" * (32 * 1024 * 1024 + 1)),
            ),
            mock.patch.object(archive_validation.subprocess, "run") as run,
        ):
            diagnostics = archive_validation._scan_archive_payloads(
                self.root, self.records
            )
        self.assertEqual(diagnostics[0].code, "ARCHIVE-SECRET-RESOURCE-LIMIT")
        run.assert_not_called()

    def test_missing_config_fails_before_classifying(self) -> None:
        (self.root / ".gitleaks.toml").unlink()
        diagnostics, run = self.scan(0)
        self.assertEqual(diagnostics[0].code, "ARCHIVE-SECRET-CLASSIFIER-ERROR")
        run.assert_not_called()

    def test_invalid_override_cannot_fall_back_to_path(self) -> None:
        with mock.patch.dict(
            archive_validation.os.environ,
            {"HY_HOME_K8S_GITLEAKS_EXECUTABLE": "/absent/gitleaks"},
        ):
            diagnostics, run = self.scan(0, preserve_override=True)
        self.assertEqual(diagnostics[0].code, "ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE")
        run.assert_not_called()

    def test_timeout_fails_closed_without_payload_output(self) -> None:
        with (
            mock.patch.dict(
                os.environ, {"HY_HOME_K8S_GITLEAKS_EXECUTABLE": "/usr/bin/gitleaks"}
            ),
            mock.patch.object(
                archive_validation,
                "parse_archive_envelope",
                return_value=SimpleNamespace(payload=b"safe fixture\n"),
            ),
            mock.patch.object(
                archive_validation,
                "_trusted_gitleaks",
                return_value="/usr/bin/gitleaks",
            ),
            mock.patch.object(
                archive_validation.subprocess,
                "run",
                side_effect=subprocess.TimeoutExpired("gitleaks", 20),
            ),
        ):
            diagnostics = archive_validation._scan_archive_payloads(
                self.root, self.records
            )
        self.assertEqual(diagnostics[0].code, "ARCHIVE-SECRET-CLASSIFIER-ERROR")

    def test_empty_or_malformed_records_do_not_claim_a_scan(self) -> None:
        with mock.patch.object(archive_validation.subprocess, "run") as run:
            self.assertEqual(
                archive_validation._scan_archive_payloads(self.root, ()), ()
            )
            run.assert_not_called()
        with (
            mock.patch.object(
                archive_validation,
                "parse_archive_envelope",
                side_effect=ArchiveContractError("ARCHIVE-ENVELOPE-INVALID", "fixture"),
            ),
            mock.patch.object(archive_validation.subprocess, "run") as run,
        ):
            self.assertEqual(
                archive_validation._scan_archive_payloads(self.root, self.records), ()
            )
            run.assert_not_called()

    def test_executable_override_under_tmp_is_refused_before_payload_transfer(
        self,
    ) -> None:
        fake = self.root / "gitleaks"
        fake.write_text("#!/bin/sh\nexit 0\n")
        fake.chmod(0o755)
        with (
            mock.patch.dict(
                os.environ,
                {"HY_HOME_K8S_GITLEAKS_EXECUTABLE": str(fake), "PATH": str(self.root)},
            ),
            mock.patch.object(
                archive_validation,
                "parse_archive_envelope",
                return_value=SimpleNamespace(payload=b"sensitive synthetic fixture"),
            ),
            mock.patch.object(archive_validation.subprocess, "run") as run,
        ):
            diagnostics = archive_validation._scan_archive_payloads(
                self.root, self.records
            )
        self.assertEqual(diagnostics[0].code, "ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE")
        run.assert_not_called()

    def test_missing_registry_blocks_current_catalog_guarantee(self) -> None:
        with (
            mock.patch.object(
                archive_validation,
                "_repository_archive_records",
                return_value=(
                    {"docs/98.archive/completed/fixture.md": b"invalid"},
                    [],
                    None,
                ),
            ),
            mock.patch.object(
                archive_validation, "_work107_stable_rows", return_value={}
            ),
            mock.patch.object(
                archive_validation, "_read_repository_index", return_value="# Archive\n"
            ),
            mock.patch.object(
                archive_validation, "repository_registry", return_value=None
            ),
        ):
            report = archive_validation.validate_repository_archive(self.root, {})
        self.assertIn(
            "ARCHIVE-REGISTRY-UNAVAILABLE",
            {item.code for item in report.diagnostics},
        )


if __name__ == "__main__":
    unittest.main()
