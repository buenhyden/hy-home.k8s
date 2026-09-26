---
title: "Finished Package Retention Implementation Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0094-PLAN-0001"
---

# Finished Package Retention Implementation Plan (Plan)

## Global Constraints

The request owner approved this round on 2026-09-27. No frozen record, sealed
ledger, or retained body is rewritten, and no registry, profile, state, or edge
changes. Each logical commit runs staged QA over its exact index. Push and
merge stay with the request owner.

## Overview

This Plan executes [Spec 0094](spec.md) in one move commit whose Retention
Envelope is `fbcafca1`, which the default branch holds.

## Context

SPEC-0087 retained the previous terminal packages. Since then, eight more packages have
finished.

## Goals & In-Scope

Retain the eight `done` packages in `completed/` and move every current
consumer in the same commit.

## Non-Goals & Out-of-Scope

No SPEC-0008 or SPEC-0086 move, no registry change, no rewrite of a retained
body, and no lowered gate, test pin, or allowlist.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose this package and record the approval and the survey | None | The request owner approved the round | The Task records each unit, its anchor state, and its consumers |
| WP-002 | Retain the eight packages in `completed/`, repointing their current citations | WP-001 | Every member is terminal and the envelope is on the default branch | Lifecycle, link, and archive gates |
| WP-003 | Record the results and close this package | WP-002 | Staged QA passes | Staged QA |

## Verification Plan

Each work package runs `python3 scripts/qa.py staged` on its exact index. The
archive contract tests run on the move commit.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A move names a commit the default branch does not hold | The envelope is the default-branch tip this branch starts from |
| A current document keeps a link to an old path | The link gate runs over the whole corpus in the move commit |
| The archive report's Git process budget shifts | Measure it and record the delta, as earlier rounds did |

## Completion Criteria

WP-001 to WP-003 pass their exit evidence, and every retained unit equals its
envelope object.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-FPR-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-003](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-004](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
