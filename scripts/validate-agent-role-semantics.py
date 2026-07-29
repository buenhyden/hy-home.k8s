#!/usr/bin/env python3
"""Validate shared role semantics across local and provider adapter surfaces."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import stat
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn

import yaml
from jsonschema import Draft202012Validator
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-role-semantics.json")
CONTRACT_VERSION = "1.0.0"
CONSUMER_ID = "role-semantics-validator"
ALLOWED_EXTENSIONS = frozenset({".md", ".toml"})
GEMINI_FRONTMATTER_KEYS = (
    "name",
    "description",
    "kind",
    "max_turns",
    "timeout_mins",
)
GEMINI_METADATA_MUTATIONS = (
    "missing-description",
    "extra-key",
    "duplicate-kind",
    "malformed-description",
    "wildcard-kind",
    "wrong-kind",
    "malformed-max-turns",
    "wrong-timeout",
    "key-order-drift",
)
GEMINI_METADATA_MUTATION_COUNT = len(GEMINI_METADATA_MUTATIONS)
CATEGORY_RULES = {
    "responsibilities": "ROLE-RESPONSIBILITY",
    "outputs": "ROLE-OUTPUT",
    "prohibitedActions": "ROLE-PROHIBITED",
    "stopConditions": "ROLE-STOP",
    "handoffs": "ROLE-HANDOFF",
    "capabilityTier": "ROLE-CAPABILITY-TIER",
    "requiredEvidence": "ROLE-EVIDENCE",
    "adapterStem": "ROLE-ADAPTER-STEM",
}
CONTRACT_CATEGORIES = tuple(
    category for category in CATEGORY_RULES if category != "adapterStem"
)
CATEGORY_SECTIONS = {
    "responsibilities": "Role",
    "outputs": "Outputs",
    "prohibitedActions": "Guardrails",
    "stopConditions": "Guardrails",
    "handoffs": "Handoff / Escalation",
    "capabilityTier": "Capability and Evidence",
    "requiredEvidence": "Capability and Evidence",
}
FORBIDDEN_COMMON_FIELDS = ("model", "tools", "modelReasoningEffort")
NEGATION_STATES = (
    "false",
    "not true",
    "invalid",
    "revoked",
    "retracted",
    "superseded",
    "contradicted",
    "non-operative",
    "not operative",
    "does not apply",
)


def _phrase_pattern(value: str) -> str:
    return re.escape(value).replace(r"\ ", r"\s+")


NEGATION_STATE_PATTERN = "(?:" + "|".join(
    _phrase_pattern(state) for state in NEGATION_STATES
) + ")"
NEGATION_PREDICATE_PATTERN = (
    rf"(?:(?:is|was)\s+{NEGATION_STATE_PATTERN}|does\s+not\s+apply)"
)
REVOKED_CONTEXT = re.compile(
    rf"(?i)(?:^|[\s[(])(?:{NEGATION_STATE_PATTERN}|deprecated|"
    rf"contradiction)\b"
    rf"|\b(?:claim|statement|requirement)\s+{NEGATION_PREDICATE_PATTERN}\b"
    rf"|\bit\s+is\s+{NEGATION_STATE_PATTERN}\s+that\b"
    rf"|\bfollowing\s+(?:claim|statement|requirement|paragraph|item)\s+"
    rf"{NEGATION_PREDICATE_PATTERN}\b"
)
FENCE_START = re.compile(r"^(?: {0,3})(`{3,}|~{3,})(.*)$")
BLOCKQUOTE_START = re.compile(
    r"^ {0,3}(?:(?:[-+*]|\d+[.)])\s+)?(?:>\s*)+"
)
MARKDOWN_UNIT_START = re.compile(
    r"^(?: {0,3})(?:#{1,6}\s|[-+*]\s|\d+[.)]\s|@import\b)"
)
BACK_REFERENCE_REVOCATION = re.compile(
    r"(?i)^(?:(?:this|that|the\s+(?:preceding|previous|above|prior))\s+)?"
    rf"(?:claim|statement|requirement|paragraph|item)\s+"
    rf"{NEGATION_PREDICATE_PATTERN}\.?$"
    rf"|^(?:{NEGATION_STATE_PATTERN}|contradiction)\s*[.:!]?$"
)
FORWARD_REVOCATION = re.compile(
    r"(?i)^(?:the\s+)?following\s+"
    r"(?:claim|statement|requirement|paragraph|item)\s+"
    rf"{NEGATION_PREDICATE_PATTERN}\s*:?[.!]?$"
)
INLINE_CODE_UNIT = re.compile(r"^(`+)(.+)\1$")
LIST_INDENTED_CODE = re.compile(
    r"^ {0,3}(?:[-+*]|\d+[.)]) {4,}\S"
)
ADVERSARIAL_SCHEMA = {
    "yaml-duplicate-name": (
        "local", "code-reviewer", "adapterStem", "yamlDuplicateName",
        "ROLE-ADAPTER-PARSE",
    ),
    "yaml-nonmapping-frontmatter": (
        "claude", "doc-writer", "adapterStem", "yamlNonMapping",
        "ROLE-ADAPTER-PARSE",
    ),
    "yaml-nonscalar-name": (
        "local", "gitops-reviewer", "adapterStem", "yamlNonScalarName",
        "ROLE-ADAPTER-PARSE",
    ),
    "fenced-responsibility": (
        "codex", "incident-responder", "responsibilities", "fenced",
        "ROLE-RESPONSIBILITY",
    ),
    "commented-output": (
        "local", "k8s-implementer", "outputs", "htmlComment", "ROLE-OUTPUT",
    ),
    "struck-prohibition": (
        "claude", "network-reviewer", "prohibitedActions", "strikethrough",
        "ROLE-PROHIBITED",
    ),
    "revoked-stop": (
        "codex", "observability-reviewer", "stopConditions", "revoked",
        "ROLE-STOP",
    ),
    "contradicted-handoff": (
        "local", "security-auditor", "handoffs", "contradicted",
        "ROLE-HANDOFF",
    ),
    "commented-capability": (
        "claude", "supervisor", "capabilityTier", "htmlComment",
        "ROLE-CAPABILITY-TIER",
    ),
    "fenced-evidence": (
        "codex", "wiki-curator", "requiredEvidence", "fenced",
        "ROLE-EVIDENCE",
    ),
    "struck-adapter-heading": (
        "local", "code-reviewer", "adapterStem", "strikethrough",
        "ROLE-ADAPTER-STEM",
    ),
    "wrapped-contradiction": (
        "claude", "doc-writer", "requiredEvidence", "wrappedContradiction",
        "ROLE-EVIDENCE",
    ),
    "quoted-responsibility": (
        "local", "code-reviewer", "responsibilities", "blockquote",
        "ROLE-RESPONSIBILITY",
    ),
    "nested-quoted-output": (
        "claude", "doc-writer", "outputs", "nestedBlockquote", "ROLE-OUTPUT",
    ),
    "lazy-quoted-prohibition": (
        "codex", "gitops-reviewer", "prohibitedActions", "lazyBlockquote",
        "ROLE-PROHIBITED",
    ),
    "quoted-stop": (
        "local", "incident-responder", "stopConditions", "blockquote",
        "ROLE-STOP",
    ),
    "nested-quoted-handoff": (
        "claude", "k8s-implementer", "handoffs", "nestedBlockquote",
        "ROLE-HANDOFF",
    ),
    "lazy-quoted-capability": (
        "codex", "network-reviewer", "capabilityTier", "lazyBlockquote",
        "ROLE-CAPABILITY-TIER",
    ),
    "quoted-evidence": (
        "local", "observability-reviewer", "requiredEvidence", "blockquote",
        "ROLE-EVIDENCE",
    ),
    "indented-tilde-output": (
        "codex", "security-auditor", "outputs", "indentedTildeFence",
        "ROLE-OUTPUT",
    ),
    "following-paragraph-revocation": (
        "claude", "security-auditor", "responsibilities",
        "followingParagraphRevocation", "ROLE-RESPONSIBILITY",
    ),
    "following-list-revocation": (
        "codex", "supervisor", "handoffs", "followingListRevocation",
        "ROLE-HANDOFF",
    ),
    "not-true-claim": (
        "local", "wiki-curator", "prohibitedActions", "notTrue",
        "ROLE-PROHIBITED",
    ),
    "forward-revocation": (
        "claude", "supervisor", "responsibilities", "forwardRevocation",
        "ROLE-RESPONSIBILITY",
    ),
    "external-negative-prefix": (
        "codex", "incident-responder", "outputs", "negativePrefix",
        "ROLE-OUTPUT",
    ),
    "inline-code-only-capability": (
        "local", "k8s-implementer", "capabilityTier", "inlineCodeOnly",
        "ROLE-CAPABILITY-TIER",
    ),
    "list-contained-blockquote": (
        "claude", "network-reviewer", "handoffs", "listBlockquote",
        "ROLE-HANDOFF",
    ),
    "quoted-adapter-heading": (
        "codex", "code-reviewer", "adapterStem", "blockquote",
        "ROLE-ADAPTER-STEM",
    ),
    "nested-quoted-adapter-heading": (
        "claude", "gitops-reviewer", "adapterStem", "nestedBlockquote",
        "ROLE-ADAPTER-STEM",
    ),
    "unordered-list-indented-code": (
        "local", "observability-reviewer", "outputs",
        "unorderedListIndentedCode", "ROLE-OUTPUT",
    ),
    "ordered-list-indented-code": (
        "codex", "security-auditor", "requiredEvidence",
        "orderedListIndentedCode", "ROLE-EVIDENCE",
    ),
    "forward-false-revocation": (
        "local", "doc-writer", "outputs", "forwardFalse",
        "ROLE-OUTPUT",
    ),
    "backward-not-true-revocation": (
        "codex", "gitops-reviewer", "stopConditions", "backwardNotTrue",
        "ROLE-STOP",
    ),
}


class UniqueKeySafeLoader(yaml.SafeLoader):
    """YAML SafeLoader that rejects duplicate mapping keys at every depth."""


def _construct_unique_mapping(
    loader: UniqueKeySafeLoader, node: MappingNode, deep: bool = False
) -> dict[Any, Any]:
    if not isinstance(node, MappingNode):
        raise ConstructorError(
            None, None, "expected a mapping node", node.start_mark
        )
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


class ContractError(ValueError):
    """Stable contract or adapter input failure."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


