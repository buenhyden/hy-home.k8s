---
title: "Argo Rollouts, Notifications & Headlamp Operations Policy"
version: "2.0.1"
type: "operation/policy"
status: "active"
owner: "platform"
updated: "2026-11-20"
artifact_id: "POL-0004"
---

# Argo Rollouts, Notifications & Headlamp Operations Policy

## 문서 개요

### 목적과 독자

이 정책은 Argo Rollouts, Notifications & Headlamp Operations Policy의 운영 조건을 적용할 플랫폼 운영자와 변경 검토자를 위한 규칙이다. 정책 목표는 [Objective](#objective)에 기록한다.

### 책임과 적용 범위

platform은 이 운영 정책을 유지한다. 적용 대상은 [Applies To](#applies-to), 규칙과 집행 조건은 [Rules](#rules) 및 [Enforcement](#enforcement)가 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Purpose and Scope

##### Objective

이 문서는 Argo Rollouts(점진적 배포), Argo Notifications(Slack 알림), Headlamp(클러스터 UI) 운영 통제 기준을 정의한다.

##### Applies To

- Argo Rollouts — `argo-rollouts` namespace
- Argo Notifications (ArgoCD 내장 컨트롤러) — `argocd` namespace
- Rollouts 알림 (Argo Rollouts 컨트롤러 자체 notification engine) — `argo-rollouts` namespace
- Headlamp — `headlamp` namespace

chart 버전은 각 Application manifest의 `targetRevision`이 소유하며 이 정책은
버전을 복제하지 않는다.

- **Systems**: `gitops/apps/root/platform-rollouts-app.yaml`, `gitops/apps/root/platform-headlamp-app.yaml`, `gitops/platform/argocd/argocd-notifications-*`, `gitops/platform/eso/rollouts-notification-secret.yaml`
- **Agents**: 운영 자동화 에이전트
- **Environments**: Linux server local cluster

###### Exclusions

범위에서 제외한다고 따로 표시한 항목은 없으며, chart 버전은 위 Applies To의 문단대로 각 Application manifest가 소유한다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| ROLLOUT-R001 | Always | **Required**: Rollouts Controller namespace: `argo-rollouts` 고정 | RUN-0004 | none |
| ROLLOUT-R002 | Always | **Required**: Rollouts Dashboard 항상 활성화 (`dashboard.enabled: true`) | RUN-0004 | none |
| ROLLOUT-R003 | Always | **Required**: canary 단계는 AnalysisTemplate으로 gate한다. 단계 사이 pause는 앱별로 timed pause(`pause: {duration: ...}`) 또는 수동 pause(`pause: {}`)를 선택하며, 플랫폼이 자동 promotion을 강제하지 않는다 (ADR-0011) | Semantic review | none |
| ROLLOUT-R004 | skipAnalysis: true를 쓸 때 | **Required**: Analysis 결과 무시(`skipAnalysis: true`)는 플랫폼 오너 승인 필요 | Semantic review | none |
| ROLLOUT-R005 | Always | **Required**: CRD 설치: `installCRDs: true` 유지 | RUN-0004 | none |
| ROLLOUT-R006 | Always | **Required**: Rollouts Dashboard는 `rollouts.hy-k8s.home.arpa` + Traefik(`nginx` IngressClass) + TLS(`rollouts-dashboard-tls`) 유지 | RUN-0004 | none |
| ROLLOUT-R007 | Always | **Required**: 완료·중단 알림은 Rollouts 컨트롤러의 notification engine이 보낸다([ADR-0054](../../02.architecture/02.decisions/0054-platform-decision-current-state-amendment.md) 조항 2). `platform-rollouts-app.yaml` chart values가 `service.slack`, `trigger.on-rollout-completed`/`on-rollout-aborted`, 대응 template과 `slack:hy-home-alerts` 구독을 소유하며, 이 알림에 ArgoCD Notifications 컨트롤러를 쓰지 않는다 | RUN-0004 | none |
| ROLLOUT-R008 | 승인/증적 절차를 따를 때 | **Allowed**: 수동 Rollout promotion은 [Rollouts/Notifications/Headlamp 런북](../03.runbooks/0004-rollouts-notifications-headlamp-runbook.md)의 승인/증적 절차로 실행 | RUN-0004 | none |
| ROLLOUT-R009 | Always | **Allowed**: canary/blue-green 전략 선택 | Semantic review | none |
| ROLLOUT-R010 | Always | **Allowed**: Prometheus AnalysisTemplate 정의 (`https://prometheus.hy.home.arpa`, `apps/prometheus-api-auth`의 Basic Auth header, controller의 `hy-home-root-ca` 신뢰; ADR-0046) | Semantic review | none |
| ROLLOUT-R011 | Always | **Disallowed**: `argo-rollouts` namespace에 Rollouts 외 워크로드 배치 | Semantic review | none |
| ROLLOUT-R012 | Always | **Disallowed**: `skipAnalysis: true` 임의 사용 | Semantic review | none |
| ROLLOUT-R013 | Always | **Required**: Slack app token(`service.slack`의 `$slack-token`): OpenBao `platform/notifications` 속성 `slack_token` → ESO → `argocd/argocd-notifications-secret`. Rollouts 컨트롤러는 같은 OpenBao 항목을 `gitops/platform/eso/rollouts-notification-secret.yaml`의 ExternalSecret으로 받아 `argo-rollouts/argo-rollouts-notification-secret`에 둔다 | RUN-0004 | none |
| ROLLOUT-R014 | Always | **Required**: templates/triggers: `argocd-notifications-cm` (GitOps 관리) | RUN-0004 | none |
| ROLLOUT-R015 | Always | **Required**: `defaultTriggers`: `on-health-degraded`, `on-sync-failed`; `subscriptions`는 `on-health-degraded`, `on-sync-failed`, `on-deployed`를 `slack:hy-home-alerts`로 보내며 `argocd-notifications-cm`이 소유한다 | RUN-0004 | none |
| ROLLOUT-R016 | Always | **Required**: 앱별 opt-in: annotation `notifications.argoproj.io/subscribe.<trigger>.slack: <channel>` | Semantic review | none |
| ROLLOUT-R017 | Always | **Allowed**: 앱 annotation으로 개별 채널 지정 | Semantic review | none |
| ROLLOUT-R018 | GitOps PR을 통할 때 | **Allowed**: template 추가 (GitOps PR 통해) | Semantic review | none |
| ROLLOUT-R019 | Always | **Disallowed**: `argocd-notifications-secret`과 `argo-rollouts-notification-secret`에 Slack token 평문 커밋 | `secret-handling` | none |
| ROLLOUT-R020 | Always | **Disallowed**: ArgoCD chart의 notifications controller 비활성화(`notifications.enabled: false`) 임의 적용 (Rollouts chart의 별도 값과 무관) | RUN-0004 | none |
| ROLLOUT-R021 | Always | **Required**: Headlamp namespace: `headlamp` 고정 | RUN-0004 | none |
| ROLLOUT-R022 | Always | **Required**: Ingress hostname: `headlamp.hy-k8s.home.arpa` | RUN-0004 | none |
| ROLLOUT-R023 | Always | **Required**: TLS Secret: `headlamp-tls` (cert-manager `mkcert-ca-issuer` 자동 발급) # pragma: allowlist secret | RUN-0004 | none |
| ROLLOUT-R024 | Always | **Required**: k8s router 경로는 [POL-0001](./0001-k8s-gitops-operations-policy.md)의 ingress 통제를 따른다 | RUN-0004 | none |
| ROLLOUT-R025 | Always | **Allowed**: ServiceAccount Token 방식 인증 (로컬 플랫폼 기본) | Semantic review | none |
| ROLLOUT-R026 | 검토 후 | **Allowed**: Headlamp 플러그인 설치 (검토 후) | Semantic review | none |
| ROLLOUT-R027 | Always | **Disallowed**: 대체된 클러스터 UI 재설치 (ADR-0014의 Headlamp 계약과 충돌) | Semantic review | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| ROLLOUT-R001 | required | active |
| ROLLOUT-R002 | required | active |
| ROLLOUT-R003 | required | active |
| ROLLOUT-R004 | required | active |
| ROLLOUT-R005 | required | active |
| ROLLOUT-R006 | required | active |
| ROLLOUT-R007 | required | active |
| ROLLOUT-R008 | required | active |
| ROLLOUT-R009 | optional | active |
| ROLLOUT-R010 | optional | active |
| ROLLOUT-R011 | required | active |
| ROLLOUT-R012 | required | active |
| ROLLOUT-R013 | required | active |
| ROLLOUT-R014 | required | active |
| ROLLOUT-R015 | required | active |
| ROLLOUT-R016 | required | active |
| ROLLOUT-R017 | optional | active |
| ROLLOUT-R018 | required | active |
| ROLLOUT-R019 | required | active |
| ROLLOUT-R020 | required | active |
| ROLLOUT-R021 | required | active |
| ROLLOUT-R022 | required | active |
| ROLLOUT-R023 | required | active |
| ROLLOUT-R024 | required | active |
| ROLLOUT-R025 | optional | active |
| ROLLOUT-R026 | required | active |
| ROLLOUT-R027 | required | active |

###### Argo Rollouts

- `ROLLOUT-R001`
- `ROLLOUT-R002`
- `ROLLOUT-R003`
- `ROLLOUT-R004`
- `ROLLOUT-R005`
- `ROLLOUT-R006`
- `ROLLOUT-R007`
- `ROLLOUT-R008`
- `ROLLOUT-R009`
- `ROLLOUT-R010`
- `ROLLOUT-R011`
- `ROLLOUT-R012`

###### Argo Notifications

- `ROLLOUT-R013`
- `ROLLOUT-R014`
- `ROLLOUT-R015`
- `ROLLOUT-R016`
- `ROLLOUT-R017`
- `ROLLOUT-R018`
- `ROLLOUT-R019`
- `ROLLOUT-R020`

###### Headlamp

- `ROLLOUT-R021`
- `ROLLOUT-R022`
- `ROLLOUT-R023`
- `ROLLOUT-R024`
- `ROLLOUT-R025`
- `ROLLOUT-R026`
- `ROLLOUT-R027`

##### Exceptions

- Rollouts analysis skip, notifications disablement, or Headlamp authentication changes require platform owner approval and a linked PR.
- Live cluster changes follow the shared exception in [POL-0001](./0001-k8s-gitops-operations-policy.md#exceptions).

###### Approval and Review

예외 승인은 위 Exceptions의 platform owner 승인과 연결된 PR 요건을 따른다.

#### Enforcement

##### Mechanisms

`Rules` 표의 RUN-0004 표기는 운영 확인 절차다. 정적 집행과 의미 검토는 다음처럼 구분한다.

| Rule IDs | 정적 검사 또는 검토 | 운영 증거와 한계 |
| --- | --- | --- |
| ROLLOUT-R001, R007, R013–R015, R020 | `scripts/validate-infrastructure-contracts.sh`가 namespace, Rollouts/ArgoCD notification 선언, ESO 경로와 ArgoCD controller 활성 선언을 검사한다 | RUN-0004의 controller·Secret·Slack 결과를 별도로 확인한다. 선언 검사는 실제 전달을 증명하지 않는다 |
| ROLLOUT-R002, R006, R022, R023 | `scripts/validate-k8s-manifests.sh`가 호출하는 `scripts/validation/platform/ingress.py`가 Rollouts dashboard/ingress와 Headlamp host/TLS 선언을 검사한다 | RUN-0004의 dashboard·Headlamp 접근 결과를 별도로 확인한다 |
| ROLLOUT-R005, R021, R024 | 변경 검토자가 CRD 설치 값, Headlamp namespace와 POL-0001 ingress 경로를 Git diff에서 의미 검토하고 결과를 PR에 기록한다 | RUN-0004의 CRD·namespace·router 관측을 별도로 기록한다. 자동 검사가 있다고 주장하지 않는다 |

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Argo Rollouts | Controller/dashboard pods are running and Rollout CRDs/list output is available | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../03.runbooks/0004-rollouts-notifications-headlamp-runbook.md) |
| Argo Notifications | ArgoCD and Rollouts controllers are running, both ESO-backed secrets exist, and Slack send/error logs are reviewed without committing token values | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../03.runbooks/0004-rollouts-notifications-headlamp-runbook.md) |
| Headlamp and k8s router | Headlamp pods/ingress/TLS are healthy and `headlamp`/`rollouts` hostnames return expected HTTP status through the k8s router | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../03.runbooks/0004-rollouts-notifications-headlamp-runbook.md) |

