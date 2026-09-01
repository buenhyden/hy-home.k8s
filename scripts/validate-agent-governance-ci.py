#!/usr/bin/env python3
"""Validate closed agent-governance CI topology and local QA evidence."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import re
import stat
import sys
from functools import lru_cache
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any, NoReturn

import yaml
from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-governance-ci.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-governance-ci.schema.json"
)
AFFECTED_PATH = PurePosixPath("scripts/validation/registry.json")
WORKFLOW_PATH = PurePosixPath(".github/workflows/ci.yml")
PRE_COMMIT_PATH = PurePosixPath(".pre-commit-config.yaml")
AGGREGATE_PATH = PurePosixPath("scripts/validate-repo-quality-gates.sh")
PROVIDER_EVIDENCE_AGGREGATE_PATH = PurePosixPath(
    "scripts/validate-agent-provider-evidence.py"
)
RUNNER_PATH = PurePosixPath("scripts/run-validation-lane.py")
QUALITY_POLICY_PATH = PurePosixPath("docs/00.agent-governance/policies/quality.md")
WORK_LIFECYCLE_PATH = PurePosixPath("docs/00.agent-governance/skills/work-lifecycle.md")
PULL_REQUEST_TEMPLATE_PATH = PurePosixPath(".github/PULL_REQUEST_TEMPLATE.md")
GITHUB_README_PATH = PurePosixPath(".github/README.md")
SCRIPTS_README_PATH = PurePosixPath("scripts/README.md")

SCHEMA_VERSION = 1
CONTRACT_VERSION = "1.4.0"
RESULT_VOCABULARY = ("PASS", "FAIL", "SKIP", "DEFER")
EVIDENCE_VOCABULARY = (
    "repo-static",
    "provider-runtime",
    "ci",
    "remote-live",
)
SELECTOR = {
    "jobId": "changes",
    "stepId": "filter",
    "output": "agent_governance",
    "expression": "${{ steps.filter.outputs.agent_governance }}",
    "selectedValue": "true",
    "unselectedValue": "false",
}
JOB = {
    "id": "agent-governance-static",
    "needs": ["changes"],
    "if": "needs.changes.outputs.agent_governance == 'true'",
    "evidence": "repo-static",
    "allowedResults": ["PASS", "FAIL"],
}
SUMMARY_NEEDS = (
    "branch-policy",
    "changes",
    "pre-commit",
    "repo-quality-static",
    "agent-governance-static",
    "manifest-static",
)
SUMMARY_ENV = {
    "EVENT_NAME": "${{ github.event_name }}",
    "BRANCH_POLICY_RESULT": "${{ needs['branch-policy'].result }}",
    "CHANGES_RESULT": "${{ needs.changes.result }}",
    "PRE_COMMIT_SELECTED": "${{ needs.changes.outputs.precommit }}",
    "PRE_COMMIT_RESULT": "${{ needs['pre-commit'].result }}",
    "REPO_QUALITY_STATIC_SELECTED": "${{ needs.changes.outputs.repo_quality }}",
    "REPO_QUALITY_STATIC_RESULT": ("${{ needs['repo-quality-static'].result }}"),
    "AGENT_GOVERNANCE_STATIC_SELECTED": (
        "${{ needs.changes.outputs.agent_governance }}"
    ),
    "AGENT_GOVERNANCE_STATIC_RESULT": (
        "${{ needs['agent-governance-static'].result }}"
    ),
    "MANIFEST_STATIC_SELECTED": "${{ needs.changes.outputs.manifests }}",
    "MANIFEST_STATIC_RESULT": "${{ needs['manifest-static'].result }}",
}
TRUTH_TABLE = (
    (True, "success", "PASS"),
    (False, "skipped", "SKIP"),
    (True, "skipped", "FAIL"),
    (True, "cancelled", "FAIL"),
    (True, "missing", "FAIL"),
    (True, "failure", "FAIL"),
)
ROUTE_CLASSES = (
    "root-config",
    "provider-gateways",
    "agent-shared",
    "agent-claude",
    "agent-codex",
    "github-automation",
    "governance-documents",
    "template-documents",
    "authored-documents",
    "scripts",
    "tests",
)
DELEGATED_COMMANDS = (
    (
        "agent-focused-tests",
        "python3 -m unittest discover --start-directory tests "
        "--top-level-directory tests --pattern 'test_validate_agent_*.py'",
    ),
    (
        "validation-tooling-tests",
        "python3 -m unittest tests.test_validation_tooling_ownership "
        "tests.test_affected_surface_migration "
        "tests.test_current_executable_references",
    ),
    (
        "agent-harness-contract",
        "python3 scripts/validate-agent-harness-contract.py --root .",
    ),
    (
        "agent-harness-semantics",
        "python3 scripts/validate-agent-harness-semantics.py --root .",
    ),
    (
        "agent-legacy-cutover",
        "python3 scripts/validate-agent-legacy-cutover.py --root .",
    ),
    (
        "agent-provider-evidence",
        "python3 scripts/validate-agent-provider-evidence.py --root .",
    ),
    (
        "agent-loop-lifecycle",
        "python3 scripts/validate-agent-loop-lifecycle.py --root .",
    ),
    (
        "affected-surfaces",
        "python3 scripts/validate-affected-surfaces.py --root .",
    ),
    (
        "ci-python",
        "python3 scripts/validate-ci-python-contract.py --root .",
    ),
    (
        "github-actions-security",
        "python3 scripts/validate-github-actions-security.py --root .",
    ),
)
DEPENDENCY_INSTALL_COMMAND = (
    "python -m pip install --disable-pip-version-check "
    "--only-binary :all: --require-hashes "
    "--requirement .github/requirements/ci-validation.txt"
)
LEGACY_DEPENDENCY_INSTALL_COMMAND = (
    "python -m pip install --disable-pip-version-check "
    "--requirement .github/requirements/ci-validation.txt"
)
PRODUCTION_COMMAND = "python3 scripts/validate-agent-governance-ci.py --root ."
OWNERSHIP_TEST_COMMAND = (
    "python3 -m unittest tests.test_validation_tooling_ownership"
)
AGGREGATE_COMMAND = "bash scripts/validate-repo-quality-gates.sh ."
CHECKOUT_ACTION = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
PROVIDER_EVIDENCE_FOCUSED_VALIDATORS = (
    "validate-agent-provider-config.py",
    "validate-agent-provider-canaries.py",
)
PROVIDER_EVIDENCE_FORBIDDEN_FRAGMENTS = (
    "secrets.",
    "${{ secrets",
    "provider_token",
    "provider-token",
    "provider token",
    "api_key",
    "api-key",
    "api key",
    "credential",
    "provider login",
    "provider auth",
    "claude auth",
    "codex login",
    "gemini auth",
    '"claude"',
    "'claude'",
    '"codex"',
    "'codex'",
    '"gemini"',
    "'gemini'",
    "hosted",
    "runtime",
    "remote",
    "live",
    "hosted ci pass",
    "hosted-ci pass",
    "provider-runtime pass",
    "provider runtime pass",
    "remote-live pass",
    "remote/live pass",
    ".agent-work",
    "checkpoint.json",
    "private transcript",
    "actual checkpoint",
    "actual state",
)
REMOTE_ACTION = re.compile(r"^[^./\s@][^\s@]*@[0-9a-f]{40}$")
EXPECTED_DEFERRED = (
    (
        "Spec046",
        (
            "hosted-ci-observation",
            "branch-protection",
            "provider-runtime-auth-model-discovery",
            "actual-evaluation-admission-promotion",
            "provider-resume-handoff-canary",
            "remote-live",
        ),
    ),
)
LOCAL_QA_SEQUENCE = (
    "targeted",
    "affected",
    "staged",
    "tests",
    "all-files",
    "formatter-review",
    "rerun",
    "diff-checks",
)
LOCAL_QA_OWNER = QUALITY_POLICY_PATH.as_posix()
LOCAL_QA_COMMANDS = {
    "affectedRunner": (
        "python3 scripts/run-validation-lane.py --root . --lane affected "
        "--paths-file <paths.nul> --delimiter nul"
    ),
    "stagedRunner": (
        "python3 scripts/run-validation-lane.py --root . --lane staged "
        "--paths-file <paths.nul> --delimiter nul"
    ),
    "stagedHooks": "pre-commit run",
    "allFiles": "pre-commit run --all-files",
    "diffCheck": "git diff --check",
    "cachedDiffCheck": "git diff --cached --check",
}
LOCAL_QA_CONSUMERS = (
    RUNNER_PATH,
    PRE_COMMIT_PATH,
    AGGREGATE_PATH,
    WORK_LIFECYCLE_PATH,
    PULL_REQUEST_TEMPLATE_PATH,
    GITHUB_README_PATH,
    SCRIPTS_README_PATH,
)


class ContractError(ValueError):
    """A stable agent-governance CI contract finding."""

    def __init__(self, rule_id: str, detail: str):
        self.rule_id = rule_id
        self.detail = detail
        super().__init__(f"{rule_id}: {detail}")


def fail(rule_id: str, detail: str) -> NoReturn:
    raise ContractError(rule_id, detail)


class DuplicateKeyError(ValueError):
    """Raised when JSON or YAML repeats a mapping key."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise DuplicateKeyError(f"duplicate YAML key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _absolute_root(root: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(root)))
    try:
        mode = absolute.lstat().st_mode
    except OSError as exc:
        fail("AGQC-CI-INPUT", f"repository root is unavailable: {exc.strerror}")
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        fail(
            "AGQC-CI-INPUT",
            "repository root must be a regular non-symlink directory",
        )
    return absolute


