---
title: 'Infrastructure Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Infrastructure Scope

## Overview

Persona: Infra Engineer

## Authority Boundary

### File Ownership

| Path                    | Owner | Notes                                 |
| ----------------------- | ----- | ------------------------------------- |
| `infrastructure/**`     | infra | k3d, bootstrap, networking assets     |
| `gitops/**`             | infra | ArgoCD apps, platform, workloads      |
| `scripts/**`            | infra | k8s validation and automation scripts |
| `docs/05.operations/policies/**` | infra | Operations policy                     |
| `docs/05.operations/runbooks/**`   | infra | Runbook procedures                    |

Infra scope does **not** own `docs/00.agent-governance/` (meta scope) or upstream requirements/architecture/execution docs.

## Governance Context

### Source of Truth

- `docs/05.operations/policies/`
- `docs/05.operations/runbooks/`
- `docs/03.specs/`

### Workspace Facts

- Local cluster patterns use `k3d` config under `infrastructure/k3d/`.
- GitOps entrypoint is `gitops/clusters/local/root-application.yaml`.
- Networking/bootstrap assets are under `infrastructure/`.

## Current Contract

### Responsibilities

- Keep infra changes aligned with operations policy and runbooks.
- Preserve secure secret handling and network isolation.
- Ensure deployment workflows remain reproducible from repository assets.

### Subagent Bridge

Agents that import this scope: `.claude/agents/k8s-implementer.md`,
`.claude/agents/gitops-reviewer.md`, `.claude/agents/incident-responder.md`.

Subagents must read `.claude/agents/<name>.md` (which `@import`s this scope) before starting work.
Subagent dispatch: follow the [Subagent Protocol](../subagent-protocol.md); never
inline a full role definition when an applicable native or local adapter exists.

## Validation and Refresh

### Definition of Done

- Infra changes map to existing operations/runbook stages.
- Command and path references point to real workspace assets.
- No plain-text secret workflow is introduced.
- GitOps-First: all cluster changes via PR → ArgoCD.

## Related Documents

- [Harness Approval Boundaries](../rules/approval-boundaries.md)
- [Agent Quality Standards](../rules/quality-standards.md)
- [Operations Policies Index](../../05.operations/policies/README.md)
- [Runbooks Index](../../05.operations/runbooks/README.md)
