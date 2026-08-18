#!/usr/bin/env python3
"""Validate closed, secret-free provider runtime/config evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import sys
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/provider-runtime-evidence.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/provider-runtime-evidence.schema.json"
)
FIXTURE_PATH = PurePosixPath(
    "tests/fixtures/agent-provider-runtime-evidence.json"
)
HARNESS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
ROUTING_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/validation-surfaces.json"
)
CLAUDE_SETTINGS_PATH = PurePosixPath(".claude/settings.json")
CAPABILITY_EVIDENCE_OWNER = CONTRACT_PATH.as_posix()
MAX_GOVERNED_INPUT_BYTES = 1024 * 1024

CUTOFF_UTC = datetime(2026, 7, 10, 1, 0, 0, tzinfo=timezone.utc)
CUTOFF_UTC_DATE = CUTOFF_UTC.date()
PROVIDER_IDS = ("local", "claude", "codex", "gemini")
SOURCE_PROVIDERS = ("claude", "codex", "gemini", "agency-agents")
SOURCE_IDS = (
    "claude-code-changelog-2-1-206",
    "claude-code-changelog-2-1-154",
    "claude-code-subagents-current",
    "codex-release-0-144-1",
    "codex-release-0-145-0-alpha-2",
    "codex-config-reference-current",
    "gemini-cli-release-0-50-0",
    "gemini-cli-release-0-51-preview-0",
    "gemini-cli-subagents-current",
    "agency-agents-pin-9f3e401c",
)
EVIDENCE_CLASSES = (
    "repo-static",
    "native-discovery",
    "authenticated-run",
)
VERDICTS = ("PASS", "FAIL", "BLOCKED", "ABSENT", "DEFER")
MCP_IDS = (
    "context7",
    "exa",
    "github",
    "memory",
    "playwright",
    "sequential-thinking",
    "supabase",
)
MODEL_GATE_IDS = ("configParse", "runtimeResolution", "spec044Fitness")
ROUTED_SURFACES = (
    "provider-gateways",
    "agent-shared",
    "agent-claude",
    "agent-codex",
    "agent-gemini",
    "governance-documents",
    "scripts",
    "tests",
)
HOOK_GRAPH_EXPECTATIONS = (
    (
        "local-compatibility-hook-graph",
        "local",
        ".agents/hooks.json",
        "unsupported",
        "ABSENT",
        (
            "03f1ce8362178ff638e6d54df9f6ed3532df262f5cd63767b0522ef4cda56cfe"  # pragma: allowlist secret
        ),
    ),
    (
        "codex-compatibility-hook-graph",
        "codex",
        ".codex/hooks.json",
        "unverified",
        "DEFER",
        (
            "666654f83dd15944e16828e30baa1c396f2884a50f001df38a47de476b096c9f"  # pragma: allowlist secret
        ),
    ),
)
FOCUSED_VALIDATORS = (
    (
        "python3",
        "scripts/validate-agent-provider-config.py",
        "--root",
        ".",
    ),
    (
        "python3",
        "scripts/validate-agent-provider-canaries.py",
        "--root",
        ".",
    ),
)
REQUIRED_PROHIBITED_CONTENT = {
    "api-keys",
    "tokens",
    "account-identifiers",
    "auth-cache-paths",
    "auth-cache-content",
    "private-endpoints",
    "prompt-transcripts",
    "provider-response-bodies",
    "secret-bearing-diagnostics",
    "environment-dumps",
    "shell-history",
    "user-configuration",
}
FORBIDDEN_KEY_NAMES = {
    "apikey",
    "token",
    "accesstoken",
    "refreshtoken",
    "secretvalue",
    "credentialvalue",
    "accountidentifier",
    "accountname",
    "authcachepath",
    "authfilepath",
    "prompttext",
    "prompttranscript",
    "providerresponse",
    "providerresponsebody",
    "environmentdump",
    "shellhistory",
    "privateendpoint",
}
FORBIDDEN_VALUE_FRAGMENTS = (
    "sk-",
    "bearer ",
    "ghp_",
    "aiza",
    "-----begin private key",
)
CLAUDE_ALLOWED_PERMISSIONS = (
    "Bash(git status --short)",
    "Bash(git diff --check)",
    "Bash(git diff --cached --check)",
    "Bash(git diff --name-only)",
    "Bash(git diff --cached --name-only)",
    "Bash(git rev-parse HEAD)",
    "Bash(git ls-files)",
)
CLAUDE_FORBIDDEN_ALLOW_PERMISSIONS = (
    "Bash(ls:*)",
    "Bash(grep:*)",
    "Bash(cat:*)",
    "Bash(git:*)",
    "Bash(kubectl get:*)",
    "Bash(kubectl describe:*)",
    "Bash(kubectl logs:*)",
)
CLAUDE_REQUIRED_DENY_PERMISSIONS = (
    "Read(./.env)",
    "Read(./.env.*)",
    "Read(./**/.env)",
    "Read(./**/.env.*)",
    "Bash(cat .env:*)",
    "Bash(cat .env.*:*)",
    "Bash(env:*)",
    "Bash(printenv:*)",
    "Bash(vault kv get:*)",
    "Bash(vault read:*)",
    "Bash(vault token lookup:*)",
    "Bash(kubectl get secret:*)",
    "Bash(kubectl get secrets:*)",
    "Bash(kubectl describe secret:*)",
    "Bash(kubectl describe secrets:*)",
    "Bash(git push:*)",
    "Bash(git merge:*)",
    "Bash(gh pr create:*)",
    "Bash(gh pr merge:*)",
    "Bash(gh release create:*)",
    "Bash(gh workflow run:*)",
    "Bash(kubectl delete:*)",
    "Bash(kubectl apply:*)",
    "Bash(kubectl create:*)",
    "Bash(kubectl replace:*)",
    "Bash(kubectl exec:*)",
    "Bash(kubectl patch:*)",
    "Bash(kubectl edit:*)",
    "Bash(kubectl label:*)",
    "Bash(kubectl annotate:*)",
    "Bash(kubectl set:*)",
    "Bash(kubectl scale:*)",
    "Bash(kubectl rollout restart:*)",
    "Bash(kubectl rollout undo:*)",
    "Bash(kubectl port-forward:*)",
    "Bash(kubectl drain:*)",
    "Bash(kubectl cordon:*)",
    "Bash(kubectl uncordon:*)",
    "Bash(kubectl taint:*)",
    "Bash(argocd app sync:*)",
    "Bash(argocd app set:*)",
    "Bash(argocd app patch:*)",
    "Bash(argocd app delete:*)",
    "Bash(argocd app create:*)",
    "Bash(argocd app unset:*)",
    "Bash(argocd app terminate-op:*)",
    "Bash(vault kv put:*)",
    "Bash(vault kv patch:*)",
    "Bash(vault write:*)",
    "Bash(git reset --hard:*)",
    "Bash(git checkout --:*)",
    "Bash(git restore:*)",
    "Bash(git clean:*)",
    "Bash(git rebase:*)",
    "Bash(git commit --amend:*)",
    "Bash(git branch -D:*)",
    "Bash(git push --force:*)",
    "Bash(git push -f:*)",
    "Bash(git push --delete:*)",
    "Bash(git push --mirror:*)",
    "Bash(rm -rf:*)",
    "Bash(k3d cluster delete:*)",
)


class ProviderConfigError(ValueError):
    """Typed provider-config contract failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def fail(code: str, detail: str, *, exit_code: int = 1) -> NoReturn:
    raise ProviderConfigError(code, detail, exit_code=exit_code)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            fail(
                "PNME-DUPLICATE-KEY",
                f"duplicate JSON key {key!r}",
                exit_code=2,
            )
        seen.add(key)
        result[key] = value
    return result


