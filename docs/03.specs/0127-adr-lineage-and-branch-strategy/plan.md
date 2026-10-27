---
title: "ADR Lineage and Branch Strategy Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0127-PLAN-0001"
parent_ids: ["SPEC-0127"]
---

# ADR Lineage and Branch Strategy Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to branch protection, rulesets or GitHub settings.

## Overview

This plan executes [SPEC-0127](spec.md) on branch
`feat/adr-lineage-and-branch-strategy` from main `0058fe3c`.

## Context

SPEC-0124 recorded the ADR source; SPEC-0125 named CR-09.06 and CR-13.07
for this slice; SPEC-0126 completed the architecture views.

## Goals & In-Scope

Close VAL-AB-001 to VAL-AB-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AB-001](spec.md#success-criteria--verification-plan) | Reject supersession chains without a current decision | None | [Task](tasks/tsk-0001-adr-lineage-and-branch-strategy.md) | Lifecycle tests |
| WORK-002 | [VAL-AB-002](spec.md#success-criteria--verification-plan) | Add the template prompt and the numbering rule | None | [Task](tasks/tsk-0001-adr-lineage-and-branch-strategy.md) | Template tests and review |
| WORK-003 | [VAL-AB-003](spec.md#success-criteria--verification-plan) | Record ADR-0052 and link it from `git.md` | None | [Task](tasks/tsk-0001-adr-lineage-and-branch-strategy.md) | Review and operator acceptance |
| WORK-004 | [VAL-AB-004](spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | WORK-001 to WORK-003 | [Task](tasks/tsk-0001-adr-lineage-and-branch-strategy.md) | Staged QA and hosted checks |

## Verification Plan

The cycle test fails before the validator change and passes after it; the
positive test passes in both.

## Risks & Mitigations

- The chain walk rejects a legitimate history. Strict validation over the
  current repository and the positive test guard it.
- ADR-0052 is read as accepted before the operator decides. It stays
  `proposed` until the acceptance commit.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Single long-lived `main` branch | [Git policy](../../../.agents/governance/git.md) | Branch and integration routing |
| ADR numbers are never reused | [ADR-0030](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) | Traceability |
