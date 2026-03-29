# ADR-0006: cert-manager with mkcert CA as ClusterIssuer

## Overview (KR)

이 ADR은 cert-manager를 플랫폼 TLS 인증서 관리 컴포넌트로 도입하고, mkcert가 생성한 rootCA를 cert-manager `ClusterIssuer`(CA 타입)로 등록하는 결정을 기록한다.

## Context

플랫폼 확장(Kubernetes Dashboard, Istio/Kiali)으로 TLS가 필요한 ingress가 증가한다.
기존에는 `bootstrap-local.sh`에서 mkcert 인증서를 수동으로 K8s Secret에 주입했으나, 서비스가 늘어날수록 수동 주입 부담이 증가한다.
mkcert rootCA는 이미 로컬 신뢰 저장소에 등록되어 있으므로, cert-manager가 동일 rootCA로 인증서를 발급하면 추가 브라우저 설정 없이 모든 신규 서비스 TLS가 신뢰된다.

## Decision

- cert-manager v1.17.x를 플랫폼 컴포넌트로 GitOps 방식으로 설치한다.
- mkcert rootCA(`secrets/certs/rootCA.pem`)를 `cert-manager` namespace의 K8s Secret으로 bootstrap 단계에 주입한다.
- cert-manager `ClusterIssuer`를 CA 타입으로 생성하고 해당 Secret을 참조한다.
- **신규 서비스**(Dashboard, Kiali)는 cert-manager `Certificate` CR로 TLS 인증서를 발급한다.
- **기존 ArgoCD**는 `argocd-local-tls` 수동 주입 방식을 유지한다(동작 보전, 후속 Phase에서 이관 가능).
- ACME/Let's Encrypt는 사용하지 않는다(로컬 nip.io 도메인 부적합).

## Explicit Non-goals

- ACME/Let's Encrypt 통합
- cert-manager를 이용한 ArgoCD 기존 TLS 즉시 이관 (후속 Phase)
- 멀티 ClusterIssuer 운영
- Vault PKI를 cert-manager issuer로 연동

## Consequences

- **Positive**:
  - 신규 서비스 TLS 발급이 선언형 GitOps 방식으로 자동화된다.
  - mkcert rootCA 신뢰가 모든 cert-manager 발급 인증서에 전파된다.
  - 브라우저 추가 설정 없이 Dashboard, Kiali HTTPS 접근 가능.
- **Trade-offs**:
  - bootstrap 단계에 rootCA Secret 주입 단계가 추가된다.
  - ArgoCD TLS가 cert-manager와 수동 주입 혼용 상태로 일시 유지된다.
  - cert-manager CRD가 AppProject clusterResourceWhitelist에 추가 필요.

## Alternatives

### 수동 mkcert 인증서 주입 유지

- Good: bootstrap 단순, cert-manager 불필요
- Bad: 서비스 증가 시 수동 작업 부담 선형 증가, GitOps 선언성 저하

### Vault PKI 연동

- Good: 엔터프라이즈급 PKI 관리
- Bad: 로컬 개발 환경에 과도한 복잡도, Vault PKI 설정 추가 필요

### Self-signed Issuer (cert-manager 자체 생성)

- Good: rootCA 주입 불필요
- Bad: 브라우저 신뢰 불가, 로컬 신뢰 저장소 재등록 필요

## Related Documents

- **PRD**: [`../01.prd/2026-03-29-platform-expansion-dashboard-mesh.md`](../01.prd/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../02.ard/0003-platform-expansion-mesh-dashboard.md`](../02.ard/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../04.specs/003-platform-expansion/spec.md`](../04.specs/003-platform-expansion/spec.md)
- **Related ADR**: [`./0007-kubernetes-dashboard-v3.md`](./0007-kubernetes-dashboard-v3.md)
- **Related ADR**: [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md)
