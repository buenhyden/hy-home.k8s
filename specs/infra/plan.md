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
  - Provide deterministic localhost access for ingress verification (`127.0.0.1:18080/18443`).
  - Enable GPU pass-through for AI workloads (optional).
  - Implement local LoadBalancer support via MetalLB on a dedicated Docker network.
- **In-Scope:**
  - WSL2 environment preparation (WSL-managed Docker Engine; systemd required for the default v1 workflow).
  - Dedicated Docker network creation with fixed CIDR (MetalLB stability baseline).
  - k3d cluster creation using YAML manifests (k3d-only standard).
  - MetalLB native installation (vendored) and IP pool configuration.
  - ingress-nginx installation (vendored) plus NodePort-based host access.
  - Baseline security scaffolding (workload namespaces + PSA labels; NetworkPolicy templates).

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Configuring individual application workloads (handled in separate plans).
- **Out-of-Scope:**
  - Public cloud provisioning.
  - External DNS resolution.

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-INF-001]`: 4-node cluster (1 server, 3 agents).
  - `[REQ-INF-002]`: Host ports 18080/18443 provide HTTP/HTTPS access to the ingress controller (no connection failures).
  - `[REQ-INF-003]`: GPU pass-through supported (optional; baseline cluster must run without GPU).
  - `[REQ-INF-004]`: Kubernetes API reachable from Windows host tooling (`kubectl`) via localhost-forwarded endpoint.
  - `[REQ-INF-005]`: Local LoadBalancer IP allocation via MetalLB IPAddressPool + L2Advertisement (dedicated Docker network CIDR).
  - `[REQ-INF-006]`: Dedicated Docker network exists (fixed CIDR; documented default).
  - `[REQ-INF-007]`: ingress-nginx installed from vendored manifests.
  - `[SEC-INF-002]`: Workload namespaces include Pod Security Admission labels (`restricted`).
  - `[SEC-INF-003]`: Provide baseline NetworkPolicy templates (default-deny + required allows).
  - `[SEC-INF-001]`: TLS SAN includes `127.0.0.1` for local API access.
- **Constraints:**
  - Limited to WSL2 version 0.67.6+.
  - Host RAM must be 8GB+.

## 5. Work Breakdown (Tasks & Traceability)

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-INF-001 | Validate WSL2 + Docker Engine prerequisites | N/A | `[REQ-INF-001]` | `docker info` succeeds in WSL2 |
| TASK-INF-002 | Create dedicated Docker network | N/A | `[REQ-INF-006]` | `docker network inspect k3d-hy-k3d` shows expected subnet |
| TASK-INF-003 | Initialize k3d cluster from config | `infrastructure/k3d/k3d-cluster.yaml` | `[REQ-INF-001]` | 4 nodes in `Ready` state |
| TASK-INF-004 | Verify Windows-host `kubectl` can reach kube-apiserver | `infrastructure/k3d/k3d-cluster.yaml` | `[REQ-INF-004]` | `kubectl version -o yaml` succeeds from Windows (or `--short` if supported) |
| TASK-INF-005 | Install MetalLB (vendored native manifests) | `infrastructure/metallb/metallb-native.yaml` | `[REQ-INF-005]` | `kubectl -n metallb-system get pods` all `Running` |
| TASK-INF-006 | Configure MetalLB IPAddressPool + L2Advertisement | `infrastructure/ipaddresspool.yaml` | `[REQ-INF-005]` | `kubectl -n metallb-system get ipaddresspools` shows `first-pool` |
| TASK-INF-007 | Install ingress-nginx (vendored manifests) | `infrastructure/ingress-nginx/ingress-nginx.yaml` | `[REQ-INF-007]` | `kubectl -n ingress-nginx get pods` controller ready |
| TASK-INF-008 | Add deterministic NodePort host access | `infrastructure/ingress-nginx/nodeport-service.yaml`, `infrastructure/k3d/k3d-cluster.yaml` | `[REQ-INF-002]` | `curl -I http://127.0.0.1:18080` returns HTTP (2xx–4xx) |
| TASK-INF-009 | Apply workload namespaces + PSA labels | `infrastructure/namespaces/*` | `[SEC-INF-002]` | `kubectl get ns -L pod-security.kubernetes.io/enforce` shows `restricted` |
| TASK-INF-010 | Provide baseline NetworkPolicy templates | `infrastructure/networkpolicies/*` | `[SEC-INF-003]` | Policies apply cleanly in target namespaces |

## 6. Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Node | Check cluster node count | `kubectl get nodes --no-headers \| wc -l` | 4 |
| VAL-PLN-002 | Windows | Verify Windows `kubectl` connectivity | `kubectl version -o yaml` (from Windows) | Exit code 0 |
| VAL-PLN-003 | MetalLB | Check MetalLB pod health | `kubectl -n metallb-system get pods` | All `Running` |
| VAL-PLN-004 | Ingress | Check ingress-nginx pod health | `kubectl -n ingress-nginx get pods` | Controller `Ready` |
| VAL-PLN-005 | Net | Test local port mapping (HTTP) | `code=$(curl -sS -o /dev/null -w \"%{http_code}\" http://127.0.0.1:18080/); test \"$code\" -ge 200 -a \"$code\" -lt 500` | Exit code 0 |
| VAL-PLN-006 | GPU | Verify GPU availability (optional) | `kubectl get nodes -o custom-columns=NAME:.metadata.name,GPUS:.status.allocatable.nvidia\\.com/gpu` | Non-empty GPU where expected |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| WSL2 Resource Pressure | High | Monitor host memory/CPU; adjust `.wslconfig`. |
| Port Conflict | Med | Verify no other services use 18080/18443. |
| ingress-nginx retirement | Med | Track and migrate to an alternative controller (Traefik/Gateway API) in a follow-up ADR if needed. |

## 8. Completion Criteria

- [ ] All nodes report `Ready` status.
- [ ] MetalLB is successfully assigning IPs from the specified range.
- [ ] `curl http://127.0.0.1:18080` returns an HTTP response (2xx–4xx).
- [ ] GPU-enabled pods can access host hardware (optional).

## 9. References

- **PRD**: `docs/prd/infra/home-cluster-infra-prd.md`
- **Spec**: `specs/infra/spec.md`
- **ADRs**: `docs/adr/infra/0001-k3d-local-cluster.md`
