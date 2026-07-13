#!/usr/bin/env python3
"""Validate the affected-surface contract and its deterministic fixtures."""

from __future__ import annotations

import argparse
import copy
import json
import re
import stat
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/validation-surfaces.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/validation-surfaces.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/validation-surfaces.json")
CI_WORKFLOW_PATH = PurePosixPath(".github/workflows/ci.yml")
SELECTOR_LANES = ("affected", "staged", "all-files", "ci")
LANES = (
    "affected",
    "staged",
    "all-files",
    "message/manual",
    "ci",
    "remote/live",
    "inventory",
)
PROTECTED_LEVELS = ("none", "review", "protected")
EVIDENCE_LANES = ("repo-static", "ci", "remote/live")
SAFE_ARG = re.compile(r"^[A-Za-z0-9_./:@%+=,-]+$")
INTERPRETER_CONTRACTS = {
    "bash": {
        "evalShort": frozenset(("c",)),
        "evalLong": frozenset(("--command",)),
        "scriptSuffixes": (".sh",),
    },
    "python3": {
        "evalShort": frozenset(("c",)),
        "evalLong": frozenset(),
        "scriptSuffixes": (".py",),
    },
    "node": {
        "evalShort": frozenset(("e", "p")),
        "evalLong": frozenset(("--eval", "--print")),
        "scriptSuffixes": (".js", ".mjs", ".cjs"),
    },
}


