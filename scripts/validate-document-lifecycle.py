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
    ROOT_FILES,
    TARGET_ROOTS,
    DocumentContractError,
    DocumentProfile,
    Registry,
    Route,
    classify_path,
    enumerate_target_markdown,
    load_registry,
    read_repository_text,
)
from document_lifecycle import (
    ArtifactIdentityLineage,
    LifecycleDiagnostic,
    LifecycleDocument,
    LifecycleEvidenceContext,
    LifecycleEvidenceDocument,
    LifecycleRename,
    MigrationLifecycleEvents,
    RETIRED_DOCUMENT_TYPES,
    compare_lifecycle,
    document_from_text,
    lifecycle_diagnostic_sort_key,
    validate_snapshot_documents,
)

from archive_dispositions import (
    ARCHIVE_INDEX as DISPOSITION_ARCHIVE_INDEX,
    ROUTE_DISPOSITION_PROFILES,
    canonical_repository_path,
    frontmatter_mapping,
    link_resolved_text,
    parse_catalog,
    retention_class_of,
    retention_source_path,
)
from archive_validation import (
    MIG0004_TERMINAL_SOURCE_COMMIT,
    MIGRATION_DOCUMENT_MAX_BYTES,
    _load_canonical_markdown_module,
    generic_migration_id,
    is_sealed_migration,
    parse_migration_control,
    parse_pinned_migration_control,
    validate_archive_immutability,
    validate_migration_records,
)
from archive_recovery import (
    ArchiveContractError,
    WP004C_SEALED_TARGET_COMMIT,
    current_named_durable_ref,
    require_commits_reachable_from_durable_refs,
    _git_capture_bounded,
)
from document_authority import (
    AuthorityError,
    REGISTRY_PATH as CURRENT_REGISTRY_PATH,
    assert_staged_authority_matches_worktree,
)


RETIRED_REGISTRY_PATH = PurePosixPath("docs/99.templates/registry.json")
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
WORK105_ADR0023_PATH = PurePosixPath(
    "docs/02.architecture/decisions/"
    "0023-work-unit-document-taxonomy-and-governance-authority.md"
)
WORK105_ADR0024_PATH = PurePosixPath(
    "docs/02.architecture/decisions/"
    "0024-terminal-artifact-identity-and-archive-layout.md"
)
WORK105_LEGACY_AD0011_PATH = PurePosixPath(
    "docs/02.architecture/requirements/"
    "0011-document-taxonomy-consolidation-architecture.md"
)
WORK105_ADR0023_BASE_SHA256 = "fadbd95c581a0874797666e200f283d0f5fdc6c103643cc653e387062adbe53a"  # pragma: allowlist secret
WORK105_ADR0023_PROPOSED_SHA256 = "717714ce153cbd75ca5a77beb42a24cd1b146f25b1112d492e30d9fd214348d5"  # pragma: allowlist secret
WORK105_ADR0023_RECIPROCAL_ROW = (
    "| [ADR-0024](./0024-terminal-artifact-identity-and-archive-layout.md) | "
    "Partially supersedes only terminal Stage 98 date/mirror-path immutability; "
    "preserves transition safety, Stage 05 stability, Release exclusion, and "
    "every unrelated decision | "
    "[Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md) |"
)

WORK054_WP002_LEDGER_KEYS = (
    "legacy_path",
    "stable_path",
    "artifact_id",
    "action",
    "replacement",
    "source_commit",
    "source_blob",
    "content_sha256",
    "reason",
)

WORK054_WP003_BASE_COMMIT = "128beada377f18bc9f942c8ebb3e27e1f2fdcfae"
WORK054_WP003_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/0003-agent-governance-control-plane-consolidation.md"
)
WORK054_WP003_MIGRATION_SHA256 = "7baa2a9b2682313d9e8cfc4d3504db14b4985f780f85ff673a4bf535ce4c755e"  # pragma: allowlist secret
WORK054_WP003_LEDGER_KEYS = WORK054_WP002_LEDGER_KEYS
WORK054_WP003_OWNER_RETIREMENTS = (
    {
        "legacy_path": "docs/00.agent-governance/common-governance.md",
        "stable_path": None,
        "artifact_id": None,
        "action": "merged",
        "replacement": "docs/00.agent-governance/harness-catalog.md",
        "source_commit": WORK054_WP003_BASE_COMMIT,
        "source_blob": "de7e7edfe177ff349cd3824aebd82418adff95d7",  # pragma: allowlist secret
        "content_sha256": "c5da620d5f6c1aa26f2e0d99769872b90c6d2ec2fdb3c03813be27992f43e4ba",  # pragma: allowlist secret
    },
    {
        "legacy_path": "docs/00.agent-governance/harness-implementation-map.md",
        "stable_path": None,
        "artifact_id": None,
        "action": "merged",
        "replacement": "docs/00.agent-governance/harness-catalog.md",
        "source_commit": WORK054_WP003_BASE_COMMIT,
        "source_blob": "7e7a6d64a05be91658cc6657cd640491153a615a",  # pragma: allowlist secret
        "content_sha256": "3ea2f89c3ba17fbf0bac64533cbb5a378a85c062a020881a3844cfa190c9c218",  # pragma: allowlist secret
    },
    {
        "legacy_path": "docs/00.agent-governance/providers/agents-md.md",
        "stable_path": None,
        "artifact_id": None,
        "action": "merged",
        "replacement": "docs/00.agent-governance/providers/codex.md",
        "source_commit": WORK054_WP003_BASE_COMMIT,
        "source_blob": "06d9a7a5453ac8b6e28268850467e3e96de06dc9",  # pragma: allowlist secret
        "content_sha256": "5ea07c187ea54061f5ecc770a58a99edf40dfd73372ba8fc9e1d4ab14bf85bae",  # pragma: allowlist secret
    },
)

