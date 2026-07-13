---
title: 'Architecture Scope'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Architecture Scope

## Overview

Persona: System Architect

## Authority Boundary

### File Ownership

| Path               | Owner        | Notes                              |
| ------------------ | ------------ | ---------------------------------- |
| `docs/02.architecture/requirements/**`   | architecture | Architecture Requirement Documents |
| `docs/02.architecture/decisions/**`   | architecture | Architecture Decision Records      |
| `docs/03.specs/**` | architecture | Technical specifications           |

Architecture scope does **not** own infrastructure (`gitops/`, `infrastructure/`) or governance (`docs/00.agent-governance/`).

## Governance Context

### Source of Truth

- `docs/02.architecture/requirements/`
- `docs/02.architecture/decisions/`
- `docs/03.specs/`

## Current Contract

### Responsibilities

- Maintain architecture consistency across ARD, ADR, and specs.
- Ensure major design changes are recorded as ADRs.
- Keep architecture-level constraints explicit for implementation layers.

### Subagent Bridge

Agents that import this scope: `.claude/agents/code-reviewer.md`.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Validation and Refresh

### Definition of Done

- Architectural changes are traceable to PRD and specs.
- Affected ADR entries exist or are explicitly referenced.
- Cross-layer impacts are documented for backend, frontend, and infra scopes.

## Related Documents
