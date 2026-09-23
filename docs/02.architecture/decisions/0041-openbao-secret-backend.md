---
title: "OpenBao as the Runtime Secret Backend"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "ADR-0041"
supersedes: "ADR-0003"
---

# ADR-0041: OpenBao as the Runtime Secret Backend

## Overview

이 ADR은 런타임 시크릿의 외부 backend를 HashiCorp Vault에서 OpenBao로
바꾼다. External Secrets Operator(ESO)와 Kubernetes Auth로 시크릿을
전달하는 패턴은 ADR-0003에서 그대로
이어받고, backend 제품과 그 접근 주소만 바뀐다. ADR-0003은 이 결정으로
대체된다.

## Context

외부 서비스 workspace(`hy-home.docker`)는 Vault container를 폐지하고
OpenBao를 운영한다. 그 workspace의 현재 사실은 다음과 같다.

- container `openbao`와 `openbao-agent`, image `openbao/openbao:2.6.2`
- k3d 네트워크 `k3d-hyhome`의 고정 주소 `172.18.0.17`, listener `8200`
  (HTTP, local-only)
- 외부 Traefik route `https://openbao.hy.home.arpa`

이 저장소는 여전히 제거된 Vault 주소(`172.18.0.8`)와 host를 desired
state와 bootstrap 기본값으로 두고 있었다. 그 상태에서는 ESO가 존재하지 않는
endpoint를 향한다. OpenBao는 Vault HTTP API, KV v2, Kubernetes auth method와
호환되므로 ESO의 `vault` provider와 기존 ClusterSecretStore가 그대로 동작한다.

## Decision

- 런타임 시크릿의 단일 소스는 외부 OpenBao다. 평문 시크릿은 Git, manifest,
  문서, 로그에 두지 않는다.
- 시크릿 동기화는 ESO `vault` provider로 수행하고, 인증은 Kubernetes Auth
  role `eso-read-platform`(audience `vault`)을 유지한다. 정책은
  namespace/path 단위 least privilege를 적용한다.
- cluster 내부 접근 경로는 `platform` namespace의 `vault-external`
  Service와 EndpointSlice이며, EndpointSlice 주소는 `172.18.0.17`, port는
  `8200`이다. ESO egress NetworkPolicy도 같은 `/32`로 제한한다.
- 호스트 쪽 관리와 bootstrap 접근은 `https://openbao.hy.home.arpa`와 검증된
  CA를 사용한다. cluster 내부 HTTP 경로는 기존과 같은 local-only 예외다.
- Kubernetes 식별자 `vault-external`, `vault-backend`, ESO `vault`
  provider와 KV 경로(`secret/platform/*`, `secret/apps/<app>/config`)는
  바꾸지 않는다. 이 이름들은 API 계약을 가리키며 제품 이름이 아니다.

## Explicit Non-goals

- Kubernetes Service, ClusterSecretStore, NetworkPolicy 이름의 개명
- 시크릿 값 이관, unseal, auth mount와 role 설정 같은 OpenBao 운영 작업.
  이 작업은 외부 workspace 운영자가 소유한다
- cluster 내부 OpenBao 경로의 TLS 전환
- 앱이 OpenBao SDK를 직접 호출하도록 강제하는 것

## Consequences

- **Positive**:
  - desired state, bootstrap, 정적 검증이 실제 외부 runtime과 다시 일치한다.
  - ESO, ClusterSecretStore, ExternalSecret 구성과 KV 경로 계약이 바뀌지 않아
    변경 범위가 endpoint 주소와 host로 한정된다.
- **Trade-offs**:
  - `vault-*` Kubernetes 이름과 제품 이름이 달라져 문서가 둘의 관계를
    명시해야 한다.
  - OpenBao의 Vault API 호환성이 깨지는 upstream 변경이 생기면 ESO provider
    선택을 다시 판단해야 한다.
- **Operational**:
  - OpenBao의 Kubernetes auth `kubernetes_host`, reviewer JWT/CA, role 설정은
    외부 운영자가 이 계약에 맞춰 유지한다. 저장소의 정적 PASS는 이를
    증명하지 않는다.

## Alternatives

### Kubernetes 식별자까지 `openbao-*`로 개명

- Good:
  - 제품 이름과 리소스 이름이 일치한다.
- Bad:
  - ClusterSecretStore, 모든 ExternalSecret, NetworkPolicy, validator를 함께
    바꾸는 live 전환이 필요하고, 그 사이 시크릿 동기화가 끊길 수 있다.

### Vault 유지

- Good:
  - 저장소 변경이 없다.
- Bad:
  - 외부 workspace가 Vault를 폐지했으므로 존재하지 않는 backend를 가리킨다.

## Traceability

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
- **Operations Policy**: [`../../05.operations/policies/0001-k8s-gitops-operations-policy.md`](../../05.operations/policies/0001-k8s-gitops-operations-policy.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| ADR-0003 | Supersedes ADR-0003; the ESO and Kubernetes Auth pattern carries over | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
