---
title: "Common Authority and Safe Authoring Plan"
version: "1.2.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0105-PLAN-0001"
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

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Trace current owners, approval callers and provider guards | None | Explicit P01 scope and observed clean baseline | Task comparison, exact source/consumer findings |
| WP-002 | Repair existing policy and executable consumers | WP-001 | Reviewed bounded findings and approved local scope | Changed owners with focused behavior checks |
| WP-003 | Independent review and local delivery | WP-002 | Reviewable final diff and available check envelope | Task lane, reviewer, logical commit and rollback evidence |

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

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-P01-001](spec.md#success-criteria--verification-plan) | WP-001 | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) |
| [VAL-P01-002](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) |
| [VAL-P01-003](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) |
| [VAL-P01-004](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) |
| [VAL-P01-005](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) |
| [VAL-P01-006](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0105-TSK-0001](tasks/tsk-0001-authority-and-authoring.md) |
| [VAL-P01-002](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0105-TSK-0002](tasks/tsk-0002-quoted-secret-output.md) |
| [VAL-P01-006](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0105-TSK-0002](tasks/tsk-0002-quoted-secret-output.md) |
