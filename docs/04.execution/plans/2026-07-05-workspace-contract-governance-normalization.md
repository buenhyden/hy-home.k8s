---
title: 'Workspace Contract Governance Normalization Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-06
---

# Workspace Contract Governance Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Define `_workspace` as a safe repository support staging surface and
normalize repo-wide documentation, governance, frontmatter, template, CI/CD,
QA, formatting, linting, automation, and validation drift against current
contracts.

**Architecture:** This is a contract-first documentation and validator change.
The implementation creates durable task evidence, establishes the `_workspace`
contract and ignore boundary, audits current repository surfaces, patches only
clear active-contract drift, then closes with deterministic validation and
progress memory.

**Tech Stack:** Markdown, YAML frontmatter, Bash, Python embedded in
`scripts/validate-repo-quality-gates.sh`, `.gitignore`, GitHub Actions YAML,
`rg`, `find`, `sed`, `git diff --check`, `apply_patch`, and repository quality
gates.

---

## Overview

This plan implements
`../../03.specs/020-workspace-contract-governance-normalization/spec.md`.
The work is repository-static. It does not mutate Kubernetes, Argo CD, Vault,
ESO, cloud resources, provider accounts, GitHub remotes, credentials, secret
values, paid jobs, published artifacts, or live CI topology.

The plan deliberately routes durable output to Stage 04 task evidence, Stage
00 governance, Stage 99 template support, active README indexes, and the
repository quality gate. `_workspace` remains temporary scratch, with one
tracked README allowed to define the boundary and all scratch artifacts ignored
by default.

## Context

The approved Stage 03 specification defines these active contracts:

- `_workspace` may hold temporary, non-secret, task-scoped analysis scratch.
- `_workspace` must not hold diagnostics, local logs with secret risk, auth
  files, token caches, kubeconfigs, SSH keys, browser profiles, shell history,
  or provider credential material.
- README files remain entrypoints and indexes, not full governance bodies.
- Template forms remain under `docs/99.templates/templates/**`; reusable rules
  remain under `docs/99.templates/support/**`.
- Stage 00 owns agent execution policy, provider behavior, protected surfaces,
  and approval boundaries.
- Current authored Markdown frontmatter uses the canonical key order `title`,
  `type`, `status`, `owner`, `updated`.

Current local evidence before implementation:

- `_workspace/` exists locally but is ignored and empty.
- `.gitignore` currently ignores `_workspace/` as a whole, so a tracked
  `_workspace/README.md` cannot be added until the ignore rule is narrowed.
- `docs/00.agent-governance/subagent-protocol.md` already mentions scratch
  workspaces but requires a checked-in skill to define them; this plan promotes
  the `_workspace` boundary into a repository contract.
- `DESIGN.md` is listed in the requested target surface but is not present in
  the repository. The task evidence must record it as absent; do not create it
  unless a future approved design-doc contract routes that file.

## Goals & In-Scope

- **Goals**:
  - Add a tracked `_workspace/README.md` contract and keep scratch files
    ignored by default.
  - Align Stage 00 governance, Stage 99 support contracts, root README, and
    validators with the `_workspace` role.
  - Audit listed repository targets for frontmatter, section, template,
    governance, legacy, README, CI/CD, QA, formatting, linting, syntax-check,
    automation, pipeline, workflow, and security drift.
  - Patch active drift when the canonical owner is clear.
  - Record baseline, remediation, validation, and deferrals in Stage 04 task
    evidence and the progress ledger.
- **In Scope**:
  - Root shims and README surfaces: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
    `README.md`, and the absent `DESIGN.md` inventory record.
  - Agent surfaces: `.agents/**`, `.claude/**`, `.codex/**`, and
    `docs/00.agent-governance/**`.
  - Documentation stages: `docs/**`, including Stage 90 references and Stage
    99 templates/support contracts.
  - Control and automation surfaces: `.github/**`, `scripts/**`, `tests/**`,
    `examples/**`, `gitops/**`, `infrastructure/**`, `policy/**`, `secrets/**`,
    and `traefik/**`.
  - Repository-static validation only.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Create a new documentation taxonomy or duplicate template contract.
  - Rewrite broad prose that already matches the active contract.
  - Promote `_workspace` into durable evidence storage.
  - Add frontmatter to README files or GitHub-native Markdown control files.
  - Add a `DESIGN.md` document without an approved route and template contract.
  - Change live CI topology, branch protection, GitHub repository settings, or
    workflow permissions.
