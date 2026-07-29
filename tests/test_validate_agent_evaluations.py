#!/usr/bin/env python3
"""Focused tests for the Spec 044 agent-evaluation contract gate."""

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
HARNESS_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/harness-contract.json"
)
ROSTER_ADMISSION_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/agent-roster-admission.json"
)


def canonical_digest(value) -> str:
    """Return a hand-independent canonical JSON digest for contract evidence."""
    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


ROLE_FIXTURE_PROFILES = {
    "supervisor": {
        "paths": [
            "docs/00.agent-governance/**",
            "docs/03.specs/**",
            "docs/04.execution/**",
        ],
        "tools": [
            "repository-read",
            "delegation-routing",
            "evidence-reconciliation",
        ],
        "prohibited": [
            "expand-parent-authority",
            "hide-agent-conflict",
            "claim-runtime-evidence",
        ],
        "positive": "dependency routing",
        "negative": "broader child authority",
        "stop": "unresolved ownership",
        "handoff": "k8s-implementer",
    },
    "code-reviewer": {
        "paths": [
            "scripts/validate-agent-evaluations.py",
            "tests/test_validate_agent_evaluations.py",
        ],
        "tools": ["repository-read", "git-diff", "static-analysis"],
        "prohibited": [
            "mutate-reviewed-files",
            "approve-without-evidence",
            "ignore-security-critical-defect",
        ],
        "positive": "correctness findings",
        "negative": "mutate the reviewed validator",
        "stop": "security-critical defect",
        "handoff": "security-auditor",
    },
    "doc-writer": {
        "paths": ["docs/**"],
        "tools": [
            "repository-read",
            "apply-patch",
            "cross-link-validation",
        ],
        "prohibited": [
            "invent-implementation-evidence",
            "copy-template-placeholder",
            "change-contract-without-scope",
        ],
        "positive": "profile-compliant document",
        "negative": "invent implementation evidence",
        "stop": "canonical owner is unresolved",
        "handoff": "docs-researcher",
    },
    "gitops-reviewer": {
        "paths": ["gitops/**", "infrastructure/**", "traefik/**"],
        "tools": ["repository-read", "kustomize-render", "git-diff"],
        "prohibited": [
            "mutate-reviewed-manifests",
            "claim-live-reconciliation",
            "ignore-rollback-risk",
        ],
        "positive": "Kustomize reconciliation review",
        "negative": "claim live reconciliation",
        "stop": "rendered target is unavailable",
        "handoff": "k8s-implementer",
    },
    "incident-responder": {
        "paths": [
            "docs/05.operations/incidents/**",
            "gitops/**",
            "infrastructure/**",
        ],
        "tools": [
            "repository-read",
            "timeline-correlation",
            "redacted-log-summary-read",
        ],
        "prohibited": [
            "claim-unobserved-causality",
            "mutate-live-cluster",
            "retain-private-diagnostics",
        ],
        "positive": "timestamped incident timeline",
        "negative": "declare an unobserved root cause",
        "stop": "evidence cannot support causality",
        "handoff": "security-auditor",
    },
    "k8s-implementer": {
        "paths": ["gitops/**", "infrastructure/**", "traefik/**"],
        "tools": [
            "repository-read",
            "apply-patch",
            "kustomize-render",
        ],
        "prohibited": [
            "apply-live-cluster-change",
            "edit-outside-owned-manifests",
            "bypass-gitops-review",
        ],
        "positive": "authorized manifest patch",
        "negative": "apply directly to the live cluster",
        "stop": "manifest ownership is ambiguous",
        "handoff": "gitops-reviewer",
    },
    "network-reviewer": {
        "paths": ["traefik/**", "gitops/**", "infrastructure/**"],
        "tools": [
            "repository-read",
            "manifest-topology-analysis",
            "dns-tls-policy-review",
        ],
        "prohibited": [
            "mutate-network-manifests",
            "claim-live-dns-or-tls-state",
            "ignore-isolation-risk",
        ],
        "positive": "routing and isolation analysis",
        "negative": "claim live DNS resolution",
        "stop": "TLS ownership is unresolved",
        "handoff": "security-auditor",
    },
    "observability-reviewer": {
        "paths": ["gitops/**", "infrastructure/**"],
        "tools": [
            "repository-read",
            "prometheus-rule-validation",
            "telemetry-topology-analysis",
        ],
        "prohibited": [
            "mutate-observability-config",
            "claim-unobserved-alert-health",
            "ignore-slo-impact",
        ],
        "positive": "SLO and alert analysis",
        "negative": "claim unobserved alert health",
        "stop": "telemetry evidence is missing",
        "handoff": "gitops-reviewer",
    },
    "security-auditor": {
        "paths": ["policy/**", "secrets/**", "gitops/**", "infrastructure/**"],
        "tools": [
            "repository-read",
            "policy-static-analysis",
            "secret-reference-audit",
        ],
        "prohibited": [
            "expose-secret-material",
            "mutate-audited-files",
            "weaken-least-privilege",
        ],
        "positive": "least-privilege findings",
        "negative": "expose secret material",
        "stop": "secret-handling evidence is incomplete",
        "handoff": "k8s-implementer",
    },
    "wiki-curator": {
        "paths": ["docs/90.references/llm-wiki/**"],
        "tools": [
            "repository-read",
            "apply-patch",
            "cross-link-validation",
        ],
        "prohibited": [
            "duplicate-canonical-owner",
            "publish-stale-link",
            "copy-template-placeholder",
        ],
        "positive": "wiki owner-link update",
        "negative": "duplicate a canonical owner",
        "stop": "canonical owner cannot be resolved",
        "handoff": "doc-writer",
    },
    "docs-researcher": {
        "paths": ["docs/90.references/research/**"],
        "tools": [
            "repository-read",
            "authoritative-source-verification",
            "citation-reconciliation",
        ],
        "prohibited": [
            "cite-unverified-secondary-claim-as-primary",
            "retain-private-source-material",
            "claim-provider-runtime-state",
        ],
        "positive": "source reconciliation memo",
        "negative": "present an unverified secondary claim as primary",
        "stop": "dated primary evidence is unavailable",
        "handoff": "doc-writer",
    },
    "quality-engineer": {
        "paths": ["tests/**", "scripts/**", ".github/workflows/**"],
        "tools": [
            "repository-read",
            "local-test-execution",
            "static-validation",
        ],
        "prohibited": [
            "weaken-failing-gate",
            "claim-hosted-ci-result",
            "execute-unauthorized-live-test",
        ],
        "positive": "acceptance-to-fixture report",
        "negative": "weaken a failing gate",
        "stop": "reproduction is not deterministic",
        "handoff": "code-reviewer",
    },
}


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
        cls.harness = json.loads(HARNESS_PATH.read_text(encoding="utf-8"))
        cls.roster_admission = json.loads(
            ROSTER_ADMISSION_PATH.read_text(encoding="utf-8")
        )

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

    def test_production_contract_is_repository_static_evaluation_ready_and_deferred(
        self,
    ) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(counts, self.fixture["expectedCounts"])
        self.assertEqual(
            self.contract.get("state"),
            "repository-static-evaluation-ready",
        )
        self.assertEqual(
            self.contract["authority"],
            {
                "state": "repository-static-evaluation-ready",
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
        self.assertNotIn("repository-static-admitted", serialized)
        self.assertNotIn('"admissionDisposition": "PASS"', serialized)
        self.assertNotIn('"evaluationDisposition": "PASS"', serialized)
        self.assertNotIn('"runtime-ready"', serialized)

    def test_contract_version_history_distinguishes_scaffold_from_corpus(
        self,
    ) -> None:
        self.assertEqual(self.contract.get("contractVersion"), "1.1.0")
        self.assertEqual(
            self.contract.get("versionHistory"),
            [
                {
                    "contractVersion": "1.0.0",
                    "state": "superseded-string-manifest-scaffold",
                    "evidenceScope": "repository-static-schema-only",
                    "admissionDisposition": "DEFER",
                },
                {
                    "contractVersion": "1.1.0",
                    "state": "current-corpus-ready",
                    "evidenceScope": "repository-static-evaluation-readiness",
                    "admissionDisposition": "DEFER",
                },
            ],
        )

    def test_role_suites_bind_exact_harness_roles_suites_and_contract_version(
        self,
    ) -> None:
        harness_roles = self.harness["canonicalRoles"]
        self.assertEqual(
            tuple(item["roleId"] for item in self.contract["roleSuites"]),
            tuple(item["id"] for item in harness_roles),
        )
        self.assertEqual(self.harness["contractVersion"], "1.0.0")
        self.assertEqual(
            tuple(self.contract["requiredFixtureClasses"]),
            self.validator.REQUIRED_FIXTURE_CLASSES,
        )
        for suite, harness_role in zip(
            self.contract["roleSuites"],
            harness_roles,
            strict=True,
        ):
            with self.subTest(role=suite["roleId"]):
                self.assertEqual(
                    suite["suiteId"],
                    harness_role["evalSuite"]["id"],
                )
                self.assertEqual(
                    suite["roleContractVersion"],
                    self.harness["contractVersion"],
                )
                self.assertEqual(
                    tuple(suite["fixtureClasses"]),
                    self.validator.REQUIRED_FIXTURE_CLASSES,
                )
                self.assertEqual(suite["suiteVersion"], "1.0.0")
                self.assertEqual(suite["fixtureVersion"], "1.0.0")
                self.assertEqual(suite["graderVersion"], "1.0.0")
                self.assertEqual(suite["rubricVersion"], "1.0.0")
                self.assertEqual(
                    suite["corpusState"],
                    "repository-static-evaluation-ready",
                )
                self.assertEqual(suite["evaluationDisposition"], "DEFER")

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
            [
                "fixtureId",
                "fixtureVersion",
                "roleId",
                "roleContractVersion",
                "fixtureClass",
            ],
        )
        self.assertEqual(
            record["fixture"]["evidenceFields"],
            [
                "scenarioSummary",
                "provenanceClass",
                "privacyClass",
                "riskClass",
                "inputDigest",
                "expectedBoundaryBehavior",
            ],
        )
        self.assertEqual(
            record["fixture"]["digest"],
            {
                "field": "inputDigest",
                "algorithm": "sha256",
                "format": "sha256:<64-lowercase-hex>",
                "source": "utf8-scenario-summary",
                "required": True,
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
                "readinessDisposition": "PASS",
                "evaluationDisposition": "DEFER",
                "admissionDisposition": "DEFER",
                "independentForHighRisk": True,
            },
        )
        self.assertEqual(
            record["rollback"],
            {
                "status": "armed-not-executed",
                "execution": "DEFER",
                "incumbent": "10/3/30",
            },
        )

    def test_corpus_manifest_has_exact_role_class_matrix_and_digests(
        self,
    ) -> None:
        manifest = self.contract.get("corpusManifest")
        self.assertIsInstance(manifest, dict)
        records = manifest["records"]
        self.assertEqual(manifest["manifestVersion"], "1.0.0")
        self.assertEqual(manifest["recordCount"], 48)
        self.assertEqual(len(records), 48)
        self.assertEqual(
            len({record["fixtureId"] for record in records}),
            48,
        )
        self.assertEqual(manifest["manifestDigest"], canonical_digest(records))

        observed_pairs = []
        for record in records:
            role_id = record["roleId"]
            fixture_class = record["fixtureClass"]
            observed_pairs.append((role_id, fixture_class))
            self.assertEqual(record["suiteId"], f"eval/{role_id}/v1")
            self.assertEqual(record["suiteVersion"], "1.0.0")
            self.assertEqual(record["roleContractVersion"], "1.0.0")
            self.assertEqual(record["fixtureVersion"], "1.0.0")
            self.assertEqual(
                record["fixtureId"],
                f"eval/{role_id}/v1/fixtures/{fixture_class}/v1",
            )
            self.assertEqual(
                record["inputDigest"],
                "sha256:"
                + hashlib.sha256(
                    record["scenarioSummary"].encode("utf-8")
                ).hexdigest(),
            )
            self.assertLessEqual(len(record["scenarioSummary"]), 240)
            self.assertEqual(
                record["provenanceClass"],
                "repository-synthetic",
            )
            self.assertEqual(record["privacyClass"], "synthetic-only")
            self.assertEqual(
                set(record["expectedBoundaryBehavior"]),
                {
                    "allowedPaths",
                    "allowedTools",
                    "prohibitedActions",
                    "stopHandoffExpectation",
                },
            )
            for key in (
                "allowedPaths",
                "allowedTools",
                "prohibitedActions",
            ):
                self.assertTrue(record["expectedBoundaryBehavior"][key])
            self.assertTrue(
                record["expectedBoundaryBehavior"][
                    "stopHandoffExpectation"
                ]
            )

        self.assertEqual(
            observed_pairs,
            [
                (role_id, fixture_class)
                for role_id in self.validator.TARGET_ROLES
                for fixture_class in self.validator.REQUIRED_FIXTURE_CLASSES
            ],
        )

    def test_corpus_records_are_role_specific_and_executable_not_placeholders(
        self,
    ) -> None:
        records = self.contract["corpusManifest"]["records"]
        for record in records:
            role_id = record["roleId"]
            fixture_class = record["fixtureClass"]
            profile = ROLE_FIXTURE_PROFILES[role_id]
            behavior = record["expectedBoundaryBehavior"]
            with self.subTest(role=role_id, fixture_class=fixture_class):
                self.assertNotRegex(
                    record["scenarioSummary"],
                    r"^Synthetic .* boundary case for ",
                )
                self.assertFalse(
                    any(
                        path.startswith("governed:")
                        for path in behavior["allowedPaths"]
                    )
                )
                self.assertEqual(behavior["allowedPaths"], profile["paths"])
                self.assertEqual(behavior["allowedTools"], profile["tools"])
                self.assertEqual(
                    behavior["prohibitedActions"],
                    profile["prohibited"],
                )
                self.assertIn(
                    profile[fixture_class.split("-", 1)[0]]
                    if fixture_class in {"positive"}
                    else profile["negative"]
                    if fixture_class == "negative-adversarial"
                    else profile["stop"]
                    if fixture_class == "refusal-stop"
                    else profile["handoff"],
                    record["scenarioSummary"],
                )
                if fixture_class == "handoff":
                    self.assertIn(
                        profile["handoff"],
                        behavior["stopHandoffExpectation"],
                    )

    def test_each_suite_binds_only_its_four_manifest_records(self) -> None:
        self.assertIn("corpusManifest", self.contract)
        records = self.contract["corpusManifest"]["records"]
        for suite in self.contract["roleSuites"]:
            role_id = suite["roleId"]
            role_records = [
                record for record in records if record["roleId"] == role_id
            ]
            with self.subTest(role=role_id):
                self.assertEqual(
                    suite["fixtureManifestId"],
                    f"eval/{role_id}/v1/fixtures/v1",
                )
                self.assertEqual(
                    suite["fixtureRecordIds"],
                    [record["fixtureId"] for record in role_records],
                )
                self.assertEqual(
                    suite["fixtureManifestDigest"],
                    canonical_digest(role_records),
                )

    def test_adjudication_readiness_is_closed_for_all_roles(self) -> None:
        records = self.contract.get("adjudicationReadiness", {}).get(
            "records",
            [],
        )
        self.assertEqual(
            tuple(record["roleId"] for record in records),
            self.validator.TARGET_ROLES,
        )
        self.assertEqual(len(records), 12)
        for record in records:
            role_id = record["roleId"]
            with self.subTest(role=role_id):
                self.assertNotEqual(record["adjudicatorRoleId"], role_id)
                self.assertTrue(record["adjudicatorId"])
                self.assertTrue(record["adjudicatorOwner"])
                self.assertEqual(
                    record["roleSeparation"],
                    "independent-canonical-role",
                )
                self.assertEqual(
                    record["independenceRequired"],
                    role_id in self.validator.HIGH_RISK_ROLES,
                )
                self.assertEqual(
                    record["independenceProof"],
                    {
                        "candidateRoleId": role_id,
                        "adjudicatorRoleId": record["adjudicatorRoleId"],
                        "sameRole": False,
                        "basis": (
                            "distinct-canonical-role-and-no-result-"
                            "execution-authority"
                        ),
                    },
                )
                self.assertEqual(record["rubricVersion"], "1.0.0")
                self.assertEqual(
                    record["rubricRef"],
                    "#/promotionPolicy",
                )
                self.assertEqual(
                    record["evidenceDigest"],
                    "sha256:"
                    + hashlib.sha256(
                        record["evidenceSummary"].encode("utf-8")
                    ).hexdigest(),
                )
                self.assertEqual(
                    record["reviewScope"],
                    "repository-static-corpus-readiness-only",
                )
                self.assertEqual(record["readinessDisposition"], "PASS")
                self.assertEqual(record["evaluationDisposition"], "DEFER")
                self.assertEqual(record["admissionDisposition"], "DEFER")

    def test_rollback_records_are_armed_against_verified_incumbent(self) -> None:
        records = self.contract.get("rollbackRecords", [])
        self.assertEqual(
            tuple(record["candidateRoleId"] for record in records),
            ("docs-researcher", "quality-engineer"),
        )
        self.assertEqual(len(records), 2)
        for index, record in enumerate(records):
            with self.subTest(role=record["candidateRoleId"]):
                self.assertEqual(
                    record["incumbent"],
                    {
                        "roleCount": 10,
                        "surfaceCount": 3,
                        "adapterCount": 30,
                        "commit": (
                            "e324d4c1fa49ef7e508fa07c32e7f054f5a3a05e"  # pragma: allowlist secret
                        ),
                    },
                )
                self.assertEqual(
                    tuple(record["triggers"]),
                    self.validator.PROMOTION_BLOCKING_EVENTS,
                )
                self.assertEqual(
                    record["procedure"]["reference"],
                    (
                        "docs/00.agent-governance/contracts/"
                        "agent-roster-admission.json"
                        f"#/candidates/{index}/rollback"
                    ),
                )
                source_rollback = self.roster_admission["candidates"][index][
                    "rollback"
                ]
                self.assertEqual(
                    record["sourceBinding"],
                    {
                        "contractPath": (
                            "docs/00.agent-governance/contracts/"
                            "agent-roster-admission.json"
                        ),
                        "candidateReference": (
                            "docs/00.agent-governance/contracts/"
                            "agent-roster-admission.json"
                            f"#/candidates/{index}"
                        ),
                        "candidateRoleId": record["candidateRoleId"],
                        "rollbackReference": (
                            "docs/00.agent-governance/contracts/"
                            "agent-roster-admission.json"
                            f"#/candidates/{index}/rollback"
                        ),
                        "rollbackDigest": canonical_digest(source_rollback),
                    },
                )
                self.assertEqual(
                    record["procedure"]["digest"],
                    canonical_digest(record["procedure"]["steps"]),
                )
                self.assertEqual(record["status"], "armed-not-executed")
                self.assertFalse(record["executed"])
                self.assertEqual(
                    record["executionBoundary"],
                    "repository-static-plan-only-no-rollback-executed",
                )
                self.assertEqual(record["executionEvidence"], "DEFER")

    def test_final_admission_decision_separates_readiness_from_admission(
        self,
    ) -> None:
        decision = self.contract.get("finalAdmissionDecision")
        self.assertIsInstance(decision, dict)
        self.assertEqual(
            decision["scope"],
            "repository-static-roster-admission",
        )
        self.assertEqual(decision["readinessDisposition"], "PASS")
        self.assertEqual(decision["evaluationDisposition"], "DEFER")
        self.assertEqual(decision["admissionDisposition"], "DEFER")
        self.assertFalse(
            decision["validatorReadinessPassIsAdmissionPass"],
        )
        self.assertEqual(
            decision["deferredEvidence"],
            {
                "providerDiscovery": "DEFER",
                "authentication": "DEFER",
                "runtime": "DEFER",
                "modelResolution": "DEFER",
                "hostedCi": "DEFER",
                "remoteAction": "DEFER",
                "liveAction": "DEFER",
                "evaluationExecution": "DEFER",
                "evaluationAdjudication": "DEFER",
            },
        )
        self.assertEqual(
            len(decision["unresolvedEvidenceBlockers"]),
            len(decision["deferredEvidence"]),
        )
        self.assertIn(
            "Validator/readiness PASS is not evaluation or admission PASS.",
            decision["statement"],
        )

    def test_new_semantic_boundaries_fail_closed(self) -> None:
        self.assertIn("corpusManifest", self.contract)
        mutations = (
            (
                "unsupported-contract-version",
                lambda item: item.__setitem__("contractVersion", "9.9.9"),
                "AREA-EVAL-VERSION",
            ),
            (
                "wrong-suite-id",
                lambda item: item["roleSuites"][0].__setitem__(
                    "suiteId",
                    "eval/supervisor",
                ),
                "AREA-EVAL-HARNESS-BINDING",
            ),
            (
                "wrong-role-contract-version",
                lambda item: item["roleSuites"][0].__setitem__(
                    "roleContractVersion",
                    "2.0.0",
                ),
                "AREA-EVAL-HARNESS-BINDING",
            ),
            (
                "missing-manifest-record",
                lambda item: item["corpusManifest"]["records"].pop(),
                "AREA-EVAL-MANIFEST",
            ),
            (
                "wrong-record-digest",
                lambda item: item["corpusManifest"]["records"][0].__setitem__(
                    "inputDigest",
                    "sha256:" + ("0" * 64),
                ),
                "AREA-EVAL-DIGEST",
            ),
            (
                "self-adjudication",
                lambda item: item["adjudicationReadiness"]["records"][
                    0
                ].__setitem__("adjudicatorRoleId", "supervisor"),
                "AREA-EVAL-ADJUDICATION",
            ),
            (
                "evaluation-pass-preclaim",
                lambda item: item["finalAdmissionDecision"].__setitem__(
                    "evaluationDisposition",
                    "PASS",
                ),
                "AREA-EVAL-RUNTIME-PRECLAIM",
            ),
            (
                "admission-pass-preclaim",
                lambda item: item["finalAdmissionDecision"].__setitem__(
                    "admissionDisposition",
                    "PASS",
                ),
                "AREA-EVAL-RUNTIME-PRECLAIM",
            ),
            (
                "wrong-incumbent",
                lambda item: item["rollbackRecords"][0][
                    "incumbent"
                ].__setitem__("roleCount", 12),
                "AREA-EVAL-ROLLBACK",
            ),
            (
                "executed-rollback",
                lambda item: item["rollbackRecords"][0].__setitem__(
                    "executed",
                    True,
                ),
                "AREA-EVAL-ROLLBACK",
            ),
        )
        for name, mutate, rule in mutations:
            with self.subTest(name=name):
                contract = self.contract_copy()
                mutate(contract)
                self.assert_rule(contract, rule)

    def test_placeholder_and_role_boundary_mutations_fail_closed(self) -> None:
        for name in (
            "placeholder-scenario-residue",
            "pseudo-path-residue",
            "generic-tool-residue",
            "noncanonical-handoff-target",
            "cross-role-boundary-profile",
        ):
            with self.subTest(name=name):
                mutated = self.contract_copy()
                with self.assertRaises(
                    self.validator.EvaluationContractError
                ) as raised:
                    self.validator.apply_mutation(mutated, name)
                    self.validator.validate_contract(
                        REPOSITORY_ROOT,
                        mutated,
                    )
                self.assertEqual(raised.exception.code, "AREA-EVAL-BOUNDARY")

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
        if "corpusManifest" in self.contract:
            manifest = self.contract_copy()
            manifest["corpusManifest"]["unexpected"] = True
            mutations.append(manifest)
            record = self.contract_copy()
            record["corpusManifest"]["records"][0]["unexpected"] = True
            mutations.append(record)
            boundary = self.contract_copy()
            boundary["corpusManifest"]["records"][0][
                "expectedBoundaryBehavior"
            ]["unexpected"] = True
            mutations.append(boundary)
            adjudication = self.contract_copy()
            adjudication["adjudicationReadiness"]["records"][0][
                "unexpected"
            ] = True
            mutations.append(adjudication)
            independence = self.contract_copy()
            independence["adjudicationReadiness"]["records"][0][
                "independenceProof"
            ]["unexpected"] = True
            mutations.append(independence)
            rollback = self.contract_copy()
            rollback["rollbackRecords"][0]["incumbent"]["unexpected"] = True
            mutations.append(rollback)
            final_decision = self.contract_copy()
            final_decision["finalAdmissionDecision"]["deferredEvidence"][
                "unexpected"
            ] = "DEFER"
            mutations.append(final_decision)
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
        self.assertIn("finalAdmissionDecision", self.contract)
        mutated = self.contract_copy()
        mutated["finalAdmissionDecision"]["evaluationDisposition"] = "PASS"
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
        self.assertTrue(hasattr(self.validator, "HARNESS_PATH"))
        self.assertTrue(hasattr(self.validator, "ROSTER_ADMISSION_PATH"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root.parent / f"{root.name}-outside-sensitive-marker"
            outside.write_text('{"outside":"must-not-be-read"}', encoding="utf-8")
            try:
                for relative in (
                    self.validator.CONTRACT_PATH,
                    self.validator.SCHEMA_PATH,
                    self.validator.FIXTURE_PATH,
                    self.validator.HARNESS_PATH,
                    self.validator.ROSTER_ADMISSION_PATH,
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
        self.assertTrue(hasattr(self.validator, "HARNESS_PATH"))
        self.assertTrue(hasattr(self.validator, "ROSTER_ADMISSION_PATH"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                self.validator.CONTRACT_PATH,
                self.validator.SCHEMA_PATH,
                self.validator.FIXTURE_PATH,
                self.validator.HARNESS_PATH,
                self.validator.ROSTER_ADMISSION_PATH,
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

    def test_cli_rejects_symlink_root_before_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            symlink_root = base / "symlink-root"
            symlink_root.symlink_to(
                REPOSITORY_ROOT,
                target_is_directory=True,
            )
            symlink_parent = base / "symlink-parent"
            symlink_parent.symlink_to(
                REPOSITORY_ROOT.parent,
                target_is_directory=True,
            )
            with self.assertRaises(
                self.validator.EvaluationContractError
            ) as raised:
                self.validator.validate_contract(symlink_root)
            self.assertEqual(raised.exception.code, "AREA-EVAL-INPUT")
            self.assertEqual(raised.exception.exit_code, 2)
            for raw_root in (
                symlink_root,
                symlink_parent / REPOSITORY_ROOT.name,
            ):
                with self.subTest(raw_root=raw_root.name):
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(SCRIPT_PATH),
                            "--root",
                            str(raw_root),
                        ],
                        capture_output=True,
                        check=False,
                        text=True,
                    )
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("ERR AREA-EVAL-INPUT", result.stderr)
                    self.assertNotIn(str(REPOSITORY_ROOT), result.stderr)

    def test_source_rollback_mutation_fails_closed_when_injected(self) -> None:
        mutated_source = copy.deepcopy(self.roster_admission)
        mutated_source["candidates"][0]["rollback"]["procedure"][0] = (
            "skip the projection freeze"
        )
        with self.assertRaises(
            self.validator.EvaluationContractError
        ) as raised:
            self.validator.validate_contract(
                REPOSITORY_ROOT,
                self.contract_copy(),
                self.harness,
                mutated_source,
            )
        self.assertEqual(raised.exception.code, "AREA-EVAL-ROLLBACK")

    def test_cli_source_rollback_mutation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            for source, relative in (
                (CONTRACT_PATH, self.validator.CONTRACT_PATH),
                (SCHEMA_PATH, self.validator.SCHEMA_PATH),
                (HARNESS_PATH, self.validator.HARNESS_PATH),
                (
                    ROSTER_ADMISSION_PATH,
                    self.validator.ROSTER_ADMISSION_PATH,
                ),
            ):
                destination = root.joinpath(*relative.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            source_path = root.joinpath(
                *self.validator.ROSTER_ADMISSION_PATH.parts
            )
            source_contract = json.loads(
                source_path.read_text(encoding="utf-8")
            )
            source_contract["candidates"][1]["rollback"]["triggers"][0] = (
                "ignore critical evaluation misses"
            )
            source_path.write_text(
                json.dumps(source_contract),
                encoding="utf-8",
            )
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
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertIn("ERR AREA-EVAL-ROLLBACK", result.stderr)

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
        self.assertIn("corpusRecords=48", production.stdout)
        self.assertIn("adjudicationRecords=12", production.stdout)
        self.assertIn("rollbackRecords=2", production.stdout)
        self.assertIn("deferredEvidence=9", production.stdout)
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
