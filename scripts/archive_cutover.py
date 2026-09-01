#!/usr/bin/env python3
"""Validate the complete ARWB-003 production archive cutover.

Diagnostics contain only stable rule identifiers and canonical repository
paths. Archive payloads, secret matches, values, and line content are never
printed or retained in the report.
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Mapping, Sequence

import yaml

if __package__:
    from scripts.archive_cutover_manifest import (
        ARCHIVE_PROFILE,
        ARCHIVE_TEMPLATE,
        CUTOVER_BASE_COMMIT,
        EXPECTED_ARCHIVE_PATHS,
    )
    from scripts.archive_recovery import (
        ArchiveContractError,
        WORK107_LEGACY_INDEX_OVERVIEW,
        WORK107_MIGRATION_PATH,
        WORK107_STABLE_INDEX_OVERVIEW,
        build_work107_migration_rows,
        parse_archive_envelope,
        render_work107_migration_document,
        render_work107_stable_envelope,
        validate_work107_migration_rows,
    )
    from scripts.document_contracts import (
        REGISTRY_PATH,
        DocumentContractError,
        Registry,
        classify_path,
        load_internal_payload,
        load_registry,
    )
    from scripts.document_lifecycle import document_from_text
    from scripts.archive_validation import (
        CurrentMarkdownDocument,
        MIGRATION_DOCUMENT_MAX_BYTES,
        generic_migration_id,
        is_sealed_migration,
        parse_migration_control,
        parse_pinned_migration_control,
        read_staged_blob_bounded,
        read_worktree_regular_bounded,
        validate_current_archive_authority,
        validate_repository_archive,
    )
else:
    from archive_cutover_manifest import (  # type: ignore[no-redef]
        ARCHIVE_PROFILE,
        ARCHIVE_TEMPLATE,
        CUTOVER_BASE_COMMIT,
        EXPECTED_ARCHIVE_PATHS,
    )
    from archive_recovery import (  # type: ignore[no-redef]
        ArchiveContractError,
        WORK107_LEGACY_INDEX_OVERVIEW,
        WORK107_MIGRATION_PATH,
        WORK107_STABLE_INDEX_OVERVIEW,
        build_work107_migration_rows,
        parse_archive_envelope,
        render_work107_migration_document,
        render_work107_stable_envelope,
        validate_work107_migration_rows,
    )
    from document_contracts import (  # type: ignore[no-redef]
        REGISTRY_PATH,
        DocumentContractError,
        Registry,
        classify_path,
        load_internal_payload,
        load_registry,
    )
    from document_lifecycle import document_from_text  # type: ignore[no-redef]
    from archive_validation import (  # type: ignore[no-redef]
        CurrentMarkdownDocument,
        MIGRATION_DOCUMENT_MAX_BYTES,
        generic_migration_id,
        is_sealed_migration,
        parse_migration_control,
        parse_pinned_migration_control,
        read_staged_blob_bounded,
        read_worktree_regular_bounded,
        validate_current_archive_authority,
        validate_repository_archive,
    )


_ARCHIVE_PREFIX = "docs/98.archive/"
WORK054_MIGRATION_PATH = (
    "docs/98.archive/migrations/0002-sdlc-document-and-governance-consolidation.md"
)
WORK054_MIGRATION_PATHS = (
    WORK054_MIGRATION_PATH,
    "docs/98.archive/migrations/"
    "0003-agent-governance-control-plane-consolidation.md",
    "docs/98.archive/migrations/0004-document-authority-convergence.md",
)
WORK054_LEDGER_FIELDS = (
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
FIRST_SOURCE_COMMIT = (
    "5e0221525450dbdacb585e6c98ade3f060ddc827"  # pragma: allowlist secret
)
SECOND_SOURCE_COMMIT = (
    "82f0e1922d9748a88b1487a32a59629ba523f408"  # pragma: allowlist secret
)
ARCHIVE_TEMPLATE_PROFILE = "template/content/archive"
ARCHIVE_INDEX = "docs/98.archive/README.md"
CURRENT_REPLACEMENT_STATUSES = frozenset({"active", "accepted", "done"})
SECRET_DETECTED_EXIT = 17
SECRET_TIMEOUT_SECONDS = 10
MAX_REPLACEMENT_BLOB_BYTES = 2_000_000
GITLEAKS_EXECUTABLE_ENV = "HY_HOME_K8S_GITLEAKS_EXECUTABLE"
_RETIRED_WORD = "tomb" + "stone"
_RETIRED_PROFILE_TOKEN = "archive-" + _RETIRED_WORD
_FULL_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")

SECOND_SOURCE_ORIGINAL_PATHS = frozenset(
    {
        "docs/03.specs/007-docs-governance-consistency/spec.md",
        "docs/04.execution/plans/2026-05-28-docs-governance-consistency.md",
        "docs/04.execution/tasks/2026-05-28-docs-governance-consistency.md",
        "docs/05.operations/guides/0004-headlamp-auth-oidc-guide.md",
        "docs/05.operations/runbooks/0005-headlamp-keycloak-runbook.md",
    }
)


@dataclass(frozen=True)
class CutoverDiagnostic:
    """One stable, redacted production diagnostic."""

    code: str
    path: str


@dataclass(frozen=True)
class CutoverReport:
    """Aggregate atomic-cutover result."""

    diagnostics: tuple[CutoverDiagnostic, ...]
    record_count: int
    historical_link_count: int
    secret_clean_count: int

    @property
    def valid(self) -> bool:
        return not self.diagnostics


@dataclass(frozen=True)
class ArchiveIndexRow:
    """One structured archive-index row keyed by canonical archive path."""

    archive_path: str
    original_path: str
    original_type: str
    source_commit: str
    source_blob: str
    content_sha256: str
    historical_links: int
    replacement: str | None
    reason: str


@dataclass(frozen=True)
class Work054MigrationProjection:
    """Exact historical-to-current aliases admitted by MIG-0002."""

    current_by_legacy: Mapping[str, str]
    action_counts: tuple[tuple[str, int], ...]


_WORK105_CURRENT_AD = (
    "docs/02.architecture/descriptions/0007-current-local-gitops-platform.md"
)
_WORK105_LEGACY_REPLACEMENT = (
    "docs/02.architecture/requirements/0007-current-local-gitops-platform.md"
)
_WORK105_REPLACEMENT_PROOFS = MappingProxyType(
    {
        "docs/98.archive/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md": ArchiveIndexRow(
            archive_path="docs/98.archive/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md",
            original_path="docs/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md",
            original_type="ard",
            source_commit=FIRST_SOURCE_COMMIT,
            source_blob="9001b10b9657396fe85d6d7b98112dcc6b310e4f",
            content_sha256="cbf08950c2da952a6ca7feaa122085700c5984c5b177a97d90277f3fcca4b44b",
            historical_links=7,
            replacement=_WORK105_LEGACY_REPLACEMENT,
            reason="superseded",
        ),
        "docs/98.archive/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md": ArchiveIndexRow(
            archive_path="docs/98.archive/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md",
            original_path="docs/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md",
            original_type="ard",
            source_commit=FIRST_SOURCE_COMMIT,
            source_blob="37857c69bd334b3acc59705a701233a303c2bcb2",
            content_sha256="4a0902cee5048f2192e16c3688e9bf1e992e60fde4fe3865abb1fcd45767f59f",
            historical_links=4,
            replacement=_WORK105_LEGACY_REPLACEMENT,
            reason="superseded",
        ),
        "docs/98.archive/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md": ArchiveIndexRow(
            archive_path="docs/98.archive/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md",
            original_path="docs/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md",
            original_type="ard",
            source_commit=FIRST_SOURCE_COMMIT,
            source_blob="4d38947d216e84dfc9430f4f632966292b602017",
            content_sha256="dfc0cd13ede805828a19909b2e525648c892dea9fc25d505d7becf8c27acd6b2",
            historical_links=9,
            replacement=_WORK105_LEGACY_REPLACEMENT,
            reason="superseded",
        ),
    }
)


def _diagnostic(code: str, path: str) -> CutoverDiagnostic:
    return CutoverDiagnostic(code=code, path=path)


def _source_commit(original_path: str) -> str:
    return (
        SECOND_SOURCE_COMMIT
        if original_path in SECOND_SOURCE_ORIGINAL_PATHS
        else FIRST_SOURCE_COMMIT
    )


def _safe_git_environment() -> dict[str, str]:
    """Return the recovery-grade Git environment for every cutover lookup."""

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


def _git_paths(root: Path) -> tuple[str, ...]:
    try:
        completed = subprocess.run(
            [
                "git",
                "--no-replace-objects",
                "--literal-pathspecs",
                "-C",
                str(root),
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "docs",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=SECRET_TIMEOUT_SECONDS,
            env=_safe_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        raise RuntimeError("tracked document inventory is unavailable") from None
    if completed.returncode != 0 or not completed.stdout.endswith(b"\0"):
        raise RuntimeError("tracked document inventory is unavailable")
    try:
        return tuple(
            sorted(
                record.decode("utf-8")
                for record in completed.stdout.split(b"\0")[:-1]
                if record
            )
        )
    except UnicodeDecodeError as exc:
        raise RuntimeError("tracked document inventory is malformed") from exc


def _tracked_regular_blobs(root: Path) -> Mapping[str, str]:
    """Return stage-zero regular authority paths and index blob identities.

    The corpus is `docs/`, plus the shared `.agents` control plane: a migration
    may retire a document into that authority, and a terminal target has to be
    verifiable wherever it now lives.
    """

    try:
        completed = subprocess.run(
            [
                "git",
                "--no-replace-objects",
                "--literal-pathspecs",
                "-C",
                str(root),
                "ls-files",
                "--stage",
                "-z",
                "--",
                "docs",
                ".agents",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=SECRET_TIMEOUT_SECONDS,
            env=_safe_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        raise RuntimeError(
            "tracked regular document inventory is unavailable"
        ) from None
    if completed.returncode != 0 or not completed.stdout.endswith(b"\0"):
        raise RuntimeError("tracked regular document inventory is unavailable")
    blobs: dict[str, str] = {}
    try:
        for record in completed.stdout.split(b"\0")[:-1]:
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            mode, object_id, stage = header.split(b" ", 2)
            path = raw_path.decode("utf-8")
            pure_path = PurePosixPath(path)
            if (
                not path.startswith(("docs/", ".agents/"))
                or "\\" in path
                or any(
                    ord(character) < 32 or ord(character) == 127 for character in path
                )
                or pure_path.is_absolute()
                or any(part in {".", ".."} for part in pure_path.parts)
                or pure_path.as_posix() != path
                or _FULL_OBJECT_ID.fullmatch(object_id.decode("ascii", errors="strict"))
                is None
            ):
                raise ValueError
            if mode in {b"100644", b"100755"} and stage == b"0":
                if path in blobs:
                    raise ValueError
                blobs[path] = object_id.decode("ascii")
    except (UnicodeDecodeError, ValueError) as exc:
        raise RuntimeError("tracked regular document inventory is malformed") from exc
    return MappingProxyType(blobs)


def _canonical_document_path(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    path = PurePosixPath(value)
    if (
        not value.startswith("docs/")
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
        or path.is_absolute()
        or any(part in {".", ".."} for part in path.parts)
        or path.as_posix() != value
    ):
        return None
    return value


def _resolve_migration_graph(
    edges: Mapping[str, str],
    current_profiles: Mapping[str, str],
) -> dict[str, str]:
    """Resolve a closed migration graph to one selected current owner per source."""

    resolved: dict[str, str] = {}
    for source in sorted(edges):
        current = source
        visited: set[str] = set()
        while current in edges:
            if current in visited:
                raise RuntimeError("migration graph cycle")
            visited.add(current)
            target = edges[current]
            if target == current:
                break
            current = target
        profile = current_profiles.get(current)
        if (
            not isinstance(profile, str)
            or not profile
            or profile in {ARCHIVE_PROFILE, "content/archive-migration"}
        ):
            raise RuntimeError("migration graph target is not current")
        resolved[source] = current
    return resolved


def _later_ledger_edges(
    root: Path,
    tracked_regular_blobs: Mapping[str, str],
    failure: str,
) -> tuple[dict[str, str], set[str]]:
    """Return replacements and deletions declared after the pinned ledgers."""

    edges: dict[str, str] = {}
    retired: set[str] = set()
    for path in sorted(tracked_regular_blobs):
        if generic_migration_id(path) is None:
            continue
        try:
            staged = read_staged_blob_bounded(
                root, path, max_bytes=MIGRATION_DOCUMENT_MAX_BYTES
            )
            if not is_sealed_migration(staged):
                continue
            parsed = parse_migration_control(path, staged)
        except (ArchiveContractError, OSError, ValueError):
            raise RuntimeError(failure) from None
        for row in parsed[0] if isinstance(parsed, tuple) and parsed else ():
            if not isinstance(row, Mapping):
                continue
            action = row.get("action")
            legacy = row.get("legacy_path")
            target = (
                row.get("stable_path") if action == "moved" else row.get("replacement")
            )
            if not isinstance(legacy, str) or not legacy.startswith("docs/"):
                continue
            if action == "deleted" and target is None:
                retired.add(legacy)
                continue
            if not isinstance(target, str) or legacy == target:
                continue
            edges[legacy] = target
    return edges, retired


def _work054_migration_projection(
    root: Path,
    tracked_regular_blobs: Mapping[str, str],
    registry: Registry,
) -> Work054MigrationProjection:
    """Compose exact MIG-0002..0004 rows to selected regular current targets."""

    failure = "WORK-054 migration ledger is unavailable"
    rows_by_path: dict[str, tuple[dict[str, object], ...]] = {}
    try:
        for migration_path in WORK054_MIGRATION_PATHS:
            if migration_path not in tracked_regular_blobs:
                raise ValueError
            staged = read_staged_blob_bounded(
                root,
                migration_path,
                max_bytes=MIGRATION_DOCUMENT_MAX_BYTES,
            )
            content = read_worktree_regular_bounded(
                root,
                migration_path,
                max_bytes=MIGRATION_DOCUMENT_MAX_BYTES,
            )
            if staged != content:
                raise ValueError
            rows_by_path[migration_path] = parse_pinned_migration_control(
                migration_path,
                staged,
            )
    except (ArchiveContractError, OSError, RuntimeError, ValueError):
        raise RuntimeError(failure) from None

    edges: dict[str, str] = {}
    dropped: set[str] = set()
    action_counts: dict[str, int] = {}
    later_edges, later_retired = _later_ledger_edges(
        root, tracked_regular_blobs, failure
    )
    for migration_path in WORK054_MIGRATION_PATHS:
        previous_legacy = ""
        for row in rows_by_path[migration_path]:
            if type(row) is not dict or tuple(row) != WORK054_LEDGER_FIELDS:
                raise RuntimeError(failure)
            legacy = _canonical_document_path(row.get("legacy_path"))
            action = row.get("action")
            target_value = (
                row.get("stable_path") if action == "moved" else row.get("replacement")
            )
            target = _canonical_document_path(target_value)
            if (
                legacy is None
                or legacy <= previous_legacy
                or legacy in edges
                or legacy in dropped
                or action not in {"merged", "moved", "replaced"}
                or target is None
                or (action == "moved" and row.get("replacement") is not None)
                or (action != "moved" and row.get("stable_path") is not None)
                or _FULL_OBJECT_ID.fullmatch(str(row.get("source_blob", ""))) is None
                or re.fullmatch(r"[0-9a-f]{64}", str(row.get("content_sha256", "")))
                is None
                or not isinstance(row.get("reason"), str)
                or not row["reason"].strip()
                or (
                    legacy != target
                    and (legacy in tracked_regular_blobs or _regular_file(root, legacy))
                )
            ):
                raise RuntimeError(f"{failure}: row {legacy or migration_path}")
            previous_legacy = legacy
            action_counts[action] = action_counts.get(action, 0) + 1
            # A later ledger may retire this target in turn, and the pinned rows
            # cannot name a successor that did not exist when they were sealed.
            terminal = later_edges.get(target, target)
            if terminal in later_retired:
                # The later ledger deleted the endpoint rather than moving it,
                # so this row composes no current owner and resolves through
                # the Archive index instead.
                dropped.add(legacy)
                continue
            edges[legacy] = terminal

    terminal_paths = {
        target
        for target in edges.values()
        if target not in edges or edges[target] == target
    }
    current_profiles: dict[str, str] = {}
    try:
        for target in terminal_paths:
            if target not in tracked_regular_blobs or not _regular_file(root, target):
                raise RuntimeError(f"{failure}: target {target}")
            if target.endswith(".md"):
                profile = classify_path(registry, PurePosixPath(target))
                if profile.mode not in {"authored", "frontmatter-free", "template"}:
                    raise RuntimeError(f"{failure}: profile {target}")
                current_profiles[target] = profile.profile_id
            else:
                current_profiles[target] = "terminal/native-contract"
        current_by_legacy = _resolve_migration_graph(edges, current_profiles)
    except DocumentContractError as exc:
        raise RuntimeError(f"{failure}: profile selection") from exc
    return Work054MigrationProjection(
        current_by_legacy=MappingProxyType(current_by_legacy),
        action_counts=tuple(sorted(action_counts.items())),
    )


def _index_blob_bytes(root: Path, object_id: str) -> bytes:
    """Read one bounded exact index blob without worktree substitution."""

    if _FULL_OBJECT_ID.fullmatch(object_id) is None:
        raise RuntimeError("replacement target blob is unavailable")

    def run_cat_file(mode: str) -> bytes:
        try:
            completed = subprocess.run(
                [
                    "git",
                    "--no-replace-objects",
                    "--literal-pathspecs",
                    "-C",
                    str(root),
                    "cat-file",
                    mode,
                    object_id,
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=SECRET_TIMEOUT_SECONDS,
                env=_safe_git_environment(),
            )
        except (OSError, subprocess.TimeoutExpired):
            raise RuntimeError("replacement target blob is unavailable") from None
        if (
            not isinstance(completed, subprocess.CompletedProcess)
            or completed.returncode != 0
            or not isinstance(completed.stdout, bytes)
        ):
            raise RuntimeError("replacement target blob is unavailable")
        return completed.stdout

    raw_size = run_cat_file("-s")
    if re.fullmatch(rb"(?:0|[1-9][0-9]*)\n", raw_size) is None:
        raise RuntimeError("replacement target blob is unavailable")
    size = int(raw_size)
    if size > MAX_REPLACEMENT_BLOB_BYTES:
        raise RuntimeError("replacement target blob is unavailable")
    content = run_cat_file("blob")
    if len(content) != size:
        raise RuntimeError("replacement target blob is unavailable")
    return content


def _regular_file(root: Path, raw_path: str) -> bool:
    try:
        mode = (root / raw_path).lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode)


def _frontmatter_identity(text: str, path: str) -> tuple[str, str]:
    if path.endswith("/README.md") or path == "docs/README.md":
        return "readme/repository", "active"
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return "content/reference", "active"
    raw = text.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError:
        return "content/reference", "active"
    if not isinstance(loaded, dict):
        return "content/reference", "active"
    profile = loaded.get("type")
    status = loaded.get("status")
    return (
        profile if isinstance(profile, str) else "content/reference",
        status if isinstance(status, str) else "active",
    )


def _secret_classifier(
    root: Path,
    archive_path: str,
    payload: bytes,
) -> CutoverDiagnostic | None:
    executable = None
    hint = os.environ.get(GITLEAKS_EXECUTABLE_ENV)
    if hint is not None:
        try:
            metadata = os.lstat(hint)
        except OSError:
            metadata = None
        candidate = Path(hint)
        if (
            candidate.is_absolute()
            and candidate.name == "gitleaks"
            and metadata is not None
            and stat.S_ISREG(metadata.st_mode)
            and metadata.st_mode & 0o111
        ):
            executable = hint
    else:
        executable = shutil.which("gitleaks")
    if executable is None:
        return _diagnostic("ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE", archive_path)
    try:
        completed = subprocess.run(
            [
                executable,
                "detect",
                "--pipe",
                "--config",
                str(root / ".gitleaks.toml"),
                "--redact=100",
                "--no-banner",
                "--no-color",
                "--log-level",
                "error",
                "--timeout",
                str(SECRET_TIMEOUT_SECONDS),
                "--exit-code",
                str(SECRET_DETECTED_EXIT),
            ],
            input=payload,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=SECRET_TIMEOUT_SECONDS * 2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return _diagnostic("ARCHIVE-SECRET-CLASSIFIER-ERROR", archive_path)
    if completed.returncode == SECRET_DETECTED_EXIT:
        return _diagnostic("ARCHIVE-SECRET-DETECTED", archive_path)
    if completed.returncode != 0:
        return _diagnostic("ARCHIVE-SECRET-CLASSIFIER-ERROR", archive_path)
    return None


_INDEX_COLUMNS = (
    "Archive Record",
    "Original Path",
    "Original Type",
    "Source Commit",
    "Source Blob",
    "Payload SHA-256",
    "Historical Links",
    "Current Replacement",
    "Reason",
)
_INDEX_HEADER = "| " + " | ".join(_INDEX_COLUMNS) + " |"
_INDEX_SEPARATOR = "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |"
_MARKDOWN_LINK = re.compile(r"\[`(?P<label>[^`]+)`\]\((?P<target>[^)]+)\)")
_CODE_CELL = re.compile(r"`(?P<value>[^`]+)`")
_INDEX_MANIFEST = re.compile(
    r"<!-- archive-manifest:v1 records=(?P<records>\d+) "
    r"historical-links=(?P<links>\d+) -->"
)


def _index_target(target: str) -> str | None:
    if not target.startswith("./"):
        return None
    normalized = posixpath.normpath(posixpath.join("docs/98.archive", target))
    if not normalized.startswith("docs/98.archive/"):
        return None
    return normalized


def _replacement_target(label: str, target: str) -> str | None:
    if not target.startswith(("../", "./")):
        return None
    normalized = posixpath.normpath(posixpath.join("docs/98.archive", target))
    if normalized != label or not normalized.startswith("docs/"):
        return None
    return normalized


def _replacement_target_diagnostic(
    root: Path,
    registry: Registry,
    target: str,
    tracked_regular_blobs: Mapping[str, str],
) -> str | None:
    """Validate one index-owned current replacement without trusting neighbors."""

    path = PurePosixPath(target)
    if (
        not target.startswith("docs/")
        or "\\" in target
        or any(ord(character) < 32 or ord(character) == 127 for character in target)
        or path.is_absolute()
        or any(part in {".", ".."} for part in path.parts)
        or path.as_posix() != target
    ):
        return "ARCHIVE-REPLACEMENT-UNSELECTED"
    if path.is_relative_to(PurePosixPath("docs/98.archive")):
        return "ARCHIVE-REPLACEMENT-ARCHIVE"
    object_id = tracked_regular_blobs.get(target)
    if object_id is None:
        return "ARCHIVE-REPLACEMENT-MISSING"
    try:
        profile = classify_path(registry, path)
    except DocumentContractError:
        return "ARCHIVE-REPLACEMENT-UNSELECTED"
    if profile.mode != "authored" or profile.profile_id == ARCHIVE_PROFILE:
        return "ARCHIVE-REPLACEMENT-PROFILE"
    try:
        text = _index_blob_bytes(root, object_id).decode("utf-8", errors="strict")
        document = document_from_text(registry, path, text)
    except (DocumentContractError, RuntimeError, UnicodeDecodeError, ValueError):
        return "ARCHIVE-REPLACEMENT-NONCURRENT"
    if (
        document.state_issue is not None
        or document.profile_id != profile.profile_id
        or document.status not in CURRENT_REPLACEMENT_STATUSES
        or document.status not in profile.status_domain
    ):
        return "ARCHIVE-REPLACEMENT-NONCURRENT"
    return None


def _work105_replacement_target(
    archive_path: str,
    index_row: ArchiveIndexRow,
    archive_metadata: Mapping[str, object],
) -> str | None:
    """Resolve the three immutable ARD rows through the exact WORK-105 AD move."""

    expected = _WORK105_REPLACEMENT_PROOFS.get(archive_path)
    if expected is None or index_row != expected:
        return index_row.replacement
    metadata_proof = (
        ("original_path", expected.original_path),
        ("original_type", expected.original_type),
        ("source_commit", expected.source_commit),
        ("source_blob", expected.source_blob),
        ("content_sha256", expected.content_sha256),
        ("replacement", expected.replacement),
        ("archive_reason", expected.reason),
    )
    if any(archive_metadata.get(key) != value for key, value in metadata_proof):
        return index_row.replacement
    return _WORK105_CURRENT_AD


def _parse_index_row(line: str) -> ArchiveIndexRow | None:
    cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
    if len(cells) != len(_INDEX_COLUMNS):
        return None
    record_match = _MARKDOWN_LINK.fullmatch(cells[0])
    code_matches = tuple(_CODE_CELL.fullmatch(cells[index]) for index in range(1, 6))
    reason_match = _CODE_CELL.fullmatch(cells[8])
    if (
        record_match is None
        or any(match is None for match in code_matches)
        or reason_match is None
        or not cells[6].isdigit()
    ):
        return None
    archive_path = _index_target(record_match.group("target"))
    reason = reason_match.group("value")
    if cells[7] == "`null`":
        replacement = None
    else:
        replacement_match = _MARKDOWN_LINK.fullmatch(cells[7])
        if replacement_match is None or reason not in {
            "superseded",
            "consolidated",
            "duplicate",
        }:
            return None
        replacement = _replacement_target(
            replacement_match.group("label"), replacement_match.group("target")
        )
    if archive_path is None or record_match.group("label") != archive_path.removeprefix(
        "docs/98.archive/"
    ):
        return None
    values = tuple(match.group("value") for match in code_matches if match is not None)
    return ArchiveIndexRow(
        archive_path=archive_path,
        original_path=values[0],
        original_type=values[1],
        source_commit=values[2],
        source_blob=values[3],
        content_sha256=values[4],
        historical_links=int(cells[6]),
        replacement=replacement,
        reason=reason,
    )


def _parse_archive_index(
    index_text: str,
) -> tuple[dict[str, ArchiveIndexRow], bool]:
    """Parse the one exact manifest table and return rows plus structure failure."""

    lines = index_text.splitlines()
    header_offsets = [
        offset for offset, line in enumerate(lines) if line == _INDEX_HEADER
    ]
    if len(header_offsets) != 1:
        return {}, True
    header_offset = header_offsets[0]
    if header_offset + 1 >= len(lines) or lines[header_offset + 1] != _INDEX_SEPARATOR:
        return {}, True
    raw_rows: list[str] = []
    for line in lines[header_offset + 2 :]:
        if not line.startswith("|"):
            break
        raw_rows.append(line)
    manifest_end = header_offset + 2 + len(raw_rows)
    rows: dict[str, ArchiveIndexRow] = {}
    structure_failure = not raw_rows or any(
        line.startswith("|")
        for offset, line in enumerate(lines)
        if not header_offset <= offset < manifest_end
    )
    for raw_row in raw_rows:
        row = _parse_index_row(raw_row)
        if row is None or row.archive_path in rows:
            structure_failure = True
            continue
        rows[row.archive_path] = row
    return rows, structure_failure


@lru_cache(maxsize=4)
def _finite_cutover_base_diagnostics(root: Path) -> tuple[CutoverDiagnostic, ...]:
    """Prove the exact 31-record legacy conversion without restoring its route."""

    diagnostics: list[CutoverDiagnostic] = []
    git_environment = _safe_git_environment()
    for archive_path in EXPECTED_ARCHIVE_PATHS:
        try:
            completed = subprocess.run(
                [
                    "git",
                    "--no-replace-objects",
                    "--literal-pathspecs",
                    "-C",
                    str(root),
                    "cat-file",
                    "blob",
                    f"{CUTOVER_BASE_COMMIT}:{archive_path}",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=SECRET_TIMEOUT_SECONDS,
                env=git_environment,
            )
            if completed.returncode != 0:
                raise ValueError
            text = completed.stdout.decode("utf-8")
            if not text.startswith("---\n") or "\n---\n" not in text[4:]:
                raise ValueError
            metadata = yaml.safe_load(text.split("\n---\n", 1)[0][4:])
        except (
            UnicodeDecodeError,
            ValueError,
            yaml.YAMLError,
            OSError,
            subprocess.TimeoutExpired,
        ):
            diagnostics.append(_diagnostic("ARCHIVE-FINITE-ADMISSION", archive_path))
            continue
        if (
            not isinstance(metadata, dict)
            or metadata.get("type") != f"content/{_RETIRED_PROFILE_TOKEN}"
            or metadata.get("status") != "archived"
        ):
            diagnostics.append(_diagnostic("ARCHIVE-FINITE-ADMISSION", archive_path))
    return tuple(diagnostics)


def validate_repository_cutover(repository_root: str | Path) -> CutoverReport:
    """Validate one complete production snapshot and reject every partial state."""

    try:
        root = Path(repository_root).resolve(strict=True)
        if not root.is_dir():
            raise OSError
    except (OSError, RuntimeError, TypeError):
        return CutoverReport(
            diagnostics=(
                _diagnostic("ARCHIVE-CUTOVER-INCOMPLETE", "<repository>"),
                _diagnostic("ARCHIVE-ROOT-UNAVAILABLE", "<repository>"),
            ),
            record_count=0,
            historical_link_count=0,
            secret_clean_count=0,
        )
    diagnostics: list[CutoverDiagnostic] = list(_finite_cutover_base_diagnostics(root))
    registry_path = root / REGISTRY_PATH
    try:
        loaded_registry = load_internal_payload(root)
    except (DocumentContractError, OSError, UnicodeDecodeError, ValueError):
        loaded_registry = {}
    registry: Mapping[str, object] = (
        loaded_registry if isinstance(loaded_registry, dict) else {}
    )
    try:
        typed_registry = load_registry(root)
    except (DocumentContractError, OSError, UnicodeDecodeError, ValueError):
        typed_registry = None
    generic_report = validate_repository_archive(root, registry)
    diagnostics.extend(
        _diagnostic(item.code, item.path) for item in generic_report.diagnostics
    )
    try:
        tracked_regular_blobs = _tracked_regular_blobs(root)
    except RuntimeError:
        tracked_regular_blobs = MappingProxyType({})
        diagnostics.append(_diagnostic("ARCHIVE-CURRENT-INVENTORY", "docs"))
    try:
        if typed_registry is None:
            raise RuntimeError
        work054_projection = _work054_migration_projection(
            root,
            tracked_regular_blobs,
            typed_registry,
        )
    except RuntimeError:
        work054_projection = Work054MigrationProjection(
            current_by_legacy=MappingProxyType({}),
            action_counts=(),
        )
        diagnostics.append(
            _diagnostic("ARCHIVE-MIGRATION-LEDGER", WORK054_MIGRATION_PATH)
        )
    try:
        work107_rows = build_work107_migration_rows(root)
        work107_by_stable = {str(row["stable_path"]): row for row in work107_rows}
        work107_legacy_to_stable = {
            str(row["legacy_path"]): str(row["stable_path"]) for row in work107_rows
        }
    except (ArchiveContractError, OSError, RuntimeError, TypeError, ValueError):
        work107_by_stable = {}
        work107_legacy_to_stable = {}
        diagnostics.append(
            _diagnostic("ARCHIVE-MIGRATION-LEDGER", WORK107_MIGRATION_PATH)
        )
    legacy_base_paths = frozenset(EXPECTED_ARCHIVE_PATHS)
    base_paths = frozenset(
        work107_legacy_to_stable.get(path, path) for path in legacy_base_paths
    )
    record_link_counts = dict(generic_report.record_link_counts)
    expected_paths = frozenset(record_link_counts)
    expected_records = generic_report.record_count
    expected_historical_links = generic_report.historical_link_count
    present_paths = frozenset(
        path for path in expected_paths if _regular_file(root, path)
    )
    if present_paths != expected_paths:
        diagnostics.append(_diagnostic("ARCHIVE-CORPUS-INCOMPLETE", ARCHIVE_INDEX))

    reviewed_manifest_rows = {
        row.target: row for row in generic_report.reviewed_manifest_records
    }
    payloads: list[bytes] = []
    metadata_rows: list[tuple[str, dict[str, object], int]] = []
    for archive_path in sorted(expected_paths):
        if archive_path not in present_paths:
            continue
        try:
            content = (root / archive_path).read_bytes()
            parsed = parse_archive_envelope(content)
        except (OSError, ArchiveContractError):
            diagnostics.append(_diagnostic("ARCHIVE-ENVELOPE-INVALID", archive_path))
            continue
        original_path = parsed.metadata.get("original_path")
        stable_row = work107_by_stable.get(archive_path)
        legacy_archive_path = (
            str(stable_row["legacy_path"]) if stable_row is not None else archive_path
        )
        expected_source_commit = (
            stable_row.get("source_commit")
            if stable_row is not None
            else (
                _source_commit(str(original_path))
                if archive_path in base_paths
                else (
                    reviewed_manifest_rows[archive_path].source_commit
                    if archive_path in reviewed_manifest_rows
                    else None
                )
            )
        )
        if (
            not isinstance(original_path, str)
            or parsed.metadata.get("source_commit") != expected_source_commit
        ):
            diagnostics.append(_diagnostic("ARCHIVE-SOURCE-OWNERSHIP", archive_path))
            continue
        payloads.append(parsed.payload)
        metadata_rows.append(
            (
                archive_path,
                dict(parsed.metadata),
                record_link_counts.get(archive_path, -1),
            )
        )

    secret_clean_count = 0
    if payloads:
        secret_diagnostic = _secret_classifier(
            root,
            ARCHIVE_INDEX,
            b"\n\n".join(payloads),
        )
        if secret_diagnostic is not None:
            diagnostics.append(secret_diagnostic)
        else:
            secret_clean_count = len(payloads)
    if (
        len(metadata_rows) != expected_records
        or frozenset(record_link_counts) != expected_paths
        or generic_report.historical_link_count != expected_historical_links
        or sum(record_link_counts.values()) != expected_historical_links
    ):
        diagnostics.append(_diagnostic("ARCHIVE-EVIDENCE-COUNT", ARCHIVE_INDEX))

    original_paths = [row[1].get("original_path") for row in metadata_rows]
    if len(original_paths) != len(set(original_paths)):
        diagnostics.append(
            _diagnostic("ARCHIVE-ORIGINAL-OWNER-DUPLICATE", ARCHIVE_INDEX)
        )
    archived_original_paths = frozenset(
        str(metadata.get("original_path"))
        for _archive_path, metadata, _link_count in metadata_rows
        if isinstance(metadata.get("original_path"), str)
    ) | frozenset(
        "docs/" + str(row["legacy_path"])[len(_ARCHIVE_PREFIX) :]
        for row in work107_rows
        if str(row.get("legacy_path", "")).startswith(_ARCHIVE_PREFIX)
    )
    for archive_path, metadata, _link_count in metadata_rows:
        original_path = metadata.get("original_path")
        replacement = metadata.get("replacement")
        if isinstance(original_path, str) and _regular_file(root, original_path):
            diagnostics.append(
                _diagnostic("ARCHIVE-ORIGINAL-STILL-CURRENT", archive_path)
            )
        reason = metadata.get("archive_reason")
        if reason == "completed-lineage":
            stable_row = work107_by_stable.get(archive_path)
            legacy_archive_path = (
                str(stable_row["legacy_path"])
                if stable_row is not None
                else archive_path
            )
            migration = None
            closure_owner = (
                migration.get("_currentClosureOwner") if migration is not None else None
            )
            current_closure_owner = work054_projection.current_by_legacy.get(
                str(closure_owner),
                str(closure_owner),
            )
            if (
                replacement is not None
                or migration is None
                or not _regular_file(root, current_closure_owner)
                or migration.get("_archiveNavigationBoundary")
                != f"{ARCHIVE_INDEX}#document-index"
            ):
                diagnostics.append(
                    _diagnostic("ARCHIVE-REPLACEMENT-MISSING", archive_path)
                )
        elif reason in {"superseded", "consolidated", "duplicate"} and not isinstance(
            replacement, str
        ):
            diagnostics.append(_diagnostic("ARCHIVE-REPLACEMENT-MISSING", archive_path))
    profiles = registry.get("profiles", ())
    profile_ids = [
        profile.get("id") for profile in profiles if isinstance(profile, dict)
    ]
    if (
        registry.get("schemaVersion") != 8
        or profile_ids.count(ARCHIVE_PROFILE) != 1
        or profile_ids.count(ARCHIVE_TEMPLATE_PROFILE) != 1
        or _RETIRED_PROFILE_TOKEN in json.dumps(registry, ensure_ascii=False).lower()
        or not _regular_file(root, ARCHIVE_TEMPLATE)
        or (
            root
            / "docs/99.templates/templates/common"
            / (_RETIRED_PROFILE_TOKEN + ".template.md")
        ).exists()
    ):
        diagnostics.append(
            _diagnostic(
                "ARCHIVE-AUTHORITY-INCOMPLETE",
                registry_path.relative_to(root).as_posix(),
            )
        )
    if typed_registry is None:
        diagnostics.append(
            _diagnostic(
                "ARCHIVE-AUTHORITY-INCOMPLETE",
                registry_path.relative_to(root).as_posix(),
            )
        )
    try:
        index_text = (root / ARCHIVE_INDEX).read_text(encoding="utf-8")
    except OSError:
        index_text = ""
    index_rows, index_structure_failure = _parse_archive_index(index_text)
    index_links = sum(row.historical_links for row in index_rows.values())
    markers = tuple(_INDEX_MANIFEST.finditer(index_text))
    marker_valid = (
        len(markers) == 1
        and int(markers[0].group("records")) == len(index_rows)
        and int(markers[0].group("links")) == index_links
        and len(index_rows) == expected_records
        and index_links == expected_historical_links
    )
    if not marker_valid:
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-MANIFEST", ARCHIVE_INDEX))
    if index_structure_failure or frozenset(index_rows) != expected_paths:
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX))
    archive_metadata = {
        archive_path: metadata for archive_path, metadata, _link_count in metadata_rows
    }
    if typed_registry is not None:
        for archive_path, index_row in index_rows.items():
            if index_row.replacement is None:
                continue
            stable_row = work107_by_stable.get(archive_path)
            legacy_archive_path = (
                str(stable_row["legacy_path"])
                if stable_row is not None
                else archive_path
            )
            legacy_index_row = (
                replace(index_row, archive_path=legacy_archive_path)
                if legacy_archive_path != archive_path
                else index_row
            )
            replacement_target = _work105_replacement_target(
                legacy_archive_path,
                legacy_index_row,
                archive_metadata.get(archive_path, {}),
            )
            if replacement_target is None:
                continue
            replacement_target = work054_projection.current_by_legacy.get(
                replacement_target,
                replacement_target,
            )
            replacement_failure = _replacement_target_diagnostic(
                root,
                typed_registry,
                replacement_target,
                tracked_regular_blobs,
            )
            if replacement_failure is not None:
                diagnostics.append(_diagnostic(replacement_failure, archive_path))
    for archive_path, metadata, link_count in metadata_rows:
        index_row = index_rows.get(archive_path)
        expected_row = ArchiveIndexRow(
            archive_path=archive_path,
            original_path=str(metadata.get("original_path")),
            original_type=str(metadata.get("original_type")),
            source_commit=str(metadata.get("source_commit")),
            source_blob=str(metadata.get("source_blob")),
            content_sha256=str(metadata.get("content_sha256")),
            historical_links=link_count,
            # ArchiveEnvelope.v1 replacement is immutable archive-time provenance.
            # The index alone owns later current-replacement evolution.
            replacement=index_row.replacement if index_row is not None else None,
            reason=str(metadata.get("archive_reason")),
        )
        if index_row != expected_row:
            diagnostics.append(_diagnostic("ARCHIVE-INDEX-MEMBER", archive_path))
        if (
            index_row is not None
            and index_row.replacement is None
            and metadata.get("archive_reason")
            in {"superseded", "consolidated", "duplicate"}
            and metadata.get("replacement") not in archived_original_paths
        ):
            diagnostics.append(_diagnostic("ARCHIVE-REPLACEMENT-MISSING", archive_path))

    current_documents: list[CurrentMarkdownDocument] = []
    try:
        current_paths = _git_paths(root)
    except RuntimeError:
        current_paths = ()
        diagnostics.append(_diagnostic("ARCHIVE-CURRENT-INVENTORY", "docs"))
    for raw_path in current_paths:
        if (
            not raw_path.endswith(".md")
            or raw_path == ARCHIVE_INDEX
            or raw_path == WORK107_MIGRATION_PATH
            or raw_path in expected_paths
            or raw_path.startswith("docs/99.templates/templates/")
            or not _regular_file(root, raw_path)
        ):
            continue
        try:
            markdown = (root / raw_path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            diagnostics.append(_diagnostic("ARCHIVE-CURRENT-READ", raw_path))
            continue
        profile, _status = _frontmatter_identity(markdown, raw_path)
        current_documents.append(
            CurrentMarkdownDocument(
                path=raw_path,
                markdown=markdown,
                profile=profile,
                status="active",
            )
        )
    current_report = validate_current_archive_authority(
        tuple(current_documents),
        individual_archive_paths=expected_paths,
    )
    diagnostics.extend(
        _diagnostic(item.code, item.path) for item in current_report.diagnostics
    )

    unique = tuple(
        sorted(
            set(diagnostics),
            key=lambda item: (item.path, item.code),
        )
    )
    if unique and not any(item.code == "ARCHIVE-CUTOVER-INCOMPLETE" for item in unique):
        unique = (
            _diagnostic("ARCHIVE-CUTOVER-INCOMPLETE", "<repository>"),
            *unique,
        )
    return CutoverReport(
        diagnostics=unique,
        record_count=len(metadata_rows),
        historical_link_count=generic_report.historical_link_count,
        secret_clean_count=secret_clean_count,
    )


def _work107_stable_index(
    legacy_index: str,
    rows: Sequence[Mapping[str, object]],
) -> str:
    """Apply the reviewed stable overview and 93 inventory link projection."""

    result = legacy_index
    if result.count(WORK107_LEGACY_INDEX_OVERVIEW) != 1:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-INDEX", "legacy index overview differs"
        )
    result = result.replace(
        WORK107_LEGACY_INDEX_OVERVIEW,
        WORK107_STABLE_INDEX_OVERVIEW,
        1,
    )
    for row in rows:
        legacy = str(row["legacy_path"]).removeprefix("docs/98.archive/")
        stable = str(row["stable_path"]).removeprefix("docs/98.archive/")
        source = f"[`{legacy}`](./{legacy})"
        target = f"[`{stable}`](./{stable})"
        if result.count(source) != 1:
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-INDEX", "legacy index member differs"
            )
        result = result.replace(source, target, 1)
    return result


def apply_work107_stable_rehome(repository_root: str | Path) -> int:
    """Apply the reviewed stable rehome with rollback on any partial write."""

    root = Path(repository_root).resolve(strict=True)
    rows = validate_work107_migration_rows(root, build_work107_migration_rows(root))
    index_path = root / ARCHIVE_INDEX
    migration_path = root / WORK107_MIGRATION_PATH
    original_index = index_path.read_bytes()
    legacy_bytes: dict[Path, bytes] = {}
    stable_bytes: dict[Path, bytes] = {}
    for row in rows:
        legacy = root / str(row["legacy_path"])
        stable = root / str(row["stable_path"])
        if not legacy.is_file() or legacy.is_symlink() or stable.exists():
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-PRECONDITION", "legacy/stable path state differs"
            )
        content = legacy.read_bytes()
        recovered = parse_archive_envelope(content)
        if (
            recovered.metadata.get("source_commit") != row["source_commit"]
            or recovered.metadata.get("source_blob") != row["source_blob"]
            or recovered.metadata.get("content_sha256") != row["content_sha256"]
        ):
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-PROVENANCE", "legacy envelope metadata differs"
            )
        legacy_bytes[legacy] = content
        stable_bytes[stable] = render_work107_stable_envelope(content, row)
    if migration_path.exists():
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PRECONDITION", "migration control record already exists"
        )
    desired_index = _work107_stable_index(original_index.decode("utf-8"), rows).encode(
        "utf-8"
    )
    desired_migration = render_work107_migration_document(rows)

    created: list[Path] = []
    removed: list[Path] = []
    try:
        for path, content in stable_bytes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            created.append(path)
        migration_path.parent.mkdir(parents=True, exist_ok=True)
        migration_path.write_bytes(desired_migration)
        created.append(migration_path)
        index_path.write_bytes(desired_index)
        for path in legacy_bytes:
            path.unlink()
            removed.append(path)
        for directory in sorted(
            {
                parent
                for path in legacy_bytes
                for parent in path.parents
                if parent != root and parent.is_relative_to(root / "docs/98.archive")
            },
            key=lambda item: len(item.parts),
            reverse=True,
        ):
            try:
                directory.rmdir()
            except OSError:
                pass
    except Exception:
        index_path.write_bytes(original_index)
        for path, content in legacy_bytes.items():
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise
    return len(rows)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--apply-work107", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.apply_work107:
        try:
            count = apply_work107_stable_rehome(args.root)
        except (ArchiveContractError, OSError, RuntimeError, ValueError) as exc:
            code = (
                exc.code
                if isinstance(exc, ArchiveContractError)
                else "ARCHIVE-MIGRATION-APPLY"
            )
            print(f"FAIL {code} path=docs/98.archive")
            return 1
        print(f"PASS archive stable rehome records={count}")
        return 0
    report = validate_repository_cutover(args.root)
    if report.valid:
        print(
            "PASS archive cutover "
            f"records={report.record_count} "
            f"historical_links={report.historical_link_count} "
            f"secret_clean={report.secret_clean_count}"
        )
        return 0
    for diagnostic in report.diagnostics:
        print(f"FAIL {diagnostic.code} path={diagnostic.path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
