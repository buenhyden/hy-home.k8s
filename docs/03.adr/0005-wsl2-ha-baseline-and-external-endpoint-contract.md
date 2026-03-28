# ADR-0005: WSL2 HA Baseline and External Endpoint Contract

## Overview (KR)

이 문서는 WSL2 기반 플랫폼의 HA 기본 토폴로지와 외부 서비스 인터페이스 계약을 고정하기 위한 결정 기록이다.

## Context

플랫폼 운영 중 Vault/ESO 연동 장애의 핵심 원인이 외부 endpoint 계약 불일치로 확인되었다. 문서/매니페스트/운영 절차 간 동일 계약을 강제할 필요가 있다.

## Decision

- 클러스터 baseline을 `k3d servers=1, agents=3`으로 고정한다.
- 외부 서비스 인터페이스 계약을 다음으로 고정한다.
  - `vault-external.platform.svc.cluster.local:8200`
  - `postgres-write-external:15432`
  - `postgres-read-external:15433`
  - `valkey-external:26379`
- Vault secret path를 `secret/platform/argocd`, `secret/platform/postgres-app`로 고정한다.
- Vault 연결 실패 시 운영 핫픽스로 `EndpointSlice platform/vault-external-1` 수동 복구 절차를 허용한다(영구 구조 개선은 백로그).

## Explicit Non-goals

- 외부 런타임(Vault/PostgreSQL/Valkey) 자체 배포 자동화
- 클라우드 멀티AZ/멀티클러스터 HA

## Consequences

- **Positive**:
  - 운영/문서/매니페스트의 계약 일관성 확보
  - 장애 원인 파악 및 복구 시간 단축
- **Trade-offs**:
  - 수동 EndpointSlice 핫픽스는 임시 조치이며 drift 관리 부담 존재

## Alternatives

### Alternative 1: Service DNS 직접 참조만 사용(EndpointSlice 미사용)

- Good: 리소스 단순화
- Bad: 외부 고정 IP 브리지 모델과 충돌

### Alternative 2: ExternalName-only 모델 통일

- Good: 관리 단순성
- Bad: PostgreSQL write/read 포트 분리 계약 표현이 약함

## Agent-related Example Decisions (If Applicable)

- 복구 자동화는 증적 수집을 포함해야 한다.
- 보안 관련 값(토큰/비밀번호)은 출력/문서화 금지.

## Related Documents

- **PRD**: [`../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Related ADR**: [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md), [`./0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md)
