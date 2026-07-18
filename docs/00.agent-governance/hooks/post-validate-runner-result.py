#!/usr/bin/python3
"""Validate exact post-validate runner result cardinality without log disclosure."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def has_one_required_pass(log_text: str, identifier: str) -> bool:
    """Require exactly one PASS and no competing status for one validator."""

    status_prefixes = tuple(
        f"[{status}] {identifier} " for status in ("PASS", "SKIP", "FAIL", "DEFER")
    )
    matching = [
        line for line in log_text.splitlines() if line.startswith(status_prefixes)
    ]
    return len(matching) == 1 and matching[0].startswith(f"[PASS] {identifier} ")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--identifier", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        log_text = args.log.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 1
    return 0 if has_one_required_pass(log_text, args.identifier) else 1


if __name__ == "__main__":
    raise SystemExit(main())