- **Out of Scope**:
  - Live Kubernetes, Argo CD, Vault, ESO, cloud, GitHub remote mutation,
    provider runtime changes, credentials, secret values, paid jobs,
    publishing, merge, push, pull request creation, or third-party mutation.

## File Structure

| Path | Responsibility |
| --- | --- |
| `docs/04.execution/plans/2026-07-05-workspace-contract-governance-normalization.md` | This implementation plan. |
| `docs/04.execution/plans/README.md` | Plan index and structure entry. |
| `docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md` | Execution evidence, audit inventory, validation results, deferrals, and handoff. |
| `docs/04.execution/tasks/README.md` | Task index and structure entry. |
| `.gitignore` | Ignore all `_workspace` scratch artifacts while allowing `_workspace/README.md`. |
| `_workspace/README.md` | Tracked boundary contract for temporary non-secret repo-support staging. |
| `README.md` | Root inventory entry for `_workspace` and boundary reminder for `secrets/`. |
| `docs/00.agent-governance/subagent-protocol.md` | Multi-agent scratch workspace rule and durable-output promotion boundary. |
| `docs/00.agent-governance/rules/documentation-protocol.md` | Document output routing and drift cleanup rule for `_workspace`. |
| `docs/00.agent-governance/rules/approval-boundaries.md` | Protected-surface boundary for scratch artifacts, secret risk, and cleanup escalation. |
| `docs/99.templates/support/documentation-contract.md` | Support contract surface table and validation boundary for `_workspace`. |
| `docs/99.templates/support/frontmatter-schema.md` | README/frontmatter-free exception notes for `_workspace/README.md`. |
| `docs/99.templates/support/legacy-cleanup-rules.md` | Legacy scratch, backup, local log, auth, token, and diagnostic residue cleanup rules. |
| `.github/ABOUT.md` | GitHub control-surface summary of repo quality and secret boundary if stale. |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR checklist mirror for `_workspace` and secret-risk staging if stale. |
| `.github/SECURITY.md` | GitHub-native security reporting boundary if stale. |
| `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md` | Current CI/CD, QA, formatting, linting, syntax-check, workflow, and automation reference owner. |
| `scripts/README.md` | Script inventory and validation contract mirror if stale. |
| `tests/README.md` | Repository test evidence boundary if stale. |
| `scripts/validate-repo-quality-gates.sh` | Deterministic checks for `_workspace` ignore/tracking boundary and routed documentation contracts. |
| `docs/00.agent-governance/memory/progress.md` | Durable completion memory after final validation. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target Spec Criteria | Validation Criteria |
| --- | --- | --- | --- | --- |
| WCGN-001 | Create Stage 04 task evidence and baseline inventory | Task record, task README, plan README | VAL-SPC-020-003, VAL-SPC-020-004, VAL-SPC-020-006, VAL-SPC-020-007 | Baseline scans recorded; working tree contains only Stage 04 evidence/index changes before commit |
| WCGN-002 | Establish `_workspace` contract and ignore boundary | `.gitignore`, `_workspace/README.md`, root README, Stage 00, Stage 99 support | VAL-SPC-020-001, VAL-SPC-020-002, VAL-SPC-020-005 | `_workspace/README.md` is tracked; scratch artifacts are ignored; quality gate passes |
| WCGN-003 | Audit and remediate frontmatter, template, section, README, and cross-link drift | `docs/**`, root shims, `.agents/**`, `.claude/**`, `.codex/**`, Stage 00/99 | VAL-SPC-020-003, VAL-SPC-020-004, VAL-SPC-020-005, VAL-SPC-020-007 | Focused scans show only templates or historical evidence for allowed legacy patterns |
| WCGN-004 | Audit and remediate CI/CD, QA, formatting, linting, syntax, automation, workflow, and security drift | `.github/**`, scripts, tests, operations guide, active control surfaces | VAL-SPC-020-006 | CI/QA descriptions match current workflows and local validators or are recorded as deferred gaps |
| WCGN-005 | Add validator coverage, close evidence, and record memory | Validator, task evidence, task README, progress memory | VAL-SPC-020-008, VAL-SPC-020-009, VAL-SPC-020-010 | `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .` pass |

## Detailed Tasks

> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.

### Task 1: Create Task Evidence and Baseline Inventory

**Files:**

- Create: `docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/04.execution/plans/README.md`
- Read: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Read: `docs/03.specs/020-workspace-contract-governance-normalization/spec.md`
- Read: `docs/99.templates/support/template-routing.md`
- Read: `docs/00.agent-governance/rules/documentation-protocol.md`

- [ ] **Step 1: Confirm the branch and clean state**

Run:

```bash
git status --short --branch
```

Expected: branch is `codex/workspace-engineering-audit-pack` and the working
tree is clean after this plan commit.

- [ ] **Step 2: Read the task template and approved spec**

Run:

```bash
sed -n '1,220p' docs/99.templates/templates/sdlc/execution/task.template.md
sed -n '1,460p' docs/03.specs/020-workspace-contract-governance-normalization/spec.md
```

Expected: the task template shows `type: sdlc/task`; the spec shows
`VAL-SPC-020-001` through `VAL-SPC-020-010`.

- [ ] **Step 3: Create the task evidence document**

Create `docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md`
with frontmatter:

```yaml
---
title: 'Task: Workspace Contract Governance Normalization'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-05
---
```

Use these top-level sections in order:

```markdown
# Task: Workspace Contract Governance Normalization

## Overview

## Inputs

## Working Rules

## Task Table

## Baseline Inventory

## Audit Findings

## Remediation Evidence

## Verification Commands

## Validation Evidence

## Deferrals

## Related Documents
```

Populate the `## Task Table` with rows for WCGN-001 through WCGN-005. Set
WCGN-001 to `In Progress` and the other rows to `Planned`.

- [ ] **Step 4: Record the requested target inventory**

Run:

```bash
find AGENTS.md CLAUDE.md GEMINI.md README.md _workspace .agents .claude .codex .github docs examples gitops infrastructure policy scripts secrets tests traefik -maxdepth 3 -print | sort
```

Expected: output lists existing target paths. Record in the task evidence that
`DESIGN.md` is absent with this exact row:

```markdown
| `DESIGN.md` | Absent | User-requested target; no canonical route currently exists. Do not create without a future approved design-doc contract. |
```

- [ ] **Step 5: Record `_workspace` baseline**

Run:

```bash
find _workspace -maxdepth 4 -type f -print | sort
git check-ignore -v _workspace/probe.log
```

Expected: `find` returns no files before implementation; `git check-ignore`
shows that `_workspace/probe.log` is ignored by `.gitignore`.

- [ ] **Step 6: Record frontmatter and template drift baselines**

Run:

