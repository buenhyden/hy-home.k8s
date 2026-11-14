#!/usr/bin/env python3
"""Validate registry-selected Markdown document profiles."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterator, Mapping, Sequence
from zoneinfo import ZoneInfo

from frontmatter_yaml import FrontmatterError, load_frontmatter
from json_schema_validation import SchemaEvaluationError, schema_errors

# This module is the markdown-profile facade over the document contract.
# The names this file does not call itself are re-exported for the
# harness validators that reach the contract through it.
from document_contracts import (
    CommonForm,
    ConditionalConstraint,  # noqa: F401 - re-exported
    ConstantConstraint,  # noqa: F401 - re-exported
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    EnumConstraint,  # noqa: F401 - re-exported
    classify_path,
    diagnostic_sort_key,
    enumerate_tracked_regular_paths,
    enumerate_target_markdown,
    is_opaque_evaluation_output,
    verify_opaque_evaluation_output,
    is_ignored_repository_path,
    load_internal_payload,  # noqa: F401 - re-exported
    load_registry,
    read_repository_text,
    scoped_document_content_paths,
    validated_changed_paths,
    task_status,
    task_contract_issues,
    direct_parent,
    MARKDOWN_TEMPLATE_PLACEHOLDER,
    validate_registry,  # noqa: F401 - re-exported
    _parse_ls_files_stage_z,
    _run_git,
)
import document_language
from validation.document_content import validate_document_content


SDLC_FRONTMATTER_KEYS = ("title", "type", "status", "owner", "updated")
# Stage 05 documents are platform-owned.  The shared registry constrains owner
# to any string, so owner is pinned per profile here, where the other
# frontmatter values are already checked.  Status is not pinned: the
# registry's status domain already bounds the value.
STAGE05_PROFILE_IDS = frozenset(
    {
        "operation/guide",
        "operation/policy",
        "operation/runbook",
        "operation/incident",
        "operation/postmortem",
    }
)
STAGE05_PINNED_FRONTMATTER = {"owner": "platform"}
NATIVE_TRACKED_PATHSPECS = (
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "docs/03.specs",
)
OWNER = "markdown-profile-validator"
FRONTMATTER_SCHEMA_PATH = PurePosixPath(
    "docs/99.templates/contracts/frontmatter.schema.json"
)

AUTHOR_PROMPT_MARKER = "Author prompt:"
AUTHOR_PROMPT_COMMENT = re.compile(r"(?m)^[ \t]*<!-- Author prompt:")
GENERIC_RESIDUE = (
    "Target: docs/",
    "Use this template",
    "Replace every placeholder with researched, topic-specific content.",
)
STARTER_PLACEHOLDER = re.compile(r"\[[^\]\n]+\]|\{[^}\n]+\}|<[^>\n]+>|#{3,}")


class ContractError(ValueError):
    """One deterministic Markdown preprocessing failure."""

    def __init__(self, rule_id: str, detail: str):
        self.rule_id = rule_id
        self.detail = detail
        super().__init__(detail)


def extract_frontmatter(text: str) -> tuple[list[str], dict[str, object], str]:
    """Extract an exact leading YAML mapping without losing key order."""

    if not text.startswith("---\n"):
        raise ContractError("FM-DELIMITER", "first line must be ---")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ContractError("FM-DELIMITER", "frontmatter is not closed")
    raw = text[4:closing]
    try:
        data = load_frontmatter(raw) or {}
    except FrontmatterError as exc:
        if exc.reason == "duplicate-key":
            raise ContractError("FM-DUPLICATE-KEY", str(exc.key)) from exc
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
        and re.fullmatch(r"[a-z][a-z0-9]*/[a-z][a-z0-9-]*", document_type) is not None
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
    return None


def _is_native_candidate_path(path: PurePosixPath) -> bool:
    parts = path.parts
    return (
        len(parts) == 3
        and parts[:2]
        in {
            (".github", "ISSUE_TEMPLATE"),
            (".github", "workflows"),
        }
        and path.suffix in {".yml", ".yaml"}
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
        if not _is_native_candidate_path(path):
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
        owner, _ = selection
        source = read_repository_text(root, path)
        if not _has_exact_leading_sdlc_frontmatter(source):
            continue
        diagnostics.append(
            Diagnostic(
                rule_id="FM-FORBIDDEN",
                path=path,
                profile=owner,
                expected=(
                    "GitHub-native YAML without the five-key SDLC frontmatter envelope"
                ),
                actual="exact leading SDLC five-key block",
                owner=OWNER,
            )
        )
    return diagnostics


@dataclass(frozen=True)
class HeadingScan:
    headings: tuple[tuple[int, str], ...]
    unclosed_fence: bool
    # One tuple of (line, fenced) pairs per heading: the visible lines up to the
    # next heading of any level, HTML comments removed and fenced code flagged.
    bodies: tuple[tuple[tuple[str, bool], ...], ...] = ()


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
    bodies: list[list[tuple[str, bool]]] = []
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
            elif bodies:
                bodies[-1].append((raw_line, True))
            continue
        line, in_comment = _strip_html_comments(raw_line, in_comment)
        match = opening.match(line)
        if match:
            marker = match.group(1)
            if marker[0] == "`" and "`" in match.group(2):
                if bodies:
                    bodies[-1].append((line, False))
                continue
            fence_character = marker[0]
            fence_length = len(marker)
            continue
        match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
        if not match:
            if bodies:
                bodies[-1].append((line, False))
            continue
        title = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(2).strip()).strip()
        headings.append((len(match.group(1)), title))
        bodies.append([])
    return HeadingScan(
        tuple(headings),
        fence_character is not None,
        tuple(tuple(body) for body in bodies),
    )


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


def _visible_tables(text: str) -> Iterator[tuple[list[str], list[list[str]]]]:
    """Yield every valid pipe-led GFM table outside comments and fences, in order."""

    lines = _visible_markdown(text).splitlines()
    index = 0
    while index < len(lines) - 1:
        start, index = index, index + 1
        if re.match(r"^ {0,3}\|", lines[start]) is None:
            continue
        header = _gfm_table_cells(lines[start])
        delimiter = _gfm_table_cells(lines[start + 1])
        if len(header) != len(delimiter) or not header:
            continue
        if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in delimiter):
            continue
        rows: list[list[str]] = []
        for row_line in lines[start + 2 :]:
            if not row_line.strip():
                break
            if re.match(r"^ {0,3}\|", row_line) is None:
                break
            rows.append(_gfm_table_cells(row_line))
        index = start + 2 + len(rows)
        yield header, rows


def _first_visible_table(
    text: str,
) -> tuple[list[str], list[list[str]]] | None:
    """Return the first valid pipe-led GFM table outside comments and fences."""

    return next(_visible_tables(text), None)


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


def expected_artifact_id(
    path: PurePosixPath,
    profile: DocumentProfile,
) -> str | None:
    """Derive one concrete identity after the Registry selected the path."""

    profile_id = profile.profile_id
    if profile_id in {
        "sdlc/requirement",
        "sdlc/architecture-description",
        "sdlc/architecture-decision",
        "operation/guide",
        "operation/policy",
        "operation/runbook",
    }:
        number = path.name[:4]
        prefix = {
            "sdlc/requirement": "REQ",
            "sdlc/architecture-description": "AD",
            "sdlc/architecture-decision": "ADR",
            "operation/guide": "GDE",
            "operation/policy": "POL",
            "operation/runbook": "RUN",
        }[profile_id]
        return f"{prefix}-{number}"
    if profile_id in {"sdlc/spec", "sdlc/plan", "sdlc/task"}:
        try:
            package_number = path.parts[path.parts.index("03.specs") + 1][:4]
        except (ValueError, IndexError):
            return None
        if profile_id == "sdlc/spec":
            return f"SPEC-{package_number}"
        if profile_id == "sdlc/plan":
            return f"SPEC-{package_number}-PLAN-0001"
        return f"SPEC-{package_number}-TSK-{path.name[4:8]}"
    if profile_id in {"operation/incident", "operation/postmortem"}:
        year = path.parent.parent.name
        incident_number = path.parent.name[4:8]
        suffix = "-PM" if profile_id == "operation/postmortem" else ""
        return f"inc-{year}-{incident_number}{suffix}"
    if profile_id in {
        "reference/audit-pack",
        "reference/research-pack",
        "reference/data-pack",
    }:
        prefix = {
            "reference/audit-pack": "AUD",
            "reference/research-pack": "RES",
            "reference/data-pack": "DATA",
        }[profile_id]
        return f"{prefix}-{path.parent.name[:4]}"
    if profile_id in {"reference/audit", "reference/research", "reference/data"}:
        prefix = {
            "reference/audit": "AUD",
            "reference/research": "RES",
            "reference/data": "DATA",
        }[profile_id]
        return f"{prefix}-{path.parent.name[:4]}-{path.stem[:5]}"
    return None


def artifact_identity_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    metadata: Mapping[str, Any],
) -> list[Diagnostic]:
    """Bind every Registry-numbered document ID to its selected route."""

    expected = expected_artifact_id(path, profile)
    artifact_id = metadata.get("artifact_id")
    if expected is None or not isinstance(artifact_id, str):
        return []
    if artifact_id == expected:
        return []
    return [
        _diagnostic(
            (
                "REQUIREMENT-PACKAGE-IDENTITY"
                if profile.profile_id == "sdlc/requirement"
                else "ARTIFACT-IDENTITY"
            ),
            path,
            profile,
            f"artifact_id equals path-derived identity {expected!r}",
            repr(artifact_id),
        )
    ]


def current_artifact_identities(
    documents: Sequence[tuple[PurePosixPath, DocumentProfile, str]],
) -> tuple[tuple[PurePosixPath, str], ...]:
    """Read only the outer frontmatter identity of current concrete records."""

    identities: dict[PurePosixPath, str] = {}
    for path, profile, text in documents:
        if profile.mode == "template" or profile.artifact_id_pattern is None:
            continue
        try:
            _, metadata, _ = extract_frontmatter(text)
        except ContractError:
            continue
        artifact_id = metadata.get("artifact_id")
        if not isinstance(artifact_id, str) or MARKDOWN_TEMPLATE_PLACEHOLDER.fullmatch(
            artifact_id
        ):
            continue
        identities[path] = artifact_id
    return tuple(sorted(identities.items(), key=lambda item: item[0].as_posix()))


def artifact_identity_uniqueness_diagnostics(
    documents: Sequence[tuple[PurePosixPath, DocumentProfile, str]],
) -> list[Diagnostic]:
    """Reject one concrete current ID owned by more than one tracked path."""

    profiles = {path: profile for path, profile, _ in documents}
    owners: dict[str, list[PurePosixPath]] = collections.defaultdict(list)
    for path, artifact_id in current_artifact_identities(documents):
        owners[artifact_id].append(path)
    diagnostics: list[Diagnostic] = []
    for artifact_id, paths in sorted(owners.items()):
        if len(paths) < 2:
            continue
        rendered = ", ".join(path.as_posix() for path in paths)
        for path in paths:
            diagnostics.append(
                _diagnostic(
                    "ARTIFACT-IDENTITY-DUPLICATE",
                    path,
                    profiles[path],
                    "one current concrete artifact_id per governed path",
                    f"{artifact_id!r} at {rendered}",
                )
            )
    return sorted(diagnostics, key=diagnostic_sort_key)


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
    if profile.body_contract.task_execution is not None:
        return True
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
        if len(row) != len(header):
            # A padded or truncated row would hide its cells from every check.
            diagnostics.append(
                _diagnostic(
                    "BODY-CONTRACT-ROW-WIDTH",
                    path,
                    profile,
                    f"{len(header)} cells, as in the header",
                    f"row {row_index}: {len(row)} cells",
                )
            )
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
            if (
                contract.task_execution is not None
                and identifier.column == "Upstream criterion"
            ):
                continue  # The Task binding accepts a list of linked criteria.
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
                and profile.profile_id == "sdlc/requirement"
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


def _form_heading(form: CommonForm, section_id: str) -> tuple[int, str] | None:
    """The heading level and title of a form section or local H3 extension."""

    for section in form.sections:
        if section.section_id == section_id:
            return section.level, section.title
        for child in section.children:
            if child.section_id == section_id:
                return child.level, child.title
    for extension in form.extensions:
        if (
            extension.kind == "local_h3"
            and extension.extension_id == section_id
            and extension.title is not None
        ):
            return 3, extension.title
    return None


def _table_diagnostics(
    path: PurePosixPath, profile: DocumentProfile, body: str
) -> list[Diagnostic]:
    """SPEC-0169: check the profile's template tables inside their sections.

    A table is identified by its first header cell. The table the body contract
    owns keeps its own checks, and a non-unique section heading is left to the
    heading-tree check.
    """

    owned = profile.body_contract.table_heading if profile.body_contract else None
    found: list[Diagnostic] = []
    for table in profile.tables:
        if profile.form is None:
            # A role without a form records the template's own heading line.
            heading_line: str | None = table.section
        else:
            heading = _form_heading(profile.form, table.section)
            heading_line = (
                None if heading is None else "#" * heading[0] + " " + heading[1]
            )
        if table.name == owned or heading_line is None:
            continue
        section = _exact_heading_section(body, heading_line)
        if section is None:
            continue
        keys = [column.key for column in table.columns]
        # Optional columns trail the required ones, so a header may stop early.
        required = sum(column.required for column in table.columns)
        rows = 0
        for header, data in _visible_tables(section):
            if header[0] != keys[0]:
                continue
            rows += len(data)
            if header != keys[: len(header)] or len(header) < required:
                found.append(
                    _diagnostic(
                        "BODY-TABLE-COLUMNS",
                        path,
                        profile,
                        f"{table.name}: {json.dumps(keys, ensure_ascii=False)}",
                        json.dumps(header, ensure_ascii=False),
                    )
                )
        if rows < table.minimum_rows:
            found.append(
                _diagnostic(
                    "BODY-TABLE-ROWS",
                    path,
                    profile,
                    f"{table.name}: at least {table.minimum_rows} data rows",
                    f"{rows} rows",
                )
            )
    return found


def _template_table_section_diagnostics(
    path: PurePosixPath, profile: DocumentProfile, body: str
) -> list[Diagnostic]:
    """BODY-TABLE-SECTION: a template of a role without a form holds each recorded
    table heading line exactly once, under an H2 of the required list."""

    if profile.form is not None:
        return []
    lines = _visible_markdown(body).splitlines()
    found: list[Diagnostic] = []
    for table in profile.tables:
        matches = [index for index, line in enumerate(lines) if line == table.section]
        if len(matches) != 1:
            found.append(
                _diagnostic(
                    "BODY-TABLE-SECTION",
                    path,
                    profile,
                    f"{table.name}: {table.section!r} exactly once outside "
                    "fences and comments",
                    f"{len(matches)} times",
                )
            )
            continue
        h2 = next(
            (
                lines[index][3:]
                for index in range(matches[0], -1, -1)
                if lines[index].startswith("## ")
            ),
            None,
        )
        if h2 not in profile.headings.required:
            found.append(
                _diagnostic(
                    "BODY-TABLE-SECTION",
                    path,
                    profile,
                    f"{table.name}: a heading line under an H2 of the required list",
                    f"{table.section!r} under {h2!r}",
                )
            )
    return found


_RULE_ID_TEXT = r"[A-Z][A-Z0-9]{1,7}-R[0-9]{3}"
_RULE_TOKEN = re.compile(rf"`({_RULE_ID_TEXT})`(?:\s|$)")
_RULE_TOKEN_LINE = re.compile(rf"`({_RULE_ID_TEXT})`\s*")
_RULE_STATUS_RETIRED = re.compile(rf"retired; (none|{_RULE_ID_TEXT})")
_LIST_ITEM = re.compile(r"^( *)(?:[-*+]|[0-9]{1,9}[.)])[ \t]+(.*)$")
_H4_HEADING = re.compile(r"^ {0,3}####[ \t]+(.*?)[ \t]*$")
_THEMATIC_BREAK = re.compile(r"^ {0,3}([-*_])(?:[ \t]*\1){2,}[ \t]*$")
RULES_COLUMN_FIRST = "Rule ID"
CONTROL_COLUMN_FIRST = "Control"


@dataclass(frozen=True)
class RuleUnit:
    """One rule unit read under Requirements and its definition token, if any."""

    kind: str  # "item", "row" or "group"
    token: str | None
    covered: bool  # begins with a token or lies in an H4 group that carries one
    text: str


@dataclass(frozen=True)
class RuleScan:
    """What the policy rule reader finds under one Requirements section."""

    items: tuple[RuleUnit, ...]  # top-level list items
    rows: tuple[RuleUnit, ...]  # table rows outside control registers and Rules tables
    groups: tuple[RuleUnit, ...]  # H4 groups with content beyond those tables
    control_rows: int
    tokens: tuple[str, ...]  # every definition token, in reading order
    rules_tables: tuple[tuple[tuple[str, ...], tuple[tuple[str, ...], ...]], ...]

    @property
    def units(self) -> tuple[RuleUnit, ...]:
        return (*self.items, *self.rows, *self.groups)


def _scan_requirements(section: str) -> RuleScan:
    """SPEC-0194: read the rule units, tokens and Rules tables of one section.

    Only visible Markdown is read. A definition token is a code span holding one
    rule ID as the first content of a list item or of the first cell of a table
    row, or as a paragraph of its own directly under an H4 heading; it then
    identifies the whole H4 group. Heading text never carries one.
    """

    lines = _visible_markdown(section).splitlines()
    items: list[RuleUnit] = []
    rows: list[RuleUnit] = []
    groups: list[RuleUnit] = []
    tokens: list[str] = []
    rules_tables: list[tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]] = []
    control_rows = 0
    # The open H4 group: its title, token, content flag and the units seen in it.
    group: dict[str, Any] | None = None

    def close_group() -> None:
        if group is not None and group["content"]:
            groups.append(
                RuleUnit(
                    "group", group["token"], group["token"] is not None, group["title"]
                )
            )

    def covered(token: str | None) -> bool:
        return token is not None or (group is not None and group["token"] is not None)

    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        heading = _H4_HEADING.match(line)
        if heading is not None:
            close_group()
            group = {"title": heading.group(1), "token": None, "content": False}
            following = index
            while following < len(lines) and not lines[following].strip():
                following += 1
            if following < len(lines):
                match = _RULE_TOKEN_LINE.fullmatch(lines[following].strip())
                after = lines[following + 1] if following + 1 < len(lines) else ""
                if match is not None and not after.strip():
                    group["token"] = match.group(1)
                    tokens.append(match.group(1))
                    index = following + 1
            continue
        if not line.strip() or _THEMATIC_BREAK.match(line):
            continue
        if re.match(r"^ {0,3}\|", line) and index < len(lines):
            header = _gfm_table_cells(line)
            delimiter = _gfm_table_cells(lines[index])
            if (
                header
                and len(header) == len(delimiter)
                and all(re.fullmatch(r":?-{3,}:?", cell) for cell in delimiter)
            ):
                data: list[list[str]] = []
                cursor = index + 1
                while cursor < len(lines) and re.match(r"^ {0,3}\|", lines[cursor]):
                    data.append(_gfm_table_cells(lines[cursor]))
                    cursor += 1
                index = cursor
                if header[0] == CONTROL_COLUMN_FIRST:
                    control_rows += len(data)
                elif header[0] == RULES_COLUMN_FIRST:
                    rules_tables.append(
                        (tuple(header), tuple(tuple(row) for row in data))
                    )
                else:
                    for row in data:
                        first = row[0] if row else ""
                        match = _RULE_TOKEN.match(first)
                        token = match.group(1) if match else None
                        if token is not None:
                            tokens.append(token)
                        rows.append(RuleUnit("row", token, covered(token), first[:60]))
                    if group is not None:
                        group["content"] = True
                continue
        item = _LIST_ITEM.match(line)
        if item is not None:
            match = _RULE_TOKEN.match(item.group(2))
            token = match.group(1) if match else None
            if token is not None:
                tokens.append(token)
            if not item.group(1):
                items.append(
                    RuleUnit("item", token, covered(token), item.group(2)[:60])
                )
        if group is not None:
            group["content"] = True
    close_group()
    return RuleScan(
        tuple(items),
        tuple(rows),
        tuple(groups),
        control_rows,
        tuple(tokens),
        tuple(rules_tables),
    )


def policy_rule_units(text: str, heading: str = "### Requirements") -> RuleScan:
    """The unit inventory of one policy's Requirements section, empty without it."""

    section = _exact_heading_section(text, heading)
    return _scan_requirements("" if section is None else section)


