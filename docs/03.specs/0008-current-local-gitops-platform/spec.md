---
title: "Current Local GitOps Platform Technical Specification"
version: "1.2.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0008"
---

# Current Local GitOps Platform Technical Specification (Spec)

## Overview

This document defines the implementation contract for the current repo-backed
local GitOps platform. Old platform specs are archived as Tombstones, and this
spec is the active technical contract for current manifests, scripts, and
validation evidence.

**Disposition note (2026-09-16).** This package stays `active` and is not closed by [SPEC-0084](../../98.archive/completed/03.specs/0084-stage03-backlog-closeout/spec.md). It owns the current platform contract rather than a finished round: ADR-0002, ADR-0041, ADR-0006, ADR-0008, ADR-0009 and ADR-0014 each name it as their Spec, REQ-0004 traces to it, the Stage 05 policies and runbooks carry it in their RACI rows, three test modules pin its path, and the Archive index names it as the replacement for three superseded platform specs. Closing it would leave those citations pointing at a finished document, and no successor exists to take them. Next owner: whoever replaces the platform contract, if anyone ever does.

## Strategic Boundaries & Non-goals

This spec owns the current local platform implementation contract represented by `gitops/`, `infrastructure/`, and `scripts/`.
README navigation is owned by [SPEC-0091](../0091-readme-navigation-contract/spec.md).
It does not own external service runtime creation, live cluster repair, secret values, or cloud provider provisioning.

## Contracts

- **Config Contract**:
  - Root ArgoCD Application source path: `gitops/apps/root`.
  - Platform Applications live under `gitops/apps/root/platform-*.yaml`.
  - Workload ApplicationSet scans `gitops/workloads/*`.
  - Platform namespace desired state lives under `gitops/platform/namespaces`.
- **Data / Interface Contract**:
  - Secret backend API: `https://openbao.hy.home.arpa`, external OpenBao (Vault API compatible, ADR-0041) behind the external Traefik. A CoreDNS custom zone resolves the name to the host address, and ESO pins the mkcert root CA (ADR-0046).
  - PostgreSQL write service: `postgres-write-external.platform.svc.cluster.local:15432`.
  - PostgreSQL read service: `postgres-read-external.platform.svc.cluster.local:15433`.
  - Valkey service: `valkey-external.platform.svc.cluster.local:6379`, backed by external `mng-valkey` at host port `26379` (ADR-0044, ADR-0046).
  - PostgreSQL services are backed by external `pg-router` of `postgresql-cluster`, which runs only under the external profile `postgres-ha` (ADR-0044). The bootstrap does not require it (ADR-0046).
  - Every external service endpoint is the host address `192.168.0.13` and a host-published port, never a `k3d-hyhome` container address (ADR-0046).
  - Observability service contracts are declared under `gitops/platform/external-services`.
- **Ingress Router Contract** (ADR-0043):
  - k8s hosts are `<name>.hy-k8s.home.arpa`; ArgoCD is `argo.hy-k8s.home.arpa`.
  - `hy-k8s.home.arpa/<name>` returns a 301 to `https://<name>.hy-k8s.home.arpa/`.
  - The k3d serverlb binds only `192.168.0.14:80` and `192.168.0.14:443` and forwards to ingress-nginx NodePorts `30080` and `30443`.
  - The external services workspace Traefik carries no k8s route.
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
  - Linux server shell, native Docker Engine, k3d, kubectl, Helm.
  - External OpenBao, PostgreSQL, Valkey, and observability services.
- **Tech Stack**:
  - Kubernetes/k3d, ArgoCD, ingress-nginx, cert-manager, External Secrets Operator, OpenBao (Vault API), Istio, Kiali, Headlamp, Argo Rollouts, Argo Notifications, Alloy/kube-state-metrics.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Kubernetes manifests define desired state.
  - External service contracts use Kubernetes `Service` and `EndpointSlice`.
  - Secrets use ESO `ExternalSecret` and OpenBao remote references through the Vault provider.
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
    static_contract: scripts/validate-infrastructure-contracts.sh
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
python3 scripts/qa.py full
bash scripts/validate-infrastructure-contracts.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `python3 scripts/qa.py full` passes and active documents have no Stage 98 dependency.
- **VAL-SPC-002**: Static contract verification passes against current GitOps manifests.
- **VAL-SPC-003**: GitOps structure check passes.
- **VAL-SPC-004**: Kubernetes manifest syntax validation passes.
- **VAL-SPC-005**: Static contracts enforce the ingress router contract: serverlb bind address and NodePorts, `hy-k8s.home.arpa` hosts, and the apex redirects.

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — [Acceptance criterion 04](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-001 | `python3 scripts/qa.py full` checks current active-document contracts without an Archive dependency. |
| N/A — [Acceptance criterion 01](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-002 | `scripts/validate-infrastructure-contracts.sh` verifies the current GitOps manifest contracts. |
| N/A — [Acceptance criterion 02](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-003 | `scripts/validate-gitops-structure.sh` checks root Application, platform Application, and workload ApplicationSet ownership. |
| N/A — [Acceptance criterion 03](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-004 | `scripts/validate-k8s-manifests.sh .` validates tracked Kubernetes YAML syntax. |
| N/A — [Acceptance criterion 01](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-005 | `scripts/validate-infrastructure-contracts.sh` and the repository-quality gate verify the ingress router contract. |

### Inputs

- **PRD**: [../../01.requirements/0004-current-local-gitops-platform.md](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [../../02.architecture/descriptions/0007-current-local-gitops-platform.md](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
- **Related ADRs**: [../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md), [../../02.architecture/decisions/0041-openbao-secret-backend.md](../../02.architecture/decisions/0041-openbao-secret-backend.md), [../../02.architecture/decisions/0042-linux-server-single-host-baseline.md](../../02.architecture/decisions/0042-linux-server-single-host-baseline.md), [../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md), [../../02.architecture/decisions/0044-stateful-data-stores-stay-external.md](../../02.architecture/decisions/0044-stateful-data-stores-stay-external.md), [../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md](../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md), [../../02.architecture/decisions/0046-external-services-over-host-addresses.md](../../02.architecture/decisions/0046-external-services-over-host-addresses.md)

### Delivery and References

- **Plan**: [plan.md](plan.md)
- **Task**: [tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md](tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md)
- **Operations Policy**: [../../05.operations/policies/0001-k8s-gitops-operations-policy.md](../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- **Runbook**: [../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md](../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- **GitOps desired state**: [../../../gitops](../../../gitops)
