---
title: 'ADR-0010: Headlamp Replaces Kubernetes Dashboard'
type: adr
status: accepted
owner: platform
updated: 2026-05-21
---

# ADR-0010: Headlamp Replaces Kubernetes Dashboard

## Overview (KR)

Kubernetes Dashboard v3을 제거하고 Headlamp으로 교체한다.
Headlamp는 더 가벼운 RBAC 기반 인증, 플러그인 확장, 단순한 배포 구조를 제공한다.

## Context

K8s Dashboard v3는 Kong Gateway를 내부 의존성으로 포함하고 있어 리소스 소비가 크다.
또한 helm chart repository(`kubernetes.github.io/dashboard`)가 비활성화되어 `404 Not Found`가 발생했다.
Headlamp는 CNCF 프로젝트로, 경량 단일 컨테이너 구성과 ServiceAccount Token 인증을 사용한다.

## Decision

- Kubernetes Dashboard (`platform-dashboard-app.yaml`, `platform-dashboard-config-app.yaml`)를 제거한다.
- Headlamp v0.41.0을 `headlamp` namespace에 설치한다 (chart: `kubernetes-sigs.github.io/headlamp/`).
- `headlamp.127.0.0.1.nip.io`로 ingress-nginx + Traefik 라우팅을 구성한다.
- cert-manager `mkcert-ca-issuer`로 TLS를 자동 발급한다.

## Explicit Non-goals

- Headlamp 플러그인 개발
- 멀티클러스터 Headlamp 연결
- OIDC 인증 (로컬 플랫폼은 ServiceAccount Token 방식)

## Consequences

- `kubernetes-dashboard` namespace 및 관련 RBAC 제거
- AppProject `sourceRepos`에서 dashboard repo 제거, headlamp repo 추가
- 외부 Traefik artifact `headlamp-k3d.yaml` 필요 (별도 Traefik 레포 적용)
- Vault/ESO 시크릿 변경 없음

## Alternatives

| 옵션                  | 평가                                                          |
| --------------------- | ------------------------------------------------------------- |
| K8s Dashboard v3 유지 | chart repo 비활성화, Kong 의존성으로 리소스 과다, 유지 어려움 |
| Headlamp              | CNCF 프로젝트, 경량, 단순 SA 토큰 인증, 플러그인 확장 가능    |
| Octant                | 개발 중단됨                                                   |

## Status

Accepted — 2026-03-30

## Related Documents

- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../requirements/0003-platform-expansion-mesh-dashboard.md`](../requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-29-platform-expansion.md`](../../04.execution/plans/2026-03-29-platform-expansion.md)
- **Task**: [`../../04.execution/tasks/2026-03-29-platform-expansion.md`](../../04.execution/tasks/2026-03-29-platform-expansion.md)
- **Superseded ADR**: [`./0007-kubernetes-dashboard-v3.md`](./0007-kubernetes-dashboard-v3.md)
