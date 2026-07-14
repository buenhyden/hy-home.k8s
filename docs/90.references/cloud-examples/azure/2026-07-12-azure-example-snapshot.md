---
title: 'Azure Cloud Example Snapshot — 2026-07-12'
type: content/reference
status: draft
owner: platform
updated: 2026-07-13
---

# Azure Cloud Example Snapshot — 2026-07-12

## Overview

이 문서는 `examples/azure/docs/`의 33개 Azure 마이그레이션 문서에서 고유한
요구사항, 결정, 설계, 명령, 운영 지식을 하나의 Stage 90 reference로 합친다.
원래 기록은 2026-03-31 계획과 2026-05-09 지원 가정을 포함하고, 저장소
원문은 2026-07-12에 관찰했으며, Azure 공식 자료의 적용성은 2026-07-13
KST에 다시 확인했다.

이 스냅샷은 Azure subscription이나 AKS의 현재 상태를 증명하지 않는다.
원문 명령은 실행하지 않았고, subscription·cluster·credential·kubeconfig·
Key Vault secret·identity·database/cache·cost·network·Azure Monitor 상태를
읽거나 변경하지 않았다. 59개 전체 source manifest SHA-256은
`2ed87a48e9b62da9e16f904f0bbe2ebdf3f1ebaef5be55fdcf06b1608c3a315b`이며,
이 문서의 Azure 부분은 그중 정확히 33개를 대상으로 한다.

## Reference Type

이 문서는 dated cloud-example consolidation snapshot이다. 다음 증거 층을
구분해 보존하며, 역사적 예시와 현재 공식 검토 기준을 합성해 새로운
provider-latest 배포 계약을 만들지 않는다.

| Evidence label | Meaning |
| --- | --- |
| **Retained source fact** | 2026-03/05 예시의 목표·결정·가정·상태·명령. 현재 사실이나 실행 승인이 아니다. |
| **Official check** | 2026-07-13 KST Azure 공식 자료에서 확인한 검토 기준. live 환경 증거가 아니다. |
| **Inference / gap** | 원문 사이의 충돌, 공식 자료와의 drift, 또는 원문이 답하지 않는 항목. 구현 계약이 아니다. |

## Authority Boundary

이 문서는 33개 삭제 후보의 지식 보존, 공식 자료 적용성, 실행 자산 매핑,
stale/conditional 판단과 refresh trigger를 소유한다. 실제 Azure architecture
승인, 지원 version/SKU/region, subscription/RBAC, Bicep deployment, AKS 접근,
AGC/identity/Key Vault/HA 구성, forced failover, node-pool 변경, 비용·SLO 달성은
소유하지 않는다. 현재 로컬 desired state의 정본은 `gitops/`이고, 실행 가능한
Azure 예시는 `examples/azure/infrastructure/`, `examples/azure/gitops/`,
`examples/azure/kubernetes/`에 남는다.

아래 command payload는 역사적 검토 증거다. 현재 공식 절차, version,
prerequisite, impact, placeholder, RBAC, rollback과 사람 승인을 다시 확인하기
전에는 copy/paste authority가 아니다. `az aks nodepool add/delete/scale/update`,
`kubectl drain`, PostgreSQL forced failover/restart는 명백한 operator-only mutation이다.

## Scope

다음 표가 Azure source coverage의 정본이다. `M`은 “이 스냅샷으로 merge;
독립 보존성 검토와 삭제 승인 전까지 원문 유지”를 뜻한다. Frontmatter가 없는
README type은 `README index`로 기록한다. Asset 열의 `B1`–`B14`는 아래 실행
자산 표와 연결된다.

