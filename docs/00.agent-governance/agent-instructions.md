---
layer: "meta"
---

# Project Agent Instructions

Shared entrypoint for all AI agents. Enforces a **Lazy Loading Protocol**.

## 1. Lazy Loading Protocol (JIT)

1. **Identify Intent**: Determine the task type (e.g., Spec work, Infrastructure setup).
2. **Bootstrap Discovery**: Load `docs/00.agent-governance/rules/bootstrap.md` to verify taxonomy.
3. **Trigger Rule**: Load `docs/00.agent-governance/rules/persona-matrix.md` to identify the required Persona.
4. **Load Scope**: Import the corresponding scope from `docs/00.agent-governance/scopes/`.
5. **Execute**: Ground work in `docs/01.prd/` to `docs/11.postmortems/`.

## 2. Intent-to-Scope Mapping

| Intent | Persona | Load Scope | Primary SSoT |
| :--- | :--- | :--- | :--- |
| Requirements | PM | `product.md` | `docs/01.prd/` |
| Architecture | Architect | `architecture.md` | `docs/02.ard/`, `docs/03.adr/` |
| Specifications | Engineer | `docs.md` | `docs/04.specs/` |
| Backend | Backend Dev | `backend.md` | `docs/04.specs/` |
| Frontend | Frontend Dev | `frontend.md` | `docs/04.specs/` |
| Infrastructure | DevOps | `infra.md` | `docs/08.operations/` |
| Security | Security | `security.md` | `docs/04.specs/`, `docs/10.incidents/` |
| QA / Testing | QA | `qa.md` | `docs/05.plans/`, `docs/06.tasks/` |
| Guides | Writer | `docs.md` | `docs/07.guides/` |
| Operations | Ops | `infra.md` | `docs/09.runbooks/` |
| Postmortems | Analyst | `docs.md` | `docs/11.postmortems/` |
| References | Researcher | `docs.md` | `docs/90.references/` |
| Templates | Engineer | `docs.md` | `docs/99.templates/` |

## 3. Core Directives

- **English Mandatory**: All internal instructions in `docs/00.agent-governance/` MUST be in English.
- **Human-Facing**: READMEs and overviews MUST be in Korean.
- **Spec-Driven**: Changes require approved artifacts in `docs/01.prd/` and `docs/04.specs/`.
- **Response Mandate**: Always respond to user requests in **Korean (한국어)**.
- **Bootstrap First**: Always load `docs/00.agent-governance/rules/bootstrap.md` initially to establish context.
