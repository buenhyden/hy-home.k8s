---
layer: "meta"
---
# CLAUDE.md

Claude-specific entrypoint for `hy-home.k8s`.

## 1. Instruction Routing

Detailed instructions are lazily loaded from the gateway:

- **Shared Contract**: [AGENTS.md](AGENTS.md)
- **Central Gateway**: [docs/agentic/agent-instructions.md](docs/agentic/agent-instructions.md)

## 2. Environment Context

- **Stack**: k3d, k3s, WSL2, Docker.
- **Workflow**: Spec-first development (`docs/specs/`).
- **Validation**: `pre-commit run --all-files`.

## 3. Skill Autonomy

Claude MUST use any appropriate skill (Cortex or otherwise) to fulfill requests efficiently.
