---
title: 'Product Scope'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Product Scope

## Overview

Persona: Product Manager

## Authority Boundary

### File Ownership

| Path               | Owner   | Notes                                 |
| ------------------ | ------- | ------------------------------------- |
| `docs/01.requirements/**`   | product | Product Requirement Documents         |
| `docs/04.execution/plans/**` | product | Implementation plans (shared with qa) |

Product scope does **not** own infra manifests, governance files, or authored specs downstream of PRD.

## Governance Context

### Source of Truth

- `docs/01.requirements/`
- `docs/04.execution/plans/`

## Current Contract

### Responsibilities

- Keep intent, value, and acceptance criteria clear before implementation.
- Ensure implementation plans and tasks stay traceable to PRD intent.
- Flag gaps when downstream stages drift from product requirements.

### Subagent Bridge

No dedicated subagent for product scope in this k8s-focused repo.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Validation and Refresh

### Definition of Done

- Product intent and acceptance criteria are testable.
- Plan/task references are anchored to PRD entries.
- Out-of-scope boundaries are explicit.

## Related Documents

- [Persona Protocol](../rules/persona.md)
- [Stage Authoring Matrix](../rules/stage-authoring-matrix.md)
- [Requirements Index](../../01.requirements/README.md)
- [Execution Index](../../04.execution/README.md)
