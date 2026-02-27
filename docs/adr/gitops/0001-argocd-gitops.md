# Architecture Decision Record (ADR)

*Target Directory: `docs/adr/gitops/0001-argocd-gitops.md`*

## Title: 0001-argocd-gitops

- **Status:** Accepted
- **Date:** 2026-02-27
- **Authors:** hy
- **Deciders:** hy
- **Reviewers:** N/A (Self-reviewed)

## 1. Context and Problem Statement

The local WSL2 + k3d cluster currently relies on manual application of Kubernetes manifests. As the infrastructure footprint grows, manual workflows become non-repeatable and drift-prone.

We need a GitOps controller that:

- Continuously reconciles desired state from Git.
- Supports deterministic rollbacks.
- Prevents plaintext secret commits while still allowing private repository access.

## 2. Decision Drivers

- **Developer Experience**: Clear `Synced/Healthy` feedback and predictable rollbacks.
- **Security**: No plaintext Secret committed; private repo access must be reproducible.
- **Determinism**: Version pins for controller manifests and ArgoCD `targetRevision`.
- **Simplicity**: v1 baseline should minimize exposed surfaces (port-forward only).

## 3. Decision Outcome

**Chosen option: "ArgoCD (App-of-Apps) + Sealed Secrets + SSH deploy key"**, because it provides strong GitOps reconciliation, well-understood workflows for Kubernetes manifests, and a path to securely manage repo credentials without committing plaintext secrets.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Enforces `[BAN-GPT-01]` (no plaintext secrets) by standardizing SealedSecrets for sensitive material.
- **Observability**: ArgoCD provides first-level operational status for GitOps-managed resources (`Synced/Healthy/Degraded`).
- **Compliance**: Keeps infrastructure state changes auditable via Git history.
- **Performance**: Adds minimal overhead for local cluster scale.
- **Documentation**: Establishes runbooks and spec-driven bootstrap to reduce tribal knowledge.
- **Localization**: N/A (infra control plane).

### 3.2 Positive Consequences

- Repeatable cluster convergence from Git.
- Drift detection and automated remediation (`selfHeal=true`).
- Clear rollback path (revert pinned revision or manifest changes).

### 3.3 Negative Consequences

- Bootstrap chicken/egg complexity for private repo credentials.
- `targetRevision` pinning adds update overhead (must bump SHA/tag intentionally).

## 4. Alternatives Considered (Pros and Cons)

### Flux CD

- **Good**, because lightweight and popular for GitOps.
- **Bad**, because the team already has ArgoCD operational patterns and UI-centric workflows; v1 favors rapid local feedback.

### ArgoCD without Sealed Secrets (manual non-Git secret)

- **Good**, because simpler bootstrap.
- **Bad**, because it violates `[BAN-GPT-01]` intent and makes reproducibility dependent on non-versioned steps.

### Expose ArgoCD via Ingress/NodePort

- **Good**, because convenient access.
- **Bad**, because it expands exposed surfaces and requires additional ingress/routing decisions; v1 standard is port-forward.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: Medium
- **Notes**: ArgoCD/SealedSecrets are standard tools, but bootstrap UX depends on clear runbooks and operator discipline.
- **Technical Requirements Addressed**: REQ-PRD-FUN-01, REQ-PRD-FUN-02, REQ-PRD-FUN-03, REQ-PRD-FUN-05

## 6. Related Documents (Traceability)

- **Feature PRD**: [docs/prd/gitops/argocd-gitops-prd.md](../../prd/gitops/argocd-gitops-prd.md)
- **Feature Spec**: [specs/gitops/spec.md](../../../specs/gitops/spec.md)
