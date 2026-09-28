---
title: "Codex Model Tier Rebinding Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0096-PLAN-0001"
---

# Codex Model Tier Rebinding Implementation Plan (Plan)

## Global Constraints

The request owner asked for this change on 2026-09-27 and asked for
`gpt-6-astra` use to be kept to a minimum. Only Codex model values and the rule
that owns a role's model departure change. Reasoning effort, tier membership,
permission classes, and Claude bindings stay as they are. Push and merge stay
with the request owner.

## Overview

This Plan executes [Spec 0096](spec.md): bind both Codex tiers to `gpt-6-sol`,
give supervisor and architect a declared `gpt-6-astra` override, and observe the
applied model and effort.

## Context

The `worker` tier was rebound to `gpt-6-sol` after a failed spawn. The `top`
tier bound `gpt-5.5`, which the catalog marks as legacy and which retires from
Codex on 2026-10-14. The registry had no way to vary a model per role.

## Goals & In-Scope

Add `native_model_override` to the registry, its schema, and its validator
rule. Bind both tiers to `gpt-6-sol` and supervisor and architect to
`gpt-6-astra`. Record the catalog, the rationale, and the spawn evidence.

## Non-Goals & Out-of-Scope

No effort change, no tier membership change, no Claude change, and no account
or usage setting.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Research both tiers and record the rationale | None | Request owner's ask | Spec Core Design and the Task |
| WP-002 | Add the model override rule, rebind the tiers, and sync the projections | WP-001 | A failing unit test for the override rule | Unit tests, governance validator, staged QA |
| WP-003 | Observe the applied model and effort, and close | WP-002 | Trusted project layer | Rollout records in the Task |

## Verification Plan

Run the unit tests, the governance validator, and `python3 scripts/qa.py staged`
on each commit. Check the catalog with `codex debug models`. Spawn roles in a
`codex exec -m gpt-6-sol --sandbox read-only` session, so the parent does not use
the client default `gpt-6-astra`. Read the applied model and effort from each
spawned thread's rollout record.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| An override becomes a second model authority | The override lives in the registry beside the tier binding, and the validator resolves both |
| Sol at `xhigh` is too weak for a `top` assignment | Escalation to Astra is a recorded, per-assignment decision |
| A probe session silently uses `gpt-6-astra` | Probes pass `-m gpt-6-sol` |

## Completion Criteria

VAL-CMT-001 to VAL-CMT-004 pass and the Task records the evidence.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CMT-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-rebind-codex-model-tiers.md) |
| [VAL-CMT-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-rebind-codex-model-tiers.md) |
| [VAL-CMT-003](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-rebind-codex-model-tiers.md) |
| [VAL-CMT-004](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-rebind-codex-model-tiers.md) |
