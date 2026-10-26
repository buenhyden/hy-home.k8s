---
title: "Archive Unit Disposition Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0122-PLAN-0001"
parent_ids: ["SPEC-0122"]
---

# Archive Unit Disposition Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to validators, registry, workflows, provider settings or
  credentials.

## Overview

This plan executes [SPEC-0122](spec.md) on branch
`feat/workspace-diagnostics-readmes` from `dc9cbeab`.

## Context

The dry-run checked all 64 Retention Catalog rows. Every envelope resolves
from `origin/main` with the expected object type. Seven units have no
consumer outside Stage 98.

## Goals & In-Scope

Close VAL-AD-001 and VAL-AD-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AD-001](spec.md#success-criteria--verification-plan) | Consumer census and isolated recovery for the seven units | None | [Task](tasks/tsk-0001-archive-unit-disposition.md) | Tree equality and scratch restore |
| WORK-002 | [VAL-AD-002](spec.md#success-criteria--verification-plan) | Remove the seven units and add their assessment rows | WORK-001 | [Task](tasks/tsk-0001-archive-unit-disposition.md) | Staged QA on the exact index |

## Verification Plan

Recovery runs before removal. Staged QA runs on the exact disposition index in
a worktree without the ignored `graphify-out/` directory.

## Risks & Mitigations

- An unobserved external consumer loses a path. Each unit stays recoverable
  from its envelope commit.
- A removal row is malformed. The assessment validator rejects it before
  commit.

## Completion Criteria

Both criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
