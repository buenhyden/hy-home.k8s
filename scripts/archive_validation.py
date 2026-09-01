"""Import-only ARWB-002 archive and authority validation interfaces.

The module consumes immutable inputs supplied by its caller.  Historical
existence checks use sanitized literal Git tree lookups; current-authority
checks use passed Markdown/profile data.  It does not activate a registry
route, scan the production archive corpus, or inspect ignored workspace state.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
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
from types import MappingProxyType, ModuleType
from typing import TYPE_CHECKING, Callable, Mapping, Protocol, Sequence

if TYPE_CHECKING:
    from document_contracts import Registry

if __package__:
    from scripts.archive_cutover_manifest import EXPECTED_ARCHIVE_PATHS
    from scripts.document_authority import REGISTRY_PATH
    from scripts.archive_recovery import (
        ArchiveContractError,
        MAX_GIT_BATCH_BYTES,
        MAX_GIT_BATCH_OBJECTS,
        RecoveryResult,
        WP004B_PINNED_MIGRATION_DOCUMENT_SHA256,
        WP004C_SEALED_TARGET_COMMIT,
        WORK107_MIGRATION_DOCUMENT_SHA256,
        WORK107_MIGRATION_PATH,
        _git_capture_bounded,
        _open_parent_at,
        _read_git_blob_batch,
        _read_stream_bounded as _recovery_read_stream_bounded,
        current_named_durable_ref,
        parse_work107_migration_document,
        parse_archive_envelope,
        require_commits_reachable_from_durable_refs,
    )
else:  # Direct import-only execution from scripts/.
    from archive_cutover_manifest import EXPECTED_ARCHIVE_PATHS  # type: ignore[no-redef]
    from document_authority import REGISTRY_PATH
    from archive_recovery import (  # type: ignore[no-redef]
        ArchiveContractError,
        MAX_GIT_BATCH_BYTES,
        MAX_GIT_BATCH_OBJECTS,
        RecoveryResult,
        WP004B_PINNED_MIGRATION_DOCUMENT_SHA256,
        WP004C_SEALED_TARGET_COMMIT,
        WORK107_MIGRATION_DOCUMENT_SHA256,
        WORK107_MIGRATION_PATH,
        _git_capture_bounded,
        _open_parent_at,
        _read_git_blob_batch,
        _read_stream_bounded as _recovery_read_stream_bounded,
        current_named_durable_ref,
        parse_work107_migration_document,
        parse_archive_envelope,
        require_commits_reachable_from_durable_refs,
    )


ARCHIVE_ROOT = PurePosixPath("docs/98.archive")
_UNSET = object()
ARCHIVE_INDEX = ARCHIVE_ROOT / "README.md"
CURRENT_MARKDOWN_MAX_BYTES = 1_000_000
CURRENT_MARKDOWN_TOTAL_BYTES = 32 * 1024 * 1024
CURRENT_MARKDOWN_MAX_FILES = 1024
_INDEX_CAPTURE_MAX_BYTES = 2 * 1024 * 1024
CURRENT_STATUSES = frozenset(
    {"draft", "active", "accepted", "done", "archived", "sealed"}
)
CURRENT_MARKDOWN_PROFILES = frozenset(
    {
        "sdlc/prd",
        "sdlc/srs",
        "sdlc/interface",
        "sdlc/requirement-package",
        "sdlc/ad",
        "sdlc/adr",
        "sdlc/spec",
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
        "content/archive-migration",
        "governance/reference",
        "governance/memory",
        "governance/template-support",
        "governance/progress-ledger",
        "readme/repository",
        "readme/stage-index",
        "readme/collection-index",
        "readme/implementation",
        "readme/audit-pack",
        "readme/data-pack",
        "readme/research-pack",
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


_NAMESPACE_IDS = (
    "arwb-base",
    "acer-additive",
    "wdtc-execution",
    "progress-snapshot",
)
_INDEX_HEADER = (
    "| Archive Record | Original Path | Original Type | Source Commit | Source "
    "Blob | Payload SHA-256 | Historical Links | Current Replacement | Reason |"
)
_INDEX_SEPARATOR = "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |"
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
_ARCHIVE_INDEX_LIMIT = 2 * 1024 * 1024
_GIT_TREE_OUTPUT_LIMIT = 2 * 1024 * 1024
_GIT_TREE_ENTRY_LIMIT = 4096
_MANIFEST_SOURCE_COMMIT = (
    "713dff1fc3de58a2d1682970a7f24faa39c14263"  # pragma: allowlist secret
)
_MIGRATION_MODULE_TOKEN = object()
_WORK109_MIGRATION_PATH = (
    "docs/98.archive/migrations/mig-0002-sdlc-document-and-governance-consolidation.md"
)
_WORK054_WP003_MIGRATION_PATH = (
    "docs/98.archive/migrations/"
    "mig-0003-agent-governance-control-plane-consolidation.md"
)
_WORK054_WP004B_MIGRATION_PATH = (
    "docs/98.archive/migrations/0004-document-authority-convergence.md"
)
MIGRATION_DOCUMENT_MAX_BYTES = 128 * 1024
MIG0002_DOCUMENT_SHA256 = "05527226d8d353f57bac1b346aaa20f1ab1951eeea7f2f570b04dbcabd381265"  # pragma: allowlist secret
MIG0003_DOCUMENT_SHA256 = "6dd85df46123bb7004b0abf0fc7cd1f1d81fcae5ea66f71f1f07ff1dba904ab2"  # pragma: allowlist secret
MIG0004_SPEC0054_LEDGER = (
    "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
)
MIG0004_TERMINAL_SOURCE_COMMIT = (
    "7a770c3c0eabaeda554c4030fc08fb17de164fe5"  # pragma: allowlist secret
)
MIG0004_ROW_COUNT = 101
MIG0004_STAGE99_ACTION_TARGETS = {
    "docs/99.templates/contracts/registry-form.schema.json": (
        "replaced",
        "docs/99.templates/contracts/document-profile.schema.json",
    ),
    "docs/99.templates/contracts/route-contract.json": (
        "replaced",
        "docs/99.templates/registry.json",
    ),
    "docs/99.templates/contracts/route-contract.schema.json": (
        "replaced",
        "docs/99.templates/registry.json",
    ),
    "docs/99.templates/support/README.md": (
        "replaced",
        "docs/99.templates/README.md",
    ),
    "docs/99.templates/support/document-contract.md": (
        "replaced",
        "docs/99.templates/README.md",
    ),
    "docs/99.templates/support/document-lifecycle.md": (
        "replaced",
        "docs/99.templates/README.md",
    ),
    "docs/99.templates/support/document-profiles.json": (
        "replaced",
        "docs/99.templates/registry.json",
    ),
    "docs/99.templates/templates/README.md": (
        "replaced",
        "docs/99.templates/README.md",
    ),
    "docs/99.templates/templates/common/archive-migration.template.md": (
        "moved",
        "docs/99.templates/templates/archive/archive-migration.template.md",
    ),
    "docs/99.templates/templates/common/archive-record.template.md": (
        "moved",
        "docs/99.templates/templates/archive/archive-record.template.md",
    ),
    "docs/99.templates/templates/common/governance-reference.template.md": (
        "moved",
        "docs/99.templates/templates/governance/governance-reference.template.md",
    ),
    "docs/99.templates/templates/common/memory.template.md": (
        "moved",
        "docs/99.templates/templates/governance/memory.template.md",
    ),
    "docs/99.templates/templates/common/progress.template.md": (
        "moved",
        "docs/99.templates/templates/governance/progress.template.md",
    ),
    "docs/99.templates/templates/common/reference.template.md": (
        "moved",
        "docs/99.templates/templates/references/reference.template.md",
    ),
    "docs/99.templates/templates/common/template-support.template.md": (
        "replaced",
        "docs/99.templates/README.md",
    ),
    "docs/99.templates/templates/sdlc/architecture/ad.template.md": (
        "replaced",
        "docs/99.templates/templates/architecture/ad.template.md",
    ),
    "docs/99.templates/templates/sdlc/architecture/adr.template.md": (
        "replaced",
        "docs/99.templates/templates/architecture/adr.template.md",
    ),
    "docs/99.templates/templates/sdlc/execution/plan.template.md": (
        "moved",
        "docs/99.templates/templates/specs/plan.template.md",
    ),
    "docs/99.templates/templates/sdlc/execution/task.template.md": (
        "moved",
        "docs/99.templates/templates/specs/task.template.md",
    ),
    "docs/99.templates/templates/sdlc/operations/guide.template.md": (
        "moved",
        "docs/99.templates/templates/operations/guide.template.md",
    ),
    "docs/99.templates/templates/sdlc/operations/incident.template.md": (
        "replaced",
        "docs/99.templates/templates/operations/incident.template.md",
    ),
    "docs/99.templates/templates/sdlc/operations/policy.template.md": (
        "moved",
        "docs/99.templates/templates/operations/policy.template.md",
    ),
    "docs/99.templates/templates/sdlc/operations/postmortem.template.md": (
        "moved",
        "docs/99.templates/templates/operations/postmortem.template.md",
    ),
    "docs/99.templates/templates/sdlc/operations/runbook.template.md": (
        "moved",
        "docs/99.templates/templates/operations/runbook.template.md",
    ),
    "docs/99.templates/templates/sdlc/requirements/interface.template.md": (
        "replaced",
        "docs/99.templates/templates/requirements/requirement-package.template.md",
    ),
    "docs/99.templates/templates/sdlc/requirements/prd.template.md": (
        "replaced",
        "docs/99.templates/templates/requirements/requirement-package.template.md",
    ),
    "docs/99.templates/templates/sdlc/requirements/srs.template.md": (
        "replaced",
        "docs/99.templates/templates/requirements/requirement-package.template.md",
    ),
    "docs/99.templates/templates/sdlc/specs/agent-design.template.md": (
        "replaced",
        "docs/99.templates/templates/specs/spec.template.md",
    ),
    "docs/99.templates/templates/sdlc/specs/data-model.template.md": (
        "replaced",
        "docs/99.templates/templates/specs/data-model.template.md",
    ),
    "docs/99.templates/templates/sdlc/specs/openapi.template.yaml": (
        "moved",
        "docs/99.templates/templates/specs/openapi.template.yaml",
    ),
    "docs/99.templates/templates/sdlc/specs/schema.template.graphql": (
        "moved",
        "docs/99.templates/templates/specs/schema.template.graphql",
    ),
    "docs/99.templates/templates/sdlc/specs/service.template.proto": (
        "moved",
        "docs/99.templates/templates/specs/service.template.proto",
    ),
    "docs/99.templates/templates/sdlc/specs/spec.template.md": (
        "replaced",
        "docs/99.templates/templates/specs/spec.template.md",
    ),
    "docs/99.templates/templates/sdlc/specs/tests.template.md": (
        "replaced",
        "docs/99.templates/templates/specs/spec.template.md",
    ),
}
_MIGRATION_LEDGER_PREFIX = (
    b"<!-- archive-migration-ledger:v1 format=json -->\n\n```json\n"
)
_ARCHIVE_MIGRATION_CONTROLS = {
    WORK107_MIGRATION_PATH: (
        "MIG-0001",
        93,
        {"moved": 93},
        "1a2f3264c380f93d435fedf4028a3fb2b843da377e99e2fd4b788dd37df45116",  # pragma: allowlist secret -- sealed migration digest
    ),
    _WORK109_MIGRATION_PATH: (
        "MIG-0002",
        154,
        {"moved": 141, "replaced": 3, "merged": 10},
        MIG0002_DOCUMENT_SHA256,
    ),
    _WORK054_WP003_MIGRATION_PATH: (
        "MIG-0003",
        3,
        {"merged": 3},
        MIG0003_DOCUMENT_SHA256,
    ),
    _WORK054_WP004B_MIGRATION_PATH: (
        "MIG-0004",
        101,
        {"merged": 2, "moved": 23, "replaced": 76},
        WP004B_PINNED_MIGRATION_DOCUMENT_SHA256,
    ),
}
_MIGRATION_FRONTMATTER_KEYS = (
    "title",
    "type",
    "status",
    "owner",
    "updated",
    "artifact_id",
)

# Reviewed pre-cutover bytes of each pinned control. The retired `migration_id`
# frontmatter key repeated `artifact_id`, so a control committed before that
# retirement still parses -- against the legacy key tuple and only at these exact
# digests. Any other byte string is rejected as before.
_MIGRATION_LEGACY_BASE_SHA256 = {
    WORK107_MIGRATION_PATH: "4e62cb6ba2a394cd9ae546543c85a58c8f105cb5d1ff48cfd8dab8b8b1082206",  # pragma: allowlist secret -- pre-cutover digest
    _WORK109_MIGRATION_PATH: "67032c0b86acbee04a1e713053d164df2e99f4486df79df5161d53975fb82a7a",  # pragma: allowlist secret -- pre-cutover digest
    _WORK054_WP003_MIGRATION_PATH: "51fe8d35febac457e562f997a711ce152a98cda67b3aec2ccd8ed08bd3ac3d42",  # pragma: allowlist secret -- pre-cutover digest
    _WORK054_WP004B_MIGRATION_PATH: "503a65a5897301be651217fcc48def5351809f272d9af510f10621f2ec2d1fe6",  # pragma: allowlist secret -- pre-cutover digest
}
_LEGACY_MIGRATION_FRONTMATTER_KEYS = _MIGRATION_FRONTMATTER_KEYS + ("migration_id",)


_GENERIC_MIGRATION_PATH = re.compile(
    r"docs/98\.archive/migrations/(?P<number>[0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z"
)
_MIGRATION_ROW_FIELDS = (
    "legacy_path",
    "stable_path",
    "artifact_id",
    "action",
    "replacement",
    "source_commit",
    "source_blob",
    "content_sha256",
    "reason",
)
_CONSUMER_PREFIX = b"<!-- archive-historical-consumers:v1 format=json -->\n\n```json\n"
_HISTORICAL_REFERENCE_PREFIX = (
    b"<!-- archive-historical-reference-evidence:v1 format=json -->\n\n```json\n"
)
_HISTORICAL_REFERENCE_MARKER = b"<!-- archive-historical-reference-evidence:"


@dataclass(frozen=True)
class MigrationDisposition:
    """One source identity and immediate disposition proved by a sealed record."""

    record_path: str
    source_commit: str
    source_blob: str
    source_bytes: bytes
    action: str
    target: str


@dataclass(frozen=True)
class MigrationDeclaration:
    """Validated path fields, separated from prose that still needs consumer checks."""

    source_bytes: bytes = field(repr=False)
    path_dispositions: Mapping[str, str]
    remaining_text: str = field(repr=False)


@dataclass(frozen=True)
class HistoricalReferenceDisposition:
    """A consumer-scoped historical reference, deliberately outside recovery."""

    kind: str
    terminal_path: str


@dataclass(frozen=True)
class MigrationProof:
    """Validated dispositions and exact historical consumer bytes, never a waiver."""

    targets: Mapping[str, str]
    consumers: Mapping[str, bytes]
    records: Mapping[str, str] = field(default_factory=dict)
    dispositions: Mapping[str, MigrationDisposition] = field(default_factory=dict)
    proposed_registry: Registry | None = None
    declarations: Mapping[str, MigrationDeclaration] = field(default_factory=dict)
    references: Mapping[tuple[str, str], HistoricalReferenceDisposition] = field(
        default_factory=dict
    )


def generic_migration_id(path: str) -> str | None:
    match = _GENERIC_MIGRATION_PATH.fullmatch(path)
    if match is None or int(match["number"]) < 5:
        return None
    return f"MIG-{match['number']}"


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _migration_json_block(content: bytes, marker: bytes) -> tuple[object, int, int]:
    if content.count(marker) != 1:
        raise ValueError("migration marker is not unique")
    before, _marker, remainder = content.partition(marker)
    raw, fence, _after = remainder.partition(b"\n```\n")
    if not fence:
        raise ValueError("migration JSON fence is absent")
    parsed = json.loads(
        raw.decode("utf-8", errors="strict"), object_pairs_hook=_unique_json_object
    )
    start = len(before) + len(marker)
    return parsed, start, start + len(raw)


def _migration_json(content: bytes, marker: bytes) -> object:
    return _migration_json_block(content, marker)[0]


def _historical_reference_rows(content: bytes) -> tuple[dict[str, object], ...]:
    """Read the optional closed evidence block without changing the public parser."""

    if _HISTORICAL_REFERENCE_MARKER not in content:
        return ()
    if (
        content.count(_HISTORICAL_REFERENCE_MARKER) != 1
        or content.count(_HISTORICAL_REFERENCE_PREFIX) != 1
    ):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "historical reference marker differs"
        )
    try:
        rows = _migration_json(content, _HISTORICAL_REFERENCE_PREFIX)
        if type(rows) is not list or any(type(row) is not dict for row in rows):
            raise ValueError
        if len(rows) > MAX_GIT_BATCH_OBJECTS:
            raise ArchiveContractError(
                "RECOVERY-RESOURCE-LIMIT", "historical reference budget differs"
            )
    except ArchiveContractError:
        raise
    except (ValueError, UnicodeError, TypeError) as exc:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "historical reference evidence differs"
        ) from exc
    return tuple(rows)


def project_migration_declaration_fields(
    content: bytes, targets: Mapping[str, str]
) -> MigrationDeclaration:
    """Project typed fields, not proof; publish only after the owner's full validation."""

    rows, start, end = _migration_json_block(content, _MIGRATION_LEDGER_PREFIX)
    path_fields = {
        "legacy_path",
        "stable_path",
        "replacement",
        "consumer_path",
        "lookup_path",
    }
    dispositions = {
        value: targets.get(value, value)
        for row in rows
        for key, value in row.items()
        if key in path_fields and isinstance(value, str)
    }
    remaining_rows = [
        {key: value for key, value in row.items() if key not in path_fields}
        for row in rows
    ]
    remaining_bytes = (
        content[:start]
        + json.dumps(remaining_rows, ensure_ascii=False).encode("utf-8")
        + content[end:]
    )
    if _HISTORICAL_REFERENCE_PREFIX in remaining_bytes:
        reference_rows, reference_start, reference_end = _migration_json_block(
            remaining_bytes, _HISTORICAL_REFERENCE_PREFIX
        )
        if type(reference_rows) is list:
            dispositions.update(
                {
                    value: targets.get(value, value)
                    for row in reference_rows
                    if type(row) is dict
                    for key, value in row.items()
                    if key in path_fields and isinstance(value, str)
                }
            )
            remaining_rows = [
                {key: value for key, value in row.items() if key not in path_fields}
                if type(row) is dict
                else row
                for row in reference_rows
            ]
            remaining_bytes = (
                remaining_bytes[:reference_start]
                + json.dumps(remaining_rows, ensure_ascii=False).encode("utf-8")
                + remaining_bytes[reference_end:]
            )
    return MigrationDeclaration(
        content,
        MappingProxyType(dispositions),
        remaining_bytes.decode("utf-8", errors="strict"),
    )


