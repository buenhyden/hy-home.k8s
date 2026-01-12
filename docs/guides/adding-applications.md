# Adding Applications to hy-home.k8s

Guide for deploying new applications using GitOps.

## Overview

Applications are deployed using:

- **Kustomize**: Base + overlays pattern
- **Argo Rollouts**: Progressive delivery (canary)
- **ArgoCD**: GitOps automation

Deployment flow: `Git Push` → `ArgoCD Sync` → `Argo Rollout` → `Application Running`

## Prerequisites

- Cluster running with ArgoCD installed
- Git repository access
- Basic Kubernetes knowledge

## Quick Start

### 1. Copy Template

```bash
# For backend API
cp -r apps/_templates/backend apps/my-api

# For frontend
cp -r apps/_templates/frontend apps/my-web-app
```

### 2. Customize Base Manifests

Edit `apps/my-api/base/rollout.yaml`:

```yaml
metadata:
  name: my-api  # Change APP_NAME
spec:
  replicas: 3  # Change REPLICA_COUNT
  template:
    spec:
      containers:
        - name: app
          image: ghcr.io/yourorg/my-api:v1.0.0  # Change image
          ports:
            - containerPort: 8000  # Change APP_PORT
```

**All placeholders to replace:**

- `APP_NAME`
- `REGISTRY/IMAGE_NAME:TAG`
- `APP_PORT`
- `CPU_REQUEST`, `CPU_LIMIT`
- `MEMORY_REQUEST`, `MEMORY_LIMIT`

### 3. Configure Overlays

Edit `apps/my-api/overlays/dev/kustomization.yaml`:

```yaml
bases:
  - ../../base
replicas:
  - name: my-api  # Match your app name
    count: 2
images:
  - name: ghcr.io/yourorg/my-api
    newTag: dev-latest
```

### 4. Create ArgoCD Application

**Option A: Add to apps.yaml (Recommended)**

Edit `clusters/docker-desktop/apps.yaml` to automatically sync:

```yaml
spec:
  source:
    path: clusters/docker-desktop/applications
```

Then create `clusters/docker-desktop/applications/my-api.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/buenhyden/hy-home.k8s.git
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

**Option B: Manual kubectl**

```bash
kubectl apply -f clusters/docker-desktop/applications/my-api.yaml
```

### 5. Deploy

```bash
git add apps/my-api clusters/docker-desktop/applications/my-api.yaml
git commit -m "feat: add my-api application"
git push origin main
```

ArgoCD will auto-sync within 3 minutes.

## Configuration Details

### Environment Variables

Create a Secret for your application:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-api-secrets
  namespace: default
stringData:
  DATABASE_URL: "postgresql://user:pass@postgres-external:15432/mydb"
  API_KEY: "your-api-key-here"
```

**Using Sealed Secrets (Recommended for GitOps):**

```bash
# Create secret
kubectl create secret generic my-api-secrets \
  --from-literal=DATABASE_URL=postgresql://... \
  --dry-run=client -o yaml > my-api-secret.yaml

# Encrypt with kubeseal
kubeseal < my-api-secret.yaml > apps/my-api/base/sealed-secrets.yaml

# Add to kustomization
echo "  - sealed-secrets.yaml" >> apps/my-api/base/kustomization.yaml
```

### Resource Limits

Set appropriate limits based on your app:

```yaml
resources:
  requests:
    cpu: 100m      # Guaranteed
    memory: 128Mi
  limits:
    cpu: 500m      # Maximum
    memory: 512Mi
```

**Guidelines:**

- **Small API**: 100m CPU, 128Mi memory
- **Medium API**: 250m CPU, 256Mi memory
- **Large API**: 500m CPU, 512Mi memory

### Auto-Scaling (HPA)

Backend template includes HPA:

```yaml
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          averageUtilization: 80
```

### Canary Deployment Configuration

Customize rollout strategy in `rollout.yaml`:

```yaml
strategy:
  canary:
    steps:
      - setWeight: 20    # 20% traffic to new version
      - pause: {duration: 30s}
      - setWeight: 50    # 50% traffic
      - pause: {duration: 30s}
      # Automatically proceeds to 100%
```

**Advanced:** Add manual approval

```yaml
steps:
  - setWeight: 20
  - pause: {}  # Manual approval required
```

## Istio Configuration

### VirtualService

Defines routing rules:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-api-vs
spec:
  hosts:
    - my-api
  http:
    - name: primary
      route:
        - destination:
            host: my-api
```

### Exposing Externally

Add Gateway route (edit infrastructure Istio):

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: my-gateway
  namespace: istio-system
spec:
  selector:
    istio: gateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "*"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-api-external
  namespace: default
spec:
  hosts:
    - "api.example.com"
  gateways:
    - istio-system/my-gateway
  http:
    - match:
        - uri:
            prefix: /v1
      route:
        - destination:
            host: my-api
```

## Monitoring Deployment

### ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Visit https://localhost:8080
```

### CLI Monitoring

```bash
# Watch ArgoCD application
kubectl get application my-api -n argocd -w

# Watch rollout progress
kubectl argo rollouts get rollout my-api -n default -w

# Check pods
kubectl get pods -n default -l app=my-api
```

### Rollout Dashboard

```bash
kubectl argo rollouts dashboard
# Visit http://localhost:3100
```

## Troubleshooting

### Application Not Syncing

```bash
# Check application status
kubectl describe application my-api -n argocd

# Manual sync
kubectl patch application my-api -n argocd \
  --type merge -p '{"operation":{"sync":{"revision":"HEAD"}}}'
```

### Image Pull Errors

Verify image exists:

```bash
docker pull ghcr.io/yourorg/my-api:v1.0.0
```

Add image pull secret if private:

```yaml
spec:
  imagePullSecrets:
    - name: ghcr-secret
```

### Rollout Stuck

```bash
# Check rollout status
kubectl argo rollouts status my-api

# Abort and rollback
kubectl argo rollouts abort my-api
kubectl argo rollouts undo my-api
```

### Pod Won't Start

```bash
# Check events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name> -n default

# Check with Istio sidecar
kubectl logs <pod-name> -c app
kubectl logs <pod-name> -c istio-proxy
```

## Multi-Environment Deployment

### Dev Environment

```bash
# Deploy to dev
kubectl apply -f clusters/docker-desktop/applications/my-api-dev.yaml
```

App definition:

```yaml
spec:
  source:
    path: apps/my-api/overlays/dev
```

### Prod Environment

```bash
# Deploy to prod
kubectl apply -f clusters/docker-desktop/applications/my-api-prod.yaml
```

App definition:

```yaml
spec:
  source:
    path: apps/my-api/overlays/prod
```

## Best Practices

1. **Always use specific image tags** - Never `:latest` in prod
2. **Set resource limits** - Prevent resource exhaustion
3. **Use Sealed Secrets** - Never commit plain secrets
4. **Test in dev first** - Validate before prod
5. **Monitor rollouts** - Watch canary deployments
6. **Enable HPA** - Auto-scale based on load
7. **Use PDB** - Maintain availability during updates

## Examples

See working examples in `apps/_examples/`:

- `demo-backend/` - FastAPI backend with PostgreSQL connection
- `demo-frontend/` - React frontend with nginx and API proxy

## Next Steps

- [Monitoring Guide](../architecture/overview.md#monitoring--alerting)
- [Troubleshooting](troubleshooting.md)
- [Credentials Management](credentials.md)
