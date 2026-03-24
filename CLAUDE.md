---
layer: "meta"
---
# CLAUDE.md

Guidance for Claude Code (claude.ai/code) in the `hy-home.k8s` repository.

## 1. Project Context

Kubernetes homelab platform for WSL2 using k3d. Managed via GitOps, spec-driven development, and AI automation.

## 2. Core Commands

| Purpose | Command |
| :--- | :--- |
| **Validate** | `pre-commit run --all-files` |
| **Cluster Setup** | `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml` |
| **Cluster Status** | `kubectl cluster-info` / `kubectl get nodes` |
| **ArgoCD UI** | `kubectl port-forward svc/argocd-server -n argocd 8080:443` |

## 3. Instruction Routing

- **Contract**: [AGENTS.md](AGENTS.md)
- **Gateway**: [docs/00.agent/agent-instructions.md](docs/00.agent/agent-instructions.md)
- **Lazy Loading**: Identify intent → Trigger rule → Load scope.

## 4. Documentation Architecture

Flattened hierarchy in `docs/`:

- `adr/`, `ard/`, `prd/`, `specs/`, `plans/`, `runbooks/`, `operations/`.
- **Constraint**: Use **plural paths** for execution docs.

## 5. Development Workflow

1. **Spec-First**: approved spec in `docs/specs/` before code.
2. **GitOps**: No manual `kubectl apply` for infra; use ArgoCD.
3. **Validation**: Run pre-commit before every commit.

## 6. Important References

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [OPERATIONS.md](OPERATIONS.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
