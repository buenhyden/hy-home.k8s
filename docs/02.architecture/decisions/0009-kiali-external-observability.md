---
title: 'ADR-0009: Kiali with External Observability Stack'
type: adr
status: accepted
owner: platform
updated: 2026-05-18
---

# ADR-0009: Kiali with External Observability Stack

## Overview (KR)

이 ADR은 Kiali를 `kiali-server` Helm chart 기반으로 설치하고, 외부 Docker 호스팅 Observability 스택(Prometheus/Grafana/Tempo)과 연동하는 결정을 기록한다.

## Context

Istio 서비스메시의 트래픽 토폴로지와 메트릭을 시각화하기 위해 Kiali가 필요하다.
Prometheus, Grafana, Tempo는 이미 Docker infra_net(`172.19.0.x`)에서 운영 중이며, K8s 내부에 별도 설치 없이 외부 엔드포인트로 연동한다.
Docker Traefik은 `kiali.127.0.0.1.nip.io`를 k3d ingress로 프록시한다.

> **현재 실행계약 메모 (2026-05-09)**: 아래 `172.19.x` observability 주소는 2026-03-29 기준의 역사적 `infra_net` 계약이다. 현재 repo-backed 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Decision

- Kiali `kiali-server` Helm chart(`https://kiali.org/helm-charts`)를 `istio-system` namespace에 설치한다.
  - 별도 Kiali Operator 없이 단일 인스턴스로 운영.
- Kiali 버전: v2.6.x
- 외부 Observability 연동:
  - Prometheus: `http://172.19.0.20:9090`
  - Grafana: `http://172.19.0.24:3000`
  - Tracing (Tempo): `http://172.19.0.22:3200`
- 인그레스: `ingress-nginx`, hostname `kiali.127.0.0.1.nip.io`.
- TLS: cert-manager `ClusterIssuer`(mkcert CA)로 발급.
- 인증: anonymous (로컬 환경 전용).
- 외부 노출: Docker Traefik router `kiali-k3d` 추가 (별도 Traefik repo 관리).
- Kiali egress NetworkPolicy: `172.19.0.20~24` 범위 허용.

## Explicit Non-goals

- Kiali Operator 방식 설치
- 프로덕션 환경 인증 강화 (로컬 전용)
- K8s 내부 Prometheus/Grafana 설치
- Jaeger 연동 (Tempo 사용)

## Consequences

- **Positive**:
  - 서비스메시 트래픽 토폴로지, 메트릭, 트레이싱을 단일 UI에서 확인 가능.
  - 기존 외부 Observability 스택 재활용으로 K8s 내 자원 절약.
  - cert-manager TLS로 HTTPS 자동화.
- **Trade-offs**:
  - 외부 Prometheus/Grafana/Tempo와의 네트워크 경로(infra_net → k3d egress) 유지 필요.
  - Kiali egress NetworkPolicy에 observability 범위 명시 필요.
  - Istio 설치가 선행되어야 함.

## Alternatives

### Kiali Operator

- Good: 운영 자동화, lifecycle 관리 향상
- Bad: 로컬 단일 인스턴스에는 과도한 복잡도

### K8s 내부 Prometheus 설치

- Good: 클러스터 자체 완결성
- Bad: 이미 외부 스택 운영 중, 자원 중복

### Grafana 단독 사용

- Good: 기존 Grafana 활용
- Bad: Istio 서비스메시 토폴로지 시각화 불가

## Related Documents

- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../requirements/0003-platform-expansion-mesh-dashboard.md`](../requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Related ADR**: [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md)
- **Related ADR**: [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md)
