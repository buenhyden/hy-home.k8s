---
title: "Dead Profile Mode Cleanup Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0143-PLAN-0001"
parent_ids: ["SPEC-0143"]
---

# Dead Profile Mode Cleanup Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- The failing regression test is written before the code change.

## Overview

This plan executes [SPEC-0143](spec.md) on branch
`refactor/dead-profile-modes` from `main` at `0b00f3a3`.

## Context

SPEC-0142 removed the schema modes `evidence` and `generated` and noted that
`frontmatter-free` and `classification-only` remained in the loader types and
validators. Rollback is reverting the implementing commit; no migration is
needed.

## Goals & In-Scope

Close VAL-DPM-001 and VAL-DPM-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DPM-001](spec.md#success-criteria--verification-plan) | Add the type regression test, then narrow the two `Literal` types | None | [Task](tasks/tsk-0001-dead-profile-mode-cleanup.md) | New regression FAIL then PASS |
| WORK-002 | [VAL-DPM-002](spec.md#success-criteria--verification-plan) | Remove the unreachable branches and the helper code only they used | WORK-001 | [Task](tasks/tsk-0001-dead-profile-mode-cleanup.md) | Code search, document suite, strict document checks, repository quality check |

## Verification Plan

Run the new regression red then green, the document contract suite, the
strict document checks, the repository quality check and
`python3 scripts/qa.py staged` on each commit.

## Risks & Mitigations

- A removed branch could have been reachable through a path the search
  missed; the document suite and strict checks over the whole tree run
  before and after.

## Completion Criteria

VAL-DPM-001 and VAL-DPM-002 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
