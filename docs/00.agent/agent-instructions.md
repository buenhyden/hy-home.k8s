---
layer: "meta"
---

# Project Agent Instructions

Shared entrypoint for all AI agents. Enforces a **Lazy Loading Protocol**.

## 1. Lazy Loading Protocol

1. **Identify Intent**: Determine the task type (e.g., Spec work, Infra setup).
2. **Trigger Rule**: Load `docs/00.agent/rules/bootstrap.md` and `docs/00.agent/rules/persona-matrix.md`.
3. **Load Scope**: Import the corresponding scope from `docs/00.agent/scopes/`.
4. **Execute**: Ground work in `docs/01.prd/` and `docs/04.specs/`.

## 2. Intent-to-Scope Mapping

| Intent | Persona | Load Scope | SSoT Path |
| :--- | :--- | :--- | :--- |
| Requirements | PM | `product.md` | `docs/01.prd/` |
| Architecture | Architect | `architecture.md` | `docs/02.ard/`, `docs/03.adr/` |
| Backend | Backend Dev | `backend.md` | `docs/04.specs/` |
| Frontend | Frontend Dev | `frontend.md` | `docs/04.specs/` |
| Infrastructure | DevOps | `infra.md` | `docs/08.operations/`, `docs/09.runbooks/` |
| Security | Security | `security.md` | `docs/04.specs/`, `docs/10.incidents/` |
| QA / Testing | QA | `qa.md` | `docs/05.plans/`, `docs/06.tasks/` |

## 3. Core Directives

- **English Mandatory**: All internal instructions in `docs/00.agent/` MUST be in English.
- **Human-Friendly**: Readmes and overviews MUST be in Korean.
- **Spec-Driven**: Changes require approved `PRD` and `Spec` in `docs/01.prd/` and `docs/04.specs/`.
- **Response Mandate**: Always respond to user requests in **Korean (한국어)**.
- **Bootstrap First**: Always load `docs/00.agent/rules/bootstrap.md` initially.
