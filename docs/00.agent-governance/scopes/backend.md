---
title: 'Backend Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Backend Scope

## Overview

Persona: Backend Engineer

## Authority Boundary

### File Ownership

| Path               | Owner   | Notes                                  |
| ------------------ | ------- | -------------------------------------- |
| `docs/03.specs/**` | backend | Technical specifications               |
| `docs/01.requirements/**`   | backend | Product requirements (read-only input) |

Backend scope does **not** own infra manifests (`gitops/`, `infrastructure/`) or governance files.

## Governance Context

### Source of Truth

- `docs/03.specs/`
- `docs/01.requirements/`

## Current Contract

### Responsibilities

- Implement backend behavior defined by specs.
- Keep API and data contract changes traceable to specs.
- Preserve compatibility expectations and explicit error semantics.

### Subagent Bridge

No dedicated subagent for backend scope in this k8s-focused repo.

Subagent dispatch: follow the [Subagent Protocol](../subagent-protocol.md); never
inline a full role definition when an applicable native or local adapter exists.

## Validation and Refresh

### Definition of Done

- Backend changes map to spec sections.
- Validation path is documented in plan/task artifacts.
- No undocumented contract drift is introduced.

## Related Documents

- [Persona Protocol](../rules/persona.md)
- [Stage Authoring Matrix](../rules/stage-authoring-matrix.md)
- [Specifications Index](../../03.specs/README.md)
- [Requirements Index](../../01.requirements/README.md)
