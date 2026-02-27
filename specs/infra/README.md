# Infrastructure Specifications (`specs/infra/`)

This directory contains implementation specifications and execution plans for the core cluster infrastructure.

## Available Specifications

| Document | Feature | Status | Last Updated |
|----------|---------|--------|--------------|
| [spec.md](./spec.md) | k3d Cluster Configuration | Validated | 2026-02-27 |
| [plan.md](./plan.md) | Cluster Deployment Roadmap | Planned | 2026-02-27 |

## Purpose

These files define the exact k3d (**k3s-in-Docker**) and MetalLB configurations required to achieve a stable WSL2-based Kubernetes environment. Where this repository mentions “k3s”, it refers to the Kubernetes distribution used by k3d, not a separate direct-install path unless explicitly stated.

They translate [Architecture Requirements](../../docs/ard/infra/k3d-cluster-requirements.md) into concrete execution steps.
