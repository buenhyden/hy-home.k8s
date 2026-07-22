"""Fail-closed Reference Information Architecture validation primitives."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import stat
import subprocess
import tempfile
import time
from types import MappingProxyType
from typing import Callable, Mapping, Sequence
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator


DEFAULT_CONTRACT_PATH = Path(
    "docs/90.references/data/reference-information-architecture.json"
)
CANONICAL_SCHEMA_PATH = Path(
    "docs/90.references/data/reference-information-architecture.schema.json"
)
DATA_ASSET_ROOT = Path("docs/90.references/data")
DATA_ASSET_README = DATA_ASSET_ROOT / "README.md"
REGISTRY_PATH = Path("docs/99.templates/support/document-profiles.json")
ALLOWED_PATH_ROOTS = frozenset({"docs", "scripts", "tests"})
GIT_SHA1_PATTERN = re.compile(r"^git-sha1:([0-9a-f]{40})$")
OID_PATTERN = re.compile(r"^[0-9a-f]{40}$")
PACK_ID_PATTERN = re.compile(
    r"^[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)*$"
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
REPOSITORY_PATH_PATTERN = re.compile(
    r"^(?:docs|scripts|tests)(?:/(?!\.{1,2}(?:/|$))[A-Za-z0-9._-]+)+$"
)

GIT_EXECUTABLE = "/usr/bin/git"
GIT_TIMEOUT_SECONDS = 10
MAX_BLOB_BYTES = 2_000_000
MAX_METADATA_BYTES = 65_536
MAX_STDERR_BYTES = 16_384
CLOSED_GIT_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "PATH": "/usr/bin:/bin",
    "LANG": "C",
    "LC_ALL": "C",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_LITERAL_PATHSPECS": "1",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
}

HISTORICAL_SOURCE_COMMIT = (
    "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47"
)
CURRENT_ROOT_COMMIT = (
    "git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe"
)
HISTORICAL_PACK_IDS = (
    "audits/2026-05-24-whga",
    "audits/2026-07-02-whia",
    "audits/2026-07-03-wdgh",
    "audits/2026-07-04-wdcn",
    "audits/2026-07-05-wea",
    "research/2026-07-04-wer",
)
AUDIT_PACK_ID = "audits/2026-07-11-weia"
RESEARCH_PACK_ID = "research/2026-07-07-wer"
TRANSITION_ID = "ria-007-postflight-ledger"
TRANSITION_SUBJECT = "document-migration-evidence-ledger"
TRANSITION_MEMBER = "document-migration-evidence-ledger.md"
DATA_ASSET_FIELDS = frozenset(
    {"id", "repositoryEvidence", "refreshTrigger", "sources"}
)
SOURCE_RECORD_FIELDS = frozenset(
    {"url", "checkedOn", "adoptedScope", "rejectedScope"}
)
GENERATED_ASSET_FIELDS = frozenset(
    {
        "id",
        "generatorPath",
        "inputRoots",
        "outputPath",
        "checkCommand",
        "canonicalOwnerPath",
    }
)
GENERATOR_CHECK_COMMAND = "bash scripts/generate-llm-wiki-index.sh --check"
GENERATOR_EXECUTABLE = "/usr/bin/bash"
GENERATOR_RELATION_ID = "llm-wiki-index"
GENERATOR_PATH = Path("scripts/generate-llm-wiki-index.sh")
GENERATOR_INPUT_ROOTS = (
    Path("docs/90.references/llm-wiki/README.md"),
    Path("docs/00.agent-governance/README.md"),
    Path("docs/00.agent-governance/harness-catalog.md"),
    Path("docs/00.agent-governance/rules/document-stage-routing.md"),
    Path("docs/README.md"),
    Path("scripts/README.md"),
)
GENERATOR_OUTPUT_PATH = Path("docs/90.references/llm-wiki/wiki-index.md")
GENERATOR_CANONICAL_OWNER_PATH = Path("docs/90.references/llm-wiki/README.md")
GENERATOR_RELATIONS: Mapping[
    str,
    tuple[tuple[str, ...], str, Path, tuple[Path, ...], Path, Path],
] = MappingProxyType(
    {
        GENERATOR_CHECK_COMMAND: (
            (
                GENERATOR_EXECUTABLE,
                GENERATOR_PATH.as_posix(),
                "--check",
            ),
            GENERATOR_RELATION_ID,
            GENERATOR_PATH,
            GENERATOR_INPUT_ROOTS,
            GENERATOR_OUTPUT_PATH,
            GENERATOR_CANONICAL_OWNER_PATH,
        )
    }
)
GENERATOR_TIMEOUT_SECONDS = 10
GENERATOR_STDOUT_BYTES = MAX_METADATA_BYTES
GENERATOR_STDERR_BYTES = MAX_STDERR_BYTES
CLOSED_GENERATOR_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "PATH": "/usr/bin:/bin",
    "LANG": "C",
    "LC_ALL": "C",
    "TMPDIR": "/tmp",
}

RIA_RULE_IDS = frozenset(
    {
        "RIA-CONTRACT",
        "RIA-BOUNDARY",
        "RIA-SNAPSHOT",
        "RIA-OVERLAY",
        "RIA-TRANSITION",
        "RIA-SOURCE",
        "RIA-GENERATOR",
        "RIA-DUPLICATE",
    }
)


@dataclass(frozen=True, order=True)
class Finding:
    rule_id: str
    path: str
    message: str


class ContractError(ValueError):
    """A malformed or unsafe contract/configuration boundary."""

    def __init__(self, rule_id: str, path: str, message: str) -> None:
        self.finding = Finding(rule_id, path, message)
        super().__init__(f"{rule_id} {path}: {message}")


class _GitError(RuntimeError):
    """A value-free fixed Git runner failure."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class _GeneratorError(RuntimeError):
    """A value-free fixed generator process failure."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


GitRunner = Callable[[Path, tuple[str, ...], int], bytes]


@dataclass(frozen=True)
class Pack:
    pack_id: str
    allowed_states: tuple[str, ...]
    members: tuple[str, ...]

    @property
    def readme_path(self) -> Path:
        return Path("docs/90.references") / self.pack_id / "README.md"

    @property
    def member_paths(self) -> tuple[Path, ...]:
        root = Path("docs/90.references") / self.pack_id
        return tuple(root / member for member in self.members)


@dataclass(frozen=True)
class RegistryProjection:
    profile_id: str
    packs: tuple[Pack, ...]

    @property
    def pack_ids(self) -> tuple[str, ...]:
        return tuple(pack.pack_id for pack in self.packs)

    @property
    def paths(self) -> tuple[Path, ...]:
        paths: list[Path] = []
        for pack in self.packs:
            paths.append(pack.readme_path)
            paths.extend(pack.member_paths)
        return tuple(paths)


@dataclass(frozen=True)
class ValidationContext:
    proposed_registry: RegistryProjection
    proposed_bytes: Mapping[Path, bytes]
    baseline_registries: Mapping[str, RegistryProjection]
    baseline_bytes: Mapping[tuple[str, Path], bytes]
    baseline_oids: Mapping[str, str]
    proposed_commit_oid: str | None


@dataclass(frozen=True)
class GeneratedAssetRelation:
    relation_id: str
    generator_path: Path
    input_roots: tuple[Path, ...]
    output_path: Path
    check_command: str
    canonical_owner_path: Path


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _decode_json_bytes(payload: bytes, *, field: str) -> dict[str, object]:
    try:
        value = json.loads(
            payload.decode("utf-8", "strict"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ContractError(
            "RIA-CONTRACT", field, "JSON must be valid and unique-keyed"
        ) from error
    if not isinstance(value, dict):
        raise ContractError("RIA-CONTRACT", field, "JSON root must be an object")
    return value


def parse_repository_path(value: object, *, field: str) -> Path:
    """Return a canonical allowlisted repository-relative POSIX path."""

    if not isinstance(value, str) or not value:
        raise ContractError("RIA-BOUNDARY", field, "path must be a non-empty string")
    if REPOSITORY_PATH_PATTERN.fullmatch(value) is None:
        raise ContractError(
            "RIA-BOUNDARY", field, "path contains characters outside the closed grammar"
        )
    if "\\" in value or value.startswith("/"):
        raise ContractError("RIA-BOUNDARY", field, "path must be relative POSIX")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ContractError("RIA-BOUNDARY", field, "path contains a forbidden segment")
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or parsed.parts[0] not in ALLOWED_PATH_ROOTS:
        raise ContractError("RIA-BOUNDARY", field, "path is outside declared roots")
    if str(parsed) != value:
        raise ContractError("RIA-BOUNDARY", field, "path is not canonical")
    return Path(*parsed.parts)


def _path_under_root(root: Path, candidate: Path, *, field: str) -> Path:
    try:
        relative = candidate.relative_to(root) if candidate.is_absolute() else candidate
    except ValueError as error:
        raise ContractError(
            "RIA-BOUNDARY", field, "path is outside repository root"
        ) from error
    return parse_repository_path(relative.as_posix(), field=field)


def _read_regular_file(root: Path, relative: Path, *, field: str) -> bytes:
    """Read at most two MB without following any path component symlink."""

    try:
        root_stat = root.lstat()
    except OSError as error:
        raise ContractError(
            "RIA-BOUNDARY", field, "repository root is unavailable"
        ) from error
    if not stat.S_ISDIR(root_stat.st_mode) or stat.S_ISLNK(root_stat.st_mode):
        raise ContractError("RIA-BOUNDARY", field, "repository root is not a directory")
    try:
        directory_fd = os.open(
            root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        )
    except OSError as error:
        raise ContractError(
            "RIA-BOUNDARY", field, "repository root cannot be opened"
        ) from error
    try:
        for component in relative.parts[:-1]:
            component_stat = os.lstat(component, dir_fd=directory_fd)
            if not stat.S_ISDIR(component_stat.st_mode) or stat.S_ISLNK(
                component_stat.st_mode
            ):
                raise ContractError(
                    "RIA-BOUNDARY", field, "path contains a non-directory"
                )
            next_fd = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory_fd,
            )
            os.close(directory_fd)
            directory_fd = next_fd
        filename = relative.parts[-1]
        file_stat = os.lstat(filename, dir_fd=directory_fd)
        if not stat.S_ISREG(file_stat.st_mode) or stat.S_ISLNK(file_stat.st_mode):
            raise ContractError("RIA-BOUNDARY", field, "path is not a regular file")
        file_fd = os.open(
            filename,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
            dir_fd=directory_fd,
        )
        try:
            if not stat.S_ISREG(os.fstat(file_fd).st_mode):
                raise ContractError("RIA-BOUNDARY", field, "opened path is not regular")
            chunks: list[bytes] = []
            remaining = MAX_BLOB_BYTES
            while chunk := os.read(file_fd, min(65_536, remaining + 1)):
                chunks.append(chunk)
                remaining -= len(chunk)
                if remaining < 0:
                    raise ContractError("RIA-CONTRACT", field, "file exceeds input limit")
            return b"".join(chunks)
        finally:
            os.close(file_fd)
    except ContractError:
        raise
    except OSError as error:
        raise ContractError("RIA-BOUNDARY", field, "safe file read failed") from error
    finally:
        os.close(directory_fd)


def _load_json(root: Path, relative: Path, *, field: str) -> dict[str, object]:
    return _decode_json_bytes(_read_regular_file(root, relative, field=field), field=field)


def parse_git_sha1(value: object, *, field: str = "snapshotGuard.sourceCommit") -> str:
    """Return only a fully validated SHA-1 payload for fixed Git argv use."""

    if not isinstance(value, str):
        raise ContractError("RIA-SNAPSHOT", field, "must be encoded SHA-1")
    match = GIT_SHA1_PATTERN.fullmatch(value)
    if match is None:
        raise ContractError(
            "RIA-SNAPSHOT", field, "must be git-sha1:<40 lowercase hex>"
        )
    oid = match.group(1)
    if OID_PATTERN.fullmatch(oid) is None:
        raise ContractError("RIA-SNAPSHOT", field, "SHA-1 payload is invalid")
    return oid


def _safe_git_path(value: str) -> bool:
    try:
        parse_repository_path(value, field="git.path")
    except ContractError:
        return False
    return True


def _git_arguments_allowed(arguments: tuple[str, ...]) -> bool:
    if len(arguments) == 5 and arguments[:4] == (
        "ls-files",
        "-z",
        "--stage",
        "--",
    ):
        return _safe_git_path(arguments[4])
    if (
        len(arguments) == 3
        and arguments[:2] in {("cat-file", "-t"), ("cat-file", "-s")}
        and OID_PATTERN.fullmatch(arguments[2]) is not None
    ):
        return True
    if (
        len(arguments) == 3
        and arguments[:2] in {("cat-file", "commit"), ("cat-file", "blob")}
        and OID_PATTERN.fullmatch(arguments[2]) is not None
    ):
        return True
    if (
        len(arguments) == 6
        and arguments[:3] == ("ls-tree", "-z", "--full-tree")
        and OID_PATTERN.fullmatch(arguments[3]) is not None
        and arguments[4] == "--"
        and _safe_git_path(arguments[5])
    ):
        return True
    if (
        len(arguments) == 6
        and arguments[:3] == ("ls-tree", "-rz", "--full-tree")
        and OID_PATTERN.fullmatch(arguments[3]) is not None
        and arguments[4:] == ("--", DATA_ASSET_ROOT.as_posix())
    ):
        return True
    if arguments == ("rev-parse", "--verify", "HEAD"):
        return True
    if (
        len(arguments) == 9
        and arguments[:6]
        == (
            "diff-tree",
            "-r",
            "--no-commit-id",
            "--name-status",
            "-z",
            "--no-renames",
        )
        and OID_PATTERN.fullmatch(arguments[6]) is not None
        and OID_PATTERN.fullmatch(arguments[7]) is not None
        and arguments[8:] == ("--",)
    ):
        return True
    return bool(
        len(arguments) == 7
        and arguments[:5]
        == ("diff-index", "--cached", "--name-status", "-z", "--no-renames")
        and OID_PATTERN.fullmatch(arguments[5]) is not None
        and arguments[6:] == ("--",)
    )


def _run_git(root: Path, arguments: tuple[str, ...], stdout_limit: int = MAX_METADATA_BYTES) -> bytes:
    """Run one fixed Git query in a closed process environment."""

    if not _git_arguments_allowed(arguments):
        raise ContractError("RIA-BOUNDARY", ".git", "Git argv is outside the allowlist")
    try:
        process = subprocess.Popen(
            [GIT_EXECUTABLE, *arguments],
            cwd=root,
            env=CLOSED_GIT_ENVIRONMENT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
    except OSError as error:
        raise _GitError("Git executable is unavailable") from error
    assert process.stdout is not None and process.stderr is not None

    def stop() -> None:
        try:
            running = process.poll() is None
        except OSError:
            running = True
        if running:
            try:
                process.kill()
            except OSError:
                pass
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass
            try:
                process.wait(timeout=1)
            except (OSError, subprocess.TimeoutExpired):
                pass
        except OSError:
            pass

    deadline = time.monotonic() + GIT_TIMEOUT_SECONDS
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    limits = {"stdout": stdout_limit, "stderr": MAX_STDERR_BYTES}
    selector: selectors.BaseSelector | None = None
    try:
        selector = selectors.DefaultSelector()
        for name, stream in (("stdout", process.stdout), ("stderr", process.stderr)):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise _GitError("Git command timed out")
            try:
                events = selector.select(timeout=min(remaining, 0.1))
            except BlockingIOError:
                continue
            if not events:
                continue
            for key, _mask in events:
                name = key.data
                stream = key.fileobj
                try:
                    chunk = os.read(
                        stream.fileno(),
                        min(65_536, limits[name] - len(buffers[name]) + 1),
                    )
                except BlockingIOError:
                    continue
                except OSError as error:
                    raise _GitError("Git pipe read failed") from error
                if not chunk:
                    selector.unregister(stream)
                    continue
                buffers[name].extend(chunk)
                if len(buffers[name]) > limits[name]:
                    raise _GitError("Git output exceeded its bound")
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _GitError("Git command timed out")
        try:
            returncode = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as error:
            raise _GitError("Git command timed out") from error
    except _GitError:
        stop()
        raise
    except OSError as error:
        stop()
        raise _GitError("Git pipe operation failed") from error
    except BaseException:
        stop()
        raise
    finally:
        if selector is not None:
            try:
                selector.close()
            except OSError:
                pass
        for stream in (process.stdout, process.stderr):
            try:
                stream.close()
            except OSError:
                pass
    if returncode != 0:
        raise _GitError("Git command failed")
    return bytes(buffers["stdout"])


def _run_generator_check(root: Path, check_command: object) -> None:
    """Run the one mapped generator check with bounded, discarded output."""

    if not isinstance(check_command, str):
        raise _GeneratorError("generator command is not mapped")
    relation = GENERATOR_RELATIONS.get(check_command)
    if relation is None:
        raise _GeneratorError("generator command is not mapped")
    arguments = relation[0]
    try:
        process = subprocess.Popen(
            list(arguments),
            cwd=root.absolute(),
            env=CLOSED_GENERATOR_ENVIRONMENT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
    except OSError as error:
        raise _GeneratorError("generator executable is unavailable") from error
    assert process.stdout is not None and process.stderr is not None

    def stop() -> None:
        try:
            running = process.poll() is None
        except OSError:
            running = True
        if running:
            try:
                process.kill()
            except OSError:
                pass
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass
            try:
                process.wait(timeout=1)
            except (OSError, subprocess.TimeoutExpired):
                pass
        except OSError:
            pass

    deadline = time.monotonic() + GENERATOR_TIMEOUT_SECONDS
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    limits = {
        "stdout": GENERATOR_STDOUT_BYTES,
        "stderr": GENERATOR_STDERR_BYTES,
    }
    selector: selectors.BaseSelector | None = None
    try:
        selector = selectors.DefaultSelector()
        for name, stream in (("stdout", process.stdout), ("stderr", process.stderr)):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise _GeneratorError("generator command timed out")
            try:
                events = selector.select(timeout=min(remaining, 0.1))
            except BlockingIOError:
                continue
            if not events:
                continue
            for key, _mask in events:
                name = key.data
                stream = key.fileobj
                try:
                    chunk = os.read(
                        stream.fileno(),
                        min(65_536, limits[name] - len(buffers[name]) + 1),
                    )
                except BlockingIOError:
                    continue
                except OSError as error:
                    raise _GeneratorError("generator pipe read failed") from error
                if not chunk:
                    selector.unregister(stream)
                    continue
                buffers[name].extend(chunk)
                if len(buffers[name]) > limits[name]:
                    raise _GeneratorError("generator output exceeded its bound")
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _GeneratorError("generator command timed out")
        try:
            returncode = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as error:
            raise _GeneratorError("generator command timed out") from error
    except _GeneratorError:
        stop()
        raise
    except OSError as error:
        stop()
        raise _GeneratorError("generator pipe operation failed") from error
    except BaseException:
        stop()
        raise
    finally:
        if selector is not None:
            try:
                selector.close()
            except OSError:
                pass
        for stream in (process.stdout, process.stderr):
            try:
                stream.close()
            except OSError:
                pass
    if returncode != 0:
        raise _GeneratorError("generator command failed")


def _git(
    root: Path,
    arguments: tuple[str, ...],
    *,
    stdout_limit: int = MAX_METADATA_BYTES,
    runner: GitRunner | None = None,
) -> bytes:
    return (runner or _run_git)(root, arguments, stdout_limit)


def _require_commit(root: Path, oid: str, runner: GitRunner | None = None) -> None:
    if _git(root, ("cat-file", "-t", oid), runner=runner) != b"commit\n":
        raise _GitError("object is not a commit")


def _parse_index_record(payload: bytes, path: Path) -> str:
    records = payload.split(b"\0")
    if not records or records[-1] != b"":
        raise _GitError("index record is not NUL terminated")
    records.pop()
    if len(records) != 1:
        raise _GitError("path does not have exactly one index record")
    match = re.fullmatch(
        rb"([0-9]{6}) ([0-9a-f]{40}) ([0-3])\t([^\0]+)", records[0]
    )
    if match is None:
        raise _GitError("index record is malformed")
    mode, oid, stage, returned_path = match.groups()
    if mode not in {b"100644", b"100755"} or stage != b"0":
        raise _GitError("index record is not a stage-zero regular file")
    try:
        decoded_path = returned_path.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise _GitError("index path is invalid") from error
    if decoded_path != path.as_posix():
        raise _GitError("index path does not match the request")
    return oid.decode("ascii")


def _parse_tree_record(payload: bytes, path: Path) -> str:
    records = payload.split(b"\0")
    if not records or records[-1] != b"":
        raise _GitError("tree record is not NUL terminated")
    records.pop()
    if len(records) != 1:
        raise _GitError("path does not have exactly one tree record")
    match = re.fullmatch(
        rb"([0-9]{6}) ([a-z]+) ([0-9a-f]{40})\t([^\0]+)", records[0]
    )
    if match is None:
        raise _GitError("tree record is malformed")
    mode, object_type, oid, returned_path = match.groups()
    if mode not in {b"100644", b"100755"} or object_type != b"blob":
        raise _GitError("tree record is not a regular blob")
    try:
        decoded_path = returned_path.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise _GitError("tree path is invalid") from error
    if decoded_path != path.as_posix():
        raise _GitError("tree path does not match the request")
    return oid.decode("ascii")


def _parse_canonical_size(payload: bytes) -> int:
    if re.fullmatch(rb"(?:0|[1-9][0-9]*)\n", payload) is None:
        raise _GitError("blob size is not canonical decimal")
    size = int(payload[:-1])
    if size > MAX_BLOB_BYTES:
        raise _GitError("blob exceeds the maximum size")
    return size


def _read_blob(root: Path, oid: str, runner: GitRunner | None = None) -> bytes:
    if OID_PATTERN.fullmatch(oid) is None:
        raise _GitError("blob identity is malformed")
    if _git(root, ("cat-file", "-t", oid), runner=runner) != b"blob\n":
        raise _GitError("object is not a blob")
    size = _parse_canonical_size(
        _git(root, ("cat-file", "-s", oid), runner=runner)
    )
    payload = _git(
        root,
        ("cat-file", "blob", oid),
        stdout_limit=size,
        runner=runner,
    )
    if len(payload) != size:
        raise _GitError("blob length does not match its declared size")
    return payload


def _read_index_path(root: Path, path: Path, runner: GitRunner | None = None) -> bytes:
    oid = _parse_index_record(
        _git(
            root,
            ("ls-files", "-z", "--stage", "--", path.as_posix()),
            runner=runner,
        ),
        path,
    )
    return _read_blob(root, oid, runner)


def read_proposed_regular_file(
    root: Path, path: Path, runner: GitRunner | None = None
) -> bytes:
    """Read one exact stage-zero blob and require equal no-follow worktree bytes."""

    indexed = _read_index_path(root, path, runner)
    worktree = _read_regular_file(root, path, field=path.as_posix())
    if indexed != worktree:
        raise ContractError(
            "RIA-BOUNDARY", path.as_posix(), "index and worktree bytes differ"
        )
    return indexed


def _read_commit_path(
    root: Path, commit_oid: str, path: Path, runner: GitRunner | None = None
) -> bytes:
    _require_commit(root, commit_oid, runner)
    oid = _parse_tree_record(
        _git(
            root,
            (
                "ls-tree",
                "-z",
                "--full-tree",
                commit_oid,
                "--",
                path.as_posix(),
            ),
            runner=runner,
        ),
        path,
    )
    return _read_blob(root, oid, runner)


def _commit_parents(root: Path, oid: str, runner: GitRunner | None = None) -> tuple[str, ...]:
    _require_commit(root, oid, runner)
    payload = _git(root, ("cat-file", "commit", oid), runner=runner)
    if len(payload) > MAX_METADATA_BYTES or b"\0" in payload:
        raise _GitError("commit object is malformed")
    lines = payload.splitlines()
    if not lines or re.fullmatch(rb"tree [0-9a-f]{40}", lines[0]) is None:
        raise _GitError("commit object has no canonical tree header")
    parents: list[str] = []
    for line in lines[1:]:
        if line == b"":
            break
        if line.startswith(b"parent "):
            if re.fullmatch(rb"parent [0-9a-f]{40}", line) is None:
                raise _GitError("commit parent is malformed")
            parents.append(line.removeprefix(b"parent ").decode("ascii"))
    return tuple(parents)


def _validate_schema_document(
    contract: dict[str, object], schema: dict[str, object]
) -> None:
    if contract.get("$schema") != "./reference-information-architecture.schema.json":
        raise ContractError("RIA-CONTRACT", "$schema", "schema reference is not canonical")
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(contract),
            key=lambda error: list(error.absolute_path),
        )
    except Exception as error:
        raise ContractError("RIA-CONTRACT", "$schema", "schema is invalid") from error
    if errors:
        location = ".".join(str(part) for part in errors[0].absolute_path) or "$"
        raise ContractError(
            "RIA-CONTRACT", location, "contract does not match closed schema"
        )


def _validate_schema(
    root: Path,
    contract: dict[str, object],
    contract_path: Path,
    runner: GitRunner | None = None,
) -> None:
    schema_path = contract_path.with_name(
        "reference-information-architecture.schema.json"
    )
    try:
        payload = read_proposed_regular_file(root, schema_path, runner)
    except (ContractError, _GitError) as error:
        raise ContractError(
            "RIA-CONTRACT", "$schema", "proposed schema authority is unavailable"
        ) from error
    schema = _decode_json_bytes(payload, field="$schema")
    _validate_schema_document(contract, schema)


def _validate_schema_at_commit(
    root: Path,
    commit_oid: str,
    contract: dict[str, object],
    contract_path: Path,
    runner: GitRunner | None,
) -> None:
    if contract.get("$schema") != "./reference-information-architecture.schema.json":
        raise ContractError("RIA-CONTRACT", "$schema", "schema reference is not canonical")
    schema_path = contract_path.with_name(
        "reference-information-architecture.schema.json"
    )
    try:
        payload = _read_commit_path(root, commit_oid, schema_path, runner)
    except _GitError as error:
        raise ContractError(
            "RIA-CONTRACT", "$schema", "named schema authority is unavailable"
        ) from error
    schema = _decode_json_bytes(payload, field="$schema")
    _validate_schema_document(contract, schema)


def _unique_strings(value: object, *, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ContractError("RIA-CONTRACT", field, "must be an array of strings")
    if len(set(value)) != len(value):
        raise ContractError("RIA-CONTRACT", field, "contains duplicate values")
    return value


def _validate_path_fields(contract: Mapping[str, object]) -> None:
    parse_repository_path(contract.get("currentPackRegistry"), field="currentPackRegistry")
    projections = contract.get("mutableIndexProjections")
    if isinstance(projections, list):
        for index, projection in enumerate(projections):
            if not isinstance(projection, Mapping):
                continue
            parse_repository_path(
                projection.get("path"), field=f"mutableIndexProjections[{index}].path"
            )
            replacement = projection.get("navigationReplacement")
            if isinstance(replacement, Mapping):
                parse_repository_path(
                    replacement.get("destination"),
                    field=(
                        f"mutableIndexProjections[{index}]"
                        ".navigationReplacement.destination"
                    ),
                )
    data_assets = contract.get("dataAssets")
    if isinstance(data_assets, list):
        for index, asset in enumerate(data_assets):
            if not isinstance(asset, Mapping):
                continue
            evidence = asset.get("repositoryEvidence")
            if isinstance(evidence, list):
                for evidence_index, path in enumerate(evidence):
                    parse_repository_path(
                        path,
                        field=f"dataAssets[{index}].repositoryEvidence[{evidence_index}]",
                    )
    generated_assets = contract.get("generatedAssets")
    if isinstance(generated_assets, list):
        for index, asset in enumerate(generated_assets):
            if not isinstance(asset, Mapping):
                continue
            for key in ("generatorPath", "outputPath", "canonicalOwnerPath"):
                if key in asset:
                    parse_repository_path(asset.get(key), field=f"generatedAssets[{index}].{key}")
            roots = asset.get("inputRoots")
            if isinstance(roots, list):
                for root_index, path in enumerate(roots):
                    parse_repository_path(
                        path, field=f"generatedAssets[{index}].inputRoots[{root_index}]"
                    )
    duplicate_rules = contract.get("duplicateRules")
    if not isinstance(duplicate_rules, Mapping):
        return
    roots = duplicate_rules.get("canonicalOwnerRoots")
    if isinstance(roots, list):
        for index, path in enumerate(roots):
            parse_repository_path(path, field=f"duplicateRules.canonicalOwnerRoots[{index}]")
    exceptions = duplicate_rules.get("structuralExceptions")
    if isinstance(exceptions, list):
        for index, exception in enumerate(exceptions):
            if not isinstance(exception, Mapping):
                continue
            for key in ("canonicalOwnerPath", "referencePath"):
                if key in exception:
                    parse_repository_path(
                        exception.get(key),
                        field=f"duplicateRules.structuralExceptions[{index}].{key}",
                    )


_PROJECTION_ALLOWLIST: dict[str, dict[str, object]] = {
    "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md": {
        "completeBody": True,
    },
    "docs/90.references/audits/README.md": {
        "table": {
            "section": "Audit Pack Registry",
            "columns": ["Pack role", "Successor / resolution"],
        },
    },
    "docs/90.references/research/README.md": {
        "table": {"section": "Research Pack Index", "columns": ["Status"]},
    },
    "docs/90.references/audits/2026-07-11-weia/README.md": {
        "table": {
            "section": "Report Index",
            "columns": ["Lifecycle", "Actionable disposition"],
        },
    },
    "docs/90.references/research/2026-07-07-wer/README.md": {
        "table": {"section": "Report Index", "columns": ["Lifecycle"]},
        "navigationReplacement": {
            "visibleText": "../README.md",
            "destination": "docs/90.references/research/README.md",
        },
    },
}


def _validate_contract_boundaries(contract: dict[str, object]) -> None:
    registry_path = parse_repository_path(
        contract.get("currentPackRegistry"), field="currentPackRegistry"
    )
    if registry_path != REGISTRY_PATH:
        raise ContractError("RIA-BOUNDARY", "currentPackRegistry", "registry path is fixed")
    if contract.get("schemaVersion") != 2:
        raise ContractError("RIA-CONTRACT", "schemaVersion", "schema version must be 2")
    guard = contract.get("snapshotGuard")
    if not isinstance(guard, Mapping):
        raise ContractError("RIA-CONTRACT", "snapshotGuard", "must be an object")
    source = guard.get("sourceCommit")
    parse_git_sha1(source)
    if source != HISTORICAL_SOURCE_COMMIT:
        raise ContractError("RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "historical source is fixed")
    historical = _unique_strings(
        guard.get("historicalPackIds"), field="snapshotGuard.historicalPackIds"
    )
    if tuple(historical) != HISTORICAL_PACK_IDS:
        raise ContractError(
            "RIA-SNAPSHOT", "snapshotGuard.historicalPackIds", "historical pack set is fixed"
        )
    baselines = contract.get("currentPackBaselines")
    if not isinstance(baselines, Mapping):
        raise ContractError("RIA-CONTRACT", "currentPackBaselines", "must be an object")
    for key, value in baselines.items():
        if not isinstance(key, str) or PACK_ID_PATTERN.fullmatch(key) is None:
            raise ContractError("RIA-CONTRACT", "currentPackBaselines", "pack key is invalid")
        parse_git_sha1(value, field=f"currentPackBaselines.{key}")
    for collection in ("baselineTransitions", "baselineSettlements"):
        records = contract.get(collection)
        if not isinstance(records, list):
            raise ContractError("RIA-CONTRACT", collection, "must be an array")
        for index, record in enumerate(records):
            if isinstance(record, Mapping):
                parse_git_sha1(
                    record.get("fromCommit"), field=f"{collection}[{index}].fromCommit"
                )
                if collection == "baselineSettlements":
                    parse_git_sha1(
                        record.get("transitionCommit"),
                        field=f"{collection}[{index}].transitionCommit",
                    )
    projections = contract.get("mutableIndexProjections")
    if not isinstance(projections, list):
        raise ContractError("RIA-CONTRACT", "mutableIndexProjections", "must be an array")
    seen: set[str] = set()
    for index, projection in enumerate(projections):
        if not isinstance(projection, Mapping):
            raise ContractError("RIA-CONTRACT", f"mutableIndexProjections[{index}]", "must be an object")
        path = projection.get("path")
        if not isinstance(path, str) or path in seen:
            raise ContractError("RIA-CONTRACT", "mutableIndexProjections", "contains duplicate paths")
        seen.add(path)
        expected = _PROJECTION_ALLOWLIST.get(path)
        if expected is None or dict(projection) != {"path": path, **expected}:
            raise ContractError("RIA-OVERLAY", path, "projection is outside the closed allowlist")
    generated = contract.get("generatedAssets")
    if isinstance(generated, list):
        outputs: set[object] = set()
        for asset in generated:
            if not isinstance(asset, Mapping):
                continue
            output = asset.get("outputPath")
            if output in outputs:
                raise ContractError("RIA-CONTRACT", "generatedAssets", "contains duplicate output paths")
            outputs.add(output)


def load_contract(
    root: Path,
    contract_path: Path,
    *,
    runner: GitRunner | None = None,
) -> dict[str, object]:
    """Load a contract whose schema has exact proposed index authority."""

    root = root.absolute()
    relative = _path_under_root(root, contract_path, field="contract")
    contract = _load_json(root, relative, field="contract")
    _validate_path_fields(contract)
    _validate_schema(root, contract, relative, runner)
    _validate_contract_boundaries(contract)
    return contract


def _load_contract_for_self_test(
    root: Path, contract_path: Path
) -> dict[str, object]:
    """Load isolated fixture files without claiming proposed Git authority."""

    root = root.absolute()
    relative = _path_under_root(root, contract_path, field="contract")
    contract = _load_json(root, relative, field="contract")
    _validate_path_fields(contract)
    schema = _load_json(
        root,
        relative.with_name("reference-information-architecture.schema.json"),
        field="$schema",
    )
    _validate_schema_document(contract, schema)
    _validate_contract_boundaries(contract)
    return contract


def load_contract_at_commit(
    root: Path,
    encoded_commit: object,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    *,
    runner: GitRunner | None = None,
) -> dict[str, object]:
    """Load the exact contract blob from one anchored literal commit."""

    root = root.absolute()
    relative = _path_under_root(root, contract_path, field="contract")
    oid = parse_git_sha1(encoded_commit, field="--commit")
    try:
        payload = _read_commit_path(root, oid, relative, runner)
    except _GitError as error:
        raise ContractError("RIA-TRANSITION", relative.as_posix(), error.message) from error
    contract = _decode_json_bytes(payload, field="contract")
    _validate_path_fields(contract)
    _validate_schema_at_commit(root, oid, contract, relative, runner)
    _validate_contract_boundaries(contract)
    return contract


def _strict_date(value: object) -> date | None:
    if not isinstance(value, str) or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.isoformat() == value else None


def _closed_https_url(value: object) -> bool:
    if (
        not isinstance(value, str)
        or not value.isascii()
        or re.search(r"[\\\x00-\x20\x7f-\x9f]", value) is not None
    ):
        return False
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return False
    del port
    return bool(
        parsed.scheme == "https"
        and value.startswith("https://")
        and parsed.netloc
        and parsed.hostname
        and parsed.username is None
        and parsed.password is None
    )


def _closed_single_line_text(value: object) -> bool:
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    return all(
        not (
            ord(character) < 0x20
            or 0x7F <= ord(character) <= 0x9F
            or character in {"\u2028", "\u2029"}
        )
        for character in value
    )


def _closed_nonempty_strings(value: object) -> bool:
    return bool(
        isinstance(value, list)
        and value
        and all(_closed_single_line_text(item) for item in value)
        and len(set(value)) == len(value)
    )


def _inventory_path(payload: bytes, *, field: str) -> Path:
    try:
        decoded = payload.decode("utf-8", "strict")
        path = parse_repository_path(decoded, field=field)
    except (UnicodeDecodeError, ContractError) as error:
        raise _GitError("data asset inventory path is invalid") from error
    if DATA_ASSET_ROOT not in path.parents:
        raise _GitError("data asset inventory escaped its fixed root")
    return path


def _parse_index_listing(payload: bytes) -> tuple[Path, ...]:
    records = payload.split(b"\0")
    if not records or records[-1] != b"":
        raise _GitError("index listing is not NUL terminated")
    paths: list[Path] = []
    seen: set[Path] = set()
    for record in records[:-1]:
        match = re.fullmatch(
            rb"([0-9]{6}) ([0-9a-f]{40}) ([0-3])\t([^\0]+)", record
        )
        if match is None:
            raise _GitError("index listing is malformed")
        mode, _oid, stage, returned_path = match.groups()
        if mode not in {b"100644", b"100755"} or stage != b"0":
            raise _GitError("index listing includes nonregular or unmerged data")
        path = _inventory_path(returned_path, field="dataAssets.repositoryEvidence")
        if path in seen:
            raise _GitError("index listing includes a duplicate path")
        seen.add(path)
        paths.append(path)
    return tuple(sorted(paths))


def _parse_tree_listing(payload: bytes) -> tuple[Path, ...]:
    records = payload.split(b"\0")
    if not records or records[-1] != b"":
        raise _GitError("tree listing is not NUL terminated")
    paths: list[Path] = []
    seen: set[Path] = set()
    for record in records[:-1]:
        match = re.fullmatch(
            rb"([0-9]{6}) ([a-z]+) ([0-9a-f]{40})\t([^\0]+)", record
        )
        if match is None:
            raise _GitError("tree listing is malformed")
        mode, object_type, _oid, returned_path = match.groups()
        if mode not in {b"100644", b"100755"} or object_type != b"blob":
            raise _GitError("tree listing includes nonregular data")
        path = _inventory_path(returned_path, field="dataAssets.repositoryEvidence")
        if path in seen:
            raise _GitError("tree listing includes a duplicate path")
        seen.add(path)
        paths.append(path)
    return tuple(sorted(paths))


def _tracked_data_asset_paths(
    root: Path,
    *,
    commit_oid: str | None,
    runner: GitRunner | None,
) -> set[Path]:
    if commit_oid is None:
        paths = _parse_index_listing(
            _git(
                root,
                ("ls-files", "-z", "--stage", "--", DATA_ASSET_ROOT.as_posix()),
                runner=runner,
            )
        )
    else:
        _require_commit(root, commit_oid, runner)
        paths = _parse_tree_listing(
            _git(
                root,
                (
                    "ls-tree",
                    "-rz",
                    "--full-tree",
                    commit_oid,
                    "--",
                    DATA_ASSET_ROOT.as_posix(),
                ),
                runner=runner,
            )
        )
    return {path for path in paths if path != DATA_ASSET_README}


def validate_data_assets(
    root: Path,
    contract: Mapping[str, object],
    *,
    proposed_commit: object | None = None,
    runner: GitRunner | None = None,
) -> list[Finding]:
    """Validate the closed, offline source ledger and exact repo evidence."""

    findings: list[Finding] = []
    cutoff = _strict_date(contract.get("evidenceCutoff"))
    if cutoff is None:
        findings.append(
            Finding("RIA-SOURCE", "evidenceCutoff", "cutoff is not a strict calendar date")
        )

    assets = contract.get("dataAssets")
    if not isinstance(assets, list):
        return sorted(
            {
                *findings,
                Finding("RIA-SOURCE", "dataAssets", "source ledger must be an array"),
            }
        )

    commit_oid: str | None = None
    if proposed_commit is not None:
        try:
            commit_oid = parse_git_sha1(proposed_commit, field="--commit")
        except ContractError:
            return sorted(
                {
                    *findings,
                    Finding("RIA-SOURCE", "--commit", "source evidence authority is unavailable"),
                }
            )

    try:
        expected_evidence = _tracked_data_asset_paths(
            root.absolute(), commit_oid=commit_oid, runner=runner
        )
    except (ContractError, _GitError):
        return sorted(
            {
                *findings,
                Finding(
                    "RIA-SOURCE",
                    DATA_ASSET_ROOT.as_posix(),
                    "tracked data asset inventory is unavailable",
                ),
            }
        )

    seen_ids: set[str] = set()
    seen_evidence: set[Path] = set()
    for asset_index, asset in enumerate(assets):
        asset_field = f"dataAssets[{asset_index}]"
        if not isinstance(asset, Mapping):
            findings.append(
                Finding("RIA-SOURCE", asset_field, "asset record must be an object")
            )
            continue
        if set(asset) != DATA_ASSET_FIELDS:
            findings.append(
                Finding("RIA-SOURCE", asset_field, "asset record fields are not closed")
            )

        asset_id = asset.get("id")
        if (
            not isinstance(asset_id, str)
            or re.fullmatch(r"[a-z][a-z0-9-]*", asset_id) is None
            or asset_id in seen_ids
        ):
            findings.append(
                Finding(
                    "RIA-SOURCE",
                    f"{asset_field}.id",
                    "asset identity is invalid or duplicated",
                )
            )
        else:
            seen_ids.add(asset_id)

        trigger = asset.get("refreshTrigger")
        if not _closed_single_line_text(trigger):
            findings.append(
                Finding(
                    "RIA-SOURCE",
                    f"{asset_field}.refreshTrigger",
                    "refresh trigger must be closed single-line text",
                )
            )

        evidence = asset.get("repositoryEvidence")
        if not isinstance(evidence, list) or not evidence:
            findings.append(
                Finding(
                    "RIA-SOURCE",
                    f"{asset_field}.repositoryEvidence",
                    "repository evidence must be non-empty",
                )
            )
        else:
            if len(evidence) != 1:
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        f"{asset_field}.repositoryEvidence",
                        "asset must own exactly one repository evidence path",
                    )
                )
            local_evidence: set[Path] = set()
            for evidence_index, value in enumerate(evidence):
                field = f"{asset_field}.repositoryEvidence[{evidence_index}]"
                try:
                    path = parse_repository_path(value, field=field)
                except ContractError:
                    findings.append(
                        Finding("RIA-SOURCE", field, "repository evidence path is invalid")
                    )
                    continue
                if path in local_evidence or path in seen_evidence:
                    findings.append(
                        Finding("RIA-SOURCE", field, "repository evidence path is duplicated")
                    )
                    continue
                local_evidence.add(path)
                seen_evidence.add(path)
                try:
                    if commit_oid is None:
                        read_proposed_regular_file(root.absolute(), path, runner)
                    else:
                        _read_commit_path(root.absolute(), commit_oid, path, runner)
                except (ContractError, _GitError):
                    findings.append(
                        Finding(
                            "RIA-SOURCE",
                            path.as_posix(),
                            "tracked repository evidence is unavailable",
                        )
                    )

        sources = asset.get("sources")
        if not isinstance(sources, list) or not sources:
            findings.append(
                Finding("RIA-SOURCE", f"{asset_field}.sources", "source records must be non-empty")
            )
            continue
        seen_sources: set[str] = set()
        for source_index, source in enumerate(sources):
            source_field = f"{asset_field}.sources[{source_index}]"
            if not isinstance(source, Mapping):
                findings.append(
                    Finding("RIA-SOURCE", source_field, "source record must be an object")
                )
                continue
            if set(source) != SOURCE_RECORD_FIELDS:
                findings.append(
                    Finding("RIA-SOURCE", source_field, "source record fields are not closed")
                )
            try:
                identity = json.dumps(
                    dict(source), sort_keys=True, separators=(",", ":"), ensure_ascii=True
                )
            except (TypeError, ValueError):
                identity = ""
            if not identity or identity in seen_sources:
                findings.append(
                    Finding("RIA-SOURCE", source_field, "source record is invalid or duplicated")
                )
            else:
                seen_sources.add(identity)

            if not _closed_https_url(source.get("url")):
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        f"{source_field}.url",
                        "source URL must use closed HTTPS syntax",
                    )
                )
            checked_on = _strict_date(source.get("checkedOn"))
            if checked_on is None:
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        f"{source_field}.checkedOn",
                        "source date is not a strict calendar date",
                    )
                )
            elif cutoff is not None and checked_on > cutoff:
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        f"{source_field}.checkedOn",
                        "source date exceeds the evidence cutoff",
                    )
                )
            adopted = source.get("adoptedScope")
            rejected = source.get("rejectedScope")
            if not _closed_nonempty_strings(adopted):
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        f"{source_field}.adoptedScope",
                        "adopted scope must be closed non-empty text",
                    )
                )
            if not _closed_nonempty_strings(rejected):
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        f"{source_field}.rejectedScope",
                        "rejected scope must be closed non-empty text",
                    )
                )
            if (
                isinstance(adopted, list)
                and isinstance(rejected, list)
                and set(item for item in adopted if isinstance(item, str))
                & set(item for item in rejected if isinstance(item, str))
            ):
                findings.append(
                    Finding("RIA-SOURCE", source_field, "adopted and rejected scopes overlap")
                )
    if seen_evidence != expected_evidence:
        findings.append(
            Finding(
                "RIA-SOURCE",
                DATA_ASSET_ROOT.as_posix(),
                "source ledger and tracked data asset inventory differ",
            )
        )
    return sorted(set(findings))


_MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]\r\n]*\]\(([^)\r\n]+)\)")


def _resolve_markdown_destination(output_path: Path, raw: str) -> Path | None:
    destination = raw.strip()
    if destination.startswith("<"):
        closing = destination.find(">")
        if closing < 0:
            return None
        destination = destination[1:closing]
    else:
        destination = destination.split(maxsplit=1)[0]
    if not destination or destination.startswith(("/", "#", "//")):
        return None
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
        return None
    components = list(output_path.parent.parts)
    for component in parsed.path.split("/"):
        if component in {"", "."}:
            continue
        if component == "..":
            if not components:
                return None
            components.pop()
            continue
        if re.fullmatch(r"[A-Za-z0-9._-]+", component) is None:
            return None
        components.append(component)
    if not components:
        return None
    candidate = Path(*components)
    try:
        return parse_repository_path(candidate.as_posix(), field="generated.ownerLink")
    except ContractError:
        return None


def _output_links_to_owner(
    output_path: Path, output: bytes, canonical_owner_path: Path
) -> bool:
    try:
        text = output.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return False
    return any(
        _resolve_markdown_destination(output_path, match.group(1))
        == canonical_owner_path
        for match in _MARKDOWN_LINK_PATTERN.finditer(text)
    )


def validate_generated_assets(
    root: Path,
    contract: Mapping[str, object],
    *,
    proposed_commit: object | None = None,
    runner: GitRunner | None = None,
) -> list[Finding]:
    """Validate closed generator ownership and current-tree zero drift.

    Named-commit mode proves only the declared relation's committed regular
    blobs and owner link. It deliberately does not attribute a current
    worktree process result to that historical commit.
    """

    findings: list[Finding] = []
    assets = contract.get("generatedAssets")
    if not isinstance(assets, list) or not assets:
        return [
            Finding(
                "RIA-GENERATOR",
                "generatedAssets",
                "generator relation must be a non-empty array",
            )
        ]

    relations: list[GeneratedAssetRelation] = []
    seen_ids: set[str] = set()
    seen_outputs: set[Path] = set()
    for index, asset in enumerate(assets):
        field = f"generatedAssets[{index}]"
        if not isinstance(asset, Mapping):
            findings.append(
                Finding("RIA-GENERATOR", field, "generator relation must be an object")
            )
            continue
        if set(asset) != GENERATED_ASSET_FIELDS:
            findings.append(
                Finding("RIA-GENERATOR", field, "generator relation fields are not closed")
            )

        relation_id = asset.get("id")
        if (
            not isinstance(relation_id, str)
            or re.fullmatch(r"[a-z][a-z0-9-]*", relation_id) is None
            or relation_id in seen_ids
        ):
            findings.append(
                Finding(
                    "RIA-GENERATOR",
                    f"{field}.id",
                    "generator identity is invalid or duplicated",
                )
            )
        else:
            seen_ids.add(relation_id)

        parsed_paths: dict[str, Path] = {}
        for key in ("generatorPath", "outputPath", "canonicalOwnerPath"):
            try:
                parsed_paths[key] = parse_repository_path(
                    asset.get(key), field=f"{field}.{key}"
                )
            except ContractError:
                findings.append(
                    Finding(
                        "RIA-GENERATOR",
                        f"{field}.{key}",
                        "generator relation path is invalid",
                    )
                )

        raw_inputs = asset.get("inputRoots")
        inputs: list[Path] = []
        if not isinstance(raw_inputs, list) or not raw_inputs:
            findings.append(
                Finding(
                    "RIA-GENERATOR",
                    f"{field}.inputRoots",
                    "generator inputs must be a non-empty array",
                )
            )
        else:
            for input_index, value in enumerate(raw_inputs):
                input_field = f"{field}.inputRoots[{input_index}]"
                try:
                    inputs.append(parse_repository_path(value, field=input_field))
                except ContractError:
                    findings.append(
                        Finding(
                            "RIA-GENERATOR",
                            input_field,
                            "generator input path is invalid",
                        )
                    )
            if len(set(inputs)) != len(inputs):
                findings.append(
                    Finding(
                        "RIA-GENERATOR",
                        f"{field}.inputRoots",
                        "generator input paths are duplicated",
                    )
                )

        check_command = asset.get("checkCommand")
        mapped_relation = (
            GENERATOR_RELATIONS.get(check_command)
            if isinstance(check_command, str)
            else None
        )
        if mapped_relation is None:
            findings.append(
                Finding(
                    "RIA-GENERATOR",
                    f"{field}.checkCommand",
                    "generator command is outside the fixed mapping",
                )
            )

        generator_path = parsed_paths.get("generatorPath")
        output_path = parsed_paths.get("outputPath")
        canonical_owner_path = parsed_paths.get("canonicalOwnerPath")
        if generator_path is not None and output_path is not None:
            if generator_path == output_path:
                findings.append(
                    Finding(
                        "RIA-GENERATOR",
                        output_path.as_posix(),
                        "generator and output identities overlap",
                    )
                )
            if output_path in seen_outputs:
                findings.append(
                    Finding(
                        "RIA-GENERATOR",
                        output_path.as_posix(),
                        "generated output has multiple owners",
                    )
                )
            seen_outputs.add(output_path)
            if output_path in inputs or output_path == canonical_owner_path:
                findings.append(
                    Finding(
                        "RIA-GENERATOR",
                        output_path.as_posix(),
                        "generated output overlaps its owner or inputs",
                    )
                )
            if mapped_relation is not None and (
                relation_id != mapped_relation[1]
                or generator_path != mapped_relation[2]
                or tuple(inputs) != mapped_relation[3]
                or output_path != mapped_relation[4]
                or canonical_owner_path != mapped_relation[5]
            ):
                findings.append(
                    Finding(
                        "RIA-GENERATOR",
                        output_path.as_posix(),
                        "generator relation does not match the fixed command",
                    )
                )

        if (
            isinstance(relation_id, str)
            and re.fullmatch(r"[a-z][a-z0-9-]*", relation_id) is not None
            and generator_path is not None
            and output_path is not None
            and canonical_owner_path is not None
            and inputs
            and len(set(inputs)) == len(inputs)
            and isinstance(check_command, str)
            and mapped_relation is not None
        ):
            relations.append(
                GeneratedAssetRelation(
                    relation_id,
                    generator_path,
                    tuple(inputs),
                    output_path,
                    check_command,
                    canonical_owner_path,
                )
            )

    if findings:
        return sorted(set(findings))

    commit_oid: str | None = None
    if proposed_commit is not None:
        try:
            commit_oid = parse_git_sha1(proposed_commit, field="--commit")
        except ContractError:
            return [
                Finding(
                    "RIA-GENERATOR",
                    "--commit",
                    "generator relation authority is unavailable",
                )
            ]

    root = root.absolute()
    authoritative: dict[Path, bytes] = {}
    paths = {
        path
        for relation in relations
        for path in (
            relation.generator_path,
            *relation.input_roots,
            relation.output_path,
            relation.canonical_owner_path,
        )
    }
    for path in sorted(paths):
        try:
            authoritative[path] = (
                read_proposed_regular_file(root, path, runner)
                if commit_oid is None
                else _read_commit_path(root, commit_oid, path, runner)
            )
        except (ContractError, _GitError):
            findings.append(
                Finding(
                    "RIA-GENERATOR",
                    path.as_posix(),
                    "tracked generator relation path is unavailable",
                )
            )

    if findings:
        return sorted(set(findings))
    for relation in relations:
        if not _output_links_to_owner(
            relation.output_path,
            authoritative[relation.output_path],
            relation.canonical_owner_path,
        ):
            findings.append(
                Finding(
                    "RIA-GENERATOR",
                    relation.output_path.as_posix(),
                    "generated output has no current canonical-owner link",
                )
            )
    if findings or commit_oid is not None:
        return sorted(set(findings))

    for relation in relations:
        try:
            _run_generator_check(root, relation.check_command)
        except _GeneratorError:
            findings.append(
                Finding(
                    "RIA-GENERATOR",
                    relation.output_path.as_posix(),
                    "generated output check failed",
                )
            )
    return sorted(set(findings))


def _registry_projection(value: Mapping[str, object]) -> RegistryProjection:
    root = value.get("referenceCurrentPacks")
    if not isinstance(root, Mapping):
        raise ContractError("RIA-CONTRACT", REGISTRY_PATH.as_posix(), "Current pack registry is malformed")
    profile = root.get("profileId")
    records = root.get("packs")
    if not isinstance(profile, str) or not isinstance(records, list):
        raise ContractError("RIA-CONTRACT", REGISTRY_PATH.as_posix(), "Current pack registry is malformed")
    packs: list[Pack] = []
    pack_ids: set[str] = set()
    all_paths: set[Path] = set()
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ContractError("RIA-CONTRACT", REGISTRY_PATH.as_posix(), "registry pack is malformed")
        pack_id = record.get("id")
        members = record.get("members")
        states = record.get("allowedStates")
        if (
            not isinstance(pack_id, str)
            or PACK_ID_PATTERN.fullmatch(pack_id) is None
            or not isinstance(members, list)
            or not isinstance(states, list)
            or any(not isinstance(item, str) or not item for item in members + states)
            or len(members) != len(set(members))
            or len(states) != len(set(states))
            or pack_id in pack_ids
        ):
            raise ContractError("RIA-CONTRACT", f"currentPackRegistry.packs[{index}]", "registry pack is malformed")
        pack_ids.add(pack_id)
        pack = Pack(pack_id, tuple(states), tuple(members))
        for path in (pack.readme_path, *pack.member_paths):
            parse_repository_path(path.as_posix(), field="currentPackRegistry.members")
            if path in all_paths:
                raise ContractError("RIA-CONTRACT", REGISTRY_PATH.as_posix(), "Current path is duplicated")
            all_paths.add(path)
        packs.append(pack)
    return RegistryProjection(profile, tuple(packs))


def _encoded_baselines(contract: Mapping[str, object]) -> dict[str, str]:
    raw = contract.get("currentPackBaselines")
    if not isinstance(raw, Mapping):
        raise ContractError("RIA-CONTRACT", "currentPackBaselines", "must be an object")
    result: dict[str, str] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ContractError("RIA-CONTRACT", "currentPackBaselines", "map is malformed")
        result[key] = value
    return result


def _proposed_path(
    root: Path, path: Path, proposed_oid: str | None, runner: GitRunner | None
) -> bytes:
    if proposed_oid is not None:
        return _read_commit_path(root, proposed_oid, path, runner)
    return read_proposed_regular_file(root, path, runner)


def _build_context(
    root: Path,
    contract: Mapping[str, object],
    *,
    proposed_oid: str | None = None,
    runner: GitRunner | None = None,
) -> ValidationContext:
    root = root.absolute()
    proposed_registry_bytes = _proposed_path(root, REGISTRY_PATH, proposed_oid, runner)
    proposed_registry = _registry_projection(
        _decode_json_bytes(proposed_registry_bytes, field=REGISTRY_PATH.as_posix())
    )
    baselines = _encoded_baselines(contract)
    if tuple(baselines) != proposed_registry.pack_ids:
        raise ContractError(
            "RIA-TRANSITION",
            "currentPackBaselines",
            "baseline keys must exactly equal ordered Current pack IDs",
        )
    baseline_registries: dict[str, RegistryProjection] = {}
    baseline_bytes: dict[tuple[str, Path], bytes] = {}
    baseline_oids: dict[str, str] = {}
    for encoded in dict.fromkeys(baselines.values()):
        oid = parse_git_sha1(encoded, field="currentPackBaselines")
        baseline_oids[encoded] = oid
        registry_bytes = _read_commit_path(root, oid, REGISTRY_PATH, runner)
        registry = _registry_projection(
            _decode_json_bytes(registry_bytes, field=REGISTRY_PATH.as_posix())
        )
        if registry != proposed_registry:
            raise ContractError(
                "RIA-TRANSITION",
                REGISTRY_PATH.as_posix(),
                "baseline and proposed Current registry projections differ",
            )
        baseline_registries[encoded] = registry
    proposed_bytes: dict[Path, bytes] = {}
    for pack in proposed_registry.packs:
        encoded = baselines[pack.pack_id]
        oid = baseline_oids[encoded]
        for path in (pack.readme_path, *pack.member_paths):
            baseline_bytes[(encoded, path)] = _read_commit_path(root, oid, path, runner)
            proposed_bytes[path] = _proposed_path(root, path, proposed_oid, runner)
    return ValidationContext(
        proposed_registry,
        proposed_bytes,
        baseline_registries,
        baseline_bytes,
        baseline_oids,
        proposed_oid,
    )


def validate_proposed_registry_authority(
    root: Path,
    contract: Mapping[str, object],
    *,
    proposed_commit: object | None = None,
    runner: GitRunner | None = None,
) -> list[Finding]:
    try:
        oid = (
            parse_git_sha1(proposed_commit, field="--commit")
            if proposed_commit is not None
            else None
        )
        _build_context(root, contract, proposed_oid=oid, runner=runner)
    except (ContractError, _GitError) as error:
        if isinstance(error, ContractError):
            return [error.finding]
        return [Finding("RIA-BOUNDARY", REGISTRY_PATH.as_posix(), error.message)]
    return []


def _links_in_section(text: str, heading: str, pack_root: Path) -> tuple[Path, ...]:
    heading_match = re.search(
        rf"(?m)^##[ \t]+{re.escape(heading)}[ \t]*$", text
    )
    if heading_match is None:
        raise _GitError("pack index section is missing")
    tail = text[heading_match.end() :]
    next_heading = re.search(r"(?m)^##[ \t]+", tail)
    section = tail[: next_heading.start()] if next_heading else tail
    paths: list[Path] = []
    for destination in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)\)", section):
        if not destination.endswith(".md") or destination.startswith(("/", "../")):
            continue
        resolved = pack_root / destination.removeprefix("./")
        parse_repository_path(resolved.as_posix(), field="snapshotGuard.members")
        if resolved.parent != pack_root or resolved.name == "README.md":
            raise _GitError("pack index member is outside the pack")
        if resolved not in paths:
            paths.append(resolved)
    if not paths:
        raise _GitError("pack index has no report members")
    return tuple(paths)


def validate_snapshot_guards(
    root: Path,
    contract: Mapping[str, object],
    *,
    proposed_commit: object | None = None,
    runner: GitRunner | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    guard = contract.get("snapshotGuard")
    if not isinstance(guard, Mapping):
        return [Finding("RIA-SNAPSHOT", "snapshotGuard", "snapshot guard is malformed")]
    try:
        source_oid = parse_git_sha1(guard.get("sourceCommit"))
        _require_commit(root.absolute(), source_oid, runner)
        proposed_oid = (
            parse_git_sha1(proposed_commit, field="--commit")
            if proposed_commit is not None
            else None
        )
    except (ContractError, _GitError):
        return [Finding("RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "source commit is unavailable")]
    ids = guard.get("historicalPackIds")
    if not isinstance(ids, list):
        return [Finding("RIA-SNAPSHOT", "snapshotGuard.historicalPackIds", "historical pack set is malformed")]
    for pack_id in ids:
        if not isinstance(pack_id, str):
            findings.append(Finding("RIA-SNAPSHOT", "snapshotGuard.historicalPackIds", "historical pack ID is invalid"))
            continue
        pack_root = Path("docs/90.references") / pack_id
        readme = pack_root / "README.md"
        try:
            baseline_readme = _read_commit_path(root.absolute(), source_oid, readme, runner)
            members = _links_in_section(
                baseline_readme.decode("utf-8", "strict"), "Report Index", pack_root
            )
        except (ContractError, _GitError, UnicodeDecodeError):
            findings.append(Finding("RIA-SNAPSHOT", readme.as_posix(), "historical pack index is unavailable"))
            continue
        for path in (readme, *members):
            try:
                baseline = (
                    baseline_readme
                    if path == readme
                    else _read_commit_path(root.absolute(), source_oid, path, runner)
                )
                proposed = _proposed_path(root.absolute(), path, proposed_oid, runner)
            except (ContractError, _GitError):
                findings.append(Finding("RIA-SNAPSHOT", path.as_posix(), "protected snapshot is unavailable"))
                continue
            if hashlib.sha256(proposed).digest() != hashlib.sha256(baseline).digest():
                findings.append(Finding("RIA-SNAPSHOT", path.as_posix(), "protected snapshot bytes differ"))
    return sorted(set(findings))


def _table_mask(text: str, section: str, columns: Sequence[str]) -> str:
    match = re.search(rf"(?m)^###[#]?[ \t]+{re.escape(section)}[ \t]*$|^##[ \t]+{re.escape(section)}[ \t]*$", text)
    if match is None:
        raise _GitError("declared table section is missing")
    lines = text.splitlines(keepends=True)
    offset = 0
    heading_index = -1
    for index, line in enumerate(lines):
        if offset <= match.start() < offset + len(line):
            heading_index = index
            break
        offset += len(line)
    section_end = next(
        (
            index
            for index in range(heading_index + 1, len(lines))
            if re.match(r"^#{1,6}[ \t]+", lines[index]) is not None
        ),
        len(lines),
    )
    table_index = next(
        (
            index
            for index in range(heading_index + 1, section_end)
            if lines[index].lstrip().startswith("|")
        ),
        -1,
    )
    if table_index < 0 or table_index + 1 >= len(lines):
        raise _GitError("declared table is missing")

    def table_parts(line: str) -> tuple[list[str], str]:
        newline = (
            "\r\n"
            if line.endswith("\r\n")
            else "\n"
            if line.endswith("\n")
            else ""
        )
        body = line[: -len(newline)] if newline else line
        parts = body.split("|")
        if len(parts) < 3 or parts[0].strip() or parts[-1].strip():
            raise _GitError("declared table row is malformed")
        return parts, newline

    def cells(line: str) -> list[str]:
        parts, _newline = table_parts(line)
        return [cell.strip() for cell in parts[1:-1]]

    header = cells(lines[table_index])
    delimiter = cells(lines[table_index + 1])
    if len(delimiter) != len(header) or any(re.fullmatch(r":?-{3,}:?", item) is None for item in delimiter):
        raise _GitError("declared table delimiter is malformed")
    indexes: list[int] = []
    for column in columns:
        if header.count(column) != 1:
            raise _GitError("declared table column is missing or duplicated")
        indexes.append(header.index(column))
    masked = list(lines)
    for index in range(table_index + 2, len(lines)):
        if not lines[index].lstrip().startswith("|"):
            break
        parts, newline = table_parts(lines[index])
        row = [cell.strip() for cell in parts[1:-1]]
        if len(row) != len(header):
            raise _GitError("declared table row width differs")
        for column_index in indexes:
            parts[column_index + 1] = f"<RIA-CELL-{column_index}>"
        masked[index] = "|".join(parts) + newline
    return "".join(masked)


def _resolved_link(path: Path, destination: str) -> Path:
    candidate = path.parent / destination
    normalized = PurePosixPath(candidate.as_posix())
    parts: list[str] = []
    for part in normalized.parts:
        if part == "..":
            if not parts:
                raise _GitError("navigation target escapes the repository")
            parts.pop()
        elif part not in {"", "."}:
            parts.append(part)
    return parse_repository_path("/".join(parts), field="navigationReplacement.destination")


def _navigation_mask(text: str, path: Path, visible: str, destination: str) -> str:
    pattern = re.compile(rf"(?<!!)\[{re.escape(visible)}\]\(([^)\s]+)\)")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise _GitError("navigation link identity is not unique")
    resolved = _resolved_link(path, matches[0].group(1))
    declared = Path(destination)
    if resolved != declared:
        raise _GitError("navigation destination is not the declared target")
    return pattern.sub(f"[{visible}](<RIA-NAVIGATION>)", text, count=1)


def _projection_mask(payload: bytes, path: Path, projection: Mapping[str, object]) -> bytes:
    try:
        text = payload.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise _GitError("projected Markdown is not UTF-8") from error
    if projection.get("completeBody") is True:
        lines = payload.splitlines(keepends=True)
        if not lines or lines[0] not in {b"---\n", b"---\r\n"}:
            raise _GitError("projected Markdown frontmatter is malformed")
        closing = next(
            (
                index
                for index, line in enumerate(lines[1:], start=1)
                if line in {b"---\n", b"---\r\n"}
            ),
            None,
        )
        if closing is None:
            raise _GitError("projected Markdown frontmatter is malformed")
        return b"".join(lines[: closing + 1]) + b"<RIA-COMPLETE-BODY>"
    table = projection.get("table")
    if isinstance(table, Mapping):
        section = table.get("section")
        columns = table.get("columns")
        if not isinstance(section, str) or not isinstance(columns, list):
            raise _GitError("table projection is malformed")
        text = _table_mask(text, section, columns)
    navigation = projection.get("navigationReplacement")
    if isinstance(navigation, Mapping):
        visible = navigation.get("visibleText")
        destination = navigation.get("destination")
        if not isinstance(visible, str) or not isinstance(destination, str):
            raise _GitError("navigation projection is malformed")
        text = _navigation_mask(text, path, visible, destination)
    return text.encode("utf-8")


def _transition_record(contract: Mapping[str, object]) -> Mapping[str, object] | None:
    records = contract.get("baselineTransitions")
    if isinstance(records, list) and len(records) == 1 and isinstance(records[0], Mapping):
        return records[0]
    return None


def _projection_map(contract: Mapping[str, object]) -> dict[Path, Mapping[str, object]]:
    projections = contract.get("mutableIndexProjections")
    if not isinstance(projections, list):
        return {}
    return {
        Path(str(projection["path"])): projection
        for projection in projections
        if isinstance(projection, Mapping) and "path" in projection
    }


def validate_overlay_guards(
    root: Path,
    contract: Mapping[str, object],
    *,
    proposed_commit: object | None = None,
    runner: GitRunner | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        proposed_oid = (
            parse_git_sha1(proposed_commit, field="--commit")
            if proposed_commit is not None
            else None
        )
        context = _build_context(root, contract, proposed_oid=proposed_oid, runner=runner)
    except (ContractError, _GitError) as error:
        if isinstance(error, ContractError):
            return [Finding("RIA-OVERLAY", error.finding.path, "Current authority is unavailable")]
        return [Finding("RIA-OVERLAY", REGISTRY_PATH.as_posix(), "Current authority is unavailable")]
    baselines = _encoded_baselines(contract)
    projections = _projection_map(contract)
    transition = _transition_record(contract)
    transition_path = (
        Path("docs/90.references/research") / "2026-07-07-wer" / TRANSITION_MEMBER
        if transition is not None
        else None
    )
    for pack in context.proposed_registry.packs:
        encoded = baselines[pack.pack_id]
        for path in (pack.readme_path, *pack.member_paths):
            baseline = context.baseline_bytes[(encoded, path)]
            proposed = context.proposed_bytes[path]
            projection = projections.get(path)
            if path == transition_path:
                digest = transition.get("targetSha256") if transition else None
                length = transition.get("targetByteLength") if transition else None
                if (
                    not isinstance(digest, str)
                    or SHA256_PATTERN.fullmatch(digest) is None
                    or length != len(proposed)
                    or hashlib.sha256(proposed).hexdigest() != digest
                    or proposed == baseline
                ):
                    findings.append(Finding("RIA-OVERLAY", path.as_posix(), "transition target bytes differ"))
                continue
            try:
                if projection is not None:
                    baseline = _projection_mask(baseline, path, projection)
                    proposed = _projection_mask(proposed, path, projection)
            except _GitError:
                findings.append(Finding("RIA-OVERLAY", path.as_posix(), "declared projection is malformed"))
                continue
            if hashlib.sha256(proposed).digest() != hashlib.sha256(baseline).digest():
                findings.append(Finding("RIA-OVERLAY", path.as_posix(), "protected Current bytes differ"))
    current_paths = set(context.proposed_registry.paths)
    for path, projection in projections.items():
        if path in current_paths:
            continue
        if path.parts[:3] == ("docs", "90.references", "audits"):
            pack_id = AUDIT_PACK_ID
        elif path.parts[:3] == ("docs", "90.references", "research"):
            pack_id = RESEARCH_PACK_ID
        else:
            findings.append(Finding("RIA-OVERLAY", path.as_posix(), "projection path has no Current pack"))
            continue
        encoded = baselines[pack_id]
        oid = context.baseline_oids[encoded]
        try:
            baseline = _read_commit_path(root.absolute(), oid, path, runner)
            proposed = _proposed_path(root.absolute(), path, proposed_oid, runner)
            baseline = _projection_mask(baseline, path, projection)
            proposed = _projection_mask(proposed, path, projection)
        except (ContractError, _GitError):
            findings.append(Finding("RIA-OVERLAY", path.as_posix(), "projected index is unavailable"))
            continue
        if hashlib.sha256(proposed).digest() != hashlib.sha256(baseline).digest():
            findings.append(Finding("RIA-OVERLAY", path.as_posix(), "protected index bytes differ"))
    return sorted(set(findings))


def _record_matches_transition(
    record: Mapping[str, object], *, settlement: bool = False
) -> bool:
    keys = {
        "id",
        "packId",
        "fromCommit",
        "subject",
        "targetSha256",
        "targetByteLength",
        "reason",
    }
    if settlement:
        keys.add("transitionCommit")
    return (
        set(record) == keys
        and record.get("id") == TRANSITION_ID
        and record.get("packId") == RESEARCH_PACK_ID
        and record.get("fromCommit") == CURRENT_ROOT_COMMIT
        and record.get("subject") == TRANSITION_SUBJECT
        and isinstance(record.get("targetSha256"), str)
        and SHA256_PATTERN.fullmatch(str(record.get("targetSha256"))) is not None
        and isinstance(record.get("targetByteLength"), int)
        and not isinstance(record.get("targetByteLength"), bool)
        and 1 <= int(record.get("targetByteLength", 0)) <= MAX_BLOB_BYTES
        and isinstance(record.get("reason"), str)
        and bool(str(record.get("reason")).strip())
        and len(str(record.get("reason"))) <= 512
    )


def _fsm_state(contract: Mapping[str, object]) -> tuple[str | None, Finding | None]:
    try:
        baselines = _encoded_baselines(contract)
    except ContractError:
        return None, Finding("RIA-TRANSITION", "currentPackBaselines", "baseline map is malformed")
    transitions = contract.get("baselineTransitions")
    settlements = contract.get("baselineSettlements")
    if (
        tuple(baselines) != (AUDIT_PACK_ID, RESEARCH_PACK_ID)
        or baselines.get(AUDIT_PACK_ID) != CURRENT_ROOT_COMMIT
        or not isinstance(transitions, list)
        or not isinstance(settlements, list)
        or len(transitions) > 1
        or len(settlements) > 1
    ):
        return None, Finding("RIA-TRANSITION", "currentPackBaselines", "baseline state is outside the closed FSM")
    research = baselines[RESEARCH_PACK_ID]
    if research == CURRENT_ROOT_COMMIT and not transitions and not settlements:
        return "root", None
    if research == CURRENT_ROOT_COMMIT and len(transitions) == 1 and not settlements:
        record = transitions[0]
        if isinstance(record, Mapping) and _record_matches_transition(record):
            return "open", None
        return None, Finding("RIA-TRANSITION", "baselineTransitions", "open transition is malformed")
    if not transitions and len(settlements) == 1:
        record = settlements[0]
        if (
            isinstance(record, Mapping)
            and _record_matches_transition(record, settlement=True)
            and record.get("transitionCommit") == research
            and research != CURRENT_ROOT_COMMIT
        ):
            return "settled", None
    return None, Finding("RIA-TRANSITION", "currentPackBaselines", "baseline state is outside the closed FSM")


def _matching_open_contract(
    settlement: Mapping[str, object],
    open_contract: Mapping[str, object],
    settled_contract: Mapping[str, object],
) -> bool:
    transitions = open_contract.get("baselineTransitions")
    settlements = open_contract.get("baselineSettlements")
    baselines = open_contract.get("currentPackBaselines")
    if (
        not isinstance(transitions, list)
        or len(transitions) != 1
        or not isinstance(transitions[0], Mapping)
        or settlements != []
        or not isinstance(baselines, Mapping)
        or baselines.get(AUDIT_PACK_ID) != CURRENT_ROOT_COMMIT
        or baselines.get(RESEARCH_PACK_ID) != CURRENT_ROOT_COMMIT
    ):
        return False
    expected = {key: value for key, value in settlement.items() if key != "transitionCommit"}
    if dict(transitions[0]) != expected:
        return False
    expected_settled = dict(open_contract)
    expected_settled["currentPackBaselines"] = {
        **baselines,
        RESEARCH_PACK_ID: settlement["transitionCommit"],
    }
    expected_settled["baselineTransitions"] = []
    expected_settled["baselineSettlements"] = [dict(settlement)]
    return expected_settled == dict(settled_contract)


def _settlement_proof(
    root: Path,
    contract: Mapping[str, object],
    context: ValidationContext,
    runner: GitRunner | None,
) -> list[Finding]:
    settlement = contract["baselineSettlements"][0]
    assert isinstance(settlement, Mapping)
    transition_commit = settlement.get("transitionCommit")
    try:
        c2_oid = parse_git_sha1(transition_commit, field="baselineSettlements.transitionCommit")
        c2_contract = _decode_json_bytes(
            _read_commit_path(root, c2_oid, DEFAULT_CONTRACT_PATH, runner),
            field=DEFAULT_CONTRACT_PATH.as_posix(),
        )
        _validate_path_fields(c2_contract)
        _validate_schema_at_commit(
            root, c2_oid, c2_contract, DEFAULT_CONTRACT_PATH, runner
        )
        _validate_contract_boundaries(c2_contract)
        if not _matching_open_contract(settlement, c2_contract, contract):
            raise _GitError("transition contract does not match settlement")
        c2_registry_bytes = _read_commit_path(root, c2_oid, REGISTRY_PATH, runner)
        c2_registry = _registry_projection(
            _decode_json_bytes(c2_registry_bytes, field=REGISTRY_PATH.as_posix())
        )
        root_registry = context.baseline_registries[CURRENT_ROOT_COMMIT]
        if c2_registry != root_registry or c2_registry != context.proposed_registry:
            raise _GitError("transition registry differs")
        target_path = Path("docs/90.references") / RESEARCH_PACK_ID / TRANSITION_MEMBER
        target = _read_commit_path(root, c2_oid, target_path, runner)
        if (
            len(target) != settlement.get("targetByteLength")
            or hashlib.sha256(target).hexdigest() != settlement.get("targetSha256")
        ):
            raise _GitError("transition target proof differs")
        root_oid = parse_git_sha1(
            CURRENT_ROOT_COMMIT, field="currentPackBaselines.root"
        )
        root_target = _read_commit_path(root, root_oid, target_path, runner)
        if target == root_target:
            raise _GitError("transition target is unchanged")
        for pack in root_registry.packs:
            for path in (pack.readme_path, *pack.member_paths):
                if path == target_path:
                    continue
                root_bytes = _read_commit_path(root, root_oid, path, runner)
                c2_bytes = _read_commit_path(root, c2_oid, path, runner)
                if c2_bytes != root_bytes:
                    raise _GitError("transition changed a non-target path")
    except (ContractError, _GitError, KeyError):
        return [Finding("RIA-TRANSITION", "baselineSettlements", "settlement proof chain is invalid")]
    return []


def _parse_diff_index(payload: bytes) -> tuple[tuple[str, str], ...]:
    parts = payload.split(b"\0")
    if not parts or parts[-1] != b"":
        raise _GitError("diff-index output is not NUL terminated")
    parts.pop()
    if len(parts) % 2:
        raise _GitError("diff-index output is malformed")
    rows: list[tuple[str, str]] = []
    for index in range(0, len(parts), 2):
        try:
            status = parts[index].decode("ascii")
            path = parts[index + 1].decode("utf-8", "strict")
        except UnicodeDecodeError as error:
            raise _GitError("diff-index output is malformed") from error
        rows.append((status, path))
    return tuple(rows)


def validate_staged_settlement_lineage(
    root: Path,
    contract: Mapping[str, object],
    *,
    runner: GitRunner | None = None,
) -> list[Finding]:
    state, finding = _fsm_state(contract)
    if finding is not None or state != "settled":
        return [Finding("RIA-TRANSITION", "baselineSettlements", "staged mode requires settled state")]
    settlement = contract["baselineSettlements"][0]
    assert isinstance(settlement, Mapping)
    try:
        c2_oid = parse_git_sha1(settlement.get("transitionCommit"), field="baselineSettlements.transitionCommit")
        head = _git(root, ("rev-parse", "--verify", "HEAD"), runner=runner)
        if re.fullmatch(rb"[0-9a-f]{40}\n", head) is None:
            raise _GitError("HEAD output is malformed")
        head_oid = head[:-1].decode("ascii")
        _require_commit(root, head_oid, runner)
        if head_oid != c2_oid:
            raise _GitError("HEAD is not settlement C2")
        rows = _parse_diff_index(
            _git(
                root,
                (
                    "diff-index",
                    "--cached",
                    "--name-status",
                    "-z",
                    "--no-renames",
                    c2_oid,
                    "--",
                ),
                runner=runner,
            )
        )
        if rows != (("M", DEFAULT_CONTRACT_PATH.as_posix()),):
            raise _GitError("staged settlement changes paths outside the contract")
    except (ContractError, _GitError):
        return [Finding("RIA-TRANSITION", DEFAULT_CONTRACT_PATH.as_posix(), "staged settlement lineage is invalid")]
    return []


def validate_explicit_commit_lineage(
    root: Path,
    contract: Mapping[str, object],
    encoded_commit: object,
    *,
    runner: GitRunner | None = None,
) -> list[Finding]:
    state, finding = _fsm_state(contract)
    if finding is not None or state != "settled":
        return [Finding("RIA-TRANSITION", "baselineSettlements", "explicit mode requires settled state")]
    settlement = contract["baselineSettlements"][0]
    assert isinstance(settlement, Mapping)
    try:
        c3_oid = parse_git_sha1(encoded_commit, field="--commit")
        c2_oid = parse_git_sha1(settlement.get("transitionCommit"), field="baselineSettlements.transitionCommit")
        if _commit_parents(root, c3_oid, runner) != (c2_oid,):
            raise _GitError("C3 does not have exactly parent C2")
        rows = _parse_diff_index(
            _git(
                root,
                (
                    "diff-tree",
                    "-r",
                    "--no-commit-id",
                    "--name-status",
                    "-z",
                    "--no-renames",
                    c2_oid,
                    c3_oid,
                    "--",
                ),
                runner=runner,
            )
        )
        if rows != (("M", DEFAULT_CONTRACT_PATH.as_posix()),):
            raise _GitError("C3 changes paths outside the contract")
    except (ContractError, _GitError):
        return [Finding("RIA-TRANSITION", "--commit", "explicit settlement lineage is invalid")]
    return []


def validate_baseline_transitions(
    root: Path,
    contract: Mapping[str, object],
    *,
    staged: bool = False,
    commit: object | None = None,
    require_settled_baselines: bool = False,
    runner: GitRunner | None = None,
) -> list[Finding]:
    if staged and commit is not None:
        return [Finding("RIA-TRANSITION", "evidenceMode", "evidence modes are mutually exclusive")]
    state, finding = _fsm_state(contract)
    if finding is not None:
        return [finding]
    if state == "open" and require_settled_baselines:
        return [Finding("RIA-TRANSITION", "baselineTransitions", "an open transition is not terminal")]
    if staged and state != "settled":
        return [Finding("RIA-TRANSITION", "baselineSettlements", "staged mode requires settled state")]
    if commit is not None and state != "settled":
        return [Finding("RIA-TRANSITION", "baselineSettlements", "explicit mode requires settled state")]
    if state == "root":
        return []
    try:
        proposed_oid = parse_git_sha1(commit, field="--commit") if commit is not None else None
        context = _build_context(root, contract, proposed_oid=proposed_oid, runner=runner)
    except (ContractError, _GitError):
        return [Finding("RIA-TRANSITION", REGISTRY_PATH.as_posix(), "transition authority is unavailable")]
    findings: list[Finding] = []
    if state == "open":
        transition = contract["baselineTransitions"][0]
        assert isinstance(transition, Mapping)
        research = next(
            (pack for pack in context.proposed_registry.packs if pack.pack_id == RESEARCH_PACK_ID),
            None,
        )
        if research is None or TRANSITION_MEMBER not in research.members:
            findings.append(Finding("RIA-TRANSITION", "baselineTransitions", "transition subject is not a Current member"))
        else:
            target_path = Path("docs/90.references") / RESEARCH_PACK_ID / TRANSITION_MEMBER
            target = context.proposed_bytes[target_path]
            if (
                len(target) != transition.get("targetByteLength")
                or hashlib.sha256(target).hexdigest() != transition.get("targetSha256")
                or target
                == context.baseline_bytes[(CURRENT_ROOT_COMMIT, target_path)]
            ):
                findings.append(Finding("RIA-TRANSITION", target_path.as_posix(), "transition target bytes differ"))
    elif state == "settled":
        findings.extend(_settlement_proof(root.absolute(), contract, context, runner))
        if staged:
            findings.extend(validate_staged_settlement_lineage(root.absolute(), contract, runner=runner))
        if commit is not None:
            findings.extend(validate_explicit_commit_lineage(root.absolute(), contract, commit, runner=runner))
    return sorted(set(findings))


def _contract_authority_finding(
    root: Path,
    contract: Mapping[str, object],
    *,
    commit: object | None,
    runner: GitRunner | None,
) -> Finding | None:
    try:
        if commit is None:
            payload = read_proposed_regular_file(root, DEFAULT_CONTRACT_PATH, runner)
        else:
            oid = parse_git_sha1(commit, field="--commit")
            payload = _read_commit_path(root, oid, DEFAULT_CONTRACT_PATH, runner)
        authoritative = _decode_json_bytes(payload, field=DEFAULT_CONTRACT_PATH.as_posix())
        if authoritative != dict(contract):
            raise _GitError("contract mapping differs from proposed authority")
    except (ContractError, _GitError):
        return Finding("RIA-BOUNDARY", DEFAULT_CONTRACT_PATH.as_posix(), "proposed contract authority is unavailable")
    return None


def validate_reference_architecture(
    root: Path,
    contract: Mapping[str, object],
    *,
    staged: bool = False,
    commit: object | None = None,
    require_settled_baselines: bool = False,
    runner: GitRunner | None = None,
) -> list[Finding]:
    """Validate schema-v2 snapshots, Current overlays, and baseline lineage."""

    if staged and commit is not None:
        return [Finding("RIA-TRANSITION", "evidenceMode", "evidence modes are mutually exclusive")]
    authority = _contract_authority_finding(root.absolute(), contract, commit=commit, runner=runner)
    if authority is not None:
        return [authority]
    findings = [
        *validate_snapshot_guards(root, contract, proposed_commit=commit, runner=runner),
        *validate_overlay_guards(root, contract, proposed_commit=commit, runner=runner),
        *validate_data_assets(
            root, contract, proposed_commit=commit, runner=runner
        ),
        *validate_generated_assets(
            root, contract, proposed_commit=commit, runner=runner
        ),
        *validate_baseline_transitions(
            root,
            contract,
            staged=staged,
            commit=commit,
            require_settled_baselines=require_settled_baselines,
            runner=runner,
        ),
    ]
    return sorted(set(findings))


def _canonical_schema_bytes() -> bytes:
    repository_root = Path(__file__).resolve().parents[1]
    return _read_regular_file(repository_root, CANONICAL_SCHEMA_PATH, field="self-test.schema")


def _self_test_contract() -> dict[str, object]:
    return {
        "$schema": "./reference-information-architecture.schema.json",
        "schemaVersion": 2,
        "evidenceCutoff": "2026-07-22",
        "currentPackRegistry": REGISTRY_PATH.as_posix(),
        "snapshotGuard": {
            "sourceCommit": HISTORICAL_SOURCE_COMMIT,
            "historicalPackIds": list(HISTORICAL_PACK_IDS),
        },
        "currentPackBaselines": {
            AUDIT_PACK_ID: CURRENT_ROOT_COMMIT,
            RESEARCH_PACK_ID: CURRENT_ROOT_COMMIT,
        },
        "baselineTransitions": [],
        "baselineSettlements": [],
        "mutableIndexProjections": [],
        "dataAssets": [],
        "generatedAssets": [],
        "duplicateRules": {
            "canonicalOwnerRoots": ["docs/00.agent-governance"],
            "minimumParagraphCharacters": 1,
            "structuralExceptions": [],
        },
    }


def run_self_test() -> None:
    """Exercise schema, SHA parsing, and hostile record parsers in isolation."""

    accepted = HISTORICAL_SOURCE_COMMIT
    rejected = (
        accepted.removeprefix("git-sha1:"),
        "git-sha1:",
        "git-sha1:" + accepted,
        accepted.upper(),
        "git-sha1:" + "z" * 40,
        "git-sha1:" + "a" * 64,
        accepted + " trailing",
        " " + accepted,
        accepted + " ",
    )
    if parse_git_sha1(accepted) != accepted.removeprefix("git-sha1:"):
        raise AssertionError("accepted SHA-1 was rejected")
    for value in rejected:
        try:
            parse_git_sha1(value)
        except ContractError:
            continue
        raise AssertionError("malformed SHA-1 was accepted")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        contract_path = root / DEFAULT_CONTRACT_PATH
        schema_path = contract_path.with_name(CANONICAL_SCHEMA_PATH.name)
        contract_path.parent.mkdir(parents=True)
        schema_path.write_bytes(_canonical_schema_bytes())
        contract = _self_test_contract()
        contract_path.write_text(json.dumps(contract), encoding="utf-8")
        loaded = _load_contract_for_self_test(root, contract_path)
        if loaded != contract:
            raise AssertionError("closed v2 contract did not round trip")
        for mutation in (
            {**contract, "schemaVersion": 1},
            {**contract, "unknown": True},
            {
                **contract,
                "snapshotGuard": {
                    **contract["snapshotGuard"],
                    "currentPackIds": [AUDIT_PACK_ID],
                },
            },
            {**contract, "currentMemberPaths": []},
        ):
            contract_path.write_text(json.dumps(mutation), encoding="utf-8")
            try:
                _load_contract_for_self_test(root, contract_path)
            except ContractError:
                continue
            raise AssertionError("closed schema mutation was accepted")
    path = Path("docs/example.md")
    bad_tree = (
        b"100644 blob " + b"a" * 40 + b"\tdocs/other.md\0",
        b"120000 blob " + b"a" * 40 + b"\tdocs/example.md\0",
        b"100644 tree " + b"a" * 40 + b"\tdocs/example.md\0",
        b"100644 blob " + b"a" * 40 + b"\tdocs/example.md\0extra\0",
    )
    for payload in bad_tree:
        try:
            _parse_tree_record(payload, path)
        except _GitError:
            continue
        raise AssertionError("hostile tree record was accepted")
    for payload in (b"01\n", b"+1\n", b"-1\n", b"2000001\n", b"1", b"1\nextra"):
        try:
            _parse_canonical_size(payload)
        except _GitError:
            continue
        raise AssertionError("hostile blob size was accepted")