```bash
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "Target: d""ocs/|Use this ""template|SNIPPET LIBRARY|\\{Folder or Project Name\\}|\\[Feature Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: active simple `type` values return no matches; template-residue
matches are limited to template files or explicitly historical evidence. Record
the exact command result class in the task evidence.

- [ ] **Step 7: Commit Task 1**

Run:

```bash
git add docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git commit -m "docs(tasks): Start workspace contract governance evidence"
```

Expected: staged diff has no whitespace errors and the commit succeeds.

### Task 2: Establish `_workspace` Contract and Ignore Boundary

**Files:**

- Modify: `.gitignore`
- Create: `_workspace/README.md`
- Modify: `README.md`
- Modify: `docs/00.agent-governance/subagent-protocol.md`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/approval-boundaries.md`
- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md`

- [ ] **Step 1: Narrow the `_workspace` ignore rule**

Replace the current `_workspace/` rule in `.gitignore` with:

```gitignore
_workspace/*
!_workspace/
!_workspace/README.md
```

Keep `_workspace_prev/` ignored.

- [ ] **Step 2: Create `_workspace/README.md` from the README template**

Create a frontmatter-free README with the required headings:

```markdown
# _workspace

> Repository-local support staging area for temporary, non-secret analysis scratch.

## Overview

## Audience

## Scope

### In Scope

### Out of Scope

## Structure

## How to Work in This Area

## Link Basis

## Related Documents
```

The body must state these contract facts:

- Allowed artifacts are temporary audit scratch, dry-run logs, migration
  ledgers, route inventories, and non-secret scan summaries.
- Prohibited artifacts are credentials, tokens, auth files, shell history,
  kubeconfigs, SSH keys, browser profiles, provider caches, personal
  diagnostics, and secret-bearing local logs.
- Durable findings must be promoted to Stage 04 task evidence, Stage 90
  audits, Stage 00 governance, Stage 99 support contracts, or deleted before
  closure.
- Scratch artifacts remain ignored by default; only this README is tracked.

- [ ] **Step 3: Update root README structure**

In `README.md`, add `_workspace/` to the repository structure block near
`tests/` and `scripts/` with this role:

```text
├── _workspace/            # Temporary non-secret analysis scratch boundary; README tracked only
```

Keep `secrets/` described as a sensitive-file boundary, not a scratch area.

- [ ] **Step 4: Promote Stage 00 governance language**

Update `docs/00.agent-governance/subagent-protocol.md` so the scratch
workspace rule points to `_workspace/README.md` as the checked-in contract,
requires scratch files to remain ignored by default, and requires durable
outputs to be promoted into the canonical docs taxonomy.

Update `docs/00.agent-governance/rules/documentation-protocol.md` under
Document Output Routing or Drift Garbage Collection with this rule:

```markdown
- `_workspace/` is a temporary non-secret repo-support staging surface.
  Do not treat it as durable documentation; promote durable findings into the
  canonical docs taxonomy before closure.
```

Update `docs/00.agent-governance/rules/approval-boundaries.md` so any
potential secret-bearing `_workspace` artifact is treated like a protected
surface: do not inspect values; record the path class; request human approval
before cleanup that could destroy user-local evidence.

- [ ] **Step 5: Align Stage 99 support contracts**

Update `docs/99.templates/support/documentation-contract.md` to add a support
surface for `_workspace`:

```markdown
| Workspace scratch staging | `_workspace/README.md` plus ignored `_workspace/**` scratch | Temporary non-secret repo-support staging; durable findings promote to canonical docs. |
```

Update `docs/99.templates/support/frontmatter-schema.md` exceptions to state
that `_workspace/README.md` is a frontmatter-free README and scratch files are
not authored documents.

Update `docs/99.templates/support/legacy-cleanup-rules.md` to reject active
tracked scratch residue named or classified as backup files, auth files, token
caches, shell history, local diagnostics, or secret-bearing logs.

- [ ] **Step 6: Validate `_workspace` behavior**

Run:

```bash
git check-ignore -v _workspace/probe.log
git check-ignore -v _workspace/README.md
git ls-files _workspace
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

- `_workspace/probe.log` is ignored.
- `_workspace/README.md` is not ignored.
- `git ls-files _workspace` lists only `_workspace/README.md`.
- `git diff --check` passes.
- Repository quality gates pass.

- [ ] **Step 7: Update task evidence and commit Task 2**

Record the command outputs and set WCGN-002 to `Done`.

Run:

```bash
git add .gitignore _workspace/README.md README.md docs/00.agent-governance/subagent-protocol.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/approval-boundaries.md docs/99.templates/support/documentation-contract.md docs/99.templates/support/frontmatter-schema.md docs/99.templates/support/legacy-cleanup-rules.md docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git commit -m "docs(governance): Define workspace staging boundary"
```

Expected: staged diff has no whitespace errors and the commit succeeds.

### Task 3: Audit and Remediate Frontmatter, Template, Section, README, and Cross-link Drift

**Files:**

- Modify as findings require: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `README.md`, `.agents/**`, `.claude/**`, `.codex/**`, `docs/**`
- Modify as evidence owner: `docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md`
- Read: `docs/99.templates/support/frontmatter-schema.md`
- Read: `docs/99.templates/support/template-routing.md`
- Read: `docs/99.templates/support/documentation-contract.md`
- Read: `docs/99.templates/support/legacy-cleanup-rules.md`

- [ ] **Step 1: Run the canonical quality gate first**

Run:

```bash
bash scripts/validate-repo-quality-gates.sh .
```

Expected: pass before further remediation. If it fails, record each failure in
the task evidence and fix the owning contract or active document before moving
to broader scans.

- [ ] **Step 2: Scan frontmatter type drift**

Run:

```bash
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references docs/98.archive docs/99.templates/support docs/00.agent-governance
```

Expected: simple un-namespaced `type` values return no active matches. For any
active match, replace the value with the profile in
`docs/99.templates/support/frontmatter-schema.md` and keep key order as
`title`, `type`, `status`, `owner`, `updated`.

- [ ] **Step 3: Scan template residue and legacy section drift**

Run:

```bash
rg -n "Target: d""ocs/|Use this ""template|SNIPPET LIBRARY|\\{Folder or Project Name\\}|\\[Feature Name\\]|command ""1|pytest ""tests|Example""Contract" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^## (Deprecated|Legacy|Related Refer""ences|Related Fold""ers|Related Fi""les|References|See Also|Links)\\b" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: matches are limited to template files, historical evidence, or
explicit cleanup rules. Remove residue from active authored documents and route
policy bodies to the canonical Stage 00 or Stage 99 support owner.

- [ ] **Step 4: Scan README governance duplication**

Run:

```bash
find . -name README.md -not -path './.git/*' -not -path './.agents/*' -not -path './.agent-work/*' -print | sort
rg -n "must|forbidden|required|canonical owner|contract owner|approval boundary|protected surface" README.md docs/**/README.md .codex/README.md .claude/README.md
```

Expected: README files summarize ownership and link to canonical contracts.
When a README contains full policy prose that belongs to Stage 00 or Stage 99,
replace it with a short entrypoint sentence and a link to the owning document.

- [ ] **Step 5: Scan route and cross-link drift**

Run:

```bash
rg -n "docs/superpowers|docs/api/|docs/01\\.requirements/YYYY-MM-DD-|docs/03\\.specs/<feature-id>" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: current-route drift returns no active references. Historical or
migration evidence remains only in Stage 04 task evidence, Stage 90 audits, or
progress memory with historical wording.

