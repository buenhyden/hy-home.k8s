"""Fail-closed Reference Information Architecture validation primitives."""

from __future__ import annotations

from array import array
from collections import Counter
from dataclasses import dataclass
from datetime import date
from html import unescape
from html.entities import html5
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
import unicodedata
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator


DEFAULT_CONTRACT_PATH = Path(
    "docs/90.references/data/reference-information-architecture.json"
)
AGENT_LEGACY_CUTOVER_PATH = Path(
    "docs/00.agent-governance/contracts/agent-legacy-cutover.json"
)
AGENT_LEGACY_CUTOVER_SCHEMA_PATH = Path(
    "docs/00.agent-governance/contracts/agent-legacy-cutover.schema.json"
)
AGENT_LEGACY_CUTOVER_SHA256 = "2f12a5a509b9f0af007caa8febd5e0f83818e0d6085009661a99b29318334b47"  # pragma: allowlist secret
AGENT_LEGACY_CUTOVER_SCHEMA_SHA256 = "4e0b7e55ee399eee5274f2b2156993da1826f1a5a53addae36b885d963828f57"  # pragma: allowlist secret
CANONICAL_SCHEMA_PATH = Path(
    "docs/90.references/data/reference-information-architecture.schema.json"
)
DATA_ASSET_ROOT = Path("docs/90.references/data")
DATA_ASSET_README = DATA_ASSET_ROOT / "README.md"
REFERENCE_ROOT = Path("docs/90.references")
REGISTRY_PATH = Path("docs/99.templates/support/document-profiles.json")
ALLOWED_PATH_ROOTS = frozenset({"docs", "scripts", "tests"})
GIT_SHA1_PATTERN = re.compile(r"^git-sha1:([0-9a-f]{40})$")
OID_PATTERN = re.compile(r"^[0-9a-f]{40}$")
PACK_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)*$")
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

HISTORICAL_SOURCE_COMMIT = "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47"
CURRENT_ROOT_COMMIT = "git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe"
HISTORICAL_PACK_IDS = (
    "audits/2026-05-24-whga",
    "audits/2026-07-02-whia",
    "audits/2026-07-03-wdgh",
    "audits/2026-07-04-wdcn",
    "audits/2026-07-05-wea",
    "research/2026-07-04-wer",
)
AUDIT_PACK_ID = "audits/2026-07-11-weia"
RESEARCH_PACK_ID = "research/2026-08-08-wer"
TRANSITION_ID = "ria-007-postflight-ledger"
TRANSITION_SUBJECT = "source-coverage-and-migration-ledger"
TRANSITION_MEMBER = "source-coverage-and-migration-ledger.md"
AGENT_CUTOVER_RETIRED_HUB = ".github/ABOUT.md"
AGENT_CUTOVER_REPLACEMENT_HUB = ".github/README.md"
AGENT_CUTOVER_CURRENT_PATH_COUNTS = (
    (
        "docs/90.references/research/2026-08-08-wer/README.md",
        1,
    ),
    (
        "docs/90.references/research/2026-08-08-wer/"
        "ci-cd-github-actions-and-qa.md",
        2,
    ),
    (
        "docs/90.references/research/2026-08-08-wer/"
        "source-coverage-and-migration-ledger.md",
        1,
    ),
)
DATA_ASSET_FIELDS = frozenset({"id", "repositoryEvidence", "refreshTrigger", "sources"})
SOURCE_RECORD_FIELDS = frozenset({"url", "checkedOn", "adoptedScope", "rejectedScope"})
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

DUPLICATE_CANONICAL_OWNER_ROOTS = (
    Path("docs/00.agent-governance"),
    Path("docs/05.operations/policies"),
    Path("docs/05.operations/runbooks"),
)
DUPLICATE_RULE_FIELDS = frozenset(
    {"canonicalOwnerRoots", "minimumParagraphCharacters", "structuralExceptions"}
)
STRUCTURAL_EXCEPTION_FIELDS = frozenset(
    {
        "canonicalOwnerPath",
        "referencePath",
        "paragraphSha256",
        "structuralRole",
        "reason",
    }
)
STRUCTURAL_ROLES = frozenset({"navigation"})
DUPLICATE_MINIMUM_PARAGRAPH_CHARACTERS = 160
CURRENT_INDEX_SPECS: Mapping[str, tuple[Path, str, str]] = MappingProxyType(
    {
        "audits": (
            Path("docs/90.references/audits/README.md"),
            "Audit Pack Registry",
            "Pack role",
        ),
        "research": (
            Path("docs/90.references/research/README.md"),
            "Research Pack Index",
            "Status",
        ),
    }
)
DUPLICATE_TREE_INVENTORY_ROOTS = frozenset(
    {DATA_ASSET_ROOT, *DUPLICATE_CANONICAL_OWNER_ROOTS}
)

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


@dataclass(frozen=True)
class VisibleParagraph:
    digest: str
    role: str


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


def normalize_contract_path(
    root: Path, contract_path: Path = DEFAULT_CONTRACT_PATH
) -> Path:
    """Return one canonical repository-relative contract authority path."""

    return _path_under_root(root.absolute(), contract_path, field="contract")


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
                    raise ContractError(
                        "RIA-CONTRACT", field, "file exceeds input limit"
                    )
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
    return _decode_json_bytes(
        _read_regular_file(root, relative, field=field), field=field
    )


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
        and arguments[4] == "--"
        and Path(arguments[5]) in DUPLICATE_TREE_INVENTORY_ROOTS
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


def _run_git(
    root: Path, arguments: tuple[str, ...], stdout_limit: int = MAX_METADATA_BYTES
) -> bytes:
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
    match = re.fullmatch(rb"([0-9]{6}) ([0-9a-f]{40}) ([0-3])\t([^\0]+)", records[0])
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
    match = re.fullmatch(rb"([0-9]{6}) ([a-z]+) ([0-9a-f]{40})\t([^\0]+)", records[0])
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
    size = _parse_canonical_size(_git(root, ("cat-file", "-s", oid), runner=runner))
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


def _commit_parents(
    root: Path, oid: str, runner: GitRunner | None = None
) -> tuple[str, ...]:
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
        raise ContractError(
            "RIA-CONTRACT", "$schema", "schema reference is not canonical"
        )
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
        raise ContractError(
            "RIA-CONTRACT", "$schema", "schema reference is not canonical"
        )
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
    parse_repository_path(
        contract.get("currentPackRegistry"), field="currentPackRegistry"
    )
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
                    parse_repository_path(
                        asset.get(key), field=f"generatedAssets[{index}].{key}"
                    )
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
            parse_repository_path(
                path, field=f"duplicateRules.canonicalOwnerRoots[{index}]"
            )
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
    "docs/90.references/audits/2026-07-11-weia/README.md": {
        "table": {
            "section": "Report Index",
            "columns": ["Lifecycle", "Actionable disposition"],
        },
    },
}


def _validate_contract_boundaries(contract: dict[str, object]) -> None:
    registry_path = parse_repository_path(
        contract.get("currentPackRegistry"), field="currentPackRegistry"
    )
    if registry_path != REGISTRY_PATH:
        raise ContractError(
            "RIA-BOUNDARY", "currentPackRegistry", "registry path is fixed"
        )
    if contract.get("schemaVersion") != 2:
        raise ContractError("RIA-CONTRACT", "schemaVersion", "schema version must be 2")
    guard = contract.get("snapshotGuard")
    if not isinstance(guard, Mapping):
        raise ContractError("RIA-CONTRACT", "snapshotGuard", "must be an object")
    source = guard.get("sourceCommit")
    parse_git_sha1(source)
    if source != HISTORICAL_SOURCE_COMMIT:
        raise ContractError(
            "RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "historical source is fixed"
        )
    historical = _unique_strings(
        guard.get("historicalPackIds"), field="snapshotGuard.historicalPackIds"
    )
    if tuple(historical) != HISTORICAL_PACK_IDS:
        raise ContractError(
            "RIA-SNAPSHOT",
            "snapshotGuard.historicalPackIds",
            "historical pack set is fixed",
        )
    baselines = contract.get("currentPackBaselines")
    if not isinstance(baselines, Mapping):
        raise ContractError("RIA-CONTRACT", "currentPackBaselines", "must be an object")
    for key, value in baselines.items():
        if not isinstance(key, str) or PACK_ID_PATTERN.fullmatch(key) is None:
            raise ContractError(
                "RIA-CONTRACT", "currentPackBaselines", "pack key is invalid"
            )
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
        raise ContractError(
            "RIA-CONTRACT", "mutableIndexProjections", "must be an array"
        )
    seen: set[str] = set()
    for index, projection in enumerate(projections):
        if not isinstance(projection, Mapping):
            raise ContractError(
                "RIA-CONTRACT", f"mutableIndexProjections[{index}]", "must be an object"
            )
        path = projection.get("path")
        if not isinstance(path, str) or path in seen:
            raise ContractError(
                "RIA-CONTRACT", "mutableIndexProjections", "contains duplicate paths"
            )
        seen.add(path)
        expected = _PROJECTION_ALLOWLIST.get(path)
        if expected is None or dict(projection) != {"path": path, **expected}:
            raise ContractError(
                "RIA-OVERLAY", path, "projection is outside the closed allowlist"
            )
    generated = contract.get("generatedAssets")
    if isinstance(generated, list):
        outputs: set[object] = set()
        for asset in generated:
            if not isinstance(asset, Mapping):
                continue
            output = asset.get("outputPath")
            if output in outputs:
                raise ContractError(
                    "RIA-CONTRACT", "generatedAssets", "contains duplicate output paths"
                )
            outputs.add(output)


def load_contract(
    root: Path,
    contract_path: Path,
    *,
    runner: GitRunner | None = None,
) -> dict[str, object]:
    """Load a contract whose schema has exact proposed index authority."""

    root = root.absolute()
    relative = normalize_contract_path(root, contract_path)
    contract = _load_json(root, relative, field="contract")
    _validate_path_fields(contract)
    _validate_schema(root, contract, relative, runner)
    _validate_contract_boundaries(contract)
    return contract


def _load_contract_for_self_test(root: Path, contract_path: Path) -> dict[str, object]:
    """Load isolated fixture files without claiming proposed Git authority."""

    root = root.absolute()
    relative = normalize_contract_path(root, contract_path)
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
    relative = normalize_contract_path(root, contract_path)
    oid = parse_git_sha1(encoded_commit, field="--commit")
    try:
        payload = _read_commit_path(root, oid, relative, runner)
    except _GitError as error:
        raise ContractError(
            "RIA-TRANSITION", relative.as_posix(), error.message
        ) from error
    contract = _decode_json_bytes(payload, field="contract")
    _validate_path_fields(contract)
    _validate_schema_at_commit(root, oid, contract, relative, runner)
    _validate_contract_boundaries(contract)
    return contract


def _strict_date(value: object) -> date | None:
    if (
        not isinstance(value, str)
        or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None
    ):
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
        match = re.fullmatch(rb"([0-9]{6}) ([0-9a-f]{40}) ([0-3])\t([^\0]+)", record)
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
        match = re.fullmatch(rb"([0-9]{6}) ([a-z]+) ([0-9a-f]{40})\t([^\0]+)", record)
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


def _inventory_path_under(payload: bytes, inventory_root: Path, *, field: str) -> Path:
    try:
        decoded = payload.decode("utf-8", "strict")
        path = parse_repository_path(decoded, field=field)
    except (UnicodeDecodeError, ContractError) as error:
        raise _GitError("tracked inventory path is invalid") from error
    if inventory_root not in path.parents:
        raise _GitError("tracked inventory escaped its fixed root")
    return path


def _parse_regular_inventory(
    payload: bytes, inventory_root: Path, *, committed: bool
) -> tuple[Path, ...]:
    records = payload.split(b"\0")
    if not records or records[-1] != b"":
        raise _GitError("tracked inventory is not NUL terminated")
    paths: list[Path] = []
    seen: set[Path] = set()
    for record in records[:-1]:
        if committed:
            match = re.fullmatch(
                rb"([0-9]{6}) ([a-z]+) ([0-9a-f]{40})\t([^\0]+)", record
            )
            if match is None:
                raise _GitError("tracked tree inventory is malformed")
            mode, object_type, _oid, returned_path = match.groups()
            if mode not in {b"100644", b"100755"} or object_type != b"blob":
                raise _GitError("tracked tree inventory includes nonregular data")
        else:
            match = re.fullmatch(
                rb"([0-9]{6}) ([0-9a-f]{40}) ([0-3])\t([^\0]+)", record
            )
            if match is None:
                raise _GitError("tracked index inventory is malformed")
            mode, _oid, stage, returned_path = match.groups()
            if mode not in {b"100644", b"100755"} or stage != b"0":
                raise _GitError("tracked index inventory includes nonregular data")
        path = _inventory_path_under(
            returned_path,
            inventory_root,
            field="duplicateRules.canonicalOwnerRoots",
        )
        if path in seen:
            raise _GitError("tracked inventory includes a duplicate path")
        seen.add(path)
        paths.append(path)
    return tuple(sorted(paths))


