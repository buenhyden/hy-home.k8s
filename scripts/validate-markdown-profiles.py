#!/usr/bin/env python3
"""Validate registry-selected Markdown document profiles."""

from __future__ import annotations

import argparse
import collections
import contextlib
import copy
import dataclasses
import datetime as dt
import io
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Sequence
from zoneinfo import ZoneInfo

import yaml

from document_contracts import (
    REGISTRY_PATH,
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    classify_path,
    diagnostic_sort_key,
    enumerate_target_markdown,
    load_registry,
    read_repository_text,
    validate_registry,
)


FIXTURE_PATH = Path("tests/fixtures/markdown-profiles.json")
README_FIXTURE_PATH = Path(
    "tests/fixtures/document-contracts/readme-profile-cases.json"
)
EXPECTED_README_CASES = (
    "valid-profile",
    "frontmatter-forbidden",
    "duplicate-h1",
    "duplicate-h2",
    "unsupported-h2",
    "missing-required-h2",
    "fenced-heading-ignored",
    "unclosed-fence",
)
COMPATIBILITY_PATH = Path(
    "tests/fixtures/document-contracts/template-compatibility.json"
)
OWNER = "markdown-profile-validator"
AUTHOR_PROMPT_MARKER = "Author prompt:"
AUTHOR_PROMPT_COMMENT = re.compile(r"(?m)^[ \t]*<!-- Author prompt:")
GENERIC_RESIDUE = (
    "Target: docs/",
    "Use this template",
    "Replace every placeholder with researched, topic-specific content.",
)
STARTER_PLACEHOLDER = re.compile(
    r"\[[^\]\n]+\]|\{[^}\n]+\}|<[^>\n]+>|#{3,}"
)
TOKEN_BEARING_DEBT_RULES = frozenset(
    {
        "BODY-H2-DUPLICATE",
        "BODY-HEADING-REQUIRED",
        "BODY-HEADING-UNSUPPORTED",
        "BODY-TEMPLATE-RESIDUE",
    }
)
IMPLEMENTED_RULE_IDS = frozenset(
    {
        "APPEND-CONTEXT",
        "APPEND-ENTRY-LEVEL",
        "APPEND-PARENT-H2",
        "APPEND-PARENT-PROFILE",
        "APPEND-SECTION-LEVEL",
        "APPEND-SECTION-REQUIRED",
        "BODY-AUTHOR-PROMPT",
        "BODY-CONTRACT-CELL",
        "BODY-CONTRACT-COLUMNS",
        "BODY-CONTRACT-COLUMN-DUPLICATE",
        "BODY-CONTRACT-EXCLUSION",
        "BODY-CONTRACT-HEADING",
        "BODY-CONTRACT-IDENTIFIER",
        "BODY-CONTRACT-TABLE",
        "BODY-FENCE-UNCLOSED",
        "BODY-H1",
        "BODY-H1-PLACEHOLDER",
        "BODY-H2-DUPLICATE",
        "BODY-HEADING-EMPTY",
        "BODY-HEADING-REQUIRED",
        "BODY-HEADING-UNSUPPORTED",
        "BODY-TEMPLATE-RESIDUE",
        "FM-DATE",
        "FM-DELIMITER",
        "FM-DUPLICATE-KEY",
        "FM-FORBIDDEN",
        "FM-FUTURE-DATE",
        "FM-KEY-ORDER",
        "FM-KEYSET",
        "FM-OWNER",
        "FM-STATUS",
        "FM-TITLE",
        "FM-TITLE-PLACEHOLDER",
        "FM-TYPE",
        "README_FENCE",
        "README_FRONTMATTER",
        "README_H1",
        "README_H2_DUPLICATE",
        "README_H2_REQUIRED",
        "README_H2_UNSUPPORTED",
    }
)


class ContractError(ValueError):
    """One deterministic Markdown preprocessing failure."""

    def __init__(self, rule_id: str, detail: str):
        self.rule_id = rule_id
        self.detail = detail
        super().__init__(detail)


class DuplicateKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


DuplicateKeyLoader.yaml_implicit_resolvers = copy.deepcopy(
    yaml.SafeLoader.yaml_implicit_resolvers
)
for _resolver_key, _resolvers in DuplicateKeyLoader.yaml_implicit_resolvers.items():
    DuplicateKeyLoader.yaml_implicit_resolvers[_resolver_key] = [
        resolver
        for resolver in _resolvers
        if resolver[0] != "tag:yaml.org,2002:timestamp"
    ]


def _construct_mapping(
    loader: DuplicateKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ContractError("FM-DUPLICATE-KEY", str(key))
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


DuplicateKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def extract_frontmatter(text: str) -> tuple[list[str], dict[str, object], str]:
    """Extract an exact leading YAML mapping without losing key order."""

    if not text.startswith("---\n"):
        raise ContractError("FM-DELIMITER", "first line must be ---")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ContractError("FM-DELIMITER", "frontmatter is not closed")
    raw = text[4:closing]
    try:
        data = yaml.load(raw, Loader=DuplicateKeyLoader) or {}
    except ContractError:
        raise
    except yaml.YAMLError as exc:
        raise ContractError("FM-KEYSET", "frontmatter YAML is invalid") from exc
    if not isinstance(data, dict):
        raise ContractError("FM-KEYSET", "frontmatter must be a mapping")
    if not all(isinstance(key, str) for key in data):
        raise ContractError("FM-KEYSET", "frontmatter keys must be strings")
    return list(data.keys()), data, text[closing + 5 :]


@dataclass(frozen=True)
class HeadingScan:
    headings: tuple[tuple[int, str], ...]
    unclosed_fence: bool


def _strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    visible: list[str] = []
    cursor = 0
    while cursor < len(line):
        if in_comment:
            end = line.find("-->", cursor)
            if end < 0:
                return "".join(visible), True
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
    return "".join(visible), in_comment


def scan_headings(markdown: str) -> HeadingScan:
    """Scan ATX headings outside CommonMark-compatible fenced blocks."""

    headings: list[tuple[int, str]] = []
    fence_character: str | None = None
    fence_length = 0
    in_comment = False
    opening = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
    for raw_line in markdown.splitlines():
        if fence_character is not None:
            closing = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[ \t]*$"
            )
            if closing.fullmatch(raw_line):
                fence_character = None
                fence_length = 0
            continue
        line, in_comment = _strip_html_comments(raw_line, in_comment)
        match = opening.match(line)
        if match:
            marker = match.group(1)
            if marker[0] == "`" and "`" in match.group(2):
                continue
            fence_character = marker[0]
            fence_length = len(marker)
            continue
        match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
        if not match:
            continue
        title = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(2).strip()).strip()
        headings.append((len(match.group(1)), title))
    return HeadingScan(tuple(headings), fence_character is not None)


def text_outside_fenced_code(markdown: str) -> str:
    """Return source outside fenced blocks while preserving HTML comments."""

    visible: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    in_comment = False
    opening = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
    for raw_line in markdown.splitlines():
        if fence_character is not None:
            closing = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[ \t]*$"
            )
            if closing.fullmatch(raw_line):
                fence_character = None
                fence_length = 0
            visible.append("")
            continue
        line, in_comment = _strip_html_comments(raw_line, in_comment)
        match = opening.match(line)
        if match:
            marker = match.group(1)
            if marker[0] == "`" and "`" in match.group(2):
                visible.append(raw_line)
                continue
            fence_character = marker[0]
            fence_length = len(marker)
            visible.append("")
            continue
        visible.append(raw_line)
    return "\n".join(visible)


def _visible_markdown(markdown: str) -> str:
    """Hide fenced code and HTML comments while retaining line positions."""

    visible: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    in_comment = False
    opening = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
    for raw_line in markdown.splitlines():
        if fence_character is not None:
            closing = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[ \t]*$"
            )
            if closing.fullmatch(raw_line):
                fence_character = None
                fence_length = 0
            visible.append("")
            continue
        line, in_comment = _strip_html_comments(raw_line, in_comment)
        match = opening.match(line)
        if match:
            marker = match.group(1)
            if marker[0] == "`" and "`" in match.group(2):
                visible.append(line)
                continue
            fence_character = marker[0]
            fence_length = len(marker)
            visible.append("")
            continue
        visible.append(line)
    return "\n".join(visible)


