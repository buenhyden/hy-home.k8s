#!/usr/bin/env python3
"""Validate registry-owned document lifecycle events against deterministic Git bases."""

from __future__ import annotations

import argparse
import copy
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Mapping, Sequence

from document_contracts import (
    ROOT_FILES,
    TARGET_ROOTS,
    DocumentContractError,
    Registry,
    classify_path,
    enumerate_target_markdown,
    load_json_file,
    load_registry,
    read_repository_text,
)
from document_lifecycle import (
    LIFECYCLE_RULE_IDS,
    LifecycleDiagnostic,
    LifecycleDocument,
    LifecycleRename,
    compare_lifecycle,
    document_from_text,
    lifecycle_diagnostic_sort_key,
    validate_snapshot_documents,
)


FIXTURE_PATH = PurePosixPath("tests/fixtures/document-lifecycle.json")
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
    "diff.renameLimit=0",
    "-c",
    "diff.renames=true",
)
EXPECTED_ENTRYPOINTS = (
    "scripts/document_lifecycle.py",
    "scripts/validate-document-lifecycle.py",
)
EXPECTED_RULE_IDS = (
    "LIFECYCLE-CREATE",
    "LIFECYCLE-DELETE",
    "LIFECYCLE-RENAME",
    "LIFECYCLE-PROFILE-CHANGE",
    "LIFECYCLE-STATE",
    "LIFECYCLE-EDGE",
    "LIFECYCLE-EVIDENCE",
    "LIFECYCLE-BASE",
    "LIFECYCLE-BASE-DEFER",
)
EXPECTED_FORWARD_CASE_NAMES = (
    "product",
    "architecture-requirement",
    "architecture-decision",
    "specification",
    "execution",
    "operations",
    "reference-governance",
)
EXPECTED_COMPARISON_CASE_NAMES = (
    "unchanged-valid-state",
    "skipped-edge",
    "reverse-edge",
    "terminal-reopen",
    "archive-reactivation",
    "same-path-profile-change",
    "same-path-unclassified-state",
    "invalid-base-state",
    "missing-proposed-state",
)
EXPECTED_ADMISSION_CASE_NAMES = (
    "draft-create-allowed",
    "active-create-denied",
    "unclassified-create-denied",
    "unclassified-delete-denied",
    "paired-draft-create-allowed",
    "paired-active-create-allowed",
    "paired-orphan-create-denied",
    "paired-state-mismatch-denied",
    "multiple-pairs-create-denied",
    "snapshot-only-create-denied",
    "delete-denied",
    "exact-rename-single-event",
)
EXPECTED_GIT_CASE_NAMES = (
    "staged-head-index-worktree-pass",
    "staged-head-index-worktree-fail",
    "staged-add",
    "staged-delete",
    "staged-exact-rename",
    "staged-modified-rename",
    "staged-modified-governed-to-unclassified",
    "staged-modified-unclassified-to-governed",
    "staged-modified-unclassified-to-unclassified",
    "staged-governed-to-unclassified-rename",
    "staged-unclassified-to-unclassified-rename",
    "staged-unclassified-add",
    "staged-unclassified-delete",
    "staged-unclassified-modify",
    "staged-same-path-profile-change",
    "staged-unknown-type-state",
    "staged-paired-create",
    "include-does-not-filter-violation",
    "staged-submodule-ignore-all",
    "ci-merge-base",
    "ci-no-merge-base",
    "ci-ambiguous-merge-base",
    "explicit-ref-pass",
    "explicit-ref-fail",
    "explicit-ref-submodule-ignore-all",
    "missing-ref",
    "ambiguous-ref",
    "raw-tree-ref",
    "raw-blob-ref",
    "annotated-tag-ref",
    "lightweight-commit-tag-pass",
    "git-environment-steering",
    "non-worktree-root",
    "wrong-worktree-root",
    "bare-root",
)
EXPECTED_ARGUMENT_CASE_NAMES = (
    "staged-forbids-refs",
    "ci-requires-base",
    "ci-requires-to",
    "explicit-requires-from",
    "explicit-requires-to",
    "snapshot-forbids-refs",
    "invalid-mode",
)
EXPECTED_INCLUDE_CASE_NAMES = (
    "duplicate",
    "noncanonical",
    "parent",
    "non-target",
    "missing-blob",
)
EXPECTED_SNAPSHOT_CASE_NAME = "exactly-one-base-defer"
FIXTURE_MUTATION_COUNT = 13


