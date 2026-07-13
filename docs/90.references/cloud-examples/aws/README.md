# AWS Cloud Example Snapshot Handoff

## Overview

This index is the current Stage 90 entrypoint for the dated AWS snapshot.
The 26 AWS paths from source59 under `examples/aws/docs/` are retired; the dated
snapshot is their durable documentation destination, while executable assets
remain under `examples/aws/`.

## Snapshot Contract

- Observation date: `2026-07-12`.
- Document registry baseline SHA:
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`.
- Retired source tree: `examples/aws/docs/` (26 source59 paths).
- Executable asset owner: `examples/aws/` (assets remain in place).
- Role: durable dated documentation destination, not active main-stage
  ownership or provider-latest AWS guidance.

## Report Index

| Snapshot index | Preserved subject |
| --- | --- |
| [AWS documentation inventory](2026-07-12-aws-example-snapshot.md#scope) | Nine-stage migration example map and AWS stack snapshot. |
| [Requirements](2026-07-12-aws-example-snapshot.md#definitions--facts) | Product intent, constraints, KPIs, and dated PRD inventory. |
| [Architecture requirements](2026-07-12-aws-example-snapshot.md#definitions--facts) | AWS reference architecture and ARD inventory. |
| [Architecture decisions](2026-07-12-aws-example-snapshot.md#definitions--facts) | Managed-service and Secrets Manager decision inventory. |
| [Technical specifications](2026-07-12-aws-example-snapshot.md#definitions--facts) | AWS migration Spec inventory and verification boundaries. |
| [Execution plans](2026-07-12-aws-example-snapshot.md#definitions--facts) | Migration plan and roadmap inventory. |
| [Execution tasks](2026-07-12-aws-example-snapshot.md#definitions--facts) | Migration and bootstrap task inventory. |
| [Operations guides](2026-07-12-aws-example-snapshot.md#definitions--facts) | AWS/EKS setup guide inventory. |
| [Operations policies](2026-07-12-aws-example-snapshot.md#definitions--facts) | Management and operations-policy inventory. |
| [Operations runbooks](2026-07-12-aws-example-snapshot.md#definitions--facts) | Disaster-recovery and recovery-procedure inventory. |

## Refresh and Succession

[Spec 030](../../../03.specs/030-authored-document-migration/spec.md) completed
the consolidation into this dated snapshot. Recheck it when an official AWS
service, API, support, or lifecycle contract changes, when retained source
coverage changes, or when Spec 030 promotes a successor. Executable examples
remain under `examples/aws/`; this index does not relocate or activate them.

## Evidence Boundary

Evidence is limited to tracked repository content observed on `2026-07-12`
and the fixed registry baseline above. No live AWS account, EKS cluster,
credential, IAM entitlement, cost, network, secret, deployment, or
provider-latest readiness was checked or is implied.

## Related Documents

- [Cloud Example Snapshot Collection](../README.md)
- [AWS consolidated snapshot](2026-07-12-aws-example-snapshot.md)
- [Tech Stack Version Inventory](../../data/tech-stack-version-inventory.md)
- [README Profile Spec](../../../03.specs/028-readme-workspace-profiles/spec.md)
- [Authored Document Migration Spec](../../../03.specs/030-authored-document-migration/spec.md)
