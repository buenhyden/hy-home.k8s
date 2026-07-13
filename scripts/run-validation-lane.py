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
from pathlib import Path
from typing import Any, Sequence


LOCAL_LANES = ("affected", "all-files")


def load_contract_module():
    module_path = Path(__file__).with_name("validate-affected-surfaces.py")
    spec = importlib.util.spec_from_file_location("affected_surface_contract", module_path)
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
    for identifier in selected["validators"]:
        validator = validators[identifier]
        argv = list(validator["argv"])
        tool = argv[0]
        evidence = validator["evidenceLane"]
        if evidence == "remote/live":
            print(
                result_line(
                    "DEFER",
                    identifier,
                    command=argv,
                    tool=tool,
                    scope=scope,
                    limitation="remote/live commands are never executed by the local runner",
                    evidence=evidence,
                )
            )
            continue

        if shutil.which(tool) is None:
            fallback = validator["fallback"]
            if validator["optional"]:
                print(
                    result_line(
                        "SKIP",
                        identifier,
                        command=argv,
                        tool=tool,
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
                    tool=tool,
                    scope=scope,
                    limitation=f"required tool unavailable; fallback: {fallback['reason']}",
                    evidence=evidence,
                )
            )
            failed = True
            continue

        environment = os.environ.copy()
        environment["HY_HOME_K8S_SKIP_HOOK_SIMULATION"] = "1"
        completed = subprocess.run(
            argv,
            cwd=root,
            text=True,
            capture_output=True,
            shell=False,
            env=environment,
        )
        status = "PASS" if completed.returncode == 0 else "FAIL"
        print(
            result_line(
                status,
                identifier,
                command=argv,
                tool=tool,
                scope=scope,
                limitation=observation(completed),
                evidence=evidence,
            )
        )
        failed = failed or completed.returncode != 0
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