def _gfm_table_cells(line: str) -> list[str]:
    """Split one pipe-led GFM table row, preserving escaped pipes."""

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
    """Return the sole exact heading section outside comments and fences."""

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


def _first_visible_table(
    text: str,
) -> tuple[list[str], list[list[str]]] | None:
    """Return the first valid pipe-led GFM table outside comments and fences."""

    lines = _visible_markdown(text).splitlines()
    for index in range(len(lines) - 1):
        if re.match(r"^ {0,3}\|", lines[index]) is None:
            continue
        header = _gfm_table_cells(lines[index])
        delimiter = _gfm_table_cells(lines[index + 1])
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
            rows.append(_gfm_table_cells(row_line))
        return header, rows
    return None


IDENTIFIER_PATTERNS = {
    "requirement": re.compile(r"^REQ-[A-Z0-9-]+-[0-9]{2,3}$"),
    "criterion": re.compile(r"^VAL-[A-Z0-9-]+-[0-9]{3}$"),
    "work-item": re.compile(r"^[A-Z][A-Z0-9-]+-[0-9]{3}$"),
}
EXPLICIT_EXCLUSION = re.compile(r"^N/A — \S(?:.*\S)?$")


def _identifier_text(cell: str) -> str:
    """Return a visible identifier from a plain, code, or full-link cell."""

    value = cell.strip()
    link = re.fullmatch(r"\[([^\]\n]+)\]\([^\n)]+\)", value)
    if link:
        value = link.group(1).strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


def _body_contract_is_enforced(
    path: PurePosixPath,
    profile: DocumentProfile,
    status: str,
    body_contracts: str,
    path_prefixes: tuple[PurePosixPath, ...],
) -> bool:
    if body_contracts not in {"registry", "audit"}:
        raise ValueError("body_contracts must be registry or audit")
    if profile.body_contract is None:
        return False
    if profile.mode == "template":
        return True
    if profile.mode != "authored":
        return False
    if body_contracts == "audit":
        in_scope = not path_prefixes or any(
            path == prefix or prefix in path.parents
            for prefix in path_prefixes
        )
        return in_scope and status in {"draft", "active"}
    return status in profile.body_contract.enforced_statuses