| ID | Source path | Source title / type | Retained unique knowledge and boundary | Executable mapping | Disposition |
| --- | --- | --- | --- | --- | --- |
| S01 | `examples/azure/docs/01.requirements/2026-03-31-azure-migration-prd.md` | Azure Migration Product Requirements Document / `sdlc/prd` | platform/developer/SRE personas, CNI Overlay/AGC/managed data/Workload Identity requirements, 99.9% goal, cost/network/permission risks and non-goals | B1–B14 | M |
| S02 | `examples/azure/docs/01.requirements/2026-03-31-azure-migration.md` | Azure Migration PRD (Product Requirements Document) / `sdlc/prd` | local k3d/Vault/PostgreSQL/Valkey/observability audit, 2026-05-09 AKS/AGC/passwordless/CSI target, FR/NFR and acceptance criteria | B1–B14 | M |
| S03 | `examples/azure/docs/01.requirements/README.md` | 01.requirements (Product Requirements Document) / `README index` | PRD inventory, 2026-03-31 source date, 2026-07-12 observation, refresh/succession and static-evidence boundary | B1–B14 | M |
| S04 | `examples/azure/docs/02.architecture/decisions/0001-cni-overlay.md` | ADR-0001: Azure CNI Overlay for AKS Networking / `sdlc/adr` | overlay IP-efficiency decision, node/VNet versus Pod address behavior, Azure CNI node-IP and Kubenet alternatives, external Pod-IP limitation | B2, B3, B7, B10 | M |
| S05 | `examples/azure/docs/02.architecture/decisions/0002-agc-gateway-api.md` | ADR-0002: Azure Application Gateway for Containers (AGC) with Gateway API / `sdlc/adr` | AGC/Gateway API/ALB Controller decision, AGIC and Nginx alternatives, routing expressiveness and learning trade-off | B4, B7, B10 | M |
| S06 | `examples/azure/docs/02.architecture/decisions/0003-workload-identity.md` | ADR-0003: Azure Workload Identity for Passwordless Auth / `sdlc/adr` | ServiceAccount-to-managed-identity federation, DefaultAzureCredential, rejection of AAD Pod Identity and static keys, local-test trade-off | B1, B8, B9, B11, B12, B14 | M |
| S07 | `examples/azure/docs/02.architecture/decisions/0004-postgresql-flexible-ha.md` | ADR-0004: PostgreSQL Flexible Server HA / `sdlc/adr` | PostgreSQL 16 Flexible/ZoneRedundant/AzureAD/private decision, Azure SQL and Single Server alternatives, cost/latency/failover consequences | B5, B13 | M |
| S08 | `examples/azure/docs/02.architecture/decisions/2026-03-31-adr-agc-selection.md` | ADR-0001: Selection of Azure Application Gateway for Containers (AGC) / `sdlc/adr` | duplicate AGC decision lineage, Gateway role separation, Standard App Gateway and Nginx alternatives, unverified 30k-rps claim and cost trade-off | B4, B7, B10 | M |
| S09 | `examples/azure/docs/02.architecture/decisions/README.md` | 02.architecture/decisions (Architecture Decision Records) / `README index` | five-ADR inventory and context/alternative/consequence traceability contract | B2–B12 | M |
| S10 | `examples/azure/docs/02.architecture/requirements/0001-azure-migration-architecture.md` | Azure Migration ARD (Architecture Reference Document) / `sdlc/ard` | AKS/AGC/managed data/Key Vault boundaries, CNI Overlay, Workload Identity, Bicep/Argo CD and Azure Monitor/Log Analytics model | B1–B14 | M |
| S11 | `examples/azure/docs/02.architecture/requirements/2026-03-31-azure-migration-ard.md` | Azure Kubernetes Service Reference Architecture (ARD) / `sdlc/ard` | single-region HA, Gateway API, managed Prometheus/Grafana, private data access, Ubuntu/AKS target and no multi-region/legacy-VM scope | B1–B14 | M |
| S12 | `examples/azure/docs/02.architecture/requirements/README.md` | 02.architecture/requirements (Architecture Reference Document) / `README index` | two-ARD inventory, architecture scope and provider-static refresh boundary | B1–B14 | M |
| S13 | `examples/azure/docs/03.specs/2026-03-31-resource-specs.md` | Azure Migration Technical Specification / `sdlc/spec` | naming/tags, VNet/subnet CIDRs, AKS pools/SKUs, AGC HTTPRoute-only interface, PostgreSQL/Redis sizing, data migration and verification | B1–B14 | M |
| S14 | `examples/azure/docs/03.specs/README.md` | 03.specs (Technical Specification) / `README index` | two-Spec inventory, implementation-versus-live boundary and succession rule | B1–B14 | M |
| S15 | `examples/azure/docs/03.specs/azure-migration/spec.md` | Azure Migration Technical Specification / `sdlc/spec` | AKS/AGC/Gateway/WI/CSI/PostgreSQL/Redis standards, local replacement map, sandbox/error/escalation boundaries | B1–B14 | M |
| S16 | `examples/azure/docs/04.execution/plans/2026-03-31-azure-migration.md` | Azure Migration Implementation Plan / `sdlc/plan` | M1–M5 dated milestones, infrastructure/platform phases, only design marked complete, provider drift/cost/IAM risk | B1–B14 | M |
| S17 | `examples/azure/docs/04.execution/plans/2026-03-31-migration-strategy.md` | Azure Migration Strategy (Phase 1) / `sdlc/plan` | four weekly phases, hybrid cutover then local shutdown, one-hour transition target, passwordless goal and sandbox-only completion | B1–B14 | M |
| S18 | `examples/azure/docs/04.execution/plans/README.md` | 04.execution/plans (Implementation Plans) / `README index` | two-plan inventory and plan/task refresh contract | B1–B14 | M |
| S19 | `examples/azure/docs/04.execution/tasks/0001-aks-cluster-provisioning.md` | Task: AKS Cluster Provisioning / `sdlc/task` | five unchecked Bicep/resource-group/deployment/node/kubeconfig tasks, 15-minute and no-SSH expectations, no-live rule | B1–B6 | M |
| S20 | `examples/azure/docs/04.execution/tasks/2026-03-31-migration-tasks.md` | Task: Azure Migration Implementation / `sdlc/task` | docs Done; Bicep, managed data, AGC, identity, secret, ops docs and README validation Todo; what-if/dry-run rules | B1–B14 | M |
| S21 | `examples/azure/docs/04.execution/tasks/README.md` | 04.execution/tasks (Execution Tasks) / `README index` | task inventory, evidence expectations and succession boundary | B1–B14 | M |
| S22 | `examples/azure/docs/05.operations/guides/0001-azure-onboarding-guide.md` | Azure Onboarding Guide / `sdlc/guide` | CLI/kubectl prerequisites, login/temp kubeconfig, WI label, CSI mount/sync, GitOps flow and troubleshooting | B7–B14 | M |
| S23 | `examples/azure/docs/05.operations/guides/2026-03-31-azure-deployment-guide.md` | Azure AKS Deployment & Onboarding Guide / `sdlc/guide` | Bicep what-if, temporary kubeconfig, Helm render, manifest diff/status checks, parameter/identity propagation pitfalls | B1–B14 | M |
| S24 | `examples/azure/docs/05.operations/guides/README.md` | 05.operations/guides (User Guides & How-to) / `README index` | two-guide inventory, onboarding audience and no-live evidence boundary | B1–B14 | M |
| S25 | `examples/azure/docs/05.operations/policies/2026-03-31-azure-ops-policy.md` | Azure Infrastructure Operations Policy / `sdlc/policy` | Bicep/passwordless/zone-HA controls, no public DB/root secret/0.0.0.0/0, emergency/vendor exceptions and quarterly review | B1–B14 | M |
| S26 | `examples/azure/docs/05.operations/policies/README.md` | 05.operations/policies (Operational Policies) / `README index` | three-policy inventory, policy scope, evidence and refresh boundary | B1–B14 | M |
| S27 | `examples/azure/docs/05.operations/policies/azure-cost-optimization.md` | Azure 비용 최적화 및 거버넌스 정책 / `sdlc/policy` | right-sizing, dev/test Spot, autoscaler, Burstable data, Dev 3/Prod 30-day retention examples and cost tags | B1–B14 | M |
| S28 | `examples/azure/docs/05.operations/policies/azure-maintenance-policy.md` | Azure Maintenance & Operations Policy / `sdlc/policy` | third-Sunday KST window, NodeImage cadence, 7-day PITR, alert thresholds, Bicep/GitOps change policy and KPI targets | B1–B14 | M |
| S29 | `examples/azure/docs/05.operations/runbooks/0001-disaster-recovery.md` | Azure Disaster Recovery Runbook / `sdlc/runbook` | region/data/security scenarios, RTO 1h/RPO 5m targets, AKS/PG/Key Vault recovery, 48-hour postmortem and escalation | B1–B14 | M |
| S30 | `examples/azure/docs/05.operations/runbooks/2026-03-31-fault-tolerance-runbook.md` | Azure Infrastructure Fault Tolerance Runbook / `sdlc/runbook` | node/PG/AGC diagnosis and operator-only mutations, readiness/DNS/FQDN verification, Monitor/activity evidence and GitOps rollback | B1–B14 | M |
| S31 | `examples/azure/docs/05.operations/runbooks/README.md` | 05.operations/runbooks (Operational Runbooks) / `README index` | three-runbook inventory, incident handoff and evidence boundary | B1–B14 | M |
| S32 | `examples/azure/docs/05.operations/runbooks/aks-node-replacement.md` | AKS 노드 풀 교체 및 규모 조정 절차 / `sdlc/runbook` | node-pool add/drain/delete/scale/autoscaler payloads, sandbox-only use and evidence/rollback boundary | B2, B3 | M |
| S33 | `examples/azure/docs/README.md` | Azure Migration Documentation Hub / `README index` | full nine-stage inventory, AKS/Bicep/AGC/data/security stack snapshot, Tech Stack Inventory SSoT and no-provider-latest boundary | B1–B14 | M |

