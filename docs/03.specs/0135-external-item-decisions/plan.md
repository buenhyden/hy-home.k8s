---
title: "External Item Decisions Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0135-PLAN-0001"
parent_ids: ["SPEC-0135"]
---

# External Item Decisions Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- GitHub reads are GET or GraphQL query calls only.

## Overview

This plan executes [SPEC-0135](spec.md) on branch
`docs/external-item-decisions` from `7142c6a8`, the SPEC-0134 head.

## Context

SPEC-0133 named the operator action each `EXTERNAL` CR waits on. Five of
those actions happened on 2026-10-28.

## Goals & In-Scope

Close VAL-XD-001 to VAL-XD-003.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-XD-001](spec.md#success-criteria--verification-plan) | Record the three operator decisions | None | [Task](tasks/tsk-0001-external-item-decisions.md) | Decision record and review |
| WORK-002 | [VAL-XD-002](spec.md#success-criteria--verification-plan) | Record the archive layouts and the Projects observation | None | [Task](tasks/tsk-0001-external-item-decisions.md) | Observation record and review |
| WORK-003 | [VAL-XD-003](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-001, WORK-002 | [Task](tasks/tsk-0001-external-item-decisions.md) | Review and hosted checks |

## Verification Plan

A reviewer re-runs the GET and GraphQL reads and checks each record.

## Risks & Mitigations

- An observation goes stale. Each row names its observation time.

## Completion Criteria

All three criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
