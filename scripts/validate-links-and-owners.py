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
    ReferenceCurrentPack,
    ReferenceCurrentPacks,
    _parse_ls_files_stage_z,
    _run_git,
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
    "BODY-LINK-BROKEN", "BODY-LINK-EXCLUSION", "BODY-LINK-RECIPROCAL",
    "BODY-LINK-SOURCE", "BODY-LINK-SOURCE-PROFILE", "BODY-LINK-TARGET",
    "BODY-LINK-TARGET-PROFILE",
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
    "REFERENCE-PACK-OWNER-UNDECLARED", "REFERENCE-PACK-OWNER-STATUS",
    "REFERENCE-PACK-COLLECTION-MISSING", "REFERENCE-PACK-COLLECTION-STALE",
    "REFERENCE-PACK-COLLECTION-DUPLICATE", "REFERENCE-PACK-INDEX-MISSING",
    "REFERENCE-PACK-INDEX-STALE", "REFERENCE-PACK-INDEX-DUPLICATE",
    "REFERENCE-PACK-INDEX-STATUS", "REFERENCE-PACK-INDEX-ORDER",
    "REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",
    "COLLECTION-INDEX-PARSE", "COLLECTION-INDEX-TREE-MISSING",
    "COLLECTION-INDEX-TREE-STALE", "COLLECTION-INDEX-TREE-DUPLICATE",
    "COLLECTION-INDEX-ROW-MISSING", "COLLECTION-INDEX-ROW-STALE",
    "COLLECTION-INDEX-ROW-DUPLICATE",
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
class CollectionIndex:
    path: PurePosixPath
    root: PurePosixPath
    target_pattern: re.Pattern[str]
    tree_anchor: str
    tree_root: str
    table_anchor: str
    table_mode: str
    table_includes_self: bool


COLLECTION_INDEXES = (
    CollectionIndex(
        PurePosixPath("docs/90.references/research/README.md"),
        PurePosixPath("docs/90.references/research"),
        re.compile(
            r"^docs/90\.references/research/(?:README\.md|"
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/]+/[^/]+\.md)$"
        ),
        "## Item Index",
        "research/",
        "### Research Pack Index",
        "section",
        True,
    ),
    CollectionIndex(
        PurePosixPath("docs/90.references/research/2026-07-07-wer/README.md"),
        PurePosixPath("docs/90.references/research/2026-07-07-wer"),
        re.compile(r"^docs/90\.references/research/2026-07-07-wer/[^/]+\.md$"),
        "### Structure",
        "2026-07-07-wer/",
        "## Report Index",
        "section",
        False,
    ),
    CollectionIndex(
        PurePosixPath("docs/99.templates/support/README.md"),
        PurePosixPath("docs/99.templates/support"),
        re.compile(r"^docs/99\.templates/support/[^/]+\.(?:md|json)$"),
        "## Item Index",
        "support/",
        "### Support Document Index",
        "section",
        False,
    ),
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
    reference_current_packs: ReferenceCurrentPacks
    tracked_regular_paths: frozenset[PurePosixPath]


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
        if fence is not None:
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", raw_line)
            if marker:
                token = marker.group(1)
                if (
                    token[0] == fence[0]
                    and len(token) >= fence[1]
                    and not marker.group(2).strip()
                ):
                    fence = None
            output.append("")
            continue
        visible: list[str] = []
        cursor = 0
        while cursor < len(raw_line):
            if in_comment:
                end = raw_line.find("-->", cursor)
                if end < 0:
                    cursor = len(raw_line)
                    continue
                cursor = end + 3
                in_comment = False
                continue
            start = raw_line.find("<!--", cursor)
            if start < 0:
                visible.append(raw_line[cursor:])
                break
            visible.append(raw_line[cursor:start])
            cursor = start + 4
            in_comment = True
        line = "".join(visible)
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            if token[0] == "`" and "`" in marker.group(2):
                output.append(line)
                continue
            fence = (token[0], len(token))
            output.append("")
            continue
        output.append(line)
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
    tracked_regular_paths = frozenset(
        entry.path
        for entry in _parse_ls_files_stage_z(
            _run_git(root, ("ls-files", "--stage", "-z"))
        )
        if entry.stage == 0 and entry.mode in {"100644", "100755"}
    )
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
        registry.reference_current_packs,
        tracked_regular_paths,
    )


def _normalize_reference_label(value: str) -> str:
    """Normalize a CommonMark reference label for deterministic lookup."""

    return re.sub(r"\s+", " ", value.strip()).casefold()


def _mask_inline_code_spans(text: str) -> str:
    """Mask matched CommonMark backtick spans while preserving source offsets."""

    masked = list(text)
    cursor = 0
    while cursor < len(text):
        if text[cursor] != "`":
            cursor += 1
            continue
        opening = cursor
        while cursor < len(text) and text[cursor] == "`":
            cursor += 1
        run_length = cursor - opening
        delimiter = re.compile(
            rf"(?<!`){re.escape('`' * run_length)}(?!`)"
        )
        closing = delimiter.search(text, cursor)
        if closing is None:
            continue
        for index in range(opening, closing.end()):
            if masked[index] != "\n":
                masked[index] = " "
        cursor = closing.end()
    return "".join(masked)


