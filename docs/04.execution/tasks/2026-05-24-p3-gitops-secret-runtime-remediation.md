---
title: 'Task: P3 GitOps Secret Runtime Remediation'
type: task
status: complete
owner: platform
updated: 2026-05-24
---

# Task: P3 GitOps Secret Runtime Remediation

## Overview (KR)

이 문서는 승인된 P3 ArgoCD, Vault, ESO, secret/runtime remediation의 구현·검증
작업 목록이다. 작업은 GitOps repository desired state와 read-only runtime metadata
검증으로 제한하며, secret 값 출력과 live mutation은 금지한다.

## Inputs

- **Parent Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Parent Plan**: [../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md](../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Source Gap Plan**: [../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md](../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md)

## Working Rules

- Use `gitops-workflow`, `k8s-security-audit`, and `k8s-validate`.
- Do not print or inspect secret values.
- Do not run `kubectl apply`, `kubectl patch`, `argocd app sync`, `vault write`,
  or `vault kv` mutation commands in this task.
- Make repository-backed changes first, then run static validation.
- Read-only runtime checks may inspect metadata/status only.

## Task Table

| Task ID         | Description                                                              | Type   | Parent Spec / Section             | Parent Plan / Phase | Validation / Evidence                           | Owner    | Status |
| --------------- | ------------------------------------------------------------------------ | ------ | --------------------------------- | ------------------- | ----------------------------------------------- | -------- | ------ |
| P3-GITOPS-T-001 | Create approved P3 plan/task evidence and indexes                        | doc    | VAL-SPC-006 / P3 deferrals        | P3-PLN-001          | repo quality gate                               | Platform | Done   |
| P3-GITOPS-T-002 | Add ESO DNS/API egress policy coverage                                   | impl   | GitOps deferred items             | P3-PLN-002          | static contract and manifest validation         | Platform | Done   |
| P3-GITOPS-T-003 | Add Vault notifications read policy coverage                             | impl   | Vault deferred items              | P3-PLN-003          | static contract and secret scan                 | Platform | Done   |
| P3-GITOPS-T-004 | Align apps AppProject ExternalSecret permission and sample remoteRef key | impl   | App onboarding deferred items     | P3-PLN-004          | static contract and manifest validation         | Platform | Done   |
| P3-GITOPS-T-005 | Add ArgoCD-owned cluster-local config app path                           | impl   | Bootstrap ownership deferred item | P3-PLN-005          | GitOps structure and static contract validation | Platform | Done   |
| P3-GITOPS-T-006 | Run repo-static validation bundle                                        | test   | Verification                      | P3-PLN-006          | verification summary                            | Platform | Done   |
| P3-GITOPS-T-007 | Run approved read-only runtime metadata checks                           | eval   | Verification                      | P3-PLN-006          | live metadata summary without secret values     | Platform | Done   |
| P3-GITOPS-T-008 | Append progress memory                                                   | memory | Memory Strategy                   | P3-PLN-001          | progress entry                                  | Platform | Done   |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `guardrail`
- `memory`
- `eval`

## Phase View

### Phase 1 - Traceability

- [x] P3-GITOPS-T-001 Create approved P3 plan/task evidence and indexes.

### Phase 2 - Repository Desired State

- [x] P3-GITOPS-T-002 Add ESO DNS/API egress policy coverage.
- [x] P3-GITOPS-T-003 Add Vault notifications read policy coverage.
- [x] P3-GITOPS-T-004 Align apps AppProject ExternalSecret permission and sample remoteRef key.
- [x] P3-GITOPS-T-005 Add ArgoCD-owned cluster-local config app path.

### Phase 3 - Verification

- [x] P3-GITOPS-T-006 Run repo-static validation bundle.
- [x] P3-GITOPS-T-007 Run approved read-only runtime metadata checks.
- [x] P3-GITOPS-T-008 Append progress memory.

## Implementation Decisions

| Decision                                                               | Evidence path                                                                                   | Rationale                                                                                              | Rollback                                                                       |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Keep all P3 implementation repo-backed                                 | `gitops/`, `infrastructure/`, `examples/`, `docs/`                                              | Preserves GitOps-first operation and avoids direct cluster mutation                                    | Revert this task's manifest, policy, test, and doc changes                     |
| Add DNS and Kubernetes API egress to ESO NetworkPolicy                 | `gitops/platform/network-policies/external-secrets-egress-to-vault.yaml`                        | ESO needs Vault, DNS, and API-server reachability while keeping egress explicit                        | Revert the added `to`/`ports` entries                                          |
| Add only the notifications Vault path                                  | `infrastructure/vault/policies/eso-read.hcl`                                                    | Keeps the ArgoCD Notifications secret path least-privilege and avoids wildcard expansion               | Remove the `platform/notifications` data/metadata policy blocks                |
| Align sample app `remoteRef.key` with ClusterSecretStore path behavior | `examples/sample-app/external-secret.yaml`                                                      | `vault kv put secret/apps/...` maps to ESO `remoteRef.key: apps/...` when the store path is `secret`   | Restore the previous sample key and related docs if the store contract changes |
| Add a root child app for cluster-local ArgoCD config                   | `gitops/apps/root/platform-cluster-config-app.yaml`, `gitops/clusters/local/kustomization.yaml` | Gives steady-state GitOps ownership to AppProject/ApplicationSet bootstrap CRs after initial bootstrap | Remove the child app and cluster-local kustomization from the root app set     |

## Verification Summary

| Command or method                                                                       | Result                  | Evidence / Note                                                                                                     |
| --------------------------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `bash scripts/validate-repo-quality-gates.sh .`                                         | PASS                    | Repository quality gates passed                                                                                     |
| `bash scripts/generate-llm-wiki-index.sh --check`                                       | PASS                    | LLM wiki index current                                                                                              |
| `bash scripts/validate-gitops-structure.sh`                                             | PASS                    | Root app manifest count is 18; root and cluster-local kustomizations passed                                         |
| `bash scripts/validate-k8s-manifests.sh .`                                              | PASS with optional skip | YAML syntax passed; optional `kube-linter` is not installed locally                                                 |
| `bash scripts/check-secret-handling.sh .`                                               | PASS                    | No plaintext secret finding from the repo scanner                                                                   |
| `bash infrastructure/tests/verify-contracts-static.sh`                                  | PASS                    | P3 static contracts for ESO egress, Vault policy, AppProjects, cluster-local ownership, and sample remoteRef passed |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +`     | PASS                    | Shell syntax passed                                                                                                 |
| `python3 -m json.tool .claude/settings.json`                                            | PASS                    | Runtime settings JSON parsed                                                                                        |
| `python3 -m json.tool .codex/hooks.json`                                                | PASS                    | Codex hook JSON parsed                                                                                              |
| `.env.example` vs `.env` key-name-only comparison                                       | PASS                    | Key names match; values were not printed                                                                            |
| `git diff --check`                                                                      | PASS                    | Whitespace sanity passed after final doc updates                                                                    |
| `kubectl config current-context`                                                        | PASS                    | Current context is `k3d-hyhome`                                                                                     |
| Read-only `kubectl get` checks for ESO, ArgoCD, AppProject, and ApplicationSet metadata | CURRENT-STATE FAIL      | Kubernetes API `https://0.0.0.0:6550` refused connection; no live metadata could be read                            |
| `docker ps --format ...` and `k3d cluster list`                                         | CURRENT-STATE INFO      | No running containers were listed; `k3d cluster list` returned only the header                                      |

## Skipped or Deferred Verification

| Check                                       | Reason                                                 | Alternative evidence                                                   | Follow-up                                                                                                             |
| ------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| ArgoCD sync/health after new root child app | Direct ArgoCD sync/mutation is out of automated scope  | Static GitOps structure and contract checks passed                     | Start the local cluster, let ArgoCD reconcile, then run read-only `kubectl get app platform-cluster-config -n argocd` |
| ESO/Vault live readiness                    | Local `k3d-hyhome` API server was unavailable          | Static contracts and secret scanner passed without secret value output | Start the local cluster and run metadata-only ClusterSecretStore and ExternalSecret readiness checks                  |
| Vault KV value validation                   | Secret value inspection and Vault writes are forbidden | Vault policy path coverage is validated statically                     | Validate values only through ESO readiness metadata after the cluster is running                                      |

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md](../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Source Plan**: [../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md](../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md)
- **GitOps README**: [../../../gitops/README.md](../../../gitops/README.md)
- **Vault Policy**: [../../../infrastructure/vault/policies/eso-read.hcl](../../../infrastructure/vault/policies/eso-read.hcl)
