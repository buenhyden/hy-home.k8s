# Unified Persona & Rule Matrix

This matrix maps AI Agent personas to their target layers and mandatory governance files.

## 1. Core Personas

| Persona | Primary Layer | SSoT Path | Mandatory Rules (JIT) |
| :--- | :--- | :--- | :--- |
| **Product Manager** | Product | `docs/01.prd/` | `.agent/rules/0100-Standards/` |
| **System Architect** | Architecture | `docs/02.ard/` | `.agent/rules/1900-Architecture_Patterns/` |
| **Frontend Engineer** | Frontend | `docs/04.specs/` | `.agent/rules/1000-Frontend/` |
| **Backend Engineer** | Backend | `docs/04.specs/` | `.agent/rules/0900-Backend/` |
| **Infra/DevOps Miner** | Infra | `docs/08.operations/` | `.agent/rules/0300-DevOps_and_Infrastructure/` |
| **Security Officer** | Security | `docs/04.specs/` | `.agent/rules/2200-Security/` |
| **QA Engineer** | QA | `docs/05.plans/` | `.agent/rules/0700-Testing_and_QA/` |

## 2. Rule Discovery Protocol

When an agent is assigned a task:

1. Check the **Layer** metadata in the relevant documentation.
2. Cross-reference with this matrix to select the correct **Persona**.
3. Load the mandatory rules from `.agent/rules/` JIT.

> [!IMPORTANT]
> All governance definitions reside in `docs/00.agent-governance/`. Technical rule files in `.agent/rules/` are implementation details loaded JIT.

---
*Ref: [agent-instructions.md](../agent-instructions.md), [git-workflow.md](git-workflow.md)*