def _rules_status_fault(
    status: str, own: str, row_ids: Sequence[str], codes: frozenset[str]
) -> str | None:
    if status == "active":
        return None
    match = _RULE_STATUS_RETIRED.fullmatch(status)
    if match is None:
        return "active, or retired; followed by a successor rule ID or none"
    successor = match.group(1)
    if successor == "none":
        return None
    if successor.rsplit("-R", 1)[0] not in codes:
        return "a successor rule ID with a registered code"
    if successor == own or successor not in row_ids:
        return "a successor that names another row of this table"
    return None


def _policy_rule_diagnostics(
    path: PurePosixPath, profile: DocumentProfile, body: str
) -> list[Diagnostic]:
    """SPEC-0194: the policy rule ID rules over one authored policy body.

    A pending record applies the adoption gate alone; an adopted one applies the
    table, ID, inline-token and coverage rules; a document with no record fails
    POLICY-RULE-CODE when it states normative rules or carries a Rules table.
    """

    ids = profile.policy_rule_ids
    table = next((item for item in profile.tables if item.name == "Rules"), None)
    heading = (
        None
        if ids is None or table is None or profile.form is None
        else _form_heading(profile.form, table.section)
    )
    if heading is None or profile.mode != "authored":
        return []
    section = _exact_heading_section(body, "#" * heading[0] + " " + heading[1])
    if section is None:
        return []
    scan = _scan_requirements(section)
    carried = sum(
        header[0] == RULES_COLUMN_FIRST for header, _ in _visible_tables(body)
    )
    record = next((item for item in ids.codes if item.path == path.as_posix()), None)

    def found(rule: str, expected: str, actual: str) -> Diagnostic:
        return _diagnostic(rule, path, profile, expected, actual)

    if record is None:
        if scan.units or carried:
            return [
                found(
                    "POLICY-RULE-CODE",
                    "a rule ID code registered in policy_rule_ids for this policy",
                    "no record for a policy that states normative rules "
                    "or carries a Rules table",
                )
            ]
        return []
    if record.state == "pending":
        if carried or scan.tokens:
            return [
                found(
                    "POLICY-RULE-ADOPTION",
                    "no Rules table and no definition token while the record is pending",
                    f"{carried} Rules tables and {len(scan.tokens)} definition tokens",
                )
            ]
        return []

    found_all: list[Diagnostic] = []

    def add(rule: str, expected: str, actual: str) -> None:
        found_all.append(found(rule, expected, actual))

    keys = tuple(column.key for column in table.columns)
    stated = bool(scan.units)
    if carried != len(scan.rules_tables):
        add(
            "POLICY-RULE-TABLE",
            "the Rules table under Requirements only",
            f"{carried - len(scan.rules_tables)} outside it",
        )
    if len(scan.rules_tables) > 1:
        add("POLICY-RULE-TABLE", "exactly one Rules table", f"{len(scan.rules_tables)}")
    if stated and not scan.rules_tables:
        add(
            "POLICY-RULE-TABLE",
            f"a Rules table when {ids.rules_table_condition}",
            "no Rules table",
        )
    row_ids: list[str] = []
    statuses: list[str] = []
    readable = not scan.rules_tables
    if scan.rules_tables:
        header, data = scan.rules_tables[0]
        readable = header == keys and all(len(row) == len(keys) for row in data)
        if header != keys:
            add("POLICY-RULE-TABLE", json.dumps(keys), json.dumps(header))
        elif not readable:
            add("POLICY-RULE-TABLE", f"{len(keys)} cells in every row", "ragged row")
        if readable:
            if stated and len(data) < ids.rules_table_minimum_rows:
                add(
                    "POLICY-RULE-TABLE",
                    f"at least {ids.rules_table_minimum_rows} row when "
                    f"{ids.rules_table_condition}",
                    f"{len(data)} rows",
                )
            level_at, status_at = keys.index("Level"), keys.index("Status")
            row_ids = [_identifier_text(row[0]) for row in data]
            statuses = [row[status_at] for row in data]
            codes = frozenset(item.code for item in ids.codes)
            for number, (row, own, status) in enumerate(
                zip(data, row_ids, statuses), start=1
            ):
                if own != f"{record.code}-R{number:03d}":
                    add(
                        "POLICY-RULE-ID",
                        f"{record.code}-R{number:03d}: this policy's code, "
                        "ascending from R001 without a gap or duplicate",
                        own,
                    )
                if row[level_at] not in ids.levels:
                    add(
                        "POLICY-RULE-TABLE",
                        f"{own}: a level of {list(ids.levels)}",
                        row[level_at],
                    )
                fault = _rules_status_fault(status, own, row_ids, codes)
                if fault is not None:
                    add("POLICY-RULE-TABLE", f"{own}: Status {fault}", status)
    if readable:
        counts = collections.Counter(scan.tokens)
        active = {own for own, status in zip(row_ids, statuses) if status == "active"}
        for own in sorted(active):
            if counts[own] != 1:
                add(
                    "POLICY-RULE-INLINE",
                    f"{own}: one definition token for an active row",
                    f"{counts[own]} tokens",
                )
        for token in sorted(set(counts) - active):
            add(
                "POLICY-RULE-INLINE",
                f"{token}: an active Rules table row for each definition token",
                "no active row",
            )
    for unit in (*scan.items, *scan.rows):
        if not unit.covered:
            add(
                "POLICY-RULE-COVERAGE",
                f"a definition token on this {unit.kind} or in its H4 group",
                unit.text,
            )
    return found_all


