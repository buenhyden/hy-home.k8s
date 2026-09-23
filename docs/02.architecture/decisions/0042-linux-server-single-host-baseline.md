---
title: "Linux Server Single-Host Baseline"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "ADR-0042"
---

# ADR-0042: Linux Server Single-Host Baseline

## Overview

이 ADR은 로컬 GitOps 플랫폼의 host를 WSL2가 아닌 Linux server로 기록한다.
[ADR-0014](./0014-current-local-gitops-platform-contract.md)의 host 조항
"WSL2 + WSL-native Docker"만 이 결정이 이어받고, k3d, ArgoCD App-of-Apps,
외부 서비스 계약을 포함한 나머지 조항은 ADR-0014에 그대로 남는다.

## Context

플랫폼은 Windows 위 WSL2가 아니라 Linux server 한 대에서 운영된다. 이 host는
Ubuntu 24.04 LTS이고 Docker Engine을 native daemon으로 실행하며, Docker
context는 `default`다. k3d cluster `k3d-hyhome`과 외부 서비스
workspace(`hy-home.docker`)의 container는 같은 host의 Docker network
`k3d-hyhome`을 공유한다.

그런데 ADR-0014, Architecture Description, Stage 05 문서, infrastructure
README, 정적 검증기는 여전히 WSL2 shell, WSL-native Docker, Windows
portproxy를 전제로 적고 있다. 이 전제는 operator가 확인해야 할 runtime
prerequisite를 잘못 안내하고, 존재하지 않는 Windows 경계를 failure boundary로
만든다.

## Decision

- 플랫폼 host는 Linux server 한 대다. Docker는 host의 native Docker Engine이며
  Docker context는 host에서 확인한다.
- local UI와 외부 서비스 host 이름은 `hy.home.arpa` domain을 쓴다. 이 이름을
  해석하는 DNS, host firewall, 외부 Traefik gateway는 operator가 소유하며
  저장소 정적 검증의 범위 밖이다.
- k3d cluster 모양, `k3d-hyhome` network와 context, ingress-nginx
  LoadBalancer `172.18.0.240`, 외부 서비스 EndpointSlice 계약은 바뀌지 않는다.
- 이전 결정이 "WSL2 자원 예산"이라 적은 제약은 single-host 자원 예산으로
  읽는다. 제약의 크기나 resource request/limit 값은 이 결정으로 바뀌지 않는다.
- infrastructure runtime prerequisite 표와 그 정적 검증은 WSL2가 아닌 Linux
  server host를 기준으로 한다.

## Explicit Non-goals

- 여러 host나 원격 cluster로의 확장
- `hy.home.arpa` DNS 서버, host firewall, TLS 인증서 발급 절차의 소유
- k3d cluster 설정, node 수, resource request/limit 변경
- 결정 당시 WSL2를 전제로 쓴 archive 기록과 accepted ADR 본문의 수정

## Consequences

- **Positive**:
  - runtime prerequisite와 failure boundary가 실제 host와 일치한다.
  - Windows portproxy와 WSL gateway 같은 존재하지 않는 경계가 운영 문서에서
    사라진다.
- **Trade-offs**:
  - 결정 당시 WSL2를 전제로 쓴 accepted ADR 본문은 그대로 남으므로, 독자는 이
    결정을 함께 읽어야 한다.
- **Operational**:
  - host DNS에서 `*.hy.home.arpa` 해석은 operator가 유지하며, 저장소 정적
    PASS는 이를 증명하지 않는다.

## Alternatives

### ADR-0014 전체를 대체

- Good:
  - 현재 플랫폼 계약이 문서 하나에 모인다.
- Bad:
  - host 조항 하나를 바꾸려고 바뀌지 않은 조항 전체를 새 결정으로 다시 적어야
    하고, ADR-0014를 인용하는 문서를 모두 옮겨야 한다.

### ADR-0014 본문을 직접 수정

- Good:
  - 가장 작은 diff다.
- Bad:
  - accepted 결정의 본문을 바꾸면 결정 당시의 기록이 사라진다.

## Traceability

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
- **Infrastructure**: [`../../../infrastructure/README.md`](../../../infrastructure/README.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0014](./0014-current-local-gitops-platform-contract.md) | Carries ADR-0014's host clause only; ADR-0014 stays accepted for every other clause | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
