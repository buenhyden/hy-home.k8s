---
title: 'Workspace Engineering Implementation Audit Pack Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-07-05
---

# Workspace Engineering Implementation Audit Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dated Stage 90 implementation audit pack and normalize the
existing audit folder structure.

**Architecture:** The work proceeds in documentation-only phases: create Stage
04 evidence, folderize existing audits with `git mv`, write four new part
reports against the current research benchmark, update indexes and memory, and
run static validation. Each audit report stays descriptive and routes active
changes to canonical owners instead of changing behavior.

**Tech Stack:** Markdown, Stage 90 reference template, Stage 04 plan/task
evidence, `git mv`, `rg`, repository quality gates, local link scans, and
subagent review.

---

## Overview

This document defines the implementation plan for
`docs/03.specs/018-workspace-engineering-implementation-audit-pack/spec.md`.
The implementation creates
`docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/`,
writes four part-based audit reports, moves existing root-level audit reports
into dated folders, updates indexes and references, and records validation
evidence.

The audit pack is descriptive reference material. It does not define active
policy, CI semantics, workflow behavior, validation script behavior, provider
runtime configuration, runbooks, deployment approval, live runtime readiness,
or secret handling.

## Context

The current research benchmark lives at:

```text
docs/90.references/research/2026-07-04-workspace-engineering-research-pack/
|-- README.md
|-- workspace-governance-baseline.md
|-- harness-and-loop-engineering.md
|-- provider-implementation-status.md
|-- spec-sdlc-ci-qa-formatting.md
|-- kubernetes-infrastructure-security.md
`-- automation-pipeline-workflow-qa.md
```

The approved new audit pack structure is:

```text
docs/90.references/audits/
`-- 2026-07-05-workspace-engineering-implementation-audit/
    |-- README.md
    |-- 01-governance-harness-loop-providers.md
    |-- 02-sdlc-ci-qa-formatting-automation.md
    |-- 03-kubernetes-infrastructure-security.md
    `-- 04-implementation-roadmap-and-automation-opportunities.md
```

Existing root-level audits are normalized into dated folders:

```text
docs/90.references/audits/
|-- 2026-05-24-workspace-harness-gap-analysis/
|   `-- workspace-harness-gap-analysis.md
|-- 2026-07-02-workspace-harness-implementation-audit-pack/
|   |-- workspace-governance-implementation-audit.md
|   |-- harness-loop-implementation-audit.md
|   |-- provider-harness-loop-implementation-audit.md
|   `-- sdlc-delivery-practices-implementation-audit.md
|-- 2026-07-03-workspace-document-governance-hardening-audit/
|   `-- workspace-document-governance-hardening-audit.md
`-- 2026-07-04-workspace-document-contract-normalization-audit/
    `-- workspace-document-contract-normalization-audit.md
```

## Goals & In-Scope

- **Goals**:
  - Create Stage 04 task evidence for the 2026-07-05 audit pack.
  - Move existing root audit reports into dated folders.
  - Add four current part reports comparing research benchmark items against
    repo-backed implementation evidence.
  - Update `docs/90.references/audits/README.md`, Stage 04 indexes, and
    progress memory.
  - Run focused stale-link scans and repository quality gates.
- **In Scope**:
  - `docs/90.references/audits/**`
  - `docs/04.execution/tasks/**`
  - `docs/04.execution/plans/README.md`
  - `docs/00.agent-governance/memory/progress.md`
  - Read-only evidence gathering across Stage 00/03/04/05/90/99 docs,
    `.github`, `.agents`, `.claude`, `.codex`, `scripts`, `gitops`,
    `infrastructure`, `policy`, `tests`, `examples`, and `traefik`.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Change active governance, provider adapter behavior, workflow semantics,
    scripts, GitOps manifests, policy rules, templates, or operations runbooks.
  - Prove live runtime or provider-runtime readiness.
  - Install tools or add external integrations.
- **Out of Scope**:
  - Live Kubernetes, Argo CD, Vault, ESO, cloud, provider runtime, GitHub
    remote, credentials, secret values, paid jobs, publishing, push, merge, PR
    creation, or third-party mutation.

## File Structure

