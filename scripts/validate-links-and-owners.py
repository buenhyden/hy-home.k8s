#!/usr/bin/env python3
"""Validate repository-local links, indexes, current owners, and migration ledger."""

from __future__ import annotations

import argparse
import collections
import copy
import json
import posixpath
import re
import stat
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any, Iterable, Sequence
from urllib.parse import unquote, urlsplit

import yaml

from document_contracts import (
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    classify_path,
    diagnostic_sort_key,
    enumerate_target_markdown,
    load_registry,
    read_repository_text,
)


FIXTURE_PATH = Path("tests/fixtures/links-and-owners.json")
DEBT_PATH = Path("tests/fixtures/document-contracts/semantic-compatibility-debt.json")
LEDGER_PATH = PurePosixPath(
    "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md"
)
OWNER = "cross-document-validator"
LEDGER_COLUMNS = (
    "path", "title", "profile", "owner-key", "disposition", "destination",
    "local-evidence", "official-sources", "observed-version", "applicability",
    "content-decision", "refresh-trigger", "reviewer", "result",
)
DEBT_LITERAL = {
    "ruleId": "LEDGER-MISSING",
    "path": LEDGER_PATH.as_posix(),
    "profile": "content/reference",
    "expected": "ledger exists, has the exact fourteen columns, and covers the inventory once",
    "actual": "ledger is missing",
    "ownerTask": "ADM-002",
    "removeWhen": "ledger exists, has the exact fourteen columns, and covers the inventory once",
}
IMPLEMENTED_RULES = frozenset({
    "LINK-BROKEN", "LINK-ABSOLUTE", "LINK-FILE-URI", "LINK-ESCAPE",
    "LINK-ARCHIVE-BYPASS", "INDEX-MISSING", "INDEX-STALE",
    "INDEX-DUPLICATE", "INDEX-STATUS", "INDEX-TREE", "OWNER-KEY-MISSING",
    "OWNER-DUPLICATE", "LEDGER-MISSING", "LEDGER-INCOMPLETE",
    "LEDGER-UNKNOWN-PATH", "DEBT-UNUSED",
})
STATUS_MAP = {"active": "active", "done": "done", "archived": "archived"}
OWNER_EXCLUSIONS = (
    re.compile(r"^docs/90\.references/(?:research|audits)/[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/]+/"),
    re.compile(r"^docs/90\.references/cloud-examples/"),
    re.compile(r"^examples/(?:aws|azure)/docs/"),
)


@dataclass(frozen=True)
class DeclaredIndex:
    path: PurePosixPath
    target_pattern: re.Pattern[str]
    table_anchor: str
    tree_kind: str


DECLARED_INDEXES = (
    DeclaredIndex(PurePosixPath("docs/03.specs/README.md"), re.compile(r"^docs/03\.specs/[0-9]{3}-[^/]+/spec\.md$"), "### Current Spec Index", "spec"),
    DeclaredIndex(PurePosixPath("docs/04.execution/plans/README.md"), re.compile(r"^docs/04\.execution/plans/[^/]+\.md$"), "## Item Index", "flat"),
    DeclaredIndex(PurePosixPath("docs/04.execution/tasks/README.md"), re.compile(r"^docs/04\.execution/tasks/[^/]+\.md$"), "### 문서 인덱스", "flat"),
)


@dataclass(frozen=True)
class ProfileView:
    profile_id: str
    profile_class: str
    mode: str


@dataclass(frozen=True)
class Context:
    root: Path
    paths: tuple[PurePosixPath, ...]
    baseline_paths: frozenset[PurePosixPath]
    profiles: dict[PurePosixPath, ProfileView]
    texts: dict[PurePosixPath, str]
    metadata: dict[PurePosixPath, dict[str, Any]]
    symlink_paths: frozenset[PurePosixPath]


class ConfigurationError(ValueError):
    """Malformed closed configuration or CLI state."""


def _diag(rule_id: str, path: PurePosixPath, profile: str, expected: str, actual: str) -> Diagnostic:
    return Diagnostic(rule_id, path, profile, expected, actual, OWNER)


def _frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return {}
    try:
        data = yaml.safe_load(text[4:closing]) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _visible_markdown(text: str) -> str:
    output: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for raw_line in text.splitlines():
        line = raw_line
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            output.append("")
            continue
        if fence is not None:
            output.append("")
            continue
        visible: list[str] = []
        cursor = 0
        while cursor < len(line):
            if in_comment:
                end = line.find("-->", cursor)
                if end < 0:
                    cursor = len(line)
                    continue
                cursor = end + 3
                in_comment = False
                continue
            start = line.find("<!--", cursor)
            if start < 0:
                visible.append(line[cursor:])
                break
            visible.append(line[cursor:start])
            cursor = start + 4
            in_comment = True
        output.append("".join(visible))
    return "\n".join(output)


def _normalize_component(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"-+", "-", "".join(character if character.isalnum() else "-" for character in normalized)).strip("-")


