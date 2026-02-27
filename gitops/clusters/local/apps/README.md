# App-of-Apps Children (Local Cluster)

This directory contains ArgoCD `Application` manifests that each point to a Kustomize directory under `gitops/clusters/local/`.

The parent `gitops/clusters/local/root-application.yaml` uses `directory.recurse: true` to discover and apply all manifests in this directory.
