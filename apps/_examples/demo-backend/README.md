# Demo Backend Example

FastAPI backend application demonstrating GitOps deployment with Argo Rollouts, Istio integration, and PostgreSQL connectivity.

## Features

- **FastAPI**: Modern Python web framework
- **PostgreSQL Connection**: External database integration
- **Health Checks**: Kubernetes-ready `/health` and `/ready` endpoints
- **Prometheus Metrics**: Metrics endpoint for observability
- **Argo Rollouts**: Canary deployment strategy
- **Istio Integration**: Service mesh with mTLS
- **Environment Configuration**: ConfigMap and Secrets support

## Directory Structure

```
demo-backend/
├── README.md (this file)
├── app/                          # Application code
│   ├── main.py                   # FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Container image
│   └── .dockerignore
├── base/                         # Base Kubernetes manifests
│   ├── rollout.yaml              # Argo Rollout
│   ├── service.yaml              # Kubernetes Service
│   ├── virtual-service.yaml      # Istio VirtualService
│   ├── hpa.yaml                  # HorizontalPodAutoscaler
│   ├── pdb.yaml                  # PodDisruptionBudget
│   ├── configmap.yaml            # Configuration
│   └── kustomization.yaml        # Kustomize base
└── overlays/                     # Environment overlays
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

## Application Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check (always returns 200)
- `GET /ready` - Readiness check (checks DB connection)
- `GET /items` - List items from database
- `POST /items` - Create new item
- `GET /items/{item_id}` - Get specific item
- `GET /metrics` - Prometheus metrics

## Quick Start

### 1. Build Docker Image

```bash
cd app
docker build -t demo-backend:v1.0.0 .
```

**Push to registry**:

```bash
# Tag for your registry
docker tag demo-backend:v1.0.0 ghcr.io/yourorg/demo-backend:v1.0.0

# Push
docker push ghcr.io/yourorg/demo-backend:v1.0.0
```

### 2. Update Image in Manifests

Edit `base/rollout.yaml` and set your image:

```yaml
spec:
  template:
    spec:
      containers:
        - name: app
          image: ghcr.io/yourorg/demo-backend:v1.0.0
```

### 3. Deploy to Kubernetes

**Option A**: Via ArgoCD (GitOps)

```bash
# 1. Commit changes
git add apps/_examples/demo-backend
git commit -m "feat: add demo-backend example"
git push

# 2. Create ArgoCD Application
kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo-backend
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/buenhyden/hy-home.k8s.git
    targetRevision: main
    path: apps/_examples/demo-backend/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

**Option B**: Direct kubectl

```bash
kubectl apply -k apps/_examples/demo-backend/overlays/dev
```

### 4. Verify Deployment

```bash
# Watch rollout progress
kubectl argo rollouts get rollout demo-backend -w

# Check pods
kubectl get pods -l app=demo-backend

# Check service
kubectl get svc demo-backend

# View logs
kubectl logs -l app=demo-backend -f
```

### 5. Test Application

```bash
# Port-forward to service
kubectl port-forward svc/demo-backend 8000:8000

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/items
```

## Configuration

### Environment Variables

**Set via ConfigMap** (`base/configmap.yaml`):

- `LOG_LEVEL`: Logging level (default: `info`)
- `ENABLE_DEBUG`: Enable debug mode (default: `false`)

**Set via Secret** (create manually):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: demo-backend-secrets
  namespace: default
stringData:
  DATABASE_URL: "postgresql://postgres:password@postgres-external:15432/demo"
```

Or use Sealed Secrets:

```bash
kubectl create secret generic demo-backend-secrets \
  --from-literal=DATABASE_URL=postgresql://postgres:password@postgres-external:15432/demo \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > base/sealed-secret.yaml