def _tracked_markdown_paths(
    root: Path,
    inventory_root: Path,
    *,
    commit_oid: str | None,
    runner: GitRunner | None,
) -> tuple[Path, ...]:
    if inventory_root not in DUPLICATE_CANONICAL_OWNER_ROOTS:
        raise _GitError("duplicate inventory root is outside the fixed set")
    if commit_oid is None:
        payload = _git(
            root,
            ("ls-files", "-z", "--stage", "--", inventory_root.as_posix()),
            runner=runner,
        )
        paths = _parse_regular_inventory(payload, inventory_root, committed=False)
    else:
        _require_commit(root, commit_oid, runner)
        payload = _git(
            root,
            (
                "ls-tree",
                "-rz",
                "--full-tree",
                commit_oid,
                "--",
                inventory_root.as_posix(),
            ),
            runner=runner,
        )
        paths = _parse_regular_inventory(payload, inventory_root, committed=True)
    return tuple(path for path in paths if path.suffix == ".md")


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
            Finding(
                "RIA-SOURCE", "evidenceCutoff", "cutoff is not a strict calendar date"
            )
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
                    Finding(
                        "RIA-SOURCE",
                        "--commit",
                        "source evidence authority is unavailable",
                    ),
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
                        Finding(
                            "RIA-SOURCE", field, "repository evidence path is invalid"
                        )
                    )
                    continue
                if path in local_evidence or path in seen_evidence:
                    findings.append(
                        Finding(
                            "RIA-SOURCE",
                            field,
                            "repository evidence path is duplicated",
                        )
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
                Finding(
                    "RIA-SOURCE",
                    f"{asset_field}.sources",
                    "source records must be non-empty",
                )
            )
            continue
        seen_sources: set[str] = set()
        for source_index, source in enumerate(sources):
            source_field = f"{asset_field}.sources[{source_index}]"
            if not isinstance(source, Mapping):
                findings.append(
                    Finding(
                        "RIA-SOURCE", source_field, "source record must be an object"
                    )
                )
                continue
            if set(source) != SOURCE_RECORD_FIELDS:
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        source_field,
                        "source record fields are not closed",
                    )
                )
            try:
                identity = json.dumps(
                    dict(source),
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=True,
                )
            except (TypeError, ValueError):
                identity = ""
            if not identity or identity in seen_sources:
                findings.append(
                    Finding(
                        "RIA-SOURCE",
                        source_field,
                        "source record is invalid or duplicated",
                    )
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
                    Finding(
                        "RIA-SOURCE",
                        source_field,
                        "adopted and rejected scopes overlap",
                    )
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
                Finding(
                    "RIA-GENERATOR", field, "generator relation fields are not closed"
                )
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
        raise ContractError(
            "RIA-CONTRACT",
            REGISTRY_PATH.as_posix(),
            "Current pack registry is malformed",
        )
    profile = root.get("profileId")
    records = root.get("packs")
    if not isinstance(profile, str) or not isinstance(records, list):
        raise ContractError(
            "RIA-CONTRACT",
            REGISTRY_PATH.as_posix(),
            "Current pack registry is malformed",
        )
    packs: list[Pack] = []
    pack_ids: set[str] = set()
    all_paths: set[Path] = set()
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ContractError(
                "RIA-CONTRACT", REGISTRY_PATH.as_posix(), "registry pack is malformed"
            )
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
            raise ContractError(
                "RIA-CONTRACT",
                f"currentPackRegistry.packs[{index}]",
                "registry pack is malformed",
            )
        pack_ids.add(pack_id)
        pack = Pack(pack_id, tuple(states), tuple(members))
        for path in (pack.readme_path, *pack.member_paths):
            parse_repository_path(path.as_posix(), field="currentPackRegistry.members")
            if path in all_paths:
                raise ContractError(
                    "RIA-CONTRACT",
                    REGISTRY_PATH.as_posix(),
                    "Current path is duplicated",
                )
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
            raise ContractError(
                "RIA-CONTRACT", "currentPackBaselines", "map is malformed"
            )
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
        # Every pack that is still declared must match its baseline declaration
        # byte for byte. Retiring a whole collection from Current-pack
        # governance is a reviewed registry change, so a pack that is absent
        # from the proposal is not drift; it simply stops being guarded here.
        baseline_by_id = {pack.pack_id: pack for pack in registry.packs}
        if registry.profile_id != proposed_registry.profile_id or any(
            baseline_by_id.get(pack.pack_id) != pack for pack in proposed_registry.packs
        ):
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


def _code_span_intervals(
    value: str,
    *,
    run_lengths: Mapping[int, int] | None = None,
    next_backtick: Mapping[int, int] | None = None,
) -> tuple[tuple[int, int], ...]:
    if run_lengths is None or next_backtick is None:
        run_lengths, next_backtick = _backtick_runs(value)
    if not run_lengths:
        return ()
    intervals: list[tuple[int, int]] = []
    cursor = 0
    while cursor < len(value):
        run_length = run_lengths.get(cursor)
        if run_length is None:
            cursor += 1
            continue
        closing = next_backtick.get(cursor)
        if closing is None:
            cursor += run_length
            continue
        intervals.append((cursor, closing + run_length))
        cursor = closing + run_length
    return tuple(intervals)


COMMONMARK_LINE_ENDING_PATTERN = re.compile(r"\r\n|\r|\n")


def _commonmark_splitlines(text: str) -> list[str]:
    if not text:
        return []
    lines = COMMONMARK_LINE_ENDING_PATTERN.split(text)
    if lines[-1] == "" and text.endswith(("\r", "\n")):
        lines.pop()
    return lines


def _commonmark_line_spans(text: str) -> tuple[tuple[int, int], ...]:
    spans: list[tuple[int, int]] = []
    start = 0
    for ending in COMMONMARK_LINE_ENDING_PATTERN.finditer(text):
        spans.append((start, ending.start()))
        start = ending.end()
    if start < len(text):
        spans.append((start, len(text)))
    return tuple(spans)


def _list_container_content(line: str) -> tuple[str, int] | None:
    match = re.match(
        r"^[ ]{0,3}(?:[-+*]|[0-9]{1,9}[.)])[ \t]+(?P<content>.*)$",
        line,
    )
    if match is None:
        return None
    return match.group("content"), match.start("content")


def _code_block_intervals(text: str) -> tuple[tuple[int, int], ...]:
    intervals: list[tuple[int, int]] = []
    fenced_character: str | None = None
    fenced_length = 0
    fenced_list_indent: int | None = None
    fenced_blockquote_depth: int | None = None
    list_indent: int | None = None
    list_blockquote_depth: int | None = None
    paragraph_open = False
    paragraph_scope: tuple[int, int | None] | None = None

    for start, end in _commonmark_line_spans(text):
        line = text[start:end]
        container_line, blockquote_depth = _blockquote_container(line)
        stripped = container_line.strip()
        if fenced_character is not None:
            intervals.append((start, end))
            semantic_line = container_line
            if (
                fenced_list_indent is not None
                and blockquote_depth == fenced_blockquote_depth
                and len(container_line) - len(container_line.lstrip(" "))
                >= fenced_list_indent
            ):
                semantic_line = container_line[fenced_list_indent:]
            candidate = semantic_line.lstrip(" ")
            indentation = len(semantic_line) - len(candidate)
            run = len(candidate) - len(candidate.lstrip(fenced_character))
            if (
                indentation <= 3
                and run >= fenced_length
                and not candidate[run:].strip()
            ):
                fenced_character = None
                fenced_length = 0
                fenced_list_indent = None
                fenced_blockquote_depth = None
            continue

        list_item = _list_container_content(container_line)
        semantic_line = container_line
        if list_item is not None:
            semantic_line, list_indent = list_item
            list_blockquote_depth = blockquote_depth
        elif list_indent is not None and blockquote_depth == list_blockquote_depth:
            leading_spaces = len(container_line) - len(container_line.lstrip(" "))
            if not stripped:
                semantic_line = ""
            elif leading_spaces >= list_indent:
                semantic_line = container_line[list_indent:]
            else:
                list_indent = None
                list_blockquote_depth = None
        else:
            list_indent = None
            list_blockquote_depth = None

        scope = (blockquote_depth, list_indent)
        if paragraph_open and scope != paragraph_scope:
            paragraph_open = False
            paragraph_scope = None
        opening_fence = _fence_opening(semantic_line)
        if opening_fence is not None:
            intervals.append((start, end))
            fenced_character, fenced_length = opening_fence
            fenced_list_indent = list_indent
            fenced_blockquote_depth = blockquote_depth
            paragraph_open = False
            paragraph_scope = None
            continue
        if not semantic_line.strip():
            paragraph_open = False
            paragraph_scope = None
            continue
        if semantic_line.startswith(("    ", "\t")) and not paragraph_open:
            intervals.append((start, end))
            continue
        if re.match(r"^[ ]{0,3}#{1,6}(?:[ \t]|$)", semantic_line):
            paragraph_open = False
            paragraph_scope = None
            continue
        paragraph_open = True
        paragraph_scope = scope
    return tuple(intervals)


def _inline_code_intervals_outside_blocks(
    text: str, block_intervals: Sequence[tuple[int, int]]
) -> tuple[tuple[int, int], ...]:
    intervals: list[tuple[int, int]] = []
    cursor = 0
    for start, end in block_intervals:
        if cursor < start:
            intervals.extend(
                (cursor + opening, cursor + closing)
                for opening, closing in _code_span_intervals(text[cursor:start])
            )
        cursor = max(cursor, end)
    if cursor < len(text):
        intervals.extend(
            (cursor + opening, cursor + closing)
            for opening, closing in _code_span_intervals(text[cursor:])
        )
    return tuple(intervals)


def _mask_block_intervals(text: str, intervals: Sequence[tuple[int, int]]) -> str:
    if not intervals:
        return text
    output: list[str] = []
    cursor = 0
    for start, end in intervals:
        output.append(text[cursor:start])
        output.append(
            "".join(
                character if character in {"\r", "\n"} else " "
                for character in text[start:end]
            )
        )
        cursor = end
    output.append(text[cursor:])
    return "".join(output)


def _valid_inline_comment_end(text: str, opening: int) -> int | None:
    body_start = opening + len("<!--")
    if text.startswith((">", "->"), body_start):
        return None
    closing = text.find("-->", body_start)
    if closing < 0:
        return None
    body = text[body_start:closing]
    if "--" in body or body.endswith("-"):
        return None
    return closing + len("-->")


def _mask_markdown_comments(text: str) -> str:
    output: list[str] = []
    cursor = 0
    block_intervals = _code_block_intervals(text)
    code_spans = tuple(
        sorted(
            (
                *block_intervals,
                *_inline_code_intervals_outside_blocks(text, block_intervals),
            )
        )
    )
    span_index = 0
    while cursor < len(text):
        opening = text.find("<!--", cursor)
        if opening < 0:
            output.append(text[cursor:])
            break
        while span_index < len(code_spans) and code_spans[span_index][1] <= opening:
            span_index += 1
        if (
            span_index < len(code_spans)
            and code_spans[span_index][0] <= opening < code_spans[span_index][1]
        ):
            preserved_end = opening + len("<!--")
            output.append(text[cursor:preserved_end])
            cursor = preserved_end
            continue
        line_start = (
            max(
                text.rfind("\n", 0, opening),
                text.rfind("\r", 0, opening),
            )
            + 1
        )
        container_prefix, _depth = _blockquote_container(text[line_start:opening])
        block_comment = len(container_prefix) <= 3 and container_prefix.strip(" ") == ""
        if block_comment:
            closing = text.find("-->", opening + 4)
            end = len(text) if closing < 0 else closing + 3
        else:
            end = _valid_inline_comment_end(text, opening)
            if end is None:
                preserved_end = opening + len("<!--")
                output.append(text[cursor:preserved_end])
                cursor = preserved_end
                continue
            closing = end - len("-->")
        output.append(text[cursor:opening])
        if block_comment and closing >= 0:
            line_end = COMMONMARK_LINE_ENDING_PATTERN.search(text, end)
            end = len(text) if line_end is None else line_end.start()
        mask = " " if block_comment else "\u2060"
        output.append(
            "".join(
                character if block_comment and character in {"\r", "\n"} else mask
                for character in text[opening:end]
            )
        )
        cursor = end
    return _mask_block_intervals("".join(output), block_intervals)


def _blockquote_container(line: str) -> tuple[str, int]:
    value = line
    depth = 0
    while True:
        candidate = value.lstrip(" ")
        removed = len(value) - len(candidate)
        if removed <= 3 and candidate.startswith(">"):
            value = candidate[1:]
            depth += 1
            if value.startswith(" "):
                value = value[1:]
            continue
        break
    return value, depth


def _strip_blockquote_container(line: str) -> str:
    return _blockquote_container(line)[0]


def _strip_markdown_container(line: str, *, strip_list_marker: bool = True) -> str:
    value = _strip_blockquote_container(line)
    if not strip_list_marker:
        return value
    match = re.match(r"^[ ]*(?:[-+*]|[0-9]{1,9}[.)])[ \t]+", value)
    return value[match.end() :] if match is not None else value


def _list_item_start(
    line: str,
    *,
    nested: bool,
    interrupting_paragraph: bool,
) -> bool:
    value = _strip_blockquote_container(line)
    match = re.match(
        r"^(?P<indent>[ ]*)(?P<marker>[-+*]|[0-9]{1,9}[.)])[ \t]+",
        value,
    )
    if match is None or not (len(match.group("indent")) <= 3 or nested):
        return False
    marker = match.group("marker")
    if interrupting_paragraph and marker[0].isdigit() and int(marker[:-1]) != 1:
        return False
    return True


class _CompactIntervals:
    __slots__ = ("ends", "starts")

    def __init__(self, starts: array | None = None, ends: array | None = None):
        self.starts = array("I") if starts is None else starts
        self.ends = array("I") if ends is None else ends

    def __len__(self) -> int:
        return len(self.starts)

    def __getitem__(self, index: int) -> tuple[int, int]:
        return self.starts[index], self.ends[index]


class _CompactCloserMap:
    __slots__ = ("_cursor", "_ends", "_last_key", "_starts")

    def __init__(self, starts: array, ends: array):
        self._starts = starts
        self._ends = ends
        self._cursor = 0
        self._last_key = -1

    def __len__(self) -> int:
        return len(self._starts)

    def get(self, key: int, default: int | None = None) -> int | None:
        if key < self._last_key:
            self._cursor = 0
        self._last_key = key
        while self._cursor < len(self._starts) and self._starts[self._cursor] < key:
            self._cursor += 1
        if (
            self._cursor < len(self._starts)
            and self._starts[self._cursor] == key
            and self._ends[self._cursor] >= 0
        ):
            return self._ends[self._cursor]
        return default


class _InlineAngleTokens:
    __slots__ = ("autolink_ends", "html_ends", "starts")

    def __init__(self) -> None:
        self.starts = array("I")
        self.html_ends = array("i")
        self.autolink_ends = array("i")

    def __len__(self) -> int:
        return len(self.starts)

    def html_closers(self) -> _CompactCloserMap:
        return _CompactCloserMap(self.starts, self.html_ends)

    def autolink_closers(self) -> _CompactCloserMap:
        return _CompactCloserMap(self.starts, self.autolink_ends)


def _inline_angle_tokens(value: str) -> _InlineAngleTokens:
    tokens = _InlineAngleTokens()
    starts = tokens.starts
    html_ends = tokens.html_ends
    autolink_ends = tokens.autolink_ends
    record = 0
    html_record = -1
    autolink_record = -1
    quote: str | None = None
    for index, character in enumerate(value):
        if character == "<":
            starts.append(index)
            html_ends.append(-1)
            autolink_ends.append(-1)
            autolink_record = record
            if html_record < 0 or quote is None:
                html_record = record
            record += 1
            continue
        if character == ">":
            if autolink_record >= 0:
                autolink_ends[autolink_record] = index
                autolink_record = -1
            if html_record >= 0 and quote is None:
                html_ends[html_record] = index
                html_record = -1
            continue
        if html_record < 0:
            continue
        if quote is not None:
            if character == quote:
                quote = None
        elif character in {'"', "'"}:
            quote = character
    return tokens


def _append_compact_interval(
    starts: array,
    ends: array,
    start: int,
    end: int,
) -> None:
    if starts and start <= ends[-1]:
        ends[-1] = max(ends[-1], end)
        return
    starts.append(start)
    ends.append(end)


def _inline_opaque_intervals(
    value: str,
    *,
    run_lengths: Mapping[int, int] | None = None,
    next_backtick: Mapping[int, int] | None = None,
    angle_tokens: _InlineAngleTokens | None = None,
) -> _CompactIntervals:
    code_spans = _code_span_intervals(
        value,
        run_lengths=run_lengths,
        next_backtick=next_backtick,
    )
    tokens = _inline_angle_tokens(value) if angle_tokens is None else angle_tokens
    starts = array("I")
    ends = array("I")
    code_index = 0
    active_code_end = -1
    for token_index, opening in enumerate(tokens.starts):
        while code_index < len(code_spans) and code_spans[code_index][0] <= opening:
            code_start, code_end = code_spans[code_index]
            _append_compact_interval(starts, ends, code_start, code_end)
            active_code_end = max(active_code_end, code_end)
            code_index += 1
        if opening < active_code_end:
            continue
        autolink_closing = tokens.autolink_ends[token_index]
        if (
            autolink_closing >= 0
            and _consume_autolink(
                value,
                opening,
                closing=autolink_closing,
            )
            is not None
        ):
            _append_compact_interval(
                starts,
                ends,
                opening,
                autolink_closing + 1,
            )
            continue
        html_closing = tokens.html_ends[token_index]
        if html_closing >= 0 and _inline_html_tag(value, opening, html_closing):
            _append_compact_interval(
                starts,
                ends,
                opening,
                html_closing + 1,
            )
    while code_index < len(code_spans):
        code_start, code_end = code_spans[code_index]
        _append_compact_interval(starts, ends, code_start, code_end)
        code_index += 1
    return _CompactIntervals(starts, ends)


def _paired_delimiters(
    value: str,
    opening: str,
    closing: str,
    *,
    opaque_spans: Sequence[tuple[int, int]] | _CompactIntervals | None = None,
) -> dict[int, int]:
    if opening not in value or closing not in value:
        return {}
    stack: list[int] = []
    pairs: dict[int, int] = {}
    escaped = False
    owned_spans = (
        _inline_opaque_intervals(value) if opaque_spans is None else opaque_spans
    )
    owned_starts = (
        owned_spans.starts if isinstance(owned_spans, _CompactIntervals) else None
    )
    owned_ends = (
        owned_spans.ends if isinstance(owned_spans, _CompactIntervals) else None
    )
    span_index = 0
    for index, character in enumerate(value):
        span_start = (
            owned_starts[span_index]
            if owned_starts is not None and span_index < len(owned_starts)
            else owned_spans[span_index][0]
            if span_index < len(owned_spans)
            else -1
        )
        span_end = (
            owned_ends[span_index]
            if owned_ends is not None and span_index < len(owned_ends)
            else owned_spans[span_index][1]
            if span_index < len(owned_spans)
            else -1
        )
        while span_index < len(owned_spans) and span_end <= index:
            span_index += 1
            span_start = (
                owned_starts[span_index]
                if owned_starts is not None and span_index < len(owned_starts)
                else owned_spans[span_index][0]
                if span_index < len(owned_spans)
                else -1
            )
            span_end = (
                owned_ends[span_index]
                if owned_ends is not None and span_index < len(owned_ends)
                else owned_spans[span_index][1]
                if span_index < len(owned_spans)
                else -1
            )
        if span_index < len(owned_spans) and span_start <= index < span_end:
            escaped = False
            continue
        if not escaped:
            if character == opening:
                stack.append(index)
            elif character == closing and stack:
                pairs[stack.pop()] = index
        if character == "\\":
            escaped = not escaped
        else:
            escaped = False
    return pairs


ASCII_PUNCTUATION = frozenset(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")

COMMONMARK_LINK_WHITESPACE = frozenset({" ", "\t", "\r", "\n"})

INVISIBLE_OBFUSCATION_CHARACTERS = frozenset({"\u00ad", "\u200b", "\u2060", "\ufeff"})

NON_RENDERING_FORMAT_CONTROL_RANGES = (
    (0x061C, 0x061C),
    (0x180E, 0x180E),
    (0x200E, 0x200F),
    (0x202A, 0x202E),
    (0x2061, 0x2064),
    (0x2066, 0x206F),
    (0xE0001, 0xE0001),
    (0xE0020, 0xE007F),
)

CHARACTER_REFERENCE_PATTERN = re.compile(
    r"&(?:#[0-9]{1,7}|#[xX][0-9A-Fa-f]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});"
)

URI_AUTOLINK_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9+.-]{1,31}:[^<>\x00-\x20]*")

EMAIL_AUTOLINK_PATTERN = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*"
)

