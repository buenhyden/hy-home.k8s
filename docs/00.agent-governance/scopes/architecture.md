---
title: 'Architecture Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
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

Subagent dispatch: follow the [Subagent Protocol](../subagent-protocol.md); never
inline a full role definition when an applicable native or local adapter exists.

## Validation and Refresh

### Definition of Done

- Architectural changes are traceable to PRD and specs.
- Affected ADR entries exist or are explicitly referenced.
- Cross-layer impacts are documented for backend, frontend, and infra scopes.

## Related Documents

- [Persona Protocol](../rules/persona.md)
- [Stage Authoring Matrix](../rules/stage-authoring-matrix.md)
- [Architecture Index](../../02.architecture/README.md)
- [Specifications Index](../../03.specs/README.md)
