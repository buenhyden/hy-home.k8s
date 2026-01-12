# Getting Started with hy-home.k8s GitOps

This guide will help you set up and deploy the GitOps infrastructure from scratch.

## Prerequisites

- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
- **kubectl** - Kubernetes command-line tool
- **Kind** - Kubernetes in Docker
- **Git** - Version control

## Architecture Overview

This GitOps repository manages:

- **Applications**: Your workloads (apps folder)
- **Infrastructure**: Platform services (infrastructure folder)  
- **Cluster Config**: ArgoCD and cluster-specific settings (clusters folder)

## Quick Start (15 minutes)

### Step 1: Clone Repository

```bash
git clone https://github.com/buenhyden/hy-home.k8s.git
cd hy-home.k8s
```

### Step 2: Create Cluster

```bash
cd bootstrap
chmod +x *.sh  # Linux/Mac only
./cluster-setup.sh
```

### Step 3: Configure Hybrid Networking

For external service connectivity (PostgreSQL, Redis in Docker):

```bash
# Get Docker network gateway
GATEWAY=$(docker network inspect infra_net --format "{{(index .IPAM.Config 0).Gateway}}")

# Add routes to Kind nodes
docker exec -it docker-desktop-control-plane ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker2 ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker3 ip route add 172.19.0.0/16 via $GATEWAY
```

### Step 4: Install ArgoCD

```bash
./argocd-install.sh
```

Wait for all ArgoCD pods to be ready (this takes 2-3 minutes).

### Step 5: Deploy Root Applications

```bash
./root-apps.sh
```

This deploys two root applications:

- **apps.yaml**: Manages your application workloads
- **infrastructure.yaml**: Manages platform infrastructure

### Step 6: Access ArgoCD UI

```bash
# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port-forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open https://localhost:8080
# Username: admin
# Password: (from above command)
```

## What Gets Deployed

### Infrastructure Components

1. **Controllers**
   - Istio Service Mesh (v1.24.0)
   - MetalLB LoadBalancer

2. **Observability**
   - Prometheus Stack (v66.7.1)
   - Loki (v6.18.0)
   - Tempo (v1.12.0)
   - Alloy (v0.9.0)
   - Grafana

3. **Security**
   - Kyverno (v3.2.0)
   - Cert-Manager (v1.16.0)
   - Sealed Secrets

4. **Workflow**
   - Apache Airflow (v1.15.0)

5. **External Services**
   - PostgreSQL (Headless Service → Docker)
   - Redis Cluster (Headless Service → Docker)
   - Kafka, OpenSearch (ServiceEntry)

### Deployment Timeline

- Namespaces: ~10 seconds
- Controllers (Istio, MetalLB): ~2 minutes
- Observability stack: ~3 minutes
- Security: ~1 minute
- Applications: ~2 minutes

**Total**: ~8-10 minutes for full deployment

## Monitoring Deployment

```bash
# Watch all applications
kubectl get applications -n argocd -w

# Check specific application
kubectl describe application infrastructure -n argocd

# View pods across all namespaces
kubectl get pods -A
```

## Next Steps

1. **Deploy Your First App**: See [adding-applications.md](adding-applications.md)
2. **Configure Monitoring**: Access Grafana at `https://localhost:3000`
3. **Review Architecture**: See [../architecture/overview.md](../architecture/overview.md)
4. **Troubleshooting**: See [troubleshooting.md](troubleshooting.md)

## Common Issues

### ArgoCD Applications Stuck in "Progressing"

Wait 5-10 minutes. Large Helm charts (Prometheus) take time.

```bash
# Force sync
kubectl patch application infrastructure -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"HEAD"}}}'
```

### Pods CrashLooping

Check logs:

```bash
kubectl logs -n <namespace> <pod-name>
```

Most common: waiting for dependencies (databases, etc.)

### Can't Access External Services

Verify hybrid networking routes:

```bash
docker exec -it docker-desktop-worker ip route
# Should show: 172.19.0.0/16 via 172.18.0.1
```

## Understanding GitOps

- **Git is Source of Truth**: All changes via git commits
- **Auto-Sync**: ArgoCD watches repo, auto-deploys changes
- **Self-Healing**: ArgoCD reverts manual kubectl changes
- **Declarative**: Describe desired state, ArgoCD makes it so

## Learning Resources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Tutorial](https://kustomize.io/)
- [Istio Docs](https://istio.io/latest/docs/)

## Support

- **Issues**: [GitHub Issues](https://github.com/buenhyden/hy-home.k8s/issues)
- **Documentation**: [docs/reference/](../reference/)