def is_sealed_migration(content: bytes) -> bool:
    """Report whether a discovered migration document is sealed evidence.

    document_lifecycle admits a migration only in `draft`, so every migration
    exists as a draft before it is sealed.  Rejecting a draft here would break
    the recovery proof for the whole repository between those two changes, which
    makes it impossible to open a migration in a green commit.  A draft is not
    yet evidence, so it is skipped rather than refused; `LIFECYCLE-DELETE` still
    reads only sealed rows, so nothing is admitted early.
    """

    try:
        _, metadata, _ = _load_canonical_markdown_module().extract_frontmatter(
            content.decode("utf-8", errors="strict")
        )
    except (ValueError, UnicodeError, KeyError, TypeError):
        return True
    return metadata.get("status") == "sealed"


def parse_migration_control(
    path: str, content: bytes
) -> tuple[tuple[dict[str, object], ...], tuple[dict[str, object], ...]]:
    """Parse recovery-specific sealed identity and ledgers, not document-form policy."""

    try:
        identity = generic_migration_id(path)
        if (
            identity is None
            or type(content) is not bytes
            or len(content) > MIGRATION_DOCUMENT_MAX_BYTES
        ):
            raise ValueError
        _, metadata, _ = _load_canonical_markdown_module().extract_frontmatter(
            content.decode("utf-8", errors="strict")
        )
        if (
            metadata.get("status") != "sealed"
            or metadata.get("artifact_id") != identity
        ):
            raise ValueError
        rows = _migration_json(content, _MIGRATION_LEDGER_PREFIX)
        consumers = _migration_json(content, _CONSUMER_PREFIX)
        if (
            type(rows) is not list
            or not rows
            or len(rows) > _GIT_TREE_ENTRY_LIMIT
            or type(consumers) is not list
            or len(consumers) > MAX_GIT_BATCH_OBJECTS
            or any(type(row) is not dict for row in [*rows, *consumers])
        ):
            raise ValueError
    except (ValueError, UnicodeError, KeyError, TypeError) as exc:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "migration profile differs"
        ) from exc
    return tuple(rows), tuple(consumers)


def compose_migration_targets(
    projections: Sequence[Mapping[str, str]],
) -> dict[str, str]:
    """Compose reviewed edges without allowing a competing successor or cycle."""

    edges: dict[str, str] = {}
    for projection in projections:
        for source, target in projection.items():
            if _canonical_path(source) != source or _canonical_path(target) != target:
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-TARGET", "noncanonical migration edge"
                )
            if source in edges and edges[source] != target:
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-CONFLICT", "competing successors"
                )
            edges[source] = target
    result: dict[str, str] = {}
    for source, target in edges.items():
        seen = {source}
        while target in edges and edges[target] != target:
            if target in seen:
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-CYCLE", "migration graph cycles"
                )
            seen.add(target)
            target = edges[target]
        result[source] = target
    return result


def _regular_source_bytes(
    root: Path,
    requests: Mapping[str, tuple[str, ...]],
    *,
    proposed_commit: str | None = None,
) -> dict[tuple[str, str], tuple[str, bytes]]:
    """Prove immutable commit, durable reachability, mode, bounded bytes and UTF-8."""

    length = _repository_identity(root)
    if not requests or len(requests) > MAX_GIT_BATCH_OBJECTS:
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "source commit budget differs"
        )
    commits = tuple(sorted(requests))
    if any(
        not isinstance(commit, str)
        or len(commit) != length
        or _FULL_OBJECT_ID.fullmatch(commit) is None
        for commit in commits
    ):
        raise ArchiveContractError(
            "RECOVERY-OBJECT-AMBIGUOUS", "source commit identity differs"
        )
    if any(kind != "commit" for kind in _commit_types(root, commits).values()):
        raise ArchiveContractError(
            "RECOVERY-OBJECT-NOT-COMMIT", "source is not a commit"
        )
    if proposed_commit is None:
        _require_commits_reachable(root, commits)
    else:
        _require_proposal_recovery_ancestry(root, commits, proposed_commit)
    members: dict[tuple[str, str], _GitTreeMember] = {}
    for commit, paths in requests.items():
        if len(paths) > _GIT_TREE_ENTRY_LIMIT or any(
            _canonical_path(path) != path for path in paths
        ):
            raise ArchiveContractError("RECOVERY-MIGRATION-ROW", "source path differs")
        found = _commit_tree_members(
            root,
            commit,
            original_paths=paths,
            historical_paths=(),
            object_id_length=length,
        )
        for path in paths:
            member = found.get(path)
            if (
                member is None
                or member.kind != "blob"
                or member.mode not in {"100644", "100755"}
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-BLOB", "source is not a regular Git blob"
                )
            members[commit, path] = member
    blobs = _batch_blob_bytes(
        root, tuple(sorted({member.object_id for member in members.values()}))
    )
    return {
        key: (member.object_id, blobs[member.object_id])
        for key, member in members.items()
    }


def _historical_view_source(
    root: Path,
    *,
    commit: str,
    path: str,
    blob: str,
    target: str,
    proposed_commit: str | None,
) -> None:
    """Prove one Git symlink view without widening regular-source admission."""

    length = _repository_identity(root)
    if (
        _canonical_path(path) != path
        or not isinstance(target, str)
        or not target
        or PurePosixPath(target).is_absolute()
        or len(commit) != length
        or len(blob) != length
        or _FULL_OBJECT_ID.fullmatch(commit) is None
        or _FULL_OBJECT_ID.fullmatch(blob) is None
    ):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "view identity differs"
        )
    if any(part in {"", "."} for part in PurePosixPath(target).parts):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "view target differs"
        )
    resolved = PurePosixPath(path).parent
    for part in PurePosixPath(target).parts:
        if part == "..":
            if resolved == PurePosixPath("."):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-REFERENCE", "view target escapes repository"
                )
            resolved = resolved.parent
        else:
            resolved /= part
    if _canonical_path(resolved.as_posix()) != resolved.as_posix():
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "view target differs"
        )
    if _commit_types(root, (commit,)).get(commit) != "commit":
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "view source is not a commit"
        )
    if proposed_commit is None:
        _require_commits_reachable(root, (commit,))
    else:
        _require_proposal_recovery_ancestry(root, (commit,), proposed_commit)
    member = _commit_tree_members(
        root,
        commit,
        original_paths=(path,),
        historical_paths=(),
        object_id_length=length,
    ).get(path)
    if (
        member is None
        or member.kind != "blob"
        or member.mode != "120000"
        or member.object_id != blob
    ):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "view source differs"
        )
    try:
        content = _batch_blob_bytes(root, (blob,))[blob].decode(
            "utf-8", errors="strict"
        )
    except UnicodeError as exc:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "view source is not UTF-8"
        ) from exc
    if content != target:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "view target differs"
        )


def _migration_input_options(
    registry: Registry | None,
    raw_schema: object,
    read_current_bytes: Callable[[str, int], bytes] | None,
) -> dict[str, object]:
    """Require a complete held mode without passing our sentinel to another owner."""

    if raw_schema is _UNSET and read_current_bytes is None:
        return {}
    _load_canonical_markdown_module()
    from document_contracts import Registry

    if (
        not isinstance(registry, Registry)
        or not isinstance(raw_schema, dict)
        or not callable(read_current_bytes)
    ):
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "held migration inputs are incomplete"
        )
    return {"raw_schema": raw_schema, "read_current_bytes": read_current_bytes}


