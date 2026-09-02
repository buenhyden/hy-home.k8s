---
title: 'Workspace Engineering Research Pack Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-07-13
artifact_id: "SPEC-0017-PLAN-0001"
---

# Workspace Engineering Research Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dated, repo-first workspace engineering research pack under `docs/90.references/research/2026-07-04-wer/`.

**Architecture:** The plan uses a source-first document migration sequence. First create Stage 04 evidence, then move the current four research references into the dated pack, then refresh existing references and add two focused references, and finally close validation evidence.

**Tech Stack:** Markdown, Stage 90 reference template, Stage 04 task evidence, `git mv`, web-verified official sources, `rg`, repository quality gates, and repo-static harness validation.

---

## Overview

This document defines the implementation plan for
`docs/03.specs/0017-workspace-engineering-research-pack/spec.md`.
The implementation creates a dated research pack, moves the four current flat
research references into that pack, adds two focused references, updates
indexes, and records validation evidence.

The research pack is descriptive reference material. It does not define active
policy, runbooks, release gates, CI semantics, provider runtime permissions, or
live cluster procedure.

## Context

The approved structure is:

```text
docs/90.references/research/
`-- 2026-07-04-wer/
    |-- README.md
    |-- workspace-governance-baseline.md
    |-- m0002-harness-and-loop-engineering.md
    |-- m0003-provider-implementation-status.md
    |-- spec-sdlc-ci-qa-formatting.md
    |-- kubernetes-infrastructure-security.md
    `-- automation-pipeline-workflow-qa.md
```

The four current research references are moved into the dated folder:

- `docs/90.references/research/workspace-governance-baseline.md`
- `docs/90.references/research/m0002-harness-and-loop-engineering.md`
- `docs/90.references/research/m0003-provider-implementation-status.md`
- `docs/90.references/research/spec-sdlc-ci-qa-formatting.md`

External source claims must be checked during implementation. Official or
primary sources outrank market scan material. Market scan material is allowed
only when labeled non-authoritative.

### Legacy Task ledger inputs

This document tracks implementation and verification work for the dated
workspace engineering research pack under
`docs/90.references/research/2026-07-04-wer/`.
It records task evidence for the parent Spec and Plan without mutating live
Kubernetes, Argo CD, Vault, cloud resources, GitHub remote state, provider
runtimes, credentials, secret values, or third-party systems.

- **Parent Spec**: [../../03.specs/0017-workspace-engineering-research-pack/spec.md](spec.md)
- **Parent Plan**: [../plans/2026-07-04-workspace-engineering-research-pack.md](plan.md)
- **Task Template**: [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)
## Goals & In-Scope

- **Goals**:
  - Create Stage 04 task evidence for this research-pack implementation.
  - Move existing research references into one dated pack folder.
  - Refresh the existing four references with repo-first and official-source
    evidence checked on 2026-07-04.
  - Add focused references for Kubernetes/infrastructure/security and
    automation/pipeline/workflow/QA.
  - Update research and parent indexes.
  - Run repository validation and focused stale-link/source-boundary scans.
- **In Scope**:
  - `docs/90.references/research/**`
  - `docs/90.references/README.md`
  - `docs/03.specs/**`
  - `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
  - `docs/00.agent-governance/memory/progress.md`
  - Read-only review of repo governance, templates, scripts, `.github`,
    GitOps, infrastructure, policy, tests, and Traefik surfaces.
  - Read-only web research using official or primary sources.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Change active governance policy.
  - Change CI workflow architecture or validation script semantics.
  - Install tools, add MCP servers, or change provider adapters.
  - Prove live runtime readiness.
- **Out of Scope**:
  - Live Kubernetes, Argo CD, Vault, ESO, cloud, DNS, GitHub remote, provider
    runtime, or third-party resource mutation.
  - Secret value inspection, credential regeneration, certificate changes, or
    paid external jobs.
  - Remote push, PR creation, publish, or merge without separate approval.

### File Structure

| Path | Responsibility |
| --- | --- |
| `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records` | Execution evidence, task table, validation commands, source limitations, handoff. |
| `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records` | Task index entry for the research-pack work. |
| `docs/90.references/research/README.md` | Research stage entrypoint and dated pack index. |
| `docs/90.references/research/2026-07-04-wer/README.md` | Dated pack entrypoint, reading order, source priority, and authority boundary. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | Repo-first workspace purpose, roles, governance, contracts, templates, scripts, integration guides, and evidence lanes. |
| `docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md` | Harness engineering and loop engineering definitions, elements, workspace application requirements, and implementation checklist. |
| `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md` | Claude, Codex, Gemini provider status and shared environment/rule/system construction analysis. |
| `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | Spec-driven development, SDLC, CI/CD, QA, formatting, linting, syntax validation, and repo validation matrix. |
| `docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md` | Kubernetes, infrastructure, GitOps, secrets, policy-as-code, supply-chain, and security reference. |
| `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md` | Automation, pipeline, workflow, CI job graph, validation loops, and QA evidence lanes reference. |
| `docs/90.references/README.md` | Parent reference index update for the dated research pack. |
| `docs/00.agent-governance/memory/progress.md` | Progress and reusable memory update after implementation stages. |

### Source Baseline

Use web research during implementation for current external claims. Start with
these official or primary source families:

- OpenAI and Codex:
  - <https://developers.openai.com/codex/>
  - <https://developers.openai.com/codex/cli>
  - <https://developers.openai.com/codex/config-reference>
  - <https://developers.openai.com/codex/agent-approvals-security>
  - <https://developers.openai.com/codex/concepts/sandboxing>
  - <https://developers.openai.com/codex/mcp>
  - <https://openai.com/index/harness-engineering/>
  - <https://openai.com/index/unrolling-the-codex-agent-loop/>
- Anthropic Claude Code:
  - <https://docs.anthropic.com/en/docs/claude-code/settings>
  - <https://docs.anthropic.com/en/docs/claude-code/hooks>
  - <https://docs.anthropic.com/en/docs/claude-code/sub-agents>
  - <https://docs.anthropic.com/en/docs/claude-code/skills>
  - <https://docs.anthropic.com/en/docs/claude-code/mcp>
- Google Gemini and ADK:
  - <https://github.com/google-gemini/gemini-cli>
  - <https://github.com/google-gemini/gemini-cli/tree/main/docs>
  - <https://cloud.google.com/products/gemini/code-assist>
  - <https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk>
  - <https://adk.dev/>
- Kubernetes, GitOps, policy, and secrets:
  - <https://kubernetes.io/docs/concepts/>
  - <https://kubernetes.io/docs/concepts/configuration/secret/>
  - <https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/>
  - <https://opengitops.dev/>
  - <https://argo-cd.readthedocs.io/>
  - <https://argoproj.github.io/rollouts/>
  - <https://external-secrets.io/latest/>
  - <https://www.openpolicyagent.org/>
  - <https://www.conftest.dev/>
