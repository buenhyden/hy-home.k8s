#!/usr/bin/env python3
"""Validate repository-local links, indexes, current owners, and migration ledger."""

from __future__ import annotations

import argparse
import collections
import contextlib
import copy
import io
import json
import os
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
    "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
    "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE", "GOVERNANCE-OWNER-STATUS",
    "GOVERNANCE-OWNER-UNDECLARED", "GOVERNANCE-OWNER-ROUTE",
    "GOVERNANCE-INDEX-MISSING", "GOVERNANCE-INDEX-STALE",
    "GOVERNANCE-INDEX-DUPLICATE", "GOVERNANCE-INDEX-STATUS",
    "GOVERNANCE-INDEX-ORDER",
})
GOVERNANCE_CURRENT_README = PurePosixPath("docs/00.agent-governance/README.md")
GOVERNANCE_CURRENT_HEADING = "### Current Governance Authority Index"
FIXTURE_GOVERNANCE_PATHS = (
    PurePosixPath("docs/00.agent-governance/current-alpha.md"),
    PurePosixPath("docs/00.agent-governance/current-beta.md"),
)
STATUS_MAP = {"active": "active", "done": "done", "archived": "archived"}
OWNER_EXCLUSIONS = (
    re.compile(r"^docs/90\.references/(?:research|audits)/[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/]+/"),
    re.compile(r"^docs/90\.references/cloud-examples/"),
    re.compile(r"^examples/(?:aws|azure)/docs/"),
)
SMDV_CLOSURE_PATHS = (
    PurePosixPath("docs/03.specs/029-semantic-document-validation/spec.md"),
    PurePosixPath(
        "docs/04.execution/plans/2026-07-12-semantic-document-validation.md"
    ),
    PurePosixPath(
        "docs/04.execution/tasks/2026-07-12-semantic-document-validation.md"
    ),
)
ADM_CLOSURE_PATHS = (
    PurePosixPath("docs/03.specs/030-authored-document-migration/spec.md"),
    PurePosixPath(
        "docs/04.execution/plans/2026-07-12-authored-document-migration.md"
    ),
    PurePosixPath(
        "docs/04.execution/tasks/2026-07-12-authored-document-migration.md"
    ),
)
@dataclass(frozen=True)
class DeclaredIndex:
    path: PurePosixPath
    target_pattern: re.Pattern[str]
    tree_anchor: str
    tree_root: str
    table_anchor: str
    table_mode: str
    tree_kind: str


DECLARED_INDEXES = (
    DeclaredIndex(PurePosixPath("docs/03.specs/README.md"), re.compile(r"^docs/03\.specs/[0-9]{3}-[^/]+/spec\.md$"), "## Document Index", "03.specs/", "### Current Spec Index", "section", "spec"),
    DeclaredIndex(PurePosixPath("docs/04.execution/plans/README.md"), re.compile(r"^docs/04\.execution/plans/[^/]+\.md$"), "## Item Index", "04.execution/plans/", "## Item Index", "after", "flat"),
    DeclaredIndex(PurePosixPath("docs/04.execution/tasks/README.md"), re.compile(r"^docs/04\.execution/tasks/[^/]+\.md$"), "## Item Index", "04.execution/tasks/", "### 문서 인덱스", "section", "flat"),
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
    adapter_targets: dict[PurePosixPath, PurePosixPath]
    governance_current_paths: tuple[PurePosixPath, ...]
    governance_current_states: tuple[str, ...]


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
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not marker.group(2).strip():
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
    adapters: dict[PurePosixPath, PurePosixPath] = {}
    for adapter in inventory.current_symlink_paths:
        raw_target = os.readlink(root / adapter)
        normalized = posixpath.normpath(posixpath.join(adapter.parent.as_posix(), raw_target))
        if normalized == ".." or normalized.startswith("../") or normalized.startswith("/"):
            raise ConfigurationError(f"symlink adapter escapes repository: {adapter.as_posix()}")
        adapters[adapter] = PurePosixPath(normalized)
    return Context(
        root,
        inventory.current_paths,
        frozenset(inventory.baseline_paths),
        profiles,
        texts,
        metadata,
        adapters,
        registry.governance_current_owners.paths,
        registry.governance_current_owners.allowed_states,
    )


def _extract_links(text: str, *, definitions_text: str | None = None) -> tuple[str, ...]:
    visible = _visible_markdown(text)
    definition_source = _visible_markdown(definitions_text) if definitions_text is not None else visible
    definitions: dict[str, str] = {}
    for match in re.finditer(r"^ {0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))", definition_source, re.MULTILINE):
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
    shortcut = re.compile(r"(?<![!\]])\[([^\]\n]+)\](?![\[(])")
    for match in shortcut.finditer(visible):
        if visible[match.end() :].lstrip().startswith(":"):
            continue
        key = match.group(1).strip().casefold()
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


def _path_exists_without_dereference(root: Path, path: PurePosixPath, adapters: dict[PurePosixPath, PurePosixPath]) -> bool:
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
            if relative not in adapters:
                return False
            if index == len(path.parts) - 1:
                return True
            canonical = adapters[relative].joinpath(*path.parts[index + 1 :])
            return _path_exists_without_dereference(root, canonical, adapters)
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
            if not _path_exists_without_dereference(context.root, target, context.adapter_targets):
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
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token)); lines = []
            elif token[0] == fence[0] and len(token) >= fence[1] and not marker.group(2).strip():
                blocks.append("\n".join(lines)); fence = None; lines = []
            continue
        if fence is not None:
            lines.append(line)
    return tuple(blocks)


