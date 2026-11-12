#!/usr/bin/env python3
"""Validate repository-local links, indexes, and current owners."""

from __future__ import annotations

import argparse
import bisect
import collections
import html
import json
import os
import posixpath
import re
import stat
import sys
import unicodedata
from dataclasses import dataclass, field as dataclass_field
from functools import lru_cache
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any, Callable, Iterable, Mapping, Sequence
from urllib.parse import unquote, urlsplit

import yaml

from document_contracts import (
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    Registry,
    TargetInventory,
    _parse_ls_files_stage_z,
    _run_git,
    classify_path,
    diagnostic_sort_key,
    enumerate_target_markdown,
    is_opaque_evaluation_output,
    verify_opaque_evaluation_output,
    load_registry,
    read_repository_text,
    scoped_document_content_paths,
    validated_changed_paths,
    task_execution_issues,
    task_status,
    task_contract_issues,
    direct_parent,
    MARKDOWN_TEMPLATE_PLACEHOLDER,
)


def frontmatter_mapping(text: str) -> Mapping[str, object]:
    """Read YAML frontmatter; malformed input names nothing."""

    if not text.startswith("---\n"):
        return {}
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return {}
    try:
        loaded = yaml.safe_load(text[4:closing])
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


# A file outside `docs/` names a numbered stage document in plain text
# instead of linking it, and reaches the tree through the documentation hub.
# The hub is the one entry point consumers depend on, so a stage can be
# reorganized without rewriting every implementation README that only needed
# to say which document owns a subject. Links inside `docs/` keep their own
# contracts, and a machine reference a program opens is not a link.
NUMBERED_STAGE_TARGET = re.compile(r"^docs/(?:0[1235]|90|99)\.")

ARCHIVE_ROOT = PurePosixPath("docs/98.archive")

OWNER = "cross-document-validator"
OWNER_EXCLUSIONS = (
    re.compile(
        r"^docs/90\.references/(?:audits|data|research)/"
        r"[0-9]{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/"
    ),
    re.compile(r"^examples/(?:aws|azure)/docs/"),
)
RETIRED_REFERENCE_ALIASES = {
    PurePosixPath(".github/README.md"): PurePosixPath(".github/repository-surface.md"),
}


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
    tracked_regular_paths: frozenset[PurePosixPath]
    tracked_modes: Mapping[PurePosixPath, str] | None = None
    readme_navigation: Any = None
    current_registry: Registry | None = None
    current_inventory: TargetInventory | None = None


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


def _terminal_governance_current_owners(
    registry: Registry,
    paths: Sequence[PurePosixPath],
    profiles: Mapping[PurePosixPath, ProfileView],
    metadata: Mapping[PurePosixPath, Mapping[str, Any]],
) -> tuple[tuple[PurePosixPath, ...], tuple[str, ...]]:
    """Derive common current owners from the terminal profile lifecycle."""

    owner_profiles = tuple(
        profile
        for profile in registry.profiles
        if profile.profile_class == "governance" and profile.mode == "authored"
    )
    owner_ids = {profile.profile_id for profile in owner_profiles}
    lifecycle_domains = {profile.lifecycle_domain for profile in owner_profiles}
    lifecycle_domain = (
        next(iter(lifecycle_domains)) if len(lifecycle_domains) == 1 else None
    )
    allowed_states = (
        tuple(
            state
            for state, validation_class in lifecycle_domain.states
            if validation_class == "current"
        )
        if lifecycle_domain is not None
        else ()
    )
    if (
        not owner_profiles
        or not allowed_states
        or any(
            not set(allowed_states).issubset(profile.status_domain)
            for profile in owner_profiles
        )
    ):
        raise ConfigurationError(
            "terminal governance current-owner profile is unavailable"
        )
    current = tuple(
        sorted(
            path
            for path in paths
            if profiles[path].profile_id in owner_ids
            and profiles[path].mode == "authored"
            and str(metadata[path].get("status", "")).casefold() in allowed_states
        )
    )
    if not current:
        raise ConfigurationError("terminal governance current-owner set is empty")
    return current, allowed_states


