---
title: "Reference: Subagent Protocol"
type: reference
status: draft
owner: "platform"
updated: 2026-05-24
---

# Reference: Subagent Protocol

## Overview

This document defines how local subagents are dispatched, constrained, and
coordinated in `hy-home.k8s`.

## Purpose

- Define the runtime contract for delegated agent execution.
- Keep orchestration behavior aligned with the local runtime catalog.
- Prevent policy duplication across gateway, provider, and agent files.

## Scope

- Covers dispatch rules, file requirements, model hierarchy, and coordination.
- Does not replace scope policy, provider notes, or runtime bridge files.

## Dispatch Rules

- Dispatch subagents via the **Task tool only**. Never embed role definitions inline in prompts.
- Each delegated agent must read its `.claude/agents/<name>.md` file before starting work.
- Codex delegated agents must use the corresponding `.codex/agents/<name>.toml` mirror with the same scope and guardrails.
- Each agent file must `@import` one or more matching scope files from `scopes/`.
- `supervisor.md` is the only supervising agent and owns routing and escalation decisions.

## Agent File Requirement

Every delegated agent must have a corresponding file in `.claude/agents/`. Each file must contain:

1. Frontmatter with `name`, `description`, and `model`.
2. One or more `@import` scope references.
3. A thin runtime contract: Role, When to use, Inputs, Outputs, Guardrails, Handoff / Escalation, Postflight.
4. No embedded policy text that belongs in `rules/`, `scopes/`, or `providers/`.

Every `.claude/agents/<name>.md` file must have a `.codex/agents/<name>.toml`
mirror for Codex execution. Mirrors must preserve the same role, scope imports,
guardrails, and postflight requirements.

The mirror relationship is validated by `scripts/validate-repo-quality-gates.sh`.
Runtime files must keep matching file stems, matching scope imports, Runtime
Bootstrap text, Guardrails, Handoff / Escalation, and Postflight requirements so
delegated work follows the same contract in Claude and Codex.

## Model Hierarchy

- `supervisor.md` uses `opus`.
- All worker agents use `sonnet`.
- Model allocation is canonical in `docs/00.agent-governance/harness-catalog.md`.

## Execution Boundaries

- Subagents may **read** any file in the repository.
- Subagents may **write** only within their declared File Ownership paths (see scope file).
- Subagents must **never** run `kubectl apply` or any destructive cluster command.
- Subagents must complete the postflight checklist before returning results.

## Coordination

- Use the Task tool for work assignment and status tracking.
- Route all multi-agent decisions through `supervisor.md`.
- Keep handoff artifacts in repository-approved locations only; do not create ad-hoc runtime folders unless a human requests them.
- Scratch workspaces such as `_workspace/` are allowed only when a checked-in
  skill explicitly defines them as temporary analysis space. Durable outputs
  from scratch work must be moved into the canonical docs taxonomy, such as
  `docs/04.execution/` for task evidence or `docs/05.operations/incidents/`
  for incident records.

## Catalog Reference

See `AGENTS.md` for the gateway routing pointer and
`docs/00.agent-governance/harness-catalog.md` for the canonical local runtime
catalog, including Codex mirrors.

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Local Harness Catalog](./harness-catalog.md)
- [Claude Provider Notes](./providers/claude.md)
