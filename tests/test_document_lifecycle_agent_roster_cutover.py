"""Finite Spec 044 AREA-002 agent-roster lifecycle admission regressions."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_agent_roster_tested",
    SCRIPTS / "validate-document-lifecycle.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError("cannot import document lifecycle validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

from document_lifecycle import LifecycleDocument  # noqa: E402


BASE = "e324d4c1fa49ef7e508fa07c32e7f054f5a3a05e"  # pragma: allowlist secret
ROLES = (
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
BASE_DEFERRED_CLASSES = (
    "runtime",
    "provider-discovery",
    "provider-authentication",
    "hosted-ci",
    "remote",
    "live",
)
PROPOSED_DEFERRED_CLASSES = (
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
EVALUATION_CLASSES = (
    "positive",
    "negative-adversarial",
    "refusal-stop",
    "handoff",
)
PATHS = frozenset(
    {
        PurePosixPath(".agents/agents/docs-researcher.md"),
        PurePosixPath(".agents/agents/quality-engineer.md"),
        PurePosixPath(".claude/agents/docs-researcher.md"),
        PurePosixPath(".claude/agents/quality-engineer.md"),
    }
)


def adapter_path(role_id: str, surface_id: str) -> str:
    extensions = {"local": "md", "claude": "md", "codex": "toml", "gemini": "md"}
    roots = {
        "local": ".agents/agents",
        "claude": ".claude/agents",
        "codex": ".codex/agents",
        "gemini": ".gemini/agents",
    }
    return f"{roots[surface_id]}/{role_id}.{extensions[surface_id]}"


def admission_inventory(state: str, role_count: int, surface_count: int, adapter_count: int):
    return {
        "state": state,
        "roleCount": role_count,
        "surfaceCount": surface_count,
        "adapterCount": adapter_count,
    }


def harness_inventory(state: str, role_count: int, surface_count: int, projection_count: int):
    return {
        "state": state,
        "expectedRoleCount": role_count,
        "expectedSurfaceCount": surface_count,
        "expectedProjectionCount": projection_count,
    }


def evaluation_gate(baseline_state: str):
    return {
        "classes": list(EVALUATION_CLASSES),
        "baselineState": baseline_state,
        "sameCorpusAndGraderRequired": True,
        "independentAdjudication": {
            "required": True,
            "selfAdjudicationProhibited": True,
            "adjudicatorOwner": "independent-reviewer",
            "thresholdOrder": ["quality", "safety", "cost", "latency"],
            "criticalMissBlocksPromotion": True,
        },
    }


def exact_contracts() -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
    base_admission = {
        "contractId": "hy-home.k8s/agent-roster-admission",
        "contractVersion": "1.0.0",
        "state": "contract-only",
        "currentInventory": admission_inventory("current", 10, 3, 30),
        "evidence": {
            "class": "repo-static",
            "claimBoundary": "prepared-policy-and-candidate-contract-only",
            "admissionVerdict": "DEFER",
            "promotionAuthorized": False,
            "deferredClasses": list(BASE_DEFERRED_CLASSES),
            "deferredClassStates": {
                evidence_class: "DEFER"
                for evidence_class in BASE_DEFERRED_CLASSES
            },
        },
        "candidates": [
            {
                "roleId": role_id,
                "evaluationGate": evaluation_gate("required-before-promotion"),
            }
            for role_id in ("docs-researcher", "quality-engineer")
        ],
    }
    candidates = []
    for role_id in ("docs-researcher", "quality-engineer"):
        candidates.append(
            {
                "roleId": role_id,
                "decision": "repository-static-admitted",
                "authority": "repository-static-role-and-adapter-inventory-only",
                "surfacePlan": [
                    {
                        "surfaceId": surface_id,
                        "state": "current",
                        "adapterPath": adapter_path(role_id, surface_id),
                        "leastPrivilege": True,
                        "providerNativeMetadataRequired": True,
                    }
                    for surface_id in SURFACES
                ],
                "evaluationGate": evaluation_gate(
                    "deferred-to-area-003-before-runtime-activation"
                ),
            }
        )
    proposed_admission = {
        "contractId": "hy-home.k8s/agent-roster-admission",
        "contractVersion": "1.0.0",
        "state": "repository-static-admitted",
        "evidence": {
            "class": "repo-static",
            "claimBoundary": "repository-static-role-and-adapter-inventory-only",
            "admissionVerdict": "PASS",
            "promotionAuthorization": {
                "authorized": True,
                "scope": "repository-static-role-and-adapter-inventory-only",
                "excludedEvidenceClasses": list(PROPOSED_DEFERRED_CLASSES),
            },
            "deferredClasses": list(PROPOSED_DEFERRED_CLASSES),
            "deferredClassStates": {
                evidence_class: "DEFER"
                for evidence_class in PROPOSED_DEFERRED_CLASSES
            },
        },
        "currentInventory": admission_inventory("current", 12, 4, 48),
        "targetInventory": {
            **admission_inventory("achieved", 12, 4, 48),
            "roleIds": list(ROLES),
            "surfaceIds": list(SURFACES),
        },
        "candidates": candidates,
    }
    projections = [
        {
            "roleId": role_id,
            "surfaceId": surface_id,
            "path": adapter_path(role_id, surface_id),
            "admissionState": "current",
        }
        for role_id in ROLES
        for surface_id in SURFACES
    ]
    base_harness = {
        "contractId": "hy-home.k8s/agent-harness",
        "contractVersion": "1.0.0",
        "currentInventory": harness_inventory("current", 10, 3, 30),
    }
    proposed_harness = {
        "contractId": "hy-home.k8s/agent-harness",
        "contractVersion": "1.0.0",
        "currentInventory": {
            **harness_inventory("current", 12, 4, 48),
            "roleIds": list(ROLES),
            "surfaceIds": list(SURFACES),
            "projections": copy.deepcopy(projections),
        },
        "targetInventory": {
            **harness_inventory("achieved", 12, 4, 48),
            "roleIds": list(ROLES),
            "surfaceIds": list(SURFACES),
            "projections": projections,
        },
    }
    return base_admission, proposed_admission, base_harness, proposed_harness


def exact_documents():
    proposed = {
        path: LifecycleDocument(
            path,
            "exception/local-agent-asset"
            if path.parts[0] == ".agents"
            else "exception/provider-native-metadata",
            None,
        )
        for path in PATHS
    }
    return {}, proposed


class FiniteAgentRosterCutoverAdmissionTest(unittest.TestCase):
    def admit(self, *, mode: str = "staged", base_commit: str = BASE, base_documents=None, proposed_documents=None, contracts=None):
        base_admission, proposed_admission, base_harness, proposed_harness = contracts or exact_contracts()
        exact_base, exact_proposed = exact_documents()
        return VALIDATOR.finite_agent_roster_cutover_paths(
            mode=mode,
            base_commit=base_commit,
            base_documents=exact_base if base_documents is None else base_documents,
            proposed_documents=exact_proposed if proposed_documents is None else proposed_documents,
            base_admission=base_admission,
            proposed_admission=proposed_admission,
            base_harness=base_harness,
            proposed_harness=proposed_harness,
        )

    def test_exact_literal_contracts_admit_only_the_four_markdown_paths(self):
        self.assertEqual(self.admit(mode="staged"), PATHS)
        self.assertEqual(self.admit(mode="ci"), PATHS)

    def test_mode_base_path_and_profile_controls_fail_closed(self):
        for mode in ("snapshot", "explicit-ref"):
            with self.subTest(mode=mode):
                self.assertFalse(self.admit(mode=mode))
        self.assertFalse(self.admit(base_commit="0" * 40))

        base, proposed = exact_documents()
        proposed.pop(next(iter(PATHS)))
        self.assertFalse(self.admit(base_documents=base, proposed_documents=proposed))
        extra = PurePosixPath(".agents/agents/unrelated.md")
        proposed[extra] = LifecycleDocument(extra, "exception/local-agent-asset", None)
        self.assertFalse(self.admit(base_documents=base, proposed_documents=proposed))

        base, proposed = exact_documents()
        path = next(iter(PATHS))
        proposed[path] = LifecycleDocument(path, "sdlc/spec", "active")
        self.assertFalse(self.admit(base_documents=base, proposed_documents=proposed))
        base, proposed = exact_documents()
        path = next(iter(PATHS))
        base[path] = proposed[path]
        self.assertFalse(self.admit(base_documents=base, proposed_documents=proposed))

    def test_admission_and_candidate_plan_controls_fail_closed(self):
        contracts = list(exact_contracts())
        contracts[1]["state"] = "contract-only"
        self.assertFalse(self.admit(contracts=tuple(contracts)))

        contracts = list(exact_contracts())
        contracts[1]["currentInventory"]["adapterCount"] = 47
        self.assertFalse(self.admit(contracts=tuple(contracts)))

        contracts = list(exact_contracts())
        contracts[1]["candidates"][0]["surfacePlan"][0]["adapterPath"] = "bad.md"
        self.assertFalse(self.admit(contracts=tuple(contracts)))

    def test_evidence_defer_and_area003_evaluation_gate_controls_fail_closed(self):
        mutations = (
            lambda contract: contract["evidence"].__setitem__("class", "runtime"),
            lambda contract: contract["evidence"].__setitem__(
                "claimBoundary", "repository-static-and-runtime"
            ),
            lambda contract: contract["evidence"]["deferredClassStates"].__setitem__(
                "runtime", "PASS"
            ),
            lambda contract: contract["evidence"]["deferredClassStates"].pop(
                "provider-discovery"
            ),
            lambda contract: contract["evidence"].pop("deferredClassStates"),
            lambda contract: contract["evidence"]["deferredClassStates"].pop("live"),
            lambda contract: contract["candidates"][0]["evaluationGate"].__setitem__(
                "baselineState", "runtime-activated"
            ),
            lambda contract: contract["candidates"][1]["evaluationGate"][
                "independentAdjudication"
            ].__setitem__("required", False),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                contracts = list(exact_contracts())
                mutate(contracts[1])
                self.assertFalse(self.admit(contracts=tuple(contracts)))

    def test_harness_inventory_and_projection_controls_fail_closed(self):
        contracts = list(exact_contracts())
        contracts[3]["targetInventory"]["expectedProjectionCount"] = 47
        self.assertFalse(self.admit(contracts=tuple(contracts)))

        contracts = list(exact_contracts())
        contracts[3]["currentInventory"]["projections"].pop()
        self.assertFalse(self.admit(contracts=tuple(contracts)))

    def test_contract_blob_decoder_rejects_malformed_missing_nonobject_and_duplicate_keys(self):
        decoder = VALIDATOR._agent_contract_blob_from_bytes
        path = PurePosixPath("docs/00.agent-governance/contracts/example.json")
        self.assertEqual(decoder(b'{"ok":true}', path), {"ok": True})
        for raw in (b"{", b"[1]", b'{"a":1,"a":2}'):
            with self.subTest(raw=raw):
                with self.assertRaises(VALIDATOR.InvocationError):
                    decoder(raw, path)
        with self.assertRaises(VALIDATOR.InvocationError):
            VALIDATOR._agent_contracts_from_blob_maps(ROOT, {}, {})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
