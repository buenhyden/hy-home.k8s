---
title: "Dedicated Kubernetes Router and Host Baseline Implementation Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0008-PLAN-0001"
---

# Dedicated Kubernetes Router and Host Baseline Implementation Plan

## Global Constraints

- 평문 시크릿은 Git, 문서, 로그, 검증 증거에 두지 않는다.
- 정상 변경은 Git과 ArgoCD reconciliation으로 수행한다. live cluster, host
  네트워크, 외부 workspace 변경은 operator 승인 대상이며 이 plan이 수행하지
  않는다.
- remote branch protection은 바꾸지 않고, push와 merge는 요청 owner가 따로
  승인한다.
- 안전 경계 marker와 sealed archive 본문은 수정하지 않는다.

## Overview

이 plan은 [SPEC-0008](spec.md)의 현재 플랫폼 계약에 다섯 가지 결정을 반영한다.

- [ADR-0041](../../02.architecture/decisions/0041-openbao-secret-backend.md):
  OpenBao backend
- [ADR-0042](../../02.architecture/decisions/0042-linux-server-single-host-baseline.md):
  Linux server host
- [ADR-0043](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md):
  k8s 전용 router와 `hy-k8s.home.arpa`
- [ADR-0044](../../02.architecture/decisions/0044-stateful-data-stores-stay-external.md):
  외부 data store 유지
- [ADR-0045](../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md):
  cluster 안 telemetry 수집과 외부 관측 backend

완료 상태는 desired state, bootstrap, 정적 검증기, 운영 문서가 다섯 결정과
일치하고 staged와 full QA가 통과한 상태다.

## Context

2026-09-23 조사 결과는 다음과 같다.

- host는 Ubuntu 24.04 LTS Linux server이고 `enp4s0`에 `192.168.0.13/24`를
  쓴다. `192.168.0.14`는 ARP 응답이 없다. 이름은 `/etc/hosts`로 해석한다.
- 외부 workspace의 Traefik은 `0.0.0.0:80/443`을 점유하고 k3d network에서
  `172.18.0.2`를 쓴다. k8s route는 그 Traefik의 dynamic config에 있다.
- k3d 설정은 serverlb에 `80:80`, `443:443`을 매핑해 host port가 충돌한다.
  ingress-nginx는 MetalLB `172.18.0.240` LoadBalancer이고 NodePort는 고정되어
  있지 않다.
- host에서 k3d cluster는 실행 중이 아니며, 별개의 native k3s가 systemd로 실행
  중이다. 요청 owner는 k3d 계약을 유지하기로 했다.
- `pg-router`(`postgresql-cluster`)는 opt-in profile `postgres-ha`로만 기동하며
  중지되어 있다. `mng-valkey`는 기동 중이다.
- 외부 관측 stack은 기동 중이며 Prometheus는 remote write를 받는다. k8s 메트릭은
  `172.18.0.2:30082-30092` static target으로 scrape되는데, 그 주소는 외부
  Traefik이 쓴다. sidecar, kubelet, cAdvisor 메트릭은 수집되지 않는다.

### 진행 중 문서와의 충돌 분석

| 문서 | 상태 | 충돌 | 처리 |
| --- | --- | --- | --- |
| SPEC-0008 | active | 외부 backend를 Vault로 적고, k8s 진입점과 domain 계약이 없다 | WP-001에서 계약과 VAL-SPC-005를 보완한다 |
| SPEC-0049 | draft, Task 7개 queued | `traefik/` dynamic config용 Traefik 검증기(VAL-PVSE-004)를 계획하고, conftest를 optional로 둔다 | WP-001에서 Traefik lane 폐지와 conftest 필수 계약을 처분 메모로 기록한다 |
| SPEC-0047 | active, Task 5개 queued | `traefik` 표면을 인벤토리 대상으로 둔다 | WP-001에서 `traefik` 표면 폐지를 처분 메모로 기록한다 |

## Goals & In-Scope

- SPEC-0008 계약 보완, SPEC-0049와 SPEC-0047 처분 기록
- k3d serverlb의 전용 IP bind, ingress-nginx 고정 NodePort, k8s host 이름을
  `<name>.hy-k8s.home.arpa`로 전환(ArgoCD는 `argo`), apex path redirect,
  OpenBao endpoint 전환, bootstrap TLS SAN 검사 전환
- `traefik/` reference 파일과 sample Traefik 예시 폐지, 관련 검증기와 테스트
  정리
- Linux server host 기준의 infrastructure 전제 표, 검증기, 문서 정렬
- Stage 05 policy와 runbook의 router, 온보딩, 복구 절차 갱신과 `pg-router`
  기동 전제 명시
