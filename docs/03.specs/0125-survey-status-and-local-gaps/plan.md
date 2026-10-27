---
title: "Survey Status and Local Gaps Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0125-PLAN-0001"
parent_ids: ["SPEC-0125"]
---

# Survey Status and Local Gaps Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- Other repositories, live systems and provider settings are not touched.

## Overview

This plan executes [SPEC-0125](spec.md) on branch
`docs/cr-status-and-local-gaps` from main `bc7da828`.

## Context

SPEC-0124 closed CR-02.04 and CR-02.06. The remaining CRs had no recorded
status.

## Goals & In-Scope

Close VAL-CS-001 to VAL-CS-003.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CS-001](spec.md#success-criteria--verification-plan) | Record the 148-CR status table | None | [Task](tasks/tsk-0001-survey-status-and-local-gaps.md) | Independent sample |
| WORK-002 | [VAL-CS-002](spec.md#success-criteria--verification-plan) | Fix the local gaps | None | [Task](tasks/tsk-0001-survey-status-and-local-gaps.md) | Ignore checks and restore test |
| WORK-003 | [VAL-CS-003](spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | WORK-001, WORK-002 | [Task](tasks/tsk-0001-survey-status-and-local-gaps.md) | Staged QA and hosted checks |

## Verification Plan

The reviewer re-checks every `GAP` and `DONE_THIS_CYCLE` row and a sample of
`KEEP` citations against the repository.

## Risks & Mitigations

- A CR is marked met without evidence. Every `KEEP` row needs a citation,
  and the review samples them.
- The table becomes a ledger. Later slices record changes in their own Tasks.

## Completion Criteria

All three criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Handoff names candidate, verified and delivered commits | [Quality policy](../../../.agents/governance/quality.md) | Handoff evidence contract |
| Memory restore procedure | [Context and memory](../../../.agents/governance/context-and-memory.md) | Shared workspace memory |
