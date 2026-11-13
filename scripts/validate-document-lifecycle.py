#!/usr/bin/env python3
"""Validate registry-owned document lifecycle events against deterministic Git bases."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict
from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path, PurePosixPath
from types import MappingProxyType, ModuleType
from typing import Any, Callable, Mapping, Sequence

from document_contracts import (
    ROOT_FILES,
    TARGET_ROOTS,
    DocumentContractError,
    Registry,
    classify_path,
    enumerate_target_markdown,
    is_opaque_evaluation_output,
    verify_opaque_evaluation_output,
    load_registry,
    read_repository_text,
    task_criterion_ids,
    task_execution_issues,
    task_contract_issues,
    direct_parent,
    _typed_registry_from_mapping,
)
from document_lifecycle import (
    LifecycleDiagnostic,
    LifecycleDocument,
    LifecycleEvidenceContext,
    LifecycleEvidenceDocument,
    LifecycleRename,
    artifact_identity_reuse_diagnostics,
    compare_lifecycle,
    document_from_text,
    lifecycle_diagnostic_sort_key,
    lineage_retired_identities,
    local_contract_diagnostics,
    package_exit_diagnostics,
    validate_current_task_evidence,
    validate_snapshot_documents,
)
from document_authority import (
    AuthorityError,
    REGISTRY_PATH as CURRENT_REGISTRY_PATH,
    assert_staged_authority_matches_worktree,
    staged_authority_bytes,
)
from validation.repository.bounded_io import (
    BoundedOutputError,
    read_bytes as read_bounded_bytes,
    run as run_bounded,
)


COMPLETION_AUTHORITY_PATHS = (
    CURRENT_REGISTRY_PATH,
    PurePosixPath("docs/99.templates/contracts/document-profile.schema.json"),
    PurePosixPath("docs/99.templates/contracts/frontmatter.schema.json"),
)
OBJECT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
FIXED_GIT_ENVIRONMENT = {
    "GIT_AUTHOR_NAME": "Lifecycle Self Test",
    "GIT_AUTHOR_EMAIL": "lifecycle@example.invalid",
    "GIT_COMMITTER_NAME": "Lifecycle Self Test",
    "GIT_COMMITTER_EMAIL": "lifecycle@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_GRAFT_FILE": os.devnull,
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_TERMINAL_PROMPT": "0",
}
GIT_GLOBAL_ARGUMENTS = (
    "--no-replace-objects",
    "-c",
    "advice.graftFileDeprecated=false",
    "-c",
    "core.fsmonitor=false",
    "-c",
    f"core.hooksPath={os.devnull}",
    "-c",
    "user.name=Lifecycle Self Test",
    "-c",
    "user.email=lifecycle@example.invalid",
    "-c",
    "diff.renameLimit=0",
    "-c",
    "diff.renames=true",
)
GIT_CAPTURE_MAX_BYTES = 2 * 1024 * 1024
GIT_TIMEOUT_SECONDS = 10.0
GIT_SIZE_OUTPUT_MAX_BYTES = 64
DOCUMENT_BLOB_MAX_BYTES = 1024 * 1024
CUMULATIVE_HISTORY_MAX_COMMITS = 256
# These are execution-safety limits for one validation invocation. They are
# deliberately not a repository corpus or document-count policy.
CUMULATIVE_HISTORY_MAX_CANDIDATES = 32
CUMULATIVE_HISTORY_MAX_CANDIDATE_EVENTS = 512
CUMULATIVE_HISTORY_CACHE_MAX_SNAPSHOTS = 4
CUMULATIVE_HISTORY_CACHE_MAX_EVIDENCE = 2
CUMULATIVE_HISTORY_MAX_SNAPSHOT_BYTES = 4 * 1024 * 1024
CUMULATIVE_HISTORY_MAX_SNAPSHOT_WORK_BYTES = 16 * 1024 * 1024
CUMULATIVE_HISTORY_MAX_SNAPSHOT_PATHS = 4_096
CUMULATIVE_HISTORY_MAX_SNAPSHOT_OBJECTS = 4_096


class InvocationError(ValueError):
    """Invalid CLI, ref, base, Git object, or include-path provenance."""


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser that returns deterministic exit 2 through ``main``."""


@dataclass(frozen=True)
class Change:
    kind: str
    path: PurePosixPath
    old_path: PurePosixPath | None = None

    @property
    def paths(self) -> tuple[PurePosixPath, ...]:
        return (self.old_path, self.path) if self.old_path is not None else (self.path,)


_LINK_VALIDATOR_MODULE: ModuleType | None = None


def _link_validator_module() -> ModuleType:
    """Load the canonical CommonMark evidence adapter once by script path."""

    global _LINK_VALIDATOR_MODULE
    if _LINK_VALIDATOR_MODULE is not None:
        return _LINK_VALIDATOR_MODULE
    path = Path(__file__).with_name("validate-links-and-owners.py")
    name = "_document_lifecycle_link_validator"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise InvocationError("canonical link validator could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    _LINK_VALIDATOR_MODULE = module
    return module


def frontmatter_mapping(text: str) -> Mapping[str, object]:
    return _link_validator_module().frontmatter_mapping(text)


@lru_cache(maxsize=1)
def _load_canonical_markdown_module() -> ModuleType:
    """Use the Stage99 document owner for parsing and registry-selected validation."""

    script_path = (
        Path(__file__).resolve(strict=True).with_name("validate-markdown-profiles.py")
    )
    name = "_document_lifecycle_markdown_validator"
    spec = importlib.util.spec_from_file_location(name, script_path)
    if spec is None or spec.loader is None:
        raise InvocationError("canonical Markdown owner is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    scripts_path = str(script_path.parent)
    inserted = scripts_path not in sys.path
    if inserted:
        sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
        if inserted:
            sys.path.remove(scripts_path)
    return module


@contextlib.contextmanager
def _git_environment_scope() -> Iterator[None]:
    original = {
        key: value for key, value in os.environ.items() if key.startswith("GIT_")
    }
    for key in tuple(os.environ):
        if key.startswith("GIT_"):
            del os.environ[key]
    os.environ.update(FIXED_GIT_ENVIRONMENT)
    try:
        yield
    finally:
        for key in tuple(os.environ):
            if key.startswith("GIT_"):
                del os.environ[key]
        os.environ.update(original)


def _safe_git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_GRAFT_FILE": os.devnull,
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
        }
    )
    return environment


def _git_process(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    output_limit: int = GIT_CAPTURE_MAX_BYTES,
) -> subprocess.CompletedProcess[bytes]:
    try:
        completed = run_bounded(
            [
                "git",
                "--no-replace-objects",
                "--literal-pathspecs",
                "-C",
                str(root),
                *GIT_GLOBAL_ARGUMENTS,
                *arguments,
            ],
            timeout=GIT_TIMEOUT_SECONDS,
            stdout_limit=output_limit,
            stderr_limit=GIT_CAPTURE_MAX_BYTES,
            env=_safe_git_environment(),
            input_bytes=input_bytes,
        )
    except (BoundedOutputError, OSError, subprocess.TimeoutExpired) as exc:
        raise InvocationError(
            f"bounded git provenance failed for "
            f"{arguments[0] if arguments else 'command'}"
        ) from exc
    # Git diagnostics on stderr never decide a provenance result.
    return subprocess.CompletedProcess(
        completed.args, completed.returncode, completed.stdout, b""
    )


def _run_git(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    allow_stderr: bool = False,
    output_limit: int = GIT_CAPTURE_MAX_BYTES,
) -> bytes:
    completed = _git_process(
        root,
        arguments,
        input_bytes=input_bytes,
        output_limit=output_limit,
    )
    if completed.returncode != 0 or (completed.stderr and not allow_stderr):
        raise InvocationError(
            f"git provenance failed for {arguments[0] if arguments else 'command'}"
        )
    return completed.stdout


def _verify_repository_root(root: Path) -> None:
    resolved = root.resolve()
    top_level = _run_git(root, ("rev-parse", "--show-toplevel"))
    try:
        reported = Path(top_level.decode("utf-8").strip()).resolve()
    except UnicodeDecodeError as exc:
        raise InvocationError("Git returned a non-UTF-8 repository root") from exc
    if reported != resolved:
        raise InvocationError("--root must equal the sanitized Git worktree root")
    if _run_git(root, ("rev-parse", "--is-inside-work-tree")).strip() != b"true":
        raise InvocationError("--root is not inside a Git worktree")
    if _run_git(root, ("rev-parse", "--is-bare-repository")).strip() != b"false":
        raise InvocationError("bare repositories are not lifecycle worktrees")


def _decode_path(raw: bytes) -> PurePosixPath:
    try:
        value = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvocationError("Git returned a non-UTF-8 path") from exc
    return _normalize_path(value)


