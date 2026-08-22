---
title: 'Stage 03/04 Repo-Static Gap Closure Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
artifact_id: "PLAN-0023"
---

# Stage 03/04 Repo-Static Gap Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close repo-static Stage 03/04 implementation and evidence gaps while
separating live/runtime, secret, remote, and provider-required work into
operator-approved follow-up.

**Architecture:** This is a repository-static documentation lifecycle pass.
Stage 03 owns the design contract, Stage 04 owns execution evidence and gap
classification, existing validation scripts prove deterministic local
correctness, and operator-required work is recorded without being reported as
implemented.

**Tech Stack:** Markdown, Git, `rg`, POSIX shell, existing Stage 03/04
templates, `scripts/validate-repo-quality-gates.sh`,
`scripts/validate-k8s-manifests.sh`, `scripts/check-secret-handling.sh`, and
`scripts/validate-policy-gates.sh`.

---

## Overview

This plan implements
`../../03.specs/0023-stage03-04-repo-static-gap-closure/spec.md`.
The first concrete repo-static gap is the Workspace Engineering Research Pack
stream: every WER task is recorded as `Done`, but the Stage 04 Plan and Task
documents and their README indexes still advertise `Draft`.

The plan avoids live/runtime work. Items that require a live cluster, secret
value inspection, remote GitHub settings, or provider mutation are recorded as
operator-approved follow-up rows.

## Context

Initial investigation found:

- `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
  has `status: draft`.
- `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
  has `status: draft`, while its task table and phase checklist record
  WER-001 through WER-007 as complete.
- Stage 04 README indexes match the current `Draft` frontmatter, so existing
  index/frontmatter validation passes but does not classify the all-done
  execution evidence.
- Runtime validation items in older active specs remain outside repo-static
  scope and need explicit operator approval.

### Legacy Task ledger inputs

This task record tracks repo-static closure work for Stage 03/04 implementation
and evidence gaps. The first confirmed closure target is the Workspace
Engineering Research Pack lifecycle drift: its execution evidence records all
WER tasks as `Done`, while its Stage 04 plan/task frontmatter and README index
rows still advertise `Draft`.

This record also separates work that cannot be proven from repository-local
files, such as live cluster validation, secret readiness, remote GitHub
settings, or provider mutation.

- **Parent Spec**: [../../03.specs/0023-stage03-04-repo-static-gap-closure/spec.md](spec.md)
- **Parent Plan**: [../plans/2026-07-06-stage03-04-repo-static-gap-closure.md](plan.md)
- **WER Plan**: [../plans/2026-07-04-workspace-engineering-research-pack.md](../0017-workspace-engineering-research-pack/plan.md)
- **WER Task**: [./2026-07-04-workspace-engineering-research-pack.md](../0017-workspace-engineering-research-pack/README.md)
## Goals & In-Scope

- **Goals**:
  - Create a Stage 04 task record for the repo-static gap-closure pass.
  - Audit Stage 03/04 documents for repo-static gaps versus
    operator-approved follow-up items.
  - Close the WER Stage 04 lifecycle drift using existing completion evidence.
  - Record live/runtime, secret, remote, and provider-required items as
    operator-approved follow-up.
  - Run and record final repository-static validation.
- **In Scope**:
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
  - Stage 04 plan/task README indexes.
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Reclassify every historical Stage 03 `draft` spec as `done`.
  - Add broad lifecycle validation rules that may create noisy false positives.
  - Prove live runtime readiness.
- **Out of Scope**:
  - Live Kubernetes, Argo CD, Vault, External Secrets Operator, cloud, DNS,
    provider runtime, GitHub remote, branch protection, or ruleset mutation.
  - Secret value inspection, credential regeneration, token updates, and
    certificate changes.
  - Remote push, pull request creation, publish, or merge actions.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target Requirement | Validation Criteria |