| Path | Responsibility |
| --- | --- |
| `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md` | Execution evidence, task table, validation commands, limitations, and handoff. |
| `docs/04.execution/tasks/README.md` | Task index entry for this audit-pack implementation. |
| `docs/04.execution/plans/2026-07-05-workspace-engineering-implementation-audit-pack.md` | This implementation plan. |
| `docs/04.execution/plans/README.md` | Plan index entry for this plan. |
| `docs/90.references/audits/README.md` | Audits folder entrypoint, normalized folder index, status vocabulary, evidence rules, and related docs. |
| `docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis/workspace-harness-gap-analysis.md` | Folderized historical 2026-05-24 harness gap snapshot. |
| `docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/*.md` | Folderized 2026-07-02 four-report implementation audit pack. |
| `docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit/workspace-document-governance-hardening-audit.md` | Folderized 2026-07-03 document governance hardening audit snapshot. |
| `docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit/workspace-document-contract-normalization-audit.md` | Folderized 2026-07-04 document contract normalization audit snapshot. |
| `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/README.md` | New dated audit pack entrypoint and report index. |
| `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/01-governance-harness-loop-providers.md` | Governance, harness, loop, Claude, Codex, Gemini, and common provider implementation audit. |
| `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/02-sdlc-ci-qa-formatting-automation.md` | Spec-driven development, SDLC, CI/CD, QA, formatting, linting, automation, pipeline, and workflow audit. |
| `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/03-kubernetes-infrastructure-security.md` | Kubernetes, infrastructure, GitOps, secrets, policy, network, supply-chain, and security audit. |
| `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/04-implementation-roadmap-and-automation-opportunities.md` | Cross-report roadmap, priority matrix, automation candidates, and future task routing. |
| `docs/00.agent-governance/memory/progress.md` | Durable progress and reusable memory entry after audit completion. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| WEA-001 | Create task evidence and baseline inventory | Task record, tasks README, progress memory | VAL-SPC-007 | Baseline inventory recorded; repo-quality gate passes |
| WEA-002 | Folderize existing root audit reports | Audits folders, moved reports, audit README, current links | VAL-SPC-001, VAL-SPC-006 | `git mv` preserves history; stale old-path scan has no current broken links |
| WEA-003 | Add dated audit pack README and governance/harness/provider report | Audit pack README, `01-governance-harness-loop-providers.md` | VAL-SPC-002, VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Required topics and evidence matrix rows present |
| WEA-004 | Add SDLC/CI/QA/formatting/automation report | `02-sdlc-ci-qa-formatting-automation.md` | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | SDLC, CI/CD, QA, formatting, linting, automation, pipeline, workflow rows present |
| WEA-005 | Add Kubernetes/infrastructure/security report | `03-kubernetes-infrastructure-security.md` | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Kubernetes, infrastructure, GitOps, secrets, policy, security rows present |
| WEA-006 | Add roadmap and automation opportunities report | `04-implementation-roadmap-and-automation-opportunities.md` | VAL-SPC-004, VAL-SPC-005 | Cross-report roadmap and automation opportunities are owner-routed |
| WEA-007 | Close indexes, evidence, review, and validation | Audits README, task evidence, progress memory | VAL-SPC-006, VAL-SPC-007, VAL-SPC-008 | Final scans and quality gates pass; no mutation boundary violation |

## Detailed Tasks

### Task 1: Task Evidence and Baseline Inventory

**Files:**

- Create: `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Read: `docs/03.specs/018-workspace-engineering-implementation-audit-pack/spec.md`
- Read: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/README.md`
- Read: `docs/90.references/audits/README.md`

- [ ] **Step 1: Confirm branch and clean state**

Run:

```bash
git status --short --branch
```

Expected: branch is `codex/workspace-engineering-audit-pack` and there are no
uncommitted changes after the plan commit.

- [ ] **Step 2: Read task template and parent spec**

Run:

```bash
sed -n '1,220p' docs/99.templates/templates/sdlc/execution/task.template.md
sed -n '1,420p' docs/03.specs/018-workspace-engineering-implementation-audit-pack/spec.md
```

Expected: task template and all `VAL-SPC-*` criteria are visible.

- [ ] **Step 3: Capture audit and research inventory**

Run:

```bash
rg --files docs/90.references/audits docs/90.references/research docs/03.specs docs/04.execution | sort
```

Expected: output includes current root audit files, the current research pack,
the new Stage 03 spec, and Stage 04 indexes.

- [ ] **Step 4: Capture old audit link candidates**

Run:

