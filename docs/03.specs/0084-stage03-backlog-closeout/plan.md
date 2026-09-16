---
title: "Stage 03 Backlog Closeout Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0084-PLAN-0001"
---

# Stage 03 Backlog Closeout Implementation Plan (Plan)

## Global Constraints

The request owner approved this round on 2026-09-16, including the two registry
gap-fills, the frontmatter reader consolidation, and the retention moves. No
frozen record, sealed ledger, or retained body is rewritten. No archive stage
directory is created. Push, pull request, and merge stay with the request owner.
Each logical commit runs staged QA over its exact index, and the final tree runs
one full QA.

## Overview

This Plan executes [Spec 0084](spec.md) in one integration, ordered so that each
commit carries its own justification: the owning package first, then the
contract gaps it declares, then the dispositions those gaps unblock, then the
retentions, then the repairs the retentions prove necessary.

## Context

[SPEC-0083](../0083-finished-package-retention/spec.md) surveyed the sixteen
remaining packages and returned two blocked dispositions to the request owner.
This round decides them.

## Goals & In-Scope

Move every remaining Stage 03 package to the terminal state its recorded
evidence supports or to a dated disposition note naming why it stays; close the
two registry gaps that block two of those moves; resolve the duplicated
frontmatter readers; retain every unit that reaches a terminal state; and repair
the consumers those retentions move.

## Non-Goals & Out-of-Scope

No new archive stage directory, no edge or key beyond the two named, no
native-runtime claim, no rewrite of a frozen body, and no decision on SPEC-0008,
which owns a current contract that six accepted ADRs name as their Spec.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose this package and record the survey of every remaining package | None | The request owner approved the round | The Task records each package, its anchor state, and its consumers |
| WP-002 | Close the two registry gaps as gap-fills | WP-001 | This package is active and declares them | The registry diff adds one optional key and one edge, and the lifecycle gate passes |
| WP-003 | Close SPEC-0071 and SPEC-0078 | WP-002 | Both record complete evidence | Lifecycle gate |
| WP-004 | Close SPEC-0062 after cancelling its three unexecutable Tasks | WP-003 | Its own record states the blockers | Lifecycle gate |
| WP-005 | Close SPEC-0054 after cancelling WP-009 and closing WP-013 and WP-014 | WP-004 | Its own record states the evidence | Lifecycle gate |
| WP-006 | Withdraw SPEC-0048 and SPEC-0051 and cancel their twelve Tasks | WP-002 | Both carry a dated note recommending withdrawal | Lifecycle gate |
| WP-007 | Repair SPEC-0006's stale sibling path, close it, and record the disposition note of every package that stays | WP-002 | The survey names them | Link gate and the Task |
| WP-008 | Resolve the duplicated frontmatter readers under `scripts/` to one owner | WP-001 | SPEC-0077 records the duplication and no blocker | Unit tests and full QA with no output change |
| WP-009 | Close SPEC-0077 with its two authority-blocked criteria recorded as deferrals | WP-008 | WP-008 landed | Lifecycle gate and the Task |
| WP-010 | Retain every package that reached a terminal state, with consumers moved first | WP-003 to WP-009 | Every member of each unit is terminal | Link, lifecycle, and archive gates |
| WP-011 | Repair the consumers the retention proves wrong | WP-010 | Full QA named the failing gates | Full QA and the unit-test suite with no pin lowered |
| WP-012 | Record the results and close this package | WP-001 to WP-011 | Full QA on the final tree | Staged and full QA |

## Verification Plan

Each work package runs its focused checks first: the lifecycle gate for each
edge, the link gate for repointing, `python3 scripts/run-archive-contract-tests.py --root .`
for the retention contract, and `python3 scripts/qa.py staged` for each logical
commit. The final tree runs one `python3 scripts/qa.py full`. Hosted results are
recorded only when observed.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A registry gap-fill silently widens more than intended | The diff is two additions, reviewed line by line, and the lifecycle gate re-runs over the whole corpus |
| Cancelling a Task discards real evidence | Each cancellation quotes the record's own blocker; an item with accepted evidence is closed rather than cancelled |
| Retaining SPEC-0054 breaks the fixtures that use it as a live package | The two fixtures are repaired in WP-011, in the same round, exactly as SPEC-0083 repaired its own |
| Retaining SPEC-0062 breaks the secret-scan allowlist that names a path inside its Plan | The allowlist entry moves with the retention in WP-011 |
| Consolidating the frontmatter readers changes a gate's output | WP-008 lands before any retention, so a changed output is attributed to the consolidation and not to a move |
| Sixty-odd edges in one change hide a mistake | One commit per disposition class, with staged QA over each exact index |

## Completion Criteria

WP-001 to WP-012 pass their exit evidence, every frozen file is unmodified, and
the final tree passes staged and full QA.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SBC-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-003](spec.md#success-criteria--verification-plan) | WP-003 to WP-005 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-004](spec.md#success-criteria--verification-plan) | WP-006 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-005](spec.md#success-criteria--verification-plan) | WP-007 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-006](spec.md#success-criteria--verification-plan) | WP-010 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-007](spec.md#success-criteria--verification-plan) | WP-007 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-008](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-009](spec.md#success-criteria--verification-plan) | WP-010 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-010](spec.md#success-criteria--verification-plan) | WP-011 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-011](spec.md#success-criteria--verification-plan) | WP-009 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
| [VAL-SBC-012](spec.md#success-criteria--verification-plan) | WP-012 | [tsk-0001](tasks/tsk-0001-close-the-stage-03-backlog.md) |
