---
title: "Dedicated Kubernetes Router and Host Baseline"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-23"
layer: "specs"
artifact_id: "SPEC-0008-TSK-0001"
---

# Task: Dedicated Kubernetes Router and Host Baseline

## Overview

이 Task는 [Implementation Plan](../plan.md)의 WP-001..WP-007을 수행한다. 완료
증거는 WP별 commit의 staged QA와 마지막 full QA다.

## Inputs

- [SPEC-0008](../spec.md)과 [Implementation Plan](../plan.md)
- [ADR-0041](../../../02.architecture/decisions/0041-openbao-secret-backend.md),
  [ADR-0042](../../../02.architecture/decisions/0042-linux-server-single-host-baseline.md),
  [ADR-0043](../../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md),
  [ADR-0044](../../../02.architecture/decisions/0044-stateful-data-stores-stay-external.md),
  [ADR-0045](../../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md)
- 2026-09-23 요청 owner 결정:
  - k3d를 유지한다
  - k8s router는 전용 host IP의 443을 쓴다
  - k8s host만 `hy-k8s.home.arpa`로 전환한다
  - subdomain을 기준 주소로 하고 apex path는 redirect한다
  - ArgoCD 이름은 `argo`다

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-SPC-001 | SPEC-0008 계약 보완, SPEC-0049와 SPEC-0047 처분 기록 | platform | Done | SPEC-0008 router, OpenBao, data store contract and VAL-SPC-005; SPEC-0049 and SPEC-0047 disposition notes | `11f81d11`; staged QA PASS |
| WORK-002 | VAL-SPC-005 | serverlb 전용 IP bind, NodePort 고정, host 이름, apex redirect, OpenBao endpoint, Traefik reference 폐지 | platform | Done | serverlb bound to `192.168.0.14:80/443`, NodePorts `30080/30443`, `<name>.hy-k8s.home.arpa` hosts, five apex redirects, OpenBao endpoint, `traefik/` retired | `cdf9a465`; staged QA PASS except `policy-gates` (conftest absent) |
| WORK-003 | VAL-SPC-002 | Linux server host 정렬 | platform | Done | Host prerequisite matrix, validators and documents aligned to the Linux server host | `cdf9a465` |
| WORK-004 | VAL-SPC-001 | Stage 05 router, 온보딩, 복구 절차와 data store 전제 | platform | Done | Stage 05 router, onboarding and recovery procedures; `pg-router` and router prerequisites | `cdf9a465` |
| WORK-005 | VAL-SPC-001 | Alloy 메트릭 수집과 remote write | platform | Done | Alloy scrapes annotated pods, platform components, kubelet and cAdvisor and remote-writes to `prometheus-external` | `e7693ff7`, `030cf5df`; `alloy validate` PASS; staged QA PASS except `policy-gates` |
| WORK-006 | VAL-SPC-001 | live 확인 뒤 metrics NodePort 폐지 | platform | Blocked | Waits for live remote write evidence; needs WORK-008 and a host-published Prometheus `9090` | DEFER; next owner operator |
| WORK-007 | VAL-SPC-001 | full QA와 handoff | platform | Queued | Not executed | full QA |
| WORK-008 | VAL-SPC-001 | 외부 서비스 host 주소 경로, ESO OpenBao HTTPS, k3d API bind, PostgreSQL bootstrap 선택화 | platform | In progress | ADR-0046 accepted | ADR-0046 commit |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/`, `gitops/`, `infrastructure/`, `examples/`,
  `scripts/`, `tests/`, `traefik/`, `README.md`, `RTK.md`, `.agents/`,
  `.github/ISSUE_TEMPLATE/`, `.env.example`
- **Forbidden Paths**: `docs/98.archive/` sealed bodies, `secrets/` values,
  외부 workspace
- **Approval Required**: host 주소 할당, DNS와 `/etc/hosts`, k3d cluster 생성과
  재생성, 외부 Traefik과 data cluster 변경, push와 merge
- **Static Validation**: WP별 `python3 scripts/qa.py staged`, 마지막
  `python3 scripts/qa.py full`
- **Live Validation**: DEFER. k3d cluster와 `192.168.0.14` host 주소가 없다.
  owner는 operator다
- **Secret / Vault Handling**: 시크릿 값을 읽거나 출력하지 않는다.
  OpenBao 운영은 외부 workspace 소유다
- **Rollback Plan**: WP별 commit을 `git revert`로 되돌린다
- **Evidence Location**: 이 Task

## Verification Summary

- **Static lanes**: 모든 구현 commit의 staged QA에서 `policy-gates`를 제외한
  모든 lane이 PASS했다.
- **Unavailable tool**: 이 host에는 `conftest`가 없다. `policy-gates`는 실행되지 못해
  FAIL로 기록되었다. 요청 owner가 conftest 설치를 `hy-home.docker` 작업으로
  미루고 설치 없이 진행하도록 승인했다. push 전에 이 lane을 실행해야 한다.
- **Alloy**: `grafana/alloy:v1.18.1 validate`가 새 설정을 통과시키고, 알려진 잘못된
  설정은 거부했다.
- **Live**: DEFER. k3d cluster, `192.168.0.14` host 주소, 이름 해석이 없다. 다음
  owner는 operator다.
- **External**: `hy-home.docker`의 작업은 다음과 같다.
  - Traefik bind를 `192.168.0.13`으로 한정한다.
  - k8s dynamic config 6개를 삭제한다.
  - k3d static scrape job은 WORK-006 시점에 폐지한다.
  - `.env.example`의 k8s API 주소 `172.18.0.2:6443`이 외부 Traefik 주소와
    겹치는 문제를 확인한다.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | `11f81d11` |
| [WORK-002](../plan.md#work-breakdown) | Done | `cdf9a465` |
| [WORK-005](../plan.md#work-breakdown) | Done | `030cf5df` |
| [WORK-006](../plan.md#work-breakdown) | Blocked | Live remote write evidence pending |
