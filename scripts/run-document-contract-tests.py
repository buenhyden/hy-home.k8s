#!/usr/bin/env python3
"""Run the document lifecycle contract regressions as one gate.

The completed-state migration, cumulative history, and Task execution and
acceptance regressions decide whether a document reader, a Stage 99 contract or
a template change is admissible, so they run in the quick and staged lanes
instead of waiting for a blanket unit run that no lane executes. This gate is
one script because the affected-surface contract identifies a gate by the exact
script it runs.
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path


MODULES = (
    "tests.test_completed_state_migration",
    "tests.test_document_lifecycle_cumulative_history",
    "tests.test_task_execution_contract",
    "tests.test_task_acceptance_contract",
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
        print(f"[FAIL] document contract regressions are unavailable: {error}")
        return 1
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    if not result.wasSuccessful():
        print(
            "[FAIL] document contract regressions failed: "
            f"tests={result.testsRun} failures={len(result.failures)} "
            f"errors={len(result.errors)}"
        )
        return 1
    print(
        "[PASS] document contract regressions passed: "
        f"modules={len(MODULES)} tests={result.testsRun}"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - module entry guard
    raise SystemExit(main())
