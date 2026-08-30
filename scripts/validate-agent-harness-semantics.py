#!/usr/bin/env python3
"""Validate harness-owned role semantics across provider adapter surfaces."""

from __future__ import annotations

import argparse
import copy
import os
import re
import stat
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

from agent_registry_compat import load_terminal_validator


REGISTRY_PATH = PurePosixPath(".agents/registry.json")
PROVIDER_BASELINE_PATHS = {
    "claude": PurePosixPath(".claude/CLAUDE.md"),
    "codex": PurePosixPath(".codex/CODEX.md"),
}
PROVIDER_BASELINE_HEADING_ORDER = (
    "Purpose",
    "Loading Order",
    "Provider Metadata",
    "Canonical References",
    "Evidence Boundary",
)
PROVIDER_BASELINE_HEADINGS = frozenset(PROVIDER_BASELINE_HEADING_ORDER)
ROLE_ADAPTER_HEADING_ORDER = (
    "Runtime Bootstrap",
    "Role",
    "When to Use",
    "Inputs",
    "Outputs",
    "Guardrails",
    "Capability and Evidence",
    "Handoff / Escalation",
    "Postflight",
)
ROLE_ADAPTER_HEADINGS = ROLE_ADAPTER_HEADING_ORDER
SURFACE_BOOTSTRAP_UNITS = {
    "neutral": (
        "Load `.agents/registry.json` and this provider-neutral role projection before work.",
        "Follow the Stage 00 policy and handoff boundaries referenced by the registry.",
    ),
    "claude": (
        "Load `CLAUDE.md`, `.claude/CLAUDE.md`, and this agent's imported scope before work.",
        "Follow `docs/00.agent-governance/skills/work-lifecycle.md` for intake and completion.",
    ),
    "codex": (
        "Load `AGENTS.md`, `.codex/CODEX.md`, and this agent's imported scope before work.",
        "Follow `docs/00.agent-governance/skills/work-lifecycle.md` for intake and completion.",
    ),
}
CLAUDE_PERMISSION_TOOLS = {
    "read-only-evidence": {
        "default": "Read, Grep, Glob, Bash",
        "docs-researcher": "Read, Grep, Glob, WebFetch, WebSearch",
    },
    "scoped-authoring": {
        "default": "Read, Write, Edit, Grep, Glob, Bash",
    },
    "orchestration": {
        "default": "Read, Grep, Glob, Task",
    },
}
BASELINE_COMMON_REFERENCES = (
    "Common execution policy: `docs/00.agent-governance/policies/agent-execution.md`.",
    "Provider facts: `docs/00.agent-governance/providers/{provider}.md`.",
    "Role inventory and semantics: `.agents/registry.json` and `.agents/agents/`.",
    "Validation lanes and handoff: `docs/00.agent-governance/policies/quality.md`.",
    "Shell guidance: `RTK.md`.",
)
PROVIDER_BASELINE_PROFILES = {
    "claude": {
        "heading": "Local Runtime Baseline (Claude)",
        "Purpose": (
            "Thin baseline for the tracked Claude-native surface. Shared policy and responsibility remain in Stage 00.",
        ),
        "Loading Order": (
            "Load root `CLAUDE.md`, then `docs/00.agent-governance/skills/work-lifecycle.md`, the Claude provider note, and the relevant responsibility and active Task.",
        ),
        "Provider Metadata": (
            "Native role projections: `.claude/agents/*.md`, with native model and least-privilege tool metadata.",
            "Native permission and event declarations: `.claude/settings.json`.",
            "Shared skill view: `.claude/skills` points to `.agents/skills`.",
        ),
        "Evidence Boundary": (
            "Tracked projections and settings prove repository configuration only, not native discovery, hook delivery, authentication, model resolution, permission enforcement, or execution.",
        ),
    },
    "codex": {
        "heading": "Local Runtime Baseline (Codex)",
        "Purpose": (
            "Thin baseline for the tracked Codex-native surface. Shared policy and responsibility remain in Stage 00.",
        ),
        "Loading Order": (
            "Load root `AGENTS.md`, then `docs/00.agent-governance/skills/work-lifecycle.md`, the Codex provider note, and the relevant responsibility and active Task.",
        ),
        "Provider Metadata": (
            "Native role projections: `.codex/agents/*.toml`, with native model and reasoning-effort metadata.",
            "Native sandbox and approval controls belong to the running client.",
            "Shared skill view: `.codex/skills` points to `.agents/skills`.",
            "Run explicit repository validation; custom hook graphs are not a supported Codex execution or permission surface.",
        ),
        "Evidence Boundary": (
            "Tracked projections prove repository configuration only, not native discovery, authentication, model resolution, sandbox or approval enforcement, event delivery, or execution.",
        ),
    },
}
MAX_ADAPTER_BYTES = 262_144
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


