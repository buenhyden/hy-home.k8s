---
title: 'Platform Expansion: cert-manager, Headlamp, Istio/Kiali Product Requirements'
type: prd
status: active
owner: platform-team
updated: 2026-05-17
---

# Platform Expansion: Headlamp, cert-manager, Istio/Kiali Product Requirements

## Overview (KR)

이 문서는 WSL2 기반 k3d/k3s 플랫폼에 Headlamp, cert-manager, Istio 서비스메시, Kiali를 추가하고, 외부 서비스 연결 계약을 repo-backed current contract와 일치시키기 위한 제품 요구사항을 정의한다.

> **현재 실행계약 메모 (2026-05-09)**: 이 문서는 2026-03-29 플랫폼 확장 요구사항 기록이다. 현재 repo-backed 실행계약은 [ADR-0010](../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)과 현재 `gitops/**` 매니페스트/정적 검증 스크립트가 우선한다. Kubernetes Dashboard는 Headlamp로 대체되었고, 외부 서비스 EndpointSlice/CIDR 계약은 `172.18.x` 기준이다.

## Requirement Status

이 PRD는 active 요구사항이지만 일부 초기 요구는 superseded 상태다.
Kubernetes Dashboard와 `dashboard.127.0.0.1.nip.io` 노출 요구는 [ADR-0010](../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)에 의해 Headlamp로 대체되었다.
`172.19.x` 값은 historical requirement이며 현재 외부 서비스 계약은 repo-backed manifests와 정적 검증 스크립트가 소유한다.

## Vision

로컬 플랫폼이 웹 UI 기반 클러스터 관찰, 자동화된 TLS 인증서 관리, 서비스메시 기반 트래픽 제어와 가시성을 갖춘 운영 수준 환경으로 발전한다.

## Problem Statement

- 초기 외부 서비스 IP(`172.30.0.x`)와 당시 Docker infra_net(`172.19.0.0/16`) 불일치가 연결 실패 위험을 만들었다.
- TLS 인증서 관리가 수동 mkcert 주입 방식으로 서비스 증가 시 운영 부담이 증가한다.
- 클러스터 워크로드를 웹 UI로 확인하는 수단이 없다.
- Istio 서비스메시 없이 pod-to-pod 트래픽 제어와 가시성이 부재하다.

## Personas

- **Platform Engineer**: IP 수정 후 서비스 재현성을 검증하고, 신규 컴포넌트를 GitOps로 배포해야 한다.
- **DevOps Engineer**: TLS 관리 자동화와 서비스메시 기반 운영 도구를 갖춰야 한다.
- **Security Engineer**: mkcert rootCA 신뢰 체인 유지와 최소권한 접근을 보장해야 한다.

## Key Use Cases

- **STORY-01**: 운영자가 `headlamp.127.0.0.1.nip.io`에서 HTTPS로 클러스터 상태를 확인한다.
- **STORY-02**: cert-manager가 mkcert rootCA로 신규 서비스 TLS 인증서를 자동 발급한다.
- **STORY-03**: Istio가 sidecar 주입 namespace의 pod-to-pod mTLS를 자동 적용한다.
- **STORY-04**: Kiali가 `kiali.127.0.0.1.nip.io`에서 서비스메시 토폴로지와 메트릭을 시각화한다.
- **STORY-05**: 외부 서비스 연결이 repo-backed EndpointSlice/CIDR 계약과 일관되게 작동한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: 외부 서비스 EndpointSlice 주소는 repo-backed current contract와 일치해야 한다. 초기 `172.19.x` 값은 historical requirement다.
- **REQ-PRD-FUN-02**: NetworkPolicy CIDR은 current external service contract와 일치해야 한다.
- **REQ-PRD-FUN-03**: 로컬 bootstrap 기본값은 current external service contract를 따르고, 구체 파일 수정 지시는 downstream Plan/Task가 소유한다.
- **REQ-PRD-FUN-04**: cert-manager v1.17.x를 GitOps 방식으로 설치한다.
- **REQ-PRD-FUN-05**: mkcert rootCA를 cert-manager `ClusterIssuer`로 등록한다.
- **REQ-PRD-FUN-06**: `bootstrap-local.sh`에 rootCA Secret 주입 단계를 추가한다.
- **REQ-PRD-FUN-07**: Headlamp를 GitOps 방식으로 제공하여 클러스터 UI 접근을 지원한다.
- **REQ-PRD-FUN-08**: Headlamp를 `headlamp.127.0.0.1.nip.io`(ingress-nginx + cert-manager TLS)로 노출한다.
- **REQ-PRD-FUN-09**: Istio v1.25.x(`istio-base` + `istiod`)를 GitOps 방식으로 설치한다.
  - IngressGateway 비활성화, ingress-nginx와 공존.
  - sidecar injection은 namespace opt-in 방식.
