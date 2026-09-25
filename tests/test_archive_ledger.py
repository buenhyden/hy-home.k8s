#!/usr/bin/env python3
"""SPEC-0092: the archive tables live in one ledger the registry names."""

from __future__ import annotations

import copy
import dataclasses
import json
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import archive_dispositions as dispositions  # noqa: E402
import archive_validation as validation  # noqa: E402
import document_contracts as contracts  # noqa: E402

REGISTRY = contracts.load_registry(ROOT)
INDEX = PurePosixPath("docs/98.archive/README.md")
LEDGER = PurePosixPath("docs/98.archive/ledger.md")
RAW = json.loads((ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8"))


def with_ledger(ledger: PurePosixPath = LEDGER):
    citation = dataclasses.replace(REGISTRY.archive_citation, ledger=ledger)
    assessment = dataclasses.replace(REGISTRY.archive_assessment, index=ledger)
    return dataclasses.replace(
        REGISTRY, archive_citation=citation, archive_assessment=assessment
    )


def residue(registry, text: str) -> list[str]:
    return [code for code, _ in validation.ledger_residue_diagnostics(registry, text)]


class ArchiveLedgerTests(unittest.TestCase):
    def test_registry_names_the_ledger_beside_the_assessment_index(self):
        self.assertEqual(
            REGISTRY.archive_citation.ledger, REGISTRY.archive_assessment.index
        )

    def test_ledger_path_comes_from_the_registry_or_the_index(self):
        self.assertEqual(dispositions.archive_ledger_path(with_ledger()), LEDGER)
        self.assertEqual(dispositions.archive_ledger_path(None), INDEX)

    def test_registry_rejects_a_ledger_apart_from_the_assessment_index(self):
        self.assertEqual(contracts._archive_ledger_registry_diagnostics(RAW), [])
        raw = copy.deepcopy(RAW)
        raw["archive_citation"]["ledger"] = "docs/98.archive/other.md"
        self.assertEqual(
            [d.rule_id for d in contracts._archive_ledger_registry_diagnostics(raw)],
            ["REGISTRY_ARCHIVE_LEDGER"],
        )

    def test_tables_left_in_the_readme_are_residue(self):
        heading = f"### {REGISTRY.archive_assessment.heading}"
        marker = "<!-- archive-manifest:v1 records=1 historical-links=0 -->"
        for text in (
            marker,
            validation._INDEX_HEADER,
            dispositions.CATALOG_HEADER,
            heading,
        ):
            self.assertEqual(
                residue(with_ledger(), f"# A\n\n{text}\n"), ["ARCHIVE-LEDGER-RESIDUE"]
            )
            self.assertEqual(residue(with_ledger(INDEX), f"# A\n\n{text}\n"), [])
        self.assertEqual(
            residue(with_ledger(), "# A\n\n## Document Index\n\n- [x/](./x/)\n"), []
        )

    def test_ledger_is_cited_as_the_index(self):
        self.assertEqual(
            dispositions.archive_target_kind(with_ledger(), LEDGER), ("index", None)
        )

    def test_absent_ledger_fails_on_its_own_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / INDEX).parent.mkdir(parents=True)
            (root / INDEX).write_text("# Archive\n", encoding="utf-8")
            _, found = validation._read_archive_ledger(root, with_ledger())
            self.assertEqual(
                [(code, path) for code, path in found],
                [("ARCHIVE-LEDGER-MISSING", LEDGER.as_posix())],
            )


if __name__ == "__main__":
    unittest.main()
