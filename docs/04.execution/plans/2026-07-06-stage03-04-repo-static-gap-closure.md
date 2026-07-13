---
title: 'Stage 03/04 Repo-Static Gap Closure Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
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
`../../03.specs/023-stage03-04-repo-static-gap-closure/spec.md`.
The first concrete repo-static gap is the Workspace Engineering Research Pack
stream: every WER task is recorded as `Done`, but the Stage 04 Plan and Task
documents and their README indexes still advertise `Draft`.

The plan avoids live/runtime work. Items that require a live cluster, secret
value inspection, remote GitHub settings, or provider mutation are recorded as
operator-approved follow-up rows.

## Context

Initial investigation found:

- `docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md`
  has `status: draft`.
- `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`
  has `status: draft`, while its task table and phase checklist record
  WER-001 through WER-007 as complete.
- Stage 04 README indexes match the current `Draft` frontmatter, so existing
  index/frontmatter validation passes but does not classify the all-done
  execution evidence.
- Runtime validation items in older active specs remain outside repo-static
  scope and need explicit operator approval.

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
  - `docs/03.specs/023-stage03-04-repo-static-gap-closure/spec.md`
  - `docs/04.execution/plans/2026-07-06-stage03-04-repo-static-gap-closure.md`
  - `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
  - `docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md`
  - `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`
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

- Create: `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
- Modify: `docs/04.execution/tasks/README.md`
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
sed -n '1,360p' docs/03.specs/023-stage03-04-repo-static-gap-closure/spec.md
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
for base in ["docs/03.specs", "docs/04.execution/plans", "docs/04.execution/tasks"]:
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
  docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md \
  docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md
```

Expected: task rows and phase checkboxes show WER-001 through WER-007 are
complete while frontmatter remains `draft`.

- [ ] **Step 5: Create the Stage 04 task record**

Create `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
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
and document index in `docs/04.execution/tasks/README.md` with status
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
git add docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(tasks): Start Stage 03 04 repo-static gap closure"
```

### Task 2: Classify Stage 03/04 Gaps

**Files:**

- Modify: `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`

- [ ] **Step 1: Run targeted gap scans**

Run:

```bash
rg -n "(?i)pending|deferred|todo|in progress|not implemented|unimplemented|missing|gap|follow-?up|remaining|blocked|outstanding|future|live validation|runtime validation|not yet|next" \
  docs/03.specs docs/04.execution/plans docs/04.execution/tasks
```

Expected: command returns historical and current candidates; classify only
active repo-static gaps in the task ledger.

- [ ] **Step 2: Add gap classification rows**

In the task record, add these initial rows under `Gap Classification Ledger`:

```markdown
| S34-GAP-001 | `docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md`; `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md` | repo-static | WER task evidence records all WER tasks done, but plan/task frontmatter and README indexes remain `Draft`. | Close Stage 04 lifecycle drift in S34-003. | platform | Open |
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
git add docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md
git commit -m "docs(tasks): Classify Stage 03 04 repo-static gaps"
```

### Task 3: Close WER Lifecycle Drift

**Files:**

- Modify: `docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md`
- Modify: `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Confirm WER files have completed task evidence**

Run:

```bash
rg -n "WER-00[1-7].*Done|\\[x\\] WER-00[1-7]|Final validation|no-mutation handoff|Required validation" \
  docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md
```

Expected: WER-001 through WER-007 are present as `Done` and phase checklist
items are checked.

- [ ] **Step 2: Update WER plan frontmatter and completion criteria**

In `docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md`:

- Change frontmatter `status: draft` to `status: done`.
- Change completion criteria checkboxes for the dated research pack, moved
  references, two focused references, index routing, task/progress evidence,
  validation, and logical-unit commits from `[ ]` to `[x]`.
- Preserve historical command checkboxes in detailed task steps; they are plan
  instructions, not current execution state.

- [ ] **Step 3: Update WER task frontmatter**

In `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`:

- Change frontmatter `status: draft` to `status: done`.
- Add a short final evidence note under `Verification Summary` or the final
  evidence section stating that the lifecycle drift was closed by
  S34-GAP-001.

- [ ] **Step 4: Update Stage 04 README indexes**

