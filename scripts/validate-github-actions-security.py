#!/usr/bin/env python3
"""Validate GitHub Actions identity, permissions, and artifact retention."""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
from pathlib import Path
from typing import Literal

import yaml


REMOTE_REF = re.compile(r"^[^\s/@]+/[^\s@]+(?:/[^\s@]+)*@([0-9a-f]{40})$")
DOCKER_REF = re.compile(r"^docker://[^\s@]+@sha256:([0-9a-f]{64})$")
VERSION_COMMENT = re.compile(r"#\s*(v?[0-9]+(?:\.[0-9]+){0,2})\s*$")
USES_LINE = re.compile(r"^\s*(?:-\s*)?uses\s*:\s*(?P<value>.+?)\s*$")
ARTIFACT_RETENTION_DAYS = 7
UPLOAD_ARTIFACT_PREFIX = "actions/upload-artifact@"
ALLOWED_JOB_WRITES = {
    ("greetings.yml", "greeting"): {"issues", "pull-requests"},
    ("labeler.yml", "label"): {"pull-requests"},
    ("stale.yml", "stale"): {"issues", "pull-requests"},
}


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
            errors.append(_diagnostic(job_path, "required allowlisted job is missing"))
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
            errors.append(_diagnostic(job_path, "write permission is not allowlisted"))
    return errors


def _validate_artifact_retention(path: Path, data: dict) -> list[str]:
    errors: list[str] = []
    jobs = data.get("jobs", {})
    if not isinstance(jobs, dict):
        return [_diagnostic(path, "workflow jobs must be a mapping")]

    for job_id, job in jobs.items():
        job_path = Path(f"{path.as_posix()}[job={job_id}]")
        if not isinstance(job, dict):
            errors.append(_diagnostic(job_path, "workflow job must be a mapping"))
            continue
        if "steps" not in job:
            continue
        steps = job["steps"]
        if not isinstance(steps, list):
            errors.append(_diagnostic(job_path, "job steps must be a list"))
            continue
        for step_index, step in enumerate(steps, start=1):
            step_path = Path(f"{job_path.as_posix()}[step={step_index}]")
            if not isinstance(step, dict):
                errors.append(_diagnostic(step_path, "job step must be a mapping"))
                continue
            uses = step.get("uses")
            if not isinstance(uses, str) or not uses.casefold().startswith(
                UPLOAD_ARTIFACT_PREFIX
            ):
                continue
            options = step.get("with")
            retention = (
                options.get("retention-days") if isinstance(options, dict) else None
            )
            if (
                isinstance(retention, bool)
                or not isinstance(retention, int)
                or retention != ARTIFACT_RETENTION_DAYS
            ):
                errors.append(
                    _diagnostic(
                        step_path,
                        "upload-artifact retention-days must equal 7",
                    )
                )
    return errors


def validate_workflow(path: Path, data: dict, lines: list[str]) -> list[str]:
    """Validate one parsed workflow or the repository zizmor configuration."""

    if path.name in {"zizmor.yml", "zizmor.yaml"}:
        return _validate_zizmor(path, data)
    return (
        _validate_permissions(path, data)
        + _validate_uses(path, data, lines)
        + _validate_artifact_retention(path, data)
    )


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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: GitHub Actions security")
    return 0


if __name__ == "__main__":
    sys.exit(main())
