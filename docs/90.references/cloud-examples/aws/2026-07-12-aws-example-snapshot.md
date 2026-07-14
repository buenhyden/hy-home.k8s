---
title: 'AWS Cloud Example Snapshot — 2026-07-12'
type: content/reference
status: draft
owner: platform
updated: 2026-07-13
---

# AWS Cloud Example Snapshot — 2026-07-12

## Overview

이 문서는 `examples/aws/docs/`에 분산되어 있던 26개 AWS 마이그레이션
문서의 고유 지식을 하나의 검토 가능한 Stage 90 reference로 합친다. 원래
기록은 주로 2026-03-31 계획과 2026-05-09 지원 가정을 담고 있고, 저장소
원문은 2026-07-12에 관찰했으며, 공식 AWS 자료의 적용성은 2026-07-13
KST에 다시 확인했다.

이 스냅샷은 AWS 계정이나 EKS 클러스터의 현재 상태를 증명하지 않는다.
원문 명령은 실행하지 않았고, 스냅샷 작성 중 계정·클러스터·자격 증명·
시크릿·비용·네트워크·데이터베이스·캐시·Argo CD 상태를 읽거나 바꾸지
않았다. 59개 전체 source manifest의 SHA-256은
`2ed87a48e9b62da9e16f904f0bbe2ebdf3f1ebaef5be55fdcf06b1608c3a315b`이며,
이 문서의 AWS 부분은 그중 정확히 26개를 대상으로 한다.

## Reference Type

이 문서는 dated cloud-example consolidation snapshot이다. 요구사항, 결정,
아키텍처, 명세, 계획, 작업, 가이드, 정책, 런북, README 인벤토리를
중복 제거해 보존하되 다음 세 증거 층을 섞지 않는다.

| Evidence label | Meaning |
| --- | --- |
| **Retained source fact** | 2026-03/05 예시 문서에 기록된 목표·가정·결정·명령·상태. 현재 사실로 승격하지 않는다. |
| **Official check** | 2026-07-13 KST에 확인한 AWS 공식 문서의 현재 검토 기준. 저장소 예시가 실제로 배포됐다는 증거가 아니다. |
| **Inference / gap** | 원문과 공식 자료를 비교해 도출한 재검토 필요성 또는 원문이 답하지 않는 항목. 구현 계약이 아니다. |

## Authority Boundary

이 스냅샷이 소유하는 것은 삭제 후보 원문의 추적 가능한 지식 보존,
공식 자료 적용성 분류, 실행 자산과 문서 결정의 매핑, refresh trigger다.
실제 AWS 아키텍처 승인, 지원 버전 확정, 비용 산정, 계정/IAM 구성,
Terraform apply, EKS 접근, 복구 실행, 시크릿 값, 런타임 건강 상태는 소유하지
않는다. 현재 로컬 desired state의 정본은 `gitops/`에 남고, 실행 가능한 AWS
예시는 `examples/aws/terraform/`과 `examples/aws/kubernetes/`에 남는다.

아래 명령 payload는 역사적 검토 증거다. placeholder 치환, 현재 CLI/API와
공식 절차 재검토, 승인된 provider sandbox, 최소 권한, rollback, 사람 승인이
모두 갖춰지기 전에는 실행 권한이나 copy/paste runbook으로 사용할 수 없다.
특히 kubeconfig·IAM identity·RDS restore·GitOps diff는 민감한 provider 또는
cluster context에 닿을 수 있다.

## Scope

다음 표가 AWS source coverage의 정본이다. `M`은 “이 스냅샷으로 merge;
독립 보존성 검토와 삭제 승인이 끝날 때까지 원문 유지”를 뜻한다. README는
Frontmatter가 없으므로 type을 `README index`로 기록한다. Asset 열의 `A1`–`A8`
식별자는 아래 실행 자산 표와 연결된다.

