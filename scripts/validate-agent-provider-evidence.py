#!/usr/bin/env python3
"""Run the two focused provider-evidence validators as one routed gate."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


FOCUSED_VALIDATORS = (
    "validate-agent-provider-config.py",
    "validate-agent-provider-canaries.py",
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run provider configuration and canary evidence validation."
    )
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run both focused validators' synthetic self-tests.",
    )
    return parser.parse_args(argv)


def run(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root
    scripts_dir = Path(__file__).resolve().parent

    for script_name in FOCUSED_VALIDATORS:
        command = [
            sys.executable,
            str(scripts_dir / script_name),
            "--root",
            str(root),
        ]
        if args.self_test:
            command.append("--self-test")
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            return completed.returncode

    mode = "self-test" if args.self_test else "production"
    print(
        "[PASS] agent provider evidence aggregate passed: "
        f"mode={mode} validators={len(FOCUSED_VALIDATORS)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(run())
