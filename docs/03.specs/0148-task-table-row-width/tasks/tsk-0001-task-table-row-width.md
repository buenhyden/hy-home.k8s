---
title: "Task Table Row Width"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0148-TSK-0001"
parent_ids: ["SPEC-0148-PLAN-0001"]
---

# Task: Task Table Row Width

## Overview

Refuse a body-contract row whose width differs from its header (AUD-0001
F-07). It executes [SPEC-0148](../spec.md) through
[WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): review F-07 and proceed.
- Review (2026-11-06): the work-item ID pattern is not the defect; a width
  mismatch silently disables the Task contract check.
- Approval (2026-11-06): the operator's request to review F-07 and proceed approves SPEC-0148 and its Plan, drafted in `49a082b6`; merge is separate and criterion acceptance stays the operator's.
- Start: branch `fix/task-table-row-width` from `main` at `d8a58a39`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | Focused test and width diagnostic | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-ROW-002](../spec.md#success-criteria--verification-plan) | Strict checks and suites | platform | in-progress | PASS | EVD-005 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-ROW-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and unit tests | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Working tree on `ae91dd3c` with the new test and the old validator | FAIL | Local run, 2026-11-06T07:03Z: `TaskTableRowWidthTests` fails; the nine-cell row yields no diagnostic at all | no | none |
| EVD-004 | [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Working tree on `ae91dd3c` with the width diagnostic | PASS | Local run, 2026-11-06T07:04Z: `TaskTableRowWidthTests` OK for a too-wide and, after review, a too-narrow row; the fixed validator run against the `7aff341c` tree reports `BODY-CONTRACT-ROW-WIDTH` for exactly its three misplaced rows | yes | EVD-001 |
| EVD-005 | [VAL-ROW-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and unit tests | Working tree on `ae91dd3c` with the change | PASS | Local run, 2026-11-06T07:04Z to 07:06Z: strict contract-registry, profile, link and lifecycle PASS on every current document; `test_document*` OK; task, form, agent-route, evaluation, operations, repository-quality and affected-surface suites OK | yes | EVD-002 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | pending | EVD-004 | Awaiting operator acceptance | platform |
| [VAL-ROW-002](../spec.md#success-criteria--verification-plan) | pending | EVD-005 | Awaiting operator acceptance | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validate-markdown-profiles.py`,
  `tests/test_task_execution_contract.py`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/90.references/audits/0001-sdlc-governance/`
- **Forbidden Paths**: `docs/99.templates/registry.json`, other validators,
  product manifests, `secrets/`, provider settings
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

- Red then green: the focused test failed on the old validator (EVD-003) and
  passes with the width diagnostic; the fixed validator also flags the three
  rows of the original `7aff341c` defect (EVD-004).
- Every current document passes the strict checks, and the consumer suites
  pass (EVD-005).
- Not run: hosted, provider-runtime and live lanes (not applicable).
- Next owner: operator, for criterion acceptance and merge. Rollback: revert
  the implementing commit.
