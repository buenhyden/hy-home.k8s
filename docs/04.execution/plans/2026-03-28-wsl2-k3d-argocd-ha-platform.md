# WSL2 k3d/k3s ArgoCD HA Platform Plan

## Overview (KR)

이 문서는 WSL2 환경에서 멀티노드 Kubernetes + GitOps + ESO/Vault + 외부 DB/Valkey 통합을 고도화하고, CI 정적 게이트를 추가하기 위한 단계별 실행 계획이다.

## Context

이 계획은 2026-03-28 기준 HA 플랫폼 고도화 작업의 실행 순서와 검증 기준을 기록한다. 현재 repo-backed 실행계약과 다를 수 있는 런타임 값은 관련 Spec, Operations policy, 정적 검증 스크립트가 우선한다.

## Goals & In-Scope

- `argocd` egress 안정성 확보(Valkey + DNS + HTTPS)
- AppProject `apps` 최소권한 allow-list 고정
- CI 변경영역 기반 정적 게이트 구축
- 2026-03-28 문서 체인(01~09) + README 인덱스 동기화

## Non-Goals & Out-of-Scope

- 외부 서비스 런타임 자체 배포 자동화
- GitHub Actions push deploy
- 외부 Traefik 라우팅 파일 직접 관리

## Phase Plan

### Phase 0. Baseline/GAP 고정

- `.github/workflows/ci.yml` 현행 단일 pre-commit 구조를 갭으로 명시
- 버전 정책 명문화: baseline 유지 + 최신 stable 후보 백로그 등록
- 인증서 SAN 점검/재발급 절차를 Guide/Runbook에 반영

### Phase 1. GitOps/Infra 하드닝

- `argocd-egress-to-external-valkey` 정책에 DNS/HTTPS egress 추가
- `appproject-apps.yaml` wildcard 제거, 최소 allow-list 적용
- `bootstrap-local.sh` 실패 메시지 표준화(`[FAIL] cause`) 및 TLS 계약 유지
- 외부 서비스 Service+EndpointSlice 계약 유지 검증

### Phase 2. CI 최적화

- `.github/workflows/ci.yml`에 `concurrency` + `paths-filter` 추가
- 조건부 잡 분기:
  - `pre-commit`
  - `manifest-static`
  - `workflow-security` (`actionlint`, `zizmor`)
  - `shell-static` (`bash -n`, `shellcheck`)
- `ci-summary` 집계 게이트로 최종 실패 반영
- `infrastructure/tests/verify-contracts-static.sh` 신규 추가

### Phase 3. 문서/인덱스 동기화

- 01~09 기존 체인 문서 업데이트
- 각 폴더 README 인덱스 설명/최종수정일 동기화

## Work Breakdown

| Task | Description | Files / Docs Affected | Validation Criteria |
| --- | --- | --- | --- |
| PLN-001 | `argocd` egress 계약 확장 | `gitops/platform/network-policies/argocd-egress-to-external-valkey.yaml` | `verify-network-policies.sh` |
| PLN-002 | AppProject 최소권한화 | `gitops/clusters/local/appproject-apps.yaml` | wildcard 금지 + allow-list 검증 |
| PLN-003 | 정적 계약 검증 스크립트 추가 | `infrastructure/tests/verify-contracts-static.sh` | standalone PASS |
| PLN-004 | CI workflow 개편 | `.github/workflows/ci.yml` | 잡 분기/보안 게이트 확인 |
| PLN-005 | Dependabot 경로 재정렬 | `.github/dependabot.yml` | 불필요 placeholder 제거 |
| PLN-006 | 문서 체인 업데이트 | `docs/01~09` target docs | 링크/계약 반영 |
| PLN-007 | README 인덱스 동기화 | `docs/01~09/README.md` | 설명/수정일 반영 |

## Verification Plan

### Static Gate

```bash
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
./infrastructure/tests/verify-contracts-static.sh
```

### Runtime Gate

```bash
./infrastructure/tests/run-all.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
```

### CI Gate

- paths-filter 분기 검증
- `.github` 변경 PR에서 workflow-security 강제 실행 확인

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| CI false-positive | Medium | 예외 승인 후 룰 보정, ADR/운영정책 갱신 |
| CI false-negative | High | `verify-contracts-static.sh` 패턴 강화 및 케이스 추가 |
| AppProject allow-list 누락으로 sync 실패 | Medium | 리소스 추가 시 allow-list 갱신 체크리스트 운영 |
| 외부 Traefik 계약 불일치 | High | 운영 정책/런북에 443->8443 검증 단계 유지 |

## Rollback Plan

- 정책/워크플로 변경으로 운영 영향 발생 시 다음 순서로 롤백:
  1. CI 룰 일시 완화(필요 최소 수준)
  2. AppProject allow-list 직전 버전 복원
  3. 네트워크 정책 직전 버전 복원
  4. `verify-contracts-static.sh` 기준 재평가
- false positive는 예외 승인 로그를 남기고, false negative는 즉시 패치 배포

## Completion Criteria

- [ ] 코드/문서 변경이 계약과 일치
- [ ] 정적 검증 PASS
- [ ] 런타임 검증 PASS
- [ ] README 인덱스 동기화 완료

## Related Documents

- **PRD**: [`../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- **ADR**: [`../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
- **Spec**: [`../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Tasks**: [`../04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
