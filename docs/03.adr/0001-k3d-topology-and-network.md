# ADR-0001: k3d Topology and External Network Baseline

## Overview (KR)

이 ADR은 WSL2 환경에서 k3d 클러스터 토폴로지와 외부 서비스 연동 네트워크 기준을 확정한다.
**2026-03-29 갱신**: 외부 서비스 네트워크 대역을 실제 Docker `infra_net` 서브넷인 `172.19.0.0/16`으로 정정한다. Valkey 포트를 컨테이너 내부 포트(`6379`)로 정정한다(`26379`는 Docker host publish 포트로 호스트 접근 전용).

> **현재 실행계약 메모 (2026-05-09)**: 아래 `172.19.x` 외부 서비스 주소는 2026-03-29 기준의 역사적 `infra_net` 계약이다. 현재 repo-backed 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Context

멀티노드 개발/운영 검증과 외부 서비스 연결 재현성을 동시에 만족시키기 위해 노드 수, ingress 방식, 네트워크 대역을 표준화할 필요가 있다.
외부 Docker 네트워크(`infra_net`)의 실제 서브넷이 `172.19.0.0/16`으로 확인됨에 따라 기존 문서의 `172.30.0.0/24`는 오기였으며 해당 참조를 전면 수정한다.

## Decision

- 클러스터는 `servers=1`, `agents=3`으로 고정한다.
- k3s 서버는 `--disable=traefik` 옵션으로 기본 ingress를 비활성화한다.
- 외부 서비스 연동 네트워크 대역:
  - `infra_net`: `172.19.0.0/16`, gateway `172.19.0.1`
  - `k3d`: `172.18.0.0/16`, gateway `172.18.0.1`
- 외부 서비스 IP 고정 할당:
  - Vault: `172.19.0.9:8200`
  - Vault Agent: `172.19.0.10` (K8s 인터페이스 불필요, ESO는 Vault 직접 참조)
  - PostgreSQL/HAProxy: `172.19.0.11` (write `15432`, read `15433`)
  - Valkey: `172.19.0.12:6379` (컨테이너 내부 포트; host publish `26379:6379`는 호스트 접근 전용)
  - Prometheus: `172.19.0.20:9090`
  - Loki: `172.19.0.21:3100`
  - Tempo: `172.19.0.22:3200`
  - Alloy: `172.19.0.23` (gRPC `4317`, HTTP `4318`)
  - Grafana: `172.19.0.24:3000`

## Explicit Non-goals

- 프로덕션급 멀티 control-plane 구성
- Docker 외 네트워크 플러그인 고도화
- Vault Agent를 별도 K8s Service/EndpointSlice로 노출

## Consequences

- **Positive**:
  - 표준 재현성이 높아지고 문서/테스트가 단순해진다.
  - infra_net 실제 대역과 계약이 일치하여 연결 실패 위험 제거.
  - Observability 서비스(Prometheus/Loki/Tempo/Alloy/Grafana) 주소가 계약에 명시됨.
- **Trade-offs**:
  - 단일 server 토폴로지로 control-plane HA는 제공하지 않는다.
  - 기존 `172.30.0.x` 참조를 EndpointSlice, NetworkPolicy, bootstrap, verify-contracts 전반에서 일괄 수정 필요.

## Alternatives

### 172.30.0.0/24 유지

- Good: 기존 구현 변경 불필요
- Bad: 실제 Docker infra_net 대역과 불일치, 런타임 연결 실패

### Single-node cluster

- Good: 최소 자원 사용
- Bad: 워커 분리/스케줄링/정책 검증 범위 축소

### Multi-server k3d cluster

- Good: control-plane redundancy 실험 가능
- Bad: 로컬 자원 부담 증가, 복잡도 증가

## Related Documents

- **PRD**: [`../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Related ADR**: [`./0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
