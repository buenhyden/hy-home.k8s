# AI Agent Persona Protocol (March 2026)

Persona routing for layer-based execution.

## Activation Steps

1. Identify target layer and stage.
2. Load `rules/bootstrap.md`.
3. Load one layer scope from `scopes/`.
4. Execute using the selected persona contract.

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