def _migration_current_bytes(
    root: Path,
    path: str,
    max_bytes: int,
    read_current_bytes: Callable[[str, int], bytes] | None,
) -> bytes:
    if read_current_bytes is None:
        return read_worktree_regular_bounded(root, path, max_bytes=max_bytes)
    content = read_current_bytes(path, max_bytes)
    if type(content) is not bytes or len(content) > max_bytes:
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "held current bytes are invalid or oversized"
        )
    return content


def _exact_historical_path_occurs(content: bytes, path: str) -> bool:
    encoded = path.encode("utf-8")
    start = 0
    while (found := content.find(encoded, start)) >= 0:
        end = found + len(encoded)
        bare = (found == 0 or content[found - 1] in b" \t\r\n") and (
            end == len(content) or content[end] in b" \t\r\n"
        )
        quoted = (
            found > 0
            and end < len(content)
            and content[found - 1] in b"`'\""
            and content[end] == content[found - 1]
            and (found == 1 or content[found - 2] in b" \t\r\n")
            and (
                end + 1 == len(content)
                or content[end + 1] in b" \t\r\n"
                or (
                    content[end + 1] == ord(",")
                    and (end + 2 == len(content) or content[end + 2] in b" \t\r\n")
                )
            )
        )
        if bare or quoted:
            return True
        start = found + 1
    return False


def _pinned_mig0003_targets(
    root: Path,
    *,
    proposed_commit: str | None,
    read_current_bytes: Callable[[str, int], bytes] | None,
) -> dict[str, str]:
    """Expose only the already sealed MIG-0003 edges for literal composition."""

    path = _WORK054_WP003_MIGRATION_PATH
    if proposed_commit is None:
        try:
            content = read_staged_blob_bounded(root, path)
        except ArchiveContractError:
            return {}
        if content != _migration_current_bytes(
            root, path, MIGRATION_DOCUMENT_MAX_BYTES, read_current_bytes
        ):
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-STAGED-DRIFT", "MIG-0003 index/worktree differ"
            )
    else:
        member = _proposal_members(root, proposed_commit, (path,)).get(path)
        if (
            member is None
            or member.kind != "blob"
            or member.mode not in {"100644", "100755"}
        ):
            return {}
        content = _batch_blob_bytes(root, (member.object_id,))[member.object_id]
    rows = validate_pinned_migration_recovery(root, path, content)
    targets: dict[str, str] = {}
    for row in rows:
        legacy, replacement = row.get("legacy_path"), row.get("replacement")
        if not isinstance(legacy, str) or not isinstance(replacement, str):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-REFERENCE", "MIG-0003 row differs"
            )
        targets[legacy] = replacement
    return targets


def _staged_path_is_present(root: Path, path: str) -> bool:
    """Check one literal index entry without accepting its mode or contents."""

    result = _git_command(
        root, "ls-files", "-s", "--", path, output_limit=_INDEX_CAPTURE_MAX_BYTES
    )
    if result.returncode:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "index lookup failed"
        )
    if not result.stdout:
        return False
    expected = b"\t" + path.encode("utf-8") + b"\n"
    lines = result.stdout.splitlines(keepends=True)
    if len(lines) != 1 or not lines[0].endswith(expected):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-REFERENCE", "index lookup differs"
        )
    return True


def validate_migration_records(
    repository_root: str | Path,
    records: Mapping[str, bytes],
    *,
    proposed_commit: str | None = None,
    registry: Registry | None = None,
    raw_schema: object = _UNSET,
    read_current_bytes: Callable[[str, int], bytes] | None = None,
) -> MigrationProof:
    """One owner for future migration rows, source proofs, consumers and current targets."""

    root = Path(repository_root).resolve(strict=True)
    input_options = _migration_input_options(registry, raw_schema, read_current_bytes)
    rows: list[dict[str, object]] = []
    consumer_commits: dict[str, str] = {}
    identities: set[str] = set()
    record_ids: dict[str, str] = {}
    row_records: dict[str, str] = {}
    reference_rows: list[dict[str, object]] = []
    if any(
        not isinstance(path, str) or type(content) is not bytes
        for path, content in records.items()
    ):
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "migration input differs"
        )
    if (
        len(records) > MAX_GIT_BATCH_OBJECTS
        or sum(map(len, records.values())) > MAX_GIT_BATCH_BYTES
    ):
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "migration record budget differs"
        )
    document_owner = _load_canonical_markdown_module()
    try:
        if records:
            if registry is None:
                registry = document_owner.load_registry(root)
            snapshot_registry = _proposed_migration_registry(
                root, proposed_commit, registry, **input_options
            )
        else:
            snapshot_registry = registry
    except ArchiveContractError:
        raise
    except (ValueError, OSError) as exc:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "migration registry differs"
        ) from exc
    for path, content in sorted(records.items()):
        identity = generic_migration_id(path)
        if identity is None or identity in identities:
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-PROFILE", "migration identity is not unique"
            )
        identities.add(identity)
        record_ids[path] = identity
        entries, groups = parse_migration_control(path, content)
        reference_rows.extend(_historical_reference_rows(content))
        if proposed_commit is not None:
            members = _proposal_members(root, proposed_commit, (path,))
            member = members.get(path)
            if (
                member is None
                or member.mode not in {"100644", "100755"}
                or member.kind != "blob"
            ):
                raise ArchiveContractError(
                    "ARCHIVE-MIGRATION-PROFILE",
                    "migration is not a regular proposed blob",
                )
            if (
                _batch_blob_bytes(root, (member.object_id,))[member.object_id]
                != content
            ):
                raise ArchiveContractError(
                    "ARCHIVE-MIGRATION-PROFILE", "migration proposed bytes differ"
                )
        elif (
            read_staged_blob_bounded(root, path) != content
            or _migration_current_bytes(
                root, path, MIGRATION_DOCUMENT_MAX_BYTES, read_current_bytes
            )
            != content
        ):
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-STAGED-DRIFT", "migration index/worktree differ"
            )
        try:
            profile = document_owner.classify_path(registry, PurePosixPath(path))
            snapshot_profile = document_owner.classify_path(
                snapshot_registry, PurePosixPath(path)
            )
            if (
                profile.profile_id != "content/archive-migration"
                or snapshot_profile.profile_id != profile.profile_id
                or snapshot_profile.mode != profile.mode
                or snapshot_profile.lifecycle_domain != profile.lifecycle_domain
                or document_owner.validate_document_text(
                    content.decode("utf-8", errors="strict"),
                    PurePosixPath(path),
                    profile,
                    "strict",
                )
                or document_owner.validate_document_text(
                    content.decode("utf-8", errors="strict"),
                    PurePosixPath(path),
                    snapshot_profile,
                    "strict",
                )
            ):
                raise ValueError
        except (ValueError, OSError) as exc:
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-PROFILE", "migration document form differs"
            ) from exc
        if proposed_commit is None and (
            _migration_current_bytes(
                root, path, MIGRATION_DOCUMENT_MAX_BYTES, read_current_bytes
            )
            != content
        ):
            raise ArchiveContractError(
                "ARCHIVE-MIGRATION-STAGED-DRIFT",
                "migration changed during document validation",
            )
        rows.extend(entries)
        for entry in entries:
            source = entry.get("legacy_path")
            if isinstance(source, str):
                row_records[source] = path
        for group in groups:
            paths, commit = group.get("paths"), group.get("source_commit")
            if (
                set(group) != {"source_commit", "paths"}
                or not isinstance(commit, str)
                or type(paths) is not list
                or not paths
                or len(paths) > _GIT_TREE_ENTRY_LIMIT
                or any(
                    not isinstance(path, str) or _canonical_path(path) != path
                    for path in paths
                )
                or paths != sorted(set(paths))
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-CONSUMER", "consumer set differs"
                )
            for consumer in paths:
                if consumer in consumer_commits:
                    raise ArchiveContractError(
                        "RECOVERY-MIGRATION-CONSUMER", "consumer identity is ambiguous"
                    )
                consumer_commits[consumer] = commit
    if len(reference_rows) > MAX_GIT_BATCH_OBJECTS:
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "historical reference budget differs"
        )
    edges: dict[str, str] = {}
    requests: dict[str, set[str]] = {}
    moved_targets: set[str] = set()
    artifacts: set[str] = set()
    for row in rows:
        source, action = row.get("legacy_path"), row.get("action")
        target = row.get("stable_path") if action == "moved" else row.get("replacement")
        if (
            tuple(row) != _MIGRATION_ROW_FIELDS
            or not isinstance(source, str)
            or _canonical_path(source) != source
            or source in edges
            or not isinstance(action, str)
            or action not in {"moved", "merged", "replaced", "deleted"}
            or (
                action != "moved"
                and (row["stable_path"] is not None or row["artifact_id"] is not None)
            )
            or (action == "moved" and row["replacement"] is not None)
            or (
                row["artifact_id"] is not None
                and (
                    not isinstance(row["artifact_id"], str)
                    or re.fullmatch(
                        r"[A-Z]+-[0-9]{4}(?:-[0-9]{4})?", row["artifact_id"]
                    )
                    is None
                )
            )
            or (action == "deleted" and target is not None)
            or (
                action != "deleted"
                and (not isinstance(target, str) or _canonical_path(target) != target)
            )
            or not isinstance(row["reason"], str)
            or not row["reason"].strip()
            or not isinstance(row["source_commit"], str)
            or not isinstance(row["source_blob"], str)
            or _FULL_OBJECT_ID.fullmatch(row["source_blob"]) is None
            or not isinstance(row["content_sha256"], str)
            or re.fullmatch(r"[0-9a-f]{64}", row["content_sha256"]) is None
        ):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-ROW", "migration row differs"
            )
        if action == "moved":
            if target in moved_targets or (
                row["artifact_id"] is not None and row["artifact_id"] in artifacts
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-CONFLICT",
                    "move target or artifact is not unique",
                )
            moved_targets.add(str(target))
            if row["artifact_id"] is not None:
                artifacts.add(str(row["artifact_id"]))
        edges[source] = ARCHIVE_INDEX.as_posix() if action == "deleted" else str(target)
        requests.setdefault(str(row["source_commit"]), set()).add(source)
    for path, commit in consumer_commits.items():
        requests.setdefault(commit, set()).add(path)
    if not rows:
        return MigrationProof({}, {})
    sources = _regular_source_bytes(
        root,
        {commit: tuple(sorted(paths)) for commit, paths in requests.items()},
        proposed_commit=proposed_commit,
    )
    for row in rows:
        blob, content = sources[str(row["source_commit"]), str(row["legacy_path"])]
        if (
            blob != row["source_blob"]
            or hashlib.sha256(content).hexdigest() != row["content_sha256"]
        ):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-CONTENT", "source identity differs"
            )
    targets = compose_migration_targets((edges,))
    pinned_targets: dict[str, str] | None = None
    references: dict[tuple[str, str], HistoricalReferenceDisposition] = {}
    view_sources: set[str] = set()
    view_identities: dict[str, tuple[str, str, str, str, str]] = {}
    lookup_paths: set[str] = set()
    reference_terminals: set[str] = set()
    for evidence in reference_rows:
        kind = evidence.get("kind")
        consumer = evidence.get("consumer_path")
        legacy = evidence.get("legacy_path")
        if (
            not isinstance(kind, str)
            or not isinstance(consumer, str)
            or not isinstance(legacy, str)
            or _canonical_path(consumer) != consumer
            or _canonical_path(legacy) != legacy
            or consumer not in consumer_commits
            or (consumer, legacy) in references
        ):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-REFERENCE", "historical reference differs"
            )
        if kind == "literal-path":
            if set(evidence) != {"kind", "consumer_path", "legacy_path"}:
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-REFERENCE", "literal reference shape differs"
                )
            terminal = targets.get(legacy)
            if terminal is None:
                if pinned_targets is None:
                    pinned_targets = _pinned_mig0003_targets(
                        root,
                        proposed_commit=proposed_commit,
                        read_current_bytes=read_current_bytes,
                    )
                terminal = compose_migration_targets((pinned_targets, edges)).get(
                    legacy
                )
            if terminal is None or terminal == legacy:
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-REFERENCE", "literal disposition differs"
                )
            references[consumer, legacy] = HistoricalReferenceDisposition(
                kind, terminal
            )
            reference_terminals.add(terminal)
        elif kind == "symlink-view":
            expected = {
                "kind",
                "consumer_path",
                "legacy_path",
                "source_commit",
                "source_mode",
                "source_blob",
                "link_target",
                "lookup_path",
            }
            if set(evidence) != expected or evidence.get("source_mode") != "120000":
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-REFERENCE", "view reference shape differs"
                )
            commit, blob, target, lookup = (
                evidence.get("source_commit"),
                evidence.get("source_blob"),
                evidence.get("link_target"),
                evidence.get("lookup_path"),
            )
            identity = (commit, "120000", blob, target, lookup)
            if (
                not all(
                    isinstance(value, str) for value in (commit, blob, target, lookup)
                )
                or lookup != ARCHIVE_INDEX.as_posix()
                or legacy in edges
                or (legacy in view_identities and view_identities[legacy] != identity)
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-REFERENCE", "view reference differs"
                )
            _historical_view_source(
                root,
                commit=commit,
                path=legacy,
                blob=blob,
                target=target,
                proposed_commit=proposed_commit,
            )
            view_sources.add(legacy)
            view_identities.setdefault(legacy, identity)
            lookup_paths.add(lookup)
            references[consumer, legacy] = HistoricalReferenceDisposition(kind, lookup)
        else:
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-REFERENCE", "reference kind differs"
            )
    selected = set(targets.values()) | lookup_paths | reference_terminals
    paths = tuple(sorted(selected | set(edges)))
    if proposed_commit is None:
        inventory = _staged_regular_blob_inventory(root, paths=paths)
        present = set(inventory)
    else:
        members = _proposal_members(root, proposed_commit, paths)
        present = set(members)
        inventory = {
            path: member.object_id
            for path, member in members.items()
            if member.kind == "blob" and member.mode in {"100644", "100755"}
        }
    # Historical consumer bytes and their reference occurrence are proven from
    # the reviewed source commit below. Current consumers belong to the active
    # document validators and may evolve or disappear independently of Archive.
    target_contents: dict[str, bytes] = {}
    historical_targets: dict[str, _GitTreeMember] = {}
    ordered = sorted(selected)
    for path in ordered:
        if path in present:
            _require_regular_current_target(path, inventory)
        elif proposed_commit is None and os.path.lexists(root / path):
            _require_regular_current_target(path, inventory)
        else:
            historical_targets[path] = _reachable_historical_regular_target(
                root,
                path,
                proposed_commit=proposed_commit,
            )
    # One batch for the whole selection: a ledger names as many targets as it
    # has rows, and a subprocess per row spends the run's budget on process
    # startup rather than on reading.
    expected_blobs = _batch_blob_bytes(
        root,
        tuple(
            sorted(
                {
                    inventory[path]
                    if path in inventory
                    else historical_targets[path].object_id
                    for path in ordered
                }
            )
        ),
    )
    for path in ordered:
        object_id = (
            inventory[path]
            if path in inventory
            else historical_targets[path].object_id
        )
        expected = expected_blobs[object_id]
        if path in inventory:
            content = (
                expected
                if proposed_commit is not None
                else _migration_current_bytes(
                    root, path, CURRENT_MARKDOWN_MAX_BYTES, read_current_bytes
                )
            )
            if expected != content:
                raise ArchiveContractError(
                    "ARCHIVE-MIGRATION-STAGED-DRIFT",
                    "target or consumer index/worktree differ",
                )
        else:
            content = expected
        target_contents[path] = content
    for legacy in view_sources:
        if proposed_commit is None:
            present_view = _staged_path_is_present(root, legacy) or os.path.lexists(
                root / legacy
            )
        else:
            present_view = legacy in _proposal_members(root, proposed_commit, (legacy,))
        if present_view:
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-REFERENCE", "historical view remains current"
            )
    for (consumer, legacy), disposition in references.items():
        source = sources[consumer_commits[consumer], consumer][1]
        if disposition.kind == "literal-path":
            valid = _exact_historical_path_occurs(source, legacy)
        else:
            valid = legacy in {
                link.target.as_posix()
                for link in _validated_rendered_links(
                    source.decode("utf-8", errors="strict"), consumer
                )
                if link.kind == "local" and link.target is not None
            }
        if not valid:
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-REFERENCE", "reference occurrence differs"
            )
    rows_by_source = {str(row["legacy_path"]): row for row in rows}
    for row in rows:
        source = str(row["legacy_path"])
        if targets[source] != source and (
            source in present
            or (proposed_commit is None and os.path.lexists(root / source))
        ):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-TARGET", "retired source remains current"
            )
        if row["action"] == "moved":
            immediate = edges[source]
            successor_row = rows_by_source.get(immediate)
            immediate_bytes = (
                sources[str(successor_row["source_commit"]), immediate][1]
                if successor_row is not None and immediate != source
                else target_contents.get(immediate)
            )
            if (
                immediate_bytes is None
                or immediate_bytes != sources[str(row["source_commit"]), source][1]
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-TARGET", "move is not byte-identical"
                )
    consumers = {}
    for path, commit in consumer_commits.items():
        content = sources[commit, path][1]
        rendered = {
            link.target.as_posix()
            for link in _validated_rendered_links(
                content.decode("utf-8", errors="strict"), path
            )
            if link.kind == "local" and link.target is not None
        }
        regular = any(
            target in targets and targets[target] != target for target in rendered
        )
        literal = any(
            key[0] == path
            and value.kind == "literal-path"
            and _exact_historical_path_occurs(content, key[1])
            for key, value in references.items()
        )
        view = any(
            key[0] == path and value.kind == "symlink-view" and key[1] in rendered
            for key, value in references.items()
        )
        if not (regular or literal or view):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-CONSUMER",
                "consumer has no rendered reviewed disposition",
            )
        consumers[path] = content
    dispositions = {
        str(row["legacy_path"]): MigrationDisposition(
            row_records[str(row["legacy_path"])],
            str(row["source_commit"]),
            str(row["source_blob"]),
            sources[str(row["source_commit"]), str(row["legacy_path"])][1],
            str(row["action"]),
            edges[str(row["legacy_path"])],
        )
        for row in rows
    }
    return MigrationProof(
        MappingProxyType(targets),
        MappingProxyType(consumers),
        MappingProxyType(record_ids),
        MappingProxyType(dispositions),
        snapshot_registry,
        MappingProxyType(
            {
                path: project_migration_declaration_fields(content, targets)
                for path, content in records.items()
            }
        ),
        MappingProxyType(references),
    )


