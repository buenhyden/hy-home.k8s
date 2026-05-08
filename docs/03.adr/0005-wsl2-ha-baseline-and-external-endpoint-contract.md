# ADR-0005: WSL2 HA Baseline and External Endpoint Contract

## Overview (KR)

이 문서는 WSL2 기반 플랫폼의 HA 기본 토폴로지와 외부 서비스 인터페이스 계약, 그리고 CI/CD 운영 모델 결정을 고정한다.
**2026-03-29 갱신**: EndpointSlice 주소를 `172.19.0.x`(infra_net 실제 서브넷)로 전면 수정한다. Valkey K8s-side 포트를 컨테이너 내부 포트(`6379`)로 정정한다(`26379`는 Docker host publish 포트로 호스트 접근 전용).

> **현재 실행계약 메모 (2026-05-09)**: 아래 `172.19.x` 외부 서비스 주소는 2026-03-29 기준의 역사적 `infra_net` 계약이다. 현재 repo-backed 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Context

Vault/ESO 연동 장애와 ArgoCD ingress 회귀는 계약 불일치에서 발생했다. 동시에 CI가 단일 pre-commit 잡으로 구성되어 계약 회귀를 조기에 차단하기 어려웠다.
추가로, 기존 문서에 기록된 `172.30.0.x` 주소가 실제 Docker `infra_net` 서브넷(`172.19.0.0/16`)과 불일치함이 확인되어 계약 전반을 수정한다.

## Decision

- 클러스터 baseline을 `k3d servers=1, agents=3`으로 고정한다.
- 외부 서비스 인터페이스 계약 (K8s DNS 기준):
  - `vault-external.platform.svc.cluster.local:8200` → `172.19.0.9`
  - `postgres-write-external.platform.svc.cluster.local:15432` → `172.19.0.11`
  - `postgres-read-external.platform.svc.cluster.local:15433` → `172.19.0.11`
  - `valkey-external.platform.svc.cluster.local:6379` → `172.19.0.12` (K8s-side 포트; Docker host publish `26379:6379`는 호스트 접근 전용)
- `valkey-external` 구현 모델은 `Service + EndpointSlice(172.19.0.12:6379)`로 고정한다.
- Vault secret path를 `secret/platform/argocd`, `secret/platform/postgres-app`로 고정한다.
- ArgoCD HTTPS 공식 호스트를 `argocd.127.0.0.1.nip.io`로 고정하고 ingress TLS secret을 `argocd-local-tls`로 고정한다.
- `ingress-nginx-controller` 서비스 타입은 `LoadBalancer`로 고정한다.
- 호스트 `80/443` 소유권은 외부 Docker Traefik에 두고, 본 저장소는 `443 -> k3d :8443` 계약만 유지한다.
- `argocd` namespace egress는 Valkey(`172.19.0.12:6379`) + DNS(53/TCP,UDP) + HTTPS(443/TCP)를 허용한다.
- `platform` namespace egress는 infra_net 외부 서비스 범위만 허용한다.
- AppProject `apps`는 namespace wildcard(`*/*`)를 금지하고 allow-list 기반 최소권한으로 운영한다.
- Vault 정책은 `platform/*` 와일드카드를 금지하고 필요 경로만 허용한다.
- CI는 변경영역 기반 정적 게이트를 필수화하고, CD는 ArgoCD pull reconciliation 모델을 유지한다.
  - 필수 게이트: `pre-commit`, `manifest-static`, `workflow-security`, `shell-static`

## Explicit Non-goals

- 외부 런타임(Vault/PostgreSQL/Valkey) 자체 배포 자동화
- GitHub Actions push 기반 배포
- 클라우드 멀티AZ/멀티클러스터 HA
- Vault Agent를 K8s Service/EndpointSlice로 노출

## Consequences

- **Positive**:
  - 운영/문서/매니페스트/CI의 계약 일관성 강화
  - 런타임 이전에 정적 회귀를 탐지해 장애 확률 감소
  - CD 경로를 ArgoCD 단일 모델로 단순화
  - infra_net 실제 주소와 계약 일치로 연결 실패 위험 제거
- **Trade-offs**:
  - AppProject allow-list 관리 비용 증가
  - workflow-security 잡 도입으로 CI 시간 증가
  - 외부 Traefik 라우팅은 별도 저장소와 계약 동기화 필요

## Alternatives

### Alternative 1: CI pre-commit 단일 게이트 유지

- Good: 간단한 운영
- Bad: 계약/워크플로 보안 회귀 탐지 누락

### Alternative 2: GitHub Actions push deploy 도입

- Good: 즉시 배포 가능
- Bad: GitOps pull 모델과 책임 중복, 운영 복잡도 증가

## Related Documents

- **PRD**: [`../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Related ADR**: [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md)
- **Related ADR**: [`./0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md)