def _bracket_opener_is_escaped(text: str, index: int) -> bool:
    """Return whether a bracket opener follows an odd backslash run."""

    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _extract_links(text: str, *, definitions_text: str | None = None) -> tuple[str, ...]:
    visible = _mask_inline_code_spans(_visible_markdown(text))
    definition_source = (
        _mask_inline_code_spans(_visible_markdown(definitions_text))
        if definitions_text is not None
        else visible
    )
    definitions: dict[str, str] = {}
    for match in re.finditer(r"^ {0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))", definition_source, re.MULTILINE):
        key = _normalize_reference_label(match.group(1))
        target = match.group(2) or match.group(3)
        definitions.setdefault(key, target)
    found: list[tuple[int, str]] = []
    inline = re.compile(r"(?<!!)\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
    for match in inline.finditer(visible):
        if _bracket_opener_is_escaped(visible, match.start()):
            continue
        found.append((match.start(), match.group(1) or match.group(2)))
    reference = re.compile(r"(?<!!)\[([^\]\n]+)\]\[([^\]\n]*)\]")
    for match in reference.finditer(visible):
        if _bracket_opener_is_escaped(visible, match.start()):
            continue
        key = _normalize_reference_label(match.group(2) or match.group(1))
        if key in definitions:
            found.append((match.start(), definitions[key]))
    shortcut = re.compile(r"(?<![!\]])\[([^\]\n]+)\](?![\[(])")
    for match in shortcut.finditer(visible):
        if _bracket_opener_is_escaped(visible, match.start()):
            continue
        if visible[match.end() :].lstrip().startswith(":"):
            continue
        key = _normalize_reference_label(match.group(1))
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


def _markdown_without_html_comments(text: str) -> str:
    """Remove HTML comments outside fences while preserving line positions."""
    output: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for raw_line in text.splitlines():
        if fence is not None:
            output.append(raw_line)
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", raw_line)
            if marker:
                token = marker.group(1)
                if (
                    token[0] == fence[0]
                    and len(token) >= fence[1]
                    and not marker.group(2).strip()
                ):
                    fence = None
            continue

        visible: list[str] = []
        cursor = 0
        while cursor < len(raw_line):
            if in_comment:
                end = raw_line.find("-->", cursor)
                if end < 0:
                    cursor = len(raw_line)
                    continue
                cursor = end + 3
                in_comment = False
                continue
            start = raw_line.find("<!--", cursor)
            if start < 0:
                visible.append(raw_line[cursor:])
                break
            visible.append(raw_line[cursor:start])
            cursor = start + 4
            in_comment = True

        line = "".join(visible)
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            fence = (token[0], len(token))
        output.append(line)
    return "\n".join(output)


def _gfm_table_cells(line: str) -> list[str]:
    """Split one GFM table row without treating escaped pipes as delimiters."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []

    def escaped(index: int) -> bool:
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and stripped[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        return backslashes % 2 == 1

    cells: list[str] = []
    current: list[str] = []
    for index, character in enumerate(stripped):
        if character == "|" and not escaped(index):
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    cells.append("".join(current).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if stripped.endswith("|") and not escaped(len(stripped) - 1) and cells[-1] == "":
        cells.pop()
    return cells


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


_COLLECTION_TREE_LINE = re.compile(
    r"^(?P<indent>(?:│   |    )*)(?:├── |└── )"
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?P<directory>/)?"
    r"(?:\s+#\s+.*)?$"
)


def _collection_tree_targets(
    declaration: CollectionIndex, text: str
) -> tuple[list[PurePosixPath], bool]:
    section = _exact_heading_section(text, declaration.tree_anchor)
    if section is None:
        return [], False
    comment_visible_section = _markdown_without_html_comments(section)
    blocks = [
        block
        for block in _fenced_blocks(comment_visible_section)
        if block.splitlines() and block.splitlines()[0] == declaration.tree_root
    ]
    if len(blocks) != 1:
        return [], False
    stack: list[str] = []
    targets: list[PurePosixPath] = []
    valid = True
    for line in blocks[0].splitlines()[1:]:
        if not line.strip():
            continue
        match = _COLLECTION_TREE_LINE.fullmatch(line)
        if match is None:
            valid = False
            continue
        indent = match.group("indent")
        depth = len(indent) // 4
        name = match.group("name")
        if name in {".", ".."}:
            valid = False
            continue
        if match.group("directory"):
            if depth > len(stack):
                valid = False
                continue
            stack[depth:] = [name]
            continue
        if depth > len(stack):
            valid = False
            continue
        relative = (*stack[:depth], name)
        target = declaration.root.joinpath(*relative)
        if declaration.target_pattern.fullmatch(target.as_posix()) is None:
            valid = False
            continue
        targets.append(target)
    return targets, valid


def _first_visible_table(
    text: str,
) -> tuple[list[str], list[list[str]]] | None:
    lines = _visible_markdown(text).splitlines()
    for index in range(len(lines) - 1):
        header_line = lines[index]
        delimiter_line = lines[index + 1]
        if (
            re.match(r"^ {0,3}\|", header_line) is None
            or re.match(r"^ {0,3}\|", delimiter_line) is None
        ):
            continue
        header = _gfm_table_cells(header_line)
        delimiter = _gfm_table_cells(delimiter_line)
        if len(header) != len(delimiter) or not header:
            continue
        if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in delimiter):
            continue
        rows: list[list[str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.strip():
                break
            if re.match(r"^ {0,3}\|", row_line) is None:
                break
            cells = _gfm_table_cells(row_line)
            rows.append((cells + [""] * len(header))[: len(header)])
        return header, rows
    return None


BODY_LINK_EXCLUSION = re.compile(r"^N/A — \S(?:.*\S)?$")


def _body_contract_link_is_enforced(
    path: PurePosixPath,
    profile: DocumentProfile,
    status: str,
    body_contracts: str,
    path_prefixes: tuple[PurePosixPath, ...],
) -> bool:
    if body_contracts not in {"registry", "audit"}:
        raise ConfigurationError("body_contracts must be registry or audit")
    if profile.body_contract is None or profile.mode != "authored":
        return False
    if body_contracts == "audit":
        in_scope = not path_prefixes or any(
            path == prefix or prefix in path.parents
            for prefix in path_prefixes
        )
        return in_scope and status in {"draft", "active"}
    return status in profile.body_contract.enforced_statuses


def _body_contract_rows(
    text: str, profile: DocumentProfile
) -> list[dict[str, str]] | None:
    """Return a shape-valid lifecycle table; local validation owns shape errors."""

    contract = profile.body_contract
    if contract is None:
        return None
    section = _exact_heading_section(text, f"## {contract.section}")
    table_section = (
        None
        if section is None
        else _exact_heading_section(section, f"### {contract.table_heading}")
    )
    if table_section is None:
        return None
    table = _first_visible_table(table_section)
    if table is None or tuple(table[0]) != contract.required_columns:
        return None
    header, rows = table
    if not rows:
        return None
    return [dict(zip(header, row, strict=True)) for row in rows]


def _links_back_to(
    context: Context, owner: PurePosixPath, expected: PurePosixPath
) -> bool:
    for raw_link in _extract_links(context.texts[owner]):
        kind, target = _local_destination(owner, raw_link)
        if kind in {"local", "anchor"} and target == expected:
            return True
    return False


def _body_contract_link_diagnostics(
    context: Context,
    profiles_by_id: dict[str, DocumentProfile],
    body_contracts: str,
    path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Validate registry-owned relationship cells and reciprocal evidence."""

    if body_contracts not in {"registry", "audit"}:
        raise ConfigurationError("body_contracts must be registry or audit")
    diagnostics: list[Diagnostic] = []
    known_paths = set(context.paths)
    for path in context.paths:
        view = context.profiles[path]
        profile = profiles_by_id.get(view.profile_id)
        if profile is None:
            continue
        status_value = context.metadata[path].get("status", "")
        status = status_value if isinstance(status_value, str) else ""
        if not _body_contract_link_is_enforced(
            path, profile, status, body_contracts, path_prefixes
        ):
            continue
        contract = profile.body_contract
        assert contract is not None
        rows = _body_contract_rows(context.texts[path], profile)
        if rows is None:
            continue
        link_columns = (
            ("source", contract.source_link_column, contract.allowed_source_profile_ids),
            ("target", contract.target_link_column, contract.allowed_target_profile_ids),
        )
        for row_number, row in enumerate(rows, start=1):
            for direction, column, allowed_profile_ids in link_columns:
                if column is None:
                    continue
                cell = row[column].strip()
                if cell.startswith("N/A"):
                    if (
                        not contract.allow_explicit_exclusion
                        or BODY_LINK_EXCLUSION.fullmatch(cell) is None
                    ):
                        diagnostics.append(
                            _diag(
                                "BODY-LINK-EXCLUSION",
                                path,
                                profile.profile_id,
                                "N/A — followed by a reviewable reason",
                                f"row {row_number}, {column}: {cell}",
                            )
                        )
                    continue
                raw_links = _extract_links(
                    cell, definitions_text=context.texts[path]
                )
                if not raw_links:
                    diagnostics.append(
                        _diag(
                            f"BODY-LINK-{direction.upper()}",
                            path,
                            profile.profile_id,
                            f"a repository-local link or explicit exclusion in {column}",
                            f"row {row_number}: {cell}",
                        )
                    )
                    continue
                for raw_link in raw_links:
                    kind, target = _local_destination(path, raw_link)
                    if kind not in {"local", "anchor"} or target not in known_paths:
                        diagnostics.append(
                            _diag(
                                "BODY-LINK-BROKEN",
                                path,
                                profile.profile_id,
                                "a tracked local lifecycle document",
                                raw_link,
                            )
                        )
                        continue
                    assert target is not None
                    target_view = context.profiles[target]
                    if target_view.profile_id not in allowed_profile_ids:
                        diagnostics.append(
                            _diag(
                                f"BODY-LINK-{direction.upper()}-PROFILE",
                                path,
                                profile.profile_id,
                                json.dumps(allowed_profile_ids),
                                target_view.profile_id,
                            )
                        )
                        continue
                    target_profile = profiles_by_id[target_view.profile_id]
                    target_status_value = context.metadata[target].get("status", "")
                    target_status = (
                        target_status_value
                        if isinstance(target_status_value, str)
                        else ""
                    )
                    reciprocal_in_scope = _body_contract_link_is_enforced(
                        target,
                        target_profile,
                        target_status,
                        body_contracts,
                        path_prefixes,
                    )
                    if (
                        contract.reciprocal_evidence
                        and reciprocal_in_scope
                        and not _links_back_to(context, target, path)
                    ):
                        diagnostics.append(
                            _diag(
                                "BODY-LINK-RECIPROCAL",
                                path,
                                profile.profile_id,
                                f"{target.as_posix()} links back to {path.as_posix()}",
                                f"row {row_number}, {column}: missing reciprocal evidence",
                            )
                        )
    return sorted(diagnostics, key=diagnostic_sort_key)


def _first_cell_target(
    owner: PurePosixPath, cell: str
) -> PurePosixPath | None:
    match = re.fullmatch(r"\[[^\]\n]+\]\(([^)]+)\)", cell)
    if match is None:
        return None
    raw = match.group(1).strip()
    if "?" in raw or "#" in raw:
        return None
    kind, target = _local_destination(owner, raw)
    return target if kind == "local" else None


def _collection_table_targets(
    declaration: CollectionIndex, text: str
) -> tuple[list[PurePosixPath], bool]:
    section = (
        _after_exact_heading(text, declaration.table_anchor)
        if declaration.table_mode == "after"
        else _exact_heading_section(text, declaration.table_anchor)
    )
    if section is None:
        return [], False
    table = _first_visible_table(section)
    if table is None:
        return [], False
    _, rows = table
    targets: list[PurePosixPath] = []
    for row in rows:
        target = _first_cell_target(declaration.path, row[0])
        if target is None:
            return [], False
        targets.append(target)
    return targets, True


def _collection_index_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for declaration in COLLECTION_INDEXES:
        profile = context.profiles[declaration.path].profile_id
        expected = {
            path
            for path in context.tracked_regular_paths
            if declaration.target_pattern.fullmatch(path.as_posix())
        }
        tree, tree_valid = _collection_tree_targets(
            declaration, context.texts[declaration.path]
        )
        rows, table_valid = _collection_table_targets(
            declaration, context.texts[declaration.path]
        )
        expected_rows = set(expected)
        if not declaration.table_includes_self:
            expected_rows.discard(declaration.path)
        if not tree_valid or not table_valid:
            diagnostics.append(
                _diag(
                    "COLLECTION-INDEX-PARSE",
                    declaration.path,
                    profile,
                    "one exact heading, bounded tree, and first-cell link table",
                    "collection index grammar is missing or malformed",
                )
            )
            continue
        tree_counter = collections.Counter(tree)
        row_counter = collections.Counter(rows)
        for target in sorted(expected | set(tree), key=lambda item: item.as_posix()):
            target_key = target.as_posix()
            if target in expected and tree_counter[target] == 0:
                diagnostics.append(_diag("COLLECTION-INDEX-TREE-MISSING", declaration.path, profile, f"target={target_key}; one tree entry", f"target={target_key}; entry is missing"))
            if target not in expected and tree_counter[target]:
                diagnostics.append(_diag("COLLECTION-INDEX-TREE-STALE", declaration.path, profile, f"target={target_key}; tracked canonical artifact", f"target={target_key}; stale tree entry"))
            if tree_counter[target] > 1:
                diagnostics.append(_diag("COLLECTION-INDEX-TREE-DUPLICATE", declaration.path, profile, f"target={target_key}; one tree entry", f"target={target_key}; {tree_counter[target]} entries"))
        for target in sorted(expected_rows | set(rows), key=lambda item: item.as_posix()):
            target_key = target.as_posix()
            if target in expected_rows and row_counter[target] == 0:
                diagnostics.append(_diag("COLLECTION-INDEX-ROW-MISSING", declaration.path, profile, f"target={target_key}; one table row", f"target={target_key}; row is missing"))
            if target not in expected_rows and row_counter[target]:
                diagnostics.append(_diag("COLLECTION-INDEX-ROW-STALE", declaration.path, profile, f"target={target_key}; tracked canonical artifact", f"target={target_key}; stale table row"))
            if row_counter[target] > 1:
                diagnostics.append(_diag("COLLECTION-INDEX-ROW-DUPLICATE", declaration.path, profile, f"target={target_key}; one table row", f"target={target_key}; {row_counter[target]} rows"))
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


def _reference_collection_rows(
    context: Context, collection: str
) -> list[PurePosixPath] | None:
    declaration = next(
        pack
        for pack in context.reference_current_packs.packs
        if pack.id.startswith(collection + "/")
    )
    heading = (
        "### Research Pack Index"
        if collection == "research"
        else "### Audit Pack Registry"
    )
    expected_parent = "## Item Index"
    text = context.texts.get(declaration.collection_readme)
    if text is None:
        return None
    visible = _visible_markdown(text).splitlines()
    matches = [index for index, line in enumerate(visible) if line == heading]
    if len(matches) != 1:
        return None
    parent = next(
        (
            line
            for line in reversed(visible[: matches[0]])
            if re.match(r"^##\s", line)
        ),
        "",
    )
    if parent != expected_parent:
        return None
    section = _exact_heading_section(text, heading)
    table = _first_visible_table(section or "")
    if table is None:
        return None
    header, rows = table
    role_indexes = [
        index
        for index, cell in enumerate(header)
        if cell.casefold() in {"status", "pack role"}
    ]
    if len(role_indexes) != 1:
        return None
    current: list[PurePosixPath] = []
    for row in rows:
        if row[role_indexes[0]].casefold() != "current pack":
            continue
        target = _first_cell_target(declaration.collection_readme, row[0])
        if target is None:
            return None
        current.append(target)
    return current


def _reference_pack_rows(
    context: Context, pack_readme: PurePosixPath
) -> list[tuple[PurePosixPath, str]] | None:
    text = context.texts.get(pack_readme)
    if text is None:
        return None
    section = _exact_heading_section(text, "## Report Index")
    table = _first_visible_table(section or "")
    if table is None:
        return None
    header, rows = table
    lifecycle_indexes = [
        index for index, cell in enumerate(header) if cell.casefold() == "lifecycle"
    ]
    if len(lifecycle_indexes) != 1:
        return None
    lifecycle_index = lifecycle_indexes[0]
    parsed: list[tuple[PurePosixPath, str]] = []
    for row in rows:
        target = _first_cell_target(pack_readme, row[0])
        if target is None:
            return None
        if (
            target.parent != pack_readme.parent
            or target == pack_readme
            or target.suffix != ".md"
        ):
            continue
        match = re.fullmatch(r"`([a-z][a-z0-9-]*)`", row[lifecycle_index])
        if match is None:
            parsed.append((target, ""))
        else:
            parsed.append((target, match.group(1)))
    return parsed


def _reference_current_pack_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for pack in context.reference_current_packs.packs:
        collection = pack.id.split("/", 1)[0]
        collection_profile = context.profiles[pack.collection_readme].profile_id
        current_rows = _reference_collection_rows(context, collection)
        if current_rows is None:
            diagnostics.append(_diag("REFERENCE-PACK-COLLECTION-MISSING", pack.collection_readme, collection_profile, f"one Current pack row for {pack.pack_readme.as_posix()}", "heading or table is missing or malformed"))
        else:
            counter = collections.Counter(current_rows)
            if counter[pack.pack_readme] == 0:
                diagnostics.append(_diag("REFERENCE-PACK-COLLECTION-MISSING", pack.collection_readme, collection_profile, f"one Current pack row for {pack.pack_readme.as_posix()}", "declared Current row is missing"))
            for target in sorted(set(current_rows) - {pack.pack_readme}, key=lambda item: item.as_posix()):
                diagnostics.append(_diag("REFERENCE-PACK-COLLECTION-STALE", pack.collection_readme, collection_profile, f"Current pack target={pack.pack_readme.as_posix()}", f"Current pack target={target.as_posix()}"))
            for target, count in sorted(counter.items(), key=lambda item: item[0].as_posix()):
                if count > 1 or len(current_rows) > 1:
                    diagnostics.append(_diag("REFERENCE-PACK-COLLECTION-DUPLICATE", pack.collection_readme, collection_profile, "one visible Current pack row", f"target={target.as_posix()}; total={len(current_rows)}; count={count}"))

        declared_order = list(pack.member_paths)
        declared = set(declared_order)
        tracked = {
            path
            for path in context.paths
            if path.parent == pack.pack_readme.parent
            and path != pack.pack_readme
            and path.suffix == ".md"
            and context.profiles[path].profile_id
            == context.reference_current_packs.profile_id
            and context.profiles[path].mode == "authored"
        }
        for path in sorted(tracked - declared, key=lambda item: item.as_posix()):
            diagnostics.append(_diag("REFERENCE-PACK-OWNER-UNDECLARED", path, context.profiles[path].profile_id, f"member declared in Current pack {pack.id}", "tracked direct member is undeclared"))
        for path in declared_order:
            profile = context.profiles.get(path)
            if profile is None or profile.profile_id != context.reference_current_packs.profile_id or profile.mode != "authored":
                diagnostics.append(_diag("REGISTRY_REFERENCE_CURRENT_PACK_PROFILE", path, profile.profile_id if profile else context.reference_current_packs.profile_id, f"authored {context.reference_current_packs.profile_id}", "declared member is missing or has the wrong profile"))
                continue
            status = str(context.metadata[path].get("status", "")).casefold()
            if status not in pack.allowed_states:
                diagnostics.append(_diag("REFERENCE-PACK-OWNER-STATUS", path, profile.profile_id, f"status in {list(pack.allowed_states)!r}", status or "missing"))

        rows = _reference_pack_rows(context, pack.pack_readme)
        pack_profile = context.profiles[pack.pack_readme].profile_id
        if rows is None:
            diagnostics.append(_diag("REFERENCE-PACK-INDEX-MISSING", pack.pack_readme, pack_profile, "one exact Report Index with one Lifecycle column", "heading or table is missing or malformed"))
            continue
        row_paths = [path for path, _ in rows]
        row_counter = collections.Counter(row_paths)
        for path in declared_order:
            if row_counter[path] == 0:
                diagnostics.append(_diag("REFERENCE-PACK-INDEX-MISSING", pack.pack_readme, pack_profile, f"one row for {path.as_posix()}", "declared member row is missing"))
        for path in sorted(set(row_paths) - declared, key=lambda item: item.as_posix()):
            diagnostics.append(_diag("REFERENCE-PACK-INDEX-STALE", pack.pack_readme, pack_profile, "registry-declared direct sibling", f"stale row for {path.as_posix()}"))
        for path, count in sorted(row_counter.items(), key=lambda item: item[0].as_posix()):
            if count > 1:
                diagnostics.append(_diag("REFERENCE-PACK-INDEX-DUPLICATE", pack.pack_readme, pack_profile, f"one row for {path.as_posix()}", f"{count} rows"))
        for path, lifecycle in rows:
            if path not in declared:
                continue
            expected_status = str(context.metadata.get(path, {}).get("status", "")).casefold()
            if lifecycle != expected_status:
                diagnostics.append(_diag("REFERENCE-PACK-INDEX-STATUS", pack.pack_readme, pack_profile, f"{path.as_posix()} lifecycle={expected_status}", f"lifecycle={lifecycle or 'malformed'}"))
        if (
            len(row_paths) == len(declared_order)
            and collections.Counter(row_paths) == collections.Counter(declared_order)
            and row_paths != declared_order
        ):
            diagnostics.append(_diag("REFERENCE-PACK-INDEX-ORDER", pack.pack_readme, pack_profile, "member rows in registry order", "member row order differs"))
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


def _raw_diagnostics(
    context: Context,
    profiles_by_id: dict[str, DocumentProfile],
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    diagnostics = _link_diagnostics(context)
    diagnostics.extend(
        _body_contract_link_diagnostics(
            context,
            profiles_by_id,
            body_contracts,
            body_contract_path_prefixes,
        )
    )
    diagnostics.extend(_index_diagnostics(context))
    diagnostics.extend(_collection_index_diagnostics(context))
    diagnostics.extend(_governance_current_owner_diagnostics(context))
    diagnostics.extend(_reference_current_pack_diagnostics(context))
    diagnostics.extend(_owner_diagnostics(context))
    diagnostics.extend(_ledger_diagnostics(context))
    return sorted(diagnostics, key=diagnostic_sort_key)


def validate_cross_document_contracts(
    root: Path,
    mode: str,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Return deterministic raw cross-document diagnostics."""

    if mode not in {"compatibility", "strict"}:
        raise ConfigurationError("mode must be compatibility or strict")
    context = _build_context(root)
    _load_debt(context.root, mode=mode)
    registry = load_registry(context.root)
    profiles_by_id = {
        profile.profile_id: profile for profile in registry.profiles
    }
    return _raw_diagnostics(
        context,
        profiles_by_id,
        body_contracts,
        body_contract_path_prefixes,
    )


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
        "collectionArtifacts",
        "declaredIndexes",
        "ledgerColumns",
        "symlinkAdapters",
        "governanceCurrentOwners",
        "governanceMirrorPath",
        "referenceCurrentPacks",
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
    collection_artifacts = tuple(
        PurePosixPath(value) for value in tree["collectionArtifacts"]
    )
    if collection_artifacts != tuple(
        sorted(collection_artifacts, key=lambda path: path.as_posix())
    ) or len(collection_artifacts) != len(set(collection_artifacts)):
        raise ConfigurationError("fixture collection artifacts must be sorted and unique")
    raw_reference = tree["referenceCurrentPacks"]
    if list(raw_reference) != ["profileId", "packs"]:
        raise ConfigurationError("fixture reference Current-pack declaration differs")
    reference_current_packs = ReferenceCurrentPacks(
        profile_id=raw_reference["profileId"],
        packs=tuple(
            ReferenceCurrentPack(
                id=item["id"],
                allowed_states=tuple(item["allowedStates"]),
                members=tuple(item["members"]),
            )
            for item in raw_reference["packs"]
        ),
    )

    def authored(title: str, doc_type: str, status: str, body: str) -> str:
        return f"---\ntitle: {title}\ntype: {doc_type}\nstatus: {status}\nowner: platform\nupdated: 2026-07-12\n---\n\n# {title}\n\n{body}\n"

    texts: dict[PurePosixPath, str] = {}
    profile_map: dict[PurePosixPath, ProfileView] = {}
    for item, path in zip(documents, paths, strict=True):
        profile_map[path] = ProfileView(item["profile"], item["profileClass"], item["mode"])
        if item["mode"] in {"frontmatter-free", "classification-only"}:
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
    for path in collection_artifacts:
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("{}\n", encoding="utf-8")
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
        reference_current_packs,
        frozenset((*paths, *collection_artifacts)),
    )


def _mutated_context(context: Context, mutation: str) -> Context:
    paths = context.paths
    profiles = dict(context.profiles)
    texts = dict(context.texts)
    metadata = copy.deepcopy(context.metadata)
    governance_current_paths = context.governance_current_paths
    reference_current_packs = context.reference_current_packs
    tracked_regular_paths = context.tracked_regular_paths
    source = PurePosixPath("docs/05.operations/guides/9999-source.md")
    if mutation == "link-broken": texts[source] += "\n[bad](./missing.md)\n"
    elif mutation == "link-absolute": texts[source] += "\n[bad](/etc/passwd)\n"
    elif mutation == "link-file-uri": texts[source] += "\n[bad](file:///tmp/x)\n"
    elif mutation == "link-escape": texts[source] += "\n[bad](../../../../escape.md)\n"
    elif mutation == "link-archive-bypass": texts[source] += "\n[bad](../../98.archive/999-fixture.md)\n"
    elif mutation == "link-adapter-missing": texts[source] += "\n[bad](../../../.claude/skills/missing/skill.md)\n"
    elif mutation == "links-excluded": texts[source] += "\n```md\n[bad](./missing.md)\n```\n<!-- [bad](./missing.md) -->\n"
    elif mutation == "link-inline-code-excluded":
        texts[source] += (
            "\n`[inline](./missing-inline.md)`\n"
            "``[full][missing full] [collapsed][] [shortcut]``\n"
            "```[different](./missing-different.md)```\n"
            "[missing full]: ./missing-full.md\n"
            "[collapsed]: ./missing-collapsed.md\n"
            "[shortcut]: ./missing-shortcut.md\n"
        )
    elif mutation == "link-odd-escaped-excluded":
        texts[source] += (
            "\n\\[inline](./missing-inline.md)\n"
            "\\[full][missing full]\n"
            "\\[collapsed][]\n"
            "\\[shortcut]\n"
            "[missing full]: ./missing-full.md\n"
            "[collapsed]: ./missing-collapsed.md\n"
            "[shortcut]: ./missing-shortcut.md\n"
        )
    elif mutation == "link-even-escaped-active":
        texts[source] += (
            "\n\\\\[inline](./missing-inline.md)\n"
            "\\\\[full][missing full]\n"
            "\\\\[collapsed][]\n"
            "\\\\[shortcut]\n"
            "[missing full]: ./missing-full.md\n"
            "[collapsed]: ./missing-collapsed.md\n"
            "[shortcut]: ./missing-shortcut.md\n"
        )
    elif mutation in {
        "link-even-escaped-inline",
        "link-even-escaped-full-reference",
        "link-even-escaped-collapsed-reference",
        "link-even-escaped-shortcut-reference",
    }:
        rendered = {
            "link-even-escaped-inline": "\\\\[inline](./missing-inline.md)",
            "link-even-escaped-full-reference": "\\\\[full][missing full]",
            "link-even-escaped-collapsed-reference": "\\\\[collapsed][]",
            "link-even-escaped-shortcut-reference": "\\\\[escaped shortcut]",
        }
        texts[source] += (
            f"\n{rendered[mutation]}\n"
            "[missing full]: ./missing-full.md\n"
            "[collapsed]: ./missing-collapsed.md\n"
            "[shortcut]: ./missing-shortcut.md\n"
            "[escaped shortcut]: ./missing-escaped-shortcut.md\n"
        )
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
    elif mutation in {"reference-valid", "collection-valid", "collection-machine-json"}:
        pass
    elif mutation in {
        "reference-research-draft",
        "reference-audit-draft",
        "reference-audit-active",
    }:
        target = {
            "reference-research-draft": PurePosixPath(
                "docs/90.references/research/2026-07-07-wer/accepted.md"
            ),
            "reference-audit-draft": PurePosixPath(
                "docs/90.references/audits/2026-07-11-weia/audit.md"
            ),
            "reference-audit-active": PurePosixPath(
                "docs/90.references/audits/2026-07-11-weia/audit.md"
            ),
        }[mutation]
        status = "active" if mutation == "reference-audit-active" else "draft"
        old_status = str(metadata[target]["status"])
        metadata[target]["status"] = status
        pack_readme = target.parent / "README.md"
        texts[pack_readme] = texts[pack_readme].replace(
            f"[{target.stem}]({target.name}) | `{old_status}` |",
            f"[{target.stem}]({target.name}) | `{status}` |",
        )
    elif mutation == "reference-active-undeclared":
        target = PurePosixPath(
            "docs/90.references/research/2026-07-07-wer/undeclared.md"
        )
        paths = tuple(sorted((*paths, target), key=lambda item: item.as_posix()))
        profiles[target] = ProfileView("content/reference", "common", "authored")
        metadata[target] = {
            "title": "Undeclared",
            "type": "content/reference",
            "status": "active",
            "owner": "platform",
            "updated": "2026-07-14",
        }
        texts[target] = "# Undeclared\n"
        tracked_regular_paths = frozenset((*tracked_regular_paths, target))
    elif mutation == "reference-declared-missing":
        target = PurePosixPath(
            "docs/90.references/research/2026-07-07-wer/accepted.md"
        )
        paths = tuple(path for path in paths if path != target)
        profiles.pop(target)
        metadata.pop(target)
        texts.pop(target)
        tracked_regular_paths = frozenset(
            path for path in tracked_regular_paths if path != target
        )
    elif mutation.startswith("reference-collection-"):
        owner = PurePosixPath("docs/90.references/research/README.md")
        row = "| [current](./2026-07-07-wer/README.md) | Current pack |"
        if mutation == "reference-collection-missing":
            texts[owner] = texts[owner].replace(row + "\n", "")
        elif mutation == "reference-collection-stale":
            texts[owner] = texts[owner].replace(
                row, "| [current](./2026-07-08-stale/README.md) | Current pack |"
            )
        elif mutation == "reference-collection-duplicate":
            texts[owner] = texts[owner].replace(row, f"{row}\n{row}")
        elif mutation == "reference-collection-wrong-parent":
            texts[owner] = texts[owner].replace(
                "### Research Pack Index",
                "## Wrong Parent\n\n### Research Pack Index",
            )
        elif mutation == "reference-collection-fenced-lookalike":
            texts[owner] = texts[owner].replace(
                "### Research Pack Index", "Research Pack Index"
            ) + "\n```markdown\n### Research Pack Index\n" + row + "\n```\n"
    elif mutation.startswith("reference-index-"):
        owner = PurePosixPath(
            "docs/90.references/research/2026-07-07-wer/README.md"
        )
        accepted = "| [accepted](accepted.md) | `accepted` |"
        active = "| [active](active.md) | `active` |"
        if mutation == "reference-index-missing":
            texts[owner] = texts[owner].replace(accepted + "\n", "")
        elif mutation == "reference-index-malformed":
            texts[owner] = texts[owner].replace("| Reference | Lifecycle |", "| Reference | Status |")
        elif mutation == "reference-index-stale":
            texts[owner] = texts[owner].replace(active, active + "\n| [ghost](ghost.md) | `active` |")
        elif mutation == "reference-index-duplicate":
            texts[owner] = texts[owner].replace(accepted, accepted + "\n" + accepted)
        elif mutation == "reference-index-status":
            texts[owner] = texts[owner].replace(accepted, "| [accepted](accepted.md) | `active` |")
        elif mutation == "reference-index-swap":
            texts[owner] = texts[owner].replace(accepted, "| [ghost](ghost.md) | `accepted` |")
        elif mutation == "reference-index-order":
            texts[owner] = texts[owner].replace(f"{accepted}\n{active}", f"{active}\n{accepted}")
        elif mutation == "reference-index-fenced-lookalike":
            texts[owner] = texts[owner].replace("## Report Index", "Report Index") + "\n```markdown\n## Report Index\n```\n"
    elif mutation == "reference-wrong-profile-member":
        target = PurePosixPath(
            "docs/90.references/research/2026-07-07-wer/accepted.md"
        )
        profiles[target] = ProfileView("content/archive-tombstone", "common", "authored")
    elif mutation.startswith("collection-"):
        owner = PurePosixPath(
            "docs/90.references/research/2026-07-07-wer/README.md"
        )
        tree_line = "├── accepted.md"
        row = "| [accepted](accepted.md) | `accepted` |"
        ghost_line = "├── ghost.md"
        ghost_row = "| [ghost](ghost.md) | `accepted` |"
        if mutation == "collection-tree-missing":
            texts[owner] = texts[owner].replace(tree_line + "\n", "")
        elif mutation == "collection-row-missing":
            texts[owner] = texts[owner].replace(row + "\n", "")
        elif mutation == "collection-tree-stale":
            texts[owner] = texts[owner].replace(tree_line, tree_line + "\n" + ghost_line)
        elif mutation == "collection-row-stale":
            texts[owner] = texts[owner].replace(row, row + "\n" + ghost_row)
        elif mutation == "collection-tree-duplicate":
            texts[owner] = texts[owner].replace(tree_line, tree_line + "\n" + tree_line)
        elif mutation == "collection-row-duplicate":
            texts[owner] = texts[owner].replace(row, row + "\n" + row)
        elif mutation == "collection-equal-count-swap":
            texts[owner] = texts[owner].replace(tree_line, ghost_line).replace(row, ghost_row)
        elif mutation == "collection-artifact-added":
            target = owner.parent / "added.md"
            paths = tuple(sorted((*paths, target), key=lambda item: item.as_posix()))
            profiles[target] = ProfileView("content/reference", "common", "authored")
            metadata[target] = {"title": "Added", "type": "content/reference", "status": "accepted", "owner": "platform", "updated": "2026-07-14"}
            texts[target] = "# Added\n"
            tracked_regular_paths = frozenset((*tracked_regular_paths, target))
        elif mutation == "collection-artifact-removed":
            target = owner.parent / "accepted.md"
            paths = tuple(path for path in paths if path != target)
            profiles.pop(target)
            metadata.pop(target)
            texts.pop(target)
            tracked_regular_paths = frozenset(path for path in tracked_regular_paths if path != target)
        elif mutation == "collection-heading-lookalike":
            texts[owner] = texts[owner].replace("### Structure", "Structure") + "\n```markdown\n### Structure\n```\n"
        elif mutation == "collection-tree-comment":
            texts[owner] = texts[owner].replace(tree_line, tree_line + " # retained")
        elif mutation == "collection-tree-comment-hidden":
            block = "```text\n2026-07-07-wer/\n├── README.md # pack index\n├── accepted.md\n├── active.md\n└── document-migration-evidence-ledger.md\n```"
            texts[owner] = texts[owner].replace(block, f"<!--\n{block}\n-->")
        elif mutation == "collection-h1-status-prose":
            variants = (
                (
                    owner,
                    "| [accepted](accepted.md) | `accepted` |",
                    "| [accepted](accepted.md) | Status: Current \\| explanatory prose |",
                ),
                (
                    PurePosixPath("docs/99.templates/support/README.md"),
                    "| [Common](./common.md) | common |",
                    "| [Common](./common.md) |",
                ),
                (
                    PurePosixPath("docs/90.references/research/README.md"),
                    "| [active](./2026-07-07-wer/active.md) | Included |",
                    "| [active](./2026-07-07-wer/active.md) | Included | ignored |",
                ),
            )
            for target, before, after in variants:
                if texts[target].count(before) != 1:
                    raise ConfigurationError(
                        "collection-h1-status-prose fixture variant is missing: "
                        f"{target.as_posix()}"
                    )
                texts[target] = texts[target].replace(before, after)
    return Context(
        context.root,
        paths,
        context.baseline_paths,
        profiles,
        texts,
        metadata,
        context.adapter_targets,
        governance_current_paths,
        context.governance_current_states,
        reference_current_packs,
        tracked_regular_paths,
    )


def _body_contract_fixture_context(
    root: Path,
    tree: dict[str, Any],
    profiles_by_id: dict[str, DocumentProfile],
) -> Context:
    if list(tree) != ["documents"] or not isinstance(tree["documents"], list):
        raise ConfigurationError("body-contract fixture tree differs")
    expected_keys = ["path", "profile", "status", "body"]
    if any(
        not isinstance(item, dict) or list(item) != expected_keys
        for item in tree["documents"]
    ):
        raise ConfigurationError("body-contract fixture document keys differ")
    paths = tuple(PurePosixPath(item["path"]) for item in tree["documents"])
    if paths != tuple(sorted(paths, key=lambda item: item.as_posix())):
        raise ConfigurationError("body-contract fixture paths must be sorted")
    profile_views: dict[PurePosixPath, ProfileView] = {}
    texts: dict[PurePosixPath, str] = {}
    metadata: dict[PurePosixPath, dict[str, Any]] = {}
    for item, path in zip(tree["documents"], paths, strict=True):
        profile = profiles_by_id[item["profile"]]
        profile_views[path] = _profile_view(profile)
        texts[path] = item["body"]
        metadata[path] = {"status": item["status"]}
    return Context(
        root,
        paths,
        frozenset(),
        profile_views,
        texts,
        metadata,
        {},
        (),
        (),
        ReferenceCurrentPacks("content/reference", ()),
        frozenset(paths),
    )


def _mutated_body_contract_context(context: Context, mutation: str) -> Context:
    mutated = copy.deepcopy(context)
    prd = PurePosixPath("docs/01.requirements/999-fixture.md")
    spec = PurePosixPath("docs/03.specs/999-fixture/spec.md")
    plan = PurePosixPath("docs/04.execution/plans/2026-07-15-fixture.md")
    incident = PurePosixPath(
        "docs/05.operations/incidents/2026-07-15-INC-999.md"
    )
    if mutation in {"none", "feedback-positive"}:
        return mutated
    if mutation == "disallowed-source-profile":
        mutated.texts[plan] = mutated.texts[plan].replace(
            "../../03.specs/999-fixture/spec.md",
            "../../01.requirements/999-fixture.md",
            1,
        )
    elif mutation == "disallowed-target-profile":
        mutated.texts[prd] = mutated.texts[prd].replace(
            "../03.specs/999-fixture/spec.md",
            "../04.execution/tasks/2026-07-15-fixture.md",
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
        )
    elif mutation == "missing-source-link":
        mutated.texts[plan] = mutated.texts[plan].replace(
            "[VAL-FIXTURE-001](../../03.specs/999-fixture/spec.md)",
            "VAL-FIXTURE-001",
            1,
        )
    elif mutation == "missing-target-link":
        mutated.texts[prd] = mutated.texts[prd].replace(
            "[Spec](../03.specs/999-fixture/spec.md)",
            "Specification owner",
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
        )
    elif mutation == "broken-link":
        mutated.texts[plan] = mutated.texts[plan].replace(
            "../tasks/2026-07-15-fixture.md",
            "../tasks/2099-01-01-missing.md",
            1,
        )
        mutated.texts[plan] += (
            "\n[Task reciprocal](../tasks/2026-07-15-fixture.md)\n"
        )
    elif mutation == "missing-reciprocal":
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[REQ-FIXTURE-001](../../01.requirements/999-fixture.md)",
            "N/A — standalone specification",
            1,
        )
    elif mutation == "exclusion-without-reason":
        mutated.texts[incident] = mutated.texts[incident].replace(
            "[Task](../../04.execution/tasks/2026-07-15-fixture.md)",
            "N/A",
            1,
        )
    elif mutation == "done-status":
        mutated.metadata[prd]["status"] = "done"
        mutated.texts[prd] = mutated.texts[prd].replace(
            "../03.specs/999-fixture/spec.md",
            "../04.execution/tasks/2026-07-15-fixture.md",
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
        )
    elif mutation == "three-space-disallowed-target":
        mutated.texts[prd] = mutated.texts[prd].replace("\n|", "\n   |")
        mutated.texts[prd] = mutated.texts[prd].replace(
            "../03.specs/999-fixture/spec.md",
            "../04.execution/tasks/2026-07-15-fixture.md",
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
        )
    elif mutation == "commented-fence-disallowed-target":
        mutated.texts[prd] = mutated.texts[prd].replace(
            "### Lifecycle Traceability\n\n|",
            "### Lifecycle Traceability\n\n<!--\n```markdown\n-->\n|",
            1,
        )
        mutated.texts[prd] = mutated.texts[prd].replace(
            "../03.specs/999-fixture/spec.md",
            "../04.execution/tasks/2026-07-15-fixture.md",
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
        )
    elif mutation in {
        "full-reference-disallowed-target",
        "collapsed-reference-disallowed-target",
        "shortcut-reference-disallowed-target",
        "full-reference-whitespace-target",
        "collapsed-reference-whitespace-target",
        "shortcut-reference-whitespace-target",
    }:
        labels = {
            "full-reference-disallowed-target": "[Task][wrong-target]",
            "collapsed-reference-disallowed-target": "[wrong-target][]",
            "shortcut-reference-disallowed-target": "[wrong-target]",
            "full-reference-whitespace-target": "[Task][wrong   target]",
            "collapsed-reference-whitespace-target": "[wrong\t\t target][]",
            "shortcut-reference-whitespace-target": "[wrong\t target]",
        }
        definition_labels = {
            "full-reference-whitespace-target": "wrong\t target",
            "collapsed-reference-whitespace-target": "wrong target",
            "shortcut-reference-whitespace-target": "wrong   target",
        }
        mutated.texts[prd] = mutated.texts[prd].replace(
            "[Spec](../03.specs/999-fixture/spec.md)",
            labels[mutation],
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal]\n\n"
            f"[{definition_labels.get(mutation, 'wrong-target')}]: "
            "../04.execution/tasks/2026-07-15-fixture.md\n"
            "[Spec reciprocal]: ../03.specs/999-fixture/spec.md\n"
        )
    elif mutation in {
        "full-reference-duplicate-definition",
        "collapsed-reference-duplicate-definition",
        "shortcut-reference-duplicate-definition",
    }:
        labels = {
            "full-reference-duplicate-definition": "[Task][Dupe   Label]",
            "collapsed-reference-duplicate-definition": "[dupe\tlabel][]",
            "shortcut-reference-duplicate-definition": "[dupe label]",
        }
        mutated.texts[prd] = mutated.texts[prd].replace(
            "[Spec](../03.specs/999-fixture/spec.md)",
            labels[mutation],
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n\n"
            "[ DUPE\tLABEL ]: ../04.execution/tasks/2026-07-15-fixture.md\n"
            "[dupe   label]: ../03.specs/999-fixture/spec.md\n"
        )
    elif mutation in {
        "inline-code-nonrendered-target",
        "odd-escaped-nonrendered-target",
        "even-escaped-rendered-target",
        "even-escaped-inline-target",
        "even-escaped-full-reference-target",
        "even-escaped-collapsed-reference-target",
        "even-escaped-shortcut-reference-target",
    }:
        labels = {
            "inline-code-nonrendered-target": (
                "`[Task](../04.execution/tasks/2026-07-15-fixture.md)` "
                "``[Task][bad ref] [bad ref][]`` ```[bad ref]```"
            ),
            "odd-escaped-nonrendered-target": (
                "\\[Task](../04.execution/tasks/2026-07-15-fixture.md), "
                "\\[Task][bad ref], \\[bad ref][], \\[bad ref]"
            ),
            "even-escaped-rendered-target": (
                "\\\\[Task](../04.execution/tasks/2026-07-15-fixture.md), "
                "\\\\[Task][bad ref], \\\\[bad ref][], \\\\[bad ref]"
            ),
            "even-escaped-inline-target": (
                "\\\\[Task](../04.execution/tasks/2026-07-15-fixture.md)"
            ),
            "even-escaped-full-reference-target": "\\\\[Task][bad ref]",
            "even-escaped-collapsed-reference-target": "\\\\[bad ref][]",
            "even-escaped-shortcut-reference-target": "\\\\[bad ref]",
        }
        mutated.texts[prd] = mutated.texts[prd].replace(
            "[Spec](../03.specs/999-fixture/spec.md)",
            labels[mutation],
            1,
        )
        mutated.texts[prd] += (
            "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n\n"
            "[bad ref]: ../04.execution/tasks/2026-07-15-fixture.md\n"
        )
    elif mutation in {
        "blank-line-after-delimiter",
        "html-comment-after-delimiter",
    }:
        spacing = (
            "\n\n"
            if mutation == "blank-line-after-delimiter"
            else "\n<!-- spacing -->\n"
        )
        mutated.texts[prd] = mutated.texts[prd].replace(
            "| --- | --- | --- |\n| REQ-FIXTURE-001",
            f"| --- | --- | --- |{spacing}| REQ-FIXTURE-001",
            1,
        )
    else:
        raise ConfigurationError(
            f"unknown body-contract fixture mutation: {mutation}"
        )
    return mutated


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
                mutated.reference_current_packs,
                mutated.tracked_regular_paths,
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
    elif mutation.startswith("reference"):
        diagnostics = _reference_current_pack_diagnostics(mutated)
    elif mutation.startswith("collection"):
        diagnostics = _collection_index_diagnostics(mutated)
        return [
            item.rule_id
            for item in sorted(diagnostics, key=diagnostic_sort_key)
        ]
    elif mutation in {"none", "link-normalization"}:
        diagnostics = (
            _link_diagnostics(mutated)
            + _index_diagnostics(mutated)
            + _collection_index_diagnostics(mutated)
            + _governance_current_owner_diagnostics(mutated)
            + _reference_current_pack_diagnostics(mutated)
            + _owner_diagnostics(mutated)
            + _ledger_diagnostics(mutated)
        )
    else:
        raise ConfigurationError(f"unknown fixture mutation: {mutation}")
    return sorted(set(item.rule_id for item in diagnostics))


def _self_test(root: Path) -> list[str]:
    fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
    failures: list[str] = []
    if list(fixture) != [
        "schemaVersion",
        "baseTree",
        "bodyContractTree",
        "bodyContractCases",
        "cases",
    ] or fixture["schemaVersion"] != 2:
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
        "reference-valid",
        "reference-research-draft",
        "reference-audit-draft",
        "reference-audit-active",
        "reference-active-undeclared",
        "reference-declared-missing",
        "reference-collection-missing",
        "reference-collection-stale",
        "reference-collection-duplicate",
        "reference-collection-wrong-parent",
        "reference-collection-fenced-lookalike",
        "reference-index-missing",
        "reference-index-malformed",
        "reference-index-stale",
        "reference-index-duplicate",
        "reference-index-status",
        "reference-index-equal-count-swap",
        "reference-index-order",
        "reference-index-fenced-lookalike",
        "reference-wrong-profile-member",
        "collection-valid",
        "collection-tree-missing",
        "collection-row-missing",
        "collection-tree-stale",
        "collection-row-stale",
        "collection-tree-duplicate",
        "collection-row-duplicate",
        "collection-equal-count-swap",
        "collection-artifact-added",
        "collection-artifact-removed",
        "collection-machine-json",
        "collection-heading-lookalike",
        "collection-tree-comment",
        "collection-tree-comment-hidden",
        "collection-h1-status-prose",
    }
    names = [case.get("name") for case in fixture["cases"]]
    if not required.issubset(names) or len(names) != len(set(names)):
        failures.append("required unique fixture cases are incomplete")
    body_shape_probe = _first_visible_table(
        "| Reference | Lifecycle |\n"
        "| --- | --- |\n"
        "| [short](short.md) |\n"
        "| [extra](extra.md) | `active` | ignored |\n"
    )
    if body_shape_probe != (
        ["Reference", "Lifecycle"],
        [["[short](short.md)", ""], ["[extra](extra.md)", "`active`"]],
    ):
        failures.append("GFM body rows are not padded/truncated to the header")
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
            expected = case["expected_rule_ids"]
            actual = _fixture_rule_ids(context, case["mutation"]["kind"])
            if actual != expected:
                failures.append(f"{case['name']}: expected {expected}, actual {actual}")
        registry = load_registry(root)
        profiles_by_id = {
            profile.profile_id: profile for profile in registry.profiles
        }
        body_context = _body_contract_fixture_context(
            Path(temporary), fixture["bodyContractTree"], profiles_by_id
        )
        body_validator = globals().get("_body_contract_link_diagnostics")
        body_case_keys = [
            "name",
            "mutation",
            "bodyContracts",
            "expected_rule_ids",
        ]
        for case in fixture["bodyContractCases"]:
            expected_case_keys = body_case_keys.copy()
            if "pathPrefixes" in case:
                expected_case_keys.insert(3, "pathPrefixes")
            if list(case) != expected_case_keys:
                failures.append(
                    f"{case.get('name')}: body-contract case schema differs"
                )
                continue
            if body_validator is None:
                failures.append(
                    f"{case['name']}: BODY-LINK rules are unimplemented"
                )
                continue
            mutated = _mutated_body_contract_context(
                body_context, case["mutation"]
            )
            try:
                diagnostics = body_validator(
                    mutated,
                    profiles_by_id,
                    case["bodyContracts"],
                    tuple(
                        PurePosixPath(value)
                        for value in case.get("pathPrefixes", [])
                    ),
                )
            except TypeError:
                failures.append(
                    f"{case['name']}: path-prefix scope is unimplemented"
                )
                continue
            actual = sorted({item.rule_id for item in diagnostics})
            if actual != case["expected_rule_ids"]:
                failures.append(
                    f"{case['name']}: expected {case['expected_rule_ids']}, actual {actual}"
                )
        try:
            default_body_contracts = _parser().parse_args([]).body_contracts
            audit_body_contracts = _parser().parse_args(
                ["--body-contracts", "audit"]
            ).body_contracts
            default_prefixes = _parser().parse_args(
                []
            ).body_contract_path_prefix
            repeated_prefixes = _parser().parse_args(
                [
                    "--body-contracts",
                    "audit",
                    "--body-contract-path-prefix",
                    "docs/01.requirements",
                    "--body-contract-path-prefix",
                    "docs/03.specs",
                ]
            ).body_contract_path_prefix
        except (AttributeError, SystemExit):
            failures.append("body-contract parser modes are unimplemented")
        else:
            if default_body_contracts != "registry" or audit_body_contracts != "audit":
                failures.append("body-contract parser mode defaults differ")
            expected_prefixes = [
                PurePosixPath("docs/01.requirements"),
                PurePosixPath("docs/03.specs"),
            ]
            if default_prefixes != [] or repeated_prefixes != expected_prefixes:
                failures.append("body-contract path-prefix parser differs")
        for invalid_prefix in (
            "",
            ".",
            "./docs/01.requirements",
            "/docs/01.requirements",
            "C:/docs/01.requirements",
            "../docs/01.requirements",
            "docs/../01.requirements",
            "docs/01.requirements/",
            "docs\\01.requirements",
        ):
            with contextlib.redirect_stderr(io.StringIO()):
                try:
                    _parser().parse_args(
                        ["--body-contract-path-prefix", invalid_prefix]
                    )
                except SystemExit as exc:
                    if exc.code == 2:
                        continue
            failures.append(
                "body-contract parser accepted invalid path prefix: "
                f"{invalid_prefix!r}"
            )
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


def _body_contract_path_prefix(value: str) -> PurePosixPath:
    """Parse one normalized repository-relative body-contract scope."""

    path = PurePosixPath(value)
    if (
        not value
        or value == "."
        or value != path.as_posix()
        or value.startswith("./")
        or path.is_absolute()
        or re.match(r"^[A-Za-z]:[/\\]", value) is not None
        or ".." in path.parts
        or "\\" in value
    ):
        raise argparse.ArgumentTypeError(
            "body-contract path prefix must be normalized and repository-relative"
        )
    return path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--mode", choices=("compatibility", "strict"), default="compatibility")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--body-contracts",
        choices=("registry", "audit"),
        default="registry",
        help="respect registry status scopes or audit all draft/active body contracts",
    )
    parser.add_argument(
        "--body-contract-path-prefix",
        action="append",
        default=[],
        type=_body_contract_path_prefix,
        help=(
            "limit forced audit enforcement to a repeatable normalized "
            "repository-relative prefix"
        ),
    )
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
        registry = load_registry(context.root)
        profiles_by_id = {
            profile.profile_id: profile for profile in registry.profiles
        }
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
                + _body_contract_link_diagnostics(
                    context,
                    profiles_by_id,
                    args.body_contracts,
                    tuple(args.body_contract_path_prefix),
                )
                + _index_diagnostics(context)
                + _collection_index_diagnostics(context)
                + _governance_current_owner_diagnostics(context)
                + _reference_current_pack_diagnostics(context)
                + _owner_diagnostics(context)
            )
            rows = [("FAIL", item) for item in sorted(diagnostics, key=diagnostic_sort_key)]
            envelope = _envelope("inventory", counts, _inventory_documents(context), rows)
            print(json.dumps(envelope, ensure_ascii=False, separators=(",", ":")))
            return int(bool(rows))
        diagnostics = _raw_diagnostics(
            context,
            profiles_by_id,
            args.body_contracts,
            tuple(args.body_contract_path_prefix),
        )
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
