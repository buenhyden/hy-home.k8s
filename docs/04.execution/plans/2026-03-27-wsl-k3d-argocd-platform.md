# WSL k3d/k3s ArgoCD Platform Plan

## Overview (KR)

이 문서는 WSL2 기반 Kubernetes GitOps 플랫폼을 단계적으로 구축하기 위한 실행 계획서다. 구성 순서, 검증 게이트, 리스크 완화를 포함한다.

## Context

문서 기반 설계(01~04)를 실제 실행 가능한 작업(06)으로 연결하고 운영 문서(07~09)까지 일관되게 제공한다.

## Goals & In-Scope

- **Goals**:
  - 멀티노드 k3d 클러스터 재현
  - ArgoCD GitOps 파이프라인 구축
  - ESO+Vault 및 외부 DB/Valkey 통합
  - 01~09 문서 완성
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
| PLN-001 | 버전 freeze 및 환경 가정 검증 | `docs/04.execution/tasks/...` | REQ-PRD-FUN-01 | VAL-PLN-001 |
| PLN-002 | k3d 클러스터 및 ingress 설계 확정 | `docs/03.specs/...` | REQ-PRD-FUN-01/02 | VAL-PLN-002 |
| PLN-003 | ArgoCD Helm + App-of-Apps 설계 확정 | `docs/02.architecture/decisions/0002...` | REQ-PRD-FUN-03/04 | VAL-PLN-003 |
| PLN-004 | ESO+Vault 및 외부 endpoint 계약 확정 | `docs/02.architecture/decisions/0003...`, `0004...` | REQ-PRD-FUN-05/06/07 | VAL-PLN-004 |
| PLN-005 | 운영 가이드/정책/런북 작성 | `docs/07~09/...` | REQ-PRD-FUN-09 | VAL-PLN-005 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | 문서/버전 기준 확인 | `rg -n "v1.35.0\+k3s1\|v5.8.3\|9.0.1" docs` | 필수 버전 표기 존재 |
| VAL-PLN-002 | Structural | 링크 무결성 점검 | `rg -n "\]\(\.\./" docs/0{1,2,3,4,5,6,7,8,9}*` | 상대 링크 누락 없음 |
| VAL-PLN-003 | Functional | Task 검증 항목 포함 여부 | `rg -n "Task-00\|VAL-" docs/04.execution/tasks/*.md` | TDD/검증 항목 존재 |

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

- [ ] Scoped work completed
- [ ] Verification passed
- [ ] Required docs updated

## Related Documents

- **PRD**: [`../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **ADR**: [`../02.architecture/decisions/0001-k3d-topology-and-network.md`](../../02.architecture/decisions/0001-k3d-topology-and-network.md), [`../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md), [`../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md), [`../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)
