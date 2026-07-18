#!/usr/bin/env python3
"""Fail-closed ACER-002 eligibility ledger validator.

The ledger is deliberately a reviewed projection of two pinned Git-object
snapshots.  It never inventories the worktree corpus (and therefore never
touches ignored workspace scratch); only the ledger file itself is read from
the supplied root.
"""

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


SCHEMA = "active-corpus-eligibility-ledger.v1"
SCHEMA_VERSION = 1
CANDIDATE_COMMIT = "a12aedfb71ccabd329dabc83bd2863474d1126b0"  # pragma: allowlist secret
EVIDENCE_COMMIT = "e251915f216ef7cf3c7eb9945cdab6cb429ab6e6"  # pragma: allowlist secret; e251915
ACTIVATION_COMMIT = "9e2ec37f483145b322cf68a2f6e697dcf4fb80e1"  # pragma: allowlist secret
CENSUS_PATH = "docs/90.references/data/active-corpus-retention-census.json"
LEDGER_PATH = "docs/90.references/data/active-corpus-eligibility-ledger.json"
PROFILE_PATH = "docs/99.templates/support/document-profiles.json"
MIGRATION_LEDGER_PATH = "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md"
ARCHIVE_INDEX_ANCHOR = "docs/98.archive/README.md#document-index"
PLAN_ROOT = "docs/04.execution/plans"
TASK_ROOT = "docs/04.execution/tasks"
CONTROL_KEY = "2026-07-18-active-corpus-and-execution-retention"
GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 10
MAX_BLOB_BYTES = 2_000_000
MAX_LEDGER_BYTES = 2_000_000
MAX_TREE_ENTRIES = 2_500
MAX_CONSUMER_BYTES = 8_000_000
FULL_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
SAFE_PATH = re.compile(r"[A-Za-z0-9._@+/-]+\Z")
TREE_HEADER = re.compile(rb"(?P<mode>[0-9]{6}) (?P<type>[a-z]+) (?P<object>[0-9a-f]+)\Z")
MARKDOWN_LINK = re.compile(r"\[[^\]\r\n]*\]\(([^()\s]+)\)")
CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": os.devnull, "GIT_CONFIG_VALUE_0": "false",
    "GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "GIT_TERMINAL_PROMPT": "0",
    "HOME": "/nonexistent", "LANG": "C", "LC_ALL": "C", "PAGER": "cat",
    "PATH": "/usr/bin:/bin", "GIT_LITERAL_PATHSPECS": "1",
}

ELIGIBLE_SPECS = {
    "2026-07-12-affected-surface-agent-qa": ("031", "005", "0008", "tranche"),
    "2026-07-12-protected-surface-supply-chain-hardening": ("032", "005", "0008", "tranche"),
    "2026-07-14-template-lifecycle-contract-normalization": ("033", "005", "0008", "follow-up"),
    "2026-07-15-authority-and-lineage-foundation": ("034", "006", "0009", "tranche"),
    "2026-07-16-document-schema-and-lifecycle-contract": ("035", "006", "0009", "tranche"),
    "2026-07-17-archive-record-and-workspace-boundary": ("036", "006", "0009", "tranche"),
}
OWNER_KEY_GAP_LINEAGE = {
    "2026-07-12-document-contract-registry": ("026", "005", "0008"),
    "2026-07-12-template-contract-consolidation": ("027", "005", "0008"),
    "2026-07-12-readme-workspace-profiles": ("028", "005", "0008"),
    "2026-07-12-semantic-document-validation": ("029", "005", "0008"),
    "2026-07-12-authored-document-migration": ("030", "005", "0008"),
}
OWNER_KEY_GAP_KEYS = frozenset(OWNER_KEY_GAP_LINEAGE)
REQUIRED_SELF_TEST_CASES = frozenset({
    "terminal-only", "age-count-only", "ambiguous-lineage", "missing-lineage",
    "plan-only", "task-only", "body-link-only", "ledger-only",
    "current-operational-authority", "missing-residue", "extra-residue",
    "duplicate-residue", "unowned-defer", "missing-consumer", "extra-consumer",
    "missing-provenance", "broken-reciprocal", "broken-spec-link", "missing-closure",
    "missing-archive-route", "missing-rollback", "partial-pair", "unsafe-path",
    "unknown-schema", "duplicate-json", "wrong-commit-object", "wrong-blob-object",
    "hostile-git-steering", "timeout", "ignored-workspace-sentinel",
    "owner-key-gap", "false-extra-axis",
    "missing-eligible-reverse-spec", "missing-eligible-migration-row",
    "wrong-eligible-migration-decision", "empty-eligible-owner-relation",
    "wrong-control-activation-identity",
})


class EligibilityError(ValueError):
    """Stable, single-line, payload-free failure diagnostic."""

    def __init__(self, code: str, path: Any = LEDGER_PATH) -> None:
        self.code = code
        self.path = path if is_safe_path(path) else LEDGER_PATH
        super().__init__(code, self.path)

    def __str__(self) -> str:
        return f"{self.code} {self.path}"


GitRunner = Callable[[str, tuple[str, ...]], subprocess.CompletedProcess[bytes]]


def is_safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not SAFE_PATH.fullmatch(value) or value.startswith("/"):
        return False
    segments = value.split("/")
    return all(segment not in {"", ".", ".."} for segment in segments) and segments[0] != "_workspace"


def validate_path(value: Any) -> str:
    if not is_safe_path(value):
        raise EligibilityError("ELIGIBILITY-PATH")
    return value


def _root(value: str | os.PathLike[str]) -> str:
    try:
        root = os.path.abspath(os.fspath(value))
    except (OSError, TypeError, ValueError) as exc:
        raise EligibilityError("ELIGIBILITY-ROOT", ".") from exc
    if not root or "\0" in root:
        raise EligibilityError("ELIGIBILITY-ROOT", ".")
    return root


def _git_arguments_allowed(arguments: tuple[str, ...]) -> bool:
    if len(arguments) == 3 and arguments[:2] in {("cat-file", "-t"), ("cat-file", "-s"), ("cat-file", "blob")}:
        return FULL_OID.fullmatch(arguments[2]) is not None
    if len(arguments) < 7 or arguments[:4] != ("ls-tree", "-r", "-z", "--full-tree"):
        return False
    if arguments[4] not in {CANDIDATE_COMMIT, EVIDENCE_COMMIT, ACTIVATION_COMMIT} or arguments[5] != "--":
        return False
    return arguments[6:] in {
        (CENSUS_PATH,), (PROFILE_PATH,), (MIGRATION_LEDGER_PATH,), ("docs",),
        (PLAN_ROOT, TASK_ROOT),
        (f"{PLAN_ROOT}/{CONTROL_KEY}.md", f"{TASK_ROOT}/{CONTROL_KEY}.md"),
    }


