---
title: "Test Module Purpose Gates Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-19"
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
| WORK-001 | [VAL-PG-001](../spec.md#success-criteria--verification-plan) | Shared suite runner and coverage guard | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | Link-boundary rewrite and lane test budgets | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | Register and route the suite gates | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Suite gate runs | `scripts/run-contract-tests.py` for every suite on this branch | NOT_RUN | Pending | yes | none |

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