```bash
rg -n "docs/90.references/audits/(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md|audits/(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md|\\./(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: output is recorded in the task evidence as the pre-move link
candidate set.

- [ ] **Step 5: Create task record from template**

Add `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`
with:

- frontmatter `title`, `type: sdlc/task`, `status: draft`, `owner:
  platform`, `updated: 2026-07-05`
- `Overview`
- `Inputs`
- `Working Rules`
- `Task Table`
- `Phase View`
- `Baseline Evidence Summary`
- `Verification Summary`
- `Related Documents`

Task IDs are `WEA-001` through `WEA-007`, matching this plan.

- [ ] **Step 6: Update task README index**

Add a row to `docs/04.execution/tasks/README.md`:

```markdown
| [`./2026-07-05-workspace-engineering-implementation-audit-pack.md`](./2026-07-05-workspace-engineering-implementation-audit-pack.md) | Workspace engineering implementation audit pack evidence for dated Stage 90 audit folderization, part-based implementation reports, automation opportunities, and validation closure. | Draft | 2026-07-05 |
```

- [ ] **Step 7: Validate WEA-001**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

- [ ] **Step 8: Commit WEA-001**

Run:

```bash
git add docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md docs/04.execution/tasks/README.md
git commit -m "docs(task): Track workspace engineering audit pack"
```

Expected: commit succeeds and the worktree is clean.

### Task 2: Folderize Existing Audit Reports

**Files:**

- Move: `docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis.md`
- Move: `docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md`
- Move: `docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: files found by the old-path candidate scan
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`

- [ ] **Step 1: Create target folders**

Run:

```bash
mkdir -p docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis
mkdir -p docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack
mkdir -p docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit
mkdir -p docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit
```

Expected: target folders exist and contain no files before moves.

- [ ] **Step 2: Move existing audit files with `git mv`**

Run:

```bash
git mv docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis.md docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis/workspace-harness-gap-analysis.md
git mv docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/workspace-governance-implementation-audit.md
git mv docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/harness-loop-implementation-audit.md
git mv docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/provider-harness-loop-implementation-audit.md
git mv docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/sdlc-delivery-practices-implementation-audit.md
git mv docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit/workspace-document-governance-hardening-audit.md
git mv docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit.md docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit/workspace-document-contract-normalization-audit.md
```

Expected: `git status --short` shows renames or delete/add pairs only for the
audit moves before link edits.

- [ ] **Step 3: Update audit README structure and index**

Edit `docs/90.references/audits/README.md` so:

- the `Structure` block lists dated folders, not root-level loose audit files
- `Audit Report Index` links to moved files under folders
- the new 2026-07-05 audit pack is listed as planned/current according to the
  files created later in this plan
- `Link Basis` states same-folder reports use folder-relative links

- [ ] **Step 4: Update current links to moved audit files**

Run the old-path scan from Task 1 Step 4. For each current navigational link,
replace the old path with the new folderized path. Leave old paths only when
they appear inside historical command strings or prior execution evidence.

Expected replacement map:

```text
docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis.md
-> docs/90.references/audits/2026-05-24-workspace-harness-gap-analysis/workspace-harness-gap-analysis.md

docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md
-> docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/workspace-governance-implementation-audit.md

docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md
-> docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/harness-loop-implementation-audit.md

docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md
-> docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/provider-harness-loop-implementation-audit.md

docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md
-> docs/90.references/audits/2026-07-02-workspace-harness-implementation-audit-pack/sdlc-delivery-practices-implementation-audit.md

docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md
-> docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit/workspace-document-governance-hardening-audit.md

docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit.md
-> docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit/workspace-document-contract-normalization-audit.md
```

- [ ] **Step 5: Record WEA-002 evidence**

Update the task record with:

- move list
- files whose links were updated
- remaining old-path matches classified as historical command/path evidence
- validation command results

- [ ] **Step 6: Validate WEA-002**

Run:

```bash
rg -n "docs/90.references/audits/(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md|audits/(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md|\\./(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: remaining old-path matches are only historical evidence; diff check
and quality gate pass.

- [ ] **Step 7: Commit WEA-002**

Run:

```bash
git add docs/90.references/audits docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md
git commit -m "docs(audits): Folderize dated audit reports"
```

Expected: commit succeeds. If the broad `git add` stages unrelated files, unstage
them before committing.

