#!/usr/bin/env python3
"""Own the ADR-0038 six-disposition Stage 98 contract the validators share.

ADR-0040 adds the current judgment of a retained unit, read from the Archive
index's Retention Assessment table beside the catalog.

Content frozen under ADR-0032 keeps its generation and its existing owners.
This module answers only what the current generation asks: which retention
class a path belongs to, which classes a current document may cite, and what
the Stage 98 catalog's one Retention Envelope names. It holds no second
recovery ledger; Git history recovers the object the envelope names.
"""

from __future__ import annotations

import datetime
import importlib
import json
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import TYPE_CHECKING, Callable, Mapping, Sequence

import yaml

if TYPE_CHECKING:
    from document_contracts import (
        ArchiveAssessment,
        CitationRule,
        Registry,
        RetentionClass,
        RetentionMode,
        RetentionUnit,
    )


def contracts_module() -> ModuleType:
    """Load the registry owner on first use.

    `document_contracts` imports its siblings as top-level modules, so a caller
    imported as `scripts.<module>` from the repository root cannot import it
    eagerly. Loading it when a registry question is first asked keeps those
    import-only callers importable."""

    loaded = sys.modules.get("document_contracts")
    if loaded is not None:
        return loaded
    scripts = str(Path(__file__).resolve().parent)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    return importlib.import_module("document_contracts")


def classify_path(registry: "Registry", path: PurePosixPath):
    return contracts_module().classify_path(registry, path)


def _is_contract_error(error: Exception) -> bool:
    return isinstance(error, contracts_module().DocumentContractError)


ARCHIVE_ROOT = PurePosixPath("docs/98.archive")
ARCHIVE_INDEX = ARCHIVE_ROOT / "README.md"
CATALOG_HEADER = "| Disposition Record | Retention Envelope |"
CATALOG_SEPARATOR = "| --- | --- |"
ROUTE_DISPOSITION_PROFILES = frozenset(
    {"archive/route-tombstone", "archive/scope-migration"}
)
# A route record names where something went and holds no evidence body; the
# frozen migration ledger is read as one for citation.
ROUTE_RECORD_PROFILES = ROUTE_DISPOSITION_PROFILES | {"archive/migration"}
SEALED_RECORD_PROFILES = frozenset({"archive/tombstone"})

# Accepts both object-format lengths ADR-0040 requires: sha1 (40) and sha256
# (64), matching the lifecycle gate's and recovery module's own grammar.
_COMMIT = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
_CATALOG_ROW = re.compile(
    r"\| \[`(?P<label>[^`|]+)`\]\(\./(?P<target>[^)|]+)\) \| `(?P<envelope>[^`|]+)` \|"
)


