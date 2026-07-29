#!/usr/bin/env python3
"""Validate the closed Spec 044 agent-evaluation contract."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-evaluations.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-evaluations.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-evaluations.json")
OWNER_SPEC = (
    "docs/03.specs/044-agent-roster-evaluation-and-admission/spec.md"
)
FIXED_CUTOFF = {
    "localTime": "2026-07-10 10:00 Asia/Seoul",
    "instantUtc": "2026-07-10T01:00:00Z",
}
TARGET_ROLES = (
    "supervisor",
    "code-reviewer",
    "doc-writer",
    "gitops-reviewer",
    "incident-responder",
    "k8s-implementer",
    "network-reviewer",
    "observability-reviewer",
    "security-auditor",
    "wiki-curator",
    "docs-researcher",
    "quality-engineer",
)
HIGH_RISK_ROLES = (
    "supervisor",
    "gitops-reviewer",
    "incident-responder",
    "k8s-implementer",
    "network-reviewer",
    "observability-reviewer",
    "security-auditor",
    "docs-researcher",
    "quality-engineer",
)
REQUIRED_FIXTURE_CLASSES = (
    "positive",
    "negative-adversarial",
    "refusal-stop",
    "handoff",
)
MEMORY_CLASSES = (
    "working-short-term",
    "durable-long-term",
    "domain-scoped",
    "provider-local-auxiliary",
)
PROMOTION_BLOCKING_EVENTS = (
    "critical-miss",
    "secret-disclosure",
    "scope-escape",
    "unsafe-live-action",
)
DEFERRED_AUTHORITY = {
    "state": "contract-only",
    "evidenceKind": "repo-static",
    "execution": "DEFER",
    "runtime": "DEFER",
    "providerResolution": "DEFER",
    "authentication": "DEFER",
    "liveAction": "DEFER",
    "evaluationDecision": "DEFER",
}
PRIVACY_POLICY = {
    "material": "synthetic-or-redacted-only",
    "secretsAllowed": False,
    "rawPromptsAllowed": False,
    "fullTranscriptsAllowed": False,
    "authenticationMaterialAllowed": False,
    "shellHistoryAllowed": False,
    "privateDiagnosticsAllowed": False,
    "productionDataAllowed": False,
}
PROHIBITED_KEY_NAMES = {
    "token",
    "apikey",
    "api_key",
    "secret",
    "password",
    "credential",
    "credentials",
    "authfile",
    "auth_file",
    "shellhistory",
    "shell_history",
    "rawprompt",
    "raw_prompt",
    "fulltranscript",
    "full_transcript",
    "privatediagnostics",
    "private_diagnostics",
}
PROHIBITED_VALUE_FRAGMENTS = (
    "sk-",
    "bearer ",
    "ghp_",
    "aiza",
    "-----begin private key",
)


class EvaluationContractError(ValueError):
    """Stable, machine-readable failure from the evaluation gate."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def fail(code: str, detail: str, *, exit_code: int = 1) -> None:
    raise EvaluationContractError(code, detail, exit_code=exit_code)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(
                "AREA-EVAL-JSON-DUPLICATE",
                f"duplicate JSON key {key!r}",
                exit_code=2,
            )
        result[key] = value
    return result


def decode_json_text(text: str, source: str) -> Any:
    """Decode JSON while rejecting duplicate keys at every object depth."""
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except EvaluationContractError:
        raise
    except json.JSONDecodeError as exc:
        fail(
            "AREA-EVAL-JSON",
            f"{source}: {exc}",
            exit_code=2,
        )


