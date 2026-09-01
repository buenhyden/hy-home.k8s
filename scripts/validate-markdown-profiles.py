#!/usr/bin/env python3
"""Validate registry-selected Markdown document profiles."""

from __future__ import annotations

import argparse
import collections
import copy
import datetime as dt
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Sequence
from zoneinfo import ZoneInfo

import yaml

from document_contracts import (
    ConditionalConstraint,
    ConstantConstraint,
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    EnumConstraint,
    classify_path,
    diagnostic_sort_key,
    enumerate_tracked_regular_paths,
    enumerate_target_markdown,
    is_ignored_repository_path,
    load_internal_payload,
    load_registry,
    read_repository_text,
    validate_registry,
)


SDLC_FRONTMATTER_KEYS = ("title", "type", "status", "owner", "updated")
# Stage 05 holds only live, platform-owned operational documents.  The shared
# registry cannot express either constraint: its status domain admits four
# lifecycle states, and it constrains owner to any string.  Both values are
# therefore pinned per profile here, where the other frontmatter values are
# already checked.
STAGE05_PROFILE_IDS = frozenset(
    {
        "sdlc/guide",
        "sdlc/policy",
        "sdlc/runbook",
        "sdlc/incident",
        "sdlc/postmortem",
    }
)
STAGE05_PINNED_FRONTMATTER = {"status": "active", "owner": "platform"}
NATIVE_TRACKED_PATHSPECS = (
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "docs/03.specs",
)
OWNER = "markdown-profile-validator"
AUTHOR_PROMPT_MARKER = "Author prompt:"
AUTHOR_PROMPT_COMMENT = re.compile(r"(?m)^[ \t]*<!-- Author prompt:")
GENERIC_RESIDUE = (
    "Target: docs/",
    "Use this template",
    "Replace every placeholder with researched, topic-specific content.",
)
STARTER_PLACEHOLDER = re.compile(r"\[[^\]\n]+\]|\{[^}\n]+\}|<[^>\n]+>|#{3,}")
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
        "FM-VALUE-CONDITIONAL",
        "FM-VALUE-CONSTANT",
        "FM-VALUE-ENUM",
        "FM-VALUE-KIND",
        "FM-VALUE-NULL",
        "FM-VALUE-PATTERN",
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


def _has_exact_leading_sdlc_frontmatter(text: str) -> bool:
    """Recognize only the canonical five-line SDLC metadata envelope.

    Native syntax remains owned by its native toolchain. A leading YAML
    document marker without this exact envelope is not Markdown frontmatter.
    """

    try:
        keys, metadata, _ = extract_frontmatter(text)
    except ContractError:
        return False
    document_type = metadata.get("type")
    return (
        tuple(keys) == SDLC_FRONTMATTER_KEYS
        and isinstance(document_type, str)
        and re.fullmatch(r"sdlc/[a-z][a-z0-9-]*", document_type) is not None
    )


def _native_surface_owner(
    registry: Any,
    path: PurePosixPath,
) -> tuple[str, DocumentProfile | None] | None:
    """Select native ownership without claiming GitHub YAML in the registry."""

    parts = path.parts
    if (
        len(parts) == 3
        and parts[:2]
        in {
            (".github", "ISSUE_TEMPLATE"),
            (".github", "workflows"),
        }
        and path.suffix in {".yml", ".yaml"}
    ):
        try:
            selected = classify_path(registry, path)
        except DocumentContractError as exc:
            if _rule_ids(exc.diagnostics) == ["REGISTRY_ROUTE_UNCOVERED"]:
                return "github-native", None
            raise ValueError(
                f"GitHub-native ownership is ambiguous: {path.as_posix()}"
            ) from exc
        raise ValueError(
            "GitHub-native surface was claimed by document profile "
            f"{selected.profile_id}: {path.as_posix()}"
        )
    try:
        profile = classify_path(registry, path)
    except DocumentContractError:
        return None
    if (
        profile.mode == "classification-only"
        and profile.frontmatter.mode == "not-applicable"
    ):
        return "registry-profile", profile
    return None


