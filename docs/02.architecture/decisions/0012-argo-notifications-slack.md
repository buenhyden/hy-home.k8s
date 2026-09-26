---
title: "Argo Notifications with Slack Webhook"
version: "1.0.3"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0012"
---

# ADR-0012: Argo Notifications with Slack Webhook

## Overview

Argo Notifications is enabled as an ArgoCD controller, with a Slack webhook as the notification destination.
ArgoCD app events (sync failure, health degradation, deployment completion) and Rollouts events (completion, abort) are delivered to Slack.

## Context

A way to deliver GitOps events (app sync failure, health degradation) and Rollouts events to operators automatically is needed.
The ArgoCD Helm chart v2.x bundles the Notifications controller, so it can be enabled with `notifications.enabled=true` without a separate install.

## Decision

- `notifications.enabled: true` is added to the ArgoCD Helm values.
- The Slack token is managed as Vault `secret/platform/notifications` → ESO ExternalSecret → the `argocd-notifications-secret` k8s Secret.
- The ConfigMap `argocd-notifications-cm` defines the templates (app-deployed, app-health-degraded, app-sync-failed, rollout-completed, rollout-aborted) and triggers.
- Default subscriptions: `on-health-degraded`, `on-sync-failed`.
- Per-app opt-in: the annotation `notifications.argoproj.io/subscribe.on-deployed.slack: <channel>`.

### Decision status

Accepted — 2026-03-30

## Explicit Non-goals

- Email/PagerDuty notifications (Slack webhook only)
- Automatic per-app notification channel routing (a single channel is the default)
- Alertmanager integration

## Consequences

- `argocd-notifications-cm` ConfigMap: templates + triggers (managed through GitOps)
- `argocd-notifications-secret` (ESO): Slack token (Vault `secret/platform/notifications.slack_token`)
- The `secret/platform/notifications` path must be added to Vault by hand (an external bootstrap task)
- An `argocd-notifications-controller` Pod is added to the argocd namespace

### Operational prerequisite

Slack token bootstrap is performed only as a human-approved external OpenBao task. This ADR owns neither the secret value nor the execution procedure; the current operating procedure follows the [Rollouts/Notifications/Headlamp Runbook](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md) and the [ESO/OpenBao secret management decision](./0041-openbao-secret-backend.md).

## Alternatives

| Option | Assessment |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| Built-in ArgoCD Notifications | No extra component; same lifecycle as ArgoCD |
| Standalone Notifications deployment | Needless duplication; excessive at this scale |
| Prometheus Alertmanager → Slack | An external Prometheus already exists, but ArgoCD is the source of GitOps events, so Notifications fits |

## Traceability

- [ADR-0011](./0011-argo-rollouts-progressive-delivery.md) — Rollouts event source
- [ADR-0041](./0041-openbao-secret-backend.md) — ESO/OpenBao secret management pattern
- [PRD](../../01.requirements/0002-argo-notifications-slack.md)
- [ARD](../descriptions/0005-argo-notifications-slack.md)
- [Spec](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md)
- [Plan](../../98.archive/completed/03.specs/0005-argo-notifications-slack/plan.md)
- [Task](../../98.archive/completed/03.specs/0005-argo-notifications-slack/plan.md)
