---
title: "Core Infrastructure Implementation Spec"
status: "Validated"
version: "1.0"
owner: "hy"
prd_reference: "../docs/prd/infra/home-cluster-infra-prd.md"
api_reference: "N/A"
arch_reference: "../../ARCHITECTURE.md"
tags: ["spec", "implementation", "infrastructure", "k3d"]
---

# Implementation Specification: Core Infrastructure

> **Status**: Validated
> **Related PRD**: [Link to PRD](../../docs/prd/infra/home-cluster-infra-prd.md)
> **Related Architecture**: [Link to ARCHITECTURE.md](../../ARCHITECTURE.md)

*Target Directory: `specs/infra/spec.md`*
*Note: This document is the absolute Source of Truth for Coder Agents. NO CODE can be generated without it.*

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes      | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | -------------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Containerized k8s    | Section 1         |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | k3d cluster boundary | Section 1         |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A (Infrastructure) | Section 3         |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | k3s, k3d, Docker     | Section 1         |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes          | Where to document |
| --------------- | ---------------------------------------------- | -------- | ------------------------ | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Node readiness check     | Section 7         |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | kubeconfig / RBAC        | Section 4         |
| Data Protection | Encryption/access policies for sensitive data?     | Must     | TLS-SAN for localhost    | Section 9         |

### 0.3 Operations / Deployment / Monitoring

| Item           | Check Question                                           | Required | Alignment Notes | Where to document |
| -------------- | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments   | Are tiers (dev/staging/prod) clarified for this feature? | Must     | Local Dev / Home Prod | Section 1         |
| Logging        | Required structured logs defined (fields, IDs)?          | Must     | K8s System Logs | Section 9         |

---

## 1. Technical Overview & Architecture Style

This specification details the automation and configuration of the `hy-k3d` Kubernetes cluster on WSL2. The cluster uses k3s (Lightweight Kubernetes) running within Docker containers, managed via the `k3d` CLI.

- **Component Boundary**: Cluster Lifecycle Management (Create, Update, Delete).
- **Key Dependencies**: Docker (WSL2), k3d, NVIDIA Container Toolkit.
- **Tech Stack**: k3d v5.x, Kubernetes v1.31.0.

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **[REQ-INF-001]** | Multi-node setup (1-server, 3-agents) | High     | REQ-PRD-FUN-01 |
| **[REQ-INF-002]** | Host port mapping (18080/18443) | High     | REQ-PRD-FUN-02 |
| **[REQ-INF-003]** | GPU Pass-through enabling | High     | REQ-PRD-FUN-03 |
| **[REQ-INF-004]** | WSL2 Port Forwarding Integration | High     | STORY-04       |
| **[REQ-INF-005]** | External IP Pool Mapping (MetalLB) | High     | REQ-PRD-FUN-05 |
| **[SEC-INF-001]** | TLS-SAN for localhost access | Critical | N/A            |

## 3. Data Modeling & Storage Strategy

- **Storage Class**: Standard `local-path` provisioner.
- **WSL Mapping**: Volumes must target paths within `/home/$USER` in WSL to avoid Windows file system overhead.

## 5. Component Breakdown

- **`infrastructure/k3d/k3d-cluster.yaml`**: Main configuration file for the cluster.
- **`infrastructure/k3d/k3d-min.yaml`**: Minimal configuration for low-resource environments.
- **`infrastructure/ipaddresspool.yaml`**: MetalLB layer-2 IP range definition.

## 6. Edge Cases & Error Handling

- **GPU Missing**: [Condition] -> NVIDIA drivers missing on host -> k3d warns but proceeds with CPU only.
- **Network Conflict**: [Condition] -> Port 18080/18443 in use -> k3d fail to start LB container.

## 7. Verification Plan (Testing & QA)

- **[VAL-INF-001] Node Check**: Verify nodes are `Ready` using `kubectl get nodes`.
- **[VAL-INF-002] GPU Visibility**: Verify GPU visibility in pod using `kubectl exec -it <test-pod> -- nvidia-smi`.
- **[VAL-INF-003] Port Access**: Verify 127.0.0.1:18080 accessibility from Windows host.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Latency**: API Server response < 10ms.
- **Resource Limits**: Configured via `.wslconfig` (Target: 8GB+ RAM).

## 9. Operations & Observability

- **Deployment**: `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml`.
- **Logging**: Local logs available via `docker logs <container_name>`.
- **Monitoring**: Integration with Prometheus/Loki planned in subsequent specs.
