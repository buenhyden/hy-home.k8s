---
title: 'Argo Notifications Slack Architecture Reference Document'
type: sdlc/ard
status: active
owner: platform
updated: 2026-07-13
---

# Argo Notifications Slack Architecture Reference Document

## Overview

이 문서는 ArgoCD Notifications 기반 Slack 알림의 참조 아키텍처와 품질 속성을 정의한다.
현재 ArgoCD values, Notifications ConfigMap, ExternalSecret이 이미 저장소에 존재하므로, 이 ARD는 repo-backed 실행계약을 추적 가능한 아키텍처 입력으로 정리하는 backfill 문서다.

### Current architecture summary

ArgoCD Notifications는 `argocd` namespace의 내장 controller로 활성화되며, Slack token은 Vault에서 ESO를 통해 `argocd-notifications-secret`로 동기화된다.
알림 template, trigger, default subscription은 GitOps ConfigMap으로 관리하고, 앱별 opt-in은 annotation으로 제한한다.

## Boundaries & Non-goals

- **Owns**:
  - ArgoCD Helm values의 `notifications.enabled: true` 계약
  - `argocd-notifications-cm` template/trigger/subscription 계약
  - `argocd-notifications-secret` ExternalSecret과 Vault path 계약
  - Slack 알림의 보안 경계와 운영 검증 경로
- **Consumes**:
  - External Secrets Operator와 Vault `secret/platform/notifications`
  - ArgoCD application status events
  - Rollouts event template context where supported by Notifications
  - Slack workspace token/channel permission
- **Does Not Own**:
  - Slack workspace/channel 생성
  - PagerDuty, Email, Alertmanager integration
  - Rollouts chart 자체 notifications 설정
- **Non-goals**:
  - 알림 채널 per-app 자동 분기
  - 평문 credential bootstrap
  - 외부 incident management platform 통합

## Quality Attributes

- **Performance**: Notifications controller metrics를 활성화해 처리 상태를 관측할 수 있게 한다.
- **Security**: Slack token은 Vault -> ESO -> Kubernetes Secret 경로로만 소비한다.
- **Reliability**: ConfigMap과 ExternalSecret은 GitOps desired state로 복구 가능해야 한다.
- **Scalability**: default subscriptions는 공통 실패 신호를 다루고, 앱별 channel opt-in은 annotation으로 확장한다.
- **Observability**: controller logs와 metrics NodePort가 Slack 전송 성공/실패와 runtime 상태를 확인하는 증거다.
- **Operability**: Slack 알림 장애 시 Vault secret, ExternalSecret, controller log 순서로 검증한다.

## System Overview & Context

- ArgoCD Helm values are stored in `infrastructure/argocd/values-local.yaml`.
- Notification templates and triggers are stored in `gitops/platform/argocd/argocd-notifications-cm.yaml`.
- Slack token material is represented by `gitops/platform/argocd/argocd-notifications-secret.yaml`.
- The ConfigMap and ExternalSecret are included through `gitops/platform/argocd/kustomization.yaml`.
- ArgoCD Notifications is separate from the Rollouts Helm chart `notifications.enabled` setting, which remains disabled.

## Data Architecture

- **Key Entities / Flows**:
  - Vault KV `secret/platform/notifications.slack_token`.
  - ExternalSecret `argocd-notifications-secret`.
  - Kubernetes Secret key `slack-token`.
  - ConfigMap entries `template.*`, `trigger.*`, and `defaultTriggers`.
  - Application annotation `notifications.argoproj.io/subscribe.<trigger>.slack`.
- **Storage Strategy**:
  - Credential source of truth is Vault.
  - Git stores only non-secret templates, triggers, ExternalSecret references, and Helm values.
- **Data Boundaries**:
  - Slack token values must never appear in docs, manifests, logs, commit messages, or PR descriptions.
  - Human-approved external bootstrap is required before live notification validation.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - ArgoCD Notifications runs inside the ArgoCD release in `argocd`.
  - ExternalSecret sync depends on ESO and Vault availability.
- **Deployment Model**:
  - `notifications.enabled: true` is set in ArgoCD Helm values.
  - `argocd-notifications-cm` and `argocd-notifications-secret` are GitOps-managed through `platform-argocd-config`.
  - Default subscriptions cover health degraded and sync failed events.
- **Operational Evidence**:
  - Static contract checks validate notification and secret wiring.
  - Runtime runbook checks controller Pod, ExternalSecret/Secret readiness, and Slack send/error logs.

### Agent architecture requirements

- **Model/Provider Strategy**: Agents may update templates and docs, but must not invent or expose Slack credentials.
- **Tooling Boundary**: Agents must not run Vault writes or Slack bootstrap commands unless explicitly approved by a human.
- **Memory & Context Strategy**: Security-sensitive findings are summarized without credential material.
- **Guardrail Boundary**: Rollouts chart notifications and ArgoCD Notifications must remain distinct in docs and specs.
- **Latency / Cost Budget**: Not applicable.

## Traceability

- **PRD**: [`../../01.requirements/002-argo-notifications-slack.md`](../../01.requirements/002-argo-notifications-slack.md)
- **Spec**: [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)
- **Plan**: [`../../04.execution/plans/2026-05-18-argo-notifications-slack.md`](../../04.execution/plans/2026-05-18-argo-notifications-slack.md)
- **ADR**: [`../decisions/0012-argo-notifications-slack.md`](../decisions/0012-argo-notifications-slack.md)
