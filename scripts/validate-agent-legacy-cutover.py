#!/usr/bin/env python3
"""Validate retired agent surfaces and current instruction consumers."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import selectors
import signal
import stat
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any, NoReturn

import agent_registry_loader
import archive_recovery as recovery
import archive_validation as archive
import document_contracts as documents
import json_schema_validation

links = archive._load_canonical_link_module()

GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 10
GIT_CLEANUP_TIMEOUT_SECONDS = 2
MAX_GIT_STDOUT_BYTES = 262_144
MAX_GIT_STDERR_BYTES = 16_384
MAX_CANDIDATES = 2_048
MAX_CANDIDATE_PATH_BYTES = 1_024
MAX_REGULAR_FILE_BYTES = 8_388_608
MAX_DIAGNOSTIC_DETAIL_BYTES = 512
READ_CHUNK_BYTES = 65_536
GIT_ENVIRONMENT = {
    "GIT_ASKPASS": "/bin/false",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_LITERAL_PATHSPECS": "1",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
    "GCM_INTERACTIVE": "never",
    "HOME": "/dev/null",
    "LANG": "C",
    "LC_ALL": "C",
    "SSH_ASKPASS": "/bin/false",
    "XDG_CONFIG_HOME": "/dev/null",
}
GIT_ARGUMENT_ALLOWLIST = {
    ("rev-parse", "--show-toplevel"),
    ("ls-files", "-z", "--cached"),
}
RETIRED_SURFACES = (
    "docs/00.agent-governance/contracts/agent-role-semantics.json",
    "docs/00.agent-governance/contracts/agent-role-semantics.schema.json",
    "scripts/validate-agent-role-semantics.py",
    "tests/fixtures/agent-role-semantics.json",
    ".github/ABOUT.md",
)
RETIRED_OWNER_PATHS = (
    "docs/00.agent-governance/common-governance.md",
    "docs/00.agent-governance/harness-implementation-map.md",
    "docs/00.agent-governance/providers/agents-md.md",
)
RETIRED_TOKENS = RETIRED_SURFACES + RETIRED_OWNER_PATHS


ALLOWED_INTERNAL_SYMLINKS = (
    (".claude/output-styles", "../.agents/output-styles"),
    (".claude/skills", "../.agents/skills"),
    (".claude/workflows", "../.agents/workflows"),
    (".codex/output-styles", "../.agents/output-styles"),
    (".codex/skills", "../.agents/skills"),
    (".codex/workflows", "../.agents/workflows"),
)


def _bounded_diagnostic(detail: str) -> str:
    escaped: list[str] = []
    for character in str(detail):
        codepoint = ord(character)
        if character == "\n":
            escaped.append("\\n")
        elif character == "\r":
            escaped.append("\\r")
        elif character == "\t":
            escaped.append("\\t")
        elif codepoint < 0x20 or 0x7F <= codepoint <= 0x9F:
            escaped.append(f"\\x{codepoint:02x}")
        elif not character.isprintable():
            if codepoint <= 0xFFFF:
                escaped.append(f"\\u{codepoint:04x}")
            else:
                escaped.append(f"\\U{codepoint:08x}")
        else:
            escaped.append(character)
    encoded = "".join(escaped).encode("utf-8")
    if len(encoded) <= MAX_DIAGNOSTIC_DETAIL_BYTES:
        return encoded.decode("utf-8")
    suffix = b"..."
    prefix = encoded[: MAX_DIAGNOSTIC_DETAIL_BYTES - len(suffix)]
    return prefix.decode("utf-8", errors="ignore") + suffix.decode("ascii")


class ContractError(ValueError):
    """One stable cutover contract finding."""

    def __init__(self, rule_id: str, detail: str):
        self.rule_id = rule_id
        self.detail = _bounded_diagnostic(detail)
        super().__init__(f"{rule_id}: {self.detail}")


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


def fail(rule_id: str, detail: str) -> NoReturn:
    raise ContractError(rule_id, detail)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        value[key] = child
    return value


def _parse_json(text: str, source: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except (json.JSONDecodeError, DuplicateKeyError):
        fail("AGQC-LEGACY-JSON", f"{source}: invalid JSON")


def _relative_path(value: str) -> PurePosixPath:
    if (
        not value
        or value == "."
        or value.startswith("/")
        or "\\" in value
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        fail("AGQC-LEGACY-INPUT", f"unsafe repository path: {value!r}")
    return PurePosixPath(value)


def _same_identity(first: os.stat_result, second: os.stat_result) -> bool:
    return (
        first.st_dev,
        first.st_ino,
        stat.S_IFMT(first.st_mode),
    ) == (
        second.st_dev,
        second.st_ino,
        stat.S_IFMT(second.st_mode),
    )


def _same_stable_file_state(
    first: os.stat_result,
    second: os.stat_result,
) -> bool:
    """Compare all metadata that must not change across a bounded read."""

    return (
        first.st_dev,
        first.st_ino,
        first.st_mode,
        first.st_size,
        first.st_mtime_ns,
        first.st_ctime_ns,
    ) == (
        second.st_dev,
        second.st_ino,
        second.st_mode,
        second.st_size,
        second.st_mtime_ns,
        second.st_ctime_ns,
    )


class _RepositoryReader:
    """One root-dirfd, no-follow, bounded reader for repository content."""

    def __init__(self, root: Path):
        self.root_path = Path(os.path.abspath(os.fspath(root)))
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        if hasattr(os, "O_CLOEXEC"):
            flags |= os.O_CLOEXEC
        root_fd: int | None = None
        try:
            root_fd = os.open(self.root_path, flags)
            root_state = os.fstat(root_fd)
        except OSError as exc:
            if root_fd is not None:
                try:
                    os.close(root_fd)
                except OSError:
                    pass
            fail(
                "AGQC-LEGACY-INPUT",
                f"repository root is unavailable: {exc.strerror}",
            )
        self.root_fd = root_fd
        self._closed = False
        if not stat.S_ISDIR(root_state.st_mode):
            os.close(self.root_fd)
            self._closed = True
            fail(
                "AGQC-LEGACY-INPUT",
                "repository root must be a non-symlink directory",
            )

    def __enter__(self) -> _RepositoryReader:
        return self

    def __exit__(self, _type: object, _value: object, _traceback: object) -> None:
        self.close()

    def close(self) -> None:
        if not self._closed:
            os.close(self.root_fd)
            self._closed = True

    @staticmethod
    def _close_descriptors(descriptors: list[int]) -> None:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass

    def _open_parents(
        self,
        relative: PurePosixPath,
        *,
        missing_ok: bool,
    ) -> tuple[int | None, list[int], list[tuple[int, str, int]]]:
        directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        if hasattr(os, "O_CLOEXEC"):
            directory_flags |= os.O_CLOEXEC
        current = self.root_fd
        descriptors: list[int] = []
        edges: list[tuple[int, str, int]] = []
        pending_descriptor: int | None = None
        try:
            for part in relative.parts[:-1]:
                pending_descriptor = os.open(
                    part,
                    directory_flags,
                    dir_fd=current,
                )
                child_state = os.fstat(pending_descriptor)
                entry_state = os.stat(part, dir_fd=current, follow_symlinks=False)
                if not stat.S_ISDIR(child_state.st_mode) or not _same_identity(
                    child_state, entry_state
                ):
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"repository parent changed or is unsafe: {relative.as_posix()}",
                    )
                descriptors.append(pending_descriptor)
                edges.append((current, part, pending_descriptor))
                current = pending_descriptor
                pending_descriptor = None
            return current, descriptors, edges
        except FileNotFoundError:
            if pending_descriptor is not None:
                self._close_descriptors([pending_descriptor])
            self._close_descriptors(descriptors)
            if missing_ok:
                return None, [], []
            fail(
                "AGQC-LEGACY-INPUT",
                f"repository parent is missing: {relative.as_posix()}",
            )
        except ContractError:
            if pending_descriptor is not None:
                self._close_descriptors([pending_descriptor])
            self._close_descriptors(descriptors)
            raise
        except OSError as exc:
            if pending_descriptor is not None:
                self._close_descriptors([pending_descriptor])
            self._close_descriptors(descriptors)
            fail(
                "AGQC-LEGACY-INPUT",
                f"repository parent is unavailable {relative.as_posix()}: {exc.strerror}",
            )

    @staticmethod
    def _verify_edges(edges: list[tuple[int, str, int]], relative: str) -> None:
        try:
            for parent_fd, name, child_fd in edges:
                entry_state = os.stat(
                    name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
                child_state = os.fstat(child_fd)
                if not stat.S_ISDIR(entry_state.st_mode) or not _same_identity(
                    entry_state, child_state
                ):
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"repository parent changed during read: {relative}",
                    )
        except ContractError:
            raise
        except OSError as exc:
            fail(
                "AGQC-LEGACY-INPUT",
                f"repository parent changed during read {relative}: {exc.strerror}",
            )

    def state(self, value: str) -> int | None:
        safe = _relative_path(value)
        parent_fd, descriptors, edges = self._open_parents(
            safe,
            missing_ok=True,
        )
        if parent_fd is None:
            return None
        try:
            try:
                state = os.stat(
                    safe.name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                return None
            self._verify_edges(edges, value)
            return state.st_mode
        except ContractError:
            raise
        except OSError as exc:
            fail(
                "AGQC-LEGACY-INPUT",
                f"repository path is unavailable {value}: {exc.strerror}",
            )
        finally:
            self._close_descriptors(descriptors)

    def _payload(
        self,
        value: str,
        *,
        read: bool,
        allow_declared_symlink: bool,
        missing_rule: str,
        max_bytes: int = MAX_REGULAR_FILE_BYTES,
    ) -> bytes | None:
        if type(max_bytes) is not int or max_bytes <= 0:
            fail("AGQC-LEGACY-INPUT", "owner byte limit must be a positive integer")
        limit = min(max_bytes, MAX_REGULAR_FILE_BYTES)
        safe = _relative_path(value)
        parent_fd, descriptors, edges = self._open_parents(
            safe,
            missing_ok=False,
        )
        assert parent_fd is not None
        file_descriptor: int | None = None
        try:
            try:
                before = os.stat(
                    safe.name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                fail(missing_rule, f"required repository path is missing: {value}")
            if stat.S_ISLNK(before.st_mode):
                if not allow_declared_symlink:
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"repository path must be a regular non-symlink file: {value}",
                    )
                try:
                    target = os.readlink(safe.name, dir_fd=parent_fd)
                except (OSError, UnicodeError) as exc:
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"cannot inspect repository symlink {value}: {exc}",
                    )
                _validate_allowed_symlink(value, target)
                after = os.stat(
                    safe.name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
                if not _same_identity(before, after):
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"repository symlink changed during inspection: {value}",
                    )
                self._verify_edges(edges, value)
                return None
            if not stat.S_ISREG(before.st_mode):
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"repository path is not regular: {value}",
                )
            if before.st_size > limit:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"repository file exceeds the byte limit: {value}",
                )
            if not read:
                self._verify_edges(edges, value)
                return b""

            file_flags = os.O_RDONLY | os.O_NOFOLLOW
            if hasattr(os, "O_NONBLOCK"):
                file_flags |= os.O_NONBLOCK
            if hasattr(os, "O_CLOEXEC"):
                file_flags |= os.O_CLOEXEC
            file_descriptor = os.open(
                safe.name,
                file_flags,
                dir_fd=parent_fd,
            )
            opened = os.fstat(file_descriptor)
            if not stat.S_ISREG(opened.st_mode) or not _same_stable_file_state(
                before, opened
            ):
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"repository file changed type or identity: {value}",
                )
            if opened.st_size > limit:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"repository file exceeds the byte limit: {value}",
                )

            chunks: list[bytes] = []
            total = 0
            while True:
                remaining = limit - total
                chunk = os.read(
                    file_descriptor,
                    min(READ_CHUNK_BYTES, remaining + 1),
                )
                if not chunk:
                    break
                total += len(chunk)
                if total > limit:
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"repository file grew beyond the byte limit: {value}",
                    )
                chunks.append(chunk)

            final_state = os.fstat(file_descriptor)
            final_entry = os.stat(
                safe.name,
                dir_fd=parent_fd,
                follow_symlinks=False,
            )
            if (
                final_state.st_size > limit
                or not _same_stable_file_state(opened, final_state)
                or not _same_stable_file_state(final_state, final_entry)
            ):
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"repository file changed or grew during read: {value}",
                )
            self._verify_edges(edges, value)
            return b"".join(chunks)
        except ContractError:
            raise
        except OSError as exc:
            fail(
                "AGQC-LEGACY-INPUT",
                f"repository file is unavailable {value}: {exc.strerror}",
            )
        finally:
            if file_descriptor is not None:
                try:
                    os.close(file_descriptor)
                except OSError:
                    pass
            self._close_descriptors(descriptors)

    def read_bytes(
        self,
        value: str,
        *,
        missing_rule: str = "AGQC-LEGACY-INPUT",
        max_bytes: int = MAX_REGULAR_FILE_BYTES,
    ) -> bytes:
        payload = self._payload(
            value,
            read=True,
            allow_declared_symlink=False,
            missing_rule=missing_rule,
            max_bytes=max_bytes,
        )
        assert payload is not None
        return payload

    def read_text(
        self,
        value: str,
        *,
        missing_rule: str = "AGQC-LEGACY-INPUT",
        max_bytes: int = MAX_REGULAR_FILE_BYTES,
    ) -> str:
        try:
            return self.read_bytes(
                value, missing_rule=missing_rule, max_bytes=max_bytes
            ).decode("utf-8")
        except UnicodeError as exc:
            fail("AGQC-LEGACY-INPUT", f"repository file is not UTF-8 {value}: {exc}")

    def candidate_payload(self, value: str, *, read: bool) -> bytes | None:
        return self._payload(
            value,
            read=read,
            allow_declared_symlink=True,
            missing_rule="AGQC-LEGACY-INPUT",
        )


def _load_json_regular(
    reader: _RepositoryReader,
    value: str,
    *,
    missing_rule: str = "AGQC-LEGACY-INPUT",
    max_bytes: int = MAX_REGULAR_FILE_BYTES,
) -> Any:
    return _parse_json(
        reader.read_text(value, missing_rule=missing_rule, max_bytes=max_bytes),
        value,
    )


def _validate_allowed_symlink(relative: str, target: str) -> None:
    expected = dict(ALLOWED_INTERNAL_SYMLINKS).get(relative)
    if expected is None or target != expected:
        fail(
            "AGQC-LEGACY-INPUT",
            f"undeclared or changed symlink: {relative} -> {target}",
        )
    lexical_parts = list(PurePosixPath(relative).parent.parts)
    for part in PurePosixPath(target).parts:
        if part == "..":
            if not lexical_parts:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"allowed symlink escapes repository: {relative}",
                )
            lexical_parts.pop()
        elif part not in ("", "."):
            lexical_parts.append(part)
    if not lexical_parts:
        fail(
            "AGQC-LEGACY-INPUT",
            f"allowed symlink escapes repository: {relative}",
        )


def _terminate_process(process: subprocess.Popen[bytes]) -> None:
    cleanup_deadline = time.monotonic() + GIT_CLEANUP_TIMEOUT_SECONDS
    remaining_wait_allowance = GIT_CLEANUP_TIMEOUT_SECONDS

    def reap_with_remaining_allowance() -> bool:
        nonlocal remaining_wait_allowance
        remaining_deadline = cleanup_deadline - time.monotonic()
        timeout = min(remaining_wait_allowance, remaining_deadline)
        if timeout <= 0:
            return False
        remaining_wait_allowance -= timeout
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            return False
        return True

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except OSError:
        pass
    if process.poll() is None:
        try:
            process.kill()
        except ProcessLookupError:
            pass
    if reap_with_remaining_allowance() or process.poll() is not None:
        return
    if reap_with_remaining_allowance() or process.poll() is not None:
        return
    fail("AGQC-LEGACY-INPUT", "Git process cleanup timed out")


def _close_process_pipes(process: subprocess.Popen[bytes]) -> None:
    for stream in (process.stdout, process.stderr):
        if stream is not None:
            try:
                stream.close()
            except OSError:
                pass


def _drain_process(
    process: subprocess.Popen[bytes],
    *,
    timeout_seconds: float,
    stdout_limit: int,
    stderr_limit: int,
    detail: str,
) -> tuple[bytes, bytes, int]:
    """Drain both process pipes with closed memory, time, and cleanup bounds."""

    if process.stdout is None or process.stderr is None:
        _terminate_process(process)
        fail("AGQC-LEGACY-INPUT", f"{detail}: Git pipes are unavailable")
    streams = {
        process.stdout.fileno(): ("stdout", process.stdout, stdout_limit),
        process.stderr.fileno(): ("stderr", process.stderr, stderr_limit),
    }
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    deadline = time.monotonic() + timeout_seconds
    selector = selectors.DefaultSelector()
    try:
        for descriptor, (_name, stream, _limit) in streams.items():
            os.set_blocking(descriptor, False)
            selector.register(stream, selectors.EVENT_READ)
        active = set(streams)
        while active:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                fail("AGQC-LEGACY-INPUT", f"{detail}: Git command timed out")
            events = selector.select(remaining)
            if not events:
                fail("AGQC-LEGACY-INPUT", f"{detail}: Git command timed out")
            for key, _mask in events:
                descriptor = key.fileobj.fileno()
                name, stream, limit = streams[descriptor]
                allowance = limit - len(buffers[name])
                try:
                    chunk = os.read(
                        descriptor,
                        min(READ_CHUNK_BYTES, allowance + 1),
                    )
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(stream)
                    active.remove(descriptor)
                    continue
                buffers[name].extend(chunk)
                if len(buffers[name]) > limit:
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"{detail}: Git {name} exceeded the byte limit",
                    )
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            fail("AGQC-LEGACY-INPUT", f"{detail}: Git command timed out")
        try:
            returncode = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            fail("AGQC-LEGACY-INPUT", f"{detail}: Git command timed out")
        return bytes(buffers["stdout"]), bytes(buffers["stderr"]), returncode
    except ContractError:
        _terminate_process(process)
        raise
    except OSError as exc:
        _terminate_process(process)
        fail("AGQC-LEGACY-INPUT", f"{detail}: Git pipe failure: {exc.strerror}")
    finally:
        selector.close()
        _close_process_pipes(process)


def _git_stdout(
    reader: _RepositoryReader,
    arguments: tuple[str, ...],
    detail: str,
) -> bytes:
    if arguments not in GIT_ARGUMENT_ALLOWLIST:
        fail("AGQC-LEGACY-INPUT", "Git argument vector is not allowlisted")
    root_fd_path = f"/proc/self/fd/{reader.root_fd}"
    command = [
        GIT_EXECUTABLE,
        "--no-pager",
        "--no-optional-locks",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.untrackedCache=false",
        "-c",
        "core.attributesFile=/dev/null",
        "-c",
        "core.excludesFile=/dev/null",
        "-C",
        root_fd_path,
        *arguments,
    ]
    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            env=dict(GIT_ENVIRONMENT),
            pass_fds=(reader.root_fd,),
            close_fds=True,
            start_new_session=True,
        )
    except OSError as exc:
        fail("AGQC-LEGACY-INPUT", f"{detail}: {exc.strerror}")
    stdout, _stderr, returncode = _drain_process(
        process,
        timeout_seconds=GIT_TIMEOUT_SECONDS,
        stdout_limit=MAX_GIT_STDOUT_BYTES,
        stderr_limit=MAX_GIT_STDERR_BYTES,
        detail=detail,
    )
    if returncode != 0:
        fail("AGQC-LEGACY-INPUT", detail)
    return stdout


def _parse_git_candidates(raw: bytes) -> tuple[str, ...]:
    if raw and not raw.endswith(b"\0"):
        fail("AGQC-LEGACY-INPUT", "Git candidate output is not NUL terminated")
    encoded = raw[:-1].split(b"\0") if raw else []
    if len(encoded) > MAX_CANDIDATES:
        fail("AGQC-LEGACY-INPUT", "Git candidate count exceeded the limit")
    if len(encoded) != len(set(encoded)):
        fail("AGQC-LEGACY-INPUT", "Git candidate output contains duplicates")
    candidates: list[str] = []
    for value in sorted(encoded):
        if len(value) > MAX_CANDIDATE_PATH_BYTES:
            fail("AGQC-LEGACY-INPUT", "Git candidate path exceeded the byte limit")
        try:
            candidate = value.decode("utf-8")
        except UnicodeError:
            fail("AGQC-LEGACY-INPUT", "Git candidate path is not UTF-8")
        candidates.append(_relative_path(candidate).as_posix())
    return tuple(candidates)


def _repository_candidates(reader: _RepositoryReader) -> tuple[str, ...]:
    top_level = _git_stdout(
        reader,
        ("rev-parse", "--show-toplevel"),
        "requested root is not a Git worktree top level",
    )
    if top_level != os.fsencode(reader.root_path) + b"\n":
        fail(
            "AGQC-LEGACY-INPUT",
            "requested root is not the Git worktree top level",
        )
    raw = _git_stdout(
        reader,
        ("ls-files", "-z", "--cached"),
        "Git repository candidate discovery failed",
    )
    return _parse_git_candidates(raw)


def _candidate_payload(root: Path, relative: str, *, read: bool) -> bytes | None:
    with _RepositoryReader(root) as reader:
        return reader.candidate_payload(relative, read=read)


def _require_candidate(
    reader: _RepositoryReader,
    candidates: set[str],
    path: str,
    *,
    missing_rule: str = "AGQC-LEGACY-INPUT",
) -> None:
    if path not in candidates:
        fail(
            missing_rule,
            f"required repository path is absent from the Git index: {path}",
        )
    mode = reader.state(path)
    if mode is None:
        fail(missing_rule, f"required repository path is missing: {path}")
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        fail(
            "AGQC-LEGACY-INPUT",
            f"required repository path is not a regular file: {path}",
        )


@dataclass(frozen=True)
class ConsumerOwners:
    document_registry: documents.Registry
    native_paths: frozenset[str]
    enforcement_paths: frozenset[str]
    proof: Any


def _trusted_script(filename: str) -> ModuleType:
    path = Path(__file__).with_name(filename)
    name = "_legacy_owner_" + path.stem.replace("-", "_")
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        fail("AGQC-LEGACY-OWNER", "owner implementation is unavailable")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def _owner_object(
    reader: _RepositoryReader,
    path: str,
    *,
    max_bytes: int = MAX_REGULAR_FILE_BYTES,
) -> dict[str, Any]:
    value = _load_json_regular(reader, path, max_bytes=max_bytes)
    if not isinstance(value, dict):
        fail("AGQC-LEGACY-JSON", "owner input must be an object")
    return value


def _load_owners(
    reader: _RepositoryReader, candidates: tuple[str, ...]
) -> ConsumerOwners:
    """Use canonical typed owners; identity establishes responsibility, not correctness."""

    candidate_set = set(candidates)
    terminal = agent_registry_loader.load_terminal_validator()
    affected = _trusted_script("validate-affected-surfaces.py")
    for path in (
        terminal.REGISTRY_PATH,
        terminal.REGISTRY_SCHEMA_PATH,
        affected.CONTRACT_PATH,
        affected.SCHEMA_PATH,
        documents.REGISTRY_PATH,
        documents.SCHEMA_PATH,
    ):
        _require_candidate(reader, candidate_set, path.as_posix())
    registry = _owner_object(reader, terminal.REGISTRY_PATH.as_posix())
    contract = _owner_object(reader, affected.CONTRACT_PATH.as_posix())
    schema = _owner_object(reader, affected.SCHEMA_PATH.as_posix())
    document_registry = _owner_object(
        reader,
        documents.REGISTRY_PATH.as_posix(),
        max_bytes=documents.REGISTRY_MAX_BYTES,
    )
    document_schema = _owner_object(
        reader, documents.SCHEMA_PATH.as_posix(), max_bytes=documents.REGISTRY_MAX_BYTES
    )

    def read_current_bytes(path: str, max_bytes: int) -> bytes:
        return reader.read_bytes(path, max_bytes=max_bytes)

    def read_symlink(path: str) -> str:
        if reader.candidate_payload(path, read=False) is not None:
            fail("AGQC-LEGACY-INPUT", "declared adapter must be a checked symlink")
        return dict(ALLOWED_INTERNAL_SYMLINKS)[path]

    try:
        terminal.validate_registry(reader.root_path, registry, check_files=True)
        entrypoints = affected.validator_script_paths(
            reader.root_path, contract, raw_schema=schema
        )
        templates = frozenset(
            PurePosixPath(profile["template_source"])
            for profile in document_registry.get("profiles", [])
            if isinstance(profile, dict)
            and isinstance(profile.get("template_source"), str)
        )
        for template in templates:
            _require_candidate(reader, candidate_set, template.as_posix())
        validated_registry = documents.load_registry(
            reader.root_path,
            raw_registry=document_registry,
            raw_schema=document_schema,
            template_regular_paths=templates,
        )
        proof = links.repository_historical_migration_proof(
            reader.root_path,
            registry=validated_registry,
            raw_schema=document_schema,
            read_current_bytes=read_current_bytes,
            read_symlink=read_symlink,
        )
    except (ValueError, OSError, KeyError, TypeError):
        fail("AGQC-LEGACY-OWNER", "canonical owner validation failed")
    if not isinstance(proof.document_registry, documents.Registry):
        fail("AGQC-LEGACY-OWNER", "validated document registry is unavailable")
    native_paths = {
        *(provider["gateway"] for provider in registry["providers"]),
        *(skill["path"] for skill in registry["skills"]),
        *(path for role in registry["roles"] for path in role["projections"].values()),
    }
    # These are the particular trusted implementations delegated above, not a
    # search through arbitrary imports, source suffixes, or candidate bytes.
    source_root = Path(__file__).absolute().parent.parent
    delegates = (
        terminal,
        affected,
        links,
        documents,
        archive,
        recovery,
        json_schema_validation,
    )
    helpers = {
        Path(module.__file__).absolute().relative_to(source_root).as_posix()
        for module in delegates
    }
    return ConsumerOwners(
        proof.document_registry,
        frozenset(native_paths),
        entrypoints | helpers,
        proof,
    )


def _published_or_native(path: str, owners: ConsumerOwners) -> bool:
    if path in owners.native_paths:
        return True
    try:
        documents.classify_path(owners.document_registry, PurePosixPath(path))
    except documents.DocumentContractError as exc:
        if all(item.rule_id == "REGISTRY_ROUTE_UNCOVERED" for item in exc.diagnostics):
            return False
        fail("AGQC-LEGACY-OWNER", "document classification is ambiguous")
    return True


def _retired_mentions(path: str, text: str) -> frozenset[str]:
    mentions = {token for token in RETIRED_TOKENS if token in text}
    for link in links.rendered_local_links(text, PurePosixPath(path)):
        if link.kind == "local" and link.target is not None:
            target = link.target.as_posix()
            if target in RETIRED_TOKENS:
                mentions.add(target)
    return frozenset(mentions)


def _historical_dispositions_cover(
    path: str, raw: bytes, mentions: frozenset[str], proof: Any
) -> bool:
    # Byte identity, not membership: the proof declares that this document's
    # mentions are historical as of reviewed bytes. Once the document changes,
    # a mention could have become live again, so coverage must be re-declared.
    if proof.consumers.get(path) != raw:
        return False
    literal_dispositions = getattr(proof, "literal_dispositions", {})
    rendered_dispositions = getattr(proof, "rendered_dispositions", {})
    if any(owner == path for owner, _ in literal_dispositions) and not any(
        owner == path for owner, _ in rendered_dispositions
    ):
        return all((path, token) in literal_dispositions for token in mentions)
    return all(
        isinstance(proof.terminal_targets.get(token), str)
        and proof.terminal_targets[token] != token
        for token in mentions
    )


def _scan_consumers_with_reader(
    reader: _RepositoryReader,
    candidates: tuple[str, ...] | None = None,
    owners: ConsumerOwners | None = None,
) -> tuple[int, int, list[str]]:
    if candidates is None:
        candidates = _repository_candidates(reader)
    if owners is None:
        owners = _load_owners(reader, candidates)
    scanned = evidence = 0
    consumers: list[str] = []
    for path in candidates:
        if path.startswith("tests/"):
            continue
        if path.startswith("docs/98.archive/completed/"):
            # A retained document is terminal work, not a current instruction.
            # It names the paths it named when it was finished, and the
            # retiring migration row is what pins that evidence.
            continue
        raw = reader.candidate_payload(path, read=True)
        if raw is None:
            continue
        scanned += 1
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeError:
            if any(token.encode("utf-8") in raw for token in RETIRED_TOKENS):
                fail("AGQC-LEGACY-INPUT", "candidate consumer is not UTF-8")
            continue
        declaration = owners.proof.declarations.get(path)
        if declaration is not None:
            if raw != declaration.source_bytes:
                fail("AGQC-LEGACY-OWNER", "migration declaration bytes changed")
            text = declaration.remaining_text
        archive_payload = getattr(owners.proof, "archive_payloads", {}).get(path)
        if archive_payload is not None:
            if raw != archive_payload.input_bytes:
                fail("AGQC-LEGACY-OWNER", "archive payload bytes changed")
            text = archive_payload.remaining_text
        mentions = _retired_mentions(path, text)
        if not mentions:
            continue
        if _historical_dispositions_cover(path, raw, mentions, owners.proof):
            evidence += 1
            continue
        if _published_or_native(path, owners):
            consumers.append(path)
            continue
        if path in owners.enforcement_paths:
            evidence += 1
            continue
        # Unknown token-bearing text remains an enforceable consumer.
        consumers.append(path)
    return scanned, evidence, consumers


def _scan_consumers(
    root: Path, candidates: tuple[str, ...] | None = None
) -> tuple[int, int, list[str]]:
    with _RepositoryReader(root) as reader:
        return _scan_consumers_with_reader(reader, candidates)


def validate_repository(root: Path) -> dict[str, int]:
    """Check unique retired surfaces and instruction uses; delegate history proof."""

    with _RepositoryReader(root) as reader:
        candidates = _repository_candidates(reader)
        candidate_set = set(candidates)
        for path in RETIRED_TOKENS:
            if path in candidate_set:
                reader.state(path)
                fail("AGQC-LEGACY-RETIRED", "retired surface remains: " + path)
        owners = _load_owners(reader, candidates)
        for path in RETIRED_TOKENS:
            target = owners.proof.terminal_targets.get(path)
            if not isinstance(target, str) or target == path:
                fail(
                    "AGQC-LEGACY-REPLACEMENT",
                    "terminal replacement proof is unavailable",
                )
            _require_candidate(
                reader, candidate_set, target, missing_rule="AGQC-LEGACY-REPLACEMENT"
            )
            reader.read_bytes(target, missing_rule="AGQC-LEGACY-REPLACEMENT")
        scanned, evidence, consumers = _scan_consumers_with_reader(
            reader, candidates, owners
        )
        if consumers:
            fail(
                "AGQC-LEGACY-CONSUMER",
                "current instruction retains a retired path: " + consumers[0],
            )
    return {
        "retiredSurfaces": len(RETIRED_SURFACES),
        "retiredOwners": len(RETIRED_OWNER_PATHS),
        "activeConsumers": len(consumers),
        "scannedFiles": scanned,
        "evidenceReferences": evidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    try:
        counts = validate_repository(args.root)
        print(
            "[PASS] agent legacy cutover: "
            + " ".join(f"{key}={value}" for key, value in counts.items())
        )
    except ContractError as exc:
        print(f"[FAIL] {exc.rule_id}: {exc.detail}", file=sys.stderr)
        return 1
    except Exception:
        print("[FAIL] AGQC-LEGACY-INPUT: invalid input", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
