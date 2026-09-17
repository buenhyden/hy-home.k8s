#!/usr/bin/env python3
"""Run the Stage 98 archive contract regressions as one fast gate.

The registry, citation table, unit retention, and catalog re-verification
regressions decide whether a Stage 98 change is admissible, so they run in the
quick and staged lanes rather than waiting for the full unit lane. This gate is
one script because the affected-surface contract identifies a gate by the exact
script it runs.
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path


MODULES = (
    "tests.test_archive_registry_contract",
    "tests.test_archive_citation_decision",
    "tests.test_archive_dispositions",
    "tests.test_archive_disposition_lifecycle",
    "tests.test_archive_catalog_reverification",
    "tests.test_archive_reappraisal",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()

    root = arguments.root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    try:
        suite = unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    except Exception as error:  # noqa: BLE001 - any load failure is a gate failure
        print(f"[FAIL] archive contract regressions are unavailable: {error}")
        return 1
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    if not result.wasSuccessful():
        print(
            "[FAIL] archive contract regressions failed: "
            f"tests={result.testsRun} failures={len(result.failures)} "
            f"errors={len(result.errors)}"
        )
        return 1
    print(
        "[PASS] archive contract regressions passed: "
        f"modules={len(MODULES)} tests={result.testsRun}"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - module entry guard
    raise SystemExit(main())