def _is_native_candidate_path(registry: Any, path: PurePosixPath) -> bool:
    parts = path.parts
    if (
        len(parts) == 3
        and parts[:2]
        in {
            (".github", "ISSUE_TEMPLATE"),
            (".github", "workflows"),
        }
        and path.suffix in {".yml", ".yaml"}
    ):
        return True
    native_basenames = {
        profile.template.name.replace(".template.", ".")
        for profile in registry.profiles
        if profile.template is not None
        and profile.mode == "classification-only"
        and profile.frontmatter.mode == "not-applicable"
    }
    return (
        len(parts) >= 2
        and parts[0] == "docs"
        and parts[1] == "03.specs"
        and path.name in native_basenames
    )


def _native_surface_diagnostics(
    root: Path,
    registry: Any,
    *,
    include_paths: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Reject an SDLC envelope on tracked or explicitly included native files."""

    indexed_paths = set(
        enumerate_tracked_regular_paths(root, pathspecs=NATIVE_TRACKED_PATHSPECS)
    )
    paths: set[PurePosixPath] = set()
    for path in indexed_paths:
        if not _is_native_candidate_path(registry, path):
            continue
        if _native_surface_owner(registry, path) is None:
            raise ValueError(
                f"tracked native path lacks an ownership contract: {path.as_posix()}"
            )
        paths.add(path)
    for requested in include_paths:
        path = _fixture_path(requested.as_posix())
        if _native_surface_owner(registry, path) is None:
            raise ValueError(
                f"included path is not a governed native surface: {path.as_posix()}"
            )
        if is_ignored_repository_path(root, path):
            raise ValueError(f"included path is ignored: {path.as_posix()}")
        read_repository_text(root, path)
        paths.add(path)

    diagnostics: list[Diagnostic] = []
    for path in sorted(paths, key=lambda item: item.as_posix()):
        selection = _native_surface_owner(registry, path)
        if selection is None:
            raise ValueError(f"native ownership disappeared: {path.as_posix()}")
        owner, profile = selection
        source = read_repository_text(root, path)
        if not _has_exact_leading_sdlc_frontmatter(source):
            continue
        if profile is None:
            diagnostics.append(
                Diagnostic(
                    rule_id="FM-FORBIDDEN",
                    path=path,
                    profile=owner,
                    expected=(
                        "GitHub-native YAML without the five-key SDLC "
                        "frontmatter envelope"
                    ),
                    actual="exact leading SDLC five-key block",
                    owner=OWNER,
                )
            )
        else:
            diagnostics.append(
                _diagnostic(
                    "FM-FORBIDDEN",
                    path,
                    profile,
                    "native syntax without the five-key SDLC frontmatter envelope",
                    "exact leading SDLC five-key block",
                )
            )
    return diagnostics


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
    "requirement": re.compile(r"^REQ-[0-9]{4}-(?:FR|NFR|IF)-[0-9]{4}$"),
    "criterion": re.compile(r"^VAL-[A-Z0-9-]+-[0-9]{3}$"),
    "work-item": re.compile(r"^[A-Z][A-Z0-9-]+-[0-9]{3}$"),
}
TEMPLATE_IDENTIFIER_PATTERNS = IDENTIFIER_PATTERNS
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


def _requirement_package_number(path: PurePosixPath) -> str | None:
    """Return the canonical four-digit Requirement Package path identity."""

    match = re.fullmatch(r"([0-9]{4})-[a-z][a-z0-9]*(?:-[a-z0-9]+)*\.md", path.name)
    return None if match is None else match.group(1)


def _requirement_package_identity_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    metadata: dict[str, Any],
) -> list[Diagnostic]:
    """Bind an authored Requirement Package artifact ID to its path number."""

    if profile.profile_id != "sdlc/requirement-package" or profile.mode != "authored":
        return []
    package_number = _requirement_package_number(path)
    artifact_id = metadata.get("artifact_id")
    if package_number is None or not isinstance(artifact_id, str):
        return []
    expected = f"REQ-{package_number}"
    if artifact_id == expected:
        return []
    return [
        _diagnostic(
            "REQUIREMENT-PACKAGE-IDENTITY",
            path,
            profile,
            f"artifact_id equals path-derived package ID {expected!r}",
            repr(artifact_id),
        )
    ]


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
            path == prefix or prefix in path.parents for prefix in path_prefixes
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
        column for column, count in collections.Counter(header).items() if count > 1
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
            patterns = (
                TEMPLATE_IDENTIFIER_PATTERNS
                if profile.mode == "template"
                else IDENTIFIER_PATTERNS
            )
            pattern = patterns[identifier.kind]
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
                continue
            if (
                identifier.kind == "requirement"
                and profile.profile_id == "sdlc/requirement-package"
                and profile.mode == "authored"
            ):
                package_number = _requirement_package_number(path)
                expected_prefix = (
                    None if package_number is None else f"REQ-{package_number}-"
                )
                if expected_prefix is not None and not value.startswith(
                    expected_prefix
                ):
                    diagnostics.append(
                        _diagnostic(
                            "REQUIREMENT-PACKAGE-MEMBER-ID",
                            path,
                            profile,
                            f"requirement identifier starts with {expected_prefix!r}",
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

        heading_match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
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
            _diagnostic(
                "FM-DATE",
                path,
                profile,
                f"{key} is an ISO calendar date",
                text or type(value).__name__,
            )
        )
        return
    if profile.mode == "authored" and parsed > today:
        diagnostics.append(
            _diagnostic(
                "FM-FUTURE-DATE",
                path,
                profile,
                f"{key} is not future-dated",
                parsed.isoformat(),
            )
        )


def _same_scalar(left: object, right: object) -> bool:
    """Compare JSON/YAML scalars without equating booleans and integers."""

    return type(left) is type(right) and left == right


def _matches_value_kind(value: object, kind: str) -> bool:
    """Return whether one parsed YAML scalar satisfies the registry kind."""

    if kind == "string":
        return isinstance(value, str)
    if kind == "date":
        return isinstance(value, (str, dt.date)) and not isinstance(value, dt.datetime)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and (not isinstance(value, float) or math.isfinite(value))
        )
    if kind == "boolean":
        return isinstance(value, bool)
    return False


def _is_string_sequence(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _value_pattern_text(value: object) -> str:
    """Render one non-null contract scalar to canonical pattern text."""

    if isinstance(value, str):
        return value
    if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
        return value.isoformat()
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _value_rule_id(key: str, constraint: str) -> str:
    """Preserve established key diagnostics for registry-owned keys."""

    if key == "title" and constraint in {"kind", "null", "pattern"}:
        return "FM-TITLE"
    if key == "type":
        return "FM-TYPE"
    if key == "status":
        return "FM-STATUS"
    if key == "owner" and constraint in {"kind", "null", "pattern"}:
        return "FM-OWNER"
    if key in {"updated", "archived_on"} and constraint in {
        "kind",
        "null",
        "pattern",
    }:
        return "FM-DATE"
    return f"FM-VALUE-{constraint.upper()}"


def _value_contract_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    data: dict[str, object],
    today: dt.date,
) -> list[Diagnostic]:
    """Validate frontmatter scalars from the terminal profile contract."""

    diagnostics: list[Diagnostic] = []
    expected_kinds = {
        "title": "string",
        "type": "string",
        "status": "string",
        "owner": "string",
        "updated": "date",
        "archived_on": "date",
        "artifact_id": "string",
        "supersedes": "string-or-sequence",
        "superseded_by": "string-or-sequence",
    }
    for key, kind in expected_kinds.items():
        if key not in data:
            continue
        value = data[key]
        if value is None:
            diagnostics.append(
                _diagnostic(
                    _value_rule_id(key, "null"),
                    path,
                    profile,
                    f"{key} is non-null",
                    "null",
                )
            )
            continue
        kind_matches = (
            (isinstance(value, str) or _is_string_sequence(value))
            if kind == "string-or-sequence"
            else _matches_value_kind(value, kind)
        )
        if not kind_matches:
            diagnostics.append(
                _diagnostic(
                    _value_rule_id(key, "kind"),
                    path,
                    profile,
                    f"{key} has {kind} kind",
                    type(value).__name__,
                )
            )
            continue

        date_placeholder = (
            profile.mode == "template" and kind == "date" and value == "YYYY-MM-DD"
        )
        if kind == "date":
            _validate_date(diagnostics, path, profile, key, value, today)
        if date_placeholder:
            continue

        if key == "type":
            expected = _expected_type(profile)
            if not _same_scalar(value, expected):
                diagnostics.append(
                    _diagnostic(
                        _value_rule_id(key, "constant"),
                        path,
                        profile,
                        repr(expected),
                        repr(value),
                    )
                )
        if key == "status" and not any(
            _same_scalar(value, item) for item in profile.status_domain
        ):
            diagnostics.append(
                _diagnostic(
                    _value_rule_id(key, "enum"),
                    path,
                    profile,
                    repr(profile.status_domain),
                    repr(value),
                )
            )
        if profile.profile_id in STAGE05_PROFILE_IDS:
            pinned = STAGE05_PINNED_FRONTMATTER.get(key)
            if pinned is not None and not _same_scalar(value, pinned):
                diagnostics.append(
                    _diagnostic(
                        _value_rule_id(key, "pattern"),
                        path,
                        profile,
                        repr(pinned),
                        repr(value),
                    )
                )
        if (
            key == "artifact_id"
            and profile.artifact_id_pattern is not None
            and not (
                profile.profile_id == "content/archive"
                and path.parts[:3] == ("docs", "98.archive", "changes")
            )
            and re.search(profile.artifact_id_pattern, _value_pattern_text(value))
            is None
        ):
            diagnostics.append(
                _diagnostic(
                    _value_rule_id(key, "pattern"),
                    path,
                    profile,
                    f"{key} matches {profile.artifact_id_pattern!r}",
                    repr(_value_pattern_text(value)),
                )
            )
    return diagnostics


def _frontmatter_body(
    text: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    diagnostics: list[Diagnostic],
    today: dt.date,
) -> str:
    contract = profile.frontmatter
    if contract.mode == "not-applicable":
        if _has_exact_leading_sdlc_frontmatter(text):
            diagnostics.append(
                _diagnostic(
                    "FM-FORBIDDEN",
                    path,
                    profile,
                    "native syntax without the five-key SDLC frontmatter envelope",
                    "exact leading SDLC five-key block",
                )
            )
        return text
    if contract.mode == "forbidden":
        if text.startswith("---\n"):
            rule = (
                "README_FRONTMATTER"
                if profile.profile_class == "readme"
                else "FM-FORBIDDEN"
            )
            diagnostics.append(
                _diagnostic(
                    rule, path, profile, "frontmatter is forbidden", "frontmatter"
                )
            )
            try:
                _, _, body = extract_frontmatter(text)
                return body
            except ContractError:
                return text
        return text
    try:
        keys, data, body = extract_frontmatter(text)
    except ContractError as exc:
        diagnostics.append(
            _diagnostic(
                exc.rule_id,
                path,
                profile,
                exc.detail,
                "frontmatter" if exc.rule_id == "FM-DELIMITER" else exc.detail,
            )
        )
        return text

    required = tuple(contract.required)
    allowed = tuple(contract.allowed)
    missing = [key for key in required if key not in data]
    extra = [key for key in keys if key not in allowed]
    if missing or extra:
        diagnostics.append(
            _diagnostic(
                "FM-KEYSET",
                path,
                profile,
                json.dumps({"required": required, "allowed": allowed}),
                json.dumps({"missing": missing, "extra": extra}),
            )
        )
    else:
        present_order = tuple(key for key in contract.order if key in data)
        if tuple(keys) != present_order:
            diagnostics.append(
                _diagnostic(
                    "FM-KEY-ORDER",
                    path,
                    profile,
                    json.dumps(present_order),
                    json.dumps(keys),
                )
            )

    diagnostics.extend(_value_contract_diagnostics(path, profile, data, today))
    if (
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
    return body


def _body_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    body: str,
) -> list[Diagnostic]:
    scan = scan_headings(body)
    if (
        profile.frontmatter.mode == "not-applicable"
        and not profile.headings.required
        and not profile.headings.allowed
    ):
        return []
    readme = profile.profile_class == "readme"
    diagnostics: list[Diagnostic] = []
    if scan.unclosed_fence:
        rule = "README_FENCE" if readme else "BODY-FENCE-UNCLOSED"
        diagnostics.append(
            _diagnostic(rule, path, profile, "all fenced blocks are closed", "unclosed")
        )
    if not profile.headings.required and not profile.headings.allowed:
        return diagnostics
    h1 = [title for level, title in scan.headings if level == 1]
    h2 = [title for level, title in scan.headings if level == 2]
    if len(h1) != 1:
        rule = "README_H1" if readme else "BODY-H1"
        diagnostics.append(
            _diagnostic(rule, path, profile, "exactly one H1", json.dumps(h1))
        )
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
    diagnostics.extend(
        _diagnostic(required_rule, path, profile, "required H2", heading)
        for heading in missing
    )
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
            for heading in empty_required_h2_sections(body, profile.headings.required)
            if h2_counts[heading] == 1
        )
    duplicate = sorted(
        heading for heading, count in collections.Counter(h2).items() if count > 1
    )
    duplicate_rule = "README_H2_DUPLICATE" if readme else "BODY-H2-DUPLICATE"
    diagnostics.extend(
        _diagnostic(duplicate_rule, path, profile, "unique H2", heading)
        for heading in duplicate
    )
    represented = set(profile.headings.allowed)
    unsupported_rule = "README_H2_UNSUPPORTED" if readme else "BODY-HEADING-UNSUPPORTED"
    diagnostics.extend(
        _diagnostic(unsupported_rule, path, profile, "allowed H2", heading)
        for heading in h2
        if heading not in represented
    )
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
                diagnostics.append(
                    _diagnostic(
                        "BODY-TEMPLATE-RESIDUE",
                        path,
                        profile,
                        "authored content without legacy/template residue",
                        marker,
                    )
                )
    return diagnostics


def validate_document(
    root: Path,
    path: PurePosixPath,
    profile: DocumentProfile,
    mode: str,
    *,
    today: dt.date | None = None,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Validate one source using only its registry-selected profile contract."""

    return validate_document_text(
        read_repository_text(root, path),
        path,
        profile,
        mode,
        today=today,
        body_contracts=body_contracts,
        body_contract_path_prefixes=body_contract_path_prefixes,
    )


def validate_document_text(
    text: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    mode: str,
    *,
    today: dt.date | None = None,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Validate exact caller-supplied text without consulting filesystem bytes."""

    if mode not in {"compatibility", "strict"}:
        raise ValueError("mode must be compatibility or strict")
    effective_today = today or dt.datetime.now(ZoneInfo("Asia/Seoul")).date()
    diagnostics: list[Diagnostic] = []
    body = _frontmatter_body(text, path, profile, diagnostics, effective_today)
    diagnostics.extend(_body_diagnostics(path, profile, body))
    status = ""
    metadata: dict[str, Any] = {}
    if profile.frontmatter.mode == "required":
        try:
            _, metadata, _ = extract_frontmatter(text)
        except ContractError:
            metadata = {}
        value = metadata.get("status")
        status = value if isinstance(value, str) else ""
    diagnostics.extend(
        _requirement_package_identity_diagnostics(path, profile, metadata)
    )
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

    del root
    if contract is not None:
        raise ValueError("DEBT-SOURCE-REINTRODUCED: retired compatibility contract")
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


def _emit_results(mode: str, output_format: str, rows: Sequence[ResultRow]) -> None:
    if output_format == "json":
        print(
            json.dumps(
                _result_object(mode, rows), ensure_ascii=False, separators=(",", ":")
            )
        )
        return
    if not rows:
        print(
            'PASS SUMMARY . - expected="no violations" actual="0" '
            f"owner={json.dumps(OWNER)}"
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
    parser.add_argument("--include-path", action="append", default=[])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--inventory", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    try:
        registry = load_registry(root)
        include_paths = tuple(PurePosixPath(value) for value in args.include_path)
        native_include_paths = tuple(
            path
            for path in include_paths
            if _native_surface_owner(registry, path) is not None
        )
        markdown_include_paths = tuple(
            path for path in include_paths if path not in native_include_paths
        )
        inventory = enumerate_target_markdown(
            root, include_paths=markdown_include_paths
        )
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
        diagnostics.extend(
            _native_surface_diagnostics(
                root,
                registry,
                include_paths=native_include_paths,
            )
        )
        for path in inventory.current_paths:
            profile = classify_path(registry, path)
            diagnostics.extend(
                validate_document(
                    root,
                    path,
                    profile,
                    args.mode,
                    body_contracts=args.body_contracts,
                    body_contract_path_prefixes=tuple(args.body_contract_path_prefix),
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
