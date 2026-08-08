#!/usr/bin/env python3
"""Validate the repository-static AGQC-003 legacy consumer cutover."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import selectors
import signal
import shutil
import stat
import subprocess
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-legacy-cutover.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-legacy-cutover.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-legacy-cutover.json")
FIXTURE_SHA256 = (
    "c38a84bf4a2abe9c3571df0c0b97125a3ba386c8fc81ae57f5e9b3d565fbce7f"  # pragma: allowlist secret
)

SCHEMA_VERSION = 1
CONTRACT_VERSION = "1.0.0"
OWNER_SPEC = "docs/03.specs/045-agent-governance-ci-qa-cutover/spec.md"
RIA_SNAPSHOT_SOURCE_COMMIT = (
    "8fb9821497aaa93d9ed5fc1a69b60c628b047b47"  # pragma: allowlist secret
)
RESULT_VOCABULARY = ("PASS", "FAIL")
EVIDENCE_VOCABULARY = ("repo-static",)
GIT_CANDIDATE_SOURCE = "git-ls-files-z-cached"
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
RESOURCE_LIMITS = {
    "gitTimeoutSeconds": GIT_TIMEOUT_SECONDS,
    "gitCleanupTimeoutSeconds": GIT_CLEANUP_TIMEOUT_SECONDS,
    "gitStdoutBytes": MAX_GIT_STDOUT_BYTES,
    "gitStderrBytes": MAX_GIT_STDERR_BYTES,
    "candidateCount": MAX_CANDIDATES,
    "candidatePathBytes": MAX_CANDIDATE_PATH_BYTES,
    "regularFileBytes": MAX_REGULAR_FILE_BYTES,
    "diagnosticDetailBytes": MAX_DIAGNOSTIC_DETAIL_BYTES,
}
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
REPLACEMENT_SURFACES = (
    "docs/00.agent-governance/contracts/harness-contract.json",
    "docs/00.agent-governance/contracts/harness-contract.schema.json",
    "scripts/validate-agent-harness-semantics.py",
    "tests/fixtures/agent-harness-semantics.json",
    ".github/README.md",
)
HARNESS_CUTOVER = {
    "contractPath": REPLACEMENT_SURFACES[0],
    "schemaPath": REPLACEMENT_SURFACES[1],
    "consumersKey": "consumers",
    "selectedConsumer": {
        "id": "harness-semantics-validator",
        "path": REPLACEMENT_SURFACES[2],
    },
    "retiredConsumerIds": ["role-semantics-validator"],
    "forbiddenTopLevelKeys": ["compatibility"],
}
CURRENT_AUTHORITY_MIGRATIONS = (
    {
        "path": (
            "docs/90.references/research/2026-08-08-wer/README.md"
        ),
        "from": RETIRED_SURFACES[4],
        "to": REPLACEMENT_SURFACES[4],
        "count": 1,
    },
    {
        "path": (
            "docs/90.references/research/2026-08-08-wer/"
            "ci-cd-github-actions-and-qa.md"
        ),
        "from": RETIRED_SURFACES[4],
        "to": REPLACEMENT_SURFACES[4],
        "count": 2,
    },
    {
        "path": (
            "docs/90.references/research/2026-08-08-wer/"
            "source-coverage-and-migration-ledger.md"
        ),
        "from": RETIRED_SURFACES[4],
        "to": REPLACEMENT_SURFACES[4],
        "count": 1,
    },
)
PACKAGE_REFERENCES = (
    CONTRACT_PATH.as_posix(),
    SCHEMA_PATH.as_posix(),
    "scripts/validate-agent-legacy-cutover.py",
    "scripts/validate-links-and-owners.py",
    FIXTURE_PATH.as_posix(),
    "tests/test_validate_agent_legacy_cutover.py",
    "docs/90.references/data/reference-information-architecture.json",
    "docs/90.references/data/reference-information-architecture.schema.json",
    "scripts/reference_information_architecture.py",
    "tests/test_reference_information_architecture.py",
)
MIGRATION_REFERENCES = (
    OWNER_SPEC,
    "docs/00.agent-governance/memory/progress.md",
)
ALLOWED_REFERENCE_COUNTS = (
    (CONTRACT_PATH.as_posix(), (1, 1, 1, 2, 7)),
    (SCHEMA_PATH.as_posix(), (0, 0, 0, 0, 0)),
    ("scripts/validate-agent-legacy-cutover.py", (1, 1, 1, 1, 1)),
    ("scripts/validate-links-and-owners.py", (1, 1, 1, 1, 4)),
    (FIXTURE_PATH.as_posix(), (1, 0, 0, 1, 1)),
    ("tests/test_validate_agent_legacy_cutover.py", (1, 0, 1, 0, 0)),
    (
        "docs/90.references/data/reference-information-architecture.json",
        (0, 0, 0, 0, 0),
    ),
    (
        "docs/90.references/data/reference-information-architecture.schema.json",
        (0, 0, 0, 0, 0),
    ),
    ("scripts/reference_information_architecture.py", (0, 0, 0, 0, 1)),
    ("tests/test_reference_information_architecture.py", (0, 0, 0, 0, 4)),
    (OWNER_SPEC, (1, 0, 1, 1, 4)),
    ("docs/00.agent-governance/memory/progress.md", (0, 0, 0, 0, 9)),
)
PROTECTED_EVIDENCE_FILES = (
    {
        "path": "docs/90.references/data/active-corpus-retention-census.json",
        "sha256": "d7052fac94af246d5254052935bc49e4a9070b06cb99160902a7e83dc7aad3e3",  # pragma: allowlist secret
        "evidenceKind": "pinned-activation-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-18",
        "sourceCommit": "9e2ec37f483145b322cf68a2f6e697dcf4fb80e1",  # pragma: allowlist secret
        "retiredReference": RETIRED_SURFACES[3],
        "supersededBy": REPLACEMENT_SURFACES[3],
        "count": 1,
    },
    {
        "path": (
            "docs/90.references/audits/2026-07-05-wea/"
            "sdlc-ci-qa-formatting-automation.md"
        ),
        "sha256": "c81e25e2346241c4ffcb83fb073ba2d7c147541dbfeadd0bdeb21bc13e004bb8",  # pragma: allowlist secret
        "evidenceKind": "pinned-ria-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-05",
        "sourceCommit": RIA_SNAPSHOT_SOURCE_COMMIT,
        "retiredReference": RETIRED_SURFACES[4],
        "supersededBy": REPLACEMENT_SURFACES[4],
        "count": 12,
    },
    {
        "path": (
            "docs/90.references/audits/2026-07-03-wdgh/"
            "workspace-document-governance-hardening-audit.md"
        ),
        "sha256": "16ebdfce8fcb4f2e82cfd47e76962b0509385c30823b3d4ece23c1b130994b4f",  # pragma: allowlist secret
        "evidenceKind": "pinned-ria-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-04",
        "sourceCommit": RIA_SNAPSHOT_SOURCE_COMMIT,
        "retiredReference": RETIRED_SURFACES[4],
        "supersededBy": REPLACEMENT_SURFACES[4],
        "count": 2,
    },
    {
        "path": (
            "docs/90.references/audits/2026-07-04-wdcn/"
            "workspace-document-contract-normalization-audit.md"
        ),
        "sha256": "bfa40f0f7e918df9dfaf0c44e5098e581a38969b7417bed2ab7fdabbdad80913",  # pragma: allowlist secret
        "evidenceKind": "pinned-ria-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-04",
        "sourceCommit": RIA_SNAPSHOT_SOURCE_COMMIT,
        "retiredReference": RETIRED_SURFACES[4],
        "supersededBy": REPLACEMENT_SURFACES[4],
        "count": 3,
    },
)
TERMINAL_STATUSES = (
    "archived",
    "cancelled",
    "closed",
    "complete",
    "completed",
    "done",
    "rejected",
    "retired",
    "superseded",
)
EXCLUDED_ROOTS = (
    ".agent-work",
    ".git",
    ".pytest_cache",
    ".superpowers",
    ".venv",
    ".worktrees",
    "__pycache__",
    "node_modules",
)
ALWAYS_ACTIVE_PREFIXES = (
    ".agents/",
    ".claude/",
    ".codex/",
    ".gemini/",
    ".github/",
    "docs/00.agent-governance/",
    "scripts/",
    "tests/",
)
ALWAYS_ACTIVE_FILES = (
    ".pre-commit-config.yaml",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "README.md",
    "pyproject.toml",
)
ALLOWED_INTERNAL_SYMLINKS = (
    (".claude/output-styles", "../.agents/output-styles"),
    (".claude/skills", "../.agents/skills"),
    (".claude/workflows", "../.agents/workflows"),
    (".codex/output-styles", "../.agents/output-styles"),
    (".codex/skills", "../.agents/skills"),
    (".codex/workflows", "../.agents/workflows"),
)
COMMANDS = {
    "selfTest": (
        "python3 scripts/validate-agent-legacy-cutover.py "
        "--root . --self-test"
    ),
    "production": "python3 scripts/validate-agent-legacy-cutover.py --root .",
}
EXIT_CODES = (
    {"code": 0, "result": "PASS"},
    {"code": 1, "result": "FAIL"},
    {"code": 2, "result": "FAIL"},
)
EXPECTED_POSITIVE_CASES = (
    ("clean-cutover", "none"),
    ("terminal-reference-is-evidence", "add-terminal-reference"),
    ("protected-reference-is-evidence", "verify-protected-evidence"),
)
EXPECTED_MUTATION_CASES = (
    ("retained-role-contract", "filesystem", "add-retired-path", "AGQC-LEGACY-RETIRED"),
    ("retained-old-github-hub", "filesystem", "add-retired-path", "AGQC-LEGACY-RETIRED"),
    ("missing-replacement", "filesystem", "remove-replacement", "AGQC-LEGACY-REPLACEMENT"),
    ("stale-active-consumer", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("old-harness-consumer", "filesystem", "select-retired-consumer", "AGQC-LEGACY-HARNESS"),
    ("old-harness-compatibility", "filesystem", "add-harness-compatibility", "AGQC-LEGACY-HARNESS"),
    ("replacement-symlink", "filesystem", "symlink-replacement", "AGQC-LEGACY-INPUT"),
    ("malformed-harness-json", "filesystem", "malform-harness-json", "AGQC-LEGACY-JSON"),
    ("duplicate-harness-json-key", "filesystem", "duplicate-harness-json-key", "AGQC-LEGACY-JSON"),
    ("migration-allowlist-growth", "contract", "add-migration-reference", "AGQC-LEGACY-SCHEMA"),
    ("replacement-path-escape", "contract", "replace-replacement-path", "AGQC-LEGACY-SCHEMA"),
    ("protected-evidence-allowlist-growth", "contract", "add-protected-evidence", "AGQC-LEGACY-SCHEMA"),
    ("active-research-reference", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("accepted-reference-pack-reference", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("protected-data-drift", "filesystem", "mutate-protected-evidence", "AGQC-LEGACY-CONSUMER"),
    ("protected-evidence-missing", "filesystem", "remove-protected-evidence", "AGQC-LEGACY-CONSUMER"),
    ("protected-reference-removal", "filesystem", "replace-protected-reference", "AGQC-LEGACY-CONSUMER"),
    ("digest-pinned-draft-reference", "contract", "replace-protected-evidence", "AGQC-LEGACY-SCHEMA"),
    ("extensionless-active-reference", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("invalid-utf8-reference", "filesystem", "add-invalid-utf8-reference", "AGQC-LEGACY-INPUT"),
    ("allowed-reference-count-drift", "filesystem", "mutate-allowed-reference", "AGQC-LEGACY-CONSUMER"),
    ("current-authority-migration-drift", "contract", "change-current-authority-migration", "AGQC-LEGACY-CONTRACT"),
    ("candidate-source-drift", "contract", "change-candidate-source", "AGQC-LEGACY-SCHEMA"),
    ("resource-limit-drift", "contract", "change-resource-limit", "AGQC-LEGACY-SCHEMA"),
)
STATUS_LINE = re.compile(r"^status\s*:\s*(.*?)\s*$", re.IGNORECASE)
UPDATED_LINE = re.compile(r"^updated\s*:\s*(.*?)\s*$", re.IGNORECASE)


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
    except (json.JSONDecodeError, DuplicateKeyError) as exc:
        fail("AGQC-LEGACY-JSON", f"{source}: {exc}")


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
                if (
                    not stat.S_ISDIR(child_state.st_mode)
                    or not _same_identity(child_state, entry_state)
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
                if (
                    not stat.S_ISDIR(entry_state.st_mode)
                    or not _same_identity(entry_state, child_state)
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
    ) -> bytes | None:
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
            if before.st_size > MAX_REGULAR_FILE_BYTES:
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
            if (
                not stat.S_ISREG(opened.st_mode)
                or not _same_stable_file_state(before, opened)
            ):
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"repository file changed type or identity: {value}",
                )
            if opened.st_size > MAX_REGULAR_FILE_BYTES:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"repository file exceeds the byte limit: {value}",
                )

            chunks: list[bytes] = []
            total = 0
            while True:
                remaining = MAX_REGULAR_FILE_BYTES - total
                chunk = os.read(
                    file_descriptor,
                    min(READ_CHUNK_BYTES, remaining + 1),
                )
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_REGULAR_FILE_BYTES:
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
                final_state.st_size > MAX_REGULAR_FILE_BYTES
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
    ) -> bytes:
        payload = self._payload(
            value,
            read=True,
            allow_declared_symlink=False,
            missing_rule=missing_rule,
        )
        assert payload is not None
        return payload

    def read_text(
        self,
        value: str,
        *,
        missing_rule: str = "AGQC-LEGACY-INPUT",
    ) -> str:
        try:
            return self.read_bytes(value, missing_rule=missing_rule).decode("utf-8")
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
) -> Any:
    return _parse_json(
        reader.read_text(value, missing_rule=missing_rule),
        value,
    )


def _load_contract_documents(
    reader: _RepositoryReader,
) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _load_json_regular(reader, CONTRACT_PATH.as_posix())
    schema = _load_json_regular(reader, SCHEMA_PATH.as_posix())
    if not isinstance(contract, dict) or not isinstance(schema, dict):
        fail("AGQC-LEGACY-JSON", "contract and schema roots must be objects")
    return contract, schema


def load_contract_documents(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load the contract and schema through one bounded repository reader."""

    with _RepositoryReader(root) as reader:
        return _load_contract_documents(reader)


