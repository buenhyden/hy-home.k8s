# 90.references/data

> Repo-backed inventories, durable catalogs, and factual lookup data that
> support the rest of the documentation system.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

`data/`는 실행 절차가 아니라 느리게 변하는 기준값과 카탈로그성 참고
자료를 보관하는 reference category다. 버전 계약, cloud example snapshot,
Agent reference catalog처럼 여러 stage가 반복해서 참조하는 data-like
facts를 둔다.

이 폴더의 문서는 정책, 배포 승인, live cluster mutation, secret handling,
runtime permission을 새로 정의하지 않는다. 그런 내용은 각 canonical owner
stage로 라우팅한다.

### Collection Readers

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Repo-backed version contracts and cloud example snapshots.
- Durable Agent reference catalog entries that do not define runtime policy.
- Factual lookup tables that multiple stages consume.
- Source-checked inventory data with explicit freshness triggers.

### Out of Scope

- Runtime governance policy.
- Feature-local agent design.
- Live upgrade procedures or deployment approvals.
- Research analysis, audit reports, learning roadmaps, or generated wiki maps.

## Item Index

```text
data/
├── active-corpus-retention-census.json # ACER-001 immutable corpus census and dispositions
├── active-corpus-eligibility-ledger.json # ACER-002 pinned dry-run eligibility ledger
├── active-corpus-migration-results.json # ACER-003 closed atomic migration results
├── agent-reference-index.md          # Durable Agent reference catalog boundary
├── tech-stack-version-inventory.md   # Repo-backed version contracts and cloud snapshots
└── README.md                         # This file
```

## Add and Find

1. Use [reference.template.md](../../99.templates/templates/common/reference.template.md) for new non-README documents.
2. Keep every data reference factual and source-checked.
3. Update the source file, this folder index, and [90.references README](../README.md) in the same change when a data reference moves.
4. Route runtime policy to `docs/00.agent-governance/**`.
5. Route execution steps, upgrade procedures, and incident handling to `docs/05.operations/**`.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/data/`다.

- 같은 data reference 문서는 `./`로 연결한다.
- sibling reference folders는 `../audits/`, `../learning/`, `../llm-wiki/`,
  `../research/`로 연결한다.
- canonical owner stage는 `../../00.agent-governance/`,
  `../../03.specs/`, `../../05.operations/`로 연결한다.

### Data Reference Index

| Document | Reference Type | Role | Freshness Trigger |
| --- | --- | --- | --- |
| [Active Corpus Retention Census](./active-corpus-retention-census.json) | repo-backed immutable census / external-method snapshot | Exact 110 candidate rows, Spec 037 controls, Stage 05, pinned 29-file helper input, exact one-test proposal delta, proposed 30-file helper counts, owned ACER-001 dispositions, explicit unresolved upstream/program/owner/link/closure evidence axes, and canonical safe row paths with value-free diagnostics; neither helper count substitutes for ACER-004 recomputation, and body-Spec links are non-authoritative observations | ACER-002 eligibility evidence, Spec 037 closure, ACER-004 then-current role audit, pinned commit/object drift, proposal delta, or methodology-source change |
| [Active Corpus Eligibility Ledger](./active-corpus-eligibility-ledger.json) | repo-backed dry-run ledger | Exact pinned 110 candidate identities, 12 complete lineage pairs eligible only for a future ACER-003 atomic cutover, 98 owned `DEFER` rows, and two retained Spec 037 controls; it records route, consumer, recovery, and no-cutover evidence without moving a file | ACER-003 cutover, pinned object or lineage evidence drift, or an owned upstream evidence change |
| [Active Corpus Migration Results](./active-corpus-migration-results.json) | repo-backed closed migration-result ledger | Exact first-two deterministic eligible-prefix ACER-003 batches, four complete Plan/Task records, immutable 31/202 archive base plus 31 additive historical links, exact source/archive identities, repaired current consumers, Spec/program closure owners, archive navigation boundary, validation results, and the exact rollback-parent chain without a self-referential batch commit | Each later ACER-003 atomic batch, archive/index drift, consumer repair, validation result, or rollback-parent change |
| [Agent Reference Index](./agent-reference-index.md) | durable-concept / data-catalog | Agent reference boundaries and canonical owner routing | Agent reference document addition, runtime roster movement, or Stage 00 routing change |
| [Tech Stack Version Inventory](./tech-stack-version-inventory.md) | version-contract-inventory / external-standard-snapshot | Repo-backed version contracts and cloud example snapshots | Manifest/config/example version change or official support-range change |

### Authority Boundary

- `data/` owns factual lookup data and source-checked reference inventories.
- `active-corpus-retention-census.json` is immutable ACER-001 input evidence;
  it does not authorize archive migration, infer current worktree state, or
  promote any row to `eligible`.
- `active-corpus-eligibility-ledger.json` is ACER-002 dry-run evidence only;
  its eligibility result does not create an archive payload, index row, or migration.
- `active-corpus-migration-results.json` is the additive ACER-003 cutover
  authority. It joins the immutable census and eligibility inputs, admits only
  a complete deterministic eligible prefix, and records current cutover state
  without rewriting either reviewed input snapshot.
- `docs/00.agent-governance/**` owns agent runtime truth, provider behavior,
  hooks, permissions, model routing, and execution rules.
- `docs/03.specs/**/agent-design.md` owns feature-local Agent designs.
- `docs/05.operations/runbooks/**` owns executable operational procedures.
- `docs/90.references/research/**`, `audits/**`, `learning/**`, and
  `llm-wiki/**` own their own reference families and should not be duplicated here.

## Related Documents

- [90.references README](../README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