def _run_git(root: str, arguments: tuple[str, ...]) -> subprocess.CompletedProcess[bytes]:
    if not _git_arguments_allowed(arguments):
        raise EligibilityError("ELIGIBILITY-GIT-QUERY", ".git")
    try:
        return subprocess.run([GIT_EXECUTABLE, *arguments], cwd=root, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=CLOSED_GIT_ENVIRONMENT,
            timeout=GIT_TIMEOUT_SECONDS, shell=False, check=False)
    except subprocess.TimeoutExpired as exc:
        raise EligibilityError("ELIGIBILITY-GIT-TIMEOUT", ".git") from exc
    except OSError as exc:
        raise EligibilityError("ELIGIBILITY-GIT-STARTUP", ".git") from exc


def _git(root: str, arguments: tuple[str, ...], runner: GitRunner, code: str, path: str) -> bytes:
    result = runner(root, arguments)
    if not isinstance(result, subprocess.CompletedProcess) or result.returncode != 0 or not isinstance(result.stdout, bytes):
        raise EligibilityError(code, path)
    return result.stdout


def _verify_commit(root: str, commit: str, runner: GitRunner) -> None:
    if not FULL_OID.fullmatch(commit):
        raise EligibilityError("ELIGIBILITY-COMMIT-ID", ".git")
    if _git(root, ("cat-file", "-t", commit), runner, "ELIGIBILITY-COMMIT-MISSING", ".git") != b"commit\n":
        raise EligibilityError("ELIGIBILITY-COMMIT-TYPE", ".git")


def _tree(root: str, commit: str, paths: tuple[str, ...], runner: GitRunner) -> dict[str, str]:
    raw = _git(root, ("ls-tree", "-r", "-z", "--full-tree", commit, "--", *paths), runner, "ELIGIBILITY-TREE", ".git")
    if raw and not raw.endswith(b"\0"):
        raise EligibilityError("ELIGIBILITY-TREE", ".git")
    result: dict[str, str] = {}
    records = raw[:-1].split(b"\0") if raw else []
    if len(records) > MAX_TREE_ENTRIES:
        raise EligibilityError("ELIGIBILITY-TREE-BOUNDS", ".git")
    for record in records:
        if record.count(b"\t") != 1:
            raise EligibilityError("ELIGIBILITY-TREE", ".git")
        header, raw_path = record.split(b"\t", 1)
        match = TREE_HEADER.fullmatch(header)
        try:
            path = raw_path.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise EligibilityError("ELIGIBILITY-TREE", ".git") from exc
        if not is_safe_path(path) or match is None or match.group("mode") not in {b"100644", b"100755"} or match.group("type") != b"blob":
            raise EligibilityError("ELIGIBILITY-TREE", ".git")
        oid = match.group("object").decode("ascii")
        if not FULL_OID.fullmatch(oid) or path in result:
            raise EligibilityError("ELIGIBILITY-TREE", ".git")
        result[path] = oid
    return result


def _blob(root: str, oid: str, path: str, runner: GitRunner) -> bytes:
    if not FULL_OID.fullmatch(oid):
        raise EligibilityError("ELIGIBILITY-BLOB-ID", path)
    if _git(root, ("cat-file", "-t", oid), runner, "ELIGIBILITY-BLOB-MISSING", path) != b"blob\n":
        raise EligibilityError("ELIGIBILITY-BLOB-TYPE", path)
    size_raw = _git(root, ("cat-file", "-s", oid), runner, "ELIGIBILITY-BLOB-SIZE", path)
    if not re.fullmatch(rb"(?:0|[1-9][0-9]*)\n", size_raw):
        raise EligibilityError("ELIGIBILITY-BLOB-SIZE", path)
    size = int(size_raw)
    if size > MAX_BLOB_BYTES:
        raise EligibilityError("ELIGIBILITY-BLOB-BOUNDS", path)
    value = _git(root, ("cat-file", "blob", oid), runner, "ELIGIBILITY-BLOB-READ", path)
    if len(value) != size:
        raise EligibilityError("ELIGIBILITY-BLOB-LENGTH", path)
    return value


def _json(value: bytes, path: str) -> Any:
    try:
        return json.loads(value.decode("utf-8", errors="strict"), object_pairs_hook=_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError, EligibilityError) as exc:
        if isinstance(exc, EligibilityError):
            raise
        raise EligibilityError("ELIGIBILITY-JSON", path) from exc


def _duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EligibilityError("ELIGIBILITY-JSON-DUPLICATE")
        result[key] = value
    return result


def _require_mapping(value: Any, code: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise EligibilityError(code)
    return value


def _require_keys(value: Mapping[str, Any], expected: set[str], code: str) -> None:
    if set(value) != expected:
        raise EligibilityError(code)


def _spec_path(number: str) -> str:
    suffix = {
        "026": "document-contract-registry", "027": "template-contract-consolidation",
        "028": "readme-workspace-profiles", "029": "semantic-document-validation",
        "030": "authored-document-migration",
        "031": "affected-surface-agent-qa", "032": "protected-surface-supply-chain-hardening",
        "033": "template-lifecycle-contract-normalization", "034": "authority-and-lineage-foundation",
        "035": "document-schema-and-lifecycle-contract", "036": "archive-record-and-workspace-boundary",
    }[number]
    return f"docs/03.specs/{number}-{suffix}/spec.md"


def _link_targets(text: str, source: str) -> set[str]:
    targets: set[str] = set()
    for raw in MARKDOWN_LINK.findall(text):
        target = raw.split("#", 1)[0]
        if not target or ":" in target or target.startswith("/"):
            continue
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source), target))
        if is_safe_path(candidate):
            targets.add(candidate)
    return targets


def _load_pinned_json(root: str, commit: str, path: str, runner: GitRunner) -> Any:
    tree = _tree(root, commit, (path,), runner)
    if set(tree) != {path}:
        raise EligibilityError("ELIGIBILITY-PINNED-INPUT", path)
    return _json(_blob(root, tree[path], path, runner), path)


def _lineage(profile: Any, spec: str, prd: str, ard: str, state: str) -> dict[str, str]:
    top = _require_mapping(profile, "ELIGIBILITY-LINEAGE")
    lineage = _require_mapping(top.get("programLineage"), "ELIGIBILITY-LINEAGE")
    programs = lineage.get("programs")
    if not isinstance(programs, list):
        raise EligibilityError("ELIGIBILITY-LINEAGE")
    for program in programs:
        item = _require_mapping(program, "ELIGIBILITY-LINEAGE")
        if item.get("prd") != prd or item.get("ard") != ard:
            continue
        section = "followUps" if state == "follow-up" else "tranches"
        entries = item.get(section)
        if not isinstance(entries, list):
            break
        for entry in entries:
            if _require_mapping(entry, "ELIGIBILITY-LINEAGE").get("spec") == spec and entry.get("state") == "done":
                return {"prd": prd, "ard": ard, "spec": spec, "state": state, "completion": "done"}
    raise EligibilityError("ELIGIBILITY-LINEAGE")


