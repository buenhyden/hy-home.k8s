"""Recovery-grade Git-object and canonical ArchiveEnvelope.v1 contracts.

The command-line boundary verifies a repository record without writing or
recovers exact bytes only to a new path under the operating-system temporary
directory. It never restores directly into a repository route.
"""

from __future__ import annotations

import datetime as dt
import argparse
import contextlib
import hashlib
import json
import os
import re
import select
import subprocess
import stat
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Mapping

import yaml


ARCHIVE_ENVELOPE_MARKER = (
    b"<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->"
)
GIT_TIMEOUT_SECONDS = 10.0
MAX_GIT_BLOB_BYTES = 8_000_000
MAX_GIT_BATCH_BYTES = 32 * 1024 * 1024
MAX_GIT_BATCH_OBJECTS = 128
MAX_GIT_HEADER_BYTES = 256
MAX_GIT_CAPTURE_BYTES = 2 * 1024 * 1024
ARCHIVE_METADATA_KEYS = (
    "title",
    "type",
    "status",
    "owner",
    "updated",
    "original_type",
    "original_path",
    "archived_on",
    "archive_reason",
    "replacement",
    "source_commit",
    "source_blob",
    "content_sha256",
)
ARCHIVE_OPTIONAL_STABLE_KEYS = (
    "artifact_id",
    "change_id",
    "original_artifact_id",
)
ARCHIVE_STABLE_METADATA_KEYS = (
    "title",
    "type",
    "status",
    "owner",
    "updated",
    *ARCHIVE_OPTIONAL_STABLE_KEYS,
    "original_type",
    "original_path",
    "archived_on",
    "archive_reason",
    "replacement",
    "source_commit",
    "source_blob",
    "content_sha256",
)
WORK107_LEGACY_ARCHIVE_COMMIT = (
    "eaf4f21ca84b68d98e20cd0b41db8b8d08ba6d0c"  # pragma: allowlist secret
)
WORK107_REGISTRY_PATH = "docs/99.templates/support/document-profiles.json"
WORK107_MIGRATION_PATH = (
    "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md"
)
WORK107_MIGRATION_DOCUMENT_SHA256 = (
    "4e62cb6ba2a394cd9ae546543c85a58c8f105cb5d1ff48cfd8dab8b8b1082206"  # pragma: allowlist secret
)
WORK107_LEGACY_INDEX_OVERVIEW = (
    "`98.archive/`는 원래 경로를 mirror한 43개의 immutable `content/archive` "
    "record를 보관한다. ARWB-003의 유한 base proof는 정확히 31 record와 202 "
    "historical link로 고정되고, ACER-003의 closed migration-result ledger가 현재 "
    "12 record와 160 historical link를 가산한다. 각 record는 canonical "
    "ArchiveEnvelope.v1 metadata 뒤에 source Git blob bytes를 EOF까지 그대로 "
    "포함한다. Archive record는 historical evidence이며 현재 요구사항·설계·실행·운영 "
    "권한이 아니다. 현재 문서는 개별 record가 아니라 이 index만 참조한다."
)
WORK107_STABLE_INDEX_OVERVIEW = (
    "`98.archive/`는 stable `changes/chg-####-<slug>/{plan.md,task.md}`와 typed "
    "`tombstones/<stage>/` 아래 93개의 `content/archive` record를 보관한다. "
    "[`migrations/mig-0001-sdlc-taxonomy-convergence.md`](./migrations/mig-0001-sdlc-taxonomy-convergence.md)는 "
    "legacy path와 stable path를 잇는 exact 14-field, 93-to-93 `moved` ledger다. 현재 "
    "census는 41 change directory(35 pair, 2 plan-only, 4 task-only)의 76 record와 "
    "17 tombstone(3/8/4/2)이다. 각 record의 ArchiveEnvelope payload와 source "
    "provenance는 보존되며, 현재 문서는 개별 record가 아니라 이 index만 참조한다."
)
WORK107_MIGRATION_ID = "MIG-0001"
WORK107_LEDGER_FIELDS = (
    "schema_version",
    "migration_id",
    "legacy_path",
    "stable_path",
    "artifact_id",
    "action",
    "replacement",
    "source_commit",
    "legacy_archive_commit",
    "legacy_envelope_blob",
    "source_blob",
    "content_sha256",
    "record_kind",
    "reason",
)
WORK107_LEDGER_MARKER = "<!-- archive-migration-ledger:v1 format=json -->"
WORK107_MIGRATION_METADATA_KEYS = (
    "title",
    "type",
    "status",
    "owner",
    "updated",
    "artifact_id",
    "migration_id",
)
_WORK107_EXECUTION_PATH = re.compile(
    r"docs/98\.archive/04\.execution/(?P<collection>plans|tasks)/"
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md\Z"
)
_WORK107_HISTORICAL_AD_TYPE = "ar" + "d"
_WORK107_TOMBSTONE_TYPES = {
    "prd": "PRD",
    _WORK107_HISTORICAL_AD_TYPE: "AD",
    "adr": "ADR",
    "spec": "SPEC",
    "guide": "GUIDE",
    "runbook": "RUNBOOK",
}
ARCHIVE_REASONS = frozenset(
    {
        "superseded",
        "consolidated",
        "completed-lineage",
        "retired",
        "abandoned",
        "duplicate",
    }
)
REPLACEMENT_REQUIRED_REASONS = frozenset({"superseded", "consolidated", "duplicate"})
_FULL_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
_INLINE_MARKDOWN_LINK = re.compile(rb"(?<!!)\[[^\]\r\n]+\]\([^\r\n)]*\)")


