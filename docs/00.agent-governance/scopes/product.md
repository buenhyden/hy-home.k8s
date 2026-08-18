---
title: 'Product Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Product Scope

## Overview

Persona: Product Manager

## Authority Boundary

### File Ownership

| Path               | Owner   | Notes                                 |
| ------------------ | ------- | ------------------------------------- |
| `docs/01.requirements/**`   | product | Product Requirement Documents         |
| `docs/03.specs/*/plan.md` | product | Feature-local implementation plans (shared with qa) |

Product scope does **not** own infra manifests, governance files, or authored specs downstream of PRD.

## Governance Context

### Source of Truth

- `docs/01.requirements/`
- `docs/03.specs/*/plan.md`

## Current Contract

### Responsibilities

- Keep intent, value, and acceptance criteria clear before implementation.
- Ensure implementation plans and tasks stay traceable to PRD intent.
- Flag gaps when downstream stages drift from product requirements.

### Subagent Bridge

No dedicated subagent for product scope in this k8s-focused repo.

Subagent dispatch: follow the [Subagent Protocol](../subagent-protocol.md); never
inline a full role definition when an applicable native or local adapter exists.

## Validation and Refresh

### Definition of Done

- Product intent and acceptance criteria are testable.
- Plan/task references are anchored to PRD entries.
- Out-of-scope boundaries are explicit.

## Related Documents

- [Persona Protocol](../rules/persona.md)
- [Stage Authoring Matrix](../rules/document-authoring.md)
- [Requirements Index](../../01.requirements/README.md)
- [Spec Work-Unit Index](../../03.specs/README.md)