| ID | Source path | Source title / type | Retained unique knowledge and boundary | Executable mapping | Disposition |
| --- | --- | --- | --- | --- | --- |
| S01 | `examples/aws/docs/01.requirements/2026-03-31-aws-migration-prd.md` | AWS Migration Product Requirements Document / `sdlc/prd` | personas, managed-service use cases, 99.9% SLO, Multi-AZ/IaC goals, AWS-only and no-app-rewrite boundaries | A1–A8 | M |
| S02 | `examples/aws/docs/01.requirements/README.md` | 01.requirements (Product Requirements Document) / `README index` | PRD inventory, 2026-03-31 source date, 2026-07-12 observation, refresh/succession and no-live evidence boundary | A1–A8 | M |
| S03 | `examples/aws/docs/02.architecture/decisions/0001-aws-managed-services-selection.md` | ADR-0001: AWS Managed Services and Compute Strategy Selection / `sdlc/adr` | EKS/Karpenter, Aurora Serverless v2, ElastiCache Serverless, Secrets Manager/ESO decision; self-managed EC2 and managed-node-group alternatives; lock-in/learning trade-offs | A2, A4, A6–A8 | M |
| S04 | `examples/aws/docs/02.architecture/decisions/2026-03-31-replace-vault-with-secrets-manager.md` | ADR-001: Replace Local Vault with AWS Secrets Manager for AWS Environment / `sdlc/adr` | AWS-example-only Vault replacement, ESO synchronization, retained Vault and Parameter Store alternatives, rotation/IAM benefits and dual-tooling cost | A5, A6 | M |
| S05 | `examples/aws/docs/02.architecture/decisions/README.md` | 02.architecture/decisions (Architecture Decision Records) / `README index` | decision inventory and context/alternative/consequence traceability contract | A2, A4–A8 | M |
| S06 | `examples/aws/docs/02.architecture/requirements/0001-aws-cloud-native-architecture.md` | AWS Cloud Native Reference Architecture (ARD) / `sdlc/ard` | 3-AZ VPC, EKS, VPC Lattice, ALB/WAF, Aurora/cache/Secrets flows, ADOT/Managed Prometheus/Grafana quality attributes and non-goals | A1–A8 | M |
| S07 | `examples/aws/docs/02.architecture/requirements/2026-03-31-aws-migration-ard.md` | AWS Infrastructure Migration Architecture Reference Document (ARD) / `sdlc/ard` | EKS/RDS/cache/ALB ownership, IRSA, HPA/autoscaling, private-node/isolated-data layout, CloudWatch/control-plane logging | A1–A8 | M |
| S08 | `examples/aws/docs/02.architecture/requirements/README.md` | 02.architecture/requirements (Architecture Requirements Document) / `README index` | three-ARD inventory, architecture audience/scope, dated refresh and static-evidence boundary | A1–A8 | M |
| S09 | `examples/aws/docs/02.architecture/requirements/aws-cloud-architecture.md` | AWS Cloud Architecture (Migration from K3s/k3d) / `sdlc/ard` | local-to-AWS resource map, public/private/database subnet roles, IRSA/ESO/ALB/ACM controls, Spot/RDS Proxy/S3 tiering cost ideas | A1–A8 | M |
| S10 | `examples/aws/docs/03.specs/README.md` | 03.specs (Technical Specifications) / `README index` | Spec inventory, implementation-versus-live boundary and succession rule | A1–A8 | M |
| S11 | `examples/aws/docs/03.specs/aws-migration/spec.md` | AWS Migration Technical Specification (Spec) / `sdlc/spec` | exact VPC/AZ/CIDR, EKS 1.35, Pod Identity/Karpenter assumptions, Aurora 16/ACU and Redis 7 contracts, endpoint/ESO verification and escalation | A1–A8 | M |
| S12 | `examples/aws/docs/04.execution/plans/2026-03-31-aws-migration-plan.md` | AWS Infrastructure Migration Implementation Plan / `sdlc/plan` | VPC→EKS→managed services→GitOps sequence, validation/risk table, docs/assets complete but live deployment unchecked | A1–A8 | M |
| S13 | `examples/aws/docs/04.execution/plans/2026-03-31-aws-migration-roadmap.md` | AWS Migration Implementation Plan (Roadmap) / `sdlc/plan` | foundation/platform/data/workload/cutover phases, dump/restore and rollback risks, historical all-complete checkboxes that lack live evidence | A1–A8 | M |
| S14 | `examples/aws/docs/04.execution/plans/README.md` | 04.execution/plans (Implementation Plans) / `README index` | two-plan inventory and plan-to-task refresh contract | A1–A8 | M |
| S15 | `examples/aws/docs/04.execution/tasks/2026-03-31-aws-migration-tasks.md` | Task: AWS Migration Execution List / `sdlc/task` | six Todo units for VPC, EKS/IAM, Karpenter, Aurora, GitOps workload and DNS cutover with intended evidence | A1–A8 | M |
| S16 | `examples/aws/docs/04.execution/tasks/2026-03-31-bootstrap-aws.md` | Task: AWS Infrastructure Migration Implementation / `sdlc/task` | historical Done claims for documentation/Terraform/manifests/guide, static validation expectations, no-live working rule | A1–A8 | M |
| S17 | `examples/aws/docs/04.execution/tasks/README.md` | 04.execution/tasks (Implementation Tasks) / `README index` | task inventory, evidence expectation and succession boundary | A1–A8 | M |
| S18 | `examples/aws/docs/05.operations/guides/README.md` | 05.operations/guides (Operational Guides) / `README index` | setup-guide inventory, onboarding audience and provider-static boundary | A1–A8 | M |
| S19 | `examples/aws/docs/05.operations/guides/aws-setup-guide.md` | AWS EKS Setup and Access Guide / `sdlc/guide` | AWS CLI/kubectl/IAM prerequisites, temporary kubeconfig, node and Pod Identity checks, unauthorized/private-endpoint pitfalls | A2, A5–A8 | M |
| S20 | `examples/aws/docs/05.operations/policies/README.md` | 05.operations/policies (System Operations & Governance) / `README index` | two-policy inventory, governance scope and quarterly refresh contract | A1–A8 | M |
| S21 | `examples/aws/docs/05.operations/policies/aws-management.md` | AWS Infrastructure Operations Policy / `sdlc/policy` | Terraform-only control, deny-by-default traffic, Project/Environment/Owner/CostCenter tags, no public data or root use, emergency manual-change reconciliation | A1–A8 | M |
| S22 | `examples/aws/docs/05.operations/policies/aws-operations-policy.md` | AWS Migration Operations Policy / `sdlc/policy` | KMS, Project/Env/Owner tags, no long-lived access keys, approved Spot use, monthly cost/quarterly policy review, 90-day agent log retention and destructive-command stop | A1–A8 | M |
| S23 | `examples/aws/docs/05.operations/runbooks/README.md` | 05.operations/runbooks (Incident Response Runbooks) / `README index` | DR/recovery inventory, incident handoff and evidence-boundary contract | A1–A8 | M |
| S24 | `examples/aws/docs/05.operations/runbooks/aws-disaster-recovery.md` | AWS Disaster Recovery Runbook / `sdlc/runbook` | EKS rebuild, RDS snapshot restore, Secrets Manager endpoint update, Argo CD diff, service checks, local/static-page rollback and IaC reconciliation | A1–A8 | M |
| S25 | `examples/aws/docs/05.operations/runbooks/aws-recovery.md` | AWS Infrastructure Recovery Runbook / `sdlc/runbook` | cluster/network/data diagnosis, Multi-AZ failover and snapshot recovery, CloudWatch/CloudTrail evidence, git/Terraform rollback review | A1–A8 | M |
| S26 | `examples/aws/docs/README.md` | AWS Migration Documentation Hub / `README index` | full nine-stage inventory, EKS/Terraform/data/security stack snapshot, Tech Stack Inventory SSoT, 2026-07-12 observation and no-provider-latest boundary | A1–A8 | M |