def _build_context(
    root: Path,
    include_paths: tuple[PurePosixPath, ...] = (),
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
        if is_opaque_evaluation_output(registry, path):
            verify_opaque_evaluation_output(root, path)
            texts[path] = ""
            metadata[path] = {}
            continue
        text = read_repository_text(root, path)
        texts[path] = text
        metadata[path] = frontmatter_mapping(text)
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
    tracked_modes = {
        entry.path: entry.mode
        for entry in _parse_ls_files_stage_z(
            _run_git(root, ("ls-files", "--stage", "-z"))
        )
        if entry.stage == 0
    }
    tracked_regular_paths = frozenset(
        path for path, mode in tracked_modes.items() if mode in {"100644", "100755"}
    )
    governance_current_paths, governance_current_states = (
        _terminal_governance_current_owners(
            registry,
            inventory.current_paths,
            profiles,
            metadata,
        )
    )
    return Context(
        root,
        inventory.current_paths,
        frozenset(inventory.baseline_paths),
        profiles,
        texts,
        metadata,
        adapters,
        governance_current_paths,
        governance_current_states,
        tracked_regular_paths,
        tracked_modes=tracked_modes,
        readme_navigation=getattr(registry, "readme_navigation", None),
        current_registry=registry,
        current_inventory=inventory,
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


# The pairing depends only on the text and the spans higher-priority syntax
# already claimed, and the same pair is scanned once per document per caller.
@lru_cache(maxsize=4096)
def _backtick_closer_scan(
    text: str,
    syntax_owned_spans: tuple[tuple[int, int], ...],
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

    # Callers receive their own mapping; the cached scan keeps its result.
    return dict(_backtick_closer_scan(text, tuple(syntax_owned_spans)).closer_ends)


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

    # Ownership resolution reaches this scan three times for the same value, so
    # keep the result. The definition scan below reads lazy-line provenance off
    # the value, which string equality cannot see, so it belongs in the key.
    return _committed_inline_link_destination_spans(
        value, getattr(value, "lazy_lines", frozenset())
    )


@lru_cache(maxsize=4096)
def _committed_inline_link_destination_spans(
    value: str,
    lazy_lines: frozenset[int],
) -> tuple[tuple[int, int], ...]:
    """Resolve suffix ownership for one exact text and provenance input."""

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

    # Resolve provenance before the cache. A rendered value carries its lazy
    # lines as an attribute that string equality cannot see, so two inputs that
    # compare and hash alike can still parse differently; the resolved set has
    # to be part of the key rather than travel on the value.
    if lazy_lines is None:
        lazy_lines = getattr(value, "lazy_lines", frozenset())
    definitions, spans = _parsed_reference_definitions(value, lazy_lines)
    # Callers own the mapping they receive; the cache keeps its own copy.
    return dict(definitions), spans


@lru_cache(maxsize=8192)
def _parsed_reference_definitions(
    value: str,
    lazy_lines: frozenset[int],
) -> tuple[tuple[tuple[str, str], ...], tuple[tuple[int, int], ...]]:
    """Parse one exact text and lazy-line input into an immutable result."""

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
    return tuple(definitions.items()), tuple(spans)


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
    source: PurePosixPath, raw: str, *, template: bool = False
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
    path_part = value.split("#", 1)[0]
    if (
        template
        and MARKDOWN_TEMPLATE_PLACEHOLDER.fullmatch(unquote(path_part)) is not None
    ):
        return "template", None
    path_part = path_part.split("?", 1)[0]
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


def _stage_boundary_diagnostic(
    source: PurePosixPath, profile: str, target: PurePosixPath
) -> Diagnostic | None:
    if source.parts and source.parts[0] == "docs":
        return None
    if not NUMBERED_STAGE_TARGET.match(target.as_posix().casefold()):
        return None
    if target.name.casefold() == "readme.md":
        return None
    return _diag(
        "LINK-STAGE-BOUNDARY",
        source,
        profile,
        "current owner or stage README navigation",
        target.as_posix(),
    )


# Exact data reads needed by current document procedures; no path glob or
# directory admission. A machine-read exception never permits a rendered link.
_STAGE_MACHINE_READS = frozenset(
    {
        (
            ".agents/skills/docs-stage-routing/SKILL.md",
            "docs/99.templates/registry.json",
            "machine-read",
        ),
        (
            ".agents/skills/incident-postmortem/SKILL.md",
            "docs/99.templates/registry.json",
            "machine-read",
        ),
        (
            ".agents/governance/document-authoring.md",
            "docs/99.templates/registry.json",
            "machine-read",
        ),
        (
            ".agents/governance/document-authoring.md",
            "docs/99.templates/contracts/frontmatter.schema.json",
            "machine-read",
        ),
        (
            ".agents/governance/document-lifecycle.md",
            "docs/99.templates/registry.json",
            "machine-read",
        ),
        (
            ".agents/governance/sdlc.md",
            "docs/99.templates/registry.json",
            "machine-read",
        ),
    }
)


def _stage_machine_reference_allowed(
    source: PurePosixPath, target: PurePosixPath, access_kind: str
) -> bool:
    return (source.as_posix(), target.as_posix(), access_kind) in _STAGE_MACHINE_READS


def _normalized_stage_reference(
    source: PurePosixPath, raw: str
) -> PurePosixPath | None:
    value = html.unescape(raw.strip())
    for _ in range(8):
        decoded = unquote(value)
        if decoded == value:
            break
        value = decoded
    value = value.replace("\\", "/")
    try:
        parsed = urlsplit(value)
    except ValueError:
        return None
    if parsed.scheme or parsed.netloc:
        host = (parsed.hostname or "").casefold()
        path = parsed.path.casefold()
        if host == "github.com" and path.startswith("/buenhyden/hy-home.k8s/"):
            if not path.startswith(
                ("/buenhyden/hy-home.k8s/blob/", "/buenhyden/hy-home.k8s/raw/")
            ):
                return None
        elif host == "raw.githubusercontent.com" and path.startswith(
            "/buenhyden/hy-home.k8s/"
        ):
            pass
        elif parsed.scheme != "file":
            return None
        value = parsed.path
    else:
        value = value.split("#", 1)[0].split("?", 1)[0]
    value = value.casefold()
    if value.startswith("docs/"):
        normalized = posixpath.normpath(value)
    elif value.startswith("/") or re.match(r"^[a-z]:/", value):
        normalized = posixpath.normpath(value)
        marker = normalized.find("/docs/")
        if marker < 0:
            return None
        normalized = normalized[marker + 1 :]
    else:
        normalized = posixpath.normpath(
            posixpath.join(source.parent.as_posix().casefold(), value)
        )
    if not NUMBERED_STAGE_TARGET.match(normalized):
        return None
    return PurePosixPath(normalized)


def _stage_reference_diagnostics(
    source: PurePosixPath, profile: str, text: str
) -> list[Diagnostic]:
    if source.parts and source.parts[0].casefold() == "docs":
        return []
    visible, _ = _readme_visible_lines(text)
    body = "\n".join(visible)
    candidates = [(target, "link") for target in _extract_links(body)]
    candidates.extend((target, "link") for target in README_NAV_HTML_HREF.findall(body))
    candidates.extend(
        (match.group(1), "link")
        for match in re.finditer(r"<(https?://[^<>\s]+)>", body, re.I)
    )
    candidates.extend(
        (match.group(1), "link")
        for match in re.finditer(r"<a\b[^>]*?\bhref\s*=\s*([^\s\"'>]+)", body, re.I)
    )
    candidates.extend(
        (match.group(1), "link")
        for match in re.finditer(r"\[\[([^]\n|]+)(?:\|[^]\n]*)?\]\]", body)
    )
    # Backtick/plain paths in instructions must not keep individual stage
    # records as hidden authority. Examples inside fences remain examples.
    candidates.extend(
        (match.group(0), "machine-read")
        for match in re.finditer(
            r"(?<![A-Za-z0-9_/:])(?:(?:\.\.?/)+|/[^\s`\"'()<>\[\],;]*/)?docs/[0-9]{2}\.[^\s`\"'()<>\[\],;]+\.(?:md|json)",
            body,
            re.I,
        )
    )
    findings: dict[str, Diagnostic] = {}
    for raw, access in candidates:
        target = _normalized_stage_reference(source, raw)
        if target is None or _stage_machine_reference_allowed(source, target, access):
            continue
        diagnostic = _stage_boundary_diagnostic(source, profile, target)
        if diagnostic is not None:
            findings.setdefault(target.as_posix(), diagnostic)
    return list(findings.values())


# Route grammars still belong to Stage 99. Normalized individual-document
# references are checked separately above; this check detects copied grammars.
_STAGE_PATH_TOKEN = re.compile(r"docs/[0-9]{2}\.[A-Za-z][^\s`\"'()\[\],;]*")
_PATH_PATTERN_META = frozenset(".^$*+?()[]{}|\\")


def _leading_alternation(body: str) -> tuple[tuple[str, ...], str] | None:
    """Split a pattern that opens on one `(?:a|b)` group into branches and tail."""

    if not body.startswith("(?:"):
        return None
    depth = 0
    branches: list[str] = []
    start = 3
    index = 0
    while index < len(body):
        character = body[index]
        if character == "\\":
            index += 2
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                branches.append(body[start:index])
                return tuple(branches), body[index + 1 :]
        elif character == "|" and depth == 1:
            branches.append(body[start:index])
            start = index + 1
        index += 1
    return None


def _fixed_directory_prefixes(pattern: str) -> tuple[str, ...]:
    """Return one literal directory per root a pattern's leading group names.

    A pattern may open on one group of alternative roots. Each branch still
    opens on a literal directory, so each branch contributes the prefix it would
    contribute alone."""

    body = pattern[1:] if pattern.startswith("^") else pattern
    split = _leading_alternation(body)
    if split is None:
        return (_fixed_directory_prefix(pattern),)
    branches, tail = split
    return tuple(_fixed_directory_prefix(branch + tail) for branch in branches)


def _fixed_directory_prefix(pattern: str) -> str:
    """Return the literal directory a profile's path pattern opens with.

    A pattern whose first metacharacter arrives before any `/` describes more
    than one root, so it contributes no prefix and governs no plain text."""

    body = pattern[1:] if pattern.startswith("^") else pattern
    literal: list[str] = []
    index = 0
    while index < len(body):
        character = body[index]
        if character == "\\" and index + 1 < len(body):
            literal.append(body[index + 1])
            index += 2
            continue
        if character in _PATH_PATTERN_META:
            break
        literal.append(character)
        index += 1
    prefix = "".join(literal)
    return prefix[: prefix.rfind("/") + 1] if "/" in prefix else ""


def _stage_document_prefixes(registry: Registry) -> frozenset[str]:
    """Collect the stage directories whose route grammar the registry owns."""

    return frozenset(
        prefix
        for profile in registry.profiles
        if profile.mode == "authored"
        for prefix in _fixed_directory_prefixes(profile.path_pattern)
        if prefix.startswith("docs/")
    )


def _stage_grammar_diagnostics(
    source: PurePosixPath,
    profile: str,
    text: str,
    prefixes: frozenset[str],
    exists: Callable[[str], bool],
) -> list[Diagnostic]:
    if source.parts and source.parts[0] == "docs":
        return []
    diagnostics: list[Diagnostic] = []
    reported: set[str] = set()
    for match in _STAGE_PATH_TOKEN.finditer(text):
        target = match.group(0).rstrip(".")
        if target in reported or not any(
            target.startswith(prefix) for prefix in prefixes
        ):
            continue
        if target in prefixes or f"{target}/" in prefixes:
            continue
        if exists(target):
            continue
        reported.add(target)
        diagnostics.append(
            _diag(
                "PATH-STAGE-GRAMMAR",
                source,
                profile,
                "named stage document or the collection that owns it",
                target,
            )
        )
    return diagnostics


def _retired_reference_link(context: Context, target: PurePosixPath) -> bool:
    """Admit a link to a retired path that declares an existing successor.

    `RETIRED_REFERENCE_ALIASES` records renamed paths. A terminal Stage 90
    document still names the path it observed, and rewriting it to follow the
    rename is what the lifecycle policy forbids. The declared successor must
    itself exist, so a retired alias cannot admit a link whose destination has
    since disappeared.
    """

    successor = RETIRED_REFERENCE_ALIASES.get(target)
    if successor is None:
        return False
    return _path_exists_without_dereference(
        context.root, successor, context.adapter_targets
    )


def _link_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    registry = context.current_registry or load_registry(context.root)
    stage_prefixes = _stage_document_prefixes(registry)

    def stage_target_exists(target: str) -> bool:
        return _path_exists_without_dereference(
            context.root, PurePosixPath(target), context.adapter_targets
        )

    for source in context.paths:
        profile = context.profiles[source].profile_id
        diagnostics.extend(
            _stage_reference_diagnostics(source, profile, context.texts[source])
        )
        diagnostics.extend(
            _stage_grammar_diagnostics(
                source,
                profile,
                context.texts[source],
                stage_prefixes,
                stage_target_exists,
            )
        )
        for raw in _extract_links(context.texts[source]):
            kind, target = _local_destination(
                source, raw, template=context.profiles[source].mode == "template"
            )
            if kind in {"external", "anchor", "template"}:
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
            if target.is_relative_to(ARCHIVE_ROOT):
                continue  # ADR-0053: the archive and links into it are unchecked.
            if not _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            ):
                if _retired_reference_link(context, target):
                    continue
                diagnostics.append(
                    _diag(
                        "LINK-BROKEN",
                        source,
                        profile,
                        "existing repository target",
                        target.as_posix(),
                    )
                )
                continue
            boundary = _stage_boundary_diagnostic(source, profile, target)
            if boundary is not None:
                diagnostics.append(boundary)
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


def task_base_rows(
    text: str, profile: DocumentProfile
) -> tuple[tuple[tuple[str, str], ...], ...]:
    """Read current Task rows."""

    contract = profile.body_contract
    if contract is None or contract.task_execution is None:
        return ()
    rows = _body_contract_rows(text, profile)
    if rows is None:
        return ()
    return tuple(tuple(row.items()) for row in rows)


def task_acceptance_rows(text: str, binding: object) -> list[dict[str, str]] | None:
    """Read the sole modern Task criterion verdict table."""

    section_name = getattr(binding, "criterion_acceptance_section", None)
    columns = getattr(binding, "criterion_acceptance_columns", ())
    if not section_name:
        return None
    section = _exact_heading_section(text, f"## {section_name}")
    table = _first_visible_table(section or "")
    if (
        table is None
        or tuple(table[0]) != columns
        or not table[1]
        or any(len(row) != len(table[0]) for row in table[1])
    ):
        return None
    return [dict(zip(table[0], row, strict=True)) for row in table[1]]


def task_evidence_rows(text: str, binding: object) -> list[dict[str, str]] | None:
    """Read a complete Task check table using its exact registry columns."""

    section_name = getattr(binding, "evidence_section", None)
    columns = getattr(binding, "evidence_columns", ())
    if not section_name:
        return None
    section = _exact_heading_section(text, f"## {section_name}")
    table = _first_visible_table(section or "")
    if (
        table is None
        or tuple(table[0]) != columns
        or not table[1]
        or any(len(row) != len(table[0]) for row in table[1])
    ):
        return None
    return [dict(zip(table[0], row, strict=True)) for row in table[1]]


def task_base_evidence_rows(text: str) -> list[dict[str, str]] | None:
    """Read Task evidence without changing its cells."""

    section = _exact_heading_section(text, "## Task Evidence")
    table = _first_visible_table(section or "")
    if (
        table is None
        or not table[1]
        or "Evidence" not in table[0]
        or any(len(row) != len(table[0]) for row in table[1])
    ):
        return None
    return [dict(zip(table[0], row, strict=True)) for row in table[1]]


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
    document_status = task_status(frontmatter_mapping(text), text, profile)

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
                    if (
                        contract.task_execution is not None
                        and identifier.column == "Upstream criterion"
                    ):
                        continue
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
            binding = contract.task_execution
            if binding is not None and binding.evidence_section:
                evidence_section = _exact_heading_section(
                    text, f"## {binding.evidence_section}"
                )
                evidence_table = _first_visible_table(evidence_section or "")
                if (
                    evidence_table is None
                    or tuple(evidence_table[0]) != binding.evidence_columns
                    or not evidence_table[1]
                    or any(
                        len(row) != len(evidence_table[0]) for row in evidence_table[1]
                    )
                ):
                    body_contract_valid = False
                else:
                    evidence_rows = [
                        dict(zip(evidence_table[0], row, strict=True))
                        for row in evidence_table[1]
                    ]
                    decision_rows = task_acceptance_rows(text, binding)
                    if decision_rows is None or task_contract_issues(
                        rows, evidence_rows, decision_rows, document_status, binding
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
        relationship_section_valid = required_headings_valid and allowed_headings_valid
        body_contract_valid = relationship_section_valid

    task_terminal_valid = True
    if profile.profile_id == "sdlc/task":
        binding = (
            profile.body_contract.task_execution if profile.body_contract else None
        )
        parsed_rows = [dict(row) for row in body_rows]
        task_terminal_valid = bool(
            binding
            and parsed_rows
            and not task_execution_issues(parsed_rows, document_status, binding)
            and body_contract_valid
            and document_status == "completed"
            and (
                (
                    len(parsed_rows) == 1
                    and parsed_rows[0]["Status"].strip() == "frontmatter"
                )
                or all(row["Status"].strip() == "completed" for row in parsed_rows)
            )
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


# Rendering depends only on the argument's text: neither this function nor the
# container renderer it calls reads an attribute off the value, and every
# returned line is a frozen record, so one result is safe to share. The bound
# holds the whole tracked Markdown corpus without retaining every transient
# fragment the block scans build.
@lru_cache(maxsize=1024)
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


def _body_contract_link_diagnostics(
    context: Context,
    profiles_by_id: dict[str, DocumentProfile],
    body_contracts: str,
    path_prefixes: tuple[PurePosixPath, ...] = (),
    *,
    selected_paths: frozenset[PurePosixPath] | None = None,
) -> list[Diagnostic]:
    """Validate registry-owned relationship cells."""

    if body_contracts not in {"registry", "audit"}:
        raise ConfigurationError("body_contracts must be registry or audit")
    diagnostics: list[Diagnostic] = []
    known_paths = set(context.paths)
    for path in context.paths:
        if selected_paths is not None and path not in selected_paths:
            continue
        view = context.profiles[path]
        profile = profiles_by_id.get(view.profile_id)
        if profile is None:
            continue
        status = task_status(
            context.metadata[path], context.texts.get(path, ""), profile
        )
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
                    if kind == "local" and target.is_relative_to(ARCHIVE_ROOT):
                        continue  # ADR-0053: links into the archive are unchecked.
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
    return sorted(diagnostics, key=diagnostic_sort_key)


def _owner_candidate(context: Context, path: PurePosixPath) -> bool:
    profile = context.profiles[path]
    status = str(context.metadata[path].get("status", "")).casefold()
    if profile.mode != "authored" or profile.profile_class in {"readme", "exception"}:
        return False
    if status not in {"active", "accepted"}:
        return False
    return not any(pattern.match(path.as_posix()) for pattern in OWNER_EXCLUSIONS)


def _traceability_lineage(context: Context, path: PurePosixPath) -> str:
    visible = _visible_markdown(context.texts[path])
    registry = context.current_registry or load_registry(context.root)
    profile_id = context.profiles[path].profile_id
    profile = next(
        (item for item in registry.profiles if item.profile_id == profile_id), None
    )
    relationship_section = (
        profile.body_contract.section if profile and profile.body_contract else None
    )
    section = (
        _exact_heading_section(context.texts[path], f"## {relationship_section}")
        if relationship_section
        else None
    )
    if section is not None:
        for raw in _extract_links(section, definitions_text=visible):
            kind, target = _local_destination(path, raw)
            if (
                kind == "local"
                and target is not None
                and (
                    re.fullmatch(
                        r"docs/01\.requirements/[0-9]{4}-[^/]+\.md", target.as_posix()
                    )
                    or re.fullmatch(
                        r"docs/03\.specs/[0-9]{4}-[^/]+/spec\.md", target.as_posix()
                    )
                )
            ):
                return _normalize_component(target.as_posix())
    value = path.as_posix()
    if re.fullmatch(r"docs/01\.requirements/[^/]+\.md", value):
        raw = path.stem
    elif re.fullmatch(r"docs/03\.specs/[^/]+/spec\.md", value):
        raw = path.parent.name
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


README_NAV_NESTED_TREE = re.compile(r"^(?:[│|] {2,3}| {4})+[├└]──", re.M)
README_NAV_CODE_SPAN = re.compile(r"(?<!`)(`{1,2})(?!`)([^`\n]+?)(?<!`)\1(?!`)")
README_NAV_FOLDER_LABEL = re.compile(r"\[([^\]\n]*)\]\(<?([^)\s>]+)>?")
# Code and emphasis markup around a label or header cell is not its text.
README_NAV_MARKUP = "`*_ "
README_NAV_TABLE_RULE = re.compile(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?")
README_NAV_HTML_HREF = re.compile(r"<a\s[^>]*?href\s*=\s*[\"']([^\"']+)[\"']", re.I)
REGULAR_MODES = frozenset({"100644", "100755"})


@dataclass(frozen=True)
class ReadmeSource:
    profile_id: str
    text: str


@dataclass(frozen=True)
class TrackedTree:
    """Stage-0 index entries by mode, plus every folder they imply."""

    modes: Mapping[PurePosixPath, str]
    folders: frozenset[PurePosixPath]

    @classmethod
    def from_modes(cls, modes: Mapping[PurePosixPath, str]) -> "TrackedTree":
        folders = {
            parent
            for path in modes
            for parent in path.parents
            if parent != PurePosixPath(".")
        }
        return cls(dict(modes), frozenset(folders))

    def kind(self, path: PurePosixPath) -> str | None:
        if path in self.folders:
            return "folder"
        mode = self.modes.get(path)
        if mode is None:
            return None
        return "file" if mode in REGULAR_MODES else "leaf"

    def children(
        self, folder: PurePosixPath, placeholders: frozenset[str]
    ) -> dict[str, str]:
        prefix = "" if folder == PurePosixPath(".") else f"{folder.as_posix()}/"
        found: dict[str, str] = {}
        for path in self.modes:
            value = path.as_posix()
            if not value.startswith(prefix):
                continue
            head, separator, _ = value[len(prefix) :].partition("/")
            if not separator and head in placeholders:
                continue
            found[head] = "folder" if separator else self.kind(path) or "file"
        return found


def _readme_visible_lines(text: str) -> tuple[list[str], list[str]]:
    """Split Markdown into lines outside fences and the fenced block bodies."""

    visible: list[str] = []
    blocks: list[str] = []
    fence: str | None = None
    body: list[str] = []
    for line in text.split("\n"):
        opener = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is None and opener:
            fence, body = opener.group(1), []
            visible.append("")
            continue
        if fence is not None:
            if line.strip().startswith(fence):
                blocks.append("\n".join(body))
                fence = None
            else:
                body.append(line)
            visible.append("")
            continue
        visible.append(line)
    return visible, blocks


def _readme_section(text: str, heading: str) -> str:
    visible, _ = _readme_visible_lines(text)
    chosen: list[str] = []
    inside = False
    for raw, line in zip(text.split("\n"), visible):
        match = re.match(r"^(#{1,2})\s+(.+?)\s*#*\s*$", line)
        if match:
            inside = len(match.group(1)) == 2 and match.group(2) == heading
            continue
        if inside:
            chosen.append(raw)
    return "\n".join(chosen)


def _readme_targets(
    source: PurePosixPath, markdown: str, definitions: str
) -> list[tuple[str, PurePosixPath]]:
    # The canonical extractor masks inline HTML; a listing hidden in raw HTML
    # anchors still lists children, so their href values count here too.
    visible, _ = _readme_visible_lines(markdown)
    hrefs = README_NAV_HTML_HREF.findall("\n".join(visible))
    found = []
    for raw in (*_extract_links(markdown, definitions_text=definitions), *hrefs):
        kind, target = _local_destination(source, raw)
        if kind == "local" and target is not None:
            found.append((raw, target))
    return found


def _readme_relative(
    folder: PurePosixPath, target: PurePosixPath
) -> tuple[str, ...] | None:
    if folder == PurePosixPath("."):
        return target.parts
    try:
        return target.relative_to(folder).parts
    except ValueError:
        return None


def _readme_is_deep(parts: tuple[str, ...]) -> bool:
    return len(parts) > 1 and not (len(parts) == 2 and parts[1] == "README.md")


def _readme_table_headers(markdown: str) -> list[frozenset[str]]:
    headers: list[frozenset[str]] = []
    previous = ""
    for line in markdown.split("\n"):
        stripped = line.strip()
        if previous.startswith("|") and README_NAV_TABLE_RULE.fullmatch(stripped):
            headers.append(
                frozenset(
                    cell.strip(README_NAV_MARKUP)
                    for cell in previous.strip("|").split("|")
                )
            )
        previous = stripped
    return headers


def _readme_findings(
    path: PurePosixPath,
    source: ReadmeSource,
    rule: Any,
    navigation: Any,
    tree: TrackedTree,
) -> list[Diagnostic]:
    folder = path.parent
    text = source.text
    visible, blocks = _readme_visible_lines(text)
    section = _readme_section(text, rule.section)
    found: list[Diagnostic] = []

    def report(code: str, expected: str, actual: str) -> None:
        found.append(_diag(code, path, source.profile_id, expected, actual))

    section_targets = _readme_targets(path, section, text)
    for raw, target in section_targets:
        parts = _readme_relative(folder, target)
        if parts and _readme_is_deep(parts):
            report(
                "README-NAV-DEPTH",
                "navigation links reach direct children",
                f"{raw} reaches {'/'.join(parts)}",
            )
    for block in blocks:
        if "──" in block and README_NAV_NESTED_TREE.search(block):
            report(
                "README-NAV-TREE",
                "a fenced tree of direct children",
                "a fenced tree nests below the first level",
            )
    for label, raw in README_NAV_FOLDER_LABEL.findall("\n".join(visible)):
        if not label.strip(README_NAV_MARKUP).endswith("/"):
            continue
        kind, target = _local_destination(path, raw)
        if kind == "local" and target is not None and tree.kind(target) != "folder":
            report(
                "README-NAV-LABEL",
                f"label {label} resolves to a folder",
                f"{raw} is not a folder",
            )
    deep: dict[str, set[str]] = collections.defaultdict(set)
    for _, target in _readme_targets(path, text, text):
        parts = _readme_relative(folder, target)
        if parts and _readme_is_deep(parts):
            deep[parts[0]].add("/".join(parts))
    scoped = [section, *(line for line in visible if line.lstrip().startswith("|"))]
    for chunk in scoped:
        for _, value in README_NAV_CODE_SPAN.findall(chunk):
            value = value.strip().rstrip("/")
            if not value or " " in value or value.startswith(("/", "-", "~")):
                continue
            # Inside the navigation section a span may name its path from the
            # repository root; elsewhere root paths cite contract evidence.
            bases = (folder, PurePosixPath(".")) if chunk is section else (folder,)
            for base in bases:
                candidate = PurePosixPath(posixpath.normpath((base / value).as_posix()))
                parts = _readme_relative(folder, candidate)
                if tree.kind(candidate) is not None and parts:
                    if _readme_is_deep(parts):
                        deep[parts[0]].add("/".join(parts))
                    break
    for child, targets in sorted(deep.items()):
        if len(targets) > navigation.max_deep_links_per_child:
            report(
                "README-NAV-ENUMERATION",
                f"at most {navigation.max_deep_links_per_child} deep target in {child}/",
                f"{len(targets)} targets: {', '.join(sorted(targets)[:4])}",
            )
    if rule.complete:
        reached = {
            parts[0]
            for _, target in section_targets
            if (parts := _readme_relative(folder, target))
        }
        for child, kind in sorted(
            tree.children(folder, navigation.placeholders).items()
        ):
            if (kind == "folder" or child.endswith(".md")) and child not in reached:
                report(
                    "README-NAV-COMPLETE",
                    f"{rule.section} reaches {child}",
                    f"{child} is unreachable",
                )
    for header in _readme_table_headers(section):
        banned = sorted(header & navigation.forbidden_index_columns)
        if banned:
            report(
                "README-NAV-COPY",
                "no copied status or date columns",
                ", ".join(banned),
            )
    return found


def readme_navigation_diagnostics(
    navigation: Any,
    readmes: Mapping[PurePosixPath, ReadmeSource],
    tree: TrackedTree,
) -> list[Diagnostic]:
    """SPEC-0091: each README lists only its direct children."""

    diagnostics: list[Diagnostic] = []
    for path, source in sorted(readmes.items(), key=lambda item: item[0].as_posix()):
        if path in navigation.exempt_paths:
            continue
        rule = navigation.profiles.get(source.profile_id)
        if rule is None:
            if path in navigation.pending_paths:
                diagnostics.append(
                    _diag(
                        "README-NAV-PENDING",
                        path,
                        source.profile_id,
                        "a pending README with a navigation profile",
                        "its profile has no navigation entry",
                    )
                )
            continue
        found = _readme_findings(path, source, rule, navigation, tree)
        if path in navigation.pending_paths:
            if not found:
                diagnostics.append(
                    _diag(
                        "README-NAV-PENDING",
                        path,
                        source.profile_id,
                        "a pending README that still violates the contract",
                        "it passes; remove it from pending_paths",
                    )
                )
            continue
        diagnostics.extend(found)
    for exempt in sorted(navigation.exempt_paths, key=PurePosixPath.as_posix):
        if tree.kind(exempt) is None:
            diagnostics.append(
                _diag(
                    "README-NAV-EXEMPT",
                    exempt,
                    "",
                    "a tracked README",
                    "exempt path is not tracked",
                )
            )
    for pending in sorted(navigation.pending_paths, key=PurePosixPath.as_posix):
        if tree.kind(pending) is None:
            diagnostics.append(
                _diag(
                    "README-NAV-PENDING",
                    pending,
                    "",
                    "a tracked README",
                    "pending path is not tracked",
                )
            )
    return diagnostics


def _readme_navigation_diagnostics(context: Context) -> list[Diagnostic]:
    navigation = getattr(context, "readme_navigation", None)
    if navigation is None:
        registry = (
            context.document_registry
            or context.current_registry
            or load_registry(context.root)
        )
        navigation = getattr(registry, "readme_navigation", None)
    if navigation is None:
        return []
    readmes = {
        path: ReadmeSource(context.profiles[path].profile_id, context.texts[path])
        for path in context.paths
        if path.name == "README.md" and path in context.texts
    }
    modes = context.tracked_modes
    if modes is None:
        modes = {
            entry.path: entry.mode
            for entry in _parse_ls_files_stage_z(
                _run_git(context.root, ("ls-files", "--stage", "-z"))
            )
            if entry.stage == 0
        }
    return readme_navigation_diagnostics(
        navigation, readmes, TrackedTree.from_modes(modes)
    )


def _governance_current_owner_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not context.governance_current_paths:
        return diagnostics
    declared = set(context.governance_current_paths)
    allowed = set(context.governance_current_states)
    for path in context.governance_current_paths:
        if path not in context.paths:
            diagnostics.append(
                _diag(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
                    path,
                    "governance",
                    "declared tracked common governance document",
                    "declared path is missing",
                )
            )
            continue
        profile = context.profiles[path]
        if profile.profile_class != "governance" or profile.mode != "authored":
            diagnostics.append(
                _diag(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",
                    path,
                    profile.profile_id,
                    "authored common governance profile",
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
        if profile.profile_class != "governance" or profile.mode != "authored":
            continue
        status = str(context.metadata[path].get("status", "")).casefold()
        if status in allowed and path not in declared:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-OWNER-UNDECLARED",
                    path,
                    profile.profile_id,
                    "active or accepted common authority declared in the registry",
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
                    f"undeclared {status} document in the current common authority route",
                )
            )

    return diagnostics


def _body_link_scope(
    context: Context,
    changed_paths: Sequence[str],
    registry: Registry,
) -> frozenset[PurePosixPath] | None:
    """Bound body-row checks to changed documents and direct inbound users.

    The ordinary link, parent, README, governance and owner graphs remain
    global. This one-hop closure does not recursively pull in router hubs.
    """

    selected = scoped_document_content_paths(registry, changed_paths, context.paths)
    if selected is None:
        return None
    changed = frozenset(PurePosixPath(raw) for raw in changed_paths)
    affected = set(selected)
    for source in context.paths:
        profile = context.profiles[source]
        parent = direct_parent(source, profile.profile_id)
        if parent is not None and parent[0] in changed:
            affected.add(source)
        if source in changed and parent is not None:
            affected.add(parent[0])
        for raw_link in _extract_links(context.texts[source]):
            kind, target = _local_destination(
                source, raw_link, template=profile.mode == "template"
            )
            if kind in {"local", "anchor"} and target in changed:
                affected.add(source)
                break
    return frozenset(affected)


def _raw_diagnostics(
    context: Context,
    profiles_by_id: dict[str, DocumentProfile],
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
    *,
    selected_body_paths: frozenset[PurePosixPath] | None = None,
) -> list[Diagnostic]:
    diagnostics = _link_diagnostics(context)
    for path in context.paths:
        parent = direct_parent(path, context.profiles[path].profile_id)
        if parent is None:
            continue
        target, identifier = parent
        if (
            context.metadata[path].get("parent_ids") != [identifier]
            or context.metadata.get(target, {}).get("artifact_id") != identifier
        ):
            diagnostics.append(
                _diag(
                    "PARENT-IDENTITY",
                    path,
                    context.profiles[path].profile_id,
                    f"one direct parent {target.as_posix()} with identity {identifier}",
                    "parent missing or inconsistent",
                )
            )
    diagnostics.extend(
        _body_contract_link_diagnostics(
            context,
            profiles_by_id,
            body_contracts,
            body_contract_path_prefixes,
            selected_paths=selected_body_paths,
        )
    )
    diagnostics.extend(_readme_navigation_diagnostics(context))
    diagnostics.extend(_governance_current_owner_diagnostics(context))
    diagnostics.extend(_owner_diagnostics(context))
    return sorted(diagnostics, key=diagnostic_sort_key)


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
    parser.add_argument("--mode", choices=("strict",), default="strict")
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
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--include-path", action="append", default=[])
    parser.add_argument("--change-scope", action="store_true")
    parser.add_argument("--changed-path", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.change_scope != bool(args.changed_path):
            raise ConfigurationError(
                "--change-scope requires one or more --changed-path values"
            )
        if args.change_scope and (
            args.body_contracts == "audit" or args.body_contract_path_prefix
        ):
            raise ConfigurationError(
                "explicit body-contract audit cannot use change scope"
            )
        if args.inventory and args.change_scope:
            raise ConfigurationError("inventory cannot use change scope")
        if args.change_scope:
            validated_changed_paths(args.changed_path)
        if args.inventory and args.format != "json":
            raise ConfigurationError("--inventory requires --format json")
        include_paths = tuple(PurePosixPath(value) for value in args.include_path)
        context = _build_context(args.root, include_paths)
        registry = context.current_registry or load_registry(context.root)
        profiles_by_id = {profile.profile_id: profile for profile in registry.profiles}
        inventory = context.current_inventory or enumerate_target_markdown(
            context.root, include_paths=include_paths
        )
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
                + _readme_navigation_diagnostics(context)
                + _governance_current_owner_diagnostics(context)
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
        selected_body_paths = (
            _body_link_scope(context, args.changed_path, registry)
            if args.change_scope
            else None
        )
        diagnostics = _raw_diagnostics(
            context,
            profiles_by_id,
            args.body_contracts,
            tuple(args.body_contract_path_prefix),
            selected_body_paths=selected_body_paths,
        )
        rows = [("FAIL", item) for item in sorted(diagnostics, key=diagnostic_sort_key)]
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
