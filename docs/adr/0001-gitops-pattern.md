# ADR 0001: GitOps-First Cluster Management

## Status

 Accepted

## Context

Standard Kubernetes management often involves imperative commands (`kubectl apply`) or fragile CI/CD pipelines that push changes to the cluster. This leads to configuration drift, difficulty in disaster recovery, and lack of traceability for cluster state changes.

## Decision

We will utilize the **GitOps** pattern as the primary mechanism for all cluster changes.

- **Source of Truth**: All Kubernetes manifests, platform configurations, and application states MUST be committed to Git.
- **Controller**: **ArgoCD** is selected as the GitOps engine.
- **Sync Method**: Automated bi-directional synchronization with `Prune` and `Self-Heal` enabled.

## Consequences

### Positive

- **Traceability**: Every change to the cluster is recorded in the Git history with a corresponding PR.
- **Reproducibility**: The entire cluster can be rebuilt from the bootstrap scripts and this repository.
- **Security**: Reduces the need for broad `kubectl` access among developers; access is managed via Git permissions.

### Negative

- **Latency**: There is a small delay (default ~3m) between pushing code and the cluster syncing.
- **Complexity**: Requires understanding Kustomize/Helm and the App-of-Apps pattern.
- **Strictness**: Manual "hot-fixes" in the cluster will be automatically reverted by the controller.