def _proposed_migration_registry(
    root: Path,
    proposal: str | None,
    trusted_registry: Registry,
    *,
    raw_schema: object = _UNSET,
    read_current_bytes: Callable[[str, int], bytes] | None = None,
) -> Registry:
    """Validate proposal registry data with trusted schema and exact Git template modes."""

    path = REGISTRY_PATH.as_posix()
    if proposal is None:
        oid = _staged_regular_blob_inventory(root, paths=(path,)).get(path)
    else:
        member = _proposal_members(root, proposal, (path,)).get(path)
        oid = (
            member.object_id
            if member is not None
            and member.kind == "blob"
            and member.mode in {"100644", "100755"}
            else None
        )
    if oid is None:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "proposal registry is not regular"
        )
    content = _batch_blob_bytes(root, (oid,))[oid]
    if (
        proposal is None
        and _migration_current_bytes(
            root, path, CURRENT_MARKDOWN_MAX_BYTES, read_current_bytes
        )
        != content
    ):
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-STAGED-DRIFT", "registry index/worktree differ"
        )
    try:
        raw = json.loads(
            content.decode("utf-8", errors="strict"),
            object_pairs_hook=_unique_json_object,
        )
        if not isinstance(raw, dict) or not isinstance(raw.get("profiles"), list):
            raise ValueError
        templates = tuple(
            sorted(
                {
                    profile["template"]
                    for profile in raw["profiles"]
                    if isinstance(profile, dict)
                    and isinstance(profile.get("template"), str)
                }
            )
        )
        _validate_commit_path_requests(templates)
        if proposal is None:
            regular = frozenset(
                PurePosixPath(path)
                for path in _staged_regular_blob_inventory(root, paths=templates)
            )
        else:
            members = _proposal_members(root, proposal, templates)
            regular = frozenset(
                PurePosixPath(path)
                for path, entry in members.items()
                if entry.kind == "blob" and entry.mode in {"100644", "100755"}
            )
        schema_options = {} if raw_schema is _UNSET else {"raw_schema": raw_schema}
        return _load_canonical_markdown_module().validate_registry(
            root,
            raw,
            template_regular_paths=regular,
            trusted_registry=trusted_registry,
            **schema_options,
        )
    except ArchiveContractError:
        raise
    except (ValueError, OSError, UnicodeError) as exc:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "proposal registry differs"
        ) from exc


def _proposal_members(
    root: Path, commit: str, paths: tuple[str, ...]
) -> dict[str, _GitTreeMember]:
    length = _repository_identity(root)
    if len(commit) != length or _FULL_OBJECT_ID.fullmatch(commit) is None:
        raise ArchiveContractError(
            "RECOVERY-OBJECT-AMBIGUOUS", "proposal identity differs"
        )
    return _commit_tree_members(
        root,
        commit,
        original_paths=paths,
        historical_paths=(),
        object_id_length=length,
    )


def _require_proposal_recovery_ancestry(
    root: Path, commits: tuple[str, ...], proposal: str
) -> None:
    """Retain the proposal through named refs and bind every source to its ancestry."""

    length = _repository_identity(root)
    if len(proposal) != length or _FULL_OBJECT_ID.fullmatch(proposal) is None:
        raise ArchiveContractError(
            "RECOVERY-OBJECT-AMBIGUOUS", "proposal identity differs"
        )
    if _commit_types(root, (proposal,)).get(proposal) != "commit":
        raise ArchiveContractError(
            "RECOVERY-OBJECT-NOT-COMMIT", "proposal is not a commit"
        )
    refs = _git_command(
        root,
        "for-each-ref",
        "--count=1",
        "--format=%(refname)",
        f"--contains={proposal}",
        "refs/heads/",
        "refs/remotes/",
        output_limit=_GIT_TREE_OUTPUT_LIMIT,
    )
    if refs.returncode:
        raise ArchiveContractError("RECOVERY-DURABLE-REF", "proposal refs unavailable")
    try:
        retained_by = tuple(refs.stdout.decode("ascii", errors="strict").splitlines())
    except UnicodeError as exc:
        raise ArchiveContractError(
            "RECOVERY-DURABLE-REF", "proposal refs malformed"
        ) from exc
    require_commits_reachable_from_durable_refs(root, (proposal,), retained_by)
    for commit in commits:
        if _git_command(
            root, "merge-base", "--is-ancestor", commit, proposal
        ).returncode:
            raise ArchiveContractError(
                "RECOVERY-OBJECT-UNREACHABLE", "source is outside proposal ancestry"
            )


def repository_migration_proof(
    root: Path,
    *,
    requested_record: tuple[str, bytes] | None = None,
    registry: Registry | None = None,
    raw_schema: object = _UNSET,
    read_current_bytes: Callable[[str, int], bytes] | None = None,
) -> MigrationProof:
    """Discover bounded generic records and retain any caller's exact requested bytes."""

    input_options = _migration_input_options(registry, raw_schema, read_current_bytes)
    if registry is not None and not input_options:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "held migration inputs are incomplete"
        )
    records: dict[str, bytes] = {}
    descriptor, _ = _open_parent_at(
        root, ARCHIVE_ROOT / "migrations" / ".discovery", code="RECOVERY-RECORD-READ"
    )
    total = 0
    try:
        with os.scandir(descriptor) as entries:
            for count, entry in enumerate(entries, 1):
                if count > _GIT_TREE_ENTRY_LIMIT:
                    raise ArchiveContractError(
                        "RECOVERY-RESOURCE-LIMIT", "migration discovery budget differs"
                    )
                path = f"{ARCHIVE_ROOT}/migrations/{entry.name}"
                if generic_migration_id(path) is None:
                    continue
                if len(records) >= MAX_GIT_BATCH_OBJECTS:
                    raise ArchiveContractError(
                        "RECOVERY-RESOURCE-LIMIT", "migration record budget differs"
                    )
                content = _migration_current_bytes(
                    root, path, MIGRATION_DOCUMENT_MAX_BYTES, read_current_bytes
                )
                if not is_sealed_migration(content):
                    continue
                total += len(content)
                if total > MAX_GIT_BATCH_BYTES:
                    raise ArchiveContractError(
                        "RECOVERY-RESOURCE-LIMIT", "migration byte budget differs"
                    )
                records[path] = content
    except OSError as exc:
        raise ArchiveContractError(
            "RECOVERY-RECORD-READ", "migration discovery is unavailable"
        ) from exc
    finally:
        os.close(descriptor)
    if (
        requested_record is not None
        and records.get(requested_record[0]) != requested_record[1]
    ):
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-STAGED-DRIFT", "requested migration bytes differ"
        )
    if not input_options:
        return validate_migration_records(root, records)
    return validate_migration_records(root, records, registry=registry, **input_options)


def _read_stream_bounded(stream: object, limit: int) -> bytes:
    """Expose the shared bounded reader at this repository validation boundary."""

    return _recovery_read_stream_bounded(stream, limit)


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