def decode_json_text(text: str, source: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=no_duplicate_pairs)
    except json.JSONDecodeError as exc:
        fail("PNME-JSON", f"{source}: {exc}", exit_code=2)


DIRECTORY_OPEN_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_DIRECTORY", 0)
    | getattr(os, "O_NOFOLLOW", 0)
)
REGULAR_FILE_OPEN_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_NOFOLLOW", 0)
    | getattr(os, "O_NONBLOCK", 0)
)


def _close_descriptor(descriptor: int) -> None:
    if descriptor < 0:
        return
    try:
        os.close(descriptor)
    except OSError:
        pass


def _same_identity(checked: os.stat_result, opened: os.stat_result) -> bool:
    return (checked.st_dev, checked.st_ino) == (
        opened.st_dev,
        opened.st_ino,
    )


def _open_repository_root(root: Path) -> tuple[Path, int]:
    raw_root = Path(root)
    if any(part == ".." for part in raw_root.parts):
        fail("PNME-INPUT", "repository root is invalid", exit_code=2)
    try:
        absolute_root = Path(os.path.abspath(os.fspath(raw_root)))
    except (OSError, TypeError, ValueError):
        fail("PNME-INPUT", "repository root is unavailable", exit_code=2)

    root_descriptor = -1
    next_descriptor = -1
    try:
        anchor = Path(absolute_root.anchor)
        try:
            checked = os.lstat(anchor)
        except OSError:
            fail("PNME-INPUT", "repository root is unavailable", exit_code=2)
        if stat.S_ISLNK(checked.st_mode) or not stat.S_ISDIR(checked.st_mode):
            fail(
                "PNME-INPUT",
                "repository root is not a real directory",
                exit_code=2,
            )
        try:
            root_descriptor = os.open(anchor, DIRECTORY_OPEN_FLAGS)
            opened = os.fstat(root_descriptor)
        except OSError:
            fail("PNME-INPUT", "repository root is unavailable", exit_code=2)
        if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
            checked,
            opened,
        ):
            fail(
                "PNME-INPUT",
                "repository root identity changed",
                exit_code=2,
            )

        for part in absolute_root.parts[1:]:
            try:
                checked = os.lstat(part, dir_fd=root_descriptor)
            except OSError:
                fail(
                    "PNME-INPUT",
                    "repository root is unavailable",
                    exit_code=2,
                )
            if stat.S_ISLNK(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "repository root path contains a symlink",
                    exit_code=2,
                )
            if not stat.S_ISDIR(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "repository root is not a real directory",
                    exit_code=2,
                )
            try:
                next_descriptor = os.open(
                    part,
                    DIRECTORY_OPEN_FLAGS,
                    dir_fd=root_descriptor,
                )
                opened = os.fstat(next_descriptor)
            except OSError:
                fail(
                    "PNME-INPUT",
                    "repository root is unavailable",
                    exit_code=2,
                )
            if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
                checked,
                opened,
            ):
                fail(
                    "PNME-INPUT",
                    "repository root identity changed",
                    exit_code=2,
                )
            _close_descriptor(root_descriptor)
            root_descriptor = next_descriptor
            next_descriptor = -1

        try:
            real_root = Path(os.path.realpath(absolute_root, strict=True))
        except (OSError, TypeError, ValueError):
            fail("PNME-INPUT", "repository root is unavailable", exit_code=2)
        if real_root != absolute_root:
            fail(
                "PNME-INPUT",
                "repository root path is not real",
                exit_code=2,
            )
        result_descriptor = root_descriptor
        root_descriptor = -1
        return absolute_root, result_descriptor
    finally:
        _close_descriptor(next_descriptor)
        _close_descriptor(root_descriptor)


