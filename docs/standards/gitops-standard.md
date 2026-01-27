# Standard: GitOps Workflow

This project utilizes ArgoCD to implement the GitOps pattern. This standard defines the workflow for promoting changes.

## 🔄 The Sync Cycle

1. **Code Commit**: Developer pushes a change to the `main` branch.
2. **ArgoCD Detection**: The controller detects a difference between the Git state and the Cluster state.
3. **Automatic Sync**:
    - **Prune**: Any resources removed from Git are deleted from the cluster.
    - **Self-Heal**: Any manual changes (drifts) in the cluster are overwritten by the Git state.

---

## 🛠️ Configuration Standards

### 1. No Manual Changes

Changes MUST NOT be made via `kubectl apply` directly in the cluster (with the exception of initial bootstrap). Any manual modification will be reverted by ArgoCD's self-healing.

### 2. Manifest Organization (Kustomize)

All applications MUST use Kustomize for multi-environment management.

- `base/`: Shared, common manifests.
- `overlays/ENV/`: Environment-specific overrides (replicas, image tags, configMaps).

### 3. Application Registration

New applications MUST be registered in the `clusters/` directory under the appropriate cluster name.

- Use the `App-of-Apps` pattern.
- Ensure the `repoURL` and `path` are correct.

---

## 🚀 Deployment Safeguards

- **Health Checks**: All workloads MUST define `livenessProbe` and `readinessProbe`.
- **Canary Rollouts**: Production deployments should use `Argo Rollouts` for progressive delivery instead of basic Kubernetes `Deployments`.
- **Resource Limits**: Every container MUST define CPU and Memory requests and limits.