Coverage arithmetic is exact: two PRDs, five ADRs, two ARDs, two Specs, two
Plans, two Tasks, two Guides, three Policies, three Runbooks, and ten README
indexes equal 33 rows. Each source path appears once in the coverage table, and
all 33 retain disposition `M` pending deletion review.

## Definitions / Facts

**Dated product intent and local baseline.** Retained source facts describe
moving a resource-constrained local k3d/k3s environment to AKS while keeping
GitOps. The local comparison recorded MetalLB/Ingress-Nginx or Traefik, Vault,
PostgreSQL at `172.18.0.15:15432/3`, Valkey at `172.18.0.9:6379`, and a
Prometheus/Alloy/Loki/Tempo/Grafana stack. The target goals were CNI Overlay,
AGC/Gateway API, Workload Identity, Key Vault/CSI, managed PostgreSQL/Redis,
Bicep and 99.9% availability. Application business-logic rewrite, a full
legacy-data migration tool and exact one-for-one local replication were
non-goals. Cost, latency, subscription ownership and RBAC were explicit risks.

**Retained decisions, alternatives and consequences.** Azure CNI Overlay was
selected for VNet-IP efficiency; node-assigned Azure CNI and Kubenet remain
documented alternatives, while direct external Pod-IP access remains excluded.
Two separately authored ADRs select AGC, Gateway API and ALB Controller over
AGIC/Standard Application Gateway and in-cluster Nginx; their duplicate ADR-0001
lineage and unverified 30,000-requests/sec claim are retained as provenance, not
facts. Workload Identity/OIDC federation and DefaultAzureCredential replace
AAD Pod Identity and static keys. PostgreSQL Flexible Server 16 with
ZoneRedundant HA, AzureAD authentication and private networking was selected
over Azure SQL and legacy Single Server, with doubled-HA-cost and same-region
latency trade-offs.

