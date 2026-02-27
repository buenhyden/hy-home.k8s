---
title: "Core Infrastructure Implementation Spec"
status: "Validated"
version: "1.0"
owner: "hy"
prd_reference: "../../docs/prd/infra/home-cluster-infra-prd.md"
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
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | N/A (Infrastructure) | Section 1         |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes       | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Infra verification cmds | Section 7       |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | N/A (Infra-only)      | Section 7         |
| Coverage Policy | Are goals defined as numbers (e.g. 100%)?      | Must     | N/A (Infra-only)      | Section 7         |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | kubeconfig / RBAC     | Section 4         |
| Data Protection | Encryption/access policies for sensitive data? | Must     | TLS-SAN for localhost | Section 9         |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | kube-apiserver p95    | Section 8         |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A (Infra-only)      | Section 8         |

### 0.3 Operations / Deployment / Monitoring

| Item           | Check Question                                           | Required | Alignment Notes | Where to document |
| -------------- | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments   | Are tiers (dev/staging/prod) clarified for this feature? | Must     | Local Dev / Home Prod | Section 1         |
| Logging        | Required structured logs defined (fields, IDs)?          | Must     | K8s System Logs | Section 9         |
| Monitoring     | Metrics and dashboards defined (RED/USE)?                | Must     | Planned later   | Section 9         |
| Alerts         | Are alert thresholds and routing defined?                | Must     | Planned later   | Section 9         |
| Backups        | Are backup policies defined for added data?              | Must     | N/A (Infra-only) | Section 9        |

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
| **[REQ-INF-003]** | GPU Pass-through enabling (optional) | High     | REQ-PRD-FUN-03 |
| **[REQ-INF-004]** | Windows host access to kube-apiserver (localhost-forwarded) | High     | REQ-PRD-FUN-07 |
| **[REQ-INF-005]** | External IP Pool Mapping (MetalLB) | High     | REQ-PRD-FUN-05 |
| **[REQ-INF-006]** | Dedicated Docker network with fixed CIDR | High     | REQ-PRD-FUN-08 |
| **[REQ-INF-007]** | Ingress controller baseline (ingress-nginx) | High     | REQ-PRD-FUN-09 |
| **[SEC-INF-001]** | TLS-SAN for localhost access | Critical | N/A            |

## 3. Data Modeling & Storage Strategy

- **Storage Class**: Standard `local-path` provisioner.
- **WSL Mapping**: Volumes must target paths within `/home/$USER` in WSL to avoid Windows file system overhead.

## 4. Interfaces & Data Structures

This specification is infrastructure-focused; the “interfaces” are primarily **cluster bootstrap contracts** (configuration files, ports, and expected endpoints).

### 4.1. Core Interfaces

- **k3d Cluster Config**: `infrastructure/k3d/k3d-cluster.yaml`
  - **Cluster Name**: `hy-k3d`
  - **k3s Image**: `rancher/k3s:v1.31.0-k3s1`
  - **Topology**: 1 server + 3 agents
  - **Docker Network**: `k3d-hy-k3d` (dedicated network; fixed CIDR)
  - **Host Port Mappings**:
    - `18080 -> 30080` (ingress-nginx NodePort via k3d load balancer)
    - `18443 -> 30443` (ingress-nginx NodePort via k3d load balancer)
  - **Kubernetes API Exposure**:
    - Host port `6443` exposed for `kubectl` access (WSL + Windows host)
  - **k3s Flags**:
    - `--tls-san=127.0.0.1`
    - `--disable=traefik`
    - `--disable=servicelb`
  - **GPU**: Optional (see GPU variant config below)

- **k3d Cluster Config (GPU Variant)**: `infrastructure/k3d/k3d-cluster.gpu.yaml`
  - **Purpose**: Enables `gpuRequest: all` when the host supports GPU pass-through.
  - **Behavior**: This file MUST NOT be required for a baseline (non-GPU) cluster.

- **MetalLB Installation Manifests (Vendored)**: `infrastructure/metallb/metallb-native.yaml`
  - **Version**: Pinned to a stable release (see `infrastructure/metallb/README.md`)

