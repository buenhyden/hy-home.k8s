#!/usr/bin/env python3
"""Validate a closed synthetic checkpoint without reading or writing one."""

from __future__ import annotations

import argparse
import copy
import json
import re
import stat
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-checkpoint.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-checkpoint.json")
HARNESS_CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
LOOP_CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-loop-lifecycle.json"
)
MEMORY_README_PATH = PurePosixPath(
    "docs/00.agent-governance/memory/README.md"
)
SPEC_PATH = PurePosixPath(
    "docs/03.specs/043-agent-harness-loop-lifecycle/spec.md"
)
CHECKPOINT_PATH = ".agent-work/checkpoint.json"
CONTRACT_VERSION = "1.0.0"
SCHEMA_VERSION = 1
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
    "durable-long-term": (
        "canonical-sdlc-owner-or-shared-progress-ledger"
    ),
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
    "working-short-term": (
        "canonical-sdlc-owner-or-shared-progress-ledger"
    ),
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
IDENTITY_RULES = {
    "taskId": "AHLL-CP-STALE-TASK",
    "specRef": "AHLL-CP-STALE-SPEC",
    "worktreeId": "AHLL-CP-STALE-WORKTREE",
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
    re.compile(r"(?:^|[^a-z0-9])akia[a-z0-9]{12,}", re.IGNORECASE),
)

