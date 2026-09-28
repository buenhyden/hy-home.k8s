---
title: "Closed Package Retention Implementation Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0095-PLAN-0001"
---

# Closed Package Retention Implementation Plan (Plan)

## Global Constraints

The request owner approved archiving the finished packages on 2026-09-27. No
frozen record, sealed ledger, or retained body is rewritten. Each logical
commit runs staged QA over its exact index. Push and merge stay with the
request owner.

## Overview

This Plan executes [Spec 0095](spec.md) in one move commit whose Retention
Envelope is `576a8927`.

## Context

SPEC-0094 deferred SPEC-0086 until its closure reached the default branch.
PR #102 merged that closure, together with SPEC-0094 itself.

## Goals & In-Scope

Retain SPEC-0086 and SPEC-0094 in `completed/` and move every current consumer
in the same commit.

## Non-Goals & Out-of-Scope

No SPEC-0008 move, no registry change, no rewrite of a retained body.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose this package and record the survey | None | PR #102 merged | The Task records each unit and its consumers |
| WP-002 | Retain both packages in `completed/`, repointing their current citations | WP-001 | The envelope is on the default branch | Lifecycle, link, and archive gates |
| WP-003 | Record the results and close this package | WP-002 | Staged QA passes | Staged QA |

## Verification Plan

Each work package runs `python3 scripts/qa.py staged` on its exact index. The
archive contract tests and the archive cutover gate run on the move commit.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A code-span path in a provider note keeps the old location | The consumer survey includes non-link path mentions |
| The archive report's Git process budget shifts | Run the budget test on a branch checkout and record the result |

## Completion Criteria

WP-001 to WP-003 pass their exit evidence, and every retained unit equals its
envelope object.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CPR-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retain-closed-packages.md) |
| [VAL-CPR-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retain-closed-packages.md) |
| [VAL-CPR-003](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retain-closed-packages.md) |
