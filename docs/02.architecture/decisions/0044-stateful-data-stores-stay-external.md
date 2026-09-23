---
title: "Stateful Data Stores Stay Outside the Cluster"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "ADR-0044"
---

# ADR-0044: Stateful Data Stores Stay Outside the Cluster

## Overview

이 ADR은 외부 서비스 workspace(`hy-home.docker`)의 `postgresql-cluster`와
`valkey-cluster`를 k3d cluster로 옮길지 검토한 결과를 기록한다. 두 cluster는
외부 workspace에 남고, 이 저장소는 기존처럼 Service와 EndpointSlice 계약으로만
연결한다.

## Context

2026-09-23 기준 두 workspace의 상태는 다음과 같다.

- `postgresql-cluster`는 Spilo(Patroni) 3개, etcd 3개, HAProxy `pg-router`로
  이루어진다. opt-in profile `postgres-ha`로만 기동하며 결정 시점에는
  중지되어 있었다. k3d network에는 `pg-router`만 `172.18.0.15`로 연결된다.
- 외부 workspace의 앱(keycloak, dbt, mlflow)은 standalone `mng-pg`를 쓴다.
  `postgresql-cluster`의 소비자는 이 저장소의 `postgres-app-secret`과 adminer
  workload뿐이다.
- `valkey-cluster`는 6노드 cluster 모드이고 `lab_net`에만 연결된다. 두
  workspace 어디에도 소비자가 없다. 이 저장소의 ArgoCD가 쓰는 Valkey
  (`172.18.0.9`)는 standalone `mng-valkey`다.
- 두 cluster의 데이터는 host bind 디렉터리에 저장된다. 이 저장소에는 PVC,
  StorageClass, k3d host volume 매핑이 없다. k3d 기본 local-path 볼륨은 노드
  container 안에 있어 cluster를 다시 만들면 사라진다.

## Decision

- `postgresql-cluster`, `valkey-cluster`, `mng-pg`, `mng-valkey`는 외부
  workspace에 남는다. 이 저장소는 그 runtime을 소유하지 않는다.
- PostgreSQL 계약은 `pg-router`(`172.18.0.15:15432/15433`)이고, 이 계약이
  동작하려면 외부 workspace의 profile `postgres-ha`가 기동되어 있어야 한다.
- Valkey 계약은 `mng-valkey`(`172.18.0.9:6379`)다. `valkey-cluster`는 이
  저장소의 계약이 아니다.

## Explicit Non-goals

- 외부 workspace의 cluster 구성, 백업, profile 변경
- 이 저장소 안의 PostgreSQL operator, StorageClass, 백업 체계 도입
- `valkey-cluster`의 유지 또는 폐지 결정. 외부 workspace가 소유한다

## Consequences

- **Positive**:
  - 데이터 수명이 k3d cluster 재생성과 분리된다.
  - 이 저장소가 stateful operator와 백업을 새로 소유하지 않는다.
- **Trade-offs**:
  - PostgreSQL 계약은 외부 workspace의 opt-in profile에 의존하며, 그 profile이
    꺼져 있으면 정적 PASS와 달리 live 연결은 실패한다.
- **Operational**:
  - bootstrap과 live 검증 전에 operator가 `pg-router`와 `mng-valkey` 기동을
    확인한다.

## Alternatives

### 두 cluster를 k8s로 이전

- Good:
  - IP 기반 교차 저장소 계약이 사라지고 lifecycle이 GitOps로 관리된다.
- Bad:
  - k3d 노드는 같은 host의 container라 Patroni와 etcd 3중화의 가용성 이점이
    없다.
  - persistent storage, operator, 백업을 새로 도입해야 하고 cluster 재생성 때
    데이터를 잃을 위험이 생긴다.
  - `valkey-cluster`는 소비자가 없다.

### PostgreSQL 계약을 `mng-pg`로 변경

- Good:
  - 항상 기동된 DB를 쓴다.
- Bad:
  - 외부 workspace의 운영 관리 DB와 k8s 앱 데이터를 한 instance에 섞는다.

## Traceability

**Current-state clarification (2026-09-23).** The endpoints
above move from container addresses to host-published ports on
`192.168.0.13` under [ADR-0046](./0046-external-services-over-host-addresses.md): `mng-valkey` at `26379`
and `pg-router` at `15432/15433`. The bootstrap no longer requires
`pg-router`. The placement decision is unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0014](./0014-current-local-gitops-platform-contract.md) | Confirms ADR-0014's external service contract for PostgreSQL and Valkey; replaces nothing | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