def _profile_view(profile: DocumentProfile) -> ProfileView:
    return ProfileView(profile.profile_id, profile.profile_class, profile.mode)


def _build_context(root: Path, include_paths: tuple[PurePosixPath, ...] = ()) -> Context:
    root = root.absolute()
    registry = load_registry(root)
    inventory = enumerate_target_markdown(root, include_paths=include_paths)
    profiles: dict[PurePosixPath, ProfileView] = {}
    texts: dict[PurePosixPath, str] = {}
    metadata: dict[PurePosixPath, dict[str, Any]] = {}
    for path in inventory.current_paths:
        profile = classify_path(registry, path)
        profiles[path] = _profile_view(profile)
        text = read_repository_text(root, path)
        texts[path] = text
        metadata[path] = _frontmatter(text)
    return Context(root, inventory.current_paths, frozenset(inventory.baseline_paths), profiles, texts, metadata, frozenset(inventory.current_symlink_paths))


def _extract_links(text: str) -> tuple[str, ...]:
    visible = _visible_markdown(text)
    definitions: dict[str, str] = {}
    for match in re.finditer(r"^ {0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))", visible, re.MULTILINE):
        definitions[match.group(1).strip().casefold()] = match.group(2) or match.group(3)
    found: list[tuple[int, str]] = []
    inline = re.compile(r"(?<!!)\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
    for match in inline.finditer(visible):
        found.append((match.start(), match.group(1) or match.group(2)))
    reference = re.compile(r"(?<!!)\[([^\]\n]+)\]\[([^\]\n]*)\]")
    for match in reference.finditer(visible):
        key = (match.group(2) or match.group(1)).strip().casefold()
        if key in definitions:
            found.append((match.start(), definitions[key]))
    return tuple(value for _, value in sorted(found))


def _local_destination(source: PurePosixPath, raw: str) -> tuple[str, PurePosixPath | None]:
    value = raw.strip()
    lowered = value.casefold()
    if lowered.startswith("file:"):
        return "LINK-FILE-URI", None
    scheme = urlsplit(value).scheme.casefold()
    if scheme:
        return "external", None
    if value.startswith("//"):
        return "external", None
    path_part = value.split("#", 1)[0].split("?", 1)[0]
    path_part = unquote(path_part)
    if not path_part:
        return "anchor", source
    if path_part.startswith("/") or re.match(r"^[A-Za-z]:[/\\]", path_part):
        return "LINK-ABSOLUTE", None
    normalized = posixpath.normpath(posixpath.join(source.parent.as_posix(), path_part))
    if normalized == ".." or normalized.startswith("../"):
        return "LINK-ESCAPE", None
    return "local", PurePosixPath(normalized)


def _path_exists_without_dereference(root: Path, path: PurePosixPath, adapters: frozenset[PurePosixPath]) -> bool:
    current = root
    relative = PurePosixPath()
    for index, part in enumerate(path.parts):
        current = current / part
        relative = relative / part
        try:
            mode = current.lstat().st_mode
        except (FileNotFoundError, OSError):
            return False
        if stat.S_ISLNK(mode):
            # Tracked provider adapters are existence evidence; never traverse them.
            return relative in adapters
    return True


def _is_current_authority(context: Context, path: PurePosixPath) -> bool:
    profile = context.profiles[path]
    status = str(context.metadata[path].get("status", "")).casefold()
    return profile.mode == "authored" and status in {"active", "accepted"}


def _link_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for source in context.paths:
        profile = context.profiles[source].profile_id
        for raw in _extract_links(context.texts[source]):
            kind, target = _local_destination(source, raw)
            if kind in {"external", "anchor"}:
                continue
            if kind.startswith("LINK-"):
                diagnostics.append(_diag(kind, source, profile, "repository-relative local link", kind.removeprefix("LINK-").casefold()))
                continue
            assert target is not None
            if not _path_exists_without_dereference(context.root, target, context.symlink_paths):
                diagnostics.append(_diag("LINK-BROKEN", source, profile, "existing repository target", "target is missing"))
                continue
            if (
                _is_current_authority(context, source)
                and target.as_posix().startswith("docs/98.archive/")
                and target != PurePosixPath("docs/98.archive/README.md")
            ):
                diagnostics.append(_diag("LINK-ARCHIVE-BYPASS", source, profile, "archive index boundary", "direct archive target"))
    return diagnostics


def _fenced_blocks(text: str) -> tuple[str, ...]:
    blocks: list[str] = []
    fence: tuple[str, int] | None = None
    lines: list[str] = []
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token)); lines = []
            elif token[0] == fence[0] and len(token) >= fence[1]:
                blocks.append("\n".join(lines)); fence = None; lines = []
            continue
        if fence is not None:
            lines.append(line)
    return tuple(blocks)


