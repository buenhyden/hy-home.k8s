---
title: "90.references/data"
version: "0.1.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-04"
layer: "references"
---
# 90.references/data

> Durable data packs, their datasets, and dataset provenance live here.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../../.agents/README.md).

## Overview

`data/` stores durable dataset material: the shape and provenance of data the
repository depends on, the collection method behind each snapshot, and its
refresh and retention boundary. It is a stable lookup area that later plans,
specs, guides, or tasks can cite without turning this folder into an active
policy owner.

This folder does not define active governance policy, runtime permissions,
deployment procedure, live cluster readiness, or provider contracts. Those stay
with their canonical owners in `.agents/`,
`docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, and
`docs/05.operations/`.

### Collection Readers

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Data pack index material
- Dataset shape, provenance, and collection-method records
- Observation-dated snapshots with an explicit refresh and retention boundary
- Pack READMEs created from `docs/99.templates/templates/references/data-pack.template.md`
- Datasets created from `docs/99.templates/templates/references/data.template.md`

### Out of Scope

- Active governance policy or provider execution rules
- Runtime roster changes, hook wiring, or permission changes
- Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime, or secret checks
- Secret values, credentials, or any unredacted sensitive record
- Operational runbooks, release gates, deployment approvals, or incident response

## Item Index

```text
data/
└── README.md                          # This file
```

이 collection은 현재 data pack을 보유하지 않는다. 이는 현재 처분 결과일 뿐이며,
고유한 목적과 출처 경계를 갖춘 data pack의 추가를 금지하지 않는다.

## Add and Find

1. Read the parent spec, plan, and task before adding or changing data pack material.
2. Create `data/####-<slug>/README.md` with
   [data-pack.template.md](../../99.templates/templates/references/data-pack.template.md)
   and authored datasets as `data/####-<slug>/m####-<slug>.md` with
   [data.template.md](../../99.templates/templates/references/data.template.md).
3. Number pack members with the pack-internal `m####` sequence, and give each
   dataset the `DATA-####-m####` artifact identity of its pack.
4. Record collection date, method, and retention boundary for every snapshot, and never store secret values.
5. Route active policy, implementation contracts, runbooks, and task evidence back to their canonical owners instead of redefining them here.
6. Update this README, the parent [90.references README](../README.md), and the task record when data pack structure or validation evidence changes.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/data/`다.

- Numbered semantic pack references use `./####-<slug>/<filename>.md` after the target file exists.
- Parent reference routing uses `../README.md`.
- Canonical owner stages use `../../../.agents/`, `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, and `../../05.operations/`.
- Root-level repository sources use `../../../<path>` from authored data reference files.
- Optional or planned target paths remain code literals until the target exists.

## Related Documents

- [90.references README](../README.md)
- [Data Pack Template](../../99.templates/templates/references/data-pack.template.md)
- [Data Reference Template](../../99.templates/templates/references/data.template.md)
- [Templates README](../../99.templates/README.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
