"""Import-only ARWB-002 archive and authority validation interfaces.

The module consumes immutable inputs supplied by its caller.  Historical
existence checks use sanitized literal Git tree lookups; current-authority
checks use passed Markdown/profile data.  It does not activate a registry
route, scan the production archive corpus, or inspect ignored workspace state.
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Mapping as RuntimeMapping
from collections.abc import Sequence as RuntimeSequence
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Mapping, Protocol, Sequence

if __package__:
    from scripts.archive_recovery import (
        ArchiveContractError,
        git_tree_path_exists,
        parse_archive_envelope,
        recover_git_blob,
    )
else:  # Direct import-only execution from scripts/.
    from archive_recovery import (  # type: ignore[no-redef]
        ArchiveContractError,
        git_tree_path_exists,
        parse_archive_envelope,
        recover_git_blob,
    )


ARCHIVE_ROOT = PurePosixPath("docs/98.archive")
ARCHIVE_INDEX = ARCHIVE_ROOT / "README.md"
CURRENT_STATUSES = frozenset({"draft", "active", "accepted", "done", "archived"})
CURRENT_MARKDOWN_PROFILES = frozenset(
    {
        "sdlc/prd",
        "sdlc/ard",
        "sdlc/adr",
        "sdlc/spec",
        "sdlc/api-spec",
        "sdlc/agent-design",
        "sdlc/data-model",
        "sdlc/tests",
        "sdlc/plan",
        "sdlc/task",
        "sdlc/guide",
        "sdlc/policy",
        "sdlc/runbook",
        "sdlc/incident",
        "sdlc/postmortem",
        "content/reference",
        "content/archive",
        "governance/reference",
        "governance/memory",
        "governance/template-support",
        "governance/progress-ledger",
        "readme/repository",
        "readme/stage-index",
        "readme/collection-index",
        "readme/implementation",
        "readme/snapshot-pack",
        "readme/workspace-staging",
    }
)
_MISSING_INVENTORY = object()
_LINK_MODULE_TOKEN = object()
_LINK_KINDS_WITH_TARGET = frozenset({"local", "anchor"})
_LINK_KINDS_WITHOUT_TARGET = frozenset(
    {"external", "LINK-FILE-URI", "LINK-ABSOLUTE", "LINK-ESCAPE"}
)


class _RenderedLink(Protocol):
    kind: str
    target: PurePosixPath | None


class _RenderedLinkAdapter(Protocol):
    def __call__(
        self, markdown: str, source_path: str | PurePosixPath
    ) -> tuple[_RenderedLink, ...]: ...


@dataclass(frozen=True)
class ArchiveRecord:
    """One proposed archive path and its non-rendered envelope bytes."""

    path: str
    content: bytes = field(repr=False)


@dataclass(frozen=True)
class CurrentMarkdownDocument:
    """Immutable current-document input supplied by the owning caller."""

    path: str
    markdown: str = field(repr=False)
    profile: str
    status: str


@dataclass(frozen=True)
class ArchiveDiagnostic:
    """Stable archive validation result without payload-derived values."""

    code: str
    path: str


@dataclass(frozen=True)
class ArchiveValidationReport:
    """Deterministic aggregate result for one validation boundary."""

    diagnostics: tuple[ArchiveDiagnostic, ...] = ()
    historical_link_count: int = 0

    @property
    def valid(self) -> bool:
        return not self.diagnostics


def _canonical_path(value: object, *, archive_only: bool = False) -> str | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        return None
    path = PurePosixPath(value)
    if (
        not path.parts
        or path.is_absolute()
        or path.as_posix() != value
        or "." in path.parts
        or ".." in path.parts
    ):
        return None
    if archive_only and (len(path.parts) < 3 or not path.is_relative_to(ARCHIVE_ROOT)):
        return None
    return path.as_posix()


def _diagnostic(code: str, path: object) -> ArchiveDiagnostic:
    canonical = _canonical_path(path)
    return ArchiveDiagnostic(code=code, path=canonical or "<invalid-path>")


def _contract_diagnostic(code: str) -> ArchiveDiagnostic:
    return ArchiveDiagnostic(code=code, path="<input>")


def _report(
    diagnostics: Sequence[ArchiveDiagnostic],
    *,
    historical_link_count: int = 0,
) -> ArchiveValidationReport:
    return ArchiveValidationReport(
        diagnostics=tuple(sorted(diagnostics, key=lambda item: (item.path, item.code))),
        historical_link_count=historical_link_count,
    )


@lru_cache(maxsize=1)
def _load_canonical_link_module() -> ModuleType:
    """Load and verify the canonical validator under a private unique identity."""

    module_path = Path(__file__).resolve(strict=True)
    script_path = module_path.with_name("validate-links-and-owners.py").resolve(
        strict=True
    )
    if script_path.parent != module_path.parent:
        raise RuntimeError("canonical rendered-link adapter is unavailable")
    private_suffix = f"{id(_LINK_MODULE_TOKEN):x}"
    module_name = f"_archive_canonical_links_{private_suffix}"
    while module_name in sys.modules:
        module_name += "_private"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical rendered-link adapter is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    scripts_path = str(script_path.parent)
    inserted = scripts_path not in sys.path
    if inserted:
        sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
        reported_file = Path(str(getattr(module, "__file__", ""))).resolve(strict=True)
        if reported_file != script_path or module.__name__ != module_name:
            raise RuntimeError("canonical rendered-link adapter is unavailable")
    except Exception:
        raise
    finally:
        sys.modules.pop(module_name, None)
        if inserted:
            sys.path.remove(scripts_path)
    return module


def _rendered_link_adapter() -> _RenderedLinkAdapter:
    module = _load_canonical_link_module()
    adapter = getattr(module, "rendered_local_links", None)
    if not callable(adapter) or getattr(adapter, "__module__", None) != module.__name__:
        raise RuntimeError("canonical rendered-link adapter is unavailable")
    return adapter


def _validated_rendered_links(
    markdown: str,
    source_path: str,
) -> tuple[_RenderedLink, ...]:
    module = _load_canonical_link_module()
    adapter = _rendered_link_adapter()
    result = adapter(markdown, source_path)
    if isinstance(result, (str, bytes, bytearray, RuntimeMapping)) or not isinstance(
        result, RuntimeSequence
    ):
        raise RuntimeError("canonical rendered-link adapter returned invalid data")
    link_type = getattr(module, "RenderedLocalLink", None)
    if not isinstance(link_type, type):
        raise RuntimeError("canonical rendered-link adapter returned invalid data")
    links = tuple(result)
    for link in links:
        if type(link) is not link_type:
            raise RuntimeError("canonical rendered-link adapter returned invalid data")
        kind = getattr(link, "kind", None)
        raw_target = getattr(link, "raw_target", None)
        target = getattr(link, "target", None)
        if not isinstance(kind, str) or not isinstance(raw_target, str):
            raise RuntimeError("canonical rendered-link adapter returned invalid data")
        if kind in _LINK_KINDS_WITH_TARGET:
            if not isinstance(target, PurePosixPath):
                raise RuntimeError(
                    "canonical rendered-link adapter returned invalid data"
                )
            canonical_target = _canonical_path(target.as_posix())
            if canonical_target != target.as_posix():
                raise RuntimeError(
                    "canonical rendered-link adapter returned invalid data"
                )
        elif kind in _LINK_KINDS_WITHOUT_TARGET:
            if target is not None:
                raise RuntimeError(
                    "canonical rendered-link adapter returned invalid data"
                )
        else:
            raise RuntimeError("canonical rendered-link adapter returned invalid data")
    return links


def _exact_sequence(
    value: object,
    *,
    element_type: type,
    container_code: str,
    element_code: str,
) -> tuple[tuple[object, ...] | None, tuple[ArchiveDiagnostic, ...]]:
    if isinstance(value, (str, bytes, bytearray, RuntimeMapping)) or not isinstance(
        value, RuntimeSequence
    ):
        return None, (_contract_diagnostic(container_code),)
    try:
        items = tuple(value)
    except Exception:
        return None, (_contract_diagnostic(container_code),)
    if any(type(item) is not element_type for item in items):
        return None, (_contract_diagnostic(element_code),)
    return items, ()


def _archive_inventory(
    value: object,
) -> tuple[frozenset[str], tuple[ArchiveDiagnostic, ...]]:
    if value is _MISSING_INVENTORY:
        return frozenset(), (_contract_diagnostic("ARCHIVE-INVENTORY-MISSING"),)
    if type(value) is not frozenset:
        return frozenset(), (_contract_diagnostic("ARCHIVE-INVENTORY-CONTRACT"),)
    if not value:
        return frozenset(), (_contract_diagnostic("ARCHIVE-INVENTORY-MISSING"),)
    diagnostics: list[ArchiveDiagnostic] = []
    canonical_paths: set[str] = set()
    for member in value:
        canonical = _canonical_path(member, archive_only=True)
        if canonical is None or canonical == ARCHIVE_INDEX.as_posix():
            diagnostics.append(_contract_diagnostic("ARCHIVE-INVENTORY-PATH-INVALID"))
        else:
            canonical_paths.add(canonical)
    return frozenset(canonical_paths), tuple(diagnostics)


def _archive_mapping(
    value: object,
    *,
    container_code: str,
) -> tuple[dict[str, bytes] | None, tuple[ArchiveDiagnostic, ...]]:
    if not isinstance(value, RuntimeMapping):
        return None, (_contract_diagnostic(container_code),)
    try:
        items = tuple(value.items())
    except Exception:
        return None, (_contract_diagnostic(container_code),)
    normalized: dict[str, bytes] = {}
    diagnostics: list[ArchiveDiagnostic] = []
    for raw_path, content in items:
        canonical = _canonical_path(raw_path, archive_only=True)
        if canonical is None:
            diagnostics.append(_contract_diagnostic("ARCHIVE-PATH-INVALID"))
            continue
        if canonical in normalized:
            diagnostics.append(_contract_diagnostic("ARCHIVE-DUPLICATE-PATH"))
            continue
        if not isinstance(content, bytes):
            diagnostics.append(_diagnostic("ARCHIVE-CONTENT-TYPE", canonical))
            continue
        normalized[canonical] = content
    return normalized, tuple(diagnostics)


def validate_archive_records(
    repository_root: str | Path,
    records: Sequence[ArchiveRecord] | object,
) -> ArchiveValidationReport:
    """Validate envelope, provenance, integrity, mirror, and historical links."""

    if not isinstance(repository_root, (str, Path)) or not str(repository_root):
        return _report((_contract_diagnostic("ARCHIVE-REPOSITORY-CONTRACT"),))
    diagnostics: list[ArchiveDiagnostic] = []
    historical_link_count = 0
    original_owners: dict[str, str] = {}
    seen_archive_paths: set[str] = set()
    materialized, contract_diagnostics = _exact_sequence(
        records,
        element_type=ArchiveRecord,
        container_code="ARCHIVE-RECORDS-CONTRACT",
        element_code="ARCHIVE-RECORD-CONTRACT",
    )
    if materialized is None:
        return _report(contract_diagnostics)
    typed_records = tuple(
        record for record in materialized if type(record) is ArchiveRecord
    )
    prepared_records: list[tuple[str, ArchiveRecord]] = []
    for record in typed_records:
        archive_path = _canonical_path(record.path, archive_only=True)
        if archive_path is None:
            diagnostics.append(_contract_diagnostic("ARCHIVE-PATH-INVALID"))
            continue
        if not isinstance(record.content, bytes):
            diagnostics.append(_diagnostic("ARCHIVE-CONTENT-TYPE", archive_path))
            continue
        prepared_records.append((archive_path, record))

    for archive_path, record in sorted(prepared_records, key=lambda item: item[0]):
        if archive_path in seen_archive_paths:
            diagnostics.append(_diagnostic("ARCHIVE-DUPLICATE-PATH", archive_path))
            continue
        seen_archive_paths.add(archive_path)

        try:
            parsed = parse_archive_envelope(record.content)
        except ArchiveContractError as exc:
            diagnostics.append(_diagnostic(exc.code, archive_path))
            continue

        original_path = parsed.metadata["original_path"]
        if not isinstance(original_path, str):
            diagnostics.append(_diagnostic("ARCHIVE-METADATA-TYPE", archive_path))
            continue
        previous_owner = original_owners.get(original_path)
        if previous_owner is not None:
            diagnostics.append(
                _diagnostic("ARCHIVE-DUPLICATE-ORIGINAL-PATH", archive_path)
            )
        else:
            original_owners[original_path] = archive_path

        source_commit = parsed.metadata["source_commit"]
        if not isinstance(source_commit, str):
            diagnostics.append(_diagnostic("ARCHIVE-METADATA-TYPE", archive_path))
            continue
        try:
            recovered = recover_git_blob(
                repository_root,
                original_path,
                source_commit,
            )
            parse_archive_envelope(record.content, expected=recovered)
        except ArchiveContractError as exc:
            diagnostics.append(_diagnostic(exc.code, archive_path))
            continue

        if archive_path != recovered.proposed_archive_path:
            diagnostics.append(_diagnostic("ARCHIVE-MIRROR-MISMATCH", archive_path))

        try:
            payload_text = parsed.payload.decode("utf-8", errors="strict")
            rendered_links = _validated_rendered_links(payload_text, original_path)
        except Exception:
            diagnostics.append(
                _diagnostic("ARCHIVE-LINK-ADAPTER-FAILURE", archive_path)
            )
            continue
        for link in rendered_links:
            if link.kind in {"external", "anchor"}:
                continue
            historical_link_count += 1
            if link.kind != "local" or link.target is None:
                diagnostics.append(
                    _diagnostic("ARCHIVE-HISTORICAL-LINK-INVALID", archive_path)
                )
                continue
            try:
                exists = git_tree_path_exists(
                    repository_root,
                    source_commit,
                    link.target.as_posix(),
                )
            except ArchiveContractError:
                diagnostics.append(
                    _diagnostic("ARCHIVE-HISTORICAL-LOOKUP-FAILURE", archive_path)
                )
                continue
            if not exists:
                diagnostics.append(
                    _diagnostic("ARCHIVE-HISTORICAL-LINK-MISSING", archive_path)
                )

    return _report(diagnostics, historical_link_count=historical_link_count)


def validate_current_archive_authority(
    documents: Sequence[CurrentMarkdownDocument] | object,
    *,
    individual_archive_paths: frozenset[str] | object = _MISSING_INVENTORY,
) -> ArchiveValidationReport:
    """Validate passed current Markdown/profile data without filesystem reads."""

    materialized, contract_diagnostics = _exact_sequence(
        documents,
        element_type=CurrentMarkdownDocument,
        container_code="ARCHIVE-CURRENT-DOCUMENTS-CONTRACT",
        element_code="ARCHIVE-CURRENT-DOCUMENT-CONTRACT",
    )
    canonical_individuals, inventory_diagnostics = _archive_inventory(
        individual_archive_paths
    )
    diagnostics: list[ArchiveDiagnostic] = [
        *contract_diagnostics,
        *inventory_diagnostics,
    ]
    if materialized is None:
        return _report(diagnostics)
    typed_documents = tuple(
        document
        for document in materialized
        if type(document) is CurrentMarkdownDocument
    )
    prepared_documents: list[tuple[str, CurrentMarkdownDocument, bool, bool, bool]] = []
    for document in typed_documents:
        path = _canonical_path(document.path)
        if path is None:
            diagnostics.append(_contract_diagnostic("ARCHIVE-CURRENT-PATH-INVALID"))
            continue
        markdown_valid = isinstance(document.markdown, str)
        status_valid = (
            isinstance(document.status, str) and document.status in CURRENT_STATUSES
        )
        profile_valid = (
            isinstance(document.profile, str)
            and document.profile in CURRENT_MARKDOWN_PROFILES
        )
        if not markdown_valid:
            diagnostics.append(_diagnostic("ARCHIVE-CURRENT-CONTENT-TYPE", path))
        if not status_valid:
            diagnostics.append(_diagnostic("ARCHIVE-CURRENT-STATUS-INVALID", path))
        if not profile_valid:
            diagnostics.append(_diagnostic("ARCHIVE-CURRENT-PROFILE-INVALID", path))
        prepared_documents.append(
            (path, document, markdown_valid, status_valid, profile_valid)
        )

    for path, document, markdown_valid, status_valid, profile_valid in sorted(
        prepared_documents, key=lambda item: item[0]
    ):
        current = status_valid and document.status in {"active", "accepted"}
        pure_path = PurePosixPath(path)
        archive_record_path = (
            pure_path.is_relative_to(ARCHIVE_ROOT) and pure_path != ARCHIVE_INDEX
        )
        if current and (
            archive_record_path
            or document.profile == "content/archive"
            or path in canonical_individuals
        ):
            diagnostics.append(_diagnostic("ARCHIVE-REACTIVATED", path))
        if not status_valid or not profile_valid or not markdown_valid or not current:
            continue
        if archive_record_path:
            continue
        try:
            rendered_links = _validated_rendered_links(document.markdown, path)
        except Exception:
            diagnostics.append(_diagnostic("ARCHIVE-LINK-ADAPTER-FAILURE", path))
            continue
        for link in rendered_links:
            target = link.target
            if link.kind != "local" or target is None:
                continue
            target_path = target.as_posix()
            if target_path in canonical_individuals or (
                target.is_relative_to(ARCHIVE_ROOT) and target != ARCHIVE_INDEX
            ):
                diagnostics.append(_diagnostic("ARCHIVE-DIRECT-CURRENT-LINK", path))
    return _report(diagnostics)


def validate_archive_immutability(
    baseline: Mapping[str, bytes] | object,
    proposed: Mapping[str, bytes] | object,
) -> ArchiveValidationReport:
    """Reject mutation or deletion of an existing archive record."""

    normalized_baseline, baseline_diagnostics = _archive_mapping(
        baseline, container_code="ARCHIVE-BASELINE-CONTRACT"
    )
    normalized_proposed, proposed_diagnostics = _archive_mapping(
        proposed, container_code="ARCHIVE-PROPOSED-CONTRACT"
    )
    input_diagnostics = (*baseline_diagnostics, *proposed_diagnostics)
    if input_diagnostics:
        return _report(input_diagnostics)
    if normalized_baseline is None or normalized_proposed is None:
        return _report((_contract_diagnostic("ARCHIVE-MAPPING-CONTRACT"),))
    diagnostics: list[ArchiveDiagnostic] = []
    for path in sorted(normalized_baseline):
        if path not in normalized_proposed:
            diagnostics.append(_diagnostic("ARCHIVE-IMMUTABLE-DELETION", path))
            continue
        if normalized_baseline[path] != normalized_proposed[path]:
            diagnostics.append(_diagnostic("ARCHIVE-IMMUTABLE-MUTATION", path))
    return _report(diagnostics)