def _exact_heading_section(text: str, heading: str) -> str | None:
    visible_lines = _visible_markdown(text).splitlines()
    raw_lines = text.splitlines()
    matches = [index for index, line in enumerate(visible_lines) if line == heading]
    if len(matches) != 1:
        return None
    start = matches[0]
    level = len(heading) - len(heading.lstrip("#"))
    end = len(raw_lines)
    for index in range(start + 1, len(visible_lines)):
        candidate = re.match(r"^(#{1,6})\s", visible_lines[index])
        if candidate and len(candidate.group(1)) <= level:
            end = index
            break
    return "\n".join(raw_lines[start + 1 : end])


def _after_exact_heading(text: str, heading: str) -> str | None:
    visible_lines = _visible_markdown(text).splitlines()
    raw_lines = text.splitlines()
    matches = [index for index, line in enumerate(visible_lines) if line == heading]
    if len(matches) != 1:
        return None
    return "\n".join(raw_lines[matches[0] + 1 :])


def _tree_targets(declaration: DeclaredIndex, text: str) -> list[PurePosixPath]:
    section = _exact_heading_section(text, declaration.tree_anchor)
    if section is None:
        return []
    expected_root = declaration.tree_root
    block = next((item for item in _fenced_blocks(section) if item.splitlines() and item.splitlines()[0] == expected_root), "")
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
    section = (_after_exact_heading(text, declaration.table_anchor) if declaration.table_mode == "after" else _exact_heading_section(text, declaration.table_anchor))
    if section is None:
        return []
    lines = _visible_markdown(section).splitlines()
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
            target_key = target.as_posix()
            if count > 1:
                diagnostics.append(_diag("INDEX-DUPLICATE", declaration.path, profile, f"target={target_key}; one table row", f"target={target_key}; {count} rows"))
            if target not in actual_set:
                diagnostics.append(_diag("INDEX-STALE", declaration.path, profile, f"target={target_key}; declared target", f"target={target_key}; non-target row"))
        for target in actual:
            target_key = target.as_posix()
            if row_counter[target] == 0:
                diagnostics.append(_diag("INDEX-MISSING", declaration.path, profile, f"target={target_key}; one table row", f"target={target_key}; row is missing"))
            for row_target, row_status in rows:
                if row_target != target:
                    continue
                expected_status = str(context.metadata[target].get("status", "")).casefold()
                actual_status = STATUS_MAP.get(row_status.casefold(), "")
                if actual_status != expected_status:
                    diagnostics.append(_diag("INDEX-STATUS", declaration.path, profile, f"target={target_key}; status={expected_status}", f"target={target_key}; status={actual_status or 'unknown'}"))
                break
        for target in sorted(actual_set | set(tree), key=lambda p: p.as_posix()):
            if tree_counter[target] != (1 if target in actual_set else 0):
                target_key = target.as_posix()
                diagnostics.append(_diag("INDEX-TREE", declaration.path, profile, f"target={target_key}; one declared tree target", f"target={target_key}; {tree_counter[target]} entries"))
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
        for raw in _extract_links(match.group(1), definitions_text=visible):
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


def _governance_mirror_rows(
    context: Context,
) -> list[tuple[PurePosixPath, str]] | None:
    readme = context.texts.get(GOVERNANCE_CURRENT_README)
    if readme is None:
        return None
    visible = _visible_markdown(readme).splitlines()
    headings = [
        index for index, line in enumerate(visible) if line == GOVERNANCE_CURRENT_HEADING
    ]
    if len(headings) != 1:
        return None
    parent_h2 = next(
        (
            line
            for line in reversed(visible[: headings[0]])
            if re.match(r"^##\s", line)
        ),
        "",
    )
    if parent_h2 != "## Document Index":
        return None
    cursor = headings[0] + 1
    while cursor < len(visible) and not visible[cursor].strip():
        cursor += 1
    if cursor >= len(visible) or visible[cursor] != "| Document | Lifecycle |":
        return None
    cursor += 1
    if cursor >= len(visible) or visible[cursor] != "| --- | --- |":
        return None
    cursor += 1
    rows: list[tuple[PurePosixPath, str]] = []
    while cursor < len(visible):
        line = visible[cursor]
        if re.match(r"^#{1,3}\s", line):
            break
        if not line.strip():
            cursor += 1
            continue
        match = re.fullmatch(
            r"\| \[`([^`]+)`\]\(([^\s?#)]+)\) \| `([^`]+)` \|",
            line,
        )
        if match is None:
            return None
        kind, target = _local_destination(GOVERNANCE_CURRENT_README, match.group(2))
        if kind != "local" or target is None or match.group(1) != target.name:
            return None
        rows.append((target, match.group(3).casefold()))
        cursor += 1
    return rows


