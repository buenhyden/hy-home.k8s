---
title: 'Argo Notifications Slack Webhook Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-07-13
---

# Argo Notifications Slack Webhook Product Requirements

## Overview

이 문서는 ArgoCD Notifications 컨트롤러를 활성화하고 Slack webhook을 알림 destination으로 사용하여 GitOps 이벤트(sync 실패, health 저하, 배포 완료)와 Rollouts 이벤트(완료, abort)를 운영자에게 자동 전달하기 위한 제품 요구사항을 정의한다.

### Current requirement status

이 PRD는 current-contract backfill 기준의 active 문서다.
ArgoCD Notifications values, ConfigMap, ExternalSecret, 운영 문서는 이미 저장소에 존재하며, 2026-05-18에 ARD/Spec/Plan/Task 추적 체인을 보강했다.
이 문서는 알림의 사용자 가치와 보안 경계를 소유하고, Secret 생성 절차와 manifest 계약은 연결된 downstream 문서와 운영 런북이 소유한다.

## Vision

플랫폼 이벤트(ArgoCD 동기화 실패, 서비스 health 저하, Rollouts 완료/abort)가 운영자에게 Slack으로 자동 전달되어 수동 모니터링 없이 신속한 대응이 가능해진다.

## Problem Statement

현재 GitOps 이벤트(앱 동기화 실패, health 저하)와 Rollouts 이벤트를 운영자에게 자동 전달할 수단이 없다. 운영자는 ArgoCD UI를 수동으로 확인해야 하며, 장애를 인지하는 시간이 늦어진다.

## Personas

- **Platform Engineer**: ArgoCD 이벤트와 Rollouts 이벤트를 Slack 채널에서 실시간으로 수신하고 싶다.
- **DevOps Engineer**: 동기화 실패나 health 저하 시 즉각 알림을 받아 신속하게 대응하고 싶다.
- **Application Team**: 배포 완료(on-deployed) 이벤트를 특정 Slack 채널에서 선택적으로 수신하고 싶다.

## Key Use Cases

- **STORY-01**: ArgoCD 앱이 sync에 실패하면 운영자 Slack 채널로 즉시 알림이 전송된다.
- **STORY-02**: 앱 health가 저하되면(Degraded) 운영자 Slack 채널로 즉시 알림이 전송된다.
- **STORY-03**: Argo Rollouts 배포가 완료되거나 abort되면 Slack 알림이 전송된다.
- **STORY-04**: 애플리케이션 팀이 annotation으로 배포 완료 알림을 특정 채널에 opt-in한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: 플랫폼은 ArgoCD Notifications 기반 GitOps 이벤트 알림을 제공해야 한다. 구체 Helm value는 downstream Spec이 소유한다.
- **REQ-PRD-FUN-02**: Slack credential material은 Vault → ESO → Kubernetes Secret 흐름으로만 소비되어야 하며 PRD, manifest, 로그에 평문으로 노출되지 않아야 한다.
- **REQ-PRD-FUN-03**: 알림 템플릿과 trigger는 배포 완료, health 저하, sync 실패, Rollouts 완료, Rollouts abort 이벤트를 표현해야 한다.
- **REQ-PRD-FUN-04**: Default subscriptions는 `on-health-degraded`, `on-sync-failed`를 전체 앱에 적용해야 한다.
- **REQ-PRD-FUN-05**: 앱별 opt-in은 annotation `notifications.argoproj.io/subscribe.on-deployed.slack: <channel>`로 설정 가능해야 한다.
- **REQ-PRD-FUN-06**: 알림 credential bootstrap은 human-approved 외부 작업으로만 수행되어야 한다.

## Success / Acceptance Criteria

- **REQ-PRD-MET-01**: 운영자가 Notifications controller 상태를 확인할 수 있다. Evidence: `argocd-notifications-controller` Pod `Running`.
- **REQ-PRD-MET-02**: 운영자가 Vault-backed notification credential sync 상태를 확인할 수 있다. Evidence: `argocd-notifications-secret` ExternalSecret `Ready=True`.
- **REQ-PRD-MET-03**: 운영자가 sync 실패를 Slack에서 인지할 수 있다. Evidence: sync 실패 이벤트의 Slack 수신 확인.
- **REQ-PRD-MET-04**: 운영자가 health 저하를 Slack에서 인지할 수 있다. Evidence: health degraded 이벤트의 Slack 수신 확인.
- **REQ-PRD-MET-05**: 운영자가 Rollouts abort를 Slack에서 인지할 수 있다. Evidence: Rollouts abort 이벤트의 Slack 수신 확인.

