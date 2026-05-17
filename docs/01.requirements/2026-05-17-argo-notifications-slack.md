---
title: 'Argo Notifications Slack Webhook Product Requirements'
type: prd
status: draft
owner: platform-team
updated: 2026-05-17
---

# Argo Notifications Slack Webhook Product Requirements

## Overview (KR)

이 문서는 ArgoCD Notifications 컨트롤러를 활성화하고 Slack webhook을 알림 destination으로 사용하여 GitOps 이벤트(sync 실패, health 저하, 배포 완료)와 Rollouts 이벤트(완료, abort)를 운영자에게 자동 전달하기 위한 제품 요구사항을 정의한다.

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

- **REQ-PRD-FUN-01**: ArgoCD Helm values에 `notifications.enabled: true`를 설정하여 Notifications 컨트롤러를 활성화해야 한다.
- **REQ-PRD-FUN-02**: Slack token은 Vault `secret/platform/notifications` → ESO ExternalSecret → `argocd-notifications-secret` K8s Secret으로 관리해야 한다.
- **REQ-PRD-FUN-03**: `argocd-notifications-cm` ConfigMap에 다음 template과 trigger를 정의해야 한다:
  - Templates: `app-deployed`, `app-health-degraded`, `app-sync-failed`, `rollout-completed`, `rollout-aborted`
  - Triggers: `on-deployed`, `on-health-degraded`, `on-sync-failed`
- **REQ-PRD-FUN-04**: Default subscriptions는 `on-health-degraded`, `on-sync-failed`를 전체 앱에 적용해야 한다.
- **REQ-PRD-FUN-05**: 앱별 opt-in은 annotation `notifications.argoproj.io/subscribe.on-deployed.slack: <channel>`로 설정 가능해야 한다.
- **REQ-PRD-FUN-06**: Vault에 `secret/platform/notifications` path가 준비되어야 한다 (human-approved bootstrap 외부 작업).

## Success Criteria

- **REQ-PRD-MET-01**: `argocd-notifications-controller` Pod `Running` 상태.
- **REQ-PRD-MET-02**: `argocd-notifications-secret` ExternalSecret `Ready=True`.
- **REQ-PRD-MET-03**: sync 실패 시 Slack 채널에 알림 수신 확인.
- **REQ-PRD-MET-04**: health 저하 시 Slack 채널에 알림 수신 확인.
- **REQ-PRD-MET-05**: Rollouts abort 시 Slack 채널에 알림 수신 확인.

## Scope and Non-goals

- **In Scope**:
  - ArgoCD Notifications 컨트롤러 활성화 (Helm values)
  - Slack token Vault/ESO 시크릿 관리
  - ConfigMap templates + triggers GitOps 관리
  - Default subscriptions 설정
- **Out of Scope**:
  - Email/PagerDuty 알림 채널
  - Alertmanager 통합
- **Non-goals**:
  - 알림 채널 per-app 자동 분기 (단일 채널 기본)
  - Slack workspace 또는 채널 생성 자체

## Risks, Dependencies, and Assumptions

- Vault에 `secret/platform/notifications` path가 사전 준비되어야 한다 (human-approved 외부 bootstrap 작업 필요).
- Slack Bot token 발급 및 채널 권한 부여는 Slack workspace 관리자 협력이 필요하다.
- ESO가 정상 동작 중인 상태를 전제한다 (PRD `2026-03-28` 의존).
- Argo Rollouts가 설치된 상태에서 rollout-\* 이벤트가 동작한다 (PRD `2026-05-17-argo-rollouts-progressive-delivery.md` 의존).

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: GitOps manifest 생성/갱신, 비파괴 상태 검증, 문서 갱신.
- **Disallowed Actions**: Slack token 평문 저장, 승인 없는 Vault 경로 조작.
- **Human-in-the-loop Requirement**: Vault `secret/platform/notifications` 초기 등록 시 승인 필수.
- **Evaluation Expectation**: 컨트롤러 상태, ExternalSecret Ready, Slack 알림 수신을 검증 단계에서 확인.

## Related Documents

- **ADR**: [`../02.architecture/decisions/0012-argo-notifications-slack.md`](../02.architecture/decisions/0012-argo-notifications-slack.md)
- **ADR**: [`../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../02.architecture/decisions/0003-eso-vault-k8s-auth.md)
- **PRD**: [`./2026-05-17-argo-rollouts-progressive-delivery.md`](./2026-05-17-argo-rollouts-progressive-delivery.md) — Rollouts 이벤트 소스
- **PRD**: [`./2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md) — ESO/Vault 의존
