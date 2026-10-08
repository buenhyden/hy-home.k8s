"""Synthetic boundaries for the single Task criterion acceptance source."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from dataclasses import replace
from pathlib import Path, PurePosixPath


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from document_contracts import (  # noqa: E402
    _terminal_semantic_diagnostics,
    _typed_registry_from_mapping,
    classify_path,
    legacy_task_profile,
    load_registry,
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


def load_lifecycle_cli():
    spec = importlib.util.spec_from_file_location(
        "task_acceptance_lifecycle", ROOT / "scripts/validate-document-lifecycle.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TaskHistoryRetentionTests(unittest.TestCase):
    path = Path(
        "docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0017-example.md"
    )

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
        document = LifecycleDocument(path, "sdlc/task", "superseded")
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

    def test_only_reviewed_p01_adverse_rows_may_rebind(self) -> None:
        cli = load_lifecycle_cli()
        registry = load_registry(ROOT)
        path = PurePosixPath(
            "docs/03.specs/0105-authority-and-safe-authoring/tasks/"
            "tsk-0004-current-contract-review.md"
        )
        spec, plan = path.parent.parent / "spec.md", path.parent.parent / "plan.md"
        old_text = subprocess.check_output(
            ["git", "show", f"ae93644e7e1137ed66ac243af4156ecea2d9cee4:{path}"],
            cwd=ROOT,
        ).decode("utf-8")
        proposed_texts = {
            item: (ROOT / item).read_text(encoding="utf-8")
            for item in (path, spec, plan)
        }
        context = cli._evidence_context(
            registry,
            {path: cli.document_from_text(registry, path, old_text)},
            {
                item: cli.document_from_text(registry, item, text)
                for item, text in proposed_texts.items()
            },
            {path: old_text},
            proposed_texts,
            root=ROOT,
        )
        profile = classify_path(registry, path)

        def rules(candidate):
            return {
                item.rule_id
                for item in _task_item_edge_diagnostics(
                    profile, path, candidate, base_mode="staged"
                )
            }

        self.assertIn(path, context.baseline_task_paths)
        self.assertEqual(rules(context), set())
        view = context.proposed_documents[path]
        rows = tuple(dict(cells) for cells in view.task_evidence_rows)
        wrong_criterion = next(
            row["Criteria"] for row in rows if row["Evidence"] == "EVD-008"
        )
        for identifier in ("EVD-001", "EVD-003"):
            with self.subTest(identifier=identifier):
                changed = tuple(
                    tuple((row | {"Criteria": wrong_criterion}).items())
                    if row["Evidence"] == identifier
                    else tuple(row.items())
                    for row in rows
                )
                tampered = replace(
                    context,
                    proposed_documents=context.proposed_documents
                    | {path: replace(view, task_evidence_rows=changed)},
                )
                self.assertIn("TASK-EVIDENCE-RETENTION", rules(tampered))


class ApprovedPackageRetentionTests(unittest.TestCase):
    package = PurePosixPath("docs/03.specs/0107-local-qa-and-release")

    def source_snapshot(self):
        cli = load_lifecycle_cli()
        registry = load_registry(ROOT)
        spec = self.package / "spec.md"
        plan = self.package / "plan.md"
        task = self.package / "tasks/tsk-0001-local-qa-and-release.md"
        texts = {
            path: (ROOT / path).read_text(encoding="utf-8")
            for path in (spec, plan, task)
        }
        for path in (spec, plan):
            texts[path] = texts[path].replace(
                'status: "completed"', 'status: "approved"', 1
            )
        documents = {
            path: cli.document_from_text(registry, path, text)
            for path, text in texts.items()
        }
        schema = json.loads(
            (ROOT / "docs/99.templates/contracts/frontmatter.schema.json").read_text()
        )
        return cli, registry, spec, plan, task, documents, texts, schema

    def test_actual_source_snapshot_requires_package_closure(self) -> None:
        cli, registry, spec, plan, task, documents, texts, schema = (
            self.source_snapshot()
        )

        def rules(docs, bodies):
            return {
                item.rule_id
                for item in cli._completion_document_diagnostics(
                    ROOT,
                    registry,
                    (spec,),
                    docs,
                    bodies,
                    schema,
                    base_mode="explicit-ref",
                )
            }

        self.assertEqual(rules(documents, texts), set())
        self.assertIn(
            "COMPLETION-PLAN",
            rules({key: val for key, val in documents.items() if key != plan}, texts),
        )
        self.assertIn(
            "COMPLETION-TASK",
            rules({key: val for key, val in documents.items() if key != task}, texts),
        )
        empty_criteria = texts | {
            spec: re.sub(r"(?m)^\| VAL-LOCAL-QA-\d{3} \|[^\n]*\n", "", texts[spec])
        }
        empty_criteria_docs = documents | {
            spec: cli.document_from_text(registry, spec, empty_criteria[spec])
        }
        self.assertIn("COMPLETION-CRITERIA", rules(empty_criteria_docs, empty_criteria))
        blocked = texts | {
            task: texts[task].replace('status: "completed"', 'status: "blocked"', 1)
        }
        blocked_docs = documents | {
            task: cli.document_from_text(registry, task, blocked[task])
        }
        self.assertTrue(rules(blocked_docs, blocked))

    def modern_failure_snapshot(self):
        cli, registry, spec, _plan, task, documents, texts, schema = (
            self.source_snapshot()
        )
        criteria = tuple(f"VAL-LOCAL-QA-{index:03d}" for index in range(1, 5))
        links = tuple(
            f"[{item}](../spec.md#success-criteria--verification-plan)"
            for item in criteria
        )
        work = f"| WORK-001 | {', '.join(links)} | Verify all criteria | platform | frontmatter | PASS | EVD-TEST-002, EVD-TEST-003, EVD-TEST-004, EVD-TEST-005 |"
        checks = [
            f"| EVD-TEST-001 | {links[0]} | WORK-001 | Focused test | same source snapshot | FAIL | tests/fixture.py | yes | none |"
        ]
        checks.extend(
            f"| EVD-TEST-{index + 1:03d} | {link} | WORK-001 | Focused test | same source snapshot | PASS | tests/fixture.py | yes | none |"
            for index, link in enumerate(links, start=1)
        )
        decisions = (
            f"| {link} | accepted | EVD-TEST-{index + 1:03d} | Focused test passed | platform |"
            for index, link in enumerate(links, start=1)
        )
        replacement = (
            "\n".join(
                (
                    "## Task Table",
                    "### Lifecycle Traceability",
                    "| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |",
                    "| --- | --- | --- | --- | --- | --- | --- |",
                    work,
                    "## Task Evidence",
                    "| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |",
                    "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                    *checks,
                    "## Criterion Acceptance",
                    "| Criterion | Acceptance | Evidence | Disposition | Current owner |",
                    "| --- | --- | --- | --- | --- |",
                    *decisions,
                )
            )
            + "\n"
        )
        modern = re.sub(
            r"## Task Table\n.*?(?=## Approval and Safety Boundaries)",
            replacement,
            texts[task],
            count=1,
            flags=re.S,
        )
        texts = texts | {task: modern}
        documents = documents | {task: cli.document_from_text(registry, task, modern)}
        return cli, registry, spec, task, documents, texts, schema

    def test_actual_source_snapshot_rejects_unresolved_modern_failure(self) -> None:
        cli, registry, spec, task, documents, texts, schema = (
            self.modern_failure_snapshot()
        )
        findings = cli._completion_document_diagnostics(
            ROOT, registry, (spec,), documents, texts, schema, base_mode="explicit-ref"
        )
        self.assertIn("TASK-EVIDENCE-UNRESOLVED", {item.rule_id for item in findings})
        empty_decisions = texts | {
            task: re.sub(
                r"(?m)^\| \[VAL-LOCAL-QA-\d{3}\]\([^\n]* \| accepted \|[^\n]*\n",
                "",
                texts[task],
            )
        }
        empty_decisions_docs = documents | {
            task: cli.document_from_text(registry, task, empty_decisions[task])
        }
        missing_verdicts = cli._completion_document_diagnostics(
            ROOT,
            registry,
            (spec,),
            empty_decisions_docs,
            empty_decisions,
            schema,
            base_mode="explicit-ref",
        )
        self.assertIn(
            "TASK-ACCEPTANCE-COLUMNS", {item.rule_id for item in missing_verdicts}
        )

    def test_completion_requires_reciprocal_current_plan_successor(self) -> None:
        cli, registry, spec, source, documents, texts, schema = (
            self.modern_failure_snapshot()
        )
        successor = source.with_name("tsk-0002-local-qa-and-release.md")
        source_id, successor_id = "SPEC-0107-TSK-0001", "SPEC-0107-TSK-0002"
        resolved = texts[source].replace(
            "| EVD-TEST-002 | [VAL-LOCAL-QA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test | same source snapshot | PASS | tests/fixture.py | yes | none |",
            "| EVD-TEST-002 | [VAL-LOCAL-QA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test | same source snapshot | PASS | tests/fixture.py | yes | EVD-TEST-001 |",
        )
        source_text = resolved.replace(
            'status: "completed"', 'status: "superseded"', 1
        ).replace(
            'parent_ids: ["SPEC-0107-PLAN-0001"]',
            f'parent_ids: ["SPEC-0107-PLAN-0001"]\nsuperseded_by: "{successor_id}"',
            1,
        )
        successor_text = resolved.replace(
            f'artifact_id: "{source_id}"',
            f'artifact_id: "{successor_id}"',
            1,
        ).replace(
            'parent_ids: ["SPEC-0107-PLAN-0001"]',
            f'parent_ids: ["SPEC-0107-PLAN-0001"]\nsupersedes: "{source_id}"',
            1,
        )
        plan = spec.with_name("plan.md")
        plan_text = (
            texts[plan]
            .replace(source.name, successor.name)
            .replace(source_id, successor_id)
        )
        current_texts = texts | {
            source: source_text,
            successor: successor_text,
            plan: plan_text,
        }
        current_docs = documents | {
            path: cli.document_from_text(registry, path, current_texts[path])
            for path in (source, successor, plan)
        }

        def rules(bodies):
            docs = current_docs | {
                path: cli.document_from_text(registry, path, bodies[path])
                for path in (source, successor, plan)
            }
            return {
                item.rule_id
                for item in cli._completion_document_diagnostics(
                    ROOT,
                    registry,
                    (spec,),
                    docs,
                    bodies,
                    schema,
                    base_mode="explicit-ref",
                )
            }

        self.assertEqual(rules(current_texts), set())
        broken_pair = current_texts | {
            successor: successor_text.replace(
                f'supersedes: "{source_id}"', 'supersedes: "SPEC-0107-TSK-9999"'
            )
        }
        self.assertIn("TASK-DISPOSITION", rules(broken_pair))
        wrong_plan = current_texts | {plan: texts[plan]}
        self.assertIn("TASK-DISPOSITION", rules(wrong_plan))
        missing_acceptance = current_texts | {
            source: source_text.replace(
                "## Criterion Acceptance", "## Missing Criterion Acceptance", 1
            )
        }
        self.assertIn("TASK-DISPOSITION", rules(missing_acceptance))

    def test_not_required_requires_same_package_cancelled_spec_proof(self) -> None:
        cli, registry, spec, task, documents, texts, _schema = (
            self.modern_failure_snapshot()
        )
        criteria = tuple(f"VAL-LOCAL-QA-{index:03d}" for index in range(1, 5))
        scope = ", ".join(criteria)
        spec_cancelled = (
            texts[spec]
            .replace('status: "approved"', 'status: "cancelled"', 1)
            .replace(
                'artifact_id: "SPEC-0107"',
                'artifact_id: "SPEC-0107"\ncancellation:\n'
                '  reason: "Criterion scope withdrawn"\n'
                '  authorization_ref: "approved user scope decision"\n'
                f'  criteria_disposition: "{scope}"',
                1,
            )
        )
        task_cancelled = (
            texts[task]
            .replace('status: "completed"', 'status: "cancelled"', 1)
            .replace(
                'parent_ids: ["SPEC-0107-PLAN-0001"]',
                'parent_ids: ["SPEC-0107-PLAN-0001"]\ncancellation:\n'
                '  reason: "Spec withdrew criteria"\n'
                '  authorization_ref: "SPEC-0107"\n'
                f'  criteria_disposition: "{scope}"',
                1,
            )
            .replace("| accepted | EVD-TEST-", "| not-required | EVD-TEST-")
            .replace(
                "| EVD-TEST-002, EVD-TEST-003, EVD-TEST-004, EVD-TEST-005 |",
                "| Reason: Spec withdrew these criteria; Next owner: platform |",
                1,
            )
        )

        def disposition(spec_text, task_text, plan_text=None):
            bodies = texts | {spec: spec_text, task: task_text}
            if plan_text is not None:
                bodies[spec.with_name("plan.md")] = plan_text
            docs = documents | {
                path: cli.document_from_text(registry, path, text)
                for path, text in bodies.items()
            }
            context = cli._evidence_context(registry, {}, docs, {}, bodies, root=ROOT)
            return context.proposed_documents[task].task_disposition_valid

        self.assertTrue(disposition(spec_cancelled, task_cancelled))
        missing_acceptance = task_cancelled.replace(
            "## Criterion Acceptance", "## Missing Criterion Acceptance", 1
        )
        self.assertFalse(disposition(spec_cancelled, missing_acceptance))
        self.assertFalse(disposition(texts[spec], task_cancelled))
        cancelled_without_proof = texts[spec].replace(
            'status: "approved"', 'status: "cancelled"', 1
        )
        self.assertFalse(disposition(cancelled_without_proof, task_cancelled))
        foreign_spec = spec_cancelled.replace(scope, "VAL-LOCAL-QA-999")
        self.assertFalse(disposition(foreign_spec, task_cancelled))
        for malformed in (
            ", ".join(f"{criterion}-extra" for criterion in criteria),
            ", ".join(f"x-{criterion}" for criterion in criteria),
            ", ".join(f"é{criterion}" for criterion in criteria),
            ", ".join(f"기준{criterion}" for criterion in criteria),
            ", ".join(f"{criterion}é" for criterion in criteria),
            ", ".join(f"{criterion}후속" for criterion in criteria),
        ):
            with self.subTest(malformed=malformed):
                self.assertFalse(
                    disposition(
                        spec_cancelled.replace(scope, malformed), task_cancelled
                    )
                )
                self.assertFalse(
                    disposition(
                        spec_cancelled, task_cancelled.replace(scope, malformed)
                    )
                )
        markdown_scope = ", ".join(
            f"[{criterion}](../spec.md)" for criterion in criteria
        )
        self.assertTrue(
            disposition(
                spec_cancelled.replace(scope, markdown_scope),
                task_cancelled.replace(scope, markdown_scope),
            )
        )
        korean_prose = f"취소한 기준 {scope} 은 철회됨"
        self.assertTrue(
            disposition(
                spec_cancelled.replace(scope, korean_prose),
                task_cancelled.replace(scope, korean_prose),
            )
        )
        foreign_task = task_cancelled.replace(
            'authorization_ref: "SPEC-0107"', 'authorization_ref: "SPEC-9999"'
        )
        self.assertFalse(disposition(spec_cancelled, foreign_task))
        placeholder_reason = task_cancelled.replace(
            'reason: "Spec withdrew criteria"', 'reason: "TBD"'
        )
        self.assertFalse(disposition(spec_cancelled, placeholder_reason))
        plan = spec.with_name("plan.md")
        successor_only = task_cancelled.replace(
            'authorization_ref: "SPEC-0107"', 'authorization_ref: "SPEC-0107-PLAN-0001"'
        )
        successor_plan = texts[plan].replace(task.name, "tsk-9999-other.md")
        self.assertFalse(disposition(texts[spec], successor_only, successor_plan))

    def test_only_closed_spec_package_may_use_approved_parents(self) -> None:
        cli = load_lifecycle_cli()
        registry = load_registry(ROOT)
        unit = next(
            item for item in registry.retention_units if item.name == "spec-package"
        )
        retention = next(
            item for item in registry.retention_classes if item.name == "completed"
        )
        source = PurePosixPath("docs/03.specs/0106-stage99-lifecycle-normalization")
        spec, plan = source / "spec.md", source / "plan.md"
        task = source / "tasks/tsk-0017-example.md"
        documents = {
            spec: LifecycleDocument(spec, "sdlc/spec", "approved"),
            plan: LifecycleDocument(plan, "sdlc/plan", "approved"),
            task: LifecycleDocument(task, "sdlc/task", "completed"),
        }
        self.assertEqual(
            cli._unit_state_gaps(
                registry,
                source,
                retention,
                unit,
                documents,
                approved_completion=True,
            ),
            [],
        )
        self.assertTrue(
            cli._unit_state_gaps(registry, source, retention, unit, documents)
        )
        blocked_documents = documents | {
            task: LifecycleDocument(task, "sdlc/task", "blocked")
        }
        self.assertTrue(
            cli._unit_state_gaps(
                registry,
                source,
                retention,
                unit,
                blocked_documents,
                approved_completion=True,
            )
        )
        self.assertTrue(
            cli._unit_state_gaps(
                registry,
                spec,
                retention,
                None,
                {spec: documents[spec]},
                approved_completion=True,
            )
        )


class ExactLegacyTaskBindingTests(unittest.TestCase):
    def test_only_original_unchanged_completed_task_uses_previous_form(self) -> None:
        registry = load_registry(ROOT)
        path = PurePosixPath(
            "docs/03.specs/0106-stage99-lifecycle-normalization/tasks/"
            "tsk-0016-shared-profile-migration.md"
        )
        text = (ROOT / path).read_text(encoding="utf-8")
        current = classify_path(registry, path)
        self.assertNotEqual(legacy_task_profile(ROOT, path, text, current), current)
        self.assertEqual(legacy_task_profile(ROOT, path, text + "\n", current), current)
        copied = path.with_name("tsk-0999-copied-old-form.md")
        self.assertEqual(legacy_task_profile(ROOT, copied, text, current), current)


class SpecPlanAuthorityTests(unittest.TestCase):
    def test_modern_parent_and_task_creation_must_start_draft(self) -> None:
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
            ("task", ["ready"]),
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

        previous = json.loads(
            subprocess.check_output(
                [
                    "git",
                    "show",
                    "ae93644e7e1137ed66ac243af4156ecea2d9cee4:docs/99.templates/registry.json",
                ],
                cwd=ROOT,
            )
        )
        self.assertNotIn("REGISTRY_LIFECYCLE_DOMAIN", issues(previous))

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


class PriorGenerationEvidenceTests(unittest.TestCase):
    def test_gen9_plan_does_not_require_modern_task_allocation_columns(self) -> None:
        raw = subprocess.check_output(
            [
                "git",
                "show",
                "7fc8829858bdcdf27e3ab93c23e62cb2a84df751:docs/99.templates/registry.json",
            ],
            cwd=ROOT,
        )
        registry = _typed_registry_from_mapping(json.loads(raw))
        path = PurePosixPath("docs/03.specs/0080-adr-0032-retention-pilot/plan.md")
        seed = (
            ROOT
            / "docs/98.archive/completed/03.specs/0080-adr-0032-retention-pilot/plan.md"
        )
        text = seed.read_text(encoding="utf-8").replace(
            'status: "done"', 'status: "completed"', 1
        )
        cli = load_lifecycle_cli()
        document = cli.document_from_text(registry, path, text)
        context = cli._evidence_context(
            registry, {}, {path: document}, {}, {path: text}, root=ROOT
        )
        self.assertEqual(context.task_plan_criteria, {})


if __name__ == "__main__":
    unittest.main()
