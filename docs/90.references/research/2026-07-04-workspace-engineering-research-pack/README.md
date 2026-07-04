# Workspace Engineering Research Pack

## Overview

This dated pack collects repo-first workspace engineering research for
`hy-home.k8s`. It moves the existing workspace harness research references
under one dated folder, includes the current Kubernetes/infrastructure/security
reference, and reserves the planned automation, pipeline, workflow, and QA
reference for WER-007.

The pack is descriptive reference material. It does not define active
governance policy, CI semantics, runtime permissions, runbooks, deployment
approval, live cluster procedure, or secret handling procedure.

## Audience

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

In scope:

- Dated research-pack routing and file index
- Repo-backed workspace governance, harness, provider, SDLC, CI, QA, and
  formatting references
- Current Kubernetes/infrastructure/security reference and planned reference
  for automation/pipeline/workflow/QA
- Source priority, freshness, and authority-boundary reminders for later
  reference refresh work

Out of scope:

- Active policy, implementation contracts, runbooks, release gates, or CI job
  semantics
- Live Kubernetes, Argo CD, Vault, ESO, cloud, provider runtime, GitHub remote,
  credential, secret-value, paid-job, publishing, merge, push, or third-party
  mutation
- Refreshing the moved reference body content before the follow-up WER tasks

## Structure

```text
2026-07-04-workspace-engineering-research-pack/
|-- README.md
|-- workspace-governance-baseline.md        # Current
|-- harness-and-loop-engineering.md         # Current
|-- provider-implementation-status.md       # Current
|-- spec-sdlc-ci-qa-formatting.md           # Current
|-- kubernetes-infrastructure-security.md   # Current
`-- automation-pipeline-workflow-qa.md      # Planned
```

## Source Priority

Use this priority order when sources disagree:

1. Canonical repository owners for local policy, contracts, tasks, and
   operations.
2. Official product, provider, standards, and upstream project documentation
   for external facts.
3. Repo-backed evidence such as committed manifests, scripts, configs, and
   templates.
4. Official issue trackers, release notes, and implementation repositories
   when they clarify current behavior.
5. Market scan, vendor marketing, blog, forum, benchmark, or comparison
   material.

Market scan material is non-authoritative. It can support landscape context,
but it cannot override official sources, repo-backed evidence, or canonical
repository owners.

## How to Work in This Pack

1. Read the parent Spec, Plan, and Task record before changing pack material.
2. Keep moved references in this dated folder and preserve one current path for
   each moved reference.
3. Use the reference template for new authored references.
4. Keep source checked dates, sources, freshness triggers, and authority
   boundaries explicit.
5. Update this README, the parent research README, task evidence, and progress
   memory when pack structure or validation evidence changes.
6. Keep repo-static, CI/toolchain, and live-runtime evidence lanes separate.
7. Do not perform live or external mutation as part of this reference work.

## How to Work in This Area

Use the pack-specific workflow above. This heading is retained for the shared
README quality gate; the authority boundary and no-live-mutation rules are the
same as `How to Work in This Pack`.

## Link Basis

This README's link basis is
`docs/90.references/research/2026-07-04-workspace-engineering-research-pack/`.

- Current same-pack references use bare filename links after the target exists.
- Planned same-pack target names remain code literals until their files are
  created.
- The parent research README is `../README.md`.
- The parent Stage 90 README is `../../README.md`.
- Canonical docs stages use `../../../<stage>/`.
- Root-level repository sources use `../../../../<path>`.

## Pack Index

| Reference | Status | Role | Authority Boundary |
| --- | --- | --- | --- |
| [workspace-governance-baseline.md](workspace-governance-baseline.md) | Current | Repo-backed workspace governance baseline reference | Descriptive summary only; active governance remains in Stage 00 owners |
| [harness-and-loop-engineering.md](harness-and-loop-engineering.md) | Current | Harness and feedback-loop engineering reference | Descriptive source snapshot only; does not define runtime procedure |
| [provider-implementation-status.md](provider-implementation-status.md) | Current | Provider capability and local adapter status reference | Distinguishes provider capability from repo implementation; does not change provider config |
| [spec-sdlc-ci-qa-formatting.md](spec-sdlc-ci-qa-formatting.md) | Current | Spec, SDLC, CI, QA, formatting, and validation reference | Descriptive reference only; active gates stay with canonical owners |
| [kubernetes-infrastructure-security.md](kubernetes-infrastructure-security.md) | Current | Kubernetes, infrastructure, GitOps, secrets, policy, supply-chain, and security reference | Descriptive reference only; no live checks or active security policy changes |
| `automation-pipeline-workflow-qa.md` | Planned | Automation, pipeline, workflow, CI job graph, validation-loop, and QA evidence reference | Planned descriptive reference; no CI workflow or runtime changes |

## Authority Boundary

This pack is authoritative for dated reference routing, source-priority
reminders, and lookup-level summaries created under the pack. It is not
authoritative for active governance policy, provider runtime permissions,
workflow semantics, validation script behavior, operations procedure, release
approval, live runtime readiness, or secret-value handling.

When a reference identifies drift or a needed behavior change, route the change
to the canonical owner in Stage 00 governance, Stage 03 specs, Stage 04
execution, Stage 05 operations, scripts, workflows, templates, or provider
adapter files instead of encoding active policy here.

## Review and Freshness

- Review cadence: on source or structure change
- Last reviewed: 2026-07-05
- Next review trigger: pack structure changes, reference status changes,
  source-priority changes, parent Spec/Plan changes, or validation evidence
  changes.

## Related Documents

- [Research README](../README.md)
- [90.references README](../../README.md)
- [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- [Workspace Engineering Research Pack Plan](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
