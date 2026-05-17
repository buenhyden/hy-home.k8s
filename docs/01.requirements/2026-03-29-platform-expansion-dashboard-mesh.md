---
title: 'Platform Expansion: cert-manager, Headlamp, Istio/Kiali Product Requirements'
type: prd
status: active
owner: platform-team
updated: 2026-05-09
---

# Platform Expansion: Dashboard, cert-manager, Istio/Kiali Product Requirements

## Overview (KR)

이 문서는 WSL2 기반 k3d/k3s 플랫폼에 Kubernetes Dashboard, cert-manager, Istio 서비스메시, Kiali를 추가하고, 외부 서비스 IP 계약을 실제 Docker infra_net(`172.19.0.0/16`)으로 수정하기 위한 제품 요구사항을 정의한다.

> **현재 실행계약 메모 (2026-05-09)**: 이 문서는 2026-03-29 플랫폼 확장 요구사항 기록이다. 현재 repo-backed 실행계약은 [ADR-0010](../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)과 현재 `gitops/**` 매니페스트/정적 검증 스크립트가 우선한다. Kubernetes Dashboard는 Headlamp로 대체되었고, 외부 서비스 EndpointSlice/CIDR 계약은 `172.18.x` 기준이다.

## Vision

로컬 플랫폼이 웹 UI 기반 클러스터 관찰, 자동화된 TLS 인증서 관리, 서비스메시 기반 트래픽 제어와 가시성을 갖춘 운영 수준 환경으로 발전한다.

## Problem Statement

- 기존 외부 서비스 IP(`172.30.0.x`)가 실제 Docker infra_net(`172.19.0.0/16`)과 불일치하여 연결 실패 위험이 있다.
- TLS 인증서 관리가 수동 mkcert 주입 방식으로 서비스 증가 시 운영 부담이 증가한다.
- 클러스터 워크로드를 웹 UI로 확인하는 수단이 없다.
- Istio 서비스메시 없이 pod-to-pod 트래픽 제어와 가시성이 부재하다.

## Personas

- **Platform Engineer**: IP 수정 후 서비스 재현성을 검증하고, 신규 컴포넌트를 GitOps로 배포해야 한다.
- **DevOps Engineer**: TLS 관리 자동화와 서비스메시 기반 운영 도구를 갖춰야 한다.
- **Security Engineer**: mkcert rootCA 신뢰 체인 유지와 최소권한 접근을 보장해야 한다.

## Key Use Cases

- **STORY-01**: 운영자가 `dashboard.127.0.0.1.nip.io`에서 HTTPS로 클러스터 상태를 확인한다.
- **STORY-02**: cert-manager가 mkcert rootCA로 신규 서비스 TLS 인증서를 자동 발급한다.
- **STORY-03**: Istio가 sidecar 주입 namespace의 pod-to-pod mTLS를 자동 적용한다.
- **STORY-04**: Kiali가 `kiali.127.0.0.1.nip.io`에서 서비스메시 토폴로지와 메트릭을 시각화한다.
- **STORY-05**: 외부 서비스 연결이 `172.19.0.x` 주소로 일관되게 작동한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: 외부 서비스 EndpointSlice 주소를 `172.19.0.x`로 갱신한다.
  - Vault: `172.19.0.9:8200`
  - PostgreSQL: `172.19.0.11:15432/15433`
  - Valkey: `172.19.0.12:6379` (K8s-side 포트; Docker host publish `26379:6379`는 호스트 접근 전용)
- **REQ-PRD-FUN-02**: NetworkPolicy cidr을 `172.19.0.x` 기준으로 수정한다.
- **REQ-PRD-FUN-03**: `bootstrap-local.sh` 기본값을 `172.19.0.x`로 수정한다.
- **REQ-PRD-FUN-04**: cert-manager v1.17.x를 GitOps 방식으로 설치한다.
- **REQ-PRD-FUN-05**: mkcert rootCA를 cert-manager `ClusterIssuer`로 등록한다.
- **REQ-PRD-FUN-06**: `bootstrap-local.sh`에 rootCA Secret 주입 단계를 추가한다.
- **REQ-PRD-FUN-07**: Kubernetes Dashboard v3.x를 GitOps 방식으로 설치한다.
- **REQ-PRD-FUN-08**: Dashboard를 `dashboard.127.0.0.1.nip.io`(ingress-nginx + cert-manager TLS)로 노출한다.
- **REQ-PRD-FUN-09**: Istio v1.25.x(`istio-base` + `istiod`)를 GitOps 방식으로 설치한다.
  - IngressGateway 비활성화, ingress-nginx와 공존.
  - sidecar injection은 namespace opt-in 방식.
