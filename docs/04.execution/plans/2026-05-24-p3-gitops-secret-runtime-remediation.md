---
title: 'P3 GitOps Secret Runtime Remediation Plan'
type: plan
status: done
owner: platform
updated: 2026-06-04
---

# P3 GitOps Secret Runtime Remediation Plan

## Overview

This document is the implementation plan for the user-approved subset of P3
ArgoCD, Vault, External Secrets, and secret/runtime boundary items deferred by
the Workspace Harness Gap Analysis. Changes are limited to a GitOps-first,
repo-backed approach; plaintext secret value output and direct `kubectl apply`,
`argocd app sync`, or `vault write` are not in the automatic execution scope of
this plan.

## Context

The pre-approval P3 items are preserved in the
[`../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md`](../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md)
audit reference. Safety boundaries remain after approval: improve repository
desired state and static validation first, and inspect live state only through
read-only commands.

## Goals & In-Scope

- **Goals**:
  - Explicitly add DNS and Kubernetes API egress to the ESO controller egress policy.
  - Add the ArgoCD Notifications path to the Vault ESO read policy with least privilege.
  - Align the apps AppProject and sample app ExternalSecret contracts.
  - Add repository-backed root App-of-Apps child application paths for ArgoCD reconciliation of bootstrap-applied AppProject/ApplicationSet CRs.
  - Record static validation and approved read-only live validation results.
- **In Scope**:
  - `gitops/platform/network-policies/`
  - `infrastructure/vault/policies/`
  - `gitops/clusters/local/`
  - `gitops/apps/root/`
  - `examples/sample-app/`
  - `infrastructure/tests/`
  - Related execution Plan/Task/README/progress evidence

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Reading or outputting secret values
  - Creating or modifying Vault KV values
  - direct cluster mutation
  - Forcing ArgoCD sync
  - Changing CI/CD policy
- **Out of Scope**:
  - Issuing or rotating Slack tokens
  - Changing the PostgreSQL/Valkey/Vault data plane
  - GitHub Actions SHA pinning follow-up
  - `.claude/settings.local.json` precedence hardening

## Work Breakdown

| Task       | Description                                              | Files / Docs Affected                                                            | Target REQ            | Validation Criteria                              |
| ---------- | -------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------ |
| P3-PLN-001 | Record approved P3 execution plan and task evidence      | this plan, linked task, README indexes                                           | REQ-P3-TRACE          | repo quality gate PASS                           |
| P3-PLN-002 | Add ESO DNS/API egress to NetworkPolicy                  | `external-secrets-egress-to-vault.yaml`, static tests                            | REQ-P3-ESO-EGRESS     | manifest validation and static contract PASS     |
| P3-PLN-003 | Add Vault notifications path to ESO read policy          | `eso-read.hcl`, static tests                                                     | REQ-P3-VAULT-NOTIF    | no wildcard policy and static contract PASS      |
| P3-PLN-004 | Align apps AppProject and sample ExternalSecret contract | `appproject-apps.yaml`, `examples/sample-app/external-secret.yaml`, static tests | REQ-P3-APP-ESO        | AppProject allow-list and sample key checks PASS |
| P3-PLN-005 | Add ArgoCD-owned cluster config app path                 | `gitops/apps/root`, `gitops/clusters/local`, static tests                        | REQ-P3-ARGO-OWNERSHIP | GitOps structure and contract checks PASS        |
| P3-PLN-006 | Run approved repo-static and read-only runtime checks    | validation scripts, `kubectl get`/`describe` only                                | REQ-P3-VERIFY         | results recorded without secret values           |

## Verification Plan

| ID         | Level              | Description                                                  | Command / How to Run                                   | Pass Criteria                          |
| ---------- | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------ | -------------------------------------- |
| VAL-P3-001 | Docs               | Repository quality and docs governance                       | `bash scripts/validate-repo-quality-gates.sh .`        | PASS                                   |
| VAL-P3-002 | GitOps             | Root apps and Kustomize structure                            | `bash scripts/validate-gitops-structure.sh`            | PASS                                   |
| VAL-P3-003 | Manifests          | YAML syntax and optional kube-linter                         | `bash scripts/validate-k8s-manifests.sh .`             | PASS or optional-tool skip recorded    |
| VAL-P3-004 | Secrets            | Plaintext secret pattern scan                                | `bash scripts/check-secret-handling.sh .`              | PASS                                   |
| VAL-P3-005 | Static contract    | Platform static contracts                                    | `bash infrastructure/tests/verify-contracts-static.sh` | PASS                                   |
| VAL-P3-006 | NetworkPolicy live | ESO NetworkPolicy exists and controller Pods are visible     | read-only `kubectl get`/`describe`                     | no secret values; result recorded      |
| VAL-P3-007 | ESO/Vault live     | ClusterSecretStore and ExternalSecret readiness metadata     | read-only `kubectl get` jsonpath                       | no Secret data output; result recorded |
| VAL-P3-008 | ArgoCD live        | Root/platform apps, AppProjects, and ApplicationSet metadata | read-only `kubectl get`                                | no sync/mutation; result recorded      |
| VAL-P3-009 | Hygiene            | Whitespace sanity                                            | `git diff --check`                                     | PASS                                   |

## Risks & Mitigations