class DispositionError(ValueError):
    """A Stage 98 disposition input that cannot be read under ADR-0038."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(code)
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class RetentionEnvelope:
    """The one Git object a disposition names: `<commit>:<original path>`."""

    commit: str
    original_path: PurePosixPath


@dataclass(frozen=True)
class CatalogRow:
    record_path: PurePosixPath
    envelope: RetentionEnvelope


def _canonical_repository_path(value: str) -> PurePosixPath | None:
    if (
        not value
        or value.startswith("/")
        or ":" in value
        or any(character.isspace() for character in value)
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        return None
    return PurePosixPath(value)


def parse_retention_envelope(value: str) -> RetentionEnvelope:
    """Read exactly one full commit and one canonical repository path."""

    commit, separator, original = value.partition(":")
    path = _canonical_repository_path(original) if separator else None
    if _COMMIT.fullmatch(commit) is None or path is None:
        raise DispositionError(
            "ARCHIVE-CATALOG-ENVELOPE",
            "a Retention Envelope names one <commit>:<original path>",
        )
    return RetentionEnvelope(commit=commit, original_path=path)


_INLINE_LINK = re.compile(r'(\]\()(<[^>\n]+>|[^)\s]+)((?:\s+"[^"\n]*")?\))')
_REFERENCE_LINK = re.compile(r"^( {0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]+>|\S+)", re.M)
_URI_SCHEME = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:")


def _relative_link(target: str) -> tuple[str, str, bool] | None:
    """Split a relative Markdown link target into path, fragment, and bracket form."""

    bracketed = target.startswith("<") and target.endswith(">")
    bare = target[1:-1] if bracketed else target
    if not bare or bare.startswith(("#", "/")) or _URI_SCHEME.match(bare):
        return None
    path, separator, fragment = bare.partition("#")
    if not path:
        return None
    return path, separator + fragment, bracketed


def _rewrite_links(text: str, rewrite) -> str:
    def inline(match: re.Match[str]) -> str:
        replaced = rewrite(match.group(2))
        return (
            match.group(0)
            if replaced is None
            else match.group(1) + replaced + match.group(3)
        )

    def reference(match: re.Match[str]) -> str:
        replaced = rewrite(match.group(2))
        return match.group(0) if replaced is None else match.group(1) + replaced

    return _REFERENCE_LINK.sub(reference, _INLINE_LINK.sub(inline, text))


def _resolve_link(document: PurePosixPath, path: str) -> PurePosixPath:
    return PurePosixPath(
        posixpath.normpath(posixpath.join(document.parent.as_posix(), path))
    )


def link_resolved_text(
    text: str,
    document: PurePosixPath,
    moves: Mapping[PurePosixPath, PurePosixPath] | None = None,
) -> str:
    """Replace each relative link with the repository path it names.

    Two copies of a document name the same targets exactly when their resolved
    texts are equal. `moves` maps a target that moves in the same change to its
    new path, so a link between documents moving together still matches."""

    moved = moves or {}

    def rewrite(target: str) -> str | None:
        relative = _relative_link(target)
        if relative is None:
            return None
        path, fragment, _bracketed = relative
        resolved = _resolve_link(document, path)
        return f"<@{moved.get(resolved, resolved).as_posix()}{fragment}>"

    return _rewrite_links(text, rewrite)


def rebase_relative_links(
    text: str,
    source: PurePosixPath,
    target: PurePosixPath,
    moves: Mapping[PurePosixPath, PurePosixPath] | None = None,
) -> str:
    """Rewrite a moved document's relative links to name the same targets.

    Only a link whose resolved target would change is rewritten, so the result
    differs from the source by relative link prefixes alone."""

    moved = moves or {}

    def rewrite(link: str) -> str | None:
        relative = _relative_link(link)
        if relative is None:
            return None
        path, fragment, bracketed = relative
        resolved = _resolve_link(source, path)
        destination = moved.get(resolved, resolved)
        if destination == _resolve_link(target, path):
            return None
        rebased = posixpath.relpath(destination.as_posix(), target.parent.as_posix())
        rebased += fragment
        return f"<{rebased}>" if bracketed else rebased

    return _rewrite_links(text, rewrite)


def canonical_repository_path(value: object) -> PurePosixPath | None:
    """Return a canonical repository-relative path, or None for anything else."""

    return _canonical_repository_path(value) if isinstance(value, str) else None


def frontmatter_mapping(text: str) -> Mapping[str, object]:
    """Read a route disposition's YAML frontmatter; malformed input names nothing."""

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


def retention_classes_by_name(registry: "Registry") -> Mapping[str, "RetentionClass"]:
    return {item.name: item for item in registry.retention_classes}


def retention_mode_of(registry: "Registry", profile_id: str) -> "RetentionMode | None":
    """Return the one retention mode the registry binds to a profile, if any."""

    for mode in registry.retention_modes:
        if mode.profile_id_pattern.search(profile_id):
            return mode
    return None


@dataclass(frozen=True)
class CitationDecision:
    """What the citation table decided and which rule decided it.

    `rule` is the 1-based position of the deciding rule, or None when no rule
    matched and the table's default decided."""

    admitted: bool
    rule: int | None


