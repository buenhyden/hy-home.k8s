---
title: "Codex Model Tier Rebinding Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0096-PLAN-0001"
---

# Codex Model Tier Rebinding Implementation Plan (Plan)

## Global Constraints

The request owner asked for this change on 2026-09-27. Only Codex model values
change. Reasoning effort, tier membership, permission classes, and Claude
bindings stay as they are. Push and merge stay with the request owner.

## Overview

This Plan executes [Spec 0096](spec.md): rebind the Codex `top` tier, record
the rationale for both tiers, and observe one spawn per tier.

## Context

The `worker` tier was rebound to `gpt-6-sol` after a failed spawn. The `top`
tier still binds `gpt-5.5`, which the catalog marks as legacy and which
retires from Codex on 2026-10-14.

## Goals & In-Scope

Bind `top` to `gpt-6-astra`, keep `worker` on `gpt-6-sol`, and record the
catalog and spawn evidence.

## Non-Goals & Out-of-Scope

No effort change, no per-role model override, no schema change, no Claude
change, and no account or usage setting.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Research both tiers and record the rationale | None | Request owner's ask | Spec Core Design and the Task |
| WP-002 | Rebind `top` in the registry and in its five projections | WP-001 | Catalog lists `gpt-6-astra` | Governance validator and staged QA |
| WP-003 | Observe one spawn per tier and close | WP-002 | Trusted project layer | Task session record |

## Verification Plan

Run the governance validator and `python3 scripts/qa.py staged` on each commit,
check the catalog with `codex debug models`, and spawn one read-only role per
tier in a `--sandbox read-only` session.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Astra usage limits bind sooner than the legacy model's | `gpt-6-sol` is the documented fallback, and switching to it is a one-value registry change |
| Higher cost per `top` spawn | Keep bounded work on `worker`, as model selection already requires |
| The catalog changes again | Re-run the catalog check and record it, rather than carrying a dated result forward |

## Completion Criteria

VAL-CMT-001 to VAL-CMT-003 pass and the Task records the evidence.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CMT-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-rebind-codex-model-tiers.md) |
| [VAL-CMT-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-rebind-codex-model-tiers.md) |
| [VAL-CMT-003](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-rebind-codex-model-tiers.md) |
