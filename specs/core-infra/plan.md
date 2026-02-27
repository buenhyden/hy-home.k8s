# Implementation Plan: Core Infrastructure Deployment

*Target Directory: `specs/core-infra/plan.md`*

## 1. Prerequisites

- Docker installed and running.
- k3d CLI installed.
- NVIDIA Container Toolkit (optional, for GPU).

## 2. Execution Steps

### Phase 1: Preparation

- [ ] Review `infrastructure/k3d/k3d-cluster.yaml`.
- [ ] Verify Docker network availability.

### Phase 2: Cluster Setup

- [ ] Create cluster: `k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml`.
- [ ] Verify nodes: `kubectl get nodes`.

### Phase 3: Post-Setup

- [ ] Install essential tools (Metallb, Ingress-Nginx) - *Coming in further specs*.

## 3. Verification

- [ ] `kubectl cluster-info`.
- [ ] Verify GPU visibility in k3s containers (if applicable).