def _resolve_repository_root(root: Path) -> Path:
    absolute_root, descriptor = _open_repository_root(root)
    _close_descriptor(descriptor)
    return absolute_root


def _canonical_relative_path(
    relative: PurePosixPath | str,
) -> PurePosixPath:
    raw = os.fspath(relative)
    path = PurePosixPath(raw)
    if (
        not raw
        or path.is_absolute()
        or raw != path.as_posix()
        or "\\" in raw
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        fail("PNME-INPUT", "governed input path is invalid", exit_code=2)
    return path


def _open_governed_node(
    root: Path,
    relative: PurePosixPath | str,
    *,
    expected_kind: str,
) -> int | None:
    if expected_kind not in {"file", "directory", "absent"}:
        fail("PNME-INPUT", "governed input kind is invalid", exit_code=2)
    canonical = _canonical_relative_path(relative)
    _, parent_descriptor = _open_repository_root(root)
    next_descriptor = -1
    final_descriptor = -1
    try:
        for index, part in enumerate(canonical.parts):
            final_component = index == len(canonical.parts) - 1
            try:
                checked = os.lstat(part, dir_fd=parent_descriptor)
            except FileNotFoundError:
                if expected_kind == "absent":
                    return None
                fail(
                    "PNME-INPUT",
                    "governed input is unavailable",
                    exit_code=2,
                )
            except OSError:
                fail(
                    "PNME-INPUT",
                    "governed input is unavailable",
                    exit_code=2,
                )

            if not final_component:
                if stat.S_ISLNK(checked.st_mode) or not stat.S_ISDIR(
                    checked.st_mode
                ):
                    fail(
                        "PNME-INPUT",
                        "governed input parent is not a real directory",
                        exit_code=2,
                    )
                try:
                    next_descriptor = os.open(
                        part,
                        DIRECTORY_OPEN_FLAGS,
                        dir_fd=parent_descriptor,
                    )
                    opened = os.fstat(next_descriptor)
                except FileNotFoundError:
                    if expected_kind == "absent":
                        return None
                    fail(
                        "PNME-INPUT",
                        "governed input is unavailable",
                        exit_code=2,
                    )
                except OSError:
                    fail(
                        "PNME-INPUT",
                        "governed input is unavailable",
                        exit_code=2,
                    )
                if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
                    checked,
                    opened,
                ):
                    fail(
                        "PNME-INPUT",
                        "governed input parent identity changed",
                        exit_code=2,
                    )
                _close_descriptor(parent_descriptor)
                parent_descriptor = next_descriptor
                next_descriptor = -1
                continue

            if expected_kind == "absent":
                fail(
                    "PNME-INPUT",
                    "declared-absent input has an existing final node",
                    exit_code=2,
                )
            if stat.S_ISLNK(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "governed input final node is a symlink",
                    exit_code=2,
                )
            if expected_kind == "file" and not stat.S_ISREG(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "governed input final node is not a regular file",
                    exit_code=2,
                )
            if expected_kind == "directory" and not stat.S_ISDIR(
                checked.st_mode
            ):
                fail(
                    "PNME-INPUT",
                    "governed input final node is not a real directory",
                    exit_code=2,
                )
            flags = (
                REGULAR_FILE_OPEN_FLAGS
                if expected_kind == "file"
                else DIRECTORY_OPEN_FLAGS
            )
            try:
                final_descriptor = os.open(
                    part,
                    flags,
                    dir_fd=parent_descriptor,
                )
                opened = os.fstat(final_descriptor)
            except OSError:
                fail(
                    "PNME-INPUT",
                    "governed input is unavailable",
                    exit_code=2,
                )
            expected_mode = (
                stat.S_ISREG(opened.st_mode)
                if expected_kind == "file"
                else stat.S_ISDIR(opened.st_mode)
            )
            if not expected_mode or not _same_identity(checked, opened):
                fail(
                    "PNME-INPUT",
                    "governed input final identity changed",
                    exit_code=2,
                )
            result_descriptor = final_descriptor
            final_descriptor = -1
            return result_descriptor
    finally:
        _close_descriptor(final_descriptor)
        _close_descriptor(next_descriptor)
        _close_descriptor(parent_descriptor)

    fail("PNME-INPUT", "governed input path is invalid", exit_code=2)


def _inspect_governed_node(
    root: Path,
    relative: PurePosixPath | str,
    *,
    expected_kind: str,
) -> None:
    descriptor = _open_governed_node(
        root,
        relative,
        expected_kind=expected_kind,
    )
    if descriptor is not None:
        _close_descriptor(descriptor)


