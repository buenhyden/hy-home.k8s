#!/usr/bin/env python3
"""Validate repository-local links, indexes, current owners, and migration ledger."""

from __future__ import annotations

import argparse
import bisect
import collections
import contextlib
import copy
import html
import io
import json
import os
import posixpath
import re
import stat
import sys
import tempfile
import time
import unicodedata
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import unquote

import yaml

from document_contracts import (
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    ProgramFollowUp,
    ProgramLineage,
    ProgramRelation,
    ReferenceCurrentPack,
    ReferenceCurrentPacks,
    Registry,
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
    "path",
    "title",
    "profile",
    "owner-key",
    "disposition",
    "destination",
    "local-evidence",
    "official-sources",
    "observed-version",
    "applicability",
    "content-decision",
    "refresh-trigger",
    "reviewer",
    "result",
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
IMPLEMENTED_RULES = frozenset(
    {
        "BODY-LINK-BROKEN",
        "BODY-LINK-EXCLUSION",
        "BODY-LINK-RECIPROCAL",
        "BODY-LINK-SOURCE",
        "BODY-LINK-SOURCE-PROFILE",
        "BODY-LINK-TARGET",
        "BODY-LINK-TARGET-PROFILE",
        "LINK-BROKEN",
        "LINK-ABSOLUTE",
        "LINK-FILE-URI",
        "LINK-ESCAPE",
        "LINK-ARCHIVE-BYPASS",
        "INDEX-MISSING",
        "INDEX-STALE",
        "INDEX-DUPLICATE",
        "INDEX-STATUS",
        "INDEX-TREE",
        "OWNER-KEY-MISSING",
        "OWNER-DUPLICATE",
        "LEDGER-MISSING",
        "LEDGER-INCOMPLETE",
        "LEDGER-UNKNOWN-PATH",
        "DEBT-UNUSED",
        "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
        "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",
        "GOVERNANCE-OWNER-STATUS",
        "GOVERNANCE-OWNER-UNDECLARED",
        "GOVERNANCE-OWNER-ROUTE",
        "GOVERNANCE-INDEX-MISSING",
        "GOVERNANCE-INDEX-STALE",
        "GOVERNANCE-INDEX-DUPLICATE",
        "GOVERNANCE-INDEX-STATUS",
        "GOVERNANCE-INDEX-ORDER",
        "REFERENCE-PACK-OWNER-UNDECLARED",
        "REFERENCE-PACK-OWNER-STATUS",
        "REFERENCE-PACK-COLLECTION-MISSING",
        "REFERENCE-PACK-COLLECTION-STALE",
        "REFERENCE-PACK-COLLECTION-DUPLICATE",
        "REFERENCE-PACK-INDEX-MISSING",
        "REFERENCE-PACK-INDEX-STALE",
        "REFERENCE-PACK-INDEX-DUPLICATE",
        "REFERENCE-PACK-INDEX-STATUS",
        "REFERENCE-PACK-INDEX-ORDER",
        "REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",
        "COLLECTION-INDEX-PARSE",
        "COLLECTION-INDEX-TREE-MISSING",
        "COLLECTION-INDEX-TREE-STALE",
        "COLLECTION-INDEX-TREE-DUPLICATE",
        "COLLECTION-INDEX-ROW-MISSING",
        "COLLECTION-INDEX-ROW-STALE",
        "COLLECTION-INDEX-ROW-DUPLICATE",
        "PROGRAM-LINEAGE-STATE",
        "PROGRAM-LINEAGE-RECIPROCAL",
        "PROGRAM-LINEAGE-HISTORICAL-EXCEPTION",
        "PROGRAM-LINEAGE-EXECUTION-GATE",
        "PROGRAM-LINEAGE-DUPLICATE-AUTHORITY",
    }
)
GOVERNANCE_CURRENT_README = PurePosixPath("docs/00.agent-governance/README.md")
GOVERNANCE_CURRENT_HEADING = "### Current Governance Authority Index"
FIXTURE_GOVERNANCE_PATHS = (
    PurePosixPath("docs/00.agent-governance/current-alpha.md"),
    PurePosixPath("docs/00.agent-governance/current-beta.md"),
)
STATUS_MAP = {"active": "active", "done": "done", "archived": "archived"}
OWNER_EXCLUSIONS = (
    re.compile(
        r"^docs/90\.references/(?:research|audits)/[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/]+/"
    ),
    re.compile(r"^docs/90\.references/cloud-examples/"),
    re.compile(r"^examples/(?:aws|azure)/docs/"),
)
SMDV_CLOSURE_PATHS = (
    PurePosixPath("docs/03.specs/029-semantic-document-validation/spec.md"),
    PurePosixPath("docs/04.execution/plans/2026-07-12-semantic-document-validation.md"),
    PurePosixPath("docs/04.execution/tasks/2026-07-12-semantic-document-validation.md"),
)
ADM_CLOSURE_PATHS = (
    PurePosixPath("docs/03.specs/030-authored-document-migration/spec.md"),
    PurePosixPath("docs/04.execution/plans/2026-07-12-authored-document-migration.md"),
    PurePosixPath("docs/04.execution/tasks/2026-07-12-authored-document-migration.md"),
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
    DeclaredIndex(
        PurePosixPath("docs/03.specs/README.md"),
        re.compile(r"^docs/03\.specs/[0-9]{3}-[^/]+/spec\.md$"),
        "## Document Index",
        "03.specs/",
        "### Current Spec Index",
        "section",
        "spec",
    ),
    DeclaredIndex(
        PurePosixPath("docs/04.execution/plans/README.md"),
        re.compile(r"^docs/04\.execution/plans/[^/]+\.md$"),
        "## Item Index",
        "04.execution/plans/",
        "## Item Index",
        "after",
        "flat",
    ),
    DeclaredIndex(
        PurePosixPath("docs/04.execution/tasks/README.md"),
        re.compile(r"^docs/04\.execution/tasks/[^/]+\.md$"),
        "## Item Index",
        "04.execution/tasks/",
        "### 문서 인덱스",
        "section",
        "flat",
    ),
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


@dataclass(frozen=True)
class LifecycleMarkdownEvidence:
    """Immutable lifecycle view derived by the canonical Markdown scanner."""

    path: PurePosixPath
    all_local_links: tuple[PurePosixPath, ...]
    relationship_links: tuple[PurePosixPath, ...]
    unresolved_relationship_links: tuple[PurePosixPath, ...]
    body_table_links: tuple[PurePosixPath, ...]
    relationship_section_valid: bool
    body_contract_valid: bool
    body_rows: tuple[tuple[tuple[str, str], ...], ...]
    task_terminal_evidence_valid: bool


class ConfigurationError(ValueError):
    """Malformed closed configuration or CLI state."""


def _diag(
    rule_id: str, path: PurePosixPath, profile: str, expected: str, actual: str
) -> Diagnostic:
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


def _commonmark_splitlines(value: str, *, keepends: bool = False) -> list[str]:
    """Split only CR, LF, or CRLF without treating controls as line endings."""

    lines: list[str] = []
    cursor = 0
    for match in re.finditer(r"\r\n|\r|\n", value):
        lines.append(value[cursor : match.end() if keepends else match.start()])
        cursor = match.end()
    if cursor < len(value):
        lines.append(value[cursor:])
    return lines


def _commonmark_blank_line(value: str) -> bool:
    """Return whether a source line contains only CommonMark blank spaces."""

    return not value.strip(" \t")


def _visible_markdown(text: str) -> str:
    inline_masked = list(text)
    cursor = 0
    while cursor < len(text):
        start = text.find("<!--", cursor)
        if start < 0:
            break
        match = _INLINE_HTML_COMMENT.match(text, start)
        if match is None:
            cursor = start + 1
            continue
        line_start = text.rfind("\n", 0, start) + 1
        prefix = text[line_start:start]
        container_prefix = prefix
        while container_prefix:
            quote_content = _strip_blockquote_marker(container_prefix)
            if quote_content is not None:
                container_prefix = quote_content
                continue
            list_content = _strip_list_item_marker(container_prefix)
            if list_content is not None:
                container_prefix = list_content[0]
                continue
            break
        if (
            _source_character_escaped(text, start)
            or re.fullmatch(r" {0,3}", container_prefix) is not None
            or re.search(r"\n[ \t]*\n", match.group(0)) is not None
        ):
            cursor = match.end()
            continue
        for offset in range(start, match.end()):
            if inline_masked[offset] not in "\r\n":
                inline_masked[offset] = _INLINE_COMMENT_OPAQUE
        cursor = match.end()

    output: list[str] = []
    fence: tuple[str, int] | None = None
    comment_block = False
    for raw_line in _commonmark_splitlines("".join(inline_masked)):
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
        if comment_block:
            output.append("")
            if "-->" in raw_line:
                comment_block = False
            continue
        comment_start = re.match(r"^ {0,3}<!--", raw_line)
        if comment_start is not None:
            output.append("")
            if raw_line.find("-->", comment_start.start() + 2) < 0:
                comment_block = True
            continue
        line = raw_line
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


_HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|"
    "colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|"
    "footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html|"
    "iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|"
    "option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|"
    "title|tr|track|ul"
)
_HTML_BLOCK_TAG = re.compile(
    rf"^ {{0,3}}</?(?:{_HTML_BLOCK_TAGS})(?:\s|/?>|$)", re.IGNORECASE
)
_INLINE_HTML_TAG_NAME = r"[A-Za-z][A-Za-z0-9-]*"
_INLINE_HTML_ATTRIBUTE_NAME = r"[A-Za-z_:][A-Za-z0-9_.:-]*"
_INLINE_HTML_ATTRIBUTE_VALUE = r"""(?:[^\s"'=<>`]+|'[^']*'|"[^"]*")"""
_INLINE_HTML_ATTRIBUTE = (
    rf"[ \t\r\n]+{_INLINE_HTML_ATTRIBUTE_NAME}"
    rf"(?:[ \t\r\n]*=[ \t\r\n]*{_INLINE_HTML_ATTRIBUTE_VALUE})?"
)
_INLINE_HTML_TAG_SOURCE = (
    rf"(?:</{_INLINE_HTML_TAG_NAME}[ \t\r\n]*>|"
    rf"<{_INLINE_HTML_TAG_NAME}(?:{_INLINE_HTML_ATTRIBUTE})*"
    r"[ \t\r\n]*/?>)"
)
_INLINE_HTML_TAG = re.compile(_INLINE_HTML_TAG_SOURCE)
_HTML_COMPLETE_TAG = re.compile(rf"^ {{0,3}}{_INLINE_HTML_TAG_SOURCE}[ \t]*$")


def _render_container_markdown(
    text: str,
    *,
    defer_indented_code: bool = False,
    paragraph_continuation_lines: frozenset[int] = frozenset(),
) -> str:
    """Render one CommonMark container while retaining soft line breaks."""

    visible = _visible_markdown(text)
    lines = _commonmark_splitlines(visible)
    output: list[str] = []
    raw_end: re.Pattern[str] | None = None
    raw_until_blank = False
    indented_code = False
    previous_blank = True
    previous_leaf_block = False
    previous_paragraph_line = False

    atx_heading = re.compile(r" {0,3}#{1,6}(?:[ \t]+.*)?")
    setext_delimiter = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
    thematic_break = re.compile(
        r" {0,3}(?:(?:\*[ \t]*){3,}|"
        r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})"
    )
    definition_lines: set[int] = set()
    if not defer_indented_code:
        _, definition_spans = _reference_definitions_with_spans(
            visible,
            lazy_lines=paragraph_continuation_lines,
        )
        for start, end in definition_spans:
            first_line = visible.count("\n", 0, start)
            last_line = visible.count("\n", 0, end)
            definition_lines.update(range(first_line, last_line + 1))

    def ends_leaf_block(line: str, setext_eligible: bool) -> bool:
        return (
            atx_heading.fullmatch(line) is not None
            or thematic_break.fullmatch(line) is not None
            or (setext_eligible and setext_delimiter.fullmatch(line) is not None)
        )

    for line_index, line in enumerate(lines):
        paragraph_continuation = line_index in paragraph_continuation_lines
        if raw_end is not None:
            output.append("")
            if raw_end.search(line):
                raw_end = None
            previous_blank = not line.strip()
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        if raw_until_blank:
            output.append("")
            if not line.strip():
                raw_until_blank = False
            previous_blank = not line.strip()
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        if line_index in definition_lines:
            output.append(line)
            previous_blank = False
            previous_leaf_block = True
            previous_paragraph_line = False
            continue
        if not defer_indented_code and indented_code and not paragraph_continuation:
            if not line.strip() or line.startswith(("    ", "\t")):
                output.append("")
                previous_blank = not line.strip()
                previous_leaf_block = False
                previous_paragraph_line = False
                continue
            indented_code = False
        if (
            not defer_indented_code
            and not paragraph_continuation
            and (previous_blank or previous_leaf_block)
            and line.startswith(("    ", "\t"))
        ):
            indented_code = True
            output.append("")
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            continue

        start = re.match(
            r"^ {0,3}<(?P<tag>script|pre|style|textarea)(?:\s|>|$)", line, re.IGNORECASE
        )
        if start is not None:
            output.append("")
            closing = re.compile(
                rf"</{re.escape(start.group('tag'))}\s*>", re.IGNORECASE
            )
            if closing.search(line, start.end()) is None:
                raw_end = closing
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        raw_delimiters = (
            (re.match(r"^ {0,3}<\?", line), re.compile(r"\?>")),
            (re.match(r"^ {0,3}<!\[CDATA\[", line), re.compile(r"\]\]>")),
            (re.match(r"^ {0,3}<![A-Z]", line), re.compile(r">")),
        )
        matched_raw = False
        for start_match, closing in raw_delimiters:
            if start_match is None:
                continue
            output.append("")
            if closing.search(line, start_match.end()) is None:
                raw_end = closing
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            matched_raw = True
            break
        if matched_raw:
            continue
        if _HTML_BLOCK_TAG.match(line) or (
            previous_blank and _HTML_COMPLETE_TAG.match(line)
        ):
            output.append("")
            raw_until_blank = True
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        leaf_block = not paragraph_continuation and ends_leaf_block(
            line, previous_paragraph_line
        )
        output.append(line)
        previous_blank = not line.strip()
        previous_leaf_block = leaf_block
        previous_paragraph_line = bool(line.strip()) and not leaf_block
    return "\n".join(output)


def _normalize_component(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(
        r"-+",
        "-",
        "".join(character if character.isalnum() else "-" for character in normalized),
    ).strip("-")


def _profile_view(profile: DocumentProfile) -> ProfileView:
    return ProfileView(profile.profile_id, profile.profile_class, profile.mode)


def _build_context(
    root: Path, include_paths: tuple[PurePosixPath, ...] = ()
) -> Context:
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
        normalized = posixpath.normpath(
            posixpath.join(adapter.parent.as_posix(), raw_target)
        )
        if (
            normalized == ".."
            or normalized.startswith("../")
            or normalized.startswith("/")
        ):
            raise ConfigurationError(
                f"symlink adapter escapes repository: {adapter.as_posix()}"
            )
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


def _normalize_reference_label(
    value: str,
    *,
    raw_pua_encoded: bool = False,
    opaque_tokens: Sequence[tuple[int, int, str]] = (),
) -> str:
    """Normalize a CommonMark reference label for deterministic lookup."""

    logical: list[str] = []
    raw_length = 0
    tokens_by_start = {start: (end, source) for start, end, source in opaque_tokens}
    cursor = 0
    while cursor < len(value):
        opaque = tokens_by_start.get(cursor)
        if opaque is not None:
            token_end, source = opaque
            logical.append(source)
            raw_length += token_end - cursor
            cursor = token_end
            continue
        character = value[cursor]
        if (
            raw_pua_encoded
            and character == _RAW_PUA_ESCAPE
            and cursor + 1 < len(value)
            and _RAW_PUA_START <= ord(value[cursor + 1]) <= _RAW_PUA_END
        ):
            logical.extend(value[cursor : cursor + 2])
            raw_length += 1
            cursor += 2
            continue
        logical.append(character)
        raw_length += 1
        cursor += 1
    if raw_length > 999:
        return ""
    return re.sub(r"\s+", " ", "".join(logical).strip()).casefold()


def _markdown_escapable(character: str) -> bool:
    """Return whether CommonMark permits backslash-unescaping this ASCII byte."""

    codepoint = ord(character)
    return (
        33 <= codepoint <= 47
        or 58 <= codepoint <= 64
        or 91 <= codepoint <= 96
        or 123 <= codepoint <= 126
    )


_HTML_CHARACTER_REFERENCE = re.compile(
    r"&(?:#[xX][0-9A-Fa-f]{1,6}|#[0-9]{1,7}|"
    r"[A-Za-z][A-Za-z0-9]{1,31});"
)


def _markdown_character_reference(
    value: str, start: int, end: int
) -> tuple[str, int] | None:
    """Decode one unescaped CommonMark character reference."""

    match = _HTML_CHARACTER_REFERENCE.match(value, start, end)
    if match is None:
        return None
    candidate = match.group(0)
    if not candidate.startswith("&#") and candidate[1:] not in html.entities.html5:
        return None
    return html.unescape(candidate), match.end()


def _merge_source_spans(
    spans: Iterable[tuple[int, int]],
) -> tuple[tuple[int, int], ...]:
    """Merge ordered source ownership spans."""

    merged: list[tuple[int, int]] = []
    for start, end in sorted(spans):
        if start >= end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return tuple(merged)


@dataclass(frozen=True)
class IntervalSweep:
    spans: tuple[tuple[int, int], ...]
    steps: int


@dataclass(frozen=True)
class BacktickCloserScan:
    closer_ends: dict[int, int]
    steps: int


def _ordered_indexed_intervals(
    intervals: Sequence[tuple[int, int]],
) -> list[tuple[int, tuple[int, int]]]:
    """Sort intervals for a sweep while retaining their source order."""

    return sorted(
        enumerate(intervals),
        key=lambda item: (item[1][0], item[1][1], item[0]),
    )


def _intervals_not_contained(
    candidates: Sequence[tuple[int, int]],
    containers: Sequence[tuple[int, int]],
) -> IntervalSweep:
    """Keep intervals not enclosed by any container in O(n log n)."""

    ordered_containers = sorted(containers)
    ordered_candidates = _ordered_indexed_intervals(candidates)
    keep = [True] * len(candidates)
    container_index = 0
    furthest_end = -1
    steps = 0
    for original_index, (candidate_start, candidate_end) in ordered_candidates:
        while (
            container_index < len(ordered_containers)
            and ordered_containers[container_index][0] <= candidate_start
        ):
            furthest_end = max(
                furthest_end,
                ordered_containers[container_index][1],
            )
            container_index += 1
            steps += 1
        steps += 1
        if furthest_end >= candidate_end:
            keep[original_index] = False
    return IntervalSweep(
        tuple(interval for index, interval in enumerate(candidates) if keep[index]),
        steps,
    )


def _intervals_not_overlapping(
    candidates: Sequence[tuple[int, int]],
    blockers: Sequence[tuple[int, int]],
) -> IntervalSweep:
    """Keep intervals disjoint from blockers with one ordered overlap sweep."""

    ordered_blockers = sorted(blockers)
    keep = [True] * len(candidates)
    blocker_index = 0
    steps = 0
    for original_index, (candidate_start, candidate_end) in _ordered_indexed_intervals(
        candidates
    ):
        while (
            blocker_index < len(ordered_blockers)
            and ordered_blockers[blocker_index][1] <= candidate_start
        ):
            blocker_index += 1
            steps += 1
        steps += 1
        if (
            blocker_index < len(ordered_blockers)
            and ordered_blockers[blocker_index][0] < candidate_end
        ):
            keep[original_index] = False
    return IntervalSweep(
        tuple(interval for index, interval in enumerate(candidates) if keep[index]),
        steps,
    )


def _backtick_closer_scan(
    text: str,
    syntax_owned_spans: Sequence[tuple[int, int]],
) -> BacktickCloserScan:
    """Pair unowned backtick runs with one monotonic ownership cursor."""

    owned = _merge_source_spans(syntax_owned_spans)
    closer_ends: dict[int, int] = {}
    owned_index = 0
    steps = 0

    def scan_segment(start: int, end: int) -> None:
        nonlocal owned_index, steps
        runs: list[tuple[int, int, int]] = []
        cursor = start
        while cursor < end:
            steps += 1
            while owned_index < len(owned) and owned[owned_index][1] <= cursor:
                owned_index += 1
                steps += 1
            if (
                owned_index < len(owned)
                and owned[owned_index][0] <= cursor < owned[owned_index][1]
            ):
                cursor = min(end, owned[owned_index][1])
                continue
            if text[cursor] != "`":
                cursor += 1
                continue
            run_start = cursor
            while cursor < end and text[cursor] == "`":
                cursor += 1
            runs.append((run_start, cursor, cursor - run_start))

        nearest: dict[int, int] = {}
        for index in range(len(runs) - 1, -1, -1):
            run_start, _, run_length = runs[index]
            escaped = _source_character_escaped(text, run_start)
            opener_start = run_start + 1 if escaped else run_start
            opener_length = run_length - 1 if escaped else run_length
            if opener_length > 0:
                closer_index = nearest.get(opener_length)
                if closer_index is not None:
                    closer_ends[opener_start] = runs[closer_index][1]
            # A backslash-prefixed raw run remains a full-length closer for
            # already-open code even though only its tail can open code.
            nearest[run_length] = index

    segment_start = 0
    for boundary in re.finditer(r"\n[ \t]*\n", text):
        scan_segment(segment_start, boundary.start())
        segment_start = boundary.end()
    scan_segment(segment_start, len(text))
    return BacktickCloserScan(closer_ends, steps)


def _backtick_closer_ends(
    text: str,
    syntax_owned_spans: Sequence[tuple[int, int]],
) -> dict[int, int]:
    """Map each unowned backtick run to its next equal-length closer."""

    return _backtick_closer_scan(text, syntax_owned_spans).closer_ends


def _inline_code_spans(
    text: str,
    *,
    syntax_owned_spans: Sequence[tuple[int, int]] | None = None,
) -> tuple[tuple[int, int], ...]:
    """Return run-length code spans after higher-priority syntax ownership."""

    owned = (
        _inline_syntax_owned_spans(text)
        if syntax_owned_spans is None
        else _merge_source_spans(syntax_owned_spans)
    )
    closer_ends = _backtick_closer_ends(text, owned)
    spans: list[tuple[int, int]] = []
    consumed_until = -1
    for opener, closer_end in sorted(closer_ends.items()):
        if opener < consumed_until or _source_character_escaped(text, opener):
            continue
        spans.append((opener, closer_end))
        consumed_until = closer_end
    return tuple(spans)


def _mask_inline_code_spans(text: str) -> str:
    """Mask code spans after higher-priority syntax claims its backticks."""

    masked = list(text)
    for start, end in _inline_code_spans(text):
        for offset in range(start, end):
            if masked[offset] != "\n":
                masked[offset] = " "
    return "".join(masked)


@dataclass(frozen=True)
class MarkdownLink:
    start: int
    end: int
    label: str
    target: str


@dataclass(frozen=True)
class RenderedLocalLink:
    """Filesystem-free resolution from the canonical rendered Markdown parser.

    Payload-derived target values are intentionally excluded from the default
    representation so importing validators cannot disclose document content in
    logs or exception rendering.
    """

    kind: str
    raw_target: str = dataclass_field(repr=False)
    target: PurePosixPath | None = dataclass_field(repr=False)


@dataclass(frozen=True)
class BracketSuppression:
    suppressed: frozenset[int]
    steps: int


def _nested_link_suppression(
    parents: dict[int, int | None],
    candidate_openers: frozenset[int],
    resolved_images: frozenset[int],
    source_consumed: frozenset[int],
) -> BracketSuppression:
    """Propagate image and nested-link suppression through the bracket tree."""

    nodes = sorted(parents)
    image_blocked: dict[int, bool] = {}
    eligible_candidates: set[int] = set()
    suppressed = set(candidate_openers.intersection(source_consumed))
    steps = 0
    for opener in nodes:
        parent = parents[opener]
        blocked = parent is not None and (
            parent in resolved_images or image_blocked.get(parent, False)
        )
        image_blocked[opener] = blocked
        if opener in candidate_openers:
            if blocked:
                suppressed.add(opener)
            elif opener not in source_consumed:
                eligible_candidates.add(opener)
        steps += 1

    has_eligible_descendant: dict[int, bool] = {}
    for opener in reversed(nodes):
        descendant = has_eligible_descendant.get(opener, False)
        if opener in eligible_candidates and descendant:
            suppressed.add(opener)
        subtree_has_candidate = descendant or opener in eligible_candidates
        parent = parents[opener]
        if subtree_has_candidate and parent is not None:
            has_eligible_descendant[parent] = True
        steps += 1
    return BracketSuppression(frozenset(suppressed), steps)


def _bracket_pairs(
    value: str,
    *,
    code_spans: Sequence[tuple[int, int]] | None = None,
) -> tuple[dict[int, int], dict[int, int | None]]:
    """Pair brackets and record their containing opener in closing order."""

    stack: list[int] = []
    pairs: dict[int, int] = {}
    parents: dict[int, int | None] = {}
    active_code_spans = (
        _inline_code_spans(value) if code_spans is None else tuple(code_spans)
    )
    code_index = 0
    cursor = 0
    while cursor < len(value):
        while (
            code_index < len(active_code_spans)
            and cursor >= active_code_spans[code_index][1]
        ):
            code_index += 1
        if (
            code_index < len(active_code_spans)
            and active_code_spans[code_index][0]
            <= cursor
            < active_code_spans[code_index][1]
        ):
            cursor = active_code_spans[code_index][1]
            continue
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < len(value)
            and _markdown_escapable(value[cursor + 1])
        ):
            cursor += 2
            continue
        if character == "[":
            stack.append(cursor)
        elif character == "]" and stack:
            opener = stack.pop()
            pairs[opener] = cursor
            parents[opener] = stack[-1] if stack else None
        cursor += 1
    return pairs, parents


