---
title: 'Workspace Document Governance Hardening Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-04
---

# Workspace Document Governance Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden workspace document type contracts, provider entrypoints,
README boundaries, and CI/QA documentation without breaking the current
repo-static quality gates.

**Architecture:** Execute the work as staged governance hardening: inventory
first, then core template and Stage 00 contracts, then provider entrypoints,
then workspace-wide document application, then final validator evidence. Each
stage produces a bounded commit and evidence in the paired Task record.

**Tech Stack:** Markdown, YAML, shell, Python-backed repository validators,
GitHub Actions, Kubernetes/GitOps manifests, Codex/Claude/Gemini provider
entrypoint files.

---

## Overview

This plan implements the approved
[Workspace Document Governance Hardening Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md).
It keeps the current passing repository quality gate as the baseline and
converts deterministic drift into either fixed documents or validator-backed
checks.

## Context

The repository already has a structured documentation taxonomy, template
routing model, Stage 00 agent governance, provider-specific shims, and
repo-static CI/QA gates. The new work combines three requested scopes:

- Workspace-wide audit and categorization.
- Core contract and governance hardening.
- Provider entrypoint alignment for AGENTS, Claude, Codex, and Gemini surfaces.

The current `bash scripts/validate-repo-quality-gates.sh .` baseline passes.
Implementation must preserve that baseline after every logical commit.

## File Structure

| Path | Responsibility in this plan |
| --- | --- |
| `docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md` | Durable audit inventory for frontmatter, README, provider, CI/QA, and workspace-wide drift classes found during Task 1. |
| `docs/90.references/audits/README.md` | Audit index registration for the new audit report if the report is created. |
| `docs/99.templates/support/*.md` | Current template support contract, frontmatter schema, SDLC/common governance, routing, and legacy cleanup owner. |
| `docs/99.templates/templates/**` | Template forms that must match support contracts without carrying long governance bodies. |
| `docs/00.agent-governance/**/*.md` | Agent-facing governance, provider routing, protected-surface rules, and provider capability boundaries. |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Thin provider gateway shims that point to Stage 00 and provider runtime overlays. |
| `.agents/**`, `.claude/**`, `.codex/**` | Shared and provider-specific agent runtime surfaces. |
| `.github/ABOUT.md`, `.github/workflows/*.yml`, `.github/PULL_REQUEST_TEMPLATE.md` | CI/QA and repository automation documentation surfaces. |
| `README.md`, `docs/**/README.md`, `examples/**/README.md`, `gitops/**/README.md`, `infrastructure/**/README.md`, `scripts/README.md`, `tests/README.md`, `traefik/README.md` | README entrypoints that must remain frontmatter-free and avoid duplicating contract bodies. |
| `scripts/validate-repo-quality-gates.sh` | Deterministic enforcement surface for document routing, frontmatter, stale wording, provider, and CI/QA drift checks. |
| `docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md` | Task evidence, status, validation results, and handoff notes for this plan. |
| `docs/00.agent-governance/memory/progress.md` | Repo-changing progress ledger entry. |

## Goals & In-Scope

- **Goals**:
  - Produce a repo-backed audit inventory before broad edits.
  - Align template support contracts, template forms, Stage 00 rules, and the
    validator.
  - Align provider entrypoints as thin shims over shared Stage 00 governance.
  - Apply topic-specific document fixes across README and authored document
    surfaces.
  - Record CI/CD and QA boundaries using official sources and current workflow
    evidence.
  - Keep every logical unit commitable and validated.
- **In Scope**:
  - Repo-static documentation, governance, CI/QA, provider, and validator
    surfaces listed in the Spec.
  - Read-only external source verification from official documentation.
  - Sub-agent review for audit, contract, provider, workspace, and final
    quality stages.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Live cluster mutation.
  - Secret value inspection.
  - External account, publishing, pushing, or merging actions.
  - Rewriting historical evidence where a Tombstone, current overlay, or
    deferred finding is safer.
- **Out of Scope**:
  - Creating a new `docs/` top-level folder.
  - Adding deploy CD to `.github/workflows`.
  - Promoting example cloud docs into active platform contracts.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Baseline audit inventory | `docs/90.references/audits/*`, Task evidence | VAL-WDGH-001, VAL-WDGH-007 | Audit report or task evidence records observed drift classes and no unsupported docs folders are introduced. |