Coverage arithmetic is exact: one PRD, two ADRs, three ARDs, one Spec, two
Plans, two Tasks, one Guide, two Policies, two Runbooks, and ten README indexes
equal 26 rows. Each source path appears once in the coverage table, and all 26
retain disposition `M` pending deletion review.

## Definitions / Facts

**Dated product intent and success conditions.** Retained source facts describe
a migration from local k3s/k3d constraints to an AWS-only target: EKS-based
compute, managed PostgreSQL/cache, native secret management, Terraform IaC,
GitOps continuity, Multi-AZ availability, automated scaling and less operator
burden. Personas are platform engineers, application developers and operators.
The PRD records a 99.9% availability SLO, no application business-logic rewrite,
no Direct Connect/hybrid scope and no simultaneous multi-cloud target. The
“80% operations reduction,” “up to 90% Spot saving,” sub-second scaling and
performance-improvement language are historical goals, not measured outcomes.

**Retained decisions and alternatives.** The dated decision set selects EKS
1.35 target, Karpenter, Aurora PostgreSQL Serverless v2/RDS, ElastiCache,
Secrets Manager plus ESO, ALB/ACM and Terraform/Argo CD. It preserves
self-managed Kubernetes on EC2, managed node groups, retaining Vault and SSM
Parameter Store as rejected alternatives, together with vendor lock-in,
learning curve, dual local/cloud tooling and cost trade-offs. Replacing Vault
is an AWS-example decision only; it does not rewrite repository-wide secret
policy. RDS Multi-AZ clusters and Aurora Global Database remain workload-,
region-, cost-, RPO- and RTO-dependent alternatives.

