#!/usr/bin/env python3
"""Validate closed ACER-003 migration results and additive archive state.

The immutable ARWB-003 31-record/202-link proof remains owned by
``archive_cutover.py``.  This validator joins only reviewed ACER-002 eligible
pairs to a deterministic complete prefix, validates every additive archive
record byte-for-byte, and derives the aggregate archive-index totals.
Diagnostics contain only fixed rule identifiers and canonical repository paths.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

try:
    from scripts.archive_cutover_manifest import EXPECTED_ARCHIVE_PATHS
    from scripts.archive_recovery import ArchiveContractError, parse_archive_envelope
    from scripts.archive_validation import (
        ArchiveRecord,
        CurrentMarkdownDocument,
        validate_archive_records,
        validate_current_archive_authority,
    )
except ModuleNotFoundError:  # Direct execution from scripts/.
    from archive_cutover_manifest import EXPECTED_ARCHIVE_PATHS  # type: ignore[no-redef]
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


SCHEMA = "active-corpus-migration-results.v1"
SCHEMA_VERSION = 1
LEDGER_PATH = "docs/90.references/data/active-corpus-migration-results.json"
CENSUS_PATH = "docs/90.references/data/active-corpus-retention-census.json"
ELIGIBILITY_PATH = "docs/90.references/data/active-corpus-eligibility-ledger.json"
ARCHIVE_INDEX_PATH = "docs/98.archive/README.md"
ARCHIVE_INDEX_ANCHOR = f"{ARCHIVE_INDEX_PATH}#document-index"
OWNER_SPEC = "docs/03.specs/037-active-corpus-and-execution-retention/spec.md"
CANDIDATE_SOURCE_COMMIT = "a12aedfb71ccabd329dabc83bd2863474d1126b0"  # pragma: allowlist secret
ELIGIBILITY_CONTENT_COMMIT = "414905ce4219a6c98088115485b37ad084e2951a"  # pragma: allowlist secret
ELIGIBILITY_EVIDENCE_COMMIT = "e251915f216ef7cf3c7eb9945cdab6cb429ab6e6"  # pragma: allowlist secret
FIRST_ROLLBACK_PARENT = "90d496e4e96c172785eb23071173a7751e688fd1"  # pragma: allowlist secret
SECOND_ROLLBACK_PARENT = "b390d54cab5c4b94960878f8d7f4fd887d18a132"  # pragma: allowlist secret
THIRD_ROLLBACK_PARENT = "22ad025ed7beb0725095d1ab413a2d5c49f8561c"  # pragma: allowlist secret
FOURTH_ROLLBACK_PARENT = "fdb65db785a4518836ddf22a102b30eb7c9c1d61"  # pragma: allowlist secret
THREE_BATCH_PREFIX_SHA256 = (
    "4269561e827a7a78f0d511d7db829aec72ed806fec831a3030e04f7dab70a27b"  # pragma: allowlist secret
)
ACCEPTED_BATCHES = 4
BASE_RECORDS = 31
BASE_HISTORICAL_LINKS = 202
GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 20
MAX_JSON_BYTES = 3_000_000
MAX_MARKDOWN_BYTES = 3_000_000
FULL_OID = re.compile(r"[0-9a-f]{40}\Z")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
MARKER = re.compile(
    r"<!-- archive-manifest:v1 records=(?P<records>\d+) "
    r"historical-links=(?P<links>\d+) -->"
)

REQUIRED_SELF_TEST_CASES = {
    "partial-second-pair",
    "skipped-first-eligible-batch",
    "skipped-second-eligible-batch",
    "skipped-third-eligible-batch",
    "skipped-fourth-eligible-batch",
    "reordered-eligible-batches",
    "prior-batch-evidence-drift",
    "prior-second-batch-drift",
    "prior-third-batch-drift",
    "partial-fourth-pair",
    "source-still-current",
    "archive-payload-byte-drift",
    "wrong-first-rollback-parent",
    "wrong-second-rollback-parent",
    "wrong-third-rollback-parent",
    "wrong-fourth-rollback-parent",
    "missing-index-row",
    "duplicate-index-row",
    "direct-current-link",
    "duplicate-original-owner",
    "rogue-extra-archive",
    "unsafe-path",
    "hostile-git-steering",
    "self-referential-batch-commit",
}

TOP_KEYS = (
    "$schema",
    "schemaVersion",
    "ownerSpec",
    "censusInput",
    "eligibilityInput",
    "candidateSourceCommit",
    "eligibilityEvidenceSnapshotCommit",
    "archiveBase",
    "archiveIndex",
    "counts",
    "batches",
)
BASE_KEYS = ("proof", "records", "historicalLinks")
COUNT_KEYS = (
    "batches",
    "records",
    "archiveRecords",
    "historicalLinksAdded",
    "historicalLinks",
)
BATCH_KEYS = (
    "sequence",
    "batchId",
    "pairKey",
    "status",
    "completedOn",
    "upstreamSpec",
    "program",
    "currentClosureOwner",
    "archiveNavigationBoundary",
    "rollbackParentCommit",
    "repairedConsumers",
    "validationResult",
    "records",
)
PROGRAM_KEYS = ("prd", "ard", "lineage")
RECORD_KEYS = (
    "kind",
    "originalPath",
    "archivePath",
    "originalType",
    "sourceCommit",
    "sourceBlob",
    "payloadBytes",
    "payloadSha256",
    "historicalLinks",
    "archiveReason",
    "replacement",
    "validationResult",
)
FIRST_REPAIRED_CONSUMERS = (
    "docs/03.specs/031-affected-surface-agent-qa/spec.md",
    "docs/03.specs/README.md",
    "docs/04.execution/plans/README.md",
    "docs/04.execution/tasks/README.md",
    "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md",
    "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
)
SECOND_REPAIRED_CONSUMERS = (
    "docs/03.specs/032-protected-surface-supply-chain-hardening/spec.md",
    "docs/03.specs/README.md",
    "docs/04.execution/plans/README.md",
    "docs/04.execution/tasks/README.md",
    "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md",
    "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
)
THIRD_REPAIRED_CONSUMERS = (
    "docs/03.specs/033-template-lifecycle-contract-normalization/spec.md",
    "docs/04.execution/plans/README.md",
    "docs/04.execution/tasks/README.md",
    "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md",
    "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
)
FOURTH_REPAIRED_CONSUMERS = (
    "docs/03.specs/034-authority-and-lineage-foundation/spec.md",
    "docs/04.execution/plans/2026-07-16-document-schema-and-lifecycle-contract.md",
    "docs/04.execution/plans/README.md",
    "docs/04.execution/tasks/2026-07-16-document-schema-and-lifecycle-contract.md",
    "docs/04.execution/tasks/README.md",
    "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
)
REPAIRED_CONSUMERS_BY_SEQUENCE = (
    FIRST_REPAIRED_CONSUMERS,
    SECOND_REPAIRED_CONSUMERS,
    THIRD_REPAIRED_CONSUMERS,
    FOURTH_REPAIRED_CONSUMERS,
)
ROLLBACK_PARENTS = (
    FIRST_ROLLBACK_PARENT,
    SECOND_ROLLBACK_PARENT,
    THIRD_ROLLBACK_PARENT,
    FOURTH_ROLLBACK_PARENT,
)

INDEX_COLUMNS = (
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
INDEX_HEADER = "| " + " | ".join(INDEX_COLUMNS) + " |"
INDEX_SEPARATOR = "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |"
MARKDOWN_LINK = re.compile(r"\[`(?P<label>[^`]+)`\]\((?P<target>[^)]+)\)")
CODE_CELL = re.compile(r"`(?P<value>[^`]+)`")


class MigrationError(ValueError):
    """One value-free migration failure."""

    def __init__(self, code: str, path: str = LEDGER_PATH) -> None:
        super().__init__(f"{code} {path}")
        self.code = code
        self.path = path


def _fail(code: str, path: str = LEDGER_PATH) -> None:
    raise MigrationError(code, path)


def _exact_keys(value: object, keys: tuple[str, ...], code: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or tuple(value) != keys:
        _fail(code)
    return value


def _exact_list(value: object, code: str) -> list[Any]:
    if not isinstance(value, list):
        _fail(code)
    return value


def _string(value: object, code: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(code)
    return value


def _integer(value: object, code: str) -> int:
    if type(value) is not int or value < 0:
        _fail(code)
    return value


def validate_path(value: object) -> str:
    """Require one canonical docs path without exposing rejected input."""

    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        _fail("MIGRATION-PATH")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or path.as_posix() != value
        or not path.parts
        or path.parts[0] != "docs"
        or "." in path.parts
        or ".." in path.parts
        or "_workspace" in path.parts
    ):
        _fail("MIGRATION-PATH")
    return path.as_posix()


def _validate_anchor(value: object) -> str:
    if value != ARCHIVE_INDEX_ANCHOR:
        _fail("MIGRATION-SCHEMA")
    return str(value)


def safe_git_environment() -> dict[str, str]:
    """Drop Git steering and retain only a deterministic executable path."""

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
            "GIT_PAGER": "cat",
            "GIT_LITERAL_PATHSPECS": "1",
            "HOME": "/nonexistent",
            "LANG": "C",
            "LC_ALL": "C",
            "PAGER": "cat",
            "PATH": "/usr/bin:/bin",
        }
    )
    return environment


@contextmanager
def _closed_git_environment():
    original = dict(os.environ)
    os.environ.clear()
    os.environ.update(safe_git_environment())
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            [
                GIT_EXECUTABLE,
                "--no-replace-objects",
                "--literal-pathspecs",
                "-C",
                str(root),
                *args,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=GIT_TIMEOUT_SECONDS,
            env=safe_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        _fail("MIGRATION-GIT")


def _require_root(value: str | Path) -> Path:
    try:
        root = Path(value).resolve(strict=True)
    except (OSError, RuntimeError, TypeError):
        _fail("MIGRATION-ROOT")
    if not root.is_dir():
        _fail("MIGRATION-ROOT")
    completed = _git(root, "rev-parse", "--show-toplevel")
    try:
        reported = Path(completed.stdout.decode("utf-8").strip()).resolve(strict=True)
    except (OSError, UnicodeDecodeError):
        _fail("MIGRATION-ROOT")
    if completed.returncode != 0 or reported != root:
        _fail("MIGRATION-ROOT")
    return root


def _load_json(path: Path) -> Mapping[str, Any]:
    try:
        if path.stat().st_size > MAX_JSON_BYTES:
            _fail("MIGRATION-JSON")
        raw = path.read_bytes()
    except OSError:
        _fail("MIGRATION-JSON")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                _fail("MIGRATION-JSON")
            value[key] = item
        return value

    try:
        loaded = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("MIGRATION-JSON")
    if not isinstance(loaded, Mapping):
        _fail("MIGRATION-JSON")
    return loaded


def load_documents(repository_root: str | Path) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    root = _require_root(repository_root)
    return _load_json(root / ELIGIBILITY_PATH), _load_json(root / LEDGER_PATH)


def _eligible_pairs(eligibility: Mapping[str, Any]) -> tuple[str, ...]:
    if (
        eligibility.get("$schema") != "active-corpus-eligibility-ledger.v1"
        or eligibility.get("candidateSourceCommit") != CANDIDATE_SOURCE_COMMIT
        or eligibility.get("evidenceSnapshotCommit") != ELIGIBILITY_EVIDENCE_COMMIT
    ):
        _fail("MIGRATION-ELIGIBILITY-INPUT")
    rows = eligibility.get("candidateRows")
    if not isinstance(rows, list):
        _fail("MIGRATION-ELIGIBILITY-INPUT")
    kinds: dict[str, set[str]] = {}
    order: list[str] = []
    for row in rows:
        if not isinstance(row, Mapping) or row.get("disposition") != "eligible":
            continue
        pair = row.get("pairKey")
        kind = row.get("kind")
        if not isinstance(pair, str) or kind not in {"plan", "task"}:
            _fail("MIGRATION-ELIGIBILITY-INPUT")
        if pair not in kinds:
            kinds[pair] = set()
            order.append(pair)
        kinds[pair].add(str(kind))
    if not order or any(kinds[pair] != {"plan", "task"} for pair in order):
        _fail("MIGRATION-ELIGIBILITY-INPUT")
    return tuple(order)


def _eligibility_rows(eligibility: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    raw_rows = eligibility.get("candidateRows")
    if not isinstance(raw_rows, list):
        _fail("MIGRATION-ELIGIBILITY-INPUT")
    for row in raw_rows:
        if not isinstance(row, Mapping) or row.get("disposition") != "eligible":
            continue
        path = validate_path(row.get("path"))
        if path in rows:
            _fail("MIGRATION-ELIGIBILITY-INPUT")
        rows[path] = row
    return rows


def _spec_path(pair_key: str, spec: str) -> str:
    parts = pair_key.split("-", 3)
    if len(parts) != 4 or not spec.isdigit() or len(spec) != 3:
        _fail("MIGRATION-ELIGIBILITY-INPUT")
    return f"docs/03.specs/{spec}-{parts[3]}/spec.md"


def validate_ledger_document(
    document: Mapping[str, Any], eligibility: Mapping[str, Any]
) -> dict[str, int]:
    """Validate the closed result schema and exact reviewed eligible prefix."""

    top = _exact_keys(document, TOP_KEYS, "MIGRATION-SCHEMA")
    if (
        top["$schema"] != SCHEMA
        or top["schemaVersion"] != SCHEMA_VERSION
        or top["ownerSpec"] != OWNER_SPEC
        or top["censusInput"] != CENSUS_PATH
        or top["eligibilityInput"] != ELIGIBILITY_PATH
        or top["candidateSourceCommit"] != CANDIDATE_SOURCE_COMMIT
        or top["eligibilityEvidenceSnapshotCommit"] != ELIGIBILITY_EVIDENCE_COMMIT
        or top["archiveIndex"] != ARCHIVE_INDEX_ANCHOR
    ):
        _fail("MIGRATION-SCHEMA")
    base = _exact_keys(top["archiveBase"], BASE_KEYS, "MIGRATION-SCHEMA")
    if base != {
        "proof": "ARWB-003",
        "records": BASE_RECORDS,
        "historicalLinks": BASE_HISTORICAL_LINKS,
    }:
        _fail("MIGRATION-BASE")
    counts = _exact_keys(top["counts"], COUNT_KEYS, "MIGRATION-SCHEMA")
    batches = _exact_list(top["batches"], "MIGRATION-SCHEMA")
    if len(batches) != ACCEPTED_BATCHES:
        _fail("MIGRATION-ELIGIBLE-PREFIX")

    eligible_order = _eligible_pairs(eligibility)
    eligible_rows = _eligibility_rows(eligibility)
    pair_keys: list[str] = []
    record_total = 0
    historical_total = 0
    repaired_total = 0
    original_owners: set[str] = set()

    for offset, raw_batch in enumerate(batches, start=1):
        batch = _exact_keys(raw_batch, BATCH_KEYS, "MIGRATION-SCHEMA")
        pair_key = _string(batch["pairKey"], "MIGRATION-SCHEMA")
        pair_keys.append(pair_key)
        if pair_keys != list(eligible_order[:offset]):
            _fail("MIGRATION-ELIGIBLE-PREFIX")
        if (
            batch["sequence"] != offset
            or batch["batchId"] != f"ACER-003-{offset:03d}"
            or batch["status"] != "complete"
            or not isinstance(batch["completedOn"], str)
            or DATE.fullmatch(batch["completedOn"]) is None
            or batch["validationResult"] != "PASS"
        ):
            _fail("MIGRATION-SEQUENCE")
        rollback = batch["rollbackParentCommit"]
        if not isinstance(rollback, str) or FULL_OID.fullmatch(rollback) is None:
            _fail("MIGRATION-ROLLBACK")
        if rollback != ROLLBACK_PARENTS[offset - 1]:
            _fail("MIGRATION-ROLLBACK")

        program = _exact_keys(batch["program"], PROGRAM_KEYS, "MIGRATION-SCHEMA")
        record_rows = _exact_list(batch["records"], "MIGRATION-PAIR")
        if len(record_rows) != 2:
            _fail("MIGRATION-PAIR")
        kinds: list[str] = []
        upstream_spec: str | None = None
        for raw_record in record_rows:
            record = _exact_keys(raw_record, RECORD_KEYS, "MIGRATION-SCHEMA")
            kind = record["kind"]
            if kind not in {"plan", "task"}:
                _fail("MIGRATION-PAIR")
            kinds.append(str(kind))
            original_path = validate_path(record["originalPath"])
            archive_path = validate_path(record["archivePath"])
            if original_path in original_owners:
                _fail("MIGRATION-DUPLICATE-ORIGINAL")
            original_owners.add(original_path)
            eligible = eligible_rows.get(original_path)
            if (
                eligible is None
                or eligible.get("pairKey") != pair_key
                or eligible.get("kind") != kind
                or record["originalType"] != kind
                or record["sourceCommit"] != eligible.get("sourceCommit")
                or record["sourceBlob"] != eligible.get("sourceBlob")
                or archive_path != (eligible.get("archive") or {}).get("destination")
                or record["archiveReason"] != "completed-lineage"
                or record["replacement"] is not None
                or record["validationResult"] != "PASS"
                or type(record["payloadBytes"]) is not int
                or record["payloadBytes"] < 0
                or not isinstance(record["payloadSha256"], str)
                or re.fullmatch(r"[0-9a-f]{64}", record["payloadSha256"]) is None
                or type(record["historicalLinks"]) is not int
                or record["historicalLinks"] < 0
            ):
                _fail("MIGRATION-RECORD")
            upstream = eligible.get("upstream")
            if not isinstance(upstream, Mapping):
                _fail("MIGRATION-ELIGIBILITY-INPUT")
            spec = upstream.get("spec")
            if not isinstance(spec, str):
                _fail("MIGRATION-ELIGIBILITY-INPUT")
            expected_spec = _spec_path(pair_key, spec)
            upstream_spec = upstream_spec or expected_spec
            if (
                upstream_spec != expected_spec
                or program
                != {
                    "prd": upstream.get("prd"),
                    "ard": upstream.get("ard"),
                    "lineage": upstream.get("state"),
                }
            ):
                _fail("MIGRATION-PROGRAM")
            record_total += 1
            historical_total += record["historicalLinks"]
        if kinds != ["plan", "task"]:
            _fail("MIGRATION-PAIR")
        if (
            batch["upstreamSpec"] != upstream_spec
            or batch["currentClosureOwner"] != upstream_spec
            or batch["archiveNavigationBoundary"] != ARCHIVE_INDEX_ANCHOR
        ):
            _fail("MIGRATION-CLOSURE-OWNER")
        repaired = _exact_list(batch["repairedConsumers"], "MIGRATION-CONSUMERS")
        canonical_repaired = tuple(validate_path(path) for path in repaired)
        if (
            not canonical_repaired
            or tuple(sorted(set(canonical_repaired))) != canonical_repaired
            or canonical_repaired != REPAIRED_CONSUMERS_BY_SEQUENCE[offset - 1]
        ):
            _fail("MIGRATION-CONSUMERS")
        repaired_total += len(canonical_repaired)

    prior_prefix_canonical = json.dumps(
        batches[:3], sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    if hashlib.sha256(prior_prefix_canonical).hexdigest() != THREE_BATCH_PREFIX_SHA256:
        _fail("MIGRATION-PRIOR-BATCH-DRIFT")

    expected_counts = {
        "batches": len(batches),
        "records": record_total,
        "archiveRecords": BASE_RECORDS + record_total,
        "historicalLinksAdded": historical_total,
        "historicalLinks": BASE_HISTORICAL_LINKS + historical_total,
    }
    if dict(counts) != expected_counts:
        _fail("MIGRATION-COUNTS")
    return {
        **expected_counts,
        "repairedConsumers": repaired_total,
    }


def _regular_file(root: Path, path: str) -> bool:
    try:
        return stat.S_ISREG((root / path).lstat().st_mode)
    except OSError:
        return False


def _record_rows(document: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    return tuple(
        record
        for batch in document["batches"]
        for record in batch["records"]
    )


def _validate_source_absence(
    root: Path,
    rows: Sequence[Mapping[str, Any]],
    *,
    is_regular=_regular_file,
) -> None:
    for row in rows:
        if is_regular(root, str(row["originalPath"])):
            _fail("MIGRATION-SOURCE-STILL-CURRENT", str(row["originalPath"]))


def _archive_path(target: str) -> str | None:
    if not target.startswith("./"):
        return None
    normalized = posixpath.normpath(posixpath.join("docs/98.archive", target))
    if not normalized.startswith("docs/98.archive/"):
        return None
    return normalized


def _replacement_path(label: str, target: str) -> str | None:
    if not target.startswith("../"):
        return None
    normalized = posixpath.normpath(posixpath.join("docs/98.archive", target))
    if normalized != label or not normalized.startswith("docs/"):
        return None
    return normalized


def _parse_index_row(line: str) -> dict[str, Any] | None:
    cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
    if len(cells) != len(INDEX_COLUMNS):
        return None
    archive_match = MARKDOWN_LINK.fullmatch(cells[0])
    values = tuple(CODE_CELL.fullmatch(cells[index]) for index in range(1, 6))
    reason_match = CODE_CELL.fullmatch(cells[8])
    if (
        archive_match is None
        or any(match is None for match in values)
        or reason_match is None
        or not cells[6].isdigit()
    ):
        return None
    archive_path = _archive_path(archive_match.group("target"))
    if (
        archive_path is None
        or archive_match.group("label")
        != archive_path.removeprefix("docs/98.archive/")
    ):
        return None
    reason = reason_match.group("value")
    replacement: str | None
    if cells[7] == "`null`":
        if reason != "completed-lineage":
            return None
        replacement = None
    else:
        replacement_match = MARKDOWN_LINK.fullmatch(cells[7])
        if replacement_match is None or reason not in {
            "superseded",
            "consolidated",
            "duplicate",
        }:
            return None
        replacement = _replacement_path(
            replacement_match.group("label"), replacement_match.group("target")
        )
        if replacement is None:
            return None
    code_values = tuple(match.group("value") for match in values if match is not None)
    return {
        "archivePath": archive_path,
        "originalPath": code_values[0],
        "originalType": code_values[1],
        "sourceCommit": code_values[2],
        "sourceBlob": code_values[3],
        "payloadSha256": code_values[4],
        "historicalLinks": int(cells[6]),
        "replacement": replacement,
        "archiveReason": reason,
    }


def _parse_archive_index(text: str) -> tuple[dict[str, Mapping[str, Any]], int, int]:
    lines = text.splitlines()
    headers = [offset for offset, line in enumerate(lines) if line == INDEX_HEADER]
    if len(headers) != 1:
        _fail("MIGRATION-INDEX-STRUCTURE", ARCHIVE_INDEX_PATH)
    header = headers[0]
    if header + 1 >= len(lines) or lines[header + 1] != INDEX_SEPARATOR:
        _fail("MIGRATION-INDEX-STRUCTURE", ARCHIVE_INDEX_PATH)
    raw_rows: list[str] = []
    for line in lines[header + 2 :]:
        if not line.startswith("|"):
            break
        raw_rows.append(line)
    end = header + 2 + len(raw_rows)
    if any(line.startswith("|") for line in lines[end:]):
        _fail("MIGRATION-INDEX-STRUCTURE", ARCHIVE_INDEX_PATH)
    rows: dict[str, Mapping[str, Any]] = {}
    for raw in raw_rows:
        row = _parse_index_row(raw)
        if row is None or row["archivePath"] in rows:
            _fail("MIGRATION-INDEX-STRUCTURE", ARCHIVE_INDEX_PATH)
        rows[str(row["archivePath"])] = row
    marker_matches = tuple(MARKER.finditer(text))
    if len(marker_matches) != 1:
        _fail("MIGRATION-INDEX-MARKER", ARCHIVE_INDEX_PATH)
    record_count = len(rows)
    link_count = sum(int(row["historicalLinks"]) for row in rows.values())
    if (
        int(marker_matches[0].group("records")) != record_count
        or int(marker_matches[0].group("links")) != link_count
    ):
        _fail("MIGRATION-INDEX-MARKER", ARCHIVE_INDEX_PATH)
    return rows, record_count, link_count


def _validate_index(
    text: str,
    document: Mapping[str, Any],
) -> tuple[int, int]:
    rows, records, links = _parse_archive_index(text)
    migration_rows = _record_rows(document)
    expected_paths = set(EXPECTED_ARCHIVE_PATHS) | {
        str(row["archivePath"]) for row in migration_rows
    }
    if set(rows) != expected_paths:
        _fail("MIGRATION-INDEX-SET", ARCHIVE_INDEX_PATH)
    for record in migration_rows:
        expected = {
            key: record[key]
            for key in (
                "archivePath",
                "originalPath",
                "originalType",
                "sourceCommit",
                "sourceBlob",
                "payloadSha256",
                "historicalLinks",
                "replacement",
                "archiveReason",
            )
        }
        if rows.get(str(record["archivePath"])) != expected:
            _fail("MIGRATION-INDEX-MEMBER", str(record["archivePath"]))
    counts = document["counts"]
    if records != counts["archiveRecords"] or links != counts["historicalLinks"]:
        _fail("MIGRATION-INDEX-COUNTS", ARCHIVE_INDEX_PATH)
    return records, links


def _git_paths(root: Path) -> tuple[str, ...]:
    completed = _git(
        root,
        "ls-files",
        "-z",
        "--cached",
        "--others",
        "--exclude-standard",
        "--",
        "docs",
    )
    if completed.returncode != 0 or not completed.stdout.endswith(b"\0"):
        _fail("MIGRATION-GIT-INVENTORY", "docs")
    try:
        paths = tuple(
            sorted(
                item.decode("utf-8")
                for item in completed.stdout.split(b"\0")[:-1]
                if item
            )
        )
    except UnicodeDecodeError:
        _fail("MIGRATION-GIT-INVENTORY", "docs")
    for path in paths:
        validate_path(path)
    return paths


def _validate_archive_inventory(
    paths: Sequence[str], individual_paths: frozenset[str]
) -> None:
    actual = frozenset(
        path
        for path in paths
        if path.startswith("docs/98.archive/")
        and path.endswith(".md")
        and path != ARCHIVE_INDEX_PATH
    )
    if actual != individual_paths:
        _fail("MIGRATION-ROGUE-ARCHIVE", ARCHIVE_INDEX_PATH)


def _current_documents(
    root: Path,
    individual_paths: frozenset[str],
) -> tuple[CurrentMarkdownDocument, ...]:
    documents: list[CurrentMarkdownDocument] = []
    for path in _git_paths(root):
        if (
            not path.endswith(".md")
            or path == ARCHIVE_INDEX_PATH
            or path in individual_paths
            or path.startswith("docs/99.templates/templates/")
            or not _regular_file(root, path)
        ):
            continue
        try:
            if (root / path).stat().st_size > MAX_MARKDOWN_BYTES:
                _fail("MIGRATION-CURRENT-READ", path)
            markdown = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            _fail("MIGRATION-CURRENT-READ", path)
        documents.append(
            CurrentMarkdownDocument(
                path=path,
                markdown=markdown,
                profile="content/reference",
                status="active",
            )
        )
    return tuple(documents)


def _secret_clean(root: Path, archive_path: str, payload: bytes) -> None:
    executable = shutil.which("gitleaks")
    if executable is None:
        _fail("MIGRATION-SECRET-CLASSIFIER", archive_path)
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
                "10",
                "--exit-code",
                "17",
            ],
            input=payload,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=20,
            env=safe_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        _fail("MIGRATION-SECRET-CLASSIFIER", archive_path)
    if completed.returncode != 0:
        _fail(
            "MIGRATION-SECRET-DETECTED"
            if completed.returncode == 17
            else "MIGRATION-SECRET-CLASSIFIER",
            archive_path,
        )


def _verify_immutable_input(root: Path, commit: str, path: str) -> None:
    completed = _git(root, "cat-file", "blob", f"{commit}:{path}")
    try:
        current = (root / path).read_bytes()
    except OSError:
        _fail("MIGRATION-IMMUTABLE-INPUT", path)
    if completed.returncode != 0 or completed.stdout != current:
        _fail("MIGRATION-IMMUTABLE-INPUT", path)


def _validate_archive_payload(
    root: Path,
    row: Mapping[str, Any],
    content: bytes,
) -> ArchiveRecord:
    archive_path = str(row["archivePath"])
    try:
        parsed = parse_archive_envelope(content)
    except ArchiveContractError:
        _fail("MIGRATION-ARCHIVE-PAYLOAD", archive_path)
    metadata = parsed.metadata
    expected = {
        "original_type": row["originalType"],
        "original_path": row["originalPath"],
        "archive_reason": row["archiveReason"],
        "replacement": row["replacement"],
        "source_commit": row["sourceCommit"],
        "source_blob": row["sourceBlob"],
        "content_sha256": row["payloadSha256"],
    }
    if any(metadata.get(key) != value for key, value in expected.items()):
        _fail("MIGRATION-ARCHIVE-METADATA", archive_path)
    if len(parsed.payload) != row["payloadBytes"]:
        _fail("MIGRATION-ARCHIVE-PAYLOAD", archive_path)
    return ArchiveRecord(path=archive_path, content=content)


def validate_active_corpus_migrations(repository_root: str | Path) -> dict[str, int]:
    root = _require_root(repository_root)
    eligibility, document = load_documents(root)
    counts = validate_ledger_document(document, eligibility)
    _verify_immutable_input(root, ELIGIBILITY_CONTENT_COMMIT, CENSUS_PATH)
    _verify_immutable_input(root, ELIGIBILITY_CONTENT_COMMIT, ELIGIBILITY_PATH)
    rows = _record_rows(document)
    _validate_source_absence(root, rows)

    records: list[ArchiveRecord] = []
    secret_clean = 0
    for row in rows:
        archive_path = str(row["archivePath"])
        if not _regular_file(root, archive_path):
            _fail("MIGRATION-ARCHIVE-MISSING", archive_path)
        try:
            content = (root / archive_path).read_bytes()
        except OSError:
            _fail("MIGRATION-ARCHIVE-MISSING", archive_path)
        record = _validate_archive_payload(root, row, content)
        _secret_clean(root, archive_path, parse_archive_envelope(content).payload)
        secret_clean += 1
        records.append(record)

    with _closed_git_environment():
        archive_report = validate_archive_records(root, tuple(records))
    if not archive_report.valid:
        first = archive_report.diagnostics[0]
        _fail(first.code, first.path)
    if archive_report.historical_link_count != counts["historicalLinksAdded"]:
        _fail("MIGRATION-HISTORICAL-LINKS", ARCHIVE_INDEX_PATH)

    base_originals: set[str] = set()
    for archive_path in EXPECTED_ARCHIVE_PATHS:
        try:
            parsed = parse_archive_envelope((root / archive_path).read_bytes())
        except (OSError, ArchiveContractError):
            _fail("MIGRATION-BASE", archive_path)
        original = parsed.metadata.get("original_path")
        if not isinstance(original, str) or original in base_originals:
            _fail("MIGRATION-DUPLICATE-ORIGINAL", archive_path)
        base_originals.add(original)
    for row in rows:
        if row["originalPath"] in base_originals:
            _fail("MIGRATION-DUPLICATE-ORIGINAL", str(row["archivePath"]))

    try:
        index_text = (root / ARCHIVE_INDEX_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        _fail("MIGRATION-INDEX-READ", ARCHIVE_INDEX_PATH)
    archive_records, historical_links = _validate_index(index_text, document)

    individual_paths = frozenset(EXPECTED_ARCHIVE_PATHS) | frozenset(
        str(row["archivePath"]) for row in rows
    )
    current_paths = set(_git_paths(root))
    _validate_archive_inventory(tuple(current_paths), individual_paths)
    with _closed_git_environment():
        current_report = validate_current_archive_authority(
            _current_documents(root, individual_paths),
            individual_archive_paths=individual_paths,
        )
    if not current_report.valid:
        first = current_report.diagnostics[0]
        _fail(first.code, first.path)

    repaired = {
        path
        for batch in document["batches"]
        for path in batch["repairedConsumers"]
    }
    if not repaired <= current_paths:
        _fail("MIGRATION-CONSUMERS")

    return {
        "batches": counts["batches"],
        "records": counts["records"],
        "baseRecords": BASE_RECORDS,
        "archiveRecords": archive_records,
        "baseHistoricalLinks": BASE_HISTORICAL_LINKS,
        "addedHistoricalLinks": counts["historicalLinksAdded"],
        "historicalLinks": historical_links,
        "secretClean": secret_clean,
        "repairedConsumers": len(repaired),
    }


def self_test_case_names(repository_root: str | Path) -> set[str]:
    """Execute the closed mutation matrix through production helpers."""

    root = _require_root(repository_root)
    eligibility, document = load_documents(root)
    executed: set[str] = set()

    def ledger_case(name: str, mutate, expected: str) -> None:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        try:
            validate_ledger_document(candidate, eligibility)
        except MigrationError as error:
            if error.code != expected:
                _fail("MIGRATION-SELF-TEST")
        else:
            _fail("MIGRATION-SELF-TEST")
        executed.add(name)

    ledger_case(
        "partial-second-pair",
        lambda value: value["batches"][1]["records"].pop(),
        "MIGRATION-PAIR",
    )
    ledger_case(
        "partial-fourth-pair",
        lambda value: value["batches"][3]["records"].pop(),
        "MIGRATION-PAIR",
    )
    ledger_case(
        "skipped-first-eligible-batch",
        lambda value: value["batches"][0].__setitem__(
            "pairKey", "2026-07-12-protected-surface-supply-chain-hardening"  # gitleaks:allow
        ),
        "MIGRATION-ELIGIBLE-PREFIX",
    )
    ledger_case(
        "skipped-second-eligible-batch",
        lambda value: value["batches"][1].__setitem__(
            "pairKey", "2026-07-14-template-lifecycle-contract-normalization"
        ),
        "MIGRATION-ELIGIBLE-PREFIX",
    )
    ledger_case(
        "skipped-third-eligible-batch",
        lambda value: value["batches"][2].__setitem__(
            "pairKey", "2026-07-15-authority-and-lineage-foundation"
        ),
        "MIGRATION-ELIGIBLE-PREFIX",
    )
    ledger_case(
        "skipped-fourth-eligible-batch",
        lambda value: value["batches"][3].__setitem__(
            "pairKey", "2026-07-16-document-schema-and-lifecycle-contract"
        ),
        "MIGRATION-ELIGIBLE-PREFIX",
    )
    ledger_case(
        "reordered-eligible-batches",
        lambda value: value["batches"].reverse(),
        "MIGRATION-ELIGIBLE-PREFIX",
    )
    ledger_case(
        "prior-batch-evidence-drift",
        lambda value: value["batches"][0].__setitem__(
            "completedOn", "2026-07-17"
        ),
        "MIGRATION-PRIOR-BATCH-DRIFT",
    )
    ledger_case(
        "prior-second-batch-drift",
        lambda value: value["batches"][1].__setitem__(
            "completedOn", "2026-07-17"
        ),
        "MIGRATION-PRIOR-BATCH-DRIFT",
    )
    ledger_case(
        "prior-third-batch-drift",
        lambda value: value["batches"][2].__setitem__(
            "completedOn", "2026-07-17"
        ),
        "MIGRATION-PRIOR-BATCH-DRIFT",
    )
    ledger_case(
        "wrong-first-rollback-parent",
        lambda value: value["batches"][0].__setitem__(
            "rollbackParentCommit", "0" * 40
        ),
        "MIGRATION-ROLLBACK",
    )
    ledger_case(
        "wrong-second-rollback-parent",
        lambda value: value["batches"][1].__setitem__(
            "rollbackParentCommit", "0" * 40
        ),
        "MIGRATION-ROLLBACK",
    )
    ledger_case(
        "wrong-third-rollback-parent",
        lambda value: value["batches"][2].__setitem__(
            "rollbackParentCommit", "0" * 40
        ),
        "MIGRATION-ROLLBACK",
    )
    ledger_case(
        "wrong-fourth-rollback-parent",
        lambda value: value["batches"][3].__setitem__(
            "rollbackParentCommit", "0" * 40
        ),
        "MIGRATION-ROLLBACK",
    )
    ledger_case(
        "duplicate-original-owner",
        lambda value: value["batches"][3]["records"][1].__setitem__(
            "originalPath", value["batches"][3]["records"][0]["originalPath"]
        ),
        "MIGRATION-DUPLICATE-ORIGINAL",
    )
    ledger_case(
        "self-referential-batch-commit",
        lambda value: value["batches"][3].__setitem__("batchCommit", "0" * 40),
        "MIGRATION-SCHEMA",
    )

    try:
        validate_path("../forged\nPASS")
    except MigrationError as error:
        if error.code != "MIGRATION-PATH":
            _fail("MIGRATION-SELF-TEST")
    else:
        _fail("MIGRATION-SELF-TEST")
    executed.add("unsafe-path")

    rows = _record_rows(document)
    try:
        _validate_source_absence(
            root,
            rows,
            is_regular=lambda _root, path: path == rows[-1]["originalPath"],
        )
    except MigrationError as error:
        if error.code != "MIGRATION-SOURCE-STILL-CURRENT":
            _fail("MIGRATION-SELF-TEST")
    else:
        _fail("MIGRATION-SELF-TEST")
    executed.add("source-still-current")

    drift_row = rows[6]
    original_content = (root / str(drift_row["archivePath"])).read_bytes()
    drifted = original_content[:-1] + bytes([original_content[-1] ^ 1])
    try:
        _validate_archive_payload(root, drift_row, drifted)
    except MigrationError as error:
        if error.code != "MIGRATION-ARCHIVE-PAYLOAD":
            _fail("MIGRATION-SELF-TEST")
    else:
        _fail("MIGRATION-SELF-TEST")
    executed.add("archive-payload-byte-drift")

    index_text = (root / ARCHIVE_INDEX_PATH).read_text(encoding="utf-8")
    first_row = rows[0]
    additive_line = next(
        line
        for line in index_text.splitlines(keepends=True)
        if str(first_row["archivePath"]).removeprefix("docs/98.archive/") in line
        and line.startswith("| [`")
    )
    for name, candidate in (
        ("missing-index-row", index_text.replace(additive_line, "", 1)),
        (
            "duplicate-index-row",
            index_text.replace(additive_line, additive_line + additive_line, 1),
        ),
    ):
        try:
            _validate_index(candidate, document)
        except MigrationError as error:
            if error.code not in {
                "MIGRATION-INDEX-STRUCTURE",
                "MIGRATION-INDEX-SET",
                "MIGRATION-INDEX-MARKER",
            }:
                _fail("MIGRATION-SELF-TEST")
        else:
            _fail("MIGRATION-SELF-TEST")
        executed.add(name)

    individual_paths = frozenset(EXPECTED_ARCHIVE_PATHS) | frozenset(
        str(row["archivePath"]) for row in rows
    )
    try:
        _validate_archive_inventory(
            (*individual_paths, "docs/98.archive/04.execution/plans/rogue-extra.md"),
            individual_paths,
        )
    except MigrationError as error:
        if error.code != "MIGRATION-ROGUE-ARCHIVE":
            _fail("MIGRATION-SELF-TEST")
    else:
        _fail("MIGRATION-SELF-TEST")
    executed.add("rogue-extra-archive")

    direct = CurrentMarkdownDocument(
        path="docs/current.md",
        markdown=(
            "[history](98.archive/04.execution/plans/"
            "2026-07-15-authority-and-lineage-foundation.md)\n"
        ),
        profile="content/reference",
        status="active",
    )
    with _closed_git_environment():
        direct_report = validate_current_archive_authority(
            (direct,),
            individual_archive_paths=frozenset(
                str(row["archivePath"]) for row in rows
            ),
        )
    if "ARCHIVE-DIRECT-CURRENT-LINK" not in {
        diagnostic.code for diagnostic in direct_report.diagnostics
    }:
        _fail("MIGRATION-SELF-TEST")
    executed.add("direct-current-link")

    hostile = {
        "GIT_CONFIG_GLOBAL": "sentinel",
        "GIT_OBJECT_DIRECTORY": "sentinel",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES": "sentinel",
        "GIT_TERMINAL_PROMPT": "1",
    }
    original_environment = dict(os.environ)
    try:
        os.environ.update(hostile)
        environment = safe_git_environment()
    finally:
        os.environ.clear()
        os.environ.update(original_environment)
    if (
        "GIT_OBJECT_DIRECTORY" in environment
        or "GIT_ALTERNATE_OBJECT_DIRECTORIES" in environment
        or environment.get("GIT_CONFIG_GLOBAL") != os.devnull
        or environment.get("GIT_TERMINAL_PROMPT") != "0"
        or environment.get("PATH") != "/usr/bin:/bin"
    ):
        _fail("MIGRATION-SELF-TEST")
    executed.add("hostile-git-steering")

    if executed != REQUIRED_SELF_TEST_CASES:
        _fail("MIGRATION-SELF-TEST")
    return executed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.self_test:
            cases = self_test_case_names(args.root)
            print(f"PASS active corpus migration self-test cases={len(cases)}")
        else:
            counts = validate_active_corpus_migrations(args.root)
            print(
                "PASS active corpus migrations "
                f"batches={counts['batches']} records={counts['records']} "
                f"archive_records={counts['archiveRecords']} "
                f"historical_links={counts['historicalLinks']} "
                f"secret_clean={counts['secretClean']} "
                f"repaired_consumers={counts['repairedConsumers']}"
            )
    except MigrationError as error:
        print(f"FAIL {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
