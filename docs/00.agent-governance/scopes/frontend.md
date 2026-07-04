# Frontend Scope

Persona: Frontend Engineer

## Source of Truth

- `docs/03.specs/`
- `docs/01.requirements/`

## Responsibilities

- Implement UI behavior and states as specified.
- Preserve accessibility and responsive behavior.
- Keep UI contract decisions aligned with stage artifacts.

## File Ownership

| Path               | Owner    | Notes                                          |
| ------------------ | -------- | ---------------------------------------------- |
| `docs/03.specs/**` | frontend | Technical specifications (shared with backend) |
| `docs/01.requirements/**`   | frontend | Product requirements (read-only input)         |

Frontend scope does **not** own infra manifests (`gitops/`, `infrastructure/`) or governance files.

## Subagent Bridge

No dedicated subagent for frontend scope in this k8s-focused repo.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Definition of Done

- UI changes are traceable to spec and acceptance criteria.
- Accessibility and responsive checks are executed.
- Frontend behavior changes are reflected in validation evidence.