def _schema_error_detail(error: Any) -> str:
    location = "/".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{location}: {error.message}"


def validate_contract_data(
    contract: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, Any]:
    """Validate closed syntax and exact no-growth cutover semantics."""

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes multiple schema exceptions
        fail("AGQC-LEGACY-SCHEMA", f"schema definition is invalid: {exc}")
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        fail("AGQC-LEGACY-SCHEMA", _schema_error_detail(errors[0]))

    if (
        contract["schemaVersion"] != SCHEMA_VERSION
        or contract["contractVersion"] != CONTRACT_VERSION
        or contract["currentOwnerSpec"] != OWNER_SPEC
    ):
        fail("AGQC-LEGACY-CONTRACT", "version or current owner differs")
    if tuple(contract["resultVocabulary"]) != RESULT_VOCABULARY:
        fail("AGQC-LEGACY-CONTRACT", "result vocabulary or order differs")
    if tuple(contract["evidenceVocabulary"]) != EVIDENCE_VOCABULARY:
        fail("AGQC-LEGACY-CONTRACT", "evidence vocabulary differs")
    if tuple(contract["retiredSurfaces"]) != RETIRED_SURFACES:
        fail("AGQC-LEGACY-CONTRACT", "retired surface set or order differs")
    if tuple(contract["replacementSurfaces"]) != REPLACEMENT_SURFACES:
        fail(
            "AGQC-LEGACY-CONTRACT",
            "replacement surface set or order differs",
        )
    if contract["harnessCutover"] != HARNESS_CUTOVER:
        fail("AGQC-LEGACY-CONTRACT", "harness cutover selector differs")
    if contract["currentAuthorityMigrations"] != list(
        CURRENT_AUTHORITY_MIGRATIONS
    ):
        fail(
            "AGQC-LEGACY-CONTRACT",
            "current authority migration set grew, shrank, or changed",
        )

    references = contract["referencePolicy"]
    expected_references = {
        "packageReferences": list(PACKAGE_REFERENCES),
        "migrationReferences": list(MIGRATION_REFERENCES),
        "allowedReferenceCounts": [
            {"path": path, "counts": list(counts)}
            for path, counts in ALLOWED_REFERENCE_COUNTS
        ],
        "protectedEvidenceFiles": copy.deepcopy(
            list(PROTECTED_EVIDENCE_FILES)
        ),
        "terminalStatuses": list(TERMINAL_STATUSES),
    }
    if references != expected_references:
        fail(
            "AGQC-LEGACY-CONTRACT",
            "reference allowlist grew, shrank, or changed order",
        )

    scan = contract["scanPolicy"]
    expected_scan = {
        "root": ".",
        "excludedRoots": list(EXCLUDED_ROOTS),
        "candidateSource": GIT_CANDIDATE_SOURCE,
        "resourceLimits": RESOURCE_LIMITS,
        "alwaysActivePrefixes": list(ALWAYS_ACTIVE_PREFIXES),
        "alwaysActiveFiles": list(ALWAYS_ACTIVE_FILES),
        "allowedInternalSymlinks": [
            {"path": path, "target": target}
            for path, target in ALLOWED_INTERNAL_SYMLINKS
        ],
    }
    if scan != expected_scan:
        fail("AGQC-LEGACY-CONTRACT", "scan policy or symlink set differs")
    if contract["commands"] != COMMANDS:
        fail("AGQC-LEGACY-CONTRACT", "command ownership differs")
    if tuple(contract["exitCodes"]) != EXIT_CODES:
        fail("AGQC-LEGACY-CONTRACT", "stable exit-code mapping differs")
    return contract


