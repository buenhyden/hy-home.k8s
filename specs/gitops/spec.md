---
title: "GitOps (ArgoCD) Implementation Spec"
status: "Draft"
version: "1.0"
owner: "hy"
prd_reference: "../../docs/prd/gitops/argocd-gitops-prd.md"
api_reference: "N/A"
arch_reference: "../../ARCHITECTURE.md"
tags: ["spec", "implementation", "gitops", "argocd", "sealed-secrets"]
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: [docs/prd/gitops/argocd-gitops-prd.md](../../docs/prd/gitops/argocd-gitops-prd.md)
> **Related API Spec**: N/A
> **Related Architecture**: [Link to ARCHITECTURE.md](../../ARCHITECTURE.md)

*Target Directory: `specs/gitops/spec.md`*
*Note: This document is the absolute Source of Truth for Coder Agents. NO CODE can be generated without it.*

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Platform GitOps | Section 1         |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | GitOps scope    | Section 1         |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A             | Section 3         |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | ArgoCD/SS       | Section 1         |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | N/A             | Section 1         |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | CLI verification | Section 7        |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | N/A (infra)     | Section 7         |
| Coverage Policy | Are goals defined as numbers (e.g. 100%)?      | Must     | N/A (infra)     | Section 7         |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | ArgoCD admin v1 | Section 4         |
| Data Protection | Encryption/access policies for sensitive data? | Must     | SealedSecrets   | Section 9         |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | Convergence goal | Section 8        |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A             | Section 8         |

### 0.3 Operations / Deployment / Monitoring

| Item           | Check Question                                           | Required | Alignment Notes | Where to document |
| -------------- | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments   | Are tiers (dev/staging/prod) clarified for this feature? | Must     | Local only      | Section 1         |
| Logging        | Required structured logs defined (fields, IDs)?          | Must     | ArgoCD events   | Section 9         |
| Monitoring     | Metrics and dashboards defined (RED/USE)?                | Must     | ArgoCD UI status | Section 9        |
| Alerts         | Are alert thresholds and routing defined?                | Must     | N/A (local)     | Section 9         |
| Backups        | Are backup policies defined for added data?              | Must     | N/A             | Section 9         |

---

## 1. Technical Overview & Architecture Style

This feature implements **GitOps for a single local cluster** using ArgoCD with an App-of-Apps pattern.

- **Component Boundary**:
  - Owns GitOps bootstrap artifacts under `gitops/`.
  - Owns vendored controller install manifests under `infrastructure/argocd/` and `infrastructure/sealed-secrets/`.
  - Does not own workload definitions beyond placeholders.
- **Key Dependencies**:
  - `specs/infra/spec.md` local cluster must exist before GitOps bootstrap.
  - Git repository hosting (GitHub).
- **Tech Stack**:
  - ArgoCD `v3.3.0` (vendored)
  - Sealed Secrets `v0.33.1` (vendored)
  - Kustomize directory sources

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-001** | Vendored ArgoCD install manifest pinned to v3.3.0 | High | REQ-PRD-FUN-01 |
| **REQ-SPC-002** | Vendored Sealed Secrets manifest pinned to v0.33.1 | High | REQ-PRD-FUN-02 |
| **REQ-SPC-003** | App-of-Apps structure exists under `gitops/clusters/local/` | High | REQ-PRD-FUN-03 |
| **SEC-SPC-001** | No plaintext Secret committed; sealed secret workflow required | Critical | REQ-PRD-FUN-05 |
| **REQ-SPC-004** | ArgoCD access via port-forward only | Medium | REQ-PRD-FUN-06 |
| **REQ-SPC-005** | ArgoCD Applications pin `targetRevision` to a SHA | High | REQ-PRD-FUN-03 |

## 3. Data Modeling & Storage Strategy

N/A. Desired state is stored in Git; live state is stored in Kubernetes.

## 4. Interfaces & Data Structures

### 4.1. Core Interfaces

- ArgoCD resources:
  - `Application` (root + children)
  - `AppProject` (local scope)
- SealedSecrets resources:
  - `SealedSecret` for ArgoCD repository credentials

### 4.2. AuthN / AuthZ (Required if protected data/actions)

- **Authentication**: ArgoCD local admin account for v1.
- **Authorization**: ArgoCD project boundaries (AppProject `local`) are used for scoping; multi-user RBAC is deferred.

## 5. Component Breakdown

- `infrastructure/argocd/argocd-install.yaml`: Vendored ArgoCD v3.3.0 install manifest.
- `infrastructure/sealed-secrets/sealed-secrets.yaml`: Vendored SealedSecrets v0.33.1 manifest.
- `gitops/clusters/local/root-application.yaml`: Root application (App-of-Apps).
- `gitops/clusters/local/apps/*.yaml`: Child applications (infra + apps).
- `gitops/clusters/local/10-infra/*/kustomization.yaml`: Kustomize entrypoints referencing `infrastructure/`.

## 6. Edge Cases & Error Handling

- **Private repo without credentials**: ArgoCD apps remain `Unknown`/`Degraded` until repo secret is applied.
- **SealedSecret applied before controller/CRD**: The CR will fail; re-apply after SealedSecrets is installed.
- **Pinned `targetRevision` drift**: New commits will not apply until the pinned SHA is updated intentionally.

## 7. Verification Plan (Testing & QA)

- **[VAL-SPC-001]** `kubectl kustomize` builds succeed for each GitOps Kustomize directory.
- **[VAL-SPC-002]** `kubectl apply --dry-run=client` succeeds for root and child Application manifests.
- **[VAL-SPC-003]** On a running cluster, ArgoCD and SealedSecrets pods are Ready.
- **[VAL-SPC-004]** ArgoCD apps converge to `Synced/Healthy` after repo secret is applied.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Performance / Latency**: GitOps convergence should complete within 5 minutes per sync on typical local hardware.
- **Throughput**: N/A.
- **Scalability Strategy**: App-of-Apps can be extended to ApplicationSet and multi-cluster later.

## 9. Operations & Observability

- **Deployment Strategy**:
  - Manual bootstrap for controllers (one-time), then GitOps reconciliation for infra/apps.
- **Monitoring & Alerts**:
  - ArgoCD UI is the primary operational view (`Synced/Healthy/Degraded`).
- **Logging**:
  - Rely on Kubernetes events and ArgoCD controller logs for troubleshooting.
- **Sensitive Data Handling**:
  - SSH deploy key is handled as a SealedSecret; no plaintext secret committed.
