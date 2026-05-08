# ADR-0004: External Service Access Model and ArgoCD Valkey Backend

## Overview (KR)

이 ADR은 외부 서비스 접근 모델과 ArgoCD 백엔드를 외부 Valkey로 구성하는 결정을 기록한다.
**2026-03-29 갱신**: Valkey 접근 모델을 `ExternalName Service`에서 `Service + EndpointSlice`로 정정하고, IP 대역을 `172.19.0.x`로 갱신한다. Vault도 동일 패턴으로 통일한다. Valkey K8s-side 포트를 컨테이너 내부 포트(`6379`)로 정정한다(`26379`는 Docker host publish 포트로 호스트 접근 전용).

> **현재 실행계약 메모 (2026-05-09)**: 아래 `172.19.x` 외부 서비스 주소는 2026-03-29 기준의 역사적 `infra_net` 계약이다. 현재 repo-backed 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Context

외부 서비스 접근을 앱/플랫폼 관점에서 일관된 인터페이스로 제공해야 설정 이식성과 운영 단순성을 확보할 수 있다.
ADR-0005(WSL2 HA Baseline) 구현 이후 실제 Valkey 접근 모델이 `ExternalName`이 아니라 `Service + EndpointSlice(고정 IP)` 패턴으로 통일되었다. 이 ADR은 실제 구현과 일치하도록 결정을 갱신한다.

## Decision

- **PostgreSQL**, **Valkey**, **Vault** 모두 `Service + EndpointSlice(고정 IP)` 패턴을 사용한다.
  - `postgres-write-external`: `172.19.0.11:15432`
  - `postgres-read-external`: `172.19.0.11:15433`
  - `valkey-external`: `172.19.0.12:6379` (K8s EndpointSlice 대상 포트; Docker host publish `26379:6379`는 호스트 접근 전용)
  - `vault-external`: `172.19.0.9:8200`
- ArgoCD Redis 계층은 외부 Valkey(`valkey-external.platform.svc.cluster.local:6379`)를 사용한다.
- Valkey 접근은 ACL 비밀번호 + NetworkPolicy 제한을 필수로 한다.
- 모든 외부 서비스 Service는 `platform` namespace에 배치한다.
- Vault Agent(`172.19.0.10`)는 K8s 인터페이스 불필요 — ESO는 `vault-external:8200`(Vault 자체)만 참조한다.

## Explicit Non-goals

- ExternalName(CNAME) 패턴 사용
- PostgreSQL을 ArgoCD 내부 메타데이터 저장소로 사용
- Vault Agent를 별도 EndpointSlice로 노출

## Consequences

- **Positive**:
  - 모든 외부 서비스가 단일 패턴(Service+EndpointSlice)으로 통일되어 운영/문서가 단순해진다.
  - K8s DNS 기반 서비스 디스커버리가 일관성 있게 동작한다.
  - NetworkPolicy cidr 제어가 IP 고정으로 명확해진다.
- **Trade-offs**:
  - IPAM 운영 부담 증가(IP 변경 시 EndpointSlice 갱신 필요).
  - ExternalName 패턴보다 초기 설정이 복잡함.

## Alternatives

### ExternalName Service (이전 결정)

- Good: 초기 설정 간단, DNS CNAME 위임
- Bad: `host.k3d.internal` DNS 해석 불안정, IP 고정 불가, NetworkPolicy cidr 제어 어려움

### host.k3d.internal 직접 참조

- Good: 설정 간단
- Bad: 워크로드 설정 중복, 추상화/교체 용이성 저하

### 모든 서비스 ExternalName으로 통일

- Good: 설정 일관성
- Bad: DNS 해석 신뢰성 문제, NetworkPolicy 적용 불가

## Related Documents

- **PRD**: [`../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Related ADR**: [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md)
- **Related ADR**: [`./0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
