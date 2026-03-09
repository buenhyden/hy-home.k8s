# Service Runbook: Sealed Secrets (Local)

*Target Directory: `runbooks/services/sealed-secrets-local.md`*
*Note: This is strictly for operational context. It MUST follow the deterministic rules in `0381-runbooks-oncall.md`.*

---

## 1. Service Overview & Ownership

- **Description**: Bitnami Sealed Secrets controller used to store sensitive Kubernetes Secrets in Git as encrypted `SealedSecret` resources for the local k3d cluster.
- **Owner Team**: hy (self-managed)
- **Primary Contact**: hy

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Local k3d cluster | Platform | Cannot unseal secrets | `runbooks/services/local-k3d-wsl2.md` |
| kubectl | Tooling | Cannot apply/verify resources | N/A |

## 3. Observability & Dashboards

- **Primary Dashboard**: N/A (local environment)
- **SLIs**:
  - `kubectl -n kube-system get pods -l name=sealed-secrets-controller` shows `Ready`
  - Applying a `SealedSecret` results in a generated `Secret`
- **Useful commands**:
  - `kubectl -n kube-system get pods -l name=sealed-secrets-controller`
  - `kubectl get sealedsecrets -A`
  - `kubectl get secrets -A | rg -n argocd`

## 4. Alerts & Common Failures

### Scenario A: Controller not running

- **Symptoms**: `SealedSecret` resources never produce a `Secret`.
- **Investigation Steps**:
  1. `kubectl -n kube-system get pods -l name=sealed-secrets-controller`
  2. `kubectl -n kube-system logs deploy/sealed-secrets-controller --tail=200`
- **Remediation Action**:
  - [ ] Re-apply vendored manifest: `kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml`
  - [ ] Verify pod becomes `Ready`

### Scenario B: SealedSecret fails to unseal (status shows error)

- **Symptoms**: `kubectl get sealedsecret -n <ns> <name> -o yaml` shows an error condition.
- **Investigation Steps**:
  1. Confirm the `SealedSecret` was sealed against the current controller certificate (see `kubeseal --fetch-cert` workflow).
  2. Check controller logs: `kubectl -n kube-system logs deploy/sealed-secrets-controller --tail=200`
- **Remediation Action**:
  - [ ] Re-seal with the current cluster cert and re-apply the `SealedSecret`.

## 5. Safe Rollback Procedure

- [ ] Remove affected sealed secret: `kubectl delete sealedsecret -n <ns> <name>`
- [ ] (Optional) Remove controller: `kubectl delete -f infrastructure/sealed-secrets/sealed-secrets.yaml`

## 6. Data Safety Notes (If Stateful)

- SealedSecrets holds encryption keys inside the cluster. Deleting the controller and keys can make previously sealed secrets unrecoverable without re-sealing.

## 7. Escalation Path

1. **Primary On-Call**: hy
2. **Secondary Escalation**: N/A
3. **Management Escalation (SEV-1)**: N/A

## 8. Verification Steps (Post-Fix)

- [ ] `kubectl -n kube-system get pods -l name=sealed-secrets-controller` shows pod `Ready`
- [ ] A test `SealedSecret` produces a corresponding `Secret`