| --- | --- | --- | --- | --- |
| S34-PLN-001 | Create Stage 04 task record and baseline gap audit | new task record, tasks README, progress memory | VAL-SPC-023-001, VAL-SPC-023-005 | Task record exists, baseline findings are captured, and repo-quality passes. |
| S34-PLN-002 | Classify Stage 03/04 gaps by evidence lane | task record | VAL-SPC-023-001, VAL-SPC-023-003 | Gap table separates `repo-static`, `operator-approved`, and `out-of-scope`. |
| S34-PLN-003 | Close WER repo-static lifecycle drift | WER plan/task, Stage 04 READMEs, progress memory | VAL-SPC-023-002 | WER plan/task frontmatter and indexes move to `done`, completion criteria are checked, and existing WER evidence remains intact. |
| S34-PLN-004 | Record operator-approved follow-up ledger | task record, progress memory | VAL-SPC-023-003 | Runtime/secret/remote/provider items are not implemented and are routed to operator approval. |
| S34-PLN-005 | Close validation and handoff evidence | current plan/task, progress memory | VAL-SPC-023-004, VAL-SPC-023-005 | Final validation bundle passes or records explicit optional-tool skips. |

### Implementation Tasks

> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.

### Task 1: Create Task Record and Baseline Audit

**Files:**

- Create: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Confirm branch and working tree**

Run:

```bash
git status --short --branch
```

Expected: branch is `codex/stage03-04-repo-static-gap-closure`; only the
pre-existing untracked `docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md`
and `sessions/` may appear.

- [ ] **Step 2: Read the parent spec and templates**

Run:

```bash
sed -n '1,360p' docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md
sed -n '1,180p' docs/99.templates/templates/sdlc/execution/task.template.md
```

Expected: spec success criteria and task template requirements are visible.

- [ ] **Step 3: Capture Stage 03/04 status inventory**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import re
root = Path(".")
for base in ["docs/03.specs", "docs/03.specs/plans", "docs/03.specs/tasks"]:
    print(f"## {base}")
    for path in sorted((root / base).rglob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"^status:\s*(\S+)", text, re.MULTILINE)
        status = match.group(1) if match else "NO_STATUS"
        if status.lower() not in {"done", "active"}:
            print(f"{path} {status}")
PY
```

Expected: output includes the WER Stage 04 plan/task as `draft` and lists
Stage 03 draft specs for classification, not automatic closure.

- [ ] **Step 4: Capture WER completion evidence**

Run:

```bash
rg -n "status: draft|WER-00[1-7].*Done|\\[x\\] WER-|Completion Criteria|Final validation|Handoff" \
  docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md \
  docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records
```

Expected: task rows and phase checkboxes show WER-001 through WER-007 are
complete while frontmatter remains `draft`.

- [ ] **Step 5: Create the Stage 04 task record**

Create `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
with frontmatter:

```yaml
---
title: 'Task: Stage 03/04 Repo-Static Gap Closure'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-06
---
```

Include:

- `Overview`
- `Inputs`
- `Working Rules`
- `Task Table`
- `Suggested Types`
- `Phase View`
- `Gap Classification Ledger`
- `Operator-Approved Follow-up Ledger`
- `Verification Summary`
- `Related Documents`

Initial task rows:

```markdown
| S34-001 | Create task record and baseline gap audit. | doc | VAL-SPC-023-001 | S34-PLN-001 | Baseline inventory and repo-quality gate. | platform | In Progress |
| S34-002 | Classify Stage 03/04 gaps by evidence lane. | eval | VAL-SPC-023-001, VAL-SPC-023-003 | S34-PLN-002 | Gap ledger separates repo-static and operator-approved work. | platform | Todo |
| S34-003 | Close WER repo-static lifecycle drift. | doc | VAL-SPC-023-002 | S34-PLN-003 | WER plan/task/index statuses and completion criteria align. | platform | Todo |
| S34-004 | Record operator-approved follow-up ledger. | ops | VAL-SPC-023-003 | S34-PLN-004 | Live/runtime and remote-required items are routed without mutation. | platform | Todo |
| S34-005 | Close validation and handoff evidence. | test | VAL-SPC-023-004, VAL-SPC-023-005 | S34-PLN-005 | Final validation bundle passes. | platform | Todo |
```

- [ ] **Step 6: Update the task README index**

