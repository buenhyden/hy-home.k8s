#!/usr/bin/env python3
"""CLI for the closed RIA-001 contract."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from reference_information_architecture import ContractError, DEFAULT_CONTRACT_PATH, load_contract, parse_git_sha1, validate_reference_architecture


def _self_test() -> int:
    accepted = "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47"
    rejected = ("8fb9821497aaa93d9ed5fc1a69b60c628b047b47", "git-sha1:", "git-sha1:git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47", "git-sha1:8FB9821497AAA93D9ED5FC1A69B60C628B047B47", "git-sha1:zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz", "git-sha1:" + "a" * 64, accepted + " trailing", " " + accepted, accepted + " ")
    if parse_git_sha1(accepted) != accepted.removeprefix("git-sha1:"):
        return 2
    for value in rejected:
        try:
            parse_git_sha1(value)
        except ContractError as error:
            if error.finding.rule_id == "RIA-SNAPSHOT":
                continue
        return 2
    print("Reference information architecture self-test: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.self_test:
        if arguments.contract is not None or arguments.root != Path("."):
            parser.error("--self-test does not accept --root or --contract")
        return _self_test()
    root = arguments.root.absolute()
    try:
        contract = load_contract(root, arguments.contract or root / DEFAULT_CONTRACT_PATH)
        findings = validate_reference_architecture(root, contract)
    except ContractError as error:
        finding = error.finding
        print(f"{finding.rule_id} {finding.path}: {finding.message}", file=sys.stderr)
        return 2
    for finding in findings:
        print(f"{finding.rule_id} {finding.path}: {finding.message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
