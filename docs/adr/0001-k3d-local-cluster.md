---
title: 'ADR 0001: Local Development Cluster selection (k3d)'
status: 'Accepted'
date: '2026-02-27'
tags: ['adr', 'infra']
layer: "infra"
---

# ADR: Local Development Cluster selection (k3d) - 0001

- **Status**: Accepted
- **Owner**: buenhyden
- **Last Reviewed**: 2026-02-27

**Overview (KR):** k3d를 사용한 로컬 개발용 Kubernetes 클러스터 구축 결정.

## 1. Metadata

- **ADR Number**: 0001
- **Status**: Accepted
- **Date**: 2026-02-27
- **Deciders**: buenhyden
- **layer**: infra

## 2. Context & Problem Statement

The home automation and development environment requires a Kubernetes cluster that can run locally on single or multiple machines without the overhead of full VMs. We need a lightweight solution that supports easy lifecycle management and advanced features like GPU pass-through.

## 3. Decision Drivers (Senior)

- **Performance**: Must be lightweight and low-overhead (`REQ-PRD-INF-01`).
- **Developer Experience**: Fast cluster creation/deletion.
- **GPU Support**: Essential for home-labs involving AI/ML workloads.
- **Flexibility**: Ability to easily expose ports to the host (WSL2).

## 4. Decision Outcome

**Chosen option: "k3d (k3s in Docker)"**

### Rationale
k3d provides the best balance between speed and resource usage on WSL2. Running k3s (v1.31.0) within Docker abstracts away service complexities and simplifies multi-node simulation.

### Consequences
- **Positive**: Sub-60s cluster startup, simple multi-node simulation.
- **Negative**: Potential resource contention with host Docker processes.

## 5. Technical Debt & Risk Assessment (Senior)

- **Debt Incurred**: Use of ephemeral Docker volumes for local storage might lead to data loss if clusters are not properly migrated to PersistentVolumes.
- **Risk Score**: Medium
- **Mitigation Plan**: Monitor Docker resource limits in WSL2 (`.wslconfig`) and implement CSI drivers early in the staging phase.

## 6. Deferred Decisions (ADL - Architecture Decision Log)

- **Production Cluster Selection**: Deferred until the home-lab hardware is purchased.
- **Multi-machine Sync**: Deferred until network adjacency is established for multiple k3d nodes.

## 7. Related Artifacts
- **ARD Reference**: `[../ard/2026-02-27-k3d-cluster-ard.md]`
- **Spec Reference**: `[../specs/2026-03-16-infra-spec.md]`