Add `2026-07-06-stage03-04-repo-static-gap-closure.md` to the structure block
and document index in `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records` with status
`Active` and updated date `2026-07-06`.

- [ ] **Step 7: Update progress memory**

Append a `2026-07-06 - Stage 03/04 repo-static gap closure` entry to
`docs/00.agent-governance/memory/progress.md` with status `in-progress`,
the branch name, and the no-live/no-secret/no-remote boundary.

- [ ] **Step 8: Validate and commit Task 1**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: `git diff --check` has no output and repo-quality prints
`[PASS] repository quality gates passed`.

Commit:

```bash
git add docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(tasks): Start Stage 03 04 repo-static gap closure"
```

### Task 2: Classify Stage 03/04 Gaps

**Files:**

- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`

- [ ] **Step 1: Run targeted gap scans**

Run:

```bash
rg -n "(?i)pending|deferred|todo|in progress|not implemented|unimplemented|missing|gap|follow-?up|remaining|blocked|outstanding|future|live validation|runtime validation|not yet|next" \
  docs/03.specs docs/03.specs/plans docs/03.specs/tasks
```

Expected: command returns historical and current candidates; classify only
active repo-static gaps in the task ledger.

- [ ] **Step 2: Add gap classification rows**

In the task record, add these initial rows under `Gap Classification Ledger`:

```markdown
| S34-GAP-001 | `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`; `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records` | repo-static | WER task evidence records all WER tasks done, but plan/task frontmatter and README indexes remain `Draft`. | Close Stage 04 lifecycle drift in S34-003. | platform | Open |
| S34-GAP-002 | Active runtime specs and older task evidence | operator-approved | Rollouts, Notifications, Vault/ESO, live validation, secret value, and remote settings require runtime/operator authority. | Record as follow-up in S34-004; do not mutate live or remote systems. | operator | Follow-up |
| S34-GAP-003 | Stage 03 draft governance specs | out-of-scope | Draft specs may remain design contracts even when their Stage 04 execution is done; automatic conversion to `done` would rewrite lifecycle semantics. | Preserve unless a scoped lifecycle decision approves spec status migration. | platform | Closed |
```

- [ ] **Step 3: Mark S34-002 done**

Update the task table row for `S34-002` to `Done` and add evidence that the
gap scan was run and classified.

- [ ] **Step 4: Validate and commit Task 2**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both pass.

Commit:

```bash
git add docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records
git commit -m "docs(tasks): Classify Stage 03 04 repo-static gaps"
```

### Task 3: Close WER Lifecycle Drift

**Files:**

- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Confirm WER files have completed task evidence**

Run:

```bash
rg -n "WER-00[1-7].*Done|\\[x\\] WER-00[1-7]|Final validation|no-mutation handoff|Required validation" \
  docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records