def _normalize_path(value: str) -> PurePosixPath:
    if (
        not value
        or value == "."
        or value.startswith("./")
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise InvocationError(f"noncanonical repository path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise InvocationError(f"noncanonical repository path: {value!r}")
    return path


def _approved_markdown(path: PurePosixPath) -> bool:
    if path.suffix != ".md" or not path.parts:
        return False
    if path.as_posix() == "RTK.md" or path.parts[0] == ".worktrees":
        return False
    if path.parts[:2] == ("docs", "98.archive"):
        return False  # Archive files are not governed documents.
    return path.as_posix() in ROOT_FILES or path.parts[0] in TARGET_ROOTS


def _normalize_include_paths(
    registry: Registry, values: Sequence[str]
) -> tuple[PurePosixPath, ...]:
    result: list[PurePosixPath] = []
    seen: set[PurePosixPath] = set()
    for value in values:
        path = _normalize_path(value)
        if path in seen:
            raise InvocationError(f"duplicate include path: {path.as_posix()}")
        if not _approved_markdown(path):
            raise InvocationError(
                f"include path is not governed target Markdown: {path.as_posix()}"
            )
        try:
            classify_path(registry, path)
        except DocumentContractError as exc:
            raise InvocationError(
                f"include path has no unique current registry profile: {path.as_posix()}"
            ) from exc
        seen.add(path)
        result.append(path)
    return tuple(result)


def _resolve_commit(root: Path, reference: str, label: str) -> str:
    if not reference:
        raise InvocationError(f"{label} must not be empty")
    matching_refs = _git_process(
        root,
        ("show-ref", "--", reference),
        output_limit=512,
    )
    completed = _git_process(
        root,
        ("rev-parse", "--verify", "--end-of-options", reference),
        output_limit=GIT_SIZE_OUTPUT_MAX_BYTES,
    )
    lines = completed.stdout.decode("ascii", errors="ignore").splitlines()
    ref_lines = matching_refs.stdout.splitlines()
    if (
        matching_refs.returncode not in {0, 1}
        or len(ref_lines) > 1
        or completed.returncode != 0
        or len(lines) != 1
        or OBJECT_ID.fullmatch(lines[0]) is None
    ):
        raise InvocationError(f"{label} is missing or ambiguous")
    object_type = _run_git(root, ("cat-file", "-t", lines[0])).decode("ascii").strip()
    if object_type != "commit":
        raise InvocationError(f"{label} directly resolves to a non-commit object")
    return lines[0]


def _merge_base(root: Path, base_commit: str, to_commit: str) -> str:
    output = _run_git(root, ("merge-base", "--all", base_commit, to_commit))
    bases = output.decode("ascii", errors="ignore").splitlines()
    if len(bases) != 1 or OBJECT_ID.fullmatch(bases[0]) is None:
        raise InvocationError("CI refs do not have exactly one commit merge base")
    return bases[0]


def _parse_changes(raw: bytes) -> tuple[Change, ...]:
    records = raw.split(b"\0")
    if not records or records[-1] != b"":
        raise InvocationError("Git name-status output is not NUL terminated")
    changes: list[Change] = []
    cursor = 0
    while cursor < len(records) - 1:
        status_raw = records[cursor]
        cursor += 1
        try:
            status = status_raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise InvocationError("Git returned a non-ASCII change status") from exc
        if status.startswith("R") and status[1:] == "100":
            if cursor + 1 >= len(records) - 1:
                raise InvocationError("Git rename record is truncated")
            old_path = _decode_path(records[cursor])
            new_path = _decode_path(records[cursor + 1])
            cursor += 2
            changes.append(Change("R", new_path, old_path))
            continue
        if status not in {"A", "D", "M", "T"}:
            raise InvocationError(
                f"unsupported or unmerged Git change status: {status}"
            )
        if cursor >= len(records) - 1:
            raise InvocationError("Git change record is truncated")
        path = _decode_path(records[cursor])
        cursor += 1
        changes.append(Change("M" if status == "T" else status, path))
    return tuple(changes)


def _staged_changes(root: Path) -> tuple[Change, ...]:
    return _parse_changes(
        _run_git(
            root,
            (
                "diff",
                "--cached",
                "--no-ext-diff",
                "--no-textconv",
                "--ignore-submodules=none",
                "--name-status",
                "-z",
                "--find-renames=100%",
                "-l0",
                "HEAD",
                "--",
            ),
        )
    )


def _tree_changes(root: Path, base: str, proposed: str) -> tuple[Change, ...]:
    return _parse_changes(
        _run_git(
            root,
            (
                "diff",
                "--no-ext-diff",
                "--no-textconv",
                "--ignore-submodules=none",
                "--name-status",
                "-z",
                "--find-renames=100%",
                "-l0",
                base,
                proposed,
                "--",
            ),
        )
    )


def _tree_blob_oid(root: Path, commit: str, path: PurePosixPath) -> str | None:
    raw = _run_git(root, ("ls-tree", "-z", commit, "--", path.as_posix()))
    if raw == b"":
        return None
    records = raw.split(b"\0")
    if records[-1] != b"" or len(records) != 2:
        raise InvocationError(f"ambiguous tree path: {path.as_posix()}")
    try:
        header, raw_path = records[0].split(b"\t", 1)
        mode, object_type, oid = header.split(b" ", 2)
    except ValueError as exc:
        raise InvocationError("malformed git ls-tree output") from exc
    if (
        _decode_path(raw_path) != path
        or mode not in {b"100644", b"100755"}
        or object_type != b"blob"
        or OBJECT_ID.fullmatch(oid.decode("ascii", errors="ignore")) is None
    ):
        raise InvocationError(f"tree path is not one regular blob: {path.as_posix()}")
    return oid.decode("ascii")


def _tree_blob_map(root: Path, commit: str) -> Mapping[PurePosixPath, str]:
    raw = _run_git(root, ("ls-tree", "-r", "-z", "--full-tree", commit))
    records = raw.split(b"\0")
    if not records or records[-1] != b"":
        raise InvocationError("Git tree inventory is not NUL terminated")
    result: dict[PurePosixPath, str] = {}
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, object_type, oid = header.split(b" ", 2)
        except ValueError as exc:
            raise InvocationError("malformed Git tree inventory") from exc
        if mode not in {b"100644", b"100755"} or object_type != b"blob":
            continue
        path = _decode_path(raw_path)
        if not _approved_markdown(path):
            continue
        value = oid.decode("ascii", errors="ignore")
        if OBJECT_ID.fullmatch(value) is None or path in result:
            raise InvocationError("ambiguous regular Markdown tree entry")
        result[path] = value
    return MappingProxyType(result)


def _index_blob_map(root: Path) -> Mapping[PurePosixPath, str]:
    raw = _run_git(root, ("ls-files", "--stage", "-z"))
    records = raw.split(b"\0")
    if not records or records[-1] != b"":
        raise InvocationError("Git index inventory is not NUL terminated")
    result: dict[PurePosixPath, str] = {}
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, oid, stage = header.split(b" ", 2)
        except ValueError as exc:
            raise InvocationError("malformed Git index inventory") from exc
        path = _decode_path(raw_path)
        if not _approved_markdown(path):
            continue
        if mode not in {b"100644", b"100755"} or stage != b"0":
            raise InvocationError(
                f"proposed Markdown is not one stage-zero regular blob: {path}"
            )
        value = oid.decode("ascii", errors="ignore")
        if OBJECT_ID.fullmatch(value) is None or path in result:
            raise InvocationError("ambiguous regular Markdown index entry")
        result[path] = value
    return MappingProxyType(result)


def _blob_text(
    root: Path,
    oid: str | None,
    path: PurePosixPath,
) -> str | None:
    if oid is None:
        return None
    raw = _blob_bytes(root, oid)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvocationError(f"document blob is not UTF-8: {path.as_posix()}") from exc


def _blob_bytes(
    root: Path,
    oid: str,
    *,
    max_bytes: int = DOCUMENT_BLOB_MAX_BYTES,
) -> bytes:
    """Read one exact Git blob without decoding or worktree substitution."""

    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes < 0
        or max_bytes > DOCUMENT_BLOB_MAX_BYTES
    ):
        raise InvocationError("Git blob byte budget is invalid")
    size_bytes = _run_git(
        root,
        ("cat-file", "-s", oid),
        output_limit=GIT_SIZE_OUTPUT_MAX_BYTES,
    )
    try:
        size = int(size_bytes.decode("ascii", errors="strict").strip())
    except (UnicodeDecodeError, ValueError) as exc:
        raise InvocationError("Git blob size is malformed") from exc
    if size < 0 or size > max_bytes:
        raise InvocationError("Git blob exceeds its byte budget")
    payload = _run_git(
        root,
        ("cat-file", "blob", oid),
        output_limit=max_bytes,
    )
    if len(payload) != size:
        raise InvocationError("Git blob size changed during bounded read")
    return payload


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise InvocationError("registry blob contains a duplicate JSON key")
        result[key] = value
    return result


def _registry_blob(
    root: Path,
    oid: str | None,
) -> Mapping[str, object]:
    text = _blob_text(root, oid, PurePosixPath(CURRENT_REGISTRY_PATH))
    if text is None:
        raise InvocationError("comparison snapshot lacks the document registry")
    try:
        loaded = json.loads(text, object_pairs_hook=_unique_json_object)
    except (json.JSONDecodeError, InvocationError) as exc:
        raise InvocationError("comparison registry blob is invalid JSON") from exc
    if not isinstance(loaded, dict):
        raise InvocationError("comparison registry blob is not an object")
    return MappingProxyType(loaded)


def _snapshot_projection(
    root: Path,
    registry: Registry,
    blobs: Mapping[PurePosixPath, str],
    *,
    reused_texts: Mapping[PurePosixPath, str] | None = None,
) -> tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]]:
    documents: dict[PurePosixPath, LifecycleDocument] = {}
    texts: dict[PurePosixPath, str] = {}
    for path in sorted(blobs, key=PurePosixPath.as_posix):
        try:
            opaque = is_opaque_evaluation_output(registry, path)
        except DocumentContractError:
            opaque = False
        if opaque:
            _blob_bytes(root, blobs[path])
        text = (
            ""
            if opaque
            else reused_texts.get(path)
            if reused_texts is not None
            else None
        )
        if text is None:
            text = _blob_text(root, blobs[path], path)
        assert text is not None
        texts[path] = text
        try:
            documents[path] = document_from_text(
                registry,
                path,
                text,
            )
        except DocumentContractError:
            documents[path] = LifecycleDocument(
                path=path,
                profile_id="unclassified",
                status=None,
                state_issue="no unique current registry profile",
            )
    return MappingProxyType(documents), MappingProxyType(texts)