- cluster 안 Alloy의 메트릭 수집과 remote write, 그 뒤 metrics NodePort 폐지

## Non-Goals & Out-of-Scope

- host 주소 할당(netplan), DNS 또는 `/etc/hosts` 변경, k3d cluster 생성
- 외부 workspace(`hy-home.docker`)의 Traefik bind, dynamic config, data
  cluster, Prometheus static job 변경. 필요한 변경은 Task handoff에 기록한다
- native k3s의 처분

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | SPEC-0008 계약 보완, SPEC-0049와 SPEC-0047 처분 기록, 이 plan과 Task 활성화 | ADR-0041..0044 accepted | 결정 commit | Markdown, link, lifecycle gate PASS |
| WP-002 | router, host 이름, apex redirect, OpenBao endpoint 구현과 Traefik reference 폐지 | WP-001 | conftest 설치 | staged QA 전체 PASS |
| WP-003 | Linux server host 정렬 | WP-002 | WP-002 commit | staged QA 전체 PASS |
| WP-004 | Stage 05 router, 온보딩, 복구 절차와 data store 전제 | WP-002 | WP-002 commit | staged QA PASS |
| WP-005 | Alloy 메트릭 수집(pod와 sidecar, kube-state-metrics, kubelet/cAdvisor, istiod, ArgoCD, Rollouts)과 `prometheus-external` remote write, egress 허용 | ADR-0045 accepted | WP-002 commit | staged QA PASS |
| WP-006 | metrics NodePort와 관련 문서 폐지. 외부 static scrape job이 먼저 사라져 live remote write 증거를 기다리지 않는다 | WP-005, WP-008 | 외부 workspace PR #218 merge | staged QA PASS |
| WP-007 | 전체 검증과 handoff | WP-002..006, WP-008, WP-009 | 모든 commit | `python3 scripts/qa.py full` PASS |
| WP-008 | 외부 서비스 경로를 host 주소 `192.168.0.13`과 host 공개 port로 이전, ESO의 OpenBao HTTPS 전환, k3d API bind와 SAN, PostgreSQL bootstrap 선택화 | ADR-0046 accepted | ADR-0046 commit | staged QA PASS; bootstrap 외부 의존성 단계 PASS |
| WP-009 | Prometheus API와 Grafana를 외부 Traefik 이름으로 호출(Alloy, Kiali, Rollouts), Basic Auth와 gateway CA 배포, `prometheus-external`·`grafana-external` 폐지 | WP-008, 외부 workspace PR #222 | ADR-0046 clarification | staged QA PASS; `alloy validate` PASS |

## Verification Plan

- 각 commit은 `python3 scripts/qa.py staged`로 검증한다.
- WP-002는 `bash scripts/validate-infrastructure-contracts.sh`와
  `python3 scripts/validation/repository/quality.py --root .`가 새 router
  계약(serverlb bind 주소, NodePort, host 이름, apex redirect)을 강제함을
  보인다.
- 마지막에 `python3 scripts/qa.py full`과 `git diff --check`를 실행한다.
- live 검증은 2026-09-23..24 재구축한 cluster에서 수행했다. 결과와 남은 DEFER는
  [Task](tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md)에 있다.

## Risks & Mitigations

- **k3d 재생성 필요**: serverlb bind 주소는 cluster 생성 시 고정된다. 기존
  cluster가 있으면 operator가 runbook 절차로 재생성한다.
- **외부 workspace 미반영**: 외부 Traefik이 `0.0.0.0:443`을 계속 점유하면
  serverlb가 `192.168.0.14:443`을 bind하지 못한다. Task handoff에 필요한
  변경을 명시한다.
- **주소 충돌**: `192.168.0.14`가 나중에 다른 기기에 할당될 수 있다. operator가
  공유기 예약으로 막는다.
- **Rollback**: 각 WP는 독립 commit이며 `git revert`로 되돌린다.

## Completion Criteria

- WP-001..WP-006 commit이 staged QA를 통과하고 WP-007의 full QA가 통과한다.
- live 증거와 외부 workspace 변경은 Task에 DEFER와 next owner로 남긴다.

## Traceability

- **Spec**: [SPEC-0008](spec.md)
- **Decisions**: ADR-0037, ADR-0041, ADR-0042, ADR-0043, ADR-0044, ADR-0045, ADR-0046

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SPC-005](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0008-TSK-0001](tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md) |
| [VAL-SPC-002](spec.md#success-criteria--verification-plan) | WP-002, WP-003 | [SPEC-0008-TSK-0001](tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md) |
| [VAL-SPC-001](spec.md#success-criteria--verification-plan) | WP-001, WP-004, WP-005, WP-006, WP-007, WP-008, WP-009 | [SPEC-0008-TSK-0001](tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md) |
