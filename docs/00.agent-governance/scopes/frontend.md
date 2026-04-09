# Frontend Scope

Persona: Frontend Engineer

## Source of Truth

- `docs/04.specs/`
- `docs/01.prd/`

## Responsibilities

- Implement UI behavior and states as specified.
- Preserve accessibility and responsive behavior.
- Keep UI contract decisions aligned with stage artifacts.

## File Ownership

| Path               | Owner    | Notes                                          |
| ------------------ | -------- | ---------------------------------------------- |
| `docs/04.specs/**` | frontend | Technical specifications (shared with backend) |
| `docs/01.prd/**`   | frontend | Product requirements (read-only input)         |

Frontend scope does **not** own infra manifests (`gitops/`, `infrastructure/`) or governance files.

## Subagent Bridge

No dedicated subagent for frontend scope in this k8s-focused repo.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- UI changes are traceable to spec and acceptance criteria.
- Accessibility and responsive checks are executed.
- Frontend behavior changes are reflected in validation evidence.
