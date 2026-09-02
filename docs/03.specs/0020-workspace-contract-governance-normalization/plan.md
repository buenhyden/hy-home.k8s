---
title: 'Workspace Contract Governance Normalization Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-07-13
artifact_id: "SPEC-0020-PLAN-0001"
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
`../../03.specs/0020-workspace-contract-governance-normalization/spec.md`.
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

### Legacy Task ledger inputs

This task record tracks implementation and verification evidence for the
workspace contract governance normalization plan. WCGN-001 created the Stage
04 evidence record and baseline inventory, WCGN-002 established the
`_workspace` staging boundary, WCGN-003 audited and remediated frontmatter,
template, section, README, and cross-link drift, and WCGN-004 aligned the
CI path-filter control surface with the documented QA gates. WCGN-005 added
deterministic `_workspace` validator coverage, closed Stage 04 evidence, and
recorded reusable progress memory.

No live Kubernetes, Argo CD, Vault, ESO, cloud, GitHub remote, credential,
secret value, paid job, push, merge, pull request, or third-party mutation is
in scope for this task.

- **Parent Spec**: [../../03.specs/0020-workspace-contract-governance-normalization/spec.md](spec.md)
- **Parent Plan**: [../plans/2026-07-05-workspace-contract-governance-normalization.md](plan.md)
- **Task Template**: [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/document-authoring.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
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

### File Structure

| Path | Responsibility |
| --- | --- |
| `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md` | This implementation plan. |
| `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md` | Plan index and structure entry. |
| `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records` | Execution evidence, audit inventory, validation results, deferrals, and handoff. |
| `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records` | Task index and structure entry. |
| `.gitignore` | Ignore all `_workspace` scratch artifacts while allowing `_workspace/README.md`. |
| `_workspace/README.md` | Tracked boundary contract for temporary non-secret repo-support staging. |
| `README.md` | Root inventory entry for `_workspace` and boundary reminder for `secrets/`. |
| `docs/00.agent-governance/subagent-protocol.md` | Multi-agent scratch workspace rule and durable-output promotion boundary. |
| `docs/00.agent-governance/rules/documentation-protocol.md` | Document output routing and drift cleanup rule for `_workspace`. |
| `docs/00.agent-governance/rules/approval-boundaries.md` | Protected-surface boundary for scratch artifacts, secret risk, and cleanup escalation. |
| `docs/99.templates/support/documentation-contract.md` | Support contract surface table and validation boundary for `_workspace`. |
| `docs/99.templates/contracts/frontmatter.schema.json` | README/frontmatter-free exception notes for `_workspace/README.md`. |
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

### Detailed Tasks

> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.

### Task 1: Create Task Evidence and Baseline Inventory

**Files:**

- Create: `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
- Modify: `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
- Modify: `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md`
- Read: `docs/99.templates/templates/specs/task.template.md`
- Read: `docs/03.specs/0020-workspace-contract-governance-normalization/spec.md`
- Read: `docs/99.templates/README.md`
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
sed -n '1,220p' docs/99.templates/templates/specs/task.template.md
sed -n '1,460p' docs/03.specs/0020-workspace-contract-governance-normalization/spec.md
```

Expected: the task template shows `type: sdlc/task`; the spec shows
`VAL-SPC-020-001` through `VAL-SPC-020-010`.

- [ ] **Step 3: Create the task evidence document**

Create `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
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



### Legacy Task supplemental evidence

### Baseline Inventory

| Date | Command | Result Class |
| --- | --- | --- |
| 2026-07-05 | `git status --short --branch` | PASS; branch was `codex/workspace-engineering-audit-pack` and the working tree had no pre-existing changes. |
| 2026-07-05 | `sed -n '1,220p' docs/99.templates/templates/specs/task.template.md` | PASS; template frontmatter uses `type: sdlc/task`, `status: draft`, `owner: platform`, and the required Stage 04 task evidence structure. |
| 2026-07-05 | `sed -n '1,460p' docs/03.specs/0020-workspace-contract-governance-normalization/spec.md` | PASS; the parent spec defines VAL-SPC-020-001 through VAL-SPC-020-010. |
| 2026-07-05 | `find AGENTS.md CLAUDE.md GEMINI.md README.md _workspace .agents .claude .codex .github docs examples gitops infrastructure policy scripts secrets tests traefik -maxdepth 3 -print \| sort` | PASS; pre-edit target inventory returned 592 paths across root shims, agent adapters, GitHub controls, docs, examples, GitOps, infrastructure, policy, scripts, secrets, tests, and Traefik surfaces. |
| 2026-07-05 | `find _workspace -maxdepth 4 -type f -print \| sort` | PASS; no files were present under `_workspace` before implementation. |
| 2026-07-05 | `git check-ignore -v _workspace/probe.log` | PASS; `_workspace/probe.log` is ignored by `.gitignore:31:_workspace/`. |
| 2026-07-05 | `rg -n "^type: (prd\|ard\|adr\|spec\|plan\|task\|guide\|policy\|runbook\|incident\|postmortem\|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | PASS; no active simple `type` values matched. Command exited with no matches. |
| 2026-07-05 | `rg -n "Target: d""ocs/\|Use this ""template\|SNIPPET LIBRARY\|\\{Folder or Project Name\\}\|\\[Feature Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | PASS; pre-edit scan returned 50 matching lines across 23 files. Result class was Stage 99 template files plus scanner-command evidence in the active implementation plan; no active authored residue outside those classes was identified. |

Requested target inventory notes:

| Target | Status | Notes |
| --- | --- | --- |
| `AGENTS.md` | Present | Root Codex/GPT gateway. |
| `CLAUDE.md` | Present | Root Claude gateway. |
| `GEMINI.md` | Present | Root Gemini gateway. |
| `README.md` | Present | Root human-facing repository entrypoint. |
| `_workspace` | Present | Empty and fully ignored before WCGN-002. |
| `.agents` | Present | Shared agent asset owner. |
| `.claude` | Present | Claude provider adapter surface. |
| `.codex` | Present | Codex provider adapter surface. |
| `.github` | Present | GitHub-native control surface. |
| `docs` | Present | Canonical documentation taxonomy. |
| `examples` | Present | Sample and cloud example surfaces. |
| `gitops` | Present | Desired-state GitOps manifests. |
| `infrastructure` | Present | Local bootstrap and verification scripts. |
| `policy` | Present | Policy-as-code surface. |
| `scripts` | Present | Repository validation and helper scripts. |
| `secrets` | Present | Repository-local certificate fixture boundary; secret values were not inspected. |
| `tests` | Present | Repository test evidence boundary. |
| `traefik` | Present | Local Traefik route examples. |
| `DESIGN.md` | Absent | User-requested target; no canonical route currently exists. Do not create without a future approved design-doc contract. |

### Audit Findings

| Finding ID | Surface | Category | Current State | Action |
| --- | --- | --- | --- | --- |
| WCGN-AUD-001 | `DESIGN.md` | route | The requested target is absent, and current template routing has no canonical design-doc route. | Record absence only; do not create in this plan without future approved contract work. |
| WCGN-AUD-002 | `_workspace` | workspace | `_workspace` exists but contains no files before implementation; `_workspace/probe.log` is ignored by the current whole-directory ignore rule. | WCGN-002 owns contract and ignore-boundary changes. |
| WCGN-AUD-003 | `docs`, root shims, `.github`, `scripts` | frontmatter | Simple legacy `type` values returned no matches in the requested baseline scan. | Keep as baseline PASS for WCGN-003. |
| WCGN-AUD-004 | `docs/99.templates/**`, Stage 04 plan | template | Template residue scan returned only template files and scanner-command evidence in the current plan before this task record was created. | Keep templates as allowed; future scans may classify task evidence command literals as scanner evidence. |
| WCGN-AUD-005 | Stage 04 indexes | README | `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records` did not yet list this task record before WCGN-001. | Update the Task stage structure and document index in WCGN-001. |
| WCGN-AUD-006 | `docs`, root shims, `.github`, `scripts` | frontmatter | WCGN-003 frontmatter scan returned no simple un-namespaced `type` values. The broad metadata-key scan showed namespaced profiles and canonical key order across active routed frontmatter. | No frontmatter remediation required. |
| WCGN-AUD-007 | `docs`, root shims, `.github`, `scripts` | template / section | WCGN-003 template residue matches were limited to Stage 99 template files, scanner-command evidence, and explicit cleanup-rule or legacy-route headings. | No active authored template residue or deprecated related-document section needed removal. |
| WCGN-AUD-008 | README entrypoints | README | README inventory returned repository, workspace, docs, examples, GitOps, infrastructure, scripts, tests, and Traefik README files. The literal README duplication scan reported missing `.codex/README.md` and `.claude/README.md` operands because those provider README files do not exist; a focused rerun over existing operands found concise owner pointers, not duplicated Stage 00 or Stage 99 policy bodies. | No README body rewrite required. Do not create provider README files without a future route need. |
| WCGN-AUD-009 | `docs/90.references/data/agent-reference-index.md`, `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | route | Two active reference documents still used the old Stage 03 placeholder `docs/03.specs/<feature-id>/...` as current guidance. | Update both references to `docs/03.specs/<###-Numbering>-<feature-id>/...`. |
| WCGN-AUD-010 | Stage 00 rules, active Stage 03 specs/guardrails, Stage 99 templates, Stage 04 migration evidence, Stage 90 audits, progress memory | route / cross-link | Remaining route scan matches are current deny-route guardrails (`docs/superpowers/**`, `docs/api/**`), active Stage 03 spec or guardrail references that reject off-taxonomy paths or record approved numbering contracts, template examples that explicitly reject `docs/api/**`, scanner-command evidence, completed migration evidence for old PRD filenames, dated Stage 90 audit evidence, or dated progress memory. | Leave accepted historical, active spec, and guardrail evidence in place; do not rewrite completed migration records into false current-state history. |
| WCGN-AUD-011 | `.github/workflows/ci.yml`, `scripts/README.md`, `tests/README.md`, CI/QA guide | CI path filters | WCGN-004 scans showed the documented Tier A policy gate and tests README quality surface, but `changes.manifests` did not include `scripts/validate-policy-gates.sh` or `policy/**`, and `changes.repo_quality` did not include `tests/**`. | Add the missing path-filter patterns to `ci.yml`; no active `.github/ABOUT.md`, PR template, SECURITY, root README, scripts README, tests README, or CI/QA guide wording drift required remediation. |

### Remediation Evidence

| Date | Task | Change | Evidence |
| --- | --- | --- | --- |
| 2026-07-05 | WCGN-001 | Created this Stage 04 task evidence record from the canonical task template and parent spec/plan. | Frontmatter uses `type: sdlc/task`; required sections are present in the requested order. |
| 2026-07-05 | WCGN-001 | Updated `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records` with the new WCGN document index row and structure block entries for WCGN plus two already-indexed 2026-07-05 task files that were missing from the structure block. | README keeps `## Link Basis` and `## Related Documents`. |
| 2026-07-05 | WCGN-001 | Reviewed `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md`. | Existing plan structure and index already include `2026-07-05-workspace-contract-governance-normalization.md`; no edit was needed. |
| 2026-07-05 | WCGN-001 | Completed controller/spec/quality review follow-up. | WCGN-001 status is `Done`; the verification command list now includes every command claimed by validation evidence. |
| 2026-07-05 | WCGN-002 | Narrowed the `_workspace` ignore rule to ignore scratch while allowing the directory and `_workspace/README.md` to be tracked. | `git check-ignore -v _workspace/probe.log` returned `.gitignore:31:_workspace/*	_workspace/probe.log`; `git check-ignore -v _workspace/README.md` exited 1 with no output, recorded as NOT IGNORED. |
| 2026-07-05 | WCGN-002 | Created `_workspace/README.md` as the frontmatter-free checked-in contract and added the root README structure entry. | `git ls-files _workspace` returned only `_workspace/README.md` after staging the README. |
| 2026-07-05 | WCGN-002 | Aligned Stage 00 governance and Stage 99 support contracts with the `_workspace` staging boundary. | `git diff --check` returned no whitespace errors and `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |
| 2026-07-05 | WCGN-002 | Followed up on quality review by tightening dry-run scratch wording from logs to redacted, non-secret summaries. | `rg -n "Dry-run logs\|dry-run\|logs\|summaries" _workspace/README.md` no longer returns `Dry-run logs`; validation passed with `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .`. |
| 2026-07-05 | WCGN-003 | Updated active Stage 90 route guidance to the numbered Stage 03 placeholder. | `docs/90.references/data/agent-reference-index.md` now points feature-local Agent design to `docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md`; `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` now points the Stage 03 spec lifecycle to `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`. |
| 2026-07-05 | WCGN-003 | Reviewed folder README impact for the two Stage 90 reference edits. | `docs/90.references/data/README.md` and `docs/90.references/research/2026-07-04-wer/README.md` remain current because their index rows summarize document ownership and do not embed the old route placeholder. |
| 2026-07-05 | WCGN-003 | Recorded frontmatter, template residue, legacy section, README duplication, and route/cross-link scan classifications. | WCGN-003 status is `Done`; remaining noisy matches are documented as templates, explicit route guardrails, scanner-command evidence, migration evidence, Stage 90 audits, or progress memory. |
| 2026-07-06 | WCGN-004 | Aligned CI path filters with documented QA control surfaces. | `repo_quality` now runs for `tests/**`; `manifest-static` now runs for `scripts/validate-policy-gates.sh` and `policy/**`. The remaining requested scans classified `.github/ABOUT.md`, PR template, SECURITY, root README, scripts README, tests README, and CI/QA guide wording as aligned with the current workflow/script split. |
| 2026-07-06 | WCGN-005 | Added deterministic `_workspace` coverage to the repository quality gate and closed Stage 04 indexes plus progress memory. | The gate now requires tracked `_workspace/README.md`, ignored `_workspace/*` scratch, an unignored README, no tracked `_workspace` file except README, and no prohibited secret-risk wording in tracked `_workspace` paths. |

### Verification Commands

```bash
git status --short --branch
sed -n '1,220p' docs/99.templates/templates/specs/task.template.md
sed -n '1,460p' docs/03.specs/0020-workspace-contract-governance-normalization/spec.md
find AGENTS.md CLAUDE.md GEMINI.md README.md _workspace .agents .claude .codex .github docs examples gitops infrastructure policy scripts secrets tests traefik -maxdepth 3 -print | sort
find _workspace -maxdepth 4 -type f -print | sort
git check-ignore -v _workspace/probe.log
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "Target: d""ocs/|Use this ""template|SNIPPET LIBRARY|\\{Folder or Project Name\\}|\\[Feature Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
which rtk
/home/hy/.local/bin/rtk --version
/home/hy/.local/bin/rtk gain
git check-ignore -v _workspace/probe.log
git check-ignore -v _workspace/README.md
git ls-files _workspace
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/03.specs/0020-workspace-contract-governance-normalization/plan.md docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
git diff --cached --check
git add .gitignore _workspace/README.md README.md docs/00.agent-governance/subagent-protocol.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/approval-boundaries.md docs/99.templates/support/documentation-contract.md docs/99.templates/contracts/frontmatter.schema.json docs/99.templates/support/legacy-cleanup-rules.md docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
git diff --cached --check
git commit -m "docs(governance): Define workspace staging boundary"
rg -n "Dry-run logs|dry-run|logs|summaries" _workspace/README.md
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add _workspace/README.md docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
git diff --cached --check
git commit -m "docs(governance): Clarify workspace dry-run boundary"
bash scripts/validate-repo-quality-gates.sh .
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" docs/01.requirements docs/02.architecture docs/03.specs docs/03.specs docs/05.operations docs/90.references docs/98.archive docs/99.templates/support docs/00.agent-governance
rg -n "Target: d""ocs/|Use this ""template|SNIPPET LIBRARY|\\{Folder or Project Name\\}|\\[Feature Name\\]|command ""1|pytest ""tests|Example""Contract" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^## (Deprecated|Legacy|Related Refer""ences|Related Fold""ers|Related Fi""les|References|See Also|Links)\\b" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
find . -name README.md -not -path './.git/*' -not -path './.agents/*' -not -path './.agent-work/*' -print | sort
# Initial README duplication probe; expected to exit 2 because provider README
# operands do not exist in this repository.
rg -n "must|forbidden|required|canonical owner|contract owner|approval boundary|protected surface" README.md docs/**/README.md .codex/README.md .claude/README.md
# Focused existing-operand README duplication rerun.
rg -n "must|forbidden|required|canonical owner|contract owner|approval boundary|protected surface" README.md docs/**/README.md
rg -n "docs/superpowers|docs/api/|docs/01\\.requirements/YYYY-MM-DD-|docs/03\\.specs/<feature-id>" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add AGENTS.md CLAUDE.md GEMINI.md README.md .agents .claude .codex docs .github scripts docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
git diff --cached --check
git commit -m "docs(governance): Normalize document contract drift"
find .github/workflows scripts tests -maxdepth 2 -type f | sort
rg -n "validate-repo-quality-gates|validate-harness|check-secret-handling|validate-gitops-structure|validate-k8s-manifests|validate-policy-gates|git diff --check|kube-linter|zizmor" .github scripts tests docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md README.md
sed -n '1,220p' .github/workflows/ci.yml
sed -n '1,260p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
sed -n '1,240p' .github/ABOUT.md
rg -n "format|formatting|lint|linting|syntax|typecheck|test|QA|quality gate" README.md docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md scripts/README.md tests/README.md .github/PULL_REQUEST_TEMPLATE.md
rg -n "secret|credential|token|kubeconfig|SSH|auth|history|_workspace|protected surface|approval" README.md .github docs/00.agent-governance docs/05.operations scripts tests
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git diff --cached --check
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git ls-files _workspace
git check-ignore -v _workspace/probe.log
find _workspace -maxdepth 4 -type f | sort
rg -n "(token|secret|credential|auth|history|kubeconfig|ssh|password|diagnostic|profile|cache)" _workspace
rg -n "T""BD|TO""DO|\\{Feature ""Name\\}|\\[Feature ""Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "docs/superpowers|docs/api/" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "^type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs
git add scripts/validate-repo-quality-gates.sh docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records docs/03.specs/0020-workspace-contract-governance-normalization/plan.md docs/00.agent-governance/memory/progress.md
git diff --cached --check
```
### Overview

### Inputs

### Working Rules

### Task Table

### Baseline Inventory

### Audit Findings

### Remediation Evidence

### Verification Commands

### Validation Evidence

### Deferrals

### Related Documents
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
git add docs/03.specs/0020-workspace-contract-governance-normalization/plan.md docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
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
- Modify: `docs/99.templates/contracts/frontmatter.schema.json`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`

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

### Overview

### Audience

### Scope

#### In Scope

#### Out of Scope

### Structure

### How to Work in This Area

### Link Basis

### Related Documents
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

Update `docs/99.templates/contracts/frontmatter.schema.json` exceptions to state
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
git add .gitignore _workspace/README.md README.md docs/00.agent-governance/subagent-protocol.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/approval-boundaries.md docs/99.templates/support/documentation-contract.md docs/99.templates/contracts/frontmatter.schema.json docs/99.templates/support/legacy-cleanup-rules.md docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
git diff --cached --check
git commit -m "docs(governance): Define workspace staging boundary"
```

Expected: staged diff has no whitespace errors and the commit succeeds.

### Task 3: Audit and Remediate Frontmatter, Template, Section, README, and Cross-link Drift

**Files:**

- Modify as findings require: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `README.md`, `.agents/**`, `.claude/**`, `.codex/**`, `docs/**`
- Modify as evidence owner: `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
- Read: `docs/99.templates/contracts/frontmatter.schema.json`
- Read: `docs/99.templates/README.md`
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
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" docs/01.requirements docs/02.architecture docs/03.specs docs/03.specs docs/05.operations docs/90.references docs/98.archive docs/99.templates/support docs/00.agent-governance
```

Expected: simple un-namespaced `type` values return no active matches. For any
active match, replace the value with the profile in
`docs/99.templates/contracts/frontmatter.schema.json` and keep key order as
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
git add AGENTS.md CLAUDE.md GEMINI.md README.md .agents .claude .codex docs .github scripts docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
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
- Modify as evidence owner: `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
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
git add .github docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md scripts/README.md tests/README.md README.md docs/00.agent-governance docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records
git diff --cached --check
git commit -m "docs(qa): Align control surface validation contracts"
```

Expected: only files with actual WCGN-004 drift fixes are staged; staged diff
has no whitespace errors and the commit succeeds.

### Task 5: Add Validator Coverage, Close Evidence, and Record Memory

**Files:**

- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
- Modify: `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
- Modify: `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Read: `docs/99.templates/templates/governance/progress.template.md`

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

Update `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md` and
`docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records` so this plan and task are listed with
status `Done` only after final validation passes.

- [ ] **Step 6: Commit Task 5**

Run:

```bash
git add scripts/validate-repo-quality-gates.sh docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records docs/03.specs/0020-workspace-contract-governance-normalization/plan.md docs/00.agent-governance/memory/progress.md
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

### Legacy Task verification evidence

- **Test Commands**:
  - `git check-ignore -v _workspace/probe.log`
  - `git check-ignore -v _workspace/README.md`
  - `git ls-files _workspace`
  - `git diff --check`
  - `git diff --cached --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**: Runtime evals are not applicable for WCGN-001 through
  WCGN-005 because the completed work is documentation, governance evidence,
  CI path-filter alignment, and repository-static validation. Verification used
  repository-static quality gates and focused scans only.
- **Logs / Evidence Location**: This task record and the WCGN implementation
  commits.

### Validation Evidence

| Date | Check | Result |
| --- | --- | --- |
| 2026-07-05 | Branch and clean state | PASS; `git status --short --branch` returned only `## codex/workspace-engineering-audit-pack` before edits. |
| 2026-07-05 | Template and spec read | PASS; required task template and parent spec were read, including VAL-SPC-020-001 through VAL-SPC-020-010. |
| 2026-07-05 | Baseline scans | PASS; requested target inventory, `_workspace` baseline, ignore baseline, frontmatter scan, and template-residue scan were recorded as summarized above. |
| 2026-07-05 | Scope control | PASS; staged files are this task record and `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`. `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md` was reviewed, added by the requested staging command, and left unchanged because it was already current. |
| 2026-07-05 | Template heading validation | PASS; the repository quality gate initially required the task-template headings `## Suggested Types` and `## Verification Summary`; they were added and the quality gate passed. |
| 2026-07-05 | Working-tree whitespace check | PASS; `git diff --check` returned no whitespace errors. |
| 2026-07-05 | Repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |
| 2026-07-05 | Staged whitespace check | PASS; `git diff --cached --check` returned no whitespace errors after staging. |
| 2026-07-05 | Runtime tooling note | PASS with limitation recorded; `which rtk` returned `rtk not found`, `/home/hy/.local/bin/rtk --version` returned `rtk 0.34.3`, and `/home/hy/.local/bin/rtk gain` failed to initialize its tracking database, so validation commands ran directly without inspecting private runtime state. |
| 2026-07-05 | `_workspace` ignore probe | PASS; `git check-ignore -v _workspace/probe.log` returned `.gitignore:31:_workspace/*	_workspace/probe.log`. |
| 2026-07-05 | `_workspace` README unignore probe | PASS; `git check-ignore -v _workspace/README.md` exited 1 with no output, recorded as NOT IGNORED. |
| 2026-07-05 | `_workspace` tracked-file boundary | PASS; `git ls-files _workspace` returned only `_workspace/README.md`. |
| 2026-07-05 | WCGN-002 working-tree whitespace check | PASS; `git diff --check` returned no whitespace errors. |
| 2026-07-05 | WCGN-002 repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |
| 2026-07-05 | WCGN-002 quality review follow-up scan | PASS; `_workspace/README.md` now says `Redacted, non-secret dry-run summaries.` and no longer says `Dry-run logs.`. Remaining `logs` mentions are the prohibited `Secret-bearing local logs` out-of-scope boundary. |
| 2026-07-05 | WCGN-002 follow-up whitespace check | PASS; `git diff --check` returned no whitespace errors. |
| 2026-07-05 | WCGN-002 follow-up repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`. |
| 2026-07-05 | WCGN-003 initial repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed` before WCGN-003 scans or edits. |
| 2026-07-05 | WCGN-003 contract reads | PASS; read `frontmatter-schema.md`, `template-routing.md`, `documentation-contract.md`, and `legacy-cleanup-rules.md`; also read Stage 00 documentation protocol and route rules through the repo-local docs-stage-conformance workflow. |
| 2026-07-05 | WCGN-003 frontmatter scans | PASS; simple legacy `type` scan returned no matches. The metadata-key scan was reviewed for routed frontmatter and showed namespaced profile values with key order `title`, `type`, `status`, `owner`, `updated`. |
| 2026-07-05 | WCGN-003 template and section scans | PASS; matches were Stage 99 templates, scanner-command evidence, explicit cleanup rules, or legacy route headings. No active authored document retained template residue or deprecated related-document headings. |
| 2026-07-05 | WCGN-003 README scans | PASS with noted literal-command limitation; sorted README inventory completed. The literal duplication scan exited 2 only because `.codex/README.md` and `.claude/README.md` do not exist; focused rerun over existing README operands found concise owner pointers rather than duplicated policy bodies. |
| 2026-07-05 | WCGN-003 route and cross-link scans | PASS after remediation; active Stage 90 references were updated from `docs/03.specs/<feature-id>/...` to `docs/03.specs/<###-Numbering>-<feature-id>/...`. Remaining matches are current route-deny guardrails, templates, scanner-command evidence, completed migration evidence, Stage 90 audits, or progress memory. |
| 2026-07-05 | WCGN-003 working-tree whitespace check | PASS; `git diff --check` returned no whitespace errors after WCGN-003 edits. |
| 2026-07-05 | WCGN-003 repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed` after WCGN-003 edits. |
| 2026-07-06 | WCGN-004 requested scan inventory | PASS; scan found five GitHub workflow files, eight top-level shell scripts plus `scripts/README.md`, and `tests/README.md`. |
| 2026-07-06 | WCGN-004 control-surface scans | PASS with one remediation; scan evidence found a CI path-filter gap for `validate-policy-gates.sh`/`policy/**` and `tests/**`. All other reviewed QA, formatting, linting, syntax, automation, workflow, and security wording matched the current script/workflow split or explicit live-runtime boundary. |
| 2026-07-06 | WCGN-004 workflow remediation | PASS; `.github/workflows/ci.yml` now includes `tests/**` in `repo_quality` and `scripts/validate-policy-gates.sh` plus `policy/**` in `manifests`. |
| 2026-07-06 | WCGN-004 working-tree whitespace check | PASS; `git diff --check` returned no whitespace errors after WCGN-004 edits. |
| 2026-07-06 | WCGN-004 repository quality gate | PASS; `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed` after WCGN-004 edits. |
| 2026-07-06 | WCGN-004 staged whitespace check | PASS; `git diff --cached --check` returned no whitespace errors after staging the WCGN-004 files. |
| 2026-07-06 | WCGN-004 runtime tooling note | PASS with limitation recorded; `which rtk` returned `rtk not found`, `/home/hy/.local/bin/rtk --version` returned `rtk 0.34.3`, and `/home/hy/.local/bin/rtk gain` failed to initialize its tracking database, so validation commands ran directly without inspecting private runtime state. |
| 2026-07-06 | WCGN-004 independent spec review | PASS; reviewer verified WCGN-004 status, commit scope, CI path-filter coverage, no validator edits, and no live/runtime or external mutation claims. |
| 2026-07-06 | WCGN-005 validator coverage | PASS; `scripts/validate-repo-quality-gates.sh` now validates the `_workspace` README, scratch ignore, README unignore, tracked-file boundary, and prohibited tracked-path wording. |
| 2026-07-06 | WCGN-005 validator behavior | PASS; `git diff --check` returned no whitespace errors, `bash scripts/validate-repo-quality-gates.sh .` returned `[PASS] repository quality gates passed`, `git ls-files _workspace` returned only `_workspace/README.md`, and `git check-ignore -v _workspace/probe.log` returned `.gitignore:31:_workspace/*	_workspace/probe.log`. |
| 2026-07-06 | WCGN-005 focused `_workspace` scans | PASS with classification; `find _workspace -maxdepth 4 -type f` returned only `_workspace/README.md`. The prohibited-word scan matched only `_workspace/README.md` contract language, not tracked scratch artifacts. |
| 2026-07-06 | WCGN-005 placeholder, route, and type scans | PASS with classification; placeholder matches are README explanatory text, validator rationale checks, Stage 99 templates, and scanner-command evidence. Route matches are active route-deny guardrails, explicit task/plan evidence, templates, Stage 90 policy text, or progress memory. Simple un-namespaced `type` values returned no active matches. |

### Deferrals

- No WCGN implementation deferrals remain in repository-static scope.
- Live GitHub Actions execution, optional installed-tool checks such as
  `kube-linter`, `zizmor`, `actionlint`, or `conftest`, and live Kubernetes,
  Argo CD, Vault, ESO, cloud, provider, credential, or secret-value validation
  remain out of scope. Future work may trigger them only through the owning
  CI/toolchain or operator-approved runtime workflow.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Broad target list creates unrelated churn | High | Patch only current-contract drift with a clear owner; record ambiguous findings as deferrals in Stage 04 evidence. |
| `_workspace` becomes a secret sink | High | Track only `_workspace/README.md`, ignore scratch by default, and add validator checks for tracked prohibited path patterns. |
| README files accumulate governance bodies | Medium | Keep README changes to inventory and routing summaries; move rules to Stage 00 or Stage 99 support owners. |
| Validator change becomes too large | Medium | Add only deterministic `_workspace` checks near existing tracked-file checks; keep unrelated validator refactors out of scope. |
| External/live validation is mistaken for repo-static validation | High | Keep live runtime, provider, GitHub remote, credential, and secret-value actions out of scope and record this in task evidence. |

### Agent Rollout & Evaluation Gates

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

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `WCGN-001 through WCGN-005` is limited to these Workspace Contract Governance Normalization owners and Task-Table surfaces:
  - `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
  - `docs/03.specs/0020-workspace-contract-governance-normalization/spec.md`
  - `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md`
  - `docs/99.templates/templates/specs/task.template.md`
  - `docs/99.templates/README.md`
  - `docs/00.agent-governance/rules/documentation-protocol.md`
  - `_workspace/README.md`
  - `_workspace/probe.log`
  - `docs/99.templates/**`
  - `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Workspace Contract Governance Normalization work items and linked evidence owners.
- **Approval Required**: Human approval is required before Workspace Contract Governance Normalization protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Workspace Contract Governance Normalization outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git check-ignore -v _workspace/probe.log`
  - `git check-ignore -v _workspace/README.md`
  - `git ls-files _workspace`
  - `git diff --check`
- **Live Validation**: DEFER — Workspace Contract Governance Normalization is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Workspace Contract Governance Normalization; do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Workspace Contract Governance Normalization change set for `WCGN-001 through WCGN-005` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Workspace Contract Governance Normalization evidence remains in:
  - `docs/03.specs/0020-workspace-contract-governance-normalization/README.md#task-records`
  - `docs/03.specs/0020-workspace-contract-governance-normalization/spec.md`
  - `docs/03.specs/0020-workspace-contract-governance-normalization/plan.md`
  - `docs/99.templates/templates/specs/task.template.md`
  - `docs/99.templates/README.md`
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

## Traceability

- **Spec**: [../../03.specs/0020-workspace-contract-governance-normalization/spec.md](spec.md)
- **Task**: [../tasks/2026-07-05-workspace-contract-governance-normalization.md](README.md#task-records)
- **Template Documentation Contract**: [../../99.templates/support/documentation-contract.md](../../99.templates/README.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/README.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/document-authoring.md)
- **Approval Boundaries**: [../../00.agent-governance/rules/approval-boundaries.md](../../00.agent-governance/rules/approval-boundaries.md)
- **Repository Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)

### Legacy Task traceability

- **Spec**: [../../03.specs/0020-workspace-contract-governance-normalization/spec.md](spec.md)
- **Plan**: [../plans/2026-07-05-workspace-contract-governance-normalization.md](plan.md)
- **Task Template**: [../../99.templates/templates/specs/task.template.md](../../99.templates/templates/specs/task.template.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/document-authoring.md)
- **Task Stage Index**: [./README.md](../../99.templates/templates/specs/task.template.md)