BLOCK_HTML_TAGS = frozenset(
    {
        "address",
        "article",
        "aside",
        "base",
        "basefont",
        "blockquote",
        "body",
        "caption",
        "center",
        "col",
        "colgroup",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frame",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hr",
        "html",
        "iframe",
        "legend",
        "li",
        "link",
        "main",
        "menu",
        "menuitem",
        "nav",
        "noframes",
        "ol",
        "optgroup",
        "option",
        "p",
        "param",
        "pre",
        "script",
        "search",
        "section",
        "style",
        "summary",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "title",
        "tr",
        "track",
        "ul",
        "textarea",
    }
)

EXPLICIT_RAW_HTML_CLOSERS = {
    "script": "</script>",
    "style": "</style>",
    "pre": "</pre>",
    "textarea": "</textarea>",
}


def _strip_commonmark_link_whitespace(value: str) -> str:
    start = 0
    end = len(value)
    while start < end and value[start] in COMMONMARK_LINK_WHITESPACE:
        start += 1
    while end > start and value[end - 1] in COMMONMARK_LINK_WHITESPACE:
        end -= 1
    return value[start:end]


def _ascii_control(character: str) -> bool:
    codepoint = ord(character)
    return codepoint < 0x20 or codepoint == 0x7F


def _valid_link_target(value: str, *, allow_empty_destination: bool) -> bool:
    candidate = _strip_commonmark_link_whitespace(value)
    if not candidate:
        return allow_empty_destination
    if "\n\n" in candidate or "\r\r" in candidate:
        return False

    cursor = 0
    if candidate.startswith("<"):
        cursor = 1
        destination_closed = False
        while cursor < len(candidate):
            character = candidate[cursor]
            if (
                character == "\\"
                and cursor + 1 < len(candidate)
                and candidate[cursor + 1] in ASCII_PUNCTUATION
            ):
                cursor += 2
                continue
            if character == ">":
                cursor += 1
                destination_closed = True
                break
            if character in {"<", "\n", "\r"}:
                return False
            cursor += 1
        if not destination_closed:
            return False
    else:
        depth = 0
        while cursor < len(candidate):
            character = candidate[cursor]
            if character in COMMONMARK_LINK_WHITESPACE:
                break
            if (
                character == "\\"
                and cursor + 1 < len(candidate)
                and candidate[cursor + 1] in ASCII_PUNCTUATION
            ):
                cursor += 2
                continue
            if character == "<" or _ascii_control(character):
                return False
            if character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    return False
                depth -= 1
            cursor += 1
        if depth != 0 or (cursor == 0 and not allow_empty_destination):
            return False

    if cursor == len(candidate):
        return True
    if candidate[cursor] not in COMMONMARK_LINK_WHITESPACE:
        return False
    tail = _strip_commonmark_link_whitespace(candidate[cursor:])
    if len(tail) < 2:
        return False
    opener = tail[0]
    closer = {'"': '"', "'": "'", "(": ")"}.get(opener)
    if closer is None or tail[-1] != closer:
        return False
    body = tail[1:-1]
    cursor = 0
    while cursor < len(body):
        character = body[cursor]
        if (
            character == "\\"
            and cursor + 1 < len(body)
            and body[cursor + 1] in ASCII_PUNCTUATION
        ):
            cursor += 2
            continue
        if character == closer or (opener == "(" and character == "("):
            return False
        cursor += 1
    return True


