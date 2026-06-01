# AI Agent Governance Hub

> Central governance entry point for AI agents operating in `hy-home.k8s`.

## Overview

This directory is the policy SSoT for local agent execution in `hy-home.k8s`.
It keeps gateway files thin by hosting durable rules, execution checklists,
scope routing, provider notes, reusable memory, shared hook scripts, model
policy, and the canonical runtime catalog used by `.claude/**`, `.codex/**`,
and `.agents/**` provider adapters.

## Audience

This README is primarily for:

- Repository maintainers
- Agent authors
- Runtime operators
- AI agents loading governance context

## Scope

### In Scope

- Governance rules and execution checklists
- Scope-specific policy for agent work
- Provider-specific notes for supported engines
- Canonical runtime roster and subagent protocol
- Reusable operational memory entries

### Out of Scope

- Product, architecture, execution, and operations SSoT under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates`
- Runtime bridge content under `.claude/**`
- Human-facing project onboarding outside this governance area

## Structure

```text
docs/00.agent-governance/
├── rules/              # Global policy, checklists, and documentation protocol
├── scopes/             # Layer-specific execution rules
├── providers/          # Provider-specific notes for Claude, Gemini, and gateways
├── hooks/              # Shared lifecycle/edit hook scripts reused by providers
├── memory/             # Reusable lessons and operational findings
├── common-governance.md
├── harness-catalog.md  # Canonical runtime roster for local agents and skills
├── model-policy.md     # Cross-provider model tier and effort policy
├── subagent-protocol.md
└── README.md           # This file
```

## How to Work in This Area

1. Start from repository gateway files: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
2. Follow the JIT loading order in `rules/bootstrap.md` and `rules/preflight-checklist.md`.
3. Use `docs/99.templates/` when creating or restructuring governance documents.
4. Update `harness-catalog.md` and this README in the same change set when the runtime roster changes.

## Link Basis

Links in this README are relative to `docs/00.agent-governance/`.

- Governance rules use `rules/<file>.md`.
- Scope and provider notes use `scopes/<file>.md` and `providers/<file>.md`.
- Repository-root runtime files use `../../<path>`.
- Template links use `../99.templates/<template>.md`.

## Governance Entry Points

- [Common Governance & Mappings](common-governance.md)
- [Model Policy](model-policy.md)
- [Preflight Checklist](rules/preflight-checklist.md)
- [Postflight Checklist](rules/postflight-checklist.md)
- [Document Stage Routing Rules](rules/document-stage-routing.md)
- [Stage Authoring Matrix](rules/stage-authoring-matrix.md)
- [Stage Checklists](rules/stage-checklists.md)
- [Local Harness Catalog](harness-catalog.md)
- [Subagent Protocol](subagent-protocol.md)
- [Codex Provider Notes](providers/codex.md)

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Codex Runtime Baseline](../../.codex/CODEX.md)
- [Claude Provider Notes](providers/claude.md)
- [Codex Provider Notes](providers/codex.md)
- [Gemini Provider Notes](providers/gemini.md)

## Related Folders

- `rules/`: global policy, checklists, and documentation protocol
- `scopes/`: layer-specific execution rules
- `providers/`: provider-specific notes
- `hooks/`: shared lifecycle/edit hook scripts invoked by provider wiring
- `memory/`: agent progress ledger and reusable operational lessons

## Examples

- Add a new execution rule under `rules/`.
- Add a provider note under `providers/`.
- Add work progress and reusable memory under `memory/progress.md` using `docs/99.templates/progress.template.md`.
