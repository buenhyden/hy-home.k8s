---
layer: "meta"
---
# Core Rules

## Repo Facts

- **Stack**: k3d (local k8s cluster), ArgoCD GitOps, MetalLB, ingress-nginx, Sealed Secrets
- **Source of truth**: `docs/specs/` for planned work; `docs/adr/` for architecture decisions
- **Templates**: flat files under `templates/` — one template per document type
- **Linting**: `pre-commit run --all-files` (no root package manager)

## Verified Commands

### Cluster Bootstrap

```bash
# 1. Network
docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d

# 2. Cluster
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml

# 3. Infrastructure
kubectl apply -f infrastructure/metallb/metallb-native.yaml
kubectl apply -f infrastructure/ipaddresspool.yaml
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml
kubectl apply -f infrastructure/namespaces/
```

### Validation

```bash
pre-commit run --all-files
kubectl get nodes
curl -I http://127.0.0.1:18080/
```

## Guidelines

- `docs/specs/` is the implementation source of truth.
- Use canonical templates in `templates/`.
- Do not fabricate commands, paths, or repo structure.
- Adhere strictly to the **Lazy Loading Protocol**.
- Every doc MUST include `layer:` metadata.
