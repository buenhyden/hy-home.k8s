# Application Templates

This directory contains generic application templates for deploying services to the Kubernetes cluster using GitOps.

## Templates

- **`_templates/backend/`**: Template for backend services (FastAPI, Node.js, etc.)
- **`_templates/frontend/`**: Template for frontend services (React, Vue, etc.)

## Template Structure

Each template follows the Kustomize pattern:

```text
app-template/
├── base/                    # Base Kubernetes manifests
│   ├── rollout.yaml         # Argo Rollout (Canary deployment)
│   ├── service.yaml         # Kubernetes Service
│   ├── virtual-service.yaml # Istio VirtualService
│   ├── hpa.yaml             # HorizontalPodAutoscaler (backend only)
│   ├── pdb.yaml             # PodDisruptionBudget (backend only)
│   └── kustomization.yaml   # Kustomize config
└── overlays/                # Environment-specific overlays
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

## Quick Start

### 1. Copy Template

```bash
# For a new backend service
cp -r _templates/backend apps/my-backend

# For a new frontend service
cp -r _templates/frontend apps/my-frontend
```

### 2. Customize Manifests

Replace the following placeholders in all YAML files:

| Placeholder | Description | Example |
| ------------- | ------------- | --------- |
| `APP_NAME` | Application name | `user-service` |
| `REGISTRY` | Container registry | `ghcr.io/yourorg` |
| `IMAGE_NAME` | Image name | `user-service` |
| `TAG` | Image tag | `v1.0.0` or `latest` |
| `APP_PORT` | Application port | `8000` |
| `REPLICA_COUNT` | Number of replicas | `3` |
| `CPU_REQUEST` | CPU request | `100m` |
| `CPU_LIMIT` | CPU limit | `500m` |
| `MEMORY_REQUEST` | Memory request | `128Mi` |
| `MEMORY_LIMIT` | Memory limit | `512Mi` |
| `MIN_REPLICAS` | HPA min replicas | `2` |
| `MAX_REPLICAS` | HPA max replicas | `10` |

**Backend-specific:**

- `BACKEND_SERVICE_NAME`: Name of backend service for API proxy
- `BACKEND_PORT`: Backend service port

### 3. Update Overlays

Edit `overlays/dev/kustomization.yaml` and `overlays/prod/kustomization.yaml`:

```yaml
bases:
  - ../../base
namePrefix: dev-  # or prod-
commonLabels:
  environment: dev  # or prod
replicas:
  - name: my-backend  # Replace with your APP_NAME
    count: 2
images:
  - name: ghcr.io/yourorg/my-backend  # Replace with your image
    newTag: dev-latest  # or version tag
```

### 4. Create ArgoCD Application

Copy and customize the ArgoCD application template:

```bash
cp clusters/docker-desktop/applications/_app-template.yaml \
   clusters/docker-desktop/applications/my-backend.yaml
```

Edit the new file and replace:

- `APP_NAME`: Your application name
- `YOUR_GIT_REPO_URL`: Your Git repository URL
- `TARGET_NAMESPACE`: Target Kubernetes namespace
- `ENV`: `dev` or `prod`

**Example:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourorg/gitops-repo.git
    targetRevision: main
    path: apps/user-service/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 5. Deploy

```bash
# Commit and push your changes
git add apps/my-backend clusters/docker-desktop/applications/my-backend.yaml
git commit -m "feat: add my-backend application"
git push origin main

# ArgoCD will automatically detect and deploy
```

## Features

### Argo Rollouts Canary Deployment

The templates use Argo Rollouts for progressive delivery:

1. Deploy new version
2. Route 20% traffic → wait 30s
3. Route 50% traffic → wait 30s
4. Route 100% traffic

### Istio Integration

- **mTLS**: Automatic mutual TLS between services
- **Traffic Management**: VirtualService for fine-grained routing
- **Observability**: Auto-instrumented metrics and traces

### Auto-Scaling

Backend template includes HPA:

- Scales based on CPU utilization
- Target: 80% CPU
- Min/Max replicas configurable

### High Availability

- **PodDisruptionBudget**: Ensures at least 1 pod during updates
- **Canary Strategy**: Zero-downtime deployments
- **Resource Limits**: Prevents resource exhaustion

## Environment Variables

### Backend Services

Create a Secret for your app:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-backend-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql://..."
  API_KEY: "your-secret-key"
```

Use SealedSecrets for GitOps:

```bash
kubectl create secret generic my-backend-secrets \
  --from-literal=DATABASE_URL=postgresql://... \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > apps/my-backend/base/sealed-secrets.yaml
```

### Frontend Services

Frontend uses nginx ConfigMap for configuration. Customize `nginx-configmap.yaml`:

```yaml
location /api {
  proxy_pass http://my-backend:8000;
  proxy_set_header Host $host;
}
```

## Examples

See `_examples/` for real working examples:

- `demo-backend/`: FastAPI backend with PostgreSQL connection
- `demo-frontend/`: React frontend with nginx and API proxy

## Troubleshooting

### Image Not Found

Ensure your image is accessible:

```bash
docker pull ghcr.io/yourorg/my-app:v1.0.0
```

### Rollout Stuck

Check rollout status:

```bash
kubectl argo rollouts get rollout my-backend
kubectl argo rollouts abort my-backend
```

### Service Not Accessible

Verify VirtualService:

```bash
kubectl get virtualservice my-backend-vs -o yaml
```

## Next Steps

1. **Image Updates**: Configure Argo Image Updater for automatic image updates
2. **Monitoring**: Add custom Grafana dashboards
3. **Alerts**: Configure Prometheus alerts for your service
4. **Load Testing**: Validate canary deployment with load tests

## References

- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- [Kustomize](https://kustomize.io/)
- [Istio VirtualService](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
