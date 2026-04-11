# Subagent Protocol

Defines how subagents are dispatched and constrained in `hy-home.k8s`.

## Dispatch Rules

- Dispatch subagents via the **Task tool only**. Never embed role definitions inline in prompts.
- Each subagent must read its `.claude/agents/<name>.md` file before starting work.
- Each agent file `@import`s its matching scope from `scopes/<layer>.md`.

## Agent File Requirement

Every subagent must have a corresponding file in `.claude/agents/`. The file must contain:

1. Role description (what the agent does).
2. `@import scopes/<layer>.md` reference.
3. Input/output contract.
4. Constraints (GitOps-First, no plaintext secrets, kube-linter compliance).

## Execution Boundaries

- Subagents may **read** any file in the repository.
- Subagents may **write** only within their declared File Ownership paths (see scope file).
- Subagents must **never** run `kubectl apply` or any destructive cluster command.
- Subagents must complete the postflight checklist before returning results.

## Coordination

- Use Task tool for work assignment and status tracking.
- Use file-based handoff under `_workspace/` for intermediate artifacts.
- Naming convention: `{phase}_{agent}_{artifact}.{ext}`.

## Catalog Reference

See `AGENTS.md §3` for the current agent catalog and
`docs/00.agent-governance/harness-catalog.md` for local harness mapping.
