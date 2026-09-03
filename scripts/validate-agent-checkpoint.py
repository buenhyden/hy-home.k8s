#!/usr/bin/env python3
"""Validate a closed synthetic checkpoint without reading or writing one."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-checkpoint.schema.json"
)
REGISTRY_PATH = PurePosixPath(".agents/registry.json")
LOOP_CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-loop-lifecycle.json"
)
SPEC_PATH = PurePosixPath("docs/03.specs/0043-agent-harness-loop-lifecycle/spec.md")
CHECKPOINT_PATH = ".agent-work/checkpoint.json"
CONTRACT_VERSION = "1.0.0"
SCHEMA_VERSION = 2
MAX_JSON_BYTES = 2 * 1024 * 1024

MEMORY_CLASS_IDS = (
    "working-short-term",
    "durable-long-term",
    "domain-scoped",
    "provider-local-auxiliary",
)
TERMINAL_STATES = ("completed", "blocked", "escalated", "aborted")
CONFLICT_ORDER = (
    "observed-repository-state",
    "canonical-sdlc-or-domain-owner",
    "reviewed-durable-memory",
    "working-short-term",
    "provider-local-auxiliary",
)
AUTHORITY_MODES = {
    "working-short-term": "temporary-context-only",
    "durable-long-term": "canonical-repository-record",
    "domain-scoped": "canonical-domain-record",
    "provider-local-auxiliary": "advisory-only",
}
CANONICAL_OWNERS = {
    "working-short-term": "active-task-executor",
    "durable-long-term": ("canonical-sdlc-owner-or-shared-progress-ledger"),
    "domain-scoped": "canonical-domain-document-owner",
    "provider-local-auxiliary": "provider-runtime-or-user-local-store",
}
PROMOTION_TARGETS = {
    "working-short-term": "durable-long-term",
    "durable-long-term": None,
    "domain-scoped": "durable-long-term",
    "provider-local-auxiliary": "working-short-term",
}
PROMOTION_OWNERS = {
    "working-short-term": ("canonical-sdlc-owner-or-shared-progress-ledger"),
    "durable-long-term": None,
    "domain-scoped": "canonical-sdlc-owner-or-shared-progress-ledger",
    "provider-local-auxiliary": "active-task-executor",
}
EXPIRY_POLICIES = {
    "working-short-term": ("task-terminal", "discard"),
    "durable-long-term": ("owner-retention", "retain"),
    "domain-scoped": ("superseded-or-invalidated", "archive"),
    "provider-local-auxiliary": (
        "provider-retention",
        "garbage-collect",
    ),
}
REFRESH_BASES = {
    "working-short-term": "task-resume",
    "durable-long-term": "canonical-owner-review",
    "domain-scoped": "domain-owner-review",
    "provider-local-auxiliary": "provider-reobservation",
}
CONFLICT_POLICIES = {
    "working-short-term": ("repository-won", "repository-state"),
    "durable-long-term": (
        "canonical-owner-won",
        "canonical-document-owner",
    ),
    "domain-scoped": (
        "canonical-owner-won",
        "canonical-domain-owner",
    ),
    "provider-local-auxiliary": (
        "repository-won",
        "repository-state",
    ),
}
RETENTION_POLICIES = {
    "working-short-term": "discard-at-task-terminal",
    "durable-long-term": "retain-under-canonical-owner",
    "domain-scoped": "archive-when-superseded-or-invalidated",
    "provider-local-auxiliary": (
        "garbage-collect-under-provider-retention-after-repository-reobservation"
    ),
}
IDENTITY_RULES = {
    "repositoryId": "AHLL-CP-STALE-REPOSITORY",
    "taskId": "AHLL-CP-STALE-TASK",
    "specRef": "AHLL-CP-STALE-SPEC",
    "worktreeId": "AHLL-CP-STALE-WORKTREE",
    "providerSurfaceId": "AHLL-CP-STALE-PROVIDER-SURFACE",
    "providerSessionInstanceDigest": "AHLL-CP-STALE-PROVIDER-SESSION",
    "namespaceDigest": "AHLL-CP-NAMESPACE-DIGEST",
    "writerId": "AHLL-CP-WRITER-ID-COLLISION",
    "writeGeneration": "AHLL-CP-WRITE-GENERATION",
    "previousCheckpointDigest": "AHLL-CP-OVERWRITE",
    "writerClaimDigest": "AHLL-CP-WRITER-CLAIM",
    "branchRef": "AHLL-CP-STALE-BRANCH",
    "baseRevision": "AHLL-CP-STALE-BASE",
    "headRevision": "AHLL-CP-STALE-HEAD",
    "contractVersion": "AHLL-CP-STALE-CONTRACT",
    "workingStateDigest": "AHLL-CP-STALE-WORKING-STATE",
    "ownedPathsDigest": "AHLL-CP-STALE-OWNERSHIP",
}

REDACTION_DECLARATION_KEYS = {
    "secretmaterialstored",
    "credentialsstored",
    "tokensstored",
    "authpathsstored",
    "accountidentifiersstored",
    "rawpromptstored",
    "transcriptstored",
    "providerbodystored",
    "stdoutstored",
    "stderrstored",
    "shellhistorystored",
    "environmentdumpstored",
    "privatediagnosticsstored",
    "userconfigurationstored",
    "rawpromptretained",
    "fulltranscriptretained",
    "providerbodyretained",
}
FORBIDDEN_KEY_EXACT = {
    "auth",
    "authorization",
    "env",
    "environment",
    "password",
    "passwd",
    "passphrase",
    "privatekey",
    "prompt",
    "settings",
    "systemprompt",
    "token",
    "userprompt",
    "usersettings",
}
FORBIDDEN_KEY_PARTS = (
    "credential",
    "secret",
    "token",
    "password",
    "privatekey",
    "apikey",
    "authcontent",
    "authfile",
    "authpath",
    "authcache",
    "accountid",
    "prompt",
    "conversation",
    "transcript",
    "providerbody",
    "providerresponse",
    "requestbody",
    "responsebody",
    "stdout",
    "stderr",
    "shellhistory",
    "environmentdump",
    "envdump",
    "privatediagnostic",
    "userconfig",
    "homeconfig",
)
FORBIDDEN_VALUE_FRAGMENTS = (
    "bearer ",
    "credential value:",
    "secret value:",
    "token value:",
    "account identifier:",
    "ghp_",
    "github_pat_",
    "xoxb-",
    "-----begin private key",
    "raw prompt:",
    "system prompt:",
    "full transcript:",
    "provider response body:",
    "shell history:",
    "environment dump:",
    "private diagnostics:",
    "user configuration:",
    "stdout:",
    "stderr:",
    "/.ssh/",
    "/.aws/credentials",
    "/.kube/config",
    "/.git-credentials",
    "/auth/",
    "/credentials/",
    "auth.json",
    "credentials.json",
    "/.netrc",
    "/.npmrc",
)
FORBIDDEN_VALUE_PATTERNS = (
    re.compile(r"(?:^|[^a-z0-9])sk-[a-z0-9]{8,}", re.IGNORECASE),
    re.compile(
        r"(?:^|[^a-z0-9])sk[-_]proj[-_][a-z0-9_-]{8,}",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:^|[^a-z0-9])gh[pousr]_[a-z0-9_-]{8,256}",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:^|[^a-z0-9])xox[baprs]-[a-z0-9_-]{8,256}",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:^|[^a-z0-9])aiza[a-z0-9_-]{12,}",
        re.IGNORECASE,
    ),
    re.compile(r"(?:^|[^a-z0-9])akia[a-z0-9]{12,}", re.IGNORECASE),
)

MUTATION_RULES = (
    ("duplicate-json-key", "AHLL-CP-DUPLICATE-KEY"),
    ("unknown-checkpoint-field", "AHLL-CP-SCHEMA"),
    ("stale-repository", "AHLL-CP-STALE-REPOSITORY"),
    ("stale-task", "AHLL-CP-STALE-TASK"),
    ("stale-spec", "AHLL-CP-STALE-SPEC"),
    ("stale-worktree", "AHLL-CP-STALE-WORKTREE"),
    ("stale-provider-surface", "AHLL-CP-STALE-PROVIDER-SURFACE"),
    ("stale-provider-session", "AHLL-CP-STALE-PROVIDER-SESSION"),
    ("namespace-digest-drift", "AHLL-CP-NAMESPACE-DIGEST"),
    ("writer-id-collision", "AHLL-CP-WRITER-ID-COLLISION"),
    ("writer-claim-drift", "AHLL-CP-WRITER-CLAIM"),
    ("write-generation-stale", "AHLL-CP-WRITE-GENERATION"),
    ("previous-checkpoint-overwrite", "AHLL-CP-OVERWRITE"),
    ("duplicate-writer", "AHLL-CP-DUPLICATE-WRITER"),
    ("duplicate-resume", "AHLL-CP-DUPLICATE-RESUME"),
    (
        "provider-executor-surface-mismatch",
        "AHLL-CP-PROVIDER-SURFACE",
    ),
    ("stale-branch", "AHLL-CP-STALE-BRANCH"),
    ("stale-base", "AHLL-CP-STALE-BASE"),
    ("stale-head", "AHLL-CP-STALE-HEAD"),
    ("stale-contract", "AHLL-CP-STALE-CONTRACT"),
    ("stale-working-state", "AHLL-CP-STALE-WORKING-STATE"),
    ("stale-owned-paths", "AHLL-CP-STALE-OWNERSHIP"),
    ("checkpoint-timestamp-order", "AHLL-CP-FRESHNESS"),
    ("checkpoint-timestamp-future", "AHLL-CP-FRESHNESS"),
    ("checkpoint-timestamp-stale", "AHLL-CP-FRESHNESS"),
    ("terminal-replay-completed", "AHLL-CP-TERMINAL-REPLAY"),
    ("terminal-replay-blocked", "AHLL-CP-TERMINAL-REPLAY"),
    ("terminal-replay-escalated", "AHLL-CP-TERMINAL-REPLAY"),
    ("terminal-replay-aborted", "AHLL-CP-TERMINAL-REPLAY"),
    ("completed-work-overflow", "AHLL-CP-SCHEMA"),
    ("validation-summary-overflow", "AHLL-CP-SCHEMA"),
    ("next-action-overflow", "AHLL-CP-SCHEMA"),
    ("atomic-write-disabled", "AHLL-CP-ATOMIC-WRITE"),
    ("atomic-partial-write", "AHLL-CP-ATOMIC-WRITE"),
    ("resume-repository-loses", "AHLL-CP-RESUME"),
    ("resume-conflict-order-drift", "AHLL-CP-RESUME"),
    ("resume-skips-rediscovery", "AHLL-CP-RESUME"),
    ("resume-identity-tuple-disabled", "AHLL-CP-SCHEMA"),
    ("resume-single-writer-disabled", "AHLL-CP-SCHEMA"),
    ("resume-duplicate-writer-enabled", "AHLL-CP-SCHEMA"),
    ("resume-duplicate-resume-enabled", "AHLL-CP-SCHEMA"),
    ("resume-overwrite-policy-drift", "AHLL-CP-SCHEMA"),
    ("resume-accepted-identity-drift", "AHLL-CP-SCHEMA"),
    ("resume-synthetic-mode-mismatch", "AHLL-CP-RESUME"),
    ("redaction-allows-token", "AHLL-CP-REDACTION"),
    ("memory-class-order", "AHLL-CP-MEMORY-CLASSES"),
    ("memory-authority-drift", "AHLL-CP-MEMORY-AUTHORITY"),
    ("promotion-evidence-missing", "AHLL-CP-MEMORY-PROMOTION"),
    ("promotion-owner-missing", "AHLL-CP-MEMORY-PROMOTION"),
    ("promotion-review-missing", "AHLL-CP-MEMORY-PROMOTION"),
    ("promotion-redaction-failed", "AHLL-CP-MEMORY-PROMOTION"),
    ("promotion-direct-write", "AHLL-CP-MEMORY-PROMOTION"),
    ("provider-local-not-reobserved", "AHLL-CP-PROVIDER-LOCAL"),
    ("provider-local-direct-canonical", "AHLL-CP-PROVIDER-LOCAL"),
    ("refresh-revision-stale", "AHLL-CP-MEMORY-REFRESH"),
    ("refresh-basis-drift", "AHLL-CP-MEMORY-REFRESH"),
    ("refresh-due-before-update", "AHLL-CP-MEMORY-REFRESH"),
    ("expiry-disposition-missing", "AHLL-CP-MEMORY-EXPIRY"),
    ("archive-gc-provenance-missing", "AHLL-CP-MEMORY-ARCHIVE-GC"),
    ("archive-gc-reason-missing", "AHLL-CP-SCHEMA"),
    ("archive-gc-date-missing", "AHLL-CP-MEMORY-ARCHIVE-GC"),
    ("archive-gc-original-owner-missing", "AHLL-CP-SCHEMA"),
    (
        "archive-gc-replacement-owner-missing",
        "AHLL-CP-MEMORY-ARCHIVE-GC",
    ),
    ("repository-conflict-loses", "AHLL-CP-MEMORY-CONFLICT"),
    ("memory-sensitivity-drift", "AHLL-CP-SCHEMA"),
    ("memory-retention-drift", "AHLL-CP-MEMORY-RETENTION"),
    ("memory-retention-evidence-missing", "AHLL-CP-SCHEMA"),
    ("memory-handoff-owner-missing", "AHLL-CP-MEMORY-HANDOFF"),
    ("memory-handoff-evidence-missing", "AHLL-CP-SCHEMA"),
    ("compaction-retains-transcript", "AHLL-CP-COMPACTION"),
    ("compaction-count-drift", "AHLL-CP-COMPACTION"),
    ("compaction-source-evidence-missing", "AHLL-CP-SCHEMA"),
    ("compaction-replacement-evidence-missing", "AHLL-CP-SCHEMA"),
    ("compaction-identical-digests", "AHLL-CP-COMPACTION"),
    ("compaction-source-owner-missing", "AHLL-CP-SCHEMA"),
    ("compaction-replacement-owner-missing", "AHLL-CP-SCHEMA"),
    ("compaction-review-unapproved", "AHLL-CP-SCHEMA"),
    ("handoff-owner-missing", "AHLL-CP-HANDOFF"),
    ("handoff-evidence-missing", "AHLL-CP-HANDOFF"),
    ("sensitive-credential-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-credential-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-secret-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-token-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-token-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-sk-proj-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-gho-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-xoxp-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-aiza-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-auth-path-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-auth-path-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-account-id-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-account-id-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-raw-prompt-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-raw-prompt-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-transcript-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-transcript-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-provider-body-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-provider-body-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-stdout-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-stdout-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-stderr-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-stderr-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-shell-history-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-shell-history-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-environment-dump-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-environment-dump-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-private-diagnostics-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-private-diagnostics-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-user-config-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-user-config-value", "AHLL-CP-SENSITIVE"),
)


class CheckpointError(ValueError):
    """Typed checkpoint contract failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def fail(code: str, detail: str, *, exit_code: int = 1) -> NoReturn:
    raise CheckpointError(code, detail, exit_code=exit_code)