```

Expected: WER-001 through WER-007 are present as `Done` and phase checklist
items are checked.

- [ ] **Step 2: Update WER plan frontmatter and completion criteria**

In `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`:

- Change frontmatter `status: draft` to `status: done`.
- Change completion criteria checkboxes for the dated research pack, moved
  references, two focused references, index routing, task/progress evidence,
  validation, and logical-unit commits from `[ ]` to `[x]`.
- Preserve historical command checkboxes in detailed task steps; they are plan
  instructions, not current execution state.

- [ ] **Step 3: Update WER task frontmatter**

In `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`:

- Change frontmatter `status: draft` to `status: done`.
- Add a short final evidence note under `Verification Summary` or the final
  evidence section stating that the lifecycle drift was closed by
  S34-GAP-001.

- [ ] **Step 4: Update Stage 04 README indexes**

In both `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md` and
`docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`, change the WER row status from `Draft` to
`Done`. Keep the updated date as `2026-07-04` unless the row already uses a
later evidence date.

- [ ] **Step 5: Update the current task and progress memory**

In `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`:

- Mark `S34-GAP-001` as `Closed`.
- Mark `S34-003` as `Done`.
- Add validation evidence for the WER closure.

In `docs/00.agent-governance/memory/progress.md`, add evidence that WER
plan/task lifecycle drift was closed without changing live/runtime state.

- [ ] **Step 6: Validate and commit Task 3**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both pass and Stage 04 README status/date sync stays valid.

Commit:

```bash
git add docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(execution): Close WER repo-static lifecycle drift"
```

### Task 4: Record Operator-Approved Follow-up

**Files:**

- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Add operator follow-up rows**

Under `Operator-Approved Follow-up Ledger`, add rows for:

```markdown
| S34-OP-001 | Argo Rollouts runtime validation | `docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md` | Requires live cluster and operator-approved runtime checks. | operator-approved | Not run in this repo-static pass. |
| S34-OP-002 | ArgoCD Notifications Slack runtime validation | `docs/03.specs/0005-argo-notifications-slack/spec.md` | Requires live controller state and Slack send/error evidence. | operator-approved | Not run in this repo-static pass. |
| S34-OP-003 | Vault/ESO/live secret readiness | `docs/03.specs/0006-workspace-harness-gap-analysis/spec.md`; `docs/03.specs/0008-current-local-gitops-platform/spec.md` | Requires live runtime and must not inspect secret values. | operator-approved | Not run in this repo-static pass. |
| S34-OP-004 | Remote GitHub ruleset or CI provider settings | Stage 03/04 deferred boundary mentions | Requires remote settings authority. | operator-approved | Not run in this repo-static pass. |
```

- [ ] **Step 2: Mark S34-004 done**

Update `S34-004` to `Done` and add evidence that no live/runtime, secret, or
remote action was performed.

- [ ] **Step 3: Update progress memory**

Add a memory bullet that repo-static closure should keep operator-approved
follow-up separate from implementation evidence.

- [ ] **Step 4: Validate and commit Task 4**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both pass.

Commit:

```bash
git add docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(tasks): Route operator-approved Stage 03 04 follow-ups"
```

### Task 5: Final Validation and Closure

**Files:**

- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
- Modify: `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Run final validation bundle**

Run:

```bash
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

Expected:

- `git diff --check` prints no output.
- Shell syntax check prints no output.
- Repo-quality prints `[PASS] repository quality gates passed`.
- Manifest validation exits 0; optional `kube-linter` skip is acceptable if
  the script reports it.
- Secret scan exits 0 with no plaintext secret findings.
- Policy gate exits 0; optional `conftest` fallback is acceptable if the
  script reports it.

- [ ] **Step 2: Close the current task record**

In `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`:

- Change frontmatter `status: active` to `status: done`.
- Mark `S34-005` as `Done`.
- Mark all Phase View items checked.
- Add the final validation bundle output summary.

- [ ] **Step 3: Close the current plan**

In `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`:

- Change frontmatter `status: draft` to `status: done`.
- Check every item under `Completion Criteria`.

- [ ] **Step 4: Update README indexes**

In both Stage 04 README files, set the current plan/task row status to `Done`
and updated date to `2026-07-06`.

- [ ] **Step 5: Update progress memory**

Set the progress entry for this stream to `completed` and record:

- WER repo-static drift closed.
- Operator-approved follow-up separated.
- Final validation bundle results.
- Pre-existing untracked files left untouched.

- [ ] **Step 6: Validate and commit final closure**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both pass.

Commit:

```bash
git add docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(tasks): Record Stage 03 04 repo-static gap closure"
```

### Legacy Task supplemental evidence

### Phase View

### Phase 1: Baseline and Classification

- [x] S34-001 Create task record and baseline gap audit.
- [x] S34-002 Classify Stage 03/04 gaps by evidence lane.

### Phase 2: Repo-Static Closure

- [x] S34-003 Close WER repo-static lifecycle drift.

### Phase 3: Follow-up Routing and Closure

- [x] S34-004 Record operator-approved follow-up ledger.
- [x] S34-005 Close validation and handoff evidence.

### Gap Classification Ledger

| Gap ID | Source | Evidence Lane | Finding | Resolution | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| S34-GAP-001 | `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`; `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records` | repo-static | WER task evidence records all WER tasks done, but plan/task frontmatter and README indexes remain `Draft`. | Closed in S34-003 by aligning WER plan/task frontmatter, plan completion criteria, and Stage 04 README indexes with existing Done evidence. | platform | Closed |
| S34-GAP-002 | Active runtime specs and older task evidence | operator-approved | Rollouts, Notifications, Vault/ESO, live validation, secret value, and remote settings require runtime/operator authority. | Record as follow-up in S34-004; do not mutate live or remote systems. | operator | Follow-up |
| S34-GAP-003 | Stage 03 draft governance specs | out-of-scope | Draft specs may remain design contracts even when their Stage 04 execution is done; automatic conversion to `done` would rewrite lifecycle semantics. | Preserve unless a scoped lifecycle decision approves spec status migration. | platform | Closed |

### Operator-Approved Follow-up Ledger

| Follow-up ID | Topic | Source | Approval Boundary | Evidence Lane | Status |
| --- | --- | --- | --- | --- | --- |
| S34-OP-001 | Argo Rollouts runtime validation | `docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md` | Requires live cluster and operator-approved runtime checks. | operator-approved | Not run in this repo-static pass. |
| S34-OP-002 | ArgoCD Notifications Slack runtime validation | `docs/03.specs/0005-argo-notifications-slack/spec.md` | Requires live controller state and Slack send/error evidence. | operator-approved | Not run in this repo-static pass. |
| S34-OP-003 | Vault/ESO/live secret readiness | `docs/03.specs/0006-workspace-harness-gap-analysis/spec.md`; `docs/03.specs/0008-current-local-gitops-platform/spec.md` | Requires live runtime and must not inspect secret values. | operator-approved | Not run in this repo-static pass. |
| S34-OP-004 | Remote GitHub ruleset or CI provider settings | Stage 03/04 deferred boundary mentions | Requires remote settings authority. | operator-approved | Not run in this repo-static pass. |

### Baseline Audit

- Branch baseline: `codex/stage03-04-repo-static-gap-closure`.
- Preserved pre-existing untracked paths:
  - `docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md`
  - `sessions/`
- Status inventory found Stage 03 draft specs from
  `0009-workspace-harness-research-pack` through
  `0023-stage03-04-repo-static-gap-closure`. These remain design contracts for
  classification, not automatic closure targets.
- Stage 04 status inventory found:
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
    as `draft`.
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
    as `draft`.
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
    as `draft`.
- WER completion evidence found `WER-001` through `WER-007` task rows as
  `Done` and checked phase-view items for WER-002 through WER-007, while WER
  plan/task frontmatter remains `status: draft`.

### Gap Scan Evidence

- Targeted scan command:
  `rg -n "(?i)pending|deferred|todo|in progress|not implemented|unimplemented|missing|gap|follow-?up|remaining|blocked|outstanding|future|live validation|runtime validation|not yet|next" docs/03.specs docs/03.specs/plans docs/03.specs/tasks`
- The scan produced historical, template, spec-policy, and task-evidence hits.
  Classification used only current Stage 03/04 ownership boundaries and active
  evidence, not raw keyword count.
- Repo-static closure candidate:
  - WER Stage 04 plan/task lifecycle drift, because completion evidence exists
    locally and the correction is limited to frontmatter, completion criteria,
    indexes, and evidence notes.
- Operator-approved follow-up candidates:
  - Argo Rollouts runtime validation.
  - ArgoCD Notifications Slack runtime validation.
  - Vault/ESO/live secret readiness.
  - Remote GitHub ruleset or CI provider settings.
- Out-of-scope candidates:
  - Bulk Stage 03 `draft` spec conversion, because Stage 03 can keep design
    contracts open while Stage 04 records execution completion.

### WER Lifecycle Closure Evidence

- WER task evidence scan confirmed `WER-001` through `WER-007` task rows as
  `Done`.
- WER plan frontmatter changed from `status: draft` to `status: done`.
- WER plan completion criteria changed from open checkboxes to checked
  completion evidence while preserving detailed historical task-step
  checkboxes.
- WER task frontmatter changed from `status: draft` to `status: done`.
- Stage 04 plan and task README index rows changed from `Draft` to `Done`.
- No live/runtime, secret, remote, provider, or third-party action was
  performed.

### Operator-Approved Follow-up Evidence

- Confirmed the referenced Stage 03 spec files exist for Rollouts,
  Notifications, workspace harness gap analysis, and current local GitOps
  platform.
- Recorded four operator-approved follow-up rows for live/runtime, secret, and
  remote authority work.
- No live cluster command, secret value inspection, remote GitHub settings
  change, provider mutation, push, publish, or merge action was performed.

### Final Validation Bundle

| Command | Result |
| --- | --- |
| `git diff --check` | PASS; no output. |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS; no output. |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS; `[PASS] repository quality gates passed`. |
| `bash scripts/validate-k8s-manifests.sh .` | PASS; 104 YAML files parsed and optional `kube-linter` was skipped because it is not installed. |
| `bash scripts/check-secret-handling.sh .` | PASS; 100 files scanned and no plaintext secret patterns found. |
| `bash scripts/validate-policy-gates.sh .` | PASS; optional `conftest` was not installed and the built-in policy fallback passed. |

Final boundary: WER repo-static drift is closed, operator-approved follow-up is
separate, and the pre-existing untracked
`docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md`
and `sessions/` paths remain untouched.
## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-023-001 | Structural | Whitespace and patch integrity | `git diff --check` | No output. |
| VAL-PLN-023-002 | Static | Repository lifecycle/index quality gate | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed`. |
| VAL-PLN-023-003 | Static | Quality gate shell syntax | `bash -n scripts/validate-repo-quality-gates.sh` | No output. |
| VAL-PLN-023-004 | Manifest | Repo manifest syntax and optional kube-linter lane | `bash scripts/validate-k8s-manifests.sh .` | Exit 0; optional kube-linter skip may be reported. |
| VAL-PLN-023-005 | Security | Plaintext secret scan | `bash scripts/check-secret-handling.sh .` | Exit 0 with no plaintext secret findings. |
| VAL-PLN-023-006 | Policy | Policy fallback or Conftest lane | `bash scripts/validate-policy-gates.sh .` | Exit 0; optional conftest fallback may be reported. |