| PLN-002 | Core contract hardening | `docs/99.templates/**`, `docs/00.agent-governance/**`, validator | VAL-WDGH-002, VAL-WDGH-005 | Template routing, frontmatter schema, Stage 00 routing, and validator describe the same rules. |
| PLN-003 | Provider entrypoint hardening | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/**`, `.claude/**`, `.codex/**` | VAL-WDGH-003 | Provider shims stay thin and provider-specific behavior remains in provider docs/runtime overlays. |
| PLN-004 | Workspace document application | README/authored docs under requested workspace surfaces | VAL-WDGH-004, VAL-WDGH-005, VAL-WDGH-006 | Topic-specific fixes remove duplicated contract prose, legacy residue, and metadata drift without breaking gates. |
| PLN-005 | Validator and CI/QA evidence finalization | `scripts/validate-repo-quality-gates.sh`, `.github/ABOUT.md`, operation guide, Task/progress | VAL-WDGH-006, VAL-WDGH-007, VAL-WDGH-008 | Local gates pass and final review finds no blocking governance contradiction. |

## Task Execution Details

### Task 1: Baseline Audit Inventory

**Files:**

- Create if durable findings exist: `docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md`
- Modify if the audit report is created: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Capture baseline status**

Run:

```bash
git status --short --branch
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

- The branch is not `main`.
- `git diff --check` prints no output.
- Repository quality gate prints `[PASS] repository quality gates passed`.

- [ ] **Step 2: Capture tracked file inventory**

Run:

```bash
git ls-files '*.md' '*.yaml' '*.yml' '*.graphql' '*.proto' | wc -l
git ls-files '*.md' | wc -l
find docs/99.templates/templates -maxdepth 5 -type f | sort
find docs/99.templates/support -maxdepth 2 -type f | sort
find docs/00.agent-governance -maxdepth 3 -type f | sort
```

Expected:

- Counts and file lists are recorded in Task evidence.
- No `docs/superpowers` or other unsupported `docs/` top-level folder appears.

- [ ] **Step 3: Scan frontmatter and README surfaces**

Run:

```bash
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" \
  README.md AGENTS.md CLAUDE.md GEMINI.md docs examples gitops infrastructure scripts tests traefik .github .agents .claude .codex
rg -n "^## (Related Folders|Related Files|References|See Also|Links|Deprecated|Legacy)$" \
  README.md docs examples gitops infrastructure scripts tests traefik .github .agents .claude .codex
```

Expected:

- README files remain frontmatter-free.
- Any current-contract README heading drift is recorded as a specific file and
  heading.
- Historical matches inside `docs/00.agent-governance/memory/progress.md` are
  treated as evidence, not active contract drift.

- [ ] **Step 4: Scan provider and CI/QA surfaces**

Run:

```bash
rg -n "AGENTS.md|CLAUDE.md|GEMINI.md|hooks|subagent|multi_agent|provider|Codex|Claude|Gemini" \
  AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex docs/00.agent-governance
rg -n "workflow|CI|QA|pre-commit|repo-quality-static|manifest-static|branch-policy|Scorecard|SLSA|zizmor|actionlint" \
  .github docs scripts tests README.md
```

Expected:

- Provider-specific claims are traceable to provider docs or runtime overlays.
- CI/QA claims match `.github/workflows/ci.yml`, `.github/ABOUT.md`,
  `scripts/README.md`, `tests/README.md`, and the CI/CD QA guide.

- [ ] **Step 5: Write audit evidence**

If the scans find durable findings, create
`docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md`
with this frontmatter and section structure:

```markdown
---
title: 'Reference: Workspace Document Governance Hardening Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-03
---

# Reference: Workspace Document Governance Hardening Audit

## Overview

This audit records repo-static findings for workspace document governance
hardening.

## Reference Type

- audit

## Authority Boundary

This document owns observed audit evidence and remediation routing. Active
execution policy remains in Stage 00 governance, template support contracts,
and repository validators.

## Findings

| Finding ID | Surface | Evidence | Decision | Routed Task |
| --- | --- | --- | --- | --- |

## Implementation Checklist

| Item | Owner Surface | Action | Status |
| --- | --- | --- | --- |

## Review and Freshness

- Review date: 2026-07-03.
- Refresh trigger: rerun when template routing, provider entrypoints, CI/QA
  workflows, or validator contracts change.

## Sources

- Repository scans from tracked files.
- Official source references listed in the parent Spec.

## Related Documents

- [Parent Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- [Parent Plan](../../04.execution/plans/2026-07-03-workspace-document-governance-hardening.md)
- [Task Evidence](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md)
```

If the scans find no durable findings beyond items already represented in the
Task table, do not create the audit report. Instead, record "No separate Stage
90 audit report was created because all findings are executable Task evidence"
in the Task record.

- [ ] **Step 6: Validate and commit audit inventory**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/90.references/audits docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(audit): Record workspace document governance baseline"
```

### Task 2: Core Contract Hardening

**Files:**

- Modify as needed: `docs/99.templates/support/documentation-contract.md`
- Modify as needed: `docs/99.templates/support/frontmatter-schema.md`
- Modify as needed: `docs/99.templates/support/template-routing.md`
- Modify as needed: `docs/99.templates/support/sdlc-governance.md`
- Modify as needed: `docs/99.templates/support/common-documentation-governance.md`
- Modify as needed: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify as needed: `docs/99.templates/templates/**`
- Modify as needed: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify as needed: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify as needed: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify as needed: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Compare route maps**

Run:

```bash
rg -n "Template-Folder Mapping|Current Route Map|required_stage_templates|template_expected_types|template_locations" \
  docs/99.templates/README.md docs/99.templates/support scripts/validate-repo-quality-gates.sh
```

Expected:

- Every structural route in `docs/99.templates/README.md` appears in
  `docs/99.templates/support/template-routing.md`.
- Every Markdown route has a matching validator mapping.
- `harness-task-contract.template.md` remains supplemental and does not become
  a second structural route for `docs/04.execution/tasks/*.md`.

- [ ] **Step 2: Compare frontmatter profiles**

Run:

```bash
rg -n "sdlc/prd|sdlc/ard|sdlc/adr|sdlc/spec|sdlc/plan|sdlc/task|sdlc/guide|sdlc/policy|sdlc/runbook|sdlc/incident|sdlc/postmortem|content/reference|content/archive-tombstone|governance/template-support|governance/reference|governance/memory" \
  docs/99.templates/support/frontmatter-schema.md docs/99.templates/templates scripts/validate-repo-quality-gates.sh
```

Expected:

- Template frontmatter, support schema, and validator expected types agree.
- README and progress templates remain frontmatter-free.
- Native OpenAPI, GraphQL, and protobuf templates remain native to their
  formats.

- [ ] **Step 3: Apply core contract fixes**

Use the following rules while editing:

- Keep reusable rules in support or Stage 00 documents, not in README bodies.
- Keep template forms short and document-type-specific.
- Replace active legacy route, key, value, and section wording with current
  contract wording.
- Preserve historical evidence in completed plans, tasks, and progress entries
  when it is clearly historical.
- Add validator coverage only for deterministic drift classes with low
  false-positive risk.

Expected edited surfaces:

- Support docs describe current-state contracts.
- Stage 00 routing docs point to support contracts instead of copying entire
  template support bodies.
- Validator mappings match support docs.

- [ ] **Step 4: Focused contract scans**

Run:

```bash
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md
template_instruction='Use this'
template_instruction="${template_instruction} template"
target_comment='Target:'
target_comment="${target_comment} docs/"
rg -n "operations-template|type: operations|owner: deprecated owner value|deprecated README heading|${template_instruction}|${target_comment}" docs README.md AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex scripts
rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support
```

Expected:

- No active flat template route references remain.
- No active legacy frontmatter/type/owner/template instruction residue remains.
- No stale migration-phase wording remains in support contracts.
- Historical evidence matches are recorded as allowed evidence, not active
  contract drift.

- [ ] **Step 5: Validate and commit core contract hardening**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/99.templates docs/00.agent-governance scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(governance): Harden document contract surfaces"
```

### Task 3: Provider Entrypoint Hardening

**Files:**

- Modify as needed: `AGENTS.md`
- Modify as needed: `CLAUDE.md`
- Modify as needed: `GEMINI.md`
- Modify as needed: `.agents/GEMINI.md`
- Modify as needed: `.agents/hooks.json`
- Modify as needed: `.agents/agents/**`
- Modify as needed: `.agents/rules/**`
- Modify as needed: `.agents/skills/**`
- Modify as needed: `.agents/workflows/**`
- Modify as needed: `.claude/CLAUDE.md`
- Modify as needed: `.claude/settings.json`
- Modify as needed: `.claude` runtime hook adapter files when current Stage 00
  hook routing evidence requires it.
- Modify as needed: `.codex/CODEX.md`
- Modify as needed: `.codex/hooks.json`
- Modify as needed: `.codex/agents/**`
- Modify as needed: `docs/00.agent-governance/providers/*.md`
- Modify as needed: `docs/00.agent-governance/common-governance.md`
- Modify as needed: `docs/00.agent-governance/harness-catalog.md`
- Modify as needed: `docs/00.agent-governance/subagent-protocol.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Inspect provider shim pointers**

Run:

```bash
sed -n '1,120p' AGENTS.md
sed -n '1,120p' CLAUDE.md
sed -n '1,120p' GEMINI.md
sed -n '1,180p' .agents/GEMINI.md
sed -n '1,180p' .claude/CLAUDE.md
sed -n '1,180p' .codex/CODEX.md
```

Expected:

- Root shims point to `docs/00.agent-governance/rules/bootstrap.md`,
  provider-specific Stage 00 provider notes, provider runtime baseline files,
  and `RTK.md`.
- Shared assets are described as `.agents/skills`, `.agents/workflows`, and
  `.agents/output-styles`.
- Provider-specific differences remain in provider docs or runtime overlays.

- [ ] **Step 2: Inspect runtime asset topology**

Run:

```bash
find .agents -maxdepth 3 -type f -o -type l | sort
find .claude -maxdepth 3 -type f -o -type l | sort
find .codex -maxdepth 3 -type f -o -type l | sort
rg -n "shared asset|canonical adapter|mirror|symlink|hooks|multi_agent|subagent|skills|workflows|output-styles" \
  .agents .claude .codex docs/00.agent-governance
```

Expected:

- Documentation matches actual files and symlinks.
- Claims about hooks are provider-accurate: Claude hook behavior stays
  Claude-specific, Codex enforcement stays instruction/sandbox/hook-json
  wrapper based, and Gemini context behavior stays GEMINI-specific.

- [ ] **Step 3: Apply provider fixes**

Use the following rules while editing:

- Root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` stay thin.
- Stage 00 provider docs own provider differences.
- `.agents` owns shared assets.
- `.claude` and `.codex` expose provider adapters and symlink or point to
  shared assets where appropriate.
- Provider docs must not claim capability parity when the runtime differs.

Expected edited surfaces:

- Provider entrypoints agree with the Stage 00 canonical adapter model.
- No provider shim duplicates full common governance.
- No stale provider-specific local hook path appears as an active current
  command.

- [ ] **Step 4: Validate provider surface**

Run:

```bash
rg -n "CLAUDE.md|GEMINI.md|AGENTS.md|CODEX.md|hooks.json|skills|workflows|output-styles" \
  AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex docs/00.agent-governance
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

- The grep output supports the provider topology recorded in Task evidence.
- Whitespace and repository quality gates pass.

- [ ] **Step 5: Commit provider entrypoint hardening**

Commit:

```bash
git add AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex docs/00.agent-governance docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(providers): Align agent entrypoint contracts"
```

### Task 4: Workspace Document Application

**Files:**

- Modify as needed: `README.md`
- Modify as needed: `DESIGN.md` if present
- Modify as needed: `.github/ABOUT.md`
- Modify as needed: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify as needed: `docs/**/*.md`
- Modify as needed: `examples/**/*.md`
- Modify as needed: `gitops/**/*.md`
- Modify as needed: `infrastructure/**/*.md`
- Modify as needed: `policy/**/*.md`
- Modify as needed: `scripts/README.md`
- Modify as needed: `tests/README.md`
- Modify as needed: `traefik/README.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Identify active README section drift**

