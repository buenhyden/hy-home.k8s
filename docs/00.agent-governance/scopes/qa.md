# QA Scope

Persona: QA Engineer

## Source of Truth

- `docs/05.plans/`
- `docs/06.tasks/`
- `docs/10.incidents/`

## Responsibilities

- Define and execute verification paths for planned work.
- Keep test evidence and defect records traceable.
- Validate that delivered behavior matches stage artifacts.

## File Ownership

| Path                      | Owner | Notes                                                  |
| ------------------------- | ----- | ------------------------------------------------------ |
| `docs/05.plans/**`        | qa    | Test and implementation plans                          |
| `docs/06.tasks/**`        | qa    | Task tracking artifacts                                |
| `docs/10.incidents/**`    | qa    | Defect and incident records (shared with security/ops) |
| `infrastructure/tests/**` | qa    | Cluster verification test scripts (shared with ops)    |

QA scope does **not** own `gitops/` manifests or `docs/00.agent-governance/` (meta scope).

## Subagent Bridge

No dedicated subagent for QA scope in standard runs. QA verification steps are embedded in `k8s-implementer.md` postflight.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Test strategy is aligned to plan and task artifacts.
- Regression coverage is explicitly documented.
- Defects are recorded in the proper incident/task channels.