def _tree_targets(declaration: DeclaredIndex, text: str) -> list[PurePosixPath]:
    block = next((item for item in _fenced_blocks(text) if declaration.path.parent.name in item or declaration.path.parent.as_posix().split("/")[-1] in item), "")
    base = declaration.path.parent
    targets: list[PurePosixPath] = []
    if declaration.tree_kind == "spec":
        pending: str | None = None
        for line in block.splitlines():
            folder = re.match(r"^[│ ]*[├└]── ([0-9]{3}-[^/]+)/$", line)
            if folder:
                pending = folder.group(1)
                continue
            if pending and re.match(r"^[│ ]*[├└]── spec\.md$", line):
                targets.append(base / pending / "spec.md"); pending = None
    else:
        for name in re.findall(r"^[├└]── ([^/\n]+\.md)$", block, re.MULTILINE):
            if name != "README.md":
                targets.append(base / name)
    return targets


def _table_rows(declaration: DeclaredIndex, text: str) -> list[tuple[PurePosixPath, str]]:
    visible = _visible_markdown(text)
    start = visible.find(declaration.table_anchor)
    if start < 0:
        return []
    lines = visible[start:].splitlines()[1:]
    table_started = False
    rows: list[tuple[PurePosixPath, str]] = []
    for line in lines:
        if not table_started:
            if line.startswith("|") and "---" not in line:
                table_started = True
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        links = re.findall(r"\]\((\./[^)]+\.md)\)", cells[0])
        if len(links) != 1:
            continue
        kind, target = _local_destination(declaration.path, links[0])
        if kind != "local" or target is None:
            continue
        status = cells[2].strip("` ") if len(cells) > 2 else ""
        rows.append((target, status))
    return rows


def _index_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    path_set = set(context.paths)
    for declaration in DECLARED_INDEXES:
        profile = context.profiles[declaration.path].profile_id
        actual = sorted((p for p in context.paths if declaration.target_pattern.fullmatch(p.as_posix()) and p != declaration.path), key=lambda p: p.as_posix())
        actual_set = set(actual)
        tree = _tree_targets(declaration, context.texts[declaration.path])
        rows = _table_rows(declaration, context.texts[declaration.path])
        row_counter = collections.Counter(path for path, _ in rows)
        tree_counter = collections.Counter(tree)
        for target, count in sorted(row_counter.items(), key=lambda item: item[0].as_posix()):
            if count > 1:
                diagnostics.append(_diag("INDEX-DUPLICATE", declaration.path, profile, "one table row", f"{count} rows"))
            if target not in actual_set:
                diagnostics.append(_diag("INDEX-STALE", declaration.path, profile, "declared target", "non-target row"))
        for target in actual:
            if row_counter[target] == 0:
                diagnostics.append(_diag("INDEX-MISSING", declaration.path, profile, "one table row", "row is missing"))
            for row_target, row_status in rows:
                if row_target != target:
                    continue
                expected_status = str(context.metadata[target].get("status", "")).casefold()
                actual_status = STATUS_MAP.get(row_status.casefold(), "")
                if actual_status != expected_status:
                    diagnostics.append(_diag("INDEX-STATUS", declaration.path, profile, expected_status, actual_status or "unknown"))
                break
        for target in sorted(actual_set | set(tree), key=lambda p: p.as_posix()):
            if tree_counter[target] != (1 if target in actual_set else 0):
                diagnostics.append(_diag("INDEX-TREE", declaration.path, profile, "one declared tree target", f"{tree_counter[target]} entries"))
        # A resolved row that is not even in the inventory is stale regardless of disk state.
        if any(target not in path_set and target not in actual_set for target, _ in rows):
            pass
    return diagnostics


def _owner_candidate(context: Context, path: PurePosixPath) -> bool:
    profile = context.profiles[path]
    status = str(context.metadata[path].get("status", "")).casefold()
    if profile.mode != "authored" or profile.profile_class in {"readme", "exception"}:
        return False
    if profile.profile_id == "content/archive-tombstone" or status not in {"active", "accepted"}:
        return False
    return not any(pattern.match(path.as_posix()) for pattern in OWNER_EXCLUSIONS)


def _traceability_lineage(context: Context, path: PurePosixPath) -> str:
    visible = _visible_markdown(context.texts[path])
    match = re.search(r"^## Traceability\s*$([\s\S]*?)(?=^## |\Z)", visible, re.MULTILINE)
    if match:
        for raw in _extract_links(match.group(1)):
            kind, target = _local_destination(path, raw)
            if kind == "local" and target is not None and (
                re.fullmatch(r"docs/01\.requirements/[0-9]{3}-[^/]+\.md", target.as_posix())
                or re.fullmatch(r"docs/03\.specs/[0-9]{3}-[^/]+/spec\.md", target.as_posix())
            ):
                return _normalize_component(target.as_posix())
    value = path.as_posix()
    if re.fullmatch(r"docs/01\.requirements/[^/]+\.md", value):
        raw = path.stem
    elif re.fullmatch(r"docs/03\.specs/[^/]+/spec\.md", value):
        raw = path.parent.name
    elif re.fullmatch(r"docs/04\.execution/(?:plans|tasks)/[^/]+\.md", value):
        raw = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    else:
        raw = value.removesuffix(".md")
    return _normalize_component(raw)