def _consume_markdown_link(
    value: str,
    cursor: int,
    *,
    limit: int,
    reference_labels: frozenset[str],
    square_pairs: Mapping[int, int],
    parenthesis_pairs: Mapping[int, int],
) -> tuple[int, int, int] | None:
    image = value.startswith("![", cursor)
    if not image and value[cursor] != "[":
        return None
    opening = cursor + 1 if image else cursor
    closing = square_pairs.get(opening)
    if closing is None or closing >= limit:
        return None
    suffix = closing + 1
    consumed = suffix
    if suffix < limit and value[suffix] == "(":
        destination_end = parenthesis_pairs.get(suffix)
        if destination_end is None or destination_end >= limit:
            return None
        if not _valid_link_target(
            value[suffix + 1 : destination_end],
            allow_empty_destination=True,
        ):
            return None
        consumed = destination_end + 1
    elif suffix < limit and value[suffix] == "[":
        reference_end = _reference_label_closing(
            value,
            suffix,
            limit=limit,
            allow_empty=True,
        )
        if reference_end is None:
            return None
        reference = value[suffix + 1 : reference_end]
        if not reference:
            reference = value[opening + 1 : closing]
            if not _valid_reference_label_content(
                reference,
                allow_empty=False,
            ):
                return None
        if _normalize_reference_label(reference) not in reference_labels:
            return None
        consumed = reference_end + 1
    else:
        reference = value[opening + 1 : closing]
        if (
            not _valid_reference_label_content(reference, allow_empty=False)
            or _normalize_reference_label(reference) not in reference_labels
        ):
            return None
    return opening + 1, closing, consumed


def _consume_autolink(
    value: str, cursor: int, *, closing: int
) -> tuple[str, int] | None:
    if closing < 0 or closing >= len(value) or value[closing] != ">":
        return None
    candidate = value[cursor + 1 : closing]
    if (
        URI_AUTOLINK_PATTERN.fullmatch(candidate) is None
        and EMAIL_AUTOLINK_PATTERN.fullmatch(candidate) is None
    ):
        return None
    return candidate, closing + 1


def _inline_html_tag(value: str, cursor: int, closing: int) -> bool:
    if closing < 0 or closing >= len(value) or value[closing] != ">":
        return False
    candidate = value[cursor + 1 : closing]
    if candidate.startswith("/"):
        return re.fullmatch(r"/[A-Za-z][A-Za-z0-9-]*[ \t\n]*", candidate) is not None
    return (
        re.fullmatch(
            r"[A-Za-z][A-Za-z0-9-]*"
            r"(?:[ \t\n]+[A-Za-z_:][A-Za-z0-9_.:-]*"
            r"(?:[ \t\n]*=[ \t\n]*"
            r"(?:[^ \t\n\"'=<>`]+|'[^']*'|\"[^\"]*\"))?)*"
            r"[ \t\n]*/?",
            candidate,
        )
        is not None
    )


def _consume_character_reference(
    value: str, cursor: int, limit: int
) -> tuple[str, int] | None:
    match = CHARACTER_REFERENCE_PATTERN.match(value, cursor, limit)
    if match is None:
        return None
    token = match.group(0)
    if not token.startswith("&#") and token[1:] not in html5:
        return None
    return unescape(token), match.end()


def _normalize_reference_label(value: str) -> str:
    output: list[str] = []
    cursor = 0
    while cursor < len(value):
        if (
            value[cursor] == "\\"
            and cursor + 1 < len(value)
            and value[cursor + 1] in ASCII_PUNCTUATION
        ):
            output.append(value[cursor + 1])
            cursor += 2
            continue
        reference = _consume_character_reference(value, cursor, len(value))
        if reference is not None:
            decoded, cursor = reference
            output.append(decoded)
            continue
        output.append(value[cursor])
        cursor += 1
    return " ".join(unicodedata.normalize("NFKC", "".join(output)).casefold().split())


def _reference_label_closing(
    value: str,
    opening: int,
    *,
    limit: int,
    allow_empty: bool,
) -> int | None:
    if opening >= limit or value[opening] != "[":
        return None
    cursor = opening + 1
    while cursor < limit:
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < limit
            and value[cursor + 1] in ASCII_PUNCTUATION
        ):
            cursor += 2
            continue
        if character == "[":
            return None
        if character == "]":
            raw_length = cursor - opening - 1
            if raw_length > 999 or (raw_length == 0 and not allow_empty):
                return None
            return cursor
        cursor += 1
    return None


def _valid_reference_label_content(value: str, *, allow_empty: bool) -> bool:
    wrapped = f"[{value}]"
    closing = _reference_label_closing(
        wrapped,
        0,
        limit=len(wrapped),
        allow_empty=allow_empty,
    )
    return closing == len(wrapped) - 1


def _parse_reference_definition(value: str) -> str | None:
    candidate = value.lstrip(" ")
    if len(value) - len(candidate) > 3 or not candidate.startswith("["):
        return None
    closing = _reference_label_closing(
        candidate,
        0,
        limit=len(candidate),
        allow_empty=False,
    )
    if (
        closing is None
        or closing + 1 >= len(candidate)
        or candidate[closing + 1] != ":"
    ):
        return None
    raw_label = candidate[1:closing]
    if not raw_label or len(raw_label) > 999:
        return None
    remainder = _strip_commonmark_link_whitespace(candidate[closing + 2 :])
    if not _valid_link_target(
        remainder,
        allow_empty_destination=False,
    ):
        return None
    label = _normalize_reference_label(raw_label)
    return label or None


def _backtick_runs(
    value: str,
) -> tuple[_CompactCloserMap, _CompactCloserMap]:
    starts = array("I")
    run_lengths = array("I")
    next_same_length = array("i")
    previous: dict[int, int] = {}
    cursor = 0
    while cursor < len(value):
        if value[cursor] != "`":
            cursor += 1
            continue
        end = cursor + 1
        while end < len(value) and value[end] == "`":
            end += 1
        run_length = end - cursor
        record = len(starts)
        starts.append(cursor)
        run_lengths.append(run_length)
        next_same_length.append(-1)
        opening_record = previous.get(run_length)
        if opening_record is not None:
            next_same_length[opening_record] = cursor
        previous[run_length] = record
        cursor = end
    return (
        _CompactCloserMap(starts, run_lengths),
        _CompactCloserMap(starts, next_same_length),
    )


def _emphasis_marker_positions(
    value: str,
    *,
    reference_labels: frozenset[str],
    square_pairs: Mapping[int, int],
    parenthesis_pairs: Mapping[int, int],
    angle_closers: _CompactCloserMap,
    autolink_closers: _CompactCloserMap,
    run_lengths: Mapping[int, int],
    next_backtick: Mapping[int, int],
) -> bytearray:
    if not any(marker in value for marker in ("*", "_", "~")):
        return bytearray(len(value))
    escaped = bytearray(len(value))
    backslashes = 0
    for index, character in enumerate(value):
        if character == "\\":
            backslashes += 1
            continue
        escaped[index] = backslashes % 2
        backslashes = 0

    destination_ends: dict[int, int] = {}
    for opening, closing in square_pairs.items():
        suffix = closing + 1
        if suffix < len(value) and value[suffix] == "(":
            destination = parenthesis_pairs.get(suffix)
            if destination is not None and _valid_link_target(
                value[suffix + 1 : destination],
                allow_empty_destination=True,
            ):
                destination_ends[suffix] = destination + 1
        elif suffix < len(value) and value[suffix] == "[":
            reference_end = square_pairs.get(suffix)
            if reference_end is not None:
                reference = (
                    value[suffix + 1 : reference_end] or value[opening + 1 : closing]
                )
                if _normalize_reference_label(reference) in reference_labels:
                    destination_ends[suffix] = reference_end + 1

    def punctuation(character: str | None) -> bool:
        return bool(
            character is not None
            and (
                character in ASCII_PUNCTUATION
                or unicodedata.category(character)[0] in {"P", "S"}
            )
        )

    delimiter_markers = bytearray()
    delimiter_starts = array("I")
    delimiter_widths = bytearray()
    delimiter_run_lengths = array("I")
    delimiter_flags = bytearray()
    delimiter_scopes = array("i")
    delimiter_ends = array("i")
    scope_stack: list[int] = []
    scope_closings: dict[int, int] = {}
    scope_ends: dict[int, int] = {}
    cursor = 0
    while cursor < len(value):
        closing_scope = scope_closings.get(cursor)
        if closing_scope is not None:
            if scope_stack and scope_stack[-1] == closing_scope:
                scope_stack.pop()
            else:
                scope_stack.clear()
        destination_end = destination_ends.get(cursor)
        if destination_end is not None:
            cursor = destination_end
            continue
        if value[cursor] == "[":
            link = _consume_markdown_link(
                value,
                cursor,
                limit=len(value),
                reference_labels=reference_labels,
                square_pairs=square_pairs,
                parenthesis_pairs=parenthesis_pairs,
            )
            if link is not None:
                scope_stack.append(cursor)
                scope_closings[link[1]] = cursor
                scope_ends[cursor] = link[1]
        if value[cursor] == "`":
            run = run_lengths.get(cursor, 1)
            closing = next_backtick.get(cursor)
            cursor = closing + run if closing is not None else cursor + run
            continue
        if value[cursor] == "<":
            autolink = _consume_autolink(
                value,
                cursor,
                closing=autolink_closers.get(cursor, -1),
            )
            if autolink is not None:
                cursor = autolink[1]
                continue
            html_closing = angle_closers.get(cursor, -1)
            if _inline_html_tag(value, cursor, html_closing):
                cursor = html_closing + 1
                continue
        marker = value[cursor]
        if marker not in {"*", "_", "~"} or escaped[cursor]:
            cursor += 1
            continue
        end = cursor + 1
        while end < len(value) and value[end] == marker and not escaped[end]:
            end += 1
        run_length = end - cursor
        scope = scope_stack[-1] if scope_stack else -1
        previous = value[cursor - 1] if cursor > 0 else None
        following = (
            None
            if scope >= 0 and end == scope_ends[scope]
            else value[end]
            if end < len(value)
            else None
        )
        previous_whitespace = previous is None or previous.isspace()
        following_whitespace = following is None or following.isspace()
        previous_punctuation = punctuation(previous)
        following_punctuation = punctuation(following)
        left_flanking = not following_whitespace and (
            not following_punctuation or previous_whitespace or previous_punctuation
        )
        right_flanking = not previous_whitespace and (
            not previous_punctuation or following_whitespace or following_punctuation
        )
        can_open = left_flanking
        can_close = right_flanking
        if marker == "_":
            can_open = left_flanking and (not right_flanking or previous_punctuation)
            can_close = right_flanking and (not left_flanking or following_punctuation)
        if can_open or can_close:
            flags = (1 if can_open else 0) | (2 if can_close else 0)
            if marker in {"*", "_"}:
                for offset in range(run_length):
                    delimiter_markers.append(ord(marker))
                    delimiter_starts.append(cursor + offset)
                    delimiter_widths.append(1)
                    delimiter_run_lengths.append(run_length)
                    delimiter_flags.append(flags)
                    delimiter_scopes.append(scope)
                    delimiter_ends.append(-1)
            elif run_length >= 2:
                first = run_length % 2
                for offset in range(first, run_length, 2):
                    delimiter_markers.append(ord(marker))
                    delimiter_starts.append(cursor + offset)
                    delimiter_widths.append(2)
                    delimiter_run_lengths.append(0)
                    delimiter_flags.append(flags)
                    delimiter_scopes.append(scope)
                    delimiter_ends.append(-1)
        cursor = end

    openers_bottom: dict[tuple[int, int], list[int]] = {}
    header_index = 0
    last_marker_end = -2
    jumps = array("I")
    for closer_index in range(len(delimiter_starts)):
        jumps.append(0)
        if (
            delimiter_markers[header_index] != delimiter_markers[closer_index]
            or last_marker_end != delimiter_starts[closer_index]
        ):
            header_index = closer_index
        last_marker_end = (
            delimiter_starts[closer_index] + delimiter_widths[closer_index]
        )
        if not delimiter_flags[closer_index] & 2:
            continue
        bottom_key = (
            delimiter_markers[closer_index],
            delimiter_scopes[closer_index],
        )
        bottoms = openers_bottom.setdefault(bottom_key, [-1] * 6)
        closer_can_open = bool(delimiter_flags[closer_index] & 1)
        closer_run_length = delimiter_run_lengths[closer_index]
        bottom_slot = (3 if closer_can_open else 0) + closer_run_length % 3
        minimum_opener = bottoms[bottom_slot]
        opener_index = header_index - jumps[header_index] - 1
        new_minimum = opener_index
        while opener_index > minimum_opener:
            if (
                delimiter_markers[opener_index] == delimiter_markers[closer_index]
                and delimiter_scopes[opener_index] == delimiter_scopes[closer_index]
                and delimiter_flags[opener_index] & 1
                and delimiter_ends[opener_index] < 0
            ):
                opener_run_length = delimiter_run_lengths[opener_index]
                odd_match = (
                    (bool(delimiter_flags[opener_index] & 2) or closer_can_open)
                    and (opener_run_length + closer_run_length) % 3 == 0
                    and (opener_run_length % 3 != 0 or closer_run_length % 3 != 0)
                )
                if not odd_match:
                    last_jump = (
                        jumps[opener_index - 1] + 1
                        if opener_index > 0
                        and not delimiter_flags[opener_index - 1] & 1
                        else 0
                    )
                    jumps[closer_index] = closer_index - opener_index + last_jump
                    jumps[opener_index] = last_jump
                    delimiter_flags[closer_index] &= ~1
                    delimiter_ends[opener_index] = closer_index
                    delimiter_flags[opener_index] &= ~2
                    new_minimum = -1
                    last_marker_end = -2
                    break
            opener_index -= jumps[opener_index] + 1
        if new_minimum != -1:
            bottoms[bottom_slot] = new_minimum

    markers = bytearray(len(value))
    for opener_index, closer_index in enumerate(delimiter_ends):
        if closer_index < 0:
            continue
        opener_start = delimiter_starts[opener_index]
        opener_width = delimiter_widths[opener_index]
        closer_start = delimiter_starts[closer_index]
        closer_width = delimiter_widths[closer_index]
        markers[opener_start : opener_start + opener_width] = b"\x01" * opener_width
        markers[closer_start : closer_start + closer_width] = b"\x01" * closer_width
    return markers


