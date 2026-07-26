#!/usr/bin/env python3
"""CLI for the closed Reference Information Architecture contract."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from reference_information_architecture import (
    ContractError,
    DEFAULT_CONTRACT_PATH,
    load_contract,
    load_contract_at_commit,
    normalize_contract_path,
    parse_git_sha1,
    run_self_test,
    validate_reference_architecture,
)


def _self_test() -> int:
    try:
        run_self_test()
    except (AssertionError, ContractError, OSError):
        print("RIA-CONTRACT self-test: isolated input failure", file=sys.stderr)
        return 2
    print("Reference information architecture self-test: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--self-test", action="store_true")
    evidence = parser.add_mutually_exclusive_group()
    evidence.add_argument("--staged", action="store_true")
    evidence.add_argument("--commit")
    parser.add_argument("--require-settled-baselines", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.self_test:
        if (
            arguments.contract is not None
            or arguments.root != Path(".")
            or arguments.staged
            or arguments.commit is not None
            or arguments.require_settled_baselines
        ):
            parser.error("--self-test does not accept validation mode arguments")
        return _self_test()
    root = arguments.root.absolute()
    try:
        contract_path = normalize_contract_path(
            root,
            arguments.contract or DEFAULT_CONTRACT_PATH,
        )
        if arguments.commit is None:
            contract = load_contract(root, contract_path)
        else:
            parse_git_sha1(arguments.commit, field="--commit")
            contract = load_contract_at_commit(
                root,
                arguments.commit,
                contract_path,
            )
        findings = validate_reference_architecture(
            root,
            contract,
            contract_path=contract_path,
            staged=arguments.staged,
            commit=arguments.commit,
            require_settled_baselines=arguments.require_settled_baselines,
        )
    except ContractError as error:
        finding = error.finding
        print(f"{finding.rule_id} {finding.path}: {finding.message}", file=sys.stderr)
        return 2
    for finding in findings:
        print(f"{finding.rule_id} {finding.path}: {finding.message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
