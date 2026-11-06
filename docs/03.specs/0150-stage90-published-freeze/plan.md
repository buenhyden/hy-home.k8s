---
title: "Stage 90 Published Member Freeze Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0150-PLAN-0001"
parent_ids: ["SPEC-0150"]
---

# Stage 90 Published Member Freeze Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- Failing tests are written before the validator change.

## Overview

This plan executes [SPEC-0150](spec.md) on branch
`fix/stage90-published-freeze` from `main` at `397e0c26`.

## Context

AUD-0001 m0002 records F-10. Constraining architecture is [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md). Rollback
is reverting the implementing commit.

## Goals & In-Scope

Close VAL-FRZ-001 and VAL-FRZ-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FRZ-001](spec.md#success-criteria--verification-plan) | Focused tests first, then the freeze check | None | [Task](tasks/tsk-0001-stage90-published-freeze.md) | Tests FAIL then PASS |
| WORK-002 | [VAL-FRZ-002](spec.md#success-criteria--verification-plan) | Run the strict checks and observe a refused m0001 rewrite | WORK-001 | [Task](tasks/tsk-0001-stage90-published-freeze.md) | Strict checks and an observed refusal |

## Verification Plan

Run the focused tests red then green, the reference and document suites, the
strict checks, `python3 scripts/qa.py staged` and an independent review.
Architecture compliance check: the change stays in the Stage 90 topology
owner and leaves the lifecycle validator to state edges, as AD-0006 and
REQ-0003-FR-0027 require.

## Risks & Mitigations

- A needed consumer succession that changes link text is refused; the
  author keeps the text and changes only the destination.

## Completion Criteria

VAL-FRZ-001 and VAL-FRZ-002 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
