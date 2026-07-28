#!/usr/bin/env python3
"""Unit tests for the provider-neutral agent loop lifecycle contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPOSITORY_ROOT / "scripts/validate-agent-loop-lifecycle.py"
)
CONTRACT_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-loop-lifecycle.json"
)
FIXTURE_PATH = (
    REPOSITORY_ROOT / "tests/fixtures/agent-loop-lifecycle.json"
)


def load_module():
    specification = importlib.util.spec_from_file_location(
        "validate_agent_loop_lifecycle", SCRIPT_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class AgentLoopLifecycleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def contract_copy(self):
        return copy.deepcopy(self.contract)

    def assert_rule(self, contract, expected_rule: str) -> None:
        with self.assertRaises(
            self.validator.LoopLifecycleError
        ) as raised:
            self.validator.validate_contract(REPOSITORY_ROOT, contract)
        self.assertEqual(raised.exception.code, expected_rule)

    def test_validator_exposes_import_safe_contract_and_decision_api(
        self,
    ) -> None:
        for name in (
            "LoopLifecycleError",
            "validate_contract",
            "normalize_failure",
            "measure_progress",
            "decide_next",
            "effective_recovery_limit",
            "normalizeFailure",
            "measureProgress",
            "decideNext",
        ):
            with self.subTest(name=name):
                self.assertTrue(hasattr(self.validator, name))

    def test_production_contract_is_closed_current_and_provider_neutral(
        self,
    ) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(counts, self.fixture["expectedCounts"])
        self.assertEqual(self.contract["schemaVersion"], 1)
        self.assertEqual(self.contract["contractId"], "agent-loop-lifecycle")
        self.assertEqual(self.contract["contractVersion"], "1.0.0")
        self.assertTrue(self.contract["providerNeutral"])
        self.assertEqual(
            self.contract["currentOwner"],
            {
                "path": (
                    "docs/00.agent-governance/contracts/"
                    "agent-loop-lifecycle.json"
                ),
                "contractVersion": "1.0.0",
                "status": "current",
            },
        )

    def test_state_machine_is_closed_with_four_terminal_states(self) -> None:
        machine = self.contract["stateMachine"]
        self.assertEqual(
            tuple(state["id"] for state in machine["states"]),
            self.validator.STATE_IDS,
        )
        self.assertEqual(
            tuple(
                state["id"]
                for state in machine["states"]
                if state["terminal"]
            ),
            self.validator.TERMINAL_STATE_IDS,
        )
        self.assertEqual(
            tuple(
                (item["from"], item["event"], item["to"])
                for item in machine["transitions"]
            ),
            self.validator.TRANSITIONS,
        )

    def test_retry_contract_uses_exact_ceilings_and_persistent_counters(
        self,
    ) -> None:
        policy = self.contract["retryPolicy"]
        self.assertFalse(policy["initialFailureCountsAsRetry"])
        self.assertEqual(policy["maxAutomaticRetriesPerSignature"], 2)
        self.assertEqual(
            policy["defaultMaxAutomaticRecoveryActionsPerTask"], 3
        )
        self.assertFalse(policy["providerFallbackResetsCounters"])
        self.assertFalse(policy["modelFallbackResetsCounters"])
        self.assertFalse(policy["handoffResetsCounters"])
        self.assertFalse(policy["signatureChangeResetsTaskRecoveryCounter"])
        self.assertEqual(
            self.validator.effective_recovery_limit(3, 2, 1), 1
        )

    def test_retry_sequence_allows_zero_to_one_to_two_then_stops(
        self,
    ) -> None:
        failure = {
            "class": "transient-validation",
            "signatureDigest": "a" * 64,
            "retryable": True,
        }
        first = self.validator.decide_next(
            {
                "automaticRetriesForSignature": 0,
                "automaticRecoveryActionsUsed": 0,
                "consecutiveIdenticalNoProgressResults": 1,
                "proposedActionDiffers": True,
            },
            {},
            failure,
            {"progressed": False, "deltaClasses": []},
            self.contract,
        )
        self.assertEqual(first["decision"], "retry")
        self.assertEqual(first["nextAutomaticRetriesForSignature"], 1)
        self.assertEqual(first["nextAutomaticRecoveryActionsUsed"], 1)

        second = self.validator.decide_next(
            {
                "automaticRetriesForSignature": 1,
                "automaticRecoveryActionsUsed": 1,
                "consecutiveIdenticalNoProgressResults": 0,
                "proposedActionDiffers": True,
            },
            {},
            failure,
            {
                "progressed": True,
                "deltaClasses": ["narrowed-reproducible-failure"],
            },
            self.contract,
        )
        self.assertEqual(second["decision"], "retry")
        self.assertEqual(second["nextAutomaticRetriesForSignature"], 2)
        self.assertEqual(second["nextAutomaticRecoveryActionsUsed"], 2)

        exhausted = self.validator.decide_next(
            {
                "automaticRetriesForSignature": 2,
                "automaticRecoveryActionsUsed": 2,
                "consecutiveIdenticalNoProgressResults": 0,
                "proposedActionDiffers": True,
            },
            {},
            failure,
            {
                "progressed": True,
                "deltaClasses": ["newly-satisfied-criterion"],
            },
            self.contract,
        )
        self.assertEqual(exhausted["decision"], "escalate")
        self.assertEqual(
            exhausted["reason"],
            "same-signature-retry-budget-exhausted",
        )

    def test_task_recovery_budget_and_lower_limits_do_not_reset(
        self,
    ) -> None:
        cases = {
            case["name"]: case for case in self.fixture["decisionCases"]
        }
        third = cases[
            "third-task-recovery-survives-provider-model-fallback"
        ]
        third_result = self.validator.decide_next(
            third["loopState"],
            third["budgets"],
            third["failure"],
            third["progress"],
            self.contract,
        )
        self.assertEqual(third_result["decision"], "retry")
        self.assertEqual(
            third_result["nextAutomaticRecoveryActionsUsed"], 3
        )

        for name, expected_limit in (
            ("fourth-task-recovery-is-denied", 3),
            ("lower-role-limit-wins", 2),
            ("lower-task-limit-wins", 1),
        ):
            with self.subTest(name=name):
                case = cases[name]
                result = self.validator.decide_next(
                    case["loopState"],
                    case["budgets"],
                    case["failure"],
                    case["progress"],
                    self.contract,
                )
                self.assertEqual(result["decision"], "escalate")
                self.assertEqual(
                    result["reason"],
                    "task-recovery-budget-exhausted",
                )
                self.assertEqual(
                    result["effectiveRecoveryLimit"], expected_limit
                )

    def test_second_identical_no_progress_result_escalates_with_budget(
        self,
    ) -> None:
        case = next(
            item
            for item in self.fixture["decisionCases"]
            if item["name"]
            == "second-identical-no-progress-result-escalates-first"
        )
        result = self.validator.decide_next(
            case["loopState"],
            case["budgets"],
            case["failure"],
            case["progress"],
            self.contract,
        )
        self.assertEqual(result["decision"], "escalate")
        self.assertEqual(
            result["reason"], "second-identical-no-progress-result"
        )
        self.assertEqual(result["nextAutomaticRetriesForSignature"], 0)
        self.assertEqual(result["nextAutomaticRecoveryActionsUsed"], 0)

    def test_exact_six_nonretryable_classes_stop_without_counter_change(
        self,
    ) -> None:
        observed = tuple(
            item["id"]
            for item in self.contract["nonRetryableFailureClasses"]
        )
        self.assertEqual(
            observed, self.validator.NONRETRYABLE_FAILURE_CLASSES
        )
        for failure_class in observed:
            with self.subTest(failure_class=failure_class):
                result = self.validator.decide_next(
                    {
                        "automaticRetriesForSignature": 0,
                        "automaticRecoveryActionsUsed": 0,
                        "consecutiveIdenticalNoProgressResults": 0,
                        "proposedActionDiffers": True,
                    },
                    {},
                    {
                        "class": failure_class,
                        "signatureDigest": "1" * 64,
                        "retryable": False,
                    },
                    {"progressed": False, "deltaClasses": []},
                    self.contract,
                )
                expected = (
                    "stop"
                    if failure_class == "explicit-user-stop"
                    else "escalate"
                )
                self.assertEqual(result["decision"], expected)
                self.assertEqual(
                    result["nextAutomaticRetriesForSignature"], 0
                )
                self.assertEqual(
                    result["nextAutomaticRecoveryActionsUsed"], 0
                )

    def test_failure_normalization_ignores_provider_and_volatile_prose(
        self,
    ) -> None:
        baseline = {
            "validatorResultClass": "Static Validation",
            "stableCommandId": "repo-quality",
            "exitClass": "nonzero",
            "sanitizedDiagnosticCode": "AHLL-EXAMPLE",
            "affectedScope": ["scripts", "tests"],
            "contractVersion": "1.0.0",
            "failureClass": "transient-validation",
            "providerId": "local",
            "modelId": "model-one",
            "timestamp": "first-observation",
            "providerProse": "wording one",
        }
        alternate = copy.deepcopy(baseline)
        alternate.update(
            {
                "providerId": "codex",
                "modelId": "model-two",
                "timestamp": "second-observation",
                "providerProse": "wording two",
            }
        )
        first = self.validator.normalize_failure(
            baseline, self.contract
        )
        second = self.validator.normalize_failure(
            alternate, self.contract
        )
        self.assertEqual(
            first["signatureDigest"], second["signatureDigest"]
        )
        self.assertTrue(first["retryable"])

        nonretryable = copy.deepcopy(baseline)
        nonretryable["failureClass"] = "permission-denial"
        nonretryable["retryable"] = True
        self.assertFalse(
            self.validator.normalize_failure(
                nonretryable, self.contract
            )["retryable"]
        )

    def test_progress_requires_one_authorized_deterministic_delta(
        self,
    ) -> None:
        before = {
            "intendedFileState": "revision-one",
            "failingAssertionCount": 4,
            "satisfiedCriteria": ["VAL-AHLL-001"],
            "reproductionScopeSize": 8,
            "approvedHandoffArtifact": None,
            "tokenCount": 10,
            "commandCount": 1,
            "providerProse": "first wording",
        }
        after = {
            "intendedFileState": "revision-two",
            "intendedFileStateAuthorized": True,
            "failingAssertionCount": 2,
            "satisfiedCriteria": ["VAL-AHLL-001", "VAL-AHLL-002"],
            "reproductionScopeSize": 3,
            "approvedHandoffArtifact": "task-evidence-ref",
            "handoffApproved": True,
            "tokenCount": 100,
            "commandCount": 5,
            "providerProse": "different wording",
        }
        result = self.validator.measure_progress(
            before, after, self.contract
        )
        self.assertTrue(result["progressed"])
        self.assertEqual(
            tuple(result["deltaClasses"]),
            self.validator.PROGRESS_DELTA_CLASSES,
        )

        rejected_only = copy.deepcopy(before)
        rejected_only.update(
            {
                "tokenCount": 1000,
                "commandCount": 9,
                "providerProse": "changed wording only",
            }
        )
        self.assertEqual(
            self.validator.measure_progress(
                before, rejected_only, self.contract
            ),
            {"progressed": False, "deltaClasses": []},
        )

    def test_decision_inputs_reject_nested_sensitive_payloads(self) -> None:
        with self.assertRaises(
            self.validator.LoopLifecycleError
        ) as raised:
            self.validator.decide_next(
                {
                    "automaticRetriesForSignature": 0,
                    "automaticRecoveryActionsUsed": 0,
                    "consecutiveIdenticalNoProgressResults": 1,
                    "proposedActionDiffers": True,
                    "token": "syntheticfixturevalue",
                },
                {},
                {
                    "class": "transient-validation",
                    "signatureDigest": "a" * 64,
                    "retryable": True,
                },
                {"progressed": False, "deltaClasses": []},
                self.contract,
            )
        self.assertEqual(raised.exception.code, "AHLL-SENSITIVE")

    def test_checkpoint_boundary_is_executable_and_harness_aligned(
        self,
    ) -> None:
        boundary = self.contract["checkpointBoundary"]
        self.assertEqual(
            boundary["schemaRef"],
            (
                "docs/00.agent-governance/contracts/"
                "agent-checkpoint.schema.json"
            ),
        )
        self.assertEqual(boundary["implementationOwner"], "AHLL-002")
        self.assertEqual(boundary["implementationState"], "executable")
        self.assertTrue(boundary["executableValidationDelegated"])
        self.assertTrue(boundary["repositoryStateWins"])
        self.assertEqual(
            tuple(boundary["memoryClassIds"]),
            self.validator.MEMORY_CLASS_IDS,
        )
        for interface_id in ("writeCheckpoint", "resume", "handoff"):
            with self.subTest(interface_id=interface_id):
                interface = self.contract["interfaces"][interface_id]
                self.assertEqual(
                    interface["implementationOwner"],
                    "AHLL-002",
                )
                self.assertEqual(
                    interface["implementationState"],
                    "executable",
                )

    def test_duplicate_json_keys_fail_at_the_input_boundary(self) -> None:
        with self.assertRaises(
            self.validator.LoopLifecycleError
        ) as raised:
            self.validator.decode_json_text(
                '{"loop":{"state":"running","state":"completed"}}',
                "<unit-fixture>",
            )
        self.assertEqual(raised.exception.code, "AHLL-DUPLICATE-KEY")
        self.assertEqual(raised.exception.exit_code, 2)

    def test_sensitive_scanner_accepts_policy_labels_and_rejects_values(
        self,
    ) -> None:
        self.validator.scan_sensitive_payload(
            {
                "prohibitedFields": [
                    "credentials",
                    "tokens",
                    "raw-prompts-or-transcripts",
                    "provider-response-bodies",
                    "shell-history",
                    "user-configuration",
                ],
                "policy": (
                    "Credentials and raw prompts are prohibited lifecycle "
                    "payload classes."
                ),
            }
        )
        with self.assertRaises(
            self.validator.LoopLifecycleError
        ) as raised:
            self.validator.scan_sensitive_payload(
                {
                    "meaning": (
                        "Bearer " + "syntheticfixturevalue"
                    )
                }
            )
        self.assertEqual(raised.exception.code, "AHLL-SENSITIVE")

        for key in ("providerResponseBody", "userConfiguration"):
            with self.subTest(key=key):
                with self.assertRaises(
                    self.validator.LoopLifecycleError
                ) as key_raised:
                    self.validator.scan_sensitive_payload(
                        {key: "syntheticfixturevalue"}
                    )
                self.assertEqual(
                    key_raised.exception.code, "AHLL-SENSITIVE"
                )

    def test_all_negative_mutations_fail_with_declared_rule(self) -> None:
        for case in self.fixture["mutations"]:
            with self.subTest(case=case["name"]):
                mutated = self.contract_copy()
                self.validator.apply_mutation(mutated, case["name"])
                self.assert_rule(mutated, case["expectedRule"])

    def test_all_fixture_decisions_match_declared_outcome(self) -> None:
        for case in self.fixture["decisionCases"]:
            with self.subTest(case=case["name"]):
                result = self.validator.decide_next(
                    case["loopState"],
                    case["budgets"],
                    case["failure"],
                    case["progress"],
                    self.contract,
                )
                self.assertEqual(
                    (
                        result["decision"],
                        result["reason"],
                        result["effectiveRecoveryLimit"],
                    ),
                    (
                        case["expectedDecision"],
                        case["expectedReason"],
                        case["expectedEffectiveRecoveryLimit"],
                    ),
                )

    def test_cli_production_and_self_test_modes_pass(self) -> None:
        for extra_args, marker in (
            (
                [],
                "[PASS] agent loop lifecycle validation passed",
            ),
            (
                ["--self-test"],
                "[PASS] agent loop lifecycle self-test passed",
            ),
        ):
            with self.subTest(extra_args=extra_args):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT_PATH),
                        "--root",
                        str(REPOSITORY_ROOT),
                        *extra_args,
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(marker, result.stdout)


if __name__ == "__main__":
    unittest.main()