WORK054_WP004B_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/0004-document-authority-convergence.md"
)
WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE = "sdlc/requirement"
WORK054_WP004B_ROUTER_PATTERN = re.compile(
    r"^docs/03\.specs/[0-9]{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/README\.md$"
)
WORK054_WP004B_TASK_PATTERN = re.compile(
    r"^docs/03\.specs/[0-9]{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/"
    r"tasks/tsk-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
WORK054_WP004B_SPEC_PATTERN = re.compile(
    r"^docs/03\.specs/(?P<spec>[0-9]{4})-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/"
    r"spec\.md$"
)
WORK054_WP004B_PLAN_PATTERN = re.compile(
    r"^docs/03\.specs/(?P<spec>[0-9]{4})-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/"
    r"plan\.md$"
)
WORK054_WP004B_REQUIREMENT_PATTERN = re.compile(
    r"^docs/01\.requirements/(?P<identity>[0-9]{4})-[a-z0-9]+"
    r"(?:-[a-z0-9]+)*\.md$"
)
WORK054_WP004B_AD_PATTERN = re.compile(
    r"^docs/02\.architecture/descriptions/(?P<identity>[0-9]{4})-"
    r"[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
WORK054_WP004B_ROUTER_TASK_LINK = re.compile(
    r"^- \[`(?P<artifact>TSK-[0-9]{4}-[0-9]{4})` — "
    r"`(?P<legacy>[^`]+)`\]\((?P<path>tasks/tsk-[0-9]{4}-[a-z0-9]+"
    r"(?:-[a-z0-9]+)*\.md)\)$"
)
WORK054_WP004B_TASK_STATUSES = MappingProxyType(
    {
        "done": "done",
        "complete": "done",
        "completed": "done",
        "archived": "done",
        "transferred": "done",
        "in progress": "in-progress",
        "in-progress": "in-progress",
        "queued": "queued",
        "pending": "queued",
        "blocked": "blocked",
        "cancelled": "cancelled",
        "canceled": "cancelled",
    }
)


@dataclass(frozen=True)
class _Work054Wp004bAdmission:
    paths: frozenset[PurePosixPath]
    diagnostics: frozenset[tuple[PurePosixPath, str, str, str]]


_EMPTY_WORK054_WP004B_ADMISSION = _Work054Wp004bAdmission(frozenset(), frozenset())


def _registry_profile_ids(raw_registry: Mapping[str, object]) -> frozenset[str]:
    profiles = raw_registry.get("profiles")
    if not isinstance(profiles, list):
        return frozenset()
    return frozenset(
        profile["id"]
        for profile in profiles
        if isinstance(profile, dict) and isinstance(profile.get("id"), str)
    )


def _work054_wp004b_document(
    root: Path,
    registry: Registry,
    path: PurePosixPath,
    oid: str | None,
    *,
    profile_id: str,
    status: str | None,
    artifact_id: str | None,
    blob_reader: Callable[[str], bytes] | None = None,
) -> LifecycleDocument | None:
    if oid is None:
        return None
    try:
        raw = (blob_reader or (lambda value: _blob_bytes(root, value)))(oid)
        text = raw.decode("utf-8")
        document = document_from_text(registry, path, text)
    except (InvocationError, UnicodeDecodeError, DocumentContractError):
        return None
    if (
        document.profile_id != profile_id
        or document.status != status
        or document.state_issue is not None
    ):
        return None
    if artifact_id is None:
        return document if not text.startswith("---\n") else None
    return (
        document
        if _work054_wp002_frontmatter_value(raw, "artifact_id") == artifact_id
        else None
    )


def _work054_wp004b_table_cells(line: str) -> tuple[str, ...] | None:
    if not line.startswith("|") or not line.endswith("|"):
        return None
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    in_code = False
    for character in line[1:-1]:
        if escaped:
            current.append(character)
            escaped = False
        elif character == "\\":
            current.append(character)
            escaped = True
        elif character == "`":
            current.append(character)
            in_code = not in_code
        elif character == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    if escaped or in_code:
        return None
    cells.append("".join(current).strip())
    return tuple(cells)


def _work054_wp004b_task_table(
    raw: bytes,
) -> tuple[str, str, tuple[tuple[str, tuple[str, ...]], ...]] | None:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    marker = "\n## Task Table\n"
    if text.count(marker) != 1:
        return None
    section = re.split(r"\n#{2,6} ", text.partition(marker)[2], maxsplit=1)[0]
    blocks: list[list[str]] = []
    block: list[str] = []
    for line in section.splitlines():
        if line.startswith("|"):
            block.append(line)
        elif block:
            blocks.append(block)
            block = []
    if block:
        blocks.append(block)

    candidates: list[tuple[str, str, tuple[tuple[str, tuple[str, ...]], ...]]] = []
    for lines in blocks:
        if len(lines) < 3:
            continue
        header = _work054_wp004b_table_cells(lines[0])
        separator = _work054_wp004b_table_cells(lines[1])
        if (
            header is None
            or separator is None
            or len(header) != len(separator)
            or any(re.fullmatch(r":?-{3,}:?", cell) is None for cell in separator)
            or "id" not in {cell.lower() for cell in header}
            or "status" not in {cell.lower() for cell in header}
        ):
            continue
        rows: list[tuple[str, tuple[str, ...]]] = []
        for line in lines[2:]:
            cells = _work054_wp004b_table_cells(line)
            if cells is None or len(cells) != len(header):
                rows = []
                break
            rows.append((line, cells))
        if rows:
            candidates.append((lines[0], lines[1], tuple(rows)))
    return candidates[0] if len(candidates) == 1 else None


def _work054_wp004b_task_slug(legacy_id: str) -> str | None:
    slug = re.sub(r"[^a-z0-9]+", "-", legacy_id.lower()).strip("-")
    return slug if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) else None


def _work054_wp004b_legacy_id(raw: str) -> str:
    link = re.fullmatch(r"\[(?P<label>[A-Za-z0-9-]+)\]\([^)]*\)", raw)
    return link.group("label") if link is not None else raw


def _work054_wp004b_task_title(raw: str) -> str:
    return raw.replace("\\|", "|").replace("`", "").strip()


def _work054_wp004b_render_task(
    *,
    artifact_id: str,
    title: str,
    status: str,
    owner: str,
    updated: str,
    legacy_id: str,
    header_line: str,
    separator_line: str,
    row_line: str,
) -> bytes:
    heading_title = title.rstrip(".")
    quoted_title = json.dumps(f"{artifact_id}: {title}", ensure_ascii=False)
    lifecycle_trace = ""
    if status != "done":
        lifecycle_trace = (
            "\n### Lifecycle Traceability\n\n"
            "| Criterion / work item | Result | Evidence |\n"
            "| --- | --- | --- |\n"
            f"| N/A — legacy work item `{legacy_id}` | Preserved legacy status; "
            f"current Task is `{status}`. | Row-specific result and evidence remain "
            "in the Task Table above. |\n\n"
        )
    return (
        f"---\n"
        f"title: {quoted_title}\n"
        f'version: "1.0.0"\n'
        f"type: sdlc/task\n"
        f'layer: "specs"\n'
        f"status: {status}\n"
        f"owner: {owner}\n"
        f"updated: {updated}\n"
        f'artifact_id: "{artifact_id}"\n'
        f"---\n\n"
        f"# {artifact_id}: {heading_title}\n\n"
        f"## Overview\n\n"
        f"Append-only Task record for legacy work item `{legacy_id}` from the package's\n"
        f"decomposed monolithic ledger. The exact row below preserves its criterion,\n"
        f"dependency, owner, result, and evidence.\n\n"
        f"## Inputs\n\n"
        f"- [Owning Spec](../spec.md)\n"
        f"- [Owning Plan](../plan.md)\n"
        f"- [Migration recovery ledger](../../../98.archive/migrations/0004-document-authority-convergence.md)\n\n"
        f"## Task Table\n\n"
        f"{header_line}\n"
        f"{separator_line}\n"
        f"{row_line}\n\n"
        f"## Approval and Safety Boundaries\n\n"
        f"The shared approval, safety, and rollback contract is preserved once in the\n"
        f"[owning Plan](../plan.md#legacy-task-approval-and-rollback-boundaries). This\n"
        f"record does not broaden that contract.\n\n"
        f"## Verification Summary\n\n"
        f"The row-specific validation/result/evidence is preserved verbatim above. The\n"
        f"shared verification context is in the\n"
        f"[owning Plan](../plan.md#legacy-task-verification-evidence).\n\n"
        f"## Traceability\n\n"
        f"- Stable Task: `{artifact_id}`\n"
        f"- Legacy work item: `{legacy_id}`\n"
        f"{lifecycle_trace}"
        f"- Legacy bytes: [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)\n"
    ).encode("utf-8")


def _work054_wp004b_admission(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    base_registry: Registry,
    proposed_registry: Registry,
) -> _Work054Wp004bAdmission:
    """Admit only the cutover projected by sealed MIG-0004 authority."""

    if mode not in {"staged", "ci"} or base_commit != MIG0004_TERMINAL_SOURCE_COMMIT:
        return _EMPTY_WORK054_WP004B_ADMISSION
    blob_cache: dict[str, bytes] = {}

    def read_blob(oid: str) -> bytes:
        if oid not in blob_cache:
            blob_cache[oid] = _blob_bytes(root, oid)
        return blob_cache[oid]

    migration_oid = proposed_blobs.get(WORK054_WP004B_MIGRATION_PATH)
    if migration_oid is None or WORK054_WP004B_MIGRATION_PATH in base_blobs:
        return _EMPTY_WORK054_WP004B_ADMISSION
    try:
        migration_bytes = read_blob(migration_oid)
        rows = parse_pinned_migration_control(
            WORK054_WP004B_MIGRATION_PATH.as_posix(),
            migration_bytes,
        )
    except (ArchiveContractError, InvocationError):
        return _EMPTY_WORK054_WP004B_ADMISSION

    migration_document = _work054_wp004b_document(
        root,
        proposed_registry,
        WORK054_WP004B_MIGRATION_PATH,
        migration_oid,
        profile_id="archive/migration",
        status="sealed",
        artifact_id="MIG-0004",
        blob_reader=read_blob,
    )
    if migration_document is None:
        return _EMPTY_WORK054_WP004B_ADMISSION

    consumed: set[PurePosixPath] = {WORK054_WP004B_MIGRATION_PATH}
    allowed_diagnostics: set[tuple[PurePosixPath, str, str, str]] = {
        (
            WORK054_WP004B_MIGRATION_PATH,
            "LIFECYCLE-CREATE",
            "archive/migration",
            "absent -> sealed",
        )
    }
    task_packages: set[PurePosixPath] = set()
    requirement_paths: set[PurePosixPath] = set()
    architecture_paths: set[PurePosixPath] = set()
    agent_replacements: set[PurePosixPath] = set()
    expected_task_paths: set[PurePosixPath] = set()
    expected_task_labels: dict[PurePosixPath, tuple[str, str]] = {}
    for row in rows:
        legacy_raw = row.get("legacy_path")
        source_commit = row.get("source_commit")
        source_blob = row.get("source_blob")
        action = row.get("action")
        if (
            not isinstance(legacy_raw, str)
            or not isinstance(source_blob, str)
            or source_commit != base_commit
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        legacy = PurePosixPath(legacy_raw)
        if base_blobs.get(legacy) != source_blob:
            return _EMPTY_WORK054_WP004B_ADMISSION
        target_raw = row.get("stable_path") or row.get("replacement")
        target = PurePosixPath(target_raw) if isinstance(target_raw, str) else None
        if action == "replaced" and target == legacy:
            proposed_oid = proposed_blobs.get(legacy)
            if proposed_oid is None or proposed_oid == source_blob:
                return _EMPTY_WORK054_WP004B_ADMISSION
            requirement_match = WORK054_WP004B_REQUIREMENT_PATTERN.fullmatch(
                legacy.as_posix()
            )
            if requirement_match is None:
                return _EMPTY_WORK054_WP004B_ADMISSION
            identity = requirement_match.group("identity")
            base_status = _work054_wp002_frontmatter_value(
                read_blob(source_blob), "status"
            )
            expected_status = {
                "active": "active",
                "done": "superseded",
            }.get(base_status or "")
            if (
                expected_status is None
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/prd",
                    status=base_status,
                    artifact_id=f"PRD-{identity}",
                    blob_reader=read_blob,
                )
                is None
                or _work054_wp004b_document(
                    root,
                    proposed_registry,
                    legacy,
                    proposed_oid,
                    profile_id=WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE,
                    status=expected_status,
                    artifact_id=f"REQ-{identity}",
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            target_bytes = read_blob(proposed_oid)
            if expected_status == "superseded" and (
                _work054_wp002_frontmatter_value(target_bytes, "superseded_by")
                != "REQ-0008"
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            if identity == "0008":
                supersedes = _work054_wp002_frontmatter_value(
                    target_bytes, "supersedes"
                )
                if supersedes is None or set(
                    re.findall(r"REQ-[0-9]{4}", supersedes)
                ) != {"REQ-0005", "REQ-0006"}:
                    return _EMPTY_WORK054_WP004B_ADMISSION
            requirement_paths.add(legacy)
            consumed.add(legacy)
            allowed_diagnostics.add(
                (
                    legacy,
                    "LIFECYCLE-STATE",
                    WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE,
                    "sdlc/prd -> sdlc/requirement-package; "
                    "current registry classification unavailable",
                )
            )
            continue
        if target is None or target not in proposed_blobs:
            return _EMPTY_WORK054_WP004B_ADMISSION
        if legacy in proposed_blobs:
            return _EMPTY_WORK054_WP004B_ADMISSION
        if action == "moved":
            identity = row.get("artifact_id")
            match = WORK054_WP004B_AD_PATTERN.fullmatch(target.as_posix())
            base_status = _work054_wp002_frontmatter_value(
                read_blob(source_blob), "status"
            )
            if (
                match is None
                or identity != f"AD-{match.group('identity')}"
                or base_status is None
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/architecture-description",
                    status=base_status,
                    artifact_id=str(identity),
                    blob_reader=read_blob,
                )
                is None
                or _work054_wp004b_document(
                    root,
                    proposed_registry,
                    target,
                    proposed_blobs[target],
                    profile_id="sdlc/architecture-description",
                    status=base_status,
                    artifact_id=str(identity),
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            architecture_paths.add(target)
            consumed.update((legacy, target))
            if source_blob == proposed_blobs[target]:
                allowed_diagnostics.add(
                    (
                        target,
                        "LIFECYCLE-RENAME",
                        "sdlc/architecture-description",
                        f"{legacy.as_posix()} -> {target.as_posix()}",
                    )
                )
            else:
                allowed_diagnostics.update(
                    {
                        (
                            legacy,
                            "LIFECYCLE-DELETE",
                            "sdlc/architecture-description",
                            f"{base_status} -> absent",
                        ),
                        (
                            target,
                            "LIFECYCLE-CREATE",
                            "sdlc/architecture-description",
                            f"absent -> {base_status}",
                        ),
                    }
                )
            continue
        if action == "replaced" and legacy.name == "tasks.md":
            if target.name != "README.md" or target in base_blobs:
                return _EMPTY_WORK054_WP004B_ADMISSION
            source_bytes = read_blob(source_blob)
            source_table = _work054_wp004b_task_table(source_bytes)
            source_status = _work054_wp002_frontmatter_value(source_bytes, "status")
            source_owner = _work054_wp002_frontmatter_value(source_bytes, "owner")
            source_updated = _work054_wp002_frontmatter_value(source_bytes, "updated")
            spec_number = legacy.parent.name[:4]
            if (
                source_table is None
                or source_status is None
                or source_owner is None
                or source_updated is None
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/task",
                    status=source_status,
                    artifact_id=f"TASK-{spec_number}",
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            header_line, separator_line, source_rows = source_table
            headers = _work054_wp004b_table_cells(header_line)
            assert headers is not None
            lowered_headers = tuple(cell.lower() for cell in headers)
            try:
                status_index = lowered_headers.index("status")
            except ValueError:
                return _EMPTY_WORK054_WP004B_ADMISSION
            owner_index = (
                lowered_headers.index("owner") if "owner" in lowered_headers else None
            )
            for sequence, (row_line, cells) in enumerate(source_rows, 1):
                legacy_id = _work054_wp004b_legacy_id(cells[0])
                slug = _work054_wp004b_task_slug(legacy_id)
                status = WORK054_WP004B_TASK_STATUSES.get(
                    cells[status_index].strip().lower()
                )
                row_owner = (
                    cells[owner_index].strip()
                    if owner_index is not None
                    else source_owner
                )
                artifact_id = f"TSK-{spec_number}-{sequence:04d}"
                if slug is None or status is None or not row_owner:
                    return _EMPTY_WORK054_WP004B_ADMISSION
                task_path = legacy.parent / "tasks" / f"tsk-{sequence:04d}-{slug}.md"
                task_oid = proposed_blobs.get(task_path)
                task_bytes = read_blob(task_oid) if task_oid is not None else b""
                task_table = _work054_wp004b_task_table(task_bytes)
                if task_table is None:
                    return _EMPTY_WORK054_WP004B_ADMISSION
                task_header, task_separator, task_rows = task_table
                target_cells = task_rows[0][1] if len(task_rows) == 1 else ()
                if (
                    task_header != header_line
                    or task_separator != separator_line
                    or len(task_rows) != 1
                    or len(target_cells) != len(cells)
                    or _work054_wp004b_legacy_id(target_cells[0]) != legacy_id
                    or target_cells[1] != cells[1]
                    or (
                        owner_index is not None
                        and target_cells[owner_index] != cells[owner_index]
                    )
                    or target_cells[status_index] != cells[status_index]
                    or any(not cell for cell in target_cells)
                ):
                    return _EMPTY_WORK054_WP004B_ADMISSION
                projected_row = task_rows[0][0]
                expected = _work054_wp004b_render_task(
                    artifact_id=artifact_id,
                    title=_work054_wp004b_task_title(cells[1]),
                    status=status,
                    owner=source_owner,
                    updated=source_updated,
                    legacy_id=legacy_id,
                    header_line=header_line,
                    separator_line=separator_line,
                    row_line=projected_row,
                )
                if (
                    task_oid is None
                    or task_bytes != expected
                    or _work054_wp004b_document(
                        root,
                        proposed_registry,
                        task_path,
                        task_oid,
                        profile_id="sdlc/task",
                        status=status,
                        artifact_id=artifact_id,
                        blob_reader=read_blob,
                    )
                    is None
                ):
                    return _EMPTY_WORK054_WP004B_ADMISSION
                expected_task_paths.add(task_path)
                expected_task_labels[task_path] = (artifact_id, legacy_id)
                allowed_diagnostics.add(
                    (
                        task_path,
                        "LIFECYCLE-CREATE",
                        "sdlc/task",
                        f"absent -> {status}",
                    )
                )
            task_packages.add(legacy.parent)
            consumed.update((legacy, target))
            allowed_diagnostics.add(
                (
                    legacy,
                    "LIFECYCLE-DELETE",
                    "sdlc/task",
                    f"{source_status} -> absent",
                )
            )
            continue
        if action == "merged" and legacy.name == "agent-design.md":
            source_status = _work054_wp002_frontmatter_value(
                read_blob(source_blob), "status"
            )
            spec_number = legacy.parent.name[:4]
            target_oid = proposed_blobs.get(target)
            if (
                source_status is None
                or target.name != "spec.md"
                or target_oid is None
                or target_oid == base_blobs.get(target)
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/agent-design",
                    status=source_status,
                    artifact_id=f"AGENT-DESIGN-{spec_number}",
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            agent_replacements.add(target)
            consumed.update((legacy, target))
            allowed_diagnostics.add(
                (
                    legacy,
                    "LIFECYCLE-DELETE",
                    "sdlc/agent-design",
                    f"{source_status} -> absent",
                )
            )
            continue
        return _EMPTY_WORK054_WP004B_ADMISSION

    routers = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_ROUTER_PATTERN.fullmatch(path.as_posix())
    }
    tasks = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_TASK_PATTERN.fullmatch(path.as_posix())
    }
    specs = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_SPEC_PATTERN.fullmatch(path.as_posix())
    }
    plans = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_PLAN_PATTERN.fullmatch(path.as_posix())
    }
    spec_packages = {path.parent for path in specs}
    task_owners = {path.parent.parent for path in tasks}
    if (
        tasks != expected_task_paths
        or any(path in base_blobs for path in routers | tasks)
        or task_owners != task_packages
        or {path.parent for path in routers} != spec_packages
        or not task_packages <= spec_packages
        or {path.parent for path in plans} - spec_packages
        or {
            path
            for path in proposed_blobs
            if WORK054_WP004B_REQUIREMENT_PATTERN.fullmatch(path.as_posix())
        }
        != requirement_paths
        or {
            path
            for path in proposed_blobs
            if WORK054_WP004B_AD_PATTERN.fullmatch(path.as_posix())
        }
        != architecture_paths
    ):
        return _EMPTY_WORK054_WP004B_ADMISSION

    for spec_path in specs:
        spec_match = WORK054_WP004B_SPEC_PATTERN.fullmatch(spec_path.as_posix())
        assert spec_match is not None
        base_oid = base_blobs.get(spec_path)
        base_status = (
            _work054_wp002_frontmatter_value(read_blob(base_oid), "status")
            if base_oid is not None
            else None
        )
        if (
            base_oid is None
            or base_status is None
            or _work054_wp004b_document(
                root,
                proposed_registry,
                spec_path,
                proposed_blobs[spec_path],
                profile_id="sdlc/spec",
                status=base_status,
                artifact_id=f"SPEC-{spec_match.group('spec')}",
                blob_reader=read_blob,
            )
            is None
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        consumed.add(spec_path)

    for plan_path in plans:
        plan_match = WORK054_WP004B_PLAN_PATTERN.fullmatch(plan_path.as_posix())
        assert plan_match is not None
        base_oid = base_blobs.get(plan_path)
        base_status = (
            _work054_wp002_frontmatter_value(read_blob(base_oid), "status")
            if base_oid is not None
            else None
        )
        if (
            base_oid is None
            or base_status is None
            or _work054_wp004b_document(
                root,
                proposed_registry,
                plan_path,
                proposed_blobs[plan_path],
                profile_id="sdlc/plan",
                status=base_status,
                artifact_id=f"PLAN-{plan_match.group('spec')}",
                blob_reader=read_blob,
            )
            is None
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        consumed.add(plan_path)

    if not agent_replacements <= specs:
        return _EMPTY_WORK054_WP004B_ADMISSION

    for router in routers:
        router_oid = proposed_blobs[router]
        if (
            _work054_wp004b_document(
                root,
                proposed_registry,
                router,
                router_oid,
                profile_id="common/readme-collection-index",
                status=None,
                artifact_id=None,
                blob_reader=read_blob,
            )
            is None
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        router_text = read_blob(router_oid).decode("utf-8")
        marker = "\n## Task Records\n"
        if router_text.count(marker) != 1 or router_text.count("(spec.md)") != 1:
            return _EMPTY_WORK054_WP004B_ADMISSION
        package = router.parent
        plan_exists = package / "plan.md" in plans
        if router_text.count("(plan.md)") != int(plan_exists):
            return _EMPTY_WORK054_WP004B_ADMISSION
        section = router_text.partition(marker)[2].partition("\n## ")[0]
        links: dict[PurePosixPath, tuple[str, str]] = {}
        for line in section.splitlines():
            match = WORK054_WP004B_ROUTER_TASK_LINK.fullmatch(line)
            if match is None:
                continue
            task_path = package / match.group("path")
            if task_path in links:
                return _EMPTY_WORK054_WP004B_ADMISSION
            links[task_path] = (match.group("artifact"), match.group("legacy"))
        actual = {path for path in tasks if path.parent.parent == package}
        if (
            set(links) != actual
            or any(links[path] != expected_task_labels[path] for path in actual)
            or router_text.count("](tasks/tsk-") != len(actual)
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        allowed_diagnostics.add(
            (
                router,
                "LIFECYCLE-CREATE",
                "common/readme-collection-index",
                "absent -> not-applicable",
            )
        )
    consumed.update(routers)
    consumed.update(tasks)
    return _Work054Wp004bAdmission(frozenset(consumed), frozenset(allowed_diagnostics))


def finite_work054_wp004b_document_authority_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Return paths only after exact WP-004B tree-object projection succeeds."""

    try:
        current_registry = load_registry(root)
        base_registry = _classification_registry(
            current_registry,
            _registry_blob(
                root,
                _tree_blob_oid(root, base_commit, RETIRED_REGISTRY_PATH),
            ),
        )
        proposed_registry = current_registry
    except (DocumentContractError, InvocationError):
        return frozenset()
    return _work054_wp004b_admission(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
        base_registry=base_registry,
        proposed_registry=proposed_registry,
    ).paths


def _git_blob_oid(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()  # noqa: S324 - Git identity


def sealed_record_relocation_paths(
    *,
    root: Path,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit each record vacancy a sealed ledger declares as a byte-identical move.

    A sealed record is immutable, and the directory holding it is a claim about
    why its origin ended. A later cycle can find that claim wrong, and correcting
    it deletes the record at one path and recreates it at another. The
    immutability rule reads that departure as a record being lost unless a sealed
    `moved` row accounts for it.

    A row is admitted only when the bytes leaving the origin and the bytes
    arriving at the target are identical and both equal the digest the row pins.
    A move that changed a byte is not a move, and this admits nothing then: like
    the declared tables beside it, one bad pair withdraws the whole admission.

    Unlike those tables the pairs are read from the sealed ledger rather than
    restated here, because the ledger is already the reviewed evidence for the
    move and a second copy could only disagree with it.
    """

    admitted: set[PurePosixPath] = set()
    for path, oid in sorted(proposed_blobs.items()):
        if generic_migration_id(path.as_posix()) is None:
            continue
        try:
            content = _blob_bytes(root, oid, max_bytes=MIGRATION_DOCUMENT_MAX_BYTES)
            if not is_sealed_migration(content):
                continue
            rows, _consumers = parse_migration_control(path.as_posix(), content)
        except (ArchiveContractError, InvocationError, OSError, ValueError):
            return frozenset()
        for row in rows:
            if row.get("action") != "moved":
                continue
            legacy = PurePosixPath(str(row.get("legacy_path")))
            target = PurePosixPath(str(row.get("stable_path")))
            base_oid = base_blobs.get(legacy)
            proposed_oid = proposed_blobs.get(target)
            if base_oid is None or proposed_oid is None:
                # Either the move already landed in an earlier commit or this row
                # moves something that is not a record. Neither is a vacancy for
                # this admission to fill.
                continue
            digest = row.get("content_sha256")
            try:
                base_digest = hashlib.sha256(_blob_bytes(root, base_oid)).hexdigest()
                target_digest = hashlib.sha256(
                    _blob_bytes(root, proposed_oid)
                ).hexdigest()
            except (InvocationError, OSError):
                return frozenset()
            if base_digest != digest or target_digest != digest:
                return frozenset()
            admitted.add(legacy)
    return frozenset(admitted)


def _work054_wp002_frontmatter_value(raw: bytes, key: str) -> str | None:
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return None
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    matches: list[str] = []
    prefix = f"{key}:"
    for line in lines[1:end]:
        if not line.startswith(prefix):
            continue
        value = line[len(prefix) :].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        matches.append(value)
    return matches[0] if len(matches) == 1 else None


def _wp004c_mig0004_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit only source-pinned WP-004C Stage99 and Spec0054 cutover rows."""

    if mode not in {"staged", "ci"}:
        return frozenset()
    migration_oid = proposed_blobs.get(WORK054_WP004B_MIGRATION_PATH)
    if migration_oid is None:
        return frozenset()
    try:
        rows = parse_pinned_migration_control(
            WORK054_WP004B_MIGRATION_PATH.as_posix(),
            _blob_bytes(root, migration_oid),
        )
    except (ArchiveContractError, InvocationError):
        return frozenset()

    cutover_rows = [row for row in rows if row.get("source_commit") == base_commit]
    task_legacy = PurePosixPath(
        "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
    )
    stage99_rows = [
        row
        for row in cutover_rows
        if isinstance(row.get("legacy_path"), str)
        and str(row["legacy_path"]).startswith("docs/99.templates/")
        and _approved_markdown(PurePosixPath(str(row["legacy_path"])))
    ]
    task_rows = [
        row for row in cutover_rows if row.get("legacy_path") == task_legacy.as_posix()
    ]
    if len(task_rows) != 1 or not stage99_rows:
        return frozenset()

    try:
        durable_ref = current_named_durable_ref(root)
        require_commits_reachable_from_durable_refs(
            root, (WP004C_SEALED_TARGET_COMMIT,), (durable_ref,)
        )
        sealed_target_blobs = _tree_blob_map(root, WP004C_SEALED_TARGET_COMMIT)
    except (ArchiveContractError, InvocationError):
        return frozenset()

    consumed: set[PurePosixPath] = set()
    stage99_legacy: set[PurePosixPath] = set()
    for row in stage99_rows:
        legacy_raw = row.get("legacy_path")
        source_blob = row.get("source_blob")
        digest = row.get("content_sha256")
        action = row.get("action")
        target_raw = (
            row.get("stable_path") if action == "moved" else row.get("replacement")
        )
        if not all(
            isinstance(value, str)
            for value in (legacy_raw, source_blob, digest, target_raw)
        ):
            return frozenset()
        legacy = PurePosixPath(legacy_raw)
        target = PurePosixPath(target_raw)
        if (
            legacy in stage99_legacy
            or base_blobs.get(legacy) != source_blob
            or hashlib.sha256(_blob_bytes(root, source_blob)).hexdigest() != digest
            or legacy in proposed_blobs
            or target not in proposed_blobs
            or action not in {"moved", "replaced"}
            or (action == "moved" and sealed_target_blobs.get(target) != source_blob)
        ):
            return frozenset()
        stage99_legacy.add(legacy)
        consumed.update((legacy, target))

    deleted_stage99 = {
        path
        for path in base_blobs
        if path.as_posix().startswith("docs/99.templates/")
        and path not in proposed_blobs
    }
    if stage99_legacy != deleted_stage99:
        return frozenset()

    task_row = task_rows[0]
    if (
        task_row.get("action") != "replaced"
        or task_row.get("stable_path") is not None
        or task_row.get("replacement") != (task_legacy.parent / "README.md").as_posix()
        or not isinstance(task_row.get("source_blob"), str)
        or not isinstance(task_row.get("content_sha256"), str)
    ):
        return frozenset()
    source_blob = str(task_row["source_blob"])
    source = _blob_bytes(root, source_blob)
    if (
        base_blobs.get(task_legacy) != source_blob
        or hashlib.sha256(source).hexdigest() != task_row["content_sha256"]
    ):
        return frozenset()
    source_table = _work054_wp004b_task_table(source)
    source_status = _work054_wp002_frontmatter_value(source, "status")
    source_owner = _work054_wp002_frontmatter_value(source, "owner")
    source_updated = _work054_wp002_frontmatter_value(source, "updated")
    readme_path = task_legacy.parent / "README.md"
    readme_oid = proposed_blobs.get(readme_path)
    if (
        source_table is None
        or source_status is None
        or source_owner is None
        or source_updated is None
        or readme_oid is None
    ):
        return frozenset()
    header_line, separator_line, source_entries = source_table
    headers = _work054_wp004b_task_table(source)
    assert headers is not None
    parsed_header = _work054_wp004b_table_cells(header_line)
    if parsed_header is None:
        return frozenset()
    try:
        status_index = tuple(cell.lower() for cell in parsed_header).index("status")
    except ValueError:
        return frozenset()
    readme = _blob_bytes(root, readme_oid).decode("utf-8", errors="strict")
    task_links: dict[str, PurePosixPath] = {}
    for line in readme.splitlines():
        match = re.fullmatch(
            r"- \[`(?P<artifact>TSK-0054-(?P<sequence>[0-9]{4}))`\]"
            r"\((?P<relative>tasks/tsk-(?P=sequence)-[a-z0-9]+"
            r"(?:-[a-z0-9]+)*\.md)\)",
            line,
        )
        if match is None:
            continue
        artifact_id = match.group("artifact")
        path = task_legacy.parent / match.group("relative")
        if artifact_id in task_links or path in task_links.values():
            return frozenset()
        task_links[artifact_id] = path
    if len(task_links) != len(source_entries):
        return frozenset()

    expected_tasks: set[PurePosixPath] = set()
    for sequence, (row_line, cells) in enumerate(source_entries, 1):
        legacy_id = _work054_wp004b_legacy_id(cells[0])
        state = WORK054_WP004B_TASK_STATUSES.get(cells[status_index].strip().lower())
        if legacy_id is None or state is None:
            return frozenset()
        artifact_id = f"TSK-0054-{sequence:04d}"
        path = task_links.get(artifact_id)
        if path is None:
            return frozenset()
        oid = proposed_blobs.get(path)
        if oid is None:
            return frozenset()
        task_bytes = _blob_bytes(root, oid)
        task_table = _work054_wp004b_task_table(task_bytes)
        if task_table is None or path.name not in readme:
            return frozenset()
        task_header, task_separator, task_entries = task_table
        task_cells = task_entries[0][1] if len(task_entries) == 1 else ()
        task_text = task_bytes.decode("utf-8", errors="strict")
        checks = {
            "header": task_header == header_line,
            "separator": task_separator == separator_line,
            "work-row": task_cells == cells,
            "artifact-id": f'artifact_id: "{artifact_id}"' in task_text,
            "status": f"status: {state}" in task_text,
            "wp": f"**Plan label:** WP-{sequence:03d}" in task_text,
            "legacy-id": legacy_id in task_text,
            "common-contract": "../README.md#common-execution-contract" in task_text,
            "plan-link": "../plan.md" in task_text,
        }
        failed = next((name for name, valid in checks.items() if not valid), None)
        if failed is not None:
            raise InvocationError(
                f"WP004C MIG-0004 task proof failed: {path.as_posix()}:{failed}"
            )
        expected_tasks.add(path)
    actual_tasks = {
        path for path in proposed_blobs if path.parent == task_legacy.parent / "tasks"
    }
    if expected_tasks != actual_tasks:
        return frozenset()
    consumed.update((task_legacy, readme_path, *expected_tasks))
    if any(
        path.suffix == ".md"
        and path in proposed_blobs
        and sealed_target_blobs.get(path) != proposed_blobs[path]
        for path in consumed
    ):
        return frozenset()
    for path in set(base_blobs) & set(proposed_blobs):
        if path.suffix != ".md" or base_blobs[path] == proposed_blobs[path]:
            continue
        if sealed_target_blobs.get(path) != proposed_blobs[path]:
            return frozenset()
        consumed.add(path)
    return frozenset(consumed)


def finite_work054_wp003_agent_governance_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit only the exact WORK-054 WP-003 legacy owner retirements."""

    if mode not in {"staged", "ci"} or base_commit != WORK054_WP003_BASE_COMMIT:
        return frozenset()
    migration_oid = proposed_blobs.get(WORK054_WP003_MIGRATION_PATH)
    if WORK054_WP003_MIGRATION_PATH in base_blobs or migration_oid is None:
        return frozenset()
    try:
        migration_bytes = _blob_bytes(root, migration_oid)
        migration_text = migration_bytes.decode("utf-8")
    except (InvocationError, OSError, UnicodeDecodeError):
        return frozenset()
    if hashlib.sha256(migration_bytes).hexdigest() != WORK054_WP003_MIGRATION_SHA256:
        return frozenset()
    marker = "<!-- archive-migration-ledger:v1 format=json -->\n\n```json\n"
    if migration_text.count(marker) != 1:
        return frozenset()
    _prefix, remainder = migration_text.split(marker, 1)
    if remainder.count("\n```") != 1:
        return frozenset()
    raw_rows, suffix = remainder.split("\n```", 1)
    if not suffix.startswith("\n\n## Recovery\n"):
        return frozenset()
    try:
        rows = json.loads(raw_rows)
    except json.JSONDecodeError:
        return frozenset()
    if not isinstance(rows, list) or len(rows) != len(WORK054_WP003_OWNER_RETIREMENTS):
        return frozenset()
    consumed: set[PurePosixPath] = {WORK054_WP003_MIGRATION_PATH}
    for row, expected in zip(rows, WORK054_WP003_OWNER_RETIREMENTS, strict=True):
        if not isinstance(row, Mapping) or tuple(row) != WORK054_WP003_LEDGER_KEYS:
            return frozenset()
        for key, value in expected.items():
            if row.get(key) != value:
                return frozenset()
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            return frozenset()
        legacy = PurePosixPath(str(row["legacy_path"]))
        replacement = PurePosixPath(str(row["replacement"]))
        if (
            base_blobs.get(legacy) != row["source_blob"]
            or legacy in proposed_blobs
            or replacement not in proposed_blobs
        ):
            return frozenset()
        consumed.add(legacy)
    return frozenset(consumed) if len(consumed) == 4 else frozenset()


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
    output_limit: int = GIT_CAPTURE_MAX_BYTES,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return _git_capture_bounded(
            root,
            *GIT_GLOBAL_ARGUMENTS,
            *arguments,
            stdout_limit=output_limit,
            input_bytes=input_bytes,
        )
    except ArchiveContractError as exc:
        raise InvocationError(
            f"bounded git provenance failed for "
            f"{arguments[0] if arguments else 'command'}"
        ) from exc


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


def _archive_immutability_diagnostics(
    root: Path,
    base_registry: Registry,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    *,
    mode: str,
    admitted_rehome_paths: frozenset[PurePosixPath] = frozenset(),
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
        if path in admitted_rehome_paths:
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


def _migration_immutability_diagnostics(
    root: Path,
    registry: Registry,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    *,
    mode: str,
) -> tuple[LifecycleDiagnostic, ...]:
    """Protect whole sealed Migration blobs before any event admission."""

    diagnostics: list[LifecycleDiagnostic] = []
    for path, oid in base_blobs.items():
        try:
            profile = classify_path(registry, path)
        except DocumentContractError:
            continue
        if profile.profile_id != "archive/migration":
            continue
        text = _blob_text(root, oid, path)
        assert text is not None
        document = document_from_text(registry, path, text)
        if document.status != "sealed" or proposed_blobs.get(path) == oid:
            continue
        proposed_text = (
            _blob_text(root, proposed_blobs[path], path)
            if path in proposed_blobs
            else None
        )
        if _is_declared_reseal(
            path,
            hashlib.sha256(text.encode("utf-8")).hexdigest(),
            None
            if proposed_text is None
            else hashlib.sha256(proposed_text.encode("utf-8")).hexdigest(),
        ):
            continue
        diagnostics.append(
            LifecycleDiagnostic(
                severity="FAIL",
                rule_id="LIFECYCLE-TERMINAL-MUTATION",
                path=path,
                profile=profile.profile_id,
                expected_transition="sealed Migration Git blob bytes unchanged",
                observed_transition="sealed Migration changed or deleted",
                base_mode=mode,  # type: ignore[arg-type]
                evidence_gap="immutable previously sealed Migration",
            )
        )
    return tuple(diagnostics)


# One declared re-seal: the domain identity key `migration_id` repeated the
# value `artifact_id` already carries, so the consolidated frontmatter contract
# retires it. Sealed Migrations stay byte-immutable against every other change;
# only these exact reviewed base -> proposed byte pairs are admitted, once.
_MIGRATION_DOMAIN_KEY_RESEAL: dict[str, tuple[tuple[str, str], ...]] = {
    "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md": (
        (
            "4e62cb6ba2a394cd9ae546543c85a58c8f105cb5d1ff48cfd8dab8b8b1082206",  # pragma: allowlist secret -- sealed base digest
            "1a2f3264c380f93d435fedf4028a3fb2b843da377e99e2fd4b788dd37df45116",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "1a2f3264c380f93d435fedf4028a3fb2b843da377e99e2fd4b788dd37df45116",  # pragma: allowlist secret -- sealed base digest
            "7d5e02139b32b14b0b32e17f8b53f01757c54584e597de331808276dbf4ad739",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "9d25b3039750bd60c18129ea7fb62576889449407b2f2fb10092b5624e47030f",  # pragma: allowlist secret -- sealed base digest
            "7d5e02139b32b14b0b32e17f8b53f01757c54584e597de331808276dbf4ad739",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0002-sdlc-document-and-governance-consolidation.md": (
        (
            "67032c0b86acbee04a1e713053d164df2e99f4486df79df5161d53975fb82a7a",  # pragma: allowlist secret -- sealed base digest
            "847b8dab8f86b0b16b47decbf59dbf355f2fbae2869582626c43d949f61dfdce",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "05527226d8d353f57bac1b346aaa20f1ab1951eeea7f2f570b04dbcabd381265",  # pragma: allowlist secret -- sealed base digest
            "847b8dab8f86b0b16b47decbf59dbf355f2fbae2869582626c43d949f61dfdce",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0003-agent-governance-control-plane-consolidation.md": (
        (
            "51fe8d35febac457e562f997a711ce152a98cda67b3aec2ccd8ed08bd3ac3d42",  # pragma: allowlist secret -- sealed base digest
            "67ab2340b257e3dee0bca1a5d3bf757038082e2ffec919bece5d977d5eb919fd",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "6dd85df46123bb7004b0abf0fc7cd1f1d81fcae5ea66f71f1f07ff1dba904ab2",  # pragma: allowlist secret -- sealed base digest
            "67ab2340b257e3dee0bca1a5d3bf757038082e2ffec919bece5d977d5eb919fd",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0004-document-authority-convergence.md": (
        (
            "503a65a5897301be651217fcc48def5351809f272d9af510f10621f2ec2d1fe6",  # pragma: allowlist secret -- sealed base digest
            "870aa210464f9059a4760411d3f8261ab14ae637f0719bd3355b59dd984634c6",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "e7eb94fc16f333a3888e8d5c4d5a17cc65a172bf3dbbf4a115b450e73724dd75",  # pragma: allowlist secret -- sealed base digest
            "870aa210464f9059a4760411d3f8261ab14ae637f0719bd3355b59dd984634c6",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md": (
        (
            "01f9834d73ec930f19d3256e104df8de8549684ae596f7f67a0a7ece28e2b55f",  # pragma: allowlist secret -- sealed base digest
            "f8e5b0a869f9fcc204b358d4c183f123e28c4db2f19329840018a69f61257be4",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "f8e5b0a869f9fcc204b358d4c183f123e28c4db2f19329840018a69f61257be4",  # pragma: allowlist secret -- sealed base digest
            "7779477ee36e9e41cc702649f6a1b3093521932f39fa9bab4d81962c18e112a0",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "c6324af84cc73365f303e96c8e34cae4c0a7717c777017de3e8222b94c0aa7a5",  # pragma: allowlist secret -- sealed base digest
            "7779477ee36e9e41cc702649f6a1b3093521932f39fa9bab4d81962c18e112a0",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "864ac2748c0a21d9b98cc0ddf871fd7335377498d7e554470a9c1a1863e04fdf",  # pragma: allowlist secret -- sealed base digest
            "7779477ee36e9e41cc702649f6a1b3093521932f39fa9bab4d81962c18e112a0",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "abf7a98e9cb9aa0b97ceda0187a0620c30f9eecb93111fa1e92e62dd86c5b6ea",  # pragma: allowlist secret -- sealed base digest
            "864ac2748c0a21d9b98cc0ddf871fd7335377498d7e554470a9c1a1863e04fdf",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "3271e0c9e4cd6698a40736a49334c1186fb958106b62dc1070c520752c850c99",  # pragma: allowlist secret -- sealed base digest
            "abf7a98e9cb9aa0b97ceda0187a0620c30f9eecb93111fa1e92e62dd86c5b6ea",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "3271e0c9e4cd6698a40736a49334c1186fb958106b62dc1070c520752c850c99",  # pragma: allowlist secret -- sealed base digest
            "3271e0c9e4cd6698a40736a49334c1186fb958106b62dc1070c520752c850c99",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "b51a591707de24b5cf2f2af347d9f0affa157cb1952b4da2f16e403ffe641d97",  # pragma: allowlist secret -- sealed base digest
            "3271e0c9e4cd6698a40736a49334c1186fb958106b62dc1070c520752c850c99",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0006-unroutable-reference-profile-retirement.md": (
        (
            "18f5c3088eed3d4e21839a73235e6b7ce572174248517c7822426b9e26bfe2e7",  # pragma: allowlist secret -- sealed base digest
            "36a17557ddbd1afa7e25fc104b11bbc9d46eacddc00eb5928163150244a25ba7",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "316bb28ec68e3850a0bd3c3e6fc345e8b956b923062ade892b3334d54b245793",  # pragma: allowlist secret -- sealed base digest
            "36a17557ddbd1afa7e25fc104b11bbc9d46eacddc00eb5928163150244a25ba7",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0007-agent-progress-ledger-retirement.md": (
        (
            "3e40c188101b9337fe6a4d385eba45aa07dedf4e948403f557e95746795618d7",  # pragma: allowlist secret -- sealed base digest
            "3f4e86833f3b22f891c6ca21ec57467225d697e83d7cb2b97da34c3bd7347055",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "728eb9241d6a76280b597ac9007c6cc278136e4038531b90c818d33978866631",  # pragma: allowlist secret -- sealed base digest
            "3f4e86833f3b22f891c6ca21ec57467225d697e83d7cb2b97da34c3bd7347055",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0008-progress-append-form-retirement.md": (
        (
            "33ec2a510743857b5591d12334f7192ef35287446693596f8e7666da11a24ca4",  # pragma: allowlist secret -- sealed base digest
            "385fc26a65ae0a13c1764f433a524b789a75ceb28cdca968bc2254fe6bb05925",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "bb5f0db3d694d8aa985598f64d0606fa0998bbf001f8f7e024df09bbc4acfc70",  # pragma: allowlist secret -- sealed base digest
            "385fc26a65ae0a13c1764f433a524b789a75ceb28cdca968bc2254fe6bb05925",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0009-governance-memory-retirement.md": (
        (
            "108ebf54112ec1a6467b8141b9136dd13b6bc72dbd0f56e39b9bf62adc1086eb",  # pragma: allowlist secret -- sealed base digest
            "355324d455205d9840c6475f635b5717fdaba3a32541be8fe894b367f3cd27b3",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "6ccca3f7aec2a5395194ba7523f309107b7ef3659595f1e6fa4142f18d4d3433",  # pragma: allowlist secret -- sealed base digest
            "355324d455205d9840c6475f635b5717fdaba3a32541be8fe894b367f3cd27b3",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
}


# A second declared re-seal: the shared frontmatter key set gave every profile
# the same `version` and `layer` keys, and the archive family's profile identity
# became `archive/migration`. Sealed Migrations stay byte-immutable against every
# other change; only these exact reviewed base -> proposed byte pairs are
# admitted, once.
_MIGRATION_SHARED_KEY_RESEAL: dict[str, tuple[tuple[str, str], ...]] = {
    "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md": (
        (
            "7d5e02139b32b14b0b32e17f8b53f01757c54584e597de331808276dbf4ad739",  # pragma: allowlist secret -- sealed base digest
            "bbc0620bd30c2f870aa6f396ba9f08ac09ba77534ccc783d6e7b73c2b10c4df3",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0002-sdlc-document-and-governance-consolidation.md": (
        (
            "847b8dab8f86b0b16b47decbf59dbf355f2fbae2869582626c43d949f61dfdce",  # pragma: allowlist secret -- sealed base digest
            "2cac1634348c9efa985099bb3a2d736609e79849e3aa3d978a8f2a6858a2a45a",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0003-agent-governance-control-plane-consolidation.md": (
        (
            "67ab2340b257e3dee0bca1a5d3bf757038082e2ffec919bece5d977d5eb919fd",  # pragma: allowlist secret -- sealed base digest
            "7baa2a9b2682313d9e8cfc4d3504db14b4985f780f85ff673a4bf535ce4c755e",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0004-document-authority-convergence.md": (
        (
            "870aa210464f9059a4760411d3f8261ab14ae637f0719bd3355b59dd984634c6",  # pragma: allowlist secret -- sealed base digest
            "13ddbddac9c5ce8b50fbab900da20d43d29770113e7c2292db81799df6566b33",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md": (
        (
            "3271e0c9e4cd6698a40736a49334c1186fb958106b62dc1070c520752c850c99",  # pragma: allowlist secret -- sealed base digest
            "628753b0544558b5abd6863da3adf33f9cede484fd36cdce3a8a02330ed42f99",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0006-unroutable-reference-profile-retirement.md": (
        (
            "36a17557ddbd1afa7e25fc104b11bbc9d46eacddc00eb5928163150244a25ba7",  # pragma: allowlist secret -- sealed base digest
            "403d318b65732ee70afbe63bf1311d5628145d87e10e2b2cab4c997e06d1548b",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0007-agent-progress-ledger-retirement.md": (
        (
            "3f4e86833f3b22f891c6ca21ec57467225d697e83d7cb2b97da34c3bd7347055",  # pragma: allowlist secret -- sealed base digest
            "ba034edf349fb9f829d7b2429eb8c1eb02c51d8ee063de8286bb3172497b2f38",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0008-progress-append-form-retirement.md": (
        (
            "385fc26a65ae0a13c1764f433a524b789a75ceb28cdca968bc2254fe6bb05925",  # pragma: allowlist secret -- sealed base digest
            "1dc87b772b16b466973f5b8c4fc2d915245bfc8772090f2d6fe3a770555725eb",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
    "docs/98.archive/migrations/0009-governance-memory-retirement.md": (
        (
            "355324d455205d9840c6475f635b5717fdaba3a32541be8fe894b367f3cd27b3",  # pragma: allowlist secret -- sealed base digest
            "41f1d334ab613c5e118b83190c413765bb6c26a278b26d916b35ef0be26b3352",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
}


# A historical-consumer declaration covers its paths by byte identity, so a
# reviewed change to a declared document invalidates the coverage until the
# declaration names a commit carrying the new bytes.  A consumer identity may
# belong to exactly one sealed record, so the re-pin has to happen inside the
# record that already owns it rather than in a newer one.
_MIGRATION_CONSUMER_REPIN_RESEAL: dict[str, tuple[tuple[str, str], ...]] = {
    "docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md": (
        (
            "628753b0544558b5abd6863da3adf33f9cede484fd36cdce3a8a02330ed42f99",  # pragma: allowlist secret -- sealed base digest
            "fa28fe51353f0cd4ad2611592707dfd42415296cabd56f5a3b727acc9deed0b3",  # pragma: allowlist secret -- re-sealed digest
        ),
        (
            "fa28fe51353f0cd4ad2611592707dfd42415296cabd56f5a3b727acc9deed0b3",  # pragma: allowlist secret -- sealed base digest
            "417f6034f225f7fa73f4ef3f6c72a583f2a2a872ed8321fbdc20a31644760ff1",  # pragma: allowlist secret -- re-sealed digest
        ),
    ),
}


def _is_declared_reseal(path: PurePosixPath, base: str, proposed: str | None) -> bool:
    """Admit only a reviewed byte pair declared for one sealed record change."""

    key = path.as_posix()
    pins = (
        *_MIGRATION_DOMAIN_KEY_RESEAL.get(key, ()),
        *_MIGRATION_SHARED_KEY_RESEAL.get(key, ()),
        *_MIGRATION_CONSUMER_REPIN_RESEAL.get(key, ()),
    )
    return proposed is not None and (base, proposed) in pins


# ADR-0032's generation retained a document only under `completed/`; its
# `superseded/` and `tombstones/` held sealed records and `migrations/` held the
# ledgers. A frozen ledger row is replayed under that generation, so this names
# the frozen generation rather than the current classes, which the registry's
# `retention_classes` owns under ADR-0038.
FROZEN_GENERATION_RETENTION_CLASSES = frozenset({"completed"})


def _is_sealed_record_path(path: PurePosixPath) -> bool:
    """Report whether a path names a sealed record rather than another artifact.

    `migrations/` holds the ledgers that prove the moves and `completed/` holds
    retained documents, which are not records at all. Neither is a record whose
    directory a relocation may decide.
    """

    parts = path.parts
    return (
        len(parts) > 3
        and parts[:2] == ("docs", "98.archive")
        and parts[2] not in {"migrations", *FROZEN_GENERATION_RETENTION_CLASSES}
    )


def _retention_rehome_target(
    source: PurePosixPath, target: PurePosixPath
) -> str | None:
    """Return the retention class when `target` mirrors `source` exactly.

    A retention move relocates a governed document into
    `docs/98.archive/<class>/<its own stage path>` and nowhere else. Proving
    the mirror rather than accepting any Stage 98 destination keeps a ledger
    row from admitting an arbitrary relocation under a retention label.
    """

    parts = target.parts
    if len(parts) < 4 or parts[:2] != ("docs", "98.archive"):
        return None
    retention_class = parts[2]
    if retention_class not in FROZEN_GENERATION_RETENTION_CLASSES:
        return None
    if parts[3:] != source.parts[1:]:
        return None
    return retention_class


def _envelope_object(
    root: Path, commit: str, path: PurePosixPath, base_commit: str
) -> str | None:
    """Return the object a Retention Envelope names when the base can reach it."""

    try:
        _run_git(root, ("merge-base", "--is-ancestor", commit, base_commit))
        raw = _run_git(
            root,
            (
                "rev-parse",
                "--verify",
                "--end-of-options",
                f"{commit}:{path.as_posix()}",
            ),
        )
    except InvocationError:
        return None
    value = raw.decode("ascii", errors="ignore").strip()
    return value if OBJECT_ID.fullmatch(value) is not None else None


def _scope_migration_moves(
    registry: Registry,
    metadata: Mapping[str, object],
    base_blobs: Mapping[PurePosixPath, str],
    base_snapshot: Mapping[PurePosixPath, LifecycleDocument],
    proposed_snapshot: Mapping[PurePosixPath, LifecycleDocument],
    base_texts: Mapping[PurePosixPath, str],
    proposed_texts: Mapping[PurePosixPath, str],
    other_moves: Mapping[PurePosixPath, PurePosixPath],
) -> tuple[set[tuple[PurePosixPath, PurePosixPath]], list[str]]:
    """Pair each document leaving a moved scope with its owner under the new root.

    A moved document keeps its state and identity, and its body differs from
    the source by relative link prefixes alone."""

    scope = canonical_repository_path(metadata.get("moved_scope"))
    owner = canonical_repository_path(metadata.get("current_owner"))
    if scope is None or owner is None or scope == owner:
        return set(), ["moved scope and current owner are not two canonical paths"]
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    moves: set[tuple[PurePosixPath, PurePosixPath]] = set()
    gaps: list[str] = []
    for source in sorted(base_blobs, key=PurePosixPath.as_posix):
        if (
            source != scope and scope not in source.parents
        ) or source in proposed_snapshot:
            continue
        target = owner if source == scope else owner / source.relative_to(scope)
        before, after = base_snapshot.get(source), proposed_snapshot.get(target)
        before_profile = profiles.get(before.profile_id) if before else None
        after_profile = profiles.get(after.profile_id) if after else None
        domain = before_profile.lifecycle_domain if before_profile else None
        if (
            target in base_blobs
            or before is None
            or after is None
            or before.state_issue
            or after.state_issue
            or domain is None
            or before.status is None
            or domain.validation_class(before.status) != "current"
            or after.status != before.status
            or after_profile is None
            or after_profile.lifecycle_domain is None
            or after_profile.lifecycle_domain.family != domain.family
            or after.artifact_id != before.artifact_id
        ):
            gaps.append(f"moved document keeps no current owner: {source.as_posix()}")
            continue
        moves.add((source, target))
    moved = {**other_moves, **dict(moves)}
    for source, target in sorted(moves, key=lambda pair: pair[0].as_posix()):
        if link_resolved_text(base_texts[source], source, moved) != link_resolved_text(
            proposed_texts[target], target
        ):
            gaps.append(
                "moved document differs beyond relative link rebasing: "
                + source.as_posix()
            )
    if not moves and not gaps:
        gaps.append("moved scope names no document this change moves")
    return moves, gaps


def _disposition_lifecycle_events(
    root: Path,
    registry: Registry,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    base_snapshot: Mapping[PurePosixPath, LifecycleDocument],
    base_texts: Mapping[PurePosixPath, str],
    proposed_snapshot: Mapping[PurePosixPath, LifecycleDocument],
    proposed_texts: Mapping[PurePosixPath, str],
    *,
    mode: str,
) -> tuple[MigrationLifecycleEvents, tuple[LifecycleDiagnostic, ...]]:
    """Admit ADR-0038 dispositions from the catalog's one Retention Envelope.

    A retained body is proved by a new catalog row whose `<commit>:<original
    path>` names the exact source object the comparison base holds. A scope
    migration is proved by a new body-less record the catalog names, and it
    admits only documents that keep their current state under the new owner.
    No row carries a digest, a blob pin, or a path ledger; Git holds the bytes.
    """

    index = DISPOSITION_ARCHIVE_INDEX
    proposed_rows, catalog_errors = parse_catalog(proposed_texts.get(index, ""))
    base_rows, _ = parse_catalog(base_texts.get(index, ""))

    def failure(path: PurePosixPath, gap: str) -> LifecycleDiagnostic:
        document = proposed_snapshot.get(path)
        return LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=path,
            profile=document.profile_id if document is not None else "",
            expected_transition="one ADR-0038 disposition proved by its Retention Envelope",
            observed_transition="disposition is not proved",
            base_mode=mode,  # type: ignore[arg-type]
            evidence_gap=gap,
        )

    diagnostics = [failure(index, code) for code in catalog_errors]
    if any(proposed_rows.get(path) != row for path, row in base_rows.items()):
        diagnostics.append(failure(index, "an existing catalog row changed or left"))
    # Retention follows the profile, and a frozen body is immutable: once a
    # body or route record sits in Stage 98, no later change rewrites or
    # removes it, whether its catalog row or a frozen ledger proved it.
    for path in sorted(base_texts, key=PurePosixPath.as_posix):
        if path.parts[:2] != DISPOSITION_ARCHIVE_INDEX.parts[:2]:
            continue
        if proposed_texts.get(path) == base_texts[path]:
            continue
        document = base_snapshot.get(path)
        if retention_class_of(registry, path) is not None or (
            document is not None and document.profile_id in ROUTE_DISPOSITION_PROFILES
        ):
            diagnostics.append(
                failure(path, "a retained body or route record changed or left")
            )
    archive_rehomes: set[tuple[PurePosixPath, PurePosixPath]] = set()
    current_rehomes: set[tuple[PurePosixPath, PurePosixPath]] = set()
    lineages: set[ArtifactIdentityLineage] = set()
    owner: ModuleType | None = None
    # Bodies retained together may link each other, so their links are compared
    # through the whole change's moves rather than one pair at a time.
    retention_moves = {
        retention_source_path(record): record
        for record, row in proposed_rows.items()
        if base_rows.get(record) != row
        and retention_class_of(registry, record) is not None
    }
    for record, row in sorted(
        proposed_rows.items(), key=lambda item: item[0].as_posix()
    ):
        if base_rows.get(record) == row:
            continue
        envelope = row.envelope
        gaps: list[str] = []
        if record in base_blobs or record not in proposed_snapshot:
            gaps.append("catalog row does not name a record this change creates")
        named_object = _envelope_object(
            root, envelope.commit, envelope.original_path, base_commit
        )
        if named_object is None:
            gaps.append(
                "Retention Envelope names no object the comparison base reaches"
            )
        retention = retention_class_of(registry, record)
        if retention is not None:
            source = retention_source_path(record)
            before, after = base_snapshot.get(source), proposed_snapshot.get(record)
            if envelope.original_path != source:
                gaps.append("Retention Envelope does not name the mirrored source")
            if before is None or source not in base_blobs:
                gaps.append("retained source is absent from the comparison base")
            elif source in proposed_snapshot:
                gaps.append("retained source remains in the proposal")
            elif named_object is not None and named_object != base_blobs[source]:
                gaps.append("Retention Envelope object differs from the base source")
            if (
                before is not None
                and after is not None
                and (
                    before.state_issue
                    or after.state_issue
                    or before.status not in retention.admitted_states
                )
            ):
                gaps.append(f"{retention.name}/ does not admit the source state")
            if retention.name == "resolved":
                sibling = record.with_name(
                    "postmortem.md" if record.name == "incident.md" else "incident.md"
                )
                if sibling not in proposed_snapshot:
                    gaps.append(
                        "a resolved Incident and its Postmortem are retained together"
                    )
            if (
                before is not None
                and after is not None
                and (
                    before.profile_id,
                    before.status,
                    before.artifact_id,
                )
                != (after.profile_id, after.status, after.artifact_id)
            ):
                gaps.append("retained body changed its profile, state, or identity")
            if (
                not gaps
                and before is not None
                and link_resolved_text(base_texts[source], source, retention_moves)
                != link_resolved_text(proposed_texts[record], record)
            ):
                gaps.append(
                    "retained body differs from its source beyond relative link rebasing"
                )
            if not gaps:
                owner = owner or _load_canonical_markdown_module()
                if owner.validate_document_text(
                    proposed_texts[record],
                    record,
                    classify_path(registry, record),
                    "strict",
                ):
                    gaps.append("canonical retained document form")
            if not gaps and before is not None:
                archive_rehomes.add((source, record))
                if before.artifact_id is not None:
                    lineages.add(
                        ArtifactIdentityLineage(before.artifact_id, source, record)
                    )
        else:
            document = proposed_snapshot.get(record)
            if (
                document is None
                or document.profile_id not in ROUTE_DISPOSITION_PROFILES
            ):
                gaps.append("catalog row names no ADR-0038 disposition")
            else:
                metadata = frontmatter_mapping(proposed_texts[record])
                key = (
                    "moved_scope"
                    if document.profile_id == "archive/scope-migration"
                    else "retired_route"
                )
                if metadata.get(key) != envelope.original_path.as_posix():
                    gaps.append(f"Retention Envelope does not name the record's {key}")
                base_object = _envelope_object(
                    root, base_commit, envelope.original_path, base_commit
                )
                if (
                    document.profile_id == "archive/scope-migration"
                    and base_object is None
                ):
                    gaps.append("moved scope is absent from the comparison base")
                elif (
                    base_object is not None
                    and named_object is not None
                    and named_object != base_object
                ):
                    gaps.append("Retention Envelope object differs from the base route")
                if not gaps and document.profile_id == "archive/scope-migration":
                    moves, move_gaps = _scope_migration_moves(
                        registry,
                        metadata,
                        base_blobs,
                        base_snapshot,
                        proposed_snapshot,
                        base_texts,
                        proposed_texts,
                        retention_moves,
                    )
                    gaps.extend(move_gaps)
                    if not gaps:
                        current_rehomes.update(moves)
                        lineages.update(
                            ArtifactIdentityLineage(
                                base_snapshot[source].artifact_id, source, target
                            )
                            for source, target in moves
                            if base_snapshot[source].artifact_id is not None
                        )
        if gaps:
            diagnostics.append(
                failure(
                    record if record in proposed_snapshot else index, "; ".join(gaps)
                )
            )
    return (
        MigrationLifecycleEvents(
            current_rehomes=frozenset(current_rehomes),
            archive_rehomes=frozenset(archive_rehomes),
            identity_lineages=frozenset(lineages),
        ),
        tuple(diagnostics),
    )


def _migration_lifecycle_events(
    root: Path,
    registry: Registry,
    base_blobs: Mapping[PurePosixPath, str],
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    base_texts: Mapping[PurePosixPath, str],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_texts: Mapping[PurePosixPath, str],
    *,
    proposed_commit: str | None,
    mode: str,
) -> tuple[MigrationLifecycleEvents, tuple[LifecycleDiagnostic, ...]]:
    """Resolve exact creation/deletion events through the shared recovery owner."""

    records = {
        path.as_posix(): proposed_texts[path].encode("utf-8")
        for path, document in proposed_documents.items()
        if generic_migration_id(path.as_posix()) is not None
        and document.profile_id == "archive/migration"
        and document.status == "sealed"
    }
    # A declared archive rehome is reviewed on its own evidence, so it survives
    # an unrelated migration-proof outcome on every return path below.
    archive_rehomes: frozenset[tuple[PurePosixPath, PurePosixPath]] = frozenset()

    def row_identity_lineages(
        rows: Sequence[Mapping[str, object]],
    ) -> set[ArtifactIdentityLineage]:
        return {
            ArtifactIdentityLineage(
                str(row["artifact_id"]),
                PurePosixPath(str(row["legacy_path"])),
                PurePosixPath(str(row["stable_path"])),
            )
            for row in rows
            if row.get("action") == "moved"
            and isinstance(row.get("artifact_id"), str)
            and isinstance(row.get("legacy_path"), str)
            and isinstance(row.get("stable_path"), str)
        }

    identity_lineages: set[ArtifactIdentityLineage] = set()

    def preserve_document_identity(
        source: PurePosixPath, target: PurePosixPath
    ) -> None:
        before = base_documents.get(source)
        after = proposed_documents.get(target)
        if (
            before is not None
            and after is not None
            and before.artifact_id is not None
            and before.artifact_id == after.artifact_id
        ):
            identity_lineages.add(
                ArtifactIdentityLineage(before.artifact_id, source, target)
            )

    for path, document in proposed_documents.items():
        if (
            document.profile_id != "archive/migration"
            or document.status != "sealed"
            or path.as_posix() in records
        ):
            continue
        try:
            identity_lineages.update(
                row_identity_lineages(
                    parse_pinned_migration_control(
                        path.as_posix(), proposed_texts[path].encode("utf-8")
                    )
                )
            )
        except ArchiveContractError:
            continue
    if not records:
        return MigrationLifecycleEvents(
            archive_rehomes=archive_rehomes,
            identity_lineages=frozenset(identity_lineages),
        ), ()

    def failure(path: PurePosixPath, gap: str) -> LifecycleDiagnostic:
        return LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=path,
            profile=proposed_documents[path].profile_id
            if path in proposed_documents
            else "",
            expected_transition="exact proposed Migration recovery and document proof",
            observed_transition="Migration event is not proved",
            base_mode=mode,  # type: ignore[arg-type]
            evidence_gap=gap,
        )

    try:
        proof = validate_migration_records(
            root,
            records,
            proposed_commit=proposed_commit,
            registry=registry,
        )
    except ArchiveContractError as exc:
        return MigrationLifecycleEvents(archive_rehomes=archive_rehomes), (
            failure(PurePosixPath(sorted(records)[0]), exc.code),
        )

    for path, content in records.items():
        rows, _ = parse_migration_control(path, content)
        identity_lineages.update(row_identity_lineages(rows))

    removals: set[PurePosixPath] = set()
    rehomes: set[tuple[PurePosixPath, PurePosixPath]] = set()
    form_rehomes: set[tuple[PurePosixPath, PurePosixPath]] = set()
    retention_rehomes: set[tuple[PurePosixPath, PurePosixPath]] = set()
    diagnostics: list[LifecycleDiagnostic] = []
    owner = _load_canonical_markdown_module()
    for source, disposition in proof.dispositions.items():
        source_path = PurePosixPath(source)
        # Recovery can also describe earlier cutovers. Only this base's exact
        # source deletion is an event in the current comparison.
        if (
            base_blobs.get(source_path) != disposition.source_blob
            or source_path in proposed_documents
        ):
            continue
        removals.add(source_path)
        if disposition.action not in {"moved", "merged", "replaced"}:
            continue
        target = PurePosixPath(proof.targets[source])
        if target in base_blobs:
            continue
        # A form carries no lifecycle state, so the current-document rule below
        # can never reach it and its tree is not the governance tree. A `moved`
        # row is byte-identical, so a reviewed move that lands on the template
        # route the registry declares is the whole of the event.
        if disposition.action == "moved":
            try:
                assert proof.proposed_registry is not None
                moved_profile = classify_path(registry, target)
                moved_snapshot = classify_path(proof.proposed_registry, target)
            except DocumentContractError:
                diagnostics.append(failure(target, "proposed target registry route"))
                continue
            if (
                moved_profile.mode == "template"
                and moved_snapshot.profile_id == moved_profile.profile_id
            ):
                form_rehomes.add((source_path, target))
                continue
            if _is_sealed_record_path(source_path) and _is_sealed_record_path(target):
                # A reviewed record relocation. The directory holding a sealed
                # record is a claim about why its origin ended, and correcting
                # that claim moves the record without changing a byte. The
                # envelope never names the record's own path, so the row is a
                # true `moved` and byte identity is proved by the immutability
                # gate. What is left to check here is that both ends are still
                # record routes: a move that lands a record outside the record
                # namespace is not a relocation.
                if (
                    moved_profile.profile_id != ARCHIVE_PROFILE
                    or moved_snapshot.profile_id != ARCHIVE_PROFILE
                    or classify_path(registry, source_path).profile_id
                    != ARCHIVE_PROFILE
                ):
                    diagnostics.append(failure(target, "relocated record route"))
                    continue
                archive_rehomes = archive_rehomes | {(source_path, target)}
                preserve_document_identity(source_path, target)
                continue
        retention_class = _retention_rehome_target(source_path, target)
        if retention_class is not None:
            # A reviewed retention move. The row retires a terminal governed
            # document at its stage path and names the retained copy under the
            # mirrored retention tree. That copy is the same document with its
            # relative link prefixes re-based, so the row is `replaced` rather
            # than `moved` and byte identity is not the retention invariant.
            # Git still recovers the exact source bytes through this row's own
            # `source_commit` and `source_blob`.
            source_document = base_documents.get(source_path)
            retained = proposed_documents.get(target)
            if (
                source_document is None
                or retained is None
                or source_document.state_issue
                or source_document.status
                not in {
                    item.name: item.admitted_states
                    for item in registry.retention_classes
                }.get(retention_class, frozenset())
            ):
                diagnostics.append(failure(target, "retention source state"))
                continue
            try:
                source_route = classify_path(registry, source_path)
                retained_route = classify_path(registry, target)
            except DocumentContractError:
                diagnostics.append(failure(target, "proposed target registry route"))
                continue
            if source_route.profile_id != retained_route.profile_id:
                diagnostics.append(failure(target, "retained document form differs"))
                continue
            if owner.validate_document_text(
                proposed_texts[target], target, retained_route, "strict"
            ):
                diagnostics.append(failure(target, "canonical retained document form"))
                continue
            retention_rehomes.add((source_path, target))
            preserve_document_identity(source_path, target)
            continue
        if target.parts[0] != ".agents" and target not in {
            PurePosixPath(".claude/provider.md"),
            PurePosixPath(".codex/provider.md"),
        }:
            continue
        before, after = base_documents.get(source_path), proposed_documents.get(target)
        if before is None or after is None or after.state_issue:
            continue
        try:
            after_profile = classify_path(registry, target)
            assert proof.proposed_registry is not None
            snapshot_profile = classify_path(proof.proposed_registry, target)
            if (
                before.profile_id == "unclassified"
                and source_path.parts[:2] == ("docs", "00.agent-governance")
                and after_profile.lifecycle_domain is not None
            ):
                # The proof above binds this deleted source to its exact base
                # blob. Recover only unchanged semantic metadata through the
                # current target profile; never restore a retired path route.
                source_text = base_texts[source_path]
                before = replace(
                    document_from_text(registry, target, source_text), path=source_path
                )
                before_profile = after_profile
                if owner.validate_document_text(
                    source_text, target, before_profile, "strict"
                ):
                    diagnostics.append(
                        failure(target, "canonical retired source document form")
                    )
                    continue
            else:
                if before.state_issue:
                    continue
                before_profile = classify_path(registry, source_path)
        except DocumentContractError:
            diagnostics.append(failure(target, "proposed target registry route"))
            continue
        if before.state_issue:
            continue
        if (
            snapshot_profile.profile_id != after_profile.profile_id
            or snapshot_profile.mode != after_profile.mode
            or snapshot_profile.lifecycle_domain != after_profile.lifecycle_domain
        ):
            diagnostics.append(
                failure(target, "proposed target profile or lifecycle domain differs")
            )
            continue
        before_domain, after_domain = (
            before_profile.lifecycle_domain,
            after_profile.lifecycle_domain,
        )
        if (
            before_domain is None
            or before.status is None
            or before_domain.validation_class(before.status) != "current"
        ):
            continue
        if owner.validate_document_text(
            proposed_texts[target], target, after_profile, "strict"
        ) or owner.validate_document_text(
            proposed_texts[target], target, snapshot_profile, "strict"
        ):
            diagnostics.append(
                failure(target, "canonical proposed target document form")
            )
            continue
        if (
            after_domain is not None
            and after_domain.family == before_domain.family
            and before.status == after.status == "active"
            and after_domain.validation_class(after.status) == "current"
        ):
            rehomes.add((source_path, target))
    events = MigrationLifecycleEvents(
        publications=frozenset(
            PurePosixPath(path)
            for path in proof.records
            if PurePosixPath(path) not in base_blobs
        ),
        source_removals=frozenset(removals),
        current_rehomes=frozenset(rehomes),
        form_rehomes=frozenset(form_rehomes),
        archive_rehomes=archive_rehomes | frozenset(retention_rehomes),
        identity_lineages=frozenset(identity_lineages),
    )
    return events, tuple(diagnostics)


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
    text = _blob_text(root, oid, RETIRED_REGISTRY_PATH)
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
    schema_version = raw_registry.get("schema_version")
    if schema_version is None:
        schema_version = raw_registry.get("schemaVersion")
    if not isinstance(raw_profiles, list) or type(schema_version) is not int:
        raise InvocationError("comparison registry profile projection is malformed")
    current_profiles = {
        profile.profile_id: profile for profile in current_registry.profiles
    }
    aliases = {
        LEGACY_ARCHIVE_PROFILE: ARCHIVE_PROFILE,
        LEGACY_ARCHIVE_TEMPLATE_PROFILE: ARCHIVE_TEMPLATE_PROFILE,
        "sdlc/ard": "sdlc/architecture-description",  # Retired WORK-105 comparison alias.
        # Retired by the family/kind profile rename. A base-commit registry
        # still projects onto the current lifecycle contract through these.
        "sdlc/ad": "sdlc/architecture-description",
        "sdlc/adr": "sdlc/architecture-decision",
        "sdlc/requirement-package": "sdlc/requirement",
        "sdlc/guide": "operation/guide",
        "sdlc/policy": "operation/policy",
        "sdlc/runbook": "operation/runbook",
        "sdlc/incident": "operation/incident",
        "sdlc/postmortem": "operation/postmortem",
        "content/audit-reference": "reference/audit",
        "content/research-reference": "reference/research",
        "content/data-reference": "reference/data",
        "content/archive": ARCHIVE_PROFILE,
        "content/archive-migration": "archive/migration",
        "governance/reference": "governance/rule",
        "template/sdlc/ad": "common/template-sdlc-architecture-description",
        "template/sdlc/adr": "common/template-sdlc-architecture-decision",
        "common/template-sdlc-requirement-package": "common/template-sdlc-requirement",
        "template/sdlc/guide": "common/template-operation-guide",
        "template/sdlc/policy": "common/template-operation-policy",
        "template/sdlc/runbook": "common/template-operation-runbook",
        "template/sdlc/incident": "common/template-operation-incident",
        "template/sdlc/postmortem": "common/template-operation-postmortem",
        "template/content/audit-reference": "common/template-reference-audit",
        "template/content/research-reference": "common/template-reference-research",
        "template/content/data-reference": "common/template-reference-data",
        "template/content/archive": ARCHIVE_TEMPLATE_PROFILE,
        "template/content/archive-migration": "common/template-archive-migration",
        "template/governance/reference": "common/template-governance-rule",
        "template/common/local-agent-asset": "common/local-agent-asset",
        "template/sdlc/ard": "common/template-sdlc-architecture-description",  # Retired comparison alias.
        "sdlc/prd": "sdlc/requirement",  # Retired WP-004B alias.
        "sdlc/srs": "sdlc/requirement",  # Retired WP-004B alias.
        "sdlc/interface": "sdlc/requirement",  # Retired WP-004B alias.
        "sdlc/api-spec": "sdlc/requirement",  # Retired comparison alias.
        "sdlc/agent-design": "sdlc/spec",  # Retired WP-004C alias.
        "sdlc/tests": "sdlc/spec",  # Retired WP-004C alias.
        "governance/template-support": "governance/rule",  # Retired WP-004C alias.
        "template/sdlc/api-spec": "common/template-sdlc-requirement",  # Retired alias.
        "template/sdlc/prd": "common/template-sdlc-requirement",  # Retired WP-004C alias.
        "template/sdlc/srs": "common/template-sdlc-requirement",  # Retired WP-004C alias.
        "template/sdlc/interface": "common/template-sdlc-requirement",  # Retired WP-004C alias.
        "template/sdlc/agent-design": "common/template-sdlc-spec",  # Retired WP-004C alias.
        "template/sdlc/tests": "common/template-sdlc-spec",  # Retired WP-004C alias.
        "template/governance/template-support": "common/template-governance-rule",  # Retired WP-004C alias.
    }
    projected: list[DocumentProfile] = []
    for raw_profile in raw_profiles:
        if not isinstance(raw_profile, dict):
            raise InvocationError("comparison registry contains a non-object profile")
        profile_id = raw_profile.get("id")
        if not isinstance(profile_id, str):
            raise InvocationError("comparison registry profile shape is malformed")
        source = current_profiles.get(aliases.get(profile_id, profile_id))
        if source is None:
            raise InvocationError(
                "comparison registry profile has no current lifecycle projection"
            )

        raw_lifecycle = raw_profile.get("lifecycle")
        raw_mode = raw_profile.get("mode")
        if schema_version == 9:
            path_pattern = raw_profile.get("path_pattern")
            raw_routes = (
                [{"kind": "regex", "value": path_pattern}]
                if isinstance(path_pattern, str)
                else None
            )
            raw_status_domain = (
                raw_lifecycle.get("status_domain")
                if isinstance(raw_lifecycle, dict)
                else list(source.status_domain)
            )
        else:
            raw_routes = raw_profile.get("routes")
            if raw_routes is None and isinstance(raw_profile.get("pathPattern"), str):
                raw_routes = [{"kind": "regex", "value": raw_profile["pathPattern"]}]
            raw_status_domain = raw_profile.get("statusDomain")
            if raw_status_domain is None and isinstance(raw_lifecycle, dict):
                raw_status_domain = raw_lifecycle.get("statusDomain")

        if (
            not isinstance(raw_routes, list)
            or not isinstance(raw_status_domain, list)
            or not all(isinstance(state, str) for state in raw_status_domain)
            or not isinstance(raw_mode, str)
        ):
            raise InvocationError("comparison registry profile shape is malformed")
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
    *,
    historical: bool = False,
) -> tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]]:
    documents: dict[PurePosixPath, LifecycleDocument] = {}
    texts: dict[PurePosixPath, str] = {}
    for path in sorted(blobs, key=PurePosixPath.as_posix):
        text = _blob_text(root, blobs[path], path)
        assert text is not None
        texts[path] = text
        try:
            documents[path] = document_from_text(
                registry,
                path,
                text,
                retired_types=RETIRED_DOCUMENT_TYPES if historical else None,
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


def _work105_predecessor_unresolved_links(
    *,
    path: PurePosixPath,
    base_document: LifecycleDocument | None,
    proposed_document: LifecycleDocument,
    base_text: str,
    proposed_text: str,
    relationship_links: tuple[PurePosixPath, ...],
    unresolved_links: tuple[PurePosixPath, ...],
    body_table_links: tuple[PurePosixPath, ...],
) -> tuple[PurePosixPath, ...]:
    """Admit only WORK-105's blob-pinned reciprocal predecessor evidence."""

    exact_document = LifecycleDocument(
        WORK105_ADR0023_PATH, "sdlc/architecture-decision", "accepted"
    )
    exact = (
        path == WORK105_ADR0023_PATH
        and base_document == exact_document
        and proposed_document == exact_document
        and hashlib.sha256(base_text.encode("utf-8")).hexdigest()
        == WORK105_ADR0023_BASE_SHA256
        and hashlib.sha256(proposed_text.encode("utf-8")).hexdigest()
        == WORK105_ADR0023_PROPOSED_SHA256
        and proposed_text.count(WORK105_ADR0023_RECIPROCAL_ROW) == 1
        and WORK105_ADR0024_PATH in relationship_links
        and WORK105_ADR0024_PATH in body_table_links
        and unresolved_links == (WORK105_LEGACY_AD0011_PATH,)
    )
    return () if exact else unresolved_links


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
            path, proposed_texts[path], profile, snapshot_profiles
        )
        unresolved_links = _work105_predecessor_unresolved_links(
            path=path,
            base_document=base_documents.get(path),
            proposed_document=document,
            base_text=base_texts.get(path, ""),
            proposed_text=proposed_texts[path],
            relationship_links=rendered.relationship_links,
            unresolved_links=rendered.unresolved_relationship_links,
            body_table_links=rendered.body_table_links,
        )
        views[path] = LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=unresolved_links,
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
        *,
        historical: bool = False,
    ) -> LifecycleDocument | None:
        text = _blob_text(root, oid, path)
        if text is None:
            return None
        try:
            return document_from_text(
                registry,
                path,
                text,
                retired_types=RETIRED_DOCUMENT_TYPES if historical else None,
            )
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
            base = load(
                base_registry,
                change.old_path,
                base_oid(change.old_path),
                historical=True,
            )
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
            base = load(
                base_registry, change.path, base_oid(change.path), historical=True
            )
            if base is None:
                raise InvocationError(f"deleted path lacks base blob: {change.path}")
            base_documents[change.path] = base
        else:
            base = load(
                base_registry, change.path, base_oid(change.path), historical=True
            )
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


def _history_rename_or_copy_into_path(
    root: Path,
    parent: str,
    commit: str,
    path: PurePosixPath,
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
            _decode_path(records[cursor])
            destination = _decode_path(records[cursor + 1])
            cursor += 2
            if destination == path:
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
    snapshots: OrderedDict[
        str,
        tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]],
    ] = field(default_factory=OrderedDict)
    snapshot_sizes: dict[str, int] = field(default_factory=dict)
    cached_snapshot_bytes: int = 0
    snapshot_work_bytes: int = 0
    evidence: OrderedDict[tuple[str, str], LifecycleEvidenceContext] = field(
        default_factory=OrderedDict
    )

    def _snapshot(
        self, commit: str
    ) -> tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]]:
        cached = self.snapshots.get(commit)
        if cached is not None:
            self.snapshots.move_to_end(commit)
            return cached
        blobs = _tree_blob_map(self.root, commit)
        size = _snapshot_blob_size(self.root, blobs)
        if size > CUMULATIVE_HISTORY_MAX_SNAPSHOT_BYTES or (
            self.snapshot_work_bytes + size > CUMULATIVE_HISTORY_MAX_SNAPSHOT_WORK_BYTES
        ):
            raise _CumulativeHistoryBudgetExceeded
        while self.snapshots and (
            len(self.snapshots) >= CUMULATIVE_HISTORY_CACHE_MAX_SNAPSHOTS
            or self.cached_snapshot_bytes + size > CUMULATIVE_HISTORY_MAX_SNAPSHOT_BYTES
        ):
            evicted, _ = self.snapshots.popitem(last=False)
            self.cached_snapshot_bytes -= self.snapshot_sizes.pop(evicted)
            for key in tuple(self.evidence):
                if evicted in key:
                    del self.evidence[key]
        if self.cached_snapshot_bytes + size > CUMULATIVE_HISTORY_MAX_SNAPSHOT_BYTES:
            raise _CumulativeHistoryBudgetExceeded
        snapshot = _snapshot_projection(
            self.root, self.registry, blobs, historical=True
        )
        self.snapshot_work_bytes += size
        self.snapshots[commit] = snapshot
        self.snapshot_sizes[commit] = size
        self.cached_snapshot_bytes += size
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
                self.registry,
                base_snapshot,
                proposed_snapshot,
                base_texts,
                proposed_texts,
            )
        return self.evidence[key]


def _history_document(
    root: Path,
    registry: Registry,
    path: PurePosixPath,
    oid: str,
) -> LifecycleDocument:
    text = _blob_text(root, oid, path)
    assert text is not None
    document = document_from_text(registry, path, text)
    profile = classify_path(registry, path)
    if (
        document.state_issue is not None
        or document.profile_id != profile.profile_id
        or profile.lifecycle_domain is None
    ):
        raise InvocationError("cumulative lifecycle path has no stable profile")
    return document


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
    return compare_lifecycle(
        registry,
        base_documents,
        {path: after},
        base_mode="explicit-ref",
        evidence_context=cache.evidence_context(parent, commit),
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
) -> bool:
    """Prove a path's complete legal lifecycle on one closed first-parent path."""

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
            if _history_rename_or_copy_into_path(root, parent, commit, path) or (
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
                return False
            if not appeared:
                if prior_blob is not None:
                    return False
                current = _history_document(root, registry, path, current_blob)
                profile = classify_path(registry, path)
                domain = profile.lifecycle_domain
                assert domain is not None
                inbound = {target for _, target in domain.transitions}
                if (
                    current.status is None
                    or current.status
                    not in {state for state, _ in domain.states if state not in inbound}
                    or _history_event_diagnostics(
                        root,
                        registry,
                        path,
                        parent,
                        commit,
                        None,
                        current,
                        history_cache,
                    )
                ):
                    return False
                appeared = True
                prior_document = current
            elif current_blob != prior_blob:
                current = _history_document(root, registry, path, current_blob)
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
) -> tuple[LifecycleDiagnostic, ...]:
    """Remove only history-proved create diagnostics in committed comparisons."""

    if mode not in {"ci", "explicit-ref"} or proposed_commit is None:
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
        history = _first_parent_history(root, base_commit, proposed_commit)
    except (InvocationError, UnicodeDecodeError, ValueError):
        return tuple(diagnostics)
    if len(candidate_paths) * len(history) > CUMULATIVE_HISTORY_MAX_CANDIDATE_EVENTS:
        return tuple(diagnostics)
    cache = _CumulativeHistoryCache(root, registry)
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
                base_commit,
                proposed_commit,
                proposed_blobs[diagnostic.path],
                commits=history,
                cache=cache,
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

    # Stage 99 is terminal: compare both snapshots with the current root
    # profile authority. Historical route and flat-registry projections are
    # intentionally not lifecycle inputs.
    base_classification_registry = registry
    proposed_classification_registry = registry
    migration_immutability = _migration_immutability_diagnostics(
        root,
        registry,
        base_blobs,
        proposed_blobs,
        mode=mode,
    )
    if migration_immutability:
        return migration_immutability
    work054_wp002_consumed_paths = frozenset()
    work054_wp003_consumed_paths = finite_work054_wp003_agent_governance_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )
    wp004c_mig0004_consumed_paths = _wp004c_mig0004_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )
    archive_rehome_consumed_paths = sealed_record_relocation_paths(
        root=root, base_blobs=base_blobs, proposed_blobs=proposed_blobs
    )

    immutability_diagnostics = _archive_immutability_diagnostics(
        root,
        base_classification_registry,
        base_blobs,
        proposed_blobs,
        mode=mode,
        admitted_rehome_paths=archive_rehome_consumed_paths,
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
    work054_wp004a_consumed_paths: frozenset[PurePosixPath] = frozenset()
    base_snapshot, base_texts = _snapshot_projection(
        root, base_classification_registry, base_blobs, historical=True
    )
    proposed_snapshot, proposed_texts = _snapshot_projection(
        root, proposed_classification_registry, proposed_blobs
    )
    migration_events, migration_diagnostics = _migration_lifecycle_events(
        root,
        registry,
        base_blobs,
        base_snapshot,
        base_texts,
        proposed_snapshot,
        proposed_texts,
        proposed_commit=proposed_commit,
        mode=mode,
    )
    disposition_events, disposition_diagnostics = _disposition_lifecycle_events(
        root,
        registry,
        base_commit,
        base_blobs,
        base_snapshot,
        base_texts,
        proposed_snapshot,
        proposed_texts,
        mode=mode,
    )
    migration_events = replace(
        migration_events,
        current_rehomes=migration_events.current_rehomes
        | disposition_events.current_rehomes,
        archive_rehomes=migration_events.archive_rehomes
        | disposition_events.archive_rehomes,
        identity_lineages=migration_events.identity_lineages
        | disposition_events.identity_lineages,
    )
    migration_diagnostics = migration_diagnostics + disposition_diagnostics
    evidence_context = evidence_context_factory(
        proposed_classification_registry,
        base_snapshot,
        proposed_snapshot,
        base_texts,
        proposed_texts,
    )
    work105_consumed_paths: frozenset[PurePosixPath] = frozenset()
    archive_consumed_paths: frozenset[PurePosixPath] = frozenset()
    legacy_consumed_paths = (
        work054_wp002_consumed_paths
        | work054_wp003_consumed_paths
        | work054_wp004a_consumed_paths
        | work105_consumed_paths
        | archive_rehome_consumed_paths
        | archive_consumed_paths
        | wp004c_mig0004_consumed_paths
    )

    def consume_finite_cutover(
        diagnostics: Sequence[LifecycleDiagnostic],
    ) -> tuple[LifecycleDiagnostic, ...]:
        return tuple(
            diagnostic
            for diagnostic in diagnostics
            if diagnostic.path not in legacy_consumed_paths
        )

    diagnostics = consume_finite_cutover(
        compare_lifecycle(
            proposed_classification_registry,
            base_documents,
            proposed_documents,
            renames=renames,
            base_mode=mode,  # type: ignore[arg-type]
            evidence_context=evidence_context,
            migration_events=migration_events,
        )
    )
    return migration_diagnostics + _admit_cumulative_create_diagnostics(
        diagnostics,
        root=root,
        registry=proposed_classification_registry,
        mode=mode,
        base_commit=base_commit,
        proposed_commit=proposed_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
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
    if args.mode in {"strict", "staged", "snapshot"} and any(
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
        choices=("strict", "staged", "ci", "explicit-ref", "snapshot"),
        default="strict",
    )
    parser.add_argument("--from-ref")
    parser.add_argument("--base-ref")
    parser.add_argument("--to-ref")
    parser.add_argument("--include-path", action="append", default=[])
    return parser


def _execute(root: Path, args: argparse.Namespace) -> int:
    _verify_repository_root(root)
    if args.mode == "staged":
        assert_staged_authority_matches_worktree(root, CURRENT_REGISTRY_PATH)
    registry = load_registry(root)
    include_paths = _normalize_include_paths(registry, args.include_path)
    if args.mode == "snapshot":
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
        if args.mode in {"strict", "staged", "ci", "explicit-ref", "snapshot"}:
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
