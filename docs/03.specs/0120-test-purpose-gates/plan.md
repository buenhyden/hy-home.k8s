---
title: "Test Module Purpose Gates Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-19"
layer: "specs"
artifact_id: "SPEC-0120-PLAN-0001"
parent_ids: ["SPEC-0120"]
---

# Test Module Purpose Gates Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to `.github/workflows/**`, provider settings or credentials.

## Overview

This plan executes [SPEC-0120](spec.md) on branch
`test/spec-0120-purpose-gates` from main `a29c836f`.

## Context

A read-only scoping review on 2026-10-16 timed the 63 unrun modules serially
in a clean clone. Without gates, running all of them costs about 1,270
seconds. Three modules carry most of that: `test_archive_validation` about
394 seconds, `test_qa_runner` about 288 seconds and
`test_documentation_link_boundary` about 263 seconds.

## Goals & In-Scope

Close VAL-PG-001 to VAL-PG-003.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PG-001](spec.md#success-criteria--verification-plan) | Shared suite runner and coverage guard | None | [Task](tasks/tsk-0001-test-purpose-gates.md) | Runner execution, guard red then green |
| WORK-002 | [VAL-PG-002](spec.md#success-criteria--verification-plan) | Link-boundary rewrite and lane test budgets | None | [Task](tasks/tsk-0001-test-purpose-gates.md) | Focused tests |
| WORK-003 | [VAL-PG-003](spec.md#success-criteria--verification-plan) | Register and route the suite gates | WORK-001, WORK-002 | [Task](tasks/tsk-0001-test-purpose-gates.md) | Suite runs, selection tests, classification |

## Verification Plan

Each work unit runs its focused modules and `qa.py staged` on the exact index.
Registry edits run in order because they touch one file. The branch gets one
independent read-only review.

## Risks & Mitigations

- A slow suite fires on frequent edits. It is attached only to narrow
  product surfaces, and a selection test proves registry and document edits
  do not select it.
- A carved script loses a broad gate. A carved surface keeps the `scripts`
  validator set for scripts that shared consumers read.

## Completion Criteria

All three criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
