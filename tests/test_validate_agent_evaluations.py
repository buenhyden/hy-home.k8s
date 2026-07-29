#!/usr/bin/env python3
"""Focused tests for the Spec 044 agent-evaluation contract gate."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-agent-evaluations.py"
CONTRACT_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-evaluations.json"
)
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-evaluations.schema.json"
)
FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/agent-evaluations.json"


def load_module():
    """Import the validator without executing its CLI."""
    specification = importlib.util.spec_from_file_location(
        "validate_agent_evaluations",
        SCRIPT_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class AgentEvaluationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def contract_copy(self):
        return copy.deepcopy(self.contract)

    def assert_rule(self, contract, expected_rule: str) -> None:
        with self.assertRaises(
            self.validator.EvaluationContractError
        ) as raised:
            self.validator.validate_contract(REPOSITORY_ROOT, contract)
        self.assertEqual(raised.exception.code, expected_rule)

    def test_import_safe_api_is_explicit(self) -> None:
        for name in (
            "EvaluationContractError",
            "decode_json_text",
            "load_json",
            "validate_contract",
            "apply_mutation",
            "run_self_test",
            "main",
        ):
            with self.subTest(name=name):
                self.assertTrue(hasattr(self.validator, name))

    def test_schema_is_draft_2020_12_and_valid(self) -> None:
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        Draft202012Validator.check_schema(self.schema)

    def test_production_contract_is_contract_only_repo_static_and_deferred(
        self,
    ) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(counts, self.fixture["expectedCounts"])
        self.assertEqual(
            self.contract["authority"],
            {
                "state": "contract-only",
                "evidenceKind": "repo-static",
                "execution": "DEFER",
                "runtime": "DEFER",
                "providerResolution": "DEFER",
                "authentication": "DEFER",
                "liveAction": "DEFER",
                "evaluationDecision": "DEFER",
            },
        )
        serialized = json.dumps(self.contract, sort_keys=True)
        self.assertNotIn('"PASS"', serialized)
        self.assertNotIn('"runtime-ready"', serialized)

    def test_role_suites_define_exact_roles_and_four_fixture_classes(
        self,
    ) -> None:
        self.assertEqual(
            tuple(item["roleId"] for item in self.contract["roleSuites"]),
            self.validator.TARGET_ROLES,
        )
        self.assertEqual(
            tuple(self.contract["requiredFixtureClasses"]),
            self.validator.REQUIRED_FIXTURE_CLASSES,
        )
        for suite in self.contract["roleSuites"]:
            with self.subTest(role=suite["roleId"]):
                self.assertEqual(
                    tuple(suite["fixtureClasses"]),
                    self.validator.REQUIRED_FIXTURE_CLASSES,
                )
                self.assertEqual(suite["suiteVersion"], "1.0.0")
                self.assertEqual(suite["fixtureVersion"], "1.0.0")
                self.assertEqual(suite["graderVersion"], "1.0.0")
                self.assertEqual(suite["rubricVersion"], "1.0.0")
                self.assertEqual(suite["corpusState"], "DEFER")
                self.assertEqual(suite["evaluationDecision"], "DEFER")
                self.assertEqual(suite["rollbackState"], "DEFER")

    def test_record_contract_names_all_required_evidence_fields(self) -> None:
        record = self.contract["evaluationRecordContract"]
        self.assertEqual(
            record["suite"],
            {
                "idField": "suiteId",
                "versionField": "suiteVersion",
                "required": True,
            },
        )
        self.assertEqual(
            record["fixture"]["identityFields"],
            ["fixtureId", "fixtureVersion"],
        )
        self.assertEqual(
            record["fixture"]["evidenceFields"],
            ["provenance", "privacy", "risk", "inputDigest"],
        )
        self.assertEqual(
            record["fixture"]["digest"],
            {
                "field": "inputDigest",
                "algorithm": "sha256",
                "format": "sha256:<64-lowercase-hex>",
                "requiredAtExecution": True,
                "currentState": "DEFER",
            },
        )
        self.assertEqual(
            record["fixture"]["expectedBehavior"],
            {
                "pathsField": "allowedPaths",
                "toolsField": "allowedTools",
                "prohibitedActionsField": "prohibitedActions",
                "stopHandoffField": "stopHandoffExpectation",
            },
        )
        self.assertEqual(
            record["grader"],
            {
                "versionField": "graderVersion",
                "rubricVersionField": "rubricVersion",
                "rubricDimensions": [
                    "quality",
                    "safety",
                    "cost",
                    "latency",
                ],
            },
        )
        self.assertEqual(
            record["providerExecution"],
            {
                "provider": "DEFER",
                "model": "DEFER",
                "reasoning": "DEFER",
                "config": "DEFER",
                "canary": "DEFER",
            },
        )
        self.assertEqual(
            record["metrics"],
            {
                "quality": "DEFER",
                "safety": "DEFER",
                "cost": "DEFER",
                "latency": "DEFER",
            },
        )
        self.assertEqual(
            record["adjudication"],
            {
                "adjudicator": "DEFER",
                "independentForHighRisk": True,
                "decision": "DEFER",
            },
        )
        self.assertEqual(
            record["rollback"],
            {"state": "DEFER", "reference": "DEFER"},
        )

    def test_baseline_candidate_requires_same_suite_and_grader(self) -> None:
        comparison = self.contract["evaluationRecordContract"][
            "baselineCandidate"
        ]
        self.assertEqual(
            comparison,
            {
                "baseline": "DEFER",
                "candidate": "DEFER",
                "sameSuiteVersionRequired": True,
                "sameGraderVersionRequired": True,
            },
        )
        mutated = self.contract_copy()
        mutated["evaluationRecordContract"]["baselineCandidate"][
            "sameSuiteVersionRequired"
        ] = False
        self.assert_rule(mutated, "AREA-EVAL-BASELINE-COMPARISON")
        mutated = self.contract_copy()
        mutated["evaluationRecordContract"]["baselineCandidate"][
            "sameGraderVersionRequired"
        ] = False
        self.assert_rule(mutated, "AREA-EVAL-BASELINE-COMPARISON")

    def test_high_risk_suites_require_independent_adjudication(self) -> None:
        observed = {
            suite["roleId"]
            for suite in self.contract["roleSuites"]
            if suite["riskClass"] == "high"
        }
        self.assertEqual(observed, set(self.validator.HIGH_RISK_ROLES))
        for suite in self.contract["roleSuites"]:
            if suite["roleId"] in observed:
                self.assertTrue(suite["independentAdjudicationRequired"])
        mutated = self.contract_copy()
        target = next(
            item
            for item in mutated["roleSuites"]
            if item["roleId"] in observed
        )
        target["independentAdjudicationRequired"] = False
        self.assert_rule(mutated, "AREA-EVAL-ADJUDICATION")

    def test_promotion_policy_blocks_all_four_critical_events(self) -> None:
        self.assertEqual(
            tuple(self.contract["promotionPolicy"]["blockingEvents"]),
            self.validator.PROMOTION_BLOCKING_EVENTS,
        )
        for event in self.validator.PROMOTION_BLOCKING_EVENTS:
            with self.subTest(event=event):
                mutated = self.contract_copy()
                mutated["promotionPolicy"]["blockingEvents"].remove(event)
                self.assert_rule(mutated, "AREA-EVAL-PROMOTION-BLOCK")

    def test_schema_is_closed_at_every_contract_object_boundary(self) -> None:
        mutations = []
        root = self.contract_copy()
        root["unexpected"] = True
        mutations.append(root)
        authority = self.contract_copy()
        authority["authority"]["unexpected"] = True
        mutations.append(authority)
        record = self.contract_copy()
        record["evaluationRecordContract"]["fixture"]["unexpected"] = True
        mutations.append(record)
        expected = self.contract_copy()
        expected["evaluationRecordContract"]["fixture"][
            "expectedBehavior"
        ]["unexpected"] = True
        mutations.append(expected)
        role = self.contract_copy()
        role["roleSuites"][0]["unexpected"] = True
        mutations.append(role)
        for index, mutated in enumerate(mutations):
            with self.subTest(index=index):
                self.assert_rule(mutated, "AREA-EVAL-SCHEMA")

    def test_privacy_and_sensitive_material_fail_closed(self) -> None:
        mutated = self.contract_copy()
        mutated["privacyPolicy"]["rawPromptsAllowed"] = True
        self.assert_rule(mutated, "AREA-EVAL-PRIVACY")
        mutated = self.contract_copy()
        mutated["evaluationRecordContract"]["rollback"][
            "reference"
        ] = "sk-" + "synthetic-value"
        self.assert_rule(mutated, "AREA-EVAL-SENSITIVE")
        mutated = self.contract_copy()
        mutated["evaluationRecordContract"]["fixture"][
            "rawPrompt"
        ] = "[REDACTED]"
        self.assert_rule(mutated, "AREA-EVAL-SENSITIVE")

    def test_execution_or_decision_pass_preclaim_fails_closed(self) -> None:
        mutated = self.contract_copy()
        mutated["authority"]["runtime"] = "PASS"
        self.assert_rule(mutated, "AREA-EVAL-RUNTIME-PRECLAIM")
        mutated = self.contract_copy()
        mutated["roleSuites"][0]["evaluationDecision"] = "PASS"
        self.assert_rule(mutated, "AREA-EVAL-RUNTIME-PRECLAIM")

    def test_duplicate_json_key_is_rejected_with_stable_rule(self) -> None:
        with self.assertRaises(
            self.validator.EvaluationContractError
        ) as raised:
            self.validator.decode_json_text(
                '{"schemaVersion": 1, "schemaVersion": 1}',
                "<duplicate>",
            )
        self.assertEqual(
            raised.exception.code,
            "AREA-EVAL-JSON-DUPLICATE",
        )

    def test_all_governed_inputs_reject_symlinks_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root.parent / f"{root.name}-outside-sensitive-marker"
            outside.write_text('{"outside":"must-not-be-read"}', encoding="utf-8")
            try:
                for relative in (
                    self.validator.CONTRACT_PATH,
                    self.validator.SCHEMA_PATH,
                    self.validator.FIXTURE_PATH,
                ):
                    with self.subTest(relative=str(relative)):
                        governed = root.joinpath(*relative.parts)
                        governed.parent.mkdir(parents=True, exist_ok=True)
                        governed.symlink_to(outside)
                        with self.assertRaises(
                            self.validator.EvaluationContractError
                        ) as raised:
                            self.validator.load_json(root, relative)
                        self.assertEqual(
                            raised.exception.code,
                            "AREA-EVAL-INPUT",
                        )
                        self.assertEqual(raised.exception.exit_code, 2)
                        self.assertNotIn(outside.name, raised.exception.detail)
                        self.assertNotIn(
                            "must-not-be-read",
                            raised.exception.detail,
                        )
            finally:
                outside.unlink(missing_ok=True)

    def test_parent_symlink_and_parent_escape_never_follow_outside_repo(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "repo"
            root.mkdir()
            outside_tree = base / "outside-tree"
            outside_contract = outside_tree.joinpath(
                *self.validator.CONTRACT_PATH.parts
            )
            outside_contract.parent.mkdir(parents=True)
            outside_contract.write_text(
                '{"outside":"parent-symlink-sensitive-marker"}',
                encoding="utf-8",
            )
            (root / "docs").symlink_to(outside_tree / "docs")
            with self.assertRaises(
                self.validator.EvaluationContractError
            ) as raised:
                self.validator.load_json(
                    root,
                    self.validator.CONTRACT_PATH,
                )
            self.assertEqual(raised.exception.code, "AREA-EVAL-INPUT")
            self.assertNotIn(
                "parent-symlink-sensitive-marker",
                raised.exception.detail,
            )

            escaped = base / "outside.json"
            escaped.write_text('{"outside":"escape-marker"}', encoding="utf-8")
            with self.assertRaises(
                self.validator.EvaluationContractError
            ) as raised:
                self.validator.load_json(
                    root,
                    PurePosixPath("../outside.json"),
                )
            self.assertEqual(raised.exception.code, "AREA-EVAL-INPUT")
            self.assertNotIn("escape-marker", raised.exception.detail)

    def test_all_governed_inputs_reject_non_regular_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                self.validator.CONTRACT_PATH,
                self.validator.SCHEMA_PATH,
                self.validator.FIXTURE_PATH,
            ):
                with self.subTest(relative=str(relative)):
                    governed = root.joinpath(*relative.parts)
                    governed.mkdir(parents=True)
                    with self.assertRaises(
                        self.validator.EvaluationContractError
                    ) as raised:
                        self.validator.load_json(root, relative)
                    self.assertEqual(
                        raised.exception.code,
                        "AREA-EVAL-INPUT",
                    )
                    self.assertEqual(raised.exception.exit_code, 2)

    def test_repository_root_must_be_real_directory_not_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            real_root = base / "real-root"
            governed = real_root.joinpath(
                *self.validator.CONTRACT_PATH.parts
            )
            governed.parent.mkdir(parents=True)
            shutil.copy2(CONTRACT_PATH, governed)
            symlink_root = base / "symlink-root"
            symlink_root.symlink_to(real_root, target_is_directory=True)
            non_directory_root = base / "root-file"
            non_directory_root.write_text("not a repository", encoding="utf-8")

            for root in (
                symlink_root,
                non_directory_root,
                base / "missing-root",
            ):
                with self.subTest(root=root.name):
                    with self.assertRaises(
                        self.validator.EvaluationContractError
                    ) as raised:
                        self.validator.load_json(
                            root,
                            self.validator.CONTRACT_PATH,
                        )
                    self.assertEqual(
                        raised.exception.code,
                        "AREA-EVAL-INPUT",
                    )
                    self.assertEqual(raised.exception.exit_code, 2)
                    self.assertNotIn(str(real_root), raised.exception.detail)

    def test_cli_rejects_symlink_without_disclosing_target_or_payload(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            outside = Path(directory) / "outside-sensitive-name.json"
            outside.write_text(
                '{"outside":"cli-sensitive-payload"}',
                encoding="utf-8",
            )
            governed = root.joinpath(*self.validator.CONTRACT_PATH.parts)
            governed.parent.mkdir(parents=True)
            governed.symlink_to(outside)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--root",
                    str(root),
                ],
                capture_output=True,
                check=False,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("ERR AREA-EVAL-INPUT", result.stderr)
            self.assertNotIn(outside.name, result.stderr)
            self.assertNotIn("cli-sensitive-payload", result.stderr)

    def test_self_test_rejects_fixture_symlink_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            for source, relative in (
                (CONTRACT_PATH, self.validator.CONTRACT_PATH),
                (SCHEMA_PATH, self.validator.SCHEMA_PATH),
            ):
                destination = root.joinpath(*relative.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            outside = Path(directory) / "fixture-sensitive-name.json"
            outside.write_text(
                '{"outside":"fixture-sensitive-payload"}',
                encoding="utf-8",
            )
            fixture = root.joinpath(*self.validator.FIXTURE_PATH.parts)
            fixture.parent.mkdir(parents=True, exist_ok=True)
            fixture.symlink_to(outside)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--root",
                    str(root),
                    "--self-test",
                ],
                capture_output=True,
                check=False,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("ERR AREA-EVAL-INPUT", result.stderr)
            self.assertNotIn(outside.name, result.stderr)
            self.assertNotIn("fixture-sensitive-payload", result.stderr)

    def test_negative_fixture_is_named_unique_and_rule_stable(self) -> None:
        names = [item["name"] for item in self.fixture["mutations"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertGreaterEqual(len(names), 12)
        for case in self.fixture["mutations"]:
            with self.subTest(name=case["name"]):
                self.assertRegex(case["expectedRule"], r"^AREA-EVAL-[A-Z0-9-]+$")
        failures, count = self.validator.run_self_test(REPOSITORY_ROOT)
        self.assertEqual(failures, [])
        self.assertEqual(count, len(names))

    def test_unknown_mutation_uses_stable_fixture_rule(self) -> None:
        with self.assertRaises(
            self.validator.EvaluationContractError
        ) as raised:
            self.validator.apply_mutation(
                self.contract_copy(),
                "not-a-real-mutation",
            )
        self.assertEqual(raised.exception.code, "AREA-EVAL-FIXTURE")

    def test_cli_production_and_self_test_paths_pass(self) -> None:
        production = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(REPOSITORY_ROOT),
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(production.returncode, 0, production.stderr)
        self.assertIn("roles=12", production.stdout)
        self_test = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(REPOSITORY_ROOT),
                "--self-test",
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(self_test.returncode, 0, self_test.stderr)
        self.assertIn("cases=", self_test.stdout)


if __name__ == "__main__":
    unittest.main()