**Architecture and interface contracts.** The resource Spec records VNet
`10.200.0.0/16`, AKS subnet `10.200.0.0/22`, dedicated AGC subnet
`10.200.4.0/24` and database subnet `10.200.5.0/24`; `HTTPRoute` is the intended
external API interface. Historical AKS assumptions include 1.35 target,
Standard tier, two-node system and autoscaled 3–10-node user pools, CNI Overlay,
Workload Identity and private managed data. Bicep owns modular infrastructure;
Argo CD owns pull-based application deployment. The two ARDs preserve Azure
Monitor/Log Analytics or managed Prometheus/Grafana observability alternatives
and explicitly scope the design to single-region HA rather than multi-region DR.

**Historical plan and task state.** The dated milestone plan marks only M1
Design complete; infrastructure, platform, workload and verification milestones
remain unchecked. The four-week strategy describes foundations, managed
services, application cutover and stabilization, including a one-hour transition
target and eventual local shutdown. The provisioning task keeps all five live
steps unchecked; the implementation task marks docs complete but Bicep, managed
data, AGC, identity, secret, operations and final indexing Todo. These are
historical planning states, not evidence that Azure resources exist.

**Operations, SLO and recovery knowledge.** Retained policy includes Bicep and
GitOps change control, passwordless identity, private data, zone HA, tagging,
quarterly review and emergency rollback/reporting. The maintenance snapshot sets
third-Sunday 02:00–05:00 KST work, weekly NodeImage review, 7-day PostgreSQL PITR,
CPU/memory >85%, AGC 5xx >1%, Key Vault denial >5%, 99.9% availability and
100 ms AGC-latency targets. A cost policy separately gives Dev 3-day/Prod 30-day
retention examples; this conflicts with the 7-day default and must be resolved
per environment. DR preserves AKS-region, data-loss and compromise scenarios,
RTO 1 hour, RPO 5 minutes, PITR/Key Vault soft-delete steps, escalation and a
48-hour postmortem requirement. Those values are unverified objectives, not
measured guarantees. Node replacement, drain, scale and forced PostgreSQL
failover remain operator-only.

