from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from document_contracts import (  # noqa: E402
    DocumentContractError,
    TASK_FIRST_RECORDING_EXTENSION,
    shared_edition_mismatches,
    shared_edition_surface_texts,
    validate_registry,
)


class SharedContractBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())

    @staticmethod
    def prior_task_creation(raw: dict) -> dict:
        previous = copy.deepcopy(raw)
        task = next(
            domain
            for domain in previous["lifecycle_domains"]
            if domain["family"] == "task"
        )
        task["initial_states"] = ["draft"]
        previous["shared_contract"]["extensions"] = [
            item
            for item in previous["shared_contract"]["extensions"]
            if item != TASK_FIRST_RECORDING_EXTENSION
        ]
        return previous

    def test_candidate_may_bind_source_without_approval_inference(self) -> None:
        raw = copy.deepcopy(self.raw)
        raw["shared_contract"].update(
            stage="candidate",
            version="3.1.0-draft.1",
            source_revision="a" * 40,
            approval_ref=None,
        )
        candidate = validate_registry(ROOT, raw).shared_contract
        self.assertEqual(candidate.stage, "candidate")
        self.assertEqual(candidate.source_revision, "a" * 40)
        self.assertIsNone(candidate.approval_ref)
        self.assertIsInstance(candidate.extensions, tuple)

    def test_adopted_binding_requires_provenance_fields_and_final_edition(self) -> None:
        for key in ("source_revision", "approval_ref", "version"):
            with self.subTest(key=key):
                raw = self.prior_task_creation(self.raw)
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
        raw = self.prior_task_creation(self.raw)
        raw["shared_contract"].update(
            stage="adopted",
            source_revision="a" * 40,
            approval_ref="reviewed-decision",
            version="3.0.0",
        )
        self.assertEqual(validate_registry(ROOT, raw).shared_contract.stage, "adopted")

    def test_absent_binding_remains_compatible_and_unknown_key_fails(self) -> None:
        raw = self.prior_task_creation(self.raw)
        spec_plan = next(
            domain
            for domain in raw["lifecycle_domains"]
            if domain["family"] == "spec-plan"
        )
        spec_plan["transitions"] = [
            edge for edge in spec_plan["transitions"] if edge != ["draft", "approved"]
        ]
        del raw["shared_contract"]
        self.assertIsNone(validate_registry(ROOT, raw).shared_contract)
        raw["unknown_common_source"] = {}
        with self.assertRaises(DocumentContractError):
            validate_registry(ROOT, raw)


class SharedEditionConsistencyTests(unittest.TestCase):
    def setUp(self) -> None:
        raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        self.contract = validate_registry(ROOT, raw).shared_contract

    def mismatches(self, texts: dict[str, str]) -> list[tuple[str, str]]:
        found = shared_edition_mismatches(
            self.contract, {PurePosixPath(k): v for k, v in texts.items()}
        )
        for item in found:
            self.assertEqual(item.rule_id, "REGISTRY_SHARED_EDITION_MISMATCH")
        return [(item.path.as_posix(), item.actual) for item in found]

    def test_rule_surface_mismatch_is_refused_in_both_forms(self) -> None:
        found = self.mismatches(
            {
                "docs/99.templates/README.md": "intro\n`WGOV-CORE / 3.1.0` binds\n",
                ".agents/governance/x.md": "not a new WGOV-CORE 2.9.0-rc.1 edition",
                ".codex/notes.md": "`WGOV-CORE` 3.2.0 and WGOV-CORE 3.0.0",
            }
        )
        self.assertEqual(
            found,
            [
                (".agents/governance/x.md", "line 1: WGOV-CORE 2.9.0-rc.1"),
                (".codex/notes.md", "line 1: WGOV-CORE 3.2.0"),
                ("docs/99.templates/README.md", "line 2: WGOV-CORE 3.1.0"),
            ],
        )

    def test_matching_history_and_editionless_mentions_pass(self) -> None:
        self.assertEqual(
            self.mismatches(
                {
                    ".claude/provider.md": "WGOV-CORE / 3.0.0 and `WGOV-CORE 3.0.0`",
                    ".agents/governance/y.md": "the WGOV-CORE claim stays local",
                    "docs/03.specs/0001-old/spec.md": "WGOV-CORE 1.0.0",
                    "CHANGELOG.md": "WGOV-CORE 2.0.0",
                    "docs/98.archive/z.md": "WGOV-CORE 2.0.0",
                    ".agents/data.json": "WGOV-CORE 9.9.9",
                }
            ),
            [],
        )

    def test_edition_boundaries_are_pinned(self) -> None:
        found = self.mismatches(
            {
                ".agents/a.md": "WGOV-CORE 3.1.0. Then WGOV-CORE 3.1.0의 판본.",
                ".agents/b.md": "first\nnot a new WGOV-CORE\n3.1.0 edition",
                ".agents/c.md": "WGOV-CORE 3.1 and WGOV-CORE v3.1.0 are not editions",
                ".agents/d.md": "WGOV-CORE 3.0.0-compatible, WGOV-CORE 3.1.0-compatible",
            }
        )
        self.assertEqual(
            found,
            [
                (".agents/a.md", "line 1: WGOV-CORE 3.1.0"),
                (".agents/a.md", "line 1: WGOV-CORE 3.1.0"),
                (".agents/b.md", "line 2: WGOV-CORE 3.1.0"),
                (".agents/d.md", "line 1: WGOV-CORE 3.1.0"),
            ],
        )

    def test_absent_shared_contract_disables_the_check(self) -> None:
        self.assertEqual(
            shared_edition_mismatches(
                None, {PurePosixPath(".agents/a.md"): "WGOV-CORE 9.9.9"}
            ),
            (),
        )

    def test_current_rule_surfaces_name_the_adopted_edition(self) -> None:
        self.assertEqual(
            shared_edition_mismatches(
                self.contract, shared_edition_surface_texts(ROOT)
            ),
            (),
        )


if __name__ == "__main__":
    unittest.main()