- SDLC, CI/CD, QA, formatting, and security:
  - <https://docs.github.com/actions>
  - <https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions>
  - <https://docs.github.com/en/code-security>
  - <https://github.com/github/spec-kit>
  - <https://csrc.nist.gov/pubs/sp/800/218/final>
  - <https://csrc.nist.gov/pubs/sp/800/204/d/final>
  - <https://slsa.dev/>
  - <https://openssf.org/>
  - <https://pre-commit.com/>
  - <https://spec.commonmark.org/>
  - <https://yaml.org/spec/1.2.2/>

Market scan material is allowed after official sources. Label it
non-authoritative in the document section where it is used.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| WER-001 | Create task evidence and baseline inventory | Task record, tasks README, progress memory | VAL-SPC-001, VAL-SPC-006 | Baseline repo/source inventory recorded; repo-quality gate passes |
| WER-002 | Scaffold dated pack and move existing references | Research pack folder, moved references, research README, parent README | VAL-SPC-001, VAL-SPC-002 | `git mv` preserves history; stale flat links are updated or recorded |
| WER-003 | Refresh workspace governance baseline | `workspace-governance-baseline.md` | VAL-SPC-003, VAL-SPC-004 | Purpose, roles, contracts, templates, scripts, integration, governance, and rules covered |
| WER-004 | Refresh harness, loop, and provider references | `m0002-harness-and-loop-engineering.md`, `m0003-provider-implementation-status.md` | VAL-SPC-004, VAL-SPC-005 | Harness/loop/provider claims cite checked official or primary sources |
| WER-005 | Refresh SDLC/CI/QA/formatting and add automation reference | `spec-sdlc-ci-qa-formatting.md`, `automation-pipeline-workflow-qa.md` | VAL-SPC-004, VAL-SPC-005 | Spec, SDLC, CI/CD, QA, formatting, linting, syntax, automation, pipeline, workflow covered |
| WER-006 | Add Kubernetes, infrastructure, and security reference | `kubernetes-infrastructure-security.md` | VAL-SPC-004, VAL-SPC-005 | Kubernetes, infrastructure, GitOps, secrets, policy, supply-chain, security covered |
| WER-007 | Close indexes, task evidence, progress, and validation | Research indexes, task evidence, progress memory | VAL-SPC-002, VAL-SPC-006, VAL-SPC-007 | Required validation passes and limitations are recorded |

### Detailed Tasks

> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.

### Task 1: Task Evidence and Baseline Inventory

**Files:**

- Create: `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`
- Modify: `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/specs/task.template.md`
- Read: `docs/03.specs/0017-workspace-engineering-research-pack/spec.md`

- [ ] **Step 1: Confirm branch and clean state**

Run:

```bash
git status --short --branch
```

Expected: branch is `codex/workspace-engineering-research-pack` and the
worktree is clean after this plan commit.

- [ ] **Step 2: Read the task template and parent spec**

Run:

```bash
sed -n '1,220p' docs/99.templates/templates/specs/task.template.md
sed -n '1,420p' docs/03.specs/0017-workspace-engineering-research-pack/spec.md
```

Expected: task template and Spec requirements are visible.

- [ ] **Step 3: Capture current research inventory**

Run:

```bash
rg --files docs/90.references/research docs/90.references docs/03.specs docs/03.specs | sort
```

Expected: output includes current flat research files, the new Spec, and Stage
04 indexes.

- [ ] **Step 4: Capture current links to flat research references**

Run:

```bash
rg -n "docs/90.references/research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|\\./(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: output lists links that must be updated after the move.

- [ ] **Step 5: Capture repo-first evidence categories**

Run:

```bash
rg -n "purpose|role|CI/CD|QA|Formatting|Linting|Automation|pipeline|workflow|operating contract|template|script|integration|SDLC|governance|Kubernetes|Infrastructure|Security|secret|policy" AGENTS.md CLAUDE.md GEMINI.md README.md .github docs/00.agent-governance docs/90.references docs/99.templates scripts tests gitops infrastructure policy traefik -g '*.md' -g '*.sh' -g '*.yml' -g '*.yaml'
```

Expected: output provides repo-backed evidence candidates for later references.

- [ ] **Step 6: Create task record**

Create `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`
from the task template with:

```yaml
title: 'Workspace Engineering Research Pack Task Record'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-04
```

Include task IDs `WER-001` through `WER-007`, parent plan link
`../plans/2026-07-04-workspace-engineering-research-pack.md`, and parent spec
link `../../03.specs/0017-workspace-engineering-research-pack/spec.md`.

- [ ] **Step 7: Update task README**

Add this row to `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`:

```markdown
| [`./2026-07-04-workspace-engineering-research-pack.md`](plan.md) | Workspace engineering research pack evidence for dated Stage 90 research references, existing reference moves, external-source refresh, Kubernetes/infrastructure/security, automation/pipeline/workflow/QA, and validation closure. | Draft | 2026-07-04 |
```

- [ ] **Step 8: Update progress ledger**

Add a progress entry titled
`2026-07-04 - Workspace engineering research pack WER-001 baseline` with:

- status complete for WER-001,
- baseline inventory commands from Steps 3 through 5,
- note that no live or external mutation was performed.

- [ ] **Step 9: Validate and commit WER-001**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(task): Track workspace engineering research pack"
```

Expected: diff check and repo quality pass; one task evidence commit is
created.

### Task 2: Dated Pack Scaffold and Existing Reference Move

**Files:**

- Create: `docs/90.references/research/2026-07-04-wer/README.md`
- Move: four current flat research references into the dated pack folder
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/README.md`
- Modify: task record and progress memory

- [ ] **Step 1: Create dated pack folder**

Run:

```bash
mkdir -p docs/90.references/research/2026-07-04-wer
```

Expected: folder exists.

- [ ] **Step 2: Move existing references with `git mv`**

Run:

```bash
git mv docs/90.references/research/workspace-governance-baseline.md docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md
git mv docs/90.references/research/m0002-harness-and-loop-engineering.md docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md
git mv docs/90.references/research/m0003-provider-implementation-status.md docs/90.references/research/2026-07-04-wer/provider-implementation-status.md
git mv docs/90.references/research/spec-sdlc-ci-qa-formatting.md docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md
```

Expected: `git status --short` shows four renames.

- [ ] **Step 3: Create dated pack README**

Create `docs/90.references/research/2026-07-04-wer/README.md`
with these sections: `# Workspace Engineering Research Pack`,
`## Overview`, `## Audience`, `## Scope`, `## Structure`,
`## Source Priority`, `## How to Work in This Pack`, `## Link Basis`,
`## Pack Index`, `## Authority Boundary`, `## Review and Freshness`, and
`## Related Documents`.

The `Pack Index` must list all six reference files and mark the two new files
as planned until created in Tasks 5 and 6.

- [ ] **Step 4: Update root research README**

Update `docs/90.references/research/README.md` so:

- the structure block shows the dated pack folder,
- the research index has a dated pack row,
- moved references point to
  `./2026-07-04-wer/<filename>.md`,
- flat reference rows are not presented as current top-level files.

- [ ] **Step 5: Update parent reference README**

Update `docs/90.references/README.md` so the research folder role mentions the
dated workspace engineering research pack.

- [ ] **Step 6: Run stale flat-link scan**

Run:

```bash
rg -n "docs/90.references/research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|\\./(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: no stale current links remain outside historical plan/task evidence.
Historical evidence may remain only if clearly describing past execution.

- [ ] **Step 7: Update task evidence and progress**

Mark `WER-002` done in the task record and append progress evidence with the
move list and stale-link scan result.

- [ ] **Step 8: Validate and commit WER-002**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research docs/90.references/README.md docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Scaffold workspace engineering research pack"
```

Expected: validation passes and the commit contains moved references, pack
README, index updates, and WER-002 evidence.

### Task 3: Workspace Governance Baseline Refresh

**Files:**

- Modify: `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md`
- Modify: task record and progress memory

- [ ] **Step 1: Inspect repo baseline sources**

Run:

```bash
rg -n "purpose|role|operating contract|template|script|integration|SDLC|governance|rule|CI/CD|QA|Formatting|Linting|Automation|Security" AGENTS.md CLAUDE.md GEMINI.md README.md docs/00.agent-governance docs/99.templates scripts tests .github -g '*.md' -g '*.sh' -g '*.yml' -g '*.yaml'
```

Expected: output identifies repo-backed baseline evidence.

- [ ] **Step 2: Refresh document metadata and scope**

Update frontmatter to `updated: 2026-07-04`. In `Reference Type`, set:

- `Source checked: 2026-07-04`
- refresh trigger covering governance, CI, scripts, templates, provider
  adapters, security, or research pack structure changes.

- [ ] **Step 3: Update definitions and facts**

Ensure `Definitions / Facts` contains explicit subsections for:

- workspace purpose and operating model,
- roles and provider adapters,
- CI/CD and QA evidence lanes,
- formatting, linting, and syntax validation,
- automation, pipeline, and workflow,
- templates and integration guides,
- scripts and validation,
- operating contract and approval boundaries,
- SDLC position,
- governance system and rules,
- security boundary.

- [ ] **Step 4: Add implementation checklist**

Add or refresh an `Implementation checklist` subsection that routes follow-up
actions to canonical owners: Stage 00, Stage 03, Stage 04, Stage 05,
`.github`, `scripts`, `docs/99.templates`, and `docs/90.references`.

- [ ] **Step 5: Validate reference format**

Run:

```bash
rg -n "^## (Overview|Purpose|Reference Type|Authority Boundary|Scope|Definitions / Facts|Sources|Review and Freshness|Related Documents)$" docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md
```

Expected: all required headings are present.

- [ ] **Step 6: Update task evidence and progress**

Mark `WER-003` done and record the baseline source scan plus heading scan.

- [ ] **Step 7: Validate and commit WER-003**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Refresh workspace governance baseline"
```

Expected: validation passes and the commit contains only the baseline
reference plus evidence updates.

### Task 4: Harness, Loop, and Provider Source Refresh

**Files:**

- Modify: `docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md`
- Modify: task record and progress memory

- [ ] **Step 1: Verify official provider and loop sources with web research**

Browse current official or primary sources for OpenAI/Codex, Anthropic Claude
Code, Google Gemini/ADK, and MCP. Record checked source URLs in task evidence.

Expected: sources are current enough to support 2026-07-04 source checked
metadata.

- [ ] **Step 2: Refresh harness and loop document**

Update `m0002-harness-and-loop-engineering.md` so it covers:

- harness engineering elements,
- loop engineering elements,
- workspace application requirements,
- required environment/rule/system elements,
- market scan section labeled non-authoritative,
- implementation checklist.

Use the source checked date `2026-07-04`.

- [ ] **Step 3: Refresh provider implementation status document**

Update `m0003-provider-implementation-status.md` so it covers:

- Claude harness and loop implementation status,
- Codex harness and loop implementation status,
- Gemini harness and loop implementation status,
- common environment/rules/system construction,
- upstream capability versus repo implementation status,
- unknowns and limitations where official sources do not prove parity.

Use the source checked date `2026-07-04`.

- [ ] **Step 4: Validate provider names and source boundaries**

Run:

```bash
rg -n "Claude|Codex|Gemini|OpenAI|Anthropic|Google|ADK|MCP|non-authoritative|Source checked: 2026-07-04|Review and Freshness" docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md docs/90.references/research/2026-07-04-wer/provider-implementation-status.md
```

Expected: output shows provider coverage, source checked metadata, and market
scan boundary wording where market scan is used.

- [ ] **Step 5: Update task evidence and progress**

Mark `WER-004` done and record web source groups, limitations, and validation
scan output.

- [ ] **Step 6: Validate and commit WER-004**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md docs/90.references/research/2026-07-04-wer/provider-implementation-status.md docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Refresh harness loop and provider sources"
```

Expected: validation passes and the commit contains two research references
plus evidence updates.

### Task 5: SDLC, CI, QA, Formatting, Automation, Pipeline, and Workflow

**Files:**

- Modify: `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md`
- Create: `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md`
- Modify: dated pack README
- Modify: task record and progress memory

- [ ] **Step 1: Verify official SDLC, CI, QA, formatting, and automation sources**

Browse current official or primary sources for GitHub Actions, GitHub Actions
security hardening, GitHub code security, GitHub Spec Kit, NIST SSDF, NIST
SP 800-204D, pre-commit, CommonMark, YAML, OpenSSF, and SLSA.

Expected: checked sources support current CI/CD, QA, formatting, linting,
syntax validation, and secure SDLC statements.

- [ ] **Step 2: Refresh SDLC/CI/QA/formatting reference**

Update `spec-sdlc-ci-qa-formatting.md` so it covers:

- spec-driven development,
- SDLC and secure SDLC,
- CI/CD,
- QA evidence lanes,
- formatting,
- linting,
- syntax validation,
- repo-local validation command mapping,
- source checked date `2026-07-04`.

- [ ] **Step 3: Create automation/pipeline/workflow/QA reference**

Create `automation-pipeline-workflow-qa.md` from
`docs/99.templates/templates/references/reference.template.md` with:

```yaml
title: 'Reference: Automation Pipeline Workflow QA Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-04
```

Required `Definitions / Facts` subsections:

- automation boundaries,
- pipeline model,
- workflow model,
- CI job graph and evidence,
- QA lanes,
- formatting/linting/syntax integration,
- validation-loop checklist,
- non-authoritative market scan.

- [ ] **Step 4: Update dated pack README**

Change `automation-pipeline-workflow-qa.md` from planned to current in the
pack index.

- [ ] **Step 5: Validate topic coverage**

Run:

```bash
rg -n "spec-driven|SDLC|CI/CD|QA|formatting|linting|syntax|Automation|pipeline|workflow|non-authoritative|Source checked: 2026-07-04|Review and Freshness" docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md
```

Expected: output shows all required topic terms and source/freshness metadata.

- [ ] **Step 6: Update task evidence and progress**

Mark `WER-005` done and record source groups, coverage scan, and limitations.