def _resolve_regular_file(root: Path, relative: PurePosixPath) -> Path:
    try:
        root_metadata = os.lstat(root)
    except OSError:
        fail("AREA-EVAL-INPUT", "repository root is unavailable", exit_code=2)
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(
        root_metadata.st_mode
    ):
        fail(
            "AREA-EVAL-INPUT",
            "repository root is not a real directory",
            exit_code=2,
        )
    try:
        repository_root = root.resolve(strict=True)
    except OSError:
        fail("AREA-EVAL-INPUT", "repository root is unavailable", exit_code=2)

    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        fail("AREA-EVAL-INPUT", "required input path is invalid", exit_code=2)

    candidate = repository_root
    for index, part in enumerate(relative.parts):
        candidate = candidate / part
        try:
            metadata = os.lstat(candidate)
        except OSError:
            fail(
                "AREA-EVAL-INPUT",
                f"required input is unavailable: {relative}",
                exit_code=2,
            )
        final_component = index == len(relative.parts) - 1
        if stat.S_ISLNK(metadata.st_mode):
            fail(
                "AREA-EVAL-INPUT",
                f"required input is not a real regular file: {relative}",
                exit_code=2,
            )
        if not final_component and not stat.S_ISDIR(metadata.st_mode):
            fail(
                "AREA-EVAL-INPUT",
                f"required input path is unavailable: {relative}",
                exit_code=2,
            )
        if final_component and not stat.S_ISREG(metadata.st_mode):
            fail(
                "AREA-EVAL-INPUT",
                f"required input is not a regular file: {relative}",
                exit_code=2,
            )

    try:
        resolved_candidate = candidate.resolve(strict=True)
        resolved_candidate.relative_to(repository_root)
    except (OSError, ValueError):
        fail(
            "AREA-EVAL-INPUT",
            f"required input is unavailable: {relative}",
            exit_code=2,
        )
    if resolved_candidate != candidate:
        fail(
            "AREA-EVAL-INPUT",
            f"required input is not a real regular file: {relative}",
            exit_code=2,
        )
    return candidate


def load_json(root: Path, relative: PurePosixPath) -> Any:
    path = _resolve_regular_file(root, relative)
    descriptor = -1
    try:
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            fail(
                "AREA-EVAL-INPUT",
                f"required input is not a regular file: {relative}",
                exit_code=2,
            )
        with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
            descriptor = -1
            text = stream.read()
    except EvaluationContractError:
        raise
    except (OSError, UnicodeError):
        fail(
            "AREA-EVAL-INPUT",
            f"required input cannot be read: {relative}",
            exit_code=2,
        )
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return decode_json_text(text, str(relative))


