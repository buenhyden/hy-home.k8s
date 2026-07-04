# Security Scope

Persona: Security Engineer

## Source of Truth

- `docs/03.specs/`
- `docs/05.operations/incidents/`
- `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md`

## Responsibilities

- Validate security controls against defined specifications.
- Ensure secrets and access controls follow secure repository patterns.
- Keep incident learnings connected to prevent recurrence.

## File Ownership

| Path                                  | Owner    | Notes                       |
| ------------------------------------- | -------- | --------------------------- |
| `docs/05.operations/incidents/**`                | security | Incident records            |
| `docs/05.operations/incidents/*/INC-*/postmortem.md` | security | Postmortem documents        |
| `gitops/platform/network-policies/**` | security | k8s NetworkPolicy manifests |
| `infrastructure/vault/**`             | security | Vault policy definitions    |

Security scope does **not** own `gitops/apps/` or `docs/00.agent-governance/` (meta scope).

## Subagent Bridge

Agents that import this scope: `.claude/agents/security-auditor.md`.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Definition of Done

- Security-impacting changes are traceable to specs or incident actions.
- Secret-handling workflow remains compliant with infra policy.
- Relevant mitigations are reflected in runbooks or follow-up tasks.