def _governance_current_owner_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    declared = set(context.governance_current_paths)
    allowed = set(context.governance_current_states)
    for path in context.governance_current_paths:
        if path not in context.paths:
            diagnostics.append(
                _diag(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
                    path,
                    "governance/reference",
                    "declared tracked governance/reference document",
                    "declared path is missing",
                )
            )
            continue
        profile = context.profiles[path]
        if (
            profile.profile_id != "governance/reference"
            or profile.mode != "authored"
        ):
            diagnostics.append(
                _diag(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",
                    path,
                    profile.profile_id,
                    "authored governance/reference",
                    f"{profile.mode} {profile.profile_id}",
                )
            )
            continue
        status = str(context.metadata[path].get("status", "")).casefold()
        if status not in allowed:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-OWNER-STATUS",
                    path,
                    profile.profile_id,
                    "active or accepted",
                    status or "missing",
                )
            )

    for path in context.paths:
        profile = context.profiles[path]
        if (
            profile.profile_id != "governance/reference"
            or profile.mode != "authored"
        ):
            continue
        status = str(context.metadata[path].get("status", "")).casefold()
        if status in allowed and path not in declared:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-OWNER-UNDECLARED",
                    path,
                    profile.profile_id,
                    "active or accepted Stage 00 authority declared in the registry",
                    "current authority is undeclared",
                )
            )
        elif status in {"done", "archived"} and path not in declared:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-OWNER-ROUTE",
                    path,
                    profile.profile_id,
                    "draft candidate or declared active/accepted current authority",
                    f"undeclared {status} document in the current Stage 00 route",
                )
            )

    mirror_rows = _governance_mirror_rows(context)
    if mirror_rows is None:
        diagnostics.append(
            _diag(
                "GOVERNANCE-INDEX-MISSING",
                GOVERNANCE_CURRENT_README,
                context.profiles.get(
                    GOVERNANCE_CURRENT_README,
                    ProfileView("readme/stage-index", "readme", "frontmatter-free"),
                ).profile_id,
                "one exact Current Governance Authority Index table",
                "heading or table is missing or malformed",
            )
        )
        return diagnostics

    declared_order = list(context.governance_current_paths)
    declared_set = set(declared_order)
    row_paths = [path for path, _ in mirror_rows]
    row_counter = collections.Counter(row_paths)
    for path in declared_order:
        if row_counter[path] == 0:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-INDEX-MISSING",
                    GOVERNANCE_CURRENT_README,
                    "readme/stage-index",
                    f"one row for {path.as_posix()}",
                    "declared owner row is missing",
                )
            )
    for path in sorted(set(row_paths) - declared_set, key=lambda item: item.as_posix()):
        diagnostics.append(
            _diag(
                "GOVERNANCE-INDEX-STALE",
                GOVERNANCE_CURRENT_README,
                "readme/stage-index",
                "registry-declared current authority row",
                f"stale row for {path.as_posix()}",
            )
        )
    for path, count in sorted(row_counter.items(), key=lambda item: item[0].as_posix()):
        if count > 1:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-INDEX-DUPLICATE",
                    GOVERNANCE_CURRENT_README,
                    "readme/stage-index",
                    f"one row for {path.as_posix()}",
                    f"{count} rows",
                )
            )
    for path, status in mirror_rows:
        expected_status = str(
            context.metadata.get(path, {}).get("status", "")
        ).casefold()
        if (
            path in declared_set
            and expected_status in allowed
            and (status not in allowed or status != expected_status)
        ):
            diagnostics.append(
                _diag(
                    "GOVERNANCE-INDEX-STATUS",
                    GOVERNANCE_CURRENT_README,
                    "readme/stage-index",
                    f"{path.as_posix()} lifecycle matches active/accepted frontmatter",
                    status or "missing",
                )
            )
    if (
        len(row_paths) == len(declared_order)
        and collections.Counter(row_paths) == collections.Counter(declared_order)
        and row_paths != declared_order
    ):
        diagnostics.append(
            _diag(
                "GOVERNANCE-INDEX-ORDER",
                GOVERNANCE_CURRENT_README,
                "readme/stage-index",
                "rows in registry declaration order",
                "row order differs",
            )
        )
    return diagnostics


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


