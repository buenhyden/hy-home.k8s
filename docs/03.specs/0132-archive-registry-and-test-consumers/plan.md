---
title: "Archive Registry and Test Consumers Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0132-PLAN-0001"
parent_ids: ["SPEC-0132"]
---

# Archive Registry and Test Consumers Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to validators, registry, workflows, provider settings or
  credentials.

## Overview

This plan executes [SPEC-0132](spec.md) on branch
`docs/archive-batch3` from `9bab5067`, the SPEC-0133 head.

## Context

The SPEC-0131 Task left 35 units `retained`. On 2026-10-28 the operator
approved the next batch. A trial removal of 34 units showed which consumers
read a body and which only name it; eight units stay.

## Goals & In-Scope

Close VAL-RT-001 to VAL-RT-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RT-001](spec.md#success-criteria--verification-plan) | Move the consumers to identifiers and the recovery route | None | [Task](tasks/tsk-0001-archive-registry-and-test-consumers.md) | Consumer search and review |
| WORK-002 | [VAL-RT-002](spec.md#success-criteria--verification-plan) | Isolated recovery of the twenty-seven units | None | [Task](tasks/tsk-0001-archive-registry-and-test-consumers.md) | Tree equality and scratch restore |
| WORK-003 | [VAL-RT-003](spec.md#success-criteria--verification-plan) | Remove the twenty-seven units and add their assessment rows | WORK-001, WORK-002 | [Task](tasks/tsk-0001-archive-registry-and-test-consumers.md) | Staged QA on the exact index |
| WORK-004 | [VAL-RT-004](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-003 | [Task](tasks/tsk-0001-archive-registry-and-test-consumers.md) | Review and hosted checks |

## Verification Plan

Recovery runs before removal. Staged QA runs on each commit's exact index in
a worktree without the ignored `graphify-out/` directory.

## Risks & Mitigations

- A reader loses one-click access to a package body or its evidence. Each
  edited document keeps the stated facts and names the Retention Catalog
  envelope as the recovery route.
- An unobserved external consumer loses a path. Each unit stays recoverable
  from its envelope commit.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
