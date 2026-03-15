---
layer: "meta"
---
# System Architecture

This document defines the high-level architecture of `hy-home.k8s`. It serves as the global architectural law of the repository.

## 1. System Context & Necessity

This repository provides a standardized foundation for building and managing a local Kubernetes platform.

**Necessity**: This `ARCHITECTURE.md` file is essential as the root architectural law. While `docs/adr/` handles specific component decisions and `docs/ard/` holds deep architectural reference documents, this root file holds the *highest-level constraints* that MUST NEVER be violated.

**Key Principles**:

- **GitOps-driven Infrastructure as Code**: Declarative state management via ArgoCD.
- **Local-First Cluster**: Optimized for k3d, k3s, and WSL2.
- **Spec-Driven Development (SDD)**: All implementation MUST trace back to `docs/specs/`.

## 2. Core Constraints & Decisions

| Decision                | Rationale                                                                           |
|-------------------------|-------------------------------------------------------------------------------------|
| **Spec-Driven Code**    | Eliminates AI hallucination by providing a hard, human-approved target in `docs/specs/`.|
| **Templates Mandatory** | Ensures structural consistency for PRDs, ADRs, Specs, and Runbooks using `templates/`.|
| **Flattened Hierarchy** | Documentation is organized in a flat, type-first hierarchy under `docs/`.           |
| **Plural Paths**        | Execution documents reside in plural directories (e.g., `docs/plans/`, `docs/specs/`).|

## 3. Architecture & Tech Stack Checklist

Development work MUST align with the **[Architecture & Tech Stack Checklist](docs/ard/architecture-checklist.md)**. All Architecture Reference Documents (ARD) in `docs/ard/` must explicitly address this checklist.

## 4. Reference Technology Stack

| Layer        | Selected Technology           | Purpose                              |
| ------------ | ----------------------------- | ------------------------------------ |
| **Engine**   | k3d (k3s)                     | Local cluster node management        |
| **Host**     | WSL2 (Ubuntu)                 | Development and runtime foundation   |
| **Networking**| MetalLB                       | L2 LoadBalancer (Deterministic IPs) |
| **Ingress**  | Ingress-Nginx                 | Layer 7 traffic and SSL              |
| **GitOps**   | ArgoCD                        | Declarative state reconciliation     |
| **Secrets**  | Sealed Secrets                | Encrypted Git-safe K8s secrets       |

## 5. Operations & Separation Points

- **`docs/prd/`**: Holds product requirements and vision.
- **`docs/adr/`**: Records architectural decisions and consequences.
- **`docs/ard/`**: Contains deep architectural diagrams and reference structures.
- **`docs/specs/`**: Holds exact implementation specifications.
- **`docs/plans/`**: Holds execution roadmaps and sequences.
- **`docs/runbooks/`**: Holds executable operational procedures.
- **`docs/operations/`**: Holds strategic operational blueprints and tracking (incidents, postmortems).

## 6. Extending the Architecture

1. **Design Decisions**: Create an ADR in `docs/adr/` using `templates/adr-template.md`.
2. **System Structure**: Document via ARD in `docs/ard/` using `templates/ard-template.md`.
3. **Instruction Refinement**: Update AI Agent rules in `docs/agentic/` to enforce new architectural standards.

---
> **Note**: This document focuses on high-level system design. For operational procedures or incident response, consult `OPERATIONS.md` and `docs/runbooks/`.
