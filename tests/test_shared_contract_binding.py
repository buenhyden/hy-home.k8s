from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from document_contracts import (  # noqa: E402
    DocumentContractError,
    validate_registry,
)


class SharedContractBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())

    def test_candidate_nullable_proof_is_read_without_approval_inference(self) -> None:
        candidate = validate_registry(ROOT, self.raw).shared_contract
        self.assertEqual(candidate.stage, "candidate")
        self.assertIsNone(candidate.source_revision)
        self.assertIsNone(candidate.approval_ref)
        self.assertIsInstance(candidate.extensions, tuple)

    def test_adopted_binding_requires_proof_and_release_edition(self) -> None:
        for key in ("source_revision", "approval_ref", "version"):
            with self.subTest(key=key):
                raw = copy.deepcopy(self.raw)
                raw["shared_contract"].update(
                    stage="adopted",
                    source_revision="a" * 40,
                    approval_ref="reviewed-decision",
                    version="3.0.0",
                )
                raw["shared_contract"][key] = (
                    "3.0.0-draft.3" if key == "version" else None
                )
                with self.assertRaises(DocumentContractError):
                    validate_registry(ROOT, raw)

    def test_complete_adoption_is_only_structural_evidence(self) -> None:
        raw = copy.deepcopy(self.raw)
        raw["shared_contract"].update(
            stage="adopted",
            source_revision="a" * 40,
            approval_ref="reviewed-decision",
            version="3.0.0",
        )
        self.assertEqual(validate_registry(ROOT, raw).shared_contract.stage, "adopted")

    def test_absent_binding_remains_compatible_and_unknown_key_fails(self) -> None:
        raw = copy.deepcopy(self.raw)
        del raw["shared_contract"]
        self.assertIsNone(validate_registry(ROOT, raw).shared_contract)
        raw["unknown_common_source"] = {}
        with self.assertRaises(DocumentContractError):
            validate_registry(ROOT, raw)


if __name__ == "__main__":
    unittest.main()