def _migration_control_diagnostics(
    path: str,
    content: bytes,
) -> tuple[ArchiveDiagnostic, ...]:
    """Validate the bounded profile and row census of one declared control."""

    contract = _ARCHIVE_MIGRATION_CONTROLS.get(path)
    if contract is None:
        if generic_migration_id(path) is not None:
            if not is_sealed_migration(content):
                return ()
            try:
                parse_migration_control(path, content)
            except ArchiveContractError:
                return (_diagnostic("ARCHIVE-MIGRATION-PROFILE", path),)
            return ()
        return (_diagnostic("ARCHIVE-MIGRATION-CONTROL", path),)
    expected_id, expected_rows, expected_actions, expected_sha256 = contract
    digest = hashlib.sha256(content).hexdigest()
    is_legacy_base = digest == _MIGRATION_LEGACY_BASE_SHA256.get(path)
    expected_keys = (
        _LEGACY_MIGRATION_FRONTMATTER_KEYS
        if is_legacy_base
        else _MIGRATION_FRONTMATTER_KEYS
    )
    try:
        if (
            expected_sha256 is not None
            and digest != expected_sha256
            and not is_legacy_base
        ):
            raise ValueError
        text = content.decode("utf-8", errors="strict")
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            raise ValueError
        frontmatter_end = lines.index("---", 1)
        metadata: dict[str, str] = {}
        for line in lines[1:frontmatter_end]:
            key, separator, value = line.partition(": ")
            if not separator or key in metadata:
                raise ValueError
            if len(value) < 2 or value[0] != '"' or value[-1] != '"':
                raise ValueError
            metadata[key] = value[1:-1]
        if (
            tuple(metadata) != expected_keys
            or metadata.get("type") != "content/archive-migration"
            or metadata.get("status")
            != ("sealed" if path == _WORK054_WP004B_MIGRATION_PATH else "accepted")
            or metadata.get("owner") != "platform"
            or metadata.get("artifact_id") != expected_id
            or not metadata.get("title", "").startswith(f"{expected_id}: ")
            or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", metadata.get("updated", ""))
            is None
        ):
            raise ValueError
        if content.count(_MIGRATION_LEDGER_PREFIX) != 1:
            raise ValueError
        _before, separator, payload = content.partition(_MIGRATION_LEDGER_PREFIX)
        if not separator:
            raise ValueError
        raw_rows, fence, suffix = payload.partition(b"\n```\n")
        if not fence or not suffix.startswith(b"\n## Recovery\n"):
            raise ValueError
        rows = json.loads(raw_rows.decode("utf-8", errors="strict"))
        if type(rows) is not list:
            raise ValueError
        actions: dict[str, int] = {}
        for row in rows:
            if type(row) is not dict or not isinstance(row.get("action"), str):
                raise ValueError
            action = row["action"]
            actions[action] = actions.get(action, 0) + 1
        if expected_rows is not None and len(rows) != expected_rows:
            raise ValueError
        if expected_actions is not None and actions != expected_actions:
            raise ValueError
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return (_diagnostic("ARCHIVE-MIGRATION-PROFILE", path),)
    return ()


def parse_pinned_migration_control(
    path: str,
    content: bytes,
) -> tuple[dict[str, object], ...]:
    """Parse one declared migration only when its reviewed bytes are exact."""

    if (
        path not in _ARCHIVE_MIGRATION_CONTROLS
        or type(content) is not bytes
        or len(content) > MIGRATION_DOCUMENT_MAX_BYTES
        or _migration_control_diagnostics(path, content)
    ):
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "migration control differs"
        )
    try:
        _prefix, marker, remainder = content.partition(_MIGRATION_LEDGER_PREFIX)
        raw_rows, fence, _suffix = remainder.partition(b"\n```\n")
        rows = json.loads(raw_rows.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "migration control differs"
        ) from exc
    if not marker or not fence or type(rows) is not list:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "migration control differs"
        )
    return tuple(rows)


def validate_pinned_migration_recovery(
    repository_root: str | Path,
    path: str,
    content: bytes,
) -> tuple[dict[str, object], ...]:
    """Verify declared recovery tuples against the exact Git object graph."""

    if path not in {
        _WORK054_WP003_MIGRATION_PATH,
        _WORK054_WP004B_MIGRATION_PATH,
    }:
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE",
            "migration recovery is not declared for this control",
        )
    rows = parse_pinned_migration_control(path, content)
    try:
        root = Path(repository_root).resolve(strict=True)
        if path == _WORK054_WP004B_MIGRATION_PATH:
            staged = read_staged_blob_bounded(root, path)
            if staged != content:
                raise ArchiveContractError(
                    "ARCHIVE-MIGRATION-STAGED-DRIFT",
                    "sealed migration differs between index and worktree",
                )
            _validate_mig0004_rows_and_targets(root, rows)
            validate_mig0004_historical_targets(root, rows)
        object_id_length = _repository_identity(root)
        by_commit: dict[str, list[dict[str, object]]] = {}
        seen_paths: set[str] = set()
        for row in rows:
            legacy_path = row.get("legacy_path")
            source_commit = row.get("source_commit")
            source_blob = row.get("source_blob")
            content_sha256 = row.get("content_sha256")
            canonical = _canonical_path(legacy_path)
            if (
                canonical is None
                or canonical != legacy_path
                or canonical in seen_paths
                or not isinstance(source_commit, str)
                or len(source_commit) != object_id_length
                or _FULL_OBJECT_ID.fullmatch(source_commit) is None
                or not isinstance(source_blob, str)
                or len(source_blob) != object_id_length
                or _FULL_OBJECT_ID.fullmatch(source_blob) is None
                or not isinstance(content_sha256, str)
                or re.fullmatch(r"[0-9a-f]{64}", content_sha256) is None
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-ROW", "migration source tuple is invalid"
                )
            seen_paths.add(canonical)
            by_commit.setdefault(source_commit, []).append(row)

        commit_types = _commit_types(root, tuple(sorted(by_commit)))
        if any(commit_types.get(commit) != "commit" for commit in by_commit):
            raise ArchiveContractError(
                "RECOVERY-OBJECT-NOT-COMMIT", "migration commit is unavailable"
            )
        if path == _WORK054_WP004B_MIGRATION_PATH:
            _require_commits_reachable(root, tuple(sorted(by_commit)))
        members = {
            commit: _commit_tree_members(
                root,
                commit,
                original_paths=tuple(
                    sorted(str(row["legacy_path"]) for row in commit_rows)
                ),
                historical_paths=(),
                object_id_length=object_id_length,
            )
            for commit, commit_rows in by_commit.items()
        }
        expected_blobs: set[str] = set()
        for commit, commit_rows in by_commit.items():
            commit_members = members.get(commit, {})
            for row in commit_rows:
                member = commit_members.get(str(row["legacy_path"]))
                if (
                    member is None
                    or member.kind != "blob"
                    or member.mode not in {"100644", "100755"}
                    or member.object_id != row["source_blob"]
                ):
                    raise ArchiveContractError(
                        "RECOVERY-MIGRATION-BLOB",
                        "migration source blob differs",
                    )
                expected_blobs.add(member.object_id)
        blobs = _batch_blob_bytes(root, tuple(sorted(expected_blobs)))
        for commit_rows in by_commit.values():
            for row in commit_rows:
                source = blobs.get(str(row["source_blob"]))
                if (
                    source is None
                    or hashlib.sha256(source).hexdigest() != row["content_sha256"]
                ):
                    raise ArchiveContractError(
                        "RECOVERY-MIGRATION-CONTENT",
                        "migration source content differs",
                    )
    except ArchiveContractError:
        raise
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-INPUT", "migration recovery input is invalid"
        ) from exc
    return rows


def read_staged_blob_bounded(
    repository_root: str | Path,
    path: str,
    *,
    max_bytes: int = MIGRATION_DOCUMENT_MAX_BYTES,
) -> bytes:
    """Read one regular stage-zero Git blob without worktree substitution."""

    if (
        _canonical_path(path, archive_only=True) != path
        or type(max_bytes) is not int
        or not 0 < max_bytes <= MIGRATION_DOCUMENT_MAX_BYTES
    ):
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "staged migration blob differs"
        )
    try:
        root = Path(repository_root).resolve(strict=True)
        if not root.is_dir():
            raise OSError
        object_id_length = _repository_identity(root)
        staged = _git_command(
            root,
            "ls-files",
            "--stage",
            "-z",
            "--",
            path,
            output_limit=4096,
        )
        records = staged.stdout.split(b"\0")
        if staged.returncode or len(records) != 2 or records[-1] != b"":
            raise ValueError
        header, raw_path = records[0].split(b"\t", 1)
        mode, raw_object_id, stage = header.split(b" ", 2)
        object_id = raw_object_id.decode("ascii", errors="strict")
        if (
            mode not in {b"100644", b"100755"}
            or stage != b"0"
            or raw_path.decode("utf-8", errors="strict") != path
            or len(object_id) != object_id_length
            or _FULL_OBJECT_ID.fullmatch(object_id) is None
        ):
            raise ValueError
        return _read_git_blob_batch(
            root,
            (object_id,),
            object_id_length=object_id_length,
            per_blob_limit=max_bytes,
            aggregate_limit=max_bytes,
            object_limit=1,
        )[object_id]
    except (KeyError, OSError, RuntimeError, UnicodeDecodeError, ValueError) as exc:
        if isinstance(exc, ArchiveContractError):
            raise
        raise ArchiveContractError(
            "ARCHIVE-MIGRATION-PROFILE", "staged migration blob differs"
        ) from exc


def read_worktree_regular_bounded(
    repository_root: str | Path,
    path: str,
    *,
    max_bytes: int = CURRENT_MARKDOWN_MAX_BYTES,
) -> bytes:
    """Read one regular file through held no-follow descriptors within a budget."""

    if (
        _canonical_path(path) != path
        or type(max_bytes) is not int
        or not 0 < max_bytes <= CURRENT_MARKDOWN_MAX_BYTES
    ):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET", "current target path is invalid"
        )
    try:
        root = Path(repository_root).resolve(strict=True)
        root_metadata = os.lstat(root)
        if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(
            root_metadata.st_mode
        ):
            raise OSError
        directory_flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        file_flags = (
            os.O_RDONLY
            | os.O_NONBLOCK
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptors: list[int] = []
        try:
            root_descriptor = os.open(root, directory_flags)
            descriptors.append(root_descriptor)
            opened_root = os.fstat(root_descriptor)
            if not stat.S_ISDIR(opened_root.st_mode) or (
                opened_root.st_dev,
                opened_root.st_ino,
            ) != (root_metadata.st_dev, root_metadata.st_ino):
                raise OSError
            parent_descriptor = root_descriptor
            parts = PurePosixPath(path).parts
            for part in parts[:-1]:
                child = os.open(part, directory_flags, dir_fd=parent_descriptor)
                descriptors.append(child)
                if not stat.S_ISDIR(os.fstat(child).st_mode):
                    raise OSError
                parent_descriptor = child
            file_descriptor = os.open(parts[-1], file_flags, dir_fd=parent_descriptor)
            descriptors.append(file_descriptor)
            before = os.fstat(file_descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise OSError
            if before.st_size > max_bytes:
                raise ArchiveContractError(
                    "RECOVERY-RESOURCE-LIMIT",
                    "current Markdown exceeds its byte budget",
                )
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = os.read(file_descriptor, min(65536, max_bytes + 1 - total))
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > max_bytes:
                    raise ArchiveContractError(
                        "RECOVERY-RESOURCE-LIMIT",
                        "current Markdown exceeds its byte budget",
                    )
            after = os.fstat(file_descriptor)
            current = os.stat(
                parts[-1], dir_fd=parent_descriptor, follow_symlinks=False
            )

            def identity(item: os.stat_result) -> tuple[int, int, int, int, int]:
                return (
                    item.st_dev,
                    item.st_ino,
                    item.st_mode,
                    item.st_size,
                    item.st_mtime_ns,
                )

            if identity(before) != identity(after) or identity(after) != identity(
                current
            ):
                raise OSError
            return b"".join(chunks)
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)
    except ArchiveContractError:
        raise
    except (OSError, RuntimeError) as exc:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET",
            "current target is unavailable or changed during read",
        ) from exc


def _staged_regular_blob_inventory(
    root: Path,
    *,
    paths: tuple[str, ...] = (
        "docs/01.requirements",
        "docs/02.architecture",
        "docs/03.specs",
        "docs/99.templates",
    ),
) -> dict[str, str]:
    """Return the bounded stage-zero regular cutover-target inventory."""

    object_id_length = _repository_identity(root)
    result = _git_command(
        root,
        "ls-files",
        "--stage",
        "-z",
        "--",
        *paths,
        output_limit=_INDEX_CAPTURE_MAX_BYTES,
    )
    if result.returncode:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-INPUT", "stage-zero inventory is unavailable"
        )
    records = result.stdout.split(b"\0")
    if not records or records[-1] != b"":
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-INPUT", "stage-zero inventory is malformed"
        )
    inventory: dict[str, str] = {}
    try:
        for record in records[:-1]:
            header, raw_path = record.split(b"\t", 1)
            mode, raw_object_id, stage = header.split(b" ", 2)
            path = raw_path.decode("utf-8", errors="strict")
            object_id = raw_object_id.decode("ascii", errors="strict")
            if (
                mode not in {b"100644", b"100755"}
                or stage != b"0"
                or _canonical_path(path) != path
                or path in inventory
                or len(object_id) != object_id_length
                or _FULL_OBJECT_ID.fullmatch(object_id) is None
            ):
                raise ValueError
            inventory[path] = object_id
    except (UnicodeDecodeError, ValueError) as exc:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-INPUT", "stage-zero inventory is malformed"
        ) from exc
    if len(inventory) > CURRENT_MARKDOWN_MAX_FILES:
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "current Markdown count exceeds its budget"
        )
    return inventory


