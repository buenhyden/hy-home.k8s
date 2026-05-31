# Model Selection Policy

This document defines the canonical model selection policy for agents running in `hy-home.k8s`, enforcing a standardized tier mapping across Gemini (Antigravity), Claude, and Codex environments.

## Principles

- **Planning & Supervisor**: Use the most capable reasoning models for tasks requiring deep context, architecture design, and complex multi-agent orchestration.
- **Worker & Subagent**: Use fast, cost-efficient models for routine tasks, validation, focused file edits, and repetitive tasks.

## Model Tiers (May 2026 Baseline)

| Provider / Environment | Planning / Supervisor Tier (High Difficulty) | Worker / Subagent Tier (Speed & Efficiency) | Reasoning / Effort Policy |
| --- | --- | --- | --- |
| **Gemini (Antigravity)** | `Gemini 3.1 Pro` | `Gemini 3.5 Flash` | Use the provider-native high/medium tier labels recorded in `harness-catalog.md`. |
| **Claude** | `opus 4.8` | `sonnet 4.6` / `haiku 4.5` | Use the provider-native model tier controls recorded in agent frontmatter. |
| **Codex** | `gpt-5.5` | `gpt-5.3-codex` | `gpt-5.5`: `none`, `low`, `medium`, `high`, `xhigh`; `gpt-5.3-codex`: `low`, `medium`, `high`, `xhigh`. |

The concrete provider identifiers consumed by local runtime files are recorded in
the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.
Codex TOML mirrors must use lowercase model IDs and must declare
`model_reasoning_effort` explicitly.

## Enforcement

- All `agent-design.md` specs must adhere to these tier definitions when assigning models to roles.
- Platform configurations (`GEMINI.md`, `CLAUDE.md`, `CODEX.md`) should inherit this policy instead of re-defining model specs locally.
- `.codex/agents/*.toml` must declare a model from this policy and an allowed `model_reasoning_effort` value.
- *Note:* The models listed above are the canonical supported versions for the May 2026 runtime. Older models are considered legacy and should not be used for new tasks.
