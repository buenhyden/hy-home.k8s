---
title: 'Workspace Engineering Research Pack Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-04
---

# Workspace Engineering Research Pack Technical Specification (Spec)

## Overview

This document defines the implementation contract for a dated, repo-first
research pack under
`docs/90.references/research/2026-07-04-workspace-engineering-research-pack/`.
The pack will synthesize the workspace purpose, roles, CI/CD, QA, formatting,
linting, automation, pipelines, workflows, operating contracts, templates,
scripts, integration guides, SDLC, governance, rules, Kubernetes,
infrastructure, and security.

The work is documentation-only. It must not mutate live Kubernetes, Argo CD,
Vault, cloud resources, GitHub remote state, credentials, or third-party
systems.

The brainstorming skill's default `docs/superpowers/specs/**` location is not
used because this repository's quality gate forbids `docs/superpowers` as a
top-level docs folder. Stage 03 is the repo-approved design/spec owner.

## Strategic Boundaries & Non-goals

In scope:

- Create a dated research pack folder under `docs/90.references/research/`.
- Move the four current flat research references into the dated pack folder.
- Refresh those four references with current repo evidence and verified
  official or primary external sources.
- Add two focused references for Kubernetes/infrastructure/security and
  automation/pipeline/workflow/QA.
- Update `docs/90.references/research/README.md` and parent reference indexes
  so the dated pack is discoverable and stale flat links are removed.
- Record source checked dates, freshness triggers, authority boundaries,
  market-scan limitations, and related documents.
- Track execution and validation through Stage 04 plan/task evidence and the
  progress ledger.

Out of scope:

- Live cluster, cloud, Vault, GitHub remote, or provider runtime mutation.
- Secret value inspection, credential regeneration, or certificate changes.
- Replacing current CI workflow architecture or installing external tools.
- Changing active governance policy except where a later implementation task
  explicitly routes documented drift to the canonical owner.
- Treating market scan material as authoritative.

## Related Inputs

- **PRD**: No separate PRD exists. The upstream requirement is the approved
  user request to build a dated workspace engineering research pack, move the
  existing four research documents into it, and include external source-backed
  analysis.
- **ARD**: No separate ARD exists. The architectural baseline is the current
  Stage 00 to Stage 99 documentation taxonomy and the existing
  `docs/90.references/**` reference contract.
- **Prior Specs**:
  - [Workspace Harness Research Pack](../009-workspace-harness-research-pack/spec.md)
  - [Workspace Harness Implementation Audit Pack](../010-workspace-harness-implementation-audit-pack/spec.md)
  - [Active Control Surface Governance Hardening](../016-active-control-surface-governance-hardening/spec.md)

Repository inputs:

- [90.references README](../../90.references/README.md)
- [Research README](../../90.references/research/README.md)
- [Reference Template](../../99.templates/templates/common/reference.template.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
- [Harness Validation Wrapper](../../../scripts/validate-harness.sh)

## Contracts

- **Config Contract**:
  - No runtime configuration, provider adapter, workflow job, GitOps manifest,
    or secret file changes are required by this spec.
  - The research pack lives only under
    `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/`.
  - The former flat research files are moved, not duplicated, so there is one
    current path for each moved reference.
- **Data / Interface Contract**:
  - Each authored reference uses `type: content/reference` frontmatter and the
    required reference sections from
    `docs/99.templates/templates/common/reference.template.md`.
  - `README.md` files remain folder entrypoints and do not copy the complete
    reference template.
  - Source claims include source checked dates and freshness triggers.
  - Market scan findings are labeled non-authoritative and cannot override
    official or repo-backed evidence.
- **Governance Contract**:
  - `docs/90.references/**` remains durable lookup material, not active
    policy, runbook, release gate, or runtime permission owner.
  - Active policy changes belong to Stage 00, Stage 05, workflows, scripts, or
    templates according to existing ownership.
  - External networked research is read-only. Posting, publishing, pushing,
    merging, credential mutation, or third-party state changes require separate
    human approval.

## Core Design

- **Component Boundary**:
  - `README.md`: pack purpose, reading order, file index, source priority,
    authority boundary, and market-scan warning.
  - `workspace-governance-baseline.md`: repo-first baseline for workspace
    purpose, roles, operating contract, templates, scripts, integration guides,
    SDLC, governance, system structure, rules, and current evidence lanes.
  - `harness-and-loop-engineering.md`: harness engineering and loop
    engineering definitions, elements, workspace application requirements,
    environment/rule needs, and implementation checklist items.
  - `provider-implementation-status.md`: Claude, Codex, and Gemini harness and
    loop capability comparison, including common environment, shared rules, and
    known differences between upstream capability and repo implementation.
  - `spec-sdlc-ci-qa-formatting.md`: spec-driven development, SDLC, CI/CD, QA,
    formatting, linting, syntax validation, and repo validation matrix mapping.
  - `kubernetes-infrastructure-security.md`: Kubernetes, infrastructure,
    GitOps, secrets, policy-as-code, supply-chain, and security source
    analysis.
  - `automation-pipeline-workflow-qa.md`: automation, pipeline, workflow, CI
    job graph, validation loops, QA evidence lanes, formatting/linting
    integration, and implementation checklist material.
- **Key Dependencies**:
  - Existing Stage 00 governance, Stage 90 references, Stage 99 templates,
    `.github`, scripts, GitOps, infrastructure, policy, tests, and Traefik
    evidence.
  - Official or primary external documentation verified during implementation.
  - Bounded market scan material labeled non-authoritative.
- **Tech Stack**:
  - Markdown, existing reference template, repository validation scripts,
    Git history, web research, and Stage 04 evidence records.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - The pack is a set of Markdown reference documents and README indexes.
  - The moved references retain their filenames and are updated in place after
    `git mv`.
  - New reference files use the same frontmatter keys as other current
    `content/reference` documents: `title`, `type`, `status`, `owner`, and
    `updated`.
- **Migration / Transition Plan**:
  - Create the dated pack folder.
  - Move the four current flat research references into it.
  - Update research and parent indexes.
  - Run stale-link focused scans.
  - Refresh content and add new references in later logical commits.

## Interfaces & Data Structures

### Research Pack Contract

```typescript
interface WorkspaceEngineeringResearchPack {
  root: "docs/90.references/research/2026-07-04-workspace-engineering-research-pack";
  references: [
    "workspace-governance-baseline.md",
    "harness-and-loop-engineering.md",
    "provider-implementation-status.md",
    "spec-sdlc-ci-qa-formatting.md",
    "kubernetes-infrastructure-security.md",
    "automation-pipeline-workflow-qa.md",
  ];
  requiredReferenceSections: [
    "Overview",
    "Purpose",
    "Reference Type",
    "Authority Boundary",
    "Scope",
    "Definitions / Facts",
    "Sources",
    "Review and Freshness",
    "Related Documents",
  ];
  sourcePriority: [
    "canonical repository owners",
    "official or primary external sources",
    "repo-backed evidence",
    "official issue trackers or release notes",
    "non-authoritative market scan material",
  ];
}
```

## API Contract (If Applicable)

No external API is introduced.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation and governance researcher operating under the
  repo-local docs, meta, QA, infra, and security scopes.
- **Inputs**: User-approved design, repo evidence, existing research
  references, official external sources, market scan sources, templates, and
  validation output.
- **Outputs**: Dated research pack folder, moved/updated references, new
  references, updated indexes, Stage 04 evidence, and progress memory.
- **Success Definition**: The dated pack exists, stale flat paths are removed,
  required topics are covered, source authority is explicit, validation passes,
  and no live or external mutation occurs.

## Tools & Tool Contract (If Applicable)

- **Tool List**:
  - `rg` and shell readers for repo evidence.
  - Web research for current external source verification.
  - `git mv` for moving existing research references.
  - `apply_patch` for manual document edits.
  - Repository validation scripts.
- **Permission Boundary**:
  - Read-only external research is allowed.
  - Remote push, PR creation, merge, publishing, credential changes, paid jobs,
    third-party mutation, live Kubernetes, Vault, cloud, or GitHub settings
    changes are not allowed without separate approval.
- **Failure Handling**:
  - If external sources conflict, official or repo-backed sources outrank
    market scan material.
  - If validation fails, fix the owning reference, index, template route, or
    stale link before proceeding.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**:
  - Follow repo-first and official-source-first research order.
  - Keep market scan material non-authoritative.
  - Keep active policy out of `docs/90.references/**`.
- **Policy Constraints**:
  - Respect approval boundaries for live mutation and external state changes.
  - Preserve one current path per moved research reference.
- **Versioning Rule**:
  - Use the dated pack folder as the version boundary for this refresh.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**:
  - Stage 04 plan and task records own execution order, evidence, and status.
- **Long-term Memory**:
  - `docs/00.agent-governance/memory/progress.md` records completion evidence
    and reusable routing lessons.
- **Retrieval Boundary**:
  - The research pack provides lookup context only. It does not become an
    execution rule source.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Verify external claims with web research before updating current source
    statements.
  - Treat missing or changed provider behavior as unknown until primary source
    evidence exists.
- **Output Guardrails**:
  - Every reference has authority boundary, sources, and freshness metadata.
  - Market scan text is labeled non-authoritative.
  - README files remain entrypoints, not policy bodies.
- **Blocked Conditions**:
  - Required source cannot be verified.
  - Moving references would leave unresolved stale links that cannot be fixed.
  - Repo quality gate fails repeatedly with unresolved ownership.
- **Escalation Rule**:
  - Stop and ask for clarification if a required source, canonical owner, or
    scope boundary is ambiguous enough to change the pack structure.

## Evaluation (If Applicable)

- **Eval Types**:
  - Structural validation, stale-link scans, source-authority review, and
    repo-static validation.
- **Metrics**:
  - All approved output files exist in the dated pack.
  - No current index points to removed flat research paths.
  - Required reference sections are present.
  - Repository quality gates pass.
- **Datasets / Fixtures**:
  - Existing Stage 90 research references, Stage 00 governance, Stage 99
    templates, scripts, workflow files, GitOps manifests, infrastructure
    docs, policy files, and official external documentation.
- **How to Run**:
  - Use the verification commands in this spec and the later Stage 04 plan.

## Edge Cases & Error Handling

- **Existing links to flat references**:
  - Update links to the dated pack path in the same move commit or an adjacent
    index commit.
- **Source drift during writing**:
  - Record the checked date and keep claims narrowly tied to the verified
    source.
- **Provider capability mismatch**:
  - Distinguish upstream provider capability from repo implementation status.
- **Optional tool absence**:
  - Report optional lint/policy tool absence as SKIP or fallback evidence, not
    as full coverage.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `docs/superpowers/**` or another non-canonical path is
  introduced.
  - **Fallback**: Move design and execution artifacts into the repo-approved
    Stage 03/04 taxonomy.
  - **Human Escalation**: Only needed if the user requires a path forbidden by
    the repository quality gate.
- **Failure Mode**: External source claims cannot be verified.
  - **Fallback**: Mark the claim as unknown or remove it.
  - **Human Escalation**: Ask before using non-primary sources for a material
    conclusion.
- **Failure Mode**: Validation fails because of stale links after moving files.
  - **Fallback**: Fix links and indexes before content refresh work continues.
  - **Human Escalation**: Ask only if multiple canonical paths are possible.

## Verification Commands

Required:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Recommended when the implementation touches validation-sensitive surfaces:

```bash
bash scripts/validate-harness.sh
```

Focused scans:

```bash
rg -n "docs/90.references/research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md" docs .github AGENTS.md CLAUDE.md GEMINI.md README.md scripts
rg -n "non-authoritative|market scan|Source checked|Review and Freshness" docs/90.references/research/2026-07-04-workspace-engineering-research-pack
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: The dated pack folder exists and contains one README, four
  moved references, and two new references.
- **VAL-SPC-002**: Root and parent reference indexes route to the dated pack
  and do not present removed flat research files as current direct paths.
- **VAL-SPC-003**: Each authored reference has required reference sections,
  source checked metadata, freshness triggers, and authority boundaries.
- **VAL-SPC-004**: The required topics are covered: workspace purpose, roles,
  CI/CD, QA, formatting, linting, syntax validation, automation, pipeline,
  workflow, operating contract, templates, scripts, integration guides, SDLC,
  governance, system/rules, security, Kubernetes, infrastructure, harness
  engineering, loop engineering, provider status, and spec-driven development.
- **VAL-SPC-005**: External-source claims are checked with official or primary
  sources where possible, and market scan material is labeled
  non-authoritative.
- **VAL-SPC-006**: Required validation commands pass, and Stage 04 task
  evidence records executed commands and limitations.
- **VAL-SPC-007**: No live Kubernetes, Argo CD, Vault, cloud, GitHub remote,
  provider runtime, credential, or third-party mutation occurs.

## Related Documents

- **Prior Spec**: [Workspace Harness Research Pack](../009-workspace-harness-research-pack/spec.md)
- **Prior Spec**: [Workspace Harness Implementation Audit Pack](../010-workspace-harness-implementation-audit-pack/spec.md)
- **Prior Spec**: [Active Control Surface Governance Hardening](../016-active-control-surface-governance-hardening/spec.md)
- **Plan**: `../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md`
- **Tasks**: `../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`
- **Research README**: [../../90.references/research/README.md](../../90.references/research/README.md)
- **Reference Template**: [../../99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md)
- **Reference Maintenance Runbook**: [../../05.operations/runbooks/0011-reference-maintenance-runbook.md](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
