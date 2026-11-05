---
title: "Argo Notifications Slack Requirement Package"
version: "1.2.1"
type: "sdlc/requirement"
status: "approved"
owner: "platform"
updated: "2026-11-05"
layer: "requirements"
artifact_id: "REQ-0002"
---

# Argo Notifications Slack Requirement Package

## Overview

This document defines the product requirements for enabling the ArgoCD Notifications controller and using a Slack channel, reached with a Slack app token, as the notification destination, so GitOps events (sync failure, health degradation, deployment completion) and Rollouts events (completion, abort) reach operators automatically.

### Current requirement status

This package is backfilled against the current contract; the operator approved it on 2026-11-05 as current requirement authority.
The ArgoCD Notifications values, ConfigMap, ExternalSecret, and operations documents already exist in the repository; SPEC-0005 completed the trace chain on 2026-05-18, and its package later left the tree under SPEC-0140 (see Archived Lineage).
The credential comes from the OpenBao runtime secret backend (ADR-0041) through ESO.
Rollouts completion and abort events are delivered by the Argo Rollouts controller's own notification engine, because the ArgoCD Notifications controller evaluates Applications only ([SPEC-0141](../03.specs/0141-rollouts-notification-delivery/spec.md), ADR-0054). Acceptance criterion 05 needs the operator's live observation.
This document owns the user value and security boundary of notifications; the linked downstream documents and operations runbooks own the Secret creation procedure and the manifest contract.

## Vision

Platform events (ArgoCD sync failure, service health degradation, Rollouts completion/abort) reach operators in Slack automatically, so they can respond quickly without manual monitoring.

## Problem Statement

The repository has notification settings, but their presence alone does not guarantee that events are delivered and actually received. Acceptance criteria for the common failure signals and the optional deployment notifications must be kept so operators do not depend on checking the UI by hand.

## Personas

- **Platform Engineer**: wants to receive ArgoCD and Rollouts events in a Slack channel in real time.
- **DevOps Engineer**: wants an immediate notification on sync failure or health degradation to respond quickly.
- **Application Team**: wants deployment completion (on-deployed) events, delivered on the default channel, and optionally on an additional channel of its own.

## Key Use Cases

- **STORY-01**: When an ArgoCD app fails to sync, a notification goes to the operators' Slack channel immediately.
- **STORY-02**: When an app's health degrades (Degraded), a notification goes to the operators' Slack channel immediately.
- **STORY-03**: When an Argo Rollouts deployment completes or aborts, a Slack notification is sent.
- **STORY-04**: Deployment completion reaches the default channel for every app, and an application team can add its own channel through per-app settings.

## Functional Requirements

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-0002-FR-0001 | The platform must deliver GitOps events to the operators' Slack channel. The downstream Spec owns the controller and the concrete settings. | Must | Acceptance criteria 01, 03 and 04. |
| REQ-0002-FR-0002 | Slack credential material must be consumed only through an approved external secret source and a bounded sync boundary, and must not appear in plaintext in the Requirement Package, manifests, or logs. | Must | Acceptance criterion 02, and secret scanning finds no token in Git. |
| REQ-0002-FR-0003 | Notification templates and triggers must express deployment completion, health degradation, sync failure, Rollouts completion, and Rollouts abort events. | Must | The templates and triggers are declared; Rollouts delivery is proven only by acceptance criterion 05. |
| REQ-0002-NFR-0001 | The common default notification policy must apply health degradation and sync failure to every app. Deployment completion may be part of the same default. The presence of the current settings does not prove an all-app subscription or actual receipt. | Must | The default subscription names both triggers; receipt is proven by acceptance criteria 03 and 04. |
| REQ-0002-IF-0001 | An application team must be able to subscribe per app to an additional Slack channel for deployment completion notifications. The AD/Spec owns the native annotation syntax. | Must | A per-app subscription can be declared without changing the platform default. |
| REQ-0002-IF-0002 | Notification credential bootstrap must be performed only as a human-approved external task. | Must | No repository change or agent action writes the credential to the secret backend. |

## Success / Acceptance Criteria

- **Acceptance criterion 01**: An operator can check the Notifications controller state. Evidence: `argocd-notifications-controller` Pod `Running`.
- **Acceptance criterion 02**: An operator can check the sync state of the notification credential held in the runtime secret backend. Evidence: `argocd-notifications-secret` ExternalSecret `Ready=True`, synced from the OpenBao backend.
- **Acceptance criterion 03**: An operator can notice a sync failure in Slack. Evidence: receipt of a sync failure event in Slack is confirmed.
- **Acceptance criterion 04**: An operator can notice health degradation in Slack. Evidence: receipt of a health degraded event in Slack is confirmed.
- **Acceptance criterion 05**: An operator can notice a Rollouts abort in Slack. Evidence: receipt of a Rollouts abort event in Slack is confirmed. The Rollouts notification engine sends it to the shared channel; live receipt is not yet observed.

