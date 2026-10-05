---
title: "Common Authority and Safe Authoring Plan"
version: "1.2.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0105-PLAN-0001"
parent_ids: ["SPEC-0105"]
---

# Common Authority and Safe Authoring Implementation Plan

## Global Constraints

Approval and safety owns authorization; agent execution owns instruction
precedence and conflict routing; quality owns validation and resource limits.
Preserve read-only reviewers, native sandbox controls and frozen evidence.
No remote push, PR, merge, archive disposition, secrets or deployment is authorized.
Task owns all execution state. A structural check never authenticates approval.

## Overview

The original [Task](tasks/tsk-0001-authority-and-authoring.md) implemented
[SPEC-0105](spec.md). The authorized bounded
[follow-up Task](tasks/tsk-0002-quoted-secret-output.md) repairs one missed
scanner form under WP-002 and records review and local delivery under WP-003.

## Context

The observed baseline is clean `main` at the supplied investigation revision
`f6501e46a0d35858c598c207e726a0e89c92d7d7`. Stage 03 has no package and
SPEC-0104 is retained history. Repository checks, not the request's checkbox,
determine implementation results. Unavailable K03/K06/K11 evidence registers
are replaced by direct baseline source inspection.

## Goals & In-Scope

Trace conflicting rules; repair safe-authoring handling, authorization wording
and resource boundaries; retain minimal negative/positive executable checks;
deliver local logical commits and evidence.

## Non-Goals & Out-of-Scope

No new taxonomy, approval identity provider, global configuration, private
memory or plugin changes. No archived execution restart, source rewriting,
remote integration, runtime capability assertion or live operation.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-P01-001](spec.md#success-criteria--verification-plan) | WP-001: trace current owners, approval callers and provider guards | None; explicit P01 scope and clean baseline | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) | Source and consumer comparison in the Task |
| WORK-002 | [VAL-P01-002](spec.md#success-criteria--verification-plan), [VAL-P01-003](spec.md#success-criteria--verification-plan), [VAL-P01-004](spec.md#success-criteria--verification-plan), [VAL-P01-005](spec.md#success-criteria--verification-plan) | WP-002: repair authorized owners and consumers | WP-001; reviewed findings and approved scope | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) | Changed-owner review and focused checks in the Task |
| WORK-003 | [VAL-P01-006](spec.md#success-criteria--verification-plan) | WP-003: independent review and local delivery | WP-002; reviewable diff and check envelope | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) | Task lane, reviewer, commit and rollback evidence |
| WORK-004 | [VAL-P01-002](spec.md#success-criteria--verification-plan) | WP-002 follow-up: repair quoted Secret output scanner | Completed original WP-002; new authorized follow-up scope | [SPEC-0105-TSK-0002](tasks/tsk-0002-quoted-secret-output.md) | Focused regression and independent re-review in the Task |
| WORK-005 | [VAL-P01-006](spec.md#success-criteria--verification-plan) | WP-003 follow-up: validate and commit local handoff | WORK-004; reviewable follow-up diff | [SPEC-0105-TSK-0002](tasks/tsk-0002-quoted-secret-output.md) | Full QA, message and commit evidence in the Task |

## Verification Plan

Use subagent-driven-development for disjoint implementation and read-only
review, with explicit paths and existing role procedures. Repository Task
replaces any external skill's separate progress ledger; canonical Stage 03
forms replace external docs/plans defaults. Run focused checks for executable
changes, affected and exact-index gates, and one local full delivery gate.
Refresh changed inputs only; do not rerun identical full/unit leaves through
multiple routes. No artificial RED/GREEN is required for prose.

## Risks & Mitigations

Over-broad keyword exceptions could hide actual action claims: test both inert
examples and affirmative execution claims. Approval metadata could be mistaken
for identity: keep the trusted operator decision distinct and fail closed on
unavailable source. Native sandbox startup is unavailable for some shell calls:
use only supported bounded approval requests and record the limitation.

## Completion Criteria

All Spec criteria have observed evidence and independent review. Required
checks pass over declared inputs; external evidence remains unobserved.
Commit with effective hooks; preserve a failed hook as a blocker. Roll back
only this branch's logical changes by reviewed forward reverts when authorized.
Do not mark incomplete checks or protected actions as completed.