**Executable owner mapping.** All fourteen tracked Azure assets existed at the
observation baseline and remain outside the documentation deletion set.

| Asset ID | Retained executable owner | Knowledge mapped to it | Currentness boundary |
| --- | --- | --- | --- |
| B1 | `examples/azure/infrastructure/main.bicep` | module orchestration, Key Vault RBAC, managed identity and federation outputs | Validate resource APIs, role IDs, public access and deployment parameters. |
| B2 | `examples/azure/infrastructure/network.bicep` | VNet, AKS/AGC/database subnets, delegation and NSG | Recheck overlay/AGC dedicated-subnet constraints and inbound exposure. |
| B3 | `examples/azure/infrastructure/aks.bicep` | AKS 1.35, CNI Overlay, Azure network policy, OIDC and Workload Identity | Validate version support; current guidance favors Cilium over legacy NPM paths. |
| B4 | `examples/azure/infrastructure/agc.bicep` | Traffic Controller, association, dedicated subnet and frontend | Recheck AGC/controller API versions, support and region availability. |
| B5 | `examples/azure/infrastructure/database.bicep` | PostgreSQL 16, Entra-only auth, ZoneRedundant HA and 32 GB example | Preview API/Burstable/HA combination, PITR and failover require current validation. |
| B6 | `examples/azure/infrastructure/redis.bicep` | Premium Redis, TLS/private endpoint and memory policy | Recheck product lifecycle, SKU, private DNS and replacement guidance. |
| B7 | `examples/azure/gitops/platform/gateway.yaml` | HTTPS Gateway/HTTPRoute and certificate reference | Validate GatewayClass, AGC annotations, namespace and certificate ownership. |
| B8 | `examples/azure/gitops/platform/managed-identity.yaml` | historical identity binding intent | Uses legacy AAD Pod Identity APIs rejected by S06; do not promote without replacement. |
| B9 | `examples/azure/gitops/platform/secret-provider-class.yaml` | Key Vault CSI objects and Kubernetes Secret synchronization | Placeholder tenant and secret-sync exposure require policy review. |
| B10 | `examples/azure/kubernetes/manifests/agc-gateway.yaml` | AGC Gateway/HTTPRoute application example | Placeholder controller ID and HTTP listener require current security review. |
| B11 | `examples/azure/kubernetes/manifests/external-secrets-azure.yaml` | ESO Workload Identity and Key Vault synchronization | Validate ESO API, vault URL, service account and whether K8s Secret materialization is allowed. |
| B12 | `examples/azure/kubernetes/manifests/external-services-azure.yaml` | PostgreSQL/Redis ExternalName and historical Vault endpoint wiring | Vault endpoint conflicts with Key Vault migration direction; classify before reuse. |
| B13 | `examples/azure/kubernetes/manifests/workload-identity.yaml` | ServiceAccount and federated-identity intent | Placeholder client/issuer and nonstandard in-cluster credential kind need validation. |
| B14 | `examples/azure/kubernetes/sample-app.yaml` | workload label, Key Vault CSI mount and managed data endpoints | Placeholder identity/tenant/image and secret synchronization are sandbox-only. |