def starter_placeholder(value: str) -> str | None:
    """Return one unresolved starter token from a title or H1."""

    match = STARTER_PLACEHOLDER.search(value)
    return match.group(0) if match else None


@dataclass(frozen=True)
class RequiredH2Content:
    empty: tuple[str, ...]
    nested_roles: tuple[str, ...]


_BARE_PLACEHOLDER = re.compile(r"(?i)^(?:TBD|TODO|N/A|NA|pending)[\s.!?]*$")
# One bare statement: a closed English "states no <words>" shape, or one Korean
# sentence about this document that ends in 없다. with no reason connective.
_BARE_STATEMENT = re.compile(
    r"None is stated in this document\."
    r"|This (?:file|policy|document|README|skill|procedure) (?:states|marks) no "
    r"[\w -]+\."
    r"|이 (?:문서|README|정책)[^.]*없다\."
)
BARE_EXPECTED = "a section that states its reason and follow-up condition"
_BARE_REASON_CONNECTIVE = re.compile(r"이며|므로|때문")
_TABLE_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$")
_EMPTY_HTML_ANCHOR = re.compile(r"(?i)<a\b[^>]*>\s*</a>|<a\b[^>]*/>")
_CHECKBOX_MARKER = re.compile(r"^\[[ xX]\](?:\s+|$)")
_MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)|<[a-z][a-z0-9+.-]*:[^>]*>")
# Sections whose job is navigation may consist of links alone.
_LINK_ONLY_SECTIONS = frozenset({"Related Documents"})


