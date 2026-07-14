---
title: 'Reference: Gemini Provider Notes'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
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
- Reserve Gemini CLI project-local settings for `.gemini/settings.json`; that
  native surface is not tracked in the current repository.

## Governance Context

### Official Source Basis

Checked on 2026-07-06:

- Gemini CLI commands and hierarchical memory: <https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md>

### Loading Model

- Keep root `GEMINI.md` thin; it imports `@docs/00.agent-governance/rules/bootstrap.md` (shared governance), `@docs/00.agent-governance/providers/gemini.md`, `@.agents/GEMINI.md`, and `@RTK.md`. It must not import `@AGENTS.md`, which is the GPT/Codex provider shim.
- Root `GEMINI.md` must load the existing hierarchy; it must not copy RTK, graphify, catalog, or governance policy blocks inline.
- Use `.agents/GEMINI.md` as the local/Antigravity adapter baseline; resolve the agent roster and model tier mapping from `docs/00.agent-governance/harness-catalog.md`.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; avoid policy duplication.
- Keep local/Antigravity adapter wiring under the existing gateway hierarchy; do not create a parallel `.github/**` instruction layer for this repository or infer Gemini CLI native wiring.

### Antigravity Harness Structure (`.agents/`)

The `.agents/` directory is the tracked local/Antigravity adapter baseline for
this repository and the provider-neutral owner for shared skills, workflows,
and output styles. It is not the Gemini CLI native configuration directory.

- **Rules (`.agents/rules/`)**: Contains local/Antigravity workflow and behavior rules (e.g., `workspace-rules.md`); these are not Gemini CLI native policy files.
- **Workflows (`.agents/workflows/`)**: Defines orchestrated workflows (e.g., `qa-cicd-workflow.md` for pre/post-edit validation).
- **Skills (`.agents/skills/`)**: Houses provider-neutral shared skill definitions for the tracked local adapters; Gemini CLI native discovery or consumption is not established.
- **Hooks (`.agents/hooks.json`)**: Declares local/Antigravity behavioral wiring where a compatible runtime honors it. It invokes shared `docs/00.agent-governance/hooks/*.sh` scripts for Template-First routing and QA/CI/static validation, but it is neither a Claude-style permission gate nor Gemini CLI native settings.
- **Agents (`.agents/agents/*.md`)**: Local/Antigravity role adapters with
  `name`, `description`, and `model` frontmatter. They preserve role parity
  with Claude and Codex adapters without requiring Claude-style `tools:`
  frontmatter.

### Context Strategy

- Gemini CLI supports hierarchical context loading (global, ancestors, subdirectories).
- The tracked local adapter workflow may be used only by a runtime that
  explicitly supports it. Do not infer Gemini CLI agent registration from
  `.agents/agents/**`.
- Prefer modular imports for large context sets.
- Keep instructions concise and non-duplicative across hierarchy.
- Avoid introducing provider-specific guidance outside the existing `GEMINI.md` + `.agents/**` + `docs/00.agent-governance/**` hierarchy.

## Current Contract

### Gemini CLI Native Surface

Gemini CLI native project agents and settings are reserved for
`.gemini/agents/**` and `.gemini/settings.json`; neither path exists in the
tracked current baseline. Native discovery, event delivery, policy loading,
and model resolution remain `DEFER`. Implementing Gemini CLI adoption requires
a separate approved PRD/ARD/Spec/Plan/Task change set, or at minimum an
approved Spec/Plan/Task when upstream intent is already established. That work
must provide schema and runtime canary evidence instead of relabeling
`.agents/**`.

### Model Policy (Gemini)

- Refer to `docs/00.agent-governance/model-policy.md` for canonical tiers.
- **Planning / Supervisor**: `Gemini 3.1 Pro` must be used for architecture, planning, and governance review.
- **Worker / Subagent**: `Gemini 3.5 Flash` must be used for routine file edits, summaries, and repetitive validation.

### Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- Keep user-facing responses in Korean.
- Keep governance and technical control docs in English.
- Use `docs/00.agent-governance/harness-catalog.md` as the canonical runtime roster.

### QA Evidence Resolution

- Resolve `affected`, `staged`, `all-files`, `message/manual`, `ci`, and
  `remote/live` semantics plus handoff fields from
  [`rules/quality-standards.md`](../rules/quality-standards.md).
- Tracked `.agents/agents/*.md` and `.agents/hooks.json` are repo-static
  local/Antigravity adapter configuration. They do not prove Gemini CLI native
  discovery, role use, event delivery, policy loading, model resolution,
  permission enforcement, or remote execution.
- Preserve local adapter model metadata and role semantics without presenting
  them as Gemini CLI native model selection or runtime wiring.

## Validation and Refresh

Run the shared role-semantic and roster checks plus the repository quality gate
after changing local/Antigravity agents, hooks, model metadata, or the root
shim:

```bash
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
bash scripts/validate-repo-quality-gates.sh .
```

Refresh the official source basis when Gemini CLI context or agent-registry
behavior changes. Tracked `.agents/**` files provide local adapter evidence
only; the absent `.gemini/**` native surfaces and all native discovery, event,
policy, and model behavior require a separately approved implementation and
runtime evidence.

## Related Documents

- [Bootstrap Governance](../rules/bootstrap.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Model Selection Policy](../model-policy.md)
- [Subagent Protocol](../subagent-protocol.md)
