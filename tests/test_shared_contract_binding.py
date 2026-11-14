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
# SPEC-0181 and SPEC-0194: the accepted texts of the eight WGOV-CORE extensions, in
# registry order.
EXTENSION_RECORDS = (
    (
        "Kubernetes/GitOps/bootstrap/external-service procedures",
        "Applies when repository work changes Kubernetes manifests, GitOps structure, cluster bootstrap or an external-service contract, procedures the shared contract does not define.",
        "The gitops-structure, gitops-change-set and external-service-contracts checks and the cluster-gate suite that scripts/validation/registry.json selects through python3 scripts/qa.py staged.",
        "When shared_contract.version changes and in any change to the k8s-validate, gitops-workflow or external-service-contract-audit skill, recorded in that change's Task.",
        "When a shared WGOV-CORE edition defines these procedures or the repository no longer carries Kubernetes or GitOps manifests.",
    ),
    (
        "Task Table/frontmatter summary",
        "Applies to every Task: one Task Table and one frontmatter status marker, with the marker derived from the rows of a multi-row Task.",
        "tests/test_task_summary_derivation.py and the strict Markdown profile check of the sdlc/task profile, both run by the document suite of scripts/run-contract-tests.py.",
        "When the sdlc/task body contract or its task_execution binding changes, and when shared_contract.version changes.",
        "When a shared WGOV-CORE edition defines the Task summary derivation or the registry drops the sdlc/task task_execution binding.",
    ),
    (
        "Registry document_language, Korean-allowed common agent Markdown, and Codex/Claude native syntax",
        "Applies to every governed document: the registry document_language contract selects its language, common agent Markdown under .agents/ may be Korean, and Codex and Claude native files keep their provider syntax.",
        "tests/test_document_language.py, the REGISTRY_DOCUMENT_LANGUAGE registry check and the strict Markdown profile check.",
        "When document_language changes and when shared_contract.version changes.",
        "When a shared WGOV-CORE edition defines the document language contract or document_language leaves the registry.",
    ),
    (
        "Local candidate Task first-recording of observed draft, ready, in-progress, or blocked state",
        "Applies when a new Task's first Git version records an observed nonterminal ready, in-progress or blocked row, under a scoped user request and Task Inputs that name its owner, prerequisites and evidence.",
        "tests/test_shared_contract_binding.py, the REGISTRY_LIFECYCLE_DOMAIN check of the Task initial states, and python3 scripts/validate-document-lifecycle.py --root . --mode staged.",
        "When shared_contract.version changes and when the task lifecycle domain changes.",
        "When a shared WGOV-CORE edition admits a nonterminal first-recording state for a Task, or Task creation returns to draft only.",
    ),
    (
        "Local candidate Spec/Plan direct draft-to-approved transition after actual batch review and approval",
        "Applies when a scoped user request, an actual batch review and the user's approval are recorded before a Spec and Plan move from draft to approved.",
        "tests/test_shared_contract_binding.py, the REGISTRY_LIFECYCLE_DOMAIN check that the spec-plan draft-to-approved edge exists exactly when this extension is declared, and the staged lifecycle check.",
        "When shared_contract.version changes and when the spec-plan lifecycle domain changes.",
        "When a shared WGOV-CORE edition admits the direct draft-to-approved transition, or Spec and Plan approval returns to a separate commit after draft.",
    ),
    (
        "Local candidate Spec/Plan first-recording as approved after actual batch review and approval",
        "Applies when a scoped request, an actual batch review and the user's approval precede the first Git record, which then holds the same-package Spec and Plan at approved with the Task Evidence review and approval receipt.",
        "tests/test_shared_contract_binding.py and the staged lifecycle check, which reads the review and approval receipt rows of the Task.",
        "When shared_contract.version changes and when the spec-plan lifecycle domain changes.",
        "When a shared WGOV-CORE edition admits a first record at approved, or Spec and Plan first records return to draft only.",
    ),
    (
        "Advisory shared workspace-memory SQLite store with Task and repository authority",
        "Applies when an agent keeps reusable context in the shared workspace memory store at .workspace-memory/memory.sqlite3, which stays advisory and never replaces Task or repository authority.",
        "tests/test_workspace_memory.py, run through the workspace-memory-regressions check in scripts/validation/registry.json.",
        "When .agents/governance/context-and-memory.md or scripts/workspace_memory.py changes, and when shared_contract.version changes.",
        "When the memory store is retired or a shared WGOV-CORE edition defines its own memory store.",
    ),
    (
        "Rules table Status column for retired policy rules",
        "Applies to every Rules table of this repository: a rule ID is never reused until a user-approved new baseline under the Q-07 contract and a retired rule keeps its row, so the table carries an optional Status column whose value is active, or retired; followed by a successor rule ID or none.",
        "POLICY-RULE-TABLE in the strict Markdown profile check and tests/test_policy_rule_ids.py, run by the document suite of scripts/run-contract-tests.py.",
        "When shared_contract.version changes and when the Rules table definition of the Policy TemplateDefinitions changes.",
        "When a shared WGOV-CORE edition of the Policy form defines rule retirement, when the user ends no-reuse retirement for rule IDs, or at a user-approved new baseline under the Q-07 contract.",
    ),
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
        self.assertEqual(len(shared["extensions"]), 8)
        self.assertEqual(len(shared["extensions"]), len(EXTENSION_RECORDS))
        for item, (name, condition, verification, review, removal) in zip(
            shared["extensions"], EXTENSION_RECORDS
        ):
            self.assertEqual(tuple(item), EXTENSION_FIELDS)
            self.assertEqual(item["name"], name)
            self.assertEqual(item["condition"], condition)
            self.assertNotEqual(item["condition"], item["name"])
            # The owner is the recorded contract owner, not a per-extension claim.
            self.assertEqual(item["owner"], shared["owner"])
            self.assertEqual(item["verification"], verification)
            self.assertEqual(item["review"], review)
            self.assertEqual(item["removal"], removal)
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
