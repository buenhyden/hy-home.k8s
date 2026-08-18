#!/usr/bin/env python3
"""Unit tests for redacted, non-transitive provider canary records."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-agent-provider-canaries.py"
CONTRACT_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/provider-runtime-evidence.json"
)
FIXTURE_PATH = (
    REPOSITORY_ROOT
    / "tests/fixtures/agent-provider-runtime-evidence.json"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_provider_canaries", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    original_argv = sys.argv[:]
    sys.argv = [str(SCRIPT_PATH)]
    try:
        try:
            spec.loader.exec_module(module)
        except SystemExit:
            # A compatibility wrapper may still execute on import. The API
            # test below turns that incomplete behavior into an explicit RED.
            pass
    finally:
        sys.argv = original_argv
    return module


class ProviderCanaryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def contract_copy(self):
        return copy.deepcopy(self.contract)

    def test_validator_exposes_import_safe_canary_api(self) -> None:
        self.assertTrue(
            hasattr(self.validator, "validate_canaries"),
            "validator must expose validate_canaries without exiting on import",
        )
        self.assertTrue(
            hasattr(self.validator, "ProviderCanaryError"),
            "validator must expose typed rule failures",
        )

    def assert_rule(self, contract, expected_rule: str) -> None:
        with self.assertRaises(self.validator.ProviderCanaryError) as raised:
            self.validator.validate_canaries(REPOSITORY_ROOT, contract)
        self.assertEqual(raised.exception.code, expected_rule)

    def test_production_canaries_cover_every_provider_and_lane(self) -> None:
        counts = self.validator.validate_canaries(REPOSITORY_ROOT)
        self.assertEqual(counts["records"], 12)
        self.assertEqual(counts["providers"], 4)
        expected = {
            (provider, lane)
            for provider in ("local", "claude", "codex", "gemini")
            for lane in (
                "repo-static",
                "native-discovery",
                "authenticated-run",
            )
        }
        actual = {
            (record["providerId"], record["evidenceClass"])
            for record in self.contract["canaryRecords"]
        }
        self.assertEqual(actual, expected)

    def test_non_pass_records_have_owner_limitation_and_retry_trigger(
        self,
    ) -> None:
        for record in self.contract["canaryRecords"]:
            if record["verdict"] != "PASS":
                self.assertTrue(record["owner"])
                self.assertTrue(record["limitation"])
                self.assertTrue(record["retryTrigger"])

    def test_records_are_synthetic_no_mutation_and_redacted(self) -> None:
        for record in self.contract["canaryRecords"]:
            self.assertTrue(record["synthetic"])
            self.assertEqual(record["mutationMode"], "no-mutation")
            self.assertFalse(record["crossLanePromotion"])
            self.assertEqual(record["redaction"]["status"], "PASS")
            self.assertFalse(record["redaction"]["rawPromptStored"])
            self.assertFalse(record["redaction"]["providerBodyStored"])
            self.assertFalse(record["redaction"]["credentialsStored"])
            self.assertFalse(record["redaction"]["authPathsStored"])

    def test_canary_verdicts_match_provider_evidence_lanes(self) -> None:
        lanes = {
            (provider["id"], lane["id"]): lane["verdict"]
            for provider in self.contract["providers"]
            for lane in provider["evidenceLanes"]
        }
        records = {
            (record["providerId"], record["evidenceClass"]): record["verdict"]
            for record in self.contract["canaryRecords"]
        }
        self.assertEqual(records, lanes)

    def test_absent_runtime_native_pass_fails_closed(self) -> None:
        mutated = self.contract_copy()
        self.validator.apply_mutation(mutated, "absent-runtime-native-pass")
        self.assert_rule(mutated, "PNME-UNSUPPORTED-RUNTIME")

    def test_all_canary_fixture_mutations_fail_with_declared_rule(self) -> None:
        for case in self.fixture["canaryMutations"]:
            with self.subTest(case=case["name"]):
                mutated = self.contract_copy()
                self.validator.apply_mutation(mutated, case["name"])
                self.assert_rule(mutated, case["expectedRule"])

    def test_self_test_cli_runs_real_records_and_mutations(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(REPOSITORY_ROOT),
                "--self-test",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "[PASS] agent provider canary self-test passed", result.stdout
        )

    def test_standalone_canary_preserves_a_symlink_root(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="provider-canary-symlink-"
        ) as directory:
            link = Path(directory) / "repository-link"
            link.symlink_to(REPOSITORY_ROOT, target_is_directory=True)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--root",
                    str(link),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("PNME-INPUT:", result.stderr)
        self.assertNotIn(str(REPOSITORY_ROOT), result.stderr)

    def test_standalone_canary_preserves_a_lexical_parent_escape(self) -> None:
        lexical_root = REPOSITORY_ROOT / "docs" / ".."
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(lexical_root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("PNME-INPUT:", result.stderr)


if __name__ == "__main__":
    unittest.main()
