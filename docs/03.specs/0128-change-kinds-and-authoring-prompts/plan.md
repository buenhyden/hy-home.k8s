---
title: "Change Kinds and Authoring Prompts Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0128-PLAN-0001"
parent_ids: ["SPEC-0128"]
---

# Change Kinds and Authoring Prompts Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No existing document is rewritten to satisfy the new rule.

## Overview

This plan executes [SPEC-0128](spec.md) on branch
`feat/sdlc-change-kinds-and-prompts` from main `71c59deb`.

## Context

SPEC-0125 named CR-06.04, 06.07, 06.09, 06.10 and 07.04 as slice C.
Architecture, interfaces, migration and rollback: no architecture view or
ADR changes; the validator keeps its call signature through a keyword
default; rollback is a revert.

## Goals & In-Scope

Close VAL-CK-001 to VAL-CK-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CK-001](spec.md#success-criteria--verification-plan) | Add the change-kind table and touchpoint sentences | None | [Task](tasks/tsk-0001-change-kinds-and-authoring-prompts.md) | Governance review |
| WORK-002 | [VAL-CK-002](spec.md#success-criteria--verification-plan) | Add the Spec, Plan and Task prompts | None | [Task](tasks/tsk-0001-change-kinds-and-authoring-prompts.md) | Template tests |
| WORK-003 | [VAL-CK-003](spec.md#success-criteria--verification-plan) | Reject link-only instruction sections | None | [Task](tasks/tsk-0001-change-kinds-and-authoring-prompts.md) | Profile validator tests |
| WORK-004 | [VAL-CK-004](spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | WORK-001 to WORK-003 | [Task](tasks/tsk-0001-change-kinds-and-authoring-prompts.md) | Staged QA and hosted checks |

## Verification Plan

The link-only test fails before the validator change and passes after it;
the profile validator then runs over the whole repository.

## Risks & Mitigations

- The rule breaks existing documents. A repository-wide run before the
  change found none that fail.
- The table restates owners. Each row links the owner instead.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Change kinds and their minimum records, checks and approval | [SDLC policy](../../../.agents/governance/sdlc.md) | Change kinds |
