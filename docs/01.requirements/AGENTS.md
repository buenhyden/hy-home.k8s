# AGENTS.md

Agent instructions for `docs/01.requirements/`. The parent
[`docs/AGENTS.md`](../AGENTS.md) still applies; this file adds the rules of
the requirements stage.

## Scope

### Allowed Surface

Stage 01 holds Requirement Packages: the solution-independent problem, goals,
stakeholder needs, functional, non-functional and interface requirements,
constraints and acceptance criteria. Design belongs to Stage 02 and change
contracts to Stage 03.

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Write or revise a requirement | [architect](../../.agents/roles/architect.md) | `requirements-to-design`, `docs-stage-routing` | `.claude/agents/architect.md` | `.codex/agents/architect.toml` |
| Author the package text and traceability | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Keep the README index current | [wiki-curator](../../.agents/roles/wiki-curator.md) | `docs-stage-conformance`, `knowledge-map` | `.claude/agents/wiki-curator.md` | `.codex/agents/wiki-curator.toml` |

### Non-goals

Non-goals are stated at the end of the Purpose text under Allowed Surface: design belongs to Stage 02 and change contracts to Stage 03.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Profile `sdlc/requirement`; start from
   `docs/99.templates/templates/requirements/requirement-package.template.md`
   and name the file `####-<slug>.md`. Reuse an existing package for the same
   problem instead of creating a duplicate.
2. Issue stable IDs `REQ-####-FR-####`, `REQ-####-NFR-####` and
   `REQ-####-IF-####`. Never renumber or reuse an ID; downstream AD, ADR and
   Spec rows trace the full ID.
3. Valid states are `draft`, `in-review` and `approved`. Only `approved` is
   current requirement authority; do not start implementation from a draft.
4. This stage has no `superseded`, `retired` or `deprecated` state. A replaced
   or completed document is summarized in the `Archived Lineage` table under
   `## Traceability` of the owning current document and deleted in the same
   change; Git history recovers it.
5. Keep requirements implementation-independent. Do not copy manifests,
   commands or change-scoped execution contracts here.
6. Agent capability requirements state allowed and forbidden actions and the
   human-in-the-loop points, in English.
7. When a requirement changes, update the linked AD, ADR and Spec traceability
   and this stage's README index in the same change.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This file states no separate handoff rule.

## Verification

### Required Checks

Run the strict document checks listed in the parent `AGENTS.md`; the
lifecycle check enforces the state edges above.

### Evidence and Limits

This file states no separate evidence or limits rule.

## Safety

### Protected Actions

This file states no separate protected-action rule.

### Stop and Escalate

This file states no separate stop or escalation rule.