def _body_contract_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    body: str,
    status: str,
    body_contracts: str,
    path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Validate one registry-owned lifecycle table deterministically."""

    contract = profile.body_contract
    if contract is None or not _body_contract_is_enforced(
        path, profile, status, body_contracts, path_prefixes
    ):
        return []
    diagnostics: list[Diagnostic] = []
    section = _exact_heading_section(body, f"## {contract.section}")
    table_section = (
        None
        if section is None
        else _exact_heading_section(section, f"### {contract.table_heading}")
    )
    if table_section is None:
        return [
            _diagnostic(
                "BODY-CONTRACT-HEADING",
                path,
                profile,
                f"one exact H3 '{contract.table_heading}' inside H2 '{contract.section}'",
                "missing, duplicated, or at the wrong level",
            )
        ]
    table = _first_visible_table(table_section)
    if table is None or not table[1]:
        return [
            _diagnostic(
                "BODY-CONTRACT-TABLE",
                path,
                profile,
                "one non-empty GFM table below the contract H3",
                "missing or malformed table",
            )
        ]
    header, rows = table
    duplicate_columns = sorted(
        column
        for column, count in collections.Counter(header).items()
        if count > 1
    )
    if duplicate_columns:
        return [
            _diagnostic(
                "BODY-CONTRACT-COLUMN-DUPLICATE",
                path,
                profile,
                "unique table headers",
                json.dumps(duplicate_columns),
            )
        ]
    if tuple(header) != contract.required_columns:
        return [
            _diagnostic(
                "BODY-CONTRACT-COLUMNS",
                path,
                profile,
                json.dumps(contract.required_columns),
                json.dumps(header),
            )
        ]
    column_indexes = {column: index for index, column in enumerate(header)}
    for row_index, row in enumerate(rows, start=1):
        normalized = row + [""] * max(0, len(header) - len(row))
        normalized = normalized[: len(header)]
        for column_index, value in enumerate(normalized):
            if not value.strip():
                diagnostics.append(
                    _diagnostic(
                        "BODY-CONTRACT-CELL",
                        path,
                        profile,
                        "every required table cell is non-empty",
                        f"row {row_index}, column {header[column_index]}",
                    )
                )
        for identifier in contract.identifier_columns:
            value = _identifier_text(normalized[column_indexes[identifier.column]])
            if value.startswith("N/A"):
                if (
                    not contract.allow_explicit_exclusion
                    or EXPLICIT_EXCLUSION.fullmatch(value) is None
                ):
                    diagnostics.append(
                        _diagnostic(
                            "BODY-CONTRACT-EXCLUSION",
                            path,
                            profile,
                            "N/A — followed by a reviewable reason",
                            value,
                        )
                    )
                continue
            pattern = IDENTIFIER_PATTERNS[identifier.kind]
            if pattern.fullmatch(value) is None:
                diagnostics.append(
                    _diagnostic(
                        "BODY-CONTRACT-IDENTIFIER",
                        path,
                        profile,
                        f"{identifier.kind} identifier matching {pattern.pattern}",
                        value,
                    )
                )
    return sorted(diagnostics, key=diagnostic_sort_key)


def starter_placeholder(value: str) -> str | None:
    """Return one unresolved starter token from a title or H1."""

    match = STARTER_PLACEHOLDER.search(value)
    return match.group(0) if match else None


def empty_required_h2_sections(
    markdown: str, required_headings: Sequence[str]
) -> tuple[str, ...]:
    """Return required H2 occurrences whose authored section body is empty.

    Blank lines, fence delimiters, and author-only HTML comments do not count
    as content. Content inside a fenced block does count, while headings inside
    that block do not open or close sections.
    """

    required = frozenset(required_headings)
    empty: list[str] = []
    current_heading: str | None = None
    current_has_content = False
    fence_character: str | None = None
    fence_length = 0
    in_comment = False
    opening = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")

    def close_current() -> None:
        nonlocal current_heading, current_has_content
        if current_heading is not None and not current_has_content:
            empty.append(current_heading)
        current_heading = None
        current_has_content = False

    for raw_line in markdown.splitlines():
        if fence_character is not None:
            closing = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[ \t]*$"
            )
            if closing.fullmatch(raw_line):
                fence_character = None
                fence_length = 0
            elif current_heading is not None and raw_line.strip():
                current_has_content = True
            continue

        line, in_comment = _strip_html_comments(raw_line, in_comment)
        match = opening.match(line)
        if match:
            marker = match.group(1)
            if marker[0] == "`" and "`" in match.group(2):
                if current_heading is not None and line.strip():
                    current_has_content = True
                continue
            fence_character = marker[0]
            fence_length = len(marker)
            continue

        heading_match = re.match(
            r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line
        )
        if heading_match:
            level = len(heading_match.group(1))
            title = re.sub(
                r"[ \t]+#+[ \t]*$", "", heading_match.group(2).strip()
            ).strip()
            if level <= 2:
                close_current()
                if level == 2 and title in required:
                    current_heading = title
            elif current_heading is not None:
                current_has_content = True
            continue

        if current_heading is not None and line.strip():
            current_has_content = True

    close_current()
    return tuple(empty)


def _diagnostic(
    rule_id: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    expected: str,
    actual: str,
) -> Diagnostic:
    return Diagnostic(rule_id, path, profile.profile_id, expected, actual, OWNER)


def _expected_type(profile: DocumentProfile) -> str:
    if profile.mode == "template" and profile.source_profile_ids:
        return profile.source_profile_ids[0]
    return profile.profile_id


def _date_text(value: object) -> str | None:
    if isinstance(value, dt.datetime):
        return None
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, str):
        return value
    return None


def _validate_date(
    diagnostics: list[Diagnostic],
    path: PurePosixPath,
    profile: DocumentProfile,
    key: str,
    value: object,
    today: dt.date,
) -> None:
    text = _date_text(value)
    if profile.mode == "template" and text == "YYYY-MM-DD":
        return
    try:
        parsed = dt.date.fromisoformat(text or "")
    except ValueError:
        diagnostics.append(
            _diagnostic("FM-DATE", path, profile, f"{key} is an ISO calendar date", text or type(value).__name__)
        )
        return
    if profile.mode == "authored" and parsed > today:
        diagnostics.append(
            _diagnostic("FM-FUTURE-DATE", path, profile, f"{key} is not future-dated", parsed.isoformat())
        )


def _frontmatter_body(
    text: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    diagnostics: list[Diagnostic],
    today: dt.date,
) -> str:
    contract = profile.frontmatter
    if contract.mode == "not-applicable":
        return text
    if contract.mode == "forbidden":
        if text.startswith("---\n"):
            rule = "README_FRONTMATTER" if profile.profile_class == "readme" else "FM-FORBIDDEN"
            diagnostics.append(_diagnostic(rule, path, profile, "frontmatter is forbidden", "frontmatter"))
            try:
                _, _, body = extract_frontmatter(text)
                return body
            except ContractError:
                return text
        return text
    try:
        keys, data, body = extract_frontmatter(text)
    except ContractError as exc:
        diagnostics.append(_diagnostic(exc.rule_id, path, profile, exc.detail, "frontmatter" if exc.rule_id == "FM-DELIMITER" else exc.detail))
        return text

    required = tuple(contract.required)
    allowed = tuple(contract.allowed)
    missing = [key for key in required if key not in data]
    extra = [key for key in keys if key not in allowed]
    if missing or extra:
        diagnostics.append(
            _diagnostic("FM-KEYSET", path, profile, json.dumps({"required": required, "allowed": allowed}), json.dumps({"missing": missing, "extra": extra}))
        )
    elif tuple(keys) != contract.order:
        diagnostics.append(
            _diagnostic("FM-KEY-ORDER", path, profile, json.dumps(contract.order), json.dumps(keys))
        )

    expected_type = _expected_type(profile)
    if "type" in data and data["type"] != expected_type:
        diagnostics.append(_diagnostic("FM-TYPE", path, profile, expected_type, str(data["type"])))
    if "status" in data and data["status"] not in profile.status_domain:
        diagnostics.append(_diagnostic("FM-STATUS", path, profile, json.dumps(profile.status_domain), str(data["status"])))
    if "owner" in data and data["owner"] != "platform":
        diagnostics.append(_diagnostic("FM-OWNER", path, profile, "platform", str(data["owner"])))
    if "title" in data and (not isinstance(data["title"], str) or not data["title"].strip()):
        diagnostics.append(_diagnostic("FM-TITLE", path, profile, "a non-empty string", type(data["title"]).__name__ if not isinstance(data["title"], str) else "empty"))
    elif (
        "title" in data
        and profile.placeholder_policy == "forbidden"
        and isinstance(data["title"], str)
        and (placeholder := starter_placeholder(data["title"])) is not None
    ):
        diagnostics.append(
            _diagnostic(
                "FM-TITLE-PLACEHOLDER",
                path,
                profile,
                "a topic-specific title without starter delimiters",
                placeholder,
            )
        )
    if "updated" in data:
        _validate_date(diagnostics, path, profile, "updated", data["updated"], today)
    if "archived_on" in data:
        _validate_date(
            diagnostics, path, profile, "archived_on", data["archived_on"], today
        )
    return body


def _append_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    scan: HeadingScan,
    append_context: AppendContext | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    contract = profile.append_contract
    if contract is None:
        return diagnostics
    if append_context is None:
        diagnostics.append(_diagnostic("APPEND-CONTEXT", path, profile, "an explicit parent context", "missing"))
    else:
        if append_context.parent_profile.profile_id != contract.parent_profile_id:
            diagnostics.append(_diagnostic("APPEND-PARENT-PROFILE", path, profile, contract.parent_profile_id, append_context.parent_profile.profile_id))
        if append_context.parent_h2 != contract.parent_h2:
            diagnostics.append(_diagnostic("APPEND-PARENT-H2", path, profile, contract.parent_h2, append_context.parent_h2))
    h3 = [
        title
        for level, title in scan.headings
        if level == contract.entry_heading_level
        and title not in contract.required_sections
    ]
    h4 = [title for level, title in scan.headings if level == contract.section_heading_level]
    if len(h3) != 1:
        diagnostics.append(_diagnostic("APPEND-ENTRY-LEVEL", path, profile, "exactly one H3 entry heading", json.dumps(h3)))
    seen_any_level = {title for _, title in scan.headings}
    missing = [
        section
        for section in contract.required_sections
        if section not in h4 and section not in seen_any_level
    ]
    if missing:
        diagnostics.extend(_diagnostic("APPEND-SECTION-REQUIRED", path, profile, "required H4 section", section) for section in missing)
    wrong_levels = [title for level, title in scan.headings if title in contract.required_sections and level != contract.section_heading_level]
    if wrong_levels:
        diagnostics.extend(_diagnostic("APPEND-SECTION-LEVEL", path, profile, "required sections use H4", title) for title in wrong_levels)
    return diagnostics


def _body_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    body: str,
    append_context: AppendContext | None,
) -> list[Diagnostic]:
    if profile.profile_id == "governance/progress-ledger":
        body = body.split("\n## Historical Entries\n", 1)[0]
    scan = scan_headings(body)
    if profile.append_contract is not None:
        diagnostics = _append_diagnostics(path, profile, scan, append_context)
        if scan.unclosed_fence:
            diagnostics.append(_diagnostic("BODY-FENCE-UNCLOSED", path, profile, "all fenced blocks are closed", "unclosed"))
        return diagnostics
    if profile.frontmatter.mode == "not-applicable" and not profile.headings.required and not profile.headings.allowed:
        return []
    readme = profile.profile_class == "readme"
    diagnostics: list[Diagnostic] = []
    if scan.unclosed_fence:
        rule = "README_FENCE" if readme else "BODY-FENCE-UNCLOSED"
        diagnostics.append(_diagnostic(rule, path, profile, "all fenced blocks are closed", "unclosed"))
    if not profile.headings.required and not profile.headings.allowed:
        return diagnostics
    h1 = [title for level, title in scan.headings if level == 1]
    h2 = [title for level, title in scan.headings if level == 2]
    if len(h1) != 1:
        rule = "README_H1" if readme else "BODY-H1"
        diagnostics.append(_diagnostic(rule, path, profile, "exactly one H1", json.dumps(h1)))
    elif (
        profile.placeholder_policy == "forbidden"
        and (placeholder := starter_placeholder(h1[0])) is not None
    ):
        diagnostics.append(
            _diagnostic(
                "BODY-H1-PLACEHOLDER",
                path,
                profile,
                "a topic-specific H1 without starter delimiters",
                placeholder,
            )
        )
    missing = [heading for heading in profile.headings.required if heading not in h2]
    required_rule = "README_H2_REQUIRED" if readme else "BODY-HEADING-REQUIRED"
    diagnostics.extend(_diagnostic(required_rule, path, profile, "required H2", heading) for heading in missing)
    if profile.mode == "authored":
        h2_counts = collections.Counter(h2)
        diagnostics.extend(
            _diagnostic(
                "BODY-HEADING-EMPTY",
                path,
                profile,
                "required H2 contains authored body content",
                heading,
            )
            for heading in empty_required_h2_sections(
                body, profile.headings.required
            )
            if h2_counts[heading] == 1
        )
    duplicate = sorted(heading for heading, count in collections.Counter(h2).items() if count > 1)
    duplicate_rule = "README_H2_DUPLICATE" if readme else "BODY-H2-DUPLICATE"
    diagnostics.extend(_diagnostic(duplicate_rule, path, profile, "unique H2", heading) for heading in duplicate)
    represented = set(profile.headings.allowed)
    unsupported_rule = "README_H2_UNSUPPORTED" if readme else "BODY-HEADING-UNSUPPORTED"
    diagnostics.extend(_diagnostic(unsupported_rule, path, profile, "allowed H2", heading) for heading in h2 if heading not in represented)
    if profile.placeholder_policy == "forbidden":
        residue_source = text_outside_fenced_code(body)
        for _ in AUTHOR_PROMPT_COMMENT.finditer(residue_source):
            diagnostics.append(
                _diagnostic(
                    "BODY-AUTHOR-PROMPT",
                    path,
                    profile,
                    "authored content without template author prompts",
                    AUTHOR_PROMPT_MARKER,
                )
            )
        for marker in GENERIC_RESIDUE:
            for _ in range(residue_source.count(marker)):
                diagnostics.append(_diagnostic("BODY-TEMPLATE-RESIDUE", path, profile, "authored content without legacy/template residue", marker))
    return diagnostics


@dataclass(frozen=True)
class AppendContext:
    parent_path: PurePosixPath
    parent_profile: DocumentProfile
    parent_h2: str


def validate_document(
    root: Path,
    path: PurePosixPath,
    profile: DocumentProfile,
    mode: str,
    *,
    append_context: AppendContext | None = None,
    today: dt.date | None = None,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Validate one source using only its registry-selected profile contract."""

    if mode not in {"compatibility", "strict"}:
        raise ValueError("mode must be compatibility or strict")
    effective_today = today or dt.datetime.now(ZoneInfo("Asia/Seoul")).date()
    text = read_repository_text(root, path)
    diagnostics: list[Diagnostic] = []
    body = _frontmatter_body(text, path, profile, diagnostics, effective_today)
    diagnostics.extend(_body_diagnostics(path, profile, body, append_context))
    status = ""
    if profile.frontmatter.mode == "required":
        try:
            _, metadata, _ = extract_frontmatter(text)
        except ContractError:
            metadata = {}
        value = metadata.get("status")
        status = value if isinstance(value, str) else ""
    diagnostics.extend(
        _body_contract_diagnostics(
            path,
            profile,
            body,
            status,
            body_contracts,
            body_contract_path_prefixes,
        )
    )
    return sorted(diagnostics, key=diagnostic_sort_key)