**Architecture and interface contracts.** The source contract uses VPC
`10.100.0.0/16` across `ap-northeast-2a/b/c`; public subnets
`10.100.1.0/24`–`10.100.3.0/24`, private subnets `10.100.11.0/24`–
`10.100.13.0/24`, and isolated data subnets `10.100.21.0/24`–
`10.100.23.0/24`. It places ALB/NAT at the public edge, EKS workers privately,
and RDS/cache in isolated networks. Historical compute/data assumptions include
EKS 1.35, Aurora PostgreSQL 16 with 0.5–4.0 ACU, Redis OSS 7 compatibility,
EBS/EFS, Route 53/ExternalDNS, ECR, CloudWatch/control-plane logging, ADOT,
Managed Prometheus/Grafana and optional VPC Lattice/Istio concepts. These are
comparison inputs, not a current supported bill of materials.

**Historical execution status.** One 2026-03-31 implementation plan marks
documentation, Terraform and manifests complete while leaving live deployment
unchecked; its sibling roadmap marks all migration outcomes complete. The task
list separately keeps six provider work units as Todo while the bootstrap task
marks six document/code deliverables Done. This inconsistency is deliberately
retained: it proves artifact drafting, not provider execution. The sources also
disagree between temporary parallel local operation and eventual local
decommission; a future migration plan must choose explicitly.

**Operations, recovery and observability.** Retained policy requires IaC,
least privilege, isolated data, encryption, tags, quarterly review, cost review,
and human approval plus later IaC reconciliation for emergencies. DR knowledge
covers impact triage, Terraform-plan review, temporary kubeconfig access,
RDS snapshot restore planning, endpoint/secret reference updates, GitOps diff,
pod/port/URL verification, CloudWatch/CloudTrail evidence and rollback to the
surviving local system or a static page. The AWS sources set 99.9% as a goal but
provide no numeric RPO or RTO; that is an explicit gap and must not be inferred.
The 90-day agent-log retention statement is retained as a dated policy claim,
not proof that an S3 retention control exists.

**Executable owner mapping.** All eight tracked AWS assets existed at the
observation baseline and remain outside the documentation deletion set.

