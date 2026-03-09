# Service Runbook: Local GitOps (ArgoCD App-of-Apps)

*Target Directory: `runbooks/services/local-gitops-argocd.md`*
*Note: This is strictly for operational context. It MUST follow the deterministic rules in `0381-runbooks-oncall.md`.*

---

## 1. Service Overview & Ownership

- **Description**: Deterministic bootstrap and operations for local GitOps using ArgoCD App-of-Apps and Sealed Secrets for repo credentials.
- **Owner Team**: hy (self-managed)
- **Primary Contact**: hy

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Local k3d cluster | Platform | GitOps cannot reconcile | `runbooks/services/local-k3d-wsl2.md` |
| Sealed Secrets | In-cluster | Sealed repo creds cannot be applied | `runbooks/services/sealed-secrets-local.md` |
| ArgoCD | In-cluster | GitOps controller unavailable | `runbooks/services/argocd-local.md` |

## 3. Observability & Dashboards

- **Primary Dashboard**: ArgoCD UI (via port-forward)
- **SLIs**:
  - Root app exists: `kubectl -n argocd get application local-root`
  - Child apps converge: `kubectl -n argocd get applications`
  - Infra controllers healthy (MetalLB, ingress-nginx)
- **Useful commands**:
  - `kubectl -n argocd get applications`
  - `kubectl -n argocd describe application local-root`
  - `kubectl -n metallb-system get pods`
  - `kubectl -n ingress-nginx get pods`

## 4. Alerts & Common Failures

### Scenario A: First-time bootstrap (private repo + sealed creds)

- **Symptoms**: ArgoCD apps show repo auth failures.
- **Investigation Steps**:
  1. Ensure SealedSecrets controller is `Ready` (kube-system).
  2. Ensure repo credential sealed secret has been applied to `argocd` namespace.
  3. Ensure `gitops/clusters/local/root-application.yaml` has correct `repoURL` and `targetRevision`.
- **Remediation Action**:
  - [ ] Install SealedSecrets: `kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml`
  - [ ] Install ArgoCD: `kubectl apply -f infrastructure/argocd/argocd-install.yaml`
  - [ ] Apply your sealed repo credential (generated via `kubeseal`)
  - [ ] Apply root app: `kubectl apply -f gitops/clusters/local/root-application.yaml`

### Scenario B: Changes not reflected (pinned targetRevision)

- **Symptoms**: New commits in Git do not change cluster state.
- **Investigation Steps**:
  1. Check `targetRevision` in `gitops/clusters/local/*.yaml`.
- **Remediation Action**:
  - [ ] Update `targetRevision` to the desired SHA and sync.

## 5. Safe Rollback Procedure

- [ ] Roll back by reverting Git to a previous known-good revision, then set `targetRevision` back to that SHA.
- [ ] If immediate stop is required: delete the root app to halt reconciliation:
  - `kubectl -n argocd delete application local-root`

## 6. Data Safety Notes (If Stateful)

- GitOps changes are declarative and can remove resources with `prune=true`. Ensure you understand resource ownership before introducing stateful workloads.

## 7. Escalation Path

1. **Primary On-Call**: hy
2. **Secondary Escalation**: N/A
3. **Management Escalation (SEV-1)**: N/A

## 8. Verification Steps (Post-Fix)

- [ ] `kubectl -n argocd get applications` shows expected apps `Healthy`
- [ ] `kubectl -n metallb-system get pods` all `Running`
- [ ] `kubectl -n ingress-nginx get pods` controller `Ready`
- [ ] `curl -I http://127.0.0.1:18080/` returns HTTP (2xx–4xx)