MUTATION_RULES = (
    ("duplicate-json-key", "AHLL-CP-DUPLICATE-KEY"),
    ("unknown-checkpoint-field", "AHLL-CP-SCHEMA"),
    ("stale-task", "AHLL-CP-STALE-TASK"),
    ("stale-spec", "AHLL-CP-STALE-SPEC"),
    ("stale-worktree", "AHLL-CP-STALE-WORKTREE"),
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
    ("compaction-retains-transcript", "AHLL-CP-COMPACTION"),
    ("compaction-count-drift", "AHLL-CP-COMPACTION"),
    ("handoff-owner-missing", "AHLL-CP-HANDOFF"),
    ("handoff-evidence-missing", "AHLL-CP-HANDOFF"),
    ("sensitive-credential-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-credential-value", "AHLL-CP-SENSITIVE"),
    ("sensitive-secret-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-token-key", "AHLL-CP-SENSITIVE"),
    ("sensitive-token-value", "AHLL-CP-SENSITIVE"),
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


def _safe_regular_file(root: Path, relative: PurePosixPath) -> Path:
    if relative.is_absolute() or ".." in relative.parts:
        fail(
            "AHLL-CP-PATH",
            "contract input path is unsafe",
            exit_code=2,
        )
    try:
        root = root.resolve(strict=True)
    except OSError:
        fail(
            "AHLL-CP-ROOT",
            "repository root is unavailable",
            exit_code=2,
        )
    current = root
    for part in relative.parts:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except OSError:
            fail(
                "AHLL-CP-MISSING-FILE",
                f"required input {relative} is unavailable",
                exit_code=2,
            )
        if stat.S_ISLNK(mode):
            fail(
                "AHLL-CP-PATH",
                f"required input {relative} crosses a symlink",
                exit_code=2,
            )
    if not stat.S_ISREG(mode):
        fail(
            "AHLL-CP-PATH",
            f"required input {relative} is not a regular file",
            exit_code=2,
        )
    return current


def load_json(root: Path, relative: PurePosixPath) -> Any:
    path = _safe_regular_file(root, relative)
    try:
        size = path.stat().st_size
        if size > MAX_JSON_BYTES:
            fail(
                "AHLL-CP-BOUNDS",
                f"required input {relative} exceeds the read bound",
                exit_code=2,
            )
        text = path.read_text(encoding="utf-8")
    except OSError:
        fail(
            "AHLL-CP-MISSING-FILE",
            f"required input {relative} cannot be read",
            exit_code=2,
        )
    return decode_json_text(text, str(relative))


def _normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def scan_sensitive_payload(value: Any, path: str = "<root>") -> None:
    """Reject prohibited payload keys and secret/conversation-like values."""

    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = _normalized_key(key)
            if (
                normalized not in REDACTION_DECLARATION_KEYS
                and (
                    normalized in FORBIDDEN_KEY_EXACT
                    or any(
                        part in normalized
                        for part in FORBIDDEN_KEY_PARTS
                    )
                )
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
    if (
        any(fragment in lowered for fragment in FORBIDDEN_VALUE_FRAGMENTS)
        or any(pattern.search(value) for pattern in FORBIDDEN_VALUE_PATTERNS)
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
    identity = dict(checkpoint["identity"])
    identity["contractVersion"] = checkpoint["contractVersion"]
    return identity


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

    _validate_freshness(checkpoint, repository_state)

    checkpoint_state = checkpoint["repository"]["loopState"]
    repository_loop_state = repository_state["loopState"]
    if (
        checkpoint_state in TERMINAL_STATES
        or repository_loop_state in TERMINAL_STATES
    ):
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
        key: value
        for key, value in redaction.items()
        if key.endswith("Stored")
    }
    if not stored_flags or any(value is not False for value in stored_flags.values()):
        fail(
            "AHLL-CP-REDACTION",
            "checkpoint permits prohibited stored payloads",
        )
    expected_marker = (
        "[REDACTED-SYNTHETIC]" if checkpoint["synthetic"] else None
    )
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
        or compaction["remainingWorkCount"]
        != len(checkpoint["remainingWork"])
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
        if (
            promotion["evidenceRefs"]
            or promotion["directCanonicalWrite"] is not False
        ):
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
        if (
            record["redactionStatus"] != "PASS"
            or not record["sourceEvidenceRefs"]
        ):
            fail(
                "AHLL-CP-MEMORY-REDACTION",
                f"{memory_id} lacks redacted source evidence",
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
            or (
                expiry["state"] == "expired"
                and expiry["disposition"] == "retain"
            )
        ):
            fail(
                "AHLL-CP-MEMORY-EXPIRY",
                f"{memory_id} expiry disposition is missing or inconsistent",
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
            None
            if expected_disposition == "discard"
            else CANONICAL_OWNERS[memory_id]
        )
        if (
            not archive_gc["reason"]
            or archive_gc["disposition"] != expected_disposition
            or archive_gc["originalOwner"] != CANONICAL_OWNERS[memory_id]
            or archive_gc["currentOrReplacementOwner"]
            != expected_current_owner
            or archive_gc["reviewStatus"] != "approved"
            or not archive_gc["provenanceRefs"]
            or requires_archive_time != (archive_time is not None)
            or (
                archive_time is not None
                and archive_time > checkpoint_updated
            )
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


def _validate_contract_refs(root: Path, checkpoint: dict[str, Any]) -> None:
    harness = load_json(root, HARNESS_CONTRACT_PATH)
    try:
        memory = harness["memory"]
        harness_class_ids = tuple(
            record["id"] for record in memory["classes"]
        )
    except (KeyError, TypeError):
        fail(
            "AHLL-CP-HARNESS-CONTRACT",
            "harness memory declaration is incomplete",
            exit_code=2,
        )
    if (
        memory.get("transientCheckpointPath") != CHECKPOINT_PATH
        or memory.get("executableLifecycleOwner") != SPEC_PATH.as_posix()
        or harness_class_ids != MEMORY_CLASS_IDS
    ):
        fail(
            "AHLL-CP-HARNESS-CONTRACT",
            "checkpoint or memory owner drifted from the harness contract",
        )
    for memory_class in memory["classes"]:
        memory_id = memory_class["id"]
        if (
            memory_class.get("owner") != CANONICAL_OWNERS[memory_id]
            or memory_class.get("authority", {}).get("mode")
            != AUTHORITY_MODES[memory_id]
            or memory_class.get("promotion", {}).get("targetClass")
            != PROMOTION_TARGETS[memory_id]
            or memory_class.get("promotion", {}).get("reviewRequired")
            is not True
            or memory_class.get("sensitivity", {}).get(
                "secretMaterialAllowed"
            )
            is not False
            or memory_class.get("sensitivity", {}).get(
                "rawPromptOrTranscriptAllowed"
            )
            is not False
        ):
            fail(
                "AHLL-CP-HARNESS-CONTRACT",
                f"{memory_id} lifecycle boundary drifted from the harness",
            )

    _safe_regular_file(root, MEMORY_README_PATH)
    gitignore = _safe_regular_file(root, PurePosixPath(".gitignore"))
    try:
        ignored_lines = {
            line.strip()
            for line in gitignore.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
    except OSError:
        fail(
            "AHLL-CP-HARNESS-CONTRACT",
            "root ignore policy cannot be read",
            exit_code=2,
        )
    if ".agent-work/" not in ignored_lines:
        fail(
            "AHLL-CP-HARNESS-CONTRACT",
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
        or boundary.get("implementationOwner") != "AHLL-002"
        or boundary.get("implementationState") != "executable"
        or boundary.get("repositoryStateWins") is not True
        or boundary.get("executableValidationDelegated") is not True
        or tuple(boundary.get("memoryClassIds", ())) != MEMORY_CLASS_IDS
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


def _memory_record(
    checkpoint: dict[str, Any],
    memory_id: str,
) -> dict[str, Any]:
    return next(
        record
        for record in checkpoint["memoryLifecycle"]
        if record["classId"] == memory_id
    )


def apply_duplicate_key_mutation() -> None:
    decode_json_text(
        '{"schemaVersion":1,"schemaVersion":1}',
        "synthetic duplicate-key mutation",
    )
    fail(
        "AHLL-CP-FIXTURE",
        "duplicate-key mutation unexpectedly passed",
    )


def apply_mutation(
    checkpoint: dict[str, Any],
    repository_state: dict[str, Any],
    name: str,
) -> None:
    """Apply one named, deterministic, non-secret negative mutation."""

    identity = repository_state["identity"]
    working = _memory_record(checkpoint, "working-short-term")
    domain = _memory_record(checkpoint, "domain-scoped")
    provider_local = _memory_record(
        checkpoint, "provider-local-auxiliary"
    )

    if name == "unknown-checkpoint-field":
        checkpoint["unexpectedField"] = True
    elif name == "stale-task":
        identity["taskId"] = "AHLL-999-SYNTHETIC"
    elif name == "stale-spec":
        identity["specRef"] = (
            "docs/03.specs/042-provider-native-runtime-and-model-evidence/spec.md"
        )
    elif name == "stale-worktree":
        identity["worktreeId"] = "sha256:" + ("5" * 64)
    elif name == "stale-branch":
        identity["branchRef"] = "refs/heads/synthetic/stale-branch"
    elif name == "stale-base":
        identity["baseRevision"] = "git-sha1:" + ("c" * 40)
    elif name == "stale-head":
        identity["headRevision"] = "git-sha1:" + ("c" * 40)
    elif name == "stale-contract":
        identity["contractVersion"] = "0.9.0"
    elif name == "stale-working-state":
        identity["workingStateDigest"] = "sha256:" + ("6" * 64)
    elif name == "stale-owned-paths":
        identity["ownedPathsDigest"] = "sha256:" + ("7" * 64)
    elif name == "checkpoint-timestamp-order":
        checkpoint["identity"]["createdAtUtc"] = "2026-07-29T00:06:00Z"
    elif name == "checkpoint-timestamp-future":
        checkpoint["identity"]["updatedAtUtc"] = "2026-07-29T00:11:00Z"
    elif name == "checkpoint-timestamp-stale":
        repository_state["observedAtUtc"] = "2026-07-31T00:10:00Z"
    elif name.startswith("terminal-replay-"):
        checkpoint["repository"]["loopState"] = name.removeprefix(
            "terminal-replay-"
        )
    elif name == "completed-work-overflow":
        checkpoint["completedWork"] = [
            f"Bounded synthetic completed item {index}."
            for index in range(13)
        ]
    elif name == "validation-summary-overflow":
        base = checkpoint["validationSummary"][0]
        checkpoint["validationSummary"] = [
            {
                **base,
                "summary": f"Bounded synthetic validation item {index}.",
            }
            for index in range(13)
        ]
    elif name == "next-action-overflow":
        checkpoint["nextAction"] = "x" * 241
    elif name == "atomic-write-disabled":
        checkpoint["atomicWrite"]["required"] = False
    elif name == "atomic-partial-write":
        checkpoint["atomicWrite"]["partialWriteAllowed"] = True
    elif name == "resume-repository-loses":
        checkpoint["resume"]["repositoryStateWins"] = False
    elif name == "resume-conflict-order-drift":
        checkpoint["resume"]["conflictOrder"][0:2] = reversed(
            checkpoint["resume"]["conflictOrder"][0:2]
        )
    elif name == "resume-skips-rediscovery":
        checkpoint["resume"]["rediscoveryRequired"] = False
    elif name == "resume-synthetic-mode-mismatch":
        repository_state["synthetic"] = False
    elif name == "redaction-allows-token":
        checkpoint["redaction"]["tokensStored"] = True
    elif name == "memory-class-order":
        checkpoint["memoryLifecycle"][0], checkpoint["memoryLifecycle"][1] = (
            checkpoint["memoryLifecycle"][1],
            checkpoint["memoryLifecycle"][0],
        )
    elif name == "memory-authority-drift":
        working["authorityMode"] = "advisory-only"
    elif name == "promotion-evidence-missing":
        working["promotion"]["evidenceRefs"] = []
    elif name == "promotion-owner-missing":
        working["promotion"]["canonicalOwner"] = None
    elif name == "promotion-review-missing":
        working["promotion"]["review"]["required"] = False
    elif name == "promotion-redaction-failed":
        working["promotion"]["redactionStatus"] = "FAIL"
    elif name == "promotion-direct-write":
        working["promotion"]["directCanonicalWrite"] = True
    elif name == "provider-local-not-reobserved":
        provider_local["promotion"]["repositoryReobserved"] = False
    elif name == "provider-local-direct-canonical":
        provider_local["promotion"]["directCanonicalWrite"] = True
    elif name == "refresh-revision-stale":
        working["refresh"]["observedRevision"] = "git-sha1:" + ("c" * 40)
    elif name == "refresh-basis-drift":
        working["refresh"]["basis"] = "provider-reobservation"
    elif name == "refresh-due-before-update":
        working["refresh"]["refreshDueAtUtc"] = "2026-07-29T00:04:00Z"
    elif name == "expiry-disposition-missing":
        working["expiry"]["state"] = "expired"
        working["expiry"]["disposition"] = "retain"
    elif name == "archive-gc-provenance-missing":
        working["archiveGc"]["provenanceRefs"] = []
    elif name == "archive-gc-reason-missing":
        working["archiveGc"].pop("reason")
    elif name == "archive-gc-date-missing":
        domain["archiveGc"]["archivedAtUtc"] = None
    elif name == "archive-gc-original-owner-missing":
        working["archiveGc"].pop("originalOwner")
    elif name == "archive-gc-replacement-owner-missing":
        domain["archiveGc"]["currentOrReplacementOwner"] = None
    elif name == "repository-conflict-loses":
        working["conflict"]["repositoryWins"] = False
    elif name == "compaction-retains-transcript":
        checkpoint["compaction"]["fullTranscriptRetained"] = True
    elif name == "compaction-count-drift":
        checkpoint["compaction"]["remainingWorkCount"] += 1
    elif name == "handoff-owner-missing":
        checkpoint["handoff"]["nextOwner"] = None
    elif name == "handoff-evidence-missing":
        checkpoint["handoff"]["evidenceRefs"] = []
    elif name == "sensitive-credential-key":
        checkpoint["credentialValue"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-credential-value":
        checkpoint["nextAction"] = (
            "Credential " + "value: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-secret-key":
        checkpoint["secret"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-token-key":
        checkpoint["token"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-token-value":
        checkpoint["nextAction"] = "Bearer " + "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-auth-path-key":
        checkpoint["authFilePath"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-auth-path-value":
        checkpoint["nextAction"] = (
            "/synthetic/" + "." + "ssh/id_" + "rsa"
        )
    elif name == "sensitive-account-id-key":
        checkpoint["accountIdentifier"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-account-id-value":
        checkpoint["nextAction"] = (
            "Account " + "identifier: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-raw-prompt-key":
        checkpoint["rawPrompt"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-raw-prompt-value":
        checkpoint["nextAction"] = (
            "Raw " + "prompt: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-transcript-key":
        checkpoint["providerTranscript"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-transcript-value":
        checkpoint["nextAction"] = (
            "Full " + "transcript: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-provider-body-key":
        checkpoint["providerResponseBody"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-provider-body-value":
        checkpoint["nextAction"] = (
            "Provider response " + "body: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-stdout-key":
        checkpoint["stdout"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-stdout-value":
        checkpoint["nextAction"] = "stdout: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-stderr-key":
        checkpoint["stderr"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-stderr-value":
        checkpoint["nextAction"] = "stderr: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-shell-history-key":
        checkpoint["shellHistory"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-shell-history-value":
        checkpoint["nextAction"] = (
            "Shell " + "history: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-environment-dump-key":
        checkpoint["environmentDump"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-environment-dump-value":
        checkpoint["nextAction"] = (
            "Environment " + "dump: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-private-diagnostics-key":
        checkpoint["privateDiagnostics"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-private-diagnostics-value":
        checkpoint["nextAction"] = (
            "Private " + "diagnostics: [REDACTED-SYNTHETIC]"
        )
    elif name == "sensitive-user-config-key":
        checkpoint["userConfiguration"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-user-config-value":
        checkpoint["nextAction"] = (
            "User " + "configuration: [REDACTED-SYNTHETIC]"
        )
    else:
        fail(
            "AHLL-CP-FIXTURE",
            "unknown checkpoint mutation",
            exit_code=2,
        )


def _validate_fixture_shape(fixture: Any) -> None:
    if not isinstance(fixture, dict) or set(fixture) != {
        "fixtureVersion",
        "syntheticCheckpoint",
        "repositoryState",
        "negativeMutations",
    }:
        fail(
            "AHLL-CP-FIXTURE",
            "fixture envelope is not closed",
            exit_code=2,
        )
    if fixture["fixtureVersion"] != 1:
        fail(
            "AHLL-CP-FIXTURE",
            "fixture version differs",
            exit_code=2,
        )
    cases = fixture["negativeMutations"]
    if not isinstance(cases, list):
        fail(
            "AHLL-CP-FIXTURE",
            "negative mutation matrix is not a list",
            exit_code=2,
        )
    observed: list[tuple[str, str]] = []
    for case in cases:
        if not isinstance(case, dict) or set(case) != {
            "name",
            "expectedRule",
        }:
            fail(
                "AHLL-CP-FIXTURE",
                "negative mutation case is not closed",
                exit_code=2,
            )
        observed.append((case["name"], case["expectedRule"]))
    if tuple(observed) != MUTATION_RULES:
        fail(
            "AHLL-CP-FIXTURE",
            "negative mutation order, membership, or rule differs",
            exit_code=2,
        )


def validate_fixture(
    root: Path,
    *,
    run_mutations: bool = True,
) -> dict[str, int]:
    """Validate the tracked synthetic fixture and optional negative matrix."""

    root = Path(root)
    fixture = load_json(root, FIXTURE_PATH)
    _validate_fixture_shape(fixture)
    counts = validate_checkpoint(
        root,
        fixture["syntheticCheckpoint"],
        fixture["repositoryState"],
        check_repository_contracts=True,
        require_synthetic=True,
    )
    mutation_count = 0
    if run_mutations:
        for case in fixture["negativeMutations"]:
            name = case["name"]
            try:
                if name == "duplicate-json-key":
                    apply_duplicate_key_mutation()
                else:
                    checkpoint = copy.deepcopy(
                        fixture["syntheticCheckpoint"]
                    )
                    repository_state = copy.deepcopy(
                        fixture["repositoryState"]
                    )
                    apply_mutation(checkpoint, repository_state, name)
                    validate_checkpoint(
                        root,
                        checkpoint,
                        repository_state,
                        check_repository_contracts=False,
                    )
            except CheckpointError as exc:
                if exc.code != case["expectedRule"]:
                    fail(
                        "AHLL-CP-FIXTURE",
                        f"{name} produced the wrong rule",
                        exit_code=2,
                    )
            else:
                fail(
                    "AHLL-CP-FIXTURE",
                    f"{name} unexpectedly passed",
                    exit_code=2,
                )
            mutation_count += 1
    return {**counts, "negativeMutations": mutation_count}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the closed synthetic agent checkpoint and memory "
            "lifecycle contract without reading or writing a real checkpoint."
        )
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve(strict=True)
        counts = validate_fixture(root, run_mutations=args.self_test)
        if args.self_test:
            print(
                "[PASS] agent checkpoint self-test passed: "
                f"mutations={counts['negativeMutations']} "
                f"memory_classes={counts['memoryClasses']} "
                f"validation_records={counts['validationRecords']}"
            )
        else:
            print(
                "[PASS] agent checkpoint validation passed: "
                f"memory_classes={counts['memoryClasses']} "
                f"completed={counts['completedWork']} "
                f"remaining={counts['remainingWork']} "
                f"validation_records={counts['validationRecords']}"
            )
        return 0
    except (CheckpointError, OSError) as exc:
        if isinstance(exc, CheckpointError):
            print(f"{exc.code}: {exc.detail}", file=sys.stderr)
            return exc.exit_code
        print(
            "AHLL-CP-ROOT: repository root is unavailable",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
