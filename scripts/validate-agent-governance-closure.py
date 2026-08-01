#!/usr/bin/env python3
"""Validate the closed, secret-free Spec 046 program-closure contract."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-governance-closure.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-governance-closure.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-governance-closure.json")
PROVIDER_SOURCE_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/provider-runtime-evidence.json"
)
PROVIDER_SOURCE_SHA256 = (
    "7b51324f-7af9ac08-8898d48e-a0f52551-50ef399e-92731da5-953483bb-6e281e93".replace(
        "-", ""
    )
)
MODEL_SOURCE_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-model-fitness.json"
)
MODEL_SOURCE_SHA256 = (
    "0b872577-7f029d84-e689f2eb-8713c0b0-4197e6f9-def39fe5-02a43156-0b369fab".replace(
        "-", ""
    )
)

EXPECTED_RESULTS = ("PASS", "FAIL", "ABSENT", "DEFER")
EXPECTED_LANES = (
    "repository_static",
    "local_validation",
    "local_review",
    "provider_runtime",
    "hosted_ci",
    "remote_action",
    "live_platform",
    "actual_evaluation",
)
EXPECTED_DURABLE_CONTENT = (
    "secret-values",
    "credential-values",
    "token-values",
    "auth-cache-paths",
    "auth-cache-bodies",
    "provider-response-bodies",
    "prompt-transcripts",
    "environment-dumps",
    "shell-history",
)
EXPECTED_PREDECESSORS = (
    (
        "prd-003",
        "docs/01.requirements/003-workspace-agent-governance-platform.md",
        "active",
        "git-sha1:" + "56f19c27-2052da00-a2f5428c-80a2388d-f2fc2e14".replace("-", ""),
        "24942404-8b6ff7cd-72939341-05fcc198-cdc490cc-8f130c63-2f11a73d-0011f9fa".replace(
            "-", ""
        ),
    ),
    (
        "ard-0006",
        "docs/02.architecture/requirements/0006-workspace-agent-governance-platform.md",
        "active",
        "git-sha1:" + "38a2fe6b-90bad694-d0a9a021-c7edce8d-800e03ea".replace("-", ""),
        "61e6f3e1-dc0ae546-72161971-abe6e64e-905e4ed3-9dbed21e-35abf7fa-99036702".replace(
            "-", ""
        ),
    ),
    (
        "adr-0019",
        "docs/02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md",
        "draft",
        "git-sha1:" + "38a2fe6b-90bad694-d0a9a021-c7edce8d-800e03ea".replace("-", ""),
        "e5a3389a-2e6aa40e-c6761d53-d003680c-7a86b161-6985927c-12a20ff9-8ab0086d".replace(
            "-", ""
        ),
    ),
    (
        "spec-038",
        "docs/03.specs/038-reference-information-architecture/spec.md",
        "done",
        "git-sha1:" + "f8ad39de-4017e399-df26625f-e72ec972-04dce88e".replace("-", ""),
        "5bf32b91-5c68d52b-a35f6a77-af4ca09f-e2786551-2cbd6dec-0f9dc878-92d3963f".replace(
            "-", ""
        ),
    ),
    (
        "spec-039",
        "docs/03.specs/039-github-ci-qa-evidence/spec.md",
        "done",
        "git-sha1:" + "11a020d9-b299ae91-b7af9278-c22ed89f-fccb5cfc".replace("-", ""),
        "fee96f18-c4ec78e2-073cc6a3-b86c4167-7e2712e1-c5167a9c-7afc6d41-f762292a".replace(
            "-", ""
        ),
    ),
    (
        "spec-040",
        "docs/03.specs/040-contract-cutover-and-program-closure/spec.md",
        "done",
        "git-sha1:" + "4335ea60-76a68fe0-bbed3526-a21b92a3-9180faa7".replace("-", ""),
        "b3cb84b4-7cbe5a8e-d47cd6eb-61fc4f3b-f9c22a45-30e6bc22-5711482d-46412365".replace(
            "-", ""
        ),
    ),
    (
        "spec-041",
        "docs/03.specs/041-stage-00-agent-governance-contract/spec.md",
        "done",
        "git-sha1:" + "38a2fe6b-90bad694-d0a9a021-c7edce8d-800e03ea".replace("-", ""),
        "50c43ec3-c070910a-388fe267-df8ac1a8-38f81ce5-a09fc12f-560f72b4-e821935d".replace(
            "-", ""
        ),
    ),
    (
        "spec-042",
        "docs/03.specs/042-provider-native-runtime-and-model-evidence/spec.md",
        "done",
        "git-sha1:" + "90a7d856-98cc024e-26085ca7-caed1b01-8f78a04e".replace("-", ""),
        "03d12d5a-3bf3190d-a567147c-dc130645-eb3801dc-6239c184-98d51ce7-8fa842fb".replace(
            "-", ""
        ),
    ),
    (
        "spec-043",
        "docs/03.specs/043-agent-harness-loop-lifecycle/spec.md",
        "done",
        "git-sha1:" + "a0bc3565-988e2919-80320dec-8442405c-7ef16eb6".replace("-", ""),
        "45c34a06-94c45c5e-9a9d2199-2086241a-a5185a2a-9ab0c71e-9f5b7bf0-25abee26".replace(
            "-", ""
        ),
    ),
    (
        "spec-044",
        "docs/03.specs/044-agent-roster-evaluation-and-admission/spec.md",
        "done",
        "git-sha1:" + "42864832-c966744a-c4e5cf8c-28baa5bf-31ac2765".replace("-", ""),
        "9a394ac3-239eec49-7c577b47-16d243fc-7938c0bd-a9de99f4-e04b0a72-ed42dd71".replace(
            "-", ""
        ),
    ),
    (
        "spec-045",
        "docs/03.specs/045-agent-governance-ci-qa-cutover/spec.md",
        "done",
        "git-sha1:" + "de9a88e4-550b8754-2eb7221c-5ae7416f-e5075763".replace("-", ""),
        "c556e745-e366eb4a-f6e0cefe-16652010-2c331e34-4cafd667-af85ed77-d91f27b8".replace(
            "-", ""
        ),
    ),
)
PREDECESSOR_VALIDATOR_COMMAND = (
    "python3 scripts/validate-markdown-profiles.py --root . --mode strict"
)
EXPECTED_PROVIDERS = ("claude", "codex", "gemini")
EXPECTED_PROVIDER_OBSERVATIONS = {
    "claude": ("present", "DEFER", "DEFER", "DEFER"),
    "codex": ("present", "DEFER", "DEFER", "DEFER"),
    "gemini": ("absent", "ABSENT", "DEFER", "DEFER"),
}
EXPECTED_PROVIDER_INSTRUCTION_SOURCES = {
    "claude": ("CLAUDE.md", ".claude/settings.json", ".claude/agents/"),
    "codex": ("AGENTS.md", ".codex/config.toml", ".codex/agents/"),
    "gemini": ("GEMINI.md", ".gemini/settings.json", ".gemini/agents/"),
}
EXPECTED_PROVIDER_SURFACES = {
    "claude": ".claude/agents:repo-static-PASS/native-discovery-DEFER",
    "codex": ".codex/agents:repo-static-PASS/native-discovery-DEFER",
    "gemini": ".gemini/agents:repo-static-PASS/native-discovery-ABSENT",
}
EXPECTED_PROVIDER_CANARY_RESULTS = {
    "claude": "DEFER",
    "codex": "DEFER",
    "gemini": "ABSENT",
}
EXPECTED_MODEL_SUMMARY = {
    "sourceRef": MODEL_SOURCE_PATH.as_posix(),
    "sourceSha256": MODEL_SOURCE_SHA256,
    "validatorPassMeaning": "mapping-readiness-only",
    "roleCount": 12,
    "providerCount": 4,
    "tupleCount": 48,
    "mappingReady": 21,
    "mappingDeferred": 27,
    "fitnessDeferred": 48,
    "thresholdDeferred": 48,
    "promotionDeferred": 48,
    "canaryDeferred": 48,
    "runtimeDeferred": 48,
    "configuredProfileResult": "PASS",
    "actualFitnessResult": "DEFER",
    "actualPromotionResult": "DEFER",
}
EXPECTED_MEMORY_CLASSES = (
    "working-short-term",
    "durable-long-term",
    "domain-scoped",
    "provider-local-auxiliary",
)
MEMORY_FIELDS = (
    "id",
    "owner",
    "sensitivity",
    "promotion",
    "retention",
    "compaction",
    "archiveGc",
    "conflictHandling",
    "handoff",
)
EXPECTED_MEMORY_PROJECTION = (
    (
        "working-short-term",
        "docs/00.agent-governance/contracts/agent-loop-lifecycle.json",
        "non-secret task state only",
        "summarize to Task/progress ledger when durable",
        "task bounded",
        "replace raw context with reviewed summary",
        "discard transient scratch after promoted evidence",
        "validated repository state wins; unresolved task-state conflicts escalate",
        "handoff through Task evidence and progress ledger",
    ),
    (
        "durable-long-term",
        "docs/00.agent-governance/memory/progress.md",
        "non-sensitive redacted summary",
        "append only after validation or handoff",
        "durable until superseded by newer owner",
        "preserve source/provenance and remove raw prompts",
        "archive only through governed document lifecycle",
        "the latest validated current-owner summary supersedes without deleting provenance",
        "future tasks read summary, not private transcripts",
    ),
    (
        "domain-scoped",
        "docs/00.agent-governance/scopes/",
        "domain policy without credentials",
        "promote from reviewed implementation evidence",
        "current while scope remains active",
        "merge duplicate scope rules under current owner",
        "retire superseded scope docs through archive policy",
        "the canonical scope owner wins; ambiguous overlap escalates",
        "route by scope owner and validation surface",
    ),
    (
        "provider-local-auxiliary",
        "provider runtime",
        "private provider-local state",
        "never promote raw values; summarize only explicit non-secret result",
        "provider controlled",
        "not read by repository validators",
        "not archived in repository",
        "repository policy wins for durable claims; provider-local state never overrides it",
        "record only redacted status and retry trigger",
    ),
)
EXPECTED_QA_LANES = (
    "local_validation",
    "provider_runtime",
    "hosted_ci",
    "remote_action",
    "live_platform",
    "actual_evaluation",
)
NON_REPOSITORY_PASS_FORBIDDEN = frozenset(
    {
        "provider_runtime",
        "hosted_ci",
        "remote_action",
        "live_platform",
        "actual_evaluation",
    }
)
FORBIDDEN_DURABLE_KEY_NAMES = frozenset(
    {
        "apikey",
        "token",
        "tokens",
        "accesstoken",
        "refreshtoken",
        "secret",
        "secrets",
        "secretvalue",
        "credential",
        "credentials",
        "credentialvalue",
        "auth",
        "authdata",
        "authpath",
        "authcache",
        "authcachepath",
        "authcachebody",
        "authbody",
        "path",
        "body",
        "responsebody",
        "providerresponse",
        "providerresponsebody",
        "promptbody",
        "prompttext",
        "prompttranscript",
        "transcript",
        "env",
        "environment",
        "envdump",
        "environmentdump",
        "history",
        "shellhistory",
        "sessionhistory",
        "conversationhistory",
        "privatekey",
    }
)
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"(?i)\bsk-[a-z0-9_-]{12,}"),
    re.compile(r"(?i)\bghp_[a-z0-9]{12,}"),
    re.compile(r"(?i)\bbearer\s+[a-z0-9._~+/-]{8,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


class DuplicateKeyError(ValueError):
    """Raised when JSON input contains a duplicate object key."""


def _no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError("duplicate JSON key")
        result[key] = value
    return result


def parse_json_text(text: str, label: str) -> Any:
    """Decode JSON while rejecting duplicate keys deterministically."""

    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_pairs)
    except (json.JSONDecodeError, DuplicateKeyError) as exc:
        raise ValueError(f"{label}: invalid JSON: {exc}") from exc


def _read_regular_bytes(root: Path, relative: PurePosixPath) -> bytes:
    try:
        root_metadata = os.lstat(root)
    except OSError as exc:
        raise ValueError("repository root is unavailable") from exc
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
        raise ValueError("repository root is not a real directory")
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise ValueError("required input path is invalid")
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
            raise ValueError("repository root identity changed during read")

        parent_descriptor = root_descriptor
        for part in relative.parts[:-1]:
            child_descriptor = os.open(part, directory_flags, dir_fd=parent_descriptor)
            descriptors.append(child_descriptor)
            if not stat.S_ISDIR(os.fstat(child_descriptor).st_mode):
                raise ValueError("required input parent is not a real directory")
            parent_descriptor = child_descriptor

        file_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        file_descriptor = os.open(
            relative.parts[-1], file_flags, dir_fd=parent_descriptor
        )
        descriptors.append(file_descriptor)
        if not stat.S_ISREG(os.fstat(file_descriptor).st_mode):
            raise ValueError("required input is not a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(file_descriptor, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except ValueError:
        raise
    except OSError as exc:
        raise ValueError(f"required input cannot be read: {relative}") from exc
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def _read_regular_text(root: Path, relative: PurePosixPath) -> str:
    try:
        return _read_regular_bytes(root, relative).decode("utf-8")
    except UnicodeError as exc:
        raise ValueError(f"required input cannot be decoded: {relative}") from exc


def _load_json(root: Path, relative: PurePosixPath) -> Any:
    return parse_json_text(
        _read_regular_text(root, relative),
        relative.as_posix(),
    )


def _schema_errors(instance: Any, schema: Any) -> list[str]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        return ["invalid Draft 2020-12 schema"]
    validator = Draft202012Validator(schema)
    return [
        f"schema validation failed ({error.validator})"
        for error in sorted(
            validator.iter_errors(instance),
            key=lambda error: (
                tuple(str(part) for part in error.absolute_path),
                str(error.validator),
            ),
        )
    ]


def _normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _sensitive_content_errors(value: Any) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if _normalized_key(key) in FORBIDDEN_DURABLE_KEY_NAMES:
                errors.append("forbidden durable key")
            if any(pattern.search(key) for pattern in SENSITIVE_VALUE_PATTERNS):
                errors.append("secret-like durable key")
            errors.extend(_sensitive_content_errors(nested))
    elif isinstance(value, list):
        for nested in value:
            errors.extend(_sensitive_content_errors(nested))
    elif isinstance(value, str):
        if any(pattern.search(value) for pattern in SENSITIVE_VALUE_PATTERNS):
            errors.append("secret-like durable value")
    return errors


def _result_rows(contract: dict[str, Any]) -> list[dict[str, Any]]:
    rows = list(contract.get("predecessorCriteria", []))
    rows.extend(contract.get("qaEvidence", []))
    for provider in contract.get("providerCanaries", []):
        rows.extend(
            {
                "lane": "provider_runtime",
                "result": provider.get(key),
                "owner": provider.get("owner"),
                "limitation": provider.get("limitation"),
                "retryTrigger": provider.get("retryTrigger"),
            }
            for key in (
                "runtimeResult",
                "authResult",
                "modelDiscoveryResult",
                "canaryResult",
            )
        )
    model = contract.get("modelProfileSummary", {})
    rows.extend(
        {
            "lane": "actual_evaluation",
            "result": model.get(key),
            "owner": model.get("owner"),
            "limitation": model.get("limitation"),
            "retryTrigger": model.get("retryTrigger"),
        }
        for key in ("actualFitnessResult", "actualPromotionResult")
    )
    roster = contract.get("rosterSummary", {})
    rows.append(
        {
            "lane": "actual_evaluation",
            "result": roster.get("actualAdmissionResult"),
            "owner": roster.get("owner"),
            "limitation": roster.get("limitation"),
            "retryTrigger": roster.get("retryTrigger"),
        }
    )
    review = contract.get("reviewEvidence", {})
    rows.extend(
        {
            "lane": "local_review",
            "result": item.get("result"),
            "owner": item.get("owner"),
            "limitation": item.get("limitation"),
            "retryTrigger": item.get("retryTrigger"),
        }
        for item in review.values()
        if isinstance(item, dict)
    )
    return rows


def _validate_predecessors(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rows = contract.get("predecessorCriteria", [])
    identities = tuple((row.get("id"), row.get("owner")) for row in rows)
    expected_identities = tuple((row[0], row[1]) for row in EXPECTED_PREDECESSORS)
    if identities != expected_identities:
        errors.append(
            "predecessor criteria must equal PRD 003, ARD 0006, ADR 0019, and Specs 038-045 in order"
        )
        return errors
    metadata = tuple(
        (
            row.get("id"),
            row.get("expectedStatus"),
            row.get("implementationRef"),
            row.get("evidenceSha256"),
        )
        for row in rows
    )
    expected_metadata = tuple(
        (identity, status, implementation_ref, digest)
        for identity, _owner, status, implementation_ref, digest in EXPECTED_PREDECESSORS
    )
    if metadata != expected_metadata:
        errors.append("predecessor status, implementation ref, or digest differs")
    for row in rows:
        if (
            row.get("validatorCommand") != PREDECESSOR_VALIDATOR_COMMAND
            or row.get("reviewerVerdict") != "PASS"
        ):
            errors.append("predecessor validator or reviewer verdict differs")
        if row.get("lane") != "repository_static" or row.get("result") != "PASS":
            errors.append("predecessor must be repository_static PASS")
        if row.get("limitation") is not None or row.get("retryTrigger") is not None:
            errors.append("PASS predecessor must not carry limitation/retryTrigger")
    return errors


def _frontmatter_status(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, separator, value = line.partition(":")
        if separator and key.strip() == "status":
            return value.strip().strip("'\"")
    return None


def _validate_predecessor_sources(root: Path, contract: dict[str, Any]) -> list[str]:
    rows = contract.get("predecessorCriteria", [])
    identities = tuple((row.get("id"), row.get("owner")) for row in rows)
    expected_identities = tuple((row[0], row[1]) for row in EXPECTED_PREDECESSORS)
    if identities != expected_identities:
        return ["predecessor source identities differ"]
    errors: list[str] = []
    for row, expected in zip(rows, EXPECTED_PREDECESSORS, strict=True):
        _identity, owner, expected_status, _implementation_ref, expected_digest = (
            expected
        )
        source = _read_regular_bytes(root, PurePosixPath(owner))
        observed_digest = hashlib.sha256(source).hexdigest()
        if (
            observed_digest != expected_digest
            or row.get("evidenceSha256") != observed_digest
        ):
            errors.append("predecessor source digest differs")
        try:
            status = _frontmatter_status(source.decode("utf-8"))
        except UnicodeError:
            status = None
        if status != expected_status or row.get("expectedStatus") != status:
            errors.append("predecessor source status differs")
    return errors


def _validate_provider_source(root: Path, contract: dict[str, Any]) -> list[str]:
    source_bytes = _read_regular_bytes(root, PROVIDER_SOURCE_PATH)
    if hashlib.sha256(source_bytes).hexdigest() != PROVIDER_SOURCE_SHA256:
        return ["provider source digest differs"]
    try:
        source = parse_json_text(
            source_bytes.decode("utf-8"), PROVIDER_SOURCE_PATH.as_posix()
        )
    except UnicodeError as exc:
        raise ValueError("provider source cannot be decoded") from exc
    source_rows = source.get("providers", []) if isinstance(source, dict) else []
    by_id = {row.get("id"): row for row in source_rows if isinstance(row, dict)}
    if (
        tuple(provider for provider in EXPECTED_PROVIDERS if provider in by_id)
        != EXPECTED_PROVIDERS
    ):
        return ["provider source identities differ"]
    errors: list[str] = []
    for closure_row in contract.get("providerCanaries", []):
        provider = closure_row.get("provider")
        if provider not in EXPECTED_PROVIDERS:
            errors.append("provider source identity differs")
            continue
        source_row = by_id[provider]
        local = source_row.get("localObservation", {})
        tracked = source_row.get("trackedSurface", {})
        verdicts = source_row.get("runtimeVerdicts", {})
        expected_runtime = EXPECTED_PROVIDER_OBSERVATIONS[provider]
        if (
            local.get("observedAt") != closure_row.get("observedAt")
            or local.get("installation") != expected_runtime[0]
            or tracked.get("pathRoot")
            != closure_row.get("discoveredRoleSurface", "").split(":", 1)[0]
            or verdicts.get("repoStatic") != "PASS"
            or verdicts.get("nativeDiscovery") != expected_runtime[1]
            or verdicts.get("authenticatedRun") != expected_runtime[2]
        ):
            errors.append("provider source projection differs")
    return errors


def _validate_model_source(root: Path, contract: dict[str, Any]) -> list[str]:
    source_bytes = _read_regular_bytes(root, MODEL_SOURCE_PATH)
    if hashlib.sha256(source_bytes).hexdigest() != MODEL_SOURCE_SHA256:
        return ["model source digest differs"]
    try:
        source = parse_json_text(
            source_bytes.decode("utf-8"), MODEL_SOURCE_PATH.as_posix()
        )
    except UnicodeError as exc:
        raise ValueError("model source cannot be decoded") from exc
    profiles = source.get("roleProfiles", []) if isinstance(source, dict) else []
    tuples = [
        provider_tuple
        for profile in profiles
        if isinstance(profile, dict)
        for provider_tuple in profile.get("providerTuples", [])
        if isinstance(provider_tuple, dict)
    ]
    mapping_ready = sum(
        row.get("decisions", {}).get("mappingReadiness") == "PASS" for row in tuples
    )
    mapping_deferred = sum(
        row.get("decisions", {}).get("mappingReadiness") == "DEFER" for row in tuples
    )
    deferred_decisions = {
        key: sum(row.get("decisions", {}).get(key) == "DEFER" for row in tuples)
        for key in ("fitness", "promotion", "canary", "runtime")
    }
    threshold_deferred = sum(
        row.get("evaluation", {}).get("thresholdResult") == "DEFER" for row in tuples
    )
    configured_complete = all(
        isinstance(row.get(key), str) and row[key].strip()
        for row in tuples
        for key in ("configuredValue", "configuredReasoning", "configPath")
    )
    observed = {
        "roleCount": len(profiles),
        "providerCount": len({row.get("providerId") for row in tuples}),
        "tupleCount": len(tuples),
        "mappingReady": mapping_ready,
        "mappingDeferred": mapping_deferred,
        "fitnessDeferred": deferred_decisions["fitness"],
        "thresholdDeferred": threshold_deferred,
        "promotionDeferred": deferred_decisions["promotion"],
        "canaryDeferred": deferred_decisions["canary"],
        "runtimeDeferred": deferred_decisions["runtime"],
    }
    expected_counts = {key: EXPECTED_MODEL_SUMMARY[key] for key in observed}
    if observed != expected_counts or not configured_complete:
        return ["model source mapping-readiness projection differs"]
    model_summary = contract.get("modelProfileSummary", {})
    if model_summary.get("sourceSha256") != MODEL_SOURCE_SHA256:
        return ["model source binding differs"]
    return []


def validate_repository(
    root: Path, contract: dict[str, Any], schema: dict[str, Any]
) -> list[str]:
    """Validate the closure record plus descriptor-bound canonical sources."""

    errors = validate_contract(contract, schema)
    errors.extend(_validate_predecessor_sources(root, contract))
    errors.extend(_validate_provider_source(root, contract))
    errors.extend(_validate_model_source(root, contract))
    return errors


def _validate_providers(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rows = contract.get("providerCanaries", [])
    providers = tuple(row.get("provider") for row in rows)
    if providers != EXPECTED_PROVIDERS:
        errors.append(
            "provider canaries must be exactly claude, codex, gemini in order"
        )
        return errors
    for row in rows:
        provider = row["provider"]
        observed = (
            row.get("installation"),
            row.get("runtimeResult"),
            row.get("authResult"),
            row.get("modelDiscoveryResult"),
        )
        if observed != EXPECTED_PROVIDER_OBSERVATIONS[provider]:
            errors.append("provider observation boundary differs")
        if (
            row.get("observedAt") != "2026-07-28"
            or row.get("sourceCutoff") != "2026-07-10T10:00:00+09:00"
            or row.get("sourceRef") != PROVIDER_SOURCE_PATH.as_posix()
            or row.get("sourceSha256") != PROVIDER_SOURCE_SHA256
            or tuple(row.get("instructionSources", []))
            != EXPECTED_PROVIDER_INSTRUCTION_SOURCES[provider]
            or row.get("discoveredRoleSurface") != EXPECTED_PROVIDER_SURFACES[provider]
            or row.get("configuredModel") != "role-specific-current-policy"
            or row.get("configuredReasoning")
            != "role-specific-current-policy-or-provider-native-equivalent"
            or row.get("modelPolicyRef")
            != f"{MODEL_SOURCE_PATH.as_posix()}#/roleProfiles"
            or row.get("authClass") != "not-inspected"
            or row.get("mcpPolicySummary")
            != "tracked-policy-summary-only; runtime-resolution-not-inferred"
            or row.get("canaryResult") != EXPECTED_PROVIDER_CANARY_RESULTS[provider]
            or row.get("rollbackCleanup")
            != "no provider mutation; discard transient canary output"
        ):
            errors.append("provider canary detail boundary differs")
    return errors


def validate_contract(contract: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Return all closed-schema and Spec 046 semantic contract failures."""

    errors = _schema_errors(contract, schema)
    errors.extend(_sensitive_content_errors(contract))
    if tuple(contract.get("resultVocabulary", [])) != EXPECTED_RESULTS:
        errors.append("result vocabulary differs from the closed order")
    if tuple(contract.get("laneVocabulary", [])) != EXPECTED_LANES:
        errors.append("lane vocabulary differs from the closed order")
    if contract.get("crossLanePromotion") is not False:
        errors.append("crossLanePromotion must remain false")
    policy = contract.get("durableEvidencePolicy", {})
    if (
        policy.get("summaryOnly") is not True
        or tuple(policy.get("prohibitedContent", [])) != EXPECTED_DURABLE_CONTENT
    ):
        errors.append(
            "durable evidence policy differs from the closed summary-only boundary"
        )
    errors.extend(_validate_predecessors(contract))
    errors.extend(_validate_providers(contract))

    memory_rows = contract.get("memoryLayers", [])
    memories = tuple(row.get("id") for row in memory_rows)
    if memories != EXPECTED_MEMORY_CLASSES:
        errors.append("memory layers must equal the four closed classes in order")
    memory_projection = tuple(
        tuple(row.get(field) for field in MEMORY_FIELDS) for row in memory_rows
    )
    if memory_projection != EXPECTED_MEMORY_PROJECTION:
        errors.append(
            "memory layer ownership, sensitivity, promotion, retention, compaction, archive-GC, conflict, or handoff differs"
        )
    qa_lanes = tuple(row.get("lane") for row in contract.get("qaEvidence", []))
    if qa_lanes != EXPECTED_QA_LANES:
        errors.append("QA evidence lanes differ from the closed local/external order")

    roster = contract.get("rosterSummary", {})
    if (
        roster.get("roleCount"),
        roster.get("surfaceCount"),
        roster.get("adapterCount"),
        roster.get("repositoryStaticResult"),
    ) != (12, 4, 48, "PASS"):
        errors.append("roster summary must remain exact 12/4/48 repository-static PASS")

    model = contract.get("modelProfileSummary", {})
    observed_model_summary = {key: model.get(key) for key in EXPECTED_MODEL_SUMMARY}
    if observed_model_summary != EXPECTED_MODEL_SUMMARY:
        errors.append("model mapping-readiness summary differs")

    qa_rows = contract.get("qaEvidence", [])
    local_qa = qa_rows[0] if qa_rows and isinstance(qa_rows[0], dict) else {}
    if (
        local_qa.get("lane"),
        local_qa.get("result"),
        local_qa.get("limitation"),
        local_qa.get("retryTrigger"),
    ) != ("local_validation", "PASS", None, None):
        errors.append("local validation closure evidence differs")

    for row in _result_rows(contract):
        lane = row.get("lane")
        result = row.get("result")
        if lane in NON_REPOSITORY_PASS_FORBIDDEN and result == "PASS":
            errors.append("non-repository lane must not claim PASS")
        if result == "FAIL":
            errors.append("closure evidence must not retain FAIL")
        if result in {"ABSENT", "DEFER"} and not all(
            isinstance(row.get(key), str) and row[key].strip()
            for key in ("owner", "limitation", "retryTrigger")
        ):
            errors.append("non-PASS row lacks owner/limitation/retryTrigger")

    review = contract.get("reviewEvidence", {})
    for row in review.values():
        if row.get("result") == "PASS" and any(
            row.get(level) != 0 for level in ("critical", "important", "minor")
        ):
            errors.append("PASS review retains findings")
    return errors


