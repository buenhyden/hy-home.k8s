---
layer: "meta"
---
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Claude-specific entrypoint for `hy-home.k8s`. Primary rules are lazily loaded from the gateway. This is a Kubernetes homelab repository for WSL2 using k3d, managed via GitOps, spec-driven development, and AI-assisted automation.

## 1. Repository Overview

**Dual-Purpose**: Kubernetes cluster platform infrastructure (`infrastructure/`, `gitops/`) + documentation-as-code system (`docs/`, `templates/`).

**Critical Rule**: All commands run from the repository root unless otherwise specified.

**Tech Stack**: k3d (k3s), WSL2 (Ubuntu), MetalLB, Ingress-Nginx, ArgoCD, Sealed Secrets.

## 2. Quick Commands

| Purpose | Command |
|---------|---------|
| **Validate changes** | `pre-commit run --all-files` |
| **Create network** | `docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d` |
| **Create cluster** | `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml` |
| **Delete cluster** | `k3d cluster delete hy-k3d` |
| **Check cluster** | `kubectl cluster-info` |

## 3. Instruction Routing

- **Shared Contract**: [AGENTS.md](AGENTS.md)
- **Central Gateway**: [docs/agentic/agent-instructions.md](docs/agentic/agent-instructions.md)
- Full lazy-loading protocol and intent-to-scope mappings documented in `docs/agentic/`.

## 4. Documentation Architecture

All documentation follows a **type-first, flattened hierarchy**:

```
docs/
├── agentic/          # AI governance, rules, scopes (gateway: agent-instructions.md)
├── adr/              # Architectural Decision Records
├── ard/              # Architecture Reference Documents
├── prd/              # Product Requirements
├── specs/            # ← All IMPLEMENTATION SPECS here (plural)
├── plans/            # ← All EXECUTION PLANS here (plural)
├── runbooks/         # ← All PROCEDURES here (plural)
└── operations/       # Incidents, postmortems, strategic docs
```

**Key Rules**:
- Execution documents use **plural paths** (`specs/`, `plans/`, `runbooks/`).
- Every document must include `layer:` metadata (meta, infra, gitops, app, ops).
- All documents must use templates in `templates/`.

## 5. Development Workflow

1. **Spec-First**: All code changes require an approved spec in `docs/specs/` **before** implementation.
2. **Validation Gate**: Run `pre-commit run --all-files` before commit.
3. **GitOps**: Infrastructure changes are deployed via ArgoCD; no manual `kubectl apply`.
4. **Rollback**: Every deployment must document rollback steps in `docs/runbooks/deployment-runbook.md`.

## 6. Skill Autonomy

Claude MUST use any appropriate skill to fulfill requests efficiently and autonomously. Do not wait for permission to use available tools.

## 7. Important References

- **Contributing Model**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Architecture Law**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Operations Index**: [OPERATIONS.md](OPERATIONS.md)
- **Agent Rules**: [AGENTS.md](AGENTS.md)
