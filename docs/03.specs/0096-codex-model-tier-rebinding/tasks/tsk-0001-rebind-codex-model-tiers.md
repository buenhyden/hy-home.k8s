---
title: "Rebind Codex Model Tiers"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
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
| WORK-002 | VAL-CMT-002, VAL-CMT-004 | Add the model override rule, rebind the tiers, and sync the projections | platform | Done | Both tiers bind `gpt-6-sol`; supervisor and architect override to `gpt-6-astra` | Unit tests, governance validator, staged QA |
| WORK-003 | VAL-CMT-003 | Observe the applied model and effort, and close | platform | Done | Six roles applied their bound model and effort | [Spawn](#spawn-2026-09-27) |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/roles/registry.json` and its schema, `scripts/validate-agent-governance.py`, `tests/test_validate_agent_registry.py`, `.agents/governance/model-selection.md`, `.codex/agents/*.toml`, `.codex/provider.md`, and this package
- **Forbidden Paths**: Claude projections and bindings; permission classes; credentials and private configuration beyond the project trust entry the user approved
- **Approval Required**: the request owner asked for the change. Push and merge stay with the request owner.
- **Static Validation**: `python3 scripts/validate-agent-governance.py --root .` and `python3 scripts/qa.py staged`
- **Live Validation**: one `--sandbox read-only` Codex session that spawns a read-only role per tier
- **Secret / Vault Handling**: no credential is read or recorded
- **Rollback Plan**: revert the rebinding commit; the validator and schema accept a registry with no override
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
- **First decision, superseded the same day**: `top` bound `gpt-6-astra` in
  `ae06a53b`. The request owner then asked for Astra to be kept to a minimum,
  with Astra for thinking and planning and a lower model for practical roles.
- **Decision**: both tiers bind `gpt-6-sol`, the documented replacement for
  `gpt-5.5`. Supervisor, which routes and plans, and architect, which owns
  structural decisions, declare `native_model_override.codex = gpt-6-astra`.
  Governance-steward, incident-responder, and security-auditor keep the `top`
  tier and its effort on Sol. Efforts are unchanged, and the catalog lists each
  one for its model. `gpt-6-luna` is not chosen, because no role here does
  extraction-style work.
- **Override rule**: the unit tests
  `test_a_model_departure_is_declared_rather_than_implied` and
  `test_a_model_override_replaces_only_its_own_provider` failed before
  `_bound_model` existed (`AttributeError`) and pass after it. The validator
  rejected a supervisor projection set back to `gpt-6-sol` with
  `AGENT-NATIVE-METADATA`, and it passed again after the value was restored.

### Spawn (2026-09-27)

`codex-cli 0.155.1` ran on the trusted project layer with
`codex exec [-m gpt-6-sol] --sandbox read-only --json -C <worktree> "<probe prompt>"`.
Each row below is the last `turn_context` that the client wrote to the spawned
thread's own rollout record, so it is the configuration the client applied, not
what the agent says about itself. Earlier `turn_context` entries in a child
rollout come from the parent history it inherits. Only the `model`, `effort`,
and `sandbox_policy` fields were read.

| Role | Registry binding now | Applied model | Applied effort | Parent thread |
| --- | --- | --- | --- | --- |
| architect | override `gpt-6-astra`, `top` `xhigh` | `gpt-6-astra` | `xhigh` | `01a0e06c-a762-7d01-b427-5488344e2e19` |
| supervisor | override `gpt-6-astra`, `top` `xhigh` | `gpt-6-astra` | `xhigh` | `01a0e064-ef8c-7032-b50e-067b67a63736`, run while the tier bound Astra; same resolved values |
| governance-steward | `top` `gpt-6-sol`, `xhigh` | `gpt-6-sol` | `xhigh` | `01a0e06c-a762-7d01-b427-5488344e2e19` |
| security-auditor | `top` `gpt-6-sol`, override `high` | `gpt-6-sol` | `high` | `01a0e068-0275-7b71-86f5-be5f5089a447` |
| code-reviewer | `worker` `gpt-6-sol`, `high` | `gpt-6-sol` | `high` | `01a0e062-3b35-7e02-83e1-4c5ef57902f7` |
| doc-writer | `worker` `gpt-6-sol`, override `medium` | `gpt-6-sol` | `medium` | `01a0e064-ef8c-7032-b50e-067b67a63736` |

Every sandbox applied as `read-only`: the parent sandbox caps a role declared
`workspace-write`, which is the expected ceiling. Two parent threads ran on the
client default, `gpt-6-astra` with `medium`. Later probes passed `-m gpt-6-sol`,
and their parents ran on `gpt-6-sol`. These records prove only that the
configuration applied. They say nothing about quality, cost, or usage limits.

### Validation

The governance validator and `python3 scripts/qa.py staged` passed on every
commit.

## Traceability

- Stable Task: `SPEC-0096-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Research above |
| [WORK-002](../plan.md#work-breakdown) | Done | Override rule and rebinding commit |
| [WORK-003](../plan.md#work-breakdown) | Done | [Spawn](#spawn-2026-09-27) |