def _read_regular_bytes(root: Path, relative: PurePosixPath | str) -> bytes:
    descriptor = _open_governed_node(root, relative, expected_kind="file")
    if descriptor is None:
        fail("PNME-INPUT", "governed input is unavailable", exit_code=2)
    try:
        before = os.fstat(descriptor)
        if before.st_size > MAX_GOVERNED_INPUT_BYTES:
            fail("PNME-INPUT", "governed input exceeds its byte limit", exit_code=2)
        chunks: list[bytes] = []
        total = 0
        while True:
            remaining = MAX_GOVERNED_INPUT_BYTES - total
            chunk = os.read(descriptor, min(65536, remaining + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_GOVERNED_INPUT_BYTES:
                fail(
                    "PNME-INPUT",
                    "governed input exceeds its byte limit",
                    exit_code=2,
                )
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (
            before.st_dev,
            before.st_ino,
            before.st_mode,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_mode,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ) or total != after.st_size:
            fail("PNME-INPUT", "governed input changed during read", exit_code=2)
        return b"".join(chunks)
    except ProviderConfigError:
        raise
    except OSError:
        fail(
            "PNME-INPUT",
            "governed input cannot be read",
            exit_code=2,
        )
    finally:
        _close_descriptor(descriptor)


def _read_regular_text(root: Path, relative: PurePosixPath | str) -> str:
    try:
        return _read_regular_bytes(root, relative).decode("utf-8")
    except UnicodeError:
        fail(
            "PNME-INPUT",
            "governed input cannot be read as UTF-8",
            exit_code=2,
        )


def load_json(root: Path, relative: PurePosixPath) -> Any:
    return decode_json_text(_read_regular_text(root, relative), str(relative))


def schema_errors(contract: Any, schema: Any) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: "
        f"{error.message}"
        for error in sorted(validator.iter_errors(contract), key=str)
    ]


def validate_schema(root: Path, contract: dict[str, Any]) -> None:
    schema = load_json(root, SCHEMA_PATH)
    errors = schema_errors(contract, schema)
    if errors:
        fail("PNME-SCHEMA", "; ".join(errors[:8]))


def _normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def validate_sensitive_content(value: Any, path: str = "<root>") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if _normalized_key(key) in FORBIDDEN_KEY_NAMES:
                fail(
                    "PNME-SENSITIVE-CONTENT",
                    f"forbidden durable key at {path}/{key}",
                )
            validate_sensitive_content(nested, f"{path}/{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            validate_sensitive_content(nested, f"{path}/{index}")
        return
    if isinstance(value, str):
        lowered = value.lower()
        for fragment in FORBIDDEN_VALUE_FRAGMENTS:
            if fragment in lowered:
                fail(
                    "PNME-SENSITIVE-CONTENT",
                    f"secret-like value at {path}",
                )


def validate_sources(contract: dict[str, Any]) -> None:
    ledger = contract["sourceLedger"]
    source_ids = [source["id"] for source in ledger]
    if len(source_ids) != len(set(source_ids)):
        fail("PNME-SOURCE-DUPLICATE", "source ledger IDs must be unique")
    if tuple(source_ids) != SOURCE_IDS:
        fail(
            "PNME-SOURCE-SET",
            f"expected fixed source ledger {SOURCE_IDS}, got {tuple(source_ids)}",
        )

    observed_providers = {source["provider"] for source in ledger}
    missing = set(SOURCE_PROVIDERS).difference(observed_providers)
    if missing:
        fail(
            "PNME-SOURCE-COVERAGE",
            f"missing official/comparison providers: {sorted(missing)}",
    )

    for source in ledger:
        try:
            source_date = date.fromisoformat(source["sourceDate"])
        except ValueError:
            fail(
                "PNME-SOURCE-CUTOFF",
                f"{source['id']} has invalid source date",
            )
        published_at_raw = source["publishedAtUtc"]
        published_at: datetime | None = None
        if published_at_raw is not None:
            try:
                published_at = datetime.strptime(
                    published_at_raw, "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)
            except ValueError:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} has invalid UTC publication timestamp",
                )
            if published_at.date() != source_date:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} publication timestamp/date disagree",
                )
        classification = source["cutoffApplicability"]
        confidence = source["confidence"]
        basis = source["dateBasis"]
        if classification == "cutoff-applicable":
            if published_at is not None and published_at > CUTOFF_UTC:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} is after cutoff but classified applicable",
                )
            if published_at is None and source_date >= CUTOFF_UTC_DATE:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} needs exact UTC time on the cutoff date",
                )
            if confidence != "dated-primary" or basis == "observed":
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} lacks dated release/commit confidence",
                )
        elif classification == "current-only":
            if confidence != "current-primary" or basis != "observed":
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} current-only confidence/date basis drifted",
                )
        elif classification == "post-cutoff":
            if published_at is not None and published_at <= CUTOFF_UTC:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} is not after the cutoff",
                )
            if published_at is None and source_date <= CUTOFF_UTC_DATE:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} needs exact UTC time on the cutoff date",
                )


