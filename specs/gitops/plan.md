---
goal: "Bootstrap ArgoCD GitOps for the local k3d cluster (infra + apps) with sealed secrets for private repo access."
version: "1.0"
date_created: "2026-02-27"
last_updated: "2026-02-27"
owner: "hy"
status: "Planned"
tags: ["implementation", "planning", "gitops", "argocd", "sealed-secrets"]
stack: "node"
---

# GitOps (ArgoCD) Implementation Plan

*Target Directory: `specs/gitops/plan.md`*

## 1. Context & Introduction

This plan implements GitOps for the local WSL2 + k3d cluster using ArgoCD and Sealed Secrets. It complements `specs/infra/` by adding:

- ArgoCD installation (vendored manifest, pinned)
- Sealed Secrets controller (vendored manifest, pinned)
- App-of-Apps GitOps layout (`gitops/` directory)
- Private repository access via SSH deploy key sealed into Git

## 2. Goals & In-Scope

- **Goals:**
  - Deterministic manual bootstrap for ArgoCD + SealedSecrets on the local cluster.
  - GitOps reconciliation for Infra (`gitops/clusters/local/10-infra`) and Apps (`gitops/clusters/local/90-apps`).
  - No plaintext secret commits (SealedSecrets workflow required).
- **In-Scope (Scope of this Plan):**
  - Vendoring ArgoCD and Sealed Secrets manifests.
  - AppProject + Applications (App-of-Apps).
  - Runbooks for bootstrap, repo credential sealing, and rollback.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Multi-cluster GitOps or ApplicationSet fleet management.
  - ArgoCD exposure via Ingress/NodePort.
- **Out-of-Scope:**
  - External Secrets Operator / Vault integration.
  - SSO/RBAC beyond default local admin workflow.

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-GITOPS-001]`: ArgoCD install manifest is vendored and pinned (v3.3.0).
  - `[REQ-GITOPS-002]`: Sealed Secrets controller manifest is vendored and pinned (v0.33.1).
  - `[REQ-GITOPS-003]`: App-of-Apps root Application exists and manages child Applications.
  - `[REQ-GITOPS-004]`: Child Applications use `automated` sync with `prune=true` and `selfHeal=true`.
  - `[REQ-GITOPS-005]`: Private repo access uses SSH deploy key stored as SealedSecret (no plaintext Secret committed).
  - `[SEC-GITOPS-001]`: No plaintext Kubernetes Secrets are committed under `gitops/`.
  - `[REQ-GITOPS-006]`: `targetRevision` is pinned to a specific tag/SHA.
- **Constraints:**
  - Bootstrap has an unavoidable manual sequence (ArgoCD cannot read a private repo without credentials).

## 5. Work Breakdown (Tasks & Traceability)

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Vendor ArgoCD install manifest | `infrastructure/argocd/argocd-install.yaml` | [REQ-GITOPS-001] | File exists; pinned version recorded |
| TASK-002 | Vendor Sealed Secrets manifest | `infrastructure/sealed-secrets/sealed-secrets.yaml` | [REQ-GITOPS-002] | File exists; pinned version recorded |
| TASK-003 | Add App-of-Apps structure | `gitops/clusters/local/*` | [REQ-GITOPS-003] | Root app creates child Applications |
| TASK-004 | Add runbooks for bootstrap + sealing | `runbooks/services/*` | [REQ-GITOPS-005] | Operators can follow without guessing |
| TASK-005 | Update documentation links/traceability | `README.md`, `infrastructure/README.md`, `OPERATIONS.md` | [REQ-GITOPS-003] | Links correct; no drift |

## 6. Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Local | Kustomize build for GitOps paths | `kubectl kustomize gitops/clusters/local/10-infra/metallb-install` | No errors |
| VAL-PLN-002 | Local | Root Application manifest syntax | `kubectl apply --dry-run=client -f gitops/clusters/local/root-application.yaml` | No errors |
| VAL-PLN-003 | Cluster | ArgoCD pods ready | `kubectl -n argocd get pods` | All Ready |
| VAL-PLN-004 | Cluster | Child Apps Synced/Healthy | ArgoCD UI / `kubectl -n argocd get applications` | All `Healthy` |
| VAL-PLN-005 | Security | No plaintext secrets committed | `rg -n \"kind: Secret\" gitops/` | No sensitive Secrets committed |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Bootstrap chicken/egg (private repo) | High | Install controllers manually, then apply sealed repo secret, then root app |
| `targetRevision` pin overhead | Medium | Document a deterministic bump procedure (update SHA intentionally) |
| ArgoCD version quirks | Medium | Vendor pinned version; upgrade via ADR if required |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/gitops/argocd-gitops-prd.md`
- **Spec**: `specs/gitops/spec.md`
- **ADR**: `docs/adr/gitops/0001-argocd-gitops.md`
