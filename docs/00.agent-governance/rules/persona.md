---
title: 'AI Agent Persona Protocol (March 2026)'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# AI Agent Persona Protocol (March 2026)

## Overview

Persona routing for layer-based execution.

### Activation Steps

1. Load `rules/bootstrap.md`.
2. Complete `rules/preflight-checklist.md`.
3. Identify target layer and stage.
4. Select the persona and load one matching layer scope from `scopes/`.
5. Load provider notes from `providers/` when relevant.
6. Execute using the selected persona contract.
7. Validate completion with `rules/postflight-checklist.md`.

## Authority Boundary

Persona selection assigns one primary decision lens and matching scope; it
does not transfer file ownership, approval authority, or provider permissions.
Cross-layer work must declare each scope transition. Unmapped or conflicting
ownership routes to the Governance Steward and, when scope would materially
change, to the human requester.

## Governance Context

### Persona Mapping

| Persona | Layer | Primary SSoT |
| --- | --- | --- |
| Product Manager | product | `docs/01.requirements/` |
| System Architect | architecture | `docs/02.architecture/requirements/`, `docs/02.architecture/decisions/` |
| Backend Engineer | backend | `docs/03.specs/` |
| Frontend Engineer | frontend | `docs/03.specs/` |
| Infra Engineer | infra | `docs/05.operations/policies/`, `docs/05.operations/runbooks/` |
| Operations Engineer | ops | `docs/05.operations/policies/`, `docs/05.operations/incidents/` |
| Security Engineer | security | `docs/03.specs/`, `docs/05.operations/incidents/` |
| QA Engineer | qa | `docs/04.execution/plans/`, `docs/04.execution/tasks/`, `docs/05.operations/incidents/` |
| Technical Writer | docs | `docs/05.operations/guides/`, `docs/90.references/` |
| Governance Steward | meta | `docs/00.agent-governance/` |

### Stage Mapping

Use [stage-authoring-matrix.md](stage-authoring-matrix.md) for canonical taxonomy authoring timing, inputs, outputs, templates, and completion criteria.

## Current Contract

- Select exactly one primary persona before non-trivial execution and load its
  scope file after preflight.
- Treat persona mappings as routing metadata; canonical stage documents and
  scope ownership remain the source of implementation authority.
- A delegated role must use an existing provider-native adapter and the
  provider-neutral semantics contract rather than an inline replacement.
- Re-resolve persona and scope when the work crosses a layer boundary.

## Validation and Refresh

Run `bash scripts/validate-repo-quality-gates.sh .` after persona or scope-map
changes. When a change affects delegated roles, also run
`python3 scripts/validate-agent-role-semantics.py --root .` and
`python3 scripts/validate-agent-roster-currentness.py .`. Review the mapping
when a stage owner, scope file, or provider role roster changes.

## Related Documents

- [Bootstrap Governance](bootstrap.md)
- [Preflight Checklist](preflight-checklist.md)
- [Stage Authoring Matrix](stage-authoring-matrix.md)
- [Subagent Protocol](../subagent-protocol.md)
