# WSL2 k3d/k3s ArgoCD HA Platform Specification

## Overview (KR)

이 문서는 WSL2 멀티노드 클러스터와 GitOps/Secret/외부 데이터 연동 구현 계약을 정의한다. 이번 확장에서 `argocd egress 안정성`, `AppProject 최소권한`, `CI 정적 계약 게이트`를 추가한다.

> **현재 실행계약 메모 (2026-05-09)**: 이 Spec은 2026-03-28 HA 플랫폼 설계 기록이다. 현재 repo-backed 외부 서비스 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Strategic Boundaries & Non-goals

- **Owns**: 클러스터 토폴로지, GitOps 배포 구조, 외부 서비스 인터페이스, CI 정적 검증, 운영 검증 스크립트
- **Does Not Own**: 외부 서비스 컨테이너 런타임, 외부 Traefik 라우팅 파일

## Related Inputs

- **PRD**: [`../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- **ADR**: [`../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)

## Phase 0 Baseline and Gap Report

### Existing CI State (as-is)

- `.github/workflows/ci.yml`는 기존 `pre-commit` 단일 잡 구조였다.
- 누락된 영역:
  - 변경영역(path-aware) 기반 실행 분기
  - static contract 검증
  - workflow 보안 게이트(actionlint/zizmor)

### Version Evidence (2026-03-28)

| Component | Current Baseline | Stable/Release Observation                        | Policy                              |
| --------- | ---------------- | ------------------------------------------------- | ----------------------------------- |
| k3s       | `v1.35.0+k3s1`   | `v1.35.2+k3s1` stable, `v1.35.3-rc1+k3s1` preview | baseline 유지, 업그레이드 후보 등록 |
| k3d       | `v5.8.3`         | `v5.8.3` stable                                   | baseline 유지                       |
| Valkey    | `9.0.1`          | `9.0.3` 후보                                      | baseline 유지, 업그레이드 후보 등록 |

참고 릴리스 페이지:

- `https://github.com/k3s-io/k3s/releases`
- `https://github.com/k3d-io/k3d/releases`
- `https://github.com/valkey-io/valkey/releases`

### Certificate Contract

- `secrets/certs/cert.pem` SAN은 최소 `127.0.0.1.nip.io` 또는 `*.127.0.0.1.nip.io`를 포함해야 한다.
- SAN 미포함 시 재발급 후 `bootstrap-local.sh`로 `argocd-local-tls`를 재주입한다.

## Contracts

### Runtime Contracts

- `vault-external.platform.svc.cluster.local:8200`
- `postgres-write-external:15432`
- `postgres-read-external:15433`
- `valkey-external:6379` (K8s-side 포트; Docker host publish `26379:6379`는 호스트 접근 전용)
- Vault paths: `secret/platform/argocd`, `secret/platform/postgres-app`

### Access/TLS Contracts

- ArgoCD 공식 host: `argocd.127.0.0.1.nip.io`
- TLS secret: `argocd-local-tls` (`kubernetes.io/tls`) # pragma: allowlist secret
- ingress-nginx controller service type: `LoadBalancer`
- 외부 Traefik 계약: `443 -> k3d :8443`
- fallback endpoint: `https://argocd.127.0.0.1.nip.io:8443`

### Network Policy Contracts

- `argocd` egress 허용:
  - Valkey: `172.19.0.12:6379/TCP`
  - DNS: `53/TCP,UDP` (`kube-system` DNS)
  - HTTPS: `443/TCP`

### GitOps Source Contracts

- root app path: `gitops/apps/root`
- root app revision: `main`
- 로컬 파일 변경만으로 반영되지 않으며 원격 `main` 기준으로 reconciliation 수행

### CI Static Contracts

- 변경영역 감지: `dorny/paths-filter`
- 필수 정적 게이트:
  - `pre-commit`
  - `manifest-static`
  - `workflow-security`
  - `shell-static`
