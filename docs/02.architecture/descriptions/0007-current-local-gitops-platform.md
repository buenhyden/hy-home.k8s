---
title: "Current Local GitOps Platform Architecture Description"
version: "1.2.2"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "AD-0007"
---

# Current Local GitOps Platform Architecture Description (AD)

## Overview

This document defines the reference architecture of the currently implemented local GitOps platform.
Old endpoints and removed UI contracts are split out into archive Tombstones, and the current structure is described from the GitOps desired state and static contract evidence.

### Current architecture summary

The current platform consists of a k3d cluster on the Linux server's native Docker Engine, the ArgoCD App-of-Apps, platform Applications, the workload ApplicationSet, and external service interface contracts.
The architecture's core goals are local reproducibility, GitOps-first ownership, secret-safe integration, and current-document traceability.

## Boundaries & Non-goals

- **Owns**:
  - Local k3d cluster configuration and bootstrap assets.
  - ArgoCD root Application, AppProjects, platform Applications, and workload ApplicationSet manifests.
  - Kubernetes interface contracts for external OpenBao (Vault API compatible), PostgreSQL, Valkey, and observability services.
  - Headlamp, Kiali, Argo Rollouts, Argo Notifications, ingress-nginx, cert-manager, Istio, monitoring, and ESO configuration.
- **Consumes**:
  - External service runtime readiness.
  - OpenBao source secrets and operator-managed secret rotation.
  - Linux server host Docker, DNS, and network state.
- **Does Not Own**:
  - External service containers or cloud provider resources.
  - Secret values.
  - Live cluster repair without explicit approval.
- **Non-goals**:
  - Preserve old conflicting runtime values in active architecture docs.
  - Treat archive Tombstones as architecture input.

## Quality Attributes

- **Performance**: Local platform components must stay suitable for the single-host k3d resource budget ([ADR-0042](../decisions/0042-linux-server-single-host-baseline.md)).
- **Security**: Secrets are synced through ESO/OpenBao contracts ([ADR-0041](../decisions/0041-openbao-secret-backend.md)) without storing values in Git.
- **Reliability**: Desired state is expressed through GitOps manifests and static contract checks.
- **Scalability**: Workload onboarding uses ApplicationSet over `gitops/workloads/*`.
- **Observability**: Kiali and monitoring manifests integrate with external observability endpoints.
- **Operability**: Static checks and runbooks separate repo-backed validation from live runtime validation.

## System Overview & Context

The root application in `gitops/clusters/local/root-application.yaml` points to `gitops/apps/root`.
Platform Applications then install or configure ArgoCD, namespaces, cert-manager, ingress-nginx, ESO, external services, Headlamp, Istio/Kiali, monitoring, Rollouts, and network policies.
The apps ApplicationSet owns workload directories under `gitops/workloads/*`.

### Delivery assurance architecture transferred from AD-0010

This AD inherits AD-0010's boundaries for platform validation, interfaces, examples, source revisions, and namespace evidence.
[AD-0006](./0006-workspace-agent-governance-platform.md) and
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) co-own the common affected-path, CI, approval, and review obligations.
[REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md) states the per-member succession of the current platform requirements.

| Surface or flow | Current source / implementation owner | Evidence boundary |
| --- | --- | --- |
| Desired-state tree | [root Application](../../../gitops/clusters/local/root-application.yaml), [root kustomization](../../../gitops/apps/root/kustomization.yaml) | The static structure of root → platform Applications / workload ApplicationSet, not live reconciliation evidence |
| Local runtime and namespace policy | [k3d config](../../../infrastructure/k3d/k3d-cluster.yaml), [namespace declarations](../../../gitops/platform/namespaces/) | Enforce only on workloads the repository owns and validates statically; chart/injection uncertainty is audit/warn |
| Dispatch and GitHub projections | [Validation Registry](../../../scripts/validation/registry.json), [.github](../../../.github/) | The Registry owns lanes and argv; parity with the labels/CODEOWNERS native projections is Spec 0048's unfinished scope |
| Platform verification | [static contract checks](../../../scripts/validate-infrastructure-contracts.sh), [validators](../../../scripts/) | Separate syntax → render → schema/policy → product semantic → live observation; derive the actual root count and tools from the executable source |
| Cloud examples | [AWS](../../../examples/aws/README.md), [Azure](../../../examples/azure/README.md) | Terraform/Bicep format/validate/lint/build; provider credentials, apply, or deploy need separate approval |
| Local browser/service transport | [k8s router](../../../infrastructure/k3d/k3d-cluster.yaml), [apex redirects](../../../gitops/platform/ingress-routes/), [external service interfaces](../../../gitops/platform/external-services/) | Check the dedicated k8s router (ADR-0043) and the local-only transport exceptions without widening an exception into a general security allowance |

Each product validator owns its own area: Kubernetes GVKs, the k8s router contract, GitOps
structure, policy, and the Vault/ESO source and secret boundary. A missing tool, malformed
input, an unsafe path, and a fallback each need a direct negative fixture, and a required-tool
failure is not hidden as a SKIP.

Exact chart, infrastructure, workflow, dependency, and example versions live in the executable
source or a reviewed lock. The Stage 90 version mirror is not an execution precondition.
The repository's own source uses `targetRevision: main`, as
[ADR-0029](../decisions/0029-mutable-target-revision-retention.md) decided, kept distinct from the
exact revisions of external charts; the branch policy is revisited when multiple operators,
multiple environments, or history rewriting are introduced.
Images keep the current non-latest tag-or-digest check, with no unverified blanket digest change.
Further digest/SBOM/provenance obligations are approved follow-on work with a consumer, owner, and trigger.
The Istio CNI manifest is desired state and proves no actual admission or network state.

### Unfinished implementation owners

