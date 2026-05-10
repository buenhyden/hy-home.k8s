# Task: WSL k3d/k3s ArgoCD Platform Execution

## Overview (KR)

이 문서는 WSL2 기반 GitOps 플랫폼 구축 작업을 TDD/검증 중심으로 추적한다. 모든 작업은 증적과 완료 기준을 포함한다.

## Inputs

- **Parent Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Parent Plan**: [`../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)

## Working Rules

- 핵심 동작은 테스트/검증 기준을 먼저 정의한다.
- 모든 Task는 실행 증적(명령/출력/링크)을 남긴다.
- 문서 작업도 링크/구조 검증을 포함한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | 최신 Stable 버전 재검증 및 freeze 표 갱신 | test | §Core Design | Phase 1 | release note 확인 로그 | Platform | Todo |
| T-002 | k3d 1+3 토폴로지 및 노드 Ready 검증 | impl | §Contracts | Phase 1 | `kubectl get nodes` | Platform | Todo |
| T-003 | ingress-nginx + `argocd.local` TLS 접근 검증 | test | §Verification | Phase 1 | curl/browser 접근 캡처 | Platform | Todo |
| T-004 | ArgoCD Helm 설치 및 external Valkey 연결 검증 | impl | §Core Design | Phase 2 | argocd/redis 관련 pod 상태 | DevOps | Todo |
| T-005 | AppProject 제한 정책 부정 테스트 | test | §Guardrails | Phase 2 | 금지 repo/ns 배포 실패 증적 | DevOps | Todo |
| T-006 | ApplicationSet 생성/동기화 검증 | impl | §Interfaces | Phase 2 | 앱 자동 생성/health 확인 | DevOps | Todo |
| T-007 | ESO->Vault Kubernetes Auth sync e2e 검증 | eval | §Data Strategy | Phase 2 | ExternalSecret Ready/Secret 생성 | Security | Todo |
| T-008 | PostgreSQL EndpointSlice + Valkey ExternalName 통신 검증 | test | §Contracts | Phase 2 | 테스트 pod 연결 성공 | Platform | Todo |
| T-009 | NetworkPolicy 허용/차단 검증 | test | §Guardrails | Phase 2 | 허용/거부 케이스 로그 | Security | Todo |
| T-010 | Drift self-heal 및 rollback 시나리오 검증 | eval | §Failure Modes | Phase 3 | ArgoCD sync/rollback 로그 | DevOps | Todo |
| T-011 | 문서 링크 무결성 및 README 인덱스 동기화 검증 | doc | §Governance | Phase 3 | 상대 링크/인덱스 점검 결과 | Docs | Todo |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [ ] T-001 버전 freeze 검증
- [ ] T-002 클러스터 토폴로지 검증
- [ ] T-003 ingress/TLS 접근 검증

### Phase 2

- [ ] T-004 ArgoCD + external Valkey 검증
- [ ] T-005 AppProject 제약 검증
- [ ] T-006 ApplicationSet 검증
- [ ] T-007 ESO+Vault sync 검증
- [ ] T-008 외부 endpoint 통신 검증
- [ ] T-009 NetworkPolicy 검증

### Phase 3

- [ ] T-010 self-heal/rollback 검증
- [ ] T-011 문서 링크/인덱스 검증

## Verification Summary

- **Test Commands**:
  - `kubectl get nodes`
  - `kubectl get svc,endpointslice -A`
  - `kubectl -n argocd get applications,appproject`
  - `kubectl -n external-secrets get externalsecret,secretstore,clustersecretstore`
- **Eval Commands**:
  - `argocd app list`
  - `argocd app sync <app>`
- **Logs / Evidence Location**:
  - `docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md` 체크리스트 기반 증적

## Related Documents

- **Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Runbook**: [`../09.runbooks/0001-argocd-platform-bootstrap-runbook.md`](../09.runbooks/0001-argocd-platform-bootstrap-runbook.md)
