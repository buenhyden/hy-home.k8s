#!/usr/bin/env python3
"""Build and validate the reviewed Stage 04 document migration manifest."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping, Sequence

try:
    from archive_recovery import (
        ArchiveContractError,
        parse_archive_envelope,
        recover_git_blob,
    )
except ModuleNotFoundError:  # Imported as a repository-root test module.
    from scripts.archive_recovery import (
        ArchiveContractError,
        parse_archive_envelope,
        recover_git_blob,
    )


OID = re.compile(r"[0-9a-f]{40}\Z")
DATE_SLUG = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-(?P<slug>[A-Za-z0-9][A-Za-z0-9._-]*)\.md\Z")
ENTRY_KEYS = {"source", "target", "workUnit", "disposition", "sourceBlob", "reviewed"}
TOP_KEYS = {"state", "sourceCommit", "entries"}
EXPECTED_SOURCE_COMMIT = "713dff1fc3de58a2d1682970a7f24faa39c14263"  # pragma: allowlist secret
PHASE_DISPOSITION = {"archive": "archive-unique", "move": "move-current"}


class MigrationAbort(RuntimeError):
    pass


@dataclass(frozen=True)
class MigrationPlan:
    source_count: int
    move_count: int
    archive_count: int


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
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


def _load_manifest_document(path: Path) -> tuple[str, tuple[Mapping[str, Any], ...]]:
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
    return commit, tuple(immutable)


def load_manifest(path: Path) -> tuple[Mapping[str, Any], ...]:
    """Load the reviewed entries into an immutable ordered representation."""
    return _load_manifest_document(path)[1]


def validate_counts(*, move_count: int, archive_count: int, source_count: int) -> None:
    if (move_count, archive_count, source_count) != (82, 50, 132):
        raise MigrationAbort("MIGRATION-COUNTS:expected=82/50/132")


def validate_work_unit_paths(work_units: Mapping[str, set[str]]) -> tuple[str, ...]:
    diagnostics = []
    for unit, names in sorted(work_units.items()):
        if ("plan.md" in names or "tasks.md" in names) and "spec.md" not in names:
            diagnostics.append(f"WORK-UNIT-MISSING-SPEC:{unit}")
        elif "tasks.md" in names and "plan.md" not in names:
            diagnostics.append(f"WORK-UNIT-MISSING-PLAN:{unit}")
    return tuple(diagnostics)


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
        source_exists = (root / source).is_file()
        target_exists = (root / target).exists()
        if source_exists and target_exists:
            diagnostics.append(f"MIGRATION-DUPLICATE-ACTIVE-OWNER:{source_name}")
        elif not source_exists and not target_exists:
            diagnostics.append(f"MIGRATION-MISSING-ENDPOINT:{source_name}")
        else:
            active_path = source if source_exists else target
            if not (root / active_path).is_file():
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
            if match is None or target.name not in {"plan.md", "tasks.md"}:
                diagnostics.append(f"MIGRATION-WORK-UNIT:{source_name}")
            else:
                unit = match.group(1)
                work_units.setdefault(unit, {"spec.md"}).add(target.name)
                if not (root / target.parent / "spec.md").is_file():
                    diagnostics.append(f"MIGRATION-WORK-UNIT-SPEC:{unit}")
        elif not target_name.startswith("docs/98.archive/04.execution/"):
            diagnostics.append(f"MIGRATION-ARCHIVE-TARGET:{target_name}")
    diagnostics.extend(validate_work_unit_paths(work_units))
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


def apply_phase(
    root: Path,
    planned_pairs: Sequence[tuple[PurePosixPath | Path, PurePosixPath | Path]],
    phase: str,
) -> None:
    """Apply an already planned phase only after an atomic full-pair preflight."""
    if phase not in PHASE_DISPOSITION:
        raise MigrationAbort("MIGRATION-PHASE")
    root = root.resolve()
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
        if phase == "archive" and not target_name.startswith("docs/98.archive/04.execution/"):
            raise MigrationAbort(f"MIGRATION-ARCHIVE-TARGET:{target_name}")
        if phase == "move" and (not target_name.startswith("docs/03.specs/") or target.name not in {"plan.md", "tasks.md"}):
            raise MigrationAbort(f"MIGRATION-WORK-UNIT:{target_name}")
        if not (root / source).is_file() or (root / target).exists():
            raise MigrationAbort(f"MIGRATION-PHASE-ENDPOINT:{source_name}")
        if _ancestor_is_file(root, target):
            raise MigrationAbort(f"MIGRATION-TARGET-ANCESTOR:{target_name}")
        checked.append((source, target))
    status_entries = tuple(
        MappingProxyType({"source": source.as_posix(), "target": target.as_posix()})
        for source, target in checked
    )
    dirty = _controlled_dirty(root, status_entries)
    if dirty:
        raise MigrationAbort(f"MIGRATION-CONTROLLED-DIRTY:{dirty[0]}")
    for source, target in checked:
        (root / target).parent.mkdir(parents=True, exist_ok=True)
        (root / source).rename(root / target)


def build_manifest(root: Path) -> dict[str, Any]:
    root = root.resolve()
    commit = _git(root, "rev-parse", "HEAD")
    paths = _git(root, "ls-files", "docs/04.execution/plans/*.md", "docs/04.execution/tasks/*.md", "docs/03.specs/*/spec.md").splitlines()
    sources = [p for p in paths if p.startswith("docs/04.execution/") and not p.endswith("/README.md")]
    specs = {p.split("/")[2].split("-", 1)[1]: p.split("/")[2] for p in paths if p.startswith("docs/03.specs/")}
    by_kind: dict[str, dict[str, str]] = {"plans": {}, "tasks": {}}
    for source in sources:
        match = DATE_SLUG.fullmatch(PurePosixPath(source).name)
        if match is None:
            raise MigrationAbort(f"MIGRATION-UNREVIEWED-NAME:{source}")
        by_kind[source.split("/")[2]][match.group("slug")] = source
    triads = sorted(set(specs) & set(by_kind["plans"]) & set(by_kind["tasks"]))
    rows = []
    for slug in triads:
        spec_dir = specs[slug]; number = spec_dir.split("-", 1)[0]
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
        manifest_path = args.root / args.manifest
        source_commit, entries = _load_manifest_document(manifest_path)
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
    print(f"PASS document migration:{action} moves={plan.move_count} archives={plan.archive_count} sources={plan.source_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
