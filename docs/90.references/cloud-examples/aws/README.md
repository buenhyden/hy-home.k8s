# AWS Cloud Example Snapshot Handoff

## Overview

이 인덱스는 `examples/aws/docs/`에 남아 있는 AWS 마이그레이션 문서 예시를
Stage 90에서 찾기 위한 handoff다. 문서와 실행 자산을 이동하지 않으며,
Spec 030이 후속 통합 범위를 결정할 때까지 원본 경로를 보존한다.

## Snapshot Contract

- Observation date: `2026-07-12`.
- Document registry baseline SHA:
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`.
- Current source tree: `examples/aws/docs/`.
- Executable asset owner: `examples/aws/`.
- Role: dated migration example handoff, not active main-stage ownership or
  provider-latest AWS guidance.

## Report Index

| Snapshot index | Preserved subject |
| --- | --- |
| [AWS documentation hub](../../../../examples/aws/docs/README.md) | Nine-stage migration example map and AWS stack snapshot. |
| [Requirements](../../../../examples/aws/docs/01.requirements/README.md) | Product intent, constraints, KPIs, and dated PRD inventory. |
| [Architecture requirements](../../../../examples/aws/docs/02.architecture/requirements/README.md) | AWS reference architecture and ARD inventory. |
| [Architecture decisions](../../../../examples/aws/docs/02.architecture/decisions/README.md) | Managed-service and Secrets Manager decision inventory. |
| [Technical specifications](../../../../examples/aws/docs/03.specs/README.md) | AWS migration Spec inventory and verification boundaries. |
| [Execution plans](../../../../examples/aws/docs/04.execution/plans/README.md) | Migration plan and roadmap inventory. |
| [Execution tasks](../../../../examples/aws/docs/04.execution/tasks/README.md) | Migration and bootstrap task inventory. |
| [Operations guides](../../../../examples/aws/docs/05.operations/guides/README.md) | AWS/EKS setup guide inventory. |
| [Operations policies](../../../../examples/aws/docs/05.operations/policies/README.md) | Management and operations-policy inventory. |
| [Operations runbooks](../../../../examples/aws/docs/05.operations/runbooks/README.md) | Disaster-recovery and recovery-procedure inventory. |

## Refresh and Succession

[Spec 030](../../../03.specs/030-authored-document-migration/spec.md) owns the
planned consolidation decision. Recheck this snapshot when an official AWS
service, API, support, or lifecycle contract changes, when the source inventory
changes, or when Spec 030 promotes a successor. Executable examples remain
under `examples/aws/`; this index does not relocate or activate them.

## Evidence Boundary

Evidence is limited to tracked repository content observed on `2026-07-12`
and the fixed registry baseline above. No live AWS account, EKS cluster,
credential, IAM entitlement, cost, network, secret, deployment, or
provider-latest readiness was checked or is implied.

## Related Documents

- [Cloud Example Snapshot Collection](../README.md)
- [AWS source documentation hub](../../../../examples/aws/docs/README.md)
- [Tech Stack Version Inventory](../../data/tech-stack-version-inventory.md)
- [README Profile Spec](../../../03.specs/028-readme-workspace-profiles/spec.md)
- [Authored Document Migration Spec](../../../03.specs/030-authored-document-migration/spec.md)
