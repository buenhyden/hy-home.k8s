---
title: "Home Cluster Infrastructure PRD"
status: "Approved"
version: "v1.0.0"
owner: "hy"
stakeholders: ["hy"]
tags: ["prd", "requirements", "product", "infrastructure", "core-infra"]
---

# Product Requirements Document (PRD)

> **Status**: Approved
> **Target Version**: v1.0.0
> **Owner**: hy
> **Stakeholders**: hy

*Target Directory: `docs/prd/core-infra/home-cluster-infra-prd.md`*

---

## 1. Vision & Problem Statement

**Vision**: Provide a robust, scalable, and reproducible Kubernetes-based home automation and development environment that supports high-performance workloads including GPU-accelerated AI components.

**Problem Statement**: Managing individual Docker containers for various home services and development tools is becoming complex and difficult to scale. There is a need for a centralized, orchestrated environment (Kubernetes) that provides high availability, resource management, and observability while running on commodity hardware or specialized local nodes.

## 2. Target Personas

- **Persona 1 (Home User)**: Wants high availability for critical home services (e.g., automation, file sharing).
- **Persona 2 (Developer)**: Needs a local Kubernetes cluster for testing k8s-native applications with GPU support for AI experiments.
- **Persona 3 (Windows Developer)**: Uses WSL2 and needs a cluster that integrates seamlessly with Windows networking.

## 3. Success Metrics (Quantitative)

| ID                 | Metric Name        | Baseline (Current) | Target (Success) | Measurement Period  |
| ------------------ | ------------------ | ------------------ | ---------------- | ------------------- |
| **REQ-PRD-MET-01** | Integration Speed | ~2 hours manual   | < 10 mins automated | Per cluster rebuild |
| **REQ-PRD-MET-02** | Service Uptime    | N/A (Manual)       | > 99.9%          | Monthly             |
| **REQ-PRD-MET-03** | GPU Availability  | Workstation-only  | All agents accessible | Always              |

## 4. Key Use Cases & Acceptance Criteria (GWT)

| ID           | User Story (INVEST)                                                                      | Acceptance Criteria (Given-When-Then)                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **STORY-01** | **As a** Developer,<br>**I want** to spin up a k8s cluster locally,<br>**So that** I can test deployments without cloud costs. | **Given** k3d is installed,<br>**When** I run the cluster creation command,<br>**Then** a 1-server 3-agent cluster is initialized. |
| **STORY-02** | **As a** Home User,<br>**I want** to access services via port 18080/18443,<br>**So that** I can use my services through the host IP. | **Given** the cluster is running,<br>**When** I access 127.0.0.1:18080,<br>**Then** traffic is routed to the k3s loadbalancer. |
| **STORY-03** | **As an** AI Researcher,<br>**I want** GPU resources shared across the cluster,<br>**So that** I can run CUDA-enabled pods. | **Given** NVIDIA runtime is configured,<br>**When** I request `gpuRequest: all`,<br>**Then** all agents expose GPU capabilities to pods. |
| **STORY-04** | **As a** Windows Developer,<br>**I want** cluster IP routes available from Windows shell,<br>**So that** I can use `kubectl` from outside WSL. | **Given** k3d cluster initialization,<br>**When** kubeconfig is updated via `--kubeconfig-switch-context`,<br>**Then** host `kubectl` can communicate with cluster. |

## 5. Scope & Functional Requirements

- **[REQ-PRD-FUN-01]**: Kubernetes cluster setup using k3d with 1 server and 3 agents.
- **[REQ-PRD-FUN-02]**: External access via host ports 18080 (HTTP) and 18443 (HTTPS).
- **[REQ-PRD-FUN-03]**: GPU resource pass-through support.
- **[REQ-PRD-FUN-04]**: Disable default Traefik and ServiceLB to allow custom ingress setup.

## 6. Out of Scope

- Multi-node physical cluster setup (hardware-level).
- Public cloud provider integration (EKS/GKE).

## 7. Milestones & Roadmap

- **PoC**: Local k3d setup with manual scripts. (Done)
- **MVP**: Automated k3d manifest-based setup with GPU support. (Current)
- **v1.0**: Full observability stack integration.

## 8. Risks, Security & Compliance

- **Risks & Mitigation**: Local storage limitations. Mitigation: External CSI integration planned.
- **Compliance & Privacy**: Local only environment ensures data privacy.
- **Security Protocols**: TLS-SAN for local host access.

## 9. Assumptions & Dependencies

- **Assumptions**: Host system has Docker and k3d installed.
- **External Dependencies**: NVIDIA Container Toolkit for GPU support.

## 11. Related Documents (Reference / Traceability)

- **Technical Specification**: [Link to Spec](../../../specs/core-infra/spec.md)
- **Architecture Decisions (ADRs)**: [Link to ADRs](../../../docs/adr/README.md)
