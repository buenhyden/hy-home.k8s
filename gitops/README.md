# GitOps (ArgoCD) Layout

This directory contains **GitOps-managed** Kubernetes manifests for the local `k3d` cluster, using **ArgoCD (App-of-Apps)**.

## Key Principles (v1)

- ArgoCD access is **port-forward only** (no Ingress/NodePort for ArgoCD itself in v1).
- Secrets are **not committed in plaintext**. Use **Sealed Secrets** for anything that would otherwise be a `Secret`.
- ArgoCD Applications **pin** `targetRevision` to a specific Git revision for reproducibility.

## Structure

- `gitops/clusters/local/`: Local cluster GitOps entrypoint (App-of-Apps).
- `gitops/apps/`: Workload application definitions (introduced in a follow-up spec; mostly empty in v1).