**Preserved fenced command groups.** The source pack contains exactly sixteen
Azure Bash fences. Each group is represented below without claiming execution.

| Group | Source ID | Preserved payload summary | Classification |
| --- | --- | --- | --- |
| C-AZ-01 | S13 | `az deployment group what-if`, `kubectl get nodes -o wide`, and AGC-controller Pod query | Render/read-oriented but requires approved provider/cluster context. |
| C-AZ-02 | S13 | comments requiring sandbox, placeholder and official-doc refresh | Guard-only fence; no executable operation. |
| C-AZ-03 | S15 | comments requiring sandbox, placeholder and official-doc refresh | Guard-only fence; no executable operation. |
| C-AZ-04 | S22 | `az login --tenant` and `az account set --subscription` | Authentication/context mutation; credential-safe operator approval required. |
| C-AZ-05 | S22 | temporary kubeconfig via `az aks get-credentials --file` and node query | Provider/cluster access; temporary file does not remove authorization needs. |
| C-AZ-06 | S23 | multi-line `az deployment group what-if` with resource group, template and placeholder admin parameters | Preview only; provider access, PII and parameter review required. |
| C-AZ-07 | S23 | temporary kubeconfig plus node query | Provider/cluster access; not executed here. |
| C-AZ-08 | S23 | `helm template` for ALB Controller into `/tmp` | Local render; chart/version/source must be refreshed. |
| C-AZ-09 | S23 | `kubectl diff` for identity/secrets manifests and ExternalSecret readiness query | Cluster access; never print secret values. |
| C-AZ-10 | S30 | `az aks nodepool update ... --node-count 5` | Live node-pool mutation; operator-only. |
| C-AZ-11 | S30 | `az postgres flexible-server restart ... --failover Forced` | Disruptive forced failover; incident approval and current procedure required. |
| C-AZ-12 | S32 | `az aks nodepool add` with VM size and count | Live capacity/cost mutation; operator-only. |
| C-AZ-13 | S32 | `kubectl drain ... --delete-emptydir-data` | Workload disruption and ephemeral-data loss risk; operator-only. |
| C-AZ-14 | S32 | `az aks nodepool delete` | Destructive live mutation; rollback and workload proof required. |
| C-AZ-15 | S32 | `az aks nodepool scale` | Live capacity/cost mutation; operator-only. |
| C-AZ-16 | S32 | `az aks nodepool update --enable-cluster-autoscaler --min-count 2 --max-count 10` | Live autoscaling-policy mutation; operator-only. |

Additional inline historical payload includes Bicep build/lint/what-if,
`kubectl get/diff/describe/logs`, Gateway/HTTPRoute/SecretProviderClass queries,
`az postgres flexible-server show`, Entra-token `psql`, `nslookup`, `curl`,
Azure Resource Graph/activity-log checks and `argocd app rollback`. These retain
the intended evidence categories only; none is asserted current or executed.

**Currentness findings.** Azure Linux 2.0 support ended 2025-11-30 and its AKS
node images were removed 2026-03-31, so any such dated assumption is stale.
Current official network-policy guidance favors Cilium and treats Azure NPM as
legacy; the source claim of complete Azure Network Policy integration and B3's
`networkPolicy: azure` require redesign review. AGC with Overlay requires current
controller/support checks and a dedicated subnet. B8 retains legacy AAD Pod
Identity even though S06 rejects it. PostgreSQL HA/PITR/failover behavior and
forced failover limitations remain conditional; HA does not itself prove the
one-hour RTO or five-minute RPO.

## Sources

Local evidence consists of the 33 rows above, the immutable source manifest,
the source-inspection artifact, and the durable migration ledger. Official
links below are direct provider-primary review inputs observed 2026-07-13 KST.