def _strip_invisible_characters(value: str) -> str:
    output: list[str] = []
    for character in value:
        codepoint = ord(character)
        if 0x20 <= codepoint <= 0x7E:
            output.append(character)
            continue
        if character in INVISIBLE_OBFUSCATION_CHARACTERS or any(
            start <= codepoint <= end
            for start, end in NON_RENDERING_FORMAT_CONTROL_RANGES
        ):
            continue
        category = unicodedata.category(character)
        if category == "Cc" and not character.isspace():
            continue
        output.append(character)
    return "".join(output)


def _markdown_visible_text(
    value: str, reference_labels: frozenset[str] = frozenset()
) -> str:
    output: list[str] = []
    length = len(value)
    run_lengths, next_backtick = _backtick_runs(value)
    angle_tokens = _inline_angle_tokens(value)
    angle_closers = angle_tokens.html_closers()
    autolink_closers = angle_tokens.autolink_closers()
    opaque_spans = _inline_opaque_intervals(
        value,
        run_lengths=run_lengths,
        next_backtick=next_backtick,
        angle_tokens=angle_tokens,
    )
    square_pairs = _paired_delimiters(
        value,
        "[",
        "]",
        opaque_spans=opaque_spans,
    )
    parenthesis_pairs = _paired_delimiters(
        value,
        "(",
        ")",
        opaque_spans=opaque_spans,
    )
    emphasis_markers = _emphasis_marker_positions(
        value,
        reference_labels=reference_labels,
        square_pairs=square_pairs,
        parenthesis_pairs=parenthesis_pairs,
        angle_closers=angle_closers,
        autolink_closers=autolink_closers,
        run_lengths=run_lengths,
        next_backtick=next_backtick,
    )
    segments = [(0, length)]
    while segments:
        cursor, limit = segments.pop()
        while cursor < limit:
            link = _consume_markdown_link(
                value,
                cursor,
                limit=limit,
                reference_labels=reference_labels,
                square_pairs=square_pairs,
                parenthesis_pairs=parenthesis_pairs,
            )
            if link is not None:
                label_start, label_end, consumed = link
                if consumed < limit:
                    segments.append((consumed, limit))
                cursor, limit = label_start, label_end
                continue
            autolink_angle = autolink_closers.get(cursor, -1)
            if autolink_angle >= limit:
                autolink_angle = -1
            autolink = _consume_autolink(value, cursor, closing=autolink_angle)
            if autolink is not None:
                label, consumed = autolink
                output.append(label)
                cursor = consumed
                continue
            character = value[cursor]
            if character == "`":
                run = run_lengths.get(cursor, 1)
                closing = next_backtick.get(cursor)
                if closing is not None and closing < limit:
                    code = value[cursor + run : closing].replace("\n", " ")
                    output.append(" ".join(code.split()))
                    cursor = closing + run
                    continue
                output.append("`" * run)
                cursor += run
                continue
            if (
                character == "\\"
                and cursor + 1 < limit
                and value[cursor + 1] in ASCII_PUNCTUATION
            ):
                output.append(value[cursor + 1])
                cursor += 2
                continue
            if character == "\\" and cursor + 1 < limit and value[cursor + 1] == "\n":
                output.append(" ")
                cursor += 2
                continue
            reference = _consume_character_reference(value, cursor, limit)
            if reference is not None:
                decoded, cursor = reference
                output.append(decoded)
                continue
            html_angle = angle_closers.get(cursor, -1)
            if html_angle >= limit:
                html_angle = -1
            if character == "<" and _inline_html_tag(value, cursor, html_angle):
                cursor = html_angle + 1
                continue
            if not emphasis_markers[cursor]:
                output.append(character)
            cursor += 1
    normalized = unicodedata.normalize("NFKC", "".join(output)).casefold()
    normalized = _strip_invisible_characters(normalized)
    return " ".join(normalized.split())


