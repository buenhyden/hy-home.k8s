---
title: 'Meta Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Meta Scope

## Overview

Persona: Governance Steward

## Authority Boundary

### File Ownership

| Path                          | Owner | Notes                                           |
| ----------------------------- | ----- | ----------------------------------------------- |
| `docs/00.agent-governance/**` | meta  | All governance policy, rules, scopes, providers |
| `AGENTS.md`                   | meta  | Gateway contract                                |
| `CLAUDE.md`                   | meta  | Claude provider overlay                         |
| `GEMINI.md`                   | meta  | Gemini provider overlay                         |
| `.claude/settings.json`       | meta  | Team settings (git tracked)                     |
| `docs/00.agent-governance/hooks/**` | meta  | Shared runtime hook contracts                   |
| `.agents/skills/**`           | meta  | Repo-backed shared skill source of truth        |
| `.claude/skills/**`           | meta  | Claude symlink view of shared skills            |
| `.codex/**`                   | meta  | Codex role adapters and hook wiring             |

Meta scope owns provider-native agent roster and role-adapter contract shape
through `harness-catalog.md` and `subagent-protocol.md`; imported scope files
own the domain behavior for each worker.

Meta scope does **not** own `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`, `docs/98.archive/`, or `docs/99.templates/` (authored SSoT).

## Governance Context

### Source of Truth

- `docs/00.agent-governance/`

## Current Contract

### Responsibilities

- Maintain governance structure, consistency, and policy clarity.
- Keep rule routing deterministic and conflict-free.
- Enforce language and taxonomy boundaries.

### Subagent Bridge

No dedicated worker subagent for meta scope. Governance steward operates
directly, while `supervisor` imports `meta` only for routing and escalation
control.

Subagent dispatch: use the current runtime's provider-native delegated-agent
mechanism; never inline full role definitions when a provider-local agent file
exists.

## Validation and Refresh

### Definition of Done

- Governance tree matches expected structure.
- Rule references are valid and non-duplicative.
- Governance documents remain English-only.

## Related Documents

- [Bootstrap Governance](../rules/bootstrap.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Subagent Protocol](../subagent-protocol.md)
- [Templates Index](../../99.templates/README.md)
