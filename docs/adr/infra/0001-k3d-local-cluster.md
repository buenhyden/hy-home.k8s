# Architecture Decision Record (ADR)

*Target Directory: `docs/adr/infra/0001-k3d-local-cluster.md`*

## Title: 0001-k3d-local-cluster

- **Status:** Accepted
- **Date:** 2026-02-27
- **Authors:** hy
- **Deciders:** hy

## 1. Context and Problem Statement

The home automation and development environment requires a Kubernetes cluster that can run locally on single or multiple machines without the overhead of full VMs or complex networking setups. We need a lightweight solution that supports easy lifecycle management (create/delete) and advanced features like GPU pass-through.

## 2. Decision Drivers

- **Performance**: Must be lightweight and low-overhead.
- **Developer Experience**: Fast cluster creation/deletion.
- **GPU Support**: Essential for AI workloads.
- **Flexibility**: Ability to easily expose ports to the host.

## 3. Decision Outcome

**Chosen option: "k3d (k3s in Docker)"**, because it provides the best balance between speed, resource usage, and features for local development, especially on **WSL2**. Running k3s within Docker containers abstracts away the complexities of running system services directly in WSL, leveraging the high-performance Docker-WSL2 integration.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Allows testing k8s security policies locally.
- **Observability**: Supports standard Helm-based observability stacks (Prometheus/Loki).
- **Performance**: High performance due to native Docker execution.
- **Documentation**: Well-established engine with extensive community documentation.

### 3.2 Positive Consequences

- Sub-60 second cluster startup.
- Easy port mapping to the local host.
- Native integration with Docker-based workflows.
- Simple multi-node simulation (1 server, 3 agents).

### 3.3 Negative Consequences

- Potential resource contention with other Docker containers.
- Some limitations in simulating certain storage backends.

## 4. Alternatives Considered (Pros and Cons)

### Kind (Kubernetes in Docker)

Similar to k3d but uses upstream k8s distributions.

- **Good**, because standard k8s.
- **Bad**, because heavier than k3s and slightly slower startup.

### Minikube

Traditional local k8s tool.

- **Good**, because mature and feature-rich.
- **Bad**, because heavier resource footprint and often requires a dedicated VM or complex Docker integration.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: k3d is the industry standard for lightweight local k8s testing.
- **Technical Requirements Addressed**: REQ-PRD-FUN-01

## 6. Related Documents (Traceability)

- **Feature PRD**: [Link to PRD](../../../docs/prd/infra/home-cluster-infra-prd.md)
- **Feature Spec**: [Link to Feature Spec](../../../specs/infra/spec.md)