### Legacy Task verification evidence

- **Test Commands**:
  - `git status --short --branch`
  - `python3 - <<'PY' ... status inventory ... PY`
  - `rg -n "status: draft|WER-00[1-7].*Done|\[x\] WER-|Completion Criteria|Final validation|Handoff" ...`
  - `rg -n "(?i)pending|deferred|todo|in progress|not implemented|unimplemented|missing|gap|follow-?up|remaining|blocked|outstanding|future|live validation|runtime validation|not yet|next" docs/03.specs docs/03.specs/plans docs/03.specs/tasks`
- **Eval Commands**:
  - `git diff --check` PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` PASS with
    `[PASS] repository quality gates passed`.
  - S34-002 validation: `git diff --check` PASS.
  - S34-002 validation: `bash scripts/validate-repo-quality-gates.sh .` PASS
    with `[PASS] repository quality gates passed`.
  - S34-003 validation: `git diff --check` PASS.
  - S34-003 validation: `bash scripts/validate-repo-quality-gates.sh .` PASS
    with `[PASS] repository quality gates passed`.
  - S34-004 validation: `git diff --check` PASS.
  - S34-004 validation: `bash scripts/validate-repo-quality-gates.sh .` PASS
    with `[PASS] repository quality gates passed`.
  - S34-005 final validation bundle PASS:
    - `git diff --check`
    - `bash -n scripts/validate-repo-quality-gates.sh`
    - `bash scripts/validate-repo-quality-gates.sh .`
    - `bash scripts/validate-k8s-manifests.sh .`
    - `bash scripts/check-secret-handling.sh .`
    - `bash scripts/validate-policy-gates.sh .`
  - S34-005 closure validation after status/index updates PASS:
    - `git diff --check`
    - `bash scripts/validate-repo-quality-gates.sh .`
- **Logs / Evidence Location**:
  - This task record, Stage 04 README index, and progress memory entry.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Draft Stage 03 specs are incorrectly marked done. | High | Do not migrate Stage 03 draft specs in this pass unless a separate lifecycle decision is approved. |
| Historical evidence is rewritten as current truth. | Medium | Preserve old command literals and evidence blocks; only change active frontmatter, indexes, and closure notes. |
| Runtime gaps are accidentally reported as implemented. | High | Put runtime, secret, remote, and provider work in the operator-approved ledger. |
| Validator hardening becomes noisy. | Medium | Do not add a broad all-done-to-frontmatter rule in this pass; rely on task evidence and existing README/frontmatter sync checks. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Run repo-static validation after each logical commit.
- **Sandbox / Canary Rollout**: Not applicable; this is documentation and
  validation evidence work.
- **Human Approval Gate**: Required before live runtime validation, remote
  GitHub changes, provider changes, credential work, or secret value
  inspection.
- **Rollback Trigger**: If WER evidence does not actually prove completion,
  stop and keep WER status as `draft` while recording the unresolved gap.
- **Prompt / Model Promotion Criteria**: Not applicable.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `S34-001 through S34-005` is limited to these Stage 03/04 Repo-Static Gap Closure owners and Task-Table surfaces:
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
  - `docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md`
  - `docs/03.specs/0005-argo-notifications-slack/spec.md`
  - `docs/03.specs/0006-workspace-harness-gap-analysis/spec.md`
  - `docs/03.specs/0008-current-local-gitops-platform/spec.md`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Stage 03/04 Repo-Static Gap Closure work items and linked evidence owners.
- **Approval Required**: Human approval is required before Stage 03/04 Repo-Static Gap Closure protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Stage 03/04 Repo-Static Gap Closure outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git status --short --branch`
  - `python3 - <<'PY' ... status inventory ... PY`
  - `rg -n "status: draft|WER-00[1-7].*Done|\[x\] WER-|Completion Criteria|Final validation|Handoff" ...`
  - `rg -n "(?i)pending|deferred|todo|in progress|not implemented|unimplemented|missing|gap|follow-?up|remaining|blocked|outstanding|future|live validation|runtime validation|not yet|next" docs/03.specs docs/03.specs/plans docs/03.specs/tasks`
