---
title: 'Reference: Subagent Protocol'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
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
frontmatter. Codex `.codex/agents/*.toml` and local/Antigravity
`.agents/agents/*.md` adapters preserve the same governance boundary without
requiring identical metadata keys; the latter is not Gemini CLI native tool
scoping.

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
catalog, including native Claude/Codex adapters and local/Antigravity role
adapters.

## Current Contract

### Dispatch Rules

- Dispatch subagents through the current runtime's verified delegated-agent mechanism. Claude uses the Task tool or explicit Agent invocation, and Codex uses explicit subagent orchestration when requested by the user. A compatible local/Antigravity runtime may use the `.agents/**` adapter workflow; Gemini CLI native delegation remains `DEFER` because `.gemini/agents/**` and `.gemini/settings.json` are absent.
- Never embed full role definitions inline when a provider-local agent file exists.
- Each delegated agent must read its provider-specific local agent file (e.g., `.claude/agents/<name>.md`, `.agents/agents/<name>.md`, `.codex/agents/<name>.toml`) before starting work.
- Each agent file must `@import` one or more matching scope files from `scopes/`.
- `supervisor.md` is the only supervising agent and owns routing and escalation decisions.

### Agent File Requirement

Every local roster role must have corresponding parity files in
`.agents/agents/`, `.claude/agents/`, and `.codex/agents/`. This is a static
local adapter contract, not proof that all three runtimes discover the files.

Claude Markdown agent files in `.claude/agents/*.md` must contain frontmatter
with `name`, `description`, `model`, and a least-privilege `tools` set (see Tool
Scoping).

Local/Antigravity Markdown agent files in `.agents/agents/*.md` must contain frontmatter
with `name`, `description`, and `model`, and must preserve the same role, scope
imports, guardrails, handoff, and postflight contract as the Claude source.
These local adapter files do not require Claude-style `tools:` frontmatter.
Gemini CLI native agents are reserved for `.gemini/agents/**`; adding them or
`.gemini/settings.json` requires a separate approved PRD/ARD/Spec/Plan/Task, or
at minimum an approved Spec/Plan/Task.

Codex agent files in `.codex/agents/*.toml` must declare `name`,
`description`, `developer_instructions`, `model`, and `model_reasoning_effort`.

All three tracked role surfaces must preserve local adapter parity: matching file
stems, scope imports, Runtime Bootstrap text, Guardrails, Handoff / Escalation,
and Postflight requirements. Surface metadata keys differ. This parity
relationship is validated by `scripts/validate-repo-quality-gates.sh` and does
not establish Gemini CLI runtime parity.

### Coordination

- Use only a verified runtime delegated-agent mechanism for work assignment and
  status tracking; local adapter presence alone is insufficient.
- Route all multi-agent decisions through `supervisor.md`.
- Keep handoff artifacts in repository-approved locations only; do not create ad-hoc runtime folders unless a human requests them.
- Scratch workspaces such as `_workspace/` are allowed only under the checked-in
  contract at [`_workspace/README.md`](../../_workspace/README.md). Scratch
  files must remain ignored by default, and durable outputs from scratch work
  must be promoted into the canonical docs taxonomy, such as
  `docs/04.execution/` for task evidence, `docs/90.references/audits/` for
  durable audits, Stage 00 governance, or Stage 99 support contracts.

### Delegated Handoff Evidence

- The delegating agent gives each worker a bounded scope, changed-path or
  ownership boundary, acceptance IDs, required validation lanes, and a next
  owner before work begins.
- The returning worker reports the canonical fields from
  [`rules/quality-standards.md`](rules/quality-standards.md): scope, changed
  paths, acceptance IDs, commands, tool/version, per-lane result, limitations,
  reviewer, rollback, residual risk, and next owner.
- `affected`, `staged`, `all-files`, `message/manual`, `ci`, and `remote/live`
  results remain distinct. A delegated agent must not promote another agent's
  repo-static result into provider-runtime, remote, or live evidence.
- Native Claude/Codex adapters and local/Antigravity adapter files establish a
  reviewable repository contract; their presence does not prove that a runtime
  discovered, loaded, or enforced an adapter in the delegated session.

## Validation and Refresh

Run both self-tests and repository checks for role semantics and roster
currentness, followed by the aggregate repository gate:

```bash
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
bash scripts/validate-repo-quality-gates.sh .
```

Refresh this protocol whenever a shared role, provider adapter schema, tool
boundary, capability tier, delegated handoff field, or runtime dispatch
mechanism changes. Native discovery and delegation remain separate
provider-runtime evidence.

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [CLAUDE.md](../../CLAUDE.md)
- [GEMINI.md](../../GEMINI.md)
- [Claude Runtime Baseline](../../.claude/CLAUDE.md)
- [Local Harness Catalog](./harness-catalog.md)
- [Quality Standards and Evidence Contract](./rules/quality-standards.md)
