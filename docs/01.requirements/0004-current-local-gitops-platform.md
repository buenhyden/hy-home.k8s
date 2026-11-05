---
title: "Local GitOps Platform and Delivery Assurance Requirements"
version: "1.4.0"
type: "sdlc/requirement"
status: "approved"
owner: "platform"
updated: "2026-11-05"
layer: "requirements"
artifact_id: "REQ-0004"
---

# Local GitOps Platform and Delivery Assurance Requirements

## Overview

This document owns the user value, operating boundaries, and delivery assurance requirements of the local GitOps platform.
[AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) owns the concrete topology and implementation choices,
and [REQ-0003](./0003-workspace-agent-governance-platform.md) owns the common governance, validation, and approval requirements.

## Vision

Users must be able to reproduce the local platform and change it safely from the repository's desired state and from evidence whose depth is kept distinct.

## Problem Statement

Confusing the current desired state, historical documents, and actual runtime state can present a removed feature or an unverified
security level as supported. The existence of static configuration must be kept apart from reconciliation or external service availability.

## Personas

- Platform engineer: manages the platform ownership boundaries and external service interfaces.
- Operator: operates through the current UIs, GitOps state, and bounded observed evidence.
- Application author: follows the validation and onboarding boundaries of workloads and cloud examples.

## Key Use Cases

- A changer finds each surface's semantic owner and the static validation it needs.
- An operator confirms the platform/workload boundary and external service dependencies.
- A reviewer judges failure, fallback, DEFER, and live-unobserved states separately.
- An executor resumes an unfinished assurance package within its prerequisite validation and approval scope.

## Functional Requirements

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-0004-FR-0001 | The local platform's desired state must be declared reproducibly in the repository, with its ownership boundaries kept distinct. | Must | Acceptance criteria 01 and 03; quality scenario GitOps reproducibility. |
| REQ-0004-FR-0002 | The reconciliation, ownership, and permission boundaries of platform components and user workloads must be separated. | Must | Acceptance criterion 02. |
| REQ-0004-FR-0003 | Connections to external secret, data, and observability services must be expressed as explicit service interfaces and kept distinct from creating the external runtime. | Must | Quality scenarios External interface and Secret TLS recovery. |
| REQ-0004-FR-0004 | Operators must be able to reach the currently supported cluster UIs, and a removed UI must not be presented as the current implementation. | Must | Acceptance criterion 04; each UI route in the AD-0007 ingress owner resolves in the desired state. |
| REQ-0004-FR-0005 | Each tracked surface in a change's scope must be classified as changed, unchanged with a reason, or DEFER with an owner and a retry condition. | Must | Each change record classifies every in-scope surface. |
| REQ-0004-FR-0006 | Resumed, recovered, and uncommitted changes must be adopted or excluded according to their semantic owner, and a temporary branch, stash, or generated identity must not be fixed as current authority. | Must | Review of the change record shows each resumed change adopted or excluded by owner. |
| REQ-0004-FR-0007 | GitHub's label and code ownership projections must match the single affected-path owner, and missing, duplicate, or ambiguous routing must be validated. | Must | The label and code-owner validator reports no missing, duplicate or ambiguous route. |
| REQ-0004-FR-0008 | Platform validation results must distinguish the depth (syntax, render, schema/policy, product semantic, and live observation) and the tool, fallback, lane, and result. | Must | Validation output records depth, tool, fallback, lane and result. |
| REQ-0004-FR-0009 | An executable cloud example must carry guidance beside the example and provider-native static validation, and must be verifiable without credentials or apply/deploy. | Must | Example static validation passes without credentials or apply. |
| REQ-0004-FR-0010 | Ingress references, resource kinds, GitOps structure, policy, secret sync, and explicit local-only transport exceptions must be checked fail-closed. | Must | The fail-closed platform validators PASS; quality scenario Workload onboarding. |
| REQ-0004-FR-0011 | Platform assurance work must proceed in ordered per-package review, validation, and rollback units and must prove the final local-only integration. | Must | Each assurance package records review, validation and rollback before integration. |
| REQ-0004-FR-0012 | Exact infrastructure, workflow, dependency, and example versions must be confirmed from the executable source or a reviewed lock, and a Reference mirror must not be required as an execution precondition. | Must | Version checks read the executable source or reviewed lock. |
| REQ-0004-FR-0013 | The revision policy of the repository's own continuously reconciled source must be kept distinct from that of external release sources, and revisited when multiple operators or environments, or history rewriting, are introduced. | Must | The self-source revision rule differs from the external release pin rule and names its revisit triggers. |
| REQ-0004-FR-0014 | The Pod security enforcement level must be proportional to the workload evidence the repository owns and validates statically. Chart, injection, and runtime uncertainty is separated as audit/warn, and CNI desired state is not promoted to live evidence. | Must | Namespace Pod Security labels match the statically owned workload evidence. |
| REQ-0004-NFR-0001 | The local platform must provide the current integration scope of certificates, ingress, service mesh, observability UIs, progressive delivery, notifications, monitoring, and external secret integration. | Must | Acceptance criterion 01; quality scenarios Telemetry and Single-host recovery. |
| REQ-0004-NFR-0002 | Secret values, tokens, and private keys must not be recorded in Git, documents, or logs. | Must | Secret scanning finds no value in Git; quality scenario Secret TLS recovery. |
| REQ-0004-NFR-0003 | Image and artifact assurance must stay fail-closed without an unvalidated blanket digest conversion, and follow-on provenance obligations must be stated with a consumer, owner, and trigger. | Must | Image checks fail closed and each provenance follow-up names consumer, owner and trigger. |
| REQ-0004-IF-0001 | Historical records must be kept apart from current execution authority; a deleted or archived document is never used as current implementation guidance. | Must | Acceptance criterion 04. |

