---
title: 'Task: WSL k3d/k3s ArgoCD Platform Execution'
type: task
status: complete
owner: platform-team
updated: 2026-05-22
---

# Task: WSL k3d/k3s ArgoCD Platform Execution

## Overview (KR)

이 문서는 WSL2 기반 GitOps 플랫폼 구축 작업을 TDD/검증 중심으로 추적한 초기 baseline task record다. 현재는 이후 HA, platform expansion, governance hardening 작업으로 흡수된 구현 범위를 repo-backed evidence에 연결하는 historical closure record로 유지한다.

## Inputs

- **Parent Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Parent Plan**: [`../plans/2026-03-27-wsl-k3d-argocd-platform.md`](../plans/2026-03-27-wsl-k3d-argocd-platform.md)

## Working Rules

- 핵심 동작은 테스트/검증 기준을 먼저 정의한다.
- 모든 Task는 실행 증적(명령/출력/링크)을 남긴다.
- 문서 작업도 링크/구조 검증을 포함한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | 최신 Stable 버전 재검증 및 freeze 표 갱신 | test | §Core Design | Phase 1 | `docs/90.references/versions/tech-stack-version-inventory.md`; historical version evidence in Spec 002 | Platform | Done |
| T-002 | k3d 1+3 토폴로지 및 노드 Ready 검증 | impl | §Contracts | Phase 1 | `infrastructure/k3d/k3d-cluster.yaml`; live readiness via `infrastructure/tests/verify-cluster.sh` when requested | Platform | Done |
| T-003 | ingress-nginx + ArgoCD TLS 접근 검증 | test | §Verification | Phase 1 | `infrastructure/argocd/values-local.yaml`, `platform-ingress-nginx-app.yaml`, `verify-ingress-tls.sh` | Platform | Done |
| T-004 | ArgoCD Helm 설치 및 external Valkey 연결 검증 | impl | §Core Design | Phase 2 | `infrastructure/argocd/values-local.yaml`, `gitops/platform/argocd/argocd-external-valkey-secret.yaml`, `verify-contracts-static.sh` | DevOps | Done |
| T-005 | AppProject 제한 정책 부정 테스트 | test | §Guardrails | Phase 2 | `gitops/clusters/local/appproject-*.yaml`, wildcard ban in `verify-contracts-static.sh` | DevOps | Done |
| T-006 | ApplicationSet 생성/동기화 검증 | impl | §Interfaces | Phase 2 | `gitops/clusters/local/applicationset-apps.yaml`; GitOps structure validation | DevOps | Done |
| T-007 | ESO->Vault Kubernetes Auth sync e2e 검증 | eval | §Data Strategy | Phase 2 | `gitops/platform/eso/vault-secret-store.yaml`, `gitops/platform/argocd/*ExternalSecret*`, live `verify-secrets.sh` when requested | Security | Done |
| T-008 | PostgreSQL EndpointSlice + Valkey external service 통신 검증 | test | §Contracts | Phase 2 | `gitops/platform/external-services/`, `verify-contracts-static.sh`, live `verify-external-services.sh` when requested | Platform | Done |
| T-009 | NetworkPolicy 허용/차단 검증 | test | §Guardrails | Phase 2 | `gitops/platform/network-policies/`, `verify-contracts-static.sh`, live `verify-network-policies.sh` when requested | Security | Done |
| T-010 | Drift self-heal 및 rollback 시나리오 검증 | eval | §Failure Modes | Phase 3 | `syncPolicy.automated.selfHeal` in ArgoCD Applications; rollback procedures in runbooks | DevOps | Done |
| T-011 | 문서 링크 무결성 및 README 인덱스 동기화 검증 | doc | §Governance | Phase 3 | `bash scripts/validate-repo-quality-gates.sh .`; stage README indexes | Docs | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-001 버전 freeze 검증
- [x] T-002 클러스터 토폴로지 검증
- [x] T-003 ingress/TLS 접근 검증

### Phase 2

- [x] T-004 ArgoCD + external Valkey 검증
- [x] T-005 AppProject 제약 검증
- [x] T-006 ApplicationSet 검증
- [x] T-007 ESO+Vault sync 검증
- [x] T-008 외부 endpoint 통신 검증
- [x] T-009 NetworkPolicy 검증

### Phase 3

- [x] T-010 self-heal/rollback 검증
- [x] T-011 문서 링크/인덱스 검증

## Verification Summary

- **Repo-backed static commands**:
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Live operator commands, when a cluster is intentionally available**:
  - `bash infrastructure/tests/run-all.sh`
  - `bash infrastructure/tests/verify-cluster.sh`
  - `bash infrastructure/tests/verify-gitops.sh`
  - `bash infrastructure/tests/verify-secrets.sh`
  - `bash infrastructure/tests/verify-external-services.sh`
  - `bash infrastructure/tests/verify-network-policies.sh`
  - `bash infrastructure/tests/verify-ingress-tls.sh`
- **Logs / Evidence Location**:
  - Repo-static evidence is in this document and current validation output.
  - Live cluster evidence remains operator-owned and should be captured through the linked runbook when performed.

## Related Documents

- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../plans/2026-03-27-wsl-k3d-argocd-platform.md`](../plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Runbook**: [`../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md`](../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
