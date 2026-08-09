#!/usr/bin/env python3
"""Build and validate the reviewed Stage 04 document migration manifest."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


OID = re.compile(r"[0-9a-f]{40}\Z")
DATE_SLUG = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-(?P<slug>[A-Za-z0-9][A-Za-z0-9._-]*)\.md\Z")
ENTRY_KEYS = {"source", "target", "workUnit", "disposition", "sourceBlob", "reviewed"}
TOP_KEYS = {"state", "sourceCommit", "entries"}


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


def load_manifest(path: Path) -> Any:
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise MigrationAbort("MIGRATION-JSON-DUPLICATE")
            out[key] = value
        return out
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    except (OSError, json.JSONDecodeError) as exc:
        raise MigrationAbort("MIGRATION-JSON") from exc


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


def validate_manifest_data(root: Path, data: Any, require_closed_counts: bool = True) -> MigrationPlan:
    root = root.resolve()
    if not isinstance(data, Mapping) or set(data) != TOP_KEYS or data.get("state") != "transition":
        raise MigrationAbort("MIGRATION-SCHEMA")
    commit = data.get("sourceCommit")
    if not isinstance(commit, str) or OID.fullmatch(commit) is None:
        raise MigrationAbort("MIGRATION-SOURCE-COMMIT")
    if _git(root, "cat-file", "-t", commit) != "commit":
        raise MigrationAbort("MIGRATION-SOURCE-COMMIT")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        raise MigrationAbort("MIGRATION-ENTRIES")
    sources, targets = set(), set()
    moves = archives = 0
    work_units: dict[str, set[str]] = {}
    for row in entries:
        if not isinstance(row, Mapping) or set(row) != ENTRY_KEYS or row.get("reviewed") is not True:
            raise MigrationAbort("MIGRATION-ENTRY-SCHEMA")
        source, target = _safe_path(row["source"]), _safe_path(row["target"])
        if source.as_posix() in sources:
            raise MigrationAbort("MIGRATION-DUPLICATE-SOURCE")
        if target.as_posix() in targets:
            raise MigrationAbort("MIGRATION-DUPLICATE-TARGET")
        sources.add(source.as_posix()); targets.add(target.as_posix())
        disposition = row.get("disposition")
        if disposition not in {"move-current", "archive-unique"}:
            raise MigrationAbort("MIGRATION-DISPOSITION")
        expected_blob = row.get("sourceBlob")
        if not isinstance(expected_blob, str) or OID.fullmatch(expected_blob) is None:
            raise MigrationAbort("MIGRATION-SOURCE-BLOB")
        if _git(root, "rev-parse", f"{commit}:{source.as_posix()}") != expected_blob:
            raise MigrationAbort("MIGRATION-SOURCE-BLOB")
        source_exists, target_exists = (root / source).is_file(), (root / target).exists()
        if source_exists and target_exists:
            raise MigrationAbort("MIGRATION-DUPLICATE-ACTIVE-OWNER")
        if not source_exists and not target_exists:
            raise MigrationAbort("MIGRATION-MISSING-ENDPOINT")
        if source_exists and _git(root, "hash-object", "--", source.as_posix()) != expected_blob:
            raise MigrationAbort("MIGRATION-CHANGED-SOURCE")
        if _ancestor_is_file(root, target):
            raise MigrationAbort("MIGRATION-TARGET-ANCESTOR")
        if disposition == "move-current":
            moves += 1
            match = re.fullmatch(r"Spec-([0-9]{3})", str(row.get("workUnit")))
            if match is None or target.name not in {"plan.md", "tasks.md"}:
                raise MigrationAbort("MIGRATION-WORK-UNIT")
            unit = match.group(1)
            work_units.setdefault(unit, {"spec.md"}).add(target.name)
            if not (root / target.parent / "spec.md").is_file():
                raise MigrationAbort("MIGRATION-WORK-UNIT-SPEC")
        else:
            archives += 1
            if not target.as_posix().startswith("docs/98.archive/04.execution/"):
                raise MigrationAbort("MIGRATION-ARCHIVE-TARGET")
    diagnostics = validate_work_unit_paths(work_units)
    if diagnostics:
        raise MigrationAbort(diagnostics[0])
    plan = MigrationPlan(len(entries), moves, archives)
    if require_closed_counts:
        validate_counts(move_count=moves, archive_count=archives, source_count=len(entries))
    return plan


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=Path("scripts/document-taxonomy-migration.json"))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    try:
        if args.build:
            data = build_manifest(args.root)
            target = args.root / args.manifest
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        data = load_manifest(args.root / args.manifest)
        plan = validate_manifest_data(args.root, data, True)
    except MigrationAbort as exc:
        print(f"FAIL document migration: {exc}")
        return 1
    print(f"PASS document migration: moves={plan.move_count} archives={plan.archive_count} sources={plan.source_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