- [ ] **Step 7: Validate and commit WER-005**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md docs/90.references/research/2026-07-04-wer/README.md docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Refresh delivery automation and QA sources"
```

Expected: validation passes and the commit contains SDLC/QA refresh,
automation reference, README index update, and evidence updates.

### Task 6: Kubernetes, Infrastructure, and Security Reference

**Files:**

- Create: `docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md`
- Modify: dated pack README
- Modify: task record and progress memory

- [ ] **Step 1: Verify official Kubernetes, infrastructure, and security sources**

Browse current official or primary sources for Kubernetes concepts, Secrets,
Kustomize, OpenGitOps, Argo CD, Argo Rollouts, External Secrets Operator, OPA,
Conftest, NIST SSDF, NIST SP 800-204D, GitHub Actions security hardening,
OpenSSF, and SLSA.

Expected: checked sources support Kubernetes, infrastructure, GitOps, secrets,
policy-as-code, supply-chain, and security statements.

- [ ] **Step 2: Create Kubernetes/infrastructure/security reference**

Create `kubernetes-infrastructure-security.md` from
`docs/99.templates/templates/references/reference.template.md` with:

```yaml
title: 'Reference: Kubernetes Infrastructure Security Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-04
```

Required `Definitions / Facts` subsections:

- Kubernetes baseline,
- Infrastructure and GitOps baseline,
- Secrets and External Secrets boundary,
- Policy-as-code and admission/static validation,
- Supply-chain and CI security,
- Workspace application requirements,
- Implementation checklist,
- non-authoritative market scan.

- [ ] **Step 3: Update dated pack README**

Change `kubernetes-infrastructure-security.md` from planned to current in the
pack index.

- [ ] **Step 4: Validate topic coverage**

Run:

```bash
rg -n "Kubernetes|Infrastructure|GitOps|Secret|External Secrets|policy-as-code|OPA|Conftest|supply-chain|security|SLSA|OpenSSF|non-authoritative|Source checked: 2026-07-04|Review and Freshness" docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md
```

Expected: output shows all required topic terms and source/freshness metadata.

- [ ] **Step 5: Update task evidence and progress**

Mark `WER-006` done and record source groups, coverage scan, and limitations.

- [ ] **Step 6: Validate and commit WER-006**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md docs/90.references/research/2026-07-04-wer/README.md docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Add Kubernetes infrastructure security sources"
```

Expected: validation passes and the commit contains the new reference, pack
README update, and evidence updates.

### Task 7: Final Index, Evidence, and Validation Closure

**Files:**

- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/README.md`
- Modify: `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
- Modify: `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
- Modify: `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`
- Modify: `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Run required validation**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: diff check prints no output and repo quality prints
`[PASS] repository quality gates passed`.

- [ ] **Step 2: Run full harness**

Run:

```bash
bash scripts/validate-harness.sh
```

Expected: command ends with `PASS harness repo-static validation`. Optional
`kube-linter` or `conftest` absence may be reported as SKIP/fallback evidence.

- [ ] **Step 3: Run focused final scans**

Run:

```bash
rg -n "docs/90.references/research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|\\./(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "Source checked: 2026-07-04|Review and Freshness|non-authoritative|Authority Boundary" docs/90.references/research/2026-07-04-wer
rg -n "Kubernetes|Infrastructure|Security|Automation|pipeline|workflow|QA|formatting|linting|syntax" docs/90.references/research/2026-07-04-wer
```

Expected: stale flat-link scan has no current-path matches outside historical
evidence; source/freshness and topic scans show required coverage.

- [ ] **Step 4: Close plan and task statuses**

Update:

- this plan frontmatter `status: done`,
- `docs/03.specs/0017-workspace-engineering-research-pack/plan.md` row to `Done`,
- task record frontmatter `status: done`,
- `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records` row to `Done`,
- task record `WER-007` status to `Done` with final validation evidence.

- [ ] **Step 5: Update progress ledger**

Append final progress evidence with:

- validation commands and results,
- optional-tool SKIP/fallback notes,
- external-source read-only boundary,
- no live or third-party mutation statement.

- [ ] **Step 6: Validate and commit WER-007**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/README.md docs/90.references/README.md docs/03.specs/0017-workspace-engineering-research-pack/plan.md docs/03.specs/0017-workspace-engineering-research-pack/plan.md docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(validation): Close workspace engineering research pack"
```

Expected: final closure commit exists and no unresolved drift remains.

### Legacy Task supplemental evidence

### Phase View

### WER-001 Baseline

- [x] Confirmed branch with `git status --short --branch`: current branch is
      `codex/workspace-engineering-research-pack`; no short-status entries were
      present at intake.
- [x] Read the task template and parent Spec.
- [x] Captured current research inventory.
- [x] Captured current links to flat research references.
- [x] Captured repo-first evidence categories for later reference refresh
      tasks.
- [x] Created this task record, updated the task index, and updated the
      progress ledger.
- [x] Ran required repo-static validation and committed WER-001 evidence.

### Remaining Research Pack Work

- [x] WER-002 move/scaffold commit.
- [x] WER-003 workspace governance baseline refresh.
- [x] WER-004 harness, loop, and provider reference refresh.
- [x] WER-005 SDLC/CI/QA/formatting/security reference refresh.
- [x] WER-006 Kubernetes, infrastructure, and security reference.
- [x] WER-007 automation, pipeline, workflow, QA reference plus final index,
      evidence, progress, and validation closure.
- [x] WER-008 AI agents roster and gap-analysis reference plus index closure,
      progress ledger entry, validation, and human-approved push.

### Baseline Evidence Summary

### Branch and Template Intake

| Evidence                                                        | Result                                                                                                                                             |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `git status --short --branch`                                   | `## codex/workspace-engineering-research-pack`; worktree clean at intake.                                                                          |
| `docs/99.templates/templates/specs/task.template.md`   | Read; task documents are traceability-first, English, and require validation evidence.                                                             |
| `docs/03.specs/0017-workspace-engineering-research-pack/spec.md` | Read; confirms documentation-only pack, dated research folder, source-priority rules, validation criteria, and no live/external mutation boundary. |

### Research Inventory

Command:

```bash
rg --files docs/90.references/research docs/90.references docs/03.specs docs/03.specs | sort
```

Summary:

- Captured 108 output rows and 103 unique paths.
- Duplicate rows are expected because `docs/90.references/research` is nested
  under `docs/90.references` and both roots were scanned.
- Current flat research references are present at:
  - `docs/90.references/research/workspace-governance-baseline.md`
  - `docs/90.references/research/m0002-harness-and-loop-engineering.md`
  - `docs/90.references/research/m0003-provider-implementation-status.md`
  - `docs/90.references/research/spec-sdlc-ci-qa-formatting.md`
- The new parent Spec and Plan are present:
  - `docs/03.specs/0017-workspace-engineering-research-pack/spec.md`
  - `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`

### Flat Research Reference Links

Command:

```bash
rg -n "docs/90.references/research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|\\./(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Summary:

- Captured 71 current references to the four flat research files.
- Highest-count current link owners:
  - `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
    with 16 matches.
  - `docs/90.references/audits/2026-07-02-provider-harness-loop-implementation-audit.md`
    with 9 matches.
  - `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
    with 8 matches.
  - `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
    with 8 matches.
  - `docs/90.references/audits/2026-07-02-sdlc-delivery-practices-implementation-audit.md`
    with 7 matches.
- Current research README and cross-reference links inside the four flat
  references are included and must be updated or intentionally preserved as
  historical evidence during WER-002 and later tasks.