- **REQ-PRD-FUN-10**: Kiali v2.6.x를 GitOps 방식으로 설치한다.
  - 외부 Prometheus/Grafana/Tempo 연동.
  - `kiali.127.0.0.1.nip.io`(ingress-nginx + cert-manager TLS)로 노출.
- **REQ-PRD-FUN-11**: 외부 Traefik route는 Headlamp/Kiali 접근을 지원해야 한다.
- **REQ-PRD-FUN-12**: 정적 검증은 신규 서비스 계약 회귀를 탐지해야 한다.

## Success Criteria

- **REQ-PRD-MET-01**: Platform Engineer가 current external service contract 회귀를 탐지할 수 있다. Evidence: 외부 서비스 연결 회귀 0건.
- **REQ-PRD-MET-02**: 운영자가 cert-manager 발급 경로를 확인할 수 있다. Evidence: cert-manager `ClusterIssuer` Ready=True.
- **REQ-PRD-MET-03**: 운영자가 Headlamp UI로 클러스터 상태를 확인할 수 있다. Evidence: `headlamp.127.0.0.1.nip.io` HTTPS 접근 성공.
- **REQ-PRD-MET-04**: 운영자가 서비스메시 control plane 상태를 확인할 수 있다. Evidence: Istio `istiod` Deployment Available=True.
- **REQ-PRD-MET-05**: 운영자가 Kiali에서 서비스메시 토폴로지와 메트릭을 확인할 수 있다. Evidence: `kiali.127.0.0.1.nip.io` HTTPS 접근 성공.
- **REQ-PRD-MET-06**: CI가 서비스 계약 회귀를 차단한다. Evidence: 정적 계약 검증 PASS.
- **REQ-PRD-MET-07**: 전체 문서/정적 품질 게이트가 신규 확장 요구를 막지 않는다. Evidence: CI 정적 게이트 전체 PASS.

## Scope and Non-goals

- **In Scope**:
  - external service contract 정합화 (EndpointSlice, NetworkPolicy, bootstrap contract, static verification)
  - cert-manager + mkcert CA ClusterIssuer
  - Headlamp cluster UI
  - Istio (istio-base + istiod, IngressGateway 제외)
  - Kiali (external observability 연동)
  - Traefik route contract (Headlamp/Kiali)
  - 문서 체인 동기화
- **Out of Scope**:
  - 외부 서비스 런타임 자체 배포
  - Istio IngressGateway 활성화
  - GitHub Actions push deploy
  - ArgoCD TLS cert-manager 이관 (후속 Phase)
- **Non-goals**:
  - 프로덕션 환경 보안 강화 (Headlamp OIDC 등)
  - Vault PKI + cert-manager 연동

## Risks, Dependencies, and Assumptions

- **Risk**: IP 수정 후 정적 계약 검증 패턴 누락 시 CI false-negative.
  - **Mitigation**: `verify-contracts-static.sh` 패턴 동시 수정.
- **Risk**: Istio 설치 순서 오류 시 Kiali 동작 불가.
  - **Mitigation**: Plan에서 istio-base → istiod → kiali 순서 명시.
- **Assumption**: mkcert rootCA가 `secrets/certs/rootCA.pem`에 존재한다.
- **Assumption**: 관측성 외부 endpoint 값은 current repo-backed contract가 소유하며, 이 PRD의 과거 `172.19.x` 값은 실행 기준으로 사용하지 않는다.

## Related Documents

- **ARD**: [`../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md`](../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md)
- **ADR**: [`../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR**: [`../02.architecture/decisions/0007-kubernetes-dashboard-v3.md`](../02.architecture/decisions/0007-kubernetes-dashboard-v3.md)
- **ADR**: [`../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md`](../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR**: [`../02.architecture/decisions/0009-kiali-external-observability.md`](../02.architecture/decisions/0009-kiali-external-observability.md)
- **ADR**: [`../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../02.architecture/decisions/0010-headlamp-replaces-dashboard.md) — REQ-PRD-FUN-07, REQ-PRD-FUN-08의 Dashboard 요구사항을 Headlamp로 대체
- **Spec**: [`../03.specs/003-platform-expansion/spec.md`](../03.specs/003-platform-expansion/spec.md)
- **Plan**: [`../04.execution/plans/2026-03-29-platform-expansion.md`](../04.execution/plans/2026-03-29-platform-expansion.md)