def _body_text(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    closing = text.find("\n---\n", 4)
    return text if closing < 0 else text[closing + 5 :]


def _local_plan_task_contract_issues(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    base_texts: Mapping[PurePosixPath, str],
    proposed_texts: Mapping[PurePosixPath, str],
) -> tuple[tuple[PurePosixPath, str, str, str, str], ...]:
    """Check only this local adopter's changed Plan and execution inputs."""

    profiles = {profile.profile_id: profile for profile in registry.profiles}
    plan_profile = profiles.get("sdlc/plan")
    if plan_profile is None or "Promotion" not in plan_profile.headings.allowed:
        return ()  # Older committed registries did not own this local extension.
    adapter = _link_validator_module()
    issues: list[tuple[PurePosixPath, str, str, str, str]] = []

    def issue(
        path: PurePosixPath, profile: str, rule: str, expected: str, observed: str
    ) -> None:
        issues.append((path, profile, rule, expected, observed))

    def promotion_valid(path: PurePosixPath, text: str) -> bool:
        """Check receipt structure and current owner; Where semantics need review."""
        section = adapter._exact_heading_section(text, "## Promotion")
        visible = adapter._visible_markdown(section or "")
        table = adapter._first_visible_table(visible)
        table_count = sum(
            bool(re.fullmatch(r"\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*", line))
            for line in visible.splitlines()
        )
        if (
            table_count != 1
            or table is None
            or table[0] != ["Durable contract", "Promoted to", "Where"]
        ):
            return False
        rows = table[1]
        if not rows or any(len(row) != 3 for row in rows):
            return False
        if len(rows) == 1 and rows[0][0] == "none":
            return rows[0] == ["none", "none", "No durable contract was introduced"]
        if any(
            any(
                not cell.strip()
                or cell.strip().casefold() in {"none", "pending", "tbd"}
                for cell in row
            )
            for row in rows
        ):
            return False
        seen: set[tuple[str, str]] = set()
        for contract, promoted_to, where in rows:
            links = adapter._extract_links(promoted_to, definitions_text=text)
            if len(links) != 1 or not where.strip():
                return False
            kind, target = adapter._local_destination(path, links[0])
            if kind not in {"local", "anchor"} or target is None:
                return False
            current_owner = target.parts[:1] == (".agents",) or target.parts[:2] in {
                ("docs", "01.requirements"),
                ("docs", "02.architecture"),
                ("docs", "05.operations"),
            }
            if not current_owner or target.suffix != ".md":
                return False
            owner = proposed_documents.get(target)
            if (
                owner is None
                or owner.profile_id == "unclassified"
                or owner.state_issue is not None
                or owner.status not in {"approved", "active", "accepted"}
            ):
                return False
            identity = (contract.strip(), target.as_posix())
            if identity in seen:
                return False
            seen.add(identity)
        return True

    for path, plan in proposed_documents.items():
        if (
            plan.profile_id != "sdlc/plan"
            or path.parts[:2] != ("docs", "03.specs")
            or plan.status == "cancelled"
            or base_texts.get(path) == proposed_texts[path]
        ):
            continue
        constraints = adapter._exact_heading_section(
            proposed_texts[path], "## Global Constraints"
        )
        visible_constraints = adapter._visible_markdown(constraints or "").strip()
        spec_path, spec_id = direct_parent(path, "sdlc/plan") or (None, None)
        spec = proposed_documents.get(spec_path) if spec_path else None
        linked_spec = any(
            adapter._local_destination(path, link)[1] == spec_path
            for link in adapter._extract_links(
                visible_constraints, definitions_text=proposed_texts[path]
            )
        )
        if (
            not visible_constraints
            or spec is None
            or spec.profile_id != "sdlc/spec"
            or spec.artifact_id != spec_id
            or frontmatter_mapping(proposed_texts[path]).get("parent_ids") != [spec_id]
            or not linked_spec
        ):
            issue(
                path,
                "sdlc/plan",
                "PLAN-GLOBAL-CONSTRAINTS",
                "one substantive Global Constraints section",
                "changed Plan has no substantive shared constraints",
            )
        if not promotion_valid(path, proposed_texts[path]):
            issue(
                path,
                "sdlc/plan",
                "PLAN-PROMOTION",
                "one Promotion table with a current .agents/ or Stage 01/02/05 owner or explicit none",
                "changed Plan has no valid durable-owner receipt",
            )

    for path, task in proposed_documents.items():
        if (
            task.profile_id != "sdlc/task"
            or path.parts[:2] != ("docs", "03.specs")
            or base_texts.get(path) == proposed_texts[path]
        ):
            continue
        task_profile = profiles.get("sdlc/task")
        rows = (
            adapter._body_contract_rows(proposed_texts[path], task_profile) or ()
            if task_profile is not None
            else ()
        )
        active = task.status in {"ready", "in-progress", "completed"} or any(
            row.get("Status", "").strip() in {"ready", "in-progress", "completed"}
            for row in rows
        )
        base_evidence = {
            row.get("Evidence", "").strip(): row
            for row in adapter.task_base_evidence_rows(base_texts.get(path, "")) or ()
        }
        active = active or any(
            row.get("Result", "").strip() == "PASS"
            and base_evidence.get(row.get("Evidence", "").strip()) != row
            for row in adapter.task_base_evidence_rows(proposed_texts[path]) or ()
        )
        if not active:
            continue
        plan_path, plan_id = direct_parent(path, "sdlc/task") or (None, None)
        spec_path = path.parent.parent / "spec.md"
        plan = proposed_documents.get(plan_path) if plan_path else None
        spec = proposed_documents.get(spec_path)
        task_metadata = frontmatter_mapping(proposed_texts[path])
        plan_metadata = (
            frontmatter_mapping(proposed_texts[plan_path])
            if plan_path in proposed_texts
            else {}
        )
        prior_task = base_documents.get(path)
        prior_rows = (
            adapter._body_contract_rows(base_texts[path], task_profile) or ()
            if prior_task is not None and task_profile is not None
            else ()
        )
        same_existing_work = bool(
            prior_task is not None
            and prior_task.profile_id == "sdlc/task"
            and prior_task.artifact_id == task.artifact_id
            and prior_task.status == "completed"
            and prior_rows
            and tuple(
                (
                    row.get("ID"),
                    row.get("Upstream criterion"),
                    row.get("Work item"),
                    row.get("Owner"),
                )
                for row in prior_rows
            )
            == tuple(
                (
                    row.get("ID"),
                    row.get("Upstream criterion"),
                    row.get("Work item"),
                    row.get("Owner"),
                )
                for row in rows
            )
        )

        def approved_parent(
            parent_path: PurePosixPath | None, parent: LifecycleDocument | None
        ) -> bool:
            if parent_path is None or parent is None:
                return False
            if parent.status == "approved":
                return True
            old = base_documents.get(parent_path)
            return bool(
                same_existing_work
                and parent.status == "completed"
                and old is not None
                and old.profile_id == parent.profile_id
                and old.artifact_id == parent.artifact_id
                and old.status == "completed"
                and base_texts.get(parent_path) == proposed_texts.get(parent_path)
            )

        expected_spec = direct_parent(plan_path, "sdlc/plan") if plan_path else None
        valid = bool(
            plan_path is not None
            and plan is not None
            and plan.profile_id == "sdlc/plan"
            and plan.artifact_id == plan_id
            and task_metadata.get("parent_ids") == [plan_id]
            and expected_spec == (spec_path, spec.artifact_id if spec else None)
            and plan_metadata.get("parent_ids") == [spec.artifact_id if spec else None]
            and spec is not None
            and spec.profile_id == "sdlc/spec"
            and approved_parent(plan_path, plan)
            and approved_parent(spec_path, spec)
        )
        if not valid:
            issue(
                path,
                "sdlc/task",
                "TASK-PARENT-APPROVAL",
                "typed same-package approved Spec and Plan before Task execution",
                "changed executable Task lacks approved parent identity or status",
            )
    return tuple(issues)


def _receipt_object(value: str, keys: frozenset[str]) -> dict[str, object] | None:
    """Parse one bounded Task receipt without admitting duplicate JSON keys."""

    if len(value.encode("utf-8")) > 4096:
        return None

    def unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, item in pairs:
            if key in result:
                raise ValueError("duplicate receipt key")
            result[key] = item
        return result

    try:
        parsed = json.loads(value, object_pairs_hook=unique)
    except (ValueError, TypeError):
        return None
    return parsed if isinstance(parsed, dict) and parsed.keys() == keys else None


def _new_approval_receipts(
    task_path: PurePosixPath,
    views: Mapping[PurePosixPath, LifecycleEvidenceDocument],
    base_texts: Mapping[PurePosixPath, str],
    spec_hash: str,
    plan_hash: str,
    spec_id: str,
    plan_id: str,
) -> bool:
    """Check structure and exact review bytes; actor truth remains human-owned."""

    view = views.get(task_path)
    if view is None or view.document.profile_id != "sdlc/task":
        return False
    rows = [dict(cells) for cells in view.task_evidence_rows]
    old_rows = (
        _link_validator_module().task_base_evidence_rows(base_texts[task_path])
        if task_path in base_texts
        else []
    )
    if old_rows is None:
        return False
    approval_keys = frozenset(
        {
            "actor",
            "approval_ref",
            "review_ref",
            "scope",
            "reviewed_spec_sha256",
            "reviewed_plan_sha256",
            "validity",
            "revocation",
        }
    )
    old_ids = {row.get("Evidence", "").strip() for row in old_rows}
    current_approvals = [
        (row, receipt)
        for row in rows
        if row.get("Check", "").strip() == "Spec/Plan first-record approval"
        and row.get("Evidence", "").strip() not in old_ids
        for receipt in (_receipt_object(row.get("Input", ""), approval_keys),)
        if receipt is not None
        and receipt["reviewed_spec_sha256"] == spec_hash
        and receipt["reviewed_plan_sha256"] == plan_hash
    ]
    if len(current_approvals) != 1:
        return False
    approval, approval_input = current_approvals[0]
    if not isinstance(approval_input["review_ref"], str):
        return False
    reviews = [
        row
        for row in rows
        if row.get("Check", "").strip() == "Independent semantic review"
        and row.get("Evidence", "").strip() == approval_input["review_ref"]
    ]
    if len(reviews) != 1:
        return False
    review = reviews[0]
    for row in (review, approval):
        if any(
            row.get(key, "").strip() != value
            for key, value in (
                ("Result", "PASS"),
                ("Required", "yes"),
                ("Resolves", "none"),
            )
        ):
            return False
    review_id = review.get("Evidence", "").strip()
    approval_id = approval.get("Evidence", "").strip()
    evidence_id = r"EVD-(?:[A-Z0-9]+-)*[0-9]{3}"
    if not all(re.fullmatch(evidence_id, item) for item in (review_id, approval_id)):
        return False
    if (
        review_id == approval_id
        or sum(row.get("Evidence", "").strip() == review_id for row in rows) != 1
        or sum(row.get("Evidence", "").strip() == approval_id for row in rows) != 1
        or any(
            row.get("Evidence", "").strip() in {review_id, approval_id}
            for row in old_rows
        )
    ):
        return False
    if rows.index(review) >= rows.index(approval):
        return False
    review_input = _receipt_object(
        review.get("Input", ""), frozenset({"spec_sha256", "plan_sha256"})
    )
    if review_input != {"spec_sha256": spec_hash, "plan_sha256": plan_hash}:
        return False
    approval_ref = approval_input["approval_ref"]
    return bool(
        approval_input["actor"] == "user"
        and isinstance(approval_ref, str)
        and approval_ref.strip() == approval_ref
        and approval_ref.casefold() not in {"", "none", "pending", "tbd", "todo"}
        and "{{" not in approval_ref
        and "}}" not in approval_ref
        and approval_input["review_ref"] == review_id
        and approval_input["scope"] == [spec_id, plan_id]
        and approval_input["reviewed_spec_sha256"] == spec_hash
        and approval_input["reviewed_plan_sha256"] == plan_hash
        and approval_input["validity"] == "confirmed"
        and approval_input["revocation"] == "none"
    )


def _approved_initial_paths(
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_texts: Mapping[PurePosixPath, str],
    base_texts: Mapping[PurePosixPath, str],
    views: Mapping[PurePosixPath, LifecycleEvidenceDocument],
) -> frozenset[PurePosixPath]:
    """Admit only one newly approved, typed package pair per exact snapshot."""

    admitted: set[PurePosixPath] = set()
    for spec_path, spec in proposed_documents.items():
        if spec.profile_id != "sdlc/spec" or spec.status != "approved":
            continue
        package = spec_path.parent
        if spec_path != package / "spec.md" or spec_path in base_documents:
            continue
        plan_path = package / "plan.md"
        plan = proposed_documents.get(plan_path)
        if (
            plan is None
            or plan.profile_id != "sdlc/plan"
            or plan.status != "approved"
            or plan_path in base_documents
        ):
            continue
        expected = direct_parent(plan_path, "sdlc/plan")
        if expected is None or expected[0] != spec_path:
            continue
        spec_id = expected[1]
        plan_id = f"{spec_id}-PLAN-0001"
        try:
            spec_metadata = frontmatter_mapping(proposed_texts[spec_path])
            plan_metadata = frontmatter_mapping(proposed_texts[plan_path])
        except (KeyError, ValueError, TypeError):
            continue
        if (
            spec_metadata.get("artifact_id") != spec_id
            or plan_metadata.get("artifact_id") != plan_id
            or plan_metadata.get("parent_ids") != [spec_id]
            or (spec.artifact_id is not None and spec.artifact_id != spec_id)
            or (plan.artifact_id is not None and plan.artifact_id != plan_id)
        ):
            continue
        spec_hash = hashlib.sha256(
            proposed_texts[spec_path].encode("utf-8")
        ).hexdigest()
        plan_hash = hashlib.sha256(
            proposed_texts[plan_path].encode("utf-8")
        ).hexdigest()
        for task_path, task in proposed_documents.items():
            if task.profile_id != "sdlc/task" or task_path.parent != package / "tasks":
                continue
            task_parent = direct_parent(task_path, "sdlc/task")
            if task_parent != (plan_path, plan_id):
                continue
            try:
                task_metadata = frontmatter_mapping(proposed_texts[task_path])
            except (KeyError, ValueError, TypeError):
                continue
            if task_metadata.get("parent_ids") != [plan_id]:
                continue
            if _new_approval_receipts(
                task_path, views, base_texts, spec_hash, plan_hash, spec_id, plan_id
            ):
                admitted.update((spec_path, plan_path))
                break
    return frozenset(admitted)


def _evidence_context(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    base_texts: Mapping[PurePosixPath, str],
    proposed_texts: Mapping[PurePosixPath, str],
) -> LifecycleEvidenceContext:
    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    snapshot_profiles = MappingProxyType(
        {path: document.profile_id for path, document in proposed_documents.items()}
    )
    adapter = _link_validator_module()
    views: dict[PurePosixPath, LifecycleEvidenceDocument] = {}
    base_task_rows: dict[PurePosixPath, tuple[tuple[tuple[str, str], ...], ...]] = {}
    base_task_evidence_rows: dict[
        PurePosixPath, tuple[tuple[tuple[str, str], ...], ...]
    ] = {}
    for path, document in base_documents.items():
        profile = profile_map.get(document.profile_id)
        if (
            document.profile_id == "sdlc/task"
            and profile is not None
            and profile.body_contract is not None
            and profile.body_contract.task_execution is not None
            and path in proposed_documents
        ):
            rows = adapter.task_base_rows(base_texts[path], profile)
            if rows:
                base_task_rows[path] = rows
            evidence = adapter.task_base_evidence_rows(base_texts[path])
            if evidence:
                base_task_evidence_rows[path] = tuple(
                    tuple(row.items()) for row in evidence
                )
    for path, document in proposed_documents.items():
        profile = profile_map.get(document.profile_id)
        if profile is None or profile.body_contract is None:
            views[path] = LifecycleEvidenceDocument(
                document=document,
                all_local_links=(),
                relationship_links=(),
                unresolved_relationship_links=(),
                body_table_links=(),
                relationship_section_valid=profile is not None,
                body_contract_valid=profile is not None,
                task_terminal_evidence_valid=False,
            )
            continue
        rendered = adapter.lifecycle_markdown_evidence(
            path,
            proposed_texts[path],
            profile,
            snapshot_profiles,
        )
        unresolved_links = rendered.unresolved_relationship_links
        views[path] = LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=unresolved_links,
            body_table_links=rendered.body_table_links,
            relationship_section_valid=rendered.relationship_section_valid,
            body_contract_valid=rendered.body_contract_valid,
            task_terminal_evidence_valid=rendered.task_terminal_evidence_valid,
            body_rows=rendered.body_rows,
            task_evidence_rows=(
                tuple(
                    tuple(row.items())
                    for row in adapter.task_base_evidence_rows(proposed_texts[path])
                )
                if document.profile_id == "sdlc/task"
                and adapter.task_base_evidence_rows(proposed_texts[path]) is not None
                else ()
            ),
        )

    task_contract = profile_map.get("sdlc/task")
    for path, view in tuple(views.items()):
        if (
            view.document.profile_id != "sdlc/task"
            or view.document.status != "cancelled"
        ):
            continue
        try:
            metadata = frontmatter_mapping(proposed_texts[path])
        except (ValueError, TypeError):
            metadata = {}
        criteria = {
            criterion
            for cells in view.body_rows
            for criterion in (
                task_criterion_ids(dict(cells)["Upstream criterion"]) or ()
            )
        }
        plan_path = path.parent.parent / "plan.md"
        plan = proposed_documents.get(plan_path)
        plan_profile = profile_map.get("sdlc/plan")
        plan_rows = (
            adapter._body_contract_rows(proposed_texts[plan_path], plan_profile)
            if plan is not None and plan_profile is not None
            else None
        )
        allocations: dict[str, set[PurePosixPath]] = {}
        for row in plan_rows or ():
            links = adapter._extract_links(
                row["Task"], definitions_text=proposed_texts[plan_path]
            )
            targets = [adapter._local_destination(plan_path, link)[1] for link in links]
            for criterion in task_criterion_ids(row["Criteria"]) or ():
                allocations.setdefault(criterion, set()).update(
                    target for target in targets if target is not None
                )
        plan_successors = {
            criterion: allocations.get(criterion, set()) - {path}
            for criterion in criteria
        }
        plan_handoff = bool(criteria) and all(
            path not in allocations.get(criterion, set()) and plan_successors[criterion]
            for criterion in criteria
        )
        cancellation = metadata.get("cancellation")
        authorization = (
            cancellation.get("authorization_ref")
            if isinstance(cancellation, dict)
            else None
        )
        disposition = (
            cancellation.get("criteria_disposition")
            if isinstance(cancellation, dict)
            else None
        )
        plan_authorized = bool(
            plan_handoff and plan is not None and authorization == plan.artifact_id
        )
        spec_path = path.parent.parent / "spec.md"
        spec = proposed_documents.get(spec_path)
        try:
            spec_metadata = frontmatter_mapping(proposed_texts[spec_path])
        except (KeyError, ValueError, TypeError):
            spec_metadata = {}
        spec_cancellation = spec_metadata.get("cancellation")

        def named_criteria(value: object) -> frozenset[str]:
            if not isinstance(value, str):
                return frozenset()
            return frozenset(
                re.findall(
                    r"(?<![\w-])VAL-[A-Z0-9-]+-[0-9]{3}(?![\w-])",
                    value,
                )
            )

        def concrete(value: object) -> bool:
            return (
                isinstance(value, str)
                and bool(value.strip())
                and value.strip().casefold()
                not in {"tbd", "todo", "pending", "n/a", "na", "none"}
            )

        scope_authorized = bool(
            spec is not None
            and spec.status == "cancelled"
            and authorization == spec.artifact_id
            and isinstance(spec_cancellation, dict)
            and criteria <= named_criteria(disposition)
        )
        acceptance_rows = (
            adapter.task_acceptance_rows(
                proposed_texts[path], task_contract.body_contract.task_execution
            )
            if task_contract is not None
            and task_contract.body_contract is not None
            and task_contract.body_contract.task_execution is not None
            else None
        )
        waived = {
            criterion
            for row in acceptance_rows or ()
            if row["Acceptance"].strip() == "not-required"
            for criterion in (task_criterion_ids(row["Criterion"]) or ())
        }
        waiver_authorized = bool(
            scope_authorized
            and waived
            and isinstance(spec_cancellation, dict)
            and waived <= named_criteria(spec_cancellation.get("criteria_disposition"))
            and all(
                concrete(spec_cancellation.get(key))
                for key in ("reason", "authorization_ref")
            )
        )
        valid = bool(
            view.body_contract_valid
            and isinstance(cancellation, dict)
            and concrete(cancellation.get("reason"))
            and concrete(disposition)
            and (waiver_authorized if waived else plan_authorized or scope_authorized)
        )
        views[path] = replace(views[path], task_disposition_valid=valid)

    common = set(base_documents) & set(proposed_documents)
    status_changed = frozenset(
        path
        for path in common
        if base_documents[path].profile_id != proposed_documents[path].profile_id
        or base_documents[path].status != proposed_documents[path].status
    )
    body_changed = frozenset(
        path
        for path in common
        if _body_text(base_texts[path]) != _body_text(proposed_texts[path])
    )
    created = frozenset(set(proposed_documents) - set(base_documents))
    return LifecycleEvidenceContext(
        base_documents=base_documents,
        proposed_documents=MappingProxyType(views),
        changed_paths=frozenset(
            path
            for path in set(base_documents) | set(proposed_documents)
            if path not in common or base_texts.get(path) != proposed_texts.get(path)
        ),
        status_changed_paths=status_changed,
        body_changed_paths=body_changed | created,
        created_paths=created,
        approved_initial_paths=_approved_initial_paths(
            base_documents, proposed_documents, proposed_texts, base_texts, views
        ),
        base_task_rows=MappingProxyType(base_task_rows),
        base_task_evidence_rows=MappingProxyType(base_task_evidence_rows),
        local_contract_issues=_local_plan_task_contract_issues(
            registry, base_documents, proposed_documents, base_texts, proposed_texts
        ),
        retired_identities=(
            lineage_retired_identities(proposed_texts)
            | lineage_retired_identities(base_texts)
        ),
    )