def _write_source(root: Path, path: str, source: str) -> None:
    if not isinstance(path, str):
        raise ValueError("fixture writer requires an unparsed path string")
    normalized_path = _fixture_path(path)
    normalized_root = root.resolve()
    target = (normalized_root / normalized_path).resolve(strict=False)
    if not target.is_relative_to(normalized_root):
        raise ValueError(f"fixture path escapes temporary root: {path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")


def _fixture_path(value: object) -> PurePosixPath:
    if not isinstance(value, str):
        raise ValueError("fixture path must be a string")
    path = PurePosixPath(value)
    if (
        not value
        or value == "."
        or value != path.as_posix()
        or value.startswith("./")
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in value
    ):
        raise ValueError(
            f"fixture path must be normalized and repository-relative: {value}"
        )
    return path


def _remove_first_required_h2(source: str, profile: DocumentProfile) -> str:
    heading = profile.headings.required[0]
    marker = f"\n## {heading}\n"
    return source.replace(marker, "\n", 1)


def _replace_required_h2_body(
    source: str, heading: str, replacement: str
) -> str:
    """Replace one fixture H2 body while preserving the heading itself."""

    marker = f"## {heading}\n"
    if source.count(marker) != 1:
        raise ValueError(f"fixture must contain exactly one H2: {heading}")
    body_start = source.index(marker) + len(marker)
    next_heading = re.search(r"(?m)^##(?:[ \t]+|$)", source[body_start:])
    body_end = (
        len(source)
        if next_heading is None
        else body_start + next_heading.start()
    )
    return source[:body_start] + replacement + source[body_end:]


def _mutation_source(
    source: str, mutation: dict[str, Any], profile: DocumentProfile
) -> str:
    kind = mutation["kind"]
    if kind == "remove-required-heading":
        return _remove_first_required_h2(source, profile)
    if kind == "add-frontmatter":
        return "---\ntitle: Forbidden\n---\n\n" + source
    if kind == "unclosed-fence":
        return source + "\n```markdown\n"
    if kind == "duplicate-h1":
        return source + "\n# Duplicate fixture title\n"
    if kind == "append-missing-section":
        section = profile.append_contract.required_sections[0]
        return source.replace(f"#### {section}\n\nFixture evidence.\n\n", "", 1)
    if kind == "append-wrong-entry-level":
        return source.replace("### 2026-07-12", "## 2026-07-12", 1)
    if kind == "append-wrong-section-level":
        return source.replace("#### Metadata", "### Metadata", 1)
    return source


def _append_context(
    registry_profiles: dict[str, DocumentProfile], mutation_kind: str | None
) -> AppendContext | None:
    if mutation_kind == "append-missing-context":
        return None
    parent = registry_profiles["governance/progress-ledger"]
    parent_h2 = "Wrong Parent" if mutation_kind == "append-wrong-parent-h2" else "Work Entries"
    if mutation_kind == "append-wrong-parent-profile":
        parent = registry_profiles["governance/reference"]
    return AppendContext(
        parent_path=PurePosixPath("docs/00.agent-governance/memory/progress.md"),
        parent_profile=parent,
        parent_h2=parent_h2,
    )


def _rule_ids(diagnostics: Sequence[Diagnostic]) -> list[str]:
    return sorted({item.rule_id for item in diagnostics})


@dataclass(frozen=True)
class ResultRow:
    outcome: str
    diagnostic: Diagnostic
    debt_token: str


def _debt_token(diagnostic: Diagnostic) -> str:
    return diagnostic.actual if diagnostic.rule_id in TOKEN_BEARING_DEBT_RULES else ""


def _assert_retired_debt_source(
    root: Path, mode: str, contract: dict[str, Any] | None = None
) -> None:
    """Require the canonical post-migration debt-source retirement state."""

    if contract is None:
        contract = json.loads((root / COMPATIBILITY_PATH).read_text(encoding="utf-8"))
    retired_fields = {"compatibilityDebt", "semanticDebtCaps"}
    if contract.get("schemaVersion") != 2:
        raise ValueError("template compatibility schemaVersion must be 2")
    if contract.get("owner") != "Spec 033" or contract.get("growthAllowed") is not False:
        raise ValueError("template compatibility contract must be Spec 033 owned and no-growth")
    if contract.get("retiredFields") != sorted(retired_fields):
        raise ValueError("template compatibility retiredFields contract differs")
    retired = retired_fields & set(contract)
    if retired:
        raise ValueError(
            "DEBT-SOURCE-REINTRODUCED: " + ",".join(sorted(retired))
        )
    if mode == "compatibility":
        raise ValueError(
            "DEBT-SOURCE-MISSING: compatibilityDebt and semanticDebtCaps are retired"
        )
    if mode != "strict":
        raise ValueError("mode must be compatibility or strict")


def _outcome_rows(
    root: Path,
    diagnostics: Sequence[Diagnostic],
    mode: str,
    *,
    contract: dict[str, Any] | None = None,
) -> list[ResultRow]:
    _assert_retired_debt_source(root, mode, contract)
    return [
        ResultRow("FAIL", diagnostic, _debt_token(diagnostic))
        for diagnostic in sorted(diagnostics, key=diagnostic_sort_key)
    ]


def _result_object(mode: str, rows: Sequence[ResultRow]) -> dict[str, Any]:
    counts = {
        "pass": 1 if not rows else 0,
        "defer": sum(row.outcome == "DEFER" for row in rows),
        "fail": sum(row.outcome == "FAIL" for row in rows),
    }
    if counts["fail"]:
        outcome = "FAIL"
    elif counts["defer"]:
        outcome = "DEFER"
    else:
        outcome = "PASS"
    diagnostics = [
        {
            "outcome": row.outcome,
            "ruleId": row.diagnostic.rule_id,
            "path": row.diagnostic.path.as_posix(),
            "profile": row.diagnostic.profile,
            "expected": row.diagnostic.expected,
            "actual": row.diagnostic.actual,
            "owner": row.diagnostic.owner,
            "debtToken": row.debt_token,
        }
        for row in rows
    ]
    return {
        "schemaVersion": 1,
        "mode": mode,
        "outcome": outcome,
        "counts": counts,
        "diagnostics": diagnostics,
    }


def _emit_results(
    mode: str, output_format: str, rows: Sequence[ResultRow]
) -> None:
    if output_format == "json":
        print(json.dumps(_result_object(mode, rows), ensure_ascii=False, separators=(",", ":")))
        return
    if not rows:
        print(
            'PASS SUMMARY . - expected="no violations" actual="0" '
            f'owner={json.dumps(OWNER)}'
        )
        return
    for row in rows:
        status = row.outcome
        diagnostic = row.diagnostic
        print(
            f"{status} {diagnostic.rule_id} {diagnostic.path.as_posix()} "
            f"{diagnostic.profile or '-'} "
            f"expected={json.dumps(diagnostic.expected, ensure_ascii=False)} "
            f"actual={json.dumps(diagnostic.actual, ensure_ascii=False)} "
            f"owner={json.dumps(diagnostic.owner, ensure_ascii=False)}"
        )


