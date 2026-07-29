#!/usr/bin/env python3
"""Focused tests for the Spec 044 roster-admission policy gate."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-agent-roster-admission.py"
CONTRACT_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-roster-admission.json"
)
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-roster-admission.schema.json"
)
FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/agent-roster-admission.json"

TARGET_ROLES = (
    "supervisor",
    "code-reviewer",
    "doc-writer",
    "gitops-reviewer",
    "incident-responder",
    "k8s-implementer",
    "network-reviewer",
    "observability-reviewer",
    "security-auditor",
    "wiki-curator",
    "docs-researcher",
    "quality-engineer",
)
SURFACES = ("local", "claude", "codex", "gemini")
EVALUATION_CLASSES = (
    "positive",
    "negative-adversarial",
    "refusal-stop",
    "handoff",
)
MEMORY_CLASSES = (
    "working-short-term",
    "durable-long-term",
    "domain-scoped",
    "provider-local-auxiliary",
)
DEFERRED_EVIDENCE = (
    "runtime",
    "provider-discovery",
    "provider-authentication",
    "hosted-ci",
    "remote",
    "live",
)


def load_module():
    scripts_dir = str(SCRIPT_PATH.parent)
    inserted = scripts_dir not in sys.path
    if inserted:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location(
        "validate_agent_roster_admission", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        if inserted:
            sys.path.remove(scripts_dir)
    return module


def assert_all_object_schemas_closed(
    testcase: unittest.TestCase,
    node: Any,
    path: str = "$",
) -> None:
    if not isinstance(node, dict):
        return
    if node.get("type") == "object" or "properties" in node:
        testcase.assertIs(
            node.get("additionalProperties"),
            False,
            f"{path} must be a closed object schema",
        )
    for key in ("properties", "$defs"):
        children = node.get(key)
        if isinstance(children, dict):
            for name, child in children.items():
                assert_all_object_schemas_closed(
                    testcase, child, f"{path}/{key}/{name}"
                )
    for key in ("items", "contains", "not", "if", "then", "else"):
        child = node.get(key)
        if isinstance(child, dict):
            assert_all_object_schemas_closed(testcase, child, f"{path}/{key}")
    for key in ("allOf", "anyOf", "oneOf", "prefixItems"):
        children = node.get(key)
        if isinstance(children, list):
            for index, child in enumerate(children):
                assert_all_object_schemas_closed(
                    testcase, child, f"{path}/{key}/{index}"
                )


class AgentRosterAdmissionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def contract_copy(self) -> dict[str, Any]:
        return copy.deepcopy(self.contract)

    def assert_rule(
        self, contract: dict[str, Any], expected_rule: str
    ) -> None:
        with self.assertRaises(self.validator.AdmissionError) as raised:
            self.validator.validate_contract(REPOSITORY_ROOT, contract)
        self.assertEqual(raised.exception.code, expected_rule)
        self.assertTrue(raised.exception.code.startswith("AREA-ADM-"))

    def test_validator_is_import_safe_and_exposes_typed_api(self) -> None:
        self.assertTrue(hasattr(self.validator, "AdmissionError"))
        self.assertTrue(hasattr(self.validator, "decode_json_text"))
        self.assertTrue(hasattr(self.validator, "load_contract"))
        self.assertTrue(hasattr(self.validator, "validate_contract"))
        self.assertTrue(hasattr(self.validator, "apply_mutation"))
        self.assertTrue(hasattr(self.validator, "run_self_test"))

    def test_schema_is_draft_2020_12_and_closes_every_object(self) -> None:
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        assert_all_object_schemas_closed(self, self.schema)

    def test_baseline_is_policy_only_and_preserves_inventory_boundary(self) -> None:
        counts = self.validator.validate_contract(
            REPOSITORY_ROOT, self.contract
        )
        self.assertEqual(
            counts,
            {
                "candidates": 2,
                "conditions": 7,
                "currentRoles": 10,
                "currentSurfaces": 3,
                "currentAdapters": 30,
                "targetRoles": 12,
                "targetSurfaces": 4,
                "targetAdapters": 48,
                "surfacePlans": 8,
                "evaluationClasses": 4,
                "memoryClasses": 4,
                "deferredEvidenceClasses": 6,
            },
        )
        self.assertEqual(self.contract["state"], "contract-only")
        self.assertEqual(self.contract["evidence"]["class"], "repo-static")
        self.assertEqual(self.contract["evidence"]["admissionVerdict"], "DEFER")
        self.assertFalse(self.contract["evidence"]["promotionAuthorized"])
        self.assertEqual(
            tuple(self.contract["evidence"]["deferredClasses"]),
            DEFERRED_EVIDENCE,
        )
        self.assertTrue(
            all(
                value == "DEFER"
                for value in self.contract["evidence"][
                    "deferredClassStates"
                ].values()
            )
        )

    def test_target_and_candidates_are_exact_but_unpromoted(self) -> None:
        self.assertEqual(
            self.contract["currentInventory"],
            {
                "state": "current",
                "roleCount": 10,
                "surfaceCount": 3,
                "adapterCount": 30,
            },
        )
        target = self.contract["targetInventory"]
        self.assertEqual(target["state"], "target-only")
        self.assertEqual(
            (target["roleCount"], target["surfaceCount"], target["adapterCount"]),
            (12, 4, 48),
        )
        self.assertEqual(tuple(target["roleIds"]), TARGET_ROLES)
        self.assertEqual(tuple(target["surfaceIds"]), SURFACES)
        self.assertEqual(
            tuple(candidate["roleId"] for candidate in self.contract["candidates"]),
            ("docs-researcher", "quality-engineer"),
        )
        self.assertTrue(
            all(
                candidate["decision"] == "candidate-only"
                for candidate in self.contract["candidates"]
            )
        )

    def test_each_candidate_has_a_closed_distinct_role_contract(self) -> None:
        deliverables: set[str] = set()
        owners: set[str] = set()
        for candidate in self.contract["candidates"]:
            requirement = candidate["requirementGap"]
            self.assertEqual(
                requirement["classification"],
                "approved-recurring-unowned-gap",
            )
            self.assertTrue(requirement["approved"])
            self.assertTrue(requirement["recurring"])
            self.assertFalse(requirement["currentlyOwned"])
            overlap = candidate["overlapAnalysis"]
            self.assertFalse(overlap["existingRoleCanOwnDeliverable"])
            self.assertFalse(overlap["strengthenExistingRoleResolvesGap"])
            self.assertTrue(overlap["distinctOwnerRequired"])
            self.assertTrue(candidate["owner"])
            self.assertTrue(candidate["inputs"])
            self.assertTrue(candidate["outputs"])
            self.assertTrue(candidate["permissions"])
            self.assertTrue(candidate["allowedTools"])
            self.assertTrue(candidate["allowedPaths"])
            self.assertTrue(candidate["prohibitedActions"])
            self.assertTrue(candidate["stopConditions"])
            self.assertTrue(candidate["handoffs"])
            self.assertTrue(candidate["distinctDeliverable"])
            self.assertNotIn(candidate["owner"], owners)
            self.assertNotIn(candidate["distinctDeliverable"], deliverables)
            owners.add(candidate["owner"])
            deliverables.add(candidate["distinctDeliverable"])

    def test_four_surface_eval_adjudication_and_rollback_are_preconditions(self) -> None:
        for candidate in self.contract["candidates"]:
            surface_plan = candidate["surfacePlan"]
            self.assertEqual(
                tuple(item["surfaceId"] for item in surface_plan), SURFACES
            )
            self.assertTrue(
                all(item["state"] == "target-only" for item in surface_plan)
            )
            self.assertTrue(
                all(item["leastPrivilege"] for item in surface_plan)
            )
            evaluation = candidate["evaluationGate"]
            self.assertEqual(
                tuple(evaluation["classes"]), EVALUATION_CLASSES
            )
            self.assertEqual(
                evaluation["baselineState"], "required-before-promotion"
            )
            adjudication = evaluation["independentAdjudication"]
            self.assertTrue(adjudication["required"])
            self.assertTrue(adjudication["selfAdjudicationProhibited"])
            self.assertEqual(
                tuple(adjudication["thresholdOrder"]),
                ("quality", "safety", "cost", "latency"),
            )
            rollback = candidate["rollback"]
            self.assertEqual(
                rollback["state"], "required-before-promotion"
            )
            self.assertEqual(rollback["restoreInventory"], "10/3/30")
            self.assertTrue(rollback["reproducible"])
            self.assertFalse(rollback["executed"])

    def test_external_catalog_and_memory_are_non_authoritative(self) -> None:
        catalog = self.contract["externalCatalogPolicy"]
        self.assertEqual(catalog["source"], "msitarzewski/agency-agents")
        self.assertEqual(catalog["authority"], "idea-catalog-only")
        self.assertFalse(catalog["directImportAllowed"])
        self.assertTrue(catalog["localAdmissionEvidenceRequired"])
        memory = self.contract["memoryPolicy"]
        self.assertEqual(tuple(memory["classes"]), MEMORY_CLASSES)
        self.assertTrue(memory["repositoryWins"])
        self.assertFalse(memory["sensitiveDataAllowed"])
        self.assertFalse(memory["rawPromptOrTranscriptAllowed"])
        self.assertTrue(memory["prohibitedContent"])

    def test_duplicate_keys_fail_at_the_input_boundary(self) -> None:
        with self.assertRaises(self.validator.AdmissionError) as raised:
            self.validator.decode_json_text(
                '{"state":"contract-only","state":"current"}',
                "<unit-fixture>",
            )
        self.assertEqual(raised.exception.code, "AREA-ADM-DUPLICATE-KEY")
        self.assertEqual(raised.exception.exit_code, 2)

    def test_all_named_negative_mutations_fail_with_declared_rule(self) -> None:
        self.assertGreaterEqual(len(self.fixture["mutations"]), 30)
        for case in self.fixture["mutations"]:
            with self.subTest(case=case["name"]):
                mutated = self.contract_copy()
                self.validator.apply_mutation(mutated, case["name"])
                self.assert_rule(mutated, case["expectedRule"])

    def test_unknown_mutation_is_a_stable_fixture_failure(self) -> None:
        with self.assertRaises(self.validator.AdmissionError) as raised:
            self.validator.apply_mutation(
                self.contract_copy(), "not-a-supported-mutation"
            )
        self.assertEqual(raised.exception.code, "AREA-ADM-FIXTURE")

    def test_self_test_and_production_cli_pass_without_runtime_claims(self) -> None:
        self_test = subprocess.run(
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
        self.assertEqual(self_test.returncode, 0, self_test.stderr)
        self.assertIn(
            "[PASS] agent roster admission self-test passed",
            self_test.stdout,
        )
        production = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(REPOSITORY_ROOT),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(production.returncode, 0, production.stderr)
        self.assertIn("state=contract-only", production.stdout)
        self.assertIn("verdict=DEFER", production.stdout)
        self.assertIn("current=10/3/30", production.stdout)
        self.assertIn("target=12/4/48", production.stdout)
        self.assertNotIn("admission=PASS", production.stdout)
        self.assertNotIn("runtime=PASS", production.stdout)


if __name__ == "__main__":
    unittest.main()
