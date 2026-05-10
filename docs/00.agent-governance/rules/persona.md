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
| Product Manager | product | `docs/01.requirements/` |
| System Architect | architecture | `docs/02.architecture/requirements/`, `docs/02.architecture/decisions/` |
| Backend Engineer | backend | `docs/03.specs/` |
| Frontend Engineer | frontend | `docs/03.specs/` |
| Infra Engineer | infra | `docs/05.operations/policies/`, `docs/05.operations/runbooks/` |
| Operations Engineer | ops | `docs/05.operations/policies/`, `docs/05.operations/incidents/` |
| Security Engineer | security | `docs/03.specs/`, `docs/05.operations/incidents/` |
| QA Engineer | qa | `docs/04.execution/plans/`, `docs/04.execution/tasks/` |
| Technical Writer | docs | `docs/05.operations/guides/`, `docs/90.references/` |
| Governance Steward | meta | `docs/00.agent-governance/` |

## Stage Mapping

Use [stage-authoring-matrix.md](stage-authoring-matrix.md) for canonical taxonomy authoring timing, inputs, outputs, templates, and completion criteria.
