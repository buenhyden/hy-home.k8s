---
title: "ArgoCD GitOps PRD (Local k3d)"
status: "Draft"
version: "v1.0.0"
owner: "hy"
stakeholders: ["hy"]
parent_epic: "../../prd/infra/home-cluster-infra-prd.md"
tags: ["prd", "requirements", "product", "gitops", "argocd", "sealed-secrets"]
---

# Product Requirements Document (PRD)

> **Status**: Draft
> **Target Version**: v1.0.0
> **Owner**: hy
> **Stakeholders**: hy
> **Parent Epic**: [Home Cluster Infra PRD](../infra/home-cluster-infra-prd.md)

*Target Directory: `docs/prd/gitops/argocd-gitops-prd.md`*
*Note: This document defines the What and Why. It must be approved before Spec generation.*

---

## 0. Pre-Review Checklist (Business & Product)

| Item                  | Check Question                                                         | Required | Alignment Notes (Agreement) | PRD Section |
| --------------------- | ---------------------------------------------------------------------- | -------- | --------------------------- | ----------- |
| Vision & Goal         | Is the problem + business goal defined in one paragraph?               | Must     | Drafted                     | Section 1   |
| Success Metrics       | Are the key success/failure metrics defined with quantitative targets? | Must     | Drafted                     | Section 3   |
| Target Users          | Are specific primary personas and their pain points defined?           | Must     | Drafted                     | Section 2   |
| Use Case (GWT)        | Are acceptance criteria written in Given-When-Then format?             | Must     | Drafted                     | Section 4   |
| Scope (In)            | Is the feature list included in this release clearly defined?          | Must     | Drafted                     | Section 5   |
| Not in Scope          | Is what we will NOT build in this release explicitly listed?           | Must     | Drafted                     | Section 6   |
| Timeline & Milestones | Are PoC / MVP / Beta / v1.0 milestones dated?                          | Must     | Drafted                     | Section 7   |
| Risks & Compliance    | Are major risks, privacy, or regulatory constraints documented?        | Must     | Drafted                     | Section 8   |

---

## 1. Vision & Problem Statement

**Vision**: Provide a reproducible, Git-driven deployment workflow for the local WSL2 + k3d Kubernetes cluster so that infrastructure and workloads converge to a known desired state with minimal manual steps.

**Problem Statement**: As the local cluster grows, manually applying YAML and debugging drift becomes error-prone and non-repeatable. We need a GitOps controller to continuously reconcile desired state, enforce deterministic version pins, and enable safe rollbacks.

## 2. Target Personas

> **Important**: Link every core requirement to a specific persona defined here.

- **Persona 1 (Local Platform Operator)**:
  - **Pain Point**: Manual `kubectl apply` steps are hard to repeat; drift is invisible.
  - **Goal**: One bootstrap flow that makes the cluster converge from Git and stay consistent.
- **Persona 2 (Developer / App Owner)**:
  - **Pain Point**: App deployment changes are not tracked; rollbacks are ad-hoc.
  - **Goal**: Declarative app delivery with clear “Synced/Healthy” feedback and rollback via Git.

## 3. Success Metrics (Quantitative)

| ID                 | Metric Name                     | Baseline (Current) | Target (Success) | Measurement Period |
| ------------------ | ------------------------------- | ------------------ | ---------------- | ------------------ |
| **REQ-PRD-MET-01** | GitOps convergence time         | Manual / unknown   | < 5 minutes      | Per sync           |
| **REQ-PRD-MET-02** | Drift correction (selfHeal)     | Manual             | Automatic        | Always             |
| **REQ-PRD-MET-03** | Plaintext secret commits        | Risk exists        | 0                | Continuous         |

## 4. Key Use Cases & Acceptance Criteria (GWT)

