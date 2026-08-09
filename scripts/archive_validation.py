"""Import-only ARWB-002 archive and authority validation interfaces.

The module consumes immutable inputs supplied by its caller.  Historical
existence checks use sanitized literal Git tree lookups; current-authority
checks use passed Markdown/profile data.  It does not activate a registry
route, scan the production archive corpus, or inspect ignored workspace state.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import posixpath
import re
import stat
import subprocess
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
        RecoveryResult,
        parse_archive_envelope,
    )
else:  # Direct import-only execution from scripts/.
    from archive_recovery import (  # type: ignore[no-redef]
        ArchiveContractError,
        RecoveryResult,
        parse_archive_envelope,
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
    reviewed_manifest_records: tuple[ReviewedManifestRecord, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.diagnostics


@dataclass(frozen=True, order=True)
class ReviewedManifestRecord:
    """One exact archive-unique row admitted by the reviewed stage-zero manifest."""

    target: str
    original_path: str
    source_commit: str
    source_blob: str


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
    reviewed_manifest_records: Sequence[ReviewedManifestRecord] = (),
) -> ArchiveValidationReport:
    return ArchiveValidationReport(
        diagnostics=tuple(sorted(diagnostics, key=lambda item: (item.path, item.code))),
        historical_link_count=historical_link_count,
        record_count=record_count,
        index_record_count=index_record_count,
        namespace_counts=tuple(namespace_counts),
        record_link_counts=tuple(record_link_counts),
        reviewed_manifest_records=tuple(reviewed_manifest_records),
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
_INDEX_REPLACEMENT_LINK = re.compile(
    r"\[`(?P<label>docs/[^`]+)`\]\((?P<target>(?:\.\.?/)[^)]+)\)\Z"
)
_INDEX_CODE = re.compile(r"`(?P<value>[^`]+)`\Z")
_INDEX_MARKER = re.compile(
    r"<!-- archive-manifest:v1 records=(?P<records>\d+) "
    r"historical-links=(?P<links>\d+) -->"
)
_FULL_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_ARCHIVE_RECORD_LIMIT = 8 * 1024 * 1024
_GIT_TIMEOUT_SECONDS = 20
_MANIFEST_SOURCE_COMMIT = (
    "713dff1fc3de58a2d1682970a7f24faa39c14263"  # pragma: allowlist secret
)
_MIGRATION_MODULE_TOKEN = object()


@dataclass(frozen=True)
class _GitTreeMember:
    mode: str
    kind: str
    object_id: str


@dataclass(frozen=True)
class _PreparedEnvelope:
    archive_path: str
    record: ArchiveRecord
    original_path: str
    source_commit: str
    rendered_links: tuple[_RenderedLink, ...]


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
    archive_fd: int | None = None

    def read_record(directory_fd: int, name: str, relative: str) -> bytes:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=directory_fd,
        )
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode) or before.st_size > _ARCHIVE_RECORD_LIMIT:
                raise OSError
            chunks: list[bytes] = []
            remaining = before.st_size
            while remaining:
                chunk = os.read(descriptor, min(65536, remaining))
                if not chunk:
                    raise OSError
                chunks.append(chunk)
                remaining -= len(chunk)
            if os.read(descriptor, 1):
                raise OSError
            after = os.fstat(descriptor)
            linked = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if (
                before.st_dev != after.st_dev
                or before.st_ino != after.st_ino
                or before.st_mode != after.st_mode
                or before.st_size != after.st_size
                or before.st_dev != linked.st_dev
                or before.st_ino != linked.st_ino
            ):
                raise OSError
            return b"".join(chunks)
        finally:
            os.close(descriptor)

    def visit(directory_fd: int, relative_directory: PurePosixPath) -> None:
        for name in sorted(os.listdir(directory_fd)):
            relative_path = relative_directory / name
            relative = relative_path.as_posix()
            metadata = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if stat.S_ISDIR(metadata.st_mode):
                child_fd = os.open(
                    name,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                    dir_fd=directory_fd,
                )
                try:
                    visit(child_fd, relative_path)
                finally:
                    os.close(child_fd)
            elif stat.S_ISREG(metadata.st_mode):
                if relative != ARCHIVE_INDEX.as_posix() and relative.endswith(".md"):
                    records[relative] = read_record(directory_fd, name, relative)
            else:
                diagnostics.append(_diagnostic("ARCHIVE-INVENTORY-TYPE", relative))

    try:
        archive_fd = os.open(
            archive_root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        visit(archive_fd, ARCHIVE_ROOT)
    except (OSError, RuntimeError, ValueError):
        diagnostics.append(_diagnostic("ARCHIVE-INVENTORY-READ", ARCHIVE_ROOT.as_posix()))
    finally:
        if archive_fd is not None:
            try:
                os.close(archive_fd)
            except OSError:
                diagnostics.append(
                    _diagnostic("ARCHIVE-INVENTORY-READ", ARCHIVE_ROOT.as_posix())
                )
    return records, diagnostics


@lru_cache(maxsize=1)
def _load_migration_module() -> ModuleType:
    module_path = Path(__file__).resolve(strict=True)
    script_path = module_path.with_name("migrate-document-work-units.py").resolve(
        strict=True
    )
    if script_path.parent != module_path.parent:
        raise RuntimeError("reviewed migration module is unavailable")
    module_name = f"_archive_reviewed_migration_{id(_MIGRATION_MODULE_TOKEN):x}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("reviewed migration module is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    scripts_path = str(script_path.parent)
    inserted = scripts_path not in sys.path
    if inserted:
        sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
        if Path(str(getattr(module, "__file__", ""))).resolve(strict=True) != script_path:
            raise RuntimeError("reviewed migration module is unavailable")
    finally:
        sys.modules.pop(module_name, None)
        if inserted:
            sys.path.remove(scripts_path)
    return module


def _reviewed_manifest_records(root: Path) -> dict[str, ReviewedManifestRecord]:
    """Return the exact 50 archive rows from the clean stage-zero manifest."""

    module = _load_migration_module()
    try:
        snapshot = module.load_reviewed_manifest_snapshot(
            root, validate_repository=False
        )
    except Exception as exc:
        if isinstance(exc, getattr(module, "MigrationAbort", ())):
            raise RuntimeError("reviewed migration manifest is unavailable") from exc
        raise
    document = snapshot.document
    if document.source_commit != _MANIFEST_SOURCE_COMMIT or len(document.entries) != 132:
        raise RuntimeError("reviewed migration manifest identity differs")
    move_count = 0
    reviewed: dict[str, ReviewedManifestRecord] = {}
    for entry in document.entries:
        disposition = entry.get("disposition")
        if disposition == "move-current":
            move_count += 1
            continue
        if disposition != "archive-unique":
            raise RuntimeError("reviewed migration manifest disposition differs")
        source = _canonical_path(entry.get("source"))
        target = _canonical_path(entry.get("target"), archive_only=True)
        source_blob = entry.get("sourceBlob")
        if (
            source is None
            or target is None
            or target != f"docs/98.archive/{source.removeprefix('docs/')}"
            or not isinstance(source_blob, str)
            or _FULL_OBJECT_ID.fullmatch(source_blob) is None
            or len(source_blob) != len(document.source_commit)
            or target in reviewed
        ):
            raise RuntimeError("reviewed migration manifest archive row differs")
        reviewed[target] = ReviewedManifestRecord(
            target=target,
            original_path=source,
            source_commit=document.source_commit,
            source_blob=source_blob,
        )
    if move_count != 82 or len(reviewed) != 50:
        raise RuntimeError("reviewed migration manifest counts differ")
    return reviewed


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
        replacement = cells[7]
        replacement_valid = replacement == "`null`"
        replacement_link = _INDEX_REPLACEMENT_LINK.fullmatch(replacement)
        if replacement_link is not None:
            replacement_target = posixpath.normpath(
                posixpath.join(
                    posixpath.dirname(ARCHIVE_INDEX.as_posix()),
                    replacement_link.group("target"),
                )
            )
            replacement_valid = (
                _canonical_path(replacement_target) == replacement_target
                and replacement_link.group("label") == replacement_target
                and not PurePosixPath(replacement_target).is_relative_to(ARCHIVE_ROOT)
            )
        if (
            link.group("label") != link.group("target")
            or _canonical_path(path, archive_only=True) is None
            or path in rows
            or not replacement_valid
        ):
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
    try:
        reviewed_manifest = _reviewed_manifest_records(root)
    except (OSError, RuntimeError, TypeError, ValueError):
        reviewed_manifest = {}
        diagnostics.append(
            _diagnostic("ARCHIVE-NAMESPACE-REVIEWED", ARCHIVE_ROOT.as_posix())
        )
    wdtc_paths = frozenset(namespaces.get("wdtc-execution", ()))
    if frozenset(reviewed_manifest) != wdtc_paths:
        diagnostics.append(
            _diagnostic("ARCHIVE-NAMESPACE-REVIEWED", ARCHIVE_ROOT.as_posix())
        )
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
        reviewed = reviewed_manifest.get(record.path)
        if reviewed is not None and (
            parsed.metadata.get("original_path") != reviewed.original_path
            or parsed.metadata.get("source_commit") != reviewed.source_commit
            or parsed.metadata.get("source_blob") != reviewed.source_blob
        ):
            diagnostics.append(_diagnostic("ARCHIVE-NAMESPACE-METADATA", record.path))
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
    record_link_counts = dict(record_report.record_link_counts)
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
        if int(row[-1]) != record_link_counts.get(path, -1):
            diagnostics.append(_diagnostic("ARCHIVE-INDEX-LINKS", path))
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
        reviewed_manifest_records=tuple(
            reviewed_manifest[path] for path in sorted(reviewed_manifest)
        ),
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


def _safe_git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_GRAFT_FILE": os.devnull,
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
        }
    )
    return environment


def _git_command(
    root: Path,
    *args: str,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            [
                "git",
                "--no-replace-objects",
                "--literal-pathspecs",
                "-C",
                str(root),
                *args,
            ],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_safe_git_environment(),
            timeout=_GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ArchiveContractError(
            "RECOVERY-GIT-STARTUP", "bounded Git evidence lookup failed"
        ) from exc


def _repository_identity(root: Path) -> int:
    top = _git_command(root, "rev-parse", "--show-toplevel")
    object_format = _git_command(root, "rev-parse", "--show-object-format")
    try:
        reported = Path(top.stdout.decode("utf-8").strip()).resolve(strict=True)
        format_name = object_format.stdout.decode("ascii", errors="strict")
    except (OSError, RuntimeError, UnicodeDecodeError) as exc:
        raise ArchiveContractError(
            "RECOVERY-REPOSITORY-INVALID", "repository identity is malformed"
        ) from exc
    if top.returncode or reported != root or object_format.returncode:
        raise ArchiveContractError(
            "RECOVERY-REPOSITORY-INVALID", "root must be the Git top level"
        )
    if format_name == "sha1\n":
        return 40
    if format_name == "sha256\n":
        return 64
    raise ArchiveContractError(
        "RECOVERY-OBJECT-FORMAT", "repository object format is unsupported"
    )


def _commit_types(
    root: Path, commits: tuple[str, ...]
) -> dict[str, str | None]:
    if not commits:
        return {}
    result = _git_command(
        root,
        "cat-file",
        "--batch-check",
        input_bytes=("\n".join(commits) + "\n").encode("ascii"),
    )
    if result.returncode:
        raise ArchiveContractError(
            "RECOVERY-OBJECT-MISSING", "commit batch lookup failed"
        )
    lines = result.stdout.splitlines()
    if len(lines) != len(commits):
        raise ArchiveContractError(
            "RECOVERY-OBJECT-MISSING", "commit batch lookup is incomplete"
        )
    kinds: dict[str, str | None] = {}
    for expected, line in zip(commits, lines, strict=True):
        fields = line.split(b" ")
        if len(fields) == 2 and fields[0].decode("ascii", errors="ignore") == expected:
            kinds[expected] = None
            continue
        if len(fields) != 3:
            raise ArchiveContractError(
                "RECOVERY-OBJECT-MISSING", "commit batch lookup is malformed"
            )
        try:
            returned = fields[0].decode("ascii", errors="strict")
            kind = fields[1].decode("ascii", errors="strict")
            int(fields[2])
        except (UnicodeDecodeError, ValueError) as exc:
            raise ArchiveContractError(
                "RECOVERY-OBJECT-MISSING", "commit batch lookup is malformed"
            ) from exc
        if returned != expected:
            raise ArchiveContractError(
                "RECOVERY-OBJECT-MISSING", "commit batch lookup changed identity"
            )
        kinds[expected] = kind
    return kinds


def _commit_tree_members(
    root: Path,
    commit: str,
    paths: tuple[str, ...],
    object_id_length: int,
) -> dict[str, _GitTreeMember]:
    result = _git_command(
        root,
        "ls-tree",
        "-r",
        "-t",
        "-z",
        "--full-tree",
        commit,
        "--",
        *paths,
    )
    if result.returncode:
        raise ArchiveContractError("RECOVERY-TREE-INVALID", "tree lookup failed")
    members: dict[str, _GitTreeMember] = {}
    for raw_record in result.stdout.split(b"\0"):
        if not raw_record:
            continue
        try:
            raw_header, raw_path = raw_record.split(b"\t", 1)
            raw_mode, raw_kind, raw_object = raw_header.split(b" ", 2)
            path = raw_path.decode("utf-8", errors="strict")
            mode = raw_mode.decode("ascii", errors="strict")
            kind = raw_kind.decode("ascii", errors="strict")
            object_id = raw_object.decode("ascii", errors="strict")
        except (UnicodeDecodeError, ValueError) as exc:
            raise ArchiveContractError(
                "RECOVERY-TREE-INVALID", "tree lookup is malformed"
            ) from exc
        if path not in paths:
            continue
        if (
            path in members
            or len(object_id) != object_id_length
            or _FULL_OBJECT_ID.fullmatch(object_id) is None
            or kind not in {"blob", "tree"}
        ):
            raise ArchiveContractError(
                "RECOVERY-TREE-INVALID", "tree lookup is ambiguous"
            )
        members[path] = _GitTreeMember(mode, kind, object_id)
    return members


def _batch_blob_bytes(root: Path, object_ids: tuple[str, ...]) -> dict[str, bytes]:
    if not object_ids:
        return {}
    result = _git_command(
        root,
        "cat-file",
        "--batch",
        input_bytes=("\n".join(object_ids) + "\n").encode("ascii"),
    )
    if result.returncode:
        raise ArchiveContractError("RECOVERY-OBJECT-MISSING", "blob batch failed")
    offset = 0
    blobs: dict[str, bytes] = {}
    for expected in object_ids:
        newline = result.stdout.find(b"\n", offset)
        if newline < 0:
            raise ArchiveContractError(
                "RECOVERY-OBJECT-MISSING", "blob batch is incomplete"
            )
        header = result.stdout[offset:newline].split(b" ")
        if len(header) != 3:
            raise ArchiveContractError(
                "RECOVERY-OBJECT-MISSING", "blob batch header is malformed"
            )
        try:
            returned = header[0].decode("ascii", errors="strict")
            kind = header[1].decode("ascii", errors="strict")
            size = int(header[2])
        except (UnicodeDecodeError, ValueError) as exc:
            raise ArchiveContractError(
                "RECOVERY-OBJECT-MISSING", "blob batch header is malformed"
            ) from exc
        start = newline + 1
        end = start + size
        if (
            returned != expected
            or kind != "blob"
            or size < 0
            or size > _ARCHIVE_RECORD_LIMIT
            or end >= len(result.stdout)
            or result.stdout[end : end + 1] != b"\n"
        ):
            raise ArchiveContractError(
                "RECOVERY-OBJECT-MISSING", "blob batch identity differs"
            )
        payload = result.stdout[start:end]
        try:
            payload.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ArchiveContractError(
                "RECOVERY-NON-UTF8", "source blob is not UTF-8 Markdown"
            ) from exc
        blobs[expected] = payload
        offset = end + 1
    if offset != len(result.stdout):
        raise ArchiveContractError(
            "RECOVERY-OBJECT-MISSING", "blob batch contains trailing output"
        )
    return blobs


def _batch_recover(
    root: Path,
    envelopes: tuple[_PreparedEnvelope, ...],
) -> tuple[
    dict[str, RecoveryResult],
    dict[str, str],
    dict[str, dict[str, _GitTreeMember]],
]:
    recovered: dict[str, RecoveryResult] = {}
    errors: dict[str, str] = {}
    try:
        object_id_length = _repository_identity(root)
    except ArchiveContractError as exc:
        return {}, {item.archive_path: exc.code for item in envelopes}, {}
    valid_by_commit: dict[str, list[_PreparedEnvelope]] = {}
    for item in envelopes:
        if (
            len(item.source_commit) != object_id_length
            or _FULL_OBJECT_ID.fullmatch(item.source_commit) is None
        ):
            errors[item.archive_path] = "RECOVERY-OBJECT-AMBIGUOUS"
        else:
            valid_by_commit.setdefault(item.source_commit, []).append(item)
    commits = tuple(sorted(valid_by_commit))
    try:
        commit_types = _commit_types(root, commits)
    except ArchiveContractError as exc:
        return {}, {item.archive_path: exc.code for item in envelopes}, {}
    trees: dict[str, dict[str, _GitTreeMember]] = {}
    for commit in commits:
        members = valid_by_commit[commit]
        kind = commit_types.get(commit)
        if kind != "commit":
            code = "RECOVERY-OBJECT-MISSING" if kind is None else "RECOVERY-OBJECT-NOT-COMMIT"
            errors.update({item.archive_path: code for item in members})
            continue
        requested = {item.original_path for item in members}
        requested.update(
            link.target.as_posix()
            for item in members
            for link in item.rendered_links
            if link.kind == "local" and link.target is not None
        )
        try:
            trees[commit] = _commit_tree_members(
                root, commit, tuple(sorted(requested)), object_id_length
            )
        except ArchiveContractError as exc:
            errors.update({item.archive_path: exc.code for item in members})
    source_members: dict[str, _GitTreeMember] = {}
    for commit, items in valid_by_commit.items():
        tree = trees.get(commit)
        if tree is None:
            continue
        for item in items:
            member = tree.get(item.original_path)
            if member is None:
                errors[item.archive_path] = "RECOVERY-PATH-MISSING"
            elif member.kind != "blob" or member.mode not in {"100644", "100755"}:
                errors[item.archive_path] = "RECOVERY-OBJECT-NOT-BLOB"
            else:
                source_members[item.archive_path] = member
    try:
        blobs = _batch_blob_bytes(
            root,
            tuple(sorted({member.object_id for member in source_members.values()})),
        )
    except ArchiveContractError as exc:
        errors.update(
            {
                path: exc.code
                for path in source_members
                if path not in errors
            }
        )
        blobs = {}
    for item in envelopes:
        if item.archive_path in errors:
            continue
        member = source_members[item.archive_path]
        source_bytes = blobs.get(member.object_id)
        if source_bytes is None:
            errors[item.archive_path] = "RECOVERY-OBJECT-MISSING"
            continue
        recovered[item.archive_path] = RecoveryResult(
            original_path=item.original_path,
            source_commit=item.source_commit,
            source_blob=member.object_id,
            byte_count=len(source_bytes),
            content_sha256=hashlib.sha256(source_bytes).hexdigest(),
            inline_link_candidate_count=0,
            proposed_archive_path=(
                "docs/98.archive/" + item.original_path.removeprefix("docs/")
            ),
            source_bytes=source_bytes,
        )
    return recovered, errors, trees


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

    prepared_envelopes: list[_PreparedEnvelope] = []
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
            payload_text = parsed.payload.decode("utf-8", errors="strict")
            rendered_links = _validated_rendered_links(payload_text, original_path)
        except Exception:
            diagnostics.append(
                _diagnostic("ARCHIVE-LINK-ADAPTER-FAILURE", archive_path)
            )
            continue
        prepared_envelopes.append(
            _PreparedEnvelope(
                archive_path=archive_path,
                record=record,
                original_path=original_path,
                source_commit=source_commit,
                rendered_links=rendered_links,
            )
        )

    try:
        root = Path(repository_root).resolve(strict=True)
    except (OSError, RuntimeError, TypeError):
        root = Path(repository_root)
    recovered_by_path, recovery_errors, commit_trees = _batch_recover(
        root, tuple(prepared_envelopes)
    )
    for item in prepared_envelopes:
        archive_path = item.archive_path
        error_code = recovery_errors.get(archive_path)
        if error_code is not None:
            diagnostics.append(_diagnostic(error_code, archive_path))
            continue
        recovered = recovered_by_path.get(archive_path)
        if recovered is None:
            diagnostics.append(_diagnostic("RECOVERY-OBJECT-MISSING", archive_path))
            continue
        try:
            parse_archive_envelope(item.record.content, expected=recovered)
        except ArchiveContractError as exc:
            diagnostics.append(_diagnostic(exc.code, archive_path))
            continue
        if archive_path != recovered.proposed_archive_path:
            diagnostics.append(_diagnostic("ARCHIVE-MIRROR-MISMATCH", archive_path))

        record_link_counts[archive_path] = 0
        tree = commit_trees.get(item.source_commit, {})
        for link in item.rendered_links:
            if link.kind in {"external", "anchor"}:
                continue
            historical_link_count += 1
            record_link_counts[archive_path] += 1
            if link.kind != "local" or link.target is None:
                diagnostics.append(
                    _diagnostic("ARCHIVE-HISTORICAL-LINK-INVALID", archive_path)
                )
                continue
            if link.target.as_posix() not in tree:
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
