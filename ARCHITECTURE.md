---
layer: "meta"
---
# System Architecture

This document defines the high-level architecture of projects created from this template. It serves as a blueprint that should be customized for each new project.

## 1. System Context & Necessity

This template provides a standardized foundation for building software projects.

**Necessity**: This specific `ARCHITECTURE.md` file is absolutely essential as the global, unchanging architectural law of the repository. While `docs/adr/` handles specific component decisions over time and `docs/ard/` holds deep architectural diagrams, this root file holds the *highest-level constraints and checklists* that must NEVER be violated by any human or AI agent without a formal override.

**What Must Be Written Here**:

- The overarching architecture is **GitOps-driven Infrastructure as Code**.
- The core tech stack revolves around **Kubernetes (k3s)**, **k3d**, and **WSL2**.
- The Architectural Checklist ensures alignment with the **Spec-Driven Development (SDD)** lifecycle.

### Core Architecture Pillars

- **Spec-Driven Development**: `docs/specs/` uniquely drives all implementation.
- **AI-Assisted Development**: Multi Sub-Agent AI system phases (`AGENTS.md`).
- **Template-Based Documentation**: Consistent output enforced via `templates/`.

## 2. Core Constraints & Decisions

### Core Constraints & Decisions

| Decision                | Rationale                                                                           |
|-------------------------|-------------------------------------------------------------------------------------|
| **Spec-Driven Code**    | Eliminates AI hallucination by giving Coder Agents a hard, human-approved target.   |
| **Templates Mandatory** | Ensures parsing consistency for future AI tasks (PRDs, Specs, Runbooks).            |
| **Dedicated Runbooks**  | Prevents ops scripts from getting lost in `docs/` hierarchies.                      |

> See `docs/adr/` for detailed Architecture Decision Records that shaped this specific system logic.

## 3. Architecture & Tech Stack Checklist

When starting a project or writing an Architecture Reference Document (ARD), the following checklist MUST be addressed and agreed upon by the Human and Planner Agent.

> [!IMPORTANT]
> The full checklist and process enforcement rules are now located in:
> **[Architecture & Tech Stack Checklist](docs/ard/architecture-checklist.md)**

All ARDs created in `docs/ard/` MUST explicitly answer the items in that checklist, adhering to `.agent/rules/1910-architecture-documentation.md` and `.agent/rules/1901-architecture-rules.md`.

## 4. Reference Technology Stack (Template)

Customize the following for your specific project upon cloning.

| Layer        | Selected Technology           | Purpose                              |
| ------------ | ----------------------------- | ------------------------------------ |
| **Engine**   | k3d (k3s)                     | Local cluster node management        |
| **Host**     | WSL2 (Ubuntu)                 | Development and runtime foundation   |
| **Networking**| MetalLB                       | L2 LoadBalancer (Deterministic IPs) |
| **Ingress**  | Ingress-Nginx                 | Layer 7 traffic and SSL              |
| **GitOps**   | ArgoCD                        | Declarative state reconciliation     |
| **Secrets**  | Sealed Secrets                | Encrypted Git-safe K8s secrets       |

## 4. Integration & Separation Points

### Document vs Code vs Operations

- **`docs/`**: Holds "Why" and "What" (PRD, ADR, ARD).
- **`docs/specs/`**: Holds "Exactly How" prior to coding.
- **`docs/runbooks/`**: Holds executable scripts and "What to do when X fails."

### Extending the Architecture

1. **Design Changes**: Create an ADR in `docs/adr/` using `templates/adr-template.md`.
2. **Data Structure Changes**: Document via ARD in `docs/ard/` using `templates/ard-template.md`.
3. **Execution Rules**: Modify `.agent/rules/` to enforce new architectural linters globally.

---
> **Note**: This architecture document must be kept strictly to high-level system design. For operational procedures, alerting logic, or CI orchestration, consult `OPERATIONS.md`.