def _self_test(root: Path) -> list[str]:
    schema = _load_json(root, SCHEMA_PATH)
    fixture = _load_json(root, FIXTURE_PATH)
    cases: list[tuple[str, dict[str, Any]]] = []

    def mutate(name: str, mutation: Any) -> None:
        candidate = copy.deepcopy(fixture)
        mutation(candidate)
        cases.append((name, candidate))

    mutate(
        "cross-lane promotion",
        lambda item: item.__setitem__("crossLanePromotion", True),
    )
    mutate("missing provider", lambda item: item["providerCanaries"].pop())
    mutate(
        "provider order",
        lambda item: item["providerCanaries"].reverse(),
    )
    mutate(
        "provider pass collapse",
        lambda item: item["providerCanaries"][0].__setitem__("runtimeResult", "PASS"),
    )
    mutate(
        "provider detail drift",
        lambda item: item["providerCanaries"][0].__setitem__(
            "sourceCutoff", "2026-07-10T10:00:01+09:00"
        ),
    )
    mutate("missing predecessor", lambda item: item["predecessorCriteria"].pop(0))
    mutate(
        "wrong predecessor owner",
        lambda item: item["predecessorCriteria"][0].__setitem__("owner", "platform"),
    )
    mutate(
        "predecessor digest drift",
        lambda item: item["predecessorCriteria"][0].__setitem__(
            "evidenceSha256", "0" * 64
        ),
    )
    mutate(
        "duplicate predecessor",
        lambda item: item["predecessorCriteria"].__setitem__(
            1, copy.deepcopy(item["predecessorCriteria"][0])
        ),
    )
    mutate("missing memory layer", lambda item: item["memoryLayers"].pop())
    mutate(
        "memory owner drift",
        lambda item: item["memoryLayers"][0].__setitem__("owner", "platform"),
    )
    mutate(
        "roster drift",
        lambda item: item["rosterSummary"].__setitem__("adapterCount", 47),
    )
    mutate(
        "model mapping drift",
        lambda item: item["modelProfileSummary"].__setitem__("mappingReady", 20),
    )
    mutate(
        "ownerless defer",
        lambda item: item["rosterSummary"].__setitem__("retryTrigger", ""),
    )
    mutate("missing hosted lane", lambda item: item["qaEvidence"].pop(2))
    mutate(
        "local validation not closed",
        lambda item: item["qaEvidence"][0].update(
            {
                "result": "DEFER",
                "limitation": "Fixture limitation.",
                "retryTrigger": "Fixture retry trigger.",
            }
        ),
    )
    mutate(
        "review pass with finding",
        lambda item: item["reviewEvidence"]["requirements"].update(
            {"result": "PASS", "critical": 1, "limitation": None, "retryTrigger": None}
        ),
    )
    for key in (
        "token",
        "authPath",
        "providerResponseBody",
        "promptTranscript",
        "environment",
        "shellHistory",
    ):
        mutate(
            f"forbidden durable key {key}",
            lambda item, key=key: item["handoff"].__setitem__(key, "redacted"),
        )
    mutate(
        "secret-like durable value",
        lambda item: item["handoff"].__setitem__(
            "localMerge", "sk-" + "examplecredential123"
        ),
    )
    mutate(
        "secret-like durable key",
        lambda item: item["handoff"].__setitem__(
            "sk-" + "examplecredential123", "redacted"
        ),
    )
    mutate(
        "cutoff drift",
        lambda item: item["cutoff"].__setitem__("utc", "2026-07-10T01:00:01Z"),
    )

    errors: list[str] = []
    if validate_contract(fixture, schema):
        errors.append("positive fixture failed validation")
    for name, mutated in cases:
        if not validate_contract(mutated, schema):
            errors.append(f"mutation accepted: {name}")
    try:
        parse_json_text('{"schemaVersion":1,"schemaVersion":2}', "self-test")
    except ValueError:
        pass
    else:
        errors.append("mutation accepted: duplicate JSON key")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    root = Path(args.root)
    try:
        schema = _load_json(root, SCHEMA_PATH)
        if args.self_test:
            errors = _self_test(root)
        else:
            contract = _load_json(root, CONTRACT_PATH)
            errors = validate_repository(root, contract, schema)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL agent-governance closure input: {exc}")
        return 2
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    mode = "self-test" if args.self_test else "production"
    print(f"PASS agent-governance closure {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
