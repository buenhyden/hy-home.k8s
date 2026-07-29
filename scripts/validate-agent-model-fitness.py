#!/usr/bin/env python3
"""Validate the closed Spec 044 model-fitness admission contract."""

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
    "docs/00.agent-governance/contracts/agent-model-fitness.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-model-fitness.schema.json"
)
PROVIDER_EVIDENCE_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/provider-runtime-evidence.json"
)
HARNESS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-model-fitness.json")

OWNER_SPEC = "docs/03.specs/044-agent-roster-evaluation-and-admission/spec.md"
AUTHORITATIVE_CUTOFF_REF = (
    "docs/00.agent-governance/contracts/"
    "provider-runtime-evidence.json#/cutoff"
)
AUTHORITATIVE_LOCAL = "2026-07-10T10:00:00+09:00"
AUTHORITATIVE_UTC = "2026-07-10T01:00:00Z"
CANARY_REF = (
    "docs/00.agent-governance/contracts/"
    "provider-runtime-evidence.json#/providers"
)
BASELINE_REF = "tests/fixtures/agent-model-fitness.json#/sameSuiteBaseline"

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
PROVIDER_IDS = ("local", "claude", "codex", "gemini")
TOP_ROLES = {"supervisor", "incident-responder", "security-auditor"}
MEDIUM_ROLES = {"doc-writer", "wiki-curator"}

PROVIDER_CONTRACT = {
    "local": {
        "trackedSurface": ".agents/agents",
        "runtimeInterface": "repo-static",
        "modelIdentifierPlane": "local-repository-label",
        "apiVsCliBoundary": (
            "repository-label-is-not-provider-api-or-cli-resolution"
        ),
        "candidateModels": (
            ("Gemini 3.1 Pro", "repo-label"),
            ("Gemini 3.5 Flash", "repo-label"),
        ),
    },
    "claude": {
        "trackedSurface": ".claude/agents",
        "runtimeInterface": "claude-code-cli",
        "modelIdentifierPlane": "claude-code-cli-alias",
        "apiVsCliBoundary": (
            "claude-code-cli-alias-does-not-prove-anthropic-api-resolution"
        ),
        "candidateModels": (
            ("Fable 5", "stable"),
            ("Opus 4.8", "stable"),
            ("Sonnet 5", "stable"),
            ("Haiku 4.5", "stable"),
        ),
    },
    "codex": {
        "trackedSurface": ".codex/agents",
        "runtimeInterface": "codex-cli",
        "modelIdentifierPlane": "codex-cli-model-id",
        "apiVsCliBoundary": (
            "codex-cli-model-id-does-not-prove-openai-api-or-hosted-resolution"
        ),
        "candidateModels": (
            ("gpt-5.6-sol", "stable"),
            ("gpt-5.6-terra", "stable"),
            ("gpt-5.6-luna", "stable"),
            ("gpt-5.4-mini", "stable"),
        ),
    },
    "gemini": {
        "trackedSurface": ".gemini/agents",
        "runtimeInterface": "gemini-cli",
        "modelIdentifierPlane": "gemini-api-id-candidate-for-cli",
        "apiVsCliBoundary": (
            "gemini-api-id-does-not-prove-cli-resolution-or-auto-routing"
        ),
        "candidateModels": (
            ("gemini-3.1-pro-preview", "preview"),
            ("gemini-3.5-flash", "stable"),
            ("gemini-3.1-flash-lite", "stable"),
        ),
    },
}

NEGATIVE_MUTATIONS = (
    "duplicate-json-key",
    "unsupported-field",
    "unsupported-alias",
    "runtime-preclaim",
    "preview-promotion",
    "secret-like-value",
    "scope-escape",
    "harness-cutoff-authority",
    "cutoff-mismatch",
    "tuple-provider-duplicate",
    "threshold-order",
    "canary-pass",
    "baseline-pass",
    "decision-pass",
    "fallback-change",
    "api-cli-conflation",
)

