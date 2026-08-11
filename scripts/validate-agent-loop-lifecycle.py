#!/usr/bin/env python3
"""Validate the closed provider-neutral agent loop lifecycle contract."""

from __future__ import annotations

import argparse
import copy
import errno
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-loop-lifecycle.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-loop-lifecycle.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-loop-lifecycle.json")
HARNESS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
CHECKPOINT_SCHEMA_PATH = (
    "docs/00.agent-governance/contracts/agent-checkpoint.schema.json"
)
SPEC_PATH = "docs/03.specs/043-agent-harness-loop-lifecycle/spec.md"

SCHEMA_VERSION = 1
CONTRACT_ID = "agent-loop-lifecycle"
CONTRACT_VERSION = "1.0.0"
MAX_JSON_BYTES = 2 * 1024 * 1024
ACCEPTANCE_CRITERIA = (
    "VAL-AHLL-001",
    "VAL-AHLL-002",
    "VAL-AHLL-003",
    "VAL-AHLL-004",
)
STATE_IDS = (
    "ready",
    "running",
    "validating",
    "retry-assessment",
    "completed",
    "blocked",
    "escalated",
    "aborted",
)
TERMINAL_STATE_IDS = ("completed", "blocked", "escalated", "aborted")
STATE_TERMINALITY = (
    ("ready", False),
    ("running", False),
    ("validating", False),
    ("retry-assessment", False),
    ("completed", True),
    ("blocked", True),
    ("escalated", True),
    ("aborted", True),
)
TRANSITIONS = (
    ("ready", "start", "running"),
    ("running", "submit-for-validation", "validating"),
    ("validating", "validation-pass", "completed"),
    ("validating", "recoverable-failure", "retry-assessment"),
    ("retry-assessment", "retry-approved", "running"),
    ("retry-assessment", "retry-denied", "escalated"),
    ("validating", "blocked-dependency", "blocked"),
    ("validating", "escalation-required", "escalated"),
    ("validating", "explicit-user-stop", "aborted"),
)
SIGNATURE_FIELDS = (
    "validator-result-class",
    "stable-command-id",
    "exit-class",
    "sanitized-diagnostic-code",
    "affected-scope",
    "contract-version",
)
EXCLUDED_SIGNATURE_FIELDS = (
    "timestamps",
    "random-paths",
    "credentials",
    "raw-stdout-stderr",
    "provider-prose",
    "volatile-ids",
)
AUTOMATIC_RECOVERY_ACTION_KINDS = (
    "retry",
    "provider-fallback",
    "model-fallback",
    "tool-fallback",
    "approved-remediation-action",
)
RETRY_EVALUATION_ORDER = (
    "non-retryable-class",
    "second-identical-no-progress-result",
    "same-signature-retry-budget",
    "task-recovery-budget",
    "different-action-requirement",
)
RESULT_IDENTITY_FIELDS = (
    "result-class",
    "normalized-signature-digest",
    "stable-command-id",
    "affected-scope",
)
NONRETRYABLE_FAILURE_CLASSES = (
    "permission-denial",
    "credential-boundary",
    "secret-detection",
    "destructive-live-mutation-risk",
    "explicit-user-stop",
    "contract-schema-corruption",
)
NONRETRYABLE_DISPOSITIONS = (
    ("permission-denial", False, "escalate", "escalated"),
    ("credential-boundary", False, "escalate", "escalated"),
    ("secret-detection", False, "escalate", "escalated"),
    ("destructive-live-mutation-risk", False, "escalate", "escalated"),
    ("explicit-user-stop", False, "stop", "aborted"),
    ("contract-schema-corruption", False, "escalate", "escalated"),
)
PROGRESS_DELTA_CLASSES = (
    "changed-intended-file-state",
    "fewer-failing-assertions",
    "newly-satisfied-criterion",
    "narrowed-reproducible-failure",
    "approved-handoff-artifact",
)
REJECTED_PROGRESS_SIGNALS = (
    "more-tokens",
    "repeated-commands",
    "changed-wording",
    "unverified-fallback",
)
EVENT_REQUIRED_FIELDS = (
    "task-id",
    "role-id",
    "provider-id",
    "state-transition",
    "attempt-counter",
    "recovery-action-counter",
    "signature-digest",
    "progress-delta-class",
    "result-class",
    "validation-evidence-ref",
    "stop-reason",
    "handoff-owner",
    "redaction-result",
)
EVENT_PROHIBITED_FIELDS = (
    "credentials",
    "tokens",
    "account-identifiers",
    "auth-paths-or-content",
    "environment-dumps",
    "shell-history",
    "raw-prompts-or-transcripts",
    "provider-response-bodies",
    "secret-bearing-output",
    "private-diagnostics",
    "user-configuration",
)
MEMORY_CLASS_IDS = (
    "working-short-term",
    "durable-long-term",
    "domain-scoped",
    "provider-local-auxiliary",
)
FEEDBACK_DESTINATIONS = (
    (
        "regression-fixture",
        "tests/fixtures/agent-loop-lifecycle.json",
    ),
    (
        "instruction-clarification",
        "docs/00.agent-governance/rules/agentic.md",
    ),
    (
        "validator-improvement",
        "scripts/validate-agent-loop-lifecycle.py",
    ),
    (
        "role-evaluation-case",
        "docs/03.specs/044-agent-roster-evaluation-and-admission/spec.md",
    ),
    (
        "owned-external-limitation",
        "docs/03.specs/043-agent-harness-loop-lifecycle/tasks.md",
    ),
)
INTERFACE_SIGNATURES = {
    "normalizeFailure": (
        "normalizeFailure(result) -> "
        "{failureClass, signatureDigest, retryable}",
        "AHLL-001",
        "executable",
    ),
    "measureProgress": (
        "measureProgress(before, after) -> {progressed, deltaClasses}",
        "AHLL-001",
        "executable",
    ),
    "decideNext": (
        "decideNext(loopState, budgets, failure, progress) -> "
        "retry | stop | escalate",
        "AHLL-001",
        "executable",
    ),
    "writeCheckpoint": (
        "writeCheckpoint(state) -> redacted transient record",
        "AHLL-002",
        "executable",
    ),
    "resume": (
        "resume(checkpoint, repositoryState) -> validated next state or rejection",
        "AHLL-002",
        "executable",
    ),
    "handoff": (
        "handoff(state) -> bounded result/evidence/limitation/next-owner summary",
        "AHLL-002",
        "executable",
    ),
}

