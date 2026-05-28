# QA Scope

Persona: QA Engineer

## Source of Truth

- `docs/04.execution/plans/`
- `docs/04.execution/tasks/`
- `docs/05.operations/incidents/`

## Responsibilities

- Define and execute verification paths for planned work.
- Keep test evidence and defect records traceable.
- Validate that delivered behavior matches stage artifacts.
- Monitor and maintain QA/CI reference guides under `docs/05.operations/guides/`.
- Reference `scripts/validate-*.sh` and `scripts/check-*.sh` as the primary repo-static QA execution surface.
- Enforce 90% coverage policy for testable application code (or validation-matrix coverage for infrastructure) when reviewing verification evidence.

## File Ownership

| Path                      | Owner | Notes                                                  |
| ------------------------- | ----- | ------------------------------------------------------ |
| `docs/04.execution/plans/**`        | qa    | Test and implementation plans                          |
| `docs/04.execution/tasks/**`        | qa    | Task tracking artifacts                                |
| `docs/05.operations/incidents/**`    | qa    | Defect and incident records (shared with security/ops) |
| `infrastructure/tests/**` | qa    | Cluster verification test scripts (shared with ops)    |
| `scripts/validate-*.sh`, `scripts/check-*.sh` | qa | Repo-static QA gate scripts (shared with ops/infra) |

QA scope does **not** own `gitops/` manifests or `docs/00.agent-governance/` (meta scope).

## Subagent Bridge

No dedicated subagent for QA scope in standard runs. QA verification steps are embedded in `k8s-implementer.md` postflight.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Test strategy is aligned to plan and task artifacts.
- Regression coverage is explicitly documented.
- 90% coverage target is maintained for testable application code, or validation-matrix coverage is verified for infrastructure changes.
- Defects are recorded in the proper incident/task channels.

## Related Documents

- [Quality Standards](../rules/quality-standards.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Stage Authoring Matrix](../rules/stage-authoring-matrix.md)
- [Persona Protocol](../rules/persona.md)
