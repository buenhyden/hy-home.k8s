#!/usr/bin/env python3
"""Validate the closed Spec 044 agent-evaluation contract."""

from __future__ import annotations

import argparse
import copy
import hashlib
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
HARNESS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
ROSTER_ADMISSION_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-roster-admission.json"
)
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
    "state": "repository-static-evaluation-ready",
    "evidenceKind": "repo-static",
    "execution": "DEFER",
    "runtime": "DEFER",
    "providerResolution": "DEFER",
    "authentication": "DEFER",
    "liveAction": "DEFER",
    "evaluationDecision": "DEFER",
}
CONTRACT_VERSION = "1.1.0"
ROLE_CONTRACT_VERSION = "1.0.0"
CORPUS_VERSION = "1.0.0"
ROLLBACK_CANDIDATES = ("docs-researcher", "quality-engineer")
VERIFIED_INCUMBENT = {
    "roleCount": 10,
    "surfaceCount": 3,
    "adapterCount": 30,
    "commit": "e324d4c1fa49ef7e508fa07c32e7f054f5a3a05e",  # pragma: allowlist secret
}
ROLLBACK_STEPS = (
    "freeze-projection",
    "remove-two-candidates-and-gemini-projection",
    "restore-verified-10-3-30",
    "rerun-static-gates",
)
SOURCE_ROLLBACK = {
    "state": "armed",
    "restoreInventory": "10/3/30",
    "reproducible": True,
    "executed": False,
    "triggers": [
        "critical evaluation miss",
        "scope or permission escape",
        "secret or private-data exposure",
        "failed adapter parity",
    ],
    "procedure": [
        (
            "freeze repository-static projection changes and keep admission "
            "and runtime evidence deferred"
        ),
        (
            "remove only the two projected candidate roles and the Gemini "
            "repository-static projections"
        ),
        "restore the last verified 10/3/30 role and surface inventory",
        "rerun repository-static roster and evaluation gates",
    ],
}
DEFERRED_EVIDENCE = {
    "providerDiscovery": "DEFER",
    "authentication": "DEFER",
    "runtime": "DEFER",
    "modelResolution": "DEFER",
    "hostedCi": "DEFER",
    "remoteAction": "DEFER",
    "liveAction": "DEFER",
    "evaluationExecution": "DEFER",
    "evaluationAdjudication": "DEFER",
}
UNRESOLVED_BLOCKERS = (
    "provider-discovery",
    "authentication",
    "runtime",
    "model-resolution",
    "hosted-ci",
    "remote-action",
    "live-action",
    "evaluation-execution",
    "evaluation-adjudication",
)
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
ROLE_BOUNDARY_DIGESTS = {
    "supervisor": (
        "sha256:bce61c42dfa08e5dc6ea079998a0e51b4dd1371433cce255d16d78c0323a2000"  # pragma: allowlist secret
    ),
    "code-reviewer": (
        "sha256:22f34b5e48570846eaab7b9f8ad1c3e1860c17f3cd24db424e6827ebace68236"  # pragma: allowlist secret
    ),
    "doc-writer": (
        "sha256:6ded335727495f0871cc812cdf391b25390e10b57dbc939e148f4913989fc250"  # pragma: allowlist secret
    ),
    "gitops-reviewer": (
        "sha256:b48402edf41fdc4b81be80dce64d5f970b2b958c4d600088d9c5d1f144b49367"  # pragma: allowlist secret
    ),
    "incident-responder": (
        "sha256:cb97edddf3814c5ad693dcc028f668876a156da1604419b7ec42aab352c087e3"  # pragma: allowlist secret
    ),
    "k8s-implementer": (
        "sha256:7d4741ba114895715989daed0ce502bfd0521a3b06e0e895161d5feb33d5f017"  # pragma: allowlist secret
    ),
    "network-reviewer": (
        "sha256:f943aa2727cb7b068200206ad5e11d9454783a11db3b16a35d71ec7c26baf203"  # pragma: allowlist secret
    ),
    "observability-reviewer": (
        "sha256:e574dd2fed77246e5a6219feb2c30624bf74208ea06d52becba64de65d4b0faf"  # pragma: allowlist secret
    ),
    "security-auditor": (
        "sha256:42bfb4379111a86edb7cf8b1920fb6b02f15fca0bcb6b854ed5a5f36029d4ad9"  # pragma: allowlist secret
    ),
    "wiki-curator": (
        "sha256:e94f6983c6249b886e7e8772dcb60491f598cf1639a786212159d8df176fc485"  # pragma: allowlist secret
    ),
    "docs-researcher": (
        "sha256:327f33b8a67e37ef0736c29331515cc4ed9a086645f1d67cb626fd40a50e61e0"  # pragma: allowlist secret
    ),
    "quality-engineer": (
        "sha256:d0497f6958f45f398e390f9da8e077f0c3c656944e882c2d7f1a5159f0e8c75b"  # pragma: allowlist secret
    ),
}
ROLE_SCENARIO_MARKERS = {
    "supervisor": (
        "dependency routing",
        "broader child authority",
        "unresolved ownership",
        "k8s-implementer",
    ),
    "code-reviewer": (
        "correctness findings",
        "mutate the reviewed validator",
        "security-critical defect",
        "security-auditor",
    ),
    "doc-writer": (
        "profile-compliant document",
        "invent implementation evidence",
        "canonical owner is unresolved",
        "docs-researcher",
    ),
    "gitops-reviewer": (
        "Kustomize reconciliation review",
        "claim live reconciliation",
        "rendered target is unavailable",
        "k8s-implementer",
    ),
    "incident-responder": (
        "timestamped incident timeline",
        "declare an unobserved root cause",
        "evidence cannot support causality",
        "security-auditor",
    ),
    "k8s-implementer": (
        "authorized manifest patch",
        "apply directly to the live cluster",
        "manifest ownership is ambiguous",
        "gitops-reviewer",
    ),
    "network-reviewer": (
        "routing and isolation analysis",
        "claim live DNS resolution",
        "TLS ownership is unresolved",
        "security-auditor",
    ),
    "observability-reviewer": (
        "SLO and alert analysis",
        "claim unobserved alert health",
        "telemetry evidence is missing",
        "gitops-reviewer",
    ),
    "security-auditor": (
        "least-privilege findings",
        "expose secret material",
        "secret-handling evidence is incomplete",
        "k8s-implementer",
    ),
    "wiki-curator": (
        "wiki owner-link update",
        "duplicate a canonical owner",
        "canonical owner cannot be resolved",
        "doc-writer",
    ),
    "docs-researcher": (
        "source reconciliation memo",
        "present an unverified secondary claim as primary",
        "dated primary evidence is unavailable",
        "doc-writer",
    ),
    "quality-engineer": (
        "acceptance-to-fixture report",
        "weaken a failing gate",
        "reproduction is not deterministic",
        "code-reviewer",
    ),
}


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


