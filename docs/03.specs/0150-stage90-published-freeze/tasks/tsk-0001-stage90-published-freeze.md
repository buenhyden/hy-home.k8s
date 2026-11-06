---
title: "Stage 90 Published Member Freeze"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0150-TSK-0001"
parent_ids: ["SPEC-0150-PLAN-0001"]
---

# Task: Stage 90 Published Member Freeze

## Overview

Refuse a rewrite of a published Stage 90 member (AUD-0001 F-10). It executes
[SPEC-0150](../spec.md) through [WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): resolve the remaining item of the same kind.
- Review (2026-11-06): the check belongs to the Stage 90 topology owner, not
  the lifecycle validator (REQ-0003-FR-0027); link destinations stay
  changeable for consumer succession.
- Start: branch `fix/stage90-published-freeze` from `main` at `397e0c26`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | Focused tests and freeze check | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-FRZ-002](../spec.md#success-criteria--verification-plan) | Strict checks and observed refusal | platform | draft | NOT_RUN | EVD-002 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-FRZ-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and observed refusal | Pending Spec approval | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | pending | none | Run the focused tests | platform |
| [VAL-FRZ-002](../spec.md#success-criteria--verification-plan) | pending | none | Run the strict checks | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validate-document-contract-registry.py`,
  `tests/test_reference_pack_routes.py`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `scripts/validate-document-lifecycle.py`, the
  registry, published Stage 90 members, `secrets/`
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

Pending.
