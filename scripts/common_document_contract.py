"""Project a common document shell to its role body or native payload."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path

from semver_grammar import is_numeric_version
from validation.repository.bounded_io import read_text


CONTRACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs/99.templates/01.contracts/common-document-contract.json"
)
NATIVE_OPEN = "~~~~~~~native-payload"
NATIVE_CLOSE = "~~~~~~~"
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
_FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})([^\r\n]*)$")
_RAW_TAG = re.compile(r"^ {0,3}<(pre|script|style|textarea)(?:\s|>)", re.IGNORECASE)
NATIVE_PROFILES = frozenset(
    {
        "common/folder-agents-guide",
        "common/native-skill-package",
        "common/provider-native-metadata",
        "common/provider-native-command",
        "common/template-agents-guide",
        "common/template-native-skill",
        "common/template-exception-provider-native-metadata",
        "common/template-exception-provider-native-command",
    }
)
SCOPE_LAYERS = frozenset(
    {"workspace", "product", "agent", "provider", "template", "reference"}
)
KNOWN_STATUSES = frozenset(
    {
        "draft",
        "in-review",
        "proposed",
        "active",
        "deprecated",
        "approved",
        "accepted",
        "published",
        "superseded",
        "retired",
        "rejected",
        "cancelled",
        "ready",
        "in-progress",
        "blocked",
        "completed",
        "detected",
        "investigating",
        "mitigated",
        "resolved",
    }
)


class CommonDocumentError(ValueError):
    """A common document cannot be projected without ambiguity."""


def _core_contract() -> Mapping[str, object]:
    """Read the local contract with bounded, stable, strict UTF-8 input."""

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate common contract key {key}")
            value[key] = item
        return value

    try:
        value = json.loads(
            read_text(CONTRACT_PATH, max_bytes=1024 * 1024),
            object_pairs_hook=unique_object,
        )
    except (OSError, UnicodeError, ValueError) as exc:
        raise CommonDocumentError(f"common contract unavailable: {exc}") from exc
    if not isinstance(value, Mapping):
        raise CommonDocumentError("common contract must be an object")
    return value


def _raw_closer(line: str) -> re.Pattern[str] | None:
    stripped = line.lstrip(" ")
    tag = _RAW_TAG.match(line)
    if tag is not None:
        return re.compile(rf"</{tag.group(1)}\s*>", re.IGNORECASE)
    for opener, closer in (("<!--", "-->"), ("<![CDATA[", "]]>"), ("<?", "?>")):
        if stripped.startswith(opener):
            return re.compile(re.escape(closer))
    return None


def _headings() -> tuple[tuple[str, tuple[str, ...]], ...]:
    try:
        contract = _core_contract()
        result = tuple(
            (name, tuple(children)) for name, children in contract["headings"].items()
        )
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        raise CommonDocumentError(f"common headings unavailable: {exc}") from exc
    if len(result) != 4 or any(len(children) != 2 for _, children in result):
        raise CommonDocumentError("common headings have invalid cardinality")
    return result


def section_rules() -> dict[str, str]:
    """Return the shared purpose and limit of each common H3, in shell order."""
    order = [child for _, children in _headings() for child in children]
    try:
        rules = _core_contract()["section_rules"]
        if (
            not isinstance(rules, Mapping)
            or list(rules) != order
            or not all(
                isinstance(rule, str) and rule.strip() for rule in rules.values()
            )
        ):
            raise ValueError("section rules must cover each common H3 once, in order")
    except (KeyError, ValueError) as exc:
        raise CommonDocumentError(f"common section rules unavailable: {exc}") from exc
    return dict(rules)


def _semantic_headings(text: str) -> list[tuple[int, str, int, int]]:
    """Return ATX headings outside fenced code, with character offsets."""

    result: list[tuple[int, str, int, int]] = []
    fence_char, fence_width = "", 0
    raw_end: re.Pattern[str] | None = None
    offset = 0
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        if raw_end is not None:
            if raw_end.search(stripped):
                raw_end = None
            offset += len(line)
            continue
        if not fence_char and (closer := _raw_closer(stripped)) is not None:
            raw_end = None if closer.search(stripped) else closer
            offset += len(line)
            continue
        fence = _FENCE.fullmatch(stripped)
        if fence:
            token = fence.group(1)
            if not fence_char:
                fence_char, fence_width = token[0], len(token)
            elif (
                token[0] == fence_char
                and len(token) >= fence_width
                and not fence.group(2).strip()
            ):
                fence_char, fence_width = "", 0
        elif not fence_char:
            match = _HEADING.fullmatch(stripped)
            if match:
                result.append(
                    (len(match.group(1)), match.group(2), offset, offset + len(line))
                )
        offset += len(line)
    if fence_char:
        raise CommonDocumentError("unclosed Markdown fence in common document")
    return result


def has_common_envelope(text: str) -> bool:
    """Detect a partial shell so its caller can route it to strict checks."""

    names = {name for name, _ in _headings()}
    try:
        return any(
            depth == 2 and name in names
            for depth, name, _, _ in _semantic_headings(text)
        )
    except CommonDocumentError:
        return any(f"## {name}" in text for name in names)


def _payload_bounds(text: str) -> tuple[int, int, int]:
    headings = _semantic_headings(text)
    expected = _headings()
    top = [(name, start) for depth, name, start, _ in headings if depth == 2]
    if [name for name, _ in top] != [name for name, _ in expected]:
        raise CommonDocumentError(
            "common H2 sections are missing, duplicated, or reordered"
        )
    children = [
        (name, start, end) for depth, name, start, end in headings if depth == 3
    ]
    if [name for name, _, _ in children] != [
        name for _, group in expected for name in group
    ]:
        raise CommonDocumentError(
            "common H3 sections are missing, duplicated, or reordered"
        )
    for index, (_, expected_children) in enumerate(expected):
        first = top[index][1]
        next_h2 = top[index + 1][1] if index + 1 < len(top) else len(text)
        actual_children = [
            name for name, start, _ in children if first < start < next_h2
        ]
        if actual_children != list(expected_children):
            raise CommonDocumentError("common H3 section is under the wrong H2 parent")
    payload_start = next(end for name, _, end in children if name == "본문과 규칙")
    payload_end = next(start for name, start in top if name == "적용과 확인")
    prefix_end = top[0][1]
    if not prefix_end or payload_start >= payload_end:
        raise CommonDocumentError("common document has no distinct role payload")
    return prefix_end, payload_start, payload_end


def _native_payload(payload: str) -> str:
    lines = payload.splitlines(keepends=True)
    openings = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == NATIVE_OPEN]
    closings = [
        i for i, line in enumerate(lines) if line.rstrip("\r\n") == NATIVE_CLOSE
    ]
    if len(openings) != 1 or len(closings) != 1 or closings[0] <= openings[0]:
        raise CommonDocumentError(
            "native payload needs exactly one closed 7-tilde fence"
        )
    guidance = re.compile(r"<!-- 작성 규칙: [^\r\n]* -->")
    outside = lines[: openings[0]] + lines[closings[0] + 1 :]
    if any(line.strip() and not guidance.fullmatch(line.strip()) for line in outside):
        raise CommonDocumentError("native fence has extra role content")
    return "".join(lines[openings[0] + 1 : closings[0]])


def _visible_lines(text: str) -> list[str]:
    """Return lines outside Markdown fences; relation rows are rendered prose."""

    result: list[str] = []
    fence_char, fence_width = "", 0
    raw_end: re.Pattern[str] | None = None
    for line in text.splitlines():
        if raw_end is not None:
            if raw_end.search(line):
                raw_end = None
            continue
        if not fence_char and (closer := _raw_closer(line)) is not None:
            raw_end = None if closer.search(line) else closer
            continue
        fence = _FENCE.fullmatch(line)
        if fence:
            token = fence.group(1)
            if not fence_char:
                fence_char, fence_width = token[0], len(token)
            elif (
                token[0] == fence_char
                and len(token) >= fence_width
                and not fence.group(2).strip()
            ):
                fence_char, fence_width = "", 0
        elif not fence_char:
            result.append(line)
    return result


def relation_rows(text: str) -> tuple[tuple[str, str], ...]:
    """Read optional typed links from the common Related Documents section.

    An untyped Markdown link remains navigation. The second tuple value is the
    link destination; callers still resolve it against the document path.
    """

    if not isinstance(text, str):
        raise CommonDocumentError("relation source must be Markdown text")
    _payload_bounds(text)
    headings = _semantic_headings(text)
    related_start = next(
        end for depth, name, _, end in headings if depth == 3 and name == "관련 문서"
    )
    sources_start = next(
        start
        for depth, name, start, _ in headings
        if depth == 3 and name == "외부 근거"
    )
    lines = _visible_lines(text[related_start:sources_start])
    header = "| Relation | Target |"
    locations = [i for i, line in enumerate(lines) if line.strip() == header]
    if not locations:
        return ()
    if len(locations) != 1:
        raise CommonDocumentError("one typed relation table is allowed")
    start = locations[0]
    if start + 1 >= len(lines) or not re.fullmatch(
        r"\|\s*:?-{3,}:?\s*\|\s*:?-{3,}:?\s*\|", lines[start + 1].strip()
    ):
        raise CommonDocumentError("typed relation table needs its two-column separator")
    try:
        kinds = frozenset(_core_contract()["relation_kinds"])
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        raise CommonDocumentError(f"relation kinds unavailable: {exc}") from exc
    rows: list[tuple[str, str]] = []
    for line in lines[start + 2 :]:
        if not line.lstrip().startswith("|"):
            if line.strip():
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] not in kinds:
            raise CommonDocumentError(
                "typed relation row has an unknown kind or column"
            )
        match = re.fullmatch(r"\[[^\]\n]+\]\(([^()\s]+)\)", cells[1])
        if match is None:
            raise CommonDocumentError("typed relation target must be one Markdown link")
        rows.append((cells[0], match.group(1)))
    return tuple(rows)


def metadata_projection(
    frontmatter: Mapping[str, object],
    *,
    profile_id: str,
    binding: Mapping[str, object] | object,
    scope_subject: str,
    scope_layer: str,
    document_lifecycle: str | None = None,
    adoption_verified: bool = False,
) -> dict[str, object]:
    """Project one existing source without treating execution as adoption.

    A caller names the subject and layer because `type`, `status`, and the
    legacy ADR `layer: architecture` cannot establish scope by themselves.
    The source frontmatter remains the single stored owner of its values.
    """

    if not isinstance(frontmatter, Mapping) or not isinstance(profile_id, str):
        raise CommonDocumentError("metadata needs a source mapping and profile ID")
    kinds = (
        binding.get("profile_kinds")
        if isinstance(binding, Mapping)
        else getattr(binding, "profile_kinds", None)
    )
    if not isinstance(kinds, Mapping) or profile_id not in kinds:
        raise CommonDocumentError(f"no common kind mapping for {profile_id}")
    try:
        canonical = _core_contract()
        allowed_kinds = canonical["payload_profiles"]
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        raise CommonDocumentError(f"common kinds unavailable: {exc}") from exc
    kind = kinds[profile_id]
    if not isinstance(kind, str) or kind not in allowed_kinds:
        raise CommonDocumentError(f"unknown common kind {kind!r}")
    for field in ("title", "version", "owner"):
        if (
            not isinstance(frontmatter.get(field), str)
            or not frontmatter[field].strip()
        ):
            raise CommonDocumentError(f"{field} needs a nonempty source value")
    if not is_numeric_version(frontmatter["version"]):
        raise CommonDocumentError("version needs an exact numeric X.X.X value")
    stored_type = frontmatter.get("type")
    if stored_type != profile_id and not (
        profile_id.startswith("common/readme-") and stored_type == "common/readme"
    ):
        raise CommonDocumentError("source type does not match the mapped profile")
    status = frontmatter.get("status")
    if not (isinstance(status, str) and status in KNOWN_STATUSES) and not (
        profile_id == "sdlc/task" and status is None
    ):
        raise CommonDocumentError(f"unknown source status {status!r}")
    if (
        not isinstance(scope_subject, str)
        or not scope_subject.strip()
        or scope_layer not in SCOPE_LAYERS
    ):
        raise CommonDocumentError("scope needs an explicit subject and canonical layer")
    if document_lifecycle is not None and not isinstance(document_lifecycle, str):
        raise CommonDocumentError("document lifecycle must be a canonical string")
    lifecycle = document_lifecycle or (
        "deprecated" if status == "deprecated" else "draft"
    )
    if lifecycle not in {"draft", "active", "deprecated"}:
        raise CommonDocumentError(f"unknown document lifecycle {lifecycle!r}")
    if lifecycle == "active" and not adoption_verified:
        raise CommonDocumentError("active lifecycle needs verified adoption context")
    return {
        "title": frontmatter["title"],
        "version": frontmatter["version"],
        "kind": kind,
        "owner": frontmatter["owner"],
        "lifecycle": lifecycle,
        "scope": {"subject": scope_subject, "layer": scope_layer},
    }


def payload_markdown(text: str, *, profile_id: str) -> str:
    """Preserve authored metadata/H1 and project H4..H6, or return native bytes."""

    if not isinstance(text, str) or not isinstance(profile_id, str) or not profile_id:
        raise CommonDocumentError("text and profile_id are required")
    prefix_end, start, end = _payload_bounds(text)
    payload = text[start:end]
    if profile_id in NATIVE_PROFILES:
        return _native_payload(payload)
    if NATIVE_OPEN in payload or NATIVE_CLOSE in payload:
        raise CommonDocumentError("native fence is not allowed for authored payload")
    headings = [item for item in _semantic_headings(payload) if 4 <= item[0] <= 6]
    projected = payload
    for depth, _, offset, _ in reversed(headings):
        projected = projected[:offset] + "#" * (depth - 2) + projected[offset + depth :]
    return text[:prefix_end] + projected