def _table_cells(line: str) -> tuple[str, ...] | None:
    stripped = line.strip()
    run_lengths, next_backtick = _backtick_runs(stripped)
    cells: list[str] = []
    cell: list[str] = []
    cursor = 0
    separators = 0
    while cursor < len(stripped):
        character = stripped[cursor]
        if character == "\\" and cursor + 1 < len(stripped):
            cell.extend(stripped[cursor : cursor + 2])
            cursor += 2
            continue
        if character == "`":
            run = run_lengths.get(cursor, 1)
            closing = next_backtick.get(cursor)
            if closing is not None:
                cell.append(stripped[cursor : closing + run])
                cursor = closing + run
                continue
            cell.append("`" * run)
            cursor += run
            continue
        if character == "|":
            cells.append("".join(cell).strip())
            cell.clear()
            separators += 1
            cursor += 1
            continue
        cell.append(character)
        cursor += 1
    if separators == 0:
        return None
    cells.append("".join(cell).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return tuple(cells)


def _table_delimiter(cells: tuple[str, ...] | None) -> bool:
    return bool(
        cells and all(re.fullmatch(r":?-{3,}:?", cell) is not None for cell in cells)
    )


def _fence_opening(line: str) -> tuple[str, int] | None:
    candidate = line.lstrip(" ")
    indentation = len(line) - len(candidate)
    if indentation > 3 or not candidate or candidate[0] not in {"`", "~"}:
        return None
    marker = candidate[0]
    run_length = len(candidate) - len(candidate.lstrip(marker))
    if run_length < 3:
        return None
    if marker == "`" and "`" in candidate[run_length:]:
        return None
    return marker, run_length


def _pure_link_list(
    lines: Sequence[str],
    reference_labels: frozenset[str],
    *,
    strip_list_marker: bool = True,
) -> bool:
    if not lines:
        return False
    for line in lines:
        candidate = _strip_markdown_container(
            line,
            strip_list_marker=strip_list_marker,
        ).strip()
        if not candidate or candidate.startswith("!["):
            return False
        if candidate.startswith("<"):
            tokens = _inline_angle_tokens(candidate)
            autolink = _consume_autolink(
                candidate,
                0,
                closing=tokens.autolink_closers().get(0, -1),
            )
            if autolink is None or autolink[1] != len(candidate):
                return False
            continue
        if not candidate.startswith("["):
            return False
        run_lengths, next_backtick = _backtick_runs(candidate)
        angle_tokens = _inline_angle_tokens(candidate)
        opaque_spans = _inline_opaque_intervals(
            candidate,
            run_lengths=run_lengths,
            next_backtick=next_backtick,
            angle_tokens=angle_tokens,
        )
        square_pairs = _paired_delimiters(
            candidate,
            "[",
            "]",
            opaque_spans=opaque_spans,
        )
        parenthesis_pairs = _paired_delimiters(
            candidate,
            "(",
            ")",
            opaque_spans=opaque_spans,
        )
        link = _consume_markdown_link(
            candidate,
            0,
            limit=len(candidate),
            reference_labels=reference_labels,
            square_pairs=square_pairs,
            parenthesis_pairs=parenthesis_pairs,
        )
        if link is not None:
            label = candidate[link[0] : link[1]]
            if link[2] != len(candidate) or not _valid_reference_label_content(
                label,
                allow_empty=False,
            ):
                return False
            continue
        return False
    return True


def _raw_html_block_start(
    stripped: str, *, paragraph_open: bool
) -> tuple[str, str | None] | None:
    lowered = stripped.casefold()
    explicit = re.match(
        r"^<(?P<tag>script|style|pre|textarea)(?=[\t />]|$)",
        lowered,
    )
    if explicit is not None:
        return "closer", EXPLICIT_RAW_HTML_CLOSERS[explicit.group("tag")]
    if stripped.startswith("<?"):
        return "closer", "?>"
    if stripped.startswith("<![CDATA["):
        return "closer", "]]>"
    if re.match(r"^<![A-Z]", stripped) is not None:
        return "closer", ">"

    tag = re.match(
        r"^</?(?P<tag>[A-Za-z][A-Za-z0-9-]*)(?=[\t />]|$)",
        stripped,
    )
    if tag is not None and tag.group("tag").casefold() in BLOCK_HTML_TAGS:
        return "blank", None
    if paragraph_open:
        return None
    if ">" not in stripped:
        return None
    closing = _inline_angle_tokens(stripped).html_closers().get(0, -1)
    if closing == len(stripped) - 1 and _inline_html_tag(stripped, 0, closing):
        return "blank", None
    return None


def _reference_definitions(
    lines: Sequence[str], *, frontmatter_end: int
) -> tuple[frozenset[str], frozenset[int]]:
    labels: set[str] = set()
    definition_lines: set[int] = set()
    fenced_character: str | None = None
    fenced_length = 0
    raw_closer: str | None = None
    raw_until_blank = False
    paragraph_open = False
    paragraph_depth: int | None = None

    for index in range(frontmatter_end, len(lines)):
        container_line, blockquote_depth = _blockquote_container(lines[index])
        stripped = container_line.strip()
        if paragraph_open and blockquote_depth != paragraph_depth:
            paragraph_open = False
            paragraph_depth = None
        if fenced_character is not None:
            candidate = container_line.lstrip(" ")
            indentation = len(container_line) - len(candidate)
            run = len(candidate) - len(candidate.lstrip(fenced_character))
            if (
                indentation <= 3
                and run >= fenced_length
                and not candidate[run:].strip()
            ):
                fenced_character = None
                fenced_length = 0
            continue
        if raw_closer is not None:
            if raw_closer in stripped.casefold():
                raw_closer = None
            continue
        if raw_until_blank:
            if not stripped:
                raw_until_blank = False
            continue
        if not stripped:
            paragraph_open = False
            paragraph_depth = None
            continue
        opening_fence = _fence_opening(container_line)
        if opening_fence is not None:
            fenced_character, fenced_length = opening_fence
            paragraph_open = False
            paragraph_depth = None
            continue
        raw_start = _raw_html_block_start(stripped, paragraph_open=paragraph_open)
        if raw_start is not None:
            mode, closer = raw_start
            paragraph_open = False
            paragraph_depth = None
            if mode == "blank":
                raw_until_blank = True
            elif closer is not None and closer.casefold() not in stripped.casefold():
                raw_closer = closer.casefold()
            continue
        if container_line.startswith(("    ", "\t")) and not paragraph_open:
            continue
        if index in definition_lines:
            paragraph_open = False
            paragraph_depth = None
            continue
        definition = _strip_markdown_container(container_line)
        label = _parse_reference_definition(definition)
        if not paragraph_open and index + 1 < len(lines):
            continuation, continuation_depth = _blockquote_container(lines[index + 1])
            continuation_text = continuation.lstrip(" ")
            continuation_indent = len(continuation) - len(continuation_text)
            if (
                continuation_depth == blockquote_depth
                and 1 <= continuation_indent <= 3
                and continuation_text
            ):
                continued_label = _parse_reference_definition(
                    definition + "\n" + continuation
                )
                destination_continuation = (
                    label is None
                    and re.fullmatch(
                        r"[ ]{0,3}\[[^\n]+\]:[ \t]*",
                        definition,
                    )
                    is not None
                )
                title_continuation = label is not None and continued_label == label
                if continued_label is not None and (
                    destination_continuation or title_continuation
                ):
                    label = continued_label
                    definition_lines.add(index + 1)
        if not paragraph_open and label is not None:
            labels.add(label)
            definition_lines.add(index)
            continue
        if re.match(r"^[ ]{0,3}#{1,6}(?:[ \t]|$)", container_line):
            paragraph_open = False
            paragraph_depth = None
            continue
        paragraph_open = True
        paragraph_depth = blockquote_depth
    return frozenset(labels), frozenset(definition_lines)


def _visible_paragraphs(payload: bytes) -> tuple[VisibleParagraph, ...]:
    try:
        text = payload.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise _GitError("Markdown is not UTF-8") from error
    lines = _commonmark_splitlines(_mask_markdown_comments(text))
    index = 0
    if lines and lines[0].strip() == "---":
        closing = next(
            (
                position
                for position in range(1, len(lines))
                if lines[position].strip() == "---"
            ),
            None,
        )
        if closing is not None:
            index = closing + 1
    reference_labels, definition_lines = _reference_definitions(
        lines, frontmatter_end=index
    )
    paragraphs: list[VisibleParagraph] = []
    buffered: list[str] = []
    buffered_list_item = False
    buffered_depth: int | None = None
    fenced_character: str | None = None
    fenced_length = 0
    raw_closer: str | None = None
    raw_until_blank = False

    def flush() -> None:
        nonlocal buffered_depth, buffered_list_item
        list_item = buffered_list_item
        buffered_list_item = False
        buffered_depth = None
        if not buffered:
            return
        raw_lines = tuple(buffered)
        buffered.clear()
        if _pure_link_list(
            raw_lines,
            reference_labels,
            strip_list_marker=list_item,
        ):
            return
        raw = "\n".join(
            _strip_markdown_container(
                line,
                strip_list_marker=list_item,
            )
            for line in raw_lines
        )
        visible = _markdown_visible_text(raw, reference_labels)
        if len(visible) < DUPLICATE_MINIMUM_PARAGRAPH_CHARACTERS:
            return
        if visible.startswith(
            (
                "generated by ",
                "this file is generated",
                "this document is generated",
                "automatically generated",
                "do not edit this generated",
            )
        ):
            return
        role = (
            "navigation"
            if ("[" in raw and visible.startswith(("see ", "refer to ")))
            else "prose"
        )
        paragraphs.append(
            VisibleParagraph(hashlib.sha256(visible.encode("utf-8")).hexdigest(), role)
        )

    while index < len(lines):
        line = lines[index]
        container_line, blockquote_depth = _blockquote_container(line)
        stripped = container_line.strip()
        if fenced_character is not None:
            candidate = container_line.lstrip(" ")
            indentation = len(container_line) - len(candidate)
            run = len(candidate) - len(candidate.lstrip(fenced_character))
            if (
                indentation <= 3
                and run >= fenced_length
                and not candidate[run:].strip()
            ):
                fenced_character = None
                fenced_length = 0
            index += 1
            continue
        if raw_closer is not None:
            if raw_closer in stripped.casefold():
                raw_closer = None
            index += 1
            continue
        if raw_until_blank:
            if not stripped:
                raw_until_blank = False
            index += 1
            continue
        if buffered and blockquote_depth != buffered_depth:
            flush()
        if index in definition_lines:
            flush()
            index += 1
            continue
        opening_fence = _fence_opening(container_line)
        if opening_fence is not None:
            flush()
            fenced_character, fenced_length = opening_fence
            index += 1
            continue
        raw_start = _raw_html_block_start(stripped, paragraph_open=bool(buffered))
        if raw_start is not None:
            flush()
            mode, closer = raw_start
            if mode == "blank":
                raw_until_blank = True
            elif closer is not None and closer.casefold() not in stripped.casefold():
                raw_closer = closer.casefold()
            index += 1
            continue
        if not stripped:
            flush()
            index += 1
            continue
        if _list_item_start(
            line,
            nested=buffered_list_item,
            interrupting_paragraph=bool(buffered and not buffered_list_item),
        ):
            flush()
            buffered.append(line)
            buffered_list_item = True
            buffered_depth = blockquote_depth
            index += 1
            continue
        if container_line.startswith(("    ", "\t")):
            if buffered:
                buffered.append(line)
            else:
                flush()
            index += 1
            continue
        if re.match(r"^[ ]{0,3}#{1,6}(?:[ \t]|$)", container_line):
            flush()
            index += 1
            continue
        if buffered and re.fullmatch(r"[ ]{0,3}(?:=+|-+)[ \t]*", container_line):
            buffered.clear()
            buffered_list_item = False
            buffered_depth = None
            index += 1
            continue
        cells = _table_cells(container_line)
        next_cells = (
            _table_cells(_strip_blockquote_container(lines[index + 1]))
            if index + 1 < len(lines)
            else None
        )
        if cells is not None and _table_delimiter(next_cells):
            flush()
            index += 2
            while index < len(lines):
                row = _table_cells(_strip_blockquote_container(lines[index]))
                if row is None:
                    break
                for cell in row:
                    buffered.append(cell)
                    buffered_depth = blockquote_depth
                    flush()
                index += 1
            continue
        if not buffered:
            buffered_depth = blockquote_depth
        buffered.append(line)
        index += 1
    flush()
    return tuple(paragraphs)


def _current_index_claims(
    payload: bytes,
    index_path: Path,
    heading: str,
    role_header: str,
) -> tuple[Path, ...]:
    try:
        lines = payload.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as error:
        raise _GitError("Current index is not UTF-8") from error
    heading_indices = tuple(
        index
        for index, line in enumerate(lines)
        if re.fullmatch(rf"###?[ \t]+{re.escape(heading)}[ \t]*", line) is not None
    )
    if len(heading_indices) != 1:
        raise _GitError("Current index heading authority is not unique")
    heading_index = heading_indices[0]
    section_end = next(
        (
            index
            for index in range(heading_index + 1, len(lines))
            if re.match(r"^#{1,6}(?:[ \t]|$)", lines[index]) is not None
        ),
        len(lines),
    )
    table_indices = tuple(
        index
        for index in range(heading_index + 1, max(heading_index + 1, section_end - 1))
        if _table_cells(lines[index]) is not None
        and _table_delimiter(_table_cells(lines[index + 1]))
    )
    if len(table_indices) != 1:
        raise _GitError("Current index table authority is not unique")
    table_index = table_indices[0]
    header = _table_cells(lines[table_index])
    delimiter = _table_cells(lines[table_index + 1])
    if (
        header is None
        or not _table_delimiter(delimiter)
        or len(header) != len(delimiter or ())
    ):
        raise _GitError("Current index table is malformed")
    normalized_header = tuple(_markdown_visible_text(cell) for cell in header)
    normalized_role = _markdown_visible_text(role_header)
    if normalized_header.count(normalized_role) != 1:
        raise _GitError("Current role column is unavailable")
    role_index = normalized_header.index(normalized_role)
    claims: list[Path] = []
    for row_line in lines[table_index + 2 : section_end]:
        row = _table_cells(row_line)
        if row is None:
            break
        if len(row) != len(header):
            raise _GitError("Current index row width differs")
        if _markdown_visible_text(row[role_index]) != "current pack":
            continue
        matches = list(_MARKDOWN_LINK_PATTERN.finditer(row[0]))
        if len(matches) != 1:
            raise _GitError("Current claim identity is malformed")
        resolved = _resolve_markdown_destination(index_path, matches[0].group(1))
        if resolved is None:
            raise _GitError("Current claim path is invalid")
        claims.append(resolved)
    return tuple(claims)


def validate_duplicate_rules(
    root: Path,
    contract: Mapping[str, object],
    *,
    proposed_commit: object | None = None,
    runner: GitRunner | None = None,
) -> list[Finding]:
    """Reject duplicate Current, generator, and active-policy ownership."""

    findings: list[Finding] = []
    rules = contract.get("duplicateRules")
    if not isinstance(rules, Mapping) or set(rules) != DUPLICATE_RULE_FIELDS:
        return [
            Finding(
                "RIA-DUPLICATE",
                "duplicateRules",
                "duplicate rule fields are not closed",
            )
        ]
    roots = rules.get("canonicalOwnerRoots")
    expected_roots = [path.as_posix() for path in DUPLICATE_CANONICAL_OWNER_ROOTS]
    if roots != expected_roots:
        findings.append(
            Finding(
                "RIA-DUPLICATE",
                "duplicateRules.canonicalOwnerRoots",
                "canonical owner roots do not match the fixed source set",
            )
        )
    threshold = rules.get("minimumParagraphCharacters")
    if threshold != DUPLICATE_MINIMUM_PARAGRAPH_CHARACTERS:
        findings.append(
            Finding(
                "RIA-DUPLICATE",
                "duplicateRules.minimumParagraphCharacters",
                "paragraph threshold does not match the fixed boundary",
            )
        )
    raw_exceptions = rules.get("structuralExceptions")
    if not isinstance(raw_exceptions, list):
        findings.append(
            Finding(
                "RIA-DUPLICATE",
                "duplicateRules.structuralExceptions",
                "structural exceptions must be an array",
            )
        )
        raw_exceptions = []
    if findings:
        return sorted(set(findings))

    commit_oid: str | None = None
    if proposed_commit is not None:
        try:
            commit_oid = parse_git_sha1(proposed_commit, field="--commit")
        except ContractError:
            return [
                Finding(
                    "RIA-DUPLICATE",
                    "--commit",
                    "duplicate authority commit is unavailable",
                )
            ]
    root = root.absolute()
    try:
        registry_payload = _proposed_path(root, REGISTRY_PATH, commit_oid, runner)
        registry = _registry_projection(
            _decode_json_bytes(registry_payload, field=REGISTRY_PATH.as_posix())
        )
    except (ContractError, _GitError):
        return [
            Finding(
                "RIA-DUPLICATE",
                REGISTRY_PATH.as_posix(),
                "Current owner registry is unavailable",
            )
        ]

    manual_paths = set(registry.paths)
    for collection, (index_path, heading, role_header) in CURRENT_INDEX_SPECS.items():
        expected = tuple(
            pack.readme_path
            for pack in registry.packs
            if pack.pack_id.split("/", 1)[0] == collection
        )
        if len(expected) != 1 and not (collection == "research" and not expected):
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    index_path.as_posix(),
                    "Current owner collection is not singular",
                )
            )
        try:
            index_payload = _proposed_path(root, index_path, commit_oid, runner)
            observed = _current_index_claims(
                index_payload, index_path, heading, role_header
            )
        except (ContractError, _GitError):
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    index_path.as_posix(),
                    "Current owner mirror is unavailable",
                )
            )
            continue
        if observed != expected:
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    index_path.as_posix(),
                    "Current owner mirror differs from the registry",
                )
            )

    generated_assets = contract.get("generatedAssets")
    if not isinstance(generated_assets, list):
        findings.append(
            Finding(
                "RIA-DUPLICATE",
                "generatedAssets",
                "generated owner relations are unavailable",
            )
        )
    else:
        for index, asset in enumerate(generated_assets):
            if not isinstance(asset, Mapping):
                findings.append(
                    Finding(
                        "RIA-DUPLICATE",
                        f"generatedAssets[{index}]",
                        "generated owner relation is malformed",
                    )
                )
                continue
            try:
                output = parse_repository_path(
                    asset.get("outputPath"),
                    field=f"generatedAssets[{index}].outputPath",
                )
            except ContractError:
                findings.append(
                    Finding(
                        "RIA-DUPLICATE",
                        f"generatedAssets[{index}].outputPath",
                        "generated output path is invalid",
                    )
                )
                continue
            if output in manual_paths:
                findings.append(
                    Finding(
                        "RIA-DUPLICATE",
                        output.as_posix(),
                        "generated output conflicts with a manual Current owner",
                    )
                )

    source_paths: set[Path] = set()
    try:
        for owner_root in DUPLICATE_CANONICAL_OWNER_ROOTS:
            source_paths.update(
                _tracked_markdown_paths(
                    root, owner_root, commit_oid=commit_oid, runner=runner
                )
            )
    except (ContractError, _GitError):
        findings.append(
            Finding(
                "RIA-DUPLICATE",
                "duplicateRules.canonicalOwnerRoots",
                "canonical owner inventory is unavailable",
            )
        )
        return sorted(set(findings))

    exceptions: list[tuple[Path, Path, str, str]] = []
    seen_exceptions: set[tuple[Path, Path, str, str]] = set()
    for index, exception in enumerate(raw_exceptions):
        field = f"duplicateRules.structuralExceptions[{index}]"
        if (
            not isinstance(exception, Mapping)
            or set(exception) != STRUCTURAL_EXCEPTION_FIELDS
        ):
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    field,
                    "structural exception fields are not closed",
                )
            )
            continue
        try:
            canonical = parse_repository_path(
                exception.get("canonicalOwnerPath"),
                field=f"{field}.canonicalOwnerPath",
            )
            reference = parse_repository_path(
                exception.get("referencePath"),
                field=f"{field}.referencePath",
            )
        except ContractError:
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    field,
                    "structural exception path is invalid",
                )
            )
            continue
        digest = exception.get("paragraphSha256")
        role = exception.get("structuralRole")
        reason = exception.get("reason")
        if (
            not isinstance(digest, str)
            or SHA256_PATTERN.fullmatch(digest) is None
            or role not in STRUCTURAL_ROLES
            or not _closed_single_line_text(reason)
            or not isinstance(reason, str)
            or len(reason) > 512
            or canonical not in source_paths
            or reference not in manual_paths
        ):
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    reference.as_posix(),
                    "structural exception is invalid",
                )
            )
            continue
        key = (canonical, reference, digest, role)
        if key in seen_exceptions:
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    reference.as_posix(),
                    "structural exception is duplicated",
                )
            )
            continue
        seen_exceptions.add(key)
        exceptions.append(key)
    if findings and not source_paths:
        return sorted(set(findings))

    source_paragraphs: dict[str, list[tuple[Path, str]]] = {}
    reference_paragraphs: dict[str, list[tuple[Path, str]]] = {}
    for paths, target in (
        (source_paths, source_paragraphs),
        (manual_paths, reference_paragraphs),
    ):
        for path in sorted(paths):
            try:
                payload = _proposed_path(root, path, commit_oid, runner)
                paragraphs = _visible_paragraphs(payload)
            except (ContractError, _GitError):
                findings.append(
                    Finding(
                        "RIA-DUPLICATE",
                        path.as_posix(),
                        "duplicate comparison input is unavailable",
                    )
                )
                continue
            for paragraph in paragraphs:
                target.setdefault(paragraph.digest, []).append((path, paragraph.role))

    used: set[tuple[Path, Path, str, str]] = set()
    exception_set = set(exceptions)
    for digest in sorted(source_paragraphs.keys() & reference_paragraphs.keys()):
        sources = source_paragraphs[digest]
        references = reference_paragraphs[digest]
        source_counts = Counter(sources)
        reference_counts = Counter(references)
        for (canonical, canonical_role), source_count in source_counts.items():
            for (
                reference,
                reference_role,
            ), reference_count in reference_counts.items():
                key = (canonical, reference, digest, reference_role)
                if (
                    key in exception_set
                    and canonical_role == reference_role
                    and source_count == 1
                    and reference_count == 1
                ):
                    used.add(key)
                    continue
                findings.append(
                    Finding(
                        "RIA-DUPLICATE",
                        reference.as_posix(),
                        f"duplicates canonical owner {canonical.as_posix()}",
                    )
                )
    for exception in exceptions:
        if exception not in used:
            findings.append(
                Finding(
                    "RIA-DUPLICATE",
                    exception[1].as_posix(),
                    "structural exception has no exact duplicate occurrence",
                )
            )
    return sorted(set(findings))


