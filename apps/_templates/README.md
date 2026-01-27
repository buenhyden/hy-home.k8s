# Application Templates

Reusable templates for deploying new applications to the cluster.

## Available Templates

- **[backend/](backend/)**: Template for backend services (REST APIs, microservices)
- **[frontend/](frontend/)**: Template for frontend applications (React, Vue, static sites)

## Quick Start

### 1. Copy Template

```bash
# For a backend service
cp -r apps/_templates/backend apps/my-api

# For a frontend application
cp -r apps/_templates/frontend apps/my-web-app
```

### 2. Customize

Replace placeholders in all YAML files:

| Placeholder | Example |
| ------------- | --------- |
| `APP_NAME` | `user-service` |
| `REGISTRY/IMAGE_NAME:TAG` | `ghcr.io/yourorg/user-service:v1.0.0` |
| `APP_PORT` | `8000` |
| `CPU_REQUEST` / `CPU_LIMIT` | `100m` / `500m` |
| `MEMORY_REQUEST` / `MEMORY_LIMIT` | `128Mi` / `512Mi` |

### 3. Commit to Git

```bash
git add apps/my-api
git commit -m "feat: add my-api application"
git push
```

### 4. Deploy with ArgoCD

Create an ArgoCD Application (or it will auto-sync if using App-of-Apps pattern):

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourorg/your-gitops-repo.git
    targetRevision: main
    path: apps/my-api/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Template Structure

```text
template/
├── base/                    # Base Kubernetes manifests
│   ├── rollout.yaml         # Argo Rollout with Canary strategy
│   ├── service.yaml         # Kubernetes Service
│   ├── virtual-service.yaml # Istio VirtualService
│   ├── hpa.yaml            # HorizontalPodAutoscaler (backend only)
│   ├── pdb.yaml            # PodDisruptionBudget (backend only)
│   └── kustomization.yaml  # Kustomize configuration
└── overlays/               # Environment-specific configurations
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

## Features

- **Canary Deployments**: Progressive rollout with Argo Rollouts
- **Service Mesh**: Istio integration for traffic management and mTLS
- **Auto-Scaling**: HPA based on CPU/memory utilization (backend)
- **High Availability**: PDB ensures minimum replicas during updates
- **Multi-Environment**: Separate dev/prod configurations

## Examples

See [../_examples/](../_examples/) for working reference implementations.

## Documentation

For detailed usage instructions, see [../README.md](../README.md).
