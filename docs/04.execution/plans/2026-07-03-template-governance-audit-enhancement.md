---
title: 'Template Governance Audit Enhancement Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-07-03
---

# Template Governance Audit Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit the current `docs/99.templates/**` governance model and apply
targeted improvements that make template routing, frontmatter contracts, and
validation harder to drift.

**Architecture:** The work stays repo-static and documentation-first. Stage 04
Plan and Task records own execution tracking, `docs/99.templates/support/**`
owns template-specific contracts, Stage 00 owns agent-facing routing policy,
and `scripts/validate-repo-quality-gates.sh` owns deterministic enforcement.

**Tech Stack:** Markdown, Bash, Python embedded in
`scripts/validate-repo-quality-gates.sh`, `rg`, `find`, `git diff`, and local
Git commits.

---

## Overview

This document defines the implementation plan for the approved follow-up audit
and enhancement pass over the template governance system. It does not repeat
the completed template migration. It verifies the current implementation,
records bounded findings, remediates clear drift, and adds validation only for
stable repo-local contracts.

## Context

The previous migration separated copy-ready template forms under
`docs/99.templates/templates/**` from support contracts under
`docs/99.templates/support/**`. The follow-up spec identified a verification
layer that should confirm route coverage, frontmatter profile consistency,
support-vs-README separation, legacy cleanup, authoring safety, and validator
alignment.

Current quick inspection shows three concrete improvement candidates:

- Some support contract wording still describes the completed migration in
  phase-oriented terms instead of current steady-state rules.
- `harness-task-contract.template.md` is a specialized Task starter, but some
  support route tables can make it look like a second structural route for
  `docs/04.execution/tasks/*.md`.
- The quality gate enforces many template rules, but it can add a narrow guard
  against stale migration-phase wording inside active support contracts.

## Goals & In-Scope

- **Goals**:
  - Record an auditable Stage 04 finding ledger for the follow-up.
  - Clarify current support contracts without changing the template taxonomy.
  - Keep `harness-task-contract.template.md` documented as a supplemental
    Task starter, not an overlapping structural route.
  - Add deterministic validation for support-contract drift where the false
    positive risk is low.
  - Re-run route, residue, frontmatter, README, and incident-bundle checks.
- **In Scope**:
  - `docs/99.templates/**`.
  - Template-related Stage 00 rules.
  - `scripts/validate-repo-quality-gates.sh`.
  - `docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`.
  - Stage README indexes and `docs/00.agent-governance/memory/progress.md`.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Re-migrate the template tree.
  - Create a new documentation taxonomy.
  - Rewrite authored documents whose topic content already matches the
    current contract.
  - Add synthetic incident, PRD, or template placeholder documents.
- **Out of Scope**:
  - Live cluster, Vault, ArgoCD, GitHub remote, paid job, or cloud mutations.
  - Secret inspection or credential changes.
  - Push, PR creation, or remote CI changes without explicit approval.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Establish audit task record and planning evidence | `docs/04.execution/plans/**`, `docs/04.execution/tasks/**`, Stage 04 READMEs, progress ledger | VAL-SPC-005 | New Plan and Task pass Stage 04 English-first and template checks |
| PLN-002 | Record baseline audit findings | Task finding ledger, `docs/99.templates/**`, Stage 00 rules, quality gate | VAL-SPC-001, VAL-SPC-002, VAL-SPC-003 | Finding ledger has evidence, risk, action, validation, and status |
| PLN-003 | Clarify current support contracts | `docs/99.templates/support/**`, `docs/99.templates/README.md` | VAL-SPC-001, VAL-SPC-002 | No active support doc describes completed migration phases as current rules |
| PLN-004 | Remove overlapping harness-task route semantics | `template-routing.md`, `sdlc-governance.md`, README references, quality gate if needed | VAL-SPC-001, VAL-SPC-003 | Harness task contract is supplemental and does not create a second structural route |
| PLN-005 | Harden deterministic validation | `scripts/validate-repo-quality-gates.sh` | VAL-SPC-003, VAL-SPC-004, VAL-SPC-005 | Quality gate fails on stable drift patterns and passes on the current repo |
| PLN-006 | Apply final verification and completion sync | Task record, progress ledger, README indexes | VAL-SPC-004, VAL-SPC-005, VAL-SPC-006 | Final scan and quality gate evidence are recorded |

## Implementation Tasks

### Task 1: Planning And Task Baseline