def _source_character_escaped(value: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and value[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


_INLINE_HTML_COMMENT = re.compile(
    r"(?:<!---->|<!--(?:-?[^>-])(?:-?[^-])*?-->)",
    re.DOTALL,
)
_INLINE_COMMENT_OPAQUE = "\U000f0000"
_INLINE_HTML_SPECIAL = (
    _INLINE_HTML_COMMENT,
    re.compile(r"<\?[\s\S]*?\?>"),
    re.compile(r"<![A-Z][\s\S]*?>"),
    re.compile(r"<!\[CDATA\[[\s\S]*?\]\]>"),
)
_RAW_PUA_START = 0xE000
_RAW_PUA_END = 0xF8FF
_RAW_PUA_ESCAPE = chr(_RAW_PUA_START)
_INLINE_HTML_OPAQUE_START = _RAW_PUA_START + 1
_INLINE_HTML_OPAQUE_BASE = _RAW_PUA_END - _INLINE_HTML_OPAQUE_START + 1
_INLINE_HTML_TOKEN_IDS: dict[str, int] = {}
_INLINE_HTML_TOKEN_SOURCES: dict[str, str] = {}


class OpaqueMarkdown(str):
    """HTML-opaque Markdown with encoded-to-source offset provenance."""

    source_offsets: tuple[int, ...]
    opaque_tokens: tuple[tuple[int, int, str], ...]
    opaque_token_starts: tuple[int, ...]
    raw_pua_encoded: bool
    lazy_lines: frozenset[int]

    def __new__(
        cls,
        value: str,
        source_offsets: tuple[int, ...],
        *,
        opaque_tokens: tuple[tuple[int, int, str], ...] = (),
        lazy_lines: frozenset[int] = frozenset(),
    ) -> "OpaqueMarkdown":
        instance = super().__new__(cls, value)
        instance.source_offsets = source_offsets
        instance.opaque_tokens = tuple(
            sorted(opaque_tokens, key=lambda token: (token[0], token[1]))
        )
        instance.opaque_token_starts = tuple(
            token[0] for token in instance.opaque_tokens
        )
        instance.raw_pua_encoded = True
        instance.lazy_lines = lazy_lines
        return instance


@dataclass(frozen=True)
class ReferenceLabelNormalization:
    label: str
    steps: int


def _opaque_token_lower_bound(starts: Sequence[int], target: int) -> tuple[int, int]:
    """Return a deterministic bisect-left result and comparison count."""

    lower = 0
    upper = len(starts)
    steps = 0
    while lower < upper:
        steps += 1
        middle = (lower + upper) // 2
        if starts[middle] < target:
            lower = middle + 1
        else:
            upper = middle
    return lower, steps


def _normalize_reference_label_span_scan(
    value: str, start: int, end: int
) -> ReferenceLabelNormalization:
    """Normalize one label after an indexed opaque-token interval lookup."""

    opaque_tokens: tuple[tuple[int, int, str], ...] = ()
    steps = 0
    if isinstance(value, OpaqueMarkdown):
        token_index, steps = _opaque_token_lower_bound(value.opaque_token_starts, start)
        if token_index > 0:
            token_index -= 1
        contained: list[tuple[int, int, str]] = []
        while token_index < len(value.opaque_tokens):
            token_start, token_end, source = value.opaque_tokens[token_index]
            if token_start >= end:
                break
            steps += 1
            if start <= token_start and token_end <= end:
                contained.append((token_start - start, token_end - start, source))
            token_index += 1
        opaque_tokens = tuple(contained)
    return ReferenceLabelNormalization(
        _normalize_reference_label(
            value[start:end],
            raw_pua_encoded=bool(getattr(value, "raw_pua_encoded", False)),
            opaque_tokens=opaque_tokens,
        ),
        steps,
    )


def _normalize_reference_label_span(value: str, start: int, end: int) -> str:
    """Normalize one label span with structured opaque-token provenance."""

    return _normalize_reference_label_span_scan(value, start, end).label


def _inline_link_destination_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Commit inline suffix ownership once in monotonic source order."""

    closer_ends = _backtick_closer_ends(value, ())
    html_ends = dict(_raw_inline_html_token_spans(value))
    _, definition_spans = _reference_definitions_with_spans(value)
    definition_ends = dict(definition_spans)
    hard_boundary_starts = tuple(
        match.start() for match in re.finditer(r"\n[ \t]*\n", value)
    )

    def label_crosses_hard_boundary(start: int, end: int) -> bool:
        index = bisect.bisect_left(hard_boundary_starts, start)
        return index < len(hard_boundary_starts) and hard_boundary_starts[index] < end

    failed_starts: set[int] = set()
    stack: list[int] = []
    suffix_spans: list[tuple[int, int]] = []
    cursor = 0
    while cursor < len(value):
        definition_end = definition_ends.get(cursor)
        if definition_end is not None:
            cursor = definition_end
            continue
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < len(value)
            and _markdown_escapable(value[cursor + 1])
        ):
            cursor += 2
            continue
        if character == "`":
            run_end = cursor + 1
            while run_end < len(value) and value[run_end] == "`":
                run_end += 1
            closer_end = closer_ends.get(cursor)
            if closer_end is not None:
                cursor = closer_end
            else:
                cursor = run_end
            continue
        html_end = html_ends.get(cursor)
        if html_end is not None:
            cursor = html_end
            continue
        if character == "[":
            stack.append(cursor)
            cursor += 1
            continue
        if character != "]" or not stack:
            cursor += 1
            continue

        opener = stack.pop()
        suffix_start = cursor + 1
        if (
            suffix_start >= len(value)
            or value[suffix_start] != "("
            or label_crosses_hard_boundary(opener + 1, cursor)
        ):
            cursor += 1
            continue
        destination_start = suffix_start + 1
        parsed = (
            None
            if destination_start in failed_starts
            else _inline_link_destination(value, destination_start, failed_starts)
        )
        if parsed is None:
            cursor += 1
            continue
        _, suffix_end = parsed
        suffix_spans.append((suffix_start, suffix_end))
        cursor = suffix_end
    return tuple(suffix_spans)


def _reference_definition_destination_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return destination/title portions of fully valid definitions."""

    _, definition_spans = _reference_definitions_with_spans(value)
    spans: list[tuple[int, int]] = []
    for definition_start, definition_end in definition_spans:
        cursor = definition_start
        while cursor < definition_end and value[cursor] == " ":
            cursor += 1
        if cursor >= definition_end or value[cursor] != "[":
            continue
        cursor += 1
        while cursor < definition_end:
            if (
                value[cursor] == "\\"
                and cursor + 1 < definition_end
                and _markdown_escapable(value[cursor + 1])
            ):
                cursor += 2
                continue
            if (
                value[cursor] == "]"
                and cursor + 1 < definition_end
                and value[cursor + 1] == ":"
            ):
                spans.append((cursor + 1, definition_end))
                break
            cursor += 1
    return tuple(spans)


def _inline_link_syntax_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return valid raw inline/reference destination and title ownership."""

    return _merge_source_spans(
        (
            *_inline_link_destination_spans(value),
            *_reference_definition_destination_spans(value),
        )
    )


def _raw_inline_html_token_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return every quote-aware raw HTML token candidate."""

    spans: list[tuple[int, int]] = []
    cursor = 0
    while cursor < len(value):
        token_start = value.find("<", cursor)
        if token_start < 0:
            break
        if _source_character_escaped(value, token_start):
            cursor = token_start + 1
            continue
        match = _INLINE_HTML_TAG.match(value, token_start)
        if match is None:
            match = next(
                (
                    candidate
                    for pattern in _INLINE_HTML_SPECIAL
                    if (candidate := pattern.match(value, token_start)) is not None
                ),
                None,
            )
        if match is None:
            cursor = token_start + 1
            continue
        if re.search(r"\n[ \t]*\n", match.group(0)) is not None:
            cursor = token_start + 1
            continue
        token_end = match.end()
        spans.append((token_start, token_end))
        cursor = token_end
    return tuple(spans)


def _inline_syntax_ownership(
    value: str,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    """Resolve nested link-suffix and HTML-token ownership by containment."""

    link_candidates = _inline_link_syntax_spans(value)
    html_candidates = _raw_inline_html_token_spans(value)
    html_spans = _intervals_not_contained(html_candidates, link_candidates).spans
    link_spans = _intervals_not_contained(link_candidates, html_spans).spans
    return link_spans, html_spans


def _inline_syntax_owned_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return raw link and HTML spans whose backticks are syntax-owned."""

    link_spans, html_spans = _inline_syntax_ownership(value)
    return _merge_source_spans((*link_spans, *html_spans))


def _inline_html_token_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return HTML candidates not rendered inside resulting code spans."""

    link_spans, raw_html_spans = _inline_syntax_ownership(value)
    syntax_owned = _merge_source_spans((*link_spans, *raw_html_spans))
    code_spans = _inline_code_spans(value, syntax_owned_spans=syntax_owned)
    return _intervals_not_overlapping(raw_html_spans, code_spans).spans


def _mask_inline_html_tokens(value: str) -> OpaqueMarkdown:
    """Namespace raw BMP PUA input and replace inline HTML with opaque IDs."""

    output: list[str] = []
    source_offsets: list[int] = []
    opaque_tokens: list[tuple[int, int, str]] = []
    cursor = 0

    def append_raw(start: int, end: int) -> None:
        for index in range(start, end):
            character = value[index]
            if _RAW_PUA_START <= ord(character) <= _RAW_PUA_END:
                output.extend((_RAW_PUA_ESCAPE, character))
                source_offsets.extend((index, index))
            else:
                output.append(character)
                source_offsets.append(index)

    for token_start, token_end in _inline_html_token_spans(value):
        append_raw(cursor, token_start)
        token = value[token_start:token_end]
        token_id = _INLINE_HTML_TOKEN_IDS.setdefault(token, len(_INLINE_HTML_TOKEN_IDS))
        opaque = list(token)
        opaque_positions = [
            index for index, character in enumerate(token) if character not in "\r\n"
        ]
        if token_id >= _INLINE_HTML_OPAQUE_BASE ** len(opaque_positions):
            raise ConfigurationError("inline HTML opaque identity exhausted")
        remaining = token_id
        for position in reversed(opaque_positions):
            opaque[position] = chr(
                _INLINE_HTML_OPAQUE_START + remaining % _INLINE_HTML_OPAQUE_BASE
            )
            remaining //= _INLINE_HTML_OPAQUE_BASE
        identity = "".join(opaque)
        source = _INLINE_HTML_TOKEN_SOURCES.setdefault(identity, token)
        if source != token:
            raise ConfigurationError("inline HTML opaque identity collision")
        encoded_start = len(output)
        output.extend(identity)
        opaque_tokens.append((encoded_start, len(output), token))
        source_offsets.extend(range(token_start, token_end))
        cursor = token_end
    append_raw(cursor, len(value))
    return OpaqueMarkdown(
        "".join(output),
        tuple(source_offsets),
        opaque_tokens=tuple(opaque_tokens),
        lazy_lines=getattr(value, "lazy_lines", frozenset()),
    )


def _decode_raw_pua_namespace(value: str) -> str:
    """Decode injectively escaped raw BMP PUA characters."""

    output: list[str] = []
    cursor = 0
    while cursor < len(value):
        if (
            value[cursor] == _RAW_PUA_ESCAPE
            and cursor + 1 < len(value)
            and _RAW_PUA_START <= ord(value[cursor + 1]) <= _RAW_PUA_END
        ):
            output.append(value[cursor + 1])
            cursor += 2
            continue
        output.append(value[cursor])
        cursor += 1
    return "".join(output)


def _rendered_inline_html_text(value: str) -> str:
    """Drop inline HTML markup while preserving its visible child text."""

    output: list[str] = []
    cursor = 0
    for token_start, token_end in _inline_html_token_spans(value):
        output.append(value[cursor:token_start])
        cursor = token_end
    output.append(value[cursor:])
    return "".join(output).replace(_INLINE_COMMENT_OPAQUE, "")


def _image_bracket_opener(value: str, opener: int) -> bool:
    return (
        opener > 0
        and value[opener - 1] == "!"
        and not _source_character_escaped(value, opener - 1)
    )


def _ascii_control(character: str) -> bool:
    """Return whether one character is an ASCII control byte."""

    codepoint = ord(character)
    return codepoint <= 0x1F or codepoint == 0x7F


def _markdown_link_separator_end(value: str, start: int, end: int) -> tuple[int, bool]:
    """Consume CommonMark space/tab plus at most one line ending."""

    cursor = start
    while cursor < end and value[cursor] in " \t":
        cursor += 1
    if cursor < end and value[cursor] in "\r\n":
        if value[cursor] == "\r" and cursor + 1 < end and value[cursor + 1] == "\n":
            cursor += 2
        else:
            cursor += 1
        while cursor < end and value[cursor] in " \t":
            cursor += 1
    return cursor, cursor > start


def _markdown_destination(value: str, start: int, end: int) -> tuple[str, int] | None:
    """Parse one destination and return its unescaped value and end offset."""

    cursor, _ = _markdown_link_separator_end(value, start, end)
    if cursor >= end:
        return "", cursor
    if value[cursor] == "<":
        cursor += 1
        target: list[str] = []
        while cursor < end:
            character = value[cursor]
            if (
                character == "\\"
                and cursor + 1 < end
                and _markdown_escapable(value[cursor + 1])
            ):
                target.append(value[cursor + 1])
                cursor += 2
                continue
            if character == "&":
                reference = _markdown_character_reference(value, cursor, end)
                if reference is not None:
                    decoded, cursor = reference
                    target.append(decoded)
                    continue
            if character == ">":
                return "".join(target), cursor + 1
            if character in {"\r", "\n", "<"}:
                return None
            target.append(character)
            cursor += 1
        return None

    target = []
    depth = 0
    while cursor < end:
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < end
            and _markdown_escapable(value[cursor + 1])
        ):
            target.append(value[cursor + 1])
            cursor += 2
            continue
        if character == "&":
            reference = _markdown_character_reference(value, cursor, end)
            if reference is not None:
                decoded, cursor = reference
                target.append(decoded)
                continue
        if character == " " or _ascii_control(character):
            if depth == 0 and character in " \t\r\n":
                break
            return None
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                return None
            depth -= 1
        target.append(character)
        cursor += 1
    return ("".join(target), cursor) if depth == 0 else None


def _markdown_title_end(value: str, start: int, end: int) -> int | None:
    """Return the offset after one quoted/parenthesized Markdown title."""

    cursor = start
    opener = value[cursor]
    closer = {'"': '"', "'": "'", "(": ")"}.get(opener)
    if closer is None:
        return None
    cursor += 1
    while cursor < end:
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < end
            and _markdown_escapable(value[cursor + 1])
        ):
            cursor += 2
            continue
        if opener == "(" and character == "(":
            return None
        if character == closer:
            return cursor + 1
        cursor += 1
    return None


def _valid_markdown_title(value: str, start: int, end: int) -> bool:
    """Accept an empty remainder or exactly one quoted/parenthesized title."""

    cursor, _ = _markdown_link_separator_end(value, start, end)
    if cursor >= end:
        return True
    title_end = _markdown_title_end(value, cursor, end)
    if title_end is None:
        return False
    cursor, _ = _markdown_link_separator_end(value, title_end, end)
    return cursor == end


def _link_destination(value: str, start: int, end: int) -> str | None:
    """Parse a destination and validate its complete optional-title remainder."""

    parsed = _markdown_destination(value, start, end)
    if parsed is None:
        return None
    target, consumed = parsed
    if consumed == end:
        return target
    _, separated = _markdown_link_separator_end(value, consumed, end)
    if not separated:
        return None
    return target if _valid_markdown_title(value, consumed, end) else None


def _inline_link_destination(
    value: str, start: int, failed_starts: set[int] | None = None
) -> tuple[str, int] | None:
    """Consume an inline destination, optional title, and real outer closer."""

    end = len(value)
    cursor, leading_space = _markdown_link_separator_end(value, start, end)
    if cursor >= end:
        return None

    target: list[str] = []
    empty_destination_title = False
    unmatched_openers = [start - 1]
    if value[cursor] == "<":
        cursor += 1
        while cursor < end:
            character = value[cursor]
            if (
                character == "\\"
                and cursor + 1 < end
                and _markdown_escapable(value[cursor + 1])
            ):
                target.append(value[cursor + 1])
                cursor += 2
                continue
            if character == "&":
                reference = _markdown_character_reference(value, cursor, end)
                if reference is not None:
                    decoded, cursor = reference
                    target.append(decoded)
                    continue
            if character == ">":
                cursor += 1
                break
            if character in {"\r", "\n", "<"}:
                return None
            target.append(character)
            cursor += 1
        else:
            return None
    elif value[cursor] == ")":
        return "", cursor + 1
    elif leading_space and value[cursor] in {'"', "'", "("}:
        empty_destination_title = True
    else:
        depth = 0
        while cursor < end:
            character = value[cursor]
            if (
                character == "\\"
                and cursor + 1 < end
                and _markdown_escapable(value[cursor + 1])
            ):
                target.append(value[cursor + 1])
                cursor += 2
                continue
            if character == "&":
                reference = _markdown_character_reference(value, cursor, end)
                if reference is not None:
                    decoded, cursor = reference
                    target.append(decoded)
                    continue
            if character == " " or _ascii_control(character):
                if depth == 0 and character in " \t\r\n":
                    break
                return None
            if character == "(":
                depth += 1
                unmatched_openers.append(cursor)
            elif character == ")":
                if depth == 0:
                    return "".join(target), cursor + 1
                depth -= 1
                unmatched_openers.pop()
            target.append(character)
            cursor += 1
        if depth != 0:
            if failed_starts is not None:
                failed_starts.update(opener + 1 for opener in unmatched_openers)
            return None

    if empty_destination_title:
        title_end = _markdown_title_end(value, cursor, end)
        if title_end is None:
            return None
        cursor, _ = _markdown_link_separator_end(value, title_end, end)
        if cursor >= end or value[cursor] != ")":
            return None
        return "", cursor + 1

    if cursor < end and value[cursor] == ")":
        return "".join(target), cursor + 1
    separator_end, separated = _markdown_link_separator_end(value, cursor, end)
    if cursor >= end or not separated:
        return None
    cursor = separator_end
    if cursor < end and value[cursor] == ")":
        return "".join(target), cursor + 1
    if cursor >= end:
        return None
    title_end = _markdown_title_end(value, cursor, end)
    if title_end is None:
        return None
    cursor, _ = _markdown_link_separator_end(value, title_end, end)
    if cursor >= end or value[cursor] != ")":
        return None
    return "".join(target), cursor + 1


def _reference_definitions_with_spans(
    value: str,
    *,
    lazy_lines: frozenset[int] | None = None,
) -> tuple[dict[str, str], tuple[tuple[int, int], ...]]:
    """Parse valid definitions and their complete, offset-stable source spans."""

    if lazy_lines is None:
        lazy_lines = getattr(value, "lazy_lines", frozenset())
    definitions: dict[str, str] = {}
    spans: list[tuple[int, int]] = []
    lines: list[tuple[str, int, int]] = []
    offset = 0
    for source_line in _commonmark_splitlines(value, keepends=True):
        line = source_line.rstrip("\r\n")
        lines.append((line, offset, offset + len(line)))
        offset += len(source_line)

    def parse_definition(
        index: int,
    ) -> tuple[str, str, int, int] | None:
        line, definition_start, definition_end = lines[index]

        opener = len(line) - len(line.lstrip(" "))
        if opener > 3 or opener >= len(line) or line[opener] != "[":
            return None

        label_start = opener + 1
        label_end: int | None = None
        label_end_index = index
        while label_end_index < len(lines):
            label_line = lines[label_end_index][0]
            if label_end_index > index and _commonmark_blank_line(label_line):
                return None
            cursor = label_start if label_end_index == index else 0
            while cursor < len(label_line):
                character = label_line[cursor]
                if (
                    character == "\\"
                    and cursor + 1 < len(label_line)
                    and _markdown_escapable(label_line[cursor + 1])
                ):
                    cursor += 2
                    continue
                if character == "[":
                    return None
                if character == "]":
                    label_end = cursor
                    break
                cursor += 1
            if label_end is not None:
                break
            label_end_index += 1
        if (
            label_end is None
            or label_end + 1 >= len(lines[label_end_index][0])
            or lines[label_end_index][0][label_end + 1] != ":"
        ):
            return None

        label = _normalize_reference_label_span(
            value,
            lines[index][1] + label_start,
            lines[label_end_index][1] + label_end,
        )
        if not label:
            return None

        def continuation_content(source: str) -> str | None:
            """Return content indented by at most four visual columns."""

            continuation_cursor = 0
            column = 0
            while (
                continuation_cursor < len(source)
                and source[continuation_cursor] in " \t"
            ):
                if source[continuation_cursor] == " ":
                    next_column = column + 1
                else:
                    next_column = column + (4 - column % 4)
                if next_column > 4:
                    return None
                column = next_column
                continuation_cursor += 1
            content = source[continuation_cursor:]
            return content if content else None

        def title_end_index(first_title: str, first_index: int) -> int | None:
            if not first_title or first_title[0] not in {'"', "'", "("}:
                return None
            closer = ")" if first_title[0] == "(" else first_title[0]
            title_index = first_index
            source = first_title
            title_cursor = 1
            while True:
                while title_cursor < len(source):
                    character = source[title_cursor]
                    if (
                        character == "\\"
                        and title_cursor + 1 < len(source)
                        and _markdown_escapable(source[title_cursor + 1])
                    ):
                        title_cursor += 2
                        continue
                    if first_title[0] == "(" and character == "(":
                        return None
                    if character == closer:
                        if source[title_cursor + 1 :].strip(" \t"):
                            return None
                        return title_index
                    title_cursor += 1
                title_index += 1
                if title_index >= len(lines) or _commonmark_blank_line(
                    lines[title_index][0]
                ):
                    return None
                source = lines[title_index][0]
                title_cursor = 0

        label_line, _, definition_end = lines[label_end_index]
        after_colon = label_line[label_end + 2 :]
        destination = after_colon.lstrip(" \t")
        destination_index = label_end_index
        span_end = definition_end
        if not destination:
            if label_end_index + 1 >= len(lines):
                return None
            continuation = continuation_content(lines[label_end_index + 1][0])
            if continuation is None:
                return None
            destination = continuation
            destination_index = label_end_index + 1
            span_end = lines[destination_index][2]

        parsed = _markdown_destination(destination, 0, len(destination))
        if parsed is None:
            return None
        target, consumed = parsed
        separator_end, separated = _markdown_link_separator_end(
            destination, consumed, len(destination)
        )
        if consumed < len(destination) and not separated:
            return None
        title_on_destination = separator_end < len(destination)
        definition_end_index = destination_index
        if title_on_destination:
            title = destination[separator_end:]
            parsed_title_index = title_end_index(title, destination_index)
            if parsed_title_index is None:
                return None
            definition_end_index = parsed_title_index
            span_end = lines[parsed_title_index][2]
        elif destination_index + 1 < len(lines):
            title = continuation_content(lines[destination_index + 1][0])
            if title is not None and title[0] in {'"', "'", "("}:
                parsed_title_index = title_end_index(title, destination_index + 1)
                if parsed_title_index is not None:
                    definition_end_index = parsed_title_index
                    span_end = lines[parsed_title_index][2]

        return (
            label,
            target,
            span_end,
            definition_end_index,
        )

    index = 0
    paragraph_open = False
    atx_heading = re.compile(r" {0,3}#{1,6}(?:[ \t]+.*)?")
    setext_delimiter = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
    thematic_break = re.compile(
        r" {0,3}(?:(?:\*[ \t]*){3,}|"
        r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})"
    )
    while index < len(lines):
        line, definition_start, _ = lines[index]
        if not line.strip():
            paragraph_open = False
            index += 1
            continue
        if (
            atx_heading.fullmatch(line) is not None
            or thematic_break.fullmatch(line) is not None
            or (
                paragraph_open
                and index not in lazy_lines
                and setext_delimiter.fullmatch(line) is not None
            )
        ):
            paragraph_open = False
            index += 1
            continue
        if paragraph_open:
            index += 1
            continue
        parsed = parse_definition(index)
        if parsed is None:
            paragraph_open = True
            index += 1
            continue
        label, target, span_end, definition_end_index = parsed
        definitions.setdefault(label, target)
        spans.append((definition_start, span_end))
        index = definition_end_index + 1
    return definitions, tuple(spans)


def _reference_definitions(value: str) -> dict[str, str]:
    """Parse first-wins rendered definitions, including continued targets."""

    definitions, _ = _reference_definitions_with_spans(value)
    return definitions


def _mask_source_spans(value: str, spans: Sequence[tuple[int, int]]) -> str:
    """Mask exact source spans while preserving line and character offsets."""

    masked = list(value)
    for start, end in spans:
        for index in range(start, end):
            if masked[index] not in {"\r", "\n"}:
                masked[index] = " "
    result = "".join(masked)
    if isinstance(value, OpaqueMarkdown):
        return OpaqueMarkdown(
            result,
            value.source_offsets,
            opaque_tokens=value.opaque_tokens,
            lazy_lines=value.lazy_lines,
        )
    return result


def _crosses_hard_inline_boundary(value: str) -> bool:
    return re.search(r"\n[ \t]*\n", value) is not None


def _scan_markdown_links(
    value: str, definitions: dict[str, str]
) -> tuple[MarkdownLink, ...]:
    """Resolve link/image bracket state in closing-token order."""

    brackets, parents = _bracket_pairs(value)
    hard_boundary_starts = tuple(
        match.start() for match in re.finditer(r"\n[ \t]*\n", value)
    )

    def crosses_hard_boundary(start: int, end: int) -> bool:
        index = bisect.bisect_left(hard_boundary_starts, start)
        return index < len(hard_boundary_starts) and hard_boundary_starts[index] < end

    candidates: dict[int, MarkdownLink] = {}
    resolved_images: set[int] = set()
    consumed: set[int] = set()
    consumed_source_spans: list[tuple[int, int]] = []
    failed_inline_starts: set[int] = set()
    for opener, label_end in brackets.items():
        if opener in consumed:
            continue
        if crosses_hard_boundary(opener + 1, label_end):
            continue
        suffix = label_end + 1
        candidate: MarkdownLink | None = None
        inline_consumed = False
        if suffix < len(value) and value[suffix] == "(":
            destination_start = suffix + 1
            parsed = (
                None
                if destination_start in failed_inline_starts
                else _inline_link_destination(
                    value, destination_start, failed_inline_starts
                )
            )
            if parsed is not None:
                target, link_end = parsed
                if not crosses_hard_boundary(suffix + 1, link_end - 1):
                    candidate = MarkdownLink(opener, link_end, "", target)
                    inline_consumed = True
            if candidate is None:
                key = _normalize_reference_label_span(value, opener + 1, label_end)
                if key and key in definitions:
                    candidate = MarkdownLink(opener, suffix, "", definitions[key])
        elif suffix < len(value) and value[suffix] == "[":
            reference_end = brackets.get(suffix)
            if reference_end is not None:
                explicit_reference = suffix + 1 < reference_end
                key_start, key_end = (
                    (suffix + 1, reference_end)
                    if explicit_reference
                    else (opener + 1, label_end)
                )
                key = _normalize_reference_label_span(value, key_start, key_end)
                if (
                    not crosses_hard_boundary(key_start, key_end)
                    and bool(key)
                    and key in definitions
                ):
                    candidate = MarkdownLink(
                        opener,
                        reference_end + 1,
                        "",
                        definitions[key],
                    )
                    consumed.add(suffix)
        else:
            after = suffix
            while after < len(value) and value[after] in " \t":
                after += 1
            key = _normalize_reference_label_span(value, opener + 1, label_end)
            if after < len(value) and value[after] == ":":
                continue
            if key and key in definitions:
                candidate = MarkdownLink(opener, suffix, "", definitions[key])
        if candidate is None:
            continue
        if inline_consumed:
            consumed_source_spans.append((suffix, candidate.end))
        if _image_bracket_opener(value, opener):
            resolved_images.add(opener)
            continue

        candidates[opener] = candidate

    merged_spans: list[tuple[int, int]] = []
    for start, end in sorted(consumed_source_spans):
        if merged_spans and start <= merged_spans[-1][1]:
            merged_spans[-1] = (
                merged_spans[-1][0],
                max(end, merged_spans[-1][1]),
            )
        else:
            merged_spans.append((start, end))
    source_consumed: set[int] = set()
    span_index = 0
    for opener in sorted(brackets):
        while span_index < len(merged_spans) and opener >= merged_spans[span_index][1]:
            span_index += 1
        if (
            span_index < len(merged_spans)
            and merged_spans[span_index][0] < opener < merged_spans[span_index][1]
        ):
            source_consumed.add(opener)
    resolved_images.difference_update(source_consumed)

    suppressed = _nested_link_suppression(
        parents,
        frozenset(candidates),
        frozenset(resolved_images),
        frozenset(source_consumed),
    ).suppressed

    return tuple(
        MarkdownLink(
            link.start,
            link.end,
            value[opener + 1 : brackets[opener]],
            link.target,
        )
        for opener in sorted(candidates)
        if opener not in suppressed
        for link in (candidates[opener],)
    )


def _extract_rendered_links(
    rendered: str, *, definitions_rendered: str | None = None
) -> tuple[str, ...]:
    """Extract links from an already block-rendered Markdown view."""

    visible_lazy_lines = getattr(rendered, "lazy_lines", frozenset())
    visible = _mask_inline_html_tokens(rendered)
    definition_lazy_lines = (
        getattr(definitions_rendered, "lazy_lines", frozenset())
        if definitions_rendered is not None
        else visible_lazy_lines
    )
    definition_source = (
        _mask_inline_html_tokens(definitions_rendered)
        if definitions_rendered is not None
        else visible
    )
    definitions, definition_spans = _reference_definitions_with_spans(
        definition_source,
        lazy_lines=definition_lazy_lines,
    )
    if definitions_rendered is not None:
        _, definition_spans = _reference_definitions_with_spans(
            visible,
            lazy_lines=visible_lazy_lines,
        )
    scan_source = _mask_source_spans(visible, definition_spans)
    code_masked = _mask_inline_code_spans(scan_source)
    return tuple(
        _decode_raw_pua_namespace(link.target)
        for link in _scan_markdown_links(scan_source, definitions)
        if code_masked[link.start] != " "
    )


def _extract_links(
    text: str, *, definitions_text: str | None = None
) -> tuple[str, ...]:
    rendered = _rendered_markdown(text)
    definitions_rendered = (
        _rendered_markdown(definitions_text) if definitions_text is not None else None
    )
    return _extract_rendered_links(rendered, definitions_rendered=definitions_rendered)


def _local_destination(
    source: PurePosixPath, raw: str
) -> tuple[str, PurePosixPath | None]:
    value = raw
    lowered = value.casefold()
    if lowered.startswith("file:"):
        return "LINK-FILE-URI", None
    if value.startswith("//"):
        return "external", None
    if value.startswith("/") or re.match(r"^[A-Za-z]:[/\\]", value):
        return "LINK-ABSOLUTE", None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return "external", None
    path_part = value.split("#", 1)[0].split("?", 1)[0]
    path_part = unquote(path_part)
    if not path_part:
        return "anchor", source
    normalized = posixpath.normpath(posixpath.join(source.parent.as_posix(), path_part))
    if normalized == ".." or normalized.startswith("../"):
        return "LINK-ESCAPE", None
    return "local", PurePosixPath(normalized)


def rendered_local_links(
    markdown: str,
    source_path: str | PurePosixPath,
) -> tuple[RenderedLocalLink, ...]:
    """Resolve rendered Markdown links without consulting the filesystem.

    This is the narrow public adapter for validators that need the canonical
    CommonMark renderer and local-destination semantics but own a different
    storage context, such as an immutable Git source tree.  Callers decide how
    a resolved local path exists; this function never opens or stats it.
    """

    if not isinstance(markdown, str):
        raise TypeError("markdown must be text")
    raw_source = (
        source_path.as_posix()
        if isinstance(source_path, PurePosixPath)
        else source_path
    )
    if not isinstance(raw_source, str) or not raw_source:
        raise ValueError("source_path must be a repository-relative POSIX path")
    source = PurePosixPath(raw_source)
    if (
        not source.parts
        or source.is_absolute()
        or source.as_posix() != raw_source
        or "." in source.parts
        or ".." in source.parts
        or "\\" in raw_source
        or any(ord(character) < 32 or ord(character) == 127 for character in raw_source)
    ):
        raise ValueError(
            "source_path must be a canonical repository-relative POSIX path"
        )

    return tuple(
        RenderedLocalLink(kind=kind, raw_target=raw, target=target)
        for raw in _extract_links(markdown)
        for kind, target in (_local_destination(source, raw),)
    )


def _path_exists_without_dereference(
    root: Path, path: PurePosixPath, adapters: dict[PurePosixPath, PurePosixPath]
) -> bool:
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
        if profile == "content/archive":
            # ArchiveEnvelope.v1 payload links are historical evidence. Their
            # authority is resolved against source_commit/original_path by the
            # archive validator, never against the current worktree.
            continue
        for raw in _extract_links(context.texts[source]):
            kind, target = _local_destination(source, raw)
            if kind in {"external", "anchor"}:
                continue
            if kind.startswith("LINK-"):
                diagnostics.append(
                    _diag(
                        kind,
                        source,
                        profile,
                        "repository-relative local link",
                        kind.removeprefix("LINK-").casefold(),
                    )
                )
                continue
            assert target is not None
            if not _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            ):
                diagnostics.append(
                    _diag(
                        "LINK-BROKEN",
                        source,
                        profile,
                        "existing repository target",
                        "target is missing",
                    )
                )
                continue
            if (
                _is_current_authority(context, source)
                and target.as_posix().startswith("docs/98.archive/")
                and target != PurePosixPath("docs/98.archive/README.md")
            ):
                diagnostics.append(
                    _diag(
                        "LINK-ARCHIVE-BYPASS",
                        source,
                        profile,
                        "archive index boundary",
                        "direct archive target",
                    )
                )
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
                fence = (token[0], len(token))
                lines = []
            elif (
                token[0] == fence[0]
                and len(token) >= fence[1]
                and not marker.group(2).strip()
            ):
                blocks.append("\n".join(lines))
                fence = None
                lines = []
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


def _exact_rendered_heading_section(text: str, heading: str) -> str | None:
    """Slice one root heading from the same rendered block view as links."""

    lines = _rendered_container_lines(text)
    matches = [
        index
        for index, line in enumerate(lines)
        if line.depth == 0 and line.text == heading
    ]
    if len(matches) != 1:
        return None
    start = matches[0]
    level = len(heading) - len(heading.lstrip("#"))
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        candidate = re.match(r"^(#{1,6})\s", line.text)
        if line.depth == 0 and candidate and len(candidate.group(1)) <= level:
            end = index
            break
    return _join_rendered_container_lines(lines[start + 1 : end])


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
    block = next(
        (
            item
            for item in _fenced_blocks(section)
            if item.splitlines() and item.splitlines()[0] == expected_root
        ),
        "",
    )
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
                targets.append(base / pending / "spec.md")
                pending = None
    else:
        for name in re.findall(r"^[├└]── ([^/\n]+\.md)$", block, re.MULTILINE):
            if name != "README.md":
                targets.append(base / name)
    return targets


def _table_rows(
    declaration: DeclaredIndex, text: str
) -> list[tuple[PurePosixPath, str]]:
    section = (
        _after_exact_heading(text, declaration.table_anchor)
        if declaration.table_mode == "after"
        else _exact_heading_section(text, declaration.table_anchor)
    )
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
        actual = sorted(
            (
                p
                for p in context.paths
                if declaration.target_pattern.fullmatch(p.as_posix())
                and p != declaration.path
            ),
            key=lambda p: p.as_posix(),
        )
        actual_set = set(actual)
        tree = _tree_targets(declaration, context.texts[declaration.path])
        rows = _table_rows(declaration, context.texts[declaration.path])
        row_counter = collections.Counter(path for path, _ in rows)
        tree_counter = collections.Counter(tree)
        for target, count in sorted(
            row_counter.items(), key=lambda item: item[0].as_posix()
        ):
            target_key = target.as_posix()
            if count > 1:
                diagnostics.append(
                    _diag(
                        "INDEX-DUPLICATE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; {count} rows",
                    )
                )
            if target not in actual_set:
                diagnostics.append(
                    _diag(
                        "INDEX-STALE",
                        declaration.path,
                        profile,
                        f"target={target_key}; declared target",
                        f"target={target_key}; non-target row",
                    )
                )
        for target in actual:
            target_key = target.as_posix()
            if row_counter[target] == 0:
                diagnostics.append(
                    _diag(
                        "INDEX-MISSING",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; row is missing",
                    )
                )
            for row_target, row_status in rows:
                if row_target != target:
                    continue
                expected_status = str(
                    context.metadata[target].get("status", "")
                ).casefold()
                actual_status = STATUS_MAP.get(row_status.casefold(), "")
                if actual_status != expected_status:
                    diagnostics.append(
                        _diag(
                            "INDEX-STATUS",
                            declaration.path,
                            profile,
                            f"target={target_key}; status={expected_status}",
                            f"target={target_key}; status={actual_status or 'unknown'}",
                        )
                    )
                break
        for target in sorted(actual_set | set(tree), key=lambda p: p.as_posix()):
            if tree_counter[target] != (1 if target in actual_set else 0):
                target_key = target.as_posix()
                diagnostics.append(
                    _diag(
                        "INDEX-TREE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one declared tree target",
                        f"target={target_key}; {tree_counter[target]} entries",
                    )
                )
        # A resolved row that is not even in the inventory is stale regardless of disk state.
        if any(
            target not in path_set and target not in actual_set for target, _ in rows
        ):
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
        if not all(re.fullmatch(r":?-+:?", cell) for cell in delimiter):
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
BODY_IDENTIFIER_PATTERNS = {
    "requirement": re.compile(r"^REQ-[A-Z0-9-]+-[0-9]{2,3}$"),
    "criterion": re.compile(r"^VAL-[A-Z0-9-]+-[0-9]{3}$"),
    "work-item": re.compile(r"^[A-Z][A-Z0-9-]+-[0-9]{3}$"),
}


def _body_identifier_text(cell: str) -> str:
    """Normalize the same plain, code, or full-link identifier forms."""

    value = cell.strip()
    link = re.fullmatch(r"\[([^\]\n]+)\]\([^\n)]+\)", value)
    if link:
        value = link.group(1).strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


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
            path == prefix or prefix in path.parents for prefix in path_prefixes
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


