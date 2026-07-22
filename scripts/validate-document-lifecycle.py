#!/usr/bin/env python3
"""Validate registry-owned document lifecycle events against deterministic Git bases."""

from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from types import MappingProxyType, ModuleType
from typing import Callable, Mapping, Sequence

from archive_cutover_manifest import (
    ARCHIVE_PROFILE,
    ARCHIVE_TEMPLATE,
    ARCHIVE_TEMPLATE_PROFILE,
    BASE_REGISTRY_BLOB_OID,
    BASE_REGISTRY_ID,
    BASE_REGISTRY_VERSION,
    CUTOVER_BASE_COMMIT,
    EXPECTED_ARCHIVE_PATHS,
    LEGACY_ARCHIVE_PROFILE,
    LEGACY_ARCHIVE_TEMPLATE,
    LEGACY_ARCHIVE_TEMPLATE_PROFILE,
    PROPOSED_REGISTRY_ID,
    PROPOSED_REGISTRY_BLOB_OID,
    PROPOSED_REGISTRY_VERSION,
)
from document_contracts import (
    REGISTRY_PATH,
    ROOT_FILES,
    TARGET_ROOTS,
    DocumentContractError,
    DocumentProfile,
    Registry,
    Route,
    classify_path,
    enumerate_target_markdown,
    load_json_file,
    load_registry,
    read_repository_text,
)
from document_lifecycle import (
    LIFECYCLE_RULE_IDS,
    SPECIFICATION_PROFILES,
    LifecycleDiagnostic,
    LifecycleDocument,
    LifecycleEvidenceContext,
    LifecycleEvidenceDocument,
    LifecycleRename,
    compare_lifecycle,
    document_from_text,
    lifecycle_diagnostic_sort_key,
    validate_snapshot_documents,
)
from archive_validation import validate_archive_immutability


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


def _registry_profile_ids(raw_registry: Mapping[str, object]) -> frozenset[str]:
    profiles = raw_registry.get("profiles")
    if not isinstance(profiles, list):
        return frozenset()
    return frozenset(
        profile["id"]
        for profile in profiles
        if isinstance(profile, dict) and isinstance(profile.get("id"), str)
    )


def finite_archive_cutover_paths(
    *,
    mode: str,
    base_commit: str,
    base_registry_oid: str,
    proposed_registry_oid: str,
    base_registry: Mapping[str, object],
    proposed_registry: Mapping[str, object],
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
) -> frozenset[PurePosixPath]:
    """Return only the exact finite ARWB-003 events admitted for consumption."""

    if (
        mode not in {"staged", "ci"}
        or base_commit != CUTOVER_BASE_COMMIT
        or base_registry_oid != BASE_REGISTRY_BLOB_OID
        or proposed_registry_oid != PROPOSED_REGISTRY_BLOB_OID
    ):
        return frozenset()
    if (
        base_registry.get("schemaVersion") != BASE_REGISTRY_VERSION
        or base_registry.get("$id") != BASE_REGISTRY_ID
        or proposed_registry.get("schemaVersion") != PROPOSED_REGISTRY_VERSION
        or proposed_registry.get("$id") != PROPOSED_REGISTRY_ID
    ):
        return frozenset()

    base_profile_ids = _registry_profile_ids(base_registry)
    proposed_profile_ids = _registry_profile_ids(proposed_registry)
    if (
        not {LEGACY_ARCHIVE_PROFILE, LEGACY_ARCHIVE_TEMPLATE_PROFILE}
        <= base_profile_ids
        or {ARCHIVE_PROFILE, ARCHIVE_TEMPLATE_PROFILE} & base_profile_ids
        or not {ARCHIVE_PROFILE, ARCHIVE_TEMPLATE_PROFILE} <= proposed_profile_ids
        or {
            LEGACY_ARCHIVE_PROFILE,
            LEGACY_ARCHIVE_TEMPLATE_PROFILE,
        }
        & proposed_profile_ids
    ):
        return frozenset()

    expected_records = frozenset(PurePosixPath(path) for path in EXPECTED_ARCHIVE_PATHS)
    common_paths = set(base_documents) & set(proposed_documents)
    profile_changes = frozenset(
        path
        for path in common_paths
        if base_documents[path].profile_id != proposed_documents[path].profile_id
    )
    if profile_changes != expected_records:
        return frozenset()
    for path in expected_records:
        base = base_documents[path]
        proposed = proposed_documents[path]
        if (
            base.profile_id != LEGACY_ARCHIVE_PROFILE
            or base.status != "archived"
            or base.state_issue is not None
            or proposed.profile_id != ARCHIVE_PROFILE
            or proposed.status != "archived"
            or proposed.state_issue is not None
        ):
            return frozenset()

    legacy_template = PurePosixPath(LEGACY_ARCHIVE_TEMPLATE)
    archive_template = PurePosixPath(ARCHIVE_TEMPLATE)
    if (
        base_documents.get(legacy_template)
        != LifecycleDocument(
            legacy_template,
            LEGACY_ARCHIVE_TEMPLATE_PROFILE,
            None,
        )
        or legacy_template in proposed_documents
        or proposed_documents.get(archive_template)
        != LifecycleDocument(
            archive_template,
            ARCHIVE_TEMPLATE_PROFILE,
            None,
        )
        or archive_template in base_documents
    ):
        return frozenset()

    if (
        frozenset(
            path
            for path, document in base_documents.items()
            if document.profile_id == LEGACY_ARCHIVE_PROFILE
        )
        != expected_records
        or frozenset(
            path
            for path, document in proposed_documents.items()
            if document.profile_id == ARCHIVE_PROFILE
        )
        != expected_records
        or frozenset(
            path
            for path, document in base_documents.items()
            if document.profile_id == LEGACY_ARCHIVE_TEMPLATE_PROFILE
        )
        != {legacy_template}
        or frozenset(
            path
            for path, document in proposed_documents.items()
            if document.profile_id == ARCHIVE_TEMPLATE_PROFILE
        )
        != {archive_template}
    ):
        return frozenset()
    return expected_records | {legacy_template, archive_template}


def _archive_cutover_fixture_inputs(
    mode: str,
    mutation: str,
) -> dict[str, object]:
    expected_records = tuple(PurePosixPath(path) for path in EXPECTED_ARCHIVE_PATHS)
    legacy_template = PurePosixPath(LEGACY_ARCHIVE_TEMPLATE)
    archive_template = PurePosixPath(ARCHIVE_TEMPLATE)
    base_documents = {
        path: LifecycleDocument(path, LEGACY_ARCHIVE_PROFILE, "archived")
        for path in expected_records
    }
    proposed_documents = {
        path: LifecycleDocument(path, ARCHIVE_PROFILE, "archived")
        for path in expected_records
    }
    base_documents[legacy_template] = LifecycleDocument(
        legacy_template,
        LEGACY_ARCHIVE_TEMPLATE_PROFILE,
        None,
    )
    proposed_documents[archive_template] = LifecycleDocument(
        archive_template,
        ARCHIVE_TEMPLATE_PROFILE,
        None,
    )
    base_registry: dict[str, object] = {
        "$id": BASE_REGISTRY_ID,
        "schemaVersion": BASE_REGISTRY_VERSION,
        "profiles": [
            {"id": LEGACY_ARCHIVE_PROFILE},
            {"id": LEGACY_ARCHIVE_TEMPLATE_PROFILE},
        ],
    }
    proposed_registry: dict[str, object] = {
        "$id": PROPOSED_REGISTRY_ID,
        "schemaVersion": PROPOSED_REGISTRY_VERSION,
        "profiles": [
            {"id": ARCHIVE_PROFILE},
            {"id": ARCHIVE_TEMPLATE_PROFILE},
        ],
    }
    base_commit = CUTOVER_BASE_COMMIT
    base_registry_oid = BASE_REGISTRY_BLOB_OID
    proposed_registry_oid = PROPOSED_REGISTRY_BLOB_OID
    if mutation == "partial":
        proposed_documents.pop(expected_records[0])
    elif mutation == "extra":
        extra = PurePosixPath("docs/98.archive/03.specs/999-extra/spec.md")
        base_documents[extra] = LifecycleDocument(
            extra, LEGACY_ARCHIVE_PROFILE, "archived"
        )
        proposed_documents[extra] = LifecycleDocument(
            extra, ARCHIVE_PROFILE, "archived"
        )
    elif mutation == "wrong-base":
        base_commit = "0" * 40
    elif mutation == "wrong-base-registry-oid":
        base_registry_oid = "0" * 40
    elif mutation == "proposed-policy-drift":
        proposed_registry["unrelatedPolicy"] = {"mode": "changed"}
        proposed_registry_oid = "f" * 40
    elif mutation == "missing-template":
        proposed_documents.pop(archive_template)
    elif mutation == "wrong-registry-version":
        proposed_registry["schemaVersion"] = PROPOSED_REGISTRY_VERSION + 1
    elif mutation == "missing-registry-profile":
        proposed_registry["profiles"] = [{"id": ARCHIVE_PROFILE}]
    elif mutation == "unrelated-profile-change":
        unrelated = PurePosixPath("docs/03.specs/999-unrelated/spec.md")
        base_documents[unrelated] = LifecycleDocument(unrelated, "sdlc/spec", "active")
        proposed_documents[unrelated] = LifecycleDocument(
            unrelated, "sdlc/guide", "active"
        )
    elif mutation != "exact":
        raise ValueError(f"unknown archive cutover fixture mutation: {mutation}")
    return {
        "mode": mode,
        "base_commit": base_commit,
        "base_registry_oid": base_registry_oid,
        "proposed_registry_oid": proposed_registry_oid,
        "base_registry": base_registry,
        "proposed_registry": proposed_registry,
        "base_documents": base_documents,
        "proposed_documents": proposed_documents,
    }


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
    "archive-envelope-create-without-evidence-denied",
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
    "staged-paired-create-blocked-spec",
    "staged-paired-create-ready-spec-done",
    "staged-paired-create-split-spec",
    "staged-evidence-index-invalid-worktree-valid",
    "staged-evidence-index-valid-worktree-invalid",
    "include-does-not-filter-violation",
    "staged-submodule-ignore-all",
    "ci-merge-base",
    "ci-no-merge-base",
    "ci-ambiguous-merge-base",
    "explicit-ref-pass",
    "explicit-ref-fail",
    "explicit-ref-proposed-only-evidence",
    "explicit-ref-base-only-evidence-removed",
    "ci-proposed-tree-evidence",
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
EXPECTED_ARCHIVE_CUTOVER_CASE_NAMES = (
    "exact-staged",
    "exact-ci",
    "partial-record-set",
    "extra-record",
    "wrong-base",
    "wrong-base-registry-oid",
    "proposed-policy-drift",
    "missing-template-pair",
    "wrong-registry-version",
    "missing-registry-profile-pair",
    "unrelated-profile-change",
    "snapshot-not-admitted",
    "explicit-ref-not-admitted",
)
EXPECTED_ARCHIVE_CUTOVER_MUTATIONS = frozenset(
    {
        "exact",
        "partial",
        "extra",
        "wrong-base",
        "wrong-base-registry-oid",
        "proposed-policy-drift",
        "missing-template",
        "wrong-registry-version",
        "missing-registry-profile",
        "unrelated-profile-change",
    }
)
FIXTURE_MUTATION_COUNT = 24
EXPECTED_EVIDENCE_ASSERTION_SHA256 = "beb430e079bf603ebd5164666218fa178c6e27550f425c62f3fd739c31675892"  # pragma: allowlist secret
EXPECTED_EVIDENCE_VARIANTS = (
    "positive",
    "missing",
    "wrong-profile",
    "wrong-state",
    "wrong-relationship-section",
    "unchanged",
    "ambiguous-base",
    "body-contract-mismatch",
    "plain-text-path",
    "opaque-markdown",
    "orphan",
    "multiple",
)