## Success / Acceptance Criteria

The current desired-state structure, Kubernetes syntax, and product static contract must pass their validators.
Delivery assurance must leave a classification, validation depth, result, and limits for every in-scope surface,
and does not substitute a static PASS for unobserved remote or runtime state. The per-member trace below states each acceptance condition and routes current architecture to AD-0007.

- **Acceptance criterion 01**: Validate the current platform product static contract.
- **Acceptance criterion 02**: Validate the GitOps ownership and reconciliation boundaries of root, platform, and workload.
- **Acceptance criterion 03**: Validate the syntax of tracked Kubernetes manifests.
- **Acceptance criterion 04**: Validate that current documents link current owners and not archived or deleted documents.
- **Acceptance criterion 05**: Review the six local product quality scenarios below against their named source, measurement boundary and owner. A repository-static result does not satisfy a live or external measurement.

### Product quality measurement boundary

The following scenarios are the product acceptance inputs the operator
approved with this Requirement on 2026-11-05; a TBD threshold stays open. A target is a decision threshold, not an
observed result. The public overviews of [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html),
[ISO/IEC 25023:2016](https://www.iso.org/standard/35747.html) and
[ISO/IEC 25030:2019](https://www.iso.org/standard/72116.html) inform the
distinction between product quality, measurement and requirements; they do not supply a universal
threshold or establish conformity. The accountable owner must record the
named revision, environment, sampling window, tool, result and missing
dependency before accepting a measurement. Static source inspection and
authorized live observation are separate rows of evidence.

### Quality scenario: GitOps reproducibility

At a reviewed repository revision, a platform engineer selects the affected
root/platform/workload targets and runs the current pinned render, schema and
product-reference validation contract once for that input. The response is a
renderable desired state with no unresolved required reference. The static
metric is **100 × valid selected targets / selected targets** (percent); the
proposed threshold is **100%** at the selected revision, with renderer version,
fallback and diagnostics recorded. If no target is selected, the result is
`NOT_APPLICABLE` with the actual selection reason, never a passing zero
denominator. The Platform Owner owns the static decision;
ArgoCD reconciliation at a named cluster is a separate operator observation.
This scenario refines REQ-0004-FR-0001, FR-0002 and FR-0008; [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md)
owns the render target and source paths.

### Quality scenario: Secret TLS recovery

After a named CA, certificate or external-secret failure, an approved
operator restores the affected service without exposing a secret value.
The static metric is **100 × resolved required TLS/ESO references / required
references in the selected manifests** (percent); the proposed source-contract
threshold is **100%**. With no applicable reference, the owner records
`NOT_APPLICABLE` and why rather than a passing zero denominator.
The sample is the affected cert-manager, ArgoCD, ESO and service-interface
references at a reviewed revision. Runtime recovery duration is measured
from the first recorded failure to the first recorded healthy service check
(minutes), but its acceptance threshold is **TBD by the Platform Owner and
Security Reviewer** for the named local-cluster incident class; it has not
been measured by this document. Only a separately authorized operator may
record the runtime sample, using status and metadata without secret values.
This scenario refines REQ-0004-FR-0003 and NFR-0002.

### Quality scenario: External interface

When a declared external endpoint changes, the Platform Owner compares the
Service/EndpointSlice name, address, port and protocol tuple, or for a
gateway-routed service (OpenBao, Prometheus, Grafana) the declared host,
port and CA, with the reviewed desired-state interface. The static metric is
**100 × matching required tuples / selected required tuples** (percent); the proposed threshold is
**100% of the selected required tuples**, with the selected target and
revision as the sampling frame. A selection with no required tuple is
`NOT_APPLICABLE` with a reason. Actual DNS, TLS, network reachability and
service response are a separate operator sample at the named cluster and
external service; the acceptable response rate and observation window are
**TBD by the Platform Owner and external-service owner** before live
acceptance. The tuple comparison does not assert that the external runtime
exists or responds. This scenario refines REQ-0004-FR-0003 and FR-0010.

### Quality scenario: Telemetry

After an authorized ArgoCD/Alloy change, the Observability Owner checks the
five declared ArgoCD component targets and `argocd_app_info` with the
`cluster="k3d-hyhome"` label in the external Prometheus. The metrics are
healthy declared ArgoCD targets (`up == 1`, targets) and present
`argocd_app_info` series (series); the local operational decision targets
are **five of five declared components** and **at least one labelled
application series**. The five ArgoCD component names and ports are part of the
`platform_pods` selector (which also selects argo-rollouts) in `gitops/platform/monitoring/alloy-k8s-logs.yaml`;
`prometheus.remote_write.external_prometheus` supplies the cluster label.
The sample is one recorded query set for the named cluster, external
Prometheus and post-reconciliation time window, repeated
on target or label changes. The current source can establish relabel and
remote-write configuration only; no query result or availability is
established here. This scenario refines REQ-0004-FR-0008 and NFR-0001;
[POL-0005](../05.operations/policies/0005-observability-platform-operations-policy.md)
routes the authorized checks.

### Quality scenario: Workload onboarding

For a new `apps` workload, the application author submits a fixed-image
Rollout, AnalysisTemplate, Service, Ingress, Kustomization and conditional
ExternalSecret, then the Platform Owner reviews its admission contract.
The static metric is **100 × matched applicable required artifact/control
checks / applicable required checks** (percent); the proposed threshold is
**100% for the selected workload**. The sample is each candidate workload
at its reviewed revision, excluding a justified optional ExternalSecret.
If there is no selected workload, record `NOT_APPLICABLE` and the reason;
do not report a passing zero denominator.
The current adminer example's 30-second analysis interval, four samples,
failure limit one and canary weights are component configuration, not a
platform-wide availability threshold. Actual Rollout health, ingress/TLS
and promotion require an approved operator's separate named-cluster sample;
their service-specific acceptance threshold is **TBD by the application
owner and Platform Owner**. This scenario refines REQ-0004-FR-0010,
FR-0014 and NFR-0001.

### Quality scenario: Single-host recovery

When the local host is rebuilt or a node fails, the Platform Owner first
checks the declared `servers: 1`, `agents: 3` k3d topology and bootstrap
inotify preflight, then an approved operator records the actual recovery.
The source metrics are declared server and agent counts (nodes) and the
configured bootstrap preflight minimum for
`fs.inotify.max_user_instances` (instances). The current source-contract
thresholds are **one server, three agents and a minimum of 512 instances**.
The actual host sysctl value is a separate operator preflight measurement
on the selected Linux host; source inspection cannot establish it. Recovery
duration is measured
from recorded start to a named healthy GitOps/platform check (minutes);
its target is **TBD by the Platform Owner** after a reviewed local-host
recovery plan and environment are named. One server is not a production HA
or failover claim. This scenario refines REQ-0004-FR-0001 and NFR-0001.

## Scope and Non-goals

In scope: the current local platform, the platform/workload separation, external service connections, onboarding examples, and local-only assurance.
Out of scope: creating the external runtime, cloud provisioning, unapproved cluster changes, and an unvalidated blanket digest conversion.

## Risks, Dependencies, and Assumptions

External services and actual cluster availability need separate preparation and observation. Updating this document is not live validation or deployment.
Reading secrets, pushing, cloud work, and live mutation each need separate approval.

### Delivery assurance coverage and limits

The repository checks structure, Kubernetes YAML, required policy tools, secret handling, the ESO/OpenBao boundary (the `vault-backend` ClusterSecretStore uses the Vault-API provider against OpenBao, ADR-0041) and product semantics. [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md), ADR-0043 and ADR-0050 own the current ingress architecture; `gitops/apps/root/platform-traefik-app.yaml` and `gitops/platform/ingress-routes/` own its desired state. SPEC-0104 closed the repository-static assurance of FR-0008 and FR-0010; the remaining custom CRD schema, generated-output and live-observation work has no active Spec and stays DEFER under the owners in the trace below. Git history recovers the withdrawn assurance Specs. The original REQ-0007 program history is kept; its current platform meaning passes to this document and its common routing, approval, and QA meaning to REQ-0003. This succession does not declare any tranche complete.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0004-FR-0001 | The selected root/platform/workload targets render at a reviewed revision (100% of selected targets). | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0002 | Static validation shows platform components and user workloads reconciled through separate projects with distinct destination and resource permissions. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0003 | Every declared external interface tuple or gateway host/port/CA matches the reviewed desired state. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0004 | Only the currently supported UIs have routes; no removed UI is described as current. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0005 | Every in-scope surface carries changed, unchanged-with-reason, or DEFER-with-owner-and-trigger. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0006 | No temporary branch, stash or generated identity is recorded as current authority. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0007 | The label and code-owner projections route each affected path to exactly one owner. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0008 | Each platform validation result names its depth, tool, fallback, lane and result. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md); custom CRD schemas and live observation remain DEFER with owners above |
| REQ-0004-FR-0009 | Each cloud example passes provider-native static validation with no credentials and no apply. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0010 | The ingress, resource-kind, GitOps, policy, secret-sync and transport checks fail closed and PASS. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md); generated and live outputs remain DEFER with owner above |
| REQ-0004-FR-0011 | The final local-only integration is proven after per-package review, validation and rollback. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0012 | Every pinned version is read from the executable source or a reviewed lock. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0013 | The self-source and external release revision rules are recorded separately with revisit triggers. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0014 | Enforced namespaces hold only statically validated workloads; the rest stay audit/warn. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0001 | The listed integrations are declared in the desired state and pass the product static contract. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0002 | No secret value, token or private key is found in Git, documents or logs. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0003 | No blanket digest conversion is made, and each provenance follow-up names consumer, owner and trigger. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-IF-0001 | Current documents link current owners only; no deleted or archived document is cited as guidance. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |

### Reviewed member-ID transfer

The table below records the succession of current meaning. Earlier member IDs are historical identifiers of the original decisions and program and are not reassigned.

| Original member ID | Current semantic owner |
| --- | --- |
| REQ-0007-FR-0001 | REQ-0004-FR-0005 |
| REQ-0007-FR-0002 | REQ-0004-FR-0006 |
| REQ-0007-FR-0003 | REQ-0004-FR-0007 / REQ-0003-FR-0016 |
| REQ-0007-FR-0004 | REQ-0003-FR-0017 |
| REQ-0007-FR-0005 | REQ-0004-FR-0008 |
| REQ-0007-FR-0006 | REQ-0004-FR-0010 |
| REQ-0007-FR-0007 | REQ-0004-FR-0009 |
| REQ-0007-FR-0008 | REQ-0003-FR-0028 |
| REQ-0007-FR-0009 | REQ-0003-FR-0007 |
| REQ-0007-FR-0010 | REQ-0004-FR-0011 / REQ-0003-FR-0018 / REQ-0003-FR-0019 |
| REQ-0007-FR-0011 | REQ-0004-FR-0012 |
| REQ-0007-FR-0012 | REQ-0004-FR-0013 |
| REQ-0007-FR-0013 | REQ-0004-FR-0014 |
| REQ-0007-NFR-0001 | REQ-0004-NFR-0003 |
| REQ-0007-NFR-0002 | REQ-0003-FR-0014 |

