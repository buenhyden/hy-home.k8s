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
- Start: branch `fix/task-table-row-width` from `main` at `d8a58a39`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | Focused test and width diagnostic | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-ROW-002](../spec.md#success-criteria--verification-plan) | Strict checks and suites | platform | draft | NOT_RUN | EVD-002 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-ROW-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and unit tests | Pending Spec approval | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ROW-001](../spec.md#success-criteria--verification-plan) | pending | none | Run the focused test | platform |
| [VAL-ROW-002](../spec.md#success-criteria--verification-plan) | pending | none | Run the strict checks and suites | platform |

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

Pending.
