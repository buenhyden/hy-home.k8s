#!/usr/bin/env python3
"""Compatibility CLI for registry-derived role admission validation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import agent_registry_compat as compat


MODE = "admission"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate role admission through the terminal agent registry."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        counts = (
            compat.run_self_test(args.root, MODE)
            if args.self_test
            else compat.validate(args.root, MODE)
        )
        suffix = " self-test" if args.self_test else ""
        print(f"[PASS] agent roster admission{suffix}: {compat.format_counts(counts)}")
        return 0
    except compat.CompatibilityError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code
    except Exception as exc:
        code = getattr(exc, "code", "AGENT-COMPAT-VALIDATION")
        detail = getattr(exc, "detail", "invalid input")
        exit_code = getattr(exc, "exit_code", 1)
        print(f"ERR {code} {detail}", file=sys.stderr)
        return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