Run:

```bash
git ls-files '*README.md' | sort
rg -n "^## " README.md .github docs examples gitops infrastructure policy scripts tests traefik .agents .claude .codex
```

Expected:

- Every README has the base entrypoint sections required by the validator.
- Any duplicate-purpose sections are listed with path and heading.
- Contract bodies that belong in support or governance docs are routed out of
  README files.

- [ ] **Step 2: Identify active authored frontmatter drift**

Run:

```bash
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references docs/98.archive docs/99.templates/support
```

Expected:

- Authored Markdown files under canonical stages have only the required
  frontmatter keys for their profile.
- README and native contract files remain frontmatter-free.

- [ ] **Step 3: Apply safe document fixes**

Use these bounded edit rules:

- Do not paste a template body into an authored document.
- Do not invent content beyond the document topic.
- Delete or merge duplicate-purpose sections only when the remaining section
  preserves the document's topic-specific information.
- Move reusable rule prose into `docs/99.templates/support/**` or
  `docs/00.agent-governance/**`.
- Keep examples as examples; do not describe them as active desired state.
- If a document contradicts current implementation and cannot be safely
  updated in place, route it to a follow-up archive decision instead of
  rewriting history.

Expected edited surfaces:

- README files remain concise entrypoints.
- Authored docs use type-appropriate metadata and topic-specific sections.
- CI/CD and QA references match actual workflow/script boundaries.

