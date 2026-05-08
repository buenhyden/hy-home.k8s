# Security Scope

Persona: Security Engineer

## Source of Truth

- `docs/04.specs/`
- `docs/10.incidents/`
- `docs/10.incidents/postmortems/`

## Responsibilities

- Validate security controls against defined specifications.
- Ensure secrets and access controls follow secure repository patterns.
- Keep incident learnings connected to prevent recurrence.

## File Ownership

| Path                                  | Owner    | Notes                       |
| ------------------------------------- | -------- | --------------------------- |
| `docs/10.incidents/**`                | security | Incident records            |
| `docs/10.incidents/postmortems/**`    | security | Postmortem documents        |
| `gitops/platform/network-policies/**` | security | k8s NetworkPolicy manifests |
| `infrastructure/vault/**`             | security | Vault policy definitions    |

Security scope does **not** own `gitops/apps/` or `docs/00.agent-governance/` (meta scope).

## Subagent Bridge

Agents that import this scope: `.claude/agents/security-auditor.md`.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Security-impacting changes are traceable to specs or incident actions.
- Secret-handling workflow remains compliant with infra policy.
- Relevant mitigations are reflected in runbooks or follow-up tasks.