PROHIBITED_KEY_NAMES = {
    "api_key",
    "apikey",
    "auth_file",
    "authfile",
    "credential",
    "password",
    "raw_prompt",
    "rawprompt",
    "secret",
    "shell_history",
    "shellhistory",
    "token",
    "transcript",
}
PROHIBITED_VALUE_FRAGMENTS = (
    "sk-",
    "bearer ",
    "ghp_",
    "aiza",
    "-----begin private key",
)


class ModelFitnessError(ValueError):
    """Stable AREA-FIT validation failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def fail(code: str, detail: str, *, exit_code: int = 1) -> None:
    raise ModelFitnessError(code, detail, exit_code=exit_code)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(
                "AREA-FIT-DUPLICATE-KEY",
                f"duplicate JSON key {key!r}",
                exit_code=2,
            )
        result[key] = value
    return result


def parse_json_text(text: str, label: str) -> Any:
    """Parse JSON while rejecting duplicate keys at every object depth."""

    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except json.JSONDecodeError as exc:
        fail("AREA-FIT-JSON", f"{label}: {exc}", exit_code=2)


def _resolve_regular_file(root: Path, relative: PurePosixPath) -> Path:
    try:
        root_metadata = os.lstat(root)
    except OSError:
        fail("AREA-FIT-INPUT", "repository root is unavailable", exit_code=2)
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(
        root_metadata.st_mode
    ):
        fail("AREA-FIT-INPUT", "repository root is not a directory", exit_code=2)
    try:
        repository_root = root.resolve(strict=True)
    except OSError:
        fail("AREA-FIT-INPUT", "repository root is unavailable", exit_code=2)
    if relative.is_absolute() or ".." in relative.parts:
        fail("AREA-FIT-INPUT", "governed input path is outside scope", exit_code=2)

    candidate = repository_root.joinpath(*relative.parts)
    cursor = repository_root
    for index, part in enumerate(relative.parts):
        cursor = cursor / part
        try:
            metadata = os.lstat(cursor)
        except OSError:
            fail(
                "AREA-FIT-INPUT",
                f"required input is unavailable: {relative}",
                exit_code=2,
            )
        is_last = index == len(relative.parts) - 1
        if stat.S_ISLNK(metadata.st_mode):
            fail(
                "AREA-FIT-INPUT",
                f"required input is unavailable: {relative}",
                exit_code=2,
            )
        if not is_last and not stat.S_ISDIR(metadata.st_mode):
            fail(
                "AREA-FIT-INPUT",
                f"required input is unavailable: {relative}",
                exit_code=2,
            )
        if is_last and not stat.S_ISREG(metadata.st_mode):
            fail(
                "AREA-FIT-INPUT",
                f"required input is not a regular file: {relative}",
                exit_code=2,
            )

    try:
        candidate.resolve(strict=True).relative_to(repository_root)
    except (OSError, ValueError):
        fail(
            "AREA-FIT-INPUT",
            f"required input is unavailable: {relative}",
            exit_code=2,
        )
    return candidate


def load_json(root: Path, relative: PurePosixPath) -> Any:
    path = _resolve_regular_file(root, relative)
    try:
        return parse_json_text(path.read_text(encoding="utf-8"), str(relative))
    except OSError:
        fail(
            "AREA-FIT-INPUT",
            f"required input cannot be read: {relative}",
            exit_code=2,
        )


def _scan_sensitive(value: Any, path: str = "<root>") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = re.sub(r"[^a-z0-9_]", "", key.lower())
            if normalized in PROHIBITED_KEY_NAMES:
                fail(
                    "AREA-FIT-SENSITIVE-CONTENT",
                    f"forbidden key at {path}/{key}",
                )
            _scan_sensitive(nested, f"{path}/{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            _scan_sensitive(nested, f"{path}/{index}")
        return
    if isinstance(value, str):
        lowered = value.lower()
        if any(fragment in lowered for fragment in PROHIBITED_VALUE_FRAGMENTS):
            fail(
                "AREA-FIT-SENSITIVE-CONTENT",
                f"secret-like value at {path}",
            )


def _validate_schema(root: Path, contract: dict[str, Any]) -> None:
    schema = load_json(root, SCHEMA_PATH)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # pragma: no cover - jsonschema detail is versioned
        fail("AREA-FIT-SCHEMA-DEFINITION", str(exc), exit_code=2)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            error.message,
        ),
    )
    if not errors:
        return
    error = errors[0]
    path = "/".join(str(part) for part in error.absolute_path) or "<root>"
    code = (
        "AREA-FIT-UNSUPPORTED-FIELD"
        if error.validator in {"additionalProperties", "unevaluatedProperties"}
        else "AREA-FIT-SCHEMA"
    )
    fail(code, f"{path}: {error.message}")


def _require_exact_sequence(
    actual: Any,
    expected: tuple[str, ...],
    code: str,
    label: str,
) -> None:
    if not isinstance(actual, list) or tuple(actual) != expected:
        fail(code, f"{label} must equal {expected!r}")


def _validate_cutoff_fields(contract: dict[str, Any]) -> None:
    cutoff = contract.get("authoritativeCutoff")
    if not isinstance(cutoff, dict):
        fail("AREA-FIT-CUTOFF", "authoritativeCutoff must be an object")
    expected = {
        "authorityRef": AUTHORITATIVE_CUTOFF_REF,
        "localTime": AUTHORITATIVE_LOCAL,
        "utc": AUTHORITATIVE_UTC,
        "timezone": "Asia/Seoul",
    }
    if any(cutoff.get(key) != value for key, value in expected.items()):
        fail(
            "AREA-FIT-CUTOFF",
            "fixed cutoff differs from the Spec 042 provider evidence boundary",
        )


def _validate_authority_boundary(contract: dict[str, Any]) -> None:
    boundaries = contract.get("authorityBoundaries")
    if not isinstance(boundaries, dict):
        fail("AREA-FIT-CUTOFF-AUTHORITY", "authorityBoundaries is missing")
    if boundaries.get("providerRuntimeEvidenceAuthority") is not True:
        fail(
            "AREA-FIT-CUTOFF-AUTHORITY",
            "provider-runtime-evidence must remain cutoff authority",
        )
    if (
        boundaries.get("harnessObservationUse")
        != "repository-observation-only"
        or boundaries.get("harnessProviderModelAuthority") is not False
    ):
        fail(
            "AREA-FIT-CUTOFF-AUTHORITY",
            "harness sourceObservationCutoff cannot grant provider/model authority",
        )


def _validate_external_authorities(root: Path, contract: dict[str, Any]) -> None:
    evidence = load_json(root, PROVIDER_EVIDENCE_PATH)
    evidence_cutoff = evidence.get("cutoff") if isinstance(evidence, dict) else None
    if not isinstance(evidence_cutoff, dict):
        fail(
            "AREA-FIT-CUTOFF-AUTHORITY",
            "provider runtime evidence cutoff is missing",
        )
    expected_evidence = {
        "localTime": AUTHORITATIVE_LOCAL,
        "utc": AUTHORITATIVE_UTC,
        "timezone": "Asia/Seoul",
    }
    if any(
        evidence_cutoff.get(key) != value
        for key, value in expected_evidence.items()
    ):
        fail(
            "AREA-FIT-CUTOFF-AUTHORITY",
            "provider runtime evidence cutoff drifted",
        )
    cutoff = contract["authoritativeCutoff"]
    if (
        cutoff["localTime"] != evidence_cutoff["localTime"]
        or cutoff["utc"] != evidence_cutoff["utc"]
    ):
        fail(
            "AREA-FIT-CUTOFF-AUTHORITY",
            "model fitness cutoff does not match provider runtime evidence",
        )

    harness = load_json(root, HARNESS_PATH)
    if not isinstance(harness, dict) or not isinstance(
        harness.get("sourceObservationCutoff"), str
    ):
        fail("AREA-FIT-HARNESS", "harness observation metadata is missing")
    target = harness.get("targetInventory")
    if not isinstance(target, dict) or target.get("state") != "target-only":
        fail("AREA-FIT-HARNESS", "harness target inventory must remain target-only")
    _require_exact_sequence(
        target.get("roleIds"), ROLE_IDS, "AREA-FIT-HARNESS", "target roleIds"
    )
    _require_exact_sequence(
        target.get("surfaceIds"),
        PROVIDER_IDS,
        "AREA-FIT-HARNESS",
        "target surfaceIds",
    )
    expected_pairs = {
        (role_id, provider_id)
        for role_id in ROLE_IDS
        for provider_id in PROVIDER_IDS
    }
    projections = target.get("projections")
    if not isinstance(projections, list):
        fail("AREA-FIT-HARNESS", "target projections must be an array")
    actual_pairs = {
        (item.get("roleId"), item.get("surfaceId"))
        for item in projections
        if isinstance(item, dict)
    }
    if len(projections) != 48 or actual_pairs != expected_pairs:
        fail("AREA-FIT-HARNESS", "target projections must equal 12 x 4")


def _expected_tier(role_id: str) -> str:
    return "top" if role_id in TOP_ROLES else "worker"


def _expected_reasoning(role_id: str) -> str:
    if role_id == "supervisor":
        return "xhigh"
    if role_id in MEDIUM_ROLES:
        return "medium"
    return "high"


def _expected_model(role_id: str, provider_id: str) -> str:
    if role_id in MEDIUM_ROLES:
        return {
            "local": "Gemini 3.5 Flash",
            "claude": "Haiku 4.5",
            "codex": "gpt-5.6-luna",
            "gemini": "gemini-3.5-flash",
        }[provider_id]
    if role_id in TOP_ROLES:
        return {
            "local": "Gemini 3.1 Pro",
            "claude": "Opus 4.8",
            "codex": "gpt-5.6-sol",
            "gemini": "gemini-3.1-pro-preview",
        }[provider_id]
    return {
        "local": "Gemini 3.1 Pro",
        "claude": "Sonnet 5",
        "codex": "gpt-5.6-terra",
        "gemini": "gemini-3.1-pro-preview",
    }[provider_id]


def _expected_config_source(role_id: str, provider_id: str) -> str:
    if provider_id == "codex":
        return f".codex/agents/{role_id}.toml#model"
    return {
        "local": f".agents/agents/{role_id}.md#frontmatter.model",
        "claude": f".claude/agents/{role_id}.md#frontmatter.model",
        "gemini": f".gemini/agents/{role_id}.md#frontmatter.model",
    }[provider_id]


def _validate_provider_contract(providers: list[dict[str, Any]]) -> dict[str, str]:
    _require_exact_sequence(
        [provider["providerId"] for provider in providers],
        PROVIDER_IDS,
        "AREA-FIT-PROVIDER-SET",
        "providers",
    )
    lifecycle_by_candidate: dict[str, str] = {}
    for provider in providers:
        provider_id = provider["providerId"]
        expected = PROVIDER_CONTRACT[provider_id]
        for field in (
            "trackedSurface",
            "runtimeInterface",
            "modelIdentifierPlane",
            "apiVsCliBoundary",
        ):
            if provider[field] != expected[field]:
                fail(
                    "AREA-FIT-NAMESPACE",
                    f"{provider_id} {field} conflates provider identifier planes",
                )
        actual_models = tuple(
            (item["modelId"], item["lifecycle"])
            for item in provider["candidateModels"]
        )
        if actual_models != expected["candidateModels"]:
            fail(
                "AREA-FIT-PROVIDER-CONTRACT",
                f"{provider_id} candidate catalog differs",
            )
        for candidate in provider["candidateModels"]:
            if (
                candidate["candidateOnly"] is not True
                or candidate["runtimeResolution"] != "DEFER"
            ):
                fail(
                    "AREA-FIT-RUNTIME-PRECLAIM",
                    f"{provider_id}/{candidate['modelId']} is not deferred",
                )
            lifecycle_by_candidate[
                f"{provider_id}:{candidate['modelId']}"
            ] = candidate["lifecycle"]
    return lifecycle_by_candidate


def _validate_policy(policy: dict[str, Any]) -> None:
    if policy["priorityOrder"] != [
        "quality",
        "safety",
        "cost",
        "latency",
    ]:
        fail(
            "AREA-FIT-ORDERING",
            "quality and safety must precede cost and latency",
        )
    if policy["promotionRequirements"] != [
        "canary-PASS",
        "same-suite-baseline-PASS",
        "quality-threshold-PASS",
        "safety-threshold-PASS",
    ]:
        fail(
            "AREA-FIT-THRESHOLD",
            "promotion requirements differ from the closed gate",
        )
    thresholds = policy["thresholds"]
    if (
        thresholds["qualityMinimum"] != 0.9
        or thresholds["safetyMinimum"] != 1
        or thresholds["costMaximumUsd"] <= 0
        or thresholds["latencyMaximumMs"] <= 0
    ):
        fail("AREA-FIT-THRESHOLD", "fitness thresholds differ")
    fallback = policy["fallback"]
    if (
        fallback["action"] != "retain-incumbent"
        or fallback["silentFallbackAllowed"] is not False
    ):
        fail("AREA-FIT-FALLBACK", "fallback must retain the incumbent explicitly")
    rollback = policy["rollback"]
    if (
        rollback["trigger"] != "quality-or-safety-regression"
        or rollback["action"] != "restore-incumbent"
    ):
        fail("AREA-FIT-ROLLBACK", "rollback must restore the incumbent")


def _validate_tuple(
    role_id: str,
    reasoning_profile: str,
    item: dict[str, Any],
    lifecycle_by_candidate: dict[str, str],
) -> None:
    provider_id = item["providerId"]
    key = f"{provider_id}:{item['modelCandidate']}"
    if key not in lifecycle_by_candidate:
        fail(
            "AREA-FIT-UNSUPPORTED-ALIAS",
            f"{role_id}/{provider_id} uses an unsupported model alias",
        )
    if item["modelCandidate"] != _expected_model(role_id, provider_id):
        fail(
            "AREA-FIT-TUPLE-CONTRACT",
            f"{role_id}/{provider_id} candidate differs from the closed tuple",
        )
    if item["reasoningEffort"] != reasoning_profile:
        fail(
            "AREA-FIT-REASONING",
            f"{role_id}/{provider_id} reasoning effort differs from role profile",
        )
    config_source = item["configSource"]
    path_part = config_source.split("#", 1)[0]
    parsed_path = PurePosixPath(path_part)
    if (
        parsed_path.is_absolute()
        or ".." in parsed_path.parts
        or config_source != _expected_config_source(role_id, provider_id)
    ):
        fail(
            "AREA-FIT-SCOPE",
            f"{role_id}/{provider_id} config source escapes its tracked surface",
        )

    is_preview = lifecycle_by_candidate[key] == "preview"
    if is_preview and (
        item["promotionState"] != "candidate-only"
        or item["decision"] == "PASS"
        or item["canary"]["verdict"] == "PASS"
    ):
        fail(
            "AREA-FIT-PREVIEW-PROMOTION",
            f"{role_id}/{provider_id} preview model was promoted",
        )
    if item["promotionState"] != "candidate-only":
        fail(
            "AREA-FIT-PROMOTION",
            f"{role_id}/{provider_id} is not candidate-only",
        )
    if item["state"] != "pending":
        fail(
            "AREA-FIT-STATE",
            f"{role_id}/{provider_id} must remain pending before AREA-004",
        )
    if item["canary"] != {"ref": CANARY_REF, "verdict": "DEFER"}:
        fail(
            "AREA-FIT-CANARY",
            f"{role_id}/{provider_id} canary is not deferred",
        )
    if item["sameSuiteBaseline"] != {
        "ref": BASELINE_REF,
        "verdict": "DEFER",
    }:
        fail(
            "AREA-FIT-BASELINE",
            f"{role_id}/{provider_id} same-suite baseline is not deferred",
        )
    if item["policyRef"] != "#/evaluationPolicy":
        fail("AREA-FIT-THRESHOLD", f"{role_id}/{provider_id} policy ref differs")
    if set(item["runtime"].values()) != {"DEFER"}:
        fail(
            "AREA-FIT-RUNTIME-PRECLAIM",
            f"{role_id}/{provider_id} claims runtime evidence",
        )
    if item["fallback"] != "retain-incumbent":
        fail(
            "AREA-FIT-FALLBACK",
            f"{role_id}/{provider_id} fallback does not retain incumbent",
        )
    if item["decision"] != "DEFER":
        fail(
            "AREA-FIT-DECISION",
            f"{role_id}/{provider_id} decision precedes AREA-004",
        )
    if item["rollback"] != "pending":
        fail(
            "AREA-FIT-ROLLBACK",
            f"{role_id}/{provider_id} rollback state precedes evaluation",
        )


def validate_contract(
    root: Path,
    contract: dict[str, Any] | None = None,
) -> dict[str, int]:
    """Validate production or supplied model-fitness contract data."""

    root = Path(root)
    if contract is None:
        loaded = load_json(root, CONTRACT_PATH)
        if not isinstance(loaded, dict):
            fail("AREA-FIT-SCHEMA", "contract root must be an object")
        contract = loaded
    if not isinstance(contract, dict):
        fail("AREA-FIT-SCHEMA", "contract root must be an object")

    _scan_sensitive(contract)
    _validate_cutoff_fields(contract)
    _validate_authority_boundary(contract)
    _validate_schema(root, contract)

    if contract["ownerSpec"] != OWNER_SPEC:
        fail("AREA-FIT-OWNER", "ownerSpec must be Spec 044")
    if (
        contract["contractMode"] != "contract-only"
        or contract["evidenceClass"] != "repo-static"
        or contract["lifecycleState"] != "pre-area004"
    ):
        fail("AREA-FIT-STATE", "production contract must remain pre-AREA-004")
    if set(contract["runtimeBoundaries"].values()) != {"DEFER"}:
        fail(
            "AREA-FIT-RUNTIME-PRECLAIM",
            "runtime resolution, auth, and live execution must be DEFER",
        )

    _validate_external_authorities(root, contract)
    _validate_policy(contract["evaluationPolicy"])
    providers = contract["providers"]
    lifecycle_by_candidate = _validate_provider_contract(providers)

    profiles = contract["roleProfiles"]
    _require_exact_sequence(
        [profile["roleId"] for profile in profiles],
        ROLE_IDS,
        "AREA-FIT-ROLE-SET",
        "roleProfiles",
    )
    tuple_count = 0
    pending = 0
    deferred = 0
    for profile in profiles:
        role_id = profile["roleId"]
        if profile["capabilityTier"] != _expected_tier(role_id):
            fail("AREA-FIT-TIER", f"{role_id} capability tier differs")
        expected_reasoning = _expected_reasoning(role_id)
        if profile["reasoningProfile"] != expected_reasoning:
            fail("AREA-FIT-REASONING", f"{role_id} reasoning profile differs")
        tuples = profile["providerTuples"]
        _require_exact_sequence(
            [item["providerId"] for item in tuples],
            PROVIDER_IDS,
            "AREA-FIT-TUPLE-SET",
            f"{role_id} providerTuples",
        )
        for item in tuples:
            tuple_count += 1
            _validate_tuple(
                role_id,
                expected_reasoning,
                item,
                lifecycle_by_candidate,
            )
            pending += int(item["state"] == "pending")
            deferred += int(item["decision"] == "DEFER")
    if tuple_count != 48:
        fail("AREA-FIT-TUPLE-SET", "role/provider tuple count must be 48")

    return {
        "roles": len(profiles),
        "providers": len(providers),
        "tuples": tuple_count,
        "pending": pending,
        "deferred": deferred,
    }


def apply_fixture_mutation(contract: dict[str, Any], name: str) -> None:
    """Apply one closed synthetic negative mutation."""

    if name == "duplicate-json-key":
        parse_json_text('{"schemaVersion": 1, "schemaVersion": 2}', "<fixture>")
    elif name == "unsupported-field":
        contract["unsupportedRuntimeClaim"] = True
    elif name == "unsupported-alias":
        contract["roleProfiles"][0]["providerTuples"][1][
            "modelCandidate"
        ] = "claude-opus-latest"
    elif name == "runtime-preclaim":
        contract["roleProfiles"][0]["providerTuples"][0]["runtime"][
            "modelResolution"
        ] = "PASS"
    elif name == "preview-promotion":
        contract["roleProfiles"][0]["providerTuples"][3][
            "promotionState"
        ] = "current"
    elif name == "secret-like-value":
        contract["roleProfiles"][3]["providerTuples"][2][
            "modelCandidate"
        ] = "sk-synthetic-fixture"
    elif name == "scope-escape":
        contract["roleProfiles"][0]["providerTuples"][0][
            "configSource"
        ] = "../secrets/model.json#model"
    elif name == "harness-cutoff-authority":
        contract["authorityBoundaries"][
            "harnessObservationUse"
        ] = "provider-model-authority"
        contract["authorityBoundaries"]["harnessProviderModelAuthority"] = True
    elif name == "cutoff-mismatch":
        contract["authoritativeCutoff"]["utc"] = "2026-07-10T01:00:01Z"
    elif name == "tuple-provider-duplicate":
        contract["roleProfiles"][0]["providerTuples"][1][
            "providerId"
        ] = "local"
    elif name == "threshold-order":
        contract["evaluationPolicy"]["priorityOrder"] = [
            "cost",
            "quality",
            "safety",
            "latency",
        ]
    elif name == "canary-pass":
        contract["roleProfiles"][1]["providerTuples"][0]["canary"][
            "verdict"
        ] = "PASS"
    elif name == "baseline-pass":
        contract["roleProfiles"][1]["providerTuples"][0][
            "sameSuiteBaseline"
        ]["verdict"] = "PASS"
    elif name == "decision-pass":
        contract["roleProfiles"][1]["providerTuples"][0]["decision"] = "PASS"
    elif name == "fallback-change":
        contract["roleProfiles"][1]["providerTuples"][0][
            "fallback"
        ] = "fail-closed"
    elif name == "api-cli-conflation":
        contract["providers"][3]["modelIdentifierPlane"] = "gemini-cli-alias"
    else:
        fail("AREA-FIT-FIXTURE", f"unknown mutation {name!r}", exit_code=2)


def run_self_test(root: Path) -> tuple[list[str], int]:
    """Run the production contract and all named negative mutations."""

    root = Path(root)
    loaded = load_json(root, CONTRACT_PATH)
    fixture = load_json(root, FIXTURE_PATH)
    if not isinstance(loaded, dict) or not isinstance(fixture, dict):
        return ["fixture or contract root is not an object"], 0
    failures: list[str] = []
    try:
        counts = validate_contract(root, loaded)
    except ModelFitnessError as exc:
        return [f"baseline: expected PASS, got {exc.code}: {exc.detail}"], 0
    if counts != fixture.get("expected"):
        failures.append(
            f"baseline counts differ: expected={fixture.get('expected')!r} "
            f"actual={counts!r}"
        )

    mutations = fixture.get("mutations")
    if not isinstance(mutations, list):
        return failures + ["mutations must be an array"], 0
    names = tuple(
        case.get("name") for case in mutations if isinstance(case, dict)
    )
    if names != NEGATIVE_MUTATIONS:
        failures.append(
            f"mutation names differ: expected={NEGATIVE_MUTATIONS!r} actual={names!r}"
        )
    cases = 0
    for case in mutations:
        cases += 1
        name = case["name"]
        expected_rule = case["expectedRule"]
        mutated = copy.deepcopy(loaded)
        try:
            apply_fixture_mutation(mutated, name)
            validate_contract(root, mutated)
        except ModelFitnessError as exc:
            if exc.code != expected_rule:
                failures.append(
                    f"{name}: expected {expected_rule}, got {exc.code}"
                )
        else:
            failures.append(f"{name}: mutation unexpectedly passed")
    return failures, cases


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    root = args.root
    try:
        if args.self_test:
            failures, cases = run_self_test(root)
            if failures:
                for failure in failures:
                    print(f"ERR AREA-FIT-SELF-TEST {failure}", file=sys.stderr)
                return 1
            print(
                "[PASS] agent model fitness self-test passed: "
                f"cases={cases}"
            )
            return 0
        counts = validate_contract(root)
        print(
            "[PASS] agent model fitness validation passed: "
            f"roles={counts['roles']} providers={counts['providers']} "
            f"tuples={counts['tuples']} pending={counts['pending']} "
            f"deferred={counts['deferred']}"
        )
        return 0
    except ModelFitnessError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
