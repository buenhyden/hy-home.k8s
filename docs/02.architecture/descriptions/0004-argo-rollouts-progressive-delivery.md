---
title: "Argo Rollouts Progressive Delivery Architecture Description"
version: "1.1.0"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-11-05"
layer: "architecture"
artifact_id: "AD-0004"
---

# Argo Rollouts Progressive Delivery Architecture Description

## Overview

This document defines the reference architecture and quality attributes of progressive delivery based on Argo Rollouts.
The GitOps resources already exist in the repository, so this AD is not a future implementation plan but a backfill that turns the repo-backed execution contract into traceable architecture input.

### Current architecture summary

Argo Rollouts provides the controller and dashboard in the `argo-rollouts` namespace and lets application teams run progressive delivery by combining `Rollout`, `AnalysisTemplate`, Istio routing, Traefik, and cert-manager TLS.
The platform owns the controller install, dashboard access, AppProject permissions, observability exposure, and a default that imposes no promotion mode, with failure safety through an approved `AnalysisTemplate`.

## Boundaries & Non-goals

- **Owns**:
  - The Argo Rollouts Helm chart deployment boundary
  - The `argo-rollouts` namespace and the controller/dashboard runtime boundary
  - The AppProject allow-list and the boundary for using Rollouts in the `apps` namespaces
  - The Rollouts Dashboard access path `rollouts.hy-k8s.home.arpa`
  - Controller metrics endpoint that in-cluster Alloy scrapes and remote-writes to the external Prometheus
- **Consumes**:
  - ArgoCD App-of-Apps reconciliation
  - Traefik and the cert-manager `mkcert-ca-issuer`
  - The external Prometheus and observability stack (analysis queries use `https://prometheus.hy.home.arpa`, [ADR-0046](../decisions/0046-external-services-over-host-addresses.md))
  - Per-application Rollout manifests
- **Does Not Own**:
  - Choosing an individual application's delivery strategy
  - Application image build and release policy
  - Slack notification templates and credential management
- **Non-goals**:
  - Forcing automatic promotion by default (the platform imposes no promotion mode; see [REQ-0001-IF-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md))
  - Multi-cluster Rollouts
  - Standardizing per-app Analysis metrics

## Quality Attributes

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| Performance | The controller and dashboard start | Single-host k3d cluster | Requests and limits stay pinned | Both Deployments declare requests and limits in the chart values |
| Security | An app Application requests Rollouts CRDs or a namespace | AppProject `platform` and `apps` | Only allow-listed kinds, repo and namespaces reconcile | A resource outside the allow-list is rejected by ArgoCD |
| Reliability | The `platform-rollouts` source drifts or a sync fails | ArgoCD reconciliation | Retry and self-heal restore the declared state | The Application returns to Synced and Healthy |
| Scalability | More apps adopt Rollouts | Shared controller, per-app Rollouts in `apps` namespaces | Per-app scaling stays in the workload contract | No controller change per adopting app |
| Observability | An operator inspects controller metrics | In-cluster Alloy scraping `argo-rollouts:8090` with remote-write to the external Prometheus | Controller metrics reach the external Prometheus | The controller target is up in Prometheus |
| Operability | An operator checks progress, promotion, abort or rollback | Dashboard, CLI and runbook | The path is available without platform changes | Each path is listed in the runbook checks |

## System Overview & Context

- Platform root app includes `gitops/apps/root/platform-rollouts-app.yaml`.
- The chart source and exact revision are owned by the [Rollouts Application](../../../gitops/apps/root/platform-rollouts-app.yaml); this AD does not maintain a second version pin.
- The controller and dashboard run in `argo-rollouts`.
- Dashboard traffic uses Traefik TLS behind the dedicated k8s router for browser access ([ADR-0043](../decisions/0043-dedicated-k8s-ingress-router.md)).
- Application teams consume the CRDs through workload manifests, for example `gitops/workloads/adminer/rollout.yaml`.

## Data Architecture

- **Key Entities / Flows**:
  - `Rollout`: application deployment state machine.
  - `AnalysisTemplate` / `AnalysisRun`: application-level metrics-driven safety checks; the current app onboarding pattern requires an `AnalysisTemplate` during canary rollout steps.
  - `Service` stable/canary pair: traffic targets for rollout steps.
  - `VirtualService` / `DestinationRule`: Istio routing for mesh-aware workloads.
- **Storage Strategy**:
  - Rollouts state is Kubernetes API state. No separate database is introduced.
  - Controller metrics are scraped in-cluster by Alloy ([ADR-0045](../decisions/0045-in-cluster-telemetry-collection.md)) and remote-written to the external Prometheus; no metrics NodePort remains.
- **Data Boundaries**:
  - No credentials are introduced by Rollouts itself; the reference analysis consumes the ESO-synced `prometheus-api-auth` Secret and the `hy-home-root-ca` ConfigMap from the app namespace.

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
- **Memory & Context Strategy**: durable change evidence stays in Git history and the owning Requirement's Archived Lineage, and common policy refers to `.agents/governance/`.
- **Guardrail Boundary**: Rollouts chart notifications stay disabled (`notifications.enabled: false`); notifications are ArgoCD Notifications, owned by [AD-0005](./0005-argo-notifications-slack.md).
- **Latency / Cost Budget**: Not applicable.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0001-FR-0001](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The GitOps-owned install boundary of the shared controller and dashboard | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-FR-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The Dashboard TLS boundary through the Traefik ingress controller ([ADR-0050](../decisions/0050-ingress-nginx-replacement-with-traefik.md)) and cert-manager | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-FR-0003](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The external Prometheus observability boundary of controller metrics | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-IF-0001](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The AppProject allow-list and ArgoCD health tracking boundary | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-IF-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | A default that imposes no promotion mode, and failure safety through an approved AnalysisTemplate | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-IF-0003](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The route boundary between the k8s router and the cluster ingress | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | Operational evidence of controller Deployment availability | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | The live evidence boundary of the Dashboard HTTPS response and progress display | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | Reconciliation evidence of the ArgoCD Rollout health state | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | The validation boundary that separates repo-static gates from runtime checks | [ADR 0011](../decisions/0011-argo-rollouts-progressive-delivery.md) |

- **Requirement**: [`../../01.requirements/0001-argo-rollouts-progressive-delivery.md`](../../01.requirements/0001-argo-rollouts-progressive-delivery.md)
- **Spec**: N/A — SPEC-0004 left the tree; Git history recovers it ([REQ-0001 Archived Lineage](../../01.requirements/0001-argo-rollouts-progressive-delivery.md#archived-lineage))
- **ADR**: [`../decisions/0011-argo-rollouts-progressive-delivery.md`](../decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../decisions/0054-platform-decision-current-state-amendment.md`](../decisions/0054-platform-decision-current-state-amendment.md) — current promotion-mode clause
