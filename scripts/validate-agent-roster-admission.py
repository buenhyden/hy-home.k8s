#!/usr/bin/env python3
"""Validate the closed Spec 044 roster-admission policy contract."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-roster-admission.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-roster-admission.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-roster-admission.json")
HARNESS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)

OWNER_SPEC = "docs/03.specs/044-agent-roster-evaluation-and-admission/spec.md"
FIXED_CUTOFF_LOCAL = "2026-07-10 10:00 Asia/Seoul"
FIXED_CUTOFF_UTC = "2026-07-10T01:00:00Z"
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
CURRENT_ROLES = frozenset(TARGET_ROLES[:-2])
TARGET_SURFACES = ("local", "claude", "codex", "gemini")
CURRENT_SURFACES = frozenset(("local", "claude", "codex"))
CANDIDATE_ROLES = ("docs-researcher", "quality-engineer")
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
ADMISSION_CONDITIONS = (
    "approved-recurring-unowned-gap",
    "non-overlap-and-existing-role-strengthening-insufficient",
    "explicit-owner-input-output-permission-boundaries",
    "least-privilege-four-surface-target-plan",
    "four-class-evaluation-with-incumbent-baseline",
    "independent-quality-safety-cost-latency-adjudication",
    "reproducible-rollback-to-current-10-3-30",
)
PROHIBITED_MEMORY_CONTENT = (
    "credential-values",
    "auth-files",
    "tokens",
    "secrets",
    "raw-prompts",
    "full-provider-transcripts",
    "shell-history",
    "private-diagnostics",
    "environment-dumps",
    "user-configuration",
)
ROLE_POLICY = {
    "docs-researcher": {
        "permissions": (
            "repository-read-only",
            "official-primary-source-read-only",
            "no-durable-document-authoring",
        ),
        "allowedTools": (
            "repository-search",
            "official-source-search",
            "source-ledger-validator",
        ),
        "allowedPaths": (
            "docs/90.references/research/**",
            "docs/90.references/audits/**",
            "docs/00.agent-governance/contracts/**",
        ),
        "prohibitedActions": (
            "write-durable-document-bodies",
            "decide-policy",
            "change-code-config-or-workflows",
            "install-or-authenticate-providers",
            "read-or-store-sensitive-data",
            "perform-live-or-remote-mutations",
        ),
        "handoffs": ("doc-writer", "supervisor", "security-auditor"),
    },
    "quality-engineer": {
        "permissions": (
            "repository-read-only",
            "delegated-tests-and-fixtures-write-only",
            "no-product-security-or-workflow-approval",
        ),
        "allowedTools": (
            "repository-search",
            "unit-test-runner",
            "validator-runner",
            "fixture-authoring",
        ),
        "allowedPaths": (
            "tests/**",
            "scripts/validate-*.py",
            "docs/00.agent-governance/contracts/**",
        ),
        "prohibitedActions": (
            "own-product-implementation",
            "grant-security-sign-off",
            "approve-workflow-or-provider-changes",
            "perform-live-or-remote-mutations",
            "read-or-store-sensitive-data",
            "bypass-independent-adjudication",
        ),
        "handoffs": ("code-reviewer", "security-auditor", "supervisor"),
    },
}
SENSITIVE_KEY_NAMES = frozenset(
    {
        "token",
        "apikey",
        "api_key",
        "secret",
        "password",
        "credential",
        "authfile",
        "auth_file",
        "shellhistory",
        "shell_history",
        "transcript",
        "rawprompt",
        "raw_prompt",
    }
)
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]+", re.IGNORECASE),
    re.compile(r"ghp_[A-Za-z0-9_-]+", re.IGNORECASE),
    re.compile(r"\bBearer\s+\S+", re.IGNORECASE),
    re.compile(r"AIza[A-Za-z0-9_-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.IGNORECASE),
)


class AdmissionError(ValueError):
    """Stable, payload-free roster-admission validation failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        if not code.startswith("AREA-ADM-"):
            raise ValueError(f"unstable admission diagnostic: {code}")
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def fail(code: str, detail: str, *, exit_code: int = 1) -> None:
    raise AdmissionError(code, detail, exit_code=exit_code)


