---
title: 'Runbook: ArgoCD (Local)'
status: 'Active'
date: '2026-03-07'
owner: 'buenhyden'
tags:
  - runbook
  - gitops
layer: 'gitops'
---

# Runbook: ArgoCD (Local)

- **Status**: Active
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-07
- **layer:** gitops

**Overview (KR):** 로컬 환경의 ArgoCD 서비스 상태 확인 및 문제 해결을 위한 운영 가이드입니다.

*Note: This is strictly for operational context. It MUST follow the deterministic rules in `0381-runbooks-oncall.md`.*

---

## Canonical References

- [docs/ard/2026-03-07-argocd-gitops-ard.md](../ard/2026-03-07-argocd-gitops-ard.md)
- [docs/plans/2026-03-16-gitops-plan.md](../plans/2026-03-16-gitops-plan.md)

---

## 1. Service Overview & Ownership

- **Description**: ArgoCD GitOps controller for the local k3d cluster. v1 standard access is via `kubectl port-forward`.
- **Owner Team**: hy (self-managed)
- **Primary Contact**: hy

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Local k3d cluster | Platform | ArgoCD cannot run | `runbooks/services/local-k3d-wsl2.md` |
| kubectl | Tooling | Cannot port-forward/verify | N/A |
| Sealed Secrets (optional) | In-cluster | Private repo creds cannot be stored in Git | `runbooks/services/sealed-secrets-local.md` |

## 3. Observability & Dashboards

- **Primary Dashboard**: ArgoCD UI (port-forward)
- **SLIs**:
  - `kubectl -n argocd get pods` shows all pods `Ready`
  - `kubectl -n argocd get applications` shows expected apps `Healthy`
- **Useful commands**:
  - `kubectl -n argocd get pods`
  - `kubectl -n argocd get applications`
  - `kubectl -n argocd get events --sort-by=.lastTimestamp | tail -n 50`

## 4. Alerts & Common Failures

### Scenario A: Port-forward fails

- **Symptoms**: `kubectl -n argocd port-forward ...` errors or UI unreachable.
- **Investigation Steps**:
  1. `kubectl -n argocd get pods`
  2. `kubectl -n argocd get svc argocd-server -o wide`
- **Remediation Action**:
  - [ ] Reinstall (vendored): `kubectl apply -f infrastructure/argocd/argocd-install.yaml`
  - [ ] Retry port-forward: `kubectl -n argocd port-forward svc/argocd-server 8080:443`

### Scenario B: Applications stuck `Unknown` / repo not accessible

- **Symptoms**: Child apps show repository errors in ArgoCD UI.
- **Investigation Steps**:
  1. Confirm the repo credential secret exists in `argocd` namespace.
  2. If using SealedSecrets, confirm the sealed secret controller is healthy.
- **Remediation Action**:
  - [ ] Re-apply the sealed repo credential and resync applications.

## 5. Safe Rollback Procedure

- [ ] Stop GitOps reconciliation by deleting the root app: `kubectl -n argocd delete application local-root`
- [ ] Remove ArgoCD: `kubectl delete -f infrastructure/argocd/argocd-install.yaml`
- [ ] Clean namespace: `kubectl delete namespace argocd --ignore-not-found`

## 6. Data Safety Notes (If Stateful)

- ArgoCD stores configuration in Kubernetes resources (Secrets/ConfigMaps). Removing the namespace deletes ArgoCD state (intended for local use).

## 7. Escalation Path

1. **Primary On-Call**: hy
2. **Secondary Escalation**: N/A
3. **Management Escalation (SEV-1)**: N/A

## 8. Verification Steps (Post-Fix)

- [ ] `kubectl -n argocd get pods` shows all pods `Ready`
- [ ] `kubectl -n argocd port-forward svc/argocd-server 8080:443` works
