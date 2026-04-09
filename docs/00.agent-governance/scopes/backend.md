# Backend Scope

Persona: Backend Engineer

## Source of Truth

- `docs/04.specs/`
- `docs/01.prd/`

## Responsibilities

- Implement backend behavior defined by specs.
- Keep API and data contract changes traceable to specs.
- Preserve compatibility expectations and explicit error semantics.

## File Ownership

| Path               | Owner   | Notes                                  |
| ------------------ | ------- | -------------------------------------- |
| `docs/04.specs/**` | backend | Technical specifications               |
| `docs/01.prd/**`   | backend | Product requirements (read-only input) |

Backend scope does **not** own infra manifests (`gitops/`, `infrastructure/`) or governance files.

## Subagent Bridge

No dedicated subagent for backend scope in this k8s-focused repo.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Backend changes map to spec sections.
- Validation path is documented in plan/task artifacts.
- No undocumented contract drift is introduced.
