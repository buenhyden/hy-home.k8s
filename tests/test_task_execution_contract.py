"""Task execution rows use one registry-owned table and evidence contract."""

from __future__ import annotations

import importlib.util
import json
import contextlib
from dataclasses import replace
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from document_contracts import (  # noqa: E402
    TaskExecution,
    load_registry,
    task_execution_issues,
    _typed_registry_from_mapping,
)
from document_lifecycle import compare_lifecycle, document_from_text  # noqa: E402


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MARKDOWN = load_script("task_execution_markdown", "validate-markdown-profiles.py")
LINKS = load_script("task_execution_links", "validate-links-and-owners.py")
LIFECYCLE_CLI = load_script(
    "task_execution_lifecycle", "validate-document-lifecycle.py"
)
TASK = PurePosixPath(
    "docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0001-example.md"
)
SPEC = TASK.parent.parent / "spec.md"
UPSTREAM = "[VAL-P02-001](../spec.md#success-criteria--verification-plan)"
HEADER = "| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |"
SEPARATOR = "| --- | --- | --- | --- | --- | --- | --- | --- |"
PRE_MIGRATION_COMMIT = "7fc8829858bdcdf27e3ab93c23e62cb2a84df751"


def task_text(status: str, rows: list[str]) -> str:
    return "\n".join(
        [
            "---",
            'title: "Example"',
            'version: "0.1.0"',
            'type: "sdlc/task"',
            f'status: "{status}"',
            'owner: "platform"',
            'updated: "2026-10-04"',
            'layer: "specs"',
            'artifact_id: "SPEC-0106-TSK-0001"',
            'parent_ids: ["SPEC-0106-PLAN-0001"]',
            "---",
            "# Task: Example",
            "## Overview",
            "Example.",
            "## Inputs",
            "[Spec](../spec.md) and [Plan](../plan.md).",
            "## Task Table",
            "### Lifecycle Traceability",
            HEADER,
            SEPARATOR,
            *rows,
            "## Approval and Safety Boundaries",
            "Example.",
            "## Task Evidence",
            "| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            "| EVD-001 | "
            + UPSTREAM
            + " | WORK-001 | Focused test | Synthetic fixture | NOT_RUN | Pending | pending |",
            "## Verification Summary",
            "Example.",
            "",
        ]
    )


def row(
    work_id: str = "WORK-001",
    *,
    criterion: str = UPSTREAM,
    status: str = "frontmatter",
    result: str = "NOT_RUN",
    acceptance: str | None = None,
    evidence: str = "Execution pending",
) -> str:
    return (
        f"| {work_id} | {criterion} | Verify the change | platform | "
        f"{status} | {result} | {acceptance or ('accepted' if result == 'PASS' else 'pending')} | {evidence} |"
    )


class TaskExecutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)
        cls.profile = next(
            profile
            for profile in cls.registry.profiles
            if profile.profile_id == "sdlc/task"
        )

    def rules(self, text: str) -> set[str]:
        return {
            item.rule_id
            for item in MARKDOWN.validate_document_text(
                text, TASK, self.profile, "strict"
            )
        }

    def test_one_task_table_is_bound_for_all_six_states(self) -> None:
        contract = self.profile.body_contract
        self.assertIsNotNone(contract)
        self.assertEqual(contract.section, "Task Table")
        self.assertEqual(contract.table_heading, "Lifecycle Traceability")
        self.assertEqual(
            contract.required_columns,
            (
                "ID",
                "Upstream criterion",
                "Work item",
                "Owner",
                "Status",
                "Result",
                "Acceptance",
                "Evidence",
            ),
        )
        self.assertEqual(
            set(contract.enforced_statuses),
            {"draft", "ready", "in-progress", "blocked"},
        )
        for status in (
            "draft",
            "ready",
            "in-progress",
            "blocked",
            "completed",
            "cancelled",
        ):
            self.assertTrue(
                MARKDOWN._body_contract_is_enforced(
                    TASK, self.profile, status, "registry", ()
                )
            )
        self.assertEqual(self.rules(task_text("draft", [row()])), set())

    def test_status_summary_and_result_are_checked_from_rows(self) -> None:
        self.assertIn(
            "TASK-EXECUTION-SUMMARY",
            self.rules(
                task_text(
                    "ready",
                    [
                        row(status="completed", result="PASS", evidence="test: PASS"),
                        row("WORK-002", status="ready"),
                    ],
                )
            ),
        )
        self.assertIn(
            "TASK-EXECUTION-RESULT",
            self.rules(task_text("completed", [row(result="NOT_RUN")])),
        )

    def test_all_state_execution_remains_strict_in_registry_and_audit(self) -> None:
        for mode in ("registry", "audit"):
            for status in ("completed", "cancelled"):
                with self.subTest(mode=mode, status=status):
                    text = task_text(
                        status,
                        [
                            row(
                                result="INVENTED",
                                evidence="Reason: factual check attempted",
                            )
                        ],
                    )
                    body = text.split("---", 2)[2]
                    rules = {
                        item.rule_id
                        for item in MARKDOWN._body_contract_diagnostics(
                            TASK, self.profile, body, status, mode
                        )
                    }
                    self.assertIn("TASK-EXECUTION-RESULT", rules)
            completed = task_text(
                "completed", [row(result="FAIL", evidence="Observed check FAIL")]
            ).split("---", 2)[2]
            self.assertIn(
                "TASK-EXECUTION-RESULT",
                {
                    item.rule_id
                    for item in MARKDOWN._body_contract_diagnostics(
                        TASK, self.profile, completed, "completed", mode
                    )
                },
            )
            cancelled = task_text(
                "cancelled",
                [
                    row(
                        result="FAIL",
                        evidence="Reason: cancelled after observed check FAIL",
                    )
                ],
            ).split("---", 2)[2]
            self.assertEqual(
                MARKDOWN._body_contract_diagnostics(
                    TASK, self.profile, cancelled, "cancelled", mode
                ),
                [],
            )

    def test_terminal_and_blocked_evidence_cannot_be_placeholders(self) -> None:
        self.assertIn(
            "TASK-EXECUTION-EVIDENCE",
            self.rules(task_text("completed", [row(result="PASS", evidence="TBD")])),
        )
        self.assertIn(
            "TASK-EXECUTION-EVIDENCE",
            self.rules(task_text("blocked", [row(result="DEFER", evidence="Waiting")])),
        )
        self.assertIn(
            "TASK-EXECUTION-EVIDENCE",
            self.rules(task_text("cancelled", [row(result="NOT_RUN", evidence="N/A")])),
        )

    def test_unknown_row_state_and_multi_criterion_cell_are_checked(self) -> None:
        self.assertIn(
            "TASK-EXECUTION-STATUS",
            self.rules(task_text("draft", [row(status="done")])),
        )
        two_links = (
            UPSTREAM + ", [VAL-P02-002](../spec.md#success-criteria--verification-plan)"
        )
        self.assertEqual(
            self.rules(task_text("draft", [row(criterion=two_links)])), set()
        )

    def test_lifecycle_adapter_reuses_bound_table_for_terminal_evidence(self) -> None:
        text = task_text("completed", [row(result="PASS", evidence="TBD")])
        view = LINKS.lifecycle_markdown_evidence(
            TASK, text, self.profile, {TASK: "sdlc/task", SPEC: "sdlc/spec"}
        )
        self.assertFalse(view.task_terminal_evidence_valid)
        self.assertTrue(view.body_rows)
        unbound = replace(
            self.profile,
            body_contract=replace(self.profile.body_contract, task_execution=None),
        )
        view = LINKS.lifecycle_markdown_evidence(
            TASK,
            task_text("completed", [row(result="PASS", evidence="focused test PASS")]),
            unbound,
            {TASK: "sdlc/task", SPEC: "sdlc/spec"},
            registry_generation=10,
        )
        self.assertFalse(view.task_terminal_evidence_valid)

    def test_route_frontmatter_schema_accepts_current_scalar_record(self) -> None:
        route = next(
            profile
            for profile in self.registry.profiles
            if profile.profile_id == "archive/scope-migration"
        )
        schema = json.loads(
            (ROOT / "docs/99.templates/contracts/frontmatter.schema.json").read_text(
                encoding="utf-8"
            )
        )
        text = "\n".join(
            [
                "---",
                'title: "Retired route"',
                'version: "0.1.0"',
                'type: "archive/route"',
                'status: "draft"',
                'owner: "platform"',
                'updated: "2026-10-04"',
                'layer: "archive"',
                'artifact_id: "MIG-9999"',
                'retired_route: "docs/03.specs/9999-example/spec.md"',
                "successor: null",
                'reason: "Retired after reviewed disposition"',
                "---",
                "",
            ]
        )
        diagnostics = MARKDOWN.validate_document_text(
            text,
            PurePosixPath("docs/98.archive/tombstones/9999-example.md"),
            route,
            "strict",
            frontmatter_schema=schema,
        )
        self.assertNotIn("FM-SCHEMA", {item.rule_id for item in diagnostics})
        for successor, rejected in (
            ('"null"', True),
            ('["docs/03.specs/9999-example/spec.md"]', True),
            ('"docs/03.specs/9999-example/spec.md"', False),
        ):
            with self.subTest(successor=successor):
                changed = text.replace("successor: null", f"successor: {successor}")
                rules = {
                    item.rule_id
                    for item in MARKDOWN.validate_document_text(
                        changed,
                        PurePosixPath("docs/98.archive/tombstones/9999-example.md"),
                        route,
                        "strict",
                        frontmatter_schema=schema,
                    )
                }
                self.assertEqual("FM-SCHEMA" in rules, rejected)

    def test_failed_completed_row_is_not_terminal_evidence(self) -> None:
        text = task_text(
            "completed",
            [
                row(status="completed", result="PASS", evidence="unit test passed"),
                row(
                    "WORK-002",
                    status="completed",
                    result="FAIL",
                    evidence="unit test failed",
                ),
            ],
        )
        view = LINKS.lifecycle_markdown_evidence(
            TASK, text, self.profile, {TASK: "sdlc/task", SPEC: "sdlc/spec"}
        )
        self.assertFalse(view.task_terminal_evidence_valid)

    def test_direct_parent_cancellation_and_evidence_table_are_required(self) -> None:
        text = task_text("draft", [row()])
        self.assertIn(
            "PARENT-IDENTITY",
            self.rules(text.replace("SPEC-0106-PLAN-0001", "SPEC-9999-PLAN-0001")),
        )
        self.assertIn(
            "TASK-EVIDENCE-COLUMNS",
            self.rules(
                text.replace("| Evidence | Criteria |", "| Evidence | Criterion |")
            ),
        )
        cancelled = task_text(
            "cancelled", [row(evidence="Reason: optional work withdrawn")]
        )
        self.assertIn("FM-CANCELLATION", self.rules(cancelled))