NEGATION_STATE_PATTERN = (
    "(?:" + "|".join(_phrase_pattern(state) for state in NEGATION_STATES) + ")"
)
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
BLOCKQUOTE_START = re.compile(r"^ {0,3}(?:(?:[-+*]|\d+[.)])\s+)?(?:>\s*)+")
MARKDOWN_UNIT_START = re.compile(r"^(?: {0,3})(?:#{1,6}\s|[-+*]\s|\d+[.)]\s|@import\b)")
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
LIST_INDENTED_CODE = re.compile(r"^ {0,3}(?:[-+*]|\d+[.)]) {4,}\S")


class UniqueKeySafeLoader(yaml.SafeLoader):
    """YAML SafeLoader that rejects duplicate mapping keys at every depth."""


def _construct_unique_mapping(
    loader: UniqueKeySafeLoader, node: MappingNode, deep: bool = False
) -> dict[Any, Any]:
    if not isinstance(node, MappingNode):
        raise ConstructorError(None, None, "expected a mapping node", node.start_mark)
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
    description: str
    provider_metadata: dict[str, Any]
    raw_body: str
    heading: str
    section_headings: tuple[str, ...]
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
                stat.S_ISREG(mode) if final_kind == "file" else stat.S_ISDIR(mode)
            )
            if not expected:
                fail(code, f"{raw}: expected a regular non-symlink {final_kind}")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(strict_root)
    except (OSError, ValueError) as exc:
        fail(code, f"{raw}: resolved path escapes the repository root: {exc}")
    return resolved


def select_current_harness(registry: dict[str, Any]) -> HarnessSelection:
    """Select role and projection semantics only from the terminal registry."""

    roles_raw = registry.get("roles")
    if not isinstance(roles_raw, list) or not roles_raw:
        fail("ROLE-IDS", "registry roles must be a non-empty list")
    role_ids = tuple(role.get("id") for role in roles_raw)
    if not all(isinstance(item, str) for item in role_ids):
        fail("ROLE-IDS", "registry role identities must be strings")

    surface_ids = ("neutral", "claude", "codex")
    locations = {
        "neutral": (PurePosixPath(".agents/agents"), ".md"),
        "claude": (PurePosixPath(".claude/agents"), ".md"),
        "codex": (PurePosixPath(".codex/agents"), ".toml"),
    }
    roles: dict[str, dict[str, Any]] = {}
    projection_paths: dict[tuple[str, str], PurePosixPath] = {}
    for role in roles_raw:
        role_id = role["id"]
        roles[role_id] = {
            "id": role_id,
            "purpose": role["responsibility"],
            "permissionClass": role["permission_class"],
            "capabilityTierRef": role["capability_tier_ref"],
            "handoffIds": copy.deepcopy(role["handoff_to"]),
        }
        projections = role.get("projections")
        if not isinstance(projections, dict) or tuple(projections) != surface_ids:
            fail("ROLE-INVENTORY", f"{role_id} projection keys differ")
        for surface in surface_ids:
            path = PurePosixPath(projections[surface])
            expected = locations[surface][0] / f"{role_id}{locations[surface][1]}"
            if path != expected:
                fail("ROLE-INVENTORY", f"{role_id}/{surface} path differs")
            projection_paths[(role_id, surface)] = path

    return HarnessSelection(
        role_ids=role_ids,
        surface_ids=surface_ids,
        roles=roles,
        locations=locations,
        projection_paths=projection_paths,
    )


