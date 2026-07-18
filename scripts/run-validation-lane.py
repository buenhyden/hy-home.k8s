#!/usr/bin/env python3
"""Run contract-approved repository-static validators for a NUL path set."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Sequence


LOCAL_LANES = ("affected", "all-files")
TRUSTED_SEARCH_DIRECTORIES = (
    "/usr/local/sbin",
    "/usr/local/bin",
    "/usr/sbin",
    "/usr/bin",
    "/sbin",
    "/bin",
)
QUALITY_SUCCESS_MARKER = "[PASS] repository quality gates passed"


def load_contract_module():
    module_path = Path(__file__).with_name("validate-affected-surfaces.py")
    spec = importlib.util.spec_from_file_location(
        "affected_surface_contract", module_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load affected-surface contract from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def encoded(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def result_line(
    status: str,
    identifier: str,
    *,
    command: Sequence[str],
    tool: str,
    scope: str,
    limitation: str,
    evidence: str,
) -> str:
    return (
        f"[{status}] {identifier} command={encoded(list(command))} "
        f"tool={encoded(tool)} scope={encoded(scope)} "
        f"limitation={encoded(limitation)} evidence={encoded(evidence)}"
    )


def bounded_metadata(label: str, value: str) -> str:
    payload = value.encode("utf-8", errors="replace")
    return (
        f"{label}_bytes={len(payload)};"
        f"{label}_sha256={hashlib.sha256(payload).hexdigest()}"
    )


def observation(completed: subprocess.CompletedProcess[str]) -> str:
    status = "completed" if completed.returncode == 0 else "failed"
    return ";".join(
        (
            f"status={status}",
            f"rc={completed.returncode}",
            bounded_metadata("stdout", completed.stdout),
            bounded_metadata("stderr", completed.stderr),
        )
    )


def trusted_search_path() -> str:
    """Build one fixed absolute PATH without caller-controlled search entries."""

    directories: list[str] = []
    for raw_path in TRUSTED_SEARCH_DIRECTORIES:
        try:
            resolved = Path(raw_path).resolve(strict=True)
        except OSError:
            continue
        value = resolved.as_posix()
        if resolved.is_dir() and value not in directories:
            directories.append(value)
    return os.pathsep.join(directories)


def closed_subprocess_environment() -> dict[str, str]:
    """Return the complete validator environment; ambient startup state is absent."""

    return {
        "GIT_TERMINAL_PROMPT": "0",
        "HOME": "/nonexistent",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_COLOR": "1",
        "PATH": trusted_search_path(),
        "PYTHONNOUSERSITE": "1",
        "TZ": "UTC",
    }


def exact_success_marker_count(stdout: str, marker: str) -> int:
    """Count exact complete success-marker lines without exposing child output."""

    return sum(line == marker for line in stdout.splitlines())


def validator_argv(
    root: Path,
    lane: str,
    paths: Sequence[str],
    validator: dict[str, Any],
    contract: dict[str, Any],
    contract_module: Any,
) -> list[str]:
    argv = list(validator["argv"])
    if lane != "affected" or validator.get("pathInput") != "include-existing-markdown":
        return argv

    include_candidates = list(paths)
    archive_form = "docs/99.templates/templates/common/archive-record.template.md"
    if (root / archive_form).is_file() and archive_form not in include_candidates:
        include_candidates.append(archive_form)

    for raw_path in include_candidates:
        if not raw_path.endswith(".md"):
            continue
        surface = contract_module.classify_path(contract, raw_path)
        if validator["id"] not in surface["validators"]:
            continue
        target = root.joinpath(*PurePosixPath(raw_path).parts)
        if target.exists() or target.is_symlink():
            argv.extend(("--include-path", raw_path))
    return argv


def run_selected(
    root: Path,
    lane: str,
    paths: Sequence[str],
    contract: dict[str, Any],
    contract_module: Any,
) -> int:
    scope = f"{lane}:paths={len(paths)}"
    if not paths:
        print(
            result_line(
                "SKIP",
                "validation-lane",
                command=(),
                tool="none",
                scope=scope,
                limitation="no paths supplied",
                evidence="repo-static",
            )
        )
        return 0

    selected = contract_module.select_paths(contract, paths, lane, root)
    validators = {row["id"]: row for row in contract["validators"]}
    if not selected["validators"]:
        print(
            result_line(
                "SKIP",
                "validation-lane",
                command=(),
                tool="none",
                scope=scope,
                limitation="matched surfaces select no local validators",
                evidence="repo-static",
            )
        )
        return 0

    failed = False
    subprocess_environment = closed_subprocess_environment()
    for identifier in selected["validators"]:
        validator = validators[identifier]
        argv = validator_argv(root, lane, paths, validator, contract, contract_module)
        tool_token = argv[0]
        evidence = validator["evidenceLane"]
        if evidence == "remote/live":
            print(
                result_line(
                    "DEFER",
                    identifier,
                    command=argv,
                    tool=tool_token,
                    scope=scope,
                    limitation="remote/live commands are never executed by the local runner",
                    evidence=evidence,
                )
            )
            continue

        resolved_tool = shutil.which(tool_token, path=subprocess_environment["PATH"])
        if resolved_tool is None:
            fallback = validator["fallback"]
            if validator["optional"]:
                print(
                    result_line(
                        "SKIP",
                        identifier,
                        command=argv,
                        tool=tool_token,
                        scope=scope,
                        limitation="optional tool unavailable",
                        evidence=evidence,
                    )
                )
                print(
                    result_line(
                        fallback["status"],
                        f"{identifier}-fallback",
                        command=(),
                        tool="none",
                        scope=scope,
                        limitation=fallback["reason"],
                        evidence=evidence,
                    )
                )
                continue
            print(
                result_line(
                    "FAIL",
                    identifier,
                    command=argv,
                    tool=tool_token,
                    scope=scope,
                    limitation=f"required tool unavailable; fallback: {fallback['reason']}",
                    evidence=evidence,
                )
            )
            failed = True
            continue

        tool = Path(resolved_tool).resolve(strict=True).as_posix()
        argv[0] = tool

        completed = subprocess.run(
            argv,
            cwd=root,
            text=True,
            capture_output=True,
            shell=False,
            env=subprocess_environment,
        )
        marker = QUALITY_SUCCESS_MARKER if identifier == "repository-quality" else None
        marker_count = (
            exact_success_marker_count(completed.stdout, marker)
            if marker is not None
            else None
        )
        passed = completed.returncode == 0 and (
            marker_count == 1 if marker is not None else True
        )
        status = "PASS" if passed else "FAIL"
        limitation = observation(completed)
        if marker_count is not None:
            limitation += f";success_marker_count={marker_count}"
        print(
            result_line(
                status,
                identifier,
                command=argv,
                tool=tool,
                scope=scope,
                limitation=limitation,
                evidence=evidence,
            )
        )
        failed = failed or not passed
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--lane", choices=LOCAL_LANES, required=True)
    parser.add_argument("--paths-file", type=Path, required=True)
    parser.add_argument("--delimiter", choices=("nul",), required=True)
    args = parser.parse_args()

    contract_module = load_contract_module()
    root = args.root.resolve()
    scope = f"{args.lane}:paths=unknown"
    try:
        contract = contract_module.validate_contract(root)
        paths = contract_module.read_nul_paths(args.paths_file)
        return run_selected(root, args.lane, paths, contract, contract_module)
    except contract_module.ContractError as exc:
        detail_metadata = bounded_metadata("detail", exc.detail)
        print(
            result_line(
                "FAIL",
                "validation-lane",
                command=(),
                tool="none",
                scope=scope,
                limitation=f"contract_error={exc.code};{detail_metadata}",
                evidence="repo-static",
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