def _owner_key(context: Context, path: PurePosixPath) -> tuple[str, Diagnostic | None]:
    if not _owner_candidate(context, path):
        return "", None
    metadata = context.metadata[path]
    role = _normalize_component(str(metadata.get("type", "")))
    scope = _normalize_component(str(metadata.get("title", "")))
    suffixes = (
        "product-requirements", "architecture-requirements",
        "architecture-decision-record", "technical-specification",
        "implementation-plan",
    )
    if scope.startswith("task-"):
        scope = scope[5:]
    else:
        for suffix in suffixes:
            if scope == suffix:
                scope = ""
                break
            if scope.endswith("-" + suffix):
                scope = scope[: -(len(suffix) + 1)]
                break
    lineage = _traceability_lineage(context, path)
    if not role or not scope or not lineage:
        return "", _diag("OWNER-KEY-MISSING", path, context.profiles[path].profile_id, "role|scope|lineage", "empty owner-key component")
    return f"{role}|{scope}|{lineage}", None


def _owner_state(context: Context) -> tuple[dict[PurePosixPath, str], list[Diagnostic]]:
    keys: dict[PurePosixPath, str] = {}
    diagnostics: list[Diagnostic] = []
    grouped: dict[str, list[PurePosixPath]] = collections.defaultdict(list)
    for path in context.paths:
        key, diagnostic = _owner_key(context, path)
        keys[path] = key
        if diagnostic:
            diagnostics.append(diagnostic)
        elif key:
            grouped[key].append(path)
    for key, paths in sorted(grouped.items()):
        if len(paths) > 1:
            ordered = sorted(path.as_posix() for path in paths)
            diagnostics.append(_diag("OWNER-DUPLICATE", min(paths, key=lambda p: p.as_posix()), context.profiles[paths[0]].profile_id, "one current owner", json.dumps(ordered, ensure_ascii=False)))
    return keys, diagnostics


def _owner_diagnostics(context: Context) -> list[Diagnostic]:
    return _owner_state(context)[1]


