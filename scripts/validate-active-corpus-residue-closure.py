#!/usr/bin/env python3
"""Validate the ACER-006 terminal residue, cardinality, and lifecycle closure."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Any


SCHEMA = "active-corpus-residue-closure.v1"
FIXED_INPUT_COMMIT = (
    "09682e9e8feaeed028bd06ef6d1733617c82029e"  # pragma: allowlist secret
)
LEDGER_PATH = "docs/90.references/data/active-corpus-residue-closure.json"
SCRIPT_PATH = "scripts/validate-active-corpus-residue-closure.py"
AGGREGATE_PATH = "scripts/validate-repo-quality-gates.sh"
REGISTRY_PATH = "docs/99.templates/support/document-profiles.json"
OWNER_SPEC = "docs/03.specs/037-active-corpus-and-execution-retention/spec.md"
EXECUTION_PLAN = (
    "docs/04.execution/plans/2026-07-18-active-corpus-and-execution-retention.md"
)
EXECUTION_TASK = (
    "docs/04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md"
)
TERMINAL_LINEAGE = "2026-07-22-reference-information-architecture"
TERMINAL_SPEC = "docs/03.specs/038-reference-information-architecture/spec.md"
TERMINAL_PLAN = f"docs/04.execution/plans/{TERMINAL_LINEAGE}.md"
TERMINAL_TASK = f"docs/04.execution/tasks/{TERMINAL_LINEAGE}.md"
TERMINAL_SUCCESSOR_SPEC = "docs/03.specs/039-github-ci-qa-evidence/spec.md"
TERMINAL_SUCCESSOR_LINEAGE = "2026-07-26-github-ci-qa-evidence"
TERMINAL_SUCCESSOR_PLAN = (
    f"docs/04.execution/plans/{TERMINAL_SUCCESSOR_LINEAGE}.md"
)
TERMINAL_SUCCESSOR_TASK = (
    f"docs/04.execution/tasks/{TERMINAL_SUCCESSOR_LINEAGE}.md"
)
TERMINAL_FRONTIER_SPEC = (
    "docs/03.specs/040-contract-cutover-and-program-closure/spec.md"
)
TERMINAL_FRONTIER_LINEAGE = "2026-07-27-contract-cutover-and-program-closure"
TERMINAL_FRONTIER_PLAN = f"docs/04.execution/plans/{TERMINAL_FRONTIER_LINEAGE}.md"
TERMINAL_FRONTIER_TASK = f"docs/04.execution/tasks/{TERMINAL_FRONTIER_LINEAGE}.md"
TERMINAL_PROGRAM_CLOSURE_ADR = (
    "docs/02.architecture/decisions/"
    "0020-document-lifecycle-program-closure-evidence.md"
)
PLAN_ROOT = "docs/04.execution/plans"
TASK_ROOT = "docs/04.execution/tasks"
ADR_ROOT = "docs/02.architecture/decisions"
SPEC_ROOT = "docs/03.specs"
ARCHIVE_PLAN_ROOT = "docs/98.archive/04.execution/plans"
ARCHIVE_TASK_ROOT = "docs/98.archive/04.execution/tasks"
SOURCE_PATHS = (
    "docs/90.references/data/active-corpus-retention-census.json",
    "docs/90.references/data/active-corpus-eligibility-ledger.json",
    "docs/90.references/data/active-corpus-migration-results.json",
    "docs/90.references/data/active-corpus-role-audit.json",
)
CONTROL_PATHS = (LEDGER_PATH, SCRIPT_PATH, AGGREGATE_PATH)
SOURCE_SCHEMAS = {
    SOURCE_PATHS[0]: "active-corpus-retention-census.v1",
    SOURCE_PATHS[1]: "active-corpus-eligibility-ledger.v1",
    SOURCE_PATHS[2]: "active-corpus-migration-results.v1",
    SOURCE_PATHS[3]: "active-corpus-role-audit.v1",
}
INVENTORY_ROOTS = (
    PLAN_ROOT,
    TASK_ROOT,
    ADR_ROOT,
    SPEC_ROOT,
    ARCHIVE_PLAN_ROOT,
    ARCHIVE_TASK_ROOT,
)
MANDATORY_OWNER_PATHS = {
    SPEC_ROOT: frozenset(
        {
            OWNER_SPEC,
            TERMINAL_SPEC,
            TERMINAL_SUCCESSOR_SPEC,
            TERMINAL_FRONTIER_SPEC,
        }
    ),
    PLAN_ROOT: frozenset(
        {
            EXECUTION_PLAN,
            TERMINAL_PLAN,
            TERMINAL_SUCCESSOR_PLAN,
            TERMINAL_FRONTIER_PLAN,
        }
    ),
    TASK_ROOT: frozenset(
        {
            EXECUTION_TASK,
            TERMINAL_TASK,
            TERMINAL_SUCCESSOR_TASK,
            TERMINAL_FRONTIER_TASK,
        }
    ),
}

DEFER_AUTHORITY = "current-execution-record-pending-exact-eligibility-evidence"
DEFER_CLOSURE_REASON = "migration-blocked-by-explicit-missing-evidence"
DEFER_TRIGGER = "exact-upstream-evidence-change"
TERMINAL_CONTROL_REASON = (
    "terminal-spec-037-lineage-awaiting-successor-migration-evidence"
)
TERMINAL_CONTROL_EVIDENCE_ROLE = "terminal-stage-04-closure-evidence"
TERMINAL_CONTROL_REFRESH_TRIGGER = "exact-successor-migration-evidence-change"
ADR_AUTHORITY = "accepted-decision-record"
SPEC_AUTHORITY = "current-done-specification"
AUTHORITY_REASON = "terminal-status-alone-is-not-an-archive-predicate"
FINDING_KEYS = (
    "duplicateCurrentOwner",
    "unexplainedResidue",
    "activeEligible",
    "staleEligible",
    "missingClosureField",
    "movedAdrOrSpec",
    "currentLinkError",
    "historicalLinkError",
)

EXPECTED_COUNTS = {
    "candidateInput": 110,
    "historicalEligible": 12,
    "historicalDefer": 98,
    "migratedClosed": 12,
    "currentStage04": 100,
    "currentPlans": 49,
    "currentTasks": 51,
    "currentDefer": 100,
    "currentRetain": 0,
    "activeEligible": 0,
    "pairKeys": 52,
    "completePairs": 48,
    "planOnly": 1,
    "taskOnly": 3,
    "duplicateSameKind": 0,
    "partialOwnedDefer": 4,
    "acceptedAdrs": 13,
    "doneSpecs": 29,
    "migratedAdrOrSpec": 0,
    "stage05Authored": 24,
    "helperTests": 33,
    "findings": 0,
}

GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 10
MAX_FILE_BYTES = 2_000_000
SAFE_PATH = re.compile(r"[A-Za-z0-9._@+/-]+\Z")
ACTIVE_CONTROL_LINEAGE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._@+-]*\Z")
TERMINAL_RELATION_IDENTITY = {
    "spec": "038",
    "order": 5,
    "reason": "Reference information architecture",
    "decision": "0017",
}
TERMINAL_SUCCESSOR_IDENTITY = {
    "spec": "039",
    "order": 6,
    "reason": "GitHub CI and QA evidence",
    "decision": "0017",
}
TERMINAL_FRONTIER_IDENTITY = {
    "spec": "040",
    "order": 7,
    "reason": "Contract cutover and program closure",
    "decision": "0017",
}
FULL_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
MODE_RECORD = re.compile(
    rb"(?P<mode>[0-9]{6}) (?P<oid>[0-9a-f]{40}|[0-9a-f]{64}) "
    rb"(?P<stage>[0-3])\t(?P<path>[^\0]+)\Z"
)
FRONTMATTER_LINE = re.compile(
    r"(?P<key>[A-Za-z][A-Za-z0-9_-]*):[ \t]*(?P<value>[^\r\n]*)\Z"
)
CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_COUNT": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_KEY_0": "core.fsmonitor",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_CONFIG_VALUE_0": "false",
    "GIT_LITERAL_PATHSPECS": "1",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_PAGER": "cat",
    "GIT_TERMINAL_PROMPT": "0",
    "HOME": "/nonexistent",
    "LANG": "C",
    "LC_ALL": "C",
    "PAGER": "cat",
    "PATH": "/usr/bin:/bin",
}


def is_safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not SAFE_PATH.fullmatch(value):
        return False
    parts = value.split("/")
    return (
        not value.startswith("/")
        and all(part not in {"", ".", ".."} for part in parts)
        and parts[0] != "_workspace"
    )


def diagnostic_path(value: Any) -> str:
    if isinstance(value, str) and value in {".", ".git"}:
        return value
    return value if is_safe_path(value) else LEDGER_PATH


def _git_identity(oid: str) -> str:
    if FULL_OID.fullmatch(oid) is None:
        raise ClosureError("CLOSURE-BLOB-ID")
    algorithm = "sha1" if len(oid) == 40 else "sha256"
    return f"git:{algorithm}:{oid}"


def _sha256_identity(digest: Any) -> str:
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise ClosureError("CLOSURE-DIGEST")
    return f"digest:sha256:{digest}"


class ClosureError(ValueError):
    """Stable, single-line, value-free closure diagnostic."""

    def __init__(self, code: str, path: Any = LEDGER_PATH) -> None:
        self.code = code
        self.path = diagnostic_path(path)
        super().__init__(self.code, self.path)

    def __str__(self) -> str:
        return f"{self.code} {self.path}"


GitRunner = Callable[[str, tuple[str, ...]], subprocess.CompletedProcess[bytes]]


def _git_arguments_allowed(arguments: tuple[str, ...]) -> bool:
    inventory_queries = {
        ("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", root)
        for root in INVENTORY_ROOTS
    }
    inventory_queries.update(
        {("ls-files", "-z", "--stage", "--", root) for root in INVENTORY_ROOTS}
    )
    inventory_queries.add(("ls-files", "-z", "--stage", "--", *SOURCE_PATHS))
    inventory_queries.add(
        (
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            REGISTRY_PATH,
        )
    )
    inventory_queries.add(("ls-files", "-z", "--stage", "--", REGISTRY_PATH))
    inventory_queries.add(
        (
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            *CONTROL_PATHS,
        )
    )
    inventory_queries.add(("ls-files", "-z", "--stage", "--", *CONTROL_PATHS))
    if arguments in inventory_queries:
        return True
    return (
        len(arguments) == 3
        and arguments[:2]
        in {
            ("cat-file", "-t"),
            ("cat-file", "-s"),
            ("cat-file", "blob"),
        }
        and FULL_OID.fullmatch(arguments[2]) is not None
    )


def _run_git(
    root: str, arguments: tuple[str, ...]
) -> subprocess.CompletedProcess[bytes]:
    if not _git_arguments_allowed(arguments):
        raise ClosureError("CLOSURE-GIT-QUERY", ".git")
    try:
        return subprocess.run(
            [GIT_EXECUTABLE, *arguments],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=CLOSED_GIT_ENVIRONMENT,
            timeout=GIT_TIMEOUT_SECONDS,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ClosureError("CLOSURE-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise ClosureError("CLOSURE-GIT-STARTUP", ".git") from exc


def _git(root: str, arguments: tuple[str, ...], runner: GitRunner) -> bytes:
    if not _git_arguments_allowed(arguments):
        raise ClosureError("CLOSURE-GIT-QUERY", ".git")
    try:
        result = runner(root, arguments)
    except subprocess.TimeoutExpired as exc:
        raise ClosureError("CLOSURE-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise ClosureError("CLOSURE-GIT-STARTUP", ".git") from exc
    if (
        not isinstance(result, subprocess.CompletedProcess)
        or result.returncode != 0
        or not isinstance(result.stdout, bytes)
    ):
        raise ClosureError("CLOSURE-GIT-RESULT", ".git")
    return result.stdout


def _parse_nul_paths(payload: bytes, scope: str) -> list[str]:
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
    paths: list[str] = []
    for raw in payload[:-1].split(b"\0") if payload else ():
        try:
            path = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path) or not path.startswith(f"{scope}/"):
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", scope)
    return sorted(paths)


def _parse_exact_nul_paths(payload: bytes, allowed_paths: set[str]) -> list[str]:
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
    paths: list[str] = []
    for raw in payload[:-1].split(b"\0") if payload else ():
        try:
            path = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path) or path not in allowed_paths:
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise ClosureError("CLOSURE-INVENTORY-DUPLICATE")
    return sorted(paths)


def _parse_modes(
    payload: bytes,
    *,
    scope: str | None = None,
    allowed_paths: set[str] | None = None,
) -> dict[str, str]:
    if payload and not payload.endswith(b"\0"):
        raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
    modes: dict[str, str] = {}
    for raw in payload[:-1].split(b"\0") if payload else ():
        match = MODE_RECORD.fullmatch(raw)
        if match is None:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git")
        try:
            path = match.group("path").decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ClosureError("CLOSURE-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path):
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        if scope is not None and not path.startswith(f"{scope}/"):
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        if allowed_paths is not None and path not in allowed_paths:
            raise ClosureError("CLOSURE-INVENTORY-PATH", path)
        expected_mode = b"100755" if path == AGGREGATE_PATH else b"100644"
        if match.group("mode") != expected_mode or match.group("stage") != b"0":
            raise ClosureError("CLOSURE-INVENTORY-OBJECT", path)
        if path in modes:
            raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", path)
        modes[path] = match.group("oid").decode("ascii")
    return modes


def _normalize_root(root: str | os.PathLike[str]) -> str:
    try:
        value = os.fspath(root)
    except TypeError as exc:
        raise ClosureError("CLOSURE-ROOT", ".") from exc
    if not isinstance(value, str) or not value or "\0" in value:
        raise ClosureError("CLOSURE-ROOT", ".")
    normalized = os.path.abspath(value)
    if not os.path.isdir(normalized) or os.path.islink(normalized):
        raise ClosureError("CLOSURE-ROOT", ".")
    return normalized


def _read_descriptor_bytes(root: str, relative: str) -> bytes:
    if not is_safe_path(relative):
        raise ClosureError("CLOSURE-INVENTORY-PATH", relative)
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
    descriptors: list[int] = []
    try:
        try:
            current = os.open(root, directory_flags)
        except OSError as exc:
            raise ClosureError("CLOSURE-ROOT", ".") from exc
        descriptors.append(current)
        parts = relative.split("/")
        for part in parts[:-1]:
            try:
                current = os.open(part, directory_flags, dir_fd=current)
            except OSError as exc:
                raise ClosureError("CLOSURE-INVENTORY-OBJECT", relative) from exc
            descriptors.append(current)
        try:
            descriptor = os.open(parts[-1], file_flags, dir_fd=current)
        except FileNotFoundError as exc:
            raise ClosureError("CLOSURE-INVENTORY-MISSING", relative) from exc
        except OSError as exc:
            raise ClosureError("CLOSURE-INVENTORY-OBJECT", relative) from exc
        descriptors.append(descriptor)
        try:
            metadata = os.fstat(descriptor)
        except OSError as exc:
            raise ClosureError("CLOSURE-READ", relative) from exc
        if not stat.S_ISREG(metadata.st_mode):
            raise ClosureError("CLOSURE-INVENTORY-OBJECT", relative)
        if metadata.st_size > MAX_FILE_BYTES:
            raise ClosureError("CLOSURE-BOUNDS", relative)
        chunks: list[bytes] = []
        total = 0
        while True:
            try:
                chunk = os.read(descriptor, min(65_536, MAX_FILE_BYTES + 1 - total))
            except OSError as exc:
                raise ClosureError("CLOSURE-READ", relative) from exc
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise ClosureError("CLOSURE-BOUNDS", relative)
        return b"".join(chunks)
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _index_blob(root: str, oid: str, path: str, runner: GitRunner) -> bytes:
    if FULL_OID.fullmatch(oid) is None:
        raise ClosureError("CLOSURE-BLOB-ID", path)
    if _git(root, ("cat-file", "-t", oid), runner) != b"blob\n":
        raise ClosureError("CLOSURE-BLOB-TYPE", path)
    size_payload = _git(root, ("cat-file", "-s", oid), runner)
    if re.fullmatch(rb"(?:0|[1-9][0-9]*)\n", size_payload) is None:
        raise ClosureError("CLOSURE-BLOB-SIZE", path)
    size = int(size_payload)
    if size > MAX_FILE_BYTES:
        raise ClosureError("CLOSURE-BOUNDS", path)
    payload = _git(root, ("cat-file", "blob", oid), runner)
    if len(payload) != size:
        raise ClosureError("CLOSURE-BLOB-LENGTH", path)
    return payload


def _decode_text(payload: bytes, path: str) -> str:
    try:
        return payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ClosureError("CLOSURE-UTF8", path) from exc


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ClosureError("CLOSURE-JSON-DUPLICATE")
        result[key] = value
    return result


def _load_json_bytes(payload: bytes, path: str) -> Any:
    try:
        return json.loads(
            _decode_text(payload, path), object_pairs_hook=_reject_duplicate_pairs
        )
    except ClosureError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ClosureError("CLOSURE-JSON", path) from exc


def _frontmatter(text: str, path: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ClosureError("CLOSURE-FRONTMATTER", path)
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ClosureError("CLOSURE-FRONTMATTER", path)
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith((" ", "-")):
            continue
        match = FRONTMATTER_LINE.fullmatch(line)
        if match is None:
            continue
        key = match.group("key")
        if key in metadata:
            raise ClosureError("CLOSURE-FRONTMATTER", path)
        metadata[key] = match.group("value").strip().strip("'\"")
    return metadata


def _inventory(
    root: str, scope: str, runner: GitRunner
) -> tuple[list[str], dict[str, str]]:
    paths = _parse_nul_paths(
        _git(
            root,
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                scope,
            ),
            runner,
        ),
        scope,
    )
    modes = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", scope), runner),
        scope=scope,
    )
    if not set(modes).issubset(paths):
        raise ClosureError("CLOSURE-INVENTORY-DRIFT", scope)
    required = MANDATORY_OWNER_PATHS.get(scope, frozenset())
    missing = required - set(modes)
    if missing:
        raise ClosureError("CLOSURE-OWNER-INVENTORY", sorted(missing)[0])
    return paths, modes


def _source_index(root: str, runner: GitRunner) -> dict[str, str]:
    index = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", *SOURCE_PATHS), runner),
        allowed_paths=set(SOURCE_PATHS),
    )
    if set(index) != set(SOURCE_PATHS):
        raise ClosureError("CLOSURE-SOURCE-INVENTORY", ".git")
    return index


def _control_inventory(root: str, runner: GitRunner) -> dict[str, str]:
    allowed = set(CONTROL_PATHS)
    paths = _parse_exact_nul_paths(
        _git(
            root,
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                *CONTROL_PATHS,
            ),
            runner,
        ),
        allowed,
    )
    if set(paths) != allowed:
        raise ClosureError("CLOSURE-CONTROL-INVENTORY", ".git")
    index = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", *CONTROL_PATHS), runner),
        allowed_paths=allowed,
    )
    missing = allowed - set(index)
    if missing:
        raise ClosureError("CLOSURE-CONTROL-INVENTORY", sorted(missing)[0])
    if set(index) != allowed:
        raise ClosureError("CLOSURE-CONTROL-INVENTORY", ".git")
    return index


def _registry_inventory(root: str, runner: GitRunner) -> dict[str, str]:
    allowed = {REGISTRY_PATH}
    paths = _parse_exact_nul_paths(
        _git(
            root,
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                REGISTRY_PATH,
            ),
            runner,
        ),
        allowed,
    )
    if paths != [REGISTRY_PATH]:
        raise ClosureError("CLOSURE-REGISTRY-INVENTORY", REGISTRY_PATH)
    index = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", REGISTRY_PATH), runner),
        allowed_paths=allowed,
    )
    if set(index) != allowed:
        raise ClosureError("CLOSURE-REGISTRY-INVENTORY", REGISTRY_PATH)
    return index


def _proposed_or_index_bytes(
    root: str,
    path: str,
    index: Mapping[str, str],
    runner: GitRunner,
) -> bytes:
    descriptor = _read_descriptor_bytes(root, path)
    oid = index.get(path)
    if oid is None:
        return descriptor
    staged = _index_blob(root, oid, path, runner)
    if descriptor != staged:
        raise ClosureError("CLOSURE-WORKTREE-INDEX-DRIFT", path)
    return staged


def _load_registry_authority(
    root: str, runner: GitRunner = _run_git
) -> Mapping[str, Any]:
    index = _registry_inventory(root, runner)
    registry = _load_json_bytes(
        _proposed_or_index_bytes(root, REGISTRY_PATH, index, runner), REGISTRY_PATH
    )
    if not isinstance(registry, Mapping):
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", REGISTRY_PATH)
    return registry


def _authored_stage04(paths: Sequence[str], scope: str) -> list[str]:
    result: list[str] = []
    support_readme = f"{scope}/README.md"
    for path in paths:
        if path == support_readme:
            continue
        if not path.endswith(".md") or path.count("/") != 3:
            raise ClosureError("CLOSURE-STAGE04-PATH", path)
        result.append(path)
    return result


def _object_identity(
    path: str, index: Mapping[str, str], payload: bytes
) -> dict[str, str]:
    oid = index.get(path)
    if oid is not None:
        return {"objectMode": "index-stage-zero", "objectId": _git_identity(oid)}
    return {
        "objectMode": "proposed-nonignored-descriptor",
        "objectId": _sha256_identity(hashlib.sha256(payload).hexdigest()),
    }


def _build_current_rows(
    plan_paths: Sequence[str],
    task_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    eligibility: Mapping[str, Any],
) -> list[dict[str, Any]]:
    candidates = eligibility.get("candidateRows")
    controls = eligibility.get("controls")
    if not isinstance(candidates, list) or not isinstance(controls, list):
        raise ClosureError("CLOSURE-ELIGIBILITY-SCHEMA", SOURCE_PATHS[1])
    defer_by_path = {
        row.get("path"): row
        for row in candidates
        if isinstance(row, Mapping) and row.get("disposition") == "DEFER"
    }
    control_by_path = {
        row.get("path"): row for row in controls if isinstance(row, Mapping)
    }
    frozen_paths = set(defer_by_path) | set(control_by_path)
    paths = sorted(frozen_paths)
    if not frozen_paths.issubset(set(plan_paths) | set(task_paths)):
        raise ClosureError("CLOSURE-CURRENT-RESIDUE")
    entries: list[dict[str, Any]] = []
    for path in paths:
        payload = payloads[path]
        metadata = _frontmatter(_decode_text(payload, path), path)
        kind = "plan" if path.startswith(f"{PLAN_ROOT}/") else "task"
        if (
            metadata.get("type") != f"sdlc/{kind}"
            or metadata.get("owner") != "platform"
        ):
            raise ClosureError("CLOSURE-CURRENT-AUTHORITY", path)
        identity = _object_identity(path, index, payload)
        if path in defer_by_path:
            source = defer_by_path[path]
            if metadata.get("status") != "done":
                raise ClosureError("CLOSURE-CURRENT-STATUS", path)
            if (
                source.get("kind") != kind
                or source.get("owner") != "platform"
                or source.get("status") != "done"
                or not isinstance(source.get("reason"), str)
                or not source.get("reason")
                or not isinstance(source.get("refreshTrigger"), str)
                or not source.get("refreshTrigger")
                or not isinstance(source.get("missingAxes"), list)
                or not source.get("missingAxes")
                or source.get("residueClass")
                not in {"deferred-evidence", "resolved-partial-evidence"}
            ):
                raise ClosureError("CLOSURE-SOURCE-DEFER", path)
            entries.append(
                {
                    "path": path,
                    "kind": kind,
                    "lineageId": source.get("pairKey"),
                    "profile": metadata.get("type"),
                    "status": "done",
                    **identity,
                    "sourceDisposition": "DEFER",
                    "sourceReason": source.get("reason"),
                    "sourceOwner": source.get("owner"),
                    "sourceRefreshTrigger": source.get("refreshTrigger"),
                    "missingAxes": source.get("missingAxes"),
                    "residueClass": source.get("residueClass"),
                    "disposition": "DEFER",
                    "owner": "platform",
                    "closureReason": DEFER_CLOSURE_REASON,
                    "postClosureRefreshTrigger": DEFER_TRIGGER,
                    "currentAuthority": DEFER_AUTHORITY,
                }
            )
        else:
            source = control_by_path[path]
            if metadata.get("status") != "done":
                raise ClosureError("CLOSURE-CONTROL-STATUS", path)
            if (
                source.get("kind") != kind
                or source.get("disposition") != "retain"
                or source.get("owner") != "platform"
                or source.get("reason") != "active-spec-037-control"
                or source.get("refreshTrigger") != "Spec037 closure"
            ):
                raise ClosureError("CLOSURE-CONTROL-SOURCE", path)
            entries.append(
                {
                    "path": path,
                    "kind": kind,
                    "lineageId": source.get("pairKey"),
                    "profile": metadata.get("type"),
                    "status": "done",
                    **identity,
                    "sourceDisposition": "retain",
                    "sourceReason": source.get("reason"),
                    "sourceOwner": source.get("owner"),
                    "sourceRefreshTrigger": source.get("refreshTrigger"),
                    "missingAxes": ["successor-migration-evidence"],
                    "residueClass": "terminal-owned-defer",
                    "disposition": "DEFER",
                    "owner": "platform",
                    "reason": TERMINAL_CONTROL_REASON,
                    "currentEvidenceRole": TERMINAL_CONTROL_EVIDENCE_ROLE,
                    "successorRefreshTrigger": TERMINAL_CONTROL_REFRESH_TRIGGER,
                }
            )
    return entries


def _active_control_lineage(path: str, kind: str) -> str:
    scope = PLAN_ROOT if kind == "plan" else TASK_ROOT
    prefix = f"{scope}/"
    if not path.startswith(prefix) or not path.endswith(".md"):
        raise ClosureError("CLOSURE-ACTIVE-CONTROL-LINEAGE", path)
    lineage = path[len(prefix) : -len(".md")]
    if ACTIVE_CONTROL_LINEAGE.fullmatch(lineage) is None:
        raise ClosureError("CLOSURE-ACTIVE-CONTROL-LINEAGE", path)
    return lineage


def _terminal_registry_relations(
    registry: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    lineage = registry.get("programLineage")
    programs = lineage.get("programs") if isinstance(lineage, Mapping) else None
    if not isinstance(programs, list):
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", REGISTRY_PATH)

    exact_programs: list[Mapping[str, Any]] = []
    relations: dict[str, list[tuple[Mapping[str, Any], str, Mapping[str, Any]]]] = {
        "038": [],
        "039": [],
        "040": [],
    }
    for program in programs:
        if not isinstance(program, Mapping):
            raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", REGISTRY_PATH)
        if program.get("prd") == "006" and program.get("ard") == "0009":
            exact_programs.append(program)
        for collection_name in ("tranches", "followUps"):
            collection = program.get(collection_name)
            if not isinstance(collection, list):
                raise ClosureError("CLOSURE-TERMINAL-REGISTRY-MALFORMED", REGISTRY_PATH)
            for relation in collection:
                if not isinstance(relation, Mapping):
                    raise ClosureError(
                        "CLOSURE-TERMINAL-REGISTRY-MALFORMED", REGISTRY_PATH
                    )
                spec_id = relation.get("spec")
                if spec_id in relations:
                    relations[str(spec_id)].append((program, collection_name, relation))

    if len(exact_programs) > 1:
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-DUPLICATE", REGISTRY_PATH)
    if len(exact_programs) != 1:
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", REGISTRY_PATH)
    if any(len(relations[spec_id]) > 1 for spec_id in relations):
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-DUPLICATE", REGISTRY_PATH)
    if len(relations["038"]) != 1:
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", REGISTRY_PATH)
    if len(relations["039"]) != 1:
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    if len(relations["040"]) != 1:
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)

    exact_program = exact_programs[0]
    program_038, collection_038, relation_038 = relations["038"][0]
    if program_038 is not exact_program or collection_038 != "tranches":
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", REGISTRY_PATH)
    if set(relation_038) != {*TERMINAL_RELATION_IDENTITY, "state"} or any(
        relation_038.get(key) != value
        for key, value in TERMINAL_RELATION_IDENTITY.items()
    ):
        raise ClosureError("CLOSURE-TERMINAL-REGISTRY-AUTHORITY", REGISTRY_PATH)
    if relation_038.get("state") not in {"active", "done"}:
        raise ClosureError("CLOSURE-TERMINAL-STATE", TERMINAL_SPEC)

    program_039, collection_039, relation_039 = relations["039"][0]
    if (
        program_039 is not exact_program
        or collection_039 != "tranches"
        or set(relation_039) != {*TERMINAL_SUCCESSOR_IDENTITY, "state"}
        or any(
            relation_039.get(key) != value
            for key, value in TERMINAL_SUCCESSOR_IDENTITY.items()
        )
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    program_040, collection_040, relation_040 = relations["040"][0]
    if (
        program_040 is not exact_program
        or collection_040 != "tranches"
        or set(relation_040) != {*TERMINAL_FRONTIER_IDENTITY, "state"}
        or any(
            relation_040.get(key) != value
            for key, value in TERMINAL_FRONTIER_IDENTITY.items()
        )
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)
    return relation_038, relation_039, relation_040


def _partition_terminal_controls(
    plan_paths: Sequence[str],
    task_paths: Sequence[str],
    spec_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    registry: Mapping[str, Any],
) -> dict[str, Any]:
    for paths, path in (
        (plan_paths, TERMINAL_PLAN),
        (task_paths, TERMINAL_TASK),
        (spec_paths, TERMINAL_SPEC),
        (spec_paths, TERMINAL_SUCCESSOR_SPEC),
        (spec_paths, TERMINAL_FRONTIER_SPEC),
    ):
        count = paths.count(path)
        if count > 1:
            raise ClosureError("CLOSURE-TERMINAL-DUPLICATE", path)
        if count != 1:
            code = (
                "CLOSURE-TERMINAL-FRONTIER"
                if path in {TERMINAL_SUCCESSOR_SPEC, TERMINAL_FRONTIER_SPEC}
                else "CLOSURE-TERMINAL-INCOMPLETE"
            )
            raise ClosureError(code, path)

    metadata: dict[str, dict[str, str]] = {}
    expected_profiles = {
        TERMINAL_SPEC: "sdlc/spec",
        TERMINAL_PLAN: "sdlc/plan",
        TERMINAL_TASK: "sdlc/task",
        TERMINAL_SUCCESSOR_SPEC: "sdlc/spec",
        TERMINAL_FRONTIER_SPEC: "sdlc/spec",
    }
    for path, profile in expected_profiles.items():
        if path not in payloads:
            raise ClosureError("CLOSURE-TERMINAL-INCOMPLETE", path)
        values = _frontmatter(_decode_text(payloads[path], path), path)
        if values.get("type") != profile or values.get("owner") != "platform":
            raise ClosureError("CLOSURE-TERMINAL-AUTHORITY", path)
        metadata[path] = values

    relation, successor_relation, frontier_relation = _terminal_registry_relations(
        registry
    )
    successor_state = metadata[TERMINAL_SUCCESSOR_SPEC].get("status")
    frontier_state = metadata[TERMINAL_FRONTIER_SPEC].get("status")
    if (
        frontier_state not in {"active", "done"}
        or frontier_relation.get("state") != frontier_state
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)
    if (
        successor_state not in {"active", "done"}
        or successor_relation.get("state") != successor_state
    ):
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    if frontier_state == "done" and successor_state != "done":
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)

    document_states = {
        metadata[path].get("status")
        for path in (TERMINAL_SPEC, TERMINAL_PLAN, TERMINAL_TASK)
    }
    if document_states not in ({"active"}, {"done"}):
        raise ClosureError("CLOSURE-TERMINAL-STATE", TERMINAL_SPEC)
    state = next(iter(document_states))
    if relation.get("state") != state:
        raise ClosureError("CLOSURE-TERMINAL-STATE", TERMINAL_SPEC)
    if state == "active" and successor_state != "active":
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_SUCCESSOR_SPEC)
    if state == "active" and frontier_state != "active":
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC)

    successor_controls_required = state == "done" or any(
        path in paths
        for path, paths in (
            (TERMINAL_SUCCESSOR_PLAN, plan_paths),
            (TERMINAL_SUCCESSOR_TASK, task_paths),
        )
    )
    if successor_controls_required:
        for paths, path, profile in (
            (plan_paths, TERMINAL_SUCCESSOR_PLAN, "sdlc/plan"),
            (task_paths, TERMINAL_SUCCESSOR_TASK, "sdlc/task"),
        ):
            count = paths.count(path)
            if count > 1:
                raise ClosureError("CLOSURE-TERMINAL-DUPLICATE", path)
            if count != 1:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            if path not in payloads:
                raise ClosureError("CLOSURE-TERMINAL-INCOMPLETE", path)
            values = _frontmatter(_decode_text(payloads[path], path), path)
            if values.get("type") != profile or values.get("owner") != "platform":
                raise ClosureError("CLOSURE-TERMINAL-AUTHORITY", path)
            if values.get("status") != successor_state:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            metadata[path] = values

    frontier_controls_required = frontier_state == "done" or any(
        path in paths
        for path, paths in (
            (TERMINAL_FRONTIER_PLAN, plan_paths),
            (TERMINAL_FRONTIER_TASK, task_paths),
        )
    )
    if frontier_controls_required:
        for paths, path, profile in (
            (plan_paths, TERMINAL_FRONTIER_PLAN, "sdlc/plan"),
            (task_paths, TERMINAL_FRONTIER_TASK, "sdlc/task"),
        ):
            count = paths.count(path)
            if count > 1:
                raise ClosureError("CLOSURE-TERMINAL-DUPLICATE", path)
            if count != 1:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            if path not in payloads:
                raise ClosureError("CLOSURE-TERMINAL-INCOMPLETE", path)
            values = _frontmatter(_decode_text(payloads[path], path), path)
            if values.get("type") != profile or values.get("owner") != "platform":
                raise ClosureError("CLOSURE-TERMINAL-AUTHORITY", path)
            if values.get("status") != frontier_state:
                raise ClosureError("CLOSURE-TERMINAL-FRONTIER", path)
            metadata[path] = values

    result = {
        "planPaths": sorted(plan_paths),
        "taskPaths": sorted(task_paths),
        "specPaths": sorted(spec_paths),
        "terminalControlRows": [],
        "terminalControlPairCardinality": [],
        "terminalSpecRows": [],
    }
    if state == "active":
        return result

    terminal_plans = {TERMINAL_PLAN}
    terminal_tasks = {TERMINAL_TASK}
    if successor_state == "done":
        terminal_plans.add(TERMINAL_SUCCESSOR_PLAN)
        terminal_tasks.add(TERMINAL_SUCCESSOR_TASK)
    if frontier_state == "done":
        terminal_plans.add(TERMINAL_FRONTIER_PLAN)
        terminal_tasks.add(TERMINAL_FRONTIER_TASK)
    result["planPaths"] = sorted(
        path for path in plan_paths if path not in terminal_plans
    )
    result["taskPaths"] = sorted(
        path for path in task_paths if path not in terminal_tasks
    )
    terminal_specs = {TERMINAL_SPEC}
    if successor_state == "done":
        terminal_specs.add(TERMINAL_SUCCESSOR_SPEC)
    if frontier_state == "done":
        terminal_specs.add(TERMINAL_FRONTIER_SPEC)
    result["specPaths"] = sorted(
        path for path in spec_paths if path not in terminal_specs
    )
    terminal_control_paths = [
        (TERMINAL_PLAN, "plan", TERMINAL_LINEAGE),
        (TERMINAL_TASK, "task", TERMINAL_LINEAGE),
    ]
    if successor_state == "done":
        terminal_control_paths.extend(
            [
                (
                    TERMINAL_SUCCESSOR_PLAN,
                    "plan",
                    TERMINAL_SUCCESSOR_LINEAGE,
                ),
                (
                    TERMINAL_SUCCESSOR_TASK,
                    "task",
                    TERMINAL_SUCCESSOR_LINEAGE,
                ),
            ]
        )
    if frontier_state == "done":
        terminal_control_paths.extend(
            [
                (
                    TERMINAL_FRONTIER_PLAN,
                    "plan",
                    TERMINAL_FRONTIER_LINEAGE,
                ),
                (
                    TERMINAL_FRONTIER_TASK,
                    "task",
                    TERMINAL_FRONTIER_LINEAGE,
                ),
            ]
        )
    result["terminalControlRows"] = sorted(
        [
            {
                "path": path,
                "kind": kind,
                "lineageId": lineage,
                "profile": f"sdlc/{kind}",
                "status": "done",
                "owner": "platform",
                **_object_identity(path, index, payloads[path]),
            }
            for path, kind, lineage in terminal_control_paths
        ],
        key=lambda row: str(row["path"]),
    )
    result["terminalControlPairCardinality"] = [
        {
            "lineageId": TERMINAL_LINEAGE,
            "state": "complete",
            "planPath": TERMINAL_PLAN,
            "taskPath": TERMINAL_TASK,
            "owner": "platform",
            "status": "done",
        }
    ]
    result["terminalSpecRows"] = [
        {
            "path": TERMINAL_SPEC,
            "profile": "sdlc/spec",
            "status": "done",
            "owner": "platform",
            **_object_identity(TERMINAL_SPEC, index, payloads[TERMINAL_SPEC]),
            "registryPath": REGISTRY_PATH,
            "programPrd": "006",
            "programArd": "0009",
            "relationClass": "original-tranche",
            **TERMINAL_RELATION_IDENTITY,
            "state": "done",
        }
    ]
    if successor_state == "done":
        result["terminalControlPairCardinality"].append(
            {
                "lineageId": TERMINAL_SUCCESSOR_LINEAGE,
                "state": "complete",
                "planPath": TERMINAL_SUCCESSOR_PLAN,
                "taskPath": TERMINAL_SUCCESSOR_TASK,
                "owner": "platform",
                "status": "done",
            }
        )
        result["terminalSpecRows"].append(
            {
                "path": TERMINAL_SUCCESSOR_SPEC,
                "profile": "sdlc/spec",
                "status": "done",
                "owner": "platform",
                **_object_identity(
                    TERMINAL_SUCCESSOR_SPEC,
                    index,
                    payloads[TERMINAL_SUCCESSOR_SPEC],
                ),
                "registryPath": REGISTRY_PATH,
                "programPrd": "006",
                "programArd": "0009",
                "relationClass": "original-tranche",
                **TERMINAL_SUCCESSOR_IDENTITY,
                "state": "done",
            }
        )
    if frontier_state == "done":
        result["terminalControlPairCardinality"].append(
            {
                "lineageId": TERMINAL_FRONTIER_LINEAGE,
                "state": "complete",
                "planPath": TERMINAL_FRONTIER_PLAN,
                "taskPath": TERMINAL_FRONTIER_TASK,
                "owner": "platform",
                "status": "done",
            }
        )
        result["terminalSpecRows"].append(
            {
                "path": TERMINAL_FRONTIER_SPEC,
                "profile": "sdlc/spec",
                "status": "done",
                "owner": "platform",
                **_object_identity(
                    TERMINAL_FRONTIER_SPEC,
                    index,
                    payloads[TERMINAL_FRONTIER_SPEC],
                ),
                "registryPath": REGISTRY_PATH,
                "programPrd": "006",
                "programArd": "0009",
                "relationClass": "original-tranche",
                **TERMINAL_FRONTIER_IDENTITY,
                "state": "done",
            }
        )
    return result


def _build_active_control_rows(
    plan_paths: Sequence[str],
    task_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for kind, paths in (("plan", plan_paths), ("task", task_paths)):
        for path in paths:
            payload = payloads[path]
            metadata = _frontmatter(_decode_text(payload, path), path)
            if (
                metadata.get("type") != f"sdlc/{kind}"
                or metadata.get("owner") != "platform"
            ):
                raise ClosureError("CLOSURE-ACTIVE-CONTROL-AUTHORITY", path)
            if metadata.get("status") != "active":
                raise ClosureError("CLOSURE-ACTIVE-CONTROL-STATUS", path)
            entries.append(
                {
                    "path": path,
                    "kind": kind,
                    "lineageId": _active_control_lineage(path, kind),
                    "profile": metadata.get("type"),
                    "status": "active",
                    "owner": "platform",
                    **_object_identity(path, index, payload),
                }
            )
    return sorted(entries, key=lambda row: str(row["path"]))


def _build_active_control_pairs(
    active: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in active:
        lineage = row.get("lineageId")
        kind = row.get("kind")
        if (
            not isinstance(lineage, str)
            or ACTIVE_CONTROL_LINEAGE.fullmatch(lineage) is None
            or kind not in {"plan", "task"}
        ):
            raise ClosureError("CLOSURE-ACTIVE-CONTROL-LINEAGE", row.get("path"))
        if kind in grouped[lineage]:
            raise ClosureError("CLOSURE-ACTIVE-CONTROL-DUPLICATE", row.get("path"))
        grouped[lineage][str(kind)] = row
    pairs: list[dict[str, Any]] = []
    for lineage, members in sorted(grouped.items()):
        if set(members) != {"plan", "task"}:
            member = next(iter(members.values()))
            raise ClosureError("CLOSURE-ACTIVE-CONTROL-PAIR", member.get("path"))
        pairs.append(
            {
                "lineageId": lineage,
                "state": "complete",
                "planPath": members["plan"]["path"],
                "taskPath": members["task"]["path"],
                "owner": "platform",
                "status": "active",
            }
        )
    return pairs


def _validate_terminal_frontier_shape(observed: Mapping[str, Any]) -> str:
    """Reject every production frontier other than the three closed shapes."""

    control_keys = {
        "path",
        "kind",
        "lineageId",
        "profile",
        "status",
        "owner",
        "objectMode",
        "objectId",
    }
    pair_keys = {
        "lineageId",
        "state",
        "planPath",
        "taskPath",
        "owner",
        "status",
    }
    spec_keys = {
        "path",
        "profile",
        "status",
        "owner",
        "objectMode",
        "objectId",
        "registryPath",
        "programPrd",
        "programArd",
        "relationClass",
        "spec",
        "order",
        "reason",
        "decision",
        "state",
    }
    families = (
        {
            "specPath": TERMINAL_SPEC,
            "planPath": TERMINAL_PLAN,
            "taskPath": TERMINAL_TASK,
            "lineageId": TERMINAL_LINEAGE,
            "relation": TERMINAL_RELATION_IDENTITY,
        },
        {
            "specPath": TERMINAL_SUCCESSOR_SPEC,
            "planPath": TERMINAL_SUCCESSOR_PLAN,
            "taskPath": TERMINAL_SUCCESSOR_TASK,
            "lineageId": TERMINAL_SUCCESSOR_LINEAGE,
            "relation": TERMINAL_SUCCESSOR_IDENTITY,
        },
        {
            "specPath": TERMINAL_FRONTIER_SPEC,
            "planPath": TERMINAL_FRONTIER_PLAN,
            "taskPath": TERMINAL_FRONTIER_TASK,
            "lineageId": TERMINAL_FRONTIER_LINEAGE,
            "relation": TERMINAL_FRONTIER_IDENTITY,
        },
    )

    def rows_for(key: str) -> list[Mapping[str, Any]]:
        rows = observed.get(key)
        if not isinstance(rows, list) or any(
            not isinstance(row, Mapping) for row in rows
        ):
            raise ClosureError(
                "CLOSURE-TERMINAL-FRONTIER", TERMINAL_FRONTIER_SPEC
            )
        return rows

    active_rows = rows_for("activeControlRows")
    active_pairs = rows_for("activeControlPairCardinality")
    terminal_rows = rows_for("terminalControlRows")
    terminal_pairs = rows_for("terminalControlPairCardinality")
    terminal_specs = rows_for("terminalSpecRows")
    terminal_authority = rows_for("terminalProgramClosureAuthority")

    spec_paths = tuple(row.get("path") for row in terminal_specs)
    modes = {
        (TERMINAL_SPEC,): ("current", 1),
        (TERMINAL_SPEC, TERMINAL_SUCCESSOR_SPEC): ("advanced", 2),
        (
            TERMINAL_SPEC,
            TERMINAL_SUCCESSOR_SPEC,
            TERMINAL_FRONTIER_SPEC,
        ): ("terminal", 3),
    }
    mode = modes.get(spec_paths)
    if mode is None:
        unexpected = next(
            (
                path
                for path in spec_paths
                if is_safe_path(path)
                and path
                not in {
                    TERMINAL_SPEC,
                    TERMINAL_SUCCESSOR_SPEC,
                    TERMINAL_FRONTIER_SPEC,
                }
            ),
            TERMINAL_FRONTIER_SPEC,
        )
        raise ClosureError("CLOSURE-TERMINAL-FRONTIER", unexpected)
    mode_name, done_count = mode
    terminal_families = families[:done_count]
    active_families = families[done_count : done_count + 1]

    def object_identity_is_indexed(row: Mapping[str, Any]) -> bool:
        value = row.get("objectId")
        if row.get("objectMode") != "index-stage-zero" or not isinstance(
            value, str
        ):
            return False
        parts = value.split(":")
        return (
            len(parts) == 3
            and parts[0] == "git"
            and parts[1] in {"sha1", "sha256"}
            and FULL_OID.fullmatch(parts[2]) is not None
            and (parts[1] == "sha1") == (len(parts[2]) == 40)
        )

    def control_signature(row: Mapping[str, Any]) -> tuple[Any, ...] | None:
        if set(row) != control_keys or not object_identity_is_indexed(row):
            return None
        return (
            row.get("path"),
            row.get("kind"),
            row.get("lineageId"),
            row.get("profile"),
            row.get("status"),
            row.get("owner"),
        )

    def expected_control_rows(
        selected: Sequence[Mapping[str, Any]], status: str
    ) -> list[tuple[Any, ...]]:
        return sorted(
            [
                (
                    family[f"{kind}Path"],
                    kind,
                    family["lineageId"],
                    f"sdlc/{kind}",
                    status,
                    "platform",
                )
                for family in selected
                for kind in ("plan", "task")
            ],
            key=lambda row: str(row[0]),
        )

    def pair_signature(row: Mapping[str, Any]) -> tuple[Any, ...] | None:
        if set(row) != pair_keys:
            return None
        return (
            row.get("lineageId"),
            row.get("state"),
            row.get("planPath"),
            row.get("taskPath"),
            row.get("owner"),
            row.get("status"),
        )

    def expected_pairs(
        selected: Sequence[Mapping[str, Any]], status: str
    ) -> list[tuple[Any, ...]]:
        return [
            (
                family["lineageId"],
                "complete",
                family["planPath"],
                family["taskPath"],
                "platform",
                status,
            )
            for family in selected
        ]

    def spec_signature(row: Mapping[str, Any]) -> tuple[Any, ...] | None:
        if set(row) != spec_keys or not object_identity_is_indexed(row):
            return None
        return (
            row.get("path"),
            row.get("profile"),
            row.get("status"),
            row.get("owner"),
            row.get("registryPath"),
            row.get("programPrd"),
            row.get("programArd"),
            row.get("relationClass"),
            row.get("spec"),
            row.get("order"),
            row.get("reason"),
            row.get("decision"),
            row.get("state"),
        )

    def expected_specs(
        selected: Sequence[Mapping[str, Any]],
    ) -> list[tuple[Any, ...]]:
        return [
            (
                family["specPath"],
                "sdlc/spec",
                "done",
                "platform",
                REGISTRY_PATH,
                "006",
                "0009",
                "original-tranche",
                family["relation"]["spec"],
                family["relation"]["order"],
                family["relation"]["reason"],
                family["relation"]["decision"],
                "done",
            )
            for family in selected
        ]

    expected_active_rows = expected_control_rows(active_families, "active")
    expected_terminal_rows = expected_control_rows(terminal_families, "done")
    expected_active_pairs = expected_pairs(active_families, "active")
    expected_terminal_pairs = expected_pairs(terminal_families, "done")
    expected_terminal_specs = expected_specs(terminal_families)

    def failure_path(
        rows: Sequence[Mapping[str, Any]],
        expected_paths: set[str],
        *,
        pair: bool = False,
    ) -> str:
        fields = ("planPath", "taskPath") if pair else ("path",)
        actual_paths = {
            row.get(field)
            for row in rows
            for field in fields
            if is_safe_path(row.get(field))
        }
        unexpected = sorted(actual_paths - expected_paths)
        if unexpected:
            return unexpected[0]
        missing = sorted(expected_paths - actual_paths)
        if missing:
            return missing[0]
        return next(iter(sorted(actual_paths)), TERMINAL_FRONTIER_SPEC)

    comparisons = (
        (
            [control_signature(row) for row in active_rows],
            expected_active_rows,
            active_rows,
            {str(row[0]) for row in expected_active_rows},
            False,
        ),
        (
            [pair_signature(row) for row in active_pairs],
            expected_active_pairs,
            active_pairs,
            {
                str(path)
                for row in expected_active_pairs
                for path in (row[2], row[3])
            },
            True,
        ),
        (
            [control_signature(row) for row in terminal_rows],
            expected_terminal_rows,
            terminal_rows,
            {str(row[0]) for row in expected_terminal_rows},
            False,
        ),
        (
            [pair_signature(row) for row in terminal_pairs],
            expected_terminal_pairs,
            terminal_pairs,
            {
                str(path)
                for row in expected_terminal_pairs
                for path in (row[2], row[3])
            },
            True,
        ),
        (
            [spec_signature(row) for row in terminal_specs],
            expected_terminal_specs,
            terminal_specs,
            {str(row[0]) for row in expected_terminal_specs},
            False,
        ),
    )
    for actual, expected, rows, paths, pair in comparisons:
        if actual != expected:
            raise ClosureError(
                "CLOSURE-TERMINAL-FRONTIER",
                failure_path(rows, paths, pair=pair),
            )
    expected_terminal_authority = (
        [
            (
                TERMINAL_PROGRAM_CLOSURE_ADR,
                "sdlc/adr",
                "accepted",
                "platform",
                "terminal-program-closure-decision",
                TERMINAL_FRONTIER_SPEC,
            )
        ]
        if mode_name == "terminal"
        else []
    )
    actual_terminal_authority: list[tuple[Any, ...] | None] = []
    for row in terminal_authority:
        if (
            set(row)
            != {
                "path",
                "profile",
                "status",
                "owner",
                "objectMode",
                "objectId",
                "authorityRole",
                "frontierSpecPath",
            }
            or not object_identity_is_indexed(row)
        ):
            actual_terminal_authority.append(None)
            continue
        actual_terminal_authority.append(
            (
                row.get("path"),
                row.get("profile"),
                row.get("status"),
                row.get("owner"),
                row.get("authorityRole"),
                row.get("frontierSpecPath"),
            )
        )
    if actual_terminal_authority != expected_terminal_authority:
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    return mode_name


def _build_pairs(current: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in current:
        pair_key = row.get("lineageId")
        kind = row.get("kind")
        if (
            not isinstance(pair_key, str)
            or not pair_key
            or kind not in {"plan", "task"}
        ):
            raise ClosureError("CLOSURE-PAIR-KEY", row.get("path"))
        if kind in grouped[pair_key]:
            raise ClosureError("CLOSURE-PAIR-DUPLICATE", row.get("path"))
        grouped[pair_key][str(kind)] = row
    entries: list[dict[str, Any]] = []
    for pair_key, members in sorted(grouped.items()):
        state = (
            "complete"
            if set(members) == {"plan", "task"}
            else "plan-only"
            if "plan" in members
            else "task-only"
        )
        dispositions = {str(row.get("disposition")) for row in members.values()}
        if len(dispositions) != 1:
            raise ClosureError("CLOSURE-PAIR-DISPOSITION")
        disposition = next(iter(dispositions))
        if state != "complete" and (
            disposition != "DEFER"
            or any(row.get("owner") != "platform" for row in members.values())
        ):
            raise ClosureError("CLOSURE-PAIR-PARTIAL")
        entries.append(
            {
                "lineageId": pair_key,
                "state": state,
                "planPath": members.get("plan", {}).get("path"),
                "taskPath": members.get("task", {}).get("path"),
                "disposition": disposition,
                "owner": "platform",
                "partialEvidence": "explicit-owned-DEFER"
                if state != "complete"
                else None,
            }
        )
    return entries


def _build_migrations(
    eligibility: Mapping[str, Any],
    migration: Mapping[str, Any],
    current_paths: set[str],
    archive_paths: set[str],
) -> list[dict[str, Any]]:
    candidates = eligibility.get("candidateRows")
    batches = migration.get("batches")
    if not isinstance(candidates, list) or not isinstance(batches, list):
        raise ClosureError("CLOSURE-MIGRATION-SCHEMA", SOURCE_PATHS[2])
    eligible = {
        row.get("path"): row
        for row in candidates
        if isinstance(row, Mapping) and row.get("disposition") == "eligible"
    }
    result_by_path: dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    for batch in batches:
        if not isinstance(batch, Mapping) or not isinstance(batch.get("records"), list):
            raise ClosureError("CLOSURE-MIGRATION-SCHEMA", SOURCE_PATHS[2])
        for record in batch["records"]:
            if not isinstance(record, Mapping) or not isinstance(
                record.get("originalPath"), str
            ):
                raise ClosureError("CLOSURE-MIGRATION-SCHEMA", SOURCE_PATHS[2])
            original = record["originalPath"]
            if original in result_by_path:
                raise ClosureError("CLOSURE-MIGRATION-DUPLICATE", original)
            result_by_path[original] = (batch, record)
    if set(result_by_path) != set(eligible):
        raise ClosureError("CLOSURE-MIGRATION-STALE")
    expected_candidate_archives = {
        path.replace("docs/04.execution/", "docs/98.archive/04.execution/")
        for path in eligible
    }
    candidate_paths = {
        row.get("path") for row in candidates if isinstance(row, Mapping)
    }
    observed_candidate_archives = {
        archive
        for archive in archive_paths
        if archive.replace("docs/98.archive/04.execution/", "docs/04.execution/")
        in candidate_paths
    }
    if observed_candidate_archives != expected_candidate_archives:
        raise ClosureError("CLOSURE-MIGRATION-ROGUE")
    entries: list[dict[str, Any]] = []
    for path, source in sorted(eligible.items()):
        batch, record = result_by_path[path]
        archive_path = record.get("archivePath")
        if path in current_paths:
            raise ClosureError("CLOSURE-MIGRATION-SOURCE", path)
        if archive_path not in archive_paths:
            raise ClosureError("CLOSURE-MIGRATION-ARCHIVE", archive_path)
        if not (
            path.startswith((f"{PLAN_ROOT}/", f"{TASK_ROOT}/"))
            and isinstance(archive_path, str)
            and archive_path.startswith(
                (f"{ARCHIVE_PLAN_ROOT}/", f"{ARCHIVE_TASK_ROOT}/")
            )
        ):
            raise ClosureError("CLOSURE-MIGRATION-SCOPE", path)
        if (
            source.get("owner") != "platform"
            or not source.get("reason")
            or not batch.get("rollbackParentCommit")
            or not batch.get("currentClosureOwner")
            or record.get("validationResult") != "PASS"
            or record.get("archiveReason") != "completed-lineage"
        ):
            raise ClosureError("CLOSURE-MIGRATION-EVIDENCE", path)
        entries.append(
            {
                "path": path,
                "kind": source.get("kind"),
                "lineageId": source.get("pairKey"),
                "sourceCommit": _git_identity(str(source.get("sourceCommit"))),
                "sourceBlob": _git_identity(str(source.get("sourceBlob"))),
                "historicalDisposition": "eligible",
                "historicalReason": source.get("reason"),
                "disposition": "migrated-closed",
                "owner": "platform",
                "closureReason": "exact-atomic-migration-result-joined",
                "batchId": batch.get("batchId"),
                "batchSequence": batch.get("sequence"),
                "archivePath": archive_path,
                "payloadBytes": record.get("payloadBytes"),
                "payloadSha256": _sha256_identity(record.get("payloadSha256")),
                "archiveReason": record.get("archiveReason"),
                "currentClosureOwner": batch.get("currentClosureOwner"),
                "rollbackParentCommit": _git_identity(
                    str(batch.get("rollbackParentCommit"))
                ),
                "validationResult": record.get("validationResult"),
                "currentSourcePresent": False,
                "archivePresent": True,
            }
        )
    return entries


def _authority_entries(
    paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    *,
    kind: str,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    expected_type = f"sdlc/{kind}"
    expected_status = "accepted" if kind == "adr" else "done"
    authority = ADR_AUTHORITY if kind == "adr" else SPEC_AUTHORITY
    trigger = (
        "accepted-adr-authority-or-evidence-change"
        if kind == "adr"
        else "done-spec-authority-or-evidence-change"
    )
    for path in paths:
        payload = payloads[path]
        metadata = _frontmatter(_decode_text(payload, path), path)
        if metadata.get("status") != expected_status:
            continue
        if metadata.get("type") != expected_type or metadata.get("owner") != "platform":
            raise ClosureError("CLOSURE-AUTHORITY-PROFILE", path)
        entries.append(
            {
                "path": path,
                "profile": expected_type,
                "status": expected_status,
                "owner": "platform",
                **_object_identity(path, index, payload),
                "disposition": "retain",
                "reason": AUTHORITY_REASON,
                "currentAuthority": authority,
                "refreshTrigger": trigger,
            }
        )
    return entries


def _terminal_program_closure_authority(
    adr_paths: Sequence[str],
    index: Mapping[str, str],
    payloads: Mapping[str, bytes],
    terminal_spec_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Classify ADR-0020 only at the exact closed Spec 040 frontier."""

    final_frontier = tuple(row.get("path") for row in terminal_spec_rows) == (
        TERMINAL_SPEC,
        TERMINAL_SUCCESSOR_SPEC,
        TERMINAL_FRONTIER_SPEC,
    )
    if not final_frontier:
        return []
    if (
        adr_paths.count(TERMINAL_PROGRAM_CLOSURE_ADR) != 1
        or TERMINAL_PROGRAM_CLOSURE_ADR not in payloads
    ):
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    payload = payloads[TERMINAL_PROGRAM_CLOSURE_ADR]
    metadata = _frontmatter(
        _decode_text(payload, TERMINAL_PROGRAM_CLOSURE_ADR),
        TERMINAL_PROGRAM_CLOSURE_ADR,
    )
    if {
        "type": metadata.get("type"),
        "status": metadata.get("status"),
        "owner": metadata.get("owner"),
    } != {
        "type": "sdlc/adr",
        "status": "accepted",
        "owner": "platform",
    }:
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    return [
        {
            "path": TERMINAL_PROGRAM_CLOSURE_ADR,
            "profile": "sdlc/adr",
            "status": "accepted",
            "owner": "platform",
            **_object_identity(TERMINAL_PROGRAM_CLOSURE_ADR, index, payload),
            "authorityRole": "terminal-program-closure-decision",
            "frontierSpecPath": TERMINAL_FRONTIER_SPEC,
        }
    ]


