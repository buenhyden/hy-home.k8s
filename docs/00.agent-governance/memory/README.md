# Contextual Memory

> Reusable, scoped lessons for future agent execution in `hy-home.k8s`.

## Overview

This folder stores durable technical lessons that reduce repeated mistakes in
agent work. Memory entries are supporting context only; they do not override
repository governance, scope rules, or direct user instructions.

## Audience

This README is primarily for:

- Agent authors
- Repository maintainers
- AI agents loading task context

## Scope

### In Scope

- Non-obvious technical findings likely to recur
- Lessons connected to specs, runbooks, incidents, or postmortems
- Short operational notes that support future task intake

### Out of Scope

- New policy rules that belong in `../rules/`
- Runtime bridge configuration that belongs under `.claude/**` or `.codex/**`
- Product, architecture, and implementation SSoT under `docs/01-10`

## Structure

```text
memory/
├── progress.md  # Historical/current-source context for agent execution
└── README.md    # This file
```

## How to Work in This Area

1. Confirm the lesson is repeat-preventing and not merely a session summary.
2. Use `../../99.templates/memory.template.md` for new memory entries.
3. Link the entry to the affected spec, runbook, incident, or postmortem.
4. Keep policy changes in `../rules/` instead of relying on memory notes.

## Related References

- [Agent Governance Hub](../README.md)
- [Memory Template](../../99.templates/memory.template.md)
- [Documentation Protocol](../rules/documentation-protocol.md)

## Policy

- Record only non-obvious and repeat-preventing insights.
- Prefer short, factual entries over narrative summaries.
- Link each memory item to affected specs, runbooks, incidents, or postmortems.

## When to Write

- After resolving a complex defect.
- After a high-severity incident or rollback.
- After discovering a tooling or environment constraint likely to recur.

## Format

Use `docs/99.templates/memory.template.md` and keep each item scoped to one problem pattern.