**Files:**
- Create: `docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md`
- Create: `docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Confirm the branch and worktree**

Run:

```bash
git status --short --branch
```

Expected: branch `codex/template-governance-audit-enhancement` with only this
planning unit changed before staging.

- [ ] **Step 2: Create the Stage 04 Plan and Task record**

Use the current Plan and Task templates:

```bash
docs/99.templates/templates/sdlc/execution/plan.template.md
docs/99.templates/templates/sdlc/execution/task.template.md
```

Expected: both authored files use `type: sdlc/*`, `owner: platform`,
`status: draft`, `updated: 2026-07-03`, and English-only body text.

- [ ] **Step 3: Register the new files in Stage 04 indexes**

Update the plan and task README document indexes with these rows:

```markdown
| [`./2026-07-03-template-governance-audit-enhancement.md`](./2026-07-03-template-governance-audit-enhancement.md) | `docs/99.templates/**` follow-up audit and targeted template-governance enhancement plan | Draft | 2026-07-03 |
| [`./2026-07-03-template-governance-audit-enhancement.md`](./2026-07-03-template-governance-audit-enhancement.md) | `docs/99.templates/**` follow-up audit findings, remediation tracking, validator hardening evidence, and final handoff | Draft | 2026-07-03 |
```

Expected: the first row lands in `plans/README.md`; the second lands in
`tasks/README.md`.

- [ ] **Step 4: Record progress memory**

Append a progress entry titled
`2026-07-03 — Template governance audit enhancement plan` to
`docs/00.agent-governance/memory/progress.md`.

Expected: the entry links the Plan and Task record and names the next action as
baseline audit execution.

- [ ] **Step 5: Validate and commit the planning unit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(plan): Plan template governance audit enhancement"
```

### Task 2: Baseline Audit And Finding Ledger

**Files:**
- Modify: `docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`
- Read: `docs/99.templates/**`
- Read: `docs/00.agent-governance/rules/document-stage-routing.md`
- Read: `docs/00.agent-governance/rules/documentation-protocol.md`
- Read: `scripts/validate-repo-quality-gates.sh`

- [ ] **Step 1: Run template inventory scan**

Run:

```bash
find docs/99.templates -maxdepth 5 -type f -print | sort
```

Expected: files are only under `README.md`, `support/**`, and
`templates/**`; no flat `docs/99.templates/*.template.*` files appear.

- [ ] **Step 2: Run current drift candidate scan**

Run:

```bash
rg -n "Phase [1-4]|during the migration|after Phase|current and target|YYYY-MM-DD-<harness-task>|harness-task-contract" docs/99.templates/support docs/99.templates/README.md docs/00.agent-governance/rules/document-stage-routing.md scripts/validate-repo-quality-gates.sh
```

Expected: the scan identifies only bounded support/README references that map
to FND-001, FND-002, or accepted historical context. It must not reveal active
flat-template routes.

- [ ] **Step 3: Run active residue scans**

Run:

```bash
rg -n -e "Target: docs[/]" -e "Use this te[m]plate" docs --glob "*.md" --glob "!docs/99.templates/**"
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex .agents AGENTS.md RTK.md
rg -n "docs/10\\.incidents|Legacy postmortem top-level|Legacy learning top-level" docs scripts .codex .agents AGENTS.md RTK.md
```

Expected: no active authored-doc residue or legacy route match is returned.
Historical migration evidence may be recorded only when the surrounding text is
dated and not a current contract.

- [ ] **Step 4: Update the finding ledger**

Record findings using this shape in the Task record:

```markdown
| Finding ID | Scope | Evidence Path | Expected Contract | Observed State | Risk | Action | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FND-001 | support | `docs/99.templates/support/frontmatter-schema.md` | Support docs describe current steady-state contracts | Migration phase wording remains in active support text | Medium | doc-sync | `rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support` | Open |
```

Expected: every finding has a concrete evidence path, expected contract,
observed state, risk, action, validation command, and status.

- [ ] **Step 5: Commit the baseline audit record**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md
git commit -m "docs(audit): Record template governance baseline"
```

Expected: both validation commands pass before commit.

### Task 3: Support Contract Remediation

**Files:**
- Modify: `docs/99.templates/support/README.md`
- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/99.templates/support/sdlc-governance.md`
- Modify: `docs/99.templates/README.md`
- Modify: `docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`

- [ ] **Step 1: Convert migration-phase wording to current-contract wording**

Apply these replacements:

```text
Defines current and target frontmatter profile rules.
-> Defines current frontmatter profile rules.

Phase 3 applies this schema to template files, authored documents, and repository validation.
-> This schema applies to Markdown template files, authored documents, and repository validation.

route references to remove during the migration.
-> route references rejected by current contracts.

Cleanup Phase
-> Current Enforcement

The flat-path search should not return active route references after Phase 2.
-> The flat-path search must not return active route references in current contracts.
```

Expected: support docs no longer speak about completed migration phases as if
they are the active operating model.

- [ ] **Step 2: Clarify harness task contract placement**

In `template-routing.md` and `sdlc-governance.md`, remove
`docs/04.execution/tasks/YYYY-MM-DD-<harness-task>.md` from structural route
tables and add a supplemental starter note:

```markdown
## Supplemental Task Starter

`harness-task-contract.template.md` supplements
`templates/sdlc/execution/task.template.md` for high-risk harness tasks. It
does not create a second structural route for `docs/04.execution/tasks/*.md`;
the authored Task record still uses `type: sdlc/task` and the Stage 04 Task
location.
```

Expected: `task.template.md` remains the only structural mapping for
`docs/04.execution/tasks/*.md`.

- [ ] **Step 3: Update the Task finding statuses**

Set FND-001 and FND-002 to `Resolved` with validation commands:

```bash
rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support
rg -n "YYYY-MM-DD-<harness-task>.*harness-task-contract|harness-task-contract.*YYYY-MM-DD-<harness-task>" docs/99.templates/support/template-routing.md docs/99.templates/support/sdlc-governance.md
```

Expected: the first command returns no support-doc matches. The second command
returns no structural route rows; supplemental prose may mention both terms
only when it explicitly says the harness starter is not a second structural
route.

- [ ] **Step 4: Validate and commit support contract remediation**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both commands pass.

Commit:

```bash
git add docs/99.templates/support/README.md docs/99.templates/support/frontmatter-schema.md docs/99.templates/support/legacy-cleanup-rules.md docs/99.templates/support/template-routing.md docs/99.templates/support/sdlc-governance.md docs/99.templates/README.md docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md
git commit -m "docs(templates): Clarify current support contracts"
```

### Task 4: Validator Guardrail Enhancement

**Files:**
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Add support-doc stale wording validation**

Add this check near the existing `template_support_root` validation block:

```python
support_stale_patterns = [
    (re.compile(r"Phase [1-4]"), "migration phase wording"),
    (re.compile(r"during the migration"), "migration-only wording"),
    (re.compile(r"after Phase"), "migration phase ordering"),
    (re.compile(r"current and target frontmatter"), "current/target schema wording"),
]
for support_doc in sorted(template_support_root.glob("*.md")):
    if support_doc.name == "README.md":
        continue
    support_text = read_text(support_doc)
    for pattern, label in support_stale_patterns:
        if pattern.search(support_text):
            fail(f"{rel(support_doc)} contains stale {label}")
```

Expected: the current repo passes after Task 3 remediation.

- [ ] **Step 2: Add harness route overlap validation**

Add this check after `template_routing.md` is available:

```python
template_routing_path = template_support_root / "template-routing.md"
template_routing_rows = markdown_table_after_heading(
    read_text(template_routing_path),
    "## Current Route Map",
)
for route_row in template_routing_rows[1:]:
    route_text = " | ".join(route_row)
    if "harness-task-contract.template.md" in route_text:
        fail(
            "docs/99.templates/support/template-routing.md Current Route Map "
            "must not list harness-task-contract.template.md as a structural route"
        )
```

Expected: the current route table passes and future overlap is rejected.

- [ ] **Step 3: Run validator and focused scans**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support
```

Expected: `git diff --check` and the quality gate pass. The focused scan
returns no active support-doc matches.

- [ ] **Step 4: Commit validator guardrails**

Run:

```bash
git add scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(validation): Guard template support drift"
```

Expected: commit succeeds after validation evidence is recorded.

### Task 5: Authored Document And Template Use Audit

**Files:**
- Modify: `docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`
- Modify only if a concrete finding exists: affected Stage README or authored
  document under `docs/00.agent-governance/**`, `docs/05.operations/**`,
  `docs/90.references/**`, or `docs/99.templates/**`

- [ ] **Step 1: Run authored-document residue audit**

Run:

```bash
rg -n -e "Target: docs[/]" -e "Use this te[m]plate" docs --glob "*.md" --glob "!docs/99.templates/**"
rg -n "type: (prd|ard|adr|spec|plan|task|policy|guide|runbook|incident|postmortem|reference)$" docs --glob "*.md" --glob "!docs/99.templates/**"
rg -n "owner: ['\"]platform['\"]" docs --glob "*.md"
```

Expected: no active authored document contains template residue, simple legacy
frontmatter type values, or quoted canonical owner values.

- [ ] **Step 2: Run incident bundle path audit**

Run:

```bash
find docs/05.operations/incidents -mindepth 1 -maxdepth 4 -type f -print | sort
rg -n "docs/05\\.operations/incidents/[0-9]{4}/INC-[0-9]{3}-[^/]+/(incident|postmortem)\\.md|docs/10\\.incidents" docs/99.templates docs/00.agent-governance docs/05.operations scripts
```

Expected: no active doc uses the old incident filename convention. Current
rules point to `INC-###-<title>.md` and `postmortem.md` inside the incident
folder.

- [ ] **Step 3: Record no-change or remediation evidence**

If all scans pass, record `accepted/no-change` entries for authored documents
in the Task record. If a scan reveals a concrete active contract mismatch,
patch only the affected document and rerun the scan that exposed it.

Expected: no broad topic rewrites; each changed authored document has a
specific finding ID and validation command.

- [ ] **Step 4: Commit authored-document audit evidence**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md
git commit -m "docs(audit): Verify authored template usage"
```

Expected: if Task 5 changes only the Task record, the commit contains evidence
only. If no file changed after Task 4, fold the evidence into Task 6 instead of
creating an empty commit.

### Task 6: Final Validation And Completion Sync

**Files:**
- Modify: `docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md`
- Modify: `docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Run final validation**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
find docs/99.templates -maxdepth 5 -type f -print | sort
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex .agents AGENTS.md RTK.md
rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support
```

Expected: diff and quality gate pass, template tree stays categorized, no flat
template route appears in active contracts, and support docs contain no stale
migration-phase wording.

- [ ] **Step 2: Mark execution records complete**

Update statuses:

```text
docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md -> status: done
docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md -> status: done
docs/04.execution/plans/README.md row -> Done
docs/04.execution/tasks/README.md row -> Done
docs/00.agent-governance/memory/progress.md entry -> complete
```

Expected: final evidence is recorded in the Task and progress ledger.

- [ ] **Step 3: Commit final completion sync**

Run:

```bash
git add docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(audit): Complete template governance audit enhancement"
```

Expected: commit succeeds after final validation evidence is recorded.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Static | Patch safety | `git diff --check` | No whitespace errors |
| VAL-PLN-002 | Static | Repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-003 | Static | Template tree shape | `find docs/99.templates -maxdepth 5 -type f -print \| sort` | Only README, support, and templates paths appear |
| VAL-PLN-004 | Static | Flat template route rejection | `rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md\|yaml\|graphql\|proto)" docs scripts .codex .agents AGENTS.md RTK.md` | No active current-route matches |
| VAL-PLN-005 | Static | Support stale wording rejection | `rg -n "Phase [1-4]\|during the migration\|after Phase\|current and target" docs/99.templates/support` | No matches after remediation |
| VAL-PLN-006 | Static | Authored template residue rejection | `rg -n -e "Target: docs[/]" -e "Use this te[m]plate" docs --glob "*.md" --glob "!docs/99.templates/**"` | No matches |
| VAL-PLN-007 | Static | Incident bundle route audit | `find docs/05.operations/incidents -mindepth 1 -maxdepth 4 -type f -print \| sort` | No placeholder incident files; future files follow bundle convention |
| VAL-PLN-008 | Review | Finding ledger completeness | Manual review of the Stage 04 Task record | Each finding has evidence, risk, action, validation, and status |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Validator check is too broad | Medium | Limit new checks to `docs/99.templates/support/*.md` and route-map tables with stable semantics. |
| Support docs need historical migration links | Low | Allow links to completed migration spec, plan, and task while rejecting phase wording in current contract prose. |
| Harness task starter is still useful but not structural | Medium | Document it as a supplemental starter that keeps `type: sdlc/task` and Stage 04 Task routing. |
| Authored-doc scan finds broad unrelated drift | Medium | Record the finding and ask for scope approval before broad rewrites. |
| External style guidance conflicts with repo governance | Low | Repo governance wins; external sources remain supporting rationale only. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: `git diff --check`, repository quality gates, focused
  `rg` scans, and manual finding-ledger review.
- **Sandbox / Canary Rollout**: Not applicable; this work changes repository
  documentation and static validation only.
- **Human Approval Gate**: Required before push, PR creation, live runtime
  validation, remote service changes, secret inspection, or scope expansion
  into a second template migration.
- **Rollback Trigger**: Revert or repair the latest logical commit if quality
  gates fail, route maps become ambiguous, or support contracts contradict
  Stage 00 governance.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [ ] Baseline audit findings recorded.
- [ ] Current support contracts clarified.
- [ ] Harness task contract documented as supplemental rather than structural.
- [ ] Deterministic validator guardrails added where stable.
- [ ] Authored document and incident route audits recorded.
- [ ] Required validation commands pass.
- [ ] Plan, Task, README indexes, and progress ledger are synchronized.

## Related Documents

- **Spec**: [../../03.specs/012-template-governance-audit-enhancement/spec.md](../../03.specs/012-template-governance-audit-enhancement/spec.md)
- **Tasks**: [../tasks/2026-07-03-template-governance-audit-enhancement.md](../tasks/2026-07-03-template-governance-audit-enhancement.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Document Stage Routing Rules**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
