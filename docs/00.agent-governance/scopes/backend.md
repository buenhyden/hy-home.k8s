# Backend Scope

Persona: Backend Engineer

## Source of Truth

- `docs/03.specs/`
- `docs/01.requirements/`

## Responsibilities

- Implement backend behavior defined by specs.
- Keep API and data contract changes traceable to specs.
- Preserve compatibility expectations and explicit error semantics.

## File Ownership

| Path               | Owner   | Notes                                  |
| ------------------ | ------- | -------------------------------------- |
| `docs/03.specs/**` | backend | Technical specifications               |
| `docs/01.requirements/**`   | backend | Product requirements (read-only input) |

Backend scope does **not** own infra manifests (`gitops/`, `infrastructure/`) or governance files.

## Subagent Bridge

No dedicated subagent for backend scope in this k8s-focused repo.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Definition of Done

- Backend changes map to spec sections.
- Validation path is documented in plan/task artifacts.
- No undocumented contract drift is introduced.