def _run_source_case(
    temp_root: Path,
    path: PurePosixPath,
    source: str,
    profile: DocumentProfile,
    *,
    append_context: AppendContext | None = None,
    today: dt.date = dt.date(2026, 7, 12),
) -> list[str]:
    _write_source(temp_root, path.as_posix(), source)
    return _rule_ids(
        validate_document(
            temp_root,
            path,
            profile,
            "strict",
            append_context=append_context,
            today=today,
            # Matrix, metadata, section, and date fixtures are independent from
            # the dedicated bodyContractCases below. Keep template forms always
            # enforced while placing authored general cases outside audit scope.
            body_contracts="audit",
            body_contract_path_prefixes=(
                PurePosixPath("__self_test_body_contracts_disabled__"),
            ),
        )
    )


def _profile_matrix_source(
    root: Path, row: dict[str, Any], profile: DocumentProfile
) -> str:
    """Use canonical template forms while retaining focused authored fixtures."""

    if (
        profile.mode == "template"
        and profile.body_contract is not None
        and profile.template is not None
    ):
        return read_repository_text(root, profile.template)
    return row["positiveSource"]


def _repository_diagnostics(
    root: Path,
    registry: Any,
    inventory: Any,
    *,
    today: dt.date | None,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    diagnostics: list[Diagnostic] = []
    for path in inventory.current_paths:
        profile = classify_path(registry, path)
        append_context = None
        if profile.append_contract is not None:
            parent = profiles[profile.append_contract.parent_profile_id]
            append_context = AppendContext(
                parent_path=PurePosixPath(
                    "docs/00.agent-governance/memory/progress.md"
                ),
                parent_profile=parent,
                parent_h2=profile.append_contract.parent_h2,
            )
        diagnostics.extend(
            validate_document(
                root,
                path,
                profile,
                "strict",
                append_context=append_context,
                today=today,
                body_contracts=body_contracts,
                body_contract_path_prefixes=body_contract_path_prefixes,
            )
        )
    return sorted(diagnostics, key=diagnostic_sort_key)


def _classification_route_mutation_registry(
    root: Path,
    raw_registry: dict[str, Any],
    profile_id: str,
    fixture_path: PurePosixPath,
) -> Any:
    mutated = copy.deepcopy(raw_registry)
    try:
        profile = next(
            item for item in mutated["profiles"] if item["id"] == profile_id
        )
    except StopIteration as exc:
        raise ContractError(f"unknown classification-only profile: {profile_id}") from exc

    path_text = fixture_path.as_posix()
    mutation_count = 0
    for route in profile["routes"]:
        matches = (
            path_text == route["value"]
            if route["kind"] == "exact"
            else re.fullmatch(route["value"], path_text) is not None
        )
        if not matches:
            continue
        route["kind"] = "exact"
        route["value"] = f"{path_text}.classification-route-mismatch"
        mutation_count += 1
    if mutation_count != 1:
        raise ContractError(
            f"classification-only route mutation expected one route, got {mutation_count}"
        )
    return validate_registry(root, mutated)


def _self_test(root: Path) -> list[str]:
    raw_registry = json.loads((root / REGISTRY_PATH).read_text(encoding="utf-8"))
    registry = load_registry(root)
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    inventory = enumerate_target_markdown(root)
    fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
    readme_fixture = json.loads(
        (root / README_FIXTURE_PATH).read_text(encoding="utf-8")
    )
    failures: list[str] = []

    if fixture.get("schemaVersion") != 1:
        failures.append("fixture schemaVersion must be 1")
    if set(fixture) != {
        "schemaVersion",
        "dateCases",
        "sectionBodyCases",
        "relationshipCases",
        "bodyContractCases",
        "profileMatrix",
        "mutationCases",
    }:
        failures.append("fixture top-level keys changed")
    rows = fixture.get("profileMatrix", [])
    row_ids = [row.get("profile") for row in rows]
    if len(row_ids) != len(set(row_ids)):
        failures.append("profileMatrix contains duplicate profiles")
    if set(row_ids) != set(profiles):
        failures.append("profileMatrix must cover every registry profile exactly once")
    expected_date_cases = (
        ("authored-previous-day", "sdlc/spec", "2026-07-11", ()),
        ("authored-same-day", "sdlc/spec", "2026-07-12", ()),
        ("authored-next-day", "sdlc/spec", "2026-07-13", ("FM-FUTURE-DATE",)),
        ("authored-valid-leap-day", "sdlc/spec", "2024-02-29", ()),
        ("authored-invalid-leap-day", "sdlc/spec", "2025-02-29", ("FM-DATE",)),
        ("template-date-placeholder", "template/sdlc/spec", "YYYY-MM-DD", ()),
        ("template-invalid-date", "template/sdlc/spec", "2025-02-29", ("FM-DATE",)),
    )
    actual_date_cases = tuple(
        (
            case.get("name"),
            case.get("profile"),
            case.get("value"),
            tuple(case.get("expectedRuleIds", ())),
        )
        for case in fixture.get("dateCases", [])
    )
    if actual_date_cases != expected_date_cases:
        failures.append("dateCases must preserve the exact seven-case contract")

    if set(readme_fixture) != {
        "schemaVersion",
        "activePaths",
        "retiredPaths",
        "cases",
    } or readme_fixture.get("schemaVersion") != 3:
        failures.append("README handoff fixture must use schema-v2 retirement inventory")
    readme_names = tuple(case.get("name") for case in readme_fixture.get("cases", []))
    if readme_names != EXPECTED_README_CASES:
        failures.append("README handoff case names changed")
    readme_path_rows = readme_fixture.get("activePaths", [])
    retired_readme_rows = readme_fixture.get("retiredPaths", [])
    readme_paths = [row.get("path") for row in readme_path_rows]
    retired_readme_paths = [row.get("path") for row in retired_readme_rows]
    if (
        len(readme_paths) != 52
        or len(readme_paths) != len(set(readme_paths))
        or readme_paths != sorted(readme_paths)
    ):
        failures.append("README activePaths must contain 52 sorted unique entries")
    if (
        len(retired_readme_paths) != 20
        or len(retired_readme_paths) != len(set(retired_readme_paths))
        or retired_readme_paths != sorted(retired_readme_paths)
    ):
        failures.append("README retiredPaths must contain 20 sorted unique entries")
    if set(readme_paths) & set(retired_readme_paths):
        failures.append("README activePaths and retiredPaths must be disjoint")
    readme_by_path = {row.get("path"): row for row in readme_path_rows}
    retired_readme_by_path = {
        row.get("path"): row for row in retired_readme_rows
    }
    inventory_readmes = {
        path.as_posix()
        for path in inventory.current_paths
        if path.name == "README.md"
        and classify_path(registry, path).profile_class == "readme"
        and classify_path(registry, path).mode != "template"
    }
    if set(readme_paths) != inventory_readmes:
        failures.append("README activePaths must equal the production inventory set")
    baseline_readmes = {
        path.as_posix()
        for path in inventory.baseline_paths
        if path.name == "README.md"
    }
    active_baseline = set(readme_paths) & baseline_readmes
    active_program_created = set(readme_paths) - baseline_readmes
    if (
        len(baseline_readmes) != 67
        or len(active_baseline) != 47
        or len(active_program_created) != 5
        or active_baseline | set(retired_readme_paths) != baseline_readmes
        or set(retired_readme_paths) - baseline_readmes
    ):
        failures.append(
            "README handoff must reconstruct baseline67 as active47 plus retired20 and active-new5"
        )
    active_keys = {"path", "profile", "requiredH2", "allowedH2", "new"}
    retired_keys = active_keys | {"retiredBy", "destination"}
    for lifecycle, handoffs, expected_keys in (
        ("active", readme_by_path, active_keys),
        ("retired", retired_readme_by_path, retired_keys),
    ):
        for path_text, handoff in handoffs.items():
            if set(handoff) != expected_keys:
                failures.append(f"README {lifecycle} handoff row fields differ: {path_text}")
                continue
            if not isinstance(path_text, str):
                failures.append("README handoff path values must be strings")
                continue
            if lifecycle == "active":
                try:
                    selected = classify_path(registry, _fixture_path(path_text))
                except (DocumentContractError, ValueError) as exc:
                    failures.append(f"README handoff path invalid: {exc}")
                    continue
                if handoff.get("profile") != selected.profile_id:
                    failures.append(f"README handoff profile mismatch: {path_text}")
            else:
                if handoff.get("profile") != "readme/snapshot-pack":
                    failures.append(
                        f"README retired historical profile mismatch: {path_text}"
                    )
                    continue
                selected = next(
                    profile
                    for profile in registry.profiles
                    if profile.profile_id == "readme/snapshot-pack"
                )
                try:
                    classify_path(registry, _fixture_path(path_text))
                except DocumentContractError as exc:
                    if not any(
                        diagnostic.rule_id == "REGISTRY_ROUTE_UNCOVERED"
                        for diagnostic in exc.diagnostics
                    ):
                        failures.append(
                            f"README retired route rule mismatch: {path_text}"
                        )
                except ValueError as exc:
                    failures.append(f"README retired path invalid: {exc}")
                else:
                    failures.append(f"README retired path is still routed: {path_text}")
            if handoff.get("requiredH2") != list(selected.headings.required):
                failures.append(f"README handoff requiredH2 mismatch: {path_text}")
            if handoff.get("allowedH2") != list(selected.headings.allowed):
                failures.append(f"README handoff allowedH2 mismatch: {path_text}")
            expected_new = path_text not in baseline_readmes
            if handoff.get("new") is not expected_new:
                failures.append(f"README handoff new disposition mismatch: {path_text}")
            if lifecycle == "active":
                if not (root / path_text).is_file():
                    failures.append(f"README active handoff path is absent: {path_text}")
                continue
            if handoff.get("retiredBy") != "ADM-006":
                failures.append(f"README retired handoff owner mismatch: {path_text}")
            if path_text.startswith("examples/aws/docs/"):
                provider = "aws"
            elif path_text.startswith("examples/azure/docs/"):
                provider = "azure"
            else:
                failures.append(f"README retired handoff provider mismatch: {path_text}")
                continue
            expected_destination = (
                f"docs/90.references/cloud-examples/{provider}/"
                f"2026-07-12-{provider}-example-snapshot.md"
            )
            if handoff.get("destination") != expected_destination:
                failures.append(f"README retired handoff destination mismatch: {path_text}")
            elif not (root / expected_destination).is_file():
                failures.append(f"README retired handoff destination is absent: {path_text}")
            if (root / path_text).exists() or path_text in inventory_readmes:
                failures.append(f"README retired handoff remains current: {path_text}")

    with tempfile.TemporaryDirectory(prefix="markdown-profile-self-test-") as directory:
        temp_root = Path(directory)
        compatibility_target = temp_root / COMPATIBILITY_PATH
        compatibility_target.parent.mkdir(parents=True, exist_ok=True)
        compatibility_target.write_text(
            (root / COMPATIBILITY_PATH).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        for row in rows:
            required_fields = {
                "profile",
                "mode",
                "applicability",
                "fixturePath",
                "positiveSource",
                "negativeMutations",
            }
            expected_fields = required_fields | ({"reason"} if row.get("applicability") == "excluded" else set())
            if set(row) != expected_fields:
                failures.append(f"matrix row is incomplete: {row.get('profile')}")
                continue
            profile = profiles[row["profile"]]
            if row["mode"] != profile.mode:
                failures.append(f"matrix mode mismatch: {profile.profile_id}")
            applicability = row["applicability"]
            if applicability not in {
                "validate-document",
                "append-fragment",
                "classification-only",
                "excluded",
            }:
                failures.append(f"invalid applicability: {profile.profile_id}")
                continue
            structural_na = (
                profile.frontmatter.mode == "not-applicable"
                and not profile.headings.required
                and not profile.headings.allowed
            )
            if applicability == "validate-document" and (
                profile.mode not in {"authored", "template", "frontmatter-free"}
                or profile.append_contract is not None
            ):
                failures.append(f"invalid validate-document mode: {profile.profile_id}")
            if applicability == "classification-only" and (
                profile.mode not in {"classification-only", "generated"} or not structural_na
            ):
                failures.append(f"invalid classification-only mode: {profile.profile_id}")
            if applicability == "append-fragment" and profile.profile_id != "governance/progress-entry":
                failures.append(f"invalid append-fragment profile: {profile.profile_id}")
            if profile.profile_id == "governance/progress-entry" and applicability != "append-fragment":
                failures.append("governance/progress-entry must be append-fragment")
            try:
                fixture_path = _fixture_path(row["fixturePath"])
            except ValueError as exc:
                failures.append(f"matrix fixture path invalid: {exc}")
                continue
            try:
                selected_profile = classify_path(registry, fixture_path).profile_id
            except DocumentContractError as exc:
                selected_profile = ",".join(item.rule_id for item in exc.diagnostics)
            if selected_profile != profile.profile_id:
                failures.append(
                    f"matrix route mismatch {profile.profile_id}: actual={selected_profile}"
                )
            if applicability == "excluded":
                if profile.mode != "non-target" or row.get("reason") != "non-target":
                    failures.append(f"unjustified excluded row: {profile.profile_id}")
                continue
            path = fixture_path
            if applicability == "classification-only":
                try:
                    actual = classify_path(registry, path).profile_id
                except DocumentContractError as exc:
                    actual = ",".join(item.rule_id for item in exc.diagnostics)
                if actual != profile.profile_id:
                    failures.append(
                        f"classification positive {profile.profile_id}: expected={profile.profile_id} actual={actual}"
                    )
                selected_inventory_paths = [
                    candidate
                    for candidate in inventory.current_paths
                    if classify_path(registry, candidate).profile_id == profile.profile_id
                ]
                if path.suffix == ".md" and not selected_inventory_paths:
                    failures.append(
                        f"classification-only inventory selection missing: {profile.profile_id}"
                    )
                for candidate in selected_inventory_paths[:1]:
                    actual_rules = _rule_ids(
                        validate_document(
                            root,
                            candidate,
                            profile,
                            "strict",
                            today=dt.date(2026, 7, 12),
                        )
                    )
                    if actual_rules:
                        failures.append(
                            f"classification-only structural N/A {profile.profile_id}: {actual_rules}"
                        )
                for mutation in row["negativeMutations"]:
                    expected_mutation = {
                        "kind": "classification-route-mismatch",
                        "expectedRuleIds": ["REGISTRY_ROUTE_UNCOVERED"],
                    }
                    if mutation != expected_mutation:
                        failures.append(
                            "classification negative "
                            f"{profile.profile_id}: mutation contract must be "
                            f"{expected_mutation!r}, got {mutation!r}"
                        )
                        continue
                    try:
                        mutated_registry = _classification_route_mutation_registry(
                            root,
                            raw_registry,
                            profile.profile_id,
                            path,
                        )
                        classify_path(mutated_registry, path)
                        actual_rules: list[str] = []
                    except (ContractError, DocumentContractError) as exc:
                        if isinstance(exc, ContractError):
                            failures.append(
                                f"classification negative {profile.profile_id}: {exc}"
                            )
                            continue
                        actual_rules = _rule_ids(exc.diagnostics)
                    if actual_rules != mutation["expectedRuleIds"]:
                        failures.append(
                            f"classification negative {profile.profile_id}: expected={mutation['expectedRuleIds']} actual={actual_rules}"
                        )
                continue
            context = (
                _append_context(profiles, None)
                if applicability == "append-fragment"
                else None
            )
            positive_source = _profile_matrix_source(root, row, profile)
            actual_rules = _run_source_case(
                temp_root,
                path,
                positive_source,
                profile,
                append_context=context,
            )
            if actual_rules:
                failures.append(
                    f"matrix positive {profile.profile_id}: expected=[] actual={actual_rules}"
                )
            if not row["negativeMutations"]:
                failures.append(f"matrix row lacks a negative mutation: {profile.profile_id}")
            for mutation in row["negativeMutations"]:
                kind = mutation["kind"]
                source = _mutation_source(positive_source, mutation, profile)
                mutation_context = (
                    _append_context(profiles, kind)
                    if applicability == "append-fragment"
                    else None
                )
                actual_rules = _run_source_case(
                    temp_root,
                    path,
                    source,
                    profile,
                    append_context=mutation_context,
                )
                if actual_rules != mutation["expectedRuleIds"]:
                    failures.append(
                        f"matrix negative {profile.profile_id}/{kind}: expected={mutation['expectedRuleIds']} actual={actual_rules}"
                    )

        for case in fixture.get("mutationCases", []):
            profile = profiles[case["profile"]]
            actual_rules = _run_source_case(
                temp_root,
                _fixture_path(case["path"]),
                case["source"],
                profile,
            )
            if actual_rules != case["expectedRuleIds"]:
                failures.append(
                    f"mutation {case['name']}: expected={case['expectedRuleIds']} actual={actual_rules}"
                )

        for case in readme_fixture.get("cases", []):
            path = _fixture_path(case["path"])
            handoff = readme_by_path.get(path.as_posix())
            if handoff is None:
                failures.append(f"README case path is absent from paths table: {path}")
                continue
            profile = classify_path(registry, path)
            if handoff.get("profile") != profile.profile_id:
                failures.append(f"README case profile differs from paths table: {path}")
            actual_rules = _run_source_case(
                temp_root, path, case["document"], profile
            )
            if actual_rules != case["expected_rule_ids"]:
                failures.append(
                    f"README handoff {case['name']}: expected={case['expected_rule_ids']} actual={actual_rules}"
                )

        matrix_by_profile = {row["profile"]: row for row in rows}

        section_cases = fixture.get("sectionBodyCases", [])
        expected_section_names = (
            "empty-required-h2",
            "comments-only-required-h2",
            "fenced-payload-required-h2",
            "empty-fence-required-h2",
            "template-form-body-exemption",
            "optional-empty-h2-unchanged",
        )
        if tuple(case.get("name") for case in section_cases) != expected_section_names:
            failures.append("focused section-body case names changed")
        section_case_keys = {
            "name",
            "profile",
            "mutation",
            "heading",
            "body",
            "expectedRuleIds",
        }
        for case in section_cases:
            if set(case) != section_case_keys:
                failures.append(
                    f"focused section-body case fields differ: {case.get('name')}"
                )
                continue
            profile = profiles[case["profile"]]
            row = matrix_by_profile[profile.profile_id]
            path = _fixture_path(row["fixturePath"])
            source = _profile_matrix_source(root, row, profile)
            mutation = case["mutation"]
            heading = case["heading"]
            if mutation == "replace-body":
                source = _replace_required_h2_body(
                    source, heading, case["body"]
                )
            elif mutation == "insert-empty-optional":
                if (
                    heading not in profile.headings.allowed
                    or heading in profile.headings.required
                ):
                    failures.append(
                        f"focused optional heading is not optional: {heading}"
                    )
                    continue
                relationship_heading = profile.headings.required[-1]
                marker = f"\n## {relationship_heading}\n"
                if source.count(marker) != 1:
                    failures.append(
                        "focused optional mutation lacks one relationship marker"
                    )
                    continue
                source = source.replace(
                    marker,
                    f"\n## {heading}\n{case['body']}" + marker,
                    1,
                )
            else:
                failures.append(
                    f"focused section-body mutation is invalid: {mutation}"
                )
                continue
            _write_source(temp_root, path.as_posix(), source)
            diagnostics = validate_document(
                temp_root,
                path,
                profile,
                "strict",
                today=dt.date(2026, 7, 12),
                body_contracts="audit",
                body_contract_path_prefixes=(
                    PurePosixPath("__self_test_body_contracts_disabled__"),
                ),
            )
            actual_rules = _rule_ids(diagnostics)
            if actual_rules != case["expectedRuleIds"]:
                failures.append(
                    f"focused section-body {case['name']}: "
                    f"expected={case['expectedRuleIds']} actual={actual_rules}"
                )
            if case["name"] == "empty-required-h2":
                empty_rows = [
                    item
                    for item in diagnostics
                    if item.rule_id == "BODY-HEADING-EMPTY"
                ]
                if (
                    len(empty_rows) != 1
                    or empty_rows[0].path != path
                    or empty_rows[0].actual != heading
                ):
                    failures.append(
                        "focused empty-H2 diagnostic must expose path and "
                        "heading without body content"
                    )

        relationship_cases = fixture.get("relationshipCases", [])
        expected_relationship_names = (
            "sdlc-spec-traceability",
            "common-reference-related-documents",
            "readme-related-documents",
        )
        if (
            tuple(case.get("name") for case in relationship_cases)
            != expected_relationship_names
        ):
            failures.append("focused relationship case names changed")
        relationship_case_keys = {
            "name",
            "profile",
            "requiredHeading",
            "forbiddenHeading",
        }
        for case in relationship_cases:
            if set(case) != relationship_case_keys:
                failures.append(
                    f"focused relationship case fields differ: {case.get('name')}"
                )
                continue
            profile = profiles[case["profile"]]
            row = matrix_by_profile[profile.profile_id]
            h2 = [
                title
                for level, title in scan_headings(
                    _profile_matrix_source(root, row, profile)
                ).headings
                if level == 2
            ]
            if (
                case["requiredHeading"] not in h2
                or case["forbiddenHeading"] in h2
                or case["requiredHeading"] not in profile.headings.required
            ):
                failures.append(
                    f"focused relationship {case['name']} does not follow "
                    "the selected profile"
                )

        for case in fixture.get("dateCases", []):
            profile = profiles[case["profile"]]
            base_row = matrix_by_profile[profile.profile_id]
            base = _profile_matrix_source(root, base_row, profile)
            source = re.sub(
                r"(?m)^updated: .+$", f"updated: {case['value']}", base, count=1
            )
            actual_rules = _run_source_case(
                temp_root,
                _fixture_path(matrix_by_profile[profile.profile_id]["fixturePath"]),
                source,
                profile,
                today=dt.date(2026, 7, 12),
            )
            if actual_rules != case["expectedRuleIds"]:
                failures.append(
                    f"date {case['name']}: expected={case['expectedRuleIds']} actual={actual_rules}"
                )

        body_contract_case_keys = {
            "name",
            "profile",
            "status",
            "bodyContracts",
            "enforcedStatuses",
            "body",
            "expectedRuleIds",
        }
        body_contract_validator = globals().get("_body_contract_diagnostics")
        for case in fixture.get("bodyContractCases", []):
            prefix_case = "pathPrefixes" in case or "path" in case
            expected_case_keys = body_contract_case_keys | (
                {"path", "pathPrefixes"} if prefix_case else set()
            )
            if set(case) != expected_case_keys:
                failures.append(
                    f"body-contract case fields differ: {case.get('name')}"
                )
                continue
            profile = profiles[case["profile"]]
            if profile.body_contract is None:
                failures.append(
                    f"body-contract case profile has no contract: {case['profile']}"
                )
                continue
            selected = dataclasses.replace(
                profile,
                body_contract=dataclasses.replace(
                    profile.body_contract,
                    enforced_statuses=tuple(case["enforcedStatuses"]),
                ),
            )
            if body_contract_validator is None:
                failures.append(
                    f"body-contract {case['name']}: BODY-CONTRACT rules are unimplemented"
                )
                continue
            try:
                diagnostics = body_contract_validator(
                    PurePosixPath(
                        case.get(
                            "path", "docs/01.requirements/999-fixture.md"
                        )
                    ),
                    selected,
                    case["body"],
                    case["status"],
                    case["bodyContracts"],
                    tuple(
                        PurePosixPath(value)
                        for value in case.get("pathPrefixes", [])
                    ),
                )
            except TypeError:
                failures.append(
                    f"body-contract {case['name']}: path-prefix scope is unimplemented"
                )
                continue
            actual_rules = _rule_ids(diagnostics)
            if actual_rules != case["expectedRuleIds"]:
                failures.append(
                    f"body-contract {case['name']}: "
                    f"expected={case['expectedRuleIds']} actual={actual_rules}"
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

        for escape in (
            ".",
            "./smdv-escape.md",
            "/tmp/smdv-escape.md",
            "../smdv-escape.md",
            "nested\\smdv-escape.md",
            PurePosixPath("./smdv-normalized-too-early.md"),
        ):
            try:
                _write_source(temp_root, escape, "unsafe")
            except ValueError:
                pass
            else:
                failures.append(f"fixture writer accepted escaping path: {escape}")
        for raw_escape in (
            ".",
            "./smdv-escape.md",
            "../smdv-escape.md",
            "/tmp/smdv-escape.md",
            "nested\\smdv-escape.md",
        ):
            try:
                _fixture_path(raw_escape)
            except ValueError:
                pass
            else:
                failures.append(f"fixture parser accepted escaping path: {raw_escape}")
    named_cases = {case.get("name") for case in fixture.get("mutationCases", [])}
    required_named_cases = {
        "valid-spec",
        "duplicate-key",
        "future-date",
        "wrong-key-order",
        "missing-heading",
        "heading-in-fence",
        "duplicate-h2",
        "unsupported-h2",
        "template-residue",
        "unclosed-fence",
        "placeholder-frontmatter-title",
        "placeholder-h1-title",
        "authored-author-prompt",
        "author-prompt-after-commented-fence",
        "authored-legacy-target-marker",
        "authored-retired-shared-paragraph",
        "fenced-starter-examples-allowed",
        "template-starters-allowed",
    }
    if not required_named_cases.issubset(named_cases):
        failures.append("required named mutation cases are incomplete")
    exercised = {
        rule
        for row in rows
        for mutation in row.get("negativeMutations", [])
        for rule in mutation.get("expectedRuleIds", [])
    }
    exercised.update(
        rule
        for case in fixture.get("mutationCases", [])
        for rule in case.get("expectedRuleIds", [])
    )
    exercised.update(
        rule
        for case in readme_fixture.get("cases", [])
        for rule in case.get("expected_rule_ids", [])
    )
    exercised.update(
        rule
        for case in fixture.get("bodyContractCases", [])
        for rule in case.get("expectedRuleIds", [])
    )
    exercised.add("BODY-HEADING-EMPTY")
    uncovered_rules = sorted(IMPLEMENTED_RULE_IDS - exercised)
    if uncovered_rules:
        failures.append(f"implemented rules lack mutations: {uncovered_rules}")

    production_diagnostics = _repository_diagnostics(
        root,
        registry,
        inventory,
        today=dt.datetime.now(ZoneInfo("Asia/Seoul")).date(),
    )
    if production_diagnostics:
        failures.append("retired-source production diagnostics must be empty")

    base_contract = json.loads(
        (root / COMPATIBILITY_PATH).read_text(encoding="utf-8")
    )
    retired_fields = {"compatibilityDebt", "semanticDebtCaps"}
    if retired_fields & set(base_contract):
        failures.append("retired template debt source is still present")
    try:
        strict_rows = _outcome_rows(root, production_diagnostics, "strict")
    except (OSError, ValueError) as exc:
        failures.append(f"strict retired-source state rejected: {exc}")
        strict_rows = []
    if strict_rows:
        failures.append("strict retired-source outcome rows must be empty")

    try:
        _outcome_rows(root, production_diagnostics, "compatibility")
    except ValueError as exc:
        expected = (
            "DEBT-SOURCE-MISSING: compatibilityDebt and semanticDebtCaps are retired"
        )
        if str(exc) != expected:
            failures.append("compatibility retired-source diagnostic differs")
    else:
        failures.append("compatibility accepted the retired template debt source")

    stdout = io.StringIO()
    stderr = io.StringIO()
    fixture_before = (root / COMPATIBILITY_PATH).read_bytes()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        return_code = main(
            ["--root", str(root), "--mode", "compatibility", "--format", "json"]
        )
    expected_stderr = (
        "configuration error: DEBT-SOURCE-MISSING: compatibilityDebt and "
        "semanticDebtCaps are retired\n"
    )
    if return_code != 2 or stdout.getvalue() or stderr.getvalue() != expected_stderr:
        failures.append("compatibility retired-source CLI boundary differs")
    if (root / COMPATIBILITY_PATH).read_bytes() != fixture_before:
        failures.append("retired-source validation rewrote the template fixture")

    def expect_config_rejection(
        label: str,
        candidate: dict[str, Any],
        *,
        modes: tuple[str, ...] = ("strict",),
    ) -> None:
        for mode in modes:
            try:
                _assert_retired_debt_source(root, mode, candidate)
            except ValueError:
                continue
            failures.append(f"debt mutation accepted in {mode}: {label}")

    reintroduced_fields = (
        ("compatibilityDebt", {"compatibilityDebt": []}),
        ("semanticDebtCaps", {"semanticDebtCaps": {}}),
        (
            "both retired fields",
            {"compatibilityDebt": [], "semanticDebtCaps": {}},
        ),
    )
    for label, values in reintroduced_fields:
        candidate = copy.deepcopy(base_contract)
        candidate.update(values)
        expect_config_rejection(
            label, candidate, modes=("strict", "compatibility")
        )

    wrong_owner = copy.deepcopy(base_contract)
    wrong_owner["owner"] = "Spec 999"
    expect_config_rejection("wrong owner", wrong_owner)

    growth_allowed = copy.deepcopy(base_contract)
    growth_allowed["growthAllowed"] = True
    expect_config_rejection("growth allowed", growth_allowed)

    synthetic_diagnostics = (
        (
            "unknown rule",
            Diagnostic(
                "UNKNOWN-RULE",
                PurePosixPath("docs/00.agent-governance/rules/bootstrap.md"),
                "governance/reference",
                "implemented semantic debt rule",
                "UNKNOWN-RULE",
                OWNER,
            ),
        ),
        (
            "unregistered known rule token",
            Diagnostic(
                "BODY-HEADING-UNSUPPORTED",
                PurePosixPath("docs/00.agent-governance/rules/bootstrap.md"),
                "governance/reference",
                "canonical H2 heading",
                "Synthetic Reintroduced Debt",
                OWNER,
            ),
        ),
    )
    for label, diagnostic in synthetic_diagnostics:
        result = _outcome_rows(root, [diagnostic], "strict")
        if (
            len(result) != 1
            or result[0].outcome != "FAIL"
            or any(row.outcome == "DEFER" for row in result)
        ):
            failures.append(f"{label} mutation did not fail in strict mode")
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
    parser.add_argument("--include-path", action="append", default=[])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--inventory", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.self_test:
            failures = _self_test(root)
            if failures:
                for failure in failures:
                    print(f"FAIL SELF-TEST {failure}")
                return 1
            print("PASS markdown profile self-test")
            return 0
        registry = load_registry(root)
        include_paths = tuple(PurePosixPath(value) for value in args.include_path)
        inventory = enumerate_target_markdown(root, include_paths=include_paths)
        if args.inventory:
            payload = {
                "schemaVersion": 1,
                "mode": args.mode,
                "outcome": "PASS",
                "counts": {
                    "baseline": len(inventory.baseline_paths),
                    "current": len(inventory.current_paths),
                    "new": len(inventory.new_paths),
                },
                "diagnostics": [],
            }
            if args.format == "json":
                print(json.dumps(payload, separators=(",", ":")))
            else:
                print(
                    f"PASS INVENTORY . - expected={json.dumps('tracked target Markdown')} "
                    f"actual={json.dumps(str(len(inventory.current_paths)))} owner={json.dumps(OWNER)}"
                )
            return 0
        diagnostics: list[Diagnostic] = []
        profiles = {profile.profile_id: profile for profile in registry.profiles}
        for path in inventory.current_paths:
            profile = classify_path(registry, path)
            append_context = None
            if profile.append_contract is not None:
                parent = profiles[profile.append_contract.parent_profile_id]
                append_context = AppendContext(
                    parent_path=PurePosixPath(
                        "docs/00.agent-governance/memory/progress.md"
                    ),
                    parent_profile=parent,
                    parent_h2=profile.append_contract.parent_h2,
                )
            diagnostics.extend(
                validate_document(
                    root,
                    path,
                    profile,
                    args.mode,
                    append_context=append_context,
                    body_contracts=args.body_contracts,
                    body_contract_path_prefixes=tuple(
                        args.body_contract_path_prefix
                    ),
                )
            )
        rows = _outcome_rows(root, diagnostics, args.mode)
        _emit_results(args.mode, args.format, rows)
        return 1 if any(row.outcome == "FAIL" for row in rows) else 0
    except (DocumentContractError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
