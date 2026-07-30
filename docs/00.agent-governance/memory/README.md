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

Exactly four memory classes are managed. `progress.md` is the durable shared
progress view for `durable-long-term` memory, not a fifth memory class.

| Class | Authority | Refresh | Retention / expiry | Archive / GC | Promotion | Conflict | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `working-short-term` | Temporary context owned by the active task executor; non-authoritative | Re-observe the task and repository on resume | Discard at task terminal | Discard after reviewed terminal disposition | Reviewed, redacted evidence may move to `durable-long-term` | Observed repository state wins | Active executor records the next owner or discard disposition with evidence |
| `durable-long-term` | Canonical SDLC owner or shared progress ledger | Canonical-owner review | Retain under the canonical owner | Retain until that owner approves a replacement | No implicit onward promotion | Canonical document owner wins | Current canonical owner records the next canonical owner and evidence |
| `domain-scoped` | Canonical domain document owner | Domain-owner review | Archive when superseded or invalidated | Archive with original and replacement ownership and provenance | Reviewed cross-domain evidence may move to `durable-long-term` | Canonical domain owner wins | Domain owner records the archive or replacement owner with evidence |
| `provider-local-auxiliary` | Provider runtime or user-local store; advisory only | Repository re-observation before use | Garbage-collect under provider retention after repository re-observation | Provider-owned GC after reviewed re-observation | May enter `working-short-term` only after repository re-observation; never writes canonical memory directly | Observed repository state wins | Provider-local owner records the next owner or GC disposition without transferring authority |

Repository state and canonical SDLC owners win every conflict with temporary or
provider-local context. Promotion is review-gated: working context may be
promoted to durable memory, domain knowledge may be promoted when it becomes
cross-domain, and provider-local claims must first be re-observed from the
repository. Credentials, auth files, tokens, secrets, raw prompts, complete
provider transcripts, shell history, private diagnostics, environment dumps,
and user configuration are never memory payloads.

The executable Spec 043 lifecycle validators enforce these four classes,
atomic redacted synthetic checkpoint shape, repository-wins resume,
promotion/refresh/expiry/archive-GC/conflict controls, compaction, handoff,
and the five bounded reviewed feedback destinations. `.agent-work/checkpoint.json`
remains ignored and advisory; validators neither read nor write it. Repository
state and canonical owners win, provider-local memory remains auxiliary, and a
repo-static PASS does not prove provider discovery, hook/event delivery,
permissions, model resolution, authenticated execution, hosted CI, remote,
credential-bearing, live, or actual checkpoint execution.

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
