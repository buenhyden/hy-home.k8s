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

## Audience

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

## Structure

```text
data/
├── agent-reference-index.md          # Durable Agent reference catalog boundary
├── tech-stack-version-inventory.md   # Repo-backed version contracts and cloud snapshots
└── README.md                         # This file
```

## How to Work in This Area

1. Use [reference.template.md](../../99.templates/templates/common/reference.template.md) for new non-README documents.
2. Keep every data reference factual and source-checked.
3. Update the source file, this folder index, and [90.references README](../README.md) in the same change when a data reference moves.
4. Route runtime policy to `docs/00.agent-governance/**`.
5. Route execution steps, upgrade procedures, and incident handling to `docs/05.operations/**`.

## Link Basis

이 README의 링크 기준 위치는 `docs/90.references/data/`다.

- 같은 data reference 문서는 `./`로 연결한다.
- sibling reference folders는 `../audits/`, `../learning/`, `../llm-wiki/`,
  `../research/`로 연결한다.
- canonical owner stage는 `../../00.agent-governance/`,
  `../../03.specs/`, `../../05.operations/`로 연결한다.

## Data Reference Index

| Document | Reference Type | Role | Freshness Trigger |
| --- | --- | --- | --- |
| [Agent Reference Index](./agent-reference-index.md) | durable-concept / data-catalog | Agent reference boundaries and canonical owner routing | Agent reference document addition, runtime roster movement, or Stage 00 routing change |
| [Tech Stack Version Inventory](./tech-stack-version-inventory.md) | version-contract-inventory / external-standard-snapshot | Repo-backed version contracts and cloud example snapshots | Manifest/config/example version change or official support-range change |

## Authority Boundary

- `data/` owns factual lookup data and source-checked reference inventories.
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
