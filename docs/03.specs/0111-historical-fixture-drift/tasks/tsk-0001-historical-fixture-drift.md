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
| WORK-001 | [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | Pin the acceptance test package snapshot | platform | completed | PASS | EVD-003 in this commit |
| WORK-002 | [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | Project the generation Task and replace the retired edge | platform | in-progress | PASS | EVD-004 in commit after review |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests and staged QA | `tests.test_task_acceptance_contract` from the validation environment: 12 tests with 2 `ApprovedPackageRetentionTests` failures (`COMPLETION-ALLOCATION`, `COMPLETION-ACCEPTANCE`) on main `07ef6b7e`, 12 OK after reading the three SPEC-0107 files from `2a27d98f`; no assertion changed. A scratch-clone `git bisect` placed the break on `2a9daeb7`. `qa.py staged` on the WORK-001 index first failed `selected-nonstyle` (detect-secrets on the SHA) and then `selected-style` (format); after the repository's allowlist pragma and Ruff format, all 10 selected gates passed | PASS | This Task; WORK-001 commit | yes | EVD-001 |
| EVD-004 | [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and staged QA | `GenerationAdmissionTests` from the validation environment: 6 tests with 3 failures on main `07ef6b7e` (`TASK-ITEM-HIDE` on the SPEC-0106 Task, `LIFECYCLE-CREATE` on its Spec), bisected to `9067729b`; 6 OK after projecting that one Task into the current table form and closing the Spec through the declared cancellation edge. A new assertion shows the retired Spec `in-progress` to `completed` edge reports `LIFECYCLE-EDGE`. Both modules together ran 47 tests OK. `qa.py staged` on the WORK-002 index passed all 10 selected gates | PASS | This Task; WORK-002 commit | yes | EVD-002 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FIXTURE-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 checks | platform |
| [VAL-FIXTURE-002](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-002 checks | platform |

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

Pending execution.
