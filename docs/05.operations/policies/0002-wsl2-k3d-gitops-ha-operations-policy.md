---
title: 'WSL2 k3d/k3s GitOps HA Operations Policy'
type: sdlc/policy
status: active
owner: platform
updated: 2026-06-02
---

# WSL2 k3d/k3s GitOps HA Operations Policy

## Overview

이 문서는 WSL2 기반 플랫폼의 운영 통제 기준을 정의한다. 외부 서비스 계약, 보안 최소권한, CI 정적 게이트, 복구 절차 준수 기준을 포함한다. 여기서 HA는 production HA가 아니라 현재 `infrastructure/k3d/k3d-cluster.yaml`의 `servers: 1`, `agents: 3` 로컬 multi-node validation baseline을 의미한다.

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
  - 인터페이스 계약 포트 고정(8200/15432/15433/6379)
  - Valkey는 `Service + EndpointSlice(172.18.0.9:6379)` 모델 사용
  - `gitops/platform/external-services/*.yaml`은 외부 서비스 `Service`와
    `EndpointSlice` desired state의 SSoT로 유지
  - Vault 경로 표준(`secret/platform/argocd`, `secret/platform/postgres-app`)
  - ArgoCD host=`argocd.127.0.0.1.nip.io`, TLS secret=`argocd-local-tls` # pragma: allowlist secret
  - `ingress-nginx-controller`는 `LoadBalancer` 타입 유지
  - 외부 Traefik `websecure/443`은 Docker 네트워크에서 접근 가능한
    ingress-nginx `LoadBalancer` IP(`172.18.0.240:443`)로 라우팅
  - direct runtime TLS 검증은 기본적으로 ingress-nginx `LoadBalancer` IP와
    host/SNI resolve를 사용하며, 호스트 포트 충돌 검증 시에만
    `ARGOCD_FALLBACK_PORT=8443` 경로를 명시
  - AppProject `apps` wildcard 금지 + 최소 allow-list 유지
  - `argocd` egress는 Valkey + DNS + HTTPS 허용
  - CI 정적 게이트 필수화(`branch-policy`, `pre-commit`,
    `repo-quality-static`, `manifest-static`)
  - `fs.inotify.max_user_instances >= 512` (권장 1024) — k3d 4노드 안정 기동 조건
  - Vault 컨테이너는 k3d-hyhome Docker 네트워크에 연결 상태를 유지해야 한다
  - `vault-external` EndpointSlice IP는 Vault의 k3d-hyhome 네트워크 IP(`172.18.0.8`)를 사용해야 한다
  - 호스트/브라우저/CLI 접근은 `VAULT_ADDR=https://vault.127.0.0.1.nip.io`
    경로를 사용하고, 클러스터 내부 ESO 접근은
    `vault-external.platform.svc`와 EndpointSlice 경로를 사용
  - Vault Kubernetes auth `kubernetes_host`는 `https://172.18.0.2:6443`으로 고정한다
  - Vault Kubernetes auth `disable_local_ca_jwt: true` + `token_reviewer_jwt` 설정 필수
  - OPA/Conftest는 아직 필수 게이트가 아니며, policy owner, policy bundle
    위치, 설치 경로, failure semantics가 정해질 때까지 기존 bash 기반
    정적 게이트를 SSoT로 사용
- **Allowed**:
  - 장애 시 수동 `EndpointSlice` 핫픽스는 human-approved break-glass와 런북 증적이 있을 때만 허용
  - ArgoCD hard-refresh 기반 상태 재평가는 런북 절차와 증적 기록을 통해 수행
  - `CHECK_TRAEFIK_443=true` 기반 운영 TLS 점검
  - Docker 재시작 후 Vault의 k3d-hyhome 네트워크 수동 재연결은 런북 절차로 수행
  - k3d 에이전트 노드 inotify 문제 시 순차 재시작(하나씩)
- **Disallowed**:
  - 평문 시크릿 커밋
  - 승인 없는 정책 완화/권한 확장
  - 로컬 파일 수정 상태만으로 배포 완료로 판단하는 행위
  - k3d 에이전트 노드 동시 재시작(inotify thundering herd 유발)

## CI Governance

- CD는 ArgoCD pull 모델을 기준으로 유지한다.
- GitHub Actions는 정적 검증 전용 게이트로 사용한다.
- `.github/workflows/**` 변경은 현재 CI workflow의 `branch-policy`,
  `pre-commit`, `repo-quality-static`, `manifest-static`
  구조와 `ci-summary` 집계를 유지해야 한다.

## Exceptions

- 긴급 복구를 위해 수동 EndpointSlice 생성은 허용한다.
- CI false-positive는 예외 승인 후 임시 우회 가능하나, 동일 스프린트 내 룰 수정이 필수다.
- 예외 승인 절차:
  1. 증적 첨부(로그, 상태 YAML, 실패 잡 링크)
  2. 플랫폼 오너 승인
  3. 실행 후 회귀 검증(`verify-contracts-static.sh`, `run-all.sh`)
  4. ADR/Operations 문서 반영

## Verification

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Static contract | Contract test and shell syntax checks pass before platform changes merge | [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md) |
| Runtime recovery | HA/runtime smoke checks and TLS checks pass after bootstrap or recovery | [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md) |
| Policy audit | GitOps root path/branch and AppProject wildcard restrictions remain compliant | [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md) |

## Review Cadence

- 운영 변경 시 즉시
- 정기 분기 검토

## EndpointSlice Ownership Boundary

- 정상 경로: `gitops/platform/external-services/*.yaml`에 `Service`와
  `EndpointSlice` desired state를 기록하고 PR review 후 ArgoCD
  reconciliation에 맡긴다.
- 예외 경로: ArgoCD resource exclusion, Docker network 재할당, 또는 runtime
  drift 때문에 즉시 복구가 필요한 경우에만 human-approved break-glass로
  직접 `EndpointSlice` patch/apply를 수행한다.
- 예외 실행 후에는 실제 endpoint 값을 Git desired state와 런북 증적으로
  되돌려 맞춰야 하며, 로컬 patch 상태만으로 완료를 선언하지 않는다.

## Audit Items

- AppProject 권한 확장 여부
- Vault 정책 wildcard 재도입 여부
- `argocd` egress 정책에서 DNS/HTTPS 누락 여부
- 현재 CI 정적 게이트(`branch-policy`, `pre-commit`, `repo-quality-static`,
  `manifest-static`) 유지 여부
- 외부 Traefik 계약(`websecure/443 -> ingress-nginx LoadBalancer IP:443`)과
  direct fallback 포트(`ARGOCD_FALLBACK_PORT`) 변경 이력
- OPA/Conftest 도입 여부와 policy owner/bundle/install path 결정 상태

## AI Agent Policy Section (If Applicable)

이 정책은 인프라 리소스를 직접 관리하며 AI Agent 모델/프롬프트/평가 정책이 별도 적용되지 않는다.
단, Agent가 이 정책 범위의 리소스를 조작할 경우 [운영 거버넌스](../../00.agent-governance/README.md)에 따른다.

## Related Documents

- **ARD**: [`../../02.architecture/requirements/0007-current-local-gitops-platform.md`](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Guide**: [`../guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Runbook**: [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md)
