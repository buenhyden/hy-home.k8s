#!/usr/bin/env python3
"""Validate the ACER-004 Stage 05 and helper Tests role audit."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any


SCHEMA = "active-corpus-role-audit.v1"
INPUT_COMMIT = "2ab01b05f0e3f91368b10cc2c30046050f081a6b"  # pragma: allowlist secret
LEDGER_PATH = "docs/90.references/data/active-corpus-role-audit.json"
SCRIPT_PATH = "scripts/validate-active-corpus-role-audit.py"
AGGREGATE_PATH = "scripts/validate-repo-quality-gates.sh"
OWNER_SPEC = "docs/03.specs/037-active-corpus-and-execution-retention/spec.md"
EXECUTION_TRACKER = (
    "docs/04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md"
)
STAGE05_ROOT = "docs/05.operations"
TESTS_ROOT = "tests"
GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 10
MAX_FILE_BYTES = 2_000_000
SAFE_PATH = re.compile(r"[A-Za-z0-9._@+/-]+\Z")
FULL_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
MODE_RECORD = re.compile(
    rb"(?P<mode>[0-9]{6}) (?P<oid>[0-9a-f]{40}|[0-9a-f]{64}) "
    rb"(?P<stage>[0-3])\t(?P<path>[^\0]+)\Z"
)
FRONTMATTER_LINE = re.compile(r"(?P<key>[A-Za-z][A-Za-z0-9_-]*):[ \t]*(?P<value>[^\r\n]*)\Z")
HEADING = re.compile(r"(?m)^##[ \t]+(.+?)[ \t]*$")
AUTHORING_PROMPT = re.compile(
    r"(?im)<!--\s*(?:describe|replace|summarize|state|list|explain|document)\b"
    r"|^\s*\[(?:describe|replace|insert|authoring prompt|template prompt)\b"
)
UNSUPPORTED_LIVE_CLAIM = re.compile(
    r"(?im)^\s*(?:live|runtime) (?:verification|status):\s*"
    r"(?:pass|ready|healthy|green)\s*$"
    r"|^\s*currently (?:deployed|running|healthy)\b"
)
HELPER_TRACKER_HEADING = re.compile(
    r"(?im)^#{1,6}[ \t]+(?:task(?::[^\r\n]+| table)?|"
    r"execution (?:tracker|status)|progress ledger|current status)\s*$"
)
HELPER_TRACKER_LINE = re.compile(
    r"(?im)^(?:task|work item|execution) status:[ \t]*"
    r"(?:active|in[ -]progress|queued|blocked|done|complete)\s*$"
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

STAGE_KINDS = {
    "guides": {
        "kind": "guide",
        "profile": "sdlc/guide",
        "sections": ["Overview", "Guide Type", "Target Audience", "Prerequisites"],
    },
    "policies": {
        "kind": "policy",
        "profile": "sdlc/policy",
        "sections": ["Overview", "Policy Scope", "Applies To", "Controls"],
    },
    "runbooks": {
        "kind": "runbook",
        "profile": "sdlc/runbook",
        "sections": ["Overview", "Runbook Type", "When to Use", "Procedure or Checklist"],
    },
    "incidents": {
        "kind": "incident",
        "profile": "sdlc/incident",
        "sections": [],
    },
    "postmortems": {
        "kind": "postmortem",
        "profile": "sdlc/postmortem",
        "sections": [],
    },
}
EXPECTED_STAGE_COUNTS = {
    "total": 24,
    "guide": 8,
    "policy": 7,
    "runbook": 9,
    "incident": 0,
    "postmortem": 0,
}
PARENT_HELPER_COUNTS = {"total": 32, "python": 11, "json": 14, "yaml": 6, "readme": 1}
FINAL_HELPER_COUNTS = {"total": 33, "python": 12, "json": 14, "yaml": 6, "readme": 1}
PROPOSAL_PATH = "tests/test_active_corpus_role_audit.py"
README_ADDITIONS = [
    "tests/fixtures/document-contracts/template-source-parity.json",
    "tests/fixtures/document-lifecycle.json",
    "tests/fixtures/gitops-change-set/base/kustomization.yaml",
    "tests/fixtures/gitops-change-set/base/removed-service.yaml",
    "tests/fixtures/gitops-change-set/base/retained-configmap.yaml",
    "tests/fixtures/gitops-change-set/cases.json",
    "tests/fixtures/gitops-change-set/head/added-service.yaml",
    "tests/fixtures/gitops-change-set/head/kustomization.yaml",
    "tests/fixtures/gitops-change-set/head/moved-retained-configmap.yaml",
    PROPOSAL_PATH,
    "tests/test_run_validation_lane.py",
    "tests/test_workspace_boundary.py",
]
README_REMOVALS = [
    "tests/fixtures/document-contracts/semantic-compatibility-debt.json"
]
FINDING_KEYS = {
    "roleOverlap",
    "copiedTemplateResidue",
    "staleCurrentClaim",
    "unownedException",
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


class RoleAuditError(ValueError):
    """Stable, value-free audit diagnostic."""

    def __init__(self, code: str, path: Any = LEDGER_PATH) -> None:
        self.code = code
        self.path = diagnostic_path(path)
        super().__init__(self.code, self.path)

    def __str__(self) -> str:
        return f"{self.code} {self.path}"


GitRunner = Callable[[str, tuple[str, ...]], subprocess.CompletedProcess[bytes]]
TextReader = Callable[[str], str]


def _git_arguments_allowed(arguments: tuple[str, ...]) -> bool:
    if arguments in {
        ("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", STAGE05_ROOT),
        ("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", TESTS_ROOT),
        ("ls-files", "-z", "--stage", "--", STAGE05_ROOT),
        ("ls-files", "-z", "--stage", "--", TESTS_ROOT),
        ("ls-files", "-z", "--stage", "--", LEDGER_PATH, SCRIPT_PATH, AGGREGATE_PATH),
    }:
        return True
    return (
        len(arguments) == 3
        and arguments[:2] in {("cat-file", "-t"), ("cat-file", "-s"), ("cat-file", "blob")}
        and FULL_OID.fullmatch(arguments[2]) is not None
    )


def _run_git(root: str, arguments: tuple[str, ...]) -> subprocess.CompletedProcess[bytes]:
    if not _git_arguments_allowed(arguments):
        raise RoleAuditError("ROLE-AUDIT-GIT-QUERY", ".git")
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
        raise RoleAuditError("ROLE-AUDIT-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise RoleAuditError("ROLE-AUDIT-GIT-STARTUP", ".git") from exc


def _git(root: str, arguments: tuple[str, ...], runner: GitRunner) -> bytes:
    if not _git_arguments_allowed(arguments):
        raise RoleAuditError("ROLE-AUDIT-GIT-QUERY", ".git")
    try:
        result = runner(root, arguments)
    except subprocess.TimeoutExpired as exc:
        raise RoleAuditError("ROLE-AUDIT-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise RoleAuditError("ROLE-AUDIT-GIT-STARTUP", ".git") from exc
    if not isinstance(result, subprocess.CompletedProcess) or result.returncode != 0:
        raise RoleAuditError("ROLE-AUDIT-GIT-RESULT", ".git")
    if not isinstance(result.stdout, bytes):
        raise RoleAuditError("ROLE-AUDIT-GIT-RESULT", ".git")
    return result.stdout


def _parse_nul_paths(payload: bytes, scope: str) -> list[str]:
    if payload and not payload.endswith(b"\0"):
        raise RoleAuditError("ROLE-AUDIT-GIT-MALFORMED", ".git")
    paths: list[str] = []
    for raw in payload[:-1].split(b"\0") if payload else ():
        try:
            path = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise RoleAuditError("ROLE-AUDIT-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path) or not path.startswith(f"{scope}/"):
            raise RoleAuditError("ROLE-AUDIT-INVENTORY-PATH", path)
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise RoleAuditError("ROLE-AUDIT-INVENTORY-DUPLICATE", scope)
    return sorted(paths)


def _parse_modes(
    payload: bytes,
    *,
    scope: str | None = None,
    allowed_paths: set[str] | None = None,
) -> dict[str, str]:
    if payload and not payload.endswith(b"\0"):
        raise RoleAuditError("ROLE-AUDIT-GIT-MALFORMED", ".git")
    modes: dict[str, str] = {}
    for raw in payload[:-1].split(b"\0") if payload else ():
        match = MODE_RECORD.fullmatch(raw)
        if match is None:
            raise RoleAuditError("ROLE-AUDIT-GIT-MALFORMED", ".git")
        try:
            path = match.group("path").decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise RoleAuditError("ROLE-AUDIT-GIT-MALFORMED", ".git") from exc
        if not is_safe_path(path) or (
            scope is not None and not path.startswith(f"{scope}/")
        ) or (allowed_paths is not None and path not in allowed_paths):
            raise RoleAuditError("ROLE-AUDIT-INVENTORY-PATH", path)
        expected_mode = b"100755" if path == AGGREGATE_PATH else b"100644"
        if match.group("mode") != expected_mode or match.group("stage") != b"0":
            raise RoleAuditError("ROLE-AUDIT-INVENTORY-OBJECT", path)
        if path in modes:
            raise RoleAuditError("ROLE-AUDIT-INVENTORY-DUPLICATE", path)
        modes[path] = match.group("oid").decode("ascii")
    return modes


def _normalize_root(root: str | os.PathLike[str]) -> str:
    try:
        value = os.fspath(root)
    except TypeError as exc:
        raise RoleAuditError("ROLE-AUDIT-ROOT", ".") from exc
    if not isinstance(value, str) or not value or "\0" in value:
        raise RoleAuditError("ROLE-AUDIT-ROOT", ".")
    path = os.path.abspath(value)
    if not os.path.isdir(path) or os.path.islink(path):
        raise RoleAuditError("ROLE-AUDIT-ROOT", ".")
    return path


def _read_worktree_bytes(root: str, relative: str) -> bytes:
    if not is_safe_path(relative):
        raise RoleAuditError("ROLE-AUDIT-INVENTORY-PATH", relative)
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
    descriptors: list[int] = []
    try:
        try:
            current = os.open(root, directory_flags)
        except OSError as exc:
            raise RoleAuditError("ROLE-AUDIT-ROOT", ".") from exc
        descriptors.append(current)
        parts = relative.split("/")
        for part in parts[:-1]:
            try:
                current = os.open(part, directory_flags, dir_fd=current)
            except OSError as exc:
                raise RoleAuditError("ROLE-AUDIT-INVENTORY-OBJECT", relative) from exc
            descriptors.append(current)
        try:
            file_descriptor = os.open(parts[-1], file_flags, dir_fd=current)
        except FileNotFoundError as exc:
            raise RoleAuditError("ROLE-AUDIT-INVENTORY-MISSING", relative) from exc
        except OSError as exc:
            raise RoleAuditError("ROLE-AUDIT-INVENTORY-OBJECT", relative) from exc
        descriptors.append(file_descriptor)
        try:
            metadata = os.fstat(file_descriptor)
        except OSError as exc:
            raise RoleAuditError("ROLE-AUDIT-READ", relative) from exc
        if not stat.S_ISREG(metadata.st_mode):
            raise RoleAuditError("ROLE-AUDIT-INVENTORY-OBJECT", relative)
        if metadata.st_size > MAX_FILE_BYTES:
            raise RoleAuditError("ROLE-AUDIT-BOUNDS", relative)
        chunks: list[bytes] = []
        total = 0
        while True:
            try:
                chunk = os.read(file_descriptor, min(65_536, MAX_FILE_BYTES + 1 - total))
            except OSError as exc:
                raise RoleAuditError("ROLE-AUDIT-READ", relative) from exc
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise RoleAuditError("ROLE-AUDIT-BOUNDS", relative)
        return b"".join(chunks)
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _index_blob(root: str, oid: str, path: str, runner: GitRunner) -> bytes:
    if FULL_OID.fullmatch(oid) is None:
        raise RoleAuditError("ROLE-AUDIT-BLOB-ID", path)
    if _git(root, ("cat-file", "-t", oid), runner) != b"blob\n":
        raise RoleAuditError("ROLE-AUDIT-BLOB-TYPE", path)
    size_output = _git(root, ("cat-file", "-s", oid), runner)
    if re.fullmatch(rb"(?:0|[1-9][0-9]*)\n", size_output) is None:
        raise RoleAuditError("ROLE-AUDIT-BLOB-SIZE", path)
    size = int(size_output)
    if size > MAX_FILE_BYTES:
        raise RoleAuditError("ROLE-AUDIT-BOUNDS", path)
    payload = _git(root, ("cat-file", "blob", oid), runner)
    if len(payload) != size:
        raise RoleAuditError("ROLE-AUDIT-BLOB-LENGTH", path)
    return payload


def _authoritative_bytes(
    root: str,
    path: str,
    index: Mapping[str, str],
    runner: GitRunner,
) -> bytes:
    worktree = _read_worktree_bytes(root, path)
    oid = index.get(path)
    if oid is None:
        return worktree
    staged = _index_blob(root, oid, path, runner)
    if worktree != staged:
        raise RoleAuditError("ROLE-AUDIT-WORKTREE-INDEX-DRIFT", path)
    return staged


def _decode_text(payload: bytes, path: str) -> str:
    try:
        return payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RoleAuditError("ROLE-AUDIT-UTF8", path) from exc


def _worktree_text(root: str, path: str) -> str:
    return _decode_text(_read_worktree_bytes(root, path), path)


def _authoritative_text(
    root: str,
    path: str,
    index: Mapping[str, str],
    runner: GitRunner,
) -> str:
    return _decode_text(_authoritative_bytes(root, path, index, runner), path)


def inventory_scope(
    root: str, scope: str, runner: GitRunner = _run_git
) -> tuple[list[str], dict[str, str]]:
    paths = _parse_nul_paths(
        _git(
            root,
            ("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", scope),
            runner,
        ),
        scope,
    )
    modes = _parse_modes(
        _git(root, ("ls-files", "-z", "--stage", "--", scope), runner),
        scope=scope,
    )
    if not set(modes).issubset(paths):
        raise RoleAuditError("ROLE-AUDIT-INVENTORY-DRIFT", scope)
    return paths, modes


def _frontmatter(text: str, path: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise RoleAuditError("ROLE-AUDIT-FRONTMATTER", path)
    end = text.find("\n---\n", 4)
    if end < 0:
        raise RoleAuditError("ROLE-AUDIT-FRONTMATTER", path)
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith((" ", "-")):
            continue
        match = FRONTMATTER_LINE.fullmatch(line)
        if match is None:
            continue
        key = match.group("key")
        if key in result:
            raise RoleAuditError("ROLE-AUDIT-FRONTMATTER", path)
        result[key] = match.group("value").strip().strip("'\"")
    return result


def _stage_kind(path: str) -> Mapping[str, Any]:
    parts = path.split("/")
    if len(parts) != 4 or parts[0:2] != ["docs", "05.operations"]:
        raise RoleAuditError("ROLE-AUDIT-STAGE05-PATH", path)
    collection = parts[2]
    if collection not in STAGE_KINDS:
        raise RoleAuditError("ROLE-AUDIT-STAGE05-PATH", path)
    return STAGE_KINDS[collection]


def _stage_entries(
    paths: Sequence[str], read_text: TextReader
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    entries: list[dict[str, Any]] = []
    counts = {key: 0 for key in EXPECTED_STAGE_COUNTS}
    for path in paths:
        if path.endswith("/README.md"):
            text = read_text(path)
            if AUTHORING_PROMPT.search(text):
                raise RoleAuditError("ROLE-AUDIT-COPIED-RESIDUE", path)
            if UNSUPPORTED_LIVE_CLAIM.search(text):
                raise RoleAuditError("ROLE-AUDIT-STALE-CLAIM", path)
            continue
        if not path.endswith(".md"):
            raise RoleAuditError("ROLE-AUDIT-STAGE05-FORMAT", path)
        contract = _stage_kind(path)
        if contract["kind"] in {"incident", "postmortem"}:
            raise RoleAuditError("ROLE-AUDIT-SYNTHETIC-EVENT", path)
        text = read_text(path)
        metadata = _frontmatter(text, path)
        profile = metadata.get("type")
        if profile != contract["profile"]:
            raise RoleAuditError("ROLE-AUDIT-STAGE05-PROFILE", path)
        if metadata.get("status") != "active":
            raise RoleAuditError("ROLE-AUDIT-STAGE05-STATUS", path)
        if metadata.get("owner") != "platform":
            raise RoleAuditError("ROLE-AUDIT-STAGE05-OWNER", path)
        headings = set(HEADING.findall(text))
        missing = [section for section in contract["sections"] if section not in headings]
        if missing:
            raise RoleAuditError("ROLE-AUDIT-STAGE05-SECTIONS", path)
        if AUTHORING_PROMPT.search(text):
            raise RoleAuditError("ROLE-AUDIT-COPIED-RESIDUE", path)
        if UNSUPPORTED_LIVE_CLAIM.search(text):
            raise RoleAuditError("ROLE-AUDIT-STALE-CLAIM", path)
        kind = str(contract["kind"])
        counts[kind] += 1
        counts["total"] += 1
        entries.append(
            {
                "path": path,
                "kind": kind,
                "profile": profile,
                "status": "active",
                "owner": "platform",
                "role": "authored-operation",
                "requiredSections": list(contract["sections"]),
            }
        )
    return entries, counts


def _helper_format_role(path: str) -> tuple[str, str]:
    if path == "tests/README.md":
        return "readme", "validation-evidence-boundary"
    if path.endswith(".py"):
        return "python", "regression-test"
    if path.endswith(".json"):
        return "json", "closed-fixture"
    if path.endswith((".yaml", ".yml")):
        return "yaml", "manifest-fixture"
    raise RoleAuditError("ROLE-AUDIT-HELPER-FORMAT", path)


def _readme_inventory(text: str) -> list[str]:
    match = re.search(r"(?ms)^## Structure\s*$.*?^```text\s*$\n(?P<body>.*?)^```\s*$", text)
    if match is None:
        raise RoleAuditError("ROLE-AUDIT-README-STRUCTURE", "tests/README.md")
    paths = [line.strip() for line in match.group("body").splitlines() if line.strip()]
    if any(not is_safe_path(path) or not path.startswith("tests/") for path in paths):
        raise RoleAuditError("ROLE-AUDIT-README-PATH", "tests/README.md")
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise RoleAuditError("ROLE-AUDIT-README-ORDER", "tests/README.md")
    return paths


def _reject_helper_tracker_semantics(text: str, path: str = "tests/README.md") -> None:
    if text.startswith("---\n"):
        metadata = _frontmatter(text, path)
        if metadata.get("type") == "sdlc/task" or "status" in metadata:
            raise RoleAuditError("ROLE-AUDIT-HELPER-TRACKER", path)
    if HELPER_TRACKER_HEADING.search(text) or HELPER_TRACKER_LINE.search(text):
        raise RoleAuditError("ROLE-AUDIT-HELPER-TRACKER", path)
    tracker_cells = {"id", "task", "work item", "criterion"}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = {cell.strip().casefold() for cell in stripped[1:-1].split("|")}
        if "status" in cells and cells.intersection(tracker_cells):
            raise RoleAuditError("ROLE-AUDIT-HELPER-TRACKER", path)


def _helper_entries(
    paths: Sequence[str], read_text: TextReader
) -> tuple[list[dict[str, str]], dict[str, int], list[str]]:
    entries: list[dict[str, str]] = []
    counts = {key: 0 for key in FINAL_HELPER_COUNTS}
    readme_text: str | None = None
    for path in paths:
        helper_format, role = _helper_format_role(path)
        text = read_text(path)
        if role == "execution-tracker":
            raise RoleAuditError("ROLE-AUDIT-HELPER-TRACKER", path)
        if path == "tests/README.md":
            readme_text = text
        entries.append({"path": path, "format": helper_format, "role": role})
        counts[helper_format] += 1
        counts["total"] += 1
    if readme_text is None:
        raise RoleAuditError("ROLE-AUDIT-README-STRUCTURE", "tests/README.md")
    _reject_helper_tracker_semantics(readme_text)
    if AUTHORING_PROMPT.search(readme_text):
        raise RoleAuditError("ROLE-AUDIT-COPIED-RESIDUE", "tests/README.md")
    if UNSUPPORTED_LIVE_CLAIM.search(readme_text):
        raise RoleAuditError("ROLE-AUDIT-STALE-CLAIM", "tests/README.md")
    return entries, counts, _readme_inventory(readme_text)


def build_observed(
    root: str | os.PathLike[str],
    runner: GitRunner = _run_git,
    *,
    enforce_index: bool = True,
) -> dict[str, Any]:
    normalized = _normalize_root(root)
    stage_paths, stage_index = inventory_scope(normalized, STAGE05_ROOT, runner)
    helper_paths, helper_index = inventory_scope(normalized, TESTS_ROOT, runner)
    combined_index = {**stage_index, **helper_index}
    if enforce_index:
        read_text = lambda path: _authoritative_text(
            normalized, path, combined_index, runner
        )
    else:
        read_text = lambda path: _worktree_text(normalized, path)
    stage_entries, stage_counts = _stage_entries(stage_paths, read_text)
    helper_entries, helper_counts, readme_paths = _helper_entries(
        helper_paths, read_text
    )
    if stage_counts != EXPECTED_STAGE_COUNTS:
        raise RoleAuditError("ROLE-AUDIT-STAGE05-COUNTS", STAGE05_ROOT)
    if helper_counts != FINAL_HELPER_COUNTS:
        raise RoleAuditError("ROLE-AUDIT-HELPER-COUNTS", TESTS_ROOT)
    if readme_paths != list(helper_paths):
        raise RoleAuditError("ROLE-AUDIT-README-DRIFT", "tests/README.md")
    return {
        "stage05": {"counts": stage_counts, "entries": stage_entries},
        "helperTests": {"counts": helper_counts, "entries": helper_entries},
        "readmeInventory": readme_paths,
    }


def _control_index(root: str, runner: GitRunner) -> dict[str, str]:
    allowed = {LEDGER_PATH, SCRIPT_PATH, AGGREGATE_PATH}
    index = _parse_modes(
        _git(
            root,
            (
                "ls-files",
                "-z",
                "--stage",
                "--",
                LEDGER_PATH,
                SCRIPT_PATH,
                AGGREGATE_PATH,
            ),
            runner,
        ),
        allowed_paths=allowed,
    )
    if set(index) != allowed:
        raise RoleAuditError("ROLE-AUDIT-CONTROL-INVENTORY", ".git")
    return index


def verify_entrypoints(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, str]:
    normalized = _normalize_root(root)
    index = _control_index(normalized, runner)
    script = _authoritative_text(normalized, SCRIPT_PATH, index, runner)
    aggregate = _authoritative_text(normalized, AGGREGATE_PATH, index, runner)
    if not script.startswith("#!/usr/bin/env python3\n"):
        raise RoleAuditError("ROLE-AUDIT-ENTRYPOINT", SCRIPT_PATH)
    required = (
        'python3 "$ROOT_DIR/scripts/validate-active-corpus-role-audit.py" '
        '--root "$ROOT_DIR" --self-test',
        'python3 "$ROOT_DIR/scripts/validate-active-corpus-role-audit.py" '
        '--root "$ROOT_DIR"',
    )
    aggregate_lines = aggregate.splitlines()
    if any(aggregate_lines.count(command) != 1 for command in required):
        raise RoleAuditError("ROLE-AUDIT-ENTRYPOINT", AGGREGATE_PATH)
    return index


def _duplicates(entries: Any, code: str) -> None:
    if not isinstance(entries, list):
        raise RoleAuditError(code)
    paths = [entry.get("path") if isinstance(entry, Mapping) else None for entry in entries]
    if any(not is_safe_path(path) for path in paths):
        bad = next((path for path in paths if not is_safe_path(path)), LEDGER_PATH)
        raise RoleAuditError(f"{code}-PATH", bad)
    if len(paths) != len(set(paths)):
        raise RoleAuditError(f"{code}-DUPLICATE")
    if paths != sorted(paths):
        raise RoleAuditError(f"{code}-ORDER")


def validate_ledger(ledger: Any, observed: Mapping[str, Any]) -> None:
    if not isinstance(ledger, Mapping) or set(ledger) != {
        "$schema",
        "observedAt",
        "authority",
        "inventoryBoundary",
        "stage05",
        "helperTests",
        "readmeRemediation",
        "findings",
    }:
        raise RoleAuditError("ROLE-AUDIT-SCHEMA")
    if ledger.get("$schema") != SCHEMA or ledger.get("observedAt") != "2026-07-19":
        raise RoleAuditError("ROLE-AUDIT-SCHEMA")
    if ledger.get("authority") != {
        "activationCommit": INPUT_COMMIT,
        "ownerSpec": OWNER_SPEC,
        "owner": "platform",
        "evidenceClass": "repository-static-role-audit",
    }:
        raise RoleAuditError("ROLE-AUDIT-AUTHORITY")
    if ledger.get("inventoryBoundary") != {
        "gitReference": None,
        "trackedAndProposed": True,
        "ignoredWorkspaceRead": False,
        "liveRuntimeClaim": False,
        "executionTracker": EXECUTION_TRACKER,
    }:
        raise RoleAuditError("ROLE-AUDIT-BOUNDARY")

    stage = ledger.get("stage05")
    if not isinstance(stage, Mapping) or set(stage) != {"parentCounts", "finalCounts", "entries"}:
        raise RoleAuditError("ROLE-AUDIT-STAGE05-SCHEMA")
    _duplicates(stage.get("entries"), "ROLE-AUDIT-STAGE05")
    if stage.get("parentCounts") != EXPECTED_STAGE_COUNTS or stage.get("finalCounts") != EXPECTED_STAGE_COUNTS:
        raise RoleAuditError("ROLE-AUDIT-STAGE05-COUNTS")
    if stage.get("entries") != observed["stage05"]["entries"]:
        raise RoleAuditError("ROLE-AUDIT-STAGE05-DRIFT")

    helper = ledger.get("helperTests")
    if not isinstance(helper, Mapping) or set(helper) != {
        "parentCounts",
        "proposalDelta",
        "finalCounts",
        "executionTracker",
        "entries",
    }:
        raise RoleAuditError("ROLE-AUDIT-HELPER-SCHEMA")
    _duplicates(helper.get("entries"), "ROLE-AUDIT-HELPER")
    if helper.get("parentCounts") != PARENT_HELPER_COUNTS:
        raise RoleAuditError("ROLE-AUDIT-HELPER-PARENT")
    if helper.get("proposalDelta") != {
        "add": [{"path": PROPOSAL_PATH, "format": "python", "role": "regression-test"}],
        "remove": [],
    }:
        raise RoleAuditError("ROLE-AUDIT-HELPER-PROPOSAL")
    if helper.get("finalCounts") != FINAL_HELPER_COUNTS:
        raise RoleAuditError("ROLE-AUDIT-HELPER-COUNTS")
    if helper.get("executionTracker") is not False:
        raise RoleAuditError("ROLE-AUDIT-HELPER-TRACKER")
    if helper.get("entries") != observed["helperTests"]["entries"]:
        raise RoleAuditError("ROLE-AUDIT-HELPER-DRIFT")

    remediation = ledger.get("readmeRemediation")
    if remediation != {
        "path": "tests/README.md",
        "addedInventoryRows": README_ADDITIONS,
        "removedInventoryRows": README_REMOVALS,
        "finalInventory": observed["readmeInventory"],
    }:
        raise RoleAuditError("ROLE-AUDIT-README-REMEDIATION")

    findings = ledger.get("findings")
    if not isinstance(findings, Mapping) or set(findings) != FINDING_KEYS:
        raise RoleAuditError("ROLE-AUDIT-FINDINGS")
    if any(not isinstance(value, list) or value for value in findings.values()):
        raise RoleAuditError("ROLE-AUDIT-FINDINGS")


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RoleAuditError("ROLE-AUDIT-JSON-DUPLICATE")
        result[key] = value
    return result


def load_ledger(
    root: str | os.PathLike[str],
    runner: GitRunner = _run_git,
    *,
    enforce_index: bool = True,
    control_index: Mapping[str, str] | None = None,
) -> Any:
    normalized = _normalize_root(root)
    if enforce_index:
        index = dict(control_index) if control_index is not None else _control_index(normalized, runner)
        text = _authoritative_text(normalized, LEDGER_PATH, index, runner)
    else:
        text = _worktree_text(normalized, LEDGER_PATH)
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except RoleAuditError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise RoleAuditError("ROLE-AUDIT-JSON") from exc


def validate_active_corpus_role_audit(
    root: str | os.PathLike[str],
    runner: GitRunner = _run_git,
    *,
    enforce_index: bool = True,
    enforce_entrypoints: bool = True,
) -> dict[str, int]:
    normalized = _normalize_root(root)
    control_index = (
        verify_entrypoints(normalized, runner) if enforce_entrypoints else None
    )
    observed = build_observed(normalized, runner, enforce_index=enforce_index)
    validate_ledger(
        load_ledger(
            normalized,
            runner,
            enforce_index=enforce_index,
            control_index=control_index,
        ),
        observed,
    )
    return {
        "stage05": observed["stage05"]["counts"]["total"],
        "guides": observed["stage05"]["counts"]["guide"],
        "policies": observed["stage05"]["counts"]["policy"],
        "runbooks": observed["stage05"]["counts"]["runbook"],
        "incidents": observed["stage05"]["counts"]["incident"],
        "postmortems": observed["stage05"]["counts"]["postmortem"],
        "helpers": observed["helperTests"]["counts"]["total"],
        "python": observed["helperTests"]["counts"]["python"],
        "json": observed["helperTests"]["counts"]["json"],
        "yaml": observed["helperTests"]["counts"]["yaml"],
        "readme": observed["helperTests"]["counts"]["readme"],
        "findings": 0,
    }


def _completed(stdout: bytes) -> subprocess.CompletedProcess[bytes]:
    return subprocess.CompletedProcess([], 0, stdout, b"")


def _fixture_runner(paths: Mapping[str, list[str]]) -> GitRunner:
    def run(_root: str, arguments: tuple[str, ...]) -> subprocess.CompletedProcess[bytes]:
        scope = arguments[-1]
        selected = paths[scope]
        if arguments[1:3] == ("-z", "--stage"):
            payload = b"".join(
                f"100644 {'0' * 40} 0\t{path}\0".encode() for path in selected
            )
        else:
            payload = b"".join(f"{path}\0".encode() for path in selected)
        return _completed(payload)

    return run


def _write_fixture_file(root: Path, path: str, text: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def run_self_test() -> int:
    cases = 0
    with tempfile.TemporaryDirectory(prefix="active-role-audit-") as temporary:
        root = Path(temporary)
        stage_paths: list[str] = []
        for collection, count in (("guides", 8), ("policies", 7), ("runbooks", 9)):
            contract = STAGE_KINDS[collection]
            for index in range(count):
                path = f"docs/05.operations/{collection}/{index + 1:04d}-fixture.md"
                stage_paths.append(path)
                sections = "\n".join(f"## {item}\nFixture." for item in contract["sections"])
                _write_fixture_file(
                    root,
                    path,
                    "---\n"
                    f"type: {contract['profile']}\nstatus: active\nowner: platform\n"
                    "---\n# Fixture\n"
                    f"{sections}\n",
                )
        helper_paths = ["tests/README.md"]
        helper_paths += [f"tests/test_fixture_{index:02d}.py" for index in range(12)]
        helper_paths += [f"tests/fixtures/fixture_{index:02d}.json" for index in range(14)]
        helper_paths += [f"tests/fixtures/fixture_{index:02d}.yaml" for index in range(6)]
        helper_paths.sort()
        for path in helper_paths:
            if path == "tests/README.md":
                continue
            _write_fixture_file(root, path, "{}\n" if path.endswith(".json") else "fixture\n")
        _write_fixture_file(
            root,
            "tests/README.md",
            "# tests\n\n## Structure\n\n```text\n"
            + "\n".join(helper_paths)
            + "\n```\n",
        )
        paths = {STAGE05_ROOT: sorted(stage_paths), TESTS_ROOT: helper_paths}
        observed = build_observed(
            root, _fixture_runner(paths), enforce_index=False
        )
        ledger = {
            "$schema": SCHEMA,
            "observedAt": "2026-07-19",
            "authority": {
                "activationCommit": INPUT_COMMIT,
                "ownerSpec": OWNER_SPEC,
                "owner": "platform",
                "evidenceClass": "repository-static-role-audit",
            },
            "inventoryBoundary": {
                "gitReference": None,
                "trackedAndProposed": True,
                "ignoredWorkspaceRead": False,
                "liveRuntimeClaim": False,
                "executionTracker": EXECUTION_TRACKER,
            },
            "stage05": {
                "parentCounts": EXPECTED_STAGE_COUNTS,
                "finalCounts": EXPECTED_STAGE_COUNTS,
                "entries": observed["stage05"]["entries"],
            },
            "helperTests": {
                "parentCounts": PARENT_HELPER_COUNTS,
                "proposalDelta": {
                    "add": [{"path": PROPOSAL_PATH, "format": "python", "role": "regression-test"}],
                    "remove": [],
                },
                "finalCounts": FINAL_HELPER_COUNTS,
                "executionTracker": False,
                "entries": observed["helperTests"]["entries"],
            },
            "readmeRemediation": {
                "path": "tests/README.md",
                "addedInventoryRows": README_ADDITIONS,
                "removedInventoryRows": README_REMOVALS,
                "finalInventory": observed["readmeInventory"],
            },
            "findings": {key: [] for key in sorted(FINDING_KEYS)},
        }
        validate_ledger(ledger, observed)
        cases += 1

        def add_unique_stage(item: dict[str, Any]) -> None:
            extra = copy.deepcopy(item["stage05"]["entries"][-1])
            extra["path"] = "docs/05.operations/runbooks/9999-extra.md"
            item["stage05"]["entries"].append(extra)

        def add_unique_helper(item: dict[str, Any]) -> None:
            extra = copy.deepcopy(item["helperTests"]["entries"][-1])
            extra["path"] = "tests/zz-extra.py"
            item["helperTests"]["entries"].append(extra)

        mutations: list[Callable[[dict[str, Any]], None]] = [
            lambda item: item["stage05"]["entries"].pop(),
            add_unique_stage,
            lambda item: item["stage05"]["entries"].append(copy.deepcopy(item["stage05"]["entries"][0])),
            lambda item: item["stage05"]["entries"].reverse(),
            lambda item: item["stage05"]["finalCounts"].__setitem__("total", 23),
            lambda item: item["stage05"]["entries"][0].__setitem__("profile", "sdlc/policy"),
            lambda item: item["stage05"]["entries"][0].__setitem__("status", "draft"),
            lambda item: item["stage05"]["entries"][0].__setitem__("owner", "unknown"),
            lambda item: item["stage05"]["entries"][0].__setitem__("role", "execution-tracker"),
            lambda item: item["helperTests"]["entries"].pop(),
            add_unique_helper,
            lambda item: item["helperTests"]["entries"].append(copy.deepcopy(item["helperTests"]["entries"][0])),
            lambda item: item["helperTests"].__setitem__("executionTracker", True),
            lambda item: item["readmeRemediation"]["finalInventory"].pop(),
            lambda item: item["readmeRemediation"]["addedInventoryRows"].pop(),
            lambda item: item["findings"]["roleOverlap"].append({"path": "tests/x.py", "owner": "platform"}),
            lambda item: item["findings"]["unownedException"].append({"path": "tests/x.py", "owner": None}),
            lambda item: item.__setitem__("$schema", "unsupported"),
            lambda item: item["helperTests"]["entries"][0].__setitem__("path", "../outside"),
            lambda item: item["helperTests"]["entries"][0].__setitem__("path", "/absolute"),
            lambda item: item["helperTests"]["entries"][0].__setitem__("path", "_workspace/secret"),
        ]
        for mutation in mutations:
            candidate = copy.deepcopy(ledger)
            mutation(candidate)
            try:
                validate_ledger(candidate, observed)
            except RoleAuditError:
                cases += 1
            else:
                raise AssertionError("closed role-audit mutation was accepted")

        prompt_path = stage_paths[0]
        original = (root / prompt_path).read_text(encoding="utf-8")
        (root / prompt_path).write_text(original + "<!-- describe the result -->\n", encoding="utf-8")
        try:
            build_observed(root, _fixture_runner(paths), enforce_index=False)
        except RoleAuditError as exc:
            if exc.code != "ROLE-AUDIT-COPIED-RESIDUE":
                raise
            cases += 1
        else:
            raise AssertionError("authoring residue was accepted")
        (root / prompt_path).write_text(original + "Runtime status: PASS\n", encoding="utf-8")
        try:
            build_observed(root, _fixture_runner(paths), enforce_index=False)
        except RoleAuditError as exc:
            if exc.code != "ROLE-AUDIT-STALE-CLAIM":
                raise
            cases += 1
        else:
            raise AssertionError("unsupported live claim was accepted")
        (root / prompt_path).write_text(original, encoding="utf-8")

        helper_readme = root / "tests/README.md"
        helper_original = helper_readme.read_text(encoding="utf-8")
        helper_readme.write_text(
            helper_original
            + "\n## Task Table\n\n| ID | Status |\n| --- | --- |\n| X | Done |\n",
            encoding="utf-8",
        )
        try:
            build_observed(root, _fixture_runner(paths), enforce_index=False)
        except RoleAuditError as exc:
            if exc.code != "ROLE-AUDIT-HELPER-TRACKER":
                raise
            cases += 1
        else:
            raise AssertionError("helper execution tracker semantics were accepted")
        helper_readme.write_text(helper_original, encoding="utf-8")

        unsafe_helper = root / helper_paths[-1]
        unsafe_original = unsafe_helper.read_text(encoding="utf-8")
        unsafe_helper.unlink()
        unsafe_helper.symlink_to(root / "outside-helper")
        try:
            build_observed(root, _fixture_runner(paths), enforce_index=False)
        except RoleAuditError as exc:
            if exc.code != "ROLE-AUDIT-INVENTORY-OBJECT":
                raise
            cases += 1
        else:
            raise AssertionError("unsafe helper object was accepted")
        unsafe_helper.unlink()
        unsafe_helper.write_text(unsafe_original, encoding="utf-8")

        incident = "docs/05.operations/incidents/0001-synthetic.md"
        _write_fixture_file(root, incident, "---\ntype: sdlc/incident\nstatus: active\nowner: platform\n---\n")
        event_paths = {**paths, STAGE05_ROOT: sorted([*stage_paths, incident])}
        try:
            build_observed(root, _fixture_runner(event_paths), enforce_index=False)
        except RoleAuditError as exc:
            if exc.code != "ROLE-AUDIT-SYNTHETIC-EVENT":
                raise
            cases += 1
        else:
            raise AssertionError("synthetic event was accepted")

    return cases


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        if arguments.self_test:
            cases = run_self_test()
            print(f"PASS active-corpus-role-audit self-test cases={cases}")
        else:
            counts = validate_active_corpus_role_audit(arguments.root)
            print(
                "PASS active-corpus-role-audit "
                f"stage05={counts['stage05']} "
                f"types={counts['guides']}/{counts['policies']}/{counts['runbooks']}/"
                f"{counts['incidents']}/{counts['postmortems']} "
                f"helpers={counts['helpers']} "
                f"formats={counts['python']}/{counts['json']}/{counts['yaml']}/{counts['readme']} "
                f"findings={counts['findings']}"
            )
        return 0
    except (RoleAuditError, AssertionError) as exc:
        print(f"ERR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
