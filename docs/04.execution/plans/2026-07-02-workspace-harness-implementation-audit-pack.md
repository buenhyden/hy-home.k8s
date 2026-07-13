---
title: 'Workspace Harness Implementation Audit Pack Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
---

# Workspace Harness Implementation Audit Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a repo-backed implementation audit pack under `docs/90.references/audits/`.

**Architecture:** The work creates one audits README and four dated audit reports. Each report uses the research pack as the benchmark model, compares it to repository evidence, and records status, evidence, gaps, automation opportunities, and follow-up routes without redefining active policy.

**Tech Stack:** Markdown, `docs/99.templates/templates/common/readme.template.md`, `docs/99.templates/templates/common/reference.template.md`, Stage 04 task evidence, `rg`, `sed`, repository validation scripts, and Git commits by logical unit.

---

## Overview

This document defines the execution plan for the workspace harness
implementation audit pack. The implementation is documentation-only and must
not change provider runtime configuration, CI enforcement semantics, GitOps
desired state, credentials, or live cluster state.

## Context

The approved parent Spec is
[`../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md`](../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md).
The user selected four audit reports plus an audits README. The audit benchmark
is the current research pack under `docs/90.references/research/`, and the
implementation evidence must come from current repository files.

## Goals & In-Scope

- **Goals**:
  - Create `docs/90.references/audits/README.md`.
  - Create four audit reports under `docs/90.references/audits/`.
  - Update `docs/90.references/README.md`, Stage 04 plan/task indexes, the
    task record, and progress memory.
  - Run repo-static validation and commit by logical unit.
- **In Scope**:
  - Repo-backed comparison of research benchmark items to implementation
    evidence.
  - Audit status vocabulary: `Implemented`, `Partial`, `Gap`, `Not in scope`.
  - Automation opportunities for candidate future pipelines, workflows,
    hooks, validators, and checklist improvements.
  - Static-vs-live limitation statements in every audit report.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Changing active governance policy.
  - Changing provider adapters, hooks, CI workflows, scripts, templates, or
    manifests.
  - Installing tools, plugins, MCP servers, or external dependencies.
  - Running live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime,
    paid-job, or secret checks.
- **Out of Scope**:
  - New Claude/Codex/Gemini role definitions.
  - Secret reads or writes.
  - Pull request creation or pushing.
  - Any external resource mutation.

### File Structure

| Path | Responsibility |
| --- | --- |
| `docs/90.references/audits/README.md` | Audit folder entry point, report index, status vocabulary, evidence rules, and static-vs-live boundary. |
| `docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md` | Workspace rules, systems, environment, operating contract, templates, scripts, shared provider structure, and automation opportunities. |
| `docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md` | Harness engineering and loop engineering implementation status against the research benchmark. |
| `docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md` | Claude, Codex, and Gemini harness/loop implementation status plus common environment/rules/system parity. |
| `docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md` | Spec-driven development, SDLC, CI/CD, QA, and formatting implementation status. |
| `docs/90.references/README.md` | Parent reference hub structure and folder-role update for `audits/`. |
| `docs/04.execution/plans/README.md` | Plan index row for this execution plan. |
| `docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md` | Execution tracking and validation evidence. |
| `docs/04.execution/tasks/README.md` | Task index row for this execution task. |
| `docs/00.agent-governance/memory/progress.md` | Progress, reusable memory, validation evidence, and final handoff update. |

### Source Baseline

Use these source groups during implementation:

- Benchmark references:
  - `docs/90.references/research/README.md`
  - `docs/90.references/research/workspace-governance-baseline.md`
  - `docs/90.references/research/harness-and-loop-engineering.md`
  - `docs/90.references/research/provider-implementation-status.md`
  - `docs/90.references/research/spec-sdlc-ci-qa-formatting.md`
