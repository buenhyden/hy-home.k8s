---
title: 'Workspace Harness Research Pack Implementation Plan'
type: plan
status: done
owner: platform
updated: 2026-07-02
---

# Workspace Harness Research Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a repo-first, source-attributed integrated research pack under `docs/90.references/research/`.

**Architecture:** The work creates one research folder README and four focused reference documents. Each document follows the existing reference template, keeps official sources authoritative, labels market scan findings as non-authoritative, and maps implementation checklist items back to canonical repo owners instead of redefining policy.

**Tech Stack:** Markdown, `docs/99.templates/reference.template.md`, `docs/99.templates/readme.template.md`, repository quality gates, web-sourced official documentation, and bounded market scan sources.

---

## Overview

This document defines the execution plan for the workspace harness research
pack. The implementation is documentation-only and must keep live cluster,
secret, CI enforcement, provider runtime, and external resource mutation out of
scope.

## Context

The approved parent Spec is
[`../../03.specs/009-workspace-harness-research-pack/spec.md`](../../03.specs/009-workspace-harness-research-pack/spec.md).
The user requested an integrated research pack with README plus three to five
reference documents. The selected design is one README plus four reference
documents, using a repo-first and official-source-first approach while also
including bounded market scan and implementation checklist sections.

## Goals & In-Scope

- **Goals**:
  - Create `docs/90.references/research/README.md`.
  - Create `workspace-governance-baseline.md`.
  - Create `harness-and-loop-engineering.md`.
  - Create `provider-implementation-status.md`.
  - Create `spec-sdlc-ci-qa-formatting.md`.
  - Update `docs/90.references/README.md`, `docs/04.execution/plans/README.md`,
    `docs/04.execution/tasks/README.md`, and
    `docs/00.agent-governance/memory/progress.md`.
  - Run repo-static validation and commit by logical unit.
- **In Scope**:
  - Repository evidence review from Stage 00 governance, templates, scripts,
    CI, reference docs, and progress memory.
  - Official external-source review for Claude, Codex/OpenAI, Gemini/Google,
    MCP, spec-driven development, SDLC, CI/CD, QA, and formatting.
  - Market scan findings clearly marked as non-authoritative.
  - Implementation checklist sections that name repo owners and follow-up
    routes.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Changing active governance policy or CI semantics.
  - Installing external tools or plugins.
  - Running live k3d, ArgoCD, Vault, ESO, Kubernetes, or cloud-provider checks.
  - Publishing, pushing, opening PRs, or changing third-party state without
    explicit human approval.
- **Out of Scope**:
  - GitOps manifest edits.
  - Secret value reads or writes.
  - Provider runtime adapter changes.
  - New validation scripts.

## File Structure

| Path | Responsibility |
| --- | --- |
| `docs/90.references/research/README.md` | Entry point, reading order, folder scope, index, authority boundary, and related documents. |
| `docs/90.references/research/workspace-governance-baseline.md` | Repo-first baseline for purpose, roles, governance, operating contract, automation, templates, scripts, CI/CD, QA, formatting, and evidence lanes. |
| `docs/90.references/research/harness-and-loop-engineering.md` | Harness engineering and loop engineering definitions, official-source analysis, market scan, workspace application requirements, and checklist. |
| `docs/90.references/research/provider-implementation-status.md` | Claude, Codex/OpenAI, and Gemini/Google implementation status for harness/loop capabilities and shared environment construction. |
| `docs/90.references/research/spec-sdlc-ci-qa-formatting.md` | Spec-driven development, SDLC, CI/CD, QA, formatting, and verification analysis mapped to this repo. |
| `docs/90.references/README.md` | Parent reference index and structure update for the new `research/` folder. |
| `docs/04.execution/plans/README.md` | Plan index update. |
| `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md` | Execution tracking and validation evidence. |
| `docs/04.execution/tasks/README.md` | Task index update. |
| `docs/00.agent-governance/memory/progress.md` | Progress, reusable memory, validation evidence, and handoff update. |

## Source Baseline

Use the following source groups during implementation.

Official or primary sources:

- Repo governance: `AGENTS.md`, `.codex/CODEX.md`,
  `docs/00.agent-governance/**`, `docs/99.templates/**`, `scripts/**`,
  `.github/workflows/**`.
- Claude Code: `https://docs.anthropic.com/en/docs/claude-code/hooks`,
  `https://docs.anthropic.com/en/docs/claude-code/sub-agents`,
  `https://docs.anthropic.com/en/docs/claude-code/skills`,
  `https://docs.anthropic.com/en/docs/claude-code/settings`,
  `https://docs.anthropic.com/en/docs/claude-code/mcp`.