def lifecycle_markdown_evidence(
    path: PurePosixPath,
    text: str,
    profile: DocumentProfile,
    snapshot_profiles: Mapping[PurePosixPath, str],
) -> LifecycleMarkdownEvidence:
    """Return lifecycle evidence without reading the filesystem.

    The caller owns Git provenance and passes one immutable proposed-snapshot
    text plus the complete selected-profile projection. This adapter only
    reuses the canonical CommonMark renderer, link extractor, heading slicer,
    and body-table parser already owned by this validator.
    """

    def local_links(raw_links: Iterable[str]) -> tuple[PurePosixPath, ...]:
        resolved: list[PurePosixPath] = []
        for raw_link in raw_links:
            kind, target = _local_destination(path, raw_link)
            if kind in {"local", "anchor"} and target is not None:
                resolved.append(target)
        return tuple(resolved)

    def selected_local_links(raw_links: Iterable[str]) -> tuple[PurePosixPath, ...]:
        return tuple(
            target for target in local_links(raw_links) if target in snapshot_profiles
        )

    all_links = local_links(_extract_links(text))
    rendered_lines = _rendered_container_lines(text)
    root_h2 = tuple(
        line.text[3:].strip()
        for line in rendered_lines
        if line.depth == 0
        and line.text.startswith("## ")
        and not line.text.startswith("### ")
    )
    required_headings_valid = all(
        _exact_rendered_heading_section(text, f"## {heading}") is not None
        for heading in profile.headings.required
    )
    allowed_headings_valid = all(
        heading in profile.headings.allowed for heading in root_h2
    )
    relationship_links: tuple[PurePosixPath, ...] = ()
    unresolved_relationship_links: tuple[PurePosixPath, ...] = ()
    relationship_section_valid = False
    body_rows: tuple[tuple[tuple[str, str], ...], ...] = ()
    body_table_links: tuple[PurePosixPath, ...] = ()
    body_contract_valid = False

    if profile.body_contract is not None:
        contract = profile.body_contract
        rows = _body_contract_rows(text, profile)
        relationship_section = _exact_rendered_heading_section(
            text, f"## {contract.section}"
        )
        relationship_section_valid = relationship_section is not None
        body_contract_valid = (
            required_headings_valid and allowed_headings_valid and rows is not None
        )
        collected: list[PurePosixPath] = []
        unresolved: list[PurePosixPath] = []
        if rows is not None:
            body_rows = tuple(tuple(row.items()) for row in rows)
            projection_columns = (
                ("Evidence",)
                if profile.profile_id == "sdlc/task"
                and "Evidence" in contract.required_columns
                else tuple(
                    column
                    for column in (
                        contract.source_link_column,
                        contract.target_link_column,
                    )
                    if column is not None
                )
            )
            projected_raw_links = tuple(
                raw_link
                for row in rows
                for column in projection_columns
                for raw_link in _extract_links(row[column], definitions_text=text)
            )
            projected_links = local_links(projected_raw_links)
            body_table_links = tuple(
                target for target in projected_links if target in snapshot_profiles
            )
            if profile.profile_id == "sdlc/task":
                unresolved.extend(
                    target
                    for target in projected_links
                    if target not in snapshot_profiles
                )
            for row in rows:
                if any(not value.strip() for value in row.values()):
                    body_contract_valid = False
                for identifier in contract.identifier_columns:
                    value = _body_identifier_text(row[identifier.column])
                    if value.startswith("N/A"):
                        if (
                            not contract.allow_explicit_exclusion
                            or BODY_LINK_EXCLUSION.fullmatch(value) is None
                        ):
                            body_contract_valid = False
                    elif (
                        BODY_IDENTIFIER_PATTERNS[identifier.kind].fullmatch(value)
                        is None
                    ):
                        body_contract_valid = False
            link_columns = (
                (contract.source_link_column, contract.allowed_source_profile_ids),
                (contract.target_link_column, contract.allowed_target_profile_ids),
            )
            for row in rows:
                for column, allowed_profiles in link_columns:
                    if column is None:
                        continue
                    cell = row[column].strip()
                    if cell.startswith("N/A"):
                        if (
                            not contract.allow_explicit_exclusion
                            or BODY_LINK_EXCLUSION.fullmatch(cell) is None
                        ):
                            body_contract_valid = False
                        continue
                    raw_links = _extract_links(cell, definitions_text=text)
                    resolved = local_links(raw_links)
                    if not raw_links or len(resolved) != len(raw_links):
                        body_contract_valid = False
                        continue
                    for target in resolved:
                        if target not in snapshot_profiles:
                            unresolved.append(target)
                            body_contract_valid = False
                        elif snapshot_profiles.get(target) not in allowed_profiles:
                            body_contract_valid = False
                        else:
                            collected.append(target)
        relationship_links = tuple(collected)
        unresolved_relationship_links = tuple(unresolved)
    else:
        heading = profile.role_decision.relationship_section
        section = (
            _exact_rendered_heading_section(text, f"## {heading}")
            if heading is not None
            else None
        )
        relationship_section_valid = section is not None
        if section is not None:
            rendered_definitions = _rendered_markdown(text)
            raw_relationship_links = local_links(
                _extract_rendered_links(
                    section, definitions_rendered=rendered_definitions
                )
            )
            relationship_links = tuple(
                target
                for target in raw_relationship_links
                if target in snapshot_profiles
            )
            unresolved_relationship_links = tuple(
                target
                for target in raw_relationship_links
                if target not in snapshot_profiles
            )
        body_contract_valid = (
            required_headings_valid and allowed_headings_valid and section is not None
        )

    task_terminal_valid = True
    if profile.profile_id == "sdlc/task":
        task_section = _exact_heading_section(text, "## Task Table")
        task_table = _first_visible_table(task_section or "")
        task_terminal_valid = False
        if task_table is not None:
            header, rows = task_table
            required = {"Status", "Result", "Evidence"}
            if required.issubset(header) and rows:
                positions = {value: header.index(value) for value in required}
                placeholder = re.compile(
                    r"(?i)^(?:|pending|not executed|not recorded|named repository "
                    r"evidence|tbd|todo|n/?a|[-—])$"
                )
                task_terminal_valid = all(
                    row[positions["Status"]].strip().casefold() in {"done", "archived"}
                    and placeholder.fullmatch(row[positions["Result"]].strip()) is None
                    and placeholder.fullmatch(row[positions["Evidence"]].strip())
                    is None
                    for row in rows
                )

    return LifecycleMarkdownEvidence(
        path=path,
        all_local_links=all_links,
        relationship_links=relationship_links,
        unresolved_relationship_links=unresolved_relationship_links,
        body_table_links=body_table_links,
        relationship_section_valid=relationship_section_valid,
        body_contract_valid=body_contract_valid,
        body_rows=body_rows,
        task_terminal_evidence_valid=task_terminal_valid,
    )


def _links_back_to(
    context: Context, owner: PurePosixPath, expected: PurePosixPath
) -> bool:
    for raw_link in _extract_links(context.texts[owner]):
        kind, target = _local_destination(owner, raw_link)
        if kind in {"local", "anchor"} and target == expected:
            return True
    return False


PROGRAM_LINEAGE_ROADMAP = PurePosixPath(
    "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md"
)
PROGRAM_LINEAGE_OVERLAY_HEADING = (
    "### 2026-07-15 template lifecycle disposition overlay"
)
PROGRAM_MUTABLE_STATES = frozenset({"draft", "active"})
PROGRAM_CURRENT_EXECUTION_STATES = frozenset({"draft", "active"})
PROGRAM_PATHS = {
    "sdlc/prd": re.compile(r"^docs/01\.requirements/({identifier})-[^/]+\.md$"),
    "sdlc/ard": re.compile(
        r"^docs/02\.architecture/requirements/({identifier})-[^/]+\.md$"
    ),
    "sdlc/adr": re.compile(
        r"^docs/02\.architecture/decisions/({identifier})-[^/]+\.md$"
    ),
    "sdlc/spec": re.compile(r"^docs/03\.specs/({identifier})-[^/]+/spec\.md$"),
}
PROGRAM_LIFECYCLE_AUTHORITY = {
    "prd": "draft -> active -> done | archived",
    "ard/adr": "draft -> active -> accepted | archived",
    "spec": "draft -> active -> done | archived",
    "plan/task": "draft -> active -> done | archived",
    "operations": "draft -> active -> accepted | archived",
    "archive record": "archived only",
}


def _program_owner_path(
    context: Context, profile_id: str, identifier: str
) -> PurePosixPath | None:
    """Resolve one numeric owner from the already bounded tracked inventory."""

    pattern_template = PROGRAM_PATHS[profile_id].pattern
    pattern = re.compile(pattern_template.format(identifier=re.escape(identifier)))
    matches = tuple(
        path
        for path in context.paths
        if context.profiles[path].profile_id == profile_id
        and pattern.fullmatch(path.as_posix()) is not None
    )
    return matches[0] if len(matches) == 1 else None


def _program_local_targets(
    context: Context, source: PurePosixPath
) -> frozenset[PurePosixPath]:
    """Return rendered, normalized, repository-local targets for one owner."""

    targets: set[PurePosixPath] = set()
    for raw_link in _extract_links(context.texts.get(source, "")):
        kind, target = _local_destination(source, raw_link)
        if kind == "local" and target is not None:
            targets.add(target)
    return frozenset(targets)


def _program_status(context: Context, path: PurePosixPath | None) -> str:
    if path is None:
        return ""
    value = context.metadata.get(path, {}).get("status", "")
    return value if isinstance(value, str) else ""


def _reference_definition_labels(text: str) -> frozenset[str]:
    """Collect only rendered definitions with a fully valid destination/title."""

    rendered = _mask_inline_html_tokens(_rendered_markdown(text))
    return frozenset(_reference_definitions(rendered))


def _rendered_inline_cell_text(value: str, definitions: frozenset[str]) -> str:
    """Replace rendered links using a code-masked offset-stable scan."""

    visible = _mask_inline_html_tokens(value)
    links = _scan_markdown_links(visible, {label: "" for label in definitions})
    code_masked = _mask_inline_code_spans(visible)
    output: list[str] = []
    cursor = 0

    def source_start(encoded_index: int) -> int:
        if encoded_index >= len(visible.source_offsets):
            return len(value)
        return visible.source_offsets[encoded_index]

    def source_end(encoded_index: int) -> int:
        if encoded_index <= 0:
            return 0
        return visible.source_offsets[encoded_index - 1] + 1

    for link in links:
        if code_masked[link.start] == " ":
            continue
        output.append(value[cursor : source_start(link.start)])
        encoded_label_start = link.start + 1
        encoded_label_end = encoded_label_start + len(link.label)
        output.append(
            value[source_start(encoded_label_start) : source_end(encoded_label_end)]
        )
        cursor = source_end(link.end)
    output.append(value[cursor:])
    return "".join(output)


def _rendered_character_reference_text(value: str) -> str:
    """Decode rendered character references outside code and escapes."""

    visible = _mask_inline_code_spans(value)
    output: list[str] = []
    cursor = 0
    while cursor < len(value):
        if (
            visible[cursor] == "\\"
            and cursor + 1 < len(value)
            and _markdown_escapable(value[cursor + 1])
        ):
            output.append(value[cursor + 1])
            cursor += 2
            continue
        if visible[cursor] == "&":
            reference = _markdown_character_reference(value, cursor, len(value))
            if reference is not None:
                decoded, cursor = reference
                output.append(decoded)
                continue
        output.append(value[cursor])
        cursor += 1
    return "".join(output)


def _normalized_lifecycle_cell(
    value: str, definitions: frozenset[str] = frozenset()
) -> str:
    rendered = _rendered_inline_cell_text(value, definitions)
    rendered = _rendered_inline_html_text(rendered)
    rendered = _rendered_character_reference_text(rendered)
    normalized = unicodedata.normalize("NFKC", rendered).casefold()
    normalized = normalized.replace("\\|", "|").replace("→", "->")
    normalized = re.sub(r"[`*_]+", "", normalized)
    normalized = re.sub(r"\s*->\s*", " -> ", normalized)
    normalized = re.sub(r"\s*\|\s*", " | ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _optional_gfm_table_cells(line: str) -> list[str]:
    """Parse a GFM table row with optional leading and trailing pipes."""

    stripped = line.strip()
    if "|" not in stripped:
        return []
    return _gfm_table_cells(stripped if stripped.startswith("|") else f"| {stripped}")


def _strip_blockquote_marker(line: str) -> str | None:
    """Strip one explicit blockquote marker from a rendered container line."""

    marker = re.match(r"^ {0,3}>[ \t]?(.*)$", line)
    return marker.group(1) if marker is not None else None


def _strip_list_item_marker(line: str) -> tuple[str, int] | None:
    """Return first-line content and continuation indent for one list item."""

    leading = re.match(r"^ {0,3}", line)
    assert leading is not None
    marker = re.match(r"(?:[*+-]|\d{1,9}[.)])", line[leading.end() :])
    if marker is None:
        return None
    marker_text = marker.group(0)
    cursor = leading.end() + marker.end()
    marker_end_column = leading.end() + len(marker_text)
    whitespace_start = cursor
    column = marker_end_column
    while cursor < len(line) and line[cursor] in " \t":
        column = column + 1 if line[cursor] == " " else ((column // 4) + 1) * 4
        cursor += 1
    body = line[cursor:]
    if body and cursor == whitespace_start:
        return None
    if not body:
        padding = 1
        content = ""
    elif column - marker_end_column <= 4:
        padding = column - marker_end_column
        content = body
    else:
        padding = 1
        content = " " * (column - marker_end_column - 1) + body
    content_indent = marker_end_column + padding
    return content, content_indent


def _strip_indentation_columns(line: str, required: int) -> str | None:
    """Strip visual indentation columns, preserving a tab's overshoot."""

    column = 0
    cursor = 0
    while cursor < len(line) and column < required:
        character = line[cursor]
        if character == " ":
            next_column = column + 1
        elif character == "\t":
            next_column = ((column // 4) + 1) * 4
        else:
            return None
        cursor += 1
        if next_column > required:
            return " " * (next_column - required) + line[cursor:]
        column = next_column
    return line[cursor:] if column == required else None


def _starts_lazy_continuation_block(line: str) -> bool:
    """Return whether an unmarked line starts a real container/block boundary."""

    if line.startswith(("    ", "\t")):
        return True
    if _strip_blockquote_marker(line) is not None:
        return True
    if _strip_list_item_marker(line) is not None:
        return True
    if re.match(r"^ {0,3}(?:`{3,}|~{3,})", line) is not None:
        return True
    if re.match(r"^ {0,3}#{1,6}(?:[ \t]+|$)", line) is not None:
        return True
    if (
        re.fullmatch(
            r" {0,3}(?:(?:\*[ \t]*){3,}|"
            r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})",
            line,
        )
        is not None
    ):
        return True
    if re.match(r"^ {0,3}(?:<!--|<\?|<!\[CDATA\[|<![A-Z])", line) is not None:
        return True
    return _HTML_BLOCK_TAG.match(line) is not None or (
        _HTML_COMPLETE_TAG.match(line) is not None
    )


def _is_lazy_paragraph_line(line: str) -> bool:
    return bool(line.strip()) and not _starts_lazy_continuation_block(line)


def _is_lazy_paragraph_continuation(line: str) -> bool:
    """Admit indentation as text while a container paragraph remains open."""

    return bool(line.strip()) and (
        line.startswith(("    ", "\t")) or not _starts_lazy_continuation_block(line)
    )


def _explicit_container_paragraph_state(line: str, previous_paragraph: bool) -> bool:
    """Track paragraphs for explicitly owned quote/list continuation lines."""

    if previous_paragraph and re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", line):
        return False
    return _is_lazy_paragraph_line(line)


def _owned_container_paragraph_state(
    lines: Sequence[str],
    previous_paragraph: bool,
    *,
    lazy_continuation: bool = False,
    lazy_lines: frozenset[int] = frozenset(),
) -> bool:
    """Close paragraph state when owned lines end in a valid definition."""

    value = "\n".join(lines)
    _, definition_spans = _reference_definitions_with_spans(
        value,
        lazy_lines=lazy_lines,
    )
    if any(end == len(value) for _, end in definition_spans):
        return False
    if lazy_continuation:
        return True
    return _explicit_container_paragraph_state(lines[-1], previous_paragraph)


@dataclass(frozen=True)
class RenderedBlockLine:
    container_id: int
    depth: int
    text: str
    lazy_continuation: bool = False


class RenderedMarkdown(str):
    """Rendered text carrying line provenance needed by later block scans."""

    lazy_lines: frozenset[int]

    def __new__(
        cls,
        value: str,
        lazy_lines: frozenset[int] = frozenset(),
    ) -> "RenderedMarkdown":
        instance = super().__new__(cls, value)
        instance.lazy_lines = lazy_lines
        return instance


def _rendered_container_lines(text: str) -> tuple[RenderedBlockLine, ...]:
    """Render containers outside-in so outer opaque state hides descendants."""

    contents = _commonmark_splitlines(
        _render_container_markdown(text, defer_indented_code=True)
    )
    depths = [0] * len(contents)
    container_paths: list[tuple[int, ...]] = [()] * len(contents)
    lazy_continuations = [False] * len(contents)
    next_container_id = 0
    while True:
        changed = False
        index = 0
        while index < len(contents):
            depth = depths[index]
            container_path = container_paths[index]
            stripped = _strip_blockquote_marker(contents[index])
            if stripped is not None:
                end = index + 1
                stripped_lines = [stripped]
                stripped_lazy = [lazy_continuations[index]]
                paragraph_open = _owned_container_paragraph_state(
                    stripped_lines,
                    False,
                    lazy_lines=frozenset(
                        offset for offset, lazy in enumerate(stripped_lazy) if lazy
                    ),
                )
                while (
                    end < len(contents)
                    and depths[end] == depth
                    and container_paths[end] == container_path
                ):
                    candidate = _strip_blockquote_marker(contents[end])
                    if candidate is not None:
                        stripped_lines.append(candidate)
                        stripped_lazy.append(lazy_continuations[end])
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    if paragraph_open and _is_lazy_paragraph_continuation(
                        contents[end]
                    ):
                        stripped_lines.append(contents[end])
                        lazy_continuations[end] = True
                        stripped_lazy.append(True)
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_continuation=True,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    break
            else:
                list_item = _strip_list_item_marker(contents[index])
                if list_item is None:
                    index += 1
                    continue
                first_line, content_indent = list_item
                end = index + 1
                stripped_lines = [first_line]
                stripped_lazy = [lazy_continuations[index]]
                paragraph_open = _owned_container_paragraph_state(
                    stripped_lines,
                    False,
                    lazy_lines=frozenset(
                        offset for offset, lazy in enumerate(stripped_lazy) if lazy
                    ),
                )
                while (
                    end < len(contents)
                    and depths[end] == depth
                    and container_paths[end] == container_path
                ):
                    continuation = contents[end]
                    if not continuation.strip():
                        stripped_lines.append("")
                        stripped_lazy.append(lazy_continuations[end])
                        paragraph_open = False
                        end += 1
                        continue
                    stripped_continuation = _strip_indentation_columns(
                        continuation, content_indent
                    )
                    if stripped_continuation is not None:
                        stripped_lines.append(stripped_continuation)
                        stripped_lazy.append(lazy_continuations[end])
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    if paragraph_open and _is_lazy_paragraph_continuation(continuation):
                        stripped_lines.append(continuation)
                        lazy_continuations[end] = True
                        stripped_lazy.append(True)
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_continuation=True,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    break
            visible = _render_container_markdown(
                "\n".join(stripped_lines),
                defer_indented_code=True,
                paragraph_continuation_lines=frozenset(
                    offset for offset, lazy in enumerate(stripped_lazy) if lazy
                ),
            ).split("\n")
            visible.extend("" for _ in range(len(stripped_lines) - len(visible)))
            child_container_id = next_container_id
            next_container_id += 1
            for offset, line in enumerate(visible[: len(stripped_lines)]):
                position = index + offset
                contents[position] = line
                depths[position] += 1
                container_paths[position] = (
                    *container_path,
                    child_container_id,
                )
            changed = True
            index = end
        if not changed:
            break

    rendered: list[RenderedBlockLine] = []
    index = 0
    container_id = 0
    while index < len(contents):
        depth = depths[index]
        container_path = container_paths[index]
        end = index + 1
        while (
            end < len(contents)
            and depths[end] == depth
            and container_paths[end] == container_path
        ):
            end += 1
        visible = _render_container_markdown(
            "\n".join(contents[index:end]),
            paragraph_continuation_lines=frozenset(
                position - index
                for position in range(index, end)
                if lazy_continuations[position]
            ),
        ).split("\n")
        visible.extend("" for _ in range(end - index - len(visible)))
        rendered.extend(
            RenderedBlockLine(
                container_id,
                depth,
                line,
                lazy_continuations[index + offset],
            )
            for offset, line in enumerate(visible[: end - index])
        )
        index = end
        container_id += 1
    return tuple(rendered)


def _join_rendered_container_lines(
    lines: Sequence[RenderedBlockLine],
) -> str:
    """Join rendered lines with CommonMark/GFM inline-block boundaries."""

    def same_container(left: int, right: int) -> bool:
        return (
            lines[left].container_id == lines[right].container_id
            and lines[left].depth == lines[right].depth
        )

    table_lines: set[int] = set()
    table_index = 0
    while table_index < len(lines) - 1:
        header = _optional_gfm_table_cells(lines[table_index].text)
        delimiter = _optional_gfm_table_cells(lines[table_index + 1].text)
        if (
            same_container(table_index, table_index + 1)
            and not lines[table_index].lazy_continuation
            and not lines[table_index + 1].lazy_continuation
            and header
            and len(header) == len(delimiter)
            and all(re.fullmatch(r":?-+:?", cell) for cell in delimiter)
        ):
            cursor = table_index + 2
            table_lines.update({table_index, table_index + 1})
            while (
                cursor < len(lines)
                and same_container(table_index, cursor)
                and not lines[cursor].lazy_continuation
                and _optional_gfm_table_cells(lines[cursor].text)
            ):
                table_lines.add(cursor)
                cursor += 1
            table_index = cursor
            continue
        table_index += 1

    atx = re.compile(r" {0,3}#{1,6}(?:[ \t]+.*)?")
    list_item = re.compile(r" {0,3}(?:[*+-]|\d{1,9}[.)])(?:[ \t]+.*)?")
    setext = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
    thematic = re.compile(
        r" {0,3}(?:(?:\*[ \t]*){3,}|"
        r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})"
    )

    definition_lines: set[int] = set()
    definition_end_lines: set[int] = set()
    segment_start = 0
    while segment_start < len(lines):
        segment_end = segment_start + 1
        while segment_end < len(lines) and same_container(segment_start, segment_end):
            segment_end += 1
        segment = "\n".join(line.text for line in lines[segment_start:segment_end])
        _, definition_spans = _reference_definitions_with_spans(
            segment,
            lazy_lines=frozenset(
                offset
                for offset, line in enumerate(lines[segment_start:segment_end])
                if line.lazy_continuation
            ),
        )
        for definition_start, definition_end in definition_spans:
            first_line = segment.count("\n", 0, definition_start)
            last_line = segment.count("\n", 0, definition_end)
            definition_lines.update(
                range(
                    segment_start + first_line,
                    segment_start + last_line + 1,
                )
            )
            definition_end_lines.add(segment_start + last_line)
        segment_start = segment_end

    paragraph_continuation_lines: set[int] = set()
    segment_start = 0
    while segment_start < len(lines):
        segment_end = segment_start + 1
        while segment_end < len(lines) and same_container(segment_start, segment_end):
            segment_end += 1
        paragraph_open = False
        for index in range(segment_start, segment_end):
            value = lines[index].text
            if not value.strip():
                paragraph_open = False
                continue
            if index in definition_lines:
                paragraph_open = False
                continue
            if (
                atx.fullmatch(value) is not None
                or thematic.fullmatch(value) is not None
                or (
                    paragraph_open
                    and not lines[index].lazy_continuation
                    and setext.fullmatch(value) is not None
                )
            ):
                paragraph_open = False
                continue
            if paragraph_open:
                paragraph_continuation_lines.add(index)
            paragraph_open = True
        segment_start = segment_end

    def starts_inline_block(value: str) -> bool:
        return any(
            pattern.fullmatch(value) is not None
            for pattern in (atx, list_item, setext, thematic)
        )

    def ends_inline_block(value: str) -> bool:
        return any(
            pattern.fullmatch(value) is not None for pattern in (atx, setext, thematic)
        )

    def hard_bound_table_cells(value: str) -> str:
        output: list[str] = []
        backslashes = 0
        for character in value:
            if character == "|" and backslashes % 2 == 0:
                output.append("|\n\n")
            else:
                output.append(character)
            backslashes = backslashes + 1 if character == "\\" else 0
        return "".join(output)

    output: list[str] = []
    output_lazy_lines: set[int] = set()
    output_line = 0

    def append_output(value: str, *, lazy: bool = False) -> None:
        nonlocal output_line
        if output:
            output_line += 1
        if lazy:
            output_lazy_lines.add(output_line)
        output.append(value)
        output_line += value.count("\n")

    for index, line in enumerate(lines):
        marker_boundary = (
            index not in definition_lines
            and not line.lazy_continuation
            and starts_inline_block(line.text)
        )
        previous_marker_boundary = (
            index > 0
            and index - 1 not in definition_lines
            and not lines[index - 1].lazy_continuation
            and ends_inline_block(lines[index - 1].text)
        )
        setext_content_boundary = (
            index + 1 < len(lines)
            and same_container(index, index + 1)
            and index not in definition_lines
            and index + 1 not in definition_lines
            and index not in paragraph_continuation_lines
            and not lines[index + 1].lazy_continuation
            and setext.fullmatch(lines[index + 1].text) is not None
        )
        definition_end_boundary = (
            index > 0
            and index - 1 in definition_end_lines
            and index not in definition_lines
        )
        if index > 0 and (
            not same_container(index - 1, index)
            or marker_boundary
            or previous_marker_boundary
            or setext_content_boundary
            or definition_end_boundary
            or index in table_lines
        ):
            append_output("")
        append_output(
            hard_bound_table_cells(line.text) if index in table_lines else line.text,
            lazy=line.lazy_continuation,
        )
    return RenderedMarkdown(
        "\n".join(output),
        frozenset(output_lazy_lines),
    )


def _rendered_markdown(text: str) -> str:
    """Return one container-aware rendered Markdown view."""

    return _join_rendered_container_lines(_rendered_container_lines(text))


def _visible_tables(text: str) -> tuple[tuple[list[str], list[list[str]]], ...]:
    """Parse all visible GFM-shaped tables, preserving overflow cells."""

    lines = _rendered_container_lines(text)
    tables: list[tuple[list[str], list[list[str]]]] = []
    index = 0
    while index < len(lines) - 1:
        header_line = lines[index]
        delimiter_line = lines[index + 1]
        header = _optional_gfm_table_cells(header_line.text)
        delimiter = _optional_gfm_table_cells(delimiter_line.text)
        if (
            header_line.container_id != delimiter_line.container_id
            or header_line.depth != delimiter_line.depth
            or header_line.lazy_continuation
            or delimiter_line.lazy_continuation
            or not header
            or len(header) != len(delimiter)
            or not all(re.fullmatch(r":?-+:?", cell) for cell in delimiter)
        ):
            index += 1
            continue
        rows: list[list[str]] = []
        cursor = index + 2
        while cursor < len(lines):
            row_line = lines[cursor]
            cells = _optional_gfm_table_cells(row_line.text)
            if (
                row_line.container_id != header_line.container_id
                or row_line.depth != header_line.depth
                or row_line.lazy_continuation
                or not cells
            ):
                break
            rows.append(cells)
            cursor += 1
        tables.append((header, rows))
        index = cursor
    return tuple(tables)


def _has_duplicate_lifecycle_authority(text: str) -> bool:
    """Detect the complete Stage 99 lifecycle map after rendered normalization."""

    definitions = _reference_definition_labels(text)
    for header, rows in _visible_tables(text):
        normalized_header = tuple(
            _normalized_lifecycle_cell(cell, definitions) for cell in header
        )
        if (
            normalized_header.count("document family") != 1
            or normalized_header.count("lifecycle transition") != 1
        ):
            continue
        family_index = normalized_header.index("document family")
        transition_index = normalized_header.index("lifecycle transition")
        required_width = max(family_index, transition_index) + 1
        normalized_rows: dict[str, set[str]] = collections.defaultdict(set)
        for row in rows:
            if len(row) < required_width:
                continue
            family = _normalized_lifecycle_cell(row[family_index], definitions)
            transition = _normalized_lifecycle_cell(row[transition_index], definitions)
            normalized_rows[family].add(transition)
        if all(
            transition in normalized_rows.get(family, set())
            for family, transition in PROGRAM_LIFECYCLE_AUTHORITY.items()
        ):
            return True
    return False


def _program_reciprocal_diagnostics(
    context: Context,
    program: ProgramLineage,
    relation: ProgramRelation,
    *,
    follow_up: bool,
) -> list[Diagnostic]:
    spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
    prd = _program_owner_path(context, "sdlc/prd", program.prd_id)
    ard = _program_owner_path(context, "sdlc/ard", program.ard_id)
    decision = _program_owner_path(context, "sdlc/adr", relation.decision_id)
    if spec is None or prd is None or ard is None or (follow_up and decision is None):
        return []
    required_from_spec = {prd, ard}
    if follow_up:
        assert decision is not None
        required_from_spec.add(decision)
    missing: list[str] = []
    spec_targets = _program_local_targets(context, spec)
    for label, target in (("PRD", prd), ("ARD", ard), ("ADR", decision)):
        if (
            target is not None
            and target in required_from_spec
            and target not in spec_targets
        ):
            missing.append(f"Spec->{label}")
    for label, upstream in (("PRD", prd), ("ARD", ard), ("ADR", decision)):
        if (
            upstream is not None
            and (
                _program_status(context, upstream) in PROGRAM_MUTABLE_STATES
                or (follow_up and label == "ADR")
            )
            and spec not in _program_local_targets(context, upstream)
        ):
            missing.append(f"{label}->Spec")
    if not missing:
        return []
    return [
        _diag(
            "PROGRAM-LINEAGE-RECIPROCAL",
            spec,
            context.profiles[spec].profile_id,
            "rendered reciprocal links required by the mutable relation",
            ", ".join(sorted(missing)),
        )
    ]


def _historical_exception_diagnostics(
    context: Context,
    program: ProgramLineage,
    follow_up: ProgramFollowUp,
) -> list[Diagnostic]:
    if follow_up.evidence_mode != "successor-record":
        return []
    spec = _program_owner_path(context, "sdlc/spec", follow_up.spec_id)
    prd = _program_owner_path(context, "sdlc/prd", program.prd_id)
    ard = _program_owner_path(context, "sdlc/ard", program.ard_id)
    decision = _program_owner_path(context, "sdlc/adr", follow_up.decision_id)
    exact_relation = (
        program.prd_id == "005"
        and program.ard_id == "0008"
        and follow_up.spec_id == "033"
        and follow_up.decision_id == "0017"
        and follow_up.state == "done"
    )
    adr_agrees = (
        spec is not None
        and prd is not None
        and ard is not None
        and decision is not None
        and _program_status(context, decision) == "accepted"
        and {spec, prd, ard}.issubset(_program_local_targets(context, decision))
    )
    roadmap_section = (
        _exact_rendered_heading_section(
            context.texts.get(PROGRAM_LINEAGE_ROADMAP, ""),
            PROGRAM_LINEAGE_OVERLAY_HEADING,
        )
        if PROGRAM_LINEAGE_ROADMAP in context.texts
        else None
    )
    overlay_agrees = (
        spec is not None
        and roadmap_section is not None
        and spec
        in {
            target
            for raw_link in _extract_rendered_links(roadmap_section)
            for kind, target in [_local_destination(PROGRAM_LINEAGE_ROADMAP, raw_link)]
            if kind == "local" and target is not None
        }
    )
    if exact_relation and adr_agrees and overlay_agrees:
        return []
    owner = spec or decision or prd or PROGRAM_LINEAGE_ROADMAP
    profile = (
        context.profiles[owner].profile_id if owner in context.profiles else "sdlc/spec"
    )
    return [
        _diag(
            "PROGRAM-LINEAGE-HISTORICAL-EXCEPTION",
            owner,
            profile,
            "exact PRD-005/ARD-0008/Spec-033/ADR-0017 registry, ADR, and Current-overlay agreement",
            "successor-record evidence is incomplete or outside the named exception",
        )
    ]


def _current_execution_link_graph(
    context: Context,
) -> dict[PurePosixPath, frozenset[PurePosixPath]]:
    """Return rendered local links for every current Plan/Task node."""

    return {
        path: _program_local_targets(context, path)
        for path in context.paths
        if context.profiles[path].profile_id in {"sdlc/plan", "sdlc/task"}
        and _program_status(context, path) in PROGRAM_CURRENT_EXECUTION_STATES
    }


@dataclass
class CurrentExecutionIndex:
    graph: dict[PurePosixPath, frozenset[PurePosixPath]]
    adjacency: dict[PurePosixPath, frozenset[PurePosixPath]]
    incoming: dict[PurePosixPath, frozenset[PurePosixPath]]
    component_by_node: dict[PurePosixPath, tuple[PurePosixPath, ...]]
    component_cache: dict[
        tuple[PurePosixPath, tuple[PurePosixPath, ...]],
        tuple[PurePosixPath, ...],
    ]
    steps: int


@dataclass(frozen=True)
class ExecutionComponentScan:
    paths: tuple[PurePosixPath, ...]
    steps: int


def _current_execution_index(
    graph: dict[PurePosixPath, frozenset[PurePosixPath]],
) -> CurrentExecutionIndex:
    """Index execution adjacency and connected components once."""

    frozen_graph = {path: frozenset(targets) for path, targets in graph.items()}
    adjacency = {path: set() for path in frozen_graph}
    incoming: dict[PurePosixPath, set[PurePosixPath]] = {}
    steps = 0
    for source, targets in frozen_graph.items():
        for target in targets:
            steps += 1
            incoming.setdefault(target, set()).add(source)
            if target in frozen_graph:
                adjacency[source].add(target)
                adjacency[target].add(source)

    component_by_node: dict[PurePosixPath, tuple[PurePosixPath, ...]] = {}
    visited: set[PurePosixPath] = set()
    for root in frozen_graph:
        steps += 1
        if root in visited:
            continue
        visited.add(root)
        pending = [root]
        members: list[PurePosixPath] = []
        while pending:
            source = pending.pop()
            members.append(source)
            steps += 1
            for candidate in adjacency[source]:
                steps += 1
                if candidate not in visited:
                    visited.add(candidate)
                    pending.append(candidate)
        component = tuple(sorted(members, key=lambda item: item.as_posix()))
        for member in members:
            component_by_node[member] = component
            steps += 1

    return CurrentExecutionIndex(
        frozen_graph,
        {path: frozenset(targets) for path, targets in adjacency.items()},
        {path: frozenset(sources) for path, sources in incoming.items()},
        component_by_node,
        {},
        steps,
    )


def _current_execution_component_scan(
    spec: PurePosixPath,
    spec_targets: frozenset[PurePosixPath],
    index: CurrentExecutionIndex,
) -> ExecutionComponentScan:
    """Close one Spec's execution seeds through cached graph components."""

    execution_targets = tuple(
        sorted(
            (target for target in spec_targets if target in index.graph),
            key=lambda item: item.as_posix(),
        )
    )
    cache_key = (spec, execution_targets)
    cached = index.component_cache.get(cache_key)
    if cached is not None:
        return ExecutionComponentScan(cached, 0)

    seeds = set(index.incoming.get(spec, ()))
    seeds.update(execution_targets)
    members: set[PurePosixPath] = set()
    seen_components: set[PurePosixPath] = set()
    steps = len(seeds)
    for seed in sorted(seeds, key=lambda item: item.as_posix()):
        component = index.component_by_node[seed]
        representative = component[0]
        if representative in seen_components:
            continue
        seen_components.add(representative)
        members.update(component)
        steps += len(component)
    result = tuple(sorted(members, key=lambda item: item.as_posix()))
    index.component_cache[cache_key] = result
    return ExecutionComponentScan(result, steps)


def _current_execution_component(
    context: Context,
    spec: PurePosixPath,
    index: CurrentExecutionIndex,
) -> tuple[PurePosixPath, ...]:
    """Close the current execution component seeded only by one relation Spec.

    A Plan/Task node is in scope when a rendered local link joins it directly
    to the Spec or transitively to another scoped execution node. Disconnected
    components therefore remain outside this program relation.
    """

    return _current_execution_component_scan(
        spec,
        _program_local_targets(context, spec),
        index,
    ).paths


def _program_execution_diagnostics(
    context: Context, program: ProgramLineage
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    graph = _current_execution_link_graph(context)
    execution_index = _current_execution_index(graph)
    relations = (*program.tranches, *program.follow_ups)
    dependency_ready = next(
        (
            relation
            for relation in program.tranches
            if relation.state not in {"done", "archived"}
        ),
        None,
    )
    for relation in relations:
        spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
        if spec is None:
            continue
        component = _current_execution_component(context, spec, execution_index)
        plans = tuple(
            path
            for path in component
            if context.profiles[path].profile_id == "sdlc/plan"
        )
        tasks = tuple(
            path
            for path in component
            if context.profiles[path].profile_id == "sdlc/task"
        )
        direct_spec_links = all(spec in graph[path] for path in component)
        reciprocal_pair = (
            len(plans) == 1
            and len(tasks) == 1
            and tasks[0] in graph[plans[0]]
            and plans[0] in graph[tasks[0]]
        )
        valid_ready_state = relation == dependency_ready and (
            not component
            or (
                len(plans) == 1
                and len(tasks) == 1
                and direct_spec_links
                and reciprocal_pair
            )
        )
        valid_blocked_state = relation != dependency_ready and not component
        if valid_ready_state or valid_blocked_state:
            continue
        diagnostics.append(
            _diag(
                "PROGRAM-LINEAGE-EXECUTION-GATE",
                spec,
                context.profiles[spec].profile_id,
                "zero current execution component or one closed reciprocal current Plan/Task component with direct Spec links for the first unfinished original tranche, and none for remaining original tranches or follow-ups",
                f"component={len(component)}, plans={len(plans)}, tasks={len(tasks)}, direct-spec={direct_spec_links}, reciprocal={reciprocal_pair}, dependency-ready-original={relation == dependency_ready}",
            )
        )
    return diagnostics


def _program_lineage_diagnostics(
    context: Context, program_lineage: Sequence[ProgramLineage]
) -> list[Diagnostic]:
    """Validate registry relations against immutable bodies and current evidence."""

    diagnostics: list[Diagnostic] = []
    for program in program_lineage:
        for relation in (*program.tranches, *program.follow_ups):
            spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
            actual_state = _program_status(context, spec)
            if spec is None or actual_state != relation.state:
                owner = spec or _program_owner_path(context, "sdlc/prd", program.prd_id)
                if owner is not None:
                    diagnostics.append(
                        _diag(
                            "PROGRAM-LINEAGE-STATE",
                            owner,
                            context.profiles[owner].profile_id,
                            relation.state,
                            actual_state or "missing Spec owner",
                        )
                    )
            if relation.state not in PROGRAM_MUTABLE_STATES:
                continue
            if isinstance(relation, ProgramFollowUp):
                if relation.evidence_mode == "reciprocal-body":
                    diagnostics.extend(
                        _program_reciprocal_diagnostics(
                            context, program, relation, follow_up=True
                        )
                    )
            else:
                diagnostics.extend(
                    _program_reciprocal_diagnostics(
                        context, program, relation, follow_up=False
                    )
                )
        for follow_up in program.follow_ups:
            diagnostics.extend(
                _historical_exception_diagnostics(context, program, follow_up)
            )
        diagnostics.extend(_program_execution_diagnostics(context, program))
    for path in context.paths:
        if path.as_posix().startswith(
            "docs/00.agent-governance/"
        ) and _has_duplicate_lifecycle_authority(context.texts[path]):
            diagnostics.append(
                _diag(
                    "PROGRAM-LINEAGE-DUPLICATE-AUTHORITY",
                    path,
                    context.profiles[path].profile_id,
                    "Stage 99 registry/schema/governance pointers without an exact lifecycle owner table",
                    "complete normalized lifecycle transition table",
                )
            )
    return diagnostics


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
            (
                "source",
                contract.source_link_column,
                contract.allowed_source_profile_ids,
            ),
            (
                "target",
                contract.target_link_column,
                contract.allowed_target_profile_ids,
            ),
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
                raw_links = _extract_links(cell, definitions_text=context.texts[path])
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


def _first_cell_target(owner: PurePosixPath, cell: str) -> PurePosixPath | None:
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
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-TREE-MISSING",
                        declaration.path,
                        profile,
                        f"target={target_key}; one tree entry",
                        f"target={target_key}; entry is missing",
                    )
                )
            if target not in expected and tree_counter[target]:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-TREE-STALE",
                        declaration.path,
                        profile,
                        f"target={target_key}; tracked canonical artifact",
                        f"target={target_key}; stale tree entry",
                    )
                )
            if tree_counter[target] > 1:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-TREE-DUPLICATE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one tree entry",
                        f"target={target_key}; {tree_counter[target]} entries",
                    )
                )
        for target in sorted(
            expected_rows | set(rows), key=lambda item: item.as_posix()
        ):
            target_key = target.as_posix()
            if target in expected_rows and row_counter[target] == 0:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-ROW-MISSING",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; row is missing",
                    )
                )
            if target not in expected_rows and row_counter[target]:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-ROW-STALE",
                        declaration.path,
                        profile,
                        f"target={target_key}; tracked canonical artifact",
                        f"target={target_key}; stale table row",
                    )
                )
            if row_counter[target] > 1:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-ROW-DUPLICATE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; {row_counter[target]} rows",
                    )
                )
    return diagnostics


