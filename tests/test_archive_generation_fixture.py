#!/usr/bin/env python3
"""The derived frozen-generation registry equals the one merged before ADR-0038."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from unittest import mock

from tests import archive_generation_fixture as fixture

from tests.archive_generation_fixture import (
    LEGACY_ARCHIVE_GENERATION_COMMIT,
    REGISTRY_PATH,
    ROOT,
    legacy_registry_bytes,
)


class ArchiveGenerationFixtureTest(unittest.TestCase):
    def test_schema_asset_matches_the_frozen_registry_generation(self) -> None:
        relative = "docs/99.templates/contracts/document-profile.schema.json"
        expected = subprocess.check_output(
            [
                "git",
                "--no-replace-objects",
                "-C",
                str(ROOT),
                "cat-file",
                "blob",
                f"{LEGACY_ARCHIVE_GENERATION_COMMIT}:{relative}",
            ],
            stderr=subprocess.DEVNULL,
        )
        self.assertEqual(fixture.legacy_asset_bytes(relative), expected)

    def test_template_asset_matches_the_frozen_registry_generation(self) -> None:
        relative = next(
            profile["template_source"]
            for profile in fixture.legacy_registry_payload()["profiles"]
            if profile["template_source"] is not None
        )
        expected = subprocess.check_output(
            [
                "git",
                "--no-replace-objects",
                "-C",
                str(ROOT),
                "cat-file",
                "blob",
                f"{LEGACY_ARCHIVE_GENERATION_COMMIT}:{relative}",
            ],
            stderr=subprocess.DEVNULL,
        )
        self.assertEqual(fixture.legacy_asset_bytes(relative), expected)

    def test_missing_asset_fails_without_current_file_fallback(self) -> None:
        missing = subprocess.CalledProcessError(128, ["git", "cat-file"])
        with (
            mock.patch.object(
                fixture.subprocess, "check_output", side_effect=missing
            ) as lookup,
            mock.patch.object(
                Path, "read_bytes", side_effect=AssertionError("current asset lookup")
            ),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            fixture.legacy_asset_bytes(
                "docs/99.templates/contracts/document-profile.schema.json"
            )
        lookup.assert_called_once()

    def test_asset_reader_rejects_paths_outside_the_generation(self) -> None:
        for relative in ("../registry.json", "/tmp/registry.json", "secrets/file"):
            with (
                self.subTest(relative=relative),
                mock.patch.object(fixture.subprocess, "check_output") as lookup,
                self.assertRaises(ValueError),
            ):
                fixture.legacy_asset_bytes(relative)
            lookup.assert_not_called()

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
