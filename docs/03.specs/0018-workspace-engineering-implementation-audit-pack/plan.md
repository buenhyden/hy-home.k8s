---
title: 'Workspace Engineering Implementation Audit Pack Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
artifact_id: "PLAN-0018"
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
`docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md`.
The implementation creates
`docs/90.references/audits/2026-07-05-wea/`,
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
docs/90.references/research/2026-07-04-wer/
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
`-- 2026-07-05-wea/
    |-- README.md
    |-- governance-harness-loop-providers.md
    |-- sdlc-ci-qa-formatting-automation.md
    |-- kubernetes-infrastructure-security.md
    `-- implementation-roadmap-and-automation-opportunities.md
```

Existing root-level audits are normalized into dated folders:

```text
docs/90.references/audits/
|-- 2026-05-24-whga/
|   `-- workspace-harness-gap-analysis.md
|-- 2026-07-02-whia/
|   |-- workspace-governance-implementation-audit.md
|   |-- harness-loop-implementation-audit.md
|   |-- provider-harness-loop-implementation-audit.md
|   `-- sdlc-delivery-practices-implementation-audit.md
|-- 2026-07-03-wdgh/
|   `-- workspace-document-governance-hardening-audit.md
`-- 2026-07-04-wdcn/
    `-- workspace-document-contract-normalization-audit.md
```

### Legacy Task ledger inputs

This document tracks execution evidence for the workspace engineering
implementation audit pack. The work creates a dated Stage 90 audit pack,
folderizes existing audit snapshots, compares the current research benchmark
against repo-backed implementation evidence, records automation opportunities,
and closes validation through local static checks.

