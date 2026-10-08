"""Adverse Task evidence must stay visible to the sole criterion decision."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path, PurePosixPath


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from document_contracts import (  # noqa: E402
    TaskExecution,
    classify_path,
    legacy_task_profile,
    load_registry,
    task_contract_issues,
    task_evidence_issues,
)


FIRST = "[VAL-P03-001](../spec.md#success-criteria--verification-plan)"
SECOND = "[VAL-P03-002](../spec.md#success-criteria--verification-plan)"
CRITERION = FIRST
ROOT = Path(__file__).resolve().parents[1]

BINDING = TaskExecution(
    single_status_marker="frontmatter",
    result_states={
        "draft": ("NOT_RUN",),
        "ready": ("NOT_RUN",),
        "in-progress": ("NOT_RUN", "PASS", "FAIL", "DEFER"),
        "blocked": ("NOT_RUN", "FAIL", "DEFER"),
        "completed": ("PASS", "NOT_APPLICABLE"),
        "cancelled": ("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"),
        "superseded": ("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"),
    },
    summary_rule="task-items-v2",
    acceptance_states=("pending", "accepted", "rejected", "not-required"),
    evidence_section="Task Evidence",
    evidence_columns=(
        "Evidence",
        "Criteria",
        "Work Unit",
        "Check",
        "Input",
        "Result",
        "Location",
        "Required",
        "Resolves",
    ),
    evidence_result_states=("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"),
    criterion_acceptance_section="Criterion Acceptance",
    criterion_acceptance_columns=(
        "Criterion",
        "Acceptance",
        "Evidence",
        "Disposition",
        "Current owner",
    ),
)


def work(
    *,
    criterion: str = FIRST,
    identifier: str = "WORK-001",
    result: str = "PASS",
    evidence: str = "EVD-002",
) -> dict[str, str]:
    return {
        "ID": identifier,
        "Upstream criterion": criterion,
        "Work item": "Verify scoped behavior",
        "Owner": "platform",
        "Status": "frontmatter",
        "Result": result,
        "Evidence": evidence,
    }


def check(
    identifier: str,
    result: str,
    *,
    criterion: str = FIRST,
    work_unit: str = "WORK-001",
    name: str = "Focused test",
    required: str = "yes",
    resolves: str = "none",
) -> dict[str, str]:
    return {
        "Evidence": identifier,
        "Criteria": criterion,
        "Work Unit": work_unit,
        "Check": name,
        "Input": "fixed fixture and revision",
        "Result": result,
        "Location": "tests/test_task_acceptance_boundaries.py",
        "Required": required,
        "Resolves": resolves,
    }


def decision(
    *,
    criterion: str = FIRST,
    verdict: str = "accepted",
    cited: str = "EVD-002",
    disposition: str = "The focused check passed",
    owner: str = "platform",
) -> dict[str, str]:
    return {
        "Criterion": criterion,
        "Acceptance": verdict,
        "Evidence": cited,
        "Disposition": disposition,
        "Current owner": owner,
    }


def rules(
    works: list[dict[str, str]],
    checks: list[dict[str, str]],
    decisions: list[dict[str, str]],
    status: str = "completed",
) -> set[str]:
    return {
        rule
        for rule, _ in task_contract_issues(works, checks, decisions, status, BINDING)
    }


class TaskAcceptanceBoundaries(unittest.TestCase):
    def test_accepted_criterion_needs_a_required_pass(self) -> None:
        for result in ("NOT_RUN", "DEFER", "FAIL"):
            with self.subTest(result=result):
                actual = rules(
                    [work(result="NOT_RUN", evidence="EVD-001")],
                    [check("EVD-001", result)],
                    [decision(cited="EVD-001")],
                    status="in-progress",
                )
                self.assertIn("TASK-ACCEPTANCE-EVIDENCE", actual)
        self.assertIn(
            "TASK-ACCEPTANCE-EVIDENCE",
            rules(
                [work(result="PASS")],
                [check("EVD-002", "PASS", required="no")],
                [decision()],
            ),
        )

    def test_new_required_failure_reopens_an_earlier_resolution(self) -> None:
        previous = [
            check("EVD-001", "FAIL"),
            check("EVD-002", "PASS", resolves="EVD-001"),
        ]
        self.assertEqual(rules([work()], previous, [decision()]), set())
        actual = rules(
            [work(evidence="EVD-002, EVD-003")],
            previous + [check("EVD-003", "FAIL")],
            [decision()],
        )
        self.assertIn("TASK-EVIDENCE-UNRESOLVED", actual)

    def test_optional_pass_cannot_close_a_required_failure(self) -> None:
        actual = rules(
            [work(evidence="EVD-003")],
            [
                check("EVD-001", "FAIL"),
                check("EVD-002", "PASS", required="no", resolves="EVD-001"),
                check("EVD-003", "PASS", name="Separate required check"),
            ],
            [decision(cited="EVD-003")],
        )
        self.assertIn("TASK-EVIDENCE-RESOLUTION", actual)
        self.assertIn("TASK-EVIDENCE-UNRESOLVED", actual)

    def test_delayed_required_check_needs_explicit_successor(self) -> None:
        for adverse in ("DEFER", "NOT_RUN"):
            with self.subTest(adverse=adverse):
                original = check("EVD-001", adverse)
                recovered = check("EVD-002", "PASS", resolves="EVD-001")
                self.assertEqual(
                    rules([work()], [original, recovered], [decision()]),
                    set(),
                )

    def test_resolution_must_match_the_original_work_and_criterion(self) -> None:
        works = [
            work(identifier="WORK-001", criterion=FIRST),
            work(identifier="WORK-002", criterion=SECOND),
        ]
        # Multi-row Tasks use row statuses and one frontmatter summary.
        works = [row | {"Status": "completed", "Result": "PASS"} for row in works]
        failed = check("EVD-001", "FAIL")
        for changed in (
            {"Work Unit": "WORK-002", "Criteria": SECOND},
            {"Criteria": SECOND},
        ):
            with self.subTest(changed=changed):
                attempted = check("EVD-002", "PASS", resolves="EVD-001") | changed
                actual = rules(
                    works,
                    [
                        failed,
                        attempted,
                        check(
                            "EVD-003",
                            "PASS",
                            criterion=SECOND,
                            work_unit="WORK-002",
                            name="Second criterion",
                        ),
                    ],
                    [decision(), decision(criterion=SECOND, cited="EVD-003")],
                )
                self.assertIn("TASK-EVIDENCE-RESOLUTION", actual)
                self.assertIn("TASK-EVIDENCE-UNRESOLVED", actual)

    def test_decision_cannot_reuse_another_criterions_evidence(self) -> None:
        works = [
            work(identifier="WORK-001") | {"Status": "completed"},
            work(identifier="WORK-002", criterion=SECOND) | {"Status": "completed"},
        ]
        actual = rules(
            works,
            [check("EVD-002", "PASS")],
            [decision(), decision(criterion=SECOND)],
        )
        self.assertIn("TASK-ACCEPTANCE-EVIDENCE", actual)

    def test_bad_identifiers_and_future_or_cyclic_resolution_fail(self) -> None:
        for bad_id in ("EVD-2", "EVD-002, EVD-003"):
            with self.subTest(bad_id=bad_id):
                self.assertIn(
                    "TASK-EVIDENCE-ID",
                    rules([work()], [check(bad_id, "PASS")], [decision()]),
                )
        for checks in (
            [check("EVD-002", "PASS", resolves="EVD-003"), check("EVD-003", "FAIL")],
            [check("EVD-001", "FAIL"), check("EVD-002", "PASS", resolves="EVD-002")],
            [
                check("EVD-001", "FAIL", resolves="EVD-002"),
                check("EVD-002", "PASS", resolves="EVD-001"),
            ],
        ):
            with self.subTest(checks=checks):
                self.assertIn(
                    "TASK-EVIDENCE-RESOLUTION",
                    rules([work()], checks, [decision()]),
                )

    def test_duplicate_evidence_and_unknown_citation_do_not_authorize(self) -> None:
        self.assertIn(
            "TASK-EVIDENCE-ID",
            rules(
                [work()],
                [check("EVD-002", "PASS"), check("EVD-002", "FAIL")],
                [decision()],
            ),
        )
        for cited in ("EVD-999", "EVD-002,EVD-003"):
            with self.subTest(cited=cited):
                self.assertIn(
                    "TASK-ACCEPTANCE-EVIDENCE",
                    rules(
                        [work()],
                        [check("EVD-002", "PASS")],
                        [decision(cited=cited)],
                    ),
                )

    def test_invalid_required_and_placeholder_decision_are_rejected(self) -> None:
        actual = rules(
            [work()],
            [check("EVD-002", "PASS", required="sometimes")],
            [decision(disposition="TBD", owner="pending")],
        )
        self.assertIn("TASK-EVIDENCE-REQUIRED", actual)
        self.assertIn("TASK-ACCEPTANCE-DISPOSITION", actual)

    def test_terminal_task_needs_every_assigned_criterion_accepted(self) -> None:
        self.assertIn(
            "TASK-ACCEPTANCE-COMPLETED",
            rules(
                [work()],
                [check("EVD-002", "PASS")],
                [decision(verdict="pending", cited="EVD-002")],
            ),
        )
        self.assertIn(
            "TASK-ACCEPTANCE-COVERAGE",
            rules([work()], [check("EVD-002", "PASS")], []),
        )
        self.assertIn(
            "TASK-ACCEPTANCE-SCOPE",
            rules(
                [work()],
                [check("EVD-002", "PASS")],
                [decision(verdict="not-required")],
            ),
        )

    def test_second_assigned_criterion_needs_its_own_decision(self) -> None:
        works = [
            work(identifier="WORK-001") | {"Status": "completed"},
            work(identifier="WORK-002", criterion=SECOND, evidence="EVD-003")
            | {"Status": "completed"},
        ]
        actual = rules(
            works,
            [
                check("EVD-002", "PASS"),
                check("EVD-003", "PASS", criterion=SECOND, work_unit="WORK-002"),
            ],
            [decision()],
        )
        self.assertIn("TASK-ACCEPTANCE-COVERAGE", actual)
        self.assertIn("TASK-ACCEPTANCE-COMPLETED", actual)


class TaskAcceptanceTests(unittest.TestCase):
    binding = TaskExecution(
        single_status_marker="frontmatter",
        result_states={
            "draft": ("NOT_RUN",),
            "ready": ("NOT_RUN",),
            "in-progress": ("NOT_RUN", "PASS", "FAIL", "DEFER"),
            "blocked": ("NOT_RUN", "FAIL", "DEFER"),
            "completed": ("PASS", "NOT_APPLICABLE"),
            "cancelled": ("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"),
            "superseded": ("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"),
        },
        summary_rule="task-items-v2",
        acceptance_states=("pending", "accepted", "rejected", "not-required"),
        evidence_section="Task Evidence",
        evidence_columns=(
            "Evidence",
            "Criteria",
            "Work Unit",
            "Check",
            "Input",
            "Result",
            "Location",
            "Required",
            "Resolves",
        ),
        evidence_result_states=("NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"),
        criterion_acceptance_section="Criterion Acceptance",
        criterion_acceptance_columns=(
            "Criterion",
            "Acceptance",
            "Evidence",
            "Disposition",
            "Current owner",
        ),
    )

    def work(self, **changes: str) -> dict[str, str]:
        return {
            "ID": "WORK-001",
            "Upstream criterion": CRITERION,
            "Work item": "Verify scoped behavior",
            "Owner": "platform",
            "Status": "frontmatter",
            "Result": "PASS",
            "Evidence": "EVD-002",
        } | changes

    def evidence(self, identifier: str, result: str, **changes: str) -> dict[str, str]:
        return {
            "Evidence": identifier,
            "Criteria": CRITERION,
            "Work Unit": "WORK-001",
            "Check": "Focused test",
            "Input": "same fixture and revision",
            "Result": result,
            "Location": "tests/test_task_acceptance_contract.py",
            "Required": "yes",
            "Resolves": "none",
        } | changes

    def acceptance(self, **changes: str) -> dict[str, str]:
        return {
            "Criterion": CRITERION,
            "Acceptance": "accepted",
            "Evidence": "EVD-002",
            "Disposition": "Focused check passed for this criterion",
            "Current owner": "platform",
        } | changes

    def rules(self, works, checks, decisions, status="completed") -> set[str]:
        return {
            rule
            for rule, _ in task_contract_issues(
                works, checks, decisions, status, self.binding
            )
        }

    def test_required_failure_needs_explicit_later_matching_resolution(self) -> None:
        work = [self.work()]
        failed = self.evidence("EVD-001", "FAIL")
        passed = self.evidence("EVD-002", "PASS")
        decision = [self.acceptance()]
        self.assertIn(
            "TASK-EVIDENCE-UNRESOLVED", self.rules(work, [failed, passed], decision)
        )
        self.assertEqual(
            self.rules(work, [failed, passed | {"Resolves": "EVD-001"}], decision),
            set(),
        )
        self.assertIn(
            "TASK-EVIDENCE-RESOLUTION",
            self.rules(
                work,
                [failed, passed | {"Check": "Unrelated", "Resolves": "EVD-001"}],
                decision,
            ),
        )

    def test_bad_resolution_edges_cannot_hide_failure(self) -> None:
        failed = self.evidence("EVD-001", "FAIL")
        passed = self.evidence("EVD-002", "PASS")
        for value in ("EVD-002", "EVD-999"):
            with self.subTest(value=value):
                self.assertIn(
                    "TASK-EVIDENCE-RESOLUTION",
                    self.rules(
                        [self.work()],
                        [failed, passed | {"Resolves": value}],
                        [self.acceptance()],
                    ),
                )

    def test_work_and_criterion_mapping_are_exact(self) -> None:
        self.assertIn(
            "TASK-EVIDENCE-WORK",
            self.rules(
                [self.work()],
                [self.evidence("EVD-002", "PASS", **{"Work Unit": "WORK-999"})],
                [self.acceptance()],
            ),
        )
        self.assertIn(
            "TASK-ACCEPTANCE-DUPLICATE",
            self.rules(
                [self.work()],
                [self.evidence("EVD-002", "PASS")],
                [self.acceptance(), self.acceptance()],
            ),
        )

    def test_pending_draft_preserves_unrun_check_without_accepting_it(self) -> None:
        self.assertEqual(
            self.rules(
                [self.work(Result="NOT_RUN", Evidence="Execution pending")],
                [self.evidence("EVD-001", "NOT_RUN", Location="Pending")],
                [
                    self.acceptance(
                        Acceptance="pending",
                        Evidence="none",
                        Disposition="Run focused test",
                    )
                ],
                status="draft",
            ),
            set(),
        )

    def test_scope_waiver_is_only_a_cancelled_task_candidate(self) -> None:
        decision = self.acceptance(
            Acceptance="not-required",
            Evidence="none",
            Disposition="Criterion withdrawn by cancelled Spec authorization",
        )
        for state in (
            "draft",
            "ready",
            "in-progress",
            "blocked",
            "completed",
            "superseded",
        ):
            with self.subTest(state=state):
                self.assertIn(
                    "TASK-ACCEPTANCE-SCOPE",
                    self.rules(
                        [self.work()],
                        [self.evidence("EVD-002", "PASS")],
                        [decision],
                        status=state,
                    ),
                )
        self.assertNotIn(
            "TASK-ACCEPTANCE-SCOPE",
            self.rules(
                [self.work()],
                [self.evidence("EVD-002", "PASS")],
                [decision],
                status="cancelled",
            ),
        )

    def test_failed_check_requires_concrete_provenance(self) -> None:
        for key in ("Check", "Input", "Location"):
            with self.subTest(key=key):
                self.assertIn(
                    "TASK-EVIDENCE-LOCATION",
                    self.rules(
                        [self.work(Result="FAIL")],
                        [self.evidence("EVD-002", "FAIL", **{key: "Pending"})],
                        [self.acceptance(Acceptance="rejected", Evidence="EVD-002")],
                        status="blocked",
                    ),
                )
        for result in ("NOT_RUN", "DEFER"):
            with self.subTest(result=result):
                self.assertNotIn(
                    "TASK-EVIDENCE-LOCATION",
                    self.rules(
                        [self.work(Result=result)],
                        [self.evidence("EVD-002", result, Location="Pending")],
                        [self.acceptance(Acceptance="pending", Evidence="EVD-002")],
                        status="blocked",
                    ),
                )


class LegacyEvidenceCompatibilityTests(unittest.TestCase):
    def test_old_accepted_check_keeps_location_only_placeholder_guard(self) -> None:
        registry = load_registry(ROOT)
        path = PurePosixPath(
            "docs/03.specs/0106-stage99-lifecycle-normalization/tasks/"
            "tsk-0016-shared-profile-migration.md"
        )
        text = (ROOT / path).read_text(encoding="utf-8")
        current = classify_path(registry, path)
        old = legacy_task_profile(ROOT, path, text, current)
        binding = old.body_contract.task_execution
        self.assertIsNone(binding.criterion_acceptance_section)
        row = {
            "Evidence": "EVD-001",
            "Criteria": CRITERION,
            "Work Unit": "WORK-001",
            "Check": "Pending",
            "Input": "Pending",
            "Result": "PASS",
            "Location": "tests/focused_fixture.py",
            "Acceptance": "accepted",
        }

        def rules(check):
            return {rule for rule, _ in task_evidence_issues((check,), binding)}

        self.assertEqual(rules(row), set())
        self.assertIn("TASK-EVIDENCE-LOCATION", rules(row | {"Location": "Pending"}))
        self.assertIn("TASK-EVIDENCE-LOCATION", rules(row | {"Input": ""}))

        modern = TaskAcceptanceTests.binding
        for result in ("PASS", "FAIL"):
            for key in ("Check", "Input", "Location"):
                with self.subTest(result=result, key=key):
                    modern_row = {
                        name: value
                        for name, value in row.items()
                        if name != "Acceptance"
                    } | {
                        "Required": "yes",
                        "Resolves": "none",
                        "Result": result,
                        key: "Pending",
                    }
                    self.assertIn(
                        "TASK-EVIDENCE-LOCATION",
                        {
                            rule
                            for rule, _ in task_evidence_issues((modern_row,), modern)
                        },
                    )


if __name__ == "__main__":
    unittest.main()
