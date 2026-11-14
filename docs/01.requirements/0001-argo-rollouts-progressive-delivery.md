---
title: "Argo Rollouts Progressive Delivery Requirement Package"
version: "2.0.0"
type: "sdlc/requirement"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "REQ-0001"
---

# Argo Rollouts Progressive Delivery Requirement Package

## Overview

### Problem and Outcome

This document defines the product requirements for introducing Argo Rollouts to the `hy-home.k8s` platform: canary/blue-green progressive delivery, deployment safety checks based on observed metrics, and automatic abort/rollback on failure.

Give platform engineers and application teams a standard GitOps delivery strategy for releasing new versions progressively while minimizing deployment risk.

With only ArgoCD's default `Deployment`-based delivery, a defective release reaches the platform with immediate service impact. Deployment safety must improve through progressive delivery (canary, blue-green), a platform default that never forces automatic promotion, and abort/rollback driven by metric-based deployment safety checks.

#### Current requirement status

This package is backfilled against the current contract; the operator approved it on 2026-11-05 as current requirement authority.
The repository already declares the Rollouts controller and Dashboard, the AppProject scope, and one reference workload (`apps/adminer`) that uses a canary `Rollout` with a metric-based safety check; the operations runbook exists.
SPEC-0004 completed the trace chain on 2026-05-18, and its package later left the tree under SPEC-0140 (see Archived Lineage).
This document owns product intent and acceptance criteria; the linked downstream documents own the implementable contracts.

### Stakeholders

- **Platform Engineer**: wants to manage the Rollouts controller through GitOps and see rollout state visually in the dashboard UI.
- **Application Team**: wants to convert a `Deployment` into a `Rollout` resource and apply a canary/blue-green strategy.
- **DevOps Engineer**: wants deployment stability guaranteed by metric-based safety checks and an automatic rollback boundary on failure.

## Scope

### In Scope

- **STORY-01**: An operator checks the current rollout state and progress in real time in the Rollouts Dashboard UI (the approved Dashboard local path).
- **STORY-02**: An application team defines a canary deployment with a `Rollout` resource and chooses how it advances: an explicit manual promotion, or timed steps that proceed only while an approved safety check passes.
- **STORY-03**: When an approved observed metric leaves its safety threshold, the deployment safety check aborts the deployment automatically.
- **STORY-04**: ArgoCD recognizes `Rollout` resources and tracks their sync state correctly.

- **In Scope**:
  - Requirements to provide the Argo Rollouts controller and the Rollouts Dashboard
  - Permission and scope requirements for ArgoCD to track Rollouts resources
  - Requirements for deployment safety checks based on observed metrics
  - Requirements for access through the standard local route
  - Synchronization of the document chain

### Constraints and Exclusions

- **Out of Scope**:
  - Converting an individual application's `Deployment` to a `Rollout` (owned by the application team)
  - Multi-cluster Rollouts
- **Non-goals**:
  - Forcing automatic promotion platform-wide (each application chooses manual promotion or check-gated timed steps)
  - Standardizing custom Analysis metrics platform-wide

- A missed AppProject allow-list update makes ArgoCD sync fail.
  - **Mitigation**: the follow-on Spec/Plan states the AppProject change and its validation order.
- Rollouts Dashboard access depends on the `rollouts.hy-k8s.home.arpa` contract of the dedicated k8s router (ADR-0043).
- Metric-based safety checks depend on the external Prometheus reached over its host address with the local gateway CA trusted by the controller (ADR-0046); if it is unreachable, the analysis errors out instead of passing.
- Readiness of the approved local certificate and the ingress boundary is confirmed by the current platform requirements and the downstream implementation and operations owners.

#### Agent execution and approval requirements

- **Allowed Actions**: Update the Requirement Package and documentation, run non-destructive static validation, and collect read-only status evidence.
- **Disallowed Actions**: Expand AppProject permissions without approval, mutate the live cluster directly, or change manifests outside an approved downstream stage.
- **Human-in-the-loop Requirement**: Required before AppProject cluster resource allow-list changes or rollout promotion policy changes.
- **Evaluation Expectation**: Verify controller status, Dashboard access, and ArgoCD sync traceability in a downstream validation stage.

The linked AD/Spec/operations owners own the concrete manifests, hostnames, annotations, resource state, and validation commands.
This update does not claim to have observed runtime state or received live notifications.

## Requirements

