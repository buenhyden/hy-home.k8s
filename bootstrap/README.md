# Bootstrap Scripts

This directory contains scripts to bootstrap a new Kubernetes cluster with GitOps.

## Prerequisites

- Docker Desktop (or Docker Engine)
- kubectl
- Kind (Kubernetes in Docker)

## Quick Start

Execute the bootstrap process in order:

```bash
# 1. Create Kind cluster
./cluster-setup.sh

# 2. Install ArgoCD
./argocd-install.sh

# 3. Deploy root applications
./root-apps.sh
```

## Scripts

### 1. cluster-setup.sh

Creates a Kind cluster with:

- 1 control plane node
- 3 worker nodes
- Hybrid networking setup for external services

### 2. argocd-install.sh

Installs ArgoCD in the cluster:

- Creates argocd namespace
- Deploys ArgoCD manifests
- Exposes initial admin password

### 3. root-apps.sh

Deploys the root App-of-Apps applications:

- Applications root app
- Infrastructure root app

### 4. dev-tools.sh / dev-tools.ps1

Installs local developer tools used by commit-time hooks:

- markdownlint-cli2
- actionlint
- kube-linter
- ruff
- mypy

```bash
./dev-tools.sh
```

```bash
./dev-tools.sh --skip-python
```

```powershell
.\dev-tools.ps1
```

```powershell
.\dev-tools.ps1 -SkipPython
```

## Manual Steps

### Get ArgoCD Admin Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Access ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Visit https://localhost:8080
```

## Network Configuration

After cluster creation, configure hybrid networking:

```bash
# Get Docker network gateway
GATEWAY=$(docker network inspect infra_net --format "{{(index .IPAM.Config 0).Gateway}}")

# Add routes to Kind nodes
docker exec -it docker-desktop-control-plane ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker2 ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker3 ip route add 172.19.0.0/16 via $GATEWAY
```

## Troubleshooting

### Cluster Creation Fails

```bash
# Delete existing cluster
kind delete cluster --name docker-desktop

# Retry
./cluster-setup.sh
```

### ArgoCD Not Accessible

```bash
# Check ArgoCD pods
kubectl get pods -n argocd

# Restart port-forward
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

## Next Steps

After bootstrap:

1. Access ArgoCD UI
2. Monitor application sync status
3. Configure Git repository credentials if needed
4. Deploy your applications