def _select_changes(
    changes: Sequence[Change],
    include_paths: Sequence[PurePosixPath],
    *,
    base_oid: Callable[[PurePosixPath], str | None],
    proposed_oid: Callable[[PurePosixPath], str | None],
) -> tuple[Change, ...]:
    target_changes = []
    for change in changes:
        if change.kind == "R" and change.old_path is not None:
            old_target = _approved_markdown(change.old_path)
            new_target = _approved_markdown(change.path)
            if old_target != new_target:
                target_changes.append(
                    Change("A", change.path)
                    if new_target
                    else Change("D", change.old_path)
                )
                continue
        if any(_approved_markdown(path) for path in change.paths):
            target_changes.append(change)
    if not include_paths:
        return tuple(target_changes)
    selected = list(target_changes)
    covered = {path for change in selected for path in change.paths}
    for path in include_paths:
        if path in covered:
            continue
        if base_oid(path) is None and proposed_oid(path) is None:
            raise InvocationError(
                f"included path has no base or proposed blob: {path.as_posix()}"
            )
        selected.append(Change("M", path))
    return tuple(selected)


def _comparison_documents(
    root: Path,
    base_registry: Registry,
    proposed_registry: Registry,
    changes: Sequence[Change],
    *,
    base_oid: Callable[[PurePosixPath], str | None],
    proposed_oid: Callable[[PurePosixPath], str | None],
) -> tuple[
    Mapping[PurePosixPath, LifecycleDocument],
    Mapping[PurePosixPath, LifecycleDocument],
    tuple[LifecycleRename, ...],
]:
    base_documents: dict[PurePosixPath, LifecycleDocument] = {}
    proposed_documents: dict[PurePosixPath, LifecycleDocument] = {}
    renames: list[LifecycleRename] = []

    def load(
        registry: Registry, path: PurePosixPath, oid: str | None
    ) -> LifecycleDocument | None:
        try:
            opaque = is_opaque_evaluation_output(registry, path)
        except DocumentContractError:
            opaque = False
        if opaque and oid is not None:
            _blob_bytes(root, oid)
        text = "" if opaque and oid is not None else _blob_text(root, oid, path)
        if text is None:
            return None
        try:
            return document_from_text(registry, path, text)
        except DocumentContractError:
            return LifecycleDocument(
                path=path,
                profile_id="unclassified",
                status=None,
                state_issue="no unique current registry profile",
            )

    for change in changes:
        if change.kind == "R":
            assert change.old_path is not None
            base = load(base_registry, change.old_path, base_oid(change.old_path))
            proposed = load(proposed_registry, change.path, proposed_oid(change.path))
            if base is None or proposed is None:
                raise InvocationError("exact rename lacks a base or proposed blob")
            base_documents[change.old_path] = base
            proposed_documents[change.path] = proposed
            renames.append(LifecycleRename(change.old_path, change.path))
        elif change.kind == "A":
            proposed = load(proposed_registry, change.path, proposed_oid(change.path))
            if proposed is None:
                raise InvocationError(f"added path lacks proposed blob: {change.path}")
            proposed_documents[change.path] = proposed
        elif change.kind == "D":
            base = load(base_registry, change.path, base_oid(change.path))
            if base is None:
                raise InvocationError(f"deleted path lacks base blob: {change.path}")
            base_documents[change.path] = base
        else:
            base = load(base_registry, change.path, base_oid(change.path))
            proposed = load(proposed_registry, change.path, proposed_oid(change.path))
            if base is None or proposed is None:
                raise InvocationError(
                    f"modified path lacks one comparison blob: {change.path}"
                )
            base_documents[change.path] = base
            proposed_documents[change.path] = proposed
    return base_documents, proposed_documents, tuple(renames)


def _first_parent_history(
    root: Path, base_commit: str, proposed_commit: str
) -> tuple[str, ...]:
    """Return one complete, bounded first-parent path from base to proposal."""

    if _run_git(root, ("rev-parse", "--is-shallow-repository")).strip() != b"false":
        raise InvocationError("cumulative lifecycle history requires a full repository")
    ancestor = _git_process(
        root,
        ("merge-base", "--is-ancestor", base_commit, proposed_commit),
        output_limit=GIT_SIZE_OUTPUT_MAX_BYTES,
    )
    if ancestor.returncode != 0 or ancestor.stdout or ancestor.stderr:
        raise InvocationError("comparison base is not an ancestor of the proposal")
    output = _run_git(
        root,
        (
            "rev-list",
            "--first-parent",
            "--reverse",
            "--topo-order",
            f"--max-count={CUMULATIVE_HISTORY_MAX_COMMITS + 1}",
            f"{base_commit}..{proposed_commit}",
        ),
        output_limit=(CUMULATIVE_HISTORY_MAX_COMMITS + 1) * GIT_SIZE_OUTPUT_MAX_BYTES,
    )
    try:
        commits = tuple(output.decode("ascii", errors="strict").splitlines())
    except UnicodeDecodeError as exc:
        raise InvocationError("cumulative lifecycle history is not ASCII") from exc
    if (
        not commits
        or len(commits) > CUMULATIVE_HISTORY_MAX_COMMITS
        or len(set(commits)) != len(commits)
        or any(OBJECT_ID.fullmatch(commit) is None for commit in commits)
        or commits[-1] != proposed_commit
    ):
        raise InvocationError(
            "cumulative lifecycle history is malformed or exceeds its cap"
        )
    parent = base_commit
    for commit in commits:
        raw = _run_git(
            root,
            ("rev-list", "--parents", "--max-count=1", commit),
            output_limit=GIT_SIZE_OUTPUT_MAX_BYTES * 4,
        )
        try:
            lines = raw.decode("ascii", errors="strict").splitlines()
            fields = lines[0].split() if len(lines) == 1 else []
        except UnicodeDecodeError as exc:
            raise InvocationError(
                "cumulative lifecycle parent evidence is not ASCII"
            ) from exc
        if (
            len(fields) < 2
            or fields[0] != commit
            or any(OBJECT_ID.fullmatch(value) is None for value in fields)
            or fields[1] != parent
        ):
            raise InvocationError(
                "cumulative lifecycle first-parent evidence is malformed"
            )
        parent = commit
    return commits


def _history_registered_task_template_copy(
    root: Path,
    parent: str,
    commit: str,
    source: PurePosixPath,
    path: PurePosixPath,
    target: LifecycleDocument,
    cache: _CumulativeHistoryCache,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
) -> bool:
    """Recognize an unchanged registered form's unique legal first Task state."""
    if (
        target.profile_id != "sdlc/task"
        or target.status not in {"draft", "ready", "in-progress", "blocked"}
        or target.state_issue is not None
        or target.artifact_id is None
        or _tree_blob_oid(root, parent, path) is not None
    ):
        return False
    profile = classify_path(cache.registry, path)
    if profile.profile_id != "sdlc/task" or source != profile.template:
        return False
    for revision in (parent, commit):
        historical = classify_path(cache.registry_at(revision), path)
        if historical.profile_id != "sdlc/task" or historical.template != source:
            return False
    source_blob = _tree_blob_oid(root, parent, source)
    owner = _load_canonical_markdown_module()
    return (
        source_blob is not None
        and source_blob == _tree_blob_oid(root, commit, source)
        and target.artifact_id == owner.expected_artifact_id(path, profile)
        and all(
            doc.artifact_id != target.artifact_id for doc in base_documents.values()
        )
        and sum(
            doc.artifact_id == target.artifact_id for doc in proposed_documents.values()
        )
        == 1
    )


def _history_first_adr_authoring_copy(
    root: Path,
    parent: str,
    commit: str,
    source: PurePosixPath,
    path: PurePosixPath,
    target: LifecycleDocument,
    cache: _CumulativeHistoryCache,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
) -> bool:
    """Admit only a distinct canonical ADR copied into a first proposed ADR."""
    if (
        target.profile_id != "sdlc/architecture-decision"
        or target.status != "proposed"
        or target.state_issue is not None
        or target.artifact_id is None
        or _tree_blob_oid(root, parent, path) is not None
    ):
        return False
    source_document = base_documents.get(source)
    if (
        source_document is None
        or source_document.profile_id != target.profile_id
        or source_document.state_issue is not None
        or source_document.artifact_id is None
        or source_document.artifact_id == target.artifact_id
    ):
        return False
    owner = _load_canonical_markdown_module()
    source_profile = classify_path(cache.registry_at(parent), source)
    target_profile = classify_path(cache.registry_at(commit), path)
    return bool(
        source_profile.profile_id == target.profile_id
        and target_profile.profile_id == target.profile_id
        and source_document.artifact_id
        == owner.expected_artifact_id(source, source_profile)
        and target.artifact_id == owner.expected_artifact_id(path, target_profile)
        and sum(
            doc.artifact_id == source_document.artifact_id
            for doc in base_documents.values()
        )
        == 1
        and all(
            doc.artifact_id != target.artifact_id for doc in base_documents.values()
        )
        and sum(
            doc.artifact_id == target.artifact_id for doc in proposed_documents.values()
        )
        == 1
        and (source_blob := _tree_blob_oid(root, parent, source)) is not None
        and source_blob == _tree_blob_oid(root, commit, source)
    )