def _substantive_section_body(
    lines: Sequence[tuple[str, bool]], *, links_are_content: bool = True
) -> bool:
    """Recognize authored prose, table data, or code, leaving facts to review.

    Outside navigation sections a prose line made only of links is not
    content: a link points at an instruction, it does not state one.
    """

    table_data = False
    for index, (raw_line, fenced_code) in enumerate(lines):
        line = raw_line.strip()
        if not line:
            table_data = False
            continue
        if fenced_code:
            if not _BARE_PLACEHOLDER.fullmatch(line):
                return True
            continue
        if _TABLE_SEPARATOR.fullmatch(line):
            table_data = True
            continue
        if "|" in line:
            if table_data:
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                if any(
                    cell and not _BARE_PLACEHOLDER.fullmatch(cell) for cell in cells
                ):
                    return True
                continue
            next_line = lines[index + 1][0].strip() if index + 1 < len(lines) else ""
            if _TABLE_SEPARATOR.fullmatch(next_line) or (
                line.startswith("|") and line.endswith("|")
            ):
                continue
        table_data = False
        prose = _EMPTY_HTML_ANCHOR.sub("", line).strip()
        prose = re.sub(r"^(?:[-*+]|\d+[.)]|>)\s+", "", prose)
        prose = _CHECKBOX_MARKER.sub("", prose)
        prose = prose.strip("*_`~ ")
        if not links_are_content and not re.search(
            r"\w", _MARKDOWN_LINK.sub("", prose)
        ):
            continue
        if prose and not _BARE_PLACEHOLDER.fullmatch(prose) and prose != "---":
            return True
    return False


