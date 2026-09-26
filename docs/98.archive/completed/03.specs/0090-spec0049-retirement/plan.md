---
title: "SPEC-0049 Retirement Implementation Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0090-PLAN-0001"
---

# SPEC-0049 Retirement Implementation Plan (Plan)

## Global Constraints

The request owner approved the move and the push of the resulting commits on
2026-09-25. No retained body, frozen record, or sealed ledger is rewritten, and
no registry, profile, state, or edge changes. Each commit runs staged QA over
its exact index.

## Overview

This Plan executes [Spec 0090](spec.md) as three local commits.

## Context

SPEC-0089 left SPEC-0049 withdrawn with its seven Tasks cancelled in commit
`62ed8f05`, and deferred the move until that commit reached the default branch.

## Goals & In-Scope

Retain SPEC-0049 in `retired/03.specs/`, rewrite its current links in the same
commit, and record the evidence.

## Non-Goals & Out-of-Scope

No other package, no registry change, no rewrite of a retained body, and no
lowered gate.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose this package and record the approval and survey | None | The request owner approved the move | Task survey |
| WP-002 | Retain SPEC-0049 in `retired/` and rewrite its current links | WP-001 | Every member is terminal and `62ed8f05` is on the default branch | Lifecycle, link, and archive gates |
| WP-003 | Record the results and close this package | WP-002 | WP-002 passes staged QA | Staged QA |

## Verification Plan

Each work package runs the gates it touches, then `python3 scripts/qa.py
staged` on its exact index. Hosted `ci-summary` is not observed.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| The envelope commit is not on the default branch | WP-002 is validated only after `62ed8f05` is pushed |
| A current document keeps a link to the retired unit | The link gate runs over the whole corpus in the move commit |

## Completion Criteria

WP-001 to WP-003 pass their exit evidence and the retained unit equals its
envelope tree.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SRT-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retire-spec-0049.md) |
| [VAL-SRT-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retire-spec-0049.md) |
| [VAL-SRT-003](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retire-spec-0049.md) |
| [VAL-SRT-004](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-retire-spec-0049.md) |