class V4TaskRowTests(unittest.TestCase):
    """The current eight-column result/acceptance contract has one source row."""

    binding = TaskExecution(
        single_status_marker="frontmatter",
        result_states={
            "draft": ("NOT_RUN",),
            "ready": ("NOT_RUN",),
            "in-progress": ("NOT_RUN", "PASS", "FAIL", "DEFER"),
            "blocked": ("FAIL", "DEFER"),
            "completed": ("PASS", "NOT_APPLICABLE"),
            "cancelled": ("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"),
        },
        summary_rule="task-items-v2",
        acceptance_states=("pending", "accepted", "rejected", "not-required"),
    )

    @staticmethod
    def work(**changes: str) -> dict[str, str]:
        return {
            "ID": "WORK-001",
            "Upstream criterion": UPSTREAM,
            "Work item": "Verify the change",
            "Owner": "platform",
            "Status": "frontmatter",
            "Result": "NOT_RUN",
            "Acceptance": "pending",
            "Evidence": "Execution pending",
        } | changes

    def rules(self, status: str, *rows: dict[str, str]) -> set[str]:
        return {rule for rule, _ in task_execution_issues(rows, status, self.binding)}

    def test_draft_is_valid_and_completed_requires_pass_and_acceptance(self) -> None:
        self.assertEqual(self.rules("draft", self.work()), set())
        self.assertIn(
            "TASK-EXECUTION-ACCEPTANCE",
            self.rules(
                "completed",
                self.work(Result="PASS", Evidence="focused test PASS"),
            ),
        )
        self.assertEqual(
            self.rules(
                "completed",
                self.work(
                    Result="PASS", Acceptance="accepted", Evidence="focused test PASS"
                ),
            ),
            set(),
        )

    def test_not_applicable_cannot_waive_linked_required_criterion(self) -> None:
        self.assertIn(
            "TASK-EXECUTION-ACCEPTANCE",
            self.rules(
                "completed",
                self.work(
                    Result="NOT_APPLICABLE",
                    Acceptance="not-required",
                    Evidence="Criterion omitted by Task",
                ),
            ),
        )

    def test_nonrequired_completed_row_cannot_claim_required_acceptance(self) -> None:
        self.assertIn(
            "TASK-EXECUTION-ACCEPTANCE",
            self.rules(
                "completed",
                self.work(
                    **{
                        "Upstream criterion": "N/A — optional experiment",
                        "Result": "PASS",
                        "Acceptance": "accepted",
                        "Evidence": "No acceptance criterion",
                    }
                ),
            ),
        )

    def test_cancellation_preserves_all_observed_results(self) -> None:
        for result in ("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"):
            with self.subTest(result=result):
                self.assertEqual(
                    self.rules(
                        "cancelled",
                        self.work(
                            **{
                                "Upstream criterion": "N/A — optional experiment",
                                "Result": result,
                                "Acceptance": "not-required",
                                "Evidence": "Reason: optional experiment withdrawn",
                            }
                        ),
                    ),
                    set(),
                )

    def test_mixed_and_remaining_states_derive_header(self) -> None:
        for states, expected in (
            (["completed", "draft"], "in-progress"),
            (["ready", "draft"], "ready"),
            (["completed", "cancelled"], "cancelled"),
            (["blocked", "in-progress"], "blocked"),
        ):
            with self.subTest(states=states):
                rows = [
                    self.work(**{"ID": f"WORK-{index:03d}", "Status": state})
                    for index, state in enumerate(states, 1)
                ]
                summary = {
                    rule
                    for rule, _ in task_execution_issues(rows, expected, self.binding)
                }
                self.assertNotIn("TASK-EXECUTION-SUMMARY", summary)


class CompletionIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="task-completion-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "docs/99.templates", self.root / "docs/99.templates")
        self.spec = SPEC
        self.plan = SPEC.parent / "plan.md"
        self.task = TASK
        self.write(
            self.spec,
            "\n".join(
                [
                    "---",
                    'title: "Spec"',
                    'version: "0.1.0"',
                    'type: "sdlc/spec"',
                    'status: "approved"',
                    'owner: "platform"',
                    'updated: "2026-10-04"',
                    'layer: "specs"',
                    'artifact_id: "SPEC-0106"',
                    "---",
                    "# Spec",
                    "## Success Criteria & Verification Plan",
                    "| Criterion | Acceptance evidence |",
                    "| --- | --- |",
                    "| VAL-P02-001 | Focused test PASS |",
                    "## Traceability",
                    "### Lifecycle Traceability",
                    "| Requirement ID | Spec criterion | Verification method |",
                    "| --- | --- | --- |",
                    "| N/A — approved direct package | VAL-P02-001 | Focused test |",
                    "",
                ]
            ),
        )
        self.write(
            self.plan,
            "\n".join(
                [
                    "---",
                    'title: "Plan"',
                    'version: "0.1.0"',
                    'type: "sdlc/plan"',
                    'status: "approved"',
                    'owner: "platform"',
                    'updated: "2026-10-04"',
                    'layer: "specs"',
                    'artifact_id: "SPEC-0106-PLAN-0001"',
                    'parent_ids: ["SPEC-0106"]',
                    "---",
                    "# Plan",
                    "## Work Breakdown",
                    "### Lifecycle Traceability",
                    "| Work Unit | Criteria | Work | Dependencies | Task | Verification |",
                    "| --- | --- | --- | --- | --- | --- |",
                    "| WORK-001 | [VAL-P02-001](spec.md#success-criteria--verification-plan) | Verify | none | "
                    "[SPEC-0106-TSK-0001](tasks/tsk-0001-example.md) | Focused test |",
                    "",
                ]
            ),
        )
        registry = load_registry(self.root)
        for path, profile_id in ((self.spec, "sdlc/spec"), (self.plan, "sdlc/plan")):
            profile = next(p for p in registry.profiles if p.profile_id == profile_id)
            text = (self.root / path).read_text()
            for heading in profile.headings.required:
                if f"## {heading}\n" not in text:
                    text += f"\n## {heading}\n\nConcrete fixture context.\n"
            self.write(path, text)
        self.write(self.task, task_text("ready", [row()]))
        subprocess.run(["git", "init", "--quiet"], cwd=self.root, check=True)
        self.stage()

    def write(self, path: PurePosixPath, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def stage(self) -> None:
        subprocess.run(
            ["git", "add", "--", "docs/99.templates", "docs/03.specs"],
            cwd=self.root,
            check=True,
        )

    def completion(self) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = LIFECYCLE_CLI.main(
                [
                    "--root",
                    str(self.root),
                    "--mode",
                    "completion",
                    "--include-path",
                    str(self.spec),
                ]
            )
        return result, output.getvalue()

    def commit(self) -> str:
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "fixture",
            ],
            cwd=self.root,
            check=True,
        )
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.root, text=True
        ).strip()

    def test_completion_reads_index_not_worktree_and_reports_identity(self) -> None:
        passed = task_text(
            "completed", [row(result="PASS", evidence="focused unit test PASS")]
        )
        self.write(self.task, passed)
        result, output = self.completion()
        self.assertEqual(result, 1, output)
        self.assertIn("COMPLETION-RESULT", output)
        self.assertIn("INDEX-SNAPSHOT sha256=", output)
        self.stage()
        self.write(self.task, task_text("ready", [row()]))
        result, output = self.completion()
        self.assertEqual(result, 0, output)
        self.assertIn("PASS lifecycle validation mode=completion", output)

    def test_defined_criterion_cannot_disappear_from_spec_traceability(self) -> None:
        text = (self.root / self.spec).read_text(encoding="utf-8")
        text = text.replace(
            "| VAL-P02-001 | Focused test PASS |",
            "| VAL-P02-001 | Focused test PASS |\n| VAL-P02-002 | Another required test |",
        )
        self.write(self.spec, text)
        self.stage()
        result, output = self.completion()
        self.assertEqual(result, 1, output)
        self.assertIn("COMPLETION-TRACE", output)

    def test_authority_drift_rejects_completion(self) -> None:
        authority = self.root / "docs/99.templates/registry.json"
        authority.write_bytes(authority.read_bytes() + b"\n")
        result, output = self.completion()
        self.assertEqual(result, 2, output)
        self.assertIn("AUTHORITY_DRIFT", output)

    def test_required_in_progress_pass_and_cancelled_rows_refuse_handoff(self) -> None:
        for state, result_value in (("in-progress", "PASS"), ("cancelled", "NOT_RUN")):
            with self.subTest(state=state):
                self.write(
                    self.task,
                    task_text(
                        state,
                        [
                            row(
                                result=result_value,
                                evidence="Reason: work remains with platform",
                            )
                        ],
                    ),
                )
                self.stage()
                result, output = self.completion()
                self.assertEqual(result, 1, output)
                self.assertIn("COMPLETION-RESULT", output)

    def test_nonrequired_cancelled_row_does_not_waive_completed_requirement(
        self,
    ) -> None:
        self.write(
            self.task,
            task_text(
                "cancelled",
                [
                    row(
                        status="completed",
                        result="PASS",
                        evidence="focused unit test PASS",
                    ),
                    row(
                        "WORK-002",
                        criterion="N/A — optional experiment outside Spec acceptance",
                        status="cancelled",
                        result="NOT_RUN",
                        evidence="Reason: optional experiment withdrawn",
                    ),
                ],
            ),
        )
        self.write(
            self.task,
            (self.root / self.task)
            .read_text()
            .replace(
                'parent_ids: ["SPEC-0106-PLAN-0001"]',
                'parent_ids: ["SPEC-0106-PLAN-0001"]\ncancellation:\n  reason: optional experiment withdrawn\n  authorization_ref: current fixture approval\n  criteria_disposition: required work completed; optional work excluded',
            ),
        )
        self.stage()
        result, output = self.completion()
        self.assertEqual(result, 0, output)

    def test_every_plan_assigned_task_must_pass_the_same_criterion(self) -> None:
        second = TASK.parent / "tsk-0002-example.md"
        plan = (self.root / self.plan).read_text(encoding="utf-8")
        extra = (
            "| WORK-002 | [VAL-P02-001](spec.md#success-criteria--verification-plan) | Verify | none | "
            "[SPEC-0106-TSK-0002](tasks/tsk-0002-example.md) | Focused test |\n"
        )
        first = next(
            line for line in plan.splitlines() if line.startswith("| WORK-001 |")
        )
        self.write(self.plan, plan.replace(first, first + "\n" + extra.rstrip()))
        self.write(
            self.task,
            task_text(
                "completed", [row(result="PASS", evidence="focused unit test PASS")]
            ),
        )
        self.write(
            second,
            task_text("ready", [row()]).replace(
                'artifact_id: "SPEC-0106-TSK-0001"',
                'artifact_id: "SPEC-0106-TSK-0002"',
            ),
        )
        self.stage()
        result, output = self.completion()
        self.assertEqual(result, 1, output)
        self.assertIn("COMPLETION-RESULT", output)

    def test_one_plan_work_unit_can_assign_multiple_required_criteria(self) -> None:
        spec = (
            (self.root / self.spec)
            .read_text()
            .replace(
                "| VAL-P02-001 | Focused test PASS |",
                "| VAL-P02-001 | Focused test PASS |\n| VAL-P02-002 | Second check |",
            )
            .replace(
                "| N/A — approved direct package | VAL-P02-001 | Focused test |",
                "| N/A — approved direct package | VAL-P02-001 | Focused test |\n| N/A — approved direct package | VAL-P02-002 | Second check |",
            )
        )
        self.write(self.spec, spec)
        criteria = "[VAL-P02-001](spec.md#success-criteria--verification-plan), [VAL-P02-002](spec.md#success-criteria--verification-plan)"
        self.write(
            self.plan,
            (self.root / self.plan)
            .read_text()
            .replace(
                "[VAL-P02-001](spec.md#success-criteria--verification-plan)", criteria
            ),
        )
        upstream = (
            UPSTREAM + ", [VAL-P02-002](../spec.md#success-criteria--verification-plan)"
        )
        self.write(
            self.task,
            task_text(
                "completed",
                [
                    row(
                        criterion=upstream,
                        result="PASS",
                        evidence="Both focused tests PASS",
                    )
                ],
            ),
        )
        self.stage()
        result, output = self.completion()
        self.assertEqual(result, 0, output)

    def test_completion_rejects_current_active_and_invalid_evidence_metadata(
        self,
    ) -> None:
        passed = task_text(
            "completed", [row(result="PASS", evidence="Focused test PASS")]
        )
        for changed_path, changed_text, expected in (
            (
                self.spec,
                (self.root / self.spec)
                .read_text()
                .replace('status: "approved"', 'status: "active"'),
                "FM-STATUS",
            ),
            (
                self.task,
                passed.replace("| Evidence | Criteria |", "| Result | Status |"),
                "TASK-EVIDENCE-COLUMNS",
            ),
            (
                self.task,
                passed.replace(
                    "| NOT_RUN | Pending | pending |",
                    "| NOT_RUN | Pending | accepted |",
                ),
                "TASK-EVIDENCE-ACCEPTANCE",
            ),
            (
                self.task,
                passed.replace(
                    'parent_ids: ["SPEC-0106-PLAN-0001"]',
                    'parent_ids: ["SPEC-9999-PLAN-0001"]',
                ),
                "PARENT-IDENTITY",
            ),
        ):
            with self.subTest(expected=expected):
                original = (self.root / changed_path).read_text()
                self.write(self.task, passed)
                self.write(changed_path, changed_text)
                self.stage()
                result, output = self.completion()
                self.assertEqual(result, 1, output)
                self.assertIn(expected, output)
                self.write(changed_path, original)

    def test_post_binding_history_rejects_intermediate_row_reopen(self) -> None:
        base_text = task_text(
            "in-progress",
            [
                row(status="completed", result="PASS", evidence="focused test PASS"),
                row("WORK-002", status="in-progress"),
            ],
        )
        self.write(self.task, base_text)
        self.stage()
        parent = self.commit()
        reopened = task_text(
            "in-progress",
            [row(status="ready"), row("WORK-002", status="in-progress")],
        )
        self.write(self.task, reopened)
        self.stage()
        commit = self.commit()
        registry = load_registry(self.root)
        self.assertTrue(LIFECYCLE_CLI._committed_task_binding(self.root, commit))
        cache = LIFECYCLE_CLI._CumulativeHistoryCache(self.root, registry)
        findings = LIFECYCLE_CLI._history_event_diagnostics(
            self.root,
            registry,
            self.task,
            parent,
            commit,
            document_from_text(registry, self.task, base_text),
            document_from_text(registry, self.task, reopened),
            cache,
        )
        self.assertIn("TASK-ITEM-EDGE", {item.rule_id for item in findings})


class LifecycleItemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)

    def rules(self, before: str, after: str) -> set[str]:
        base = document_from_text(self.registry, TASK, before)
        proposed = document_from_text(self.registry, TASK, after)
        context = LIFECYCLE_CLI._evidence_context(
            self.registry,
            {TASK: base},
            {TASK: proposed},
            {TASK: before},
            {TASK: after},
        )
        return {
            item.rule_id
            for item in compare_lifecycle(
                self.registry,
                {TASK: base},
                {TASK: proposed},
                base_mode="staged",
                evidence_context=context,
                enforce_task_execution=True,
            )
        }

    def test_deleting_and_reopening_rows_fails_even_when_header_does_not_change(
        self,
    ) -> None:
        base = task_text(
            "in-progress",
            [
                row(status="completed", result="PASS", evidence="focused test PASS"),
                row("WORK-002", status="in-progress"),
            ],
        )
        deleted = task_text("in-progress", [row("WORK-002")])
        reopened = task_text(
            "in-progress",
            [
                row(status="ready"),
                row("WORK-002", status="in-progress"),
            ],
        )
        self.assertIn("TASK-ITEM-DELETE", self.rules(base, deleted))
        self.assertIn("TASK-ITEM-EDGE", self.rules(base, reopened))

    def test_legacy_seven_column_base_preserves_work_ids_without_old_result_reparse(
        self,
    ) -> None:
        old = (
            task_text(
                "completed",
                [
                    row(
                        status="Completed",
                        result="Old prose result",
                        evidence="Prior evidence",
                    ),
                    row(
                        "WORK-002",
                        status="Completed",
                        result="Old prose result",
                        evidence="Prior evidence",
                    ),
                ],
            )
            .replace(SEPARATOR, "| --- | --- | --- | --- | --- | --- | --- |")
            .replace("| Acceptance |", "|")
            .replace("| pending |", "|")
            .replace("### Lifecycle Traceability\n", "")
            .replace(UPSTREAM, "VAL-P02-001")
        )
        current = task_text(
            "completed", [row(result="PASS", evidence="focused test PASS")]
        )
        self.assertIn("TASK-ITEM-DELETE", self.rules(old, current))


class GenerationAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load_registry(ROOT)
        self.base = _typed_registry_from_mapping(
            json.loads(
                subprocess.check_output(
                    [
                        "git",
                        "show",
                        f"{PRE_MIGRATION_COMMIT}:docs/99.templates/registry.json",
                    ],
                    cwd=ROOT,
                )
            )
        )
        self.before, self.after = {}, {}
        for entry in self.registry.migration_admission["entries"]:
            path = PurePosixPath(entry["path"])
            old = subprocess.check_output(
                ["git", "show", f"{PRE_MIGRATION_COMMIT}:{path}"], cwd=ROOT
            ).decode()
            self.before[path] = document_from_text(self.base, path, old)
            self.after[path] = document_from_text(
                self.registry, path, (ROOT / path).read_text()
            )

    def test_actual_nine_to_ten_boundary_and_absent_source(self) -> None:
        admitted = LIFECYCLE_CLI._generation_admission_paths(
            self.registry, self.base, self.before, self.after
        )
        self.assertEqual(admitted, frozenset(self.before))
        path = next(iter(self.before))
        self.assertNotIn(
            path,
            LIFECYCLE_CLI._generation_admission_paths(
                self.registry,
                self.base,
                {p: d for p, d in self.before.items() if p != path},
                self.after,
            ),
        )
        self.assertEqual(
            LIFECYCLE_CLI._generation_admission_paths(
                self.registry, self.registry, self.before, self.after
            ),
            frozenset(),
        )

    def test_unknown_reference_and_status_fail_closed(self) -> None:
        for change in ("reference", "status"):
            declaration = json.loads(json.dumps(self.registry.migration_admission))
            if change == "reference":
                declaration["spec_ref"] = "docs/03.specs/9999-missing/spec.md"
            else:
                declaration["entries"][0]["target_status"] = "INVENTED"
            with (
                self.subTest(change=change),
                self.assertRaises(LIFECYCLE_CLI.InvocationError),
            ):
                LIFECYCLE_CLI._generation_admission_paths(
                    replace(self.registry, migration_admission=declaration),
                    self.base,
                    self.before,
                    self.after,
                )

    def test_exact_git_boundary_replay_and_later_completion(self) -> None:
        with tempfile.TemporaryDirectory(prefix="generation-history-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "docs/99.templates", root / "docs/99.templates")
            registry_path = root / "docs/99.templates/registry.json"
            registry_path.write_bytes(
                subprocess.check_output(
                    [
                        "git",
                        "show",
                        f"{PRE_MIGRATION_COMMIT}:docs/99.templates/registry.json",
                    ],
                    cwd=ROOT,
                )
            )
            for markdown in (root / "docs/99.templates").rglob("*.md"):
                markdown.unlink()
            copy_sources = (
                PurePosixPath(
                    "docs/98.archive/completed/03.specs/0063-governance-invariant-consolidation/spec.md"
                ),
                PurePosixPath(
                    "docs/98.archive/completed/03.specs/0091-readme-navigation-contract/tasks/tsk-0001-converge-readme-navigation.md"
                ),
                PurePosixPath(
                    "docs/03.specs/0105-authority-and-safe-authoring/plan.md"
                ),
            )
            for source in copy_sources:
                target = root / source
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(
                    subprocess.check_output(
                        ["git", "show", f"{PRE_MIGRATION_COMMIT}:{source}"], cwd=ROOT
                    )
                )
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)

            def commit() -> str:
                subprocess.run(["git", "add", "--all"], cwd=root, check=True)
                subprocess.run(
                    [
                        "git",
                        "-c",
                        "user.name=Fixture",
                        "-c",
                        "user.email=fixture@example.invalid",
                        "commit",
                        "--quiet",
                        "-m",
                        "fixture",
                    ],
                    cwd=root,
                    check=True,
                )
                return subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=root, text=True
                ).strip()

            absent = commit()
            for markdown in (ROOT / "docs/99.templates").rglob("*.md"):
                target = root / markdown.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(markdown.read_bytes())
            for path in self.before:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(
                    subprocess.check_output(
                        ["git", "show", f"{PRE_MIGRATION_COMMIT}:{path}"], cwd=ROOT
                    )
                )
            intake = commit()
            registry_path.write_bytes(
                (ROOT / "docs/99.templates/registry.json").read_bytes()
            )
            for path in self.after:
                (root / path).write_bytes((ROOT / path).read_bytes())
            subprocess.run(["git", "add", "--all"], cwd=root, check=True)
            findings = LIFECYCLE_CLI._evaluate_comparison(
                root,
                self.registry,
                mode="staged",
                from_ref=None,
                base_ref=None,
                to_ref=None,
            )
            self.assertEqual(
                findings,
                (),
                [LIFECYCLE_CLI._format_diagnostic(item) for item in findings],
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                result = LIFECYCLE_CLI.main(["--root", str(root), "--mode", "staged"])
            self.assertEqual(result, 0, output.getvalue())
            self.assertIn("PASS lifecycle validation mode=staged", output.getvalue())
            migration = commit()
            cache = LIFECYCLE_CLI._CumulativeHistoryCache(root, self.registry)
            for path in (SPEC, self.registry.migration_admission["task_ref"]):
                path = PurePosixPath(path)
                findings = LIFECYCLE_CLI._history_event_diagnostics(
                    root,
                    self.registry,
                    path,
                    intake,
                    migration,
                    cache._snapshot(intake)[0][path],
                    cache._snapshot(migration)[0][path],
                    cache,
                )
                self.assertEqual(
                    findings,
                    (),
                    [LIFECYCLE_CLI._format_diagnostic(item) for item in findings],
                )
            text = (
                (root / SPEC)
                .read_text()
                .replace('status: "in-progress"', 'status: "completed"', 1)
            )
            (root / SPEC).write_text(text)
            completed = commit()
            for before_commit, after_commit in (
                (absent, intake),
                (migration, completed),
            ):
                findings = LIFECYCLE_CLI._history_event_diagnostics(
                    root,
                    self.registry,
                    SPEC,
                    before_commit,
                    after_commit,
                    cache._snapshot(before_commit)[0].get(SPEC),
                    cache._snapshot(after_commit)[0][SPEC],
                    cache,
                )
                self.assertEqual(
                    findings,
                    (),
                    [LIFECYCLE_CLI._format_diagnostic(item) for item in findings],
                )
            self.assertFalse(
                LIFECYCLE_CLI._history_proves_cumulative_create(
                    root, self.registry, SPEC, absent, completed
                )
            )
            task_path = PurePosixPath(self.registry.migration_admission["task_ref"])
            self.assertFalse(
                LIFECYCLE_CLI._history_proves_cumulative_create(
                    root, self.registry, task_path, absent, completed
                )
            )
            findings = LIFECYCLE_CLI._evaluate_comparison(
                root,
                self.registry,
                mode="explicit-ref",
                from_ref=absent,
                to_ref=completed,
                include_paths=(SPEC, SPEC.parent / "plan.md", task_path),
            )
            package_paths = {SPEC, SPEC.parent / "plan.md", task_path}
            package_findings = tuple(
                item for item in findings if item.path in package_paths
            )
            self.assertEqual(
                package_findings,
                (),
                [LIFECYCLE_CLI._format_diagnostic(item) for item in package_findings],
            )

    def test_terminal_reopen_is_never_a_generation_admission(self) -> None:
        path = SPEC
        old = replace(self.before[path], status="completed")
        new = replace(self.after[path], status="ready")
        declaration = json.loads(json.dumps(self.registry.migration_admission))
        declaration["entries"] = [
            {
                "path": str(path),
                "source_profile": "sdlc/spec",
                "source_status": "completed",
                "target_profile": "sdlc/task",
                "target_status": "ready",
            }
        ]
        new = replace(new, profile_id="sdlc/task")
        with self.assertRaises(LIFECYCLE_CLI.InvocationError):
            LIFECYCLE_CLI._generation_admission_paths(
                replace(self.registry, migration_admission=declaration),
                self.base,
                self.before | {path: old},
                self.after | {path: new},
            )


if __name__ == "__main__":
    unittest.main()