def _resolve_repository_root(root: Path) -> Path:
    """Resolve a repository root only after rejecting lexical symlink paths."""
    raw_root = Path(root)
    if any(part == ".." for part in raw_root.parts):
        fail("AREA-EVAL-INPUT", "repository root is invalid", exit_code=2)
    try:
        absolute_root = Path(os.path.abspath(os.fspath(raw_root)))
    except (OSError, TypeError, ValueError):
        fail("AREA-EVAL-INPUT", "repository root is unavailable", exit_code=2)

    current = Path(absolute_root.anchor)
    components = absolute_root.parts[1:]
    paths = [current]
    for part in components:
        current = current / part
        paths.append(current)
    for candidate in paths:
        try:
            metadata = os.lstat(candidate)
        except OSError:
            fail(
                "AREA-EVAL-INPUT",
                "repository root is unavailable",
                exit_code=2,
            )
        if stat.S_ISLNK(metadata.st_mode):
            fail(
                "AREA-EVAL-INPUT",
                "repository root path contains a symlink",
                exit_code=2,
            )
        if not stat.S_ISDIR(metadata.st_mode):
            fail(
                "AREA-EVAL-INPUT",
                "repository root is not a real directory",
                exit_code=2,
            )

    try:
        real_root = Path(os.path.realpath(absolute_root, strict=True))
    except (OSError, TypeError, ValueError):
        fail("AREA-EVAL-INPUT", "repository root is unavailable", exit_code=2)
    if real_root != absolute_root:
        fail(
            "AREA-EVAL-INPUT",
            "repository root path is not real",
            exit_code=2,
        )
    return absolute_root


def _resolve_regular_file(root: Path, relative: PurePosixPath) -> Path:
    repository_root = _resolve_repository_root(root)

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