def _scan_sensitive_payload(value: Any, path: str = "<root>") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = re.sub(r"[^a-z0-9_]", "", key.lower())
            if normalized in PROHIBITED_KEY_NAMES:
                fail(
                    "AREA-EVAL-SENSITIVE",
                    f"forbidden sensitive field at {path}/{key}",
                )
            _scan_sensitive_payload(nested, f"{path}/{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            _scan_sensitive_payload(nested, f"{path}/{index}")
        return
    if isinstance(value, str):
        lowered = value.lower()
        if any(fragment in lowered for fragment in PROHIBITED_VALUE_FRAGMENTS):
            fail("AREA-EVAL-SENSITIVE", f"secret-like value at {path}")


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _targeted_preflight(contract: dict[str, Any]) -> None:
    """Emit stable semantic rules before generic schema diagnostics."""
    authority = _mapping(contract.get("authority"))
    if authority and any(
        key in authority and authority[key] != expected
        for key, expected in DEFERRED_AUTHORITY.items()
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "authority must remain contract-only, repo-static, and DEFER",
        )

    policy = _mapping(contract.get("privacyPolicy"))
    if policy and any(
        key in policy and policy[key] != expected
        for key, expected in PRIVACY_POLICY.items()
    ):
        fail(
            "AREA-EVAL-PRIVACY",
            "only synthetic/redacted material is allowed; "
            "private evidence is forbidden",
        )

    required_classes = contract.get("requiredFixtureClasses")
    if (
        isinstance(required_classes, list)
        and tuple(required_classes) != REQUIRED_FIXTURE_CLASSES
    ):
        fail(
            "AREA-EVAL-FIXTURE-CLASS",
            f"requiredFixtureClasses must equal {REQUIRED_FIXTURE_CLASSES!r}",
        )

    promotion = _mapping(contract.get("promotionPolicy"))
    blocking = promotion.get("blockingEvents")
    if (
        isinstance(blocking, list)
        and tuple(blocking) != PROMOTION_BLOCKING_EVENTS
    ):
        fail(
            "AREA-EVAL-PROMOTION-BLOCK",
            f"blockingEvents must equal {PROMOTION_BLOCKING_EVENTS!r}",
        )

    record = _mapping(contract.get("evaluationRecordContract"))
    comparison = _mapping(record.get("baselineCandidate"))
    if comparison and (
        comparison.get("sameSuiteVersionRequired") is not True
        or comparison.get("sameGraderVersionRequired") is not True
        or comparison.get("baseline") != "DEFER"
        or comparison.get("candidate") != "DEFER"
    ):
        fail(
            "AREA-EVAL-BASELINE-COMPARISON",
            "baseline and candidate must use the same suite and grader",
        )
    execution = _mapping(record.get("providerExecution"))
    if execution and (
        set(execution) != {"provider", "model", "reasoning", "config", "canary"}
        or any(value != "DEFER" for value in execution.values())
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "provider/model/reasoning/config/canary evidence must remain DEFER",
        )
    metrics = _mapping(record.get("metrics"))
    if metrics and (
        set(metrics) != {"quality", "safety", "cost", "latency"}
        or any(value != "DEFER" for value in metrics.values())
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "quality/safety/cost/latency results must remain DEFER",
        )
    adjudication = _mapping(record.get("adjudication"))
    if adjudication and (
        adjudication.get("adjudicator") != "DEFER"
        or adjudication.get("decision") != "DEFER"
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "adjudicator and decision evidence must remain DEFER",
        )
    rollback = _mapping(record.get("rollback"))
    if rollback and (
        rollback.get("state") != "DEFER"
        or rollback.get("reference") != "DEFER"
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "rollback evidence must remain DEFER",
        )

    for suite in _list(contract.get("roleSuites")):
        if not isinstance(suite, dict):
            continue
        classes = suite.get("fixtureClasses")
        if isinstance(classes, list) and tuple(classes) != REQUIRED_FIXTURE_CLASSES:
            fail(
                "AREA-EVAL-FIXTURE-CLASS",
                f"{suite.get('roleId', '<unknown>')} fixture classes differ",
            )
        version_fields = (
            suite.get("suiteVersion"),
            suite.get("fixtureVersion"),
            suite.get("graderVersion"),
            suite.get("rubricVersion"),
        )
        if all(value is not None for value in version_fields) and any(
            value != "1.0.0" for value in version_fields
        ):
            fail(
                "AREA-EVAL-VERSION",
                f"{suite.get('roleId', '<unknown>')} versions must equal 1.0.0",
            )
        if any(
            suite.get(field) not in (None, "DEFER")
            for field in ("corpusState", "evaluationDecision", "rollbackState")
        ):
            fail(
                "AREA-EVAL-RUNTIME-PRECLAIM",
                f"{suite.get('roleId', '<unknown>')} preclaims evaluation evidence",
            )
        if (
            suite.get("riskClass") == "high"
            and suite.get("independentAdjudicationRequired") is not True
        ):
            fail(
                "AREA-EVAL-ADJUDICATION",
                f"{suite.get('roleId', '<unknown>')} requires independent adjudication",
            )


def _validate_schema(root: Path, contract: dict[str, Any]) -> None:
    schema = load_json(root, SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("AREA-EVAL-SCHEMA", "schema root must be an object", exit_code=2)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        fail("AREA-EVAL-SCHEMA", f"invalid Draft 2020-12 schema: {exc}", exit_code=2)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: (tuple(str(part) for part in item.path), item.message),
    )
    if errors:
        rendered = []
        for error in errors[:8]:
            path = "/".join(str(part) for part in error.path) or "<root>"
            rendered.append(f"{path}: {error.message}")
        fail("AREA-EVAL-SCHEMA", "; ".join(rendered))


def _validate_record_contract(record: dict[str, Any]) -> None:
    if record["suite"] != {
        "idField": "suiteId",
        "versionField": "suiteVersion",
        "required": True,
    }:
        fail("AREA-EVAL-RECORD-CONTRACT", "suite field contract differs")
    fixture = record["fixture"]
    if fixture["identityFields"] != ["fixtureId", "fixtureVersion"]:
        fail("AREA-EVAL-RECORD-CONTRACT", "fixture identity fields differ")
    if fixture["requiredClasses"] != list(REQUIRED_FIXTURE_CLASSES):
        fail("AREA-EVAL-FIXTURE-CLASS", "record fixture classes differ")
    if fixture["evidenceFields"] != [
        "provenance",
        "privacy",
        "risk",
        "inputDigest",
    ]:
        fail("AREA-EVAL-RECORD-CONTRACT", "fixture evidence fields differ")
    if fixture["digest"] != {
        "field": "inputDigest",
        "algorithm": "sha256",
        "format": "sha256:<64-lowercase-hex>",
        "requiredAtExecution": True,
        "currentState": "DEFER",
    }:
        fail("AREA-EVAL-RECORD-CONTRACT", "input digest contract differs")
    if fixture["expectedBehavior"] != {
        "pathsField": "allowedPaths",
        "toolsField": "allowedTools",
        "prohibitedActionsField": "prohibitedActions",
        "stopHandoffField": "stopHandoffExpectation",
    }:
        fail("AREA-EVAL-EXPECTED-BEHAVIOR", "expected behavior fields differ")
    if record["grader"] != {
        "versionField": "graderVersion",
        "rubricVersionField": "rubricVersion",
        "rubricDimensions": ["quality", "safety", "cost", "latency"],
    }:
        fail("AREA-EVAL-GRADER", "grader/rubric field contract differs")
    if record["providerExecution"] != {
        "provider": "DEFER",
        "model": "DEFER",
        "reasoning": "DEFER",
        "config": "DEFER",
        "canary": "DEFER",
    }:
        fail("AREA-EVAL-RUNTIME-PRECLAIM", "provider execution is not DEFER")
    if record["metrics"] != {
        "quality": "DEFER",
        "safety": "DEFER",
        "cost": "DEFER",
        "latency": "DEFER",
    }:
        fail("AREA-EVAL-RUNTIME-PRECLAIM", "metric results are not DEFER")
    if record["adjudication"] != {
        "adjudicator": "DEFER",
        "independentForHighRisk": True,
        "decision": "DEFER",
    }:
        fail("AREA-EVAL-ADJUDICATION", "adjudication field contract differs")
    if record["rollback"] != {"state": "DEFER", "reference": "DEFER"}:
        fail("AREA-EVAL-RUNTIME-PRECLAIM", "rollback field contract differs")


def validate_contract(
    root: Path,
    contract: dict[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the production contract or an injected negative fixture."""
    root = root.resolve()
    loaded = load_json(root, CONTRACT_PATH) if contract is None else contract
    if not isinstance(loaded, dict):
        fail("AREA-EVAL-CONTRACT-TYPE", "contract root must be an object")
    _scan_sensitive_payload(loaded)
    _targeted_preflight(loaded)
    _validate_schema(root, loaded)

    if loaded["ownerSpec"] != OWNER_SPEC:
        fail("AREA-EVAL-OWNER", "ownerSpec must be Spec 044")
    if loaded["fixedSourceCutoff"] != FIXED_CUTOFF:
        fail(
            "AREA-EVAL-CUTOFF",
            "fixed cutoff must remain 2026-07-10 10:00 Asia/Seoul",
        )
    if tuple(loaded["memoryClasses"]) != MEMORY_CLASSES:
        fail("AREA-EVAL-MEMORY", "memory class order or identity differs")
    if tuple(loaded["requiredFixtureClasses"]) != REQUIRED_FIXTURE_CLASSES:
        fail("AREA-EVAL-FIXTURE-CLASS", "fixture class set differs")

    promotion = loaded["promotionPolicy"]
    if (
        promotion["baselineComparison"] != "same-suite-and-grader"
        or promotion["highRiskAdjudication"] != "independent-required"
        or promotion["qualitySafetyBeforeCostLatency"] is not True
        or tuple(promotion["blockingEvents"]) != PROMOTION_BLOCKING_EVENTS
        or promotion["promotionState"] != "DEFER"
    ):
        fail("AREA-EVAL-PROMOTION-BLOCK", "promotion policy differs")

    record = loaded["evaluationRecordContract"]
    _validate_record_contract(record)
    comparison = record["baselineCandidate"]
    if comparison != {
        "baseline": "DEFER",
        "candidate": "DEFER",
        "sameSuiteVersionRequired": True,
        "sameGraderVersionRequired": True,
    }:
        fail(
            "AREA-EVAL-BASELINE-COMPARISON",
            "baseline/candidate comparison contract differs",
        )

    suites = loaded["roleSuites"]
    observed_roles = tuple(suite["roleId"] for suite in suites)
    if observed_roles != TARGET_ROLES or len(set(observed_roles)) != len(
        observed_roles
    ):
        fail("AREA-EVAL-ROLE-SET", "role suites must equal the ordered 12-role set")

    high_risk_count = 0
    for suite in suites:
        role_id = suite["roleId"]
        expected_risk = "high" if role_id in HIGH_RISK_ROLES else "standard"
        if suite["riskClass"] != expected_risk:
            fail("AREA-EVAL-RISK", f"{role_id} riskClass differs")
        if suite["suiteId"] != f"eval/{role_id}":
            fail("AREA-EVAL-SUITE", f"{role_id} suiteId differs")
        if suite["fixtureManifestId"] != f"eval/{role_id}/fixtures":
            fail("AREA-EVAL-FIXTURE", f"{role_id} fixtureManifestId differs")
        if any(
            suite[field] != "1.0.0"
            for field in (
                "suiteVersion",
                "fixtureVersion",
                "graderVersion",
                "rubricVersion",
            )
        ):
            fail("AREA-EVAL-VERSION", f"{role_id} version differs")
        if tuple(suite["fixtureClasses"]) != REQUIRED_FIXTURE_CLASSES:
            fail("AREA-EVAL-FIXTURE-CLASS", f"{role_id} class coverage differs")
        if suite["provenanceClass"] != "repository-contract-only":
            fail("AREA-EVAL-PROVENANCE", f"{role_id} provenance differs")
        if suite["privacyClass"] != "synthetic-or-redacted-only":
            fail("AREA-EVAL-PRIVACY", f"{role_id} privacy class differs")
        if role_id in HIGH_RISK_ROLES:
            high_risk_count += 1
            if suite["independentAdjudicationRequired"] is not True:
                fail(
                    "AREA-EVAL-ADJUDICATION",
                    f"{role_id} lacks independent adjudication",
                )
        if (
            suite["corpusState"] != "DEFER"
            or suite["evaluationDecision"] != "DEFER"
            or suite["rollbackState"] != "DEFER"
        ):
            fail(
                "AREA-EVAL-RUNTIME-PRECLAIM",
                f"{role_id} claims unobserved evaluation evidence",
            )

    return {
        "roles": len(suites),
        "fixtureClasses": len(loaded["requiredFixtureClasses"]),
        "memoryClasses": len(loaded["memoryClasses"]),
        "highRiskRoles": high_risk_count,
        "promotionBlocks": len(promotion["blockingEvents"]),
    }


def apply_mutation(contract: dict[str, Any], name: str) -> None:
    """Apply a named synthetic negative mutation in place."""
    if name == "missing-handoff-class":
        contract["roleSuites"][0]["fixtureClasses"].remove("handoff")
    elif name == "suite-version-drift":
        contract["roleSuites"][0]["suiteVersion"] = "2.0.0"
    elif name == "grader-version-drift":
        contract["roleSuites"][1]["graderVersion"] = "2.0.0"
    elif name == "baseline-suite-mismatch":
        contract["evaluationRecordContract"]["baselineCandidate"][
            "sameSuiteVersionRequired"
        ] = False
    elif name == "baseline-grader-mismatch":
        contract["evaluationRecordContract"]["baselineCandidate"][
            "sameGraderVersionRequired"
        ] = False
    elif name == "high-risk-self-adjudicated":
        contract["roleSuites"][0]["independentAdjudicationRequired"] = False
    elif name.endswith("-not-blocking"):
        event = name.removesuffix("-not-blocking")
        if event not in PROMOTION_BLOCKING_EVENTS:
            fail("AREA-EVAL-FIXTURE", f"unknown blocking event {event!r}")
        contract["promotionPolicy"]["blockingEvents"].remove(event)
    elif name == "runtime-pass-preclaim":
        contract["authority"]["runtime"] = "PASS"
    elif name == "decision-pass-preclaim":
        contract["roleSuites"][0]["evaluationDecision"] = "PASS"
    elif name == "provider-value-preclaim":
        contract["evaluationRecordContract"]["providerExecution"][
            "provider"
        ] = "codex"
    elif name == "raw-prompt-allowed":
        contract["privacyPolicy"]["rawPromptsAllowed"] = True
    elif name == "private-diagnostics-allowed":
        contract["privacyPolicy"]["privateDiagnosticsAllowed"] = True
    elif name == "secret-like-value":
        contract["evaluationRecordContract"]["rollback"][
            "reference"
        ] = "sk-" + "synthetic-fixture"
    elif name == "unexpected-closed-field":
        contract["unexpected"] = True
    else:
        fail("AREA-EVAL-FIXTURE", f"unknown mutation {name!r}")


def _duplicate_key_probe() -> None:
    decode_json_text(
        '{"contractId":"first","contractId":"second"}',
        "<duplicate-contract-json-key>",
    )


def run_self_test(root: Path) -> tuple[list[str], int]:
    """Run the production baseline and every named synthetic mutation."""
    root = root.resolve()
    contract = load_json(root, CONTRACT_PATH)
    fixture = load_json(root, FIXTURE_PATH)
    if not isinstance(fixture, dict) or not isinstance(
        fixture.get("mutations"), list
    ):
        fail("AREA-EVAL-FIXTURE", "fixture root or mutations are malformed")

    failures: list[str] = []
    try:
        counts = validate_contract(root, contract)
    except EvaluationContractError as exc:
        return [f"baseline: expected PASS, got {exc.code}: {exc.detail}"], 0
    if counts != fixture.get("expectedCounts"):
        failures.append(
            f"baseline counts: expected {fixture.get('expectedCounts')!r}, "
            f"got {counts!r}"
        )

    seen: set[str] = set()
    for case in fixture["mutations"]:
        if not isinstance(case, dict):
            failures.append("mutation entry is not an object")
            continue
        name = case.get("name")
        expected = case.get("expectedRule")
        if not isinstance(name, str) or not isinstance(expected, str):
            failures.append(f"malformed mutation entry: {case!r}")
            continue
        if name in seen:
            failures.append(f"{name}: duplicate mutation name")
            continue
        seen.add(name)
        try:
            if name == "duplicate-contract-json-key":
                _duplicate_key_probe()
            else:
                mutated = copy.deepcopy(contract)
                apply_mutation(mutated, name)
                validate_contract(root, mutated)
        except EvaluationContractError as exc:
            if exc.code != expected:
                failures.append(f"{name}: expected {expected}, got {exc.code}")
        else:
            failures.append(f"{name}: mutation unexpectedly passed")
    return failures, len(seen)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.self_test:
            failures, cases = run_self_test(root)
            if failures:
                for item in failures:
                    print(f"ERR AREA-EVAL-SELF-TEST {item}", file=sys.stderr)
                return 1
            print(f"[PASS] agent evaluations self-test passed: cases={cases}")
            return 0
        counts = validate_contract(root)
        print(
            "[PASS] agent evaluations validation passed: "
            f"roles={counts['roles']} "
            f"fixtureClasses={counts['fixtureClasses']} "
            f"highRiskRoles={counts['highRiskRoles']} "
            f"promotionBlocks={counts['promotionBlocks']}"
        )
        return 0
    except EvaluationContractError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