- [ ] **Step 6: Validate and commit Task 3**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Record findings, remediations, and any accepted historical evidence in the task
document. Set WCGN-003 to `Done`.

Run:

```bash
git add AGENTS.md CLAUDE.md GEMINI.md README.md .agents .claude .codex docs .github scripts docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git commit -m "docs(governance): Normalize document contract drift"
```

Expected: only files with actual WCGN-003 drift fixes are staged; staged diff
has no whitespace errors and the commit succeeds.

### Task 4: Audit and Remediate CI/CD, QA, Formatting, Linting, Syntax, Automation, Workflow, and Security Drift

**Files:**

- Modify as findings require: `.github/ABOUT.md`
- Modify as findings require: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify as findings require: `.github/SECURITY.md`
- Modify as findings require: `.github/workflows/*.yml`
- Modify as findings require: `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`
- Modify as findings require: `scripts/README.md`
- Modify as findings require: `tests/README.md`
- Modify as evidence owner: `docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md`
- Read: `.github/workflows/ci.yml`
- Read: `scripts/validate-repo-quality-gates.sh`
- Read: `scripts/validate-harness.sh`
- Read: `scripts/check-secret-handling.sh`
- Read: `scripts/validate-gitops-structure.sh`
- Read: `scripts/validate-k8s-manifests.sh`
- Read: `scripts/validate-policy-gates.sh`

- [ ] **Step 1: Inventory current workflows and validator commands**

Run:

```bash
find .github/workflows scripts tests -maxdepth 2 -type f | sort
rg -n "validate-repo-quality-gates|validate-harness|check-secret-handling|validate-gitops-structure|validate-k8s-manifests|validate-policy-gates|git diff --check|kube-linter|zizmor" .github scripts tests docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md README.md
```

Expected: active descriptions point to existing scripts and workflow jobs.
Record workflow names, script names, and documented validation lanes in the
task evidence.

- [ ] **Step 2: Verify workflow claims against `.github/workflows/ci.yml`**

Run:

```bash
sed -n '1,220p' .github/workflows/ci.yml
sed -n '1,260p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
sed -n '1,240p' .github/ABOUT.md
```

Expected: `.github/ABOUT.md` and the CI/QA guide describe the same active jobs,
static validation commands, and non-deploy boundary as `.github/workflows/ci.yml`.
Patch stale job names, obsolete shell validation job claims, or missing repo-quality
coverage references.

- [ ] **Step 3: Verify QA, formatting, linting, and syntax wording**

Run:

```bash
rg -n "format|formatting|lint|linting|syntax|typecheck|test|QA|quality gate" README.md docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md scripts/README.md tests/README.md .github/PULL_REQUEST_TEMPLATE.md
```

