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

### Source Ledger Contract

[`reference-information-architecture.json`](./reference-information-architecture.json)
records one source-ledger entry for every tracked data asset in this directory
other than this routing README. Each entry names the exact repository evidence,
a non-empty refresh trigger, and closed source records with an official HTTPS
URL, strict `checkedOn` date, adopted scope, and rejected scope.

`checkedOn` proves only that the cited source and stated scope were inspected by
that date. It does not prove current URL availability, remote execution, CI, or
live environment state. The offline validator performs no network request;
instead it bounds source dates by the contract `evidenceCutoff` and verifies
repository evidence through the exact stage-zero index blob plus no-follow
worktree boundary. Refresh remains event-driven rather than an invented common
expiry interval, and external sources do not inherit local policy authority.

## Item Index

```text
data/
├── active-corpus-retention-census.json # ACER-001 immutable corpus census and dispositions
├── active-corpus-eligibility-ledger.json # ACER-002 pinned dry-run eligibility ledger
├── active-corpus-migration-results.json # ACER-003 closed atomic migration results
├── active-corpus-role-audit.json # ACER-004 Stage 05 and helper role audit
├── active-corpus-residue-closure.json # ACER-006 terminal closure evidence, cardinality, and authority guards
├── agent-reference-index.md          # Durable Agent reference catalog boundary
├── reference-information-architecture.json # RIA closed reference architecture contract
├── reference-information-architecture.schema.json # RIA Draft 2020-12 schema
├── tech-stack-version-inventory.md   # Repo-backed version contracts and cloud snapshots
├── pod-security-compliance-inventory.md # PSS Baseline/Restricted verdicts for every deployed workload
├── istio-cni-adoption-evaluation.md  # Istio CNI effect, cost, and k3d-specific risk
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
| [Active Corpus Migration Results](./active-corpus-migration-results.json) | repo-backed closed migration-result ledger | Exact complete six-pair deterministic eligible-prefix ACER-003 corpus, twelve Plan/Task records, immutable 31/202 archive base plus 160 additive historical links, exact source/archive identities, repaired current-or-migrated-original consumers, pinned committed five-batch prefix, Spec/program closure owners, archive navigation boundary, validation results, and the exact rollback-parent chain without a self-referential batch commit | Archive/index drift, consumer repair, validation result, or rollback-parent change |
| [Active Corpus Role Audit](./active-corpus-role-audit.json) | repo-backed closed role-audit ledger | ACER-004 exact 24-record Stage 05 corpus and frozen 33-helper ledger, including exact paths, formats, roles, remediation inventory, and zero findings; exactly eight manifested RIA identities—seven named JSON fixtures (`current-owner`, `generator-collision`, `minimal-valid`, `overlay-mutation`, `policy-copy`, `snapshot-mutation`, `source-freshness`) and the RIA Python regression test—form the separate post-closure partition without rewriting this ledger or downstream ACER counts | Stage 05 authored-record change, frozen helper drift, post-closure identity/role manifest drift, current helper/README safety drift, or Spec 037 closure |
| [Active Corpus Residue Closure](./active-corpus-residue-closure.json) | repo-backed closed post-cutover ledger | ACER-006 preserves immutable reviewed inputs while recording 12 migrated-closed rows, 100 current Stage 04 `DEFER`/0 `retain`, exact 52-key 48/1/3 cardinality, 13 accepted ADR and 29 done-Spec guards, the ACER-004 24/33/0 dependency, and eight empty finding classes | Exact successor migration evidence, current Plan/Task inventory or authority, migration/archive result, ADR/Spec authority, ACER-004 input, strict link evidence, closure commit, or post-commit result change |
| [Agent Reference Index](./agent-reference-index.md) | durable-concept / data-catalog | Agent reference boundaries and canonical owner routing | Agent reference document addition, runtime roster movement, or Stage 00 routing change |
| [Reference Information Architecture Contract](./reference-information-architecture.json) | closed repository-static contract | Pins the exact registry-derived Current pack IDs to committed baselines and owns immutable Historical guards, bounded Current projections, the offline source ledger, and a one-shot transition/settlement FSM; it does not copy Current members, paths, digests, states, or pointers | Current-pack registry, protected observation bytes, declared projection, source-ledger relation, or baseline-state change |
| [Reference Information Architecture Schema](./reference-information-architecture.schema.json) | Draft 2020-12 schema | Closed schema-v2 form for Historical guards, exact Current baseline pins, bounded projections, source/scope/freshness records, and transition/settlement records; the validator adds strict calendar, HTTPS, duplicate, and safe repository-evidence semantics without network access | Contract field, source-ledger shape, fixed runner, projection, or baseline-FSM change |
| [Tech Stack Version Inventory](./tech-stack-version-inventory.md) | version-contract-inventory / external-standard-snapshot | Repo-backed version contracts and cloud example snapshots | Manifest/config/example version change or official support-range change |
| [Pod Security Compliance Inventory](./pod-security-compliance-inventory.md) | platform-compliance-inventory / external-standard-snapshot | Baseline/Restricted verdicts for all 26 deployed workloads, keyed to this repository's own values | Chart version change, Application helm.values change, repo-authored securityContext change, or PSS profile revision |
| [Istio CNI Adoption Evaluation](./istio-cni-adoption-evaluation.md) | adoption-evaluation / external-standard-snapshot | Effect on injected pod privilege, the privilege relocation it causes, and k3d-specific paths and risks | Istio minor version change, k3d/k3s CNI path change, or ambient mode evaluation |

### Authority Boundary

- `data/` owns factual lookup data and source-checked reference inventories.
- The RIA source ledger owns source/scope/freshness metadata for this category,
  not the policy or runtime authority of any cited source or repository asset.
- `active-corpus-retention-census.json` is immutable ACER-001 input evidence;
  it does not authorize archive migration, infer current worktree state, or
  promote any row to `eligible`.
- `active-corpus-eligibility-ledger.json` is ACER-002 dry-run evidence only;
  its eligibility result does not create an archive payload, index row, or migration.
- `active-corpus-migration-results.json` is the additive ACER-003 cutover
  authority. It joins the immutable census and eligibility inputs, admits only
  a complete deterministic eligible prefix, and records current cutover state
  without rewriting either reviewed input snapshot.
- `active-corpus-role-audit.json` is ACER-004 repository-static evidence. It
  preserves real operation records, treats empty Incident/Postmortem
  collections as valid, and freezes the reviewed 33-helper corpus and README
  remediation. The validator separately reports the current 41-helper corpus
  as 33 frozen plus eight exact manifested RIA helpers: the `current-owner`,
  `generator-collision`, `minimal-valid`, `overlay-mutation`, `policy-copy`,
  `snapshot-mutation`, and `source-freshness` JSON fixtures plus the RIA Python
  regression test, with the canonical 13/21/6/1 format split. A supported extension or
  sorted `tests/README.md` row cannot create another post-closure role; every
  admitted helper also remains an authoritative safe regular read and exact
  README member. Neither partition claims live/runtime state.
- `active-corpus-residue-closure.json` is the ACER-006 terminal closure proposal.
  It keeps the twelve historical `migrated-closed` rows and immutable source
  joins, records all 100 current Stage 04 rows as owned `DEFER`, preserves the
  complete Spec 037 pair as terminal evidence pending exact successor migration
  evidence, and rejects terminal-status-only ADR or Spec movement.
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