REQ-0004-FR-0009 also inherits the requirement of the former REQ-0005-FR-0006 (REQ-0005 was merged into REQ-0003; see its member-ID transfer and Archived Lineage) that examples sit beside their executable sources.

- Current architecture: [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md).
- Current desired state and validation: `gitops/`, `infrastructure/`, and `scripts/` as routed by [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md).
- Earlier delivery evidence: N/A — SPEC-0008 left the tree; Git history recovers it ([Archived Lineage](#archived-lineage)).
- Shared architecture: [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
- Current self-source and namespace decisions remain in the [decision log](../02.architecture/decisions/README.md).

### Archived Lineage

These documents were deleted from `docs/98.archive/` or `docs/03.specs/` under SPEC-0140 and are recovered with `git show 69445fca:<path>`. Paths below are the paths at that commit; a completed Spec path is its package directory (`spec.md`, `plan.md`, `tasks/`).

| Source | Kind | Summary | Original path |
| --- | --- | --- | --- |
| REQ-0001 (superseded) | superseded requirement | Initial product requirements for a WSL2 k3s/k3d multi-node platform with an ArgoCD GitOps pipeline and external Vault, PostgreSQL and Valkey; traceability was the success criterion. Status draft when archived; superseded by this document (2026-06-02). | `docs/98.archive/superseded/01.requirements/0001-wsl-k3d-argocd-platform.md` |
| REQ-0002 (superseded) | superseded requirement | 2026-03-28 HA platform requirements (1 master and 3 workers) integrating ArgoCD GitOps, ESO with Vault, external PostgreSQL and external Valkey. Status draft when archived; superseded by this document (2026-06-02). | `docs/98.archive/superseded/01.requirements/0002-wsl2-k3d-argocd-ha-platform.md` |
| REQ-0003 (superseded) | superseded requirement | 2026-03-29 platform expansion requirements for cert-manager, Headlamp, Istio and Kiali, and for aligning external-service contracts. Some early requirements (Dashboard) were already superseded by ADR-0010 Headlamp; the package was superseded by this document (2026-06-02). | `docs/98.archive/superseded/01.requirements/0003-platform-expansion-dashboard-mesh.md` |
| SPEC-0001 (superseded) | superseded spec | Early technical specification for the WSL k3d/k3s ArgoCD platform with ESO, Vault and external PostgreSQL/Valkey. Superseded by SPEC-0008 (2026-06-02). | `docs/98.archive/superseded/03.specs/0001-wsl-k3d-argocd-platform.md` |
| SPEC-0002 (superseded) | superseded spec | 2026-03-28 HA platform specification, extended with ArgoCD egress stability, least-privilege AppProjects and a CI static-contract gate. Superseded by SPEC-0008 (2026-06-02). | `docs/98.archive/superseded/03.specs/0002-wsl2-k3d-argocd-ha-platform.md` |
| SPEC-0003 (superseded) | superseded spec | Technical specification for cert-manager, Headlamp, Istio, Kiali and external-service endpoint contracts; its Dashboard and old network values were kept only as superseded history (current UI is Headlamp; current endpoints are owned by `gitops/platform/external-services/`). Superseded by SPEC-0008 (2026-06-02). | `docs/98.archive/superseded/03.specs/0003-platform-expansion.md` |
| OPS-0004 (superseded) | superseded operation | Guide to Headlamp authentication: anonymous mode, ServiceAccount token login and a staged move to Keycloak OIDC via GitOps. Superseded by the rollouts-notifications-headlamp runbook (`docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`) on 2026-06-02. | `docs/98.archive/superseded/05.operations/0004-headlamp-auth-oidc-guide.md` |
| OPS-0005 (superseded) | superseded operation | Runbook for Headlamp ServiceAccount login, Keycloak OIDC cut-over through ArgoCD, a Keycloak checklist and OIDC troubleshooting. Superseded by the same rollouts-notifications-headlamp runbook on 2026-06-02. | `docs/98.archive/superseded/05.operations/0005-headlamp-keycloak-runbook.md` |
| REQ-0007 (superseded) | superseded requirement | Bounded assurance path for GitHub automation, GitOps desired state, infrastructure examples, policy, scripts, tests, secret boundaries and Traefik dynamic configuration, complementing the local platform baseline. Active when archived (2026-09-05); its platform meaning passed to this document and its routing, approval and QA meaning to REQ-0003 (see the member-ID transfer tables). | `docs/98.archive/superseded/01.requirements/0007-repository-delivery-and-platform-assurance.md` |
| SPEC-0008 | completed spec | Completed implementation contract for the repo-backed local GitOps platform. Left active by SPEC-0084 on 2026-09-16; the 2026-10-03 closeout transferred current architecture and execution authority to AD-0007 and kept this package as a historical delivery record. | `docs/98.archive/completed/03.specs/0008-current-local-gitops-platform/` |
| SPEC-0060 | completed spec | Remediated six version-currency drift items found by the 2026-08-17 research refresh: four pinned images (adminer, grafana/alloy, rancher/k3s, kube-state-metrics) and two unpinned Helm charts (metallb, argo-cd). Completed; live-cluster verification stayed blocked and was not promoted. | `docs/98.archive/completed/03.specs/0060-platform-currency-defect-closure/` |
| SPEC-0061 | completed spec | Closed the workload security-context asymmetry: adminer declared no `securityContext` while kube-state-metrics and alloy-k8s-logs carried a common hardening pattern. Completed as a repository-static change; no scheduling or container-start outcome was claimed. | `docs/98.archive/completed/03.specs/0061-workload-security-context-baseline/` |
| SPEC-0104 | completed spec | Closed the repository-static assurance of REQ-0004-FR-0008 and REQ-0004-FR-0010: evidence classification, rendered-manifest and API-schema checks, and bounded ingress and resource-kind cross-reference checks. Completed as a static contract; it asserts no live readiness. | `docs/98.archive/completed/03.specs/0104-platform-validation-assurance/` |
| SPEC-0119 | completed spec | Centralized the ingress controller identity (class, namespace, Service, Application, annotation keys, NodePorts) that the platform validators spelled as literals, so a controller swap changes one place. No durable contract introduced; ADR-0050 owns the replacement decision. | `docs/03.specs/0119-ingress-controller-identity/` |
| SPEC-0121 | completed spec | Cut over from the retired ingress-nginx controller to Traefik (Kubernetes Ingress-NGINX provider only) under ADR-0050: ingress-nginx gave up IngressClass ownership and its webhook, routes were verified through Traefik and the router contract moved to Traefik. No durable contract introduced beyond ADR-0050. | `docs/03.specs/0121-traefik-ingress-cutover/` |
