# 90.references/audits

## Overview

`docs/90.references/audits/` stores implementation audit reports for
workspace governance, harness behavior, provider adapters, and delivery
practices. Audit reports are dated reference snapshots. They preserve what was
checked, what repo-backed evidence existed at the time, and what follow-up was
recommended without redefining active policy or runtime behavior.

## Audience

This README is for:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

This folder is for dated audit snapshots, implementation matrices, evidence
summaries, gap notes, automation opportunities, and links to canonical owners.

This folder is not for active requirements, architecture decisions,
implementation contracts, execution plans, operations runbooks, provider
runtime configuration, credentials, or live cluster procedure. Those remain in
their owning stages and may be linked here as evidence.

## Structure

```text
docs/90.references/audits/
├── 2026-05-24-whga/
│   └── workspace-harness-gap-analysis.md
├── 2026-07-02-whia/
│   ├── workspace-governance-implementation-audit.md
│   ├── harness-loop-implementation-audit.md
│   ├── provider-harness-loop-implementation-audit.md
│   └── sdlc-delivery-practices-implementation-audit.md
├── 2026-07-03-wdgh/
│   └── workspace-document-governance-hardening-audit.md
├── 2026-07-04-wdcn/
│   └── workspace-document-contract-normalization-audit.md
├── 2026-07-05-wea/
│   ├── README.md
│   ├── governance-harness-loop-providers.md
│   ├── sdlc-ci-qa-formatting-automation.md
│   ├── kubernetes-infrastructure-security.md
│   └── implementation-roadmap-and-automation-opportunities.md
├── 2026-07-11-weia/
│   ├── README.md
│   ├── implementation-plan.md
│   ├── governance-harness-loop-providers.md
│   ├── sdlc-document-lifecycle-frontmatter.md
│   ├── ci-qa-automation-pipeline-workflow.md
│   ├── kubernetes-infrastructure-security.md
│   ├── ai-agents-model-routing-vibe-coding.md
│   └── remediation-roadmap.md
└── README.md
```

The dated audit reports are listed as resolved Markdown links in the Audit
Report Index once created. Future planned reports should stay as code literals
until their files exist.

Dated audit packs must use `YYYY-MM-DD-<sdlc_key>/` folders. Report files inside
a pack use semantic topic names only; do not use `part-*.md` or numeric
order-prefix filenames for current reports.

## How to Work in This Area

1. Start from the parent Spec, Plan, task record, and current research pack.
2. Use `docs/99.templates/templates/common/reference.template.md` for authored audit reports.
3. Treat research references as the benchmark model and repository files as
   local implementation evidence.
4. Keep audit findings factual, dated, and explicitly bounded to the checked
   evidence.
5. Update this README and the Stage 04 task record when adding or refreshing an
   audit report.

## Link Basis

This README is located at `docs/90.references/audits/`.

- Parent reference hub links start with `../`.
- Other docs stages use `../../<stage>/...`.
- Repository-root files use `../../../<path>`.
- Reports inside the same dated audit folder use folder-relative links.
- Planned but missing reports should stay as code literals until created.

## Audit Report Index