def _object_without_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(
                "AREA-ADM-DUPLICATE-KEY",
                f"duplicate JSON key at {key!r}",
                exit_code=2,
            )
        result[key] = value
    return result


def decode_json_text(text: str, source: str) -> Any:
    """Decode JSON while rejecting duplicate keys before schema validation."""

    try:
        return json.loads(text, object_pairs_hook=_object_without_duplicate_keys)
    except AdmissionError:
        raise
    except json.JSONDecodeError as exc:
        fail(
            "AREA-ADM-JSON",
            f"{source}: invalid JSON at line {exc.lineno} column {exc.colno}",
            exit_code=2,
        )


def _resolve_regular_file(root: Path, relative: PurePosixPath) -> Path:
    try:
        repository_root = root.resolve(strict=True)
    except OSError:
        fail("AREA-ADM-INPUT", "repository root is unavailable", exit_code=2)
    if not repository_root.is_dir():
        fail("AREA-ADM-INPUT", "repository root is not a directory", exit_code=2)
    candidate = repository_root.joinpath(*relative.parts)
    try:
        candidate.relative_to(repository_root)
        metadata = os.lstat(candidate)
    except (OSError, ValueError):
        fail(
            "AREA-ADM-INPUT",
            f"required input is unavailable: {relative}",
            exit_code=2,
        )
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        fail(
            "AREA-ADM-INPUT",
            f"required input is not a regular file: {relative}",
            exit_code=2,
        )
    return candidate


def _load_json_file(root: Path, relative: PurePosixPath) -> Any:
    path = _resolve_regular_file(root, relative)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        fail(
            "AREA-ADM-INPUT",
            f"required input cannot be read: {relative}",
            exit_code=2,
        )
    return decode_json_text(text, str(relative))


def load_contract(root: Path) -> dict[str, Any]:
    contract = _load_json_file(root, CONTRACT_PATH)
    if not isinstance(contract, dict):
        fail("AREA-ADM-SCHEMA", "contract root must be an object")
    return contract


def _validate_schema(root: Path, contract: dict[str, Any]) -> None:
    schema = _load_json_file(root, SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("AREA-ADM-SCHEMA", "schema root must be an object", exit_code=2)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception:
        fail("AREA-ADM-SCHEMA", "schema is not valid Draft 2020-12", exit_code=2)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.absolute_path) or "<root>"
        fail("AREA-ADM-SCHEMA", f"closed schema violation at {location}")


