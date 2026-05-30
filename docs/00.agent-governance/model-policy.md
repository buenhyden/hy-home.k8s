# Model Selection Policy

This document defines the canonical model selection policy for agents running in `hy-home.k8s`, enforcing a standardized mapping across Gemini (Antigravity), Claude, and Codex environments.

## Principles

- **Planning & Supervisor**: Use the most capable reasoning models for tasks requiring deep context, architecture design, and complex multi-agent orchestration.
- **Worker & Subagent**: Use fast, cost-efficient models for routine tasks, validation, focused file edits, and repetitive tasks.

## Model Tiers (May 2026 Baseline)

| Provider / Environment | Planning / Supervisor Tier (High Difficulty) | Worker / Subagent Tier (Speed & Efficiency) |
| --- | --- | --- |
| **Gemini (Antigravity)** | `Gemini 3.1 Pro` | `Gemini 3.5 Flash` |
| **Claude** | `Claude 3.5 Opus` (e.g. `opus 4.8`) | `Claude 3.5 Sonnet` / `Haiku` (e.g. `sonnet 4.6`) |
| **Codex** | `GPT-5.5` | `GPT-5.4-mini` |

## Enforcement

- All `agent-design.md` specs must adhere to these tier definitions when assigning models to roles.
- Platform configurations (`GEMINI.md`, `CLAUDE.md`, `CODEX.md`) should inherit this policy instead of re-defining model specs locally.
- *Note:* The models listed above are the canonical supported versions for the May 2026 runtime. Older models are considered legacy and should not be used for new tasks.
