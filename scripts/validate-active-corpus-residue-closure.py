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
OWNER_SPEC = "docs/03.specs/037-active-corpus-and-execution-retention/spec.md"
EXECUTION_PLAN = (
    "docs/04.execution/plans/2026-07-18-active-corpus-and-execution-retention.md"
)
EXECUTION_TASK = (
    "docs/04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md"
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
    SPEC_ROOT: frozenset({OWNER_SPEC}),
    PLAN_ROOT: frozenset({EXECUTION_PLAN}),
    TASK_ROOT: frozenset({EXECUTION_TASK}),
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


def _authored_stage04(paths: Sequence[str], scope: str) -> list[str]:
    result = [
        path for path in paths if path.endswith(".md") and path != f"{scope}/README.md"
    ]
    if any(path.count("/") != 3 for path in result):
        bad = next(path for path in result if path.count("/") != 3)
        raise ClosureError("CLOSURE-STAGE04-PATH", bad)
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
    paths = sorted([*plan_paths, *task_paths])
    if set(paths) != set(defer_by_path) | set(control_by_path):
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


def build_observed(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, Any]:
    normalized = _normalize_root(root)
    if _git(normalized, ("cat-file", "-t", FIXED_INPUT_COMMIT), runner) != b"commit\n":
        raise ClosureError("CLOSURE-FIXED-COMMIT", ".git")
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
    spec_paths = [
        path for path in inventories[SPEC_ROOT][0] if path.endswith("/spec.md")
    ]
    accepted_adrs = _authority_entries(
        adr_paths, combined_index, inventory_payloads, kind="adr"
    )
    done_specs = _authority_entries(
        spec_paths, combined_index, inventory_payloads, kind="spec"
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
        "currentPlans": len(plan_paths),
        "currentTasks": len(task_paths),
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


def run_self_test() -> int:
    observed = _self_test_observed()
    ledger = _ledger_from_observed(observed)
    validate_ledger(ledger, observed)
    cases = 1
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
                f"guards={counts['acceptedAdrs']}/{counts['doneSpecs']} "
                f"findings={counts['findings']}"
            )
        return 0
    except (ClosureError, AssertionError) as exc:
        print(f"ERR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
