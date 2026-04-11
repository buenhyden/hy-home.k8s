---
title: "Reference: Subagent Protocol"
type: reference
status: draft
owner: "platform"
updated: 2026-04-11
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
- Each agent file must `@import` one or more matching scope files from `scopes/`.
- `supervisor.md` is the only supervising agent and owns routing and escalation decisions.

## Agent File Requirement

Every delegated agent must have a corresponding file in `.claude/agents/`. Each file must contain:

1. Frontmatter with `name`, `description`, and `model`.
2. One or more `@import` scope references.
3. A thin runtime contract: Role, When to use, Inputs, Outputs, Guardrails, Handoff / Escalation, Postflight.
4. No embedded policy text that belongs in `rules/`, `scopes/`, or `providers/`.

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

## Catalog Reference

See `AGENTS.md §3` for the gateway roster and
`docs/00.agent-governance/harness-catalog.md` for the canonical local runtime catalog.

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Local Harness Catalog](./harness-catalog.md)
- [Claude Provider Notes](./providers/claude.md)
