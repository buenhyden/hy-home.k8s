---
title: "90.references/research"
version: "0.1.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-04"
layer: "references"
---
# 90.references/research

> Workspace harness research pack references, source ledgers, and durable research synthesis live here.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../../.agents/README.md).

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
│   ├── README.md
│   ├── m0011-agent-memory-tiers-and-management.md
│   ├── m0010-agent-model-routing-and-configuration.md
│   ├── m0009-ai-agents-and-agency-agents.md
│   ├── m0008-ci-cd-github-actions-and-qa.md
│   ├── m0005-documentation-architecture-and-diataxis.md
│   ├── m0002-harness-and-loop-engineering.md
│   ├── m0007-kubernetes-infrastructure-and-security.md
│   ├── m0006-llm-wiki-and-knowledge-routing.md
│   ├── m0003-provider-implementation-status.md
│   ├── m0013-scope-application-index.md
│   ├── m0012-source-coverage.md
│   ├── m0004-spec-driven-sdlc-and-document-contracts.md
│   └── m0001-workspace-governance-and-common-agent-environment.md
└── README.md                            # This file
```

### Research Pack Index

| Material                                                                                                                      | Status      | Role                                                                      | Authority Boundary                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [README.md](./README.md)                                                                                                      | Index       | Research folder entry point and source-priority guide                     | Authoritative for folder routing only; not active policy                                                  |
| [0001-workspace-engineering/README.md](./0001-workspace-engineering/README.md)                                                                        | Active pack | Successor workspace engineering research pack entry point                 | Research routing and observation-dated coverage only; canonical owners retain current authority           |
| [m0011-agent-memory-tiers-and-management.md](./0001-workspace-engineering/m0011-agent-memory-tiers-and-management.md)                                 | Active pack | Working, durable, domain-scoped, and provider-local memory research       | Descriptive reference only; memory lifecycle contract remains with Stage 00                               |
| [m0010-agent-model-routing-and-configuration.md](./0001-workspace-engineering/m0010-agent-model-routing-and-configuration.md)                         | Active pack | Model-routing and configuration research                                  | Descriptive reference only; provider availability and observed model resolution require separate evidence |
| [m0009-ai-agents-and-agency-agents.md](./0001-workspace-engineering/m0009-ai-agents-and-agency-agents.md)                                             | Active pack | AI-agent-system and agency-agents research                                | Descriptive reference only; roster and admission remain with canonical Stage 00 owners                    |
| [m0008-ci-cd-github-actions-and-qa.md](./0001-workspace-engineering/m0008-ci-cd-github-actions-and-qa.md)                                             | Active pack | CI/CD, GitHub Actions, and QA research                                    | Descriptive reference only; static validation does not prove hosted CI or deployment                      |
| [m0005-documentation-architecture-and-diataxis.md](./0001-workspace-engineering/m0005-documentation-architecture-and-diataxis.md)                     | Active pack | Documentation architecture and Diátaxis research                          | Descriptive mapping only; document profiles and templates remain canonical                                |
| [m0002-harness-and-loop-engineering.md](./0001-workspace-engineering/m0002-harness-and-loop-engineering.md)                                           | Active pack | Harness components, loop state machine, recovery, and evaluation research | Descriptive reference only; Stage 00 contracts remain the executable control owners                       |
| [m0007-kubernetes-infrastructure-and-security.md](./0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md)                       | Active pack | Kubernetes, infrastructure, GitOps, and security research                 | Descriptive reference only; no live-cluster or active security-policy claim                               |
| [m0006-llm-wiki-and-knowledge-routing.md](./0001-workspace-engineering/m0006-llm-wiki-and-knowledge-routing.md)                                       | Active pack | LLM-WIKI routing and knowledge-management research                        | Descriptive reference only; generated/index owners remain canonical                                       |
| [m0003-provider-implementation-status.md](./0001-workspace-engineering/m0003-provider-implementation-status.md)                                       | Active pack | Claude/Codex product-surface and static-adapter status research           | Product and static evidence only; native discovery/authenticated runtime remain separate                  |
| [m0013-scope-application-index.md](./0001-workspace-engineering/m0013-scope-application-index.md)                                                     | Active pack | Governance-scope routing over the pack's requirement coverage             | Routing index only; Stage 00 scopes retain scope authority and the pack README retains status authority   |
| [m0012-source-coverage.md](./0001-workspace-engineering/m0012-source-coverage.md)                                                   | Active pack | Source and claim coverage with bounded historical disposition             | Preserves provenance; it does not make external or runtime claims authoritative                           |
| [m0004-spec-driven-sdlc-and-document-contracts.md](./0001-workspace-engineering/m0004-spec-driven-sdlc-and-document-contracts.md)                     | Active pack | Spec-driven SDLC and document-contract research                           | Descriptive reference only; lifecycle documents and templates retain authority                            |
| [m0001-workspace-governance-and-common-agent-environment.md](./0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md) | Active pack | Provider-neutral workspace control-plane research                         | Descriptive reference only; provider permissions and active governance remain canonical elsewhere         |

`Active pack` and `Index` are collection roles,
not report lifecycle values. This collection declares no Current pack in the
document-profile registry; report lifecycle is owned by the selected pack's
`## Report Index`, and source coverage is owned by the active pack's
[source coverage](./0001-workspace-engineering/m0012-source-coverage.md).

Current research packs exist only at `research/####-<slug>/`. The four-digit
number is unique within Research and the slug is semantic kebab-case, never a
date. Reference files inside a pack use semantic topic names only; do not use
`part-*.md`, dates, or numeric order prefixes for current report filenames.

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
- [Workspace Engineering Research Pack Spec](../../98.archive/completed/03.specs/0017-workspace-engineering-research-pack/spec.md)
- [Workspace Harness Research Pack Spec](../../98.archive/completed/03.specs/0009-workspace-harness-research-pack/spec.md)
- [Workspace Harness Research Pack Plan](../../98.archive/completed/03.specs/0009-workspace-harness-research-pack/plan.md)
- [Workspace Harness Research Pack Plan](../../98.archive/completed/03.specs/0009-workspace-harness-research-pack/plan.md)
- [Research Reference Template](../../99.templates/templates/references/research.template.md)
- [Templates README](../../99.templates/README.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
