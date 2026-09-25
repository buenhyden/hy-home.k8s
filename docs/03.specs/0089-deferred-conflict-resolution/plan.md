---
title: "Deferred Conflict Resolution Implementation Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0089-PLAN-0001"
---

# Deferred Conflict Resolution Implementation Plan

## Global Constraints

The request owner authorized this round and its local commits on 2026-09-25.
Push, pull request, merge, remote protection, Stage 98 moves, and live systems
are not authorized. Each commit runs staged QA over its exact index.

## Overview

This Plan executes [Spec 0089](spec.md) as five local commits and ends with
full QA on the final tree.

## Context

SPEC-0088 deferred four conflicts. The open packages are SPEC-0008 (spec
active, plan and Task done), SPEC-0049 (draft, seven Tasks queued), and
SPEC-0086 (draft, one Task queued). The survey is recorded in the Task.

## Goals & In-Scope

Resolve the four deferrals and withdraw or correct each open package that
conflicts with current authority.

## Non-Goals & Out-of-Scope

No new platform validator for the SPEC-0049 scope, no manifest change, and no
move into `98.archive/retired/` in this round.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose this package and record the survey | None | Request approval | Task survey |
| WP-002 | Declare covered gates and scope English-first by registry state, test-first | WP-001 | Survey | Focused tests and staged QA |
| WP-003 | Correct ADR-0031 and AD-0006 | WP-001 | Survey | Link gate and staged QA |
| WP-004 | Withdraw SPEC-0049 and its Plan, open its Tasks for cancellation, and update its current consumers | WP-001 | Conflict evidence | Lifecycle and link gates |
| WP-005 | Cancel the SPEC-0049 Tasks, record evidence, and close | WP-002 to WP-004 | Every earlier commit passes staged QA | Full QA |

## Verification Plan

Each work package runs its focused gates, then `python3 scripts/qa.py staged`.
WP-005 runs `python3 scripts/qa.py full`. Hosted `ci-summary` is not observed.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A registry edit leaves the routing contract invalid and the write guard blocks every tool | Validate the candidate registry in memory and write it only after it passes |
| Withdrawing SPEC-0049 erases its unowned requirement gap | Record the gap and its next owner at REQ-0004 |
| A covered gate silently stops running | The covered gate stays in quick and staged, and its coverer must be in full |

## Completion Criteria

WP-001 to WP-005 meet their exit evidence and the final tree runs full QA.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-DCR-001](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-resolve-deferred-conflicts.md) |
| [VAL-DCR-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-resolve-deferred-conflicts.md) |
| [VAL-DCR-003](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-resolve-deferred-conflicts.md) |
| [VAL-DCR-004](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-resolve-deferred-conflicts.md) |
| [VAL-DCR-005](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-resolve-deferred-conflicts.md) |
| [VAL-DCR-006](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0001](tasks/tsk-0001-resolve-deferred-conflicts.md) |
