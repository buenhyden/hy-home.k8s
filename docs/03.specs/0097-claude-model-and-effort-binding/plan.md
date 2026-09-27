---
title: "Claude Model and Effort Binding Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0097-PLAN-0001"
---

# Claude Model and Effort Binding Implementation Plan (Plan)

## Global Constraints

The request owner asked for this change on 2026-09-27 and asked for Fable 5.1
to be kept to a minimum. Only Claude model and effort values, and the rules
that own them, change. Tool scopes, tier membership, and Codex bindings stay as
they are. Push and merge stay with the request owner.

## Overview

This Plan executes [Spec 0097](spec.md): add a Claude effort binding, let a role
depart from its Claude model, bind Fable only to the planning roles, and record
the `Grep` and `Glob` gap.

## Context

SPEC-0096 gave Codex a per-role model override and Astra only for the planning
roles. The Claude side had no effort binding and no model override.

## Goals & In-Scope

Registry, schema, validator, tests, the 17 Claude projections, the
model-selection policy, the Claude provider note, and this package.

## Non-Goals & Out-of-Scope

No tool scope change, no Codex change, and no user-level setting.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Research the Claude subagent contract and the tool gap | None | Request owner's ask | Spec Overview and the Task |
| WP-002 | Add the Claude effort binding and overrides, bind Fable to the planning roles, and sync the projections | WP-001 | Failing unit tests for the Claude effort rule | Unit tests, governance validator, staged QA |
| WP-003 | Observe the applied model and effort in new sessions, and close | WP-002 | Changed projections on disk | Transcript records in the Task |

## Verification Plan

Run the unit tests, the governance validator, and `python3 scripts/qa.py staged`
on each commit. Spawn roles from a new `claude -p --model sonnet` session,
because a running session keeps the definitions it loaded, and read each
subagent transcript's `model` and `effort`.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A running session keeps the old definitions | Verify in a new headless session |
| Fable spreads to practical roles | Only two roles declare the override, and the validator rejects drift |
| The tool gap blocks search for roles without `Bash` | Record it with an owner. Granting `Bash` is a separate permission decision |

## Completion Criteria

VAL-CMB-001 to VAL-CMB-004 pass and the Task records the evidence.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CMB-001](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-bind-claude-model-and-effort.md) |
| [VAL-CMB-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-bind-claude-model-and-effort.md) |
| [VAL-CMB-003](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-bind-claude-model-and-effort.md) |
| [VAL-CMB-004](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-bind-claude-model-and-effort.md) |
