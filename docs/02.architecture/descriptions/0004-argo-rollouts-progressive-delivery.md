---
title: "Argo Rollouts Progressive Delivery Architecture Description"
version: "1.0.4"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "AD-0004"
---

# Argo Rollouts Progressive Delivery Architecture Description

## Overview

This document defines the reference architecture and quality attributes of progressive delivery based on Argo Rollouts.
The GitOps resources already exist in the repository, so this AD is not a future implementation plan but a backfill that turns the repo-backed execution contract into traceable architecture input.

### Current architecture summary

Argo Rollouts provides the controller and dashboard in the `argo-rollouts` namespace and lets application teams run progressive delivery by combining `Rollout`, `AnalysisTemplate`, Istio routing, ingress-nginx, and cert-manager TLS.
The platform owns the controller install, dashboard access, AppProject permissions, observability exposure, and the safe manual promotion boundary.

## Boundaries & Non-goals

- **Owns**:
  - The Argo Rollouts Helm chart deployment boundary
  - The `argo-rollouts` namespace and the controller/dashboard runtime boundary
  - The AppProject allow-list and the boundary for using Rollouts in the `apps` namespaces
  - The Rollouts Dashboard access path `rollouts.hy-k8s.home.arpa`
  - Exposing controller metrics for Prometheus to collect
- **Consumes**:
  - ArgoCD App-of-Apps reconciliation
  - ingress-nginx and the cert-manager `mkcert-ca-issuer`
  - The external Prometheus and observability stack
  - Per-application Rollout manifests
- **Does Not Own**:
  - Choosing an individual application's delivery strategy
  - Application image build and release policy
  - Slack notification templates and credential management
- **Non-goals**:
  - Forcing automatic promotion by default
  - Multi-cluster Rollouts
  - Standardizing per-app Analysis metrics

## Quality Attributes

- **Performance**: the controller and dashboard pin their requests/limits so they run within the single-host k3d resource budget.
- **Security**: Rollouts CRDs and namespace permissions are limited by the AppProject allow-list.
- **Reliability**: the `platform-rollouts` Application owns the GitOps source and uses retries and self-heal.
- **Scalability**: the controller stays shared across the platform, and per-app rollout scaling is separated into the workload contract of the `apps` namespaces.
- **Observability**: controller metrics are exposed through a NodePort and the Prometheus scrape contract.
- **Operability**: the dashboard, CLI, and runbook checks confirm the progress, promotion, abort, and rollback paths.

## System Overview & Context

- Platform root app includes `gitops/apps/root/platform-rollouts-app.yaml`.
- The chart source and exact revision are owned by the [Rollouts Application](../../../gitops/apps/root/platform-rollouts-app.yaml); this AD does not maintain a second version pin.
- The controller and dashboard run in `argo-rollouts`.
- Dashboard traffic uses ingress-nginx TLS behind the dedicated k8s router for browser access ([ADR-0043](../decisions/0043-dedicated-k8s-ingress-router.md)).
- Application teams consume the CRDs through workload manifests, for example `gitops/workloads/adminer/rollout.yaml`.

## Data Architecture

- **Key Entities / Flows**:
  - `Rollout`: application deployment state machine.
  - `AnalysisTemplate` / `AnalysisRun`: application-level metrics-driven safety checks; the current app onboarding pattern requires an `AnalysisTemplate` during canary rollout steps.
  - `Service` stable/canary pair: traffic targets for rollout steps.
  - `VirtualService` / `DestinationRule`: Istio routing for mesh-aware workloads.
- **Storage Strategy**:
  - Rollouts state is Kubernetes API state. No separate database is introduced.
  - Controller metrics are exposed for external Prometheus scraping.
- **Data Boundaries**:
  - No credentials are introduced by Rollouts itself.
  - Notifications are intentionally handled by ArgoCD Notifications, not Rollouts chart notifications.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Linux server + k3d/k3s local platform managed by ArgoCD.
  - Namespace: `argo-rollouts`.
  - Dashboard host: `rollouts.hy-k8s.home.arpa`.
- **Deployment Model**:
  - `platform-rollouts` ArgoCD Application installs the Helm chart.
  - `gitops/apps/root/kustomization.yaml` includes the Application.
  - AppProject `platform` allows the chart repo and destination namespace.
  - AppProject `apps` allows application workloads to use Rollout and Analysis resources.
- **Operational Evidence**:
  - Static GitOps checks validate application and kustomization structure.
  - Manifest checks validate YAML syntax.
  - Runtime checks are deferred to the runbook when a live cluster is intentionally available.

### Agent architecture requirements

- **Model/Provider Strategy**: Agents may update docs and manifests only through repo-backed GitOps flow.
- **Tooling Boundary**: Direct `kubectl apply` or live promotion is not allowed without explicit human approval.
- **Memory & Context Strategy**: durable change evidence stays in the package-local Task, and common policy refers to `.agents/governance/`.
- **Guardrail Boundary**: Agents must distinguish Rollouts chart `notifications.enabled: false` from ArgoCD Notifications.
- **Latency / Cost Budget**: Not applicable.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0001-FR-0001](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The GitOps-owned install boundary of the shared controller and dashboard | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| [REQ-0001-FR-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The Dashboard TLS boundary through ingress-nginx and cert-manager | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| [REQ-0001-FR-0003](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The external Prometheus observability boundary of controller metrics | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| [REQ-0001-IF-0001](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The AppProject allow-list and ArgoCD health tracking boundary | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| [REQ-0001-IF-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The manual promotion default and failure safety through an approved AnalysisTemplate | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| [REQ-0001-IF-0003](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The route boundary between the k8s router and the cluster ingress | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | Operational evidence of controller Deployment availability | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | The live evidence boundary of the Dashboard HTTPS response and progress display | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | Reconciliation evidence of the ArgoCD Rollout health state | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | The validation boundary that separates repo-static gates from runtime checks | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) and [Spec 004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |

- **PRD**: [`../../01.requirements/0001-argo-rollouts-progressive-delivery.md`](../../01.requirements/0001-argo-rollouts-progressive-delivery.md)
- **Spec**: [`../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md`](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md)
- **Plan**: [`../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/plan.md`](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/plan.md)
- **ADR**: [`../decisions/0011-argo-rollouts-progressive-delivery.md`](../decisions/0011-argo-rollouts-progressive-delivery.md)