def validate_claude_permissions(root: Path) -> None:
    settings = load_json(root, CLAUDE_SETTINGS_PATH)
    if not isinstance(settings, dict):
        fail("PNME-CLAUDE-PERMISSIONS", "Claude settings must be an object")
    permissions = settings.get("permissions")
    if not isinstance(permissions, dict):
        fail(
            "PNME-CLAUDE-PERMISSIONS",
            "Claude permissions must be an object",
        )

    permission_lists: dict[str, list[str]] = {}
    for key in ("allow", "deny"):
        values = permissions.get(key)
        if (
            not isinstance(values, list)
            or not all(isinstance(value, str) and value for value in values)
            or len(values) != len(set(values))
        ):
            fail(
                "PNME-CLAUDE-PERMISSIONS",
                f"Claude permissions.{key} must be a unique non-empty string list",
            )
        permission_lists[key] = values

    allow = permission_lists["allow"]
    if any(character in permission for permission in allow for character in "*?[]"):
        fail(
            "PNME-CLAUDE-PERMISSIONS",
            "Claude allow permissions must not contain wildcard syntax",
        )
    if tuple(allow) != CLAUDE_ALLOWED_PERMISSIONS:
        fail(
            "PNME-CLAUDE-PERMISSIONS",
            "Claude allow permissions must match the narrow repository-static set",
        )
    if set(allow).intersection(CLAUDE_FORBIDDEN_ALLOW_PERMISSIONS):
        fail(
            "PNME-CLAUDE-PERMISSIONS",
            "Claude allow permissions include a broad command family",
        )

    deny = permission_lists["deny"]
    if tuple(deny) != CLAUDE_REQUIRED_DENY_PERMISSIONS:
        fail(
            "PNME-CLAUDE-PERMISSIONS",
            "Claude deny permissions must match the complete required set",
        )


def provider_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    observed = [provider["id"] for provider in contract["providers"]]
    if observed != list(PROVIDER_IDS):
        fail(
            "PNME-PROVIDER-ORDER",
            f"expected {PROVIDER_IDS}, got {observed}",
        )
    return {
        provider["id"]: provider
        for provider in contract["providers"]
    }


def validate_repo_path(raw_path: str, field: str) -> PurePosixPath:
    path = PurePosixPath(raw_path)
    if (
        path.is_absolute()
        or raw_path != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
        or "\\" in raw_path
    ):
        fail("PNME-PATH", f"{field} must be a canonical repo-relative path")
    return path


def validate_observations(providers: dict[str, dict[str, Any]], contract: dict[str, Any]) -> None:
    expected_current = {
        "claude": ("present", "2.1.220 (Claude Code)"),
        "codex": ("present", "codex-cli 0.140.0"),
        "gemini": ("absent", None),
    }
    for provider_id, (installation, version) in expected_current.items():
        observation = providers[provider_id]["localObservation"]
        if (
            observation["installation"],
            observation["version"],
            observation["observedAt"],
            observation["userReported"],
            observation["readinessClaim"],
        ) != (installation, version, "2026-07-28", False, False):
            fail(
                "PNME-LOCAL-OBSERVATION",
                f"{provider_id} current local observation drifted",
            )

    prior = contract["observationHistory"]
    matching = [
        item
        for item in prior
        if item["observationClass"] == "prior-user-report"
        and item["providers"]["codex"]["version"]
        == "codex-cli 0.145.0-alpha.27"
        and item["providers"]["claude"]["installation"] == "absent"
        and item["providers"]["gemini"]["installation"] == "absent"
        and item["readinessClaim"] is False
    ]
    if len(matching) != 1:
        fail(
            "PNME-LOCAL-OBSERVATION",
            "prior user-reported Codex alpha/Claude absent state must be preserved once",
        )


def validate_surface_parity(
    root: Path,
    providers: dict[str, dict[str, Any]],
    *,
    check_paths: bool,
) -> dict[str, Any]:
    harness = load_json(root, HARNESS_PATH)
    harness_surfaces = {
        surface["id"]: surface
        for surface in harness["surfaces"]
    }
    if tuple(harness_surfaces) != PROVIDER_IDS:
        fail(
            "PNME-HARNESS-PARITY",
            f"harness surfaces drifted: {tuple(harness_surfaces)}",
        )

    for provider_id in PROVIDER_IDS:
        provider = providers[provider_id]
        surface = provider["trackedSurface"]
        surface_path_root = validate_repo_path(
            surface["pathRoot"], f"{provider_id}.trackedSurface.pathRoot"
        )
        harness_surface = harness_surfaces[provider_id]
        expected = (
            harness_surface["pathRoot"],
            harness_surface["admissionState"],
            harness_surface["evidenceClass"],
        )
        actual = (
            surface["pathRoot"],
            surface["state"],
            surface["evidenceClass"],
        )
        if actual != expected:
            fail(
                "PNME-SURFACE-PARITY",
                f"{provider_id} expected {expected}, got {actual}",
            )
        if surface["state"] == "current" and surface["presence"] != "present":
            fail(
                "PNME-SURFACE-PARITY",
                f"{provider_id} current surface must be declared present",
            )

        project_paths = [
            (
                item,
                validate_repo_path(
                    item["path"], f"{provider_id}.projectPaths.path"
                ),
            )
            for item in provider["projectPaths"]
        ]
        if len({path for _, path in project_paths}) != len(project_paths):
            fail(
                "PNME-PATH",
                f"{provider_id}.projectPaths contains duplicate paths",
            )

        if check_paths:
            _inspect_governed_node(
                root,
                surface_path_root,
                expected_kind=(
                    "directory"
                    if surface["presence"] == "present"
                    else "absent"
                ),
            )

            for item, relative_item_path in project_paths:
                expected_kind = "absent"
                if item["state"] == "current":
                    expected_kind = (
                        "directory"
                        if item["kind"] == "role-directory"
                        else "file"
                    )
                _inspect_governed_node(
                    root,
                    relative_item_path,
                    expected_kind=expected_kind,
                )

    if providers["local"]["trackedSurface"]["pathRoot"] != ".agents/agents":
        fail(
            "PNME-SURFACE-PARITY",
            ".agents must remain the local projection",
        )
    if providers["gemini"]["trackedSurface"]["pathRoot"] != ".gemini/agents":
        fail(
            "PNME-SURFACE-PARITY",
            "Gemini native projection must remain under .gemini",
        )
    if (
        check_paths
        and providers["gemini"]["trackedSurface"]["state"] != "current"
    ):
        _inspect_governed_node(
            root,
            PurePosixPath(".gemini"),
            expected_kind="absent",
        )
    return harness