class ArchiveContractError(ValueError):
    """Fail-closed, payload-free diagnostic for recovery fixture contracts."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


class _DuplicateFrontmatterKey(ValueError):
    """Internal signal converted to a stable payload-free public diagnostic."""


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """Private YAML loader that rejects duplicate keys at every mapping level."""


def _construct_unique_mapping(
    loader: _UniqueKeySafeLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise _DuplicateFrontmatterKey
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


@dataclass(frozen=True)
class RecoveryResult:
    """One exact Git-object recovery result and its in-memory source bytes."""

    original_path: str
    source_commit: str
    source_blob: str
    byte_count: int
    content_sha256: str
    inline_link_candidate_count: int
    proposed_archive_path: str
    source_bytes: bytes = field(repr=False)


@dataclass(frozen=True)
class ArchiveReplacementReference:
    """Canonical archive-time replacement requiring caller-owned authority proof."""

    path: str


@dataclass(frozen=True)
class ParsedArchiveEnvelope:
    """Parsed ArchiveEnvelope.v1 metadata and byte-preserved payload."""

    metadata: dict[str, object]
    payload: bytes = field(repr=False)
    replacement_reference: ArchiveReplacementReference | None


@dataclass(frozen=True)
class _OutputTarget:
    """One output basename anchored to a held non-symlink parent directory."""

    parent_fd: int
    name: str


@dataclass(frozen=True)
class _DeadlineReader:
    """Pipe reader that applies one monotonic deadline to every bounded read."""

    stream: BinaryIO = field(repr=False)
    deadline: float

    def read(self, size: int = -1) -> bytes:
        if size == 0:
            return b""
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise _error("RECOVERY-GIT-TIMEOUT", "Git output deadline expired")
        try:
            readable, _, _ = select.select((self.stream.fileno(),), (), (), remaining)
        except (OSError, ValueError) as exc:
            raise _error(
                "RECOVERY-GIT-STARTUP", "Git output stream is unavailable"
            ) from exc
        if not readable:
            raise _error("RECOVERY-GIT-TIMEOUT", "Git output deadline expired")
        try:
            return os.read(self.stream.fileno(), 65536 if size < 0 else size)
        except OSError as exc:
            raise _error(
                "RECOVERY-GIT-STARTUP", "Git output stream could not be read"
            ) from exc


def _error(code: str, detail: str) -> ArchiveContractError:
    return ArchiveContractError(code, detail)


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


def _git_argv(root: Path, args: tuple[str, ...]) -> list[str]:
    return [
        "git",
        "--no-replace-objects",
        "--literal-pathspecs",
        "-C",
        str(root),
        *args,
    ]


def _start_git(
    root: Path,
    args: tuple[str, ...],
    *,
    input_bytes: bytes | None = None,
) -> tuple[subprocess.Popen[bytes], _DeadlineReader, list[str]]:
    argv = _git_argv(root, args)
    input_stream: BinaryIO | int = subprocess.DEVNULL
    try:
        if input_bytes is not None:
            input_stream = tempfile.TemporaryFile(mode="w+b")
            input_stream.write(input_bytes)
            input_stream.seek(0)
        process = subprocess.Popen(
            argv,
            stdin=input_stream,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=_safe_git_environment(),
            bufsize=0,
        )
    except OSError as exc:
        raise _error(
            "RECOVERY-GIT-STARTUP",
            "Git object lookup could not start",
        ) from exc
    finally:
        if not isinstance(input_stream, int):
            input_stream.close()
    if process.stdout is None:
        process.kill()
        process.wait()
        raise _error("RECOVERY-GIT-STARTUP", "Git output pipe is unavailable")
    deadline = time.monotonic() + GIT_TIMEOUT_SECONDS
    return process, _DeadlineReader(process.stdout, deadline), argv


def _finish_git(process: subprocess.Popen[bytes], deadline: float) -> int:
    remaining = deadline - time.monotonic()
    try:
        return process.wait(timeout=max(0.0, remaining))
    except subprocess.TimeoutExpired as exc:
        process.kill()
        process.wait()
        raise _error(
            "RECOVERY-GIT-TIMEOUT",
            "Git object lookup exceeded its bounded timeout",
        ) from exc


def _abort_git(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.kill()
    try:
        process.wait(timeout=1)
    except (OSError, subprocess.TimeoutExpired):
        pass
    if process.stdout is not None:
        process.stdout.close()


def _read_stream_bounded(stream: Any, limit: int) -> bytes:
    """Read at most ``limit`` bytes and reject the first excess byte."""

    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise _error("RECOVERY-RESOURCE-LIMIT", "output budget is invalid")
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = stream.read(min(65536, limit + 1 - total))
        if not isinstance(chunk, bytes):
            raise _error("RECOVERY-OBJECT-MISSING", "Git output type is invalid")
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            raise _error("RECOVERY-RESOURCE-LIMIT", "Git output exceeds its budget")
    return b"".join(chunks)


def _git_capture_bounded(
    root: Path,
    *args: str,
    stdout_limit: int = MAX_GIT_CAPTURE_BYTES,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    process, reader, argv = _start_git(root, args, input_bytes=input_bytes)
    try:
        output = _read_stream_bounded(reader, stdout_limit)
        returncode = _finish_git(process, reader.deadline)
    except Exception:
        _abort_git(process)
        raise
    finally:
        if process.stdout is not None:
            process.stdout.close()
    return subprocess.CompletedProcess(argv, returncode, output, b"")


def _read_bounded_line(stream: Any) -> bytes:
    line = bytearray()
    while len(line) <= MAX_GIT_HEADER_BYTES:
        byte = stream.read(1)
        if not isinstance(byte, bytes):
            raise _error("RECOVERY-OBJECT-MISSING", "Git header type is invalid")
        if not byte:
            raise _error("RECOVERY-OBJECT-MISSING", "Git batch header is truncated")
        line.extend(byte)
        if byte == b"\n":
            return bytes(line)
    raise _error("RECOVERY-RESOURCE-LIMIT", "Git batch header exceeds its budget")


def _read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(min(65536, remaining))
        if not isinstance(chunk, bytes) or not chunk:
            raise _error("RECOVERY-OBJECT-MISSING", "Git batch body is truncated")
        if len(chunk) > remaining:
            raise _error("RECOVERY-OBJECT-MISSING", "Git batch body is malformed")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _read_git_blob_batch_protocol(
    stream: Any,
    object_ids: tuple[str, ...],
    *,
    object_id_length: int,
    per_blob_limit: int = MAX_GIT_BLOB_BYTES,
    aggregate_limit: int = MAX_GIT_BATCH_BYTES,
    object_limit: int = MAX_GIT_BATCH_OBJECTS,
) -> dict[str, bytes]:
    """Parse a streaming ``cat-file --batch`` response within fixed budgets."""

    if len(object_ids) > object_limit:
        raise _error("RECOVERY-RESOURCE-LIMIT", "Git object count exceeds its budget")
    blobs: dict[str, bytes] = {}
    aggregate = 0
    for expected in object_ids:
        if (
            not isinstance(expected, str)
            or len(expected) != object_id_length
            or _FULL_OBJECT_ID.fullmatch(expected) is None
        ):
            raise _error("RECOVERY-OBJECT-AMBIGUOUS", "Git object identity is invalid")
        header = _read_bounded_line(stream).removesuffix(b"\n").split(b" ")
        if len(header) != 3:
            raise _error("RECOVERY-OBJECT-MISSING", "Git batch header is malformed")
        try:
            returned = header[0].decode("ascii", errors="strict")
            kind = header[1].decode("ascii", errors="strict")
            size = int(header[2])
        except (UnicodeDecodeError, ValueError) as exc:
            raise _error("RECOVERY-OBJECT-MISSING", "Git batch header is malformed") from exc
        if returned != expected or kind != "blob" or size < 0:
            raise _error("RECOVERY-OBJECT-MISSING", "Git batch identity differs")
        if size > per_blob_limit or aggregate + size > aggregate_limit:
            raise _error("RECOVERY-RESOURCE-LIMIT", "Git blob bytes exceed their budget")
        payload = _read_exact(stream, size)
        if stream.read(1) != b"\n":
            raise _error("RECOVERY-OBJECT-MISSING", "Git batch separator is malformed")
        try:
            payload.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise _error("RECOVERY-NON-UTF8", "source blob is not UTF-8 Markdown") from exc
        blobs[expected] = payload
        aggregate += size
    if stream.read(1) != b"":
        raise _error("RECOVERY-OBJECT-MISSING", "Git batch contains trailing output")
    return blobs


def _read_git_blob_batch(
    root: Path,
    object_ids: tuple[str, ...],
    *,
    object_id_length: int,
    per_blob_limit: int = MAX_GIT_BLOB_BYTES,
    aggregate_limit: int = MAX_GIT_BATCH_BYTES,
    object_limit: int = MAX_GIT_BATCH_OBJECTS,
) -> dict[str, bytes]:
    if not object_ids:
        return {}
    input_bytes = ("\n".join(object_ids) + "\n").encode("ascii")
    process, reader, _argv = _start_git(
        root, ("cat-file", "--batch"), input_bytes=input_bytes
    )
    try:
        blobs = _read_git_blob_batch_protocol(
            reader,
            object_ids,
            object_id_length=object_id_length,
            per_blob_limit=per_blob_limit,
            aggregate_limit=aggregate_limit,
            object_limit=object_limit,
        )
        returncode = _finish_git(process, reader.deadline)
        if returncode:
            raise _error("RECOVERY-OBJECT-MISSING", "Git blob batch failed")
        return blobs
    except Exception:
        _abort_git(process)
        raise
    finally:
        if process.stdout is not None:
            process.stdout.close()


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return _git_capture_bounded(root, *args)


def _require_repository(root: Path) -> tuple[Path, int]:
    try:
        candidate = root.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise _error(
            "RECOVERY-ROOT-INVALID",
            "repository root is unavailable or noncanonical",
        ) from exc
    top_level = _git(candidate, "rev-parse", "--show-toplevel")
    if top_level.returncode != 0:
        raise _error("RECOVERY-REPOSITORY-INVALID", "root is not a Git worktree")
    try:
        reported_root = Path(top_level.stdout.decode("utf-8").strip()).resolve(
            strict=True
        )
    except (UnicodeDecodeError, OSError) as exc:
        raise _error(
            "RECOVERY-REPOSITORY-INVALID", "Git root is not canonical"
        ) from exc
    if reported_root != candidate:
        raise _error("RECOVERY-REPOSITORY-INVALID", "root must be the Git top level")

    object_format = _git(candidate, "rev-parse", "--show-object-format")
    if object_format.returncode != 0:
        raise _error("RECOVERY-REPOSITORY-INVALID", "object format is unavailable")
    try:
        format_output = object_format.stdout.decode("ascii", errors="strict")
    except UnicodeDecodeError as exc:
        raise _error(
            "RECOVERY-OBJECT-FORMAT",
            "Git object format output is malformed",
        ) from exc
    if format_output == "sha1\n":
        return candidate, 40
    if format_output == "sha256\n":
        return candidate, 64
    raise _error(
        "RECOVERY-OBJECT-FORMAT",
        "Git object format output is malformed or unsupported",
    )


def _require_repository_path(value: object, *, field: str) -> str:
    canonical = _require_git_tree_path(value, field=field)
    path = PurePosixPath(canonical)
    if not path.parts or path.parts[0] != "docs":
        raise _error("ARCHIVE-METADATA-PATH", f"{field} must remain under docs")
    return canonical


def _require_git_tree_path(value: object, *, field: str) -> str:
    """Require one literal repository-relative path without reading a worktree."""

    if not isinstance(value, str) or not value:
        raise _error("ARCHIVE-METADATA-PATH", f"{field} must be a repository path")
    if "\\" in value or any(
        ord(character) < 32 or ord(character) == 127 for character in value
    ):
        raise _error("ARCHIVE-METADATA-PATH", f"{field} is not canonical POSIX")
    path = PurePosixPath(value)
    if path.is_absolute() or "." in path.parts or ".." in path.parts:
        raise _error("ARCHIVE-METADATA-PATH", f"{field} is not repository-relative")
    if path.as_posix() != value:
        raise _error("ARCHIVE-METADATA-PATH", f"{field} is not canonical POSIX")
    return path.as_posix()


def git_tree_path_exists(
    repository_root: str | Path,
    source_commit: str,
    repository_path: str,
) -> bool:
    """Check one sanitized literal path in one full immutable commit tree."""

    root, object_id_length = _require_repository(Path(repository_root))
    canonical_path = _require_git_tree_path(repository_path, field="repository_path")
    if (
        not isinstance(source_commit, str)
        or len(source_commit) != object_id_length
        or _FULL_OBJECT_ID.fullmatch(source_commit) is None
    ):
        raise _error(
            "RECOVERY-OBJECT-AMBIGUOUS",
            "source_commit must be one full lowercase object ID",
        )
    commit_type = _git(root, "cat-file", "-t", source_commit)
    if commit_type.returncode != 0:
        raise _error("RECOVERY-OBJECT-MISSING", "source commit object is unavailable")
    if commit_type.stdout != b"commit\n":
        raise _error("RECOVERY-OBJECT-NOT-COMMIT", "source object is not a commit")

    tree = _git(
        root,
        "ls-tree",
        "-z",
        "--full-tree",
        source_commit,
        "--",
        canonical_path,
    )
    if tree.returncode != 0:
        raise _error("RECOVERY-TREE-INVALID", "source tree lookup failed")
    records = [record for record in tree.stdout.split(b"\0") if record]
    if not records:
        return False
    if len(records) != 1:
        raise _error("RECOVERY-PATH-AMBIGUOUS", "source path resolves more than once")
    try:
        header, raw_path = records[0].split(b"\t", 1)
        _mode, object_type, raw_object = header.split(b" ", 2)
        resolved_path = raw_path.decode("utf-8")
        object_id = raw_object.decode("ascii")
    except (ValueError, UnicodeDecodeError) as exc:
        raise _error(
            "RECOVERY-TREE-INVALID", "source tree record is malformed"
        ) from exc
    if resolved_path != canonical_path:
        raise _error("RECOVERY-PATH-AMBIGUOUS", "source tree returned a different path")
    if object_type not in {b"blob", b"tree"}:
        raise _error("RECOVERY-OBJECT-UNSUPPORTED", "source path is not a blob or tree")
    if (
        len(object_id) != object_id_length
        or _FULL_OBJECT_ID.fullmatch(object_id) is None
    ):
        raise _error("RECOVERY-TREE-INVALID", "source object ID is not full length")
    return True


def _proposed_archive_path(original_path: str) -> str:
    path = PurePosixPath(original_path)
    if len(path.parts) < 3 or path.parts[1] not in {
        "01.requirements",
        "02.architecture",
        "03.specs",
        "04.execution",
        "05.operations",
    }:
        raise _error(
            "RECOVERY-PATH-OUTSIDE-SDLC",
            "original path is outside the mirrored docs/01-05 stages",
        )
    return PurePosixPath("docs/98.archive", *path.parts[1:]).as_posix()


def _inline_link_candidate_count(payload: bytes) -> int:
    """Count bounded inline candidates; ARWB-002 owns authoritative resolution."""

    return len(_INLINE_MARKDOWN_LINK.findall(payload))


def recover_git_blob(
    repository_root: str | Path,
    original_path: str,
    source_commit: str,
) -> RecoveryResult:
    """Recover one UTF-8 Markdown source exactly from an unambiguous Git tree."""

    root, object_id_length = _require_repository(Path(repository_root))
    canonical_original = _require_repository_path(original_path, field="original_path")
    proposed_archive = _proposed_archive_path(canonical_original)

    if (
        not isinstance(source_commit, str)
        or len(source_commit) != object_id_length
        or _FULL_OBJECT_ID.fullmatch(source_commit) is None
    ):
        raise _error(
            "RECOVERY-OBJECT-AMBIGUOUS",
            "source_commit must be one full lowercase object ID",
        )

    commit_type = _git(root, "cat-file", "-t", source_commit)
    if commit_type.returncode != 0:
        raise _error("RECOVERY-OBJECT-MISSING", "source commit object is unavailable")
    if commit_type.stdout != b"commit\n":
        raise _error("RECOVERY-OBJECT-NOT-COMMIT", "source object is not a commit")

    tree = _git(
        root,
        "ls-tree",
        "-z",
        "--full-tree",
        source_commit,
        "--",
        canonical_original,
    )
    if tree.returncode != 0:
        raise _error("RECOVERY-TREE-INVALID", "source tree lookup failed")
    records = [record for record in tree.stdout.split(b"\0") if record]
    if not records:
        raise _error(
            "RECOVERY-PATH-MISSING", "original path is absent from source tree"
        )
    if len(records) != 1:
        raise _error("RECOVERY-PATH-AMBIGUOUS", "original path resolves more than once")

    try:
        header, raw_path = records[0].split(b"\t", 1)
        mode, object_type, raw_blob = header.split(b" ", 2)
        resolved_path = raw_path.decode("utf-8")
        source_blob = raw_blob.decode("ascii")
    except (ValueError, UnicodeDecodeError) as exc:
        raise _error(
            "RECOVERY-TREE-INVALID", "source tree record is malformed"
        ) from exc
    if resolved_path != canonical_original:
        raise _error("RECOVERY-PATH-AMBIGUOUS", "source tree returned a different path")
    if object_type != b"blob" or mode not in {b"100644", b"100755"}:
        raise _error("RECOVERY-OBJECT-NOT-BLOB", "original path is not a regular blob")
    if (
        len(source_blob) != object_id_length
        or _FULL_OBJECT_ID.fullmatch(source_blob) is None
    ):
        raise _error("RECOVERY-TREE-INVALID", "source blob ID is not full length")

    source_bytes = _read_git_blob_batch(
        root,
        (source_blob,),
        object_id_length=object_id_length,
        per_blob_limit=MAX_GIT_BLOB_BYTES,
        aggregate_limit=MAX_GIT_BLOB_BYTES,
        object_limit=1,
    )[source_blob]

    return RecoveryResult(
        original_path=canonical_original,
        source_commit=source_commit,
        source_blob=source_blob,
        byte_count=len(source_bytes),
        content_sha256=hashlib.sha256(source_bytes).hexdigest(),
        inline_link_candidate_count=_inline_link_candidate_count(source_bytes),
        proposed_archive_path=proposed_archive,
        source_bytes=source_bytes,
    )


def _require_string(metadata: Mapping[str, object], key: str) -> str:
    value = metadata[key]
    if not isinstance(value, str) or not value:
        raise _error("ARCHIVE-METADATA-TYPE", f"{key} must be a non-empty string")
    return value


def _require_date(metadata: Mapping[str, object], key: str) -> str:
    value = _require_string(metadata, key)
    if _DATE.fullmatch(value) is None:
        raise _error("ARCHIVE-METADATA-DATE", f"{key} must be YYYY-MM-DD")
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise _error("ARCHIVE-METADATA-DATE", f"{key} is not a calendar date") from exc
    return value


def validate_archive_metadata(
    metadata: Mapping[str, object],
) -> ArchiveReplacementReference | None:
    """Validate metadata and return typed archive-time replacement evidence."""

    if not isinstance(metadata, Mapping):
        raise _error("ARCHIVE-METADATA-TYPE", "metadata must be a mapping")
    keys = tuple(metadata)
    allowed_keys = tuple(
        key
        for key in ARCHIVE_STABLE_METADATA_KEYS
        if key not in ARCHIVE_OPTIONAL_STABLE_KEYS or key in metadata
    )
    if keys != allowed_keys:
        raise _error(
            "ARCHIVE-METADATA-KEYS", "metadata keys or order are not canonical"
        )

    _require_string(metadata, "title")
    if metadata["type"] != "content/archive":
        raise _error("ARCHIVE-METADATA-TYPE", "type must be content/archive")
    if metadata["status"] != "archived":
        raise _error("ARCHIVE-METADATA-STATUS", "status must be archived")
    _require_string(metadata, "owner")
    _require_date(metadata, "updated")
    artifact_id = metadata.get("artifact_id")
    if artifact_id is not None and (
        not isinstance(artifact_id, str)
        or re.fullmatch(r"[A-Z0-9]+(?:-[A-Z0-9]+)*", artifact_id) is None
    ):
        raise _error("ARCHIVE-METADATA-IDENTITY", "artifact_id is non-canonical")
    change_id = metadata.get("change_id")
    if change_id is not None and (
        not isinstance(change_id, str)
        or re.fullmatch(r"CHG-[0-9]{4}", change_id) is None
    ):
        raise _error("ARCHIVE-METADATA-IDENTITY", "change_id is non-canonical")
    original_artifact_id = metadata.get("original_artifact_id")
    if original_artifact_id is not None and (
        not isinstance(original_artifact_id, str)
        or re.fullmatch(r"[A-Z0-9]+(?:-[A-Z0-9]+)*", original_artifact_id) is None
    ):
        raise _error(
            "ARCHIVE-METADATA-IDENTITY",
            "original_artifact_id is non-canonical",
        )
    _require_string(metadata, "original_type")
    original_path = _require_repository_path(
        metadata["original_path"], field="original_path"
    )
    _proposed_archive_path(original_path)
    _require_date(metadata, "archived_on")

    reason = _require_string(metadata, "archive_reason")
    if reason not in ARCHIVE_REASONS:
        raise _error("ARCHIVE-METADATA-REASON", "archive_reason is unsupported")
    replacement = metadata["replacement"]
    replacement_reference: ArchiveReplacementReference | None = None
    if reason in REPLACEMENT_REQUIRED_REASONS:
        canonical_replacement = _require_repository_path(
            replacement, field="replacement"
        )
        if PurePosixPath(canonical_replacement).is_relative_to(
            PurePosixPath("docs/98.archive")
        ):
            raise _error(
                "ARCHIVE-METADATA-REPLACEMENT",
                "replacement must not name an archive record",
            )
        replacement_reference = ArchiveReplacementReference(canonical_replacement)
    elif replacement is not None:
        raise _error(
            "ARCHIVE-METADATA-REPLACEMENT",
            "replacement must be null for this archive_reason",
        )

    commit = _require_string(metadata, "source_commit")
    blob = _require_string(metadata, "source_blob")
    if (
        _FULL_OBJECT_ID.fullmatch(commit) is None
        or _FULL_OBJECT_ID.fullmatch(blob) is None
        or len(commit) != len(blob)
    ):
        raise _error(
            "ARCHIVE-METADATA-OBJECT",
            "source_commit and source_blob must be full same-format object IDs",
        )
    digest = _require_string(metadata, "content_sha256")
    if _SHA256.fullmatch(digest) is None:
        raise _error(
            "ARCHIVE-METADATA-DIGEST", "content_sha256 must be lowercase SHA-256"
        )
    return replacement_reference


def _metadata_bytes(metadata: Mapping[str, object]) -> bytes:
    lines = ["---\n"]
    for key in metadata:
        lines.append(
            f"{key}: {json.dumps(metadata[key], ensure_ascii=False, separators=(',', ':'))}\n"
        )
    lines.append("---\n")
    return "".join(lines).encode("utf-8")


def render_archive_envelope(
    metadata: Mapping[str, object],
    recovered: RecoveryResult,
    payload: bytes,
) -> bytes:
    """Render one canonical envelope only from the exact recovered Git blob."""

    validate_archive_metadata(metadata)
    if not isinstance(payload, bytes) or payload != recovered.source_bytes:
        raise _error(
            "ARCHIVE-PAYLOAD-NOT-SOURCE-BLOB",
            "payload must be the exact recovered Git blob bytes",
        )
    expected_fields = {
        "original_path": recovered.original_path,
        "source_commit": recovered.source_commit,
        "source_blob": recovered.source_blob,
        "content_sha256": recovered.content_sha256,
    }
    for key, expected_value in expected_fields.items():
        if metadata[key] != expected_value:
            raise _error("ARCHIVE-METADATA-PROVENANCE", f"{key} differs from recovery")
    if hashlib.sha256(payload).hexdigest() != recovered.content_sha256:
        raise _error("ARCHIVE-PAYLOAD-DIGEST", "payload digest differs from recovery")
    if len(payload) != recovered.byte_count:
        raise _error("ARCHIVE-PAYLOAD-SIZE", "payload byte count differs from recovery")
    return _metadata_bytes(metadata) + ARCHIVE_ENVELOPE_MARKER + b"\n" + payload


def render_fixture_archive_envelope(
    metadata: Mapping[str, object],
    recovered: RecoveryResult,
    payload: bytes,
) -> bytes:
    """Compatibility wrapper for existing fixture callers."""

    return render_archive_envelope(metadata, recovered, payload)


def parse_archive_envelope(
    archive_bytes: bytes,
    *,
    expected: RecoveryResult | None = None,
) -> ParsedArchiveEnvelope:
    """Parse the single exact marker and return every remaining byte as payload."""

    if not isinstance(archive_bytes, bytes) or not archive_bytes.startswith(
        (b"---\n", b"---\r\n")
    ):
        raise _error("ARCHIVE-FRONTMATTER-INVALID", "frontmatter opening is absent")
    lines = archive_bytes.splitlines(keepends=True)
    closing_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line in {b"---\n", b"---\r\n"}:
            closing_index = index
            break
    if closing_index is None:
        raise _error(
            "ARCHIVE-FRONTMATTER-INVALID", "frontmatter closing line is absent"
        )

    prefix_length = sum(len(line) for line in lines[: closing_index + 1])
    marker_line = ARCHIVE_ENVELOPE_MARKER + b"\n"
    if archive_bytes[prefix_length : prefix_length + len(marker_line)] != marker_line:
        raise _error(
            "ARCHIVE-MARKER-INVALID",
            "the v1 marker must immediately follow frontmatter",
        )
    frontmatter_bytes = archive_bytes[:prefix_length]
    payload = archive_bytes[prefix_length + len(marker_line) :]
    try:
        frontmatter_text = b"".join(lines[1:closing_index]).decode("utf-8")
        payload.decode("utf-8", errors="strict")
        loaded = yaml.load(frontmatter_text, Loader=_UniqueKeySafeLoader)
    except _DuplicateFrontmatterKey as exc:
        raise _error(
            "ARCHIVE-FRONTMATTER-DUPLICATE",
            "frontmatter contains a duplicate key",
        ) from exc
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise _error(
            "ARCHIVE-UTF8-INVALID", "envelope is not canonical UTF-8 YAML/Markdown"
        ) from exc
    if not isinstance(loaded, dict):
        raise _error("ARCHIVE-METADATA-TYPE", "frontmatter must be one mapping")
    metadata = dict(loaded)
    replacement_reference = validate_archive_metadata(metadata)
    if _metadata_bytes(metadata) != frontmatter_bytes:
        raise _error(
            "ARCHIVE-FRONTMATTER-NONCANONICAL",
            "frontmatter bytes differ from canonical UTF-8/LF serialization",
        )

    digest = hashlib.sha256(payload).hexdigest()
    if digest != metadata["content_sha256"]:
        raise _error("ARCHIVE-PAYLOAD-DIGEST", "payload digest differs from metadata")
    if expected is not None:
        expected_fields = {
            "original_path": expected.original_path,
            "source_commit": expected.source_commit,
            "source_blob": expected.source_blob,
            "content_sha256": expected.content_sha256,
        }
        for key, expected_value in expected_fields.items():
            if metadata[key] != expected_value:
                raise _error(
                    "ARCHIVE-METADATA-PROVENANCE", f"{key} differs from recovery"
                )
        if len(payload) != expected.byte_count:
            raise _error(
                "ARCHIVE-PAYLOAD-SIZE", "payload byte count differs from recovery"
            )
        if payload != expected.source_bytes:
            raise _error(
                "ARCHIVE-PAYLOAD-NOT-SOURCE-BLOB",
                "payload differs from recovered Git blob bytes",
            )

    return ParsedArchiveEnvelope(
        metadata=metadata,
        payload=payload,
        replacement_reference=replacement_reference,
    )


def _work107_commit_path_blobs(
    root: Path,
    commit: str,
    paths: tuple[str, ...],
) -> dict[str, tuple[str, bytes]]:
    """Read an exact bounded path set from one reviewed Git commit."""

    repository, object_id_length = _require_repository(root)
    if (
        len(commit) != object_id_length
        or _FULL_OBJECT_ID.fullmatch(commit) is None
        or not paths
        or len(paths) > MAX_GIT_BATCH_OBJECTS
    ):
        raise _error("ARCHIVE-MIGRATION-PROVENANCE", "reviewed commit input differs")
    canonical = tuple(_require_git_tree_path(path, field="legacy_path") for path in paths)
    if len(set(canonical)) != len(canonical):
        raise _error("ARCHIVE-MIGRATION-PROVENANCE", "legacy paths are not unique")
    tree = _git(
        repository,
        "ls-tree",
        "-z",
        "--full-tree",
        commit,
        "--",
        *canonical,
    )
    if tree.returncode != 0:
        raise _error("ARCHIVE-MIGRATION-PROVENANCE", "legacy tree lookup failed")
    object_ids: dict[str, str] = {}
    for raw in (record for record in tree.stdout.split(b"\0") if record):
        try:
            header, raw_path = raw.split(b"\t", 1)
            mode, kind, raw_object_id = header.split(b" ", 2)
            path = raw_path.decode("utf-8")
            object_id = raw_object_id.decode("ascii")
        except (UnicodeDecodeError, ValueError) as exc:
            raise _error(
                "ARCHIVE-MIGRATION-PROVENANCE", "legacy tree output is malformed"
            ) from exc
        if (
            path not in canonical
            or path in object_ids
            or mode not in {b"100644", b"100755"}
            or kind != b"blob"
            or len(object_id) != object_id_length
            or _FULL_OBJECT_ID.fullmatch(object_id) is None
        ):
            raise _error(
                "ARCHIVE-MIGRATION-PROVENANCE", "legacy tree member differs"
            )
        object_ids[path] = object_id
    if frozenset(object_ids) != frozenset(canonical):
        raise _error("ARCHIVE-MIGRATION-PROVENANCE", "legacy tree is incomplete")
    unique_ids = tuple(dict.fromkeys(object_ids[path] for path in canonical))
    blobs = _read_git_blob_batch(
        repository,
        unique_ids,
        object_id_length=object_id_length,
    )
    return {path: (object_ids[path], blobs[object_ids[path]]) for path in canonical}


def _work107_registry_archive_paths(root: Path) -> tuple[str, ...]:
    registry = _work107_commit_path_blobs(
        root,
        WORK107_LEGACY_ARCHIVE_COMMIT,
        (WORK107_REGISTRY_PATH,),
    )[WORK107_REGISTRY_PATH][1]
    try:
        loaded = json.loads(registry.decode("utf-8"))
        namespaces = loaded["archiveNamespaces"]
        paths = tuple(
            path
            for namespace in namespaces
            for path in namespace["records"]
        )
    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _error(
            "ARCHIVE-MIGRATION-PROVENANCE", "reviewed archive registry is malformed"
        ) from exc
    if (
        len(paths) != 93
        or len(set(paths)) != 93
        or any(
            not isinstance(path, str)
            or not path.startswith("docs/98.archive/")
            or path == WORK107_MIGRATION_PATH
            for path in paths
        )
    ):
        raise _error(
            "ARCHIVE-MIGRATION-PROVENANCE", "reviewed archive census differs"
        )
    return tuple(sorted(paths))


def _work107_tombstone_identity(
    legacy_path: str,
    original_type: str,
    source_blob: str,
) -> tuple[str, str]:
    parts = PurePosixPath(legacy_path).parts
    if len(parts) < 4:
        raise _error("ARCHIVE-MIGRATION-IDENTITY", "legacy tombstone path differs")
    stage = parts[2]
    terminal_type = _WORK107_TOMBSTONE_TYPES.get(original_type)
    allowed_stage = {
        "01.requirements": {"PRD", "SRS", "IFC"},
        "02.architecture": {"AD", "ADR"},
        "03.specs": {"SPEC", "AGENT-DESIGN", "DATA-MODEL", "TESTS", "PLAN", "TASK"},
        "05.operations": {"GUIDE", "POLICY", "RUNBOOK", "INCIDENT", "POSTMORTEM"},
    }
    if terminal_type is None or terminal_type not in allowed_stage.get(stage, set()):
        raise _error(
            "ARCHIVE-MIGRATION-IDENTITY", "legacy tombstone type is unsupported"
        )
    digest = hashlib.sha256(
        legacy_path.encode("utf-8") + b"\0" + source_blob.encode("ascii")
    ).hexdigest()
    stable_path = (
        f"docs/98.archive/tombstones/{stage}/"
        f"tmb-{terminal_type.lower()}-legacy-{digest}.md"
    )
    artifact_id = f"TMB-{terminal_type}-LEGACY-{digest.upper()}"
    return stable_path, artifact_id


def build_work107_migration_rows(
    repository_root: str | Path,
) -> tuple[dict[str, object], ...]:
    """Derive the exact reviewed 93-row stable rehome from the pinned legacy tree."""

    root, _object_id_length = _require_repository(Path(repository_root))
    legacy_paths = _work107_registry_archive_paths(root)
    records = _work107_commit_path_blobs(
        root, WORK107_LEGACY_ARCHIVE_COMMIT, legacy_paths
    )
    parsed: dict[str, ParsedArchiveEnvelope] = {}
    execution: dict[str, tuple[str, str]] = {}
    slugs: set[str] = set()
    for legacy_path in legacy_paths:
        envelope = parse_archive_envelope(records[legacy_path][1])
        parsed[legacy_path] = envelope
        match = _WORK107_EXECUTION_PATH.fullmatch(legacy_path)
        if match is not None:
            leaf = "plan" if match.group("collection") == "plans" else "task"
            slug = match.group("slug")
            execution[legacy_path] = (slug, leaf)
            slugs.add(slug)
    if len(execution) != 76 or len(slugs) != 41:
        raise _error("ARCHIVE-MIGRATION-CENSUS", "execution grouping differs")
    change_numbers = {slug: index for index, slug in enumerate(sorted(slugs), start=1)}

    rows: list[dict[str, object]] = []
    for legacy_path in legacy_paths:
        envelope = parsed[legacy_path]
        metadata = envelope.metadata
        source_commit = metadata.get("source_commit")
        source_blob = metadata.get("source_blob")
        content_sha256 = metadata.get("content_sha256")
        original_type = metadata.get("original_type")
        if not all(
            isinstance(value, str)
            for value in (source_commit, source_blob, content_sha256, original_type)
        ):
            raise _error("ARCHIVE-MIGRATION-PROVENANCE", "legacy metadata differs")
        if legacy_path in execution:
            slug, leaf = execution[legacy_path]
            number = change_numbers[slug]
            stable_path = (
                f"docs/98.archive/changes/chg-{number:04d}-{slug}/{leaf}.md"
            )
            prefix = "PLAN" if leaf == "plan" else "TASK"
            artifact_id = f"{prefix}-CHG-{number:04d}"
            record_kind = f"change-{leaf}"
        else:
            stable_path, artifact_id = _work107_tombstone_identity(
                legacy_path, str(original_type), str(source_blob)
            )
            record_kind = "tombstone"
        rows.append(
            {
                "schema_version": 1,
                "migration_id": WORK107_MIGRATION_ID,
                "legacy_path": legacy_path,
                "stable_path": stable_path,
                "artifact_id": artifact_id,
                "action": "moved",
                "replacement": None,
                "source_commit": source_commit,
                "legacy_archive_commit": WORK107_LEGACY_ARCHIVE_COMMIT,
                "legacy_envelope_blob": records[legacy_path][0],
                "source_blob": source_blob,
                "content_sha256": content_sha256,
                "record_kind": record_kind,
                "reason": "Reviewed stable Stage 98 rehome",
            }
        )
    return tuple(sorted(rows, key=lambda row: str(row["stable_path"])))


def _work107_validate_closed_census(rows: tuple[Mapping[str, object], ...]) -> None:
    if len(rows) != 93:
        raise _error("ARCHIVE-MIGRATION-CENSUS", "ledger row count differs")
    legacy_paths: set[object] = set()
    stable_paths: set[object] = set()
    artifact_ids: set[object] = set()
    change_leaves: dict[str, set[str]] = {}
    tombstones: dict[str, int] = {}
    for row in rows:
        if tuple(row) != WORK107_LEDGER_FIELDS:
            raise _error("ARCHIVE-MIGRATION-FIELDS", "ledger field set differs")
        if (
            row["schema_version"] != 1
            or row["migration_id"] != WORK107_MIGRATION_ID
            or row["action"] != "moved"
            or row["replacement"] is not None
            or row["reason"] != "Reviewed stable Stage 98 rehome"
        ):
            raise _error("ARCHIVE-MIGRATION-ROW", "ledger row contract differs")
        for key in (
            "legacy_path",
            "stable_path",
            "artifact_id",
            "source_commit",
            "legacy_archive_commit",
            "legacy_envelope_blob",
            "source_blob",
            "content_sha256",
            "record_kind",
        ):
            if not isinstance(row[key], str):
                raise _error("ARCHIVE-MIGRATION-ROW", "ledger value type differs")
        for key in (
            "source_commit",
            "legacy_archive_commit",
            "legacy_envelope_blob",
            "source_blob",
        ):
            if _FULL_OBJECT_ID.fullmatch(str(row[key])) is None:
                raise _error("ARCHIVE-MIGRATION-PROVENANCE", "Git object differs")
        if _SHA256.fullmatch(str(row["content_sha256"])) is None:
            raise _error("ARCHIVE-MIGRATION-PROVENANCE", "payload digest differs")
        legacy_paths.add(row["legacy_path"])
        stable_paths.add(row["stable_path"])
        artifact_ids.add(row["artifact_id"])
        stable = PurePosixPath(str(row["stable_path"]))
        kind = str(row["record_kind"])
        if kind in {"change-plan", "change-task"}:
            leaf = "plan.md" if kind == "change-plan" else "task.md"
            if stable.name != leaf:
                raise _error("ARCHIVE-MIGRATION-IDENTITY", "change leaf differs")
            change_leaves.setdefault(stable.parent.as_posix(), set()).add(leaf)
        elif kind == "tombstone" and len(stable.parts) == 5:
            stage = stable.parts[3]
            tombstones[stage] = tombstones.get(stage, 0) + 1
        else:
            raise _error("ARCHIVE-MIGRATION-IDENTITY", "record kind differs")
    if not all(len(values) == 93 for values in (legacy_paths, stable_paths, artifact_ids)):
        raise _error("ARCHIVE-MIGRATION-BIJECTION", "ledger identity is not unique")
    shapes = tuple(frozenset(leaves) for leaves in change_leaves.values())
    if (
        len(change_leaves) != 41
        or shapes.count(frozenset({"plan.md", "task.md"})) != 35
        or shapes.count(frozenset({"plan.md"})) != 2
        or shapes.count(frozenset({"task.md"})) != 4
    ):
        raise _error("ARCHIVE-MIGRATION-CENSUS", "change grouping differs")
    if tombstones != {
        "01.requirements": 3,
        "02.architecture": 8,
        "03.specs": 4,
        "05.operations": 2,
    }:
        raise _error("ARCHIVE-MIGRATION-CENSUS", "tombstone grouping differs")


def validate_work107_migration_rows(
    repository_root: str | Path,
    rows: list[Mapping[str, object]] | tuple[Mapping[str, object], ...],
) -> tuple[dict[str, object], ...]:
    """Require the supplied ledger to equal the reviewed Git-derived bijection."""

    if not isinstance(rows, (list, tuple)):
        raise _error("ARCHIVE-MIGRATION-ROW", "ledger must be one ordered sequence")
    materialized = tuple(dict(row) for row in rows)
    _work107_validate_closed_census(materialized)
    expected = build_work107_migration_rows(repository_root)
    if materialized != expected:
        raise _error("ARCHIVE-MIGRATION-REVIEWED", "ledger differs from reviewed mapping")
    return materialized


def _work107_migration_metadata_bytes() -> bytes:
    metadata = {
        "title": "MIG-0001: SDLC Taxonomy Convergence",
        "type": "content/archive-migration",
        "status": "accepted",
        "owner": "platform",
        "updated": "2026-08-12",
        "artifact_id": WORK107_MIGRATION_ID,
        "migration_id": WORK107_MIGRATION_ID,
    }
    return (
        "---\n"
        + "".join(
            f"{key}: {json.dumps(metadata[key], ensure_ascii=False, separators=(',', ':'))}\n"
            for key in WORK107_MIGRATION_METADATA_KEYS
        )
        + "---\n"
    ).encode("utf-8")


def render_work107_migration_document(
    rows: list[Mapping[str, object]] | tuple[Mapping[str, object], ...],
) -> bytes:
    materialized = tuple(dict(row) for row in rows)
    _work107_validate_closed_census(materialized)
    ledger = json.dumps(materialized, ensure_ascii=False, indent=2) + "\n"
    return (
        _work107_migration_metadata_bytes()
        + b"\n# MIG-0001: SDLC Taxonomy Convergence\n\n"
        + b"## Overview\n\nExact reviewed 93-to-93 Stage 98 stable rehome.\n\n"
        + b"## Migration Ledger\n\n"
        + WORK107_LEDGER_MARKER.encode("ascii")
        + b"\n\n```json\n"
        + ledger.encode("utf-8")
        + b"```\n\n## Recovery\n\n"
        + b"Each row binds the original source object, legacy envelope object, and stable record.\n"
    )


def parse_work107_migration_document(content: bytes) -> tuple[dict[str, object], ...]:
    if not isinstance(content, bytes) or not content.startswith(_work107_migration_metadata_bytes()):
        raise _error("ARCHIVE-MIGRATION-DOCUMENT", "migration frontmatter differs")
    marker = WORK107_LEDGER_MARKER.encode("ascii") + b"\n\n```json\n"
    if content.count(marker) != 1 or not content.endswith(
        b"```\n\n## Recovery\n\nEach row binds the original source object, legacy envelope object, and stable record.\n"
    ):
        raise _error("ARCHIVE-MIGRATION-DOCUMENT", "migration body differs")
    raw = content.split(marker, 1)[1].split(b"\n```\n", 1)[0]
    try:
        loaded = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _error("ARCHIVE-MIGRATION-DOCUMENT", "migration ledger JSON differs") from exc
    if not isinstance(loaded, list) or any(not isinstance(row, dict) for row in loaded):
        raise _error("ARCHIVE-MIGRATION-DOCUMENT", "migration ledger shape differs")
    rows = tuple(dict(row) for row in loaded)
    _work107_validate_closed_census(rows)
    if render_work107_migration_document(rows) != content:
        raise _error("ARCHIVE-MIGRATION-DOCUMENT", "migration document is noncanonical")
    return rows


def _work107_git_blob_oid(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()  # noqa: S324 - Git SHA-1 identity


def render_work107_stable_envelope(
    legacy_envelope: bytes,
    row: Mapping[str, object],
) -> bytes:
    """Transform only the outer wrapper required by one reviewed stable row."""

    materialized = dict(row)
    if tuple(materialized) != WORK107_LEDGER_FIELDS:
        raise _error("ARCHIVE-MIGRATION-FIELDS", "ledger field set differs")
    parsed = parse_archive_envelope(legacy_envelope)
    if (
        _work107_git_blob_oid(legacy_envelope) != materialized["legacy_envelope_blob"]
        or parsed.metadata.get("source_commit") != materialized["source_commit"]
        or parsed.metadata.get("source_blob") != materialized["source_blob"]
        or parsed.metadata.get("content_sha256") != materialized["content_sha256"]
    ):
        raise _error("ARCHIVE-MIGRATION-PROVENANCE", "legacy envelope differs")
    metadata: dict[str, object] = {}
    change_id: str | None = None
    kind = materialized.get("record_kind")
    artifact_id = materialized.get("artifact_id")
    if kind in {"change-plan", "change-task"} and isinstance(artifact_id, str):
        change_id = artifact_id.removeprefix("PLAN-").removeprefix("TASK-")
        if re.fullmatch(r"CHG-[0-9]{4}", change_id) is None:
            raise _error("ARCHIVE-MIGRATION-IDENTITY", "change identity differs")
    for key in ARCHIVE_STABLE_METADATA_KEYS:
        if key == "artifact_id":
            metadata[key] = artifact_id
        elif key == "change_id" and change_id is not None:
            metadata[key] = change_id
        elif key in parsed.metadata:
            metadata[key] = parsed.metadata[key]
    validate_archive_metadata(metadata)
    rendered = _metadata_bytes(metadata) + ARCHIVE_ENVELOPE_MARKER + b"\n" + parsed.payload
    reparsed = parse_archive_envelope(rendered)
    if reparsed.payload != parsed.payload:
        raise _error("ARCHIVE-MIGRATION-PAYLOAD", "stable payload differs")
    return rendered


def recover_work107_legacy_envelope(
    repository_root: str | Path,
    row: Mapping[str, object],
) -> ParsedArchiveEnvelope:
    """Recover and validate one old ArchiveEnvelope by independent commit/path/blob."""

    materialized = dict(row)
    if tuple(materialized) != WORK107_LEDGER_FIELDS:
        raise _error("ARCHIVE-MIGRATION-FIELDS", "ledger field set differs")
    commit = str(materialized["legacy_archive_commit"])
    legacy_path = str(materialized["legacy_path"])
    root, _object_id_length = _require_repository(Path(repository_root))
    blob_id, content = _work107_commit_path_blobs(root, commit, (legacy_path,))[legacy_path]
    if blob_id != materialized["legacy_envelope_blob"]:
        raise _error("ARCHIVE-MIGRATION-PROVENANCE", "legacy envelope object differs")
    parsed = parse_archive_envelope(content)
    if (
        parsed.metadata.get("source_commit") != materialized["source_commit"]
        or parsed.metadata.get("source_blob") != materialized["source_blob"]
        or parsed.metadata.get("content_sha256") != materialized["content_sha256"]
    ):
        raise _error("ARCHIVE-MIGRATION-PROVENANCE", "legacy envelope metadata differs")
    return parsed


MAX_ARCHIVE_RECORD_BYTES = MAX_GIT_BLOB_BYTES


def _open_parent_at(root: Path, path: PurePosixPath, *, code: str) -> tuple[int, str]:
    """Open every parent component relative to held descriptors without symlinks."""

    if not path.parts:
        raise _error(code, "path has no basename")
    current: int | None = None
    try:
        current = os.open(
            root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        for part in path.parts[:-1]:
            child = os.open(
                part,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=current,
            )
            os.close(current)
            current = child
        return current, path.name
    except OSError as exc:
        if current is not None:
            try:
                os.close(current)
            except OSError:
                pass
        raise _error(code, "path parent is unavailable") from exc


def _read_archive_record(root: Path, record: object) -> tuple[str, bytes]:
    canonical = _require_repository_path(record, field="record")
    pure = PurePosixPath(canonical)
    if (
        not pure.is_relative_to(PurePosixPath("docs/98.archive"))
        or pure == PurePosixPath("docs/98.archive/README.md")
        or pure.suffix != ".md"
    ):
        raise _error("RECOVERY-RECORD-PATH", "record must name an archive envelope")
    parent_fd: int | None = None
    descriptor: int | None = None
    try:
        parent_fd, name = _open_parent_at(root, pure, code="RECOVERY-RECORD-READ")
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=parent_fd,
        )
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise OSError
        if metadata.st_size > MAX_ARCHIVE_RECORD_BYTES:
            raise _error("RECOVERY-RECORD-SIZE", "archive record exceeds the limit")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(
                descriptor,
                min(65536, MAX_ARCHIVE_RECORD_BYTES + 1 - total),
            )
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_ARCHIVE_RECORD_BYTES:
                raise _error(
                    "RECOVERY-RECORD-SIZE", "archive record exceeds the limit"
                )
        content = b"".join(chunks)
        after = os.fstat(descriptor)
        linked = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except ArchiveContractError:
        raise
    except OSError as exc:
        raise _error("RECOVERY-RECORD-READ", "archive record is unavailable") from exc
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError as exc:
                raise _error("RECOVERY-RECORD-READ", "archive record close failed") from exc
        if parent_fd is not None:
            try:
                os.close(parent_fd)
            except OSError as exc:
                raise _error("RECOVERY-RECORD-READ", "archive parent close failed") from exc
    if (
        metadata.st_dev != after.st_dev
        or metadata.st_ino != after.st_ino
        or metadata.st_mode != after.st_mode
        or metadata.st_dev != linked.st_dev
        or metadata.st_ino != linked.st_ino
        or len(content) != metadata.st_size
    ):
        raise _error("RECOVERY-RECORD-CHANGED", "archive record changed during read")
    return canonical, content


@contextlib.contextmanager
def _confined_output(root: Path, output: object):
    if not isinstance(output, (str, Path)):
        raise _error("RECOVERY-OUTPUT-CONFINEMENT", "output must be an absolute path")
    candidate = Path(output)
    if not candidate.is_absolute():
        raise _error("RECOVERY-OUTPUT-CONFINEMENT", "output must be an absolute path")
    try:
        temporary_root = Path(tempfile.gettempdir()).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise _error("RECOVERY-OUTPUT-CONFINEMENT", "output parent is unavailable") from exc
    if (
        any(part in {".", ".."} for part in candidate.parts)
        or not candidate.is_relative_to(temporary_root)
        or candidate.is_relative_to(root)
        or not candidate.name
        or candidate.name in {".", ".."}
    ):
        raise _error(
            "RECOVERY-OUTPUT-CONFINEMENT",
            "output must remain outside the repository under the temporary root",
        )
    relative = PurePosixPath(candidate.relative_to(temporary_root).as_posix())
    parent_fd: int | None = None
    try:
        parent_fd, name = _open_parent_at(
            temporary_root,
            relative,
            code="RECOVERY-OUTPUT-CONFINEMENT",
        )
        yield _OutputTarget(parent_fd=parent_fd, name=name)
    finally:
        if parent_fd is not None:
            try:
                os.close(parent_fd)
            except OSError as exc:
                raise _error(
                    "RECOVERY-OUTPUT-WRITE", "output parent close failed"
                ) from exc


def _write_new_output(target: _OutputTarget, payload: bytes) -> None:
    descriptor: int | None = None
    created_identity: os.stat_result | None = None
    try:
        descriptor = os.open(
            target.name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=target.parent_fd,
        )
        created_identity = os.fstat(descriptor)
        if not stat.S_ISREG(created_identity.st_mode):
            raise OSError
        os.fchmod(descriptor, 0o600)
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError
            view = view[written:]
        os.fsync(descriptor)
        linked = os.stat(
            target.name,
            dir_fd=target.parent_fd,
            follow_symlinks=False,
        )
        if (
            linked.st_dev != created_identity.st_dev
            or linked.st_ino != created_identity.st_ino
            or not stat.S_ISREG(linked.st_mode)
        ):
            raise OSError
    except FileExistsError as exc:
        raise _error("RECOVERY-OUTPUT-EXISTS", "output already exists") from exc
    except OSError as exc:
        if created_identity is not None:
            try:
                linked = os.stat(
                    target.name,
                    dir_fd=target.parent_fd,
                    follow_symlinks=False,
                )
                if (
                    linked.st_dev == created_identity.st_dev
                    and linked.st_ino == created_identity.st_ino
                ):
                    os.unlink(target.name, dir_fd=target.parent_fd)
            except OSError:
                pass
        raise _error("RECOVERY-OUTPUT-WRITE", "output could not be written") from exc
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError as exc:
                raise _error("RECOVERY-OUTPUT-WRITE", "output close failed") from exc


def recover_archive_record(
    repository_root: str | Path,
    record: object,
    *,
    verify: bool = False,
    output: str | Path | None = None,
) -> RecoveryResult:
    """Verify one envelope or recover its exact payload to a new temp file."""

    if verify == (output is not None):
        raise _error("RECOVERY-OPERATION", "choose exactly one recovery operation")
    root, _object_length = _require_repository(Path(repository_root))
    _record_path, content = _read_archive_record(root, record)
    try:
        parsed = parse_archive_envelope(content)
        original_path = parsed.metadata["original_path"]
        source_commit = parsed.metadata["source_commit"]
        recovered = recover_git_blob(root, original_path, source_commit)
        parse_archive_envelope(content, expected=recovered)
    except (KeyError, TypeError) as exc:
        raise _error("RECOVERY-RECORD-METADATA", "archive metadata is invalid") from exc
    if output is not None:
        with _confined_output(root, output) as target:
            _write_new_output(target, recovered.source_bytes)
    return recovered


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--record", required=True)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--verify", action="store_true")
    operation.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        recovered = recover_archive_record(
            args.root,
            args.record,
            verify=args.verify,
            output=args.output,
        )
    except ArchiveContractError as exc:
        print(f"FAIL archive recovery code={exc.code}")
        return 1
    operation = "verify" if args.verify else "output"
    print(f"PASS archive recovery operation={operation} bytes={recovered.byte_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
