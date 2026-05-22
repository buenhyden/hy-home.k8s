---
title: 'Platform Expansion Mesh Dashboard Architecture Reference Document'
type: ard
status: draft
owner: platform-team
updated: 2026-05-22
---

# Platform Expansion: Mesh, Dashboard, cert-manager Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 WSL2 k3d 플랫폼 확장의 참조 아키텍처를 정의한다. cert-manager(TLS 자동화), Kubernetes Dashboard(웹 UI), Istio(서비스메시), Kiali(메시 관측) 추가와 외부 서비스 IP 수정을 포함한다.

> **현재 실행계약 메모 (2026-05-22)**: 이 ARD는 2026-03-29 플랫폼 확장 참조 아키텍처 기록이다. 현재 기본 컨테이너 런타임 전제는 WSL-native Docker이며, 역사적 Docker Desktop 표현은 당시 실행 기준으로만 해석한다. 현재 repo-backed 실행계약은 [ADR-0010](../decisions/0010-headlamp-replaces-dashboard.md)과 현재 `gitops/**` 매니페스트/정적 검증 스크립트가 우선한다. Kubernetes Dashboard는 Headlamp로 대체되었고, 외부 서비스 EndpointSlice/CIDR 계약은 `172.18.x` 기준이다.

## Summary

플랫폼은 기존 5개 평면에 3개 평면을 추가한다.

- **Cluster Plane**: k3d/k3s `1 master + 3 workers` (변경 없음)
- **GitOps Plane**: ArgoCD App-of-Apps + ApplicationSet (변경 없음)
- **Secret Plane**: ESO + Vault Kubernetes auth (변경 없음)
- **External Data Plane**: PostgreSQL/Valkey/Vault endpoint — `172.19.0.x` 갱신
- **CI Control Plane**: GitHub Actions 변경영역 정적 게이트 (변경 없음)
- **Access Plane**: Traefik(443) → k3d(:8443) → ingress-nginx (변경 없음)
- **[NEW] TLS Plane**: cert-manager + mkcert ClusterIssuer
- **[NEW] Mesh Plane**: Istio(istiod) + Kiali
- **[NEW] Observability Access Plane**: Dashboard + Kiali ingress 노출

## Boundaries & Non-goals

- **Owns**:
  - 플랫폼 선언형 리소스 (`gitops/`, `infrastructure/`)
  - 외부 서비스 K8s 인터페이스 계약 (Service/EndpointSlice)
  - TLS 인증서 lifecycle (cert-manager + mkcert CA)
  - 서비스메시 컨트롤 플레인 (Istio istiod)
  - 메시 관측 UI (Kiali)
  - 클러스터 운영 UI (Kubernetes Dashboard)
- **Consumes**:
  - 외부 런타임 (Vault/PostgreSQL/Valkey)
  - 외부 Observability (Prometheus/Grafana/Tempo/Alloy)
  - WSL2 + Docker Desktop 실행 환경
  - Docker Traefik (외부 노출 경로)
- **Does Not Own**:
  - 외부 서비스 컨테이너 라이프사이클
  - 외부 Traefik 라우팅 파일 (별도 repo)
  - Istio IngressGateway
- **Non-goals**:
  - 멀티클러스터 Istio federation
  - Ambient mesh
  - Vault PKI + cert-manager 연동

## Quality Attributes

- **Performance**: WSL2 자원 예산 내 제어면 안정 유지. Istio sidecar opt-in으로 불필요한 자원 소모 방지.
- **Security**: mkcert CA 신뢰 체인 유지. RBAC 최소권한. Dashboard는 로컬 전용 cluster-admin. sidecar mTLS는 opt-in namespace 적용.
- **Reliability**: ArgoCD self-heal 유지. cert-manager 인증서 자동 갱신.
- **Scalability**: Git generator ApplicationSet으로 신규 앱 확장 가능. cert-manager Certificate CR 선언적 추가.
- **Observability**: Kiali → Prometheus/Grafana/Tempo 연동. Dashboard에서 Pod/Service 상태 확인.
- **Operability**: bootstrap-local.sh에서 rootCA 주입 단계 추가. 현재 docs taxonomy 추적성 유지.