def _scan_sensitive_payload(value: Any, path: str = "<root>") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = re.sub(r"[^a-z0-9_]", "", key.lower())
            if normalized in SENSITIVE_KEY_NAMES:
                fail(
                    "AREA-ADM-SENSITIVE",
                    f"forbidden sensitive key at {path}/{key}",
                )
            _scan_sensitive_payload(nested, f"{path}/{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            _scan_sensitive_payload(nested, f"{path}/{index}")
        return
    if isinstance(value, str):
        if any(pattern.search(value) for pattern in SENSITIVE_VALUE_PATTERNS):
            fail("AREA-ADM-SENSITIVE", f"secret-like value at {path}")


def _require_exact_list(
    value: Any,
    expected: tuple[str, ...],
    code: str,
    label: str,
) -> None:
    if not isinstance(value, list) or tuple(value) != expected:
        fail(code, f"{label} differs from the closed ordered set")


def _require_unique_strings(
    value: Any,
    *,
    code: str,
    label: str,
    minimum: int,
) -> None:
    if (
        not isinstance(value, list)
        or len(value) < minimum
        or any(not isinstance(item, str) or not item.strip() for item in value)
        or len(value) != len(set(value))
    ):
        fail(code, f"{label} must contain at least {minimum} unique strings")


def _validate_identity_and_cutoff(contract: dict[str, Any]) -> None:
    expected_identity = {
        "$schema": "./agent-roster-admission.schema.json",
        "schemaVersion": 1,
        "contractId": "hy-home.k8s/agent-roster-admission",
        "contractVersion": "1.0.0",
        "ownerSpec": OWNER_SPEC,
    }
    for key, expected in expected_identity.items():
        if contract.get(key) != expected:
            code = "AREA-ADM-OWNER" if key == "ownerSpec" else "AREA-ADM-IDENTITY"
            fail(code, f"{key} differs from the Spec 044 contract identity")
    cutoff = contract["fixedSourceCutoff"]
    if (
        cutoff["localTime"] != FIXED_CUTOFF_LOCAL
        or cutoff["instantUtc"] != FIXED_CUTOFF_UTC
    ):
        fail("AREA-ADM-CUTOFF", "fixed source cutoff differs")


def _validate_evidence_boundary(contract: dict[str, Any]) -> None:
    if contract["state"] != "contract-only":
        fail("AREA-ADM-STATE", "roster admission policy must remain contract-only")
    evidence = contract["evidence"]
    if (
        evidence["class"] != "repo-static"
        or evidence["claimBoundary"]
        != "prepared-policy-and-candidate-contract-only"
        or evidence["admissionVerdict"] != "DEFER"
        or evidence["promotionAuthorized"] is not False
    ):
        fail(
            "AREA-ADM-EVIDENCE",
            "repo-static policy must not claim admission or promotion",
        )
    _require_exact_list(
        evidence["deferredClasses"],
        DEFERRED_EVIDENCE,
        "AREA-ADM-EVIDENCE",
        "deferred evidence classes",
    )
    states = evidence["deferredClassStates"]
    if tuple(states) != DEFERRED_EVIDENCE or any(
        states[evidence_class] != "DEFER"
        for evidence_class in DEFERRED_EVIDENCE
    ):
        fail(
            "AREA-ADM-EVIDENCE",
            "runtime/provider/auth/CI/remote/live evidence must remain DEFER",
        )


def _validate_harness_and_inventory(
    root: Path, contract: dict[str, Any]
) -> None:
    harness = _load_json_file(root, HARNESS_PATH)
    if not isinstance(harness, dict):
        fail("AREA-ADM-INVENTORY", "harness contract root must be an object")
    current = contract["currentInventory"]
    if current != {
        "state": "current",
        "roleCount": 10,
        "surfaceCount": 3,
        "adapterCount": 30,
    }:
        fail("AREA-ADM-INVENTORY", "current inventory must remain 10/3/30")
    target = contract["targetInventory"]
    if (
        target["state"] != "target-only"
        or (
            target["roleCount"],
            target["surfaceCount"],
            target["adapterCount"],
        )
        != (12, 4, 48)
    ):
        fail("AREA-ADM-INVENTORY", "target inventory must remain target-only 12/4/48")
    _require_exact_list(
        target["roleIds"],
        TARGET_ROLES,
        "AREA-ADM-INVENTORY",
        "target roles",
    )
    _require_exact_list(
        target["surfaceIds"],
        TARGET_SURFACES,
        "AREA-ADM-INVENTORY",
        "target surfaces",
    )

    harness_current = harness.get("currentInventory")
    harness_target = harness.get("targetInventory")
    if not isinstance(harness_current, dict) or not isinstance(
        harness_target, dict
    ):
        fail("AREA-ADM-INVENTORY", "harness inventories are missing")
    if (
        harness_current.get("state") != "current"
        or (
            harness_current.get("expectedRoleCount"),
            harness_current.get("expectedSurfaceCount"),
            harness_current.get("expectedProjectionCount"),
        )
        != (10, 3, 30)
        or set(harness_current.get("roleIds", [])) != CURRENT_ROLES
        or set(harness_current.get("surfaceIds", [])) != CURRENT_SURFACES
        or len(harness_current.get("projections", [])) != 30
    ):
        fail(
            "AREA-ADM-INVENTORY",
            "harness current inventory no longer proves 10/3/30",
        )
    if (
        harness_target.get("state") != "target-only"
        or (
            harness_target.get("expectedRoleCount"),
            harness_target.get("expectedSurfaceCount"),
            harness_target.get("expectedProjectionCount"),
        )
        != (12, 4, 48)
        or tuple(harness_target.get("roleIds", [])) != TARGET_ROLES
        or tuple(harness_target.get("surfaceIds", [])) != TARGET_SURFACES
    ):
        fail(
            "AREA-ADM-INVENTORY",
            "harness target inventory no longer proves target-only 12/4/48",
        )
    projections = harness_target.get("projections")
    if not isinstance(projections, list) or len(projections) != 48:
        fail("AREA-ADM-INVENTORY", "harness target projections are incomplete")
    actual_projection_set = {
        (item.get("roleId"), item.get("surfaceId"))
        for item in projections
        if isinstance(item, dict) and item.get("admissionState") == "target-only"
    }
    expected_projection_set = {
        (role_id, surface_id)
        for role_id in TARGET_ROLES
        for surface_id in TARGET_SURFACES
    }
    if actual_projection_set != expected_projection_set:
        fail(
            "AREA-ADM-INVENTORY",
            "harness target projection set differs from 12 x 4",
        )


def _validate_catalog_conditions_and_memory(contract: dict[str, Any]) -> None:
    catalog = contract["externalCatalogPolicy"]
    if catalog != {
        "source": "msitarzewski/agency-agents",
        "authority": "idea-catalog-only",
        "directImportAllowed": False,
        "popularityIsAdmissionEvidence": False,
        "upstreamPromptIsAdmissionEvidence": False,
        "localAdmissionEvidenceRequired": True,
    }:
        fail(
            "AREA-ADM-CATALOG",
            "agency-agents must remain non-authoritative idea evidence",
        )
    _require_exact_list(
        contract["admissionConditions"],
        ADMISSION_CONDITIONS,
        "AREA-ADM-CONDITIONS",
        "admission conditions",
    )
    memory = contract["memoryPolicy"]
    _require_exact_list(
        memory["classes"],
        MEMORY_CLASSES,
        "AREA-ADM-MEMORY",
        "memory classes",
    )
    if memory["repositoryWins"] is not True:
        fail("AREA-ADM-MEMORY", "repository authority must win memory conflicts")
    if (
        memory["sensitiveDataAllowed"] is not False
        or memory["rawPromptOrTranscriptAllowed"] is not False
    ):
        fail(
            "AREA-ADM-SENSITIVE",
            "memory must exclude sensitive data and raw prompts/transcripts",
        )
    _require_exact_list(
        memory["prohibitedContent"],
        PROHIBITED_MEMORY_CONTENT,
        "AREA-ADM-SENSITIVE",
        "prohibited memory content",
    )


def _validate_allowed_path(path: str, role_id: str) -> None:
    if (
        path.startswith("/")
        or "\\" in path
        or any(part == ".." for part in path.split("/"))
        or path.startswith(".git")
        or path.startswith("_workspace")
        or path.startswith("secrets")
        or ".env" in path
    ):
        fail("AREA-ADM-AUTHORITY", f"{role_id} contains an unsafe allowed path")


def _validate_candidate(candidate: dict[str, Any], role_id: str) -> None:
    if (
        candidate["roleId"] != role_id
        or candidate["decision"] != "candidate-only"
        or candidate["authority"] != "repository-static-candidate-only"
        or candidate["owner"] != role_id
    ):
        fail(
            "AREA-ADM-CANDIDATE",
            f"{role_id} must remain an unpromoted repository-static candidate",
        )
    gap = candidate["requirementGap"]
    if (
        gap["classification"] != "approved-recurring-unowned-gap"
        or gap["requirementId"] != "REQ-PRD-FUN-12"
        or gap["approved"] is not True
        or gap["approvalOwner"] != "platform"
        or gap["recurring"] is not True
        or gap["currentlyOwned"] is not False
        or not gap["gapStatement"].strip()
    ):
        fail(
            "AREA-ADM-GAP",
            f"{role_id} lacks an approved recurring unowned requirement gap",
        )
    _require_unique_strings(
        gap["recurrenceEvidence"],
        code="AREA-ADM-GAP",
        label=f"{role_id} recurrence evidence",
        minimum=2,
    )
    overlap = candidate["overlapAnalysis"]
    if (
        overlap["existingRoleCanOwnDeliverable"] is not False
        or overlap["strengthenExistingRoleResolvesGap"] is not False
        or overlap["distinctOwnerRequired"] is not True
        or not overlap["rationale"].strip()
    ):
        fail(
            "AREA-ADM-OVERLAP",
            f"{role_id} overlap analysis does not prove a distinct owner",
        )
    _require_unique_strings(
        overlap["existingRolesReviewed"],
        code="AREA-ADM-OVERLAP",
        label=f"{role_id} reviewed roles",
        minimum=3,
    )
    if any(
        reviewed in CANDIDATE_ROLES
        for reviewed in overlap["existingRolesReviewed"]
    ):
        fail(
            "AREA-ADM-OVERLAP",
            f"{role_id} overlap review cannot use a candidate as incumbent owner",
        )
    for field, minimum in (
        ("inputs", 4),
        ("outputs", 4),
        ("stopConditions", 4),
    ):
        _require_unique_strings(
            candidate[field],
            code="AREA-ADM-ROLE-CONTRACT",
            label=f"{role_id} {field}",
            minimum=minimum,
        )
    role_policy = ROLE_POLICY[role_id]
    for field in (
        "permissions",
        "allowedTools",
        "allowedPaths",
        "prohibitedActions",
    ):
        _require_exact_list(
            candidate[field],
            role_policy[field],
            "AREA-ADM-AUTHORITY",
            f"{role_id} {field}",
        )
    _require_exact_list(
        candidate["handoffs"],
        role_policy["handoffs"],
        "AREA-ADM-HANDOFF",
        f"{role_id} handoffs",
    )
    if role_id in candidate["handoffs"]:
        fail("AREA-ADM-HANDOFF", f"{role_id} cannot hand off to itself")
    for allowed_path in candidate["allowedPaths"]:
        _validate_allowed_path(allowed_path, role_id)

    surface_plan = candidate["surfacePlan"]
    if tuple(item["surfaceId"] for item in surface_plan) != TARGET_SURFACES:
        fail("AREA-ADM-SURFACE", f"{role_id} surface plan differs")
    for item in surface_plan:
        suffix = ".toml" if item["surfaceId"] == "codex" else ".md"
        root_by_surface = {
            "local": ".agents/agents",
            "claude": ".claude/agents",
            "codex": ".codex/agents",
            "gemini": ".gemini/agents",
        }
        expected_path = (
            f"{root_by_surface[item['surfaceId']]}/{role_id}{suffix}"
        )
        if (
            item["state"] != "target-only"
            or item["adapterPath"] != expected_path
            or item["leastPrivilege"] is not True
            or item["providerNativeMetadataRequired"] is not True
        ):
            fail(
                "AREA-ADM-SURFACE",
                f"{role_id} {item['surfaceId']} plan is not target-only least privilege",
            )

    evaluation = candidate["evaluationGate"]
    _require_exact_list(
        evaluation["classes"],
        EVALUATION_CLASSES,
        "AREA-ADM-EVALUATION",
        f"{role_id} evaluation classes",
    )
    if (
        evaluation["baselineState"] != "required-before-promotion"
        or evaluation["sameCorpusAndGraderRequired"] is not True
    ):
        fail(
            "AREA-ADM-EVALUATION",
            f"{role_id} lacks the closed incumbent comparison gate",
        )
    adjudication = evaluation["independentAdjudication"]
    if (
        adjudication["required"] is not True
        or adjudication["selfAdjudicationProhibited"] is not True
        or adjudication["adjudicatorOwner"] != "independent-reviewer"
        or tuple(adjudication["thresholdOrder"])
        != ("quality", "safety", "cost", "latency")
        or adjudication["criticalMissBlocksPromotion"] is not True
    ):
        fail(
            "AREA-ADM-ADJUDICATION",
            f"{role_id} lacks independent quality/safety-first adjudication",
        )
    rollback = candidate["rollback"]
    if (
        rollback["state"] != "required-before-promotion"
        or rollback["restoreInventory"] != "10/3/30"
        or rollback["reproducible"] is not True
        or rollback["executed"] is not False
    ):
        fail(
            "AREA-ADM-ROLLBACK",
            f"{role_id} rollback must remain prepared and unexecuted",
        )
    _require_unique_strings(
        rollback["triggers"],
        code="AREA-ADM-ROLLBACK",
        label=f"{role_id} rollback triggers",
        minimum=4,
    )
    _require_unique_strings(
        rollback["procedure"],
        code="AREA-ADM-ROLLBACK",
        label=f"{role_id} rollback procedure",
        minimum=4,
    )


def _validate_candidates(contract: dict[str, Any]) -> None:
    candidates = contract["candidates"]
    if tuple(candidate["roleId"] for candidate in candidates) != CANDIDATE_ROLES:
        fail(
            "AREA-ADM-CANDIDATE",
            "candidate set must be docs-researcher then quality-engineer",
        )
    owners = [candidate["owner"] for candidate in candidates]
    deliverables = [candidate["distinctDeliverable"] for candidate in candidates]
    if len(owners) != len(set(owners)) or len(deliverables) != len(
        set(deliverables)
    ):
        fail(
            "AREA-ADM-OVERLAP",
            "candidate owners and distinct deliverables must not overlap",
        )
    for candidate, role_id in zip(candidates, CANDIDATE_ROLES, strict=True):
        _validate_candidate(candidate, role_id)


def validate_contract(
    root: Path, contract: dict[str, Any] | None = None
) -> dict[str, int]:
    """Validate one policy contract without authorizing roster promotion."""

    root = Path(root)
    selected = load_contract(root) if contract is None else contract
    if not isinstance(selected, dict):
        fail("AREA-ADM-SCHEMA", "contract root must be an object")
    _validate_schema(root, selected)
    _scan_sensitive_payload(selected)
    _validate_identity_and_cutoff(selected)
    _validate_evidence_boundary(selected)
    _validate_harness_and_inventory(root, selected)
    _validate_catalog_conditions_and_memory(selected)
    _validate_candidates(selected)
    return {
        "candidates": len(selected["candidates"]),
        "conditions": len(selected["admissionConditions"]),
        "currentRoles": selected["currentInventory"]["roleCount"],
        "currentSurfaces": selected["currentInventory"]["surfaceCount"],
        "currentAdapters": selected["currentInventory"]["adapterCount"],
        "targetRoles": selected["targetInventory"]["roleCount"],
        "targetSurfaces": selected["targetInventory"]["surfaceCount"],
        "targetAdapters": selected["targetInventory"]["adapterCount"],
        "surfacePlans": sum(
            len(candidate["surfacePlan"]) for candidate in selected["candidates"]
        ),
        "evaluationClasses": len(EVALUATION_CLASSES),
        "memoryClasses": len(selected["memoryPolicy"]["classes"]),
        "deferredEvidenceClasses": len(
            selected["evidence"]["deferredClasses"]
        ),
    }


def apply_mutation(contract: dict[str, Any], name: str) -> None:
    """Apply one named synthetic mutation used by the closed self-test."""

    candidates = contract["candidates"]
    first = candidates[0]
    second = candidates[1]
    mutations = {
        "unknown-top-level": lambda: contract.__setitem__("unknown", True),
        "wrong-owner-spec": lambda: contract.__setitem__(
            "ownerSpec", "docs/03.specs/999-invalid/spec.md"
        ),
        "wrong-cutoff": lambda: contract["fixedSourceCutoff"].__setitem__(
            "instantUtc", "2026-07-10T01:00:01Z"
        ),
        "wrong-contract-state": lambda: contract.__setitem__("state", "current"),
        "non-static-evidence": lambda: contract["evidence"].__setitem__(
            "class", "runtime"
        ),
        "admission-pass-preclaim": lambda: contract["evidence"].__setitem__(
            "admissionVerdict", "PASS"
        ),
        "promotion-authorized": lambda: contract["evidence"].__setitem__(
            "promotionAuthorized", True
        ),
        "runtime-pass": lambda: contract["evidence"][
            "deferredClassStates"
        ].__setitem__("runtime", "PASS"),
        "provider-discovery-pass": lambda: contract["evidence"][
            "deferredClassStates"
        ].__setitem__("provider-discovery", "PASS"),
        "provider-auth-pass": lambda: contract["evidence"][
            "deferredClassStates"
        ].__setitem__("provider-authentication", "PASS"),
        "live-pass": lambda: contract["evidence"][
            "deferredClassStates"
        ].__setitem__("live", "PASS"),
        "promoted-current-count": lambda: contract[
            "currentInventory"
        ].__setitem__("roleCount", 12),
        "target-state-current": lambda: contract["targetInventory"].__setitem__(
            "state", "current"
        ),
        "missing-target-role": lambda: contract["targetInventory"][
            "roleIds"
        ].pop(),
        "extra-target-surface": lambda: contract["targetInventory"][
            "surfaceIds"
        ].append("unsupported"),
        "duplicate-candidate": lambda: candidates.__setitem__(
            1, copy.deepcopy(first)
        ),
        "swapped-candidates": lambda: candidates.reverse(),
        "candidate-pass-preclaim": lambda: first.__setitem__("decision", "PASS"),
        "gap-not-approved": lambda: first["requirementGap"].__setitem__(
            "approved", False
        ),
        "gap-not-recurring": lambda: first["requirementGap"].__setitem__(
            "recurring", False
        ),
        "gap-already-owned": lambda: first["requirementGap"].__setitem__(
            "currentlyOwned", True
        ),
        "overlap-existing-owner": lambda: first["overlapAnalysis"].__setitem__(
            "existingRoleCanOwnDeliverable", True
        ),
        "overlap-strengthening-sufficient": lambda: first[
            "overlapAnalysis"
        ].__setitem__("strengthenExistingRoleResolvesGap", True),
        "duplicate-owner": lambda: second.__setitem__("owner", first["owner"]),
        "duplicate-deliverable": lambda: second.__setitem__(
            "distinctDeliverable", first["distinctDeliverable"]
        ),
        "over-authorized-permission": lambda: first["permissions"].append(
            "repository-write"
        ),
        "forbidden-tool": lambda: first["allowedTools"].append("shell-exec"),
        "unsafe-allowed-path": lambda: second["allowedPaths"].__setitem__(
            0, "secrets/**"
        ),
        "missing-prohibited-action": lambda: first[
            "prohibitedActions"
        ].pop(),
        "missing-stop-condition": lambda: first["stopConditions"].pop(),
        "self-handoff": lambda: first["handoffs"].__setitem__(
            0, "docs-researcher"
        ),
        "promoted-surface": lambda: first["surfacePlan"][0].__setitem__(
            "state", "current"
        ),
        "wrong-adapter-path": lambda: second["surfacePlan"][2].__setitem__(
            "adapterPath", ".codex/agents/docs-researcher.toml"
        ),
        "duplicate-surface": lambda: first["surfacePlan"].__setitem__(
            3, copy.deepcopy(first["surfacePlan"][0])
        ),
        "missing-evaluation-class": lambda: first["evaluationGate"][
            "classes"
        ].__setitem__(3, "positive"),
        "missing-baseline": lambda: first["evaluationGate"].__setitem__(
            "baselineState", "absent"
        ),
        "different-grader": lambda: second["evaluationGate"].__setitem__(
            "sameCorpusAndGraderRequired", False
        ),
        "self-adjudication": lambda: first["evaluationGate"][
            "independentAdjudication"
        ].__setitem__("selfAdjudicationProhibited", False),
        "cost-first-threshold": lambda: first["evaluationGate"][
            "independentAdjudication"
        ].__setitem__("thresholdOrder", ["cost", "latency", "quality", "safety"]),
        "rollback-not-required": lambda: first["rollback"].__setitem__(
            "state", "optional"
        ),
        "rollback-executed": lambda: second["rollback"].__setitem__(
            "executed", True
        ),
        "rollback-wrong-inventory": lambda: second["rollback"].__setitem__(
            "restoreInventory", "12/4/48"
        ),
        "agency-agents-authoritative": lambda: contract[
            "externalCatalogPolicy"
        ].__setitem__("authority", "roster-authority"),
        "agency-agents-direct-import": lambda: contract[
            "externalCatalogPolicy"
        ].__setitem__("directImportAllowed", True),
        "agency-no-local-evidence": lambda: contract[
            "externalCatalogPolicy"
        ].__setitem__("localAdmissionEvidenceRequired", False),
        "duplicate-condition": lambda: contract[
            "admissionConditions"
        ].__setitem__(6, contract["admissionConditions"][0]),
        "missing-memory-class": lambda: contract["memoryPolicy"][
            "classes"
        ].__setitem__(3, "working-short-term"),
        "repository-wins-false": lambda: contract["memoryPolicy"].__setitem__(
            "repositoryWins", False
        ),
        "sensitive-data-allowed": lambda: contract["memoryPolicy"].__setitem__(
            "sensitiveDataAllowed", True
        ),
        "raw-transcript-allowed": lambda: contract[
            "memoryPolicy"
        ].__setitem__("rawPromptOrTranscriptAllowed", True),
        "secret-like-value": lambda: first["outputs"].__setitem__(
            0, "sk-synthetic-fixture"
        ),
    }
    mutation = mutations.get(name)
    if mutation is None:
        fail("AREA-ADM-FIXTURE", f"unknown mutation name: {name}")
    mutation()


def run_self_test(root: Path) -> tuple[list[str], int]:
    contract = load_contract(root)
    fixture = _load_json_file(root, FIXTURE_PATH)
    if not isinstance(fixture, dict):
        fail("AREA-ADM-FIXTURE", "fixture root must be an object", exit_code=2)
    expected_keys = {"schemaVersion", "expected", "mutations"}
    if set(fixture) != expected_keys or fixture["schemaVersion"] != 1:
        fail("AREA-ADM-FIXTURE", "fixture envelope differs", exit_code=2)
    mutations = fixture["mutations"]
    if (
        not isinstance(mutations, list)
        or len(mutations) < 30
        or any(not isinstance(case, dict) for case in mutations)
    ):
        fail("AREA-ADM-FIXTURE", "fixture mutation matrix is incomplete", exit_code=2)
    names = [case.get("name") for case in mutations]
    if len(names) != len(set(names)):
        fail("AREA-ADM-FIXTURE", "fixture mutation names are duplicated", exit_code=2)
    failures: list[str] = []
    try:
        counts = validate_contract(root, contract)
    except AdmissionError as exc:
        return [f"baseline expected PASS but got {exc.code}"], 0
    if counts != fixture["expected"]:
        failures.append("baseline counts differ from fixture")
    for case in mutations:
        name = case.get("name")
        expected_rule = case.get("expectedRule")
        if (
            not isinstance(name, str)
            or not isinstance(expected_rule, str)
            or not expected_rule.startswith("AREA-ADM-")
            or set(case) != {"name", "expectedRule"}
        ):
            failures.append("fixture case envelope differs")
            continue
        mutated = copy.deepcopy(contract)
        try:
            apply_mutation(mutated, name)
            validate_contract(root, mutated)
        except AdmissionError as exc:
            if exc.code != expected_rule:
                failures.append(
                    f"{name}: expected {expected_rule}, got {exc.code}"
                )
        else:
            failures.append(f"{name}: mutation unexpectedly passed")
    return failures, len(mutations)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            failures, cases = run_self_test(args.root)
            if failures:
                for failure in failures:
                    print(
                        f"ERR AREA-ADM-SELF-TEST {failure}",
                        file=sys.stderr,
                    )
                return 1
            print(
                "[PASS] agent roster admission self-test passed: "
                f"cases={cases}"
            )
            return 0
        counts = validate_contract(args.root)
        print(
            "[PASS] agent roster admission policy validation passed: "
            "state=contract-only verdict=DEFER "
            f"candidates={counts['candidates']} "
            f"conditions={counts['conditions']} "
            f"current={counts['currentRoles']}/"
            f"{counts['currentSurfaces']}/{counts['currentAdapters']} "
            f"target={counts['targetRoles']}/"
            f"{counts['targetSurfaces']}/{counts['targetAdapters']} "
            f"surface_plans={counts['surfacePlans']} "
            f"evaluation_classes={counts['evaluationClasses']} "
            f"memory_classes={counts['memoryClasses']} "
            f"deferred_evidence={counts['deferredEvidenceClasses']}"
        )
        return 0
    except AdmissionError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