def validate_evidence_lanes(providers: dict[str, dict[str, Any]]) -> None:
    runtime_keys = {
        "repo-static": "repoStatic",
        "native-discovery": "nativeDiscovery",
        "authenticated-run": "authenticatedRun",
    }
    for provider_id, provider in providers.items():
        lanes = provider["evidenceLanes"]
        observed = [lane["id"] for lane in lanes]
        if observed != list(EVIDENCE_CLASSES):
            fail(
                "PNME-EVIDENCE-LANE",
                f"{provider_id} lane order/coverage drifted: {observed}",
            )
        for lane in lanes:
            if lane["verdict"] not in VERDICTS:
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} has invalid verdict",
                )
            if lane["crossLanePromotion"] is not False:
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} permits cross-lane promotion",
                )
            if (
                provider["runtimeVerdicts"][runtime_keys[lane["id"]]]
                != lane["verdict"]
            ):
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} compatibility verdict drifted",
                )
            if lane["verdict"] != "PASS" and (
                not lane["owner"]
                or not lane["limitation"]
                or not lane["retryTrigger"]
            ):
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} limitation is not actionable",
                )

        by_id = {lane["id"]: lane["verdict"] for lane in lanes}
        if provider["localObservation"]["installation"] != "present" and (
            by_id["native-discovery"] == "PASS"
            or by_id["authenticated-run"] == "PASS"
        ):
            fail(
                "PNME-UNSUPPORTED-RUNTIME",
                f"{provider_id} cannot claim runtime PASS without an installed runtime",
            )
        if (
            by_id["authenticated-run"] == "PASS"
            and by_id["native-discovery"] != "PASS"
        ):
            fail(
                "PNME-EVIDENCE-LANE",
                f"{provider_id} authenticated PASS lacks discovery PASS",
            )
        if (
            by_id["native-discovery"] == "PASS"
            and by_id["repo-static"] != "PASS"
        ):
            fail(
                "PNME-EVIDENCE-LANE",
                f"{provider_id} discovery PASS lacks repo-static PASS",
            )


def validate_hook_graphs(
    root: Path,
    contract: dict[str, Any],
    providers: dict[str, dict[str, Any]],
    *,
    check_paths: bool,
) -> None:
    if contract["capabilityEvidenceOwner"] != CAPABILITY_EVIDENCE_OWNER:
        fail(
            "PNME-HOOK-BOUNDARY",
            "provider capability evidence must have one Stage 00 machine owner",
        )

    records = contract["hookGraphs"]
    observed = tuple(
        (
            record["id"],
            record["providerId"],
            record["path"],
            record["runtimeSupport"],
            record["deliveryVerdict"],
            record["contentSha256"],
        )
        for record in records
    )
    if observed != HOOK_GRAPH_EXPECTATIONS:
        fail(
            "PNME-HOOK-BOUNDARY",
            f"retained hook graph inventory drifted: {observed}",
        )
    if len({record["path"] for record in records}) != len(records):
        fail("PNME-HOOK-BOUNDARY", "hook graph paths must be unique")

    for record in records:
        key = f"{record['providerId']}/{record['path']}"
        path = validate_repo_path(record["path"], f"{key}.path")
        if (
            record["classification"] != "custom-compatibility-bridge"
            or record["evidenceClass"] != "repo-static"
        ):
            fail(
                "PNME-HOOK-BOUNDARY",
                f"{key} is not a repo-static custom compatibility bridge",
            )
        if record["runtimeSupport"] != "supported" and (
            record["deliveryVerdict"] == "PASS"
        ):
            fail(
                "PNME-HOOK-BOUNDARY",
                f"{key} claims delivery PASS for an unsupported or unverified runtime",
            )
        native_verdict = {
            lane["id"]: lane["verdict"]
            for lane in providers[record["providerId"]]["evidenceLanes"]
        }["native-discovery"]
        if record["deliveryVerdict"] == "PASS" and native_verdict != "PASS":
            fail(
                "PNME-HOOK-BOUNDARY",
                f"{key} claims delivery PASS without native discovery PASS",
            )
        if not all(
            record[field]
            for field in (
                "owner",
                "limitation",
                "retryTrigger",
                "claimBoundary",
                "embeddedDeclaration",
            )
        ):
            fail(
                "PNME-HOOK-BOUNDARY",
                f"{key} lacks an actionable compatibility boundary",
            )

        project_paths = {
            (item["path"], item["kind"], item["state"])
            for item in providers[record["providerId"]]["projectPaths"]
        }
        if (
            record["path"],
            "compatibility-hook-graph",
            "current",
        ) not in project_paths:
            fail(
                "PNME-HOOK-BOUNDARY",
                f"{key} is not declared as a current compatibility hook graph",
            )

        if check_paths:
            graph_bytes = _read_regular_bytes(root, path)
            if hashlib.sha256(graph_bytes).hexdigest() != record["contentSha256"]:
                fail(
                    "PNME-HOOK-BOUNDARY",
                    f"{key} bytes differ from the reviewed hook graph",
                )
            try:
                graph_text = graph_bytes.decode("utf-8")
            except UnicodeError:
                fail("PNME-HOOK-BOUNDARY", f"{key} is not UTF-8")
            graph = decode_json_text(graph_text, str(path))
            if not isinstance(graph, dict) or not isinstance(
                graph.get("hooks"), dict
            ):
                fail(
                    "PNME-HOOK-BOUNDARY",
                    f"{key} does not contain a closed hook graph",
                )
            if graph.get("description") != record["embeddedDeclaration"]:
                fail(
                    "PNME-HOOK-BOUNDARY",
                    f"{key} does not embed its repo-static delivery boundary",
                )