def _load_debt(
    root: Path,
    raw: Any | None = None,
    *,
    mode: str = "strict",
) -> dict[str, Any]:
    """Require the canonical retired semantic-debt source state."""

    if mode not in {"compatibility", "strict"}:
        raise ConfigurationError("mode must be compatibility or strict")
    if raw is not None or (root / DEBT_PATH).exists():
        raise ConfigurationError(
            "DEBT-SOURCE-REINTRODUCED: semantic compatibility debt must remain absent"
        )
    if mode == "compatibility":
        raise ConfigurationError(
            "DEBT-SOURCE-MISSING: semantic compatibility debt is retired"
        )
    return {
        "schemaVersion": 1,
        "owner": "Spec 030",
        "growthAllowed": False,
        "items": [],
    }


def _apply_debt(root: Path, diagnostics: Iterable[Diagnostic], mode: str, contract: Any | None = None) -> list[tuple[str, Diagnostic]]:
    _load_debt(root, contract, mode=mode)
    return [
        ("FAIL", diagnostic)
        for diagnostic in sorted(diagnostics, key=diagnostic_sort_key)
    ]


def _raw_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics = _link_diagnostics(context)
    diagnostics.extend(_index_diagnostics(context))
    diagnostics.extend(_governance_current_owner_diagnostics(context))
    diagnostics.extend(_owner_diagnostics(context))
    diagnostics.extend(_ledger_diagnostics(context))
    return sorted(diagnostics, key=diagnostic_sort_key)


def validate_cross_document_contracts(root: Path, mode: str) -> list[Diagnostic]:
    """Return deterministic raw cross-document diagnostics."""

    if mode not in {"compatibility", "strict"}:
        raise ConfigurationError("mode must be compatibility or strict")
    context = _build_context(root)
    _load_debt(context.root, mode=mode)
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
    if list(tree) != [
        "documents",
        "declaredIndexes",
        "ledgerColumns",
        "symlinkAdapters",
        "governanceCurrentOwners",
        "governanceMirrorPath",
    ]:
        raise ConfigurationError("fixture baseTree keys differ")
    documents = tree["documents"]
    if not isinstance(documents, list):
        raise ConfigurationError("fixture documents must be a list")
    document_keys = ["path", "profile", "profileClass", "mode", "title", "type", "status", "body"]
    if any(not isinstance(item, dict) or list(item) != document_keys for item in documents):
        raise ConfigurationError("fixture document keys differ")
    paths = tuple(PurePosixPath(item["path"]) for item in documents)
    if tree["declaredIndexes"] != [item.path.as_posix() for item in DECLARED_INDEXES]:
        raise ConfigurationError("fixture declared indexes differ")
    if tuple(tree["ledgerColumns"]) != LEDGER_COLUMNS:
        raise ConfigurationError("fixture ledger columns differ")
    governance_current_paths = tuple(
        PurePosixPath(value) for value in tree["governanceCurrentOwners"]
    )
    if governance_current_paths != FIXTURE_GOVERNANCE_PATHS:
        raise ConfigurationError("fixture governance current-owner declaration differs")
    if tree["governanceMirrorPath"] != GOVERNANCE_CURRENT_README.as_posix():
        raise ConfigurationError("fixture governance mirror path differs")
    if paths != tuple(sorted(paths, key=lambda path: path.as_posix())) or len(paths) != len(set(paths)):
        raise ConfigurationError("fixture paths must be sorted and unique")

    def authored(title: str, doc_type: str, status: str, body: str) -> str:
        return f"---\ntitle: {title}\ntype: {doc_type}\nstatus: {status}\nowner: platform\nupdated: 2026-07-12\n---\n\n# {title}\n\n{body}\n"

    texts: dict[PurePosixPath, str] = {}
    profile_map: dict[PurePosixPath, ProfileView] = {}
    for item, path in zip(documents, paths, strict=True):
        profile_map[path] = ProfileView(item["profile"], item["profileClass"], item["mode"])
        if item["mode"] in {"frontmatter-free", "native"}:
            texts[path] = item["body"]
        elif item["body"] != "@ledger":
            texts[path] = authored(item["title"], item["type"], item["status"], item["body"])
    header = "| " + " | ".join(LEDGER_COLUMNS) + " |"
    alignment = "| " + " | ".join("---" for _ in LEDGER_COLUMNS) + " |"
    rows = []
    for path in paths:
        cells = [f"`{path.as_posix()}`", "Fixture", profile_map[path].profile_id, "", "preserve", f"`{path.as_posix()}`", "fixture", "not applicable", "2026-07-12", "repository-specific", "retain", "contract change", "platform", "reviewed"]
        rows.append("| " + " | ".join(cells) + " |")
    ledger_item = next((item for item in documents if item["path"] == LEDGER_PATH.as_posix()), None)
    if ledger_item is None or ledger_item["body"] != "@ledger":
        raise ConfigurationError("fixture ledger marker differs")
    texts[LEDGER_PATH] = authored(ledger_item["title"], ledger_item["type"], ledger_item["status"], "\n".join((header, alignment, *rows)))
    for path, text in texts.items():
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    adapter_targets: dict[PurePosixPath, PurePosixPath] = {}
    for adapter in tree["symlinkAdapters"]:
        if list(adapter) != ["path", "target"]:
            raise ConfigurationError("fixture symlink adapter keys differ")
        adapter_path = PurePosixPath(adapter["path"])
        link_path = root / adapter_path
        link_path.parent.mkdir(parents=True, exist_ok=True)
        link_path.symlink_to(adapter["target"])
        normalized = posixpath.normpath(posixpath.join(adapter_path.parent.as_posix(), adapter["target"]))
        adapter_targets[adapter_path] = PurePosixPath(normalized)
    metadata = {path: _frontmatter(texts[path]) for path in paths}
    return Context(
        root,
        paths,
        frozenset(paths),
        profile_map,
        texts,
        metadata,
        adapter_targets,
        governance_current_paths,
        ("active", "accepted"),
    )