### Task 3: Governance, Harness, Loop, and Provider Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/README.md`
- Create: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/01-governance-harness-loop-providers.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`

- [ ] **Step 1: Read benchmark and evidence sources**

Run:

```bash
sed -n '1,220p' docs/90.references/research/2026-07-04-workspace-engineering-research-pack/workspace-governance-baseline.md
sed -n '1,260p' docs/90.references/research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md
sed -n '1,260p' docs/90.references/research/2026-07-04-workspace-engineering-research-pack/provider-implementation-status.md
sed -n '1,220p' docs/00.agent-governance/harness-catalog.md
sed -n '1,220p' docs/00.agent-governance/harness-implementation-map.md
```

Expected: benchmark definitions and repo implementation surfaces are visible.

- [ ] **Step 2: Create audit pack README**

Create `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/README.md`
with sections:

- `Overview`
- `Audience`
- `Scope`
- `Structure`
- `How to Work in This Area`
- `Link Basis`
- `Report Index`
- `Benchmark Sources`
- `Status Vocabulary`
- `Evidence Rules`
- `Review and Freshness`
- `Related Documents`

The `Report Index` lists all four part reports. Existing missing report paths
remain code literals until each report exists.

- [ ] **Step 3: Create governance/harness/provider report**

Create `01-governance-harness-loop-providers.md` with frontmatter:

```yaml
---
title: 'Reference: Governance Harness Loop Provider Implementation Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-05
---
```

Required sections:

- `Overview`
- `Purpose`
- `Reference Type`
- `Authority Boundary`
- `Scope`
- `Definitions / Facts`
- `Sources`
- `Review and Freshness`
- `Related Documents`

Under `Definitions / Facts`, include:

- `Benchmark Model`
- `Implementation Matrix`
- `Comparison Analysis`
- `Automation Opportunities`
- `Implementation Checklist`
- `Residual Risks`

The implementation matrix includes rows for:

- workspace purpose and operating model
- rules and governance system
- template and script routing
- harness instruction/settings surfaces
- harness architecture constraints
- harness feedback loops
- harness knowledge stores
- observe/plan/act/verify/learn loop
- eval/review loop
- Claude instruction/settings, agents, hooks/permissions, skills/MCP/tooling,
  feedback loops
- Codex instruction/settings, agents, hooks/permissions, skills/MCP/tooling,
  feedback loops
- Gemini instruction/settings, agents, hooks/permissions, skills/MCP/tooling,
  feedback loops
- common provider environment/rule/system parity
- known non-parity boundaries

- [ ] **Step 4: Update indexes**

Update:

- `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/README.md`
  so `01-governance-harness-loop-providers.md` is a link with `Current`
  status.
- `docs/90.references/audits/README.md` so the 2026-07-05 audit pack is
  discoverable.

- [ ] **Step 5: Record WEA-003 evidence**

Update task record with:

- source files read
- matrix row list
- status vocabulary confirmation
- validation command results

- [ ] **Step 6: Validate WEA-003**

Run:

```bash
rg -n "workspace purpose|harness|loop|Claude|Codex|Gemini|common provider|Implemented|Partial|Gap|Not in scope|repo-static|live-runtime|Evidence|Follow-up route|Review and Freshness" docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/01-governance-harness-loop-providers.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: required topics and headings are present; diff check and quality gate
pass.

- [ ] **Step 7: Commit WEA-003**

Run:

```bash
git add docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit docs/90.references/audits/README.md docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md
git commit -m "docs(audits): Add governance harness provider audit"
```

Expected: commit succeeds.

### Task 4: SDLC, CI/CD, QA, Formatting, and Automation Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/02-sdlc-ci-qa-formatting-automation.md`
- Modify: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/README.md`
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`

- [ ] **Step 1: Read benchmark and repo evidence**

Run:

```bash
sed -n '1,260p' docs/90.references/research/2026-07-04-workspace-engineering-research-pack/spec-sdlc-ci-qa-formatting.md
sed -n '1,260p' docs/90.references/research/2026-07-04-workspace-engineering-research-pack/automation-pipeline-workflow-qa.md
sed -n '1,220p' .github/ABOUT.md
sed -n '1,260p' .github/workflows/ci.yml
sed -n '1,260p' .pre-commit-config.yaml
sed -n '1,220p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
```

Expected: SDLC, CI, QA, formatting, automation, and workflow evidence is
visible.

