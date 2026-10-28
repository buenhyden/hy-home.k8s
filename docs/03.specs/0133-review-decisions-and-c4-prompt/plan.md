---
title: "Review Decisions and C4 Prompt Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0133-PLAN-0001"
parent_ids: ["SPEC-0133"]
---

# Review Decisions and C4 Prompt Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- GitHub reads are GET calls only.

## Overview

This plan executes [SPEC-0133](spec.md) on branch
`docs/review-decisions-and-c4-prompt` from main `8d1ddd2b`.

## Context

Two read-only reviews on 2026-10-28 covered the m0012 matrix and the eight
`EXTERNAL` CRs. No architecture decision, interface or migration changes;
rollback is a revert.

## Goals & In-Scope

Close VAL-RD-001 to VAL-RD-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RD-001](spec.md#success-criteria--verification-plan) | Add the C4 checks to the diagram author prompt | None | [Task](tasks/tsk-0001-review-decisions-and-c4-prompt.md) | Staged QA |
| WORK-002 | [VAL-RD-002](spec.md#success-criteria--verification-plan) | Record the proposal and catalogue decisions | None | [Task](tasks/tsk-0001-review-decisions-and-c4-prompt.md) | Decision record and review |
| WORK-003 | [VAL-RD-003](spec.md#success-criteria--verification-plan) | Record the external evidence and closing actions | None | [Task](tasks/tsk-0001-review-decisions-and-c4-prompt.md) | External record and review |
| WORK-004 | [VAL-RD-004](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-001 to WORK-003 | [Task](tasks/tsk-0001-review-decisions-and-c4-prompt.md) | Review and hosted checks |

## Verification Plan

A reviewer re-reads the m0012 matrix and the GitHub metadata and checks each
recorded decision and observation.

## Risks & Mitigations

- A recorded observation goes stale. Each row names its observation date.
- A prompt change implies a new rule. The prompt asks the author and adds no
  validator rule.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