def _mutated_context(context: Context, mutation: str) -> Context:
    texts = dict(context.texts)
    metadata = copy.deepcopy(context.metadata)
    governance_current_paths = context.governance_current_paths
    source = PurePosixPath("docs/05.operations/guides/9999-source.md")
    if mutation == "link-broken": texts[source] += "\n[bad](./missing.md)\n"
    elif mutation == "link-absolute": texts[source] += "\n[bad](/etc/passwd)\n"
    elif mutation == "link-file-uri": texts[source] += "\n[bad](file:///tmp/x)\n"
    elif mutation == "link-escape": texts[source] += "\n[bad](../../../../escape.md)\n"
    elif mutation == "link-archive-bypass": texts[source] += "\n[bad](../../98.archive/999-fixture.md)\n"
    elif mutation == "link-adapter-missing": texts[source] += "\n[bad](../../../.claude/skills/missing/skill.md)\n"
    elif mutation == "links-excluded": texts[source] += "\n```md\n[bad](./missing.md)\n```\n<!-- [bad](./missing.md) -->\n"
    elif mutation == "link-invalid-fence-closer": texts[source] += "\n```md\n[bad](./missing.md)\n``` still-open\n[also-bad](./missing-two.md)\n```\n"
    elif mutation == "index-missing":
        path = DECLARED_INDEXES[0].path; texts[path] = "\n".join(line for line in texts[path].splitlines() if "[`./999-fixture/spec.md`]" not in line)
    elif mutation == "index-stale":
        path = DECLARED_INDEXES[0].path; texts[path] += "| [`./stale/spec.md`](./stale/spec.md) | stale | Active |\n"
    elif mutation == "index-duplicate":
        path = DECLARED_INDEXES[0].path; row = next(line for line in texts[path].splitlines() if "[`./999-fixture/spec.md`]" in line); texts[path] += row + "\n"
    elif mutation == "index-status": texts[DECLARED_INDEXES[0].path] = texts[DECLARED_INDEXES[0].path].replace("| Active |", "| Done |")
    elif mutation == "index-tree": texts[DECLARED_INDEXES[0].path] = texts[DECLARED_INDEXES[0].path].replace("    └── spec.md\n", "")
    elif mutation == "index-anchor-prose": texts[DECLARED_INDEXES[0].path] = texts[DECLARED_INDEXES[0].path].replace("### Current Spec Index", "This prose mentions ### Current Spec Index")
    elif mutation == "index-multi-order":
        path = DECLARED_INDEXES[0].path
        texts[path] = "\n".join(line for line in texts[path].splitlines() if "[`./998-second/spec.md`]" not in line and "[`./999-fixture/spec.md`]" not in line)
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
    elif mutation in {
        "governance-declared-accepted",
        "governance-declared-draft",
        "governance-declared-done",
        "governance-declared-archived",
    }:
        status = mutation.removeprefix("governance-declared-")
        metadata[FIXTURE_GOVERNANCE_PATHS[0]]["status"] = status
        texts[GOVERNANCE_CURRENT_README] = texts[GOVERNANCE_CURRENT_README].replace(
            "| [`current-alpha.md`](current-alpha.md) | `active` |",
            f"| [`current-alpha.md`](current-alpha.md) | `{status}` |",
        )
    elif mutation in {
        "governance-undeclared-draft",
        "governance-active-undeclared",
        "governance-accepted-undeclared",
        "governance-undeclared-done",
        "governance-undeclared-archived",
    }:
        status = {
            "governance-undeclared-draft": "draft",
            "governance-active-undeclared": "active",
            "governance-accepted-undeclared": "accepted",
            "governance-undeclared-done": "done",
            "governance-undeclared-archived": "archived",
        }[mutation]
        metadata[FIXTURE_GOVERNANCE_PATHS[0]]["status"] = status
        governance_current_paths = (FIXTURE_GOVERNANCE_PATHS[1],)
        texts[GOVERNANCE_CURRENT_README] = "\n".join(
            line
            for line in texts[GOVERNANCE_CURRENT_README].splitlines()
            if "current-alpha.md" not in line
        )
    elif mutation == "governance-declared-missing":
        missing = PurePosixPath("docs/00.agent-governance/current-missing.md")
        governance_current_paths = (missing, FIXTURE_GOVERNANCE_PATHS[1])
        metadata[FIXTURE_GOVERNANCE_PATHS[0]]["status"] = "draft"
        texts[GOVERNANCE_CURRENT_README] = texts[GOVERNANCE_CURRENT_README].replace(
            "| [`current-alpha.md`](current-alpha.md) | `active` |",
            "| [`current-missing.md`](current-missing.md) | `active` |",
        )
    elif mutation == "governance-index-missing":
        texts[GOVERNANCE_CURRENT_README] = "\n".join(
            line
            for line in texts[GOVERNANCE_CURRENT_README].splitlines()
            if "current-alpha.md" not in line
        )
    elif mutation == "governance-index-stale":
        texts[GOVERNANCE_CURRENT_README] += (
            "\n| [`current-stale.md`](current-stale.md) | `active` |\n"
        )
    elif mutation == "governance-index-duplicate":
        row = "| [`current-alpha.md`](current-alpha.md) | `active` |"
        texts[GOVERNANCE_CURRENT_README] = texts[GOVERNANCE_CURRENT_README].replace(
            row, f"{row}\n{row}"
        )
    elif mutation == "governance-index-status":
        texts[GOVERNANCE_CURRENT_README] = texts[GOVERNANCE_CURRENT_README].replace(
            "| [`current-alpha.md`](current-alpha.md) | `active` |",
            "| [`current-alpha.md`](current-alpha.md) | `accepted` |",
        )
    elif mutation == "governance-index-swap":
        texts[GOVERNANCE_CURRENT_README] = texts[GOVERNANCE_CURRENT_README].replace(
            "| [`current-alpha.md`](current-alpha.md) | `active` |",
            "| [`current-stale.md`](current-stale.md) | `active` |",
        )
    elif mutation == "governance-index-order":
        alpha = "| [`current-alpha.md`](current-alpha.md) | `active` |"
        beta = "| [`current-beta.md`](current-beta.md) | `active` |"
        texts[GOVERNANCE_CURRENT_README] = texts[GOVERNANCE_CURRENT_README].replace(
            f"{alpha}\n{beta}", f"{beta}\n{alpha}"
        )
    elif mutation == "governance-index-lookalike":
        texts[GOVERNANCE_CURRENT_README] = texts[GOVERNANCE_CURRENT_README].replace(
            GOVERNANCE_CURRENT_HEADING,
            "Current Governance Authority Index",
        ) + (
            "\n```markdown\n"
            + GOVERNANCE_CURRENT_HEADING
            + "\n\n| Document | Lifecycle |\n| --- | --- |\n"
            + "| [`current-alpha.md`](current-alpha.md) | `active` |\n```\n"
        )
    return Context(
        context.root,
        context.paths,
        context.baseline_paths,
        context.profiles,
        texts,
        metadata,
        context.adapter_targets,
        governance_current_paths,
        context.governance_current_states,
    )