def _history_first_approved_template_copy(
    root: Path,
    parent: str,
    commit: str,
    source: PurePosixPath,
    path: PurePosixPath,
    target: LifecycleDocument,
    cache: _CumulativeHistoryCache,
) -> bool:
    """Admit a registered Spec/Plan form copied into a receipt-bound new pair."""

    if (
        target.profile_id not in {"sdlc/spec", "sdlc/plan"}
        or target.status != "approved"
        or target.state_issue is not None
        or target.artifact_id is None
        or _tree_blob_oid(root, parent, path) is not None
    ):
        return False
    profile = classify_path(cache.registry_at(commit), path)
    if profile.profile_id != target.profile_id or source != profile.template:
        return False
    for revision in (parent, commit):
        historical = classify_path(cache.registry_at(revision), path)
        if historical.profile_id != target.profile_id or historical.template != source:
            return False
    source_blob = _tree_blob_oid(root, parent, source)
    owner = _load_canonical_markdown_module()
    return bool(
        source_blob is not None
        and source_blob == _tree_blob_oid(root, commit, source)
        and target.artifact_id == owner.expected_artifact_id(path, profile)
        and path in cache.evidence_context(parent, commit).approved_initial_paths
    )


def _history_rename_or_copy_into_path(
    root: Path,
    parent: str,
    commit: str,
    path: PurePosixPath,
    *,
    target_document: LifecycleDocument | None = None,
    cache: _CumulativeHistoryCache | None = None,
    allow_distinct_artifact_copy: bool = True,
) -> bool:
    """Reject bounded Git evidence of a rename or copy into the target path."""

    raw = _run_git(
        root,
        (
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--ignore-submodules=none",
            "--name-status",
            "-z",
            "--find-renames=1%",
            "--find-copies=1%",
            "--find-copies-harder",
            "-l0",
            parent,
            commit,
            "--",
        ),
    )
    records = raw.split(b"\0")
    if not records or records[-1] != b"":
        raise InvocationError("cumulative lifecycle provenance evidence is malformed")
    cursor = 0
    while cursor < len(records) - 1:
        try:
            status = records[cursor].decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise InvocationError(
                "cumulative lifecycle provenance status is malformed"
            ) from exc
        cursor += 1
        if status.startswith("R") or status.startswith("C"):
            if cursor + 1 >= len(records):
                raise InvocationError(
                    "cumulative lifecycle provenance evidence is truncated"
                )
            source = _decode_path(records[cursor])
            destination = _decode_path(records[cursor + 1])
            cursor += 2
            if destination == path:
                if (
                    status.startswith("C")
                    and target_document is not None
                    and cache is not None
                ):
                    base_documents = cache._snapshot(parent)[0]
                    source_document = base_documents.get(source)
                    proposed_documents = cache._snapshot(commit)[0]
                    target_id = target_document.artifact_id
                    source_blob = _tree_blob_oid(root, parent, source)
                    owner = _load_canonical_markdown_module()
                    if _history_registered_task_template_copy(
                        root,
                        parent,
                        commit,
                        source,
                        path,
                        target_document,
                        cache,
                        base_documents,
                        proposed_documents,
                    ):
                        continue
                    if _history_first_approved_template_copy(
                        root, parent, commit, source, path, target_document, cache
                    ):
                        continue
                    if _history_first_adr_authoring_copy(
                        root,
                        parent,
                        commit,
                        source,
                        path,
                        target_document,
                        cache,
                        base_documents,
                        proposed_documents,
                    ):
                        continue
                    if (
                        allow_distinct_artifact_copy
                        and not (
                            target_document.profile_id in {"sdlc/spec", "sdlc/plan"}
                            and target_document.status == "approved"
                        )
                        and source_document is not None
                        and source_document.state_issue is None
                        and source_document.artifact_id is not None
                        and target_id is not None
                        and source_document.artifact_id != target_id
                        and source_document.profile_id
                        == classify_path(cache.registry, source).profile_id
                        and source_document.artifact_id
                        == owner.expected_artifact_id(
                            source, classify_path(cache.registry, source)
                        )
                        and sum(
                            doc.artifact_id == source_document.artifact_id
                            for doc in base_documents.values()
                        )
                        == 1
                        and target_id
                        == owner.expected_artifact_id(
                            path, classify_path(cache.registry, path)
                        )
                        and all(
                            doc.artifact_id != target_id
                            for doc in base_documents.values()
                        )
                        and sum(
                            doc.artifact_id == target_id
                            for doc in proposed_documents.values()
                        )
                        == 1
                        and source_blob is not None
                        and source_blob == _tree_blob_oid(root, commit, source)
                    ):
                        continue
                return True
        elif status[:1] in {"A", "D", "M", "T"}:
            if cursor >= len(records):
                raise InvocationError(
                    "cumulative lifecycle provenance change is truncated"
                )
            _decode_path(records[cursor])
            cursor += 1
        else:
            raise InvocationError(
                "cumulative lifecycle provenance status is unsupported"
            )
    return False


def _history_first_appearance_has_deletion(
    root: Path,
    parent: str,
    commit: str,
) -> bool:
    """Reject any concurrent deletion before admitting a first appearance."""

    return any(change.kind == "D" for change in _tree_changes(root, parent, commit))


def _matching_seed_registry_oid(root: Path, base_commit: str) -> str | None:
    """Use compared base documents as a seed only under identical registry bytes."""

    oid = _tree_blob_oid(root, base_commit, CURRENT_REGISTRY_PATH)
    if oid is None:
        return None
    try:
        current_bytes = read_bounded_bytes(
            root / CURRENT_REGISTRY_PATH, max_bytes=DOCUMENT_BLOB_MAX_BYTES
        )
        historical_bytes = _blob_bytes(root, oid)
    except (OSError, ValueError):
        return None
    return oid if current_bytes == historical_bytes else None


class _CumulativeHistoryBudgetExceeded(RuntimeError):
    """A bounded cumulative-history cache cannot safely serve this invocation."""


def _snapshot_blob_size(root: Path, blobs: Mapping[PurePosixPath, str]) -> int:
    """Preflight exact per-path blob bytes without reading snapshot content."""

    if len(blobs) > CUMULATIVE_HISTORY_MAX_SNAPSHOT_PATHS:
        raise _CumulativeHistoryBudgetExceeded
    object_ids = tuple(dict.fromkeys(blobs.values()))
    if len(object_ids) > CUMULATIVE_HISTORY_MAX_SNAPSHOT_OBJECTS or any(
        OBJECT_ID.fullmatch(oid) is None for oid in object_ids
    ):
        raise _CumulativeHistoryBudgetExceeded
    if not object_ids:
        return 0
    request = ("\n".join(object_ids) + "\n").encode("ascii")
    output_limit = len(object_ids) * (GIT_SIZE_OUTPUT_MAX_BYTES * 2)
    if len(request) > GIT_CAPTURE_MAX_BYTES or output_limit > GIT_CAPTURE_MAX_BYTES:
        raise _CumulativeHistoryBudgetExceeded
    try:
        raw = _run_git(
            root,
            ("cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"),
            input_bytes=request,
            output_limit=output_limit,
        )
    except InvocationError as exc:
        raise _CumulativeHistoryBudgetExceeded from exc
    lines = raw.splitlines()
    if len(lines) != len(object_ids):
        raise _CumulativeHistoryBudgetExceeded
    sizes: dict[str, int] = {}
    for expected, line in zip(object_ids, lines, strict=True):
        fields = line.split(b" ")
        if len(fields) != 3:
            raise _CumulativeHistoryBudgetExceeded
        try:
            returned = fields[0].decode("ascii", errors="strict")
            object_type = fields[1].decode("ascii", errors="strict")
            size_text = fields[2].decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise _CumulativeHistoryBudgetExceeded from exc
        if (
            returned != expected
            or object_type != "blob"
            or not size_text.isascii()
            or not size_text.isdecimal()
        ):
            raise _CumulativeHistoryBudgetExceeded
        size = int(size_text)
        if size > DOCUMENT_BLOB_MAX_BYTES:
            raise _CumulativeHistoryBudgetExceeded
        if returned in sizes:
            raise _CumulativeHistoryBudgetExceeded
        sizes[returned] = size
    total = sum(sizes[oid] for oid in blobs.values())
    if total < 0:
        raise _CumulativeHistoryBudgetExceeded
    return total


@dataclass
class _CumulativeHistoryCache:
    """Share bounded snapshot and evidence work across one comparison's paths."""

    root: Path
    registry: Registry
    seed_blobs: Mapping[PurePosixPath, str] | None = None
    seed_documents: Mapping[PurePosixPath, LifecycleDocument] | None = None
    seed_texts: Mapping[PurePosixPath, str] | None = None
    seed_registry: Registry | None = None
    seed_registry_oid: str | None = None
    snapshots: OrderedDict[
        str,
        tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]],
    ] = field(default_factory=OrderedDict)
    snapshot_blobs: dict[str, Mapping[PurePosixPath, str]] = field(default_factory=dict)
    snapshot_registry_oids: dict[str, str | None] = field(default_factory=dict)
    cached_snapshot_bytes: int = 0
    snapshot_work_bytes: int = 0
    evidence: OrderedDict[tuple[str, str], LifecycleEvidenceContext] = field(
        default_factory=OrderedDict
    )
    retired: dict[str, dict[str, PurePosixPath]] = field(default_factory=dict)

    def retired_between(self, parent: str, commit: str) -> dict[str, PurePosixPath]:
        """Lineage-reserved identities of two snapshots, derived once per commit."""

        for oid in (parent, commit):
            if oid not in self.retired:
                self.retired[oid] = lineage_retired_identities(self._snapshot(oid)[1])
        return self.retired[commit] | self.retired[parent]

    def _resident_size_with(self, additional: Mapping[PurePosixPath, str]) -> int:
        """Bound live raw payloads by exact path/blob identity across snapshots."""

        live = {
            (path, oid): oid
            for snapshot in self.snapshot_blobs.values()
            for path, oid in snapshot.items()
        }
        live.update(((path, oid), oid) for path, oid in additional.items())
        return _snapshot_blob_size(
            self.root,
            {
                PurePosixPath(f"cache/{index}"): oid
                for index, oid in enumerate(live.values())
            },
        )

    def _needs_resident_eviction(self, additional: Mapping[PurePosixPath, str]) -> bool:
        try:
            return (
                self._resident_size_with(additional)
                > CUMULATIVE_HISTORY_MAX_SNAPSHOT_BYTES
            )
        except _CumulativeHistoryBudgetExceeded:
            # The temporary union may exceed an object/path bound even when
            # the new snapshot alone fits after an old snapshot is evicted.
            return True

    def registry_at(self, commit: str) -> Registry:
        """Classify each history event with the registry that commit carried.

        A historical registry still carrying keys the current schema retired
        loads unchanged, because the typed reader takes only the fields it owns.
        """
        oid = _tree_blob_oid(self.root, commit, CURRENT_REGISTRY_PATH)
        raw = _registry_blob(self.root, oid) if oid is not None else {}
        if raw.get("schema_version") != 10:
            return self.registry
        try:
            return _typed_registry_from_mapping(raw)
        except (KeyError, TypeError, ValueError, re.error) as exc:
            raise InvocationError("history registry is malformed") from exc

    def _snapshot(
        self, commit: str
    ) -> tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]]:
        cached = self.snapshots.get(commit)
        if cached is not None:
            self.snapshots.move_to_end(commit)
            return cached
        blobs = _tree_blob_map(self.root, commit)
        if (
            len(blobs) > CUMULATIVE_HISTORY_MAX_SNAPSHOT_PATHS
            or len(set(blobs.values())) > CUMULATIVE_HISTORY_MAX_SNAPSHOT_OBJECTS
        ):
            raise _CumulativeHistoryBudgetExceeded
        own_registry = self.registry_at(commit)
        registry_oid = _tree_blob_oid(self.root, commit, CURRENT_REGISTRY_PATH)
        prior_commit = next(
            (
                revision
                for revision in reversed(self.snapshots)
                if self.snapshot_registry_oids[revision] == registry_oid
            ),
            None,
        )
        prior_blobs = self.snapshot_blobs[prior_commit] if prior_commit else None
        prior_snapshot = self.snapshots[prior_commit] if prior_commit else None
        has_seed = (
            self.seed_blobs is not None
            and self.seed_documents is not None
            and self.seed_texts is not None
        )
        reuse_seed = (
            prior_snapshot is None
            and has_seed
            and self.seed_registry_oid is not None
            and self.seed_registry_oid == registry_oid
        )
        reference_blobs = prior_blobs if prior_blobs is not None else self.seed_blobs
        changed_blobs = (
            {
                path: oid
                for path, oid in blobs.items()
                if reference_blobs.get(path) != oid
            }
            if prior_snapshot is not None or reuse_seed
            else blobs
        )
        size = _snapshot_blob_size(self.root, changed_blobs)
        if size > CUMULATIVE_HISTORY_MAX_SNAPSHOT_BYTES or (
            self.snapshot_work_bytes + size > CUMULATIVE_HISTORY_MAX_SNAPSHOT_WORK_BYTES
        ):
            raise _CumulativeHistoryBudgetExceeded
        reused_texts: dict[PurePosixPath, str] = {}
        for path, oid in changed_blobs.items():
            for revision, old_blobs in reversed(tuple(self.snapshot_blobs.items())):
                if old_blobs.get(path) == oid:
                    candidate_text = self.snapshots[revision][1][path]
                    if candidate_text:
                        reused_texts[path] = candidate_text
                        break
            if (
                path not in reused_texts
                and self.seed_blobs is not None
                and self.seed_texts is not None
                and self.seed_blobs.get(path) == oid
                and self.seed_texts[path]
            ):
                reused_texts[path] = self.seed_texts[path]
        while self.snapshots and (
            len(self.snapshots) >= CUMULATIVE_HISTORY_CACHE_MAX_SNAPSHOTS
            or self._needs_resident_eviction(blobs)
        ):
            evicted, _ = self.snapshots.popitem(last=False)
            del self.snapshot_blobs[evicted]
            del self.snapshot_registry_oids[evicted]
            for key in tuple(self.evidence):
                if evicted in key:
                    del self.evidence[key]
        resident_size = self._resident_size_with(blobs)
        if resident_size > CUMULATIVE_HISTORY_MAX_SNAPSHOT_BYTES:
            raise _CumulativeHistoryBudgetExceeded
        changed_documents, changed_texts = _snapshot_projection(
            self.root,
            own_registry,
            changed_blobs,
            reused_texts=reused_texts,
        )
        if prior_snapshot is not None or reuse_seed:
            if prior_snapshot is not None:
                reference_documents, reference_texts = prior_snapshot
            else:
                assert self.seed_documents is not None and self.seed_texts is not None
                reference_documents, reference_texts = (
                    self.seed_documents,
                    self.seed_texts,
                )
            snapshot = (
                MappingProxyType(
                    {
                        path: changed_documents.get(path, reference_documents.get(path))
                        for path in blobs
                    }
                ),
                MappingProxyType(
                    {
                        path: changed_texts.get(path, reference_texts.get(path))
                        for path in blobs
                    }
                ),
            )
            if any(value is None for mapping in snapshot for value in mapping.values()):
                raise _CumulativeHistoryBudgetExceeded
        else:
            snapshot = changed_documents, changed_texts
        self.snapshot_work_bytes += size
        self.snapshots[commit] = snapshot
        self.snapshot_blobs[commit] = blobs
        self.snapshot_registry_oids[commit] = registry_oid
        self.cached_snapshot_bytes = resident_size
        return snapshot

    def evidence_context(self, parent: str, commit: str) -> LifecycleEvidenceContext:
        key = (parent, commit)
        cached = self.evidence.get(key)
        if cached is not None:
            self.evidence.move_to_end(key)
            return cached
        if len(self.evidence) >= CUMULATIVE_HISTORY_CACHE_MAX_EVIDENCE:
            self.evidence.popitem(last=False)
        if key not in self.evidence:
            base_snapshot, base_texts = self._snapshot(parent)
            proposed_snapshot, proposed_texts = self._snapshot(commit)
            self.evidence[key] = _evidence_context(
                self.registry_at(commit),
                base_snapshot,
                proposed_snapshot,
                base_texts,
                proposed_texts,
            )
        return self.evidence[key]


