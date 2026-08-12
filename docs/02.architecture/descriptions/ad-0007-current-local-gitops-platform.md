---
title: 'Current Local GitOps Platform Architecture Description'
type: sdlc/ad
status: active
owner: platform
updated: 2026-07-13
artifact_id: "AD-0007"
---

# Current Local GitOps Platform Architecture Description (AD)

## Overview

이 문서는 현재 구현된 local GitOps platform의 참조 아키텍처를 정의한다.
old endpoint와 제거된 UI 계약은 archive Tombstone으로 분리하고, 현재 구조는 GitOps desired state와 static contract evidence를 기준으로 설명한다.

### Current architecture summary

현재 플랫폼은 WSL2 + WSL-native Docker 위의 k3d cluster, ArgoCD App-of-Apps, platform Application, workload ApplicationSet, external service interface contract로 구성된다.
아키텍처의 핵심 목표는 local reproducibility, GitOps-first ownership, secret-safe integration, and current-document traceability다.

## Boundaries & Non-goals

- **Owns**:
  - Local k3d cluster configuration and bootstrap assets.
  - ArgoCD root Application, AppProjects, platform Applications, and workload ApplicationSet manifests.
  - Kubernetes interface contracts for external Vault, PostgreSQL, Valkey, and observability services.
  - Headlamp, Kiali, Argo Rollouts, Argo Notifications, ingress-nginx, cert-manager, Istio, monitoring, and ESO configuration.
- **Consumes**:
  - External service runtime readiness.
  - Vault source secrets and operator-managed secret rotation.
  - WSL2 Docker and network state.
- **Does Not Own**:
  - External service containers or cloud provider resources.
  - Secret values.
  - Live cluster repair without explicit approval.
- **Non-goals**:
  - Preserve old conflicting runtime values in active architecture docs.
  - Treat archive Tombstones as architecture input.

## Quality Attributes

- **Performance**: Local platform components must stay suitable for WSL2/k3d resource budgets.
- **Security**: Secrets are synced through ESO/Vault contracts without storing values in Git.
- **Reliability**: Desired state is expressed through GitOps manifests and static contract checks.
- **Scalability**: Workload onboarding uses ApplicationSet over `gitops/workloads/*`.
- **Observability**: Kiali and monitoring manifests integrate with external observability endpoints.
- **Operability**: Static checks and runbooks separate repo-backed validation from live runtime validation.

## System Overview & Context

The root application in `gitops/clusters/local/root-application.yaml` points to `gitops/apps/root`.
Platform Applications then install or configure ArgoCD, namespaces, cert-manager, ingress-nginx, ESO, external services, Headlamp, Istio/Kiali, monitoring, Rollouts, and network policies.
The apps ApplicationSet owns workload directories under `gitops/workloads/*`.

## Data Architecture

- **Key Entities / Flows**:
  - ArgoCD reconciles Git manifests into the local cluster.
  - ESO reads approved Vault paths through the `vault-backend` ClusterSecretStore.
  - External service `Service` and `EndpointSlice` resources expose local service interfaces to workloads.
- **Storage Strategy**:
  - Runtime data remains in external PostgreSQL, Valkey, Vault, and observability services.
  - This repository stores only interface contracts and configuration.
- **Data Boundaries**:
  - Secret values, tokens, and private keys stay outside Git.
  - Active docs store current contract facts only.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - WSL2 shell with WSL-native Docker.
  - k3d cluster named `hyhome`.
  - ingress-nginx LoadBalancer plus local Traefik dynamic config references for browser access.
- **Deployment Model**:
  - Bootstrap installs the initial ArgoCD boundary.
  - Steady-state changes flow through Git and ArgoCD reconciliation.
- **Operational Evidence**:
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`

### Agent architecture requirements

- **Model/Provider Strategy**: Provider adapters must route to Stage 00 governance and current active docs.
- **Tooling Boundary**: Agents may inspect and edit repo files inside the workspace; live mutation requires approval.
- **Memory & Context Strategy**: Durable governance memory remains under `docs/00.agent-governance/memory`.
- **Guardrail Boundary**: Archive Tombstones are index records, not active implementation sources.
- **Latency / Cost Budget**: Not applicable to platform runtime.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-PRD-FUN-01](../../01.requirements/004-current-local-gitops-platform.md) | clusters, root apps, platform 및 workloads desired-state root ownership | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-FUN-02](../../01.requirements/004-current-local-gitops-platform.md) | App-of-Apps와 ApplicationSet reconciliation 경계 | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-FUN-03](../../01.requirements/004-current-local-gitops-platform.md) | 외부 runtime과 Kubernetes Service/EndpointSlice interface의 분리 | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-FUN-04](../../01.requirements/004-current-local-gitops-platform.md) | Headlamp current UI와 archived UI history의 분리 | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-FUN-05](../../01.requirements/004-current-local-gitops-platform.md) | 현재 platform component graph의 명시적 scope | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-FUN-06](../../01.requirements/004-current-local-gitops-platform.md) | ESO/Vault reference와 secret value의 trust boundary | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-FUN-07](../../01.requirements/004-current-local-gitops-platform.md) | active current contract와 archive Tombstone의 authority boundary | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-MET-01](../../01.requirements/004-current-local-gitops-platform.md) | static contract verification이 소유하는 repo-backed evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-MET-02](../../01.requirements/004-current-local-gitops-platform.md) | root, platform, workload 구조 검증 evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-MET-03](../../01.requirements/004-current-local-gitops-platform.md) | tracked Kubernetes manifest syntax evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [REQ-PRD-MET-04](../../01.requirements/004-current-local-gitops-platform.md) | repository quality gate의 active/archive currentness evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/008-current-local-gitops-platform/spec.md) |

- **PRD**: [../../01.requirements/004-current-local-gitops-platform.md](../../01.requirements/004-current-local-gitops-platform.md)
- **Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan**: [../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md](../../98.archive/README.md#document-index)
- **ADR**: [../decisions/0014-current-local-gitops-platform-contract.md](../decisions/0014-current-local-gitops-platform-contract.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
