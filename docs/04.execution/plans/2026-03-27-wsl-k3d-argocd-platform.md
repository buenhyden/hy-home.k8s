---
title: 'WSL k3d/k3s ArgoCD Platform Plan'
type: plan
status: complete
owner: platform-team
updated: 2026-05-22
---

# WSL k3d/k3s ArgoCD Platform Plan

## Overview (KR)

이 문서는 WSL2 기반 Kubernetes GitOps 플랫폼을 단계적으로 구축하기 위한 초기 실행 계획서다. 현재는 이후 `2026-03-28`, `2026-03-29`, 2026-05 hardening 작업에 흡수된 historical closure record로 유지한다.

## Context

문서 기반 요구사항/아키텍처/스펙 체계를 `04.execution`의 실행 계획·작업 증적으로 연결하고, 운영 문서는 `05.operations/{guides,policies,runbooks}`로 제공한다.

2026-05-22 구현 감사 기준으로 이 계획의 원래 범위는 현재 repo-backed desired state와 후속 실행 문서에 의해 닫혔다. 이 문서는 새 active execution 지시가 아니라 초기 baseline이 어디에서 구현·검증되는지 안내하는 이력 문서다.

## Goals & In-Scope

- **Goals**:
  - 멀티노드 k3d 클러스터 재현
  - ArgoCD GitOps 파이프라인 구축
  - ESO+Vault 및 외부 DB/Valkey 통합
  - 현재 문서 taxonomy에 맞춘 요구사항, 아키텍처, 스펙, 실행, 운영 문서 완성
- **In Scope**:
  - 선언형 매니페스트/헬름 값 설계
  - 보안 최소권한 및 네트워크 정책

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 프로덕션 DR 아키텍처
- **Out of Scope**:
  - 애플리케이션 기능 개발

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | 버전 freeze 및 환경 가정 검증 | `docs/90.references/versions/tech-stack-version-inventory.md`, `docs/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md` | REQ-PRD-FUN-01 | Current source-date inventory plus historical version evidence |
| PLN-002 | k3d 클러스터 및 ingress 설계 확정 | `infrastructure/k3d/k3d-cluster.yaml`, `infrastructure/argocd/values-local.yaml`, `gitops/apps/root/platform-ingress-nginx-app.yaml` | REQ-PRD-FUN-01/02 | `verify-contracts-static.sh`; live `verify-cluster.sh` / `verify-ingress-tls.sh` when requested |
| PLN-003 | ArgoCD Helm + App-of-Apps 설계 확정 | `gitops/clusters/local/root-application.yaml`, `gitops/apps/root/kustomization.yaml`, `infrastructure/argocd/values-local.yaml` | REQ-PRD-FUN-03/04 | `bash scripts/validate-gitops-structure.sh` |
| PLN-004 | ESO+Vault 및 외부 endpoint 계약 확정 | `gitops/platform/eso/`, `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/vault/policies/eso-read.hcl` | REQ-PRD-FUN-05/06/07 | `verify-contracts-static.sh`, `check-secret-handling.sh`; live ESO/Vault checks when requested |
| PLN-005 | 운영 가이드/정책/런북 작성 | `docs/05.operations/guides/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/` | REQ-PRD-FUN-09 | stage README links and repo quality gate |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Static | repo contract validation | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-002 | GitOps | App-of-Apps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-003 | Manifest | Kubernetes YAML syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-004 | Docs | lifecycle/template/link governance | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-005 | Live, operator-owned | k3d/ArgoCD/ESO runtime readiness | `bash infrastructure/tests/run-all.sh` | Run only when a live cluster is intentionally available |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 외부 Valkey 설정 키 차이 | High | Helm values 계약 문서화 + fallback 명시 |
| 고정 IP 충돌 | Medium | IPAM 표/사전 점검 체크리스트 운영 |
| Vault auth misconfig | High | runbook에 빠른 진단 절차 포함 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: 문서 링크/섹션 완결성 검사 통과
- **Sandbox / Canary Rollout**: 로컬 WSL 환경 1차 검증
- **Human Approval Gate**: 보안 정책 변경 전 승인
- **Rollback Trigger**: ArgoCD sync failure 반복/critical 보안 경보
- **Prompt / Model Promotion Criteria**: 작업 증적 완결 시 승격

## Completion Criteria

- [x] Scoped baseline work is mapped to current repo-backed implementation.
- [x] Static verification path is defined.
- [x] Required docs are linked to current contracts.

## Historical Closure Notes

- The unchecked draft criteria from this initial plan were stale after the later HA, platform expansion, and governance hardening work completed.
- The current implementation evidence is repository-static by default. Live `kubectl`, ArgoCD sync, Vault write, and Slack/send checks remain operator-owned and require intentional execution.
- Future platform changes should create or update the current active Spec/Plan/Task chain instead of reopening this historical baseline plan.

## Related Documents

- **PRD**: [`../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **ADR**: [`../../02.architecture/decisions/0001-k3d-topology-and-network.md`](../../02.architecture/decisions/0001-k3d-topology-and-network.md), [`../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md), [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md), [`../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)
- **Tasks**: [`../tasks/2026-03-27-wsl-k3d-argocd-platform.md`](../tasks/2026-03-27-wsl-k3d-argocd-platform.md)