def _dependency_ready_tranche_window(
    registry: Registry,
) -> tuple[str, str, str | None]:
    """Return the current original-tranche ready identity, state, and successor."""

    programs = [
        program for program in registry.program_lineage if program.prd_id == "006"
    ]
    if len(programs) != 1:
        raise ValueError("PRD-006 does not resolve one program lineage")
    program = programs[0]
    completed_count = sum(relation.state == "done" for relation in program.tranches)
    expected_states = tuple(
        "done" if index < completed_count else "active"
        for index in range(len(program.tranches))
    )
    actual_states = tuple(relation.state for relation in program.tranches)
    if actual_states != expected_states:
        raise ValueError(
            "PRD-006 original tranche is not one contiguous done prefix "
            "followed by an active suffix"
        )
    if completed_count == len(program.tranches):
        raise ValueError("PRD-006 has no dependency-ready original tranche")
    ready = program.tranches[completed_count]
    blocked = (
        program.tranches[completed_count + 1]
        if completed_count + 1 < len(program.tranches)
        else None
    )
    return ready.spec_id, ready.state, blocked.spec_id if blocked is not None else None


def _execution_spec_fixture_path(spec_id: str) -> PurePosixPath:
    return PurePosixPath(f"docs/03.specs/{spec_id}-evidence-fixture/spec.md")


def _registry_with_ready_spec(registry: Registry, ready_spec_id: str) -> Registry:
    """Build an isolated typed registry at one supported rollover boundary."""

    program = next(
        program for program in registry.program_lineage if program.prd_id == "006"
    )
    ready_order = next(
        relation.order
        for relation in program.tranches
        if relation.spec_id == ready_spec_id
    )
    candidate_program = replace(
        program,
        tranches=tuple(
            replace(
                relation,
                state="done" if relation.order < ready_order else "active",
            )
            for relation in program.tranches
        ),
    )
    return replace(
        registry,
        program_lineage=tuple(
            candidate_program if item.prd_id == "006" else item
            for item in registry.program_lineage
        ),
    )


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


def _blob_bytes(root: Path, oid: str) -> bytes:
    """Read one exact Git blob without decoding or worktree substitution."""

    return _run_git(root, ("cat-file", "blob", oid))


def _archive_immutability_diagnostics(
    root: Path,
    base_registry: Registry,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    *,
    mode: str,
) -> tuple[LifecycleDiagnostic, ...]:
    """Compare exact bytes for every base-selected ArchiveEnvelope record."""

    baseline: dict[str, bytes] = {}
    proposed: dict[str, bytes] = {}
    for path, oid in base_blobs.items():
        try:
            profile = classify_path(base_registry, path)
        except DocumentContractError:
            continue
        if profile.profile_id != ARCHIVE_PROFILE:
            continue
        canonical = path.as_posix()
        baseline[canonical] = _blob_bytes(root, oid)
        proposed_oid = proposed_blobs.get(path)
        if proposed_oid is not None:
            proposed[canonical] = _blob_bytes(root, proposed_oid)
    report = validate_archive_immutability(baseline, proposed)
    return tuple(
        LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=PurePosixPath(item.path),
            profile=ARCHIVE_PROFILE,
            expected_transition="existing archive record Git blob bytes remain identical",
            observed_transition=(
                "existing archive record deleted"
                if item.code == "ARCHIVE-IMMUTABLE-DELETION"
                else "existing archive record bytes changed"
            ),
            base_mode=mode,  # type: ignore[arg-type]
            evidence_gap=f"archive immutability rule {item.code}",
        )
        for item in report.diagnostics
    )


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
    text = _blob_text(root, oid, REGISTRY_PATH)
    if text is None:
        raise InvocationError("comparison snapshot lacks the document registry")
    try:
        loaded = json.loads(text, object_pairs_hook=_unique_json_object)
    except (json.JSONDecodeError, InvocationError) as exc:
        raise InvocationError("comparison registry blob is invalid JSON") from exc
    if not isinstance(loaded, dict):
        raise InvocationError("comparison registry blob is not an object")
    return MappingProxyType(loaded)


def _classification_registry(
    current_registry: Registry,
    raw_registry: Mapping[str, object],
) -> Registry:
    """Project snapshot-owned routes and IDs onto immutable lifecycle profiles."""

    raw_profiles = raw_registry.get("profiles")
    schema_version = raw_registry.get("schemaVersion")
    if not isinstance(raw_profiles, list) or type(schema_version) is not int:
        raise InvocationError("comparison registry profile projection is malformed")
    current_profiles = {
        profile.profile_id: profile for profile in current_registry.profiles
    }
    aliases = {
        LEGACY_ARCHIVE_PROFILE: ARCHIVE_PROFILE,
        LEGACY_ARCHIVE_TEMPLATE_PROFILE: ARCHIVE_TEMPLATE_PROFILE,
    }
    projected: list[DocumentProfile] = []
    for raw_profile in raw_profiles:
        if not isinstance(raw_profile, dict):
            raise InvocationError("comparison registry contains a non-object profile")
        profile_id = raw_profile.get("id")
        raw_routes = raw_profile.get("routes")
        raw_status_domain = raw_profile.get("statusDomain")
        raw_mode = raw_profile.get("mode")
        if (
            not isinstance(profile_id, str)
            or not isinstance(raw_routes, list)
            or not isinstance(raw_status_domain, list)
            or not all(isinstance(state, str) for state in raw_status_domain)
            or not isinstance(raw_mode, str)
        ):
            raise InvocationError("comparison registry profile shape is malformed")
        source = current_profiles.get(aliases.get(profile_id, profile_id))
        if source is None:
            raise InvocationError(
                "comparison registry profile has no current lifecycle projection"
            )
        routes: list[Route] = []
        for raw_route in raw_routes:
            if not isinstance(raw_route, dict):
                raise InvocationError("comparison registry route is malformed")
            kind = raw_route.get("kind")
            value = raw_route.get("value")
            if kind not in {"exact", "regex"} or not isinstance(value, str):
                raise InvocationError("comparison registry route is malformed")
            routes.append(Route(kind=kind, value=value))  # type: ignore[arg-type]
        projected.append(
            replace(
                source,
                profile_id=profile_id,
                routes=tuple(routes),
                status_domain=tuple(raw_status_domain),
                mode=raw_mode,  # type: ignore[arg-type]
            )
        )
    return replace(
        current_registry,
        schema_version=schema_version,
        profiles=tuple(projected),
    )


def _snapshot_projection(
    root: Path,
    registry: Registry,
    blobs: Mapping[PurePosixPath, str],
) -> tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]]:
    documents: dict[PurePosixPath, LifecycleDocument] = {}
    texts: dict[PurePosixPath, str] = {}
    for path in sorted(blobs, key=PurePosixPath.as_posix):
        text = _blob_text(root, blobs[path], path)
        assert text is not None
        texts[path] = text
        try:
            documents[path] = document_from_text(registry, path, text)
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
    for path, document in proposed_documents.items():
        profile = profile_map.get(document.profile_id)
        if profile is None:
            views[path] = LifecycleEvidenceDocument(
                document=document,
                all_local_links=(),
                relationship_links=(),
                unresolved_relationship_links=(),
                body_table_links=(),
                relationship_section_valid=False,
                body_contract_valid=False,
                task_terminal_evidence_valid=False,
            )
            continue
        rendered = adapter.lifecycle_markdown_evidence(
            path, proposed_texts[path], profile, snapshot_profiles
        )
        views[path] = LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=rendered.unresolved_relationship_links,
            body_table_links=rendered.body_table_links,
            relationship_section_valid=rendered.relationship_section_valid,
            body_contract_valid=rendered.body_contract_valid,
            task_terminal_evidence_valid=rendered.task_terminal_evidence_valid,
        )

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
    )


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
        registry: Registry,
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