def validate_contract(
    root: Path, raw_contract: dict[str, Any] | None = None
) -> HarnessSelection:
    terminal = load_terminal_validator()
    try:
        registry = (
            terminal.load_json(root, REGISTRY_PATH)
            if raw_contract is None
            else copy.deepcopy(raw_contract)
        )
        terminal.validate_registry(
            root,
            registry,
            check_files=raw_contract is None,
        )
    except terminal.HarnessError as exc:
        fail("ROLE-REGISTRY", f"{exc.code}: {exc.detail}")
    selection = select_current_harness(registry)
    for role_id in selection.role_ids:
        role = selection.roles[role_id]
        path, source = adapter_source(root, selection, "neutral", role_id)
        neutral = parse_adapter_text("neutral", path, source)
        role["_neutralUnits"] = copy.deepcopy(neutral.section_units)
        role["_neutralBody"] = neutral.raw_body
        tier = (
            f"Capability tier reference: {chr(96)}{role['capabilityTierRef']}{chr(96)}."
        )
        handoff = (
            "Registry handoff targets: "
            + ", ".join(f"{chr(96)}{item}{chr(96)}" for item in role["handoffIds"])
            + "."
        )
        for declaration, section, prefix, code in (
            (
                tier,
                "Capability and Evidence",
                "Capability tier reference:",
                "ROLE-REGISTRY-TIER",
            ),
            (
                handoff,
                "Handoff / Escalation",
                "Registry handoff targets:",
                "ROLE-REGISTRY-HANDOFF",
            ),
        ):
            declarations = re.findall(
                r"(?m)^[ \t]*(?:[-+*][ \t]+|\d+[.)][ \t]+)?"
                + re.escape(prefix)
                + r"[^\n]*",
                neutral.raw_body,
            )
            if (
                len(declarations) != 1
                or neutral.section_units.get(section, ()).count(declaration) != 1
            ):
                fail(
                    code,
                    "projection declaration must uniquely match registry in its section",
                )
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
    return metadata, body.removeprefix("\n")


def canonical_yaml_frontmatter(raw_frontmatter: str, path: str) -> str:
    if not raw_frontmatter or any(
        not line or line.startswith((" ", "\t", "#")) or ": " not in line
        for line in raw_frontmatter.splitlines()
    ):
        fail("ROLE-ADAPTER-BOUNDS", f"{path}: YAML metadata is not canonical")
    return raw_frontmatter


def canonical_codex_metadata(text: str, body: str, path: str) -> None:
    escaped_body = f'developer_instructions = """\n{body}"""'
    if text.count(escaped_body) != 1:
        fail("ROLE-ADAPTER-BOUNDS", f"{path}: Codex body boundary differs")
    metadata = text.replace(escaped_body, "", 1)
    metadata_lines = [line for line in metadata.splitlines() if line]
    if any(
        line.startswith((" ", "\t", "#"))
        or not re.fullmatch(r"[a-z_]+ = \"[^\n\"]*\"", line)
        for line in metadata_lines
    ):
        fail("ROLE-ADAPTER-BOUNDS", f"{path}: Codex metadata is not canonical")


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
        return re.sub(r"^(?:#{1,6}\s+|[-+*]\s+|\d+[.)]\s+)", "", raw_unit)

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


def extract_section_headings(body: str) -> tuple[str, ...]:
    return tuple(re.findall(r"(?m)^## ([^\n]+?)\s*$", body))


