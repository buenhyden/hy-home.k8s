---
title: 'Documentation Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
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

Subagent dispatch: follow the [Subagent Protocol](../subagent-protocol.md); never
inline a full role definition when an applicable native or local adapter exists.

## Validation and Refresh

### Definition of Done

- Links across related stage docs are valid.
- Language policy remains consistent with root README guidance.
- Templates remain aligned with active taxonomy and governance policy.

## Related Documents

- [Documentation Protocol](../rules/documentation-protocol.md)
- [Document Stage Routing Rules](../rules/document-stage-routing.md)
- [Operations Guides Index](../../05.operations/guides/README.md)
- [References Index](../../90.references/README.md)
- [Templates Index](../../99.templates/README.md)
