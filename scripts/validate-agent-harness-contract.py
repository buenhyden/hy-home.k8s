#!/usr/bin/env python3
"""Validate the provider-neutral Stage 00 agent harness contract."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-harness-contract.json")
ROUTING_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/validation-surfaces.json"
)
CANONICAL_MEMORY_PATH = PurePosixPath(
    "docs/00.agent-governance/memory/progress.md"
)
LOOP_LIFECYCLE_SPEC = PurePosixPath(
    "docs/03.specs/043-agent-harness-loop-lifecycle/spec.md"
)
MODEL_POLICY_PATH = "docs/00.agent-governance/model-policy.md"
EVAL_OWNER_SPEC = (
    "docs/03.specs/044-agent-roster-evaluation-and-admission/spec.md"
)
SCHEMA_VERSION = 1
CONTRACT_VERSION = "1.0.0"
SOURCE_OBSERVATION_CUTOFF = "2026-07-10T10:00:00+09:00"
EVAL_ADMISSION_STATE = "repository-static-evaluation-ready"
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
TARGET_SURFACES = ("local", "claude", "codex", "gemini")
CURRENT_ROLES = TARGET_ROLES
CURRENT_SURFACES = TARGET_SURFACES
SURFACE_LAYOUT = {
    "local": (PurePosixPath(".agents/agents"), ".md"),
    "claude": (PurePosixPath(".claude/agents"), ".md"),
    "codex": (PurePosixPath(".codex/agents"), ".toml"),
    "gemini": (PurePosixPath(".gemini/agents"), ".md"),
}
EVIDENCE_CLASSES = ("repo-static", "provider-runtime", "ci", "remote-live")
HARNESS_ROUTED_SURFACES = (
    "provider-gateways",
    "agent-shared",
    "agent-claude",
    "agent-codex",
    "agent-gemini",
    "governance-documents",
    "scripts",
    "tests",
)
HARNESS_VALIDATOR = {
    "id": "agent-harness-contract",
    "argv": [
        "python3",
        "scripts/validate-agent-harness-contract.py",
        "--root",
        ".",
    ],
    "lanes": ["affected", "staged", "all-files", "ci"],
    "optional": False,
    "fallback": {
        "status": "FAIL",
        "reason": "Provider-neutral harness contract validation is required.",
    },
    "evidenceLane": "repo-static",
}
PERMISSION_CLASSES = (
    "read-only-evidence",
    "scoped-authoring",
    "orchestration",
)
MEMORY_CLASSES = (
    "working-short-term",
    "durable-long-term",
    "domain-scoped",
    "provider-local-auxiliary",
)
ADAPTER_SEMANTIC_FIELDS = (
    "responsibilities",
    "outputs",
    "prohibitedActions",
    "stopConditions",
    "handoffs",
    "capabilityTier",
    "capabilityTierClaim",
    "requiredEvidence",
)
PROHIBITED_CONTENT = (
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
CONSUMERS = (
    (
        "harness-validator",
        "scripts/validate-agent-harness-contract.py",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "roster-admission-validator",
        "scripts/validate-agent-roster-admission.py",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "role-evaluations-validator",
        "scripts/validate-agent-evaluations.py",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "model-fitness-validator",
        "scripts/validate-agent-model-fitness.py",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "harness-semantics-validator",
        "scripts/validate-agent-harness-semantics.py",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "roster-currentness-validator",
        "scripts/validate-agent-roster-currentness.py",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "harness-catalog",
        "docs/00.agent-governance/harness-catalog.md",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "harness-implementation-map",
        "docs/00.agent-governance/harness-implementation-map.md",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "provider-agents-md-note",
        "docs/00.agent-governance/providers/agents-md.md",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "provider-claude-note",
        "docs/00.agent-governance/providers/claude.md",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "provider-codex-note",
        "docs/00.agent-governance/providers/codex.md",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "provider-gemini-note",
        "docs/00.agent-governance/providers/gemini.md",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "affected-surface-selector",
        "scripts/validate-affected-surfaces.py",
        "harness-contract",
        "1.0.0",
        "current",
    ),
    (
        "repository-quality-aggregate",
        "scripts/validate-repo-quality-gates.sh",
        "harness-contract",
        "1.0.0",
        "current",
    ),
)
EVIDENCE_MAPPING = (
    ("repo-static", "repo-static", "validation-surfaces", False),
    ("provider-runtime", None, "provider-runtime-record", False),
    ("ci", "ci", "validation-surfaces", False),
    ("remote-live", "remote/live", "validation-surfaces", False),
)
PERMISSION_BEHAVIOR = {
    "read-only-evidence": (False, False),
    "scoped-authoring": (True, False),
    "orchestration": (False, True),
}
MEMORY_AUTHORITY = {
    "working-short-term": {
        "mode": "temporary-context-only",
        "repositoryFacts": False,
        "decisions": False,
        "taskStatus": False,
        "durableHandoffEvidence": False,
    },
    "durable-long-term": {
        "mode": "canonical-repository-record",
        "repositoryFacts": True,
        "decisions": True,
        "taskStatus": True,
        "durableHandoffEvidence": True,
    },
    "domain-scoped": {
        "mode": "canonical-domain-record",
        "repositoryFacts": True,
        "decisions": True,
        "taskStatus": False,
        "durableHandoffEvidence": True,
    },
    "provider-local-auxiliary": {
        "mode": "advisory-only",
        "repositoryFacts": False,
        "decisions": False,
        "taskStatus": False,
        "durableHandoffEvidence": False,
    },
}
MEMORY_PROMOTION = {
    "working-short-term": "durable-long-term",
    "durable-long-term": None,
    "domain-scoped": "durable-long-term",
    "provider-local-auxiliary": "working-short-term",
}
SENSITIVE_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{12,}", re.IGNORECASE),
    re.compile(
        r"\b(?:password|passwd|api[_-]?key|client[_-]?secret|"
        r"access[_-]?token|token|secret|"
        r"aws[_-]?secret[_-]?access[_-]?key)"
        r"\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{12,}",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:raw|full)\s+(?:provider\s+)?(?:prompt|transcript)"
        r"\s*[:=]\s*\S+",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:observed\s+)?(?:"
        r"auth[_ -]?file(?:[_ -]?(?:content|path|payload))?|"
        r"shell[_ -]?history(?:[_ -]?(?:content|payload|entry))?|"
        r"private[_ -]?diagnostic(?:[_ -]?(?:content|payload|dump))?|"
        r"(?:environment|env)[_ -]?dump|"
        r"user[_ -]?(?:configuration|config)"
        r"(?:[_ -]?(?:content|payload|dump))?)"
        r"\s*[:=]\s*\S.{7,}",
        re.IGNORECASE,
    ),
)
SENSITIVE_MUTATIONS = (
    "bare-token-assignment",
    "bare-secret-assignment",
    "aws-secret-access-key",
    "slack-token-prefix",
    "auth-file-payload",
    "auth-file-path-payload",
    "shell-history-payload",
    "observed-shell-history",
    "private-diagnostic-payload",
    "environment-dump-payload",
    "user-configuration-payload",
    "raw-prompt-payload",
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


class HarnessError(ValueError):
    """Stable harness validation failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1):
        self.code = code
        self.detail = detail
        self.exit_code = exit_code
        super().__init__(f"{code}: {detail}")


