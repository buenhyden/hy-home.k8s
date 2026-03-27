# ADR-0004: External Service Access Model and ArgoCD Valkey Backend

## Overview (KR)

이 ADR은 외부 서비스 접근 모델(PostgreSQL은 `Service + EndpointSlice`, Valkey는 `ExternalName Service`, Vault는 외부 URL)과 ArgoCD 백엔드를 외부 Valkey로 구성하는 결정을 기록한다.

## Context

외부 서비스 접근을 앱/플랫폼 관점에서 일관된 인터페이스로 제공해야 설정 이식성과 운영 단순성을 확보할 수 있다. 다만 서비스 특성(고정 IP 필요 여부, 관리 주체)에 따라 접근 방식이 달라진다.

## Decision

- PostgreSQL은 Kubernetes `Service + EndpointSlice`로 래핑하고 고정 IP(`172.30.0.11`)를 사용한다.
- Valkey는 Kubernetes `ExternalName Service`(`valkey-external -> host.k3d.internal`)로 노출한다.
- Vault는 Kubernetes 내부 래핑 없이 외부 URL(`https://vault.127.0.0.1.nip.io`)로 접근한다.
- ArgoCD Redis 계층은 외부 Valkey를 사용한다.
- Valkey 접근은 ACL 비밀번호 + NetworkPolicy 제한을 필수로 한다.

## Explicit Non-goals

- ExternalName 서비스만 사용한 단순 CNAME 모델
- PostgreSQL을 ArgoCD 내부 메타데이터 저장소로 사용

## Consequences

- **Positive**:
  - 워크로드의 의존 경로가 K8s DNS로 표준화
  - 외부 서비스 교체 시 인터페이스 안정성 확보
- **Trade-offs**:
  - 고정 IP 관리(IPAM) 운영 부담 증가

## Alternatives

### Vault/Valkey까지 EndpointSlice 고정 IP로 통일

- Good:
  - 인터페이스가 단일 패턴으로 단순화
- Bad:
  - IPAM 운영 부담 증가, 관리형 외부 엔드포인트와 충돌 가능

### host.k3d.internal 직접 참조 (Service 미사용)

- Good:
  - 초기 설정이 빠름
- Bad:
  - 워크로드 설정 중복, 추상화/교체 용이성 저하

## Related Documents

- **PRD**: [`../01.prd/2026-03-27-wsl-k3d-argocd-platform.md`](../01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../02.ard/0001-wsl-k3d-argocd-platform.md`](../02.ard/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Related ADR**: [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md)
