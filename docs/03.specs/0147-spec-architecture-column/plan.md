---
title: "Spec Architecture Column Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0147-PLAN-0001"
parent_ids: ["SPEC-0147"]
---

# Spec Architecture Column Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- The failing test is written before the registry change.

## Overview

This plan executes [SPEC-0147](spec.md) on branch
`docs/sdlc-cross-artifact-conformance` after `d4338908`.

## Context

The D-1 review found that the body contract already enforces exact headers
and non-empty cells. Constraining architecture is
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
Rollback is reverting the implementing commit.

## Goals & In-Scope

Close VAL-ARCH-001 and VAL-ARCH-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ARCH-001](spec.md#success-criteria--verification-plan) | Focused test first, then add the column to the registry | None | [Task](tasks/tsk-0001-spec-architecture-column.md) | Test FAIL then PASS |
| WORK-002 | [VAL-ARCH-002](spec.md#success-criteria--verification-plan) | Update the Spec template and the Spec fixtures | WORK-001 | [Task](tasks/tsk-0001-spec-architecture-column.md) | Strict document checks and unit tests |

## Verification Plan

Run the focused test red then green, the affected unit tests, the strict
document checks and `python3 scripts/qa.py staged`. Architecture compliance
check: every work unit edits only the Stage 99 form owner and its tests, the
split AD-0006 assigns.

## Risks & Mitigations

- An unlisted consumer may build a Spec table; the full document and
  Task-contract test suites run after the change.

## Completion Criteria

VAL-ARCH-001 and VAL-ARCH-002 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Spec Lifecycle Traceability carries an Architecture column | [Software Development Lifecycle](../../../.agents/governance/sdlc.md) | Current Contract, `Cross-artifact conformance` |
