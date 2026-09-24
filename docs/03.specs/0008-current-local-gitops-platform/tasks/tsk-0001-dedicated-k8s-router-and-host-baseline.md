---
title: "Dedicated Kubernetes Router and Host Baseline"
version: "0.3.2"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-24"
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
| WORK-006 | VAL-SPC-001 | metrics NodePort 폐지 | platform | Done | NodePort Services `30082-30092` removed with a static check against new ones; RUN-0009 owns in-cluster collection; RUN-0008 is reduced to ArgoCD component checks on that path. Live remote write still needs a host-published Prometheus `9090` (external owner) | `dfbf63f9`; staged QA PASS except `policy-gates` (conftest absent) |
| WORK-007 | VAL-SPC-001 | full QA와 handoff | platform | Done | Cluster rebuilt and verified live; seven defects found and fixed on the way (see Verification Summary). Final full QA fails only on known pre-existing or host-only lanes | PR #74..#82; full QA on `088fd4ac` |
| WORK-008 | VAL-SPC-001 | 외부 서비스 host 주소 경로, ESO OpenBao HTTPS, k3d API bind, PostgreSQL bootstrap 선택화 | platform | Done | EndpointSlices and egress on `192.168.0.13`, ESO over `https://openbao.hy.home.arpa` with `openbao-ca`, CoreDNS custom zone, k3d API `192.168.0.13:6550`, optional PostgreSQL; live bootstrap pending cluster recreation | `b7521749`, `4a6e5548`, `888c22be`; staged QA PASS except `policy-gates` (conftest absent) |
| WORK-009 | VAL-SPC-001 | Prometheus API와 Grafana HTTPS 경로, Basic Auth, gateway CA, Kiali Grafana Viewer token | platform | Done | Alloy, Kiali and Rollouts call `https://prometheus.hy.home.arpa` with Basic Auth from OpenBao `platform/prometheus-api`, and Kiali calls `https://grafana.hy.home.arpa`. CoreDNS resolves both, and bootstrap distributes the CA. `prometheus-external` and `grafana-external` are retired. Live check waits on the OpenBao P0 provisioning (external owner) | `8125c87f`; staged QA PASS except `policy-gates` (conftest absent); `alloy validate` PASS |

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
- **Live Validation**: 2026-09-23..24 재구축한 cluster에서 수행했다. 결과는
  Verification Summary에 있다
- **Secret / Vault Handling**: 시크릿 값을 읽거나 출력하지 않는다.
  OpenBao 운영은 외부 workspace 소유다
- **Rollback Plan**: WP별 commit을 `git revert`로 되돌린다
- **Evidence Location**: 이 Task

## Verification Summary

WORK-001..006, 008, 009의 staged QA 기록은 Task Table에 있다. 당시 `policy-gates`는
conftest가 없어 FAIL이었으나 `156ffecc` 이후 container 경로로 PASS한다.

### Live verification (WORK-007, 2026-09-23..24)

owner가 `/etc/hosts`, bootstrap, OpenBao Kubernetes auth 재등록(RUN-0096 5.1..5.5)을
수행했다. live mutation은 owner가 승인한 범위(멈춘 hook Job pod 삭제, 실패 app
resync, 누수된 flannel IP 정리)만 수행했다.

| Check | Result | Evidence |
| --- | --- | --- |
| cluster | PASS | node 4개 Ready, API SAN에 `192.168.0.13` |
| ESO | PASS | `vault-backend` Ready. `argocd-external-valkey`, `monitoring/prometheus-api-auth`, `kiali-prometheus-auth`, `kiali-grafana-auth`, `apps/prometheus-api-auth` SecretSynced. `argocd-notifications-secret`, `postgres-app-secret`은 OpenBao에 KV가 없어 SecretSyncedError(owner가 알려진 상태로 기록 결정) |
| ArgoCD | PASS except known | 20개 Synced/Healthy. `platform-argocd-config`, `platform-eso-config`는 위 두 Secret 때문에 Degraded |
| router (ADR-0043) | PASS | `CHECK_K8S_ROUTER=true verify-ingress-tls.sh`; `argo.hy-k8s.home.arpa` 200; apex 5개 path가 각 host로 301 |
| external services, policies | PASS | `verify-external-services.sh`, `verify-network-policies.sh` |
| CoreDNS | PASS | owner 승인 임시 pod에서 `openbao`, `prometheus`, `grafana.hy.home.arpa`가 `192.168.0.13`으로 풀렸다. pod는 삭제했다 |
| Alloy, Prometheus | PASS | Alloy 1/1, 오류 없음. `up{cluster="k3d-hyhome"}` job `kubernetes-pods`=19, `kubelet`=4, `cadvisor`=4; `argocd_app_info`=22; `istio_requests_total` 수집 |
| Loki | PASS | `{cluster="k3d-hyhome"}` range query에서 namespace 12개 stream |
| Kiali | PASS | Prometheus 3.14.0, Grafana 13.2.2(bearer, `/api/grafana` 200), Tempo v3.0.3 |
| Rollouts | PASS | owner 승인 canary(pod template annotation)에서 AnalysisRun `adminer-5b74d8ff8-2-1.2` Successful, Rollout 6 step 완료. 앞선 두 시도는 아래 #81, #82 결함으로 Error였다 |
| `run-all.sh` | PASS | `CHECK_K8S_ROUTER=true` 전체 PASS |

