# Task: WSL2 k3d/k3s ArgoCD HA Platform Execution

## Overview (KR)

이 문서는 인프라 컴포넌트별 TDD 검증 스크립트를 중심으로 실행 작업을 추적한다.

## Inputs

- **Parent Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Parent Plan**: [`../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)

## Working Rules

- RED: 먼저 실패 가능한 검증 조건을 정의한다.
- GREEN: 최소 변경으로 조건을 통과시킨다.
- REFACTOR: 문서/스크립트 중복을 줄이고 추적성을 유지한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Cluster topology 검증 스크립트 작성 | test | Contracts | PLN-005 | `infrastructure/tests/verify-cluster.sh` | Platform | Done |
| T-002 | GitOps(App/Project) 검증 스크립트 작성 | test | Core Design | PLN-005 | `infrastructure/tests/verify-gitops.sh` | DevOps | Done |
| T-003 | ESO/Vault 연동 검증 스크립트 작성 | test | Data Strategy | PLN-005 | `infrastructure/tests/verify-secrets.sh` | Security | Done |
| T-004 | 외부 서비스 계약 검증 스크립트 작성 | test | Interfaces | PLN-005 | `infrastructure/tests/verify-external-services.sh` | Platform | Done |
| T-005 | 네트워크 정책 검증 스크립트 작성 | test | Guardrails | PLN-007 | `infrastructure/tests/verify-network-policies.sh` | Security | Done |
| T-006 | 통합 실행 스크립트 확장(run-all) | test | Verification | PLN-007 | `infrastructure/tests/run-all.sh` | DevOps | Done |
| T-007 | Vault endpoint 수동 핫픽스 런북 정리 | ops | Failure Modes | PLN-004 | runbook 0002 체크리스트 | Platform | Done |
| T-008 | AppProject/Vault policy 최소권한 반영 | impl | Guardrails | PLN-006 | manifest/policy diff 확인 | Security | Done |
| T-009 | 폴더별 README 인덱스 동기화 | doc | Governance | PLN-008 | README row 반영 확인 | Docs | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-001
- [x] T-002

### Phase 2

- [x] T-003
- [x] T-004
- [x] T-005
- [x] T-006

### Phase 3

- [x] T-007
- [x] T-008
- [x] T-009

## TDD Scenarios by Component

### TC-01 Cluster Topology (`verify-cluster.sh`)

- RED: 노드 수/Ready 상태가 기준(<4)일 때 실패 확인
- GREEN: 4노드 Ready에서 PASS
- REFACTOR: 실패 원인 메시지 표준화(`[FAIL] cause`)

### TC-02 GitOps Contract (`verify-gitops.sh`)

- RED: `root-platform` path/revision 불일치 시 실패
- GREEN: `gitops/apps/root`, `main` 일치 시 PASS
- REFACTOR: 건강성 체크 로직 재사용 가능 구조 유지

### TC-03 Secret Plane (`verify-secrets.sh`)

- RED: `vault-backend`/`argocd-external-valkey` Ready=False 시 실패
- GREEN: Ready=True 및 role/SA 참조 일치 시 PASS
- REFACTOR: role/SA 검증을 명시 조건으로 고정

### TC-04 External Services (`verify-external-services.sh`)

- RED: 서비스/포트/EndpointSlice 주소 불일치 시 실패
- GREEN: Vault/Postgres/Valkey 계약 일치 시 PASS
- REFACTOR: ExternalName 의존 제거 후 EndpointSlice 검증 일원화

### TC-05 Network Policies (`verify-network-policies.sh`)

- RED: `argocd`/`external-secrets` 정책 누락 시 실패
- GREEN: CIDR/포트(172.30.0.12:26379, 172.30.0.10:8200) 일치 시 PASS
- REFACTOR: 정책명/검증 키를 계약화

### TC-06 Runbook Regression (`0002 runbook`)

- RED: 복구 절차 후 Degraded 지속 시 실패
- GREEN: Store/ExternalSecret/App 상태 정상화 시 PASS
- REFACTOR: 증적 수집 항목 표준화

## Verification Summary

- **Test Commands**:
  - `./infrastructure/tests/verify-cluster.sh`
  - `./infrastructure/tests/verify-gitops.sh`
  - `./infrastructure/tests/verify-secrets.sh`
  - `./infrastructure/tests/verify-external-services.sh`
- **Eval Commands**:
  - `./infrastructure/tests/run-all.sh`
- **Logs / Evidence Location**:
  - `docs/09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`
