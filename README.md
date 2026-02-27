# hy-home.k8s

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

> Reproducible local Kubernetes-based home automation and development environment (k3d).

## Overview

This project provides a robust, scalable, and automated Kubernetes environment for running home services and development workloads. It leverages k3d for a lightweight footprint and includes support for GPU-accelerated AI experiments.

- **Centralized Orchestration**: Managed via k3s on Docker nodes.
- **Automated Lifecycle**: Spec-driven development and deployment.
- **GPU Ready**: Pass-through support for NVIDIA hardware.

## Tech Stack

| Category | Technology |
|----------|------------|
| Orchestration | Kubernetes (k3s) |
| Engine | k3d (Docker) |
| Configuration | YAML / k3d Manifests |
| Runtime | NVIDIA Container Runtime |

## Prerequisites

- Windows 10/11 with **WSL2** installed.
- Docker Desktop >= 24.x (with WSL2 integration) or Native Docker in WSL.
- k3d CLI >= 5.x.
- NVIDIA Container Toolkit (Optional, for GPU support).

### WSL2 Configuration

Ensure systemd is enabled in `/etc/wsl.conf`:

```ini
[boot]
systemd=true
```

## Project Structure

This project follows an AI-Agent-managed, Spec-Driven Development structure:

```text
hy-home.k8s/
├── .agent/             # AI Agent rules, workflows, and prompts
├── .github/            # CI/CD workflows and repository templates
├── infrastructure/     # k3d cluster manifests and base resources
├── docs/               # Project documentation (PRD, ADR, ARD, Guides, Manuals)
├── runbooks/           # Operational, incident, and deployment runbooks
├── scripts/            # Utility and automation scripts
├── specs/              # Implementation Plans, Specs, and API Contracts
├── templates/          # Markdown templates for engineering and product
├── tests/              # Unit and Integration test suites
├── AGENTS.md           # Multi-Agent governance and persona guide
├── ARCHITECTURE.md     # High-level system blueprints and principles
├── OPERATIONS.md       # Target environment and deployment baseline
├── llms.txt            # System context for prompt construction
├── .env.example        # Environment template
└── README.md           # This file
```

## Quick Start

### 1. Create Cluster

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
```

### 2. Verify Nodes

```bash
kubectl get nodes
```

## Extensibility & Documentation

Ensure you read the governance files before contributing or generating code via AI Agents:

- [🤖 Multi-Agent Governance](./AGENTS.md)
- [🏛️ System Architecture](./ARCHITECTURE.md)
- [⚙️ Operations Baseline](./OPERATIONS.md)
- [📝 Specifications & API Contracts](./specs/README.md)
- [📚 Product & Arch Docs](./docs/README.md)
- [🤝 Contributor Guide](./CONTRIBUTING.md)

## License

This project is licensed under the MIT License.