def _generic_adr_authority_paths(
    adr_paths: Sequence[str],
    terminal_program_closure_authority: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Keep every accepted ADR generic except exact final ADR-0020 authority."""

    if not terminal_program_closure_authority:
        return list(adr_paths)
    if [row.get("path") for row in terminal_program_closure_authority] != [
        TERMINAL_PROGRAM_CLOSURE_ADR
    ]:
        raise ClosureError(
            "CLOSURE-TERMINAL-AUTHORITY",
            TERMINAL_PROGRAM_CLOSURE_ADR,
        )
    return [path for path in adr_paths if path != TERMINAL_PROGRAM_CLOSURE_ADR]


def build_observed(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, Any]:
    normalized = _normalize_root(root)
    if _git(normalized, ("cat-file", "-t", FIXED_INPUT_COMMIT), runner) != b"commit\n":
        raise ClosureError("CLOSURE-FIXED-COMMIT", ".git")
    registry = _load_registry_authority(normalized, runner)
    source_index = _source_index(normalized, runner)
    sources: dict[str, Any] = {}
    source_rows: list[dict[str, Any]] = []
    for path in SOURCE_PATHS:
        document = _load_json_bytes(
            _proposed_or_index_bytes(normalized, path, source_index, runner), path
        )
        if (
            not isinstance(document, Mapping)
            or document.get("$schema") != SOURCE_SCHEMAS[path]
        ):
            raise ClosureError("CLOSURE-SOURCE-SCHEMA", path)
        sources[path] = document
        source_rows.append(
            {
                "path": path,
                "schema": SOURCE_SCHEMAS[path],
                "objectId": _git_identity(source_index[path]),
            }
        )
    census, eligibility, migration, role_audit = (
        sources[path] for path in SOURCE_PATHS
    )
    if (
        census.get("candidateBaseline", {}).get("candidateCounts", {}).get("total")
        != 110
        or eligibility.get("counts")
        != {"candidates": 110, "eligible": 12, "DEFER": 98, "retain": 2, "residue": 0}
        or migration.get("counts", {}).get("batches") != 6
        or migration.get("counts", {}).get("records") != 12
    ):
        raise ClosureError("CLOSURE-SOURCE-COUNTS")

    inventories = {
        scope: _inventory(normalized, scope, runner) for scope in INVENTORY_ROOTS
    }
    combined_index: dict[str, str] = {}
    inventory_payloads: dict[str, bytes] = {}
    for paths, modes in inventories.values():
        overlap = set(combined_index) & set(modes)
        if overlap:
            raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", next(iter(overlap)))
        combined_index.update(modes)
        for path in paths:
            if path in inventory_payloads:
                raise ClosureError("CLOSURE-INVENTORY-DUPLICATE", path)
            inventory_payloads[path] = _proposed_or_index_bytes(
                normalized, path, modes, runner
            )
    plan_paths = _authored_stage04(inventories[PLAN_ROOT][0], PLAN_ROOT)
    task_paths = _authored_stage04(inventories[TASK_ROOT][0], TASK_ROOT)
    current = _build_current_rows(
        plan_paths,
        task_paths,
        combined_index,
        inventory_payloads,
        eligibility,
    )
    pairs = _build_pairs(current)
    frozen_paths = {row["path"] for row in current}
    spec_paths = [
        path for path in inventories[SPEC_ROOT][0] if path.endswith("/spec.md")
    ]
    terminal = _partition_terminal_controls(
        [path for path in plan_paths if path not in frozen_paths],
        [path for path in task_paths if path not in frozen_paths],
        spec_paths,
        combined_index,
        inventory_payloads,
        registry,
    )
    active_controls = _build_active_control_rows(
        terminal["planPaths"],
        terminal["taskPaths"],
        combined_index,
        inventory_payloads,
    )
    active_control_pairs = _build_active_control_pairs(active_controls)
    archive_paths = {
        path
        for scope in (ARCHIVE_PLAN_ROOT, ARCHIVE_TASK_ROOT)
        for path in inventories[scope][0]
        if path.endswith(".md")
    }
    migrated = _build_migrations(
        eligibility, migration, {row["path"] for row in current}, archive_paths
    )

    adr_paths = [
        path
        for path in inventories[ADR_ROOT][0]
        if path.endswith(".md") and path != f"{ADR_ROOT}/README.md"
    ]
    terminal_program_closure_authority = _terminal_program_closure_authority(
        adr_paths,
        combined_index,
        inventory_payloads,
        terminal["terminalSpecRows"],
    )
    generic_adr_paths = _generic_adr_authority_paths(
        adr_paths,
        terminal_program_closure_authority,
    )
    accepted_adrs = _authority_entries(
        generic_adr_paths, combined_index, inventory_payloads, kind="adr"
    )
    done_specs = _authority_entries(
        terminal["specPaths"], combined_index, inventory_payloads, kind="spec"
    )
    migrated_paths = {row["path"] for row in migrated} | {
        row["archivePath"] for row in migrated
    }
    if migrated_paths & (
        {row["path"] for row in accepted_adrs} | {row["path"] for row in done_specs}
    ):
        raise ClosureError("CLOSURE-AUTHORITY-MOVED")

    role_stage = role_audit.get("stage05", {}).get("finalCounts", {}).get("total")
    role_helpers = role_audit.get("helperTests", {}).get("finalCounts", {}).get("total")
    role_findings = role_audit.get("findings")
    if (
        role_stage != 24
        or role_helpers != 33
        or not isinstance(role_findings, Mapping)
        or any(value for value in role_findings.values())
    ):
        raise ClosureError("CLOSURE-ACER004", SOURCE_PATHS[3])
    dependency = {
        "path": SOURCE_PATHS[3],
        "objectId": _git_identity(source_index[SOURCE_PATHS[3]]),
        "stage05Authored": 24,
        "helperTests": 33,
        "roleAuditFindings": 0,
        "status": "satisfied",
        "requiredForClosure": True,
    }

    pair_counts = Counter(row["state"] for row in pairs)
    disposition_counts = Counter(row["disposition"] for row in current)
    status_dispositions = Counter(
        (row["status"], row["disposition"]) for row in current
    )
    residue_counts = Counter(
        row.get("residueClass") for row in current if row["disposition"] == "DEFER"
    )
    if residue_counts != Counter(
        {
            "deferred-evidence": 88,
            "resolved-partial-evidence": 10,
            "terminal-owned-defer": 2,
        }
    ):
        raise ClosureError("CLOSURE-RESIDUE-CLASS")
    counts = {
        "candidateInput": 110,
        "historicalEligible": len(migrated),
        "historicalDefer": len(
            [
                row
                for row in eligibility["candidateRows"]
                if row.get("disposition") == "DEFER"
            ]
        ),
        "migratedClosed": len(migrated),
        "currentStage04": len(current),
        "currentPlans": len([row for row in current if row["kind"] == "plan"]),
        "currentTasks": len([row for row in current if row["kind"] == "task"]),
        "currentDefer": disposition_counts["DEFER"],
        "currentRetain": disposition_counts["retain"],
        "activeEligible": status_dispositions[("active", "eligible")],
        "pairKeys": len(pairs),
        "completePairs": pair_counts["complete"],
        "planOnly": pair_counts["plan-only"],
        "taskOnly": pair_counts["task-only"],
        "duplicateSameKind": 0,
        "partialOwnedDefer": len(
            [
                row
                for row in pairs
                if row["state"] != "complete" and row["disposition"] == "DEFER"
            ]
        ),
        "acceptedAdrs": len(accepted_adrs),
        "doneSpecs": len(done_specs),
        "migratedAdrOrSpec": 0,
        "stage05Authored": role_stage,
        "helperTests": role_helpers,
        "findings": 0,
    }
    if counts != EXPECTED_COUNTS:
        raise ClosureError("CLOSURE-COUNTS")
    return {
        "sourceLedgers": source_rows,
        "counts": counts,
        "migratedClosed": migrated,
        "currentRows": current,
        "pairCardinality": pairs,
        "activeControlRows": active_controls,
        "activeControlPairCardinality": active_control_pairs,
        "terminalControlRows": terminal["terminalControlRows"],
        "terminalControlPairCardinality": terminal["terminalControlPairCardinality"],
        "terminalSpecRows": terminal["terminalSpecRows"],
        "terminalProgramClosureAuthority": terminal_program_closure_authority,
        "authorityGuards": {
            "acceptedAdrs": accepted_adrs,
            "doneSpecs": done_specs,
        },
        "acer004Dependency": dependency,
    }


def _ledger_from_observed(observed: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "$schema": SCHEMA,
        "schemaVersion": 1,
        "observedAt": "2026-07-19",
        "authority": {
            "fixedInputCommit": _git_identity(FIXED_INPUT_COMMIT),
            "ownerSpec": OWNER_SPEC,
            "owner": "platform",
            "evidenceClass": "repository-static-post-cutover-closure",
        },
        "sourceLedgers": copy.deepcopy(observed["sourceLedgers"]),
        "inventoryBoundary": {
            "gitReference": None,
            "trackedAndProposedNonignored": True,
            "trackedObjectMode": "index-stage-zero",
            "proposedObjectMode": "bounded-no-follow-descriptor",
            "ignoredWorkspaceRead": False,
            "liveRuntimeClaim": False,
            "executionTracker": EXECUTION_TASK,
        },
        "counts": copy.deepcopy(observed["counts"]),
        "migratedClosed": copy.deepcopy(observed["migratedClosed"]),
        "currentRows": copy.deepcopy(observed["currentRows"]),
        "pairCardinality": copy.deepcopy(observed["pairCardinality"]),
        "authorityGuards": copy.deepcopy(observed["authorityGuards"]),
        "acer004Dependency": copy.deepcopy(observed["acer004Dependency"]),
        "linkEvidenceBoundary": {
            "evidenceClass": "repository-static-aggregate",
            "currentLinks": "strict-cross-document-validation",
            "historicalLinks": "archive-and-migration-validation",
            "liveRuntimeClaim": False,
        },
        "findings": {key: [] for key in FINDING_KEYS},
    }


def _ordered_unique_paths(rows: Any, code: str, field: str = "path") -> None:
    if not isinstance(rows, list):
        raise ClosureError(code)
    paths = [row.get(field) if isinstance(row, Mapping) else None for row in rows]
    if any(not is_safe_path(path) for path in paths):
        bad = next((path for path in paths if not is_safe_path(path)), LEDGER_PATH)
        raise ClosureError(f"{code}-PATH", bad)
    if len(paths) != len(set(paths)):
        raise ClosureError(f"{code}-DUPLICATE")
    if paths != sorted(paths):
        raise ClosureError(f"{code}-ORDER")


def validate_ledger(ledger: Any, observed: Mapping[str, Any]) -> None:
    top_keys = {
        "$schema",
        "schemaVersion",
        "observedAt",
        "authority",
        "sourceLedgers",
        "inventoryBoundary",
        "counts",
        "migratedClosed",
        "currentRows",
        "pairCardinality",
        "authorityGuards",
        "acer004Dependency",
        "linkEvidenceBoundary",
        "findings",
    }
    if not isinstance(ledger, Mapping) or set(ledger) != top_keys:
        raise ClosureError("CLOSURE-SCHEMA")
    if (
        ledger.get("$schema") != SCHEMA
        or ledger.get("schemaVersion") != 1
        or ledger.get("observedAt") != "2026-07-19"
    ):
        raise ClosureError("CLOSURE-SCHEMA")
    expected = _ledger_from_observed(observed)
    if ledger.get("authority") != expected["authority"]:
        raise ClosureError("CLOSURE-AUTHORITY")
    if ledger.get("inventoryBoundary") != expected["inventoryBoundary"]:
        raise ClosureError("CLOSURE-BOUNDARY")
    if ledger.get("sourceLedgers") != expected["sourceLedgers"]:
        raise ClosureError("CLOSURE-SOURCE-DRIFT")
    if ledger.get("counts") != EXPECTED_COUNTS:
        raise ClosureError("CLOSURE-COUNTS")

    current = ledger.get("currentRows")
    _ordered_unique_paths(current, "CLOSURE-CURRENT")
    if any(row.get("disposition") == "eligible" for row in current):
        raise ClosureError("CLOSURE-ACTIVE-ELIGIBLE")
    if any(row.get("disposition") != "DEFER" for row in current):
        raise ClosureError("CLOSURE-CURRENT-DISPOSITION")
    for row in current:
        if row.get("sourceDisposition") == "DEFER":
            if (
                not row.get("sourceReason")
                or row.get("sourceOwner") != "platform"
                or not row.get("sourceRefreshTrigger")
                or not row.get("missingAxes")
                or row.get("residueClass")
                not in {"deferred-evidence", "resolved-partial-evidence"}
                or row.get("closureReason") != DEFER_CLOSURE_REASON
                or row.get("postClosureRefreshTrigger") != DEFER_TRIGGER
                or row.get("currentAuthority") != DEFER_AUTHORITY
                or row.get("owner") != "platform"
            ):
                raise ClosureError("CLOSURE-CURRENT-FIELDS", row.get("path"))
        elif row.get("sourceDisposition") == "retain":
            if (
                row.get("status") != "done"
                or row.get("sourceReason") != "active-spec-037-control"
                or row.get("sourceOwner") != "platform"
                or row.get("sourceRefreshTrigger") != "Spec037 closure"
                or row.get("missingAxes") != ["successor-migration-evidence"]
                or row.get("residueClass") != "terminal-owned-defer"
                or row.get("owner") != "platform"
                or row.get("reason") != TERMINAL_CONTROL_REASON
                or row.get("currentEvidenceRole") != TERMINAL_CONTROL_EVIDENCE_ROLE
                or row.get("successorRefreshTrigger")
                != TERMINAL_CONTROL_REFRESH_TRIGGER
                or "currentAuthority" in row
                or "closureTrigger" in row
            ):
                raise ClosureError("CLOSURE-CONTROL-FIELDS", row.get("path"))
        else:
            raise ClosureError("CLOSURE-CURRENT-FIELDS", row.get("path"))
    if current != expected["currentRows"]:
        raise ClosureError("CLOSURE-CURRENT-DRIFT")

    migrated = ledger.get("migratedClosed")
    _ordered_unique_paths(migrated, "CLOSURE-MIGRATION")
    if len(migrated) != 12:
        raise ClosureError("CLOSURE-MIGRATION-STALE")
    if any(row.get("currentSourcePresent") is not False for row in migrated):
        raise ClosureError("CLOSURE-MIGRATION-SOURCE")
    if any(
        row.get("disposition") != "migrated-closed"
        or row.get("historicalDisposition") != "eligible"
        or row.get("archivePresent") is not True
        or row.get("owner") != "platform"
        or not row.get("rollbackParentCommit")
        for row in migrated
    ):
        raise ClosureError("CLOSURE-MIGRATION-EVIDENCE")
    if migrated != expected["migratedClosed"]:
        raise ClosureError("CLOSURE-MIGRATION-DRIFT")

    pairs = ledger.get("pairCardinality")
    if not isinstance(pairs, list):
        raise ClosureError("CLOSURE-PAIR-SCHEMA")
    keys = [row.get("lineageId") if isinstance(row, Mapping) else None for row in pairs]
    if any(not isinstance(key, str) or not key for key in keys):
        raise ClosureError("CLOSURE-PAIR-KEY")
    if len(keys) != len(set(keys)):
        raise ClosureError("CLOSURE-PAIR-DUPLICATE")
    if keys != sorted(keys):
        raise ClosureError("CLOSURE-PAIR-ORDER")
    if any(
        row.get("state") != "complete"
        and (
            row.get("disposition") != "DEFER"
            or row.get("owner") != "platform"
            or row.get("partialEvidence") != "explicit-owned-DEFER"
        )
        for row in pairs
    ):
        raise ClosureError("CLOSURE-PAIR-PARTIAL")
    if pairs != expected["pairCardinality"]:
        raise ClosureError("CLOSURE-PAIR-DRIFT")

    guards = ledger.get("authorityGuards")
    if not isinstance(guards, Mapping) or set(guards) != {"acceptedAdrs", "doneSpecs"}:
        raise ClosureError("CLOSURE-AUTHORITY-SCHEMA")
    for key, authority, status in (
        ("acceptedAdrs", ADR_AUTHORITY, "accepted"),
        ("doneSpecs", SPEC_AUTHORITY, "done"),
    ):
        rows = guards.get(key)
        _ordered_unique_paths(rows, "CLOSURE-AUTHORITY")
        if any(
            row.get("status") != status
            or row.get("owner") != "platform"
            or row.get("disposition") != "retain"
            or row.get("reason") != AUTHORITY_REASON
            or row.get("currentAuthority") != authority
            or not row.get("refreshTrigger")
            for row in rows
        ):
            raise ClosureError("CLOSURE-AUTHORITY-GUARD")
    if guards != expected["authorityGuards"]:
        raise ClosureError("CLOSURE-AUTHORITY-DRIFT")
    if ledger.get("acer004Dependency") != expected["acer004Dependency"]:
        raise ClosureError("CLOSURE-ACER004")
    if ledger.get("linkEvidenceBoundary") != expected["linkEvidenceBoundary"]:
        raise ClosureError("CLOSURE-LINK-BOUNDARY")
    findings = ledger.get("findings")
    if not isinstance(findings, Mapping) or tuple(findings) != FINDING_KEYS:
        raise ClosureError("CLOSURE-FINDINGS")
    if any(not isinstance(value, list) or value for value in findings.values()):
        raise ClosureError("CLOSURE-FINDINGS")


def load_ledger(
    root: str | os.PathLike[str],
    runner: GitRunner = _run_git,
    *,
    control_index: Mapping[str, str] | None = None,
) -> Any:
    normalized = _normalize_root(root)
    index = (
        dict(control_index)
        if control_index is not None
        else _control_inventory(normalized, runner)
    )
    return _load_json_bytes(
        _proposed_or_index_bytes(normalized, LEDGER_PATH, index, runner), LEDGER_PATH
    )


def verify_entrypoints(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, str]:
    normalized = _normalize_root(root)
    index = _control_inventory(normalized, runner)
    script = _decode_text(
        _proposed_or_index_bytes(normalized, SCRIPT_PATH, index, runner), SCRIPT_PATH
    )
    aggregate = _decode_text(
        _proposed_or_index_bytes(normalized, AGGREGATE_PATH, index, runner),
        AGGREGATE_PATH,
    )
    if not script.startswith("#!/usr/bin/env python3\n"):
        raise ClosureError("CLOSURE-ENTRYPOINT", SCRIPT_PATH)
    required = (
        'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" --root "$ROOT_DIR" --self-test',
        'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" --root "$ROOT_DIR"',
    )
    lines = aggregate.splitlines()
    if any(lines.count(command) != 1 for command in required):
        raise ClosureError("CLOSURE-ENTRYPOINT", AGGREGATE_PATH)
    return index


def validate_active_corpus_residue_closure(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, int]:
    control_index = verify_entrypoints(root, runner)
    observed = build_observed(root, runner)
    _validate_terminal_frontier_shape(observed)
    validate_ledger(load_ledger(root, runner, control_index=control_index), observed)
    counts = observed["counts"]
    return {
        "migratedClosed": counts["migratedClosed"],
        "currentRows": counts["currentStage04"],
        "defer": counts["currentDefer"],
        "retain": counts["currentRetain"],
        "pairKeys": counts["pairKeys"],
        "completePairs": counts["completePairs"],
        "planOnly": counts["planOnly"],
        "taskOnly": counts["taskOnly"],
        "acceptedAdrs": counts["acceptedAdrs"],
        "doneSpecs": counts["doneSpecs"],
        "findings": counts["findings"],
        "activeControlRows": len(observed["activeControlRows"]),
        "activeControlPairs": len(observed["activeControlPairCardinality"]),
        "terminalControlRows": len(observed["terminalControlRows"]),
        "terminalControlPairs": len(observed["terminalControlPairCardinality"]),
        "terminalSpecs": len(observed["terminalSpecRows"]),
    }


def _self_test_observed() -> dict[str, Any]:
    current: list[dict[str, Any]] = []
    for index in range(48):
        source_disposition = "retain" if index == 47 else "DEFER"
        for kind, collection in (("plan", "plans"), ("task", "tasks")):
            path = f"docs/04.execution/{collection}/fixture-{index:02d}.md"
            common = {
                "path": path,
                "kind": kind,
                "lineageId": f"fixture-{index:02d}",
                "profile": f"sdlc/{kind}",
                "status": "done",
                "objectMode": "index-stage-zero",
                "objectId": _git_identity("0" * 40),
                "sourceDisposition": source_disposition,
                "sourceReason": "active-spec-037-control"
                if source_disposition == "retain"
                else "missing-evidence",
                "sourceOwner": "platform",
                "sourceRefreshTrigger": "Spec037 closure"
                if source_disposition == "retain"
                else "ACER-005-or-exact-upstream-evidence-change",
                "disposition": "DEFER",
                "owner": "platform",
            }
            if source_disposition == "DEFER":
                common.update(
                    {
                        "missingAxes": ["axis"],
                        "residueClass": "deferred-evidence",
                        "closureReason": DEFER_CLOSURE_REASON,
                        "postClosureRefreshTrigger": DEFER_TRIGGER,
                        "currentAuthority": DEFER_AUTHORITY,
                    }
                )
            else:
                common.update(
                    {
                        "missingAxes": ["successor-migration-evidence"],
                        "residueClass": "terminal-owned-defer",
                        "reason": TERMINAL_CONTROL_REASON,
                        "currentEvidenceRole": TERMINAL_CONTROL_EVIDENCE_ROLE,
                        "successorRefreshTrigger": TERMINAL_CONTROL_REFRESH_TRIGGER,
                    }
                )
            current.append(common)
    for index, kind, collection in (
        (48, "plan", "plans"),
        (49, "task", "tasks"),
        (50, "task", "tasks"),
        (51, "task", "tasks"),
    ):
        current.append(
            {
                "path": f"docs/04.execution/{collection}/fixture-{index:02d}.md",
                "kind": kind,
                "lineageId": f"fixture-{index:02d}",
                "profile": f"sdlc/{kind}",
                "status": "done",
                "objectMode": "index-stage-zero",
                "objectId": _git_identity("0" * 40),
                "sourceDisposition": "DEFER",
                "sourceReason": "missing-evidence",
                "sourceOwner": "platform",
                "sourceRefreshTrigger": "evidence-change",
                "missingAxes": ["axis"],
                "residueClass": "deferred-evidence",
                "disposition": "DEFER",
                "owner": "platform",
                "closureReason": DEFER_CLOSURE_REASON,
                "postClosureRefreshTrigger": DEFER_TRIGGER,
                "currentAuthority": DEFER_AUTHORITY,
            }
        )
    current.sort(key=lambda row: row["path"])
    pairs = _build_pairs(current)
    migrated = [
        {
            "path": f"docs/04.execution/{'plans' if index % 2 == 0 else 'tasks'}/migrated-{index:02d}.md",
            "kind": "plan" if index % 2 == 0 else "task",
            "lineageId": f"migrated-{index // 2:02d}",
            "sourceCommit": _git_identity("1" * 40),
            "sourceBlob": _git_identity("2" * 40),
            "historicalDisposition": "eligible",
            "historicalReason": "complete-evidence",
            "disposition": "migrated-closed",
            "owner": "platform",
            "closureReason": "exact-atomic-migration-result-joined",
            "batchId": f"ACER-003-{index // 2 + 1:03d}",
            "batchSequence": index // 2 + 1,
            "archivePath": f"docs/98.archive/04.execution/{'plans' if index % 2 == 0 else 'tasks'}/migrated-{index:02d}.md",
            "payloadBytes": 1,
            "payloadSha256": _sha256_identity("3" * 64),
            "archiveReason": "completed-lineage",
            "currentClosureOwner": "docs/03.specs/fixture/spec.md",
            "rollbackParentCommit": _git_identity("4" * 40),
            "validationResult": "PASS",
            "currentSourcePresent": False,
            "archivePresent": True,
        }
        for index in range(12)
    ]
    migrated.sort(key=lambda row: row["path"])

    def guards(count: int, kind: str) -> list[dict[str, Any]]:
        status = "accepted" if kind == "adr" else "done"
        authority = ADR_AUTHORITY if kind == "adr" else SPEC_AUTHORITY
        trigger = (
            "accepted-adr-authority-or-evidence-change"
            if kind == "adr"
            else "done-spec-authority-or-evidence-change"
        )
        return [
            {
                "path": f"docs/{'02.architecture/decisions' if kind == 'adr' else '03.specs'}/fixture-{index:02d}{'.md' if kind == 'adr' else '/spec.md'}",
                "profile": f"sdlc/{kind}",
                "status": status,
                "owner": "platform",
                "objectMode": "index-stage-zero",
                "objectId": _git_identity("5" * 40),
                "disposition": "retain",
                "reason": AUTHORITY_REASON,
                "currentAuthority": authority,
                "refreshTrigger": trigger,
            }
            for index in range(count)
        ]

    return {
        "sourceLedgers": [
            {
                "path": path,
                "schema": SOURCE_SCHEMAS[path],
                "objectId": _git_identity("0" * 40),
            }
            for path in SOURCE_PATHS
        ],
        "counts": copy.deepcopy(EXPECTED_COUNTS),
        "migratedClosed": migrated,
        "currentRows": current,
        "pairCardinality": pairs,
        "authorityGuards": {
            "acceptedAdrs": guards(13, "adr"),
            "doneSpecs": guards(29, "spec"),
        },
        "acer004Dependency": {
            "path": SOURCE_PATHS[3],
            "objectId": _git_identity("0" * 40),
            "stage05Authored": 24,
            "helperTests": 33,
            "roleAuditFindings": 0,
            "status": "satisfied",
            "requiredForClosure": True,
        },
    }


def _self_test_terminal_frontier() -> int:
    def payload(profile: str, status: str) -> bytes:
        return (
            "---\n"
            f"type: {profile}\n"
            f"status: {status}\n"
            "owner: platform\n"
            "---\n"
            "# Fixture\n"
        ).encode()

    def registry(
        successor_state: str, frontier_state: str
    ) -> dict[str, Any]:
        return {
            "programLineage": {
                "programs": [
                    {
                        "prd": "006",
                        "ard": "0009",
                        "tranches": [
                            {**TERMINAL_RELATION_IDENTITY, "state": "done"},
                            {
                                **TERMINAL_SUCCESSOR_IDENTITY,
                                "state": successor_state,
                            },
                            {
                                **TERMINAL_FRONTIER_IDENTITY,
                                "state": frontier_state,
                            },
                        ],
                        "followUps": [],
                    }
                ]
            }
        }

    retained_spec = "docs/03.specs/fixture-retained/spec.md"
    payloads = {
        TERMINAL_SPEC: payload("sdlc/spec", "done"),
        TERMINAL_PLAN: payload("sdlc/plan", "done"),
        TERMINAL_TASK: payload("sdlc/task", "done"),
        TERMINAL_SUCCESSOR_SPEC: payload("sdlc/spec", "active"),
        TERMINAL_SUCCESSOR_PLAN: payload("sdlc/plan", "active"),
        TERMINAL_SUCCESSOR_TASK: payload("sdlc/task", "active"),
        TERMINAL_FRONTIER_SPEC: payload("sdlc/spec", "active"),
        retained_spec: payload("sdlc/spec", "done"),
    }
    spec_paths = [
        TERMINAL_SPEC,
        TERMINAL_SUCCESSOR_SPEC,
        TERMINAL_FRONTIER_SPEC,
        retained_spec,
    ]
    cases = 0

    active = _partition_terminal_controls(
        [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN],
        [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK],
        spec_paths,
        {},
        payloads,
        registry("active", "active"),
    )
    if (
        active["specPaths"]
        != [TERMINAL_SUCCESSOR_SPEC, TERMINAL_FRONTIER_SPEC, retained_spec]
        or active["planPaths"] != [TERMINAL_SUCCESSOR_PLAN]
        or active["taskPaths"] != [TERMINAL_SUCCESSOR_TASK]
        or len(active["terminalControlRows"]) != 2
        or [row["path"] for row in active["terminalSpecRows"]]
        != [TERMINAL_SPEC]
    ):
        raise AssertionError("active terminal frontier partition drift")
    cases += 1

    advanced_payloads = dict(payloads)
    advanced_payloads[TERMINAL_SUCCESSOR_SPEC] = payload("sdlc/spec", "done")
    advanced_payloads[TERMINAL_SUCCESSOR_PLAN] = payload("sdlc/plan", "done")
    advanced_payloads[TERMINAL_SUCCESSOR_TASK] = payload("sdlc/task", "done")
    advanced_payloads[TERMINAL_FRONTIER_PLAN] = payload("sdlc/plan", "active")
    advanced_payloads[TERMINAL_FRONTIER_TASK] = payload("sdlc/task", "active")
    advanced = _partition_terminal_controls(
        [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN, TERMINAL_FRONTIER_PLAN],
        [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK, TERMINAL_FRONTIER_TASK],
        spec_paths,
        {},
        advanced_payloads,
        registry("done", "active"),
    )
    if (
        advanced["specPaths"] != [TERMINAL_FRONTIER_SPEC, retained_spec]
        or advanced["planPaths"] != [TERMINAL_FRONTIER_PLAN]
        or advanced["taskPaths"] != [TERMINAL_FRONTIER_TASK]
        or len(advanced["terminalControlRows"]) != 4
        or len(advanced["terminalControlPairCardinality"]) != 2
        or [row["path"] for row in advanced["terminalSpecRows"]]
        != [TERMINAL_SPEC, TERMINAL_SUCCESSOR_SPEC]
    ):
        raise AssertionError("advanced terminal frontier partition drift")
    cases += 1

    final_payloads = dict(advanced_payloads)
    final_payloads[TERMINAL_FRONTIER_SPEC] = payload("sdlc/spec", "done")
    final_payloads[TERMINAL_FRONTIER_PLAN] = payload("sdlc/plan", "done")
    final_payloads[TERMINAL_FRONTIER_TASK] = payload("sdlc/task", "done")
    final = _partition_terminal_controls(
        [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN, TERMINAL_FRONTIER_PLAN],
        [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK, TERMINAL_FRONTIER_TASK],
        spec_paths,
        {},
        final_payloads,
        registry("done", "done"),
    )
    if (
        final["specPaths"] != [retained_spec]
        or final["planPaths"]
        or final["taskPaths"]
        or len(final["terminalControlRows"]) != 6
        or len(final["terminalControlPairCardinality"]) != 3
        or [row["path"] for row in final["terminalSpecRows"]]
        != [TERMINAL_SPEC, TERMINAL_SUCCESSOR_SPEC, TERMINAL_FRONTIER_SPEC]
    ):
        raise AssertionError("final terminal frontier partition drift")
    cases += 1

    blocked_payloads = dict(advanced_payloads)
    blocked_payloads[TERMINAL_FRONTIER_SPEC] = payload("sdlc/spec", "done")
    try:
        _partition_terminal_controls(
            [TERMINAL_PLAN, TERMINAL_SUCCESSOR_PLAN],
            [TERMINAL_TASK, TERMINAL_SUCCESSOR_TASK],
            spec_paths,
            {},
            blocked_payloads,
            registry("done", "done"),
        )
    except ClosureError as exc:
        if (
            exc.code != "CLOSURE-TERMINAL-FRONTIER"
            or exc.path != TERMINAL_FRONTIER_PLAN
        ):
            raise
        cases += 1
    else:
        raise AssertionError("closed terminal frontier was accepted")

    return cases


def run_self_test() -> int:
    observed = _self_test_observed()
    ledger = _ledger_from_observed(observed)
    validate_ledger(ledger, observed)
    cases = 1 + _self_test_terminal_frontier()
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("CLOSURE-SCHEMA", lambda item: item.__setitem__("schemaVersion", 2)),
        ("CLOSURE-SOURCE-DRIFT", lambda item: item["sourceLedgers"].pop()),
        (
            "CLOSURE-COUNTS",
            lambda item: item["counts"].__setitem__("currentStage04", 99),
        ),
        (
            "CLOSURE-CURRENT-DUPLICATE",
            lambda item: item["currentRows"].append(
                copy.deepcopy(item["currentRows"][0])
            ),
        ),
        (
            "CLOSURE-ACTIVE-ELIGIBLE",
            lambda item: item["currentRows"][0].__setitem__("disposition", "eligible"),
        ),
        (
            "CLOSURE-CURRENT-FIELDS",
            lambda item: item["currentRows"][0].__setitem__("closureReason", ""),
        ),
        (
            "CLOSURE-CONTROL-FIELDS",
            lambda item: next(
                row
                for row in item["currentRows"]
                if row["sourceDisposition"] == "retain"
            ).__setitem__("currentEvidenceRole", ""),
        ),
        (
            "CLOSURE-CONTROL-FIELDS",
            lambda item: next(
                row
                for row in item["currentRows"]
                if row["sourceDisposition"] == "retain"
            ).__setitem__("status", "active"),
        ),
        ("CLOSURE-MIGRATION-STALE", lambda item: item["migratedClosed"].pop()),
        (
            "CLOSURE-MIGRATION-SOURCE",
            lambda item: item["migratedClosed"][0].__setitem__(
                "currentSourcePresent", True
            ),
        ),
        (
            "CLOSURE-PAIR-PARTIAL",
            lambda item: next(
                row for row in item["pairCardinality"] if row["state"] != "complete"
            ).__setitem__("disposition", "retain"),
        ),
        (
            "CLOSURE-AUTHORITY-GUARD",
            lambda item: item["authorityGuards"]["acceptedAdrs"][0].__setitem__(
                "disposition", "migrated-closed"
            ),
        ),
        (
            "CLOSURE-ACER004",
            lambda item: item["acer004Dependency"].__setitem__("helperTests", 32),
        ),
        (
            "CLOSURE-FINDINGS",
            lambda item: item["findings"]["unexplainedResidue"].append(
                {"path": "docs/x.md"}
            ),
        ),
    ]
    for expected_code, mutation in mutations:
        candidate = copy.deepcopy(ledger)
        mutation(candidate)
        try:
            validate_ledger(candidate, observed)
        except ClosureError as exc:
            if exc.code != expected_code:
                raise AssertionError(
                    f"unexpected mutation diagnostic: {exc.code}"
                ) from exc
            cases += 1
        else:
            raise AssertionError("closed residue mutation was accepted")
    try:
        _reject_duplicate_pairs([("a", 1), ("a", 2)])
    except ClosureError as exc:
        if exc.code != "CLOSURE-JSON-DUPLICATE":
            raise
        cases += 1
    else:
        raise AssertionError("duplicate JSON key was accepted")
    for path in ("../outside", "/absolute", "_workspace/private"):
        if is_safe_path(path):
            raise AssertionError("unsafe path was accepted")
        cases += 1
    return cases


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        if arguments.self_test:
            cases = run_self_test()
            print(f"PASS active-corpus-residue-closure self-test cases={cases}")
        else:
            counts = validate_active_corpus_residue_closure(arguments.root)
            print(
                "PASS active-corpus-residue-closure "
                f"migrated={counts['migratedClosed']} "
                f"current={counts['currentRows']} "
                f"dispositions={counts['defer']}/{counts['retain']} "
                f"pairs={counts['pairKeys']}:{counts['completePairs']}/{counts['planOnly']}/{counts['taskOnly']} "
                f"active_controls={counts['activeControlRows']}/{counts['activeControlPairs']} "
                f"terminal_controls={counts['terminalControlRows']}/{counts['terminalControlPairs']} "
                f"terminal_specs={counts['terminalSpecs']} "
                f"guards={counts['acceptedAdrs']}/{counts['doneSpecs']} "
                f"findings={counts['findings']}"
            )
        return 0
    except (ClosureError, AssertionError) as exc:
        print(f"ERR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
