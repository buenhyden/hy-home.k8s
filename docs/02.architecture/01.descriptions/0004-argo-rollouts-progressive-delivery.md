---
title: "Argo Rollouts Progressive Delivery Architecture Description"
version: "3.0.0"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-11-20"
artifact_id: "AD-0004"
---

# Argo Rollouts Progressive Delivery Architecture Description

## 문서 개요

### 목적과 독자

This architecture description lets architects, GitOps implementers, and reviewers inspect the structural boundary for Argo Rollouts Progressive Delivery. The actual components and flow are under [Structure](#structure) and [Runtime Behavior](#runtime-behavior).

### 책임과 적용 범위

platform maintains the current architecture description. The owned and excluded system boundary is stated in [System Boundary](#system-boundary); constraints remain in [Constraints](#constraints).

## 내용 계약

### 입력과 전제

Inputs and assumptions remain in the cited upstream requirements, boundaries, and payload sections.

### 본문과 규칙

#### Context and Boundaries

##### System Boundary

- **Owns**:
  - The Argo Rollouts Helm chart deployment boundary
  - The `argo-rollouts` namespace and the controller/dashboard runtime boundary
  - The AppProject allow-list and the boundary for using Rollouts in the `apps` namespaces
  - The Rollouts Dashboard access path `rollouts.hy-k8s.home.arpa`
  - Controller metrics endpoint that in-cluster Alloy scrapes and remote-writes to the external Prometheus
- **Does Not Own**:
  - Choosing an individual application's delivery strategy
  - Application image build and release policy
  - Slack notification templates and credential management
- **Non-goals**:
  - Forcing automatic promotion by default (the platform imposes no promotion mode; see [REQ-0001-IF-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md))
  - Multi-cluster Rollouts
  - Standardizing per-app Analysis metrics

###### Purpose and Readers

This document defines the reference architecture and quality attributes of progressive delivery based on Argo Rollouts.
It describes the current GitOps declarations and traces them to the platform requirements. The operational verification scope is recorded under [Normal Flow](#normal-flow).

<a id="current-architecture-summary"></a>

**Current architecture summary**

GitOps declares the Argo Rollouts controller and dashboard in the `argo-rollouts` namespace. The designed workload path combines `Rollout`, `AnalysisTemplate`, Istio routing, Traefik, and cert-manager TLS.
The platform owns the controller install, dashboard access, AppProject permissions, observability exposure, and a default that imposes no promotion mode, with failure safety through an approved `AnalysisTemplate`.

###### Context

- **Consumes**:
  - ArgoCD App-of-Apps reconciliation
  - Traefik and the cert-manager `mkcert-ca-issuer`
  - The external Prometheus and observability stack (analysis queries use `https://prometheus.hy.home.arpa`, [ADR-0046](../02.decisions/0046-external-services-over-host-addresses.md))
  - Per-application Rollout manifests

##### Constraints

###### Agent architecture requirements

- **Model/Provider Strategy**: Agents may update docs and manifests only through repo-backed GitOps flow.
- **Tooling Boundary**: Direct `kubectl apply` or live promotion is not allowed without explicit human approval.
- **Memory & Context Strategy**: durable change evidence stays in Git history and the owning Requirement's Archived Lineage, and common policy refers to `.agents/governance/`.
- **Guardrail Boundary**: the Rollouts controller sends only its completion and abort events to the shared Slack channel; the notification architecture is owned by [AD-0005](./0005-argo-notifications-slack.md).
- **Latency / Cost Budget**: Not applicable.

#### Structure

##### Building Blocks

- Platform root app includes `gitops/apps/root/platform-rollouts-app.yaml`.
- The chart source and exact revision are owned by the [Rollouts Application](../../../gitops/apps/root/platform-rollouts-app.yaml); this AD does not maintain a second version pin.
- The Application targets `argo-rollouts` for the controller and dashboard.
- The declared dashboard route uses Traefik TLS behind the dedicated k8s router for browser access ([ADR-0043](../02.decisions/0043-dedicated-k8s-ingress-router.md)).
- Application teams consume the CRDs through workload manifests, for example `gitops/workloads/adminer/rollout.yaml`.

##### Interfaces

- **Key Entities / Flows**:
  - `Rollout`: application deployment state machine.
  - `AnalysisTemplate` / `AnalysisRun`: application-level metrics-driven safety checks; the current app onboarding pattern requires an `AnalysisTemplate` during canary rollout steps.
  - `Service` stable/canary pair: traffic targets for rollout steps.
  - `VirtualService` / `DestinationRule`: Istio routing for mesh-aware workloads.
- **Storage Strategy**:
  - Rollouts state is Kubernetes API state. No separate database is introduced.
  - Controller metrics are scraped in-cluster by Alloy ([ADR-0045](../02.decisions/0045-in-cluster-telemetry-collection.md)) and remote-written to the external Prometheus; no metrics NodePort remains.
- **Data Boundaries**:
  - No credentials are introduced by Rollouts itself; the reference analysis consumes the ESO-synced `prometheus-api-auth` Secret and the `hy-home-root-ca` ConfigMap from the app namespace.

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Rollouts dashboard `rollouts.hy-k8s.home.arpa` | `argo-rollouts` dashboard | Browser users | [Rollouts Application](../../../gitops/apps/root/platform-rollouts-app.yaml) | not stated in this document |
| Controller metrics `argo-rollouts:8090` | Argo Rollouts controller | In-cluster Alloy, remote-written to the external Prometheus | [ADR-0045](../02.decisions/0045-in-cluster-telemetry-collection.md) | not stated in this document |
| `Rollout` and `AnalysisTemplate` CRDs | Application teams through workload manifests | Argo Rollouts controller | `gitops/workloads/adminer/rollout.yaml` | not stated in this document |
| Analysis queries to `https://prometheus.hy.home.arpa` | Reference `AnalysisTemplate` | External Prometheus | [ADR-0046](../02.decisions/0046-external-services-over-host-addresses.md) | not stated in this document |

#### Runtime Behavior

##### Normal Flow

- **Runtime / Platform**:
  - Linux server + k3d/k3s local platform managed by ArgoCD.
  - Namespace: `argo-rollouts`.
  - Dashboard host: `rollouts.hy-k8s.home.arpa`.
- **Declared Deployment Model**:
  - `platform-rollouts` ArgoCD Application declares the Helm chart installation.
  - `gitops/apps/root/kustomization.yaml` includes the Application.
  - AppProject `platform` allows the chart repo and destination namespace.
  - AppProject `apps` allows application workloads to use Rollout and Analysis resources.
- **Verification Scope**:
  - Static checks cover Application and kustomization structure and manifest syntax.
  - Controller availability and dashboard reachability remain unobserved in this description. The [operations runbook](../../05.operations/03.runbooks/0004-rollouts-notifications-headlamp-runbook.md) owns runtime verification.

##### Failure and Recovery

No separate failure boundary is recorded in this description; the failure and recovery behavior it states is in [Scenarios](#scenarios).

#### Quality Scenarios

##### Scenarios

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| Performance | The controller and dashboard start | Single-host k3d cluster | Requests and limits stay pinned | Both Deployments declare requests and limits in the chart values |
| Security | An app Application requests Rollouts CRDs or a namespace | AppProject `platform` and `apps` | Only allow-listed kinds, repo and namespaces reconcile | A resource outside the allow-list is rejected by ArgoCD |
| Reliability | The `platform-rollouts` source drifts or a sync fails | ArgoCD reconciliation | Retry and self-heal restore the declared state | The Application returns to Synced and Healthy |
| Scalability | More apps adopt Rollouts | Shared controller, per-app Rollouts in `apps` namespaces | Per-app scaling stays in the workload contract | No controller change per adopting app |
| Observability | An operator inspects controller metrics | In-cluster Alloy scraping `argo-rollouts:8090` with remote-write to the external Prometheus | Controller metrics reach the external Prometheus | The controller target is up in Prometheus |
| Operability | An operator checks progress, promotion, abort or rollback | Dashboard, CLI and runbook | The path is available without platform changes | Each path is listed in the runbook checks |

##### Trade-offs

One shared controller serves every app that adopts Rollouts, so an adopting app needs no controller change, while every app depends on that controller. Pinned requests and limits keep the controller and dashboard inside the single-host k3d cluster, and progress, promotion, abort and rollback stay on the dashboard, CLI and runbook paths without a platform change.

#### Decisions and Adoption

##### Decisions

- **ADR**: [`../decisions/0011-argo-rollouts-progressive-delivery.md`](../02.decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../decisions/0054-platform-decision-current-state-amendment.md`](../02.decisions/0054-platform-decision-current-state-amendment.md) — current promotion-mode clause

###### Requirement Mapping

- **Requirement**: [`../../01.requirements/0001-argo-rollouts-progressive-delivery.md`](../../01.requirements/0001-argo-rollouts-progressive-delivery.md)

##### Adoption Boundaries

- **Spec**: N/A — SPEC-0004 left the tree; Git history recovers it ([REQ-0001 Archived Lineage](../../01.requirements/0001-argo-rollouts-progressive-delivery.md#archived-lineage))

##### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0001-FR-0001](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The GitOps-owned install boundary of the shared controller and dashboard | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-FR-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The Dashboard TLS boundary through the Traefik ingress controller ([ADR-0050](../02.decisions/0050-ingress-nginx-replacement-with-traefik.md)) and cert-manager | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-FR-0003](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The external Prometheus observability boundary of controller metrics | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-IF-0001](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The AppProject allow-list and ArgoCD health tracking boundary | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-IF-0002](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | A default that imposes no promotion mode, and failure safety through an approved AnalysisTemplate | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| [REQ-0001-IF-0003](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) | The route boundary between the k8s router and the cluster ingress | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | Operational evidence of controller Deployment availability | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | The live evidence boundary of the Dashboard HTTPS response and progress display | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | Reconciliation evidence of the ArgoCD Rollout health state | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0001-argo-rollouts-progressive-delivery.md) remains package-owned | The validation boundary that separates repo-static gates from runtime checks | [ADR 0011](../02.decisions/0011-argo-rollouts-progressive-delivery.md) |

## 적용과 확인

### 적용 방법

Apply the decisions and procedures in the role payload under its stated conditions.

### 확인 기준

Check the role payload acceptance or verification conditions and report observed limits.

## 관계와 출처

### 관련 문서

Follow the current upstream and downstream links in the role payload.

### 외부 근거

External evidence, when used, remains attributed and bounded in the role payload.
