#!/usr/bin/env python3
"""Validate the immutable ACER-001 current-corpus census snapshot."""

from __future__ import annotations

import argparse
import copy
import json
import os
import posixpath
import re
import stat
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from typing import Any


SCHEMA = "active-corpus-retention-census.v1"
SCHEMA_VERSION = 1
OBSERVED_AT = "2026-07-18"
CANDIDATE_COMMIT = (
    "a12aedfb71ccabd329dabc83bd2863474d1126b0"  # pragma: allowlist secret
)
ACTIVATION_COMMIT = (
    "9e2ec37f483145b322cf68a2f6e697dcf4fb80e1"  # pragma: allowlist secret
)
SNAPSHOT_PATH = "docs/90.references/data/active-corpus-retention-census.json"
LEDGER_PATH = (
    "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md"
)
PLAN_ROOT = "docs/04.execution/plans"
TASK_ROOT = "docs/04.execution/tasks"
STAGE05_ROOT = "docs/05.operations"
TESTS_ROOT = "tests"
HELPER_PROPOSAL_PATH = "tests/test_active_corpus_retention.py"
CONTROL_NAME = "2026-07-18-active-corpus-and-execution-retention.md"
DELTA_NAMES = (
    "2026-07-15-authority-and-lineage-foundation.md",
    "2026-07-16-document-schema-and-lifecycle-contract.md",
    "2026-07-17-archive-record-and-workspace-boundary.md",
)
GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 10
MAX_BLOB_BYTES = 2_000_000
MAX_SNAPSHOT_BYTES = 1_500_000
FULL_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
TREE_HEADER = re.compile(
    rb"(?P<mode>[0-9]{6}) (?P<type>[a-z]+) (?P<object>[0-9a-f]+)\Z"
)
FRONTMATTER_STATUS = re.compile(r"(?m)^status:[ \t]*['\"]?([^'\"\r\n]+)")
MARKDOWN_LINK = re.compile(r"\[[^\]\r\n]*\]\(([^()\s]+)\)")
SAFE_PATH = re.compile(r"[A-Za-z0-9._@+/-]+\Z")
CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_COUNT": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_KEY_0": "core.fsmonitor",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_CONFIG_VALUE_0": "false",
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
LITERAL_GIT_ENVIRONMENT = {
    **CLOSED_GIT_ENVIRONMENT,
    "GIT_LITERAL_PATHSPECS": "1",
}


def _is_safe_repo_path(value: Any) -> bool:
    if not isinstance(value, str) or not SAFE_PATH.fullmatch(value):
        return False
    segments = value.split("/")
    return (
        not value.startswith("/")
        and all(segment not in {"", ".", ".."} for segment in segments)
        and segments[0] != "_workspace"
    )


def _diagnostic_path(value: Any) -> str:
    if isinstance(value, str) and value in {".", ".git"}:
        return value
    if _is_safe_repo_path(value):
        return value
    return SNAPSHOT_PATH


class CensusError(ValueError):
    """Stable payload-free census diagnostic."""

    def __init__(self, code: str, path: Any = SNAPSHOT_PATH) -> None:
        safe_path = _diagnostic_path(path)
        super().__init__(code, safe_path)
        self.code = code
        self.path = safe_path

    def __str__(self) -> str:
        return f"{self.code} {self.path}"


GitRunner = Callable[[str, tuple[str, ...]], subprocess.CompletedProcess[bytes]]


def _git_arguments_allowed(arguments: tuple[str, ...]) -> bool:
    if (
        len(arguments) == 3
        and arguments[:2]
        in {
            ("cat-file", "-t"),
            ("cat-file", "-s"),
            ("cat-file", "blob"),
        }
        and FULL_OID.fullmatch(arguments[2])
    ):
        return True
    if len(arguments) < 7 or arguments[:4] != (
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
    ):
        return False
    commit = arguments[4]
    if arguments[5] != "--" or commit not in {CANDIDATE_COMMIT, ACTIVATION_COMMIT}:
        return False
    paths = arguments[6:]
    allowed = {
        (PLAN_ROOT, TASK_ROOT),
        (LEDGER_PATH,),
        (
            f"{PLAN_ROOT}/{CONTROL_NAME}",
            f"{TASK_ROOT}/{CONTROL_NAME}",
        ),
        (STAGE05_ROOT,),
        (TESTS_ROOT,),
    }
    return paths in allowed


def _normalize_root(root: str | os.PathLike[str]) -> str:
    try:
        value = os.fspath(root)
    except TypeError as exc:
        raise CensusError("CENSUS-ROOT-INVALID", ".") from exc
    if not isinstance(value, str) or not value or "\0" in value:
        raise CensusError("CENSUS-ROOT-INVALID", ".")
    try:
        return os.path.abspath(value)
    except (OSError, ValueError) as exc:
        raise CensusError("CENSUS-ROOT-INVALID", ".") from exc


