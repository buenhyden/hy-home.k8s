"""Synthetic checkpoint mutations owned by the independent test suite."""

from __future__ import annotations

from typing import Any


def _memory_record(
    checkpoint: dict[str, Any],
    memory_id: str,
) -> dict[str, Any]:
    return next(
        record
        for record in checkpoint["memoryLifecycle"]
        if record["classId"] == memory_id
    )


def apply_duplicate_key_mutation(validator: Any) -> None:
    validator.decode_json_text(
        '{"schemaVersion":2,"schemaVersion":2}',
        "synthetic duplicate-key mutation",
    )
    raise AssertionError("duplicate-key mutation unexpectedly passed")


def apply_mutation(
    checkpoint: dict[str, Any],
    repository_state: dict[str, Any],
    name: str,
) -> None:
    """Apply one named, deterministic, non-secret negative mutation."""

    identity = repository_state["identity"]
    working = _memory_record(checkpoint, "working-short-term")
    domain = _memory_record(checkpoint, "domain-scoped")
    provider_local = _memory_record(checkpoint, "provider-local-auxiliary")

    if name == "unknown-checkpoint-field":
        checkpoint["unexpectedField"] = True
    elif name == "stale-repository":
        identity["repositoryId"] = "sha256:" + ("4" * 64)
    elif name == "stale-task":
        identity["taskId"] = "AHLL-999-SYNTHETIC"
    elif name == "stale-spec":
        identity["specRef"] = (
            "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/spec.md"
        )
    elif name == "stale-worktree":
        identity["worktreeId"] = "sha256:" + ("5" * 64)
    elif name == "stale-provider-surface":
        identity["providerSurfaceId"] = "claude"
    elif name == "stale-provider-session":
        identity["providerSessionInstanceDigest"] = "sha256:" + ("4" * 64)
    elif name == "namespace-digest-drift":
        checkpoint["identity"]["namespaceDigest"] = "sha256:" + ("4" * 64)
    elif name == "writer-id-collision":
        identity["writerId"] = "sha256:" + ("4" * 64)
    elif name == "writer-claim-drift":
        checkpoint["identity"]["writerClaimDigest"] = "sha256:" + ("4" * 64)
    elif name == "write-generation-stale":
        identity["writeGeneration"] += 1
    elif name == "previous-checkpoint-overwrite":
        identity["previousCheckpointDigest"] = "sha256:" + ("4" * 64)
    elif name == "duplicate-writer":
        repository_state["activeWriterCount"] = 2
    elif name == "duplicate-resume":
        repository_state["activeResumeCount"] = 2
    elif name == "provider-executor-surface-mismatch":
        checkpoint["executor"]["providerId"] = "claude"
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
        checkpoint["repository"]["loopState"] = name.removeprefix("terminal-replay-")
    elif name == "completed-work-overflow":
        checkpoint["completedWork"] = [
            f"Bounded synthetic completed item {index}." for index in range(13)
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
    elif name == "resume-identity-tuple-disabled":
        checkpoint["resume"]["identityTupleRequired"] = False
    elif name == "resume-single-writer-disabled":
        checkpoint["resume"]["singleWriterRequired"] = False
    elif name == "resume-duplicate-writer-enabled":
        checkpoint["resume"]["duplicateWriterAllowed"] = True
    elif name == "resume-duplicate-resume-enabled":
        checkpoint["resume"]["duplicateResumeAllowed"] = True
    elif name == "resume-overwrite-policy-drift":
        checkpoint["resume"]["overwritePolicy"] = "replace-unconditionally"
    elif name == "resume-accepted-identity-drift":
        checkpoint["resume"]["acceptedIdentity"] = "partial-match"
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
    elif name == "memory-sensitivity-drift":
        working["sensitivity"]["restrictedContextAllowed"] = True
    elif name == "memory-retention-drift":
        working["retention"]["policy"] = "retain-under-canonical-owner"
    elif name == "memory-retention-evidence-missing":
        working["retention"]["evidenceRefs"] = []
    elif name == "memory-handoff-owner-missing":
        working["handoff"]["nextOwner"] = None
    elif name == "memory-handoff-evidence-missing":
        working["handoff"]["evidenceRefs"] = []
    elif name == "compaction-retains-transcript":
        checkpoint["compaction"]["fullTranscriptRetained"] = True
    elif name == "compaction-count-drift":
        checkpoint["compaction"]["remainingWorkCount"] += 1
    elif name == "compaction-source-evidence-missing":
        checkpoint["compaction"]["source"]["evidenceRefs"] = []
    elif name == "compaction-replacement-evidence-missing":
        checkpoint["compaction"]["replacement"]["evidenceRefs"] = []
    elif name == "compaction-identical-digests":
        checkpoint["compaction"]["replacement"]["digest"] = checkpoint["compaction"][
            "source"
        ]["digest"]
    elif name == "compaction-source-owner-missing":
        checkpoint["compaction"]["source"].pop("owner")
    elif name == "compaction-replacement-owner-missing":
        checkpoint["compaction"]["replacement"].pop("owner")
    elif name == "compaction-review-unapproved":
        checkpoint["compaction"]["reviewStatus"] = "pending"
    elif name == "handoff-owner-missing":
        checkpoint["handoff"]["nextOwner"] = None
    elif name == "handoff-evidence-missing":
        checkpoint["handoff"]["evidenceRefs"] = []
    elif name == "sensitive-credential-key":
        checkpoint["credentialValue"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-credential-value":
        checkpoint["nextAction"] = "Credential " + "value: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-secret-key":
        checkpoint["secret"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-token-key":
        checkpoint["token"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-token-value":
        checkpoint["nextAction"] = "Bearer " + "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-sk-proj-value":
        checkpoint["nextAction"] = "sk" + "-proj-" + "synthetic_marker_only"
    elif name == "sensitive-gho-value":
        checkpoint["nextAction"] = "gh" + "o_" + "syntheticmarkeronly"
    elif name == "sensitive-xoxp-value":
        checkpoint["nextAction"] = "xox" + "p-" + "synthetic-marker-only"
    elif name == "sensitive-aiza-value":
        checkpoint["nextAction"] = "AI" + "za" + "SyntheticMarkerOnly"
    elif name == "sensitive-auth-path-key":
        checkpoint["authFilePath"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-auth-path-value":
        checkpoint["nextAction"] = "/synthetic/" + "." + "ssh/id_" + "rsa"
    elif name == "sensitive-account-id-key":
        checkpoint["accountIdentifier"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-account-id-value":
        checkpoint["nextAction"] = "Account " + "identifier: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-raw-prompt-key":
        checkpoint["rawPrompt"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-raw-prompt-value":
        checkpoint["nextAction"] = "Raw " + "prompt: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-transcript-key":
        checkpoint["providerTranscript"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-transcript-value":
        checkpoint["nextAction"] = "Full " + "transcript: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-provider-body-key":
        checkpoint["providerResponseBody"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-provider-body-value":
        checkpoint["nextAction"] = "Provider response " + "body: [REDACTED-SYNTHETIC]"
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
        checkpoint["nextAction"] = "Shell " + "history: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-environment-dump-key":
        checkpoint["environmentDump"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-environment-dump-value":
        checkpoint["nextAction"] = "Environment " + "dump: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-private-diagnostics-key":
        checkpoint["privateDiagnostics"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-private-diagnostics-value":
        checkpoint["nextAction"] = "Private " + "diagnostics: [REDACTED-SYNTHETIC]"
    elif name == "sensitive-user-config-key":
        checkpoint["userConfiguration"] = "[REDACTED-SYNTHETIC]"
    elif name == "sensitive-user-config-value":
        checkpoint["nextAction"] = "User " + "configuration: [REDACTED-SYNTHETIC]"
    else:
        raise AssertionError(f"unknown checkpoint mutation: {name!r}")