def validate_models(contract: dict[str, Any], providers: dict[str, dict[str, Any]]) -> None:
    source_ids = {source["id"] for source in contract["sourceLedger"]}
    for provider_id, provider in providers.items():
        candidates = provider["modelCandidates"]
        if [item["roleClass"] for item in candidates] != [
            "planning-supervisor",
            "worker-subagent",
        ]:
            fail(
                "PNME-MODEL-GATE",
                f"{provider_id} role-class candidate coverage drifted",
            )
        for candidate in candidates:
            missing_sources = set(candidate["sourceIds"]).difference(source_ids)
            if missing_sources:
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} references unknown sources {sorted(missing_sources)}",
                )
            if candidate["promotionState"] != "candidate-only":
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} candidate was promoted",
                )
            if candidate["fallback"]["silentFallbackAllowed"]:
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} candidate permits silent fallback",
                )
            if set(candidate["gates"]) != set(MODEL_GATE_IDS):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} model gates are incomplete",
                )
            if candidate["idResolution"] == "configured-only" and (
                candidate["configuredId"] is None
                or candidate["observedId"] is not None
            ):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} configured-only ID boundary drifted",
                )
            if candidate["idResolution"] == "unresolved" and (
                candidate["observedId"] is not None
            ):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} unresolved candidate has observed ID",
                )
            if candidate["idResolution"] == "resolved" and (
                candidate["configuredId"] is None
                or candidate["observedId"] is None
                or candidate["gates"]["runtimeResolution"] != "PASS"
            ):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} resolved candidate lacks exact runtime evidence",
                )
            if candidate["fallback"]["observedId"] is not None:
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} candidate records unapproved fallback",
                )


def validate_mcp_inventory(
    contract: dict[str, Any],
    harness: dict[str, Any],
) -> None:
    inventory = contract["mcpInventory"]
    ids = [server["id"] for server in inventory]
    if tuple(ids) != MCP_IDS or len(ids) != len(set(ids)):
        fail(
            "PNME-MCP-BOUNDARY",
            f"expected MCP inventory {MCP_IDS}, got {ids}",
        )
    allowed_roles = set(harness["targetInventory"]["roleIds"])
    for server in inventory:
        unknown = set(server["allowedRoles"]).difference(allowed_roles)
        if unknown:
            fail(
                "PNME-MCP-BOUNDARY",
                f"{server['id']} allows unknown roles {sorted(unknown)}",
            )
        if server["credentialClass"] not in {
            "none",
            "environment-reference",
            "provider-managed-auth",
        }:
            fail(
                "PNME-MCP-BOUNDARY",
                f"{server['id']} credential class is not declarative",
            )
        if server["runtimeState"] == "PASS":
            fail(
                "PNME-MCP-BOUNDARY",
                f"{server['id']} cannot claim runtime PASS without a canary",
            )


def validate_canary_policy(contract: dict[str, Any]) -> None:
    policy = contract["canaryRecordContract"]
    if tuple(policy["allowedVerdicts"]) != VERDICTS:
        fail("PNME-CANARY-POLICY", "allowed verdicts drifted")
    if tuple(policy["requiredEvidenceClasses"]) != EVIDENCE_CLASSES:
        fail("PNME-CANARY-POLICY", "required evidence classes drifted")
    if (
        policy["redactionRequired"] is not True
        or policy["syntheticTaskRequired"] is not True
        or policy["mutationMode"] != "no-mutation"
        or policy["crossLanePromotionAllowed"] is not False
    ):
        fail("PNME-CANARY-POLICY", "safe canary policy drifted")
    missing = REQUIRED_PROHIBITED_CONTENT.difference(
        policy["prohibitedDurableContent"]
    )
    if missing:
        fail(
            "PNME-CANARY-POLICY",
            f"missing prohibited content classes {sorted(missing)}",
        )


def validate_routing(root: Path, contract: dict[str, Any]) -> None:
    route = contract["routeIntegration"]
    if tuple(tuple(argv) for argv in route["focusedValidators"]) != FOCUSED_VALIDATORS:
        fail("PNME-ROUTING", "focused validator commands drifted")
    if tuple(route["surfaces"]) != ROUTED_SURFACES:
        fail("PNME-ROUTING", "provider evidence surfaces drifted")
    if not {"infrastructure", "gitops", "vault", "remote-live"}.issubset(
        route["excludedSurfaces"]
    ):
        fail("PNME-ROUTING", "protected/live exclusions are incomplete")

    routing = load_json(root, ROUTING_PATH)
    registrations = [
        item
        for item in routing["validators"]
        if item["id"] == route["validatorId"]
    ]
    if len(registrations) != 1:
        fail("PNME-ROUTING", "agent-provider-evidence route must be unique")
    if registrations[0]["argv"] != route["argv"]:
        fail("PNME-ROUTING", "registered provider evidence argv drifted")
    routed = tuple(
        surface["id"]
        for surface in routing["surfaces"]
        if route["validatorId"] in surface["validators"]
    )
    if routed != ROUTED_SURFACES:
        fail("PNME-ROUTING", f"registered surfaces drifted: {routed}")