Spec 0049 depended on the retired Spec 0048 and the Traefik lane and was withdrawn on 2026-09-25 ([SPEC-0089](../../03.specs/0089-deferred-conflict-resolution/spec.md)); it is kept in `98.archive/retired/` and not cited ([SPEC-0090](../../03.specs/0090-spec0049-retirement/spec.md)). Its unimplemented scope (render, schema, policy, secret, shell fixture, image, and tool evidence lanes) remains an ownerless gap of REQ-0004-FR-0008 and FR-0010; the next owner is the request owner who plans a new package under current authority.
GitHub routing/CI (Spec 0048), native IaC/direct negative fixtures (Spec 0050),
the final local-only integration (Spec 0051), and surface/hunk reconciliation (Spec 0047) were withdrawn without successors
and kept in `98.archive/retired/` ([SPEC-0087](../../03.specs/0087-stage03-terminal-package-retention/spec.md));
their scope currently has no implementation owner. The AD succession does not mean any tranche or WP-013 is complete.

## Data Architecture

- **Key Entities / Flows**:
  - ArgoCD reconciles Git manifests into the local cluster.
  - ESO reads approved OpenBao paths through the `vault-backend` ClusterSecretStore and its Vault-API `vault` provider.
  - External service `Service` and `EndpointSlice` resources expose local service interfaces to workloads.
- **Storage Strategy**:
  - Runtime data remains in external PostgreSQL, Valkey, OpenBao, and observability services.
  - This repository stores only interface contracts and configuration.
- **Data Boundaries**:
  - Secret values, tokens, and private keys stay outside Git.
  - Active docs store current contract facts only.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Linux server shell with the native Docker Engine.
  - k3d cluster named `hyhome`.
  - ingress-nginx behind the dedicated k8s router (k3d serverlb on `192.168.0.14:443`) for browser access at `<name>.hy-k8s.home.arpa` ([ADR-0043](../decisions/0043-dedicated-k8s-ingress-router.md)).
- **Deployment Model**:
  - Bootstrap installs the initial ArgoCD boundary.
  - Steady-state changes flow through Git and ArgoCD reconciliation.
- **Operational Evidence**:
  - `bash scripts/validate-infrastructure-contracts.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`

### Agent architecture requirements

- **Model/Provider Strategy**: Provider adapters must route to Common agent governance and current active docs.
- **Tooling Boundary**: Agents may inspect and edit repo files inside the workspace; live mutation requires approval.
- **Memory & Context Strategy**: durable execution evidence goes in the package-local Task, common rules in `.agents/governance/`, and temporary checkpoints in ignored recovery state.
- **Guardrail Boundary**: Superseded/ended records are non-authoritative history; completed packages retain their own types under ADR-0038.
- **Latency / Cost Budget**: Not applicable to platform runtime.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0004-FR-0001](../../01.requirements/0004-current-local-gitops-platform.md) | Desired-state root ownership of clusters, root apps, platform, and workloads | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-FR-0002](../../01.requirements/0004-current-local-gitops-platform.md) | The App-of-Apps and ApplicationSet reconciliation boundary | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-FR-0003](../../01.requirements/0004-current-local-gitops-platform.md) | Separation of the external runtime from the Kubernetes Service/EndpointSlice interface | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-FR-0004](../../01.requirements/0004-current-local-gitops-platform.md) | Separation of the current Headlamp UI from archived UI history | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-NFR-0001](../../01.requirements/0004-current-local-gitops-platform.md) | The explicit scope of the current platform component graph | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-NFR-0002](../../01.requirements/0004-current-local-gitops-platform.md) | The trust boundary between ESO/Vault references and secret values | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-IF-0001](../../01.requirements/0004-current-local-gitops-platform.md) | The authority boundary between the active current contract and archive Tombstones | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | Repo-backed evidence owned by static contract verification | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | Structure validation evidence for root, platform, and workload | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | tracked Kubernetes manifest syntax evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | Active/archive currentness evidence from the repository quality gate | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |

### Transferred requirement members

| Current requirement | Retained architecture boundary | Implementation owner |
| --- | --- | --- |
| REQ-0004-FR-0005, REQ-0004-FR-0006 | Source inventory and resumed-change semantic ownership | None; Spec 0047 was withdrawn without a successor |
| REQ-0004-FR-0007 | Single routing owner with GitHub-native projections | AD-0006; Spec 0048 was withdrawn without a successor |
| REQ-0004-FR-0008, REQ-0004-FR-0010, REQ-0004-FR-0014, REQ-0004-NFR-0003 | Layered product/policy evidence, local exceptions, namespace and artifact assurance | None; Spec 0049 withdrawn 2026-09-25, gap recorded at REQ-0004 |
| REQ-0004-FR-0009 | Example-adjacent native validation without cloud deployment | None; Spec 0050 was withdrawn without a successor |
| REQ-0004-FR-0011 | Ordered review/rollback boundaries and local-only integration | None; Spec 0051 was withdrawn without a successor |
| REQ-0004-FR-0012, REQ-0004-FR-0013 | Direct executable-source versions and self-source/external-source distinction | Executable manifests and ADR-0029 |

Original AD-0010 and REQ-0007 program identity remain historical lineage. These current boundaries
do not rewrite which description the original ADRs served; superseded bodies are retained under `98.archive/superseded/`.

- **Requirement**: [../../01.requirements/0004-current-local-gitops-platform.md](../../01.requirements/0004-current-local-gitops-platform.md)
- **Spec**: [../../03.specs/0008-current-local-gitops-platform/spec.md](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Plan**: [../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md](../../98.archive/README.md#document-index)
- **ADR**: [../decisions/0014-current-local-gitops-platform-contract.md](../decisions/0014-current-local-gitops-platform-contract.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
