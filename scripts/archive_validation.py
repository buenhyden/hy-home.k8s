"""Import-only ARWB-002 archive and authority validation interfaces.

The module consumes immutable inputs supplied by its caller.  Historical
existence checks use sanitized literal Git tree lookups; current-authority
checks use passed Markdown/profile data.  It does not activate a registry
route, scan the production archive corpus, or inspect ignored workspace state.
"""

from __future__ import annotations

import importlib.util
import os
import re
import stat
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
    record_count: int = 0
    index_record_count: int = 0
    namespace_counts: tuple[tuple[str, int], ...] = ()
    record_link_counts: tuple[tuple[str, int], ...] = ()

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
    record_count: int = 0,
    index_record_count: int = 0,
    namespace_counts: Sequence[tuple[str, int]] = (),
    record_link_counts: Sequence[tuple[str, int]] = (),
) -> ArchiveValidationReport:
    return ArchiveValidationReport(
        diagnostics=tuple(sorted(diagnostics, key=lambda item: (item.path, item.code))),
        historical_link_count=historical_link_count,
        record_count=record_count,
        index_record_count=index_record_count,
        namespace_counts=tuple(namespace_counts),
        record_link_counts=tuple(record_link_counts),
    )


_NAMESPACE_CONTRACT = (
    ("arwb-base", "exact-immutable", 31, 31),
    ("acer-additive", "exact-immutable", 12, 12),
    ("wdtc-execution", "exact-reviewed-manifest", 50, 50),
    ("progress-snapshot", "append-only-unique", 0, 1),
)
_INDEX_HEADER = (
    "| Archive Record | Original Path | Original Type | Source Commit | Source "
    "Blob | Payload SHA-256 | Historical Links | Current Replacement | Reason |"
)
_INDEX_SEPARATOR = (
    "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |"
)
_INDEX_LINK = re.compile(r"\[`(?P<label>[^`]+)`\]\(\./(?P<target>[^)]+)\)\Z")
_INDEX_CODE = re.compile(r"`(?P<value>[^`]+)`\Z")
_INDEX_MARKER = re.compile(
    r"<!-- archive-manifest:v1 records=(?P<records>\d+) "
    r"historical-links=(?P<links>\d+) -->"
)


def _namespace_records(
    registry: object,
) -> tuple[dict[str, tuple[str, ...]], list[ArchiveDiagnostic]]:
    diagnostics: list[ArchiveDiagnostic] = []
    if not isinstance(registry, RuntimeMapping) or registry.get(
        "archiveContractVersion"
    ) != 2:
        return {}, [_contract_diagnostic("ARCHIVE-NAMESPACE-CONTRACT")]
    raw_namespaces = registry.get("archiveNamespaces")
    if type(raw_namespaces) is not list or len(raw_namespaces) != len(
        _NAMESPACE_CONTRACT
    ):
        return {}, [_contract_diagnostic("ARCHIVE-NAMESPACE-CONTRACT")]
    namespaces: dict[str, tuple[str, ...]] = {}
    seen: set[str] = set()
    for raw, (expected_id, expected_policy, minimum, maximum) in zip(
        raw_namespaces, _NAMESPACE_CONTRACT, strict=True
    ):
        if (
            type(raw) is not dict
            or tuple(raw) != ("id", "policy", "records")
            or raw.get("id") != expected_id
            or raw.get("policy") != expected_policy
            or type(raw.get("records")) is not list
        ):
            diagnostics.append(_contract_diagnostic("ARCHIVE-NAMESPACE-CONTRACT"))
            continue
        raw_records = raw["records"]
        if not minimum <= len(raw_records) <= maximum:
            diagnostics.append(_contract_diagnostic("ARCHIVE-NAMESPACE-COUNT"))
        canonical: list[str] = []
        for value in raw_records:
            path = _canonical_path(value, archive_only=True)
            if path is None or path == ARCHIVE_INDEX.as_posix():
                diagnostics.append(_diagnostic("ARCHIVE-NAMESPACE-PATH", value))
                continue
            if path in seen:
                diagnostics.append(_diagnostic("ARCHIVE-NAMESPACE-OVERLAP", path))
            seen.add(path)
            canonical.append(path)
        if len(set(canonical)) != len(canonical):
            diagnostics.append(_contract_diagnostic("ARCHIVE-NAMESPACE-OVERLAP"))
        namespaces[expected_id] = tuple(canonical)
    return namespaces, diagnostics


