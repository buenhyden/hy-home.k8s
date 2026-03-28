# WSL2 k3d/k3s ArgoCD HA Platform Plan

## Overview (KR)

이 문서는 WSL2 환경에서 멀티노드 Kubernetes + GitOps + ESO/Vault + 외부 DB/Valkey 통합을 실행하기 위한 단계별 계획이다.

## Context

운영 중 확인된 병목(Vault external endpoint)을 기준으로 즉시 복구 절차와 구조 개선 백로그를 분리해 실행한다.

## Goals & In-Scope

- **Goals**:
  - 운영 핫픽스로 Vault-ESO 연동 즉시 복구
  - 인터페이스 계약 회귀 없이 ArgoCD 건강성 회복
  - 문서/검증 스크립트 기반 운영 표준 확립
- **In Scope**:
  - 사전 증적 수집
  - EndpointSlice 핫픽스
  - 상태 재평가 및 회귀 검증
  - README 인덱스 자동 동기화

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 외부 런타임 아키텍처 전면 재설계
- **Out of Scope**:
  - 외부 Vault/PostgreSQL/Valkey 배포 자동화

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Asset/버전 검증 결과 정리 | `docs/04.specs/002-.../spec.md` | REQ-PRD-FUN-01/02 | VAL-PLN-001 |
| PLN-002 | HA 토폴로지/자원/네트워크 설계 확정 | `docs/02.ard/0002-...md` | REQ-PRD-FUN-01/02 | VAL-PLN-002 |
| PLN-003 | GitOps 구조(App-of-Apps/ApplicationSet) 정리 | `docs/07.guides/0002-...md` | REQ-PRD-FUN-03 | VAL-PLN-003 |
| PLN-004 | ESO+Vault 연동/핫픽스 절차 문서화 | `docs/09.runbooks/0002-...md` | REQ-PRD-FUN-04/05 | VAL-PLN-004 |
| PLN-005 | Valkey EndpointSlice/네트워크 정책 보강 | `gitops/platform/external-services/valkey-external.yaml`, `gitops/platform/network-policies/*` | REQ-PRD-FUN-03A | VAL-PLN-004 |
| PLN-006 | AppProject/Vault policy 최소권한화 | `gitops/clusters/local/appproject-platform.yaml`, `infrastructure/vault/policies/eso-read.hcl` | REQ-PRD-FUN-05 | VAL-PLN-003 |
| PLN-007 | bootstrap/검증 스크립트 고도화 | `infrastructure/bootstrap-local.sh`, `infrastructure/tests/*.sh` | REQ-PRD-FUN-06 | VAL-PLN-005 |
| PLN-008 | 폴더별 README 인덱스 동기화 | `docs/01~09/*/README.md` | REQ-PRD-FUN-06 | VAL-PLN-006 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | 버전/계약 표 확인 | `rg -n 'k3s|k3d|Valkey|172.30.0.0/24' docs/04.specs/002-*/spec.md` | 필수 값 존재 |
| VAL-PLN-002 | Functional | 클러스터/앱 상태 점검 | `./infrastructure/tests/verify-cluster.sh && ./infrastructure/tests/verify-gitops.sh` | PASS |
| VAL-PLN-003 | Functional | Secret 연동 점검 | `./infrastructure/tests/verify-secrets.sh` | PASS |
| VAL-PLN-004 | Functional | 외부 서비스 계약 점검 | `./infrastructure/tests/verify-external-services.sh` | PASS |
| VAL-PLN-005 | Functional | 네트워크 정책 점검 | `./infrastructure/tests/verify-network-policies.sh` | PASS |
| VAL-PLN-006 | Structural | README 인덱스 반영 확인 | `rg -n '2026-03-28|0002-|002-' docs/0{1,2,3,4,5,6,7,8,9}*/README.md` | 전 디렉터리 반영 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Vault endpoint 재변경으로 재장애 | High | Runbook 핫픽스 절차/검증 명령 상시 유지 |
| WSL 자원 부족 | Medium | ARD에 자원 권장치 명시 및 모니터링 |
| 문서-실제 상태 괴리 | High | Task 기반 증적 업데이트 룰 강제 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: 문서/스크립트 정적 검증 통과
- **Sandbox / Canary Rollout**: WSL 로컬 클러스터에서만 선검증
- **Human Approval Gate**: 운영 endpoint/policy 변경 승인
- **Rollback Trigger**: `vault-backend Ready=False` 재발
- **Prompt / Model Promotion Criteria**: 재현 가능한 PASS 증적 확보

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **PRD**: [`../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **ADR**: [`../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