- [ ] **Step 4: Scan for residue**

Run:

```bash
template_instruction='Use this'
template_instruction="${template_instruction} template"
target_comment='Target:'
target_comment="${target_comment} docs/"
incomplete_marker='TB'
incomplete_marker="${incomplete_marker}D"
todo_marker='TO'
todo_marker="${todo_marker}DO"
rg -n "${template_instruction}|${target_comment}|${incomplete_marker}|${todo_marker}|deprecated README heading|owner: deprecated owner value|type: operations|operations-template" \
  README.md AGENTS.md CLAUDE.md GEMINI.md .github docs examples gitops infrastructure policy scripts tests traefik .agents .claude .codex
rg -n "direct push|force push|kubectl apply|kubectl patch|argocd app sync|vault kv put|secret value" \
  README.md docs examples gitops infrastructure policy scripts tests traefik .github .agents .claude .codex
```

Expected:

- Active template residue is removed.
- Any high-risk command mention is either a prohibited boundary, a runbook
  approval path, or a historical evidence note.

- [ ] **Step 5: Validate and commit workspace document application**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add README.md DESIGN.md .github docs examples gitops infrastructure policy scripts tests traefik .agents .claude .codex docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(workspace): Apply document governance profiles"
```

If `DESIGN.md` is absent, omit it from `git add`.

### Task 5: Validator, CI/QA Evidence, and Final Review

**Files:**

- Modify as needed: `scripts/validate-repo-quality-gates.sh`
- Modify as needed: `.github/ABOUT.md`
- Modify as needed: `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`
- Modify: `docs/04.execution/plans/2026-07-03-workspace-document-governance-hardening.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Add deterministic validator checks for accepted drift classes**

