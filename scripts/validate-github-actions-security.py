#!/usr/bin/env python3
"""Validate immutable GitHub Action identities and least-privilege permissions."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Literal

import yaml


REMOTE_REF = re.compile(r"^[^\s/@]+/[^\s@]+(?:/[^\s@]+)*@([0-9a-f]{40})$")
DOCKER_REF = re.compile(r"^docker://[^\s@]+@sha256:([0-9a-f]{64})$")
VERSION_COMMENT = re.compile(r"#\s*(v?[0-9]+(?:\.[0-9]+){0,2})\s*$")
USES_LINE = re.compile(r"^\s*(?:-\s*)?uses\s*:\s*(?P<value>.+?)\s*$")
ALLOWED_JOB_WRITES = {
    ("greetings.yml", "greeting"): {"issues", "pull-requests"},
    ("labeler.yml", "label"): {"pull-requests"},
    ("stale.yml", "stale"): {"issues", "pull-requests"},
}
EXPECTED_CASES = [
    {
        "name": "valid-remote-sha",
        "uses": "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "comment": "v7.0.0",
        "expected": [],
    },
    {
        "name": "remote-tag",
        "uses": "actions/checkout@v7.0.0",
        "comment": "v7.0.0",
        "expected": ["remote uses must use a forty-character commit SHA"],
    },
    {
        "name": "missing-version-comment",
        "uses": "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "comment": "",
        "expected": ["remote uses must retain a version comment"],
    },
    {
        "name": "valid-local",
        "uses": "./.github/actions/local-check",
        "comment": "",
        "expected": [],
    },
    {
        "name": "valid-docker-digest",
        "uses": "docker://alpine@sha256:"
        + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "comment": "3.22.1",
        "expected": [],
    },
    {
        "name": "mutable-docker",
        "uses": "docker://alpine:3.22.1",
        "comment": "3.22.1",
        "expected": ["docker uses must use a sha256 digest"],
    },
    {
        "name": "broad-write",
        "permissions": {"contents": "write"},
        "expected": ["workflow default permissions must be read-only"],
    },
    {
        "name": "valid-allowlisted-job",
        "workflow": "greetings.yml",
        "job": "greeting",
        "permissions": {"issues": "write", "pull-requests": "write"},
        "expected": [],
    },
    {
        "name": "unlisted-write",
        "workflow": "ci.yml",
        "job": "build",
        "permissions": {"pages": "write"},
        "expected": ["write permission is not allowlisted"],
    },
    {
        "name": "write-all",
        "permissions": "write-all",
        "expected": ["write-all is forbidden"],
    },
    {
        "name": "unpinned-suppression",
        "zizmor": {"rules": {"unpinned-uses": {"disable": True}}},
        "expected": ["unpinned-uses suppression is forbidden"],
    },
]
EXPECTED_REPOSITORY_BOUNDARY_CASES = [
    {
        "name": "missing-root",
        "setup": "missing-root",
        "expected": ["repository root must be an existing non-symlink directory"],
    },
    {
        "name": "root-symlink",
        "setup": "root-symlink",
        "expected": ["repository root must be an existing non-symlink directory"],
    },
    {
        "name": "missing-github",
        "setup": "missing-github",
        "expected": [".github must be an existing non-symlink directory"],
    },
    {
        "name": "github-symlink",
        "setup": "github-symlink",
        "expected": [".github must be an existing non-symlink directory"],
    },
    {
        "name": "missing-workflows",
        "setup": "missing-workflows",
        "expected": [
            "workflow directory must be an existing non-symlink directory"
        ],
    },
    {
        "name": "workflows-symlink",
        "setup": "workflows-symlink",
        "expected": [
            "workflow directory must be an existing non-symlink directory"
        ],
    },
    {
        "name": "empty-workflows",
        "setup": "empty-workflows",
        "expected": [
            "workflow directory must contain at least one regular workflow YAML file"
        ],
    },
    {
        "name": "workflow-file-symlink",
        "setup": "workflow-file-symlink",
        "expected": ["workflow YAML must be a non-symlink regular file"],
    },
    {
        "name": "workflow-nonregular-file",
        "setup": "workflow-nonregular-file",
        "expected": ["workflow YAML must be a non-symlink regular file"],
    },
    {
        "name": "zizmor-symlink",
        "setup": "zizmor-symlink",
        "expected": [
            "zizmor configuration must be a non-symlink regular file"
        ],
    },
]
EXPECTED_REQUIRED_WRITE_CASES = [
    {
        "name": f"{workflow.removesuffix('.yml')}-{mutation}",
        "workflow": workflow,
        "job": job,
        "mutation": mutation,
        "expected": expected,
    }
    for workflow, job in (
        ("greetings.yml", "greeting"),
        ("labeler.yml", "label"),
        ("stale.yml", "stale"),
    )
    for mutation, expected in (
        ("exact-writes", []),
        ("extra-read", []),
        ("missing-job", ["required allowlisted job is missing"]),
        ("missing-permissions", ["required job permissions must be a mapping"]),
        ("all-read", ["required job write permissions must match allowlist"]),
        ("missing-write", ["required job write permissions must match allowlist"]),
        ("extra-write", ["required job write permissions must match allowlist"]),
    )
]
INTERNAL_USES_SHAPE_CASES = [
    ("quoted-local", "'./.github/actions/local-check'", []),
    ("numeric", "123", ["uses entries must be plain same-line scalar values"]),
    ("null", "null", ["uses entries must be plain same-line scalar values"]),
    ("mapping", "{}", ["uses entries must be plain same-line scalar values"]),
    ("list", "[]", ["uses entries must be plain same-line scalar values"]),
]


class DuplicateKeyError(ValueError):
    """Raised when a YAML mapping repeats a key."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict:
    loader.flatten_mapping(node)
    mapping: dict = {}
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
            raise DuplicateKeyError("duplicate YAML mapping key")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def classify_uses(value: str) -> Literal["local", "docker", "remote"]:
    """Classify a GitHub Actions ``uses`` reference without resolving it."""

    if value.startswith("./"):
        return "local"
    if value.startswith("docker://"):
        return "docker"
    return "remote"


