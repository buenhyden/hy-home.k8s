#!/usr/bin/env python3
"""Validate the complete ARWB-003 production archive cutover.

Diagnostics contain only stable rule identifiers and canonical repository
paths. Archive payloads, secret matches, values, and line content are never
printed or retained in the report.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Sequence

import yaml

if __package__:
    from scripts.archive_cutover_manifest import (
        ARCHIVE_PROFILE,
        ARCHIVE_TEMPLATE,
        CUTOVER_BASE_COMMIT,
        EXPECTED_ARCHIVE_PATHS,
        EXPECTED_ARCHIVE_RECORDS,
    )
    from scripts.archive_recovery import (
        ArchiveContractError,
        parse_archive_envelope,
    )
    from scripts.archive_validation import (
        ArchiveRecord,
        CurrentMarkdownDocument,
        validate_archive_records,
        validate_current_archive_authority,
    )
else:
    from archive_cutover_manifest import (  # type: ignore[no-redef]
        ARCHIVE_PROFILE,
        ARCHIVE_TEMPLATE,
        CUTOVER_BASE_COMMIT,
        EXPECTED_ARCHIVE_PATHS,
        EXPECTED_ARCHIVE_RECORDS,
    )
    from archive_recovery import (  # type: ignore[no-redef]
        ArchiveContractError,
        parse_archive_envelope,
    )
    from archive_validation import (  # type: ignore[no-redef]
        ArchiveRecord,
        CurrentMarkdownDocument,
        validate_archive_records,
        validate_current_archive_authority,
    )


EXPECTED_HISTORICAL_LINKS = 202
MIGRATION_RESULTS_PATH = "docs/90.references/data/active-corpus-migration-results.json"
FIRST_SOURCE_COMMIT = (
    "5e0221525450dbdacb585e6c98ade3f060ddc827"  # pragma: allowlist secret
)
SECOND_SOURCE_COMMIT = (
    "82f0e1922d9748a88b1487a32a59629ba523f408"  # pragma: allowlist secret
)
ARCHIVE_TEMPLATE_PROFILE = "template/content/archive"
ARCHIVE_INDEX = "docs/98.archive/README.md"
SECRET_DETECTED_EXIT = 17
SECRET_TIMEOUT_SECONDS = 10
_RETIRED_WORD = "tomb" + "stone"
_RETIRED_PROFILE_TOKEN = "archive-" + _RETIRED_WORD

SECOND_SOURCE_ORIGINAL_PATHS = frozenset(
    {
        "docs/03.specs/007-docs-governance-consistency/spec.md",
        "docs/04.execution/plans/2026-05-28-docs-governance-consistency.md",
        "docs/04.execution/tasks/2026-05-28-docs-governance-consistency.md",
        "docs/05.operations/guides/0004-headlamp-auth-oidc-guide.md",
        "docs/05.operations/runbooks/0005-headlamp-keycloak-runbook.md",
    }
)

STALE_CONTRACT_SURFACES = (
    ".github/ABOUT.md",
    "docs/README.md",
    "docs/00.agent-governance/harness-catalog.md",
    "docs/00.agent-governance/scopes/docs.md",
    "docs/00.agent-governance/rules/agentic.md",
    "docs/00.agent-governance/rules/document-stage-routing.md",
    "docs/00.agent-governance/rules/documentation-protocol.md",
    "docs/00.agent-governance/rules/stage-authoring-matrix.md",
    "docs/00.agent-governance/rules/stage-checklists.md",
    "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
    "docs/01.requirements/README.md",
    "docs/02.architecture/README.md",
    "docs/02.architecture/decisions/README.md",
    "docs/02.architecture/requirements/README.md",
    "docs/03.specs/README.md",
    "docs/04.execution/plans/README.md",
    "docs/04.execution/tasks/README.md",
    "docs/05.operations/README.md",
    "docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md",
    "docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md",
    "docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md",
    "docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md",
    "docs/99.templates/README.md",
    "docs/99.templates/templates/README.md",
    "docs/99.templates/support/common-documentation-governance.md",
    "docs/99.templates/support/documentation-contract.md",
    "docs/99.templates/support/frontmatter-schema.md",
    "docs/99.templates/support/legacy-cleanup-rules.md",
    "docs/99.templates/support/sdlc-governance.md",
    "scripts/README.md",
    "scripts/validate-links-and-owners.py",
    "scripts/validate-markdown-profiles.py",
    "scripts/validate-repo-quality-gates.sh",
    "tests/fixtures/document-lifecycle.json",
    "tests/fixtures/links-and-owners.json",
    "tests/fixtures/markdown-profiles.json",
    "tests/README.md",
)


@dataclass(frozen=True)
class CutoverDiagnostic:
    """One stable, redacted production diagnostic."""

    code: str
    path: str


@dataclass(frozen=True)
class CutoverReport:
    """Aggregate atomic-cutover result."""

    diagnostics: tuple[CutoverDiagnostic, ...]
    record_count: int
    historical_link_count: int
    secret_clean_count: int

    @property
    def valid(self) -> bool:
        return not self.diagnostics


@dataclass(frozen=True)
class ArchiveIndexRow:
    """One structured archive-index row keyed by canonical archive path."""

    archive_path: str
    original_path: str
    original_type: str
    source_commit: str
    source_blob: str
    content_sha256: str
    historical_links: int
    replacement: str | None
    reason: str


def _diagnostic(code: str, path: str) -> CutoverDiagnostic:
    return CutoverDiagnostic(code=code, path=path)


def _source_commit(original_path: str) -> str:
    return (
        SECOND_SOURCE_COMMIT
        if original_path in SECOND_SOURCE_ORIGINAL_PATHS
        else FIRST_SOURCE_COMMIT
    )


def _safe_git_environment() -> dict[str, str]:
    """Return the recovery-grade Git environment for every cutover lookup."""

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


def _git_paths(root: Path) -> tuple[str, ...]:
    try:
        completed = subprocess.run(
            [
                "git",
                "--no-replace-objects",
                "--literal-pathspecs",
                "-C",
                str(root),
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "docs",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=SECRET_TIMEOUT_SECONDS,
            env=_safe_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        raise RuntimeError("tracked document inventory is unavailable") from None
    if completed.returncode != 0 or not completed.stdout.endswith(b"\0"):
        raise RuntimeError("tracked document inventory is unavailable")
    try:
        return tuple(
            sorted(
                record.decode("utf-8")
                for record in completed.stdout.split(b"\0")[:-1]
                if record
            )
        )
    except UnicodeDecodeError as exc:
        raise RuntimeError("tracked document inventory is malformed") from exc


def _regular_file(root: Path, raw_path: str) -> bool:
    try:
        mode = (root / raw_path).lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode)


def _frontmatter_identity(text: str, path: str) -> tuple[str, str]:
    if path.endswith("/README.md") or path == "docs/README.md":
        return "readme/repository", "active"
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return "content/reference", "active"
    raw = text.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError:
        return "content/reference", "active"
    if not isinstance(loaded, dict):
        return "content/reference", "active"
    profile = loaded.get("type")
    status = loaded.get("status")
    return (
        profile if isinstance(profile, str) else "content/reference",
        status if isinstance(status, str) else "active",
    )


def _secret_classifier(
    root: Path,
    archive_path: str,
    payload: bytes,
) -> CutoverDiagnostic | None:
    executable = shutil.which("gitleaks")
    if executable is None:
        return _diagnostic("ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE", archive_path)
    try:
        completed = subprocess.run(
            [
                executable,
                "detect",
                "--pipe",
                "--config",
                str(root / ".gitleaks.toml"),
                "--redact=100",
                "--no-banner",
                "--no-color",
                "--log-level",
                "error",
                "--timeout",
                str(SECRET_TIMEOUT_SECONDS),
                "--exit-code",
                str(SECRET_DETECTED_EXIT),
            ],
            input=payload,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=SECRET_TIMEOUT_SECONDS * 2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return _diagnostic("ARCHIVE-SECRET-CLASSIFIER-ERROR", archive_path)
    if completed.returncode == SECRET_DETECTED_EXIT:
        return _diagnostic("ARCHIVE-SECRET-DETECTED", archive_path)
    if completed.returncode != 0:
        return _diagnostic("ARCHIVE-SECRET-CLASSIFIER-ERROR", archive_path)
    return None


_INDEX_COLUMNS = (
    "Archive Record",
    "Original Path",
    "Original Type",
    "Source Commit",
    "Source Blob",
    "Payload SHA-256",
    "Historical Links",
    "Current Replacement",
    "Reason",
)
_INDEX_HEADER = "| " + " | ".join(_INDEX_COLUMNS) + " |"
_INDEX_SEPARATOR = "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |"
_MARKDOWN_LINK = re.compile(r"\[`(?P<label>[^`]+)`\]\((?P<target>[^)]+)\)")
_CODE_CELL = re.compile(r"`(?P<value>[^`]+)`")
_INDEX_MANIFEST = re.compile(
    r"<!-- archive-manifest:v1 records=(?P<records>\d+) "
    r"historical-links=(?P<links>\d+) -->"
)


def _index_target(target: str) -> str | None:
    if not target.startswith("./"):
        return None
    normalized = posixpath.normpath(posixpath.join("docs/98.archive", target))
    if not normalized.startswith("docs/98.archive/"):
        return None
    return normalized


def _replacement_target(label: str, target: str) -> str | None:
    if not target.startswith("../"):
        return None
    normalized = posixpath.normpath(posixpath.join("docs/98.archive", target))
    if normalized != label or not normalized.startswith("docs/"):
        return None
    return normalized


@lru_cache(maxsize=1)
def _load_migration_validator() -> ModuleType:
    """Load the additive ACER validator from its canonical CLI module."""

    path = Path(__file__).resolve(strict=True).with_name(
        "validate-active-corpus-migrations.py"
    )
    spec = importlib.util.spec_from_file_location(
        "_archive_cutover_active_corpus_migrations", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("migration validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if Path(str(getattr(module, "__file__", ""))).resolve(strict=True) != path:
        raise RuntimeError("migration validator is unavailable")
    return module


def _migration_projection(
    root: Path,
) -> tuple[dict[str, dict[str, object]], dict[str, int]]:
    """Return only records admitted by the closed eligible-prefix ledger."""

    module = _load_migration_validator()
    eligibility, document = module.load_documents(root)
    counts = module.validate_ledger_document(document, eligibility)
    rows: dict[str, dict[str, object]] = {}
    for batch in document["batches"]:
        for row in batch["records"]:
            projected = dict(row)
            projected["_currentClosureOwner"] = batch["currentClosureOwner"]
            projected["_archiveNavigationBoundary"] = batch[
                "archiveNavigationBoundary"
            ]
            rows[str(row["archivePath"])] = projected
    if len(rows) != counts["records"]:
        raise RuntimeError("migration validator returned an invalid projection")
    return rows, dict(counts)


def _parse_index_row(line: str) -> ArchiveIndexRow | None:
    cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
    if len(cells) != len(_INDEX_COLUMNS):
        return None
    record_match = _MARKDOWN_LINK.fullmatch(cells[0])
    code_matches = tuple(_CODE_CELL.fullmatch(cells[index]) for index in range(1, 6))
    reason_match = _CODE_CELL.fullmatch(cells[8])
    if (
        record_match is None
        or any(match is None for match in code_matches)
        or reason_match is None
        or not cells[6].isdigit()
    ):
        return None
    archive_path = _index_target(record_match.group("target"))
    reason = reason_match.group("value")
    if cells[7] == "`null`":
        replacement = None
        if reason != "completed-lineage":
            return None
    else:
        replacement_match = _MARKDOWN_LINK.fullmatch(cells[7])
        if replacement_match is None or reason not in {
            "superseded",
            "consolidated",
            "duplicate",
        }:
            return None
        replacement = _replacement_target(
            replacement_match.group("label"), replacement_match.group("target")
        )
    if (
        archive_path is None
        or (reason != "completed-lineage" and replacement is None)
        or record_match.group("label") != archive_path.removeprefix("docs/98.archive/")
    ):
        return None
    values = tuple(match.group("value") for match in code_matches if match is not None)
    return ArchiveIndexRow(
        archive_path=archive_path,
        original_path=values[0],
        original_type=values[1],
        source_commit=values[2],
        source_blob=values[3],
        content_sha256=values[4],
        historical_links=int(cells[6]),
        replacement=replacement,
        reason=reason,
    )


def _parse_archive_index(
    index_text: str,
) -> tuple[dict[str, ArchiveIndexRow], bool]:
    """Parse the one exact manifest table and return rows plus structure failure."""

    lines = index_text.splitlines()
    header_offsets = [
        offset for offset, line in enumerate(lines) if line == _INDEX_HEADER
    ]
    if len(header_offsets) != 1:
        return {}, True
    header_offset = header_offsets[0]
    if header_offset + 1 >= len(lines) or lines[header_offset + 1] != _INDEX_SEPARATOR:
        return {}, True
    raw_rows: list[str] = []
    for line in lines[header_offset + 2 :]:
        if not line.startswith("|"):
            break
        raw_rows.append(line)
    manifest_end = header_offset + 2 + len(raw_rows)
    rows: dict[str, ArchiveIndexRow] = {}
    structure_failure = not raw_rows or any(
        line.startswith("|")
        for offset, line in enumerate(lines)
        if not header_offset <= offset < manifest_end
    )
    for raw_row in raw_rows:
        row = _parse_index_row(raw_row)
        if row is None or row.archive_path in rows:
            structure_failure = True
            continue
        rows[row.archive_path] = row
    return rows, structure_failure


@lru_cache(maxsize=4)
def _finite_cutover_base_diagnostics(root: Path) -> tuple[CutoverDiagnostic, ...]:
    """Prove the exact 31-record legacy conversion without restoring its route."""

    diagnostics: list[CutoverDiagnostic] = []
    git_environment = _safe_git_environment()
    for archive_path in EXPECTED_ARCHIVE_PATHS:
        try:
            completed = subprocess.run(
                [
                    "git",
                    "--no-replace-objects",
                    "--literal-pathspecs",
                    "-C",
                    str(root),
                    "cat-file",
                    "blob",
                    f"{CUTOVER_BASE_COMMIT}:{archive_path}",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=SECRET_TIMEOUT_SECONDS,
                env=git_environment,
            )
            if completed.returncode != 0:
                raise ValueError
            text = completed.stdout.decode("utf-8")
            if not text.startswith("---\n") or "\n---\n" not in text[4:]:
                raise ValueError
            metadata = yaml.safe_load(text.split("\n---\n", 1)[0][4:])
        except (
            UnicodeDecodeError,
            ValueError,
            yaml.YAMLError,
            OSError,
            subprocess.TimeoutExpired,
        ):
            diagnostics.append(_diagnostic("ARCHIVE-FINITE-ADMISSION", archive_path))
            continue
        if (
            not isinstance(metadata, dict)
            or metadata.get("type") != f"content/{_RETIRED_PROFILE_TOKEN}"
            or metadata.get("status") != "archived"
        ):
            diagnostics.append(_diagnostic("ARCHIVE-FINITE-ADMISSION", archive_path))
    return tuple(diagnostics)


def validate_repository_cutover(repository_root: str | Path) -> CutoverReport:
    """Validate one complete production snapshot and reject every partial state."""

    try:
        root = Path(repository_root).resolve(strict=True)
        if not root.is_dir():
            raise OSError
    except (OSError, RuntimeError, TypeError):
        return CutoverReport(
            diagnostics=(
                _diagnostic("ARCHIVE-CUTOVER-INCOMPLETE", "<repository>"),
                _diagnostic("ARCHIVE-ROOT-UNAVAILABLE", "<repository>"),
            ),
            record_count=0,
            historical_link_count=0,
            secret_clean_count=0,
        )
    diagnostics: list[CutoverDiagnostic] = list(_finite_cutover_base_diagnostics(root))
    try:
        migration_rows, migration_counts = _migration_projection(root)
    except Exception:
        migration_rows = {}
        migration_counts = {
            "records": 0,
            "historicalLinksAdded": 0,
        }
        diagnostics.append(
            _diagnostic("ARCHIVE-MIGRATION-LEDGER", MIGRATION_RESULTS_PATH)
        )
    base_paths = frozenset(EXPECTED_ARCHIVE_PATHS)
    expected_paths = base_paths | frozenset(migration_rows)
    expected_records = EXPECTED_ARCHIVE_RECORDS + migration_counts["records"]
    expected_historical_links = (
        EXPECTED_HISTORICAL_LINKS + migration_counts["historicalLinksAdded"]
    )
    present_paths = frozenset(
        path for path in expected_paths if _regular_file(root, path)
    )
    if present_paths != expected_paths:
        diagnostics.append(_diagnostic("ARCHIVE-CORPUS-INCOMPLETE", ARCHIVE_INDEX))

    records: list[ArchiveRecord] = []
    metadata_rows: list[tuple[str, dict[str, object], int]] = []
    secret_clean_count = 0
    for archive_path in sorted(expected_paths):
        if archive_path not in present_paths:
            continue
        try:
            content = (root / archive_path).read_bytes()
            parsed = parse_archive_envelope(content)
        except (OSError, ArchiveContractError):
            diagnostics.append(_diagnostic("ARCHIVE-ENVELOPE-INVALID", archive_path))
            continue
        original_path = parsed.metadata.get("original_path")
        expected_source_commit = (
            migration_rows[archive_path].get("sourceCommit")
            if archive_path in migration_rows
            else _source_commit(str(original_path))
        )
        if (
            not isinstance(original_path, str)
            or parsed.metadata.get("source_commit") != expected_source_commit
        ):
            diagnostics.append(_diagnostic("ARCHIVE-SOURCE-OWNERSHIP", archive_path))
            continue
        secret_diagnostic = _secret_classifier(root, archive_path, parsed.payload)
        if secret_diagnostic is not None:
            diagnostics.append(secret_diagnostic)
            continue
        secret_clean_count += 1
        record = ArchiveRecord(path=archive_path, content=content)
        records.append(record)
        focused = validate_archive_records(root, (record,))
        if not focused.valid:
            diagnostics.extend(
                _diagnostic(item.code, item.path) for item in focused.diagnostics
            )
            continue
        metadata_rows.append(
            (archive_path, dict(parsed.metadata), focused.historical_link_count)
        )

    archive_report = validate_archive_records(root, tuple(records))
    diagnostics.extend(
        _diagnostic(item.code, item.path) for item in archive_report.diagnostics
    )
    if (
        len(records) != expected_records
        or archive_report.historical_link_count != expected_historical_links
    ):
        diagnostics.append(_diagnostic("ARCHIVE-EVIDENCE-COUNT", ARCHIVE_INDEX))
    base_report = validate_archive_records(
        root,
        tuple(record for record in records if record.path in base_paths),
    )
    if (
        not base_report.valid
        or len(tuple(record for record in records if record.path in base_paths))
        != EXPECTED_ARCHIVE_RECORDS
        or base_report.historical_link_count != EXPECTED_HISTORICAL_LINKS
    ):
        diagnostics.append(_diagnostic("ARCHIVE-FINITE-BASE", ARCHIVE_INDEX))

    original_paths = [row[1].get("original_path") for row in metadata_rows]
    if len(original_paths) != len(set(original_paths)):
        diagnostics.append(
            _diagnostic("ARCHIVE-ORIGINAL-OWNER-DUPLICATE", ARCHIVE_INDEX)
        )
    for archive_path, metadata, _link_count in metadata_rows:
        original_path = metadata.get("original_path")
        replacement = metadata.get("replacement")
        if isinstance(original_path, str) and _regular_file(root, original_path):
            diagnostics.append(
                _diagnostic("ARCHIVE-ORIGINAL-STILL-CURRENT", archive_path)
            )
        reason = metadata.get("archive_reason")
        if reason == "completed-lineage":
            migration = migration_rows.get(archive_path)
            if (
                replacement is not None
                or migration is None
                or not _regular_file(
                    root,
                    str(migration.get("_currentClosureOwner", "<invalid-path>")),
                )
                or migration.get("_archiveNavigationBoundary")
                != f"{ARCHIVE_INDEX}#document-index"
            ):
                diagnostics.append(
                    _diagnostic("ARCHIVE-REPLACEMENT-MISSING", archive_path)
                )
        elif not isinstance(replacement, str) or not _regular_file(root, replacement):
            diagnostics.append(
                _diagnostic("ARCHIVE-REPLACEMENT-MISSING", archive_path)
            )

    registry_path = root / "docs/99.templates/support/document-profiles.json"
    try:
        loaded_registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        loaded_registry = {}
    if isinstance(loaded_registry, dict):
        registry = loaded_registry
    else:
        registry = {}
    profiles = registry.get("profiles", ())
    profile_ids = [
        profile.get("id") for profile in profiles if isinstance(profile, dict)
    ]
    if (
        registry.get("schemaVersion") != 8
        or profile_ids.count(ARCHIVE_PROFILE) != 1
        or profile_ids.count(ARCHIVE_TEMPLATE_PROFILE) != 1
        or _RETIRED_WORD in json.dumps(registry, ensure_ascii=False).lower()
        or not _regular_file(root, ARCHIVE_TEMPLATE)
        or (
            root
            / "docs/99.templates/templates/common"
            / (_RETIRED_PROFILE_TOKEN + ".template.md")
        ).exists()
    ):
        diagnostics.append(
            _diagnostic(
                "ARCHIVE-AUTHORITY-INCOMPLETE",
                registry_path.relative_to(root).as_posix(),
            )
        )

    try:
        index_text = (root / ARCHIVE_INDEX).read_text(encoding="utf-8")
    except OSError:
        index_text = ""
    index_rows, index_structure_failure = _parse_archive_index(index_text)
    index_links = sum(row.historical_links for row in index_rows.values())
    markers = tuple(_INDEX_MANIFEST.finditer(index_text))
    marker_valid = (
        len(markers) == 1
        and int(markers[0].group("records")) == len(index_rows)
        and int(markers[0].group("links")) == index_links
        and len(index_rows) == expected_records
        and index_links == expected_historical_links
    )
    if not marker_valid:
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-MANIFEST", ARCHIVE_INDEX))
    if index_structure_failure or frozenset(index_rows) != expected_paths:
        diagnostics.append(_diagnostic("ARCHIVE-INDEX-STRUCTURE", ARCHIVE_INDEX))
    for archive_path, metadata, link_count in metadata_rows:
        index_row = index_rows.get(archive_path)
        expected_row = ArchiveIndexRow(
            archive_path=archive_path,
            original_path=str(metadata.get("original_path")),
            original_type=str(metadata.get("original_type")),
            source_commit=str(metadata.get("source_commit")),
            source_blob=str(metadata.get("source_blob")),
            content_sha256=str(metadata.get("content_sha256")),
            historical_links=link_count,
            replacement=metadata.get("replacement")
            if isinstance(metadata.get("replacement"), str)
            else None,
            reason=str(metadata.get("archive_reason")),
        )
        if index_row != expected_row:
            diagnostics.append(_diagnostic("ARCHIVE-INDEX-MEMBER", archive_path))

    current_documents: list[CurrentMarkdownDocument] = []
    try:
        current_paths = _git_paths(root)
    except RuntimeError:
        current_paths = ()
        diagnostics.append(_diagnostic("ARCHIVE-CURRENT-INVENTORY", "docs"))
    for raw_path in current_paths:
        if (
            not raw_path.endswith(".md")
            or raw_path == ARCHIVE_INDEX
            or raw_path in expected_paths
            or raw_path.startswith("docs/99.templates/templates/")
            or not _regular_file(root, raw_path)
        ):
            continue
        try:
            markdown = (root / raw_path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            diagnostics.append(_diagnostic("ARCHIVE-CURRENT-READ", raw_path))
            continue
        profile, _status = _frontmatter_identity(markdown, raw_path)
        current_documents.append(
            CurrentMarkdownDocument(
                path=raw_path,
                markdown=markdown,
                profile=profile,
                status="active",
            )
        )
    current_report = validate_current_archive_authority(
        tuple(current_documents),
        individual_archive_paths=expected_paths,
    )
    diagnostics.extend(
        _diagnostic(item.code, item.path) for item in current_report.diagnostics
    )

    for raw_path in STALE_CONTRACT_SURFACES:
        try:
            text = (root / raw_path).read_text(encoding="utf-8")
        except OSError:
            diagnostics.append(
                _diagnostic("ARCHIVE-CONTRACT-SURFACE-MISSING", raw_path)
            )
            continue
        if _RETIRED_WORD in text.lower():
            diagnostics.append(_diagnostic("ARCHIVE-RETIRED-AUTHORITY", raw_path))

    unique = tuple(
        sorted(
            set(diagnostics),
            key=lambda item: (item.path, item.code),
        )
    )
    if unique and not any(item.code == "ARCHIVE-CUTOVER-INCOMPLETE" for item in unique):
        unique = (
            _diagnostic("ARCHIVE-CUTOVER-INCOMPLETE", "<repository>"),
            *unique,
        )
    return CutoverReport(
        diagnostics=unique,
        record_count=len(records),
        historical_link_count=archive_report.historical_link_count,
        secret_clean_count=secret_clean_count,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    report = validate_repository_cutover(args.root)
    if report.valid:
        print(
            "PASS archive cutover "
            f"records={report.record_count} "
            f"historical_links={report.historical_link_count} "
            f"secret_clean={report.secret_clean_count}"
        )
        return 0
    for diagnostic in report.diagnostics:
        print(f"FAIL {diagnostic.code} path={diagnostic.path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
