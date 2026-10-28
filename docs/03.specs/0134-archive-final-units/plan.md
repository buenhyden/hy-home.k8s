---
title: "Archive Final Units Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0134-PLAN-0001"
parent_ids: ["SPEC-0134"]
---

# Archive Final Units Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to validators, the registry, workflows or frozen Archive records.

## Overview

This plan executes [SPEC-0134](spec.md) on branch
`docs/archive-final-units` from main `480ec7eb`.

## Context

SPEC-0132 kept nine units because frozen ledgers, tests or current traces
read or cite them. Only two of those reasons are test reads that a pinned
read can replace.

## Goals & In-Scope

Close VAL-AF-001 to VAL-AF-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AF-001](spec.md#success-criteria--verification-plan) | Move the test reads and links of SPEC-0080 and SPEC-0103 | None | [Task](tasks/tsk-0001-archive-final-units.md) | Test runs and link search |
| WORK-002 | [VAL-AF-002](spec.md#success-criteria--verification-plan) | Isolated recovery of the two units | None | [Task](tasks/tsk-0001-archive-final-units.md) | Tree equality and scratch restore |
| WORK-003 | [VAL-AF-003](spec.md#success-criteria--verification-plan) | Remove the two units and record the nine assessment rows | WORK-001, WORK-002 | [Task](tasks/tsk-0001-archive-final-units.md) | Validators and staged QA |
| WORK-004 | [VAL-AF-004](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-003 | [Task](tasks/tsk-0001-archive-final-units.md) | Review and hosted checks |

## Verification Plan

The three test modules run before and after removal; the archive, lifecycle
and link validators run on the removal commit.

## Risks & Mitigations

- A test loses coverage. Each test keeps its assertions; only the source of
  its input changes.
- A `usable` row reads as current authority. ADR-0040 defines `usable` as
  citable history, not authority.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