- **Parent Spec**: [../../03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md](spec.md)
- **Parent Plan**: [../plans/2026-07-05-workspace-engineering-implementation-audit-pack.md](plan.md)
- **Task Template**: [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)
- **Research Pack**: `docs/90.references/research/2026-07-04-wer/README.md`; [current lookup](../../90.references/research/0001-workspace-engineering/README.md)
- **Stage 90 Router**: [../../90.references/README.md](../../90.references/README.md)
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
  - `docs/03.specs/**`
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md`
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

### File Structure

| Path | Responsibility |
| --- | --- |
| `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records` | Execution evidence, task table, validation commands, limitations, and handoff. |
| `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records` | Task index entry for this audit-pack implementation. |
| `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md` | This implementation plan. |
| `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md` | Plan index entry for this plan. |
| `docs/90.references/audits/README.md` | Audits folder entrypoint, normalized folder index, status vocabulary, evidence rules, and related docs. |
| `docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md` | Folderized historical 2026-05-24 harness gap snapshot. |
| `docs/90.references/audits/2026-07-02-whia/*.md` | Folderized 2026-07-02 four-report implementation audit pack. |
| `docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md` | Folderized 2026-07-03 document governance hardening audit snapshot. |
| `docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md` | Folderized 2026-07-04 document contract normalization audit snapshot. |
| `docs/90.references/audits/2026-07-05-wea/README.md` | New dated audit pack entrypoint and report index. |
| `docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md` | Governance, harness, loop, Claude, Codex, Gemini, and common provider implementation audit. |
| `docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md` | Spec-driven development, SDLC, CI/CD, QA, formatting, linting, automation, pipeline, and workflow audit. |
| `docs/90.references/audits/2026-07-05-wea/kubernetes-infrastructure-security.md` | Kubernetes, infrastructure, GitOps, secrets, policy, network, supply-chain, and security audit. |
| `docs/90.references/audits/2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md` | Cross-report roadmap, priority matrix, automation candidates, and future task routing. |
| `docs/00.agent-governance/memory/progress.md` | Durable progress and reusable memory entry after audit completion. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| WEA-001 | Create task evidence and baseline inventory | Task record, tasks README, progress memory | VAL-SPC-007 | Baseline inventory recorded; repo-quality gate passes |
| WEA-002 | Folderize existing root audit reports | Audits folders, moved reports, audit README, current links | VAL-SPC-001, VAL-SPC-006 | `git mv` preserves history; stale old-path scan has no current broken links |
| WEA-003 | Add dated audit pack README and governance/harness/provider report | Audit pack README, `governance-harness-loop-providers.md` | VAL-SPC-002, VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Required topics and evidence matrix rows present |
| WEA-004 | Add SDLC/CI/QA/formatting/automation report | `sdlc-ci-qa-formatting-automation.md` | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | SDLC, CI/CD, QA, formatting, linting, automation, pipeline, workflow rows present |
| WEA-005 | Add Kubernetes/infrastructure/security report | `kubernetes-infrastructure-security.md` | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Kubernetes, infrastructure, GitOps, secrets, policy, security rows present |
| WEA-006 | Add roadmap and automation opportunities report | `implementation-roadmap-and-automation-opportunities.md` | VAL-SPC-004, VAL-SPC-005 | Cross-report roadmap and automation opportunities are owner-routed |
| WEA-007 | Close indexes, evidence, review, and validation | Audits README, task evidence, progress memory | VAL-SPC-006, VAL-SPC-007, VAL-SPC-008 | Final scans and quality gates pass; no mutation boundary violation |

### Detailed Tasks

> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.

### Task 1: Task Evidence and Baseline Inventory

**Files:**

- Create: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`
- Modify: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/specs/task.template.md`
- Read: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md`
- Read: `docs/90.references/research/2026-07-04-wer/README.md`
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
sed -n '1,220p' docs/99.templates/templates/specs/task.template.md
sed -n '1,420p' docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md
```

Expected: task template and all `VAL-SPC-*` criteria are visible.

- [ ] **Step 3: Capture audit and research inventory**

Run:

```bash
rg --files docs/90.references/audits docs/90.references/research docs/03.specs docs/03.specs | sort
```

Expected: output includes current root audit files, the current research pack,
the new Stage 03 spec, and Stage 04 indexes.

- [ ] **Step 4: Capture old audit link candidates**

Run:

```bash
rg -n "docs/90.references/audits/(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md|audits/(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md|\\./(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: output is recorded in the task evidence as the pre-move link
candidate set.

- [ ] **Step 5: Create task record from template**

Add `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`
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

Add a row to `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`:

```markdown
| [`./2026-07-05-workspace-engineering-implementation-audit-pack.md`](plan.md) | Workspace engineering implementation audit pack evidence for dated Stage 90 audit folderization, part-based implementation reports, automation opportunities, and validation closure. | Draft | 2026-07-05 |
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
git add docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records
git commit -m "docs(task): Track workspace engineering audit pack"
```

Expected: commit succeeds and the worktree is clean.

### Task 2: Folderize Existing Audit Reports

**Files:**

- Move: `docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md`
- Move: `docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md`
- Move: `docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md`
- Move: `docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: files found by the old-path candidate scan
- Modify: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`

- [ ] **Step 1: Create target folders**

Run:

```bash
mkdir -p docs/90.references/audits/2026-05-24-whga
mkdir -p docs/90.references/audits/2026-07-02-whia
mkdir -p docs/90.references/audits/2026-07-03-wdgh
mkdir -p docs/90.references/audits/2026-07-04-wdcn
```

Expected: target folders exist and contain no files before moves.

- [ ] **Step 2: Move existing audit files with `git mv`**

Run:

```bash
git mv docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md
git mv docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md docs/90.references/audits/2026-07-02-whia/workspace-governance-implementation-audit.md
git mv docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md docs/90.references/audits/2026-07-02-whia/harness-loop-implementation-audit.md
git mv docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md docs/90.references/audits/2026-07-02-whia/provider-harness-loop-implementation-audit.md
git mv docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md docs/90.references/audits/2026-07-02-whia/sdlc-delivery-practices-implementation-audit.md
git mv docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md
git mv docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md
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
docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md
-> docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md

docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md
-> docs/90.references/audits/2026-07-02-whia/workspace-governance-implementation-audit.md

docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md
-> docs/90.references/audits/2026-07-02-whia/harness-loop-implementation-audit.md

docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md
-> docs/90.references/audits/2026-07-02-whia/provider-harness-loop-implementation-audit.md

docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md
-> docs/90.references/audits/2026-07-02-whia/sdlc-delivery-practices-implementation-audit.md

docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md
-> docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md

docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md
-> docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md
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
rg -n "docs/90.references/audits/(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md|audits/(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md|\\./(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: remaining old-path matches are only historical evidence; diff check
and quality gate pass.

- [ ] **Step 7: Commit WEA-002**

Run:

```bash
git add docs/90.references/audits docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records
git commit -m "docs(audits): Folderize dated audit reports"
```

Expected: commit succeeds. If the broad `git add` stages unrelated files, unstage
them before committing.

### Task 3: Governance, Harness, Loop, and Provider Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-wea/README.md`
- Create: `docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`

- [ ] **Step 1: Read benchmark and evidence sources**

Run:

```bash
sed -n '1,220p' docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md
sed -n '1,260p' docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md
sed -n '1,260p' docs/90.references/research/2026-07-04-wer/provider-implementation-status.md
sed -n '1,220p' docs/00.agent-governance/harness-catalog.md
```

Expected: benchmark definitions and repo implementation surfaces are visible.

- [ ] **Step 2: Create audit pack README**

Create `docs/90.references/audits/2026-07-05-wea/README.md`
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

Create `governance-harness-loop-providers.md` with frontmatter:

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

- `docs/90.references/audits/2026-07-05-wea/README.md`
  so `governance-harness-loop-providers.md` is a link with `Current`
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
rg -n "workspace purpose|harness|loop|Claude|Codex|Gemini|common provider|Implemented|Partial|Gap|Not in scope|repo-static|live-runtime|Evidence|Follow-up route|Review and Freshness" docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: required topics and headings are present; diff check and quality gate
pass.

- [ ] **Step 7: Commit WEA-003**

Run:

```bash
git add docs/90.references/audits/2026-07-05-wea docs/90.references/audits/README.md docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records
git commit -m "docs(audits): Add governance harness provider audit"
```

Expected: commit succeeds.

### Task 4: SDLC, CI/CD, QA, Formatting, and Automation Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md`
- Modify: `docs/90.references/audits/2026-07-05-wea/README.md`
- Modify: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`

- [ ] **Step 1: Read benchmark and repo evidence**

Run:

```bash
sed -n '1,260p' docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md
sed -n '1,260p' docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md
sed -n '1,220p' .github/README.md
sed -n '1,260p' .github/workflows/ci.yml
sed -n '1,260p' .pre-commit-config.yaml
sed -n '1,220p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
```

Expected: SDLC, CI, QA, formatting, automation, and workflow evidence is
visible.

- [ ] **Step 2: Create report**

Create `sdlc-ci-qa-formatting-automation.md` with the same required
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

Update the pack README so `sdlc-ci-qa-formatting-automation.md` is current.
Update the task record with WEA-004 evidence.

- [ ] **Step 4: Validate WEA-004**

Run:

```bash
rg -n "spec-driven|SDLC|CI/CD|QA|Formatting|Linting|pre-commit|markdownlint|YAML|actionlint|zizmor|artifact|Dependabot|pipeline|workflow|automation|DORA|Implemented|Partial|Gap|Not in scope|repo-static|CI/toolchain|live-runtime|Review and Freshness" docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: required topics and evidence-lane wording are present; diff check and
quality gate pass.

- [ ] **Step 5: Commit WEA-004**

Run:

```bash
git add docs/90.references/audits/2026-07-05-wea docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records
git commit -m "docs(audits): Add SDLC CI QA automation audit"
```

Expected: commit succeeds.

### Task 5: Kubernetes, Infrastructure, and Security Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-wea/kubernetes-infrastructure-security.md`
- Modify: `docs/90.references/audits/2026-07-05-wea/README.md`
- Modify: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`

- [ ] **Step 1: Read benchmark and repo evidence**

Run:

```bash
sed -n '1,300p' docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md
sed -n '1,220p' gitops/README.md
sed -n '1,220p' infrastructure/README.md
sed -n '1,220p' scripts/README.md
sed -n '1,220p' policy/conftest/kubernetes.rego
sed -n '1,220p' infrastructure/tests/verify-contracts-static.sh
```

Expected: Kubernetes, infrastructure, GitOps, secrets, policy, and static
contract evidence is visible.

- [ ] **Step 2: Create report**

Create `kubernetes-infrastructure-security.md` with the same required
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

Update the pack README so `kubernetes-infrastructure-security.md` is
current. Update the task record with WEA-005 evidence.

- [ ] **Step 4: Validate WEA-005**

Run:

```bash
rg -n "Kubernetes|Infrastructure|GitOps|Argo CD|AppProject|Kustomize|External Secrets|Vault|secret|RBAC|NetworkPolicy|Traefik|OPA|Conftest|kube-linter|supply-chain|security|Implemented|Partial|Gap|Not in scope|repo-static|live-runtime|Review and Freshness" docs/90.references/audits/2026-07-05-wea/kubernetes-infrastructure-security.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: required Kubernetes/infrastructure/security topics are present; diff
check and quality gate pass.

- [ ] **Step 5: Commit WEA-005**

Run:

```bash
git add docs/90.references/audits/2026-07-05-wea docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records
git commit -m "docs(audits): Add Kubernetes infrastructure security audit"
```

Expected: commit succeeds.

### Task 6: Roadmap and Automation Opportunities Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md`
- Modify: `docs/90.references/audits/2026-07-05-wea/README.md`
- Modify: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`

- [ ] **Step 1: Read previous part reports**

Run:

```bash
sed -n '1,260p' docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md
sed -n '1,260p' docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md
sed -n '1,260p' docs/90.references/audits/2026-07-05-wea/kubernetes-infrastructure-security.md
```

Expected: all previous report findings and opportunities are visible.

- [ ] **Step 2: Create roadmap report**

Create `implementation-roadmap-and-automation-opportunities.md` with the
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
rg -n "Priority Matrix|Automation Opportunity|Protected Surface|Owner Routing|audit matrix|provider parity|workflow|GitOps|secret-handling|DORA|live-runtime|repo-static|Implemented|Partial|Gap|Not in scope|Review and Freshness" docs/90.references/audits/2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: roadmap, automation opportunities, owner routes, and protected
surface constraints are present; diff check and quality gate pass.

- [ ] **Step 5: Commit WEA-006**

Run:

```bash
git add docs/90.references/audits/2026-07-05-wea docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records
git commit -m "docs(audits): Add implementation roadmap audit"
```

Expected: commit succeeds.

### Task 7: Final Index, Review, Validation, and Handoff

**Files:**

- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`
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
rg -n "docs/90.references/audits/(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md|audits/(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md|\\./(2026-05-24-whga|2026-07-02-harness-loop-implementation-audit|2026-07-02-provider-harness-loop-implementation-audit|2026-07-02-sdlc-delivery-practices-implementation-audit|2026-07-02-workspace-governance-implementation-audit|2026-07-03-wdgh|2026-07-04-wdcn)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: no current navigational links point to removed root-level audit
files. Remaining matches, if any, are recorded as historical command/path
evidence.

- [ ] **Step 3: Run report coverage scan**

Run:

```bash
rg -n "Overview|Purpose|Reference Type|Authority Boundary|Scope|Definitions / Facts|Sources|Review and Freshness|Related Documents|Implemented|Partial|Gap|Not in scope|Evidence|Follow-up route|repo-static|live-runtime" docs/90.references/audits/2026-07-05-wea
```

Expected: all four part reports show required sections, status vocabulary,
evidence language, and static-vs-live boundary language.

- [ ] **Step 4: Dispatch final review subagent when available**

If subagents are available, dispatch a read-only reviewer with this scope:

- all files under
  `docs/90.references/audits/2026-07-05-wea/`
- `docs/90.references/audits/README.md`
- `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`

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
git add docs/90.references/audits docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(audits): Close workspace engineering audit pack"
```

Expected: commit succeeds and the worktree is clean.

### Legacy Task supplemental evidence

### Phase View

### Phase 1: Baseline and Task Evidence

- [x] WEA-001 Create task evidence and baseline inventory

### Phase 2: Audit Folderization

- [x] WEA-002 Folderize existing root audit reports

### Phase 3: Part-Based Audit Reports

- [x] WEA-003 Add dated audit pack README and governance/harness/provider report
- [x] WEA-004 Add SDLC/CI/QA/formatting/automation report
- [x] WEA-005 Add Kubernetes/infrastructure/security report
- [x] WEA-006 Add roadmap and automation opportunities report

### Phase 4: Closure

- [x] WEA-007 Close indexes, evidence, review, and validation

### Baseline Evidence Summary

- `git status --short --branch` confirmed branch
  `codex/workspace-engineering-audit-pack` with no uncommitted changes before
  WEA-001 edits.
- The task template requires traceability-first task records with parent
  Spec/Plan links, evidence, validation commands, and relative links from the
  authored task location.
- The parent spec defines eight validation criteria. The relevant WEA-001
  criterion is VAL-SPC-007 for Stage 04 task evidence and static validation;
  the final boundary criterion is VAL-SPC-008.
- Inventory across Stage 90, Stage 03, and Stage 04 found seven current
  root-level audit files, one current research pack folder with six part files
  plus README, the Stage 03 spec, the Stage 04 plan, the Stage 04 task index,
  and prior execution records.
- The old-path candidate scan used the full plan scope:
  `docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts`. Matches
  were found across current and historical docs, including Stage 03 specs,
  Stage 04 plans/tasks, Stage 00 memory, and `docs/90.references/audits/README.md`.
  They include current navigational links that WEA-002 must update and
  historical command/path evidence that may remain if intentionally preserved.

### WEA-002 Evidence Summary

- `git status --short --branch` confirmed WEA-002 started from branch
  `codex/workspace-engineering-audit-pack` with no uncommitted changes.
- Folderized the seven existing root audit reports with `git mv`:
  - `docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md`
    to
    `docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md`
  - `docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md`
    to
    `docs/90.references/audits/2026-07-02-whia/workspace-governance-implementation-audit.md`
  - `docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md`
    to
    `docs/90.references/audits/2026-07-02-whia/harness-loop-implementation-audit.md`
  - `docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md`
    to
    `docs/90.references/audits/2026-07-02-whia/provider-harness-loop-implementation-audit.md`
  - `docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md`
    to
    `docs/90.references/audits/2026-07-02-whia/sdlc-delivery-practices-implementation-audit.md`
  - `docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md`
    to
    `docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md`
  - `docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md`
    to
    `docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md`
- Updated the Stage 90 audit index structure, links, Link Basis note, and
  planned/current `2026-07-05-wea/`
  directory entry in the [Stage 90 router](../../90.references/README.md).
- Updated current navigational links and moved-report relative links in:
  - [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
  - [../../03.specs/0006-workspace-harness-gap-analysis/spec.md](../0006-workspace-harness-gap-analysis/spec.md)
  - [../../03.specs/0009-workspace-harness-research-pack/spec.md](../0009-workspace-harness-research-pack/spec.md)
  - [../../03.specs/0010-workspace-harness-implementation-audit-pack/spec.md](../0010-workspace-harness-implementation-audit-pack/spec.md)
  - [../../03.specs/0013-workspace-document-governance-hardening/spec.md](../0013-workspace-document-governance-hardening/spec.md)
  - [Archived P3 GitOps secret runtime remediation Plan](../../98.archive/README.md#document-index)
  - [Archived P3 GitOps secret runtime remediation Task](../../98.archive/README.md#document-index)
  - [2026-07-03-workspace-document-governance-hardening.md](../0013-workspace-document-governance-hardening/README.md)
  - [2026-07-04-workspace-document-contract-normalization.md](../0014-workspace-document-contract-normalization/README.md)
  - moved reports under `docs/90.references/audits/`
- The required old-path scan still returns matches, all classified as
  historical evidence:
  - prior plan instructions and command examples in the 2026-07-02,
    2026-07-03, 2026-07-04, and 2026-07-05 Stage 04 plans
  - prior task evidence path literals in the 2026-07-03 and 2026-07-04
    Stage 04 task records
  - current WEA baseline scan evidence in this task record
  - progress-memory historical path literals that are not Markdown links
- WEA-002 validation results:
  - Required old-path scan completed; remaining matches are classified above.
  - `git diff --check` passed.
  - First `bash scripts/validate-repo-quality-gates.sh .` run exposed broken
    Markdown links caused by the folder moves; after repairing those links, the
    final repository quality gate passed.
## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Confirm audit folderization | `rg --files docs/90.references/audits | sort` | Root audit folder has only `README.md` plus dated folders. |
| VAL-PLN-002 | Link hygiene | Detect old root audit links | Old-path `rg` scan from Task 7 Step 2 | No current navigational links point to removed root-level audit reports. |
| VAL-PLN-003 | Coverage | Confirm requested topics in audit reports | Topic scans listed in Tasks 3-6 | Required topic terms and matrices are present. |
| VAL-PLN-004 | Evidence boundary | Confirm status vocabulary and evidence lanes | `rg -n "Implemented|Partial|Gap|Not in scope|repo-static|live-runtime" docs/90.references/audits/2026-07-05-wea` | Approved status vocabulary and static-vs-live boundary language are present. |
| VAL-PLN-005 | Formatting | Check whitespace and diff hygiene | `git diff --check` | No whitespace errors. |
| VAL-PLN-006 | Repo quality | Run repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-PLN-007 | Boundary | Confirm no live or external mutation | Task evidence and command history review | Only repository reads, documentation edits, local validation, local commits, and optional read-only subagent review occurred. |

### Legacy Task verification evidence

- **Baseline Commands**:
  - `git status --short --branch`
  - `sed -n '1,220p' docs/99.templates/templates/specs/task.template.md`
  - `sed -n '1,420p' docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md`
  - `rg --files docs/90.references/audits docs/90.references/research docs/03.specs docs/03.specs | sort`
  - Full old-path candidate scan over
    `docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` for these
    seven root audit paths:
    - `docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md`
    - `docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md`
    - `docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md`
    - `docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md`
    - `docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md`
    - `docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md`
    - `docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md`
- **WEA-001 Validation Commands**:
  - `git diff --check` passed.
  - `bash scripts/validate-repo-quality-gates.sh .` passed with
    `[PASS] repository quality gates passed`.
- **WEA-003 Source Files Read**:
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md` Task 3
  - `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md`
  - `docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md`
  - `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md`
  - `docs/00.agent-governance/harness-catalog.md`
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
  - `.claude/CLAUDE.md`, `.codex/CODEX.md`, `.agents/GEMINI.md`
  - `.claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json`
  - `docs/00.agent-governance/providers/claude.md`
  - `docs/00.agent-governance/providers/codex.md`
  - `docs/00.agent-governance/providers/gemini.md`
  - `.claude/agents/`, `.codex/agents/`, `.agents/agents/`,
    `.agents/skills/`, `.agents/workflows/`, and `.agents/output-styles/`
- **WEA-003 Matrix Rows Recorded**:
  - workspace purpose and operating model
  - rules and governance system
  - template and script routing
  - harness instruction/settings surfaces
  - harness architecture constraints
  - harness feedback loops
  - harness knowledge stores
  - observe/plan/act/verify/learn loop
  - eval/review loop
  - Claude instruction/settings, agents, hooks/permissions,
    skills/MCP/tooling, feedback loops
  - Codex instruction/settings, agents, hooks/permissions,
    skills/MCP/tooling, feedback loops
  - Gemini instruction/settings, agents, hooks/permissions,
    skills/MCP/tooling, feedback loops
  - common provider environment/rule/system parity
  - known non-parity boundaries
- **WEA-003 Status Vocabulary Confirmation**:
  - The audit pack uses only `Implemented`, `Partial`, `Gap`, and
    `Not in scope`.
  - Repo-backed evidence is used for implementation status; upstream provider
    capability remains benchmark context.
  - Static validation is recorded as repo-static evidence only, not
    live-runtime, provider-runtime, Kubernetes, cloud, or secret readiness.
- **WEA-003 Validation Commands**:
  - Required `rg -n "workspace purpose|harness|loop|Claude|Codex|Gemini|common provider|Implemented|Partial|Gap|Not in scope|repo-static|live-runtime|Evidence|Follow-up route|Review and Freshness" docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md` completed.
  - `git diff --check` passed.
  - `bash scripts/validate-repo-quality-gates.sh .` passed with
    `[PASS] repository quality gates passed`.
- **WEA-004 Source Files Read**:
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md` Task 4
  - `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md`
  - `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md`
  - `.github/README.md`
  - `.github/workflows/ci.yml`
  - `.github/workflows/generate-changelog.yml`
  - `.github/workflows/labeler.yml`
  - `.github/workflows/greetings.yml`
  - `.github/workflows/stale.yml`
  - `.github/dependabot.yml`
  - `.github/labeler.yml`
  - `.github/zizmor.yml`
  - `.pre-commit-config.yaml`
  - `.editorconfig`
  - `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`
  - `scripts/README.md`
- **WEA-004 Matrix Rows Recorded**:
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
  - linting with pre-commit, shellcheck, shfmt, actionlint, zizmor,
    hadolint, kube-linter
  - secret scanning with gitleaks, detect-secrets, and static secret handling
  - release-evidence artifact workflow
  - maintenance automation: Dependabot, labeler, greetings, stale
  - automation, pipeline, workflow, artifact/cache/reusable-workflow gaps
  - DORA/Fowler context as non-authoritative market/context scan
- **WEA-004 Status Vocabulary Confirmation**:
  - The audit pack uses only `Implemented`, `Partial`, `Gap`, and
    `Not in scope`.
  - Repo-backed evidence is used for implementation status; research,
    DORA/Fowler, and external market/context material remain benchmark
    context.
  - Repo-static, CI/toolchain, artifact/release, maintenance,
    market/context, and live-runtime evidence lanes are kept separate.
  - Static validation is recorded as repo-static evidence only, not
    live-runtime, provider-runtime, Kubernetes, cloud, or secret readiness.
- **WEA-004 Validation Commands**:
  - Required `rg -n "spec-driven|SDLC|CI/CD|QA|Formatting|Linting|pre-commit|markdownlint|YAML|actionlint|zizmor|artifact|Dependabot|pipeline|workflow|automation|DORA|Implemented|Partial|Gap|Not in scope|repo-static|CI/toolchain|live-runtime|Review and Freshness" docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md` completed.
  - `git diff --check` passed.
  - `bash scripts/validate-repo-quality-gates.sh .` passed with
    `[PASS] repository quality gates passed`.
- **WEA-005 Source Files Read**:
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md` Task 5
  - `docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md`
  - `gitops/README.md`
  - `infrastructure/README.md`
  - `scripts/README.md`
  - `tests/README.md`
  - `traefik/README.md`
  - `docs/05.operations/policies/0001-k8s-gitops-operations-policy.md`
  - `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md`
  - `policy/conftest/kubernetes.rego`
  - `scripts/validate-policy-gates.sh`
  - `scripts/validate-gitops-structure.sh`
  - `scripts/validate-k8s-manifests.sh`
  - `scripts/check-secret-handling.sh`
  - `infrastructure/tests/verify-contracts-static.sh`
  - representative GitOps and infrastructure evidence under
    `gitops/clusters/local/`, `gitops/apps/root/`, `gitops/platform/eso/`,
    `gitops/platform/network-policies/`, and `infrastructure/vault/`
- **WEA-005 Matrix Rows Recorded**:
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
- **WEA-005 Status Vocabulary Confirmation**:
  - The audit pack uses only `Implemented`, `Partial`, `Gap`, and
    `Not in scope`.
  - Repo-backed evidence is used for implementation status; official
    Kubernetes, Argo, Vault, OPA, NIST, OpenSSF, and related sources remain
    benchmark context through the research pack.
  - Policy-as-code evidence is repo-static/CI-toolchain evidence only, not
    live admission control.
  - Static validation is recorded as repo-static evidence only, not
    live-runtime, Kubernetes, Argo CD, Vault, ESO, network, cloud, or secret
    readiness.
- **WEA-005 Validation Commands**:
  - Required `rg -n "Kubernetes|Infrastructure|GitOps|Argo CD|AppProject|Kustomize|External Secrets|Vault|secret|RBAC|NetworkPolicy|Traefik|OPA|Conftest|kube-linter|supply-chain|security|Implemented|Partial|Gap|Not in scope|repo-static|live-runtime|Review and Freshness" docs/90.references/audits/2026-07-05-wea/kubernetes-infrastructure-security.md` completed.
  - `git diff --check` passed.
  - `bash scripts/validate-repo-quality-gates.sh .` passed with
    `[PASS] repository quality gates passed`.
- **WEA-006 Source Files Read**:
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md` Task 6
  - `docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md`
  - `docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md`
  - `docs/90.references/audits/2026-07-05-wea/kubernetes-infrastructure-security.md`
- **WEA-006 Sections Recorded**:
  - Cross-report Status Summary
  - Priority Matrix
  - Automation Opportunity Matrix
  - Protected Surface Constraints
  - Owner Routing
  - Implementation Checklist
  - Residual Risks
- **WEA-006 Automation Opportunity Rows Recorded**:
  - audit matrix validator
  - README/index stale-link checker for audit folderization
  - provider parity evidence checker
  - workflow/QA evidence summarizer
  - GitOps manifest and policy evidence aggregator
  - secret-handling evidence summarizer
  - DORA/CI metrics proposal route
  - live-runtime readiness evidence route
- **WEA-006 Status Vocabulary Confirmation**:
  - The audit pack uses only `Implemented`, `Partial`, `Gap`, and
    `Not in scope`.
  - Each automation opportunity records owner route, required approval
    boundary, evidence lane, and whether it is safe for future repo-static
    automation.
  - Repo-static, CI/toolchain, market/context, and live-runtime evidence lanes
    are kept separate.
- **WEA-006 Validation Commands**:
  - Required `rg -n "Priority Matrix|Automation Opportunity|Protected Surface|Owner Routing|audit matrix|provider parity|workflow|GitOps|secret-handling|DORA|live-runtime|repo-static|Implemented|Partial|Gap|Not in scope|Review and Freshness" docs/90.references/audits/2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md` completed.
  - `git diff --check` passed.
  - `bash scripts/validate-repo-quality-gates.sh .` passed with
    `[PASS] repository quality gates passed`.
- **WEA-007 Index Closure**:
  - Updated the parent audit index so the 2026-07-05 audit pack lists all
    four reports as current Markdown links.
  - Updated the Stage 04 plan/task frontmatter and indexes from Draft to Done
    for this completed implementation audit pack.
  - Confirmed `rg --files docs/90.references/audits | sort` shows only
    `README.md` at the audit root plus dated audit folders and their reports.
  - Confirmed the old root-audit-path scan has no unresolved current
    navigational links; remaining matches are historical command/path evidence
    in prior plans, prior tasks, and progress-memory history.
- **WEA-007 Coverage Review**:
  - Confirmed the dated audit pack includes README plus four reports:
    governance/harness/provider, SDLC/CI/QA/formatting/automation,
    Kubernetes/infrastructure/security, and implementation roadmap.
  - Confirmed all four reports use the required reference sections, approved
    status vocabulary, repo-backed evidence language, and repo-static versus
    live-runtime boundary language.
  - No unsupported active-policy change, live-readiness claim, secret-value
    inspection, workflow mutation, manifest mutation, policy mutation, or
    provider runtime mutation was found during local read-only review.
  - A fresh subagent review was not available in this session after the prior
    child-agent capacity failure, so final review was performed locally.
- **WEA-007 Validation Commands**:
  - `rg --files docs/90.references/audits | sort` completed.
  - Required old root-audit-path scan over
    `docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts`
    completed; remaining matches are historical evidence only.
  - Required report coverage scan over
    `docs/90.references/audits/2026-07-05-wea`
    completed.
  - `git diff --check` passed.
  - `bash scripts/validate-repo-quality-gates.sh .` passed with
    `[PASS] repository quality gates passed`.
  - `git status --short --branch` confirmed only intended closure edits before
    the final WEA-007 commit.
- **Evidence Location**:
  - This task record and [README.md](../../99.templates/templates/specs/task.template.md)

### Boundary Statement

This audit-pack implementation performed local documentation edits, repository
inspection, local validation, and local commits only. It did not perform live
Kubernetes, Argo CD, Vault, cloud, GitHub remote, provider runtime,
credential, secret-value, paid-job, publish, merge, push, or third-party
mutation.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Existing audit folderization breaks links | Current docs may point to removed paths | Run old-path scans after moves and update current navigational links before committing. |
| Audit rows overclaim implementation | Reports may imply capability exists without repo evidence | Require repo-backed evidence links for `Implemented` and `Partial`; downgrade to `Gap` or `Not in scope` when evidence is absent. |
| Stage 90 audit recommendations become active policy | Governance ownership becomes unclear | Keep recommendations in follow-up routes and roadmap; do not edit active policy, workflows, scripts, or manifests in this plan. |
| Static validation is mistaken for live readiness | Operators may trust unverified runtime state | Repeat static-vs-live boundary language in every report and task handoff. |
| Report count or matrix scope grows too large | Completion slows and review quality drops | Keep four reports with focused matrices and route future details to owner-scoped tasks. |
| Subagent edits conflict with local work | Merge noise and duplicated edits | Use one implementer task at a time, or read-only reviewers; provide disjoint write scopes if delegation is used. |

### Agent Rollout & Evaluation Gates

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

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `WEA-001 through WEA-007` is limited to these Workspace Engineering Implementation Audit Pack Task Record owners and Task-Table surfaces:
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md`
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md`
  - `docs/99.templates/templates/specs/task.template.md`
  - `docs/90.references/research/2026-07-04-wer/README.md`
  - `docs/90.references/audits/README.md`
  - `docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md`
  - `docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md`
  - `docs/90.references/audits/2026-07-02-whia/workspace-governance-implementation-audit.md`
  - `docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md`
- **Forbidden Paths**: active policy or runtime configuration not named by the Workspace Engineering Implementation Audit Pack Task Record Task Table, provider settings, secret values, local diagnostics, and remote publication surfaces.
- **Approval Required**: Human approval is required before publishing Workspace Engineering Implementation Audit Pack Task Record research, changing active policy/runtime behavior, deleting evidence, contacting providers, push, merge, or corpus expansion.
- **Static Validation**: Preserve the Workspace Engineering Implementation Audit Pack Task Record outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git status --short --branch`
  - `rg --files docs/90.references/audits docs/90.references/research docs/03.specs docs/03.specs | sort`
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Live Validation**: DEFER — Workspace Engineering Implementation Audit Pack Task Record is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Workspace Engineering Implementation Audit Pack Task Record evidence must use public or repository-visible facts only; do not inspect or reproduce credentials, tokens, auth files, private logs, kubeconfigs, or shell history.
- **Rollback Plan**: Revert the logical Workspace Engineering Implementation Audit Pack Task Record change set for `WEA-001 through WEA-007` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Workspace Engineering Implementation Audit Pack Task Record evidence remains in:
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/README.md#task-records`
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md`
  - `docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md`
  - `docs/99.templates/templates/specs/task.template.md`
  - `docs/90.references/research/2026-07-04-wer/README.md`
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

## Traceability

- **Spec**: [../../03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md](spec.md)
- **Research Pack Spec**: [../../03.specs/0017-workspace-engineering-research-pack/spec.md](../0017-workspace-engineering-research-pack/spec.md)
- **Prior Audit Pack Spec**: [../../03.specs/0010-workspace-harness-implementation-audit-pack/spec.md](../0010-workspace-harness-implementation-audit-pack/spec.md)
- **Task**: [../tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md](README.md#task-records)
- **Research Pack README**: `docs/90.references/research/2026-07-04-wer/README.md`; [current lookup](../../90.references/research/0001-workspace-engineering/README.md)
- **Stage 90 Router**: [../../90.references/README.md](../../90.references/README.md)
- **Reference Template**: [../../99.templates/templates/references/reference.template.md](../../99.templates/templates/references/reference.template.md)
- **Task Template**: [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)

### Legacy Task traceability

- **Spec**: [../../03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md](spec.md)
- **Plan**: [../plans/2026-07-05-workspace-engineering-implementation-audit-pack.md](plan.md)
- **Research Pack README**: `docs/90.references/research/2026-07-04-wer/README.md`; [current lookup](../../90.references/research/0001-workspace-engineering/README.md)
- **Stage 90 Router**: [../../90.references/README.md](../../90.references/README.md)
- **Task Index**: [README.md](../../99.templates/templates/specs/task.template.md)
