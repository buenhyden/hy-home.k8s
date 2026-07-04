---
title: 'Workspace Engineering Research Pack Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-07-04
---

# Workspace Engineering Research Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dated, repo-first workspace engineering research pack under `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/`.

**Architecture:** The plan uses a source-first document migration sequence. First create Stage 04 evidence, then move the current four research references into the dated pack, then refresh existing references and add two focused references, and finally close validation evidence.

**Tech Stack:** Markdown, Stage 90 reference template, Stage 04 task evidence, `git mv`, web-verified official sources, `rg`, repository quality gates, and repo-static harness validation.

---

## Overview

This document defines the implementation plan for
`docs/03.specs/017-workspace-engineering-research-pack/spec.md`.
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
`-- 2026-07-04-workspace-engineering-research-pack/
    |-- README.md
    |-- workspace-governance-baseline.md
    |-- harness-and-loop-engineering.md
    |-- provider-implementation-status.md
    |-- spec-sdlc-ci-qa-formatting.md
    |-- kubernetes-infrastructure-security.md
    `-- automation-pipeline-workflow-qa.md
```

The four current research references are moved into the dated folder:

- `docs/90.references/research/workspace-governance-baseline.md`
- `docs/90.references/research/harness-and-loop-engineering.md`
- `docs/90.references/research/provider-implementation-status.md`
- `docs/90.references/research/spec-sdlc-ci-qa-formatting.md`

External source claims must be checked during implementation. Official or
primary sources outrank market scan material. Market scan material is allowed
only when labeled non-authoritative.

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
  - `docs/04.execution/tasks/**`
  - `docs/04.execution/plans/README.md`
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

## File Structure

| Path | Responsibility |
| --- | --- |
| `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md` | Execution evidence, task table, validation commands, source limitations, handoff. |
| `docs/04.execution/tasks/README.md` | Task index entry for the research-pack work. |
| `docs/90.references/research/README.md` | Research stage entrypoint and dated pack index. |
| `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/README.md` | Dated pack entrypoint, reading order, source priority, and authority boundary. |
| `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/workspace-governance-baseline.md` | Repo-first workspace purpose, roles, governance, contracts, templates, scripts, integration guides, and evidence lanes. |
| `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md` | Harness engineering and loop engineering definitions, elements, workspace application requirements, and implementation checklist. |
| `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/provider-implementation-status.md` | Claude, Codex, Gemini provider status and shared environment/rule/system construction analysis. |
| `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/spec-sdlc-ci-qa-formatting.md` | Spec-driven development, SDLC, CI/CD, QA, formatting, linting, syntax validation, and repo validation matrix. |
| `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/kubernetes-infrastructure-security.md` | Kubernetes, infrastructure, GitOps, secrets, policy-as-code, supply-chain, and security reference. |
| `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/automation-pipeline-workflow-qa.md` | Automation, pipeline, workflow, CI job graph, validation loops, and QA evidence lanes reference. |
| `docs/90.references/README.md` | Parent reference index update for the dated research pack. |
| `docs/00.agent-governance/memory/progress.md` | Progress and reusable memory update after implementation stages. |

## Source Baseline

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
| WER-004 | Refresh harness, loop, and provider references | `harness-and-loop-engineering.md`, `provider-implementation-status.md` | VAL-SPC-004, VAL-SPC-005 | Harness/loop/provider claims cite checked official or primary sources |
| WER-005 | Refresh SDLC/CI/QA/formatting and add automation reference | `spec-sdlc-ci-qa-formatting.md`, `automation-pipeline-workflow-qa.md` | VAL-SPC-004, VAL-SPC-005 | Spec, SDLC, CI/CD, QA, formatting, linting, syntax, automation, pipeline, workflow covered |
| WER-006 | Add Kubernetes, infrastructure, and security reference | `kubernetes-infrastructure-security.md` | VAL-SPC-004, VAL-SPC-005 | Kubernetes, infrastructure, GitOps, secrets, policy, supply-chain, security covered |
| WER-007 | Close indexes, task evidence, progress, and validation | Research indexes, task evidence, progress memory | VAL-SPC-002, VAL-SPC-006, VAL-SPC-007 | Required validation passes and limitations are recorded |

## Detailed Tasks

### Task 1: Task Evidence and Baseline Inventory

**Files:**

- Create: `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Read: `docs/03.specs/017-workspace-engineering-research-pack/spec.md`

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
sed -n '1,220p' docs/99.templates/templates/sdlc/execution/task.template.md
sed -n '1,420p' docs/03.specs/017-workspace-engineering-research-pack/spec.md
```

Expected: task template and Spec requirements are visible.

- [ ] **Step 3: Capture current research inventory**

Run:

```bash
rg --files docs/90.references/research docs/90.references docs/03.specs docs/04.execution | sort
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

Create `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`
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
link `../../03.specs/017-workspace-engineering-research-pack/spec.md`.

- [ ] **Step 7: Update task README**

Add this row to `docs/04.execution/tasks/README.md`:

```markdown
| [`./2026-07-04-workspace-engineering-research-pack.md`](./2026-07-04-workspace-engineering-research-pack.md) | Workspace engineering research pack evidence for dated Stage 90 research references, existing reference moves, external-source refresh, Kubernetes/infrastructure/security, automation/pipeline/workflow/QA, and validation closure. | Draft | 2026-07-04 |
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
git add docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(task): Track workspace engineering research pack"
```

Expected: diff check and repo quality pass; one task evidence commit is
created.

### Task 2: Dated Pack Scaffold and Existing Reference Move

**Files:**

- Create: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/README.md`
- Move: four current flat research references into the dated pack folder
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/README.md`
- Modify: task record and progress memory

- [ ] **Step 1: Create dated pack folder**

Run:

```bash
mkdir -p docs/90.references/research/2026-07-04-workspace-engineering-research-pack
```

Expected: folder exists.

- [ ] **Step 2: Move existing references with `git mv`**

Run:

```bash
git mv docs/90.references/research/workspace-governance-baseline.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/workspace-governance-baseline.md
git mv docs/90.references/research/harness-and-loop-engineering.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md
git mv docs/90.references/research/provider-implementation-status.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/provider-implementation-status.md
git mv docs/90.references/research/spec-sdlc-ci-qa-formatting.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/spec-sdlc-ci-qa-formatting.md
```

Expected: `git status --short` shows four renames.

- [ ] **Step 3: Create dated pack README**

Create `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/README.md`
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
  `./2026-07-04-workspace-engineering-research-pack/<filename>.md`,
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
git add docs/90.references/research docs/90.references/README.md docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Scaffold workspace engineering research pack"
```

Expected: validation passes and the commit contains moved references, pack
README, index updates, and WER-002 evidence.

### Task 3: Workspace Governance Baseline Refresh

**Files:**

- Modify: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/workspace-governance-baseline.md`
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
rg -n "^## (Overview|Purpose|Reference Type|Authority Boundary|Scope|Definitions / Facts|Sources|Review and Freshness|Related Documents)$" docs/90.references/research/2026-07-04-workspace-engineering-research-pack/workspace-governance-baseline.md
```

Expected: all required headings are present.

- [ ] **Step 6: Update task evidence and progress**

Mark `WER-003` done and record the baseline source scan plus heading scan.

- [ ] **Step 7: Validate and commit WER-003**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/2026-07-04-workspace-engineering-research-pack/workspace-governance-baseline.md docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Refresh workspace governance baseline"
```

Expected: validation passes and the commit contains only the baseline
reference plus evidence updates.

### Task 4: Harness, Loop, and Provider Source Refresh

**Files:**

- Modify: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/provider-implementation-status.md`
- Modify: task record and progress memory

- [ ] **Step 1: Verify official provider and loop sources with web research**

Browse current official or primary sources for OpenAI/Codex, Anthropic Claude
Code, Google Gemini/ADK, and MCP. Record checked source URLs in task evidence.

Expected: sources are current enough to support 2026-07-04 source checked
metadata.

- [ ] **Step 2: Refresh harness and loop document**

Update `harness-and-loop-engineering.md` so it covers:

- harness engineering elements,
- loop engineering elements,
- workspace application requirements,
- required environment/rule/system elements,
- market scan section labeled non-authoritative,
- implementation checklist.

Use the source checked date `2026-07-04`.

- [ ] **Step 3: Refresh provider implementation status document**

Update `provider-implementation-status.md` so it covers:

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
rg -n "Claude|Codex|Gemini|OpenAI|Anthropic|Google|ADK|MCP|non-authoritative|Source checked: 2026-07-04|Review and Freshness" docs/90.references/research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/provider-implementation-status.md
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
git add docs/90.references/research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/provider-implementation-status.md docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Refresh harness loop and provider sources"
```

Expected: validation passes and the commit contains two research references
plus evidence updates.

### Task 5: SDLC, CI, QA, Formatting, Automation, Pipeline, and Workflow

**Files:**

- Modify: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/spec-sdlc-ci-qa-formatting.md`
- Create: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/automation-pipeline-workflow-qa.md`
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
`docs/99.templates/templates/common/reference.template.md` with:

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
rg -n "spec-driven|SDLC|CI/CD|QA|formatting|linting|syntax|Automation|pipeline|workflow|non-authoritative|Source checked: 2026-07-04|Review and Freshness" docs/90.references/research/2026-07-04-workspace-engineering-research-pack/spec-sdlc-ci-qa-formatting.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/automation-pipeline-workflow-qa.md
```

Expected: output shows all required topic terms and source/freshness metadata.

- [ ] **Step 6: Update task evidence and progress**

Mark `WER-005` done and record source groups, coverage scan, and limitations.

- [ ] **Step 7: Validate and commit WER-005**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/2026-07-04-workspace-engineering-research-pack/spec-sdlc-ci-qa-formatting.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/automation-pipeline-workflow-qa.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/README.md docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Refresh delivery automation and QA sources"
```

Expected: validation passes and the commit contains SDLC/QA refresh,
automation reference, README index update, and evidence updates.

### Task 6: Kubernetes, Infrastructure, and Security Reference

**Files:**

- Create: `docs/90.references/research/2026-07-04-workspace-engineering-research-pack/kubernetes-infrastructure-security.md`
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
`docs/99.templates/templates/common/reference.template.md` with:

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
rg -n "Kubernetes|Infrastructure|GitOps|Secret|External Secrets|policy-as-code|OPA|Conftest|supply-chain|security|SLSA|OpenSSF|non-authoritative|Source checked: 2026-07-04|Review and Freshness" docs/90.references/research/2026-07-04-workspace-engineering-research-pack/kubernetes-infrastructure-security.md
```

Expected: output shows all required topic terms and source/freshness metadata.

- [ ] **Step 5: Update task evidence and progress**

Mark `WER-006` done and record source groups, coverage scan, and limitations.

- [ ] **Step 6: Validate and commit WER-006**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/research/2026-07-04-workspace-engineering-research-pack/kubernetes-infrastructure-security.md docs/90.references/research/2026-07-04-workspace-engineering-research-pack/README.md docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(research): Add Kubernetes infrastructure security sources"
```

Expected: validation passes and the commit contains the new reference, pack
README update, and evidence updates.

### Task 7: Final Index, Evidence, and Validation Closure

**Files:**

- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/README.md`
- Modify: `docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`
- Modify: `docs/04.execution/tasks/README.md`
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
rg -n "Source checked: 2026-07-04|Review and Freshness|non-authoritative|Authority Boundary" docs/90.references/research/2026-07-04-workspace-engineering-research-pack
rg -n "Kubernetes|Infrastructure|Security|Automation|pipeline|workflow|QA|formatting|linting|syntax" docs/90.references/research/2026-07-04-workspace-engineering-research-pack
```

Expected: stale flat-link scan has no current-path matches outside historical
evidence; source/freshness and topic scans show required coverage.

- [ ] **Step 4: Close plan and task statuses**

Update:

- this plan frontmatter `status: done`,
- `docs/04.execution/plans/README.md` row to `Done`,
- task record frontmatter `status: done`,
- `docs/04.execution/tasks/README.md` row to `Done`,
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
git add docs/90.references/research/README.md docs/90.references/README.md docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(validation): Close workspace engineering research pack"
```

Expected: final closure commit exists and no unresolved drift remains.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WER-001 | Structural | Diff hygiene | `git diff --check` | No output |
| VAL-WER-002 | Repository | Repository quality gate | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed` |
| VAL-WER-003 | Harness | Full repo-static harness | `bash scripts/validate-harness.sh` | Ends with `PASS harness repo-static validation` |
| VAL-WER-004 | Links | Flat research stale-link scan | Focused `rg` command in Task 7 Step 3 | No current stale flat links outside historical evidence |
| VAL-WER-005 | Source boundary | Source/freshness scan | Focused `rg` command in Task 7 Step 3 | Source checked, freshness, non-authoritative, and authority boundary terms are present |
| VAL-WER-006 | Topic coverage | Required topic scan | Focused `rg` command in Task 7 Step 3 | Required topics appear in the dated pack |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Stale flat research links remain after the move | Medium | Run focused `rg` stale-link scans and update indexes in the move commit |
| Research documents become active policy | High | Keep authority boundaries explicit and route policy changes to canonical owners |
| Provider or tool claims drift from current docs | Medium | Use web research during implementation and record checked dates |
| Market scan becomes over-weighted | Medium | Label market scan non-authoritative and place it below official/repo-backed evidence |
| Scope grows beyond a compact pack | Medium | Keep the pack to one README, four moved references, and two new references |
| Optional tools are mistaken for full coverage | Medium | Preserve SKIP/fallback wording for optional `kube-linter` and `conftest` results |

## Agent Rollout & Evaluation Gates (If Applicable)

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

## Completion Criteria

- [ ] Dated research pack folder exists.
- [ ] Four existing research references are moved into the dated pack.
- [ ] Two new focused references exist.
- [ ] Existing references are refreshed with 2026-07-04 source checked
  metadata where claims are updated.
- [ ] Root and parent indexes route to the dated pack.
- [ ] Stage 04 task evidence and progress memory are complete.
- [ ] Required validation passes.
- [ ] Logical-unit commits exist for each completed task.

## Related Documents

- **Spec**: [Workspace Engineering Research Pack](../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Prior Research Spec**: [Workspace Harness Research Pack](../../03.specs/009-workspace-harness-research-pack/spec.md)
- **Task Record**: `../tasks/2026-07-04-workspace-engineering-research-pack.md`
- **Research README**: [../../90.references/research/README.md](../../90.references/research/README.md)
- **Reference Template**: [../../99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md)
- **Task Template**: [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
- **Reference Maintenance Runbook**: [../../05.operations/runbooks/0011-reference-maintenance-runbook.md](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