def _comparison_requires_evidence(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
) -> bool:
    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    if any(
        document.profile_id == ARCHIVE_PROFILE and path not in base_documents
        for path, document in proposed_documents.items()
    ):
        return True
    for path in set(base_documents) & set(proposed_documents):
        base = base_documents[path]
        proposed = proposed_documents[path]
        if (
            base.profile_id != proposed.profile_id
            or base.status is None
            or proposed.status is None
            or base.status == proposed.status
        ):
            continue
        profile = profile_map.get(proposed.profile_id)
        if profile is not None and any(
            edge.from_state == base.status and edge.to_state == proposed.status
            for edge in profile.lifecycle.edges
        ):
            return True
    return any(
        document.profile_id in {"sdlc/plan", "sdlc/task"}
        and document.status in {"draft", "active"}
        for path, document in proposed_documents.items()
        if path not in base_documents
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
        proposed_registry_oid = _index_blob_oid(root, REGISTRY_PATH)
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
        proposed_registry_oid = _tree_blob_oid(root, proposed_commit, REGISTRY_PATH)

    base_registry_oid = _tree_blob_oid(root, base_commit, REGISTRY_PATH)
    base_registry_raw = _registry_blob(root, base_registry_oid)
    proposed_registry_raw = _registry_blob(root, proposed_registry_oid)
    base_classification_registry = _classification_registry(registry, base_registry_raw)
    proposed_classification_registry = _classification_registry(
        registry, proposed_registry_raw
    )

    immutability_diagnostics = _archive_immutability_diagnostics(
        root,
        base_classification_registry,
        base_blobs,
        proposed_blobs,
        mode=mode,
    )
    if immutability_diagnostics:
        return immutability_diagnostics

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
    consumed_paths = finite_archive_cutover_paths(
        mode=mode,
        base_commit=base_commit,
        base_registry_oid=base_registry_oid or "",
        proposed_registry_oid=proposed_registry_oid or "",
        base_registry=base_registry_raw,
        proposed_registry=proposed_registry_raw,
        base_documents=base_documents,
        proposed_documents=proposed_documents,
    )

    def consume_finite_cutover(
        diagnostics: Sequence[LifecycleDiagnostic],
    ) -> tuple[LifecycleDiagnostic, ...]:
        return tuple(
            diagnostic
            for diagnostic in diagnostics
            if diagnostic.path not in consumed_paths
        )

    if not _comparison_requires_evidence(
        proposed_classification_registry,
        base_documents,
        proposed_documents,
    ):
        return consume_finite_cutover(
            compare_lifecycle(
                proposed_classification_registry,
                base_documents,
                proposed_documents,
                renames=renames,
                base_mode=mode,  # type: ignore[arg-type]
            )
        )
    base_snapshot, base_texts = _snapshot_projection(
        root, base_classification_registry, base_blobs
    )
    proposed_snapshot, proposed_texts = _snapshot_projection(
        root, proposed_classification_registry, proposed_blobs
    )
    evidence = evidence_context_factory(
        proposed_classification_registry,
        base_snapshot,
        proposed_snapshot,
        base_texts,
        proposed_texts,
    )
    return consume_finite_cutover(
        compare_lifecycle(
            proposed_classification_registry,
            base_documents,
            proposed_documents,
            renames=renames,
            base_mode=mode,  # type: ignore[arg-type]
            evidence_context=evidence,
        )
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


def _fixture_link(source: PurePosixPath, target: PurePosixPath, label: str) -> str:
    relative = posixpath.relpath(target.as_posix(), source.parent.as_posix())
    return f"[{label}]({relative})"


def _opaque_fixture_link(
    source: PurePosixPath,
    target: PurePosixPath,
    label: str,
    form: int,
) -> str:
    link = _fixture_link(source, target, label)
    forms = (
        f"`{link}`",
        f"```text\n{link}\n```",
        f"<!-- {link} -->",
        f'<span data-evidence="{link}">opaque</span>',
        f"\n    {link}",
    )
    return forms[form % len(forms)]


def _evidence_fixture_text(
    profile: DocumentProfile,
    document: LifecycleDocument,
    snapshot_profiles: Mapping[PurePosixPath, str],
    relationship_targets: Sequence[PurePosixPath],
    *,
    table_targets: Sequence[PurePosixPath] = (),
    backlink_targets: Sequence[PurePosixPath] = (),
    link_mode: str = "rendered",
    opaque_form: int = 0,
    body_mismatch: bool = False,
    wrong_section: bool = False,
) -> str:
    """Build authored fixture Markdown consumed by the canonical adapter."""

    def syntax(target: PurePosixPath, label: str) -> str:
        relative = posixpath.relpath(target.as_posix(), document.path.parent.as_posix())
        if link_mode == "plain":
            return relative
        if link_mode == "opaque":
            return _opaque_fixture_link(document.path, target, label, opaque_form)
        return _fixture_link(document.path, target, label)

    sections: list[str] = []
    relationship_heading = profile.role_decision.relationship_section
    for heading in profile.headings.required:
        if wrong_section and heading == relationship_heading:
            continue
        parts = [
            f"## {heading}",
            f"Fixture {document.status or 'draft'} content for {heading}.",
        ]
        if heading == profile.headings.required[0]:
            parts.extend(
                syntax(target, f"Backlink {index + 1}")
                for index, target in enumerate(backlink_targets)
            )
        if profile.profile_id == "sdlc/task" and heading == "Task Table":
            parts.append(
                "| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |\n"
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                "| FIX-001 | VAL-FIX-001 | Verify lifecycle evidence | platform | Done | Verified current authored row | [Review log](../../../README.md) |"
            )
        if heading == relationship_heading:
            if profile.body_contract is None:
                parts.extend(
                    syntax(target, f"Evidence {index + 1}")
                    for index, target in enumerate(relationship_targets)
                )
            elif body_mismatch:
                parts.append("### Lifecycle Traceability\n\nMalformed evidence table.")
            else:
                contract = profile.body_contract
                parts.append(f"### {contract.table_heading}")
                table_lines = [
                    "| " + " | ".join(contract.required_columns) + " |",
                    "| " + " | ".join("---" for _ in contract.required_columns) + " |",
                ]
                rows: list[list[str]] = []
                targets = list(relationship_targets) or [None]
                for row_number, target in enumerate(targets, start=1):
                    row = ["fixture" for _ in contract.required_columns]
                    for identifier in contract.identifier_columns:
                        index = contract.required_columns.index(identifier.column)
                        prefix = {
                            "requirement": "REQ-FIX-",
                            "criterion": "VAL-FIX-",
                            "work-item": "FIX-",
                        }[identifier.kind]
                        row[index] = f"{prefix}{row_number:03d}"
                    selected_column: str | None = None
                    if target is not None:
                        target_profile = snapshot_profiles.get(target)
                        if (
                            contract.source_link_column is not None
                            and target_profile in contract.allowed_source_profile_ids
                        ):
                            selected_column = contract.source_link_column
                        elif (
                            contract.target_link_column is not None
                            and target_profile in contract.allowed_target_profile_ids
                        ):
                            selected_column = contract.target_link_column
                        elif target_profile is None:
                            selected_column = (
                                contract.source_link_column
                                or contract.target_link_column
                            )
                    for column in (
                        contract.source_link_column,
                        contract.target_link_column,
                    ):
                        if column is None:
                            continue
                        index = contract.required_columns.index(column)
                        if column == selected_column and target is not None:
                            label = row[index]
                            row[index] = syntax(target, label)
                        else:
                            row[index] = "N/A — isolated evidence fixture"
                    if table_targets:
                        evidence_column = next(
                            (
                                column
                                for column in contract.required_columns
                                if column.casefold() == "evidence"
                            ),
                            None,
                        )
                        if evidence_column is not None:
                            row[contract.required_columns.index(evidence_column)] = (
                                " ".join(
                                    syntax(target, f"Review {index + 1}")
                                    for index, target in enumerate(table_targets)
                                )
                            )
                    rows.append(row)
                table_lines.extend("| " + " | ".join(row) + " |" for row in rows)
                parts.append("\n".join(table_lines))
        sections.append("\n\n".join(parts))
    if wrong_section:
        links = "\n".join(
            syntax(target, f"Wrong section {index + 1}")
            for index, target in enumerate(relationship_targets)
        )
        sections.append(f"## Other Relationship\n\n{links or 'No evidence.'}")
    status = document.status or "draft"
    return (
        "---\n"
        "title: 'Lifecycle evidence fixture'\n"
        f"type: {document.profile_id}\n"
        f"status: {status}\n"
        "owner: platform\n"
        "updated: 2099-01-01\n"
        "---\n\n"
        "# Lifecycle evidence fixture\n\n" + "\n\n".join(sections) + "\n"
    )


def _evidence_target_path(
    profile_id: str, predicate_id: str, case_index: int
) -> PurePosixPath:
    if predicate_id == "complete-product-program":
        return PurePosixPath("docs/01.requirements/006-evidence-fixture.md")
    if profile_id == "sdlc/plan":
        return PurePosixPath(
            f"docs/04.execution/plans/2099-01-01-edge-{case_index:02d}.md"
        )
    if profile_id == "sdlc/task":
        return PurePosixPath(
            f"docs/04.execution/tasks/2099-01-01-edge-{case_index:02d}.md"
        )
    return PurePosixPath(f"docs/__lifecycle_evidence__/{case_index:02d}-target.md")


def _evidence_case_context(
    registry: Registry,
    case: Mapping[str, object],
    variant: str,
    case_index: int,
) -> tuple[LifecycleDocument, LifecycleEvidenceContext]:
    profile_id = str(case["profile"])
    from_state = str(case["from"])
    to_state = str(case["to"])
    predicate_id = str(case["predicate"])
    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    target_path = _evidence_target_path(profile_id, predicate_id, case_index)
    target = LifecycleDocument(target_path, profile_id, to_state)
    documents: dict[PurePosixPath, LifecycleDocument] = {target_path: target}
    relationships: dict[PurePosixPath, list[PurePosixPath]] = {target_path: []}
    table_targets: dict[PurePosixPath, list[PurePosixPath]] = {target_path: []}

    def add(path: PurePosixPath, added_profile: str, status: str) -> PurePosixPath:
        documents[path] = LifecycleDocument(path, added_profile, status)
        relationships.setdefault(path, [])
        table_targets.setdefault(path, [])
        return path

    def previous(status: str | None) -> str | None:
        return {"active": "draft", "accepted": "active", "done": "active"}.get(
            status, status
        )

    primary_evidence: list[PurePosixPath] = []
    pair_paths: tuple[PurePosixPath, PurePosixPath] | None = None
    spec_identity: PurePosixPath | None = None

    if predicate_id == "accept-architecture":
        adr = add(
            PurePosixPath(
                f"docs/02.architecture/decisions/{case_index:04d}-fixture.md"
            ),
            "sdlc/adr",
            "accepted",
        )
        relationships[target_path].append(adr)
        relationships[adr].append(target_path)
        primary_evidence.append(adr)
    elif predicate_id == "complete-product-program":
        program = next(
            program for program in registry.program_lineage if program.prd_id == "006"
        )
        relation_paths: list[PurePosixPath] = []
        for relation in (*program.tranches, *program.follow_ups):
            relation_path = add(
                PurePosixPath(
                    f"docs/03.specs/{relation.spec_id}-evidence-fixture/spec.md"
                ),
                "sdlc/spec",
                "done",
            )
            relation_paths.append(relation_path)
        relationships[target_path].extend(relation_paths)
        primary_evidence.extend(relation_paths)
    elif predicate_id in {
        "activate-execution-pair",
        "complete-specification",
        "complete-execution-pair",
        "accept-operated-document",
        "terminate-reviewed-reference",
    }:
        ready_spec_id, ready_spec_state, _ = _dependency_ready_tranche_window(registry)
        spec_identity = (
            target_path
            if profile_id
            in {
                "sdlc/spec",
                "sdlc/api-spec",
                "sdlc/agent-design",
                "sdlc/data-model",
                "sdlc/tests",
            }
            else add(
                _execution_spec_fixture_path(ready_spec_id)
                if predicate_id == "activate-execution-pair"
                else PurePosixPath(
                    f"docs/03.specs/{900 + case_index:03d}-evidence/spec.md"
                ),
                "sdlc/spec",
                ready_spec_state
                if predicate_id == "activate-execution-pair"
                else "active",
            )
        )
        plan = (
            target_path
            if profile_id == "sdlc/plan"
            else add(
                PurePosixPath(
                    f"docs/04.execution/plans/2099-01-01-pair-{case_index:02d}.md"
                ),
                "sdlc/plan",
                "active" if predicate_id == "activate-execution-pair" else "done",
            )
        )
        task = (
            target_path
            if profile_id == "sdlc/task"
            else add(
                PurePosixPath(
                    f"docs/04.execution/tasks/2099-01-01-pair-{case_index:02d}.md"
                ),
                "sdlc/task",
                "active" if predicate_id == "activate-execution-pair" else "done",
            )
        )
        relationships[plan].extend((spec_identity, task))
        relationships[task].extend((spec_identity, plan))
        pair_paths = (plan, task)
        primary_evidence.extend(pair_paths)
        if predicate_id in {"accept-operated-document", "terminate-reviewed-reference"}:
            relationships[target_path].append(task)
            table_targets[task].append(target_path)
    else:
        if predicate_id in {"activate-heading-profile", "accept-decision-self"}:
            support_profile = "sdlc/ard" if profile_id == "sdlc/adr" else "sdlc/spec"
            support = add(
                PurePosixPath(
                    f"docs/__lifecycle_evidence__/{case_index:02d}-support.md"
                ),
                support_profile,
                "active",
            )
            relationships[target_path].append(support)
        primary_evidence.append(target_path)

    predicate_contract = next(
        predicate
        for predicate in registry.evidence_predicates
        if predicate.predicate_id == predicate_id
    )
    if "rendered-link" in predicate_contract.capabilities and not relationships.get(
        target_path
    ):
        target_profile = profile_map[profile_id]
        allowed = ()
        if target_profile.body_contract is not None:
            allowed = (
                target_profile.body_contract.allowed_source_profile_ids
                or target_profile.body_contract.allowed_target_profile_ids
            )
        support_profile = allowed[0] if allowed else "sdlc/spec"
        support = add(
            PurePosixPath(
                f"docs/__lifecycle_evidence__/{case_index:02d}-rendered-support.md"
            ),
            support_profile,
            "active",
        )
        relationships[target_path].append(support)

    def remove(path: PurePosixPath) -> None:
        documents.pop(path, None)
        relationships.pop(path, None)
        table_targets.pop(path, None)

    self_requirement = any(
        "$self" in requirement.profile_ids
        for requirement in predicate_contract.evidence
    )

    def mutation_evidence_path() -> PurePosixPath:
        if self_requirement:
            return target_path
        if pair_paths is not None:
            return next(
                (path for path in pair_paths if path != target_path),
                pair_paths[0],
            )
        return primary_evidence[0] if primary_evidence else target_path

    if variant == "missing":
        if pair_paths is not None:
            plan, task = pair_paths
            if target_path in {plan, task} or profile_id in SPECIFICATION_PROFILES:
                relationships[plan] = [
                    path for path in relationships[plan] if path != task
                ]
                relationships[task] = [
                    path for path in relationships[task] if path != plan
                ]
            else:
                relationships[target_path] = [
                    path for path in relationships[target_path] if path != task
                ]
                table_targets[task] = [
                    path for path in table_targets[task] if path != target_path
                ]
        elif predicate_id == "complete-product-program" and primary_evidence:
            removed = primary_evidence[-1]
            relationships[target_path] = [
                path for path in relationships[target_path] if path != removed
            ]
        elif predicate_id == "accept-architecture" and primary_evidence:
            removed = primary_evidence[0]
            relationships[target_path] = [
                path for path in relationships[target_path] if path != removed
            ]
        else:
            relationships[target_path] = []
    elif variant == "orphan":
        removed: PurePosixPath | None = None
        if pair_paths is not None:
            plan, task = pair_paths
            removable = plan if target_path == task else task
            remove(removable)
            removed = removable
        elif predicate_id == "complete-product-program" and primary_evidence:
            removed = primary_evidence[-1]
            remove(removed)
        elif predicate_id == "accept-architecture" and primary_evidence:
            removed = primary_evidence[0]
            remove(removed)
        else:
            missing_path = PurePosixPath(
                f"docs/__lifecycle_evidence__/{case_index:02d}-orphan.md"
            )
            relationships[target_path] = [missing_path]
    elif variant == "wrong-profile":
        path = mutation_evidence_path()
        current = documents.get(path)
        if current is not None:
            wrong_profile = (
                "sdlc/prd" if current.profile_id == "sdlc/guide" else "sdlc/guide"
            )
            documents[path] = LifecycleDocument(path, wrong_profile, current.status)
    elif variant == "wrong-state":
        path = mutation_evidence_path()
        current = documents.get(path)
        if current is not None:
            documents[path] = LifecycleDocument(path, current.profile_id, "draft")
    elif variant == "multiple":
        if pair_paths is not None and spec_identity is not None:
            plan, task = pair_paths
            if target_path == plan:
                task_two = add(
                    PurePosixPath(
                        f"docs/04.execution/tasks/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/task",
                    documents[task].status or "done",
                )
                relationships[plan].append(task_two)
                relationships[task_two].extend((spec_identity, plan))
                if predicate_id in {
                    "accept-operated-document",
                    "terminate-reviewed-reference",
                }:
                    table_targets[task_two].append(target_path)
            elif target_path == task:
                plan_two = add(
                    PurePosixPath(
                        f"docs/04.execution/plans/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/plan",
                    documents[plan].status or "done",
                )
                relationships[task].append(plan_two)
                relationships[plan_two].extend((spec_identity, task))
            else:
                plan_two = add(
                    PurePosixPath(
                        f"docs/04.execution/plans/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/plan",
                    documents[plan].status or "done",
                )
                task_two = add(
                    PurePosixPath(
                        f"docs/04.execution/tasks/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/task",
                    documents[task].status or "done",
                )
                relationships[plan_two].extend((spec_identity, task_two))
                relationships[task_two].extend((spec_identity, plan_two))
                if predicate_id in {
                    "accept-operated-document",
                    "terminate-reviewed-reference",
                }:
                    relationships[target_path].append(task_two)
                    table_targets[task_two].append(target_path)
        elif predicate_id == "complete-product-program" and primary_evidence:
            relation = primary_evidence[0]
            duplicate = add(
                relation.parent.with_name(relation.parent.name + "-duplicate")
                / "spec.md",
                "sdlc/spec",
                "done",
            )
            relationships[target_path].append(duplicate)
        elif relationships.get(target_path):
            relationships[target_path].append(relationships[target_path][0])
        else:
            target_profile = profile_map[profile_id]
            allowed = ()
            if target_profile.body_contract is not None:
                allowed = (
                    target_profile.body_contract.allowed_source_profile_ids
                    or target_profile.body_contract.allowed_target_profile_ids
                )
            support_profile = allowed[0] if allowed else "sdlc/spec"
            support = add(
                PurePosixPath(
                    f"docs/__lifecycle_evidence__/{case_index:02d}-duplicate.md"
                ),
                support_profile,
                "active",
            )
            relationships[target_path].extend((support, support))

    corrupt_path = target_path
    if variant in {"plain-text-path", "opaque-markdown"} and not relationships.get(
        corrupt_path
    ):
        target_profile = profile_map[profile_id]
        allowed = ()
        if target_profile.body_contract is not None:
            allowed = (
                target_profile.body_contract.allowed_source_profile_ids
                or target_profile.body_contract.allowed_target_profile_ids
            )
        support_profile = allowed[0] if allowed else "sdlc/spec"
        support = add(
            PurePosixPath(
                f"docs/__lifecycle_evidence__/{case_index:02d}-syntax-support.md"
            ),
            support_profile,
            "active",
        )
        relationships.setdefault(corrupt_path, []).append(support)

    backlink_targets: dict[PurePosixPath, list[PurePosixPath]] = {
        path: [] for path in documents
    }
    for owner, linked_paths in relationships.items():
        owner_document = documents.get(owner)
        if owner_document is None:
            continue
        owner_profile = profile_map[owner_document.profile_id]
        contract = owner_profile.body_contract
        if contract is None or not contract.reciprocal_evidence:
            continue
        for linked_path in linked_paths:
            if linked_path in documents:
                backlink_targets[linked_path].append(owner)

    snapshot_profiles = MappingProxyType(
        {path: document.profile_id for path, document in documents.items()}
    )
    adapter = _link_validator_module()
    views: dict[PurePosixPath, LifecycleEvidenceDocument] = {}
    for path, document in documents.items():
        profile = profile_map[document.profile_id]
        mode = (
            "plain"
            if variant == "plain-text-path" and path == corrupt_path
            else "opaque"
            if variant == "opaque-markdown" and path == corrupt_path
            else "rendered"
        )
        text = _evidence_fixture_text(
            profile,
            document,
            snapshot_profiles,
            relationships.get(path, ()),
            table_targets=table_targets.get(path, ()),
            backlink_targets=backlink_targets.get(path, ()),
            link_mode=mode,
            opaque_form=case_index,
            body_mismatch=(
                variant == "body-contract-mismatch"
                or (variant == "missing" and predicate_contract.relationship == "self")
            )
            and path == corrupt_path,
            wrong_section=(
                variant == "wrong-relationship-section"
                or (
                    variant == "body-contract-mismatch"
                    and profile.body_contract is None
                )
            )
            and path == corrupt_path,
        )
        rendered = adapter.lifecycle_markdown_evidence(
            path, text, profile, snapshot_profiles
        )
        views[path] = LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=rendered.unresolved_relationship_links,
            body_table_links=rendered.body_table_links,
            relationship_section_valid=rendered.relationship_section_valid,
            body_contract_valid=rendered.body_contract_valid,
            task_terminal_evidence_valid=rendered.task_terminal_evidence_valid,
        )

    base_documents = {
        path: LifecycleDocument(path, document.profile_id, previous(document.status))
        for path, document in documents.items()
    }
    base_documents[target_path] = LifecycleDocument(target_path, profile_id, from_state)
    if predicate_id == "complete-product-program" and primary_evidence:
        last_relation = primary_evidence[-1]
        if last_relation in base_documents:
            base_documents[last_relation] = LifecycleDocument(
                last_relation, "sdlc/spec", "active"
            )
    body_changed = set(documents)
    if variant == "unchanged":
        if predicate_contract.same_diff == "self-status-and-body":
            body_changed.discard(target_path)
        elif predicate_contract.same_diff == "pair-created-or-status-changed":
            assert pair_paths is not None
            unchanged_member = next(path for path in pair_paths if path != target_path)
            base_documents[unchanged_member] = documents[unchanged_member]
        elif predicate_contract.same_diff == "target-and-last-relation-changed":
            for relation in primary_evidence:
                base_documents[relation] = documents[relation]
        elif predicate_contract.same_diff == "target-and-evidence-status-body-changed":
            evidence_path = primary_evidence[0]
            base_documents[evidence_path] = documents[evidence_path]
            body_changed.discard(evidence_path)
        elif predicate_contract.same_diff in {
            "target-plan-task-status-changed",
            "pair-status-changed",
        }:
            assert pair_paths is not None
            for pair_path in pair_paths:
                if pair_path != target_path:
                    base_documents[pair_path] = documents[pair_path]
    projected_documents = {path: view.document for path, view in views.items()}
    status_changed = frozenset(
        path
        for path in set(base_documents) & set(projected_documents)
        if base_documents[path].profile_id != projected_documents[path].profile_id
        or base_documents[path].status != projected_documents[path].status
    )
    body_changed_paths = frozenset(body_changed & set(projected_documents))
    changed_paths = status_changed | body_changed_paths
    return target, LifecycleEvidenceContext(
        base_documents=MappingProxyType(base_documents),
        proposed_documents=MappingProxyType(views),
        changed_paths=changed_paths,
        status_changed_paths=status_changed,
        body_changed_paths=body_changed_paths,
        created_paths=frozenset(),
    )


def _fixture_document_text(
    path: str,
    profile_id: str,
    status: str,
    *,
    claimed_profile_id: str | None = None,
    execution_spec_path: PurePosixPath | None = None,
) -> str:
    execution_spec = execution_spec_path or PurePosixPath(
        "docs/03.specs/900-lifecycle-fixture/spec.md"
    )
    heading_sets = {
        "sdlc/spec": (
            "Overview",
            "Strategic Boundaries & Non-goals",
            "Contracts",
            "Core Design",
            "Data Modeling & Storage Strategy",
            "Interfaces & Data Structures",
            "Edge Cases & Error Handling",
            "Failure Modes & Fallback / Human Escalation",
            "Verification Commands",
            "Success Criteria & Verification Plan",
            "Traceability",
        ),
        "sdlc/plan": (
            "Overview",
            "Context",
            "Goals & In-Scope",
            "Non-Goals & Out-of-Scope",
            "Work Breakdown",
            "Verification Plan",
            "Risks & Mitigations",
            "Completion Criteria",
            "Traceability",
        ),
        "sdlc/task": (
            "Overview",
            "Inputs",
            "Task Table",
            "Approval and Safety Boundaries",
            "Verification Summary",
            "Traceability",
        ),
    }
    body_parts: list[str] = []
    for heading in heading_sets.get(profile_id, ()):
        body_parts.append(f"## {heading}\n\nLifecycle fixture {status} evidence.")
        if (
            profile_id == "sdlc/spec"
            and PurePosixPath(path) == execution_spec
            and heading == "Overview"
        ):
            owner = PurePosixPath(path)
            body_parts.append(
                " ".join(
                    (
                        _fixture_link(
                            owner,
                            PurePosixPath(
                                "docs/04.execution/plans/2099-01-01-example.md"
                            ),
                            "Plan backlink",
                        ),
                        _fixture_link(
                            owner,
                            PurePosixPath(
                                "docs/04.execution/tasks/2099-01-01-example.md"
                            ),
                            "Task backlink",
                        ),
                    )
                )
            )
        if profile_id == "sdlc/task" and heading == "Task Table":
            body_parts.append(
                "| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |\n"
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                "| FIX-001 | VAL-FIX-001 | Exercise evidence | platform | Done | Verified fixture | [Log](../../../README.md) |"
            )
        if heading != "Traceability":
            continue
        body_parts.append("### Lifecycle Traceability")
        if profile_id == "sdlc/spec":
            body_parts.append(
                "| PRD requirement | Spec criterion | Verification method |\n"
                "| --- | --- | --- |\n"
                "| N/A — isolated lifecycle fixture | VAL-FIX-001 | Self-test |"
            )
        elif profile_id == "sdlc/plan":
            body_parts.append(
                "| Spec criterion | Work package | Expected Task |\n"
                "| --- | --- | --- |\n"
                f"| {_fixture_link(PurePosixPath(path), execution_spec, 'VAL-FIX-001')} | FIX-001 | [Task](../tasks/2099-01-01-example.md) |"
            )
        elif profile_id == "sdlc/task":
            spec_link = _fixture_link(
                PurePosixPath(path), execution_spec, "Spec evidence"
            )
            body_parts.append(
                "| Criterion / work item | Result | Evidence |\n"
                "| --- | --- | --- |\n"
                f"| {_fixture_link(PurePosixPath(path), execution_spec, 'FIX-001')} | Verified | {spec_link} |\n"
                f"| [FIX-002](../plans/2099-01-01-example.md) | Verified | {spec_link} |"
            )
    body = "\n\n".join(body_parts)
    return (
        "---\n"
        "title: 'Lifecycle fixture'\n"
        f"type: {claimed_profile_id or profile_id}\n"
        f"status: {status}\n"
        "owner: platform\n"
        "updated: 2099-01-01\n"
        "---\n\n"
        "# Lifecycle fixture\n"
        f"\n{body}\n"
    )


def _write_fixture_document(
    root: Path,
    path: str,
    profile_id: str,
    status: str,
    *,
    claimed_profile_id: str | None = None,
    execution_spec_path: PurePosixPath | None = None,
) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _fixture_document_text(
            path,
            profile_id,
            status,
            claimed_profile_id=claimed_profile_id,
            execution_spec_path=execution_spec_path,
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


def _write_invalid_evidence_document(
    root: Path, path: str, profile_id: str, status: str
) -> None:
    destination = root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "---\n"
        "title: 'Invalid evidence fixture'\n"
        f"type: {profile_id}\n"
        f"status: {status}\n"
        "owner: platform\n"
        "updated: 2099-01-01\n"
        "---\n\n# Invalid evidence fixture\n",
        encoding="utf-8",
    )


def _write_architecture_evidence_pair(
    root: Path,
    registry: Registry,
    *,
    ard_status: str,
    adr_status: str,
    linked: bool,
) -> tuple[str, str]:
    ard_path = PurePosixPath(
        "docs/02.architecture/requirements/0900-evidence-fixture.md"
    )
    adr_path = PurePosixPath("docs/02.architecture/decisions/0900-evidence-fixture.md")
    documents = {
        ard_path: LifecycleDocument(ard_path, "sdlc/ard", ard_status),
        adr_path: LifecycleDocument(adr_path, "sdlc/adr", adr_status),
    }
    snapshot_profiles = MappingProxyType(
        {path: document.profile_id for path, document in documents.items()}
    )
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    for path, document in documents.items():
        relations = (
            (adr_path,)
            if linked and path == ard_path
            else (ard_path,)
            if linked and path == adr_path
            else ()
        )
        text = _evidence_fixture_text(
            profiles[document.profile_id],
            document,
            snapshot_profiles,
            relations,
        )
        destination = root / path.as_posix()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    return ard_path.as_posix(), adr_path.as_posix()


def _git_case(
    name: str,
    root: Path,
    registry: Registry,
    contract_root: Path,
) -> tuple[int, list[str]]:
    fixture_registry = root / REGISTRY_PATH
    fixture_registry.parent.mkdir(parents=True, exist_ok=True)
    fixture_registry.write_bytes((contract_root / REGISTRY_PATH).read_bytes())
    spec_path = "docs/03.specs/900-example/spec.md"
    ready_spec_id, ready_spec_state, blocked_spec_id = _dependency_ready_tranche_window(
        registry
    )
    ready_spec_path = _execution_spec_fixture_path(ready_spec_id)
    blocked_spec_path = (
        _execution_spec_fixture_path(blocked_spec_id)
        if blocked_spec_id is not None
        else None
    )
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
        "staged-evidence-index-invalid-worktree-valid",
        "staged-evidence-index-valid-worktree-invalid",
    }:
        _write_fixture_document(root, spec_path, "sdlc/spec", "draft")
    if name in {
        "staged-paired-create",
        "staged-paired-create-ready-spec-done",
        "staged-paired-create-split-spec",
    }:
        _write_fixture_document(
            root,
            ready_spec_path.as_posix(),
            "sdlc/spec",
            "done"
            if name == "staged-paired-create-ready-spec-done"
            else ready_spec_state,
            execution_spec_path=ready_spec_path,
        )
    if name == "staged-paired-create-blocked-spec":
        if blocked_spec_path is None:
            raise ValueError("blocked-pair fixture requires one successor tranche")
        _write_fixture_document(
            root,
            blocked_spec_path.as_posix(),
            "sdlc/spec",
            "active",
            execution_spec_path=blocked_spec_path,
        )
    if name == "staged-paired-create-split-spec":
        if blocked_spec_path is None:
            raise ValueError("split-pair fixture requires one successor tranche")
        _write_fixture_document(
            root,
            blocked_spec_path.as_posix(),
            "sdlc/spec",
            "active",
            execution_spec_path=blocked_spec_path,
        )
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
    elif name in {
        "staged-paired-create",
        "staged-paired-create-ready-spec-done",
    }:
        _write_fixture_document(
            root,
            "docs/04.execution/plans/2099-01-01-example.md",
            "sdlc/plan",
            "active",
            execution_spec_path=ready_spec_path,
        )
        _write_fixture_document(
            root,
            "docs/04.execution/tasks/2099-01-01-example.md",
            "sdlc/task",
            "active",
            execution_spec_path=ready_spec_path,
        )
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-paired-create-blocked-spec":
        plan_path = "docs/04.execution/plans/2099-01-01-example.md"
        task_path = "docs/04.execution/tasks/2099-01-01-example.md"
        assert blocked_spec_path is not None
        _write_fixture_document(
            root,
            plan_path,
            "sdlc/plan",
            "active",
            execution_spec_path=blocked_spec_path,
        )
        _write_fixture_document(
            root,
            task_path,
            "sdlc/task",
            "active",
            execution_spec_path=blocked_spec_path,
        )
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-paired-create-split-spec":
        plan_path = "docs/04.execution/plans/2099-01-01-example.md"
        task_path = "docs/04.execution/tasks/2099-01-01-example.md"
        assert blocked_spec_path is not None
        _write_fixture_document(
            root,
            plan_path,
            "sdlc/plan",
            "active",
            execution_spec_path=ready_spec_path,
        )
        _write_fixture_document(
            root,
            task_path,
            "sdlc/task",
            "active",
            execution_spec_path=blocked_spec_path,
        )
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-evidence-index-invalid-worktree-valid":
        _write_invalid_evidence_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-evidence-index-valid-worktree-invalid":
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", spec_path)
        _write_invalid_evidence_document(root, spec_path, "sdlc/spec", "active")
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
    elif name in {
        "explicit-ref-proposed-only-evidence",
        "explicit-ref-base-only-evidence-removed",
    }:
        proposed_only = name == "explicit-ref-proposed-only-evidence"
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="active",
            adr_status="active",
            linked=not proposed_only,
        )
        base = _commit_fixture(root, "architecture evidence base")
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="accepted",
            adr_status="accepted",
            linked=proposed_only,
        )
        proposed = _commit_fixture(root, "architecture evidence proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="explicit-ref",
            from_ref=base,
            to_ref=proposed,
        )
    elif name == "ci-proposed-tree-evidence":
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="active",
            adr_status="active",
            linked=False,
        )
        configured_base = _commit_fixture(root, "CI evidence base")
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="accepted",
            adr_status="accepted",
            linked=True,
        )
        proposed = _commit_fixture(root, "CI evidence proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="ci",
            base_ref=configured_base,
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
        resolver_calls = 0

        def unexpected_evidence_resolver(*args: object) -> LifecycleEvidenceContext:
            nonlocal resolver_calls
            resolver_calls += 1
            raise AssertionError("evidence resolver ran before unique base selection")

        try:
            _evaluate_comparison(
                root,
                registry,
                mode="ci",
                base_ref=merge_left,
                to_ref=merge_right,
                evidence_context_factory=unexpected_evidence_resolver,
            )
        except InvocationError:
            return (
                (2, ["LIFECYCLE-BASE"])
                if resolver_calls == 0
                else (1, ["LIFECYCLE-EVIDENCE"])
            )
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
        "evidenceCases",
        "archiveCutoverCases",
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
        (
            "archiveCutoverCases",
            EXPECTED_ARCHIVE_CUTOVER_CASE_NAMES,
            {"name", "mode", "mutation", "expectedAdmittedCount"},
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
            elif group_name == "archiveCutoverCases":
                if case.get("mode") not in {
                    "staged",
                    "ci",
                    "snapshot",
                    "explicit-ref",
                }:
                    failures.append(f"archiveCutoverCases mode differs: {case_name}")
                if case.get("mutation") not in EXPECTED_ARCHIVE_CUTOVER_MUTATIONS:
                    failures.append(
                        f"archiveCutoverCases mutation differs: {case_name}"
                    )
                if case.get("expectedAdmittedCount") not in {0, 33}:
                    failures.append(f"archiveCutoverCases count differs: {case_name}")

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

    evidence_cases = fixture.get("evidenceCases")
    if not isinstance(evidence_cases, list):
        failures.append("evidenceCases must be a list")
    else:
        for case in evidence_cases:
            if not isinstance(case, dict):
                failures.append("evidenceCases contains a non-object case")
                continue
            if set(case) != {
                "name",
                "profile",
                "from",
                "to",
                "predicate",
                "variants",
            }:
                failures.append(f"evidenceCases keys differ: {case.get('name')}")
                continue
            profile_id = case.get("profile")
            from_state = case.get("from")
            to_state = case.get("to")
            predicate = case.get("predicate")
            name = case.get("name")
            if not all(
                isinstance(value, str)
                for value in (name, profile_id, from_state, to_state, predicate)
            ):
                failures.append("evidenceCases scalar values must be strings")
            elif name != f"{profile_id}:{from_state}->{to_state}":
                failures.append(f"evidenceCases name differs: {name}")
            variants = case.get("variants")
            if (
                not _is_string_list(variants, nonempty=True)
                or tuple(variants) != EXPECTED_EVIDENCE_VARIANTS
            ):
                failures.append(f"evidenceCases variants differ: {name}")

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
    evidence_projection = [
        (case["profile"], case["from"], case["to"], case["predicate"])
        for case in fixture["evidenceCases"]
    ]
    production_evidence_projection = [
        (
            profile.profile_id,
            edge.from_state,
            edge.to_state,
            edge.predicate_id,
        )
        for profile in registry.profiles
        for edge in profile.lifecycle.edges
    ]
    if len(evidence_projection) != len(set(evidence_projection)):
        failures.append("fixture evidence edge projection contains duplicates")
    if evidence_projection != production_evidence_projection:
        failures.append("fixture evidence edge projection differs from production")
    if len(evidence_projection) != 42 or len(registry.evidence_predicates) != 11:
        failures.append("production evidence inventory is not 42 edges/11 predicates")
    if len({item[0] for item in evidence_projection}) != 19:
        failures.append("production evidence profile inventory is not 19")
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

    missing_archive_cutover = copy.deepcopy(fixture)
    missing_archive_cutover["archiveCutoverCases"] = [
        case
        for case in missing_archive_cutover["archiveCutoverCases"]
        if case["name"] != "partial-record-set"
    ]
    probes.append(("missing archive cutover denial", missing_archive_cutover))

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

    missing_evidence_edge = copy.deepcopy(fixture)
    missing_evidence_edge["evidenceCases"].pop()
    probes.append(("missing evidence edge", missing_evidence_edge))

    duplicate_evidence_edge = copy.deepcopy(fixture)
    duplicate_evidence_edge["evidenceCases"].append(
        copy.deepcopy(duplicate_evidence_edge["evidenceCases"][0])
    )
    probes.append(("duplicate evidence edge", duplicate_evidence_edge))

    unknown_evidence_predicate = copy.deepcopy(fixture)
    unknown_evidence_predicate["evidenceCases"][0]["predicate"] = "unknown"
    probes.append(("unknown evidence predicate", unknown_evidence_predicate))

    swapped_evidence_edges = copy.deepcopy(fixture)
    (
        swapped_evidence_edges["evidenceCases"][0],
        swapped_evidence_edges["evidenceCases"][1],
    ) = (
        swapped_evidence_edges["evidenceCases"][1],
        swapped_evidence_edges["evidenceCases"][0],
    )
    probes.append(("swapped evidence edges", swapped_evidence_edges))

    missing_evidence_variant = copy.deepcopy(fixture)
    missing_evidence_variant["evidenceCases"][0]["variants"].pop()
    probes.append(("missing evidence variant", missing_evidence_variant))

    extra_evidence_variant = copy.deepcopy(fixture)
    extra_evidence_variant["evidenceCases"][0]["variants"].append("extra")
    probes.append(("extra evidence variant", extra_evidence_variant))

    reordered_evidence_variants = copy.deepcopy(fixture)
    reordered_evidence_variants["evidenceCases"][0]["variants"].reverse()
    probes.append(("reordered evidence variants", reordered_evidence_variants))

    null_evidence_variants = copy.deepcopy(fixture)
    null_evidence_variants["evidenceCases"][0]["variants"] = None
    probes.append(("null evidence variants", null_evidence_variants))

    non_string_evidence_variant = copy.deepcopy(fixture)
    non_string_evidence_variant["evidenceCases"][0]["variants"][0] = []
    probes.append(("non-string evidence variant", non_string_evidence_variant))

    null_evidence_case = copy.deepcopy(fixture)
    null_evidence_case["evidenceCases"][0] = None
    probes.append(("null evidence case", null_evidence_case))

    failures: list[str] = []
    for name, candidate in probes:
        if not _fixture_contract_failures(candidate, registry):
            failures.append(f"fixture mutation accepted: {name}")
    return failures


EVIDENCE_REGRESSION_COUNT = 5


def _evidence_regression_failures(
    registry: Registry, evidence_cases: Sequence[Mapping[str, object]]
) -> list[str]:
    """Close the concrete bypasses reproduced by independent review."""

    failures: list[str] = []
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    adapter = _link_validator_module()

    def render_view(
        document: LifecycleDocument,
        text: str,
        snapshot_profiles: Mapping[PurePosixPath, str],
    ) -> LifecycleEvidenceDocument:
        rendered = adapter.lifecycle_markdown_evidence(
            document.path,
            text,
            profiles[document.profile_id],
            snapshot_profiles,
        )
        return LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=rendered.unresolved_relationship_links,
            body_table_links=rendered.body_table_links,
            relationship_section_valid=rendered.relationship_section_valid,
            body_contract_valid=rendered.body_contract_valid,
            task_terminal_evidence_valid=rendered.task_terminal_evidence_valid,
        )

    prd_path = PurePosixPath("docs/01.requirements/999-reciprocal-fixture.md")
    spec_path = PurePosixPath("docs/03.specs/999-reciprocal-fixture/spec.md")
    prd = LifecycleDocument(prd_path, "sdlc/prd", "active")
    spec = LifecycleDocument(spec_path, "sdlc/spec", "active")
    snapshot_profiles = MappingProxyType(
        {prd_path: prd.profile_id, spec_path: spec.profile_id}
    )
    prd_text = _evidence_fixture_text(
        profiles[prd.profile_id], prd, snapshot_profiles, (spec_path,)
    )
    spec_without_backlink = _evidence_fixture_text(
        profiles[spec.profile_id], spec, snapshot_profiles, ()
    )
    no_backlink_views = MappingProxyType(
        {
            prd_path: render_view(prd, prd_text, snapshot_profiles),
            spec_path: render_view(spec, spec_without_backlink, snapshot_profiles),
        }
    )
    base_documents = MappingProxyType(
        {
            prd_path: LifecycleDocument(prd_path, "sdlc/prd", "draft"),
            spec_path: spec,
        }
    )
    no_backlink_context = LifecycleEvidenceContext(
        base_documents=base_documents,
        proposed_documents=no_backlink_views,
        changed_paths=frozenset({prd_path}),
        status_changed_paths=frozenset({prd_path}),
        body_changed_paths=frozenset({prd_path}),
        created_paths=frozenset(),
    )
    no_backlink_actual = compare_lifecycle(
        registry,
        {prd_path: base_documents[prd_path]},
        {prd_path: prd},
        base_mode="explicit-ref",
        evidence_context=no_backlink_context,
    )
    no_backlink_expected = (
        LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=prd_path,
            profile="sdlc/prd",
            expected_transition="predicate activate-self-body for draft -> active",
            observed_transition=f"evidence paths {[prd_path.as_posix()]!r}",
            base_mode="explicit-ref",
            evidence_gap=(
                f"reciprocal body evidence is missing from {spec_path.as_posix()}"
            ),
        ),
    )
    if no_backlink_actual != no_backlink_expected:
        failures.append(f"regression reciprocal-body: {no_backlink_actual!r}")

    spec_with_backlink = _evidence_fixture_text(
        profiles[spec.profile_id],
        spec,
        snapshot_profiles,
        (),
        backlink_targets=(prd_path,),
    )
    forged_views = MappingProxyType(
        {
            prd_path: no_backlink_views[prd_path],
            spec_path: render_view(spec, spec_with_backlink, snapshot_profiles),
        }
    )
    forged_base = MappingProxyType(
        {
            prd_path: LifecycleDocument(prd_path, "sdlc/prd", "done"),
            spec_path: spec,
        }
    )
    forged_context = LifecycleEvidenceContext(
        base_documents=forged_base,
        proposed_documents=forged_views,
        changed_paths=frozenset({prd_path}),
        status_changed_paths=frozenset({prd_path}),
        body_changed_paths=frozenset({prd_path}),
        created_paths=frozenset({prd_path}),
    )
    forged_actual = compare_lifecycle(
        registry,
        {prd_path: LifecycleDocument(prd_path, "sdlc/prd", "draft")},
        {prd_path: prd},
        base_mode="explicit-ref",
        evidence_context=forged_context,
    )
    forged_expected = (
        LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=prd_path,
            profile="sdlc/prd",
            expected_transition="predicate activate-self-body for draft -> active",
            observed_transition=f"evidence paths {[prd_path.as_posix()]!r}",
            base_mode="explicit-ref",
            evidence_gap=(
                "created-path projection differs from canonical snapshots; "
                "base evidence projection differs from transition source"
            ),
        ),
    )
    if forged_actual != forged_expected:
        failures.append(f"regression forged-context: {forged_actual!r}")

    reference_path = PurePosixPath(
        "docs/90.references/research/2099-01-01-heading-fixture.md"
    )
    support_path = PurePosixPath("docs/03.specs/998-heading-fixture/spec.md")
    reference = LifecycleDocument(reference_path, "content/reference", "active")
    support = LifecycleDocument(support_path, "sdlc/spec", "active")
    heading_profiles = MappingProxyType(
        {reference_path: reference.profile_id, support_path: support.profile_id}
    )
    reference_text = _evidence_fixture_text(
        profiles[reference.profile_id],
        reference,
        heading_profiles,
        (support_path,),
    )
    reference_text += "\n## Unsupported Lifecycle Heading\n\nRejected.\n"
    heading_view = render_view(reference, reference_text, heading_profiles)
    if heading_view.body_contract_valid:
        failures.append("regression unsupported-root-h2: adapter accepted heading")
    heading_context = LifecycleEvidenceContext(
        base_documents=MappingProxyType(
            {
                reference_path: LifecycleDocument(
                    reference_path, "content/reference", "draft"
                ),
                support_path: support,
            }
        ),
        proposed_documents=MappingProxyType(
            {
                reference_path: heading_view,
                support_path: render_view(
                    support,
                    _evidence_fixture_text(
                        profiles[support.profile_id],
                        support,
                        heading_profiles,
                        (),
                    ),
                    heading_profiles,
                ),
            }
        ),
        changed_paths=frozenset({reference_path}),
        status_changed_paths=frozenset({reference_path}),
        body_changed_paths=frozenset({reference_path}),
        created_paths=frozenset(),
    )
    heading_actual = compare_lifecycle(
        registry,
        {reference_path: heading_context.base_documents[reference_path]},
        {reference_path: reference},
        base_mode="explicit-ref",
        evidence_context=heading_context,
    )
    if (
        len(heading_actual) != 1
        or heading_actual[0].evidence_gap
        != f"body contract mismatch at {reference_path.as_posix()}"
    ):
        failures.append(f"regression unsupported-root-h2: {heading_actual!r}")

    task_path = PurePosixPath("docs/04.execution/tasks/2099-01-01-terminal.md")
    task = LifecycleDocument(task_path, "sdlc/task", "done")
    terminal_profiles = MappingProxyType({task_path: task.profile_id})
    task_text = _evidence_fixture_text(
        profiles[task.profile_id], task, terminal_profiles, ()
    )
    real_terminal = render_view(task, task_text, terminal_profiles)
    placeholder_text = task_text.replace(
        "[Review log](../../../README.md)", "Named repository evidence"
    )
    placeholder_terminal = render_view(task, placeholder_text, terminal_profiles)
    if (
        not real_terminal.task_terminal_evidence_valid
        or placeholder_terminal.task_terminal_evidence_valid
    ):
        failures.append(
            "regression task-terminal-placeholder: canonical phrase/link differs"
        )

    operated_index, operated_case = next(
        (index, case)
        for index, case in enumerate(evidence_cases)
        if case["predicate"] == "accept-operated-document"
    )
    operated_target, operated_context = _evidence_case_context(
        registry, operated_case, "positive", operated_index
    )
    operated_views = dict(operated_context.proposed_documents)
    operated_task_path = next(
        path
        for path, view in operated_views.items()
        if view.document.profile_id == "sdlc/task"
    )
    operated_task = operated_views[operated_task_path].document
    operated_profiles = MappingProxyType(
        {path: view.document.profile_id for path, view in operated_views.items()}
    )
    operated_relationships = operated_views[operated_task_path].relationship_links
    task_with_evidence = _evidence_fixture_text(
        profiles[operated_task.profile_id],
        operated_task,
        operated_profiles,
        operated_relationships,
        table_targets=(operated_target.path,),
    )
    evidence_link = _fixture_link(operated_task_path, operated_target.path, "Review 1")
    result_link = _fixture_link(
        operated_task_path, operated_target.path, "Result target"
    )
    task_with_result_only = task_with_evidence.replace(evidence_link, "Verified")
    task_with_result_only = task_with_result_only.replace(
        "| fixture | Verified |", f"| {result_link} | Verified |"
    )
    result_only_view = render_view(
        operated_task, task_with_result_only, operated_profiles
    )
    if (
        operated_target.path in result_only_view.body_table_links
        or operated_target.path not in result_only_view.all_local_links
    ):
        failures.append("regression task-result-column: adapter projection differs")
    operated_views[operated_task_path] = result_only_view
    result_context = LifecycleEvidenceContext(
        base_documents=operated_context.base_documents,
        proposed_documents=MappingProxyType(operated_views),
        changed_paths=operated_context.changed_paths,
        status_changed_paths=operated_context.status_changed_paths,
        body_changed_paths=operated_context.body_changed_paths,
        created_paths=operated_context.created_paths,
    )
    result_actual = compare_lifecycle(
        registry,
        {
            operated_target.path: LifecycleDocument(
                operated_target.path,
                operated_target.profile_id,
                operated_case["from"],
            )
        },
        {operated_target.path: operated_target},
        base_mode="explicit-ref",
        evidence_context=result_context,
    )
    if _rule_ids(result_actual) != ["LIFECYCLE-EVIDENCE"]:
        failures.append(f"regression task-result-column: {result_actual!r}")

    return failures