### Repo-First Evidence Categories

Command:

```bash
rg -n "purpose|role|CI/CD|QA|Formatting|Linting|Automation|pipeline|workflow|operating contract|template|script|integration|SDLC|governance|Kubernetes|Infrastructure|Security|secret|policy" AGENTS.md CLAUDE.md GEMINI.md README.md .github docs/00.agent-governance docs/90.references docs/99.templates scripts tests gitops infrastructure policy traefik -g '*.md' -g '*.sh' -g '*.yml' -g '*.yaml'
```

Summary:

- Captured 4,838 repo-first evidence lines for later reference refresh tasks.
- Top evidence buckets by normalized owner:
  - `docs/00.agent-governance`: 2,265 matches.
  - `scripts`: 949 matches.
  - `docs/90.references`: 764 matches.
  - `docs/99.templates`: 437 matches.
  - `gitops`: 158 matches.
  - `infrastructure`: 109 matches.
  - `.github`: 78 matches.
  - `README.md`: 36 matches.
  - `tests`: 15 matches.
  - Gateway files: `AGENTS.md` 8, `GEMINI.md` 7, `CLAUDE.md` 7.
- Top individual files include
  `docs/00.agent-governance/memory/progress.md`,
  `scripts/validate-repo-quality-gates.sh`,
  `docs/00.agent-governance/harness-catalog.md`,
  `docs/90.references/research/spec-sdlc-ci-qa-formatting.md`,
  `docs/99.templates/README.md`, existing Stage 90 audits, the four flat
  research references, `scripts/README.md`,
  `docs/99.templates/README.md`, `gitops/README.md`,
  `infrastructure/README.md`, and repo-static validation scripts.

### WER-002 Evidence Summary

### Dated Pack Scaffold

- Created
  `docs/90.references/research/2026-07-04-wer/README.md`
  with the required sections:
  `Overview`, `Audience`, `Scope`, `Structure`, `Source Priority`,
  `How to Work in This Pack`, `Link Basis`, `Pack Index`,
  `Authority Boundary`, `Review and Freshness`, and `Related Documents`.
- The Pack Index lists all six approved references:
  - Current: `workspace-governance-baseline.md`
  - Current: `m0002-harness-and-loop-engineering.md`
  - Current: `m0003-provider-implementation-status.md`
  - Current: `spec-sdlc-ci-qa-formatting.md`
  - Planned: `kubernetes-infrastructure-security.md`
  - Planned: `automation-pipeline-workflow-qa.md`

### Move List

Moved with `git mv`:

| Source                                                          | Destination                                                                    |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `docs/90.references/research/workspace-governance-baseline.md`  | `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md`  |
| `docs/90.references/research/m0002-harness-and-loop-engineering.md`   | `docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md`   |
| `docs/90.references/research/m0003-provider-implementation-status.md` | `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md` |
| `docs/90.references/research/spec-sdlc-ci-qa-formatting.md`     | `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md`     |

### Index Updates

- Updated `docs/90.references/research/README.md` so the structure block shows
  the dated pack folder.
- Added the dated pack row to the research index.
- Updated current moved-reference rows to point to
  `./2026-07-04-wer/<filename>.md`.
- Added the two planned reference slots as code literals until their files are
  created by later WER tasks.
- Updated `docs/90.references/README.md` so the research folder role mentions
  the dated workspace engineering research pack.

### Stale Flat-Link Scan

Command:

```bash
rg -n "docs/90.references/research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md|\\./(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Summary:

- Current research indexes and the moved dated pack do not present the former
  flat reference paths as current top-level files.
- Broken Markdown links in current Stage 03, Stage 05, and Stage 90 audit
  consumers were repaired to point at the dated pack.
- Remaining matches are historical command strings, creation evidence, move
  evidence, or old plan/task path literals that describe past execution.

### WER-003 Evidence Summary

### Workspace Governance Baseline Refresh

- Refreshed
  `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md`
  as a dated, descriptive Stage 90 reference.
- Updated frontmatter `updated: 2026-07-04`, `Source checked:
2026-07-04`, and freshness trigger language for governance, CI/CD, scripts,
  templates, provider adapters, security, and research pack structure changes.
- Preserved the authority boundary: the reference summarizes canonical owners
  and does not redefine active governance policy, CI semantics, provider
  runtime permissions, approval boundaries, runbooks, live checks, or secret
  handling.
- Refreshed `Definitions / Facts` coverage for workspace purpose and operating
  model, roles and provider adapters, CI/CD and QA evidence lanes, formatting,
  linting, syntax validation, automation, pipeline, workflow, templates,
  integration guides, scripts, operating contract, SDLC position, governance
  rules, and security boundary.
- Added an owner-routed `Implementation checklist` for Stage 00, Stage 03,
  Stage 04, Stage 05, `.github`, `scripts`, `docs/99.templates`, and
  `docs/90.references`.

### Repo Baseline Source Scan

Command:

```bash
rg -n "purpose|role|operating contract|template|script|integration|SDLC|governance|rule|CI/CD|QA|Formatting|Linting|Automation|Security" AGENTS.md CLAUDE.md GEMINI.md README.md docs/00.agent-governance docs/99.templates scripts tests .github -g '*.md' -g '*.sh' -g '*.yml' -g '*.yaml'
```

Summary:

- PASS; command completed successfully.
- Terminal output was large and truncated for display after 3,208 returned
  lines / 119,880 original tokens.
- Follow-up focused inspection covered the root gateway files, root README,
  `.codex/CODEX.md`, provider notes, bootstrap and approval-boundary rules,
  quality standards, harness catalog, harness implementation map, template
  routing, scripts inventory, GitHub CI workflow, CI/CD QA guide, and the dated
  research pack README.

### Required Heading Scan

Command:

```bash
rg -n "^## (Overview|Purpose|Reference Type|Authority Boundary|Scope|Definitions / Facts|Sources|Review and Freshness|Related Documents)$" docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md
```

Summary:

- PASS; found all required top-level reference headings:
  `Overview`, `Purpose`, `Reference Type`, `Authority Boundary`, `Scope`,
  `Definitions / Facts`, `Sources`, `Review and Freshness`, and
  `Related Documents`.

### WER-004 Evidence Summary

### Harness, Loop, and Provider Reference Refresh

- Refreshed
  `docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md`
  with `updated: 2026-07-04`, `Source checked: 2026-07-04`, provider
  agent-loop docs freshness triggers, workspace requirements, environment/rule
  implications, MCP/tool boundaries, the non-authoritative market scan label,
  and the implementation checklist routed to the current WER task.
- Refreshed
  `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md`
  with `updated: 2026-07-04`, `Source checked: 2026-07-04`, upstream
  capability versus repo implementation status, common environment/rule/system
  construction, provider-specific implementation status, and explicit unknowns
  where official sources do not prove parity.
- Preserved authority boundaries: these references remain descriptive Stage 90
  material and do not redefine active governance, provider runtime
  permissions, hook enforcement, CI semantics, subagent dispatch procedure, or
  live operations.

### Official and Primary Source Groups Checked

- OpenAI/Codex: Codex docs home, CLI, config reference, agent approvals and
  security, sandboxing, MCP, subagents, hooks, skills, rules, OpenAI harness
  engineering article, and OpenAI Codex agent-loop article.
- Anthropic Claude Code: settings, hooks, subagents, skills, and MCP.
- Google/Gemini/ADK: Gemini CLI repository, Gemini CLI docs tree, Google Cloud
  ADK page, and ADK site.
- MCP: Model Context Protocol 2025-06-18 specification and MCP Security Best
  Practices.
- Repo-backed sources: Stage 00 harness catalog, harness implementation map,
  provider notes, runtime baselines, hook wiring, reference template, research
  README, and this task record.

### Limitations

- Gemini Code Assist is retained as a freshness trigger, but the WER-004
  required source group did not include Code Assist agent-mode pages; no fresh
  Code Assist parity claim is made.
- Gemini CLI native hook/permission parity with Claude Code was not verified
  from the required official sources.
- Codex rules remain an upstream capability marked experimental in the checked
  official docs; repo-local `.codex/hooks.json` remains context/validation
  wiring, not a Claude-style permission gate.
- `.codex/config.toml` is an upstream/trusted-project capability, but no
  tracked `.codex/config.toml` exists in this checkout.
- Static validation is repo correctness evidence only and does not prove live
  Kubernetes, Vault, cloud, provider runtime, secret, or deployment readiness.

### WER-004 Validation Scan

Command:

```bash
rg -n "Claude|Codex|Gemini|OpenAI|Anthropic|Google|ADK|MCP|non-authoritative|Source checked: 2026-07-04|Review and Freshness" docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md docs/90.references/research/2026-07-04-wer/provider-implementation-status.md
```

Summary:

- PASS; command completed successfully.
- The scan returned 214 matching lines. This is keyword-presence evidence that
  both refreshed references mention `Source checked: 2026-07-04`,
  `Review and Freshness`, official provider source groups, MCP,
  Google/ADK, `non-authoritative` market-scan language, and
  provider-specific boundary wording.
- Source support and claim correctness were reviewed separately by reading the
  refreshed references and checking the cited official/primary source set; the
  `rg` scan alone does not prove source freshness, link reachability, or claim
  support.

### WER-005 Evidence Summary

### SDLC CI QA Formatting Security Reference Refresh

- Refreshed
  `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md`
  with `updated: 2026-07-05` and `Source checked: 2026-07-05` for WER-005
  refreshed sources.
- Preserved the reference as descriptive Stage 90 material. It does not define
  active policy for GitHub Actions, pre-commit, CodeQL/code scanning,
  Dependency Review, SLSA provenance/attestation, OpenSSF Scorecard, live
  runtime checks, release approval, or secret handling.
- Refreshed official/primary source coverage for GitHub Actions workflow
  syntax, GitHub Actions secure use, GitHub Code scanning/CodeQL concepts,
  GitHub Dependency Review, GitHub Spec Kit, NIST SSDF SP 800-218, NIST
  SP 800-204D, SLSA spec v1.2, OpenSSF Scorecard, Prettier, EditorConfig,
  CommonMark 0.31.2, YAML 1.2.2, markdownlint, and pre-commit. SLSA v1.1 was
  checked as a retired historical page only.
- Added security and supply-chain findings for least-privilege workflow
  permissions, the GitHub Actions secrets boundary, Dependency Review,
  CodeQL/code scanning, SLSA provenance/attestation, and OpenSSF Scorecard
  context.
- Kept repo-static, CI/toolchain, artifact attestation, non-authoritative
  market/context scan, and live-runtime evidence lanes separate.
- Updated implementation checklist routing for GitHub Actions permissions,
  secrets, CodeQL/code scanning, Dependency Review, SLSA provenance,
  OpenSSF Scorecard, Prettier, EditorConfig, CommonMark, YAML 1.2.2,
  markdownlint, pre-commit, scripts, Stage 00 governance, and Stage 04 task
  evidence.

### WER-005 Validation Scan

Command:

```bash
rg -n "Source checked: 2026-07-05|GitHub Actions|NIST|SSDF|SLSA|OpenSSF|CodeQL|Dependency Review|Prettier|EditorConfig|CommonMark|YAML 1.2.2|pre-commit|non-authoritative|Review and Freshness" docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md
```

Summary:

- PASS; command completed successfully.
- The scan returned matching lines for the WER-005 source-checked date,
  official/primary source families, formatting references, supply-chain
  findings, non-authoritative market/context language, and
  `Review and Freshness`.

### WER-006 Evidence Summary

### Kubernetes Infrastructure Security Reference

- Added
  `docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md`
  with `updated: 2026-07-05`, `Source checked: 2026-07-05`, and
  `Review and Freshness` metadata for WER-006 source checks.
- Preserved the reference as descriptive Stage 90 material. It does not define
  active Kubernetes policy, GitOps policy, Argo CD sync procedure, Argo
  Rollouts operation, External Secrets Operator procedure, Vault procedure,
  NetworkPolicy procedure, RBAC procedure, live checks, release approval, or
  secret handling.
- Checked official/primary source coverage for Kubernetes Secrets,
  Kubernetes NetworkPolicies, Kubernetes RBAC, Kubernetes
  Kustomize/declarative management, OpenGitOps, Argo CD docs, Argo CD
  declarative setup, Argo CD best practices, Argo Rollouts, External Secrets
  Operator, ESO Vault provider, OPA Kubernetes admission, Conftest, HashiCorp
  Vault policies, Vault Kubernetes auth, NIST SP 800-204D, and OpenSSF
  Scorecard.
- Added repo implementation comparison for desired-state surfaces, AppProject
  allow-list boundaries, namespace ownership, image policy, ESO/Vault
  boundaries, NetworkPolicy coverage, infrastructure static/live test
  boundaries, and policy-as-code evidence.
- Kept repo-static, CI/toolchain, and live-runtime evidence lanes separate.
- Updated the dated pack README and parent research README so
  `kubernetes-infrastructure-security.md` is current while
  `automation-pipeline-workflow-qa.md` remains planned for WER-007.

### WER-006 Validation Scan

Command:

```bash
rg -n "Source checked: 2026-07-05|Kubernetes|GitOps|Argo CD|Argo Rollouts|External Secrets Operator|Vault|NetworkPolicy|RBAC|Kustomize|OPA|Conftest|NIST|OpenSSF|repo-static|live-runtime|non-authoritative|Review and Freshness" docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md
```

Summary:

- PASS; command completed successfully.
- The scan returned matching lines for the WER-006 source-checked date,
  required Kubernetes/GitOps/security source families, repo-static and
  live-runtime evidence-lane language, non-authoritative market/context
  language, and `Review and Freshness`.

### WER-007 Evidence Summary

### Automation Pipeline Workflow QA Reference

- Added
  `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md`
  with `updated: 2026-07-05`, `Source checked: 2026-07-05`, and
  `Review and Freshness` metadata for WER-007 source checks.
- Preserved the reference as descriptive Stage 90 material. It does not define
  active GitHub Actions semantics, branch protection, workflow permissions,
  release approval, dependency-update policy, maintenance-bot policy,
  deployment procedure, live checks, or secret handling.
- Checked official/primary source coverage for GitHub Actions workflow syntax,
  events, concurrency, reusable workflows, workflow commands, `GITHUB_TOKEN`,
  secrets, workflow artifacts, dependency caching, workflow visualization graph,
  secure use, Martin Fowler Continuous Integration, DORA metrics, pre-commit,
  and OpenSSF Scorecard context.
- Added repo implementation comparison for `.github/workflows/ci.yml`,
  `generate-changelog.yml`, maintenance workflows, Dependabot, Zizmor,
  pre-commit, path filtering, branch policy, permissions, checkout credential
  handling, artifacts, cache, reusable workflow status, and QA evidence lanes.
- Kept repo-static, CI/toolchain, artifact/release, maintenance automation,
  market/context, and live-runtime evidence lanes separate.
- Updated the dated pack README and parent research README so
  `automation-pipeline-workflow-qa.md` is current and the research pack has no
  planned target literals.

### WER-007 Validation Scan

Command:

```bash
rg -n "Source checked: 2026-07-05|GitHub Actions|workflow|pipeline|automation|CI/CD|QA|pre-commit|DORA|Martin Fowler|artifact|cache|GITHUB_TOKEN|concurrency|repo-static|CI/toolchain|live-runtime|non-authoritative|Review and Freshness" docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md
```

Summary:

- PASS; command completed successfully.
- The scan returned matching lines for the WER-007 source-checked date,
  required workflow/automation/QA source families, artifact/cache/token
  concepts, repo-static and CI/toolchain evidence-lane language,
  live-runtime boundary language, non-authoritative market/context language,
  and `Review and Freshness`.

### Reference Closure Scan

Command:

```bash
rg -n "automation-pipeline-workflow-qa.md[[:space:]]+# P[l]anned|P[l]anned descriptive reference" docs/90.references/research/2026-07-04-wer/README.md docs/90.references/research/README.md
```

Summary:

- PASS; no matches after WER-007 index closure.
- WER-007 task table status and phase-view checkbox were updated to `Done`
  and checked, respectively.

### WER-008 Evidence Summary

### AI Agents Roster and Gap Analysis Reference

- Added
  `docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md`
  with `updated: 2026-07-06`, `Source checked: 2026-07-06`, and
  `Review and Freshness` metadata.
- Recorded the repo-backed workspace agent roster (8 agents, two-tier model
  policy, triple provider adapters) and the local agent-file contract from
  `docs/00.agent-governance/harness-catalog.md`,
  `docs/00.agent-governance/model-policy.md`, and `.claude/agents/`.
- Captured a dated, non-authoritative market scan of the external
  `msitarzewski/agency-agents` catalog (17 divisions, 230+ persona agents,
  no `model`/`tools` contract) via read-only GitHub API and raw file fetches.
- Added an agent-file contract comparison and an adopt/adapt/skip gap
  analysis, routing all addition candidates through Stage 03 specs first.
- Updated the dated pack README and parent research README index tables and
  structure trees, and refreshed pack `Last reviewed` to 2026-07-06.

### WER-008 Push Boundary Exception

- WER working rules default to no push. For WER-008 the human operator
  explicitly approved pushing this documentation change to the GitHub remote.
- Push scope is limited to committed Stage 04 task, Stage 90 reference, and
  Stage 00 progress documentation. No live Kubernetes, Argo CD, Vault, cloud,
  provider runtime, credential, secret-value, paid-job, publishing, or merge
  action was performed.
## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WER-001 | Structural | Diff hygiene | `git diff --check` | No output |
| VAL-WER-002 | Repository | Repository quality gate | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed` |
| VAL-WER-003 | Harness | Full repo-static harness | `bash scripts/validate-harness.sh` | Ends with `PASS harness repo-static validation` |
| VAL-WER-004 | Links | Flat research stale-link scan | Focused `rg` command in Task 7 Step 3 | No current stale flat links outside historical evidence |
| VAL-WER-005 | Source boundary | Source/freshness scan | Focused `rg` command in Task 7 Step 3 | Source checked, freshness, non-authoritative, and authority boundary terms are present |
| VAL-WER-006 | Topic coverage | Required topic scan | Focused `rg` command in Task 7 Step 3 | Required topics appear in the dated pack |

