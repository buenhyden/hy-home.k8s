---
title: "Agent Surface Conformance Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0144-PLAN-0001"
parent_ids: ["SPEC-0144"]
---

# Agent Surface Conformance Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- A failing regression test is written before each code change.
- Each audit item is verified against the code before it is changed.

## Overview

This plan executes [SPEC-0144](spec.md) on branch `docs/agents-conformance`
from `main` at `75ba7b04`.

## Context

The 2026-11-06 read-only audits of `.agents/governance/`, `.agents/roles/`,
`.agents/skills/` and the remaining `.agents/` files supply the item list.
Rollback is reverting the implementing commits; no migration is needed.

## Goals & In-Scope

Close VAL-AGC-001 to VAL-AGC-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AGC-004](spec.md#success-criteria--verification-plan) | Tests first, then the `prompt-input.py` exit-code and pathspec changes, the `ops-runbook` binding with its projections, and the schema-field removal | None | [Task](tasks/tsk-0001-agents-conformance.md) | Regression tests FAIL then PASS; agent-governance validator |
| WORK-002 | [VAL-AGC-001](spec.md#success-criteria--verification-plan) | Correct the governance files | None | [Task](tasks/tsk-0001-agents-conformance.md) | Strict document checks |
| WORK-003 | [VAL-AGC-002](spec.md#success-criteria--verification-plan) | Correct the roles README, role bodies and skills | WORK-001 | [Task](tasks/tsk-0001-agents-conformance.md) | Strict document checks, agent-governance validator |
| WORK-004 | [VAL-AGC-003](spec.md#success-criteria--verification-plan) | Correct the README, knowledge, prompts, workflows and evaluations files | WORK-001 | [Task](tasks/tsk-0001-agents-conformance.md) | Strict document checks |

## Verification Plan

Run the new regressions red then green, the agent-governance validator, the
document contract suite, the strict document checks, an independent review
of the whole diff and `python3 scripts/qa.py staged` on each commit.

## Risks & Mitigations

- A wording change could drop a rule another file relies on; each
  de-duplication keeps the owner's copy and the review checks consumers.
- A projection could fall out of step with the registry; the agent-governance
  validator compares them.

## Completion Criteria

VAL-AGC-001 to VAL-AGC-004 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