def _reject_duplicate_pairs(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(
                "AHLL-CP-DUPLICATE-KEY",
                "duplicate JSON key rejected",
                exit_code=2,
            )
        result[key] = value
    return result


def decode_json_text(text: str, source: str = "<memory>") -> Any:
    """Decode JSON with duplicate mapping keys rejected at every depth."""

    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except UnicodeError:
        fail(
            "AHLL-CP-JSON",
            f"{source} is not valid UTF-8 JSON",
            exit_code=2,
        )
    except json.JSONDecodeError:
        fail(
            "AHLL-CP-JSON",
            f"{source} is not valid JSON",
            exit_code=2,
        )


def _read_regular_bytes(root: Path, relative: PurePosixPath) -> bytes:
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        fail(
            "AHLL-CP-PATH",
            "contract input path is unsafe",
            exit_code=2,
        )
    try:
        root_metadata = os.lstat(root)
    except OSError:
        fail(
            "AHLL-CP-ROOT",
            "repository root is unavailable",
            exit_code=2,
        )
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
        fail(
            "AHLL-CP-ROOT",
            "repository root is unavailable",
            exit_code=2,
        )

    descriptors: list[int] = []
    try:
        directory_flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        root_descriptor = os.open(root, directory_flags)
        descriptors.append(root_descriptor)
        opened_root = os.fstat(root_descriptor)
        if (
            not stat.S_ISDIR(opened_root.st_mode)
            or opened_root.st_dev != root_metadata.st_dev
            or opened_root.st_ino != root_metadata.st_ino
        ):
            fail(
                "AHLL-CP-ROOT",
                "repository root identity changed during read",
                exit_code=2,
            )

        parent_descriptor = root_descriptor
        for part in relative.parts[:-1]:
            child_descriptor = os.open(
                part,
                directory_flags,
                dir_fd=parent_descriptor,
            )
            descriptors.append(child_descriptor)
            if not stat.S_ISDIR(os.fstat(child_descriptor).st_mode):
                fail(
                    "AHLL-CP-PATH",
                    f"required input {relative} crosses a non-directory",
                    exit_code=2,
                )
            parent_descriptor = child_descriptor

        file_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        if hasattr(os, "O_NONBLOCK"):
            file_flags |= os.O_NONBLOCK
        file_descriptor = os.open(
            relative.parts[-1],
            file_flags,
            dir_fd=parent_descriptor,
        )
        descriptors.append(file_descriptor)
        opened_file = os.fstat(file_descriptor)
        if not stat.S_ISREG(opened_file.st_mode):
            fail(
                "AHLL-CP-PATH",
                f"required input {relative} is not a regular file",
                exit_code=2,
            )
        if opened_file.st_size > MAX_JSON_BYTES:
            fail(
                "AHLL-CP-BOUNDS",
                f"required input {relative} exceeds the read bound",
                exit_code=2,
            )

        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(file_descriptor, 65536)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_JSON_BYTES:
                fail(
                    "AHLL-CP-BOUNDS",
                    f"required input {relative} exceeds the read bound",
                    exit_code=2,
                )
            chunks.append(chunk)
        return b"".join(chunks)
    except CheckpointError:
        raise
    except OSError:
        fail(
            "AHLL-CP-MISSING-FILE",
            f"required input {relative} cannot be read",
            exit_code=2,
        )
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _read_regular_text(root: Path, relative: PurePosixPath) -> str:
    try:
        return _read_regular_bytes(root, relative).decode("utf-8")
    except UnicodeError:
        fail(
            "AHLL-CP-JSON",
            f"required input {relative} is not valid UTF-8",
            exit_code=2,
        )


def load_json(root: Path, relative: PurePosixPath) -> Any:
    return decode_json_text(_read_regular_text(root, relative), str(relative))


def _normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def scan_sensitive_payload(value: Any, path: str = "<root>") -> None:
    """Reject prohibited payload keys and secret/conversation-like values."""

    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = _normalized_key(key)
            if normalized not in REDACTION_DECLARATION_KEYS and (
                normalized in FORBIDDEN_KEY_EXACT
                or any(part in normalized for part in FORBIDDEN_KEY_PARTS)
            ):
                fail(
                    "AHLL-CP-SENSITIVE",
                    f"prohibited payload key at {path}",
                )
            scan_sensitive_payload(nested, f"{path}/{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            scan_sensitive_payload(nested, f"{path}/{index}")
        return
    if not isinstance(value, str) or value == "[REDACTED-SYNTHETIC]":
        return
    lowered = value.lower().replace("\\", "/")
    if any(fragment in lowered for fragment in FORBIDDEN_VALUE_FRAGMENTS) or any(
        pattern.search(value) for pattern in FORBIDDEN_VALUE_PATTERNS
    ):
        fail(
            "AHLL-CP-SENSITIVE",
            f"prohibited payload value at {path}",
        )


def _schema_errors(instance: Any, schema: Any) -> list[str]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        fail(
            "AHLL-CP-SCHEMA-CONTRACT",
            "checkpoint schema is invalid",
            exit_code=2,
        )
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda item: (
            tuple(str(part) for part in item.absolute_path),
            item.validator or "",
        ),
    )
    return [
        (
            f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'} "
            f"failed {error.validator or 'schema'}"
        )
        for error in errors
    ]


def validate_schema(root: Path, checkpoint: Any) -> None:
    schema = load_json(root, SCHEMA_PATH)
    errors = _schema_errors(checkpoint, schema)
    if errors:
        fail("AHLL-CP-SCHEMA", "; ".join(errors[:8]))


def _validate_atomic_write(checkpoint: dict[str, Any]) -> None:
    atomic = checkpoint["atomicWrite"]
    expected = {
        "required": True,
        "strategy": "same-directory-temp-fsync-replace",
        "targetPath": CHECKPOINT_PATH,
        "partialWriteAllowed": False,
    }
    if atomic != expected:
        fail(
            "AHLL-CP-ATOMIC-WRITE",
            "checkpoint does not require atomic same-directory replacement",
        )


def _checkpoint_identity(checkpoint: dict[str, Any]) -> dict[str, Any]:
    identity = {
        key: value
        for key, value in checkpoint["identity"].items()
        if key not in {"createdAtUtc", "updatedAtUtc"}
    }
    identity["contractVersion"] = checkpoint["contractVersion"]
    return identity


def _digest_values(*values: Any) -> str:
    payload = "\n".join(str(value) for value in values).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _validate_isolation_digests(checkpoint: dict[str, Any]) -> None:
    identity = checkpoint["identity"]
    expected_namespace = _digest_values(
        identity["repositoryId"],
        identity["worktreeId"],
        identity["taskId"],
        identity["providerSurfaceId"],
        identity["providerSessionInstanceDigest"],
    )
    if identity["namespaceDigest"] != expected_namespace:
        fail(
            "AHLL-CP-NAMESPACE-DIGEST",
            "checkpoint namespace digest does not match the identity tuple",
        )
    expected_writer_claim = _digest_values(
        identity["namespaceDigest"],
        identity["writerId"],
        identity["writeGeneration"],
        identity["previousCheckpointDigest"],
        identity["baseRevision"],
        identity["headRevision"],
    )
    if identity["writerClaimDigest"] != expected_writer_claim:
        fail(
            "AHLL-CP-WRITER-CLAIM",
            "checkpoint writer claim digest does not match its inputs",
        )


def _parse_timestamp(value: Any, code: str) -> datetime:
    if not isinstance(value, str):
        fail(code, "synthetic UTC timestamp is missing")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        fail(code, "synthetic UTC timestamp is invalid")
    return parsed


def _validate_freshness(
    checkpoint: dict[str, Any],
    repository_state: dict[str, Any],
) -> None:
    created = _parse_timestamp(
        checkpoint["identity"]["createdAtUtc"],
        "AHLL-CP-FRESHNESS",
    )
    updated = _parse_timestamp(
        checkpoint["identity"]["updatedAtUtc"],
        "AHLL-CP-FRESHNESS",
    )
    observed = _parse_timestamp(
        repository_state["observedAtUtc"],
        "AHLL-CP-FRESHNESS",
    )
    if (
        created > updated
        or updated > observed
        or observed - updated > timedelta(hours=24)
    ):
        fail(
            "AHLL-CP-FRESHNESS",
            "checkpoint freshness ordering is stale or future-dated",
        )


def validate_resume(
    checkpoint: dict[str, Any],
    repository_state: dict[str, Any],
) -> None:
    """Validate repository-first resume and reject every stale identity axis."""

    expected_state_keys = {
        "synthetic",
        "observed",
        "observedAtUtc",
        "identity",
        "loopState",
        "activeWriterCount",
        "activeResumeCount",
    }
    if (
        not isinstance(repository_state, dict)
        or set(repository_state) != expected_state_keys
        or not isinstance(repository_state.get("synthetic"), bool)
        or repository_state.get("observed") is not True
        or not isinstance(repository_state.get("identity"), dict)
        or set(repository_state["identity"]) != set(IDENTITY_RULES)
    ):
        fail(
            "AHLL-CP-RESUME",
            "repository state was not fully rediscovered",
        )
    if checkpoint["synthetic"] is not repository_state["synthetic"]:
        fail(
            "AHLL-CP-RESUME",
            "checkpoint and repository synthetic modes differ",
        )
    if (
        type(repository_state["activeWriterCount"]) is not int
        or repository_state["activeWriterCount"] != 1
    ):
        fail(
            "AHLL-CP-DUPLICATE-WRITER",
            "repository state does not declare exactly one active writer",
        )
    if (
        type(repository_state["activeResumeCount"]) is not int
        or repository_state["activeResumeCount"] != 1
    ):
        fail(
            "AHLL-CP-DUPLICATE-RESUME",
            "repository state does not declare exactly one active resume",
        )

    _validate_freshness(checkpoint, repository_state)
    _validate_isolation_digests(checkpoint)
    if (
        checkpoint["identity"]["providerSurfaceId"]
        != checkpoint["executor"]["providerId"]
    ):
        fail(
            "AHLL-CP-PROVIDER-SURFACE",
            "checkpoint provider surface and executor differ",
        )

    checkpoint_state = checkpoint["repository"]["loopState"]
    repository_loop_state = repository_state["loopState"]
    if checkpoint_state in TERMINAL_STATES or repository_loop_state in TERMINAL_STATES:
        fail(
            "AHLL-CP-TERMINAL-REPLAY",
            "terminal checkpoint state cannot be replayed",
        )

    resume = checkpoint["resume"]
    if (
        resume["repositoryStateWins"] is not True
        or tuple(resume["conflictOrder"]) != CONFLICT_ORDER
        or resume["rediscoveryRequired"] is not True
        or resume["recomputeRemainingWork"] is not True
        or resume["terminalReplayAllowed"] is not False
        or resume["identityTupleRequired"] is not True
        or resume["singleWriterRequired"] is not True
        or resume["duplicateWriterAllowed"] is not False
        or resume["duplicateResumeAllowed"] is not False
        or resume["overwritePolicy"]
        != "compare-generation-and-previous-checkpoint-digest"
        or resume["acceptedIdentity"] != "exact-match-only"
    ):
        fail(
            "AHLL-CP-RESUME",
            "resume does not require repository-first rediscovery",
        )

    observed = repository_state["identity"]
    proposed = _checkpoint_identity(checkpoint)
    for field, rule in IDENTITY_RULES.items():
        if proposed[field] != observed[field]:
            fail(rule, f"checkpoint {field} is stale")
    if checkpoint_state != repository_loop_state:
        fail(
            "AHLL-CP-STALE-WORKING-STATE",
            "checkpoint loop state is stale",
        )


def _validate_redaction(checkpoint: dict[str, Any]) -> None:
    redaction = checkpoint["redaction"]
    if redaction["status"] != "PASS":
        fail("AHLL-CP-REDACTION", "redaction did not pass")
    stored_flags = {
        key: value for key, value in redaction.items() if key.endswith("Stored")
    }
    if not stored_flags or any(value is not False for value in stored_flags.values()):
        fail(
            "AHLL-CP-REDACTION",
            "checkpoint permits prohibited stored payloads",
        )
    expected_marker = "[REDACTED-SYNTHETIC]" if checkpoint["synthetic"] else None
    if redaction["syntheticMarker"] != expected_marker:
        fail(
            "AHLL-CP-REDACTION",
            "redaction marker differs from checkpoint mode",
        )


def _validate_compaction(checkpoint: dict[str, Any]) -> None:
    compaction = checkpoint["compaction"]
    if (
        compaction["state"] != "compacted"
        or compaction["rawPromptRetained"] is not False
        or compaction["fullTranscriptRetained"] is not False
        or compaction["providerBodyRetained"] is not False
        or not compaction["validationEvidenceRefs"]
        or compaction["remainingWorkCount"] != len(checkpoint["remainingWork"])
        or not compaction["source"]["owner"]
        or not compaction["source"]["evidenceRefs"]
        or not compaction["replacement"]["owner"]
        or not compaction["replacement"]["evidenceRefs"]
        or compaction["source"]["digest"] == compaction["replacement"]["digest"]
        or compaction["reviewStatus"] != "approved"
    ):
        fail(
            "AHLL-CP-COMPACTION",
            "compaction is unbounded or lacks continuation evidence",
        )


def _validate_handoff(checkpoint: dict[str, Any]) -> None:
    handoff = checkpoint["handoff"]
    if (
        handoff["state"] != "ready"
        or not handoff["owner"]
        or not handoff["nextOwner"]
        or not handoff["resultSummary"]
        or not handoff["evidenceRefs"]
        or not handoff["nextAction"]
    ):
        fail(
            "AHLL-CP-HANDOFF",
            "handoff lacks bounded result, owner, evidence, or next action",
        )


def _validate_promotion(
    memory_id: str,
    promotion: dict[str, Any],
) -> None:
    if promotion["targetClass"] != PROMOTION_TARGETS[memory_id]:
        fail(
            "AHLL-CP-MEMORY-PROMOTION",
            f"{memory_id} promotion target differs",
        )
    if promotion["canonicalOwner"] != PROMOTION_OWNERS[memory_id]:
        fail(
            "AHLL-CP-MEMORY-PROMOTION",
            f"{memory_id} promotion owner differs",
        )
    review = promotion["review"]
    if (
        review["required"] is not True
        or review["status"] != "approved"
        or not review["reviewer"]
        or not review["evidenceRef"]
        or promotion["redactionStatus"] != "PASS"
    ):
        fail(
            "AHLL-CP-MEMORY-PROMOTION",
            f"{memory_id} promotion lacks review or redaction evidence",
        )

    if memory_id == "durable-long-term":
        if promotion["evidenceRefs"] or promotion["directCanonicalWrite"] is not False:
            fail(
                "AHLL-CP-MEMORY-PROMOTION",
                "durable memory cannot promote implicitly",
            )
        return

    if memory_id == "provider-local-auxiliary":
        if (
            promotion["targetClass"] != "working-short-term"
            or promotion["repositoryReobserved"] is not True
            or promotion["directCanonicalWrite"] is not False
            or promotion["reobservationEvidenceClass"] != "repo-static"
        ):
            fail(
                "AHLL-CP-PROVIDER-LOCAL",
                "provider-local context attempted canonical promotion",
            )
    elif (
        not promotion["evidenceRefs"]
        or promotion["repositoryReobserved"] is not True
        or promotion["reobservationEvidenceClass"] != "repo-static"
        or promotion["directCanonicalWrite"] is not False
    ):
        fail(
            "AHLL-CP-MEMORY-PROMOTION",
            f"{memory_id} promotion lacks reviewed repository evidence",
        )


def validate_memory_lifecycle(checkpoint: dict[str, Any]) -> None:
    """Validate all four memory classes and their executable lifecycle gates."""

    records = checkpoint["memoryLifecycle"]
    memory_ids = tuple(record["classId"] for record in records)
    if memory_ids != MEMORY_CLASS_IDS:
        fail(
            "AHLL-CP-MEMORY-CLASSES",
            "memory class order or membership differs",
        )

    head_revision = checkpoint["identity"]["headRevision"]
    for record in records:
        memory_id = record["classId"]
        if (
            record["authorityMode"] != AUTHORITY_MODES[memory_id]
            or record["canonicalOwner"] != CANONICAL_OWNERS[memory_id]
        ):
            fail(
                "AHLL-CP-MEMORY-AUTHORITY",
                f"{memory_id} authority or canonical owner differs",
            )
        if record["redactionStatus"] != "PASS" or not record["sourceEvidenceRefs"]:
            fail(
                "AHLL-CP-MEMORY-REDACTION",
                f"{memory_id} lacks redacted source evidence",
            )
        sensitivity = record["sensitivity"]
        if (
            sensitivity["classification"] != "non-sensitive-redacted"
            or sensitivity["restrictedContextAllowed"] is not False
            or sensitivity["rawContextAllowed"] is not False
            or sensitivity["providerPayloadAllowed"] is not False
            or sensitivity["reviewStatus"] != "approved"
        ):
            fail(
                "AHLL-CP-MEMORY-SENSITIVITY",
                f"{memory_id} sensitivity boundary differs",
            )

        _validate_promotion(memory_id, record["promotion"])

        refresh = record["refresh"]
        refresh_due = _parse_timestamp(
            refresh["refreshDueAtUtc"],
            "AHLL-CP-MEMORY-REFRESH",
        )
        checkpoint_updated = _parse_timestamp(
            checkpoint["identity"]["updatedAtUtc"],
            "AHLL-CP-MEMORY-REFRESH",
        )
        if (
            refresh["status"] != "refreshed"
            or refresh["basis"] != REFRESH_BASES[memory_id]
            or refresh_due < checkpoint_updated
            or refresh_due - checkpoint_updated > timedelta(days=30)
            or refresh["observedRevision"] != head_revision
            or refresh["canonicalOwner"] != CANONICAL_OWNERS[memory_id]
            or not refresh["evidenceRefs"]
        ):
            fail(
                "AHLL-CP-MEMORY-REFRESH",
                f"{memory_id} refresh evidence is stale or unowned",
            )

        expiry = record["expiry"]
        expected_basis, expected_disposition = EXPIRY_POLICIES[memory_id]
        if (
            expiry["basis"] != expected_basis
            or expiry["disposition"] != expected_disposition
            or expiry["decisionOwner"] != CANONICAL_OWNERS[memory_id]
            or not expiry["evidenceRefs"]
            or (expiry["state"] == "expired" and expiry["disposition"] == "retain")
        ):
            fail(
                "AHLL-CP-MEMORY-EXPIRY",
                f"{memory_id} expiry disposition is missing or inconsistent",
            )
        retention = record["retention"]
        if (
            retention["policy"] != RETENTION_POLICIES[memory_id]
            or retention["canonicalDecisionOwner"] != CANONICAL_OWNERS[memory_id]
            or retention["reviewStatus"] != "approved"
            or not retention["evidenceRefs"]
        ):
            fail(
                "AHLL-CP-MEMORY-RETENTION",
                f"{memory_id} retention decision differs",
            )

        archive_gc = record["archiveGc"]
        archive_time = (
            _parse_timestamp(
                archive_gc["archivedAtUtc"],
                "AHLL-CP-MEMORY-ARCHIVE-GC",
            )
            if archive_gc["archivedAtUtc"] is not None
            else None
        )
        requires_archive_time = expected_disposition in {
            "archive",
            "garbage-collect",
        }
        expected_current_owner = (
            None if expected_disposition == "discard" else CANONICAL_OWNERS[memory_id]
        )
        if (
            not archive_gc["reason"]
            or archive_gc["disposition"] != expected_disposition
            or archive_gc["originalOwner"] != CANONICAL_OWNERS[memory_id]
            or archive_gc["currentOrReplacementOwner"] != expected_current_owner
            or archive_gc["reviewStatus"] != "approved"
            or not archive_gc["provenanceRefs"]
            or requires_archive_time != (archive_time is not None)
            or (archive_time is not None and archive_time > checkpoint_updated)
        ):
            fail(
                "AHLL-CP-MEMORY-ARCHIVE-GC",
                f"{memory_id} archive or GC provenance differs",
            )

        conflict = record["conflict"]
        expected_status, expected_winner = CONFLICT_POLICIES[memory_id]
        if (
            conflict["status"] != expected_status
            or conflict["winner"] != expected_winner
            or conflict["repositoryWins"] is not True
            or not conflict["resolutionEvidenceRefs"]
        ):
            fail(
                "AHLL-CP-MEMORY-CONFLICT",
                f"{memory_id} conflict does not preserve repository authority",
            )
        handoff = record["handoff"]
        if (
            handoff["currentOwner"] != CANONICAL_OWNERS[memory_id]
            or handoff["nextOwner"] != CANONICAL_OWNERS[memory_id]
            or handoff["disposition"] != expected_disposition
            or handoff["reviewStatus"] != "approved"
            or not handoff["evidenceRefs"]
        ):
            fail(
                "AHLL-CP-MEMORY-HANDOFF",
                f"{memory_id} handoff ownership or evidence differs",
            )


def _validate_contract_refs(root: Path, checkpoint: dict[str, Any]) -> None:
    registry = load_json(root, REGISTRY_PATH)
    try:
        provider_rows = registry["providers"]
        role_rows = registry["roles"]
        if not isinstance(provider_rows, list) or not isinstance(role_rows, list):
            raise TypeError
        providers = {row["id"] for row in provider_rows}
        roles = {row["id"]: row["supported_providers"] for row in role_rows}
        if (
            len(providers) != len(provider_rows)
            or len(roles) != len(role_rows)
            or not all(isinstance(provider, str) for provider in providers)
            or not all(
                isinstance(role_id, str)
                and isinstance(supported, list)
                and bool(supported)
                and all(isinstance(provider, str) for provider in supported)
                and len(set(supported)) == len(supported)
                and set(supported).issubset(providers)
                for role_id, supported in roles.items()
            )
        ):
            raise TypeError
    except (KeyError, TypeError):
        fail(
            "AHLL-CP-REGISTRY",
            "agent registry role or provider declaration is invalid",
            exit_code=2,
        )
    executor = checkpoint["executor"]
    if executor["providerId"] not in providers or executor[
        "providerId"
    ] not in roles.get(executor["roleId"], ()):
        fail(
            "AHLL-CP-REGISTRY",
            "checkpoint executor is not supported by the agent registry",
        )
    ignored_lines = {
        line.strip()
        for line in _read_regular_text(
            root,
            PurePosixPath(".gitignore"),
        ).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if ".agent-work/" not in ignored_lines:
        fail(
            "AHLL-CP-LOOP-CONTRACT",
            "transient checkpoint parent is not ignored",
        )

    loop_contract = load_json(root, LOOP_CONTRACT_PATH)
    if (
        loop_contract.get("contractId") != "agent-loop-lifecycle"
        or loop_contract.get("contractVersion") != checkpoint["contractVersion"]
        or loop_contract.get("currentOwner")
        != {
            "path": LOOP_CONTRACT_PATH.as_posix(),
            "contractVersion": checkpoint["contractVersion"],
            "status": "current",
        }
    ):
        fail(
            "AHLL-CP-LOOP-CONTRACT",
            "checkpoint contract version differs from loop lifecycle",
        )
    boundary = loop_contract.get("checkpointBoundary")
    if not isinstance(boundary, dict):
        fail(
            "AHLL-CP-LOOP-CONTRACT",
            "loop lifecycle checkpoint boundary is absent",
        )
    if (
        boundary.get("schemaRef") != SCHEMA_PATH.as_posix()
        or boundary.get("checkpointSchemaVersion") != SCHEMA_VERSION
        or boundary.get("implementationOwner") != "AHLL-002"
        or boundary.get("implementationState") != "executable"
        or boundary.get("repositoryStateWins") is not True
        or boundary.get("executableValidationDelegated") is not True
        or tuple(boundary.get("memoryClassIds", ())) != MEMORY_CLASS_IDS
        or tuple(boundary.get("identityAxes", ()))
        != (
            "repository-id",
            "worktree-id",
            "task-id",
            "provider-surface-id",
            "provider-session-instance-digest",
        )
        or boundary.get("namespaceDigestRequired") is not True
        or boundary.get("singleWriterRequired") is not True
        or boundary.get("duplicateResumeAllowed") is not False
        or boundary.get("overwritePolicy")
        != "compare-generation-and-previous-checkpoint-digest"
        or boundary.get("actualProviderStateReadAllowed") is not False
    ):
        fail(
            "AHLL-CP-LOOP-CONTRACT",
            "loop lifecycle checkpoint boundary differs",
        )
    interfaces = loop_contract.get("interfaces")
    if not isinstance(interfaces, dict):
        fail(
            "AHLL-CP-LOOP-CONTRACT",
            "loop lifecycle interfaces are absent",
        )
    for interface_id in ("writeCheckpoint", "resume", "handoff"):
        definition = interfaces.get(interface_id)
        if (
            not isinstance(definition, dict)
            or definition.get("implementationOwner") != "AHLL-002"
            or definition.get("implementationState") != "executable"
        ):
            fail(
                "AHLL-CP-LOOP-CONTRACT",
                "AHLL-002 loop interface is not executable",
            )


def validate_checkpoint(
    root: Path,
    checkpoint: dict[str, Any],
    repository_state: dict[str, Any],
    *,
    check_repository_contracts: bool = True,
    require_synthetic: bool | None = None,
) -> dict[str, int]:
    """Validate a supplied checkpoint; never read or write the ignored path."""

    root = Path(root)
    scan_sensitive_payload(checkpoint)
    scan_sensitive_payload(repository_state)
    validate_schema(root, checkpoint)

    if (
        checkpoint["schemaVersion"] != SCHEMA_VERSION
        or checkpoint["contractVersion"] != CONTRACT_VERSION
        or checkpoint["checkpointPath"] != CHECKPOINT_PATH
    ):
        fail(
            "AHLL-CP-CONTRACT",
            "checkpoint identity or synthetic fixture boundary differs",
        )
    if (
        require_synthetic is not None
        and checkpoint["synthetic"] is not require_synthetic
    ):
        fail(
            "AHLL-CP-CONTRACT",
            "checkpoint synthetic mode differs from the caller boundary",
        )

    _validate_atomic_write(checkpoint)
    _validate_redaction(checkpoint)
    validate_resume(checkpoint, repository_state)
    validate_memory_lifecycle(checkpoint)
    _validate_compaction(checkpoint)
    _validate_handoff(checkpoint)

    if check_repository_contracts:
        _validate_contract_refs(root, checkpoint)

    return {
        "memoryClasses": len(checkpoint["memoryLifecycle"]),
        "completedWork": len(checkpoint["completedWork"]),
        "remainingWork": len(checkpoint["remainingWork"]),
        "validationRecords": len(checkpoint["validationSummary"]),
    }
