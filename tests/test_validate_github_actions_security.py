"""Independent fixture tests for GitHub Actions security validation."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/validate-github-actions-security.py"
FIXTURE_PATH = ROOT / "tests/fixtures/github-actions-security.json"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_github_actions_security", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


INTERNAL_USES_SHAPE_CASES = (
    ("quoted-local", "'./.github/actions/local-check'", []),
    ("numeric", "123", ["uses entries must be plain same-line scalar values"]),
    ("null", "null", ["uses entries must be plain same-line scalar values"]),
    ("mapping", "{}", ["uses entries must be plain same-line scalar values"]),
    ("list", "[]", ["uses entries must be plain same-line scalar values"]),
)
INTERNAL_ARTIFACT_RETENTION_CASES = (
    ("bool-true", True, ["upload-artifact retention-days must equal 7"]),
)
INTERNAL_ARTIFACT_RETENTION_SHAPE_CASES = (
    ("jobs-list", "jobs: [build]\n", ["workflow jobs must be a mapping"]),
    (
        "job-scalar",
        "jobs:\n  build: reusable-workflow\n",
        ["workflow job must be a mapping"],
    ),
    (
        "steps-mapping-upload",
        "jobs:\n"
        "  build:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      upload:\n"
        "        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7\n",
        ["job steps must be a list"],
    ),
    (
        "step-scalar",
        "jobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - not-a-step\n",
        ["job step must be a mapping"],
    ),
)


def _mapping_lines(mapping: dict, indent: int) -> list[str]:
    prefix = " " * indent
    return [f"{prefix}{key}: {value}" for key, value in mapping.items()]


def _write_self_test_case(root: Path, case: dict) -> None:
    workflow_name = case.get("workflow", "ci.yml")
    workflow_path = root / ".github" / "workflows" / workflow_name
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["name: Fixture", "'on': workflow_dispatch"]

    if "permissions" in case and "job" not in case:
        permissions = case["permissions"]
        if isinstance(permissions, dict):
            lines.append("permissions:")
            lines.extend(_mapping_lines(permissions, 2))
        else:
            lines.append(f"permissions: {permissions}")
        lines.append("jobs: {}")
    else:
        lines.extend(["permissions:", "  contents: read", "jobs:"])
        job_id = case.get("job", "build")
        lines.append(f"  {job_id}:")
        if "permissions" in case:
            lines.append("    permissions:")
            lines.extend(_mapping_lines(case["permissions"], 6))
        lines.extend(["    runs-on: ubuntu-latest", "    steps:"])
        if "uses" in case:
            suffix = f" # {case['comment']}" if case.get("comment") else ""
            lines.append(f"      - uses: {case['uses']}{suffix}")
        else:
            lines.append("      - run: 'true'")
    workflow_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if "zizmor" in case:
        (root / ".github" / "zizmor.yml").write_text(
            yaml.safe_dump(case["zizmor"], sort_keys=False), encoding="utf-8"
        )


def _write_artifact_retention_case(
    root: Path,
    retention: object,
    *,
    uses: str = "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
) -> None:
    path = root / ".github" / "workflows" / "ci.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "name: Artifact retention fixture",
        "'on': workflow_dispatch",
        "permissions:",
        "  contents: read",
        "jobs:",
        "  build:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        f"      - uses: {uses} # v7",
        "        with:",
        "          name: artifact",
        "          path: artifact.txt",
    ]
    if retention is not None:
        rendered_retention = yaml.safe_dump(retention, default_flow_style=True).strip()
        lines.append(f"          retention-days: {rendered_retention}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_artifact_retention_shape_case(root: Path, body: str) -> None:
    path = root / ".github" / "workflows" / "ci.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "name: Artifact retention shape fixture\n"
        "'on': workflow_dispatch\n"
        "permissions:\n"
        "  contents: read\n" + body,
        encoding="utf-8",
    )


def _write_valid_workflow(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "name: Boundary fixture\n"
        "'on': workflow_dispatch\n"
        "permissions:\n"
        "  contents: read\n"
        "jobs: {}\n",
        encoding="utf-8",
    )


def _run_repository_boundary_case(validator, temp_root: Path, case: dict) -> list[str]:
    setup = case["setup"]
    case_root = temp_root / "repository"
    external = temp_root / "external"
    external.mkdir()

    if setup == "missing-root":
        return validator.validate_repository(case_root)
    if setup == "root-symlink":
        _write_valid_workflow(external / ".github" / "workflows" / "ci.yml")
        case_root.symlink_to(external, target_is_directory=True)
        result = subprocess.run(
            [sys.executable, os.fspath(SCRIPT_PATH), "--root", os.fspath(case_root)],
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        if result.returncode != 1:
            return ["CLI root-symlink probe did not fail"]
        return [
            line.removeprefix("FAIL: ")
            for line in result.stdout.splitlines()
            if line.startswith("FAIL: ")
        ]

    case_root.mkdir()
    if setup == "missing-github":
        return validator.validate_repository(case_root)
    if setup == "github-symlink":
        _write_valid_workflow(external / "workflows" / "ci.yml")
        (case_root / ".github").symlink_to(external, target_is_directory=True)
        return validator.validate_repository(case_root)

    github_dir = case_root / ".github"
    github_dir.mkdir()
    if setup == "missing-workflows":
        return validator.validate_repository(case_root)
    if setup == "workflows-symlink":
        _write_valid_workflow(external / "ci.yml")
        (github_dir / "workflows").symlink_to(external, target_is_directory=True)
        return validator.validate_repository(case_root)

    workflow_dir = github_dir / "workflows"
    workflow_dir.mkdir()
    if setup == "empty-workflows":
        return validator.validate_repository(case_root)

    _write_valid_workflow(workflow_dir / "ci.yml")
    if setup == "workflow-file-symlink":
        _write_valid_workflow(external / "linked.yml")
        (workflow_dir / "linked.yml").symlink_to(external / "linked.yml")
    elif setup == "workflow-nonregular-file":
        (workflow_dir / "directory.yml").mkdir()
    elif setup == "zizmor-symlink":
        (external / "zizmor.yml").write_text(
            "rules:\n  unpinned-uses:\n    disable: true\n", encoding="utf-8"
        )
        (github_dir / "zizmor.yml").symlink_to(external / "zizmor.yml")
    else:
        raise ValueError(f"unknown repository boundary setup: {setup}")
    return validator.validate_repository(case_root)


def _write_required_write_case(validator, root: Path, case: dict) -> None:
    workflow = case["workflow"]
    job_id = case["job"]
    mutation = case["mutation"]
    required = validator.ALLOWED_JOB_WRITES[(workflow, job_id)]
    path = root / ".github" / "workflows" / workflow
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "name: Required write fixture",
        "'on': workflow_dispatch",
        "permissions:",
        "  contents: read",
        "jobs:",
    ]
    if mutation == "missing-job":
        lines.append("  other: {runs-on: ubuntu-latest, steps: []}")
    else:
        lines.extend([f"  {job_id}:", "    runs-on: ubuntu-latest"])
        if mutation != "missing-permissions":
            permissions = {key: "write" for key in sorted(required)}
            if mutation == "extra-read":
                permissions["contents"] = "read"
            elif mutation == "all-read":
                permissions = {key: "read" for key in sorted(required)}
            elif mutation == "missing-write":
                permissions.pop(sorted(required)[0])
                permissions["contents"] = "read"
            elif mutation == "extra-write":
                permissions["pages"] = "write"
            lines.append("    permissions:")
            lines.extend(_mapping_lines(permissions, 6))
        lines.append("    steps: []")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_uses_shape_case(root: Path, raw_uses: str) -> None:
    path = root / ".github" / "workflows" / "ci.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "name: Uses shape fixture\n"
        "'on': workflow_dispatch\n"
        "permissions:\n"
        "  contents: read\n"
        "jobs:\n"
        "  build:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        f"      - uses: {raw_uses}\n",
        encoding="utf-8",
    )


class GitHubActionsSecurityFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def observed(self, root: Path) -> list[str]:
        return [
            item.rsplit(": ", 1)[-1]
            for item in self.validator.validate_repository(root)
        ]

    def test_primary_cases(self) -> None:
        for case in self.fixture["cases"]:
            with (
                self.subTest(case=case["name"]),
                tempfile.TemporaryDirectory(prefix="actions-security-") as directory,
            ):
                root = Path(directory)
                _write_self_test_case(root, case)
                self.assertEqual(self.observed(root), case["expected"])

    def test_repository_boundaries(self) -> None:
        for case in self.fixture["repositoryBoundaryCases"]:
            with (
                self.subTest(case=case["name"]),
                tempfile.TemporaryDirectory(
                    prefix="actions-security-boundary-"
                ) as directory,
            ):
                actual = [
                    item.rsplit(": ", 1)[-1]
                    for item in _run_repository_boundary_case(
                        self.validator, Path(directory), case
                    )
                ]
                self.assertEqual(actual, case["expected"])

    def test_required_write_cases(self) -> None:
        for case in self.fixture["requiredWriteCases"]:
            with (
                self.subTest(case=case["name"]),
                tempfile.TemporaryDirectory(
                    prefix="actions-security-permissions-"
                ) as directory,
            ):
                root = Path(directory)
                _write_required_write_case(self.validator, root, case)
                self.assertEqual(self.observed(root), case["expected"])

    def test_artifact_retention_cases(self) -> None:
        for case in self.fixture["artifactRetentionCases"]:
            with (
                self.subTest(case=case["name"]),
                tempfile.TemporaryDirectory(
                    prefix="actions-security-retention-"
                ) as directory,
            ):
                root = Path(directory)
                _write_artifact_retention_case(root, case["retention"])
                self.assertEqual(self.observed(root), case["expected"])

    def test_internal_shape_cases(self) -> None:
        groups = (
            (
                INTERNAL_ARTIFACT_RETENTION_CASES,
                _write_artifact_retention_case,
            ),
            (
                INTERNAL_ARTIFACT_RETENTION_SHAPE_CASES,
                _write_artifact_retention_shape_case,
            ),
            (
                INTERNAL_USES_SHAPE_CASES,
                _write_uses_shape_case,
            ),
        )
        for cases, writer in groups:
            for name, value, expected in cases:
                with (
                    self.subTest(case=name),
                    tempfile.TemporaryDirectory(
                        prefix="actions-security-shape-"
                    ) as directory,
                ):
                    root = Path(directory)
                    writer(root, value)
                    self.assertEqual(self.observed(root), expected)


if __name__ == "__main__":
    unittest.main()