- OpenAI Codex: `https://developers.openai.com/codex/cli`,
  `https://developers.openai.com/codex/config-reference`,
  `https://developers.openai.com/codex/agent-approvals-security`,
  `https://developers.openai.com/codex/concepts/sandboxing`,
  `https://developers.openai.com/codex/mcp`,
  `https://openai.com/index/unrolling-the-codex-agent-loop/`,
  `https://openai.com/index/harness-engineering/`.
- Gemini / Google: `https://github.com/google-gemini/gemini-cli`,
  `https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md`,
  `https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk`,
  `https://adk.dev/`,
  `https://codelabs.developers.google.com/adk-eval/instructions`.
- MCP: `https://modelcontextprotocol.io/specification/2025-06-18`,
  `https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices`.
- SDLC / CI / QA / formatting:
  `https://csrc.nist.gov/pubs/sp/800/218/final`,
  `https://csrc.nist.gov/News/2024/nist-publishes-sp-800204d`,
  `https://docs.github.com/actions`,
  `https://docs.github.com/en/actions/reference/security/secure-use`,
  `https://pre-commit.com/`,
  `https://github.github.com/spec-kit/`,
  `https://github.com/github/spec-kit`,
  `https://martinfowler.com/articles/continuousIntegration.html`.

Market scan and comparative sources:

- `https://www.anthropic.com/research/building-effective-agents`
- `https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents`
- `https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop`
- `https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/`
- Current market articles on loop engineering, agent harnesses, and coding-agent workflows, labeled as non-authoritative and refreshed at write time.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create research folder scaffold and source ledger | `docs/90.references/research/README.md`, `docs/90.references/README.md` | VAL-SPC-001, VAL-SPC-006 | README has Link Basis and Related Documents; parent README indexes `research/`. |
| PLN-002 | Write workspace governance baseline reference | `docs/90.references/research/workspace-governance-baseline.md` | VAL-SPC-003, VAL-SPC-005 | Reference template headings present; repo-first categories covered. |
| PLN-003 | Write harness and loop engineering reference | `docs/90.references/research/harness-and-loop-engineering.md` | VAL-SPC-004, VAL-SPC-005 | Harness, loop, market scan, and implementation checklist sections present. |
| PLN-004 | Write provider implementation status reference | `docs/90.references/research/provider-implementation-status.md` | VAL-SPC-004, VAL-SPC-005 | Claude, Codex/OpenAI, and Gemini/Google sections cite current sources and mark unknowns. |
| PLN-005 | Write spec/SDLC/CI/QA/formatting reference | `docs/90.references/research/spec-sdlc-ci-qa-formatting.md` | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | SDD, SDLC, CI/CD, QA, formatting, and validation matrix mapped to repo controls. |
| PLN-006 | Integrate indexes, task evidence, memory, and validation | `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`, `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | VAL-SPC-006 | Repo-static validation passes and task evidence records executed commands. |

## Detailed Task Steps

### Task 1: Research Folder Scaffold and Source Ledger

**Files:**

- Create: `docs/90.references/research/README.md`
- Modify: `docs/90.references/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`

- [x] **Step 1: Read templates and parent README**

Run:

```bash
sed -n '1,220p' docs/99.templates/readme.template.md
sed -n '1,220p' docs/99.templates/reference.template.md
sed -n '1,260p' docs/90.references/README.md
```

Expected: commands print the README/reference template contracts and current
reference index.

- [x] **Step 2: Create `docs/90.references/research/README.md`**

Include these sections exactly: `# 90.references/research`, `## Overview`,
`## Audience`, `## Scope`, `## Structure`, `## How to Work in This Area`,
`## Link Basis`, `## Research Pack Index`, `## Source Priority`, `## Related Documents`.

The README must state that official and repo-backed sources outrank market scan
sources, and that market findings are non-authoritative.

- [x] **Step 3: Update parent reference README**

Add `research/` to the structure tree, Reference Index, Reference Folder Roles,
and Related Documents in `docs/90.references/README.md`. Keep Korean
human-facing prose and do not redefine governance policy.

- [x] **Step 4: Validate the scaffold**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass. If `validate-repo-quality-gates.sh` fails on a
new README/index issue, fix the README structure before continuing.

- [x] **Step 5: Commit scaffold**

Run:

```bash
git add docs/90.references/research/README.md docs/90.references/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md
git commit -m "docs(research): Scaffold workspace harness research references"
```

Expected: one commit containing the research folder README and parent index
updates.

### Task 2: Workspace Governance Baseline Reference

**Files:**