def _run_git(
    root: str, arguments: tuple[str, ...]
) -> subprocess.CompletedProcess[bytes]:
    if not _git_arguments_allowed(arguments):
        raise CensusError("CENSUS-GIT-QUERY", ".git")
    try:
        return subprocess.run(
            [GIT_EXECUTABLE, *arguments],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=LITERAL_GIT_ENVIRONMENT,
            timeout=GIT_TIMEOUT_SECONDS,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CensusError("CENSUS-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise CensusError("CENSUS-GIT-STARTUP", ".git") from exc


def _git(
    root: str,
    arguments: tuple[str, ...],
    runner: GitRunner,
    *,
    code: str,
    path: str,
) -> bytes:
    completed = runner(root, arguments)
    if not isinstance(completed, subprocess.CompletedProcess):
        raise CensusError("CENSUS-GIT-RESULT", path)
    if completed.returncode != 0 or not isinstance(completed.stdout, bytes):
        raise CensusError(code, path)
    return completed.stdout


def _verify_commit(root: str, commit: str, runner: GitRunner) -> None:
    if not FULL_OID.fullmatch(commit):
        raise CensusError("CENSUS-COMMIT-ID", ".git")
    object_type = _git(
        root,
        ("cat-file", "-t", commit),
        runner,
        code="CENSUS-COMMIT-MISSING",
        path=".git",
    )
    if object_type != b"commit\n":
        raise CensusError("CENSUS-COMMIT-TYPE", ".git")


def _safe_path(raw: bytes) -> str:
    try:
        path = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CensusError("CENSUS-TREE-MALFORMED", ".git") from exc
    if not _is_safe_repo_path(path):
        raise CensusError("CENSUS-TREE-PATH", ".git")
    return path


def _snapshot_row_path(value: Any, code: str) -> str:
    if not _is_safe_repo_path(value):
        raise CensusError(code)
    return value


def _tree(
    root: str,
    commit: str,
    paths: tuple[str, ...],
    runner: GitRunner,
) -> dict[str, str]:
    output = _git(
        root,
        ("ls-tree", "-r", "-z", "--full-tree", commit, "--", *paths),
        runner,
        code="CENSUS-TREE-QUERY",
        path=".git",
    )
    if output and not output.endswith(b"\0"):
        raise CensusError("CENSUS-TREE-MALFORMED", ".git")
    result: dict[str, str] = {}
    for record in output[:-1].split(b"\0") if output else ():
        if record.count(b"\t") != 1:
            raise CensusError("CENSUS-TREE-MALFORMED", ".git")
        header, raw_path = record.split(b"\t", 1)
        match = TREE_HEADER.fullmatch(header)
        if match is None:
            raise CensusError("CENSUS-TREE-MALFORMED", ".git")
        path = _safe_path(raw_path)
        oid = match.group("object").decode("ascii")
        if (
            match.group("mode") != b"100644"
            or match.group("type") != b"blob"
            or not FULL_OID.fullmatch(oid)
        ):
            raise CensusError("CENSUS-TREE-OBJECT", path)
        if path in result:
            raise CensusError("CENSUS-TREE-DUPLICATE", path)
        result[path] = oid
    return result


def _blob(root: str, oid: str, path: str, runner: GitRunner) -> bytes:
    if not FULL_OID.fullmatch(oid):
        raise CensusError("CENSUS-BLOB-ID", path)
    object_type = _git(
        root,
        ("cat-file", "-t", oid),
        runner,
        code="CENSUS-BLOB-MISSING",
        path=path,
    )
    if object_type != b"blob\n":
        raise CensusError("CENSUS-BLOB-TYPE", path)
    size_output = _git(
        root,
        ("cat-file", "-s", oid),
        runner,
        code="CENSUS-BLOB-SIZE",
        path=path,
    )
    if not re.fullmatch(rb"(?:0|[1-9][0-9]*)\n", size_output):
        raise CensusError("CENSUS-BLOB-SIZE", path)
    size = int(size_output)
    if size > MAX_BLOB_BYTES:
        raise CensusError("CENSUS-BLOB-BOUNDS", path)
    payload = _git(
        root,
        ("cat-file", "blob", oid),
        runner,
        code="CENSUS-BLOB-READ",
        path=path,
    )
    if len(payload) != size:
        raise CensusError("CENSUS-BLOB-LENGTH", path)
    return payload


def _text(payload: bytes, path: str) -> str:
    try:
        return payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CensusError("CENSUS-BLOB-UTF8", path) from exc


def _status(text: str, path: str) -> str:
    if not text.startswith("---\n"):
        raise CensusError("CENSUS-STATUS-MISSING", path)
    end = text.find("\n---\n", 4)
    if end < 0:
        raise CensusError("CENSUS-STATUS-MISSING", path)
    matches = FRONTMATTER_STATUS.findall(text[4:end])
    if len(matches) != 1:
        raise CensusError("CENSUS-STATUS-MISSING", path)
    value = matches[0].strip()
    if not re.fullmatch(r"[a-z][a-z-]*", value):
        raise CensusError("CENSUS-STATUS-INVALID", path)
    return value


def _body_spec_links(text: str, path: str) -> list[str]:
    body_start = text.find("\n---\n", 4)
    if body_start < 0:
        raise CensusError("CENSUS-STATUS-MISSING", path)
    links: list[str] = []
    for raw_target in MARKDOWN_LINK.findall(text[body_start + 5 :]):
        target = raw_target.split("#", 1)[0]
        if not target or ":" in target or target.startswith("/"):
            continue
        normalized = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
        if re.fullmatch(r"docs/03\.specs/[A-Za-z0-9._@+/-]+/spec\.md", normalized):
            links.append(normalized)
    return links


def _ledger_paths(text: str) -> set[str]:
    paths: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^\| `([^`]+)` \|", line)
        if match is not None:
            path = match.group(1)
            if path in paths:
                raise CensusError("CENSUS-LEDGER-DUPLICATE", LEDGER_PATH)
            paths.add(path)
    return paths


def _pending_eligibility_evidence() -> dict[str, dict[str, Any]]:
    return {
        "upstreamSpec": {
            "state": "unknown",
            "value": None,
            "refreshTrigger": "ACER-002",
        },
        "program": {
            "state": "unknown",
            "value": None,
            "refreshTrigger": "ACER-002",
        },
        "currentOwner": {
            "state": "unknown",
            "value": None,
            "refreshTrigger": "ACER-002",
        },
        "reciprocalLinks": {
            "state": "pending",
            "paths": [],
            "refreshTrigger": "ACER-002",
        },
        "closure": {
            "state": "unknown",
            "references": [],
            "refreshTrigger": "ACER-002",
        },
    }


def _candidate_entries(
    root: str,
    tree: Mapping[str, str],
    ledger_paths: set[str],
    runner: GitRunner,
) -> list[dict[str, Any]]:
    paths = sorted(
        path
        for path in tree
        if path.endswith(".md") and not path.endswith("/README.md")
    )
    by_key: dict[str, set[str]] = {}
    for path in paths:
        kind = "plan" if path.startswith(f"{PLAN_ROOT}/") else "task"
        key = posixpath.basename(path)[:-3]
        by_key.setdefault(key, set()).add(kind)
    entries: list[dict[str, Any]] = []
    for path in paths:
        kind = "plan" if path.startswith(f"{PLAN_ROOT}/") else "task"
        key = posixpath.basename(path)[:-3]
        kinds = by_key[key]
        pair_state = "paired" if kinds == {"plan", "task"} else f"{kind}-only"
        payload = _text(_blob(root, tree[path], path, runner), path)
        links = _body_spec_links(payload, path)
        segment = "delta" if f"{key}.md" in DELTA_NAMES else "frozen"
        entries.append(
            {
                "path": path,
                "kind": kind,
                "status": _status(payload, path),
                "sourceBlob": tree[path],
                "baselineSegment": segment,
                "pairKey": key,
                "pairState": pair_state,
                "ledgerRowPresent": path in ledger_paths,
                "bodySpecLinkCount": len(links),
                "bodySpecLinks": links,
                "eligibilityEvidence": _pending_eligibility_evidence(),
                "disposition": "DEFER",
                "reason": "eligibility-evidence-pending",
                "owner": "platform",
                "refreshTrigger": "ACER-002",
            }
        )
    return entries


def _operation_entries(
    root: str, tree: Mapping[str, str], runner: GitRunner
) -> list[dict[str, Any]]:
    routes = {
        "guides": "guide",
        "policies": "policy",
        "runbooks": "runbook",
        "incidents": "incident",
        "postmortems": "postmortem",
    }
    entries: list[dict[str, Any]] = []
    for path in sorted(tree):
        if not path.endswith(".md") or path.endswith("/README.md"):
            continue
        collection = path.split("/", 3)[2]
        if collection not in routes:
            raise CensusError("CENSUS-STAGE05-ROUTE", path)
        payload = _text(_blob(root, tree[path], path, runner), path)
        entries.append(
            {
                "path": path,
                "kind": routes[collection],
                "status": _status(payload, path),
                "sourceBlob": tree[path],
                "auditState": "pending",
                "auditOwner": "platform",
                "refreshTrigger": "ACER-004",
            }
        )
    return entries


def _helper_entries(tree: Mapping[str, str]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for path in sorted(tree):
        if path.endswith(".py"):
            kind = "python"
        elif path.endswith(".json"):
            kind = "json"
        elif path.endswith((".yaml", ".yml")):
            kind = "yaml"
        elif path == "tests/README.md":
            kind = "readme"
        else:
            raise CensusError("CENSUS-HELPER-ROUTE", path)
        entries.append({"path": path, "kind": kind, "sourceBlob": tree[path]})
    return entries


def _methodology_sources() -> list[dict[str, str]]:
    return [
        {
            "authority": "Kubernetes SIG Architecture",
            "title": "Kubernetes Enhancement Proposals README",
            "url": "https://github.com/kubernetes/enhancements/blob/master/keps/README.md",
            "observedAt": OBSERVED_AT,
            "use": "lifecycle-state-and-ownership-method",
        },
        {
            "authority": "U.S. National Archives and Records Administration",
            "title": "Guidance on Managing Web Records",
            "url": "https://www.archives.gov/records-mgmt/policy/managing-web-records-index.html",
            "observedAt": OBSERVED_AT,
            "use": "records-disposition-and-retention-method",
        },
        {
            "authority": "Git",
            "title": "git-reflog",
            "url": "https://git-scm.com/docs/git-reflog",
            "observedAt": OBSERVED_AT,
            "use": "local-reference-recovery-boundary",
        },
        {
            "authority": "Git",
            "title": "git-gc",
            "url": "https://git-scm.com/docs/git-gc",
            "observedAt": OBSERVED_AT,
            "use": "object-retention-boundary",
        },
    ]


def build_expected_snapshot(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, Any]:
    repository = _normalize_root(root)
    _verify_commit(repository, CANDIDATE_COMMIT, runner)
    _verify_commit(repository, ACTIVATION_COMMIT, runner)

    candidate_tree = _tree(repository, CANDIDATE_COMMIT, (PLAN_ROOT, TASK_ROOT), runner)
    ledger_tree = _tree(repository, ACTIVATION_COMMIT, (LEDGER_PATH,), runner)
    if set(ledger_tree) != {LEDGER_PATH}:
        raise CensusError("CENSUS-LEDGER-MISSING", LEDGER_PATH)
    ledger = _text(
        _blob(repository, ledger_tree[LEDGER_PATH], LEDGER_PATH, runner), LEDGER_PATH
    )
    candidates = _candidate_entries(
        repository, candidate_tree, _ledger_paths(ledger), runner
    )

    control_paths = (
        f"{PLAN_ROOT}/{CONTROL_NAME}",
        f"{TASK_ROOT}/{CONTROL_NAME}",
    )
    control_tree = _tree(repository, ACTIVATION_COMMIT, control_paths, runner)
    controls: list[dict[str, Any]] = []
    for path in control_paths:
        if path not in control_tree:
            raise CensusError("CENSUS-CONTROL-MISSING", path)
        payload = _text(_blob(repository, control_tree[path], path, runner), path)
        kind = "plan" if path.startswith(f"{PLAN_ROOT}/") else "task"
        controls.append(
            {
                "path": path,
                "kind": kind,
                "status": _status(payload, path),
                "sourceBlob": control_tree[path],
                "pairKey": CONTROL_NAME[:-3],
                "pairState": "paired",
                "disposition": "retain",
                "reason": "active-execution-control",
                "owner": "platform",
                "refreshTrigger": "Spec037 closure",
                "candidateEligible": False,
            }
        )

    operation_tree = _tree(repository, ACTIVATION_COMMIT, (STAGE05_ROOT,), runner)
    operations = _operation_entries(repository, operation_tree, runner)
    helper_tree = _tree(repository, ACTIVATION_COMMIT, (TESTS_ROOT,), runner)
    helpers = _helper_entries(helper_tree)

    delta_paths = sorted(
        f"{root}/{name}" for name in DELTA_NAMES for root in (PLAN_ROOT, TASK_ROOT)
    )
    candidate_counts = {
        "plan": sum(row["kind"] == "plan" for row in candidates),
        "task": sum(row["kind"] == "task" for row in candidates),
        "total": len(candidates),
    }
    frozen_counts = {
        "plan": sum(
            row["kind"] == "plan" and row["baselineSegment"] == "frozen"
            for row in candidates
        ),
        "task": sum(
            row["kind"] == "task" and row["baselineSegment"] == "frozen"
            for row in candidates
        ),
        "total": sum(row["baselineSegment"] == "frozen" for row in candidates),
    }
    delta_counts = {
        "plan": sum(
            row["kind"] == "plan" and row["baselineSegment"] == "delta"
            for row in candidates
        ),
        "task": sum(
            row["kind"] == "task" and row["baselineSegment"] == "delta"
            for row in candidates
        ),
        "total": sum(row["baselineSegment"] == "delta" for row in candidates),
    }
    keys: dict[str, str] = {}
    for row in candidates:
        keys[row["pairKey"]] = row["pairState"]
    pair_counts = {
        "paired": sum(value == "paired" for value in keys.values()),
        "plan-only": sum(value == "plan-only" for value in keys.values()),
        "task-only": sum(value == "task-only" for value in keys.values()),
    }
    operation_counts = {
        "guide": sum(row["kind"] == "guide" for row in operations),
        "policy": sum(row["kind"] == "policy" for row in operations),
        "runbook": sum(row["kind"] == "runbook" for row in operations),
        "incident": sum(row["kind"] == "incident" for row in operations),
        "postmortem": sum(row["kind"] == "postmortem" for row in operations),
        "total": len(operations),
    }
    helper_counts = {
        "python": sum(row["kind"] == "python" for row in helpers),
        "json": sum(row["kind"] == "json" for row in helpers),
        "yaml": sum(row["kind"] == "yaml" for row in helpers),
        "readme": sum(row["kind"] == "readme" for row in helpers),
        "total": len(helpers),
    }
    helper_delta_counts = {
        "python": 1,
        "json": 0,
        "yaml": 0,
        "readme": 0,
        "total": 1,
    }
    helper_proposed_counts = {
        key: helper_counts[key] + helper_delta_counts[key]
        for key in ("python", "json", "yaml", "readme", "total")
    }
    return {
        "$schema": SCHEMA,
        "schemaVersion": SCHEMA_VERSION,
        "observedAt": OBSERVED_AT,
        "candidateBaseline": {
            "candidateBaselineCommit": CANDIDATE_COMMIT,
            "frozenCounts": frozen_counts,
            "deltaCounts": delta_counts,
            "candidateCounts": candidate_counts,
            "pairCounts": pair_counts,
            "deltaPaths": delta_paths,
            "entries": candidates,
        },
        "activation": {
            "activationCommit": ACTIVATION_COMMIT,
            "proposedCounts": {"plan": 55, "task": 57, "total": 112},
            "activeControls": controls,
            "stage05": {"counts": operation_counts, "entries": operations},
            "helperTests": {
                "observationBoundary": {
                    "kind": "pinned-activation-input",
                    "source": "activation.activationCommit",
                    "worktreeInference": False,
                },
                "counts": helper_counts,
                "proposalDelta": {
                    "counts": helper_delta_counts,
                    "entries": [{"path": HELPER_PROPOSAL_PATH, "kind": "python"}],
                },
                "proposedCounts": helper_proposed_counts,
                "role": "support-only",
                "executionTracker": False,
                "auditState": "pending",
                "auditOwner": "platform",
                "refreshTrigger": "ACER-004",
                "entries": helpers,
            },
        },
        "methodologySources": _methodology_sources(),
    }


def _keys(value: Mapping[str, Any], expected: set[str], code: str) -> None:
    if set(value) != expected:
        raise CensusError(code)


def _mapping(value: Any, code: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CensusError(code)
    return value


def _sequence(value: Any, code: str) -> list[Any]:
    if not isinstance(value, list):
        raise CensusError(code)
    return value


def _preflight(snapshot: Any) -> Mapping[str, Any]:
    top = _mapping(snapshot, "CENSUS-SCHEMA")
    _keys(
        top,
        {
            "$schema",
            "schemaVersion",
            "observedAt",
            "candidateBaseline",
            "activation",
            "methodologySources",
        },
        "CENSUS-SCHEMA",
    )
    if (
        top["$schema"] != SCHEMA
        or type(top["schemaVersion"]) is not int
        or top["schemaVersion"] != SCHEMA_VERSION
        or top["observedAt"] != OBSERVED_AT
    ):
        raise CensusError("CENSUS-SCHEMA")
    baseline = _mapping(top["candidateBaseline"], "CENSUS-BASELINE-SCHEMA")
    _keys(
        baseline,
        {
            "candidateBaselineCommit",
            "frozenCounts",
            "deltaCounts",
            "candidateCounts",
            "pairCounts",
            "deltaPaths",
            "entries",
        },
        "CENSUS-BASELINE-SCHEMA",
    )
    if baseline["candidateBaselineCommit"] != CANDIDATE_COMMIT:
        raise CensusError("CENSUS-BASELINE-COMMIT")
    for count_key in ("frozenCounts", "deltaCounts", "candidateCounts"):
        counts = _mapping(baseline[count_key], "CENSUS-COUNT-SCHEMA")
        _keys(counts, {"plan", "task", "total"}, "CENSUS-COUNT-SCHEMA")
        if any(type(value) is not int for value in counts.values()):
            raise CensusError("CENSUS-COUNT-SCHEMA")
    pair_counts = _mapping(baseline["pairCounts"], "CENSUS-PAIR-COUNT-SCHEMA")
    _keys(
        pair_counts,
        {"paired", "plan-only", "task-only"},
        "CENSUS-PAIR-COUNT-SCHEMA",
    )
    if any(type(value) is not int for value in pair_counts.values()):
        raise CensusError("CENSUS-PAIR-COUNT-SCHEMA")
    entries = _sequence(baseline["entries"], "CENSUS-CANDIDATES")
    paths: set[str] = set()
    candidate_keys = {
        "path",
        "kind",
        "status",
        "sourceBlob",
        "baselineSegment",
        "pairKey",
        "pairState",
        "ledgerRowPresent",
        "bodySpecLinkCount",
        "bodySpecLinks",
        "eligibilityEvidence",
        "disposition",
        "reason",
        "owner",
        "refreshTrigger",
    }
    for row_value in entries:
        row = _mapping(row_value, "CENSUS-CANDIDATE-SCHEMA")
        _keys(row, candidate_keys, "CENSUS-CANDIDATE-SCHEMA")
        path = _snapshot_row_path(row.get("path"), "CENSUS-CANDIDATE-PATH")
        if path in paths:
            raise CensusError("CENSUS-CANDIDATE-DUPLICATE")
        paths.add(path)
        if row.get("disposition") != "DEFER":
            raise CensusError("CENSUS-PREMATURE-ELIGIBLE", path)
        if (
            row.get("reason") != "eligibility-evidence-pending"
            or row.get("owner") != "platform"
            or row.get("refreshTrigger") != "ACER-002"
        ):
            raise CensusError("CENSUS-DEFER-EVIDENCE", path)
        links = row.get("bodySpecLinks")
        if not isinstance(links, list) or row.get("bodySpecLinkCount") != len(links):
            raise CensusError("CENSUS-SPEC-LINK-EVIDENCE", path)
        if row.get("eligibilityEvidence") != _pending_eligibility_evidence():
            raise CensusError("CENSUS-ELIGIBILITY-EVIDENCE", path)
    activation = _mapping(top["activation"], "CENSUS-ACTIVATION-SCHEMA")
    _keys(
        activation,
        {
            "activationCommit",
            "proposedCounts",
            "activeControls",
            "stage05",
            "helperTests",
        },
        "CENSUS-ACTIVATION-SCHEMA",
    )
    if activation["activationCommit"] != ACTIVATION_COMMIT:
        raise CensusError("CENSUS-ACTIVATION-COMMIT")
    proposed = _mapping(activation["proposedCounts"], "CENSUS-COUNT-SCHEMA")
    _keys(proposed, {"plan", "task", "total"}, "CENSUS-COUNT-SCHEMA")
    controls = _sequence(activation["activeControls"], "CENSUS-CONTROLS")
    control_keys = {
        "path",
        "kind",
        "status",
        "sourceBlob",
        "pairKey",
        "pairState",
        "disposition",
        "reason",
        "owner",
        "refreshTrigger",
        "candidateEligible",
    }
    for row_value in controls:
        row = _mapping(row_value, "CENSUS-CONTROL-SCHEMA")
        _keys(row, control_keys, "CENSUS-CONTROL-SCHEMA")
        _snapshot_row_path(row.get("path"), "CENSUS-CONTROL-PATH")
        if (
            row.get("disposition") != "retain"
            or row.get("reason") != "active-execution-control"
            or row.get("refreshTrigger") != "Spec037 closure"
            or row.get("candidateEligible") is not False
        ):
            raise CensusError("CENSUS-CONTROL-DISPOSITION")
    stage05 = _mapping(activation["stage05"], "CENSUS-STAGE05-SCHEMA")
    _keys(stage05, {"counts", "entries"}, "CENSUS-STAGE05-SCHEMA")
    operation_counts = _mapping(stage05["counts"], "CENSUS-STAGE05-COUNT-SCHEMA")
    _keys(
        operation_counts,
        {"guide", "policy", "runbook", "incident", "postmortem", "total"},
        "CENSUS-STAGE05-COUNT-SCHEMA",
    )
    operation_keys = {
        "path",
        "kind",
        "status",
        "sourceBlob",
        "auditState",
        "auditOwner",
        "refreshTrigger",
    }
    for row_value in _sequence(stage05["entries"], "CENSUS-STAGE05"):
        row = _mapping(row_value, "CENSUS-STAGE05-ROW")
        _keys(row, operation_keys, "CENSUS-STAGE05-ROW")  # gitleaks:allow
        path = _snapshot_row_path(row.get("path"), "CENSUS-STAGE05-PATH")
        if row.get("kind") in {"incident", "postmortem"}:
            raise CensusError("CENSUS-FAKE-EVENT", path)
        if (
            row.get("auditState") != "pending"
            or row.get("auditOwner") != "platform"
            or row.get("refreshTrigger") != "ACER-004"
        ):
            raise CensusError("CENSUS-STAGE05-AUDIT")
    helpers = _mapping(activation["helperTests"], "CENSUS-HELPER-SCHEMA")
    _keys(
        helpers,
        {
            "observationBoundary",
            "counts",
            "proposalDelta",
            "proposedCounts",
            "role",
            "executionTracker",
            "auditState",
            "auditOwner",
            "refreshTrigger",
            "entries",
        },
        "CENSUS-HELPER-SCHEMA",
    )
    boundary = _mapping(helpers["observationBoundary"], "CENSUS-HELPER-BOUNDARY-SCHEMA")
    _keys(
        boundary,
        {"kind", "source", "worktreeInference"},
        "CENSUS-HELPER-BOUNDARY-SCHEMA",
    )
    if boundary != {
        "kind": "pinned-activation-input",
        "source": "activation.activationCommit",
        "worktreeInference": False,
    }:
        raise CensusError("CENSUS-HELPER-BOUNDARY")
    helper_counts = _mapping(helpers["counts"], "CENSUS-HELPER-COUNT-SCHEMA")
    _keys(
        helper_counts,
        {"python", "json", "yaml", "readme", "total"},
        "CENSUS-HELPER-COUNT-SCHEMA",
    )
    helper_proposed_counts = _mapping(
        helpers["proposedCounts"], "CENSUS-HELPER-PROPOSED-COUNT-SCHEMA"
    )
    _keys(
        helper_proposed_counts,
        {"python", "json", "yaml", "readme", "total"},
        "CENSUS-HELPER-PROPOSED-COUNT-SCHEMA",
    )
    delta = _mapping(helpers["proposalDelta"], "CENSUS-HELPER-DELTA-SCHEMA")
    _keys(delta, {"counts", "entries"}, "CENSUS-HELPER-DELTA-SCHEMA")
    delta_counts = _mapping(delta["counts"], "CENSUS-HELPER-DELTA-COUNT-SCHEMA")
    _keys(
        delta_counts,
        {"python", "json", "yaml", "readme", "total"},
        "CENSUS-HELPER-DELTA-COUNT-SCHEMA",
    )
    delta_entries = _sequence(delta["entries"], "CENSUS-HELPER-DELTA")
    for row_value in delta_entries:
        row = _mapping(row_value, "CENSUS-HELPER-DELTA-ROW")
        _keys(row, {"path", "kind"}, "CENSUS-HELPER-DELTA-ROW")
        _snapshot_row_path(row.get("path"), "CENSUS-HELPER-DELTA-PATH")
    if delta_entries != [{"path": HELPER_PROPOSAL_PATH, "kind": "python"}]:
        raise CensusError("CENSUS-HELPER-DELTA")
    if (
        helpers["role"] != "support-only"
        or helpers["executionTracker"] is not False
        or helpers["auditState"] != "pending"
        or helpers["auditOwner"] != "platform"
        or helpers["refreshTrigger"] != "ACER-004"
    ):
        raise CensusError("CENSUS-HELPER-ROLE")
    helper_keys = {"path", "kind", "sourceBlob"}
    for row_value in _sequence(helpers["entries"], "CENSUS-HELPERS"):
        row = _mapping(row_value, "CENSUS-HELPER-ROW")
        _keys(row, helper_keys, "CENSUS-HELPER-ROW")
        _snapshot_row_path(row.get("path"), "CENSUS-HELPER-PATH")
    sources = _sequence(top["methodologySources"], "CENSUS-SOURCES")
    source_keys = {"authority", "title", "url", "observedAt", "use"}
    for row_value in sources:
        row = _mapping(row_value, "CENSUS-SOURCE-ROW")
        _keys(row, source_keys, "CENSUS-SOURCE-ROW")
        if row.get("observedAt") != OBSERVED_AT:
            raise CensusError("CENSUS-SOURCE-FRESHNESS")
    return top


def validate_snapshot(snapshot: Any, expected: Mapping[str, Any]) -> None:
    actual = _preflight(snapshot)
    if actual.get("candidateBaseline") != expected.get("candidateBaseline"):
        raise CensusError("CENSUS-CANDIDATE-DRIFT")
    if actual.get("activation") != expected.get("activation"):
        raise CensusError("CENSUS-ACTIVATION-DRIFT")
    if actual.get("methodologySources") != expected.get("methodologySources"):
        raise CensusError("CENSUS-SOURCE-DRIFT")


def _duplicate_key(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CensusError("CENSUS-JSON-DUPLICATE")
        result[key] = value
    return result


def load_snapshot(root: str | os.PathLike[str]) -> Any:
    repository = _normalize_root(root)
    path = os.path.join(repository, SNAPSHOT_PATH)
    try:
        metadata = os.lstat(path)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise CensusError("CENSUS-SNAPSHOT-TYPE")
        if metadata.st_size > MAX_SNAPSHOT_BYTES:
            raise CensusError("CENSUS-SNAPSHOT-BOUNDS")
        with open(path, "r", encoding="utf-8", newline="") as handle:
            return json.load(handle, object_pairs_hook=_duplicate_key)
    except CensusError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CensusError("CENSUS-SNAPSHOT-READ") from exc


def validate_active_corpus_retention(
    root: str | os.PathLike[str], runner: GitRunner = _run_git
) -> dict[str, int]:
    snapshot = load_snapshot(root)
    expected = build_expected_snapshot(root, runner)
    validate_snapshot(snapshot, expected)
    baseline = snapshot["candidateBaseline"]
    activation = snapshot["activation"]
    return {
        "candidates": baseline["candidateCounts"]["total"],
        "controls": len(activation["activeControls"]),
        "stage05": activation["stage05"]["counts"]["total"],
        "helpersInput": activation["helperTests"]["counts"]["total"],
        "helpersProposed": activation["helperTests"]["proposedCounts"]["total"],
    }


def _run_self_test(root: str | os.PathLike[str]) -> int:
    expected = build_expected_snapshot(root)
    validate_snapshot(copy.deepcopy(expected), expected)
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("missing candidate", lambda x: x["candidateBaseline"]["entries"].pop()),
        (
            "extra candidate",
            lambda x: x["candidateBaseline"]["entries"].append(
                copy.deepcopy(x["candidateBaseline"]["entries"][0])
            ),
        ),
        (
            "duplicate candidate",
            lambda x: x["candidateBaseline"]["entries"].__setitem__(
                1, copy.deepcopy(x["candidateBaseline"]["entries"][0])
            ),
        ),
        (
            "wrong candidate count",
            lambda x: x["candidateBaseline"]["candidateCounts"].__setitem__(
                "total", 109
            ),
        ),
        ("wrong delta", lambda x: x["candidateBaseline"]["deltaPaths"].pop()),
        ("wrong control", lambda x: x["activation"]["activeControls"].pop()),
        (
            "premature eligible",
            lambda x: x["candidateBaseline"]["entries"][0].__setitem__(
                "disposition", "eligible"
            ),
        ),
        (
            "missing defer evidence",
            lambda x: x["candidateBaseline"]["entries"][0].__setitem__("reason", ""),
        ),
        (
            "unsafe candidate path",
            lambda x: x["candidateBaseline"]["entries"][0].__setitem__(
                "path", "../injected\nFORGED PASS"
            ),
        ),
        (
            "premature eligibility evidence",
            lambda x: x["candidateBaseline"]["entries"][0]["eligibilityEvidence"][
                "upstreamSpec"
            ].update({"state": "known", "value": "inferred"}),
        ),
        (
            "fake event",
            lambda x: x["activation"]["stage05"]["entries"][0].__setitem__(
                "kind", "incident"
            ),
        ),
        (
            "unsafe control path",
            lambda x: x["activation"]["activeControls"][0].__setitem__(
                "path", "_workspace/control.md"
            ),
        ),
        (
            "unsafe stage05 path",
            lambda x: x["activation"]["stage05"]["entries"][0].__setitem__(
                "path", "docs/05.operations/../injected.md"
            ),
        ),
        (
            "helper tracker",
            lambda x: x["activation"]["helperTests"].__setitem__(
                "executionTracker", True
            ),
        ),
        (
            "wrong helper observation boundary",
            lambda x: x["activation"]["helperTests"]["observationBoundary"].__setitem__(
                "worktreeInference", True
            ),
        ),
        (
            "missing helper proposal delta",
            lambda x: x["activation"]["helperTests"]["proposalDelta"][
                "entries"
            ].clear(),
        ),
        (
            "unsafe helper proposal path",
            lambda x: x["activation"]["helperTests"]["proposalDelta"]["entries"][
                0
            ].__setitem__("path", "tests/../injected.py"),
        ),
        (
            "unsafe helper path",
            lambda x: x["activation"]["helperTests"]["entries"][0].__setitem__(
                "path", "tests//injected.py"
            ),
        ),
        (
            "wrong helper proposed counts",
            lambda x: x["activation"]["helperTests"]["proposedCounts"].__setitem__(
                "total", 29
            ),
        ),
        (
            "wrong blob",
            lambda x: x["candidateBaseline"]["entries"][0].__setitem__(
                "sourceBlob", "f" * 40
            ),
        ),
        (
            "wrong baseline commit",
            lambda x: x["candidateBaseline"].__setitem__(
                "candidateBaselineCommit", "f" * 40
            ),
        ),
        (
            "wrong activation ref",
            lambda x: x["activation"].__setitem__("activationCommit", CANDIDATE_COMMIT),
        ),
        ("unknown top key", lambda x: x.__setitem__("unknown", True)),
        (
            "unknown row key",
            lambda x: x["candidateBaseline"]["entries"][0].__setitem__("unknown", True),
        ),
        ("wrong schema", lambda x: x.__setitem__("schemaVersion", 2)),
        (
            "wrong source",
            lambda x: x["methodologySources"][0].__setitem__(
                "observedAt", "2026-07-17"
            ),
        ),
    ]
    for name, mutate in cases:
        fixture = copy.deepcopy(expected)
        mutate(fixture)
        try:
            validate_snapshot(fixture, expected)
        except CensusError:
            continue
        raise AssertionError(f"self-test negative passed: {name}")
    return len(cases) + 1


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the ACER-001 immutable retention census."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if arguments.self_test:
            cases = _run_self_test(arguments.root)
            print(f"[PASS] active corpus retention self-test: {cases} cases")
        else:
            counts = validate_active_corpus_retention(arguments.root)
            print(
                "[PASS] active corpus retention: "
                f"candidates={counts['candidates']} controls={counts['controls']} "
                f"stage05={counts['stage05']} "
                f"helpers_input={counts['helpersInput']} "
                f"helpers_proposed={counts['helpersProposed']}"
            )
    except CensusError as exc:
        print(f"ERR {exc}", file=sys.stderr)
        return 1
    except (AssertionError, OSError, subprocess.SubprocessError):
        print("ERR CENSUS-SELF-TEST .", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