def _owner_candidate(context: Context, path: PurePosixPath) -> bool:
    profile = context.profiles[path]
    status = str(context.metadata[path].get("status", "")).casefold()
    if profile.mode != "authored" or profile.profile_class in {"readme", "exception"}:
        return False
    if profile.profile_id == "content/archive" or status not in {
        "active",
        "accepted",
    }:
        return False
    return not any(pattern.match(path.as_posix()) for pattern in OWNER_EXCLUSIONS)


def _traceability_lineage(context: Context, path: PurePosixPath) -> str:
    visible = _visible_markdown(context.texts[path])
    match = re.search(
        r"^## Traceability\s*$([\s\S]*?)(?=^## |\Z)", visible, re.MULTILINE
    )
    if match:
        for raw in _extract_links(match.group(1), definitions_text=visible):
            kind, target = _local_destination(path, raw)
            if (
                kind == "local"
                and target is not None
                and (
                    re.fullmatch(
                        r"docs/01\.requirements/[0-9]{3}-[^/]+\.md", target.as_posix()
                    )
                    or re.fullmatch(
                        r"docs/03\.specs/[0-9]{3}-[^/]+/spec\.md", target.as_posix()
                    )
                )
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
        "product-requirements",
        "architecture-requirements",
        "architecture-decision-record",
        "technical-specification",
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
        return "", _diag(
            "OWNER-KEY-MISSING",
            path,
            context.profiles[path].profile_id,
            "role|scope|lineage",
            "empty owner-key component",
        )
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
            diagnostics.append(
                _diag(
                    "OWNER-DUPLICATE",
                    min(paths, key=lambda p: p.as_posix()),
                    context.profiles[paths[0]].profile_id,
                    "one current owner",
                    json.dumps(ordered, ensure_ascii=False),
                )
            )
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
        index
        for index, line in enumerate(visible)
        if line == GOVERNANCE_CURRENT_HEADING
    ]
    if len(headings) != 1:
        return None
    parent_h2 = next(
        (line for line in reversed(visible[: headings[0]]) if re.match(r"^##\s", line)),
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
        if profile.profile_id != "governance/reference" or profile.mode != "authored":
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
        if profile.profile_id != "governance/reference" or profile.mode != "authored":
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
        (line for line in reversed(visible[: matches[0]]) if re.match(r"^##\s", line)),
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
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-COLLECTION-MISSING",
                    pack.collection_readme,
                    collection_profile,
                    f"one Current pack row for {pack.pack_readme.as_posix()}",
                    "heading or table is missing or malformed",
                )
            )
        else:
            counter = collections.Counter(current_rows)
            if counter[pack.pack_readme] == 0:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-COLLECTION-MISSING",
                        pack.collection_readme,
                        collection_profile,
                        f"one Current pack row for {pack.pack_readme.as_posix()}",
                        "declared Current row is missing",
                    )
                )
            for target in sorted(
                set(current_rows) - {pack.pack_readme}, key=lambda item: item.as_posix()
            ):
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-COLLECTION-STALE",
                        pack.collection_readme,
                        collection_profile,
                        f"Current pack target={pack.pack_readme.as_posix()}",
                        f"Current pack target={target.as_posix()}",
                    )
                )
            for target, count in sorted(
                counter.items(), key=lambda item: item[0].as_posix()
            ):
                if count > 1 or len(current_rows) > 1:
                    diagnostics.append(
                        _diag(
                            "REFERENCE-PACK-COLLECTION-DUPLICATE",
                            pack.collection_readme,
                            collection_profile,
                            "one visible Current pack row",
                            f"target={target.as_posix()}; total={len(current_rows)}; count={count}",
                        )
                    )

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
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-OWNER-UNDECLARED",
                    path,
                    context.profiles[path].profile_id,
                    f"member declared in Current pack {pack.id}",
                    "tracked direct member is undeclared",
                )
            )
        for path in declared_order:
            profile = context.profiles.get(path)
            if (
                profile is None
                or profile.profile_id != context.reference_current_packs.profile_id
                or profile.mode != "authored"
            ):
                diagnostics.append(
                    _diag(
                        "REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",
                        path,
                        profile.profile_id
                        if profile
                        else context.reference_current_packs.profile_id,
                        f"authored {context.reference_current_packs.profile_id}",
                        "declared member is missing or has the wrong profile",
                    )
                )
                continue
            status = str(context.metadata[path].get("status", "")).casefold()
            if status not in pack.allowed_states:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-OWNER-STATUS",
                        path,
                        profile.profile_id,
                        f"status in {list(pack.allowed_states)!r}",
                        status or "missing",
                    )
                )

        rows = _reference_pack_rows(context, pack.pack_readme)
        pack_profile = context.profiles[pack.pack_readme].profile_id
        if rows is None:
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-INDEX-MISSING",
                    pack.pack_readme,
                    pack_profile,
                    "one exact Report Index with one Lifecycle column",
                    "heading or table is missing or malformed",
                )
            )
            continue
        row_paths = [path for path, _ in rows]
        row_counter = collections.Counter(row_paths)
        for path in declared_order:
            if row_counter[path] == 0:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-INDEX-MISSING",
                        pack.pack_readme,
                        pack_profile,
                        f"one row for {path.as_posix()}",
                        "declared member row is missing",
                    )
                )
        for path in sorted(set(row_paths) - declared, key=lambda item: item.as_posix()):
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-INDEX-STALE",
                    pack.pack_readme,
                    pack_profile,
                    "registry-declared direct sibling",
                    f"stale row for {path.as_posix()}",
                )
            )
        for path, count in sorted(
            row_counter.items(), key=lambda item: item[0].as_posix()
        ):
            if count > 1:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-INDEX-DUPLICATE",
                        pack.pack_readme,
                        pack_profile,
                        f"one row for {path.as_posix()}",
                        f"{count} rows",
                    )
                )
        for path, lifecycle in rows:
            if path not in declared:
                continue
            expected_status = str(
                context.metadata.get(path, {}).get("status", "")
            ).casefold()
            if lifecycle != expected_status:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-INDEX-STATUS",
                        pack.pack_readme,
                        pack_profile,
                        f"{path.as_posix()} lifecycle={expected_status}",
                        f"lifecycle={lifecycle or 'malformed'}",
                    )
                )
        if (
            len(row_paths) == len(declared_order)
            and collections.Counter(row_paths) == collections.Counter(declared_order)
            and row_paths != declared_order
        ):
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-INDEX-ORDER",
                    pack.pack_readme,
                    pack_profile,
                    "member rows in registry order",
                    "member row order differs",
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
        return [
            _diag(
                "LEDGER-MISSING",
                LEDGER_PATH,
                "content/reference",
                expected_literal,
                DEBT_LITERAL["actual"],
            )
        ]
    columns, rows = _ledger_rows(context.texts[LEDGER_PATH])
    if columns != LEDGER_COLUMNS:
        return [
            _diag(
                "LEDGER-INCOMPLETE",
                LEDGER_PATH,
                "content/reference",
                "exact ordered fourteen columns",
                "ledger columns differ",
            )
        ]
    diagnostics: list[Diagnostic] = []
    ledger_paths: list[str] = []
    for row in rows:
        if len(row) != 14:
            diagnostics.append(
                _diag(
                    "LEDGER-INCOMPLETE",
                    LEDGER_PATH,
                    "content/reference",
                    "fourteen cells per row",
                    f"{len(row)} cells",
                )
            )
            continue
        raw_path = row[0]
        if not (raw_path.startswith("`") and raw_path.endswith("`")):
            diagnostics.append(
                _diag(
                    "LEDGER-INCOMPLETE",
                    LEDGER_PATH,
                    "content/reference",
                    "backtick repository path",
                    "path cell format",
                )
            )
            continue
        ledger_paths.append(raw_path[1:-1])
        required_indexes = [index for index in range(14) if index != 3]
        if any(not row[index] for index in required_indexes):
            diagnostics.append(
                _diag(
                    "LEDGER-INCOMPLETE",
                    LEDGER_PATH,
                    "content/reference",
                    "complete ledger row",
                    "empty required cell",
                )
            )
    inventory_paths = {path.as_posix() for path in context.paths}
    counter = collections.Counter(ledger_paths)
    for missing in sorted(inventory_paths - set(counter)):
        diagnostics.append(
            _diag(
                "LEDGER-MISSING",
                LEDGER_PATH,
                "content/reference",
                "one row per inventory path",
                "inventory row is missing",
            )
        )
    for unknown in sorted(set(counter) - inventory_paths):
        diagnostics.append(
            _diag(
                "LEDGER-UNKNOWN-PATH",
                LEDGER_PATH,
                "content/reference",
                "tracked inventory path",
                "unknown ledger path",
            )
        )
    if any(count > 1 for count in counter.values()):
        diagnostics.append(
            _diag(
                "LEDGER-INCOMPLETE",
                LEDGER_PATH,
                "content/reference",
                "unique path rows",
                "duplicate ledger path",
            )
        )
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


def _apply_debt(
    root: Path,
    diagnostics: Iterable[Diagnostic],
    mode: str,
    contract: Any | None = None,
) -> list[tuple[str, Diagnostic]]:
    _load_debt(root, contract, mode=mode)
    return [
        ("FAIL", diagnostic)
        for diagnostic in sorted(diagnostics, key=diagnostic_sort_key)
    ]