def parse_adapter_text(
    surface: str,
    relative_path: PurePosixPath,
    text: str,
) -> Adapter:
    suffix = relative_path.suffix
    if suffix == ".md":
        metadata, body = parse_frontmatter(text, relative_path.as_posix())
        frontmatter_end = text.find("\n---\n", 4)
        canonical_yaml_frontmatter(text[4:frontmatter_end], relative_path.as_posix())
        declared_name = metadata["name"]
        description = metadata.get("description")
        expected_metadata_keys = {
            "neutral": ("name", "description"),
            "claude": ("name", "description", "model", "tools"),
        }
        if tuple(metadata) != expected_metadata_keys.get(surface, ()):
            fail(
                "ROLE-ADAPTER-BOUNDS",
                f"{relative_path}: metadata keys or order differ",
            )
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
        description = data.get("description")
        if not isinstance(declared_name, str):
            fail("ROLE-ADAPTER-PARSE", f"{relative_path}: name must be a string")
        if tuple(data) != (
            "description",
            "developer_instructions",
            "name",
            "model",
            "model_reasoning_effort",
        ):
            fail(
                "ROLE-ADAPTER-BOUNDS",
                f"{relative_path}: Codex metadata keys or order differ",
            )
        body = body_value
        canonical_codex_metadata(text, body, relative_path.as_posix())

    operative_body = operative_markdown(body, relative_path.as_posix())
    return Adapter(
        surface=surface,
        path=relative_path.as_posix(),
        path_stem=relative_path.stem,
        declared_name=declared_name,
        raw_body=body.rstrip("\n") + "\n",
        description=description if isinstance(description, str) else "",
        provider_metadata=copy.deepcopy(metadata if suffix == ".md" else data),
        heading=extract_heading(operative_body),
        section_headings=extract_section_headings(operative_body),
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
        path = safe_repo_path(
            root,
            relative_path,
            final_kind="file",
            code="ROLE-ADAPTER-PARSE",
        )
        descriptor = os.open(
            path,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode):
                fail(
                    "ROLE-ADAPTER-PARSE",
                    f"{relative_path}: expected a regular file",
                )
            if metadata.st_size > MAX_ADAPTER_BYTES:
                fail(
                    "ROLE-ADAPTER-PARSE",
                    f"{relative_path}: input exceeds {MAX_ADAPTER_BYTES} bytes",
                )
            payload = os.read(descriptor, MAX_ADAPTER_BYTES + 1)
            if len(payload) > MAX_ADAPTER_BYTES:
                fail(
                    "ROLE-ADAPTER-PARSE",
                    f"{relative_path}: input exceeds {MAX_ADAPTER_BYTES} bytes",
                )
            text = payload.decode("utf-8")
        finally:
            os.close(descriptor)
    except (OSError, UnicodeError) as exc:
        fail("ROLE-ADAPTER-PARSE", f"{relative_path}: {exc}")
    return relative_path, text


def expected_adapter_section_units(
    role: dict[str, Any], surface: str
) -> dict[str, tuple[str, ...]]:
    """Project provider bootstrap onto registry-selected neutral semantics."""

    neutral_units = role.get("_neutralUnits")
    if not isinstance(neutral_units, dict):
        fail("ROLE-ADAPTER-BOUNDS", f"{role['id']} neutral projection is missing")
    units = copy.deepcopy(neutral_units)
    if surface == "neutral":
        return units
    neutral_bootstrap = units.get("Runtime Bootstrap", ())
    imports = tuple(unit for unit in neutral_bootstrap if unit.startswith("@import "))
    try:
        units["Runtime Bootstrap"] = SURFACE_BOOTSTRAP_UNITS[surface] + imports
    except KeyError as exc:
        fail("ROLE-ADAPTER-BOUNDS", f"unknown projection surface: {exc}")
    return units


def render_adapter_body(role: dict[str, Any], surface: str) -> str:
    units = expected_adapter_section_units(role, surface)
    paragraph_sections = {"Role", "When to Use", "Postflight"}
    lines = [f"# {role['id']}", ""]
    for heading in ROLE_ADAPTER_HEADING_ORDER:
        lines.extend((f"## {heading}", ""))
        for unit in units[heading]:
            lines.append(
                unit
                if unit.startswith("@import ") or heading in paragraph_sections
                else f"- {unit}"
            )
            if unit.startswith(
                "Follow `docs/00.agent-governance/skills/work-lifecycle.md`"
            ):
                lines.append("")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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

    expected_description = f"{role['purpose']}"
    if adapter.description != expected_description:
        diagnostics.append(
            Diagnostic(
                "ROLE-ADAPTER-BOUNDS",
                adapter.path,
                role_id,
                "description must equal the canonical role purpose",
            )
        )

    if adapter.surface == "claude":
        permission_class = role["permissionClass"]
        tool_profiles = CLAUDE_PERMISSION_TOOLS.get(permission_class, {})
        expected_tools = tool_profiles.get(
            role_id,
            tool_profiles.get("default"),
        )
        if adapter.provider_metadata.get("tools") != expected_tools:
            diagnostics.append(
                Diagnostic(
                    "ROLE-ADAPTER-BOUNDS",
                    adapter.path,
                    role_id,
                    "Claude tools exceed or differ from the permission-class projection",
                )
            )

    expected_units = expected_adapter_section_units(role, adapter.surface)
    expected_body = render_adapter_body(role, adapter.surface)
    if (
        adapter.raw_body != expected_body
        or adapter.section_headings != ROLE_ADAPTER_HEADING_ORDER
        or adapter.section_units != expected_units
    ):
        diagnostics.append(
            Diagnostic(
                "ROLE-ADAPTER-BOUNDS",
                adapter.path,
                role_id,
                "operative H2 sections must equal the closed role adapter set",
            )
        )

    return diagnostics


def validate_provider_baseline_text(
    surface: str,
    relative_path: PurePosixPath,
    source: str,
) -> list[str]:
    if surface not in PROVIDER_BASELINE_PATHS:
        return ["PROVIDER-BASELINE-BOUNDS"]
    operative = operative_markdown(source, relative_path.as_posix())
    headings = extract_section_headings(operative)
    profile = PROVIDER_BASELINE_PROFILES[surface]
    provider = surface
    expected_units = {
        heading: (
            tuple(unit.format(provider=provider) for unit in BASELINE_COMMON_REFERENCES)
            if heading == "Canonical References"
            else profile[heading]
        )
        for heading in PROVIDER_BASELINE_HEADING_ORDER
    }
    if (
        operative != source.rstrip("\n")
        or extract_heading(operative) != profile["heading"]
        or headings != PROVIDER_BASELINE_HEADING_ORDER
        or extract_section_units(operative) != expected_units
    ):
        return ["PROVIDER-BASELINE-BOUNDS"]
    return []


def validate_provider_baselines(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for surface, relative in PROVIDER_BASELINE_PATHS.items():
        try:
            source = safe_repo_path(
                root, relative, final_kind="file", code="PROVIDER-BASELINE-PARSE"
            ).read_text(encoding="utf-8")
        except OSError as exc:
            fail("PROVIDER-BASELINE-PARSE", f"{relative}: {exc}")
        for code in validate_provider_baseline_text(surface, relative, source):
            diagnostics.append(
                Diagnostic(code, relative.as_posix(), surface, "baseline is unbounded")
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
    ] + validate_provider_baselines(root)


def validate_mutated_source(
    surface: str,
    path: PurePosixPath,
    source: str,
    role: dict[str, Any],
) -> list[str]:
    """Return stable diagnostics for one in-memory projection mutation."""

    try:
        adapter = parse_adapter_text(surface, path, source)
    except ContractError as exc:
        return [exc.code]
    return [diagnostic.code for diagnostic in validate_adapter(role, adapter)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.absolute()
    try:
        selection = validate_contract(root)
        diagnostics = validate_repository(root)
        if diagnostics:
            for diagnostic in diagnostics:
                print(diagnostic.render(), file=sys.stderr)
            return 1
        print(
            "[PASS] agent harness semantics validation passed: "
            f"roles={len(selection.role_ids)} "
            f"adapters={len(selection.projection_paths)} "
            f"surfaces={len(selection.surface_ids)}"
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