- Repo implementation evidence:
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/CODEX.md`
  - `.agents/**`, `.claude/**`, `.codex/**`
  - `docs/00.agent-governance/**`
  - `docs/04.execution/**`
  - `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`
  - `docs/99.templates/**`
  - `scripts/**`
  - `.github/workflows/**`
  - `.pre-commit-config.yaml`
- Existing audit precedent:
  - `docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md`

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create audits folder README and parent/index scaffolding | `docs/90.references/audits/README.md`, `docs/90.references/README.md`, Stage 04 task | VAL-SPC-001, VAL-SPC-002 | README includes status vocabulary, source/evidence rules, report index, static-vs-live boundary. |
| PLN-002 | Write workspace governance implementation audit | `2026-07-02-workspace-governance-implementation-audit.md`, audits README, task, progress | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Matrix covers workspace rules/system/environment, common provider structure, templates, scripts, operating contract, automation opportunities. |
| PLN-003 | Write harness and loop implementation audit | `2026-07-02-harness-loop-implementation-audit.md`, audits README, task | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Matrix covers harness engineering, loop engineering, feedback/eval loops, knowledge stores, review loops, automation opportunities. |
| PLN-004 | Write provider harness and loop implementation audit | `2026-07-02-provider-harness-loop-implementation-audit.md`, audits README, task | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Matrix covers Claude, Codex, Gemini, and common environment/rule/system parity. |
| PLN-005 | Write SDLC delivery practices implementation audit | `2026-07-02-sdlc-delivery-practices-implementation-audit.md`, audits README, task | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Matrix covers spec-driven development, SDLC, CI/CD, QA, formatting, and validation evidence lanes. |
| PLN-006 | Final integration, validation, status alignment, and handoff | Plan/task/index/progress files | VAL-SPC-006 | Final validation bundle passes; plan/task status and indexes are aligned. |

### Detailed Task Steps

### Task 1: Audit Folder README and Parent Scaffolding

**Files:**

- Create: `docs/90.references/audits/README.md`
- Modify: `docs/90.references/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md`

- [x] **Step 1: Read templates and existing audit precedent**

Run:

```bash
sed -n '1,220p' docs/99.templates/templates/common/readme.template.md
sed -n '1,220p' docs/99.templates/templates/common/reference.template.md
sed -n '1,220p' docs/90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md
sed -n '1,240p' docs/90.references/README.md
```

Expected: commands print README/reference template rules, the existing audit
precedent, and current reference hub structure.

- [x] **Step 2: Create audits README**

Create `docs/90.references/audits/README.md` with these sections exactly:

- `# 90.references/audits`
- `## Overview`
- `## Audience`
- `## Scope`
- `## Structure`
- `## How to Work in This Area`
- `## Link Basis`
- `## Audit Report Index`
- `## Status Vocabulary`
- `## Evidence Rules`
- `## Related Documents`

The README must state:

- Audit reports are dated reference snapshots.
- `Implemented`, `Partial`, `Gap`, and `Not in scope` are the only audit
  status values.
- Repo-backed evidence outranks upstream capability for local implementation
  status.
- Repo-static validation does not imply live runtime readiness.

- [x] **Step 3: Update parent references README**

Update `docs/90.references/README.md`:

- Add `audits/` to the structure tree.
- Add `audits/README.md` to the Reference Index.
- Add `audits/` to Reference Folder Roles.
- Add the audits README to Related Documents.

- [x] **Step 4: Update task evidence**

In the task record:

- Mark T-001 as `Done`.
- Check T-001 in Phase View.
- Add evidence rows for manual README/template review, `git diff --check`, and
  `bash scripts/validate-repo-quality-gates.sh .`.

- [x] **Step 5: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

- `git diff --check`: no output.
- `bash scripts/validate-repo-quality-gates.sh .`: includes
  `[PASS] repository quality gates passed`.

Commit:

```bash
git add docs/90.references/audits/README.md docs/90.references/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md
git commit -m "docs(audit): Scaffold workspace harness audit references"
```

### Task 2: Workspace Governance Implementation Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Gather benchmark and repo evidence**

Run:

```bash
sed -n '1,260p' docs/90.references/research/workspace-governance-baseline.md
sed -n '1,260p' docs/00.agent-governance/harness-catalog.md
sed -n '1,220p' docs/00.agent-governance/common-governance.md
sed -n '1,220p' docs/00.agent-governance/harness-implementation-map.md
sed -n '1,220p' scripts/README.md
sed -n '1,220p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
```

Expected: commands print the governance benchmark and current implementation
evidence for rules, adapters, scripts, templates, validation, and QA/CI lanes.

- [x] **Step 2: Write the governance audit report**

Create the report from `docs/99.templates/templates/common/reference.template.md` with:

- `title: 'Reference: Workspace Governance Implementation Audit'`
- `type: reference`
- `status: draft`
- `owner: platform`
- `updated: 2026-07-02`
- `Reference Type`: `durable-concept / external-standard-snapshot`
- `Source checked`: `2026-07-02`
- `Refresh trigger`: Stage 00 governance, provider adapter, template, script,
  CI/QA, or audit benchmark changes.

Inside `Definitions / Facts`, include these subsections:

- `Benchmark Model`
- `Implementation Matrix`
- `Comparison Analysis`
- `Automation Opportunities`
- `Implementation Checklist`
- `Residual Risks`

The implementation matrix must include rows for:

- Workspace purpose and operating model
- Rules and governance system
- Provider adapter and shared asset structure
- Templates and formatting routing
- Scripts and validation
- CI/CD and QA evidence lanes
- Operating contract and approval boundaries
- Automation opportunities

- [x] **Step 3: Update indexes and evidence**

Update `docs/90.references/audits/README.md` to mark the governance audit as
`Current`. Update T-002 to `Done` with manual review and validation evidence.
Append progress memory noting that the governance audit is complete and that
it is documentation-only.

- [x] **Step 4: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/90.references/audits/2026-07-02-workspace-governance-implementation-audit.md docs/90.references/audits/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(audit): Assess workspace governance implementation"
```

### Task 3: Harness and Loop Implementation Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md`

- [x] **Step 1: Gather benchmark and repo evidence**

Run:

```bash
sed -n '1,320p' docs/90.references/research/harness-and-loop-engineering.md
sed -n '1,300p' docs/00.agent-governance/harness-catalog.md
sed -n '1,260p' docs/00.agent-governance/harness-implementation-map.md
sed -n '1,220p' docs/00.agent-governance/subagent-protocol.md
sed -n '1,220p' docs/00.agent-governance/rules/agentic.md
sed -n '1,220p' docs/00.agent-governance/memory/README.md
```

Expected: commands print benchmark model and evidence for four-element
harness, feedback loops, subagent protocol, validation loops, and memory.

- [x] **Step 2: Write the harness/loop audit report**

Create the report from `reference.template.md` with the same audit subsections
as Task 2.

The implementation matrix must include rows for:

- Instruction/settings surfaces
- Architecture constraints
- Feedback loops
- Knowledge stores
- Observe/plan/act/verify/learn loop
- Eval/review loops
- Subagent/worktree/review-loop practices
- MCP/tool boundary implications
- Automation opportunities

- [x] **Step 3: Update index and evidence**

Update `docs/90.references/audits/README.md` to mark the harness/loop audit as
`Current`. Update T-003 to `Done` with manual review and validation evidence.

- [x] **Step 4: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/90.references/audits/2026-07-02-harness-loop-implementation-audit.md docs/90.references/audits/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md
git commit -m "docs(audit): Assess harness and loop implementation"
```

### Task 4: Provider Harness and Loop Implementation Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md`

- [x] **Step 1: Gather benchmark and repo evidence**

Run:

```bash
sed -n '1,340p' docs/90.references/research/provider-implementation-status.md
sed -n '1,220p' docs/00.agent-governance/providers/claude.md
sed -n '1,220p' docs/00.agent-governance/providers/codex.md
sed -n '1,220p' docs/00.agent-governance/providers/gemini.md
sed -n '1,220p' docs/00.agent-governance/common-governance.md
find .claude/agents .codex/agents .agents/agents -maxdepth 1 -type f | sort
```

Expected: commands print provider benchmark and current local provider adapter
evidence. If a file is missing, record the absence as evidence instead of
inferring status.

- [x] **Step 2: Write the provider audit report**

Create the report from `reference.template.md` with the same audit subsections
as Task 2.

The implementation matrix must include rows for each provider and common
parity:

- Claude instruction/settings, subagents, hooks/permissions, skills, MCP,
  sandbox/approvals, feedback loops
- Codex instruction/settings, subagents, hooks/permissions, skills, MCP,
  sandbox/approvals, feedback loops
- Gemini instruction/settings, agents, hooks/permissions, skills, MCP,
  sandbox/approvals, feedback loops
- Common environment/rule/system parity
- Known non-parity boundaries
- Automation opportunities

- [x] **Step 3: Update index and evidence**

Update `docs/90.references/audits/README.md` to mark the provider audit as
`Current`. Update T-004 to `Done` with manual review and validation evidence.

- [x] **Step 4: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md docs/90.references/audits/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md
git commit -m "docs(audit): Assess provider harness implementation"
```

### Task 5: SDLC Delivery Practices Implementation Audit

**Files:**

- Create: `docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md`

- [x] **Step 1: Gather benchmark and repo evidence**

Run:

```bash
sed -n '1,340p' docs/90.references/research/spec-sdlc-ci-qa-formatting.md
sed -n '1,220p' docs/03.specs/README.md
sed -n '1,220p' docs/04.execution/plans/README.md
sed -n '1,220p' docs/04.execution/tasks/README.md
sed -n '1,220p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
sed -n '1,220p' .github/workflows/ci.yml
sed -n '1,220p' .pre-commit-config.yaml
```

Expected: commands print benchmark model and repo evidence for spec-driven
development, SDLC, CI/CD, QA, formatting, and pre-commit.

- [x] **Step 2: Write the SDLC/delivery audit report**

Create the report from `reference.template.md` with the same audit subsections
as Task 2.

The implementation matrix must include rows for:

- Spec-driven development
- Stage 03 Spec lifecycle
- Stage 04 Plan/Task lifecycle
- SDLC and secure SDLC evidence lanes
- CI/CD jobs
- QA validation commands
- Formatting and pre-commit
- Static-vs-live readiness boundary
- Automation opportunities

- [x] **Step 3: Update index and evidence**

Update `docs/90.references/audits/README.md` to mark the SDLC/delivery audit as
`Current`. Update T-005 to `Done` with manual review and validation evidence.

- [x] **Step 4: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md docs/90.references/audits/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md
git commit -m "docs(audit): Assess SDLC delivery implementation"
```

### Task 6: Final Integration, Validation, and Handoff

**Files:**

- Modify: `docs/04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Align plan/task completion state**

Update this plan and the task record:

- Mark all plan checkboxes as complete.
- Set plan frontmatter `status: done`.
- Set task frontmatter `status: done`.
- Mark T-006 as `Done`.
- Check T-006 in Phase View.

- [x] **Step 2: Update indexes and progress memory**

Update:

- `docs/04.execution/plans/README.md`: add or update this plan row to `Done`.
- `docs/04.execution/tasks/README.md`: add or update this task row to `Done`.
- `docs/00.agent-governance/memory/progress.md`: set the audit pack entry to
  `complete`, summarize created audit reports, record final validation
  evidence, and state that no live runtime readiness check was run.

- [x] **Step 3: Run final validation**

Run:

```bash
git diff --check
bash scripts/generate-llm-wiki-index.sh --check
bash scripts/validate-repo-quality-gates.sh .
rg --files | rg '(^|/)progress\.md$'
rg -n '^status: draft|^- \\[ \\]' docs/04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md
rg -n 'workspace-harness-implementation-audit-pack.*\\| Draft \\|' docs/04.execution/plans/README.md docs/04.execution/tasks/README.md
```

Expected:

- `git diff --check`: no output.
- LLM wiki check: `[PASS] LLM WIKI generated index is current`.
- Quality gate: `[PASS] repository quality gates passed`.
- Progress singleton: only `docs/00.agent-governance/memory/progress.md`.
- Stale-marker scan: no rows for the audit pack remain `Draft` or unchecked.

- [x] **Step 4: Commit final integration**

Commit:

```bash
git add docs/04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md docs/04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(audit): Finalize workspace harness implementation audit pack"
```

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Diff whitespace check | `git diff --check` | No output and zero exit code. |
| VAL-PLN-002 | Generated index | LLM wiki index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | Prints `[PASS] LLM WIKI generated index is current`. |
| VAL-PLN-003 | Repo quality | Repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed`. |
| VAL-PLN-004 | Progress singleton | Canonical progress ledger uniqueness | `rg --files \| rg '(^\|/)progress\.md$'` | Prints only `docs/00.agent-governance/memory/progress.md`. |
| VAL-PLN-005 | Status alignment | No stale audit-pack draft/checklist markers | Targeted `rg` commands from Task 6 Step 3 | No audit-pack frontmatter remains `draft`, no audit-pack checklist remains unchecked, and no audit-pack README row remains `Draft`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Audit reports accidentally redefine active policy | High | Keep all findings as reference snapshots and route follow-up to canonical owners. |
| Upstream provider capability is mistaken for local implementation | High | Status must depend on repo-backed evidence, not upstream capability alone. |
| Audit matrices become too broad or repetitive | Medium | Keep four report boundaries aligned to the approved research pack categories. |
| Static validation is overstated as live readiness | High | Repeat static-vs-live boundary in README, reports, task evidence, and progress memory. |
| Existing `audits/` folder lacks README | Low | Create README first and update parent reference hub in the scaffold commit. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Use repo-static validation only.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only work.
- **Human Approval Gate**: Required for live runtime validation, CI topology
  changes, provider config changes, runtime role changes, GitOps manifest
  changes, secret handling changes, pushes, PR creation, or external resource
  mutation.
- **Rollback Trigger**: If an audit report introduces active policy or
  overstates implementation status, rewrite the affected report or revert the
  affected documentation commit.
- **Prompt / Model Promotion Criteria**: Not applicable; no model or prompt
  surface is promoted.

## Completion Criteria

- [x] `docs/90.references/audits/README.md` exists and indexes all audit
  reports.
- [x] Four new dated audit reports exist and follow the reference template plus
  audit subsections.
- [x] Parent `docs/90.references/README.md` indexes `audits/`.
- [x] Audit matrices cover all requested categories from the parent Spec.
- [x] Automation opportunities and implementation checklists are present in
  each report.
- [x] Task evidence and progress memory are updated.
- [x] Final validation commands pass.
- [x] Work is committed by logical unit.

## Traceability

- **ARD**:
  `[../../02.architecture/requirements/0006-workspace-agent-governance-platform.md]`
- **ADR**:
  `[../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md]`
- **Spec**:
  `[../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md]`
- **Task**: [../tasks/2026-07-02-workspace-harness-implementation-audit-pack.md](../tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)
- **Research README**:
  `[../../90.references/research/README.md]`
- **Audits README**:
  `../../90.references/audits/README.md`
- **Reference Maintenance Runbook**:
  `[../../05.operations/runbooks/0011-reference-maintenance-runbook.md]`
