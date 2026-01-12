# Application Examples

This directory contains working reference implementations demonstrating GitOps deployment patterns, Kubernetes best practices, and platform features.

## Available Examples

### [demo-backend](demo-backend/)

FastAPI backend application demonstrating:

- **Progressive Delivery**: Argo Rollouts canary deployment (20% → 50% → 100%)
- **Service Mesh**: Istio VirtualService for traffic management
- **Database Integration**: PostgreSQL connection via external service
- **Health Checks**: Kubernetes liveness and readiness probes
- **Auto-Scaling**: HPA based on CPU utilization
- **High Availability**: PodDisruptionBudget ensuring minimum availability
- **Observability**: Prometheus metrics endpoint
- **Security**: Non-root container, resource limits
- **Configuration**: ConfigMap and Secrets management

**Tech Stack**: Python, FastAPI, PostgreSQL, Prometheus

**Quick Start**:

```bash
cd demo-backend/app
docker build -t demo-backend:v1.0.0 .
# See demo-backend/README.md for complete instructions
```

### demo-frontend (Coming Soon)

React frontend example demonstrating:

- nginx configuration
- SPA routing
- API proxy to backend
- Environment variable injection
- Canary deployment

## Purpose

## Creating Your App (Recommended Approach)

1. **Start with templates**: `cp -r apps/_templates/backend apps/my-api`
2. **Replace placeholders**: Change `APP_NAME`, image, ports, resources
3. **Customize overlays**: Configure dev/prod environments
4. **Create ArgoCD App**: Add to `clusters/docker-desktop/applications/`
5. **Deploy**: Commit to Git, let ArgoCD auto-sync

**Full Guide**: [docs/guides/adding-applications.md](../../docs/guides/adding-applications.md)
