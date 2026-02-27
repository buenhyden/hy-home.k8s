# Implementation Plan: Core Infrastructure Deployment

*Target Directory: `specs/infra/plan.md`*

## 1. Prerequisites

- Docker installed and running.
- k3d CLI installed.
- NVIDIA Container Toolkit (optional, for GPU).

## 2. Execution Steps

### Phase 0: WSL Environment Preparation

- [ ] **WSL2 System Check**: Verify version 0.67.6+ using `wsl --version`.
- [ ] **Systemd Enablement**: Ensure `[boot] systemd=true` exists in `/etc/wsl.conf`.
- [ ] **NVIDIA Toolkit**: Verify GPU visibility via `nvidia-smi` inside a test Docker container.
- [ ] **Restart**: Run `wsl --shutdown` and restart terminal to apply systemd changes.

### Phase 1: Preparation

- [ ] Review `infrastructure/k3d/k3d-cluster.yaml`.
- [ ] Verify `docker` and `k3d` CLI readiness.

### Phase 2: Cluster Setup

- [ ] **Cluster Creation**: `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml`.
- [ ] **Kubeconfig Audit**: Ensure context is set to `k3d-hy-k3d`.

### Phase 3: Post-Setup & Networking

- [ ] **MetalLB Native Installation**:
  - [ ] Apply manifest: `kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml`.
  - [ ] Verification: `kubectl wait --namespace metallb-system --for=condition=ready pod --selector=app=metallb --timeout=120s`.
- [ ] **IP Pool Configuration**:
  - [ ] Apply config: `kubectl apply -f infrastructure/ipaddresspool.yaml`.

## 3. Verification

- [ ] **Node Count**: `kubectl get nodes` (Expected: 1 server + 3 agents + 1 LB container).
- [ ] **GPU Capacity**: `kubectl describe node | grep -i nvidia.com/gpu:`.
- [ ] **LoadBalancer Pool**: `kubectl get ipaddresspool -n metallb-system`.
- [ ] **External Connectivity**: Test access to `127.0.0.1:18080`.
