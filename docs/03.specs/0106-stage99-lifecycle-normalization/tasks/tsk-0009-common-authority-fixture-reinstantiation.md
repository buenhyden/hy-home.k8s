---
title: "Common Authority Fixture Reinstantiation"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0009"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Common Authority Fixture Reinstantiation

## Overview

Execute [VAL-P02-009](../spec.md#success-criteria--verification-plan) through
[WORK-009](../plan.md#work-breakdown), using the registered form for this
new unique draft and retaining current authority fixture refusals.

## Inputs

- [Plan](../plan.md) and [registered form](../../../99.templates/templates/specs/task.template.md).
- Retained Task8 source metadata, local receipts and reviewed forward rollback.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-009 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | One bounded authority fixture repair | repo-tooling-engineer | frontmatter | NOT_RUN | pending | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-090 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Retained first-appearance source mismatch | Task8 creation metadata | FAIL | [Intake](#verification-summary) | pending |
| EVD-P02-091 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Named deterministic checks | Upcoming fixture input | NOT_RUN | Pending | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec, Plan, Task and `tests/test_common_agents_document_routes.py`.
- **Forbidden Paths**: Production contracts, schemas, Registry, frozen Archive and completed historical evidence.
- **Approval Required**: Existing scoped normal delivery and reviewed rollback authority; conditional closing reflection requires fresh actual checks and separate review before commit.
- **Static Validation**: Actual first-appearance source; named routing/native refusals, pinned hooks, each actual staged/message; prospective completion/review then fresh actual closing checks. Full/affected execution stays NOT_RUN.
- **Live Validation**: DEFER — no runtime action requested.
- **Secret / Vault Handling**: Safe metadata only; no raw logs or private values.
- **Rollback Plan**: Reviewed forward correction or revert preserving all commits and receipts.
- **Evidence Location**: This Task and external ignored retention/validation receipts.

## Verification Summary

Task8's real first-appearance metadata is `C014` from completed Task0007,
not its registered form. CI refusal is a static owner prediction; hosted
jobs were cancelled without runner assignment or code execution, with cause
unconfirmed. Its original four commits, source bytes and local PASS receipts
remain historical evidence. This new draft has no execution acceptance.
Observe genuine registered-template source metadata before its first commit.