def _staged_markdown_documents(
    root: Path,
    inventory: Mapping[str, str],
    paths: Sequence[str],
) -> dict[str, str]:
    """Read exact stage-zero Markdown and require byte-identical worktree files."""

    selected = tuple(sorted(paths))
    if (
        len(selected) > CURRENT_MARKDOWN_MAX_FILES
        or len(set(selected)) != len(selected)
        or any(path not in inventory for path in selected)
    ):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET", "current staged target set differs"
        )
    object_ids = tuple(sorted({inventory[path] for path in selected}))
    object_id_length = _repository_identity(root)
    blobs: dict[str, bytes] = {}
    remaining_bytes = CURRENT_MARKDOWN_TOTAL_BYTES
    for offset in range(0, len(object_ids), MAX_GIT_BATCH_OBJECTS):
        batch = object_ids[offset : offset + MAX_GIT_BATCH_OBJECTS]
        batch_blobs = _read_git_blob_batch(
            root,
            batch,
            object_id_length=object_id_length,
            per_blob_limit=CURRENT_MARKDOWN_MAX_BYTES,
            aggregate_limit=remaining_bytes,
            object_limit=MAX_GIT_BATCH_OBJECTS,
        )
        batch_bytes = sum(len(content) for content in batch_blobs.values())
        if batch_bytes > remaining_bytes:
            raise ArchiveContractError(
                "RECOVERY-RESOURCE-LIMIT",
                "current Markdown bytes exceed their aggregate budget",
            )
        remaining_bytes -= batch_bytes
        blobs.update(batch_blobs)
    documents: dict[str, str] = {}
    total = 0
    for path in selected:
        staged = blobs[inventory[path]]
        total += len(staged)
        if total > CURRENT_MARKDOWN_TOTAL_BYTES:
            raise ArchiveContractError(
                "RECOVERY-RESOURCE-LIMIT",
                "current Markdown bytes exceed their aggregate budget",
            )
        worktree = read_worktree_regular_bounded(root, path)
        if worktree != staged:
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-TARGET",
                "current target differs between index and worktree",
            )
        try:
            documents[path] = staged.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ArchiveContractError(
                "RECOVERY-NON-UTF8", "current Markdown is not UTF-8"
            ) from exc
    return documents


def _untracked_task_paths(root: Path) -> tuple[str, ...]:
    result = _git_command(
        root,
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        "docs/03.specs",
        output_limit=_INDEX_CAPTURE_MAX_BYTES,
    )
    if result.returncode:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-INPUT", "untracked Task lookup failed"
        )
    try:
        paths = tuple(
            sorted(
                raw.decode("utf-8", errors="strict")
                for raw in result.stdout.split(b"\0")
                if raw
            )
        )
    except UnicodeDecodeError as exc:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-INPUT", "untracked Task lookup is malformed"
        ) from exc
    pattern = re.compile(
        r"docs/03\.specs/[0-9]{4}-[a-z0-9-]+/tasks/tsk-[0-9]{4}-[a-z0-9-]+\.md\Z"
    )
    return tuple(path for path in paths if pattern.fullmatch(path))


def _require_commits_reachable(root: Path, commits: tuple[str, ...]) -> None:
    """Require each source commit through the named current durable ref."""

    durable_ref = current_named_durable_ref(root)
    require_commits_reachable_from_durable_refs(root, commits, (durable_ref,))


def _require_regular_current_target(
    relative: str,
    inventory: Mapping[str, str],
) -> None:
    """Require a canonical current target to be a tracked stage-zero blob."""

    if _canonical_path(relative) != relative or relative not in inventory:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET",
            "migration target is not a tracked stage-zero regular blob",
        )


def _reachable_historical_regular_target(
    root: Path,
    relative: str,
    *,
    proposed_commit: str | None,
) -> _GitTreeMember:
    """Prove an absent Migration target existed on the reachable branch history."""

    if _canonical_path(relative) != relative:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET", "migration target path differs"
        )
    anchor = proposed_commit or current_named_durable_ref(root)
    result = _git_capture_bounded(
        root,
        "log",
        "-1",
        "--format=%H",
        "--diff-filter=AM",
        "--no-renames",
        anchor,
        "--",
        relative,
        stdout_limit=_INDEX_CAPTURE_MAX_BYTES,
    )
    try:
        commits = tuple(
            line.decode("ascii", errors="strict")
            for line in result.stdout.splitlines()
            if line
        )
    except UnicodeDecodeError as exc:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET", "historical target lookup is malformed"
        ) from exc
    object_id_length = _repository_identity(root)
    if (
        result.returncode
        or len(commits) != 1
        or len(commits[0]) != object_id_length
        or _FULL_OBJECT_ID.fullmatch(commits[0]) is None
    ):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET",
            "migration target has no reachable regular-file history",
        )
    member = _commit_tree_members(
        root,
        commits[0],
        original_paths=(relative,),
        historical_paths=(),
        object_id_length=object_id_length,
    ).get(relative)
    if member is None or member.kind != "blob" or member.mode not in {
        "100644",
        "100755",
    }:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET",
            "migration target has no reachable regular-file history",
        )
    return member


def _sealed_row_retired_paths(root: Path) -> frozenset[str]:
    """Return every legacy path a sealed generic migration row retires."""

    inventory = _staged_regular_blob_inventory(
        root, paths=((ARCHIVE_ROOT / "migrations").as_posix(),)
    )
    retired: set[str] = set()
    for path in sorted(inventory):
        if generic_migration_id(path) is None:
            continue
        content = read_staged_blob_bounded(root, path)
        if not is_sealed_migration(content):
            continue
        rows, _consumers = parse_migration_control(path, content)
        for row in rows:
            legacy = row.get("legacy_path")
            if isinstance(legacy, str):
                retired.add(legacy)
    return frozenset(retired)


def _validate_mig0004_rows_and_targets(
    root: Path,
    rows: tuple[dict[str, object], ...],
) -> None:
    """Validate MIG-0004's finite disposition and current target inventory."""

    if len(rows) != MIG0004_ROW_COUNT:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-ROW", "MIG-0004 row census differs"
        )
    fields = (
        "legacy_path",
        "stable_path",
        "artifact_id",
        "action",
        "replacement",
        "source_commit",
        "source_blob",
        "content_sha256",
        "reason",
    )
    requirement = re.compile(r"docs/01\.requirements/[0-9]{4}-[a-z0-9-]+\.md\Z")
    architecture = re.compile(
        r"docs/02\.architecture/descriptions/ad-([0-9]{4})-[a-z0-9-]+\.md\Z"
    )
    task_ledger = re.compile(
        r"docs/03\.specs/(?P<spec>[0-9]{4})-[a-z0-9-]+/tasks\.md\Z"
    )
    agent_design_paths = {
        "docs/03.specs/0024-observability-and-network-review-agents/agent-design.md",
        "docs/03.specs/0041-stage-00-agent-governance-contract/agent-design.md",
    }
    task_directories: set[str] = set()
    target_paths: set[str] = set()
    stage99_paths: set[str] = set()
    spec0054_rows = 0
    previous: str | None = None
    legacy_paths: set[str] = set()
    inventory = _staged_regular_blob_inventory(root)
    # A sealed generic row already refuses a legacy path that is still present,
    # and validate_mig0004_historical_targets proves each sealed Stage 99 move
    # against its pinned historical commit. Requiring the target to remain in
    # the current tree adds no proof about the past; it only forbids a later
    # reviewed retirement, so a retired target is released from the inventory.
    stage99_targets = frozenset(
        target for _action, target in MIG0004_STAGE99_ACTION_TARGETS.values()
    ) - _sealed_row_retired_paths(root)
    consumer_paths = tuple(
        path
        for path in inventory
        if path.endswith(".md")
        and path.startswith(
            ("docs/01.requirements/", "docs/02.architecture/", "docs/03.specs/")
        )
    )
    selected_documents = _staged_markdown_documents(
        root,
        inventory,
        tuple(sorted(set(consumer_paths) | set(stage99_targets))),
    )

    for row in rows:
        legacy = row.get("legacy_path")
        expected_stage99 = (
            MIG0004_STAGE99_ACTION_TARGETS.get(legacy)
            if isinstance(legacy, str)
            else None
        )
        stage99_row = expected_stage99 is not None
        if (
            type(row) is not dict
            or tuple(row) != fields
            or not isinstance(legacy, str)
            or _canonical_path(legacy) != legacy
            or legacy in legacy_paths
            or (previous is not None and legacy <= previous)
            or not isinstance(row.get("source_commit"), str)
            or _FULL_OBJECT_ID.fullmatch(str(row["source_commit"])) is None
            or not isinstance(row.get("source_blob"), str)
            or _FULL_OBJECT_ID.fullmatch(str(row["source_blob"])) is None
            or not isinstance(row.get("content_sha256"), str)
            or re.fullmatch(r"[0-9a-f]{64}", str(row["content_sha256"])) is None
            or not isinstance(row.get("reason"), str)
            or not str(row["reason"]).strip()
            or (
                legacy
                in set(MIG0004_STAGE99_ACTION_TARGETS) | {MIG0004_SPEC0054_LEDGER}
                and row.get("source_commit") != MIG0004_TERMINAL_SOURCE_COMMIT
            )
        ):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-ROW", f"row identity differs: {legacy!r}"
            )
        previous = legacy
        legacy_paths.add(legacy)
        target: object
        if stage99_row:
            expected_action, expected_target = expected_stage99
            target_field = (
                "stable_path" if expected_action == "moved" else "replacement"
            )
            empty_field = "replacement" if expected_action == "moved" else "stable_path"
            if (
                row.get("action") != expected_action
                or row.get(target_field) != expected_target
                or row.get(empty_field) is not None
                or row.get("artifact_id") is not None
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-ROW", f"Stage99 action target differs: {legacy}"
                )
            stage99_paths.add(legacy)
            target = expected_target
        elif isinstance(legacy, str) and legacy.startswith("docs/99.templates/"):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-ROW", f"undeclared Stage99 row: {legacy}"
            )
        elif requirement.fullmatch(legacy):
            if (
                row.get("action") != "replaced"
                or row.get("stable_path") is not None
                or row.get("artifact_id") is not None
                or row.get("replacement") != legacy
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-ROW",
                    f"Requirement replacement differs: {legacy}",
                )
            target = row["replacement"]
        elif (match := architecture.fullmatch(legacy)) is not None:
            expected_target = legacy.replace("/ad-", "/", 1)
            expected_artifact = f"AD-{match.group(1)}"
            if (
                row.get("action") != "moved"
                or row.get("stable_path") != expected_target
                or row.get("artifact_id") != expected_artifact
                or row.get("replacement") is not None
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-ROW", f"Architecture move differs: {legacy}"
                )
            target = row["stable_path"]
        elif legacy in agent_design_paths:
            expected_target = str(PurePosixPath(legacy).with_name("spec.md"))
            if (
                row.get("action") != "merged"
                or row.get("stable_path") is not None
                or row.get("artifact_id") is not None
                or row.get("replacement") != expected_target
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-ROW",
                    f"agent-design disposition differs: {legacy}",
                )
            target = row["replacement"]
        elif (match := task_ledger.fullmatch(legacy)) is not None:
            if legacy == MIG0004_SPEC0054_LEDGER:
                spec0054_rows += 1
            expected_target = str(PurePosixPath(legacy).with_name("README.md"))
            if (
                row.get("action") != "replaced"
                or row.get("stable_path") is not None
                or row.get("artifact_id") is not None
                or row.get("replacement") != expected_target
            ):
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-ROW", f"Task replacement differs: {legacy}"
                )
            task_directories.add(PurePosixPath(legacy).parent.as_posix())
            target = row["replacement"]
        else:
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-ROW",
                f"MIG-0004 legacy path is undeclared: {legacy}",
            )
        if not isinstance(target, str):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-TARGET", "migration target is invalid"
            )
        if not stage99_row:
            _require_regular_current_target(target, inventory)
            target_paths.add(target)
        if target != legacy and legacy in inventory:
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-TARGET", "retired source remains current"
            )

    if stage99_paths != set(MIG0004_STAGE99_ACTION_TARGETS):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-ROW", "MIG-0004 Stage99 disposition differs"
        )
    if spec0054_rows != 1:
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-ROW", "MIG-0004 Spec0054 disposition differs"
        )

    task_artifacts: dict[str, str] = {}
    if _untracked_task_paths(root):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TASK", "untracked Task record is present"
        )
    for package in sorted(task_directories):
        prefix = f"{package}/tasks/"
        for relative in sorted(
            path
            for path in inventory
            if path.startswith(prefix) and PurePosixPath(path).name.startswith("tsk-")
        ):
            _require_regular_current_target(relative, inventory)
            task_name = PurePosixPath(relative).name
            match = re.fullmatch(
                r"tsk-(?P<sequence>[0-9]{4})-[a-z0-9-]+\.md", task_name
            )
            if match is None:
                raise ArchiveContractError(
                    "RECOVERY-MIGRATION-TASK", "Task path differs"
                )
            spec = PurePosixPath(package).name[:4]
            artifact = f"SPEC-{spec}-TSK-{match.group('sequence')}"
            task_artifacts[relative] = artifact
    if len(task_artifacts) != len(set(task_artifacts.values())):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TASK", "Task artifact identity is not unique"
        )
    consumer_documents = {path: selected_documents[path] for path in consumer_paths}
    if not {path for path in target_paths if path.endswith(".md")}.issubset(
        consumer_documents
    ):
        raise ArchiveContractError(
            "RECOVERY-MIGRATION-TARGET", "migration target is outside current Markdown"
        )
    for relative, artifact in task_artifacts.items():
        if f'artifact_id: "{artifact}"' not in consumer_documents[relative]:
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-TASK", "Task identity differs"
            )

    retired_consumer = re.compile(
        r"docs/04\.execution/|docs/02\.architecture/descriptions/ad-[0-9]{4}-"
    )
    for contents in consumer_documents.values():
        if retired_consumer.search(contents):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-CONSUMER",
                "current document retains a retired path consumer",
            )


