---
title: "Dedicated Kubernetes Router and Host Baseline"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-23"
layer: "specs"
artifact_id: "SPEC-0008-TSK-0001"
---

# Task: Dedicated Kubernetes Router and Host Baseline

## Overview

이 Task는 [Implementation Plan](../plan.md)의 WP-001..WP-005를 수행한다. 완료
증거는 WP별 commit의 staged QA와 마지막 full QA다.

## Inputs

- [SPEC-0008](../spec.md)과 [Implementation Plan](../plan.md)
- [ADR-0041](../../../02.architecture/decisions/0041-openbao-secret-backend.md),
  [ADR-0042](../../../02.architecture/decisions/0042-linux-server-single-host-baseline.md),
  [ADR-0043](../../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md),
  [ADR-0044](../../../02.architecture/decisions/0044-stateful-data-stores-stay-external.md)
- 2026-09-23 요청 owner 결정:
  - k3d를 유지한다
  - k8s router는 전용 host IP의 443을 쓴다
  - k8s host만 `hy-k8s.home.arpa`로 전환한다
  - subdomain을 기준 주소로 하고 apex path는 redirect한다
  - ArgoCD 이름은 `argo`다

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-SPC-001 | SPEC-0008 계약 보완, SPEC-0049와 SPEC-0047 처분 기록 | platform | Queued | Not executed | Markdown and link gates |
| WORK-002 | VAL-SPC-005 | serverlb 전용 IP bind, NodePort 고정, host 이름, apex redirect, OpenBao endpoint, Traefik reference 폐지 | platform | Queued | Not executed | staged QA |
| WORK-003 | VAL-SPC-002 | Linux server host 정렬 | platform | Queued | Not executed | staged QA |
| WORK-004 | VAL-SPC-001 | Stage 05 router, 온보딩, 복구 절차와 data store 전제 | platform | Queued | Not executed | staged QA |
| WORK-005 | VAL-SPC-001 | full QA와 handoff | platform | Queued | Not executed | full QA |

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

아직 실행하지 않았다.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Not executed | None yet |