def _diagnostic(path: Path, message: str, line_number: int | None = None) -> str:
    location = path.as_posix()
    if line_number is not None:
        location = f"{location}:{line_number}"
    return f"{location}: {message}"


def _collect_parsed_uses(value: object) -> list[object]:
    found: list[object] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "uses":
                found.append(child)
            else:
                found.extend(_collect_parsed_uses(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_collect_parsed_uses(child))
    return found


def _source_uses(lines: list[str]) -> list[tuple[int, object, bool]]:
    found: list[tuple[int, object, bool]] = []
    for line_number, line in enumerate(lines, start=1):
        match = USES_LINE.match(line)
        if not match:
            continue
        try:
            value = yaml.safe_load(match.group("value"))
        except yaml.YAMLError:
            continue
        found.append((line_number, value, VERSION_COMMENT.search(line) is not None))
    return found


def _validate_uses(path: Path, data: dict, lines: list[str]) -> list[str]:
    errors: list[str] = []
    parsed_uses = _collect_parsed_uses(data)
    source_uses = _source_uses(lines)
    source_values = [value for _, value, _ in source_uses]
    if (
        parsed_uses != source_values
        or not all(isinstance(value, str) for value in parsed_uses)
        or not all(isinstance(value, str) for value in source_values)
    ):
        errors.append(
            _diagnostic(path, "uses entries must be plain same-line scalar values")
        )
        return errors

    for line_number, value, has_version_comment in source_uses:
        assert isinstance(value, str)
        kind = classify_uses(value)
        if kind == "local":
            continue
        if kind == "docker":
            if not DOCKER_REF.fullmatch(value):
                errors.append(
                    _diagnostic(
                        path, "docker uses must use a sha256 digest", line_number
                    )
                )
            elif not has_version_comment:
                errors.append(
                    _diagnostic(
                        path,
                        "docker uses must retain a version comment",
                        line_number,
                    )
                )
            continue
        if not REMOTE_REF.fullmatch(value):
            errors.append(
                _diagnostic(
                    path,
                    "remote uses must use a forty-character commit SHA",
                    line_number,
                )
            )
        elif not has_version_comment:
            errors.append(
                _diagnostic(
                    path, "remote uses must retain a version comment", line_number
                )
            )
    return errors


def _validate_zizmor(path: Path, data: dict) -> list[str]:
    rules = data.get("rules")
    if not isinstance(rules, dict):
        return []
    unpinned = rules.get("unpinned-uses")
    if isinstance(unpinned, dict) and unpinned.get("disable") is True:
        return [_diagnostic(path, "unpinned-uses suppression is forbidden")]
    return []


def _validate_permissions(path: Path, data: dict) -> list[str]:
    errors: list[str] = []
    permissions = data.get("permissions")
    if permissions == "write-all":
        errors.append(_diagnostic(path, "write-all is forbidden"))
    elif isinstance(permissions, dict):
        if any(value == "write" for value in permissions.values()):
            errors.append(
                _diagnostic(path, "workflow default permissions must be read-only")
            )
        elif permissions.get("contents") != "read":
            errors.append(
                _diagnostic(
                    path, "workflow default permissions must set contents: read"
                )
            )
    else:
        errors.append(
            _diagnostic(path, "workflow default permissions must set contents: read")
        )

    jobs = data.get("jobs", {})
    if not isinstance(jobs, dict):
        jobs = {}

    required = [
        (job_id, writes)
        for (workflow, job_id), writes in ALLOWED_JOB_WRITES.items()
        if workflow == path.name
    ]
    for job_id, _ in required:
        job_path = Path(f"{path.as_posix()}[job={job_id}]")
        job = jobs.get(job_id)
        if not isinstance(job, dict):
            errors.append(
                _diagnostic(job_path, "required allowlisted job is missing")
            )
        elif not isinstance(job.get("permissions"), dict):
            errors.append(
                _diagnostic(job_path, "required job permissions must be a mapping")
            )

    for job_id, job in jobs.items():
        if not isinstance(job, dict) or "permissions" not in job:
            continue
        job_permissions = job["permissions"]
        job_path = Path(f"{path.as_posix()}[job={job_id}]")
        if job_permissions == "write-all":
            errors.append(_diagnostic(job_path, "write-all is forbidden"))
            continue
        if not isinstance(job_permissions, dict):
            continue
        writes = {
            str(key) for key, value in job_permissions.items() if value == "write"
        }
        allowed = ALLOWED_JOB_WRITES.get((path.name, str(job_id)))
        if allowed is not None:
            if allowed != writes:
                errors.append(
                    _diagnostic(
                        job_path,
                        "required job write permissions must match allowlist",
                    )
                )
        elif writes:
            errors.append(
                _diagnostic(job_path, "write permission is not allowlisted")
            )
    return errors


def validate_workflow(path: Path, data: dict, lines: list[str]) -> list[str]:
    """Validate one parsed workflow or the repository zizmor configuration."""

    if path.name in {"zizmor.yml", "zizmor.yaml"}:
        return _validate_zizmor(path, data)
    return _validate_permissions(path, data) + _validate_uses(path, data, lines)


def _load_yaml(path: Path) -> tuple[dict | None, list[str], str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None, [], "unable to read YAML"
    try:
        data = yaml.load(text, Loader=UniqueKeyLoader)
    except DuplicateKeyError:
        return None, text.splitlines(), "duplicate YAML mapping keys are forbidden"
    except yaml.YAMLError:
        return None, text.splitlines(), "invalid YAML"
    if not isinstance(data, dict):
        return None, text.splitlines(), "YAML root must be a mapping"
    return data, text.splitlines(), None


def _has_symlink_component(path: Path) -> bool:
    """Return whether an existing component in ``path`` is a symbolic link."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            if stat.S_ISLNK(current.lstat().st_mode):
                return True
        except OSError:
            return False
    return False


def _is_real_directory(path: Path) -> bool:
    try:
        return stat.S_ISDIR(path.lstat().st_mode) and not _has_symlink_component(path)
    except OSError:
        return False


def _is_real_file(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
        return stat.S_ISREG(mode) and not stat.S_ISLNK(mode)
    except OSError:
        return False


def validate_repository(root: Path) -> list[str]:
    """Validate tracked workflow-shaped files under a repository root."""

    errors: list[str] = []
    if not _is_real_directory(root):
        return [
            _diagnostic(
                root, "repository root must be an existing non-symlink directory"
            )
        ]

    github_dir = root / ".github"
    if not _is_real_directory(github_dir):
        return [
            _diagnostic(
                Path(".github"), ".github must be an existing non-symlink directory"
            )
        ]

    workflow_dir = github_dir / "workflows"
    if not _is_real_directory(workflow_dir):
        return [
            _diagnostic(
                Path(".github/workflows"),
                "workflow directory must be an existing non-symlink directory",
            )
        ]

    workflow_paths: list[tuple[Path, Path]] = []
    try:
        candidates = sorted(workflow_dir.iterdir(), key=lambda path: path.name)
    except OSError:
        return [
            _diagnostic(Path(".github/workflows"), "unable to list workflow directory")
        ]
    for absolute_path in candidates:
        if absolute_path.suffix not in {".yml", ".yaml"}:
            continue
        relative_path = Path(".github/workflows") / absolute_path.name
        if not _is_real_file(absolute_path):
            errors.append(
                _diagnostic(
                    relative_path, "workflow YAML must be a non-symlink regular file"
                )
            )
            continue
        workflow_paths.append((absolute_path, relative_path))

    if not workflow_paths:
        errors.append(
            _diagnostic(
                Path(".github/workflows"),
                "workflow directory must contain at least one regular workflow YAML file",
            )
        )

    for absolute_path, relative_path in workflow_paths:
        data, lines, load_error = _load_yaml(absolute_path)
        if load_error is not None:
            errors.append(_diagnostic(relative_path, load_error))
            continue
        assert data is not None
        errors.extend(validate_workflow(relative_path, data, lines))

    for filename in ("zizmor.yml", "zizmor.yaml"):
        absolute_path = github_dir / filename
        try:
            absolute_path.lstat()
        except FileNotFoundError:
            continue
        except OSError:
            errors.append(
                _diagnostic(Path(".github") / filename, "unable to inspect YAML")
            )
            continue
        relative_path = Path(".github") / filename
        if not _is_real_file(absolute_path):
            errors.append(
                _diagnostic(
                    relative_path,
                    "zizmor configuration must be a non-symlink regular file",
                )
            )
            continue
        data, lines, load_error = _load_yaml(absolute_path)
        if load_error is not None:
            errors.append(_diagnostic(relative_path, load_error))
            continue
        assert data is not None
        errors.extend(validate_workflow(relative_path, data, lines))
    return errors


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
        zizmor_path = root / ".github" / "zizmor.yml"
        zizmor_path.write_text(
            yaml.safe_dump(case["zizmor"], sort_keys=False), encoding="utf-8"
        )


def _message_only(diagnostic: str) -> str:
    return diagnostic.rsplit(": ", 1)[-1]


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


def _run_repository_boundary_case(temp_root: Path, case: dict) -> list[str]:
    setup = case["setup"]
    case_root = temp_root / "repository"
    external = temp_root / "external"
    external.mkdir()

    if setup == "missing-root":
        return validate_repository(case_root)
    if setup == "root-symlink":
        _write_valid_workflow(external / ".github" / "workflows" / "ci.yml")
        case_root.symlink_to(external, target_is_directory=True)
        result = subprocess.run(
            [sys.executable, os.fspath(Path(__file__).absolute()), "--root", os.fspath(case_root)],
            capture_output=True,
            text=True,
            check=False,
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
        return validate_repository(case_root)
    if setup == "github-symlink":
        _write_valid_workflow(external / "workflows" / "ci.yml")
        (case_root / ".github").symlink_to(external, target_is_directory=True)
        return validate_repository(case_root)

    github_dir = case_root / ".github"
    github_dir.mkdir()
    if setup == "missing-workflows":
        return validate_repository(case_root)
    if setup == "workflows-symlink":
        _write_valid_workflow(external / "ci.yml")
        (github_dir / "workflows").symlink_to(external, target_is_directory=True)
        return validate_repository(case_root)

    workflow_dir = github_dir / "workflows"
    workflow_dir.mkdir()
    if setup == "empty-workflows":
        return validate_repository(case_root)

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
    return validate_repository(case_root)


def _write_required_write_case(root: Path, case: dict) -> None:
    workflow = case["workflow"]
    job_id = case["job"]
    mutation = case["mutation"]
    required = ALLOWED_JOB_WRITES[(workflow, job_id)]
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


def run_self_test(script_root: Path) -> list[str]:
    fixture_path = script_root / "tests" / "fixtures" / "github-actions-security.json"
    try:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["self-test fixture is unreadable or invalid JSON"]
    expected_fixture = {
        "cases": EXPECTED_CASES,
        "repositoryBoundaryCases": EXPECTED_REPOSITORY_BOUNDARY_CASES,
        "requiredWriteCases": EXPECTED_REQUIRED_WRITE_CASES,
    }
    if fixture != expected_fixture:
        return [
            "self-test fixture differs from the exact eleven-case and supplemental contract"
        ]
    cases = fixture["cases"]

    failures: list[str] = []
    for case in cases:
        expected = case.get("expected")
        if not isinstance(expected, list) or not all(
            isinstance(message, str) for message in expected
        ):
            failures.append(f"{case.get('name')}: expected must be a string list")
            continue
        if "uses" in case:
            classify_uses(case["uses"])
        with tempfile.TemporaryDirectory(prefix="actions-security-") as temp_dir:
            case_root = Path(temp_dir)
            _write_self_test_case(case_root, case)
            actual = [_message_only(item) for item in validate_repository(case_root)]
        if actual != expected:
            failures.append(
                f"{case['name']}: expected {expected!r}, observed {actual!r}"
            )

    with tempfile.TemporaryDirectory(prefix="actions-security-duplicate-") as temp_dir:
        duplicate_root = Path(temp_dir)
        duplicate_path = duplicate_root / ".github" / "workflows" / "ci.yml"
        duplicate_path.parent.mkdir(parents=True)
        duplicate_path.write_text(
            "name: Duplicate\n"
            "permissions:\n"
            "  contents: read\n"
            "  contents: write\n"
            "jobs: {}\n",
            encoding="utf-8",
        )
        duplicate_errors = [
            _message_only(item) for item in validate_repository(duplicate_root)
        ]
    if duplicate_errors != ["duplicate YAML mapping keys are forbidden"]:
        failures.append(
            "duplicate-key: expected duplicate YAML rejection, observed "
            f"{duplicate_errors!r}"
        )

    for case in fixture["repositoryBoundaryCases"]:
        with tempfile.TemporaryDirectory(
            prefix="actions-security-boundary-"
        ) as temp_dir:
            actual = [
                _message_only(item)
                for item in _run_repository_boundary_case(Path(temp_dir), case)
            ]
        if actual != case["expected"]:
            failures.append(
                f"{case['name']}: expected {case['expected']!r}, observed {actual!r}"
            )

    for case in fixture["requiredWriteCases"]:
        with tempfile.TemporaryDirectory(
            prefix="actions-security-permissions-"
        ) as temp_dir:
            case_root = Path(temp_dir)
            _write_required_write_case(case_root, case)
            actual = [
                _message_only(item) for item in validate_repository(case_root)
            ]
        if actual != case["expected"]:
            failures.append(
                f"{case['name']}: expected {case['expected']!r}, observed {actual!r}"
            )

    for name, raw_uses, expected in INTERNAL_USES_SHAPE_CASES:
        with tempfile.TemporaryDirectory(
            prefix="actions-security-uses-shape-"
        ) as temp_dir:
            case_root = Path(temp_dir)
            _write_uses_shape_case(case_root, raw_uses)
            actual = [
                _message_only(item) for item in validate_repository(case_root)
            ]
        if actual != expected:
            failures.append(
                f"uses-shape-{name}: expected {expected!r}, observed {actual!r}"
            )
    return failures


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--root", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.self_test:
        root = Path(__file__).resolve().parent.parent
        errors = run_self_test(root)
        if errors:
            for error in errors:
                print(f"FAIL: {error}")
            return 1
        print("PASS: GitHub Actions security fixture")
        return 0

    errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: GitHub Actions security")
    return 0


if __name__ == "__main__":
    sys.exit(main())
