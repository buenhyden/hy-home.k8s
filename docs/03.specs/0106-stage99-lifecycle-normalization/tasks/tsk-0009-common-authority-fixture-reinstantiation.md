---
title: "Common Authority Fixture Reinstantiation"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
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
| EVD-P02-090 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Retained first-appearance source mismatch | Task8 creation metadata | FAIL | [Intake](#verification-summary) | rejected |
| EVD-P02-091 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Named deterministic checks | Upcoming fixture input | NOT_RUN | Pending | pending |
| EVD-P02-092 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Actual draft index and configured message | Draft tree `127a63a6` | PASS | [Draft acceptance](#draft-acceptance) | accepted |
| EVD-P02-093 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Prospective terminal completion and review | Upcoming terminal candidate | NOT_RUN | Pending | pending |
| EVD-P02-094 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Actual committed registered-form creation | Parent `342a105e` to draft `8fe19c20` | PASS | [Creation proof](#creation-proof) | accepted |

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
remain historical evidence. This ready Task has no implementation or terminal acceptance. Its actual
registered-form creation and draft checks are recorded below; the ready
index and every later source index still require their own actual checks.

### Creation proof

The existing Git copy flags observed `C016` from
`docs/99.templates/templates/specs/task.template.md` to this new Task in both
the cached draft and committed parent-to-draft diff. The source is the same
regular blob, the target was absent in the parent and its ID is unique.
The committed receipt `hy-p01-task9-c1-committed-creation.json` has SHA-256
`034ef72d05294f76bf8fa6e50ad05c33d8752ac0c780ed5c32e5998fa2e0f9c3`.
It records selected tool-stdout metadata; the full raw diff was not persisted.

### Draft acceptance

Actual draft tree `127a63a62ae45181531d342fe0953407a45e2300` passed six fresh
canonical staged gates and the pinned configured draft message; separate
review accepted that exact input before the normal draft commit. The staged
receipt SHA-256 is
`767e42c0bafd939416df0a12d4bd71c736899a18faec966ed016374a2dc05d98`
and message receipt SHA-256 is
`9380f2ae170c1f95bdfcaa874e63f3e773a40c5002243193f315081ed566f9ba`.
These observed results belong to the prior draft input; the current ready
index has not yet been accepted.

### Readiness

Finite four-path selection reports seven validators, no unmatched paths and
no validator execution. `hy-p01-task9-selection.json` has SHA-256
`93c0892a7cf2af05b452efcd95dc82f7ca3c424bc65044436b5b3f5596a86dc3`.
The first ready index passed five of six actual gates; Markdown rejected
the historical `FAIL` row's erroneous `accepted` disposition. The failed
receipt SHA-256 is
`74c8c044ce6132055d59bb375f1b80ec2e4a0b0a56184e89c3214846acc78a39`.
The owner requires `accepted` results to be `PASS`; this correction retains
the failed observation with `rejected`. The message was not checked, and
the corrected ready index still requires fresh actual checks and review.
The four-method manifest retains governance routing, unowned/retired route,
native invocation-control and dangling-root refusals; its SHA-256 is
`7e13588a823153383e59ca5c5e625d3d1fa72c7ced5d72fb1e7f2051186db2e5`.
Existing focused bounds are sixty seconds; canonical staged uses the owner's
1200-second bound. Pinned Ruff, scanner, Markdown and configured message
prerequisites remain unchanged. Prior pure fixture observations can support
the upcoming implementation only after exact source, configuration and
public-dependency identity proof with independent attribution. No fixture
check, full/affected execution or hosted acceptance is claimed here.