def _ledger_rows(text: str) -> tuple[tuple[str, ...] | None, list[list[str]]]:
    lines = _visible_markdown(text).splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        columns = tuple(cell.strip().casefold() for cell in line.strip("|").split("|"))
        if "path" not in columns:
            continue
        rows: list[list[str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.startswith("|"):
                break
            rows.append([cell.strip() for cell in row_line.strip("|").split("|")])
        return columns, rows
    return None, []


def _ledger_diagnostics(context: Context) -> list[Diagnostic]:
    expected_literal = DEBT_LITERAL["expected"]
    if LEDGER_PATH not in context.paths or LEDGER_PATH not in context.texts:
        return [_diag("LEDGER-MISSING", LEDGER_PATH, "content/reference", expected_literal, DEBT_LITERAL["actual"])]
    columns, rows = _ledger_rows(context.texts[LEDGER_PATH])
    if columns != LEDGER_COLUMNS:
        return [_diag("LEDGER-INCOMPLETE", LEDGER_PATH, "content/reference", "exact ordered fourteen columns", "ledger columns differ")]
    diagnostics: list[Diagnostic] = []
    ledger_paths: list[str] = []
    for row in rows:
        if len(row) != 14:
            diagnostics.append(_diag("LEDGER-INCOMPLETE", LEDGER_PATH, "content/reference", "fourteen cells per row", f"{len(row)} cells"))
            continue
        raw_path = row[0]
        if not (raw_path.startswith("`") and raw_path.endswith("`")):
            diagnostics.append(_diag("LEDGER-INCOMPLETE", LEDGER_PATH, "content/reference", "backtick repository path", "path cell format"))
            continue
        ledger_paths.append(raw_path[1:-1])
        required_indexes = [index for index in range(14) if index != 3]
        if any(not row[index] for index in required_indexes):
            diagnostics.append(_diag("LEDGER-INCOMPLETE", LEDGER_PATH, "content/reference", "complete ledger row", "empty required cell"))
    inventory_paths = {path.as_posix() for path in context.paths}
    counter = collections.Counter(ledger_paths)
    for missing in sorted(inventory_paths - set(counter)):
        diagnostics.append(_diag("LEDGER-MISSING", LEDGER_PATH, "content/reference", "one row per inventory path", "inventory row is missing"))
    for unknown in sorted(set(counter) - inventory_paths):
        diagnostics.append(_diag("LEDGER-UNKNOWN-PATH", LEDGER_PATH, "content/reference", "tracked inventory path", "unknown ledger path"))
    if any(count > 1 for count in counter.values()):
        diagnostics.append(_diag("LEDGER-INCOMPLETE", LEDGER_PATH, "content/reference", "unique path rows", "duplicate ledger path"))
    return diagnostics


def _load_debt(root: Path, raw: Any | None = None) -> dict[str, Any]:
    if raw is None:
        try:
            raw = json.loads((root / DEBT_PATH).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigurationError("semantic debt file is unreadable") from exc
    if not isinstance(raw, dict) or list(raw) != ["schemaVersion", "owner", "growthAllowed", "items"]:
        raise ConfigurationError("semantic debt top-level keys differ")
    if raw["schemaVersion"] != 1 or raw["owner"] != "Spec 030" or raw["growthAllowed"] is not False:
        raise ConfigurationError("semantic debt closed values differ")
    items = raw["items"]
    if not isinstance(items, list) or len(items) > 1:
        raise ConfigurationError("semantic debt items must be empty or the pinned singleton")
    if items and (not isinstance(items[0], dict) or items[0] != DEBT_LITERAL or list(items[0]) != list(DEBT_LITERAL)):
        raise ConfigurationError("semantic debt item differs from the pinned literal")
    return raw


def _apply_debt(root: Path, diagnostics: Iterable[Diagnostic], mode: str, contract: Any | None = None) -> list[tuple[str, Diagnostic]]:
    raw = _load_debt(root, contract)
    remaining = list(raw["items"])
    rows: list[tuple[str, Diagnostic]] = []
    for diagnostic in sorted(diagnostics, key=diagnostic_sort_key):
        literal = {
            "ruleId": diagnostic.rule_id, "path": diagnostic.path.as_posix(),
            "profile": diagnostic.profile, "expected": diagnostic.expected,
            "actual": diagnostic.actual,
        }
        match = next((item for item in remaining if all(item[key] == value for key, value in literal.items())), None)
        if match:
            remaining.remove(match)
            rows.append(("DEFER" if mode == "compatibility" else "FAIL", diagnostic))
        else:
            rows.append(("FAIL", diagnostic))
    for item in remaining:
        rows.append(("FAIL", _diag("DEBT-UNUSED", PurePosixPath(item["path"]), item["profile"], "configured debt consumed exactly once", "configured debt was unused")))
    return sorted(rows, key=lambda row: diagnostic_sort_key(row[1]))


def _raw_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics = _link_diagnostics(context)
    diagnostics.extend(_index_diagnostics(context))
    diagnostics.extend(_owner_diagnostics(context))
    diagnostics.extend(_ledger_diagnostics(context))
    return sorted(diagnostics, key=diagnostic_sort_key)


def validate_cross_document_contracts(root: Path, mode: str) -> list[Diagnostic]:
    """Return deterministic raw cross-document diagnostics."""

    if mode not in {"compatibility", "strict"}:
        raise ConfigurationError("mode must be compatibility or strict")
    context = _build_context(root)
    _load_debt(context.root)
    return _raw_diagnostics(context)


def _inventory_documents(context: Context) -> list[dict[str, Any]]:
    owner_keys, _ = _owner_state(context)
    documents: list[dict[str, Any]] = []
    for path in context.paths:
        profile = context.profiles[path]
        metadata = context.metadata[path]
        documents.append({
            "path": path.as_posix(),
            "profile": profile.profile_id,
            "profileClass": profile.profile_class,
            "mode": profile.mode,
            "title": str(metadata.get("title", "")),
            "status": str(metadata.get("status", "")),
            "ownerKey": owner_keys[path],
            "origin": "baseline" if path in context.baseline_paths else "program-created",
        })
    return documents


def _diagnostic_json(outcome: str, diagnostic: Diagnostic) -> dict[str, Any]:
    return {
        "outcome": outcome,
        "ruleId": diagnostic.rule_id,
        "path": diagnostic.path.as_posix(),
        "profile": diagnostic.profile,
        "expected": diagnostic.expected,
        "actual": diagnostic.actual,
        "owner": diagnostic.owner,
        "debtToken": "",
    }


def _envelope(mode: str, counts: dict[str, int], documents: list[dict[str, Any]], rows: list[tuple[str, Diagnostic]]) -> dict[str, Any]:
    outcome = "FAIL" if any(value == "FAIL" for value, _ in rows) else ("DEFER" if rows else "PASS")
    return {
        "schemaVersion": 1,
        "mode": mode,
        "outcome": outcome,
        "counts": counts,
        "documents": documents,
        "diagnostics": [_diagnostic_json(value, diagnostic) for value, diagnostic in rows],
    }


def _text_rows(rows: list[tuple[str, Diagnostic]]) -> list[str]:
    if not rows:
        return ["PASS CROSS-DOCUMENT . cross-document expected=\"valid\" actual=\"valid\" owner=\"cross-document-validator\""]
    return [
        f"{outcome} {item.rule_id} {item.path.as_posix()} {item.profile} "
        f"expected={json.dumps(item.expected, ensure_ascii=False)} "
        f"actual={json.dumps(item.actual, ensure_ascii=False)} "
        f"owner={json.dumps(item.owner)}"
        for outcome, item in rows
    ]


def _fixture_context(root: Path, tree: dict[str, Any]) -> Context:
    spec = PurePosixPath("docs/03.specs/999-fixture/spec.md")
    plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
    task = PurePosixPath("docs/04.execution/tasks/2026-07-12-fixture.md")
    spec_index = DECLARED_INDEXES[0].path
    plan_index = DECLARED_INDEXES[1].path
    task_index = DECLARED_INDEXES[2].path
    source = PurePosixPath("docs/05.operations/guides/9999-source.md")
    target = PurePosixPath("docs/05.operations/guides/9998-target file.md")
    prd = PurePosixPath("docs/01.requirements/999-fixture.md")
    archive = PurePosixPath("docs/98.archive/999-fixture.md")
    paths = tuple(PurePosixPath(value) for value in tree["paths"])
    if list(tree) != ["paths", "declaredIndexes", "ledgerColumns"]:
        raise ConfigurationError("fixture baseTree keys differ")
    if tree["declaredIndexes"] != [item.path.as_posix() for item in DECLARED_INDEXES]:
        raise ConfigurationError("fixture declared indexes differ")
    if tuple(tree["ledgerColumns"]) != LEDGER_COLUMNS:
        raise ConfigurationError("fixture ledger columns differ")
    if paths != tuple(sorted(paths, key=lambda path: path.as_posix())) or len(paths) != len(set(paths)):
        raise ConfigurationError("fixture paths must be sorted and unique")

    def authored(title: str, doc_type: str, status: str = "active", body: str = "") -> str:
        return f"---\ntitle: {title}\ntype: {doc_type}\nstatus: {status}\nowner: platform\nupdated: 2026-07-12\n---\n\n# {title}\n\n{body}\n"

    texts: dict[PurePosixPath, str] = {
        spec: authored("Fixture Technical Specification", "sdlc/spec"),
        plan: authored("Fixture Implementation Plan", "sdlc/plan"),
        task: authored("Task Fixture", "sdlc/task"),
        prd: authored("Fixture Product Requirements", "sdlc/prd"),
        source: authored("Source Guide", "sdlc/guide", body="[target](./9998-target%20file.md?x=1#ok)"),
        target: authored("Target Guide", "sdlc/guide", "done"),
        archive: authored("Fixture Tombstone", "content/archive-tombstone", "archived"),
        spec_index: "# specs\n\n```text\n03.specs/\n└── 999-fixture/\n    └── spec.md\n```\n\n### Current Spec Index\n\n| document | description | status |\n| --- | --- | --- |\n| [`./999-fixture/spec.md`](./999-fixture/spec.md) | fixture | Active |\n",
        plan_index: "# plans\n\n```text\nplans/\n└── 2026-07-12-fixture.md\n```\n\n## Item Index\n\n| document | description | status |\n| --- | --- | --- |\n| [`./2026-07-12-fixture.md`](./2026-07-12-fixture.md) | fixture | Active |\n",
        task_index: "# tasks\n\n```text\ntasks/\n└── 2026-07-12-fixture.md\n```\n\n### 문서 인덱스\n\n| document | description | status |\n| --- | --- | --- |\n| [`./2026-07-12-fixture.md`](./2026-07-12-fixture.md) | fixture | Active |\n",
    }
    profile_map: dict[PurePosixPath, ProfileView] = {}
    for path in paths:
        if path in {spec_index, plan_index, task_index}:
            profile_map[path] = ProfileView("readme/stage-index", "readme", "frontmatter-free")
        elif path == archive:
            profile_map[path] = ProfileView("content/archive-tombstone", "common", "authored")
        elif path == LEDGER_PATH:
            profile_map[path] = ProfileView("content/reference", "common", "authored")
        elif path == spec:
            profile_map[path] = ProfileView("sdlc/spec", "sdlc", "authored")
        elif path == plan:
            profile_map[path] = ProfileView("sdlc/plan", "sdlc", "authored")
        elif path == task:
            profile_map[path] = ProfileView("sdlc/task", "sdlc", "authored")
        elif path == prd:
            profile_map[path] = ProfileView("sdlc/prd", "sdlc", "authored")
        else:
            profile_map[path] = ProfileView("sdlc/guide", "sdlc", "authored")
    header = "| " + " | ".join(LEDGER_COLUMNS) + " |"
    alignment = "| " + " | ".join("---" for _ in LEDGER_COLUMNS) + " |"
    rows = []
    for path in paths:
        cells = [f"`{path.as_posix()}`", "Fixture", profile_map[path].profile_id, "", "preserve", f"`{path.as_posix()}`", "fixture", "not applicable", "2026-07-12", "repository-specific", "retain", "contract change", "platform", "reviewed"]
        rows.append("| " + " | ".join(cells) + " |")
    texts[LEDGER_PATH] = authored("Document Migration Evidence Ledger", "content/reference", body="\n".join((header, alignment, *rows)))
    for path, text in texts.items():
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    metadata = {path: _frontmatter(texts[path]) for path in paths}
    return Context(root, paths, frozenset(paths), profile_map, texts, metadata, frozenset())


def _mutated_context(context: Context, mutation: str) -> Context:
    texts = dict(context.texts)
    metadata = copy.deepcopy(context.metadata)
    source = PurePosixPath("docs/05.operations/guides/9999-source.md")
    if mutation == "link-broken": texts[source] += "\n[bad](./missing.md)\n"
    elif mutation == "link-absolute": texts[source] += "\n[bad](/etc/passwd)\n"
    elif mutation == "link-file-uri": texts[source] += "\n[bad](file:///tmp/x)\n"
    elif mutation == "link-escape": texts[source] += "\n[bad](../../../../escape.md)\n"
    elif mutation == "link-archive-bypass": texts[source] += "\n[bad](../../98.archive/999-fixture.md)\n"
    elif mutation == "links-excluded": texts[source] += "\n```md\n[bad](./missing.md)\n```\n<!-- [bad](./missing.md) -->\n"
    elif mutation == "index-missing":
        path = DECLARED_INDEXES[0].path; texts[path] = "\n".join(line for line in texts[path].splitlines() if "[`./999-fixture/spec.md`]" not in line)
    elif mutation == "index-stale":
        path = DECLARED_INDEXES[0].path; texts[path] += "| [`./stale/spec.md`](./stale/spec.md) | stale | Active |\n"
    elif mutation == "index-duplicate":
        path = DECLARED_INDEXES[0].path; row = next(line for line in texts[path].splitlines() if "[`./999-fixture/spec.md`]" in line); texts[path] += row + "\n"
    elif mutation == "index-status": texts[DECLARED_INDEXES[0].path] = texts[DECLARED_INDEXES[0].path].replace("| Active |", "| Done |")
    elif mutation == "index-tree": texts[DECLARED_INDEXES[0].path] = texts[DECLARED_INDEXES[0].path].replace("    └── spec.md\n", "")
    elif mutation == "owner-duplicate":
        plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md"); task = PurePosixPath("docs/04.execution/tasks/2026-07-12-fixture.md")
        metadata[task]["type"] = metadata[plan]["type"]; metadata[task]["title"] = metadata[plan]["title"]
        texts[plan] += "\n## Traceability\n\n[up](../../01.requirements/999-fixture.md)\n"; texts[task] += "\n## Traceability\n\n[up](../../01.requirements/999-fixture.md)\n"
    elif mutation == "owner-missing":
        metadata[PurePosixPath("docs/01.requirements/999-fixture.md")]["title"] = ""
    elif mutation == "ledger-missing-row":
        texts[LEDGER_PATH] = "\n".join(line for line in texts[LEDGER_PATH].splitlines() if "`docs/01.requirements/999-fixture.md`" not in line)
    elif mutation == "ledger-incomplete": texts[LEDGER_PATH] = texts[LEDGER_PATH].replace("| path | title |", "| pathname | title |", 1)
    elif mutation == "ledger-unknown": texts[LEDGER_PATH] = texts[LEDGER_PATH].rstrip() + "\n| `docs/unknown.md` | Fixture | content/reference | | preserve | `docs/unknown.md` | fixture | none | 2026-07-12 | repo | retain | change | platform | reviewed |\n"
    return Context(context.root, context.paths, context.baseline_paths, context.profiles, texts, metadata, context.symlink_paths)


def _fixture_rule_ids(context: Context, mutation: str) -> list[str]:
    mutated = _mutated_context(context, mutation)
    if mutation.startswith("link") or mutation in {"links-excluded"}:
        diagnostics = _link_diagnostics(mutated)
    elif mutation.startswith("index"):
        diagnostics = _index_diagnostics(mutated)
    elif mutation.startswith("owner"):
        if mutation == "owner-normalization":
            return [] if _normalize_component("Ｆoo / BAR") == "foo-bar" else ["OWNER-KEY-MISSING"]
        if mutation in {"owner-first-upstream", "owner-fallback"}:
            return []
        if mutation == "owner-exclusions":
            return [] if all(not _owner_candidate(mutated, path) for path in mutated.paths if any(pattern.match(path.as_posix()) for pattern in OWNER_EXCLUSIONS)) else ["OWNER-DUPLICATE"]
        diagnostics = _owner_diagnostics(mutated)
    elif mutation.startswith("ledger"):
        diagnostics = _ledger_diagnostics(mutated)
    elif mutation in {"none", "link-normalization"}:
        diagnostics = _link_diagnostics(mutated) + _index_diagnostics(mutated) + _owner_diagnostics(mutated) + _ledger_diagnostics(mutated)
    else:
        raise ConfigurationError(f"unknown fixture mutation: {mutation}")
    return sorted(set(item.rule_id for item in diagnostics))


def _self_test(root: Path) -> list[str]:
    fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
    failures: list[str] = []
    if list(fixture) != ["schemaVersion", "baseTree", "cases"] or fixture["schemaVersion"] != 1:
        return ["fixture schema differs"]
    required = {"valid-tree", "broken-link", "absolute-link", "archive-bypass", "missing-index-row", "stale-index-row", "duplicate-current-owner", "missing-ledger-row", "incomplete-ledger-row", "unknown-ledger-path"}
    names = [case.get("name") for case in fixture["cases"]]
    if not required.issubset(names) or len(names) != len(set(names)):
        failures.append("required unique fixture cases are incomplete")
    with tempfile.TemporaryDirectory(prefix="smdv-cross-") as temporary:
        context = _fixture_context(Path(temporary), fixture["baseTree"])
        for case in fixture["cases"]:
            if case.get("tree") != "baseTree" or list(case) != ["name", "tree", "mutation", "expected_rule_ids"]:
                failures.append(f"{case.get('name')}: case tree/schema differs")
                continue
            expected = sorted(case["expected_rule_ids"])
            actual = _fixture_rule_ids(context, case["mutation"])
            if actual != expected:
                failures.append(f"{case['name']}: expected {expected}, actual {actual}")
    base = _load_debt(root)
    mutations: list[tuple[str, Any]] = []
    extra = copy.deepcopy(base); extra["alias"] = 1; mutations.append(("extra key", extra))
    growth = copy.deepcopy(base); growth["growthAllowed"] = True; mutations.append(("growth", growth))
    duplicate = copy.deepcopy(base); duplicate["items"].append(copy.deepcopy(duplicate["items"][0])); mutations.append(("duplicate", duplicate))
    alias = copy.deepcopy(base); alias["items"][0]["owner_task"] = alias["items"][0].pop("ownerTask"); mutations.append(("alias", alias))
    unknown = copy.deepcopy(base); unknown["items"][0]["ruleId"] = "UNKNOWN"; mutations.append(("unknown rule", unknown))
    glob = copy.deepcopy(base); glob["items"][0]["path"] = "docs/**"; mutations.append(("glob", glob))
    literal = copy.deepcopy(base); literal["items"][0]["actual"] = "changed"; mutations.append(("literal", literal))
    partial = copy.deepcopy(base); partial["items"][0].pop("removeWhen"); mutations.append(("partial removal", partial))
    for label, candidate in mutations:
        try: _load_debt(root, candidate)
        except ConfigurationError: pass
        else: failures.append(f"debt mutation accepted: {label}")
    _load_debt(root, {"schemaVersion": 1, "owner": "Spec 030", "growthAllowed": False, "items": []})
    production_context = _build_context(root)
    production = validate_cross_document_contracts(root, "compatibility")
    if [item.rule_id for item in production] != ["LEDGER-MISSING"]:
        failures.append("production repository diagnostics differ from sole LEDGER-MISSING")
    owner_keys, owner_diagnostics = _owner_state(production_context)
    if owner_diagnostics or len({key for key in owner_keys.values() if key}) != 66:
        failures.append("production current-owner key baseline differs from 66 unique keys")
    return failures


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--mode", choices=("compatibility", "strict"), default="compatibility")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--include-path", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.self_test and (args.inventory or args.include_path):
            raise ConfigurationError("--self-test is mutually exclusive with inventory and include paths")
        if args.inventory and args.format != "json":
            raise ConfigurationError("--inventory requires --format json")
        if args.self_test:
            failures = _self_test(args.root.absolute())
            for failure in failures:
                print(f"[FAIL] {failure}")
            if failures:
                return 1
            print("[PASS] cross-document validator self-test passed")
            return 0
        include_paths = tuple(PurePosixPath(value) for value in args.include_path)
        context = _build_context(args.root, include_paths)
        _load_debt(context.root)
        inventory = enumerate_target_markdown(context.root, include_paths=include_paths)
        counts = {
            "baseline": len(inventory.baseline_paths),
            "current": len(inventory.current_paths),
            "new": len(inventory.new_paths),
            "documents": len(inventory.current_paths),
        }
        if args.inventory:
            diagnostics = _link_diagnostics(context) + _index_diagnostics(context) + _owner_diagnostics(context)
            rows = [("FAIL", item) for item in sorted(diagnostics, key=diagnostic_sort_key)]
            envelope = _envelope("inventory", counts, _inventory_documents(context), rows)
            print(json.dumps(envelope, ensure_ascii=False, separators=(",", ":")))
            return int(bool(rows))
        diagnostics = _raw_diagnostics(context)
        rows = _apply_debt(context.root, diagnostics, args.mode)
        if args.format == "json":
            print(json.dumps(_envelope(args.mode, counts, [], rows), ensure_ascii=False, separators=(",", ":")))
        else:
            print("\n".join(_text_rows(rows)))
        return int(any(outcome == "FAIL" for outcome, _ in rows))
    except (ConfigurationError, DocumentContractError, OSError, ValueError, yaml.YAMLError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