def _links_in_section(text: str, heading: str, pack_root: Path) -> tuple[Path, ...]:
    heading_match = re.search(rf"(?m)^##[ \t]+{re.escape(heading)}[ \t]*$", text)
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
        return [
            Finding(
                "RIA-SNAPSHOT",
                "snapshotGuard.sourceCommit",
                "source commit is unavailable",
            )
        ]
    ids = guard.get("historicalPackIds")
    if not isinstance(ids, list):
        return [
            Finding(
                "RIA-SNAPSHOT",
                "snapshotGuard.historicalPackIds",
                "historical pack set is malformed",
            )
        ]
    for pack_id in ids:
        if not isinstance(pack_id, str):
            findings.append(
                Finding(
                    "RIA-SNAPSHOT",
                    "snapshotGuard.historicalPackIds",
                    "historical pack ID is invalid",
                )
            )
            continue
        pack_root = Path("docs/90.references") / pack_id
        readme = pack_root / "README.md"
        try:
            baseline_readme = _read_commit_path(
                root.absolute(), source_oid, readme, runner
            )
            members = _links_in_section(
                baseline_readme.decode("utf-8", "strict"), "Report Index", pack_root
            )
        except (ContractError, _GitError, UnicodeDecodeError):
            findings.append(
                Finding(
                    "RIA-SNAPSHOT",
                    readme.as_posix(),
                    "historical pack index is unavailable",
                )
            )
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
                findings.append(
                    Finding(
                        "RIA-SNAPSHOT",
                        path.as_posix(),
                        "protected snapshot is unavailable",
                    )
                )
                continue
            if hashlib.sha256(proposed).digest() != hashlib.sha256(baseline).digest():
                findings.append(
                    Finding(
                        "RIA-SNAPSHOT",
                        path.as_posix(),
                        "protected snapshot bytes differ",
                    )
                )
    return sorted(set(findings))


def _table_mask(text: str, section: str, columns: Sequence[str]) -> str:
    match = re.search(
        rf"(?m)^###[#]?[ \t]+{re.escape(section)}[ \t]*$|^##[ \t]+{re.escape(section)}[ \t]*$",
        text,
    )
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
            "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
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
    if len(delimiter) != len(header) or any(
        re.fullmatch(r":?-{3,}:?", item) is None for item in delimiter
    ):
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
    return parse_repository_path(
        "/".join(parts), field="navigationReplacement.destination"
    )


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


def _projection_mask(
    payload: bytes,
    path: Path,
    projection: Mapping[str, object],
    *,
    state: str = "either",
) -> bytes:
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
    literals = projection.get("literalReplacements")
    if literals is not None:
        if not isinstance(literals, list) or not literals:
            raise _GitError("literal replacement projection is malformed")
        for index, replacement in enumerate(literals):
            if not isinstance(replacement, Mapping):
                raise _GitError("literal replacement projection is malformed")
            source = replacement.get("from")
            target = replacement.get("to")
            count = replacement.get("count")
            if (
                not isinstance(source, str)
                or not source
                or not isinstance(target, str)
                or not target
                or source == target
                or not isinstance(count, int)
                or isinstance(count, bool)
                or count < 1
            ):
                raise _GitError("literal replacement projection is malformed")
            source_count = text.count(source)
            target_count = text.count(target)
            expected = {
                "baseline": (count, 0),
                "proposed": (0, count),
            }
            if state in expected:
                if (source_count, target_count) != expected[state]:
                    raise _GitError("literal replacement count differs")
            elif state == "either":
                if (source_count, target_count) not in {
                    (count, 0),
                    (0, count),
                }:
                    raise _GitError("literal replacement count differs")
            else:
                raise _GitError("literal replacement state is invalid")
            marker = f"<RIA-LITERAL-{index}>"
            text = text.replace(source, marker).replace(target, marker)
    return text.encode("utf-8")


def _transition_record(contract: Mapping[str, object]) -> Mapping[str, object] | None:
    records = contract.get("baselineTransitions")
    if (
        isinstance(records, list)
        and len(records) == 1
        and isinstance(records[0], Mapping)
    ):
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


