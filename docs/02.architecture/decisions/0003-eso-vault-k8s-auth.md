---
title: 'ADR-0003: ESO + Vault Kubernetes Auth for Runtime Secrets'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-05-18
---

# ADR-0003: ESO + Vault Kubernetes Auth for Runtime Secrets

## Overview

이 ADR은 런타임 시크릿 전달 패턴으로 External Secrets Operator와 Vault Kubernetes Auth를 채택한다.

## Context

GitOps 환경에서 시크릿 원문이 Git에 저장되지 않으면서도 선언형 동기화가 가능해야 한다.

## Decision

- 시크릿 동기화는 ESO를 사용한다.
- Vault 인증은 Kubernetes Auth 방식으로 수행한다.
- Vault 정책은 namespace/path 단위 least privilege를 적용한다.
- SecretStore/ClusterSecretStore 사용 기준을 문서화한다.

## Explicit Non-goals

- static sealed secrets only 방식 고정
- 앱 단 직접 Vault SDK 호출 강제

## Consequences

- **Positive**:
  - Git 비밀 노출 위험 감소
  - 런타임 최소권한 접근 제어 가능
- **Trade-offs**:
  - ESO/Vault 연계 장애 시 동기화 실패 가능성

## Alternatives

### ArgoCD Vault Plugin only

- Good:
  - 렌더 단계 주입 단순화
- Bad:
  - repo-server 의존 및 운영 복잡도 증가

### Kubernetes Secret 수동 관리

- Good:
  - 초기 구성 단순
- Bad:
  - 회전/감사/일관성 취약

## Related Documents

- **PRD**: [`../../01.requirements/2026-06-02-current-local-gitops-platform.md`](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
- **ARD**: [`../requirements/0007-current-local-gitops-platform.md`](../requirements/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
