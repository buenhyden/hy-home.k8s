# Command Inventory & Execution Patterns

This document serves as the Single Source of Truth (SSoT) for all standardized commands used within the `hy-home.k8s` project. Agents MUST prioritize these patterns to maintain infrastructure consistency.

## 1. Local Cluster Management (k3d)

### Cluster Lifecycle

```bash
# Create dedicated bridge network (Required for MetalLB stability)
docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d

# Create standard cluster (4 nodes: 1 server, 3 agents)
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml

# Create GPU-enabled cluster
k3d cluster create --config infrastructure/k3d/k3d-cluster.gpu.yaml

# Delete cluster
k3d cluster delete hy-home
```

## 2. Infrastructure Bootstrapping (kubectl)

### Core Networking & LoadBalancing

```bash
# Install MetalLB
kubectl apply -f infrastructure/metallb/metallb-native.yaml
kubectl apply -f infrastructure/ipaddresspool.yaml

# Install Ingress-Nginx
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml
```

### GitOps & Secrets

```bash
# Bootstrap Sealed Secrets
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml

# Bootstrap ArgoCD
kubectl apply -f infrastructure/argocd/argocd-install.yaml

# Apply Root GitOps Application
kubectl apply -f gitops/clusters/local/root-application.yaml
```

## 3. Automation & Testing (Scripts)

### Script Execution Pattern

Agents have the **Creative Mandate** to generate automation scripts in `scripts/` and tests in `tests/`.

- **Standard**: Always use absolute paths or paths relative to the root.
- **Rules**:
  - Must be **Idempotent** (safe to run multiple times).
  - Must include **Error Handling**.
  - Must NOT contain hardcoded secrets (use env vars).

```bash
# Example usage of a maintenance script
bash scripts/cleanup-orphaned-pods.sh
```

---
*Ref: [agent-instructions.md](agent-instructions.md)*
