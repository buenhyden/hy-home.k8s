# Home Cluster Infrastructure

This directory contains the core infrastructure configurations for the `hy-home` Kubernetes cluster, implemented using **k3d** (**k3s in Docker**) on **WSL2**.

## Directory Structure

- `k3d/`: Contains k3d cluster configuration manifests.
  - `k3d-cluster.yaml`: Main configuration for the 4-node cluster (1 server, 3 agents) with GPU support.
  - `k3d-min.yaml`: Minimal configuration for low-resource testing.
- `ipaddresspool.yaml`: MetalLB IPAddressPool and L2Advertisement configuration for local LoadBalancer support.

## Prerequisites

- **WSL2**: Version 0.67.6+.
- **Docker Desktop**: Integrated with WSL2.
- **k3d CLI**: Version 5.x+.
- **NVIDIA Container Toolkit**: Required only for GPU pass-through functionality.

> Notes:
> - `systemd=true` in `/etc/wsl.conf` is recommended when you need Linux services managed inside WSL2 (e.g., a direct `k3s` install). For the default **k3d-only** workflow, it is typically not required.

## Usage

### Create Cluster

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
```

### Configure LoadBalancer (MetalLB)

Ensure MetalLB native manifests are applied, then:

```bash
kubectl apply -f infrastructure/ipaddresspool.yaml
```

## Related Documentation

- **PRD**: [docs/prd/infra/home-cluster-infra-prd.md](../docs/prd/infra/home-cluster-infra-prd.md)
- **ADR**: [docs/adr/infra/0001-k3d-local-cluster.md](../docs/adr/infra/0001-k3d-local-cluster.md)
- **ARD**: [docs/ard/infra/k3d-cluster-requirements.md](../docs/ard/infra/k3d-cluster-requirements.md)
- **Spec**: [specs/infra/spec.md](../specs/infra/spec.md)