def _history_document(
    cache: _CumulativeHistoryCache, commit: str, path: PurePosixPath
) -> LifecycleDocument:
    document = cache._snapshot(commit)[0].get(path)
    profile = classify_path(cache.registry_at(commit), path)
    if (
        document is None
        or document.state_issue is not None
        or document.profile_id != profile.profile_id
        or profile.lifecycle_domain is None
    ):
        raise InvocationError("cumulative lifecycle path has no stable profile")
    return document


def _committed_task_binding(root: Path, commit: str) -> bool:
    """Recognize only commits whose own Stage 99 registry bound Task execution."""

    oid = _tree_blob_oid(root, commit, CURRENT_REGISTRY_PATH)
    if oid is None:
        return False
    text = _blob_text(root, oid, CURRENT_REGISTRY_PATH)
    try:
        raw = json.loads(text) if text is not None else None
    except (TypeError, ValueError):
        return False
    if not isinstance(raw, dict) or not isinstance(raw.get("profiles"), list):
        return False
    return any(
        isinstance(profile, dict)
        and profile.get("id") == "sdlc/task"
        and isinstance((profile.get("relationships") or {}).get("body_contract"), dict)
        and isinstance(
            profile["relationships"]["body_contract"].get("task_execution"), dict
        )
        for profile in raw["profiles"]
    )


def _history_event_diagnostics(
    root: Path,
    registry: Registry,
    path: PurePosixPath,
    parent: str,
    commit: str,
    before: LifecycleDocument | None,
    after: LifecycleDocument,
    cache: _CumulativeHistoryCache,
) -> tuple[LifecycleDiagnostic, ...]:
    """Use the normal lifecycle comparison with exact parent/commit evidence."""

    base_documents = {} if before is None else {path: before}
    event_registry = cache.registry_at(commit)
    base_registry = cache.registry_at(parent)
    task_binding = after.profile_id == "sdlc/task" and _committed_task_binding(
        root, commit
    )
    if (
        after.profile_id == "sdlc/architecture-decision"
        and after.status != "superseded"
    ):
        # Ordinary ADR creation and forward edges have no body contract.
        # Still bind identity to both complete immutable snapshots; a terminal
        # supersession keeps the full reciprocal-evidence path below.
        parent_documents = cache._snapshot(parent)[0]
        commit_documents = cache._snapshot(commit)[0]
        identity_diagnostics = artifact_identity_reuse_diagnostics(
            parent_documents,
            commit_documents,
            base_mode="explicit-ref",
            retired=cache.retired_between(parent, commit),
        )
        if any(item.path == path for item in identity_diagnostics):
            return tuple(item for item in identity_diagnostics if item.path == path)
        return compare_lifecycle(
            event_registry,
            base_documents,
            {path: after},
            base_mode="explicit-ref",
            base_registry=base_registry,
        )
    if cache.seed_blobs is not None and cache.seed_registry is None:
        # Ordinary initial/forward edges need no cross-document body evidence.
        # Terminal supersession events retain the full-snapshot path.
        if after.status == "superseded":
            raise InvocationError("staged cumulative edge needs full evidence")
        parent_documents = cache._snapshot(parent)[0]
        commit_documents = cache._snapshot(commit)[0]
        identity_diagnostics = artifact_identity_reuse_diagnostics(
            parent_documents,
            commit_documents,
            base_mode="explicit-ref",
            retired=cache.retired_between(parent, commit),
        )
        if any(item.path == path for item in identity_diagnostics):
            return tuple(item for item in identity_diagnostics if item.path == path)
        if task_binding or (
            before is None
            and after.profile_id in {"sdlc/spec", "sdlc/plan"}
            and after.status == "approved"
        ):
            return compare_lifecycle(
                event_registry,
                base_documents,
                {path: after},
                base_mode="explicit-ref",
                evidence_context=cache.evidence_context(parent, commit),
                enforce_task_execution=True,
                base_registry=base_registry,
            )
        return compare_lifecycle(
            event_registry,
            base_documents,
            {path: after},
            base_mode="explicit-ref",
            base_registry=base_registry,
        )
    return compare_lifecycle(
        event_registry,
        base_documents,
        {path: after},
        base_mode="explicit-ref",
        evidence_context=cache.evidence_context(parent, commit),
        enforce_task_execution=task_binding,
        base_registry=base_registry,
    )


def _history_proves_cumulative_create(
    root: Path,
    registry: Registry,
    path: PurePosixPath,
    base_commit: str,
    proposed_commit: str,
    expected_proposed_blob: str | None = None,
    commits: tuple[str, ...] | None = None,
    cache: _CumulativeHistoryCache | None = None,
    allow_merge_create: bool = False,
    allow_distinct_artifact_copy: bool = False,
    remaining_events: list[int] | None = None,
) -> bool:
    """Prove a path's legal history, allowing at most one merge import when requested."""

    try:
        if _tree_blob_oid(root, base_commit, path) is not None:
            return False
        final_blob = _tree_blob_oid(root, proposed_commit, path)
        if final_blob is None or (
            expected_proposed_blob is not None and final_blob != expected_proposed_blob
        ):
            return False
        history = (
            _first_parent_history(root, base_commit, proposed_commit)
            if commits is None
            else commits
        )
        if not history:
            return False
        if remaining_events is None:
            remaining_events = [CUMULATIVE_HISTORY_MAX_CANDIDATE_EVENTS]
        if len(history) > remaining_events[0]:
            return False
        remaining_events[0] -= len(history)
        history_cache = (
            _CumulativeHistoryCache(root, registry) if cache is None else cache
        )
        appeared = False
        prior_blob: str | None = None
        prior_document: LifecycleDocument | None = None
        parent = base_commit
        for commit in history:
            current_blob = _tree_blob_oid(root, commit, path)
            if current_blob is None:
                if appeared:
                    return False
                parent = commit
                continue
            target_document = (
                _history_document(history_cache, commit, path)
                if not appeared
                and (
                    allow_distinct_artifact_copy
                    or classify_path(registry, path).profile_id
                    in {
                        "sdlc/task",
                        "sdlc/spec",
                        "sdlc/plan",
                        "sdlc/architecture-decision",
                    }
                )
                else None
            )
            if _history_rename_or_copy_into_path(
                root,
                parent,
                commit,
                path,
                target_document=target_document,
                cache=history_cache if target_document is not None else None,
                allow_distinct_artifact_copy=allow_distinct_artifact_copy,
            ) or (
                not appeared
                and _history_first_appearance_has_deletion(root, parent, commit)
            ):
                return False
            parent_raw = _run_git(
                root,
                ("rev-list", "--parents", "--max-count=1", commit),
                output_limit=GIT_SIZE_OUTPUT_MAX_BYTES * 4,
            )
            parent_fields = parent_raw.decode("ascii", errors="strict").split()
            if len(parent_fields) != 2 and current_blob != prior_blob:
                if not (
                    allow_merge_create
                    and not appeared
                    and prior_blob is None
                    and len(parent_fields) == 3
                    and parent_fields[:2] == [commit, parent]
                    and _tree_blob_oid(root, parent, path) is None
                    and _tree_blob_oid(root, parent_fields[2], path) == current_blob
                ):
                    return False
                side_base = _merge_base(root, parent, parent_fields[2])
                side_history = _first_parent_history(root, side_base, parent_fields[2])
                if not _history_proves_cumulative_create(
                    root,
                    registry,
                    path,
                    side_base,
                    parent_fields[2],
                    current_blob,
                    commits=side_history,
                    cache=history_cache,
                    allow_distinct_artifact_copy=allow_distinct_artifact_copy,
                    remaining_events=remaining_events,
                ):
                    return False
                appeared = True
                prior_document = _history_document(history_cache, commit, path)
            elif not appeared:
                if prior_blob is not None:
                    return False
                current = _history_document(history_cache, commit, path)
                if current.status is None or _history_event_diagnostics(
                    root,
                    registry,
                    path,
                    parent,
                    commit,
                    None,
                    current,
                    history_cache,
                ):
                    return False
                appeared = True
                prior_document = current
            elif current_blob != prior_blob:
                current = _history_document(history_cache, commit, path)
                if (
                    prior_document is None
                    or current.profile_id != prior_document.profile_id
                    or _history_event_diagnostics(
                        root,
                        registry,
                        path,
                        parent,
                        commit,
                        prior_document,
                        current,
                        history_cache,
                    )
                ):
                    return False
                prior_document = current
            prior_blob = current_blob
            parent = commit
        return appeared and prior_blob == final_blob
    except (DocumentContractError, InvocationError, UnicodeDecodeError, ValueError):
        return False


def _staged_merge_parent(root: Path, head: str) -> tuple[str, str] | None:
    """Return the actual divergent merge parent and its unique common base."""

    raw_path = _run_git(
        root, ("rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD")
    )
    path = Path(raw_path.decode("utf-8").strip())
    if not os.path.lexists(path):
        return None
    raw = read_bounded_bytes(path, max_bytes=128)
    if re.fullmatch(rb"(?:[0-9a-f]{40}|[0-9a-f]{64})\n", raw) is None:
        return None
    parent = raw.decode("ascii").strip()
    if parent == head or _resolve_commit(root, parent, "MERGE_HEAD") != parent:
        return None
    common = _merge_base(root, head, parent)
    if common in {head, parent}:
        return None
    return common, parent