def _repository_archive_records(
    root: Path,
) -> tuple[dict[str, bytes], list[ArchiveDiagnostic]]:
    records: dict[str, bytes] = {}
    diagnostics: list[ArchiveDiagnostic] = []
    archive_root = root / ARCHIVE_ROOT
    try:
        archive_root_stat = archive_root.lstat()
    except OSError:
        return {}, [_diagnostic("ARCHIVE-ROOT-UNAVAILABLE", ARCHIVE_ROOT.as_posix())]
    if stat.S_ISLNK(archive_root_stat.st_mode) or not stat.S_ISDIR(
        archive_root_stat.st_mode
    ):
        return {}, [_diagnostic("ARCHIVE-ROOT-UNAVAILABLE", ARCHIVE_ROOT.as_posix())]
    try:
        for directory, names, filenames in os.walk(archive_root, followlinks=False):
            directory_path = Path(directory)
            safe_names: list[str] = []
            for name in names:
                child = directory_path / name
                metadata = child.lstat()
                if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
                    safe_names.append(name)
                else:
                    relative = child.relative_to(root).as_posix()
                    diagnostics.append(_diagnostic("ARCHIVE-INVENTORY-TYPE", relative))
            names[:] = safe_names
            for filename in filenames:
                child = directory_path / filename
                relative = child.relative_to(root).as_posix()
                if relative == ARCHIVE_INDEX.as_posix() or not relative.endswith(".md"):
                    continue
                metadata = child.lstat()
                if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                    diagnostics.append(_diagnostic("ARCHIVE-INVENTORY-TYPE", relative))
                    continue
                records[relative] = child.read_bytes()
    except (OSError, RuntimeError, ValueError):
        diagnostics.append(_diagnostic("ARCHIVE-INVENTORY-READ", ARCHIVE_ROOT.as_posix()))
    return records, diagnostics


def _parse_repository_index(
    text: str,
) -> tuple[dict[str, tuple[str, ...]], int, list[ArchiveDiagnostic]]:
    diagnostics: list[ArchiveDiagnostic] = []
    lines = text.splitlines()
    headers = [offset for offset, line in enumerate(lines) if line == _INDEX_HEADER]
    if len(headers) != 1:
        return {}, 0, [_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix())]
    header = headers[0]
    if header + 1 >= len(lines) or lines[header + 1] != _INDEX_SEPARATOR:
        return {}, 0, [_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix())]
    raw_rows: list[str] = []
    for line in lines[header + 2 :]:
        if not line.startswith("|"):
            break
        raw_rows.append(line)
    end = header + 2 + len(raw_rows)
    if any(line.startswith("|") for line in lines[end:]):
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix()))
    rows: dict[str, tuple[str, ...]] = {}
    link_total = 0
    for line in raw_rows:
        cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
        if len(cells) != 9:
            diagnostics.append(_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix()))
            continue
        link = _INDEX_LINK.fullmatch(cells[0])
        code_cells = tuple(_INDEX_CODE.fullmatch(cells[index]) for index in (1, 2, 3, 4, 5, 8))
        if link is None or any(match is None for match in code_cells) or not cells[6].isdigit():
            diagnostics.append(_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix()))
            continue
        path = f"docs/98.archive/{link.group('target')}"
        if link.group("label") != link.group("target") or _canonical_path(path, archive_only=True) is None or path in rows:
            diagnostics.append(_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix()))
            continue
        values = tuple(match.group("value") for match in code_cells if match is not None)
        rows[path] = (*values, cells[7], cells[6])
        link_total += int(cells[6])
    markers = tuple(_INDEX_MARKER.finditer(text))
    if (
        len(markers) != 1
        or int(markers[0].group("records")) != len(rows)
        or int(markers[0].group("links")) != link_total
    ):
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-MANIFEST", ARCHIVE_INDEX.as_posix()))
    return rows, link_total, diagnostics