| Asset ID | Retained executable owner | Knowledge mapped to it | Currentness boundary |
| --- | --- | --- | --- |
| A1 | `examples/aws/terraform/main.tf` | Terraform/provider constraints, region, cluster name and default tagging | Re-resolve provider/module versions and backend design before use. |
| A2 | `examples/aws/terraform/eks.tf` | EKS 1.35 target, core managed nodes, Karpenter and Pod Identity/IRSA transition | Validate EKS support, access entries and identity model. |
| A3 | `examples/aws/terraform/vpc.tf` | 3-AZ VPC/subnet layout, NAT, flow logs and discovery tags | Validate IP capacity, endpoints, cost and subnet recommendations. |
| A4 | `examples/aws/terraform/rds_cache.tf` | Aurora Serverless v2, ElastiCache and node-security-group connectivity | Validate engine/SKU availability, HA, backup, RPO/RTO and secret ownership. |
| A5 | `examples/aws/terraform/secrets.tf` | Secrets Manager, recovery window, ESO role and Pod Identity association | Dummy values are not secrets; reduce broad policy and verify service-account name. |
| A6 | `examples/aws/kubernetes/external-secrets.yaml` | ClusterSecretStore/ExternalSecret synchronization example | Verify current ESO API, Pod Identity/Fargate constraints and secret exposure policy. |
| A7 | `examples/aws/kubernetes/external-services-aws.yaml` | RDS/cache ExternalName wiring and ALB Ingress example | Placeholder endpoints/ARN require approved substitution; current controller review required. |
| A8 | `examples/aws/kubernetes/karpenter.yaml` | current asset uses `NodePool`/`EC2NodeClass`, Spot/on-demand and disruption settings | Recheck Karpenter API and `do-not-disrupt`/disruption behavior. |

**Preserved fenced command groups.** The source pack contains exactly seven
AWS Bash fences. Every group is represented below without claiming execution.

| Group | Source ID | Preserved payload summary | Classification |
| --- | --- | --- | --- |
| C-AWS-01 | S11 | temporary `mktemp` kubeconfig, `aws eks update-kubeconfig`, `kubectl get nodes`, `nc` checks for PostgreSQL/Redis, and `kubectl get externalsecrets -A` | Read/access checks only after sandbox and placeholder approval. |
| C-AWS-02 | S11 | comments requiring approved sandbox, placeholder replacement and official-doc refresh | Guard-only fence; no executable operation. |
| C-AWS-03 | S19 | temporary kubeconfig plus `aws eks update-kubeconfig` and `kubectl get nodes` | Provider/cluster access; human authorization required. |
| C-AWS-04 | S19 | `kubectl get nodes` | Read-only cluster query; not executed here. |
| C-AWS-05 | S19 | `kubectl run aws-cli --image=amazon/aws-cli:latest --restart=Never -- aws sts get-caller-identity` | Creates a pod and exposes identity output; operator-only, not a harmless read. |
| C-AWS-06 | S24 | `cd examples/aws/terraform`, `terraform plan -out dr-recovery.plan`, then temporary kubeconfig and node query | Generates a local plan and accesses a cluster; DR approval required. |
| C-AWS-07 | S24 | `argocd app diff root-apps --refresh` | Reconciliation-system access; approved context required. |

Additional inline historical payload includes `terraform validate/show/state
list/plan`, `kubectl diff/get/describe`, `aws eks describe-cluster`, AWS RDS
describe/restore commands, endpoint `nc`/`telnet`/`curl`, `git revert`, DNS
lookup and CloudTrail review. These names preserve the intended evidence
categories; none is asserted safe, current or executed.

**Currentness findings.** Source text that names Karpenter `Provisioner` or
`do-not-evict` is historical; the retained asset already uses `NodePool`, but
current disruption and `do-not-disrupt` semantics still require review. IRSA,
EKS Pod Identity and ASCP/ESO are not interchangeable. Pod Identity is an EKS
capability, and ASCP/Pod Identity has documented Fargate constraints. HA and
backup selection is conditional, and no official page proves the dated Aurora,
ElastiCache, IAM, controller or cost configuration is deployed.

## Sources

Local evidence consists of the 26 rows above, the immutable source manifest,
the source-inspection artifact, and the durable migration ledger. Official
links below are direct provider-primary review inputs observed 2026-07-13 KST.