## Scope and Non-goals

- **In Scope**:
  - ArgoCD Notifications 컨트롤러 활성화 요구
  - Slack credential Vault/ESO 보안 경계
  - 알림 template + trigger 요구
  - Default subscriptions 설정
- **Out of Scope**:
  - Email/PagerDuty 알림 채널
  - Alertmanager 통합
- **Non-goals**:
  - 알림 채널 per-app 자동 분기 (단일 채널 기본)
  - Slack workspace 또는 채널 생성 자체

## Risks, Dependencies, and Assumptions

- Notification credential은 human-approved 외부 bootstrap 작업으로 준비되어야 한다.
- Slack Bot token 발급 및 채널 권한 부여는 Slack workspace 관리자 협력이 필요하다.
- ESO가 정상 동작 중인 상태를 전제한다 (현재 baseline PRD 의존).
- Argo Rollouts가 설치된 상태에서 rollout-\* 이벤트가 동작한다 (PRD `001-argo-rollouts-progressive-delivery.md` 의존).

### Agent execution and approval requirements

- **Allowed Actions**: Update PRD/documentation, run non-destructive static validation, and collect read-only status evidence.
- **Disallowed Actions**: Store Slack credentials in plaintext, modify Vault paths without approval, or change manifests outside an approved downstream stage.
- **Human-in-the-loop Requirement**: Required before initial notification credential registration or Slack channel permission changes.
- **Evaluation Expectation**: Verify controller status, ExternalSecret readiness, and Slack notification receipt in a downstream validation stage.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-PRD-FUN-01 | ArgoCD Notifications controller가 활성화되고 운영자가 Pod 상태를 확인할 수 있다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-FUN-02 | Slack credential이 Vault에서 ESO를 거쳐 동기화되며 Git과 로그에 평문 token이 없다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-FUN-03 | ConfigMap이 배포, health, sync, Rollouts 완료 및 abort 이벤트의 template과 trigger를 정의한다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-FUN-04 | default subscriptions가 health 저하와 sync 실패 알림을 전체 앱에 적용한다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-FUN-05 | 앱 annotation으로 `on-deployed` Slack 채널 opt-in을 선언할 수 있다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-FUN-06 | notification credential bootstrap은 human-approved 외부 작업으로만 수행된다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-MET-01 | `argocd-notifications-controller` Pod가 `Running`임을 운영자가 확인할 수 있다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-MET-02 | `argocd-notifications-secret` ExternalSecret이 `Ready=True`임을 확인할 수 있다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-MET-03 | 의도적으로 발생시킨 sync 실패 이벤트가 승인된 Slack 채널에 도착한다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-MET-04 | health degraded 이벤트가 승인된 Slack 채널에 도착한다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |
| REQ-PRD-MET-05 | Rollouts abort 이벤트가 승인된 Slack 채널에 도착한다. | [ARD 0005](../02.architecture/requirements/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/005-argo-notifications-slack/spec.md) |

- **ARD**: [`../02.architecture/requirements/0005-argo-notifications-slack.md`](../02.architecture/requirements/0005-argo-notifications-slack.md)
- **Spec**: [`../03.specs/005-argo-notifications-slack/spec.md`](../03.specs/005-argo-notifications-slack/spec.md)
- **Plan**: [`../04.execution/plans/2026-05-18-argo-notifications-slack.md`](../04.execution/plans/2026-05-18-argo-notifications-slack.md)
- **Task**: [`../04.execution/tasks/2026-05-18-argo-notifications-slack.md`](../04.execution/tasks/2026-05-18-argo-notifications-slack.md)
- **ADR**: [`../02.architecture/decisions/0012-argo-notifications-slack.md`](../02.architecture/decisions/0012-argo-notifications-slack.md)
- **ADR**: [`../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../02.architecture/decisions/0003-eso-vault-k8s-auth.md)
- **PRD**: [`./001-argo-rollouts-progressive-delivery.md`](./001-argo-rollouts-progressive-delivery.md) — Rollouts 이벤트 소스
- **PRD**: [`./004-current-local-gitops-platform.md`](./004-current-local-gitops-platform.md) — ESO/Vault 의존