- 운영 변경 시 즉시
- 정기 분기 검토
- Rollout 구성과 AnalysisTemplate 참조의 정적 검사는
  [REQ-0004 workload 온보딩 시나리오](../../01.requirements/0004-current-local-gitops-platform.md#quality-scenario-workload-onboarding)의
  source-side 입력이다. Dashboard, Slack 전송, Headlamp 접근 및 실제 promotion
  결과는 명명된 환경의 운영자 증거가 필요하다. 이 정책은 제품 임계값의
  별도 작성 원본이 아니다.

- **Runbook**: [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../03.runbooks/0004-rollouts-notifications-headlamp-runbook.md)

##### Limits

Rollout과 AnalysisTemplate 참조의 정적 검사는 REQ-0004 workload onboarding 시나리오의 source 쪽 입력일 뿐이다. 대시보드 동작, Slack 전달, Headlamp 접근과 실제 promotion 결과는 이름 있는 환경의 운영자 증거가 필요하며, 이 정책은 제품 임계값의 작성 원본이 아니다.

#### Ownership

##### Owner

- **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/02.decisions/0014-current-local-gitops-platform-contract.md)
- **ADR-0011**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/02.decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/02.decisions/0012-argo-notifications-slack.md)
- **ADR-0054**: [`../../02.architecture/decisions/0054-platform-decision-current-state-amendment.md`](../../02.architecture/02.decisions/0054-platform-decision-current-state-amendment.md)

###### Responsibilities

책임 주체는 아래 Lifecycle Traceability 표의 Control owner 열에 적혀 있다.

##### Review Triggers

변경 검토 시점은 위 Enforcement의 운영 변경 시 즉시 및 정기 분기 검토 항목을 따른다.

##### Lifecycle Traceability

- **Rollouts Spec**: SPEC-0004 (left the tree; Git history recovers it)
- **Notifications Spec**: SPEC-0005 (left the tree; Git history recovers it)
- **Rollouts notification delivery**: SPEC-0141 (left the tree; Git history recovers it)

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| N/A — SPEC-0004 left the tree and is recovered from Git history, so no eligible upstream document is available to link as the promoting owner | Platform Owner for promotion approval, analysis exceptions, CRDs, dashboard, and rollback evidence | Argo Rollouts chart values, Rollout resources, AnalysisTemplate review, dashboard ingress/TLS, and runbook evidence |
| N/A — SPEC-0005 left the tree and is recovered from Git history, so no eligible upstream document is available to link as the promoting owner | Platform Owner for subscription policy; secret owner for the Slack credential path | OpenBao-to-ESO secret contract, ArgoCD notifications ConfigMap and annotations, Rollouts controller notification values, controller logs, and plaintext-secret gates |

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
