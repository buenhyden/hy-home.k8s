# Azure Cloud Example Snapshot Handoff

## Overview

이 인덱스는 `examples/azure/docs/`에 남아 있는 Azure 마이그레이션 문서 예시를
Stage 90에서 찾기 위한 handoff다. 문서와 실행 자산을 이동하지 않으며,
Spec 030이 후속 통합 범위를 결정할 때까지 원본 경로를 보존한다.

## Snapshot Contract

- Observation date: `2026-07-12`.
- Document registry baseline SHA:
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`.
- Current source tree: `examples/azure/docs/`.
- Executable asset owner: `examples/azure/`.
- Role: dated migration example handoff, not active main-stage ownership or
  provider-latest Azure guidance.

## Report Index

| Snapshot index | Preserved subject |
| --- | --- |
| [Azure documentation hub](../../../../examples/azure/docs/README.md) | Nine-stage migration example map and Azure stack snapshot. |
| [Requirements](../../../../examples/azure/docs/01.requirements/README.md) | Product intent, FR/NFR, SLA, and dated PRD inventory. |
| [Architecture requirements](../../../../examples/azure/docs/02.architecture/requirements/README.md) | AKS reference architecture and ARD inventory. |
| [Architecture decisions](../../../../examples/azure/docs/02.architecture/decisions/README.md) | CNI, AGC, and Workload Identity decision inventory. |
| [Technical specifications](../../../../examples/azure/docs/03.specs/README.md) | Azure migration Spec and resource-contract inventory. |
| [Execution plans](../../../../examples/azure/docs/04.execution/plans/README.md) | Migration strategy and phase inventory. |
| [Execution tasks](../../../../examples/azure/docs/04.execution/tasks/README.md) | Migration and AKS provisioning task inventory. |
| [Operations guides](../../../../examples/azure/docs/05.operations/guides/README.md) | Azure onboarding and deployment-guide inventory. |
| [Operations policies](../../../../examples/azure/docs/05.operations/policies/README.md) | Maintenance, operations, and cost-policy inventory. |
| [Operations runbooks](../../../../examples/azure/docs/05.operations/runbooks/README.md) | Disaster recovery, fault tolerance, and node-replacement inventory. |

## Refresh and Succession

[Spec 030](../../../03.specs/030-authored-document-migration/spec.md) owns the
planned consolidation decision. Recheck this snapshot when an official Azure
service, API, support, or lifecycle contract changes, when the source inventory
changes, or when Spec 030 promotes a successor. Executable examples remain
under `examples/azure/`; this index does not relocate or activate them.

## Evidence Boundary

Evidence is limited to tracked repository content observed on `2026-07-12`
and the fixed registry baseline above. No live Azure subscription, AKS cluster,
credential, RBAC entitlement, cost, network, secret, deployment, or
provider-latest readiness was checked or is implied.

## Related Documents

- [Cloud Example Snapshot Collection](../README.md)
- [Azure source documentation hub](../../../../examples/azure/docs/README.md)
- [Tech Stack Version Inventory](../../data/tech-stack-version-inventory.md)
- [README Profile Spec](../../../03.specs/028-readme-workspace-profiles/spec.md)
- [Authored Document Migration Spec](../../../03.specs/030-authored-document-migration/spec.md)
