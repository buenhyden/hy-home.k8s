#!/usr/bin/env python3
"""Focused tests for the Spec 046 agent-governance closure contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from unittest.mock import patch

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate-agent-governance-closure.py"
CONTRACT_PATH = (
    REPO_ROOT / "docs/00.agent-governance/contracts/agent-governance-closure.json"
)
SCHEMA_PATH = CONTRACT_PATH.with_name("agent-governance-closure.schema.json")
FIXTURE_PATH = REPO_ROOT / "tests/fixtures/agent-governance-closure.json"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_governance_closure",
        VALIDATOR_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentGovernanceClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_validator()
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def assertRejected(self, contract: dict, expected: str) -> None:
        errors = self.module.validate_contract(contract, self.schema)
        self.assertTrue(errors)
        self.assertIn(expected, "\n".join(errors))

    def test_contract_artifacts_exist(self) -> None:
        for path in (VALIDATOR_PATH, CONTRACT_PATH, SCHEMA_PATH, FIXTURE_PATH):
            self.assertTrue(path.is_file(), path)

    def test_schema_is_valid_closed_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertFalse(self.schema["additionalProperties"])

        def assert_closed_objects(value: object) -> None:
            if isinstance(value, dict):
                if value.get("type") == "object":
                    self.assertIs(value.get("additionalProperties"), False)
                for nested in value.values():
                    assert_closed_objects(nested)
            elif isinstance(value, list):
                for nested in value:
                    assert_closed_objects(nested)

        assert_closed_objects(self.schema)

    def test_positive_fixture_and_contract_pass(self) -> None:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(self.module.validate_contract(self.fixture, self.schema), [])
        self.assertEqual(self.module.validate_contract(contract, self.schema), [])
        for review in self.fixture["reviewEvidence"].values():
            self.assertEqual(
                review,
                {
                    "result": "PASS",
                    "owner": "AGPC-004",
                    "critical": 0,
                    "important": 0,
                    "minor": 0,
                    "limitation": None,
                    "retryTrigger": None,
                },
            )
        self.assertEqual(
            self.module.validate_repository(REPO_ROOT, contract, self.schema),
            [],
        )

    def test_terminal_transition_metadata_is_exact(self) -> None:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        expected_handoff = {
            "localMerge": "planned",
            "remoteAction": "not-authorized",
            "worktreeCleanup": "planned",
        }
        for candidate in (self.fixture, contract):
            with self.subTest(contractVersion=candidate["contractVersion"]):
                self.assertEqual(candidate["contractVersion"], "1.2.1")
                adr = candidate["predecessorCriteria"][2]
                self.assertEqual(adr["id"], "adr-0019")
                self.assertEqual(adr["expectedStatus"], "accepted")
                self.assertEqual(
                    adr["implementationRef"],
                    "git-sha1:0a9e10324b552079fdd212683570e08a19878376",
                )
                self.assertEqual(
                    {row["owner"] for row in candidate["reviewEvidence"].values()},
                    {"AGPC-004"},
                )
                self.assertEqual(candidate["handoff"], expected_handoff)
        self.assertIn(
            "accepted",
            self.schema["$defs"]["criterion"]["properties"]["expectedStatus"]["enum"],
        )

    def test_fixed_cutoff_and_cross_lane_boundary_are_exact(self) -> None:
        self.assertEqual(
            self.fixture["cutoff"],
            {
                "localTime": "2026-07-10T10:00:00+09:00",
                "utc": "2026-07-10T01:00:00Z",
                "timezone": "Asia/Seoul",
            },
        )
        self.assertIs(self.fixture["crossLanePromotion"], False)

    def test_predecessor_set_includes_upstream_and_specs_038_through_045(self) -> None:
        self.assertEqual(
            tuple(row["id"] for row in self.fixture["predecessorCriteria"]),
            tuple(row[0] for row in self.module.EXPECTED_PREDECESSORS),
        )

    def test_provider_and_memory_sets_are_exact_and_ordered(self) -> None:
        self.assertEqual(
            tuple(row["provider"] for row in self.fixture["providerCanaries"]),
            self.module.EXPECTED_PROVIDERS,
        )
        self.assertEqual(
            tuple(row["id"] for row in self.fixture["memoryLayers"]),
            self.module.EXPECTED_MEMORY_CLASSES,
        )
        for layer in self.fixture["memoryLayers"]:
            self.assertTrue(layer["conflictHandling"])
        self.assertEqual(
            {
                row["provider"]: (
                    row["installation"],
                    row["runtimeResult"],
                    row["authResult"],
                    row["modelDiscoveryResult"],
                )
                for row in self.fixture["providerCanaries"]
            },
            self.module.EXPECTED_PROVIDER_OBSERVATIONS,
        )

    def test_self_test_rejects_every_deterministic_mutation(self) -> None:
        self.assertEqual(self.module._self_test(REPO_ROOT), [])

    def test_rejects_cross_lane_promotion(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["crossLanePromotion"] = True
        self.assertRejected(contract, "crossLanePromotion must remain false")

    def test_rejects_provider_runtime_pass_collapse(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["providerCanaries"][0]["runtimeResult"] = "PASS"
        self.assertRejected(contract, "non-repository lane must not claim PASS")

    def test_rejects_missing_or_reordered_provider(self) -> None:
        missing = copy.deepcopy(self.fixture)
        missing["providerCanaries"].pop()
        self.assertRejected(missing, "must be exactly claude, codex, gemini")

        reordered = copy.deepcopy(self.fixture)
        reordered["providerCanaries"].reverse()
        self.assertRejected(reordered, "must be exactly claude, codex, gemini")

    def test_rejects_provider_observation_boundary_drift(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["providerCanaries"][1]["installation"] = "not-observed"
        self.assertRejected(contract, "provider observation boundary differs")

        detail_drift = copy.deepcopy(self.fixture)
        detail_drift["providerCanaries"][1]["instructionSources"].reverse()
        self.assertRejected(detail_drift, "provider canary detail boundary differs")

    def test_rejects_missing_or_wrong_upstream_predecessor(self) -> None:
        missing = copy.deepcopy(self.fixture)
        missing["predecessorCriteria"].pop(0)
        self.assertRejected(missing, "PRD 003, AD 0006, ADR 0019")

        wrong_owner = copy.deepcopy(self.fixture)
        wrong_owner["predecessorCriteria"][1]["owner"] = "platform"
        self.assertRejected(wrong_owner, "PRD 003, AD 0006, ADR 0019")

    def test_rejects_duplicate_predecessor(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["predecessorCriteria"][1] = copy.deepcopy(
            contract["predecessorCriteria"][0]
        )
        self.assertRejected(contract, "PRD 003, AD 0006, ADR 0019")

    def test_rejects_non_repository_predecessor(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["predecessorCriteria"][0]["lane"] = "hosted_ci"
        contract["predecessorCriteria"][0]["result"] = "DEFER"
        contract["predecessorCriteria"][0]["limitation"] = "Not observed."
        contract["predecessorCriteria"][0]["retryTrigger"] = "Observe later."
        self.assertRejected(contract, "predecessor must be repository_static PASS")

    def test_rejects_missing_memory_layer_or_conflict_rule(self) -> None:
        missing = copy.deepcopy(self.fixture)
        missing["memoryLayers"].pop()
        self.assertRejected(missing, "four closed classes")

        no_conflict_rule = copy.deepcopy(self.fixture)
        del no_conflict_rule["memoryLayers"][0]["conflictHandling"]
        self.assertRejected(no_conflict_rule, "schema validation failed (required)")

        wrong_owner = copy.deepcopy(self.fixture)
        wrong_owner["memoryLayers"][0]["owner"] = "platform"
        self.assertRejected(wrong_owner, "memory layer ownership")

    def test_rejects_roster_count_drift(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["rosterSummary"]["adapterCount"] = 47
        self.assertRejected(contract, "exact 12/4/48")

    def test_rejects_model_mapping_readiness_drift(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["modelProfileSummary"]["mappingReady"] = 20
        contract["modelProfileSummary"]["mappingDeferred"] = 28
        self.assertRejected(contract, "model mapping-readiness summary differs")

    def test_rejects_ownerless_defer_in_each_summary_kind(self) -> None:
        mutations = (
            lambda item: item["rosterSummary"].__setitem__("retryTrigger", ""),
            lambda item: item["modelProfileSummary"].__setitem__("owner", ""),
            lambda item: item["qaEvidence"][1].__setitem__("owner", ""),
            lambda item: item["qaEvidence"][1].__setitem__("retryTrigger", ""),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                contract = copy.deepcopy(self.fixture)
                mutation(contract)
                self.assertRejected(contract, "schema validation failed (minLength)")

    def test_rejects_missing_or_reordered_external_lane_evidence(self) -> None:
        missing = copy.deepcopy(self.fixture)
        missing["qaEvidence"].pop(2)
        self.assertRejected(missing, "QA evidence lanes differ")

        reordered = copy.deepcopy(self.fixture)
        reordered["qaEvidence"][1], reordered["qaEvidence"][2] = (
            reordered["qaEvidence"][2],
            reordered["qaEvidence"][1],
        )
        self.assertRejected(reordered, "QA evidence lanes differ")

    def test_rejects_review_pass_with_findings(self) -> None:
        contract = copy.deepcopy(self.fixture)
        review = contract["reviewEvidence"]["requirements"]
        review.update(
            {
                "result": "PASS",
                "critical": 1,
                "limitation": None,
                "retryTrigger": None,
            }
        )
        self.assertRejected(contract, "PASS review retains findings")

    def test_rejects_forbidden_durable_data_keys(self) -> None:
        for key in (
            "token",
            "authPath",
            "body",
            "providerResponseBody",
            "promptTranscript",
            "env",
            "history",
            "shellHistory",
        ):
            with self.subTest(key=key):
                contract = copy.deepcopy(self.fixture)
                contract["handoff"][key] = "redacted"
                self.assertRejected(contract, "forbidden durable key")

        contract = copy.deepcopy(self.fixture)
        forbidden_key = "sk-" + "examplecredential123"
        contract["handoff"][forbidden_key] = "redacted"
        diagnostics = "\n".join(self.module.validate_contract(contract, self.schema))
        self.assertNotIn(forbidden_key, diagnostics)
        self.assertIn("secret-like durable key", diagnostics)

    def test_rejects_secret_like_durable_values(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["handoff"]["localMerge"] = "sk-" + "examplecredential123"
        self.assertRejected(contract, "secret-like durable value")

    def test_rejects_unknown_fields_under_closed_schema(self) -> None:
        contract = copy.deepcopy(self.fixture)
        contract["unexpected"] = True
        self.assertRejected(contract, "schema validation failed (additionalProperties)")

    def test_schema_diagnostics_do_not_disclose_rejected_values(self) -> None:
        contract = copy.deepcopy(self.fixture)
        sensitive = "sk-" + "examplecredential123"
        contract["handoff"]["localMerge"] = sensitive
        diagnostics = "\n".join(self.module.validate_contract(contract, self.schema))
        self.assertNotIn(sensitive, diagnostics)
        self.assertIn("secret-like durable value", diagnostics)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            self.module.parse_json_text(
                '{"schemaVersion":1,"schemaVersion":2}',
                "unit-test",
            )

    def test_input_boundary_rejects_symlink_and_non_regular_inputs(self) -> None:
        relative = PurePosixPath("nested/input.json")
        with TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            target = root / "target.json"
            target.write_text("{}\n", encoding="utf-8")
            (nested / "input.json").symlink_to(target)
            with self.assertRaisesRegex(ValueError, "cannot be read"):
                self.module._load_json(root, relative)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested" / "input.json").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "not a regular file"):
                self.module._load_json(root, relative)

        with TemporaryDirectory() as repository, TemporaryDirectory() as outside:
            root = Path(repository)
            outside_root = Path(outside)
            (outside_root / "input.json").write_text("{}\n", encoding="utf-8")
            (root / "nested").symlink_to(outside_root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "cannot be read"):
                self.module._load_json(root, relative)

    def test_input_boundary_rejects_symlink_root(self) -> None:
        with TemporaryDirectory() as directory:
            base = Path(directory)
            actual = base / "actual"
            actual.mkdir()
            link = base / "repository"
            link.symlink_to(actual, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "not a real directory"):
                self.module._load_json(link, PurePosixPath("input.json"))

    def test_repository_sources_are_digest_bound(self) -> None:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        read_regular_bytes = self.module._read_regular_bytes
        for row in contract["predecessorCriteria"]:
            predecessor_path = PurePosixPath(row["owner"])

            def read_with_drift(root: Path, path: PurePosixPath) -> bytes:
                source = read_regular_bytes(root, path)
                return source + b"\n" if path == predecessor_path else source

            with self.subTest(predecessor=predecessor_path), patch.object(
                self.module,
                "_read_regular_bytes",
                side_effect=read_with_drift,
            ):
                self.assertEqual(
                    self.module._validate_predecessor_sources(REPO_ROOT, contract),
                    [f"predecessor source digest differs: {predecessor_path}"],
                )

        for source_path, validator, expected in (
            (
                self.module.PROVIDER_SOURCE_PATH,
                self.module._validate_provider_source,
                "provider source digest differs",
            ),
            (
                self.module.MODEL_SOURCE_PATH,
                self.module._validate_model_source,
                "model source digest differs",
            ),
        ):
            with self.subTest(source_path=source_path):
                source_bytes = self.module._read_regular_bytes(REPO_ROOT, source_path)
                with patch.object(
                    self.module,
                    "_read_regular_bytes",
                    return_value=source_bytes + b"\n",
                ):
                    self.assertEqual(validator(REPO_ROOT, contract), [expected])

    def test_work108_predecessor_projection_accepts_only_exact_outer_identity(
        self,
    ) -> None:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        for row, expected in zip(
            contract["predecessorCriteria"],
            self.module.EXPECTED_PREDECESSORS,
            strict=True,
        ):
            owner = PurePosixPath(row["owner"])
            source = self.module._read_regular_bytes(REPO_ROOT, owner)
            projected = self.module._work108_predecessor_digest_payload(
                owner,
                source,
            )
            with self.subTest(owner=owner):
                self.assertIsNotNone(projected)
                self.assertEqual(
                    self.module.hashlib.sha256(projected).hexdigest(),
                    expected[4],
                )

            artifact_id = self.module.WORK108_PREDECESSOR_ARTIFACT_IDS[owner]
            exact_line = f'artifact_id: "{artifact_id}"\n'.encode("ascii")
            mutations = {
                "missing": source.replace(exact_line, b"", 1),
                "wrong": source.replace(exact_line, b'artifact_id: "ROGUE-999"\n', 1),
                "duplicate": source.replace(exact_line, exact_line * 2, 1),
                "payload-drift": source + b"\n",
            }
            for mutation, candidate in mutations.items():
                with self.subTest(owner=owner, mutation=mutation):
                    self.assertIsNone(
                        self.module._work108_predecessor_digest_payload(
                            owner,
                            candidate,
                        )
                    )


if __name__ == "__main__":
    unittest.main()