## System Overview & Context

```text
Host (Windows + WSL2)
  └─ Docker Desktop
       ├─ infra_net (172.19.0.0/16)
       │    ├─ Traefik (443) ──────────────────┐
       │    ├─ Vault (172.19.0.9:8200)         │
       │    ├─ PostgreSQL (172.19.0.11:15432/3) │
       │    ├─ Valkey (172.19.0.12:6379)        │
       │    ├─ Prometheus (172.19.0.20:9090)    │
       │    ├─ Loki (172.19.0.21:3100)          │
       │    ├─ Tempo (172.19.0.22:3200)         │
       │    ├─ Alloy (172.19.0.23:4317/4318)   │
       │    └─ Grafana (172.19.0.24:3000)       │
       └─ k3d cluster (172.18.0.0/16)          │
            ├─ ingress-nginx (LoadBalancer :443) ◄─┘
            │    ├─ argocd.127.0.0.1.nip.io
            │    ├─ dashboard.127.0.0.1.nip.io  [NEW]
            │    └─ kiali.127.0.0.1.nip.io      [NEW]
            ├─ argocd (namespace)
            │    └─ ArgoCD + GitOps
            ├─ cert-manager (namespace)          [NEW]
            │    └─ cert-manager + ClusterIssuer(mkcert CA)
            ├─ kubernetes-dashboard (namespace)  [NEW]
            │    └─ Dashboard v3
            ├─ istio-system (namespace)          [NEW]
            │    ├─ istiod
            │    └─ Kiali
            ├─ platform (namespace)
            │    ├─ ESO + VaultSecretStore
            │    └─ External Services (Service+EndpointSlice)
            └─ external-secrets (namespace)
```

## Data Architecture

- **Key Flows**:
  - cert-manager: `Certificate CR → ClusterIssuer(mkcert CA) → TLS Secret → ingress`
  - Dashboard: `ingress-nginx → Dashboard Service → K8s API`
  - Kiali: `ingress-nginx → Kiali Service → Istio metrics + Prometheus(172.19.0.20)`
  - Istio: `Pod(sidecar) ↔ istiod(xDS) → mTLS, traffic policy`
- **Storage Strategy**:
  - cert-manager: TLS Secret을 대상 namespace에 생성
  - Dashboard: 상태 없음, K8s API read-only
  - Istio: istiod config 저장 없음 (xDS 동적 구성)
  - Kiali: 상태 없음, Prometheus/Grafana 외부 참조

## Infrastructure & Deployment

- **Runtime / Platform**: k3s v1.35.0+k3s1, k3d v5.8.3
- **cert-manager**: v1.17.x via `https://charts.jetstack.io`
- **Kubernetes Dashboard**: v3.x via `https://kubernetes.github.io/dashboard`
- **Istio**: v1.25.x via `https://istio-release.storage.googleapis.com/charts`
- **Kiali**: v2.6.x via `https://kiali.org/helm-charts`
- **Deployment Model**: ArgoCD GitOps (App-of-Apps 확장)
- **Operational Evidence**: `verify-contracts-static.sh`, `verify-ingress-tls.sh`, `run-all.sh`

## Related Documents

- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ADR**: [`../decisions/0006-cert-manager-mkcert-ca-issuer.md`](../decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **Historical/Superseded ADR**: [`../decisions/0007-kubernetes-dashboard-v3.md`](../decisions/0007-kubernetes-dashboard-v3.md)
- **ADR**: [`../decisions/0008-istio-install-and-ingress-coexist.md`](../decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR**: [`../decisions/0009-kiali-external-observability.md`](../decisions/0009-kiali-external-observability.md)
- **Current ADR**: [`../decisions/0010-headlamp-replaces-dashboard.md`](../decisions/0010-headlamp-replaces-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-29-platform-expansion.md`](../../04.execution/plans/2026-03-29-platform-expansion.md)