## Scope and Non-goals

- **In Scope**:
  - Requirement to enable the ArgoCD Notifications controller
  - OpenBao/ESO security boundary for the Slack credential
  - Notification template and trigger requirements
  - Default subscriptions on one shared channel (health degradation, sync failure, and deployment completion)
- **Out of Scope**:
  - Email/PagerDuty notification channels
  - Alertmanager integration
- **Non-goals**:
  - Automatic per-app notification channel routing (one shared channel is the default; extra channels are per-app opt-in)
  - Creating the Slack workspace or channels

## Risks, Dependencies, and Assumptions

- The notification credential must be prepared by a human-approved external bootstrap task.
- Issuing the Slack Bot token and granting channel permissions needs the cooperation of the Slack workspace administrator.
- Assumes ESO and the OpenBao backend are operating normally (depends on the current baseline Requirement and ADR-0041).
- rollout-\* events need Argo Rollouts (REQ-0001); the Rollouts notification engine reads the same OpenBao credential through its own ExternalSecret in `argo-rollouts`.

### Agent execution and approval requirements

- **Allowed Actions**: Update the Requirement Package and documentation, run non-destructive static validation, and collect read-only status evidence.
- **Disallowed Actions**: Store Slack credentials in plaintext, modify secret backend paths without approval, or change manifests outside an approved downstream stage.
- **Human-in-the-loop Requirement**: Required before initial notification credential registration or Slack channel permission changes.
- **Evaluation Expectation**: Verify controller status, ExternalSecret readiness, and Slack notification receipt in a downstream validation stage.

The linked AD/Spec/operations owners own the concrete manifests, hostnames, annotations, resource state, and validation commands.
This update does not claim to have observed runtime state or received live notifications.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0002-FR-0001 | The ArgoCD Notifications controller is enabled and an operator can check its Pod state. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| REQ-0002-FR-0002 | The Slack credential syncs from OpenBao through ESO, and no plaintext token appears in Git or logs. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| REQ-0002-FR-0003 | The ConfigMap defines templates and triggers for deployment, health, sync, Rollouts completion, and abort events. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| REQ-0002-NFR-0001 | Default subscriptions apply health degradation and sync failure notifications to every app. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| REQ-0002-IF-0001 | A per-app subscription to an additional Slack channel for deployment completion notifications can be declared. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| REQ-0002-IF-0002 | Notification credential bootstrap is performed only as a human-approved external task. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | An operator can confirm that the `argocd-notifications-controller` Pod is `Running`. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | The `argocd-notifications-secret` ExternalSecret can be confirmed as `Ready=True`. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | A deliberately triggered sync failure event arrives in the approved Slack channel. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | A health degraded event arrives in the approved Slack channel. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |
| N/A — Acceptance criterion 05 remains acceptance-only | A Rollouts abort event arrives in the approved Slack channel. | [AD 0005](../02.architecture/descriptions/0005-argo-notifications-slack.md) |

- **AD**: [`../02.architecture/descriptions/0005-argo-notifications-slack.md`](../02.architecture/descriptions/0005-argo-notifications-slack.md)
- **Spec**: [SPEC-0141](../03.specs/0141-rollouts-notification-delivery/spec.md) — Rollouts notification delivery (open)
- **Spec**: N/A — SPEC-0005 left the tree; Git history recovers it ([REQ-0002 Archived Lineage](./0002-argo-notifications-slack.md#archived-lineage))
- **ADR**: [`../02.architecture/decisions/0012-argo-notifications-slack.md`](../02.architecture/decisions/0012-argo-notifications-slack.md)
- **ADR**: [`../02.architecture/decisions/0041-openbao-secret-backend.md`](../02.architecture/decisions/0041-openbao-secret-backend.md)
- **Requirement**: [`./0001-argo-rollouts-progressive-delivery.md`](./0001-argo-rollouts-progressive-delivery.md) — Rollouts event source
- **Requirement**: [`./0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md) — ESO/OpenBao dependency

### Archived Lineage

These documents were deleted from `docs/98.archive/` under SPEC-0140 and are recovered with `git show 69445fca:<path>`. Paths below are the archive paths at that commit; a completed Spec path is its package directory (`spec.md`, `plan.md`, `tasks/`).

| Source | Kind | Summary | Original path |
| --- | --- | --- | --- |
| SPEC-0005 | completed spec | Defined the repo-backed contract for Slack notifications through ArgoCD Notifications: Helm values, Notifications ConfigMap, Vault-backed ExternalSecret, default subscriptions and per-application opt-in annotations. Completed against the static contract; Slack token bootstrap, Vault writes and live sends stayed human-approved runtime validation. | `docs/98.archive/completed/03.specs/0005-argo-notifications-slack/` |
