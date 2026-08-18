---
title: 'Reference: Model Selection Policy'
type: governance/reference
status: active
owner: platform
updated: 2026-07-30
---

# Model Selection Policy

## Overview

This document defines the canonical model selection policy for agents running in `hy-home.k8s`, enforcing a standardized tier mapping across Gemini (Antigravity), Claude, and Codex environments.

### Principles

- **Planning & Supervisor (`top`)**: Use the strongest permitted capability tier for supervisor orchestration, deep context synthesis, architecture design, and complex multi-agent routing.
- **Worker & Subagent (`worker`)**: Use the bounded worker tier for routine tasks, validation, focused file edits, and repetitive tasks.
- **Escalation**: A worker task may be routed to a top-tier model for high-risk governance, security, or cluster-affecting review, but that does not reclassify the worker agent itself as a top-tier agent.
- **Reasoning effort**: `medium`, `high`, and `xhigh` express increasing
  repository routing intent. They are not a universal provider enum or proof
  that a runtime accepts or applies the requested value.

## Authority Boundary

This file owns the shared `top` / `worker` tier vocabulary, the
`medium` / `high` / `xhigh` reasoning-intent vocabulary, and escalation policy.
[`contracts/agent-model-fitness.json`](contracts/agent-model-fitness.json) owns
each role's capability-tier membership and each role/provider tuple's
incumbent, configured and observed values, candidate, reasoning state, mapping
rationale, fallback, and decisions.
[`contracts/harness-contract.json`](contracts/harness-contract.json) owns the
adapter inventory, permission classes, and role behavior; it references each
role's fitness-owned capability tier and does not restate a tier literal.
[`contracts/provider-runtime-evidence.json`](contracts/provider-runtime-evidence.json)
owns provider source cutoff/currentness and runtime evidence. Provider-native
availability, entitlement, and enforcement remain outside repository-static
authority. A model change requires platform-owner authorization and the
evidence-backed promotion gates recorded by the model-fitness contract before
an adapter changes.

## Governance Context

### Source Freshness

- Last checked: 2026-07-10 10:00 Asia/Seoul cutoff, refreshed on
  2026-07-28 by Spec 042.
- Provider capability references are reconciled with
  `contracts/provider-runtime-evidence.json`.
- AREA-004 repository-static fitness readiness is recorded in
  `contracts/agent-model-fitness.json` version `1.1.0`; source publication and
  repository observation remain separate from provider/runtime evidence.
- Do not treat local/Antigravity labels as Gemini CLI native model resolution
  or any configured adapter value as observed provider fitness.

## Current Contract

### Model Tiers (July 2026 Local Baseline)

| Provider / Environment               | Planning / Supervisor Tier | Worker / Subagent Tier | Reasoning / Effort Policy                                                                                                                                           |
| ------------------------------------ | -------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Local/Antigravity and Gemini CLI** | `top`                      | `worker`               | Local adapter labels are configured incumbents only. Gemini CLI candidates and non-configurable reasoning state resolve per tuple in the model-fitness contract.    |
| **Claude**                           | `top`                      | `worker`               | Exact incumbent/candidate aliases and reasoning support resolve per tuple; cutoff mapping readiness is not runtime fitness or promotion.                            |
| **Codex**                            | `top`                      | `worker`               | Current adapters declare `model_reasoning_effort`; exact configured/candidate values and support resolve per tuple and are not inferred from the shared vocabulary. |

The closed AREA-004 result covers exactly `12 roles / 4 providers / 48
tuples`. Repository-static mapping readiness is `PASS` for 21 tuples and
`DEFER` for 27. Observed fitness, threshold, promotion, canary, and runtime are
`DEFER` for all 48, so configured incumbents remain in place. This result is
mapping readiness only. AREA-003 repository-static evaluation readiness is
complete, while observed same-suite evaluation and final admission remain
`DEFER`.

The harness catalog remains the readable roster projection. Exact per-tuple
model and reasoning state comes from the model-fitness contract, and provider
source confidence and runtime/canary records come from the provider evidence
contract. Codex TOML role adapters must use lowercase model IDs and declare
`model_reasoning_effort` explicitly when current.

## Validation and Refresh

### Enforcement

- All `agent-design.md` specs must adhere to these tier definitions when assigning models to roles.
- Platform configurations (`GEMINI.md`, `CLAUDE.md`, `CODEX.md`) should inherit this policy instead of re-defining model specs locally.
- `.codex/agents/*.toml` must match the configured incumbent model and
  `model_reasoning_effort` recorded for that tuple in the model-fitness
  contract.
- A future promotion requires explicit authorization plus observed provider
  resolution, same-suite fitness, thresholds, independent adjudication, and
  canary evidence. Newer is not automatically better, supported, or
  cost-appropriate.

## Related Documents

- [Harness Catalog](harness-catalog.md)
- [Model Fitness Contract](contracts/agent-model-fitness.json)
- [Provider Runtime Evidence Contract](contracts/provider-runtime-evidence.json)
- [Codex Provider Notes](providers/codex.md)
- [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