### Legacy Task verification evidence

| Date       | Scope                             | Command                                                                                                                                                                                                                          | Result                                                                                                                                                                            |
| ---------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-07-04 | WER-001 intake                    | `git status --short --branch`                                                                                                                                                                                                    | PASS; current branch is `codex/workspace-engineering-research-pack`; worktree clean at intake.                                                                                    |
| 2026-07-04 | WER-001 inventory                 | Baseline scan commands listed above                                                                                                                                                                                              | PASS; inventory, stale flat-link candidates, and repo-first evidence categories captured.                                                                                         |
| 2026-07-04 | WER-001 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-04 | WER-001 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |
| 2026-07-04 | WER-002 stale flat-link scan      | Focused `rg` scan listed in WER-002 evidence                                                                                                                                                                                     | PASS; current consumer broken links were repaired, and remaining matches are historical-only command/path evidence.                                                               |
| 2026-07-04 | WER-002 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-04 | WER-002 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |
| 2026-07-04 | WER-003 repo baseline source scan | Required WER-003 `rg` scan listed above                                                                                                                                                                                          | PASS; large output completed successfully and was summarized from focused canonical source inspection.                                                                            |
| 2026-07-04 | WER-003 required heading scan     | `rg -n "^## (Overview\|Purpose\|Reference Type\|Authority Boundary\|Scope\|Definitions / Facts\|Sources\|Review and Freshness\|Related Documents)$" docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | PASS; all required reference headings present.                                                                                                                                    |
| 2026-07-04 | WER-003 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-04 | WER-003 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |
| 2026-07-04 | WER-004 reference scan            | Required WER-004 `rg` scan listed above                                                                                                                                                                                          | PASS; 214 matching lines across the refreshed harness/loop and provider references.                                                                                               |
| 2026-07-04 | WER-004 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-04 | WER-004 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |
| 2026-07-05 | WER-005 reference scan            | Required WER-005 `rg` scan listed above                                                                                                                                                                                          | PASS; WER-005 refreshed source date, official source families, supply-chain terms, formatting terms, non-authoritative language, and freshness heading were present.              |
| 2026-07-05 | WER-005 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-05 | WER-005 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |
| 2026-07-05 | WER-006 reference scan            | Required WER-006 `rg` scan listed above                                                                                                                                                                                          | PASS; WER-006 source date, Kubernetes/GitOps/security terms, repo-static/live-runtime language, non-authoritative language, and freshness heading were present.                   |
| 2026-07-05 | WER-006 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-05 | WER-006 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |
| 2026-07-05 | WER-007 reference scan            | Required WER-007 `rg` scan listed above                                                                                                                                                                                          | PASS; WER-007 source date, workflow/automation/QA terms, artifact/cache/token concepts, evidence-lane language, non-authoritative language, and freshness heading were present.   |
| 2026-07-05 | WER-007 planned-reference closure | Focused planned-reference `rg` scan listed above                                                                                                                                                                                 | PASS; README index scan found no stale planned reference literals; WER-007 status was separately updated to Done.                                                                 |
| 2026-07-05 | WER-007 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-05 | WER-007 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |
| 2026-07-06 | Lifecycle drift closure           | S34-GAP-001 in `2026-07-06-stage03-04-repo-static-gap-closure.md`                                                                                                                                                                | PASS; existing WER task evidence already recorded WER-001 through WER-007 as Done, so frontmatter and README lifecycle status were aligned without changing live/runtime state.   |
| 2026-07-06 | WER-008 external source check     | Read-only GitHub API and raw file fetches for `msitarzewski/agency-agents`                                                                                                                                                       | PASS; repo metadata, `divisions.json`, engineering/security/testing/project-management listings, and a sample agent file were captured and labeled non-authoritative market scan. |
| 2026-07-06 | WER-008 formatting                | `git diff --check`                                                                                                                                                                                                               | PASS.                                                                                                                                                                             |
| 2026-07-06 | WER-008 repo quality              | `bash scripts/validate-repo-quality-gates.sh .`                                                                                                                                                                                  | PASS.                                                                                                                                                                             |

Tooling limitation:

- `rtk` is not on PATH in this shell. `/home/hy/.local/bin/rtk --version`
  reports `rtk 0.34.3`, but `/home/hy/.local/bin/rtk gain` cannot initialize
  its tracking database. Required commands were run directly and the limitation
  was recorded without inspecting private runtime state.

Boundary statement:

- WER-001 performed repository reads, documentation edits, local validation,
  local staging, and a local commit only.
- WER-002 performed repository reads, documentation edits, `git mv` file moves,
  local validation, local staging, and a local commit only.
- WER-003 performed repository reads, documentation edits, local validation,
  local staging, and a local commit only.
- WER-004 performed read-only official/primary web source checks, repository
  reads, documentation edits, and local validation only before commit.
- WER-005 performed read-only official/primary web source checks, repository
  reads, documentation edits, and local validation only before commit.
- WER-006 performed read-only official/primary web source checks, repository
  reads, documentation edits, and local validation only before commit.
- WER-007 performed read-only official/primary web source checks, repository
  reads, documentation edits, and local validation only before commit.
- WER-008 performed read-only external GitHub API and raw file source checks,
  repository reads, documentation edits, local validation, a local commit,
  and a human-approved documentation-branch push only.
- Except for the WER-008 human-approved documentation-branch push, no live
  Kubernetes, Argo CD, Vault, cloud, provider runtime, credential,
  secret-value, paid-job, publishing, merge, or third-party mutation was
  performed across WER-001 through WER-008.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Stale flat research links remain after the move | Medium | Run focused `rg` stale-link scans and update indexes in the move commit |
| Research documents become active policy | High | Keep authority boundaries explicit and route policy changes to canonical owners |
| Provider or tool claims drift from current docs | Medium | Use web research during implementation and record checked dates |
| Market scan becomes over-weighted | Medium | Label market scan non-authoritative and place it below official/repo-backed evidence |
| Scope grows beyond a compact pack | Medium | Keep the pack to one README, four moved references, and two new references |
| Optional tools are mistaken for full coverage | Medium | Preserve SKIP/fallback wording for optional `kube-linter` and `conftest` results |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Run repo-quality, focused stale-link scans, source
  boundary scans, topic scans, and full harness before closure.
- **Sandbox / Canary Rollout**: Not applicable. This is documentation-only
  reference work.
- **Human Approval Gate**: Required for live runtime validation, remote push,
  PR creation, merge, publishing, credential changes, paid jobs, third-party
  state changes, or changing active governance policy.
- **Rollback Trigger**: Any validation failure that cannot be fixed by
  aligning research references, indexes, or evidence records.
- **Prompt / Model Promotion Criteria**: Not applicable. No prompt or model
  runtime promotion is included.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `WER-001 through WER-008` is limited to these Workspace Engineering Research Pack Task Record owners and Task-Table surfaces:
  - `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`
  - `docs/03.specs/0017-workspace-engineering-research-pack/spec.md`
  - `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
  - `docs/99.templates/templates/specs/task.template.md`
  - `docs/90.references/research`
  - `docs/90.references`
  - `docs/90.references/research/workspace-governance-baseline.md`
  - `docs/90.references/research/m0002-harness-and-loop-engineering.md`
