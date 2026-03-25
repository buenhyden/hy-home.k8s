# GEMINI.md

Gemini entrypoint for `hy-home.k8s`. Optimized for **Long-Context Discovery**.

## 1. Governance Gateway

- **Primary**: [agent-instructions.md](docs/00.agent-governance/agent-instructions.md)
- **Rules & Scopes**: [persona-matrix.md](docs/00.agent-governance/rules/persona-matrix.md)
- **Provider Settings**: [gemini-provider.md](docs/00.agent-governance/gemini-provider.md)

## 2. Strategy

- **Response**: Always respond in **Korean (한국어)**.
- **Search**: Use hierarchical discovery.
- **Lazy Loading**: Load context JIT via `agent-instructions.md`.

---
*Ref: [AGENTS.md](AGENTS.md)*
