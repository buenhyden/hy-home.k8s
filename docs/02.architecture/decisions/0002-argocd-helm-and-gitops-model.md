---
title: 'ADR-0002: ArgoCD Helm Install with App-of-Apps and ApplicationSet'
type: adr
status: accepted
owner: platform
updated: 2026-05-18
---

# ADR-0002: ArgoCD Helm Install with App-of-Apps and ApplicationSet

## Overview (KR)

이 ADR은 ArgoCD 설치 방식을 Helm 기반으로 확정하고, App-of-Apps + ApplicationSet + AppProject 스코핑 모델을 채택한다.

## Context

외부 Valkey 백엔드 설정, 버전 업그레이드, 선언형 재현성을 고려하면 raw manifest보다 Helm values 관리가 유리하다.

## Decision

- ArgoCD는 Helm chart로 설치/업그레이드한다.
- 루트 App-of-Apps 애플리케이션을 통해 하위 플랫폼/앱 애플리케이션을 관리한다.
- ApplicationSet Git generator를 사용해 앱 선언을 자동화한다.
- AppProject를 `platform`, `apps`로 분리하고 `sourceRepos/destinations/roles` 최소권한을 적용한다.

## Explicit Non-goals

- 멀티 클러스터 관리 확장
- ArgoCD 플러그인 생태계 확장

## Consequences

- **Positive**:
  - 설치/업그레이드/롤백 표준화
  - 프로젝트 경계 기반 권한 분리가 명확해짐
- **Trade-offs**:
  - Helm values 스키마 추적 유지 필요

## Alternatives

### Raw install.yaml + kustomize patch

- Good:
  - 공식 매니페스트 직결
- Bad:
  - 외부 백엔드/설정 확장 시 패치 복잡도 증가

### ArgoCD operator 중심 설치

- Good:
  - operator-managed lifecycle
- Bad:
  - 학습/운영 복잡도 증가, 로컬 범위 대비 과도

## Related Documents

- **PRD**: [`../../01.requirements/2026-06-02-current-local-gitops-platform.md`](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
- **ARD**: [`../requirements/0007-current-local-gitops-platform.md`](../requirements/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
