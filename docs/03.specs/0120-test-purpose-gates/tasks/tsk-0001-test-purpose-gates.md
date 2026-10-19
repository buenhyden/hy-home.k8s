---
title: "Test Module Purpose Gates Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0120-TSK-0001"
parent_ids: ["SPEC-0120-PLAN-0001"]
---

# Task: Test Module Purpose Gates Execution

## Overview

Execute [SPEC-0120](../spec.md) through [WORK-001–003](../plan.md#work-breakdown):
a shared suite runner with a coverage guard, two test cost and stability
fixes, and a registered purpose gate for every unrun test module.

## Inputs

- The operator's 2026-10-16 instruction to review and proceed with purpose
  gates for the 63 test modules that no lane runs, and the 2026-10-19
  instruction to continue from where the work stopped.
- Start: main `a29c836f` (PR #161 merge), branch
  `test/spec-0120-purpose-gates` in a separate worktree.
- The read-only scoping report of 2026-10-16.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PG-001](../spec.md#success-criteria--verification-plan) | Shared suite runner and coverage guard | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | Link-boundary rewrite and lane test budgets | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | Register and route the suite gates | platform | in-progress | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Suite gate runs | `scripts/run-contract-tests.py` for every suite on this branch | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests | Commit `8cb8980a`: `tests/test_documentation_link_boundary.py`, `tests/test_run_validation_lane.py` | PASS | The placeholder link test now runs the link pass over the two Stage 99 forms only, with the historical owner edges stubbed: those edges only exempt archived links. The module took 263 s and now takes 22 s (35 OK), and the three malformed placeholders still produce `LINK-BROKEN`. The two escaped-descendant tests got wider budgets and an atomic child write. Under 30 busy loops on 12 cores, the three escape tests passed 10 of 10. Idle, the lane module passed 3 of 3 (90 OK) | yes | none |
| EVD-003 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Commit `8cb8980a` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-004 | [VAL-PG-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Coverage guard | `test_every_test_module_runs_in_one_gate_selected_by_its_file` before and after the registry change | PASS | 74 subtests failed first; the two direct gates keep their own argv. With 11 suites registered, each of the 76 modules has exactly one gate, and its own file selects that gate in both lanes. The old archive and document runners are removed. `run-contract-tests.py --suite nope` exits 2 with an argparse error | yes | none |
| EVD-005 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Suite gate runs | `python3 scripts/run-contract-tests.py --root . --suite <id>` for every suite, run serially on the working tree that became commit `774b13bb`, with pinned tools first on `PATH` | PASS | archive: 13 modules, 286 tests, 124 s; archive-validation: 1/86, 430 s; document: 21/325, 225 s; document-lifecycle: 3/71, 98 s; validation-routing: 8/192, 54 s; qa-runner: 1/38, 569 s; ci-metadata: 3/84, 9 s; release: 2/27, 34 s; agent-governance: 5/147, 47 s; tooling: 9/156, 15 s; cluster-gate: 8 modules OK in the foreground | yes | EVD-001 |
| EVD-006 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selection tests and classification | Commit `774b13bb`: `registry.json`, the fixture, and the selection and registry tests | PASS | `validate-affected-surfaces.py --root .` PASS: 1,361 paths, uncovered 0, ambiguous 0. New surfaces: `validation-routing-scripts`, `qa-runner`, `lane-runner`, `contract-test-runner` and `archive-test-modules`. Two cluster test helpers moved to `cluster-gate-scripts`. A registry edit selects `validation-routing-tests` but not `qa-runner-tests`, and `qa.py` no longer pulls the broad script gates. Every changed fixture expectation adds only the newly intended gate. `test_validate_affected_surfaces`, `test_document_scope_selection`, `test_archive_registry_contract` and `test_validation_profiles` all OK | yes | none |
| EVD-007 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selected staged QA | First commit attempt on the same index, with pinned tools first on `PATH` and SIGINT reset to default, while another repository's validation loaded the host | FAIL | 24 gates passed. `validation-routing-tests` failed one test, `test_successful_leader_closes_silent_owned_process_group`, which used the shared helper's 2 s timeout and 0.5 s cleanup. The same suite passed on an exported index snapshot, with and without the closed `HOME` and `PATH` | yes | none |
| EVD-008 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Load test of the bounded-command class | Commit `774b13bb`: the shared `_run_python` defaults widened to 15 s timeout and 3 s cleanup; the per-test overrides from `8cb8980a` removed | PASS | Under 30 busy loops on 12 cores, the bounded-command class failed 5 to 7 tests per run across 9 tests with the old defaults, and 0 to 2 with the new ones. The remaining failures are only the two interrupt-count tests. The lane module passes idle (90 OK, 20 s) | yes | none |
| EVD-009 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selected staged QA | Commit `774b13bb` with pinned tools first on `PATH` and SIGINT reset to default | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed | yes | EVD-007 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PG-001](../spec.md#success-criteria--verification-plan) | pending | none | Runner and guard remain | platform |
| [VAL-PG-002](../spec.md#success-criteria--verification-plan) | pending | none | Test fixes remain | platform |
| [VAL-PG-003](../spec.md#success-criteria--verification-plan) | pending | none | Gate registration remains | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0120-test-purpose-gates/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/validation/registry.json`, `scripts/run-contract-tests.py`,
  `scripts/run-archive-contract-tests.py`,
  `scripts/run-document-contract-tests.py`, `scripts/README.md`, `tests/**`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**: The operator's 2026-10-16 instruction to review and
  proceed is recorded as approval of SPEC-0120 and its Plan as written on
  2026-10-19. The operator may revoke or amend it. Push, pull request and
  merge follow RUN-0013.
- **Static Validation**: Focused tests, Ruff and `qa.py staged` on the exact
  index.
- **Live Validation**: None.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

Pending.