def _admit_cumulative_create_diagnostics(
    diagnostics: Sequence[LifecycleDiagnostic],
    *,
    root: Path,
    registry: Registry,
    mode: str,
    base_commit: str,
    proposed_commit: str | None,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    base_snapshot: Mapping[PurePosixPath, LifecycleDocument] | None = None,
    base_texts: Mapping[PurePosixPath, str] | None = None,
    base_registry: Registry | None = None,
) -> tuple[LifecycleDiagnostic, ...]:
    """Remove only history-proved create diagnostics in committed comparisons."""

    if mode not in {"ci", "explicit-ref", "staged"}:
        return tuple(diagnostics)
    if mode != "staged" and proposed_commit is None:
        return tuple(diagnostics)
    candidates = [
        (index, diagnostic)
        for index, diagnostic in enumerate(diagnostics)
        if (
            diagnostic.rule_id == "LIFECYCLE-CREATE"
            and base_blobs.get(diagnostic.path) is None
            and proposed_blobs.get(diagnostic.path) is not None
        )
    ]
    if not candidates:
        return tuple(diagnostics)
    candidate_paths = tuple(
        dict.fromkeys(diagnostic.path for _, diagnostic in candidates)
    )
    if len(candidate_paths) > CUMULATIVE_HISTORY_MAX_CANDIDATES:
        return tuple(diagnostics)
    try:
        if mode == "staged":
            merge_parent = _staged_merge_parent(root, base_commit)
            if merge_parent is None:
                return tuple(diagnostics)
            history_base, history_tip = merge_parent
        else:
            history_base, history_tip = base_commit, proposed_commit
        assert history_tip is not None
        history = _first_parent_history(root, history_base, history_tip)
    except (InvocationError, UnicodeDecodeError, ValueError):
        return tuple(diagnostics)
    if len(candidate_paths) * len(history) > CUMULATIVE_HISTORY_MAX_CANDIDATE_EVENTS:
        return tuple(diagnostics)
    cache = _CumulativeHistoryCache(
        root,
        registry,
        seed_blobs=base_blobs if base_snapshot is not None else None,
        seed_documents=base_snapshot,
        seed_texts=base_texts,
        seed_registry=base_registry if mode != "staged" else None,
        seed_registry_oid=_matching_seed_registry_oid(root, base_commit),
    )
    remaining_events = [CUMULATIVE_HISTORY_MAX_CANDIDATE_EVENTS]
    admitted_indices: set[int] = set()
    proved_paths: set[PurePosixPath] = set()
    try:
        for index, diagnostic in candidates:
            if diagnostic.path in proved_paths:
                continue
            if _history_proves_cumulative_create(
                root,
                registry,
                diagnostic.path,
                history_base,
                history_tip,
                proposed_blobs[diagnostic.path],
                commits=history,
                cache=cache,
                allow_merge_create=mode == "staged",
                allow_distinct_artifact_copy=mode == "staged",
                remaining_events=remaining_events,
            ):
                admitted_indices.add(index)
                proved_paths.add(diagnostic.path)
    except _CumulativeHistoryBudgetExceeded:
        return tuple(diagnostics)
    return tuple(
        diagnostic
        for index, diagnostic in enumerate(diagnostics)
        if index not in admitted_indices
    )


def _evaluate_comparison(
    root: Path,
    registry: Registry,
    *,
    mode: str,
    from_ref: str | None = None,
    base_ref: str | None = None,
    to_ref: str | None = None,
    include_paths: Sequence[PurePosixPath] = (),
    evidence_context_factory: Callable[
        ..., LifecycleEvidenceContext
    ] = _evidence_context,
) -> tuple[LifecycleDiagnostic, ...]:
    _verify_repository_root(root)
    proposed_commit: str | None = None
    if mode == "staged":
        base_commit = _resolve_commit(root, "HEAD", "HEAD")
        base_blobs = _tree_blob_map(root, base_commit)
        proposed_blobs = _index_blob_map(root)
        changes = _staged_changes(root)
    else:
        if mode == "ci":
            assert base_ref is not None and to_ref is not None
            configured_base = _resolve_commit(root, base_ref, "base-ref")
            proposed_commit = _resolve_commit(root, to_ref, "to-ref")
            base_commit = _merge_base(root, configured_base, proposed_commit)
        elif mode == "explicit-ref":
            assert from_ref is not None and to_ref is not None
            base_commit = _resolve_commit(root, from_ref, "from-ref")
            proposed_commit = _resolve_commit(root, to_ref, "to-ref")
        else:
            raise InvocationError(f"unsupported comparison mode: {mode}")

        base_blobs = _tree_blob_map(root, base_commit)
        proposed_blobs = _tree_blob_map(root, proposed_commit)
        changes = _tree_changes(root, base_commit, proposed_commit)

    # The comparison base is classified with the current registry. A historical
    # registry is never parsed, so keys it carries that the current schema
    # retired cannot fail base loading.
    base_classification_registry = registry
    proposed_classification_registry = registry

    def base_oid(path: PurePosixPath) -> str | None:
        return base_blobs.get(path)

    def proposed_oid(path: PurePosixPath) -> str | None:
        return proposed_blobs.get(path)

    selected = _select_changes(
        changes,
        include_paths,
        base_oid=base_oid,
        proposed_oid=proposed_oid,
    )
    base_documents, proposed_documents, renames = _comparison_documents(
        root,
        base_classification_registry,
        proposed_classification_registry,
        selected,
        base_oid=base_oid,
        proposed_oid=proposed_oid,
    )
    base_snapshot, base_texts = _snapshot_projection(
        root, base_classification_registry, base_blobs
    )
    proposed_snapshot, proposed_texts = _snapshot_projection(
        root, proposed_classification_registry, proposed_blobs
    )
    evidence_context = evidence_context_factory(
        proposed_classification_registry,
        base_snapshot,
        proposed_snapshot,
        base_texts,
        proposed_texts,
    )
    diagnostics = compare_lifecycle(
        proposed_classification_registry,
        base_documents,
        proposed_documents,
        renames=renames,
        base_mode=mode,  # type: ignore[arg-type]
        evidence_context=evidence_context,
        enforce_task_execution=True,
        base_registry=base_classification_registry,
    )
    diagnostics += validate_current_task_evidence(
        evidence_context,
        base_mode=mode,  # type: ignore[arg-type]
    )
    if mode == "staged":
        diagnostics += package_exit_diagnostics(
            base_snapshot,
            proposed_snapshot,
            base_texts,
            proposed_texts,
            base_mode="staged",
        )
    return _admit_cumulative_create_diagnostics(
        diagnostics,
        root=root,
        registry=proposed_classification_registry,
        mode=mode,
        base_commit=base_commit,
        proposed_commit=proposed_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
        base_snapshot=base_snapshot,
        base_texts=base_texts,
        base_registry=base_classification_registry,
    )


def _verified_opaque_snapshot_text(root: Path, path: PurePosixPath) -> str:
    verify_opaque_evaluation_output(root, path)
    return ""


def _evaluate_snapshot(
    root: Path,
    registry: Registry,
    include_paths: Sequence[PurePosixPath],
) -> tuple[LifecycleDiagnostic, ...]:
    _verify_repository_root(root)
    inventory = enumerate_target_markdown(root, include_paths=tuple(include_paths))
    texts = {
        path: (
            _verified_opaque_snapshot_text(root, path)
            if is_opaque_evaluation_output(registry, path)
            else read_repository_text(root, path)
        )
        for path in inventory.current_paths
    }
    documents = {
        path: document_from_text(registry, path, text) for path, text in texts.items()
    }
    context = _evidence_context(registry, {}, documents, {}, texts)
    return validate_snapshot_documents(registry, tuple(documents.values())) + (
        validate_current_task_evidence(context, base_mode="explicit-ref")
    )


def _evaluate_completion(
    root: Path,
    registry: Registry,
    include_paths: Sequence[PurePosixPath],
) -> tuple[tuple[LifecycleDiagnostic, ...], str]:
    """Assess package completion using only one exact Git index snapshot."""

    if not include_paths:
        raise InvocationError("completion mode requires --include-path Spec anchors")
    blobs = _index_blob_map(root)
    snapshot_hash = hashlib.sha256()
    for path, oid in sorted(blobs.items(), key=lambda item: item[0].as_posix()):
        snapshot_hash.update(
            path.as_posix().encode("utf-8") + b"\0" + oid.encode("ascii") + b"\0"
        )
    for path in COMPLETION_AUTHORITY_PATHS:
        snapshot_hash.update(path.as_posix().encode("utf-8") + b"\0")
        snapshot_hash.update(staged_authority_bytes(root, path) + b"\0")
    digest = snapshot_hash.hexdigest()
    documents, texts = _snapshot_projection(root, registry, blobs)
    schema_path = PurePosixPath("docs/99.templates/contracts/frontmatter.schema.json")
    schema_text = staged_authority_bytes(root, schema_path).decode("utf-8")
    schema = json.loads(schema_text, object_pairs_hook=_unique_json_object)
    return _completion_document_diagnostics(
        root, registry, include_paths, documents, texts, schema, base_mode="completion"
    ), digest