def fail(code: str, detail: str) -> NoReturn:
    raise ContractError(code, detail)


@dataclass(frozen=True)
class Adapter:
    surface: str
    path: str
    path_stem: str
    declared_name: str
    heading: str
    section_units: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class HarnessSelection:
    """Current role semantics and adapter layout selected by the harness."""

    role_ids: tuple[str, ...]
    surface_ids: tuple[str, ...]
    roles: dict[str, dict[str, Any]]
    locations: dict[str, tuple[PurePosixPath, str]]
    projection_paths: dict[tuple[str, str], PurePosixPath]


@dataclass(frozen=True)
class Diagnostic:
    code: str
    path: str
    role: str
    detail: str

    def render(self) -> str:
        return f"ERR {self.code} {self.path} role={self.role}: {self.detail}"


def load_json(root: Path, relative: PurePosixPath) -> Any:
    path = safe_repo_path(
        root,
        relative,
        final_kind="file",
        code="ROLE-JSON",
    )
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail("ROLE-JSON", f"{path}: {exc}")


def normalize_whitespace(value: str) -> str:
    """Normalize whitespace only; punctuation, case, and Markdown stay semantic."""

    return " ".join(value.split())


def safe_relative_root(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        fail("ROLE-ADAPTER-SURFACES", f"unsafe surface path root: {value!r}")
    return path


def safe_repo_path(
    root: Path,
    relative: PurePosixPath | str,
    *,
    final_kind: str,
    code: str,
) -> Path:
    raw = relative.as_posix() if isinstance(relative, PurePosixPath) else relative
    candidate_relative = PurePosixPath(raw)
    segments = raw.split("/")
    if (
        candidate_relative.is_absolute()
        or not segments
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        fail(code, f"{raw}: expected a normalized repository-relative path")
    try:
        absolute_root = root.absolute()
        root_mode = os.lstat(absolute_root).st_mode
    except OSError as exc:
        fail(code, f"repository root: {exc}")
    if stat.S_ISLNK(root_mode) or not stat.S_ISDIR(root_mode):
        fail(code, "repository root must be a non-symlink directory")
    strict_root = absolute_root.resolve(strict=True)
    candidate = strict_root
    for index, segment in enumerate(segments):
        candidate = candidate / segment
        try:
            mode = os.lstat(candidate).st_mode
        except OSError as exc:
            fail(code, f"{raw}: {exc}")
        if stat.S_ISLNK(mode):
            fail(code, f"{raw}: symlink path component {segment!r} is forbidden")
        is_final = index == len(segments) - 1
        if not is_final and not stat.S_ISDIR(mode):
            fail(code, f"{raw}: parent component {segment!r} is not a directory")
        if is_final:
            expected = (
                stat.S_ISREG(mode)
                if final_kind == "file"
                else stat.S_ISDIR(mode)
            )
            if not expected:
                fail(code, f"{raw}: expected a regular non-symlink {final_kind}")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(strict_root)
    except (OSError, ValueError) as exc:
        fail(code, f"{raw}: resolved path escapes the repository root: {exc}")
    return resolved


def select_current_harness(contract: dict[str, Any]) -> HarnessSelection:
    """Select the current adapter claims without a hard-coded roster or layout."""

    if contract.get("contractVersion") != CONTRACT_VERSION:
        fail("ROLE-CONTRACT-VERSION", "harness contract version differs")
    consumers = contract.get("consumers")
    if not isinstance(consumers, list):
        fail("ROLE-CONSUMER", "harness consumers must be a list")
    selected = [
        consumer for consumer in consumers
        if isinstance(consumer, dict) and consumer.get("id") == CONSUMER_ID
    ]
    if len(selected) != 1 or (
        selected[0].get("selectedContract"),
        selected[0].get("selectedVersion"),
        selected[0].get("migrationState"),
    ) != ("harness-contract", CONTRACT_VERSION, "current"):
        fail(
            "ROLE-CONSUMER",
            "role semantics validator must select harness-contract/1.0.0/current",
        )

    inventory = contract.get("currentInventory")
    if not isinstance(inventory, dict) or inventory.get("state") != "current":
        fail("ROLE-INVENTORY", "currentInventory must be a current object")
    role_ids = tuple(inventory.get("roleIds", ()))
    surface_ids = tuple(inventory.get("surfaceIds", ()))
    if (
        not role_ids
        or not surface_ids
        or not all(isinstance(item, str) for item in (*role_ids, *surface_ids))
        or len(role_ids) != len(set(role_ids))
        or len(surface_ids) != len(set(surface_ids))
    ):
        fail("ROLE-INVENTORY", "current role and surface identities differ")
    expected_counts = (
        len(role_ids),
        len(surface_ids),
        len(role_ids) * len(surface_ids),
    )
    actual_counts = (
        inventory.get("expectedRoleCount"),
        inventory.get("expectedSurfaceCount"),
        inventory.get("expectedProjectionCount"),
    )
    if actual_counts != expected_counts:
        fail("ROLE-INVENTORY", "current inventory counts differ")

    canonical = contract.get("canonicalRoles")
    if not isinstance(canonical, list):
        fail("ROLE-IDS", "canonicalRoles must be a list")
    canonical_by_id = {
        role.get("id"): role
        for role in canonical
        if isinstance(role, dict) and isinstance(role.get("id"), str)
    }
    semantic_keys = {
        "admissionState",
        "responsibilities",
        "outputs",
        "prohibitedActions",
        "stopConditions",
        "handoffs",
        "capabilityTier",
        "capabilityTierClaim",
        "requiredEvidence",
    }
    roles: dict[str, dict[str, Any]] = {}
    for role_id in role_ids:
        role = canonical_by_id.get(role_id)
        if not isinstance(role, dict) or role.get("admissionState") != "current":
            fail("ROLE-IDS", f"{role_id} is not a current canonical role")
        semantics = role.get("adapterSemantics")
        if not isinstance(semantics, dict) or set(semantics) != semantic_keys:
            fail("ROLE-CATEGORIES", f"{role_id} adapter semantics differ")
        if semantics.get("admissionState") != "current":
            fail("ROLE-CATEGORIES", f"{role_id} adapter semantics are not current")
        roles[role_id] = {
            "id": role_id,
            **{
                key: copy.deepcopy(value)
                for key, value in semantics.items()
                if key != "admissionState"
            },
        }

    surfaces = contract.get("surfaces")
    if not isinstance(surfaces, list):
        fail("ROLE-ADAPTER-SURFACES", "surfaces must be a list")
    surface_by_id = {
        surface.get("id"): surface
        for surface in surfaces
        if isinstance(surface, dict) and isinstance(surface.get("id"), str)
    }
    locations: dict[str, tuple[PurePosixPath, str]] = {}
    for surface_id in surface_ids:
        surface = surface_by_id.get(surface_id)
        if not isinstance(surface, dict) or surface.get("admissionState") != "current":
            fail(
                "ROLE-ADAPTER-SURFACES",
                f"{surface_id} is not a current canonical surface",
            )
        path_root = surface.get("pathRoot")
        extension = surface.get("extension")
        if (
            not isinstance(path_root, str)
            or not isinstance(extension, str)
            or extension not in ALLOWED_EXTENSIONS
        ):
            fail(
                "ROLE-ADAPTER-SURFACES",
                f"{surface_id} adapter location differs",
            )
        locations[surface_id] = (safe_relative_root(path_root), extension)

    projections = inventory.get("projections")
    if not isinstance(projections, list):
        fail("ROLE-INVENTORY", "current projections must be a list")
    expected_projection_paths = {
        (role_id, surface_id): (
            locations[surface_id][0]
            / f"{role_id}{locations[surface_id][1]}"
        )
        for role_id in role_ids
        for surface_id in surface_ids
    }
    actual_projection_paths: dict[tuple[str, str], PurePosixPath] = {}
    for projection in projections:
        if not isinstance(projection, dict):
            fail("ROLE-INVENTORY", "current projection must be an object")
        key = (projection.get("roleId"), projection.get("surfaceId"))
        path = projection.get("path")
        if (
            key not in expected_projection_paths
            or projection.get("admissionState") != "current"
            or not isinstance(path, str)
            or PurePosixPath(path) != expected_projection_paths[key]
            or key in actual_projection_paths
        ):
            fail("ROLE-INVENTORY", "current projection layout differs")
        actual_projection_paths[key] = PurePosixPath(path)
    if actual_projection_paths != expected_projection_paths:
        fail("ROLE-INVENTORY", "current projection membership differs")

    return HarnessSelection(
        role_ids=role_ids,
        surface_ids=surface_ids,
        roles=roles,
        locations=locations,
        projection_paths=actual_projection_paths,
    )


def validate_contract(
    root: Path, raw_contract: dict[str, Any] | None = None
) -> HarnessSelection:
    schema = load_json(root, SCHEMA_PATH)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes multiple schema subclasses
        fail("ROLE-SCHEMA-DEFINITION", str(exc))
    contract = (
        copy.deepcopy(raw_contract)
        if raw_contract is not None
        else load_json(root, CONTRACT_PATH)
    )
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        fail("ROLE-SCHEMA", f"{location}: {error.message}")

    selection = select_current_harness(contract)

    anchors: dict[str, tuple[str, str]] = {}
    for role in selection.roles.values():
        role_id = role["id"]
        if role["capabilityTier"] not in {"top", "worker"}:
            fail(
                "ROLE-CAPABILITY-TIER",
                f"{role_id} declares an unsupported capability tier",
            )
        for category in CONTRACT_CATEGORIES:
            claims = (
                [role["capabilityTierClaim"]]
                if category == "capabilityTier"
                else role[category]
            )
            for claim in claims:
                normalized = normalize_whitespace(claim)
                if normalized != claim:
                    fail(
                        "ROLE-ANCHOR-WHITESPACE",
                        f"{role_id}/{category} anchor is not whitespace-normalized",
                    )
                if claim in anchors:
                    other_role, other_category = anchors[claim]
                    fail(
                        "ROLE-ANCHOR-UNIQUE",
                        f"{role_id}/{category} duplicates "
                        f"{other_role}/{other_category}",
                    )
                anchors[claim] = (role_id, category)
    return selection


def parse_frontmatter(text: str, path: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        fail("ROLE-ADAPTER-PARSE", f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail("ROLE-ADAPTER-PARSE", f"{path}: unterminated YAML frontmatter")
    raw_frontmatter = text[4:end]
    body = text[end + 5 :]
    try:
        metadata = yaml.load(raw_frontmatter, Loader=UniqueKeySafeLoader)
    except yaml.YAMLError as exc:
        fail("ROLE-ADAPTER-PARSE", f"{path}: invalid YAML frontmatter: {exc}")
    if not isinstance(metadata, dict) or not all(
        isinstance(key, str) for key in metadata
    ):
        fail(
            "ROLE-ADAPTER-PARSE",
            f"{path}: YAML frontmatter must be a string-keyed mapping",
        )
    if not isinstance(metadata.get("name"), str):
        fail(
            "ROLE-ADAPTER-PARSE",
            f"{path}: YAML frontmatter name must be a string scalar",
        )
    return metadata, body


def _without_html_comments(body: str, path: str) -> str:
    output: list[str] = []
    position = 0
    while position < len(body):
        opening = body.find("<!--", position)
        closing = body.find("-->", position)
        if closing >= 0 and (opening < 0 or closing < opening):
            fail("ROLE-ADAPTER-PARSE", f"{path}: unmatched HTML comment close")
        if opening < 0:
            output.append(body[position:])
            break
        output.append(body[position:opening])
        end = body.find("-->", opening + 4)
        if end < 0:
            fail("ROLE-ADAPTER-PARSE", f"{path}: unterminated HTML comment")
        hidden = body[opening : end + 3]
        output.append("\n" * hidden.count("\n"))
        position = end + 3
    return "".join(output)


def _without_strikethrough(body: str, path: str) -> str:
    chunks = body.split("~~")
    if (len(chunks) - 1) % 2:
        fail("ROLE-ADAPTER-PARSE", f"{path}: unmatched strikethrough delimiter")
    output: list[str] = []
    for index, chunk in enumerate(chunks):
        output.append(chunk if index % 2 == 0 else "\n" * chunk.count("\n"))
    return "".join(output)


def _without_code_blocks(body: str, path: str) -> str:
    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in body.splitlines():
        if fence_character is not None:
            close_pattern = (
                rf" {{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[ \t]*"
            )
            if re.fullmatch(close_pattern, line):
                fence_character = None
                fence_length = 0
            output.append("")
            continue
        fence = FENCE_START.fullmatch(line)
        if fence is not None:
            marker = fence.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            output.append("")
            continue
        output.append(
            ""
            if line.startswith(("    ", "\t")) or LIST_INDENTED_CODE.match(line)
            else line
        )
    if fence_character is not None:
        fail("ROLE-ADAPTER-PARSE", f"{path}: unterminated fenced code block")
    return "\n".join(output)


def _without_blockquotes(lines: list[str]) -> list[str]:
    """Exclude blockquote starts plus nested or lazy continuation lines."""

    output: list[str] = []
    in_blockquote = False
    for line in lines:
        if in_blockquote:
            if not line.strip():
                output.append("")
                in_blockquote = False
            elif BLOCKQUOTE_START.match(line):
                output.append("")
            elif MARKDOWN_UNIT_START.match(line):
                in_blockquote = False
                output.append(line)
            else:
                output.append("")
            continue
        if BLOCKQUOTE_START.match(line):
            in_blockquote = True
            output.append("")
            continue
        output.append(line)
    return output


def _without_revoked_units(lines: list[str]) -> list[str]:
    """Exclude an entire Markdown paragraph or list item if it is revoked."""

    output: list[str] = []
    current: list[str] = []
    previous_operative_indexes: list[int] = []
    revoke_next_unit = False

    def semantic_text(raw_unit: str) -> str:
        return re.sub(
            r"^(?:#{1,6}\s+|[-+*]\s+|\d+[.)]\s+)", "", raw_unit
        )

    def flush() -> None:
        nonlocal previous_operative_indexes, revoke_next_unit
        if not current:
            return
        unit = normalize_whitespace("\n".join(current))
        semantic_unit = semantic_text(unit)
        if REVOKED_CONTEXT.search(unit):
            if BACK_REFERENCE_REVOCATION.fullmatch(semantic_unit):
                for index in previous_operative_indexes:
                    output[index] = ""
            if FORWARD_REVOCATION.fullmatch(semantic_unit):
                revoke_next_unit = True
            output.extend("" for _ in current)
        elif revoke_next_unit or INLINE_CODE_UNIT.fullmatch(semantic_unit):
            output.extend("" for _ in current)
            previous_operative_indexes = []
            revoke_next_unit = False
        else:
            start = len(output)
            output.extend(current)
            previous_operative_indexes = list(range(start, len(output)))
        current.clear()

    for line in lines:
        if not line.strip():
            flush()
            output.append("")
            continue
        if current and FORWARD_REVOCATION.fullmatch(
            semantic_text(normalize_whitespace("\n".join(current)))
        ):
            flush()
        if current and MARKDOWN_UNIT_START.match(line):
            flush()
        current.append(line)
    flush()
    return output


def operative_markdown(body: str, path: str) -> str:
    """Return only operative prose/headings from an adapter Markdown body."""

    uncommented = _without_html_comments(body, path)
    without_code = _without_code_blocks(uncommented, path)
    visible = _without_strikethrough(without_code, path)
    unquoted = _without_blockquotes(visible.splitlines())
    return "\n".join(_without_revoked_units(unquoted))


def extract_section_units(body: str) -> dict[str, tuple[str, ...]]:
    sections: dict[str, list[str]] = {}
    current_section: str | None = None
    current_unit: list[str] = []

    def flush() -> None:
        if current_section is None or not current_unit:
            current_unit.clear()
            return
        unit = normalize_whitespace("\n".join(current_unit))
        unit = re.sub(r"^(?:[-+*]\s+|\d+[.)]\s+)", "", unit)
        if unit:
            sections.setdefault(current_section, []).append(unit)
        current_unit.clear()

    for line in body.splitlines():
        section_heading = re.fullmatch(r"## ([^\n]+?)\s*", line)
        if section_heading is not None:
            flush()
            current_section = section_heading.group(1).strip()
            sections.setdefault(current_section, [])
            continue
        if re.match(r"^#{1,6}\s", line):
            flush()
            continue
        if not line.strip():
            flush()
            continue
        if current_unit and MARKDOWN_UNIT_START.match(line):
            flush()
        current_unit.append(line)
    flush()
    return {section: tuple(units) for section, units in sections.items()}


def extract_heading(body: str) -> str:
    headings = re.findall(r"(?m)^# ([^\n]+?)\s*$", body)
    return headings[0].strip() if len(headings) == 1 else ""


def validate_gemini_frontmatter(
    metadata: dict[str, Any],
    relative_path: PurePosixPath,
) -> None:
    role_id = relative_path.stem
    if tuple(metadata) != GEMINI_FRONTMATTER_KEYS:
        fail(
            "ROLE-ADAPTER-PARSE",
            f"{relative_path}: Gemini frontmatter keys or key order differ",
        )
    if metadata["name"] != role_id:
        fail("ROLE-ADAPTER-PARSE", f"{relative_path}: name must match file stem")
    description = metadata["description"]
    if not isinstance(description, str) or not description.strip():
        fail(
            "ROLE-ADAPTER-PARSE",
            f"{relative_path}: description must be a non-empty string",
        )
    wildcard_values = {"*", "all", "inherit", "inherited-all"}
    for field in ("name", "description", "kind"):
        value = metadata[field]
        if isinstance(value, str) and value.strip().lower() in wildcard_values:
            fail(
                "ROLE-ADAPTER-PARSE",
                f"{relative_path}: wildcard {field} is forbidden",
            )
    if metadata["kind"] != "local":
        fail("ROLE-ADAPTER-PARSE", f"{relative_path}: kind must be local")
    expected_limits = (12, 30) if role_id == "supervisor" else (8, 20)
    actual_limits = (metadata["max_turns"], metadata["timeout_mins"])
    if any(type(value) is not int for value in actual_limits):
        fail(
            "ROLE-ADAPTER-PARSE",
            f"{relative_path}: turn and timeout limits must be integers",
        )
    if actual_limits != expected_limits:
        fail(
            "ROLE-ADAPTER-PARSE",
            f"{relative_path}: turn and timeout limits differ from the closed role values",
        )


def parse_adapter_text(
    surface: str,
    relative_path: PurePosixPath,
    text: str,
) -> Adapter:
    suffix = relative_path.suffix
    if suffix == ".md":
        metadata, body = parse_frontmatter(text, relative_path.as_posix())
        declared_name = metadata["name"]
        if surface == "gemini":
            validate_gemini_frontmatter(metadata, relative_path)
    else:
        try:
            data = tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            fail("ROLE-ADAPTER-PARSE", f"{relative_path}: {exc}")
        body_value = data.get("developer_instructions")
        if not isinstance(body_value, str):
            fail(
                "ROLE-ADAPTER-PARSE",
                f"{relative_path}: developer_instructions must be a string",
            )
        declared_name = data.get("name", "")
        if not isinstance(declared_name, str):
            fail("ROLE-ADAPTER-PARSE", f"{relative_path}: name must be a string")
        body = body_value

    operative_body = operative_markdown(body, relative_path.as_posix())
    return Adapter(
        surface=surface,
        path=relative_path.as_posix(),
        path_stem=relative_path.stem,
        declared_name=declared_name,
        heading=extract_heading(operative_body),
        section_units=extract_section_units(operative_body),
    )


def adapter_source(
    root: Path,
    selection: HarnessSelection,
    surface: str,
    role_id: str,
) -> tuple[PurePosixPath, str]:
    relative_path = selection.projection_paths[(role_id, surface)]
    try:
        text = safe_repo_path(
            root,
            relative_path,
            final_kind="file",
            code="ROLE-ADAPTER-PARSE",
        ).read_text(encoding="utf-8")
    except OSError as exc:
        fail("ROLE-ADAPTER-PARSE", f"{relative_path}: {exc}")
    return relative_path, text


def _missing_claims(
    adapter: Adapter, category: str, claims: list[str]
) -> list[str]:
    section = CATEGORY_SECTIONS[category]
    operative_units = set(adapter.section_units.get(section, ()))
    return [claim for claim in claims if claim not in operative_units]


def validate_adapter(role: dict[str, Any], adapter: Adapter) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    role_id = role["id"]
    stem_values = (adapter.path_stem, adapter.declared_name, adapter.heading)
    if any(value != role_id for value in stem_values):
        diagnostics.append(
            Diagnostic(
                "ROLE-ADAPTER-STEM",
                adapter.path,
                role_id,
                "path stem, declared name, and H1 must all equal the role id",
            )
        )

    for category in CONTRACT_CATEGORIES:
        claims = (
            [role["capabilityTierClaim"]]
            if category == "capabilityTier"
            else role[category]
        )
        missing = _missing_claims(adapter, category, claims)
        if missing:
            diagnostics.append(
                Diagnostic(
                    CATEGORY_RULES[category],
                    adapter.path,
                    role_id,
                    f"missing {category} claim: {missing[0]}",
                )
            )
    return diagnostics


def repository_adapters(
    root: Path, selection: HarnessSelection
) -> dict[tuple[str, str], Adapter]:
    return {
        (surface, role_id): parse_adapter_text(
            surface,
            *adapter_source(root, selection, surface, role_id),
        )
        for surface in selection.surface_ids
        for role_id in selection.role_ids
    }


def validate_repository(root: Path) -> list[Diagnostic]:
    selection = validate_contract(root)
    adapters = repository_adapters(root, selection)
    return [
        diagnostic
        for surface in selection.surface_ids
        for role_id in selection.role_ids
        for diagnostic in validate_adapter(
            selection.roles[role_id], adapters[(surface, role_id)]
        )
    ]


def validate_fixture(
    fixture: dict[str, Any], selection: HarnessSelection
) -> None:
    expected_keys = {
        "schemaVersion",
        "adapterSurfaces",
        "roles",
        "categories",
        "mutations",
        "geminiMetadataMutations",
        "forbiddenCommonFields",
        "negationStates",
        "adversarialCases",
        "expectedCaseCount",
    }
    if set(fixture) != expected_keys or fixture["schemaVersion"] != 3:
        fail("ROLE-FIXTURE", "fixture keys or schemaVersion differ")
    if tuple(fixture["adapterSurfaces"]) != selection.surface_ids:
        fail("ROLE-FIXTURE", "fixture adapter surfaces differ")
    if tuple(fixture["roles"]) != selection.role_ids:
        fail("ROLE-FIXTURE", "fixture roles differ")
    if fixture["categories"] != CATEGORY_RULES:
        fail("ROLE-FIXTURE", "fixture category rule IDs differ")
    if tuple(fixture["mutations"]) != ("remove", "replace"):
        fail("ROLE-FIXTURE", "fixture mutations must be remove then replace")
    if tuple(fixture["geminiMetadataMutations"]) != GEMINI_METADATA_MUTATIONS:
        fail("ROLE-FIXTURE", "Gemini metadata mutations differ")
    if tuple(fixture["forbiddenCommonFields"]) != FORBIDDEN_COMMON_FIELDS:
        fail("ROLE-FIXTURE", "forbidden common fields differ")
    if tuple(fixture["negationStates"]) != NEGATION_STATES:
        fail("ROLE-FIXTURE", "negation state vocabulary differs")
    expected_count = (
        len(selection.surface_ids)
        * len(selection.role_ids)
        * len(CATEGORY_RULES)
        * 2
    )
    if fixture["expectedCaseCount"] != expected_count:
        fail("ROLE-FIXTURE", f"expectedCaseCount must equal {expected_count}")
    adversarial = fixture["adversarialCases"]
    if not isinstance(adversarial, list):
        fail("ROLE-FIXTURE", "adversarialCases must be a list")
    actual_adversarial: dict[str, tuple[str, str, str, str, str]] = {}
    required_case_keys = {
        "name", "adapterSurface", "role", "category", "mutation", "expectedRule"
    }
    for case in adversarial:
        if not isinstance(case, dict) or set(case) != required_case_keys:
            fail("ROLE-FIXTURE", "adversarial case keys differ")
        name = case["name"]
        if not isinstance(name, str) or name in actual_adversarial:
            fail("ROLE-FIXTURE", "adversarial case names must be unique strings")
        actual_adversarial[name] = (
            case["adapterSurface"], case["role"], case["category"],
            case["mutation"], case["expectedRule"],
        )
    if actual_adversarial != ADVERSARIAL_SCHEMA:
        fail("ROLE-FIXTURE", "adversarial case semantics differ")


def category_anchor(
    role: dict[str, Any],
    category: str,
) -> str:
    if category == "adapterStem":
        return f"# {role['id']}"
    claims = (
        [role["capabilityTierClaim"]]
        if category == "capabilityTier"
        else role[category]
    )
    return claims[0]


def replace_source_anchor(
    source: str, anchor: str, replacement: str, path: PurePosixPath, label: str
) -> str:
    if source.count(anchor) != 1:
        fail(
            "ROLE-SELF-TEST",
            f"{path}/{label} anchor must occur exactly once",
        )
    return source.replace(anchor, replacement, 1)


def mutate_source(
    source: str,
    role: dict[str, Any],
    category: str,
    mutation: str,
    path: PurePosixPath,
) -> str:
    anchor = category_anchor(role, category)
    if mutation == "remove":
        replacement = ""
    elif mutation == "replace":
        replacement = f"mutated-{category}-claim"
    elif mutation == "fenced":
        replacement = f"\n\n```text\n{anchor}\n```\n\n"
    elif mutation == "indentedTildeFence":
        replacement = f"\n\n   ~~~~ text\n{anchor}\n   ~~~~\n\n"
    elif mutation == "unorderedListIndentedCode":
        replacement = f"    {anchor}"
    elif mutation == "orderedListIndentedCode":
        replacement = f"\n1.     {anchor}"
    elif mutation == "htmlComment":
        replacement = f"<!-- {anchor} -->"
    elif mutation == "strikethrough":
        replacement = f"~~{anchor}~~"
    elif mutation == "blockquote":
        replacement = f"\n\n> {anchor}\n\n"
    elif mutation == "nestedBlockquote":
        replacement = f"\n\n> > {anchor}\n\n"
    elif mutation == "lazyBlockquote":
        replacement = f"\n\n> {anchor}\nlazy quoted continuation\n\n"
    elif mutation == "listBlockquote":
        replacement = f"> {anchor}"
    elif mutation == "revoked":
        replacement = f"REVOKED: {anchor}"
    elif mutation == "contradicted":
        replacement = f"CONTRADICTION: {anchor}"
    elif mutation == "wrappedContradiction":
        replacement = f"{anchor}\nThis statement is contradicted."
    elif mutation == "followingParagraphRevocation":
        replacement = f"{anchor}\n\nThis statement is contradicted."
    elif mutation == "followingListRevocation":
        replacement = f"{anchor}\n- The preceding statement is revoked."
    elif mutation == "notTrue":
        replacement = f"It is not true that {anchor}"
    elif mutation == "forwardRevocation":
        replacement = f"The following claim does not apply:\n{anchor}"
    elif mutation == "negativePrefix":
        replacement = f"Do not {anchor}"
    elif mutation == "inlineCodeOnly":
        replacement = f"``{anchor}``"
    elif mutation == "forwardFalse":
        replacement = f"The following statement is false:\n\n{anchor}"
    elif mutation == "backwardNotTrue":
        replacement = f"{anchor}\n\nThis statement is not true."
    elif mutation == "yamlDuplicateName":
        yaml_anchor = f"name: {role['id']}"
        return replace_source_anchor(
            source,
            yaml_anchor,
            f"{yaml_anchor}\nname: conflicting-role",
            path,
            mutation,
        )
    elif mutation == "yamlNonScalarName":
        yaml_anchor = f"name: {role['id']}"
        return replace_source_anchor(
            source,
            yaml_anchor,
            "name:\n  nested: conflicting-role",
            path,
            mutation,
        )
    elif mutation == "yamlNonMapping":
        end = source.find("\n---\n", 4)
        if not source.startswith("---\n") or end < 0:
            fail("ROLE-SELF-TEST", f"{path}: frontmatter boundary missing")
        return "---\n- invalid-frontmatter\n---\n" + source[end + 5 :]
    else:
        fail("ROLE-SELF-TEST", f"{path}: unknown mutation {mutation!r}")
    return replace_source_anchor(source, anchor, replacement, path, category)


def validate_mutated_source(
    surface: str,
    path: PurePosixPath,
    source: str,
    role: dict[str, Any],
) -> list[str]:
    try:
        adapter = parse_adapter_text(surface, path, source)
    except ContractError as exc:
        return [exc.code]
    return [diagnostic.code for diagnostic in validate_adapter(role, adapter)]


def mutate_gemini_frontmatter(source: str, mutation: str) -> str:
    if mutation == "missing-description":
        return re.sub(
            r"^description: .*\n", "", source, count=1, flags=re.MULTILINE
        )
    if mutation == "extra-key":
        return source.replace(
            "timeout_mins:",
            "tools: [read_file]\n" "timeout_mins:",
            1,
        )
    if mutation == "duplicate-kind":
        return source.replace("kind:", "kind: local\nkind:", 1)
    if mutation == "malformed-description":
        return re.sub(
            r"^description: .*$",
            "description: [invalid]",
            source,
            count=1,
            flags=re.MULTILINE,
        )
    if mutation == "wildcard-kind":
        return re.sub(
            r"^kind: .*$", 'kind: "*"', source, count=1, flags=re.MULTILINE
        )
    if mutation == "wrong-kind":
        return re.sub(
            r"^kind: .*$", "kind: remote", source, count=1, flags=re.MULTILINE
        )
    if mutation == "malformed-max-turns":
        return re.sub(
            r"^max_turns: .*$",
            "max_turns: many",
            source,
            count=1,
            flags=re.MULTILINE,
        )
    if mutation == "wrong-timeout":
        return re.sub(
            r"^timeout_mins: .*$",
            "timeout_mins: 0",
            source,
            count=1,
            flags=re.MULTILINE,
        )
    if mutation == "key-order-drift":
        return re.sub(
            r"^(max_turns: .*\n)(timeout_mins: .*\n)",
            r"\2\1",
            source,
            count=1,
            flags=re.MULTILINE,
        )
    fail("ROLE-SELF-TEST", f"unknown Gemini frontmatter mutation {mutation!r}")


def run_self_test(root: Path) -> tuple[list[str], int]:
    selection = validate_contract(root)
    roles = selection.roles
    fixture = load_json(root, FIXTURE_PATH)
    validate_fixture(fixture, selection)
    sources = {
        (surface, role_id): adapter_source(
            root, selection, surface, role_id
        )
        for surface in selection.surface_ids
        for role_id in selection.role_ids
    }
    adapters = {
        key: parse_adapter_text(key[0], path, source)
        for key, (path, source) in sources.items()
    }
    baseline = [
        diagnostic
        for surface in selection.surface_ids
        for role_id in selection.role_ids
        for diagnostic in validate_adapter(roles[role_id], adapters[(surface, role_id)])
    ]
    if baseline:
        return (["baseline adapters fail: " + baseline[0].render()], 0)

    failures: list[str] = []
    cases = 0
    for surface in selection.surface_ids:
        for role_id in selection.role_ids:
            role = roles[role_id]
            path, base_source = sources[(surface, role_id)]
            for category, expected_rule in CATEGORY_RULES.items():
                for mutation in fixture["mutations"]:
                    cases += 1
                    mutated_source = mutate_source(
                        base_source, role, category, mutation, path
                    )
                    actual_rules = validate_mutated_source(
                        surface,
                        path,
                        mutated_source,
                        role,
                    )
                    if actual_rules != [expected_rule]:
                        failures.append(
                            f"{surface}/{role_id}/{category}/{mutation}: "
                            f"expected {[expected_rule]!r}, got {actual_rules!r}"
                        )

    for case in fixture["adversarialCases"]:
        surface = case["adapterSurface"]
        role_id = case["role"]
        role = roles[role_id]
        path, base_source = sources[(surface, role_id)]
        mutated_source = mutate_source(
            base_source, role, case["category"], case["mutation"], path
        )
        actual_rules = validate_mutated_source(
            surface,
            path,
            mutated_source,
            role,
        )
        if actual_rules != [case["expectedRule"]]:
            failures.append(
                f"adversarial/{case['name']}: expected "
                f"{[case['expectedRule']]!r}, got {actual_rules!r}"
            )

    gemini_path, gemini_source = sources[("gemini", "code-reviewer")]
    gemini_role = roles["code-reviewer"]
    for mutation in fixture["geminiMetadataMutations"]:
        actual_rules = validate_mutated_source(
            "gemini",
            gemini_path,
            mutate_gemini_frontmatter(gemini_source, mutation),
            gemini_role,
        )
        if actual_rules != ["ROLE-ADAPTER-PARSE"]:
            failures.append(
                f"gemini-frontmatter/{mutation}: expected "
                f"['ROLE-ADAPTER-PARSE'], got {actual_rules!r}"
            )

    vocabulary_surface = "local"
    vocabulary_role = roles["code-reviewer"]
    vocabulary_path, vocabulary_source = sources[
        (vocabulary_surface, "code-reviewer")
    ]
    vocabulary_anchor = category_anchor(vocabulary_role, "responsibilities")
    for state in fixture["negationStates"]:
        predicate = (
            "does not apply" if state == "does not apply" else f"is {state}"
        )
        for direction, replacement in (
            (
                "forward",
                f"The following statement {predicate}:\n\n{vocabulary_anchor}",
            ),
            (
                "backward",
                f"{vocabulary_anchor}\n\nThis statement {predicate}.",
            ),
        ):
            mutated_source = replace_source_anchor(
                vocabulary_source,
                vocabulary_anchor,
                replacement,
                vocabulary_path,
                f"vocabulary-{direction}-{state}",
            )
            actual_rules = validate_mutated_source(
                vocabulary_surface,
                vocabulary_path,
                mutated_source,
                vocabulary_role,
            )
            if actual_rules != ["ROLE-RESPONSIBILITY"]:
                failures.append(
                    f"vocabulary/{direction}/{state}: expected "
                    f"['ROLE-RESPONSIBILITY'], got {actual_rules!r}"
                )

    raw_contract = load_json(root, CONTRACT_PATH)
    for forbidden in fixture["forbiddenCommonFields"]:
        mutated_contract = copy.deepcopy(raw_contract)
        mutated_contract["canonicalRoles"][0]["adapterSemantics"][
            forbidden
        ] = "adapter-owned"
        try:
            validate_contract(root, mutated_contract)
        except ContractError as exc:
            if exc.code != "ROLE-SCHEMA":
                failures.append(
                    f"forbidden field {forbidden}: expected ROLE-SCHEMA, got {exc.code}"
                )
        else:
            failures.append(f"forbidden field {forbidden}: mutation passed")

    with tempfile.TemporaryDirectory(
        prefix="agent-role-semantics-root-boundary-"
    ) as directory:
        symlink_root = Path(directory) / "repository-root-link"
        symlink_root.symlink_to(root.absolute(), target_is_directory=True)
        try:
            validate_contract(symlink_root)
        except ContractError as exc:
            if exc.code != "ROLE-JSON":
                failures.append(
                    "symlink root: expected ROLE-JSON, "
                    f"got {exc.code}"
                )
        else:
            failures.append("symlink root: mutation passed")
    return failures, cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    root = args.root.absolute()
    try:
        if args.self_test:
            failures, cases = run_self_test(root)
            if failures:
                for failure in failures:
                    print(f"ERR ROLE-SELF-TEST {failure}", file=sys.stderr)
                return 1
            print(
                "[PASS] agent role semantics self-test passed: "
                f"cases={cases} adversarial={len(ADVERSARIAL_SCHEMA)} "
                f"vocabulary={len(NEGATION_STATES) * 2} "
                f"geminiMetadata={GEMINI_METADATA_MUTATION_COUNT} "
                f"roles={len(validate_contract(root).role_ids)} "
                f"adapters={len(validate_contract(root).projection_paths)} "
                f"categories={len(CATEGORY_RULES)}"
            )
            return 0

        selection = validate_contract(root)
        diagnostics = validate_repository(root)
        if diagnostics:
            for diagnostic in diagnostics:
                print(diagnostic.render(), file=sys.stderr)
            return 1
        print(
            "[PASS] agent role semantics validation passed: "
            f"roles={len(selection.role_ids)} "
            f"adapters={len(selection.projection_paths)} "
            f"categories={len(CATEGORY_RULES)}"
        )
        return 0
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, ContractError):
            print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        else:
            print(f"ERR ROLE-INPUT {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