def _fixture_rule_ids(context: Context, mutation: str) -> list[str]:
    mutated = _mutated_context(context, mutation)
    if mutation.startswith("link") or mutation in {"links-excluded"}:
        diagnostics = _link_diagnostics(mutated)
    elif mutation.startswith("index"):
        if mutation == "index-multi-order":
            missing = [item for item in _index_diagnostics(mutated) if item.rule_id == "INDEX-MISSING"]
            targets = [item.expected.split(";", 1)[0] for item in missing]
            return [] if len(missing) == 2 and targets == sorted(targets) and len(set(targets)) == 2 else ["INDEX-MISSING"]
        diagnostics = _index_diagnostics(mutated)
    elif mutation.startswith("owner"):
        if mutation == "owner-normalization":
            plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
            mutated.metadata[plan]["type"] = "ＳＤＬＣ／ＰＬＡＮ"
            mutated.metadata[plan]["title"] = "Ｆixture__Implementation Plan"
            key, diagnostic = _owner_key(mutated, plan)
            return [] if diagnostic is None and key == "sdlc-plan|fixture|fixture" else ["OWNER-KEY-MISSING"]
        if mutation == "owner-first-upstream":
            plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
            texts = dict(mutated.texts)
            texts[plan] += "\n[local-ref]: ../../README.md\n[prd-ref]: ../../01.requirements/999-fixture.md\n[spec-ref]: ../../03.specs/999-fixture/spec.md\n\n## Traceability\n\n[local][local-ref]\n[prd][prd-ref]\n[spec][spec-ref]\n"
            selected = Context(
                mutated.root,
                mutated.paths,
                mutated.baseline_paths,
                mutated.profiles,
                texts,
                mutated.metadata,
                mutated.adapter_targets,
                mutated.governance_current_paths,
                mutated.governance_current_states,
            )
            key, diagnostic = _owner_key(selected, plan)
            expected = "sdlc-plan|fixture|docs-01-requirements-999-fixture-md"
            return [] if diagnostic is None and key == expected else ["OWNER-KEY-MISSING"]
        if mutation == "owner-fallback":
            plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
            key, diagnostic = _owner_key(mutated, plan)
            return [] if diagnostic is None and key == "sdlc-plan|fixture|fixture" else ["OWNER-KEY-MISSING"]
        if mutation == "owner-exclusions":
            key, diagnostic = _owner_key(mutated, LEDGER_PATH)
            return [] if not key and diagnostic is None and not _owner_candidate(mutated, LEDGER_PATH) else ["OWNER-DUPLICATE"]
        diagnostics = _owner_diagnostics(mutated)
    elif mutation.startswith("ledger"):
        diagnostics = _ledger_diagnostics(mutated)
    elif mutation.startswith("governance"):
        diagnostics = _governance_current_owner_diagnostics(mutated)
    elif mutation in {"none", "link-normalization"}:
        diagnostics = (
            _link_diagnostics(mutated)
            + _index_diagnostics(mutated)
            + _governance_current_owner_diagnostics(mutated)
            + _owner_diagnostics(mutated)
            + _ledger_diagnostics(mutated)
        )
    else:
        raise ConfigurationError(f"unknown fixture mutation: {mutation}")
    return sorted(set(item.rule_id for item in diagnostics))


