# Product Scope

Persona: Product Manager

## Source of Truth

- `docs/01.requirements/`
- `docs/04.execution/plans/`

## Responsibilities

- Keep intent, value, and acceptance criteria clear before implementation.
- Ensure implementation plans and tasks stay traceable to PRD intent.
- Flag gaps when downstream stages drift from product requirements.

## File Ownership

| Path               | Owner   | Notes                                 |
| ------------------ | ------- | ------------------------------------- |
| `docs/01.requirements/**`   | product | Product Requirement Documents         |
| `docs/04.execution/plans/**` | product | Implementation plans (shared with qa) |

Product scope does **not** own infra manifests, governance files, or authored specs downstream of PRD.

## Subagent Bridge

No dedicated subagent for product scope in this k8s-focused repo.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Product intent and acceptance criteria are testable.
- Plan/task references are anchored to PRD entries.
- Out-of-scope boundaries are explicit.
