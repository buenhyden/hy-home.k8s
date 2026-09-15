#!/usr/bin/env python3
"""Own the ADR-0038 six-disposition Stage 98 contract the validators share.

Content frozen under ADR-0032 keeps its generation and its existing owners.
This module answers only what the current generation asks: which retention
class a path belongs to, which classes a current document may cite, and what
the Stage 98 catalog's one Retention Envelope names. It holds no second
recovery ledger; Git history recovers the object the envelope names.
"""

from __future__ import annotations

import importlib
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import TYPE_CHECKING, Mapping, Sequence

import yaml

if TYPE_CHECKING:
    from document_contracts import CitationRule, Registry, RetentionClass, RetentionMode


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

_COMMIT = re.compile(r"[0-9a-f]{40}")
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
    if target == (table.index if table is not None else ARCHIVE_INDEX):
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
    # A retained-body rule that does not cover this class passes to the next rule.
    return rule.target != "retained-body" or target_class in rule.target_classes


def citation_decision(
    registry: "Registry",
    source: PurePosixPath,
    source_profile_id: str,
    target: PurePosixPath,
) -> CitationDecision | None:
    """Decide a citation into Stage 98 from the registry's ordered table.

    The first matching rule decides; with no match the table's default does.
    A target outside Stage 98 is not a citation decision and returns None."""

    kind = archive_target_kind(registry, target)
    if kind is None:
        return None
    table = registry.archive_citation
    if table is None:
        raise DispositionError(
            "ARCHIVE-CITATION-TABLE", "the registry declares no archive citation table"
        )
    target_kind, target_class = kind
    for position, rule in enumerate(table.rules, start=1):
        if _rule_matches(rule, source, source_profile_id, target_kind, target_class):
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
    generation: dict[PurePosixPath, tuple[str, object, str]] = {}
    for path, text in texts.items():
        if path in frozen_retained:
            continue
        retention = retention_class_of(registry, path)
        if retention is not None:
            generation[path] = ("retention", retention, text)
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
        diagnostics.append(("ARCHIVE-CATALOG-PARITY", path.as_posix()))
    for path, (family, kind, text) in sorted(
        generation.items(), key=lambda item: item[0].as_posix()
    ):
        row = rows.get(path)
        if row is None:
            continue
        metadata = frontmatter_mapping(text)
        if family == "retention":
            if row.envelope.original_path != retention_source_path(path):
                diagnostics.append(("ARCHIVE-CATALOG-ENVELOPE", path.as_posix()))
            if kind.names == "successor" and not metadata.get("superseded_by"):
                diagnostics.append(("ARCHIVE-DISPOSITION-NAMING", path.as_posix()))
            if kind.name == "resolved":
                sibling = path.with_name(
                    "postmortem.md" if path.name == "incident.md" else "incident.md"
                )
                if sibling not in generation:
                    diagnostics.append(("ARCHIVE-DISPOSITION-NAMING", path.as_posix()))
            continue
        key = "moved_scope" if kind == "archive/scope-migration" else "retired_route"
        if metadata.get(key) != row.envelope.original_path.as_posix():
            diagnostics.append(("ARCHIVE-CATALOG-ENVELOPE", path.as_posix()))
    return tuple(dict.fromkeys(diagnostics))
