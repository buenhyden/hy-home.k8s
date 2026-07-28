---
title: 'Reference: Model Selection Policy'
type: governance/reference
status: active
owner: platform
updated: 2026-07-28
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

- Last checked: 2026-07-10 10:00 Asia/Seoul cutoff, refreshed on
  2026-07-28 by Spec 042.
- Provider capability references are reconciled with
  `contracts/provider-runtime-evidence.json`.
- Claude and local/Antigravity Gemini identifiers remain the repository-local
  baseline recorded in `harness-catalog.md`; verify provider identifiers against
  official sources before changing those concrete IDs. Do not treat the local
  Gemini labels as proof of Gemini CLI native model resolution.

## Current Contract

### Model Tiers (July 2026 Local Baseline)

| Provider / Environment | Planning / Supervisor Tier (High Difficulty) | Worker / Subagent Tier (Speed & Efficiency) | Reasoning / Effort Policy |
| --- | --- | --- | --- |
| **Gemini (Antigravity / Gemini CLI)** | Local high-tier label or Gemini-native pro candidate | Local worker label, Gemini-native flash candidate, or provider Auto | `.agents/**` is local adapter evidence only. Gemini CLI native IDs and reasoning settings remain candidate-only until `.gemini/**` parse/runtime evidence exists. |
| **Claude** | Opus 4.8 family candidate for high-risk planning/security | Sonnet/Haiku family candidate for bounded work | `/effort` and exact model aliases require Claude runtime/account resolution; cutoff evidence does not promote a local assignment by itself. |
| **Codex** | GPT-5.6 family candidate or installed-runtime demanding candidate | Installed-runtime balanced candidate | `model_reasoning_effort` is required for Codex role adapters but exact accepted values are model/runtime dependent and must be validated before promotion. |

The concrete provider identifiers consumed by local runtime files are recorded
in `docs/00.agent-governance/harness-catalog.md` and
`docs/00.agent-governance/contracts/provider-runtime-evidence.json`. The
catalog remains the readable roster table; the provider evidence contract owns
cutoff confidence, runtime verdicts, candidate-only status, and canary record
boundaries. Codex TOML role adapters must use lowercase model IDs and must
declare `model_reasoning_effort` explicitly when the adapter is current.

## Validation and Refresh

### Enforcement

- All `agent-design.md` specs must adhere to these tier definitions when assigning models to roles.
- Platform configurations (`GEMINI.md`, `CLAUDE.md`, `CODEX.md`) should inherit this policy instead of re-defining model specs locally.
- `.codex/agents/*.toml` must declare a model from this policy and an allowed `model_reasoning_effort` value.
- *Note:* The models listed above are candidate families or local labels unless
  a provider-specific runtime/canary/eval record promotes an exact ID. Newer is
  not automatically better, supported, or cost-appropriate.

## Related Documents

- [Harness Catalog](harness-catalog.md)
- [Provider Runtime Evidence Contract](contracts/provider-runtime-evidence.json)
- [Codex Provider Notes](providers/codex.md)
- [Codex Subagents](https://developers.openai.com/codex/subagents)
- [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
