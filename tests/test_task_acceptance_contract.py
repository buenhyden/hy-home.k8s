"""Synthetic boundaries for the single Task criterion acceptance source."""

from __future__ import annotations

import json
import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from document_contracts import (  # noqa: E402
    TASK_FIRST_RECORDING_EXTENSION,
    _terminal_semantic_diagnostics,
    extension_name,
    load_registry,
    local_extension_names,
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


def shared_extension(name: str) -> dict[str, str]:
    """A local extension whose owner, tests and review are not recorded."""

    return {
        "name": name,
        "condition": name,
        "owner": "unverified",
        "verification": "unverified",
        "review": "unverified",
        "removal": "unverified",
    }


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
    def test_first_approved_requires_scoped_approval_context(self) -> None:
        raw = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        extension = "Local candidate Spec/Plan first-recording as approved after actual batch review and approval"
        if extension not in local_extension_names(raw["shared_contract"]):
            raw["shared_contract"]["extensions"].append(shared_extension(extension))
        registry = validate_registry(ROOT, raw)
        package = PurePosixPath("docs/03.specs/0999-new-package")
        spec = package / "spec.md"
        plan = package / "plan.md"
        task = package / "tasks/tsk-0001-work.md"
        texts = {
            spec: (
                "---\n"
                'title: "Example Spec"\nversion: "0.1.0"\ntype: "sdlc/spec"\n'
                'status: "approved"\nowner: "platform"\nupdated: "2026-11-10"\n'
                'artifact_id: "SPEC-0999"\n---\n\n'
                "# Example Spec\n\n## Overview\n\nReviewed contract.\n"
            ),
            plan: (
                "---\n"
                'title: "Example Plan"\nversion: "0.1.0"\ntype: "sdlc/plan"\n'
                'status: "approved"\nowner: "platform"\nupdated: "2026-11-10"\n'
                'artifact_id: "SPEC-0999-PLAN-0001"\n'
                'parent_ids: ["SPEC-0999"]\n---\n\n'
                "# Example Plan\n\n## Overview\n\nReviewed order.\n"
            ),
        }
        spec_hash = hashlib.sha256(texts[spec].encode()).hexdigest()
        plan_hash = hashlib.sha256(texts[plan].encode()).hexdigest()
        review_input = json.dumps(
            {"spec_sha256": spec_hash, "plan_sha256": plan_hash},
            separators=(",", ":"),
        )
        approval_input = json.dumps(
            {
                "actor": "user",
                "approval_ref": "synthetic-chat-approval",
                "review_ref": "EVD-003",
                "scope": ["SPEC-0999", "SPEC-0999-PLAN-0001"],
                "reviewed_spec_sha256": spec_hash,
                "reviewed_plan_sha256": plan_hash,
                "validity": "confirmed",
                "revocation": "none",
            },
            separators=(",", ":"),
        )
        prior_hash = "0" * 64
        prior_review_input = json.dumps(
            {"spec_sha256": prior_hash, "plan_sha256": prior_hash},
            separators=(",", ":"),
        )
        prior_approval_input = json.dumps(
            {
                "actor": "user",
                "approval_ref": "synthetic-prior-approval",
                "review_ref": "EVD-001",
                "scope": ["SPEC-0999", "SPEC-0999-PLAN-0001"],
                "reviewed_spec_sha256": prior_hash,
                "reviewed_plan_sha256": prior_hash,
                "validity": "confirmed",
                "revocation": "none",
            },
            separators=(",", ":"),
        )
        texts[task] = (
            "---\n"
            'title: "Example Task"\nversion: "0.1.0"\ntype: "sdlc/task"\n'
            'status: "draft"\nowner: "platform"\nupdated: "2026-11-10"\n'
            'artifact_id: "SPEC-0999-TSK-0001"\n'
            'parent_ids: ["SPEC-0999-PLAN-0001"]\n---\n\n'
            "# Example Task\n\n## Task Evidence\n\n"
            "| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            f"| EVD-001 | {CRITERION} | WORK-001 | Independent semantic review | {prior_review_input} | PASS | older synthetic review | yes | none |\n"
            f"| EVD-002 | {CRITERION} | WORK-001 | Spec/Plan first-record approval | {prior_approval_input} | PASS | older synthetic approval | yes | none |\n"
            f"| EVD-003 | {CRITERION} | WORK-001 | Independent semantic review | {review_input} | PASS | current synthetic reviewer receipt | yes | none |\n"
            f"| EVD-004 | {CRITERION} | WORK-001 | Spec/Plan first-record approval | {approval_input} | PASS | synthetic chat reply | yes | none |\n"
        )
        documents = {
            path: LifecycleDocument(path, profile, "approved")
            for path, profile in (
                (spec, "sdlc/spec"),
                (plan, "sdlc/plan"),
            )
        }
        documents[task] = LifecycleDocument(task, "sdlc/task", "draft")
        module_spec = importlib.util.spec_from_file_location(
            "first_approved_lifecycle_tested",
            ROOT / "scripts/validate-document-lifecycle.py",
        )
        assert module_spec is not None and module_spec.loader is not None
        validator = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = validator
        module_spec.loader.exec_module(validator)

        def rules(
            *,
            candidate_registry=registry,
            candidate_documents=documents,
            candidate_texts=texts,
            base_documents=None,
            base_texts=None,
            with_context=True,
        ) -> set[str]:
            prior_documents = base_documents or {}
            prior_texts = base_texts or {}
            context = (
                validator._evidence_context(
                    candidate_registry,
                    prior_documents,
                    candidate_documents,
                    prior_texts,
                    candidate_texts,
                )
                if with_context
                else None
            )
            return {
                item.rule_id
                for item in compare_lifecycle(
                    candidate_registry,
                    prior_documents,
                    candidate_documents,
                    base_mode="staged",
                    evidence_context=context,
                )
            }

        self.assertNotIn(
            "LIFECYCLE-CREATE",
            rules(),
        )
        self.assertIn("LIFECYCLE-CREATE", rules(with_context=False))

        missing_extension = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text()
        )
        missing_extension["shared_contract"]["extensions"] = [
            item
            for item in missing_extension["shared_contract"]["extensions"]
            if extension_name(item)
            != "Local candidate Spec/Plan first-recording as approved after actual batch review and approval"
        ]
        self.assertIn(
            "LIFECYCLE-CREATE",
            rules(candidate_registry=validate_registry(ROOT, missing_extension)),
        )

        def changed_task(old: str, new: str) -> dict[PurePosixPath, str]:
            lines = texts[task].splitlines(keepends=True)
            current = next(
                index
                for index, line in enumerate(lines)
                if line.startswith("| EVD-004 |")
            )
            assert old in lines[current]
            lines[current] = lines[current].replace(old, new, 1)
            return texts | {task: "".join(lines)}

        adverse_rows = {
            "wrong actor": changed_task('"actor":"user"', '"actor":"agent"'),
            "empty approval ref": changed_task(
                '"approval_ref":"synthetic-chat-approval"',
                '"approval_ref":""',
            ),
            "wrong scope": changed_task(
                '"scope":["SPEC-0999","SPEC-0999-PLAN-0001"]',
                '"scope":["SPEC-0998","SPEC-0999-PLAN-0001"]',
            ),
            "wrong review ref": changed_task(
                '"review_ref":"EVD-003"', '"review_ref":"EVD-001"'
            ),
            "missing review ref": changed_task(
                '"review_ref":"EVD-003"', '"review_ref":"EVD-099"'
            ),
            "wrong approval digest": changed_task(
                f'"reviewed_spec_sha256":"{spec_hash}"',
                f'"reviewed_spec_sha256":"{"0" * 64}"',
            ),
            "unknown revocation": changed_task(
                '"revocation":"none"', '"revocation":"unknown"'
            ),
            "unknown validity": changed_task(
                '"validity":"confirmed"', '"validity":"unknown"'
            ),
            "missing approval row": texts
            | {
                task: "\n".join(
                    line
                    for line in texts[task].split("\n")
                    if "Spec/Plan first-record approval" not in line
                )
            },
            "stale approval only": texts
            | {
                task: "\n".join(
                    line
                    for line in texts[task].split("\n")
                    if not line.startswith("| EVD-004 |")
                )
            },
            "duplicate current approval": texts
            | {
                task: texts[task]
                + next(
                    line
                    for line in texts[task].splitlines(keepends=True)
                    if line.startswith("| EVD-004 |")
                ).replace("| EVD-004 |", "| EVD-005 |", 1)
            },
        }
        for label, candidate in adverse_rows.items():
            with self.subTest(label=label):
                self.assertIn(
                    "LIFECYCLE-CREATE",
                    rules(candidate_texts=candidate),
                )

        old_task = {task: documents[task]}
        self.assertIn(
            "LIFECYCLE-CREATE",
            rules(base_documents=old_task, base_texts={task: texts[task]}),
        )

        for name, path, status in (
            ("half approved", plan, "draft"),
            ("terminal", spec, "completed"),
        ):
            with self.subTest(name=name):
                old_text = texts[path]
                new_text = old_text.replace(
                    'status: "approved"', f'status: "{status}"', 1
                )
                old_hash = hashlib.sha256(old_text.encode()).hexdigest()
                new_hash = hashlib.sha256(new_text.encode()).hexdigest()
                candidate_texts = texts | {
                    path: new_text,
                    task: texts[task].replace(old_hash, new_hash),
                }
                candidate_documents = documents | {
                    path: LifecycleDocument(path, documents[path].profile_id, status)
                }
                self.assertIn(
                    "LIFECYCLE-CREATE",
                    rules(
                        candidate_documents=candidate_documents,
                        candidate_texts=candidate_texts,
                    ),
                )

        invalid_plan = texts[plan].replace(
            'parent_ids: ["SPEC-0999"]', 'parent_ids: ["SPEC-0998"]', 1
        )
        invalid_plan_hash = hashlib.sha256(invalid_plan.encode()).hexdigest()
        self.assertIn(
            "LIFECYCLE-CREATE",
            rules(
                candidate_texts=texts
                | {
                    plan: invalid_plan,
                    task: texts[task].replace(plan_hash, invalid_plan_hash),
                }
            ),
        )

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
        self.assertIn(extension, local_extension_names(raw["shared_contract"]))
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
            item
            for item in raw["shared_contract"]["extensions"]
            if extension_name(item) != extension
        ]
        for shared in (
            {**raw["shared_contract"], "extensions": extensions},
            {
                **raw["shared_contract"],
                "extensions": [
                    *extensions,
                    shared_extension("unreviewed direct approval"),
                ],
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
        spec = PurePosixPath("docs/03.specs/0999-new-package/spec.md")
        task = PurePosixPath("docs/03.specs/0999-new-package/tasks/tsk-0001-work.md")
        for stage in ("approved", "adopted"):
            registry = validate_registry(
                ROOT,
                raw | {"shared_contract": {**raw["shared_contract"], "stage": stage}},
            )
            with self.subTest(stage=stage):
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
            TASK_FIRST_RECORDING_EXTENSION,
            local_extension_names(raw["shared_contract"]),
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
                    "extensions": [
                        shared_extension("unreviewed Task creation permission")
                    ],
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