| ID           | User Story (INVEST) | Acceptance Criteria (Given-When-Then) |
| ------------ | ------------------- | ------------------------------------- |
| **STORY-01** | **As a** Local Platform Operator,<br>**I want** to bootstrap ArgoCD and a root application,<br>**So that** infra/apps reconcile from Git. | **Given** ArgoCD and Sealed Secrets are installed,<br>**When** I apply the root Application manifest,<br>**Then** ArgoCD creates child Applications and they converge to `Synced/Healthy`. |
| **STORY-02** | **As a** Developer,<br>**I want** ArgoCD to detect drift and reconcile it,<br>**So that** the cluster matches Git. | **Given** `selfHeal=true`,<br>**When** a managed resource is changed out-of-band,<br>**Then** ArgoCD returns it to the Git-defined state. |
| **STORY-03** | **As a** Local Platform Operator,<br>**I want** private repo access via SSH deploy key without committing plaintext secrets,<br>**So that** GitOps remains secure. | **Given** a sealed repository credential is applied,<br>**When** ArgoCD attempts to fetch the repo,<br>**Then** repo connection is `OK` and no plaintext Secret is stored in Git. |

## 5. Scope & Functional Requirements

- **[REQ-PRD-FUN-01]** Install ArgoCD (pinned version) for local cluster GitOps.
- **[REQ-PRD-FUN-02]** Install Sealed Secrets (pinned version) for sealed secret workflow.
- **[REQ-PRD-FUN-03]** Implement App-of-Apps GitOps structure for local cluster (infra + apps).
- **[REQ-PRD-FUN-04]** Configure ArgoCD applications with `automated` sync, `prune=true`, `selfHeal=true`.
- **[REQ-PRD-FUN-05]** Enforce “no plaintext secrets in Git” via SealedSecrets usage.
- **[REQ-PRD-FUN-06]** Standardize ArgoCD access via `kubectl port-forward` (v1 baseline).

## 6. Out of Scope

- Public exposure of ArgoCD via Ingress/NodePort (v1 baseline uses port-forward only).
- Multi-cluster GitOps, multi-environment promotion, or ApplicationSet-based fleet management.
- External Secrets Operator, Vault, or cloud KMS integrations (future iterations).

## 7. Milestones & Roadmap

- **PoC**: 2026-02-27 - Vendored manifests + manual bootstrap documented.
- **MVP**: 2026-03-07 - App-of-Apps structure + infra convergence for local cluster.
- **Beta**: 2026-03-14 - Private repo SSH deploy key + SealedSecrets workflow validated end-to-end.
- **v1.0**: 2026-03-21 - Documentation/Runbooks complete + drift/rollback verified.

## 8. Risks, Security & Compliance

- **Risks & Mitigation**:
  - Bootstrap chicken/egg (private repo + sealed secrets) → Define deterministic manual bootstrap runbook.
  - Version pin drift (targetRevision pinning) → Update process documented in Spec and runbook.
  - Controller lifecycle changes (upstream breaking changes) → Vendoring + pinned versions.
- **Compliance & Privacy**: No PII required for local cluster bootstrap.
- **Security Protocols**:
  - No plaintext secrets committed.
  - SSH deploy key is read-only and stored sealed.

## 9. Assumptions & Dependencies

- **Assumptions**:
  - The local cluster uses WSL2 + k3d as defined by the Infra PRD/Spec.
  - Repo is private or treated as private for credential management.
- **External Dependencies**:
  - GitHub for repository hosting.
  - ArgoCD and Sealed Secrets upstream release artifacts.

## 10. Q&A / Open Issues

- **[ISSUE-01]** targetRevision pinning vs developer convenience - **Update**: Use pinning; document update workflow.

## 11. Related Documents (Reference / Traceability)

- **Infra PRD**: [docs/prd/infra/home-cluster-infra-prd.md](../infra/home-cluster-infra-prd.md)
- **Technical Specification**: [specs/gitops/spec.md](../../../specs/gitops/spec.md)
- **Architecture Decisions (ADRs)**: [docs/adr/gitops/0001-argocd-gitops.md](../../adr/gitops/0001-argocd-gitops.md)
