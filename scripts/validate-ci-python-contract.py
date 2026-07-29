#!/usr/bin/env python3
"""Validate the exact network-free CI Python and pre-commit contract."""

from __future__ import annotations

import argparse
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any, NoReturn

import yaml


REQUIREMENTS_PATH = Path(".github/requirements/ci-validation.txt")
WORKFLOW_PATH = Path(".github/workflows/ci.yml")
INVENTORY_PATH = Path(
    "docs/90.references/data/tech-stack-version-inventory.md"
)
EXPECTED_REQUIREMENT_LINES = (
    "jsonschema==4.26.0",
    "pre-commit==4.6.1",
    "PyYAML==6.0.3",
)
EXPECTED_PINS = {
    "jsonschema": "4.26.0",
    "pre-commit": "4.6.1",
    "pyyaml": "6.0.3",
}
EXPECTED_INVENTORY_PINS = {
    "jsonschema": "4.26.0",
    "pre-commit": "4.6.1",
    "PyYAML": "6.0.3",
}
GITLEAKS_SHA256 = (
    "79a3ab579b53f71efd634f3aaf7e04a0fa0cf206b7ed434638d1547a2470a66e"  # pragma: allowlist secret
)
EXPECTED_GITLEAKS_INVENTORY = {
    "version": "8.30.0",
    "asset": "gitleaks_8.30.0_linux_x64.tar.gz",
    "sha256": GITLEAKS_SHA256,
    "install_path": "/usr/local/bin/gitleaks",
}
EXPECTED_PYTHON = "3.12"
VALIDATION_JOBS = (
    "pre-commit",
    "repo-quality-static",
    "agent-governance-static",
    "manifest-static",
)
AGENT_GOVERNANCE_JOB = "agent-governance-static"
INSTALL_COMMAND = (
    "python -m pip install --disable-pip-version-check "
    "--requirement .github/requirements/ci-validation.txt"
)
PRE_COMMIT_COMMAND = "pre-commit run --all-files --show-diff-on-failure"
GITLEAKS_JOBS = ("pre-commit", "repo-quality-static")
GITLEAKS_INSTALL_COMMAND = f"""\
set -euo pipefail
curl --fail --location --silent --show-error \\
  https://github.com/gitleaks/gitleaks/releases/download/v8.30.0/gitleaks_8.30.0_linux_x64.tar.gz \\
  --output "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz"
gitleaks_sha256='{GITLEAKS_SHA256}' # pragma: allowlist secret
printf '%s  %s\\n' "$gitleaks_sha256" "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" | sha256sum --check --strict
tar -xzf "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" -C "$RUNNER_TEMP" gitleaks
sudo install -o root -g root -m 0755 "$RUNNER_TEMP/gitleaks" /usr/local/bin/gitleaks"""
PIN_PATTERN = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)"
    r"==(?P<version>[A-Za-z0-9][A-Za-z0-9.+_-]*)$"
)
PIP_INSTALL_PATTERN = re.compile(
    r"(?:^|\s)(?:python(?:3)?\s+-m\s+pip|pip(?:3)?)\s+install(?:\s|$)"
)
INVENTORY_FENCE_PATTERN = re.compile(
    r"^### Version Contracts[^\n]*\n"
    r".*?^```yaml[ \t]*\n(?P<yaml>.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


class ContractError(ValueError):
    """A stable CI Python contract finding."""

    def __init__(self, rule_id: str, detail: str):
        self.rule_id = rule_id
        self.detail = detail
        super().__init__(f"{rule_id}: {detail}")


def fail(rule_id: str, detail: str) -> NoReturn:
    raise ContractError(rule_id, detail)


def canonical_package_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


class DuplicateKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects every duplicate mapping key."""


def _construct_mapping_without_duplicates(
    loader: DuplicateKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    seen: set[Any] = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in seen
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "unhashable YAML mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                f"duplicate YAML mapping key: {key!r}",
                key_node.start_mark,
            )
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


DuplicateKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping_without_duplicates,
)


def _read_regular_text(root: Path, relative: Path, rule_id: str) -> str:
    path = root / relative
    try:
        metadata = os.lstat(path)
    except OSError as exc:
        fail(rule_id, f"{relative.as_posix()} is unavailable: {exc.strerror}")
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        fail(rule_id, f"{relative.as_posix()} must be a regular non-symlink file")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(rule_id, f"{relative.as_posix()} cannot be read as UTF-8: {exc}")


def _load_yaml(text: str, rule_id: str, source: Path) -> dict[str, Any]:
    try:
        value = yaml.load(text, Loader=DuplicateKeyLoader)
    except yaml.YAMLError as exc:
        fail(rule_id, f"{source.as_posix()} YAML is invalid: {exc}")
    if not isinstance(value, dict):
        fail(rule_id, f"{source.as_posix()} YAML root must be a mapping")
    return value


def _validate_requirements(text: str) -> None:
    expected_text = "\n".join(EXPECTED_REQUIREMENT_LINES) + "\n"
    if text != expected_text:
        fail(
            "CI-PYTHON-PIN",
            f"{REQUIREMENTS_PATH.as_posix()} must contain exactly the three ordered pins",
        )

    observed: dict[str, str] = {}
    for line in text.splitlines():
        match = PIN_PATTERN.fullmatch(line)
        if match is None:
            fail("CI-PYTHON-PIN", "every dependency must use one exact == pin")
        package = canonical_package_name(match.group("name"))
        if package in observed:
            fail("CI-PYTHON-PIN", f"duplicate dependency name: {package}")
        observed[package] = match.group("version")
    if observed != EXPECTED_PINS:
        fail("CI-PYTHON-PIN", "dependency names or versions differ")


def _inventory_contract(text: str) -> dict[str, Any]:
    matches = list(INVENTORY_FENCE_PATTERN.finditer(text))
    if len(matches) != 1:
        fail(
            "CI-PYTHON-INVENTORY",
            "technology inventory must contain one Version Contracts YAML fence",
        )
    return _load_yaml(
        matches[0].group("yaml"),
        "CI-PYTHON-INVENTORY",
        INVENTORY_PATH,
    )


def _validate_inventory(inventory: dict[str, Any]) -> None:
    if inventory.get("ci_python") != EXPECTED_PYTHON:
        fail("CI-PYTHON-INVENTORY", "ci_python must mirror Python 3.12")
    dependencies = inventory.get("ci_python_dependencies")
    if dependencies != EXPECTED_INVENTORY_PINS:
        fail(
            "CI-PYTHON-INVENTORY",
            "ci_python_dependencies must mirror the exact requirements owner",
        )
    if inventory.get("ci_gitleaks") != EXPECTED_GITLEAKS_INVENTORY:
        fail(
            "CI-GITLEAKS-TOOL",
            "ci_gitleaks must mirror the exact release asset, digest, and install path",
        )


def _steps_for_job(workflow: dict[str, Any], job_id: str) -> list[dict[str, Any]]:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-PYTHON-WORKFLOW", "workflow jobs must be a mapping")
    job = jobs.get(job_id)
    if not isinstance(job, dict):
        fail("CI-PYTHON-WORKFLOW", f"validation job is missing: {job_id}")
    steps = job.get("steps")
    if not isinstance(steps, list) or any(not isinstance(step, dict) for step in steps):
        fail("CI-PYTHON-WORKFLOW", f"{job_id} steps must be a mapping list")
    return steps


def _run_text(step: dict[str, Any]) -> str:
    value = step.get("run")
    return value.strip() if isinstance(value, str) else ""


def _validate_python_versions(
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    for job_id, steps in job_steps.items():
        setup_steps = [
            step
            for step in steps
            if isinstance(step.get("uses"), str)
            and step["uses"].startswith("actions/setup-python@")
        ]
        if len(setup_steps) != 1:
            fail(
                "CI-PYTHON-VERSION",
                f"{job_id} must contain exactly one actions/setup-python step",
            )
        setup_with = setup_steps[0].get("with")
        if not isinstance(setup_with, dict) or setup_with.get(
            "python-version"
        ) != EXPECTED_PYTHON:
            fail("CI-PYTHON-VERSION", f"{job_id} must select Python 3.12")


def _validate_shared_installs(
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    for job_id, steps in job_steps.items():
        run_commands = [_run_text(step) for step in steps]
        if run_commands.count(INSTALL_COMMAND) != 1:
            fail(
                "CI-PYTHON-WORKFLOW",
                f"{job_id} must contain exactly one shared requirements install",
            )
        install_commands = [
            command for command in run_commands if PIP_INSTALL_PATTERN.search(command)
        ]
        if install_commands != [INSTALL_COMMAND]:
            fail(
                "CI-PYTHON-WORKFLOW",
                f"{job_id} must not install loose inline Python packages",
            )


def _validate_no_outside_python_validation(workflow: dict[str, Any]) -> None:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-PYTHON-WORKFLOW", "workflow jobs must be a mapping")
    for job_id, job in jobs.items():
        if job_id in VALIDATION_JOBS or not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if isinstance(uses, str) and uses.startswith("actions/setup-python@"):
                fail(
                    "CI-PYTHON-WORKFLOW",
                    f"non-validation job must not own setup-python: {job_id}",
                )
            if PIP_INSTALL_PATTERN.search(_run_text(step)):
                fail(
                    "CI-PYTHON-WORKFLOW",
                    f"non-validation job must not own a pip install: {job_id}",
                )


def _validate_pre_commit_execution(
    workflow: dict[str, Any],
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-PRECOMMIT-ALL-FILES", "workflow jobs must be a mapping")
    all_run_commands: list[str] = []
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        all_run_commands.extend(
            _run_text(step)
            for step in steps
            if isinstance(step, dict) and _run_text(step)
        )
    pre_commit_commands = [
        command for command in all_run_commands if "pre-commit run" in command
    ]
    if pre_commit_commands != [PRE_COMMIT_COMMAND]:
        fail(
            "CI-PRECOMMIT-ALL-FILES",
            "workflow must contain exactly one explicit all-files/show-diff command",
        )

    pre_commit_steps = job_steps["pre-commit"]
    if [_run_text(step) for step in pre_commit_steps].count(PRE_COMMIT_COMMAND) != 1:
        fail(
            "CI-PRECOMMIT-ALL-FILES",
            "the explicit all-files/show-diff command must run in pre-commit",
        )
    checkout_steps = [
        step
        for step in pre_commit_steps
        if isinstance(step.get("uses"), str)
        and step["uses"].startswith("actions/checkout@")
    ]
    if len(checkout_steps) != 1:
        fail(
            "CI-PRECOMMIT-HISTORY",
            "pre-commit must contain exactly one checkout step",
        )
    checkout_with = checkout_steps[0].get("with")
    if not isinstance(checkout_with, dict) or checkout_with.get("fetch-depth") != 0:
        fail(
            "CI-PRECOMMIT-HISTORY",
            "pre-commit checkout must use fetch-depth: 0",
        )


def _validate_gitleaks_tool(
    workflow: dict[str, Any],
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    for job_id in GITLEAKS_JOBS:
        commands = [_run_text(step) for step in job_steps[job_id]]
        if commands.count(GITLEAKS_INSTALL_COMMAND) != 1:
            fail(
                "CI-GITLEAKS-TOOL",
                f"{job_id} must install the exact verified Gitleaks release",
            )

    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-GITLEAKS-TOOL", "workflow jobs must be a mapping")
    for job_id, job in jobs.items():
        if job_id in GITLEAKS_JOBS or not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        if any(
            "gitleaks/releases/download" in _run_text(step)
            or "/usr/local/bin/gitleaks" in _run_text(step)
            for step in steps
            if isinstance(step, dict)
        ):
            fail(
                "CI-GITLEAKS-TOOL",
                f"non-owning job must not install Gitleaks: {job_id}",
            )


def _validate_repository_history(
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    steps = job_steps["repo-quality-static"]
    checkout_steps = [
        step
        for step in steps
        if isinstance(step.get("uses"), str)
        and step["uses"].startswith("actions/checkout@")
    ]
    if len(checkout_steps) != 1:
        fail(
            "CI-REPOSITORY-HISTORY",
            "repo-quality-static must contain exactly one checkout step",
        )
    checkout_with = checkout_steps[0].get("with")
    if not isinstance(checkout_with, dict) or checkout_with.get("fetch-depth") != 0:
        fail(
            "CI-REPOSITORY-HISTORY",
            "repo-quality-static checkout must use fetch-depth: 0",
        )


def _validate_agent_governance_checkout(
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    steps = job_steps[AGENT_GOVERNANCE_JOB]
    checkout_steps = [
        step
        for step in steps
        if isinstance(step.get("uses"), str)
        and step["uses"].startswith("actions/checkout@")
    ]
    if len(checkout_steps) != 1:
        fail(
            "CI-AGENT-GOVERNANCE-CHECKOUT",
            "agent-governance-static must contain exactly one checkout step",
        )
    checkout_with = checkout_steps[0].get("with")
    if checkout_with != {
        "persist-credentials": False,
        "fetch-depth": 0,
    }:
        fail(
            "CI-AGENT-GOVERNANCE-CHECKOUT",
            "agent-governance-static checkout must disable credentials and fetch full history",
        )


def validate_repository(root: Path) -> int:
    root = Path(root)
    requirements_text = _read_regular_text(
        root,
        REQUIREMENTS_PATH,
        "CI-PYTHON-PIN",
    )
    inventory_text = _read_regular_text(
        root,
        INVENTORY_PATH,
        "CI-PYTHON-INVENTORY",
    )
    workflow_text = _read_regular_text(
        root,
        WORKFLOW_PATH,
        "CI-PYTHON-WORKFLOW",
    )

    _validate_requirements(requirements_text)
    inventory = _inventory_contract(inventory_text)
    _validate_inventory(inventory)
    workflow = _load_yaml(workflow_text, "CI-PYTHON-WORKFLOW", WORKFLOW_PATH)

    if (
        "pre-commit/action" in workflow_text.lower()
        or "pre-commit/action" in inventory_text.lower()
    ):
        fail(
            "CI-PRECOMMIT-ACTION",
            "pre-commit/action must be absent from workflow and inventory",
        )

    job_steps = {
        job_id: _steps_for_job(workflow, job_id) for job_id in VALIDATION_JOBS
    }
    _validate_no_outside_python_validation(workflow)
    _validate_python_versions(job_steps)
    _validate_shared_installs(job_steps)
    _validate_pre_commit_execution(workflow, job_steps)
    _validate_gitleaks_tool(workflow, job_steps)
    _validate_repository_history(job_steps)
    _validate_agent_governance_checkout(job_steps)
    return len(job_steps)


def _valid_self_test_content() -> tuple[str, str, str]:
    requirements = "\n".join(EXPECTED_REQUIREMENT_LINES) + "\n"
    inventory = f"""\
### Version Contracts

```yaml
ci_python: '3.12'
ci_python_dependencies:
  jsonschema: '4.26.0'
  pre-commit: '4.6.1'
  PyYAML: '6.0.3'
ci_gitleaks:
  version: '8.30.0'
  asset: 'gitleaks_8.30.0_linux_x64.tar.gz'
  sha256: '{GITLEAKS_SHA256}' # pragma: allowlist secret
  install_path: '/usr/local/bin/gitleaks'
```
"""
    workflow = f"""\
name: CI
jobs:
  pre-commit:
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
        with:
          fetch-depth: 0
      - uses: actions/setup-python@0123456789abcdef0123456789abcdef01234567
        with:
          python-version: '3.12'
      - run: {INSTALL_COMMAND}
      - run: |
          {GITLEAKS_INSTALL_COMMAND.replace(chr(10), chr(10) + "          ")}
      - run: {PRE_COMMIT_COMMAND}
  repo-quality-static:
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
        with:
          fetch-depth: 0
      - uses: actions/setup-python@0123456789abcdef0123456789abcdef01234567
        with:
          python-version: '3.12'
      - run: {INSTALL_COMMAND}
      - run: |
          {GITLEAKS_INSTALL_COMMAND.replace(chr(10), chr(10) + "          ")}
  agent-governance-static:
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
        with:
          persist-credentials: false
          fetch-depth: 0
      - uses: actions/setup-python@0123456789abcdef0123456789abcdef01234567
        with:
          python-version: '3.12'
      - run: {INSTALL_COMMAND}
      - run: python3 scripts/validate-agent-harness-contract.py --root .
  manifest-static:
    steps:
      - uses: actions/checkout@0123456789abcdef0123456789abcdef01234567
      - uses: actions/setup-python@0123456789abcdef0123456789abcdef01234567
        with:
          python-version: '3.12'
      - run: {INSTALL_COMMAND}
"""
    return requirements, inventory, workflow


def _write_self_test_root(
    root: Path,
    requirements: str,
    inventory: str,
    workflow: str,
) -> None:
    (root / REQUIREMENTS_PATH.parent).mkdir(parents=True)
    (root / WORKFLOW_PATH.parent).mkdir(parents=True, exist_ok=True)
    (root / INVENTORY_PATH.parent).mkdir(parents=True)
    (root / REQUIREMENTS_PATH).write_text(requirements, encoding="utf-8")
    (root / INVENTORY_PATH).write_text(inventory, encoding="utf-8")
    (root / WORKFLOW_PATH).write_text(workflow, encoding="utf-8")


def run_self_test() -> int:
    requirements, inventory, workflow = _valid_self_test_content()
    repository_job_start = workflow.find("  repo-quality-static:\n")
    repository_history = workflow.find(
        "          fetch-depth: 0\n",
        repository_job_start,
    )
    if repository_job_start < 0 or repository_history < 0:
        fail(
            "CI-PYTHON-WORKFLOW",
            "self-test fixture lacks repo-quality-static full history",
        )
    shallow_repo_quality = (
        workflow[:repository_history]
        + workflow[
            repository_history + len("          fetch-depth: 0\n") :
        ]
    )
    agent_job_start = workflow.find("  agent-governance-static:\n")
    agent_persist_credentials = workflow.find(
        "          persist-credentials: false\n",
        agent_job_start,
    )
    if agent_job_start < 0 or agent_persist_credentials < 0:
        fail(
            "CI-PYTHON-WORKFLOW",
            "self-test fixture lacks agent-governance-static checkout hardening",
        )
    credential_persisting_agent = (
        workflow[:agent_persist_credentials]
        + workflow[
            agent_persist_credentials
            + len("          persist-credentials: false\n") :
        ]
    )
    mutations = (
        (
            "CI-PYTHON-PIN",
            requirements.replace("jsonschema==", "jsonschema>=", 1),
            inventory,
            workflow,
        ),
        (
            "CI-PYTHON-INVENTORY",
            requirements,
            inventory.replace("4.26.0", "4.25.1", 1),
            workflow,
        ),
        (
            "CI-PYTHON-VERSION",
            requirements,
            inventory,
            workflow.replace("python-version: '3.12'", "python-version: '3.x'", 1),
        ),
        (
            "CI-PYTHON-WORKFLOW",
            requirements,
            inventory,
            workflow.replace(INSTALL_COMMAND, "python -m pip install pyyaml", 1),
        ),
        (
            "CI-PYTHON-WORKFLOW",
            requirements,
            inventory,
            workflow
            + """\
  unexpected-python:
    steps:
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.x'
      - run: python -m pip install pyyaml jsonschema
""",
        ),
        (
            "CI-PRECOMMIT-ACTION",
            requirements,
            inventory,
            workflow + "\n# pre-commit/action@0123456789abcdef\n",
        ),
        (
            "CI-PRECOMMIT-ALL-FILES",
            requirements,
            inventory,
            workflow.replace(
                PRE_COMMIT_COMMAND,
                "pre-commit run --all-files",
                1,
            ),
        ),
        (
            "CI-PRECOMMIT-HISTORY",
            requirements,
            inventory,
            workflow.replace("          fetch-depth: 0\n", "", 1),
        ),
        (
            "CI-GITLEAKS-TOOL",
            requirements,
            inventory,
            workflow.replace(
                "sudo install -o root -g root -m 0755 "
                '"$RUNNER_TEMP/gitleaks" /usr/local/bin/gitleaks',
                "true",
                1,
            ),
        ),
        (
            "CI-GITLEAKS-TOOL",
            requirements,
            inventory,
            workflow.replace(
                EXPECTED_GITLEAKS_INVENTORY["sha256"],
                "0" * 64,
                1,
            ),
        ),
        (
            "CI-GITLEAKS-TOOL",
            requirements,
            inventory,
            workflow.replace("sha256sum --check --strict", "cat", 1),
        ),
        (
            "CI-REPOSITORY-HISTORY",
            requirements,
            inventory,
            shallow_repo_quality,
        ),
        (
            "CI-AGENT-GOVERNANCE-CHECKOUT",
            requirements,
            inventory,
            credential_persisting_agent,
        ),
    )

    with tempfile.TemporaryDirectory(prefix="ci-python-contract-self-test-") as raw:
        root = Path(raw)
        _write_self_test_root(root, requirements, inventory, workflow)
        validate_repository(root)

    for expected_rule, mutated_requirements, mutated_inventory, mutated_workflow in mutations:
        with tempfile.TemporaryDirectory(
            prefix="ci-python-contract-self-test-"
        ) as raw:
            root = Path(raw)
            _write_self_test_root(
                root,
                mutated_requirements,
                mutated_inventory,
                mutated_workflow,
            )
            try:
                validate_repository(root)
            except ContractError as exc:
                if exc.rule_id != expected_rule:
                    fail(
                        "CI-PYTHON-WORKFLOW",
                        f"self-test expected {expected_rule}, got {exc.rule_id}",
                    )
            else:
                fail(
                    "CI-PYTHON-WORKFLOW",
                    f"self-test mutation was accepted: {expected_rule}",
                )

    with tempfile.TemporaryDirectory(prefix="ci-python-contract-self-test-") as raw:
        root = Path(raw)
        _write_self_test_root(root, requirements, inventory, workflow)
        requirements_path = root / REQUIREMENTS_PATH
        requirements_copy = root / "requirements-copy.txt"
        requirements_copy.write_text(requirements, encoding="utf-8")
        requirements_path.unlink()
        requirements_path.symlink_to(requirements_copy)
        try:
            validate_repository(root)
        except ContractError as exc:
            if exc.rule_id != "CI-PYTHON-PIN":
                fail(
                    "CI-PYTHON-WORKFLOW",
                    f"symlink self-test emitted {exc.rule_id}",
                )
        else:
            fail("CI-PYTHON-WORKFLOW", "symlink requirements input was accepted")

    return len(mutations) + 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            case_count = run_self_test()
            print(
                "[PASS] CI Python contract self-test passed: "
                f"rules=10 cases={case_count}"
            )
            return 0
        job_count = validate_repository(args.root)
        print(
            "[PASS] CI Python contract validation passed: "
            f"jobs={job_count} pins={len(EXPECTED_PINS)}"
        )
        return 0
    except ContractError as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