FORBIDDEN_KEY_NAMES = {
    "apikey",
    "token",
    "accesstoken",
    "refreshtoken",
    "secret",
    "secretvalue",
    "password",
    "credential",
    "credentials",
    "credentialvalue",
    "accountidentifier",
    "accountname",
    "authpath",
    "authfilepath",
    "authfilecontent",
    "prompt",
    "prompttext",
    "rawprompt",
    "prompttranscript",
    "transcript",
    "rawtranscript",
    "providerresponse",
    "providerresponsebody",
    "stdout",
    "stderr",
    "rawoutput",
    "environmentdump",
    "shellhistory",
    "privatediagnostic",
    "userconfiguration",
}
SENSITIVE_DECLARATION_KEYS = {
    "rawoutputallowed",
    "rawpayloadallowed",
    "rawtraceprompttranscriptpromotionallowed",
}
SENSITIVE_KEY_PARTS = (
    "stdout",
    "stderr",
    "rawoutput",
    "rawprompt",
    "rawtranscript",
    "prompttext",
    "promptbody",
    "promptcontent",
    "promptpayload",
    "prompttranscript",
    "transcripttext",
    "transcriptbody",
    "transcriptcontent",
    "transcriptpayload",
    "providerresponse",
    "providerbody",
    "requestbody",
    "responsebody",
)
SENSITIVE_KEY_EDGE_TERMS = (
    "prompt",
    "transcript",
    "body",
)
FAILURE_CLASS_PATTERN = re.compile(
    r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
)
SIGNATURE_DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
SENSITIVE_VALUE_PATTERNS = (
    re.compile(
        r"(?i)\b(?:sk|gh[pousr]|xox[baprs])[-_][a-z0-9_-]{8,}"
    ),
    re.compile(r"\bAKIA[A-Z0-9]{12,}\b"),
    re.compile(r"\bAIza[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"(?i)\bbearer\s+\S{8,}"),
    re.compile(r"(?i)-----begin (?:rsa |ec |openssh )?private key-----"),
    re.compile(
        r"(?i)\b(?:api[-_ ]?key|token|secret|password|credential)"
        r"\s*[:=]\s*\S.{7,}"
    ),
    re.compile(r"(?i)\braw (?:prompt|transcript)\s*:\s*\S"),
    re.compile(
        r"(?i)\b(?:auth-file-path|shell-history|environment-dump|"
        r"private-diagnostic-payload)\s*:\s*\S"
    ),
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


class LoopLifecycleError(ValueError):
    """Stable agent-loop lifecycle validation failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        self.code = code
        self.detail = detail
        self.exit_code = exit_code
        super().__init__(f"{code}: {detail}")


def fail(
    code: str, detail: str, *, exit_code: int = 1
) -> NoReturn:
    raise LoopLifecycleError(code, detail, exit_code=exit_code)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def decode_json_text(text: str, source: str = "<memory>") -> Any:
    """Decode JSON while rejecting duplicate object keys at every depth."""

    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except DuplicateKeyError as exc:
        fail("AHLL-DUPLICATE-KEY", f"{source}: {exc}", exit_code=2)
    except json.JSONDecodeError as exc:
        fail("AHLL-JSON", f"{source}: {exc}", exit_code=2)


def _read_regular_bytes(root: Path, relative: PurePosixPath) -> bytes:
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        fail(
            "AHLL-PATH",
            "contract input path is unsafe",
            exit_code=2,
        )
    try:
        root_metadata = os.lstat(root)
    except OSError:
        fail(
            "AHLL-ROOT",
            "repository root is unavailable",
            exit_code=2,
        )
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(
        root_metadata.st_mode
    ):
        fail(
            "AHLL-ROOT",
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
                "AHLL-ROOT",
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
                    "AHLL-PATH",
                    f"required input {relative} crosses a non-directory",
                    exit_code=2,
                )
            parent_descriptor = child_descriptor

        file_flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
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
                "AHLL-PATH",
                f"required input {relative} is not a regular file",
                exit_code=2,
            )
        if opened_file.st_size > MAX_JSON_BYTES:
            fail(
                "AHLL-BOUNDS",
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
                    "AHLL-BOUNDS",
                    f"required input {relative} exceeds the read bound",
                    exit_code=2,
                )
            chunks.append(chunk)
        return b"".join(chunks)
    except LoopLifecycleError:
        raise
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.ENOTDIR}:
            fail(
                "AHLL-PATH",
                f"required input {relative} crosses a symlink or non-directory",
                exit_code=2,
            )
        fail(
            "AHLL-MISSING-FILE",
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
            "AHLL-JSON",
            f"required input {relative} is not valid UTF-8",
            exit_code=2,
        )


def load_json(root: Path, relative: PurePosixPath) -> Any:
    return decode_json_text(_read_regular_text(root, relative), str(relative))


def _normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _is_sensitive_key(normalized: str, nested: Any) -> bool:
    if normalized in SENSITIVE_DECLARATION_KEYS:
        return not isinstance(nested, bool)
    return (
        normalized in FORBIDDEN_KEY_NAMES
        or any(part in normalized for part in SENSITIVE_KEY_PARTS)
        or any(
            normalized.startswith(term) or normalized.endswith(term)
            for term in SENSITIVE_KEY_EDGE_TERMS
        )
    )


def scan_sensitive_payload(
    value: Any, path: tuple[Any, ...] = ()
) -> None:
    """Reject sensitive key names and secret-shaped or conversational values."""

    if isinstance(value, dict):
        for key, nested in value.items():
            location = "/".join(str(part) for part in (*path, key))
            if _is_sensitive_key(_normalized_key(key), nested):
                fail(
                    "AHLL-SENSITIVE",
                    f"{location}: prohibited sensitive key",
                )
            scan_sensitive_payload(nested, (*path, key))
        return
    if isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            scan_sensitive_payload(nested, (*path, index))
        return
    if not isinstance(value, str):
        return
    for pattern in SENSITIVE_VALUE_PATTERNS:
        if pattern.search(value):
            location = "/".join(str(part) for part in path) or "<root>"
            fail(
                "AHLL-SENSITIVE",
                f"{location}: prohibited sensitive or conversational value",
            )


def _schema_errors(instance: Any, schema: Any) -> list[str]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        fail("AHLL-SCHEMA-DEFINITION", str(exc), exit_code=2)
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            error.message,
        ),
    )
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: "
        f"{error.message}"
        for error in errors
    ]


def _validate_schema(root: Path, contract: Any) -> None:
    schema = load_json(root, SCHEMA_PATH)
    errors = _schema_errors(contract, schema)
    if errors:
        fail("AHLL-SCHEMA", "; ".join(errors[:8]))


def _validate_identity(contract: dict[str, Any]) -> None:
    authority = contract["authority"]
    current_owner = contract["currentOwner"]
    if (
        contract["schemaVersion"] != SCHEMA_VERSION
        or contract["contractId"] != CONTRACT_ID
        or contract["contractVersion"] != CONTRACT_VERSION
        or current_owner["path"] != CONTRACT_PATH.as_posix()
        or current_owner["contractVersion"] != CONTRACT_VERSION
        or current_owner["status"] != "current"
        or contract["providerNeutral"] is not True
        or authority["spec"] != SPEC_PATH
        or authority["implementationScope"] != "AHLL-001"
        or tuple(authority["acceptanceCriteria"]) != ACCEPTANCE_CRITERIA
        or authority["checkpointControlsOwner"] != "AHLL-002"
    ):
        fail(
            "AHLL-IDENTITY",
            "ID, current owner, version, scope, authority, or criteria differ",
        )


def _validate_state_machine(contract: dict[str, Any]) -> None:
    machine = contract["stateMachine"]
    observed_states = tuple(
        (state["id"], state["terminal"]) for state in machine["states"]
    )
    observed_transitions = tuple(
        (item["from"], item["event"], item["to"])
        for item in machine["transitions"]
    )
    if (
        machine["initialState"] != "ready"
        or observed_states != STATE_TERMINALITY
        or observed_transitions != TRANSITIONS
        or tuple(machine["automaticTerminalStates"]) != TERMINAL_STATE_IDS
    ):
        fail(
            "AHLL-STATE",
            "closed state order, terminality, or transition graph differs",
        )


def _validate_failure_normalization(contract: dict[str, Any]) -> None:
    policy = contract["failureNormalization"]
    if (
        policy["signatureVersion"] != 1
        or policy["digestAlgorithm"] != "sha256"
        or tuple(policy["signatureFields"]) != SIGNATURE_FIELDS
        or tuple(policy["excludedFields"]) != EXCLUDED_SIGNATURE_FIELDS
        or policy["boundedDiagnosticRequired"] is not True
        or policy["semanticEquivalenceAcrossProviders"] is not True
        or policy["providerEvidenceRetainedSeparately"] is not True
        or policy["rawOutputAllowed"] is not False
    ):
        fail(
            "AHLL-FAILURE-NORMALIZATION",
            "signature fields, exclusions, digest, or evidence boundary differs",
        )


def _validate_retry_policy(contract: dict[str, Any]) -> None:
    policy = contract["retryPolicy"]
    if (
        policy["initialFailureCountsAsRetry"] is not False
        or policy["maxAutomaticRetriesPerSignature"] != 2
        or policy["defaultMaxAutomaticRecoveryActionsPerTask"] != 3
        or policy["effectiveRecoveryLimit"]
        != "minimum-of-present-default-role-task-limits"
        or policy["counterScope"] != "task"
        or policy["signatureRetriesKeyedByNormalizedSignature"] is not True
        or policy["providerFallbackResetsCounters"] is not False
        or policy["modelFallbackResetsCounters"] is not False
        or policy["handoffResetsCounters"] is not False
        or policy["signatureChangeResetsTaskRecoveryCounter"] is not False
        or policy["retryRequiresDifferentAction"] is not True
        or tuple(policy["automaticRecoveryActionKinds"])
        != AUTOMATIC_RECOVERY_ACTION_KINDS
        or policy["budgetExhaustionDecision"] != "escalate"
        or tuple(policy["evaluationOrder"]) != RETRY_EVALUATION_ORDER
    ):
        fail(
            "AHLL-RETRY",
            "retry ceiling, task budget, lower-limit rule, or persistence differs",
        )


def _validate_no_progress_policy(contract: dict[str, Any]) -> None:
    policy = contract["noProgressPolicy"]
    if (
        tuple(policy["resultIdentityFields"]) != RESULT_IDENTITY_FIELDS
        or policy["maxConsecutiveIdenticalResultsWithoutProgress"] != 2
        or policy["secondObservationDecision"] != "escalate"
        or policy["secondObservationState"] != "escalated"
        or policy["consumesRetryBudgetBeforeStop"] is not False
        or policy["progressResetsConsecutiveCount"] is not True
        or policy["providerChangeResetsSequence"] is not False
        or policy["modelChangeResetsSequence"] is not False
    ):
        fail(
            "AHLL-NO-PROGRESS",
            "second identical no-progress result must immediately escalate",
        )


def _validate_nonretryable_classes(contract: dict[str, Any]) -> None:
    observed = tuple(
        (
            item["id"],
            item["retryable"],
            item["decision"],
            item["terminalState"],
        )
        for item in contract["nonRetryableFailureClasses"]
    )
    if observed != NONRETRYABLE_DISPOSITIONS:
        fail(
            "AHLL-NONRETRYABLE",
            "the exact six immediate-stop failure classes must remain closed",
        )


def _validate_progress_policy(contract: dict[str, Any]) -> None:
    policy = contract["progressPolicy"]
    if (
        tuple(policy["allowedDeltaClasses"]) != PROGRESS_DELTA_CLASSES
        or tuple(policy["rejectedSignals"]) != REJECTED_PROGRESS_SIGNALS
        or policy["requiresAtLeastOneAuthorizedDelta"] is not True
        or policy["requiresDeterministicEvidence"] is not True
        or policy["providerProseIsEvidence"] is not False
    ):
        fail(
            "AHLL-PROGRESS",
            "authorized progress deltas or rejected signals differ",
        )


def _validate_event_record(contract: dict[str, Any]) -> None:
    event = contract["eventRecord"]
    if (
        tuple(event["requiredFields"]) != EVENT_REQUIRED_FIELDS
        or tuple(event["prohibitedFields"]) != EVENT_PROHIBITED_FIELDS
        or event["rawPayloadAllowed"] is not False
    ):
        fail(
            "AHLL-EVENT",
            "bounded event record fields or raw-payload boundary differs",
        )


def _validate_checkpoint_boundary(
    root: Path, contract: dict[str, Any]
) -> None:
    boundary = contract["checkpointBoundary"]
    if (
        boundary["schemaRef"] != CHECKPOINT_SCHEMA_PATH
        or boundary["checkpointSchemaVersion"] != 2
        or boundary["implementationOwner"] != "AHLL-002"
        or boundary["implementationState"] != "executable"
        or boundary["repositoryStateWins"] is not True
        or boundary["executableValidationDelegated"] is not True
        or tuple(boundary["memoryClassIds"]) != MEMORY_CLASS_IDS
        or tuple(boundary["identityAxes"])
        != (
            "repository-id",
            "worktree-id",
            "task-id",
            "provider-surface-id",
            "provider-session-instance-digest",
        )
        or boundary["namespaceDigestRequired"] is not True
        or boundary["singleWriterRequired"] is not True
        or boundary["duplicateResumeAllowed"] is not False
        or boundary["overwritePolicy"]
        != "compare-generation-and-previous-checkpoint-digest"
        or boundary["actualProviderStateReadAllowed"] is not False
    ):
        fail(
            "AHLL-CHECKPOINT-BOUNDARY",
            "checkpoint reference, repository authority, or delegation differs",
        )

    checkpoint_schema = load_json(
        root, PurePosixPath(CHECKPOINT_SCHEMA_PATH)
    )
    if (
        checkpoint_schema.get("properties", {})
        .get("schemaVersion", {})
        .get("const")
        != boundary["checkpointSchemaVersion"]
    ):
        fail(
            "AHLL-CHECKPOINT-BOUNDARY",
            "checkpoint schema version differs from the loop boundary",
        )

    harness = load_json(root, HARNESS_PATH)
    try:
        harness_memory_ids = tuple(
            item["id"] for item in harness["memory"]["classes"]
        )
    except (KeyError, TypeError):
        fail(
            "AHLL-CHECKPOINT-BOUNDARY",
            "harness memory class declaration is unreadable",
        )
    if harness_memory_ids != MEMORY_CLASS_IDS:
        fail(
            "AHLL-CHECKPOINT-BOUNDARY",
            "loop checkpoint memory IDs differ from the harness contract",
        )


def _validate_feedback_routing(contract: dict[str, Any]) -> None:
    routing = contract["feedbackRouting"]
    destinations = tuple(
        (destination["id"], destination["ownerRef"])
        for destination in routing["destinations"]
    )
    if (
        routing["trigger"] != "repeated-stable-failure"
        or routing["selection"]
        != "exactly-one-reviewed-destination"
        or routing["reviewRequired"] is not True
        or routing["rawTracePromptTranscriptPromotionAllowed"] is not False
        or destinations != FEEDBACK_DESTINATIONS
    ):
        fail(
            "AHLL-FEEDBACK-ROUTING",
            "trigger, review boundary, or ordered feedback owners differ",
        )


def _validate_interfaces(contract: dict[str, Any]) -> None:
    interfaces = contract["interfaces"]
    observed = {
        name: (
            definition["signature"],
            definition["implementationOwner"],
            definition["implementationState"],
        )
        for name, definition in interfaces.items()
    }
    if observed != INTERFACE_SIGNATURES:
        fail(
            "AHLL-INTERFACE",
            "loop APIs or executable checkpoint ownership differs",
        )


def validate_contract(
    root: Path,
    raw_contract: dict[str, Any] | None = None,
) -> dict[str, int]:
    """Validate schema plus exact lifecycle, retry, failure, and progress rules."""

    root = Path(root).resolve()
    contract = (
        copy.deepcopy(raw_contract)
        if raw_contract is not None
        else load_json(root, CONTRACT_PATH)
    )
    scan_sensitive_payload(contract)
    _validate_schema(root, contract)
    _validate_identity(contract)
    _validate_state_machine(contract)
    _validate_failure_normalization(contract)
    _validate_retry_policy(contract)
    _validate_no_progress_policy(contract)
    _validate_nonretryable_classes(contract)
    _validate_progress_policy(contract)
    _validate_event_record(contract)
    _validate_checkpoint_boundary(root, contract)
    _validate_feedback_routing(contract)
    _validate_interfaces(contract)
    return {
        "states": len(contract["stateMachine"]["states"]),
        "transitions": len(contract["stateMachine"]["transitions"]),
        "nonRetryableFailureClasses": len(
            contract["nonRetryableFailureClasses"]
        ),
        "progressDeltaClasses": len(
            contract["progressPolicy"]["allowedDeltaClasses"]
        ),
        "feedbackDestinations": len(
            contract["feedbackRouting"]["destinations"]
        ),
        "interfaces": len(contract["interfaces"]),
    }


def _bounded_nonnegative_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        fail("AHLL-INPUT", f"{field} must be a non-negative integer")
    return value


def effective_recovery_limit(
    default_limit: int = 3,
    role_limit: int | None = None,
    task_limit: int | None = None,
) -> int:
    """Return the lowest present automatic-recovery ceiling."""

    limits = [_bounded_nonnegative_int(default_limit, "default_limit")]
    for field, value in (
        ("role_limit", role_limit),
        ("task_limit", task_limit),
    ):
        if value is not None:
            limits.append(_bounded_nonnegative_int(value, field))
    return min(limits)


def _stable_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail("AHLL-INPUT", f"{field} must be a non-empty string")
    normalized = " ".join(value.strip().lower().split())
    if "\n" in value or "\r" in value or len(normalized) > 256:
        fail("AHLL-INPUT", f"{field} must be bounded and single-line")
    return normalized


def _canonical_failure_class(value: Any) -> str:
    if not isinstance(value, str):
        fail("AHLL-INPUT", "failureClass must be a non-empty string")
    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value.strip())
    normalized = _stable_text(separated, "failureClass")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    if (
        not 3 <= len(slug) <= 80
        or FAILURE_CLASS_PATTERN.fullmatch(slug) is None
    ):
        fail(
            "AHLL-INPUT",
            "failureClass must normalize to a 3-80 character kebab-case slug",
        )
    return slug


def normalize_failure(
    result: dict[str, Any],
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize stable failure fields into a provider-neutral SHA-256 digest."""

    if not isinstance(result, dict):
        fail("AHLL-INPUT", "failure result must be an object")
    scan_sensitive_payload(result)
    required = (
        "validatorResultClass",
        "stableCommandId",
        "exitClass",
        "sanitizedDiagnosticCode",
        "affectedScope",
        "contractVersion",
    )
    missing = [field for field in required if field not in result]
    if missing:
        fail("AHLL-INPUT", f"failure result missing {missing}")

    affected_scope = result["affectedScope"]
    if isinstance(affected_scope, str):
        scope = [_stable_text(affected_scope, "affectedScope")]
    elif isinstance(affected_scope, list) and affected_scope:
        scope = sorted(
            {
                _stable_text(item, "affectedScope")
                for item in affected_scope
            }
        )
    else:
        fail(
            "AHLL-INPUT",
            "affectedScope must be a string or non-empty string list",
        )

    expected_version = (
        contract["contractVersion"] if contract is not None else CONTRACT_VERSION
    )
    if result["contractVersion"] != expected_version:
        fail(
            "AHLL-INPUT",
            "failure result contractVersion differs from the loop contract",
        )

    signature = {
        "validator-result-class": _stable_text(
            result["validatorResultClass"], "validatorResultClass"
        ),
        "stable-command-id": _stable_text(
            result["stableCommandId"], "stableCommandId"
        ),
        "exit-class": _stable_text(result["exitClass"], "exitClass"),
        "sanitized-diagnostic-code": _stable_text(
            result["sanitizedDiagnosticCode"],
            "sanitizedDiagnosticCode",
        ),
        "affected-scope": scope,
        "contract-version": expected_version,
    }
    encoded = json.dumps(
        signature,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    signature_digest = "sha256:" + hashlib.sha256(encoded).hexdigest()

    failure_class = result.get(
        "failureClass", signature["validator-result-class"]
    )
    failure_class = _canonical_failure_class(failure_class)
    explicitly_retryable = result.get("retryable", True)
    if not isinstance(explicitly_retryable, bool):
        fail("AHLL-INPUT", "retryable must be boolean when present")
    retryable = (
        explicitly_retryable
        and failure_class not in NONRETRYABLE_FAILURE_CLASSES
    )
    return {
        "failureClass": failure_class,
        "signatureDigest": signature_digest,
        "retryable": retryable,
    }


def _string_set(value: Any, field: str) -> set[str]:
    if value is None:
        return set()
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        fail("AHLL-INPUT", f"{field} must be a string list")
    return set(value)


def measure_progress(
    before: dict[str, Any],
    after: dict[str, Any],
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Measure only deterministic, authorized progress dimensions."""

    if not isinstance(before, dict) or not isinstance(after, dict):
        fail("AHLL-INPUT", "progress snapshots must be objects")
    scan_sensitive_payload(before)
    scan_sensitive_payload(after)
    allowed = (
        tuple(contract["progressPolicy"]["allowedDeltaClasses"])
        if contract is not None
        else PROGRESS_DELTA_CLASSES
    )
    deltas: set[str] = set()

    if (
        "intendedFileState" in before
        and "intendedFileState" in after
        and before["intendedFileState"] != after["intendedFileState"]
        and after.get("intendedFileStateAuthorized") is True
    ):
        deltas.add("changed-intended-file-state")

    if (
        "failingAssertionCount" in before
        and "failingAssertionCount" in after
    ):
        previous_failures = _bounded_nonnegative_int(
            before["failingAssertionCount"], "before.failingAssertionCount"
        )
        current_failures = _bounded_nonnegative_int(
            after["failingAssertionCount"], "after.failingAssertionCount"
        )
        if current_failures < previous_failures:
            deltas.add("fewer-failing-assertions")

    before_criteria = _string_set(
        before.get("satisfiedCriteria"), "before.satisfiedCriteria"
    )
    after_criteria = _string_set(
        after.get("satisfiedCriteria"), "after.satisfiedCriteria"
    )
    if after_criteria.difference(before_criteria):
        deltas.add("newly-satisfied-criterion")

    if (
        "reproductionScopeSize" in before
        and "reproductionScopeSize" in after
    ):
        previous_scope = _bounded_nonnegative_int(
            before["reproductionScopeSize"],
            "before.reproductionScopeSize",
        )
        current_scope = _bounded_nonnegative_int(
            after["reproductionScopeSize"],
            "after.reproductionScopeSize",
        )
        if current_scope < previous_scope:
            deltas.add("narrowed-reproducible-failure")

    previous_handoff = before.get("approvedHandoffArtifact")
    current_handoff = after.get("approvedHandoffArtifact")
    if (
        isinstance(current_handoff, str)
        and current_handoff
        and current_handoff != previous_handoff
        and after.get("handoffApproved") is True
    ):
        deltas.add("approved-handoff-artifact")

    ordered = [delta for delta in allowed if delta in deltas]
    return {"progressed": bool(ordered), "deltaClasses": ordered}


def _decision(
    decision: str,
    next_state: str,
    reason: str,
    *,
    effective_limit: int,
    signature_retries: int,
    recovery_actions: int,
) -> dict[str, Any]:
    return {
        "decision": decision,
        "nextState": next_state,
        "reason": reason,
        "effectiveRecoveryLimit": effective_limit,
        "nextAutomaticRetriesForSignature": signature_retries,
        "nextAutomaticRecoveryActionsUsed": recovery_actions,
    }


def decide_next(
    loop_state: dict[str, Any],
    budgets: dict[str, Any],
    failure: dict[str, Any],
    progress: dict[str, Any],
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply stop rules and both budgets without fallback counter resets."""

    if not all(
        isinstance(item, dict)
        for item in (loop_state, budgets, failure, progress)
    ):
        fail("AHLL-INPUT", "decision inputs must be objects")
    scan_sensitive_payload((loop_state, budgets, failure, progress))
    retry_policy = (
        contract["retryPolicy"]
        if contract is not None
        else {
            "maxAutomaticRetriesPerSignature": 2,
            "defaultMaxAutomaticRecoveryActionsPerTask": 3,
        }
    )
    no_progress_policy = (
        contract["noProgressPolicy"]
        if contract is not None
        else {"maxConsecutiveIdenticalResultsWithoutProgress": 2}
    )

    signature_retries = _bounded_nonnegative_int(
        loop_state.get("automaticRetriesForSignature"),
        "automaticRetriesForSignature",
    )
    recovery_actions = _bounded_nonnegative_int(
        loop_state.get("automaticRecoveryActionsUsed"),
        "automaticRecoveryActionsUsed",
    )
    identical_no_progress = _bounded_nonnegative_int(
        loop_state.get("consecutiveIdenticalNoProgressResults"),
        "consecutiveIdenticalNoProgressResults",
    )
    proposed_action_differs = loop_state.get("proposedActionDiffers")
    if not isinstance(proposed_action_differs, bool):
        fail("AHLL-INPUT", "proposedActionDiffers must be boolean")

    role_limit = budgets.get("roleMaxAutomaticRecoveryActions")
    task_limit = budgets.get("taskMaxAutomaticRecoveryActions")
    effective_limit = effective_recovery_limit(
        retry_policy["defaultMaxAutomaticRecoveryActionsPerTask"],
        role_limit,
        task_limit,
    )

    failure_class = failure.get("failureClass")
    retryable = failure.get("retryable")
    signature_digest = failure.get("signatureDigest")
    if (
        not isinstance(failure_class, str)
        or FAILURE_CLASS_PATTERN.fullmatch(failure_class) is None
        or not 3 <= len(failure_class) <= 80
        or not isinstance(retryable, bool)
        or not isinstance(signature_digest, str)
        or SIGNATURE_DIGEST_PATTERN.fullmatch(signature_digest) is None
    ):
        fail("AHLL-INPUT", "failure must be a normalized failure object")
    progressed = progress.get("progressed")
    delta_classes = progress.get("deltaClasses")
    if not isinstance(progressed, bool) or not isinstance(delta_classes, list):
        fail("AHLL-INPUT", "progress must be a measured progress object")
    if any(delta not in PROGRESS_DELTA_CLASSES for delta in delta_classes):
        fail("AHLL-INPUT", "progress contains an unauthorized delta class")
    if progressed != bool(delta_classes):
        fail("AHLL-INPUT", "progressed must match deltaClasses")

    disposition = {
        item[0]: (item[2], item[3]) for item in NONRETRYABLE_DISPOSITIONS
    }
    if failure_class in disposition:
        decision, next_state = disposition[failure_class]
        return _decision(
            decision,
            next_state,
            f"non-retryable:{failure_class}",
            effective_limit=effective_limit,
            signature_retries=signature_retries,
            recovery_actions=recovery_actions,
        )
    if not retryable:
        return _decision(
            "escalate",
            "escalated",
            "non-retryable-result",
            effective_limit=effective_limit,
            signature_retries=signature_retries,
            recovery_actions=recovery_actions,
        )
    if (
        not progressed
        and identical_no_progress
        >= no_progress_policy[
            "maxConsecutiveIdenticalResultsWithoutProgress"
        ]
    ):
        return _decision(
            "escalate",
            "escalated",
            "second-identical-no-progress-result",
            effective_limit=effective_limit,
            signature_retries=signature_retries,
            recovery_actions=recovery_actions,
        )
    if (
        signature_retries
        >= retry_policy["maxAutomaticRetriesPerSignature"]
    ):
        return _decision(
            "escalate",
            "escalated",
            "same-signature-retry-budget-exhausted",
            effective_limit=effective_limit,
            signature_retries=signature_retries,
            recovery_actions=recovery_actions,
        )
    if recovery_actions >= effective_limit:
        return _decision(
            "escalate",
            "escalated",
            "task-recovery-budget-exhausted",
            effective_limit=effective_limit,
            signature_retries=signature_retries,
            recovery_actions=recovery_actions,
        )
    if not proposed_action_differs:
        return _decision(
            "escalate",
            "escalated",
            "proposed-action-not-different",
            effective_limit=effective_limit,
            signature_retries=signature_retries,
            recovery_actions=recovery_actions,
        )
    return _decision(
        "retry",
        "running",
        "retry-approved",
        effective_limit=effective_limit,
        signature_retries=signature_retries + 1,
        recovery_actions=recovery_actions + 1,
    )


def _synthetic_sensitive_value() -> str:
    return "Bearer " + "syntheticfixturevalue"


def apply_mutation(contract: dict[str, Any], name: str) -> None:
    """Apply one deterministic negative contract mutation."""

    if name == "unknown-top-level-key":
        contract["unexpected"] = True
    elif name == "unknown-nested-key":
        contract["retryPolicy"]["unexpected"] = True
    elif name == "unsupported-schema-version":
        contract["schemaVersion"] = 2
    elif name == "unsupported-contract-version":
        contract["contractVersion"] = "2.0.0"
    elif name == "contract-id-drift":
        contract["contractId"] = "replacement-loop-contract"
    elif name == "current-owner-drift":
        contract["currentOwner"]["path"] = (
            "docs/00.agent-governance/contracts/replacement-loop.json"
        )
    elif name == "provider-neutral-disabled":
        contract["providerNeutral"] = False
    elif name == "state-order-drift":
        contract["stateMachine"]["states"][0], contract["stateMachine"][
            "states"
        ][1] = (
            contract["stateMachine"]["states"][1],
            contract["stateMachine"]["states"][0],
        )
    elif name == "terminal-state-drift":
        contract["stateMachine"]["states"][4]["terminal"] = False
    elif name == "transition-drift":
        contract["stateMachine"]["transitions"][4]["to"] = "validating"
    elif name == "signature-field-drift":
        contract["failureNormalization"]["signatureFields"][0] = (
            "provider-result-prose"
        )
    elif name == "initial-failure-counted-as-retry":
        contract["retryPolicy"]["initialFailureCountsAsRetry"] = True
    elif name == "same-signature-retry-ceiling":
        contract["retryPolicy"]["maxAutomaticRetriesPerSignature"] = 3
    elif name == "task-recovery-ceiling":
        contract["retryPolicy"][
            "defaultMaxAutomaticRecoveryActionsPerTask"
        ] = 4
    elif name == "provider-fallback-reset":
        contract["retryPolicy"]["providerFallbackResetsCounters"] = True
    elif name == "model-fallback-reset":
        contract["retryPolicy"]["modelFallbackResetsCounters"] = True
    elif name == "recovery-limit-precedence-drift":
        contract["retryPolicy"]["effectiveRecoveryLimit"] = (
            "default-overrides-lower-limits"
        )
    elif name == "no-progress-limit":
        contract["noProgressPolicy"][
            "maxConsecutiveIdenticalResultsWithoutProgress"
        ] = 3
    elif name == "no-progress-budget-consumption":
        contract["noProgressPolicy"]["consumesRetryBudgetBeforeStop"] = True
    elif name == "missing-nonretryable-class":
        contract["nonRetryableFailureClasses"][-1]["id"] = (
            "recoverable-contract-error"
        )
    elif name == "nonretryable-marked-retryable":
        contract["nonRetryableFailureClasses"][0]["retryable"] = True
    elif name == "progress-delta-drift":
        contract["progressPolicy"]["allowedDeltaClasses"][0] = (
            "more-provider-prose"
        )
    elif name == "rejected-signal-drift":
        contract["progressPolicy"]["rejectedSignals"][0] = (
            "changed-intended-file-state"
        )
    elif name == "checkpoint-owner-drift":
        contract["checkpointBoundary"]["implementationOwner"] = "AHLL-001"
    elif name == "checkpoint-execution-demoted":
        contract["checkpointBoundary"]["implementationState"] = (
            "declaration-only"
        )
    elif name == "checkpoint-validation-disabled":
        contract["checkpointBoundary"][
            "executableValidationDelegated"
        ] = False
    elif name == "checkpoint-schema-version-drift":
        contract["checkpointBoundary"]["checkpointSchemaVersion"] = 1
    elif name == "checkpoint-identity-axes-drift":
        contract["checkpointBoundary"]["identityAxes"][0] = "repository-path"
    elif name == "checkpoint-namespace-digest-disabled":
        contract["checkpointBoundary"]["namespaceDigestRequired"] = False
    elif name == "checkpoint-single-writer-disabled":
        contract["checkpointBoundary"]["singleWriterRequired"] = False
    elif name == "checkpoint-duplicate-resume-enabled":
        contract["checkpointBoundary"]["duplicateResumeAllowed"] = True
    elif name == "checkpoint-overwrite-policy-drift":
        contract["checkpointBoundary"]["overwritePolicy"] = (
            "replace-unconditionally"
        )
    elif name == "checkpoint-provider-state-read-enabled":
        contract["checkpointBoundary"]["actualProviderStateReadAllowed"] = True
    elif name == "memory-class-drift":
        contract["checkpointBoundary"]["memoryClassIds"][-1] = (
            "provider-local-authority"
        )
    elif name == "feedback-destination-id-drift":
        contract["feedbackRouting"]["destinations"][0]["id"] = (
            "replacement-fixture"
        )
    elif name == "feedback-destination-order-drift":
        destinations = contract["feedbackRouting"]["destinations"]
        destinations[0], destinations[1] = destinations[1], destinations[0]
    elif name == "feedback-owner-ref-drift":
        contract["feedbackRouting"]["destinations"][0]["ownerRef"] = (
            "tests/fixtures/replacement.json"
        )
    elif name == "feedback-review-disabled":
        contract["feedbackRouting"]["reviewRequired"] = False
    elif name == "feedback-raw-promotion-enabled":
        contract["feedbackRouting"][
            "rawTracePromptTranscriptPromotionAllowed"
        ] = True
    elif name == "interface-owner-drift":
        contract["interfaces"]["resume"]["implementationOwner"] = "AHLL-001"
    elif name == "checkpoint-interface-demoted":
        contract["interfaces"]["resume"]["implementationState"] = (
            "declaration-only"
        )
    elif name == "sensitive-key":
        contract["authority"]["token"] = "syntheticfixturevalue"
    elif name == "sensitive-provider-response-key":
        contract["authority"]["providerResponseBody"] = (
            "syntheticfixturevalue"
        )
    elif name == "sensitive-user-configuration-key":
        contract["authority"]["userConfiguration"] = (
            "syntheticfixturevalue"
        )
    elif name == "sensitive-raw-stdout-key":
        contract["authority"]["rawStdout"] = "syntheticfixturevalue"
    elif name == "sensitive-raw-stderr-key":
        contract["authority"]["RAW_STDERR"] = "syntheticfixturevalue"
    elif name == "sensitive-normalized-raw-output-key":
        contract["authority"]["normalizedRawOutputPayload"] = (
            "syntheticfixturevalue"
        )
    elif name == "sensitive-transcript-body-key":
        contract["authority"]["capturedTranscriptBody"] = (
            "syntheticfixturevalue"
        )
    elif name == "sensitive-prompt-text-key":
        contract["authority"]["capturedPromptText"] = (
            "syntheticfixturevalue"
        )
    elif name == "sensitive-value":
        contract["stateMachine"]["states"][0]["meaning"] = (
            _synthetic_sensitive_value()
        )
    else:
        fail("AHLL-FIXTURE", f"unknown lifecycle mutation {name!r}")


def _validate_fixture_shape(fixture: Any) -> None:
    if not isinstance(fixture, dict):
        fail("AHLL-FIXTURE", "fixture root must be an object")
    expected_keys = {
        "schemaVersion",
        "expectedCounts",
        "decisionCases",
        "mutations",
        "expectedCaseCount",
    }
    if set(fixture) != expected_keys or fixture.get("schemaVersion") != 1:
        fail("AHLL-FIXTURE", "fixture keys or schemaVersion differ")
    if not isinstance(fixture["expectedCounts"], dict):
        fail("AHLL-FIXTURE", "expectedCounts must be an object")

    decision_keys = {
        "name",
        "loopState",
        "budgets",
        "failure",
        "progress",
        "expectedDecision",
        "expectedReason",
        "expectedEffectiveRecoveryLimit",
    }
    decision_cases = fixture["decisionCases"]
    if not isinstance(decision_cases, list) or not all(
        isinstance(case, dict)
        and set(case) == decision_keys
        and isinstance(case["name"], str)
        and case["name"]
        for case in decision_cases
    ):
        fail("AHLL-FIXTURE", "decision cases must be closed objects")

    mutation_keys = {"name", "expectedRule"}
    mutations = fixture["mutations"]
    if not isinstance(mutations, list) or not all(
        isinstance(case, dict)
        and set(case) == mutation_keys
        and isinstance(case["name"], str)
        and isinstance(case["expectedRule"], str)
        for case in mutations
    ):
        fail("AHLL-FIXTURE", "mutations must be closed name/rule objects")

    names = [
        case["name"] for case in (*decision_cases, *mutations)
    ]
    if len(names) != len(set(names)):
        fail("AHLL-FIXTURE", "fixture case names must be unique")
    expected_count = len(decision_cases) + len(mutations) + 1
    if fixture["expectedCaseCount"] != expected_count:
        fail(
            "AHLL-FIXTURE",
            "expectedCaseCount must include decisions, mutations, and duplicate key",
        )


def run_self_test(root: Path) -> tuple[list[str], int, dict[str, int]]:
    contract = load_json(root, CONTRACT_PATH)
    fixture = load_json(root, FIXTURE_PATH)
    _validate_fixture_shape(fixture)
    failures: list[str] = []
    try:
        counts = validate_contract(root, contract)
    except LoopLifecycleError as exc:
        return (
            [f"baseline: expected PASS, got {exc.code}: {exc.detail}"],
            0,
            {},
        )
    if counts != fixture["expectedCounts"]:
        failures.append(
            f"baseline counts: expected {fixture['expectedCounts']!r}, "
            f"got {counts!r}"
        )

    cases = 0
    for case in fixture["decisionCases"]:
        cases += 1
        try:
            result = decide_next(
                case["loopState"],
                case["budgets"],
                case["failure"],
                case["progress"],
                contract,
            )
        except LoopLifecycleError as exc:
            failures.append(
                f"{case['name']}: decision raised {exc.code}: {exc.detail}"
            )
            continue
        observed = (
            result["decision"],
            result["reason"],
            result["effectiveRecoveryLimit"],
        )
        expected = (
            case["expectedDecision"],
            case["expectedReason"],
            case["expectedEffectiveRecoveryLimit"],
        )
        if observed != expected:
            failures.append(
                f"{case['name']}: expected {expected!r}, got {observed!r}"
            )

    for case in fixture["mutations"]:
        cases += 1
        mutated = copy.deepcopy(contract)
        apply_mutation(mutated, case["name"])
        try:
            validate_contract(root, mutated)
        except LoopLifecycleError as exc:
            if exc.code != case["expectedRule"]:
                failures.append(
                    f"{case['name']}: expected {case['expectedRule']}, "
                    f"got {exc.code}: {exc.detail}"
                )
        else:
            failures.append(f"{case['name']}: mutation passed")

    cases += 1
    duplicate_text = (
        '{"schemaVersion":1,"contractVersion":"1.0.0",'
        '"schemaVersion":1}'
    )
    try:
        decode_json_text(duplicate_text, "<duplicate-key-fixture>")
    except LoopLifecycleError as exc:
        if exc.code != "AHLL-DUPLICATE-KEY":
            failures.append(
                "duplicate-json-key: expected AHLL-DUPLICATE-KEY, "
                f"got {exc.code}"
            )
    else:
        failures.append("duplicate-json-key: mutation passed")
    return failures, cases, counts


def _resolve_root(value: Path) -> Path:
    try:
        mode = os.lstat(value).st_mode
    except OSError as exc:
        fail("AHLL-INPUT", f"root {value}: {exc}", exit_code=2)
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        fail(
            "AHLL-INPUT",
            f"root {value}: expected a directory that is not a symlink",
            exit_code=2,
        )
    try:
        return value.resolve(strict=True)
    except OSError as exc:
        fail("AHLL-INPUT", f"root {value}: {exc}", exit_code=2)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the provider-neutral agent loop lifecycle."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = _resolve_root(args.root)
        if args.self_test:
            failures, cases, counts = run_self_test(root)
            if failures:
                for failure in failures:
                    print(
                        f"ERR AHLL-SELF-TEST {failure}",
                        file=sys.stderr,
                    )
                return 1
            print(
                "[PASS] agent loop lifecycle self-test passed: "
                f"cases={cases} states={counts['states']} "
                f"transitions={counts['transitions']} "
                "same-signature-retries=2 task-recovery=3 "
                "no-progress-stop=2 nonretryable=6"
            )
            return 0

        counts = validate_contract(root)
        print(
            "[PASS] agent loop lifecycle validation passed: "
            f"states={counts['states']} "
            f"transitions={counts['transitions']} "
            "same-signature-retries=2 task-recovery=3 "
            "no-progress-stop=2 "
            f"nonretryable={counts['nonRetryableFailureClasses']} "
            f"progress={counts['progressDeltaClasses']} "
            f"interfaces={counts['interfaces']}"
        )
        return 0
    except LoopLifecycleError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code
    except (KeyError, TypeError, ValueError) as exc:
        print(f"ERR AHLL-INTERNAL {exc}", file=sys.stderr)
        return 1


# Spec-facing aliases keep the provider-neutral interface names importable.
normalizeFailure = normalize_failure
measureProgress = measure_progress
decideNext = decide_next
effectiveRecoveryLimit = effective_recovery_limit


if __name__ == "__main__":
    raise SystemExit(main())