def _ambiguous_base_edge_failures(
    registry: Registry, evidence_cases: Sequence[Mapping[str, object]]
) -> list[str]:
    """Run an edge-shaped public CI base gate for every production edge."""

    failures: list[str] = []
    invoked_edges: list[tuple[str, str, str]] = []
    expected_edges = [
        (str(case["profile"]), str(case["from"]), str(case["to"]))
        for case in evidence_cases
    ]
    for case_index, case in enumerate(evidence_cases):
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-ambiguous-evidence-"
        ) as directory:
            repo = Path(directory)
            _init_fixture_repo(repo)
            profile_id = str(case["profile"])
            from_state = str(case["from"])
            to_state = str(case["to"])
            edge = (profile_id, from_state, to_state)
            invoked_edges.append(edge)
            target_path = _evidence_target_path(
                profile_id, str(case["predicate"]), case_index
            )
            _write_fixture_document(
                repo, target_path.as_posix(), profile_id, from_state
            )
            common = _commit_fixture(repo, f"common {case['name']}")
            base_tree = _git_fixture(repo, "rev-parse", "HEAD^{tree}")
            left = _git_fixture(
                repo, "commit-tree", base_tree, "-p", common, "-m", "left"
            )
            right = _git_fixture(
                repo, "commit-tree", base_tree, "-p", common, "-m", "right"
            )
            _write_fixture_document(repo, target_path.as_posix(), profile_id, to_state)
            _git_fixture(repo, "add", "--", target_path.as_posix())
            proposed_tree = _git_fixture(repo, "write-tree")
            merge_left = _git_fixture(
                repo,
                "commit-tree",
                base_tree,
                "-p",
                left,
                "-p",
                right,
                "-m",
                "merge-left",
            )
            merge_right = _git_fixture(
                repo,
                "commit-tree",
                proposed_tree,
                "-p",
                right,
                "-p",
                left,
                "-m",
                "merge-right",
            )
            resolver_calls = 0

            def unexpected_evidence_resolver(
                *args: object,
            ) -> LifecycleEvidenceContext:
                nonlocal resolver_calls
                resolver_calls += 1
                raise AssertionError(
                    "evidence resolver ran before unique base selection"
                )

            try:
                _evaluate_comparison(
                    repo,
                    registry,
                    mode="ci",
                    base_ref=merge_left,
                    to_ref=merge_right,
                    include_paths=(target_path,),
                    evidence_context_factory=unexpected_evidence_resolver,
                )
            except InvocationError as exc:
                if str(exc) != "CI refs do not have exactly one commit merge base":
                    failures.append(
                        f"evidence {case['name']}/ambiguous-base: "
                        f"base error differs: {exc}"
                    )
            else:
                failures.append(
                    f"evidence {case['name']}/ambiguous-base: base gate passed"
                )
            if resolver_calls != 0:
                failures.append(
                    f"evidence {case['name']}/ambiguous-base: "
                    f"resolver calls {resolver_calls}"
                )
    if invoked_edges != expected_edges or len(set(invoked_edges)) != 42:
        failures.append(
            "ambiguous-base did not invoke the exact 42 unique profile/state edges"
        )
    return failures


