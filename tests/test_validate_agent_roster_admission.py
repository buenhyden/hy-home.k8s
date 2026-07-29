#!/usr/bin/env python3
"""Focused tests for the Spec 044 roster-admission policy gate."""

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
    "model-resolution",
    "hosted-ci",
    "remote",
    "live",
    "agent-evaluation",
    "model-fitness",
)
PROMOTION_SCOPE = "repository-static-role-and-adapter-inventory-only"
GOVERNED_INPUTS = (
    CONTRACT_PATH,
    SCHEMA_PATH,
    FIXTURE_PATH,
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/harness-contract.json",
)


def copy_governed_inputs(root: Path) -> None:
    for source in GOVERNED_INPUTS:
        destination = root / source.relative_to(REPOSITORY_ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


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

    def test_baseline_admits_only_repository_static_inventory(self) -> None:
        counts = self.validator.validate_contract(
            REPOSITORY_ROOT, self.contract
        )
        self.assertEqual(
            counts,
            {
                "candidates": 2,
                "conditions": 7,
                "currentRoles": 12,
                "currentSurfaces": 4,
                "currentAdapters": 48,
                "targetRoles": 12,
                "targetSurfaces": 4,
                "targetAdapters": 48,
                "surfacePlans": 8,
                "evaluationClasses": 4,
                "memoryClasses": 4,
                "deferredEvidenceClasses": 9,
            },
        )
        self.assertEqual(
            self.contract["state"], "repository-static-admitted"
        )
        self.assertEqual(self.contract["evidence"]["class"], "repo-static")
        self.assertEqual(self.contract["evidence"]["admissionVerdict"], "PASS")
        authorization = self.contract["evidence"]["promotionAuthorization"]
        self.assertTrue(authorization["authorized"])
        self.assertEqual(authorization["scope"], PROMOTION_SCOPE)
        self.assertEqual(
            tuple(authorization["excludedEvidenceClasses"]),
            DEFERRED_EVIDENCE,
        )
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

    def test_target_is_achieved_and_candidates_are_static_only(self) -> None:
        self.assertEqual(
            self.contract["currentInventory"],
            {
                "state": "current",
                "roleCount": 12,
                "surfaceCount": 4,
                "adapterCount": 48,
            },
        )
        target = self.contract["targetInventory"]
        self.assertEqual(target["state"], "achieved")
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
                candidate["decision"] == "repository-static-admitted"
                and candidate["authority"] == PROMOTION_SCOPE
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

    def test_static_surfaces_are_current_but_future_gates_stay_deferred(self) -> None:
        for candidate in self.contract["candidates"]:
            surface_plan = candidate["surfacePlan"]
            self.assertEqual(
                tuple(item["surfaceId"] for item in surface_plan), SURFACES
            )
            self.assertTrue(
                all(item["state"] == "current" for item in surface_plan)
            )
            self.assertTrue(
                all(item["leastPrivilege"] for item in surface_plan)
            )
            evaluation = candidate["evaluationGate"]
            self.assertEqual(
                tuple(evaluation["classes"]), EVALUATION_CLASSES
            )
            self.assertEqual(
                evaluation["baselineState"],
                "deferred-to-area-003-before-runtime-activation",
            )
            adjudication = evaluation["independentAdjudication"]
            self.assertTrue(adjudication["required"])
            self.assertTrue(adjudication["selfAdjudicationProhibited"])
            self.assertEqual(
                tuple(adjudication["thresholdOrder"]),
                ("quality", "safety", "cost", "latency"),
            )
            rollback = candidate["rollback"]
            self.assertEqual(rollback["state"], "armed")
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
                '{"state":"repository-static-admitted","state":"current"}',
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

    def test_governed_inputs_reject_final_and_intermediate_symlinks(self) -> None:
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
                        self.validator.AdmissionError
                    ) as raised:
                        if source == FIXTURE_PATH:
                            self.validator.run_self_test(root)
                        else:
                            self.validator.validate_contract(root)
                    self.assertEqual(raised.exception.code, "AREA-ADM-INPUT")
                    self.assertNotIn(str(outside), raised.exception.detail)

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
            with self.assertRaises(self.validator.AdmissionError) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-ADM-INPUT")
            self.assertNotIn(str(REPOSITORY_ROOT), raised.exception.detail)

    def test_non_regular_input_and_symlink_or_file_root_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "repository"
            copy_governed_inputs(root)
            harness = root / GOVERNED_INPUTS[-1].relative_to(REPOSITORY_ROOT)
            harness.unlink()
            harness.mkdir()
            with self.assertRaises(self.validator.AdmissionError) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-ADM-INPUT")

            root_file = base / "not-a-directory"
            root_file.write_text("synthetic\n", encoding="utf-8")
            with self.assertRaises(self.validator.AdmissionError) as raised:
                self.validator.validate_contract(root_file)
            self.assertEqual(raised.exception.code, "AREA-ADM-INPUT")
            self.assertNotIn(str(root_file), raised.exception.detail)

            actual_root = base / "actual-repository"
            copy_governed_inputs(actual_root)
            root_link = base / "repository-link"
            root_link.symlink_to(actual_root)
            with self.assertRaises(self.validator.AdmissionError) as raised:
                self.validator.validate_contract(root_link)
            self.assertEqual(raised.exception.code, "AREA-ADM-INPUT")
            self.assertNotIn(str(actual_root), raised.exception.detail)

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
        self.assertIn("state=repository-static-admitted", production.stdout)
        self.assertIn("verdict=PASS", production.stdout)
        self.assertIn(f"scope={PROMOTION_SCOPE}", production.stdout)
        self.assertIn("current=12/4/48", production.stdout)
        self.assertIn("target=achieved:12/4/48", production.stdout)
        self.assertNotIn("runtime=PASS", production.stdout)
        self.assertNotIn("model_resolution=PASS", production.stdout)
        self.assertNotIn("agent_evaluation=PASS", production.stdout)
        self.assertNotIn("model_fitness=PASS", production.stdout)


if __name__ == "__main__":
    unittest.main()
