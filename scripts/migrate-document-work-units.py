#!/usr/bin/env python3
"""Build and validate the reviewed Stage 04 document migration manifest."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from dataclasses import dataclass
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


def load_manifest_document(path: Path) -> ManifestDocument:
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise MigrationAbort("MIGRATION-JSON-DUPLICATE")
            out[key] = value
        return out
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    except (OSError, json.JSONDecodeError) as exc:
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


def _run_gitleaks(executable: Path, root: Path, payload: bytes) -> int:
    try:
        completed = subprocess.run(
            [
                str(executable),
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
            env={"LC_ALL": "C"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MigrationAbort("MIGRATION-SECRET-CLASSIFIER-ERROR") from exc
    return completed.returncode


def _classify_secret_payload(root: Path, archive_path: str, payload: bytes) -> None:
    executable = _gitleaks_executable(root)
    if executable is None:
        raise MigrationAbort(
            f"MIGRATION-SECRET-CLASSIFIER-UNAVAILABLE:{archive_path}"
        )
    return_code = _run_gitleaks(executable, root, payload)
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
) -> tuple[str, tuple[Mapping[str, Any], ...]]:
    _validate_control_surface(root, MANIFEST_PATH)
    _validate_control_surface(root, GITLEAKS_CONFIG_PATH)
    document = load_manifest_document(root / MANIFEST_PATH)
    if document.source_commit != EXPECTED_SOURCE_COMMIT:
        raise MigrationAbort("MIGRATION-SOURCE-COMMIT:unexpected")
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
    return document.source_commit, rows


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


def _validate_control_surface(root: Path, path: PurePosixPath) -> None:
    absolute = root / path
    try:
        metadata = absolute.lstat()
        if absolute.resolve(strict=True) != absolute:
            raise MigrationAbort(f"MIGRATION-CONTROL-SURFACE:{path.as_posix()}")
    except (OSError, RuntimeError) as exc:
        raise MigrationAbort(
            f"MIGRATION-CONTROL-SURFACE:{path.as_posix()}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise MigrationAbort(f"MIGRATION-CONTROL-SURFACE:{path.as_posix()}")
    _tracked_source_blob(root, path)
    if _git(root, "status", "--porcelain=v1", "--", path.as_posix()):
        raise MigrationAbort(f"MIGRATION-CONTROL-DIRTY:{path.as_posix()}")


def _prepare_operations(
    root: Path,
    rows: Sequence[Mapping[str, Any]],
    source_commit: str,
    phase: str,
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
            source_bytes = source_path.read_bytes()
        except OSError as exc:
            raise MigrationAbort(f"MIGRATION-SOURCE-READ:{source_name}") from exc
        if phase == "archive":
            try:
                recovered = recover_git_blob(root, source_name, source_commit)
                if recovered.source_blob != expected_blob:
                    raise MigrationAbort(f"MIGRATION-SOURCE-BLOB:{source_name}")
                _classify_secret_payload(root, target_name, recovered.source_bytes)
                metadata = _archive_metadata(row, recovered)
                output = render_archive_envelope(
                    metadata, recovered, recovered.source_bytes
                )
                parse_archive_envelope(output, expected=recovered)
            except ArchiveContractError as exc:
                raise MigrationAbort(
                    f"MIGRATION-ARCHIVE-METADATA:{target_name}"
                ) from exc
            target_mode = 0o644
        else:
            output = source_bytes
            target_mode = stat.S_IMODE(source_metadata.st_mode)
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


def _ensure_parent(path: Path, root: Path, created: list[Path]) -> None:
    relative = path.relative_to(root)
    current = root
    for part in relative.parts:
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            current.mkdir()
            created.append(current)
            continue
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise MigrationAbort("MIGRATION-TARGET-ANCESTOR")


def _stage_output(operation: _PreparedOperation, root: Path) -> Path:
    target_parent = (root / operation.target).parent
    raw_path: str | None = None
    try:
        descriptor, raw_path = tempfile.mkstemp(
            prefix=".migration-", dir=target_parent
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(operation.output)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(raw_path, operation.target_mode)
    except OSError as exc:
        if raw_path is not None:
            try:
                Path(raw_path).unlink(missing_ok=True)
            except OSError:
                raise MigrationAbort("MIGRATION-ROLLBACK") from exc
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
    return Path(raw_path)


def _cleanup_paths(paths: Sequence[Path]) -> bool:
    clean = True
    for path in reversed(tuple(paths)):
        try:
            if path.exists() or path.is_symlink():
                path.unlink()
        except OSError:
            clean = False
    return clean


def _restore_source(operation: _PreparedOperation, root: Path) -> bool:
    source_path = root / operation.source
    raw_path: str | None = None
    try:
        descriptor, raw_path = tempfile.mkstemp(
            prefix=".migration-rollback-", dir=source_path.parent
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(operation.source_bytes)
        os.chmod(raw_path, operation.source_mode)
        os.replace(raw_path, source_path)
    except (OSError, MigrationAbort, ArchiveContractError):
        if raw_path is not None:
            try:
                Path(raw_path).unlink(missing_ok=True)
            except OSError:
                return False
        return False
    return True


def apply_phase(
    root: Path,
    planned_pairs: Sequence[tuple[PurePosixPath | Path, PurePosixPath | Path]],
    phase: str,
) -> None:
    """Apply a manifest-exact phase with full preflight and rollback."""
    if phase not in PHASE_DISPOSITION:
        raise MigrationAbort("MIGRATION-PHASE")
    root = _canonical_root(root)
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
    source_commit, rows = _phase_manifest_rows(root, checked_tuple, phase)
    status_entries = tuple(
        MappingProxyType({"source": source.as_posix(), "target": target.as_posix()})
        for source, target in checked
    )
    dirty = _controlled_dirty(root, status_entries)
    if dirty:
        raise MigrationAbort(f"MIGRATION-CONTROLLED-DIRTY:{dirty[0]}")
    prepared = _prepare_operations(root, rows, source_commit, phase)
    created_directories: list[Path] = []
    staged: list[Path] = []
    installed: list[Path] = []
    removed_sources: list[_PreparedOperation] = []
    try:
        for operation in prepared:
            _ensure_parent((root / operation.target).parent, root, created_directories)
            staged.append(_stage_output(operation, root))
        for operation in prepared:
            source_path = root / operation.source
            try:
                metadata = source_path.lstat()
            except OSError as exc:
                raise MigrationAbort("MIGRATION-FILESYSTEM") from exc
            if (
                stat.S_ISLNK(metadata.st_mode)
                or not stat.S_ISREG(metadata.st_mode)
                or _git(root, "hash-object", "--", operation.source.as_posix())
                != operation.source_blob
            ):
                raise MigrationAbort("MIGRATION-CHANGED-SOURCE")
        for operation, temporary in zip(prepared, staged, strict=True):
            os.replace(temporary, root / operation.target)
            installed.append(root / operation.target)
        for operation in prepared:
            (root / operation.source).unlink()
            removed_sources.append(operation)
    except (OSError, subprocess.TimeoutExpired, MigrationAbort) as exc:
        rollback_ok = True
        for operation in reversed(removed_sources):
            rollback_ok = _restore_source(operation, root) and rollback_ok
        rollback_ok = _cleanup_paths(installed) and rollback_ok
        rollback_ok = _cleanup_paths(staged) and rollback_ok
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                if directory.exists():
                    rollback_ok = False
        if not rollback_ok:
            raise MigrationAbort("MIGRATION-ROLLBACK") from exc
        raise MigrationAbort("MIGRATION-FILESYSTEM") from exc


def build_manifest(root: Path) -> dict[str, Any]:
    root = root.resolve()
    commit = _git(root, "rev-parse", "HEAD")
    paths = _git(
        root,
        "ls-files",
        "--",
        "docs/04.execution/plans",
        "docs/04.execution/tasks",
        "docs/03.specs",
    ).splitlines()
    sources = [p for p in paths if p.startswith("docs/04.execution/") and not p.endswith("/README.md")]
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
            rows.append({"source": source, "target": f"docs/03.specs/{spec_dir}/{target_name}", "workUnit": f"Spec-{number}", "disposition": "move-current", "sourceBlob": _git(root, "rev-parse", f"HEAD:{source}"), "reviewed": True})
    used = {row["source"] for row in rows}
    for source in sorted(set(sources) - used):
        suffix = source.removeprefix("docs/04.execution/")
        slug = DATE_SLUG.fullmatch(PurePosixPath(source).name).group("slug")
        kind = source.split("/")[2][:-1]
        rows.append({"source": source, "target": f"docs/98.archive/04.execution/{suffix}", "workUnit": f"Archive-unique-{kind}-{slug}", "disposition": "archive-unique", "sourceBlob": _git(root, "rev-parse", f"HEAD:{source}"), "reviewed": True})
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