def _evidence_assertion_run(
    registry: Registry,
    evidence_cases: Sequence[Mapping[str, object]],
) -> tuple[list[dict[str, object]], list[str], list[str]]:
    """Build the exact 504-case diagnostic projection for one lineage state."""

    projection: list[dict[str, object]] = []
    ambiguous_controls: list[str] = []
    failures: list[str] = []
    for case_index, case in enumerate(evidence_cases):
        for variant_value in case["variants"]:
            variant = str(variant_value)
            if variant == "ambiguous-base":
                ambiguous_controls.append(str(case["name"]))
                diagnostics = (
                    LifecycleDiagnostic(
                        severity="FAIL",
                        rule_id="LIFECYCLE-BASE",
                        path=PurePosixPath("."),
                        profile="",
                        expected_transition=(
                            "valid invocation, unique commit refs, and one "
                            "comparison base"
                        ),
                        observed_transition=(
                            "CI refs do not have exactly one commit merge base"
                        ),
                        base_mode="ci",
                        evidence_gap="argument or Git provenance",
                    ),
                )
                target_path = _evidence_target_path(
                    str(case["profile"]), str(case["predicate"]), case_index
                )
                expected_rules = ["LIFECYCLE-BASE"]
            else:
                target, evidence_context = _evidence_case_context(
                    registry, case, variant, case_index
                )
                target_path = target.path
                base_target = LifecycleDocument(
                    target.path, target.profile_id, str(case["from"])
                )
                diagnostics = compare_lifecycle(
                    registry,
                    {target.path: base_target},
                    {target.path: target},
                    base_mode="explicit-ref",
                    evidence_context=evidence_context,
                )
                expected_rules = [] if variant == "positive" else ["LIFECYCLE-EVIDENCE"]
            actual_rules = _rule_ids(diagnostics)
            if actual_rules != expected_rules:
                failures.append(
                    f"evidence {case['name']}/{variant}: "
                    f"expected {expected_rules}, actual {actual_rules}"
                )
            if variant not in {"positive", "ambiguous-base"} and len(diagnostics) != 1:
                failures.append(
                    f"evidence {case['name']}/{variant}: diagnostic count differs"
                )
            projection.append(
                {
                    "case": case["name"],
                    "profile": case["profile"],
                    "from": case["from"],
                    "to": case["to"],
                    "predicate": case["predicate"],
                    "variant": variant,
                    "target": target_path.as_posix(),
                    "diagnostics": [
                        {
                            "severity": diagnostic.severity,
                            "ruleId": diagnostic.rule_id,
                            "path": diagnostic.path.as_posix(),
                            "profile": diagnostic.profile,
                            "expectedTransition": diagnostic.expected_transition,
                            "observedTransition": diagnostic.observed_transition,
                            "baseMode": diagnostic.base_mode,
                            "evidenceGap": diagnostic.evidence_gap,
                        }
                        for diagnostic in diagnostics
                    ],
                }
            )
    return projection, ambiguous_controls, failures


