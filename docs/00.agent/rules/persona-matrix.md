# Unified Persona & Rule Matrix

This matrix maps AI Agent personas to their target layers and mandatory governance files.

## 1. Core Personas

| Persona | Primary Layer | Primary SSoT Path | Mandatory Rules |
| :--- | :--- | :--- | :--- |
| **Product Manager** | Product | `docs/01.prd/` | `0110-prd-standard.md` |
| **System Architect** | Architecture | `docs/02.ard/` | `0130-architecture-standard.md` |
| **Frontend Engineer** | Frontend | `docs/04.specs/` | `0210-frontend-standard.md` |
| **Backend Engineer** | Backend | `docs/04.specs/` | `0220-backend-standard.md` |
| **Infra/DevOps Miner** | Infra | `docs/08.operations/` | `0310-infra-standard.md` |
| **Security Officer** | Security | `docs/04.specs/` | `0410-security-audit.md` |
| **QA Engineer** | QA | `docs/05.plans/` | `0510-qa-standard.md` |

## 2. Rule Discovery Protocol

When an agent is assigned a task:

1. Check the **Layer** metadata in the relevant documentation.
2. Cross-reference with this matrix to select the correct **Persona**.
3. Load the mandatory rules from `docs/00.agent/rules/` JIT.

> [!IMPORTANT]
> Some rule files may reside in `.agent/rules/` while high-level scopes reside in `docs/00.agent/scopes/`. Always prioritize the specific rule file for implementation work.
