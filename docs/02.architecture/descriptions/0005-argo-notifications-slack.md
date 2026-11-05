---
title: "Argo Notifications Slack Architecture Description"
version: "1.1.2"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-11-05"
layer: "architecture"
artifact_id: "AD-0005"
---

# Argo Notifications Slack Architecture Description

## Overview

This document defines the reference architecture and quality attributes of Slack notifications based on ArgoCD Notifications.
The ArgoCD values, Notifications ConfigMap, and ExternalSecret already exist in the repository, so this AD is a backfill that turns the repo-backed execution contract into traceable architecture input.

### Current architecture summary

ArgoCD Notifications is enabled as the built-in controller in the `argocd` namespace, and the Slack token syncs from OpenBao through ESO into `argocd-notifications-secret`.
Notification templates, triggers, `service.slack` (token `$slack-token`), `defaultTriggers` and a `subscriptions` block are managed as a GitOps ConfigMap. The `subscriptions` block sends on-health-degraded, on-sync-failed and on-deployed for all apps to `slack:hy-home-alerts`; annotation opt-in remains an optional additional channel and no app uses it today. Neither declaration alone proves receipt in Slack.

## Boundaries & Non-goals

- **Owns**:
  - The `notifications.enabled: true` contract in the ArgoCD Helm values
  - The `argocd-notifications-cm` template/trigger/subscription contract
  - The `argocd-notifications-secret` ExternalSecret and OpenBao path contract
  - The security boundary and operational validation path of Slack notifications
- **Consumes**:
  - The External Secrets Operator and OpenBao (KV v2 `secret`, key `platform/notifications`, property `slack_token`) through the `vault-backend` Vault-API ClusterSecretStore ([ADR-0041](../decisions/0041-openbao-secret-backend.md))
  - ArgoCD application status events
  - Rollouts events, sent by the Argo Rollouts controller's own notification engine with the `on-rollout-completed` and `on-rollout-aborted` triggers and templates defined in the Rollouts chart values, the same OpenBao credential through `argo-rollouts-notification-secret`, and the shared channel ([ADR-0054](../decisions/0054-platform-decision-current-state-amendment.md) clause 2)
  - Slack workspace token/channel permission
- **Does Not Own**:
  - Creating the Slack workspace or channels
  - PagerDuty, Email, Alertmanager integration
  - The Rollouts chart's own notification settings
- **Non-goals**:
  - Automatic per-app notification channel routing (one shared channel is the default)
  - Plaintext credential bootstrap
  - Integrating an external incident management platform

## Quality Attributes

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| Performance | The Notifications controller processes app events | ArgoCD release in `argocd` | Controller state stays observable | In-cluster Alloy scrapes the controller metrics port (9001) |
| Security | The Slack token is synced | OpenBao, ESO, `argocd-notifications-secret` | The token travels only along that path | No token value in docs, manifests, logs or commits |
| Reliability | The ConfigMap or ExternalSecret is lost | Cluster rebuild from GitOps | Both are recovered from desired state | The ExternalSecret reaches Ready after sync |
| Scalability | A new app is added | Shared-channel `subscriptions` | Common failure signals reach the shared channel with no per-app change | The `subscriptions` block covers all apps; annotations add optional channels |
| Observability | Slack delivery succeeds or fails | Controller logs and metrics | Operators see delivery and error state | Controller log shows send or error per event |
| Operability | A Slack notification fails | Operator troubleshooting | Check OpenBao secret, then ExternalSecret, then controller log | The runbook lists the three checks in that order |

## System Overview & Context

- ArgoCD Helm values are stored in `infrastructure/argocd/values-local.yaml`.
- Notification templates and triggers are stored in `gitops/platform/argocd/argocd-notifications-cm.yaml`.
- Slack token material is represented by `gitops/platform/argocd/argocd-notifications-secret.yaml`.
- The ConfigMap and ExternalSecret are included through `gitops/platform/argocd/kustomization.yaml`.
The current sources are the [Notifications ConfigMap](../../../gitops/platform/argocd/argocd-notifications-cm.yaml) and
the [ExternalSecret reference](../../../gitops/platform/argocd/argocd-notifications-secret.yaml).
ArgoCD Notifications evaluates Applications only, so Rollouts events are configured in the Rollouts chart's `notifications` values and the [Rollouts notification ExternalSecret](../../../gitops/platform/eso/rollouts-notification-secret.yaml), not in this ConfigMap.

