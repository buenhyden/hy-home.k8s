# Azure Cloud Example Snapshot Handoff

## Overview

This index is the current Stage 90 entrypoint for the dated Azure snapshot.
The 33 Azure paths from source59 under `examples/azure/docs/` are retired; the
dated snapshot is their durable documentation destination, while executable
assets remain under `examples/azure/`.

## Snapshot Contract

- Observation date: `2026-07-12`.
- Document registry baseline SHA:
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`.
- Retired source tree: `examples/azure/docs/` (33 source59 paths).
- Executable asset owner: `examples/azure/` (assets remain in place).
- Role: durable dated documentation destination, not active main-stage
  ownership or provider-latest Azure guidance.

## Report Index

| Snapshot index | Preserved subject |
| --- | --- |
| [Azure documentation inventory](2026-07-12-azure-example-snapshot.md#scope) | Nine-stage migration example map and Azure stack snapshot. |
| [Requirements](2026-07-12-azure-example-snapshot.md#definitions--facts) | Product intent, FR/NFR, SLA, and dated PRD inventory. |
| [Architecture requirements](2026-07-12-azure-example-snapshot.md#definitions--facts) | AKS reference architecture and ARD inventory. |
| [Architecture decisions](2026-07-12-azure-example-snapshot.md#definitions--facts) | CNI, AGC, and Workload Identity decision inventory. |
| [Technical specifications](2026-07-12-azure-example-snapshot.md#definitions--facts) | Azure migration Spec and resource-contract inventory. |
| [Execution plans](2026-07-12-azure-example-snapshot.md#definitions--facts) | Migration strategy and phase inventory. |
| [Execution tasks](2026-07-12-azure-example-snapshot.md#definitions--facts) | Migration and AKS provisioning task inventory. |
| [Operations guides](2026-07-12-azure-example-snapshot.md#definitions--facts) | Azure onboarding and deployment-guide inventory. |
| [Operations policies](2026-07-12-azure-example-snapshot.md#definitions--facts) | Maintenance, operations, and cost-policy inventory. |
| [Operations runbooks](2026-07-12-azure-example-snapshot.md#definitions--facts) | Disaster recovery, fault tolerance, and node-replacement inventory. |

## Refresh and Succession

[Spec 030](../../../03.specs/030-authored-document-migration/spec.md) completed
the consolidation into this dated snapshot. Recheck it when an official Azure
service, API, support, or lifecycle contract changes, when retained source
coverage changes, or when Spec 030 promotes a successor. Executable examples
remain under `examples/azure/`; this index does not relocate or activate them.

## Evidence Boundary

Evidence is limited to tracked repository content observed on `2026-07-12`
and the fixed registry baseline above. No live Azure subscription, AKS cluster,
credential, RBAC entitlement, cost, network, secret, deployment, or
provider-latest readiness was checked or is implied.

## Related Documents

- [Cloud Example Snapshot Collection](../README.md)
- [Azure consolidated snapshot](2026-07-12-azure-example-snapshot.md)
- [Tech Stack Version Inventory](../../data/tech-stack-version-inventory.md)
- [README Profile Spec](../../../03.specs/028-readme-workspace-profiles/spec.md)
- [Authored Document Migration Spec](../../../03.specs/030-authored-document-migration/spec.md)
