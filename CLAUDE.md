# CLAUDE.md

Claude entrypoint for `hy-home.k8s`. Optimized for **Tool-Use** and **Greedy Autonomy**.

## 1. Governance Gateway

- **Primary**: [agent-instructions.md](docs/00.agent-governance/agent-instructions.md)
- **Rules & Scopes**: [persona-matrix.md](docs/00.agent-governance/rules/persona-matrix.md)
- **Provider Settings**: [claude-provider.md](docs/00.agent-governance/claude-provider.md)

## 2. Operational Mandate

- **Response**: Always respond in **Korean (한국어)**.
- **Internal**: Use English for technical governance.
- **Lazy Loading**: DO NOT read all docs; use JIT loading via `bootstrap.md`.

---
*Ref: [AGENTS.md](AGENTS.md)*
