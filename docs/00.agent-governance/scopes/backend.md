---
title: 'Backend Scope'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
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

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Validation and Refresh

### Definition of Done

- Backend changes map to spec sections.
- Validation path is documented in plan/task artifacts.
- No undocumented contract drift is introduced.

## Related Documents
