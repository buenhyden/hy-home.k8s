# Contextual Memory

> Reusable, scoped lessons for future agent execution in `hy-home.k8s`.

## Overview

This folder stores agent work progress and durable technical lessons that reduce
repeated mistakes in agent work. Memory entries are supporting context only;
they do not override repository governance, scope rules, or direct user
instructions.

### Collection Readers

This README is primarily for:

- Agent authors
- Repository maintainers
- AI agents loading task context

## Scope

### In Scope

- Non-obvious technical findings likely to recur
- Work progress and handoff notes in `progress.md`
- Lessons connected to specs, runbooks, incidents, or postmortems
- Short operational notes that support future task intake

### Out of Scope

- New policy rules that belong in `../rules/`
- Runtime bridge configuration that belongs under `.claude/**` or `.codex/**`
- Product, architecture, execution, and operations SSoT under the current docs taxonomy

## Item Index

```text
memory/
├── progress.md  # Agent progress and reusable memory ledger
├── <topic>.md   # Optional standalone memory entry using memory.template.md
└── README.md    # This file
```

## Add and Find

1. Read `progress.md` before substantial repo-changing work to avoid repeating
   stale assumptions.
2. Append progress and reusable memory to `progress.md` during repo-changing
   work using `../../99.templates/templates/common/progress.template.md`.
3. Use `../../99.templates/templates/common/memory.template.md` for standalone memory entries if
   a future task creates separate memory files.
4. Link the entry to the affected spec, runbook, incident, or postmortem when
   useful.
5. Keep policy changes in `../rules/` instead of relying on memory notes.
6. When a standalone memory file is added or updated, append a matching
   progress entry to `progress.md` in the same change.

### Relative Link Rules

Links in this README are relative to `docs/00.agent-governance/memory/`.

- Same-folder memory entries use `./<topic>.md`.
- Governance rules use `../rules/<file>.md`.
- Templates use `../../99.templates/templates/**/<template>`.
- Repository-root files use `../../../<path>`.

## Related Documents

- [Agent Governance Hub](../README.md)
- [Memory Template](../../99.templates/templates/common/memory.template.md)
- [Progress Template](../../99.templates/templates/common/progress.template.md)
- [Documentation Protocol](../rules/documentation-protocol.md)

### Policy

- Record only non-obvious and repeat-preventing insights.
- Record progress and handoff notes for repo-changing agent work.
- Prefer short, factual entries over narrative summaries.
- Link each memory item to affected specs, runbooks, incidents, or postmortems.

### When to Write

- After resolving a complex defect.
- After a high-severity incident or rollback.
- After discovering a tooling or environment constraint likely to recur.

### Format

Use `docs/99.templates/templates/common/progress.template.md` for `progress.md` entries and keep
each item scoped to one workstream.

Standalone files under this folder must use
`docs/99.templates/templates/common/memory.template.md`. They are supporting context only and
must include a `Related Progress` section that points back to the matching
`progress.md` work entry.
