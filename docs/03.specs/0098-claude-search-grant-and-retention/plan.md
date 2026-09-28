---
title: "Claude Search Grant and Package Retention Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0098-PLAN-0001"
---

# Claude Search Grant and Package Retention Implementation Plan (Plan)

## Global Constraints

The request owner asked for both changes on 2026-09-27. Only Claude tool
scopes, the two guardrails, and the three retained packages change. No retained
body, frozen record, or Codex binding changes. Push and merge stay with the
request owner.

## Overview

This Plan executes [Spec 0098](spec.md): grant `Bash` to the four Claude roles
that lack it, and retain SPEC-0095, SPEC-0096, and SPEC-0097.

## Context

SPEC-0097 recorded the missing search path. SPEC-0095 deferred its own
retention, and SPEC-0096 and SPEC-0097 finished afterwards.

## Goals & In-Scope

Registry scopes and overrides, the four projections, two role bodies, the tests
that pinned the no-shell roles, the provider note, and the retention move.

## Non-Goals & Out-of-Scope

No Codex change, no mutation or network right, no model change, and no rewrite
of a retained body.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Grant `Bash` and restate the two guardrails | None | Failing tests for the new contract | Unit tests, governance validator, staged QA |
| WP-002 | Retain SPEC-0095, SPEC-0096, and SPEC-0097 | None | Envelope `fc469fd1` on the default branch | Lifecycle and archive gates |
| WP-003 | Observe the scopes in a new session and close | WP-001, WP-002 | Changed projections on disk | Session record in the Task |

## Verification Plan

Run the unit tests, the governance validator, and `python3 scripts/qa.py staged`
on each commit. Run the archive contract tests and the archive cutover gate on
the move. Spawn the changed roles from a new `claude -p --model sonnet` session.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A read-only role uses its shell for live state | Its guardrail forbids it, and the write guard reports shell writes |
| A retained package is edited after the move | Retention moves whole units at the envelope commit, and the gates reject drift |

## Completion Criteria

VAL-CSR-001 to VAL-CSR-004 pass and the Task records the evidence.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CSR-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-grant-search-and-retain-packages.md) |
| [VAL-CSR-002](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-grant-search-and-retain-packages.md) |
| [VAL-CSR-003](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-grant-search-and-retain-packages.md) |
| [VAL-CSR-004](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-grant-search-and-retain-packages.md) |