| Official primary source | Applicability to retained facts | Rejected / conditional guidance | Refresh trigger |
| --- | --- | --- | --- |
| [EKS best-practices introduction](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html) | Architecture and operations review baseline | Does not certify this example or a live cluster. | EKS support or best-practice structure changes. |
| [EKS subnet guidance](https://docs.aws.amazon.com/eks/latest/best-practices/subnets.html) | Checks the dated 3-AZ/IP/subnet assumptions. | The frozen CIDRs are not universally correct. | IP, subnet, control-plane or VPC guidance changes. |
| [EKS identity and access management](https://docs.aws.amazon.com/eks/latest/best-practices/identity-and-access-management.html) | Least-privilege and access review. | Dated IRSA/Pod Identity statements need service-by-service validation. | IAM/access-entry recommendations change. |
| [EKS Pod Identities](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) | Current EKS workload-identity option. | Cloud-EKS-specific, not generic Kubernetes identity. | Supported platforms, agents or limitations change. |
| [Use secrets with EKS](https://docs.aws.amazon.com/eks/latest/userguide/manage-secrets.html) | Secret integration review. | No evidence of a configured store or secret. | CSI/ASCP/ESO guidance changes. |
| [ASCP with EKS Pod Identity](https://docs.aws.amazon.com/secretsmanager/latest/userguide/ascp-pod-identity-integration.html) | ASCP/Pod Identity integration boundary. | Fargate and compatibility limitations remain conditional. | ASCP, Pod Identity or Fargate support changes. |
| [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html) | Controller/install boundary for ALB claims. | Does not validate the placeholder Ingress/ACM ARN. | Controller, IAM or ingress support changes. |
| [Karpenter best practices](https://docs.aws.amazon.com/eks/latest/best-practices/karpenter.html) | NodePool and disruption review. | Old `Provisioner`/`do-not-evict` guidance is rejected as current. | Karpenter APIs or disruption semantics change. |
| [RDS Multi-AZ DB clusters](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html) | HA alternative and failure-domain review. | Not a universal Aurora replacement. | Engine, region, failover or topology support changes. |
| [RDS backup and restore](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html) | Backup/restore boundary for DR planning. | No restore was run; retention and RPO are unverified. | Backup, PITR or restore behavior changes. |
| [Aurora global database DR](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database-disaster-recovery.html) | Conditional cross-region DR option. | Not the default for every workload or budget. | Global failover, switchover or region support changes. |
| [ElastiCache engine versions](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.Redis.Versions.html) | Engine/version refresh basis. | Frozen Redis compatibility is not provider-latest certification. | Supported engines or end-of-support dates change. |
| [Argo CD concepts for EKS](https://docs.aws.amazon.com/eks/latest/userguide/argocd-concepts.html) | Conceptual GitOps boundary. | Does not prove this repository reconciles an EKS application. | AWS-managed Argo CD integration guidance changes. |

## Review and Freshness

Refresh this document when the 59-path source manifest, any of A1–A8, the
durable ledger destination, provider README inventory, EKS/Kubernetes support,
Terraform/provider/module constraints, Pod Identity/IRSA/secret integration,
ALB controller, Karpenter, RDS/Aurora backup/HA, ElastiCache engine, VPC/subnet
model, GitOps owner, cost assumptions, or any cited official page materially
changes.

Before deletion, an independent reviewer must prove that the 26-row source set,
seven Bash groups, decisions, alternatives, dated requirements, historical
statuses, operational controls, rollback facts and README succession boundaries
are all represented. Before any live use, an operator must separately establish
current versions, account/region/quota, IAM, cost, network, backup, RPO/RTO,
secret, rollback and observability evidence. Secret values, credentials,
kubeconfigs and sensitive provider output must stay outside the repository.

## Related Documents

- [AWS snapshot index](README.md)
- [Cloud example reference collection](../README.md)
- [AWS executable example entrypoint](../../../../examples/aws/README.md)
- [Tech Stack Version Inventory](../../data/tech-stack-version-inventory.md)
- [Authored Document Migration Spec](../../../03.specs/030-authored-document-migration/spec.md)
