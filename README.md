---
layer: "meta"
---
# hy-home.k8s

![Kubernetes](https://img.shields.io/badge/kubernetes-v1.31.0-blue.svg)
![k3d](https://img.shields.io/badge/k3d-v5.x-orange.svg)
![WSL2](https://img.shields.io/badge/platform-WSL2-informational.svg)

> Operator-first local Kubernetes platform for WSL2, built around k3d, deterministic networking, and GitOps-driven automation.

## Overview

`hy-home.k8s` is a professional-grade homelab repository for running Reproducible multi-node k3s clusters inside Docker on WSL2. It leverages **GitOps** for state reconciliation and **Spec-Driven Development** for platform evolution.

## Key Features

- **Standardized Topology**: 1 server + 3 agents via k3d.
- **Deterministic Networking**: Fixed subnets and MetalLB address pools.
- **GitOps-First**: ArgoCD and Sealed Secrets integrated by default.
- **Agentic Automation**: AI-assisted development driven by `docs/agentic/`.

## Tech Stack

| Category | Technology | Purpose |
| --- | --- | --- |
| **Cluster** | k3d (k3s) | Container-based local K8s |
| **OS** | WSL2 (Ubuntu) | High-performance Linux host |
| **Ingress** | ingress-nginx | Layer 7 traffic routing |
| **LB** | MetalLB | L2/L3 LoadBalancer |
| **GitOps** | ArgoCD | Manifest reconciliation |
| **Secrets** | Sealed Secrets | Encrypted git-safe secrets |

## Project Structure

Documentation is organized in a flat, type-first hierarchy.

```text
hy-home.k8s/
├── AGENTS.md               # AI Agent entrypoint & Rule triggers
├── ARCHITECTURE.md         # Global architectural constraints
├── CONTRIBUTING.md         # Spec-first contribution model
├── OPERATIONS.md           # Operational index and policies
├── README.md               # Standard landing page
├── docs/
│   ├── adr/                # Architectural Decision Records
│   ├── ard/                # Architecture Reference Documents
│   ├── prd/                # Product Requirements Documents
│   ├── specs/              # Technical Specifications (Flattened)
│   ├── plans/              # Execution Implementation Plans
│   ├── runbooks/           # Executable Runbooks (Flattened)
│   └── operations/         # Strategic Ops (Incidents/Postmortems)
├── templates/              # Canonical Markdown templates
└── infrastructure/         # Platform manifests
```

## Quick Start

### 1. Networking

```bash
docker network create --driver bridge --subnet 172.20.0.0/16 k3d-hy-k3d
```

### 2. Cluster Creation

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
```

### 3. Bootstrap Baseline

```bash
kubectl apply -f infrastructure/metallb/metallb-native.yaml
kubectl apply -f infrastructure/ipaddresspool.yaml
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml
```

## Governance & Collaboration

This repository is designed for Human-AI collaboration.

- See **[AGENTS.md](AGENTS.md)** for AI Agent rules and entrypoints.
- See **[COLLABORATING.md](COLLABORATING.md)** for human-managed handoff rules.
- See **[CONTRIBUTING.md](CONTRIBUTING.md)** for PR quality gates.

## License

This project is currently private/unlicensed.