- [ ] **Step 2: Create report**

Create `02-sdlc-ci-qa-formatting-automation.md` with the same required
frontmatter and reference sections as Task 3.

The implementation matrix includes rows for:

- spec-driven development lifecycle
- Stage 03 spec lifecycle
- Stage 04 plan lifecycle
- Stage 04 task/evidence lifecycle
- SDLC and secure SDLC evidence lanes
- CI/CD workflow graph
- branch policy and path filtering
- QA validation commands
- formatting and `.editorconfig`
- markdownlint/CommonMark
- YAML syntax and manifest checks
- linting with pre-commit, shellcheck, shfmt, actionlint, zizmor, hadolint,
  kube-linter
- secret scanning with gitleaks, detect-secrets, and static secret handling
- release-evidence artifact workflow
- maintenance automation: Dependabot, labeler, greetings, stale
- automation, pipeline, workflow, artifact/cache/reusable-workflow gaps
- DORA/Fowler context as non-authoritative market/context scan

- [ ] **Step 3: Update pack README and task evidence**

Update the pack README so `02-sdlc-ci-qa-formatting-automation.md` is current.
Update the task record with WEA-004 evidence.

- [ ] **Step 4: Validate WEA-004**

Run:

```bash
rg -n "spec-driven|SDLC|CI/CD|QA|Formatting|Linting|pre-commit|markdownlint|YAML|actionlint|zizmor|artifact|Dependabot|pipeline|workflow|automation|DORA|Implemented|Partial|Gap|Not in scope|repo-static|CI/toolchain|live-runtime|Review and Freshness" docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/02-sdlc-ci-qa-formatting-automation.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: required topics and evidence-lane wording are present; diff check and
quality gate pass.

- [ ] **Step 5: Commit WEA-004**

Run:

```bash
git add docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md
git commit -m "docs(audits): Add SDLC CI QA automation audit"
```

Expected: commit succeeds.

### Task 5: Kubernetes, Infrastructure, and Security Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/03-kubernetes-infrastructure-security.md`
- Modify: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/README.md`
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`

- [ ] **Step 1: Read benchmark and repo evidence**

Run:

```bash
sed -n '1,300p' docs/90.references/research/2026-07-04-workspace-engineering-research-pack/kubernetes-infrastructure-security.md
sed -n '1,220p' gitops/README.md
sed -n '1,220p' infrastructure/README.md
sed -n '1,220p' scripts/README.md
sed -n '1,220p' policy/conftest/kubernetes.rego
sed -n '1,220p' infrastructure/tests/verify-contracts-static.sh
```

Expected: Kubernetes, infrastructure, GitOps, secrets, policy, and static
contract evidence is visible.

- [ ] **Step 2: Create report**

Create `03-kubernetes-infrastructure-security.md` with the same required
frontmatter and reference sections as Task 3.

The implementation matrix includes rows for:

- Kubernetes desired-state surfaces
- GitOps repository layout
- Argo CD App-of-Apps/root app boundaries
- AppProject allow-list boundaries
- namespace ownership
- Kustomize/declarative management
- External Secrets Operator and Vault boundaries
- secret handling and no plaintext secret values
- RBAC and service account evidence
- NetworkPolicy coverage and gaps
- ingress/Traefik/static routing evidence
- policy-as-code with Conftest/OPA
- manifest validation and kube-linter path
- infrastructure static contract tests
- supply-chain and image policy boundaries
- live-runtime readiness boundary
- security automation opportunities

- [ ] **Step 3: Update pack README and task evidence**

Update the pack README so `03-kubernetes-infrastructure-security.md` is
current. Update the task record with WEA-005 evidence.

- [ ] **Step 4: Validate WEA-005**

Run:

