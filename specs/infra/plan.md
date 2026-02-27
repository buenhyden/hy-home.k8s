# Implementation Plan: Core Infrastructure Deployment

*Target Directory: `specs/infra/plan.md`*

## 1. Prerequisites

- Docker installed and running.
- k3d CLI installed.
- NVIDIA Container Toolkit (optional, for GPU).

## 2. Execution Steps

### Phase 0: WSL Environment Preparation

- [ ] Verify WSL2 version: `wsl --version` (should be 0.67.6+).
- [ ] Enable systemd: `echo -e "[boot]\nsystemd=true" | sudo tee -a /etc/wsl.conf`.
- [ ] Restart WSL: `wsl --shutdown` (from Windows PowerShell).
- [ ] Configure Docker integration in Docker Desktop or install native Docker in WSL.

### Phase 1: Preparation

- [ ] Review `infrastructure/k3d/k3d-cluster.yaml`.
- [ ] Verify Docker network availability.

### Phase 2: Cluster Setup

- [ ] Create cluster: `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml`.
- [ ] Verify nodes: `kubectl get nodes`.

### Phase 3: Post-Setup

- [ ] Install essential tools (Metallb, Ingress-Nginx) - *Coming in further specs*.
- [ ] (Optional) Merge kubeconfig to Windows host for external access.

## 3. Verification

- [ ] `kubectl cluster-info`.
- [ ] Verify GPU visibility in k3s containers (if applicable).