def fail(
    code: str, detail: str, *, exit_code: int = 1
) -> NoReturn:
    raise HarnessError(code, detail, exit_code=exit_code)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def decode_json_text(text: str, source: str = "<memory>") -> Any:
    """Decode JSON while rejecting duplicate object keys at every depth."""

    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except DuplicateKeyError as exc:
        fail("HARNESS-DUPLICATE-KEY", f"{source}: {exc}", exit_code=2)
    except json.JSONDecodeError as exc:
        fail("HARNESS-JSON", f"{source}: {exc}", exit_code=2)


def _strict_root(
    root: Path, code: str, detail: str, *, exit_code: int = 1
) -> Path:
    try:
        absolute = root.absolute()
        mode = os.lstat(absolute).st_mode
    except OSError as exc:
        fail(code, f"{detail}: {exc}", exit_code=exit_code)
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        fail(
            code,
            f"{detail}: expected a directory that is not a symlink",
            exit_code=exit_code,
        )
    try:
        return absolute.resolve(strict=True)
    except OSError as exc:
        fail(code, f"{detail}: {exc}", exit_code=exit_code)


def _safe_repo_path(
    root: Path,
    relative: PurePosixPath | str,
    *,
    final_kind: str,
    code: str,
    detail: str,
    exit_code: int = 1,
) -> Path:
    """Resolve a repository path without following any declared component."""

    raw = relative.as_posix() if isinstance(relative, PurePosixPath) else relative
    candidate_relative = PurePosixPath(raw)
    segments = raw.split("/")
    if (
        candidate_relative.is_absolute()
        or not segments
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        fail(
            code,
            f"{detail}: expected a normalized repository-relative path",
            exit_code=exit_code,
        )

    strict_root = _strict_root(root, code, "repository root", exit_code=exit_code)
    candidate = strict_root
    for index, segment in enumerate(segments):
        candidate = candidate / segment
        try:
            mode = os.lstat(candidate).st_mode
        except OSError as exc:
            fail(code, f"{detail}: {exc}", exit_code=exit_code)
        if stat.S_ISLNK(mode):
            fail(
                code,
                f"{detail}: symlink path component {segment!r} is forbidden",
                exit_code=exit_code,
            )
        is_final = index == len(segments) - 1
        if not is_final and not stat.S_ISDIR(mode):
            fail(
                code,
                f"{detail}: parent component {segment!r} is not a directory",
                exit_code=exit_code,
            )
        if is_final:
            expected = (
                stat.S_ISREG(mode)
                if final_kind == "file"
                else stat.S_ISDIR(mode)
            )
            if not expected:
                fail(
                    code,
                    f"{detail}: expected a regular non-symlink {final_kind}",
                    exit_code=exit_code,
                )
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(strict_root)
    except (OSError, ValueError) as exc:
        fail(
            code,
            f"{detail}: resolved path escapes the strict repository root: {exc}",
            exit_code=exit_code,
        )
    return resolved


def _safe_repo_regular_file(
    root: Path,
    relative: PurePosixPath | str,
    code: str,
    detail: str,
    *,
    exit_code: int = 1,
) -> Path:
    return _safe_repo_path(
        root,
        relative,
        final_kind="file",
        code=code,
        detail=detail,
        exit_code=exit_code,
    )


def _safe_repo_directory(
    root: Path,
    relative: PurePosixPath | str,
    code: str,
    detail: str,
) -> Path:
    return _safe_repo_path(
        root,
        relative,
        final_kind="directory",
        code=code,
        detail=detail,
    )


def load_json(
    root: Path,
    relative: PurePosixPath | str,
    *,
    code: str = "HARNESS-INPUT",
    exit_code: int = 2,
) -> Any:
    path = _safe_repo_regular_file(
        root,
        relative,
        code,
        f"JSON input {relative}",
        exit_code=exit_code,
    )
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(code, f"{path}: {exc}", exit_code=exit_code)
    return decode_json_text(text, str(path))


def _identity_values(
    values: Any, key: str, collection: str
) -> list[str]:
    if not isinstance(values, list):
        return []
    result: list[str] = []
    for item in values:
        if isinstance(item, dict) and isinstance(item.get(key), str):
            result.append(item[key])
    if len(result) != len(set(result)):
        fail(
            f"HARNESS-{collection}-DUPLICATE",
            f"{collection.lower()} identities must be unique",
        )
    return result


def _precheck_contract(contract: Any) -> None:
    if not isinstance(contract, dict):
        fail("HARNESS-SCHEMA", "contract root must be an object")
    if contract.get("schemaVersion") != SCHEMA_VERSION:
        fail(
            "HARNESS-VERSION",
            f"unsupported schemaVersion {contract.get('schemaVersion')!r}",
        )
    if contract.get("contractVersion") != CONTRACT_VERSION:
        fail(
            "HARNESS-VERSION",
            f"unsupported contractVersion {contract.get('contractVersion')!r}",
        )
    if contract.get("sourceObservationCutoff") != SOURCE_OBSERVATION_CUTOFF:
        fail(
            "HARNESS-CUTOFF",
            "source observation cutoff differs from the authoritative instant",
        )

    _identity_values(contract.get("canonicalRoles"), "id", "ROLE")
    _identity_values(contract.get("surfaces"), "id", "SURFACE")
    _identity_values(contract.get("evidenceClasses"), "id", "EVIDENCE")
    _identity_values(contract.get("permissionClasses"), "id", "PERMISSION")
    _identity_values(contract.get("consumers"), "id", "CONSUMER")
    memory = contract.get("memory")
    if isinstance(memory, dict):
        _identity_values(memory.get("classes"), "id", "MEMORY")
    for role in contract.get("canonicalRoles", []):
        if not isinstance(role, dict):
            continue
        eval_suite = role.get("evalSuite")
        if (
            isinstance(eval_suite, dict)
            and eval_suite.get("admissionState") != EVAL_ADMISSION_STATE
        ):
            fail(
                "HARNESS-EVAL",
                "role evaluation state differs from repository-static readiness",
            )
    for inventory_name in ("currentInventory", "targetInventory"):
        inventory = contract.get(inventory_name)
        if not isinstance(inventory, dict):
            continue
        expected_state = (
            "current" if inventory_name == "currentInventory" else "achieved"
        )
        if inventory.get("state") != expected_state:
            fail(
                "HARNESS-INVENTORY-STATE",
                f"{inventory_name} must remain {expected_state!r}",
            )
        projections = inventory.get("projections")
        if not isinstance(projections, list):
            continue
        keys: list[tuple[Any, Any]] = []
        for projection in projections:
            if isinstance(projection, dict):
                keys.append(
                    (projection.get("roleId"), projection.get("surfaceId"))
                )
        if len(keys) != len(set(keys)):
            fail(
                "HARNESS-PROJECTION-DUPLICATE",
                f"{inventory_name} repeats a role/surface projection",
            )

    routing = contract.get("routingContract")
    if isinstance(routing, dict) and routing.get("ownsPathRouting") is not False:
        fail(
            "HARNESS-ROUTING",
            "the harness contract must not own path-to-validation routes",
        )
    if isinstance(memory, dict):
        for memory_class in memory.get("classes", []):
            if not isinstance(memory_class, dict):
                continue
            memory_id = memory_class.get("id")
            if memory_id in MEMORY_AUTHORITY:
                if memory_class.get("authority") != MEMORY_AUTHORITY[memory_id]:
                    fail(
                        "HARNESS-MEMORY-AUTHORITY",
                        f"{memory_id} authority differs from the closed boundary",
                    )
                sensitivity = memory_class.get("sensitivity")
                if isinstance(sensitivity, dict) and (
                    sensitivity.get("secretMaterialAllowed") is not False
                    or sensitivity.get("rawPromptOrTranscriptAllowed") is not False
                ):
                    fail(
                        "HARNESS-MEMORY-SENSITIVITY",
                        f"{memory_id} permits a prohibited sensitive payload",
                    )


def _schema_errors(
    schema: dict[str, Any], contract: dict[str, Any]
) -> list[Any]:
    return sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: (
            tuple(str(part) for part in item.absolute_path),
            item.message,
        ),
    )