- Create: `docs/90.references/research/workspace-governance-baseline.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Gather repo evidence**

Run:

```bash
sed -n '1,260p' AGENTS.md
sed -n '1,280p' docs/00.agent-governance/rules/bootstrap.md
sed -n '1,300p' docs/00.agent-governance/harness-catalog.md
sed -n '1,260p' docs/00.agent-governance/harness-implementation-map.md
sed -n '1,260p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
sed -n '1,220p' scripts/README.md
```

Expected: commands print the current workspace purpose, governance, harness,
CI/QA, and scripts evidence.

- [x] **Step 2: Write the baseline document**

Create the document from `docs/99.templates/reference.template.md` with:

- `title: 'Reference: Workspace Governance Baseline Research'`
- `type: reference`
- `status: draft`
- `owner: platform`
- `updated: 2026-07-02`
- `Reference Type`: `durable-concept / external-standard-snapshot`
- `Source checked`: `2026-07-02`
- `Refresh trigger`: governance, CI, scripts, templates, provider adapter, or research pack structure changes

The `Definitions / Facts` section must include subsections for:

- Workspace purpose and operating model
- Roles and provider adapters
- CI/CD and QA
- Automation and hooks
- Templates and formatting
- Scripts and validation
- Operating contract and approval boundaries
- Integration guides and SDLC position
- Governance system and rules
- Implementation checklist

- [x] **Step 3: Update indexes and task evidence**

Add the document to `docs/90.references/research/README.md` and update the task
record status for this task to `Done` with evidence commands.

- [x] **Step 4: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/workspace-governance-baseline.md docs/90.references/research/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Document workspace governance baseline"
```

Expected: validation passes and the commit contains only baseline-related docs
and evidence updates.

### Task 3: Harness and Loop Engineering Reference

**Files:**

- Create: `docs/90.references/research/harness-and-loop-engineering.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`

- [x] **Step 1: Gather official and market scan sources**

Browse or open current sources for OpenAI harness engineering, OpenAI Codex
agent loop, OpenAI agent improvement loop, Anthropic building effective agents,
Anthropic evals for agents, MCP specification, MCP security best practices, and
one or two current market-scan articles on loop engineering.

Expected: record source URLs and source-checked date in the draft.

- [x] **Step 2: Write the harness/loop document**

Create the document from `reference.template.md` with:

- `Reference Type`: `durable-concept / external-standard-snapshot`
- `Authority Boundary`: authoritative for definitions and source-attributed
  analysis, not authoritative for repo policy.
- `Definitions / Facts` subsections for:
  - Harness engineering elements
  - Loop engineering elements
  - Feedback and eval loops
  - Worktree/subagent/review-loop implications
  - MCP and tool boundary implications
  - Market scan findings
  - Workspace application requirements
  - Implementation checklist

Market scan findings must be labeled `Non-authoritative market scan`.

- [x] **Step 3: Update index, task evidence, validate, and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/harness-and-loop-engineering.md docs/90.references/research/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md
git commit -m "docs(research): Analyze harness and loop engineering"
```

Expected: validation passes and the commit contains the harness/loop reference.

### Task 4: Provider Implementation Status Reference

**Files:**

- Create: `docs/90.references/research/provider-implementation-status.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`

- [x] **Step 1: Gather provider sources**

Browse or open current official sources for:

- Claude Code hooks, subagents, skills, settings, MCP, and release notes.
- OpenAI Codex CLI, config reference, sandboxing, agent approvals/security,
  MCP, changelog, and agent-loop article.
- Gemini CLI repository and MCP docs, Google Gemini Code Assist agent mode, and
  Google ADK docs/eval codelab.

Expected: record the source URLs and note any provider feature that cannot be
verified from official docs.

- [x] **Step 2: Write the provider status document**

Create the document from `reference.template.md` with sections for:

- Provider capability matrix
- Claude implementation status
- Codex/OpenAI implementation status
- Gemini/Google implementation status
- Common environment and rule system
- Shared MCP/tooling considerations
- Current gaps and uncertainty
- Workspace implementation checklist

Each provider section must distinguish repo-local implementation from upstream
provider capability.

- [x] **Step 3: Update index, task evidence, validate, and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/provider-implementation-status.md docs/90.references/research/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md
git commit -m "docs(research): Compare provider harness implementations"
```

Expected: validation passes and the commit contains the provider comparison.

### Task 5: Spec, SDLC, CI, QA, and Formatting Reference

**Files:**

- Create: `docs/90.references/research/spec-sdlc-ci-qa-formatting.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`

- [x] **Step 1: Gather delivery-practice sources**

Browse or open current sources for NIST SSDF, NIST SP 800-204D, GitHub Actions
docs/security, GitHub Spec Kit, pre-commit docs, Martin Fowler Continuous
Integration, and repo-local CI/QA docs.

Expected: record source URLs and source-checked date in the draft.

- [x] **Step 2: Write the delivery-practice document**