Only add checks for drift classes that Task 1 through Task 4 prove are
deterministic. Use this pattern inside
`scripts/validate-repo-quality-gates.sh` when adding active-document text
checks:

```python
active_doc_roots = [
    root / "README.md",
    root / "AGENTS.md",
    root / "CLAUDE.md",
    root / "GEMINI.md",
    root / "docs",
    root / "examples",
    root / "gitops",
    root / "infrastructure",
    root / "policy",
    root / "scripts",
    root / "tests",
    root / "traefik",
]
```

Expected:

- Checks are path-scoped.
- Historical progress entries and archive Tombstones are not falsely rejected.
- Failure messages name the path and drift class.

- [x] **Step 2: Reconcile CI/QA documentation**

Compare:

```bash
sed -n '1,240p' .github/workflows/ci.yml
sed -n '1,220p' .github/ABOUT.md
sed -n '1,240p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
sed -n '1,240p' scripts/README.md
sed -n '1,200p' tests/README.md
```

Expected:

- `ci.yml` remains the required QA gate.
- `generate-changelog.yml`, `labeler.yml`, `greetings.yml`, and `stale.yml`
  are documented as maintenance or release-evidence automation, not QA gates.
- Local equivalents for repo-quality and manifest-static checks are accurate.
- Documentation cites official basis from the parent Spec where external
  claims are made.

- [x] **Step 3: Run full local validation bundle**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
```

If GitOps, infrastructure, policy, examples YAML, secrets, tests, or Traefik
surfaces changed, also run:

```bash
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

Expected:

- Required commands pass.
- Optional tooling skips, if any, are recorded as limitations rather than
  hidden success.

- [x] **Step 4: Prepare final sub-agent review handoff**

Task 5 implementer boundary: the parent agent dispatches the independent final
sub-agent review after the Task 5 commit. Prepare the evidence for this
read-only reviewer brief:

```text
Review the workspace document governance hardening branch. Verify that:
1. The implementation satisfies docs/03.specs/013-workspace-document-governance-hardening/spec.md.
2. docs/99.templates support contracts, templates, Stage 00 routing docs, and scripts/validate-repo-quality-gates.sh agree.
3. AGENTS.md, CLAUDE.md, GEMINI.md, .agents, .claude, and .codex remain thin provider surfaces over Stage 00 governance.
4. README files are frontmatter-free and do not duplicate support/governance contract bodies.
5. CI/QA documentation matches .github/workflows and scripts.
6. git diff --check and bash scripts/validate-repo-quality-gates.sh . pass.
Return READY or list findings with file/line references.
```

Expected: parent agent can dispatch the reviewer with complete local evidence;
reviewer returns READY or findings are remediated and re-reviewed.

- [x] **Step 5: Complete final evidence and commit**

Update the Plan completion checklist, Task status/evidence, and progress entry.

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add scripts/validate-repo-quality-gates.sh .github docs scripts tests README.md AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex examples gitops infrastructure policy traefik
git commit -m "docs(validation): Finalize workspace governance hardening"
```

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Baseline | Whitespace and patch hygiene | `git diff --check` | No output and exit `0`. |
| VAL-PLN-002 | Repo quality | Documentation, template, provider, CI/QA, and archive gates | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed`. |
| VAL-PLN-003 | Harness | Full repo-static harness bundle | `bash scripts/validate-harness.sh` | Exits `0`; limitations are recorded. |
| VAL-PLN-004 | Manifest bundle | GitOps and manifest checks when YAML surfaces change | `bash infrastructure/tests/verify-contracts-static.sh` plus manifest scripts | All commands exit `0`. |
| VAL-PLN-005 | Review | Final independent review | Sub-agent reviewer prompt in Task 5 | Parent-agent reviewer handoff is ready; reviewer returns READY or all findings are fixed and re-reviewed. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Workspace-wide edits create noisy diffs | High | Audit first, edit by surface, commit each logical unit after gates pass. |
| Validator false positives reject historical evidence | High | Scope checks to active docs or add explicit historical allow-lists with comments. |
| Provider docs imply false capability parity | Medium | Keep common policy in Stage 00 and provider differences in provider-specific docs. |
| README files become contract dumping grounds | Medium | Route reusable rules to support or Stage 00 docs and keep README as entrypoint inventory. |
| External source claims drift over time | Medium | Prefer official sources and record freshness boundaries in reference or task evidence. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Repository-static validation commands in the
  Verification Plan.
- **Sandbox / Canary Rollout**: Not applicable; changes are documentation and
  repository validation only.
- **Human Approval Gate**: Required before live runtime checks, external
  mutations, push, merge, PR creation, or destructive cleanup.
- **Rollback Trigger**: Revert the latest logical commit if repository quality
  gates fail and the failure cannot be fixed within the task scope.
- **Prompt / Model Promotion Criteria**: Not applicable; provider prompts and
  policy documents must remain governed by Stage 00.

## Completion Criteria

- [x] Audit inventory is recorded in Task evidence or Stage 90 audit report.
- [x] Core template, frontmatter, routing, Stage 00, and validator contracts
  agree.
- [x] Provider entrypoints are thin and provider-specific behavior is routed to
  provider docs or runtime overlays.
- [x] Workspace README and authored docs have type-appropriate sections and
  frontmatter.
- [x] CI/CD and QA documentation matches current workflows and scripts.
- [x] Final `git diff --check` passes.
- [x] Final `bash scripts/validate-repo-quality-gates.sh .` passes.
- [x] Final sub-agent review handoff is ready for parent-agent dispatch.

## Related Documents

- [Parent Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- [Task Evidence](../tasks/2026-07-03-workspace-document-governance-hardening.md)
- [Template Documentation Contract](../../99.templates/support/documentation-contract.md)
- [Template Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [GitHub Configuration Hub](../../../.github/ABOUT.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