def validate_contract(
    root: Path,
    contract: dict[str, Any] | None = None,
    *,
    check_paths: bool = True,
) -> dict[str, int]:
    root = _resolve_repository_root(root)
    if contract is None:
        contract = load_json(root, CONTRACT_PATH)
    validate_schema(root, contract)
    validate_sensitive_content(contract)
    validate_sources(contract)
    providers = provider_map(contract)
    validate_observations(providers, contract)
    harness = validate_surface_parity(
        root,
        providers,
        check_paths=check_paths,
    )
    if check_paths:
        validate_claude_permissions(root)
    validate_evidence_lanes(providers)
    validate_hook_graphs(
        root,
        contract,
        providers,
        check_paths=check_paths,
    )
    validate_models(contract, providers)
    validate_mcp_inventory(contract, harness)
    validate_canary_policy(contract)
    if check_paths:
        validate_routing(root, contract)
    return {
        "providers": len(providers),
        "sources": len(contract["sourceLedger"]),
        "modelCandidates": sum(
            len(provider["modelCandidates"])
            for provider in providers.values()
        ),
        "mcpServers": len(contract["mcpInventory"]),
        "hookGraphs": len(contract["hookGraphs"]),
    }


def apply_mutation(contract: dict[str, Any], name: str) -> None:
    if name == "unknown-top-level-key":
        contract["unexpected"] = True
    elif name == "cutoff-source-after-cutoff":
        contract["sourceLedger"][0]["sourceDate"] = "2026-07-11"
    elif name == "cutoff-source-same-day-after-cutoff":
        contract["sourceLedger"][0]["sourceDate"] = "2026-07-10"
        contract["sourceLedger"][0][
            "publishedAtUtc"
        ] = "2026-07-10T01:00:01Z"
    elif name == "source-id-substitution":
        contract["sourceLedger"][0]["id"] = "replacement-source-id"
    elif name == "extra-source-new-id":
        extra = copy.deepcopy(contract["sourceLedger"][0])
        extra["id"] = "extra-source-new-id"
        contract["sourceLedger"].append(extra)
    elif name == "absolute-project-path":
        contract["providers"][1]["projectPaths"][0]["path"] = "/etc/passwd"
    elif name == "invalid-calendar-source-date":
        contract["sourceLedger"][0]["sourceDate"] = "2026-02-30"
    elif name == "gemini-current-while-absent":
        contract["providers"][3]["trackedSurface"]["presence"] = "absent"
    elif name == "agents-relabeled-as-gemini":
        contract["providers"][0]["trackedSurface"]["pathRoot"] = ".gemini/agents"
    elif name == "model-silent-fallback-enabled":
        contract["providers"][2]["modelCandidates"][0]["fallback"][
            "silentFallbackAllowed"
        ] = True
    elif name == "model-fitness-promoted-without-gates":
        contract["providers"][2]["modelCandidates"][0][
            "promotionState"
        ] = "current-assignment"
    elif name == "mcp-role-outside-harness":
        contract["mcpInventory"][0]["allowedRoles"].append("unowned-agent")
    elif name == "secret-like-contract-value":
        contract["sourceLedger"][0]["claim"] = "sk-test-not-a-real-secret"
    elif name == "hook-graph-unclassified":
        contract["hookGraphs"][0]["classification"] = "unclassified"
    elif name == "hook-graph-runtime-pass":
        contract["hookGraphs"][0]["deliveryVerdict"] = "PASS"
    elif name == "hook-graph-digest-drift":
        contract["hookGraphs"][0]["contentSha256"] = "0" * 64
    elif name == "absent-runtime-native-pass":
        contract["providers"][3]["evidenceLanes"][1]["verdict"] = "PASS"
        contract["providers"][3]["runtimeVerdicts"][
            "nativeDiscovery"
        ] = "PASS"
    else:
        fail("PNME-FIXTURE", f"unknown config mutation {name}")


def validate_fixture(root: Path) -> int:
    contract = load_json(root, CONTRACT_PATH)
    fixture = load_json(root, FIXTURE_PATH)
    cases = fixture["configMutations"]
    for case in cases:
        mutated = copy.deepcopy(contract)
        apply_mutation(mutated, case["name"])
        try:
            validate_contract(root, mutated, check_paths=True)
        except ProviderConfigError as exc:
            if exc.code != case["expectedRule"]:
                fail(
                    "PNME-FIXTURE",
                    f"{case['name']} expected {case['expectedRule']} got {exc.code}",
                )
        else:
            fail("PNME-FIXTURE", f"{case['name']} unexpectedly passed")
    return len(cases)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate provider runtime/config evidence."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root)
    try:
        cases = validate_fixture(root) if args.self_test else 0
        counts = validate_contract(root)
        if args.self_test:
            print(
                "[PASS] agent provider config self-test passed: "
                f"cases={cases} providers={counts['providers']} "
                f"sources={counts['sources']} "
                f"models={counts['modelCandidates']} "
                f"mcp={counts['mcpServers']} "
                f"hooks={counts['hookGraphs']}"
            )
        else:
            print(
                "[PASS] agent provider config validation passed: "
                f"providers={counts['providers']} "
                f"sources={counts['sources']} "
                f"models={counts['modelCandidates']} "
                f"mcp={counts['mcpServers']} "
                f"hooks={counts['hookGraphs']}"
            )
        return 0
    except ProviderConfigError as exc:
        print(f"{exc.code}: {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
