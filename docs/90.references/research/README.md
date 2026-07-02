# 90.references/research

> Workspace harness research pack references, source ledgers, and durable research synthesis live here.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

`research/` stores durable reference material for the workspace harness research
pack. It is a stable lookup area for source-backed findings, dated source
checks, and synthesis that later plans, specs, guides, or tasks can cite without
turning this folder into an active policy owner.

This folder does not define active governance policy, runtime permissions,
deployment procedure, live cluster readiness, or provider contracts. Those stay
with their canonical owners in `docs/00.agent-governance/`, `docs/03.specs/`,
`docs/04.execution/`, and `docs/05.operations/`.

## Audience

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
- Reference documents created from `docs/99.templates/reference.template.md`

### Out of Scope

- Active governance policy or provider execution rules
- Runtime roster changes, hook wiring, or permission changes
- Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime, or secret checks
- Operational runbooks, release gates, deployment approvals, or incident response
- Generated or parallel `docs/superpowers/**` content

## Structure

```text
research/
├── workspace-governance-baseline.md     # Current durable governance baseline reference
├── harness-and-loop-engineering.md      # Planned harness and feedback-loop engineering reference
├── provider-implementation-status.md    # Planned provider implementation status reference
├── spec-sdlc-ci-qa-formatting.md        # Planned spec, SDLC, CI, QA, and formatting reference
└── README.md                            # This file
```

## How to Work in This Area

1. Read the parent spec, plan, and task before adding or changing research pack material.
2. Create authored reference documents with [reference.template.md](../../99.templates/reference.template.md).
3. Keep source claims factual, dated, and explicitly bounded by `Source checked`, `Sources`, and `Review and Freshness`.
4. Prefer official documentation and repo-backed evidence over market scan material.
5. Label market findings as non-authoritative, and do not use them to override official or repo-backed sources.
6. Route active policy, implementation contracts, runbooks, and task evidence back to their canonical owners instead of redefining them here.
7. Update this README, the parent [90.references README](../README.md), and the task record when research pack structure or validation evidence changes.

## Link Basis

이 README의 링크 기준 위치는 `docs/90.references/research/`다.

- Same-folder research references use `./` only after the target file exists.
- Parent reference routing uses `../README.md`.
- Canonical owner stages use `../../00.agent-governance/`, `../../03.specs/`, `../../04.execution/`, and `../../05.operations/`.
- Root-level repository sources use `../../../<path>` from authored research reference files.
- Optional or planned target paths remain code literals until the target exists.

## Research Pack Index

| Material | Status | Role | Authority Boundary |
| --- | --- | --- | --- |
| [README.md](./README.md) | Current | Research folder entry point and source-priority guide | Authoritative for folder routing only; not active policy |
| [workspace-governance-baseline.md](./workspace-governance-baseline.md) | Current | Durable workspace governance baseline reference | Summarizes canonical governance owners; does not replace them |
| `harness-and-loop-engineering.md` | Planned | Harness and feedback-loop engineering reference | Summarizes source-backed patterns; does not define runtime procedure |
| `provider-implementation-status.md` | Planned | Provider implementation status and source ledger | Official and repo-backed sources outrank market scan; market findings are non-authoritative |
| `spec-sdlc-ci-qa-formatting.md` | Planned | Spec, SDLC, CI, QA, and formatting reference | Summarizes reference material; active gates stay with canonical owners |

## Source Priority

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
- [Workspace Harness Research Pack Spec](../../03.specs/009-workspace-harness-research-pack/spec.md)
- [Workspace Harness Research Pack Plan](../../04.execution/plans/2026-07-02-workspace-harness-research-pack.md)
- [Workspace Harness Research Pack Task](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md)
- [Reference Template](../../99.templates/reference.template.md)
- [Templates README](../../99.templates/README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