def validate_mig0004_historical_targets(
    root: Path,
    rows: tuple[dict[str, object], ...],
) -> None:
    """Prove sealed Stage99 moves in their original target tree, not mutable templates."""

    moved = tuple(
        row
        for row in rows
        if row.get("action") == "moved"
        and row.get("legacy_path") in MIG0004_STAGE99_ACTION_TARGETS
    )
    sources = _regular_source_bytes(
        root,
        {
            WP004C_SEALED_TARGET_COMMIT: tuple(
                sorted(str(row["stable_path"]) for row in moved)
            )
        },
    )
    for row in moved:
        blob, content = sources[WP004C_SEALED_TARGET_COMMIT, str(row["stable_path"])]
        if (
            blob != row["source_blob"]
            or hashlib.sha256(content).hexdigest() != row["content_sha256"]
        ):
            raise ArchiveContractError(
                "RECOVERY-MIGRATION-TARGET", "sealed Stage99 move differs"
            )


def _stage98_namespace_records(
    actual: frozenset[str],
    stable_rows: Mapping[str, Mapping[str, object]],
    reviewed_manifest: Mapping[str, ReviewedManifestRecord],
) -> tuple[dict[str, tuple[str, ...]], list[ArchiveDiagnostic]]:
    """Derive reporting partitions from Stage 98's durable recovery owners."""

    diagnostics: list[ArchiveDiagnostic] = []
    legacy_to_stable = {
        str(row["legacy_path"]): stable for stable, row in stable_rows.items()
    }
    base = frozenset(
        legacy_to_stable.get(path, path) for path in EXPECTED_ARCHIVE_PATHS
    )
    reviewed = frozenset(reviewed_manifest)
    # ADR-0030 makes Git history the full-content archive, so a base record is
    # proved by presence or by a sealed row in the digest-pinned WORK-107
    # ledger, which carries its source blob and content digest.
    sealed = frozenset(stable_rows)
    if not base.issubset(actual | sealed) or not reviewed.issubset(actual | sealed):
        diagnostics.append(
            _diagnostic("ARCHIVE-NAMESPACE-REVIEWED", ARCHIVE_ROOT.as_posix())
        )
    if base & reviewed:
        diagnostics.append(
            _diagnostic("ARCHIVE-NAMESPACE-OVERLAP", ARCHIVE_ROOT.as_posix())
        )
    additive = actual - base - reviewed
    namespaces = {
        "arwb-base": tuple(sorted(base & actual)),
        "acer-additive": tuple(sorted(additive)),
        "wdtc-execution": tuple(sorted(reviewed & actual)),
        "progress-snapshot": (),
    }
    return namespaces, diagnostics


def _repository_archive_records(
    root: Path,
) -> tuple[dict[str, bytes], list[ArchiveDiagnostic]]:
    records: dict[str, bytes] = {}
    migration_controls: dict[str, bytes] = {}
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
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_size > _ARCHIVE_RECORD_LIMIT
            ):
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
                if relative == ARCHIVE_INDEX.as_posix() or not relative.endswith(".md"):
                    continue
                content = read_record(directory_fd, name, relative)
                if (
                    relative in _ARCHIVE_MIGRATION_CONTROLS
                    or generic_migration_id(relative) is not None
                ):
                    migration_controls[relative] = content
                    diagnostics.extend(
                        _migration_control_diagnostics(relative, content)
                    )
                elif relative_path.parent == ARCHIVE_ROOT / "migrations":
                    diagnostics.append(
                        _diagnostic("ARCHIVE-MIGRATION-CONTROL", relative)
                    )
                else:
                    records[relative] = content
            else:
                diagnostics.append(_diagnostic("ARCHIVE-INVENTORY-TYPE", relative))

    try:
        archive_fd = os.open(
            archive_root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        visit(archive_fd, ARCHIVE_ROOT)
    except (OSError, RuntimeError, ValueError):
        diagnostics.append(
            _diagnostic("ARCHIVE-INVENTORY-READ", ARCHIVE_ROOT.as_posix())
        )
    finally:
        if archive_fd is not None:
            try:
                os.close(archive_fd)
            except OSError:
                diagnostics.append(
                    _diagnostic("ARCHIVE-INVENTORY-READ", ARCHIVE_ROOT.as_posix())
                )
    for migration_path in (
        _WORK054_WP003_MIGRATION_PATH,
        _WORK054_WP004B_MIGRATION_PATH,
    ):
        migration_content = migration_controls.get(migration_path)
        if migration_content is not None and not _migration_control_diagnostics(
            migration_path,
            migration_content,
        ):
            try:
                validate_pinned_migration_recovery(
                    root,
                    migration_path,
                    migration_content,
                )
            except ArchiveContractError as exc:
                diagnostics.append(_diagnostic(exc.code, migration_path))
    generic_controls = {
        path: content
        for path, content in migration_controls.items()
        if generic_migration_id(path) is not None and is_sealed_migration(content)
    }
    if generic_controls:
        try:
            validate_migration_records(root, generic_controls)
        except ArchiveContractError as exc:
            diagnostics.append(
                _diagnostic(exc.code, (ARCHIVE_ROOT / "migrations").as_posix())
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
        if (
            Path(str(getattr(module, "__file__", ""))).resolve(strict=True)
            != script_path
        ):
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
    if (
        document.source_commit != _MANIFEST_SOURCE_COMMIT
        or len(document.entries) != 132
    ):
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


def _work107_stable_rows(root: Path) -> dict[str, Mapping[str, object]]:
    """Load the exact reviewed stable ledger when WORK-107 has been applied."""

    path = root / WORK107_MIGRATION_PATH
    if not path.exists():
        return {}
    try:
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != WORK107_MIGRATION_DOCUMENT_SHA256:
            raise RuntimeError("WORK-107 stable ledger digest differs")
        validated = parse_work107_migration_document(content)
    except (ArchiveContractError, OSError, RuntimeError, TypeError, ValueError) as exc:
        raise RuntimeError("WORK-107 stable ledger is unavailable") from exc
    return {str(row["stable_path"]): row for row in validated}


def _read_repository_index(root: Path) -> str:
    """Read the Stage 98 index through held descriptors within a fixed budget."""

    current_fd: int | None = None
    descriptor: int | None = None
    try:
        current_fd = os.open(
            root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        for part in ARCHIVE_INDEX.parts[:-1]:
            child_fd = os.open(
                part,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=current_fd,
            )
            os.close(current_fd)
            current_fd = child_fd
        descriptor = os.open(
            ARCHIVE_INDEX.name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=current_fd,
        )
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise OSError
        if before.st_size > _ARCHIVE_INDEX_LIMIT:
            raise ArchiveContractError(
                "ARCHIVE-INDEX-SIZE", "archive index exceeds its byte budget"
            )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            chunk = os.read(descriptor, min(65536, remaining))
            if not chunk:
                raise OSError
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise ArchiveContractError(
                "ARCHIVE-INDEX-SIZE", "archive index changed beyond its byte budget"
            )
        after = os.fstat(descriptor)
        linked = os.stat(
            ARCHIVE_INDEX.name,
            dir_fd=current_fd,
            follow_symlinks=False,
        )
        if (
            before.st_dev != after.st_dev
            or before.st_ino != after.st_ino
            or before.st_mode != after.st_mode
            or before.st_size != after.st_size
            or before.st_dev != linked.st_dev
            or before.st_ino != linked.st_ino
        ):
            raise OSError
        return b"".join(chunks).decode("utf-8", errors="strict")
    except ArchiveContractError:
        raise
    except (OSError, UnicodeDecodeError) as exc:
        raise ArchiveContractError(
            "ARCHIVE-INDEX-READ", "archive index is unavailable"
        ) from exc
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
        if current_fd is not None:
            try:
                os.close(current_fd)
            except OSError:
                pass


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
        diagnostics.append(
            _diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix())
        )
    rows: dict[str, tuple[str, ...]] = {}
    link_total = 0
    for line in raw_rows:
        cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
        if len(cells) != 9:
            diagnostics.append(
                _diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix())
            )
            continue
        link = _INDEX_LINK.fullmatch(cells[0])
        code_cells = tuple(
            _INDEX_CODE.fullmatch(cells[index]) for index in (1, 2, 3, 4, 5, 8)
        )
        if (
            link is None
            or any(match is None for match in code_cells)
            or not cells[6].isdigit()
        ):
            diagnostics.append(
                _diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix())
            )
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
            diagnostics.append(
                _diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX.as_posix())
            )
            continue
        values = tuple(
            match.group("value") for match in code_cells if match is not None
        )
        rows[path] = (*values, cells[7], cells[6])
        link_total += int(cells[6])
    markers = tuple(_INDEX_MARKER.finditer(text))
    if (
        len(markers) != 1
        or int(markers[0].group("records")) != len(rows)
        or int(markers[0].group("links")) != link_total
    ):
        diagnostics.append(
            _diagnostic("ARCHIVE-INDEX-MANIFEST", ARCHIVE_INDEX.as_posix())
        )
    return rows, link_total, diagnostics


def validate_repository_archive(
    repository_root: str | Path,
    registry: object,
) -> ArchiveValidationReport:
    """Validate the repository archive from Stage 98 recovery owners."""

    del registry  # Kept for the public compatibility signature through WP-011.

    try:
        root = Path(repository_root).resolve(strict=True)
        if not root.is_dir():
            raise OSError
    except (OSError, RuntimeError, TypeError):
        return _report((_diagnostic("ARCHIVE-ROOT-UNAVAILABLE", "<repository>"),))
    records, inventory_diagnostics = _repository_archive_records(root)
    actual = frozenset(records)
    diagnostics = [*inventory_diagnostics]
    try:
        stable_rows = _work107_stable_rows(root)
    except RuntimeError:
        stable_rows = {}
        diagnostics.append(
            _diagnostic("ARCHIVE-MIGRATION-LEDGER", WORK107_MIGRATION_PATH)
        )
    legacy_to_stable = {
        str(row["legacy_path"]): stable for stable, row in stable_rows.items()
    }
    try:
        reviewed_manifest = _reviewed_manifest_records(root)
    except (OSError, RuntimeError, TypeError, ValueError):
        reviewed_manifest = {}
        diagnostics.append(
            _diagnostic("ARCHIVE-NAMESPACE-REVIEWED", ARCHIVE_ROOT.as_posix())
        )
    if stable_rows:
        reviewed_manifest = {
            legacy_to_stable.get(path, path): ReviewedManifestRecord(
                target=legacy_to_stable.get(path, path),
                original_path=row.original_path,
                source_commit=row.source_commit,
                source_blob=row.source_blob,
            )
            for path, row in reviewed_manifest.items()
        }
    namespaces, namespace_diagnostics = _stage98_namespace_records(
        actual,
        stable_rows,
        reviewed_manifest,
    )
    diagnostics.extend(namespace_diagnostics)
    if stable_rows and not actual.issubset(frozenset(stable_rows)):
        diagnostics.append(
            _diagnostic("ARCHIVE-MIGRATION-PARITY", WORK107_MIGRATION_PATH)
        )
    typed_records = tuple(
        ArchiveRecord(path=path, content=content)
        for path, content in sorted(records.items())
    )
    record_report = validate_archive_records(
        root,
        typed_records,
        stable_archive_paths=frozenset(stable_rows),
    )
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
        stable_row = stable_rows.get(record.path)
        if stable_row is not None and any(
            parsed.metadata.get(key) != stable_row[key]
            for key in ("source_commit", "source_blob", "content_sha256")
        ):
            diagnostics.append(_diagnostic("ARCHIVE-MIGRATION-PROVENANCE", record.path))
        original_path = parsed.metadata.get("original_path")
        if isinstance(original_path, str):
            try:
                (root / original_path).lstat()
            except FileNotFoundError:
                pass
            except OSError:
                diagnostics.append(_diagnostic("ARCHIVE-ORIGINAL-READ", record.path))
            else:
                diagnostics.append(
                    _diagnostic("ARCHIVE-ORIGINAL-STILL-CURRENT", record.path)
                )
    try:
        index_text = _read_repository_index(root)
    except ArchiveContractError as exc:
        index_text = ""
        diagnostics.append(_diagnostic(exc.code, ARCHIVE_INDEX.as_posix()))
    index_rows, index_links, index_diagnostics = _parse_repository_index(index_text)
    diagnostics.extend(index_diagnostics)
    if frozenset(index_rows) != actual:
        diagnostics.append(
            _diagnostic("ARCHIVE-INDEX-PARITY", ARCHIVE_INDEX.as_posix())
        )
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
        (namespace, len(namespaces.get(namespace, ()))) for namespace in _NAMESPACE_IDS
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
def _load_canonical_markdown_module() -> ModuleType:
    """Use the Stage99 document owner for parsing and registry-selected validation."""

    script_path = (
        Path(__file__).resolve(strict=True).with_name("validate-markdown-profiles.py")
    )
    module_name = f"_archive_canonical_markdown_{id(_LINK_MODULE_TOKEN):x}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical Markdown owner is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    scripts_path = str(script_path.parent)
    inserted = scripts_path not in sys.path
    if inserted:
        sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
        if inserted:
            sys.path.remove(scripts_path)
    return module


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


