#!/usr/bin/env python3
"""The derived frozen-generation registry equals the one merged before ADR-0038."""

from __future__ import annotations

import subprocess
import unittest

from tests.archive_generation_fixture import (
    LEGACY_ARCHIVE_GENERATION_COMMIT,
    REGISTRY_PATH,
    ROOT,
    legacy_registry_bytes,
)


class ArchiveGenerationFixtureTest(unittest.TestCase):
    def test_derivation_equals_the_merged_frozen_generation_registry(self) -> None:
        completed = subprocess.run(
            [
                "git",
                "--no-replace-objects",
                "-C",
                str(ROOT),
                "cat-file",
                "blob",
                f"{LEGACY_ARCHIVE_GENERATION_COMMIT}:{REGISTRY_PATH}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if completed.returncode != 0:
            self.skipTest(
                "frozen generation commit is absent from this clone's history; "
                "hosted CI fetches full history and runs this proof"
            )
        self.assertEqual(legacy_registry_bytes(), completed.stdout)


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
