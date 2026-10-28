---
title: "Archive History Link Migration Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0130-PLAN-0001"
parent_ids: ["SPEC-0130"]
---

# Archive History Link Migration Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to validators, registry, workflows, provider settings or
  credentials.

## Overview

This plan executes [SPEC-0130](spec.md) on branch
`docs/archive-history-link-migration` from `26d3da3f`, the SPEC-0129 head.

## Context

The census on 2026-10-28 searched the 57 retained catalog units. Twelve have
only history-link consumers in REQ-0003, REQ-0004 and AD-0007. Test fixtures
such as `0079-x` and `0090-example` are synthetic paths, not consumers.

## Goals & In-Scope

Close VAL-AM-001 to VAL-AM-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AM-001](spec.md#success-criteria--verification-plan) | Replace the history links with plain identifiers | None | [Task](tasks/tsk-0001-archive-history-link-migration.md) | Path search and review |
| WORK-002 | [VAL-AM-002](spec.md#success-criteria--verification-plan) | Isolated recovery of the twelve units | None | [Task](tasks/tsk-0001-archive-history-link-migration.md) | Tree equality and scratch restore |
| WORK-003 | [VAL-AM-003](spec.md#success-criteria--verification-plan) | Remove the twelve units and add their assessment rows | WORK-001, WORK-002 | [Task](tasks/tsk-0001-archive-history-link-migration.md) | Staged QA on the exact index |
| WORK-004 | [VAL-AM-004](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-003 | [Task](tasks/tsk-0001-archive-history-link-migration.md) | Review and hosted checks |

## Verification Plan

Recovery runs before removal. Staged QA runs on each commit's exact index in
a worktree without the ignored `graphify-out/` directory.

## Risks & Mitigations

- A reader loses one-click access to a package body. Each edited document
  names the Retention Catalog envelope as the recovery route.
- An unobserved external consumer loses a path. Each unit stays recoverable
  from its envelope commit.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
