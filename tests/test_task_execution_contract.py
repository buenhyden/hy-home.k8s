"""Task execution rows use one registry-owned table and evidence contract."""

from __future__ import annotations

import importlib.util
import contextlib
import dataclasses
from dataclasses import replace
import io
import json
import re
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
    HeadingContract,
    TaskExecution,
    load_registry,
    task_contract_issues,
    task_execution_issues,
)
from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    compare_lifecycle,
    document_from_text,
)


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
UPSTREAM = "[VAL-P02-001](../spec.md#criteria)"
HEADER = "| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |"
SEPARATOR = "| --- | --- | --- | --- | --- | --- | --- |"
OLD_CHECK_HEADER = "| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |"
CHECK_HEADER = "| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |"
CHECK_SEPARATOR = "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
RESULTS = ("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE")


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip("|").split(" | ")]


def task_text(status: str, rows: list[str], *, old_form: bool = False) -> str:
    """Render one Task whose checks and verdicts follow its rows.

    The default is the SPEC-0203 form; `old_form` renders the seven-heading layout
    and the old evidence header that a registry from before the form binds.
    """

    checks, decisions, decided = [], [], set()
    for number, line in enumerate(rows, 1):
        work, criterion, _, _, state, result, _ = _cells(line)
        outcome = result if result in RESULTS else "NOT_RUN"
        linked = re.findall(r"\[VAL-[^\]]+\]\([^)]*\)", criterion)
        checks.append(
            f"| EVD-{number:03d} | {', '.join(linked) or criterion} | {work} | "
            f"Focused test | Synthetic fixture | {outcome} | "
            f"{'tests/fixture.py' if outcome in ('PASS', 'FAIL') else 'Pending'} | "
            "yes | none |"
        )
        for link in linked:
            if link not in decided:
                decided.add(link)
                accepted = "completed" in (status, state) and outcome == "PASS"
                decisions.append(
                    f"| {link} | {'accepted' if accepted else 'pending'} | "
                    f"{f'EVD-{number:03d}' if accepted else 'none'} | Fixture | platform |"
                )
    front = [
        "---",
        'title: "Example"',
        'version: "0.1.0"',
        'type: "sdlc/task"',
        f'status: "{status}"',
        'owner: "platform"',
        'updated: "2026-10-04"',
        'artifact_id: "SPEC-0106-TSK-0001"',
        'parent_ids: ["SPEC-0106-PLAN-0001"]',
        "---",
        "# Task: Example",
    ]
    decision_table = [
        "| Criterion | Acceptance | Evidence | Disposition | Current owner |",
        "| --- | --- | --- | --- | --- |",
        *decisions,
    ]
    if old_form:
        return "\n".join(
            [
                *front,
                "## Overview",
                "Example.",
                "## Inputs",
                "[Spec](../spec.md) and [Plan](../plan.md).",
                "## Task Table",
                "### Lifecycle Traceability",
                HEADER,
                SEPARATOR,
                *rows,
                "## Task Evidence",
                OLD_CHECK_HEADER,
                CHECK_SEPARATOR,
                *checks,
                "## Criterion Acceptance",
                *decision_table,
                "## Approval and Safety Boundaries",
                "Example.",
                "## Verification Summary",
                "Example.",
                "",
            ]
        )
    return "\n".join(
        [
            *front,
            "## Scope",
            "### Objective and Parent",
            "Example.",
            "### Inputs and Authority",
            "[Spec](../spec.md) and [Plan](../plan.md).",
            "## Execution Log",
            "### Work Performed",
            "The rows below record the work.",
            "### Blockers and Decisions",
            "No blocker is recorded.",
            "### Lifecycle Traceability",
            HEADER,
            SEPARATOR,
            *rows,
            "## Verification Evidence",
            "### Results",
            CHECK_HEADER,
            CHECK_SEPARATOR,
            *checks,
            "### Resolution Links",
            "The Resolves column names the row each PASS row closes.",
            "## Acceptance Decision",
            "### Criterion Decisions",
            *decision_table,
            "### Remaining Conditions",
            "No condition remains.",
            "## Handoff",
            "### Promotion Receipt",
            "No durable contract is promoted.",
            "### Next Owner",
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
    evidence: str = "Execution pending",
) -> str:
    return (
        f"| {work_id} | {criterion} | Verify the change | platform | "
        f"{status} | {result} | {evidence} |"
    )


def _frontmatter(kind: str, artifact: str, extra: str = "") -> list[str]:
    return [
        "---",
        f'title: "{kind.title()}"',
        'version: "0.1.0"',
        f'type: "sdlc/{kind}"',
        'status: "approved"',
        'owner: "platform"',
        'updated: "2026-10-04"',
        f'artifact_id: "{artifact}"',
        *([extra] if extra else []),
        "---",
    ]


def form_spec_text() -> str:
    """A Spec in the COMMON-DOC-FORM-1 shape (SPEC-0200)."""

    def block(title: str, *children: str) -> list[str]:
        return [f"## {title}"] + [
            line
            for child in children
            for line in (f"### {child}", "Concrete fixture text.")
        ]

    return "\n".join(
        [
            *_frontmatter("spec", "SPEC-0106"),
            "# Spec",
            *block("Overview", "Intent", "Owning Requirements"),
            *block("Scope", "In Scope", "Non-goals"),
            *block("Behavior Contract", "Normal Behavior", "Failure and Edge Cases"),
            "## Acceptance Criteria",
            "### Criteria",
            "| Criterion ID | Expected Result |",
            "| --- | --- |",
            "| VAL-P02-001 | Focused test PASS |",
            "### Evidence Requirements",
            "Concrete fixture text.",
            *block("References", "Normative and Evidence", "Historical and Navigation"),
            "### Lifecycle Traceability",
            "| Requirement ID | Spec criterion | Architecture | Verification method |",
            "| --- | --- | --- | --- |",
            "| N/A — approved direct package | VAL-P02-001 | None apply: fixture | Focused test |",
            "",
        ]
    )


def form_plan_text() -> str:
    """A Plan in the COMMON-DOC-FORM-1 shape (SPEC-0200)."""

    def block(title: str, *children: str) -> list[str]:
        return [f"## {title}"] + [
            line
            for child in children
            for line in (f"### {child}", "Concrete fixture text.")
        ]

    return "\n".join(
        [
            *_frontmatter("plan", "SPEC-0106-PLAN-0001", 'parent_ids: ["SPEC-0106"]'),
            "# Plan",
            "## Overview",
            "### Goal and Boundary",
            "Concrete fixture goal.",
            "#### Global Constraints",
            "Keep the approved [Spec](spec.md#scope) parent contract.",
            "### Assumptions",
            "Concrete fixture text.",
            *block("Dependencies", "Prerequisites", "Dependency Order"),
            "## Implementation Strategy",
            "### Work Breakdown",
            "| Work Unit | Criteria | Work | Dependencies | Task | Verification |",
            "| --- | --- | --- | --- | --- | --- |",
            "| WORK-001 | [VAL-P02-001](spec.md#criteria) | Verify | none | "
            "[SPEC-0106-TSK-0001](tasks/tsk-0001-example.md) | Focused test |",
            "### Change and Rollback",
            "Concrete fixture text.",
            *block("Verification Plan", "Verification Matrix", "Stage Placement"),
            *block("Risks", "Risks and Mitigations", "Escalation"),
            "## Promotion Map",
            "### Durable Meaning",
            "Concrete fixture text.",
            "### Owner and Receipt",
            "| Promotion ID | Target Owner | Acceptance | Evidence |",
            "| --- | --- | --- | --- |",
            "| none | none | none | No durable contract was introduced |",
            "",
        ]
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
        """Profile findings plus the Task row, check and verdict contract."""

        found = {
            item.rule_id
            for item in MARKDOWN.validate_document_text(
                text, TASK, self.profile, "strict"
            )
        }
        binding = self.profile.body_contract.task_execution
        state = re.search(r'(?m)^status: "([^"]+)"$', text)
        work = LINKS._body_contract_rows(text, self.profile)
        checks = LINKS.task_evidence_rows(text, binding)
        decisions = LINKS.task_acceptance_rows(text, binding)
        if work and checks is not None and decisions is not None:
            found |= {
                rule
                for rule, _ in task_contract_issues(
                    work, checks, decisions, state.group(1) if state else "", binding
                )
            }
        return found

    def test_one_task_table_is_bound_for_all_six_states(self) -> None:
        contract = self.profile.body_contract
        self.assertIsNotNone(contract)
        self.assertEqual(contract.section, "Execution Log")
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

    def test_all_state_execution_remains_strict(self) -> None:
        for status in ("completed", "cancelled"):
            with self.subTest(status=status):
                self.assertIn(
                    "TASK-EXECUTION-RESULT",
                    self.rules(
                        task_text(
                            status,
                            [
                                row(
                                    result="INVENTED",
                                    evidence="Reason: factual check attempted",
                                )
                            ],
                        )
                    ),
                )
        self.assertIn(
            "TASK-EXECUTION-RESULT",
            self.rules(
                task_text(
                    "completed", [row(result="FAIL", evidence="Observed check FAIL")]
                )
            ),
        )
        self.assertNotIn(
            "TASK-EXECUTION-RESULT",
            self.rules(
                task_text(
                    "cancelled",
                    [
                        row(
                            result="FAIL",
                            evidence="Reason: cancelled after observed check FAIL",
                        )
                    ],
                )
            ),
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
        two_links = UPSTREAM + ", [VAL-P02-002](../spec.md#criteria)"
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
        )
        self.assertFalse(view.task_terminal_evidence_valid)

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
                text.replace(
                    "| Evidence ID | Consumer |", "| Evidence ID | Criterion |"
                )
            ),
        )
        cancelled = task_text(
            "cancelled", [row(evidence="Reason: optional work withdrawn")]
        )
        self.assertIn("FM-CANCELLATION", self.rules(cancelled))


