"""Synthetic loop-lifecycle mutations owned by the independent test suite."""

from __future__ import annotations

from typing import Any


def apply_mutation(contract: dict[str, Any], name: str) -> None:
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
        contract["stateMachine"]["states"][0], contract["stateMachine"]["states"][1] = (
            contract["stateMachine"]["states"][1],
            contract["stateMachine"]["states"][0],
        )
    elif name == "terminal-state-drift":
        contract["stateMachine"]["states"][4]["terminal"] = False
    elif name == "transition-drift":
        contract["stateMachine"]["transitions"][4]["to"] = "validating"
    elif name == "signature-field-drift":
        contract["failureNormalization"]["signatureFields"][0] = "provider-result-prose"
    elif name == "initial-failure-counted-as-retry":
        contract["retryPolicy"]["initialFailureCountsAsRetry"] = True
    elif name == "same-signature-retry-ceiling":
        contract["retryPolicy"]["maxAutomaticRetriesPerSignature"] = 3
    elif name == "task-recovery-ceiling":
        contract["retryPolicy"]["defaultMaxAutomaticRecoveryActionsPerTask"] = 4
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
        contract["nonRetryableFailureClasses"][-1]["id"] = "recoverable-contract-error"
    elif name == "nonretryable-marked-retryable":
        contract["nonRetryableFailureClasses"][0]["retryable"] = True
    elif name == "progress-delta-drift":
        contract["progressPolicy"]["allowedDeltaClasses"][0] = "more-provider-prose"
    elif name == "rejected-signal-drift":
        contract["progressPolicy"]["rejectedSignals"][0] = "changed-intended-file-state"
    elif name == "checkpoint-owner-drift":
        contract["checkpointBoundary"]["implementationOwner"] = "AHLL-001"
    elif name == "checkpoint-execution-demoted":
        contract["checkpointBoundary"]["implementationState"] = "declaration-only"
    elif name == "checkpoint-validation-disabled":
        contract["checkpointBoundary"]["executableValidationDelegated"] = False
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
        contract["checkpointBoundary"]["overwritePolicy"] = "replace-unconditionally"
    elif name == "checkpoint-provider-state-read-enabled":
        contract["checkpointBoundary"]["actualProviderStateReadAllowed"] = True
    elif name == "memory-class-drift":
        contract["checkpointBoundary"]["memoryClassIds"][-1] = (
            "provider-local-authority"
        )
    elif name == "feedback-destination-id-drift":
        contract["feedbackRouting"]["destinations"][0]["id"] = "replacement-fixture"
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
        contract["feedbackRouting"]["rawTracePromptTranscriptPromotionAllowed"] = True
    elif name == "interface-owner-drift":
        contract["interfaces"]["resume"]["implementationOwner"] = "AHLL-001"
    elif name == "checkpoint-interface-demoted":
        contract["interfaces"]["resume"]["implementationState"] = "declaration-only"
    elif name == "sensitive-key":
        contract["authority"]["token"] = "syntheticfixturevalue"
    elif name == "sensitive-provider-response-key":
        contract["authority"]["providerResponseBody"] = "syntheticfixturevalue"
    elif name == "sensitive-user-configuration-key":
        contract["authority"]["userConfiguration"] = "syntheticfixturevalue"
    elif name == "sensitive-raw-stdout-key":
        contract["authority"]["rawStdout"] = "syntheticfixturevalue"
    elif name == "sensitive-raw-stderr-key":
        contract["authority"]["RAW_STDERR"] = "syntheticfixturevalue"
    elif name == "sensitive-normalized-raw-output-key":
        contract["authority"]["normalizedRawOutputPayload"] = "syntheticfixturevalue"
    elif name == "sensitive-transcript-body-key":
        contract["authority"]["capturedTranscriptBody"] = "syntheticfixturevalue"
    elif name == "sensitive-prompt-text-key":
        contract["authority"]["capturedPromptText"] = "syntheticfixturevalue"
    elif name == "sensitive-value":
        contract["stateMachine"]["states"][0]["meaning"] = (
            "Bearer " + "syntheticfixturevalue"
        )
    else:
        raise AssertionError(f"unknown lifecycle mutation: {name!r}")