- 집계 게이트: `ci-summary`

## Core Design

- WSL2/k3d cluster state is managed through GitOps manifests, static contract tests, and documented bootstrap boundaries.
- ArgoCD remains the reconciliation controller; local file edits are not treated as live deployment proof.
- External service access is modeled through Kubernetes Services, EndpointSlices, NetworkPolicies, and Vault-backed ESO contracts.

## Data Modeling & Storage Strategy

- This spec does not introduce application storage schemas.
- Persistent data remains outside the local k3d cluster in external PostgreSQL, Valkey, and Vault services.
- Storage-related changes are represented as endpoint, secret-path, and policy contracts rather than database migrations.

## Interfaces & Data Structures

### Core Interfaces

- Kubernetes YAML manifests under `gitops/`
- static verification shell scripts under `infrastructure/tests/`
- GitHub Actions workflow definitions under `.github/workflows/`
- Vault path and Kubernetes ExternalSecret conventions documented in this spec and related ADRs

## File-level Implementation Contract

- `.github/workflows/ci.yml`
  - `concurrency`: `ci-${{ github.ref }}` + `cancel-in-progress: true`
  - path filter 기반 조건부 잡 분기
  - workflow 변경 시 `actionlint`/`zizmor` 강제
- `infrastructure/tests/verify-contracts-static.sh` (신규)
  - root app path/revision
  - 외부 서비스 포트/EndpointSlice 주소
  - ArgoCD host/TLS secret 명칭
  - Vault policy 최소권한 경로
  - AppProject wildcard 금지 및 allow-list 존재
- `infrastructure/tests/run-all.sh`
  - runtime(kubectl) 검증 전용 유지

## Guardrails

- AppProject `apps`는 namespace wildcard(`*/*`) 금지
- Vault 정책에서 `secret/data/platform/*` wildcard 금지
- 시크릿/토큰/인증서 평문 커밋 금지

## Edge Cases & Error Handling

- External services may be reachable from the Docker network but not from k3d pods; verify EndpointSlice IPs and NetworkPolicy egress together.
- Local k3d readiness can drift from repo/static readiness; treat runtime checks as separate evidence.
- Optional local tools such as `kube-linter`, `actionlint`, or `zizmor` may be unavailable in a developer shell; CI/static script results remain the canonical minimum evidence.

## Failure Modes & Fallback / Human Escalation

- **Failure**: repo-server egress 부족으로 Git fetch 실패
  - **Fallback**: `argocd` egress에 DNS/443 허용 확인
  - **Human Escalation**: NetworkPolicy 변경은 PR review 후 GitOps reconciliation으로 반영한다.
- **Failure**: CI false positive
  - **Fallback**: 예외 승인 후 룰 보정(ADR/Operations 업데이트)
  - **Human Escalation**: gate 예외는 PR에 근거와 후속 보정 작업을 남긴다.
- **Failure**: CI false negative
  - **Fallback**: `verify-contracts-static.sh` 패턴 강화 + 회귀 테스트 추가
  - **Human Escalation**: 정적 계약 누락이 반복되면 관련 Operations policy를 갱신한다.

## Verification

### Static (CI/Local)

```bash
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
./infrastructure/tests/verify-contracts-static.sh
```

### Runtime (Local cluster)

```bash
./infrastructure/tests/run-all.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
```

## Success Criteria & Verification Plan

- `gitops/`, `infrastructure/`, `.github/` 변경이 계약 문서와 일치
- AppProject wildcard 권한 제거
- `argocd` egress가 Valkey + DNS + HTTPS 충족
- CI가 변경영역 기반으로 동작하고 정적 계약 검증 포함
- 현재 docs taxonomy 및 README 인덱스 동기화 완료

## Related Documents

- **Plan**: [`../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Tasks**: [`../../04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Guide**: [`../../05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../../05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Runbook**: [`../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