- **MetalLB Address Pool**: `infrastructure/ipaddresspool.yaml`
  - **Namespace**: `metallb-system`
  - **Mode**: L2 (`L2Advertisement`)
  - **Pool Range (Default)**: `172.20.0.100-172.20.0.150` (must match the dedicated Docker network CIDR)

- **Ingress Controller Manifests (Vendored)**: `infrastructure/ingress-nginx/ingress-nginx.yaml`
  - **Controller**: ingress-nginx
  - **Service**: LoadBalancer (MetalLB assigns an External IP on the dedicated Docker network)

- **Ingress Controller Host Access (NodePort)**: `infrastructure/ingress-nginx/nodeport-service.yaml`
  - **Purpose**: Deterministic localhost access for `curl http://127.0.0.1:18080` without relying on Docker network routing from Windows.
  - **NodePorts**: `30080` (HTTP), `30443` (HTTPS)

- **MetalLB Address Pool**: `infrastructure/ipaddresspool.yaml`
  - **Namespace**: `metallb-system`
  - **Mode**: L2 (`L2Advertisement`)
  - **Pool Range (Default)**: `172.20.0.100-172.20.0.150` (must match the Docker network used by k3d)

### 4.2. AuthN / AuthZ (Required if protected data/actions)

- **Authentication**: kubeconfig client credentials (generated by k3d and written to the default kubeconfig).
- **Authorization**: Kubernetes RBAC (default model).
- **Sensitive Actions**: Cluster-admin operations (e.g., installing controllers, MetalLB) must be done from a controlled admin context.

## 5. Component Breakdown

- **`infrastructure/k3d/k3d-cluster.yaml`**: Main configuration file for the cluster.
- **`infrastructure/k3d/k3d-cluster.gpu.yaml`**: GPU-enabled variant configuration (optional).
- **`infrastructure/k3d/k3d-min.yaml`**: Minimal configuration for low-resource environments.
- **`infrastructure/metallb/metallb-native.yaml`**: Vendored MetalLB native install manifest.
- **`infrastructure/ipaddresspool.yaml`**: MetalLB layer-2 IP range definition.
- **`infrastructure/ingress-nginx/ingress-nginx.yaml`**: Vendored ingress-nginx install manifest.
- **`infrastructure/ingress-nginx/nodeport-service.yaml`**: Host-access NodePort service for ingress-nginx.
- **`infrastructure/namespaces/`**: Workload namespaces (Pod Security Admission labels).
- **`infrastructure/networkpolicies/`**: Baseline NetworkPolicy templates (default-deny + allows).

## 6. Edge Cases & Error Handling

- **GPU Missing / Not Configured**: If the host GPU runtime is not available, the cluster still starts, but GPU workloads cannot schedule. Treat this as a non-fatal configuration gap unless GPU workloads are in-scope for the current deployment.
- **Network / Port Conflicts**: If host ports `18080`, `18443`, or `6443` are already in use, cluster creation fails or exposes inconsistent endpoints. Resolve by freeing ports or updating the k3d config.
- **Ingress Controller Lifecycle Risk**: ingress-nginx upstream retirement (planned around 2026-03) may reduce patch availability. For v1, ingress-nginx is accepted; follow-up work should migrate to an alternative controller if needed.

## 7. Verification Plan (Testing & QA)

- **[VAL-INF-001] Node Check**: `kubectl get nodes` shows 4 nodes and all are `Ready`.
- **[VAL-INF-002] GPU Visibility (Optional)**: `kubectl get nodes -o custom-columns=NAME:.metadata.name,GPUS:.status.allocatable.nvidia\\.com/gpu` shows a GPU value where expected.
- **[VAL-INF-003] Port Access**: Windows host can reach `http://127.0.0.1:18080` and receives an HTTP response (any 2xx–4xx).
- **[VAL-INF-004] MetalLB Health**: `kubectl -n metallb-system get pods` shows all pods running.
- **[VAL-INF-005] Ingress Health**: `kubectl -n ingress-nginx get pods` shows the controller pod(s) ready.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Latency**: API Server response < 10ms.
- **Resource Limits**: Configured via `.wslconfig` (Target: 8GB+ RAM).

## 9. Operations & Observability

- **Deployment**: `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml`.
- **Logging**: Local logs available via `docker logs <container_name>`.
- **Monitoring**: Integration with Prometheus/Loki planned in subsequent specs.
