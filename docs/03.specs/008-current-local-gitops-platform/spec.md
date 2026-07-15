---
title: 'Current Local GitOps Platform Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-06-02
---

# Current Local GitOps Platform Technical Specification (Spec)

## Overview

This document defines the implementation contract for the current repo-backed
local GitOps platform. Old platform specs are archived as Tombstones, and this
spec is the active technical contract for current manifests, scripts, and
validation evidence.

## Strategic Boundaries & Non-goals

This spec owns the current local platform implementation contract represented by `gitops/`, `infrastructure/`, `scripts/`, and root/stage READMEs.
It does not own external service runtime creation, live cluster repair, secret values, or cloud provider provisioning.

## Contracts

- **Config Contract**:
  - Root ArgoCD Application source path: `gitops/apps/root`.
  - Platform Applications live under `gitops/apps/root/platform-*.yaml`.
  - Workload ApplicationSet scans `gitops/workloads/*`.
  - Platform namespace desired state lives under `gitops/platform/namespaces`.
- **Data / Interface Contract**:
  - Vault API service: `vault-external.platform.svc.cluster.local:8200`.
  - PostgreSQL write service: `postgres-write-external.platform.svc.cluster.local:15432`.
  - PostgreSQL read service: `postgres-read-external.platform.svc.cluster.local:15433`.
  - Valkey service: `valkey-external.platform.svc.cluster.local:6379`.
  - Observability service contracts are declared under `gitops/platform/external-services`.
- **Governance Contract**:
  - Active docs must describe current implementation only.
  - Old conflicting docs move to `docs/98.archive` as Tombstones.
  - Secret values stay outside Git and docs.

## Core Design

- **Component Boundary**:
  - `gitops/clusters/local`: root Application, AppProjects, workload ApplicationSet.
  - `gitops/apps/root`: platform Application graph.
  - `gitops/platform`: platform component manifests.
  - `gitops/workloads/adminer`: reference workload pattern.
  - `infrastructure`: k3d, bootstrap, ArgoCD values, static and live validation scripts.
- **Key Dependencies**:
  - WSL2 shell, WSL-native Docker, k3d, kubectl, Helm.
  - External Vault, PostgreSQL, Valkey, and observability services.
- **Tech Stack**:
  - Kubernetes/k3d, ArgoCD, ingress-nginx, cert-manager, External Secrets Operator, Vault, Istio, Kiali, Headlamp, Argo Rollouts, Argo Notifications, Alloy/kube-state-metrics.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Kubernetes manifests define desired state.
  - External service contracts use Kubernetes `Service` and `EndpointSlice`.
  - Secrets use ESO `ExternalSecret` and Vault remote references.
- **Migration / Transition Plan**:
  - Old docs are archived into Tombstones.
  - Active README indexes and Related Documents point to this current contract.

## Interfaces & Data Structures

### Core Interfaces

```yaml
platform_contract:
  desired_state_roots:
    - gitops/clusters/local
    - gitops/apps/root
    - gitops/platform
    - gitops/workloads
  validation:
    static_contract: infrastructure/tests/verify-contracts-static.sh
    gitops_structure: scripts/validate-gitops-structure.sh
    manifest_syntax: scripts/validate-k8s-manifests.sh
```

## Edge Cases & Error Handling

- **Missing external service runtime**: static contracts may pass while live validation fails; record this as an external/runtime blocker.
- **Broken kubeconfig or TLS trust**: do not repair automatically; require operator approval.
- **Archived doc referenced directly**: update the active document to use the archive index or current replacement.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Active docs reintroduce old conflicting implementation contracts.
- **Fallback**: Fail repo quality gate and move old material to Tombstone or rewrite as current.
- **Human Escalation**: Required for live mutation, Vault writes, or external runtime changes.

## Verification Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Repo quality gate passes with archive Tombstone policy enabled.
- **VAL-SPC-002**: Static contract verification passes against current GitOps manifests.
- **VAL-SPC-003**: GitOps structure check passes.
- **VAL-SPC-004**: Kubernetes manifest syntax validation passes.

## Traceability

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-MET-04](../../01.requirements/004-current-local-gitops-platform.md) | VAL-SPC-001 | `scripts/validate-repo-quality-gates.sh .` checks current active-document and archive Tombstone policy. |
| [REQ-PRD-MET-01](../../01.requirements/004-current-local-gitops-platform.md) | VAL-SPC-002 | `infrastructure/tests/verify-contracts-static.sh` verifies the current GitOps manifest contracts. |
| [REQ-PRD-MET-02](../../01.requirements/004-current-local-gitops-platform.md) | VAL-SPC-003 | `scripts/validate-gitops-structure.sh` checks root Application, platform Application, and workload ApplicationSet ownership. |
| [REQ-PRD-MET-03](../../01.requirements/004-current-local-gitops-platform.md) | VAL-SPC-004 | `scripts/validate-k8s-manifests.sh .` validates tracked Kubernetes YAML syntax. |

### Inputs

- **PRD**: [../../01.requirements/004-current-local-gitops-platform.md](../../01.requirements/004-current-local-gitops-platform.md)
- **ARD**: [../../02.architecture/requirements/0007-current-local-gitops-platform.md](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- **Related ADRs**: [../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)

### Delivery and References

- **Plan**: [../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md](../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
- **Tasks**: [../../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md](../../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md)
- **Runbook**: [../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md](../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