def _consumer_map(
    root: str,
    candidate_paths: set[str],
    pair_by_path: Mapping[str, str],
    runner: GitRunner,
) -> dict[str, list[str]]:
    docs = _tree(root, EVIDENCE_COMMIT, ("docs",), runner)
    consumers = {path: set() for path in candidate_paths}
    total = 0
    for path, oid in sorted(docs.items()):
        raw = _blob(root, oid, path, runner)
        total += len(raw)
        if total > MAX_CONSUMER_BYTES:
            raise EligibilityError("ELIGIBILITY-CONSUMER-BOUNDS", ".git")
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise EligibilityError("ELIGIBILITY-CONSUMER-UTF8", path) from exc
        targets = _link_targets(text, path) if path.endswith(".md") else set()
        for candidate in candidate_paths:
            if candidate not in targets and candidate not in text:
                continue
            # The reciprocal Plan/Task is part of the same future atomic batch;
            # it is relationship evidence, not an external repair consumer.
            if pair_by_path.get(path) == pair_by_path.get(candidate):
                continue
            consumers[candidate].add(path)
    return {path: sorted(values) for path, values in consumers.items()}


def _migration_rows(text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]] if line.startswith("|") and line.endswith("|") else []
        if len(cells) != 14 or not cells or not re.fullmatch(r"`[^`]+`", cells[0]):
            continue
        path = cells[0][1:-1]
        if is_safe_path(path):
            if path in rows:
                raise EligibilityError("ELIGIBILITY-MIGRATION-DUPLICATE", MIGRATION_LEDGER_PATH)
            canonical = cells[5][1:-1] if re.fullmatch(r"`[^`]+`", cells[5]) else ""
            if not is_safe_path(canonical):
                raise EligibilityError("ELIGIBILITY-MIGRATION-SCHEMA", MIGRATION_LEDGER_PATH)
            rows[path] = {"relation": cells[3], "decision": cells[4], "canonicalPath": canonical}
    return rows


def _program_membership(profile: Any, spec_path: str) -> Mapping[str, Any] | None:
    match = re.fullmatch(r"docs/03\.specs/([0-9]{3})-[A-Za-z0-9._-]+/spec\.md", spec_path)
    if match is None:
        return None
    number = match.group(1)
    top = _require_mapping(profile, "ELIGIBILITY-LINEAGE")
    lineage = _require_mapping(top.get("programLineage"), "ELIGIBILITY-LINEAGE")
    programs = lineage.get("programs")
    if not isinstance(programs, list):
        raise EligibilityError("ELIGIBILITY-LINEAGE")
    matches: list[Mapping[str, Any]] = []
    for program in programs:
        item = _require_mapping(program, "ELIGIBILITY-LINEAGE")
        for section in ("tranches", "followUps"):
            entries = item.get(section)
            if not isinstance(entries, list):
                raise EligibilityError("ELIGIBILITY-LINEAGE")
            for entry in entries:
                value = _require_mapping(entry, "ELIGIBILITY-LINEAGE")
                if value.get("spec") == number:
                    matches.append({"prd": item.get("prd"), "ard": item.get("ard"), "state": value.get("state"), "kind": section})
    return matches[0] if len(matches) == 1 else None


def _defer_evidence(
    source: Mapping[str, Any],
    source_text: str,
    profile: Any,
    migration: Mapping[str, str],
    candidate_paths: set[str],
) -> tuple[list[str], str]:
    path, kind, key = str(source["path"]), str(source["kind"]), str(source["pairKey"])
    links = _link_targets(source_text, path)
    counterpart = f"{TASK_ROOT if kind == 'plan' else PLAN_ROOT}/{key}.md"
    specs = sorted(target for target in links if re.fullmatch(r"docs/03\.specs/[0-9]{3}-[A-Za-z0-9._-]+/spec\.md", target))
    axes: list[str] = []
    if source.get("pairState") != "paired" or counterpart not in candidate_paths:
        axes.append("pair-completeness")
    if len(specs) != 1:
        axes.append("authoritative-upstream-spec")
    if counterpart not in links:
        axes.append("reciprocal-plan-task-link")
    if len(specs) != 1 or _program_membership(profile, specs[0]) is None or _program_membership(profile, specs[0]).get("state") != "done":
        axes.append("program-lineage-completion")
    if len(specs) != 1 or specs[0] not in links:
        axes.append("reciprocal-spec-link")
    migration_row = migration.get(path)
    if migration_row is None:
        axes.append("ledger-current-owner-lineage")
        axes.append("closure-evidence")
    else:
        if not migration_row["relation"] or migration_row["decision"] not in {"preserve", "transform"} or migration_row["canonicalPath"] != path:
            axes.append("ledger-current-owner-lineage")
        if migration_row["decision"] not in {"preserve", "transform"}:
            axes.append("closure-evidence")
    if key in OWNER_KEY_GAP_KEYS and "ledger-current-owner-lineage" not in axes:
        # These completed Specs have migration-table rows but no exact current
        # operational-owner key that an ACER-003 repair batch can replace.
        axes.append("ledger-current-owner-lineage")
    # A body link is evidence for only this axis; it never independently promotes.
    if not axes:
        axes.append("cutover-eligibility-not-approved")
    return axes, "missing-" + "-and-".join(axes)