Create the document from `reference.template.md` with subsections for:

- Spec-driven development
- SDLC and secure SDLC
- CI/CD
- QA and validation evidence
- Formatting and pre-commit
- Repo-local validation matrix
- Market scan findings
- Implementation checklist

The document must state that repo-static validation does not prove live runtime
readiness.

- [x] **Step 3: Update index, task evidence, validate, and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/spec-sdlc-ci-qa-formatting.md docs/90.references/research/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md
git commit -m "docs(research): Map SDD SDLC CI QA formatting practices"
```

Expected: validation passes and the commit contains the delivery-practice
reference.

### Task 6: Integration, Validation, and Handoff

**Files:**

- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/README.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Update plan and task indexes**

Add this plan and task to their stage README index tables with the current
lifecycle status and `2026-07-02` updated date.

- [x] **Step 2: Complete task evidence and progress memory**

Update the task record with final validation command results and update the
progress ledger status to `complete` only after all reference documents and
checks are complete.

- [x] **Step 3: Run final validation**

Run:

```bash
git diff --check
bash scripts/generate-llm-wiki-index.sh --check
bash scripts/validate-repo-quality-gates.sh .
rg --files | rg '(^|/)progress\.md$'
```

Expected:

- `git diff --check`: no output and exit 0.
- `generate-llm-wiki-index.sh --check`: `[PASS] LLM WIKI generated index is current`.
- `validate-repo-quality-gates.sh .`: `[PASS] repository quality gates passed`.
- `rg --files | rg '(^|/)progress\.md$'`: only
  `docs/00.agent-governance/memory/progress.md`.

- [x] **Step 4: Review final diff**

Run:

```bash
git status --short
git diff --stat
```

Expected: only research pack, indexes, task evidence, and progress memory files
are modified.

- [x] **Step 5: Commit integration**

Run:

```bash
git add docs/90.references/research/README.md docs/90.references/README.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Finalize workspace harness research pack"
```

Expected: one final integration commit.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Markdown whitespace check | `git diff --check` | Exit 0 with no output. |
| VAL-PLN-002 | Generated index | LLM Wiki freshness | `bash scripts/generate-llm-wiki-index.sh --check` | Prints `[PASS] LLM WIKI generated index is current`. |
| VAL-PLN-003 | Repo quality | Template, README, link, and governance gates | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed`. |
| VAL-PLN-004 | Memory singleton | Confirm only canonical progress ledger exists | `rg --files \| rg '(^\|/)progress\.md$'` | Prints only `docs/00.agent-governance/memory/progress.md`. |
| VAL-PLN-005 | Source attribution | Confirm each reference has `Sources` and `Review and Freshness` | Manual review plus repo gate | Every reference document contains required sections and source-checked date. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Provider docs change during or after authoring | Medium | Record `Source checked: 2026-07-02` and refresh triggers; avoid unverified current-status claims. |
| Market scan conflicts with official sources | Medium | Prefer official sources and label market scan findings non-authoritative. |
| Reference docs accidentally redefine governance | High | Keep checklist items as candidate follow-up and name canonical owners for real policy changes. |
| Research pack becomes too broad | Medium | Keep the approved four-document structure and route deeper follow-up to future plans. |
| Validation fails on README/template shape | Medium | Fix the smallest README or reference-template conformance issue before continuing. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Use repository-static validation only; no live runtime
  eval is in scope.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only work.
- **Human Approval Gate**: Required for live runtime validation, provider config
  changes, CI enforcement changes, GitOps manifest changes, secret handling
  changes, pushes, PR creation, or external resource mutation.
- **Rollback Trigger**: If a reference introduces conflicting active policy,
  revert the affected documentation commit or rewrite it as non-authoritative
  analysis.
- **Prompt / Model Promotion Criteria**: Not applicable; no model or prompt
  surface is promoted.

## Completion Criteria

- [x] `docs/90.references/research/README.md` exists and indexes all four
  reference documents.
- [x] Four reference documents exist and use the reference template structure.
- [x] Official source findings, market scan findings, and implementation
  checklist sections are present where required.
- [x] Parent `docs/90.references/README.md` indexes the new folder.
- [x] Plan and task README indexes are updated.
- [x] Task evidence and progress memory are updated.
- [x] Final validation commands pass.
- [x] Work is committed by logical unit.

## Related Documents

- **PRD**: `../../01.requirements/2026-06-01-workspace-agent-governance-platform.md`
- **ARD**: `../../02.architecture/requirements/0006-workspace-agent-governance-platform.md`
- **Spec**: `../../03.specs/009-workspace-harness-research-pack/spec.md`
- **ADR**: `../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md`
- **Tasks**: `../tasks/2026-07-02-workspace-harness-research-pack.md`
