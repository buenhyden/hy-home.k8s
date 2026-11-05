---
title: "Argo Notifications with Slack"
version: "1.0.4"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-05"
layer: "architecture"
artifact_id: "ADR-0012"
---

# ADR-0012: Argo Notifications with Slack

## Overview

Argo Notifications is enabled as an ArgoCD controller, with Slack, authenticated by an app token, as the notification destination.
ArgoCD app events (sync failure, health degradation, deployment completion) are delivered to Slack. Rollouts events (completion, abort) have templates and triggers declared here; their delivery depends on Rollouts-side enablement.

## Context

A way to deliver GitOps events (app sync failure, health degradation) and, where enabled, Rollouts events to operators automatically is needed.
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
- `argocd-notifications-secret` (ESO): Slack token (OpenBao `secret/platform/notifications.slack_token`)
- The `secret/platform/notifications` path must be added to OpenBao by hand (an external bootstrap task)
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

**Current-state clarification (2026-11-05).** Four points differ from the
Decision. (1) The secret backend named as Vault is OpenBao, reached through the
`vault-backend` ClusterSecretStore under [ADR-0041](./0041-openbao-secret-backend.md).
(2) Slack authenticates with an app token (`service.slack`, token `$slack-token`),
not a webhook. (3) Rollouts events are not evaluated by the ArgoCD controller; the Argo
Rollouts controller's own notification engine sends them under ADR-0054
clause 2, and the `rollout-*` keys left this ConfigMap. (4) The implemented `subscriptions` block in
[`argocd-notifications-cm.yaml`](../../../gitops/platform/argocd/argocd-notifications-cm.yaml)
subscribes all apps to `on-health-degraded`, `on-sync-failed` and also
`on-deployed` on `slack:hy-home-alerts`. The default subscription sending
`on-deployed` extends the Decision's defaults and is permitted by
[REQ-0002-NFR-0001](../../01.requirements/0002-argo-notifications-slack.md); no
successor decision is pending for it. The Non-goal's "Slack webhook" means this
Slack app-token integration. The operator-approved [ADR-0054](./0054-platform-decision-current-state-amendment.md) (clause 2) records these replacements.

- **Requirement**: [REQ-0002](../../01.requirements/0002-argo-notifications-slack.md) — REQ-0002-FR-0001, REQ-0002-FR-0002, REQ-0002-FR-0003, REQ-0002-NFR-0001, REQ-0002-IF-0001, REQ-0002-IF-0002
- [ARD](../descriptions/0005-argo-notifications-slack.md)
- **Spec**: N/A — SPEC-0005 left the tree; Git history recovers it

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [Architecture owner](../descriptions/0005-argo-notifications-slack.md) | N/A — first decision; no whole-document supersession | N/A — SPEC-0005 left the tree; Git history recovers it |