In both `docs/04.execution/plans/README.md` and
`docs/04.execution/tasks/README.md`, change the WER row status from `Draft` to
`Done`. Keep the updated date as `2026-07-04` unless the row already uses a
later evidence date.

- [ ] **Step 5: Update the current task and progress memory**

In `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`:

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
git add docs/04.execution/plans/2026-07-04-workspace-engineering-research-pack.md docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(execution): Close WER repo-static lifecycle drift"
```

### Task 4: Record Operator-Approved Follow-up

**Files:**

- Modify: `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Add operator follow-up rows**

Under `Operator-Approved Follow-up Ledger`, add rows for:

```markdown
| S34-OP-001 | Argo Rollouts runtime validation | `docs/03.specs/004-argo-rollouts-progressive-delivery/spec.md` | Requires live cluster and operator-approved runtime checks. | operator-approved | Not run in this repo-static pass. |
| S34-OP-002 | ArgoCD Notifications Slack runtime validation | `docs/03.specs/005-argo-notifications-slack/spec.md` | Requires live controller state and Slack send/error evidence. | operator-approved | Not run in this repo-static pass. |
| S34-OP-003 | Vault/ESO/live secret readiness | `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`; `docs/03.specs/008-current-local-gitops-platform/spec.md` | Requires live runtime and must not inspect secret values. | operator-approved | Not run in this repo-static pass. |
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
git add docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(tasks): Route operator-approved Stage 03 04 follow-ups"
```

### Task 5: Final Validation and Closure

**Files:**

- Modify: `docs/04.execution/plans/2026-07-06-stage03-04-repo-static-gap-closure.md`
- Modify: `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
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

In `docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`:

- Change frontmatter `status: active` to `status: done`.
- Mark `S34-005` as `Done`.
- Mark all Phase View items checked.
- Add the final validation bundle output summary.

- [ ] **Step 3: Close the current plan**

In `docs/04.execution/plans/2026-07-06-stage03-04-repo-static-gap-closure.md`:

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
git add docs/04.execution/plans/2026-07-06-stage03-04-repo-static-gap-closure.md docs/04.execution/tasks/2026-07-06-stage03-04-repo-static-gap-closure.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(tasks): Record Stage 03 04 repo-static gap closure"
```

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-023-001 | Structural | Whitespace and patch integrity | `git diff --check` | No output. |
| VAL-PLN-023-002 | Static | Repository lifecycle/index quality gate | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed`. |
| VAL-PLN-023-003 | Static | Quality gate shell syntax | `bash -n scripts/validate-repo-quality-gates.sh` | No output. |
| VAL-PLN-023-004 | Manifest | Repo manifest syntax and optional kube-linter lane | `bash scripts/validate-k8s-manifests.sh .` | Exit 0; optional kube-linter skip may be reported. |
| VAL-PLN-023-005 | Security | Plaintext secret scan | `bash scripts/check-secret-handling.sh .` | Exit 0 with no plaintext secret findings. |
| VAL-PLN-023-006 | Policy | Policy fallback or Conftest lane | `bash scripts/validate-policy-gates.sh .` | Exit 0; optional conftest fallback may be reported. |

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

## Completion Criteria

- [x] Stage 04 task record exists and is indexed.
- [x] Stage 03/04 gaps are classified by evidence lane.
- [x] WER repo-static lifecycle drift is closed.
- [x] Operator-approved follow-up is recorded separately.
- [x] Final validation bundle passes.
- [x] Progress memory records completion and untouched pre-existing files.

## Traceability

- **Spec**: [../../03.specs/023-stage03-04-repo-static-gap-closure/spec.md](../../03.specs/023-stage03-04-repo-static-gap-closure/spec.md)
- **Planned Tasks Path**: `../tasks/2026-07-06-stage03-04-repo-static-gap-closure.md`
- **WER Plan**: [./2026-07-04-workspace-engineering-research-pack.md](./2026-07-04-workspace-engineering-research-pack.md)
- **WER Task**: [../tasks/2026-07-04-workspace-engineering-research-pack.md](../tasks/2026-07-04-workspace-engineering-research-pack.md)
- **SDLC Lifecycle Contract Spec**: [../../03.specs/021-sdlc-lifecycle-contract/spec.md](../../03.specs/021-sdlc-lifecycle-contract/spec.md)
- **Progress Memory**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