def archive_target_kind(
    registry: "Registry", target: PurePosixPath
) -> tuple[str, str | None] | None:
    """Classify a Stage 98 link target by its registry profile.

    Returns the target kind the citation table names and, for a retained body,
    its class. A target outside Stage 98 has no kind. The directory name alone
    never decides: a frozen record is a record wherever it sits."""

    if target.parts[:2] != ARCHIVE_ROOT.parts:
        return None
    table = registry.archive_citation
    if target in (
        (table.index, table.ledger) if table is not None else (ARCHIVE_INDEX,)
    ):
        return ("index", None)
    retention = retention_class_of(registry, target)
    if retention is not None:
        return ("retained-body", retention.name)
    try:
        profile_id = classify_path(registry, target).profile_id
    except Exception as error:  # noqa: BLE001 - only the registry's own error means unrouted
        if _is_contract_error(error):
            return ("unclassified", None)
        raise
    if profile_id in ROUTE_RECORD_PROFILES:
        return ("route-record", None)
    if profile_id in SEALED_RECORD_PROFILES:
        return ("sealed-record", None)
    return ("unclassified", None)


def _rule_matches(
    rule: "CitationRule",
    source: PurePosixPath,
    source_profile_id: str,
    target_kind: str,
    target_class: str | None,
    target_judgment: tuple[str, str] | None = None,
) -> bool:
    """Report whether one citation-table rule applies to this source and target.

    `rule.source` is "archive" (the source sits under Stage 98), "profiles" (the
    source profile is in `rule.source_profile_ids`), or "any". `rule.target` is
    "any" or one kind from `archive_target_kind`; a "retained-body" rule also
    names the classes it covers in `rule.target_classes`.
    """

    if rule.source == "archive":
        source_matches = source.parts[:2] == ARCHIVE_ROOT.parts
    elif rule.source == "profiles":
        source_matches = source_profile_id in rule.source_profile_ids
    else:
        source_matches = True
    if not source_matches:
        return False
    if rule.target == "any":
        return True
    if rule.target != target_kind:
        return False
    if rule.target != "retained-body":
        return True
    # A retained-body rule that does not cover this class passes to the next rule.
    if target_class not in rule.target_classes:
        return False
    # An assessment or availability condition narrows the rule to units judged so.
    assessment, availability = target_judgment or ("", "")
    if rule.target_assessments and assessment not in rule.target_assessments:
        return False
    return not rule.target_availabilities or availability in rule.target_availabilities


def citation_decision(
    registry: "Registry",
    source: PurePosixPath,
    source_profile_id: str,
    target: PurePosixPath,
    *,
    assessments: Mapping[PurePosixPath, "AssessmentRow"] | None = None,
) -> CitationDecision | None:
    """Decide a citation into Stage 98 from the registry's ordered table.

    The first matching rule decides; with no match the table's default does.
    `assessments` is the parsed Retention Assessment table; a unit it does not
    name carries the registry defaults. A target outside Stage 98 is not a
    citation decision and returns None."""

    kind = archive_target_kind(registry, target)
    if kind is None:
        return None
    table = registry.archive_citation
    if table is None:
        raise DispositionError(
            "ARCHIVE-CITATION-TABLE", "the registry declares no archive citation table"
        )
    target_kind, target_class = kind
    judgment = (
        assessment_of(registry, assessments or {}, target)
        if target_kind == "retained-body"
        else None
    )
    for position, rule in enumerate(table.rules, start=1):
        if _rule_matches(
            rule, source, source_profile_id, target_kind, target_class, judgment
        ):
            return CitationDecision(admitted=rule.decision == "admit", rule=position)
    return CitationDecision(admitted=table.default == "admit", rule=None)


def retention_class_of(
    registry: "Registry", path: PurePosixPath
) -> "RetentionClass | None":
    """Return the class of a retained body; frozen records and routes have none.

    A frozen ADR-0032 record may share `superseded/` with retained bodies, so
    the class is read from the path only after the registry has classified the
    path to a governed profile rather than to the frozen record generation.
    """

    parts = path.parts
    if len(parts) < 4 or parts[:2] != ARCHIVE_ROOT.parts:
        return None
    retention = retention_classes_by_name(registry).get(parts[2])
    if retention is None:
        return None
    try:
        profile = classify_path(registry, path)
    except Exception as error:  # noqa: BLE001 - only the registry's own error means unrouted
        if _is_contract_error(error):
            return None
        raise
    if profile.profile_class == "archive":
        return None
    return retention


def retention_source_path(path: PurePosixPath) -> PurePosixPath:
    """Return the active-stage path a retained body mirrors."""

    return PurePosixPath("docs", *path.parts[3:])


