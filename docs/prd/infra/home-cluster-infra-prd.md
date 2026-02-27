---
title: "Home Cluster Infrastructure PRD"
status: "Approved"
version: "v1.0.0"
owner: "hy"
stakeholders: ["hy"]
tags: ["prd", "requirements", "product", "infrastructure", "infra"]
---

# Product Requirements Document (PRD)

> **Status**: Approved
> **Target Version**: v1.0.0
> **Owner**: hy
> **Stakeholders**: hy

*Target Directory: `docs/prd/infra/home-cluster-infra-prd.md`*
*Note: This document defines the What and Why for the Core Infrastructure.*

---

## 0. Pre-Review Checklist (Business & Product)

| Item                  | Check Question                                                         | Required | Alignment Notes (Agreement) | PRD Section |
| --------------------- | ---------------------------------------------------------------------- | -------- | --------------------------- | ----------- |
| Vision & Goal         | Is the problem + business goal defined in one paragraph?               | Must     | Defined                     | Section 1   |
| Success Metrics       | Are the key success/failure metrics defined with quantitative targets? | Must     | Defined                     | Section 3   |
| Target Users          | Are specific primary personas and their pain points defined?           | Must     | Home User & AI Dev          | Section 2   |
| Use Case (GWT)        | Are acceptance criteria written in Given-When-Then format?             | Must     | Yes                         | Section 4   |
| Scope (In)            | Is the feature list included in this release clearly defined?          | Must     | k3d lifecycle               | Section 5   |
| Not in Scope          | Is what we will NOT build in this release explicitly listed?           | Must     | Public Cloud                | Section 6   |
| Timeline & Milestones | Are PoC / MVP / Beta / v1.0 milestones dated?                          | Must     | TBD                         | Section 7   |
| Risks & Compliance    | Are major risks, privacy, or regulatory constraints documented?        | Must     | Hardware dep noted          | Section 8   |

---

## 1. Vision & Problem Statement

**Vision**: Provide a robust, scalable, and reproducible Kubernetes-based home automation and development environment that supports high-performance workloads including GPU-accelerated AI components.

**Problem Statement**: Managing individual Docker containers for various home services and development tools is becoming complex and difficult to scale. There is a need for a centralized, orchestrated environment (Kubernetes) that provides high availability, resource management, and observability while running on commodity hardware or specialized local nodes.

## 2. Target Personas

> **Important**: Link every core requirement to a specific persona defined here.

- **Persona 1 (Home User)**:
  - **Pain Point**: Difficulty managing multiple disconnected home automation services.
  - **Goal**: High availability and centralized management for home services.
- **Persona 2 (Developer)**:
  - **Pain Point**: High cloud costs for testing Kubernetes-native applications.
  - **Goal**: Local k8s cluster for rapid iteration with GPU support for AI.
- **Persona 3 (Windows Developer)**:
  - **Pain Point**: Networking friction between WSL2 and Windows host.
  - **Goal**: Seamless cluster integration with Windows development workflow.

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
- **[REQ-PRD-FUN-05]**: Support for external LoadBalancer IP pools (via MetalLB).
- **[REQ-PRD-FUN-06]**: Use of native MetalLB manifests (v0.14.8+) for deterministic deployment across environments.
- **[REQ-PRD-FUN-07]**: Windows host access to kube-apiserver via a localhost-forwarded endpoint (kubeconfig/TLS SAN alignment).

## 6. Out of Scope

- Multi-node physical cluster setup (hardware-level).
- Public cloud provider integration (EKS/GKE).

## 7. Milestones & Roadmap

- **PoC**: 2026-02-27 - Local k3d setup with manual commands. (Done)
- **MVP**: 2026-02-27 - YAML-based k3d setup with GPU support and port mappings. (Current)
- **Beta**: TBD - Add GitOps deployment flow and baseline security policies.
- **v1.0**: TBD - Full observability stack integration.

## 8. Risks, Security & Compliance

- **Risks & Mitigation**: Local storage limitations. Mitigation: External CSI integration planned.
- **Compliance & Privacy**: Local only environment ensures data privacy.
- **Security Protocols**: TLS-SAN for local host access.

## 9. Assumptions & Dependencies

- **Assumptions**: Host system has Docker and k3d installed.
- **External Dependencies**: NVIDIA Container Toolkit for GPU support.

## 10. Q&A / Open Issues

- **[ISSUE-01]**: Do we require `systemd=true` for k3d-only workflows on WSL2? - **Update**: TBD (document and minimize hard requirements).
- **[ISSUE-02]**: Is the primary Docker runtime Docker Desktop (Windows) or Docker Engine inside WSL? - **Update**: TBD (affects GPU and networking steps).
- **[ISSUE-03]**: Do we support a direct `k3s` install in WSL2 (no Docker) as an alternative local cluster mode? - **Update**: Out of scope for v1.0.0 (tracked for future evaluation).

## 11. Related Documents (Reference / Traceability)

- **Technical Specification**: [Link to Spec](../../../specs/infra/spec.md)
- **API Specification**: N/A
- **Architecture Decisions (ADRs)**: [Link to ADRs](../../../docs/adr/README.md)