```bash
rg -n "Kubernetes|Infrastructure|GitOps|Argo CD|AppProject|Kustomize|External Secrets|Vault|secret|RBAC|NetworkPolicy|Traefik|OPA|Conftest|kube-linter|supply-chain|security|Implemented|Partial|Gap|Not in scope|repo-static|live-runtime|Review and Freshness" docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/03-kubernetes-infrastructure-security.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: required Kubernetes/infrastructure/security topics are present; diff
check and quality gate pass.

- [ ] **Step 5: Commit WEA-005**

Run:

```bash
git add docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md
git commit -m "docs(audits): Add Kubernetes infrastructure security audit"
```

Expected: commit succeeds.

### Task 6: Roadmap and Automation Opportunities Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/04-implementation-roadmap-and-automation-opportunities.md`
- Modify: `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/README.md`
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`

- [ ] **Step 1: Read previous part reports**

Run:

```bash
sed -n '1,260p' docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/01-governance-harness-loop-providers.md
sed -n '1,260p' docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/02-sdlc-ci-qa-formatting-automation.md
sed -n '1,260p' docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/03-kubernetes-infrastructure-security.md
```

Expected: all previous report findings and opportunities are visible.

- [ ] **Step 2: Create roadmap report**

Create `04-implementation-roadmap-and-automation-opportunities.md` with the
same required frontmatter and reference sections as Task 3.

Under `Definitions / Facts`, include:

- `Cross-report Status Summary`
- `Priority Matrix`
- `Automation Opportunity Matrix`
- `Protected Surface Constraints`
- `Owner Routing`
- `Implementation Checklist`
- `Residual Risks`

The automation opportunity matrix includes rows for:

- audit matrix validator
- README/index stale-link checker for audit folderization
- provider parity evidence checker
- workflow/QA evidence summarizer
- GitOps manifest and policy evidence aggregator
- secret-handling evidence summarizer
- DORA/CI metrics proposal route
- live-runtime readiness evidence route

Each row has owner route, required approval boundary, evidence lane, and
whether it is safe for future repo-static automation.

- [ ] **Step 3: Update pack README and task evidence**

Update the pack README so all four reports are current. Update task evidence
with WEA-006 findings.

- [ ] **Step 4: Validate WEA-006**

Run:

```bash
rg -n "Priority Matrix|Automation Opportunity|Protected Surface|Owner Routing|audit matrix|provider parity|workflow|GitOps|secret-handling|DORA|live-runtime|repo-static|Implemented|Partial|Gap|Not in scope|Review and Freshness" docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/04-implementation-roadmap-and-automation-opportunities.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: roadmap, automation opportunities, owner routes, and protected
surface constraints are present; diff check and quality gate pass.

- [ ] **Step 5: Commit WEA-006**

Run:

```bash
git add docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md
git commit -m "docs(audits): Add implementation roadmap audit"
```

Expected: commit succeeds.

### Task 7: Final Index, Review, Validation, and Handoff

**Files:**

- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Review: all new and moved audit files

- [ ] **Step 1: Run final structure scan**

Run:

```bash
rg --files docs/90.references/audits | sort
```

Expected: root audit folder contains `README.md` plus dated folders; no
root-level audit report Markdown files remain except `README.md`.

- [ ] **Step 2: Run old-path stale scan**

Run:

```bash
rg -n "docs/90.references/audits/(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md|audits/(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md|\\./(2026-05-24-workspace-harness-gap-analysis|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-workspace-document-governance-hardening-audit|2026-07-04-workspace-document-contract-normalization-audit)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: no current navigational links point to removed root-level audit
files. Remaining matches, if any, are recorded as historical command/path
evidence.

- [ ] **Step 3: Run report coverage scan**

Run:

```bash
rg -n "Overview|Purpose|Reference Type|Authority Boundary|Scope|Definitions / Facts|Sources|Review and Freshness|Related Documents|Implemented|Partial|Gap|Not in scope|Evidence|Follow-up route|repo-static|live-runtime" docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit
```

Expected: all four part reports show required sections, status vocabulary,
evidence language, and static-vs-live boundary language.

- [ ] **Step 4: Dispatch final review subagent when available**

If subagents are available, dispatch a read-only reviewer with this scope:

- all files under
  `docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit/`
- `docs/90.references/audits/README.md`
- `docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`

Ask the reviewer to check for:

- unsupported `Implemented` or `Partial` claims
- broken local links
- Stage 90 material becoming active policy
- repo-static evidence overclaiming live readiness
- stale old audit paths
- missing requested topics

Fix any findings in a separate logical commit.

- [ ] **Step 5: Update progress memory**

Add a new top entry to `docs/00.agent-governance/memory/progress.md` with:

- date `2026-07-05`
- layer `docs, references, audits, governance, platform, qa`
- status `complete`
- progress summary for folderization and the four audit reports
- memory notes about audit status vocabulary and evidence lanes
- validation evidence
- no-live/no-external-mutation handoff statement

- [ ] **Step 6: Final validation**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git status --short --branch
```

