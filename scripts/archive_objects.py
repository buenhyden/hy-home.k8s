#!/usr/bin/env python3
"""Read the Git objects an ADR-0039 Retention Envelope names.

A retained unit is compared as its entries: path relative to the unit root,
file mode, and object id. The lifecycle gate reads a proposal against its
comparison base, and full validation re-verifies every catalog row against the
history it names. Any Git failure reads as an absent object, so a caller fails
closed rather than skipping.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

if __package__:
    from scripts.archive_recovery import ArchiveContractError, _git_capture_bounded
else:
    from archive_recovery import (  # type: ignore[no-redef]
        ArchiveContractError,
        _git_capture_bounded,
    )


GIT_ARGUMENTS = (
    "--no-replace-objects",
    "--literal-pathspecs",
    "-c",
    "core.fsmonitor=false",
)
LISTING_MAX_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True, order=True)
class UnitEntry:
    """One tracked entry, relative to its unit root ("" for a document unit)."""

    path: str
    mode: str
    object_id: str


def _git(root: Path, *arguments: str) -> bytes | None:
    try:
        completed = _git_capture_bounded(
            root, *GIT_ARGUMENTS, *arguments, stdout_limit=LISTING_MAX_BYTES
        )
    except ArchiveContractError:
        return None
    return completed.stdout if completed.returncode == 0 else None


def object_type(root: Path, commit: str, path: PurePosixPath) -> str | None:
    """Return `blob`, `tree`, or another type for `<commit>:<path>`, if it exists."""

    raw = _git(root, "cat-file", "-t", f"{commit}:{path.as_posix()}")
    return raw.decode("ascii", errors="replace").strip() if raw else None


def is_ancestor(root: Path, commit: str, descendant: str) -> bool:
    return _git(root, "merge-base", "--is-ancestor", commit, descendant) is not None


_BRANCH_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*\Z")


def is_shallow_repository(root: Path) -> bool:
    """Return True unless Git reports a complete, unbounded history.

    Any unreadable answer fails closed as shallow, so a partial clone with an
    unavailable history never reads as an ordinary repository.
    """

    raw = _git(root, "rev-parse", "--is-shallow-repository")
    return raw is None or raw.strip() != b"false"


def resolve_default_branch(root: Path, default_branch: str) -> str | None:
    """Resolve the registry's default branch to a checkable ref.

    A remote-tracking ref for the name wins when one exists; a local branch of
    the same name is used otherwise. Neither existing resolves to None rather
    than falling back to `HEAD`, per ADR-0040.
    """

    if _BRANCH_NAME.fullmatch(default_branch) is None:
        return None
    raw = _git(
        root, "for-each-ref", "--format=%(refname)", f"refs/remotes/*/{default_branch}"
    )
    if raw:
        try:
            names = sorted(raw.decode("ascii", errors="strict").splitlines())
        except UnicodeDecodeError:
            return None
        if names:
            return names[0]
    local = f"refs/heads/{default_branch}"
    if (
        _git(root, "rev-parse", "--verify", "--quiet", "--end-of-options", local)
        is not None
    ):
        return local
    return None


def blob_text(root: Path, specification: str) -> str | None:
    """Return a UTF-8 blob named as `<commit>:<path>` or `:<path>` (the index)."""

    raw = _git(root, "cat-file", "blob", specification)
    if raw is None:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _entries(
    raw: bytes | None, prefix: str, *, staged: bool
) -> tuple[UnitEntry, ...] | None:
    if raw is None:
        return None
    entries: list[UnitEntry] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        header, _, name = record.partition(b"\t")
        try:
            path = name.decode("utf-8")
        except UnicodeDecodeError:
            return None
        if path == prefix:
            relative = ""
        elif path.startswith(prefix + "/"):
            relative = path[len(prefix) + 1 :]
        else:
            continue
        fields = header.split(b" ")
        if len(fields) != 3:
            return None
        # `ls-files --stage` prints mode, object, stage; `ls-tree` prints mode, type, object.
        mode, object_id = (fields[0], fields[1]) if staged else (fields[0], fields[2])
        if staged and fields[2] != b"0":
            return None
        entries.append(UnitEntry(relative, mode.decode(), object_id.decode()))
    return tuple(sorted(entries))


def commit_entries(
    root: Path, commit: str, path: PurePosixPath
) -> tuple[UnitEntry, ...] | None:
    """Return every entry at or under `path` in `commit`; None when unreadable."""

    prefix = path.as_posix()
    raw = _git(root, "ls-tree", "-r", "-z", "--full-tree", commit, "--", prefix)
    return _entries(raw, prefix, staged=False)


def index_entries(root: Path, path: PurePosixPath) -> tuple[UnitEntry, ...] | None:
    """Return every stage-zero index entry at or under `path`."""

    prefix = path.as_posix()
    raw = _git(root, "ls-files", "--stage", "-z", "--", prefix)
    return _entries(raw, prefix, staged=True)
