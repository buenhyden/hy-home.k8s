# ADR-0001: k3d Topology and External Network Baseline

## Overview (KR)

이 ADR은 WSL2 환경에서 k3d 클러스터 토폴로지와 외부 Docker 네트워크 기준(`172.30.0.0/24`)을 확정한다.

## Context

멀티노드 개발/운영 검증과 외부 서비스 연결 재현성을 동시에 만족시키기 위해 노드 수, ingress 방식, 네트워크 대역을 표준화할 필요가 있다.

## Decision

- 클러스터는 `servers=1`, `agents=3`으로 고정한다.
- k3s 서버는 `--disable=traefik` 옵션으로 기본 ingress를 비활성화한다.
- 외부 Docker 서비스 네트워크는 `172.30.0.0/24` 대역을 사용한다.
- Vault/PostgreSQL/Valkey는 고정 IP를 부여한다.

## Explicit Non-goals

- 프로덕션급 멀티 control-plane 구성
- Docker 외 네트워크 플러그인 고도화

## Consequences

- **Positive**:
  - 표준 재현성이 높아지고 문서/테스트가 단순해진다.
- **Trade-offs**:
  - 단일 server 토폴로지로 control-plane HA는 제공하지 않는다.

## Alternatives

### Single-node cluster

- Good:
  - 최소 자원 사용
- Bad:
  - 워커 분리/스케줄링/정책 검증 범위 축소

### Multi-server k3d cluster

- Good:
  - control-plane redundancy 실험 가능
- Bad:
  - 로컬 자원 부담 증가, 복잡도 증가

## Related Documents

- **PRD**: [`../01.prd/2026-03-27-wsl-k3d-argocd-platform.md`](../01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../02.ard/0001-wsl-k3d-argocd-platform.md`](../02.ard/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Related ADR**: [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md)