## Data Architecture

- **Key Entities / Flows**:
  - OpenBao KV v2 `secret/platform/notifications`, property `slack_token`.
  - ExternalSecret `argocd-notifications-secret`.
  - Kubernetes Secret key `slack-token`.
  - ConfigMap entries `service.slack`, `template.*`, `trigger.*`, `defaultTriggers` and `subscriptions`.
  - Optional Application annotation `notifications.argoproj.io/subscribe.<trigger>.slack` for an additional channel.
- **Storage Strategy**:
  - Credential source of truth is OpenBao.
  - Git stores only non-secret templates, triggers, ExternalSecret references, and Helm values.
- **Data Boundaries**:
  - Slack token values must never appear in docs, manifests, logs, commit messages, or PR descriptions.
  - Human-approved external bootstrap is required before live notification validation.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - ArgoCD Notifications runs inside the ArgoCD release in `argocd`.
  - ExternalSecret sync depends on ESO and OpenBao availability.
- **Deployment Model**:
  - `notifications.enabled: true` is set in ArgoCD Helm values.
  - `argocd-notifications-cm` and `argocd-notifications-secret` are GitOps-managed through `platform-argocd-config`.
  - The ConfigMap declares the `subscriptions` block (shared channel `slack:hy-home-alerts` for health-degraded, sync-failed and deployed). Actual delivery requires separate approved runtime evidence; the static declaration is not that evidence.
- **Operational Evidence**:
  - Static contract checks validate notification and secret wiring.
  - Runtime runbook checks controller Pod, ExternalSecret/Secret readiness, and Slack send/error logs.

### Agent architecture requirements

- **Model/Provider Strategy**: Agents may update templates and docs, but must not invent or expose Slack credentials.
- **Tooling Boundary**: Agents must not run OpenBao writes or Slack bootstrap commands unless explicitly approved by a human.
- **Memory & Context Strategy**: Security-sensitive findings are summarized without credential material.
- **Guardrail Boundary**: Rollouts chart notifications and ArgoCD Notifications must remain distinct in docs and specs.
- **Latency / Cost Budget**: Not applicable.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0002-FR-0001](../../01.requirements/0002-argo-notifications-slack.md) | The ownership boundary of the Notifications controller inside the ArgoCD release | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| [REQ-0002-FR-0002](../../01.requirements/0002-argo-notifications-slack.md) | The one-way OpenBao → ESO → Kubernetes Secret credential boundary | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| [REQ-0002-FR-0003](../../01.requirements/0002-argo-notifications-slack.md) | The template and trigger catalog owned by the GitOps ConfigMap | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| [REQ-0002-NFR-0001](../../01.requirements/0002-argo-notifications-slack.md) | The shared-channel default subscription boundary for common health/sync failures and deployments | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| [REQ-0002-IF-0001](../../01.requirements/0002-argo-notifications-slack.md) | The optional annotation-based per-app opt-in boundary (the implemented default is the shared `subscriptions` block) | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| [REQ-0002-IF-0002](../../01.requirements/0002-argo-notifications-slack.md) | The approval boundary that separates Slack/OpenBao bootstrap from repository changes | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Notifications controller Pod readiness evidence | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Credential sync evidence from the ExternalSecret Ready state | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Human-approved live receipt evidence for sync failure notifications | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Human-approved live receipt evidence for health degraded notifications | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |
| N/A — [Acceptance criterion 05](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Human-approved live receipt evidence for Rollouts abort notifications sent by the Rollouts notification engine ([REQ-0002](../../01.requirements/0002-argo-notifications-slack.md)) | [ADR 0012](../decisions/0012-argo-notifications-slack.md) |

- **Requirement**: [`../../01.requirements/0002-argo-notifications-slack.md`](../../01.requirements/0002-argo-notifications-slack.md)
- **Spec**: N/A — SPEC-0005 left the tree; Git history recovers it ([REQ-0002 Archived Lineage](../../01.requirements/0002-argo-notifications-slack.md#archived-lineage))
- **ADR**: [`../decisions/0012-argo-notifications-slack.md`](../decisions/0012-argo-notifications-slack.md)
- **ADR**: [`../decisions/0054-platform-decision-current-state-amendment.md`](../decisions/0054-platform-decision-current-state-amendment.md) — current token, backend and subscription clauses
