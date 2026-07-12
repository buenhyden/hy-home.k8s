# 90.references/audits

## Overview

`docs/90.references/audits/` stores dated implementation-audit packs for
workspace governance, harness behavior, provider adapters, delivery practices,
and platform controls. Each pack is a descriptive snapshot; active policy,
execution, and operations remain in their owning stages.

### Collection Readers

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Dated audit snapshots and their compact pack indexes.
- Pack-level currentness, successor, and resolution routing.
- Repository-static evidence boundaries and links to canonical owners.

### Out of Scope

- Active requirements, architecture, implementation, or operations contracts.
- Live cluster, provider-runtime, credential, or secret-value evidence.
- Report-by-report duplication already owned by each dated pack README.

## Item Index

```text
audits/
├── 2026-05-24-whga/
├── 2026-07-02-whia/
├── 2026-07-03-wdgh/
├── 2026-07-04-wdcn/
├── 2026-07-05-wea/
├── 2026-07-11-weia/
└── README.md
```

### Audit Pack Registry

| Pack | Pack role | Snapshot scope | Successor / resolution |
| --- | --- | --- | --- |
| [2026-05-24-whga](./2026-05-24-whga/README.md) | Historical | Workspace harness gap-analysis snapshot. | Successor: [2026-07-02-whia](./2026-07-02-whia/README.md). |
| [2026-07-02-whia](./2026-07-02-whia/README.md) | Historical | Workspace governance, harness/loop, provider, and SDLC delivery implementation audit. | Successor: [2026-07-05-wea](./2026-07-05-wea/README.md). |
| [2026-07-03-wdgh](./2026-07-03-wdgh/README.md) | Resolved | Workspace document-governance hardening baseline. | Resolution: [2026-07-04-wdcn](./2026-07-04-wdcn/README.md). |
| [2026-07-04-wdcn](./2026-07-04-wdcn/README.md) | Resolved | Workspace document-contract normalization audit. | Current comparison owner: [2026-07-11-weia](./2026-07-11-weia/README.md). |
| [2026-07-05-wea](./2026-07-05-wea/README.md) | Historical | Workspace engineering implementation audit based on the 2026-07-04 research benchmark. | Successor: [2026-07-11-weia](./2026-07-11-weia/README.md). |
| [2026-07-11-weia](./2026-07-11-weia/README.md) | Current pack | Evidence-scored workspace engineering implementation audit at the pinned observation SHA. | No successor; completion evidence is in the [Plan](../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md) and [Task](../../04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md). |

## Add and Find

1. Start from the single Current pack row above.
2. Open a dated pack README for its report-level inventory and evidence cutoff.
3. Treat historical and resolved packs as immutable snapshots except for
   navigation, currentness, or broken-link corrections.
4. Route implementation work to a canonical Stage 01-05 owner.

### Relative Link Rules

- Dated pack links start with `./`.
- Other documentation stages start with `../../<stage>/`.
- Repository-root links start with `../../../`.

### Evidence Boundary

- Repository-backed evidence outranks upstream capability for local status.
- Repository-static validation does not imply live runtime readiness.
- Do not infer live k3d, Argo CD, Vault, ESO, Kubernetes, provider, credential,
  secret-value, deployment, or external-service state from these packs.

## Related Documents

- [Parent Reference README](../README.md)
- [Current Audit Pack](./2026-07-11-weia/README.md)
- [Current Audit Integration Plan](../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- [Current Audit Integration Task](../../04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md)
- [Workspace Harness Research Packs](../research/README.md)
- [Reference Template](../../99.templates/templates/common/reference.template.md)
- [Collection Index README Form](../../99.templates/templates/common/readme-collection-index.template.md)
