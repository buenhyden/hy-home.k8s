#!/usr/bin/env python3
"""Focused tests for the Spec 044 model-fitness contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-agent-model-fitness.py"
CONTRACT_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-model-fitness.json"
)
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-model-fitness.schema.json"
)
FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/agent-model-fitness.json"
PROVIDER_EVIDENCE_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/provider-runtime-evidence.json"
)
HARNESS_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/harness-contract.json"
)
GOVERNED_INPUTS = (
    CONTRACT_PATH,
    SCHEMA_PATH,
    FIXTURE_PATH,
    PROVIDER_EVIDENCE_PATH,
    HARNESS_PATH,
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_model_fitness", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    scripts_path = str(SCRIPT_PATH.parent)
    sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts_path)
    return module


def assert_all_objects_closed(test: unittest.TestCase, node, path="<root>"):
    if isinstance(node, dict):
        if node.get("type") == "object":
            test.assertIs(
                node.get("additionalProperties"),
                False,
                f"open object schema at {path}",
            )
        for key, value in node.items():
            assert_all_objects_closed(test, value, f"{path}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_all_objects_closed(test, value, f"{path}/{index}")


def copy_governed_inputs(root: Path) -> None:
    for source in GOVERNED_INPUTS:
        destination = root / source.relative_to(REPOSITORY_ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


class ModelFitnessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def contract_copy(self):
        return copy.deepcopy(self.contract)

    def assert_rule(self, contract, expected_rule: str) -> None:
        with self.assertRaises(self.validator.ModelFitnessError) as raised:
            self.validator.validate_contract(REPOSITORY_ROOT, contract)
        self.assertEqual(raised.exception.code, expected_rule)

    def test_validator_is_import_safe_and_exposes_typed_api(self) -> None:
        self.assertTrue(hasattr(self.validator, "validate_contract"))
        self.assertTrue(hasattr(self.validator, "ModelFitnessError"))
        self.assertTrue(hasattr(self.validator, "parse_json_text"))
        self.assertTrue(hasattr(self.validator, "run_self_test"))

    def test_schema_is_draft_2020_12_and_fully_closed(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        Draft202012Validator.check_schema(schema)
        assert_all_objects_closed(self, schema)

    def test_production_contract_is_pre_area004_and_exact_12_by_4(self) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(
            counts,
            {
                "roles": 12,
                "providers": 4,
                "tuples": 48,
                "pending": 48,
                "deferred": 48,
            },
        )
        self.assertEqual(self.contract["contractMode"], "contract-only")
        self.assertEqual(self.contract["evidenceClass"], "repo-static")
        self.assertEqual(self.contract["lifecycleState"], "pre-area004")
        for profile in self.contract["roleProfiles"]:
            for item in profile["providerTuples"]:
                self.assertEqual(item["state"], "pending")
                self.assertEqual(item["promotionState"], "candidate-only")
                self.assertEqual(item["decision"], "DEFER")
                self.assertEqual(item["canary"]["verdict"], "DEFER")
                self.assertEqual(item["sameSuiteBaseline"]["verdict"], "DEFER")
                self.assertTrue(
                    all(value == "DEFER" for value in item["runtime"].values())
                )

    def test_fixed_cutoff_is_cross_checked_against_spec042_authority(self) -> None:
        provider_evidence = json.loads(
            PROVIDER_EVIDENCE_PATH.read_text(encoding="utf-8")
        )
        cutoff = self.contract["authoritativeCutoff"]
        self.assertEqual(
            cutoff["authorityRef"],
            "docs/00.agent-governance/contracts/provider-runtime-evidence.json#/cutoff",
        )
        self.assertEqual(
            cutoff["localTime"], "2026-07-10T10:00:00+09:00"
        )
        self.assertEqual(cutoff["utc"], "2026-07-10T01:00:00Z")
        self.assertEqual(cutoff["localTime"], provider_evidence["cutoff"]["localTime"])
        self.assertEqual(cutoff["utc"], provider_evidence["cutoff"]["utc"])
        self.assertEqual(
            self.contract["authorityBoundaries"]["harnessObservationUse"],
            "repository-observation-only",
        )
        self.assertFalse(
            self.contract["authorityBoundaries"][
                "harnessProviderModelAuthority"
            ]
        )

    def test_authoritative_cutoff_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in (
                CONTRACT_PATH,
                SCHEMA_PATH,
                PROVIDER_EVIDENCE_PATH,
                HARNESS_PATH,
            ):
                destination = root / source.relative_to(REPOSITORY_ROOT)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            evidence_path = root / PROVIDER_EVIDENCE_PATH.relative_to(
                REPOSITORY_ROOT
            )
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence["cutoff"]["utc"] = "2026-07-10T01:00:01Z"
            evidence_path.write_text(
                json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
            )
            with self.assertRaises(self.validator.ModelFitnessError) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(
                raised.exception.code, "AREA-FIT-CUTOFF-AUTHORITY"
            )

    def test_governed_inputs_reject_symlinks_without_following_outside_repo(
        self,
    ) -> None:
        for source in GOVERNED_INPUTS:
            with self.subTest(path=source.relative_to(REPOSITORY_ROOT)):
                with tempfile.TemporaryDirectory() as directory:
                    base = Path(directory)
                    root = base / "repository"
                    copy_governed_inputs(root)
                    relative = source.relative_to(REPOSITORY_ROOT)
                    candidate = root / relative
                    outside = base / "outside.json"
                    shutil.copy2(source, outside)
                    candidate.unlink()
                    candidate.symlink_to(outside)
                    with self.assertRaises(
                        self.validator.ModelFitnessError
                    ) as raised:
                        if source == FIXTURE_PATH:
                            self.validator.run_self_test(root)
                        else:
                            self.validator.validate_contract(root)
                    self.assertEqual(
                        raised.exception.code, "AREA-FIT-INPUT"
                    )
                    self.assertNotIn(str(outside), raised.exception.detail)

    def test_intermediate_symlink_cannot_escape_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "repository"
            root.mkdir()
            (root / "tests/fixtures").mkdir(parents=True)
            shutil.copy2(
                FIXTURE_PATH,
                root / FIXTURE_PATH.relative_to(REPOSITORY_ROOT),
            )
            (root / "docs").symlink_to(REPOSITORY_ROOT / "docs")
            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-FIT-INPUT")
            self.assertNotIn(str(REPOSITORY_ROOT), raised.exception.detail)

    def test_non_regular_governed_input_and_non_directory_root_fail_closed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "repository"
            copy_governed_inputs(root)
            harness = root / HARNESS_PATH.relative_to(REPOSITORY_ROOT)
            harness.unlink()
            harness.mkdir()
            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-FIT-INPUT")

            root_file = base / "not-a-directory"
            root_file.write_text("synthetic\n", encoding="utf-8")
            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root_file)
            self.assertEqual(raised.exception.code, "AREA-FIT-INPUT")
            self.assertNotIn(str(root_file), raised.exception.detail)

    def test_symlink_repository_root_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            actual_root = base / "actual-repository"
            copy_governed_inputs(actual_root)
            root_link = base / "repository-link"
            root_link.symlink_to(actual_root)
            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root_link)
            self.assertEqual(raised.exception.code, "AREA-FIT-INPUT")
            self.assertNotIn(str(actual_root), raised.exception.detail)

    def test_cli_symlink_failure_is_stable_and_non_disclosing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "repository"
            copy_governed_inputs(root)
            contract = root / CONTRACT_PATH.relative_to(REPOSITORY_ROOT)
            outside = base / "outside-contract.json"
            shutil.copy2(CONTRACT_PATH, outside)
            contract.unlink()
            contract.symlink_to(outside)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--root",
                    str(root),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("ERR AREA-FIT-INPUT", result.stderr)
            self.assertNotIn(str(outside), result.stderr)

    def test_symlink_contract_input_is_rejected_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in (
                SCHEMA_PATH,
                PROVIDER_EVIDENCE_PATH,
                HARNESS_PATH,
                FIXTURE_PATH,
            ):
                destination = root / source.relative_to(REPOSITORY_ROOT)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            contract_path = root / CONTRACT_PATH.relative_to(REPOSITORY_ROOT)
            contract_path.parent.mkdir(parents=True, exist_ok=True)
            contract_path.symlink_to(CONTRACT_PATH)
            with self.assertRaises(self.validator.ModelFitnessError) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-FIT-INPUT")
            self.assertEqual(raised.exception.exit_code, 2)

    def test_provider_identifier_planes_keep_local_api_and_cli_distinct(self) -> None:
        providers = {
            provider["providerId"]: provider
            for provider in self.contract["providers"]
        }
        self.assertEqual(tuple(providers), ("local", "claude", "codex", "gemini"))
        self.assertEqual(providers["local"]["runtimeInterface"], "repo-static")
        self.assertEqual(
            providers["claude"]["modelIdentifierPlane"],
            "claude-code-cli-alias",
        )
        self.assertEqual(
            providers["codex"]["modelIdentifierPlane"],
            "codex-cli-model-id",
        )
        self.assertEqual(
            providers["gemini"]["modelIdentifierPlane"],
            "gemini-api-id-candidate-for-cli",
        )
        self.assertIn(
            "does-not-prove-cli-resolution",
            providers["gemini"]["apiVsCliBoundary"],
        )

    def test_gemini_candidate_config_sources_are_contract_owned(self) -> None:
        gemini_index = 3
        candidates = self.contract["providers"][gemini_index]["candidateModels"]
        candidate_indexes = {
            candidate["modelId"]: index
            for index, candidate in enumerate(candidates)
        }
        for candidate in candidates:
            self.assertTrue(candidate["candidateOnly"])
            self.assertEqual(candidate["runtimeResolution"], "DEFER")
        for profile in self.contract["roleProfiles"]:
            gemini_tuple = next(
                item
                for item in profile["providerTuples"]
                if item["providerId"] == "gemini"
            )
            candidate_index = candidate_indexes[gemini_tuple["modelCandidate"]]
            self.assertEqual(
                gemini_tuple["configSource"],
                "docs/00.agent-governance/contracts/"
                "agent-model-fitness.json"
                f"#/providers/{gemini_index}/candidateModels/"
                f"{candidate_index}/modelId",
            )

    def test_api_cli_boundary_text_is_closed_for_every_provider(self) -> None:
        for index, provider_id in enumerate(
            ("local", "claude", "codex", "gemini")
        ):
            mutated = self.contract_copy()
            mutated["providers"][index][
                "apiVsCliBoundary"
            ] = "api-and-cli-resolution-are-authoritative"
            with self.subTest(provider=provider_id):
                self.assert_rule(mutated, "AREA-FIT-NAMESPACE")

    def test_evaluation_policy_orders_quality_and_safety_first(self) -> None:
        policy = self.contract["evaluationPolicy"]
        self.assertEqual(
            policy["priorityOrder"], ["quality", "safety", "cost", "latency"]
        )
        self.assertGreater(policy["thresholds"]["qualityMinimum"], 0)
        self.assertEqual(policy["thresholds"]["safetyMinimum"], 1)
        self.assertTrue(policy["sameSuiteRequired"])
        self.assertFalse(policy["fallback"]["silentFallbackAllowed"])
        self.assertEqual(policy["rollback"]["action"], "restore-incumbent")

    def test_duplicate_json_key_is_rejected_with_stable_rule(self) -> None:
        with self.assertRaises(self.validator.ModelFitnessError) as raised:
            self.validator.parse_json_text(
                '{"schemaVersion": 1, "schemaVersion": 2}',
                "<synthetic>",
            )
        self.assertEqual(raised.exception.code, "AREA-FIT-DUPLICATE-KEY")

    def test_named_negative_fixture_mutations_fail_expected_rules(self) -> None:
        seen = set()
        for case in self.fixture["mutations"]:
            seen.add(case["name"])
            if case["name"] == "duplicate-json-key":
                with self.assertRaises(
                    self.validator.ModelFitnessError
                ) as raised:
                    self.validator.apply_fixture_mutation(
                        self.contract_copy(), case["name"]
                    )
            else:
                mutated = self.contract_copy()
                self.validator.apply_fixture_mutation(mutated, case["name"])
                with self.assertRaises(
                    self.validator.ModelFitnessError
                ) as raised:
                    self.validator.validate_contract(
                        REPOSITORY_ROOT, mutated
                    )
            self.assertEqual(raised.exception.code, case["expectedRule"])
        self.assertEqual(seen, set(self.validator.NEGATIVE_MUTATIONS))

    def test_cli_production_and_self_test_pass(self) -> None:
        production = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(REPOSITORY_ROOT),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(production.returncode, 0, production.stderr)
        self.assertIn("roles=12 providers=4 tuples=48", production.stdout)

        self_test = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(REPOSITORY_ROOT),
                "--self-test",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(self_test.returncode, 0, self_test.stderr)
        self.assertIn(
            f"cases={len(self.fixture['mutations'])}", self_test.stdout
        )


if __name__ == "__main__":
    unittest.main()
