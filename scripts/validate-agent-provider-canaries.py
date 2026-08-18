#!/usr/bin/env python3
"""Validate synthetic, redacted, non-transitive provider canary records."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence


CONFIG_VALIDATOR_PATH = Path(__file__).with_name(
    "validate-agent-provider-config.py"
)
SPEC = importlib.util.spec_from_file_location(
    "agent_provider_config_validator", CONFIG_VALIDATOR_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import {CONFIG_VALIDATOR_PATH}")
CONFIG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONFIG)

PROVIDER_IDS = ("local", "claude", "codex", "gemini")
EVIDENCE_CLASSES = (
    "repo-static",
    "native-discovery",
    "authenticated-run",
)
VERDICTS = ("PASS", "FAIL", "BLOCKED", "ABSENT", "DEFER")


class ProviderCanaryError(ValueError):
    """Typed provider-canary contract failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def fail(code: str, detail: str, *, exit_code: int = 1) -> NoReturn:
    raise ProviderCanaryError(code, detail, exit_code=exit_code)


def _load_config_json(root: Path, relative: Any) -> Any:
    try:
        return CONFIG.load_json(root, relative)
    except CONFIG.ProviderConfigError as exc:
        fail(exc.code, exc.detail, exit_code=exc.exit_code)


def _provider_lanes(contract: dict[str, Any]) -> dict[tuple[str, str], str]:
    return {
        (provider["id"], lane["id"]): lane["verdict"]
        for provider in contract["providers"]
        for lane in provider["evidenceLanes"]
    }


def validate_canaries(
    root: Path,
    contract: dict[str, Any] | None = None,
) -> dict[str, int]:
    root = Path(root)
    if contract is None:
        contract = _load_config_json(root, CONFIG.CONTRACT_PATH)

    records = contract["canaryRecords"]
    record_ids = [record["id"] for record in records]
    if len(record_ids) != len(set(record_ids)):
        fail("PNME-CANARY-COVERAGE", "canary record IDs must be unique")

    expected = {
        (provider_id, evidence_class)
        for provider_id in PROVIDER_IDS
        for evidence_class in EVIDENCE_CLASSES
    }
    observed = {
        (record["providerId"], record["evidenceClass"])
        for record in records
    }
    if observed != expected or len(records) != len(expected):
        fail(
            "PNME-CANARY-COVERAGE",
            f"expected one record per provider/lane, got {sorted(observed)}",
        )

    for record in records:
        key = f"{record['providerId']}/{record['evidenceClass']}"
        if record["verdict"] not in VERDICTS:
            fail("PNME-CANARY-VERDICT", f"{key} verdict is not allowed")
        if record["synthetic"] is not True:
            fail("PNME-CANARY-MUTATION", f"{key} is not synthetic")
        if record["mutationMode"] != "no-mutation":
            fail("PNME-CANARY-MUTATION", f"{key} permits mutation")
        if record["allowedTools"]:
            fail(
                "PNME-CANARY-MUTATION",
                f"{key} declares tools despite no execution authority",
            )
        if record["crossLanePromotion"] is not False:
            fail(
                "PNME-CANARY-CROSS-LANE",
                f"{key} permits cross-lane promotion",
            )

        redaction = record["redaction"]
        if (
            redaction["status"] != "PASS"
            or redaction["rawPromptStored"] is not False
            or redaction["providerBodyStored"] is not False
            or redaction["credentialsStored"] is not False
            or redaction["authPathsStored"] is not False
        ):
            fail(
                "PNME-CANARY-REDACTION",
                f"{key} contains or permits prohibited durable evidence",
            )

        if record["verdict"] != "PASS" and (
            not record["owner"]
            or not record["limitation"]
            or not record["retryTrigger"]
        ):
            fail(
                "PNME-CANARY-LIMITATION",
                f"{key} limitation lacks owner/detail/retry trigger",
            )
        if record["fallbackObserved"] and record["verdict"] != "FAIL":
            fail(
                "PNME-CANARY-FALLBACK",
                f"{key} observed fallback without FAIL",
            )

    lane_verdicts = _provider_lanes(contract)
    record_verdicts = {
        (record["providerId"], record["evidenceClass"]): record["verdict"]
        for record in records
    }
    if record_verdicts != lane_verdicts:
        fail(
            "PNME-CANARY-PARITY",
            "canary records drifted from provider evidence lanes",
        )

    for provider_id in PROVIDER_IDS:
        native = record_verdicts[(provider_id, "native-discovery")]
        authenticated = record_verdicts[
            (provider_id, "authenticated-run")
        ]
        repo_static = record_verdicts[(provider_id, "repo-static")]
        if authenticated == "PASS" and native != "PASS":
            fail(
                "PNME-CANARY-ORDER",
                f"{provider_id} authenticated PASS lacks discovery PASS",
            )
        if native == "PASS" and repo_static != "PASS":
            fail(
                "PNME-CANARY-ORDER",
                f"{provider_id} discovery PASS lacks repo-static PASS",
            )

    try:
        CONFIG.validate_contract(root, contract, check_paths=True)
    except CONFIG.ProviderConfigError as exc:
        fail(exc.code, exc.detail, exit_code=exc.exit_code)

    verdict_counts = {
        verdict: sum(
            record["verdict"] == verdict
            for record in records
        )
        for verdict in VERDICTS
    }
    return {
        "records": len(records),
        "providers": len(PROVIDER_IDS),
        **{f"verdict{key}": value for key, value in verdict_counts.items()},
    }


def apply_mutation(contract: dict[str, Any], name: str) -> None:
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
        contract["canaryRecords"][10]["verdict"] = "PASS"
        contract["providers"][3]["evidenceLanes"][1]["verdict"] = "PASS"
        contract["providers"][3]["runtimeVerdicts"]["nativeDiscovery"] = "PASS"
    else:
        fail("PNME-FIXTURE", f"unknown canary mutation {name}")


def validate_fixture(root: Path) -> int:
    contract = _load_config_json(root, CONFIG.CONTRACT_PATH)
    fixture = _load_config_json(root, CONFIG.FIXTURE_PATH)
    cases = fixture["canaryMutations"]
    for case in cases:
        mutated = copy.deepcopy(contract)
        apply_mutation(mutated, case["name"])
        try:
            validate_canaries(root, mutated)
        except ProviderCanaryError as exc:
            if exc.code != case["expectedRule"]:
                fail(
                    "PNME-FIXTURE",
                    f"{case['name']} expected {case['expectedRule']} got {exc.code}",
                )
        else:
            fail("PNME-FIXTURE", f"{case['name']} unexpectedly passed")
    return len(cases)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate provider canary evidence records."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root)
    try:
        cases = validate_fixture(root) if args.self_test else 0
        counts = validate_canaries(root)
        if args.self_test:
            print(
                "[PASS] agent provider canary self-test passed: "
                f"cases={cases} records={counts['records']} "
                f"providers={counts['providers']}"
            )
        else:
            print(
                "[PASS] agent provider canary validation passed: "
                f"records={counts['records']} providers={counts['providers']}"
            )
        return 0
    except ProviderCanaryError as exc:
        print(f"{exc.code}: {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
