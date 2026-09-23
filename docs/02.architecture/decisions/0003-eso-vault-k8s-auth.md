---
title: "ESO + Vault Kubernetes Auth for Runtime Secrets"
version: "1.1.0"
type: "sdlc/architecture-decision"
status: "superseded"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "ADR-0003"
superseded_by: "ADR-0041"
---

# ADR-0003: ESO + Vault Kubernetes Auth for Runtime Secrets

## Overview

이 ADR은 런타임 시크릿 전달 패턴으로 External Secrets Operator와 Vault Kubernetes Auth를 채택한다.

이 결정은 [ADR-0041](./0041-openbao-secret-backend.md)로 대체되었다. ESO와 Kubernetes Auth 패턴은 ADR-0041이 이어받고, backend는 OpenBao로 바뀌었다.

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

## Traceability

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **ARD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../../98.archive/README.md#document-index)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0041](./0041-openbao-secret-backend.md) | Supersedes this decision; the ESO and Kubernetes Auth pattern carries over with OpenBao as the backend | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