def retained_body_path(source: PurePosixPath, class_name: str) -> PurePosixPath:
    """Return `docs/98.archive/<class>/<the document's own stage path>`."""

    return ARCHIVE_ROOT.joinpath(class_name, *source.parts[1:])


def enclosing_unit(
    registry: "Registry", source: PurePosixPath
) -> tuple["RetentionUnit", PurePosixPath] | None:
    """Return the retention unit whose root holds an active-stage document."""

    for parent in source.parents:
        for unit in registry.retention_units:
            if unit.root.fullmatch(parent.as_posix()):
                return unit, parent
    return None


def retained_unit_of(
    registry: "Registry", record: PurePosixPath
) -> tuple["RetentionUnit", "RetentionClass"] | None:
    """Return the unit and class when a catalog record names a retained unit root."""

    parts = record.parts
    if len(parts) < 4 or parts[:2] != ARCHIVE_ROOT.parts:
        return None
    retention = retention_classes_by_name(registry).get(parts[2])
    if retention is None:
        return None
    source = retention_source_path(record).as_posix()
    for unit in registry.retention_units:
        if unit.root.fullmatch(source):
            return unit, retention
    return None


def archive_ledger_path(registry: "Registry | None") -> PurePosixPath:
    """Return the file that holds the archive tables (ADR-0047).

    A registry that declares no ledger keeps its tables in the index itself."""

    table = getattr(registry, "archive_citation", None)
    return table.ledger if table is not None else ARCHIVE_INDEX


_LEDGER_PATH = re.compile(r"docs/98\.archive/(?:README|[a-z0-9-]+)\.md")


