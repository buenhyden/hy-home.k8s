# GitOps Specifications (`specs/gitops/`)

This directory contains implementation specifications and execution plans for **GitOps** using **ArgoCD** and **Sealed Secrets** on the local k3d cluster.

## Available Specifications

| Document | Feature | Status | Last Updated |
|----------|---------|--------|--------------|
| [spec.md](./spec.md) | ArgoCD + SealedSecrets + App-of-Apps | Draft | 2026-02-27 |
| [plan.md](./plan.md) | GitOps Bootstrap & Rollout Plan | Planned | 2026-02-27 |

## Related Documents (Traceability)

- **PRD**: [docs/prd/gitops/argocd-gitops-prd.md](../../docs/prd/gitops/argocd-gitops-prd.md)
- **ADR**: [docs/adr/gitops/0001-argocd-gitops.md](../../docs/adr/gitops/0001-argocd-gitops.md)
- **ARD**: [docs/ard/gitops/argocd-gitops-architecture.md](../../docs/ard/gitops/argocd-gitops-architecture.md)
