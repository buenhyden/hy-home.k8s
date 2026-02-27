# Home Cluster Infrastructure

This directory contains the core infrastructure configurations for the `hy-home` Kubernetes cluster, implemented using **k3d** (**k3s in Docker**) on **WSL2**.

## Directory Structure

- `k3d/`: Contains k3d cluster configuration manifests.
  - `k3d-cluster.yaml`: Main configuration for the 4-node cluster (1 server, 3 agents).
  - `k3d-cluster.gpu.yaml`: GPU-enabled variant (optional; requires host GPU runtime support).
  - `k3d-min.yaml`: Minimal configuration for low-resource testing.
- `argocd/`: Vendored ArgoCD install manifest (pinned) for local GitOps bootstrap.
- `sealed-secrets/`: Vendored Sealed Secrets controller manifest (pinned) for sealed secret workflows.
- `metallb/`: Vendored MetalLB native manifests (pinned).
- `ingress-nginx/`: Vendored ingress-nginx manifests (pinned) + deterministic NodePort service for localhost access.
- `namespaces/`: Workload namespaces with Pod Security Admission labels.
- `networkpolicies/`: Baseline NetworkPolicy templates (default-deny + required allows).
- `ipaddresspool.yaml`: MetalLB IPAddressPool and L2Advertisement configuration for local LoadBalancer support (dedicated Docker network).

## Prerequisites

- **WSL2**: Version 0.67.6+.
- **Docker Engine (WSL-managed)**: Docker daemon runs inside WSL2 (systemd-managed for the default v1 workflow).
- **k3d CLI**: Version 5.x+.
- **kubectl**: Matched to Kubernetes v1.31.0 (or newer client compatible with v1.31).
- **NVIDIA Container Toolkit**: Required only for GPU pass-through functionality.

> Notes:
>
> - For the v1 standard, `systemd=true` is required to run Docker Engine as a service inside WSL2. See the runbook in `runbooks/services/` for the exact setup steps.

## Usage

### Create Dedicated Docker Network (Fixed CIDR)

MetalLB stability depends on a fixed Docker network CIDR. Create the network **before** creating the cluster:

```bash
docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d
```

### Create Cluster

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
```

Optional (GPU-enabled):

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.gpu.yaml
```

### Configure LoadBalancer (MetalLB)

Install MetalLB from vendored manifests, then apply the local IP pool:

```bash
kubectl apply -f infrastructure/metallb/metallb-native.yaml
kubectl apply -f infrastructure/ipaddresspool.yaml
```

### Install Ingress (ingress-nginx)

```bash
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml
```

### Baseline Security (Minimum)

Apply workload namespaces with Pod Security Admission labels:

```bash
kubectl apply -f infrastructure/namespaces/
```

NetworkPolicy templates are provided in `infrastructure/networkpolicies/` (apply selectively per namespace/workload).

## GitOps (ArgoCD) (Optional)

v1 supports GitOps using ArgoCD + Sealed Secrets. The bootstrap sequence is intentionally short and deterministic:

```bash
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml
kubectl apply -f infrastructure/argocd/argocd-install.yaml
```

Then apply your **sealed** ArgoCD repository credential and the root Application:

```bash
kubectl apply -f gitops/clusters/local/root-application.yaml
```

See the runbooks under `runbooks/services/` for the full workflow (including `kubeseal` usage).

## Related Documentation

- **PRD**: [docs/prd/infra/home-cluster-infra-prd.md](../docs/prd/infra/home-cluster-infra-prd.md)
- **ADR**: [docs/adr/infra/0001-k3d-local-cluster.md](../docs/adr/infra/0001-k3d-local-cluster.md)
- **ARD**: [docs/ard/infra/k3d-cluster-requirements.md](../docs/ard/infra/k3d-cluster-requirements.md)
- **Spec**: [specs/infra/spec.md](../specs/infra/spec.md)
- **GitOps PRD**: [docs/prd/gitops/argocd-gitops-prd.md](../docs/prd/gitops/argocd-gitops-prd.md)
- **GitOps Spec**: [specs/gitops/spec.md](../specs/gitops/spec.md)
