---
title: 'Reference: Model Selection Policy'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Model Selection Policy

## Overview

This document defines the canonical model selection policy for agents running in `hy-home.k8s`, enforcing a standardized tier mapping across Gemini (Antigravity), Claude, and Codex environments.

### Principles

- **Planning & Supervisor**: Use the most capable reasoning models for supervisor orchestration, deep context synthesis, architecture design, and complex multi-agent routing.
- **Worker & Subagent**: Use coding-optimized or cost-efficient models for routine tasks, validation, focused file edits, and repetitive tasks.
- **Escalation**: A worker task may be routed to a top-tier model for high-risk governance, security, or cluster-affecting review, but that does not reclassify the worker agent itself as a top-tier agent.

## Authority Boundary

This file owns the shared tier vocabulary and reasoning-effort policy. The
canonical provider identifiers and adapter inventory remain owned by
[`harness-catalog.md`](harness-catalog.md), while provider-native availability,
entitlements, and runtime enforcement remain outside repository-static
authority. A model change that alters cost, capability, or provider support
must be reviewed by the platform owner before the catalog and adapters change.

## Governance Context

### Source Freshness

- Last checked: 2026-07-06
- Provider capability references were reconciled with the official source basis
  recorded in `harness-catalog.md`.
- Claude and Gemini identifiers remain the repository-local provider baseline
  recorded in `harness-catalog.md`; verify against provider-native docs before
  changing those concrete IDs.

## Current Contract

### Model Tiers (July 2026 Local Baseline)

| Provider / Environment | Planning / Supervisor Tier (High Difficulty) | Worker / Subagent Tier (Speed & Efficiency) | Reasoning / Effort Policy |
| --- | --- | --- | --- |
| **Gemini (Antigravity)** | `Gemini 3.1 Pro` | `Gemini 3.5 Flash` | Use the provider-native high/medium tier labels recorded in `harness-catalog.md`. |
| **Claude** | `opus 4.8` | `sonnet 4.6` / `haiku 4.5` | Use the provider-native model tier controls recorded in agent frontmatter. |
| **Codex** | `gpt-5.5` | `gpt-5.3-codex` | `gpt-5.5`: `none`, `low`, `medium`, `high`, `xhigh`; `gpt-5.3-codex`: `low`, `medium`, `high`, `xhigh`. |

The concrete provider identifiers consumed by local runtime files are recorded in
the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.
That catalog is the canonical roster table; this file owns the tier vocabulary
and reasoning/effort policy. Codex TOML role adapters must use lowercase model
IDs and must declare `model_reasoning_effort` explicitly.

## Validation and Refresh

### Enforcement

- All `agent-design.md` specs must adhere to these tier definitions when assigning models to roles.
- Platform configurations (`GEMINI.md`, `CLAUDE.md`, `CODEX.md`) should inherit this policy instead of re-defining model specs locally.
- `.codex/agents/*.toml` must declare a model from this policy and an allowed `model_reasoning_effort` value.
- *Note:* The models listed above are the canonical supported versions for the
  July 2026 local runtime. Older local baseline models are considered legacy and
  should not be used for new tasks unless a provider-specific migration plan
  records the exception.

## Related Documents

- [Harness Catalog](harness-catalog.md)
- [Codex Provider Notes](providers/codex.md)
- [Codex Subagents](https://developers.openai.com/codex/subagents)
- [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
