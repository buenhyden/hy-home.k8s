#!/usr/bin/env python3
"""Validate the closed Spec 044 AREA-004 model-fitness readiness contract."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
import tomllib
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
PROVIDER_EVIDENCE_SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/provider-runtime-evidence.schema.json"
)
PROVIDER_CONFIG_VALIDATOR_PATH = PurePosixPath(
    "scripts/validate-agent-provider-config.py"
)
EVALUATIONS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-evaluations.json"
)
EVALUATIONS_VALIDATOR_PATH = PurePosixPath(
    "scripts/validate-agent-evaluations.py"
)
ADMISSION_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-roster-admission.json"
)
HARNESS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-model-fitness.json")

OWNER_SPEC = "docs/03.specs/0044-agent-roster-evaluation-and-admission/spec.md"
AUTHORITATIVE_CUTOFF_REF = (
    "docs/00.agent-governance/contracts/"
    "provider-runtime-evidence.json#/cutoff"
)
AUTHORITATIVE_LOCAL = "2026-07-10T10:00:00+09:00"
AUTHORITATIVE_UTC = "2026-07-10T01:00:00Z"
EVALUATION_REF_PREFIX = (
    "docs/00.agent-governance/contracts/agent-evaluations.json#"
)
ROLLBACK_REF = "#/rollbackAuthority"
VERIFIED_INCUMBENT_COMMIT = (
    "e324d4c1fa49ef7e508fa07c32e7f054f5a3a05e"  # pragma: allowlist secret
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
PROVIDER_IDS = ("local", "claude", "codex", "gemini")
MEDIUM_ROLES = {"doc-writer", "wiki-curator"}
EVALUATION_THRESHOLDS = {
    "qualityMinimum": 0.9,
    "safetyMinimum": 1,
    "costMaximumUsd": 1,
    "latencyMaximumMs": 120000,
}

PROVIDER_METADATA = {
    "local": {
        "displayName": "Local repository projection",
        "trackedSurface": ".agents/agents",
        "runtimeInterface": "repo-static",
        "modelIdentifierPlane": "local-repository-label",
        "apiVsCliBoundary": (
            "repository-label-is-not-provider-api-or-cli-resolution"
        ),
        "candidateLifecycle": "repository-label",
        "limitation": "repository-label-only-no-provider-runtime",
    },
    "claude": {
        "displayName": "Claude Code",
        "trackedSurface": ".claude/agents",
        "runtimeInterface": "claude-code-cli",
        "modelIdentifierPlane": "claude-code-cli-alias",
        "apiVsCliBoundary": (
            "claude-code-cli-alias-does-not-prove-anthropic-api-resolution"
        ),
        "candidateLifecycle": "stable",
        "limitation": "configured-adapter-only-no-cli-or-api-observation",
    },
    "codex": {
        "displayName": "Codex CLI",
        "trackedSurface": ".codex/agents",
        "runtimeInterface": "codex-cli",
        "modelIdentifierPlane": "codex-cli-model-id",
        "apiVsCliBoundary": (
            "codex-cli-model-id-does-not-prove-openai-api-or-hosted-resolution"
        ),
        "candidateLifecycle": "stable",
        "limitation": "configured-adapter-only-no-cli-or-hosted-observation",
    },
    "gemini": {
        "displayName": "Gemini CLI",
        "trackedSurface": ".gemini/agents",
        "runtimeInterface": "gemini-cli",
        "modelIdentifierPlane": "gemini-cli-family-unresolved",
        "apiVsCliBoundary": (
            "gemini-api-family-does-not-prove-cli-resolution-or-auto-routing"
        ),
        "candidateLifecycle": "unresolved",
        "limitation": (
            "native-agent-surface-has-no-model-field-and-runtime-is-unresolved"
        ),
    },
}

NEGATIVE_MUTATIONS = (
    "duplicate-json-key",
    "unsupported-field",
    "lifecycle-version-drift",
    "role-order-drift",
    "tuple-provider-duplicate",
    "tuple-count-drift",
    "configured-incumbent-drift",
    "unsupported-reasoning-effort",
    "current-only-mapping-pass",
    "provider-source-id-drift",
    "provider-evidence-ref-drift",
    "suite-version-drift",
    "manifest-digest-drift",
    "adjudicator-drift",
    "fabricated-baseline-metrics",
    "fabricated-candidate-metrics",
    "quality-threshold-weakened",
    "safety-threshold-weakened",
    "cost-threshold-loosened",
    "latency-threshold-loosened",
    "threshold-pass",
    "fitness-pass",
    "promotion-pass",
    "canary-pass",
    "runtime-preclaim",
    "preview-promotion",
    "fallback-change",
    "silent-fallback",
    "rollback-weakening",
    "scope-escape",
    "harness-cutoff-authority",
    "harness-tier-authority",
    "cutoff-mismatch",
    "secret-like-value",
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


def _read_regular_bytes(root: Path, relative: PurePosixPath) -> bytes:
    try:
        root_metadata = os.lstat(root)
    except OSError:
        fail("AREA-FIT-INPUT", "repository root is unavailable", exit_code=2)
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(
        root_metadata.st_mode
    ):
        fail("AREA-FIT-INPUT", "repository root is not a directory", exit_code=2)
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        fail("AREA-FIT-INPUT", "governed input path is outside scope", exit_code=2)

    descriptors: list[int] = []
    try:
        directory_flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        root_descriptor = os.open(root, directory_flags)
        descriptors.append(root_descriptor)
        opened_root = os.fstat(root_descriptor)
        if (
            not stat.S_ISDIR(opened_root.st_mode)
            or opened_root.st_dev != root_metadata.st_dev
            or opened_root.st_ino != root_metadata.st_ino
        ):
            fail(
                "AREA-FIT-INPUT",
                "repository root identity changed during read",
                exit_code=2,
            )

        parent_descriptor = root_descriptor
        for part in relative.parts[:-1]:
            child_descriptor = os.open(
                part,
                directory_flags,
                dir_fd=parent_descriptor,
            )
            descriptors.append(child_descriptor)
            if not stat.S_ISDIR(os.fstat(child_descriptor).st_mode):
                fail(
                    "AREA-FIT-INPUT",
                    f"required input is unavailable: {relative}",
                    exit_code=2,
                )
            parent_descriptor = child_descriptor

        file_flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        if hasattr(os, "O_NONBLOCK"):
            file_flags |= os.O_NONBLOCK
        file_descriptor = os.open(
            relative.parts[-1],
            file_flags,
            dir_fd=parent_descriptor,
        )
        descriptors.append(file_descriptor)
        if not stat.S_ISREG(os.fstat(file_descriptor).st_mode):
            fail(
                "AREA-FIT-INPUT",
                f"required input is not a regular file: {relative}",
                exit_code=2,
            )

        chunks: list[bytes] = []
        while True:
            chunk = os.read(file_descriptor, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except ModelFitnessError:
        raise
    except OSError:
        fail(
            "AREA-FIT-INPUT",
            f"required input is unavailable: {relative}",
            exit_code=2,
        )
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def load_text(root: Path, relative: PurePosixPath) -> str:
    try:
        return _read_regular_bytes(root, relative).decode("utf-8")
    except UnicodeError:
        fail(
            "AREA-FIT-INPUT",
            f"required input cannot be read: {relative}",
            exit_code=2,
        )


def _load_validator_module(
    root: Path,
    relative: PurePosixPath,
    module_name: str,
    failure_code: str,
    failure_detail: str,
) -> Any:
    source = _read_regular_bytes(root, relative)
    spec = importlib.util.spec_from_loader(
        module_name,
        loader=None,
        origin=relative.as_posix(),
    )
    if spec is None:
        fail(failure_code, failure_detail, exit_code=2)
    module = importlib.util.module_from_spec(spec)
    try:
        exec(
            compile(source, relative.as_posix(), "exec"),
            module.__dict__,
        )
    except Exception:
        fail(failure_code, failure_detail, exit_code=2)
    return module


def load_json(root: Path, relative: PurePosixPath) -> Any:
    return parse_json_text(load_text(root, relative), str(relative))


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
    except Exception as exc:  # pragma: no cover - dependency detail is versioned
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


def _validate_lifecycle(contract: dict[str, Any]) -> None:
    expected = {
        "schemaVersion": 2,
        "contractVersion": "1.1.0",
        "contractMode": "repository-static-fitness-readiness",
        "evidenceClass": "repository-static",
        "lifecycleState": "repository-static-fitness-ready",
    }
    if any(contract.get(key) != value for key, value in expected.items()):
        fail(
            "AREA-FIT-LIFECYCLE",
            "AREA-004 semantic version or lifecycle state drifted",
        )
    history = contract.get("versionHistory")
    expected_history = [
        {
            "contractVersion": "1.0.0",
            "schemaVersion": 1,
            "lifecycleState": "pre-area004",
            "disposition": "superseded",
        },
        {
            "contractVersion": "1.1.0",
            "schemaVersion": 2,
            "lifecycleState": "repository-static-fitness-ready",
            "disposition": "current",
        },
    ]
    if history != expected_history:
        fail("AREA-FIT-LIFECYCLE", "versionHistory is not the closed AREA-004 history")


def _validate_cutoff_fields(contract: dict[str, Any]) -> None:
    cutoff = contract.get("authoritativeCutoff")
    expected = {
        "authorityRef": AUTHORITATIVE_CUTOFF_REF,
        "localTime": AUTHORITATIVE_LOCAL,
        "utc": AUTHORITATIVE_UTC,
        "timezone": "Asia/Seoul",
    }
    if not isinstance(cutoff, dict) or cutoff != expected:
        fail(
            "AREA-FIT-CUTOFF",
            "fixed cutoff differs from the provider evidence authority",
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
        boundaries.get("capabilityTierAuthority") != "roleProfiles"
        or boundaries.get("harnessCapabilityTierUse") != "reference-only"
    ):
        fail(
            "AREA-FIT-TIER-AUTHORITY",
            "roleProfiles must remain the capability-tier authority",
        )
    if (
        boundaries.get("harnessObservationUse")
        != "repository-observation-only"
        or boundaries.get("harnessProviderModelAuthority") is not False
    ):
        fail(
            "AREA-FIT-CUTOFF-AUTHORITY",
            "harness observation cannot grant provider/model authority",
        )


def _adapter_path(role_id: str, provider_id: str) -> PurePosixPath:
    if provider_id == "local":
        return PurePosixPath(f".agents/agents/{role_id}.md")
    if provider_id == "claude":
        return PurePosixPath(f".claude/agents/{role_id}.md")
    if provider_id == "codex":
        return PurePosixPath(f".codex/agents/{role_id}.toml")
    return PurePosixPath(f".gemini/agents/{role_id}.md")


def _config_ref(role_id: str, provider_id: str) -> str:
    path = _adapter_path(role_id, provider_id).as_posix()
    if provider_id == "codex":
        return f"{path}#model"
    return f"{path}#frontmatter.model"


def _frontmatter_model(text: str, relative: PurePosixPath) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail("AREA-FIT-ADAPTER", f"{relative} has no closed frontmatter")
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration:
        fail("AREA-FIT-ADAPTER", f"{relative} has unterminated frontmatter")
    model_values = []
    for line in lines[1:end]:
        match = re.fullmatch(r"model:\s*(.+)", line)
        if match:
            model_values.append(match.group(1).strip().strip("\"'"))
    if len(model_values) > 1:
        fail("AREA-FIT-ADAPTER", f"{relative} has duplicate model fields")
    return model_values[0] if model_values else None


def _read_adapter(root: Path, role_id: str, provider_id: str) -> tuple[str, str]:
    relative = _adapter_path(role_id, provider_id)
    text = load_text(root, relative)
    if provider_id == "codex":
        try:
            parsed = tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            fail("AREA-FIT-ADAPTER", f"{relative} is invalid TOML: {exc}")
        model = parsed.get("model")
        effort = parsed.get("model_reasoning_effort")
        if not isinstance(model, str) or not isinstance(effort, str):
            fail("AREA-FIT-ADAPTER", f"{relative} lacks model or reasoning effort")
        return model, effort
    model = _frontmatter_model(text, relative)
    if provider_id == "gemini":
        if model is not None:
            fail(
                "AREA-FIT-ADAPTER",
                f"{relative} unexpectedly declares a native model field",
            )
        return (
            "not-configurable-on-native-surface",
            "not-configurable-on-native-surface",
        )
    if model is None:
        fail("AREA-FIT-ADAPTER", f"{relative} lacks a model field")
    return model, "not-configurable-on-native-surface"


def _validate_harness(harness: dict[str, Any]) -> None:
    if not isinstance(harness.get("sourceObservationCutoff"), str):
        fail("AREA-FIT-HARNESS", "harness observation metadata is missing")
    target = harness.get("targetInventory")
    if not isinstance(target, dict) or target.get("state") != "achieved":
        fail("AREA-FIT-HARNESS", "harness target inventory must remain achieved")
    _require_exact_sequence(
        target.get("roleIds"), ROLE_IDS, "AREA-FIT-HARNESS", "target roleIds"
    )
    _require_exact_sequence(
        target.get("surfaceIds"),
        PROVIDER_IDS,
        "AREA-FIT-HARNESS",
        "target surfaceIds",
    )
    roles = harness.get("canonicalRoles")
    if not isinstance(roles, list):
        fail("AREA-FIT-HARNESS", "canonical roles must be an array")
    _require_exact_sequence(
        [role.get("id") for role in roles if isinstance(role, dict)],
        ROLE_IDS,
        "AREA-FIT-HARNESS",
        "canonical roleIds",
    )
    for role_index, role in enumerate(roles):
        semantics = role.get("adapterSemantics")
        expected_ref = (
            f"{HARNESS_PATH.parent.as_posix()}/agent-model-fitness.json"
            f"#/roleProfiles/{role_index}/capabilityTier"
        )
        if not isinstance(semantics, dict):
            fail("AREA-FIT-HARNESS", "adapter semantics must be an object")
        if {"capabilityTier", "capabilityTierClaim"} & set(semantics):
            fail(
                "AREA-FIT-TIER-AUTHORITY",
                f"{role['id']} harness semantics duplicate capability tier",
            )
        if role.get("capabilityTierRef") != expected_ref:
            fail(
                "AREA-FIT-TIER-AUTHORITY",
                f"{role['id']} harness capability tier reference drifted",
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


def _validated_source_ledger(
    evidence: dict[str, Any],
    expected_source_ids: tuple[str, ...],
) -> dict[str, dict[str, Any]]:
    ledger = evidence.get("sourceLedger")
    if not isinstance(ledger, list):
        fail("AREA-FIT-SOURCE-ID", "provider source ledger is missing")
    source_ids = tuple(
        source.get("id") if isinstance(source, dict) else None
        for source in ledger
    )
    if source_ids != expected_source_ids:
        fail(
            "AREA-FIT-SOURCE-ID",
            "provider source ledger differs from the Spec 042 fixed source set",
        )
    return {source["id"]: source for source in ledger}


def _provider_source_ids(evidence: dict[str, Any]) -> tuple[Any, ...] | None:
    ledger = evidence.get("sourceLedger")
    if not isinstance(ledger, list):
        return None
    return tuple(
        source.get("id") if isinstance(source, dict) else None
        for source in ledger
    )


def _provider_candidates_have_unknown_sources(
    evidence: dict[str, Any],
    expected_source_ids: tuple[str, ...],
) -> bool:
    providers = evidence.get("providers")
    if not isinstance(providers, list):
        return False
    known = set(expected_source_ids)
    for provider in providers:
        if not isinstance(provider, dict):
            continue
        candidates = provider.get("modelCandidates")
        if not isinstance(candidates, list):
            continue
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            source_ids = candidate.get("sourceIds")
            if isinstance(source_ids, list) and any(
                source_id not in known for source_id in source_ids
            ):
                return True
    return False


def _provider_failure_rule(
    code: str,
    evidence: dict[str, Any],
    expected_source_ids: tuple[str, ...],
) -> tuple[str, int]:
    if _provider_source_ids(evidence) != expected_source_ids:
        return "AREA-FIT-SOURCE-ID", 1
    if code in {
        "PNME-SOURCE-DUPLICATE",
        "PNME-SOURCE-SET",
        "PNME-SOURCE-COVERAGE",
    }:
        return "AREA-FIT-SOURCE-ID", 1
    if code == "PNME-SOURCE-CUTOFF":
        return "AREA-FIT-SOURCE-CLASSIFICATION", 1
    if code == "PNME-MODEL-GATE" and _provider_candidates_have_unknown_sources(
        evidence,
        expected_source_ids,
    ):
        return "AREA-FIT-SOURCE-ID", 1
    if code == "PNME-MISSING-FILE":
        return "AREA-FIT-INPUT", 2
    if code == "PNME-SENSITIVE-CONTENT":
        return "AREA-FIT-SENSITIVE-CONTENT", 1
    return "AREA-FIT-PROVIDER-EVIDENCE", 1


def _validate_full_provider_source(
    root: Path,
    evidence: dict[str, Any],
) -> tuple[str, ...]:
    _read_regular_bytes(root, PROVIDER_EVIDENCE_SCHEMA_PATH)
    module = _load_validator_module(
        root,
        PROVIDER_CONFIG_VALIDATOR_PATH,
        "hy_home_agent_provider_config_validator",
        "AREA-FIT-PROVIDER-EVIDENCE",
        "Spec 042 provider validator failed closed",
    )

    expected_source_ids = getattr(module, "SOURCE_IDS", None)
    validate_provider_contract = getattr(module, "validate_contract", None)
    if (
        not isinstance(expected_source_ids, tuple)
        or not expected_source_ids
        or any(
            not isinstance(source_id, str) or not source_id
            for source_id in expected_source_ids
        )
        or not callable(validate_provider_contract)
    ):
        fail(
            "AREA-FIT-PROVIDER-EVIDENCE",
            "Spec 042 provider validator API drifted",
            exit_code=2,
        )
    try:
        validate_provider_contract(root, evidence, check_paths=False)
    except Exception as exc:
        provider_error = getattr(module, "ProviderConfigError", None)
        if provider_error is not None and isinstance(exc, provider_error):
            rule, exit_code = _provider_failure_rule(
                exc.code,
                evidence,
                expected_source_ids,
            )
            fail(
                rule,
                "Spec 042 provider source failed validation",
                exit_code=exit_code,
            )
        fail(
            "AREA-FIT-PROVIDER-EVIDENCE",
            "Spec 042 provider validator failed closed",
            exit_code=2,
        )
    return expected_source_ids


def _derive_mapping_from_sources(
    provider_id: str,
    candidate: dict[str, Any],
    sources: dict[str, dict[str, Any]],
) -> tuple[str, str]:
    source_ids = candidate.get("sourceIds")
    if not isinstance(source_ids, list) or any(
        not isinstance(source_id, str) or not source_id for source_id in source_ids
    ):
        fail("AREA-FIT-SOURCE-ID", f"{provider_id} sourceIds are invalid")
    if len(source_ids) != len(set(source_ids)):
        fail("AREA-FIT-SOURCE-ID", f"{provider_id} sourceIds are duplicated")
    if provider_id == "local":
        if source_ids:
            fail(
                "AREA-FIT-SOURCE-ID",
                "local repository labels cannot claim provider sources",
            )
        return "repository-only", "PASS"
    if not source_ids:
        fail(
            "AREA-FIT-SOURCE-ID",
            f"{provider_id} candidate has no provider source",
        )

    applicability: set[str] = set()
    for source_id in source_ids:
        source = sources.get(source_id)
        if source is None:
            fail("AREA-FIT-SOURCE-ID", f"{provider_id} sourceId is unknown")
        if source["provider"] != provider_id:
            fail(
                "AREA-FIT-SOURCE-ALIAS",
                f"{source_id} is owned by another provider",
            )
        applicability.add(source["cutoffApplicability"])

    candidate_model = candidate.get("candidate")
    unresolved = (
        candidate.get("idResolution") == "unresolved"
        or isinstance(candidate_model, str)
        and "unresolved" in candidate_model
    )
    if applicability == {"cutoff-applicable"} and not unresolved:
        return "fixed-cutoff-source", "PASS"
    if applicability == {"current-only"} and not unresolved:
        return "current-only-source", "DEFER"
    if applicability == {"cutoff-applicable", "current-only"}:
        confidence = (
            "mixed-cutoff-current-unresolved"
            if unresolved
            else "mixed-cutoff-current"
        )
        return confidence, "DEFER"
    if applicability == {"cutoff-applicable"} and unresolved:
        return "unresolved-at-cutoff", "DEFER"
    return "current-only-unresolved", "DEFER"


def _validate_provider_evidence(
    root: Path,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    cutoff = evidence.get("cutoff")
    expected_cutoff = {
        "localTime": AUTHORITATIVE_LOCAL,
        "utc": AUTHORITATIVE_UTC,
        "timezone": "Asia/Seoul",
    }
    if cutoff != expected_cutoff:
        fail(
            "AREA-FIT-CUTOFF-AUTHORITY",
            "provider runtime evidence cutoff drifted",
        )
    expected_source_ids = _validate_full_provider_source(root, evidence)
    providers = evidence.get("providers")
    if not isinstance(providers, list):
        fail("AREA-FIT-PROVIDER-EVIDENCE", "provider evidence is missing")
    _require_exact_sequence(
        [item.get("id") for item in providers if isinstance(item, dict)],
        PROVIDER_IDS,
        "AREA-FIT-PROVIDER-EVIDENCE",
        "provider evidence order",
    )
    sources = _validated_source_ledger(evidence, expected_source_ids)
    candidates: dict[tuple[str, str], dict[str, Any]] = {}
    for provider_index, provider in enumerate(providers):
        provider_id = provider["id"]
        model_candidates = provider.get("modelCandidates")
        if not isinstance(model_candidates, list) or len(model_candidates) != 2:
            fail(
                "AREA-FIT-PROVIDER-EVIDENCE",
                f"{provider_id} must expose two role-class candidates",
            )
        _require_exact_sequence(
            [item.get("roleClass") for item in model_candidates],
            ("planning-supervisor", "worker-subagent"),
            "AREA-FIT-PROVIDER-EVIDENCE",
            f"{provider_id} role-class evidence",
        )
        for candidate_index, candidate in enumerate(model_candidates):
            source_ids = candidate.get("sourceIds")
            cutoff_confidence, mapping_readiness = (
                _derive_mapping_from_sources(provider_id, candidate, sources)
            )
            key = (provider_id, candidate["roleClass"])
            candidates[key] = {
                "candidateModel": candidate.get("candidate"),
                "sourceIds": source_ids,
                "sourceReasoningCandidate": (
                    candidate.get("effort", {}).get("candidate")
                    or "not-configurable-on-native-surface"
                ),
                "reasoningSupport": candidate.get("effort", {}).get("support"),
                "providerEvidenceRef": (
                    f"{PROVIDER_EVIDENCE_PATH.as_posix()}"
                    f"#/providers/{provider_index}/modelCandidates/{candidate_index}"
                ),
                "cutoffConfidence": cutoff_confidence,
                "mappingReadiness": mapping_readiness,
            }
    return candidates


def _evaluation_failure_rule(code: str) -> str:
    if code == "AREA-EVAL-INPUT":
        return "AREA-FIT-INPUT"
    if code in {
        "AREA-EVAL-MANIFEST",
        "AREA-EVAL-DIGEST",
        "AREA-EVAL-RECORD-CONTRACT",
        "AREA-EVAL-FIXTURE-CLASS",
        "AREA-EVAL-GRADER",
        "AREA-EVAL-EXPECTED-BEHAVIOR",
        "AREA-EVAL-BOUNDARY",
        "AREA-EVAL-PRIVACY",
    }:
        return "AREA-FIT-MANIFEST"
    if code == "AREA-EVAL-ADJUDICATION":
        return "AREA-FIT-ADJUDICATOR"
    if code == "AREA-EVAL-ROLLBACK":
        return "AREA-FIT-ROLLBACK-SOURCE"
    return "AREA-FIT-EVALUATION-SOURCE"


def _validate_full_evaluation_source(
    root: Path,
    evaluations: dict[str, Any],
    harness: dict[str, Any],
    admission: dict[str, Any],
) -> None:
    module = _load_validator_module(
        root,
        EVALUATIONS_VALIDATOR_PATH,
        "hy_home_agent_evaluations_validator",
        "AREA-FIT-EVALUATION-SOURCE",
        "AREA-003 validator cannot be loaded",
    )
    try:
        module.validate_contract(
            root,
            evaluations,
            harness_contract=harness,
            roster_admission_contract=admission,
        )
    except Exception as exc:
        evaluation_error = getattr(module, "EvaluationContractError", None)
        if evaluation_error is not None and isinstance(exc, evaluation_error):
            rule = _evaluation_failure_rule(exc.code)
            exit_code = exc.exit_code if rule == "AREA-FIT-INPUT" else 1
            fail(rule, "AREA-003 evaluation source failed validation", exit_code=exit_code)
        fail(
            "AREA-FIT-EVALUATION-SOURCE",
            "AREA-003 validator failed closed",
            exit_code=2,
        )


def _validate_evaluations(evaluations: dict[str, Any]) -> dict[str, Any]:
    if (
        evaluations.get("schemaVersion") != 2
        or evaluations.get("contractVersion") != "1.1.0"
        or evaluations.get("state") != "repository-static-evaluation-ready"
    ):
        fail(
            "AREA-FIT-EVALUATION-SOURCE",
            "AREA-003 evaluation contract lifecycle drifted",
        )
    manifest = evaluations.get("corpusManifest")
    if (
        not isinstance(manifest, dict)
        or manifest.get("manifestId") != "hy-home.k8s/agent-evaluation-corpus/v1"
        or manifest.get("manifestVersion") != "1.0.0"
        or manifest.get("recordCount") != 48
        or not isinstance(manifest.get("manifestDigest"), str)
    ):
        fail("AREA-FIT-EVALUATION-SOURCE", "AREA-003 corpus manifest drifted")
    suites = evaluations.get("roleSuites")
    if not isinstance(suites, list):
        fail("AREA-FIT-EVALUATION-SOURCE", "role suites are missing")
    _require_exact_sequence(
        [suite.get("roleId") for suite in suites if isinstance(suite, dict)],
        ROLE_IDS,
        "AREA-FIT-EVALUATION-SOURCE",
        "AREA-003 role suites",
    )
    adjudication = evaluations.get("adjudicationReadiness")
    records = (
        adjudication.get("records")
        if isinstance(adjudication, dict)
        else None
    )
    if not isinstance(records, list):
        fail("AREA-FIT-ADJUDICATOR", "adjudication readiness is missing")
    _require_exact_sequence(
        [record.get("roleId") for record in records if isinstance(record, dict)],
        ROLE_IDS,
        "AREA-FIT-ADJUDICATOR",
        "AREA-003 adjudication records",
    )
    for index, (suite, record) in enumerate(zip(suites, records, strict=True)):
        if (
            suite.get("suiteId") != f"eval/{ROLE_IDS[index]}/v1"
            or suite.get("suiteVersion") != "1.0.0"
            or suite.get("graderVersion") != "1.0.0"
            or suite.get("rubricVersion") != "1.0.0"
            or suite.get("evaluationDisposition") != "DEFER"
            or suite.get("adjudicationRef")
            != f"#/adjudicationReadiness/records/{index}"
        ):
            fail(
                "AREA-FIT-EVALUATION-SOURCE",
                f"{ROLE_IDS[index]} suite binding drifted",
            )
        if (
            record.get("adjudicationId")
            != f"adjudication/{ROLE_IDS[index]}/v1"
            or record.get("readinessDisposition") != "PASS"
            or record.get("evaluationDisposition") != "DEFER"
            or record.get("admissionDisposition") != "DEFER"
        ):
            fail(
                "AREA-FIT-ADJUDICATOR",
                f"{ROLE_IDS[index]} adjudication readiness drifted",
            )
    rollback_records = evaluations.get("rollbackRecords")
    candidate_roles = ("docs-researcher", "quality-engineer")
    if not isinstance(rollback_records, list):
        fail("AREA-FIT-ROLLBACK-SOURCE", "AREA-003 rollback records are missing")
    _require_exact_sequence(
        [
            record.get("candidateRoleId")
            for record in rollback_records
            if isinstance(record, dict)
        ],
        candidate_roles,
        "AREA-FIT-ROLLBACK-SOURCE",
        "AREA-003 rollback records",
    )
    for index, record in enumerate(rollback_records):
        role_id = candidate_roles[index]
        incumbent = record.get("incumbent")
        procedure = record.get("procedure")
        source_binding = record.get("sourceBinding")
        if (
            record.get("rollbackId") != f"rollback/{role_id}/v1"
            or record.get("rollbackVersion") != "1.0.0"
            or record.get("status") != "armed-not-executed"
            or record.get("executed") is not False
            or record.get("executionBoundary")
            != "repository-static-plan-only-no-rollback-executed"
            or record.get("executionEvidence") != "DEFER"
            or incumbent
            != {
                "roleCount": 10,
                "surfaceCount": 3,
                "adapterCount": 30,
                "commit": VERIFIED_INCUMBENT_COMMIT,
            }
            or not isinstance(procedure, dict)
            or not isinstance(source_binding, dict)
        ):
            fail(
                "AREA-FIT-ROLLBACK-SOURCE",
                f"{role_id} evaluation rollback record drifted",
            )
        steps = procedure.get("steps")
        if (
            procedure.get("reference")
            != f"{ADMISSION_PATH.as_posix()}#/candidates/{index}/rollback"
            or not isinstance(steps, list)
            or not steps
            or procedure.get("digest") != _canonical_digest(steps)
        ):
            fail(
                "AREA-FIT-ROLLBACK-SOURCE",
                f"{role_id} rollback procedure binding drifted",
            )
    return {
        "manifest": manifest,
        "suites": suites,
        "adjudication": records,
        "rollbackRecords": rollback_records,
    }


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _validate_admission(admission: dict[str, Any]) -> list[dict[str, Any]]:
    current = admission.get("currentInventory")
    candidates = admission.get("candidates")
    if (
        admission.get("state") != "repository-static-projected"
        or not isinstance(current, dict)
        or current.get("roleCount") != 12
        or current.get("surfaceCount") != 4
        or current.get("adapterCount") != 48
        or not isinstance(candidates, list)
        or len(candidates) != 2
    ):
        fail("AREA-FIT-ROLLBACK-SOURCE", "roster admission authority drifted")
    _require_exact_sequence(
        [
            candidate.get("roleId")
            for candidate in candidates
            if isinstance(candidate, dict)
        ],
        ("docs-researcher", "quality-engineer"),
        "AREA-FIT-ROLLBACK-SOURCE",
        "roster admission rollback candidates",
    )
    for candidate in candidates:
        rollback = candidate.get("rollback")
        if (
            not isinstance(rollback, dict)
            or rollback.get("state") != "armed"
            or rollback.get("restoreInventory") != "10/3/30"
            or rollback.get("reproducible") is not True
            or rollback.get("executed") is not False
            or not isinstance(rollback.get("triggers"), list)
            or not rollback["triggers"]
            or not isinstance(rollback.get("procedure"), list)
            or not rollback["procedure"]
        ):
            fail(
                "AREA-FIT-ROLLBACK-SOURCE",
                f"{candidate.get('roleId')} admission rollback drifted",
            )
    return candidates


def _validate_rollback_source_bindings(
    rollback_records: list[dict[str, Any]],
    admission_candidates: list[dict[str, Any]],
) -> None:
    for index, (record, candidate) in enumerate(
        zip(rollback_records, admission_candidates, strict=True)
    ):
        role_id = candidate["roleId"]
        source_binding = record["sourceBinding"]
        expected_candidate_ref = (
            f"{ADMISSION_PATH.as_posix()}#/candidates/{index}"
        )
        expected_rollback_ref = f"{expected_candidate_ref}/rollback"
        if source_binding != {
            "contractPath": ADMISSION_PATH.as_posix(),
            "candidateReference": expected_candidate_ref,
            "candidateRoleId": role_id,
            "rollbackReference": expected_rollback_ref,
            "rollbackDigest": _canonical_digest(candidate["rollback"]),
        }:
            fail(
                "AREA-FIT-ROLLBACK-SOURCE",
                f"{role_id} rollback source binding drifted",
            )


def _external_authorities(root: Path) -> dict[str, Any]:
    provider_evidence = load_json(root, PROVIDER_EVIDENCE_PATH)
    evaluations = load_json(root, EVALUATIONS_PATH)
    admission = load_json(root, ADMISSION_PATH)
    harness = load_json(root, HARNESS_PATH)
    if not all(
        isinstance(value, dict)
        for value in (provider_evidence, evaluations, admission, harness)
    ):
        fail("AREA-FIT-INPUT", "governed input root must be an object", exit_code=2)
    _validate_full_evaluation_source(
        root,
        evaluations,
        harness,
        admission,
    )
    _validate_harness(harness)
    admission_candidates = _validate_admission(admission)
    evaluation_contract = _validate_evaluations(evaluations)
    _validate_rollback_source_bindings(
        evaluation_contract["rollbackRecords"],
        admission_candidates,
    )
    return {
        "providerCandidates": _validate_provider_evidence(
            root,
            provider_evidence,
        ),
        "evaluations": evaluation_contract,
    }


def _expected_tier(role_id: str) -> str:
    return (
        "top"
        if role_id in {"supervisor", "incident-responder", "security-auditor"}
        else "worker"
    )


def _expected_reasoning(role_id: str, provider_id: str) -> str:
    if provider_id != "codex":
        return "not-configurable-on-native-surface"
    if role_id == "supervisor":
        return "xhigh"
    if role_id in MEDIUM_ROLES:
        return "medium"
    return "high"


def _mapping_rationale(
    role_id: str,
    provider_id: str,
    risk_tier: str,
    role_class: str,
    provider_profile: dict[str, Any],
) -> str:
    mapping_deferred = provider_profile["mappingReadiness"] == "DEFER"
    if risk_tier == "high" and mapping_deferred:
        basis = "high-risk work targets the planning-supervisor candidate class"
    elif risk_tier == "high":
        basis = "high-risk work selects the strongest fixed-cutoff class"
    elif role_id in MEDIUM_ROLES:
        basis = "bounded documentation work selects the worker class"
    else:
        basis = "standard review work selects the balanced worker class"
    confidence = provider_profile["cutoffConfidence"]
    if mapping_deferred:
        if confidence == "current-only-source":
            source_boundary = (
                "current-only evidence cannot establish fixed-cutoff readiness"
            )
        elif confidence == "mixed-cutoff-current-unresolved":
            source_boundary = (
                "mixed cutoff/current evidence and an unresolved family defer mapping"
            )
        else:
            source_boundary = "unresolved source evidence defers mapping"
        return (
            f"{role_id} on {provider_id}: {basis}; {source_boundary}; "
            f"quality and safety precede unobserved cost and latency "
            f"({role_class})."
        )
    return (
        f"{role_id} on {provider_id}: {basis}; quality and safety precede "
        f"unobserved cost and latency ({role_class})."
    )


def _expected_limitation(
    provider_id: str,
    provider_profile: dict[str, Any],
) -> str:
    confidence = provider_profile["cutoffConfidence"]
    if confidence == "current-only-source":
        return "current-only-source-no-fixed-cutoff-or-runtime-evidence"
    if confidence == "mixed-cutoff-current-unresolved":
        return (
            "mixed-cutoff-current-source-and-unresolved-family-"
            "no-runtime-evidence"
        )
    return PROVIDER_METADATA[provider_id]["limitation"]


def _validate_policy(policy: dict[str, Any]) -> None:
    if policy.get("priorityOrder") != [
        "quality",
        "safety",
        "cost",
        "latency",
    ]:
        fail("AREA-FIT-ORDERING", "quality and safety must precede cost and latency")
    if policy.get("sameSuiteRequired") is not True:
        fail("AREA-FIT-THRESHOLD", "same-suite comparison is mandatory")
    if policy.get("thresholds") != EVALUATION_THRESHOLDS:
        fail(
            "AREA-FIT-THRESHOLD",
            "evaluation thresholds differ from the fixed AREA-004 policy",
        )
    if policy.get("promotionRequirements") != [
        "observed-fitness-PASS",
        "independent-adjudication-PASS",
        "canary-PASS",
        "same-suite-baseline-PASS",
        "quality-threshold-PASS",
        "safety-threshold-PASS",
    ]:
        fail("AREA-FIT-THRESHOLD", "promotion requirements differ")
    if policy.get("validatorPassMeaning") != "mapping-readiness-only":
        fail("AREA-FIT-DECISION-PLANE", "validator PASS meaning is ambiguous")


def _validate_provider_profiles(
    providers: list[dict[str, Any]],
    evidence_candidates: dict[tuple[str, str], dict[str, Any]],
) -> dict[tuple[str, str], dict[str, Any]]:
    _require_exact_sequence(
        [provider.get("providerId") for provider in providers],
        PROVIDER_IDS,
        "AREA-FIT-PROVIDER-SET",
        "providers",
    )
    profiles: dict[tuple[str, str], dict[str, Any]] = {}
    for provider in providers:
        provider_id = provider["providerId"]
        metadata = PROVIDER_METADATA[provider_id]
        for field in (
            "displayName",
            "trackedSurface",
            "runtimeInterface",
            "modelIdentifierPlane",
            "apiVsCliBoundary",
        ):
            if provider.get(field) != metadata[field]:
                fail(
                    "AREA-FIT-NAMESPACE",
                    f"{provider_id} {field} differs from the closed namespace",
                )
        candidates = provider.get("roleClassCandidates")
        if not isinstance(candidates, list):
            fail("AREA-FIT-PROVIDER-CONTRACT", f"{provider_id} candidates missing")
        _require_exact_sequence(
            [item.get("roleClass") for item in candidates],
            ("planning-supervisor", "worker-subagent"),
            "AREA-FIT-PROVIDER-CONTRACT",
            f"{provider_id} candidate role classes",
        )
        for candidate in candidates:
            key = (provider_id, candidate["roleClass"])
            evidence = evidence_candidates[key]
            expected = {
                "roleClass": candidate["roleClass"],
                "candidateModel": evidence["candidateModel"],
                "sourceIds": evidence["sourceIds"],
                "sourceReasoningCandidate": evidence[
                    "sourceReasoningCandidate"
                ],
                "reasoningSupport": evidence["reasoningSupport"],
                "providerEvidenceRef": evidence["providerEvidenceRef"],
                "candidateLifecycle": metadata["candidateLifecycle"],
                "cutoffConfidence": evidence["cutoffConfidence"],
                "mappingReadiness": evidence["mappingReadiness"],
                "runtimeResolution": "DEFER",
            }
            if candidate != expected:
                if (
                    candidate.get("mappingReadiness")
                    != expected["mappingReadiness"]
                ):
                    fail(
                        "AREA-FIT-MAPPING",
                        f"{provider_id}/{candidate['roleClass']} mapping classification drifted",
                    )
                fail(
                    "AREA-FIT-PROVIDER-EVIDENCE",
                    f"{provider_id}/{candidate['roleClass']} source binding drifted",
                )
            profiles[key] = candidate
    return profiles


def _validate_contract_evaluation_bindings(
    bindings: list[dict[str, Any]],
    evaluations: dict[str, Any],
) -> None:
    _require_exact_sequence(
        [binding.get("roleId") for binding in bindings],
        ROLE_IDS,
        "AREA-FIT-EVALUATION-BINDING",
        "evaluationBindings",
    )
    manifest = evaluations["manifest"]
    for index, binding in enumerate(bindings):
        suite = evaluations["suites"][index]
        adjudicator = evaluations["adjudication"][index]
        expected = {
            "roleId": ROLE_IDS[index],
            "suiteId": suite["suiteId"],
            "suiteVersion": suite["suiteVersion"],
            "corpusManifestId": manifest["manifestId"],
            "corpusManifestVersion": manifest["manifestVersion"],
            "corpusManifestDigest": manifest["manifestDigest"],
            "fixtureManifestDigest": suite["fixtureManifestDigest"],
            "graderVersion": suite["graderVersion"],
            "rubricVersion": suite["rubricVersion"],
            "baselineRef": f"{EVALUATION_REF_PREFIX}/roleSuites/{index}",
            "adjudicatorRef": (
                f"{EVALUATION_REF_PREFIX}/adjudicationReadiness/records/{index}"
            ),
            "adjudicatorId": adjudicator["adjudicationId"],
        }
        if binding != expected:
            if (
                binding.get("suiteId") != expected["suiteId"]
                or binding.get("suiteVersion") != expected["suiteVersion"]
            ):
                fail(
                    "AREA-FIT-SUITE",
                    f"{ROLE_IDS[index]} evaluation suite binding drifted",
                )
            if (
                binding.get("corpusManifestDigest")
                != expected["corpusManifestDigest"]
                or binding.get("fixtureManifestDigest")
                != expected["fixtureManifestDigest"]
                or binding.get("graderVersion") != expected["graderVersion"]
                or binding.get("rubricVersion") != expected["rubricVersion"]
            ):
                fail(
                    "AREA-FIT-MANIFEST",
                    f"{ROLE_IDS[index]} evaluation manifest binding drifted",
                )
            if (
                binding.get("adjudicatorRef") != expected["adjudicatorRef"]
                or binding.get("adjudicatorId") != expected["adjudicatorId"]
            ):
                fail(
                    "AREA-FIT-ADJUDICATOR",
                    f"{ROLE_IDS[index]} adjudicator binding drifted",
                )
            fail(
                "AREA-FIT-EVALUATION-BINDING",
                f"{ROLE_IDS[index]} evaluation binding drifted",
            )


def _validate_preview_preclaim(
    tuple_item: dict[str, Any],
    provider_profiles: dict[tuple[str, str], dict[str, Any]],
) -> None:
    key = (tuple_item["providerId"], tuple_item["roleClass"])
    lifecycle = provider_profiles.get(key, {}).get("candidateLifecycle")
    decisions = tuple_item.get("decisions", {})
    if lifecycle == "preview" and any(
        decisions.get(field) == "PASS"
        for field in ("fitness", "promotion", "canary", "runtime")
    ):
        fail(
            "AREA-FIT-PREVIEW-PROMOTION",
            f"{tuple_item['roleId']}/{tuple_item['providerId']} preview preclaim",
        )


def _validate_preview_preclaims_before_source_binding(
    providers: list[dict[str, Any]],
    role_profiles: list[dict[str, Any]],
) -> None:
    """Reject preview success claims before source-equality checks mask them."""

    candidate_profiles: dict[tuple[str, str], dict[str, Any]] = {}
    for provider in providers:
        provider_id = provider.get("providerId")
        candidates = provider.get("roleClassCandidates")
        if not isinstance(provider_id, str) or not isinstance(candidates, list):
            continue
        for candidate in candidates:
            if isinstance(candidate, dict) and isinstance(
                candidate.get("roleClass"), str
            ):
                candidate_profiles[(provider_id, candidate["roleClass"])] = candidate
    for profile in role_profiles:
        tuples = profile.get("providerTuples")
        if not isinstance(tuples, list):
            continue
        for tuple_item in tuples:
            if isinstance(tuple_item, dict):
                _validate_preview_preclaim(tuple_item, candidate_profiles)


def _validate_tuple(
    root: Path,
    role_index: int,
    profile: dict[str, Any],
    item: dict[str, Any],
    provider_profiles: dict[tuple[str, str], dict[str, Any]],
    evaluations: dict[str, Any],
) -> None:
    role_id = profile["roleId"]
    provider_id = item["providerId"]
    risk_tier = profile["riskTier"]
    role_class = "planning-supervisor" if risk_tier == "high" else "worker-subagent"
    provider_profile = provider_profiles[(provider_id, role_class)]
    _validate_preview_preclaim(item, provider_profiles)

    if (
        item["roleId"] != role_id
        or item["roleClass"] != role_class
        or item["capabilityTier"] != profile["capabilityTier"]
        or item["riskTier"] != risk_tier
    ):
        fail("AREA-FIT-TUPLE-CONTRACT", f"{role_id}/{provider_id} identity drifted")

    incumbent_model, incumbent_effort = _read_adapter(root, role_id, provider_id)
    expected_candidate = provider_profile["candidateModel"]
    expected_effort = _expected_reasoning(role_id, provider_id)
    if (
        item["incumbentModel"] != incumbent_model
        or item["configuredValue"] != incumbent_model
        or item["configuredReasoning"] != incumbent_effort
    ):
        fail(
            "AREA-FIT-INCUMBENT-DRIFT",
            f"{role_id}/{provider_id} differs from its tracked adapter",
        )
    if item["observedValue"] != "DEFER":
        fail("AREA-FIT-RUNTIME-PRECLAIM", f"{role_id}/{provider_id} was observed")
    if item["candidateModel"] != expected_candidate:
        fail(
            "AREA-FIT-TUPLE-CONTRACT",
            f"{role_id}/{provider_id} candidate differs from fixed-cutoff evidence",
        )
    if item["reasoningCandidate"] != expected_effort:
        fail(
            "AREA-FIT-REASONING",
            f"{role_id}/{provider_id} reasoning candidate is unsupported",
        )
    if item["reasoningSupport"] != provider_profile["reasoningSupport"]:
        fail(
            "AREA-FIT-REASONING",
            f"{role_id}/{provider_id} reasoning support drifted",
        )
    if (
        item["sourceIds"] != provider_profile["sourceIds"]
        or item["cutoffConfidence"] != provider_profile["cutoffConfidence"]
    ):
        fail(
            "AREA-FIT-SOURCE-ID",
            f"{role_id}/{provider_id} source IDs or confidence drifted",
        )
    if item["providerEvidenceRef"] != provider_profile["providerEvidenceRef"]:
        fail(
            "AREA-FIT-PROVIDER-EVIDENCE",
            f"{role_id}/{provider_id} provider evidence ref drifted",
        )
    if item["configPath"] != _config_ref(role_id, provider_id):
        fail("AREA-FIT-SCOPE", f"{role_id}/{provider_id} config path drifted")
    parsed_path = PurePosixPath(item["configPath"].split("#", 1)[0])
    if parsed_path.is_absolute() or ".." in parsed_path.parts:
        fail("AREA-FIT-SCOPE", f"{role_id}/{provider_id} config path escapes scope")

    expected_evaluation = {
        "bindingRef": f"#/evaluationBindings/{role_index}",
        "baselineMetricsDigest": "DEFER",
        "candidateMetricsDigest": "DEFER",
        "thresholdResult": "DEFER",
        "adjudicatorReadiness": "PASS",
        "evaluationDisposition": "DEFER",
    }
    evaluation = item["evaluation"]
    if evaluation.get("bindingRef") != expected_evaluation["bindingRef"]:
        fail("AREA-FIT-SUITE", f"{role_id}/{provider_id} suite ref drifted")
    if evaluation.get("adjudicatorReadiness") != "PASS":
        fail(
            "AREA-FIT-ADJUDICATOR",
            f"{role_id}/{provider_id} adjudicator readiness drifted",
        )
    if evaluation.get("baselineMetricsDigest") != "DEFER":
        fail(
            "AREA-FIT-BASELINE-METRICS",
            f"{role_id}/{provider_id} fabricated baseline metrics",
        )
    if evaluation.get("candidateMetricsDigest") != "DEFER":
        fail(
            "AREA-FIT-CANDIDATE-METRICS",
            f"{role_id}/{provider_id} fabricated candidate metrics",
        )
    if evaluation.get("thresholdResult") != "DEFER":
        fail(
            "AREA-FIT-THRESHOLD-PRECLAIM",
            f"{role_id}/{provider_id} threshold was preclaimed",
        )
    if evaluation != expected_evaluation:
        fail(
            "AREA-FIT-EVALUATION-BINDING",
            f"{role_id}/{provider_id} evaluation binding drifted",
        )

    no_incumbent = provider_id == "gemini"
    expected_fallback = (
        "fail-closed-no-configurable-incumbent"
        if no_incumbent
        else "retain-configured-incumbent"
    )
    expected_target = "fail-closed" if no_incumbent else incumbent_model
    if (
        item["fallbackPolicy"] != expected_fallback
        or item["fallbackTarget"] != expected_target
    ):
        fail("AREA-FIT-FALLBACK", f"{role_id}/{provider_id} fallback weakened")
    if item["silentFallbackAllowed"] is not False:
        fail("AREA-FIT-SILENT-FALLBACK", f"{role_id}/{provider_id} is silent")
    if (
        item["rollbackRef"] != ROLLBACK_REF
        or item["rollbackState"] != "armed-not-executed"
        or item["rollbackExecutionEvidence"] != "DEFER"
    ):
        fail("AREA-FIT-ROLLBACK", f"{role_id}/{provider_id} rollback weakened")
    if item["limitation"] != _expected_limitation(
        provider_id,
        provider_profile,
    ):
        fail("AREA-FIT-LIMITATION", f"{role_id}/{provider_id} limitation drifted")
    if (
        item["retryTrigger"]
        != "provider-runtime-plus-same-suite-evaluation-evidence"
    ):
        fail("AREA-FIT-RETRY", f"{role_id}/{provider_id} retry trigger drifted")
    if item["mappingRationale"] != _mapping_rationale(
        role_id,
        provider_id,
        risk_tier,
        role_class,
        provider_profile,
    ):
        fail("AREA-FIT-RATIONALE", f"{role_id}/{provider_id} rationale drifted")

    decisions = item["decisions"]
    if (
        decisions.get("mappingReadiness")
        != provider_profile["mappingReadiness"]
    ):
        fail(
            "AREA-FIT-MAPPING",
            f"{role_id}/{provider_id} mapping classification drifted",
        )
    if decisions.get("fitness") != "DEFER":
        fail("AREA-FIT-FITNESS-PRECLAIM", f"{role_id}/{provider_id} fitness claim")
    if decisions.get("promotion") != "DEFER":
        fail(
            "AREA-FIT-PROMOTION-PRECLAIM",
            f"{role_id}/{provider_id} promotion claim",
        )
    if decisions.get("canary") != "DEFER":
        fail("AREA-FIT-CANARY-PRECLAIM", f"{role_id}/{provider_id} canary claim")
    if decisions.get("runtime") != "DEFER":
        fail("AREA-FIT-RUNTIME-PRECLAIM", f"{role_id}/{provider_id} runtime claim")


def validate_contract(
    root: Path,
    contract: dict[str, Any] | None = None,
) -> dict[str, int]:
    """Validate production or supplied AREA-004 contract data."""

    root = Path(root)
    if contract is None:
        loaded = load_json(root, CONTRACT_PATH)
        if not isinstance(loaded, dict):
            fail("AREA-FIT-SCHEMA", "contract root must be an object")
        contract = loaded
    if not isinstance(contract, dict):
        fail("AREA-FIT-SCHEMA", "contract root must be an object")

    _scan_sensitive(contract)
    _validate_lifecycle(contract)
    _validate_cutoff_fields(contract)
    _validate_authority_boundary(contract)
    _validate_schema(root, contract)
    if contract["ownerSpec"] != OWNER_SPEC:
        fail("AREA-FIT-OWNER", "ownerSpec must be Spec 044")
    if set(contract["runtimeBoundaries"].values()) != {"DEFER"}:
        fail("AREA-FIT-RUNTIME-PRECLAIM", "runtime boundaries must remain DEFER")
    rollback_authority = contract["rollbackAuthority"]
    if rollback_authority != {
        "evaluationRecordsRef": (
            f"{EVALUATIONS_PATH.as_posix()}#/rollbackRecords"
        ),
        "admissionCandidatesRef": (
            f"{ADMISSION_PATH.as_posix()}#/candidates"
        ),
        "verifiedIncumbentRef": (
            f"{ADMISSION_PATH.as_posix()}#/currentInventory"
        ),
        "state": "armed-not-executed",
        "executionEvidence": "DEFER",
    }:
        fail("AREA-FIT-ROLLBACK", "rollback authority is not AREA-003 bound")
    _validate_policy(contract["evaluationPolicy"])

    external = _external_authorities(root)
    _validate_contract_evaluation_bindings(
        contract["evaluationBindings"], external["evaluations"]
    )
    providers = contract["providers"]
    _validate_preview_preclaims_before_source_binding(
        providers,
        contract["roleProfiles"],
    )
    provider_profiles = _validate_provider_profiles(
        providers, external["providerCandidates"]
    )
    profiles = contract["roleProfiles"]
    _require_exact_sequence(
        [profile.get("roleId") for profile in profiles],
        ROLE_IDS,
        "AREA-FIT-ROLE-SET",
        "roleProfiles",
    )

    tuple_count = 0
    mapping_ready = 0
    mapping_deferred = 0
    fitness_deferred = 0
    threshold_deferred = 0
    promotion_deferred = 0
    canary_deferred = 0
    runtime_deferred = 0
    for role_index, profile in enumerate(profiles):
        role_id = profile["roleId"]
        suite = external["evaluations"]["suites"][role_index]
        if profile["capabilityTier"] != _expected_tier(role_id):
            fail("AREA-FIT-TIER", f"{role_id} capability tier differs")
        if profile["riskTier"] != suite["riskClass"]:
            fail("AREA-FIT-RISK", f"{role_id} risk tier differs from AREA-003")
        tuples = profile["providerTuples"]
        _require_exact_sequence(
            [item.get("providerId") for item in tuples],
            PROVIDER_IDS,
            "AREA-FIT-TUPLE-SET",
            f"{role_id} providerTuples",
        )
        for item in tuples:
            tuple_count += 1
            _validate_tuple(
                root,
                role_index,
                profile,
                item,
                provider_profiles,
                external["evaluations"],
            )
            decisions = item["decisions"]
            mapping_ready += int(decisions["mappingReadiness"] == "PASS")
            mapping_deferred += int(
                decisions["mappingReadiness"] == "DEFER"
            )
            fitness_deferred += int(decisions["fitness"] == "DEFER")
            threshold_deferred += int(
                item["evaluation"]["thresholdResult"] == "DEFER"
            )
            promotion_deferred += int(decisions["promotion"] == "DEFER")
            canary_deferred += int(decisions["canary"] == "DEFER")
            runtime_deferred += int(decisions["runtime"] == "DEFER")
    if tuple_count != 48:
        fail("AREA-FIT-TUPLE-SET", "role/provider tuple count must be 48")

    return {
        "roles": len(profiles),
        "providers": len(providers),
        "tuples": tuple_count,
        "mappingReady": mapping_ready,
        "mappingDeferred": mapping_deferred,
        "fitnessDeferred": fitness_deferred,
        "thresholdDeferred": threshold_deferred,
        "promotionDeferred": promotion_deferred,
        "canaryDeferred": canary_deferred,
        "runtimeDeferred": runtime_deferred,
    }


def apply_fixture_mutation(contract: dict[str, Any], name: str) -> None:
    """Apply one closed synthetic negative mutation."""

    first = contract["roleProfiles"][0]["providerTuples"][0]
    if name == "duplicate-json-key":
        parse_json_text('{"schemaVersion": 1, "schemaVersion": 2}', "<fixture>")
    elif name == "unsupported-field":
        contract["unsupportedRuntimeClaim"] = True
    elif name == "lifecycle-version-drift":
        contract["lifecycleState"] = "pre-area004"
    elif name == "role-order-drift":
        contract["roleProfiles"][0], contract["roleProfiles"][1] = (
            contract["roleProfiles"][1],
            contract["roleProfiles"][0],
        )
    elif name == "tuple-provider-duplicate":
        contract["roleProfiles"][0]["providerTuples"][1]["providerId"] = "local"
    elif name == "tuple-count-drift":
        contract["roleProfiles"][0]["providerTuples"].pop()
    elif name == "configured-incumbent-drift":
        first["configuredValue"] = "unverified-incumbent"
    elif name == "unsupported-reasoning-effort":
        first["reasoningCandidate"] = "extreme"
    elif name == "current-only-mapping-pass":
        contract["providers"][1]["roleClassCandidates"][1][
            "mappingReadiness"
        ] = "PASS"
        contract["roleProfiles"][1]["providerTuples"][1]["decisions"][
            "mappingReadiness"
        ] = "PASS"
    elif name == "provider-source-id-drift":
        contract["roleProfiles"][0]["providerTuples"][1]["sourceIds"] = [
            "codex-config-reference-current"
        ]
    elif name == "provider-evidence-ref-drift":
        first["providerEvidenceRef"] = (
            f"{PROVIDER_EVIDENCE_PATH.as_posix()}#/providers/1/modelCandidates/0"
        )
    elif name == "suite-version-drift":
        contract["evaluationBindings"][0]["suiteVersion"] = "2.0.0"
    elif name == "manifest-digest-drift":
        contract["evaluationBindings"][0]["fixtureManifestDigest"] = (
            "sha256:" + ("0" * 64)
        )
    elif name == "adjudicator-drift":
        contract["evaluationBindings"][0][
            "adjudicatorId"
        ] = "adjudication/unverified/v1"
    elif name == "fabricated-baseline-metrics":
        first["evaluation"]["baselineMetricsDigest"] = "sha256:" + ("1" * 64)
    elif name == "fabricated-candidate-metrics":
        first["evaluation"]["candidateMetricsDigest"] = "sha256:" + ("2" * 64)
    elif name == "quality-threshold-weakened":
        contract["evaluationPolicy"]["thresholds"]["qualityMinimum"] = 0.89
    elif name == "safety-threshold-weakened":
        contract["evaluationPolicy"]["thresholds"]["safetyMinimum"] = 0.99
    elif name == "cost-threshold-loosened":
        contract["evaluationPolicy"]["thresholds"]["costMaximumUsd"] = 1.01
    elif name == "latency-threshold-loosened":
        contract["evaluationPolicy"]["thresholds"][
            "latencyMaximumMs"
        ] = 120001
    elif name == "threshold-pass":
        first["evaluation"]["thresholdResult"] = "PASS"
    elif name == "fitness-pass":
        first["decisions"]["fitness"] = "PASS"
    elif name == "promotion-pass":
        first["decisions"]["promotion"] = "PASS"
    elif name == "canary-pass":
        first["decisions"]["canary"] = "PASS"
    elif name == "runtime-preclaim":
        first["decisions"]["runtime"] = "PASS"
    elif name == "preview-promotion":
        contract["providers"][0]["roleClassCandidates"][0][
            "candidateLifecycle"
        ] = "preview"
        first["decisions"]["promotion"] = "PASS"
    elif name == "fallback-change":
        first["fallbackTarget"] = "candidate"
    elif name == "silent-fallback":
        first["silentFallbackAllowed"] = True
    elif name == "rollback-weakening":
        first["rollbackState"] = "not-armed"
    elif name == "scope-escape":
        first["configPath"] = "../secrets/model.json#model"
    elif name == "harness-cutoff-authority":
        contract["authorityBoundaries"][
            "harnessObservationUse"
        ] = "provider-model-authority"
        contract["authorityBoundaries"]["harnessProviderModelAuthority"] = True
    elif name == "harness-tier-authority":
        contract["authorityBoundaries"][
            "harnessCapabilityTierUse"
        ] = "literal-owner"
    elif name == "cutoff-mismatch":
        contract["authoritativeCutoff"]["utc"] = "2026-07-10T01:00:01Z"
    elif name == "secret-like-value":
        first["candidateModel"] = "sk-synthetic-fixture"
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
                failures.append(f"{name}: expected {expected_rule}, got {exc.code}")
        else:
            failures.append(f"{name}: mutation unexpectedly passed")
    return failures, cases


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
                    print(f"ERR AREA-FIT-SELF-TEST {failure}", file=sys.stderr)
                return 1
            print(
                "[PASS] agent model fitness self-test passed: "
                f"cases={cases}"
            )
            return 0
        counts = validate_contract(args.root)
        print(
            "[PASS] agent model fitness validation passed: "
            f"roles={counts['roles']} providers={counts['providers']} "
            f"tuples={counts['tuples']} mappingReady={counts['mappingReady']} "
            f"mappingDeferred={counts['mappingDeferred']} "
            f"fitnessDeferred={counts['fitnessDeferred']} "
            f"thresholdDeferred={counts['thresholdDeferred']} "
            f"promotionDeferred={counts['promotionDeferred']} "
            f"canaryDeferred={counts['canaryDeferred']} "
            f"runtimeDeferred={counts['runtimeDeferred']}"
        )
        return 0
    except ModelFitnessError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
