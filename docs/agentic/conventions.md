---
layer: "meta"
---
# Coding Conventions & Standards

This document defines the universal coding and documentation standards for the `hy-home.k8s` repository.

## 1. Metadata Compliance

All documentation created or modified MUST include `layer:` metadata in the frontmatter.

- `layer: "meta"`: Governance and root documentation.
- `layer: "infra"`: Host, cluster, and networking.
- `layer: "gitops"`: ArgoCD and Sealed Secrets.
- `layer: "app"`: Application logic and manifests.
- `layer: "ops"`: Runbooks and incident reports.

## 2. Documentation Standards

- **Flattened Hierarchy**: All docs belong in `docs/<type>/`.
- **Plural Paths**: Execution documents reside in plural directories (e.g., `docs/plans/`, `docs/specs/`).
- **Template Driven**: Use `templates/` for all new documents.

## 3. Kubernetes & Infrastructure Patterns

- **k3d/WSL2 Context**: Always assume a local WSL2 environment with k3d.
- **GitOps First**: All infrastructure changes must be declarative and managed via ArgoCD.
- **Secrets Management**: Use Sealed Secrets for all sensitive data.
