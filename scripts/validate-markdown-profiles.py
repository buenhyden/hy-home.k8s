#!/usr/bin/env python3
"""Validate registry-selected Markdown document profiles."""

from __future__ import annotations

import argparse
import collections
import copy
import datetime as dt
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
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    classify_path,
    diagnostic_sort_key,
    enumerate_target_markdown,
    load_registry,
    read_repository_text,
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
GENERIC_RESIDUE = ("Target: docs/", "Use this template")
TOKEN_BEARING_DEBT_RULES = frozenset(
    {
        "BODY-H2-DUPLICATE",
        "BODY-HEADING-REQUIRED",
        "BODY-HEADING-UNSUPPORTED",
        "BODY-TEMPLATE-RESIDUE",
    }
)
DEFERABLE_DEBT_RULES = TOKEN_BEARING_DEBT_RULES | {"FM-DELIMITER"}
EXPECTED_DEBT_CAPS: dict[str, dict[str, int]] = {
    "BODY-HEADING-REQUIRED": {
        "pathCount": 89,
        "occurrenceCount": 247,
        "tokenObligationCount": 247,
    },
    "BODY-TEMPLATE-RESIDUE": {
        "pathCount": 188,
        "occurrenceCount": 410,
    },
    "FM-DELIMITER": {
        "pathCount": 24,
        "occurrenceCount": 24,
        "tokenObligationCount": 0,
    },
    "BODY-HEADING-UNSUPPORTED": {
        "pathCount": 175,
        "occurrenceCount": 617,
        "tokenObligationCount": 617,
        "distinctTokenCount": 400,
    },
    "BODY-H2-DUPLICATE": {
        "pathCount": 1,
        "occurrenceCount": 1,
        "tokenObligationCount": 1,
    },
}
EXPECTED_REQUIRED_RESIDUE_OVERLAP = 51
EXPECTED_REQUIRED_RESIDUE_UNION = 226
EXPECTED_DEBT_UNION = 266
IMPLEMENTED_RULE_IDS = frozenset(
    {
        "APPEND-CONTEXT",
        "APPEND-ENTRY-LEVEL",
        "APPEND-PARENT-H2",
        "APPEND-PARENT-PROFILE",
        "APPEND-SECTION-LEVEL",
        "APPEND-SECTION-REQUIRED",
        "BODY-FENCE-UNCLOSED",
        "BODY-H1",
        "BODY-H2-DUPLICATE",
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


def _diagnostic(
    rule_id: str,
    path: PurePosixPath,
    profile: DocumentProfile,
    expected: str,
    actual: str,
) -> Diagnostic:
    return Diagnostic(rule_id, path, profile.profile_id, expected, actual, OWNER)


def _compatibility_rows(root: Path) -> dict[str, dict[str, Any]]:
    data = json.loads((root / COMPATIBILITY_PATH).read_text(encoding="utf-8"))
    rows = data.get("compatibilityDebt")
    if not isinstance(rows, list):
        raise ValueError("compatibilityDebt must be a list")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        profile = row.get("profile")
        if not isinstance(profile, str) or profile in result:
            raise ValueError("compatibilityDebt profile IDs must be unique strings")
        result[profile] = row
    return result


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
    root: Path,
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
    compatibility = _compatibility_rows(root).get(profile.profile_id, {})
    aliases = {item["canonical"]: tuple(item["aliases"]) for item in compatibility.get("legacyRequiredAnyOf", [])}
    residue = tuple(compatibility.get("forbiddenResidue", []))
    missing = [heading for heading in profile.headings.required if heading not in h2 and not any(alias in h2 for alias in aliases.get(heading, ()))]
    required_rule = "README_H2_REQUIRED" if readme else "BODY-HEADING-REQUIRED"
    diagnostics.extend(_diagnostic(required_rule, path, profile, "required H2", heading) for heading in missing)
    duplicate = sorted(heading for heading, count in collections.Counter(h2).items() if count > 1)
    duplicate_rule = "README_H2_DUPLICATE" if readme else "BODY-H2-DUPLICATE"
    diagnostics.extend(_diagnostic(duplicate_rule, path, profile, "unique H2", heading) for heading in duplicate)
    represented = set(profile.headings.allowed) | set(residue)
    represented.update(alias for values in aliases.values() for alias in values)
    unsupported_rule = "README_H2_UNSUPPORTED" if readme else "BODY-HEADING-UNSUPPORTED"
    diagnostics.extend(_diagnostic(unsupported_rule, path, profile, "allowed H2", heading) for heading in h2 if heading not in represented)
    if profile.placeholder_policy == "forbidden":
        diagnostics.extend(_diagnostic("BODY-TEMPLATE-RESIDUE", path, profile, "authored content without legacy/template residue", heading) for heading in h2 if heading in residue)
        for marker in GENERIC_RESIDUE:
            for _ in range(body.count(marker)):
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
) -> list[Diagnostic]:
    """Validate one source using only its registry-selected profile contract."""

    if mode not in {"compatibility", "strict"}:
        raise ValueError("mode must be compatibility or strict")
    effective_today = today or dt.datetime.now(ZoneInfo("Asia/Seoul")).date()
    text = read_repository_text(root, path)
    diagnostics: list[Diagnostic] = []
    body = _frontmatter_body(text, path, profile, diagnostics, effective_today)
    diagnostics.extend(_body_diagnostics(root, path, profile, body, append_context))
    return sorted(diagnostics, key=diagnostic_sort_key)


def _write_source(root: Path, path: PurePosixPath, source: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")


def _remove_first_required_h2(source: str, profile: DocumentProfile) -> str:
    heading = profile.headings.required[0]
    marker = f"\n## {heading}\n"
    return source.replace(marker, "\n", 1)


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
class DebtContract:
    keys: frozenset[tuple[str, str, str, str]]
    caps: dict[str, dict[str, int]]
    union_path_count: int


@dataclass(frozen=True)
class ResultRow:
    outcome: str
    diagnostic: Diagnostic
    debt_token: str


def _debt_token(diagnostic: Diagnostic) -> str:
    return diagnostic.actual if diagnostic.rule_id in TOKEN_BEARING_DEBT_RULES else ""


def _load_debt_contract(
    root: Path, contract: dict[str, Any] | None = None
) -> DebtContract:
    if contract is None:
        contract = json.loads((root / COMPATIBILITY_PATH).read_text(encoding="utf-8"))
    if contract.get("schemaVersion") != 1:
        raise ValueError("template compatibility schemaVersion must be 1")
    if contract.get("owner") != "Spec 030" or contract.get("growthAllowed") is not False:
        raise ValueError("template compatibility debt must be Spec 030 owned and no-growth")
    registry = load_registry(root)
    inventory_paths = set(enumerate_target_markdown(root).current_paths)
    aggregate = contract.get("semanticDebtCaps")
    if not isinstance(aggregate, dict):
        raise ValueError("semanticDebtCaps must be an object")
    if aggregate.get("rules") != EXPECTED_DEBT_CAPS:
        raise ValueError("semantic debt rule caps changed")
    if aggregate.get("requiredResidueOverlapPathCount") != EXPECTED_REQUIRED_RESIDUE_OVERLAP:
        raise ValueError("required/residue overlap cap changed")
    if aggregate.get("requiredResidueUnionPathCount") != EXPECTED_REQUIRED_RESIDUE_UNION:
        raise ValueError("required/residue union cap changed")
    if aggregate.get("unionPathCount") != EXPECTED_DEBT_UNION:
        raise ValueError("semantic debt union cap changed")

    rows = contract.get("compatibilityDebt")
    if not isinstance(rows, list):
        raise ValueError("compatibilityDebt must be a list")
    keys: set[tuple[str, str, str, str]] = set()
    profile_ids: set[str] = set()
    for row in rows:
        profile = row.get("profile")
        if not isinstance(profile, str) or profile in profile_ids:
            raise ValueError("compatibilityDebt profile IDs must be unique strings")
        profile_ids.add(profile)
        affected_paths = row.get("affectedPaths")
        if not isinstance(affected_paths, list):
            raise ValueError("every compatibilityDebt row requires affectedPaths")
        path_values = [item.get("path") for item in affected_paths if isinstance(item, dict)]
        if len(path_values) != len(affected_paths):
            raise ValueError("affectedPaths entries must be objects")
        if path_values != sorted(path_values) or len(path_values) != len(set(path_values)):
            raise ValueError("affectedPaths must be unique and sorted by path")
        for item in affected_paths:
            if set(item) != {"path", "ruleIds", "tokens"}:
                raise ValueError("affectedPaths entries require exactly path, ruleIds, and tokens")
            path = item["path"]
            rule_ids = item["ruleIds"]
            encoded_tokens = item["tokens"]
            if not isinstance(path, str) or not isinstance(rule_ids, list) or not isinstance(encoded_tokens, list):
                raise ValueError("affectedPaths path, ruleIds, and tokens have invalid types")
            pure_path = PurePosixPath(path)
            if path != pure_path.as_posix() or path.startswith("./") or ".." in pure_path.parts:
                raise ValueError(f"affectedPaths path is not normalized: {path}")
            try:
                actual_profile = classify_path(registry, pure_path).profile_id
            except DocumentContractError as exc:
                raise ValueError(f"affectedPaths path is not classifiable: {path}") from exc
            if pure_path not in inventory_paths:
                raise ValueError(f"affectedPaths path is not in the tracked target inventory: {path}")
            if actual_profile != profile:
                raise ValueError(
                    f"affectedPaths profile mismatch for {path}: {profile} != {actual_profile}"
                )
            if rule_ids != sorted(set(rule_ids)) or not rule_ids:
                raise ValueError("affectedPaths ruleIds must be non-empty, unique, and sorted")
            if not set(rule_ids).issubset(DEFERABLE_DEBT_RULES):
                raise ValueError("affectedPaths contains a non-deferable rule")
            if encoded_tokens != sorted(set(encoded_tokens)):
                raise ValueError("affectedPaths tokens must be unique and sorted")
            tokens_by_rule: dict[str, list[str]] = collections.defaultdict(list)
            for encoded in encoded_tokens:
                if not isinstance(encoded, str) or "::" not in encoded:
                    raise ValueError("affectedPaths tokens must use RULE_ID::token")
                rule_id, token = encoded.split("::", 1)
                if rule_id not in rule_ids or rule_id not in TOKEN_BEARING_DEBT_RULES or not token:
                    raise ValueError("affectedPaths token rule must be declared and token-bearing")
                tokens_by_rule[rule_id].append(token)
            for rule_id in rule_ids:
                if rule_id in TOKEN_BEARING_DEBT_RULES and not tokens_by_rule[rule_id]:
                    raise ValueError("token-bearing affectedPaths rules require exact tokens")
                rule_tokens = tokens_by_rule[rule_id] if rule_id in TOKEN_BEARING_DEBT_RULES else [""]
                for token in rule_tokens:
                    key = (path, profile, rule_id, token)
                    if key in keys:
                        raise ValueError("affectedPaths contains a duplicate debt obligation")
                    keys.add(key)

    paths_by_rule = {
        rule_id: {path for path, _, rule, _ in keys if rule == rule_id}
        for rule_id in DEFERABLE_DEBT_RULES
    }
    tokens_by_rule = {
        rule_id: {
            (path, token)
            for path, _, rule, token in keys
            if rule == rule_id and token
        }
        for rule_id in DEFERABLE_DEBT_RULES
    }
    for rule_id, expected in EXPECTED_DEBT_CAPS.items():
        if len(paths_by_rule[rule_id]) != expected["pathCount"]:
            raise ValueError(f"{rule_id} affected path cap does not match records")
        if "tokenObligationCount" in expected and len(tokens_by_rule[rule_id]) != expected["tokenObligationCount"]:
            raise ValueError(f"{rule_id} token obligation cap does not match records")
        if "distinctTokenCount" in expected:
            distinct = {token for _, token in tokens_by_rule[rule_id]}
            if len(distinct) != expected["distinctTokenCount"]:
                raise ValueError(f"{rule_id} distinct token cap does not match records")
    required_paths = paths_by_rule["BODY-HEADING-REQUIRED"]
    residue_paths = paths_by_rule["BODY-TEMPLATE-RESIDUE"]
    if len(required_paths & residue_paths) != EXPECTED_REQUIRED_RESIDUE_OVERLAP:
        raise ValueError("required/residue overlap does not match exact records")
    if len(required_paths | residue_paths) != EXPECTED_REQUIRED_RESIDUE_UNION:
        raise ValueError("required/residue union does not match exact records")
    if len({path for path, _, _, _ in keys}) != EXPECTED_DEBT_UNION:
        raise ValueError("semantic debt union does not match exact records")
    return DebtContract(frozenset(keys), EXPECTED_DEBT_CAPS, EXPECTED_DEBT_UNION)


def _unused_diagnostic(key: tuple[str, str, str, str]) -> Diagnostic:
    path, profile, rule_id, token = key
    return Diagnostic(
        "DEBT-UNUSED",
        PurePosixPath(path),
        profile,
        "configured debt produces one or more matching diagnostics",
        f"{rule_id}::{token}" if token else rule_id,
        OWNER,
    )


def _outcome_rows(
    root: Path,
    diagnostics: Sequence[Diagnostic],
    mode: str,
    *,
    contract: dict[str, Any] | None = None,
) -> list[ResultRow]:
    debt = _load_debt_contract(root, contract)
    diagnostic_keys = [
        (item.path.as_posix(), item.profile, item.rule_id, _debt_token(item))
        for item in diagnostics
    ]
    consumption = collections.Counter(diagnostic_keys)
    consumed = set(consumption) & set(debt.keys)
    actual_paths: dict[str, set[str]] = collections.defaultdict(set)
    actual_occurrences: collections.Counter[str] = collections.Counter()
    for diagnostic in diagnostics:
        if diagnostic.rule_id in DEFERABLE_DEBT_RULES:
            actual_paths[diagnostic.rule_id].add(diagnostic.path.as_posix())
            actual_occurrences[diagnostic.rule_id] += 1
    growth_rules = {
        rule_id
        for rule_id, caps in debt.caps.items()
        if len(actual_paths[rule_id]) > caps["pathCount"]
        or actual_occurrences[rule_id] > caps["occurrenceCount"]
    }
    union_growth = len({path for path, _, _, _ in diagnostic_keys}) > debt.union_path_count
    rows: list[ResultRow] = []
    for diagnostic, key in sorted(
        zip(diagnostics, diagnostic_keys), key=lambda pair: diagnostic_sort_key(pair[0])
    ):
        token = key[3]
        exact = key in debt.keys
        can_defer = (
            exact
            and consumption[key] == 1
            and diagnostic.rule_id not in growth_rules
            and not union_growth
        )
        outcome = "DEFER" if mode == "compatibility" and can_defer else "FAIL"
        rows.append(ResultRow(outcome, diagnostic, token))
    for key in sorted(debt.keys - consumed):
        rows.append(ResultRow("FAIL", _unused_diagnostic(key), key[3]))
    return sorted(rows, key=lambda row: diagnostic_sort_key(row.diagnostic))


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
    _write_source(temp_root, path, source)
    return _rule_ids(
        validate_document(
            temp_root,
            path,
            profile,
            "strict",
            append_context=append_context,
            today=today,
        )
    )


def _repository_diagnostics(
    root: Path,
    registry: Any,
    inventory: Any,
    *,
    today: dt.date | None,
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
            )
        )
    return sorted(diagnostics, key=diagnostic_sort_key)


def _self_test(root: Path) -> list[str]:
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
    if set(fixture) != {"schemaVersion", "dateCases", "profileMatrix", "mutationCases"}:
        failures.append("fixture top-level keys changed")
    rows = fixture.get("profileMatrix", [])
    row_ids = [row.get("profile") for row in rows]
    if len(row_ids) != len(set(row_ids)):
        failures.append("profileMatrix contains duplicate profiles")
    if set(row_ids) != set(profiles):
        failures.append("profileMatrix must cover every registry profile exactly once")

    readme_names = tuple(case.get("name") for case in readme_fixture.get("cases", []))
    if readme_names != EXPECTED_README_CASES:
        failures.append("README handoff case names changed")
    readme_path_rows = readme_fixture.get("paths", [])
    readme_paths = [row.get("path") for row in readme_path_rows]
    if len(readme_paths) != 72 or len(readme_paths) != len(set(readme_paths)):
        failures.append("README handoff paths must contain 72 unique entries")
    readme_by_path = {row.get("path"): row for row in readme_path_rows}
    inventory_readmes = {
        path.as_posix()
        for path in inventory.current_paths
        if path.name == "README.md"
        and classify_path(registry, path).profile_class == "readme"
        and classify_path(registry, path).mode != "template"
    }
    if set(readme_paths) != inventory_readmes:
        failures.append("README handoff paths must equal the production inventory set")
    for path_text, handoff in readme_by_path.items():
        if not isinstance(path_text, str):
            failures.append("README handoff path values must be strings")
            continue
        selected = classify_path(registry, PurePosixPath(path_text))
        if handoff.get("profile") != selected.profile_id:
            failures.append(f"README handoff profile mismatch: {path_text}")
        if handoff.get("requiredH2") != list(selected.headings.required):
            failures.append(f"README handoff requiredH2 mismatch: {path_text}")
        if handoff.get("allowedH2") != list(selected.headings.allowed):
            failures.append(f"README handoff allowedH2 mismatch: {path_text}")

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
                profile.mode not in {"native", "generated"} or not structural_na
            ):
                failures.append(f"invalid classification-only mode: {profile.profile_id}")
            if applicability == "append-fragment" and profile.profile_id != "governance/progress-entry":
                failures.append(f"invalid append-fragment profile: {profile.profile_id}")
            if profile.profile_id == "governance/progress-entry" and applicability != "append-fragment":
                failures.append("governance/progress-entry must be append-fragment")
            fixture_path = PurePosixPath(row["fixturePath"])
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
                    try:
                        classify_path(registry, PurePosixPath("uncovered.fixture"))
                        actual_rules: list[str] = []
                    except DocumentContractError as exc:
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
            actual_rules = _run_source_case(
                temp_root,
                path,
                row["positiveSource"],
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
                source = _mutation_source(row["positiveSource"], mutation, profile)
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
                PurePosixPath(case["path"]),
                case["source"],
                profile,
            )
            if actual_rules != case["expectedRuleIds"]:
                failures.append(
                    f"mutation {case['name']}: expected={case['expectedRuleIds']} actual={actual_rules}"
                )

        for case in readme_fixture.get("cases", []):
            path = PurePosixPath(case["path"])
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
        for case in fixture.get("dateCases", []):
            profile = profiles[case["profile"]]
            base = matrix_by_profile[profile.profile_id]["positiveSource"]
            source = re.sub(
                r"(?m)^updated: .+$", f"updated: {case['value']}", base, count=1
            )
            actual_rules = _run_source_case(
                temp_root,
                PurePosixPath(matrix_by_profile[profile.profile_id]["fixturePath"]),
                source,
                profile,
                today=dt.date(2026, 7, 12),
            )
            if actual_rules != case["expectedRuleIds"]:
                failures.append(
                    f"date {case['name']}: expected={case['expectedRuleIds']} actual={actual_rules}"
                )
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
    uncovered_rules = sorted(IMPLEMENTED_RULE_IDS - exercised)
    if uncovered_rules:
        failures.append(f"implemented rules lack mutations: {uncovered_rules}")

    try:
        _load_debt_contract(root)
    except (DocumentContractError, OSError, ValueError) as exc:
        failures.append(f"semantic debt contract invalid: {exc}")
        return failures
    production_diagnostics = _repository_diagnostics(
        root, registry, inventory, today=dt.date(2026, 7, 12)
    )
    expected_occurrences = {
        rule_id: caps["occurrenceCount"] for rule_id, caps in EXPECTED_DEBT_CAPS.items()
    }
    actual_occurrences = collections.Counter(
        item.rule_id for item in production_diagnostics
    )
    if dict(actual_occurrences) != expected_occurrences:
        failures.append(
            f"repository semantic occurrence caps changed: {dict(actual_occurrences)}"
        )
    actual_paths = {
        rule_id: {item.path.as_posix() for item in production_diagnostics if item.rule_id == rule_id}
        for rule_id in EXPECTED_DEBT_CAPS
    }
    for rule_id, caps in EXPECTED_DEBT_CAPS.items():
        if len(actual_paths[rule_id]) != caps["pathCount"]:
            failures.append(f"repository semantic path cap changed: {rule_id}")
    if len(actual_paths["BODY-HEADING-REQUIRED"] & actual_paths["BODY-TEMPLATE-RESIDUE"]) != EXPECTED_REQUIRED_RESIDUE_OVERLAP:
        failures.append("repository required/residue overlap changed")
    if len(actual_paths["BODY-HEADING-REQUIRED"] | actual_paths["BODY-TEMPLATE-RESIDUE"]) != EXPECTED_REQUIRED_RESIDUE_UNION:
        failures.append("repository required/residue union changed")
    if len({item.path.as_posix() for item in production_diagnostics}) != EXPECTED_DEBT_UNION:
        failures.append("repository semantic debt union changed")
    unsupported_tokens = {
        item.actual
        for item in production_diagnostics
        if item.rule_id == "BODY-HEADING-UNSUPPORTED"
    }
    if len(unsupported_tokens) != 400:
        failures.append("repository unsupported-heading distinct token cap changed")

    compatibility_rows = _outcome_rows(
        root, production_diagnostics, "compatibility"
    )
    strict_rows = _outcome_rows(root, production_diagnostics, "strict")
    compatibility_keys = [
        (
            row.diagnostic.path.as_posix(),
            row.diagnostic.profile,
            row.diagnostic.rule_id,
            row.debt_token,
        )
        for row in compatibility_rows
    ]
    strict_keys = [
        (
            row.diagnostic.path.as_posix(),
            row.diagnostic.profile,
            row.diagnostic.rule_id,
            row.debt_token,
        )
        for row in strict_rows
    ]
    if compatibility_keys != strict_keys or len(compatibility_keys) != 1299:
        failures.append("compatibility and strict diagnostic tuples differ")
    if {row.outcome for row in compatibility_rows} != {"DEFER"}:
        failures.append("repository compatibility results are not exact DEFER debt")
    if {row.outcome for row in strict_rows} != {"FAIL"}:
        failures.append("repository strict results are not exact FAIL debt")
    if any(row.diagnostic.rule_id == "DEBT-UNUSED" for row in compatibility_rows):
        failures.append("repository compatibility debt contains unused records")

    base_contract = json.loads(
        (root / COMPATIBILITY_PATH).read_text(encoding="utf-8")
    )

    def expect_config_rejection(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(base_contract)
        mutate(candidate)
        try:
            _load_debt_contract(root, candidate)
        except (DocumentContractError, ValueError):
            return
        failures.append(f"debt mutation accepted: {label}")

    first_affected = next(
        item
        for row in base_contract["compatibilityDebt"]
        for item in row["affectedPaths"]
    )

    def mutate_path(candidate: dict[str, Any]) -> None:
        item = next(
            item
            for row in candidate["compatibilityDebt"]
            for item in row["affectedPaths"]
        )
        item["path"] = "./" + item["path"]

    def mutate_rule(candidate: dict[str, Any]) -> None:
        item = next(
            item
            for row in candidate["compatibilityDebt"]
            for item in row["affectedPaths"]
        )
        item["ruleIds"][0] = "UNKNOWN-RULE"

    def mutate_cap(candidate: dict[str, Any]) -> None:
        candidate["semanticDebtCaps"]["rules"]["BODY-HEADING-REQUIRED"]["pathCount"] += 1

    def mutate_union(candidate: dict[str, Any]) -> None:
        candidate["semanticDebtCaps"]["unionPathCount"] += 1

    def duplicate_record(candidate: dict[str, Any]) -> None:
        row = next(row for row in candidate["compatibilityDebt"] if row["affectedPaths"])
        row["affectedPaths"].append(copy.deepcopy(row["affectedPaths"][0]))
        row["affectedPaths"].sort(key=lambda item: item["path"])

    expect_config_rejection("affected path", mutate_path)
    expect_config_rejection("rule ID", mutate_rule)
    expect_config_rejection("rule cap", mutate_cap)
    expect_config_rejection("union cap", mutate_union)
    expect_config_rejection("duplicate consumed record", duplicate_record)

    stale_contract = copy.deepcopy(base_contract)
    stale_item = next(
        item
        for row in stale_contract["compatibilityDebt"]
        for item in row["affectedPaths"]
        if any(token.startswith("BODY-HEADING-REQUIRED::") for token in item["tokens"])
    )
    token_index = next(
        index
        for index, token in enumerate(stale_item["tokens"])
        if token.startswith("BODY-HEADING-REQUIRED::")
    )
    stale_item["tokens"][token_index] += " drift"
    stale_item["tokens"].sort()
    for mode in ("compatibility", "strict"):
        mutated_rows = _outcome_rows(
            root, production_diagnostics, mode, contract=stale_contract
        )
        if not any(row.outcome == "FAIL" for row in mutated_rows):
            failures.append(f"stale token mutation did not fail in {mode}")
        if not any(row.diagnostic.rule_id == "DEBT-UNUSED" for row in mutated_rows):
            failures.append(f"stale token mutation lacked DEBT-UNUSED in {mode}")

    known = production_diagnostics[0]
    mutation_diagnostics = (
        Diagnostic(
            known.rule_id,
            PurePosixPath("docs/00.agent-governance/rules/bootstrap.md"),
            "governance/reference",
            known.expected,
            "unknown-token",
            OWNER,
        ),
        Diagnostic(
            "UNKNOWN-RULE",
            known.path,
            known.profile,
            known.expected,
            known.actual,
            OWNER,
        ),
        Diagnostic(
            known.rule_id,
            known.path,
            known.profile,
            known.expected,
            "unknown-token",
            OWNER,
        ),
    )
    for label, diagnostic in zip(
        ("new path", "unknown rule", "unknown token"), mutation_diagnostics
    ):
        for mode in ("compatibility", "strict"):
            result = _outcome_rows(root, [diagnostic], mode)
            if not result or not all(row.outcome == "FAIL" for row in result):
                failures.append(f"{label} mutation deferred in {mode}")

    if first_affected.get("path") is None:
        failures.append("semantic debt proof fixture unexpectedly empty")
    return failures


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--mode", choices=("compatibility", "strict"), default="compatibility")
    parser.add_argument("--format", choices=("text", "json"), default="text")
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
