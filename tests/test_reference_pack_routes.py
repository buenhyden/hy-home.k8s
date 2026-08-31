#!/usr/bin/env python3
"""Focused Stage 90 semantic pack route tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from document_contracts import (  # noqa: E402
    DocumentContractError,
    classify_path,
    load_registry,
)


class ReferencePackRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)

    def test_each_category_selects_its_matching_pack_template(self) -> None:
        for category, singular in (
            ("audits", "audit"),
            ("data", "data"),
            ("research", "research"),
        ):
            with self.subTest(category=category):
                profile = classify_path(
                    self.registry,
                    PurePosixPath(
                        f"docs/90.references/{category}/0001-example/README.md"
                    ),
                )
                self.assertEqual(profile.profile_id, f"readme/{singular}-pack")
                self.assertEqual(
                    profile.template,
                    PurePosixPath(
                        f"docs/99.templates/templates/references/{singular}-pack.template.md"
                    ),
                )

    def test_pack_members_use_the_reference_profile(self) -> None:
        for category in ("audits", "data", "research"):
            with self.subTest(category=category):
                profile = classify_path(
                    self.registry,
                    PurePosixPath(
                        f"docs/90.references/{category}/0001-example/report.md"
                    ),
                )
                self.assertEqual(profile.profile_id, "content/reference")

    def test_date_based_and_loose_reference_paths_are_uncovered(self) -> None:
        for path in (
            "docs/90.references/research/2026-08-31-example/README.md",
            "docs/90.references/data/example.md",
        ):
            with self.subTest(path=path), self.assertRaises(
                DocumentContractError
            ) as raised:
                classify_path(self.registry, PurePosixPath(path))
            self.assertEqual(
                {item.rule_id for item in raised.exception.diagnostics},
                {"REGISTRY_ROUTE_UNCOVERED"},
            )


if __name__ == "__main__":
    unittest.main()
