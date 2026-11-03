"""Synthetic boundaries for the single Task criterion acceptance source."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path, PurePosixPath


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from document_contracts import (  # noqa: E402
    TASK_FIRST_RECORDING_EXTENSION,
    _terminal_semantic_diagnostics,
    load_registry,
    validate_registry,
)
from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    LifecycleEvidenceContext,
    LifecycleEvidenceDocument,
    _task_item_edge_diagnostics,
    compare_lifecycle,
    validate_current_task_evidence,
)


CRITERION = "[VAL-P03-001](../spec.md#success-criteria--verification-plan)"
ROOT = Path(__file__).resolve().parents[1]


class TaskHistoryRetentionTests(unittest.TestCase):
    path = Path("docs/03.specs/0999-example-package/tasks/tsk-0001-example.md")

    @classmethod
    def setUpClass(cls) -> None:
        registry = load_registry(Path(__file__).resolve().parents[1])
        cls.profile = next(
            profile
            for profile in registry.profiles
            if profile.profile_id == "sdlc/task"
        )

    def issues(
        self, *, evidence_changes: dict[str, str] | None = None, drop: bool = False
    ) -> set[str]:
        path = self.path
        base_work = {
            "ID": "WORK-001",
            "Upstream criterion": CRITERION,
            "Work item": "Verify",
            "Owner": "platform",
            "Status": "frontmatter",
            "Result": "FAIL",
            "Evidence": "Reason: check failed; Next owner: platform",
        }
        base_check = {
            "Evidence": "EVD-001",
            "Criteria": CRITERION,
            "Work Unit": "WORK-001",
            "Check": "Focused test",
            "Input": "revision one",
            "Result": "FAIL",
            "Location": "tests/fixture.py",
            "Required": "yes",
            "Resolves": "none",
        }
        proposed = (
            () if drop else (tuple((base_check | (evidence_changes or {})).items()),)
        )
        document = LifecycleDocument(path, "sdlc/task", "blocked")
        view = LifecycleEvidenceDocument(
            document=document,
            all_local_links=(),
            relationship_links=(),
            unresolved_relationship_links=(),
            body_table_links=(),
            relationship_section_valid=True,
            body_contract_valid=True,
            task_terminal_evidence_valid=False,
            body_rows=(tuple(base_work.items()),),
            task_evidence_rows=proposed,
        )
        context = LifecycleEvidenceContext(
            base_documents={path: document},
            proposed_documents={path: view},
            changed_paths=frozenset({path}),
            status_changed_paths=frozenset(),
            body_changed_paths=frozenset({path}),
            created_paths=frozenset(),
            base_task_rows={path: (tuple(base_work.items()),)},
            base_task_evidence_rows={path: (tuple(base_check.items()),)},
        )
        return {
            item.rule_id
            for item in _task_item_edge_diagnostics(
                self.profile, path, context, base_mode="staged"
            )
        }

    def test_adverse_evidence_cannot_be_deleted_or_rewritten(self) -> None:
        self.assertIn("TASK-EVIDENCE-RETENTION", self.issues(drop=True))
        for change in ({"Result": "PASS"}, {"Required": "no"}, {"Check": "Other"}):
            with self.subTest(change=change):
                self.assertIn(
                    "TASK-EVIDENCE-RETENTION", self.issues(evidence_changes=change)
                )
        self.assertEqual(self.issues(), set())

    def test_same_status_terminal_without_current_handoff_fails(self) -> None:
        path = self.path
        document = LifecycleDocument(path, "sdlc/task", "cancelled")
        view = LifecycleEvidenceDocument(
            document=document,
            all_local_links=(),
            relationship_links=(),
            unresolved_relationship_links=(),
            body_table_links=(),
            relationship_section_valid=True,
            body_contract_valid=True,
            task_terminal_evidence_valid=False,
            task_disposition_valid=False,
        )
        context = LifecycleEvidenceContext(
            base_documents={path: document},
            proposed_documents={path: view},
            changed_paths=frozenset(),
            status_changed_paths=frozenset(),
            body_changed_paths=frozenset(),
            created_paths=frozenset(),
        )
        self.assertIn(
            "TASK-DISPOSITION",
            {
                item.rule_id
                for item in validate_current_task_evidence(context, base_mode="staged")
            },
        )


class SpecPlanAuthorityTests(unittest.TestCase):
    def test_local_spec_plan_direct_approval_after_batch_review(self) -> None:
        raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        extension = (
            "Local candidate Spec/Plan direct draft-to-approved transition "
            "after actual batch review and approval"
        )
        domain = next(
            item for item in raw["lifecycle_domains"] if item["family"] == "spec-plan"
        )
        self.assertIn(raw["shared_contract"]["stage"], ("candidate", "adopted"))
        self.assertIn(extension, raw["shared_contract"]["extensions"])
        self.assertEqual(domain["initial_states"], ["draft"])
        self.assertIn(["draft", "approved"], domain["transitions"])
        registry = validate_registry(ROOT, raw)
        for name in ("spec", "plan"):
            with self.subTest(name=name):
                path = PurePosixPath(f"docs/03.specs/0999-new-package/{name}.md")
                profile = f"sdlc/{name}"
                previous = LifecycleDocument(path, profile, "draft")
                approved = LifecycleDocument(path, profile, "approved")
                self.assertNotIn(
                    "LIFECYCLE-EDGE",
                    {
                        item.rule_id
                        for item in compare_lifecycle(
                            registry,
                            {path: previous},
                            {path: approved},
                            base_mode="staged",
                        )
                    },
                )
                self.assertIn(
                    "LIFECYCLE-CREATE",
                    {
                        item.rule_id
                        for item in compare_lifecycle(
                            registry, {}, {path: approved}, base_mode="staged"
                        )
                    },
                )

    def test_spec_plan_direct_approval_requires_exact_local_extension(self) -> None:
        raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        extension = (
            "Local candidate Spec/Plan direct draft-to-approved transition "
            "after actual batch review and approval"
        )
        domains = [dict(item) for item in raw["lifecycle_domains"]]
        index = next(
            i for i, item in enumerate(domains) if item["family"] == "spec-plan"
        )
        domains[index]["transitions"] = [
            *(
                edge
                for edge in domains[index]["transitions"]
                if edge != ["draft", "approved"]
            ),
            ["draft", "approved"],
        ]
        candidate = raw | {"lifecycle_domains": domains}
        extensions = [
            item for item in raw["shared_contract"]["extensions"] if item != extension
        ]
        for shared in (
            {**raw["shared_contract"], "extensions": extensions},
            {
                **raw["shared_contract"],
                "extensions": [*extensions, "unreviewed direct approval"],
            },
            {**raw["shared_contract"], "stage": "unreviewed"},
        ):
            with self.subTest(shared_contract=shared):
                self.assertTrue(
                    any(
                        item.rule_id == "REGISTRY_LIFECYCLE_DOMAIN"
                        and "spec-plan" in item.actual
                        for item in _terminal_semantic_diagnostics(
                            ROOT, candidate | {"shared_contract": shared}
                        )
                    ),
                )
        without_edge = [dict(item) for item in raw["lifecycle_domains"]]
        without_edge[index]["transitions"] = [
            edge
            for edge in without_edge[index]["transitions"]
            if edge != ["draft", "approved"]
        ]
        self.assertTrue(
            any(
                item.rule_id == "REGISTRY_LIFECYCLE_DOMAIN"
                and "spec-plan" in item.actual
                for item in _terminal_semantic_diagnostics(
                    ROOT, raw | {"lifecycle_domains": without_edge}
                )
            )
        )

    def test_modern_parent_creation_stays_draft_and_task_initial_set_is_exact(
        self,
    ) -> None:
        registry = json.loads((ROOT / "docs/99.templates/registry.json").read_text())

        def issues(payload):
            return {
                item.rule_id for item in _terminal_semantic_diagnostics(ROOT, payload)
            }

        self.assertNotIn("REGISTRY_LIFECYCLE_DOMAIN", issues(registry))
        for family, invalid in (
            ("spec-plan", ["approved"]),
            ("spec-plan", ["blocked"]),
            ("spec-plan", ["in-progress"]),
            ("spec-plan", None),
            ("task", ["draft"]),
            ("task", ["ready"]),
            ("task", ["draft", "ready", "completed"]),
            ("task", ["draft", "ready", "in-progress", "blocked", "cancelled"]),
            ("task", None),
        ):
            with self.subTest(family=family, invalid=invalid):
                domains = [dict(item) for item in registry["lifecycle_domains"]]
                index = next(
                    i for i, item in enumerate(domains) if item["family"] == family
                )
                if invalid is None:
                    domains[index].pop("initial_states")
                else:
                    domains[index]["initial_states"] = invalid
                self.assertIn(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    issues(registry | {"lifecycle_domains": domains}),
                )

    def test_local_lifecycle_extensions_remain_effective_after_adoption(self) -> None:
        raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        adopted = raw | {
            "shared_contract": {**raw["shared_contract"], "stage": "adopted"}
        }
        registry = validate_registry(ROOT, adopted)
        spec = PurePosixPath("docs/03.specs/0999-new-package/spec.md")
        task = PurePosixPath("docs/03.specs/0999-new-package/tasks/tsk-0001-work.md")
        self.assertNotIn(
            "LIFECYCLE-EDGE",
            {
                item.rule_id
                for item in compare_lifecycle(
                    registry,
                    {spec: LifecycleDocument(spec, "sdlc/spec", "draft")},
                    {spec: LifecycleDocument(spec, "sdlc/spec", "approved")},
                    base_mode="staged",
                )
            },
        )
        self.assertNotIn(
            "LIFECYCLE-CREATE",
            {
                item.rule_id
                for item in compare_lifecycle(
                    registry,
                    {},
                    {task: LifecycleDocument(task, "sdlc/task", "blocked")},
                    base_mode="staged",
                )
            },
        )

    def test_local_task_first_recording_accepts_observed_nonterminal_state(
        self,
    ) -> None:
        raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        self.assertIn(raw["shared_contract"]["stage"], ("candidate", "adopted"))
        self.assertIn(
            TASK_FIRST_RECORDING_EXTENSION, raw["shared_contract"]["extensions"]
        )
        registry = validate_registry(ROOT, raw)
        task = PurePosixPath("docs/03.specs/0999-new-package/tasks/tsk-0001-work.md")
        for status in ("draft", "ready", "in-progress", "blocked"):
            with self.subTest(status=status):
                created = LifecycleDocument(task, "sdlc/task", status)
                self.assertNotIn(
                    "LIFECYCLE-CREATE",
                    {
                        item.rule_id
                        for item in compare_lifecycle(
                            registry, {}, {task: created}, base_mode="staged"
                        )
                    },
                )
        for status in ("completed", "cancelled"):
            with self.subTest(status=status):
                created = LifecycleDocument(task, "sdlc/task", status)
                self.assertIn(
                    "LIFECYCLE-CREATE",
                    {
                        item.rule_id
                        for item in compare_lifecycle(
                            registry, {}, {task: created}, base_mode="staged"
                        )
                    },
                )

    def test_task_first_recording_requires_explicit_local_extension(self) -> None:
        raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        for candidate in (
            {**raw, "shared_contract": {**raw["shared_contract"], "extensions": []}},
            {
                **raw,
                "shared_contract": {
                    **raw["shared_contract"],
                    "extensions": ["unreviewed Task creation permission"],
                },
            },
            {
                **raw,
                "shared_contract": {**raw["shared_contract"], "stage": "unreviewed"},
            },
        ):
            with self.subTest(shared_contract=candidate["shared_contract"]):
                self.assertIn(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    {
                        item.rule_id
                        for item in _terminal_semantic_diagnostics(ROOT, candidate)
                    },
                )

    def test_new_parent_cannot_claim_legacy_execution_state(self) -> None:
        registry = load_registry(ROOT)
        domain = next(
            item for item in registry.lifecycle_domains if item.family == "spec-plan"
        )
        self.assertTrue(domain.allows("approved", "in-review"))
        self.assertTrue(domain.allows("draft", "cancelled"))
        self.assertFalse(domain.allows("approved", "in-progress"))
        self.assertFalse(domain.allows("in-progress", "completed"))
        path = PurePosixPath("docs/03.specs/0999-new-package/spec.md")
        created = LifecycleDocument(path, "sdlc/spec", "completed")
        self.assertIn(
            "LIFECYCLE-CREATE",
            {
                item.rule_id
                for item in compare_lifecycle(
                    registry, {}, {path: created}, base_mode="staged"
                )
            },
        )


if __name__ == "__main__":
    unittest.main()
