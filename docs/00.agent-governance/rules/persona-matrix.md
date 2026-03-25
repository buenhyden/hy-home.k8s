# Unified Persona & Rule Matrix

This matrix maps AI Agent personas to their target layers and mandatory governance files.

## 1. Core Personas

| Persona | Primary Layer | SSoT Path | Mandatory Rules (JIT) |
| :--- | :--- | :--- | :--- |
| **Product Manager** | Product | `docs/01.prd/` | `rules/bootstrap.md` |
| **System Architect** | Architecture | `docs/02.ard/` | `scopes/architecture.md` |
| **Frontend Engineer** | Frontend | `docs/04.specs/` | `scopes/frontend.md` |
| **Backend Engineer** | Backend | `docs/04.specs/` | `scopes/backend.md` |
| **Infra/DevOps Miner** | Infra | `docs/08.operations/` | `scopes/infra.md` |
| **Security Officer** | Security | `docs/04.specs/` | `scopes/security.md` |
| **QA Engineer** | QA | `docs/05.plans/` | `scopes/qa.md` |

## 2. Rule Discovery Protocol

When an agent is assigned a task:

1. Check the **Layer** metadata in the relevant documentation.
2. Cross-reference with this matrix to select the correct **Persona**.
3. Load the mandatory rules from `docs/00.agent-governance/` JIT.

> [!IMPORTANT]
> All governance definitions and implementation rules reside in `docs/00.agent-governance/`. Technical rules are loaded JIT via the Gateway.

---
*Ref: [agent-instructions.md](../agent-instructions.md), [git-workflow.md](git-workflow.md)*