def _git_command(
    root: Path,
    *args: str,
    input_bytes: bytes | None = None,
    output_limit: int = _GIT_TREE_OUTPUT_LIMIT,
) -> subprocess.CompletedProcess[bytes]:
    return _git_capture_bounded(
        root,
        *args,
        stdout_limit=output_limit,
        input_bytes=input_bytes,
    )


@lru_cache(maxsize=8)
def _repository_identity(root: Path) -> int:
    """Resolve the repository top level and object format once per root.

    The answer is a property of the checkout, and every archive reader asks for
    it, so probing per call spends the run's whole subprocess budget on a
    constant.
    """

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


def _commit_types(root: Path, commits: tuple[str, ...]) -> dict[str, str | None]:
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
    *,
    original_paths: tuple[str, ...],
    historical_paths: tuple[str, ...],
    object_id_length: int,
    exact_members: Mapping[str, _GitTreeMember] | None = None,
) -> dict[str, _GitTreeMember]:
    paths = tuple(sorted(set(original_paths) | set(historical_paths)))
    _validate_commit_path_requests(paths)
    if exact_members is None:
        exact_by_commit = _batch_commit_path_members(
            root, {commit: paths}, object_id_length
        )
        members = exact_by_commit.get(commit, {})
    else:
        if any(
            path not in paths or not isinstance(member, _GitTreeMember)
            for path, member in exact_members.items()
        ):
            raise ArchiveContractError(
                "RECOVERY-TREE-INVALID", "tree lookup evidence is malformed"
            )
        members = dict(exact_members)
    original_blobs = tuple(
        path
        for path in original_paths
        if (member := members.get(path)) is not None and member.kind == "blob"
    )
    if not original_blobs:
        return members
    modes = _git_command(
        root,
        "ls-tree",
        "-z",
        "--full-tree",
        commit,
        "--",
        *original_blobs,
        output_limit=_GIT_TREE_OUTPUT_LIMIT,
    )
    if modes.returncode:
        raise ArchiveContractError("RECOVERY-TREE-INVALID", "tree lookup failed")
    mode_members = _parse_git_tree_output(
        modes.stdout,
        paths=original_blobs,
        object_id_length=object_id_length,
    )
    for path in original_blobs:
        exact_member = members[path]
        mode_member = mode_members.get(path)
        if (
            mode_member is None
            or mode_member.kind != "blob"
            or mode_member.object_id != exact_member.object_id
        ):
            raise ArchiveContractError(
                "RECOVERY-TREE-INVALID", "tree lookup changed identity"
            )
        members[path] = mode_member
    return members


def _validate_commit_path_requests(paths: tuple[str, ...]) -> None:
    if len(paths) > _GIT_TREE_ENTRY_LIMIT or any(
        "\n" in path or "\r" in path or "\0" in path for path in paths
    ):
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "tree lookup request exceeds its budget"
        )


def _batch_commit_path_members(
    root: Path,
    paths_by_commit: Mapping[str, tuple[str, ...]],
    object_id_length: int,
) -> dict[str, dict[str, _GitTreeMember]]:
    ordered: list[tuple[str, tuple[str, ...]]] = []
    request_lines: list[str] = []
    total = 0
    for commit in sorted(paths_by_commit):
        paths = tuple(sorted(set(paths_by_commit[commit])))
        _validate_commit_path_requests(paths)
        total += len(paths)
        if total > _GIT_TREE_ENTRY_LIMIT:
            raise ArchiveContractError(
                "RECOVERY-RESOURCE-LIMIT", "tree lookup request exceeds its budget"
            )
        ordered.append((commit, paths))
        request_lines.extend(f"{commit}:{path}\n" for path in paths)
    if not request_lines:
        return {}
    requests = "".join(request_lines).encode("utf-8")
    if len(requests) > _GIT_TREE_OUTPUT_LIMIT:
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "tree lookup request exceeds its budget"
        )
    exact = _git_command(
        root,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        input_bytes=requests,
        output_limit=_GIT_TREE_OUTPUT_LIMIT,
    )
    if exact.returncode:
        raise ArchiveContractError("RECOVERY-TREE-INVALID", "tree lookup failed")
    lines = exact.stdout.splitlines()
    if len(lines) != total:
        raise ArchiveContractError("RECOVERY-TREE-INVALID", "tree lookup is incomplete")
    offset = 0
    members_by_commit: dict[str, dict[str, _GitTreeMember]] = {}
    for commit, paths in ordered:
        end = offset + len(paths)
        output = b"\n".join(lines[offset:end])
        members_by_commit[commit] = _parse_git_path_batch_output(
            output,
            paths=paths,
            object_id_length=object_id_length,
            missing_prefix=f"{commit}:",
        )
        offset = end
    return members_by_commit


def _parse_git_tree_output(
    output: bytes,
    *,
    paths: tuple[str, ...],
    object_id_length: int,
    entry_limit: int = _GIT_TREE_ENTRY_LIMIT,
) -> dict[str, _GitTreeMember]:
    if len(output) > _GIT_TREE_OUTPUT_LIMIT:
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "tree output exceeds its budget"
        )
    members: dict[str, _GitTreeMember] = {}
    entry_count = 0
    for raw_record in output.split(b"\0"):
        if not raw_record:
            continue
        entry_count += 1
        if entry_count > entry_limit:
            raise ArchiveContractError(
                "RECOVERY-RESOURCE-LIMIT", "tree entries exceed their budget"
            )
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


def _parse_git_path_batch_output(
    output: bytes,
    *,
    paths: tuple[str, ...],
    object_id_length: int,
    entry_limit: int = _GIT_TREE_ENTRY_LIMIT,
    missing_prefix: str = "",
) -> dict[str, _GitTreeMember]:
    """Parse exact ``commit:path`` batch-check evidence without path disclosure."""

    if (
        len(output) > _GIT_TREE_OUTPUT_LIMIT
        or len(paths) > entry_limit
        or not isinstance(output, bytes)
    ):
        raise ArchiveContractError(
            "RECOVERY-RESOURCE-LIMIT", "tree entries exceed their budget"
        )
    lines = output.splitlines()
    if len(lines) != len(paths):
        raise ArchiveContractError("RECOVERY-TREE-INVALID", "tree lookup is incomplete")
    members: dict[str, _GitTreeMember] = {}
    for path, line in zip(paths, lines, strict=True):
        missing = f"{missing_prefix}{path} missing".encode("utf-8")
        if line == missing:
            continue
        fields = line.split(b" ")
        if len(fields) != 3:
            raise ArchiveContractError(
                "RECOVERY-TREE-INVALID", "tree lookup is malformed"
            )
        raw_object, raw_kind, raw_size = fields
        try:
            object_id = raw_object.decode("ascii", errors="strict")
            kind = raw_kind.decode("ascii", errors="strict")
            size = int(raw_size)
        except (UnicodeDecodeError, ValueError) as exc:
            raise ArchiveContractError(
                "RECOVERY-TREE-INVALID", "tree lookup is malformed"
            ) from exc
        if (
            len(object_id) != object_id_length
            or _FULL_OBJECT_ID.fullmatch(object_id) is None
            or kind not in {"blob", "tree"}
            or size < 0
        ):
            raise ArchiveContractError(
                "RECOVERY-TREE-INVALID", "tree lookup is malformed"
            )
        mode = "040000" if kind == "tree" else "000000"
        members[path] = _GitTreeMember(mode, kind, object_id)
    return members


def _batch_blob_bytes(root: Path, object_ids: tuple[str, ...]) -> dict[str, bytes]:
    """Read every requested blob, one bounded `cat-file --batch` at a time.

    MAX_GIT_BATCH_OBJECTS bounds a single read, not the whole request. Reading
    the request in one call made the budget a cliff instead of a guard: a
    repository sitting at the budget lost its entire recovery proof the moment
    one migration row or historical consumer was added. The aggregate byte
    budget, which is the actual memory bound, is threaded across the reads so
    chunking cannot multiply it. This is the same shape `_current_target_bytes`
    already uses for the current-tree read.
    """

    if not object_ids:
        return {}
    object_id_length = len(object_ids[0])
    blobs: dict[str, bytes] = {}
    remaining_bytes = MAX_GIT_BATCH_BYTES
    for offset in range(0, len(object_ids), MAX_GIT_BATCH_OBJECTS):
        batch = object_ids[offset : offset + MAX_GIT_BATCH_OBJECTS]
        batch_blobs = _read_git_blob_batch(
            root,
            batch,
            object_id_length=object_id_length,
            per_blob_limit=_ARCHIVE_RECORD_LIMIT,
            aggregate_limit=remaining_bytes,
            object_limit=MAX_GIT_BATCH_OBJECTS,
        )
        batch_bytes = sum(len(content) for content in batch_blobs.values())
        if batch_bytes > remaining_bytes:
            raise ArchiveContractError(
                "RECOVERY-RESOURCE-LIMIT", "Git blob bytes exceed their budget"
            )
        remaining_bytes -= batch_bytes
        blobs.update(batch_blobs)
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
    request_groups: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {}
    for commit in commits:
        members = valid_by_commit[commit]
        kind = commit_types.get(commit)
        if kind != "commit":
            code = (
                "RECOVERY-OBJECT-MISSING"
                if kind is None
                else "RECOVERY-OBJECT-NOT-COMMIT"
            )
            errors.update({item.archive_path: code for item in members})
            continue
        originals = {item.original_path for item in members}
        historical = {
            link.target.as_posix()
            for item in members
            for link in item.rendered_links
            if link.kind == "local" and link.target is not None
        }
        request_groups[commit] = (
            tuple(sorted(originals)),
            tuple(sorted(historical)),
        )
    try:
        exact_by_commit = _batch_commit_path_members(
            root,
            {
                commit: tuple(sorted(set(originals) | set(historical)))
                for commit, (originals, historical) in request_groups.items()
            },
            object_id_length,
        )
    except ArchiveContractError as exc:
        errors.update(
            {
                item.archive_path: exc.code
                for commit in request_groups
                for item in valid_by_commit[commit]
            }
        )
        exact_by_commit = {}
    trees: dict[str, dict[str, _GitTreeMember]] = {}
    for commit, (originals, historical) in request_groups.items():
        if any(item.archive_path in errors for item in valid_by_commit[commit]):
            continue
        try:
            trees[commit] = _commit_tree_members(
                root,
                commit,
                original_paths=originals,
                historical_paths=historical,
                object_id_length=object_id_length,
                exact_members=exact_by_commit.get(commit, {}),
            )
        except ArchiveContractError as exc:
            errors.update(
                {item.archive_path: exc.code for item in valid_by_commit[commit]}
            )
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
        errors.update({path: exc.code for path in source_members if path not in errors})
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
    *,
    stable_archive_paths: frozenset[str] = frozenset(),
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
        if (
            archive_path != recovered.proposed_archive_path
            and archive_path not in stable_archive_paths
        ):
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
        migration_control = (
            path in _ARCHIVE_MIGRATION_CONTROLS
            or generic_migration_id(path) is not None
        ) and document.profile == "content/archive-migration"
        archive_record_path = (
            pure_path.is_relative_to(ARCHIVE_ROOT)
            and pure_path != ARCHIVE_INDEX
            and not migration_control
        )
        if current and (
            archive_record_path
            or document.profile == "content/archive"
            or path in canonical_individuals
        ):
            diagnostics.append(_diagnostic("ARCHIVE-REACTIVATED", path))
        if migration_control:
            continue
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
            # Migration ledgers are the declared lookup path from a current
            # document to archived evidence, so they are navigational like the
            # archive index rather than a direct link to an archived record.
            if target_path in canonical_individuals or (
                target.is_relative_to(ARCHIVE_ROOT)
                and target != ARCHIVE_INDEX
                and target_path != _WORK054_WP004B_MIGRATION_PATH
                and generic_migration_id(target_path) is None
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
