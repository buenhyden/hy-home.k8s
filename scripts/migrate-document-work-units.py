#!/usr/bin/env python3
"""Build, validate, and transactionally apply the reviewed migration manifest.

The Git-common-directory lock is the mandatory coordination boundary for
supported repository and migration writers; it is not a security sandbox.
Non-cooperative replacement of public source, target, or ancestor paths remains
in scope and fails closed through anchored descriptors, no-clobber operations,
and recovery preservation. A hostile same-EUID process that enumerates and
mutates random mode-0700 private quarantine entries is outside the supported
threat model. Private rename/identity/unlink cleanup is an internal integrity
check only and does not claim hostile-process isolation.

Platforms without the required dir_fd, O_NOFOLLOW, follow_symlinks, and
pass_fds-compatible POSIX behavior are rejected before the migration lock or
any filesystem mutation is created.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping, Sequence

import yaml

try:
    from archive_recovery import (
        ArchiveContractError,
        parse_archive_envelope,
        recover_git_blob,
        render_archive_envelope,
    )
except ModuleNotFoundError:  # Imported as a repository-root test module.
    from scripts.archive_recovery import (
        ArchiveContractError,
        parse_archive_envelope,
        recover_git_blob,
        render_archive_envelope,
    )


OID = re.compile(r"[0-9a-f]{40}\Z")
DATE_SLUG = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-(?P<slug>[A-Za-z0-9][A-Za-z0-9._-]*)\.md\Z")
ENTRY_KEYS = {"source", "target", "workUnit", "disposition", "sourceBlob", "reviewed"}
TOP_KEYS = {"state", "sourceCommit", "entries"}
EXPECTED_SOURCE_COMMIT = "713dff1fc3de58a2d1682970a7f24faa39c14263"  # pragma: allowlist secret
PHASE_DISPOSITION = {"archive": "archive-unique", "move": "move-current"}
GIT_TIMEOUT_SECONDS = 20
SECRET_TIMEOUT_SECONDS = 10
SECRET_DETECTED_EXIT = 17
CONTROL_SURFACE_LIMIT = 8 * 1024 * 1024
GITLEAKS_HINT = "HY_HOME_K8S_GITLEAKS_EXECUTABLE"
GITLEAKS_CANDIDATES = tuple(
    Path(directory) / "gitleaks"
    for directory in ("/usr/local/bin", "/usr/bin", "/bin")
)
ARCHIVED_ON = "2026-08-09"
ARCHIVE_INDEX_HANDOFF = "docs/98.archive/README.md#document-index"
MANIFEST_PATH = PurePosixPath("scripts/document-taxonomy-migration.json")
GITLEAKS_CONFIG_PATH = PurePosixPath(".gitleaks.toml")
SOURCE_PATH = re.compile(r"docs/04\.execution/(?:plans|tasks)/[^/]+\.md\Z")
MOVE_TARGET = re.compile(
    r"docs/03\.specs/(?P<unit>[0-9]{3})-[^/]+/(?P<name>plan|tasks)\.md\Z"
)
_REQUIRED_DIR_FD_FUNCTIONS = (
    os.open,
    os.stat,
    os.mkdir,
    os.rename,
    os.link,
    os.unlink,
    os.rmdir,
)
_TRANSACTION_PLATFORM_SUPPORTED = (
    os.name == "posix"
    and hasattr(os, "O_NOFOLLOW")
    and all(function in os.supports_dir_fd for function in _REQUIRED_DIR_FD_FUNCTIONS)
    and os.stat in os.supports_follow_symlinks
)


class MigrationAbort(RuntimeError):
    pass


class _DuplicateYAMLKey(ValueError):
    pass


class _UniqueKeySafeLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeySafeLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise _DuplicateYAMLKey from exc
        if duplicate:
            raise _DuplicateYAMLKey
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


@dataclass(frozen=True)
class MigrationPlan:
    source_count: int
    move_count: int
    archive_count: int


@dataclass(frozen=True)
class ManifestDocument:
    source_commit: str
    entries: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class _PreparedOperation:
    source: PurePosixPath
    target: PurePosixPath
    source_blob: str
    source_bytes: bytes
    output: bytes
    source_mode: int
    target_mode: int


@dataclass(frozen=True)
class _FileIdentity:
    path: Path
    device: int
    inode: int
    mode: int


@dataclass(frozen=True)
class _ControlSurface:
    path: PurePosixPath
    contents: bytes = field(repr=False)
    index_blob: str


@dataclass(frozen=True)
class _ConfigHandle:
    descriptor: int
    device: int
    inode: int
    mode: int


@dataclass
class _DirectoryAnchor:
    parent_fd: int
    descriptor: int
    name: str
    relative: PurePosixPath
    identity: _FileIdentity
    created: bool = False
    active: bool = True


@dataclass
class _CreatedDirectory:
    parent_fd: int
    name: str
    relative: PurePosixPath
    descriptor: int | None = None
    identity: _FileIdentity | None = None
    active: bool = True


@dataclass
class _TransactionOperation:
    prepared: _PreparedOperation
    source_parent_fd: int
    source_fd: int
    source_identity: _FileIdentity
    source_anchor: str
    target_parent_fd: int
    stage_fd: int
    stage_name: str
    target_fd: int | None = None
    target_identity: _FileIdentity | None = None
    target_installed: bool = False
    removed_name: str | None = None
    removed_identity: _FileIdentity | None = None


@dataclass
class _Transaction:
    root: Path
    root_fd: int
    root_identity: _FileIdentity
    quarantine_fd: int
    quarantine_name: str
    quarantine_identity: _FileIdentity
    operations: list[_TransactionOperation] = field(default_factory=list)
    directory_anchors: list[_DirectoryAnchor] = field(default_factory=list)
    created_directories: list[_CreatedDirectory] = field(default_factory=list)
    recovery_required: bool = False
    replacement_detected: bool = False
    commit_started: bool = False


@dataclass(frozen=True)
class _RepositoryLockHandle:
    parent_fd: int
    descriptor: int
    name: str
    identity: _FileIdentity


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
    root: Path, *args: str, literal_paths: bool = True
) -> subprocess.CompletedProcess[str]:
    global_options = ["--no-replace-objects"]
    if literal_paths:
        global_options.append("--literal-pathspecs")
    try:
        return subprocess.run(
            [
                "git",
                *global_options,
                "-C",
                str(root),
                *args,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=GIT_TIMEOUT_SECONDS,
            env=_safe_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MigrationAbort("MIGRATION-GIT-ERROR") from exc


def _canonical_root(root: Path) -> Path:
    try:
        if stat.S_ISLNK(root.lstat().st_mode):
            raise MigrationAbort("MIGRATION-ROOT")
        candidate = root.resolve(strict=True)
        metadata = candidate.lstat()
    except (OSError, RuntimeError) as exc:
        raise MigrationAbort("MIGRATION-ROOT") from exc
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        raise MigrationAbort("MIGRATION-ROOT")
    result = _git_process(candidate, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise MigrationAbort("MIGRATION-ROOT")
    try:
        reported = Path(result.stdout.strip()).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise MigrationAbort("MIGRATION-ROOT") from exc
    if reported != candidate:
        raise MigrationAbort("MIGRATION-ROOT")
    return candidate


def _git(root: Path, *args: str) -> str:
    root = _canonical_root(root)
    result = _git_process(root, *args)
    if result.returncode:
        raise MigrationAbort(f"MIGRATION-GIT:{args[0]}")
    return result.stdout.strip()


def _safe_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value or value.startswith(("/", "./")) or "\\" in value:
        raise MigrationAbort("MIGRATION-PATH")
    path = PurePosixPath(value)
    if ".." in path.parts:
        raise MigrationAbort("MIGRATION-PATH")
    return path


def _parse_manifest_bytes(contents: bytes) -> ManifestDocument:
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise MigrationAbort("MIGRATION-JSON-DUPLICATE")
            out[key] = value
        return out

    try:
        data = json.loads(contents.decode("utf-8"), object_pairs_hook=unique)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MigrationAbort("MIGRATION-JSON") from exc
    if not isinstance(data, Mapping) or set(data) != TOP_KEYS or data.get("state") != "transition":
        raise MigrationAbort("MIGRATION-SCHEMA")
    commit = data.get("sourceCommit")
    if not isinstance(commit, str) or OID.fullmatch(commit) is None:
        raise MigrationAbort("MIGRATION-SOURCE-COMMIT")
    rows = data.get("entries")
    if not isinstance(rows, list) or not rows:
        raise MigrationAbort("MIGRATION-ENTRIES")
    immutable = []
    for row in rows:
        if not isinstance(row, Mapping) or set(row) != ENTRY_KEYS:
            raise MigrationAbort("MIGRATION-ENTRY-SCHEMA")
        source = _safe_path(row.get("source"))
        target = _safe_path(row.get("target"))
        if (
            row.get("reviewed") is not True
            or row.get("disposition") not in PHASE_DISPOSITION.values()
            or not isinstance(row.get("workUnit"), str)
            or not row["workUnit"]
            or not isinstance(row.get("sourceBlob"), str)
            or OID.fullmatch(row["sourceBlob"]) is None
            or not source.as_posix().startswith("docs/04.execution/")
            or not target.as_posix().startswith(("docs/03.specs/", "docs/98.archive/"))
        ):
            raise MigrationAbort("MIGRATION-ENTRY-SCHEMA")
        immutable.append(MappingProxyType(dict(row)))
    return ManifestDocument(commit, tuple(immutable))


def load_manifest_document(path: Path) -> ManifestDocument:
    try:
        contents = path.read_bytes()
    except OSError as exc:
        raise MigrationAbort("MIGRATION-JSON") from exc
    return _parse_manifest_bytes(contents)


def load_manifest(path: Path) -> tuple[Mapping[str, Any], ...]:
    """Load the reviewed entries into an immutable ordered representation."""
    return load_manifest_document(path).entries


def validate_counts(*, move_count: int, archive_count: int, source_count: int) -> None:
    if (move_count, archive_count, source_count) != (82, 50, 132):
        raise MigrationAbort("MIGRATION-COUNTS:expected=82/50/132")


def validate_work_unit_paths(work_units: Mapping[str, set[str]]) -> tuple[str, ...]:
    diagnostics: list[str] = []
    for unit, names in sorted(work_units.items()):
        if "spec.md" not in names:
            diagnostics.append(f"WORK-UNIT-MISSING-SPEC:{unit}")
        if "plan.md" not in names:
            diagnostics.append(f"WORK-UNIT-MISSING-PLAN:{unit}")
        if "tasks.md" not in names:
            diagnostics.append(f"WORK-UNIT-MISSING-TASK:{unit}")
        unexpected = names - {"spec.md", "plan.md", "tasks.md"}
        if unexpected:
            diagnostics.append(f"WORK-UNIT-UNEXPECTED:{unit}")
    return tuple(sorted(diagnostics))


def validate_route_paths(paths: Sequence[str], route_state: str) -> tuple[str, ...]:
    if route_state not in {"legacy", "transition", "terminal"}:
        return ("ROUTE-STATE-UNKNOWN",)
    if route_state == "terminal" and any(path.startswith("docs/04.execution/") for path in paths):
        return ("ROUTE-TERMINAL-STAGE04",)
    return ()


def _ancestor_is_file(root: Path, path: PurePosixPath) -> bool:
    current = root
    for part in path.parts[:-1]:
        current = current / part
        if current.is_file() or current.is_symlink():
            return True
    return False


def _path_mode(path: Path) -> int | None:
    try:
        return path.lstat().st_mode
    except FileNotFoundError:
        return None
    except OSError:
        return -1


def _archive_envelope_is_exact(
    root: Path,
    row: Mapping[str, Any],
    target: PurePosixPath,
    expected_commit: str | None,
) -> bool:
    try:
        archive_bytes = (root / target).read_bytes()
        parsed = parse_archive_envelope(archive_bytes)
        metadata_commit = parsed.metadata.get("source_commit")
        if not isinstance(metadata_commit, str):
            return False
        if expected_commit is not None and metadata_commit != expected_commit:
            return False
        recovered = recover_git_blob(root, str(row["source"]), metadata_commit)
        if (
            recovered.source_blob != row.get("sourceBlob")
            or recovered.proposed_archive_path != target.as_posix()
        ):
            return False
        parse_archive_envelope(archive_bytes, expected=recovered)
    except (ArchiveContractError, OSError, KeyError, TypeError, ValueError):
        return False
    return True


def _entry_diagnostics(root: Path, entries: Sequence[Mapping[str, Any]], commit: str | None) -> tuple[str, ...]:
    diagnostics: list[str] = []
    sources: set[str] = set()
    targets: set[str] = set()
    work_units: dict[str, set[str]] = {}
    for index, row in enumerate(entries):
        if not isinstance(row, Mapping) or set(row) != ENTRY_KEYS or row.get("reviewed") is not True:
            diagnostics.append(f"MIGRATION-ENTRY-SCHEMA:{index}")
            continue
        try:
            source = _safe_path(row.get("source"))
            target = _safe_path(row.get("target"))
        except MigrationAbort:
            diagnostics.append(f"MIGRATION-PATH:{index}")
            continue
        source_name = source.as_posix()
        target_name = target.as_posix()
        if source_name in sources:
            diagnostics.append(f"MIGRATION-DUPLICATE-SOURCE:{source_name}")
        if target_name in targets:
            diagnostics.append(f"MIGRATION-DUPLICATE-TARGET:{target_name}")
        sources.add(source_name)
        targets.add(target_name)
        disposition = row.get("disposition")
        if disposition not in PHASE_DISPOSITION.values():
            diagnostics.append(f"MIGRATION-DISPOSITION:{source_name}")
            continue
        expected_blob = row.get("sourceBlob")
        if not isinstance(expected_blob, str) or OID.fullmatch(expected_blob) is None:
            diagnostics.append(f"MIGRATION-SOURCE-BLOB:{source_name}")
            continue
        if commit is not None:
            try:
                pinned_blob = _git(root, "rev-parse", f"{commit}:{source_name}")
            except MigrationAbort:
                diagnostics.append(f"MIGRATION-SOURCE-BLOB:{source_name}")
            else:
                if pinned_blob != expected_blob:
                    diagnostics.append(f"MIGRATION-SOURCE-BLOB:{source_name}")
        source_mode = _path_mode(root / source)
        target_mode = _path_mode(root / target)
        source_exists = source_mode is not None
        target_exists = target_mode is not None
        if source_exists and target_exists:
            diagnostics.append(f"MIGRATION-DUPLICATE-ACTIVE-OWNER:{source_name}")
        elif not source_exists and not target_exists:
            diagnostics.append(f"MIGRATION-MISSING-ENDPOINT:{source_name}")
        else:
            active_path = source if source_exists else target
            active_mode = source_mode if source_exists else target_mode
            if (
                active_mode is None
                or active_mode == -1
                or stat.S_ISLNK(active_mode)
                or not stat.S_ISREG(active_mode)
            ):
                diagnostics.append(f"MIGRATION-ENDPOINT-TYPE:{active_path.as_posix()}")
            elif not source_exists and disposition == "archive-unique":
                if not _archive_envelope_is_exact(root, row, target, commit):
                    diagnostics.append(f"MIGRATION-ARCHIVE-ENVELOPE:{source_name}")
            else:
                try:
                    active_blob = _git(root, "hash-object", "--", active_path.as_posix())
                except MigrationAbort:
                    diagnostics.append(f"MIGRATION-ENDPOINT-BLOB:{active_path.as_posix()}")
                else:
                    if active_blob != expected_blob:
                        diagnostics.append(f"MIGRATION-CHANGED-SOURCE:{source_name}")
        if _ancestor_is_file(root, target):
            diagnostics.append(f"MIGRATION-TARGET-ANCESTOR:{target_name}")
        if disposition == "move-current":
            match = re.fullmatch(r"Spec-([0-9]{3})", str(row.get("workUnit")))
            target_match = MOVE_TARGET.fullmatch(target_name)
            if (
                match is None
                or target_match is None
                or target_match.group("unit") != match.group(1)
            ):
                diagnostics.append(f"MIGRATION-WORK-UNIT:{source_name}")
            else:
                unit = match.group(1)
                names = work_units.setdefault(unit, set())
                names.add(target.name)
                if (root / target.parent / "spec.md").is_file():
                    names.add("spec.md")
                else:
                    diagnostics.append(f"MIGRATION-WORK-UNIT-SPEC:{unit}")
        elif not target_name.startswith("docs/98.archive/04.execution/"):
            diagnostics.append(f"MIGRATION-ARCHIVE-TARGET:{target_name}")
    diagnostics.extend(validate_work_unit_paths(work_units))
    move_count = sum(
        isinstance(row, Mapping) and row.get("disposition") == "move-current"
        for row in entries
    )
    if move_count == 82 and len(work_units) != 41:
        diagnostics.append(
            f"WORK-UNIT-COUNT:expected=41:actual={len(work_units)}"
        )
    return tuple(sorted(set(diagnostics)))


def validate_manifest(
    root: Path,
    entries: Sequence[Mapping[str, Any]],
    expected_source_commit: str,
) -> tuple[str, ...]:
    """Return all deterministic manifest diagnostics without mutating the tree."""
    root = root.resolve()
    diagnostics: list[str] = []
    if not isinstance(expected_source_commit, str) or OID.fullmatch(expected_source_commit) is None:
        diagnostics.append("MIGRATION-SOURCE-COMMIT")
        commit = None
    else:
        try:
            kind = _git(root, "cat-file", "-t", expected_source_commit)
        except MigrationAbort:
            diagnostics.append("MIGRATION-SOURCE-COMMIT")
            commit = None
        else:
            if kind != "commit":
                diagnostics.append("MIGRATION-SOURCE-COMMIT")
                commit = None
            else:
                commit = expected_source_commit
    diagnostics.extend(_entry_diagnostics(root, entries, commit))
    return tuple(sorted(set(diagnostics)))


def validate_manifest_data(root: Path, data: Any, require_closed_counts: bool = True) -> MigrationPlan:
    root = root.resolve()
    if not isinstance(data, Mapping) or set(data) != TOP_KEYS or data.get("state") != "transition":
        raise MigrationAbort("MIGRATION-SCHEMA")
    commit = data.get("sourceCommit")
    if not isinstance(commit, str) or OID.fullmatch(commit) is None:
        raise MigrationAbort("MIGRATION-SOURCE-COMMIT")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        raise MigrationAbort("MIGRATION-ENTRIES")
    for row in entries:
        if not isinstance(row, Mapping) or set(row) != ENTRY_KEYS:
            raise MigrationAbort("MIGRATION-ENTRY-SCHEMA")
        _safe_path(row.get("source"))
        _safe_path(row.get("target"))
    diagnostics = validate_manifest(root, tuple(MappingProxyType(dict(row)) for row in entries), commit)
    if diagnostics:
        raise MigrationAbort(diagnostics[0])
    moves = sum(row["disposition"] == "move-current" for row in entries)
    archives = sum(row["disposition"] == "archive-unique" for row in entries)
    plan = MigrationPlan(len(entries), moves, archives)
    if require_closed_counts:
        validate_counts(move_count=moves, archive_count=archives, source_count=len(entries))
    return plan


def _controlled_dirty(root: Path, entries: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    paths = sorted({str(row[key]) for row in entries for key in ("source", "target")})
    if not paths:
        return ()
    output = _git(root, "status", "--porcelain=v1", "-z", "--", *paths)
    if not output:
        return ()
    dirty = []
    for record in output.split("\0"):
        if record:
            dirty.append(record[3:] if len(record) > 3 else record)
    return tuple(sorted(set(dirty)))


def plan_phase(
    root: Path,
    entries: Sequence[Mapping[str, Any]],
    phase: str,
) -> tuple[tuple[PurePosixPath, PurePosixPath], ...]:
    """Preflight one migration phase and return immutable, ordered rename pairs."""
    if phase not in PHASE_DISPOSITION:
        raise MigrationAbort("MIGRATION-PHASE")
    root = root.resolve()
    for index, row in enumerate(entries):
        if not isinstance(row, Mapping) or set(row) != ENTRY_KEYS:
            raise MigrationAbort(f"MIGRATION-ENTRY-SCHEMA:{index}")
        _safe_path(row.get("source"))
        _safe_path(row.get("target"))
    dirty = _controlled_dirty(root, entries)
    if dirty:
        raise MigrationAbort(f"MIGRATION-CONTROLLED-DIRTY:{dirty[0]}")
    structural = _entry_diagnostics(root, entries, None)
    if structural:
        raise MigrationAbort(structural[0])
    if phase == "move":
        for row in entries:
            if row["disposition"] != "archive-unique":
                continue
            source = root / _safe_path(row["source"])
            target = root / _safe_path(row["target"])
            if source.exists() or not target.is_file():
                raise MigrationAbort(f"MIGRATION-PHASE-PREREQUISITE:{row['source']}")
    pairs = []
    for row in entries:
        if row["disposition"] != PHASE_DISPOSITION[phase]:
            continue
        source = _safe_path(row["source"])
        target = _safe_path(row["target"])
        if not (root / source).is_file() or (root / target).exists():
            raise MigrationAbort(f"MIGRATION-PHASE-ENDPOINT:{source.as_posix()}")
        if _ancestor_is_file(root, target):
            raise MigrationAbort(f"MIGRATION-TARGET-ANCESTOR:{target.as_posix()}")
        expected_blob = row.get("sourceBlob")
        if _git(root, "hash-object", "--", source.as_posix()) != expected_blob:
            raise MigrationAbort(f"MIGRATION-CHANGED-SOURCE:{source.as_posix()}")
        pairs.append((source, target))
    return tuple(sorted(pairs, key=lambda pair: (pair[0].as_posix(), pair[1].as_posix())))


def _gitleaks_candidate_is_safe(candidate: Path, root: Path) -> bool:
    if (
        not candidate.is_absolute()
        or candidate.name != "gitleaks"
        or candidate.is_relative_to(root)
        or candidate.is_relative_to(Path("/tmp"))
    ):
        return False
    try:
        metadata = candidate.lstat()
        if candidate.resolve(strict=True) != candidate:
            return False
    except OSError:
        return False
    return (
        stat.S_ISREG(metadata.st_mode)
        and not stat.S_ISLNK(metadata.st_mode)
        and metadata.st_uid in {0, os.geteuid()}
        and not metadata.st_mode & 0o022
        and os.access(candidate, os.X_OK)
    )


def _gitleaks_executable(root: Path) -> Path | None:
    candidates: list[Path] = []
    hint = os.environ.get(GITLEAKS_HINT)
    if hint:
        candidates.append(Path(hint))
    discovered = shutil.which("gitleaks")
    if discovered:
        candidates.append(Path(discovered))
    candidates.extend(GITLEAKS_CANDIDATES)
    for candidate in candidates:
        if _gitleaks_candidate_is_safe(candidate, root):
            return candidate
    return None


def _config_fstat(config: _ConfigHandle) -> os.stat_result:
    try:
        metadata = os.fstat(config.descriptor)
    except OSError as exc:
        raise MigrationAbort("MIGRATION-SECRET-CONFIG") from exc
    if (
        metadata.st_dev != config.device
        or metadata.st_ino != config.inode
        or not stat.S_ISREG(metadata.st_mode)
        or stat.S_IMODE(metadata.st_mode) != 0o600
    ):
        raise MigrationAbort("MIGRATION-SECRET-CONFIG")
    return metadata


def _run_gitleaks(executable: Path, config_fd: int, payload: bytes) -> int:
    try:
        metadata = os.fstat(config_fd)
    except OSError as exc:
        raise MigrationAbort("MIGRATION-SECRET-CONFIG") from exc
    if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o600:
        raise MigrationAbort("MIGRATION-SECRET-CONFIG")
    config_reference = f"/proc/self/fd/{config_fd}"
    try:
        completed = subprocess.run(
            [
                str(executable),
                "detect",
                "--pipe",
                "--config",
                config_reference,
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
            env={"LC_ALL": "C"},
            pass_fds=(config_fd,),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MigrationAbort("MIGRATION-SECRET-CLASSIFIER-ERROR") from exc
    return completed.returncode


def _classify_secret_payload(
    root: Path,
    archive_path: str,
    payload: bytes,
    config: _ConfigHandle,
) -> None:
    executable = _gitleaks_executable(root)
    if executable is None:
        raise MigrationAbort(
            f"MIGRATION-SECRET-CLASSIFIER-UNAVAILABLE:{archive_path}"
        )
    _config_fstat(config)
    return_code = _run_gitleaks(executable, config.descriptor, payload)
    if return_code == SECRET_DETECTED_EXIT:
        raise MigrationAbort(f"MIGRATION-SECRET-DETECTED:{archive_path}")
    if return_code != 0:
        raise MigrationAbort(f"MIGRATION-SECRET-CLASSIFIER-ERROR:{archive_path}")


def _source_frontmatter(payload: bytes) -> Mapping[str, Any]:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationAbort("MIGRATION-ARCHIVE-METADATA") from exc
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return MappingProxyType({"text": text})
    raw, body = text[4:].split("\n---\n", 1)
    try:
        loaded = yaml.load(raw, Loader=_UniqueKeySafeLoader)
    except (_DuplicateYAMLKey, yaml.YAMLError) as exc:
        raise MigrationAbort("MIGRATION-ARCHIVE-METADATA") from exc
    if not isinstance(loaded, dict):
        raise MigrationAbort("MIGRATION-ARCHIVE-METADATA")
    return MappingProxyType({**loaded, "text": body})


def _archive_metadata(
    row: Mapping[str, Any], recovered: Any
) -> dict[str, object]:
    frontmatter = _source_frontmatter(recovered.source_bytes)
    body = str(frontmatter.get("text", ""))
    heading = next(
        (line[2:].strip() for line in body.splitlines() if line.startswith("# ")),
        "",
    )
    title = frontmatter.get("title")
    owner = frontmatter.get("owner")
    updated = frontmatter.get("updated")
    original_type = frontmatter.get("type")
    source = PurePosixPath(str(row["source"]))
    expected_type = "sdlc/plan" if source.parent.name == "plans" else "sdlc/task"
    return {
        "title": title if isinstance(title, str) and title else heading or source.stem,
        "type": "content/archive",
        "status": "archived",
        "owner": owner if isinstance(owner, str) and owner else "platform",
        "updated": (
            str(updated)
            if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", str(updated))
            else ARCHIVED_ON
        ),
        "original_type": (
            original_type
            if isinstance(original_type, str) and original_type
            else expected_type
        ),
        "original_path": recovered.original_path,
        "archived_on": ARCHIVED_ON,
        "archive_reason": "retired",
        "replacement": None,
        "source_commit": recovered.source_commit,
        "source_blob": recovered.source_blob,
        "content_sha256": recovered.content_sha256,
    }


def _path_is_ignored(root: Path, path: PurePosixPath) -> bool:
    result = _git_process(
        root,
        "check-ignore",
        "--no-index",
        "--quiet",
        "--",
        path.as_posix(),
        literal_paths=False,
    )
    if result.returncode not in {0, 1}:
        raise MigrationAbort("MIGRATION-GIT:check-ignore")
    return result.returncode == 0


def _phase_manifest_rows(
    root: Path,
    planned_pairs: Sequence[tuple[PurePosixPath, PurePosixPath]],
    phase: str,
) -> tuple[str, tuple[Mapping[str, Any], ...], bytes]:
    manifest = _capture_control_surface(root, MANIFEST_PATH)
    gitleaks_config = _capture_control_surface(root, GITLEAKS_CONFIG_PATH)
    document = _parse_manifest_bytes(manifest.contents)
    if document.source_commit != EXPECTED_SOURCE_COMMIT:
        raise MigrationAbort("MIGRATION-SOURCE-COMMIT:unexpected")
    diagnostics = validate_manifest(root, document.entries, document.source_commit)
    if diagnostics:
        raise MigrationAbort(diagnostics[0])
    move_count = sum(
        row["disposition"] == "move-current" for row in document.entries
    )
    archive_count = sum(
        row["disposition"] == "archive-unique" for row in document.entries
    )
    validate_counts(
        move_count=move_count,
        archive_count=archive_count,
        source_count=len(document.entries),
    )
    rows = tuple(
        sorted(
            (
                row
                for row in document.entries
                if row["disposition"] == PHASE_DISPOSITION[phase]
            ),
            key=lambda row: str(row["source"]),
        )
    )
    expected = tuple(
        sorted(
            (
                (_safe_path(row["source"]), _safe_path(row["target"]))
                for row in rows
            ),
            key=lambda pair: (pair[0].as_posix(), pair[1].as_posix()),
        )
    )
    if tuple(planned_pairs) != expected:
        raise MigrationAbort("MIGRATION-PLANNED-PAIRS-MISMATCH")
    return document.source_commit, rows, gitleaks_config.contents


def _tracked_source_blob(root: Path, source: PurePosixPath) -> str:
    line = _git(root, "ls-files", "--stage", "--", source.as_posix())
    records = [record for record in line.splitlines() if record]
    if len(records) != 1:
        raise MigrationAbort(f"MIGRATION-SOURCE-TRACKED:{source.as_posix()}")
    try:
        header, tracked_path = records[0].split("\t", 1)
        mode, blob, stage = header.split(" ", 2)
    except ValueError as exc:
        raise MigrationAbort("MIGRATION-SOURCE-TRACKED") from exc
    if (
        tracked_path != source.as_posix()
        or mode not in {"100644", "100755"}
        or stage != "0"
        or OID.fullmatch(blob) is None
    ):
        raise MigrationAbort(f"MIGRATION-SOURCE-TYPE:{source.as_posix()}")
    return blob


def _git_hash_bytes(root: Path, contents: bytes) -> str:
    root = _canonical_root(root)
    try:
        result = subprocess.run(
            [
                "git",
                "--no-replace-objects",
                "--literal-pathspecs",
                "-C",
                str(root),
                "hash-object",
                "--stdin",
            ],
            input=contents,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=GIT_TIMEOUT_SECONDS,
            env=_safe_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MigrationAbort("MIGRATION-GIT-ERROR") from exc
    try:
        digest = result.stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise MigrationAbort("MIGRATION-GIT:hash-object") from exc
    if result.returncode != 0 or OID.fullmatch(digest) is None:
        raise MigrationAbort("MIGRATION-GIT:hash-object")
    return digest


def _identity(path: Path) -> _FileIdentity:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
    return _FileIdentity(path, metadata.st_dev, metadata.st_ino, metadata.st_mode)


@contextlib.contextmanager
def _temporary_gitleaks_config(root: Path, contents: bytes):
    temporary = None
    body_error: BaseException | None = None
    try:
        temporary = tempfile.TemporaryFile(mode="w+b", dir=root)
        descriptor = temporary.fileno()
        os.fchmod(descriptor, 0o600)
        temporary.write(contents)
        temporary.flush()
        os.fsync(descriptor)
        temporary.seek(0)
        metadata = os.fstat(descriptor)
        handle = _ConfigHandle(
            descriptor,
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_mode,
        )
        _config_fstat(handle)
    except OSError as exc:
        if temporary is not None:
            temporary.close()
        raise MigrationAbort("MIGRATION-SECRET-CONFIG") from exc
    try:
        yield handle
    except BaseException as exc:
        body_error = exc
        raise
    finally:
        if temporary is not None:
            try:
                temporary.close()
            except OSError as cleanup_error:
                if body_error is not None:
                    body_error.add_note("MIGRATION-SECRET-CONFIG-CLEANUP")
                else:
                    raise MigrationAbort(
                        "MIGRATION-SECRET-CONFIG-CLEANUP"
                    ) from cleanup_error


def _capture_control_surface(root: Path, path: PurePosixPath) -> _ControlSurface:
    absolute = root / path
    descriptor: int | None = None
    try:
        before = absolute.lstat()
        descriptor = os.open(
            absolute,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
        )
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or stat.S_ISLNK(before.st_mode)
            or before.st_dev != opened.st_dev
            or before.st_ino != opened.st_ino
        ):
            raise MigrationAbort(f"MIGRATION-CONTROL-SURFACE:{path.as_posix()}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65536, CONTROL_SURFACE_LIMIT + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > CONTROL_SURFACE_LIMIT:
                raise MigrationAbort(
                    f"MIGRATION-CONTROL-SURFACE-SIZE:{path.as_posix()}"
                )
        contents = b"".join(chunks)
        after = absolute.lstat()
        if (
            after.st_dev != opened.st_dev
            or after.st_ino != opened.st_ino
            or after.st_mode != opened.st_mode
        ):
            raise MigrationAbort(f"MIGRATION-CONTROL-SURFACE:{path.as_posix()}")
    except (OSError, RuntimeError) as exc:
        raise MigrationAbort(
            f"MIGRATION-CONTROL-SURFACE:{path.as_posix()}"
        ) from exc
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError as exc:
                raise MigrationAbort(
                    f"MIGRATION-CONTROL-SURFACE:{path.as_posix()}"
                ) from exc
    index_blob = _tracked_source_blob(root, path)
    flags = _git(root, "ls-files", "-v", "--", path.as_posix())
    if flags != f"H {path.as_posix()}":
        raise MigrationAbort(f"MIGRATION-CONTROL-INDEX-FLAGS:{path.as_posix()}")
    if _git_hash_bytes(root, contents) != index_blob:
        raise MigrationAbort(f"MIGRATION-CONTROL-DIRTY:{path.as_posix()}")
    if _git(root, "status", "--porcelain=v1", "--", path.as_posix()):
        raise MigrationAbort(f"MIGRATION-CONTROL-DIRTY:{path.as_posix()}")
    return _ControlSurface(path, contents, index_blob)


def _prepare_operations(
    root: Path,
    rows: Sequence[Mapping[str, Any]],
    source_commit: str,
    phase: str,
    gitleaks_config: _ConfigHandle | None,
) -> tuple[_PreparedOperation, ...]:
    prepared: list[_PreparedOperation] = []
    for row in rows:
        source = _safe_path(row["source"])
        target = _safe_path(row["target"])
        source_name = source.as_posix()
        target_name = target.as_posix()
        if SOURCE_PATH.fullmatch(source_name) is None:
            raise MigrationAbort(f"MIGRATION-SOURCE-PATH:{source_name}")
        if phase == "archive":
            if target_name != source_name.replace(
                "docs/04.execution/", "docs/98.archive/04.execution/", 1
            ):
                raise MigrationAbort(f"MIGRATION-ARCHIVE-TARGET:{target_name}")
        elif MOVE_TARGET.fullmatch(target_name) is None:
            raise MigrationAbort(f"MIGRATION-WORK-UNIT:{target_name}")
        source_path = root / source
        target_path = root / target
        try:
            source_metadata = source_path.lstat()
        except OSError as exc:
            raise MigrationAbort(f"MIGRATION-PHASE-ENDPOINT:{source_name}") from exc
        if stat.S_ISLNK(source_metadata.st_mode) or not stat.S_ISREG(
            source_metadata.st_mode
        ):
            raise MigrationAbort(f"MIGRATION-SOURCE-TYPE:{source_name}")
        try:
            if source_path.resolve(strict=True) != source_path:
                raise MigrationAbort(f"MIGRATION-SOURCE-PATH:{source_name}")
        except (OSError, RuntimeError) as exc:
            raise MigrationAbort(f"MIGRATION-SOURCE-PATH:{source_name}") from exc
        try:
            target_path.lstat()
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise MigrationAbort(f"MIGRATION-PHASE-ENDPOINT:{target_name}") from exc
        else:
            raise MigrationAbort(f"MIGRATION-PHASE-ENDPOINT:{target_name}")
        if _ancestor_is_file(root, target):
            raise MigrationAbort(f"MIGRATION-TARGET-ANCESTOR:{target_name}")
        if _path_is_ignored(root, source) or _path_is_ignored(root, target):
            raise MigrationAbort(f"MIGRATION-IGNORED-PATH:{source_name}")
        expected_blob = str(row["sourceBlob"])
        if _tracked_source_blob(root, source) != expected_blob:
            raise MigrationAbort(f"MIGRATION-SOURCE-BLOB:{source_name}")
        if _git(root, "rev-parse", f"{source_commit}:{source_name}") != expected_blob:
            raise MigrationAbort(f"MIGRATION-SOURCE-BLOB:{source_name}")
        if _git(root, "hash-object", "--", source_name) != expected_blob:
            raise MigrationAbort(f"MIGRATION-CHANGED-SOURCE:{source_name}")
        try:
            recovered = recover_git_blob(root, source_name, source_commit)
            if recovered.source_blob != expected_blob:
                raise MigrationAbort(f"MIGRATION-SOURCE-BLOB:{source_name}")
            source_bytes = recovered.source_bytes
            if phase == "archive":
                if gitleaks_config is None:
                    raise MigrationAbort("MIGRATION-SECRET-CONFIG")
                _classify_secret_payload(
                    root,
                    target_name,
                    recovered.source_bytes,
                    gitleaks_config,
                )
                metadata = _archive_metadata(row, recovered)
                output = render_archive_envelope(
                    metadata, recovered, recovered.source_bytes
                )
                parse_archive_envelope(output, expected=recovered)
                target_mode = 0o644
            else:
                output = recovered.source_bytes
                target_mode = stat.S_IMODE(source_metadata.st_mode)
        except ArchiveContractError as exc:
            raise MigrationAbort(
                f"MIGRATION-ARCHIVE-METADATA:{target_name}"
            ) from exc
        source_mode = stat.S_IMODE(source_metadata.st_mode)
        prepared.append(
            _PreparedOperation(
                source,
                target,
                expected_blob,
                source_bytes,
                output,
                source_mode,
                target_mode,
            )
        )
    return tuple(prepared)


def _fd_identity(descriptor: int, path: Path) -> _FileIdentity:
    try:
        metadata = os.fstat(descriptor)
    except OSError as exc:
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
    return _FileIdentity(path, metadata.st_dev, metadata.st_ino, metadata.st_mode)


def _stat_at(directory_fd: int, name: str, path: Path) -> _FileIdentity:
    try:
        metadata = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except OSError as exc:
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
    return _FileIdentity(path, metadata.st_dev, metadata.st_ino, metadata.st_mode)


def _same_object(left: _FileIdentity, right: _FileIdentity) -> bool:
    return left.device == right.device and left.inode == right.inode


def _read_descriptor(descriptor: int) -> bytes:
    try:
        os.lseek(descriptor, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
    except OSError as exc:
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc


def _open_directory(path: Path) -> int:
    try:
        return os.open(
            path,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
    except OSError as exc:
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc


def _close_descriptor(descriptor: int) -> bool:
    if descriptor < 0:
        return True
    try:
        os.close(descriptor)
    except OSError:
        return False
    return True


def _cleanup_failed_transaction_init(
    root: Path,
    root_fd: int,
    name: str,
    quarantine_fd: int | None,
) -> bool:
    current_name = name
    descriptor = quarantine_fd
    clean = False
    try:
        if descriptor is None:
            descriptor = os.open(
                name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=root_fd,
            )
        opened = os.fstat(descriptor)
        linked = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
        if (
            not stat.S_ISDIR(opened.st_mode)
            or opened.st_dev != linked.st_dev
            or opened.st_ino != linked.st_ino
            or os.listdir(descriptor)
        ):
            raise OSError("unsafe transaction initialization residue")
        disposal = f".migration-disposal-{secrets.token_hex(8)}"
        os.rename(name, disposal, src_dir_fd=root_fd, dst_dir_fd=root_fd)
        current_name = disposal
        moved = os.stat(disposal, dir_fd=root_fd, follow_symlinks=False)
        if moved.st_dev != opened.st_dev or moved.st_ino != opened.st_ino:
            raise OSError("transaction initialization identity changed")
        os.rmdir(disposal, dir_fd=root_fd)
        clean = True
    except OSError:
        recovery = f".migration-recovery-{secrets.token_hex(8)}"
        try:
            os.rename(
                current_name,
                recovery,
                src_dir_fd=root_fd,
                dst_dir_fd=root_fd,
            )
        except OSError:
            pass
    finally:
        if descriptor is not None:
            _close_descriptor(descriptor)
        _close_descriptor(root_fd)
    return clean


def _start_transaction(root: Path) -> _Transaction:
    root_fd = _open_directory(root)
    try:
        root_identity = _fd_identity(root_fd, root)
    except MigrationAbort:
        _close_descriptor(root_fd)
        raise
    name = f".migration-transaction-{secrets.token_hex(8)}"
    quarantine_fd: int | None = None
    created = False
    try:
        os.mkdir(name, mode=0o700, dir_fd=root_fd)
        created = True
        quarantine_fd = os.open(
            name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=root_fd,
        )
        identity = _fd_identity(quarantine_fd, root / name)
        return _Transaction(
            root,
            root_fd,
            root_identity,
            quarantine_fd,
            name,
            identity,
        )
    except (OSError, MigrationAbort) as exc:
        if created:
            cleaned = _cleanup_failed_transaction_init(
                root, root_fd, name, quarantine_fd
            )
            if not cleaned:
                exc.add_note("MIGRATION-ROLLBACK:RECOVERY-RESIDUE")
        else:
            if quarantine_fd is not None:
                _close_descriptor(quarantine_fd)
            _close_descriptor(root_fd)
        if isinstance(exc, MigrationAbort):
            raise
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc


def _verify_directory_anchors(transaction: _Transaction) -> None:
    try:
        root_open = os.fstat(transaction.root_fd)
        root_linked = transaction.root.lstat()
    except OSError as exc:
        raise MigrationAbort("MIGRATION-DIRECTORY-CHANGED") from exc
    if (
        root_open.st_dev != transaction.root_identity.device
        or root_open.st_ino != transaction.root_identity.inode
        or root_linked.st_dev != transaction.root_identity.device
        or root_linked.st_ino != transaction.root_identity.inode
        or not stat.S_ISDIR(root_open.st_mode)
    ):
        raise MigrationAbort("MIGRATION-DIRECTORY-CHANGED")
    for anchor in transaction.directory_anchors:
        if not anchor.active:
            continue
        try:
            opened = os.fstat(anchor.descriptor)
            linked = os.stat(
                anchor.name,
                dir_fd=anchor.parent_fd,
                follow_symlinks=False,
            )
        except OSError as exc:
            raise MigrationAbort("MIGRATION-DIRECTORY-CHANGED") from exc
        if (
            opened.st_dev != anchor.identity.device
            or opened.st_ino != anchor.identity.inode
            or linked.st_dev != anchor.identity.device
            or linked.st_ino != anchor.identity.inode
            or not stat.S_ISDIR(opened.st_mode)
            or not stat.S_ISDIR(linked.st_mode)
        ):
            raise MigrationAbort("MIGRATION-DIRECTORY-CHANGED")


def _open_relative_directory(
    transaction: _Transaction,
    relative: PurePosixPath,
    *,
    create: bool,
) -> int:
    if relative.is_absolute() or not relative.parts:
        raise MigrationAbort("MIGRATION-DIRECTORY-PATH")
    parent_fd = transaction.root_fd
    current = PurePosixPath()
    for component in relative.parts:
        if component in {"", ".", ".."}:
            raise MigrationAbort("MIGRATION-DIRECTORY-PATH")
        current /= component
        _verify_directory_anchors(transaction)
        created = False
        created_identity: _FileIdentity | None = None
        provisional: _CreatedDirectory | None = None
        descriptor: int | None = None
        try:
            descriptor = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=parent_fd,
            )
        except FileNotFoundError:
            if not create:
                raise MigrationAbort("MIGRATION-DIRECTORY-CHANGED") from None
            try:
                _verify_directory_anchors(transaction)
                os.mkdir(component, mode=0o755, dir_fd=parent_fd)
                provisional = _CreatedDirectory(parent_fd, component, current)
                transaction.created_directories.append(provisional)
                created_identity = _stat_at(
                    parent_fd, component, transaction.root / current
                )
                provisional.identity = created_identity
                descriptor = os.open(
                    component,
                    os.O_RDONLY
                    | os.O_DIRECTORY
                    | os.O_NOFOLLOW
                    | os.O_CLOEXEC,
                    dir_fd=parent_fd,
                )
                provisional.descriptor = descriptor
                created = True
            except (OSError, MigrationAbort) as exc:
                if descriptor is not None:
                    _close_descriptor(descriptor)
                    descriptor = None
                if provisional is not None:
                    provisional.descriptor = None
                if isinstance(exc, MigrationAbort):
                    raise
                raise MigrationAbort("MIGRATION-TARGET-ANCESTOR") from exc
        except OSError as exc:
            raise MigrationAbort("MIGRATION-TARGET-ANCESTOR") from exc
        if descriptor is None:
            raise MigrationAbort("MIGRATION-TARGET-ANCESTOR")
        try:
            identity = _fd_identity(descriptor, transaction.root / current)
            linked = _stat_at(parent_fd, component, transaction.root / current)
        except MigrationAbort:
            _close_descriptor(descriptor)
            if provisional is not None:
                provisional.descriptor = None
            raise
        if (
            not stat.S_ISDIR(identity.mode)
            or not _same_object(identity, linked)
            or (
                created_identity is not None
                and not _same_object(identity, created_identity)
            )
        ):
            _close_descriptor(descriptor)
            if provisional is not None:
                provisional.descriptor = None
            raise MigrationAbort("MIGRATION-DIRECTORY-CHANGED")
        anchor = _DirectoryAnchor(
            parent_fd,
            descriptor,
            component,
            current,
            identity,
            created,
        )
        transaction.directory_anchors.append(anchor)
        if provisional is not None:
            provisional.descriptor = descriptor
            provisional.identity = identity
        parent_fd = descriptor
    _verify_directory_anchors(transaction)
    return parent_fd


def _private_unlink(
    transaction: _Transaction,
    name: str,
    expected: _FileIdentity,
) -> bool:
    disposal = f"private-disposal-{secrets.token_hex(8)}"
    try:
        os.rename(
            name,
            disposal,
            src_dir_fd=transaction.quarantine_fd,
            dst_dir_fd=transaction.quarantine_fd,
        )
        moved = _stat_at(
            transaction.quarantine_fd,
            disposal,
            transaction.root / transaction.quarantine_name / disposal,
        )
        if not _same_object(moved, expected):
            transaction.recovery_required = True
            transaction.replacement_detected = True
            try:
                os.link(
                    disposal,
                    name,
                    src_dir_fd=transaction.quarantine_fd,
                    dst_dir_fd=transaction.quarantine_fd,
                    follow_symlinks=False,
                )
            except OSError:
                pass
            return False
        os.unlink(disposal, dir_fd=transaction.quarantine_fd)
    except MigrationAbort:
        transaction.recovery_required = True
        return False
    except OSError:
        transaction.recovery_required = True
        return False
    return True


def _close_transaction_fds(transaction: _Transaction) -> bool:
    clean = True
    for operation in transaction.operations:
        for descriptor_name in (
            "target_fd",
            "stage_fd",
            "source_fd",
        ):
            descriptor = getattr(operation, descriptor_name)
            if descriptor is None or descriptor < 0:
                continue
            try:
                os.close(descriptor)
            except OSError:
                clean = False
            setattr(operation, descriptor_name, -1)
        operation.target_parent_fd = -1
        operation.source_parent_fd = -1
    for anchor in reversed(transaction.directory_anchors):
        if anchor.descriptor < 0:
            continue
        if not _close_descriptor(anchor.descriptor):
            clean = False
        anchor.descriptor = -1
    return clean


def _preserve_recovery(transaction: _Transaction) -> None:
    recovery_name = transaction.quarantine_name
    failure: OSError | None = None
    try:
        if not recovery_name.startswith(".migration-recovery-"):
            recovery_name = f".migration-recovery-{secrets.token_hex(8)}"
            os.rename(
                transaction.quarantine_name,
                recovery_name,
                src_dir_fd=transaction.root_fd,
                dst_dir_fd=transaction.root_fd,
            )
            transaction.quarantine_name = recovery_name
    except OSError as exc:
        failure = exc
    finally:
        if transaction.quarantine_fd >= 0:
            if not _close_descriptor(transaction.quarantine_fd) and failure is None:
                failure = OSError("quarantine descriptor close failed")
            transaction.quarantine_fd = -1
        if transaction.root_fd >= 0:
            if not _close_descriptor(transaction.root_fd) and failure is None:
                failure = OSError("root descriptor close failed")
            transaction.root_fd = -1
    if failure is not None:
        raise MigrationAbort("MIGRATION-ROLLBACK:RECOVERY-RESIDUE") from failure


def _deactivate_directory_identity(
    transaction: _Transaction,
    identity: _FileIdentity,
) -> None:
    for anchor in transaction.directory_anchors:
        if _same_object(anchor.identity, identity):
            anchor.active = False
    for created in transaction.created_directories:
        if created.identity is not None and _same_object(created.identity, identity):
            created.active = False


def _rollback_created_directories(transaction: _Transaction) -> bool:
    clean = True
    for created in reversed(transaction.created_directories):
        if not created.active:
            continue
        disposal = f"created-directory-{secrets.token_hex(8)}"
        moved_fd: int | None = None
        temporary_fd: int | None = None
        try:
            if created.identity is None:
                recovery_entry = f"unverified-created-{secrets.token_hex(8)}"
                _verify_directory_anchors(transaction)
                os.rename(
                    created.name,
                    recovery_entry,
                    src_dir_fd=created.parent_fd,
                    dst_dir_fd=transaction.quarantine_fd,
                )
                created.active = False
                transaction.recovery_required = True
                clean = False
                continue
            _verify_directory_anchors(transaction)
            descriptor = created.descriptor
            if descriptor is None:
                temporary_fd = os.open(
                    created.name,
                    os.O_RDONLY
                    | os.O_DIRECTORY
                    | os.O_NOFOLLOW
                    | os.O_CLOEXEC,
                    dir_fd=created.parent_fd,
                )
                descriptor = temporary_fd
            opened = _fd_identity(
                descriptor, transaction.root / created.relative
            )
            linked = _stat_at(
                created.parent_fd,
                created.name,
                transaction.root / created.relative,
            )
            if (
                not _same_object(opened, created.identity)
                or not _same_object(linked, created.identity)
            ):
                transaction.recovery_required = True
                clean = False
                continue
            if os.listdir(descriptor):
                continue
            os.rename(
                created.name,
                disposal,
                src_dir_fd=created.parent_fd,
                dst_dir_fd=transaction.quarantine_fd,
            )
            _deactivate_directory_identity(transaction, created.identity)
            moved_fd = os.open(
                disposal,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=transaction.quarantine_fd,
            )
            moved = _fd_identity(
                moved_fd,
                transaction.root / transaction.quarantine_name / disposal,
            )
            if not _same_object(moved, created.identity) or os.listdir(moved_fd):
                transaction.recovery_required = True
                clean = False
                continue
            os.rmdir(disposal, dir_fd=transaction.quarantine_fd)
        except (OSError, MigrationAbort):
            transaction.recovery_required = True
            clean = False
        finally:
            if moved_fd is not None:
                _close_descriptor(moved_fd)
            if temporary_fd is not None:
                _close_descriptor(temporary_fd)
    return clean


def _dispose_transaction(transaction: _Transaction) -> bool:
    if not _close_transaction_fds(transaction):
        transaction.recovery_required = True
        try:
            _preserve_recovery(transaction)
        except MigrationAbort:
            pass
        return False
    try:
        if os.listdir(transaction.quarantine_fd):
            raise OSError("transaction quarantine is not empty")
        disposal = f".migration-disposal-{secrets.token_hex(8)}"
        os.rename(
            transaction.quarantine_name,
            disposal,
            src_dir_fd=transaction.root_fd,
            dst_dir_fd=transaction.root_fd,
        )
        transaction.quarantine_name = disposal
        moved = _stat_at(transaction.root_fd, disposal, transaction.root / disposal)
        opened = _fd_identity(transaction.quarantine_fd, transaction.root / disposal)
        if (
            not _same_object(moved, transaction.quarantine_identity)
            or not _same_object(opened, transaction.quarantine_identity)
        ):
            raise OSError("transaction disposal identity changed")
        os.rmdir(disposal, dir_fd=transaction.root_fd)
        descriptors_closed = _close_descriptor(transaction.quarantine_fd)
        transaction.quarantine_fd = -1
        descriptors_closed = (
            _close_descriptor(transaction.root_fd) and descriptors_closed
        )
        transaction.root_fd = -1
        if not descriptors_closed:
            return False
    except (OSError, MigrationAbort):
        transaction.recovery_required = True
        try:
            _preserve_recovery(transaction)
        except MigrationAbort:
            pass
        return False
    return True


def _write_private_stage(
    transaction: _Transaction,
    name: str,
    contents: bytes,
    mode: int,
) -> tuple[int, _FileIdentity]:
    descriptor: int | None = None
    identity: _FileIdentity | None = None
    try:
        descriptor = os.open(
            name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            mode,
            dir_fd=transaction.quarantine_fd,
        )
        identity = _fd_identity(
            descriptor,
            transaction.root / transaction.quarantine_name / name,
        )
        os.fchmod(descriptor, mode)
        offset = 0
        while offset < len(contents):
            offset += os.write(descriptor, contents[offset:])
        os.fsync(descriptor)
        os.lseek(descriptor, 0, os.SEEK_SET)
    except (OSError, MigrationAbort) as exc:
        cleanup_identity = identity
        if descriptor is not None:
            try:
                if cleanup_identity is None:
                    metadata = os.fstat(descriptor)
                    if stat.S_ISREG(metadata.st_mode):
                        cleanup_identity = _FileIdentity(
                            transaction.root / transaction.quarantine_name / name,
                            metadata.st_dev,
                            metadata.st_ino,
                            metadata.st_mode,
                        )
            except OSError:
                transaction.recovery_required = True
            finally:
                if not _close_descriptor(descriptor):
                    transaction.recovery_required = True
        if cleanup_identity is not None:
            _private_unlink(transaction, name, cleanup_identity)
        else:
            transaction.recovery_required = True
        if isinstance(exc, MigrationAbort):
            raise
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
    if identity is None:
        raise MigrationAbort("MIGRATION-FILESYSTEM")
    return descriptor, identity


def _create_transaction_operation(
    transaction: _Transaction,
    prepared: _PreparedOperation,
    index: int,
) -> _TransactionOperation:
    source_path = transaction.root / prepared.source
    source_parent_fd = _open_relative_directory(
        transaction, prepared.source.parent, create=False
    )
    source_fd: int | None = None
    target_parent_fd: int | None = None
    anchor: _FileIdentity | None = None
    source_anchor = f"source-{index}"
    try:
        source_fd = os.open(
            source_path.name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=source_parent_fd,
        )
        source_identity = _fd_identity(source_fd, source_path)
        if (
            not stat.S_ISREG(source_identity.mode)
            or _read_descriptor(source_fd) != prepared.source_bytes
        ):
            raise MigrationAbort("MIGRATION-CHANGED-SOURCE")
        os.link(
            source_path.name,
            source_anchor,
            src_dir_fd=source_parent_fd,
            dst_dir_fd=transaction.quarantine_fd,
            follow_symlinks=False,
        )
        anchor = source_identity
        linked_anchor = _stat_at(
            transaction.quarantine_fd,
            source_anchor,
            transaction.root / transaction.quarantine_name / source_anchor,
        )
        if not _same_object(linked_anchor, source_identity):
            raise MigrationAbort("MIGRATION-CHANGED-SOURCE")
        target_parent_fd = _open_relative_directory(
            transaction, prepared.target.parent, create=True
        )
        try:
            os.stat(
                prepared.target.name,
                dir_fd=target_parent_fd,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            pass
        else:
            raise MigrationAbort("MIGRATION-PHASE-ENDPOINT")
        stage_name = f"stage-{index}"
        stage_fd, _ = _write_private_stage(
            transaction, stage_name, prepared.output, prepared.target_mode
        )
    except (OSError, MigrationAbort) as exc:
        if anchor is not None:
            _private_unlink(transaction, source_anchor, anchor)
        for descriptor in (source_fd,):
            if descriptor is not None:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
        if isinstance(exc, MigrationAbort):
            raise
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
    if source_fd is None or target_parent_fd is None:
        raise MigrationAbort("MIGRATION-FILESYSTEM")
    return _TransactionOperation(
        prepared,
        source_parent_fd,
        source_fd,
        source_identity,
        source_anchor,
        target_parent_fd,
        stage_fd,
        stage_name,
    )


def _verify_target(operation: _TransactionOperation) -> None:
    target_name = operation.prepared.target.name
    try:
        descriptor = os.open(
            target_name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=operation.target_parent_fd,
        )
    except OSError as exc:
        raise MigrationAbort("MIGRATION-TARGET-CHANGED") from exc
    try:
        current = _fd_identity(descriptor, Path(target_name))
        if (
            operation.target_identity is None
            or not _same_object(current, operation.target_identity)
            or _read_descriptor(descriptor) != operation.prepared.output
        ):
            raise MigrationAbort("MIGRATION-TARGET-CHANGED")
    finally:
        try:
            os.close(descriptor)
        except OSError as exc:
            raise MigrationAbort("MIGRATION-FILESYSTEM") from exc


def _verify_all_targets(transaction: _Transaction) -> None:
    _verify_directory_anchors(transaction)
    for operation in transaction.operations:
        if operation.target_identity is not None:
            _verify_target(operation)
    _verify_directory_anchors(transaction)


def _install_targets(transaction: _Transaction) -> None:
    for operation in transaction.operations:
        stage_identity = _fd_identity(
            operation.stage_fd, Path(operation.stage_name)
        )
        try:
            _verify_directory_anchors(transaction)
            os.link(
                operation.stage_name,
                operation.prepared.target.name,
                src_dir_fd=transaction.quarantine_fd,
                dst_dir_fd=operation.target_parent_fd,
                follow_symlinks=False,
            )
            operation.target_installed = True
            operation.target_identity = stage_identity
            target_fd = os.open(
                operation.prepared.target.name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=operation.target_parent_fd,
            )
            operation.target_fd = target_fd
            _verify_directory_anchors(transaction)
            target_identity = _fd_identity(
                target_fd, transaction.root / operation.prepared.target
            )
            if not _same_object(stage_identity, target_identity):
                raise MigrationAbort("MIGRATION-TARGET-CHANGED")
            _verify_target(operation)
        except (OSError, MigrationAbort) as exc:
            if operation.target_fd is not None:
                _close_descriptor(operation.target_fd)
                operation.target_fd = None
            if isinstance(exc, MigrationAbort):
                raise
            raise MigrationAbort("MIGRATION-FILESYSTEM") from exc


def _restore_quarantined_entry(
    transaction: _Transaction,
    quarantine_name: str,
    operation: _TransactionOperation,
    expected: _FileIdentity,
) -> bool:
    try:
        _verify_directory_anchors(transaction)
        os.link(
            quarantine_name,
            operation.prepared.source.name,
            src_dir_fd=transaction.quarantine_fd,
            dst_dir_fd=operation.source_parent_fd,
            follow_symlinks=False,
        )
        restored = _stat_at(
            operation.source_parent_fd,
            operation.prepared.source.name,
            transaction.root / operation.prepared.source,
        )
        _verify_directory_anchors(transaction)
    except (OSError, MigrationAbort):
        return False
    if not _same_object(restored, expected):
        return False
    return _private_unlink(transaction, quarantine_name, expected)


def _quarantine_source(
    transaction: _Transaction,
    operation: _TransactionOperation,
    index: int,
) -> None:
    source_name = operation.prepared.source.name
    current_fd: int | None = None
    try:
        current_fd = os.open(
            source_name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=operation.source_parent_fd,
        )
        current = _fd_identity(current_fd, transaction.root / operation.prepared.source)
        current_bytes = _read_descriptor(current_fd)
        if (
            not _same_object(current, operation.source_identity)
            or current_bytes != operation.prepared.source_bytes
        ):
            raise MigrationAbort("MIGRATION-CHANGED-SOURCE")
        removed_name = f"removed-{index}"
        _verify_directory_anchors(transaction)
        os.rename(
            source_name,
            removed_name,
            src_dir_fd=operation.source_parent_fd,
            dst_dir_fd=transaction.quarantine_fd,
        )
        operation.removed_name = removed_name
        moved = _stat_at(
            transaction.quarantine_fd,
            removed_name,
            transaction.root / transaction.quarantine_name / removed_name,
        )
        operation.removed_identity = moved
        _verify_directory_anchors(transaction)
    except OSError as exc:
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
    finally:
        if current_fd is not None:
            _close_descriptor(current_fd)
    if not _same_object(moved, operation.source_identity):
        raise MigrationAbort("MIGRATION-ROLLBACK:SOURCE-REPLACED")


def _rollback_source(
    transaction: _Transaction,
    operation: _TransactionOperation,
) -> bool:
    if operation.removed_name is None:
        return True
    try:
        moved = _stat_at(
            transaction.quarantine_fd,
            operation.removed_name,
            transaction.root
            / transaction.quarantine_name
            / operation.removed_name,
        )
    except MigrationAbort:
        moved = None
    if moved is not None and _same_object(moved, operation.source_identity):
        return _restore_quarantined_entry(
            transaction,
            operation.removed_name,
            operation,
            operation.source_identity,
        )
    if moved is not None:
        _restore_quarantined_entry(
            transaction,
            operation.removed_name,
            operation,
            moved,
        )
        transaction.recovery_required = True
        return False
    _restore_quarantined_entry(
        transaction,
        operation.source_anchor,
        operation,
        operation.source_identity,
    )
    transaction.recovery_required = True
    return False


def _rollback_target(
    transaction: _Transaction,
    operation: _TransactionOperation,
    index: int,
) -> bool:
    if not operation.target_installed or operation.target_identity is None:
        return True
    quarantine_name = f"rollback-target-{index}"
    try:
        _verify_directory_anchors(transaction)
        os.rename(
            operation.prepared.target.name,
            quarantine_name,
            src_dir_fd=operation.target_parent_fd,
            dst_dir_fd=transaction.quarantine_fd,
        )
    except FileNotFoundError:
        return True
    except MigrationAbort:
        transaction.recovery_required = True
        return False
    except OSError:
        return False
    try:
        moved = _stat_at(
            transaction.quarantine_fd,
            quarantine_name,
            transaction.root / transaction.quarantine_name / quarantine_name,
        )
    except MigrationAbort:
        return False
    if _same_object(moved, operation.target_identity):
        return _private_unlink(transaction, quarantine_name, moved)
    transaction.replacement_detected = True
    try:
        os.link(
            quarantine_name,
            operation.prepared.target.name,
            src_dir_fd=transaction.quarantine_fd,
            dst_dir_fd=operation.target_parent_fd,
            follow_symlinks=False,
        )
        restored = _stat_at(
            operation.target_parent_fd,
            operation.prepared.target.name,
            transaction.root / operation.prepared.target,
        )
        _verify_directory_anchors(transaction)
    except (OSError, MigrationAbort):
        transaction.recovery_required = True
        return False
    if not _same_object(restored, moved):
        transaction.recovery_required = True
        return False
    return _private_unlink(transaction, quarantine_name, moved)


def _rollback_transaction(transaction: _Transaction) -> bool:
    clean = True
    for operation in reversed(transaction.operations):
        if operation.removed_name is not None:
            clean = _rollback_source(transaction, operation) and clean
            if not clean:
                transaction.recovery_required = True
    for index, operation in reversed(tuple(enumerate(transaction.operations))):
        clean = _rollback_target(transaction, operation, index) and clean
    for operation in transaction.operations:
        if not transaction.recovery_required:
            clean = _private_unlink(
                transaction,
                operation.source_anchor,
                operation.source_identity,
            ) and clean
        stage_identity = _fd_identity(operation.stage_fd, Path(operation.stage_name))
        clean = _private_unlink(
            transaction, operation.stage_name, stage_identity
        ) and clean
    clean = _rollback_created_directories(transaction) and clean
    if not clean:
        transaction.recovery_required = True
    if transaction.recovery_required:
        _close_transaction_fds(transaction)
        _preserve_recovery(transaction)
        return False
    return _dispose_transaction(transaction)


def _commit_transaction(transaction: _Transaction) -> None:
    _verify_all_targets(transaction)
    transaction.commit_started = True
    clean = True
    for operation in transaction.operations:
        if operation.removed_name is None:
            raise MigrationAbort("MIGRATION-ROLLBACK")
        clean = _private_unlink(
            transaction, operation.removed_name, operation.source_identity
        ) and clean
        clean = _private_unlink(
            transaction, operation.source_anchor, operation.source_identity
        ) and clean
        stage_identity = _fd_identity(operation.stage_fd, Path(operation.stage_name))
        clean = _private_unlink(
            transaction, operation.stage_name, stage_identity
        ) and clean
    if not clean or not _dispose_transaction(transaction):
        raise MigrationAbort("MIGRATION-ROLLBACK")


def _repository_lock_path(root: Path) -> Path:
    raw = _git(root, "rev-parse", "--git-common-dir")
    common = Path(raw)
    if not common.is_absolute():
        common = root / common
    try:
        common = common.resolve(strict=True)
        metadata = common.lstat()
    except (OSError, RuntimeError) as exc:
        raise MigrationAbort("MIGRATION-LOCK") from exc
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        raise MigrationAbort("MIGRATION-LOCK")
    return common / "document-taxonomy-migration.lock"


def _cleanup_repository_lock(handle: _RepositoryLockHandle) -> None:
    disposal = f"document-taxonomy-migration.lock-disposal-{secrets.token_hex(8)}"
    try:
        os.rename(
            handle.name,
            disposal,
            src_dir_fd=handle.parent_fd,
            dst_dir_fd=handle.parent_fd,
        )
        moved = _stat_at(handle.parent_fd, disposal, Path(disposal))
        if not _same_object(moved, handle.identity):
            raise MigrationAbort("MIGRATION-LOCK-CLEANUP")
        os.unlink(disposal, dir_fd=handle.parent_fd)
        os.close(handle.descriptor)
        os.close(handle.parent_fd)
    except (OSError, MigrationAbort) as exc:
        for descriptor in (handle.descriptor, handle.parent_fd):
            try:
                os.close(descriptor)
            except OSError:
                pass
        raise MigrationAbort("MIGRATION-LOCK-CLEANUP") from exc


@contextlib.contextmanager
def _repository_lock(root: Path):
    path = _repository_lock_path(root)
    parent_fd = _open_directory(path.parent)
    descriptor: int | None = None
    try:
        descriptor = os.open(
            path.name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=parent_fd,
        )
    except FileExistsError as exc:
        os.close(parent_fd)
        raise MigrationAbort("MIGRATION-LOCK-CONTENDED") from exc
    except OSError as exc:
        os.close(parent_fd)
        raise MigrationAbort("MIGRATION-LOCK") from exc
    try:
        identity = _fd_identity(descriptor, path)
    except MigrationAbort as exc:
        os.close(descriptor)
        os.close(parent_fd)
        exc.add_note("MIGRATION-LOCK-IDENTITY-UNAVAILABLE:lock preserved")
        raise
    handle = _RepositoryLockHandle(parent_fd, descriptor, path.name, identity)
    try:
        yield
    except BaseException as body_error:
        try:
            _cleanup_repository_lock(handle)
        except MigrationAbort as cleanup_error:
            body_error.add_note(str(cleanup_error))
        raise
    else:
        _cleanup_repository_lock(handle)


def _require_transaction_platform(phase: str) -> None:
    if (
        not _TRANSACTION_PLATFORM_SUPPORTED
        or (phase == "archive" and not Path("/proc/self/fd").is_dir())
    ):
        raise MigrationAbort("MIGRATION-PLATFORM-UNSUPPORTED")


def apply_phase(
    root: Path,
    planned_pairs: Sequence[tuple[PurePosixPath | Path, PurePosixPath | Path]],
    phase: str,
) -> None:
    """Apply a manifest-exact phase with full preflight and rollback."""
    if phase not in PHASE_DISPOSITION:
        raise MigrationAbort("MIGRATION-PHASE")
    root = _canonical_root(root)
    _require_transaction_platform(phase)
    with _repository_lock(root):
        _apply_phase_locked(root, planned_pairs, phase)


def _apply_phase_locked(
    root: Path,
    planned_pairs: Sequence[tuple[PurePosixPath | Path, PurePosixPath | Path]],
    phase: str,
) -> None:
    checked: list[tuple[PurePosixPath, PurePosixPath]] = []
    sources: set[str] = set()
    targets: set[str] = set()
    for raw_pair in planned_pairs:
        if not isinstance(raw_pair, tuple) or len(raw_pair) != 2:
            raise MigrationAbort("MIGRATION-PLANNED-PAIR")
        source = _safe_path(raw_pair[0].as_posix() if isinstance(raw_pair[0], PurePosixPath) else raw_pair[0])
        target = _safe_path(raw_pair[1].as_posix() if isinstance(raw_pair[1], PurePosixPath) else raw_pair[1])
        source_name, target_name = source.as_posix(), target.as_posix()
        if source_name in sources or target_name in targets:
            raise MigrationAbort("MIGRATION-PLANNED-DUPLICATE")
        sources.add(source_name)
        targets.add(target_name)
        checked.append((source, target))
    checked_tuple = tuple(checked)
    source_commit, rows, gitleaks_contents = _phase_manifest_rows(
        root, checked_tuple, phase
    )
    status_entries = tuple(
        MappingProxyType({"source": source.as_posix(), "target": target.as_posix()})
        for source, target in checked
    )
    dirty = _controlled_dirty(root, status_entries)
    if dirty:
        raise MigrationAbort(f"MIGRATION-CONTROLLED-DIRTY:{dirty[0]}")
    config_context = (
        _temporary_gitleaks_config(root, gitleaks_contents)
        if phase == "archive"
        else contextlib.nullcontext(None)
    )
    with config_context as gitleaks_config:
        prepared = _prepare_operations(
            root, rows, source_commit, phase, gitleaks_config
        )
    transaction = _start_transaction(root)
    try:
        for index, operation in enumerate(prepared):
            transaction.operations.append(
                _create_transaction_operation(transaction, operation, index)
            )
        _install_targets(transaction)
        _verify_all_targets(transaction)
        for index, operation in enumerate(transaction.operations):
            _verify_all_targets(transaction)
            _quarantine_source(transaction, operation, index)
        _commit_transaction(transaction)
    except (OSError, subprocess.TimeoutExpired, MigrationAbort) as exc:
        if transaction.commit_started:
            if transaction.quarantine_fd >= 0:
                _close_transaction_fds(transaction)
                try:
                    _preserve_recovery(transaction)
                except MigrationAbort as recovery_error:
                    exc.add_note(str(recovery_error))
            raise MigrationAbort("MIGRATION-ROLLBACK:COMMIT-CLEANUP") from exc
        try:
            rollback_ok = _rollback_transaction(transaction)
        except MigrationAbort as rollback_error:
            exc.add_note(str(rollback_error))
            if isinstance(exc, MigrationAbort):
                raise exc
            raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
        if not rollback_ok or transaction.replacement_detected:
            raise MigrationAbort("MIGRATION-ROLLBACK") from exc
        if isinstance(exc, MigrationAbort):
            raise
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc


def build_manifest(root: Path) -> dict[str, Any]:
    root = root.resolve()
    commit = EXPECTED_SOURCE_COMMIT
    if _git(root, "cat-file", "-t", commit) != "commit":
        raise MigrationAbort("MIGRATION-SOURCE-COMMIT")
    paths = _git(
        root,
        "ls-files",
        "--",
        "docs/04.execution/plans",
        "docs/04.execution/tasks",
        "docs/03.specs",
    ).splitlines()
    sources = [p for p in paths if p.startswith("docs/04.execution/") and not p.endswith("/README.md")]
    pinned_paths = _git(
        root,
        "ls-tree",
        "-r",
        "--name-only",
        commit,
        "--",
        "docs/04.execution/plans",
        "docs/04.execution/tasks",
    ).splitlines()
    pinned_sources = sorted(
        path
        for path in pinned_paths
        if path.startswith("docs/04.execution/")
        and not path.endswith("/README.md")
    )
    if sorted(sources) != pinned_sources:
        raise MigrationAbort("MIGRATION-CENSUS")
    specs: dict[str, str] = {}
    for path in paths:
        if not path.startswith("docs/03.specs/") or not path.endswith("/spec.md"):
            continue
        directory = path.split("/")[2]
        slug = directory.split("-", 1)[1]
        if slug in specs:
            raise MigrationAbort(f"MIGRATION-DUPLICATE-SLUG:{slug}")
        specs[slug] = directory
    by_kind: dict[str, dict[str, str]] = {"plans": {}, "tasks": {}}
    for source in sources:
        match = DATE_SLUG.fullmatch(PurePosixPath(source).name)
        if match is None:
            raise MigrationAbort(f"MIGRATION-UNREVIEWED-NAME:{source}")
        kind = source.split("/")[2]
        slug = match.group("slug")
        if slug in by_kind[kind]:
            raise MigrationAbort(f"MIGRATION-DUPLICATE-SLUG:{kind}:{slug}")
        by_kind[kind][slug] = source
    triads = sorted(set(specs) & set(by_kind["plans"]) & set(by_kind["tasks"]))
    rows = []
    for slug in triads:
        spec_dir = specs[slug]
        number = spec_dir.split("-", 1)[0]
        for kind, target_name in (("plans", "plan.md"), ("tasks", "tasks.md")):
            source = by_kind[kind][slug]
            rows.append({"source": source, "target": f"docs/03.specs/{spec_dir}/{target_name}", "workUnit": f"Spec-{number}", "disposition": "move-current", "sourceBlob": _git(root, "rev-parse", f"{commit}:{source}"), "reviewed": True})
    used = {row["source"] for row in rows}
    for source in sorted(set(sources) - used):
        suffix = source.removeprefix("docs/04.execution/")
        slug = DATE_SLUG.fullmatch(PurePosixPath(source).name).group("slug")
        kind = source.split("/")[2][:-1]
        rows.append({"source": source, "target": f"docs/98.archive/04.execution/{suffix}", "workUnit": f"Archive-unique-{kind}-{slug}", "disposition": "archive-unique", "sourceBlob": _git(root, "rev-parse", f"{commit}:{source}"), "reviewed": True})
    first_source = "docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md"
    rows.sort(key=lambda row: (row["source"] != first_source, row["source"]))
    manifest = {"state": "transition", "sourceCommit": commit, "entries": rows}
    validate_manifest_data(root, manifest, True)
    return manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=Path("scripts/document-taxonomy-migration.json"))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--phase", choices=tuple(PHASE_DISPOSITION))
    parser.add_argument("--apply", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.apply != (args.phase is not None):
            raise MigrationAbort("MIGRATION-CLI:phase-and-apply-required")
        if sum((args.check, args.apply)) != 1:
            raise MigrationAbort("MIGRATION-CLI:choose-one-operation")
        if args.manifest != Path(MANIFEST_PATH.as_posix()):
            raise MigrationAbort("MIGRATION-CLI:manifest-path")
        manifest_path = args.root / args.manifest
        document = load_manifest_document(manifest_path)
        source_commit, entries = document.source_commit, document.entries
        if source_commit != EXPECTED_SOURCE_COMMIT:
            raise MigrationAbort("MIGRATION-SOURCE-COMMIT:unexpected")
        if args.apply:
            dirty = _controlled_dirty(args.root.resolve(), entries)
            if dirty:
                raise MigrationAbort(f"MIGRATION-CONTROLLED-DIRTY:{dirty[0]}")
        diagnostics = validate_manifest(args.root, entries, EXPECTED_SOURCE_COMMIT)
        if diagnostics:
            raise MigrationAbort(diagnostics[0])
        moves = sum(row["disposition"] == "move-current" for row in entries)
        archives = sum(row["disposition"] == "archive-unique" for row in entries)
        validate_counts(move_count=moves, archive_count=archives, source_count=len(entries))
        plan = MigrationPlan(len(entries), moves, archives)
        if args.apply:
            planned_pairs = plan_phase(args.root, entries, args.phase)
            apply_phase(args.root, planned_pairs, args.phase)
    except MigrationAbort as exc:
        print(f"FAIL document migration: {exc}")
        return 1
    action = f" phase={args.phase}" if args.apply else ""
    handoff = (
        f" archive_index_handoff={ARCHIVE_INDEX_HANDOFF}"
        if args.apply and args.phase == "archive"
        else ""
    )
    print(
        f"PASS document migration:{action} moves={plan.move_count} "
        f"archives={plan.archive_count} sources={plan.source_count}{handoff}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
