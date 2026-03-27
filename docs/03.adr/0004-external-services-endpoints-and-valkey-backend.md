# ADR-0004: External Service Wrapping via Service/EndpointSlice and ArgoCD Valkey Backend

## Overview (KR)

이 ADR은 외부 Docker 서비스(Vault, PostgreSQL, Valkey)를 Kubernetes `Service + EndpointSlice`로 래핑하고, ArgoCD 백엔드를 외부 Valkey로 구성하는 결정을 기록한다.

## Context

외부 서비스 접근을 앱 관점에서 Kubernetes DNS 인터페이스로 통일해야 설정 일관성과 이식성을 확보할 수 있다.

## Decision

- Vault/PostgreSQL/Valkey 각각에 대해 Kubernetes Service/EndpointSlice를 생성한다.
- EndpointSlice는 고정 IP(`172.30.0.10/11/12`)를 사용한다.
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

### host.docker.internal 직접 사용

- Good:
  - 빠른 초기 연결
- Bad:
  - 환경 의존성 증가, 추상화 부족

### ExternalName 서비스

- Good:
  - 매니페스트 간결
- Bad:
  - 포트/엔드포인트 통제 한계, 정책 표현력 제한

## Related Documents

- **PRD**: [`../01.prd/2026-03-27-wsl-k3d-argocd-platform.md`](../01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../02.ard/0001-wsl-k3d-argocd-platform.md`](../02.ard/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Related ADR**: [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md)
