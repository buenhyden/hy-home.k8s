#!/usr/bin/env python3
"""Select validators and CI jobs from NUL-delimited repository paths."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


def load_contract_module():
    module_path = Path(__file__).with_name("validate-affected-surfaces.py")
    spec = importlib.util.spec_from_file_location("affected_surface_contract", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load affected-surface contract from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--lane", choices=("affected", "staged", "all-files", "ci"), required=True)
    parser.add_argument("--paths-file", type=Path, required=True)
    parser.add_argument("--delimiter", choices=("nul",), required=True)
    parser.add_argument("--format", choices=("json", "github-output"), required=True)
    args = parser.parse_args()
    contract_module = load_contract_module()
    root = args.root.resolve()
    try:
        contract = contract_module.validate_contract(root)
        paths = contract_module.read_nul_paths(args.paths_file)
        result = contract_module.select_paths(
            contract, paths, args.lane, root, collect_unmatched=True
        )
        if args.format == "json":
            print(contract_module.json_output(result))
        else:
            print(contract_module.github_output(contract, result))
        if result["unmatchedPaths"]:
            print(
                "[FAIL] SURFACE-PATH-UNMATCHED: "
                + ", ".join(result["unmatchedPaths"]),
                file=sys.stderr,
            )
            return 1
        return 0
    except contract_module.ContractError as exc:
        print(f"[FAIL] {exc.code}: {exc.detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
