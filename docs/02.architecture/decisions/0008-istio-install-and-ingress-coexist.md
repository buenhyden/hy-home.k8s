---
title: 'ADR-0008: Istio Default Profile with ingress-nginx Coexistence'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-05-18
---

# ADR-0008: Istio Default Profile with ingress-nginx Coexistence

## Overview

이 ADR은 Istio를 `default` 프로필로 Helm 기반 설치하고, 기존 ingress-nginx와 공존하는 전략을 확정한다.

## Context

서비스메시(mTLS, 트래픽 관리, 관측가능성)가 필요하며, 기존 ingress-nginx 기반 외부 노출 구조를 유지해야 한다.
WSL2 로컬 환경에서 자원 예산이 제한적이므로 설치 복잡도를 최소화해야 한다.
Istio IngressGateway가 ingress-nginx와 포트 충돌 없이 공존해야 한다.

## Decision

- Istio를 `istio-base` + `istiod` Helm chart(`https://istio-release.storage.googleapis.com/charts`) 조합으로 설치한다.
- 프로필: `default` (ambient mesh 미사용, sidecar 모델).
- `istiod` 리소스 제한 적용 (WSL2 자원 예산):
  - `pilot.resources.requests.cpu: 100m`
  - `pilot.resources.requests.memory: 128Mi`
- **Istio IngressGateway 비활성화** (`gateways.istio-ingressgateway.enabled: false`).
  - 외부 노출은 ingress-nginx가 담당하고, Istio Gateway CR은 사용하지 않는다.
- sidecar injection은 **namespace opt-in** 방식: `istio-injection=enabled` label이 있는 namespace에만 적용.
- 기본 sidecar injection 미적용 namespace: `argocd`, `cert-manager`, `headlamp`, `ingress-nginx`, `external-secrets`, `platform`.
- Istio 버전: v1.25.x

## Explicit Non-goals

- Istio IngressGateway를 ingress-nginx 대체로 사용
- Ambient mesh 도입
- istioctl 기반 설치 (GitOps 불가)
- 멀티클러스터 Istio federation

## Consequences

- **Positive**:
  - 서비스메시(mTLS, 트래픽 정책) 기능 확보.
  - GitOps 방식으로 Istio 수명주기 관리.
  - ingress-nginx 기반 외부 노출 구조 변경 없음.
  - sidecar opt-in으로 시스템 namespace 영향 없음.
- **Trade-offs**:
  - Istio CRD 등록으로 AppProject clusterResourceWhitelist 갱신 필요.
  - 사이드카 주입된 Pod의 컨테이너 수 증가로 자원 사용 증가.
  - Kiali 설치 전에 Istio 설치가 선행되어야 함.

## Alternatives

### Istio IngressGateway 활성화

- Good: Istio 기능 풀 활용
- Bad: ingress-nginx와 포트 충돌, k3d LoadBalancer 포트 경합

### Linkerd

- Good: Istio보다 가볍고 설치 단순
- Bad: 사용자 요구사항이 Istio/Kiali이므로 기각

### istioctl install

- Good: 프로파일 기반 편의 설치
- Bad: GitOps 선언형 관리 불가

## Related Documents

- **PRD**: [`../../01.requirements/2026-06-02-current-local-gitops-platform.md`](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
- **ARD**: [`../requirements/0007-current-local-gitops-platform.md`](../requirements/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md)