def _candidate_rows(census: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    try:
        rows = census["candidateBaseline"]["entries"]
    except (KeyError, TypeError) as exc:
        raise EligibilityError("ELIGIBILITY-CENSUS") from exc
    if not isinstance(rows, list) or len(rows) != 110:
        raise EligibilityError("ELIGIBILITY-CENSUS")
    paths: set[str] = set()
    result: list[Mapping[str, Any]] = []
    for row in rows:
        item = _require_mapping(row, "ELIGIBILITY-CENSUS")
        path = item.get("path")
        if not is_safe_path(path) or path in paths or item.get("kind") not in {"plan", "task"} or not FULL_OID.fullmatch(item.get("sourceBlob", "")):
            raise EligibilityError("ELIGIBILITY-CENSUS")
        paths.add(path)
        result.append(item)
    return sorted(result, key=lambda item: str(item["path"]))


def _archive_destination(path: str, kind: str) -> str:
    root = "plans" if kind == "plan" else "tasks"
    return f"docs/98.archive/04.execution/{root}/{posixpath.basename(path)}"


def _closed_pair_evidence(
    root: str,
    runner: GitRunner,
    evidence_tree: Mapping[str, str],
    migration: Mapping[str, Mapping[str, str]],
    profile: Any,
    *,
    path: str,
    kind: str,
    key: str,
    spec: str,
    prd: str,
    ard: str,
    state: str,
    relation_policy: str,
    link_code: str,
    reverse_spec_code: str,
    migration_missing_code: str,
    migration_schema_code: str,
    utf8_code: str,
) -> dict[str, Any]:
    """Return closed, normalized proof for a complete Plan/Task pair.

    Both promotion and the owner-key-gap exception use the same pinned-object
    proof.  Their only closure difference is the migration relation policy.
    """
    if relation_policy not in {"nonempty", "exactly-empty"}:
        raise EligibilityError("ELIGIBILITY-RELATION-POLICY", path)
    spec_path = _spec_path(spec)
    counterpart = f"{TASK_ROOT if kind == 'plan' else PLAN_ROOT}/{key}.md"
    plan_path, task_path = f"{PLAN_ROOT}/{key}.md", f"{TASK_ROOT}/{key}.md"
    if path not in evidence_tree or spec_path not in evidence_tree:
        raise EligibilityError(link_code, path)
    try:
        source_text = _blob(root, evidence_tree[path], path, runner).decode("utf-8", errors="strict")
        spec_text = _blob(root, evidence_tree[spec_path], spec_path, runner).decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise EligibilityError(utf8_code, path) from exc
    if spec_path not in _link_targets(source_text, path) or counterpart not in _link_targets(source_text, path):
        raise EligibilityError(link_code, path)
    if not {plan_path, task_path} <= _link_targets(spec_text, spec_path):
        raise EligibilityError(reverse_spec_code, path)
    migration_row = migration.get(path)
    if migration_row is None:
        raise EligibilityError(migration_missing_code, path)
    relation = migration_row["relation"]
    relation_matches = bool(relation) if relation_policy == "nonempty" else relation == ""
    if (
        not relation_matches
        or migration_row["decision"] not in {"preserve", "transform"}
        or migration_row["canonicalPath"] != path
    ):
        raise EligibilityError(migration_schema_code, path)
    return {
        "upstream": _lineage(profile, spec, prd, ard, state),
        "reciprocalLinks": [counterpart],
        "specLinks": [spec_path],
        "closureReferences": [spec_path, MIGRATION_LEDGER_PATH],
    }


def build_expected_ledger(root: str | os.PathLike[str], runner: GitRunner = _run_git) -> dict[str, Any]:
    repository = _root(root)
    for commit in (CANDIDATE_COMMIT, EVIDENCE_COMMIT, ACTIVATION_COMMIT):
        _verify_commit(repository, commit, runner)
    census = _require_mapping(_load_pinned_json(repository, EVIDENCE_COMMIT, CENSUS_PATH, runner), "ELIGIBILITY-CENSUS")
    profile = _load_pinned_json(repository, EVIDENCE_COMMIT, PROFILE_PATH, runner)
    candidates = _candidate_rows(census)
    candidate_paths = {str(row["path"]) for row in candidates}
    pair_by_path = {str(row["path"]): str(row["pairKey"]) for row in candidates}
    migration_tree = _tree(repository, EVIDENCE_COMMIT, (MIGRATION_LEDGER_PATH,), runner)
    if set(migration_tree) != {MIGRATION_LEDGER_PATH}:
        raise EligibilityError("ELIGIBILITY-MIGRATION-MISSING", MIGRATION_LEDGER_PATH)
    try:
        migration_text = _blob(repository, migration_tree[MIGRATION_LEDGER_PATH], MIGRATION_LEDGER_PATH, runner).decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise EligibilityError("ELIGIBILITY-MIGRATION-UTF8", MIGRATION_LEDGER_PATH) from exc
    migration = _migration_rows(migration_text)
    consumers = _consumer_map(repository, candidate_paths, pair_by_path, runner)
    candidate_tree = _tree(repository, CANDIDATE_COMMIT, (PLAN_ROOT, TASK_ROOT), runner)
    evidence_tree = _tree(repository, EVIDENCE_COMMIT, ("docs",), runner)
    rows: list[dict[str, Any]] = []
    for source in candidates:
        path, kind, key, blob = (str(source["path"]), str(source["kind"]), str(source["pairKey"]), str(source["sourceBlob"]))
        if candidate_tree.get(path) != blob:
            raise EligibilityError("ELIGIBILITY-CANDIDATE-IDENTITY", path)
        is_eligible = key in ELIGIBLE_SPECS
        destination = _archive_destination(path, kind)
        base: dict[str, Any] = {
            "path": path, "kind": kind, "pairKey": key, "status": source.get("status"),
            "sourceCommit": CANDIDATE_COMMIT, "sourceBlob": blob, "evidenceSnapshotCommit": EVIDENCE_COMMIT,
            "upstream": None, "authority": "unresolved", "reciprocalLinks": [], "specLinks": [],
            "trackedCurrentConsumers": consumers[path], "closureReferences": [],
            "archive": {"destination": destination, "replacementIndexAnchor": ARCHIVE_INDEX_ANCHOR},
            "recovery": {"sourceCommit": CANDIDATE_COMMIT, "sourceBlob": blob,
                "inverseBatchRecipe": "restore-exact-source-blob-before-index-ledger-consumer-repair",
                "cutoverComplete": False},
            "disposition": "DEFER", "reason": "missing-pinned-eligibility-evidence", "owner": "platform",
            "refreshTrigger": "ACER-005-or-exact-upstream-evidence-change",
            "missingAxes": ["program-lineage", "reciprocal-links", "closure"], "residueClass": "deferred-evidence",
        }
        if is_eligible:
            spec, prd, ard, state = ELIGIBLE_SPECS[key]
            closed = _closed_pair_evidence(
                repository, runner, evidence_tree, migration, profile,
                path=path, kind=kind, key=key, spec=spec, prd=prd, ard=ard, state=state,
                relation_policy="nonempty", link_code="ELIGIBILITY-RECIPROCAL",
                reverse_spec_code="ELIGIBILITY-REVERSE-SPEC",
                migration_missing_code="ELIGIBILITY-MIGRATION-MISSING",
                migration_schema_code="ELIGIBILITY-MIGRATION-SCHEMA",
                utf8_code="ELIGIBILITY-REVERSE-SPEC",
            )
            if not consumers[path]:
                raise EligibilityError("ELIGIBILITY-CONSUMER", path)
            base.update({
                "authority": "cutover-replaceable-current-tree-authority",
                "disposition": "eligible", "reason": "complete-pinned-lineage-reciprocal-closure",
                "refreshTrigger": "ACER-003-atomic-cutover",
                "missingAxes": [], "residueClass": "none",
                **closed,
            })
        elif key in OWNER_KEY_GAP_LINEAGE:
            spec, prd, ard = OWNER_KEY_GAP_LINEAGE[key]
            closed = _closed_pair_evidence(
                repository, runner, evidence_tree, migration, profile,
                path=path, kind=kind, key=key, spec=spec, prd=prd, ard=ard, state="tranche",
                relation_policy="exactly-empty", link_code="ELIGIBILITY-OWNER-GAP-LINK",
                reverse_spec_code="ELIGIBILITY-OWNER-GAP-LINK",
                migration_missing_code="ELIGIBILITY-OWNER-GAP-CLOSURE",
                migration_schema_code="ELIGIBILITY-OWNER-GAP-CLOSURE",
                utf8_code="ELIGIBILITY-OWNER-GAP-UTF8",
            )
            base.update({
                "authority": "owner-key-gap-resolved-partial-evidence",
                "reason": "missing-ledger-current-owner-lineage",
                "missingAxes": ["ledger-current-owner-lineage"],
                "residueClass": "resolved-partial-evidence",
                **closed,
            })
        else:
            source_text = _blob(repository, evidence_tree.get(path, ""), path, runner).decode("utf-8", errors="strict") if path in evidence_tree else ""
            axes, reason = _defer_evidence(source, source_text, profile, migration, candidate_paths)
            base.update({"reason": reason, "missingAxes": axes})
        rows.append(base)
    eligible = [row for row in rows if row["disposition"] == "eligible"]
    if len(rows) != 110 or len(eligible) != 12 or {row["pairKey"] for row in eligible} != set(ELIGIBLE_SPECS):
        raise EligibilityError("ELIGIBILITY-COUNTS")
    for key in ELIGIBLE_SPECS:
        promoted = [row for row in eligible if row["pairKey"] == key]
        if len(promoted) != 2 or {row["kind"] for row in promoted} != {"plan", "task"}:
            raise EligibilityError("ELIGIBILITY-PARTIAL-PAIR")
    controls = census.get("activation", {}).get("activeControls")
    if not isinstance(controls, list) or len(controls) != 2:
        raise EligibilityError("ELIGIBILITY-CONTROLS")
    control_paths = (f"{PLAN_ROOT}/{CONTROL_KEY}.md", f"{TASK_ROOT}/{CONTROL_KEY}.md")
    control_tree = _tree(repository, ACTIVATION_COMMIT, control_paths, runner)
    if set(control_tree) != set(control_paths):
        raise EligibilityError("ELIGIBILITY-CONTROLS")
    control_rows: list[dict[str, Any]] = []
    for control in controls:
        item = _require_mapping(control, "ELIGIBILITY-CONTROLS")
        path = item.get("path")
        kind = item.get("kind")
        if not is_safe_path(path) or path not in control_tree or kind not in {"plan", "task"} or not str(path).startswith(f"docs/04.execution/{kind}s/") or item.get("sourceBlob") != control_tree[path] or item.get("pairKey") != CONTROL_KEY or item.get("disposition") != "retain" or item.get("candidateEligible") is not False:
            raise EligibilityError("ELIGIBILITY-CONTROLS")
        control_rows.append({"path": item.get("path"), "kind": item.get("kind"), "pairKey": CONTROL_KEY,
            "sourceCommit": ACTIVATION_COMMIT, "sourceBlob": item.get("sourceBlob"), "disposition": "retain",
            "reason": "active-spec-037-control", "owner": "platform", "refreshTrigger": "Spec037 closure"})
    return {"$schema": SCHEMA, "schemaVersion": SCHEMA_VERSION, "candidateSourceCommit": CANDIDATE_COMMIT,
        "evidenceSnapshotCommit": EVIDENCE_COMMIT,
        "counts": {"candidates": 110, "eligible": 12, "DEFER": 98, "retain": 2, "residue": 0},
        "candidateRows": rows, "controls": sorted(control_rows, key=lambda item: str(item["path"]))}


ROW_KEYS = {"path", "kind", "pairKey", "status", "sourceCommit", "sourceBlob", "evidenceSnapshotCommit", "upstream", "authority", "reciprocalLinks", "specLinks", "trackedCurrentConsumers", "closureReferences", "archive", "recovery", "disposition", "reason", "owner", "refreshTrigger", "missingAxes", "residueClass"}


def _preflight(ledger: Any) -> Mapping[str, Any]:
    top = _require_mapping(ledger, "ELIGIBILITY-SCHEMA")
    _require_keys(top, {"$schema", "schemaVersion", "candidateSourceCommit", "evidenceSnapshotCommit", "counts", "candidateRows", "controls"}, "ELIGIBILITY-SCHEMA")
    if top.get("$schema") != SCHEMA or top.get("schemaVersion") != SCHEMA_VERSION or top.get("candidateSourceCommit") != CANDIDATE_COMMIT or top.get("evidenceSnapshotCommit") != EVIDENCE_COMMIT:
        raise EligibilityError("ELIGIBILITY-SCHEMA")
    counts = _require_mapping(top.get("counts"), "ELIGIBILITY-COUNTS")
    _require_keys(counts, {"candidates", "eligible", "DEFER", "retain", "residue"}, "ELIGIBILITY-COUNTS")
    if counts != {"candidates": 110, "eligible": 12, "DEFER": 98, "retain": 2, "residue": 0}:
        raise EligibilityError("ELIGIBILITY-COUNTS")
    rows = top.get("candidateRows")
    if not isinstance(rows, list) or len(rows) != 110:
        raise EligibilityError("ELIGIBILITY-ROWS")
    prior = ""
    seen: set[str] = set()
    for row_value in rows:
        row = _require_mapping(row_value, "ELIGIBILITY-ROW")
        _require_keys(row, ROW_KEYS, "ELIGIBILITY-ROW")
        path = validate_path(row.get("path"))
        if path in seen or path <= prior:
            raise EligibilityError("ELIGIBILITY-ROW-ORDER")
        seen.add(path); prior = path
        for key in ("reciprocalLinks", "specLinks", "trackedCurrentConsumers", "closureReferences", "missingAxes"):
            value = row.get(key)
            if not isinstance(value, list) or any(not is_safe_path(item) and key != "missingAxes" for item in value):
                raise EligibilityError("ELIGIBILITY-ROW")
        archive = _require_mapping(row.get("archive"), "ELIGIBILITY-ARCHIVE")
        _require_keys(archive, {"destination", "replacementIndexAnchor"}, "ELIGIBILITY-ARCHIVE")
        if not is_safe_path(archive.get("destination")) or archive.get("replacementIndexAnchor") != ARCHIVE_INDEX_ANCHOR:
            raise EligibilityError("ELIGIBILITY-ARCHIVE")
        recovery = _require_mapping(row.get("recovery"), "ELIGIBILITY-RECOVERY")
        _require_keys(recovery, {"sourceCommit", "sourceBlob", "inverseBatchRecipe", "cutoverComplete"}, "ELIGIBILITY-RECOVERY")
        if recovery.get("cutoverComplete") is not False or recovery.get("sourceCommit") != CANDIDATE_COMMIT or recovery.get("sourceBlob") != row.get("sourceBlob"):
            raise EligibilityError("ELIGIBILITY-RECOVERY")
        if row.get("sourceCommit") != CANDIDATE_COMMIT or row.get("evidenceSnapshotCommit") != EVIDENCE_COMMIT or not FULL_OID.fullmatch(row.get("sourceBlob", "")):
            raise EligibilityError("ELIGIBILITY-PROVENANCE")
        expected_destination = _archive_destination(path, row.get("kind")) if row.get("kind") in {"plan", "task"} else ""
        if archive.get("destination") != expected_destination:
            raise EligibilityError("ELIGIBILITY-ARCHIVE")
        if row.get("disposition") == "eligible":
            upstream = _require_mapping(row.get("upstream"), "ELIGIBILITY-LINEAGE")
            _require_keys(upstream, {"prd", "ard", "spec", "state", "completion"}, "ELIGIBILITY-LINEAGE")
            if row.get("authority") != "cutover-replaceable-current-tree-authority" or len(row["reciprocalLinks"]) != 1 or len(row["specLinks"]) != 1 or not row["trackedCurrentConsumers"] or not row["closureReferences"] or row.get("missingAxes") != [] or row.get("residueClass") != "none":
                raise EligibilityError("ELIGIBILITY-ELIGIBLE-EVIDENCE")
        elif row.get("disposition") == "DEFER":
            axes = row.get("missingAxes")
            common = row.get("owner") == "platform" and row.get("refreshTrigger") == "ACER-005-or-exact-upstream-evidence-change" and isinstance(axes, list) and bool(axes) and not any(not isinstance(axis, str) or not axis for axis in axes)
            if not common:
                raise EligibilityError("ELIGIBILITY-DEFER")
            if row.get("authority") == "unresolved":
                valid = row.get("upstream") is None and not row.get("reciprocalLinks") and not row.get("specLinks") and not row.get("closureReferences") and row.get("reason") == "missing-" + "-and-".join(axes) and row.get("residueClass") == "deferred-evidence"
            elif row.get("authority") == "owner-key-gap-resolved-partial-evidence":
                upstream = _require_mapping(row.get("upstream"), "ELIGIBILITY-LINEAGE")
                valid = set(upstream) == {"prd", "ard", "spec", "state", "completion"} and upstream.get("completion") == "done" and len(row["reciprocalLinks"]) == 1 and len(row["specLinks"]) == 1 and row.get("closureReferences") == [row["specLinks"][0], MIGRATION_LEDGER_PATH] and axes == ["ledger-current-owner-lineage"] and row.get("reason") == "missing-ledger-current-owner-lineage" and row.get("residueClass") == "resolved-partial-evidence"
            else:
                valid = False
            if not valid:
                raise EligibilityError("ELIGIBILITY-DEFER")
        else:
            raise EligibilityError("ELIGIBILITY-DISPOSITION")
    return top


def validate_ledger(ledger: Any, expected: Mapping[str, Any]) -> None:
    actual = _preflight(ledger)
    if actual != expected:
        raise EligibilityError("ELIGIBILITY-DRIFT")


def load_ledger(root: str | os.PathLike[str]) -> Any:
    repository = _root(root)
    path = os.path.join(repository, LEDGER_PATH)
    try:
        metadata = os.lstat(path)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or metadata.st_size > MAX_LEDGER_BYTES:
            raise EligibilityError("ELIGIBILITY-LEDGER-TYPE")
        with open(path, "r", encoding="utf-8", newline="") as handle:
            return json.load(handle, object_pairs_hook=_duplicate_keys)
    except EligibilityError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EligibilityError("ELIGIBILITY-LEDGER-READ") from exc


def validate_active_corpus_eligibility(root: str | os.PathLike[str], runner: GitRunner = _run_git) -> dict[str, int]:
    expected = build_expected_ledger(root, runner)
    validate_ledger(load_ledger(root), expected)
    return {"candidates": 110, "eligible": 12, "defer": 98, "controls": 2}


TARGETED_ELIGIBLE_KEY = "2026-07-12-affected-surface-agent-qa"
TARGETED_ELIGIBLE_PATH = f"{PLAN_ROOT}/{TARGETED_ELIGIBLE_KEY}.md"
TARGETED_ELIGIBLE_SPEC_PATH = _spec_path("031")


class TargetedRunnerCase:
    def __init__(
        self,
        expected_code: str,
        expected_path: str,
        mutate: Callable[[str, Mapping[str, Any]], GitRunner],
    ) -> None:
        self.expected_code = expected_code
        self.expected_path = expected_path
        self.mutate = mutate


def _targeted_fixture_targets(root: str) -> dict[str, Any]:
    """Obtain fixture OIDs and source bytes from the actual pinned trees."""
    evidence = _tree(root, EVIDENCE_COMMIT, ("docs",), _run_git)
    activation_paths = (f"{PLAN_ROOT}/{CONTROL_KEY}.md", f"{TASK_ROOT}/{CONTROL_KEY}.md")
    activation = _tree(root, ACTIVATION_COMMIT, activation_paths, _run_git)
    if TARGETED_ELIGIBLE_SPEC_PATH not in evidence or MIGRATION_LEDGER_PATH not in evidence or set(activation) != set(activation_paths):
        raise AssertionError("targeted fixture sources unavailable")
    return {
        "specOid": evidence[TARGETED_ELIGIBLE_SPEC_PATH],
        "specBytes": _blob(root, evidence[TARGETED_ELIGIBLE_SPEC_PATH], TARGETED_ELIGIBLE_SPEC_PATH, _run_git),
        "migrationOid": evidence[MIGRATION_LEDGER_PATH],
        "migrationBytes": _blob(root, evidence[MIGRATION_LEDGER_PATH], MIGRATION_LEDGER_PATH, _run_git),
        "controlPaths": activation_paths,
        "controlPlanOid": activation[activation_paths[0]],
    }


def _blob_override_runner(oid: str, value: bytes) -> GitRunner:
    """Override both size and payload reads for one real pinned blob OID."""
    def runner(root: str, arguments: tuple[str, ...]) -> subprocess.CompletedProcess[bytes]:
        if arguments == ("cat-file", "-s", oid):
            return subprocess.CompletedProcess([GIT_EXECUTABLE, *arguments], 0, f"{len(value)}\n".encode("ascii"))
        if arguments == ("cat-file", "blob", oid):
            return subprocess.CompletedProcess([GIT_EXECUTABLE, *arguments], 0, value)
        return _run_git(root, arguments)
    return runner


def _migration_row_edit(value: bytes, path: str, column: int, replacement: str | None) -> bytes:
    """Change one 14-column migration row without perturbing any other row."""
    try:
        lines = value.decode("utf-8", errors="strict").splitlines(keepends=True)
    except UnicodeDecodeError as exc:
        raise AssertionError("targeted migration fixture is not UTF-8") from exc
    found = 0
    updated: list[str] = []
    for line in lines:
        cells = line.rstrip("\r\n").split("|")
        if len(cells) == 16 and cells[1].strip() == f"`{path}`":
            found += 1
            if replacement is None:
                continue
            cells[column] = f" {replacement} "
            line = "|".join(cells) + ("\r\n" if line.endswith("\r\n") else "\n")
        updated.append(line)
    if found != 1:
        raise AssertionError("targeted migration row is not unique")
    return "".join(updated).encode("utf-8")


def _mutate_missing_eligible_reverse_spec(root: str, targets: Mapping[str, Any]) -> GitRunner:
    original = targets["specBytes"]
    needle = b"../../04.execution/plans/2026-07-12-affected-surface-agent-qa.md"
    if original.count(needle) != 1:
        raise AssertionError("targeted reverse Spec link is not unique")
    return _blob_override_runner(str(targets["specOid"]), original.replace(needle, b"../../04.execution/plans/missing-proof.md", 1))


def _mutate_missing_eligible_migration_row(root: str, targets: Mapping[str, Any]) -> GitRunner:
    return _blob_override_runner(str(targets["migrationOid"]), _migration_row_edit(targets["migrationBytes"], TARGETED_ELIGIBLE_PATH, 0, None))


def _mutate_wrong_eligible_migration_decision(root: str, targets: Mapping[str, Any]) -> GitRunner:
    return _blob_override_runner(str(targets["migrationOid"]), _migration_row_edit(targets["migrationBytes"], TARGETED_ELIGIBLE_PATH, 5, "invalid"))


def _mutate_empty_eligible_owner_relation(root: str, targets: Mapping[str, Any]) -> GitRunner:
    return _blob_override_runner(str(targets["migrationOid"]), _migration_row_edit(targets["migrationBytes"], TARGETED_ELIGIBLE_PATH, 4, ""))


def _mutate_wrong_control_activation_identity(root: str, targets: Mapping[str, Any]) -> GitRunner:
    arguments = ("ls-tree", "-r", "-z", "--full-tree", ACTIVATION_COMMIT, "--", *targets["controlPaths"])
    original_oid = str(targets["controlPlanOid"]).encode("ascii")
    replacement_oid = b"f" * len(original_oid)
    if original_oid == replacement_oid:
        replacement_oid = b"0" * len(original_oid)

    def runner(run_root: str, actual: tuple[str, ...]) -> subprocess.CompletedProcess[bytes]:
        if actual == arguments:
            result = _run_git(run_root, actual)
            if result.returncode != 0 or result.stdout.count(original_oid) != 1:
                raise AssertionError("targeted activation control identity is not unique")
            return subprocess.CompletedProcess([GIT_EXECUTABLE, *actual], 0, result.stdout.replace(original_oid, replacement_oid, 1))
        return _run_git(run_root, actual)
    return runner


TARGETED_RUNNER_CASES = {
    "missing-eligible-reverse-spec": TargetedRunnerCase("ELIGIBILITY-REVERSE-SPEC", TARGETED_ELIGIBLE_PATH, _mutate_missing_eligible_reverse_spec),
    "missing-eligible-migration-row": TargetedRunnerCase("ELIGIBILITY-MIGRATION-MISSING", TARGETED_ELIGIBLE_PATH, _mutate_missing_eligible_migration_row),
    "wrong-eligible-migration-decision": TargetedRunnerCase("ELIGIBILITY-MIGRATION-SCHEMA", TARGETED_ELIGIBLE_PATH, _mutate_wrong_eligible_migration_decision),
    "empty-eligible-owner-relation": TargetedRunnerCase("ELIGIBILITY-MIGRATION-SCHEMA", TARGETED_ELIGIBLE_PATH, _mutate_empty_eligible_owner_relation),
    "wrong-control-activation-identity": TargetedRunnerCase("ELIGIBILITY-CONTROLS", LEDGER_PATH, _mutate_wrong_control_activation_identity),
}


def targeted_runner_case_results(root: str | os.PathLike[str]) -> dict[str, tuple[str, str]]:
    """Execute every pinned-object runner fixture and verify its exact failure."""
    repository = _root(root)
    targets = _targeted_fixture_targets(repository)
    results: dict[str, tuple[str, str]] = {}
    for name, case in TARGETED_RUNNER_CASES.items():
        try:
            build_expected_ledger(repository, case.mutate(repository, targets))
        except EligibilityError as exc:
            actual = (exc.code, str(exc.path))
            expected = (case.expected_code, case.expected_path)
            if actual != expected:
                raise AssertionError(f"targeted runner wrong diagnostic: {name}") from exc
            results[name] = actual
        else:
            raise AssertionError(f"targeted runner fixture passed: {name}")
    return results


def _run_self_test(root: str | os.PathLike[str], executed: set[str] | None = None) -> int:
    expected = build_expected_ledger(root)
    validate_ledger(copy.deepcopy(expected), expected)
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("missing row", lambda item: item["candidateRows"].pop()),
        ("extra row", lambda item: item["candidateRows"].append(copy.deepcopy(item["candidateRows"][0]))),
        ("duplicate row", lambda item: item["candidateRows"].__setitem__(1, copy.deepcopy(item["candidateRows"][0]))),
        ("unowned defer", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "DEFER").__setitem__("owner", "")),
        ("partial pair", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible").__setitem__("disposition", "DEFER")),
        ("missing consumer", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["trackedCurrentConsumers"].clear()),
        ("missing provenance", lambda item: item["candidateRows"][0].__setitem__("sourceBlob", "f" * 40)),
        ("missing archive", lambda item: item["candidateRows"][0]["archive"].__setitem__("destination", "")),
        ("missing rollback", lambda item: item["candidateRows"][0]["recovery"].__setitem__("cutoverComplete", True)),
        ("unsafe path", lambda item: item["candidateRows"][0].__setitem__("path", "../hostile\nPASS")),
        ("unknown key", lambda item: item.__setitem__("unknown", True)),
        ("wrong commit", lambda item: item.__setitem__("candidateSourceCommit", "f" * 40)),
        ("terminal-only", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "DEFER").__setitem__("disposition", "eligible")),
        ("age-count-only", lambda item: item["counts"].__setitem__("eligible", 13)),
        ("ambiguous lineage", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["upstream"].__setitem__("state", "ambiguous")),
        ("missing lineage", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible").__setitem__("upstream", None)),
        ("current operational authority", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible").__setitem__("authority", "current-operational-procedure-authority")),
        ("missing reciprocal", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["reciprocalLinks"].clear()),
        ("broken spec link", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["specLinks"].clear()),
        ("missing closure", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["closureReferences"].clear()),
        ("wrong archive mirror", lambda item: item["candidateRows"][0]["archive"].__setitem__("destination", "docs/98.archive/04.execution/tasks/wrong.md")),
        ("missing inverse recipe", lambda item: item["candidateRows"][0]["recovery"].__setitem__("inverseBatchRecipe", "")),
        ("unsafe consumer", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["trackedCurrentConsumers"].append("_workspace/sentinel")),
        ("unsafe archive", lambda item: item["candidateRows"][0]["archive"].__setitem__("destination", "_workspace/sentinel")),
        ("unsafe reciprocal", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["reciprocalLinks"].__setitem__(0, "../sentinel")),
        ("unknown row key", lambda item: item["candidateRows"][0].__setitem__("unknown", True)),
        ("unknown-schema", lambda item: item.__setitem__("schemaVersion", 2)),
        ("wrong source object", lambda item: item["candidateRows"][0].__setitem__("sourceBlob", "not-an-oid")),
        ("wrong evidence commit", lambda item: item["candidateRows"][0].__setitem__("evidenceSnapshotCommit", "f" * 40)),
        ("missing control", lambda item: item["controls"].pop()),
        ("plan-only", lambda item: next(row for row in item["candidateRows"] if row["kind"] == "plan").__setitem__("pairKey", "plan-only-fixture")),
        ("task-only", lambda item: next(row for row in item["candidateRows"] if row["kind"] == "task").__setitem__("pairKey", "task-only-fixture")),
        ("body-link-only", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "DEFER").__setitem__("reason", "body-link-only")),
        ("ledger-only", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "DEFER").__setitem__("missingAxes", ["ledger-membership-only"])),
        ("missing-residue", lambda item: item["candidateRows"].pop()),
        ("extra-residue", lambda item: item["candidateRows"].append(copy.deepcopy(item["candidateRows"][0]))),
        ("duplicate-residue", lambda item: item["candidateRows"].__setitem__(2, copy.deepcopy(item["candidateRows"][0]))),
        ("extra-consumer", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["trackedCurrentConsumers"].append("docs/90.references/README.md")),
        ("missing-archive-route", lambda item: item["candidateRows"][0]["archive"].__setitem__("destination", "")),
        ("broken-reciprocal", lambda item: next(row for row in item["candidateRows"] if row["disposition"] == "eligible")["reciprocalLinks"].clear()),
        ("wrong-commit-object", lambda item: item.__setitem__("candidateSourceCommit", "0" * 40)),
        ("wrong-blob-object", lambda item: item["candidateRows"][0].__setitem__("sourceBlob", "0" * 40)),
        ("owner-key-gap", lambda item: next(row for row in item["candidateRows"] if row["authority"] == "owner-key-gap-resolved-partial-evidence").__setitem__("authority", "unresolved")),
        ("false-extra-axis", lambda item: next(row for row in item["candidateRows"] if row["authority"] == "owner-key-gap-resolved-partial-evidence")["missingAxes"].append("closure-evidence")),
    ]
    for name, mutate in cases:
        fixture = copy.deepcopy(expected); mutate(fixture)
        try:
            validate_ledger(fixture, expected)
        except EligibilityError:
            continue
        raise AssertionError(f"self-test negative passed: {name}")
    case_names = {name.replace(" ", "-") for name, _ in cases}
    for invalid in ("", "/absolute", "../parent", "docs//empty", "_workspace/sentinel", "hostile\npath"):
        try:
            validate_path(invalid)
        except EligibilityError:
            continue
        raise AssertionError("self-test unsafe path passed")
    try:
        _duplicate_keys([("same", 1), ("same", 2)])
    except EligibilityError:
        pass
    else:
        raise AssertionError("self-test duplicate JSON key passed")
    if _git_arguments_allowed(("show", "HEAD")):
        raise AssertionError("self-test hostile Git steering passed")
    case_names.update({"duplicate-json", "hostile-git-steering", "ignored-workspace-sentinel", "unsafe-path"})
    original_run = subprocess.run
    try:
        def _timeout(*_args: Any, **_kwargs: Any) -> Any:
            raise subprocess.TimeoutExpired("git", GIT_TIMEOUT_SECONDS)
        subprocess.run = _timeout  # type: ignore[assignment]
        try:
            _run_git(_root(root), ("cat-file", "-t", CANDIDATE_COMMIT))
        except EligibilityError:
            case_names.add("timeout")
        else:
            raise AssertionError("self-test timeout passed")
    finally:
        subprocess.run = original_run  # type: ignore[assignment]
    case_names.update(targeted_runner_case_results(root))
    if not REQUIRED_SELF_TEST_CASES <= case_names:
        raise AssertionError("self-test required case missing")
    if executed is not None:
        executed.update(case_names)
    return len(case_names) + 1


def self_test_case_names(root: str | os.PathLike[str]) -> frozenset[str]:
    executed: set[str] = set()
    _run_self_test(root, executed)
    return frozenset(executed)


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the ACER-002 fail-closed eligibility ledger.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--emit-ledger", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if arguments.emit_ledger:
            print(json.dumps(build_expected_ledger(arguments.root), indent=2, ensure_ascii=False) + "\n", end="")
        elif arguments.self_test:
            print(f"[PASS] active corpus eligibility self-test: {_run_self_test(arguments.root)} cases")
        else:
            counts = validate_active_corpus_eligibility(arguments.root)
            print("[PASS] active corpus eligibility: " + " ".join(f"{key}={value}" for key, value in counts.items()))
    except EligibilityError as exc:
        print(f"ERR {exc}", file=sys.stderr); return 1
    except (AssertionError, OSError, subprocess.SubprocessError):
        print("ERR ELIGIBILITY-SELF-TEST .", file=sys.stderr); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