def archive_ledger_path_at(root: Path) -> PurePosixPath:
    """Return the ledger path from the registry file without loading profiles.

    For readers that hold no typed registry. A missing, unreadable, or
    malformed value keeps the tables in the index, as a registry without a
    ledger does; the registry gate reports the malformed value itself."""

    try:
        raw = json.loads(
            (root / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        value = raw["archive_citation"]["ledger"]
    except (OSError, UnicodeDecodeError, ValueError, KeyError, TypeError):
        return ARCHIVE_INDEX
    if isinstance(value, str) and _LEDGER_PATH.fullmatch(value):
        return PurePosixPath(value)
    return ARCHIVE_INDEX


def catalog_line_span(lines: Sequence[str]) -> tuple[int, int] | None:
    """Return the first catalog table's line span so another table parser skips it."""

    for start, line in enumerate(lines):
        if line == CATALOG_HEADER:
            end = start + 1
            while end < len(lines) and lines[end].startswith("|"):
                end += 1
            return start, end
    return None


def parse_catalog(
    text: str,
) -> tuple[dict[PurePosixPath, CatalogRow], tuple[str, ...]]:
    """Parse the Stage 98 catalog; a catalog with no disposition has no table."""

    lines = text.splitlines()
    if sum(1 for line in lines if line == CATALOG_HEADER) > 1:
        return {}, ("ARCHIVE-CATALOG-STRUCTURE",)
    span = catalog_line_span(lines)
    if span is None:
        return {}, ()
    start, end = span
    if start + 1 >= end or lines[start + 1] != CATALOG_SEPARATOR:
        return {}, ("ARCHIVE-CATALOG-STRUCTURE",)
    errors: list[str] = []
    raw_rows = lines[start + 2 : end]
    if not raw_rows:
        errors.append("ARCHIVE-CATALOG-STRUCTURE")
    rows: dict[PurePosixPath, CatalogRow] = {}
    for line in raw_rows:
        match = _CATALOG_ROW.fullmatch(line)
        if match is None or match.group("label") != match.group("target"):
            errors.append("ARCHIVE-CATALOG-STRUCTURE")
            continue
        record = _canonical_repository_path(
            f"{ARCHIVE_ROOT.as_posix()}/{match.group('target')}"
        )
        try:
            envelope = parse_retention_envelope(match.group("envelope"))
        except DispositionError as error:
            errors.append(error.code)
            continue
        if record is None or record in rows:
            errors.append("ARCHIVE-CATALOG-STRUCTURE")
            continue
        rows[record] = CatalogRow(record_path=record, envelope=envelope)
    return rows, tuple(dict.fromkeys(errors))


def catalog_parity_diagnostics(
    registry: "Registry",
    index_text: str,
    texts: Mapping[PurePosixPath, str],
    *,
    frozen_retained: frozenset[PurePosixPath] = frozenset(),
) -> tuple[tuple[str, str], ...]:
    """Require one catalog row per current-generation Stage 98 file, and no other.

    `texts` holds the Stage 98 files the caller read. A retained body a frozen
    ledger already proves keeps that generation and needs no row. Each row must
    name the object its record describes: the mirrored source of a retained
    body, the retired route of a tombstone, or the moved scope of a migration.
    """

    rows, errors = parse_catalog(index_text)
    diagnostics: list[tuple[str, str]] = [
        (code, ARCHIVE_INDEX.as_posix()) for code in errors
    ]
    # ADR-0040: a unit approved to leave the tree keeps its row and its envelope,
    # so its absence is its availability rather than a missing payload.
    removed = removed_records(registry, index_text)
    generation: dict[PurePosixPath, tuple[str, object, str]] = {}
    unit_members: dict[PurePosixPath, dict[PurePosixPath, str]] = {}
    for path, text in texts.items():
        if path in frozen_retained:
            continue
        retention = retention_class_of(registry, path)
        if retention is not None:
            enclosing = enclosing_unit(registry, retention_source_path(path))
            if enclosing is None:
                generation[path] = ("retention", retention, text)
                continue
            # A spec package or Incident bundle is one unit with one row.
            unit, source_root = enclosing
            record = retained_body_path(source_root, retention.name)
            generation[record] = ("unit", (unit, retention), "")
            unit_members.setdefault(record, {})[path] = text
            continue
        try:
            profile = classify_path(registry, path)
        except Exception as error:  # noqa: BLE001 - only the registry's own error means unrouted
            if _is_contract_error(error):
                continue
            raise
        if profile.profile_id in ROUTE_DISPOSITION_PROFILES:
            generation[path] = ("route", profile.profile_id, text)
    for path in sorted(set(generation) ^ set(rows), key=PurePosixPath.as_posix):
        if path in removed and path not in generation:
            continue
        diagnostics.append(("ARCHIVE-CATALOG-PARITY", path.as_posix()))
    for path, (family, kind, text) in sorted(
        generation.items(), key=lambda item: item[0].as_posix()
    ):
        row = rows.get(path)
        if row is None:
            continue
        if family == "route":
            key = (
                "moved_scope" if kind == "archive/scope-migration" else "retired_route"
            )
            if (
                frontmatter_mapping(text).get(key)
                != row.envelope.original_path.as_posix()
            ):
                diagnostics.append(("ARCHIVE-CATALOG-ENVELOPE", path.as_posix()))
            continue
        if row.envelope.original_path != retention_source_path(path):
            diagnostics.append(("ARCHIVE-CATALOG-ENVELOPE", path.as_posix()))
        retention = kind
        if family == "unit":
            unit, retention = kind
            members = unit_members[path]
            if any(path / name not in members for name in unit.required_members):
                diagnostics.append(("ARCHIVE-DISPOSITION-NAMING", path.as_posix()))
                continue
            text = members[path / unit.anchor]
        if retention.names == "successor" and not frontmatter_mapping(text).get(
            "superseded_by"
        ):
            diagnostics.append(("ARCHIVE-DISPOSITION-NAMING", path.as_posix()))
    return tuple(dict.fromkeys(diagnostics))


# ADR-0040: the Retention Assessment table beside the catalog.

_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_RECORD_CELL = re.compile(r"`(?P<record>[^`|]+)`")
_LINK_CELL = re.compile(r"\[[^\]|]+\]\((?P<target>[^)|\s]+)\)")


@dataclass(frozen=True)
class AssessmentRow:
    """One unit's current judgment; the catalog row keeps its source."""

    record_path: PurePosixPath
    assessment: str
    availability: str
    current_owner: PurePosixPath | None
    decision: PurePosixPath | None
    assessed: str
    hold: PurePosixPath | None


def _split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _assessment_contract(registry: "Registry") -> "ArchiveAssessment":
    contract = registry.archive_assessment
    if contract is None:
        raise DispositionError(
            "ARCHIVE-ASSESSMENT-CONTRACT",
            "the registry declares no archive assessment contract",
        )
    return contract


def assessment_line_span(
    registry: "Registry", lines: Sequence[str]
) -> tuple[int, int] | None:
    """Return the assessment table's line span so another table parser skips it."""

    contract = registry.archive_assessment
    if contract is None:
        return None
    heading = f"### {contract.heading}"
    for offset, line in enumerate(lines):
        if line != heading:
            continue
        # The table is the first one in the section; prose may precede it.
        start = offset + 1
        while (
            start < len(lines)
            and not lines[start].startswith("|")
            and not lines[start].startswith("#")
        ):
            start += 1
        end = start
        while end < len(lines) and lines[end].startswith("|"):
            end += 1
        return (start, end) if end > start else None
    return None


def _link_cell(value: str, index: PurePosixPath) -> PurePosixPath | None | str:
    """Return `none` as None, one resolved local link as a path, else the raw cell."""

    if value == "none":
        return None
    match = _LINK_CELL.fullmatch(value)
    if match is None:
        return value
    resolved = posixpath.normpath(
        posixpath.join(index.parent.as_posix(), match.group("target").split("#", 1)[0])
    )
    path = _canonical_repository_path(resolved)
    return path if path is not None else value


def parse_assessment(
    registry: "Registry", text: str
) -> tuple[dict[PurePosixPath, AssessmentRow], tuple[tuple[str, str], ...]]:
    """Parse the Retention Assessment table; no table means no judgment yet."""

    contract = _assessment_contract(registry)
    index = contract.index.as_posix()
    lines = text.splitlines()
    heading = f"### {contract.heading}"
    if sum(1 for line in lines if line == heading) > 1:
        return {}, (("ARCHIVE-ASSESSMENT-STRUCTURE", index),)
    span = assessment_line_span(registry, lines)
    if span is None:
        present = heading in lines
        return {}, ((("ARCHIVE-ASSESSMENT-STRUCTURE", index),) if present else ())
    start, end = span
    width = len(contract.columns)
    if (
        end - start < 2
        or tuple(_split_cells(lines[start])) != contract.columns
        or any(
            re.fullmatch(r":?-{3,}:?", cell) is None
            for cell in _split_cells(lines[start + 1])
        )
        or len(_split_cells(lines[start + 1])) != width
    ):
        return {}, (("ARCHIVE-ASSESSMENT-STRUCTURE", index),)
    rows: dict[PurePosixPath, AssessmentRow] = {}
    errors: list[tuple[str, str]] = []
    for line in lines[start + 2 : end]:
        cells = _split_cells(line)
        record_match = _RECORD_CELL.fullmatch(cells[0]) if cells else None
        record = (
            _canonical_repository_path(
                f"{ARCHIVE_ROOT.as_posix()}/{record_match.group('record')}"
            )
            if record_match is not None
            else None
        )
        links = (
            [_link_cell(cells[column], contract.index) for column in (3, 4, 6)]
            if len(cells) == width
            else []
        )
        if (
            len(cells) != width
            or record is None
            or record in rows
            or any(isinstance(item, str) for item in links)
        ):
            errors.append(("ARCHIVE-ASSESSMENT-STRUCTURE", index))
            continue
        owner, decision, hold = links
        rows[record] = AssessmentRow(
            record_path=record,
            assessment=cells[1],
            availability=cells[2],
            current_owner=owner,  # type: ignore[arg-type]
            decision=decision,  # type: ignore[arg-type]
            assessed=cells[5],
            hold=hold,  # type: ignore[arg-type]
        )
    return rows, tuple(dict.fromkeys(errors))


def assessment_of(
    registry: "Registry",
    rows: Mapping[PurePosixPath, AssessmentRow],
    target: PurePosixPath,
) -> tuple[str, str]:
    """Return the judgment of the unit that holds a target, or the defaults."""

    contract = _assessment_contract(registry)
    for candidate in (target, *target.parents):
        row = rows.get(candidate)
        if row is not None:
            return row.assessment, row.availability
    return contract.default_assessment, contract.default_availability


def _is_calendar_date(value: str) -> bool:
    if _DATE.fullmatch(value) is None:
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def assessment_diagnostics(
    registry: "Registry",
    rows: Mapping[PurePosixPath, AssessmentRow],
    catalog_rows: Mapping[PurePosixPath, object],
    *,
    present: Callable[[PurePosixPath], bool],
    profile_of: Callable[[PurePosixPath], str | None],
) -> tuple[tuple[str, str], ...]:
    """Judge each row against the catalog and the current tree.

    `present` reports whether the tree still holds a record, and `profile_of`
    returns the governed profile of a current document or None. These checks
    prove a Decision document exists and is of an allowed kind; whether its
    approval is real stays a review judgment."""

    contract = _assessment_contract(registry)
    diagnostics: list[tuple[str, str]] = []

    def current(path: PurePosixPath | None) -> str | None:
        if path is None or path.parts[:2] == ARCHIVE_ROOT.parts:
            return None
        return profile_of(path)

    for record, row in sorted(rows.items(), key=lambda item: item[0].as_posix()):
        where = record.as_posix()
        if record not in catalog_rows:
            diagnostics.append(("ARCHIVE-ASSESSMENT-RECORD", where))
        if (
            row.assessment not in contract.assessments
            or row.availability not in contract.availabilities
        ):
            diagnostics.append(("ARCHIVE-ASSESSMENT-VALUE", where))
            continue
        if (row.assessment, row.availability) == (
            contract.default_assessment,
            contract.default_availability,
        ):
            diagnostics.append(("ARCHIVE-ASSESSMENT-NOOP", where))
        if row.availability in contract.reserved_availabilities:
            diagnostics.append(("ARCHIVE-ASSESSMENT-RESERVED", where))
        if current(row.decision) not in contract.decision_profile_ids:
            diagnostics.append(("ARCHIVE-ASSESSMENT-DECISION", where))
        if (
            row.assessment in contract.owner_required_assessments
            and current(row.current_owner) is None
        ) or (row.current_owner is not None and current(row.current_owner) is None):
            diagnostics.append(("ARCHIVE-ASSESSMENT-OWNER", where))
        if not _is_calendar_date(row.assessed):
            diagnostics.append(("ARCHIVE-ASSESSMENT-DATE", where))
        removed = row.availability in contract.removed_availabilities
        if row.hold is not None and (removed or current(row.hold) is None):
            diagnostics.append(("ARCHIVE-ASSESSMENT-HOLD", where))
        if removed == present(record) and row.availability not in (
            contract.reserved_availabilities
        ):
            diagnostics.append(("ARCHIVE-ASSESSMENT-AVAILABILITY", where))
    return tuple(dict.fromkeys(diagnostics))


def removed_records(
    registry: "Registry",
    index_text: str,
    *,
    exists: Callable[[PurePosixPath], bool] | None = None,
) -> frozenset[PurePosixPath]:
    """Return the catalog records a valid assessment row says left the tree.

    A consumer that skips a payload check trusts this answer, so it fails
    closed: a malformed table removes nothing, and a removal row counts only
    when every condition that needs no tree listing holds. Its Decision, owner,
    and Hold are classified by the registry, and, when `exists` is given, must
    also exist. Whether the unit is really absent stays with the caller's own
    payload comparison."""

    contract = registry.archive_assessment
    if contract is None:
        return frozenset()
    rows, errors = parse_assessment(registry, index_text)
    catalog_rows, catalog_errors = parse_catalog(index_text)
    if errors or catalog_errors:
        return frozenset()

    def profile_of(path: PurePosixPath) -> str | None:
        if exists is not None and not exists(path):
            return None
        try:
            return classify_path(registry, path).profile_id
        except Exception as error:  # noqa: BLE001 - only the registry's own error means unrouted
            if _is_contract_error(error):
                return None
            raise

    candidates = {
        record: row
        for record, row in rows.items()
        if row.availability in contract.removed_availabilities
    }
    faulty = {
        PurePosixPath(path)
        for code, path in assessment_diagnostics(
            registry,
            candidates,
            catalog_rows,
            present=lambda _record: False,
            profile_of=profile_of,
        )
    }
    return frozenset(record for record in candidates if record not in faulty)
