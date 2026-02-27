# Local Cluster (k3d) GitOps

This directory contains the **local** cluster ArgoCD bootstrap manifests and the GitOps-managed infrastructure/apps layout.

## Bootstrap Overview (Chicken/Egg)

Because the repo is intended to be **private** and ArgoCD repo access is via **SSH deploy key**, the initial bootstrap requires a short manual sequence:

1. Install Sealed Secrets controller (vendored).
2. Install ArgoCD (vendored).
3. Create the ArgoCD repository credential secret **as a SealedSecret** and apply it.
4. Apply `gitops/clusters/local/root-application.yaml` to start reconciliation.

See runbooks in `runbooks/services/` for the exact steps.
