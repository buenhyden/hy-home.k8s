---
title: "Stage 99 Contract Cleanup Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0142-PLAN-0001"
parent_ids: ["SPEC-0142"]
---

# Stage 99 Contract Cleanup Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- A failing regression test is written before each code change.
- The `.secrets.baseline` line move lands in its own commit before the
  registry edit.

## Overview

This plan executes [SPEC-0142](spec.md) on branch
`docs/requirements-conformance` after commit `90c15f94`.

## Context

The 2026-11-05 Stage 99 audits found the stale and dead items listed in the
Spec. [ADR-0055](../../02.architecture/decisions/0055-governance-decision-current-state-amendment.md)
already records the retired Archive modes in governance terms. Rollback is
reverting the implementing commits; no migration is needed.

## Goals & In-Scope

Close VAL-S99-001 to VAL-S99-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-S99-001](spec.md#success-criteria--verification-plan) | Refuse a Stage 00 promotion target; reword the Plan form, the validator message and the governance sentence | None | [Task](tasks/tsk-0001-stage99-contract-cleanup.md) | New lifecycle regression FAIL then PASS |
| WORK-002 | [VAL-S99-002](spec.md#success-criteria--verification-plan) | Replace the ADR form trace cells with author prompts | None | [Task](tasks/tsk-0001-stage99-contract-cleanup.md) | Template and profile checks |
| WORK-003 | [VAL-S99-003](spec.md#success-criteria--verification-plan) | Move the secret-scan baseline line, then remove the unused modes, dead branches, schema definition and language entry | None | [Task](tasks/tsk-0001-stage99-contract-cleanup.md) | New schema regression FAIL then PASS; code search |
| WORK-004 | [VAL-S99-004](spec.md#success-criteria--verification-plan) | Correct the Stage 99 README and AGENTS prose | WORK-001, WORK-002, WORK-003 | [Task](tasks/tsk-0001-stage99-contract-cleanup.md) | Document suite and strict document checks |

## Verification Plan

Run the new regressions red then green, the document contract suite, the
strict document checks and `python3 scripts/qa.py staged` on each commit.

## Risks & Mitigations

- A test fixture may still use mode `evidence`; the document suite run before
  and after shows it, and the fixture changes with the code.
- The comparison base holds the old registry; the staged lifecycle check is
  run before each commit.

## Completion Criteria

VAL-S99-001 to VAL-S99-004 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Profile modes and Plan promotion owners | [Document lifecycle](../../../.agents/governance/document-lifecycle.md) | Current Contract, Plan promotion rule |
