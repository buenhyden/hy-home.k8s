# Contextual Memory

> Reusable, scoped lessons for future agent execution in `hy-home.k8s`.

## Overview

This folder stores agent work progress and durable technical lessons that reduce
repeated mistakes in agent work. Memory entries are supporting context only;
they do not override repository governance, scope rules, or direct user
instructions.

The machine-readable class and authority owner is
[`../contracts/harness-contract.json`](../contracts/harness-contract.json).
This README explains how its four memory classes are used; it does not create a
second memory taxonomy.

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

### Four Memory Classes

| Class | Use | Authority and Location |
| --- | --- | --- |
| `working-short-term` | Bounded context for one active task or session | Temporary and non-authoritative. The ignored `.agent-work/checkpoint.json` path is an advisory recovery carrier only. |
| `durable-long-term` | Reviewed repository facts, decisions, task status, reusable lessons, and handoff evidence | Canonical repository records, with `docs/00.agent-governance/memory/progress.md` as the durable shared progress ledger and the owning SDLC document as applicable. |
| `domain-scoped` | Knowledge whose meaning belongs to one product, architecture, operation, incident, or policy domain | The owning Spec, Runbook, Incident, Postmortem, or other canonical domain document, linked to related progress. It does not independently own task status. |
| `provider-local-auxiliary` | Provider- or user-local recall that may help rediscovery | Advisory only. It must not own repository facts, decisions, task status, or durable handoff evidence. |

Repository state and canonical SDLC owners win every conflict with temporary or
provider-local context. Promotion is review-gated: working context may be
promoted to durable memory, domain knowledge may be promoted when it becomes
cross-domain, and provider-local claims must first be re-observed from the
repository. Credentials, auth files, tokens, secrets, raw prompts, complete
provider transcripts, shell history, private diagnostics, environment dumps,
and user configuration are never memory payloads.

The contract declares these boundaries now. Spec 043
([`../../03.specs/043-agent-harness-loop-lifecycle/spec.md`](../../03.specs/043-agent-harness-loop-lifecycle/spec.md))
owns future executable promotion, refresh, expiry, archive/garbage-collection,
redaction, conflict, and resume controls. Until those controls are implemented
and validated, do not report them as executable runtime behavior.

## Item Index

```text
memory/
├── progress.md  # Canonical durable shared progress ledger
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
7. On resume, rediscover repository status and the owning SDLC record before
   using `.agent-work/checkpoint.json` or provider-local memory; the repository
   wins on conflict.

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
