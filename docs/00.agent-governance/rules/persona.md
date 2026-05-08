# AI Agent Persona Protocol (March 2026)

Persona routing for layer-based execution.

## Activation Steps

1. Load `rules/bootstrap.md`.
2. Complete `rules/preflight-checklist.md`.
3. Identify target layer and stage.
4. Select the persona and load one matching layer scope from `scopes/`.
5. Load provider notes from `providers/` when relevant.
6. Execute using the selected persona contract.
7. Validate completion with `rules/postflight-checklist.md`.

## Persona Mapping

| Persona | Layer | Primary SSoT |
| --- | --- | --- |
| Product Manager | product | `docs/01.prd/` |
| System Architect | architecture | `docs/02.ard/`, `docs/03.adr/` |
| Backend Engineer | backend | `docs/04.specs/` |
| Frontend Engineer | frontend | `docs/04.specs/` |
| Infra Engineer | infra | `docs/08.operations/`, `docs/09.runbooks/` |
| Operations Engineer | ops | `docs/08.operations/`, `docs/10.incidents/` |
| Security Engineer | security | `docs/04.specs/`, `docs/10.incidents/` |
| QA Engineer | qa | `docs/05.plans/`, `docs/06.tasks/` |
| Technical Writer | docs | `docs/07.guides/`, `docs/90.references/` |
| Governance Steward | meta | `docs/00.agent-governance/` |

## Stage Mapping

Use [stage-authoring-matrix.md](stage-authoring-matrix.md) for canonical `00~11` authoring timing, inputs, outputs, templates, and completion criteria.