### Functional Requirements

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0001-FR-0001 | The platform must provide progressive delivery within the standard GitOps flow. The ADR/Spec owns the implementing product and chart/version. | Serves the GitOps-owned install boundary of the shared controller and dashboard (AD-0004 Lifecycle Traceability). | Acceptance criterion 01: the controller is available and reconciled from Git. | Must |
| REQ-0001-FR-0002 | The Rollouts Dashboard UI must be exposed on the approved local TLS path. | Serves the Dashboard TLS boundary through the Traefik ingress controller (ADR-0050) and cert-manager (AD-0004 Lifecycle Traceability). | Acceptance criterion 02: HTTPS access to the Dashboard path succeeds. | Must |
| REQ-0001-FR-0003 | Controller metrics must be collectable so operators can observe rollout state and failure signals. | Serves the external Prometheus observability boundary of controller metrics (AD-0004 Lifecycle Traceability). | Static validation shows the metrics exposure and scrape contract. | Must |
| REQ-0001-IF-0001 | The platform must be able to track the sync and health state of progressive deliveries in the GitOps state model. The downstream Spec owns the concrete resources and permissions. | Serves the AppProject allow-list and ArgoCD health tracking boundary (AD-0004 Lifecycle Traceability). | Acceptance criterion 03: ArgoCD reports the `Rollout` health. | Must |
| REQ-0001-IF-0002 | The default promotion policy must not force automatic promotion, and a per-application deployment must be able to abort/rollback automatically on failure through an approved safety check. | Serves a default that imposes no promotion mode, and failure safety through an approved AnalysisTemplate (AD-0004 Lifecycle Traceability). | The platform imposes no promotion mode, and a failing safety check aborts the reference Rollout and returns traffic to the stable version. | Must |
| REQ-0001-IF-0003 | Access to the approved Dashboard local path must be provided through the standard local route. | Serves the route boundary between the k8s router and the cluster ingress (AD-0004 Lifecycle Traceability). | The shared local entry point forwards its Rollouts path to the Dashboard host, distinct from the direct TLS access of FR-0002. | Must |

## Acceptance Criteria

### Acceptance Conditions

- **Acceptance criterion 01**: An operator can check the Rollouts controller state. Evidence: the Rollouts controller Deployment (`argo-rollouts`) is `Available=True`.
- **Acceptance criterion 02**: An operator can see rollout progress in the Dashboard. Evidence: HTTPS access to the approved Dashboard local path succeeds.
- **Acceptance criterion 03**: An application team can track Rollout resources in the ArgoCD state model. Evidence: ArgoCD shows the `Rollout` resource as `Healthy` or `Progressing`.
- **Acceptance criterion 04**: CI blocks static contract regressions related to Rollouts. Evidence: the repo quality gate and static contract validation PASS.

### Verification Method

No separate verification method is stated: each requirement is verified by the evidence named in its `Acceptance` cell, and the acceptance-criterion column of `Lifecycle Traceability` states the acceptance condition of every member.

## Traceability

### Source and Constraints

- **Requirement**: [`./0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md) — cert-manager dependency

### Downstream Links

- **AD**: [`../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md`](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md)
- **Spec**: N/A — SPEC-0004 left the tree; Git history recovers it ([REQ-0001 Archived Lineage](./0001-argo-rollouts-progressive-delivery.md#archived-lineage))
- **ADR**: [`../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0001-FR-0001 | GitOps static validation passes the `platform-rollouts` install contract, and an operator can confirm controller availability. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| REQ-0001-FR-0002 | Dashboard progress is visible over HTTPS on the approved Dashboard local path. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| REQ-0001-FR-0003 | The controller state and metrics exposure contract are observable in static validation and operational checks. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| REQ-0001-IF-0001 | ArgoCD can track a `Rollout` as `Healthy` or `Progressing`. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| REQ-0001-IF-0002 | A per-application deployment using an approved safety check keeps the abort/rollback boundary on failure signals and does not force automatic promotion. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| REQ-0001-IF-0003 | The shared local entry point's Rollouts path reaches the Dashboard host. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | An operator can confirm that the Rollouts controller Deployment (`argo-rollouts`) is `Available=True`. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | HTTPS access to the approved Dashboard local path succeeds and the Dashboard shows progress. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | ArgoCD shows the reference Rollout resource as `Healthy` or `Progressing`. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | The repository quality gate and the Rollouts static contract validation PASS. | [AD 0004](../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md) |

### Archived Lineage

These documents were deleted from `docs/98.archive/` under SPEC-0140 and are recovered with `git show 69445fca:<path>`. Paths below are the archive paths at that commit; a completed Spec path is its package directory (`spec.md`, `plan.md`, `tasks/`).

| Source | Kind | Summary | Original path |
| --- | --- | --- | --- |
| SPEC-0004 | completed spec | Defined the repo-backed contract for Argo Rollouts progressive delivery: the `platform-rollouts` Application, AppProject permissions, dashboard route, metrics, and workload consumption boundaries. Completed; the repo-backed implementation was done, while live promote, abort and undo stayed operator-approved runtime validation. | `docs/98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/` |