class ContractError(ValueError):
    """A stable affected-surface contract or selection failure."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


def fail(code: str, detail: str) -> NoReturn:
    raise ContractError(code, detail)


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail("SURFACE-JSON", f"{path}: {exc}")


def normalize_path(raw: str) -> str:
    if not raw or raw == ".":
        fail("SURFACE-PATH-NORMALIZATION", "path must not be empty")
    if raw.startswith("./"):
        fail("SURFACE-PATH-NORMALIZATION", "path must not start with './'")
    if "\\" in raw:
        fail("SURFACE-PATH-NORMALIZATION", "path must use POSIX separators")
    path = PurePosixPath(raw)
    if path.is_absolute():
        fail("SURFACE-PATH-NORMALIZATION", "path must be repository-relative")
    if ".." in path.parts:
        fail("SURFACE-PATH-NORMALIZATION", "path must not contain '..'")
    normalized = path.as_posix()
    if normalized != raw or raw.endswith("/") or "//" in raw:
        fail("SURFACE-PATH-NORMALIZATION", "path must already be normalized")
    return normalized


def match_route(path: str, route: dict[str, str]) -> bool:
    if route["kind"] == "exact":
        return path == route["value"]
    if route["kind"] == "regex":
        pattern = route["value"]
        if not pattern.startswith("^") or not pattern.endswith("$"):
            fail("SURFACE-REGEX-ANCHOR", pattern)
        try:
            return re.fullmatch(pattern[1:-1], path) is not None
        except re.error as exc:
            fail("SURFACE-REGEX", f"{pattern}: {exc}")
    fail("SURFACE-ROUTE-KIND", route["kind"])


def _unique_ids(rows: Sequence[dict[str, Any]], kind: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        identifier = row["id"]
        if identifier in indexed:
            fail(f"SURFACE-{kind}-ID", f"duplicate id {identifier!r}")
        indexed[identifier] = row
    return indexed


def _validate_direct_script_argv(identifier: str, argv: Sequence[str]) -> None:
    if any(SAFE_ARG.fullmatch(argument) is None for argument in argv):
        fail(
            "SURFACE-VALIDATOR-ARGV",
            f"{identifier} argv must not require shell parsing or expansion",
        )

    executable = argv[0]
    interpreter = INTERPRETER_CONTRACTS.get(executable)
    if interpreter is None:
        fail(
            "SURFACE-VALIDATOR-EXECUTABLE",
            f"{identifier} executable token {executable!r} is not exactly one of "
            + ", ".join(sorted(INTERPRETER_CONTRACTS)),
        )

    arguments = list(argv[1:])
    if not arguments:
        fail("SURFACE-VALIDATOR-ARGV-SCRIPT", f"{identifier} has no script operand")

    options: list[str] = []
    script_operand: str | None = None
    after_option_boundary = False
    for argument in arguments:
        if script_operand is not None:
            break
        if not after_option_boundary and argument == "--":
            after_option_boundary = True
            continue
        if not after_option_boundary and argument.startswith("-"):
            options.append(argument)
            if argument.startswith("--"):
                if any(
                    argument == flag or argument.startswith(f"{flag}=")
                    for flag in interpreter["evalLong"]
                ):
                    fail(
                        "SURFACE-VALIDATOR-ARGV-EVAL",
                        f"{identifier} may not use {executable} evaluation option {argument!r}",
                    )
            elif set(argument[1:]).intersection(interpreter["evalShort"]):
                fail(
                    "SURFACE-VALIDATOR-ARGV-EVAL",
                    f"{identifier} may not use {executable} evaluation option {argument!r}",
                )
            continue
        script_operand = argument

    if script_operand is None:
        fail("SURFACE-VALIDATOR-ARGV-SCRIPT", f"{identifier} has no script operand")
    if options:
        fail(
            "SURFACE-VALIDATOR-ARGV-SCRIPT",
            f"{identifier} first post-executable operand must be the script path or '--'",
        )
    try:
        normalized_script = normalize_path(script_operand)
    except ContractError:
        fail(
            "SURFACE-VALIDATOR-ARGV-SCRIPT",
            f"{identifier} script operand must be a normalized repository path",
        )
    if not normalized_script.endswith(interpreter["scriptSuffixes"]):
        fail(
            "SURFACE-VALIDATOR-ARGV-SCRIPT",
            f"{identifier} script {normalized_script!r} does not match {executable}",
        )


def validate_contract(
    root: Path, raw_contract: dict[str, Any] | None = None
) -> dict[str, Any]:
    schema = load_json(root / SCHEMA_PATH)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema subclasses
        fail("SURFACE-SCHEMA-DEFINITION", str(exc))
    contract = (
        copy.deepcopy(raw_contract)
        if raw_contract is not None
        else load_json(root / CONTRACT_PATH)
    )
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        fail("SURFACE-SCHEMA", f"{location}: {error.message}")

    if tuple(contract["lanes"]) != LANES:
        fail("SURFACE-LANE", "lane order or membership differs from the contract")
    if tuple(contract["protectedLevels"]) != PROTECTED_LEVELS:
        fail("SURFACE-PROTECTED-LEVEL", "protected level order differs")
    if tuple(contract["evidenceLanes"]) != EVIDENCE_LANES:
        fail("SURFACE-EVIDENCE-LANE", "evidence lane order differs")

    validators = _unique_ids(contract["validators"], "VALIDATOR")
    ci_jobs = _unique_ids(contract["ciJobs"], "CI-JOB")
    surfaces = _unique_ids(contract["surfaces"], "SURFACE")
    outputs: set[str] = set()

    for validator in validators.values():
        if any(lane not in LANES for lane in validator["lanes"]):
            fail("SURFACE-VALIDATOR-LANE", validator["id"])
        _validate_direct_script_argv(validator["id"], validator["argv"])
        if validator["evidenceLane"] not in EVIDENCE_LANES:
            fail("SURFACE-EVIDENCE-LANE", validator["id"])
        status = validator["fallback"]["status"]
        if (not validator["optional"] and status != "FAIL") or (
            validator["optional"] and status not in {"DEFER", "SKIP"}
        ):
            fail("SURFACE-FALLBACK", validator["id"])

    for job in ci_jobs.values():
        if job["output"] in outputs:
            fail("SURFACE-CI-OUTPUT", f"duplicate output {job['output']!r}")
        outputs.add(job["output"])
        if job["evidenceLane"] != "ci":
            fail("SURFACE-EVIDENCE-LANE", job["id"])

    route_keys: set[tuple[str, str, str]] = set()
    for surface in surfaces.values():
        if any(item not in validators for item in surface["validators"]):
            fail("SURFACE-VALIDATOR-REFERENCE", surface["id"])
        if any(item not in ci_jobs for item in surface["ciJobs"]):
            fail("SURFACE-CI-JOB-REFERENCE", surface["id"])
        if surface["protectedLevel"] not in PROTECTED_LEVELS:
            fail("SURFACE-PROTECTED-LEVEL", surface["id"])
        if surface["evidenceLane"] not in EVIDENCE_LANES:
            fail("SURFACE-EVIDENCE-LANE", surface["id"])
        if surface["fallback"]["status"] != "FAIL":
            fail(
                "SURFACE-SURFACE-FALLBACK",
                f"{surface['id']} is non-optional and must fail closed",
            )
        for route in surface["routes"]:
            if route["kind"] == "exact":
                normalize_path(route["value"])
            else:
                pattern = route["value"]
                if not pattern.startswith("^") or not pattern.endswith("$"):
                    fail("SURFACE-REGEX-ANCHOR", pattern)
                try:
                    re.compile(pattern)
                except re.error as exc:
                    fail("SURFACE-REGEX", f"{pattern}: {exc}")
            key = (surface["id"], route["kind"], route["value"])
            if key in route_keys:
                fail("SURFACE-ROUTE-DUPLICATE", f"{surface['id']}: {route}")
            route_keys.add(key)
    return contract


def _case_alias(contract: dict[str, Any], path: str) -> bool:
    for surface in contract["surfaces"]:
        for route in surface["routes"]:
            if route["kind"] == "exact" and route["value"].casefold() == path.casefold():
                return route["value"] != path
            if route["kind"] == "regex":
                pattern = route["value"]
                try:
                    if re.fullmatch(pattern[1:-1], path, flags=re.IGNORECASE):
                        return not match_route(path, route)
                except re.error:
                    continue
    return False


def classify_path(contract: dict[str, Any], raw_path: str) -> dict[str, Any]:
    path = normalize_path(raw_path)
    matches = [
        surface
        for surface in contract["surfaces"]
        if any(match_route(path, route) for route in surface["routes"])
    ]
    if not matches:
        if _case_alias(contract, path):
            fail("SURFACE-PATH-CASE-ALIAS", path)
        fail("SURFACE-PATH-UNMATCHED", path)
    if len(matches) != 1:
        fail(
            "SURFACE-PATH-AMBIGUOUS",
            f"{path}: {sorted(surface['id'] for surface in matches)}",
        )
    return matches[0]


def reject_symlink_traversal(root: Path, raw_path: str) -> None:
    path = PurePosixPath(normalize_path(raw_path))
    current = root
    for part in path.parts[:-1]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            return
        except OSError as exc:
            fail("SURFACE-PATH-SYMLINK", f"{raw_path}: {exc}")
        if stat.S_ISLNK(mode):
            fail("SURFACE-PATH-SYMLINK", raw_path)


def select_paths(
    contract: dict[str, Any],
    paths: Sequence[str],
    lane: str,
    root: Path | None = None,
    *,
    collect_unmatched: bool = False,
) -> dict[str, Any]:
    if lane not in SELECTOR_LANES:
        fail("SURFACE-LANE", lane)
    validators_by_id = {row["id"]: row for row in contract["validators"]}
    validator_ids: set[str] = set()
    ci_job_ids: set[str] = set()
    unmatched_paths: set[str] = set()
    maximum = 0
    for raw_path in paths:
        if root is not None:
            reject_symlink_traversal(root, raw_path)
        try:
            surface = classify_path(contract, raw_path)
        except ContractError as exc:
            if collect_unmatched and exc.code == "SURFACE-PATH-UNMATCHED":
                unmatched_paths.add(normalize_path(raw_path))
                continue
            raise
        for identifier in surface["validators"]:
            if lane in validators_by_id[identifier]["lanes"]:
                validator_ids.add(identifier)
        ci_job_ids.update(surface["ciJobs"])
        maximum = max(maximum, PROTECTED_LEVELS.index(surface["protectedLevel"]))
    return {
        "validators": sorted(validator_ids),
        "ciJobs": sorted(ci_job_ids),
        "protectedLevel": PROTECTED_LEVELS[maximum],
        "unmatchedPaths": sorted(unmatched_paths),
    }


def json_output(result: dict[str, Any]) -> str:
    return json.dumps(
        result,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def github_output(contract: dict[str, Any], result: dict[str, Any]) -> str:
    selected = set(result["ciJobs"])
    return "\n".join(
        f"{job['output']}={'true' if job['id'] in selected else 'false'}"
        for job in sorted(contract["ciJobs"], key=lambda row: row["output"])
    )


def validate_ci_workflow_selector(root: Path) -> None:
    try:
        workflow = (root / CI_WORKFLOW_PATH).read_text(encoding="utf-8")
        changes = workflow.split("\n  changes:\n", 1)[1].split(
            "\n  pre-commit:\n", 1
        )[0]
    except (OSError, UnicodeError, IndexError) as exc:
        fail("SURFACE-LOCAL-CI-MISMATCH", f"cannot read changes job: {exc}")

    required_fragments = (
        "precommit: ${{ steps.filter.outputs.precommit }}",
        "repo_quality: ${{ steps.filter.outputs.repo_quality }}",
        "manifests: ${{ steps.filter.outputs.manifests }}",
        "fetch-depth: 0",
        "id: filter",
        "EVENT_NAME: ${{ github.event_name }}",
        "BEFORE_SHA: ${{ github.event.before }}",
        "BASE_SHA: ${{ github.event.pull_request.base.sha }}",
        "HEAD_SHA: ${{ github.event.pull_request.head.sha || github.sha }}",
        'ZERO_SHA: "0000000000000000000000000000000000000000"',
        'case "$EVENT_NAME" in',
        "push)",
        "pull_request)",
        "workflow_dispatch)",
        '[ "$BEFORE_SHA" != "$ZERO_SHA" ]',
        'git cat-file -e "$BEFORE_SHA^{commit}" 2>/dev/null',
        '[ -z "$BASE_SHA" ]',
        'git diff --name-only -z "$BEFORE_SHA" "$HEAD_SHA" > "$RUNNER_TEMP/changed-paths.nul"',
        'git diff --name-only -z "$BASE_SHA" "$HEAD_SHA" > "$RUNNER_TEMP/changed-paths.nul"',
        'git ls-tree -r --name-only -z "$HEAD_SHA" > "$RUNNER_TEMP/changed-paths.nul"',
        "python3 scripts/select-affected-surfaces.py \\",
        "--root . \\",
        "--lane ci \\",
        '--paths-file "$RUNNER_TEMP/changed-paths.nul" \\',
        "--delimiter nul \\",
        "--format github-output >> \"$GITHUB_OUTPUT\"",
    )
    missing = [fragment for fragment in required_fragments if fragment not in changes]
    forbidden_fragments = (
        "dorny/paths-filter",
        "filters: |",
        "$(",
        "`",
    )
    present = [fragment for fragment in forbidden_fragments if fragment in changes]
    if missing or present:
        detail = []
        if missing:
            detail.append(f"missing={missing!r}")
        if present:
            detail.append(f"forbidden={present!r}")
        fail("SURFACE-LOCAL-CI-MISMATCH", "; ".join(detail))


def read_nul_paths(path: Path) -> list[str]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        fail("SURFACE-PATH-TRANSPORT", f"{path}: {exc}")
    if not payload:
        return []
    if not payload.endswith(b"\0"):
        fail("SURFACE-PATH-TRANSPORT", "NUL path input must be terminated")
    records = payload[:-1].split(b"\0")
    if any(record == b"" for record in records):
        fail("SURFACE-PATH-TRANSPORT", "NUL path input contains an empty record")
    try:
        return [record.decode("utf-8") for record in records]
    except UnicodeDecodeError as exc:
        fail("SURFACE-PATH-TRANSPORT", f"path input must be UTF-8: {exc}")


def tracked_paths(root: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail("SURFACE-GIT-INVENTORY", str(exc))
    payload = completed.stdout
    if payload and not payload.endswith(b"\0"):
        fail("SURFACE-GIT-INVENTORY", "git ls-files output is not NUL terminated")
    try:
        return [record.decode("utf-8") for record in payload.split(b"\0") if record]
    except UnicodeDecodeError as exc:
        fail("SURFACE-GIT-INVENTORY", f"tracked path must be UTF-8: {exc}")


def _mutate(contract: dict[str, Any], mutation: dict[str, Any]) -> None:
    if mutation["kind"] == "append-route":
        surface = next(
            row for row in contract["surfaces"] if row["id"] == mutation["surfaceId"]
        )
        surface["routes"].append(copy.deepcopy(mutation["route"]))
        return
    if mutation["kind"] == "replace-argv":
        validator = next(
            row
            for row in contract["validators"]
            if row["id"] == mutation["validatorId"]
        )
        validator["argv"] = list(mutation["argv"])
        return
    if mutation["kind"] == "replace-validator-lanes":
        validator = next(
            row
            for row in contract["validators"]
            if row["id"] == mutation["validatorId"]
        )
        validator["lanes"] = list(mutation["lanes"])
        return
    if mutation["kind"] == "append-validator-reference":
        surface = next(
            row for row in contract["surfaces"] if row["id"] == mutation["surfaceId"]
        )
        surface["validators"].append(mutation["validatorId"])
        return
    if mutation["kind"] == "append-ci-job-reference":
        surface = next(
            row for row in contract["surfaces"] if row["id"] == mutation["surfaceId"]
        )
        surface["ciJobs"].append(mutation["ciJobId"])
        return
    if mutation["kind"] == "replace-protected-level":
        surface = next(
            row for row in contract["surfaces"] if row["id"] == mutation["surfaceId"]
        )
        surface["protectedLevel"] = mutation["protectedLevel"]
        return
    if mutation["kind"] == "replace-fallback-status":
        validator = next(
            row
            for row in contract["validators"]
            if row["id"] == mutation["validatorId"]
        )
        validator["fallback"]["status"] = mutation["status"]
        return
    if mutation["kind"] == "replace-surface-fallback-status":
        surface = next(
            row for row in contract["surfaces"] if row["id"] == mutation["surfaceId"]
        )
        surface["fallback"]["status"] = mutation["status"]
        return
    if mutation["kind"] == "replace-evidence-lane":
        validator = next(
            row
            for row in contract["validators"]
            if row["id"] == mutation["validatorId"]
        )
        validator["evidenceLane"] = mutation["evidenceLane"]
        return
    if mutation["kind"] == "replace-ci-output":
        job = next(
            row for row in contract["ciJobs"] if row["id"] == mutation["ciJobId"]
        )
        job["output"] = mutation["output"]
        return
    fail("SURFACE-FIXTURE", f"unknown mutation {mutation['kind']!r}")


def run_self_test(root: Path) -> tuple[int, int, int, int, int, int]:
    contract = validate_contract(root)
    fixture = load_json(root / FIXTURE_PATH)
    expected_keys = {
        "schemaVersion",
        "surfaceCases",
        "selectionCases",
        "ciRangeCases",
        "rejectionCases",
        "argvPositiveCases",
        "mutationCases",
    }
    if set(fixture) != expected_keys or fixture["schemaVersion"] != 2:
        fail("SURFACE-FIXTURE", "fixture shape or version differs")

    surface_cases = fixture["surfaceCases"]
    required_names = {
        "workspace-readme",
        "gitignore",
        "environment-example",
        "root-provider-gateway",
        "governance",
        "templates",
        "shared-agent",
        "claude-adapter",
        "codex-adapter",
        "github",
        "gitops",
        "infrastructure",
        "policy",
        "scripts",
        "secrets",
        "tests",
        "traefik",
        "examples",
        "authored-doc",
        "generated-record",
        "root-config",
    }
    if {case.get("name") for case in surface_cases} != required_names:
        fail("SURFACE-FIXTURE", "surface case coverage differs")
    for case in surface_cases:
        actual = classify_path(contract, case["path"])["id"]
        if actual != case["expectedSurface"]:
            fail("SURFACE-SELF-TEST", f"{case['name']}: {actual}")

    for case in fixture["selectionCases"]:
        actual = select_paths(contract, case["paths"], case["lane"], root)
        if actual != case["expected"]:
            fail(
                "SURFACE-SELF-TEST",
                f"{case['name']}: expected {case['expected']!r}, got {actual!r}",
            )

    required_ci_range_cases = {
        "push-before-head-document-surfaces": ("push", "before-head"),
        "pull-request-base-head-document-surfaces": ("pull_request", "base-head"),
        "push-initial-head-tree-all-surfaces": ("push", "initial-head-tree"),
        "pull-request-base-head-protected-surfaces": (
            "pull_request",
            "base-head",
        ),
    }
    ci_range_cases = fixture["ciRangeCases"]
    observed_ci_ranges = {
        case.get("name"): (case.get("event"), case.get("rangeKind"))
        for case in ci_range_cases
    }
    if (
        len(ci_range_cases) != len(required_ci_range_cases)
        or observed_ci_ranges != required_ci_range_cases
    ):
        fail("SURFACE-FIXTURE", "push/pull-request range coverage differs")
    required_ci_paths = {
        "docs/03.specs/031-affected-surface-agent-qa/spec.md",
        "_workspace/README.md",
        "policy/conftest/kubernetes.rego",
        "gitops/clusters/local/root-application.yaml",
        "infrastructure/tests/verify-contracts-static.sh",
        "secrets/README.md",
        "traefik/traefik.yaml",
        ".agents/agents/supervisor.md",
        "docs/99.templates/support/template-routing.md",
        ".github/workflows/ci.yml",
    }
    observed_ci_paths = {
        path for case in ci_range_cases for path in case.get("paths", [])
    }
    if observed_ci_paths != required_ci_paths:
        fail("SURFACE-FIXTURE", "CI range path coverage differs")
    for case in ci_range_cases:
        if set(case) != {
            "name",
            "event",
            "rangeKind",
            "paths",
            "expectedJobs",
            "expectedGithubOutput",
        }:
            fail("SURFACE-FIXTURE", f"{case.get('name')}: CI range shape differs")
        actual = select_paths(contract, case["paths"], "ci", root)
        actual_output = github_output(contract, actual)
        if (
            actual["ciJobs"] != case["expectedJobs"]
            or actual_output != case["expectedGithubOutput"]
        ):
            fail(
                "SURFACE-LOCAL-CI-MISMATCH",
                f"{case['name']}: jobs={actual['ciJobs']!r} output={actual_output!r}",
            )

    validate_ci_workflow_selector(root)

    for case in fixture["rejectionCases"]:
        try:
            select_paths(contract, case["paths"], "affected", root)
        except ContractError as exc:
            if exc.code != case["expectedError"]:
                fail("SURFACE-SELF-TEST", f"{case['name']}: {exc.code}")
        else:
            fail("SURFACE-SELF-TEST", f"{case['name']}: mutation was accepted")

    positive_names = {
        "bash-script-argument-c",
        "python-script-argument-c",
        "node-script-argument-e",
        "bash-option-boundary",
    }
    if {case.get("name") for case in fixture["argvPositiveCases"]} != positive_names:
        fail("SURFACE-FIXTURE", "direct-script positive argv coverage differs")
    for case in fixture["argvPositiveCases"]:
        mutated = copy.deepcopy(contract)
        _mutate(
            mutated,
            {
                "kind": "replace-argv",
                "validatorId": case["validatorId"],
                "argv": case["argv"],
            },
        )
        validate_contract(root, mutated)

    required_argv_mutations = {
        "shell-eval-argv",
        "python-eval-argv",
        "node-eval-argv",
        "bash-eval-bundle-lc",
        "bash-eval-bundle-cl",
        "python-eval-bundle-Ic",
        "python-eval-bundle-cI",
        "node-eval-bundle-pe",
        "node-eval-bundle-ep",
        "node-eval-assignment",
        "node-print-assignment",
        "bash-command-assignment",
        "wrapper-trampoline",
        "option-before-script",
        "relative-executable-prefix",
        "dot-executable-prefix",
        "absolute-executable-prefix",
        "parent-executable-prefix",
        "executable-case-alias",
    }
    mutation_names = {case.get("name") for case in fixture["mutationCases"]}
    if not required_argv_mutations.issubset(mutation_names):
        fail("SURFACE-FIXTURE", "direct-script negative argv coverage differs")

    for case in fixture["mutationCases"]:
        mutated = copy.deepcopy(contract)
        _mutate(mutated, case["mutation"])
        try:
            validated = validate_contract(root, mutated)
            select_paths(validated, case["paths"], "affected", root)
        except ContractError as exc:
            if exc.code != case["expectedError"]:
                fail("SURFACE-SELF-TEST", f"{case['name']}: {exc.code}")
        else:
            fail("SURFACE-SELF-TEST", f"{case['name']}: mutation was accepted")

    root_result = select_paths(contract, ["README.md"], "ci", root)
    if json_output(root_result) != (
        '{"ciJobs":["pre-commit","repo-quality-static"],'
        '"protectedLevel":"review","unmatchedPaths":[],'
        '"validators":["repository-quality"]}'
    ):
        fail("SURFACE-SELF-TEST", "stable JSON output differs")
    if github_output(contract, root_result) != (
        "manifests=false\nprecommit=true\nrepo_quality=true"
    ):
        fail("SURFACE-SELF-TEST", "stable GitHub output differs")
    mixed_result = select_paths(
        contract,
        ["unowned/z.txt", "README.md", "unowned/a.txt"],
        "ci",
        root,
        collect_unmatched=True,
    )
    if mixed_result["unmatchedPaths"] != ["unowned/a.txt", "unowned/z.txt"]:
        fail("SURFACE-SELF-TEST", "unmatched path output is not sorted")

    with tempfile.TemporaryDirectory(prefix="affected-surface-") as directory:
        path_file = Path(directory) / "paths.nul"
        path_file.write_bytes(b"README.md\0gitops/README.md\0")
        if read_nul_paths(path_file) != ["README.md", "gitops/README.md"]:
            fail("SURFACE-SELF-TEST", "NUL records were not preserved")
        path_file.write_bytes(b"README\n.md\0")
        if read_nul_paths(path_file) != ["README\n.md"]:
            fail("SURFACE-SELF-TEST", "newline data changed record boundaries")
        path_file.write_bytes(b"README.md\n")
        try:
            read_nul_paths(path_file)
        except ContractError as exc:
            if exc.code != "SURFACE-PATH-TRANSPORT":
                fail("SURFACE-SELF-TEST", f"transport: {exc.code}")
        else:
            fail("SURFACE-SELF-TEST", "newline transport was accepted")

    return (
        len(surface_cases),
        len(fixture["selectionCases"]),
        len(ci_range_cases),
        len(fixture["rejectionCases"]),
        len(fixture["argvPositiveCases"]),
        len(fixture["mutationCases"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.self_test:
            (
                path_count,
                selection_count,
                ci_range_count,
                rejection_count,
                argv_positive_count,
                mutation_count,
            ) = run_self_test(root)
            contract = validate_contract(root)
            print(
                "[PASS] affected surface self-test passed: "
                f"surfaces={len(contract['surfaces'])} path_cases={path_count} "
                f"selection_cases={selection_count} rejection_cases={rejection_count} "
                f"ci_range_cases={ci_range_count} "
                f"argv_positive_cases={argv_positive_count} "
                f"mutation_cases={mutation_count}"
            )
            return 0

        contract = validate_contract(root)
        paths = tracked_paths(root)
        observed_surfaces = {
            (
                reject_symlink_traversal(root, path),
                classify_path(contract, path)["id"],
            )[1]
            for path in paths
        }
        print(
            "[PASS] affected surface validation passed: "
            f"paths={len(paths)} surfaces={len(observed_surfaces)}/"
            f"{len(contract['surfaces'])} validators={len(contract['validators'])} "
            f"ci_jobs={len(contract['ciJobs'])} uncovered=0 ambiguous=0"
        )
        return 0
    except ContractError as exc:
        print(f"[FAIL] {exc.code}: {exc.detail}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