def _read_regular_bytes(root: Path, relative: PurePosixPath) -> bytes:
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        fail("AGQC-CI-INPUT", "repository input path is unsafe")
    try:
        root_metadata = os.lstat(root)
    except OSError as exc:
        fail(
            "AGQC-CI-INPUT",
            f"repository root is unavailable: {exc.strerror}",
        )
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
        fail(
            "AGQC-CI-INPUT",
            "repository root must be a regular non-symlink directory",
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
                "AGQC-CI-INPUT",
                "repository root identity changed during read",
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
                    "AGQC-CI-INPUT",
                    f"{relative.as_posix()} has a non-directory parent",
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
        if not stat.S_ISREG(os.fstat(file_descriptor).st_mode):
            fail(
                "AGQC-CI-INPUT",
                f"{relative.as_posix()} must be a regular non-symlink file",
            )

        chunks: list[bytes] = []
        while True:
            chunk = os.read(file_descriptor, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except ContractError:
        raise
    except OSError as exc:
        fail(
            "AGQC-CI-INPUT",
            f"{relative.as_posix()} cannot be read: {exc}",
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
    except UnicodeError as exc:
        fail(
            "AGQC-CI-INPUT",
            f"{relative.as_posix()} cannot be read as UTF-8: {exc}",
        )


def _read_path_regular_text(path: Path) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    relative = PurePosixPath(*absolute.parts[1:])
    return _read_regular_text(Path(absolute.anchor), relative)


def _parse_json(text: str, rule_id: str, source: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except (json.JSONDecodeError, DuplicateKeyError) as exc:
        fail(rule_id, f"{source}: {exc}")


def load_json_document(path: Path, rule_id: str) -> Any:
    """Load one regular JSON file while rejecting duplicate keys."""

    return _parse_json(_read_path_regular_text(path), rule_id, path.name)


def _parse_yaml(text: str, source: str) -> dict[str, Any]:
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, DuplicateKeyError) as exc:
        fail("AGQC-CI-YAML", f"{source}: {exc}")
    if not isinstance(value, dict):
        fail("AGQC-CI-YAML", f"{source}: YAML root must be a mapping")
    return value


def classify_conditional(selected: bool, conclusion: str) -> str:
    """Apply the fail-closed conditional-job result contract."""

    if selected is True and conclusion == "success":
        return "PASS"
    if selected is False and conclusion == "skipped":
        return "SKIP"
    return "FAIL"


def _schema_error_detail(error: Any) -> str:
    location = "/".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{location}: {error.message}"


def _validate_provider_evidence_aggregate(
    root: Path,
    manifest: dict[str, Any],
) -> None:
    expected_manifest = {
        "path": PROVIDER_EVIDENCE_AGGREGATE_PATH.as_posix(),
        "focusedValidators": list(PROVIDER_EVIDENCE_FOCUSED_VALIDATORS),
    }
    if manifest != expected_manifest:
        fail(
            "AGQC-CI-PROVIDER-AGGREGATE",
            "provider-evidence aggregate manifest differs",
        )

    source_bytes = _read_regular_bytes(
        root,
        PROVIDER_EVIDENCE_AGGREGATE_PATH,
    )
    try:
        source = source_bytes.decode("utf-8")
    except UnicodeError:
        fail(
            "AGQC-CI-PROVIDER-AGGREGATE",
            "provider-evidence aggregate source is not UTF-8",
        )

    lowered = source.casefold()
    present = [
        fragment
        for fragment in PROVIDER_EVIDENCE_FORBIDDEN_FRAGMENTS
        if fragment in lowered
    ]
    if present:
        fail(
            "AGQC-CI-PROVIDER-AGGREGATE",
            "provider-evidence aggregate crosses the repository-static boundary",
        )

    try:
        tree = ast.parse(
            source,
            filename=PROVIDER_EVIDENCE_AGGREGATE_PATH.as_posix(),
        )
    except SyntaxError:
        fail(
            "AGQC-CI-PROVIDER-AGGREGATE",
            "provider-evidence aggregate source is not valid Python",
        )
    assignments: list[ast.AST] = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "FOCUSED_VALIDATORS"
            for target in node.targets
        ):
            assignments.append(node.value)
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == "FOCUSED_VALIDATORS"
            and node.value is not None
        ):
            assignments.append(node.value)
    if len(assignments) != 1:
        fail(
            "AGQC-CI-PROVIDER-AGGREGATE",
            "provider-evidence focused-validator assignment differs",
        )
    try:
        observed_focused = ast.literal_eval(assignments[0])
    except (ValueError, TypeError, SyntaxError):
        fail(
            "AGQC-CI-PROVIDER-AGGREGATE",
            "provider-evidence focused-validator list is not literal",
        )
    if (
        not isinstance(observed_focused, (tuple, list))
        or any(not isinstance(item, str) for item in observed_focused)
        or tuple(observed_focused) != PROVIDER_EVIDENCE_FOCUSED_VALIDATORS
    ):
        fail(
            "AGQC-CI-PROVIDER-AGGREGATE",
            "provider-evidence focused-validator list differs",
        )


def validate_contract_data(
    root: Path,
    contract: dict[str, Any],
    *,
    schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate parsed contract data against schema and exact semantics."""

    absolute = _absolute_root(root)
    if schema is None:
        schema = _parse_json(
            _read_regular_text(absolute, SCHEMA_PATH),
            "AGQC-CI-JSON",
            SCHEMA_PATH.as_posix(),
        )
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes multiple schema exceptions
        fail("AGQC-CI-SCHEMA", f"schema definition is invalid: {exc}")
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        fail("AGQC-CI-SCHEMA", _schema_error_detail(errors[0]))

    if (
        contract["schemaVersion"] != SCHEMA_VERSION
        or contract["contractVersion"] != CONTRACT_VERSION
    ):
        fail("AGQC-CI-VERSION", "schemaVersion or contractVersion differs")
    if tuple(contract["resultVocabulary"]) != RESULT_VOCABULARY:
        fail("AGQC-CI-VOCABULARY", "result vocabulary or order differs")
    if tuple(contract["evidenceVocabulary"]) != EVIDENCE_VOCABULARY:
        fail("AGQC-CI-VOCABULARY", "evidence vocabulary or order differs")
    if contract["selector"] != SELECTOR:
        fail("AGQC-CI-SELECTOR", "selector ownership or output differs")
    if contract["job"] != JOB:
        fail("AGQC-CI-WORKFLOW", "static job topology differs")

    summary = contract["summary"]
    expected_summary = {
        "jobId": "ci-summary",
        "needs": list(SUMMARY_NEEDS),
        "if": "always()",
        "selectedEnv": "AGENT_GOVERNANCE_STATIC_SELECTED",
        "resultEnv": "AGENT_GOVERNANCE_STATIC_RESULT",
        "truthTable": [
            {
                "selected": selected,
                "conclusion": conclusion,
                "result": result,
            }
            for selected, conclusion, result in TRUTH_TABLE
        ],
        "defaultResult": "FAIL",
    }
    if summary != expected_summary:
        observed_truth = tuple(
            (
                row.get("selected"),
                row.get("conclusion"),
                row.get("result"),
            )
            for row in summary.get("truthTable", [])
            if isinstance(row, dict)
        )
        if observed_truth != TRUTH_TABLE or summary.get("defaultResult") != "FAIL":
            fail("AGQC-CI-TRUTH", "conditional-job truth table differs")
        fail("AGQC-CI-SUMMARY", "summary topology differs")

    expected_routes = [
        {
            "surfaceId": surface_id,
            "jobId": JOB["id"],
            "validatorId": "agent-governance-ci",
        }
        for surface_id in ROUTE_CLASSES
    ]
    if contract["requiredRouteClasses"] != expected_routes:
        fail("AGQC-CI-ROUTE", "required route classes differ")

    expected_checks = [
        {
            "id": identifier,
            "command": command,
            "evidence": "repo-static",
            "allowedResults": ["PASS", "FAIL"],
        }
        for identifier, command in DELEGATED_COMMANDS
    ]
    if contract["delegatedChecks"] != expected_checks:
        fail(
            "AGQC-CI-DELEGATION",
            "delegated check IDs, commands, evidence, or results differ",
        )
    if contract["gateCommands"] != {"production": PRODUCTION_COMMAND}:
        fail("AGQC-CI-DELEGATION", "gate command ownership differs")

    expected_security = {
        "workflowPermissions": {"contents": "read"},
        "checkoutAction": CHECKOUT_ACTION,
        "checkout": {"persistCredentials": False, "fetchDepth": 0},
        "remoteUsesPin": "full-commit-sha",
        "providerEvidenceAggregate": {
            "path": PROVIDER_EVIDENCE_AGGREGATE_PATH.as_posix(),
            "focusedValidators": list(PROVIDER_EVIDENCE_FOCUSED_VALIDATORS),
        },
        "forbiddenCommandClasses": [
            "provider-auth",
            "provider-canary",
            "provider-secret",
            "private-transcript-read",
            "actual-checkpoint-read",
            "hosted-ci-pass-claim",
            "validation-step-skip",
            "custom-or-default-shell",
            "extra-run-command",
            "continue-on-error",
            "summary-job-overrides",
            "summary-verdict-step-drift",
            "summary-script-drift",
            "write-or-oidc",
        ],
    }
    if contract["securityBoundary"] != expected_security:
        fail("AGQC-CI-SECURITY", "security boundary differs")
    _validate_provider_evidence_aggregate(
        absolute,
        contract["securityBoundary"]["providerEvidenceAggregate"],
    )

    observed_deferred = tuple(
        (
            row.get("owner"),
            row.get("result"),
            tuple(row.get("scope", [])),
        )
        for row in contract["deferredEvidence"]
    )
    expected_deferred = tuple(
        (owner, "DEFER", scope) for owner, scope in EXPECTED_DEFERRED
    )
    if observed_deferred != expected_deferred:
        fail(
            "AGQC-CI-EVIDENCE",
            "Spec046 DEFER ownership differs",
        )
    expected_local_qa = {
        "owner": LOCAL_QA_OWNER,
        "sequence": list(LOCAL_QA_SEQUENCE),
        "commands": LOCAL_QA_COMMANDS,
        "consumerSurfaces": [path.as_posix() for path in LOCAL_QA_CONSUMERS],
        "formatterCompletion": {
            "mutationResult": "not-completion-evidence",
            "requiredFinalResult": "PASS",
            "rerun": ["affected", "staged", "all-files"],
        },
    }
    if contract["localQa"] != expected_local_qa:
        if contract["localQa"].get("sequence") != list(LOCAL_QA_SEQUENCE):
            fail("AGQC-QA-ORDER", "local QA sequence or order differs")
        fail("AGQC-QA-CONTRACT", "local QA owner, command, or consumer differs")
    return contract


def _normalize_needs(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    return []


def _job_steps(job: dict[str, Any], rule_id: str) -> list[dict[str, Any]]:
    steps = job.get("steps")
    if not isinstance(steps, list) or any(not isinstance(step, dict) for step in steps):
        fail(rule_id, "job steps must be a mapping list")
    return steps


def _run_lines(steps: list[dict[str, Any]]) -> list[str]:
    return [
        line.strip()
        for step in steps
        for line in str(step.get("run") or "").splitlines()
        if line.strip()
    ]


def _summary_truth_block(selected: str, result: str, label: str) -> str:
    return "\n".join(
        (
            f'case "${selected}:${result}" in',
            "true:success)",
            'verdict="PASS"',
            ";;",
            "false:skipped)",
            'verdict="SKIP"',
            ";;",
            "*)",
            'verdict="FAIL"',
            "failed=1",
            ";;",
            "esac",
            (
                f"printf '{label} selected=%s result=%s verdict=%s\\n' "
                f'"${selected}" "${result}" "$verdict"'
            ),
        )
    )


def _expected_summary_run() -> str:
    blocks = [
        "\n".join(
            (
                "set -euo pipefail",
                "failed=0",
                'case "$EVENT_NAME" in',
                "pull_request)",
                'branch_policy_selected="true"',
                ";;",
                "push|workflow_dispatch)",
                'branch_policy_selected="false"',
                ";;",
                "*)",
                'branch_policy_selected="invalid"',
                ";;",
                "esac",
            )
        ),
        _summary_truth_block(
            "branch_policy_selected",
            "BRANCH_POLICY_RESULT",
            "branch-policy",
        ),
        "\n".join(
            (
                'if [ "$CHANGES_RESULT" = "success" ]; then',
                'verdict="PASS"',
                "else",
                'verdict="FAIL"',
                "failed=1",
                "fi",
                (
                    "printf 'changes selected=true result=%s verdict=%s\\n' "
                    '"$CHANGES_RESULT" "$verdict"'
                ),
            )
        ),
        _summary_truth_block(
            "PRE_COMMIT_SELECTED",
            "PRE_COMMIT_RESULT",
            "pre-commit",
        ),
        _summary_truth_block(
            "REPO_QUALITY_STATIC_SELECTED",
            "REPO_QUALITY_STATIC_RESULT",
            "repo-quality-static",
        ),
        _summary_truth_block(
            "AGENT_GOVERNANCE_STATIC_SELECTED",
            "AGENT_GOVERNANCE_STATIC_RESULT",
            "agent-governance-static",
        ),
        _summary_truth_block(
            "MANIFEST_STATIC_SELECTED",
            "MANIFEST_STATIC_RESULT",
            "manifest-static",
        ),
        "\n".join(
            (
                'if [ "$failed" -ne 0 ]; then',
                'echo "one or more required CI gates failed closed"',
                "exit 1",
                "fi",
            )
        ),
    ]
    return "\n".join(blocks)


def _all_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            strings.append(str(key))
            strings.extend(_all_strings(child))
    elif isinstance(value, list):
        for child in value:
            strings.extend(_all_strings(child))
    elif isinstance(value, str):
        strings.append(value)
    return strings


def _validate_security(
    workflow: dict[str, Any],
    agent_job: dict[str, Any],
    steps: list[dict[str, Any]],
    contract: dict[str, Any],
) -> None:
    if workflow.get("permissions") != {"contents": "read"}:
        fail("AGQC-CI-SECURITY", "workflow permissions must be contents: read")
    if "defaults" in workflow:
        fail(
            "AGQC-CI-SECURITY",
            "workflow defaults must not alter static-job execution",
        )
    workflow_env = workflow.get("env")
    if workflow_env is not None:
        if not isinstance(workflow_env, dict):
            fail("AGQC-CI-SECURITY", "workflow env must be a mapping")
        inherited_env = "\n".join(_all_strings(workflow_env)).casefold()
        if any(
            fragment in inherited_env
            for fragment in (
                "secrets.",
                "${{ secrets",
                "provider_token",
                "provider-token",
                "provider token",
            )
        ):
            fail(
                "AGQC-CI-SECURITY",
                "workflow-level provider or secret env must not reach the static job",
            )
    if "permissions" in agent_job and agent_job["permissions"] != {"contents": "read"}:
        fail(
            "AGQC-CI-SECURITY",
            "agent-governance-static must not add write or OIDC permissions",
        )
    if "continue-on-error" in agent_job or any(
        "continue-on-error" in step for step in steps
    ):
        fail(
            "AGQC-CI-SECURITY",
            "agent-governance-static and every validation step must fail closed",
        )
    if "defaults" in agent_job or "shell" in agent_job:
        fail(
            "AGQC-CI-SECURITY",
            "agent-governance-static must not override run defaults or shell",
        )
    if any(("if" in step or "shell" in step) for step in steps if "run" in step):
        fail(
            "AGQC-CI-SECURITY",
            "agent-governance static run steps must not be skipped or override shell",
        )

    uses = [step.get("uses") for step in steps if "uses" in step]
    if not uses or any(
        not isinstance(value, str) or REMOTE_ACTION.fullmatch(value) is None
        for value in uses
    ):
        fail(
            "AGQC-CI-SECURITY",
            "every remote Action must use a full forty-character commit SHA",
        )
    checkout_steps = [
        step
        for step in steps
        if step.get("uses") == contract["securityBoundary"]["checkoutAction"]
    ]
    if len(checkout_steps) != 1 or checkout_steps[0].get("with") != {
        "persist-credentials": False,
        "fetch-depth": 0,
    }:
        fail(
            "AGQC-CI-SECURITY",
            "checkout must disable persisted credentials and fetch full history",
        )

    flattened = "\n".join(_all_strings(agent_job)).casefold()
    forbidden_fragments = (
        "secrets.",
        "${{ secrets",
        "provider_token",
        "provider-token",
        "provider token",
        "validate-agent-provider-canaries.py",
        "provider login",
        "provider auth",
        "claude auth",
        "codex login",
        "gemini auth",
        ".agent-work",
        "checkpoint.json",
        "private transcript",
        "hosted ci pass",
        "hosted-ci pass",
        LEGACY_DEPENDENCY_INSTALL_COMMAND,
    )
    present = [item for item in forbidden_fragments if item in flattened]
    if present:
        fail(
            "AGQC-CI-SECURITY",
            f"forbidden provider, secret, transcript, checkpoint, or hosted claim: {present[0]}",
        )


def validate_workflow_data(
    workflow: dict[str, Any],
    contract: dict[str, Any],
) -> None:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("AGQC-CI-WORKFLOW", "workflow jobs must be a mapping")

    selector = contract["selector"]
    changes = jobs.get(selector["jobId"])
    if not isinstance(changes, dict):
        fail("AGQC-CI-SELECTOR", "changes job is missing")
    outputs = changes.get("outputs")
    if (
        not isinstance(outputs, dict)
        or outputs.get(selector["output"]) != selector["expression"]
    ):
        fail("AGQC-CI-SELECTOR", "agent_governance selector output is missing")
    output_owners = [
        job_id
        for job_id, job in jobs.items()
        if isinstance(job, dict)
        and isinstance(job.get("outputs"), dict)
        and selector["output"] in job["outputs"]
    ]
    if output_owners != [selector["jobId"]]:
        fail("AGQC-CI-SELECTOR", "agent_governance selector output owner differs")
    selector_steps = [
        step
        for step in _job_steps(changes, "AGQC-CI-SELECTOR")
        if step.get("id") == selector["stepId"]
    ]
    if len(selector_steps) != 1:
        fail("AGQC-CI-SELECTOR", "selector step cardinality differs")
    selector_run = str(selector_steps[0].get("run") or "")
    if (
        "python3 scripts/select-affected-surfaces.py" not in selector_run
        or "--format github-output" not in selector_run
    ):
        fail("AGQC-CI-SELECTOR", "selector implementation differs")

    job = jobs.get(contract["job"]["id"])
    if not isinstance(job, dict):
        fail("AGQC-CI-WORKFLOW", "agent-governance-static job is missing")
    if _normalize_needs(job.get("needs")) != contract["job"]["needs"]:
        fail("AGQC-CI-WORKFLOW", "agent-governance-static needs differs")
    if str(job.get("if") or "") != contract["job"]["if"]:
        fail("AGQC-CI-WORKFLOW", "agent-governance-static if differs")
    steps = _job_steps(job, "AGQC-CI-WORKFLOW")
    _validate_security(workflow, job, steps, contract)

    run_lines = _run_lines(steps)
    production = contract["gateCommands"]["production"]
    expected_run_lines = [
        DEPENDENCY_INSTALL_COMMAND,
        production,
        *(check["command"] for check in contract["delegatedChecks"]),
    ]
    if run_lines != expected_run_lines:
        fail(
            "AGQC-CI-DELEGATION",
            "agent-governance static run-line sequence differs",
        )

    summary = jobs.get(contract["summary"]["jobId"])
    if not isinstance(summary, dict):
        fail("AGQC-CI-SUMMARY", "ci-summary job is missing")
    if "permissions" in summary or "env" in summary:
        fail(
            "AGQC-CI-SECURITY",
            "ci-summary must inherit read-only permissions and no job env",
        )
    if set(summary) != {
        "needs",
        "if",
        "runs-on",
        "timeout-minutes",
        "steps",
    }:
        fail("AGQC-CI-TRUTH", "ci-summary execution-control shape differs")
    if _normalize_needs(summary.get("needs")) != contract["summary"]["needs"]:
        fail("AGQC-CI-SUMMARY", "ci-summary needs differs")
    if str(summary.get("if") or "") != contract["summary"]["if"]:
        fail("AGQC-CI-SUMMARY", "ci-summary if differs")
    if summary.get("runs-on") != "ubuntu-latest" or summary.get("timeout-minutes") != 5:
        fail("AGQC-CI-TRUTH", "ci-summary runner or timeout differs")
    summary_steps = _job_steps(summary, "AGQC-CI-SUMMARY")
    if len(summary_steps) != 1:
        fail("AGQC-CI-TRUTH", "ci-summary must have exactly one verdict step")
    summary_step = summary_steps[0]
    env = summary_step.get("env")
    if isinstance(env, dict):
        flattened_env = "\n".join(_all_strings(env)).casefold()
        if any(
            fragment in flattened_env
            for fragment in (
                "secrets.",
                "${{ secrets",
                "provider_token",
                "provider-token",
                "provider token",
            )
        ):
            fail(
                "AGQC-CI-SECURITY",
                "ci-summary verdict env must not contain provider or secret input",
            )
    if set(summary_step) != {"name", "env", "run"}:
        fail("AGQC-CI-TRUTH", "ci-summary verdict step shape differs")
    if summary_step.get("name") != "Summarize CI result" or env != SUMMARY_ENV:
        fail("AGQC-CI-TRUTH", "ci-summary verdict step or env differs")
    summary_run = str(summary_step.get("run") or "")
    normalized_run = "\n".join(
        line.strip() for line in summary_run.splitlines() if line.strip()
    )
    if normalized_run != _expected_summary_run():
        fail("AGQC-CI-TRUTH", "ci-summary fail-closed verdict script differs")


def validate_affected_data(
    affected: dict[str, Any],
    contract: dict[str, Any],
) -> None:
    jobs = affected.get("ciJobs")
    if not isinstance(jobs, list) or any(not isinstance(row, dict) for row in jobs):
        fail("AGQC-CI-SELECTOR", "affected ciJobs must be a mapping list")
    matching_jobs = [
        row
        for row in jobs
        if row.get("id") == contract["job"]["id"]
        or row.get("output") == contract["selector"]["output"]
    ]
    expected_job = {
        "id": contract["job"]["id"],
        "output": contract["selector"]["output"],
        "evidenceLane": "ci",
    }
    if matching_jobs != [expected_job]:
        fail(
            "AGQC-CI-SELECTOR",
            "affected selector job/output is missing, duplicated, or drifted",
        )

    validators = affected.get("validators")
    if not isinstance(validators, list) or any(
        not isinstance(row, dict) for row in validators
    ):
        fail("AGQC-CI-ROUTE", "affected validators must be a mapping list")
    expected_registrations = (
        {
            "id": "agent-governance-ci",
            "argv": [
                "python3",
                "scripts/validate-agent-governance-ci.py",
                "--root",
                ".",
            ],
            "lanes": ["affected", "staged", "all-files", "ci"],
            "optional": False,
            "fallback": {
                "status": "FAIL",
                "reason": "Agent-governance CI topology validation is required.",
            },
            "evidenceLane": "repo-static",
        },
    )
    for expected_registration in expected_registrations:
        registrations = [
            row for row in validators if row.get("id") == expected_registration["id"]
        ]
        if registrations != [expected_registration]:
            fail("AGQC-CI-ROUTE", "affected validator registration differs")

    surfaces = affected.get("surfaces")
    if not isinstance(surfaces, list) or any(
        not isinstance(row, dict) for row in surfaces
    ):
        fail("AGQC-CI-ROUTE", "affected surfaces must be a mapping list")
    by_id = {row.get("id"): row for row in surfaces}
    if len(by_id) != len(surfaces):
        fail("AGQC-CI-ROUTE", "affected surface IDs must be unique")
    selected_job = {
        surface_id
        for surface_id, surface in by_id.items()
        if contract["job"]["id"] in surface.get("ciJobs", [])
    }
    selected_validator = {
        surface_id
        for surface_id, surface in by_id.items()
        if "agent-governance-ci" in surface.get("validators", [])
    }
    expected = set(ROUTE_CLASSES)
    if selected_job != expected or selected_validator != expected:
        fail(
            "AGQC-CI-ROUTE",
            "required route classes must select one static job and its gate",
        )


def _validate_integrations(
    aggregate_text: str,
    pre_commit: dict[str, Any],
) -> None:
    required_fragments = (
        'python3 "$ROOT_DIR/scripts/run-validation-lane.py"',
        '--root "$ROOT_DIR"',
        "--lane all-files",
    )
    if any(aggregate_text.count(fragment) != 1 for fragment in required_fragments):
        fail(
            "AGQC-CI-DELEGATION",
            "aggregate must invoke the registry all-files runner exactly once",
        )
    forbidden_direct_commands = (
        "scripts/validate-agent-governance-ci.py",
        "scripts/validate-agent-legacy-cutover.py",
        "scripts/validate-affected-surfaces.py",
        "scripts/validate-agent-provider-evidence.py",
    )
    if any(command in aggregate_text for command in forbidden_direct_commands):
        fail(
            "AGQC-CI-DELEGATION",
            "aggregate must not embed validator command ownership",
        )

    repos = pre_commit.get("repos")
    if not isinstance(repos, list):
        fail("AGQC-CI-DELEGATION", "pre-commit repos must be a list")
    local = [
        row for row in repos if isinstance(row, dict) and row.get("repo") == "local"
    ]
    if len(local) != 1 or not isinstance(local[0].get("hooks"), list):
        fail("AGQC-CI-DELEGATION", "pre-commit local hook owner differs")
    hooks = local[0]["hooks"]
    expected_hooks = (
        (
            "validate-validation-tooling-ownership",
            "validate validation-tooling ownership",
            OWNERSHIP_TEST_COMMAND,
        ),
        (
            "strict-repository-quality",
            "validate strict repository quality",
            AGGREGATE_COMMAND,
        ),
    )
    for hook_id, hook_name, entry in expected_hooks:
        matches = [
            hook
            for hook in hooks
            if isinstance(hook, dict) and hook.get("id") == hook_id
        ]
        if len(matches) != 1 or matches[0] != {
            "id": hook_id,
            "name": hook_name,
            "entry": entry,
            "language": "system",
            "pass_filenames": False,
            "always_run": True,
            "stages": ["pre-commit", "manual"],
        }:
            fail(
                "AGQC-CI-DELEGATION",
                f"pre-commit hook differs: {hook_id}",
            )
    hook_ids = [hook.get("id") for hook in hooks if isinstance(hook, dict)]
    required_hook_order = (
        "validate-validation-tooling-ownership",
        "strict-repository-quality",
    )
    forbidden_duplicate_hooks = (
        "validate-agent-governance-ci",
        "validate-agent-legacy-cutover",
        "validate-affected-surfaces",
    )
    if any(identifier not in hook_ids for identifier in required_hook_order):
        fail("AGQC-CI-DELEGATION", "pre-commit gate ordering owner is missing")
    if any(identifier in hook_ids for identifier in forbidden_duplicate_hooks):
        fail("AGQC-CI-DELEGATION", "pre-commit duplicates registry-owned validators")
    observed_positions = [
        hook_ids.index(identifier) for identifier in required_hook_order
    ]
    if observed_positions != sorted(observed_positions):
        fail(
            "AGQC-CI-DELEGATION",
            "pre-commit gate order must avoid aggregate recursion",
        )


@lru_cache(maxsize=1)
def _load_link_validator() -> ModuleType:
    """Load the existing parser beside this validator, not from the input root."""
    script_path = Path(__file__).with_name("validate-links-and-owners.py")
    module_name = f"_ci_canonical_links_{id(_load_link_validator):x}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical rendered-link adapter is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    scripts_path = str(script_path.parent)
    inserted = scripts_path not in sys.path
    if inserted:
        sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
        if inserted:
            sys.path.remove(scripts_path)
    return module


def _routes_to_quality_owner(path: PurePosixPath, text: str) -> bool:
    return any(
        link.kind == "local" and link.target == QUALITY_POLICY_PATH
        for link in _load_link_validator().rendered_local_links(text, path)
    )


def _validate_local_qa_surfaces(
    root: Path,
    contract: dict[str, Any],
    texts: dict[PurePosixPath, str],
) -> None:
    local_qa = contract["localQa"]
    expected_consumers = [path.as_posix() for path in LOCAL_QA_CONSUMERS]
    if local_qa["owner"] != LOCAL_QA_OWNER:
        fail("AGQC-QA-OWNER", "canonical local QA owner differs")
    if local_qa["consumerSurfaces"] != expected_consumers:
        fail("AGQC-QA-OWNER", "local QA consumer surface inventory differs")

    quality_text = texts[QUALITY_POLICY_PATH]
    markers = [
        f"{index}. **{identifier}**:"
        for index, identifier in enumerate(LOCAL_QA_SEQUENCE, start=1)
    ]
    if any(quality_text.count(marker) != 1 for marker in markers):
        fail("AGQC-QA-ORDER", "canonical local QA step markers differ")
    positions = [quality_text.index(marker) for marker in markers]
    if positions != sorted(positions):
        fail("AGQC-QA-ORDER", "canonical local QA step order differs")
    for marker in (
        "`git diff --check`",
        "`git diff --cached --check`",
    ):
        if marker not in quality_text:
            fail(
                "AGQC-QA-EVIDENCE",
                f"canonical local QA owner lacks {marker}",
            )

    rerun_text = " ".join(quality_text[positions[6] : positions[7]].split())
    if "not completion evidence" not in rerun_text or any(
        lane not in rerun_text for lane in ("affected", "staged", "all-files")
    ):
        fail("AGQC-QA-EVIDENCE", "canonical formatter rerun evidence differs")

    for path in LOCAL_QA_CONSUMERS:
        if path.suffix == ".md" and not _routes_to_quality_owner(path, texts[path]):
            fail(
                "AGQC-QA-OWNER",
                f"{path.as_posix()} lacks a link to the canonical local QA owner",
            )

    runner_text = texts[RUNNER_PATH]
    if 'LOCAL_LANES = ("affected", "staged", "all-files")' not in runner_text:
        fail("AGQC-QA-RUNNER", "local runner lane set differs")
    command_paths = {
        PurePosixPath(match)
        for command in local_qa["commands"].values()
        for match in re.findall(r"scripts/[A-Za-z0-9_.-]+\.(?:py|sh)", command)
    }
    for path in sorted(command_paths):
        _read_regular_text(root, path)


def _load_repository_inputs(
    root: Path,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    str,
    dict[str, Any],
    dict[PurePosixPath, str],
]:
    schema = _parse_json(
        _read_regular_text(root, SCHEMA_PATH),
        "AGQC-CI-JSON",
        SCHEMA_PATH.as_posix(),
    )
    contract = _parse_json(
        _read_regular_text(root, CONTRACT_PATH),
        "AGQC-CI-JSON",
        CONTRACT_PATH.as_posix(),
    )
    affected = _parse_json(
        _read_regular_text(root, AFFECTED_PATH),
        "AGQC-CI-JSON",
        AFFECTED_PATH.as_posix(),
    )
    workflow = _parse_yaml(
        _read_regular_text(root, WORKFLOW_PATH),
        WORKFLOW_PATH.as_posix(),
    )
    aggregate = _read_regular_text(root, AGGREGATE_PATH)
    pre_commit_text = _read_regular_text(root, PRE_COMMIT_PATH)
    pre_commit = _parse_yaml(
        pre_commit_text,
        PRE_COMMIT_PATH.as_posix(),
    )
    qa_texts = {
        path: _read_regular_text(root, path)
        for path in (
            QUALITY_POLICY_PATH,
            RUNNER_PATH,
            WORK_LIFECYCLE_PATH,
            PULL_REQUEST_TEMPLATE_PATH,
            GITHUB_README_PATH,
            SCRIPTS_README_PATH,
        )
    }
    qa_texts[PRE_COMMIT_PATH] = pre_commit_text
    qa_texts[AGGREGATE_PATH] = aggregate
    return (
        schema,
        contract,
        affected,
        workflow,
        aggregate,
        pre_commit,
        qa_texts,
    )


def validate_repository(root: Path) -> dict[str, int]:
    absolute = _absolute_root(root)
    (
        schema,
        contract,
        affected,
        workflow,
        aggregate,
        pre_commit,
        qa_texts,
    ) = _load_repository_inputs(absolute)
    validate_contract_data(absolute, contract, schema=schema)
    validate_affected_data(affected, contract)
    validate_workflow_data(workflow, contract)
    _validate_integrations(aggregate, pre_commit)
    _validate_local_qa_surfaces(absolute, contract, qa_texts)
    return {
        "routeClasses": len(contract["requiredRouteClasses"]),
        "delegatedChecks": len(contract["delegatedChecks"]),
        "truthRows": len(contract["summary"]["truthTable"]),
        "deferredOwners": len(contract["deferredEvidence"]),
        "qaSurfaces": 1 + len(contract["localQa"]["consumerSurfaces"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        counts = validate_repository(args.root)
        print(
            "[PASS] agent-governance CI validation passed: "
            f"route_classes={counts['routeClasses']} "
            f"delegated_checks={counts['delegatedChecks']} "
            f"truth_rows={counts['truthRows']} "
            f"deferred_owners={counts['deferredOwners']} "
            f"qa_surfaces={counts['qaSurfaces']}"
        )
        return 0
    except ContractError as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
