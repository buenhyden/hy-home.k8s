#!/usr/bin/env python3
"""Focused tests for the Spec 044 model-fitness contract."""

from __future__ import annotations

import copy
import hashlib
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
PROVIDER_EVIDENCE_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/provider-runtime-evidence.schema.json"
)
PROVIDER_CONFIG_VALIDATOR_PATH = (
    REPOSITORY_ROOT / "scripts/validate-agent-provider-config.py"
)
EVALUATIONS_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-evaluations.json"
)
EVALUATIONS_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-evaluations.schema.json"
)
EVALUATIONS_VALIDATOR_PATH = (
    REPOSITORY_ROOT / "scripts/validate-agent-evaluations.py"
)
ADMISSION_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-roster-admission.json"
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
    PROVIDER_EVIDENCE_SCHEMA_PATH,
    PROVIDER_CONFIG_VALIDATOR_PATH,
    EVALUATIONS_PATH,
    EVALUATIONS_SCHEMA_PATH,
    EVALUATIONS_VALIDATOR_PATH,
    ADMISSION_PATH,
    HARNESS_PATH,
)
ROLE_IDS = (
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
ADAPTER_INPUTS = tuple(
    REPOSITORY_ROOT / path
    for role_id in ROLE_IDS
    for path in (
        f".agents/agents/{role_id}.md",
        f".claude/agents/{role_id}.md",
        f".codex/agents/{role_id}.toml",
        f".gemini/agents/{role_id}.md",
    )
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
    for source in (*GOVERNED_INPUTS, *ADAPTER_INPUTS):
        destination = root / source.relative_to(REPOSITORY_ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def canonical_digest(value) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def text_digest(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


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

    def test_production_contract_is_area004_ready_and_exact_12_by_4(self) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(
            counts,
            {
                "roles": 12,
                "providers": 4,
                "tuples": 48,
                "mappingReady": 21,
                "mappingDeferred": 27,
                "fitnessDeferred": 48,
                "thresholdDeferred": 48,
                "promotionDeferred": 48,
                "canaryDeferred": 48,
                "runtimeDeferred": 48,
            },
        )
        self.assertEqual(self.contract["contractVersion"], "1.1.0")
        self.assertEqual(self.contract["schemaVersion"], 2)
        self.assertEqual(
            self.contract["contractMode"],
            "repository-static-fitness-readiness",
        )
        self.assertEqual(self.contract["evidenceClass"], "repository-static")
        self.assertEqual(
            self.contract["lifecycleState"],
            "repository-static-fitness-ready",
        )
        for profile in self.contract["roleProfiles"]:
            for item in profile["providerTuples"]:
                decisions = item["decisions"]
                expected_mapping = (
                    "PASS"
                    if item["providerId"] == "local"
                    or (
                        item["providerId"] == "claude"
                        and profile["riskTier"] == "high"
                    )
                    else "DEFER"
                )
                self.assertEqual(
                    decisions["mappingReadiness"],
                    expected_mapping,
                )
                self.assertEqual(decisions["fitness"], "DEFER")
                self.assertEqual(decisions["promotion"], "DEFER")
                self.assertEqual(decisions["canary"], "DEFER")
                self.assertEqual(decisions["runtime"], "DEFER")
                self.assertEqual(
                    item["evaluation"]["baselineMetricsDigest"], "DEFER"
                )
                self.assertEqual(
                    item["evaluation"]["candidateMetricsDigest"], "DEFER"
                )
                self.assertEqual(
                    item["evaluation"]["thresholdResult"], "DEFER"
                )

    def test_current_only_candidate_mapping_pass_fails_closed(self) -> None:
        mutated = self.contract_copy()
        claude_worker = mutated["providers"][1]["roleClassCandidates"][1]
        claude_worker["mappingReadiness"] = "PASS"
        code_reviewer = mutated["roleProfiles"][1]["providerTuples"][1]
        code_reviewer["decisions"]["mappingReadiness"] = "PASS"
        self.assert_rule(mutated, "AREA-FIT-MAPPING")

    def test_unknown_and_cross_provider_source_ids_fail_closed(self) -> None:
        cases = (
            ("unknown-provider-source", "AREA-FIT-SOURCE-ID"),
            ("codex-release-0-144-1", "AREA-FIT-SOURCE-ALIAS"),
        )
        for source_id, expected_rule in cases:
            with self.subTest(source_id=source_id):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    copy_governed_inputs(root)
                    evidence_path = root / PROVIDER_EVIDENCE_PATH.relative_to(
                        REPOSITORY_ROOT
                    )
                    evidence = json.loads(
                        evidence_path.read_text(encoding="utf-8")
                    )
                    evidence["providers"][1]["modelCandidates"][1][
                        "sourceIds"
                    ] = [source_id]
                    evidence_path.write_text(
                        json.dumps(evidence, indent=2) + "\n",
                        encoding="utf-8",
                    )

                    contract_path = root / CONTRACT_PATH.relative_to(
                        REPOSITORY_ROOT
                    )
                    contract = json.loads(
                        contract_path.read_text(encoding="utf-8")
                    )
                    contract["providers"][1]["roleClassCandidates"][1][
                        "sourceIds"
                    ] = [source_id]
                    for profile in contract["roleProfiles"]:
                        if profile["riskTier"] == "standard":
                            claude_tuple = profile["providerTuples"][1]
                            claude_tuple["sourceIds"] = [source_id]
                    contract_path.write_text(
                        json.dumps(contract, indent=2) + "\n",
                        encoding="utf-8",
                    )

                    with self.assertRaises(
                        self.validator.ModelFitnessError
                    ) as raised:
                        self.validator.validate_contract(root)
                    self.assertEqual(raised.exception.code, expected_rule)

    def test_area003_scenario_digest_tamper_fails_before_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            copy_governed_inputs(root)
            evaluations_path = root / EVALUATIONS_PATH.relative_to(
                REPOSITORY_ROOT
            )
            evaluations = json.loads(
                evaluations_path.read_text(encoding="utf-8")
            )
            records = evaluations["corpusManifest"]["records"]
            records[0]["scenarioSummary"] += " tampered"
            evaluations["corpusManifest"]["manifestDigest"] = canonical_digest(
                records
            )
            evaluations_path.write_text(
                json.dumps(evaluations, indent=2) + "\n",
                encoding="utf-8",
            )

            contract_path = root / CONTRACT_PATH.relative_to(REPOSITORY_ROOT)
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            for binding in contract["evaluationBindings"]:
                binding["corpusManifestDigest"] = evaluations[
                    "corpusManifest"
                ]["manifestDigest"]
            contract_path.write_text(
                json.dumps(contract, indent=2) + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-FIT-MANIFEST")

    def test_area003_role_fixture_manifest_tamper_fails_before_binding(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            copy_governed_inputs(root)
            evaluations_path = root / EVALUATIONS_PATH.relative_to(
                REPOSITORY_ROOT
            )
            evaluations = json.loads(
                evaluations_path.read_text(encoding="utf-8")
            )
            records = evaluations["corpusManifest"]["records"]
            records[0]["scenarioSummary"] += " tampered"
            records[0]["inputDigest"] = text_digest(
                records[0]["scenarioSummary"]
            )
            evaluations["corpusManifest"]["manifestDigest"] = canonical_digest(
                records
            )
            evaluations_path.write_text(
                json.dumps(evaluations, indent=2) + "\n",
                encoding="utf-8",
            )

            contract_path = root / CONTRACT_PATH.relative_to(REPOSITORY_ROOT)
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            for binding in contract["evaluationBindings"]:
                binding["corpusManifestDigest"] = evaluations[
                    "corpusManifest"
                ]["manifestDigest"]
            contract_path.write_text(
                json.dumps(contract, indent=2) + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-FIT-MANIFEST")

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
            copy_governed_inputs(root)
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

    def test_spec042_source_set_and_exact_utc_cutoff_fail_closed(self) -> None:
        def same_day_after_cutoff(ledger) -> None:
            ledger[0]["sourceDate"] = "2026-07-10"
            ledger[0]["publishedAtUtc"] = "2026-07-10T01:00:01Z"

        def cutoff_day_without_timestamp(ledger) -> None:
            ledger[0]["sourceDate"] = "2026-07-10"
            ledger[0]["publishedAtUtc"] = None

        def publication_date_mismatch(ledger) -> None:
            ledger[0]["publishedAtUtc"] = "2026-07-08T23:59:59Z"

        def extra_source(ledger) -> None:
            extra = copy.deepcopy(ledger[-1])
            extra["id"] = "extra-source-new-id"
            ledger.append(extra)

        def missing_source(ledger) -> None:
            ledger.pop()

        cases = (
            (
                "same-day-after-cutoff",
                same_day_after_cutoff,
                "AREA-FIT-SOURCE-CLASSIFICATION",
            ),
            (
                "cutoff-day-without-timestamp",
                cutoff_day_without_timestamp,
                "AREA-FIT-SOURCE-CLASSIFICATION",
            ),
            (
                "publication-date-mismatch",
                publication_date_mismatch,
                "AREA-FIT-SOURCE-CLASSIFICATION",
            ),
            ("extra-source", extra_source, "AREA-FIT-SOURCE-ID"),
            ("missing-source", missing_source, "AREA-FIT-SOURCE-ID"),
        )
        for name, mutate, expected_rule in cases:
            with self.subTest(case=name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    copy_governed_inputs(root)
                    evidence_path = (
                        root
                        / PROVIDER_EVIDENCE_PATH.relative_to(REPOSITORY_ROOT)
                    )
                    evidence = json.loads(
                        evidence_path.read_text(encoding="utf-8")
                    )
                    mutate(evidence["sourceLedger"])
                    evidence_path.write_text(
                        json.dumps(evidence, indent=2) + "\n",
                        encoding="utf-8",
                    )

                    with self.assertRaises(
                        self.validator.ModelFitnessError
                    ) as raised:
                        self.validator.validate_contract(root)
                    self.assertEqual(raised.exception.code, expected_rule)

    def test_provider_source_alias_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            copy_governed_inputs(root)
            evidence_path = root / PROVIDER_EVIDENCE_PATH.relative_to(
                REPOSITORY_ROOT
            )
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence["providers"][1]["modelCandidates"][0]["sourceIds"] = [
                "codex-config-reference-current"
            ]
            evidence_path.write_text(
                json.dumps(evidence, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-FIT-SOURCE-ALIAS")

    def test_area003_suite_source_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            copy_governed_inputs(root)
            evaluations_path = root / EVALUATIONS_PATH.relative_to(
                REPOSITORY_ROOT
            )
            evaluations = json.loads(
                evaluations_path.read_text(encoding="utf-8")
            )
            evaluations["roleSuites"][0]["suiteVersion"] = "2.0.0"
            evaluations_path.write_text(
                json.dumps(evaluations, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(
                raised.exception.code,
                "AREA-FIT-EVALUATION-SOURCE",
            )

    def test_area003_rollback_sources_cannot_be_weakened(self) -> None:
        cases = (
            (
                ADMISSION_PATH,
                lambda data: data["candidates"][0]["rollback"].update(
                    {"state": "not-armed"}
                ),
            ),
            (
                EVALUATIONS_PATH,
                lambda data: data["rollbackRecords"][0].update(
                    {"status": "not-armed"}
                ),
            ),
        )
        for source, mutate in cases:
            with self.subTest(path=source.relative_to(REPOSITORY_ROOT)):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    copy_governed_inputs(root)
                    target = root / source.relative_to(REPOSITORY_ROOT)
                    data = json.loads(target.read_text(encoding="utf-8"))
                    mutate(data)
                    target.write_text(
                        json.dumps(data, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    with self.assertRaises(
                        self.validator.ModelFitnessError
                    ) as raised:
                        self.validator.validate_contract(root)
                    self.assertEqual(
                        raised.exception.code,
                        "AREA-FIT-ROLLBACK-SOURCE",
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

    def test_adapter_symlink_is_rejected_before_model_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "repository"
            copy_governed_inputs(root)
            relative = Path(".codex/agents/supervisor.toml")
            adapter = root / relative
            outside = base / "outside-adapter.toml"
            outside.write_text(
                'model = "unverified"\nmodel_reasoning_effort = "high"\n',
                encoding="utf-8",
            )
            adapter.unlink()
            adapter.symlink_to(outside)
            with self.assertRaises(
                self.validator.ModelFitnessError
            ) as raised:
                self.validator.validate_contract(root)
            self.assertEqual(raised.exception.code, "AREA-FIT-INPUT")
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
            copy_governed_inputs(root)
            contract_path = root / CONTRACT_PATH.relative_to(REPOSITORY_ROOT)
            contract_path.unlink()
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
            "gemini-cli-family-unresolved",
        )
        self.assertIn(
            "does-not-prove-cli-resolution",
            providers["gemini"]["apiVsCliBoundary"],
        )
        self.assertEqual(
            self.contract["authorityBoundaries"][
                "providerEvidenceGranularity"
            ],
            "two-role-class-candidates-per-provider",
        )
        self.assertEqual(
            self.contract["authorityBoundaries"][
                "roleSpecificRuntimeEvidence"
            ],
            "DEFER",
        )

    def test_gemini_native_surface_fails_closed_without_fabricated_model(
        self,
    ) -> None:
        candidates = self.contract["providers"][3]["roleClassCandidates"]
        for candidate in candidates:
            self.assertIn("unresolved", candidate["candidateModel"])
            self.assertEqual(candidate["mappingReadiness"], "DEFER")
            self.assertEqual(
                candidate["cutoffConfidence"],
                "mixed-cutoff-current-unresolved",
            )
            self.assertEqual(candidate["runtimeResolution"], "DEFER")
        for profile in self.contract["roleProfiles"]:
            gemini_tuple = next(
                item
                for item in profile["providerTuples"]
                if item["providerId"] == "gemini"
            )
            self.assertEqual(
                gemini_tuple["incumbentModel"],
                "not-configurable-on-native-surface",
            )
            self.assertEqual(gemini_tuple["observedValue"], "DEFER")
            self.assertEqual(
                gemini_tuple["configPath"],
                f".gemini/agents/{profile['roleId']}.md#frontmatter.model",
            )
            self.assertEqual(
                gemini_tuple["fallbackPolicy"],
                "fail-closed-no-configurable-incumbent",
            )
            self.assertEqual(gemini_tuple["fallbackTarget"], "fail-closed")

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
        self.assertEqual(
            policy["thresholds"],
            {
                "qualityMinimum": 0.9,
                "safetyMinimum": 1,
                "costMaximumUsd": 1,
                "latencyMaximumMs": 120000,
            },
        )
        self.assertTrue(policy["sameSuiteRequired"])
        self.assertEqual(
            policy["validatorPassMeaning"],
            "mapping-readiness-only",
        )
        self.assertEqual(
            policy["unobservedMetricPolicy"],
            "remain-DEFER-never-synthesize",
        )
        self.assertEqual(
            self.contract["rollbackAuthority"]["state"],
            "armed-not-executed",
        )
        for profile in self.contract["roleProfiles"]:
            for item in profile["providerTuples"]:
                self.assertFalse(item["silentFallbackAllowed"])

    def test_all_evaluation_threshold_fields_are_exact_and_fail_closed(
        self,
    ) -> None:
        cases = (
            ("qualityMinimum", 0.89),
            ("safetyMinimum", 0.99),
            ("costMaximumUsd", 1.01),
            ("latencyMaximumMs", 120001),
        )
        for field, weakened_value in cases:
            with self.subTest(field=field):
                mutated = self.contract_copy()
                mutated["evaluationPolicy"]["thresholds"][
                    field
                ] = weakened_value
                self.assert_rule(mutated, "AREA-FIT-THRESHOLD")

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