def _text_digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _targeted_preflight(contract: dict[str, Any]) -> None:
    """Emit stable semantic rules before generic schema diagnostics."""
    if contract.get("contractVersion") not in (None, CONTRACT_VERSION):
        fail(
            "AREA-EVAL-VERSION",
            f"contractVersion must equal {CONTRACT_VERSION}",
        )
    if "versionHistory" in contract and contract.get("versionHistory") != [
        {
            "contractVersion": "1.0.0",
            "state": "superseded-string-manifest-scaffold",
            "evidenceScope": "repository-static-schema-only",
            "admissionDisposition": "DEFER",
        },
        {
            "contractVersion": "1.1.0",
            "state": "current-corpus-ready",
            "evidenceScope": "repository-static-evaluation-readiness",
            "admissionDisposition": "DEFER",
        },
    ]:
        fail("AREA-EVAL-VERSION", "version history differs")

    authority = _mapping(contract.get("authority"))
    if authority and any(
        key in authority and authority[key] != expected
        for key, expected in DEFERRED_AUTHORITY.items()
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "authority must remain repository-static evaluation-ready and DEFER",
        )

    harness_binding = _mapping(contract.get("harnessBinding"))
    if harness_binding and harness_binding != {
        "contractPath": str(HARNESS_PATH),
        "contractId": "hy-home.k8s/agent-harness",
        "contractVersion": ROLE_CONTRACT_VERSION,
        "roleSetSource": "#/canonicalRoles",
        "evalSuiteField": "evalSuite.id",
    }:
        fail(
            "AREA-EVAL-HARNESS-BINDING",
            "declared harness binding differs",
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
        adjudication.get("readinessDisposition") != "PASS"
        or adjudication.get("evaluationDisposition") != "DEFER"
        or adjudication.get("admissionDisposition") != "DEFER"
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "readiness PASS must not preclaim evaluation or admission PASS",
        )
    rollback = _mapping(record.get("rollback"))
    if rollback and (
        rollback.get("status") != "armed-not-executed"
        or rollback.get("execution") != "DEFER"
        or rollback.get("incumbent") != "10/3/30"
    ):
        fail(
            "AREA-EVAL-ROLLBACK",
            "rollback contract must remain armed but unexecuted",
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
            value != CORPUS_VERSION for value in version_fields
        ):
            fail(
                "AREA-EVAL-VERSION",
                f"{suite.get('roleId', '<unknown>')} versions must equal 1.0.0",
            )
        role_id = suite.get("roleId")
        if isinstance(role_id, str) and (
            suite.get("suiteId") not in (None, f"eval/{role_id}/v1")
            or suite.get("roleContractVersion")
            not in (None, ROLE_CONTRACT_VERSION)
        ):
            fail(
                "AREA-EVAL-HARNESS-BINDING",
                f"{role_id} suite or role-contract binding differs",
            )
        if suite.get("evaluationDisposition") not in (None, "DEFER"):
            fail(
                "AREA-EVAL-RUNTIME-PRECLAIM",
                f"{suite.get('roleId', '<unknown>')} preclaims evaluation evidence",
            )
        if suite.get("corpusState") not in (
            None,
            "repository-static-evaluation-ready",
        ):
            fail(
                "AREA-EVAL-MANIFEST",
                f"{suite.get('roleId', '<unknown>')} corpus state differs",
            )
        if (
            suite.get("riskClass") == "high"
            and suite.get("independentAdjudicationRequired") is not True
        ):
            fail(
                "AREA-EVAL-ADJUDICATION",
                f"{suite.get('roleId', '<unknown>')} requires independent adjudication",
            )

    manifest = _mapping(contract.get("corpusManifest"))
    records = manifest.get("records")
    if isinstance(records, list) and len(records) != 48:
        fail("AREA-EVAL-MANIFEST", "corpus manifest must contain 48 records")
    for item in _list(records):
        if not isinstance(item, dict):
            continue
        if (
            item.get("fixtureVersion") not in (None, CORPUS_VERSION)
            or item.get("suiteVersion") not in (None, CORPUS_VERSION)
            or item.get("roleContractVersion")
            not in (None, ROLE_CONTRACT_VERSION)
        ):
            fail(
                "AREA-EVAL-VERSION",
                f"{item.get('fixtureId', '<unknown>')} version differs",
            )
        if item.get("privacyClass") not in (None, "synthetic-only"):
            fail(
                "AREA-EVAL-PRIVACY",
                f"{item.get('fixtureId', '<unknown>')} privacy class differs",
            )

    adjudication_records = _mapping(
        contract.get("adjudicationReadiness")
    ).get("records")
    if isinstance(adjudication_records, list) and len(
        adjudication_records
    ) != 12:
        fail(
            "AREA-EVAL-ADJUDICATION",
            "adjudication readiness must cover 12 roles",
        )
    for item in _list(adjudication_records):
        if not isinstance(item, dict):
            continue
        role_id = item.get("roleId")
        if (
            item.get("adjudicatorRoleId") == role_id
            or _mapping(item.get("independenceProof")).get("sameRole") is True
        ):
            fail(
                "AREA-EVAL-ADJUDICATION",
                f"{role_id or '<unknown>'} cannot self-adjudicate",
            )
        if (
            role_id in HIGH_RISK_ROLES
            and item.get("independenceRequired") is not True
        ):
            fail(
                "AREA-EVAL-ADJUDICATION",
                f"{role_id} requires independence proof",
            )
        if (
            item.get("evaluationDisposition") not in (None, "DEFER")
            or item.get("admissionDisposition") not in (None, "DEFER")
        ):
            fail(
                "AREA-EVAL-RUNTIME-PRECLAIM",
                f"{role_id or '<unknown>'} adjudication preclaims a result",
            )
        if item.get("rubricVersion") not in (None, CORPUS_VERSION):
            fail(
                "AREA-EVAL-ADJUDICATION",
                f"{role_id or '<unknown>'} rubric version differs",
            )

    rollback_records = contract.get("rollbackRecords")
    if isinstance(rollback_records, list) and len(rollback_records) != 2:
        fail(
            "AREA-EVAL-ROLLBACK",
            "rollback readiness must cover two candidates",
        )
    for item in _list(rollback_records):
        if not isinstance(item, dict):
            continue
        incumbent = _mapping(item.get("incumbent"))
        incumbent_differs = any(
            key in incumbent and incumbent[key] != expected
            for key, expected in VERIFIED_INCUMBENT.items()
        )
        if (
            incumbent_differs
            or item.get("status") not in (None, "armed-not-executed")
            or item.get("executed") not in (None, False)
            or item.get("executionEvidence") not in (None, "DEFER")
            or (
                isinstance(item.get("triggers"), list)
                and tuple(item["triggers"]) != PROMOTION_BLOCKING_EVENTS
            )
        ):
            fail(
                "AREA-EVAL-ROLLBACK",
                f"{item.get('candidateRoleId', '<unknown>')} rollback differs",
            )

    decision = _mapping(contract.get("finalAdmissionDecision"))
    if decision and (
        decision.get("readinessDisposition") != "PASS"
        or decision.get("evaluationDisposition") != "DEFER"
        or decision.get("admissionDisposition") != "DEFER"
        or decision.get("validatorReadinessPassIsAdmissionPass") is not False
        or any(
            value != "DEFER"
            for value in _mapping(decision.get("deferredEvidence")).values()
        )
        or (
            isinstance(decision.get("unresolvedEvidenceBlockers"), list)
            and tuple(decision["unresolvedEvidenceBlockers"])
            != UNRESOLVED_BLOCKERS
        )
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "readiness PASS must remain separate from evaluation/admission",
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
    if fixture["identityFields"] != [
        "fixtureId",
        "fixtureVersion",
        "roleId",
        "roleContractVersion",
        "fixtureClass",
    ]:
        fail("AREA-EVAL-RECORD-CONTRACT", "fixture identity fields differ")
    if fixture["requiredClasses"] != list(REQUIRED_FIXTURE_CLASSES):
        fail("AREA-EVAL-FIXTURE-CLASS", "record fixture classes differ")
    if fixture["evidenceFields"] != [
        "scenarioSummary",
        "provenanceClass",
        "privacyClass",
        "riskClass",
        "inputDigest",
        "expectedBoundaryBehavior",
    ]:
        fail("AREA-EVAL-RECORD-CONTRACT", "fixture evidence fields differ")
    if fixture["digest"] != {
        "field": "inputDigest",
        "algorithm": "sha256",
        "format": "sha256:<64-lowercase-hex>",
        "source": "utf8-scenario-summary",
        "required": True,
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
        "readinessDisposition": "PASS",
        "evaluationDisposition": "DEFER",
        "admissionDisposition": "DEFER",
        "independentForHighRisk": True,
    }:
        fail("AREA-EVAL-ADJUDICATION", "adjudication field contract differs")
    if record["rollback"] != {
        "status": "armed-not-executed",
        "execution": "DEFER",
        "incumbent": "10/3/30",
    }:
        fail("AREA-EVAL-ROLLBACK", "rollback field contract differs")


def _validate_harness_binding(
    contract: dict[str, Any],
    harness: dict[str, Any],
) -> None:
    expected_binding = {
        "contractPath": str(HARNESS_PATH),
        "contractId": "hy-home.k8s/agent-harness",
        "contractVersion": ROLE_CONTRACT_VERSION,
        "roleSetSource": "#/canonicalRoles",
        "evalSuiteField": "evalSuite.id",
    }
    if contract["harnessBinding"] != expected_binding:
        fail("AREA-EVAL-HARNESS-BINDING", "declared harness binding differs")
    if (
        harness.get("contractId") != expected_binding["contractId"]
        or harness.get("contractVersion") != ROLE_CONTRACT_VERSION
    ):
        fail("AREA-EVAL-HARNESS-BINDING", "harness identity or version differs")
    harness_roles = _list(harness.get("canonicalRoles"))
    if tuple(
        item.get("id") for item in harness_roles if isinstance(item, dict)
    ) != TARGET_ROLES:
        fail("AREA-EVAL-HARNESS-BINDING", "harness role set differs")
    for index, (suite, harness_role) in enumerate(
        zip(contract["roleSuites"], harness_roles, strict=True)
    ):
        role_id = TARGET_ROLES[index]
        eval_suite = _mapping(harness_role.get("evalSuite"))
        if (
            suite["roleId"] != role_id
            or suite["roleContractVersion"] != ROLE_CONTRACT_VERSION
            or suite["suiteId"] != eval_suite.get("id")
            or suite["suiteId"] != f"eval/{role_id}/v1"
            or ROLE_SCENARIO_MARKERS[role_id][3]
            not in _list(harness_role.get("handoffs"))
        ):
            fail(
                "AREA-EVAL-HARNESS-BINDING",
                f"{role_id} harness suite binding differs",
            )


def _validate_manifest(contract: dict[str, Any]) -> list[dict[str, Any]]:
    manifest = contract["corpusManifest"]
    records = manifest["records"]
    if (
        manifest["manifestId"] != "hy-home.k8s/agent-evaluation-corpus/v1"
        or manifest["manifestVersion"] != CORPUS_VERSION
        or manifest["digestAlgorithm"] != "sha256-canonical-json"
        or manifest["recordCount"] != 48
        or len(records) != 48
    ):
        fail("AREA-EVAL-MANIFEST", "manifest identity, version, or count differs")
    if manifest["manifestDigest"] != _canonical_digest(records):
        fail("AREA-EVAL-DIGEST", "manifest digest differs")

    expected_pairs = tuple(
        (role_id, fixture_class)
        for role_id in TARGET_ROLES
        for fixture_class in REQUIRED_FIXTURE_CLASSES
    )
    observed_pairs = tuple(
        (item["roleId"], item["fixtureClass"]) for item in records
    )
    fixture_ids = [item["fixtureId"] for item in records]
    if observed_pairs != expected_pairs:
        fail(
            "AREA-EVAL-MANIFEST",
            "manifest must equal the ordered 12-role by four-class matrix",
        )
    if len(fixture_ids) != len(set(fixture_ids)):
        fail("AREA-EVAL-MANIFEST", "manifest fixture identities are not unique")

    for item in records:
        role_id = item["roleId"]
        fixture_class = item["fixtureClass"]
        expected_risk = "high" if role_id in HIGH_RISK_ROLES else "standard"
        if (
            item["suiteId"] != f"eval/{role_id}/v1"
            or item["suiteVersion"] != CORPUS_VERSION
            or item["roleContractVersion"] != ROLE_CONTRACT_VERSION
            or item["fixtureVersion"] != CORPUS_VERSION
            or item["fixtureId"]
            != f"eval/{role_id}/v1/fixtures/{fixture_class}/v1"
        ):
            fail(
                "AREA-EVAL-MANIFEST",
                f"{role_id}/{fixture_class} identity or version differs",
            )
        if item["inputDigest"] != _text_digest(item["scenarioSummary"]):
            fail(
                "AREA-EVAL-DIGEST",
                f"{role_id}/{fixture_class} scenario digest differs",
            )
        if (
            item["provenanceClass"] != "repository-synthetic"
            or item["privacyClass"] != "synthetic-only"
            or item["riskClass"] != expected_risk
        ):
            fail(
                "AREA-EVAL-PRIVACY",
                f"{role_id}/{fixture_class} evidence class differs",
            )
        behavior = item["expectedBoundaryBehavior"]
        boundary_payload = {
            key: behavior[key]
            for key in (
                "allowedPaths",
                "allowedTools",
                "prohibitedActions",
            )
        }
        marker_index = REQUIRED_FIXTURE_CLASSES.index(fixture_class)
        marker = ROLE_SCENARIO_MARKERS[role_id][marker_index]
        if (
            re.match(
                r"^Synthetic .* boundary case for ",
                item["scenarioSummary"],
            )
            or any(
                path.startswith("governed:")
                for path in behavior["allowedPaths"]
            )
            or _canonical_digest(boundary_payload)
            != ROLE_BOUNDARY_DIGESTS[role_id]
            or marker not in item["scenarioSummary"]
            or marker not in behavior["stopHandoffExpectation"]
        ):
            fail(
                "AREA-EVAL-BOUNDARY",
                f"{role_id}/{fixture_class} uses generic or mismatched boundaries",
            )

    for index, suite in enumerate(contract["roleSuites"]):
        role_id = suite["roleId"]
        role_records = [
            item for item in records if item["roleId"] == role_id
        ]
        expected_risk = "high" if role_id in HIGH_RISK_ROLES else "standard"
        if (
            suite["fixtureManifestId"] != f"eval/{role_id}/v1/fixtures/v1"
            or suite["fixtureRecordIds"]
            != [item["fixtureId"] for item in role_records]
            or suite["fixtureManifestDigest"] != _canonical_digest(role_records)
        ):
            fail(
                "AREA-EVAL-MANIFEST",
                f"{role_id} suite-to-manifest binding differs",
            )
        if (
            tuple(suite["fixtureClasses"]) != REQUIRED_FIXTURE_CLASSES
            or suite["riskClass"] != expected_risk
            or suite["provenanceClass"] != "repository-synthetic"
            or suite["privacyClass"] != "synthetic-only"
            or suite["corpusState"]
            != "repository-static-evaluation-ready"
            or suite["evaluationDisposition"] != "DEFER"
            or suite["adjudicationRef"]
            != f"#/adjudicationReadiness/records/{index}"
        ):
            fail("AREA-EVAL-MANIFEST", f"{role_id} suite metadata differs")
    return records


def _validate_adjudication(contract: dict[str, Any]) -> int:
    readiness = contract["adjudicationReadiness"]
    records = readiness["records"]
    if (
        readiness["readinessVersion"] != CORPUS_VERSION
        or tuple(item["roleId"] for item in records) != TARGET_ROLES
    ):
        fail("AREA-EVAL-ADJUDICATION", "adjudication role coverage differs")
    for item in records:
        role_id = item["roleId"]
        adjudicator = item["adjudicatorRoleId"]
        expected_required = role_id in HIGH_RISK_ROLES
        if adjudicator == role_id or adjudicator not in TARGET_ROLES:
            fail("AREA-EVAL-ADJUDICATION", f"{role_id} self-adjudicates")
        if (
            item["adjudicationId"] != f"adjudication/{role_id}/v1"
            or item["adjudicationVersion"] != CORPUS_VERSION
            or item["adjudicatorId"] != f"adjudicator/{adjudicator}/v1"
            or item["adjudicatorOwner"] != "workspace-quality-governance"
            or item["roleSeparation"] != "independent-canonical-role"
            or item["independenceRequired"] is not expected_required
            or item["independenceProof"]
            != {
                "candidateRoleId": role_id,
                "adjudicatorRoleId": adjudicator,
                "sameRole": False,
                "basis": (
                    "distinct-canonical-role-and-no-result-"
                    "execution-authority"
                ),
            }
        ):
            fail(
                "AREA-EVAL-ADJUDICATION",
                f"{role_id} separation or independence evidence differs",
            )
        if (
            item["rubricVersion"] != CORPUS_VERSION
            or item["rubricRef"] != "#/promotionPolicy"
            or item["evidenceDigest"]
            != _text_digest(item["evidenceSummary"])
            or item["reviewScope"]
            != "repository-static-corpus-readiness-only"
            or item["readinessDisposition"] != "PASS"
            or item["evaluationDisposition"] != "DEFER"
            or item["admissionDisposition"] != "DEFER"
        ):
            fail(
                "AREA-EVAL-ADJUDICATION",
                f"{role_id} readiness evidence differs",
            )
    return sum(item["independenceRequired"] is True for item in records)


def _validate_rollback(
    contract: dict[str, Any],
    roster_admission: dict[str, Any],
) -> None:
    records = contract["rollbackRecords"]
    if tuple(item["candidateRoleId"] for item in records) != ROLLBACK_CANDIDATES:
        fail("AREA-EVAL-ROLLBACK", "rollback candidate set differs")
    candidates = roster_admission.get("candidates")
    if (
        not isinstance(candidates, list)
        or len(candidates) != len(ROLLBACK_CANDIDATES)
    ):
        fail("AREA-EVAL-ROLLBACK", "source candidate set differs")
    for index, item in enumerate(records):
        role_id = ROLLBACK_CANDIDATES[index]
        procedure = item["procedure"]
        candidate = candidates[index]
        if not isinstance(candidate, dict):
            fail("AREA-EVAL-ROLLBACK", f"{role_id} source candidate differs")
        source_rollback = candidate.get("rollback")
        if (
            candidate.get("roleId") != role_id
            or source_rollback != SOURCE_ROLLBACK
        ):
            fail("AREA-EVAL-ROLLBACK", f"{role_id} source rollback differs")
        source_path = str(ROSTER_ADMISSION_PATH)
        candidate_reference = f"{source_path}#/candidates/{index}"
        rollback_reference = f"{candidate_reference}/rollback"
        source_binding = {
            "contractPath": source_path,
            "candidateReference": candidate_reference,
            "candidateRoleId": role_id,
            "rollbackReference": rollback_reference,
            "rollbackDigest": _canonical_digest(source_rollback),
        }
        if (
            item["rollbackId"] != f"rollback/{role_id}/v1"
            or item["rollbackVersion"] != CORPUS_VERSION
            or item["incumbent"] != VERIFIED_INCUMBENT
            or tuple(item["triggers"]) != PROMOTION_BLOCKING_EVENTS
            or procedure["reference"] != rollback_reference
            or tuple(procedure["steps"]) != ROLLBACK_STEPS
            or procedure["digest"] != _canonical_digest(list(ROLLBACK_STEPS))
            or item["sourceBinding"] != source_binding
            or item["status"] != "armed-not-executed"
            or item["executed"] is not False
            or item["executionBoundary"]
            != "repository-static-plan-only-no-rollback-executed"
            or item["executionEvidence"] != "DEFER"
        ):
            fail("AREA-EVAL-ROLLBACK", f"{role_id} rollback evidence differs")


def _validate_final_decision(contract: dict[str, Any]) -> None:
    decision = contract["finalAdmissionDecision"]
    if (
        decision["decisionId"]
        != "spec044/repository-static-roster-admission/v1"
        or decision["decisionVersion"] != CORPUS_VERSION
        or decision["scope"] != "repository-static-roster-admission"
        or decision["readinessDisposition"] != "PASS"
        or decision["evaluationDisposition"] != "DEFER"
        or decision["admissionDisposition"] != "DEFER"
        or decision["validatorReadinessPassIsAdmissionPass"] is not False
        or tuple(decision["unresolvedEvidenceBlockers"])
        != UNRESOLVED_BLOCKERS
        or decision["deferredEvidence"] != DEFERRED_EVIDENCE
        or "not evaluation or admission PASS" not in decision["statement"]
    ):
        fail(
            "AREA-EVAL-RUNTIME-PRECLAIM",
            "final admission decision is not evidence-honest",
        )


def validate_contract(
    root: Path,
    contract: dict[str, Any] | None = None,
    harness_contract: dict[str, Any] | None = None,
    roster_admission_contract: dict[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the production contract or an injected negative fixture."""
    root = _resolve_repository_root(root)
    loaded = load_json(root, CONTRACT_PATH) if contract is None else contract
    if not isinstance(loaded, dict):
        fail("AREA-EVAL-CONTRACT-TYPE", "contract root must be an object")
    _scan_sensitive_payload(loaded)
    _targeted_preflight(loaded)
    _validate_schema(root, loaded)

    harness = (
        load_json(root, HARNESS_PATH)
        if harness_contract is None
        else harness_contract
    )
    if not isinstance(harness, dict):
        fail(
            "AREA-EVAL-HARNESS-BINDING",
            "harness contract root must be an object",
        )
    roster_admission = (
        load_json(root, ROSTER_ADMISSION_PATH)
        if roster_admission_contract is None
        else roster_admission_contract
    )
    if not isinstance(roster_admission, dict):
        fail(
            "AREA-EVAL-ROLLBACK",
            "roster admission source root must be an object",
        )

    if (
        loaded["contractVersion"] != CONTRACT_VERSION
        or loaded["state"] != "repository-static-evaluation-ready"
    ):
        fail("AREA-EVAL-VERSION", "current contract state or version differs")
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

    record_contract = loaded["evaluationRecordContract"]
    _validate_record_contract(record_contract)
    if record_contract["baselineCandidate"] != {
        "baseline": "DEFER",
        "candidate": "DEFER",
        "sameSuiteVersionRequired": True,
        "sameGraderVersionRequired": True,
    }:
        fail(
            "AREA-EVAL-BASELINE-COMPARISON",
            "baseline/candidate comparison contract differs",
        )

    _validate_harness_binding(loaded, harness)
    records = _validate_manifest(loaded)
    high_risk_count = _validate_adjudication(loaded)
    _validate_rollback(loaded, roster_admission)
    _validate_final_decision(loaded)

    return {
        "roles": len(loaded["roleSuites"]),
        "fixtureClasses": len(loaded["requiredFixtureClasses"]),
        "corpusRecords": len(records),
        "memoryClasses": len(loaded["memoryClasses"]),
        "highRiskRoles": high_risk_count,
        "adjudicationRecords": len(
            loaded["adjudicationReadiness"]["records"]
        ),
        "rollbackRecords": len(loaded["rollbackRecords"]),
        "promotionBlocks": len(promotion["blockingEvents"]),
        "versionHistory": len(loaded["versionHistory"]),
        "deferredEvidence": len(DEFERRED_EVIDENCE),
    }


def _refresh_manifest_digests(
    contract: dict[str, Any],
    role_id: str,
) -> None:
    records = contract["corpusManifest"]["records"]
    contract["corpusManifest"]["manifestDigest"] = _canonical_digest(records)
    role_records = [item for item in records if item["roleId"] == role_id]
    suite = next(
        item for item in contract["roleSuites"] if item["roleId"] == role_id
    )
    suite["fixtureManifestDigest"] = _canonical_digest(role_records)


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
        contract["finalAdmissionDecision"]["evaluationDisposition"] = "PASS"
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
    elif name == "unsupported-contract-version":
        contract["contractVersion"] = "9.9.9"
    elif name == "version-history-drift":
        contract["versionHistory"][1]["contractVersion"] = "1.2.0"
    elif name == "harness-binding-declaration-drift":
        contract["harnessBinding"]["contractVersion"] = "2.0.0"
    elif name == "suite-id-drift":
        contract["roleSuites"][0]["suiteId"] = "eval/supervisor"
    elif name == "role-contract-version-drift":
        contract["roleSuites"][0]["roleContractVersion"] = "2.0.0"
    elif name == "missing-manifest-record":
        contract["corpusManifest"]["records"].pop()
    elif name == "duplicate-manifest-record":
        contract["corpusManifest"]["records"].append(
            copy.deepcopy(contract["corpusManifest"]["records"][0])
        )
    elif name == "extra-manifest-record":
        extra = copy.deepcopy(contract["corpusManifest"]["records"][0])
        extra["fixtureId"] = "eval/supervisor/v1/fixtures/positive/v2"
        contract["corpusManifest"]["records"].append(extra)
    elif name == "cross-role-manifest-record":
        contract["corpusManifest"]["records"][0]["roleId"] = "code-reviewer"
        _refresh_manifest_digests(contract, "supervisor")
    elif name == "wrong-fixture-class":
        contract["corpusManifest"]["records"][0][
            "fixtureClass"
        ] = "handoff"
        _refresh_manifest_digests(contract, "supervisor")
    elif name == "wrong-fixture-version":
        contract["corpusManifest"]["records"][0]["fixtureVersion"] = "2.0.0"
    elif name == "wrong-record-digest":
        contract["corpusManifest"]["records"][0]["inputDigest"] = (
            "sha256:" + ("0" * 64)
        )
    elif name == "wrong-manifest-digest":
        contract["corpusManifest"]["manifestDigest"] = "sha256:" + ("0" * 64)
    elif name == "wrong-suite-manifest-digest":
        contract["roleSuites"][0]["fixtureManifestDigest"] = (
            "sha256:" + ("0" * 64)
        )
    elif name == "privacy-unsafe-record":
        contract["corpusManifest"]["records"][0][
            "privacyClass"
        ] = "production-data"
    elif name == "missing-adjudication-record":
        contract["adjudicationReadiness"]["records"].pop()
    elif name == "adjudication-self-review":
        contract["adjudicationReadiness"]["records"][0][
            "adjudicatorRoleId"
        ] = "supervisor"
    elif name == "adjudication-missing-independence":
        contract["adjudicationReadiness"]["records"][0][
            "independenceRequired"
        ] = False
    elif name == "adjudication-proof-missing":
        del contract["adjudicationReadiness"]["records"][0][
            "independenceProof"
        ]
    elif name == "adjudication-rubric-drift":
        contract["adjudicationReadiness"]["records"][0][
            "rubricVersion"
        ] = "2.0.0"
    elif name == "adjudication-evidence-digest-drift":
        contract["adjudicationReadiness"]["records"][0][
            "evidenceDigest"
        ] = "sha256:" + ("0" * 64)
    elif name == "adjudication-evaluation-pass-preclaim":
        contract["adjudicationReadiness"]["records"][0][
            "evaluationDisposition"
        ] = "PASS"
    elif name == "adjudication-admission-pass-preclaim":
        contract["adjudicationReadiness"]["records"][0][
            "admissionDisposition"
        ] = "PASS"
    elif name == "missing-rollback-record":
        contract["rollbackRecords"].pop()
    elif name == "wrong-rollback-incumbent":
        contract["rollbackRecords"][0]["incumbent"]["roleCount"] = 12
    elif name == "weakened-rollback-triggers":
        contract["rollbackRecords"][0]["triggers"].pop()
    elif name == "executed-rollback":
        contract["rollbackRecords"][0]["executed"] = True
    elif name == "rollback-procedure-digest-drift":
        contract["rollbackRecords"][0]["procedure"]["digest"] = (
            "sha256:" + ("0" * 64)
        )
    elif name == "rollback-reference-drift":
        contract["rollbackRecords"][0]["procedure"]["reference"] = (
            "docs/00.agent-governance/contracts/"
            "agent-roster-admission.json#/candidates/1/rollback"
        )
    elif name == "rollback-status-weakened":
        contract["rollbackRecords"][0]["status"] = "armed"
    elif name == "final-admission-pass-preclaim":
        contract["finalAdmissionDecision"]["admissionDisposition"] = "PASS"
    elif name == "final-evaluation-pass-preclaim":
        contract["finalAdmissionDecision"]["evaluationDisposition"] = "PASS"
    elif name == "readiness-implies-admission":
        contract["finalAdmissionDecision"][
            "validatorReadinessPassIsAdmissionPass"
        ] = True
    elif name == "deferred-blocker-missing":
        contract["finalAdmissionDecision"][
            "unresolvedEvidenceBlockers"
        ].pop()
    elif name == "deferred-evidence-pass-preclaim":
        contract["finalAdmissionDecision"]["deferredEvidence"][
            "runtime"
        ] = "PASS"
    elif name == "placeholder-scenario-residue":
        item = contract["corpusManifest"]["records"][0]
        item["scenarioSummary"] = (
            "Synthetic positive boundary case for supervisor."
        )
        item["inputDigest"] = _text_digest(item["scenarioSummary"])
        _refresh_manifest_digests(contract, "supervisor")
    elif name == "pseudo-path-residue":
        item = contract["corpusManifest"]["records"][0]
        item["expectedBoundaryBehavior"]["allowedPaths"] = [
            "governed:supervisor"
        ]
        _refresh_manifest_digests(contract, "supervisor")
    elif name == "generic-tool-residue":
        item = contract["corpusManifest"]["records"][0]
        item["expectedBoundaryBehavior"]["allowedTools"] = [
            "repository-read"
        ]
        _refresh_manifest_digests(contract, "supervisor")
    elif name == "noncanonical-handoff-target":
        item = contract["corpusManifest"]["records"][3]
        item["scenarioSummary"] = item["scenarioSummary"].replace(
            "k8s-implementer",
            "incident-responder",
        )
        item["inputDigest"] = _text_digest(item["scenarioSummary"])
        item["expectedBoundaryBehavior"][
            "stopHandoffExpectation"
        ] = "handoff to incident-responder without expanding authority"
        _refresh_manifest_digests(contract, "supervisor")
    elif name == "cross-role-boundary-profile":
        source = contract["corpusManifest"]["records"][4][
            "expectedBoundaryBehavior"
        ]
        contract["corpusManifest"]["records"][0][
            "expectedBoundaryBehavior"
        ] = copy.deepcopy(source)
        _refresh_manifest_digests(contract, "supervisor")
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
    root = _resolve_repository_root(root)
    contract = load_json(root, CONTRACT_PATH)
    fixture = load_json(root, FIXTURE_PATH)
    harness = load_json(root, HARNESS_PATH)
    roster_admission = load_json(root, ROSTER_ADMISSION_PATH)
    if not isinstance(fixture, dict) or not isinstance(
        fixture.get("mutations"), list
    ):
        fail("AREA-EVAL-FIXTURE", "fixture root or mutations are malformed")

    failures: list[str] = []
    try:
        counts = validate_contract(
            root,
            contract,
            harness,
            roster_admission,
        )
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
            elif name == "harness-suite-id-drift":
                mutated_harness = copy.deepcopy(harness)
                mutated_harness["canonicalRoles"][0]["evalSuite"][
                    "id"
                ] = "eval/supervisor"
                validate_contract(
                    root,
                    copy.deepcopy(contract),
                    mutated_harness,
                    roster_admission,
                )
            elif name == "source-rollback-drift":
                mutated_source = copy.deepcopy(roster_admission)
                mutated_source["candidates"][0]["rollback"]["procedure"][
                    0
                ] = "skip the projection freeze"
                validate_contract(
                    root,
                    copy.deepcopy(contract),
                    harness,
                    mutated_source,
                )
            else:
                mutated = copy.deepcopy(contract)
                apply_mutation(mutated, name)
                validate_contract(
                    root,
                    mutated,
                    harness,
                    roster_admission,
                )
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
    try:
        root = _resolve_repository_root(args.root)
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
            f"corpusRecords={counts['corpusRecords']} "
            f"highRiskRoles={counts['highRiskRoles']} "
            f"adjudicationRecords={counts['adjudicationRecords']} "
            f"rollbackRecords={counts['rollbackRecords']} "
            f"promotionBlocks={counts['promotionBlocks']} "
            f"deferredEvidence={counts['deferredEvidence']}"
        )
        return 0
    except EvaluationContractError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