| Official primary source | Applicability to retained facts | Rejected / conditional guidance | Refresh trigger |
| --- | --- | --- | --- |
| [AKS baseline architecture](https://learn.microsoft.com/en-gb/azure/architecture/reference-architectures/containers/aks/baseline-aks) | Architecture, security and operations review baseline. | Does not certify this example or live AKS. | Baseline architecture or supported topology changes. |
| [Azure CNI Overlay](https://learn.microsoft.com/en-us/azure/aks/azure-cni-overlay) | Overlay constraints, version support and Azure Linux warning basis. | Azure Linux 2.0 assumptions are stale. | Overlay requirements, OS support or scale limits change. |
| [AKS networking best practices](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-network) | VNet/subnet/operator design review. | Frozen CIDRs and policies are not universal defaults. | Network design, egress or private-cluster guidance changes. |
| [Application Gateway for Containers](https://learn.microsoft.com/en-us/azure/application-gateway/for-containers/) | AGC capability and support boundary. | Does not prove controller, region or subscription readiness. | AGC APIs, controller or feature support changes. |
| [AGC networking](https://learn.microsoft.com/en-us/azure/application-gateway/for-containers/container-networking) | Overlay/controller/dedicated-subnet review. | Dated AGC design is conditional on current prerequisites. | Delegation, subnet or controller requirements change. |
| [AKS Workload Identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview) | Passwordless workload identity review basis. | No federated credential or live identity was verified. | OIDC, labels, SDK or supported-version guidance changes. |
| [CSI/Key Vault identity access](https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-identity-access) | Secret-store identity and CSI boundary. | Does not approve K8s Secret synchronization or expose values. | CSI driver, identity or access-model guidance changes. |
| [PostgreSQL Flexible Server HA](https://learn.microsoft.com/en-us/azure/postgresql/high-availability/concepts-high-availability) | HA, PITR and failover limitation review. | HA/RPO/RTO remain workload- and region-dependent; forced failover is operator-only. | HA modes, backup, PITR or failover behavior changes. |
| [AKS upgrade options](https://learn.microsoft.com/en-us/azure/aks/upgrade-options) | Supported upgrade-path review. | Dated 1.35 target is not certified by this snapshot. | Kubernetes support calendar or upgrade paths change. |
| [Resize AKS node pools](https://learn.microsoft.com/en-us/azure/aks/resize-node-pool) | Current node resize/replacement review. | Historical add/delete/drain commands are not approved procedure. | Resize, migration or node-image procedure changes. |
| [Monitor AKS](https://learn.microsoft.com/en-us/azure/aks/monitor-aks) | Monitoring surface review. | No workspace, alert or metric was observed. | AKS monitoring integration changes. |
| [Container monitoring practices](https://learn.microsoft.com/en-us/azure/azure-monitor/containers/best-practices-containers) | Observability and cost review. | Frozen thresholds are objectives, not evidence. | Collection, retention or cost guidance changes. |
| [AKS cost optimization](https://learn.microsoft.com/en-us/azure/aks/optimize-aks-costs) | Conditional autoscaling/Spot/right-sizing review. | “90% saving” is not a quote or guarantee. | Pricing model or cost-control guidance changes. |
| [AKS network policy best practices](https://learn.microsoft.com/en-us/azure/aks/network-policy-best-practices) | Cilium preference and legacy NPM boundary. | Azure NPM-oriented assumptions are historical. | Supported policy engines or migration guidance changes. |

## Review and Freshness

Refresh this document when the source manifest, any of B1–B14, durable-ledger
destination, provider README inventory, AKS/Kubernetes/OS support, Bicep resource
APIs, CNI/policy engine, AGC/controller, Workload Identity/CSI/ESO, PostgreSQL
HA/PITR, Redis product lifecycle, node replacement, observability, cost/retention
assumptions, or any cited official page materially changes.

Before deletion, an independent reviewer must prove that the 33-row source set,
16 Bash groups, every ADR alternative/consequence, dated requirement and plan
status, RTO/RPO, rollback, observability fact and README succession boundary is
represented. Before live use, an operator must establish current subscription,
region/SKU/quota, RBAC, identity, cost, network, backup/PITR, RPO/RTO, rollback
and monitoring evidence. Credentials, secret values, kubeconfigs and sensitive
provider output must remain outside the repository.

## Related Documents

- [Azure snapshot index](README.md)
- [Cloud example reference collection](../README.md)
- [Azure executable example entrypoint](../../../../examples/azure/README.md)
- [Tech Stack Version Inventory](../../data/tech-stack-version-inventory.md)
- [Authored Document Migration Spec](../../../03.specs/030-authored-document-migration/spec.md)
