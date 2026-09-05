---
title: "Argo Notifications Slack Webhook Requirement Package"
version: "1.0.0"
type: "sdlc/requirement"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "requirements"
artifact_id: "REQ-0002"
---

# Argo Notifications Slack Webhook Requirement Package

## Overview

이 문서는 ArgoCD Notifications 컨트롤러를 활성화하고 Slack webhook을 알림 destination으로 사용하여 GitOps 이벤트(sync 실패, health 저하, 배포 완료)와 Rollouts 이벤트(완료, abort)를 운영자에게 자동 전달하기 위한 제품 요구사항을 정의한다.

### Current requirement status

이 Requirement는 current-contract backfill 기준의 active 문서다.
ArgoCD Notifications values, ConfigMap, ExternalSecret, 운영 문서는 이미 저장소에 존재하며, 2026-05-18에 AD/Spec/Plan/Task 추적 체인을 보강했다.
이 문서는 알림의 사용자 가치와 보안 경계를 소유하고, Secret 생성 절차와 manifest 계약은 연결된 downstream 문서와 운영 런북이 소유한다.

## Vision

플랫폼 이벤트(ArgoCD 동기화 실패, 서비스 health 저하, Rollouts 완료/abort)가 운영자에게 Slack으로 자동 전달되어 수동 모니터링 없이 신속한 대응이 가능해진다.

## Problem Statement

저장소에는 알림 설정이 있지만 설정의 존재만으로 이벤트 전달과 실제 수신을 보장할 수 없다. 운영자가 수동 UI 확인에만 의존하지 않도록 공통 실패 신호와 선택적 배포 알림의 수용 기준을 유지해야 한다.

## Personas

- **Platform Engineer**: ArgoCD 이벤트와 Rollouts 이벤트를 Slack 채널에서 실시간으로 수신하고 싶다.
- **DevOps Engineer**: 동기화 실패나 health 저하 시 즉각 알림을 받아 신속하게 대응하고 싶다.
- **Application Team**: 배포 완료(on-deployed) 이벤트를 특정 Slack 채널에서 선택적으로 수신하고 싶다.

## Key Use Cases

- **STORY-01**: ArgoCD 앱이 sync에 실패하면 운영자 Slack 채널로 즉시 알림이 전송된다.
- **STORY-02**: 앱 health가 저하되면(Degraded) 운영자 Slack 채널로 즉시 알림이 전송된다.
- **STORY-03**: Argo Rollouts 배포가 완료되거나 abort되면 Slack 알림이 전송된다.
- **STORY-04**: 애플리케이션 팀이 앱별 설정으로 배포 완료 알림을 특정 채널에 opt-in한다.

## Functional Requirements

- **REQ-0002-FR-0001**: 플랫폼은 GitOps 이벤트를 운영자의 Slack 채널에 전달해야 한다. Controller와 구체 설정은 downstream Spec이 소유한다.
- **REQ-0002-FR-0002**: Slack credential material은 승인된 외부 secret source와 제한된 동기화 경계를 통해서만 소비되어야 하며 PRD, manifest, 로그에 평문으로 노출되지 않아야 한다.
- **REQ-0002-FR-0003**: 알림 템플릿과 trigger는 배포 완료, health 저하, sync 실패, Rollouts 완료, Rollouts abort 이벤트를 표현해야 한다.
- **REQ-0002-NFR-0001**: 공통 기본 알림 정책은 health 저하와 sync 실패를 전체 앱에 적용해야 한다. 현재 설정의 존재는 전체 앱 구독이나 실제 수신을 증명하지 않는다.
- **REQ-0002-IF-0001**: 애플리케이션 팀은 배포 완료 알림의 Slack 채널을 앱별로 opt-in할 수 있어야 한다. Native annotation 문법은 AD/Spec이 소유한다.
- **REQ-0002-IF-0002**: 알림 credential bootstrap은 human-approved 외부 작업으로만 수행되어야 한다.

## Success / Acceptance Criteria

