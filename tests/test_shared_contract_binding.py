from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_contracts as CONTRACTS  # noqa: E402
from document_contracts import (  # noqa: E402
    DocumentContractError,
    SPEC_PLAN_DIRECT_APPROVAL_EXTENSION,
    SPEC_PLAN_FIRST_APPROVED_EXTENSION,
    TASK_FIRST_RECORDING_EXTENSION,
    shared_edition_mismatches,
    shared_edition_surface_texts,
    validate_registry,
)

APPROVAL_FIELDS = ("approved_by", "approved_at", "effective_from")
EXTENSION_FIELDS = ("name", "condition", "owner", "verification", "review", "removal")


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
            if CONTRACTS.extension_name(item) != TASK_FIRST_RECORDING_EXTENSION
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
        for key in APPROVAL_FIELDS:
            del raw["shared_contract"][key]
        candidate = validate_registry(ROOT, raw).shared_contract
        self.assertEqual(candidate.stage, "candidate")
        self.assertEqual(candidate.source_revision, "a" * 40)
        self.assertIsNone(candidate.approval_ref)
        self.assertIsNone(candidate.approved_by)
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


class SharedContractApprovalFieldsTests(unittest.TestCase):
    """SPEC-0168: the approved stage, approval facts and extension objects."""

    def setUp(self) -> None:
        self.raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())

    def candidate(self, **changes: object) -> dict:
        raw = copy.deepcopy(self.raw)
        raw["shared_contract"].update(changes)
        return raw

    def rules(self, raw: dict) -> set[str]:
        try:
            validate_registry(ROOT, raw)
        except DocumentContractError as error:
            return {item.rule_id for item in error.diagnostics}
        return set()

    def test_repository_record_states_only_what_is_recorded(self) -> None:
        shared = self.raw["shared_contract"]
        self.assertEqual(shared["stage"], "adopted")
        for key in APPROVAL_FIELDS:
            self.assertEqual(shared[key], "unverified")
        # No record states scope, migration or rollback (W03-D05); the
        # consumed edition is the registry's own version.
        for key in ("scope", "migration", "rollback"):
            self.assertEqual(shared[key], "unverified")
        self.assertEqual(shared["consumer_version"], shared["version"])
        self.assertEqual(len(shared["extensions"]), 7)
        for item in shared["extensions"]:
            self.assertEqual(tuple(item), EXTENSION_FIELDS)
            self.assertEqual(item["condition"], item["name"])
            for key in ("owner", "verification", "review", "removal"):
                self.assertEqual(item[key], "unverified")
        names = [CONTRACTS.extension_name(item) for item in shared["extensions"]]
        self.assertEqual(
            names[3:6],
            [
                TASK_FIRST_RECORDING_EXTENSION,
                SPEC_PLAN_DIRECT_APPROVAL_EXTENSION,
                SPEC_PLAN_FIRST_APPROVED_EXTENSION,
            ],
        )
        loaded = validate_registry(ROOT, self.raw).shared_contract
        self.assertEqual(loaded.approved_by, "unverified")
        self.assertEqual([item.name for item in loaded.extensions], names)

    def test_approved_and_adopted_require_every_approval_fact(self) -> None:
        for stage in ("approved", "adopted"):
            for key in APPROVAL_FIELDS:
                raw = self.candidate(stage=stage)
                del raw["shared_contract"][key]
                with self.subTest(stage=stage, missing=key):
                    self.assertIn("REGISTRY_SCHEMA", self.rules(raw))
        self.assertEqual(self.rules(self.candidate(stage="approved")), set())

    def test_candidate_needs_no_approval_facts(self) -> None:
        raw = self.candidate(
            stage="candidate",
            version="3.1.0-draft.1",
            source_revision="a" * 40,
            approval_ref=None,
        )
        for key in APPROVAL_FIELDS:
            del raw["shared_contract"][key]
        self.assertEqual(self.rules(raw), set())

    def test_unverified_is_admitted_only_with_an_approval_ref(self) -> None:
        for stage in ("candidate", "approved", "adopted"):
            raw = self.candidate(stage=stage, approval_ref=None)
            with self.subTest(stage=stage):
                self.assertIn("REGISTRY_SCHEMA", self.rules(raw))
        for key in APPROVAL_FIELDS:
            raw = self.candidate(stage="approved", approval_ref=None)
            for other in APPROVAL_FIELDS:
                raw["shared_contract"][other] = (
                    "unverified"
                    if other == key
                    else "operator"
                    if other == "approved_by"
                    else "2026-11-12"
                )
            with self.subTest(only=key):
                self.assertIn("REGISTRY_SCHEMA", self.rules(raw))
        recorded = self.candidate(
            stage="approved",
            approval_ref=None,
            approved_by="operator",
            approved_at="2026-11-12",
            effective_from="2026-11-12",
        )
        self.assertEqual(self.rules(recorded), set())
        for key, value in (
            ("approved_at", "yesterday"),
            ("effective_from", "2026-13-40x"),
            ("approved_by", " "),
        ):
            with self.subTest(malformed=key):
                self.assertIn(
                    "REGISTRY_SCHEMA", self.rules(self.candidate(**{key: value}))
                )

    def test_optional_descriptive_fields_are_nonempty_strings(self) -> None:
        raw = self.candidate(
            scope="repository",
            migration="none",
            rollback="revert",
            consumer_version="1",
        )
        self.assertEqual(self.rules(raw), set())
        loaded = validate_registry(ROOT, raw).shared_contract
        self.assertEqual((loaded.scope, loaded.consumer_version), ("repository", "1"))
        self.assertIn("REGISTRY_SCHEMA", self.rules(self.candidate(rollback="")))

    def test_extension_is_an_object_with_every_field(self) -> None:
        for key in EXTENSION_FIELDS:
            raw = copy.deepcopy(self.raw)
            del raw["shared_contract"]["extensions"][0][key]
            with self.subTest(missing=key):
                self.assertIn("REGISTRY_SCHEMA", self.rules(raw))
        raw = copy.deepcopy(self.raw)
        raw["shared_contract"]["extensions"][0]["owner"] = ""
        self.assertIn("REGISTRY_SCHEMA", self.rules(raw))
        raw = copy.deepcopy(self.raw)
        raw["shared_contract"]["extensions"][0] = "a bare name"
        self.assertIn("REGISTRY_SCHEMA", self.rules(raw))
        raw = copy.deepcopy(self.raw)
        raw["shared_contract"]["extensions"][0]["note"] = "extra"
        self.assertIn("REGISTRY_SCHEMA", self.rules(raw))

    def test_extension_names_are_unique(self) -> None:
        raw = copy.deepcopy(self.raw)
        twin = copy.deepcopy(raw["shared_contract"]["extensions"][0])
        twin["condition"] = "a different condition"
        raw["shared_contract"]["extensions"].append(twin)
        self.assertIn("REGISTRY_SHARED_EXTENSION", self.rules(raw))

    def test_local_extensions_apply_at_all_three_stages_and_no_other(self) -> None:
        for stage in ("candidate", "approved", "adopted"):
            shared = {**self.raw["shared_contract"], "stage": stage}
            with self.subTest(stage=stage):
                self.assertIn(
                    TASK_FIRST_RECORDING_EXTENSION,
                    CONTRACTS.local_extension_names(shared),
                )
                self.assertEqual(self.rules(self.candidate(stage=stage)), set())
        unreviewed = {**self.raw["shared_contract"], "stage": "unreviewed"}
        self.assertEqual(CONTRACTS.local_extension_names(unreviewed), frozenset())
        self.assertEqual(CONTRACTS.local_extension_names(None), frozenset())

    def test_one_accessor_reads_names_from_every_extension_form(self) -> None:
        raw = self.raw["shared_contract"]["extensions"][0]
        typed = validate_registry(ROOT, self.raw).shared_contract
        self.assertEqual(CONTRACTS.extension_name(raw), raw["name"])
        self.assertEqual(CONTRACTS.extension_name(typed.extensions[0]), raw["name"])
        self.assertEqual(
            CONTRACTS.local_extension_names(typed),
            CONTRACTS.local_extension_names(self.raw["shared_contract"]),
        )

    def test_comparison_base_with_bare_extension_names_reads_unchanged(self) -> None:
        raw = copy.deepcopy(self.raw)
        shared = raw["shared_contract"]
        for key in APPROVAL_FIELDS:
            del shared[key]
        shared["extensions"] = [
            CONTRACTS.extension_name(item) for item in shared["extensions"]
        ]
        del raw["common_forms"]
        for profile in raw["profiles"]:
            profile.pop("document_role", None)
        loaded = CONTRACTS._typed_registry_from_mapping(raw)
        self.assertEqual(loaded.common_forms, ())
        self.assertIsNone(loaded.shared_contract.approved_by)
        self.assertIn(
            SPEC_PLAN_FIRST_APPROVED_EXTENSION,
            CONTRACTS.local_extension_names(loaded.shared_contract),
        )
        self.assertEqual(loaded.shared_contract.extensions[0].owner, "unverified")


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