def _evidence_assertion_sha256(projection: Sequence[Mapping[str, object]]) -> str:
    return hashlib.sha256(
        json.dumps(
            projection,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


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

    evidence_cases = fixture.get("evidenceCases", [])
    failures.extend(_ambiguous_base_edge_failures(registry, evidence_cases))
    (
        evidence_assertion_projection,
        ambiguous_edge_controls,
        evidence_assertion_failures,
    ) = _evidence_assertion_run(registry, evidence_cases)
    failures.extend(evidence_assertion_failures)
    if len(ambiguous_edge_controls) != 42 or len(set(ambiguous_edge_controls)) != 42:
        failures.append("ambiguous-base edge projection is not exactly 42 unique edges")
    evidence_assertion_sha256 = _evidence_assertion_sha256(
        evidence_assertion_projection
    )
    if (
        len(evidence_assertion_projection) != 504
        or evidence_assertion_sha256 != EXPECTED_EVIDENCE_ASSERTION_SHA256
    ):
        failures.append(
            "evidence exact assertion projection differs: "
            f"count={len(evidence_assertion_projection)} "
            f"sha256={evidence_assertion_sha256}"
        )

    current_ready_spec_id, current_ready_state, _ = _dependency_ready_tranche_window(
        registry
    )
    if current_ready_state != "active":
        failures.append("current dependency-ready original tranche is not active")
    # The main projection above and named staged-paired-create case below prove
    # the current boundary.  Fixed 035/036 proofs that are not current still
    # run; after production advances to 037 or later, both fixed proofs run.
    fixed_proof_ids = {"035", "036"} - {current_ready_spec_id}
    for ready_spec_id in sorted(fixed_proof_ids):
        rollover_registry = _registry_with_ready_spec(registry, ready_spec_id)
        actual_ready_spec_id, actual_ready_state, _ = _dependency_ready_tranche_window(
            rollover_registry
        )
        if (actual_ready_spec_id, actual_ready_state) != (ready_spec_id, "active"):
            failures.append(
                f"rollover {ready_spec_id}: dependency-ready projection differs"
            )
            continue
        (
            rollover_projection,
            rollover_controls,
            rollover_failures,
        ) = _evidence_assertion_run(rollover_registry, evidence_cases)
        if rollover_failures:
            failures.extend(
                f"rollover {ready_spec_id}: {failure}" for failure in rollover_failures
            )
        rollover_sha256 = _evidence_assertion_sha256(rollover_projection)
        if (
            len(rollover_projection) != 504
            or rollover_sha256 != EXPECTED_EVIDENCE_ASSERTION_SHA256
            or len(rollover_controls) != 42
            or len(set(rollover_controls)) != 42
        ):
            failures.append(
                f"rollover {ready_spec_id}: evidence exact assertion projection "
                f"differs: count={len(rollover_projection)} sha256={rollover_sha256}"
            )
        with tempfile.TemporaryDirectory(
            prefix=f"document-lifecycle-rollover-{ready_spec_id}-"
        ) as directory:
            repo = Path(directory)
            _init_fixture_repo(repo)
            try:
                pair_exit, pair_rules = _git_case(
                    "staged-paired-create", repo, rollover_registry, root
                )
            except (InvocationError, OSError, ValueError) as exc:
                failures.append(f"rollover {ready_spec_id}: paired create error {exc}")
            else:
                if pair_exit != 0 or pair_rules:
                    failures.append(
                        f"rollover {ready_spec_id}: paired create differs "
                        f"exit={pair_exit} rules={pair_rules}"
                    )
    failures.extend(_evidence_regression_failures(registry, evidence_cases))

    for case in fixture.get("archiveCutoverCases", []):
        admitted = finite_archive_cutover_paths(
            **_archive_cutover_fixture_inputs(case["mode"], case["mutation"])
        )
        if len(admitted) != case["expectedAdmittedCount"]:
            failures.append(
                f"archive cutover {case['name']}: expected admitted count "
                f"{case['expectedAdmittedCount']}, actual {len(admitted)}"
            )

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
        evidence_count = sum(len(item["variants"]) for item in fixture["evidenceCases"])
        total = (
            forward_count
            + evidence_count
            + len(fixture["comparisonCases"])
            + len(fixture["admissionCases"])
            + len(fixture["gitCases"])
            + len(fixture["argumentCases"])
            + len(fixture["includePathCases"])
            + len(fixture["archiveCutoverCases"])
            + 1
            + FIXTURE_MUTATION_COUNT
            + EVIDENCE_REGRESSION_COUNT
        )
        print(
            "PASS lifecycle self-test "
            f"({total} cases: {forward_count} forward edges, "
            f"{evidence_count} edge evidence scenarios, "
            f"{len(fixture['comparisonCases'])} comparisons, "
            f"{len(fixture['admissionCases'])} admissions, "
            f"{len(fixture['gitCases'])} Git bases, "
            f"{len(fixture['argumentCases'])} arguments, "
            f"{len(fixture['includePathCases'])} includes, 1 snapshot, "
            f"{len(fixture['archiveCutoverCases'])} archive cutovers, "
            f"{FIXTURE_MUTATION_COUNT} fixture mutations, "
            f"{EVIDENCE_REGRESSION_COUNT} evidence regressions)"
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
