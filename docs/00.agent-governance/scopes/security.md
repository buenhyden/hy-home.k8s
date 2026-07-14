---
title: 'Security Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Security Scope

## Overview

Persona: Security Engineer

## Authority Boundary

### File Ownership

| Path                                  | Owner    | Notes                       |
| ------------------------------------- | -------- | --------------------------- |
| `docs/05.operations/incidents/**`                | security | Incident records            |
| `docs/05.operations/incidents/*/INC-*/postmortem.md` | security | Postmortem documents        |
| `gitops/platform/network-policies/**` | security | k8s NetworkPolicy manifests |
| `infrastructure/vault/**`             | security | Vault policy definitions    |

Security scope does **not** own `gitops/apps/` or `docs/00.agent-governance/` (meta scope).

## Governance Context

### Source of Truth

- `docs/03.specs/`
- `docs/05.operations/incidents/`
- `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md`

## Current Contract

### Responsibilities

- Validate security controls against defined specifications.
- Ensure secrets and access controls follow secure repository patterns.
- Keep incident learnings connected to prevent recurrence.

### Subagent Bridge

Agents that import this scope: `.claude/agents/security-auditor.md`.

Subagent dispatch: follow the [Subagent Protocol](../subagent-protocol.md); never
inline a full role definition when an applicable native or local adapter exists.

## Validation and Refresh

### Definition of Done

- Security-impacting changes are traceable to specs or incident actions.
- Secret-handling workflow remains compliant with infra policy.
- Relevant mitigations are reflected in runbooks or follow-up tasks.

## Related Documents

- [Harness Approval Boundaries](../rules/approval-boundaries.md)
- [Agent Quality Standards](../rules/quality-standards.md)
- [Specifications Index](../../03.specs/README.md)
- [Incidents Index](../../05.operations/incidents/README.md)
