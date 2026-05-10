# AI Agent Governance Hub

> Central governance entry point for AI agents operating in `hy-home.k8s`.

## Overview

This directory is the policy SSoT for local agent execution in `hy-home.k8s`.
It keeps gateway files thin by hosting durable rules, execution checklists,
scope routing, provider notes, reusable memory, and the canonical runtime
catalog used by `.claude/**` and `.codex/**` mirrors.

## Purpose

This directory contains the durable governance policy for the local agent runtime.
It defines execution rules, scope-specific constraints, provider notes, reusable
operational memory, and the canonical runtime catalog that supports `.claude/**`.

## Allowed Content

- Governance rules and execution checklists
- Scope-specific policy for agent work
- Provider-specific notes for supported engines
- Canonical runtime roster and subagent protocol
- Reusable operational memory entries

## Disallowed Content

- Product, architecture, execution, and operations SSoT under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, and `docs/05.operations`
- Human-facing project onboarding outside this governance area
- Runtime bridge files that belong under `.claude/**` or `.codex/**`

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
├── memory/             # Reusable lessons and operational findings
├── harness-catalog.md  # Canonical runtime roster for local agents and skills
├── subagent-protocol.md
└── README.md           # This file
```

## How to Work in This Area

1. Start from repository gateway files: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
2. Follow the JIT loading order in `rules/bootstrap.md` and `rules/preflight-checklist.md`.
3. Use `docs/99.templates/` when creating or restructuring governance documents.
4. Update `harness-catalog.md` and this README in the same change set when the runtime roster changes.

## Governance Entry Points

- [Preflight Checklist](rules/preflight-checklist.md)
- [Postflight Checklist](rules/postflight-checklist.md)
- [Document Stage Routing Rules](rules/document-stage-routing.md)
- [Stage Authoring Matrix](rules/stage-authoring-matrix.md)
- [Stage Checklists](rules/stage-checklists.md)
- [Local Harness Catalog](harness-catalog.md)
- [Subagent Protocol](subagent-protocol.md)

## Related References

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Claude Provider Notes](providers/claude.md)
- [Gemini Provider Notes](providers/gemini.md)

## Related Folders

- `rules/`: global policy, checklists, and documentation protocol
- `scopes/`: layer-specific execution rules
- `providers/`: provider-specific notes
- `memory/`: reusable operational lessons

## Examples

- Add a new execution rule under `rules/`.
- Add a provider note under `providers/`.
- Add a reusable governance lesson under `memory/` using `docs/99.templates/memory.template.md`.
