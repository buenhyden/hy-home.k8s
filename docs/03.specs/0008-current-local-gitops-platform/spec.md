---
title: "Current Local GitOps Platform Technical Specification"
version: "1.3.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0008"
---

# Current Local GitOps Platform Technical Specification (Spec)

## Overview

This document records the completed implementation contract for the repo-backed
local GitOps platform. [AD-0007](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
owns the current architecture view; `gitops/`, `infrastructure/`, and `scripts/`
own their executable desired state and validation behavior.

**Disposition history.** On 2026-09-16, [SPEC-0084](../../98.archive/completed/03.specs/0084-stage03-backlog-closeout/spec.md)
left this package active because current consumers still treated it as a living
platform contract. The 2026-10-03 closeout transferred current architecture and
execution authority to AD-0007 and the executable sources above; current
consumers are routed there. This completed package remains historical delivery
evidence. [Task 0002](tasks/tsk-0002-platform-contract-closeout.md) records the
verification and residual boundaries.

## Strategic Boundaries & Non-goals

This spec bounded the local platform implementation work represented by `gitops/`, `infrastructure/`, and `scripts/`.
README navigation is owned by [SPEC-0091](../../98.archive/completed/03.specs/0091-readme-navigation-contract/spec.md).
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
  - Prometheus and Grafana use authenticated HTTPS gateway names. Remaining
    cluster service interfaces, including Tempo, are declared under
    `gitops/platform/external-services` (ADR-0037, ADR-0046).
- **Ingress Router Contract** (ADR-0043):
  - k8s hosts are `<name>.hy-k8s.home.arpa`; ArgoCD is `argo.hy-k8s.home.arpa`.
  - `hy-k8s.home.arpa/<name>` returns a 301 to `https://<name>.hy-k8s.home.arpa/`.
  - The k3d serverlb binds only `192.168.0.14:80` and `192.168.0.14:443` and forwards to ingress-nginx NodePorts `30080` and `30443`.
  - The external services workspace Traefik carries no k8s route.
- **Governance Contract**:
  - Current docs use AD-0007 and executable sources for current implementation;
    completed Spec packages may be cited only as historical delivery evidence.
  - Old documents follow the disposition and citation rules in
    [document lifecycle](../../../.agents/governance/document-lifecycle.md).
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
  - Kubernetes/k3d, ArgoCD, ingress-nginx, cert-manager, External Secrets Operator, OpenBao (Vault API), Istio, Kiali Operator, Headlamp, Argo Rollouts, Argo Notifications, Alloy/kube-state-metrics.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Kubernetes manifests define desired state.
  - External service contracts use Kubernetes `Service` and `EndpointSlice`.
  - Secrets use ESO `ExternalSecret` and OpenBao remote references through the Vault provider.
- **Migration / Transition Plan**:
  - Superseded or completed documents follow their Stage 98 disposition.
  - Current indexes and operational guidance point to AD-0007 and executable sources.

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
- **Archived doc used as current guidance**: route the current contract to its
  active owner; cite a completed package only as historical evidence.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Current docs reintroduce conflicting historical implementation contracts.
- **Fallback**: Fail the repository quality gate and use the current owner or the
  applicable Stage 98 disposition.
- **Human Escalation**: Required for live mutation, Vault writes, or external runtime changes.

## Verification Commands

```bash
python3 scripts/qa.py full
bash scripts/validate-infrastructure-contracts.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: The full-equivalent QA profile passes on an immutable hosted
  checkout, or the local full profile passes for local-only handoff. Current
  documents do not use archived history as execution authority; explicit
  historical citations of completed packages remain valid.
- **VAL-SPC-002**: Static contract verification passes against current GitOps manifests.
- **VAL-SPC-003**: GitOps structure check passes.
- **VAL-SPC-004**: Kubernetes manifest syntax validation passes.
- **VAL-SPC-005**: Static contracts enforce the ingress router contract: serverlb bind address and NodePorts, `hy-k8s.home.arpa` hosts, and the apex redirects.

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — [Acceptance criterion 04](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-001 | Hosted full-equivalent QA or local-only full QA checks current authority and permitted historical citations. |
| N/A — [Acceptance criterion 01](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-002 | `scripts/validate-infrastructure-contracts.sh` verifies the current GitOps manifest contracts. |
| N/A — [Acceptance criterion 02](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-003 | `scripts/validate-gitops-structure.sh` checks root Application, platform Application, and workload ApplicationSet ownership. |
| N/A — [Acceptance criterion 03](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-004 | `scripts/validate-k8s-manifests.sh .` validates tracked Kubernetes YAML syntax. |
| N/A — [Acceptance criterion 01](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | VAL-SPC-005 | `scripts/validate-infrastructure-contracts.sh` and the repository-quality gate verify the ingress router contract. |

### Inputs

- **PRD**: [../../01.requirements/0004-current-local-gitops-platform.md](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [../../02.architecture/descriptions/0007-current-local-gitops-platform.md](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
- **Related ADRs**: [ADR-0014](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md), [ADR-0037](../../02.architecture/decisions/0037-kiali-operator-installation.md), [ADR-0041](../../02.architecture/decisions/0041-openbao-secret-backend.md), [ADR-0042](../../02.architecture/decisions/0042-linux-server-single-host-baseline.md), [ADR-0043](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md), [ADR-0044](../../02.architecture/decisions/0044-stateful-data-stores-stay-external.md), [ADR-0045](../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md), [ADR-0046](../../02.architecture/decisions/0046-external-services-over-host-addresses.md)

### Delivery and References

- **Plan**: [plan.md](plan.md)
- **Task**: [tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md](tasks/tsk-0001-dedicated-k8s-router-and-host-baseline.md)
- **Closeout Task**: [tasks/tsk-0002-platform-contract-closeout.md](tasks/tsk-0002-platform-contract-closeout.md)
- **Operations Policy**: [../../05.operations/policies/0001-k8s-gitops-operations-policy.md](../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- **Runbook**: [../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md](../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- **GitOps desired state**: [../../../gitops](../../../gitops)