def load_agent_cutover_projections(
    root: Path,
    runner: GitRunner | None,
) -> dict[Path, Mapping[str, object]]:
    authority = root / AGENT_LEGACY_CUTOVER_PATH
    try:
        mode = authority.lstat().st_mode
    except FileNotFoundError:
        return {}
    except OSError as error:
        raise _GitError("agent cutover projection authority is unavailable") from error
    if not stat.S_ISREG(mode):
        raise _GitError("agent cutover projection authority is not regular")
    try:
        payload = read_proposed_regular_file(
            root,
            AGENT_LEGACY_CUTOVER_PATH,
            runner,
        )
        schema_payload = read_proposed_regular_file(
            root,
            AGENT_LEGACY_CUTOVER_SCHEMA_PATH,
            runner,
        )
        if (
            hashlib.sha256(payload).hexdigest() != AGENT_LEGACY_CUTOVER_SHA256
            or hashlib.sha256(schema_payload).hexdigest()
            != AGENT_LEGACY_CUTOVER_SCHEMA_SHA256
        ):
            raise _GitError("agent cutover projection authority digest differs")
        cutover = _decode_json_bytes(
            payload,
            field=AGENT_LEGACY_CUTOVER_PATH.as_posix(),
        )
        cutover_schema = _decode_json_bytes(
            schema_payload,
            field=AGENT_LEGACY_CUTOVER_SCHEMA_PATH.as_posix(),
        )
        Draft202012Validator.check_schema(cutover_schema)
        if any(Draft202012Validator(cutover_schema).iter_errors(cutover)):
            raise _GitError("agent cutover projection authority schema differs")
    except (ContractError, _GitError) as error:
        raise _GitError("agent cutover projection authority is unavailable") from error
    expected = [
        {
            "path": path,
            "from": AGENT_CUTOVER_RETIRED_HUB,
            "to": AGENT_CUTOVER_REPLACEMENT_HUB,
            "count": count,
        }
        for path, count in AGENT_CUTOVER_CURRENT_PATH_COUNTS
    ]
    if (
        cutover.get("schemaVersion") != 1
        or cutover.get("currentOwnerSpec")
        != "docs/03.specs/045-agent-governance-ci-qa-cutover/spec.md"
        or cutover.get("currentAuthorityMigrations") != expected
    ):
        raise _GitError("agent cutover projection authority differs")
    return {
        Path(row["path"]): {
            "path": row["path"],
            "literalReplacements": [
                {
                    "from": row["from"],
                    "to": row["to"],
                    "count": row["count"],
                }
            ],
        }
        for row in expected
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
        context = _build_context(
            root, contract, proposed_oid=proposed_oid, runner=runner
        )
    except (ContractError, _GitError) as error:
        if isinstance(error, ContractError):
            return [
                Finding(
                    "RIA-OVERLAY",
                    error.finding.path,
                    "Current authority is unavailable",
                )
            ]
        return [
            Finding(
                "RIA-OVERLAY",
                REGISTRY_PATH.as_posix(),
                "Current authority is unavailable",
            )
        ]
    baselines = _encoded_baselines(contract)
    projections = _projection_map(contract)
    try:
        cutover_projections = load_agent_cutover_projections(
            root.absolute(),
            runner,
        )
    except _GitError:
        return [
            Finding(
                "RIA-OVERLAY",
                AGENT_LEGACY_CUTOVER_PATH.as_posix(),
                "Current cutover projection authority is unavailable",
            )
        ]
    overlap = set(projections) & set(cutover_projections)
    if overlap:
        return [
            Finding(
                "RIA-OVERLAY",
                min(path.as_posix() for path in overlap),
                "Projection ownership overlaps",
            )
        ]
    projections.update(cutover_projections)
    transition = _transition_record(contract)
    transition_path = (
        Path("docs/90.references") / RESEARCH_PACK_ID / TRANSITION_MEMBER
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
                    findings.append(
                        Finding(
                            "RIA-OVERLAY",
                            path.as_posix(),
                            "transition target bytes differ",
                        )
                    )
                continue
            try:
                if projection is not None:
                    baseline = _projection_mask(
                        baseline,
                        path,
                        projection,
                        state="baseline",
                    )
                    proposed = _projection_mask(
                        proposed,
                        path,
                        projection,
                        state="proposed",
                    )
            except _GitError:
                findings.append(
                    Finding(
                        "RIA-OVERLAY",
                        path.as_posix(),
                        "declared projection is malformed",
                    )
                )
                continue
            if hashlib.sha256(proposed).digest() != hashlib.sha256(baseline).digest():
                findings.append(
                    Finding(
                        "RIA-OVERLAY", path.as_posix(), "protected Current bytes differ"
                    )
                )
    current_paths = set(context.proposed_registry.paths)
    for path, projection in projections.items():
        if path in current_paths:
            continue
        if path.parts[:3] == ("docs", "90.references", "audits"):
            pack_id = AUDIT_PACK_ID
        elif path.parts[:3] == ("docs", "90.references", "research"):
            pack_id = RESEARCH_PACK_ID
        else:
            findings.append(
                Finding(
                    "RIA-OVERLAY",
                    path.as_posix(),
                    "projection path has no Current pack",
                )
            )
            continue
        if pack_id not in baselines:
            # The collection is retired from Current-pack governance, so its
            # historical cutover projection has nothing left to guard here.
            continue
        encoded = baselines[pack_id]
        oid = context.baseline_oids[encoded]
        try:
            baseline = _read_commit_path(root.absolute(), oid, path, runner)
            proposed = _proposed_path(root.absolute(), path, proposed_oid, runner)
            baseline = _projection_mask(
                baseline,
                path,
                projection,
                state="baseline",
            )
            proposed = _projection_mask(
                proposed,
                path,
                projection,
                state="proposed",
            )
        except (ContractError, _GitError):
            findings.append(
                Finding(
                    "RIA-OVERLAY", path.as_posix(), "projected index is unavailable"
                )
            )
            continue
        if hashlib.sha256(proposed).digest() != hashlib.sha256(baseline).digest():
            findings.append(
                Finding("RIA-OVERLAY", path.as_posix(), "protected index bytes differ")
            )
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
        return None, Finding(
            "RIA-TRANSITION", "currentPackBaselines", "baseline map is malformed"
        )
    transitions = contract.get("baselineTransitions")
    settlements = contract.get("baselineSettlements")
    if not isinstance(transitions, list) or not isinstance(settlements, list):
        return None, Finding(
            "RIA-TRANSITION",
            "currentPackBaselines",
            "baseline state is outside the closed FSM",
        )
    if tuple(baselines) == (AUDIT_PACK_ID,):
        if (
            baselines.get(AUDIT_PACK_ID) == CURRENT_ROOT_COMMIT
            and not transitions
            and not settlements
        ):
            return "root", None
        return None, Finding(
            "RIA-TRANSITION",
            "currentPackBaselines",
            "baseline state is outside the closed FSM",
        )
    if (
        tuple(baselines) != (AUDIT_PACK_ID, RESEARCH_PACK_ID)
        or baselines.get(AUDIT_PACK_ID) != CURRENT_ROOT_COMMIT
    ):
        return None, Finding(
            "RIA-TRANSITION",
            "currentPackBaselines",
            "baseline state is outside the closed FSM",
        )
    research = baselines[RESEARCH_PACK_ID]
    if research == CURRENT_ROOT_COMMIT and not transitions and not settlements:
        return "root", None
    if research == CURRENT_ROOT_COMMIT and len(transitions) == 1 and not settlements:
        record = transitions[0]
        if isinstance(record, Mapping) and _record_matches_transition(record):
            return "open", None
        return None, Finding(
            "RIA-TRANSITION", "baselineTransitions", "open transition is malformed"
        )
    if not transitions and len(settlements) == 1:
        record = settlements[0]
        if (
            isinstance(record, Mapping)
            and _record_matches_transition(record, settlement=True)
            and record.get("transitionCommit") == research
            and research != CURRENT_ROOT_COMMIT
        ):
            return "settled", None
    return None, Finding(
        "RIA-TRANSITION",
        "currentPackBaselines",
        "baseline state is outside the closed FSM",
    )


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
    expected = {
        key: value for key, value in settlement.items() if key != "transitionCommit"
    }
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
    *,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> list[Finding]:
    settlement = contract["baselineSettlements"][0]
    assert isinstance(settlement, Mapping)
    transition_commit = settlement.get("transitionCommit")
    try:
        c2_oid = parse_git_sha1(
            transition_commit, field="baselineSettlements.transitionCommit"
        )
        c2_contract = _decode_json_bytes(
            _read_commit_path(root, c2_oid, contract_path, runner),
            field=contract_path.as_posix(),
        )
        _validate_path_fields(c2_contract)
        _validate_schema_at_commit(root, c2_oid, c2_contract, contract_path, runner)
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
        if len(target) != settlement.get("targetByteLength") or hashlib.sha256(
            target
        ).hexdigest() != settlement.get("targetSha256"):
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
        return [
            Finding(
                "RIA-TRANSITION",
                "baselineSettlements",
                "settlement proof chain is invalid",
            )
        ]
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
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    runner: GitRunner | None = None,
) -> list[Finding]:
    state, finding = _fsm_state(contract)
    if finding is not None or state != "settled":
        return [
            Finding(
                "RIA-TRANSITION",
                "baselineSettlements",
                "staged mode requires settled state",
            )
        ]
    settlement = contract["baselineSettlements"][0]
    assert isinstance(settlement, Mapping)
    try:
        c2_oid = parse_git_sha1(
            settlement.get("transitionCommit"),
            field="baselineSettlements.transitionCommit",
        )
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
        if rows != (("M", contract_path.as_posix()),):
            raise _GitError("staged settlement changes paths outside the contract")
    except (ContractError, _GitError):
        return [
            Finding(
                "RIA-TRANSITION",
                contract_path.as_posix(),
                "staged settlement lineage is invalid",
            )
        ]
    return []


def validate_explicit_commit_lineage(
    root: Path,
    contract: Mapping[str, object],
    encoded_commit: object,
    *,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    runner: GitRunner | None = None,
) -> list[Finding]:
    state, finding = _fsm_state(contract)
    if finding is not None or state != "settled":
        return [
            Finding(
                "RIA-TRANSITION",
                "baselineSettlements",
                "explicit mode requires settled state",
            )
        ]
    settlement = contract["baselineSettlements"][0]
    assert isinstance(settlement, Mapping)
    try:
        c3_oid = parse_git_sha1(encoded_commit, field="--commit")
        c2_oid = parse_git_sha1(
            settlement.get("transitionCommit"),
            field="baselineSettlements.transitionCommit",
        )
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
        if rows != (("M", contract_path.as_posix()),):
            raise _GitError("C3 changes paths outside the contract")
    except (ContractError, _GitError):
        return [
            Finding(
                "RIA-TRANSITION", "--commit", "explicit settlement lineage is invalid"
            )
        ]
    return []


def validate_baseline_transitions(
    root: Path,
    contract: Mapping[str, object],
    *,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    staged: bool = False,
    commit: object | None = None,
    require_settled_baselines: bool = False,
    runner: GitRunner | None = None,
) -> list[Finding]:
    if staged and commit is not None:
        return [
            Finding(
                "RIA-TRANSITION",
                "evidenceMode",
                "evidence modes are mutually exclusive",
            )
        ]
    state, finding = _fsm_state(contract)
    if finding is not None:
        return [finding]
    if state == "open" and require_settled_baselines:
        return [
            Finding(
                "RIA-TRANSITION",
                "baselineTransitions",
                "an open transition is not terminal",
            )
        ]
    if staged and state != "settled":
        return [
            Finding(
                "RIA-TRANSITION",
                "baselineSettlements",
                "staged mode requires settled state",
            )
        ]
    if commit is not None and state != "settled":
        return [
            Finding(
                "RIA-TRANSITION",
                "baselineSettlements",
                "explicit mode requires settled state",
            )
        ]
    if state == "root":
        return []
    try:
        proposed_oid = (
            parse_git_sha1(commit, field="--commit") if commit is not None else None
        )
        context = _build_context(
            root, contract, proposed_oid=proposed_oid, runner=runner
        )
    except (ContractError, _GitError):
        return [
            Finding(
                "RIA-TRANSITION",
                REGISTRY_PATH.as_posix(),
                "transition authority is unavailable",
            )
        ]
    findings: list[Finding] = []
    if state == "open":
        transition = contract["baselineTransitions"][0]
        assert isinstance(transition, Mapping)
        research = next(
            (
                pack
                for pack in context.proposed_registry.packs
                if pack.pack_id == RESEARCH_PACK_ID
            ),
            None,
        )
        if research is None or TRANSITION_MEMBER not in research.members:
            findings.append(
                Finding(
                    "RIA-TRANSITION",
                    "baselineTransitions",
                    "transition subject is not a Current member",
                )
            )
        else:
            target_path = (
                Path("docs/90.references") / RESEARCH_PACK_ID / TRANSITION_MEMBER
            )
            target = context.proposed_bytes[target_path]
            if (
                len(target) != transition.get("targetByteLength")
                or hashlib.sha256(target).hexdigest() != transition.get("targetSha256")
                or target == context.baseline_bytes[(CURRENT_ROOT_COMMIT, target_path)]
            ):
                findings.append(
                    Finding(
                        "RIA-TRANSITION",
                        target_path.as_posix(),
                        "transition target bytes differ",
                    )
                )
    elif state == "settled":
        findings.extend(
            _settlement_proof(
                root.absolute(),
                contract,
                context,
                runner,
                contract_path=contract_path,
            )
        )
        if staged:
            findings.extend(
                validate_staged_settlement_lineage(
                    root.absolute(),
                    contract,
                    contract_path=contract_path,
                    runner=runner,
                )
            )
        if commit is not None:
            findings.extend(
                validate_explicit_commit_lineage(
                    root.absolute(),
                    contract,
                    commit,
                    contract_path=contract_path,
                    runner=runner,
                )
            )
    return sorted(set(findings))


def _contract_authority_finding(
    root: Path,
    contract: Mapping[str, object],
    *,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    commit: object | None,
    runner: GitRunner | None,
) -> Finding | None:
    try:
        if commit is None:
            payload = read_proposed_regular_file(root, contract_path, runner)
        else:
            oid = parse_git_sha1(commit, field="--commit")
            payload = _read_commit_path(root, oid, contract_path, runner)
        authoritative = _decode_json_bytes(payload, field=contract_path.as_posix())
        if authoritative != dict(contract):
            raise _GitError("contract mapping differs from proposed authority")
    except (ContractError, _GitError):
        return Finding(
            "RIA-BOUNDARY",
            contract_path.as_posix(),
            "proposed contract authority is unavailable",
        )
    return None


def validate_reference_architecture(
    root: Path,
    contract: Mapping[str, object],
    *,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    staged: bool = False,
    commit: object | None = None,
    require_settled_baselines: bool = False,
    runner: GitRunner | None = None,
) -> list[Finding]:
    """Validate schema-v2 snapshots, Current overlays, and baseline lineage."""

    if staged and commit is not None:
        return [
            Finding(
                "RIA-TRANSITION",
                "evidenceMode",
                "evidence modes are mutually exclusive",
            )
        ]
    try:
        normalized_contract_path = normalize_contract_path(root, contract_path)
    except ContractError as error:
        return [error.finding]
    authority = _contract_authority_finding(
        root.absolute(),
        contract,
        contract_path=normalized_contract_path,
        commit=commit,
        runner=runner,
    )
    if authority is not None:
        return [authority]
    findings = [
        *validate_snapshot_guards(
            root, contract, proposed_commit=commit, runner=runner
        ),
        *validate_overlay_guards(root, contract, proposed_commit=commit, runner=runner),
        *validate_data_assets(root, contract, proposed_commit=commit, runner=runner),
        *validate_generated_assets(
            root, contract, proposed_commit=commit, runner=runner
        ),
        *validate_duplicate_rules(
            root, contract, proposed_commit=commit, runner=runner
        ),
        *validate_baseline_transitions(
            root,
            contract,
            contract_path=normalized_contract_path,
            staged=staged,
            commit=commit,
            require_settled_baselines=require_settled_baselines,
            runner=runner,
        ),
    ]
    return sorted(set(findings))


def _canonical_schema_bytes() -> bytes:
    repository_root = Path(__file__).resolve().parents[1]
    return _read_regular_file(
        repository_root, CANONICAL_SCHEMA_PATH, field="self-test.schema"
    )


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
        },
        "baselineTransitions": [],
        "baselineSettlements": [],
        "mutableIndexProjections": [],
        "dataAssets": [],
        "generatedAssets": [],
        "duplicateRules": {
            "canonicalOwnerRoots": [
                path.as_posix() for path in DUPLICATE_CANONICAL_OWNER_ROOTS
            ],
            "minimumParagraphCharacters": DUPLICATE_MINIMUM_PARAGRAPH_CHARACTERS,
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
