---
title: "Local QA Phase Two Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0118-PLAN-0001"
parent_ids: ["SPEC-0118"]
---

# Local QA Phase Two Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to `.github/workflows/**`, provider settings or credentials.

## Overview

This plan executes [SPEC-0118](spec.md) on branch
`refactor/spec-0118-qa-phase-two` from main `2e27681d` (rebased from `ad3e187f`).

## Context

A read-only `quality-engineer` scoping review on 2026-10-16 measured gate costs
serially. Selection was checked through `validate-affected-surfaces.py` on
in-memory registry copies.

## Goals & In-Scope

Close VAL-QP2-001 to VAL-QP2-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-QP2-001](spec.md#success-criteria--verification-plan) | Remove dead workflow rules and the zizmor guard; move `timeout-minutes` | None | [Task](tasks/tsk-0001-qa-phase-two.md) | Focused tests, staged QA |
| WORK-002 | [VAL-QP2-002](spec.md#success-criteria--verification-plan) | Rename the CI metadata test and drop its duplicates | WORK-001 | [Task](tasks/tsk-0001-qa-phase-two.md) | Focused tests, staged QA |
| WORK-003 | [VAL-QP2-003](spec.md#success-criteria--verification-plan) | Narrow `scripts` and `tests` catch-all surfaces | WORK-002 | [Task](tasks/tsk-0001-qa-phase-two.md) | Selection tests, full-tree classification |
| WORK-004 | [VAL-QP2-004](spec.md#success-criteria--verification-plan) | Register `document-contract-tests` and extend the archive runner | WORK-003 | [Task](tasks/tsk-0001-qa-phase-two.md) | Registry and selection tests, runner execution |

## Verification Plan

Each work unit runs its focused modules and `qa.py staged` on the exact index.
The registry edits run in order because they touch the same file. The branch
receives one independent read-only review.

## Risks & Mitigations

- A narrowed surface drops a needed gate: the full-tree classification check
  and the "must not select" and "must select" fixture cases.
- A removed workflow rule held a real protection: each removal names its
  remaining owner in the Task.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
