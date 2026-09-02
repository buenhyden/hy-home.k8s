# 90.references/audits

> Implementation audit packs, their reports, and durable audit evidence live here.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

`audits/` stores durable audit material: observation-dated checks of what the
repository actually contains, the method that produced each observation, and
the findings that follow from it. It is a stable lookup area that later plans,
specs, guides, or tasks can cite without turning this folder into an active
policy owner.

This folder does not define active governance policy, runtime permissions,
deployment procedure, live cluster readiness, or provider contracts. Those stay
with their canonical owners in `docs/00.agent-governance/`,
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

- Audit pack index material
- Observation-dated implementation and conformance checks
- Repo-backed finding evidence and its disposition
- Pack READMEs created from `docs/99.templates/templates/references/audit-pack.template.md`
- Reports created from `docs/99.templates/templates/references/audit-reference.template.md`

### Out of Scope

- Active governance policy or provider execution rules
- Runtime roster changes, hook wiring, or permission changes
- Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime, or secret checks
- Operational runbooks, release gates, deployment approvals, or incident response
- Generated or parallel `docs/superpowers/**` content

## Item Index

```text
audits/
└── README.md                          # This file
```

이 collection은 현재 audit pack을 보유하지 않는다. 이는 현재 처분 결과일 뿐이며,
고유한 목적과 출처 경계를 갖춘 audit pack의 추가를 금지하지 않는다.

## Add and Find

1. Read the parent spec, plan, and task before adding or changing audit pack material.
2. Create `audits/####-<slug>/README.md` with
   [audit-pack.template.md](../../99.templates/templates/references/audit-pack.template.md)
   and authored reports as `audits/####-<slug>/m####-<slug>.md` with
   [audit-reference.template.md](../../99.templates/templates/references/audit-reference.template.md).
3. Number pack members with the pack-internal `m####` sequence, and give each
   report the `AUD-####-m####` artifact identity of its pack.
4. Keep findings factual, dated, and explicitly bounded by their observation basis.
5. Route active policy, implementation contracts, runbooks, and task evidence back to their canonical owners instead of redefining them here.
6. Update this README, the parent [90.references README](../README.md), and the task record when audit pack structure or validation evidence changes.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/audits/`다.

- Numbered semantic pack references use `./####-<slug>/<filename>.md` after the target file exists.
- Parent reference routing uses `../README.md`.
- Canonical owner stages use `../../00.agent-governance/`, `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, and `../../05.operations/`.
- Root-level repository sources use `../../../<path>` from authored audit reference files.
- Optional or planned target paths remain code literals until the target exists.

## Related Documents

- [90.references README](../README.md)
- [Audit Pack Template](../../99.templates/templates/references/audit-pack.template.md)
- [Audit Reference Template](../../99.templates/templates/references/audit-reference.template.md)
- [Templates README](../../99.templates/README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
