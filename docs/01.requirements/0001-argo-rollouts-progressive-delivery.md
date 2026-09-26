---
title: "Argo Rollouts Progressive Delivery Requirement Package"
version: "1.0.2"
type: "sdlc/requirement"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "requirements"
artifact_id: "REQ-0001"
---

# Argo Rollouts Progressive Delivery Requirement Package

## Overview

This document defines the product requirements for introducing Argo Rollouts to the `hy-home.k8s` platform: canary/blue-green progressive delivery, deployment safety checks based on observed metrics, and automatic abort/rollback on failure.

### Current requirement status

This Requirement is an active document backfilled against the current contract.
The Rollouts GitOps resources and operations documents already exist in the repository; the AD/Spec/Plan/Task trace chain was completed on 2026-05-18.
This document owns product intent and acceptance criteria; the linked downstream documents own the implementable contracts.

## Vision

Give platform engineers and application teams a standard GitOps delivery strategy for releasing new versions progressively while minimizing deployment risk.

## Problem Statement

With only ArgoCD's default `Deployment`-based delivery, a defective release reaches the platform with immediate service impact. Deployment safety must improve through progressive delivery (canary, blue-green), a manual promotion default, and abort/rollback driven by metric-based deployment safety checks.

## Personas

- **Platform Engineer**: wants to manage the Rollouts controller through GitOps and see rollout state visually in the dashboard UI.
- **Application Team**: wants to convert a `Deployment` into a `Rollout` resource and apply a canary/blue-green strategy.
- **DevOps Engineer**: wants deployment stability guaranteed by metric-based safety checks and an automatic rollback boundary on failure.

## Key Use Cases

- **STORY-01**: An operator checks the current rollout state and progress in real time in the Rollouts Dashboard UI (the approved Dashboard local path).
- **STORY-02**: An application team defines a canary deployment with a `Rollout` resource and promotes it safely through manual approval.
- **STORY-03**: When an approved observed metric leaves its safety threshold, the deployment safety check aborts the deployment automatically.
- **STORY-04**: ArgoCD recognizes `Rollout` resources and tracks their sync state correctly.

## Functional Requirements

- **REQ-0001-FR-0001**: The platform must provide progressive delivery within the standard GitOps flow. The ADR/Spec owns the implementing product and chart/version.
- **REQ-0001-FR-0002**: The Rollouts Dashboard UI must be exposed on the approved local TLS path.
- **REQ-0001-FR-0003**: Controller metrics must be collectable so operators can observe rollout state and failure signals.
- **REQ-0001-IF-0001**: The platform must be able to track the sync and health state of progressive deliveries in the GitOps state model. The downstream Spec owns the concrete resources and permissions.
- **REQ-0001-IF-0002**: The default promotion policy must not force automatic promotion, and a per-application deployment must be able to abort/rollback automatically on failure through an approved safety check.
- **REQ-0001-IF-0003**: Access to the approved Dashboard local path must be provided through the standard local route.

## Success / Acceptance Criteria

- **Acceptance criterion 01**: An operator can check the Rollouts controller state. Evidence: `argo-rollouts-controller` Deployment `Available=True`.
- **Acceptance criterion 02**: An operator can see rollout progress in the Dashboard. Evidence: HTTPS access to the approved Dashboard local path succeeds.
- **Acceptance criterion 03**: An application team can track Rollout resources in the ArgoCD state model. Evidence: ArgoCD shows the `Rollout` resource as `Healthy` or `Progressing`.
- **Acceptance criterion 04**: CI blocks static contract regressions related to Rollouts. Evidence: the repo quality gate and static contract validation PASS.

## Scope and Non-goals

- **In Scope**:
  - Requirements to provide the Argo Rollouts controller and the Rollouts Dashboard
  - Permission and scope requirements for ArgoCD to track Rollouts resources
  - Requirements for deployment safety checks based on observed metrics
  - Requirements for access through the standard local route
  - Synchronization of the document chain
- **Out of Scope**:
  - Converting an individual application's `Deployment` to a `Rollout` (owned by the application team)
  - Multi-cluster Rollouts
- **Non-goals**:
  - Forcing automatic promotion (manual approval is the default)
  - Standardizing custom Analysis metrics platform-wide

## Risks, Dependencies, and Assumptions

- A missed AppProject allow-list update makes ArgoCD sync fail.
  - **Mitigation**: the follow-on Spec/Plan states the AppProject change and its validation order.
- Rollouts Dashboard access depends on the `rollouts.hy-k8s.home.arpa` contract of the dedicated k8s router (ADR-0043).
- Readiness of the approved local certificate and the ingress boundary is confirmed by the current platform requirements and the downstream implementation and operations owners.

### Agent execution and approval requirements

- **Allowed Actions**: Update PRD/documentation, run non-destructive static validation, and collect read-only status evidence.
- **Disallowed Actions**: Expand AppProject permissions without approval, mutate the live cluster directly, or change manifests outside an approved downstream stage.
- **Human-in-the-loop Requirement**: Required before AppProject cluster resource allow-list changes or rollout promotion policy changes.
- **Evaluation Expectation**: Verify controller status, Dashboard access, and ArgoCD sync traceability in a downstream validation stage.

The linked AD/Spec/operations owners own the concrete manifests, hostnames, annotations, resource state, and validation commands.
This update does not claim to have observed runtime state or received live notifications.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0001-FR-0001 | GitOps static validation passes the `platform-rollouts` install contract, and an operator can confirm controller availability. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| REQ-0001-FR-0002 | Dashboard progress is visible over HTTPS on the approved Dashboard local path. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| REQ-0001-FR-0003 | The controller state and metrics exposure contract are observable in static validation and operational checks. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| REQ-0001-IF-0001 | ArgoCD can track a `Rollout` as `Healthy` or `Progressing`. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| REQ-0001-IF-0002 | A per-application deployment using an approved safety check keeps the abort/rollback boundary on failure signals and does not force automatic promotion. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| REQ-0001-IF-0003 | The standard local route matches the Dashboard HTTPS access contract. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | An operator can confirm that the `argo-rollouts-controller` Deployment is `Available=True`. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | HTTPS access to the approved Dashboard local path succeeds and the Dashboard shows progress. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | ArgoCD shows the reference Rollout resource as `Healthy` or `Progressing`. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | The repository quality gate and the Rollouts static contract validation PASS. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) and [Spec 004](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |

- **AD**: [`../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md`](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md)
- **Spec**: [`../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md`](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md)
- **Plan**: [`../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/plan.md`](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/plan.md)
- **Task**: [Spec 0004 Plan](../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/plan.md)
- **ADR**: [`../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)
- **Requirement**: [`./0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md) — cert-manager dependency
