# Agent Framework Contract

Shared contract for `hy-home.k8s`. Primary **Explicit Trigger** for AI rules.

## 1. Lazy Loading Protocol (JIT)

Agents MUST NOT load all instructions. Identify **Intent** and load **Scope** from the gateway.

- **Gateway**: [agent-instructions.md](docs/00.agent/agent-instructions.md)
- **Rules**: [persona-matrix.md](docs/00.agent/rules/persona-matrix.md)

## 2. Core Directives

- **English Mandatory**: All internal instructions in `docs/00.agent/` MUST be in English.
- **Spec-First**: Implementation work requires approved artifacts in `docs/01.prd/` and `docs/04.specs/`.
- **Response Mandate**: 요청에 대한 답변은 **한글(Korean)**로 한다.

## 3. Taxonomy (SSoT Paths)

| Layer | Folder | SSoT Path |
| :--- | :--- | :--- |
| **Agent** | 00 | `docs/00.agent/` |
| **Product** | 01 | `docs/01.prd/` |
| **Arch** | 02-03 | `docs/02.ard/`, `docs/03.adr/` |
| **Spec** | 04 | `docs/04.specs/` |
| **Plan/Task** | 05-06 | `docs/05.plans/`, `docs/06.tasks/` |
| **Ops/Inc** | 07-11 | `docs/07~11/` |

---
*Generated 2026-03-25. Follow [bootstrap.md](docs/00.agent/rules/bootstrap.md) for initial context.*