Expected: diff check and quality gate pass; worktree has only intended staged
or committed changes.

- [ ] **Step 7: Commit final closure**

Run:

```bash
git add docs/90.references/audits docs/04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(audits): Close workspace engineering audit pack"
```

Expected: commit succeeds and the worktree is clean.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Confirm audit folderization | `rg --files docs/90.references/audits | sort` | Root audit folder has only `README.md` plus dated folders. |
| VAL-PLN-002 | Link hygiene | Detect old root audit links | Old-path `rg` scan from Task 7 Step 2 | No current navigational links point to removed root-level audit reports. |
| VAL-PLN-003 | Coverage | Confirm requested topics in audit reports | Topic scans listed in Tasks 3-6 | Required topic terms and matrices are present. |
| VAL-PLN-004 | Evidence boundary | Confirm status vocabulary and evidence lanes | `rg -n "Implemented|Partial|Gap|Not in scope|repo-static|live-runtime" docs/90.references/audits/2026-07-05-workspace-engineering-implementation-audit` | Approved status vocabulary and static-vs-live boundary language are present. |
| VAL-PLN-005 | Formatting | Check whitespace and diff hygiene | `git diff --check` | No whitespace errors. |
| VAL-PLN-006 | Repo quality | Run repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-PLN-007 | Boundary | Confirm no live or external mutation | Task evidence and command history review | Only repository reads, documentation edits, local validation, local commits, and optional read-only subagent review occurred. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Existing audit folderization breaks links | Current docs may point to removed paths | Run old-path scans after moves and update current navigational links before committing. |
| Audit rows overclaim implementation | Reports may imply capability exists without repo evidence | Require repo-backed evidence links for `Implemented` and `Partial`; downgrade to `Gap` or `Not in scope` when evidence is absent. |
| Stage 90 audit recommendations become active policy | Governance ownership becomes unclear | Keep recommendations in follow-up routes and roadmap; do not edit active policy, workflows, scripts, or manifests in this plan. |
| Static validation is mistaken for live readiness | Operators may trust unverified runtime state | Repeat static-vs-live boundary language in every report and task handoff. |
| Report count or matrix scope grows too large | Completion slows and review quality drops | Keep four reports with focused matrices and route future details to owner-scoped tasks. |
| Subagent edits conflict with local work | Merge noise and duplicated edits | Use one implementer task at a time, or read-only reviewers; provide disjoint write scopes if delegation is used. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: `git diff --check`, focused `rg` scans, and
  `bash scripts/validate-repo-quality-gates.sh .`.
- **Sandbox / Canary Rollout**: Not applicable. This is documentation-only.
- **Human Approval Gate**: Required before any live runtime validation,
  workflow behavior change, script semantic change, provider adapter change,
  GitOps manifest change, policy change, credential action, remote GitHub
  action, push, merge, publish, or PR creation.
- **Rollback Trigger**: Broken current links, failed repo-quality gate,
  unsupported `Implemented` claim, or accidental active-policy change.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [ ] Task record created and updated for WEA-001 through WEA-007.
- [ ] Existing root audit files moved into dated folders.
- [ ] New 2026-07-05 audit pack contains README plus four part reports.
- [ ] Audit README indexes folderized legacy audits and the new audit pack.
- [ ] Old root audit path scan has no unresolved current-link matches.
- [ ] Each part report uses required reference sections and approved audit
  status vocabulary.
- [ ] Task evidence records validation commands and no-mutation boundary.
- [ ] `git diff --check` passes.
- [ ] `bash scripts/validate-repo-quality-gates.sh .` passes.
- [ ] Logical commits are created for each major task group.

## Related Documents

- **Spec**: [../../03.specs/018-workspace-engineering-implementation-audit-pack/spec.md](../../03.specs/018-workspace-engineering-implementation-audit-pack/spec.md)
- **Research Pack Spec**: [../../03.specs/017-workspace-engineering-research-pack/spec.md](../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Prior Audit Pack Spec**: [../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md](../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- **Tasks**: `../tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md`
- **Research Pack README**: [../../90.references/research/2026-07-04-workspace-engineering-research-pack/README.md](../../90.references/research/2026-07-04-workspace-engineering-research-pack/README.md)
- **Audits README**: [../../90.references/audits/README.md](../../90.references/audits/README.md)
- **Reference Template**: [../../99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md)
- **Task Template**: [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