live 검증에서 찾아 고친 결함:

| PR | Defect |
| --- | --- |
| #74 | ESO token에 API server audience가 없어 OpenBao TokenReview가 401 |
| #75 | AnalysisTemplate metric에 `count`가 없어 Rollout 거부; istio-cni bin dir |
| #76 | istio-cni chart의 platform profile이 `cniBinDir`를 덮어씀(`platform: k3s`) |
| #77 | ingress-nginx admission hook Job에 sidecar가 주입되어 끝나지 않음 |
| #78 | Alloy와 Kiali ExternalSecret sync wave가 소비자보다 늦어 deadlock |
| #79 | Kiali가 `ca_file` 없이는 CA bundle을 쓰지 않음; `platform-monitoring` server-side diff; RUN-0009 Loki instant query |
| #81 | analysis 조건이 숫자 결과를 문자열과 비교 |
| #82 | kube-state-metrics scrape에 `honor_labels`가 없어 `namespace`가 `monitoring`으로 덮임 |

Handoff 뒤 follow-up(2026-09-24):

| PR | Change |
| --- | --- |
| #84 | Alloy pod template `checksum/config`로 config 변경 시 rollout; 소비자 없는 `postgres-app-secret` 제거; archive test 4개 수정 |
| #85 | Stage 05 operation 문서가 `superseded`로 archive될 수 있게 profile 조정 |
| #86 | Istio mesh trace를 OTLP로 외부 Alloy(`alloy-external:4317`)에 전송, sampling 10% |
| #87 | #85가 깨뜨린 frozen archive fixture test 복구(#85, #86이 `qa` FAIL 상태로 merge됨) |

### Final full QA

`python3 scripts/qa.py full` on `main` `088fd4ac`: exit 1. 20 lanes PASS,
`policy-gates` 포함. FAIL 3개는 모두 기존 또는 host 전용이다.

- `unit-tests`: 1141개 중 8개 FAIL. 알려진 archive test 4개, host 전용 secret
  scan test 2개, flaky `test_file_reader_rejects_changes_during_read`, 그리고
  `test_escaped_descendant_is_failed_without_post_reap_group_signal`. 마지막
  것은 이 host에서 과거 `main`에서도 실패하고 CI에서는 통과한다(host 환경).
- `archive-cutover`: 과거 `main`(`a9c94d7f`)에서도 같은 FAIL이다.
- `pre-commit`: runner의 trusted PATH에 `~/.local/bin`이 없어 도구 미발견.
  같은 명령을 직접 실행하면 20 hook PASS, gitleaks만 FAIL이며 finding은 모두
  git이 무시하는 host 파일(`secrets/certs/*.pem`, `.env`, `.superpowers/`)이다.

### Handoff

- **Snapshot**: `main` `088fd4ac`; 이 Task 갱신은 그 뒤 문서 전용 commit이다.
- **Approval boundary**: agent는 push, merge, OpenBao 운영, 시크릿 조회를 하지
  않았다. live mutation은 위에 적은 owner 승인 범위만 수행했다.
- **Skipped or unavailable**: host에 `argocd` CLI와 `shellcheck`가 없다
  (pre-commit이 shellcheck를 대신한다).
- **Rollback**: PR별 merge commit을 `git revert`한다. live 상태는 ArgoCD가
  `main`으로 되돌린다.
- **Residual risk** (follow-up 반영, `main` `83de9cbc`):
  - `platform/notifications` KV 부재로 `platform-argocd-config` Degraded.
    owner가 root session으로 Slack token을 넣어야 한다(RUN-0096).
  - OpenBao snapshot 없음. 새 snapshot과 offline 보관이 필요하다(RUN-0096 v1.2.1).
  - Grafana Viewer token 만료 2026-12-22(RUN-0096 재발급 절차, 2026-12-15 알림).
  - trace 경로는 Git에만 있다. docker `infra-alloy` 재생성(docker PR #248) 뒤
    `apps`, `ingress-nginx` pod 재시작과 Tempo/Kiali 확인이 필요하다.
  - adminer Rollout pod template에 검증용 live annotation
    `verification/canary-at`이 남아 있다(Git에 없는 필드라 ArgoCD drift 아님)
- **Next owner**: operator. KV와 snapshot, 그리고 docker Alloy 재생성은
  hy-home.docker session에 넘겼고 모두 owner 승인 대기다.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | `11f81d11` |
| [WORK-002](../plan.md#work-breakdown) | Done | `cdf9a465` |
| [WORK-005](../plan.md#work-breakdown) | Done | `030cf5df` |
| [WORK-006](../plan.md#work-breakdown) | Done | `dfbf63f9` |
| [WORK-007](../plan.md#work-breakdown) | Done | PR #74..#82; full QA on `088fd4ac`; follow-up #84..#87 |
| [WORK-008](../plan.md#work-breakdown) | Done | `4a6e5548` |