def _raw_diagnostics(
    context: Context,
    registry: Registry,
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
    diagnostics.extend(_program_lineage_diagnostics(context, registry.program_lineage))
    return sorted(diagnostics, key=diagnostic_sort_key)


def validate_cross_document_contracts(
    root: Path,
    mode: str,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
    include_paths: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Return deterministic raw cross-document diagnostics."""

    if mode not in {"compatibility", "strict"}:
        raise ConfigurationError("mode must be compatibility or strict")
    context = _build_context(root, include_paths=include_paths)
    _load_debt(context.root, mode=mode)
    registry = load_registry(context.root)
    profiles_by_id = {profile.profile_id: profile for profile in registry.profiles}
    return _raw_diagnostics(
        context,
        registry,
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
        documents.append(
            {
                "path": path.as_posix(),
                "profile": profile.profile_id,
                "profileClass": profile.profile_class,
                "mode": profile.mode,
                "title": str(metadata.get("title", "")),
                "status": str(metadata.get("status", "")),
                "ownerKey": owner_keys[path],
                "origin": "baseline"
                if path in context.baseline_paths
                else "program-created",
            }
        )
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


def _envelope(
    mode: str,
    counts: dict[str, int],
    documents: list[dict[str, Any]],
    rows: list[tuple[str, Diagnostic]],
) -> dict[str, Any]:
    outcome = (
        "FAIL"
        if any(value == "FAIL" for value, _ in rows)
        else ("DEFER" if rows else "PASS")
    )
    return {
        "schemaVersion": 1,
        "mode": mode,
        "outcome": outcome,
        "counts": counts,
        "documents": documents,
        "diagnostics": [
            _diagnostic_json(value, diagnostic) for value, diagnostic in rows
        ],
    }


def _text_rows(rows: list[tuple[str, Diagnostic]]) -> list[str]:
    if not rows:
        return [
            'PASS CROSS-DOCUMENT . cross-document expected="valid" actual="valid" owner="cross-document-validator"'
        ]
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
    document_keys = [
        "path",
        "profile",
        "profileClass",
        "mode",
        "title",
        "type",
        "status",
        "body",
    ]
    if any(
        not isinstance(item, dict) or list(item) != document_keys for item in documents
    ):
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
    if paths != tuple(sorted(paths, key=lambda path: path.as_posix())) or len(
        paths
    ) != len(set(paths)):
        raise ConfigurationError("fixture paths must be sorted and unique")
    collection_artifacts = tuple(
        PurePosixPath(value) for value in tree["collectionArtifacts"]
    )
    if collection_artifacts != tuple(
        sorted(collection_artifacts, key=lambda path: path.as_posix())
    ) or len(collection_artifacts) != len(set(collection_artifacts)):
        raise ConfigurationError(
            "fixture collection artifacts must be sorted and unique"
        )
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
        profile_map[path] = ProfileView(
            item["profile"], item["profileClass"], item["mode"]
        )
        if item["mode"] in {"frontmatter-free", "classification-only"}:
            texts[path] = item["body"]
        elif item["body"] != "@ledger":
            texts[path] = authored(
                item["title"], item["type"], item["status"], item["body"]
            )
    header = "| " + " | ".join(LEDGER_COLUMNS) + " |"
    alignment = "| " + " | ".join("---" for _ in LEDGER_COLUMNS) + " |"
    rows = []
    for path in paths:
        cells = [
            f"`{path.as_posix()}`",
            "Fixture",
            profile_map[path].profile_id,
            "",
            "preserve",
            f"`{path.as_posix()}`",
            "fixture",
            "not applicable",
            "2026-07-12",
            "repository-specific",
            "retain",
            "contract change",
            "platform",
            "reviewed",
        ]
        rows.append("| " + " | ".join(cells) + " |")
    ledger_item = next(
        (item for item in documents if item["path"] == LEDGER_PATH.as_posix()), None
    )
    if ledger_item is None or ledger_item["body"] != "@ledger":
        raise ConfigurationError("fixture ledger marker differs")
    texts[LEDGER_PATH] = authored(
        ledger_item["title"],
        ledger_item["type"],
        ledger_item["status"],
        "\n".join((header, alignment, *rows)),
    )
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
        normalized = posixpath.normpath(
            posixpath.join(adapter_path.parent.as_posix(), adapter["target"])
        )
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


def _program_lineage_fixture_context(
    root: Path, tree: dict[str, Any]
) -> tuple[Context, tuple[ProgramLineage, ...]]:
    """Build an isolated typed lineage tree without loading production data."""

    if list(tree) != ["documents", "programs"]:
        raise ConfigurationError("program-lineage fixture tree keys differ")
    documents = tree["documents"]
    expected_document_keys = ["path", "profile", "status", "body"]
    if not isinstance(documents, list) or any(
        not isinstance(item, dict) or list(item) != expected_document_keys
        for item in documents
    ):
        raise ConfigurationError("program-lineage fixture document keys differ")
    paths = tuple(PurePosixPath(item["path"]) for item in documents)
    if paths != tuple(sorted(paths, key=lambda item: item.as_posix())) or len(
        paths
    ) != len(set(paths)):
        raise ConfigurationError(
            "program-lineage fixture paths must be sorted and unique"
        )
    profiles: dict[PurePosixPath, ProfileView] = {}
    texts: dict[PurePosixPath, str] = {}
    metadata: dict[PurePosixPath, dict[str, Any]] = {}
    for item, path in zip(documents, paths, strict=True):
        profile_id = item["profile"]
        profile_class = (
            "sdlc"
            if profile_id.startswith("sdlc/")
            else "governance"
            if profile_id.startswith("governance/")
            else "common"
        )
        profiles[path] = ProfileView(profile_id, profile_class, "authored")
        texts[path] = item["body"]
        metadata[path] = {
            "title": f"Fixture {path.stem}",
            "type": profile_id,
            "status": item["status"],
            "owner": "platform",
            "updated": "2026-07-15",
        }

    raw_programs = tree["programs"]
    if not isinstance(raw_programs, list):
        raise ConfigurationError("program-lineage fixture programs must be a list")
    programs: list[ProgramLineage] = []
    for raw_program in raw_programs:
        if not isinstance(raw_program, dict) or list(raw_program) != [
            "prd",
            "ard",
            "tranches",
            "followUps",
        ]:
            raise ConfigurationError("program-lineage fixture program keys differ")
        tranches = tuple(
            ProgramRelation(
                spec_id=item["spec"],
                order=item["order"],
                state=item["state"],
                reason=item["reason"],
                decision_id=item["decision"],
            )
            for item in raw_program["tranches"]
        )
        follow_ups = tuple(
            ProgramFollowUp(
                spec_id=item["spec"],
                order=item["order"],
                state=item["state"],
                reason=item["reason"],
                decision_id=item["decision"],
                evidence_mode=item["evidenceMode"],
            )
            for item in raw_program["followUps"]
        )
        programs.append(
            ProgramLineage(
                prd_id=raw_program["prd"],
                ard_id=raw_program["ard"],
                tranches=tranches,
                follow_ups=follow_ups,
            )
        )
    context = Context(
        root,
        paths,
        frozenset(),
        profiles,
        texts,
        metadata,
        {},
        (),
        (),
        ReferenceCurrentPacks("content/reference", ()),
        frozenset(paths),
    )
    return context, tuple(programs)


def _mutated_program_lineage_fixture(
    context: Context,
    programs: tuple[ProgramLineage, ...],
    mutation: str,
) -> tuple[Context, tuple[ProgramLineage, ...]]:
    mutated = copy.deepcopy(context)
    paths = mutated.paths
    tracked_regular_paths = mutated.tracked_regular_paths
    plan_034 = PurePosixPath("docs/04.execution/plans/2026-07-15-fixture-034.md")
    task_034 = PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-034.md")

    def remove_execution_path(path: PurePosixPath) -> None:
        nonlocal paths, tracked_regular_paths
        paths = tuple(item for item in paths if item != path)
        tracked_regular_paths = frozenset(
            item for item in tracked_regular_paths if item != path
        )
        mutated.profiles.pop(path)
        mutated.metadata.pop(path)
        mutated.texts.pop(path)

    def add_execution_pair(suffix: str, spec_id: str) -> None:
        plan = PurePosixPath(f"docs/04.execution/plans/2026-07-15-fixture-{suffix}.md")
        task = PurePosixPath(f"docs/04.execution/tasks/2026-07-15-fixture-{suffix}.md")

        add_execution_node(
            plan,
            "sdlc/plan",
            f"[Spec](../../03.specs/{spec_id}-fixture/spec.md)\n"
            f"[Task](../tasks/2026-07-15-fixture-{suffix}.md)",
        )
        add_execution_node(
            task,
            "sdlc/task",
            f"[Spec](../../03.specs/{spec_id}-fixture/spec.md)\n"
            f"[Plan](../plans/2026-07-15-fixture-{suffix}.md)",
        )

    def add_execution_node(path: PurePosixPath, profile_id: str, body: str) -> None:
        nonlocal paths, tracked_regular_paths
        paths = tuple(sorted((*paths, path), key=lambda item: item.as_posix()))
        tracked_regular_paths = frozenset((*tracked_regular_paths, path))
        mutated.profiles[path] = ProfileView(profile_id, "sdlc", "authored")
        mutated.metadata[path] = {"type": profile_id, "status": "active"}
        mutated.texts[path] = body

    def close_original_034() -> None:
        nonlocal programs
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.metadata[spec]["status"] = "done"
        mutated.texts[spec] = mutated.texts[spec].replace(
            "\n[Plan](../../04.execution/plans/2026-07-15-fixture-034.md)",
            "",
        )
        remove_execution_path(plan_034)
        remove_execution_path(task_034)
        program = programs[1]
        first = program.tranches[0]
        closed = ProgramRelation(
            spec_id=first.spec_id,
            order=first.order,
            state="done",
            reason=first.reason,
            decision_id=first.decision_id,
        )
        programs = (
            programs[0],
            ProgramLineage(
                prd_id=program.prd_id,
                ard_id=program.ard_id,
                tranches=(closed, *program.tranches[1:]),
                follow_ups=program.follow_ups,
            ),
            *programs[2:],
        )

    def add_original_036() -> None:
        nonlocal programs
        spec = PurePosixPath("docs/03.specs/036-fixture/spec.md")
        add_execution_node(
            spec,
            "sdlc/spec",
            "[PRD](../../01.requirements/006-fixture.md)\n"
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
        )
        prd = PurePosixPath("docs/01.requirements/006-fixture.md")
        ard = PurePosixPath("docs/02.architecture/requirements/0009-fixture.md")
        mutated.texts[prd] += "\n[Spec 036](../03.specs/036-fixture/spec.md)"
        mutated.texts[ard] += "\n[Spec 036](../../03.specs/036-fixture/spec.md)"
        program = programs[1]
        programs = (
            programs[0],
            ProgramLineage(
                prd_id=program.prd_id,
                ard_id=program.ard_id,
                tranches=(
                    *program.tranches,
                    ProgramRelation(
                        spec_id="036",
                        order=3,
                        state="active",
                        reason="Premature successor",
                        decision_id="0017",
                    ),
                ),
                follow_ups=program.follow_ups,
            ),
            *programs[2:],
        )

    def rename_document_path(source: PurePosixPath, target: PurePosixPath) -> None:
        nonlocal paths, tracked_regular_paths
        paths = tuple(
            sorted(
                (target if path == source else path for path in paths),
                key=lambda item: item.as_posix(),
            )
        )
        tracked_regular_paths = frozenset(
            target if path == source else path for path in tracked_regular_paths
        )
        mutated.profiles[target] = mutated.profiles.pop(source)
        mutated.metadata[target] = mutated.metadata.pop(source)
        mutated.texts[target] = mutated.texts.pop(source)

    if mutation in {"none", "program-execution-follow-up-absence"}:
        return mutated, programs
    if mutation == "program-state":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.metadata[spec]["status"] = "done"
    elif mutation == "program-reciprocal":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)\n",
            "",
        )
        mutated.texts[spec] += "\n`../../02.architecture/requirements/0009-fixture.md`"
    elif mutation == "program-reciprocal-unicode-space-inline":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD](../../02.architecture/requirements/0009-fixture.md\u00a0)",
        )
    elif mutation == "program-execution-unicode-space-reference":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Spec](../../03.specs/034-fixture/spec.md)",
            "[Spec][owner]\n\n[owner]: ../../03.specs/034-fixture/spec.md\u2003",
        )
    elif mutation == "program-reciprocal-balanced-escaped":
        old_ard = PurePosixPath("docs/02.architecture/requirements/0009-fixture.md")
        new_ard = PurePosixPath(
            "docs/02.architecture/requirements/0009-fixture-(owner).md"
        )
        rename_document_path(old_ard, new_ard)
        prd = PurePosixPath("docs/01.requirements/006-fixture.md")
        spec_034 = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        spec_035 = PurePosixPath("docs/03.specs/035-fixture/spec.md")
        mutated.texts[prd] = mutated.texts[prd].replace(
            "0009-fixture.md", "0009-fixture-(owner).md"
        )
        mutated.texts[spec_034] = mutated.texts[spec_034].replace(
            "0009-fixture.md", "0009-fixture-(owner).md"
        )
        mutated.texts[spec_035] = mutated.texts[spec_035].replace(
            "0009-fixture.md", r"0009-fixture-\(owner\).md"
        )
    elif mutation == "program-reciprocal-cross-container":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD\n> owner](../../02.architecture/requirements/0009-fixture.md)",
        )
    elif mutation == "program-reciprocal-cross-container-reference":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD][owner\n> key]\n\n"
            "[owner key]: ../../02.architecture/requirements/0009-fixture.md",
        )
    elif mutation == "program-reciprocal-outer-fence-nested":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "> ~~~markdown\n"
            "> > [ARD](../../02.architecture/requirements/0009-fixture.md)\n"
            "> ~~~",
        )
    elif mutation in {
        "program-reciprocal-invalid-reference-garbage",
        "program-reciprocal-valid-reference-title",
    }:
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        suffix = (
            " garbage"
            if mutation == "program-reciprocal-invalid-reference-garbage"
            else ' "owner"'
        )
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD][owner]\n\n"
            "[owner]: ../../02.architecture/requirements/0009-fixture.md" + suffix,
        )
    elif mutation == "program-reciprocal-valid-double-title":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            '[ARD](../../02.architecture/requirements/0009-fixture.md "owner")',
        )
    elif mutation in {
        "program-reciprocal-invalid-reference-angle-less-than",
        "program-reciprocal-valid-reference-angle-escaped-less-than",
    }:
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        fragment = (
            "#<owner"
            if mutation == "program-reciprocal-invalid-reference-angle-less-than"
            else r"#\<owner"
        )
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD][owner]\n\n"
            "[owner]: "
            "<../../02.architecture/requirements/0009-fixture.md"
            f"{fragment}>",
        )
    elif mutation == "program-reciprocal-valid-double-title-closing-paren":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD](../../02.architecture/requirements/0009-fixture.md "
            '"owner ) current")',
        )
    elif mutation == "program-reciprocal-list-marker-boundary":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD\n- owner](../../02.architecture/requirements/0009-fixture.md)",
        )
    elif mutation == "program-reciprocal-bare-nonpunctuation-escape":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            r"[ARD](../../02.architecture/requirements/00\09-fixture.md)",
        )
    elif mutation == "program-reciprocal-reference-nonpunctuation-escape":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[ARD][owner]\n\n"
            r"[owner]: ../../02.architecture/requirements/00\09-fixture.md",
        )
    elif mutation == "program-reciprocal-nested-link":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[outer [inner](./unrelated.md)]"
            "(../../02.architecture/requirements/0009-fixture.md)",
        )
    elif mutation == "program-reciprocal-adjacent-references":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[Other][other][ARD]\n\n"
            "[other]: ./unrelated.md\n"
            "[ARD]: ../../02.architecture/requirements/0009-fixture.md",
        )
    elif mutation == "program-reciprocal-image-alt-subtree":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "![owner [ARD]"
            "(../../02.architecture/requirements/0009-fixture.md)]"
            "(./owner.png)",
        )
    elif mutation == "program-reciprocal-unresolved-before-inline":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[literal][ARD](../../02.architecture/requirements/0009-fixture.md)",
        )
    elif mutation == "program-reciprocal-unresolved-before-full-reference":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "[literal][ARD][owner]\n\n"
            "[owner]: ../../02.architecture/requirements/0009-fixture.md",
        )
    elif mutation == "program-reciprocal-escaped-literal-before-shortcut":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "\\[literal][ARD]\n\n"
            "[ARD]: ../../02.architecture/requirements/0009-fixture.md",
        )
    elif mutation == "program-reciprocal-unresolved-image-inline":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "![literal [ARD](../../02.architecture/requirements/0009-fixture.md)]",
        )
    elif mutation == "program-reciprocal-unresolved-image-full-reference":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "![literal [ARD][owner]]\n\n"
            "[owner]: ../../02.architecture/requirements/0009-fixture.md",
        )
    elif mutation in {
        "program-reciprocal-link-destination-span",
        "program-reciprocal-link-title-span",
        "program-reciprocal-image-title-span",
    }:
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        evidence = {
            "program-reciprocal-link-destination-span": (
                "[Other](<./unrelated.md#[ARD]>)"
            ),
            "program-reciprocal-link-title-span": ('[Other](./unrelated.md "[ARD]")'),
            "program-reciprocal-image-title-span": ('![Other](./owner.png "[ARD]")'),
        }[mutation]
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            evidence
            + "\n\n"
            + "[ARD]: ../../02.architecture/requirements/0009-fixture.md",
        )
    elif mutation in {
        "program-reciprocal-definition-title-span",
        "program-reciprocal-multiline-single-title",
        "program-reciprocal-escaped-paren-title",
        "program-reciprocal-nested-paren-title",
        "program-reciprocal-blank-definition-continuation",
        "program-reciprocal-unclosed-definition-title",
        "program-reciprocal-space-remainder-valid-title-span",
        "program-reciprocal-tab-remainder-valid-title-span",
        "program-reciprocal-space-remainder-nested-paren-title",
        "program-reciprocal-tab-remainder-unclosed-title",
        "program-reciprocal-next-line-title-trailing-garbage",
        "program-reciprocal-invalid-next-line-title-phantom",
        "program-reciprocal-continued-destination-invalid-title",
        "program-reciprocal-definition-before-thematic",
        "program-reciprocal-setext-destination-first-wins",
        "program-reciprocal-paragraph-definition-setext",
        "program-reciprocal-html-numeric-destination",
        "program-reciprocal-html-backslash-destination",
        "program-reciprocal-quote-lazy-setext-definition",
        "program-reciprocal-inline-html-attribute",
        "program-reciprocal-markdown-inside-inline-html",
        "program-reciprocal-inline-html-definition-lookalike",
        "program-reciprocal-type7-html-quoted-greater",
        "program-reciprocal-inline-html-shortcut-collision",
        "program-reciprocal-inline-html-shortcut-identical",
        "program-reciprocal-inline-html-label-999",
        "program-reciprocal-inline-html-label-1000",
        "program-reciprocal-comment-block-trailing",
        "program-reciprocal-invalid-inline-comment",
        "program-reciprocal-inline-html-blank-boundary",
        "program-reciprocal-multiline-definition-label",
        "program-reciprocal-inline-backtick-suffix",
        "program-reciprocal-quote-comment-leaf",
        "program-reciprocal-root-declaration-leaf",
        "program-reciprocal-escaped-definition-label-close",
        "program-reciprocal-destination-continuation-zero",
        "program-reciprocal-destination-continuation-four",
        "program-reciprocal-destination-continuation-tab",
        "program-reciprocal-title-continuation-zero",
        "program-reciprocal-title-continuation-four",
        "program-reciprocal-title-continuation-tab",
        "program-reciprocal-title-continuation-multiline",
        "program-reciprocal-invalid-blank-title-rendered",
        "program-reciprocal-complete-definition-four-space-code",
        "program-reciprocal-definition-paragraph-interruption",
        "program-reciprocal-definition-blank-boundary",
        "program-reciprocal-definition-heading-boundary",
        "program-reciprocal-failed-inline-shortcut-fallback",
        "program-reciprocal-ordered-123-tilde-fence",
        "program-reciprocal-unordered-indented-code",
        "program-reciprocal-unordered-empty-four-code",
        "program-reciprocal-ordered-empty-five-code",
        "program-reciprocal-unordered-tab-code",
        "program-reciprocal-list-lazy-continuation",
        "program-reciprocal-list-sibling-boundary",
        "program-reciprocal-whitespace-shortcut-label",
        "program-reciprocal-normal-spaced-label",
        "program-reciprocal-setext-indented-code",
        "program-reciprocal-standalone-setext-equals-indented-continuation",
        "program-reciprocal-definition-standalone-equals-indented-continuation",
        "program-reciprocal-quote-lazy-hyphen-indented-continuation",
        "program-reciprocal-quote-definition-indented-code",
        "program-reciprocal-invalid-quote-definition-indented-lazy",
        "program-reciprocal-multiline-quote-definition-indented-code",
        "program-reciprocal-multiline-list-definition-indented-code",
        "program-reciprocal-explicit-quote-setext-indented-code",
        "program-reciprocal-thematic-definition-indented-code",
        "program-reciprocal-list-atx-definition-indented-code",
        "program-reciprocal-shortcut-label-999",
        "program-reciprocal-full-label-1000",
        "program-reciprocal-failed-inline-label-999",
        "program-reciprocal-escaped-label-1000",
        "program-reciprocal-code-label-closing-bracket",
        "program-reciprocal-code-label-mixed-run",
        "program-reciprocal-raw-pua-html-collision",
        "program-reciprocal-inline-html-tag-casefold",
        "program-reciprocal-orphan-inline-suffix-backtick",
        "program-reciprocal-code-closing-backslash",
    }:
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        target = "../../02.architecture/requirements/0009-fixture.md"
        raw_pua_html_identity = (
            str(_mask_inline_html_tokens("<i>"))
            + "ARD"
            + str(_mask_inline_html_tokens("</i>"))
        )
        evidence = {
            "program-reciprocal-definition-title-span": (
                f'[Other][owner]\n\n[owner]: ./unrelated.md "[ARD]"\n[ARD]: {target}'
            ),
            "program-reciprocal-multiline-single-title": (
                f"[ARD][owner]\n\n[owner]:\n  {target}\n  'owner'"
            ),
            "program-reciprocal-escaped-paren-title": (
                f"[ARD][owner]\n\n[owner]: {target} (\\(owner)"
            ),
            "program-reciprocal-nested-paren-title": (
                f"[ARD][owner]\n\n[owner]: {target} ((nested)"
            ),
            "program-reciprocal-blank-definition-continuation": (
                f"[ARD][owner]\n\n[owner]:\n\n  {target}"
            ),
            "program-reciprocal-unclosed-definition-title": (
                f'[ARD][owner]\n\n[owner]: {target} "owner'
            ),
            "program-reciprocal-space-remainder-valid-title-span": (
                "[Other][owner]\n\n"
                "[owner]: ./unrelated.md   \n"
                '  "[ARD]"\n'
                f"[ARD]: {target}"
            ),
            "program-reciprocal-tab-remainder-valid-title-span": (
                "[Other][owner]\n\n"
                "[owner]: ./unrelated.md\t\n"
                "  '[ARD]'\n"
                f"[ARD]: {target}"
            ),
            "program-reciprocal-space-remainder-nested-paren-title": (
                f"[ARD][owner]\n\n[owner]: {target}   \n  ((nested)"
            ),
            "program-reciprocal-tab-remainder-unclosed-title": (
                f'[ARD][owner]\n\n[owner]: {target}\t\n  "owner'
            ),
            "program-reciprocal-next-line-title-trailing-garbage": (
                f'[ARD][owner]\n\n[owner]: {target}\n  "owner" garbage'
            ),
            "program-reciprocal-invalid-next-line-title-phantom": (
                "[Other][owner]\n\n"
                "[owner]: ./unrelated.md\n"
                f'  "[ARD]({target})" garbage'
            ),
            "program-reciprocal-continued-destination-invalid-title": (
                f'[ARD][owner]\n\n[owner]:\n    {target}\n    "owner" garbage'
            ),
            "program-reciprocal-definition-before-thematic": (
                f"[ARD][owner]\n\n[owner]:\n{target}\n---"
            ),
            "program-reciprocal-setext-destination-first-wins": (
                f"[ARD][owner]\n\n[owner]:\n===\n[owner]: {target}"
            ),
            "program-reciprocal-paragraph-definition-setext": (
                f"Ordinary paragraph\n[owner]: {target}\n---\n[ARD][owner]"
            ),
            "program-reciprocal-html-numeric-destination": (
                "[ARD](../../02.architecture/requirements/0009&#45;fixture.md)"
            ),
            "program-reciprocal-html-backslash-destination": (
                "[ARD](../../02.architecture/requirements/"
                r"0009\&#45;fixture.md)"
            ),
            "program-reciprocal-quote-lazy-setext-definition": (
                f"> paragraph\n===\n> [owner]: {target}\n> [ARD][owner]"
            ),
            "program-reciprocal-inline-html-attribute": (
                f'<span title="[ARD]({target})">ok</span>'
            ),
            "program-reciprocal-markdown-inside-inline-html": (
                f"<span>[ARD]({target})</span>"
            ),
            "program-reciprocal-inline-html-definition-lookalike": (
                f"[ARD][owner]\n\n<b>[owner]: {target}"
            ),
            "program-reciprocal-type7-html-quoted-greater": (
                f'\n<x title=">">\n[ARD]({target})'
            ),
            "program-reciprocal-inline-html-shortcut-collision": (
                f"[<i>ARD</i>]\n\n[<b>ARD</b>]: {target}"
            ),
            "program-reciprocal-inline-html-shortcut-identical": (
                f"[<i>ARD</i>]\n\n[<i>ARD</i>]: {target}"
            ),
            "program-reciprocal-inline-html-label-999": (
                f"[<i>{'x' * 992}</i>]\n\n[<i>{'x' * 992}</i>]: {target}"
            ),
            "program-reciprocal-inline-html-label-1000": (
                f"[<i>{'x' * 993}</i>]\n\n[<i>{'x' * 993}</i>]: {target}"
            ),
            "program-reciprocal-comment-block-trailing": (
                f"\n<!-- owner evidence --> [ARD]({target})"
            ),
            "program-reciprocal-invalid-inline-comment": (
                f"before <!-- invalid -- [ARD]({target}) --> after"
            ),
            "program-reciprocal-inline-html-blank-boundary": (
                f'<span\n\n title="[ARD]({target})">ok</span>'
            ),
            "program-reciprocal-multiline-definition-label": (
                f"[ARD][owner key]\n\n[owner\nkey]: {target}"
            ),
            "program-reciprocal-inline-backtick-suffix": (f"[ARD]({target} `suffix`)"),
            "program-reciprocal-quote-comment-leaf": (
                f"> paragraph\n> <!-- owner -->\n    [ARD]({target})"
            ),
            "program-reciprocal-root-declaration-leaf": (
                f"paragraph\n<!A owner>\n    [ARD]({target})"
            ),
            "program-reciprocal-escaped-definition-label-close": (
                f"[ARD][owner\\]]\n\n[owner\\]]: {target}"
            ),
            "program-reciprocal-destination-continuation-zero": (
                f"[ARD][owner]\n\n[owner]:\n{target}"
            ),
            "program-reciprocal-destination-continuation-four": (
                f"[ARD][owner]\n\n[owner]:\n    {target}"
            ),
            "program-reciprocal-destination-continuation-tab": (
                f"[ARD][owner]\n\n[owner]:\n\t{target}"
            ),
            "program-reciprocal-title-continuation-zero": (
                f'[Other][owner]\n\n[owner]: ./unrelated.md\n"[ARD]({target})"'
            ),
            "program-reciprocal-title-continuation-four": (
                f'[Other][owner]\n\n[owner]: ./unrelated.md\n    "[ARD]({target})"'
            ),
            "program-reciprocal-title-continuation-tab": (
                f'[Other][owner]\n\n[owner]: ./unrelated.md\n\t"[ARD]({target})"'
            ),
            "program-reciprocal-title-continuation-multiline": (
                "[Other][owner]\n\n"
                '[owner]: ./unrelated.md "first line\n'
                f"[ARD]({target})\n"
                'last line"'
            ),
            "program-reciprocal-invalid-blank-title-rendered": (
                "[Other][owner]\n\n"
                '[owner]: ./unrelated.md "first line\n\n'
                f"[ARD]({target})\n"
                'last line"'
            ),
            "program-reciprocal-complete-definition-four-space-code": (
                f"[Other][owner]\n\n[owner]: ./unrelated.md\n    [ARD]({target})"
            ),
            "program-reciprocal-definition-paragraph-interruption": (
                f"[ARD][owner]\n\nOrdinary paragraph continuation\n[owner]: {target}"
            ),
            "program-reciprocal-definition-blank-boundary": (
                f"[ARD][owner]\n\nCompleted paragraph.\n\n[owner]: {target}"
            ),
            "program-reciprocal-definition-heading-boundary": (
                f"[ARD][owner]\n\n# Reference definitions\n[owner]: {target}"
            ),
            "program-reciprocal-failed-inline-shortcut-fallback": (
                f"[ARD](not a link)\n\n[ARD]: {target}"
            ),
            "program-reciprocal-ordered-123-tilde-fence": (
                f"123. fenced block\n     ~~~markdown\n     [ARD]({target})\n     ~~~"
            ),
            "program-reciprocal-unordered-indented-code": (f"-\n      [ARD]({target})"),
            "program-reciprocal-unordered-empty-four-code": (
                f"-    \n      [ARD]({target})"
            ),
            "program-reciprocal-ordered-empty-five-code": (
                f"1.     \n       [ARD]({target})"
            ),
            "program-reciprocal-unordered-tab-code": (f"-\t    [ARD]({target})"),
            "program-reciprocal-list-lazy-continuation": (f"- [ARD\n]({target})"),
            "program-reciprocal-list-sibling-boundary": (f"- [ARD\n- ]({target})"),
            "program-reciprocal-whitespace-shortcut-label": (f"[ ]\n\n[ ]: {target}"),
            "program-reciprocal-normal-spaced-label": (
                f"[ARD][ owner key ]\n\n[owner   key]: {target}"
            ),
            "program-reciprocal-setext-indented-code": (
                f"Reference evidence\n---\n    [ARD]({target})"
            ),
            "program-reciprocal-standalone-setext-equals-indented-continuation": (
                f"\n===\n    [ARD]({target})"
            ),
            "program-reciprocal-definition-standalone-equals-indented-continuation": (
                f"\n[r]: /u\n===\n    [ARD]({target})"
            ),
            "program-reciprocal-quote-lazy-hyphen-indented-continuation": (
                f"> paragraph\n--\n    [ARD]({target})"
            ),
            "program-reciprocal-quote-definition-indented-code": (
                f"> [r]: /u\n    [ARD]({target})"
            ),
            "program-reciprocal-invalid-quote-definition-indented-lazy": (
                f"> [r]: <unterminated\n    [ARD]({target})"
            ),
            "program-reciprocal-multiline-quote-definition-indented-code": (
                f"> [r]:\n /u\n    [ARD]({target})"
            ),
            "program-reciprocal-multiline-list-definition-indented-code": (
                f"- [r]:\n /u\n      [ARD]({target})"
            ),
            "program-reciprocal-explicit-quote-setext-indented-code": (
                f"> paragraph\n> ===\n    [ARD]({target})"
            ),
            "program-reciprocal-thematic-definition-indented-code": (
                f"***\n[r]: /u\n    [ARD]({target})"
            ),
            "program-reciprocal-list-atx-definition-indented-code": (
                f"- # Heading\n  [r]: /u\n      [ARD]({target})"
            ),
            "program-reciprocal-shortcut-label-999": (
                f"[{'s' * 999}]\n\n[{'s' * 999}]: {target}"
            ),
            "program-reciprocal-full-label-1000": (
                f"[ARD][{'f' * 1000}]\n\n[{'f' * 1000}]: {target}"
            ),
            "program-reciprocal-failed-inline-label-999": (
                f"[{'i' * 999}](not a link)\n\n[{'i' * 999}]: {target}"
            ),
            "program-reciprocal-escaped-label-1000": (
                f"[ARD][{r'\*' * 500}]\n\n[{r'\*' * 500}]: {target}"
            ),
            "program-reciprocal-code-label-closing-bracket": (f"[ARD `]`]({target})"),
            "program-reciprocal-code-label-mixed-run": (
                f"[ARD ``code `]` still``]({target})"
            ),
            "program-reciprocal-raw-pua-html-collision": (
                f"[<i>ARD</i>]\n\n[{raw_pua_html_identity}]: {target}"
            ),
            "program-reciprocal-inline-html-tag-casefold": (
                f"[<I>ARD</I>]\n\n[<i>ard</i>]: {target}"
            ),
            "program-reciprocal-orphan-inline-suffix-backtick": (
                f"orphan](`[ARD]({target})`)"
            ),
            "program-reciprocal-code-closing-backslash": ("`[ARD](" + target + ")\\`"),
        }[mutation]
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            evidence,
        )
    elif mutation == "program-reciprocal-code-paragraph-recovery":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "[ARD](../../02.architecture/requirements/0009-fixture.md)",
            "`unmatched\n\n[ARD](../../02.architecture/requirements/0009-fixture.md)`",
        )
    elif mutation == "program-historical-exception":
        roadmap = PurePosixPath(
            "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md"
        )
        mutated.texts[roadmap] = mutated.texts[roadmap].replace(
            "[Spec\n033](../../../03.specs/033-fixture/spec.md)",
            "Spec 033",
        )
        mutated.texts[roadmap] += "\n`../../../03.specs/033-fixture/spec.md`"
    elif mutation in {
        "program-historical-paragraph-break",
        "program-historical-raw-html",
        "program-historical-indented-code",
        "program-historical-heading-indented-code",
        "program-historical-paragraph-continuation",
        "program-historical-blockquote-raw-html",
        "program-historical-blockquote-tilde-fence",
        "program-historical-blockquote-indented-code",
        "program-historical-raw-html-heading",
        "program-historical-root-to-quote",
        "program-historical-quote-to-root",
        "program-historical-quote-depth-transition",
        "program-historical-quote-depth-return",
        "program-historical-sibling-quotes",
        "program-historical-same-quote-soft-break",
        "program-historical-reference-root-to-quote",
        "program-historical-reference-quote-to-root",
        "program-historical-reference-quote-depth",
        "program-historical-reference-same-quote",
        "program-historical-outer-raw-nested",
        "program-historical-nested-indented",
        "program-historical-valid-angle-destination",
        "program-historical-valid-angle-parentheses",
        "program-historical-invalid-unmatched-angle",
        "program-historical-atx-boundary",
        "program-historical-setext-boundary",
        "program-historical-thematic-boundary",
        "program-historical-table-cell-boundary",
        "program-historical-angle-nonpunctuation-escape",
        "program-historical-image-only",
        "program-historical-image-in-link",
        "program-historical-unresolved-before-collapsed",
        "program-historical-multiline-double-title",
        "program-historical-valid-single-title",
        "program-historical-code-paragraph-recovery",
        "program-historical-code-container-recovery",
        "program-historical-code-soft-break",
        "program-historical-ordered-1-normal-paragraph",
        "program-historical-nested-list-raw-html",
        "program-historical-ordered-empty-two-code",
        "program-historical-unordered-four-content",
        "program-historical-unordered-five-content",
        "program-historical-unordered-tab-content",
        "program-historical-ordered-tab-content",
        "program-historical-blockquote-lazy-continuation",
        "program-historical-tab-only-label",
        "program-historical-soft-break-whitespace-label",
        "program-historical-setext-indented-code",
        "program-historical-thematic-indented-code",
        "program-historical-standalone-setext-hyphen-indented-continuation",
        "program-historical-standalone-thematic-hyphen-indented-code",
        "program-historical-definition-indented-code",
        "program-historical-list-second-paragraph",
        "program-historical-quote-definition-indented-code",
        "program-historical-quote-paragraph-indented-lazy",
        "program-historical-multiline-quote-definition-indented-code",
        "program-historical-invalid-multiline-quote-definition-indented-lazy",
        "program-historical-explicit-quote-setext-indented-code",
        "program-historical-explicit-normal-quote-indented-lazy",
        "program-historical-atx-definition-indented-code",
        "program-historical-quote-atx-definition-indented-code",
        "program-historical-paragraph-definition-lookalike-indented-continuation",
        "program-historical-shortcut-label-1000",
        "program-historical-collapsed-label-999",
        "program-historical-failed-inline-label-1000",
        "program-historical-soft-line-label-999",
        "program-historical-definition-before-thematic",
        "program-historical-setext-destination-first-wins",
        "program-historical-paragraph-definition-setext",
        "program-historical-html-named-destination",
        "program-historical-list-lazy-setext-definition",
        "program-historical-inline-html-anchor-attribute",
        "program-historical-escaped-inline-html-opener",
        "program-historical-inline-html-comment",
        "program-historical-inline-html-reference-label",
        "program-historical-invalid-type7-html-opener",
        "program-historical-inline-html-collapsed-collision",
        "program-historical-inline-html-collapsed-identical",
        "program-historical-comment-block-multiline-trailing",
        "program-historical-valid-inline-comment-trailing",
        "program-historical-escaped-multiline-definition-label",
        "program-historical-short-table-cell-boundary",
        "program-historical-definition-backtick-title",
        "program-historical-quote-processing-leaf",
        "program-historical-code-span-fake-link",
        "program-historical-raw-pua-identical",
        "program-historical-inline-html-casefold-distinct-tag",
        "program-historical-double-backslash-code-span",
        "program-historical-orphan-inline-suffix-backtick",
    }:
        roadmap = PurePosixPath(
            "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md"
        )
        heading = "### 2026-07-15 template lifecycle disposition overlay"
        target = "../../../03.specs/033-fixture/spec.md"
        evidence = {
            "program-historical-paragraph-break": (f"[Spec\n   \n033]({target})"),
            "program-historical-raw-html": (f"<div>\n[Spec 033]({target})\n</div>"),
            "program-historical-indented-code": (f"    [Spec 033]({target})"),
            "program-historical-heading-indented-code": (f"    [Spec 033]({target})"),
            "program-historical-paragraph-continuation": (
                f"Continuation paragraph\n    [Spec 033]({target})"
            ),
            "program-historical-blockquote-raw-html": (
                f"> <div>\n> [Spec 033]({target})\n> </div>"
            ),
            "program-historical-blockquote-tilde-fence": (
                f"> ~~~markdown\n> [Spec 033]({target})\n> ~~~"
            ),
            "program-historical-blockquote-indented-code": (
                f">     [Spec 033]({target})"
            ),
            "program-historical-raw-html-heading": (
                f"<div>\n{heading}\n[Spec 033]({target})\n</div>"
            ),
            "program-historical-root-to-quote": (f"[Spec\n> 033]({target})"),
            "program-historical-quote-to-root": (f"> [Spec\n# 033]({target})"),
            "program-historical-quote-depth-transition": (
                f"> [Spec\n> > 033]({target})"
            ),
            "program-historical-quote-depth-return": (f"> > [Spec\n> # 033]({target})"),
            "program-historical-sibling-quotes": (f"> [Spec\n\n> 033]({target})"),
            "program-historical-same-quote-soft-break": (f"> [Spec\n> 033]({target})"),
            "program-historical-reference-root-to-quote": (
                f"[Spec 033][owner\n> key]\n\n[owner key]: {target}"
            ),
            "program-historical-reference-quote-to-root": (
                f"> [Spec 033][owner\n- key]\n\n[owner - key]: {target}"
            ),
            "program-historical-reference-quote-depth": (
                f"> [Spec 033][owner\n> > key]\n\n[owner key]: {target}"
            ),
            "program-historical-reference-same-quote": (
                f"> [Spec 033][owner\n> key]\n>\n> [owner key]: {target}"
            ),
            "program-historical-outer-raw-nested": (
                f"> <div>\n> > [Spec 033]({target})\n> </div>"
            ),
            "program-historical-nested-indented": (f">     > [Spec 033]({target})"),
            "program-historical-valid-angle-destination": (f"[Spec 033](<{target}>)"),
            "program-historical-valid-angle-parentheses": (
                f"[Spec 033](<{target}#)(>)"
            ),
            "program-historical-invalid-unmatched-angle": (f"[Spec 033](<{target})"),
            "program-historical-atx-boundary": (f"[Spec\n# 033]({target})"),
            "program-historical-setext-boundary": (
                f"[Spec\nHeading\n---\n033]({target})"
            ),
            "program-historical-thematic-boundary": (f"[Spec\n***\n033]({target})"),
            "program-historical-table-cell-boundary": (
                f"Label | Target\n--- | ---\n[Spec | 033]({target})"
            ),
            "program-historical-angle-nonpunctuation-escape": (
                r"[Spec 033](<../../../03.specs/\033-fixture/spec.md>)"
            ),
            "program-historical-image-only": (f"![Spec 033]({target})"),
            "program-historical-image-in-link": (
                f"[![Spec icon](./icon.png)]({target})"
            ),
            "program-historical-unresolved-before-collapsed": (
                f"[literal][Spec 033][]\n\n[Spec 033]: {target}"
            ),
            "program-historical-multiline-double-title": (
                f'[Spec 033][owner]\n\n[owner]: {target}\n  "history"'
            ),
            "program-historical-valid-single-title": (
                f"[Spec 033]({target} 'history')"
            ),
            "program-historical-code-paragraph-recovery": (
                f"`unmatched\n\n[Spec 033]({target})`"
            ),
            "program-historical-code-container-recovery": (
                f"`unmatched\n> [Spec 033]({target})`"
            ),
            "program-historical-code-soft-break": (f"`code\n[Spec 033]({target})`"),
            "program-historical-ordered-1-normal-paragraph": (
                f"1.\n   [Spec 033]({target})"
            ),
            "program-historical-nested-list-raw-html": (
                "12. outer item\n"
                "    - inner item\n"
                "      <div>\n"
                f"      [Spec 033]({target})\n"
                "      </div>"
            ),
            "program-historical-ordered-empty-two-code": (
                f"1.  \n       [Spec 033]({target})"
            ),
            "program-historical-unordered-four-content": (f"-    [Spec 033]({target})"),
            "program-historical-unordered-five-content": (
                f"-     [Spec 033]({target})"
            ),
            "program-historical-unordered-tab-content": (f"-\t[Spec 033]({target})"),
            "program-historical-ordered-tab-content": (f"123.\t[Spec 033]({target})"),
            "program-historical-blockquote-lazy-continuation": (
                f"> [Spec 033\n]({target})"
            ),
            "program-historical-tab-only-label": (f"[Spec 033][\t]\n\n[\t]: {target}"),
            "program-historical-soft-break-whitespace-label": (
                f"[Spec 033][ \n\t]\n\n[ ]: {target}"
            ),
            "program-historical-setext-indented-code": (
                f"Historical evidence\n===\n    [Spec 033]({target})"
            ),
            "program-historical-thematic-indented-code": (
                f"***\n    [Spec 033]({target})"
            ),
            "program-historical-standalone-setext-hyphen-indented-continuation": (
                f"--\n    [Spec 033]({target})"
            ),
            "program-historical-standalone-thematic-hyphen-indented-code": (
                f"---\n    [Spec 033]({target})"
            ),
            "program-historical-definition-indented-code": (
                f"[r]: /u\n    [Spec 033]({target})"
            ),
            "program-historical-list-second-paragraph": (
                f"- paragraph\n\n    [Spec 033]({target})"
            ),
            "program-historical-quote-definition-indented-code": (
                f"> [r]: /u\n    [Spec 033]({target})"
            ),
            "program-historical-quote-paragraph-indented-lazy": (
                f"> paragraph\n    [Spec 033]({target})"
            ),
            "program-historical-multiline-quote-definition-indented-code": (
                f"> [r]:\n /u\n    [Spec 033]({target})"
            ),
            "program-historical-invalid-multiline-quote-definition-indented-lazy": (
                f"> [r]:\n <unterminated\n    [Spec 033]({target})"
            ),
            "program-historical-explicit-quote-setext-indented-code": (
                f"> paragraph\n> ===\n    [Spec 033]({target})"
            ),
            "program-historical-explicit-normal-quote-indented-lazy": (
                f"> paragraph\n> continuation\n    [Spec 033]({target})"
            ),
            "program-historical-atx-definition-indented-code": (
                f"# Heading\n[r]: /u\n    [Spec 033]({target})"
            ),
            "program-historical-quote-atx-definition-indented-code": (
                f"> # Heading\n> [r]: /u\n>     [Spec 033]({target})"
            ),
            "program-historical-paragraph-definition-lookalike-indented-continuation": (
                f"ordinary paragraph\n[r]: /u\n    [Spec 033]({target})"
            ),
            "program-historical-shortcut-label-1000": (
                f"[{'s' * 1000}]\n\n[{'s' * 1000}]: {target}"
            ),
            "program-historical-collapsed-label-999": (
                f"[{'c' * 999}][]\n\n[{'c' * 999}]: {target}"
            ),
            "program-historical-failed-inline-label-1000": (
                f"[{'i' * 1000}](not a link)\n\n[{'i' * 1000}]: {target}"
            ),
            "program-historical-soft-line-label-999": (
                f"[Spec 033][{'m' * 997}\nn]\n\n[{'m' * 997} n]: {target}"
            ),
            "program-historical-definition-before-thematic": (
                f"> [Spec 033][owner]\n>\n> [owner]:\n> {target}\n> ---"
            ),
            "program-historical-setext-destination-first-wins": (
                f"> [Spec 033][owner]\n>\n> [owner]:\n> ===\n> [owner]: {target}"
            ),
            "program-historical-paragraph-definition-setext": (
                f"> Ordinary paragraph\n> [owner]: {target}\n> ---\n> [Spec 033][owner]"
            ),
            "program-historical-html-named-destination": (
                "[Spec 033](..&sol;..&sol;..&sol;03.specs&sol;033-fixture&sol;spec.md)"
            ),
            "program-historical-list-lazy-setext-definition": (
                f"- paragraph\n===\n  [owner]: {target}\n  [Spec 033][owner]"
            ),
            "program-historical-inline-html-anchor-attribute": (
                f'<a href="[Spec 033]({target})">ok</a>'
            ),
            "program-historical-escaped-inline-html-opener": (
                f'\\<span title="[Spec 033]({target})">ok</span>'
            ),
            "program-historical-inline-html-comment": (
                f"before <!-- [Spec 033]({target}) --> after"
            ),
            "program-historical-inline-html-reference-label": (
                f"[<i>Spec 033</i>]\n\n[Spec 033]: {target}"
            ),
            "program-historical-invalid-type7-html-opener": (
                f"<x !!!>\n[Spec 033]({target})"
            ),
            "program-historical-inline-html-collapsed-collision": (
                '[<span title="x">Spec 033</span>][]\n\n'
                f'[<span title="y">Spec 033</span>]: {target}'
            ),
            "program-historical-inline-html-collapsed-identical": (
                '[<span title="x">Spec 033</span>][]\n\n'
                f'[<span title="x">Spec 033</span>]: {target}'
            ),
            "program-historical-comment-block-multiline-trailing": (
                f"<!-- owner evidence\nend --> [Spec 033]({target})"
            ),
            "program-historical-valid-inline-comment-trailing": (
                f"before <!-- owner evidence --> [Spec 033]({target})"
            ),
            "program-historical-escaped-multiline-definition-label": (
                r"[owner\] key][]"
                "\n\n"
                r"[owner\]"
                "\n"
                f"key]: {target}"
            ),
            "program-historical-short-table-cell-boundary": (
                f"| Label | Target |\n| - | :-: |\n| [Spec | 033]({target}) |"
            ),
            "program-historical-definition-backtick-title": (
                f"[Spec 033][owner]\n\n[owner]: {target} `title`"
            ),
            "program-historical-quote-processing-leaf": (
                f"> paragraph\n> <? owner ?>\n    [Spec 033]({target})"
            ),
            "program-historical-code-span-fake-link": (f"`[Spec 033]({target})`"),
            "program-historical-raw-pua-identical": (
                f"[Spec 033][\ue000owner]\n\n[\ue000owner]: {target}"
            ),
            "program-historical-inline-html-casefold-distinct-tag": (
                f"[<I>Spec 033</I>][]\n\n[<b>spec 033</b>]: {target}"
            ),
            "program-historical-double-backslash-code-span": (
                f"\\\\`[Spec 033]({target})`"
            ),
            "program-historical-orphan-inline-suffix-backtick": (
                f"orphan](`[Spec 033]({target})`)"
            ),
        }[mutation]
        if mutation == "program-historical-raw-html-heading":
            mutated.texts[roadmap] = evidence
        elif mutation == "program-historical-heading-indented-code":
            mutated.texts[roadmap] = f"{heading}\n\n#### Evidence\n{evidence}"
        else:
            mutated.texts[roadmap] = f"{heading}\n\n{evidence}"
    elif mutation == "program-execution-gate":
        plan = PurePosixPath("docs/04.execution/plans/2026-07-15-fixture-035.md")
        task = PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-035.md")
        spec = PurePosixPath("docs/03.specs/035-fixture/spec.md")
        paths = tuple(sorted((*paths, plan, task), key=lambda item: item.as_posix()))
        mutated.profiles[plan] = ProfileView("sdlc/plan", "sdlc", "authored")
        mutated.profiles[task] = ProfileView("sdlc/task", "sdlc", "authored")
        mutated.metadata[plan] = {"type": "sdlc/plan", "status": "active"}
        mutated.metadata[task] = {"type": "sdlc/task", "status": "active"}
        mutated.texts[plan] = (
            "[Spec](../../03.specs/035-fixture/spec.md)\n"
            "[Task](../tasks/2026-07-15-fixture-035.md)"
        )
        mutated.texts[task] = (
            "[Spec](../../03.specs/035-fixture/spec.md)\n"
            "[Plan](../plans/2026-07-15-fixture-035.md)"
        )
        mutated.texts[spec] += (
            "\n[Plan](../../04.execution/plans/2026-07-15-fixture-035.md)"
        )
        tracked_regular_paths = frozenset((*tracked_regular_paths, plan, task))
    elif mutation == "program-execution-no-pair":
        remove_execution_path(plan_034)
        remove_execution_path(task_034)
    elif mutation == "program-execution-closure-gap":
        close_original_034()
    elif mutation == "program-execution-closure-planning-gate":
        close_original_034()
        add_execution_pair("035", "035")
    elif mutation == "program-execution-closure-plan-only":
        close_original_034()
        add_execution_node(
            PurePosixPath("docs/04.execution/plans/2026-07-15-fixture-035.md"),
            "sdlc/plan",
            "[Spec](../../03.specs/035-fixture/spec.md)",
        )
    elif mutation == "program-execution-closure-task-only":
        close_original_034()
        add_execution_node(
            PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-035.md"),
            "sdlc/task",
            "[Spec](../../03.specs/035-fixture/spec.md)",
        )
    elif mutation == "program-execution-closure-nonreciprocal":
        close_original_034()
        add_execution_pair("035", "035")
        plan = PurePosixPath("docs/04.execution/plans/2026-07-15-fixture-035.md")
        mutated.texts[plan] = mutated.texts[plan].replace(
            "[Task](../tasks/2026-07-15-fixture-035.md)",
            "Task pending",
        )
    elif mutation == "program-execution-closure-multiple":
        close_original_034()
        add_execution_pair("035", "035")
        add_execution_pair("035-extra", "035")
    elif mutation == "program-execution-closure-connected-extra":
        close_original_034()
        add_execution_pair("035", "035")
        add_execution_node(
            PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-035-extra.md"),
            "sdlc/task",
            "[Plan](../plans/2026-07-15-fixture-035.md)",
        )
    elif mutation == "program-execution-premature-036-pair":
        close_original_034()
        add_original_036()
        add_execution_pair("036", "036")
    elif mutation == "program-execution-plan-only":
        remove_execution_path(task_034)
    elif mutation == "program-execution-task-only":
        remove_execution_path(plan_034)
    elif mutation == "program-execution-multiple":
        add_execution_pair("034-extra", "034")
    elif mutation == "program-execution-one-plan-two-tasks":
        add_execution_node(
            PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-034-extra.md"),
            "sdlc/task",
            "[Plan](../plans/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-two-plans-one-task":
        add_execution_node(
            PurePosixPath("docs/04.execution/plans/2026-07-15-fixture-034-extra.md"),
            "sdlc/plan",
            "[Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-unrelated-component":
        add_execution_pair("999", "999")
    elif mutation == "program-execution-active-follow-up-direct":
        add_execution_pair("042", "042")
    elif mutation == "program-execution-draft-follow-up-indirect":
        spec = PurePosixPath("docs/03.specs/042-fixture/spec.md")
        mutated.metadata[spec]["status"] = "draft"
        program = programs[2]
        follow_up = program.follow_ups[0]
        draft_follow_up = ProgramFollowUp(
            spec_id=follow_up.spec_id,
            order=follow_up.order,
            state="draft",
            reason=follow_up.reason,
            decision_id=follow_up.decision_id,
            evidence_mode=follow_up.evidence_mode,
        )
        programs = (
            *programs[:2],
            ProgramLineage(
                prd_id=program.prd_id,
                ard_id=program.ard_id,
                tranches=program.tranches,
                follow_ups=(draft_follow_up,),
            ),
            *programs[3:],
        )
        add_execution_node(
            PurePosixPath("docs/04.execution/plans/2026-07-15-fixture-042-draft.md"),
            "sdlc/plan",
            "[Spec](../../03.specs/042-fixture/spec.md)\n"
            "[Task](../tasks/2026-07-15-fixture-042-draft.md)",
        )
        add_execution_node(
            PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-042-draft.md"),
            "sdlc/task",
            "[Plan](../plans/2026-07-15-fixture-042-draft.md)",
        )
    elif mutation == "program-execution-balanced-escaped":
        remove_execution_path(plan_034)
        remove_execution_path(task_034)
        plan = PurePosixPath("docs/04.execution/plans/2026-07-15-fixture-(034).md")
        task = PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-(034).md")
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.texts[spec] = mutated.texts[spec].replace(
            "2026-07-15-fixture-034.md",
            "2026-07-15-fixture-(034).md",
        )
        add_execution_node(
            plan,
            "sdlc/plan",
            "[Spec](../../03.specs/034-fixture/spec.md)\n"
            "[Task](../tasks/2026-07-15-fixture-(034).md)",
        )
        add_execution_node(
            task,
            "sdlc/task",
            "[Spec](../../03.specs/034-fixture/spec.md)\n"
            r"[Plan](../plans/2026-07-15-fixture-\(034\).md)",
        )
    elif mutation == "program-execution-cross-container":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task\n> current](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-cross-container-destination":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](../tasks/2026-07-15-fixture-034.md\n> )",
        )
    elif mutation == "program-execution-cross-container-reference":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task][owner\n> key]\n\n[owner key]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-outer-fence-nested":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "> ~~~markdown\n> > [Task](../tasks/2026-07-15-fixture-034.md)\n> ~~~",
        )
    elif mutation == "program-execution-invalid-inline-garbage":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](../tasks/2026-07-15-fixture-034.md garbage)",
        )
    elif mutation == "program-execution-invalid-inline-angle-less-than":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](<../tasks/2026-07-15-fixture-034.md#<owner>)",
        )
    elif mutation == "program-execution-valid-paren-title":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](../tasks/2026-07-15-fixture-034.md (current))",
        )
    elif mutation == "program-execution-valid-single-title-closing-paren":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](../tasks/2026-07-15-fixture-034.md 'current ) owner')",
        )
    elif mutation == "program-execution-table-row-boundary":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "Label | Target\n"
            "--- | ---\n"
            "[Task | start\n"
            "current](../tasks/2026-07-15-fixture-034.md) | owner",
        )
    elif mutation == "program-execution-multiline-reference-definition":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task][owner]\n\n[owner]:\n  ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-definition-before-thematic":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "- [Task][owner]\n  \n  [owner]:\n"
            "  ../tasks/2026-07-15-fixture-034.md\n  ---",
        )
    elif mutation == "program-execution-setext-destination-first-wins":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "- [Task][owner]\n  \n  [owner]:\n  ===\n"
            "  [owner]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-paragraph-definition-setext":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "- Ordinary paragraph\n"
            "  [owner]: ../tasks/2026-07-15-fixture-034.md\n"
            "  ---\n  [Task][owner]",
        )
    elif mutation == "program-execution-html-percent-destination":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](..&#37;2Ftasks&#37;2F2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-quote-lazy-setext-definition":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "> paragraph\n===\n"
            "> [owner]: ../tasks/2026-07-15-fixture-034.md\n"
            "> [Task][owner]",
        )
    elif mutation == "program-execution-inline-html-multiline-attribute":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '<span\n title="[Task](../tasks/2026-07-15-fixture-034.md)">\nok</span>',
        )
    elif mutation == "program-execution-invalid-inline-html-tag":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "<x [Task](../tasks/2026-07-15-fixture-034.md)>ok</x>",
        )
    elif mutation == "program-execution-escaped-html-comment-opener":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "\\<!-- [Task](../tasks/2026-07-15-fixture-034.md) -->",
        )
    elif mutation == "program-execution-inline-html-full-unicode-collision":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '[Task][<span title="가">owner</span>]\n\n'
            '[<span title="나">owner</span>]: '
            "../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-inline-html-full-unicode-identical":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '[Task][<span title="가">owner</span>]\n\n'
            '[<span title="가">owner</span>]: '
            "../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-comment-block-next-line":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "\n<!-- owner evidence --> ignored\n"
            "[Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation in {
        "program-execution-multiline-definition-label-999",
        "program-execution-multiline-definition-label-1000",
    }:
        second_length = 498 if mutation.endswith("label-999") else 499
        first = "a" * 500
        second = "b" * second_length
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            f"[Task][{first} {second}]\n\n"
            f"[{first}\n{second}]: "
            "../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-code-span-link":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "`[Task](../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-list-cdata-leaf":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "- paragraph\n"
            "  <![CDATA[owner]]>\n"
            "      [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-overlapping-comment-closer":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "\n<!-->\n[Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-invalid-html-destination":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](../tasks/2026-07-15-fixture-034&bogus;.md)",
        )
    elif mutation == "program-execution-completed-follow-up-component":
        add_execution_pair("033", "033")
    elif mutation == "program-execution-unresolved-before-shortcut":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[literal][Task]\n\n[Task]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-multiline-paren-title":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task][owner]\n\n[owner]: ../tasks/2026-07-15-fixture-034.md\n  (current)",
        )
    elif mutation == "program-execution-inline-nested-paren-title":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task](../tasks/2026-07-15-fixture-034.md ((nested))",
        )
    elif mutation == "program-execution-ordered-12-indented-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "12.\n        [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-ordered-empty-three-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "12.   \n        [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-ordered-tab-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "12.\t    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-tab-continuation-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "12.\n\t    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-list-lazy-continuation":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "- [Task\n](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-whitespace-collapsed-label":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[ \t][]\n\n[ \t]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-normal-tab-spaced-label":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Task][ owner\tkey ]\n\n[owner key]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-setext-indented-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "Execution evidence\n---\n    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-standalone-setext-equals-indented-continuation":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "\n===\n    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-quote-lazy-equals-indented-continuation":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "> paragraph\n===\n    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-quote-definition-indented-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "> [r]: /u\n    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-multiline-quote-definition-indented-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "> [r]:\n /u\n    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif (
        mutation == "program-execution-invalid-multiline-list-definition-indented-lazy"
    ):
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "- [r]:\n <unterminated\n      [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-explicit-quote-setext-indented-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "> paragraph\n> ===\n    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-setext-definition-indented-code":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "Heading\n===\n[r]: /u\n    [Task](../tasks/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-execution-full-label-999":
        label = "f" * 999
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            f"[Task][{label}]\n\n[{label}]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-collapsed-label-1000":
        label = "c" * 1000
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            f"[{label}][]\n\n[{label}]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-soft-line-label-1000":
        usage = "m" * 998 + "\n" + "n"
        definition = "m" * 998 + " n"
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            f"[Task][{usage}]\n\n[{definition}]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-escaped-label-999":
        label = r"\*" * 499 + "x"
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            f"[Task][{label}]\n\n[{label}]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-escaped-backtick-link":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "\\`[Task](../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-code-first-html-overlap":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '`<a x="`">[Task](../tasks/2026-07-15-fixture-034.md)`',
        )
    elif mutation == "program-execution-inline-html-attribute-casefold":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '[Task][<SPAN TITLE="가">OWNER</SPAN>]\n\n'
            '[<span title="가">owner</span>]: '
            "../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-angle-destination-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Other](<foo`bar>)[Task](../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-html-attribute-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '<span title="`">[Task](../tasks/2026-07-15-fixture-034.md)</span>`',
        )
    elif mutation == "program-execution-invalid-inline-title-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '[Other](./unrelated.md "<span title=`bad>) [Task]'
            "(../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-invalid-reference-title-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Other][owner]\n\n"
            '[owner]: ./unrelated.md "<span title=`bad>\n'
            "[Task](../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-valid-inline-title-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '[Other](./unrelated.md "<span title=`bad>") [Task]'
            "(../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-valid-reference-title-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "[Other][owner]\n\n"
            '[owner]: ./unrelated.md "<span title=`bad>"\n'
            "[Task](../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-orphan-inline-suffix-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "orphan](`[Task](../tasks/2026-07-15-fixture-034.md)`)",
        )
    elif mutation == "program-execution-unmatched-outer-title-backtick":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            '[`[Task](../tasks/2026-07-15-fixture-034.md "`")',
        )
    elif mutation in {
        "program-execution-raw-pua-label-999",
        "program-execution-raw-pua-label-1000",
    }:
        label = "\ue000" * (
            999 if mutation == "program-execution-raw-pua-label-999" else 1000
        )
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            f"[Task][{label}]\n\n[{label}]: ../tasks/2026-07-15-fixture-034.md",
        )
    elif mutation == "program-execution-code-paragraph-recovery":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "`unmatched\n\n[Task](../tasks/2026-07-15-fixture-034.md)`",
        )
    elif mutation == "program-execution-nonreciprocal":
        mutated.texts[plan_034] = mutated.texts[plan_034].replace(
            "[Task](../tasks/2026-07-15-fixture-034.md)",
            "`../tasks/2026-07-15-fixture-034.md`",
        )
    elif mutation == "program-diagnostic-contract":
        spec = PurePosixPath("docs/03.specs/034-fixture/spec.md")
        mutated.metadata[spec]["status"] = "done"
        add_execution_node(
            PurePosixPath("docs/04.execution/tasks/2026-07-15-fixture-034-extra.md"),
            "sdlc/task",
            "[Plan](../plans/2026-07-15-fixture-034.md)",
        )
    elif mutation == "program-ordered-123-indented-code-authority":
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        table = (
            "Document Family | Lifecycle Transition\n"
            "--- | ---\n"
            "PRD | `draft -> active -> done \\| archived`\n"
            "ARD/ADR | `draft -> active -> accepted \\| archived`\n"
            "Spec | `draft -> active -> done \\| archived`\n"
            "Plan/Task | `draft -> active -> done \\| archived`\n"
            "Operations | `draft -> active -> accepted \\| archived`\n"
            "Archive Record | `archived` only"
        )
        indented = "\n".join(f"         {line}" for line in table.splitlines())
        mutated.texts[stage_zero] += f"\n\n123.\n{indented}"
    elif mutation == "program-ordered-empty-four-code-authority":
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        table = (
            "Document Family | Lifecycle Transition\n"
            "--- | ---\n"
            "PRD | `draft -> active -> done \\| archived`\n"
            "ARD/ADR | `draft -> active -> accepted \\| archived`\n"
            "Spec | `draft -> active -> done \\| archived`\n"
            "Plan/Task | `draft -> active -> done \\| archived`\n"
            "Operations | `draft -> active -> accepted \\| archived`\n"
            "Archive Record | `archived` only"
        )
        indented = "\n".join(f"         {line}" for line in table.splitlines())
        mutated.texts[stage_zero] += f"\n\n123.    \n{indented}"
    elif mutation == "program-thematic-indented-code-authority":
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        table = (
            "Document Family | Lifecycle Transition\n"
            "--- | ---\n"
            "PRD | `draft -> active -> done \\| archived`\n"
            "ARD/ADR | `draft -> active -> accepted \\| archived`\n"
            "Spec | `draft -> active -> done \\| archived`\n"
            "Plan/Task | `draft -> active -> done \\| archived`\n"
            "Operations | `draft -> active -> accepted \\| archived`\n"
            "Archive Record | `archived` only"
        )
        indented = "\n".join(f"    {line}" for line in table.splitlines())
        mutated.texts[stage_zero] += f"\n\n***\n{indented}"
    elif mutation in {
        "program-lazy-quote-pseudo-authority",
        "program-explicit-quote-authority",
    }:
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        rows = [
            "Document Family | Lifecycle Transition",
            "--- | ---",
            "PRD | `draft -> active -> done \\| archived`",
            "ARD/ADR | `draft -> active -> accepted \\| archived`",
            "Spec | `draft -> active -> done \\| archived`",
            "Plan/Task | `draft -> active -> done \\| archived`",
            "Operations | `draft -> active -> accepted \\| archived`",
            "Archive Record | `archived` only",
        ]
        if mutation == "program-lazy-quote-pseudo-authority":
            table = "> paragraph\n" + "\n".join(rows)
        else:
            table = "\n".join(f"> {row}" for row in rows)
        mutated.texts[stage_zero] += "\n\n" + table
    elif mutation in {
        "program-duplicate-authority",
        "program-duplicate-authority-leading",
        "program-duplicate-authority-trailing",
        "program-duplicate-authority-shortcut",
        "program-duplicate-authority-collapsed",
        "program-duplicate-authority-full-reference",
        "program-duplicate-authority-balanced",
        "program-duplicate-authority-blockquote",
        "program-duplicate-authority-extra-prd",
        "program-duplicate-authority-wrapper-columns",
        "program-invalid-authority-link-garbage",
        "program-code-wrapped-authority-link",
        "program-code-label-authority-link",
        "program-code-html-literal-authority",
        "program-invalid-authority-reference-definition",
        "program-duplicate-authority-html-numeric",
        "program-duplicate-authority-html-named",
        "program-invalid-authority-html-reference",
        "program-duplicate-authority-html-headers",
        "program-duplicate-authority-html-family",
        "program-duplicate-authority-html-transition",
        "program-duplicate-authority-one-hyphen-delimiter",
        "program-duplicate-authority-two-hyphen-delimiter",
    }:
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        rows = [
            "**[Ｄｏｃｕｍｅｎｔ Ｆａｍｉｌｙ](./family.md)** | *Lifecycle   Transition*",
            "--- | ---",
            "[*ＰＲＤ*](./prd.md) | `draft → active → done \\| archived`",
            "ARD/ADR | `draft -> active -> accepted \\| archived`",
            "Spec | `draft -> active -> done \\| archived`",
            "Plan/Task | `draft -> active -> done \\| archived`",
            "Operations | `draft -> active -> accepted \\| archived`",
            "Archive Record | `archived` only",
        ]
        definitions = ""
        if mutation == "program-duplicate-authority-leading":
            rows = [f"| {row}" for row in rows]
        elif mutation == "program-duplicate-authority-trailing":
            rows = [f"{row} |" for row in rows]
        elif mutation == "program-duplicate-authority-shortcut":
            rows[2] = "[ＰＲＤ] | `draft -> active -> done \\| archived`"
            definitions = "\n\n[ＰＲＤ]: ./prd_(owner).md"
        elif mutation == "program-duplicate-authority-collapsed":
            rows[2] = "[ＰＲＤ][] | `draft -> active -> done \\| archived`"
            definitions = "\n\n[ＰＲＤ]: ./prd_(owner).md"
        elif mutation == "program-duplicate-authority-full-reference":
            rows[2] = "[*ＰＲＤ*][prd-owner] | `draft -> active -> done \\| archived`"
            definitions = "\n\n[prd-owner]: ./prd_(owner).md"
        elif mutation == "program-duplicate-authority-balanced":
            rows[2] = (
                "[*ＰＲＤ*](./prd_(owner).md) | `draft -> active -> done \\| archived`"
            )
        elif mutation == "program-duplicate-authority-blockquote":
            rows = [f"> > {row}" for row in rows]
        elif mutation == "program-duplicate-authority-extra-prd":
            rows.append("PRD | `draft -> archived`")
        elif mutation == "program-duplicate-authority-wrapper-columns":
            rows = [
                "Owner | Lifecycle Transition | Document Family | Notes",
                "--- | --- | --- | ---",
                "platform | `draft -> active -> done \\| archived` | PRD | current",
                "platform | `draft -> active -> accepted \\| archived` | ARD/ADR | current",
                "platform | `draft -> active -> done \\| archived` | Spec | current",
                "platform | `draft -> active -> done \\| archived` | Plan/Task | current",
                "platform | `draft -> active -> accepted \\| archived` | Operations | current",
                "platform | `archived` only | Archive Record | current",
            ]
        elif mutation == "program-invalid-authority-link-garbage":
            rows[2] = (
                "[*ＰＲＤ*](./prd.md garbage) | `draft -> active -> done \\| archived`"
            )
        elif mutation == "program-code-wrapped-authority-link":
            rows[2] = "`[ＰＲＤ](./prd.md)` | `draft -> active -> done \\| archived`"
        elif mutation == "program-code-label-authority-link":
            rows[2] = "[`ＰＲＤ`](./prd.md) | `draft -> active -> done \\| archived`"
        elif mutation == "program-code-html-literal-authority":
            rows[2] = "`<i>`PRD | `draft -> active -> done \\| archived`"
        elif mutation == "program-invalid-authority-reference-definition":
            rows[2] = "[ＰＲＤ][owner] | `draft -> active -> done \\| archived`"
            definitions = "\n\n[owner]: ./prd.md garbage"
        elif mutation == "program-duplicate-authority-html-numeric":
            rows[2] = "[PR&#68;](./prd.md) | `draft -> active -> done \\| archived`"
        elif mutation == "program-duplicate-authority-html-named":
            rows[2] = "[PR&Dopf;](./prd.md) | `draft -> active -> done \\| archived`"
        elif mutation == "program-invalid-authority-html-reference":
            rows[2] = "[PR&bogus;](./prd.md) | `draft -> active -> done \\| archived`"
        elif mutation == "program-duplicate-authority-html-headers":
            rows[0] = "<span>Document Family</span> | <b>Lifecycle Transition</b>"
        elif mutation == "program-duplicate-authority-html-family":
            rows[2] = (
                '<span title="ARD/ADR">PRD</span> | '
                "`draft -> active -> done \\| archived`"
            )
        elif mutation == "program-duplicate-authority-html-transition":
            rows[2] = "PRD | <span>draft -> active -> done \\| archived</span>"
        elif mutation == "program-duplicate-authority-one-hyphen-delimiter":
            rows = [f"| {row} |" for row in rows]
            rows[1] = "| - | :-: |"
        elif mutation == "program-duplicate-authority-two-hyphen-delimiter":
            rows[1] = "-- | :--:"
        mutated.texts[stage_zero] += "\n\n" + "\n".join(rows) + definitions
    elif mutation == "program-nonrendered-authority":
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        table = (
            "| Document Family | Lifecycle Transition |\n"
            "| --- | --- |\n"
            "| PRD | `draft -> active -> done \\| archived` |\n"
            "| ARD/ADR | `draft -> active -> accepted \\| archived` |\n"
            "| Spec | `draft -> active -> done \\| archived` |\n"
            "| Plan/Task | `draft -> active -> done \\| archived` |\n"
            "| Operations | `draft -> active -> accepted \\| archived` |\n"
            "| Archive Record | `archived` only |"
        )
        mutated.texts[stage_zero] += (
            f"\n\n```markdown\n{table}\n```\n\n<!--\n{table}\n-->"
        )
    elif mutation == "program-nonrendered-authority-blockquote-fence":
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        table = (
            "Document Family | Lifecycle Transition\n"
            "--- | ---\n"
            "PRD | `draft -> active -> done \\| archived`\n"
            "ARD/ADR | `draft -> active -> accepted \\| archived`\n"
            "Spec | `draft -> active -> done \\| archived`\n"
            "Plan/Task | `draft -> active -> done \\| archived`\n"
            "Operations | `draft -> active -> accepted \\| archived`\n"
            "Archive Record | `archived` only"
        )
        quoted = "\n".join(f"> > {line}" for line in table.splitlines())
        mutated.texts[stage_zero] += f"\n\n> > ```markdown\n{quoted}\n> > ```"
    elif mutation in {
        "program-nonrendered-authority-outer-fence-nested",
        "program-nonrendered-authority-outer-raw-nested",
    }:
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        table = (
            "Document Family | Lifecycle Transition\n"
            "--- | ---\n"
            "PRD | `draft -> active -> done \\| archived`\n"
            "ARD/ADR | `draft -> active -> accepted \\| archived`\n"
            "Spec | `draft -> active -> done \\| archived`\n"
            "Plan/Task | `draft -> active -> done \\| archived`\n"
            "Operations | `draft -> active -> accepted \\| archived`\n"
            "Archive Record | `archived` only"
        )
        quoted = "\n".join(f"> > {line}" for line in table.splitlines())
        if mutation == "program-nonrendered-authority-outer-fence-nested":
            mutated.texts[stage_zero] += f"\n\n> ~~~markdown\n{quoted}\n> ~~~"
        else:
            mutated.texts[stage_zero] += f"\n\n> <div>\n{quoted}\n> </div>"
    elif mutation == "program-unmatched-bracket-performance":
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        mutated.texts[stage_zero] += (
            "\n\n" + "[" * 20_000 + " | Lifecycle Transition\n--- | ---\nPRD | active"
        )
    elif mutation == "program-unmatched-code-run-performance":
        stage_zero = PurePosixPath("docs/00.agent-governance/lineage-fixture.md")
        mutated.texts[stage_zero] += "\n\n" + "\n".join(
            "`" * length + "x" for length in range(1, 501)
        )
    elif mutation == "program-failed-inline-candidate-performance":
        mutated.texts[plan_034] += "\n\n" + "[x](" * 4_000
    elif mutation in {
        "program-inline-angle-destination-contract",
        "program-reference-angle-destination-contract",
        "program-inline-ownership-sweep-2000",
        "program-inline-ownership-sweep-4000",
        "program-inline-ownership-sweep-8000",
        "program-code-wrapped-html-sweep-2000",
        "program-code-wrapped-html-sweep-4000",
        "program-code-wrapped-html-sweep-8000",
        "program-provisional-self-visibility-contract",
        "program-nested-link-suppression-2000",
        "program-nested-link-suppression-4000",
        "program-nested-link-suppression-8000",
        "program-escaped-adjacent-backtick-contract",
        "program-bare-destination-depth-whitespace-contract",
        "program-backtick-owned-paragraph-sweep-2000",
        "program-backtick-owned-paragraph-sweep-4000",
        "program-backtick-owned-paragraph-sweep-8000",
        "program-execution-component-chain-500",
        "program-execution-component-chain-1000",
        "program-execution-component-chain-2000",
        "program-execution-component-chain-4000",
        "program-commonmark-character-predicate-contract",
        "program-opaque-label-index-sweep-2000",
        "program-opaque-label-index-sweep-4000",
        "program-opaque-label-index-sweep-8000",
    }:
        pass
    else:
        raise ConfigurationError(
            f"unknown program-lineage fixture mutation: {mutation}"
        )
    return (
        Context(
            mutated.root,
            paths,
            mutated.baseline_paths,
            mutated.profiles,
            mutated.texts,
            mutated.metadata,
            mutated.adapter_targets,
            mutated.governance_current_paths,
            mutated.governance_current_states,
            mutated.reference_current_packs,
            tracked_regular_paths,
        ),
        programs,
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
    if mutation == "link-broken":
        texts[source] += "\n[bad](./missing.md)\n"
    elif mutation == "link-absolute":
        texts[source] += "\n[bad](/etc/passwd)\n"
    elif mutation == "link-file-uri":
        texts[source] += "\n[bad](file:///tmp/x)\n"
    elif mutation == "link-escape":
        texts[source] += "\n[bad](../../../../escape.md)\n"
    elif mutation == "link-archive-bypass":
        texts[source] += "\n[bad](../../98.archive/999-fixture.md)\n"
    elif mutation == "link-adapter-missing":
        texts[source] += "\n[bad](../../../.claude/skills/missing/skill.md)\n"
    elif mutation == "links-excluded":
        texts[source] += (
            "\n```md\n[bad](./missing.md)\n```\n<!-- [bad](./missing.md) -->\n"
        )
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
            "\\[collapsed][]\n"
            "\\[shortcut]\n"
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
            f"\n{rendered[mutation]}\n\n"
            "[missing full]: ./missing-full.md\n"
            "[collapsed]: ./missing-collapsed.md\n"
            "[shortcut]: ./missing-shortcut.md\n"
            "[escaped shortcut]: ./missing-escaped-shortcut.md\n"
        )
    elif mutation == "link-invalid-fence-closer":
        texts[source] += (
            "\n```md\n[bad](./missing.md)\n``` still-open\n"
            "[also-bad](./missing-two.md)\n```\n"
        )
    elif mutation == "index-missing":
        path = DECLARED_INDEXES[0].path
        texts[path] = "\n".join(
            line
            for line in texts[path].splitlines()
            if "[`./999-fixture/spec.md`]" not in line
        )
    elif mutation == "index-stale":
        path = DECLARED_INDEXES[0].path
        texts[path] += "| [`./stale/spec.md`](./stale/spec.md) | stale | Active |\n"
    elif mutation == "index-duplicate":
        path = DECLARED_INDEXES[0].path
        row = next(
            line
            for line in texts[path].splitlines()
            if "[`./999-fixture/spec.md`]" in line
        )
        texts[path] += row + "\n"
    elif mutation == "index-status":
        path = DECLARED_INDEXES[0].path
        texts[path] = texts[path].replace("| Active |", "| Done |")
    elif mutation == "index-tree":
        path = DECLARED_INDEXES[0].path
        texts[path] = texts[path].replace("    └── spec.md\n", "")
    elif mutation == "index-anchor-prose":
        path = DECLARED_INDEXES[0].path
        texts[path] = texts[path].replace(
            "### Current Spec Index",
            "This prose mentions ### Current Spec Index",
        )
    elif mutation == "index-multi-order":
        path = DECLARED_INDEXES[0].path
        texts[path] = "\n".join(
            line
            for line in texts[path].splitlines()
            if "[`./998-second/spec.md`]" not in line
            and "[`./999-fixture/spec.md`]" not in line
        )
    elif mutation == "owner-duplicate":
        plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
        task = PurePosixPath("docs/04.execution/tasks/2026-07-12-fixture.md")
        metadata[task]["type"] = metadata[plan]["type"]
        metadata[task]["title"] = metadata[plan]["title"]
        traceability = (
            "\n## Traceability\n\n[up](../../01.requirements/999-fixture.md)\n"
        )
        texts[plan] += traceability
        texts[task] += traceability
    elif mutation == "owner-missing":
        metadata[PurePosixPath("docs/01.requirements/999-fixture.md")]["title"] = ""
    elif mutation == "ledger-missing-row":
        texts[LEDGER_PATH] = "\n".join(
            line
            for line in texts[LEDGER_PATH].splitlines()
            if "`docs/01.requirements/999-fixture.md`" not in line
        )
    elif mutation == "ledger-incomplete":
        texts[LEDGER_PATH] = texts[LEDGER_PATH].replace(
            "| path | title |", "| pathname | title |", 1
        )
    elif mutation == "ledger-unknown":
        texts[LEDGER_PATH] = texts[LEDGER_PATH].rstrip() + (
            "\n| `docs/unknown.md` | Fixture | content/reference | | preserve | "
            "`docs/unknown.md` | fixture | none | 2026-07-12 | repo | retain | "
            "change | platform | reviewed |\n"
        )
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
        target = PurePosixPath("docs/90.references/research/2026-07-07-wer/accepted.md")
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
            texts[owner] = (
                texts[owner].replace("### Research Pack Index", "Research Pack Index")
                + "\n```markdown\n### Research Pack Index\n"
                + row
                + "\n```\n"
            )
    elif mutation.startswith("reference-index-"):
        owner = PurePosixPath("docs/90.references/research/2026-07-07-wer/README.md")
        accepted = "| [accepted](accepted.md) | `accepted` |"
        active = "| [active](active.md) | `active` |"
        if mutation == "reference-index-missing":
            texts[owner] = texts[owner].replace(accepted + "\n", "")
        elif mutation == "reference-index-malformed":
            texts[owner] = texts[owner].replace(
                "| Reference | Lifecycle |", "| Reference | Status |"
            )
        elif mutation == "reference-index-stale":
            texts[owner] = texts[owner].replace(
                active, active + "\n| [ghost](ghost.md) | `active` |"
            )
        elif mutation == "reference-index-duplicate":
            texts[owner] = texts[owner].replace(accepted, accepted + "\n" + accepted)
        elif mutation == "reference-index-status":
            texts[owner] = texts[owner].replace(
                accepted, "| [accepted](accepted.md) | `active` |"
            )
        elif mutation == "reference-index-swap":
            texts[owner] = texts[owner].replace(
                accepted, "| [ghost](ghost.md) | `accepted` |"
            )
        elif mutation == "reference-index-order":
            texts[owner] = texts[owner].replace(
                f"{accepted}\n{active}", f"{active}\n{accepted}"
            )
        elif mutation == "reference-index-fenced-lookalike":
            texts[owner] = (
                texts[owner].replace("## Report Index", "Report Index")
                + "\n```markdown\n## Report Index\n```\n"
            )
    elif mutation == "reference-wrong-profile-member":
        target = PurePosixPath("docs/90.references/research/2026-07-07-wer/accepted.md")
        profiles[target] = ProfileView("content/archive", "common", "authored")
    elif mutation.startswith("collection-"):
        owner = PurePosixPath("docs/90.references/research/2026-07-07-wer/README.md")
        tree_line = "├── accepted.md"
        row = "| [accepted](accepted.md) | `accepted` |"
        ghost_line = "├── ghost.md"
        ghost_row = "| [ghost](ghost.md) | `accepted` |"
        if mutation == "collection-tree-missing":
            texts[owner] = texts[owner].replace(tree_line + "\n", "")
        elif mutation == "collection-row-missing":
            texts[owner] = texts[owner].replace(row + "\n", "")
        elif mutation == "collection-tree-stale":
            texts[owner] = texts[owner].replace(
                tree_line, tree_line + "\n" + ghost_line
            )
        elif mutation == "collection-row-stale":
            texts[owner] = texts[owner].replace(row, row + "\n" + ghost_row)
        elif mutation == "collection-tree-duplicate":
            texts[owner] = texts[owner].replace(tree_line, tree_line + "\n" + tree_line)
        elif mutation == "collection-row-duplicate":
            texts[owner] = texts[owner].replace(row, row + "\n" + row)
        elif mutation == "collection-equal-count-swap":
            texts[owner] = (
                texts[owner].replace(tree_line, ghost_line).replace(row, ghost_row)
            )
        elif mutation == "collection-artifact-added":
            target = owner.parent / "added.md"
            paths = tuple(sorted((*paths, target), key=lambda item: item.as_posix()))
            profiles[target] = ProfileView("content/reference", "common", "authored")
            metadata[target] = {
                "title": "Added",
                "type": "content/reference",
                "status": "accepted",
                "owner": "platform",
                "updated": "2026-07-14",
            }
            texts[target] = "# Added\n"
            tracked_regular_paths = frozenset((*tracked_regular_paths, target))
        elif mutation == "collection-artifact-removed":
            target = owner.parent / "accepted.md"
            paths = tuple(path for path in paths if path != target)
            profiles.pop(target)
            metadata.pop(target)
            texts.pop(target)
            tracked_regular_paths = frozenset(
                path for path in tracked_regular_paths if path != target
            )
        elif mutation == "collection-heading-lookalike":
            texts[owner] = (
                texts[owner].replace("### Structure", "Structure")
                + "\n```markdown\n### Structure\n```\n"
            )
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
    incident = PurePosixPath("docs/05.operations/incidents/2026-07-15-INC-999.md")
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
        mutated.texts[prd] += "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
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
        mutated.texts[prd] += "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
    elif mutation == "broken-link":
        mutated.texts[plan] = mutated.texts[plan].replace(
            "../tasks/2026-07-15-fixture.md",
            "../tasks/2099-01-01-missing.md",
            1,
        )
        mutated.texts[plan] += "\n[Task reciprocal](../tasks/2026-07-15-fixture.md)\n"
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
        mutated.texts[prd] += "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
    elif mutation == "three-space-disallowed-target":
        mutated.texts[prd] = mutated.texts[prd].replace("\n|", "\n   |")
        mutated.texts[prd] = mutated.texts[prd].replace(
            "../03.specs/999-fixture/spec.md",
            "../04.execution/tasks/2026-07-15-fixture.md",
            1,
        )
        mutated.texts[prd] += "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
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
        mutated.texts[prd] += "\n[Spec reciprocal](../03.specs/999-fixture/spec.md)\n"
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
                "\\[bad ref][], \\[bad ref]"
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
        raise ConfigurationError(f"unknown body-contract fixture mutation: {mutation}")
    return mutated


def _fixture_rule_ids(context: Context, mutation: str) -> list[str]:
    mutated = _mutated_context(context, mutation)
    if mutation.startswith("link") or mutation in {"links-excluded"}:
        diagnostics = _link_diagnostics(mutated)
    elif mutation.startswith("index"):
        if mutation == "index-multi-order":
            missing = [
                item
                for item in _index_diagnostics(mutated)
                if item.rule_id == "INDEX-MISSING"
            ]
            targets = [item.expected.split(";", 1)[0] for item in missing]
            return (
                []
                if len(missing) == 2
                and targets == sorted(targets)
                and len(set(targets)) == 2
                else ["INDEX-MISSING"]
            )
        diagnostics = _index_diagnostics(mutated)
    elif mutation.startswith("owner"):
        if mutation == "owner-normalization":
            plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
            mutated.metadata[plan]["type"] = "ＳＤＬＣ／ＰＬＡＮ"
            mutated.metadata[plan]["title"] = "Ｆixture__Implementation Plan"
            key, diagnostic = _owner_key(mutated, plan)
            return (
                []
                if diagnostic is None and key == "sdlc-plan|fixture|fixture"
                else ["OWNER-KEY-MISSING"]
            )
        if mutation == "owner-first-upstream":
            plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
            texts = dict(mutated.texts)
            texts[plan] += (
                "\n[local-ref]: ../../README.md\n[prd-ref]: ../../01.requirements/999-fixture.md\n[spec-ref]: ../../03.specs/999-fixture/spec.md\n\n## Traceability\n\n[local][local-ref]\n[prd][prd-ref]\n[spec][spec-ref]\n"
            )
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
            return (
                [] if diagnostic is None and key == expected else ["OWNER-KEY-MISSING"]
            )
        if mutation == "owner-fallback":
            plan = PurePosixPath("docs/04.execution/plans/2026-07-12-fixture.md")
            key, diagnostic = _owner_key(mutated, plan)
            return (
                []
                if diagnostic is None and key == "sdlc-plan|fixture|fixture"
                else ["OWNER-KEY-MISSING"]
            )
        if mutation == "owner-exclusions":
            key, diagnostic = _owner_key(mutated, LEDGER_PATH)
            return (
                []
                if not key
                and diagnostic is None
                and not _owner_candidate(mutated, LEDGER_PATH)
                else ["OWNER-DUPLICATE"]
            )
        diagnostics = _owner_diagnostics(mutated)
    elif mutation.startswith("ledger"):
        diagnostics = _ledger_diagnostics(mutated)
    elif mutation.startswith("governance"):
        diagnostics = _governance_current_owner_diagnostics(mutated)
    elif mutation.startswith("reference"):
        diagnostics = _reference_current_pack_diagnostics(mutated)
    elif mutation.startswith("collection"):
        diagnostics = _collection_index_diagnostics(mutated)
        return [item.rule_id for item in sorted(diagnostics, key=diagnostic_sort_key)]
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
    if (
        list(fixture)
        != [
            "schemaVersion",
            "baseTree",
            "programLineageTree",
            "programLineageCases",
            "bodyContractTree",
            "bodyContractCases",
            "cases",
        ]
        or fixture["schemaVersion"] != 3
    ):
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
            if case.get("tree") != {"base": "baseTree"} or list(case) != [
                "name",
                "tree",
                "mutation",
                "expected_rule_ids",
            ]:
                failures.append(f"{case.get('name')}: case tree/schema differs")
                continue
            if not isinstance(case["mutation"], dict) or list(case["mutation"]) != [
                "kind"
            ]:
                failures.append(f"{case.get('name')}: structured mutation differs")
                continue
            expected = case["expected_rule_ids"]
            actual = _fixture_rule_ids(context, case["mutation"]["kind"])
            if actual != expected:
                failures.append(f"{case['name']}: expected {expected}, actual {actual}")
        program_context, program_lineage = _program_lineage_fixture_context(
            Path(temporary), fixture["programLineageTree"]
        )
        program_case_names = [
            case.get("name") for case in fixture["programLineageCases"]
        ]
        required_program_cases = {
            "program-lineage-valid",
            "program-lineage-state-mismatch",
            "program-lineage-missing-reciprocal",
            "program-lineage-balanced-escaped-reciprocal-links",
            "program-lineage-outer-fence-nested-reciprocal-is-not-evidence",
            "program-lineage-invalid-reference-definition-garbage",
            "program-lineage-valid-reference-definition-title",
            "program-lineage-valid-inline-double-title",
            "program-lineage-invalid-reference-angle-less-than",
            "program-lineage-valid-reference-angle-escaped-less-than",
            "program-lineage-valid-double-title-with-closing-paren",
            "program-lineage-list-marker-is-hard-boundary",
            "program-lineage-bare-nonpunctuation-escape-is-preserved",
            "program-lineage-reference-nonpunctuation-escape-is-preserved",
            "program-lineage-nested-link-outer-target-is-not-evidence",
            "program-lineage-adjacent-full-and-shortcut-references",
            "program-lineage-image-alt-subtree-link-is-not-evidence",
            "program-lineage-unresolved-bracket-before-inline-link",
            "program-lineage-unresolved-bracket-before-full-reference",
            "program-lineage-escaped-literal-before-shortcut-reference",
            "program-lineage-unresolved-image-opener-inline-link",
            "program-lineage-unresolved-image-opener-full-reference",
            "program-lineage-link-destination-span-is-consumed",
            "program-lineage-link-title-span-is-consumed",
            "program-lineage-image-title-span-is-consumed",
            "program-lineage-reference-definition-title-span-is-nonrendered",
            "program-lineage-valid-multiline-single-title-definition",
            "program-lineage-valid-escaped-paren-title-definition",
            "program-lineage-invalid-nested-paren-title-definition",
            "program-lineage-invalid-blank-destination-continuation",
            "program-lineage-invalid-unclosed-definition-title",
            "program-lineage-space-remainder-valid-title-span-is-nonrendered",
            "program-lineage-tab-remainder-valid-title-span-is-nonrendered",
            "program-lineage-space-remainder-invalid-nested-paren-title-keeps-definition",
            "program-lineage-tab-remainder-invalid-unclosed-title-keeps-definition",
            "program-lineage-next-line-title-trailing-garbage-keeps-definition",
            "program-lineage-invalid-next-line-title-phantom-remains-rendered",
            "program-lineage-continued-destination-invalid-title-keeps-definition",
            "program-lineage-escaped-close-in-reference-definition-label",
            "program-lineage-zero-column-reference-destination-continuation",
            "program-lineage-four-column-reference-destination-continuation",
            "program-lineage-tab-reference-destination-continuation",
            "program-lineage-zero-column-reference-title-span-is-nonrendered",
            "program-lineage-four-column-reference-title-span-is-nonrendered",
            "program-lineage-tab-reference-title-span-is-nonrendered",
            "program-lineage-multiline-reference-title-span-is-nonrendered",
            "program-lineage-blank-line-invalid-title-remains-rendered",
            "program-lineage-complete-definition-followed-four-space-code",
            "program-lineage-root-definition-before-thematic-boundary",
            "program-lineage-root-setext-looking-destination-first-wins",
            "program-lineage-quote-definition-before-thematic-boundary",
            "program-lineage-quote-setext-looking-destination-first-wins",
            "program-lineage-list-definition-before-thematic-boundary",
            "program-lineage-list-setext-looking-destination-first-wins",
            "program-lineage-root-paragraph-definition-lookalike-setext",
            "program-lineage-quote-paragraph-definition-lookalike-setext",
            "program-lineage-list-paragraph-definition-lookalike-setext",
            "program-lineage-numeric-character-reference-destination",
            "program-lineage-named-character-reference-destination",
            "program-lineage-character-reference-before-percent-decode",
            "program-lineage-escaped-ampersand-is-not-character-reference",
            "program-lineage-invalid-character-reference-destination",
            "program-lineage-numeric-character-reference-authority",
            "program-lineage-named-character-reference-authority",
            "program-lineage-invalid-character-reference-is-not-authority",
            "program-lineage-quote-lazy-setext-does-not-admit-definition",
            "program-lineage-list-lazy-setext-does-not-admit-definition",
            "program-lineage-execution-quote-lazy-setext-does-not-admit-definition",
            "program-lineage-inline-html-span-attribute-is-not-evidence",
            "program-lineage-inline-html-anchor-attribute-is-not-evidence",
            "program-lineage-multiline-inline-html-attribute-is-not-evidence",
            "program-lineage-markdown-inside-inline-html-is-evidence",
            "program-lineage-escaped-inline-html-opener-keeps-markdown",
            "program-lineage-invalid-inline-html-tag-keeps-markdown",
            "program-lineage-inline-html-comment-is-not-evidence",
            "program-lineage-inline-html-before-definition-does-not-create-definition",
            "program-lineage-inline-html-reference-label-remains-distinct",
            "program-lineage-escaped-html-comment-opener-keeps-execution-link",
            "program-lineage-valid-type7-html-quoted-greater-is-not-evidence",
            "program-lineage-invalid-type7-html-opener-keeps-historical-link",
            "program-lineage-inline-html-wrapped-authority-headers",
            "program-lineage-inline-html-wrapped-authority-family-ignores-attributes",
            "program-lineage-inline-html-wrapped-authority-transition",
            "program-lineage-inline-html-shortcut-label-tags-remain-distinct",
            "program-lineage-inline-html-collapsed-label-attributes-remain-distinct",
            "program-lineage-inline-html-full-label-unicode-attributes-remain-distinct",
            "program-lineage-identical-inline-html-shortcut-label-matches",
            "program-lineage-identical-inline-html-collapsed-label-matches",
            "program-lineage-identical-inline-html-full-unicode-label-matches",
            "program-lineage-inline-html-reference-label-999-count-is-preserved",
            "program-lineage-inline-html-reference-label-1000-is-rejected",
            "program-lineage-comment-block-closing-line-trailing-link-is-not-evidence",
            "program-lineage-multiline-comment-block-closing-line-is-raw",
            "program-lineage-comment-block-next-line-keeps-execution-link",
            "program-lineage-invalid-inline-comment-keeps-reciprocal-link",
            "program-lineage-valid-inline-comment-keeps-trailing-historical-link",
            "program-lineage-inline-html-tag-cannot-cross-blank-paragraph",
            "program-lineage-multiline-reference-definition-label-resolves",
            "program-lineage-escaped-multiline-definition-label-resolves-collapsed",
            "program-lineage-multiline-reference-definition-label-999-resolves",
            "program-lineage-multiline-reference-definition-label-1000-is-rejected",
            "program-lineage-one-hyphen-delimiter-authority",
            "program-lineage-two-hyphen-delimiter-authority",
            "program-lineage-short-delimiter-table-cell-is-hard-boundary",
            "program-lineage-inline-destination-backtick-suffix-is-invalid",
            "program-lineage-reference-definition-backtick-title-is-invalid",
            "program-lineage-code-span-link-remains-nonrendered",
            "program-lineage-quote-comment-block-closes-paragraph",
            "program-lineage-quote-processing-instruction-closes-paragraph",
            "program-lineage-list-cdata-closes-paragraph",
            "program-lineage-root-declaration-closes-paragraph",
            "program-lineage-overlapping-comment-closer-ends-first-line",
            "program-lineage-lazy-quote-pseudo-table-is-not-authority",
            "program-lineage-explicit-quote-table-is-authority",
            "program-lineage-reference-definition-cannot-interrupt-paragraph",
            "program-lineage-reference-definition-after-blank-boundary",
            "program-lineage-reference-definition-after-heading-boundary",
            "program-lineage-failed-inline-candidate-falls-back-to-shortcut",
            "program-lineage-ordered-123-tilde-fence-reciprocal-is-not-evidence",
            "program-lineage-unordered-indented-code-reciprocal-is-not-evidence",
            "program-lineage-ordered-1-normal-list-paragraph-is-evidence",
            "program-lineage-nested-list-raw-html-is-not-evidence",
            "program-lineage-ordered-12-indented-code-execution-is-not-evidence",
            "program-lineage-ordered-123-indented-code-table-is-not-authority",
            "program-lineage-unordered-empty-marker-four-spaces-code-is-not-evidence",
            "program-lineage-ordered-empty-marker-five-spaces-code-is-not-evidence",
            "program-lineage-ordered-empty-marker-two-spaces-code-is-not-evidence",
            "program-lineage-unordered-four-space-same-line-content-is-evidence",
            "program-lineage-unordered-five-space-same-line-content-is-code",
            "program-lineage-ordered-empty-marker-three-spaces-code-is-not-execution",
            "program-lineage-ordered-empty-marker-four-spaces-code-table-is-not-authority",
            "program-lineage-unordered-tab-padding-code-is-not-reciprocal-evidence",
            "program-lineage-list-lazy-continuation-reciprocal-is-evidence",
            "program-lineage-list-sibling-is-hard-boundary",
            "program-lineage-unordered-tab-normal-content-is-historical-evidence",
            "program-lineage-ordered-tab-normal-content-is-historical-evidence",
            "program-lineage-blockquote-lazy-continuation-is-historical-evidence",
            "program-lineage-ordered-tab-padding-code-is-not-execution-evidence",
            "program-lineage-tab-continuation-code-is-not-execution-evidence",
            "program-lineage-list-lazy-continuation-is-execution-evidence",
            "program-lineage-whitespace-shortcut-label-is-not-reciprocal-evidence",
            "program-lineage-normal-spaced-reference-label-is-reciprocal-evidence",
            "program-lineage-tab-only-full-reference-label-is-not-historical-evidence",
            "program-lineage-soft-break-whitespace-reference-label-is-not-historical-evidence",
            "program-lineage-whitespace-collapsed-label-is-not-execution-evidence",
            "program-lineage-normal-tab-spaced-label-is-execution-evidence",
            "program-lineage-setext-followed-indented-reciprocal-is-not-evidence",
            "program-lineage-setext-followed-indented-historical-is-not-evidence",
            "program-lineage-thematic-followed-indented-historical-is-not-evidence",
            "program-lineage-setext-followed-indented-execution-is-not-evidence",
            "program-lineage-thematic-followed-indented-table-is-not-authority",
            "program-lineage-standalone-equals-before-indented-reciprocal-is-evidence",
            "program-lineage-standalone-double-hyphen-before-indented-historical-is-evidence",
            "program-lineage-standalone-equals-before-indented-execution-is-evidence",
            "program-lineage-standalone-triple-hyphen-before-indented-historical-is-code",
            "program-lineage-definition-then-standalone-equals-indented-reciprocal-is-evidence",
            "program-lineage-definition-then-indented-historical-is-code",
            "program-lineage-list-second-paragraph-is-historical-evidence",
            "program-lineage-quote-lazy-equals-indented-execution-is-evidence",
            "program-lineage-quote-lazy-double-hyphen-indented-reciprocal-is-evidence",
            "program-lineage-valid-quote-definition-closes-reciprocal-paragraph",
            "program-lineage-valid-quote-definition-closes-historical-paragraph",
            "program-lineage-valid-quote-definition-closes-execution-paragraph",
            "program-lineage-normal-quote-paragraph-indented-historical-is-lazy-evidence",
            "program-lineage-invalid-quote-definition-indented-reciprocal-is-lazy-evidence",
            "program-lineage-valid-multiline-quote-definition-closes-reciprocal-paragraph",
            "program-lineage-valid-multiline-quote-definition-closes-historical-paragraph",
            "program-lineage-valid-multiline-quote-definition-closes-execution-paragraph",
            "program-lineage-invalid-multiline-quote-definition-indented-historical-is-lazy-evidence",
            "program-lineage-valid-multiline-list-definition-then-code-is-not-reciprocal-evidence",
            "program-lineage-invalid-multiline-list-definition-then-indent-is-execution-evidence",
            "program-lineage-explicit-quote-setext-closes-reciprocal-paragraph",
            "program-lineage-explicit-quote-setext-closes-historical-paragraph",
            "program-lineage-explicit-quote-setext-closes-execution-paragraph",
            "program-lineage-explicit-normal-quote-line-keeps-historical-lazy-paragraph",
            "program-lineage-thematic-then-definition-indented-reciprocal-is-code",
            "program-lineage-atx-then-definition-indented-historical-is-code",
            "program-lineage-setext-then-definition-indented-execution-is-code",
            "program-lineage-quote-atx-then-definition-indented-historical-is-code",
            "program-lineage-list-atx-then-definition-indented-reciprocal-is-code",
            "program-lineage-paragraph-definition-lookalike-indented-historical-is-evidence",
            "program-lineage-shortcut-reference-label-999-is-reciprocal-evidence",
            "program-lineage-shortcut-reference-label-1000-is-not-historical-evidence",
            "program-lineage-full-reference-label-999-is-execution-evidence",
            "program-lineage-full-reference-label-1000-is-not-reciprocal-evidence",
            "program-lineage-collapsed-reference-label-999-is-historical-evidence",
            "program-lineage-collapsed-reference-label-1000-is-not-execution-evidence",
            "program-lineage-failed-inline-fallback-label-999-is-reciprocal-evidence",
            "program-lineage-failed-inline-fallback-label-1000-is-not-historical-evidence",
            "program-lineage-soft-line-reference-label-999-is-historical-evidence",
            "program-lineage-soft-line-reference-label-1000-is-not-execution-evidence",
            "program-lineage-escaped-reference-label-999-is-execution-evidence",
            "program-lineage-escaped-reference-label-1000-is-not-reciprocal-evidence",
            "program-lineage-unmatched-code-next-paragraph-reciprocal",
            "program-lineage-cross-container-reciprocal-is-not-evidence",
            "program-lineage-cross-container-reciprocal-reference-is-not-evidence",
            "program-lineage-invalid-historical-exception",
            "program-lineage-paragraph-break-is-not-evidence",
            "program-lineage-raw-html-is-not-evidence",
            "program-lineage-indented-code-is-not-evidence",
            "program-lineage-heading-indented-code-is-not-evidence",
            "program-lineage-paragraph-continuation-is-evidence",
            "program-lineage-blockquote-raw-html-is-not-evidence",
            "program-lineage-blockquote-tilde-fence-is-not-evidence",
            "program-lineage-blockquote-indented-code-is-not-evidence",
            "program-lineage-outer-raw-nested-link-is-not-evidence",
            "program-lineage-nested-indented-link-is-not-evidence",
            "program-lineage-valid-angle-destination",
            "program-lineage-valid-angle-destination-parentheses",
            "program-lineage-invalid-unmatched-angle-destination",
            "program-lineage-atx-heading-is-hard-boundary",
            "program-lineage-setext-heading-is-hard-boundary",
            "program-lineage-thematic-break-is-hard-boundary",
            "program-lineage-gfm-table-cell-is-hard-boundary",
            "program-lineage-angle-nonpunctuation-escape-is-preserved",
            "program-lineage-image-target-is-not-link-evidence",
            "program-lineage-image-inside-link-preserves-outer-target",
            "program-lineage-unresolved-bracket-before-collapsed-reference",
            "program-lineage-valid-multiline-double-title-definition",
            "program-lineage-valid-inline-single-title",
            "program-lineage-unmatched-code-next-paragraph-historical",
            "program-lineage-unmatched-code-next-container-historical",
            "program-lineage-soft-break-code-span-is-not-evidence",
            "program-lineage-raw-html-heading-is-not-section",
            "program-lineage-root-to-quote-link-is-not-evidence",
            "program-lineage-quote-to-root-link-is-not-evidence",
            "program-lineage-quote-depth-link-is-not-evidence",
            "program-lineage-quote-depth-return-link-is-not-evidence",
            "program-lineage-sibling-quote-link-is-not-evidence",
            "program-lineage-same-quote-soft-break-is-evidence",
            "program-lineage-root-to-quote-reference-is-not-evidence",
            "program-lineage-quote-to-root-reference-is-not-evidence",
            "program-lineage-quote-depth-reference-is-not-evidence",
            "program-lineage-same-quote-reference-soft-break-is-evidence",
            "program-lineage-blocked-successor-execution",
            "program-lineage-ready-preplanning-gap",
            "program-lineage-successor-closure-gap",
            "program-lineage-successor-planning-gate",
            "program-lineage-successor-plan-only",
            "program-lineage-successor-task-only",
            "program-lineage-successor-nonreciprocal-pair",
            "program-lineage-successor-multiple-pairs",
            "program-lineage-successor-connected-extra",
            "program-lineage-premature-third-tranche-pair",
            "program-lineage-ready-plan-only",
            "program-lineage-ready-task-only",
            "program-lineage-ready-multiple-pairs",
            "program-lineage-ready-one-plan-two-tasks",
            "program-lineage-ready-two-plans-one-task",
            "program-lineage-unrelated-execution-component",
            "program-lineage-follow-up-current-execution-is-absent",
            "program-lineage-active-follow-up-direct-execution-is-rejected",
            "program-lineage-draft-follow-up-indirect-execution-is-rejected",
            "program-lineage-balanced-escaped-execution-links",
            "program-lineage-outer-fence-nested-execution-is-not-evidence",
            "program-lineage-invalid-inline-destination-garbage",
            "program-lineage-invalid-inline-angle-less-than",
            "program-lineage-valid-inline-paren-title",
            "program-lineage-valid-single-title-with-closing-paren",
            "program-lineage-gfm-table-row-is-hard-boundary",
            "program-lineage-multiline-reference-definition",
            "program-lineage-completed-follow-up-rejects-current-execution",
            "program-lineage-unresolved-bracket-before-shortcut-reference",
            "program-lineage-valid-multiline-paren-title-definition",
            "program-lineage-invalid-inline-nested-paren-title",
            "program-lineage-unmatched-code-next-paragraph-execution",
            "program-lineage-cross-container-execution-is-not-evidence",
            "program-lineage-cross-container-destination-is-not-evidence",
            "program-lineage-cross-container-execution-reference-is-not-evidence",
            "program-lineage-ready-nonreciprocal-pair",
            "program-lineage-stable-diagnostic-contract",
            "program-lineage-duplicate-stage00-authority",
            "program-lineage-leading-pipe-authority",
            "program-lineage-trailing-pipe-authority",
            "program-lineage-shortcut-reference-authority",
            "program-lineage-collapsed-reference-authority",
            "program-lineage-full-reference-authority",
            "program-lineage-balanced-destination-authority",
            "program-lineage-nested-blockquote-authority",
            "program-lineage-duplicate-extra-family-row-authority",
            "program-lineage-wrapper-column-authority",
            "program-lineage-invalid-authority-link-garbage",
            "program-lineage-code-wrapped-authority-link-is-not-family",
            "program-lineage-code-label-inside-authority-link-is-family",
            "program-lineage-invalid-reference-definition-is-not-authority",
            "program-lineage-outer-fence-nested-table-is-not-authority",
            "program-lineage-outer-raw-nested-table-is-not-authority",
            "program-lineage-fenced-blockquote-is-not-authority",
            "program-lineage-nonrendered-stage00-table",
            "program-lineage-unmatched-bracket-performance",
            "program-lineage-unmatched-code-run-performance",
            "program-lineage-failed-inline-candidate-performance",
            "program-lineage-inline-ownership-sweep-2000",
            "program-lineage-inline-ownership-sweep-4000",
            "program-lineage-inline-ownership-sweep-8000",
            "program-lineage-code-wrapped-html-sweep-2000",
            "program-lineage-code-wrapped-html-sweep-4000",
            "program-lineage-code-wrapped-html-sweep-8000",
            "program-lineage-provisional-self-visibility-is-source-ordered",
            "program-lineage-nested-link-suppression-2000",
            "program-lineage-nested-link-suppression-4000",
            "program-lineage-nested-link-suppression-8000",
            "program-lineage-escaped-adjacent-backtick-run-is-code",
            "program-lineage-bare-destination-depth-whitespace-is-invalid",
            "program-lineage-backtick-owned-paragraph-sweep-2000",
            "program-lineage-backtick-owned-paragraph-sweep-4000",
            "program-lineage-backtick-owned-paragraph-sweep-8000",
            "program-lineage-execution-component-chain-500",
            "program-lineage-execution-component-chain-1000",
            "program-lineage-execution-component-chain-2000",
            "program-lineage-execution-component-chain-4000",
            "program-lineage-commonmark-character-predicates",
            "program-lineage-opaque-label-index-sweep-2000",
            "program-lineage-opaque-label-index-sweep-4000",
            "program-lineage-opaque-label-index-sweep-8000",
            "program-lineage-unicode-space-inline-is-not-reciprocal",
            "program-lineage-unicode-space-reference-is-not-execution",
            "program-lineage-link-label-code-span-bracket-does-not-close-link",
            "program-lineage-code-span-fake-link-remains-nonrendered-run-control",
            "program-lineage-odd-backslash-escapes-opening-code-run",
            "program-lineage-backslash-inside-code-does-not-escape-closing-run",
            "program-lineage-mixed-backtick-run-label-keeps-reciprocal-link",
            "program-lineage-raw-pua-cannot-collide-with-html-identity",
            "program-lineage-identical-raw-pua-reference-label-matches",
            "program-lineage-raw-pua-reference-label-999-resolves",
            "program-lineage-raw-pua-reference-label-1000-is-rejected",
            "program-lineage-html-backtick-does-not-close-outer-code-span",
            "program-lineage-inline-angle-destination-is-link-grammar",
            "program-lineage-reference-angle-destination-is-link-grammar",
            "program-lineage-code-span-html-is-literal-not-authority",
            "program-lineage-inline-html-label-casefolds-tags",
            "program-lineage-inline-html-label-casefolds-attributes",
            "program-lineage-inline-html-label-distinct-tags-after-casefold",
            "program-lineage-even-backslash-keeps-opening-code-run",
            "program-lineage-angle-destination-backtick-owns-syntax",
            "program-lineage-html-attribute-backtick-owns-syntax",
            "program-lineage-invalid-inline-title-does-not-own-backtick",
            "program-lineage-invalid-reference-title-does-not-own-backtick",
            "program-lineage-valid-inline-title-owns-backtick",
            "program-lineage-valid-reference-title-owns-backtick",
            "program-lineage-orphan-inline-suffix-does-not-own-reciprocal-backtick",
            "program-lineage-orphan-inline-suffix-does-not-own-historical-backtick",
            "program-lineage-orphan-inline-suffix-does-not-own-execution-backtick",
            "program-lineage-unmatched-outer-bracket-opens-code-before-title-suffix",
        }
        if set(program_case_names) != required_program_cases or len(
            program_case_names
        ) != len(set(program_case_names)):
            failures.append("required unique program-lineage cases are incomplete")
        program_validator = globals().get("_program_lineage_diagnostics")
        for case in fixture["programLineageCases"]:
            if list(case) != ["name", "mutation", "expected_rule_ids"]:
                failures.append(
                    f"{case.get('name')}: program-lineage case schema differs"
                )
                continue
            if program_validator is None:
                failures.append(
                    f"{case['name']}: PROGRAM-LINEAGE rules are unimplemented"
                )
                continue
            mutated, mutated_programs = _mutated_program_lineage_fixture(
                program_context, program_lineage, case["mutation"]
            )
            started = time.perf_counter()
            diagnostics = sorted(
                program_validator(mutated, mutated_programs),
                key=diagnostic_sort_key,
            )
            elapsed = time.perf_counter() - started
            actual = [item.rule_id for item in diagnostics]
            if actual != case["expected_rule_ids"]:
                failures.append(
                    f"{case['name']}: expected {case['expected_rule_ids']}, "
                    f"actual {actual}"
                )
            angle_contract = {
                "program-inline-angle-destination-contract": (
                    "[x](<foo>)",
                    ("foo",),
                ),
                "program-reference-angle-destination-contract": (
                    "[x]\n\n[x]: <foo>",
                    ("foo",),
                ),
                "program-execution-unmatched-outer-title-backtick": (
                    '[`[x](/t "`")',
                    (),
                ),
                "program-provisional-self-visibility-contract": (
                    '[y](/u "`")`[y](/u "`")',
                    ("/u",),
                ),
                "program-escaped-adjacent-backtick-contract": (
                    r"\``[Task](../tasks/t.md)`",
                    (),
                ),
            }.get(case["mutation"])
            if angle_contract is not None:
                source, expected_links = angle_contract
                actual_links = _extract_links(source)
                if actual_links != expected_links:
                    failures.append(
                        f"{case['name']}: expected links "
                        f"{expected_links!r}, actual {actual_links!r}"
                    )
            if case["mutation"] == "program-bare-destination-depth-whitespace-contract":
                destination_contracts = (
                    ("[Task](../tasks/t(foo bar).md)", ()),
                    (
                        "[Task]\n\n[Task]: ../tasks/t(foo bar).md",
                        (),
                    ),
                    (
                        "[outer]([Task](../tasks/t.md ))",
                        ("../tasks/t.md",),
                    ),
                )
                for source, expected_links in destination_contracts:
                    actual_links = _extract_links(source)
                    if actual_links != expected_links:
                        failures.append(
                            f"{case['name']}: destination input "
                            f"{source!r} expected links "
                            f"{expected_links!r}, actual "
                            f"{actual_links!r}"
                        )
            if case["mutation"] == "program-commonmark-character-predicate-contract":
                character_contracts = (
                    ("[Task](../tasks/t.md\x1c)", ()),
                    (
                        "[Task](../tasks/t.md\u00a0x)",
                        ("../tasks/t.md\u00a0x",),
                    ),
                    ("[x]\n\n[x]: /t\x1c", ()),
                    ("[x]\n\n[x]: /t\u00a0x", ("/t\u00a0x",)),
                    ('[x](/t\t"title")', ("/t",)),
                    ('[x](/t\n"title")', ("/t",)),
                    ('[x](/t\r\n"title")', ("/t",)),
                    ('[x](\n/t "title")', ("/t",)),
                    ('[x](\r\n/t "title")', ("/t",)),
                    ('[x](/t "title"\n)', ("/t",)),
                    ('[x](/t\x00"title")', ()),
                    ('[x](/t\x0b"title")', ()),
                    ('[x](/t\x0c"title")', ()),
                    ('[x](/t\x1f"title")', ()),
                    ('[x](/t\x7f"title")', ()),
                    ("[x](/t\u2003x)", ("/t\u2003x",)),
                    ("[x](/t\u3000x)", ("/t\u3000x",)),
                    ('[x](/t\u00a0"title")', ('/t\u00a0"title"',)),
                    ('[x](/t "a\u00a0b")', ("/t",)),
                    ('[x](/t "a\x0bb")', ("/t",)),
                    ('[x](/t "a\x1cb")', ("/t",)),
                    ('[x](/t "a\n\u00a0\nb")', ("/t",)),
                    ('[x](/t\n \n"title")', ()),
                    ('[x](/t\r\n \r\n"title")', ()),
                    ('[x](/t\x1c"title")', ()),
                    ('[x]\n\n[x]: /t\t"title"', ("/t",)),
                    ('[x]\n\n[x]: /t "a\x0bb"', ("/t",)),
                    ('[x]\n\n[x]: /t "a\x1cb"', ("/t",)),
                    ('[x]\n\n[x]: /t "a\n\u00a0\nb"', ("/t",)),
                    ('[x]\n\n[x]: /t\x0b"title"', ()),
                    ("[x](<http://[>)", ("http://[",)),
                )
                for source, expected_links in character_contracts:
                    actual_links = _extract_links(source)
                    if actual_links != expected_links:
                        failures.append(
                            f"{case['name']}: character-predicate input "
                            f"{source!r} expected links "
                            f"{expected_links!r}, actual "
                            f"{actual_links!r}"
                        )
                local_destination_contracts = (
                    ("http://[", ("external", None)),
                    (r"C:\docs\owner.md", ("LINK-ABSOLUTE", None)),
                )
                for raw_target, expected_local in local_destination_contracts:
                    try:
                        actual_local = _local_destination(
                            PurePosixPath("docs/spec.md"), raw_target
                        )
                    except ValueError as error:
                        failures.append(
                            f"{case['name']}: local destination {raw_target!r} "
                            f"raised {error!r}"
                        )
                        continue
                    if actual_local != expected_local:
                        failures.append(
                            f"{case['name']}: local destination {raw_target!r} "
                            f"expected {expected_local!r}, actual {actual_local!r}"
                        )
            if case["mutation"] == "program-reciprocal-unicode-space-inline":
                source_path = PurePosixPath("docs/03.specs/034-fixture/spec.md")
                canonical_raw = "../../02.architecture/requirements/0009-fixture.md"
                canonical_path = PurePosixPath(
                    "docs/02.architecture/requirements/0009-fixture.md"
                )
                canonical_contracts = (
                    canonical_raw,
                    canonical_raw.replace("0009-fixture", "0009%2Dfixture"),
                )
                for raw_target in canonical_contracts:
                    actual_local = _local_destination(source_path, raw_target)
                    if actual_local != ("local", canonical_path):
                        failures.append(
                            f"{case['name']}: canonical local input "
                            f"{raw_target!r} resolved as {actual_local!r}"
                        )
                rendered_canonical_contracts = (
                    f"[ARD]({canonical_raw.replace('-', '&#45;', 1)})",
                    "[ARD](" + canonical_raw.replace("-", r"\-", 1) + ")",
                )
                for markdown_source in rendered_canonical_contracts:
                    extracted = _extract_links(markdown_source)
                    actual_local = (
                        _local_destination(source_path, extracted[0])
                        if len(extracted) == 1
                        else None
                    )
                    if actual_local != ("local", canonical_path):
                        failures.append(
                            f"{case['name']}: grammar-normalized input "
                            f"{markdown_source!r} resolved as {actual_local!r}"
                        )
                for unicode_space in ("\u00a0", "\u2003", "\u3000"):
                    for raw_target in (
                        canonical_raw + unicode_space,
                        unicode_space + canonical_raw,
                    ):
                        actual_local = _local_destination(source_path, raw_target)
                        if actual_local == ("local", canonical_path):
                            failures.append(
                                f"{case['name']}: Unicode-space target "
                                f"{raw_target!r} collapsed to canonical path"
                            )
                        inline_source = f"[ARD]({raw_target})"
                        reference_source = "[ARD][owner]\n\n[owner]: " + raw_target
                        for markdown_source in (inline_source, reference_source):
                            extracted = _extract_links(markdown_source)
                            if extracted != (raw_target,):
                                failures.append(
                                    f"{case['name']}: rendered Unicode-space "
                                    f"input {markdown_source!r} extracted "
                                    f"{extracted!r}"
                                )
                            elif _local_destination(source_path, extracted[0]) == (
                                "local",
                                canonical_path,
                            ):
                                failures.append(
                                    f"{case['name']}: rendered Unicode-space "
                                    "target satisfied canonical ownership"
                                )
                control_target = canonical_raw + "\x1c"
                if _local_destination(source_path, control_target) == (
                    "local",
                    canonical_path,
                ):
                    failures.append(
                        f"{case['name']}: direct ASCII-control target "
                        "collapsed to canonical path"
                    )
            opaque_label_scale = {
                "program-opaque-label-index-sweep-2000": 2_000,
                "program-opaque-label-index-sweep-4000": 4_000,
                "program-opaque-label-index-sweep-8000": 8_000,
            }.get(case["mutation"])
            if opaque_label_scale is not None:
                label_scan = globals().get("_normalize_reference_label_span_scan")
                if label_scan is None:
                    failures.append(
                        f"{case['name']}: opaque-label interval index is unimplemented"
                    )
                else:
                    source = ("<i></i>[x] " * opaque_label_scale) + "\n\n[x]: /t"
                    masked = _mask_inline_html_tokens(source)
                    label_spans = tuple(
                        (match.start() + 1, match.end() - 1)
                        for match in re.finditer(r"\[x\]", masked)
                    )
                    token_count = len(masked.opaque_tokens)
                    if token_count != opaque_label_scale * 2:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{opaque_label_scale * 2} opaque tokens, actual "
                            f"{token_count}"
                        )
                    if len(label_spans) != opaque_label_scale + 1:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{opaque_label_scale + 1} labels, actual "
                            f"{len(label_spans)}"
                        )
                    total_steps = token_count
                    for label_start, label_end in label_spans:
                        scan_result = label_scan(masked, label_start, label_end)
                        total_steps += scan_result.steps
                        if scan_result.label != "x":
                            failures.append(
                                f"{case['name']}: opaque label normalized as "
                                f"{scan_result.label!r}"
                            )
                            break
                    work_bound = token_count + len(label_spans) * (
                        token_count.bit_length() + 3
                    )
                    if total_steps > work_bound:
                        failures.append(
                            f"{case['name']}: opaque-label work "
                            f"{total_steps} exceeded indexed bound "
                            f"{work_bound}"
                        )
                    actual_links = _extract_links(source)
                    if actual_links != ("/t",) * opaque_label_scale:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{opaque_label_scale} resolved shortcuts, actual "
                            f"{len(actual_links)}"
                        )
                    if opaque_label_scale == 2_000:
                        controls = _mask_inline_html_tokens("<i>x</i><b>y</b>")
                        control_spans = (
                            (0, 3),
                            (0, len(controls)),
                            (3, 4),
                            (1, 2),
                            (0, 2),
                            (1, 4),
                            (4, 8),
                            (8, 11),
                        )
                        for label_start, label_end in control_spans:
                            legacy_tokens = tuple(
                                (
                                    token_start - label_start,
                                    token_end - label_start,
                                    token_source,
                                )
                                for token_start, token_end, token_source in (
                                    controls.opaque_tokens
                                )
                                if label_start <= token_start and token_end <= label_end
                            )
                            expected_label = _normalize_reference_label(
                                controls[label_start:label_end],
                                raw_pua_encoded=True,
                                opaque_tokens=legacy_tokens,
                            )
                            scan_result = label_scan(controls, label_start, label_end)
                            if scan_result.label != expected_label:
                                failures.append(
                                    f"{case['name']}: adjacent/covering/"
                                    f"touching span {(label_start, label_end)} "
                                    f"expected {expected_label!r}, actual "
                                    f"{scan_result.label!r}"
                                )
            if case["mutation"] == "program-escaped-adjacent-backtick-contract":
                escaped_run_contracts = (
                    (r"\``[x](/t)`", ()),
                    (r"\```[x](/t)``", ()),
                    (r"\``[x](/t)``", ("/t",)),
                    (r"\\``[x](/t)``", ()),
                    (r"`open \``[x](/t)", ("/t",)),
                )
                for source, expected_links in escaped_run_contracts:
                    actual_links = _extract_links(source)
                    if actual_links != expected_links:
                        failures.append(
                            f"{case['name']}: escaped-run input "
                            f"{source!r} expected links "
                            f"{expected_links!r}, actual "
                            f"{actual_links!r}"
                        )
            if case["mutation"] == "program-execution-unmatched-outer-title-backtick":
                commonmark_code_contracts = (
                    ('[`[x](/t "`")', ()),
                    ('[x](/t "`")', ("/t",)),
                    (r"\`[x](/t) `", ("/t",)),
                    (r"`hidden \` [x](/t)", ("/t",)),
                    (r"\\`[x](/t)`", ()),
                    ("`[x](/t)`", ()),
                )
                for source, expected_links in commonmark_code_contracts:
                    actual_links = _extract_links(source)
                    if actual_links != expected_links:
                        failures.append(
                            f"{case['name']}: CommonMark source "
                            f"{source!r} expected links "
                            f"{expected_links!r}, actual "
                            f"{actual_links!r}"
                        )
            if case["mutation"] == "program-provisional-self-visibility-contract":
                source_order_contracts = (
                    ('[y](/u "`")`[y](/u "`")', ("/u",)),
                    ("[a](/a)[b](/b)", ("/a", "/b")),
                    ('`[a](/hidden)`[b](/b "`")', ("/b",)),
                    ('[a](/a "`")`[b](/hidden)`', ("/a",)),
                )
                for source, expected_links in source_order_contracts:
                    actual_links = _extract_links(source)
                    if actual_links != expected_links:
                        failures.append(
                            f"{case['name']}: source-order input "
                            f"{source!r} expected links "
                            f"{expected_links!r}, actual "
                            f"{actual_links!r}"
                        )
            backtick_owned_scale = {
                "program-backtick-owned-paragraph-sweep-2000": 2_000,
                "program-backtick-owned-paragraph-sweep-4000": 4_000,
                "program-backtick-owned-paragraph-sweep-8000": 8_000,
            }.get(case["mutation"])
            if backtick_owned_scale is not None:
                closer_scan = globals().get("_backtick_closer_scan")
                if closer_scan is None:
                    failures.append(
                        f"{case['name']}: backtick ownership scan is unimplemented"
                    )
                else:
                    source = "\n\n".join(
                        '[x](/t "`")' for _ in range(backtick_owned_scale)
                    )
                    owned_spans = _inline_link_syntax_spans(source)
                    scan_result = closer_scan(source, owned_spans)
                    if scan_result.closer_ends:
                        failures.append(
                            f"{case['name']}: owned backticks remained eligible: "
                            f"{len(scan_result.closer_ends)}"
                        )
                    linear_bound = len(source) + len(owned_spans) * 2
                    if scan_result.steps > linear_bound:
                        failures.append(
                            f"{case['name']}: backtick ownership work "
                            f"{scan_result.steps} exceeded linear bound "
                            f"{linear_bound}"
                        )
            execution_chain_scale = {
                "program-execution-component-chain-500": 500,
                "program-execution-component-chain-1000": 1_000,
                "program-execution-component-chain-2000": 2_000,
                "program-execution-component-chain-4000": 4_000,
            }.get(case["mutation"])
            if execution_chain_scale is not None:
                index_builder = globals().get("_current_execution_index")
                component_scan = globals().get("_current_execution_component_scan")
                if index_builder is None or component_scan is None:
                    failures.append(
                        f"{case['name']}: execution adjacency index is unimplemented"
                    )
                else:
                    spec = PurePosixPath("docs/03.specs/999-chain/spec.md")
                    nodes = tuple(
                        PurePosixPath(
                            f"docs/04.execution/tasks/999-chain-{index:04d}.md"
                        )
                        for index in range(execution_chain_scale)
                    )
                    chain_graph: dict[PurePosixPath, frozenset[PurePosixPath]] = {}
                    for index, node in enumerate(nodes):
                        targets = {spec} if index == 0 else set()
                        if index + 1 < len(nodes):
                            targets.add(nodes[index + 1])
                        chain_graph[node] = frozenset(targets)
                    execution_index = index_builder(chain_graph)
                    scan_result = component_scan(spec, frozenset(), execution_index)
                    cached_result = component_scan(spec, frozenset(), execution_index)
                    if scan_result.paths != nodes:
                        failures.append(
                            f"{case['name']}: expected ordered chain of "
                            f"{execution_chain_scale}, actual "
                            f"{len(scan_result.paths)}"
                        )
                    linear_bound = execution_chain_scale * 8 + 8
                    total_steps = execution_index.steps + scan_result.steps
                    if total_steps > linear_bound:
                        failures.append(
                            f"{case['name']}: execution graph work "
                            f"{total_steps} exceeded linear bound "
                            f"{linear_bound}"
                        )
                    if (
                        cached_result.steps != 0
                        or cached_result.paths is not scan_result.paths
                    ):
                        failures.append(
                            f"{case['name']}: execution component cache "
                            "was not reused safely"
                        )
            ownership_scale = {
                "program-inline-ownership-sweep-2000": 2_000,
                "program-inline-ownership-sweep-4000": 4_000,
                "program-inline-ownership-sweep-8000": 8_000,
            }.get(case["mutation"])
            if ownership_scale is not None:
                sweep_filter = globals().get("_intervals_not_contained")
                if sweep_filter is None:
                    failures.append(f"{case['name']}: interval sweep is unimplemented")
                else:
                    source = " ".join(
                        f'[x{index}](/t{index}) <i data-n="{index}">v</i>'
                        for index in range(ownership_scale)
                    )
                    link_spans, html_spans = _inline_syntax_ownership(source)
                    if len(link_spans) != ownership_scale:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{ownership_scale} independent links, actual "
                            f"{len(link_spans)}"
                        )
                    if len(html_spans) != ownership_scale * 2:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{ownership_scale * 2} independent HTML "
                            f"tokens, actual {len(html_spans)}"
                        )
                    html_result = sweep_filter(
                        _raw_inline_html_token_spans(source),
                        _inline_link_syntax_spans(source),
                    )
                    link_result = sweep_filter(
                        _inline_link_syntax_spans(source),
                        html_result.spans,
                    )
                    total_intervals = ownership_scale * 3
                    if (
                        html_result.steps > total_intervals
                        or link_result.steps > total_intervals
                    ):
                        failures.append(
                            f"{case['name']}: interval sweep work exceeded "
                            f"linear bound {total_intervals}: "
                            f"html={html_result.steps}, "
                            f"links={link_result.steps}"
                        )
                    if ownership_scale == 2_000:
                        endpoint_result = sweep_filter(
                            (
                                (-1, 10),
                                (0, 9),
                                (0, 10),
                                (0, 11),
                                (1, 10),
                                (9, 11),
                                (19, 29),
                                (20, 30),
                                (21, 29),
                                (21, 31),
                                (30, 31),
                            ),
                            ((0, 10), (20, 30)),
                        )
                        expected_endpoints = (
                            (-1, 10),
                            (0, 11),
                            (9, 11),
                            (19, 29),
                            (21, 31),
                            (30, 31),
                        )
                        if endpoint_result.spans != expected_endpoints:
                            failures.append(
                                f"{case['name']}: endpoint/nesting/overlap "
                                f"semantics differ: "
                                f"{endpoint_result.spans!r}"
                            )
            wrapped_html_scale = {
                "program-code-wrapped-html-sweep-2000": 2_000,
                "program-code-wrapped-html-sweep-4000": 4_000,
                "program-code-wrapped-html-sweep-8000": 8_000,
            }.get(case["mutation"])
            if wrapped_html_scale is not None:
                overlap_filter = globals().get("_intervals_not_overlapping")
                if overlap_filter is None:
                    failures.append(
                        f"{case['name']}: interval overlap sweep is unimplemented"
                    )
                else:
                    source = " ".join("`<i>x</i>`" for _ in range(wrapped_html_scale))
                    raw_html = _raw_inline_html_token_spans(source)
                    code_spans = _inline_code_spans(source, syntax_owned_spans=())
                    visible_html = _inline_html_token_spans(source)
                    overlap_result = overlap_filter(raw_html, code_spans)
                    if len(raw_html) != wrapped_html_scale * 2:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{wrapped_html_scale * 2} raw HTML tokens, "
                            f"actual {len(raw_html)}"
                        )
                    if len(code_spans) != wrapped_html_scale:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{wrapped_html_scale} code spans, actual "
                            f"{len(code_spans)}"
                        )
                    if visible_html or overlap_result.spans:
                        failures.append(
                            f"{case['name']}: code-wrapped HTML remained visible"
                        )
                    linear_bound = wrapped_html_scale * 3
                    if overlap_result.steps > linear_bound:
                        failures.append(
                            f"{case['name']}: overlap sweep work "
                            f"{overlap_result.steps} exceeded linear "
                            f"bound {linear_bound}"
                        )
                    if wrapped_html_scale == 2_000:
                        endpoint_result = overlap_filter(
                            (
                                (8, 10),
                                (0, 2),
                                (2, 4),
                                (1, 6),
                                (2, 5),
                                (3, 4),
                                (5, 7),
                            ),
                            ((2, 5),),
                        )
                        expected_endpoints = (
                            (8, 10),
                            (0, 2),
                            (5, 7),
                        )
                        if endpoint_result.spans != expected_endpoints:
                            failures.append(
                                f"{case['name']}: overlap before/inside/"
                                "covering/after/touching semantics or "
                                "source order differ: "
                                f"{endpoint_result.spans!r}"
                            )
                        html_contracts = (
                            (
                                "<i>v</i> `<b>h</b>` <u>v</u>",
                                ("<i>", "</i>", "<u>", "</u>"),
                            ),
                            (r"\`<i>x</i> `", ("<i>", "</i>")),
                            (r"\\`<i>x</i>`", ()),
                            (
                                r"`<i>x</i> \` <b>v</b>",
                                ("<b>", "</b>"),
                            ),
                            ("`<i>x</i>`", ()),
                        )
                        for html_source, expected_tokens in html_contracts:
                            actual_tokens = tuple(
                                html_source[start:end]
                                for start, end in _inline_html_token_spans(html_source)
                            )
                            if actual_tokens != expected_tokens:
                                failures.append(
                                    f"{case['name']}: HTML/code source "
                                    f"{html_source!r} expected tokens "
                                    f"{expected_tokens!r}, actual "
                                    f"{actual_tokens!r}"
                                )
            nested_link_scale = {
                "program-nested-link-suppression-2000": 2_000,
                "program-nested-link-suppression-4000": 4_000,
                "program-nested-link-suppression-8000": 8_000,
            }.get(case["mutation"])
            if nested_link_scale is not None:
                suppression_helper = globals().get("_nested_link_suppression")
                if suppression_helper is None:
                    failures.append(
                        f"{case['name']}: bracket-tree suppression is unimplemented"
                    )
                else:
                    source = "[" * nested_link_scale + "x" + "](/t)" * nested_link_scale
                    actual_links = _extract_links(source)
                    brackets, parents = _bracket_pairs(source, code_spans=())
                    suppression = suppression_helper(
                        parents,
                        frozenset(brackets),
                        frozenset(),
                        frozenset(),
                    )
                    if actual_links != ("/t",):
                        failures.append(
                            f"{case['name']}: expected deepest link only, "
                            f"actual {actual_links!r}"
                        )
                    if len(suppression.suppressed) != nested_link_scale - 1:
                        failures.append(
                            f"{case['name']}: expected "
                            f"{nested_link_scale - 1} suppressed ancestors, "
                            f"actual {len(suppression.suppressed)}"
                        )
                    linear_bound = nested_link_scale * 3
                    if suppression.steps > linear_bound:
                        failures.append(
                            f"{case['name']}: bracket-tree work "
                            f"{suppression.steps} exceeded linear bound "
                            f"{linear_bound}"
                        )
                    if nested_link_scale == 2_000:
                        nested_contracts = (
                            ("[[x](/inner)](broken", ("/inner",)),
                            ("[[x](broken](/outer)", ("/outer",)),
                            ("![alt [x](/hidden)](/image)", ()),
                            ("[![alt](/image)](/outer)", ("/outer",)),
                            ("![alt [x](/visible)", ("/visible",)),
                        )
                        for nested_source, expected_links in nested_contracts:
                            actual_links = _extract_links(nested_source)
                            if actual_links != expected_links:
                                failures.append(
                                    f"{case['name']}: nested/image input "
                                    f"{nested_source!r} expected links "
                                    f"{expected_links!r}, actual "
                                    f"{actual_links!r}"
                                )
            if (
                case["mutation"]
                in {
                    "program-unmatched-bracket-performance",
                    "program-unmatched-code-run-performance",
                    "program-failed-inline-candidate-performance",
                }
                and elapsed >= 2.0
            ):
                performance_subject = (
                    "20k unmatched bracket scan"
                    if case["mutation"] == "program-unmatched-bracket-performance"
                    else (
                        "500 unique unmatched backtick-run scan"
                        if case["mutation"] == "program-unmatched-code-run-performance"
                        else "4k failed inline-candidate scan"
                    )
                )
                failures.append(
                    f"{case['name']}: {performance_subject} took "
                    f"{elapsed:.3f}s, expected <2.000s"
                )
            if case["mutation"] == "program-diagnostic-contract":
                projection = tuple(
                    (
                        item.rule_id,
                        item.path.as_posix(),
                        item.profile,
                        item.expected,
                        item.actual,
                        item.owner,
                    )
                    for item in diagnostics
                )
                expected_projection = (
                    (
                        "PROGRAM-LINEAGE-EXECUTION-GATE",
                        "docs/03.specs/034-fixture/spec.md",
                        "sdlc/spec",
                        "zero current execution component or one closed reciprocal current Plan/Task component with direct Spec links for the first unfinished original tranche, and none for remaining original tranches or follow-ups",
                        "component=3, plans=1, tasks=2, direct-spec=False, reciprocal=False, dependency-ready-original=True",
                        OWNER,
                    ),
                    (
                        "PROGRAM-LINEAGE-STATE",
                        "docs/03.specs/034-fixture/spec.md",
                        "sdlc/spec",
                        "active",
                        "done",
                        OWNER,
                    ),
                )
                if projection != expected_projection:
                    failures.append(
                        f"{case['name']}: stable diagnostic tuples differ: "
                        f"{projection!r}"
                    )
        registry = load_registry(root)
        profiles_by_id = {profile.profile_id: profile for profile in registry.profiles}
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
                failures.append(f"{case['name']}: BODY-LINK rules are unimplemented")
                continue
            mutated = _mutated_body_contract_context(body_context, case["mutation"])
            try:
                diagnostics = body_validator(
                    mutated,
                    profiles_by_id,
                    case["bodyContracts"],
                    tuple(
                        PurePosixPath(value) for value in case.get("pathPrefixes", [])
                    ),
                )
            except TypeError:
                failures.append(f"{case['name']}: path-prefix scope is unimplemented")
                continue
            actual = sorted({item.rule_id for item in diagnostics})
            if actual != case["expected_rule_ids"]:
                failures.append(
                    f"{case['name']}: expected {case['expected_rule_ids']}, actual {actual}"
                )
        try:
            default_body_contracts = _parser().parse_args([]).body_contracts
            audit_body_contracts = (
                _parser().parse_args(["--body-contracts", "audit"]).body_contracts
            )
            default_prefixes = _parser().parse_args([]).body_contract_path_prefix
            repeated_prefixes = (
                _parser()
                .parse_args(
                    [
                        "--body-contracts",
                        "audit",
                        "--body-contract-path-prefix",
                        "docs/01.requirements",
                        "--body-contract-path-prefix",
                        "docs/03.specs",
                    ]
                )
                .body_contract_path_prefix
            )
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
                f"body-contract parser accepted invalid path prefix: {invalid_prefix!r}"
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
    proposed_forms = tuple(
        path
        for path in (
            PurePosixPath(
                "docs/99.templates/templates/common/archive-record.template.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/plans/"
                "2026-07-12-protected-surface-supply-chain-hardening.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/tasks/"
                "2026-07-12-protected-surface-supply-chain-hardening.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/plans/"
                "2026-07-14-template-lifecycle-contract-normalization.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/tasks/"
                "2026-07-14-template-lifecycle-contract-normalization.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/plans/"
                "2026-07-15-authority-and-lineage-foundation.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/tasks/"
                "2026-07-15-authority-and-lineage-foundation.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/plans/"
                "2026-07-16-document-schema-and-lifecycle-contract.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/tasks/"
                "2026-07-16-document-schema-and-lifecycle-contract.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/plans/"
                "2026-07-17-archive-record-and-workspace-boundary.md"
            ),
            PurePosixPath(
                "docs/98.archive/04.execution/tasks/"
                "2026-07-17-archive-record-and-workspace-boundary.md"
            ),
        )
        if (root / path).is_file()
    )
    production_context = _build_context(root, include_paths=proposed_forms)
    production = validate_cross_document_contracts(
        root,
        "strict",
        include_paths=proposed_forms,
    )
    if production:
        failures.append("strict production repository diagnostics must be empty")
    owner_keys, owner_diagnostics = _owner_state(production_context)
    current_unique_keys = {key for key in owner_keys.values() if key}
    governance_keys = [
        owner_keys.get(path, "") for path in production_context.governance_current_paths
    ]
    if owner_diagnostics:
        failures.append("production current-owner state has diagnostics")
    if any(not key for key in governance_keys) or len(governance_keys) != len(
        set(governance_keys)
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
        post_smdv_unique_keys = {key for key in post_smdv_keys.values() if key}
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
            pre_smdv_unique_keys = {key for key in pre_smdv_keys.values() if key}
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
    parser.add_argument(
        "--mode", choices=("compatibility", "strict"), default="compatibility"
    )
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
            raise ConfigurationError(
                "--self-test is mutually exclusive with inventory and include paths"
            )
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
        profiles_by_id = {profile.profile_id: profile for profile in registry.profiles}
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
            rows = [
                ("FAIL", item) for item in sorted(diagnostics, key=diagnostic_sort_key)
            ]
            envelope = _envelope(
                "inventory", counts, _inventory_documents(context), rows
            )
            print(json.dumps(envelope, ensure_ascii=False, separators=(",", ":")))
            return int(bool(rows))
        diagnostics = _raw_diagnostics(
            context,
            registry,
            profiles_by_id,
            args.body_contracts,
            tuple(args.body_contract_path_prefix),
        )
        rows = _apply_debt(context.root, diagnostics, args.mode)
        if args.format == "json":
            print(
                json.dumps(
                    _envelope(args.mode, counts, [], rows),
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print("\n".join(_text_rows(rows)))
        return int(any(outcome == "FAIL" for outcome, _ in rows))
    except (
        ConfigurationError,
        DocumentContractError,
        OSError,
        ValueError,
        yaml.YAMLError,
    ) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
