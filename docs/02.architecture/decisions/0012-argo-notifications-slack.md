# ADR-0012: Argo Notifications with Slack Webhook

## Overview (KR)

Argo Notifications를 ArgoCD 컨트롤러로 활성화하고 Slack webhook을 알림 destination으로 사용한다.
ArgoCD 앱 이벤트(sync 실패, health 저하, 배포 완료)와 Rollouts 이벤트(완료, abort)를 Slack으로 전달한다.

## Context

GitOps 이벤트(앱 동기화 실패, health 저하)와 Rollouts 이벤트를 운영자에게 자동 전달할 수단이 필요하다.
ArgoCD Helm chart v2.x에 Notifications controller가 내장되어 있어 별도 설치 없이 `notifications.enabled=true`로 활성화 가능하다.

## Decision

- ArgoCD Helm values에 `notifications.enabled: true` 추가.
- Slack token은 Vault `secret/platform/notifications` → ESO ExternalSecret → `argocd-notifications-secret` k8s Secret으로 관리.
- ConfigMap `argocd-notifications-cm`에 templates(app-deployed, app-health-degraded, app-sync-failed, rollout-completed, rollout-aborted)와 triggers 정의.
- Default subscriptions: `on-health-degraded`, `on-sync-failed`.
- 앱별 opt-in: annotation `notifications.argoproj.io/subscribe.on-deployed.slack: <channel>`.

## Explicit Non-goals

- Email/PagerDuty 알림 (Slack webhook만)
- 알림 채널 per-app 자동 분기 (단일 채널 기본)
- Alertmanager 통합

## Alternatives

| 옵션                            | 평가                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| ArgoCD 내장 Notifications       | 추가 컴포넌트 없음, ArgoCD와 동일 lifecycle                                           |
| 독립 Notifications 배포         | 불필요한 중복, 이 규모에서는 과도함                                                   |
| Prometheus Alertmanager → Slack | 이미 외부 Prometheus 있지만, GitOps 이벤트는 ArgoCD가 소스이므로 Notifications가 적합 |

## Consequences

- `argocd-notifications-cm` ConfigMap: templates + triggers (GitOps 관리)
- `argocd-notifications-secret` (ESO): Slack token (Vault `secret/platform/notifications.slack_token`)
- Vault에 `secret/platform/notifications` path 수동 추가 필요 (bootstrap 외부 작업)
- `argocd-notifications-controller` Pod가 argocd namespace에 추가됨

## Vault Secret 준비

```bash
# external secret operation; human-approved bootstrap only
vault kv put secret/platform/notifications \
  slack_token="xoxb-your-slack-bot-token"
```

## Status

Accepted — 2026-03-30

## Related Documents

- [ADR-0011](./0011-argo-rollouts-progressive-delivery.md) — Rollouts 이벤트 소스
- [ADR-0003](./0003-eso-vault-k8s-auth.md) — ESO/Vault 시크릿 관리 패턴
- [PRD](../../01.requirements/2026-05-17-argo-notifications-slack.md)
- [ARD](../requirements/0005-argo-notifications-slack.md)
- [Spec](../../03.specs/005-argo-notifications-slack/spec.md)
- [Plan](../../04.execution/plans/2026-05-18-argo-notifications-slack.md)
- [Task](../../04.execution/tasks/2026-05-18-argo-notifications-slack.md)