- **REQ-PRD-FUN-10**: Kiali v2.6.x를 GitOps 방식으로 설치한다.
  - 외부 Prometheus/Grafana/Tempo 연동.
  - `kiali.127.0.0.1.nip.io`(ingress-nginx + cert-manager TLS)로 노출.
- **REQ-PRD-FUN-11**: Docker Traefik router를 Dashboard/Kiali용으로 추가한다 (외부 Traefik repo에서 관리).
- **REQ-PRD-FUN-12**: `verify-contracts-static.sh`에 신규 서비스 계약 검증을 추가한다.

## Success Criteria

- **REQ-PRD-MET-01**: 외부 서비스 연결(`172.19.0.x`) 회귀 0건.
- **REQ-PRD-MET-02**: cert-manager `ClusterIssuer` Ready=True.
- **REQ-PRD-MET-03**: `dashboard.127.0.0.1.nip.io` HTTPS 접근 성공(mkcert CA 신뢰).
- **REQ-PRD-MET-04**: Istio `istiod` Deployment Available=True.
- **REQ-PRD-MET-05**: Kiali `kiali.127.0.0.1.nip.io` HTTPS 접근 성공.
- **REQ-PRD-MET-06**: `verify-contracts-static.sh` PASS.
- **REQ-PRD-MET-07**: CI 정적 게이트 전체 PASS.

## Scope and Non-goals

- **In Scope**:
  - IP 수정 (EndpointSlice, NetworkPolicy, bootstrap, verify-contracts)
  - cert-manager + mkcert CA ClusterIssuer
  - Kubernetes Dashboard v3
  - Istio (istio-base + istiod, IngressGateway 제외)
  - Kiali (external observability 연동)
  - Traefik router config (Dashboard/Kiali)
  - 문서 체인 동기화
- **Out of Scope**:
  - 외부 서비스 런타임 자체 배포
  - Istio IngressGateway 활성화
  - GitHub Actions push deploy
  - ArgoCD TLS cert-manager 이관 (후속 Phase)
- **Non-goals**:
  - 프로덕션 환경 보안 강화 (Dashboard OIDC 등)
  - Vault PKI + cert-manager 연동

## Risks, Dependencies, and Assumptions

- **Risk**: IP 수정 후 정적 계약 검증 패턴 누락 시 CI false-negative.
  - **Mitigation**: `verify-contracts-static.sh` 패턴 동시 수정.
- **Risk**: Istio 설치 순서 오류 시 Kiali 동작 불가.
  - **Mitigation**: Plan에서 istio-base → istiod → kiali 순서 명시.
- **Assumption**: mkcert rootCA가 `secrets/certs/rootCA.pem`에 존재한다.
- **Assumption**: Docker infra_net에 Prometheus/Grafana/Tempo가 `172.19.0.20~24`에서 동작 중이다.

## Related Documents

- **ARD**: [`../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md`](../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md)
- **ADR**: [`../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR**: [`../02.architecture/decisions/0007-kubernetes-dashboard-v3.md`](../02.architecture/decisions/0007-kubernetes-dashboard-v3.md)
- **ADR**: [`../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md`](../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR**: [`../02.architecture/decisions/0009-kiali-external-observability.md`](../02.architecture/decisions/0009-kiali-external-observability.md)
- **ADR**: [`../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../02.architecture/decisions/0010-headlamp-replaces-dashboard.md) — REQ-PRD-FUN-07, REQ-PRD-FUN-08의 Dashboard 요구사항을 Headlamp로 대체
- **Spec**: [`../03.specs/003-platform-expansion/spec.md`](../03.specs/003-platform-expansion/spec.md)
- **Plan**: [`../04.execution/plans/2026-03-29-platform-expansion.md`](../04.execution/plans/2026-03-29-platform-expansion.md)