class V4TaskRowTests(unittest.TestCase):
    """The current seven-column Task row; verdicts live in Acceptance Decision."""

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
        criterion_acceptance_section="Acceptance Decision",
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
            "Evidence": "Execution pending",
        } | changes

    def rules(self, status: str, *rows: dict[str, str]) -> set[str]:
        return {rule for rule, _ in task_execution_issues(rows, status, self.binding)}

    def test_draft_is_valid_and_completed_linked_row_requires_pass(self) -> None:
        self.assertEqual(self.rules("draft", self.work()), set())
        self.assertEqual(
            self.rules(
                "completed", self.work(Result="PASS", Evidence="focused test PASS")
            ),
            set(),
        )

    def test_not_applicable_cannot_waive_linked_required_criterion(self) -> None:
        self.assertIn(
            "TASK-EXECUTION-RESULT",
            self.rules(
                "completed",
                self.work(
                    Result="NOT_APPLICABLE", Evidence="Criterion omitted by Task"
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
        shutil.copytree(
            ROOT / "docs/99.templates",
            self.root / "docs/99.templates",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        # A TemplateDefinition names consumer paths outside Stage 99 and the
        # registry check requires them to exist.
        registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        for profile in registry["profiles"]:
            for named in profile.get("template_definition", {}).get(
                "consumer_paths", ()
            ):
                target = self.root / named
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / named, target)
        self.spec = SPEC
        self.plan = SPEC.parent / "plan.md"
        self.task = TASK
        self.write(self.spec, form_spec_text())
        self.write(self.plan, form_plan_text())
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

    def test_every_plan_assigned_task_must_pass_the_same_criterion(self) -> None:
        second = TASK.parent / "tsk-0002-example.md"
        plan = (self.root / self.plan).read_text(encoding="utf-8")
        extra = (
            "| WORK-002 | [VAL-P02-001](spec.md#criteria) | Verify | none | "
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
                "| N/A — approved direct package | VAL-P02-001 | None apply: fixture | Focused test |",
                "| N/A — approved direct package | VAL-P02-001 | None apply: fixture | Focused test |\n| N/A — approved direct package | VAL-P02-002 | None apply: fixture | Second check |",
            )
        )
        self.write(self.spec, spec)
        criteria = "[VAL-P02-001](spec.md#criteria), [VAL-P02-002](spec.md#criteria)"
        self.write(
            self.plan,
            (self.root / self.plan)
            .read_text()
            .replace("[VAL-P02-001](spec.md#criteria)", criteria),
        )
        upstream = UPSTREAM + ", [VAL-P02-002](../spec.md#criteria)"
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
                passed.replace("| Evidence ID | Consumer |", "| Result | Status |"),
                "TASK-EVIDENCE-COLUMNS",
            ),
            (
                self.task,
                passed.replace("| accepted |", "| bogus |"),
                "TASK-ACCEPTANCE-STATE",
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


class AdoptedExecutionParentTests(unittest.TestCase):
    """Current Plan/Task authority is checked on actual changed snapshots."""

    package = PurePosixPath("docs/03.specs/0900-approved-parent-fixture")
    spec = package / "spec.md"
    plan = package / "plan.md"
    task = package / "tasks/tsk-0001-fixture.md"
    CONSTRAINTS = "Keep the approved [Spec](spec.md#scope) parent contract.\n"
    NONE_ROW = "| none | none | none | No durable contract was introduced |"

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)

    def spec_text(self, status: str = "approved") -> str:
        return (
            "---\n"
            'title: "Fixture Spec"\nversion: "0.1.0"\n'
            f'type: "sdlc/spec"\nstatus: "{status}"\n'
            'owner: "platform"\nupdated: "2026-10-16"\n'
            'artifact_id: "SPEC-0900"\n'
            "---\n# Spec\n"
        )

    def plan_text(self, status: str = "approved") -> str:
        return (
            "---\n"
            'title: "Fixture Plan"\nversion: "0.1.0"\n'
            f'type: "sdlc/plan"\nstatus: "{status}"\n'
            'owner: "platform"\nupdated: "2026-10-16"\n'
            'artifact_id: "SPEC-0900-PLAN-0001"\n'
            'parent_ids: ["SPEC-0900"]\n'
            "---\n# Plan\n"
            "## Overview\n"
            "### Goal and Boundary\n"
            "The fixture goal and its boundary.\n"
            "#### Global Constraints\n"
            f"{self.CONSTRAINTS}"
            "### Assumptions\n"
            "The fixture assumptions.\n"
            "## Promotion Map\n"
            "### Durable Meaning\n"
            "Each row of the table below names one durable contract.\n"
            "### Owner and Receipt\n"
            "| Promotion ID | Target Owner | Acceptance | Evidence |\n"
            "| --- | --- | --- | --- |\n"
            "| none | none | none | No durable contract was introduced |\n"
        )

    def task_text(
        self,
        status: str = "ready",
        parent_id: str = "SPEC-0900-PLAN-0001",
        row_status: str = "frontmatter",
    ) -> str:
        return (
            "---\n"
            'title: "Fixture Task"\nversion: "0.1.0"\n'
            f'type: "sdlc/task"\nstatus: "{status}"\n'
            'owner: "platform"\nupdated: "2026-10-16"\n'
            'artifact_id: "SPEC-0900-TSK-0001"\n'
            f'parent_ids: ["{parent_id}"]\n'
            "---\n# Task\n"
            "## Execution Log\n### Lifecycle Traceability\n"
            "| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            f"| WORK-001 | [VAL-P02-001](../spec.md) | Verify | platform | {row_status} | {'PASS' if status == 'completed' else 'NOT_RUN'} | Fixture |\n"
        )

    def rules(
        self,
        *,
        base: dict[PurePosixPath, str] | None = None,
        proposed: dict[PurePosixPath, str],
        classified: dict[PurePosixPath, LifecycleDocument] | None = None,
    ) -> set[str]:
        before = base or {}
        fixed = classified or {}
        base_docs = {
            path: fixed.get(path) or document_from_text(self.registry, path, text)
            for path, text in before.items()
        }
        proposed_docs = {
            path: fixed.get(path) or document_from_text(self.registry, path, text)
            for path, text in proposed.items()
        }
        context = LIFECYCLE_CLI._evidence_context(
            self.registry, base_docs, proposed_docs, before, proposed
        )
        return {
            finding.rule_id
            for finding in compare_lifecycle(
                self.registry,
                base_docs,
                proposed_docs,
                base_mode="staged",
                evidence_context=context,
                enforce_task_execution=True,
            )
        }

    def test_changed_plan_requires_constraints_and_promotion_owner(self) -> None:
        plan = self.plan_text()
        base = {self.spec: self.spec_text(), self.plan: plan}
        bad = (
            (
                plan.replace(
                    "#### Global Constraints\n" + self.CONSTRAINTS,
                    "",
                ),
                "PLAN-GLOBAL-CONSTRAINTS",
            ),
            (
                plan.replace("### Owner and Receipt\n", "### Other\n"),
                "PLAN-PROMOTION",
            ),
            (
                plan.replace(self.NONE_ROW, "| | | | |"),
                "PLAN-PROMOTION",
            ),
            (
                plan.replace(
                    self.NONE_ROW,
                    "| Shared lifecycle | [old Task](tasks/tsk-0001-fixture.md) | done | done |",
                ),
                "PLAN-PROMOTION",
            ),
            (
                plan.replace(self.NONE_ROW, "| none | none | none | none |"),
                "PLAN-PROMOTION",
            ),
            (
                plan.replace(
                    "| Promotion ID | Target Owner | Acceptance | Evidence |\n"
                    "| --- | --- | --- | --- |\n" + self.NONE_ROW,
                    "| Durable contract | Promoted to | Where |\n"
                    "| --- | --- | --- |\n"
                    "| none | none | No durable contract was introduced |",
                ),
                "PLAN-PROMOTION",
            ),
            (
                plan.replace(
                    "No durable contract was introduced",
                    "No durable contract introduced",
                ),
                "PLAN-PROMOTION",
            ),
            (
                plan.replace("[Spec](spec.md#scope)", "Spec"),
                "PLAN-GLOBAL-CONSTRAINTS",
            ),
        )
        for changed, rule in bad:
            with self.subTest(rule=rule):
                proposed = {**base, self.plan: changed}
                self.assertIn(rule, self.rules(base=base, proposed=proposed))
        completed_without_receipt = self.plan_text("completed").replace(
            "### Owner and Receipt\n", "### Other\n"
        )
        self.assertIn(
            "PLAN-PROMOTION",
            self.rules(
                base=base, proposed={**base, self.plan: completed_without_receipt}
            ),
        )
        self.assertNotIn("PLAN-PROMOTION", self.rules(base=base, proposed=base))
        with_prompt = plan.replace(
            "#### Global Constraints\n",
            "#### Global Constraints\n<!-- Author prompt: link the Spec -->\n",
        )
        self.assertNotIn(
            "PLAN-GLOBAL-CONSTRAINTS",
            self.rules(base=base, proposed={**base, self.plan: with_prompt}),
        )

    def test_promotion_requires_current_owner_and_sole_none_decision(self) -> None:
        owner_path = PurePosixPath(".agents/governance/document-lifecycle.md")
        owner_text = (ROOT / owner_path).read_text(encoding="utf-8")
        plan = self.plan_text()
        valid_row = (
            "| Lifecycle contract | "
            "[current owner](../../../.agents/governance/document-lifecycle.md) "
            "| The sentence is in force | `Current Contract` |"
        )
        current = plan.replace(self.NONE_ROW, valid_row)
        base = {self.spec: self.spec_text(), self.plan: plan, owner_path: owner_text}
        self.assertNotIn(
            "PLAN-PROMOTION",
            self.rules(base=base, proposed={**base, self.plan: current}),
        )
        member_location = current.replace(
            "`Current Contract` |",
            "Registry member delegated by Current Contract |",
        )
        self.assertNotIn(
            "PLAN-PROMOTION",
            self.rules(base=base, proposed={**base, self.plan: member_location}),
        )
        for bad in (
            current + self.NONE_ROW + "\n",
            current.replace("`Current Contract` |", " |"),
            current.replace("| The sentence is in force |", "| |"),
            current.replace("| The sentence is in force |", "| pending |"),
            current
            + "\n| Promotion ID | Target Owner | Acceptance | Evidence |\n"
            + "| --- | --- | --- | --- |\n"
            + "| Other | [current owner](../../../.agents/governance/document-lifecycle.md) | Done | `Current Contract` |\n",
            current.replace(
                "../../../.agents/governance/document-lifecycle.md",
                "tasks/tsk-0001-fixture.md",
            ),
        ):
            with self.subTest(bad=bad[-90:]):
                self.assertIn(
                    "PLAN-PROMOTION",
                    self.rules(base=base, proposed={**base, self.plan: bad}),
                )

    def test_promotion_refuses_retired_stage_00_owner(self) -> None:
        # No profile covers docs/00.agent-governance, so classify the owner by hand
        # as an approved document and show the owner path alone is refused.
        owner_path = PurePosixPath("docs/00.agent-governance/policies/quality.md")
        owner = LifecycleDocument(
            path=owner_path,
            profile_id="governance/rule",
            status="active",
        )
        plan = self.plan_text()
        retired = plan.replace(
            self.NONE_ROW,
            "| Lifecycle contract | "
            "[retired owner](../../../docs/00.agent-governance/policies/quality.md) "
            "| The sentence is in force | `Current Contract` |",
        )
        base = {self.spec: self.spec_text(), self.plan: plan, owner_path: "# owner\n"}
        self.assertIn(
            "PLAN-PROMOTION",
            self.rules(
                base=base,
                proposed={**base, self.plan: retired},
                classified={owner_path: owner},
            ),
        )

    def test_active_task_needs_approved_typed_parents(self) -> None:
        spec = self.spec_text()
        plan = self.plan_text()
        valid = {self.spec: spec, self.plan: plan, self.task: self.task_text()}
        self.assertNotIn("TASK-PARENT-APPROVAL", self.rules(proposed=valid))
        for change in (
            {self.plan: self.plan_text("in-review")},
            {self.spec: self.spec_text("in-review")},
            {self.plan: self.plan_text("in-progress")},
            {self.spec: self.spec_text("in-progress")},
            {self.task: self.task_text(parent_id="SPEC-9999-PLAN-0001")},
        ):
            with self.subTest(change=change):
                self.assertIn(
                    "TASK-PARENT-APPROVAL", self.rules(proposed={**valid, **change})
                )
        blocked = {
            **valid,
            self.plan: self.plan_text("in-review"),
            self.task: self.task_text("blocked"),
        }
        self.assertNotIn("TASK-PARENT-APPROVAL", self.rules(proposed=blocked))
        working_blocked = {
            **blocked,
            self.task: self.task_text("blocked", row_status="in-progress"),
        }
        self.assertIn("TASK-PARENT-APPROVAL", self.rules(proposed=working_blocked))
        evidence_blocked = {
            **blocked,
            self.task: self.task_text("blocked")
            + "## Verification Evidence\n### Results\n"
            + "| Evidence ID | Result |\n| --- | --- |\n| EVD-001 | PASS |\n",
        }
        self.assertIn("TASK-PARENT-APPROVAL", self.rules(proposed=evidence_blocked))
        self.assertNotIn(
            "TASK-PARENT-APPROVAL",
            self.rules(
                base=valid, proposed={**valid, self.plan: self.plan_text("in-review")}
            ),
        )

    def test_exact_completed_parent_extension_keeps_historical_authority(self) -> None:
        base = {
            self.spec: self.spec_text("completed"),
            self.plan: self.plan_text("completed"),
        }
        proposed = {**base, self.task: self.task_text()}
        self.assertIn("TASK-PARENT-APPROVAL", self.rules(base=base, proposed=proposed))
        planted = {
            **base,
            self.task: self.task_text("blocked", row_status="blocked"),
        }
        self.assertEqual(self.rules(base=base, proposed=planted), set())
        resumed = {
            **planted,
            self.task: self.task_text("in-progress", row_status="in-progress"),
        }
        self.assertIn(
            "TASK-PARENT-APPROVAL", self.rules(base=planted, proposed=resumed)
        )
        old_task = self.task_text("completed", row_status="completed")
        prior_execution = {**base, self.task: old_task}
        self.assertNotIn(
            "TASK-PARENT-APPROVAL",
            self.rules(
                base=prior_execution,
                proposed={
                    **prior_execution,
                    self.task: old_task + "\n## Note\nSame work.",
                },
            ),
        )
        added_work = old_task.replace(
            "| WORK-001 |",
            "| WORK-002 | [VAL-P02-002](../spec.md) | New work | platform | ready | NOT_RUN | Fixture |\n| WORK-001 |",
            1,
        )
        self.assertIn(
            "TASK-PARENT-APPROVAL",
            self.rules(
                base=prior_execution,
                proposed={**prior_execution, self.task: added_work},
            ),
        )
        changed_work = old_task.replace("| Verify |", "| New obligation |", 1)
        self.assertIn(
            "TASK-PARENT-APPROVAL",
            self.rules(
                base=prior_execution,
                proposed={**prior_execution, self.task: changed_work},
            ),
        )
        self.assertIn(
            "TASK-PARENT-APPROVAL",
            self.rules(
                base=base,
                proposed={
                    **proposed,
                    self.plan: self.plan_text("completed") + "\nchanged",
                },
            ),
        )

    # SPEC-0200 (W03-H10, W03-H24): the Plan and Task rules read the registry shape.
    OLD_CONSTRAINTS = "Keep the approved [Spec](spec.md#scope) parent contract.\n"
    OLD_ROW = "| none | none | No durable contract was introduced |"

    def old_plan_text(self) -> str:
        return (
            self.plan_text().split("## Overview\n", 1)[0]
            + "## Overview\nThe fixture.\n"
            + "## Global Constraints\n"
            + self.OLD_CONSTRAINTS
            + "## Promotion\n"
            + "| Durable contract | Promoted to | Where |\n"
            + "| --- | --- | --- |\n"
            + self.OLD_ROW
            + "\n"
        )

    def registry_with(self, *, drop_sections: tuple[str, ...] = ()):
        """The repository registry whose Plan form lacks the named sections."""

        def prune(sections):
            return tuple(
                dataclasses.replace(item, children=prune(item.children))
                for item in sections
                if item.section_id not in drop_sections
            )

        forms = tuple(
            dataclasses.replace(form, sections=prune(form.sections))
            if form.form_id == "plan"
            else form
            for form in self.registry.common_forms
        )
        return dataclasses.replace(self.registry, common_forms=forms)

    def old_list_registry(self, allowed: tuple[str, ...] | None):
        """A registry from before the Plan form: the H2 lists, no form."""

        profiles = tuple(
            dataclasses.replace(
                item,
                form=None,
                listed_headings=HeadingContract(
                    required=("Overview",), allowed=allowed or ("Overview",)
                ),
            )
            if item.profile_id == "sdlc/plan"
            else item
            for item in self.registry.profiles
        )
        forms = tuple(
            form for form in self.registry.common_forms if form.form_id != "plan"
        )
        return dataclasses.replace(self.registry, profiles=profiles, common_forms=forms)

    def rules_under(self, registry, base, proposed) -> set[str]:
        saved = self.registry
        type(self).registry = registry
        try:
            return self.rules(base=base, proposed=proposed)
        finally:
            type(self).registry = saved

    def test_three_rules_stay_active_with_the_forms_bound(self) -> None:
        plan = self.plan_text()
        base = {self.spec: self.spec_text(), self.plan: plan}
        self.assertTrue(
            any(form.form_id == "plan" for form in self.registry.common_forms)
        )
        self.assertIn(
            "PLAN-PROMOTION",
            self.rules(
                base=base,
                proposed={
                    **base,
                    self.plan: plan.replace("### Owner and Receipt\n", "### Other\n"),
                },
            ),
        )
        self.assertIn(
            "PLAN-GLOBAL-CONSTRAINTS",
            self.rules(
                base=base,
                proposed={
                    **base,
                    self.plan: plan.replace(
                        "#### Global Constraints\n" + self.CONSTRAINTS, ""
                    ),
                },
            ),
        )
        draft_parent = {
            self.spec: self.spec_text("in-review"),
            self.plan: plan,
            self.task: self.task_text(),
        }
        self.assertIn("TASK-PARENT-APPROVAL", self.rules(proposed=draft_parent))

    def test_constraints_heading_first_does_not_read_goal_text_as_constraints(
        self,
    ) -> None:
        plan = self.plan_text()
        base = {self.spec: self.spec_text(), self.plan: plan}
        first = plan.replace(
            "The fixture goal and its boundary.\n"
            "#### Global Constraints\n" + self.CONSTRAINTS,
            "#### Global Constraints\n"
            "The fixture goal links the [Spec](spec.md#scope).\n",
        )
        self.assertNotEqual(first, plan)
        self.assertIn(
            "PLAN-GLOBAL-CONSTRAINTS",
            self.rules(base=base, proposed={**base, self.plan: first}),
        )
        after = plan.replace(
            "#### Global Constraints\n" + self.CONSTRAINTS,
            "#### Global Constraints\n",
        ).replace(
            "The fixture assumptions.\n",
            "The assumptions link the [Spec](spec.md#scope).\n",
        )
        self.assertIn(
            "PLAN-GLOBAL-CONSTRAINTS",
            self.rules(base=base, proposed={**base, self.plan: after}),
        )
        self.assertNotIn(
            "PLAN-GLOBAL-CONSTRAINTS",
            self.rules(base=base, proposed={**base, self.plan: plan + "\nTail.\n"}),
        )

    def test_a_plan_form_without_a_needed_section_fails_closed(self) -> None:
        plan = self.plan_text()
        base = {self.spec: self.spec_text(), self.plan: plan}
        changed = {**base, self.plan: plan + "\nA changed line.\n"}
        for dropped, rule in (
            ("plan-promotion-map-owner-and-receipt", "PLAN-PROMOTION"),
            ("plan-overview-goal-and-boundary", "PLAN-GLOBAL-CONSTRAINTS"),
        ):
            with self.subTest(dropped=dropped):
                registry = self.registry_with(drop_sections=(dropped,))
                self.assertIn(rule, self.rules_under(registry, base, changed))

    def test_each_reader_handles_form_old_list_and_neither_registry(self) -> None:
        form_base = {self.spec: self.spec_text(), self.plan: self.plan_text()}
        form_bad = {
            **form_base,
            self.plan: self.plan_text().replace(
                "### Owner and Receipt\n", "### Other\n"
            ),
        }
        self.assertIn(
            "PLAN-PROMOTION", self.rules_under(self.registry, form_base, form_bad)
        )
        old = self.old_list_registry(("Overview", "Global Constraints", "Promotion"))
        old_base = {self.spec: self.spec_text(), self.plan: self.old_plan_text()}
        old_good = {**old_base, self.plan: self.old_plan_text() + "\nNote.\n"}
        old_bad = {
            **old_base,
            self.plan: self.old_plan_text().replace("## Promotion\n", "## Other\n"),
        }
        self.assertEqual(
            {"PLAN-PROMOTION", "PLAN-GLOBAL-CONSTRAINTS"}
            & self.rules_under(old, old_base, old_good),
            set(),
        )
        self.assertIn("PLAN-PROMOTION", self.rules_under(old, old_base, old_bad))
        neither = self.old_list_registry(None)
        self.assertEqual(
            {"PLAN-PROMOTION", "PLAN-GLOBAL-CONSTRAINTS", "TASK-PARENT-APPROVAL"}
            & self.rules_under(
                neither,
                old_base,
                {**old_bad, self.task: self.task_text(parent_id="SPEC-9999-PLAN-0001")},
            ),
            set(),
        )

    def test_the_old_shape_branch_reads_the_list_field_through_one_accessor(
        self,
    ) -> None:
        source = (SCRIPTS / "validate-document-lifecycle.py").read_text(
            encoding="utf-8"
        )
        # SPEC-0205: the one accessor function reads the list through heading_contract.
        self.assertEqual(source.count("heading_contract(profile).allowed"), 1)
        self.assertEqual(source.count("profile.headings"), 0)
        old_base = {self.spec: self.spec_text(), self.plan: self.old_plan_text()}
        old_bad = {
            **old_base,
            self.plan: self.old_plan_text().replace("## Promotion\n", "## Other\n"),
        }
        listing_without = self.old_list_registry(None)
        listing_with = self.old_list_registry(("Overview", "Promotion"))
        original = LIFECYCLE_CLI._allowed_h2
        try:
            LIFECYCLE_CLI._allowed_h2 = lambda profile: ("Promotion",)
            self.assertIn(
                "PLAN-PROMOTION", self.rules_under(listing_without, old_base, old_bad)
            )
            LIFECYCLE_CLI._allowed_h2 = lambda profile: ()
            self.assertNotIn(
                "PLAN-PROMOTION", self.rules_under(listing_with, old_base, old_bad)
            )
        finally:
            LIFECYCLE_CLI._allowed_h2 = original
        self.assertIn(
            "PLAN-PROMOTION", self.rules_under(listing_with, old_base, old_bad)
        )

    def test_text_read_after_the_move_equals_the_old_constraints_body(self) -> None:
        text = self.plan_text()
        read = LINKS._exact_heading_section(text, "#### Global Constraints")
        self.assertEqual((read or "").strip(), self.OLD_CONSTRAINTS.strip())


class OptionalMultiRowStatusTests(unittest.TestCase):
    """A multi-row Task may omit its frontmatter summary; readers derive it."""

    @classmethod
    def setUpClass(cls) -> None:
        from document_contracts import classify_path, load_registry, task_status

        cls.task_status = staticmethod(task_status)
        cls.registry = load_registry(ROOT)
        cls.profile = classify_path(cls.registry, TASK)
        cls.binding = cls.profile.body_contract.task_execution
        single = task_text("completed", [row(result="PASS", evidence="test: PASS")])
        second = row(
            "WORK-099", status="completed", result="PASS", evidence="test: PASS"
        )
        cls.with_status = task_text(
            "completed",
            [row(status="completed", result="PASS", evidence="test: PASS"), second],
        )
        cls.without_status = cls.with_status.replace('status: "completed"\n', "", 1)
        cls.single = single
        cls.single_without = single.replace('status: "completed"\n', "", 1)

    def rows(self, *states: str) -> list[dict[str, str]]:
        return [
            {
                "ID": f"WORK-{index:03d}",
                "Upstream criterion": "N/A — synthetic",
                "Work item": "x",
                "Owner": "platform",
                "Status": state,
                "Result": "PASS" if state == "completed" else "NOT_RUN",
                "Evidence": "test: PASS",
            }
            for index, state in enumerate(states, 1)
        ]

    def rule_ids(self, status: str, *states: str) -> set[str]:
        return {
            rule
            for rule, _ in task_execution_issues(
                self.rows(*states), status, self.binding
            )
        }

    def test_absent_summary_is_derived_and_present_summary_wins(self) -> None:
        self.assertEqual(
            self.task_status({}, self.without_status, self.profile), "completed"
        )
        self.assertEqual(
            self.task_status({"status": "draft"}, self.without_status, self.profile),
            "draft",
        )
        self.assertEqual(self.task_status({}, self.single_without, self.profile), "")

    def test_execution_rules_require_only_the_single_row_status(self) -> None:
        # An empty summary on parsed rows means the shared reader could not derive it.
        self.assertIn("TASK-EXECUTION-SUMMARY", self.rule_ids("", "completed", "draft"))
        self.assertNotIn(
            "TASK-EXECUTION-SUMMARY", self.rule_ids("in-progress", "completed", "draft")
        )
        self.assertIn(
            "TASK-EXECUTION-SUMMARY", self.rule_ids("draft", "completed", "draft")
        )
        self.assertIn("TASK-EXECUTION-STATUS", self.rule_ids("", "frontmatter"))

    def test_lifecycle_reads_the_derived_status(self) -> None:
        document = document_from_text(self.registry, TASK, self.without_status)
        self.assertEqual((document.status, document.state_issue), ("completed", None))
        document = document_from_text(self.registry, TASK, self.single_without)
        self.assertIsNone(document.status)

    def test_profile_validation_accepts_an_omitted_multi_row_summary(self) -> None:
        def rule_ids(text: str) -> set[str]:
            return {
                item.rule_id
                for item in MARKDOWN.validate_document_text(
                    text, TASK, self.profile, "strict"
                )
            }

        self.assertEqual(rule_ids(self.without_status), rule_ids(self.with_status))
        self.assertIn("TASK-EXECUTION-STATUS", rule_ids(self.single_without))
        hidden = self.without_status.replace(
            "### Lifecycle Traceability\n",
            "### Lifecycle Traceability\n<!--\n# x\n-->\n",
            1,
        )
        self.assertEqual(self.task_status({}, hidden, self.profile), "")
        self.assertIn("TASK-EXECUTION-SUMMARY", rule_ids(hidden))
        self.assertEqual(
            self.task_status({"status": None}, self.without_status, self.profile), ""
        )


class SpecArchitectureColumnTests(unittest.TestCase):
    """SPEC-0147: a Spec states its constraining architecture in one column."""

    def _diagnostics(self, header: str, row: str) -> list[str]:
        registry = load_registry(ROOT)
        profile = next(p for p in registry.profiles if p.profile_id == "sdlc/spec")
        path = PurePosixPath("docs/03.specs/0147-example/spec.md")
        text = ROOT.joinpath(
            "docs/99.templates/templates/specs/spec.template.md"
        ).read_text(encoding="utf-8")
        body = text.split("### Lifecycle Traceability", 1)[0]
        body = body.replace("{{TITLE}}", "Example").replace("{{OWNER}}", "platform")
        body = body.replace("{{UPDATED}}", "2026-11-06").replace(
            "{{ARTIFACT_ID}}", "SPEC-0147"
        )
        separator = "| " + " | ".join("---" for _ in header.split("|")[1:-1]) + " |"
        text = f"{body}### Lifecycle Traceability\n\n{header}\n{separator}\n{row}\n"
        return [
            item.rule_id
            for item in MARKDOWN.validate_document_text(
                text, path, profile, "strict", body_contracts="audit"
            )
        ]

    def test_architecture_column_is_required_and_non_empty(self) -> None:
        registry = load_registry(ROOT)
        columns = {
            p.profile_id: p.body_contract.required_columns
            for p in registry.profiles
            if p.profile_id in {"sdlc/spec", "common/template-sdlc-spec"}
        }
        self.assertEqual(len(set(columns.values())), 1, columns)
        self.assertIn("Architecture", columns["sdlc/spec"])
        new = "| Requirement ID | Spec criterion | Architecture | Verification method |"
        old = "| Requirement ID | Spec criterion | Verification method |"
        self.assertNotIn(
            "BODY-CONTRACT-COLUMNS",
            self._diagnostics(
                new,
                "| REQ-0001-FR-0001 | VAL-FEATURE-001 | None apply: no boundary change | Named test |",
            ),
        )
        self.assertIn(
            "BODY-CONTRACT-COLUMNS",
            self._diagnostics(
                old, "| REQ-0001-FR-0001 | VAL-FEATURE-001 | Named test |"
            ),
        )
        self.assertIn(
            "BODY-CONTRACT-CELL",
            self._diagnostics(
                new, "| REQ-0001-FR-0001 | VAL-FEATURE-001 |  | Named test |"
            ),
        )


class TaskTableRowWidthTests(unittest.TestCase):
    """SPEC-0148: a row wider or narrower than its header is refused."""

    def test_misplaced_evidence_row_is_refused(self) -> None:
        registry = load_registry(ROOT)
        profile = next(p for p in registry.profiles if p.profile_id == "sdlc/task")
        second = "[VAL-P02-002](../spec.md#criteria)"
        good = task_text(
            "in-progress",
            [
                row(
                    "WORK-001", status="in-progress", result="PASS", evidence="EVD-001"
                ),
                row(
                    "WORK-002",
                    criterion=second,
                    status="in-progress",
                    result="PASS",
                    evidence="EVD-002",
                ),
            ],
        ).replace('status: "in-progress"\n', "", 1)
        misplaced = (
            f"| EVD-004 | {UPSTREAM} | WORK-001 | Check | Staged index | PASS | "
            "Local run | yes | none |"
        )
        bad = good.replace(
            "\n## Verification Evidence",
            "\n" + misplaced + "\n## Verification Evidence",
            1,
        )

        def rules(text: str) -> set[str]:
            return {
                item.rule_id
                for item in MARKDOWN.validate_document_text(
                    text, TASK, profile, "strict"
                )
            }

        self.assertNotIn("BODY-CONTRACT-ROW-WIDTH", rules(good))
        self.assertIn("BODY-CONTRACT-ROW-WIDTH", rules(bad))
        narrow = good.replace(
            "\n## Verification Evidence",
            f"\n| WORK-003 | {UPSTREAM} | x |\n## Verification Evidence",
            1,
        )
        self.assertIn("BODY-CONTRACT-ROW-WIDTH", rules(narrow))


OLD_TASK_H2 = (
    "Overview",
    "Inputs",
    "Task Table",
    "Task Evidence",
    "Criterion Acceptance",
    "Approval and Safety Boundaries",
    "Verification Summary",
)
OLD_EVIDENCE_COLUMNS = (
    "Evidence",
    "Criteria",
    "Work Unit",
    "Check",
    "Input",
    "Result",
    "Location",
    "Required",
    "Resolves",
)


def old_task_registry(registry):
    """The registry as it stood before the Task form (SPEC-0203), derived from the
    repository registry: the seven H2 lists, the old evidence section and columns,
    the old acceptance section and no Task form."""

    profiles = []
    for profile in registry.profiles:
        if profile.profile_id == "sdlc/task":
            binding = replace(
                profile.body_contract.task_execution,
                evidence_section="Task Evidence",
                evidence_columns=OLD_EVIDENCE_COLUMNS,
                criterion_acceptance_section="Criterion Acceptance",
            )
            profile = replace(
                profile,
                listed_headings=HeadingContract(
                    required=OLD_TASK_H2, allowed=OLD_TASK_H2
                ),
                body_contract=replace(
                    profile.body_contract, section="Task Table", task_execution=binding
                ),
                form=None,
            )
        profiles.append(profile)
    return replace(
        registry,
        profiles=tuple(profiles),
        common_forms=tuple(f for f in registry.common_forms if f.form_id != "task"),
    )


def old_registry_json(raw: dict) -> dict:
    """The same undoing on the registry JSON, for a temporary repository."""

    raw = json.loads(json.dumps(raw))
    # MAJOR 15 is the registry before the Task form; the history reading builds the
    # H2 lists such a registry carried (SPEC-0205).
    raw["schema_version"] = "15.0.0"
    forms = raw["common_forms"]["forms"]
    raw["common_forms"]["forms"] = [f for f in forms if f["form_id"] != "task"]
    for profile in raw["profiles"]:
        if profile["id"] in ("sdlc/task", "common/template-sdlc-task"):
            profile["sections"] = {
                "required": list(OLD_TASK_H2),
                "optional": [],
                "forbidden": [],
            }
            contract = profile["relationships"]["body_contract"]
            contract["section"] = "Task Table"
            binding = contract["task_execution"]
            binding["evidence_section"] = "Task Evidence"
            binding["evidence_columns"] = list(OLD_EVIDENCE_COLUMNS)
            binding["criterion_acceptance_section"] = "Criterion Acceptance"
            profile.pop("template_definition", None)
    raw["work_residue"]["task_table"]["section"] = "Task Evidence"
    return raw


class TaskFormTwoRegistryTests(unittest.TestCase):
    """SPEC-0203: each side of a Task comparison is read with its own registry."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)
        cls.old = old_task_registry(cls.registry)

    def rules(self, before: str, after: str, *, old_base: bool) -> list[str]:
        base_registry = self.old if old_base else self.registry
        base = document_from_text(base_registry, TASK, before)
        proposed = document_from_text(self.registry, TASK, after)
        context = LIFECYCLE_CLI._evidence_context(
            self.registry,
            {TASK: base},
            {TASK: proposed},
            {TASK: before},
            {TASK: after},
            base_registry=base_registry,
        )
        return [
            item.rule_id
            for item in compare_lifecycle(
                self.registry,
                {TASK: base},
                {TASK: proposed},
                base_mode="staged",
                evidence_context=context,
                enforce_task_execution=True,
            )
        ]

    @staticmethod
    def rows() -> list[str]:
        return [
            row(status="completed", result="PASS", evidence="focused test PASS"),
            row("WORK-002", status="in-progress"),
        ]

    def pair(self) -> tuple[str, str]:
        return (
            task_text("in-progress", self.rows(), old_form=True),
            task_text("in-progress", self.rows()),
        )

    def edit_cell(self, text: str, column: int, value: str) -> str:
        """Change one cell of the first evidence data row of the form Task."""

        lines = text.split("\n")
        start = next(
            i for i, line in enumerate(lines) if line.startswith("| Evidence ID |")
        )
        cells = _cells(lines[start + 2])
        cells[column] = value
        lines[start + 2] = "| " + " | ".join(cells) + " |"
        return "\n".join(lines)

    def test_a_moving_commit_with_identical_rows_passes_every_rule(self) -> None:
        before, after = self.pair()
        found = self.rules(before, after, old_base=True)
        compared = [
            item
            for item in found
            if item.startswith("TASK-ITEM-") or item == "TASK-EVIDENCE-RETENTION"
        ]
        self.assertEqual(compared, [], found)

    def test_the_same_move_with_one_edited_cell_fails_retention_once_per_column(
        self,
    ) -> None:
        before, after = self.pair()
        columns = {
            1: "[VAL-P02-009](../spec.md#criteria)",
            2: "WORK-009",
            3: "Other command",
            4: "Other input",
            5: "FAIL",
            6: "elsewhere",
            7: "no",
            8: "EVD-009",
        }
        for column, value in columns.items():
            with self.subTest(column=column):
                found = self.rules(
                    before, self.edit_cell(after, column, value), old_base=True
                )
                self.assertEqual(found.count("TASK-EVIDENCE-RETENTION"), 1, found)

    def test_the_same_move_with_a_changed_removed_or_reordered_row_fails(self) -> None:
        before, after = self.pair()
        removed = task_text("in-progress", [self.rows()[1]])
        self.assertIn("TASK-ITEM-DELETE", self.rules(before, removed, old_base=True))
        hidden = after.replace(
            "[VAL-P02-001](../spec.md#criteria)",
            "[VAL-P02-002](../spec.md#criteria)",
            1,
        )
        self.assertIn("TASK-ITEM-HIDE", self.rules(before, hidden, old_base=True))
        reopened = task_text(
            "in-progress",
            [row(status="ready"), row("WORK-002", status="in-progress")],
        )
        self.assertIn("TASK-ITEM-EDGE", self.rules(before, reopened, old_base=True))
        reset = task_text(
            "in-progress",
            [
                row(status="completed", result="NOT_RUN"),
                row("WORK-002", status="in-progress"),
            ],
        )
        self.assertIn("TASK-ITEM-RESET", self.rules(before, reset, old_base=True))
        reordered = after.replace("| EVD-001 |", "| EVD-009 |", 1)
        self.assertIn(
            "TASK-EVIDENCE-RETENTION", self.rules(before, reordered, old_base=True)
        )

    def test_a_task_that_loses_its_recorded_rows_never_passes_on_nothing(self) -> None:
        before, after = self.pair()
        lost = after.replace("## Verification Evidence", "## Elsewhere", 1)
        found = self.rules(before, lost, old_base=True)
        self.assertIn("TASK-EVIDENCE-RETENTION", found)

    def test_a_column_missing_from_a_recorded_row_is_an_error_not_an_empty_cell(
        self,
    ) -> None:
        before, after = self.pair()
        for lacking in ("| Command |", "| Consumer |"):
            with self.subTest(lacking=lacking):
                bad = after.replace(lacking, "| Renamed |", 1)
                self.assertIn(
                    "TASK-EVIDENCE-RETENTION", self.rules(before, bad, old_base=True)
                )

    def test_a_table_that_keeps_the_old_header_fails_under_the_new_registry(
        self,
    ) -> None:
        _, after = self.pair()
        old_header = after.replace(CHECK_HEADER, OLD_CHECK_HEADER, 1)
        profile = next(p for p in self.registry.profiles if p.profile_id == "sdlc/task")
        found = {
            item.rule_id
            for item in MARKDOWN.validate_document_text(
                old_header, TASK, profile, "strict"
            )
        }
        self.assertIn("TASK-EVIDENCE-COLUMNS", found)

    def test_rules_stay_active_on_the_repository_registry_for_a_form_task(self) -> None:
        before = task_text("in-progress", self.rows())
        edited = self.edit_cell(before, 4, "Other input")
        self.assertIn(
            "TASK-EVIDENCE-RETENTION", self.rules(before, edited, old_base=False)
        )
        removed = task_text("in-progress", [self.rows()[1]])
        self.assertIn("TASK-ITEM-DELETE", self.rules(before, removed, old_base=False))
        reopened = task_text(
            "in-progress",
            [row(status="ready"), row("WORK-002", status="in-progress")],
        )
        self.assertIn("TASK-ITEM-EDGE", self.rules(before, reopened, old_base=False))
        hidden = before.replace(
            "[VAL-P02-001](../spec.md#criteria)",
            "[VAL-P02-002](../spec.md#criteria)",
            1,
        )
        self.assertIn("TASK-ITEM-HIDE", self.rules(before, hidden, old_base=False))
        reset = task_text(
            "in-progress",
            [
                row(status="completed", result="NOT_RUN"),
                row("WORK-002", status="in-progress"),
            ],
        )
        self.assertIn("TASK-ITEM-RESET", self.rules(before, reset, old_base=False))

    def test_each_reader_handles_a_form_an_old_and_a_binding_less_registry(
        self,
    ) -> None:
        form_binding = next(
            p for p in self.registry.profiles if p.profile_id == "sdlc/task"
        ).body_contract.task_execution
        old_binding = next(
            p for p in self.old.profiles if p.profile_id == "sdlc/task"
        ).body_contract.task_execution
        before, after = self.pair()
        current = LINKS.task_base_evidence_rows(after, form_binding)
        carried = LINKS.task_base_evidence_rows(before, old_binding)
        literal = LINKS.task_base_evidence_rows(before)
        self.assertEqual(current, carried)
        self.assertEqual(current, literal)
        self.assertEqual(
            list(current[0]),
            [
                "Evidence ID",
                "Consumer",
                "Work Unit",
                "Command",
                "Input",
                "Result",
                "Location",
                "Required",
                "Resolves",
            ],
        )
        self.assertIsNone(LINKS.task_base_evidence_rows(after, old_binding))
        self.assertIsNone(LINKS.task_base_evidence_rows(before, form_binding))

    def test_the_header_map_is_a_history_reading_and_leaves_current_names_alone(
        self,
    ) -> None:
        from document_contracts import carry_evidence_rows

        binding = next(
            p for p in self.registry.profiles if p.profile_id == "sdlc/task"
        ).body_contract.task_execution
        rows = [{"Evidence ID": "EVD-001", "Consumer": "c", "Command": "k"}]
        self.assertEqual(carry_evidence_rows(rows, binding), rows)
        self.assertIsNone(carry_evidence_rows(None, binding))


class TaskFormRegistryCheckTests(unittest.TestCase):
    """SPEC-0203: the registry refuses a column or a binding the form does not own."""

    @classmethod
    def setUpClass(cls) -> None:
        import document_contracts

        cls.contracts = document_contracts
        cls.raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )

    def faults(self, raw: dict) -> set[str]:
        profiles = {profile["id"]: profile for profile in raw["profiles"]}
        return {
            item.rule_id
            for item in self.contracts._form_registry_diagnostics(ROOT, raw, profiles)
        }

    def test_the_repository_registry_has_no_task_form_fault(self) -> None:
        self.assertEqual(self.faults(self.raw), set())

    def test_a_results_column_that_is_neither_common_nor_registered_is_refused(
        self,
    ) -> None:
        raw = json.loads(json.dumps(self.raw))
        twin = next(
            p for p in raw["profiles"] if p["id"] == "common/template-sdlc-task"
        )
        table = next(
            t for t in twin["template_definition"]["tables"] if t["name"] == "Results"
        )
        table["columns"].append(
            {"key": "Extra", "meaning": "x", "data_type": "string", "required": False}
        )
        self.assertIn("REGISTRY_TABLE_COLUMNS", self.faults(raw))

    def test_a_binding_naming_a_section_the_form_lacks_is_refused(self) -> None:
        for key in ("evidence_section", "criterion_acceptance_section"):
            with self.subTest(key=key):
                raw = json.loads(json.dumps(self.raw))
                task = next(p for p in raw["profiles"] if p["id"] == "sdlc/task")
                task["relationships"]["body_contract"]["task_execution"][key] = (
                    "Task Evidence"
                )
                self.assertIn("REGISTRY_TASK_BINDING", self.faults(raw))

    def test_a_binding_column_that_is_neither_common_nor_registered_is_refused(
        self,
    ) -> None:
        raw = json.loads(json.dumps(self.raw))
        task = next(p for p in raw["profiles"] if p["id"] == "sdlc/task")
        task["relationships"]["body_contract"]["task_execution"][
            "evidence_columns"
        ].append("Extra")
        self.assertIn("REGISTRY_TASK_BINDING", self.faults(raw))


class TaskFormStagedMoveTests(unittest.TestCase):
    """SPEC-0203: the staged check reads the base registry from the base commit."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="task-form-move-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(
            ROOT / "docs/99.templates",
            self.root / "docs/99.templates",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        self.registry_path = self.root / "docs/99.templates/registry.json"
        raw = json.loads(self.registry_path.read_text(encoding="utf-8"))
        for profile in raw["profiles"]:
            for named in profile.get("template_definition", {}).get(
                "consumer_paths", ()
            ):
                target = self.root / named
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / named, target)
        self.new_registry = self.registry_path.read_text(encoding="utf-8")
        self.registry_path.write_text(
            json.dumps(old_registry_json(raw), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self.rows = [
            row(status="completed", result="PASS", evidence="focused test PASS"),
            row("WORK-002", status="in-progress"),
        ]
        self.write(SPEC, form_spec_text())
        self.write(SPEC.parent / "plan.md", form_plan_text())
        self.write(TASK, task_text("in-progress", self.rows, old_form=True))
        subprocess.run(["git", "init", "--quiet"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "--", "docs"], cwd=self.root, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=f@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "base",
            ],
            cwd=self.root,
            check=True,
        )
        # The index now binds the form; the working tree is not read for the base.
        self.registry_path.write_text(self.new_registry, encoding="utf-8")

    def write(self, path: PurePosixPath, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def staged(self, task: str) -> tuple[int, str]:
        self.write(TASK, task)
        subprocess.run(["git", "add", "--", "docs"], cwd=self.root, check=True)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = LIFECYCLE_CLI.main(["--root", str(self.root), "--mode", "staged"])
        return result, output.getvalue()

    def test_identical_rows_pass_and_an_edited_or_removed_row_fails(self) -> None:
        moved = task_text("in-progress", self.rows)
        result, output = self.staged(moved)
        self.assertEqual(result, 0, output)
        edited = moved.replace("Synthetic fixture", "Edited fixture", 1)
        result, output = self.staged(edited)
        self.assertEqual(result, 1, output)
        self.assertIn("TASK-EVIDENCE-RETENTION", output)
        removed = task_text("in-progress", [self.rows[1]])
        result, output = self.staged(removed)
        self.assertEqual(result, 1, output)
        self.assertIn("TASK-ITEM-DELETE", output)


if __name__ == "__main__":
    unittest.main()
