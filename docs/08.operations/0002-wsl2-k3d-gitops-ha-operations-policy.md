# WSL2 k3d/k3s GitOps HA Operations Policy

## Overview (KR)

이 문서는 WSL2 기반 플랫폼의 운영 통제 기준을 정의한다. 외부 서비스 계약, 보안 최소권한, CI 정적 게이트, 복구 절차 준수 기준을 포함한다.

## Policy Scope

- k3d/k3s 멀티노드 로컬 플랫폼
- ArgoCD/ESO/Vault 연동
- 외부 PostgreSQL/Valkey/Vault endpoint 계약
- GitHub Actions 정적 품질/보안 게이트

## Applies To

- **Systems**: `gitops/`, `infrastructure/`, `.github/`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: WSL2 local cluster + GitHub CI

## Controls

- **Required**:
  - 인터페이스 계약 포트 고정(8200/15432/15433/26379)
  - Valkey는 `Service + EndpointSlice(172.30.0.12:26379)` 모델 사용
  - Vault 경로 표준(`secret/platform/argocd`, `secret/platform/postgres-app`)
  - ArgoCD host=`argocd.127.0.0.1.nip.io`, TLS secret=`argocd-local-tls`
  - `ingress-nginx-controller`는 `LoadBalancer` 타입 유지
  - 외부 Traefik 443 -> k3d 8443 라우팅 계약 유지
  - AppProject `apps` wildcard 금지 + 최소 allow-list 유지
  - `argocd` egress는 Valkey + DNS + HTTPS 허용
  - CI 정적 게이트 필수화(`pre-commit`, `manifest-static`, `workflow-security`, `shell-static`)
- **Allowed**:
  - 장애 시 수동 `EndpointSlice` 핫픽스
  - `argocd --hard-refresh` 기반 상태 재평가
  - `CHECK_TRAEFIK_443=true` 기반 운영 TLS 점검
- **Disallowed**:
  - 평문 시크릿 커밋
  - 승인 없는 정책 완화/권한 확장
  - 로컬 파일 수정 상태만으로 배포 완료로 판단하는 행위

## CI Governance

- CD는 ArgoCD pull 모델을 기준으로 유지한다.
- GitHub Actions는 정적 검증 전용 게이트로 사용한다.
- `.github/workflows/**` 변경은 workflow-security 잡을 반드시 통과해야 한다.

## Exceptions

- 긴급 복구를 위해 수동 EndpointSlice 생성은 허용한다.
- CI false-positive는 예외 승인 후 임시 우회 가능하나, 동일 스프린트 내 룰 수정이 필수다.
- 예외 승인 절차:
  1. 증적 첨부(로그, 상태 YAML, 실패 잡 링크)
  2. 플랫폼 오너 승인
  3. 실행 후 회귀 검증(`verify-contracts-static.sh`, `run-all.sh`)
  4. ADR/Operations 문서 반영

## Verification

### Static

```bash
./infrastructure/tests/verify-contracts-static.sh
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
```

### Runtime

```bash
./infrastructure/tests/run-all.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
```

### Policy/Audit

```bash
kubectl -n argocd get app root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
rg -n 'group:\s*"\*"|kind:\s*"\*"' gitops/clusters/local/appproject-apps.yaml
```

## Review Cadence

- 운영 변경 시 즉시
- 정기 분기 검토

## Audit Items

- AppProject 권한 확장 여부
- Vault 정책 wildcard 재도입 여부
- `argocd` egress 정책에서 DNS/HTTPS 누락 여부
- workflow-security 강제 실행 여부
- 외부 Traefik 계약(`443 -> 8443`) 변경 이력

## Related Documents

- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Guide**: [`../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Runbook**: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)