- **Acceptance criterion 01**: 운영자가 Notifications controller 상태를 확인할 수 있다. Evidence: `argocd-notifications-controller` Pod `Running`.
- **Acceptance criterion 02**: 운영자가 Vault-backed notification credential sync 상태를 확인할 수 있다. Evidence: `argocd-notifications-secret` ExternalSecret `Ready=True`.
- **Acceptance criterion 03**: 운영자가 sync 실패를 Slack에서 인지할 수 있다. Evidence: sync 실패 이벤트의 Slack 수신 확인.
- **Acceptance criterion 04**: 운영자가 health 저하를 Slack에서 인지할 수 있다. Evidence: health degraded 이벤트의 Slack 수신 확인.
- **Acceptance criterion 05**: 운영자가 Rollouts abort를 Slack에서 인지할 수 있다. Evidence: Rollouts abort 이벤트의 Slack 수신 확인.

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
- ESO가 정상 동작 중인 상태를 전제한다 (현재 baseline Requirement 의존).
- Argo Rollouts가 설치된 상태에서 rollout-\* 이벤트가 동작한다 (PRD `0001-argo-rollouts-progressive-delivery.md` 의존).

### Agent execution and approval requirements

- **Allowed Actions**: Update PRD/documentation, run non-destructive static validation, and collect read-only status evidence.
- **Disallowed Actions**: Store Slack credentials in plaintext, modify Vault paths without approval, or change manifests outside an approved downstream stage.
- **Human-in-the-loop Requirement**: Required before initial notification credential registration or Slack channel permission changes.
- **Evaluation Expectation**: Verify controller status, ExternalSecret readiness, and Slack notification receipt in a downstream validation stage.

구체 manifest, hostname, annotation, 리소스 상태와 검증 명령은 연결된 AD/Spec/운영 owner가 소유한다.
이 갱신은 runtime 상태나 live 알림 수신을 관측했다는 주장이 아니다.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0002-FR-0001 | ArgoCD Notifications controller가 활성화되고 운영자가 Pod 상태를 확인할 수 있다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-FR-0002 | Slack credential이 Vault에서 ESO를 거쳐 동기화되며 Git과 로그에 평문 token이 없다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-FR-0003 | ConfigMap이 배포, health, sync, Rollouts 완료 및 abort 이벤트의 template과 trigger를 정의한다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-NFR-0001 | default subscriptions가 health 저하와 sync 실패 알림을 전체 앱에 적용한다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-IF-0001 | 앱별 배포 완료 알림의 Slack 채널 opt-in을 선언할 수 있다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-IF-0002 | notification credential bootstrap은 human-approved 외부 작업으로만 수행된다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | `argocd-notifications-controller` Pod가 `Running`임을 운영자가 확인할 수 있다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | `argocd-notifications-secret` ExternalSecret이 `Ready=True`임을 확인할 수 있다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | 의도적으로 발생시킨 sync 실패 이벤트가 승인된 Slack 채널에 도착한다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | health degraded 이벤트가 승인된 Slack 채널에 도착한다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 05 remains acceptance-only | Rollouts abort 이벤트가 승인된 Slack 채널에 도착한다. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../03.specs/0005-argo-notifications-slack/spec.md) |

- **AD**: [`../02.architecture/descriptions/0005-argo-notifications-slack.md`](../02.architecture/descriptions/0005-argo-notifications-slack.md)
- **Spec**: [`../03.specs/0005-argo-notifications-slack/spec.md`](../03.specs/0005-argo-notifications-slack/spec.md)
- **Plan**: [`../03.specs/0005-argo-notifications-slack/plan.md`](../03.specs/0005-argo-notifications-slack/plan.md)
- **Task**: [Spec 0005 Plan](../03.specs/0005-argo-notifications-slack/plan.md)
- **ADR**: [`../02.architecture/decisions/0012-argo-notifications-slack.md`](../02.architecture/decisions/0012-argo-notifications-slack.md)
- **ADR**: [`../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../02.architecture/decisions/0003-eso-vault-k8s-auth.md)
- **Requirement**: [`./0001-argo-rollouts-progressive-delivery.md`](./0001-argo-rollouts-progressive-delivery.md) — Rollouts 이벤트 소스
- **Requirement**: [`./0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md) — ESO/Vault 의존