| Report | Availability | Purpose |
| --- | --- | --- |
| [2026-05-24-whga/workspace-harness-gap-analysis.md](./2026-05-24-whga/workspace-harness-gap-analysis.md) | Historical snapshot | Historical workspace harness gap-analysis reference. |
| [2026-07-02-whia/workspace-governance-implementation-audit.md](./2026-07-02-whia/workspace-governance-implementation-audit.md) | Historical snapshot | Workspace rules, systems, environment, operating contracts, templates, scripts, shared provider structure, and automation opportunities at that cutoff. |
| [2026-07-02-whia/harness-loop-implementation-audit.md](./2026-07-02-whia/harness-loop-implementation-audit.md) | Historical snapshot | Harness engineering and loop engineering implementation status against the then-current research benchmark. |
| [2026-07-02-whia/provider-harness-loop-implementation-audit.md](./2026-07-02-whia/provider-harness-loop-implementation-audit.md) | Historical snapshot | Claude, Codex, Gemini, and common provider harness/loop parity at that cutoff. |
| [2026-07-02-whia/sdlc-delivery-practices-implementation-audit.md](./2026-07-02-whia/sdlc-delivery-practices-implementation-audit.md) | Historical snapshot | Spec-driven development, SDLC, CI/CD, QA, formatting, and validation evidence lanes at that cutoff. |
| [2026-07-03-wdgh/workspace-document-governance-hardening-audit.md](./2026-07-03-wdgh/workspace-document-governance-hardening-audit.md) | Resolved snapshot | Baseline workspace document governance inventory, README drift classes, provider traceability, and CI/QA evidence routing with a 2026-07-04 resolution overlay. |
| [2026-07-04-wdcn/workspace-document-contract-normalization-audit.md](./2026-07-04-wdcn/workspace-document-contract-normalization-audit.md) | Resolved snapshot | Frontmatter, section, template, reference, archive, CI/QA, and historical-evidence drift inventory for workspace document contract normalization. |
| [2026-07-05-wea/README.md](./2026-07-05-wea/README.md) | Historical pack | Replaced workspace engineering implementation audit pack entrypoint and evidence rules. |
| [2026-07-05-wea/governance-harness-loop-providers.md](./2026-07-05-wea/governance-harness-loop-providers.md) | Historical snapshot | Governance, harness, loop, Claude, Codex, Gemini, and common provider implementation audit at that cutoff. |
| [2026-07-05-wea/sdlc-ci-qa-formatting-automation.md](./2026-07-05-wea/sdlc-ci-qa-formatting-automation.md) | Historical snapshot | Spec-driven development, SDLC, CI/CD, QA, formatting, linting, automation, pipeline, and workflow audit at that cutoff. |
| [2026-07-05-wea/kubernetes-infrastructure-security.md](./2026-07-05-wea/kubernetes-infrastructure-security.md) | Historical snapshot | Kubernetes, infrastructure, GitOps, secrets, policy, network, supply-chain, and security audit at that cutoff. |
| [2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md](./2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md) | Historical roadmap | Replaced cross-report roadmap, priority matrix, automation candidates, and task routing. |
| [2026-07-11-weia/README.md](./2026-07-11-weia/README.md) | Current pack | Current workspace engineering implementation audit pack, method, evidence boundary, and completed report index. |
| [2026-07-11-weia/implementation-plan.md](./2026-07-11-weia/implementation-plan.md) | Execution ledger | Completed Stage 90 implementation, whole-branch review, and final repository-static publication ledger. |
| [2026-07-11-weia/governance-harness-loop-providers.md](./2026-07-11-weia/governance-harness-loop-providers.md) | Included | Governance, harness, loop, provider, and common-system audit. |
| [2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md](./2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md) | Included | SDLC, document-family, lifecycle, lineage, Release, incident, and frontmatter audit. |
| [2026-07-11-weia/ci-qa-automation-pipeline-workflow.md](./2026-07-11-weia/ci-qa-automation-pipeline-workflow.md) | Included | CI/CD, QA, formatting, linting, automation, pipeline, workflow, and supply-chain audit. |
| [2026-07-11-weia/kubernetes-infrastructure-security.md](./2026-07-11-weia/kubernetes-infrastructure-security.md) | Included | Kubernetes, infrastructure, GitOps, Vault/ESO, network, policy, and security audit. |
| [2026-07-11-weia/ai-agents-model-routing-vibe-coding.md](./2026-07-11-weia/ai-agents-model-routing-vibe-coding.md) | Included | Local AI roles, `agency-agents`, model routing, and vibe-coding audit. |
| [2026-07-11-weia/remediation-roadmap.md](./2026-07-11-weia/remediation-roadmap.md) | Included | Integrated 32-finding remediation roadmap and follow-up SDLC disposition. |

## Status Vocabulary

`Implemented`, `Partial`, `Gap`, and `Not in scope` are the only audit status
values.

| Audit Status | Meaning |
| --- | --- |
| `Implemented` | Repo-backed evidence shows the capability exists and is documented in the canonical owner. |
| `Partial` | Some evidence exists, but parity, automation, coverage, enforcement, or documentation is incomplete. |
| `Gap` | The expected capability is relevant but no sufficient repo-backed implementation evidence was found. |
| `Not in scope` | The capability is intentionally outside the workspace boundary or requires human-approved future work. |

## Evidence Rules

- Repo-backed evidence outranks upstream capability for local implementation
  status.
- Repo-static validation does not imply live runtime readiness.
- External provider capability may inform the benchmark model, but it does not
  prove local implementation unless a repository surface implements or routes
  it.
- Ambiguous evidence should be recorded as `Partial` or `Gap`; do not infer
  `Implemented` without a repo-backed owner.
- Do not inspect secret values or claim live k3d, ArgoCD, Vault, ESO,
  Kubernetes, cloud, provider runtime, paid-job, or external-service readiness
  unless a separate approved task performs that live validation.

## Related Documents

- [Parent Reference README](../README.md)
- [Workspace Harness Implementation Audit Pack Spec](../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- [Workspace Harness Implementation Audit Pack Plan](../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md)
- [Workspace Harness Implementation Audit Pack Task](../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)
- [Workspace Harness Research Pack README](../research/README.md)
- [Reference Template](../../99.templates/templates/common/reference.template.md)
- [README Template](../../99.templates/templates/common/readme.template.md)
