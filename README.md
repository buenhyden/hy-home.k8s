# hy-home.k8s

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

> Reproducible local Kubernetes-based home automation and development environment (k3d) on WSL2.

## Overview

This project provides a robust, scalable, and automated Kubernetes environment for running specialized home services and high-performance development workloads. It leverages **k3d** for a lightweight footprint and includes native support for **GPU-accelerated** AI components.

- **Centralized Orchestration**: Managed via k3s on Docker nodes within WSL2.
- **Automated Lifecycle**: Spec-Driven Development (SDD) approach for all infra changes.
- **GPU Ready**: Native pass-through support for NVIDIA hardware.

## Tech Stack

| Category | Technology |
|----------|------------|
| Orchestration | Kubernetes (k3s distribution) |
| Engine | k3d (k3s in Docker) |
| Host Platform | Windows Subsystem for Linux (WSL2) |
| Runtime | NVIDIA Container Runtime |
| Networking | MetalLB (L2 Mode) |

## Prerequisites

List all required tools and versions:

- **WSL2** >= 0.67.6 ( `systemd=true` optional; required only for direct `k3s` installs / Linux-managed services )
- **Docker Desktop** >= 24.x (Integrated with WSL2)
- **k3d CLI** >= 5.x
- **kubectl** (matched to k8s version v1.31.0)
- **NVIDIA Container Toolkit** (Optional, for GPU support)

## Quick Start

### 1. Environment Setup

Optional: If you plan to run Linux-managed services directly inside WSL2 (for example, a direct `k3s` install outside of Docker), enable systemd in WSL:

```bash
# In WSL2
cat /etc/wsl.conf
# Expected output: [boot] systemd=true
```

### 2. Create Cluster

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
```

### 3. Verify Health

```bash
kubectl get nodes
```

## Project Structure

This project follows an AI-Agent-managed, Spec-Driven Development structure:

```text
hy-home.k8s/
├── .agent/             # AI Agent rules, workflows, and prompts
├── .github/            # CI/CD workflows and repository templates
├── infrastructure/     # k3d cluster manifests and base resources (MetalLB, etc.)
├── docs/               # Project documentation (PRD, ADR, ARD, Guides)
├── runbooks/           # Operational, incident, and deployment runbooks
├── scripts/            # Utility and automation scripts
├── specs/              # Implementation Plans, Specs, and API Contracts
├── templates/          # Markdown templates for engineering and product
├── tests/              # Unit and Integration test suites
├── AGENTS.md           # Multi-Agent governance and persona guide
├── ARCHITECTURE.md     # High-level system blueprints and principles
└── README.md           # This file
```

## Extensibility & Documentation

Ensure you read the governance files before contributing or generating code via AI Agents:

- [🤖 Multi-Agent Governance](./AGENTS.md)
- [🏛️ System Architecture](./ARCHITECTURE.md)
- [📝 Specifications & API Contracts](./specs/README.md)
- [📚 Product & Arch Docs](./docs/README.md)
- [⚙️ Operations Baseline](./OPERATIONS.md)

## Contributing

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines on the Spec-Driven development workflow.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
