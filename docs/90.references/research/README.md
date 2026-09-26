---
title: "90.references/research"
version: "0.1.1"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-15"
layer: "references"
---
# 90.references/research

> Workspace harness research pack references, source ledgers, and durable research synthesis live here.

> [!NOTE]
> 이 디렉터리에서 이루어지는 모든 AI 에이전트 작업은 [Agent Governance Hub](../../../.agents/README.md)를 따른다.

## Overview

`research/` stores durable reference material for workspace harness and
workspace engineering research packs. It is a stable lookup area for
source-backed findings, observation-dated source checks, and synthesis that later plans,
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

- Workspace harness research pack index material
- Durable source ledgers and source-priority notes
- Official-source and repo-backed evidence summaries
- Non-authoritative market scan summaries when clearly labeled
- Pack READMEs created from `docs/99.templates/templates/references/research-pack.template.md`
- Reports created from `docs/99.templates/templates/references/research.template.md`

### Out of Scope

- Active governance policy or provider execution rules
- Runtime roster changes, hook wiring, or permission changes
- Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime, or secret checks
- Operational runbooks, release gates, deployment approvals, or incident response
- Generated or parallel `docs/superpowers/**` content

## Item Index

```text
research/
├── 0001-workspace-engineering/
├── 0002-archive-retention-and-provenance/
└── README.md
```

### Research Pack Index

| Pack | Role | Authority Boundary |
| --- | --- | --- |
| [0001-workspace-engineering/](./0001-workspace-engineering/) | Successor workspace engineering research pack | Research routing and observation-dated coverage only; canonical owners retain current authority |
| [0002-archive-retention-and-provenance/](./0002-archive-retention-and-provenance/) | Archive retention and provenance research pack | Research routing and observation-dated evidence only; canonical owners retain current authority |

Each pack README owns its own `## Report Index`, including report lifecycle
and source coverage; this collection lists packs only and declares no Current
pack in the document-profile registry.

Current research packs exist only at `research/####-<slug>/`. The four-digit
number is unique within Research and the slug is semantic kebab-case, never a
date. A report inside a pack carries the registry-mandated `m####-` identity
prefix followed by a semantic topic name. That prefix is an identity, not an
ordering key: do not add `part-*.md`, a date, or a second ordering prefix to a
current report filename.

## Add and Find

1. Read the parent spec, plan, and task before adding or changing research pack material.
2. Create the pack README with
   [research-pack.template.md](../../99.templates/templates/references/research-pack.template.md)
   and authored reports with
   [research.template.md](../../99.templates/templates/references/research.template.md).
3. Keep source claims factual, dated, and explicitly bounded by `Source checked`, `Sources`, and `Review and Freshness`.
4. Prefer official documentation and repo-backed evidence over market scan material.
5. Label market findings as non-authoritative, and do not use them to override official or repo-backed sources.
6. Route active policy, implementation contracts, runbooks, and task evidence back to their canonical owners instead of redefining them here.
7. Update this README, the parent [90.references README](../README.md), and the task record when research pack structure or validation evidence changes.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/research/`다.

- Same-folder research references use `./` only after the target file exists.
- Numbered semantic pack references use `./0001-workspace-engineering/<filename>.md` after the target
  file exists.
- Parent reference routing uses `../README.md`.
- Canonical owner stages use `../../../.agents/`, `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, and `../../05.operations/`.
- Root-level repository sources use `../../../<path>` from authored research reference files.
- Optional or planned target paths remain code literals until the target exists.

### Source Priority

Use the following priority order when research sources disagree:

1. Canonical repo owners for local policy, contracts, tasks, and operations.
2. Official product, provider, standards, and upstream project documentation for external facts.
3. Repo-backed evidence such as committed manifests, scripts, configs, and templates.
4. Official issue trackers, release notes, and implementation repositories when they clarify current behavior.
5. Market scan, vendor marketing, blog, forum, benchmark, or comparison material.

Market scan findings are non-authoritative. They may inform context, landscape,
or terminology, but they must be labeled as market scan material and cannot
override official documentation, repo-backed evidence, or canonical repository
owners.

## Related Documents

- [90.references README](../README.md)
- [Workspace Engineering Research Pack](./0001-workspace-engineering/README.md)
- [Archive Retention and Provenance Research Pack](./0002-archive-retention-and-provenance/README.md)
- [Archive index](../../98.archive/README.md) routes the retired packs that
  preceded this collection; no active document links their bodies directly.
- [Research Reference Template](../../99.templates/templates/references/research.template.md)
- [Templates README](../../99.templates/README.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
