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
| T-005 | 통합 실행 스크립트 작성 | test | Verification | PLN-005 | `infrastructure/tests/run-all.sh` | DevOps | Done |
| T-006 | Vault endpoint 수동 핫픽스 런북 정리 | ops | Failure Modes | PLN-004 | runbook 0002 체크리스트 | Platform | Done |
| T-007 | 폴더별 README 인덱스 동기화 | doc | Governance | PLN-006 | README row 반영 확인 | Docs | Done |

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

### Phase 3

- [x] T-006
- [x] T-007

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
