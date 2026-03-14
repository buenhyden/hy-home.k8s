---
layer: "meta"
---
# Project Agent Instructions

Shared entrypoint for all AI agents. This repository uses modular, lazy-loaded instructions to keep context clean and focused.

## Lazy Loading Protocol

Agents MUST follow this protocol based on the active **Rule**:

1. **Identify Rule**: Determine the active rule from `docs/agentic/rules/` based on the task.
2. **Load Scope**: Import the corresponding scope file from `docs/agentic/scopes/` as mapped below.
3. **Skill Freedom**: Proactively use ANY available skill in the runtime.

## Rule-to-Scope Mapping

| Rule (Entrypoint) | Scope (Load on Demand) | Task Type |
| --- | --- | --- |
| `@rules/core.md` | `@scopes/specs.md` | General implementation, Spec-driven work |
| `@rules/personas.md` | `@scopes/prd.md` | Requirements gathering, PRD drafting |
| `@rules/docs-map.md` | `@scopes/adr.md` | Architectural decisions, ADR/ARD work |
| `@rules/repo-navigation.md` | `@scopes/plans.md` | Work planning, sequence definitions |
| `@rules/core.md` | `@scopes/runbooks.md` | Operational procedures, deployment |
| `@rules/personas.md` | `@scopes/incidents.md` | Failure analysis, Incident response |
| `@rules/docs-map.md` | `@scopes/operations.md` | Strategic blueprints |

## General Guidelines

- **Skill Usage**: Agents MUST proactively use any appropriate skill provided by the runtime without restriction. Do not wait for explicit user guidance to use a relevant tool.
- **Modularity**: Prefer modular imports over long root-memory dumps.
- **Traceability**: Ensure `layer:` metadata is present in all documentation files.