```

### Resource Limits

**Development** (`overlays/dev`):

- CPU: 100m request, 500m limit
- Memory: 128Mi request, 512Mi limit
- Replicas: 2

**Production** (`overlays/prod`):

- CPU: 250m request, 1000m limit
- Memory: 256Mi request, 1Gi limit
- Replicas: 3

## Canary Deployment

The Rollout is configured for progressive canary deployment:

1. **Deploy new version** (20% traffic) → Wait 30s
2. **Increase to 50%** → Wait 30s
3. **Full rollout** (100%)

Monitor canary deployment:

```bash
kubectl argo rollouts get rollout demo-backend --watch
kubectl argo rollouts status demo-backend
```

Promote manually (if paused):

```bash
kubectl argo rollouts promote demo-backend
```

Abort and rollback:

```bash
kubectl argo rollouts abort demo-backend
kubectl argo rollouts undo demo-backend
```

## Istio Integration

### VirtualService

Traffic routing is managed by Istio VirtualService (`base/virtual-service.yaml`).

### mTLS

Application automatically uses mutual TLS for service-to-service communication (Istio sidecar injected).

### Test Traffic Split

During canary, check traffic distribution:

```bash
# Watch logs from both versions
kubectl logs -l app=demo-backend -f --prefix
```

## Monitoring

### Prometheus Metrics

Application exposes metrics at `/metrics`:

- `http_requests_total`: Total HTTP requests (counter)
- `http_request_duration_seconds`: Request duration (histogram)
- `db_connection_active`: Active database connections (gauge)

### Grafana

Import dashboard or create custom queries:

```promql
# Request rate
rate(http_requests_total{app="demo-backend"}[5m])

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{app="demo-backend",status=~"5.."}[5m])
```

### Logs

View logs in Grafana Loki:

```
{app="demo-backend", namespace="default"}
{app="demo-backend"} |= "error"
```

## Database Setup

This example requires PostgreSQL:

1. **Set up PostgreSQL external service** (already configured in `infrastructure/external-services/postgres`)

2. **Create database**:

```bash
# Connect to PostgreSQL
kubectl run psql --image=postgres:15 -it --rm -- \
  psql -h postgres-external -p 15432 -U postgres

# Create database
CREATE DATABASE demo;

# Create table
\c demo
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod -l app=demo-backend
kubectl logs -l app=demo-backend
```

Common issues:

- **ImagePullBackOff**: Check image name and registry access
- **CrashLoopBackOff**: Check logs for application errors
- **Pending**: Insufficient cluster resources

### Database Connection Failed

```bash
# Test connection from pod
kubectl exec -it deployment/demo-backend -- sh
nc -zv postgres-external 15432
```

Verify:

- PostgreSQL service is running
- DATABASE_URL secret is correct
- Network routes are configured

### Rollout Stuck

```bash
# Check rollout status
kubectl argo rollouts status demo-backend

# View detailed information
kubectl argo rollouts get rollout demo-backend

# Check analysis (if configured)
kubectl get analysisrun
```

## Development

### Local Development

```bash
cd app

# Install uv if not installed
# See: https://docs.astral.sh/uv/getting-started/installation/

# Install dependencies and create virtual environment
uv sync

# Set environment variables
export DATABASE_URL=postgresql://postgres:password@localhost:5432/demo
export LOG_LEVEL=debug

# Run application
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format --check .

# Type check
uv run mypy .
```

## Best Practices Demonstrated

1. **Health Checks**: Proper liveness and readiness probes
2. **Resource Limits**: Defined CPU and memory limits
3. **High Availability**: Multiple replicas with PDB
4. **Auto-Scaling**: HPA based on CPU utilization
5. **Progressive Delivery**: Canary deployment with Argo Rollouts
6. **Observability**: Metrics, logs, and tracing integration
7. **Security**: Non-root container, secrets management
8. **GitOps**: Declarative configuration in Git

## Next Steps

- Add automated tests
- Configure custom Canary analysis
- Set up CI/CD pipeline
- Add distributed tracing with OpenTelemetry
- Create custom Grafana dashboard

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Argo Rollouts Canary](https://argoproj.github.io/argo-rollouts/features/canary/)
- [Istio VirtualService](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
