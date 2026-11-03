# AGENTS.md

Agent instructions for `docs/90.references/` and its `audits/`, `data/` and
`research/` collections. The parent [`docs/AGENTS.md`](../AGENTS.md) still
applies.

## Purpose

Stage 90 holds evidence: external research, audits and data packs with their
observation dates, claims and coverage. It informs Stages 01 to 05 but is
never policy or current authority by itself.

## Responsibilities and Projections

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Collect and classify source evidence | [docs-researcher](../../.agents/roles/docs-researcher.md) | `docs-stage-routing`, `knowledge-map` | `.claude/agents/docs-researcher.md` | `.codex/agents/docs-researcher.toml` |
| Author pack members | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Keep collection and pack routers current | [wiki-curator](../../.agents/roles/wiki-curator.md) | `docs-stage-conformance`, `knowledge-map` | `.claude/agents/wiki-curator.md` | `.codex/agents/wiki-curator.toml` |

`docs-researcher` is read-only (`read-only-research`); a writing role records
its findings.

## Rules

1. Every collection keeps three levels: the collection `README.md`, a pack
   router `####-<slug>/README.md` with the `reference/<kind>-pack` profile,
   and members `####-<slug>/m####-<slug>.md` with `reference/audit`,
   `reference/research` or `reference/data`.
2. Record each claim with its source, observation date and verification
   state. Prefer official and primary sources, and keep past local
   observations apart from current external knowledge.
3. Do not rewrite a published member to follow a later rename or form; add a
   new member or a dated addendum instead.
4. A pack README lists exactly its members. Stage the pack README together
   with member changes: the registry check compares the staged and worktree
   pack sets.
5. Never present a Stage 90 claim as a requirement, decision or policy; link
   the Stage 01, 02 or 05 owner that adopts it.

## Checks

Run the strict document checks listed in the parent `AGENTS.md`;
`validate-document-contract-registry.py` checks pack topology.