def _self_test(root: Path) -> list[str]:
    fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
    failures: list[str] = []
    if list(fixture) != ["schemaVersion", "baseTree", "cases"] or fixture["schemaVersion"] != 1:
        return ["fixture schema differs"]
    required = {
        "valid-tree",
        "broken-link",
        "absolute-link",
        "archive-bypass",
        "missing-index-row",
        "stale-index-row",
        "duplicate-current-owner",
        "governance-declared-active",
        "governance-declared-accepted",
        "governance-undeclared-draft",
        "governance-declared-draft",
        "governance-declared-done",
        "governance-declared-archived",
        "governance-active-undeclared",
        "governance-accepted-undeclared",
        "governance-undeclared-done",
        "governance-undeclared-archived",
        "governance-declared-missing",
        "governance-index-missing",
        "governance-index-stale",
        "governance-index-duplicate",
        "governance-index-status",
        "governance-index-equal-count-swap",
        "governance-index-order",
        "governance-index-fenced-lookalike",
        "missing-ledger-row",
        "incomplete-ledger-row",
        "unknown-ledger-path",
    }
    names = [case.get("name") for case in fixture["cases"]]
    if not required.issubset(names) or len(names) != len(set(names)):
        failures.append("required unique fixture cases are incomplete")
    ledger_existed_before = (root / LEDGER_PATH).exists()
    with tempfile.TemporaryDirectory(prefix="smdv-cross-") as temporary:
        context = _fixture_context(Path(temporary), fixture["baseTree"])
        for case in fixture["cases"]:
            if case.get("tree") != {"base": "baseTree"} or list(case) != ["name", "tree", "mutation", "expected_rule_ids"]:
                failures.append(f"{case.get('name')}: case tree/schema differs")
                continue
            if not isinstance(case["mutation"], dict) or list(case["mutation"]) != ["kind"]:
                failures.append(f"{case.get('name')}: structured mutation differs")
                continue
            expected = sorted(case["expected_rule_ids"])
            actual = _fixture_rule_ids(context, case["mutation"]["kind"])
            if actual != expected:
                failures.append(f"{case['name']}: expected {expected}, actual {actual}")
    if (root / LEDGER_PATH).exists() != ledger_existed_before:
        failures.append("self-test changed the repository ledger artifact")
    if (root / DEBT_PATH).exists():
        failures.append("retired semantic debt source is still present")
    base = _load_debt(root, mode="strict")
    singleton = {
        "schemaVersion": 1,
        "owner": "Spec 030",
        "growthAllowed": False,
        "items": [copy.deepcopy(DEBT_LITERAL)],
    }
    partial = copy.deepcopy(singleton)
    partial["items"][0].pop("removeWhen")
    mutations = (
        ("empty source", base),
        ("new debt", singleton),
        ("partial source", partial),
    )
    for label, candidate in mutations:
        for mode in ("compatibility", "strict"):
            try:
                _load_debt(root, candidate, mode=mode)
            except ConfigurationError:
                continue
            failures.append(f"debt source mutation accepted in {mode}: {label}")
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        return_code = main(
            ["--root", str(root), "--mode", "compatibility", "--format", "json"]
        )
    expected_stderr = (
        "configuration error: DEBT-SOURCE-MISSING: semantic compatibility "
        "debt is retired\n"
    )
    if return_code != 2 or stdout.getvalue() or stderr.getvalue() != expected_stderr:
        failures.append("retired semantic debt CLI boundary differs")
    if (root / DEBT_PATH).exists():
        failures.append("retired semantic debt source was recreated")
    production_context = _build_context(root)
    production = validate_cross_document_contracts(root, "strict")
    if production:
        failures.append("strict production repository diagnostics must be empty")
    owner_keys, owner_diagnostics = _owner_state(production_context)
    current_unique_keys = {key for key in owner_keys.values() if key}
    governance_keys = [
        owner_keys.get(path, "")
        for path in production_context.governance_current_paths
    ]
    if owner_diagnostics:
        failures.append("production current-owner state has diagnostics")
    if (
        any(not key for key in governance_keys)
        or len(governance_keys) != len(set(governance_keys))
    ):
        failures.append(
            "declared Stage 00 current owners must have non-empty unique owner keys"
        )

    post_smdv_context = copy.deepcopy(production_context)
    adm_closure_valid = True
    for path in ADM_CLOSURE_PATHS:
        if (
            path not in production_context.metadata
            or production_context.metadata[path].get("status") != "done"
            or _owner_candidate(production_context, path)
            or owner_keys.get(path)
        ):
            adm_closure_valid = False
            break
        post_smdv_context.metadata[path]["status"] = "active"
    if not adm_closure_valid:
        failures.append(
            "ADM closure paths must be the exact done-status owner exclusions"
        )
    else:
        post_smdv_keys, post_smdv_diagnostics = _owner_state(post_smdv_context)
        adm_transitioned_paths = {
            path
            for path in production_context.paths
            if owner_keys.get(path) != post_smdv_keys.get(path)
        }
        post_smdv_unique_keys = {
            key for key in post_smdv_keys.values() if key
        }
        if (
            post_smdv_diagnostics
            or adm_transitioned_paths != set(ADM_CLOSURE_PATHS)
            or any(not post_smdv_keys.get(path) for path in ADM_CLOSURE_PATHS)
            or len(post_smdv_unique_keys) - len(current_unique_keys)
            != len(ADM_CLOSURE_PATHS)
        ):
            failures.append(
                "ADM done-to-active transition must change only its three paths "
                "and add three non-empty unique owner keys"
            )
        pre_smdv_context = copy.deepcopy(post_smdv_context)
        smdv_closure_valid = True
        for path in SMDV_CLOSURE_PATHS:
            if (
                path not in post_smdv_context.metadata
                or post_smdv_context.metadata[path].get("status") != "done"
                or _owner_candidate(post_smdv_context, path)
                or post_smdv_keys.get(path)
            ):
                smdv_closure_valid = False
                break
            pre_smdv_context.metadata[path]["status"] = "active"
        if not smdv_closure_valid:
            failures.append(
                "SMDV closure paths must be the exact done-status owner exclusions"
            )
        else:
            pre_smdv_keys, pre_smdv_diagnostics = _owner_state(pre_smdv_context)
            smdv_transitioned_paths = {
                path
                for path in post_smdv_context.paths
                if post_smdv_keys.get(path) != pre_smdv_keys.get(path)
            }
            pre_smdv_unique_keys = {
                key for key in pre_smdv_keys.values() if key
            }
            if (
                pre_smdv_diagnostics
                or smdv_transitioned_paths != set(SMDV_CLOSURE_PATHS)
                or any(not pre_smdv_keys.get(path) for path in SMDV_CLOSURE_PATHS)
                or len(pre_smdv_unique_keys) - len(post_smdv_unique_keys)
                != len(SMDV_CLOSURE_PATHS)
            ):
                failures.append(
                    "SMDV done-to-active transition must change only its three "
                    "paths and add three non-empty unique owner keys"
                )
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
        inventory = enumerate_target_markdown(context.root, include_paths=include_paths)
        counts = {
            "baseline": len(inventory.baseline_paths),
            "current": len(inventory.current_paths),
            "new": len(inventory.new_paths),
            "documents": len(inventory.current_paths),
        }
        if args.inventory:
            diagnostics = (
                _link_diagnostics(context)
                + _index_diagnostics(context)
                + _governance_current_owner_diagnostics(context)
                + _owner_diagnostics(context)
            )
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