- **Forbidden Paths**: active policy or runtime configuration not named by the Workspace Engineering Research Pack Task Record Task Table, provider settings, secret values, local diagnostics, and remote publication surfaces.
- **Approval Required**: Human approval is required before publishing Workspace Engineering Research Pack Task Record research, changing active policy/runtime behavior, deleting evidence, contacting providers, push, merge, or corpus expansion.
- **Static Validation**: Preserve the Workspace Engineering Research Pack Task Record outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git status --short --branch`
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Live Validation**: DEFER — Workspace Engineering Research Pack Task Record is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Workspace Engineering Research Pack Task Record evidence must use public or repository-visible facts only; do not inspect or reproduce credentials, tokens, auth files, private logs, kubeconfigs, or shell history.
- **Rollback Plan**: Revert the logical Workspace Engineering Research Pack Task Record change set for `WER-001 through WER-008` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Workspace Engineering Research Pack Task Record evidence remains in:
  - `docs/03.specs/0017-workspace-engineering-research-pack/README.md#task-records`
  - `docs/03.specs/0017-workspace-engineering-research-pack/spec.md`
  - `docs/03.specs/0017-workspace-engineering-research-pack/plan.md`
  - `docs/99.templates/templates/specs/task.template.md`
## Completion Criteria

- [x] Dated research pack folder exists.
- [x] Four existing research references are moved into the dated pack.
- [x] Two new focused references exist.
- [x] Existing references are refreshed with 2026-07-04 source checked
  metadata where claims are updated.
- [x] Root and parent indexes route to the dated pack.
- [x] Stage 04 task evidence and progress memory are complete.
- [x] Required validation passes.
- [x] Logical-unit commits exist for each completed task.

## Traceability

- **Spec**: [Workspace Engineering Research Pack](spec.md)
- **Prior Research Spec**: [Workspace Harness Research Pack](../0009-workspace-harness-research-pack/spec.md)
- **Task**: [../tasks/2026-07-04-workspace-engineering-research-pack.md](plan.md)
- **Research README**: [../../90.references/research/README.md](../../90.references/research/README.md)
- **Reference Template**: [../../99.templates/templates/references/research-reference.template.md](../../99.templates/templates/references/research-reference.template.md)
- **Task Template**: [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)
- **Reference Maintenance Runbook**: [../../05.operations/runbooks/0011-reference-maintenance-runbook.md](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)

### Legacy Task traceability

- **Spec**: [../../03.specs/0017-workspace-engineering-research-pack/spec.md](spec.md)
- **Plan**: [../plans/2026-07-04-workspace-engineering-research-pack.md](plan.md)
- **Research README**: [../../90.references/research/README.md](../../90.references/research/README.md)
- **Reference Template**: [../../99.templates/templates/references/research-reference.template.md](../../99.templates/templates/references/research-reference.template.md)
- **Task Template**: [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)
