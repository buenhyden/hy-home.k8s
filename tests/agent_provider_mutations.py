"""Synthetic provider evidence mutations owned by provider tests."""

from __future__ import annotations

import copy
from typing import Any


def apply_config_mutation(contract: dict[str, Any], name: str) -> None:
    if name == "unknown-top-level-key":
        contract["unexpected"] = True
    elif name == "cutoff-source-after-cutoff":
        contract["sourceLedger"][0]["sourceDate"] = "2026-07-11"
    elif name == "cutoff-source-same-day-after-cutoff":
        contract["sourceLedger"][0]["sourceDate"] = "2026-07-10"
        contract["sourceLedger"][0]["publishedAtUtc"] = "2026-07-10T01:00:01Z"
    elif name == "source-id-substitution":
        contract["sourceLedger"][0]["id"] = "replacement-source-id"
    elif name == "extra-source-new-id":
        extra = copy.deepcopy(contract["sourceLedger"][0])
        extra["id"] = "extra-source-new-id"
        contract["sourceLedger"].append(extra)
    elif name == "absolute-project-path":
        contract["providers"][1]["projectPaths"][0]["path"] = "/etc/passwd"
    elif name == "invalid-calendar-source-date":
        contract["sourceLedger"][0]["sourceDate"] = "2026-02-30"
    elif name == "third-provider-added":
        extra = copy.deepcopy(contract["providers"][0])
        extra["id"] = "unsupported-third-provider"
        contract["providers"].append(extra)
    elif name == "provider-relabeled-as-neutral":
        contract["providers"][0]["trackedSurface"]["pathRoot"] = ".agents/agents"
    elif name == "model-silent-fallback-enabled":
        contract["providers"][1]["modelCandidates"][0]["fallback"][
            "silentFallbackAllowed"
        ] = True
    elif name == "model-fitness-promoted-without-gates":
        contract["providers"][1]["modelCandidates"][0]["promotionState"] = (
            "current-assignment"
        )
    elif name == "mcp-role-outside-registry":
        contract["mcpInventory"][0]["allowedRoles"].append("unowned-agent")
    elif name == "secret-like-contract-value":
        contract["sourceLedger"][0]["claim"] = "sk-test-not-a-real-secret"
    elif name == "absent-runtime-native-pass":
        contract["providers"][0]["localObservation"]["installation"] = "absent"
        contract["providers"][0]["evidenceLanes"][1]["verdict"] = "PASS"
        contract["providers"][0]["runtimeVerdicts"]["nativeDiscovery"] = "PASS"
    else:
        raise AssertionError(f"unknown provider config mutation: {name!r}")


def apply_canary_mutation(contract: dict[str, Any], name: str) -> None:
    if name == "canary-allows-mutation":
        contract["canaryRecords"][0]["mutationMode"] = "write"
    elif name == "canary-stores-prompt":
        contract["canaryRecords"][0]["redaction"]["rawPromptStored"] = True
    elif name == "canary-stores-credentials":
        contract["canaryRecords"][0]["redaction"]["credentialsStored"] = True
    elif name == "canary-unowned-limitation":
        contract["canaryRecords"][1]["owner"] = ""
    elif name == "canary-missing-retry-trigger":
        contract["canaryRecords"][1]["retryTrigger"] = None
    elif name == "canary-cross-lane-promotion":
        contract["canaryRecords"][1]["crossLanePromotion"] = True
    elif name == "canary-verdict-drift":
        contract["canaryRecords"][1]["verdict"] = "ABSENT"
    elif name == "authenticated-pass-without-discovery":
        contract["canaryRecords"][5]["verdict"] = "PASS"
        contract["providers"][1]["evidenceLanes"][2]["verdict"] = "PASS"
        contract["providers"][1]["runtimeVerdicts"]["authenticatedRun"] = "PASS"
    elif name == "absent-runtime-native-pass":
        contract["providers"][0]["localObservation"]["installation"] = "absent"
        contract["canaryRecords"][1]["verdict"] = "PASS"
        contract["providers"][0]["evidenceLanes"][1]["verdict"] = "PASS"
        contract["providers"][0]["runtimeVerdicts"]["nativeDiscovery"] = "PASS"
    else:
        raise AssertionError(f"unknown provider canary mutation: {name!r}")
