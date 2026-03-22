---
layer: "meta"
---
# GEMINI.md

Gemini-specific entrypoint for `hy-home.k8s`. Optimized for Google Gemini agents.

## 1. Instruction Routing

- **Shared Contract**: [AGENTS.md](AGENTS.md)
- **Gateway**: [docs/agentic/agent-instructions.md](docs/agentic/agent-instructions.md)

## 2. Model Constraints & Context

- **WSL2/k3d Awareness**: Always operationalize commands for a WSL2/k3d environment.
- **Metadata Compliance**: Strictly enforce `layer:` frontmatter in all documentation.
- **Skill Usage**: Proactively use high-level skills (e.g., `writing-plans`, `producing-docs`) without prompts.
- **Korean Responses**: Unless specified otherwise, provide summaries and explanations in Korean.
