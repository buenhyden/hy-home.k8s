---
layer: "meta"
---
# GEMINI.md

Gemini-specific entrypoint for `hy-home.k8s`. Primary rules are lazily loaded from the gateway.

## 1. Instruction Routing

- **Shared Contract**: [AGENTS.md](AGENTS.md)
- **Central Gateway**: [docs/agentic/agent-instructions.md](docs/agentic/agent-instructions.md)

## 2. Model Constraints

- **Context Awareness**: Maintain k3d/WSL2 context awareness.
- **Metadata Compliance**: Strictly follow `layer:` metadata requirements.
- **Skill Usage**: Proactively use appropriate skills without restriction.
