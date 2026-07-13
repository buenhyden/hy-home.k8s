---
title: 'Documentation Scope'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Documentation Scope

## Overview

Persona: Technical Writer

## Authority Boundary

### File Ownership

| Path                    | Owner | Notes                           |
| ----------------------- | ----- | ------------------------------- |
| `docs/05.operations/guides/**`     | docs  | Bootstrap and onboarding guides |
| `docs/90.references/**` | docs  | Reference documents             |
| `docs/98.archive/**` | docs  | Archive Tombstone index and metadata-only old document Tombstones |
| `docs/99.templates/**`  | docs  | Document templates              |
| `README.md`             | docs  | Root README (Korean)            |
| `docs/README.md`        | docs  | Docs index README (Korean)      |

Docs scope does **not** own `docs/00.agent-governance/` (meta scope) or infra manifests.
Stage README ownership follows the owning stage persona. Docs scope owns shared README and template standards, not every stage-specific README implementation detail.

## Governance Context

### Source of Truth

- `docs/05.operations/guides/`
- `docs/90.references/`
- `docs/98.archive/`
- `docs/99.templates/`

## Current Contract

### Responsibilities

- Keep documentation traceable to stage taxonomy.
- Keep language policy explicit: governance/spec internals in English, human overviews in Korean.
- Avoid rewriting authored stage content unless explicitly requested.

### Subagent Bridge

Agents that import this scope: `.claude/agents/doc-writer.md`,
`.claude/agents/wiki-curator.md`.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Validation and Refresh

### Definition of Done

- Links across related stage docs are valid.
- Language policy remains consistent with root README guidance.
- Templates remain aligned with active taxonomy and governance policy.

## Related Documents
