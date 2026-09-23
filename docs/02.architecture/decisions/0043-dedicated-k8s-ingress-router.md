---
title: "Dedicated Kubernetes Ingress Router on hy-k8s.home.arpa"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "ADR-0043"
---

# ADR-0043: Dedicated Kubernetes Ingress Router on hy-k8s.home.arpa

## Overview

이 ADR은 k8s가 제공하는 UI와 앱에 외부 서비스 workspace의 Traefik과 분리된
진입점과 domain을 부여한다. k8s host 이름은 `<name>.hy-k8s.home.arpa`이고,
진입점은 전용 host IP `192.168.0.14`에 bind한 k3d serverlb다. ArgoCD UI는
`argo.hy-k8s.home.arpa`다.
[ADR-0042](./0042-linux-server-single-host-baseline.md)가 local UI domain으로
정한 `hy.home.arpa`는 외부 서비스 workspace의 host 이름에만 남는다.

## Context

- 외부 서비스 workspace(`hy-home.docker`)의 Traefik은 host의 `0.0.0.0:80`과
  `0.0.0.0:443`을 점유한다. k3d 설정도 serverlb에 `80:80`, `443:443`을
  매핑하므로 두 진입점은 같은 host 주소에서 공존할 수 없다.
- k8s route는 그 Traefik의 file provider에 둔 dynamic config를 거쳐 k3d로
  전달되었다. 이 저장소의 `traefik/` reference 파일과 외부 workspace의 실제
  파일이 backend를 서로 다르게 적었고, k8s route를 바꿀 때마다 두 저장소를
  함께 고쳐야 했다.
- ingress-nginx는 MetalLB `172.18.0.240`의 LoadBalancer Service다. 이 주소는
  Docker bridge `k3d-hyhome` 위에 있어 server 자신만 도달할 수 있고 LAN
  client는 도달할 수 없다.
- host는 `enp4s0`에 정적 주소 `192.168.0.13/24`를 쓰며, 결정 시점에
  `192.168.0.14`는 ARP 응답이 없었다.

## Decision

- k8s가 제공하는 host 이름은 `<name>.hy-k8s.home.arpa`다. 현재 이름은
  `argo`(ArgoCD), `kiali`, `headlamp`, `rollouts`, `adminer`이며 새 앱은
  `<appname>.hy-k8s.home.arpa`를 쓴다. 이 subdomain이 앱이 응답하는 기준
  주소다.
- apex `hy-k8s.home.arpa/<name>` 요청은 ingress-nginx
  `permanent-redirect` annotation으로 `https://<name>.hy-k8s.home.arpa/`에
  301로 넘긴다. 앱의 root path 설정은 바꾸지 않으며 snippet annotation은 쓰지
  않는다. TLS 인증서의 SAN은 apex와 앱 subdomain을 함께 담는다.
- k8s 전용 진입점은 k3d serverlb다. serverlb는 host의 `192.168.0.14:80`과
  `192.168.0.14:443`만 bind하고, 이를 ingress-nginx의 고정 NodePort `30080`과
  `30443`으로 전달한다. TLS는 ingress-nginx가 종료한다.
- ingress-nginx Service는 LoadBalancer(`172.18.0.240`)를 유지한다. 이 주소는
  server 내부 검증 경로다.
- 외부 서비스 workspace의 Traefik은 k8s route를 싣지 않는다. 이 저장소의
  `traefik/` reference 파일과 sample app의 Traefik 예시는 폐지한다.
- `192.168.0.14`의 host 주소 할당, `*.hy-k8s.home.arpa` 이름 해석, 외부
  Traefik을 `192.168.0.13`에만 bind하는 변경은 operator와 외부 workspace가
  소유한다. 저장소 정적 검증은 이 상태를 증명하지 않는다.

## Explicit Non-goals

- 외부 서비스(OpenBao, Grafana, Keycloak 등)의 host 이름 변경
- ingress controller 교체나 Gateway API 도입
- 공인 인증서, ACME, wildcard DNS 서버 운영
- MetalLB address pool 변경

## Consequences

- **Positive**:
  - k8s route의 추가와 변경이 이 저장소의 Ingress 선언만으로 끝난다.
  - 두 진입점이 서로 다른 host 주소를 가지므로 host port 충돌이 사라진다.
  - k8s와 외부 서비스의 domain이 분리되어 어느 router가 응답하는지 이름으로
    구분된다.
- **Trade-offs**:
  - host에 두 번째 주소가 필요하고, LAN client는 `hy-k8s.home.arpa` 이름을
    `192.168.0.14`로 해석해야 한다.
  - 기존 `*.hy.home.arpa` k8s 주소로 들어오던 client는 새 이름으로 옮겨야 한다.
- **Operational**:
  - k3d serverlb의 host 주소는 cluster 생성 시점에 고정된다. 주소를 바꾸려면
    cluster를 다시 만들어야 한다.

## Alternatives

### 외부 Traefik이 계속 k8s route를 전달

- Good:
  - host 주소나 DNS 변경이 없다.
- Bad:
  - k8s route마다 두 저장소를 함께 바꿔야 하고, 요청 owner가 명시적으로
    배제했다.

### 같은 host 주소의 대체 port(`8443`)

- Good:
  - host 네트워크 변경이 없다.
- Bad:
  - 모든 URL에 port가 붙고, 표준 port를 기대하는 client와 OAuth redirect
    설정이 복잡해진다.

### MetalLB 주소를 이름으로 직접 해석

- Good:
  - 추가 router가 없다.
- Bad:
  - Docker bridge 주소라 LAN client가 도달하지 못한다.

## Traceability

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0042-linux-server-single-host-baseline.md`](./0042-linux-server-single-host-baseline.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0042](./0042-linux-server-single-host-baseline.md) | Narrows ADR-0042's `hy.home.arpa` clause to external service hosts; k8s hosts move to `hy-k8s.home.arpa` | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
