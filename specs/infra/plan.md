---
goal: "Establish a robust, reproducible k3d-based Kubernetes environment on WSL2."
version: "1.0"
date_created: "2026-02-27"
last_updated: "2026-02-27"
owner: "hy"
status: "Planned"
tags: ["implementation", "planning", "infrastructure", "k3d"]
stack: "kubernetes"
---

# Core Infrastructure Implementation Plan

*Target Directory: `specs/infra/plan.md`*

## 1. Context & Introduction

The `hy-home` project requires a centralized orchestration layer for home automation and development services. This plan details the deployment of a k3d-managed Kubernetes cluster on WSL2, providing GPU support and local load balancing.

## 2. Goals & In-Scope

- **Goals:**
  - Standardize Kubernetes environment setup across WSL2 instances.
  - Enable GPU pass-through for AI workloads.
  - Implement local LoadBalancer support via MetalLB.
- **In-Scope:**
  - WSL2 environment preparation (systemd, NVIDIA Toolkit).
  - k3d cluster creation using YAML manifests.
  - MetalLB native installation and configuration.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Configuring individual application workloads (handled in separate plans).
- **Out-of-Scope:**
  - Public cloud provisioning.
  - External DNS resolution.

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-INF-001]`: 4-node cluster (1 server, 3 agents).
  - `[REQ-INF-002]`: Host ports 18080/18443 mapped to LB.
  - `[REQ-INF-003]`: GPU accessibility in all agent nodes.
- **Constraints:**
  - Limited to WSL2 version 0.67.6+.
  - Host RAM must be 8GB+.

## 5. Work Breakdown (Tasks & Traceability)

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-INF-001 | Prepare WSL2 config (`systemd=true`) | `/etc/wsl.conf` | `[REQ-INF-001]` | `systemctl is-system-running` |
| TASK-INF-002 | Initialize k3d cluster | `infrastructure/k3d/k3d-cluster.yaml` | `[REQ-INF-001]` | 4 nodes in `Ready` state |
| TASK-INF-003 | Install MetalLB Native | N/A | `[REQ-INF-005]` | MetalLB pods running |
| TASK-INF-004 | Configure IP Address Pool | `infrastructure/ipaddresspool.yaml` | `[REQ-INF-005]` | IP pool status is `Ready` |

## 6. Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Node | Check cluster node count | `kubectl get nodes --no-headers \| wc -l` | 4 |
| VAL-PLN-002 | GPU | Verify NVIDIA devices in pod | `kubectl run -it test --image=nvidia/cuda -- nvidia-smi` | GPU detected |
| VAL-PLN-003 | Net | Test local port mapping | `curl -k https://127.0.0.1:18443` | 404 (Traefik) or 200 |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| WSL2 Resource Pressure | High | Monitor host memory/CPU; adjust `.wslconfig`. |
| Port Conflict | Med | Verify no other services use 18080/18443. |

## 8. Completion Criteria

- [ ] All nodes report `Ready` status.
- [ ] MetalLB is successfully assigning IPs from the specified range.
- [ ] GPU-enabled pods can access host hardware.

## 9. References

- **PRD**: `docs/prd/infra/home-cluster-infra-prd.md`
- **Spec**: `specs/infra/spec.md`
- **ADRs**: `docs/adr/infra/0001-k3d-local-cluster.md`
