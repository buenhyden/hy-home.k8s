---
title: 'Reference: Subagent Protocol'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Reference: Subagent Protocol

## Overview

This document defines how local subagents are dispatched, constrained, and
coordinated in `hy-home.k8s`.

### Purpose

- Define the runtime contract for delegated agent execution.
- Keep orchestration behavior aligned with the local runtime catalog.
- Prevent policy duplication across gateway, provider, and agent files.

## Authority Boundary

### Scope

- Covers dispatch rules, file requirements, model hierarchy, and coordination.
- Does not replace scope policy, provider notes, or runtime bridge files.

### Tool Scoping

Each agent declares a least-privilege tool set matched to its responsibility. The
canonical mapping below is implemented natively in `.claude/agents/*.md` `tools:`
frontmatter; Gemini (`.agents/agents/*.md`) and Codex (`.codex/agents/*.toml`)
honor the same boundary within their native capabilities and governance
guardrails without requiring identical metadata keys.

- `supervisor`: full toolset (orchestration and delegation).
- Read-only review agents (`code-reviewer`, `gitops-reviewer`, `security-auditor`, `incident-responder`): `Read`, `Grep`, `Glob`, `Bash` (read-only command policy still applies).
- Authoring agents (`k8s-implementer`, `doc-writer`, `wiki-curator`): `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`.
- Tool scoping never overrides the destructive-command deny list or the no-direct-cluster-mutation boundary.
- Additional Claude agent frontmatter fields (`permissionMode`, `memory`, `effort`) are deferred until verified against the current Claude Code agent schema; add them only when confirmed supported, otherwise keep the boundary in this contract.

### Execution Boundaries

- Subagents may **read** any file in the repository.
- Subagents may **write** only within their declared File Ownership paths (see scope file).
- Subagents must **never** run `kubectl apply` or any destructive cluster command.
- Subagents must complete the postflight checklist before returning results.

## Governance Context

### Model Hierarchy

- `supervisor.md` uses the `top` model tier; all worker agents use the `worker` tier.
- Per-provider concrete model identifiers are canonical in the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.

### Catalog Reference

Start from the appropriate root provider shim (`AGENTS.md`, `CLAUDE.md`, or
`GEMINI.md`) for gateway routing and use
`docs/00.agent-governance/harness-catalog.md` for the canonical local runtime
catalog, including provider-native role adapters.

## Current Contract

### Dispatch Rules

- Dispatch subagents through the current runtime's provider-native delegated-agent mechanism. Claude uses the Task tool or explicit Agent invocation, Codex uses explicit subagent orchestration when requested by the user, and Gemini uses the available agent registry or project-local adapter workflow where supported.
- Never embed full role definitions inline when a provider-local agent file exists.
- Each delegated agent must read its provider-specific local agent file (e.g., `.claude/agents/<name>.md`, `.agents/agents/<name>.md`, `.codex/agents/<name>.toml`) before starting work.
- Each agent file must `@import` one or more matching scope files from `scopes/`.
- `supervisor.md` is the only supervising agent and owns routing and escalation decisions.

### Agent File Requirement

Every delegated agent must have corresponding provider files in `.agents/agents/`,
`.claude/agents/`, and `.codex/agents/`.

Claude Markdown agent files in `.claude/agents/*.md` must contain frontmatter
with `name`, `description`, `model`, and a least-privilege `tools` set (see Tool
Scoping).

Gemini Markdown agent files in `.agents/agents/*.md` must contain frontmatter
with `name`, `description`, and `model`, and must preserve the same role, scope
imports, guardrails, handoff, and postflight contract as the Claude source.
Gemini files do not require Claude-style `tools:` frontmatter unless a future
approved Gemini adapter change adds a verified native tool-scoping field.

Codex agent files in `.codex/agents/*.toml` must declare `name`,
`description`, `developer_instructions`, `model`, and `model_reasoning_effort`.

All provider-native role adapters must preserve role parity: matching file
stems, scope imports, Runtime Bootstrap text, Guardrails, Handoff / Escalation,
and Postflight requirements. Native metadata keys differ by provider. This
parity relationship is validated by `scripts/validate-repo-quality-gates.sh`.

### Coordination

- Use the provider-native delegated-agent mechanism for work assignment and
  status tracking.
- Route all multi-agent decisions through `supervisor.md`.
- Keep handoff artifacts in repository-approved locations only; do not create ad-hoc runtime folders unless a human requests them.
- Scratch workspaces such as `_workspace/` are allowed only under the checked-in
  contract at [`_workspace/README.md`](../../_workspace/README.md). Scratch
  files must remain ignored by default, and durable outputs from scratch work
  must be promoted into the canonical docs taxonomy, such as
  `docs/04.execution/` for task evidence, `docs/90.references/audits/` for
  durable audits, Stage 00 governance, or Stage 99 support contracts.

## Validation and Refresh

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [CLAUDE.md](../../CLAUDE.md)
- [GEMINI.md](../../GEMINI.md)
- [Claude Runtime Baseline](../../.claude/CLAUDE.md)
- [Local Harness Catalog](./harness-catalog.md)
