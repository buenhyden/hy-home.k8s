---
title: "Current Local GitOps Platform Architecture Description"
version: "1.2.2"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "architecture"
artifact_id: "AD-0007"
---

# Current Local GitOps Platform Architecture Description (AD)

## Overview

이 문서는 현재 구현된 local GitOps platform의 참조 아키텍처를 정의한다.
old endpoint와 제거된 UI 계약은 archive Tombstone으로 분리하고, 현재 구조는 GitOps desired state와 static contract evidence를 기준으로 설명한다.

### Current architecture summary

현재 플랫폼은 Linux server의 native Docker Engine 위 k3d cluster, ArgoCD App-of-Apps, platform Application, workload ApplicationSet, external service interface contract로 구성된다.
아키텍처의 핵심 목표는 local reproducibility, GitOps-first ownership, secret-safe integration, and current-document traceability다.

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

이 AD는 AD-0010의 플랫폼 검증·interface·예제·source revision·namespace evidence 경계를 승계한다.
공통 affected-path/CI/승인/검토 의무는 [AD-0006](./0006-workspace-agent-governance-platform.md)와
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)가 함께 소유한다.
현재 플랫폼 요구의 member별 승계는 [REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md)에 명시한다.

| Surface or flow | Current source / implementation owner | Evidence boundary |
| --- | --- | --- |
| Desired-state tree | [root Application](../../../gitops/clusters/local/root-application.yaml), [root kustomization](../../../gitops/apps/root/kustomization.yaml) | Root → platform Applications / workload ApplicationSet의 정적 구조이며 live reconciliation 증거가 아님 |
| Local runtime and namespace policy | [k3d config](../../../infrastructure/k3d/k3d-cluster.yaml), [namespace declarations](../../../gitops/platform/namespaces/) | 저장소가 소유·정적으로 검증한 workload에만 enforce; chart/injection 불확실성은 audit/warn |
| Dispatch and GitHub projections | [Validation Registry](../../../scripts/validation/registry.json), [.github](../../../.github/) | Registry가 lane/argv owner; labels/CODEOWNERS native projections와의 parity는 Spec 0048의 미완료 범위 |
| Platform verification | [static contract checks](../../../scripts/validate-infrastructure-contracts.sh), [validators](../../../scripts/) | syntax → render → schema/policy → product semantic → live observation을 분리; 실제 root 수와 도구는 실행 source에서 도출 |
| Cloud examples | [AWS](../../../examples/aws/README.md), [Azure](../../../examples/azure/README.md) | Terraform/Bicep의 format/validate/lint/build; provider credential, apply 또는 deploy는 별도 승인 범위 |
| Local browser/service transport | [k8s router](../../../infrastructure/k3d/k3d-cluster.yaml), [apex redirects](../../../gitops/platform/ingress-routes/), [external service interfaces](../../../gitops/platform/external-services/) | k8s 전용 router(ADR-0043)와 local-only transport 예외를 검사하고 예외를 일반 보안 허용으로 확대하지 않음 |

Kubernetes GVK, k8s router 계약, GitOps 구조, 정책과 Vault/ESO source/secret 경계는 각각의
product validator가 소유한다. 도구 부재·malformed input·unsafe path·fallback에는 직접
negative fixture가 필요하며 required-tool 실패를 SKIP으로 숨기지 않는다.

정확한 chart, infrastructure, workflow, dependency와 example 버전은 executable source 또는
검토된 lock에 둔다. Stage 90 version mirror는 실행 선행조건이 아니다.
[ADR-0029](../decisions/0029-mutable-target-revision-retention.md)가 정한 자기 저장소
source의 `targetRevision: main`과 외부 chart의 exact revision을 구분하며, multi-operator,
multi-environment 또는 history rewrite 도입 시 branch 정책을 재검토한다.
Image는 현행 non-latest tag-or-digest 검사를 유지하고 확인 없는 blanket digest 변경을 하지 않는다.
추가 digest/SBOM/provenance 의무는 consumer, owner와 trigger를 갖는 승인된 후속 작업이다.
Istio CNI의 manifest는 desired state이며 실제 admission 또는 network 상태를 증명하지 않는다.

### Unfinished implementation owners

Spec 0049는 retired Spec 0048과 Traefik lane에 의존해 2026-09-25에 철회되었고([SPEC-0089](../../03.specs/0089-deferred-conflict-resolution/spec.md)), `98.archive/retired/`에 보존되어 인용하지 않는다([SPEC-0090](../../03.specs/0090-spec0049-retirement/spec.md)). 그 미구현 범위(render, schema, policy, secret, shell fixture, image, tool evidence lane)는 REQ-0004-FR-0008·FR-0010의 owner 없는 gap으로 남으며, 다음 owner는 현재 authority에서 새 package를 계획할 request owner다.
GitHub routing/CI(Spec 0048), native IaC/direct negative fixtures(Spec 0050),
최종 local-only integration(Spec 0051)과 surface/hunk 재조정(Spec 0047)은 후속 없이 철회되어
`98.archive/retired/`에 보존되었고([SPEC-0087](../../03.specs/0087-stage03-terminal-package-retention/spec.md)),
그 범위의 구현 owner는 현재 없다. AD 승계는 tranche 또는 WP-013 완료를 뜻하지 않는다.

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
- **Memory & Context Strategy**: Durable 실행 증거는 package-local Task에, 공통 규칙은 `.agents/governance/`에, 임시 checkpoint는 ignored recovery state에 둔다.
- **Guardrail Boundary**: Superseded/ended records are non-authoritative history; completed packages retain their own types under ADR-0038.
- **Latency / Cost Budget**: Not applicable to platform runtime.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0004-FR-0001](../../01.requirements/0004-current-local-gitops-platform.md) | clusters, root apps, platform 및 workloads desired-state root ownership | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-FR-0002](../../01.requirements/0004-current-local-gitops-platform.md) | App-of-Apps와 ApplicationSet reconciliation 경계 | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-FR-0003](../../01.requirements/0004-current-local-gitops-platform.md) | 외부 runtime과 Kubernetes Service/EndpointSlice interface의 분리 | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-FR-0004](../../01.requirements/0004-current-local-gitops-platform.md) | Headlamp current UI와 archived UI history의 분리 | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-NFR-0001](../../01.requirements/0004-current-local-gitops-platform.md) | 현재 platform component graph의 명시적 scope | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-NFR-0002](../../01.requirements/0004-current-local-gitops-platform.md) | ESO/Vault reference와 secret value의 trust boundary | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [REQ-0004-IF-0001](../../01.requirements/0004-current-local-gitops-platform.md) | active current contract와 archive Tombstone의 authority boundary | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | static contract verification이 소유하는 repo-backed evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | root, platform, workload 구조 검증 evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | tracked Kubernetes manifest syntax evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0004-current-local-gitops-platform.md) remains package-owned | repository quality gate의 active/archive currentness evidence | [ADR 0014](../decisions/0014-current-local-gitops-platform-contract.md) and [Spec 008](../../03.specs/0008-current-local-gitops-platform/spec.md) |

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