def _scan_required_h2_content(
    markdown: str, required_headings: Sequence[str], *, substantive_body: bool
) -> RequiredH2Content:
    """Scan required H2 bodies once, preserving the legacy empty-body rule."""

    required = frozenset(required_headings)
    empty: list[str] = []
    nested_roles: list[str] = []
    current_heading: str | None = None
    current_has_content = False
    current_lines: list[tuple[str, bool]] = []
    fence_character: str | None = None
    fence_length = 0
    in_comment = False
    opening = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")

    def close_current() -> None:
        nonlocal current_heading, current_has_content, current_lines
        if current_heading is not None and not (
            _substantive_section_body(
                current_lines,
                links_are_content=current_heading in _LINK_ONLY_SECTIONS,
            )
            if substantive_body
            else current_has_content
        ):
            empty.append(current_heading)
        current_heading = None
        current_has_content = False
        current_lines = []

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
                if substantive_body:
                    current_lines.append((raw_line, True))
            continue

        line, in_comment = _strip_html_comments(raw_line, in_comment)
        match = opening.match(line)
        if match:
            marker = match.group(1)
            if marker[0] == "`" and "`" in match.group(2):
                if current_heading is not None and line.strip():
                    current_has_content = True
                    if substantive_body:
                        current_lines.append((line, False))
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
            else:
                if current_heading is not None:
                    current_has_content = True
                if substantive_body and title in required:
                    nested_roles.append(title)
            continue

        if current_heading is not None and line.strip():
            current_has_content = True
            if substantive_body:
                current_lines.append((line, False))

    close_current()
    return RequiredH2Content(tuple(empty), tuple(nested_roles))


def empty_required_h2_sections(
    markdown: str, required_headings: Sequence[str]
) -> tuple[str, ...]:
    """Return empty required H2 bodies under the historical content rule."""

    return _scan_required_h2_content(
        markdown, required_headings, substantive_body=False
    ).empty


def _diagnostic(
    rule_id: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    expected: str,
    actual: str,
) -> Diagnostic:
    return Diagnostic(rule_id, path, profile.profile_id, expected, actual, OWNER)


def _frontmatter_value_style_diagnostics(
    text: str,
    path: PurePosixPath,
    profile: DocumentProfile,
) -> list[Diagnostic]:
    """Require canonical JSON-style quoting in current-generation metadata."""

    lines = text.splitlines()
    try:
        closing_delimiter = lines.index("---", 1)
    except ValueError:
        return []

    diagnostics: list[Diagnostic] = []
    for line in lines[1:closing_delimiter]:
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):[ \t]+(.+)", line)
        if match is None:
            continue
        key, raw_value = match.groups()
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError:
            value = None
        if isinstance(value, str) or (
            isinstance(value, list) and all(isinstance(item, str) for item in value)
        ):
            continue
        if (
            profile.mode in {"native", "template"}
            and isinstance(dict(profile.constants).get(key), bool)
            and isinstance(value, bool)
        ):
            continue
        diagnostics.append(
            _diagnostic(
                "FM-QUOTE",
                path,
                profile,
                "a double-quoted scalar or JSON string array",
                key,
            )
        )
    return diagnostics


