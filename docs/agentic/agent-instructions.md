---
layer: "meta"
---
# Project Agent Instructions

Shared entrypoint for all AI agents. This repository enforces a **Lazy Loading Protocol** to maintain context efficiency.

## 1. Lazy Loading Protocol

Agents MUST follow this protocol based on user intent:

1. **Identify Intent**: Determine the task type (e.g., Spec work, Incident response).
2. **Trigger Rule**: Identify the governing rule in `docs/agentic/rules/`.
3. **Load Scope**: Import the corresponding scope file from `docs/agentic/scopes/`.
4. **Execute**: Leverage **Greedy Autonomy** to use any relevant skill.

## 2. Intent-to-Scope Mapping

| Task Type | Trigger Rule | Load Scope | Target Directory |
| :--- | :--- | :--- | :--- |
| Requirements | `@rules/personas.md` | `@scopes/prd.md` | `docs/prd/` |
| Technical Spec | `@rules/core.md` | `@scopes/specs.md` | `docs/specs/` |
| Implementation Plan | `@rules/repo-navigation.md` | `@scopes/plans.md` | `docs/plans/` |
| Architecture Decision | `@rules/docs-map.md` | `@scopes/adr.md` | `docs/adr/` |
| System Reference | `@rules/docs-map.md` | `@scopes/ard.md` | `docs/ard/` |
| Deployment/Operations | `@rules/core.md` | `@scopes/runbooks.md` | `docs/runbooks/` |
| Incident Handling | `@rules/personas.md` | `@scopes/incidents.md` | `docs/operations/incidents/` |
| Performance/Strategic | `@rules/docs-map.md` | `@scopes/operations.md` | `docs/operations/` |

## 3. Core Directives

- **Non-Technical PRDs**: PRDs define *What* and *Why*; Specs define *How*.
- **Plural Persistence**: Always use `docs/plans/` and `docs/specs/`.
- **Greedy Skills**: Do not ask for tool permission if it helps the goal.
- **Layered Truth**: Every document MUST include `layer:` metadata.