def _validate_replacements(
    reader: _RepositoryReader,
    candidates: set[str],
) -> None:
    for value in RETIRED_SURFACES:
        if value in candidates:
            reader.state(value)
            fail("AGQC-LEGACY-RETIRED", f"retired surface remains: {value}")
    for value in REPLACEMENT_SURFACES:
        _require_candidate(
            reader,
            candidates,
            value,
            missing_rule="AGQC-LEGACY-REPLACEMENT",
        )
        reader.read_text(
            value,
            missing_rule="AGQC-LEGACY-REPLACEMENT",
        )
    for value in (
        REPLACEMENT_SURFACES[0],
        REPLACEMENT_SURFACES[1],
        REPLACEMENT_SURFACES[3],
    ):
        _load_json_regular(
            reader,
            value,
            missing_rule="AGQC-LEGACY-REPLACEMENT",
        )


def _all_strings(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            values.append(str(key))
            values.extend(_all_strings(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(_all_strings(child))
    elif isinstance(value, str):
        values.append(value)
    return values


def _validate_harness(reader: _RepositoryReader) -> None:
    harness = _load_json_regular(
        reader,
        REPLACEMENT_SURFACES[0],
        missing_rule="AGQC-LEGACY-REPLACEMENT",
    )
    if not isinstance(harness, dict):
        fail("AGQC-LEGACY-HARNESS", "harness contract root must be an object")
    for key in HARNESS_CUTOVER["forbiddenTopLevelKeys"]:
        if key in harness:
            fail(
                "AGQC-LEGACY-HARNESS",
                f"retired harness compatibility owner remains: {key}",
            )
    consumers = harness.get(HARNESS_CUTOVER["consumersKey"])
    if not isinstance(consumers, list) or any(
        not isinstance(row, dict) for row in consumers
    ):
        fail("AGQC-LEGACY-HARNESS", "harness consumers must be an object list")
    expected = HARNESS_CUTOVER["selectedConsumer"]
    selected = [
        row
        for row in consumers
        if row.get("id") == expected["id"]
        and row.get("path") == expected["path"]
    ]
    if len(selected) != 1:
        fail(
            "AGQC-LEGACY-HARNESS",
            "new harness semantics consumer is not selected exactly once",
        )
    retired_ids = set(HARNESS_CUTOVER["retiredConsumerIds"])
    if any(row.get("id") in retired_ids for row in consumers):
        fail("AGQC-LEGACY-HARNESS", "retired harness consumer remains")
    flattened = _all_strings(harness)
    stale = next(
        (
            token
            for token in RETIRED_SURFACES
            if any(token in value for value in flattened)
        ),
        None,
    )
    if stale is not None:
        fail(
            "AGQC-LEGACY-HARNESS",
            f"harness contract retains retired token: {stale}",
        )


def _under_prefix(value: str, prefix: str) -> bool:
    return value == prefix or value.startswith(prefix + "/")


def _is_terminal_document(text: str) -> bool:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration:
        return False
    statuses: list[str] = []
    for line in lines[1:end]:
        match = STATUS_LINE.fullmatch(line)
        if match is not None:
            value = match.group(1).split("#", 1)[0].strip().strip("'\"")
            statuses.append(value.casefold())
    return len(statuses) == 1 and statuses[0] in TERMINAL_STATUSES


def _is_verified_protected_evidence(
    raw: bytes,
    text: str,
    record: dict[str, Any],
) -> bool:
    """Accept only a closed superseding relation, never a digest alone."""

    if hashlib.sha256(raw).hexdigest() != record["sha256"]:
        return False
    if (
        record["lifecycleStatus"] != "superseded"
        or record["supersededBy"] not in REPLACEMENT_SURFACES
    ):
        return False
    if record["evidenceKind"] == "pinned-activation-snapshot":
        try:
            snapshot = _parse_json(text, record["path"])
        except ContractError:
            return False
        if not isinstance(snapshot, dict):
            return False
        activation = snapshot.get("activation")
        if not isinstance(activation, dict):
            return False
        if (
            snapshot.get("observedAt") != record["observedAt"]
            or activation.get("activationCommit") != record["sourceCommit"]
        ):
            return False
    elif record["evidenceKind"] == "pinned-ria-snapshot":
        if record["sourceCommit"] != RIA_SNAPSHOT_SOURCE_COMMIT:
            return False
        updated_values = [
            match.group(1).split("#", 1)[0].strip().strip("'\"")
            for line in text.splitlines()
            if (match := UPDATED_LINE.fullmatch(line)) is not None
        ]
        if updated_values != [record["observedAt"]]:
            return False
    else:
        return False
    retired_reference = record["retiredReference"].encode("utf-8")
    if raw.count(retired_reference) != record["count"]:
        return False
    if any(
        token != record["retiredReference"]
        and token.encode("utf-8") in raw
        for token in RETIRED_SURFACES
    ):
        return False
    if record["supersededBy"].encode("utf-8") in raw:
        return False
    return True


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


def _scan_consumers_with_reader(
    reader: _RepositoryReader,
    candidates: tuple[str, ...] | None = None,
) -> tuple[int, int, list[str]]:
    if candidates is None:
        candidates = _repository_candidates(reader)
    allowed_counts = dict(ALLOWED_REFERENCE_COUNTS)
    protected_files = {
        record["path"]: record for record in PROTECTED_EVIDENCE_FILES
    }
    candidate_set = set(candidates)
    for relative in allowed_counts:
        _require_candidate(reader, candidate_set, relative)
    for relative in protected_files:
        _require_candidate(
            reader,
            candidate_set,
            relative,
            missing_rule="AGQC-LEGACY-CONSUMER",
        )
    excluded_roots = set(EXCLUDED_ROOTS)
    scanned = 0
    evidence = 0
    consumers: list[str] = []

    for relative in candidates:
        excluded = any(
            _under_prefix(relative, value) for value in excluded_roots
        )
        raw = reader.candidate_payload(relative, read=not excluded)
        if raw is None or excluded:
            continue
        scanned += 1
        observed_counts = tuple(
            raw.count(token.encode("utf-8"))
            for token in RETIRED_SURFACES
        )
        retired = [
            token
            for token, count in zip(RETIRED_SURFACES, observed_counts)
            if count
        ]
        expected_counts = allowed_counts.get(relative)
        if expected_counts is not None:
            if observed_counts == expected_counts:
                if retired:
                    evidence += 1
            else:
                consumers.append(
                    f"{relative}:allowed-reference-count-drift"
                )
            continue
        protected_record = protected_files.get(relative)
        if protected_record is not None:
            try:
                text = raw.decode("utf-8")
            except UnicodeError as exc:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"protected evidence is not UTF-8 {relative}: {exc}",
                )
            if not _is_verified_protected_evidence(
                raw,
                text,
                protected_record,
            ):
                consumers.append(f"{relative}:protected-evidence-drift")
            else:
                evidence += 1
            continue
        if not retired:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeError as exc:
            fail(
                "AGQC-LEGACY-INPUT",
                f"candidate consumer is not UTF-8 {relative}: {exc}",
            )
        always_active = (
            relative in ALWAYS_ACTIVE_FILES
            or any(
                relative.startswith(prefix)
                for prefix in ALWAYS_ACTIVE_PREFIXES
            )
        )
        if not always_active and _is_terminal_document(text):
            evidence += 1
            continue
        consumers.append(f"{relative}:{retired[0]}")
    return scanned, evidence, consumers


def _scan_consumers(
    root: Path,
    candidates: tuple[str, ...] | None = None,
) -> tuple[int, int, list[str]]:
    with _RepositoryReader(root) as reader:
        return _scan_consumers_with_reader(reader, candidates)


def validate_repository(root: Path) -> dict[str, int]:
    """Validate a completed cutover using repository-static evidence only."""

    with _RepositoryReader(root) as reader:
        candidates = _repository_candidates(reader)
        candidate_set = set(candidates)
        for required in (CONTRACT_PATH.as_posix(), SCHEMA_PATH.as_posix()):
            _require_candidate(reader, candidate_set, required)
        contract, schema = _load_contract_documents(reader)
        validate_contract_data(contract, schema)
        _validate_replacements(reader, candidate_set)
        _validate_harness(reader)
        scanned, evidence, consumers = _scan_consumers_with_reader(
            reader,
            candidates,
        )
        if consumers:
            fail(
                "AGQC-LEGACY-CONSUMER",
                "active consumer retains a retired token: " + consumers[0],
            )
    return {
        "retiredSurfaces": len(RETIRED_SURFACES),
        "replacementSurfaces": len(REPLACEMENT_SURFACES),
        "activeConsumers": len(consumers),
        "scannedFiles": scanned,
        "evidenceReferences": evidence,
    }


def _fixture_target(root: Path, relative: str) -> Path:
    safe = _relative_path(relative)
    current = root
    for part in safe.parts[:-1]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            current.mkdir()
            continue
        except OSError as exc:
            fail(
                "AGQC-LEGACY-FIXTURE",
                f"fixture parent is unavailable {relative}: {exc}",
            )
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            fail(
                "AGQC-LEGACY-FIXTURE",
                f"fixture parent must be a non-symlink directory: {relative}",
            )
    return current / safe.name


def _write_text(root: Path, relative: str, text: str) -> Path:
    path = _fixture_target(root, relative)
    path.write_text(text, encoding="utf-8")
    return path


def _write_bytes(root: Path, relative: str, payload: bytes) -> Path:
    path = _fixture_target(root, relative)
    path.write_bytes(payload)
    return path


def _fixture_regular_file(root: Path, relative: str) -> Path:
    path = root / _relative_path(relative)
    try:
        mode = path.lstat().st_mode
    except OSError:
        mode = None
    if mode is None or stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        fail(
            "AGQC-LEGACY-FIXTURE",
            f"fixture target must be a regular non-symlink file: {relative}",
        )
    return path


def _synthetic_git(target_root: Path, arguments: tuple[str, ...]) -> None:
    if arguments not in (("init", "--quiet"), ("add", "--all")):
        fail("AGQC-LEGACY-FIXTURE", "synthetic Git argv is not allowlisted")
    try:
        completed = subprocess.run(
            [GIT_EXECUTABLE, *arguments],
            cwd=target_root,
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
            env=dict(GIT_ENVIRONMENT),
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        fail("AGQC-LEGACY-FIXTURE", f"synthetic Git setup failed: {exc}")
    if completed.returncode != 0:
        fail("AGQC-LEGACY-FIXTURE", "synthetic Git setup failed")


def _create_baseline(
    source_reader: _RepositoryReader,
    target_root: Path,
) -> None:
    for relative in dict.fromkeys(PACKAGE_REFERENCES + MIGRATION_REFERENCES):
        _write_bytes(target_root, relative, source_reader.read_bytes(relative))
    for record in PROTECTED_EVIDENCE_FILES:
        relative = record["path"]
        _write_bytes(target_root, relative, source_reader.read_bytes(relative))
    _write_text(
        target_root,
        REPLACEMENT_SURFACES[0],
        json.dumps(
            {
                "consumers": [
                    {
                        "id": HARNESS_CUTOVER["selectedConsumer"]["id"],
                        "path": HARNESS_CUTOVER["selectedConsumer"]["path"],
                    }
                ]
            },
            indent=2,
        )
        + "\n",
    )
    _write_text(target_root, REPLACEMENT_SURFACES[1], "{}\n")
    _write_text(target_root, REPLACEMENT_SURFACES[2], "replacement\n")
    _write_text(target_root, REPLACEMENT_SURFACES[3], "{}\n")
    _write_text(target_root, REPLACEMENT_SURFACES[4], "replacement hub\n")
    _synthetic_git(target_root, ("init", "--quiet"))
    _synthetic_git(target_root, ("add", "--all"))


def _load_fixture_with_reader(reader: _RepositoryReader) -> dict[str, Any]:
    try:
        raw = reader.read_bytes(FIXTURE_PATH.as_posix())
        text = raw.decode("utf-8")
    except (ContractError, UnicodeError) as exc:
        if isinstance(exc, ContractError):
            raise
        fail("AGQC-LEGACY-FIXTURE", f"fixture is unreadable: {exc}")
    if hashlib.sha256(raw).hexdigest() != FIXTURE_SHA256:
        fail("AGQC-LEGACY-FIXTURE", "fixture bytes differ from the closed set")
    fixture = _parse_json(text, FIXTURE_PATH.as_posix())
    if not isinstance(fixture, dict):
        fail("AGQC-LEGACY-FIXTURE", "fixture root must be an object")
    expected_keys = {"fixtureVersion", "positiveCases", "mutationCases"}
    if set(fixture) != expected_keys or fixture["fixtureVersion"] != 1:
        fail("AGQC-LEGACY-FIXTURE", "fixture keys or version differ")
    positives = tuple(
        (case.get("name"), case.get("mutation", {}).get("kind"))
        for case in fixture["positiveCases"]
        if isinstance(case, dict) and isinstance(case.get("mutation"), dict)
    )
    mutations = tuple(
        (
            case.get("name"),
            case.get("target"),
            case.get("mutation", {}).get("kind"),
            case.get("expectedRule"),
        )
        for case in fixture["mutationCases"]
        if isinstance(case, dict) and isinstance(case.get("mutation"), dict)
    )
    if positives != EXPECTED_POSITIVE_CASES or mutations != EXPECTED_MUTATION_CASES:
        fail("AGQC-LEGACY-FIXTURE", "fixture case set or order differs")
    return fixture


def _load_fixture(root: Path) -> dict[str, Any]:
    with _RepositoryReader(root) as reader:
        return _load_fixture_with_reader(reader)


def _require_self_test_sources(
    reader: _RepositoryReader,
    candidates: tuple[str, ...],
) -> None:
    """Admit every self-test source before its first content read."""

    candidate_set = set(candidates)
    required = dict.fromkeys(
        (
            CONTRACT_PATH.as_posix(),
            SCHEMA_PATH.as_posix(),
            FIXTURE_PATH.as_posix(),
            *PACKAGE_REFERENCES,
            *MIGRATION_REFERENCES,
            *(record["path"] for record in PROTECTED_EVIDENCE_FILES),
        )
    )
    for relative in required:
        _require_candidate(reader, candidate_set, relative)


def _apply_positive(root: Path, kind: str) -> None:
    if kind == "none":
        return
    if kind == "add-terminal-reference":
        _write_text(
            root,
            "docs/04.execution/plans/terminal-evidence.md",
            "---\nstatus: Done\n---\n"
            f"historical: {RETIRED_SURFACES[0]}\n",
        )
        return
    if kind == "verify-protected-evidence":
        if not all(
            (root / PurePosixPath(record["path"])).is_file()
            for record in PROTECTED_EVIDENCE_FILES
        ):
            fail(
                "AGQC-LEGACY-FIXTURE",
                "protected evidence baseline is incomplete",
            )
        return
    fail("AGQC-LEGACY-FIXTURE", f"unknown positive mutation: {kind}")


def _mutate_contract(contract: dict[str, Any], mutation: dict[str, Any]) -> None:
    kind = mutation["kind"]
    if kind == "add-migration-reference":
        contract["referencePolicy"]["migrationReferences"].append(
            mutation["path"]
        )
    elif kind == "replace-replacement-path":
        contract["replacementSurfaces"][mutation["index"]] = mutation["path"]
    elif kind == "add-protected-evidence":
        contract["referencePolicy"]["protectedEvidenceFiles"].append(
            {
                "path": mutation["path"],
                "sha256": mutation["sha256"],
            }
        )
    elif kind == "replace-protected-evidence":
        contract["referencePolicy"]["protectedEvidenceFiles"][0] = {
            "path": mutation["path"],
            "sha256": mutation["sha256"],
            "evidenceKind": "authored-document",
            "lifecycleStatus": mutation["lifecycleStatus"],
            "observedAt": mutation["observedAt"],
            "sourceCommit": mutation["sourceCommit"],
            "retiredReference": mutation["retiredReference"],
            "supersededBy": mutation["supersededBy"],
            "count": mutation["count"],
        }
    elif kind == "change-current-authority-migration":
        contract["currentAuthorityMigrations"][mutation["index"]][
            mutation["field"]
        ] = mutation["value"]
    elif kind == "change-candidate-source":
        contract["scanPolicy"]["candidateSource"] = mutation["value"]
    elif kind == "change-resource-limit":
        contract["scanPolicy"]["resourceLimits"][mutation["field"]] = mutation[
            "value"
        ]
    else:
        fail("AGQC-LEGACY-FIXTURE", f"unknown contract mutation: {kind}")


def _mutate_filesystem(root: Path, mutation: dict[str, Any]) -> None:
    kind = mutation["kind"]
    harness_path = root / PurePosixPath(REPLACEMENT_SURFACES[0])
    if kind == "add-retired-path":
        _write_text(root, mutation["path"], "{}\n")
    elif kind == "remove-replacement":
        _fixture_regular_file(root, mutation["path"]).unlink()
    elif kind == "add-active-reference":
        _write_text(
            root,
            mutation["path"],
            (
                "---\n"
                "title: 'Stale reference fixture'\n"
                "type: content/reference\n"
                f"status: {mutation.get('status', 'active')}\n"
                "owner: platform\n"
                "updated: 2026-07-30\n"
                "---\n\n"
                f"use {RETIRED_SURFACES[0]}\n"
            ),
        )
    elif kind == "mutate-protected-evidence":
        path = _fixture_regular_file(root, mutation["path"])
        path.write_bytes(path.read_bytes() + b"\nprotected evidence drift\n")
    elif kind == "remove-protected-evidence":
        _fixture_regular_file(root, mutation["path"]).unlink()
    elif kind == "replace-protected-reference":
        path = _fixture_regular_file(root, mutation["path"])
        raw = path.read_bytes()
        retired = RETIRED_SURFACES[3].encode("utf-8")
        replacement = REPLACEMENT_SURFACES[3].encode("utf-8")
        if raw.count(retired) != 1:
            fail(
                "AGQC-LEGACY-FIXTURE",
                "protected reference fixture count differs",
            )
        path.write_bytes(raw.replace(retired, replacement))
    elif kind == "add-invalid-utf8-reference":
        _write_bytes(
            root,
            mutation["path"],
            RETIRED_SURFACES[0].encode("utf-8") + b"\xff\n",
        )
    elif kind == "mutate-allowed-reference":
        path = _fixture_regular_file(root, mutation["path"])
        path.write_bytes(
            path.read_bytes()
            + b"\n"
            + RETIRED_SURFACES[0].encode("utf-8")
            + b"\n"
        )
    elif kind == "select-retired-consumer":
        _write_text(
            root,
            REPLACEMENT_SURFACES[0],
            json.dumps(
                {
                    "consumers": [
                        {
                            "id": "role-semantics-validator",
                            "path": RETIRED_SURFACES[2],
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
        )
    elif kind == "add-harness-compatibility":
        value = _parse_json(
            harness_path.read_text(encoding="utf-8"),
            REPLACEMENT_SURFACES[0],
        )
        value["compatibility"] = {"removalOwnerSpec": OWNER_SPEC}
        harness_path.write_text(
            json.dumps(value, indent=2) + "\n",
            encoding="utf-8",
        )
    elif kind == "symlink-replacement":
        path = _fixture_regular_file(root, mutation["path"])
        copy_path = path.with_name("replacement-copy" + path.suffix)
        shutil.copyfile(path, copy_path)
        path.unlink()
        path.symlink_to(copy_path.name)
    elif kind == "malform-harness-json":
        harness_path.write_text('{"consumers": [', encoding="utf-8")
    elif kind == "duplicate-harness-json-key":
        harness_path.write_text(
            '{"consumers": [], "consumers": []}\n',
            encoding="utf-8",
        )
    else:
        fail("AGQC-LEGACY-FIXTURE", f"unknown filesystem mutation: {kind}")


def run_self_test(root: Path) -> tuple[int, int]:
    """Execute deterministic fixtures in temporary repositories only."""

    with _RepositoryReader(root) as source_reader:
        candidates = _repository_candidates(source_reader)
        _require_self_test_sources(source_reader, candidates)
        contract, schema = _load_contract_documents(source_reader)
        validate_contract_data(contract, schema)
        fixture = _load_fixture_with_reader(source_reader)

        for case in fixture["positiveCases"]:
            with tempfile.TemporaryDirectory(
                prefix="agent-legacy-cutover-positive-"
            ) as directory:
                target = Path(directory)
                _create_baseline(source_reader, target)
                _apply_positive(target, case["mutation"]["kind"])
                _synthetic_git(target, ("add", "--all"))
                validate_repository(target)

        for case in fixture["mutationCases"]:
            expected = case["expectedRule"]
            try:
                if case["target"] == "contract":
                    mutated = copy.deepcopy(contract)
                    _mutate_contract(mutated, case["mutation"])
                    validate_contract_data(mutated, schema)
                elif case["target"] == "filesystem":
                    with tempfile.TemporaryDirectory(
                        prefix="agent-legacy-cutover-negative-"
                    ) as directory:
                        target = Path(directory)
                        _create_baseline(source_reader, target)
                        _mutate_filesystem(target, case["mutation"])
                        _synthetic_git(target, ("add", "--all"))
                        validate_repository(target)
                else:
                    fail(
                        "AGQC-LEGACY-FIXTURE",
                        f"unknown mutation target: {case['target']}",
                    )
            except ContractError as exc:
                if exc.rule_id != expected:
                    fail(
                        "AGQC-LEGACY-FIXTURE",
                        f"{case['name']}: expected {expected}, got {exc.rule_id}",
                    )
            else:
                fail(
                    "AGQC-LEGACY-FIXTURE",
                    f"{case['name']}: mutation was accepted",
                )
    return len(fixture["positiveCases"]), len(fixture["mutationCases"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            positive_count, mutation_count = run_self_test(args.root)
            print(
                "[PASS] agent legacy cutover self-test passed: "
                f"positive_cases={positive_count} "
                f"mutation_cases={mutation_count}"
            )
            return 0
        counts = validate_repository(args.root)
        print(
            "[PASS] agent legacy cutover validation passed: "
            f"retired_surfaces={counts['retiredSurfaces']} "
            f"replacement_surfaces={counts['replacementSurfaces']} "
            f"active_consumers={counts['activeConsumers']} "
            f"scanned_files={counts['scannedFiles']} "
            f"evidence_references={counts['evidenceReferences']}"
        )
        return 0
    except ContractError as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