- **Live Validation**: DEFER — Stage 03/04 Repo-Static Gap Closure is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Stage 03/04 Repo-Static Gap Closure; do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Stage 03/04 Repo-Static Gap Closure change set for `S34-001 through S34-005` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Stage 03/04 Repo-Static Gap Closure evidence remains in:
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md`
  - `docs/03.specs/0023-stage03-04-repo-static-gap-closure/README.md#task-records`
## Completion Criteria

- [x] Stage 04 task record exists and is indexed.
- [x] Stage 03/04 gaps are classified by evidence lane.
- [x] WER repo-static lifecycle drift is closed.
- [x] Operator-approved follow-up is recorded separately.
- [x] Final validation bundle passes.
- [x] Progress memory records completion and untouched pre-existing files.

## Traceability

- **Spec**: [../../03.specs/0023-stage03-04-repo-static-gap-closure/spec.md](spec.md)
- **Planned Tasks Path**: `../tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
- **WER Plan**: [./2026-07-04-workspace-engineering-research-pack.md](../0017-workspace-engineering-research-pack/plan.md)
- **WER Task**: [../tasks/2026-07-04-workspace-engineering-research-pack.md](../0017-workspace-engineering-research-pack/README.md)
- **SDLC Lifecycle Contract Spec**: [../../03.specs/0021-sdlc-lifecycle-contract/spec.md](../0021-sdlc-lifecycle-contract/spec.md)
- **Progress Memory**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)

### Legacy Task traceability

- **Spec**: [../../03.specs/0023-stage03-04-repo-static-gap-closure/spec.md](spec.md)
- **Plan**: [../plans/2026-07-06-stage03-04-repo-static-gap-closure.md](plan.md)
- **WER Plan**: [../plans/2026-07-04-workspace-engineering-research-pack.md](../0017-workspace-engineering-research-pack/plan.md)
- **WER Task**: [./2026-07-04-workspace-engineering-research-pack.md](../0017-workspace-engineering-research-pack/README.md)
- **Progress Memory**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
