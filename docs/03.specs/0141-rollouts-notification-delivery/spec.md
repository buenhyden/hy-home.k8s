---
title: "Rollouts Notification Delivery"
version: "0.1.2"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0141"
---

# Rollouts Notification Delivery Technical Specification (Spec)

## Overview

On 2026-11-05 the operator asked to close the open Rollouts notification gap:
Argo Rollouts completion and abort events must reach the shared Slack channel.
[ADR-0054](../../02.architecture/decisions/0054-platform-decision-current-state-amendment.md)
clause 2 records the decision. Today the `rollout-*` templates and triggers
sit in `argocd-notifications-cm`, which the ArgoCD Notifications controller
evaluates against Applications only, so they never fire, and the Rollouts
controller's own notification engine has no service, secret or subscription.
The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-rollouts-notification-delivery.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the `notifications` values of `gitops/apps/root/platform-rollouts-app.yaml`;
  - a new ExternalSecret for the Rollouts notification secret under
    `gitops/platform/eso/`;
  - removing the `rollout-*` templates and triggers from
    `gitops/platform/argocd/argocd-notifications-cm.yaml`;
  - the matching assertions in `scripts/validate-infrastructure-contracts.sh`;
  - REQ-0002, AD-0005, ADR-0012 and the operations runbook text that states
    the current delivery path.
- Non-goals:
  - templates or triggers beyond the completion and abort pairs taken from
    the upstream catalog, per-Rollout routing, or other Rollouts events;
  - writing the OpenBao entry, reading the token, or any live cluster action;
  - changing the ArgoCD Notifications application triggers or subscriptions.

## Contracts

- The Rollouts chart renders `argo-rollouts-notification-configmap` with
  `service.slack` (`token: $slack-token`) and one default subscription that
  sends `on-rollout-completed` and `on-rollout-aborted` to
  `slack:hy-home-alerts`. The controller ships no triggers or templates, so
  the chart values also define `trigger.on-rollout-completed`,
  `trigger.on-rollout-aborted`, `template.rollout-completed` and
  `template.rollout-aborted` after the upstream `manifests/notifications`
  catalog.
- `argo-rollouts/argo-rollouts-notification-secret` is created only by an
  ExternalSecret from the `vault-backend` ClusterSecretStore, key
  `platform/notifications`, property `slack_token`, target key `slack-token`,
  with the label `app.kubernetes.io/component: rollouts-controller`. No
  secret value enters Git.
- `argocd-notifications-cm` holds no `rollout-*` template or trigger.
- The static contract validator fails if any of these three statements stops
  being true.

## Core Design

The Rollouts controller already runs the notifications engine; it reads the
chart-managed ConfigMap and the named Secret in its own namespace. Moving the
configuration there needs no new component, but every trigger and template
must be defined in that ConfigMap; the engine has no defaults. The existing OpenBao policy
`eso-read` already allows `secret/data/platform/notifications`, so the
ExternalSecret reuses the same credential as ArgoCD Notifications.

## Data Modeling & Storage Strategy

One Kubernetes Secret, owned by its ExternalSecret (`creationPolicy: Owner`),
refreshed hourly from OpenBao. No new OpenBao path is introduced.

## Interfaces & Data Structures

- Chart values `notifications.notifiers` and `notifications.subscriptions`
  (chart `argo-rollouts` 2.40.9, `templates/controller/notifications-configmap.yaml`).
- ExternalSecret `external-secrets.io/v1beta1`, as the existing
  `prometheus-api-auth` ExternalSecret uses.

## Edge Cases & Error Handling

- Normal: a Rollout finishes or aborts and one Slack message is sent
  (REQ-0002-FR-0001, FR-0003).
- Error: the OpenBao entry lacks `slack_token`; the ExternalSecret stays not
  ready, no Secret exists, and the engine logs a missing-token error without
  affecting rollout progress (REQ-0002-IF-0002).
- Boundary: the platform ArgoCD notifications keep their own subscription;
  no event is sent twice because the ArgoCD controller never evaluated the
  removed Rollouts triggers (REQ-0002-NFR-0001).

## Failure Modes & Fallback / Human Escalation

Notification failure never blocks a rollout. Rollback is reverting the
change; the operator owns the OpenBao entry and live receipt.

## Verification Commands

- `bash scripts/validate-infrastructure-contracts.sh` — PASS after the change,
  FAIL on the old manifests once the assertions change.
- `helm template` of `argo-rollouts` 2.40.9 with the Application values — the
  rendered ConfigMap holds `service.slack` and the subscription.
- `python3 scripts/qa.py staged` on each commit.
- Live Slack receipt is an operator observation and stays `DEFER`.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RND-001 | Rendered Rollouts ConfigMap and the new ExternalSecret meet the Contracts; static contract validator PASS |
| VAL-RND-002 | `argocd-notifications-cm` has no `rollout-*` key; the validator fails on the old manifests and passes on the new |
| VAL-RND-003 | REQ-0002, AD-0005, ADR-0012 and the runbook state the delivery path; strict document checks PASS |
| VAL-RND-004 | Operator observes a Rollouts abort or completion message in `#hy-home-alerts` |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0002-FR-0001](../../01.requirements/0002-argo-notifications-slack.md) | VAL-RND-001 | Static contract validator and rendered chart output |
| [REQ-0002-FR-0002](../../01.requirements/0002-argo-notifications-slack.md) | VAL-RND-001 | ExternalSecret review; secret scanning finds no token |
| [REQ-0002-FR-0003](../../01.requirements/0002-argo-notifications-slack.md) | VAL-RND-002 | Validator assertions on both ConfigMaps |
| [REQ-0002-NFR-0001](../../01.requirements/0002-argo-notifications-slack.md) | VAL-RND-003 | Document review and strict document checks |
| [REQ-0002-IF-0002](../../01.requirements/0002-argo-notifications-slack.md) | VAL-RND-004 | Operator live observation after the OpenBao entry is confirmed |
