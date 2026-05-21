---
title: 'ADR-0007: Kubernetes Dashboard v3 Installation'
type: adr
status: superseded
owner: platform-team
updated: 2026-05-21
---

# ADR-0007: Kubernetes Dashboard v3 Installation

## Overview (KR)

이 ADR은 Kubernetes Dashboard를 v3 Helm chart 기반으로 설치하고, ingress-nginx + cert-manager를 통해 `k8s-dashboard.127.0.0.1.nip.io`로 노출하는 결정을 기록한다.

> **Superseded (2026-05-09)**: 현재 실행계약은 [ADR-0010](./0010-headlamp-replaces-dashboard.md)이 우선한다. Kubernetes Dashboard는 Headlamp로 대체되었고, 현재 매니페스트/검증 스크립트는 `platform-headlamp*`, `headlamp` namespace, `headlamp.127.0.0.1.nip.io`를 기준으로 한다.

## Context

플랫폼 운영자가 클러스터 워크로드 상태를 웹 UI로 확인할 수 있어야 한다.
v2(standalone)는 지원이 종료되었으며, v3는 chart 기반 설치를 지원하여 GitOps 관리가 가능하다.
Docker Traefik은 `k8s-dashboard.127.0.0.1.nip.io`를 k3d ingress로 프록시하는 router를 관리한다.

## Decision

- Kubernetes Dashboard v3.x(`kubernetes/dashboard` Helm chart)를 `kubernetes-dashboard` namespace에 설치한다.
- Helm repo: `https://kubernetes.github.io/dashboard`
- 인증 방식: ServiceAccount Bearer Token (로컬 운영 기준 충족).
- 인그레스: `ingress-nginx`, hostname `k8s-dashboard.127.0.0.1.nip.io`.
- TLS: cert-manager `ClusterIssuer`(mkcert CA)로 발급.
- RBAC: 별도 `dashboard-admin` ServiceAccount + `cluster-admin` ClusterRoleBinding (로컬 전용).
- 외부 노출: Docker Traefik router `dashboard-k3d` 추가 (별도 Traefik repo 관리).

## Explicit Non-goals

- 프로덕션 환경 Dashboard 운영 (인증 강화 필요)
- OIDC/OAuth 연동 (로컬 전용)
- v2 Dashboard 유지 또는 혼용

## Consequences

- **Positive**:
  - GitOps 방식으로 Dashboard 수명주기 관리.
  - cert-manager TLS로 HTTPS 자동화.
  - `k8s-dashboard.127.0.0.1.nip.io`에서 mkcert rootCA 신뢰 HTTPS 접근 가능.
- **Trade-offs**:
  - `cluster-admin` 권한 부여는 로컬 전용으로 제한 (프로덕션에서는 최소권한 재검토 필요).
  - Traefik router 추가를 외부 repo에서 별도 관리해야 함.

## Alternatives

### v2 standalone

- Good: 기존 숙련도
- Bad: 지원 종료, chart 없음

### Lens / k9s

- Good: 로컬 클라이언트 도구로 더 강력
- Bad: 웹 UI가 아님, Traefik 노출 불필요

## Status

Superseded by [ADR-0010](./0010-headlamp-replaces-dashboard.md) — 2026-05-09

## Related Documents

- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../requirements/0003-platform-expansion-mesh-dashboard.md`](../requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Replacement ADR**: [`./0010-headlamp-replaces-dashboard.md`](./0010-headlamp-replaces-dashboard.md)
- **Related ADR**: [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md)