def validate_repository_archive(
    repository_root: str | Path,
    registry: object,
) -> ArchiveValidationReport:
    """Validate the complete version-2 repository archive and README index."""

    try:
        root = Path(repository_root).resolve(strict=True)
        if not root.is_dir():
            raise OSError
    except (OSError, RuntimeError, TypeError):
        return _report((_diagnostic("ARCHIVE-ROOT-UNAVAILABLE", "<repository>"),))
    namespaces, namespace_diagnostics = _namespace_records(registry)
    records, inventory_diagnostics = _repository_archive_records(root)
    declared = frozenset(path for paths in namespaces.values() for path in paths)
    actual = frozenset(records)
    diagnostics = [*namespace_diagnostics, *inventory_diagnostics]
    if actual != declared:
        diagnostics.append(_diagnostic("ARCHIVE-NAMESPACE-PARITY", ARCHIVE_ROOT.as_posix()))
    typed_records = tuple(
        ArchiveRecord(path=path, content=content)
        for path, content in sorted(records.items())
    )
    record_report = validate_archive_records(root, typed_records)
    diagnostics.extend(record_report.diagnostics)
    metadata_by_path: dict[str, Mapping[str, object]] = {}
    for record in typed_records:
        try:
            parsed = parse_archive_envelope(record.content)
        except ArchiveContractError:
            continue
        metadata_by_path[record.path] = parsed.metadata
        original_path = parsed.metadata.get("original_path")
        if isinstance(original_path, str):
            try:
                (root / original_path).lstat()
            except FileNotFoundError:
                pass
            except OSError:
                diagnostics.append(_diagnostic("ARCHIVE-ORIGINAL-READ", record.path))
            else:
                diagnostics.append(_diagnostic("ARCHIVE-ORIGINAL-STILL-CURRENT", record.path))
    try:
        index_text = (root / ARCHIVE_INDEX).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        index_text = ""
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-READ", ARCHIVE_INDEX.as_posix()))
    index_rows, index_links, index_diagnostics = _parse_repository_index(index_text)
    diagnostics.extend(index_diagnostics)
    if frozenset(index_rows) != actual:
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-PARITY", ARCHIVE_INDEX.as_posix()))
    if index_links != record_report.historical_link_count:
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-LINKS", ARCHIVE_INDEX.as_posix()))
    for path, metadata in metadata_by_path.items():
        row = index_rows.get(path)
        if row is None:
            continue
        expected = (
            str(metadata.get("original_path")),
            str(metadata.get("original_type")),
            str(metadata.get("source_commit")),
            str(metadata.get("source_blob")),
            str(metadata.get("content_sha256")),
            str(metadata.get("archive_reason")),
        )
        if row[:5] + (row[5],) != expected:
            diagnostics.append(_diagnostic("ARCHIVE-INDEX-MEMBER", path))
    namespace_counts = tuple(
        (namespace, len(namespaces.get(namespace, ())))
        for namespace, _policy, _minimum, _maximum in _NAMESPACE_CONTRACT
    )
    return _report(
        diagnostics,
        historical_link_count=record_report.historical_link_count,
        record_count=len(records),
        index_record_count=len(index_rows),
        namespace_counts=namespace_counts,
        record_link_counts=record_report.record_link_counts,
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
    record_link_counts: dict[str, int] = {}
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
        record_link_counts[archive_path] = 0
        for link in rendered_links:
            if link.kind in {"external", "anchor"}:
                continue
            historical_link_count += 1
            record_link_counts[archive_path] += 1
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

    return _report(
        diagnostics,
        historical_link_count=historical_link_count,
        record_link_counts=tuple(sorted(record_link_counts.items())),
    )


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
