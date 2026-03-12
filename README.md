# hy-home.k8s

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

> Reproducible local Kubernetes-based home automation and development environment (k3d) on WSL2.

## Overview

This project provides a robust, scalable, and automated Kubernetes environment for running specialized home services and high-performance development workloads. It leverages **k3d** for a lightweight footprint and includes native support for **GPU-accelerated** AI components.

The system is designed with a **Spec-Driven Development (SDD)** approach, ensuring that all infrastructure and application changes are documented and approved before implementation.

### Key Features

- **Centralized Orchestration**: Managed via k3s on Docker nodes within WSL2.
- **Automated Lifecycle**: GitOps-driven deployment using ArgoCD and Sealed Secrets.
- **GPU Ready**: Native pass-through support for NVIDIA hardware.
- **Deterministic Networking**: Fixed CIDR bridge networks with MetalLB L2 load balancing.
- **Agent-Managed**: Optimized for AI-assisted development and maintenance.

## Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Orchestration** | Kubernetes (k3s distribution) | Container orchestration baseline |
| **Engine** | k3d (k3s in Docker) | Lightweight local cluster engine |
| **Host Platform** | Windows Subsystem for Linux (WSL2) | Primary development environment |
| **Runtime** | Docker Engine (WSL-managed) | Systemd-enabled container runtime |
| **GPU (Optional)** | NVIDIA Container Toolkit / runtime | Hardware acceleration for AI/ML |
| **Networking** | MetalLB (L2 Mode) | Local LoadBalancer provider |
| **Ingress** | ingress-nginx | Layer 7 traffic management |
| **GitOps** | ArgoCD + Sealed Secrets | Automated deployment and secret management |

## Prerequisites

Ensure your host machine meets the following requirements:

- **WSL2** >= 0.67.6 (`systemd=true` is mandatory).
- **Docker Engine** (WSL-managed, systemd-enabled).
- **k3d CLI** >= 5.x.
- **kubectl** (matched to k8s version v1.31.0).
- **NVIDIA Container Toolkit** (Optional, for GPU-accelerated namespaces).

## Quick Start

### 1. Network Initialization

Create a dedicated Docker bridge network with a fixed CIDR for deterministic IP management:

```bash
docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d
```

### 2. Cluster Creation

Provison the cluster using the local k3d configuration:

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
```

### 3. Load Balancer & Ingress Setup

Apply the core networking infrastructure:

```bash
# Install MetalLB
kubectl apply -f infrastructure/metallb/metallb-native.yaml
kubectl apply -f infrastructure/ipaddresspool.yaml

# Install Ingress-Nginx
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml
```

### 4. GitOps Bootstrap (Optional)

If you wish to use GitOps for application management:

```bash
# Install ArgoCD and Sealed Secrets
kubectl apply -f infrastructure/argocd/argocd-install.yaml
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml

# Apply the root application
kubectl apply -f gitops/clusters/local/root-application.yaml
```

## Project Structure

This repository follows a Spec-Driven Development (SDD) layout, segregating hardware-specific infrastructure from high-level application definitions.

```text
hy-home.k8s/
├── .agent/             # AI Agent rules, workflows, and skills
├── .github/            # CI/CD (GitHub Actions) and repo templates
├── gitops/             # ArgoCD application manifests and cluster definitions
├── infrastructure/     # K8s base resources (MetalLB, Ingress, k3d configs)
├── docs/               # Documentation Hub (PRD, ADR, ARD, Specs, Runbooks)
│   ├── adr/            # Architecture Decision Records
│   ├── ard/            # Architecture Reference Documents
│   ├── prd/            # Product Requirements Documents
│   ├── runbooks/       # Executable operational guides and incident recovery
│   └── specs/          # Implementation plans and logic specifications
├── scripts/            # Automation utilities
├── templates/          # Documentation and engineering templates
├── tests/              # E2E and integration testing suites
├── AGENTS.md           # Multi-Agent governance guidelines
├── ARCHITECTURE.md     # High-level system blueprints
└── OPERATIONS.md       # Operational index and readiness baseline
```

## Architecture & Framework

The project is built on three core pillars:

1. **Spec-Driven**: Every change begins in `docs/specs/` to prevent implementation drift.
2. **GitOps-First**: The cluster state is reconciled against the `gitops/` directory.
3. **Isolated Operations**: Runbooks in `docs/runbooks/` provide a "low-stress" path for cluster maintenance.

For deep architectural details, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure the following variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_STAGE` | No | `dev` | Deployment stage (e.g., `dev`, `staging`, `prod`) |

### Cluster Configuration

The k3d cluster is defined in `infrastructure/k3d/k3d-cluster.yaml`. You can customize node counts, image versions, and port mappings there.

## Available Scripts

While most operations are handled via `kubectl` or `k3d`, the following automation scripts are available:

| Script | Purpose |
|--------|---------|
| `scripts/setup-env.sh` | (Placeholder) Automates local WSL2 and Docker prep |
| `scripts/bootstrap-gitops.sh` | (Placeholder) Automates ArgoCD and root app deployment |

## Testing

Verification is critical in the SDD workflow. Run tests to ensure infrastructure components are healthy:

```bash
# Run all infrastructure validation tests
npm run test

# Run specific E2E tests for Ingress connectivity
npm run test:e2e
```

## Troubleshooting

### WSL2 Systemd Issues

If `systemctl` is not available in WSL2:

1. Ensure you are on a recent WSL2 version (`wsl --version`).
2. Add `[boot]\nsystemd=true` to `/etc/wsl.conf` and restart WSL (`wsl --shutdown`).

### MetalLB IP Address Conflicts

If load balancers are stuck in `Pending` state:

1. Verify the Docker network CIDR (`172.20.0.0/16`) matches `infrastructure/ipaddresspool.yaml`.
2. Ensure no other k3d clusters are using the same IP range.

## Extensibility & Documentation

Ensure you read the governance files before contributing or generating code via AI Agents:

- [🤖 Multi-Agent Governance](./AGENTS.md)
- [🏛️ System Architecture](./ARCHITECTURE.md)
- [⚙️ Operations Baseline](./OPERATIONS.md)
- [🤝 Contributor Guide](./CONTRIBUTING.md)
- [📚 Documentation Hub](./docs/README.md)

## Contributing

We follow a strict **Spec-Driven Development** (SDD) workflow. All changes must be preceded by an approved specification in the `specs/` directory.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines on PR gates and code quality standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
