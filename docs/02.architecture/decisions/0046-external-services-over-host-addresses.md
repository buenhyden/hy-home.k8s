---
title: "External Services Reached Through Host-Published Addresses"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "ADR-0046"
---

# ADR-0046: External Services Reached Through Host-Published Addresses

## Overview

이 ADR은 cluster가 외부 서비스 workspace(`hy-home.docker`)의 서비스에 닿는
경로를 바꾼다. 외부 backend를 쓴다는 결정([ADR-0041](./0041-openbao-secret-backend.md),
[ADR-0044](./0044-stateful-data-stores-stay-external.md),
[ADR-0045](./0045-in-cluster-telemetry-collection.md))은 그대로 두고, 공유
docker network `k3d-hyhome`의 container 주소 대신 host가 공개한 주소와 port를
쓴다.

## Context

2026-09-23 기준 상태는 다음과 같다.

- 외부 workspace는 소유자 지시로 모든 Compose 서비스를 `k3d-hyhome`에서
  분리했다(`hy-home.docker` commit `f6d481e74`, PR #218). 고정 주소, Traefik
  k3d route, Prometheus NodePort job, k8s dashboard와 alert rule이 사라졌다.
  이미 실행 중인 container는 재생성될 때까지 기존 주소를 유지한다.
- 이 저장소의 external service 계약은 모두 `172.18.0.x` container 주소였다.
  container가 재생성되면 ESO, ArgoCD Valkey, 로그 수집, Kiali가 함께 끊긴다.
- host 주 주소는 `192.168.0.13`이고 외부 Traefik이 그 주소의 `80/443`에
  bind한다. `k3d-hyhome`에서 그 주소로 닿는 port는 다음과 같다.
  - 열림: `443`(Traefik), `3100`(Loki), `3200`(Tempo), `26379`(`mng-valkey`),
    `25432`(`mng-pg`), `6550`(k3d API)
  - 닫힘: `9090`(Prometheus, host 공개 없음), `3000`(Grafana, host 공개
    없음), `4317`(Alloy OTLP, 공개되었으나 연결 거부), `15432/15433`
    (`pg-router`, profile `postgres-ha` 중지)
- Traefik의 Prometheus route는 SSO middleware 뒤에 있어 machine client가 쓸 수
  없다. OpenBao와 Grafana route는 SSO가 없다.
- k3d API 인증서 SAN에는 `192.168.0.13`이 없다. OpenBao가 `k3d-hyhome`을
  떠나면 `k3d-hyhome-server-0` 이름으로 API에 닿을 수 없다.

## Decision

- cluster는 외부 서비스에 host 주소 `192.168.0.13`과 host 공개 port로
  닿는다. `platform` namespace의 `*-external` Service 이름은 유지하고
  EndpointSlice 주소와 port만 바꾼다. Service port와 host port가 다르면
  Service `targetPort`가 host port를 가리킨다.
  - Valkey(`mng-valkey`): `192.168.0.13:26379`
  - PostgreSQL(`pg-router`): `192.168.0.13:15432`(write), `15433`(read)
  - Loki `3100`, Tempo `3200`, Alloy OTLP `4317/4318`
  - Prometheus `9090`, Grafana `3000`: 외부 workspace가 host에 공개해야
    동작한다
- ESO는 OpenBao에 `https://openbao.hy.home.arpa`(외부 Traefik)로 닿고,
  mkcert root CA로 인증서를 검증한다. cluster 안에서 그 이름은 CoreDNS
  custom zone이 `192.168.0.13`으로 푼다. `vault-external` Service와
  EndpointSlice, 그리고 cluster 내부 HTTP local-only 예외는 폐지한다.
- k3d API는 `192.168.0.13:6550`에만 bind하고 그 주소를 인증서 SAN에 둔다.
  OpenBao Kubernetes auth의 `kubernetes_host`는
  `https://192.168.0.13:6550`이다.
- NetworkPolicy egress는 `192.168.0.13/32`와 필요한 port만 허용한다.
- PostgreSQL은 bootstrap 필수 의존성이 아니다. `postgresql-cluster`는
  서비스용 DB이고 profile이 꺼져 있을 수 있으므로 bootstrap은 경고만 한다.
  `mng-pg`는 외부 workspace의 관리용 DB라 이 저장소의 계약이 아니다.

## Explicit Non-goals

- 외부 workspace의 port 공개, bind 주소, Traefik route 변경. Prometheus와
  Grafana의 host 공개는 외부 workspace에 요청하는 작업이다
- Alloy OTLP `4317` 연결 거부의 원인 수정
- 외부 backend를 cluster 안으로 옮기는 것

## Consequences

- **Positive**:
  - 두 workspace가 docker network와 container 주소를 공유하지 않는다.
    container 재생성이 cluster 계약을 깨지 않는다.
  - ESO와 OpenBao 사이의 cluster 내부 HTTP 예외가 사라지고 TLS로 검증한다.
- **Trade-offs**:
  - 계약이 외부 workspace의 host port 공개에 의존한다. port가 loopback으로
    좁혀지면 cluster에서 닿지 않는다.
  - CoreDNS custom zone과 root CA ConfigMap을 bootstrap이 관리해야 한다.
  - k3d API bind 변경은 cluster 재생성이 필요하다.
- **Operational**:
  - operator는 OpenBao `kubernetes_host`를 새 주소로 바꾼다.
  - Prometheus와 Grafana가 host에 공개되기 전에는 remote write와 Kiali
    메트릭 조회가 동작하지 않는다.

## Alternatives

### cluster가 외부에 의존하지 않도록 자립

- Good:
  - 외부 workspace 변경의 영향을 받지 않는다.
- Bad:
  - ADR-0041, ADR-0044, ADR-0045를 모두 뒤집고 저장 backend와 시크릿
    backend를 cluster 안에 새로 소유해야 한다.

### 외부 workspace의 `k3d-hyhome` 연결 복원

- Good:
  - 이 저장소의 변경이 없다.
- Bad:
  - 외부 workspace 소유자의 결정과 충돌한다.

## Traceability

**Current-state clarification (2026-09-23).** The external workspace chose
not to publish Prometheus `9090` or Grafana `3000` on the host. Prometheus
exposes only its HTTP API through the external Traefik at
`https://prometheus.hy.home.arpa/api/v1/`, with Basic Auth
(`hy-home.docker` PR #222). Grafana is reached at `https://grafana.hy.home.arpa`. So the
`prometheus-external` and `grafana-external` Services are retired, and Alloy,
Kiali and the Rollouts controller call those names directly:

- The CoreDNS custom zone resolves the names to the host address.
- The Basic Auth credentials come from OpenBao `platform/prometheus-api`
  through ESO.
- The gateway CA comes from bootstrap-created ConfigMaps (`hy-home-root-ca`,
  `kiali-cabundle`).
- Egress uses `192.168.0.13:443`.

Every other clause of this decision is unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0041-openbao-secret-backend.md`](./0041-openbao-secret-backend.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0041](./0041-openbao-secret-backend.md) | Keeps OpenBao as the secret backend; replaces the cluster-internal `vault-external` HTTP path with HTTPS through the external Traefik | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [ADR-0044](./0044-stateful-data-stores-stay-external.md) | Keeps PostgreSQL and Valkey external; moves their endpoints from container addresses to host-published ports | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [ADR-0045](./0045-in-cluster-telemetry-collection.md) | Keeps in-cluster collection with an external backend; moves the backend endpoints to host-published ports | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
