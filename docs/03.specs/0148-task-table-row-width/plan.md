---
title: "Task Table Row Width Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0148-PLAN-0001"
parent_ids: ["SPEC-0148"]
---

# Task Table Row Width Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- The failing test is written before the validator change.

## Overview

This plan executes [SPEC-0148](spec.md) on branch
`fix/task-table-row-width` from `main` at `d8a58a39`.

## Context

The F-07 review reproduced the defect: at `7aff341c` the strict
Markdown-profile, link and lifecycle CLIs all PASS on the misplaced rows.
Constraining architecture is [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md). Rollback is reverting the implementing
commit.

## Goals & In-Scope

Close VAL-ROW-001 and VAL-ROW-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ROW-001](spec.md#success-criteria--verification-plan) | Focused test first, then the width diagnostic | None | [Task](tasks/tsk-0001-task-table-row-width.md) | Test FAIL then PASS |
| WORK-002 | [VAL-ROW-002](spec.md#success-criteria--verification-plan) | Run the strict checks and suites on every current document | WORK-001 | [Task](tasks/tsk-0001-task-table-row-width.md) | Strict checks and unit tests |

## Verification Plan

Run the focused test red then green, the document and Task-contract suites,
the strict checks and `python3 scripts/qa.py staged`, then an independent
review. Architecture compliance check: the change stays in a validator that
consumes the Stage 99 registry, as AD-0006 assigns.

## Risks & Mitigations

- A current document with a malformed row would start failing; a scan on
  2026-11-06 found none.

## Completion Criteria

VAL-ROW-001 and VAL-ROW-002 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