class InvocationError(ValueError):
    """Invalid CLI, ref, base, Git object, or include-path provenance."""


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser that returns deterministic exit 2 through ``main``."""

    def error(self, message: str) -> None:
        raise InvocationError(message)


@dataclass(frozen=True)
class Change:
    kind: str
    path: PurePosixPath
    old_path: PurePosixPath | None = None

    @property
    def paths(self) -> tuple[PurePosixPath, ...]:
        return (self.old_path, self.path) if self.old_path is not None else (self.path,)


def _sanitized_git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment.update(FIXED_GIT_ENVIRONMENT)
    return environment


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


def _git_process(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *GIT_GLOBAL_ARGUMENTS, *arguments],
        cwd=root,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=_sanitized_git_environment(),
    )


def _run_git(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    allow_stderr: bool = False,
) -> bytes:
    completed = _git_process(root, arguments, input_bytes=input_bytes)
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
    if path.as_posix() == "RTK.md" or path.parts[0] in {".worktrees", "graphify-out"}:
        return False
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
    completed = _git_process(
        root,
        ("rev-parse", "--verify", "--end-of-options", reference),
    )
    lines = completed.stdout.decode("ascii", errors="ignore").splitlines()
    if (
        completed.returncode != 0
        or completed.stderr
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


def _index_blob_oid(root: Path, path: PurePosixPath) -> str | None:
    raw = _run_git(root, ("ls-files", "--stage", "-z", "--", path.as_posix()))
    if raw == b"":
        return None
    records = raw.split(b"\0")
    if records[-1] != b"" or len(records) != 2:
        raise InvocationError(f"ambiguous index path: {path.as_posix()}")
    try:
        header, raw_path = records[0].split(b"\t", 1)
        mode, oid, stage = header.split(b" ", 2)
    except ValueError as exc:
        raise InvocationError("malformed git ls-files output") from exc
    if (
        _decode_path(raw_path) != path
        or mode not in {b"100644", b"100755"}
        or stage != b"0"
        or OBJECT_ID.fullmatch(oid.decode("ascii", errors="ignore")) is None
    ):
        raise InvocationError(f"index path is not one stage-zero regular blob: {path}")
    return oid.decode("ascii")


def _blob_text(
    root: Path,
    oid: str | None,
    path: PurePosixPath,
) -> str | None:
    if oid is None:
        return None
    raw = _run_git(root, ("cat-file", "blob", oid))
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvocationError(f"document blob is not UTF-8: {path.as_posix()}") from exc


def _select_changes(
    changes: Sequence[Change],
    include_paths: Sequence[PurePosixPath],
    *,
    base_oid: Callable[[PurePosixPath], str | None],
    proposed_oid: Callable[[PurePosixPath], str | None],
) -> tuple[Change, ...]:
    target_changes = [
        change
        for change in changes
        if any(_approved_markdown(path) for path in change.paths)
    ]
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
    registry: Registry,
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
        path: PurePosixPath,
        oid: str | None,
    ) -> LifecycleDocument | None:
        text = _blob_text(root, oid, path)
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
            base = load(change.old_path, base_oid(change.old_path))
            proposed = load(change.path, proposed_oid(change.path))
            if base is None or proposed is None:
                raise InvocationError("exact rename lacks a base or proposed blob")
            base_documents[change.old_path] = base
            proposed_documents[change.path] = proposed
            renames.append(LifecycleRename(change.old_path, change.path))
        elif change.kind == "A":
            proposed = load(change.path, proposed_oid(change.path))
            if proposed is None:
                raise InvocationError(f"added path lacks proposed blob: {change.path}")
            proposed_documents[change.path] = proposed
        elif change.kind == "D":
            base = load(change.path, base_oid(change.path))
            if base is None:
                raise InvocationError(f"deleted path lacks base blob: {change.path}")
            base_documents[change.path] = base
        else:
            base = load(change.path, base_oid(change.path))
            proposed = load(change.path, proposed_oid(change.path))
            if base is None or proposed is None:
                raise InvocationError(
                    f"modified path lacks one comparison blob: {change.path}"
                )
            base_documents[change.path] = base
            proposed_documents[change.path] = proposed
    return base_documents, proposed_documents, tuple(renames)


def _evaluate_comparison(
    root: Path,
    registry: Registry,
    *,
    mode: str,
    from_ref: str | None = None,
    base_ref: str | None = None,
    to_ref: str | None = None,
    include_paths: Sequence[PurePosixPath] = (),
) -> tuple[LifecycleDiagnostic, ...]:
    _verify_repository_root(root)
    if mode == "staged":
        base_commit = _resolve_commit(root, "HEAD", "HEAD")

        def base_oid(path: PurePosixPath) -> str | None:
            return _tree_blob_oid(root, base_commit, path)

        def proposed_oid(path: PurePosixPath) -> str | None:
            return _index_blob_oid(root, path)

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

        def base_oid(path: PurePosixPath) -> str | None:
            return _tree_blob_oid(root, base_commit, path)

        def proposed_oid(path: PurePosixPath) -> str | None:
            return _tree_blob_oid(root, proposed_commit, path)

        changes = _tree_changes(root, base_commit, proposed_commit)
    selected = _select_changes(
        changes,
        include_paths,
        base_oid=base_oid,
        proposed_oid=proposed_oid,
    )
    base_documents, proposed_documents, renames = _comparison_documents(
        root,
        registry,
        selected,
        base_oid=base_oid,
        proposed_oid=proposed_oid,
    )
    return compare_lifecycle(
        registry,
        base_documents,
        proposed_documents,
        renames=renames,
        base_mode=mode,  # type: ignore[arg-type]
    )


def _evaluate_snapshot(
    root: Path,
    registry: Registry,
    include_paths: Sequence[PurePosixPath],
) -> tuple[LifecycleDiagnostic, ...]:
    _verify_repository_root(root)
    inventory = enumerate_target_markdown(root, include_paths=tuple(include_paths))
    documents = [
        document_from_text(registry, path, read_repository_text(root, path))
        for path in inventory.current_paths
    ]
    return validate_snapshot_documents(registry, documents)


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
    if args.self_test:
        if (
            args.mode is not None
            or any(ref is not None for ref in refs)
            or args.include_path
        ):
            raise InvocationError("--self-test accepts only --root")
        return
    if args.mode is None:
        raise InvocationError("--mode is required unless --self-test is selected")
    if args.mode in {"staged", "snapshot"} and any(ref is not None for ref in refs):
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
    parser.add_argument("--mode", choices=("staged", "ci", "explicit-ref", "snapshot"))
    parser.add_argument("--from-ref")
    parser.add_argument("--base-ref")
    parser.add_argument("--to-ref")
    parser.add_argument("--include-path", action="append", default=[])
    parser.add_argument("--self-test", action="store_true")
    return parser


def _document(path: str, profile_id: str, status: str | None) -> LifecycleDocument:
    return LifecycleDocument(PurePosixPath(path), profile_id, status)


def _rule_ids(diagnostics: Sequence[LifecycleDiagnostic]) -> list[str]:
    return [item.rule_id for item in diagnostics]


def _fixture_document_text(
    profile_id: str,
    status: str,
    *,
    claimed_profile_id: str | None = None,
) -> str:
    return (
        "---\n"
        "title: 'Lifecycle fixture'\n"
        f"type: {claimed_profile_id or profile_id}\n"
        f"status: {status}\n"
        "owner: platform\n"
        "updated: 2099-01-01\n"
        "---\n\n"
        "# Lifecycle fixture\n"
    )


def _write_fixture_document(
    root: Path,
    path: str,
    profile_id: str,
    status: str,
    *,
    claimed_profile_id: str | None = None,
) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _fixture_document_text(
            profile_id,
            status,
            claimed_profile_id=claimed_profile_id,
        ),
        encoding="utf-8",
    )


def _git_fixture(root: Path, *arguments: str, input_bytes: bytes | None = None) -> str:
    return _run_git(root, arguments, input_bytes=input_bytes).decode("utf-8").strip()


def _init_fixture_repo(root: Path) -> None:
    _git_fixture(root, "init", "-q")


def _commit_fixture(root: Path, message: str) -> str:
    _git_fixture(root, "add", "--all")
    _git_fixture(root, "commit", "-q", "--allow-empty", "-m", message)
    return _git_fixture(root, "rev-parse", "HEAD")


def _configure_submodule_ignore_fixture(root: Path, path: str) -> None:
    (root / ".gitmodules").write_text(
        f'[submodule "governed"]\n\tpath = {path}\n\turl = ./unused\n\tignore = all\n',
        encoding="utf-8",
    )
    _git_fixture(root, "config", "diff.ignoreSubmodules", "all")


def _git_case(
    name: str,
    root: Path,
    registry: Registry,
    contract_root: Path,
) -> tuple[int, list[str]]:
    spec_path = "docs/03.specs/900-example/spec.md"
    if name in {
        "staged-head-index-worktree-pass",
        "staged-head-index-worktree-fail",
        "staged-delete",
        "staged-exact-rename",
        "staged-modified-rename",
        "staged-modified-governed-to-unclassified",
        "staged-governed-to-unclassified-rename",
        "staged-same-path-profile-change",
        "staged-unknown-type-state",
        "explicit-ref-pass",
        "explicit-ref-fail",
        "ci-merge-base",
        "include-does-not-filter-violation",
        "git-environment-steering",
        "staged-submodule-ignore-all",
        "explicit-ref-submodule-ignore-all",
    }:
        _write_fixture_document(root, spec_path, "sdlc/spec", "draft")
    if name in {
        "staged-modified-unclassified-to-governed",
        "staged-modified-unclassified-to-unclassified",
        "staged-unclassified-to-unclassified-rename",
        "staged-unclassified-delete",
        "staged-unclassified-modify",
    }:
        _write_fixture_document(
            root,
            "docs/__unclassified__/source.md",
            "sdlc/spec",
            "draft",
        )
    if name == "include-does-not-filter-violation":
        _write_fixture_document(
            root,
            "docs/03.specs/901-clean/spec.md",
            "sdlc/spec",
            "draft",
        )
    if name in {
        "staged-submodule-ignore-all",
        "explicit-ref-submodule-ignore-all",
    }:
        _configure_submodule_ignore_fixture(root, spec_path)
    base_commit = _commit_fixture(root, "base")

    if name == "staged-head-index-worktree-pass":
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-head-index-worktree-fail":
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        _git_fixture(root, "add", "--", spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-add":
        _write_fixture_document(root, spec_path, "sdlc/spec", "draft")
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-delete":
        (root / spec_path).unlink()
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-exact-rename":
        new_path = "docs/03.specs/901-example/spec.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-rename":
        new_path = "docs/03.specs/901-example/spec.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        _write_fixture_document(root, new_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-governed-to-unclassified":
        new_path = "docs/__unclassified__/destination.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        _write_fixture_document(root, new_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-unclassified-to-governed":
        old_path = "docs/__unclassified__/source.md"
        (root / spec_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", old_path, spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-unclassified-to-unclassified":
        old_path = "docs/__unclassified__/source.md"
        new_path = "docs/__unclassified__/destination.md"
        _git_fixture(root, "mv", old_path, new_path)
        _write_fixture_document(root, new_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-governed-to-unclassified-rename":
        new_path = "docs/__unclassified__/renamed.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-to-unclassified-rename":
        old_path = "docs/__unclassified__/source.md"
        new_path = "docs/__unclassified__/destination.md"
        _git_fixture(root, "mv", old_path, new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-add":
        new_path = "docs/__unclassified__/new.md"
        _write_fixture_document(root, new_path, "sdlc/spec", "draft")
        _git_fixture(root, "add", "--", new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-delete":
        old_path = "docs/__unclassified__/source.md"
        (root / old_path).unlink()
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-modify":
        path = "docs/__unclassified__/source.md"
        _write_fixture_document(root, path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-same-path-profile-change":
        _write_fixture_document(
            root,
            spec_path,
            "sdlc/spec",
            "active",
            claimed_profile_id="sdlc/guide",
        )
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unknown-type-state":
        _write_fixture_document(
            root,
            spec_path,
            "sdlc/spec",
            "active",
            claimed_profile_id="sdlc/unknown",
        )
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-paired-create":
        _write_fixture_document(
            root, "docs/04.execution/plans/2099-01-01-example.md", "sdlc/plan", "active"
        )
        _write_fixture_document(
            root, "docs/04.execution/tasks/2099-01-01-example.md", "sdlc/task", "active"
        )
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "include-does-not-filter-violation":
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="staged",
            include_paths=(PurePosixPath("docs/03.specs/901-clean/spec.md"),),
        )
    elif name == "staged-submodule-ignore-all":
        _git_fixture(
            root,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{base_commit},{spec_path}",
        )
        try:
            _evaluate_comparison(root, registry, mode="staged")
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "explicit-ref-submodule-ignore-all":
        _git_fixture(
            root,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{base_commit},{spec_path}",
        )
        _git_fixture(root, "commit", "-q", "-m", "gitlink proposed")
        proposed = _git_fixture(root, "rev-parse", "HEAD")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref=base_commit,
                to_ref=proposed,
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name in {"explicit-ref-pass", "explicit-ref-fail"}:
        base = _git_fixture(root, "rev-parse", "HEAD")
        status = "active" if name.endswith("pass") else "done"
        _write_fixture_document(root, spec_path, "sdlc/spec", status)
        proposed = _commit_fixture(root, "proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="explicit-ref",
            from_ref=base,
            to_ref=proposed,
        )
    elif name == "ci-merge-base":
        _git_fixture(root, "branch", "proposed")
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        configured_base = _commit_fixture(root, "base advanced")
        _git_fixture(root, "switch", "-q", "proposed")
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _commit_fixture(root, "proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="ci",
            base_ref=configured_base,
            to_ref="proposed",
        )
    elif name == "ci-no-merge-base":
        base = _git_fixture(root, "rev-parse", "HEAD")
        tree = _git_fixture(root, "rev-parse", "HEAD^{tree}")
        orphan = _git_fixture(root, "commit-tree", tree, "-m", "orphan")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="ci",
                base_ref=base,
                to_ref=orphan,
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "ci-ambiguous-merge-base":
        common = _git_fixture(root, "rev-parse", "HEAD")
        tree = _git_fixture(root, "rev-parse", "HEAD^{tree}")
        left = _git_fixture(root, "commit-tree", tree, "-p", common, "-m", "left")
        right = _git_fixture(root, "commit-tree", tree, "-p", common, "-m", "right")
        merge_left = _git_fixture(
            root,
            "commit-tree",
            tree,
            "-p",
            left,
            "-p",
            right,
            "-m",
            "merge-left",
        )
        merge_right = _git_fixture(
            root,
            "commit-tree",
            tree,
            "-p",
            right,
            "-p",
            left,
            "-m",
            "merge-right",
        )
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="ci",
                base_ref=merge_left,
                to_ref=merge_right,
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "missing-ref":
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref="refs/heads/missing",
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "ambiguous-ref":
        _git_fixture(root, "branch", "ambiguous")
        _git_fixture(root, "tag", "ambiguous")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref="ambiguous",
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "raw-tree-ref":
        tree = _git_fixture(root, "rev-parse", "HEAD^{tree}")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref=tree,
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "raw-blob-ref":
        blob = _git_fixture(root, "hash-object", "-w", "--stdin", input_bytes=b"blob")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref=blob,
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "annotated-tag-ref":
        _git_fixture(root, "tag", "-a", "annotated", "-m", "annotated")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref="annotated",
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "lightweight-commit-tag-pass":
        _git_fixture(root, "tag", "lightweight", "HEAD")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="explicit-ref",
            from_ref="lightweight",
            to_ref="HEAD",
        )
    elif name == "git-environment-steering":
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        _git_fixture(root, "add", "--", spec_path)
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-alternate-"
        ) as directory:
            alternate = Path(directory)
            _init_fixture_repo(alternate)
            _commit_fixture(alternate, "clean alternate")
            attack_values = {
                "GIT_DIR": str(alternate / ".git"),
                "GIT_WORK_TREE": str(alternate),
                "GIT_INDEX_FILE": str(alternate / ".git" / "index"),
            }
            previous = {key: os.environ.get(key) for key in attack_values}
            try:
                os.environ.update(attack_values)
                caller_environment = dict(os.environ)
                diagnostics = _evaluate_comparison(root, registry, mode="staged")
                if os.environ != caller_environment:
                    raise InvocationError("Git adapter changed the caller environment")
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    snapshot_exit = main(
                        ["--root", str(contract_root), "--mode", "snapshot"]
                    )
                if snapshot_exit != 0 or os.environ != caller_environment:
                    raise InvocationError(
                        "registry/inventory Git environment scope differs"
                    )
            finally:
                for key, value in previous.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
    elif name == "wrong-worktree-root":
        nested = root / "nested"
        nested.mkdir()
        try:
            _evaluate_comparison(nested, registry, mode="staged")
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "non-worktree-root":
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-non-worktree-"
        ) as directory:
            try:
                _verify_repository_root(Path(directory))
            except InvocationError:
                return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "bare-root":
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-bare-"
        ) as directory:
            bare = Path(directory)
            _git_fixture(bare, "init", "--bare", "-q")
            try:
                _verify_repository_root(bare)
            except InvocationError:
                return 2, ["LIFECYCLE-BASE"]
        return 0, []
    else:
        raise AssertionError(f"unknown Git fixture: {name}")
    return _exit_code(diagnostics), _rule_ids(diagnostics)


def _is_string_list(value: object, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(isinstance(item, str) for item in value)
    )


def _is_rule_id_list(value: object) -> bool:
    return _is_string_list(value) and all(
        rule_id in LIFECYCLE_RULE_IDS for rule_id in value
    )


def _is_exit_code(value: object) -> bool:
    return type(value) is int and value in {0, 1, 2}


def _is_document_triple(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 3
        and isinstance(value[0], str)
        and isinstance(value[1], str)
        and (isinstance(value[2], str) or value[2] is None)
    )


def _fixture_contract_failures(fixture: object, registry: Registry) -> list[str]:
    failures: list[str] = []
    if not isinstance(fixture, dict):
        return ["fixture must be an object"]
    if type(fixture.get("schemaVersion")) is not int or fixture["schemaVersion"] != 1:
        return ["fixture schemaVersion must be integer 1"]

    expected_root_keys = {
        "schemaVersion",
        "requiredEntrypoints",
        "ruleIds",
        "forwardContracts",
        "comparisonCases",
        "admissionCases",
        "gitCases",
        "argumentCases",
        "includePathCases",
        "snapshotCase",
    }
    if set(fixture) != expected_root_keys:
        failures.append("fixture root keys differ")

    fixture_entrypoints = fixture.get("requiredEntrypoints")
    if not _is_string_list(fixture_entrypoints):
        failures.append("fixture entrypoints must be a list of strings")
    elif tuple(fixture_entrypoints) != EXPECTED_ENTRYPOINTS:
        failures.append("fixture entrypoints or order differ")

    fixture_rule_ids = fixture.get("ruleIds")
    if not _is_string_list(fixture_rule_ids):
        failures.append("stable lifecycle rule IDs must be a list of strings")
    elif (
        tuple(fixture_rule_ids) != EXPECTED_RULE_IDS
        or frozenset(fixture_rule_ids) != LIFECYCLE_RULE_IDS
    ):
        failures.append("stable lifecycle rule IDs or order differ")

    group_contracts = (
        (
            "forwardContracts",
            EXPECTED_FORWARD_CASE_NAMES,
            {"name", "profiles", "edges"},
        ),
        (
            "comparisonCases",
            EXPECTED_COMPARISON_CASE_NAMES,
            {"name", "base", "proposed", "expectedRuleIds"},
        ),
        (
            "gitCases",
            EXPECTED_GIT_CASE_NAMES,
            {"name", "expectedExit", "expectedRuleIds"},
        ),
        (
            "argumentCases",
            EXPECTED_ARGUMENT_CASE_NAMES,
            {
                "name",
                "argv",
                "expectedExit",
                "expectedRuleIds",
                "expectedBaseMode",
            },
        ),
        (
            "includePathCases",
            EXPECTED_INCLUDE_CASE_NAMES,
            {"name", "values", "expectedExit"},
        ),
    )
    for group_name, expected_names, expected_keys in group_contracts:
        cases = fixture.get(group_name)
        if not isinstance(cases, list):
            failures.append(f"{group_name} must be a list")
            continue
        actual_names = tuple(
            case.get("name") if isinstance(case, dict) else None for case in cases
        )
        if actual_names != expected_names:
            failures.append(f"{group_name} names or order differ")
        for case in cases:
            if not isinstance(case, dict):
                failures.append(f"{group_name} contains a non-object case")
                continue
            case_name = case.get("name")
            if set(case) != expected_keys:
                failures.append(f"{group_name} keys differ: {case_name}")

            if group_name == "forwardContracts":
                profiles = case.get("profiles")
                edges = case.get("edges")
                if not _is_string_list(profiles, nonempty=True):
                    failures.append(f"forwardContracts profiles differ: {case_name}")
                if not (
                    isinstance(edges, list)
                    and bool(edges)
                    and all(
                        isinstance(edge, list)
                        and len(edge) == 2
                        and all(isinstance(state, str) for state in edge)
                        for edge in edges
                    )
                ):
                    failures.append(f"forwardContracts edges differ: {case_name}")
            elif group_name == "comparisonCases":
                if not _is_document_triple(case.get("base")):
                    failures.append(f"comparisonCases base differs: {case_name}")
                if not _is_document_triple(case.get("proposed")):
                    failures.append(f"comparisonCases proposed differs: {case_name}")
                if not _is_rule_id_list(case.get("expectedRuleIds")):
                    failures.append(f"comparisonCases rule IDs differ: {case_name}")
            elif group_name == "gitCases":
                if not _is_exit_code(case.get("expectedExit")):
                    failures.append(f"gitCases exit differs: {case_name}")
                if not _is_rule_id_list(case.get("expectedRuleIds")):
                    failures.append(f"gitCases rule IDs differ: {case_name}")
            elif group_name == "argumentCases":
                if not _is_string_list(case.get("argv")):
                    failures.append(f"argumentCases argv differs: {case_name}")
                if not _is_exit_code(case.get("expectedExit")):
                    failures.append(f"argumentCases exit differs: {case_name}")
                expected_rules = case.get("expectedRuleIds")
                if not _is_rule_id_list(expected_rules):
                    failures.append(f"argumentCases rule IDs differ: {case_name}")
                elif expected_rules != ["LIFECYCLE-BASE"]:
                    failures.append(f"argumentCases base rule differs: {case_name}")
                expected_base_mode = case.get("expectedBaseMode")
                if not isinstance(
                    expected_base_mode, str
                ) or expected_base_mode not in {
                    "staged",
                    "ci",
                    "explicit-ref",
                    "snapshot",
                    "unknown",
                }:
                    failures.append(f"argumentCases base mode differs: {case_name}")
            elif group_name == "includePathCases":
                if not _is_string_list(case.get("values"), nonempty=True):
                    failures.append(f"includePathCases values differ: {case_name}")
                if not _is_exit_code(case.get("expectedExit")):
                    failures.append(f"includePathCases exit differs: {case_name}")

    admission_cases = fixture.get("admissionCases")
    if not isinstance(admission_cases, list):
        failures.append("admissionCases must be a list")
    else:
        actual_names = tuple(
            case.get("name") if isinstance(case, dict) else None
            for case in admission_cases
        )
        if actual_names != EXPECTED_ADMISSION_CASE_NAMES:
            failures.append("admissionCases names or order differ")
        for case in admission_cases:
            if not isinstance(case, dict):
                failures.append("admissionCases contains a non-object case")
                continue
            case_name = case.get("name")
            operation = case.get("operation", "create")
            operation_is_valid = isinstance(operation, str) and operation in {
                "create",
                "delete",
                "rename",
            }
            expected_keys = {"name", "documents", "expectedRuleIds"}
            if operation_is_valid and operation in {"delete", "rename"}:
                expected_keys.add("operation")
            if set(case) != expected_keys:
                failures.append(f"admissionCases keys differ: {case_name}")
            if not operation_is_valid:
                failures.append(f"admissionCases operation differs: {case_name}")
            documents = case.get("documents")
            if not (
                isinstance(documents, list)
                and bool(documents)
                and all(_is_document_triple(document) for document in documents)
            ):
                failures.append(f"admissionCases documents differ: {case_name}")
            if not _is_rule_id_list(case.get("expectedRuleIds")):
                failures.append(f"admissionCases rule IDs differ: {case_name}")

    snapshot = fixture.get("snapshotCase")
    if not isinstance(snapshot, dict):
        failures.append("snapshotCase must be an object")
    else:
        if set(snapshot) != {"name", "expectedExit", "expectedRuleIds"}:
            failures.append("snapshotCase keys differ")
        if snapshot.get("name") != EXPECTED_SNAPSHOT_CASE_NAME:
            failures.append("snapshotCase name differs")
        if not _is_exit_code(snapshot.get("expectedExit")):
            failures.append("snapshotCase exit differs")
        if not _is_rule_id_list(snapshot.get("expectedRuleIds")):
            failures.append("snapshotCase rule IDs differ")

    if failures:
        return failures

    fixture_projection = [
        (profile_id, edge[0], edge[1])
        for contract in fixture["forwardContracts"]
        for profile_id in contract["profiles"]
        for edge in contract["edges"]
    ]
    production_projection = [
        (profile.profile_id, edge.from_state, edge.to_state)
        for profile in registry.profiles
        for edge in profile.lifecycle.edges
    ]
    if len(fixture_projection) != len(set(fixture_projection)):
        failures.append("fixture lifecycle edge projection contains duplicates")
    if sorted(fixture_projection) != sorted(production_projection):
        failures.append("fixture lifecycle edge projection differs from production")
    return failures


def _fixture_mutation_probe_failures(
    fixture: dict[str, object], registry: Registry
) -> list[str]:
    probes: list[tuple[str, dict[str, object]]] = []

    missing_operations = copy.deepcopy(fixture)
    missing_operations["forwardContracts"] = [
        case
        for case in missing_operations["forwardContracts"]
        if case["name"] != "operations"
    ]
    probes.append(("missing operations family", missing_operations))

    missing_skip = copy.deepcopy(fixture)
    missing_skip["comparisonCases"] = [
        case
        for case in missing_skip["comparisonCases"]
        if case["name"] != "skipped-edge"
    ]
    probes.append(("missing skipped edge", missing_skip))

    missing_active_create = copy.deepcopy(fixture)
    missing_active_create["admissionCases"] = [
        case
        for case in missing_active_create["admissionCases"]
        if case["name"] != "active-create-denied"
    ]
    probes.append(("missing active create denial", missing_active_create))

    duplicate_case = copy.deepcopy(fixture)
    duplicate_case["gitCases"].append(copy.deepcopy(duplicate_case["gitCases"][0]))
    probes.append(("duplicate Git case", duplicate_case))

    unknown_case = copy.deepcopy(fixture)
    unknown_case["includePathCases"][0]["name"] = "unknown-case"
    probes.append(("unknown include case", unknown_case))

    malformed_member = copy.deepcopy(fixture)
    malformed_member["admissionCases"][0] = None
    probes.append(("malformed list member", malformed_member))

    null_comparison_base = copy.deepcopy(fixture)
    null_comparison_base["comparisonCases"][0]["base"] = None
    probes.append(("null comparison base", null_comparison_base))

    null_admission_documents = copy.deepcopy(fixture)
    null_admission_documents["admissionCases"][0]["documents"] = None
    probes.append(("null admission documents", null_admission_documents))

    malformed_status = copy.deepcopy(fixture)
    malformed_status["comparisonCases"][0]["proposed"][2] = 7
    probes.append(("malformed comparison status", malformed_status))

    malformed_exit = copy.deepcopy(fixture)
    malformed_exit["gitCases"][0]["expectedExit"] = None
    probes.append(("malformed expected exit", malformed_exit))

    malformed_nested_member = copy.deepcopy(fixture)
    malformed_nested_member["argumentCases"][0]["argv"][0] = None
    probes.append(("malformed argv member", malformed_nested_member))

    unhashable_base_mode = copy.deepcopy(fixture)
    unhashable_base_mode["argumentCases"][0]["expectedBaseMode"] = []
    probes.append(("unhashable argument base mode", unhashable_base_mode))

    unhashable_operation = copy.deepcopy(fixture)
    unhashable_operation["admissionCases"][0]["operation"] = {}
    probes.append(("unhashable admission operation", unhashable_operation))

    failures: list[str] = []
    for name, candidate in probes:
        if not _fixture_contract_failures(candidate, registry):
            failures.append(f"fixture mutation accepted: {name}")
    return failures


def _run_self_test(root: Path) -> list[str]:
    failures: list[str] = []
    fixture = load_json_file(root / FIXTURE_PATH, diagnostic_path=FIXTURE_PATH)
    registry = load_registry(root)
    if not isinstance(fixture, dict):
        return ["fixture must be an object"]
    contract_failures = _fixture_contract_failures(fixture, registry)
    failures.extend(contract_failures)
    if contract_failures:
        return failures
    failures.extend(_fixture_mutation_probe_failures(fixture, registry))
    for entrypoint in fixture.get("requiredEntrypoints", []):
        if not (root / entrypoint).is_file():
            failures.append(f"missing public entrypoint: {entrypoint}")

    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    forward_count = 0
    for contract in fixture.get("forwardContracts", []):
        literal_edges = {tuple(edge) for edge in contract["edges"]}
        for profile_id in contract["profiles"]:
            profile = profile_map.get(profile_id)
            if profile is None:
                failures.append(f"forward {contract['name']}: unknown {profile_id}")
                continue
            production_edges = {
                (edge.from_state, edge.to_state) for edge in profile.lifecycle.edges
            }
            if production_edges != literal_edges:
                failures.append(
                    f"forward {contract['name']}/{profile_id}: literal edge set differs"
                )
                continue
            for from_state, to_state in contract["edges"]:
                path = PurePosixPath(f"docs/__lifecycle__/{forward_count}.md")
                diagnostics = compare_lifecycle(
                    registry,
                    {path: LifecycleDocument(path, profile_id, from_state)},
                    {path: LifecycleDocument(path, profile_id, to_state)},
                    base_mode="explicit-ref",
                )
                if diagnostics:
                    failures.append(
                        f"forward {contract['name']}/{profile_id}/{from_state}-{to_state}: rejected"
                    )
                forward_count += 1

    for case in fixture.get("comparisonCases", []):
        base = _document(*case["base"])
        proposed = _document(*case["proposed"])
        actual = _rule_ids(
            compare_lifecycle(
                registry,
                {base.path: base},
                {proposed.path: proposed},
                base_mode="explicit-ref",
            )
        )
        if actual != case["expectedRuleIds"]:
            failures.append(
                f"comparison {case['name']}: expected {case['expectedRuleIds']}, actual {actual}"
            )

    for case in fixture.get("admissionCases", []):
        documents = [_document(*item) for item in case["documents"]]
        operation = case.get("operation", "create")
        if operation == "create":
            diagnostics = compare_lifecycle(
                registry,
                {},
                {item.path: item for item in documents},
                base_mode="staged",
            )
        elif operation == "delete":
            diagnostics = compare_lifecycle(
                registry,
                {item.path: item for item in documents},
                {},
                base_mode="staged",
            )
        elif operation == "rename":
            base, proposed = documents
            diagnostics = compare_lifecycle(
                registry,
                {base.path: base},
                {proposed.path: proposed},
                renames=(LifecycleRename(base.path, proposed.path),),
                base_mode="staged",
            )
        else:
            failures.append(f"admission {case['name']}: unknown operation")
            continue
        actual = _rule_ids(diagnostics)
        if actual != case["expectedRuleIds"]:
            failures.append(
                f"admission {case['name']}: expected {case['expectedRuleIds']}, actual {actual}"
            )

    for case in fixture.get("gitCases", []):
        with tempfile.TemporaryDirectory(prefix="document-lifecycle-") as directory:
            repo = Path(directory)
            _init_fixture_repo(repo)
            try:
                actual_exit, actual_rules = _git_case(
                    case["name"], repo, registry, root
                )
            except (InvocationError, OSError, ValueError) as exc:
                failures.append(f"git {case['name']}: unexpected error {exc}")
                continue
        if actual_exit != case["expectedExit"]:
            failures.append(
                f"git {case['name']}: expected exit {case['expectedExit']}, actual {actual_exit}"
            )
        if actual_rules != case["expectedRuleIds"]:
            failures.append(
                f"git {case['name']}: expected rules {case['expectedRuleIds']}, actual {actual_rules}"
            )

    for case in fixture.get("argumentCases", []):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            actual_exit = main(["--root", str(root), *case["argv"]])
        if actual_exit != case["expectedExit"]:
            failures.append(
                f"argument {case['name']}: expected exit {case['expectedExit']}, actual {actual_exit}"
            )
        error_line = stderr.getvalue().strip()
        if (
            not error_line.startswith("FAIL LIFECYCLE-BASE . ")
            or f"base_mode={json.dumps(case['expectedBaseMode'])}" not in error_line
            or "profile=" not in error_line
            or "expected=" not in error_line
            or "observed=" not in error_line
            or "evidence_gap=" not in error_line
        ):
            failures.append(
                f"argument {case['name']}: base diagnostic envelope differs"
            )

    for case in fixture.get("includePathCases", []):
        try:
            paths = _normalize_include_paths(registry, case["values"])
            if case["name"] == "missing-blob":
                with tempfile.TemporaryDirectory(
                    prefix="document-lifecycle-include-"
                ) as directory:
                    repo = Path(directory)
                    _init_fixture_repo(repo)
                    _commit_fixture(repo, "base")
                    _evaluate_comparison(
                        repo,
                        registry,
                        mode="staged",
                        include_paths=paths,
                    )
            actual_exit = 0
        except (InvocationError, DocumentContractError, OSError, ValueError):
            actual_exit = 2
        if actual_exit != case["expectedExit"]:
            failures.append(
                f"include {case['name']}: expected exit {case['expectedExit']}, actual {actual_exit}"
            )

    snapshot = fixture["snapshotCase"]
    diagnostics = _evaluate_snapshot(root, registry, ())
    actual_rules = _rule_ids(diagnostics)
    if (
        _exit_code(diagnostics) != snapshot["expectedExit"]
        or actual_rules != snapshot["expectedRuleIds"]
        or sum(item.severity == "DEFER" for item in diagnostics) != 1
    ):
        failures.append(
            f"snapshot {snapshot['name']}: expected one DEFER only, actual {actual_rules}"
        )
    if any(item.rule_id == "LIFECYCLE-EVIDENCE" for item in diagnostics):
        failures.append("snapshot evaluated DSLC-004 evidence predicates")
    return failures


def _execute(root: Path, args: argparse.Namespace) -> int:
    _verify_repository_root(root)
    if args.self_test:
        failures = _run_self_test(root)
        if failures:
            for failure in failures:
                print(f"FAIL SELF-TEST {failure}")
            return 1
        fixture = load_json_file(root / FIXTURE_PATH, diagnostic_path=FIXTURE_PATH)
        forward_count = sum(
            len(item["profiles"]) * len(item["edges"])
            for item in fixture["forwardContracts"]
        )
        total = (
            forward_count
            + len(fixture["comparisonCases"])
            + len(fixture["admissionCases"])
            + len(fixture["gitCases"])
            + len(fixture["argumentCases"])
            + len(fixture["includePathCases"])
            + 1
            + FIXTURE_MUTATION_COUNT
        )
        print(
            "PASS lifecycle self-test "
            f"({total} cases: {forward_count} forward edges, "
            f"{len(fixture['comparisonCases'])} comparisons, "
            f"{len(fixture['admissionCases'])} admissions, "
            f"{len(fixture['gitCases'])} Git bases, "
            f"{len(fixture['argumentCases'])} arguments, "
            f"{len(fixture['includePathCases'])} includes, 1 snapshot, "
            f"{FIXTURE_MUTATION_COUNT} fixture mutations)"
        )
        return 0
    registry = load_registry(root)
    include_paths = _normalize_include_paths(registry, args.include_path)
    if args.mode == "snapshot":
        diagnostics = _evaluate_snapshot(root, registry, include_paths)
    else:
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode=args.mode,
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
        if args.mode in {"staged", "ci", "explicit-ref", "snapshot"}:
            error_mode = args.mode
        _validate_arguments(args)
        root = Path(args.root).resolve()
        if not root.is_dir():
            raise InvocationError("--root must be an existing directory")
        with _git_environment_scope():
            return _execute(root, args)
    except (InvocationError, DocumentContractError, OSError, ValueError) as exc:
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
