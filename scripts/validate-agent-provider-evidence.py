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
        try:
            completed = subprocess.run(command, check=False, timeout=120)
        except subprocess.TimeoutExpired:
            print(
                "[FAIL] provider evidence validator timed out",
                file=sys.stderr,
            )
            return 124
        except OSError:
            print(
                "[FAIL] provider evidence validator could not start",
                file=sys.stderr,
            )
            return 2
        if completed.returncode != 0:
            return completed.returncode

    print(
        "[PASS] agent provider evidence aggregate passed: "
        f"validators={len(FOCUSED_VALIDATORS)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(run())