| Risk                                                      | Impact   | Mitigation                                                                                                                      |
| --------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------- |
| AppProject self-management can block first reconciliation | High     | Keep bootstrap-local initial AppProject apply as break-glass/bootstrap exception; add root child app for steady-state ownership |
| Vault policy widening grants too much access              | High     | Add only `platform/notifications` data/metadata paths; reject wildcards in static test                                          |
| ExternalSecret app examples expose secret values          | Critical | Keep examples reference-only and run secret scanner                                                                             |
| Live checks leak secret values                            | Critical | Use only status/metadata commands; never print Kubernetes Secret data or Vault KV values                                        |
| Local cluster is not running                              | Medium   | Record live checks as skipped/failed-current-state and keep repo-static validation authoritative for the commit                 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: full repo-static validation bundle must pass.
- **Sandbox / Canary Rollout**: not applicable in this repository-only pass.
- **Human Approval Gate**: already granted for P3 ArgoCD/Vault/ESO/secret/runtime scope; direct mutation still remains out of automated scope.
- **Rollback Trigger**: revert the P3 manifest/test/docs change set if static validation fails or live metadata checks reveal an incompatible ownership model.
- **Prompt / Model Promotion Criteria**: not applicable.

## Implementation Results

| Work item                                     | Result                                                                                                           | Evidence path                                                                                   |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| ESO NetworkPolicy egress                      | Added explicit DNS and Kubernetes API egress while preserving Vault egress                                       | `gitops/platform/network-policies/external-secrets-egress-to-vault.yaml`                        |
| Vault notifications policy                    | Added least-privilege `platform/notifications` data and metadata reads                                           | `infrastructure/vault/policies/eso-read.hcl`                                                    |
| AppProject and sample ExternalSecret contract | Allowed app `ExternalSecret` resources and corrected sample `remoteRef.key` semantics                            | `gitops/clusters/local/appproject-apps.yaml`, `examples/sample-app/external-secret.yaml`        |
| Cluster-local ownership                       | Added `platform-cluster-config` root child app and cluster-local kustomization for AppProject/ApplicationSet CRs | `gitops/apps/root/platform-cluster-config-app.yaml`, `gitops/clusters/local/kustomization.yaml` |
| Static validation                             | Added static contract checks for all implemented P3 contracts                                                    | `infrastructure/tests/verify-contracts-static.sh`                                               |
| Operations docs                               | Clarified Vault CLI path versus ESO `remoteRef.key` behavior                                                     | `docs/05.operations/`, `examples/sample-app/README.md`                                          |

## Verification Results

| ID         | Result                  | Evidence / Note                                                                                                           |
| ---------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| VAL-P3-001 | PASS                    | `bash scripts/validate-repo-quality-gates.sh .` passed                                                                    |
| VAL-P3-002 | PASS                    | `bash scripts/validate-gitops-structure.sh` passed; root app manifest count is 18                                         |
| VAL-P3-003 | PASS with optional skip | `bash scripts/validate-k8s-manifests.sh .` passed YAML syntax; optional `kube-linter` is not installed locally            |
| VAL-P3-004 | PASS                    | `bash scripts/check-secret-handling.sh .` passed                                                                          |
| VAL-P3-005 | PASS                    | `bash infrastructure/tests/verify-contracts-static.sh` passed                                                             |
| VAL-P3-006 | CURRENT-STATE FAIL      | `kubectl -n external-secrets get ...` could not reach `https://0.0.0.0:6550`; API server refused connection               |
| VAL-P3-007 | CURRENT-STATE FAIL      | ClusterSecretStore and ExternalSecret readiness metadata could not be read because the local cluster was not reachable    |
| VAL-P3-008 | CURRENT-STATE FAIL      | ArgoCD Application, ApplicationSet, and AppProject metadata could not be read because the local cluster was not reachable |
| VAL-P3-009 | PASS                    | `git diff --check` passed after final doc updates                                                                         |

## Runtime Check Interpretation

The read-only live check was approved and attempted, but the current WSL runtime
has no reachable `k3d-hyhome` API server: `kubectl config current-context`
returned `k3d-hyhome`, while all resource reads failed against
`https://0.0.0.0:6550` with connection refused. `docker ps` listed no running
containers and `k3d cluster list` returned no cluster rows. This is recorded as
a current-state runtime unavailability, not as live validation success.

## Completion Criteria

- [x] P3 plan/task evidence created and indexed.
- [x] ESO NetworkPolicy DNS/API egress committed.
- [x] Vault notifications path policy committed.
- [x] apps AppProject ExternalSecret and sample remoteRef contract aligned.
- [x] cluster-local AppProject/ApplicationSet steady-state ownership path added.
- [x] static validation passed.
- [x] approved read-only runtime validation attempted and recorded.

## Remaining Follow-up

- Start `k3d-hyhome` and rerun metadata-only ESO, ArgoCD, AppProject, and
  ApplicationSet checks after ArgoCD has reconciled the root app.
- Confirm whether `platform-cluster-config` needs a one-time bootstrap handoff
  on existing clusters where the current AppProject policy predates this commit.
- Keep Vault KV writes, ArgoCD sync, and `kubectl apply` as explicit
  human-approved operations outside this repository-only commit.

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Audit Reference**: [../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md](../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md)
- **Tasks**: [../tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md](../tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Policy**: [../../05.operations/policies/0007-app-gitops-onboarding-policy.md](../../05.operations/policies/0007-app-gitops-onboarding-policy.md)
- **Runbook**: [../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
