---
layer: "meta"
---

# Project Agent Instructions

Shared entrypoint for all AI agents. This repository enforces a **Lazy Loading Protocol** to maintain context efficiency.

## 1. Lazy Loading Protocol

Agents MUST follow this protocol based on user intent:

1. **Identify Intent**: Determine the task type (e.g., Spec work, Incident response).
2. **Trigger Rule**: Load `docs/00.agent/rules/bootstrap.md` and check `docs/00.agent/rules/persona-matrix.md`.
3. **Load Scope**: Import the corresponding functional scope file from `docs/00.agent/scopes/`.
4. **Execute**: Leverage **Greedy Autonomy** to use any relevant skill.

## 2. Intent-to-Scope Mapping

| Task Type | Trigger Rule | Load Scope | Target Directory |
| :--- | :--- | :--- | :--- |
| Product / Requirements | `persona-matrix.md` | `product.md` | `docs/01.prd/` |
| System Architecture | `persona-matrix.md` | `architecture.md` | `docs/02.ard/`, `docs/03.adr/` |
| Backend Development | `persona-matrix.md` | `backend.md` | `docs/04.specs/` |
| Frontend Development | `persona-matrix.md` | `frontend.md` | `docs/04.specs/` |
| Infrastructure / Ops | `persona-matrix.md` | `infra.md` | `docs/08.operations/`, `docs/09.runbooks/` |
| Security / Compliance | `persona-matrix.md` | `security.md` | `docs/04.specs/`, `docs/10.incidents/` |
| QA / Testing | `persona-matrix.md` | `qa.md` | `docs/05.plans/`, `docs/06.tasks/` |

## 3. Core Directives

- **English Mandatory**: All files in `docs/00.agent/` MUST be written in English.
- **Spec-Driven**: All work MUST be grounded in `docs/01.prd/` and `docs/04.specs/`.
- **Greedy Skills**: Do not ask for tool permission if it helps the goal.
- **Layered Truth**: Every document MUST include `layer:` metadata.
- **Bootstrap First**: Always load `docs/00.agent/rules/bootstrap.md`.
