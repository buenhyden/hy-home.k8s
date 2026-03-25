# Agent Bootstrap Governance

> [!NOTE]
> **hy-home.k8s**: A spec-driven Kubernetes home-lab infrastructure for documentation governance and AI-assisted delivery workflows.

This document defines the universal entry point for all AI Agents. It enforces **Spec-Driven Development (SDD)** and JIT (Just-In-Time) metadata routing for maximum context efficiency.

## 1. Core Principles (March 2026)

- **Spec-Anchored**: All implementation work MUST be grounded in approved `PRD` and `Spec` artifacts in `docs/01.prd/` and `docs/04.specs/`.
- **Flat Taxonomy**: SSoT files live in numbered folders (01-11).
- **Lazy Loading**: Load only shared governance initially; dynamically load scope-specific detail JIT via the `scopes/` directory.

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
| **07-11** | `docs/07~11/` | Guides, Ops, Runbooks, Incidents, Postmortems |

## 3. Layer Identification Protocol

Before performing any task, the Agent MUST:

1. Identify the target **Layer** (Product, Architecture, Frontend, Backend, Infra, Security, QA).
2. Load the corresponding scope from `docs/00.agent/scopes/<layer>.md`.
3. Adopt the required Persona from `persona-matrix.md`.
4. Announce:
    > "As your **[Persona Name]**, I am targeting the **[Layer]** layer. I am using all available skills to accelerate this task."
