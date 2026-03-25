# Unified Persona & Rule Matrix

This matrix maps AI Agent personas to their target layers and mandatory governance files.

## 1. Core Personas

| Persona | Primary Layer | Primary SSoT Path | Mandatory Rules (JIT) |
| :--- | :--- | :--- | :--- |
| **Product Manager** | Product | `docs/01.prd/` | `.agent/rules/0100-Product_and_Vision/0101-prd-blueprint-standard.md` |
| **System Architect** | Architecture | `docs/02.ard/` | `.agent/rules/1900-Architecture_Patterns/1901-architecture-rules.md` |
| **Frontend Engineer** | Frontend | `docs/04.specs/` | `.agent/rules/1000-Frontend/1000-frontend-standard.md` |
| **Backend Engineer** | Backend | `docs/04.specs/` | `.agent/rules/0900-Backend/0900-backend-standard.md` |
| **Infra/DevOps Miner** | Infra | `docs/08.operations/` | `.agent/rules/0300-DevOps_and_Infrastructure/0300-devops-pillar-standard.md` |
| **Security Officer** | Security | `docs/04.specs/` | `.agent/rules/2200-Security/2201-security-general.md` |
| **QA Engineer** | QA | `docs/05.plans/` | `.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md` |

## 2. Rule Discovery Protocol

When an agent is assigned a task:

1. Check the **Layer** metadata in the relevant documentation.
2. Cross-reference with this matrix to select the correct **Persona**.
3. Load the mandatory rules from `.agent/rules/` JIT.

> [!IMPORTANT]
> Always prioritize the specific rule file for implementation work over high-level scopes.
