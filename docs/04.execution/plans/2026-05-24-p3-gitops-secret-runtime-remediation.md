---
title: 'P3 GitOps Secret Runtime Remediation Plan'
type: plan
status: active
owner: platform
updated: 2026-05-24
---

# P3 GitOps Secret Runtime Remediation Plan

## Overview (KR)

이 문서는 Workspace Harness Gap Analysis에서 P3로 보류했던 ArgoCD, Vault,
External Secrets, secret/runtime 경계 항목 중 사용자가 승인한 범위의 실행 계획이다.
변경은 GitOps-first repo-backed 방식으로 제한하며, plaintext secret 값 출력이나
직접 `kubectl apply`, `argocd app sync`, `vault write`는 이 계획의 자동 실행 범위가
아니다.

## Context

승인 전 P3 항목은 `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`에
deferred 상태로 남아 있었다. 승인 후에도 안전 경계는 유지한다: repository desired
state와 정적 검증을 먼저 보강하고, live 상태는 read-only 명령으로만 확인한다.

## Goals & In-Scope

- **Goals**:
  - ESO controller egress policy에 DNS와 Kubernetes API egress를 명시한다.
  - Vault ESO read policy에 ArgoCD Notifications 경로를 least-privilege로 추가한다.
  - apps AppProject와 sample app ExternalSecret 계약을 일치시킨다.
  - bootstrap-applied AppProject/ApplicationSet CR의 ArgoCD reconciliation 경로를
    repository-backed root App-of-Apps 하위 앱으로 보강한다.
  - static validation과 승인된 read-only live validation 결과를 기록한다.
- **In Scope**:
  - `gitops/platform/network-policies/`
  - `infrastructure/vault/policies/`
  - `gitops/clusters/local/`
  - `gitops/apps/root/`
  - `examples/sample-app/`
  - `infrastructure/tests/`
  - 관련 execution Plan/Task/README/progress evidence

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - secret 값 조회 또는 출력
  - Vault KV 값 생성/수정
  - direct cluster mutation
  - ArgoCD sync 강제 실행
  - CI/CD policy 변경
- **Out of Scope**:
  - Slack token 발급/교체
  - PostgreSQL/Valkey/Vault 데이터 플레인 변경
  - GitHub Actions SHA pinning follow-up
  - `.claude/settings.local.json` precedence hardening

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| P3-PLN-001 | Record approved P3 execution plan and task evidence | this plan, linked task, README indexes | REQ-P3-TRACE | repo quality gate PASS |
| P3-PLN-002 | Add ESO DNS/API egress to NetworkPolicy | `external-secrets-egress-to-vault.yaml`, static tests | REQ-P3-ESO-EGRESS | manifest validation and static contract PASS |
| P3-PLN-003 | Add Vault notifications path to ESO read policy | `eso-read.hcl`, static tests | REQ-P3-VAULT-NOTIF | no wildcard policy and static contract PASS |
| P3-PLN-004 | Align apps AppProject and sample ExternalSecret contract | `appproject-apps.yaml`, `examples/sample-app/external-secret.yaml`, static tests | REQ-P3-APP-ESO | AppProject allow-list and sample key checks PASS |
| P3-PLN-005 | Add ArgoCD-owned cluster config app path | `gitops/apps/root`, `gitops/clusters/local`, static tests | REQ-P3-ARGO-OWNERSHIP | GitOps structure and contract checks PASS |
| P3-PLN-006 | Run approved repo-static and read-only runtime checks | validation scripts, `kubectl get`/`describe` only | REQ-P3-VERIFY | results recorded without secret values |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P3-001 | Docs | Repository quality and docs governance | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-P3-002 | GitOps | Root apps and Kustomize structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-P3-003 | Manifests | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or optional-tool skip recorded |
| VAL-P3-004 | Secrets | Plaintext secret pattern scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-P3-005 | Static contract | Platform static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-P3-006 | NetworkPolicy live | ESO NetworkPolicy exists and controller Pods are visible | read-only `kubectl get`/`describe` | no secret values; result recorded |
| VAL-P3-007 | ESO/Vault live | ClusterSecretStore and ExternalSecret readiness metadata | read-only `kubectl get` jsonpath | no Secret data output; result recorded |
| VAL-P3-008 | ArgoCD live | Root/platform apps, AppProjects, and ApplicationSet metadata | read-only `kubectl get` | no sync/mutation; result recorded |
| VAL-P3-009 | Hygiene | Whitespace sanity | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| AppProject self-management can block first reconciliation | High | Keep bootstrap-local initial AppProject apply as break-glass/bootstrap exception; add root child app for steady-state ownership |
| Vault policy widening grants too much access | High | Add only `platform/notifications` data/metadata paths; reject wildcards in static test |
| ExternalSecret app examples expose secret values | Critical | Keep examples reference-only and run secret scanner |
| Live checks leak secret values | Critical | Use only status/metadata commands; never print Kubernetes Secret data or Vault KV values |
| Local cluster is not running | Medium | Record live checks as skipped/failed-current-state and keep repo-static validation authoritative for the commit |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: full repo-static validation bundle must pass.
- **Sandbox / Canary Rollout**: not applicable in this repository-only pass.
- **Human Approval Gate**: already granted for P3 ArgoCD/Vault/ESO/secret/runtime scope; direct mutation still remains out of automated scope.
- **Rollback Trigger**: revert the P3 manifest/test/docs change set if static validation fails or live metadata checks reveal an incompatible ownership model.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [ ] P3 plan/task evidence created and indexed.
- [ ] ESO NetworkPolicy DNS/API egress committed.
- [ ] Vault notifications path policy committed.
- [ ] apps AppProject ExternalSecret and sample remoteRef contract aligned.
- [ ] cluster-local AppProject/ApplicationSet steady-state ownership path added.
- [ ] static validation passed.
- [ ] approved read-only runtime validation attempted and recorded.

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Source Plan**: [./2026-05-24-workspace-harness-gap-analysis.md](./2026-05-24-workspace-harness-gap-analysis.md)
- **Tasks**: [../tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md](../tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Policy**: [../../05.operations/policies/0007-app-gitops-onboarding-policy.md](../../05.operations/policies/0007-app-gitops-onboarding-policy.md)
- **Runbook**: [../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
