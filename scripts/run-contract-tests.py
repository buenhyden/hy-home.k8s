#!/usr/bin/env python3
"""Run one named suite of contract regressions as a purpose gate.

Each registered gate runs one suite, so a test module runs when its product or
its own file changes instead of waiting for a blanket unit run that no lane
executes. A suite is one file under `validation/contract-suites/` plus one
registry validator; the affected-surface tests require every test module to
belong to exactly one gate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unittest
from pathlib import Path


SUITE_DIR = Path(__file__).resolve().parent / "validation/contract-suites"
SUITE_LIMIT = 64 * 1024
MODULE = re.compile(r"tests\.test_[a-z0-9_]+\Z")


def load_suites(directory: Path = SUITE_DIR) -> dict[str, tuple[str, ...]]:
    """Read each suite's module list from its own registration file.

    Registration data lives outside this engine so that adding a module to one
    suite selects that suite and the registration checks, not every suite.
    """
    suites: dict[str, tuple[str, ...]] = {}
    for path in sorted(directory.glob("*.json")):
        if path.is_symlink() or path.stat().st_size > SUITE_LIMIT:
            raise ValueError(f"{path.name}: suite registration is not a bounded file")
        modules = json.loads(path.read_text(encoding="utf-8"))
        if (
            not isinstance(modules, list)
            or not modules
            or len(set(modules)) != len(modules)
            or not all(isinstance(m, str) and MODULE.fullmatch(m) for m in modules)
        ):
            raise ValueError(
                f"{path.name}: suite must list unique tests.test_* modules"
            )
        suites[path.stem] = tuple(modules)
    if not suites:
        raise ValueError("no contract suite is registered")
    return suites


SUITES = load_suites()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--suite", required=True, choices=sorted(SUITES))
    arguments = parser.parse_args()

    root = arguments.root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    modules = SUITES[arguments.suite]
    label = f"{arguments.suite} contract regressions"
    try:
        suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    except Exception as error:  # noqa: BLE001 - any load failure is a gate failure
        print(f"[FAIL] {label} are unavailable: {error}")
        return 1
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    if not result.wasSuccessful():
        print(
            f"[FAIL] {label} failed: "
            f"tests={result.testsRun} failures={len(result.failures)} "
            f"errors={len(result.errors)}"
        )
        return 1
    print(f"[PASS] {label} passed: modules={len(modules)} tests={result.testsRun}")
    return 0


if __name__ == "__main__":  # pragma: no cover - module entry guard
    raise SystemExit(main())
