---
title: "Argo Notifications Slack Architecture Description"
version: "1.0.1"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "AD-0005"
---

# Argo Notifications Slack Architecture Description

## Overview

This document defines the reference architecture and quality attributes of Slack notifications based on ArgoCD Notifications.
The ArgoCD values, Notifications ConfigMap, and ExternalSecret already exist in the repository, so this AD is a backfill that turns the repo-backed execution contract into traceable architecture input.

### Current architecture summary

ArgoCD Notifications is enabled as the built-in controller in the `argocd` namespace, and the Slack token syncs from Vault through ESO into `argocd-notifications-secret`.
Notification templates, triggers, and `defaultTriggers` are managed as a GitOps ConfigMap, and per-app opt-in is expressed with annotations. `defaultTriggers` alone proves neither a global subscription for every app nor receipt in Slack.

## Boundaries & Non-goals

- **Owns**:
  - The `notifications.enabled: true` contract in the ArgoCD Helm values
  - The `argocd-notifications-cm` template/trigger/subscription contract
  - The `argocd-notifications-secret` ExternalSecret and Vault path contract
  - The security boundary and operational validation path of Slack notifications
- **Consumes**:
  - The External Secrets Operator and Vault `secret/platform/notifications`
  - ArgoCD application status events
  - Rollouts event template context where supported by Notifications
  - Slack workspace token/channel permission
- **Does Not Own**:
  - Creating the Slack workspace or channels
  - PagerDuty, Email, Alertmanager integration
  - The Rollouts chart's own notification settings
- **Non-goals**:
  - Automatic per-app notification channel routing
  - Plaintext credential bootstrap
  - Integrating an external incident management platform

## Quality Attributes

- **Performance**: Notifications controller metrics are enabled so processing state can be observed.
- **Security**: the Slack token is consumed only along the Vault -> ESO -> Kubernetes Secret path.
- **Reliability**: the ConfigMap and ExternalSecret must be recoverable from the GitOps desired state.
- **Scalability**: subscribing to the common failure signals is a requirement, and per-app channel opt-in extends through annotations.
- **Observability**: controller logs and the metrics NodePort are the evidence for Slack delivery success or failure and runtime state.
- **Operability**: when Slack notifications fail, check the Vault secret, then the ExternalSecret, then the controller log.

## System Overview & Context

- ArgoCD Helm values are stored in `infrastructure/argocd/values-local.yaml`.
- Notification templates and triggers are stored in `gitops/platform/argocd/argocd-notifications-cm.yaml`.
- Slack token material is represented by `gitops/platform/argocd/argocd-notifications-secret.yaml`.
- The ConfigMap and ExternalSecret are included through `gitops/platform/argocd/kustomization.yaml`.
- ArgoCD Notifications is separate from the Rollouts Helm chart `notifications.enabled` setting, which remains disabled.

The current sources are the [Notifications ConfigMap](../../../gitops/platform/argocd/argocd-notifications-cm.yaml) and
the [ExternalSecret reference](../../../gitops/platform/argocd/argocd-notifications-secret.yaml).
The presence of a Rollouts event template does not guarantee runtime event context or successful delivery either.

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
  - The ConfigMap declares health-degraded and sync-failed default triggers. Global subscription coverage and actual delivery require separate approved runtime evidence; the static declaration is not that evidence.
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

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0002-FR-0001](../../01.requirements/0002-argo-notifications-slack.md) | The ownership boundary of the Notifications controller inside the ArgoCD release | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| [REQ-0002-FR-0002](../../01.requirements/0002-argo-notifications-slack.md) | The one-way Vault → ESO → Kubernetes Secret credential boundary | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| [REQ-0002-FR-0003](../../01.requirements/0002-argo-notifications-slack.md) | The template and trigger catalog owned by the GitOps ConfigMap | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| [REQ-0002-NFR-0001](../../01.requirements/0002-argo-notifications-slack.md) | The default subscription boundary for common health/sync failures | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| [REQ-0002-IF-0001](../../01.requirements/0002-argo-notifications-slack.md) | The annotation-based per-app deployment notification opt-in boundary | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| [REQ-0002-IF-0002](../../01.requirements/0002-argo-notifications-slack.md) | The approval boundary that separates Slack/Vault bootstrap from repository changes | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Notifications controller Pod readiness evidence | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Credential sync evidence from the ExternalSecret Ready state | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Human-approved live receipt evidence for sync failure notifications | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Human-approved live receipt evidence for health degraded notifications | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — [Acceptance criterion 05](../../01.requirements/0002-argo-notifications-slack.md) remains package-owned | Human-approved live receipt evidence for Rollouts abort notifications | [ADR 0012](../decisions/0012-argo-notifications-slack.md) and [Spec 005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |

- **PRD**: [`../../01.requirements/0002-argo-notifications-slack.md`](../../01.requirements/0002-argo-notifications-slack.md)
- **Spec**: [`../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md`](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md)
- **Plan**: [`../../98.archive/completed/03.specs/0005-argo-notifications-slack/plan.md`](../../98.archive/completed/03.specs/0005-argo-notifications-slack/plan.md)
- **ADR**: [`../decisions/0012-argo-notifications-slack.md`](../decisions/0012-argo-notifications-slack.md)
