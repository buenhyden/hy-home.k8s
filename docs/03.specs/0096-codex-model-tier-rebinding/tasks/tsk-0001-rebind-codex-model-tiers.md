---
title: "Rebind Codex Model Tiers"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0096-TSK-0001"
---

# Task: Rebind Codex Model Tiers

## Overview

Execute [SPEC-0096-PLAN-0001](../plan.md). On 2026-09-27 the request owner
asked for the `top` and `worker` roles to be researched and analyzed, and for
their Codex models to be improved.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- `.agents/governance/model-selection.md`, `.agents/roles/registry.json`, and `.codex/provider.md`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-CMT-001 | Research both tiers and check the catalog | platform | Done | Rationale in the Spec; catalog check below | [Research](#research-2026-09-27) |
| WORK-002 | VAL-CMT-002 | Rebind `top` to `gpt-6-astra` | platform | Queued | Pending | Governance validator |
| WORK-003 | VAL-CMT-003 | Observe one spawn per tier and close | platform | Queued | Pending | Codex session record |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/roles/registry.json`, `.codex/agents/*.toml`, `.codex/provider.md`, and this package
- **Forbidden Paths**: Claude projections and bindings; permission classes; credentials and private configuration beyond the project trust entry the user approved
- **Approval Required**: the request owner asked for the change. Push and merge stay with the request owner.
- **Static Validation**: `python3 scripts/validate-agent-governance.py --root .` and `python3 scripts/qa.py staged`
- **Live Validation**: one `--sandbox read-only` Codex session that spawns a read-only role per tier
- **Secret / Vault Handling**: no credential is read or recorded
- **Rollback Plan**: revert the rebinding commit; the fallback for `top` is `gpt-6-sol`
- **Evidence Location**: this Task

## Verification Summary

### Research (2026-09-27)

- **Tiers**: `top` holds supervisor, architect, governance-steward,
  incident-responder, and security-auditor. `worker` holds the twelve other
  roles. Model selection defines `top` as "the strongest permitted capability"
  and `worker` as "a bounded capable model".
- **Catalog** (`codex debug models`, `codex-cli 0.155.1`, ChatGPT account):
  `gpt-6-astra` ("Frontier intelligence for the most demanding work",
  efforts low to ultra), `gpt-6-sol` ("Workhorse model for coding and everyday
  work", low to ultra), `gpt-6-luna` ("Fast and affordable model for easier
  tasks", low to max), the older `gpt-5.6-*` models, and `gpt-5.5` ("Legacy
  coding model", low to xhigh). `gpt-5.3-codex-spark` is absent.
- **Documentation**: the [models page](https://learn.chatgpt.com/docs/models)
  recommends Astra for complex end-to-end workflows, Sol for everyday and
  intricate coding, and Luna for clear, repeatable operations. It retires
  `gpt-5.5` from Codex on 2026-10-14. The
  [subagents page](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  notes that subagent workflows spend more tokens than single-agent runs.
- **Decision**: `top` binds `gpt-6-astra`, and `worker` stays on `gpt-6-sol`.
  Efforts are unchanged, and each one is supported by its model.
  `gpt-6-luna` is not chosen for any tier, because no role here does
  extraction-style work.

## Traceability

- Stable Task: `SPEC-0096-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Research above |
| [WORK-002](../plan.md#work-breakdown) | Queued | Pending |
| [WORK-003](../plan.md#work-breakdown) | Queued | Pending |
