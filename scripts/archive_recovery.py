"""Private ARWB-001 Git-object recovery and ArchiveEnvelope.v1 fixtures.

This module deliberately has no command-line entry point and does not activate
the production document registry, archive form, lifecycle admission, or corpus
validation.  Later ARWB packages may consume the byte-exact primitives after
their own production contracts are approved.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml


ARCHIVE_ENVELOPE_MARKER = (
    b"<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->"
)
GIT_TIMEOUT_SECONDS = 10.0
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
class ParsedArchiveEnvelope:
    """Parsed ArchiveEnvelope.v1 metadata and byte-preserved payload."""

    metadata: dict[str, object]
    payload: bytes = field(repr=False)


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


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_safe_git_environment(),
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise _error(
            "RECOVERY-GIT-TIMEOUT",
            "Git object lookup exceeded its bounded timeout",
        ) from exc
    except OSError as exc:
        raise _error(
            "RECOVERY-GIT-STARTUP",
            "Git object lookup could not start",
        ) from exc


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
    if not path.parts or path.parts[0] != "docs":
        raise _error("ARCHIVE-METADATA-PATH", f"{field} must remain under docs")
    return path.as_posix()


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

    blob = _git(root, "cat-file", "blob", source_blob)
    if blob.returncode != 0:
        raise _error("RECOVERY-OBJECT-MISSING", "source blob object is unavailable")
    source_bytes = blob.stdout
    try:
        source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise _error("RECOVERY-NON-UTF8", "source blob is not UTF-8 Markdown") from exc

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


def validate_archive_metadata(metadata: Mapping[str, object]) -> None:
    """Validate the closed fixture-only ArchiveEnvelope.v1 metadata schema."""

    if not isinstance(metadata, Mapping):
        raise _error("ARCHIVE-METADATA-TYPE", "metadata must be a mapping")
    if tuple(metadata) != ARCHIVE_METADATA_KEYS:
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
    if reason in REPLACEMENT_REQUIRED_REASONS:
        _require_repository_path(replacement, field="replacement")
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


def _metadata_bytes(metadata: Mapping[str, object]) -> bytes:
    lines = ["---\n"]
    for key in ARCHIVE_METADATA_KEYS:
        lines.append(
            f"{key}: {json.dumps(metadata[key], ensure_ascii=False, separators=(',', ':'))}\n"
        )
    lines.append("---\n")
    return "".join(lines).encode("utf-8")


def render_fixture_archive_envelope(
    metadata: Mapping[str, object],
    recovered: RecoveryResult,
    payload: bytes,
) -> bytes:
    """Render one fixture envelope only when payload is the recovered Git blob."""

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
    validate_archive_metadata(metadata)
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

    return ParsedArchiveEnvelope(metadata=metadata, payload=payload)
