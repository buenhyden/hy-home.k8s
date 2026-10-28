---
title: "Archive Evidence Owner Migration Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0131-PLAN-0001"
parent_ids: ["SPEC-0131"]
---

# Archive Evidence Owner Migration Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to validators, registry, workflows, provider settings or
  credentials.

## Overview

This plan executes [SPEC-0131](spec.md) on branch
`docs/archive-evidence-owner-migration` from `0d5d491e`, the SPEC-0130 head.

## Context

The SPEC-0130 census left eleven units whose consumers are current
documents only. The operator chose ten of them on 2026-10-28 and kept
SPEC-0104, whose Tasks are current acceptance evidence for REQ-0004.

## Goals & In-Scope

Close VAL-EO-001 to VAL-EO-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EO-001](spec.md#success-criteria--verification-plan) | Move the consumers to identifiers and the recovery route | None | [Task](tasks/tsk-0001-archive-evidence-owner-migration.md) | Consumer search and review |
| WORK-002 | [VAL-EO-002](spec.md#success-criteria--verification-plan) | Isolated recovery of the ten units | None | [Task](tasks/tsk-0001-archive-evidence-owner-migration.md) | Tree equality and scratch restore |
| WORK-003 | [VAL-EO-003](spec.md#success-criteria--verification-plan) | Remove the ten units and add their assessment rows | WORK-001, WORK-002 | [Task](tasks/tsk-0001-archive-evidence-owner-migration.md) | Staged QA on the exact index |
| WORK-004 | [VAL-EO-004](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-003 | [Task](tasks/tsk-0001-archive-evidence-owner-migration.md) | Review and hosted checks |

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
