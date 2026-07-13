---
title: 'Operations Scope'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Operations Scope

## Overview

Persona: Operations Engineer

## Authority Boundary

### File Ownership

| Path                      | Owner | Notes                        |
| ------------------------- | ----- | ---------------------------- |
| `docs/05.operations/policies/**`   | ops   | Operations policy documents  |
| `docs/05.operations/runbooks/**`     | ops   | Runbook procedures           |
| `docs/05.operations/incidents/**`    | ops   | Incident records             |
| `infrastructure/tests/**` | ops   | Cluster verification scripts |

Ops scope does **not** own `gitops/` (infra scope) or `docs/00.agent-governance/` (meta scope).

## Governance Context

### Source of Truth

- `docs/05.operations/policies/`
- `docs/05.operations/runbooks/`
- `docs/05.operations/incidents/`

## Current Contract

### Responsibilities

- Align operational execution with approved policy.
- Keep runbook procedures executable and incident-linked.
- Preserve recoverability and clear escalation paths.

### Subagent Bridge

Agents that import this scope: `.claude/agents/incident-responder.md`.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Validation and Refresh

### Definition of Done

- Operational actions are traceable to policy or incident context.
- Recovery and rollback paths are explicit.
- Evidence collection and escalation responsibilities are clear.

## Related Documents
