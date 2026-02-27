---
title: "Core Infrastructure Implementation Spec"
status: "Validated"
version: "1.0.0"
owner: "hy"
prd_reference: "../docs/prd/core-infra/home-cluster-infra-prd.md"
api_reference: "N/A"
arch_reference: "../../ARCHITECTURE.md"
tags: ["spec", "implementation", "infrastructure", "k3d"]
---

# Implementation Specification: Core Infrastructure

> **Status**: Validated
> **Related PRD**: [Link to PRD](../../docs/prd/core-infra/home-cluster-infra-prd.md)
> **Related Architecture**: [Link to ARCHITECTURE.md](../../ARCHITECTURE.md)

*Target Directory: `specs/core-infra/spec.md`*

---

## 1. Technical Overview & Architecture Style

This specification details the automation and configuration of the `hy-k3d` Kubernetes cluster. The cluster uses k3s (Lightweight Kubernetes) running within Docker containers, managed via the `k3d` CLI.

- **Component Boundary**: Cluster Lifecycle Management (Create, Update, Delete).
- **Key Dependencies**: Docker (with WSL2 integration), k3d, NVIDIA Container Toolkit.
- **Tech Stack**: k3d v5.x, Kubernetes v1.31.0.

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **[REQ-SPC-001]** | Multi-node setup (1-server, 3-agents) | High     | REQ-PRD-FUN-01 |
| **[REQ-SPC-002]** | Host port mapping (18080/18443) | High     | REQ-PRD-FUN-02 |
| **[REQ-SPC-003]** | GPU Pass-through enabling | High     | REQ-PRD-FUN-03 |
| **[REQ-SPC-004]** | WSL2 Port Forwarding Integration | High     | STORY-04       |
| **[SEC-SPC-001]** | TLS-SAN for localhost access | Critical | N/A            |

## 3. Data Modeling & Storage Strategy

- **Local Path Provisioner**: Default storage class using host-local directories.
- **Persistence Strategy**: Use `hostPath` mappings for critical logs and metrics if needed, otherwise standard PVCs.

## 5. Component Breakdown

- **`infrastructure/k3d/k3d-cluster.yaml`**: Main configuration file for the cluster.
- **`infrastructure/k3d/k3d-min.yaml`**: Minimal configuration for low-resource environments.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Performance / Latency**: Control plane response < 5ms.
- **Scale-out**: Up to 10 agent nodes supported on a single large host.

## 9. Operations & Observability

- **Deployment Strategy**: Re-run `k3d cluster create --config` to apply changes (immutable infrastructure pattern).
- **Logging**: K8s logs forwarded to Loki (once observability stack is spec'd).

## 10. Acceptance Criteria (GWT Format)

**[REQ-CLU-001] Cluster Creation**

- **Given** no existing cluster named `hy-k3d`
- **When** I execute `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml`
- **Then** 4 containers (1 server, 3 agents, 1 LB) are created
- **And** `kubectl get nodes` returns all 4 nodes in `Ready` status