def _expected_type(profile: DocumentProfile) -> str:
    declared_type = dict(profile.constants).get("type")
    if isinstance(declared_type, str):
        return declared_type
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
    if profile.mode == "template" and MARKDOWN_TEMPLATE_PLACEHOLDER.fullmatch(
        text or ""
    ):
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
    if key == "updated" and constraint in {
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
    for key, expected in profile.constants:
        if key in {"type", "status"} or key not in data:
            continue
        if not _same_scalar(data[key], expected):
            diagnostics.append(
                _diagnostic(
                    "FM-VALUE-CONSTANT", path, profile, repr(expected), repr(data[key])
                )
            )
    expected_kinds = {
        "title": "string",
        "type": "string",
        "status": "string",
        "owner": "string",
        "updated": "date",
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

        template_placeholder = (
            profile.mode == "template"
            and isinstance(value, str)
            and MARKDOWN_TEMPLATE_PLACEHOLDER.fullmatch(value) is not None
        )
        if template_placeholder:
            continue
        if kind == "date":
            _validate_date(diagnostics, path, profile, key, value, today)

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


def load_frontmatter_schema(root: Path) -> dict[str, Any] | None:
    """Load the authored frontmatter value contract when the root ships one."""

    path = root / FRONTMATTER_SCHEMA_PATH
    if not path.is_file():
        return None
    schema = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise ValueError("frontmatter schema must be a JSON object")
    return schema


def _schema_scalar(value: object) -> object:
    """Render one YAML scalar the way the frontmatter schema declares it."""

    if isinstance(value, dt.datetime):
        return value.isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    return value


def _frontmatter_schema_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    data: Mapping[str, object],
    schema: Mapping[str, Any] | None,
) -> list[Diagnostic]:
    """Validate frontmatter values against the repository value contract.

    Template forms are exempt: their placeholders deliberately spell a grammar
    the authored contract rejects, which is what makes them placeholders.
    """

    if (
        schema is None
        or profile.mode == "template"
        or (
            profile.profile_class == "exception"
            and profile.profile_id != "common/native-skill-package"
        )
    ):
        return []
    if profile.mode == "native":
        if profile.profile_id != "common/native-skill-package":
            return []
        nested = data.get("metadata")
        if not isinstance(nested, dict):
            return [
                _diagnostic(
                    "FM-SCHEMA",
                    path,
                    profile,
                    "nested Skill document metadata",
                    "missing metadata",
                )
            ]
        if (
            tuple(nested) != ("title", "version", "type", "status", "owner", "updated")
            or nested.get("type") != "governance/skill"
            or nested.get("status") not in profile.status_domain
        ):
            return [
                _diagnostic(
                    "FM-SCHEMA",
                    path,
                    profile,
                    "ordered common Skill metadata with its own lifecycle type and status",
                    "invalid native document metadata",
                )
            ]
        data = nested
    payload = {key: _schema_scalar(value) for key, value in data.items()}
    try:
        errors = schema_errors(dict(schema), payload)
    except SchemaEvaluationError:
        return [
            _diagnostic(
                "FM-SCHEMA",
                path,
                profile,
                "an evaluable frontmatter value contract",
                "schema evaluation failed",
            )
        ]
    return [
        _diagnostic(
            "FM-SCHEMA",
            path,
            profile,
            error.message,
            error.json_path or "frontmatter",
        )
        for error in errors
    ]


def _frontmatter_body(
    text: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    diagnostics: list[Diagnostic],
    today: dt.date,
    frontmatter_schema: Mapping[str, Any] | None = None,
) -> str:
    contract = profile.frontmatter
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

    diagnostics.extend(_frontmatter_value_style_diagnostics(text, path, profile))

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
    if profile.mode != "template":
        parent = direct_parent(path, profile.profile_id)
        if parent is not None and data.get("parent_ids") != [parent[1]]:
            diagnostics.append(
                _diagnostic(
                    "PARENT-IDENTITY",
                    path,
                    profile,
                    f"parent_ids equals {[parent[1]]!r}",
                    repr(data.get("parent_ids")),
                )
            )
        if (
            task_status(data, text, profile) == "cancelled"
            and "cancellation" in contract.allowed
        ):
            cancellation = data.get("cancellation")
            fields = ("reason", "authorization_ref", "criteria_disposition")
            if (
                not isinstance(cancellation, dict)
                or set(cancellation) != set(fields)
                or any(
                    not isinstance(cancellation.get(key), str)
                    or not cancellation[key].strip()
                    for key in fields
                )
            ):
                diagnostics.append(
                    _diagnostic(
                        "FM-CANCELLATION",
                        path,
                        profile,
                        "reason, authorization_ref and criteria_disposition",
                        "missing or invalid cancellation",
                    )
                )
        if (
            "layer" in data
            and "layer" in contract.allowed
            and data.get("status") != "accepted"
        ):
            diagnostics.append(
                _diagnostic(
                    "FM-LAYER-ADR",
                    path,
                    profile,
                    "layer only on a document whose status is accepted",
                    f"layer on status {data.get('status')!r}",
                )
            )
        if (
            profile.profile_id == "operation/incident"
            and data.get("status") == "resolved"
        ):
            try:
                value = data.get("resolved_at")
                resolved_at = (
                    dt.datetime.fromisoformat(value) if isinstance(value, str) else None
                )
                if resolved_at is None or resolved_at.utcoffset() is None:
                    raise ValueError("missing timezone")
            except ValueError:
                diagnostics.append(
                    _diagnostic(
                        "INCIDENT-RESOLVED-AT",
                        path,
                        profile,
                        "real resolved_at calendar timestamp with timezone",
                        repr(data.get("resolved_at")),
                    )
                )
            # SPEC-0171: the Incident form holds resolution evidence in its
            # unique Recovery Verification H3 (its Resolution parent is
            # enforced by BODY-H3-PARENT in the tree check, not here).
            recovery = _exact_heading_section(body, "### Recovery Verification")
            if (
                not recovery
                or not recovery.strip()
                or re.fullmatch(r"(?is)\s*(?:TBD|Pending|N/A|<!--.*?-->)\s*", recovery)
            ):
                diagnostics.append(
                    _diagnostic(
                        "INCIDENT-RESOLUTION-EVIDENCE",
                        path,
                        profile,
                        "concrete Recovery Verification resolution evidence",
                        "missing resolution evidence",
                    )
                )
    diagnostics.extend(
        _frontmatter_schema_diagnostics(path, profile, data, frontmatter_schema)
    )
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


def _form_tree_diagnostics(
    path: PurePosixPath, profile: DocumentProfile, scan: HeadingScan
) -> list[Diagnostic]:
    """SPEC-0168 QA-C02: check the H2 and H3 headings against the role's form."""

    form = profile.form
    assert form is not None
    found: list[Diagnostic] = []

    def add(rule_id: str, expected: str, actual: str) -> None:
        found.append(_diagnostic(rule_id, path, profile, expected, actual))

    registered = {section.title: section for section in form.sections}
    local: dict[str | None, set[str]] = {}
    homes: dict[str, set[str | None]] = {}
    for section in form.sections:
        for child in section.children:
            homes.setdefault(child.title, set()).add(section.section_id)
    for extension in form.extensions:
        if extension.kind == "local_h3" and extension.title is not None:
            local.setdefault(extension.parent_id, set()).add(extension.title)
            homes.setdefault(extension.title, set()).add(extension.parent_id)

    headings = scan.headings
    h2_titles = [title for level, title in headings if level == 2]
    for title in dict.fromkeys(h2_titles):
        if h2_titles.count(title) > 1:
            add("BODY-H2-DUPLICATE", "unique H2", title)
    for title in h2_titles:
        if title not in registered:
            add("BODY-HEADING-UNSUPPORTED", "a registered H2", title)
    for section in form.sections:
        if section.requiredness == "required" and section.title not in h2_titles:
            add("BODY-HEADING-REQUIRED", "required H2", section.title)
    present = [title for title in dict.fromkeys(h2_titles) if title in registered]
    in_order = [s.title for s in form.sections if s.title in present]
    if present != in_order:
        add("BODY-H2-ORDER", json.dumps(in_order), json.dumps(present))

    # Each block is one H2 and the H3 headings under it; the first block holds
    # any H3 that has no H2 above it.
    blocks: list[tuple[int | None, str | None, list[tuple[int, str]]]] = [
        (None, None, [])
    ]
    for index, (level, title) in enumerate(headings):
        if level == 2:
            blocks.append((index, title, []))
        elif level == 3:
            blocks[-1][2].append((index, title))

    def body_lines(index: int) -> list[tuple[str, bool]]:
        level = headings[index][0]
        end = next(
            (i for i in range(index + 1, len(headings)) if headings[i][0] <= level),
            len(headings),
        )
        return [line for body in scan.bodies[index:end] for line in body]

    def empty(index: int, link_only: bool) -> bool:
        return not _substantive_section_body(
            body_lines(index), links_are_content=link_only
        )

    def bare(index: int) -> bool:
        # SPEC-0182: the whole body up to the next heading is one bare statement.
        # A reworded statement passes; whether a line explains is semantic review.
        lines = [(line.strip(), fenced) for line, fenced in scan.bodies[index]]
        lines = [(line, fenced) for line, fenced in lines if line]
        return (
            len(lines) == 1
            and not lines[0][1]
            and _BARE_STATEMENT.fullmatch(lines[0][0]) is not None
            and not _BARE_REASON_CONNECTIVE.search(lines[0][0])
        )

    for index, title, children in blocks:
        names = [name for _, name in children]
        if index is None:
            for name in dict.fromkeys(names):
                add("BODY-H3-PARENT", "an H2 above every H3", name)
            continue
        parent = registered.get(title or "")
        kids = {child.title: child for child in parent.children} if parent else {}
        extras = local.get(parent.section_id if parent else None, set())
        for name in dict.fromkeys(names):
            if names.count(name) > 1:
                add("BODY-H3-DUPLICATE", "unique H3 under one H2", f"{title}: {name}")
            if name in kids or name in extras:
                continue
            if name in homes:
                add(
                    "BODY-H3-PARENT",
                    "an H3 under its registered H2",
                    f"{title}: {name}",
                )
            else:
                add(
                    "BODY-H3-UNSUPPORTED",
                    "a registered H3 or local extension",
                    f"{title}: {name}",
                )
        if parent is None:
            continue
        for child in parent.children:
            if child.requiredness == "required" and child.title not in names:
                add("BODY-H3-REQUIRED", "required H3", f"{title}: {child.title}")
        seen = [name for name in dict.fromkeys(names) if name in kids]
        ordered = [child.title for child in parent.children if child.title in seen]
        if seen != ordered:
            add("BODY-H3-ORDER", json.dumps(ordered), json.dumps(seen))
        if profile.mode == "template":
            continue
        # An empty section is judged on authored documents only; a bare
        # statement (SPEC-0182) on every non-template document of a form.
        authored = profile.mode == "authored"
        if authored and not children and empty(index, parent.link_only):
            add("BODY-SECTION-EMPTY", "a section with authored content", title or "")
        elif not children and bare(index):
            add("BODY-SECTION-BARE", BARE_EXPECTED, title or "")
        for position, name in children:
            if name in kids or name in extras:
                link_only = name in kids and kids[name].link_only
                if authored and empty(position, link_only):
                    add(
                        "BODY-SECTION-EMPTY",
                        "a section with authored content",
                        f"{title}: {name}",
                    )
                elif bare(position):
                    add("BODY-SECTION-BARE", BARE_EXPECTED, f"{title}: {name}")
    return found


def _template_residue_diagnostics(
    path: PurePosixPath, profile: DocumentProfile, body: str
) -> list[Diagnostic]:
    """Authored content carries no template author prompt or legacy residue."""

    diagnostics: list[Diagnostic] = []
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


def _body_diagnostics(
    path: PurePosixPath,
    profile: DocumentProfile,
    body: str,
    status: str = "",
) -> list[Diagnostic]:
    scan = scan_headings(body)
    readme = profile.profile_class == "readme"
    diagnostics: list[Diagnostic] = []
    if scan.unclosed_fence:
        rule = "README_FENCE" if readme else "BODY-FENCE-UNCLOSED"
        diagnostics.append(
            _diagnostic(rule, path, profile, "all fenced blocks are closed", "unclosed")
        )
    # SPEC-0168: a profile whose role has a form is checked against its section
    # tree, unless a retained form names this status and supplies H2 lists.
    headings = profile.headings
    tree = profile.form is not None
    if profile.form is not None:
        retained = profile.form.retained_headings(status)
        if retained is not None:
            headings, tree = retained, False
    if not tree and not headings.required and not headings.allowed:
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
    if tree:
        diagnostics.extend(_form_tree_diagnostics(path, profile, scan))
        diagnostics.extend(_template_residue_diagnostics(path, profile, body))
        return diagnostics
    missing = [heading for heading in headings.required if heading not in h2]
    required_rule = "README_H2_REQUIRED" if readme else "BODY-HEADING-REQUIRED"
    diagnostics.extend(
        _diagnostic(required_rule, path, profile, "required H2", heading)
        for heading in missing
    )
    if headings.ordered and not missing:
        observed_order = [heading for heading in h2 if heading in headings.required]
        if observed_order != list(headings.required):
            diagnostics.append(
                _diagnostic(
                    "BODY-H2-ORDER",
                    path,
                    profile,
                    json.dumps(headings.required),
                    json.dumps(observed_order),
                )
            )
    if profile.mode == "authored":
        h2_counts = collections.Counter(h2)
        section_content = _scan_required_h2_content(
            body,
            headings.required,
            substantive_body=headings.substantive_body,
        )
        diagnostics.extend(
            _diagnostic(
                "BODY-HEADING-EMPTY",
                path,
                profile,
                "required H2 contains authored body content",
                heading,
            )
            for heading in section_content.empty
            if h2_counts[heading] == 1
        )
        diagnostics.extend(
            _diagnostic(
                "BODY-HEADING-NESTED-ROLE",
                path,
                profile,
                "required role headings occur only at H2",
                heading,
            )
            for heading in section_content.nested_roles
        )
    duplicate = sorted(
        heading for heading, count in collections.Counter(h2).items() if count > 1
    )
    duplicate_rule = "README_H2_DUPLICATE" if readme else "BODY-H2-DUPLICATE"
    diagnostics.extend(
        _diagnostic(duplicate_rule, path, profile, "unique H2", heading)
        for heading in duplicate
    )
    represented = set(headings.allowed)
    unsupported_rule = "README_H2_UNSUPPORTED" if readme else "BODY-HEADING-UNSUPPORTED"
    diagnostics.extend(
        _diagnostic(unsupported_rule, path, profile, "allowed H2", heading)
        for heading in h2
        if heading not in represented
    )
    diagnostics.extend(_template_residue_diagnostics(path, profile, body))
    return diagnostics


def _terminal(registry: Any, profile: DocumentProfile, text: str) -> bool:
    try:
        _, metadata, _ = extract_frontmatter(text)
    except ContractError:
        return False
    status = task_status(metadata, text, profile)
    if not status:
        return False
    return any(
        profile.profile_id in domain.profile_ids
        and domain.validation_class(status) == "terminal"
        for domain in registry.lifecycle_domains
    )


def document_language_diagnostics(
    registry: Any,
    documents: Sequence[tuple[PurePosixPath, DocumentProfile, str]],
    english_only_texts: Mapping[PurePosixPath, str],
    *,
    content_paths: frozenset[PurePosixPath] | None = None,
    english_only_paths: frozenset[PurePosixPath] | None = None,
) -> list[Diagnostic]:
    """SPEC-0093: each document is written in the language its profile names."""

    contract = getattr(registry, "document_language", None)
    if contract is None:
        return []
    outputs = {
        profile.template: profile.profile_id
        for profile in registry.profiles
        if profile.template is not None and profile.mode != "template"
    }
    diagnostics: list[Diagnostic] = []
    checked: set[PurePosixPath] = set()
    for path, profile, text in documents:
        kind = document_language.classify(
            path,
            profile.profile_id,
            profile.mode,
            outputs.get(path),
            _terminal(registry, profile, text),
            contract,
        )
        if kind is None or kind == "english-only":
            continue
        checked.add(path)
        if (
            content_paths is not None
            and path not in content_paths
            and path not in contract.pending_paths
        ):
            continue
        found = document_language.findings(text, kind, contract)
        if path in contract.pending_paths:
            if not found:
                diagnostics.append(
                    _diagnostic(
                        "LANG-PENDING",
                        path,
                        profile,
                        "a pending document that still violates the contract",
                        "it passes; remove it from pending_paths",
                    )
                )
            continue
        diagnostics.extend(
            _diagnostic(code, path, profile, f"{kind} language", detail)
            for code, detail in found
        )
    for path, text in sorted(english_only_texts.items()):
        if english_only_paths is not None and path not in english_only_paths:
            continue
        if not contract.english_only(path):
            continue
        diagnostics.extend(
            Diagnostic(code, path, "", "english-only", detail, OWNER)
            for code, detail in document_language.findings(
                text, "english-only", contract
            )
        )
    for pending in sorted(contract.pending_paths - checked, key=PurePosixPath.as_posix):
        diagnostics.append(
            Diagnostic(
                "LANG-PENDING",
                pending,
                "",
                "a tracked, checked document",
                "pending path is untracked or unchecked",
                OWNER,
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
    frontmatter_schema: Mapping[str, Any] | None = None,
) -> list[Diagnostic]:
    """Validate one source using only its registry-selected profile contract."""

    if profile.profile_id == "evaluation/raw-output" and profile.mode == "native":
        verify_opaque_evaluation_output(root, path)
        return []
    text = read_repository_text(root, path)
    return validate_document_text(
        text,
        path,
        profile,
        mode,
        today=today,
        body_contracts=body_contracts,
        body_contract_path_prefixes=body_contract_path_prefixes,
        frontmatter_schema=frontmatter_schema,
    )


def _document_content_table(
    text: str, title: str
) -> tuple[list[str], list[list[str]]] | None:
    sections = [
        section
        for heading in (f"## {title}", f"### {title}", f"#### {title}")
        if (section := _exact_heading_section(text, heading)) is not None
    ]
    return _first_visible_table(sections[0]) if len(sections) == 1 else None


def document_content_diagnostics(
    root: Path,
    path: PurePosixPath,
    profile: DocumentProfile,
    text: str,
    *,
    registry: Any | None = None,
) -> list[Diagnostic]:
    """Check one current router's live rows using the selected document gate."""

    source = registry or load_registry(root)
    navigation = source.readme_navigation
    found = validate_document_content(
        root,
        path,
        text,
        _document_content_table,
        index_columns=navigation.index_columns,
        optional_index_columns=navigation.optional_index_columns,
    )
    return [
        Diagnostic(rule, path, profile.profile_id, expected, actual, OWNER)
        for rule, expected, actual in found
    ]


def validate_document_text(
    text: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    mode: str,
    *,
    today: dt.date | None = None,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
    frontmatter_schema: Mapping[str, Any] | None = None,
    include_body: bool = True,
) -> list[Diagnostic]:
    """Validate exact caller-supplied text without consulting filesystem bytes."""

    if mode != "strict":
        raise ValueError("mode must be strict")
    if profile.profile_id == "evaluation/raw-output" and profile.mode == "native":
        return []
    effective_today = today or dt.datetime.now(ZoneInfo("Asia/Seoul")).date()
    diagnostics: list[Diagnostic] = []
    body = _frontmatter_body(
        text, path, profile, diagnostics, effective_today, frontmatter_schema
    )
    status = ""
    metadata: dict[str, Any] = {}
    if profile.frontmatter.mode == "required":
        try:
            _, metadata, _ = extract_frontmatter(text)
        except ContractError:
            metadata = {}
        status = task_status(metadata, text, profile)
    if include_body:
        diagnostics.extend(_body_diagnostics(path, profile, body, status))
        if profile.mode == "authored":
            diagnostics.extend(_table_diagnostics(path, profile, body))
            diagnostics.extend(_policy_rule_diagnostics(path, profile, body))
        elif profile.mode == "template":
            diagnostics.extend(_template_table_section_diagnostics(path, profile, body))
    diagnostics.extend(artifact_identity_diagnostics(path, profile, metadata))
    if not include_body:
        return sorted(diagnostics, key=diagnostic_sort_key)
    binding = profile.body_contract.task_execution if profile.body_contract else None
    if binding and binding.evidence_section:
        section = _exact_heading_section(body, f"## {binding.evidence_section}")
        table = _first_visible_table(section or "")
        if table is None or tuple(table[0]) != binding.evidence_columns or not table[1]:
            diagnostics.append(
                _diagnostic(
                    "TASK-EVIDENCE-COLUMNS",
                    path,
                    profile,
                    repr(binding.evidence_columns),
                    "missing or malformed evidence table",
                )
            )
        elif profile.mode != "template":
            if any(len(row) != len(table[0]) for row in table[1]):
                diagnostics.append(
                    _diagnostic(
                        "TASK-EVIDENCE-COLUMNS",
                        path,
                        profile,
                        f"{len(binding.evidence_columns)} cells in every evidence row",
                        "ragged evidence row",
                    )
                )
                return sorted(diagnostics, key=diagnostic_sort_key)
            evidence_rows = [dict(zip(table[0], row, strict=True)) for row in table[1]]
            decision_section = _exact_heading_section(
                body, f"## {binding.criterion_acceptance_section}"
            )
            decision_table = _first_visible_table(decision_section or "")
            execution_section = _exact_heading_section(
                body, f"## {profile.body_contract.section}"
            )
            execution_table = _first_visible_table(
                _exact_heading_section(
                    execution_section or "",
                    f"### {profile.body_contract.table_heading}",
                )
                or ""
            )
            if (
                decision_table is None
                or tuple(decision_table[0]) != binding.criterion_acceptance_columns
                or not decision_table[1]
                or any(len(row) != len(decision_table[0]) for row in decision_table[1])
            ):
                diagnostics.append(
                    _diagnostic(
                        "TASK-ACCEPTANCE-COLUMNS",
                        path,
                        profile,
                        repr(binding.criterion_acceptance_columns),
                        "missing or malformed criterion acceptance table",
                    )
                )
            elif (
                execution_table is not None
                and tuple(execution_table[0]) == profile.body_contract.required_columns
                and all(
                    len(row) == len(execution_table[0]) for row in execution_table[1]
                )
            ):
                work_rows = [
                    dict(zip(execution_table[0], row, strict=True))
                    for row in execution_table[1]
                ]
                decision_rows = [
                    dict(zip(decision_table[0], row, strict=True))
                    for row in decision_table[1]
                ]
                diagnostics.extend(
                    _diagnostic(
                        rule, path, profile, "valid Task acceptance graph", detail
                    )
                    for rule, detail in task_contract_issues(
                        work_rows, evidence_rows, decision_rows, status, binding
                    )
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


def _outcome_rows(diagnostics: Sequence[Diagnostic]) -> list[ResultRow]:
    return [
        ResultRow("FAIL", diagnostic)
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
    parser.add_argument("--change-scope", action="store_true")
    parser.add_argument("--changed-path", action="append", default=[])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--inventory", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.change_scope != bool(args.changed_path):
            raise ValueError(
                "--change-scope requires one or more --changed-path values"
            )
        if args.change_scope and (
            args.body_contracts == "audit" or args.body_contract_path_prefix
        ):
            raise ValueError("explicit body-contract audit cannot use change scope")
        if args.inventory and args.change_scope:
            raise ValueError("inventory cannot use change scope")
        changed_paths = (
            validated_changed_paths(args.changed_path) if args.change_scope else ()
        )
        registry = load_registry(root)
        frontmatter_schema = load_frontmatter_schema(root)
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
        content_paths = (
            scoped_document_content_paths(
                registry, args.changed_path, inventory.current_paths
            )
            if args.change_scope
            else None
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
        identity_documents: list[tuple[PurePosixPath, DocumentProfile, str]] = []
        for path in inventory.current_paths:
            profile = classify_path(registry, path)
            if is_opaque_evaluation_output(registry, path):
                verify_opaque_evaluation_output(root, path)
                continue
            text = read_repository_text(root, path)
            identity_documents.append((path, profile, text))
            diagnostics.extend(
                validate_document_text(
                    text,
                    path,
                    profile,
                    args.mode,
                    body_contracts=args.body_contracts,
                    body_contract_path_prefixes=tuple(args.body_contract_path_prefix),
                    frontmatter_schema=frontmatter_schema,
                    include_body=content_paths is None or path in content_paths,
                )
            )
            if content_paths is None or path in content_paths:
                diagnostics.extend(
                    document_content_diagnostics(
                        root, path, profile, text, registry=registry
                    )
                )
        diagnostics.extend(artifact_identity_uniqueness_diagnostics(identity_documents))
        language = getattr(registry, "document_language", None)
        english_only_texts: dict[PurePosixPath, str] = {}
        if language is not None:
            entries = _parse_ls_files_stage_z(
                _run_git(root, ("ls-files", "--stage", "-z"))
            )
            for entry in entries:
                if (
                    entry.stage == 0
                    and entry.mode.startswith("100")
                    and language.english_only(entry.path)
                    and not is_opaque_evaluation_output(registry, entry.path)
                ):
                    english_only_texts[entry.path] = read_repository_text(
                        root, entry.path
                    )
            for path in changed_paths:
                if (
                    path in english_only_texts
                    or not language.english_only(path)
                    or is_opaque_evaluation_output(registry, path)
                ):
                    continue
                try:
                    (root / path).lstat()
                except FileNotFoundError:
                    # Deleted Git paths have no current language body.
                    continue
                if is_ignored_repository_path(root, path):
                    raise ValueError(f"changed English-only path is ignored: {path}")
                # The bounded reader rejects symlinks in every path component,
                # non-regular files, oversized input and invalid UTF-8.
                english_only_texts[path] = read_repository_text(root, path)
        diagnostics.extend(
            document_language_diagnostics(
                registry,
                identity_documents,
                english_only_texts,
                content_paths=content_paths,
                english_only_paths=(
                    frozenset((*content_paths, *changed_paths))
                    if content_paths is not None
                    else None
                ),
            )
        )
        rows = _outcome_rows(diagnostics)
        _emit_results(args.mode, args.format, rows)
        return 1 if any(row.outcome == "FAIL" for row in rows) else 0
    except (DocumentContractError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
