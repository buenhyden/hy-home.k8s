# Operations Scope

Persona: Operations Engineer

## Source of Truth

- `docs/05.operations/policies/`
- `docs/05.operations/runbooks/`
- `docs/05.operations/incidents/`

## Responsibilities

- Align operational execution with approved policy.
- Keep runbook procedures executable and incident-linked.
- Preserve recoverability and clear escalation paths.

## File Ownership

| Path                      | Owner | Notes                        |
| ------------------------- | ----- | ---------------------------- |
| `docs/05.operations/policies/**`   | ops   | Operations policy documents  |
| `docs/05.operations/runbooks/**`     | ops   | Runbook procedures           |
| `docs/05.operations/incidents/**`    | ops   | Incident records             |
| `infrastructure/tests/**` | ops   | Cluster verification scripts |

Ops scope does **not** own `gitops/` (infra scope) or `docs/00.agent-governance/` (meta scope).

## Subagent Bridge

Agents that import this scope: `.claude/agents/incident-responder.md`.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Operational actions are traceable to policy or incident context.
- Recovery and rollback paths are explicit.
- Evidence collection and escalation responsibilities are clear.
