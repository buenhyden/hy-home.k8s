---
title: "Historical Fixture Drift in Lifecycle Tests"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0111-TSK-0001"
parent_ids: ["SPEC-0111-PLAN-0001"]
---

# Task: Historical Fixture Drift in Lifecycle Tests

## Overview

Execute the two work units of the [Plan](../plan.md) for
[SPEC-0111](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0111](../spec.md) and its [Plan](../plan.md).
- Operator selection on 2026-10-13: fix both failing suites in SPEC-0111.
- Main `07ef6b7eabea8c654b6825e4443c8eebf206f7b8`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | Pin the acceptance test package snapshot | platform | completed | PASS | EVD-003 in commit `5cb5d87d` |
| WORK-002 | [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | Project the generation Task and replace the retired edge | platform | completed | PASS | EVD-004 in commit `e925c469`; EVD-005 review |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests and staged QA | `tests.test_task_acceptance_contract` from the validation environment: 12 tests with 2 `ApprovedPackageRetentionTests` failures (`COMPLETION-ALLOCATION`, `COMPLETION-ACCEPTANCE`) on main `07ef6b7e`, 12 OK after reading the three SPEC-0107 files from `2a27d98f`; no assertion changed. A scratch-clone `git bisect` placed the break on `2a9daeb7`. `qa.py staged` on the WORK-001 index first failed `selected-nonstyle` (detect-secrets on the SHA) and then `selected-style` (format); after the repository's allowlist pragma and Ruff format, all 10 selected gates passed | PASS | This Task; WORK-001 commit | yes | EVD-001 |
| EVD-004 | [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and staged QA | `GenerationAdmissionTests` from the validation environment: 6 tests with 3 failures on main `07ef6b7e` (`TASK-ITEM-HIDE` on the SPEC-0106 Task, `LIFECYCLE-CREATE` on its Spec), bisected to `9067729b`; 6 OK after projecting that one Task into the current table form and closing the Spec through the declared cancellation edge. A new assertion shows the retired Spec `in-progress` to `completed` edge reports `LIFECYCLE-EDGE`. Both modules together ran 47 tests OK. `qa.py staged` on the WORK-002 index passed all 10 selected gates | PASS | This Task; WORK-002 commit | yes | EVD-002 |
| EVD-005 | [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent read-only review | A code-reviewer subagent reviewed `5cb5d87d` and `e925c469`, reran 18 tests OK and diffed `current_task_form` on the real blob: 806 lines kept, 17 changed, all 12 evidence rows kept. No HIGH or MEDIUM finding. LOW, accepted: the projection is guarded only downstream; FAIL rows map to `Resolves=none`, which an in-progress Task allows today; the cancelled step no longer replays a Spec reaching a terminal state with an in-progress Task, and the fixture cancellation values are unvalidated; the replay still copies live templates and Registry by design, and three other live reads outside this scope (SPEC-0105 package, SPEC-0106 `tsk-0016`, `CURRENT_TASK`) could drift the same way | PASS | This Task | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-003 | Accept the pinned package snapshot; 12 acceptance tests pass with no assertion changed | platform |
| [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-004, EVD-005 | Accept the current-form replay and the retired-edge assertion; review LOW items recorded as residual risk | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `docs/03.specs/README.md`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
  (reciprocal link), `tests/test_task_acceptance_contract.py` and
  `tests/test_task_execution_contract.py`.
- **Forbidden Paths**: `scripts/`, `docs/99.templates/`, other Spec
  packages, frozen Archive payloads, live cluster, Vault and secret
  material.
- **Approval Required**: the operator selected this scope and approved
  SPEC-0111 and its Plan for implementation on 2026-10-13 after reviewing
  the draft at `f2eea19c`; push, pull request and merge await the operator.
- **Static Validation**: focused tests and staged QA from the documented
  validation environment.
- **Live Validation**: DEFER — no live surface is touched.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Both work units are complete and both criteria are accepted. The five
lifecycle tests that failed on main `07ef6b7e` now pass: the acceptance
module and the execution module ran 47 tests OK, and every commit passed
`qa.py staged` from the documented validation environment. No validator,
Registry, template or recorded Task changed.

Residual risk: three other tests still read live SPEC-0105, SPEC-0106
`tsk-0016` and current Task documents and could drift the same way; the
generation replay follows the live templates and Registry by design; the
fixture cancellation values rely on the field staying unvalidated.
Limitations: hosted CI, push and pull request are not executed. Next owner:
the operator for push, pull request and merge.
