# Agent Framework Contract

Shared contract for `hy-home.k8s`. Primary **Explicit Trigger** for AI rules.

## 1. Lazy Loading Protocol (JIT)

Agents MUST NOT load all instructions. Identify **Intent** and load **Scope** from the gateway.

- **Gateway**: [agent-instructions.md](docs/00.agent-governance/agent-instructions.md)
- **Rules**: [persona-matrix.md](docs/00.agent-governance/rules/persona-matrix.md)

## 2. Core Directives

- **English Mandatory**: All internal instructions in `docs/00.agent-governance/` MUST be in English.
- **Spec-First**: Implementation work requires approved artifacts in `docs/01.prd/` and `docs/04.specs/`.
- **Response Mandate**: 요청에 대한 답변은 항상 **한글(Korean)**로 한다.

---
*Generated: 2026-03-25. Context: [bootstrap.md](docs/00.agent-governance/rules/bootstrap.md)*
