---
layer: "meta"
---
# CLAUDE.md

Claude-specific entrypoint for `hy-home.k8s`.

## 1. Instruction Routing

- **Primary Contract**: [AGENTS.md](AGENTS.md)
- **Gateway**: [docs/00.agent/agent-instructions.md](docs/00.agent/agent-instructions.md)

## 2. Quick Commands

- **Validate**: `pre-commit run --all-files`
- **Cluster**: `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml`
- **Details**: See [Core Rules](docs/00.agent/rules/core.md) for verified commands.

## 3. Persona & Style

- Follow [Global Persona](docs/00.agent/rules/global-persona.md).
- Prioritize **Korean** for explanations and summaries.