def _completion_document_diagnostics(
    root: Path,
    registry: Registry,
    include_paths: Sequence[PurePosixPath],
    documents: Mapping[PurePosixPath, LifecycleDocument],
    texts: Mapping[PurePosixPath, str],
    schema: Mapping[str, Any],
    *,
    base_mode: str,
) -> tuple[LifecycleDiagnostic, ...]:
    """Judge one immutable package snapshot for index completion."""

    owner = _load_canonical_markdown_module()
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    adapter = _link_validator_module()
    diagnostics: list[LifecycleDiagnostic] = []

    def fail(path: PurePosixPath, rule: str, detail: str) -> None:
        diagnostics.append(
            LifecycleDiagnostic(
                severity="FAIL",
                rule_id=rule,
                path=path,
                profile=documents[path].profile_id if path in documents else "",
                expected_transition="complete Spec criterion -> Plan assignment -> Task PASS evidence",
                observed_transition=detail,
                base_mode=base_mode,
                evidence_gap=(
                    "exact Git index package traceability"
                    if base_mode == "completion"
                    else "immutable comparison-base package traceability"
                ),
            )
        )

    def rows(path: PurePosixPath) -> list[dict[str, str]] | None:
        document = documents.get(path)
        profile = profiles.get(document.profile_id) if document else None
        if profile is None:
            return None
        return adapter._body_contract_rows(texts[path], profile)

    def linked_target(path: PurePosixPath, cell: str) -> PurePosixPath | None:
        links = adapter._extract_links(cell, definitions_text=texts[path])
        if len(links) != 1:
            return None
        kind, target = adapter._local_destination(path, links[0])
        return target if kind in {"local", "anchor"} else None

    for spec_path in include_paths:
        if (
            spec_path.parts[:2] != ("docs", "03.specs")
            or spec_path.name != "spec.md"
            or documents.get(spec_path, None) is None
            or documents[spec_path].profile_id != "sdlc/spec"
        ):
            fail(spec_path, "COMPLETION-SPEC", "anchor must be an indexed current Spec")
            continue
        if documents[spec_path].status not in {"active", "approved", "completed"}:
            fail(
                spec_path,
                "COMPLETION-SPEC",
                "Spec approval state is not active/completed",
            )
        package = spec_path.parent
        plan_path = package / "plan.md"
        for path, document in documents.items():
            if path in {spec_path, plan_path} or (
                path.parent == package / "tasks" and document.profile_id == "sdlc/task"
            ):
                for finding in owner.validate_document_text(
                    texts[path],
                    path,
                    profiles[document.profile_id],
                    "strict",
                    frontmatter_schema=schema,
                ):
                    fail(path, finding.rule_id, finding.actual)
        if plan_path not in documents or documents[plan_path].profile_id != "sdlc/plan":
            fail(plan_path, "COMPLETION-PLAN", "indexed same-package Plan missing")
            continue
        if documents[plan_path].status not in {
            "active",
            "approved",
            "in-progress",
            "completed",
        }:
            fail(
                plan_path,
                "COMPLETION-PLAN",
                "Plan approval state is not active/completed",
            )

        success_section = adapter._exact_heading_section(
            texts[spec_path], "## Success Criteria & Verification Plan"
        )
        success_table = adapter._first_visible_table(success_section or "")
        if success_table is None or success_table[0] != [
            "Criterion",
            "Acceptance evidence",
        ]:
            fail(
                spec_path, "COMPLETION-CRITERIA", "missing exact Success Criteria table"
            )
            continue
        defined: list[str] = []
        for entry in success_table[1]:
            if len(entry) != 2 or not entry[1].strip():
                fail(spec_path, "COMPLETION-CRITERIA", "malformed criterion definition")
                continue
            identifier = entry[0].strip()
            if re.fullmatch(r"VAL-[A-Z0-9-]+-[0-9]{3}", identifier):
                defined.append(identifier)
            elif not re.fullmatch(r"N/A — \S(?:.*\S)?", identifier):
                fail(
                    spec_path,
                    "COMPLETION-CRITERIA",
                    f"invalid definition {identifier!r}",
                )
        if not defined or len(defined) != len(set(defined)):
            fail(
                spec_path,
                "COMPLETION-CRITERIA",
                "at least one unique concrete VAL definition required",
            )
            continue
        spec_rows = rows(spec_path)
        if spec_rows is None:
            fail(
                spec_path,
                "COMPLETION-TRACE",
                "Spec Lifecycle Traceability table missing",
            )
            continue
        traced = [row["Spec criterion"].strip() for row in spec_rows]
        concrete = [item for item in traced if not item.startswith("N/A — ")]
        if len(concrete) != len(set(concrete)) or set(concrete) != set(defined):
            fail(
                spec_path,
                "COMPLETION-TRACE",
                "defined and traced VAL sets differ or duplicate",
            )
            continue

        plan_rows = rows(plan_path)
        if not plan_rows:
            fail(plan_path, "COMPLETION-PLAN", "Plan allocations missing")
            continue
        assignments: set[tuple[str, PurePosixPath]] = set()
        plan_contract = profiles["sdlc/plan"].body_contract
        assert plan_contract is not None
        for entry in plan_rows:
            source = entry[plan_contract.source_link_column]
            criteria = task_criterion_ids(source)
            task_path = linked_target(
                plan_path, entry[plan_contract.target_link_column]
            )
            source_links = adapter._extract_links(
                source, definitions_text=texts[plan_path]
            )
            if (
                not criteria
                or any(criterion not in defined for criterion in criteria)
                or len(source_links) != len(criteria)
                or any(
                    adapter._local_destination(plan_path, link)[1] != spec_path
                    for link in source_links
                )
                or task_path is None
                or task_path.parent != package / "tasks"
                or task_path not in documents
                or documents[task_path].profile_id != "sdlc/task"
            ):
                fail(
                    plan_path,
                    "COMPLETION-ALLOCATION",
                    f"invalid Plan row for {criteria!r}",
                )
                continue
            assignments.update((criterion, task_path) for criterion in criteria)
        if {criterion for criterion, _ in assignments} != set(defined):
            fail(
                plan_path,
                "COMPLETION-ALLOCATION",
                "one or more required criteria lack a Task assignment",
            )

        baseline_documents: dict[PurePosixPath, LifecycleDocument] = {}
        baseline_texts: dict[PurePosixPath, str] = {}
        if base_mode == "completion":
            for current_path, current_doc in documents.items():
                if current_path not in {spec_path, plan_path} and not (
                    current_path.parent == package / "tasks"
                    and current_doc.profile_id == "sdlc/task"
                ):
                    continue
                try:
                    prior_oid = _tree_blob_oid(root, "HEAD", current_path)
                except InvocationError:  # An unborn fixture has no comparison base.
                    prior_oid = None
                if prior_oid is not None:
                    prior_text = _blob_text(root, prior_oid, current_path)
                    baseline_texts[current_path] = prior_text
                    baseline_documents[current_path] = document_from_text(
                        registry, current_path, prior_text
                    )
        context = _evidence_context(
            registry, baseline_documents, documents, baseline_texts, texts
        )
        for diagnostic in validate_current_task_evidence(
            context, base_mode="explicit-ref"
        ):
            if diagnostic.path.parent == package / "tasks":
                fail(
                    diagnostic.path, diagnostic.rule_id, diagnostic.observed_transition
                )
        if base_mode == "completion":
            for diagnostic in local_contract_diagnostics(
                context, base_mode="completion"
            ):
                if (
                    diagnostic.path == plan_path
                    or diagnostic.path.parent == package / "tasks"
                ):
                    fail(
                        diagnostic.path,
                        diagnostic.rule_id,
                        diagnostic.observed_transition,
                    )

        task_pairs: dict[tuple[str, PurePosixPath], list[dict[str, str]]] = {}
        accepted_origins: dict[str, list[PurePosixPath]] = {}
        modern_origins: dict[str, list[PurePosixPath]] = {}
        task_paths = sorted(
            (
                path
                for path, doc in documents.items()
                if path.parent == package / "tasks" and doc.profile_id == "sdlc/task"
            ),
            key=PurePosixPath.as_posix,
        )
        if not task_paths:
            fail(spec_path, "COMPLETION-TASK", "no indexed same-package Task")
        for task_path in task_paths:
            for path in (plan_path, task_path):
                parent = direct_parent(path, documents[path].profile_id)
                metadata = frontmatter_mapping(texts[path])
                if parent is not None and (
                    metadata.get("parent_ids") != [parent[1]]
                    or parent[0] not in documents
                    or documents[parent[0]].artifact_id != parent[1]
                ):
                    fail(
                        path,
                        "PARENT-IDENTITY",
                        "direct indexed parent identity differs from the package path",
                    )
            entries = rows(task_path)
            binding = profiles["sdlc/task"].body_contract.task_execution  # type: ignore[union-attr]
            if not entries or binding is None:
                fail(task_path, "COMPLETION-TASK", "bound Task rows missing")
                continue
            state = documents[task_path].status or ""
            for rule, detail in task_execution_issues(entries, state, binding):
                fail(task_path, rule, detail)
            evidence = adapter.task_evidence_rows(texts[task_path], binding)
            decisions = adapter.task_acceptance_rows(texts[task_path], binding)
            if evidence is None or decisions is None:
                fail(
                    task_path,
                    "COMPLETION-ACCEPTANCE",
                    "bound evidence or criterion verdict table missing",
                )
            else:
                for rule, detail in task_contract_issues(
                    entries, evidence, decisions, state, binding
                ):
                    fail(task_path, rule, detail)
                for decision in decisions:
                    criterion_ids = task_criterion_ids(decision["Criterion"])
                    if criterion_ids and (criterion_ids[0], task_path) in assignments:
                        modern_origins.setdefault(criterion_ids[0], []).append(
                            task_path
                        )
                        if decision["Acceptance"].strip() == "accepted":
                            accepted_origins.setdefault(criterion_ids[0], []).append(
                                task_path
                            )
            for entry in entries:
                criterion_ids = task_criterion_ids(entry["Upstream criterion"])
                if criterion_ids is None:
                    continue
                raw_links = adapter._extract_links(
                    entry["Upstream criterion"], definitions_text=texts[task_path]
                )
                if len(raw_links) != len(criterion_ids) or any(
                    adapter._local_destination(task_path, link)[1] != spec_path
                    for link in raw_links
                ):
                    fail(
                        task_path,
                        "COMPLETION-UPSTREAM",
                        "Task criterion link is not its Spec",
                    )
                for criterion in criterion_ids:
                    if criterion not in defined:
                        fail(
                            task_path,
                            "COMPLETION-UPSTREAM",
                            f"unknown or foreign {criterion}",
                        )
                    else:
                        if (criterion, task_path) in assignments:
                            task_pairs.setdefault((criterion, task_path), []).append(
                                entry
                            )
                        elif state != "cancelled":
                            fail(
                                task_path,
                                "COMPLETION-TRACE",
                                f"{criterion} lacks current Plan assignment",
                            )
        if set(task_pairs) != assignments:
            fail(
                spec_path,
                "COMPLETION-TRACE",
                "Plan and Task criterion assignments differ",
            )
        for criterion in defined:
            if len(modern_origins.get(criterion, [])) > 1:
                fail(
                    spec_path,
                    "COMPLETION-ACCEPTANCE",
                    f"{criterion} has duplicate current Task verdict authors",
                )
            origins = accepted_origins.get(criterion, [])
            if len(origins) != 1:
                fail(
                    spec_path,
                    "COMPLETION-ACCEPTANCE",
                    f"{criterion} requires exactly one accepted Task origin; found {len(origins)}",
                )
        for criterion, task_path in assignments:
            for entry in task_pairs.get((criterion, task_path), []):
                effective = (
                    documents[task_path].status
                    if len(rows(task_path) or ()) == 1
                    else entry["Status"].strip()
                )
                if effective != "completed" or entry["Result"].strip() != "PASS":
                    fail(
                        task_path,
                        "COMPLETION-RESULT",
                        f"{criterion} remains {effective}/{entry['Result']}",
                    )
    return tuple(sorted(diagnostics, key=lifecycle_diagnostic_sort_key))


def _exit_code(diagnostics: Sequence[LifecycleDiagnostic]) -> int:
    return 1 if any(item.severity == "FAIL" for item in diagnostics) else 0


def _format_diagnostic(diagnostic: LifecycleDiagnostic) -> str:
    profile = diagnostic.profile or "-"
    return (
        f"{diagnostic.severity} {diagnostic.rule_id} {diagnostic.path.as_posix()} "
        f"profile={json.dumps(profile)} "
        f"expected={json.dumps(diagnostic.expected_transition)} "
        f"observed={json.dumps(diagnostic.observed_transition)} "
        f"base_mode={json.dumps(diagnostic.base_mode)} "
        f"evidence_gap={json.dumps(diagnostic.evidence_gap)}"
    )


def _validate_arguments(args: argparse.Namespace) -> None:
    refs = (args.from_ref, args.base_ref, args.to_ref)
    if args.mode in {"strict", "staged", "snapshot", "completion"} and any(
        ref is not None for ref in refs
    ):
        raise InvocationError(f"{args.mode} mode forbids ref flags")
    if args.mode == "ci" and (
        args.base_ref is None or args.to_ref is None or args.from_ref is not None
    ):
        raise InvocationError("ci mode requires only --base-ref and --to-ref")
    if args.mode == "explicit-ref" and (
        args.from_ref is None or args.to_ref is None or args.base_ref is not None
    ):
        raise InvocationError("explicit-ref mode requires only --from-ref and --to-ref")


def _parser() -> ArgumentParser:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--mode",
        choices=("strict", "staged", "ci", "explicit-ref", "snapshot", "completion"),
        default="strict",
    )
    parser.add_argument("--from-ref")
    parser.add_argument("--base-ref")
    parser.add_argument("--to-ref")
    parser.add_argument("--include-path", action="append", default=[])
    return parser


def _execute(root: Path, args: argparse.Namespace) -> int:
    _verify_repository_root(root)
    if args.mode in {"staged", "completion"}:
        assert_staged_authority_matches_worktree(root, CURRENT_REGISTRY_PATH)
    if args.mode == "completion":
        for authority in COMPLETION_AUTHORITY_PATHS[1:]:
            assert_staged_authority_matches_worktree(root, authority)
    registry = load_registry(root)
    include_paths = _normalize_include_paths(registry, args.include_path)
    if args.mode == "completion":
        diagnostics, index_digest = _evaluate_completion(root, registry, include_paths)
        print(f"INDEX-SNAPSHOT sha256={index_digest}")
    elif args.mode == "snapshot":
        diagnostics = _evaluate_snapshot(root, registry, include_paths)
    else:
        comparison_mode = "staged" if args.mode == "strict" else args.mode
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode=comparison_mode,
            from_ref=args.from_ref,
            base_ref=args.base_ref,
            to_ref=args.to_ref,
            include_paths=include_paths,
        )
    for diagnostic in sorted(diagnostics, key=lifecycle_diagnostic_sort_key):
        print(_format_diagnostic(diagnostic))
    result = _exit_code(diagnostics)
    if result == 0 and not diagnostics:
        print(f"PASS lifecycle validation mode={args.mode}")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    error_mode = "unknown"
    try:
        args = _parser().parse_args(argv)
        if args.mode in {
            "strict",
            "staged",
            "ci",
            "explicit-ref",
            "snapshot",
            "completion",
        }:
            error_mode = args.mode
        _validate_arguments(args)
        root = Path(args.root).resolve()
        if not root.is_dir():
            raise InvocationError("--root must be an existing directory")
        with _git_environment_scope():
            return _execute(root, args)
    except (
        AuthorityError,
        InvocationError,
        DocumentContractError,
        OSError,
        ValueError,
    ) as exc:
        diagnostic = LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-BASE",
            path=PurePosixPath("."),
            profile="",
            expected_transition=(
                "valid invocation, unique commit refs, and one comparison base"
            ),
            observed_transition=str(exc),
            base_mode=error_mode,  # type: ignore[arg-type]
            evidence_gap="argument or Git provenance",
        )
        print(_format_diagnostic(diagnostic), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
