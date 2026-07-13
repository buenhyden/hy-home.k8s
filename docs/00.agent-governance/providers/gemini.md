---
title: 'Reference: Gemini Provider Notes'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Gemini Provider Notes

## Overview

Gemini-specific guidance for `hy-home.k8s`.

## Authority Boundary

### File Name Compatibility

- Default context file is `GEMINI.md`.
- In this repository, keep `AGENTS.md` out of the Gemini loading path unless a
  future approved adapter change updates Stage 00; `AGENTS.md` is the Codex/GPT
  gateway.
- Prefer project-local settings under `.gemini/settings.json`.

## Governance Context

### Official Source Basis

Checked on 2026-07-06:

- Gemini CLI commands and hierarchical memory: <https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md>

### Loading Model

- Keep root `GEMINI.md` thin; it imports `@docs/00.agent-governance/rules/bootstrap.md` (shared governance), `@docs/00.agent-governance/providers/gemini.md`, `@.agents/GEMINI.md`, and `@RTK.md`. It must not import `@AGENTS.md`, which is the GPT/Codex provider shim.
- Root `GEMINI.md` must load the existing hierarchy; it must not copy RTK, graphify, catalog, or governance policy blocks inline.
- Use `.agents/GEMINI.md` as the local runtime baseline; resolve the agent roster and model tier mapping from `docs/00.agent-governance/harness-catalog.md`.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; avoid policy duplication.
- Keep Gemini-specific runtime wiring under the existing gateway hierarchy; do not create a parallel `.github/**` instruction layer for this repository.

### Antigravity Harness Structure (`.agents/`)

The `.agents/` directory is the tracked Antigravity/Gemini adapter baseline for
this repository and the provider-neutral owner for shared skills, workflows,
and output styles.

- **Rules (`.agents/rules/`)**: Contains Gemini-specific workflow and behavior rules (e.g., `workspace-rules.md`).
- **Workflows (`.agents/workflows/`)**: Defines orchestrated workflows (e.g., `qa-cicd-workflow.md` for pre/post-edit validation).
- **Skills (`.agents/skills/`)**: Houses Gemini skill definitions that respect the model tiers defined in `model-policy.md`.
- **Hooks (`.agents/hooks.json`)**: Configures event wiring for PreToolUse/PostToolUse-style behavior where the runtime honors it. It invokes shared `docs/00.agent-governance/hooks/*.sh` scripts for Template-First routing and QA/CI/static validation, but it is not a Claude-style permission gate.
- **Agents (`.agents/agents/*.md`)**: Provider-native Gemini role adapters with
  `name`, `description`, and `model` frontmatter. They preserve role parity
  with Claude and Codex adapters without requiring Claude-style `tools:`
  frontmatter.

### Context Strategy

- Gemini CLI supports hierarchical context loading (global, ancestors, subdirectories).
- Gemini CLI command support includes an agents command/registry surface where
  available; otherwise use the project-local adapter workflow defined by
  Stage 00.
- Prefer modular imports for large context sets.
- Keep instructions concise and non-duplicative across hierarchy.
- Avoid introducing provider-specific guidance outside the existing `GEMINI.md` + `.agents/**` + `docs/00.agent-governance/**` hierarchy.

## Current Contract

### Model Policy (Gemini)

- Refer to `docs/00.agent-governance/model-policy.md` for canonical tiers.
- **Planning / Supervisor**: `Gemini 3.1 Pro` must be used for architecture, planning, and governance review.
- **Worker / Subagent**: `Gemini 3.5 Flash` must be used for routine file edits, summaries, and repetitive validation.

### Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- Keep user-facing responses in Korean.
- Keep governance and technical control docs in English.
- Use `docs/00.agent-governance/harness-catalog.md` as the canonical runtime roster.

## Validation and Refresh

## Related Documents
