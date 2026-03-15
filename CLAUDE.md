---
layer: "meta"
---
# CLAUDE.md

Claude-specific entrypoint for `hy-home.k8s`. Primary rules are lazily loaded from the gateway.

## 1. Instruction Routing

- **Shared Contract**: [AGENTS.md](AGENTS.md)
- **Central Gateway**: [docs/agentic/agent-instructions.md](docs/agentic/agent-instructions.md)

## 2. Model Constraints

- **Stack Context**: k3d, k3s, WSL2, Docker.
- **Workflow**: Spec-first development via `docs/specs/`.
- **Validation**: Strict adherence to `pre-commit` and coverage gates.

## 3. Skill Autonomy

Claude MUST use any appropriate skill to fulfill requests efficiently and autonomously.
