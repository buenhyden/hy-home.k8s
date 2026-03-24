# Agent Bootstrap Governance

> [!NOTE]
> **hy-home.k8s**: A spec-driven Kubernetes home-lab infrastructure for documentation governance and AI-assisted delivery workflows.

This document defines the universal entry point for all AI Agents interacting with this repository. It enforces **Spec-Driven Development (SDD)** and JIT (Just-In-Time) metadata routing for maximum context efficiency.

## 1. Core Principles (March 2026)

- **Spec-Anchored**: All implementation work MUST be grounded in approved `PRD` and `Spec` artifacts in `docs/01.prd/` and `docs/04.specs/`.
- **Flat Taxonomy**: SSoT (Single Source of Truth) files live in numbered folders (e.g., `docs/01.prd/`).
- **Metadata Routing**: Agents discover context by searching for `layer: <name>` inside `docs/` to identify ownership.
- **Lazy Loading**: Load only shared governance initially; dynamically load layer-specific detail JIT via the `scopes/` directory.

## 2. Mandatory Taxonomy (SSoT Paths)

| Stage | Path | Purpose |
| :--- | :--- | :--- |
| **00** | `docs/00.agent/` | AI Agent Governance & Scopes |
| **01** | `docs/01.prd/` | Product Requirements & Intent |
| **02** | `docs/02.ard/` | Architecture Reference Documents |
| **03** | `docs/03.adr/` | Architectural Decision Records |
| **04** | `docs/04.specs/` | Technical Specifications (SSoT) |
| **05** | `docs/05.plans/` | Implementation & Validation Plans |
| **06** | `docs/06.tasks/` | Granular Task & Progress Tracking |
| **07** | `docs/07.guides/` | Operational & Developer Guides |
| **08** | `docs/08.operations/` | Monitoring & Environment State |
| **09** | `docs/09.runbooks/` | Incident Response Procedures |
| **10** | `docs/10.incidents/` | Live Incident Tracking |
| **11** | `docs/11.postmortems/` | Retrospectives & Lessons Learned |

## 3. Layer Identification Protocol

Before performing any task, the Agent MUST:

1. Identify the target **Layer** (Product, Architecture, Frontend, Backend, Infra, Security, QA).
2. Locate the SSoT for that layer using `grep -r "layer: <name>" docs/`.
3. Load the corresponding scope 지침 from `docs/00.agent/scopes/<layer>.md`.
4. Adopt the required Persona and announce:
    > "As your **[Persona Name]**, I am targeting the **[Layer]** layer and adopting the **[Standard ID]** governance. I am using all available skills to accelerate this task."
