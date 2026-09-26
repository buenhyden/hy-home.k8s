---
title: "Argo Notifications Slack Webhook Requirement Package"
version: "1.0.2"
type: "sdlc/requirement"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "requirements"
artifact_id: "REQ-0002"
---

# Argo Notifications Slack Webhook Requirement Package

## Overview

This document defines the product requirements for enabling the ArgoCD Notifications controller and using a Slack webhook as the notification destination, so GitOps events (sync failure, health degradation, deployment completion) and Rollouts events (completion, abort) reach operators automatically.

### Current requirement status

This Requirement is an active document backfilled against the current contract.
The ArgoCD Notifications values, ConfigMap, ExternalSecret, and operations documents already exist in the repository; the AD/Spec/Plan/Task trace chain was completed on 2026-05-18.
This document owns the user value and security boundary of notifications; the linked downstream documents and operations runbooks own the Secret creation procedure and the manifest contract.

## Vision

Platform events (ArgoCD sync failure, service health degradation, Rollouts completion/abort) reach operators in Slack automatically, so they can respond quickly without manual monitoring.

## Problem Statement

The repository has notification settings, but their presence alone does not guarantee that events are delivered and actually received. Acceptance criteria for the common failure signals and the optional deployment notifications must be kept so operators do not depend on checking the UI by hand.

## Personas

- **Platform Engineer**: wants to receive ArgoCD and Rollouts events in a Slack channel in real time.
- **DevOps Engineer**: wants an immediate notification on sync failure or health degradation to respond quickly.
- **Application Team**: wants to opt in to deployment completion (on-deployed) events in a specific Slack channel.

## Key Use Cases

- **STORY-01**: When an ArgoCD app fails to sync, a notification goes to the operators' Slack channel immediately.
- **STORY-02**: When an app's health degrades (Degraded), a notification goes to the operators' Slack channel immediately.
- **STORY-03**: When an Argo Rollouts deployment completes or aborts, a Slack notification is sent.
- **STORY-04**: An application team opts in to deployment completion notifications for a specific channel through per-app settings.

## Functional Requirements

- **REQ-0002-FR-0001**: The platform must deliver GitOps events to the operators' Slack channel. The downstream Spec owns the controller and the concrete settings.
- **REQ-0002-FR-0002**: Slack credential material must be consumed only through an approved external secret source and a bounded sync boundary, and must never appear in plaintext in the PRD, manifests, or logs.
- **REQ-0002-FR-0003**: Notification templates and triggers must express deployment completion, health degradation, sync failure, Rollouts completion, and Rollouts abort events.
- **REQ-0002-NFR-0001**: The common default notification policy must apply health degradation and sync failure to every app. The presence of the current settings does not prove an all-app subscription or actual receipt.
- **REQ-0002-IF-0001**: An application team must be able to opt in per app to a Slack channel for deployment completion notifications. The AD/Spec owns the native annotation syntax.
- **REQ-0002-IF-0002**: Notification credential bootstrap must be performed only as a human-approved external task.

## Success / Acceptance Criteria

- **Acceptance criterion 01**: An operator can check the Notifications controller state. Evidence: `argocd-notifications-controller` Pod `Running`.
- **Acceptance criterion 02**: An operator can check the sync state of the Vault-backed notification credential. Evidence: `argocd-notifications-secret` ExternalSecret `Ready=True`.
- **Acceptance criterion 03**: An operator can notice a sync failure in Slack. Evidence: receipt of a sync failure event in Slack is confirmed.
- **Acceptance criterion 04**: An operator can notice health degradation in Slack. Evidence: receipt of a health degraded event in Slack is confirmed.
- **Acceptance criterion 05**: An operator can notice a Rollouts abort in Slack. Evidence: receipt of a Rollouts abort event in Slack is confirmed.

## Scope and Non-goals

- **In Scope**:
  - Requirement to enable the ArgoCD Notifications controller
  - Vault/ESO security boundary for the Slack credential
  - Notification template and trigger requirements
  - Default subscriptions settings
- **Out of Scope**:
  - Email/PagerDuty notification channels
  - Alertmanager integration
- **Non-goals**:
  - Automatic per-app notification channel routing (a single channel is the default)
  - Creating the Slack workspace or channels

## Risks, Dependencies, and Assumptions

- The notification credential must be prepared by a human-approved external bootstrap task.
- Issuing the Slack Bot token and granting channel permissions needs the cooperation of the Slack workspace administrator.
- Assumes ESO is operating normally (depends on the current baseline Requirement).
- rollout-\* events work only with Argo Rollouts installed (depends on PRD `0001-argo-rollouts-progressive-delivery.md`).

### Agent execution and approval requirements

- **Allowed Actions**: Update PRD/documentation, run non-destructive static validation, and collect read-only status evidence.
- **Disallowed Actions**: Store Slack credentials in plaintext, modify Vault paths without approval, or change manifests outside an approved downstream stage.
- **Human-in-the-loop Requirement**: Required before initial notification credential registration or Slack channel permission changes.
- **Evaluation Expectation**: Verify controller status, ExternalSecret readiness, and Slack notification receipt in a downstream validation stage.

The linked AD/Spec/operations owners own the concrete manifests, hostnames, annotations, resource state, and validation commands.
This update does not claim to have observed runtime state or received live notifications.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0002-FR-0001 | The ArgoCD Notifications controller is enabled and an operator can check its Pod state. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-FR-0002 | The Slack credential syncs from Vault through ESO, and no plaintext token appears in Git or logs. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-FR-0003 | The ConfigMap defines templates and triggers for deployment, health, sync, Rollouts completion, and abort events. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-NFR-0001 | Default subscriptions apply health degradation and sync failure notifications to every app. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-IF-0001 | A per-app Slack channel opt-in for deployment completion notifications can be declared. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| REQ-0002-IF-0002 | Notification credential bootstrap is performed only as a human-approved external task. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | An operator can confirm that the `argocd-notifications-controller` Pod is `Running`. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | The `argocd-notifications-secret` ExternalSecret can be confirmed as `Ready=True`. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | A deliberately triggered sync failure event arrives in the approved Slack channel. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | A health degraded event arrives in the approved Slack channel. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |
| N/A — Acceptance criterion 05 remains acceptance-only | A Rollouts abort event arrives in the approved Slack channel. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) and [Spec 005](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md) |

- **AD**: [`../02.architecture/descriptions/0005-argo-notifications-slack.md`](../02.architecture/descriptions/0005-argo-notifications-slack.md)
- **Spec**: [`../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md`](../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md)
- **Plan**: [`../98.archive/completed/03.specs/0005-argo-notifications-slack/plan.md`](../98.archive/completed/03.specs/0005-argo-notifications-slack/plan.md)
- **Task**: [Spec 0005 Plan](../98.archive/completed/03.specs/0005-argo-notifications-slack/plan.md)
- **ADR**: [`../02.architecture/decisions/0012-argo-notifications-slack.md`](../02.architecture/decisions/0012-argo-notifications-slack.md)
- **ADR**: [`../02.architecture/decisions/0041-openbao-secret-backend.md`](../02.architecture/decisions/0041-openbao-secret-backend.md)
- **Requirement**: [`./0001-argo-rollouts-progressive-delivery.md`](./0001-argo-rollouts-progressive-delivery.md) — Rollouts event source
- **Requirement**: [`./0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md) — ESO/Vault dependency