Expected: wording distinguishes formatting checks, linting/static checks,
syntax checks, manifest checks, secret scans, policy checks, and repository
quality gates. Patch only statements that contradict current local scripts or
workflow jobs.

- [ ] **Step 4: Verify security and protected-surface wording**

Run:

```bash
rg -n "secret|credential|token|kubeconfig|SSH|auth|history|_workspace|protected surface|approval" README.md .github docs/00.agent-governance docs/05.operations scripts tests
```

Expected: security wording forbids plaintext secrets and points to
`scripts/check-secret-handling.sh .`; `_workspace` references state the
non-secret scratch boundary.

- [ ] **Step 5: Validate and commit Task 4**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Record findings, remediations, and deferred external/live checks in the task
document. Set WCGN-004 to `Done`.

Run:

```bash
git add .github docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md scripts/README.md tests/README.md README.md docs/00.agent-governance docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md
git diff --cached --check
git commit -m "docs(qa): Align control surface validation contracts"
```

Expected: only files with actual WCGN-004 drift fixes are staged; staged diff
has no whitespace errors and the commit succeeds.

### Task 5: Add Validator Coverage, Close Evidence, and Record Memory

**Files:**

- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/common/progress.template.md`

- [ ] **Step 1: Add deterministic `_workspace` validator checks**

In `scripts/validate-repo-quality-gates.sh`, add checks near the existing
tracked-file and temporary-file checks so the gate fails when:

- `_workspace/README.md` is missing after the contract is introduced.
- `.gitignore` does not ignore `_workspace/*`.
- `.gitignore` does not unignore `_workspace/README.md`.
- `git ls-files _workspace` contains any tracked file other than
  `_workspace/README.md`.
- Any tracked `_workspace` file path contains a prohibited name pattern:
  `token`, `secret`, `credential`, `auth`, `history`, `kubeconfig`, `ssh`,
  `password`, `diagnostic`, `profile`, or `cache`.

Use existing helper functions such as `fail()` and `rel()` and existing
`git ls-files` inventory variables instead of adding a separate validator.

- [ ] **Step 2: Validate the new validator behavior**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git ls-files _workspace
git check-ignore -v _workspace/probe.log
```

Expected:

- `git diff --check` passes.
- Repository quality gates pass.
- `git ls-files _workspace` lists `_workspace/README.md` only.
- `_workspace/probe.log` is ignored.

- [ ] **Step 3: Run final focused scans**

Run:

```bash
find _workspace -maxdepth 4 -type f | sort
rg -n "(token|secret|credential|auth|history|kubeconfig|ssh|password|diagnostic|profile|cache)" _workspace
rg -n "T""BD|TO""DO|\\{Feature ""Name\\}|\\[Feature ""Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "docs/superpowers|docs/api/" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs
```

Expected:

- `_workspace` contains only `README.md`.
- The `_workspace` prohibited-word scan does not report tracked scratch files.
- Placeholder matches are limited to templates or explicit scanner commands in
  task/spec evidence.
- Route drift scans report no active contract drift.
- Simple `type` values return no active matches.

- [ ] **Step 4: Close task evidence and progress memory**

Update the task document:

- Set all WCGN rows to `Done`.
- Add final validation outputs.
- Record any accepted deferrals with owner, reason, and next trigger.

Append a progress ledger entry to
`docs/00.agent-governance/memory/progress.md` using the progress template
style. The entry must include:

- `_workspace` contract introduced.
- Scratch files ignored by default; only `_workspace/README.md` tracked.
- No live runtime, GitHub remote, provider, credential, or secret-value action
  performed.
- Final validation commands and pass/finding status.

- [ ] **Step 5: Mark plan and task indexes current**

Update `docs/04.execution/plans/README.md` and
`docs/04.execution/tasks/README.md` so this plan and task are listed with
status `Done` only after final validation passes.

- [ ] **Step 6: Commit Task 5**

Run:

```bash
git add scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md docs/04.execution/tasks/README.md docs/04.execution/plans/README.md docs/00.agent-governance/memory/progress.md
git diff --cached --check
git commit -m "docs(validation): Close workspace contract governance normalization"
```

Expected: staged diff has no whitespace errors and the commit succeeds.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-020-001 | Structural | `_workspace` tracking boundary | `git ls-files _workspace` | Lists `_workspace/README.md` only |
| VAL-PLN-020-002 | Structural | `_workspace` scratch ignore boundary | `git check-ignore -v _workspace/probe.log` | Returns the `.gitignore` rule that ignores scratch |
| VAL-PLN-020-003 | Security | `_workspace` prohibited path scan | `rg -n "(token|secret|credential|auth|history|kubeconfig|ssh|password|diagnostic|profile|cache)" _workspace` | No tracked scratch artifact is reported |
| VAL-PLN-020-004 | Documentation | Frontmatter simple type scan | `rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs` | No active un-namespaced `type` value remains |
| VAL-PLN-020-005 | Documentation | Template residue scan | `rg -n "Target: d""ocs/|Use this ""template|SNIPPET LIBRARY|\\{Folder or Project Name\\}|\\[Feature Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | Matches are templates, historical evidence, or scanner commands only |
| VAL-PLN-020-006 | Documentation | Route drift scan | `rg -n "docs/superpowers|docs/api/" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | No active route drift remains |
| VAL-PLN-020-007 | QA | Whitespace validation | `git diff --check` | Exits 0 |
| VAL-PLN-020-008 | QA | Repository quality gate | `bash scripts/validate-repo-quality-gates.sh .` | Exits 0 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Broad target list creates unrelated churn | High | Patch only current-contract drift with a clear owner; record ambiguous findings as deferrals in Stage 04 evidence. |
| `_workspace` becomes a secret sink | High | Track only `_workspace/README.md`, ignore scratch by default, and add validator checks for tracked prohibited path patterns. |
| README files accumulate governance bodies | Medium | Keep README changes to inventory and routing summaries; move rules to Stage 00 or Stage 99 support owners. |
| Validator change becomes too large | Medium | Add only deterministic `_workspace` checks near existing tracked-file checks; keep unrelated validator refactors out of scope. |
| External/live validation is mistaken for repo-static validation | High | Keep live runtime, provider, GitHub remote, credential, and secret-value actions out of scope and record this in task evidence. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: `git diff --check`, focused `rg` scans, `git ls-files
  _workspace`, `git check-ignore -v _workspace/probe.log`, and
  `bash scripts/validate-repo-quality-gates.sh .`.
- **Sandbox / Canary Rollout**: Not applicable. The change is repository-static
  documentation and validation.
- **Human Approval Gate**: Required for live runtime validation, CI topology
  mutation, provider config changes, model policy changes, GitOps manifest
  mutation, secret handling, push, merge, PR creation, or cleanup of
  user-local secret-risk artifacts.
- **Rollback Trigger**: Revert the last logical commit if the quality gate
  fails because a new contract contradicts an existing Stage 00 or Stage 99
  owner and the conflict cannot be resolved in the same task.
- **Prompt / Model Promotion Criteria**: Not applicable. No prompt, model, or
  provider runtime promotion is introduced.

## Completion Criteria

- [ ] `_workspace/README.md` documents allowed artifacts, prohibited artifacts,
  retention, cleanup, and promotion targets.
- [ ] `_workspace` scratch files are ignored by default and only
  `_workspace/README.md` is tracked.
- [ ] Stage 00 and Stage 99 support contracts route `_workspace` and durable
  evidence consistently.
- [ ] Frontmatter, template residue, legacy section, README, and route scans
  have been remediated or recorded as allowed historical evidence.
- [ ] CI/CD, QA, formatting, linting, syntax-check, automation, workflow, and
  security docs match current local scripts/workflows or have explicit
  deferrals.
- [ ] `scripts/validate-repo-quality-gates.sh` enforces the `_workspace`
  tracking boundary.
- [ ] Stage 04 task evidence and progress memory record final results.
- [ ] `git diff --check` passes.
- [ ] `bash scripts/validate-repo-quality-gates.sh .` passes.

## Related Documents

- **Spec**: [../../03.specs/020-workspace-contract-governance-normalization/spec.md](../../03.specs/020-workspace-contract-governance-normalization/spec.md)
- **Task**: [../tasks/2026-07-05-workspace-contract-governance-normalization.md](../tasks/2026-07-05-workspace-contract-governance-normalization.md)
- **Template Documentation Contract**: [../../99.templates/support/documentation-contract.md](../../99.templates/support/documentation-contract.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Approval Boundaries**: [../../00.agent-governance/rules/approval-boundaries.md](../../00.agent-governance/rules/approval-boundaries.md)
- **Repository Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
