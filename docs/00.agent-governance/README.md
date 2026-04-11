# AI Agent Governance Hub

> Central governance entry point for AI agents operating in `hy-home.k8s`.

## Overview

This directory contains the durable governance policy for the local agent runtime.
It defines execution rules, scope-specific constraints, provider notes, reusable
operational memory, and the canonical runtime catalog that supports `.claude/**`.

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

- Product, architecture, and implementation SSoT under `docs/01~99`
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
- [Stage Authoring Matrix (00-11)](rules/stage-authoring-matrix.md)
- [Stage Checklists](rules/stage-checklists.md)
- [Local Harness Catalog](harness-catalog.md)
- [Subagent Protocol](subagent-protocol.md)

## Related References

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Claude Provider Notes](providers/claude.md)
- [Gemini Provider Notes](providers/gemini.md)
