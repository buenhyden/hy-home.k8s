---
goal: "Establish a robust, reproducible k3d-based Kubernetes environment on WSL2."
version: "1.0"
date_created: "2026-02-27"
last_updated: "2026-02-27"
owner: "hy"
status: "Planned"
tags: ["implementation", "planning", "infrastructure", "k3d"]
stack: "node"
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
  - WSL2 environment preparation (Docker Desktop integration; optional systemd + GPU runtime).
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
  - `[REQ-INF-002]`: Host ports 18080/18443 mapped to cluster LoadBalancer.
  - `[REQ-INF-003]`: GPU pass-through enabled for all nodes (when host supports it).
  - `[REQ-INF-004]`: Kubernetes API reachable from Windows host tooling (`kubectl`) via localhost-forwarded endpoint.
  - `[REQ-INF-005]`: Local LoadBalancer IP allocation via MetalLB IPAddressPool + L2Advertisement.
  - `[SEC-INF-001]`: TLS SAN includes `127.0.0.1` for local API access.
- **Constraints:**
  - Limited to WSL2 version 0.67.6+.
  - Host RAM must be 8GB+.

## 5. Work Breakdown (Tasks & Traceability)

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-INF-001 | Validate WSL2 + Docker Desktop prerequisites | N/A | `[REQ-INF-001]` | `docker info` succeeds in WSL2 |
| TASK-INF-002 | Initialize k3d cluster from config | `infrastructure/k3d/k3d-cluster.yaml` | `[REQ-INF-001]` | 4 nodes in `Ready` state |
| TASK-INF-003 | Verify Windows-host `kubectl` can reach kube-apiserver | `infrastructure/k3d/k3d-cluster.yaml` | `[REQ-INF-004]` | `kubectl version --short` succeeds from Windows |
| TASK-INF-004 | Install MetalLB (native manifests) | N/A | `[REQ-INF-005]` | `kubectl -n metallb-system get pods` all `Running` |
| TASK-INF-005 | Configure MetalLB IPAddressPool + L2Advertisement | `infrastructure/ipaddresspool.yaml` | `[REQ-INF-005]` | `kubectl -n metallb-system get ipaddresspools` shows `first-pool` |

## 6. Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Node | Check cluster node count | `kubectl get nodes --no-headers \| wc -l` | 4 |
| VAL-PLN-002 | GPU | Verify GPU availability (if enabled) | `kubectl get nodes -o yaml \| grep -i nvidia` | Output contains `nvidia` |
| VAL-PLN-003 | Net | Test local port mapping | `code=$(curl -sS -o /dev/null -w \"%{http_code}\" http://127.0.0.1:18080/); test \"$code\" -ge 200 -a \"$code\" -lt 500` | Exit code 0 |

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
