#!/usr/bin/env python3
"""Unit tests for the provider runtime/config evidence contract."""

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
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-agent-provider-config.py"
AGGREGATE_PATH = (
    REPOSITORY_ROOT / "scripts/validate-agent-provider-evidence.py"
)
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
        "validate_agent_provider_config", SCRIPT_PATH
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


class ProviderConfigContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def contract_copy(self):
        return copy.deepcopy(self.contract)

    def test_validator_exposes_import_safe_contract_api(self) -> None:
        self.assertTrue(
            hasattr(self.validator, "validate_contract"),
            "validator must expose validate_contract without exiting on import",
        )
        self.assertTrue(
            hasattr(self.validator, "ProviderConfigError"),
            "validator must expose typed rule failures",
        )

    def assert_rule(self, contract, expected_rule: str) -> None:
        with self.assertRaises(self.validator.ProviderConfigError) as raised:
            self.validator.validate_contract(
                REPOSITORY_ROOT, contract, check_paths=True
            )
        self.assertEqual(raised.exception.code, expected_rule)

    def test_production_contract_is_closed_and_cutoff_bounded(self) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(counts["providers"], 4)
        self.assertEqual(counts["sources"], 10)
        self.assertEqual(counts["modelCandidates"], 8)
        self.assertEqual(counts["mcpServers"], 7)
        self.assertEqual(
            self.contract["cutoff"]["utc"], "2026-07-10T01:00:00Z"
        )
        self.assertEqual(self.contract["contractVersion"], "1.0.0")

    def test_provider_order_and_local_observations_are_exact(self) -> None:
        providers = self.contract["providers"]
        self.assertEqual(
            [provider["id"] for provider in providers],
            ["local", "claude", "codex", "gemini"],
        )
        observed = {
            provider["id"]: provider["localObservation"]
            for provider in providers
        }
        self.assertEqual(
            observed["claude"]["version"], "2.1.220 (Claude Code)"
        )
        self.assertEqual(observed["claude"]["observedAt"], "2026-07-28")
        self.assertEqual(observed["claude"]["installation"], "present")
        self.assertEqual(observed["codex"]["version"], "codex-cli 0.140.0")
        self.assertEqual(observed["codex"]["installation"], "present")
        self.assertEqual(observed["gemini"]["installation"], "absent")
        self.assertTrue(
            all(item["readinessClaim"] is False for item in observed.values())
        )
        self.assertTrue(
            all(item["userReported"] is False for item in observed.values())
        )
        prior = self.contract["observationHistory"][0]
        self.assertEqual(prior["observationClass"], "prior-user-report")
        self.assertEqual(
            prior["providers"]["codex"]["version"],
            "codex-cli 0.145.0-alpha.27",
        )
        self.assertEqual(prior["providers"]["claude"]["installation"], "absent")
        self.assertEqual(prior["providers"]["gemini"]["installation"], "absent")

    def test_surface_paths_match_harness_without_relabeling_local_as_gemini(
        self,
    ) -> None:
        harness = json.loads(
            (
                REPOSITORY_ROOT
                / "docs/00.agent-governance/contracts/harness-contract.json"
            ).read_text(encoding="utf-8")
        )
        expected = {
            surface["id"]: (
                surface["pathRoot"],
                surface["admissionState"],
            )
            for surface in harness["surfaces"]
        }
        actual = {
            provider["id"]: (
                provider["trackedSurface"]["pathRoot"],
                provider["trackedSurface"]["state"],
            )
            for provider in self.contract["providers"]
        }
        self.assertEqual(actual, expected)
        self.assertEqual(actual["local"][0], ".agents/agents")
        self.assertEqual(actual["gemini"], (".gemini/agents", "current"))

    def test_sources_have_dates_cutoff_classification_and_primary_claims(
        self,
    ) -> None:
        ledger = self.contract["sourceLedger"]
        self.assertEqual(
            tuple(source["id"] for source in ledger),
            self.validator.SOURCE_IDS,
        )
        self.assertEqual(
            set(source["provider"] for source in ledger),
            {"claude", "codex", "gemini", "agency-agents"},
        )
        self.assertTrue(
            {
                "claude-code-changelog-2-1-154",
                "codex-release-0-145-0-alpha-2",
                "gemini-cli-release-0-51-preview-0",
            }.issubset({source["id"] for source in ledger})
        )
        for source in ledger:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertIn(source["publisher"], {"Anthropic", "OpenAI", "Google", "GitHub"})
            self.assertRegex(source["sourceDate"], r"^2026-\d{2}-\d{2}$")
            if source["publishedAtUtc"] is not None:
                self.assertRegex(
                    source["publishedAtUtc"],
                    r"^2026-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
                )
            self.assertIn(
                source["cutoffApplicability"],
                {"cutoff-applicable", "current-only"},
            )
            self.assertIn(
                source["confidence"], {"dated-primary", "current-primary"}
            )
            self.assertTrue(source["claim"])
        exact_cutoff_source = next(
            source
            for source in ledger
            if source["id"] == "codex-release-0-145-0-alpha-2"
        )
        self.assertEqual(
            exact_cutoff_source["publishedAtUtc"],
            "2026-07-10T00:09:39Z",
        )

    def test_model_candidates_are_unpromoted_and_gate_exact_resolution(
        self,
    ) -> None:
        for provider in self.contract["providers"]:
            self.assertEqual(len(provider["modelCandidates"]), 2)
            for candidate in provider["modelCandidates"]:
                self.assertEqual(candidate["promotionState"], "candidate-only")
                self.assertIn("configuredId", candidate)
                self.assertIn("observedId", candidate)
                self.assertFalse(
                    candidate["fallback"]["silentFallbackAllowed"]
                )
                self.assertEqual(
                    set(candidate["gates"]),
                    {"configParse", "runtimeResolution", "spec044Fitness"},
                )

    def test_mcp_inventory_has_closed_ownership_and_trust_boundaries(self) -> None:
        inventory = self.contract["mcpInventory"]
        self.assertEqual(len(inventory), 7)
        self.assertEqual(
            {server["id"] for server in inventory},
            {
                "context7",
                "exa",
                "github",
                "memory",
                "playwright",
                "sequential-thinking",
                "supabase",
            },
        )
        for server in inventory:
            self.assertTrue(server["owner"])
            self.assertTrue(server["purpose"])
            self.assertTrue(server["transport"])
            self.assertTrue(server["trustBoundary"])
            self.assertTrue(server["allowedRoles"])
            self.assertIn(
                server["credentialClass"],
                {"none", "environment-reference", "provider-managed-auth"},
            )

    def test_duplicate_json_keys_fail_at_the_input_boundary(self) -> None:
        with self.assertRaises(self.validator.ProviderConfigError) as raised:
            self.validator.decode_json_text(
                '{"provider":{"id":"claude","id":"codex"}}',
                "<unit-fixture>",
            )
        self.assertEqual(raised.exception.code, "PNME-DUPLICATE-KEY")
        self.assertEqual(raised.exception.exit_code, 2)

    def test_all_config_fixture_mutations_fail_with_declared_rule(self) -> None:
        for case in self.fixture["configMutations"]:
            with self.subTest(case=case["name"]):
                mutated = self.contract_copy()
                self.validator.apply_mutation(mutated, case["name"])
                self.assert_rule(mutated, case["expectedRule"])

    def test_self_test_cli_runs_real_contract_and_mutations(self) -> None:
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
            "[PASS] agent provider config self-test passed", result.stdout
        )

    def test_provider_evidence_self_test_propagates_explicit_root_from_foreign_cwd(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="provider-evidence-root-"
        ) as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(AGGREGATE_PATH),
                    "--root",
                    str(REPOSITORY_ROOT),
                    "--self-test",
                ],
                cwd=directory,
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "[PASS] agent provider evidence aggregate passed: "
            "mode=self-test validators=2",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
