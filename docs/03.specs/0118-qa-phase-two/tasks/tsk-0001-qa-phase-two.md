---
title: "Local QA Phase Two Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0118-TSK-0001"
parent_ids: ["SPEC-0118-PLAN-0001"]
---

# Task: Local QA Phase Two Execution

## Overview

Execute [SPEC-0118](../spec.md) through [WORK-001–004](../plan.md#work-breakdown):
a single owner for each workflow rule, a correctly named CI metadata test,
narrowed script and test surfaces, and a gate for the lifecycle modules.

## Inputs

- The operator's 2026-10-16 instruction to proceed as recommended with phase
  two. The recommended defaults are: keep `agent-governance` on its current
  surfaces, and leave the other unrun modules to a separate Spec.
- Start: main `2e27681d` (PR #158 merge; first drafted on `ad3e187f`), branch `refactor/spec-0118-qa-phase-two` in a
  separate worktree.
- The read-only phase-two scoping report of the same date.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | Workflow rule single ownership | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | CI metadata test rename | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | Narrowed script and test surfaces | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | Lifecycle module gate | platform | draft | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Lifecycle module gate run | `scripts/run-document-contract-tests.py` on this branch | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | pending | none | Validator and test change remains | platform |
| [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | pending | none | Test rename remains | platform |
| [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | pending | none | Registry change remains | platform |
| [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | pending | none | Gate registration remains | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0118-qa-phase-two/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/validation/**`, `scripts/validate-github-actions-security.py`,
  `scripts/validate-affected-surfaces.py`, `scripts/run-archive-contract-tests.py`,
  `scripts/run-document-contract-tests.py`, `scripts/README.md`, `tests/**`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**: The operator's "proceed as recommended" is recorded
  as approval of SPEC-0118 and its Plan as written on 2026-10-16. The operator
  may revoke or amend it. Push, pull request and merge follow RUN-0013.
- **Static Validation**: Focused tests, Ruff and `qa.py staged` on the exact
  index.
- **Live Validation**: None.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

Pending.
