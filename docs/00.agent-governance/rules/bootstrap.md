# Agent Bootstrap Governance (March 2026)

Universal entry point for all agents in `hy-home.k8s`.

## Core Rules

- Use spec-driven execution anchored to `docs/01.prd/` and `docs/04.specs/`.
- Load governance just-in-time, not full-repository-first.
- Do not mutate authored documentation in `docs/01~99` unless explicitly instructed by a human.

## JIT Loading Sequence

1. Load `rules/bootstrap.md`.
2. Resolve persona via `rules/persona.md`.
3. Load one layer scope from `scopes/`.
4. Load provider notes from `providers/` when needed.
5. Load `memory/` entries only if relevant.

## Stage Taxonomy

| Stage | Path | Purpose |
| --- | --- | --- |
| 00 | `docs/00.agent-governance/` | Agent governance |
| 01 | `docs/01.prd/` | Product requirements |
| 02 | `docs/02.ard/` | Architecture references |
| 03 | `docs/03.adr/` | Architecture decisions |
| 04 | `docs/04.specs/` | Technical specs and contracts |
| 05 | `docs/05.plans/` | Implementation plans |
| 06 | `docs/06.tasks/` | Execution tracking |
| 07 | `docs/07.guides/` | Guides |
| 08 | `docs/08.operations/` | Operations policy |
| 09 | `docs/09.runbooks/` | Operational runbooks |
| 10 | `docs/10.incidents/` | Incident records |
| 11 | `docs/11.postmortems/` | Postmortems |
| 90 | `docs/90.references/` | References |
| 99 | `docs/99.templates/` | Templates |

## Definition of Done for Governance Tasks

- Policy changes are reflected in the correct file under `rules/`, `scopes/`, or `providers/`.
- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` remain thin gateways.
- English-only policy is preserved under `docs/00.agent-governance/`.