def _validate_schema(root: Path, contract: dict[str, Any]) -> None:
    schema = load_json(root, SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail(
            "HARNESS-SCHEMA-DEFINITION",
            "schema root must be an object",
            exit_code=2,
        )
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        fail("HARNESS-SCHEMA-DEFINITION", str(exc), exit_code=2)
    errors = _schema_errors(schema, contract)
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        fail("HARNESS-SCHEMA", f"{location}: {error.message}")


def _expected_projection(
    role_id: str, surface_id: str, admission_state: str
) -> tuple[str, str, str, str]:
    path_root, extension = SURFACE_LAYOUT[surface_id]
    path = (path_root / f"{role_id}{extension}").as_posix()
    return role_id, surface_id, path, admission_state


def _projection_tuple(projection: dict[str, Any]) -> tuple[Any, Any, Any, Any]:
    return (
        projection.get("roleId"),
        projection.get("surfaceId"),
        projection.get("path"),
        projection.get("admissionState"),
    )


def _validate_inventory(
    inventory: dict[str, Any],
    *,
    name: str,
    roles: tuple[str, ...],
    surfaces: tuple[str, ...],
    state: str,
    projection_state: str | None = None,
) -> None:
    projection_state = projection_state or state
    if inventory["state"] != state:
        fail(
            "HARNESS-INVENTORY-STATE",
            f"{name} state {inventory['state']!r}, expected {state!r}",
        )
    expected_count = len(roles) * len(surfaces)
    expected_counts = (
        len(roles),
        len(surfaces),
        expected_count,
    )
    actual_counts = (
        inventory["expectedRoleCount"],
        inventory["expectedSurfaceCount"],
        inventory["expectedProjectionCount"],
    )
    if actual_counts != expected_counts:
        fail(
            "HARNESS-INVENTORY-COUNT",
            f"{name} declared counts {actual_counts!r}, expected {expected_counts!r}",
        )
    if tuple(inventory["roleIds"]) != roles:
        fail(
            "HARNESS-ROLE-SET",
            f"{name} role order or membership differs from the closed set",
        )
    if tuple(inventory["surfaceIds"]) != surfaces:
        fail(
            "HARNESS-SURFACE-SET",
            f"{name} surface order or membership differs from the closed set",
        )
    expected = tuple(
        _expected_projection(role_id, surface_id, projection_state)
        for role_id in roles
        for surface_id in surfaces
    )
    actual = tuple(
        _projection_tuple(projection)
        for projection in inventory["projections"]
    )
    if actual != expected:
        fail(
            "HARNESS-PROJECTION-SET",
            f"{name} projection order, membership, path, or state differs",
        )


def validate_projection_files(root: Path, projections: Sequence[dict[str, Any]]) -> None:
    """Require the closed current 48 adapter files."""

    expected_paths = {
        PurePosixPath(projection["path"]) for projection in projections
    }
    for relative in sorted(expected_paths):
        _safe_repo_regular_file(
            root,
            relative,
            "HARNESS-FILE",
            f"adapter projection {relative.as_posix()}",
        )

    observed_paths_by_surface: dict[str, set[PurePosixPath]] = {}
    for surface_id in TARGET_SURFACES:
        directory, extension = SURFACE_LAYOUT[surface_id]
        absolute_directory = _safe_repo_directory(
            root,
            directory,
            "HARNESS-FILE",
            f"adapter surface {directory.as_posix()}",
        )
        try:
            entries = list(absolute_directory.iterdir())
        except OSError as exc:
            fail(
                "HARNESS-FILE",
                f"adapter surface {directory.as_posix()}: {exc}",
            )
        observed_paths: set[PurePosixPath] = set()
        for entry in entries:
            if entry.suffix != extension:
                continue
            strict_root = _strict_root(root, "HARNESS-FILE", "repository root")
            relative = PurePosixPath(entry.relative_to(strict_root).as_posix())
            _safe_repo_regular_file(
                root,
                relative,
                "HARNESS-FILE",
                f"adapter surface member {relative.as_posix()}",
            )
            observed_paths.add(relative)
        observed_paths_by_surface[surface_id] = observed_paths

    for surface_id in TARGET_SURFACES:
        directory, extension = SURFACE_LAYOUT[surface_id]
        expected_surface_paths = {
            path for path in expected_paths
            if path.parent == directory and path.suffix == extension
        }
        observed_paths = observed_paths_by_surface[surface_id]
        if observed_paths != expected_surface_paths:
            missing = sorted(
                path.as_posix() for path in expected_surface_paths - observed_paths
            )
            extra = sorted(
                path.as_posix() for path in observed_paths - expected_surface_paths
            )
            fail(
                "HARNESS-FILE",
                f"target adapter set drift for {surface_id}: missing={missing!r} extra={extra!r}",
            )


def _validate_roles(root: Path, contract: dict[str, Any]) -> None:
    roles = contract["canonicalRoles"]
    role_ids = tuple(role["id"] for role in roles)
    if role_ids != TARGET_ROLES:
        fail(
            "HARNESS-ROLE-SET",
            "canonical role order or membership differs from the 12-role target",
        )
    defined_permissions = {
        permission["id"] for permission in contract["permissionClasses"]
    }
    adapter_anchors: dict[str, tuple[str, str]] = {}
    for role in roles:
        role_id = role["id"]
        expected_state = (
            "current" if role_id in CURRENT_ROLES else "target-only"
        )
        if role["admissionState"] != expected_state:
            fail(
                "HARNESS-INVENTORY-STATE",
                f"{role_id} must remain {expected_state!r}",
            )
        if role["permissionClass"] not in defined_permissions:
            fail(
                "HARNESS-PERMISSION",
                f"{role_id} references an unknown permission class",
            )
        adapter_semantics = role["adapterSemantics"]
        expected_tier = "top" if role_id == "supervisor" else "worker"
        if (
            adapter_semantics["admissionState"] != expected_state
            or adapter_semantics["capabilityTier"] != expected_tier
        ):
            fail(
                "HARNESS-ADAPTER-SEMANTICS",
                f"{role_id} adapter semantics state or capability tier differs",
            )
        for field in ADAPTER_SEMANTIC_FIELDS:
            if field == "capabilityTier":
                continue
            values = (
                [adapter_semantics[field]]
                if field == "capabilityTierClaim"
                else adapter_semantics[field]
            )
            for value in values:
                if " ".join(value.split()) != value:
                    fail(
                        "HARNESS-ADAPTER-SEMANTICS",
                        f"{role_id}/{field} is not whitespace-normalized",
                    )
                if value in adapter_anchors:
                    other_role, other_field = adapter_anchors[value]
                    fail(
                        "HARNESS-ADAPTER-SEMANTICS",
                        f"{role_id}/{field} duplicates "
                        f"{other_role}/{other_field}",
                    )
                adapter_anchors[value] = (role_id, field)
        if not set(role["handoffs"]).issubset(TARGET_ROLES):
            fail(
                "HARNESS-HANDOFF",
                f"{role_id} has a handoff outside the canonical roster",
            )
        expected_eval = f"eval/{role_id}/v1"
        if (
            role["evalSuite"]["id"] != expected_eval
            or role["evalSuite"]["ownerSpec"] != EVAL_OWNER_SPEC
            or role["evalSuite"]["admissionState"] != EVAL_ADMISSION_STATE
        ):
            fail(
                "HARNESS-EVAL",
                f"{role_id} eval reference differs from the Spec 044 boundary",
            )
        if role["modelPolicyRef"] != MODEL_POLICY_PATH:
            fail(
                "HARNESS-MODEL-POLICY",
                f"{role_id} model policy reference differs",
            )
    _safe_repo_regular_file(
        root,
        MODEL_POLICY_PATH,
        "HARNESS-MODEL-POLICY",
        "canonical model policy",
    )
    _safe_repo_regular_file(
        root,
        EVAL_OWNER_SPEC,
        "HARNESS-EVAL",
        "Spec 044 eval owner",
    )


def _validate_surfaces(contract: dict[str, Any]) -> None:
    surfaces = contract["surfaces"]
    surface_ids = tuple(surface["id"] for surface in surfaces)
    if surface_ids != TARGET_SURFACES:
        fail(
            "HARNESS-SURFACE-SET",
            "surface order or membership differs from the four-surface target",
        )
    for surface in surfaces:
        surface_id = surface["id"]
        expected_state = (
            "current" if surface_id in CURRENT_SURFACES else "target-only"
        )
        if surface["admissionState"] != expected_state:
            fail(
                "HARNESS-INVENTORY-STATE",
                f"{surface_id} must remain {expected_state!r}",
            )
        path_root, extension = SURFACE_LAYOUT[surface_id]
        if (
            surface["pathRoot"] != path_root.as_posix()
            or surface["extension"] != extension
        ):
            fail(
                "HARNESS-SURFACE-PATH",
                f"{surface_id} path root or extension differs",
            )


def _validate_evidence(contract: dict[str, Any]) -> None:
    evidence = contract["evidenceClasses"]
    if tuple(item["id"] for item in evidence) != EVIDENCE_CLASSES:
        fail(
            "HARNESS-EVIDENCE",
            "evidence class order or membership differs",
        )
    if any(item["crossClassInferenceAllowed"] is not False for item in evidence):
        fail(
            "HARNESS-EVIDENCE",
            "an evidence class permits cross-class inference",
        )
    mapping = tuple(
        (
            item["evidenceClass"],
            item["validationSurfaceLane"],
            item["owner"],
            item["crossClassInferenceAllowed"],
        )
        for item in contract["routingContract"]["evidenceMapping"]
    )
    if mapping != EVIDENCE_MAPPING:
        fail(
            "HARNESS-EVIDENCE",
            "validation-surface evidence mapping differs",
        )


def _validate_permissions(contract: dict[str, Any]) -> None:
    permissions = contract["permissionClasses"]
    if tuple(item["id"] for item in permissions) != PERMISSION_CLASSES:
        fail(
            "HARNESS-PERMISSION",
            "permission class order or membership differs",
        )
    for permission in permissions:
        expected = PERMISSION_BEHAVIOR[permission["id"]]
        actual = (
            permission["allowsMutation"],
            permission["allowsDelegation"],
        )
        if actual != expected or permission["externalWritesRequireApproval"] is not True:
            fail(
                "HARNESS-PERMISSION",
                f"{permission['id']} permission behavior differs",
            )


def _validate_routing(root: Path, contract: dict[str, Any]) -> None:
    routing_ref = contract["routingContract"]
    if (
        routing_ref["path"] != ROUTING_PATH.as_posix()
        or routing_ref["schemaVersion"] != 2
        or routing_ref["ownership"] != "independent-path-to-validation-routing"
        or routing_ref["ownsPathRouting"] is not False
    ):
        fail("HARNESS-ROUTING", "routing owner reference differs")
    routing = load_json(
        root, ROUTING_PATH, code="HARNESS-ROUTING", exit_code=1
    )
    if not isinstance(routing, dict):
        fail("HARNESS-ROUTING", "validation-surfaces root must be an object")
    if routing.get("schemaVersion") != 2:
        fail("HARNESS-ROUTING", "validation-surfaces schemaVersion differs")
    lanes = tuple(routing.get("evidenceLanes", []))
    if lanes != ("repo-static", "ci", "remote/live"):
        fail(
            "HARNESS-ROUTING",
            "validation-surfaces evidence lanes differ from the mapped owner",
        )
    validators = routing.get("validators")
    if not isinstance(validators, list):
        fail("HARNESS-ROUTING", "validation-surfaces validators must be a list")
    harness_validators = [
        validator
        for validator in validators
        if isinstance(validator, dict)
        and validator.get("id") == HARNESS_VALIDATOR["id"]
    ]
    if harness_validators != [HARNESS_VALIDATOR]:
        fail(
            "HARNESS-ROUTING",
            "agent-harness-contract validator registration differs",
        )
    surfaces = routing.get("surfaces")
    if not isinstance(surfaces, list):
        fail("HARNESS-ROUTING", "validation-surfaces surfaces must be a list")
    routed_surfaces: list[str] = []
    for surface in surfaces:
        if not isinstance(surface, dict):
            fail("HARNESS-ROUTING", "validation surface must be an object")
        surface_validators = surface.get("validators")
        if not isinstance(surface_validators, list):
            fail(
                "HARNESS-ROUTING",
                f"surface {surface.get('id', '<missing>')} validators must be a list",
            )
        occurrences = surface_validators.count(HARNESS_VALIDATOR["id"])
        if occurrences > 1:
            fail(
                "HARNESS-ROUTING",
                f"surface {surface.get('id', '<missing>')} repeats the harness validator",
            )
        if occurrences == 1:
            routed_surfaces.append(surface.get("id"))
    if tuple(routed_surfaces) != HARNESS_ROUTED_SURFACES:
        fail(
            "HARNESS-ROUTING",
            "agent-harness-contract surface routing differs from the closed set",
        )


def _validate_consumers(root: Path, contract: dict[str, Any]) -> None:
    actual = tuple(
        (
            consumer["id"],
            consumer["path"],
            consumer["selectedContract"],
            consumer["selectedVersion"],
            consumer["migrationState"],
        )
        for consumer in contract["consumers"]
    )
    if actual != CONSUMERS:
        fail(
            "HARNESS-CONSUMER",
            "consumer order, path, selected version, or migration state differs",
        )
    for consumer in contract["consumers"]:
        _safe_repo_regular_file(
            root,
            PurePosixPath(consumer["path"]),
            "HARNESS-CONSUMER",
            f"consumer {consumer['id']}",
        )


def _validate_memory(root: Path, contract: dict[str, Any]) -> None:
    memory = contract["memory"]
    if (
        memory["canonicalDurableSharedPath"] != CANONICAL_MEMORY_PATH.as_posix()
        or memory["transientCheckpointPath"] != ".agent-work/checkpoint.json"
        or memory["executableLifecycleOwner"] != LOOP_LIFECYCLE_SPEC.as_posix()
    ):
        fail(
            "HARNESS-MEMORY",
            "canonical memory path or Spec 043 lifecycle ownership differs",
        )
    classes = memory["classes"]
    if tuple(item["id"] for item in classes) != MEMORY_CLASSES:
        fail(
            "HARNESS-MEMORY",
            "memory class order or membership differs",
        )
    for memory_class in classes:
        memory_id = memory_class["id"]
        if memory_class["authority"] != MEMORY_AUTHORITY[memory_id]:
            fail(
                "HARNESS-MEMORY-AUTHORITY",
                f"{memory_id} authority differs",
            )
        sensitivity = memory_class["sensitivity"]
        if (
            sensitivity["classification"] != "non-sensitive-redacted"
            or sensitivity["secretMaterialAllowed"] is not False
            or sensitivity["rawPromptOrTranscriptAllowed"] is not False
        ):
            fail(
                "HARNESS-MEMORY-SENSITIVITY",
                f"{memory_id} sensitivity differs",
            )
        if tuple(memory_class["prohibitedContent"]) != PROHIBITED_CONTENT:
            fail(
                "HARNESS-MEMORY-SENSITIVITY",
                f"{memory_id} prohibited content differs",
            )
        promotion = memory_class["promotion"]
        if (
            promotion["targetClass"] != MEMORY_PROMOTION[memory_id]
            or promotion["reviewRequired"] is not True
        ):
            fail(
                "HARNESS-MEMORY-PROMOTION",
                f"{memory_id} promotion boundary differs",
            )
        if LOOP_LIFECYCLE_SPEC.as_posix() not in memory_class[
            "lifecyclePolicyRefs"
        ]:
            fail(
                "HARNESS-MEMORY-LIFECYCLE",
                f"{memory_id} does not delegate executable lifecycle to Spec 043",
            )
        for policy_ref in memory_class["lifecyclePolicyRefs"]:
            _safe_repo_regular_file(
                root,
                PurePosixPath(policy_ref),
                "HARNESS-MEMORY-LIFECYCLE",
                f"{memory_id} lifecycle reference {policy_ref}",
            )
    _safe_repo_regular_file(
        root,
        CANONICAL_MEMORY_PATH,
        "HARNESS-MEMORY",
        "canonical durable shared memory",
    )
    _safe_repo_regular_file(
        root,
        LOOP_LIFECYCLE_SPEC,
        "HARNESS-MEMORY-LIFECYCLE",
        "Spec 043 executable lifecycle owner",
    )

    redaction = contract["redaction"]
    if (
        redaction["secretMaterialAllowed"] is not False
        or redaction["rawPromptOrTranscriptAllowed"] is not False
        or redaction["syntheticFixtureMarker"] != "[REDACTED-SYNTHETIC]"
        or tuple(redaction["prohibitedPayloadKinds"]) != PROHIBITED_CONTENT
    ):
        fail("HARNESS-MEMORY-SENSITIVITY", "redaction boundary differs")


def scan_sensitive_payload(value: Any, path: tuple[Any, ...] = ()) -> None:
    """Reject secret-shaped or conversational payloads, not policy labels."""

    if isinstance(value, dict):
        for key, item in value.items():
            scan_sensitive_payload(item, (*path, key))
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            scan_sensitive_payload(item, (*path, index))
        return
    if not isinstance(value, str):
        return
    if any(
        key in path for key in ("prohibitedContent", "prohibitedPayloadKinds")
    ):
        return
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(value):
            location = "/".join(str(part) for part in path) or "<root>"
            fail(
                "HARNESS-SENSITIVE",
                f"{location}: prohibited sensitive or conversational payload",
            )


def validate_contract(
    root: Path,
    raw_contract: dict[str, Any] | None = None,
    *,
    check_files: bool = True,
) -> dict[str, int]:
    """Validate schema, exact sets, memory, consumers, and current files."""

    contract = (
        copy.deepcopy(raw_contract)
        if raw_contract is not None
        else load_json(root, CONTRACT_PATH)
    )
    _precheck_contract(contract)
    _validate_schema(root, contract)
    scan_sensitive_payload(contract)
    _validate_evidence(contract)
    _validate_permissions(contract)
    _validate_roles(root, contract)
    _validate_surfaces(contract)
    _validate_inventory(
        contract["currentInventory"],
        name="currentInventory",
        roles=CURRENT_ROLES,
        surfaces=CURRENT_SURFACES,
        state="current",
    )
    _validate_inventory(
        contract["targetInventory"],
        name="targetInventory",
        roles=TARGET_ROLES,
        surfaces=TARGET_SURFACES,
        state="achieved",
        projection_state="current",
    )
    _validate_routing(root, contract)
    _validate_consumers(root, contract)
    _validate_memory(root, contract)
    if check_files:
        validate_projection_files(root, contract["currentInventory"]["projections"])
    return {
        "currentRoles": len(contract["currentInventory"]["roleIds"]),
        "currentSurfaces": len(contract["currentInventory"]["surfaceIds"]),
        "currentProjections": len(contract["currentInventory"]["projections"]),
        "targetRoles": len(contract["targetInventory"]["roleIds"]),
        "targetSurfaces": len(contract["targetInventory"]["surfaceIds"]),
        "targetProjections": len(contract["targetInventory"]["projections"]),
        "evidenceClasses": len(contract["evidenceClasses"]),
        "memoryClasses": len(contract["memory"]["classes"]),
        "consumers": len(contract["consumers"]),
    }


def _synthetic_sensitive_payload(name: str) -> str:
    synthetic_value = "synthetic" + "fixturevalue"
    payloads = {
        "bare-token-assignment": "to" + "ken: " + synthetic_value,
        "bare-secret-assignment": "se" + "cret: " + synthetic_value,
        "aws-secret-access-key": (
            "AWS_" + "SECRET_" + "ACCESS_" + "KEY=" + synthetic_value
        ),
        "slack-token-prefix": "xox" + "b-" + synthetic_value,
        "auth-file-payload": (
            "auth-file-" + "content: " + synthetic_value + " fixture"
        ),
        "auth-file-path-payload": (
            "auth-file-" + "path: /tmp/" + synthetic_value + "/auth.json"
        ),
        "shell-history-payload": (
            "shell-history-" + "payload: " + synthetic_value + " fixture"
        ),
        "observed-shell-history": (
            "Observed shell " + "history: cd /repo; synthetic fixture"
        ),
        "private-diagnostic-payload": (
            "private-diagnostic-" + "payload: " + synthetic_value + " fixture"
        ),
        "environment-dump-payload": (
            "environment-" + "dump: " + synthetic_value + " fixture"
        ),
        "user-configuration-payload": (
            "user-configuration-" + "dump: " + synthetic_value + " fixture"
        ),
        "raw-prompt-payload": (
            "Raw " + "prompt" + ": [REDACTED-SYNTHETIC]"
        ),
    }
    try:
        return payloads[name]
    except KeyError:
        fail("HARNESS-SELF-TEST", f"unknown sensitive mutation {name!r}")


def _apply_mutation(contract: dict[str, Any], name: str) -> None:
    if name == "unknown-top-level-key":
        contract["unexpected"] = True
    elif name == "unknown-nested-key":
        contract["memory"]["classes"][0]["unexpected"] = True
    elif name == "duplicate-role":
        contract["canonicalRoles"].append(
            copy.deepcopy(contract["canonicalRoles"][0])
        )
    elif name == "missing-role":
        contract["canonicalRoles"][2]["id"] = "unregistered-researcher"
    elif name == "unsupported-schema-version":
        contract["schemaVersion"] = 99
    elif name == "unsupported-contract-version":
        contract["contractVersion"] = "99.0.0"
    elif name == "stale-source-observation-cutoff":
        contract["sourceObservationCutoff"] = "2026-07-26 Asia/Seoul"
    elif name == "stale-eval-admission-state":
        contract["canonicalRoles"][0]["evalSuite"][
            "admissionState"
        ] = "pending-spec-044"
    elif name == "count-drift":
        contract["currentInventory"]["expectedProjectionCount"] = 29
    elif name == "current-projection-drift":
        contract["currentInventory"]["projections"][0][
            "path"
        ] = ".agents/agents/wrong-role.md"
    elif name == "target-projection-drift":
        contract["targetInventory"]["projections"][0][
            "path"
        ] = ".agents/agents/wrong-role.md"
    elif name == "duplicate-projection":
        contract["targetInventory"]["projections"][-1] = copy.deepcopy(
            contract["targetInventory"]["projections"][0]
        )
    elif name == "current-target-conflation":
        contract["targetInventory"]["state"] = "current"
    elif name == "invalid-permission":
        contract["canonicalRoles"][0]["permissionClass"] = "unbounded"
    elif name == "adapter-state-drift":
        contract["canonicalRoles"][0]["adapterSemantics"][
            "admissionState"
        ] = "target-only"
    elif name == "target-adapter-state-drift":
        contract["canonicalRoles"][-1]["adapterSemantics"][
            "admissionState"
        ] = "target-only"
    elif name == "unbounded-stop-rules":
        contract["canonicalRoles"][0]["stopConditions"] = [
            f"synthetic bounded fixture condition {index}"
            for index in range(7)
        ]
    elif name == "evidence-class-drift":
        contract["evidenceClasses"][0], contract["evidenceClasses"][1] = (
            contract["evidenceClasses"][1],
            contract["evidenceClasses"][0],
        )
    elif name == "consumer-version-drift":
        contract["consumers"][0]["selectedVersion"] = "2"
    elif name == "routing-ownership-drift":
        contract["routingContract"]["ownsPathRouting"] = True
    elif name == "memory-authority-drift":
        contract["memory"]["classes"][3]["authority"][
            "repositoryFacts"
        ] = True
    elif name == "memory-sensitivity-drift":
        contract["memory"]["classes"][0]["sensitivity"][
            "secretMaterialAllowed"
        ] = True
    elif name == "sensitive-payload":
        contract["canonicalRoles"][0]["purpose"] = (
            "Raw " + "transcript" + ": [REDACTED-SYNTHETIC]"
        )
    elif name in SENSITIVE_MUTATIONS:
        contract["canonicalRoles"][0]["purpose"] = (
            _synthetic_sensitive_payload(name)
        )
    elif name == "missing-required-field":
        del contract["redaction"]
    else:
        fail("HARNESS-SELF-TEST", f"unknown mutation {name!r}")


def _validate_fixture(fixture: Any) -> None:
    if not isinstance(fixture, dict):
        fail("HARNESS-FIXTURE", "fixture root must be an object")
    expected_keys = {"schemaVersion", "expected", "mutations", "expectedCaseCount"}
    if set(fixture) != expected_keys or fixture.get("schemaVersion") != 1:
        fail("HARNESS-FIXTURE", "fixture keys or schemaVersion differ")
    mutations = fixture.get("mutations")
    if not isinstance(mutations, list) or not all(
        isinstance(case, dict)
        and set(case) == {"name", "expectedRule"}
        and isinstance(case["name"], str)
        and isinstance(case["expectedRule"], str)
        for case in mutations
    ):
        fail("HARNESS-FIXTURE", "mutations must be closed name/rule objects")
    names = [case["name"] for case in mutations]
    if len(names) != len(set(names)):
        fail("HARNESS-FIXTURE", "mutation names must be unique")
    if fixture.get("expectedCaseCount") != len(mutations) + 1:
        fail(
            "HARNESS-FIXTURE",
            "expectedCaseCount must include mutations and duplicate-key case",
        )


def run_self_test(root: Path) -> tuple[list[str], int]:
    contract = load_json(root, CONTRACT_PATH)
    fixture = load_json(root, FIXTURE_PATH)
    _validate_fixture(fixture)
    failures: list[str] = []
    try:
        counts = validate_contract(root, contract, check_files=True)
    except HarnessError as exc:
        return [f"baseline: expected PASS, got {exc.code}: {exc.detail}"], 0
    if counts != fixture["expected"]:
        failures.append(
            f"baseline counts: expected {fixture['expected']!r}, got {counts!r}"
        )

    cases = 0
    for case in fixture["mutations"]:
        cases += 1
        mutated = copy.deepcopy(contract)
        _apply_mutation(mutated, case["name"])
        try:
            validate_contract(root, mutated, check_files=False)
        except HarnessError as exc:
            if exc.code != case["expectedRule"]:
                failures.append(
                    f"{case['name']}: expected {case['expectedRule']}, "
                    f"got {exc.code}: {exc.detail}"
                )
        else:
            failures.append(f"{case['name']}: mutation passed")

    cases += 1
    duplicate_text = (
        '{"schemaVersion":1,"contractVersion":"1.0.0",'
        '"schemaVersion":1}'
    )
    try:
        decode_json_text(duplicate_text, "<duplicate-key-fixture>")
    except HarnessError as exc:
        if exc.code != "HARNESS-DUPLICATE-KEY":
            failures.append(
                "duplicate-json-key: expected HARNESS-DUPLICATE-KEY, "
                f"got {exc.code}"
            )
    else:
        failures.append("duplicate-json-key: mutation passed")
    return failures, cases


def _resolve_root(value: Path) -> Path:
    try:
        mode = os.lstat(value).st_mode
    except OSError as exc:
        fail("HARNESS-INPUT", f"root {value}: {exc}", exit_code=2)
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        fail(
            "HARNESS-INPUT",
            f"root {value}: expected a directory that is not a symlink",
            exit_code=2,
        )
    try:
        return value.resolve(strict=True)
    except OSError as exc:
        fail("HARNESS-INPUT", f"root {value}: {exc}", exit_code=2)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Stage 00 provider-neutral harness contract."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = _resolve_root(args.root)
        if args.self_test:
            failures, cases = run_self_test(root)
            if failures:
                for failure in failures:
                    print(f"ERR HARNESS-SELF-TEST {failure}", file=sys.stderr)
                return 1
            print(
                "[PASS] agent harness contract self-test passed: "
                f"cases={cases} current=12/4/48 target=12/4/48 "
                "evidence=4 memory=4 consumers=14"
            )
            return 0
        counts = validate_contract(root)
        print(
            "[PASS] agent harness contract validation passed: "
            f"current={counts['currentRoles']}/"
            f"{counts['currentSurfaces']}/"
            f"{counts['currentProjections']} "
            f"target={counts['targetRoles']}/"
            f"{counts['targetSurfaces']}/"
            f"{counts['targetProjections']} "
            f"evidence={counts['evidenceClasses']} "
            f"memory={counts['memoryClasses']} "
            f"consumers={counts['consumers']}"
        )
        return 0
    except HarnessError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code
    except (KeyError, TypeError, ValueError) as exc:
        print(f"ERR HARNESS-INPUT {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
