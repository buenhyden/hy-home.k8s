#!/usr/bin/env python3
"""Validate current Archive integrity, provenance, index and secret safety."""

from __future__ import annotations

import argparse
from pathlib import Path
from collections.abc import Sequence

from archive_validation import validate_repository_archive


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    report = validate_repository_archive(args.root, {}, scan_secrets=True)
    if not report.valid:
        for diagnostic in report.diagnostics:
            print(f"FAIL {diagnostic.code} path={diagnostic.path}")
        return 1
    print(
        "PASS archive integrity "
        f"records={report.record_count} "
        f"historical_links={report.historical_link_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
