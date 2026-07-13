---
title: 'Governance Owner and Roster Currentness Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
---

# Governance Owner and Roster Currentness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the complete audit/Spec/Plan information architecture and
close RMD-004 with one tested ten-role, thirty-adapter, canonical-owner
currentness contract.

**Architecture:** Preserve dated and completed evidence while making current
ownership explicit. Stage 90 routes findings, Spec 025 owns RMD-004 acceptance,
Stage 00 owns durable roster facts, Stage 04 Tasks own completion evidence, and
a focused validator enforces exact provider stem parity and owner pointers.

**Tech Stack:** Markdown, YAML frontmatter, Python 3 standard library, Bash,
Git, `rg`, `pre-commit`, and repository quality gates.

## Overview

This Plan converts the approved Spec 025 disposition ledgers into six
independently testable and reviewable implementation tasks. It preserves
completed evidence, repairs current ownership and navigation, and adds one
focused repository-static roster validator.

## Context

The Current 2026-07-11 audit found stale eight-role currentness prose and
ambiguous canonical-owner pointers. The broader design review also found
sixteen draft Specs backed by done Plans/Tasks, one completed execution Plan
misplaced in Stage 90, and incomplete evidence links across the forty-one
baseline Stage 04 Plans.

## Goals & In-Scope

- Normalize the Stage 90 audit pack information architecture.
- Reconcile all baseline Spec and Plan lifecycle/evidence records.
- Implement and test the RMD-004 ten-role/thirty-adapter contract.
- Preserve completed records unless all five Archive gates pass.
- Close the work with reciprocal SDLC links and rerunnable evidence.

## Non-Goals & Out-of-Scope

- Provider role-body, model, tool, or prompt changes.
- Live Kubernetes, Argo CD, Vault, ESO, cloud, or provider-runtime validation.
- Secret-value or credential inspection.
- Unrelated RMD remediation.
- Remote push, pull request, or merge.

### Global Constraints

- Work only in `.worktrees/spec-plan-roster-normalization` on branch
  `codex/spec-plan-roster-normalization`.
- Use evidence-based selective Archive; do not Archive a document because it
  is old or complete.
- Preserve dated audit report bodies except for navigation, currentness, and
  reciprocal-link corrections explicitly listed in this plan.
- Keep all forty-one baseline Plans as `done` execution evidence.
- Use Spec 025 as the sole RMD-004 implementation-contract owner.
- Keep Stage 00 as the durable-policy and current-roster owner.
- Keep Stage 04 Tasks as execution-evidence owners.
- Do not change provider role semantics, provider model policy, live runtime,
  GitOps desired state, credentials, secret values, or third-party resources.
- Use `apply_patch` for content edits and `git mv` only for the approved
  Stage 90-to-Stage 04 relocation.
- Run focused validation before each logical commit.
- Run `pre-commit run --all-files` before final closure.
- Do not push or remotely merge. The requested finish target is a local merge
  to `main` after explicit finishing approval.

---

### File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Execution control | Spec 025, this Plan, same-topic Task, Spec/Plan/Task READMEs | Own lifecycle, work units, and evidence routing. |
| Audit IA | `docs/90.references/audits/**`, relocated 2026-07-11 audit Plan/Task | Own one Current pointer, pack registry, pack roles, and dated evidence navigation. |
| Spec normalization | `docs/03.specs/006-*`, `009-*` through `024-*`, Spec README | Reconcile lifecycle, lineage, and implementation-contract ownership. |
| Plan normalization | Forty-one baseline Plan files and Plan README | Reconcile Task evidence links and label historical unchecked instructions. |
| Roster policy | `docs/00.agent-governance/harness-catalog.md` | Own ten-role and thirty-adapter durable current facts and owner pointers. |
| Roster validation | `scripts/validate-agent-roster-currentness.py`, fixture JSON, repository quality gate, script/test READMEs | Reject missing/mismatched stems, stale eight-role prose, and owner-pointer drift. |
| Closure evidence | Same-topic Task, remediation roadmap, progress ledger, indexes | Record results, commands, limitations, and RMD-004 closure. |

## Work Breakdown

| Task | Description | Primary validation | Commit |
| --- | --- | --- | --- |
| T-001 | Start the canonical execution chain | Reciprocal Spec/Plan/Task links | `docs(execution): start roster currentness workstream` |
| T-002 | Normalize audit IA and relocate the completed audit Plan | One Current pointer, six pack READMEs, no Stage 90 execution Plan | `docs(audits): normalize audit pack information architecture` |
| T-003 | Reconcile every Spec lifecycle and current owner | Twenty baseline dispositions plus Spec 025 | `docs(specs): reconcile lifecycle and current ownership` |
| T-004 | Reconcile every Plan with Task evidence | Forty-one baseline Plan ledger rows | `docs(plans): reconcile execution evidence links` |
| T-005 | Implement tested roster/current-owner enforcement | Positive and four negative fixture cases | `fix(governance): enforce canonical roster and owner pointers` |
| T-006 | Close evidence, lifecycle, and RMD-004 | Full QA bundle and clean worktree | `docs(governance): close roster currentness evidence` |

## Verification Plan

| ID | Level | Description | Command | Pass criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Spec/Plan/Task reciprocal lineage | Focused Python assertions in T-001 | All three paths and links exist. |
| VAL-PLN-002 | Audit IA | Current pointer and pack classification | Focused Python assertions in T-002 | Exactly one Current pack; every pack has README. |
| VAL-PLN-003 | Lifecycle | Spec disposition matches evidence | Focused Python assertions in T-003 | Expected active/done states and index values match. |
| VAL-PLN-004 | Evidence | Plan-to-Task relationships are explicit | Focused Python assertions in T-004 | Forty-one baseline Plans resolve Task evidence. |
| VAL-PLN-005 | Guardrail | Roster and owner-pointer drift fails | Roster validator self-test | Valid case passes; four invalid cases fail as expected. |
| VAL-PLN-006 | Repository | Full repository conformance | Quality gate and pre-commit | All required checks pass; optional skips are labeled. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical evidence is mistaken for current authority | High | Keep `done` records, add explicit owner/successor text, and avoid broad body rewrites. |
| Archive removes unique evidence | High | Apply the five-condition Archive gate; current known candidates all remain retained. |
| Monolithic Plan edits hide accidental changes | Medium | Use the approved 41-row ledger, focused assertions, and an independent review before commit. |
| Stale-word validation flags historical quotations | Medium | Restrict stale count checks to the active harness catalog. |
| Provider adapter semantics change accidentally | High | Compare filenames only; do not edit adapter files in this cycle. |
| Fixture tests pass without exercising production logic | High | Make fixture self-tests call the same `validate_contract()` function as repository validation. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Every task must pass its focused assertions and
  changed-file pre-commit checks.
- **Sandbox / Canary Rollout**: Repository-static only; the roster validator
  runs against fixture JSON before validating the real checkout.
- **Human Approval Gate**: Required before remote push, local merge to `main`,
  live runtime action, provider configuration change, model-policy change, or
  secret access.
- **Rollback Trigger**: A focused assertion, quality gate, or review identifies
  evidence loss, incorrect current ownership, or false-positive validation.
- **Prompt / Model Promotion Criteria**: Not applicable; provider models and
  prompts are out of scope.

---

### Task 1: Start the Canonical Execution Chain

**Files:**

- Modify: `docs/03.specs/025-governance-owner-and-roster-currentness/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: approved Spec 025 at commit `0473404`.
- Produces: one active Spec, one active Plan, and one active Task with task IDs
  `RCR-001` through `RCR-006` corresponding to T-001 through T-006.

- [ ] **Step 1: Write the failing reciprocal-lineage assertion**

Run this before creating the Task:

```bash
python3 - <<'PY'
from pathlib import Path

spec = Path('docs/03.specs/025-governance-owner-and-roster-currentness/spec.md')
plan = Path('docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md')
task = Path('docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md')
assert task.exists(), task
assert '../../04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md' in spec.read_text()
assert '../../04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md' in spec.read_text()
assert '../../03.specs/025-governance-owner-and-roster-currentness/spec.md' in plan.read_text()
assert '../tasks/2026-07-11-governance-owner-and-roster-currentness.md' in plan.read_text()
assert '../../03.specs/025-governance-owner-and-roster-currentness/spec.md' in task.read_text()
assert '../plans/2026-07-11-governance-owner-and-roster-currentness.md' in task.read_text()
PY
```

Expected: FAIL because the Task does not exist and the reciprocal links are not
yet present.

- [ ] **Step 2: Create the active execution record**

Set Spec 025 and this Plan to `status: active`. Create the Task from the
canonical Task template with this exact task table:

```markdown
| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RCR-001 | Start reciprocal execution lineage | doc | Interfaces & Data Structures | T-001 | Reciprocal-link assertion | platform | Done |
| RCR-002 | Normalize audit IA and relocate completed audit Plan | doc | Audit Information Architecture | T-002 | Current-pointer and pack assertion | platform | Todo |
| RCR-003 | Reconcile all Spec lifecycle and ownership records | doc | Complete Spec Disposition Ledger | T-003 | Spec status/index assertion | platform | Todo |
| RCR-004 | Reconcile all Plan-to-Task evidence links | doc | Complete Plan Evidence Ledger | T-004 | Plan evidence assertion | platform | Todo |
| RCR-005 | Enforce roster and owner-pointer currentness | guardrail | RMD-004 Implementation Components | T-005 | Fixture self-test and quality gate | platform | Todo |
| RCR-006 | Close lifecycle, evidence, and RMD-004 | doc | Success Criteria & Verification Plan | T-006 | Full validation bundle | platform | Todo |
```

Add reciprocal links in each document's `Related Documents`. Change the Spec
and Plan README rows from `Draft` to `Active`, and add the Task to
`docs/04.execution/tasks/README.md` with status `Active` and date `2026-07-11`.

- [ ] **Step 3: Run the reciprocal-lineage assertion**

Run the Step 1 command again.

Expected: PASS with no output.

- [ ] **Step 4: Run focused conformance checks**

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/03.specs/025-governance-owner-and-roster-currentness/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md \
  docs/04.execution/tasks/README.md
```

Expected: all required checks PASS.

- [ ] **Step 5: Commit**

```bash
git add \
  docs/03.specs/025-governance-owner-and-roster-currentness/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md \
  docs/04.execution/tasks/README.md
git commit -m "docs(execution): start roster currentness workstream"
```

---

### Task 2: Normalize Audit IA and Relocate the Completed Audit Plan

**Files:**

- Modify: `docs/90.references/audits/README.md`
- Create: `docs/90.references/audits/2026-05-24-whga/README.md`
- Create: `docs/90.references/audits/2026-07-02-whia/README.md`
- Create: `docs/90.references/audits/2026-07-03-wdgh/README.md`
- Create: `docs/90.references/audits/2026-07-04-wdcn/README.md`
- Modify: `docs/90.references/audits/2026-07-05-wea/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/README.md`
- Move: `docs/90.references/audits/2026-07-11-weia/implementation-plan.md`
  to `docs/04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md`
- Create: `docs/04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md`
- Modify: the six other Markdown reports under
  `docs/90.references/audits/2026-07-11-weia/`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: dated audit snapshots and the completed 967-line Stage 90 ledger.
- Produces: one Current pointer, six dated pack registry rows, a canonical
  `done` Stage 04 Plan, and a compact `done` Task.

- [ ] **Step 1: Run the failing audit-IA assertion**

```bash
python3 - <<'PY'
from pathlib import Path

root = Path('docs/90.references/audits')
packs = [
    '2026-05-24-whga', '2026-07-02-whia', '2026-07-03-wdgh',
    '2026-07-04-wdcn', '2026-07-05-wea', '2026-07-11-weia',
]
for pack in packs:
    assert (root / pack / 'README.md').exists(), pack
parent = (root / 'README.md').read_text()
assert parent.count('| Current pack |') == 1
historical = (root / '2026-07-05-wea' / 'README.md').read_text()
assert '| Current |' not in historical
assert not (root / '2026-07-11-weia' / 'implementation-plan.md').exists()
assert Path('docs/04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md').exists()
assert Path('docs/04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md').exists()
PY
```

Expected: FAIL for four missing pack READMEs, stale 2026-07-05 Current labels,
and the misplaced implementation plan.

- [ ] **Step 2: Create compact dated-pack indexes**

Create the four missing READMEs with the standard sections `Overview`,
`Snapshot Contract`, `Report Index`, `Successor or Resolution`, `Evidence
Boundary`, and `Related Documents`. Use these exact pack classifications:

```text
2026-05-24-whga  Historical  successor: 2026-07-02-whia
2026-07-02-whia  Historical  successor: 2026-07-05-wea
2026-07-03-wdgh  Resolved    resolution: 2026-07-04-wdcn
2026-07-04-wdcn  Resolved    current comparison owner: 2026-07-11-weia
2026-07-05-wea   Historical  successor: 2026-07-11-weia
2026-07-11-weia  Current     successor: none
```

List only files that exist in each pack. Do not copy report bodies into a
README.

- [ ] **Step 3: Reduce the parent and Current-pack index responsibilities**

Change the parent README to one pack-level table with columns:

```markdown
| Pack | Pack role | Snapshot scope | Successor / resolution |
```

Keep exactly one `Current pack` row for `2026-07-11-weia`. Remove the
report-by-report duplication from the parent index. In the Current pack README,
keep snapshot/method/interfaces/evidence/freshness material and condense
`Planned Logical Commits`, `Execution and Review`, and `Approval Record` into a
short completion-evidence pointer to the relocated Plan and Task.

- [ ] **Step 4: Relocate and normalize the completed execution plan**

```bash
git mv \
  docs/90.references/audits/2026-07-11-weia/implementation-plan.md \
  docs/04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md
```

Change its frontmatter to:

```yaml
title: 'Workspace Engineering Research and Implementation Audit Integration Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-11
```

Add Related Documents links to the Current pack and the new same-basename
Task. Create the Task with `status: done`, the completed 13-task summary, the
known publication commits, repository-static validation evidence, and the
explicit no-live/no-secret boundary.

- [ ] **Step 5: Repair all relocation links**

Update the parent audit README, Current pack README, and these six reports:

```text
ai-agents-model-routing-vibe-coding.md
ci-qa-automation-pipeline-workflow.md
governance-harness-loop-providers.md
kubernetes-infrastructure-security.md
remediation-roadmap.md
sdlc-document-lifecycle-frontmatter.md
```

Their link target from the Current pack is the exact relative path:

```text
../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md
```

Add the relocated Plan and Task to their Stage 04 README indexes as `Done`.

- [ ] **Step 6: Run focused validation**

Run the Step 1 assertion again, then:

```bash
rg -n 'implementation-plan\.md' docs/90.references/audits docs/04.execution
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/README.md \
  docs/90.references/audits/2026-05-24-whga/README.md \
  docs/90.references/audits/2026-07-02-whia/README.md \
  docs/90.references/audits/2026-07-03-wdgh/README.md \
  docs/90.references/audits/2026-07-04-wdcn/README.md \
  docs/90.references/audits/2026-07-05-wea/README.md \
  docs/90.references/audits/2026-07-11-weia/README.md \
  docs/04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md \
  docs/04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md
```

Expected: no active link targets the old Stage 90 path; all required checks
PASS.

- [ ] **Step 7: Commit**

```bash
git add docs/90.references/audits docs/04.execution/plans docs/04.execution/tasks
git commit -m "docs(audits): normalize audit pack information architecture"
```

---

### Task 3: Reconcile Every Spec Lifecycle and Current Owner

**Files:**

- Modify: `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
- Modify: every `spec.md` under `docs/03.specs/009-*` through
  `docs/03.specs/024-*`
- Modify: `docs/03.specs/024-observability-and-network-review-agents/agent-design.md`
- Modify: `docs/03.specs/README.md`

**Interfaces:**

- Consumes: the complete Spec disposition ledger in Spec 025.
- Produces: four active baseline Specs (004, 005, 006, 008), sixteen done
  baseline Specs (009-024), one active implementation Spec (025), and explicit
  lineage without Archive movement.

- [ ] **Step 1: Run the failing Spec-lifecycle assertion**

```bash
python3 - <<'PY'
from pathlib import Path
import re

expected = {
    '004': 'active', '005': 'active', '006': 'active', '008': 'active',
    **{f'{n:03d}': 'done' for n in range(9, 25)},
    '025': 'active',
}
for spec in sorted(Path('docs/03.specs').glob('[0-9][0-9][0-9]-*/spec.md')):
    ident = spec.parent.name[:3]
    if ident not in expected:
        continue
    status = re.search(r'^status: (\w+)$', spec.read_text(), re.MULTILINE).group(1)
    assert status == expected[ident], (ident, status, expected[ident])
agent_design = Path('docs/03.specs/024-observability-and-network-review-agents/agent-design.md').read_text()
assert 'status: done' in agent_design
PY
```

Expected: FAIL because Specs 009-024 and the 024 agent design are still draft.

- [ ] **Step 2: Apply evidence-backed lifecycle states**

Change Specs 009-024 and the 024 agent design to `status: done` and
`updated: 2026-07-11`. Keep 004, 005, 006, and 008 active. Keep Spec 025 active.

Update every affected Spec README row to the same status and date. Do not alter
the accepted status of PRD, ARD, ADR, or operations documents.

- [ ] **Step 3: Add explicit lineage and missing links**

Add these ownership statements to `## Related Documents` in Specs 009, 010,
011-015, and 020-024. Add `### Current Ownership Boundary` immediately after
`## Strategic Boundaries & Non-goals` in Spec 006:

```text
009 completed predecessor -> 017 current research lineage
010 completed predecessor -> 018 later audit-pack lineage
011 -> 012 -> 013 -> 014 -> 020 -> 021 -> 022 -> 023 completed evolution
006 runtime-gap boundary; RMD-004 implementation contract -> 025
015 completed normalization input -> 025
024 completed role-delivery evidence -> 025
```

Add missing reciprocal Plan and Task links to Specs 011, 016, and 019. Link
006, 015, and 024 to Spec 025. Link Spec 025 back to those three inputs.

- [ ] **Step 4: Narrow Spec 006 without deleting historical overlays**

Add this current-owner boundary near its Strategic Boundaries section:

```markdown
### Current Ownership Boundary

This Spec remains active only for the historical harness-gap baseline and
unresolved runtime/operator-approved boundaries. RMD-004 roster counts,
provider stem parity, and canonical-owner pointer acceptance are owned by
Spec 025 at `../025-governance-owner-and-roster-currentness/spec.md`.
Completed provider normalization and role-addition evidence remain in Specs
015 and 024.
```

- [ ] **Step 5: Run focused validation**

Run the Step 1 assertion again, then:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files docs/03.specs/README.md \
  docs/03.specs/006-workspace-harness-gap-analysis/spec.md \
  docs/03.specs/009-workspace-harness-research-pack/spec.md \
  docs/03.specs/010-workspace-harness-implementation-audit-pack/spec.md \
  docs/03.specs/011-template-contract-governance-migration/spec.md \
  docs/03.specs/012-template-governance-audit-enhancement/spec.md \
  docs/03.specs/013-workspace-document-governance-hardening/spec.md \
  docs/03.specs/014-workspace-document-contract-normalization/spec.md \
  docs/03.specs/015-agent-governance-contract-normalization/spec.md \
  docs/03.specs/016-active-control-surface-governance-hardening/spec.md \
  docs/03.specs/017-workspace-engineering-research-pack/spec.md \
  docs/03.specs/018-workspace-engineering-implementation-audit-pack/spec.md \
  docs/03.specs/019-template-path-numbering-contract/spec.md \
  docs/03.specs/020-workspace-contract-governance-normalization/spec.md \
  docs/03.specs/021-sdlc-lifecycle-contract/spec.md \
  docs/03.specs/022-control-cloud-doc-normalization/spec.md \
  docs/03.specs/023-stage03-04-repo-static-gap-closure/spec.md \
  docs/03.specs/024-observability-and-network-review-agents/spec.md \
  docs/03.specs/024-observability-and-network-review-agents/agent-design.md
```

Expected: all expected statuses, links, index rows, and quality gates PASS.

- [ ] **Step 6: Commit**

```bash
git add docs/03.specs
git commit -m "docs(specs): reconcile lifecycle and current ownership"
```

---

### Task 4: Reconcile Every Plan with Task Evidence

**Files:**

- Modify: `docs/04.execution/plans/README.md`
- Modify: the forty-one baseline Plan files listed in Spec 025's Complete Plan
  Evidence Ledger when their row requires a link, historical-instruction note,
  Spec link, or pre-Spec declaration.

**Interfaces:**

- Consumes: the 41-row Plan evidence ledger and existing done Tasks.
- Produces: one resolvable evidence Task per baseline Plan, explicit N/A for
  fourteen pre-Spec records, and no unchecked section interpreted as current
  execution authority.

- [ ] **Step 1: Run the failing Plan-evidence assertion**

```bash
python3 - <<'PY'
from pathlib import Path

plans = sorted(p for p in Path('docs/04.execution/plans').glob('*.md') if p.name != 'README.md')
baseline = [p for p in plans if p.name <= '2026-07-10-current-research-pack-fact-first-hardening.md']
assert len(baseline) == 41, len(baseline)
exception = {
    '2026-06-02-phase-1-decision-follow-up.md':
        '2026-06-02-phase-1-governance-alignment-audit.md',
}
for plan in baseline:
    task_name = exception.get(plan.name, plan.name)
    task = Path('docs/04.execution/tasks') / task_name
    assert task.exists(), (plan, task)
    text = plan.read_text()
    assert f'../tasks/{task_name}' in text, plan
    assert ('03.specs/' in text or 'Parent Spec: N/A' in text), plan
PY
```

Expected: FAIL on Plans with raw/missing Task links or missing Spec/N/A input.

- [ ] **Step 2: Normalize the sixteen explicit Task-link gaps**

Add a clickable Task link using these exact Plan-to-Task mappings:

| Plan filename | Task filename |
| --- | --- |
| `2026-05-17-template-crosslink-fix.md` | `2026-05-17-template-crosslink-fix.md` |
| `2026-05-28-workspace-skill-expansion.md` | `2026-05-28-workspace-skill-expansion.md` |
| `2026-05-30-antigravity-governance.md` | `2026-05-30-antigravity-governance.md` |
| `2026-06-02-phase-1-decision-follow-up.md` | `2026-06-02-phase-1-governance-alignment-audit.md` |
| `2026-07-02-workspace-harness-implementation-audit-pack.md` | `2026-07-02-workspace-harness-implementation-audit-pack.md` |
| `2026-07-02-workspace-harness-research-pack.md` | `2026-07-02-workspace-harness-research-pack.md` |
| `2026-07-04-active-control-surface-governance-hardening.md` | `2026-07-04-active-control-surface-governance-hardening.md` |
| `2026-07-04-agent-governance-contract-normalization.md` | `2026-07-04-agent-governance-contract-normalization.md` |
| `2026-07-04-workspace-engineering-research-pack.md` | `2026-07-04-workspace-engineering-research-pack.md` |
| `2026-07-05-template-path-numbering-contract.md` | `2026-07-05-template-path-numbering-contract.md` |
| `2026-07-05-workspace-contract-governance-normalization.md` | `2026-07-05-workspace-contract-governance-normalization.md` |
| `2026-07-05-workspace-engineering-implementation-audit-pack.md` | `2026-07-05-workspace-engineering-implementation-audit-pack.md` |
| `2026-07-06-observability-and-network-review-agents.md` | `2026-07-06-observability-and-network-review-agents.md` |
| `2026-07-06-sdlc-lifecycle-contract.md` | `2026-07-06-sdlc-lifecycle-contract.md` |
| `2026-07-07-workspace-engineering-research-pack-refresh.md` | `2026-07-07-workspace-engineering-research-pack-refresh.md` |
| `2026-07-10-current-research-pack-fact-first-hardening.md` | `2026-07-10-current-research-pack-fact-first-hardening.md` |

For each row, add `- **Task**:` followed by a Markdown link whose label and
target are `../tasks/` plus the exact Task filename in the table.

Use the recorded exception
`2026-06-02-phase-1-governance-alignment-audit.md` for the Phase 1 decision
follow-up Plan. Correct the 2026-05-17 Plan's false statement that no Task was
created.

- [ ] **Step 3: Add missing Spec links and pre-Spec declarations**

Add these two missing parent links:

```text
2026-07-06-sdlc-lifecycle-contract.md -> ../../03.specs/021-sdlc-lifecycle-contract/spec.md
2026-07-07-workspace-engineering-research-pack-refresh.md -> ../../03.specs/017-workspace-engineering-research-pack/spec.md
```

Add `- **Parent Spec**: N/A — pre-Spec execution record.` to these fourteen
Plans instead of inventing retroactive parentage:

```text
2026-05-09-github-qa-ci-remediation.md
2026-05-09-scripts-inventory-remediation.md
2026-05-10-agent-first-harness-llm-wiki-hooks.md
2026-05-22-docs-governance-full-ab-hardening.md
2026-05-22-workspace-purpose-alignment.md
2026-05-30-antigravity-governance.md
2026-05-31-codex-governance-harness-alignment.md
2026-06-01-claude-agent-surface-restoration.md
2026-06-01-stage-00-canonical-adapter-redesign.md
2026-06-02-phase-1-decision-follow-up.md
2026-06-02-phase-2-governance-alignment.md
2026-06-02-phase-3-protected-surface-hardening.md
2026-06-02-stage-00-codex-harness-coverage-reconciliation.md
2026-06-05-harness-governance-v2-overlay.md
```

- [ ] **Step 4: Label unchecked completed instructions as historical**

For the ten Plans listed in Spec 025, add this note immediately before the
first remaining unchecked execution section:

```markdown
> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.
```

Do not change `- [ ]` to `- [x]`. Update the Plan README overview to state the
same Plan-versus-Task evidence rule.

- [ ] **Step 5: Run focused validation**

Run the Step 1 assertion again, then:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files docs/04.execution/plans/*.md
```

Expected: all 41 baseline Plans resolve one existing Task and either a parent
Spec or an explicit pre-Spec N/A declaration; required checks PASS.

- [ ] **Step 6: Commit**

```bash
git add docs/04.execution/plans
git commit -m "docs(plans): reconcile execution evidence links"
```

---

### Task 5: Implement Tested Roster and Owner-Pointer Enforcement

**Files:**

- Create: `scripts/validate-agent-roster-currentness.py`
- Create: `tests/fixtures/agent-roster-currentness.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/00.agent-governance/harness-catalog.md`

**Interfaces:**

- Consumes: three provider directory stem sets and the active harness catalog.
- Produces:
  - `validate_contract(provider_stems: dict[str, set[str]], catalog_text: str) -> list[str]`;
  - CLI `python3 scripts/validate-agent-roster-currentness.py .`;
  - CLI self-test flag `--self-test`; and
  - exact deterministic errors for missing roles, provider mismatch, stale
    eight-role prose, and missing owner pointers.

- [ ] **Step 1: Create the fixture contract before the validator**

Create one JSON document with this schema and exact canonical role set:

```json
{
  "expected_stems": [
    "code-reviewer",
    "doc-writer",
    "gitops-reviewer",
    "incident-responder",
    "k8s-implementer",
    "network-reviewer",
    "observability-reviewer",
    "security-auditor",
    "supervisor",
    "wiki-curator"
  ],
  "cases": [
    {"name": "valid", "mutation": "none", "expected_error": null},
    {"name": "missing-role", "mutation": "remove-network-from-claude", "expected_error": "claude roster missing expected stems: network-reviewer"},
    {"name": "provider-mismatch", "mutation": "add-extra-to-codex", "expected_error": "codex roster has unexpected stems: extra-reviewer"},
    {"name": "stale-count", "mutation": "replace-ten-with-eight", "expected_error": "harness catalog contains stale eight-role currentness prose"},
    {"name": "bad-owner", "mutation": "remove-bootstrap-owner", "expected_error": "harness catalog missing canonical owner pointer: docs/00.agent-governance/rules/bootstrap.md"}
  ]
}
```

The validator self-test will expand each named mutation from the valid base
case and call production `validate_contract()`.

- [ ] **Step 2: Run the failing validator command**

```bash
python3 scripts/validate-agent-roster-currentness.py . --self-test
```

Expected: FAIL because the validator does not exist.

- [ ] **Step 3: Implement the minimal focused validator**

Create an executable Python script with these exact constants and functions:

```python
EXPECTED_STEMS = frozenset({
    "code-reviewer", "doc-writer", "gitops-reviewer", "incident-responder",
    "k8s-implementer", "network-reviewer", "observability-reviewer",
    "security-auditor", "supervisor", "wiki-curator",
})
REQUIRED_OWNER_POINTERS = (
    "docs/00.agent-governance/rules/bootstrap.md",
    "docs/00.agent-governance/rules/persona.md",
    "docs/00.agent-governance/rules/stage-authoring-matrix.md",
    "docs/04.execution/tasks/2026-07-06-observability-and-network-review-agents.md",
    "docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md",
    "docs/99.templates/support/documentation-contract.md",
    "docs/99.templates/support/template-routing.md",
)

def validate_contract(
    provider_stems: dict[str, set[str]], catalog_text: str
) -> list[str]:
    errors: list[str] = []
    for provider in ("claude", "codex", "gemini"):
        stems = provider_stems[provider]
        missing = sorted(EXPECTED_STEMS - stems)
        extra = sorted(stems - EXPECTED_STEMS)
        if missing:
            errors.append(f"{provider} roster missing expected stems: {', '.join(missing)}")
        if extra:
            errors.append(f"{provider} roster has unexpected stems: {', '.join(extra)}")
    if sum(len(stems) for stems in provider_stems.values()) != 30:
        errors.append("provider adapter inventory must contain exactly 30 files")
    if re.search(r"\b(?:Eight|eight) (?:local )?(?:provider adapters|agents)\b", catalog_text):
        errors.append("harness catalog contains stale eight-role currentness prose")
    for pointer in REQUIRED_OWNER_POINTERS:
        if pointer not in catalog_text:
            errors.append(f"harness catalog missing canonical owner pointer: {pointer}")
    return errors
```

Implement `repository_inputs(root: Path)` using extensions `.md`, `.toml`,
`.md` for Claude, Codex, and Gemini respectively. Implement `run_self_test()`
by loading the fixture JSON, creating one valid catalog string containing
`Ten local provider adapters` plus every required pointer, applying the five
named mutations, and comparing each case's expected error with the actual
error list. Exit 1 and print each error as `ERR ...`; otherwise print
`[PASS] agent roster currentness validation passed`.

Use this exact helper and CLI flow so fixtures and the real repository share
the same production validation function:

```python
def repository_inputs(root: Path) -> tuple[dict[str, set[str]], str]:
    providers = {
        "claude": {path.stem for path in (root / ".claude/agents").glob("*.md")},
        "codex": {path.stem for path in (root / ".codex/agents").glob("*.toml")},
        "gemini": {path.stem for path in (root / ".agents/agents").glob("*.md")},
    }
    catalog = (root / "docs/00.agent-governance/harness-catalog.md").read_text(
        encoding="utf-8"
    )
    return providers, catalog


def run_self_test(fixture_path: Path) -> list[str]:
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    if frozenset(data["expected_stems"]) != EXPECTED_STEMS:
        failures.append("fixture expected_stems does not match EXPECTED_STEMS")
    base_catalog = "Ten local provider adapters\n" + "\n".join(
        REQUIRED_OWNER_POINTERS
    )
    for case in data["cases"]:
        providers = {name: set(EXPECTED_STEMS) for name in ("claude", "codex", "gemini")}
        catalog = base_catalog
        mutation = case["mutation"]
        if mutation == "remove-network-from-claude":
            providers["claude"].remove("network-reviewer")
        elif mutation == "add-extra-to-codex":
            providers["codex"].add("extra-reviewer")
        elif mutation == "replace-ten-with-eight":
            catalog = catalog.replace("Ten local", "Eight local", 1)
        elif mutation == "remove-bootstrap-owner":
            catalog = catalog.replace(
                "docs/00.agent-governance/rules/bootstrap.md", "", 1
            )
        elif mutation != "none":
            failures.append(f"{case['name']}: unknown mutation {mutation}")
            continue
        errors = validate_contract(providers, catalog)
        expected = case["expected_error"]
        if expected is None and errors:
            failures.append(f"{case['name']}: expected no errors, got {errors}")
        elif expected is not None and expected not in errors:
            failures.append(f"{case['name']}: missing expected error {expected!r}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        errors = run_self_test(
            args.repo_root / "tests/fixtures/agent-roster-currentness.json"
        )
    else:
        providers, catalog = repository_inputs(args.repo_root)
        errors = validate_contract(providers, catalog)
    if errors:
        for error in errors:
            print(f"ERR {error}", file=sys.stderr)
        return 1
    print("[PASS] agent roster currentness validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Import `argparse`, `json`, `re`, `sys`, and `Path` from `pathlib`, and start
the file with `#!/usr/bin/env python3`. Run
`chmod +x scripts/validate-agent-roster-currentness.py` after creation.

- [ ] **Step 4: Verify RED against the real harness catalog**

```bash
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
```

Expected: self-test PASS; repository validation FAIL on the three stale
eight-role statements and missing declared owner pointers.

- [ ] **Step 5: Update the durable roster and owner pointers**

In `harness-catalog.md`:

- replace the three eight-role claims with `Ten local provider adapters`,
  `Ten local agents`, and `Keep ten local agents...` respectively;
- state `10 shared role stems / 30 provider adapters` in the roster section;
- link the bootstrap, persona, stage-authoring matrix, completed role-addition
  Task, new RMD-004 Task, documentation contract, and template-routing contract
  using the exact repository paths in `REQUIRED_OWNER_POINTERS`; and
- keep provider-specific model and tool semantics out of this RMD-004 change.

Update `scripts/README.md` with the validator CLI and update `tests/README.md`
with the fixture path, five cases, and repository-static evidence boundary.

- [ ] **Step 6: Wire the focused validator into the repository gate**

Before the monolithic embedded Python section in
`scripts/validate-repo-quality-gates.sh`, add:

```bash
python3 "$ROOT_DIR/scripts/validate-agent-roster-currentness.py" \
  "$ROOT_DIR" --self-test
python3 "$ROOT_DIR/scripts/validate-agent-roster-currentness.py" "$ROOT_DIR"
```

Both commands must be blocking. Do not duplicate the ten-role list in the
monolithic embedded Python validator.

- [ ] **Step 7: Run GREEN validation**

```bash
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
bash -n scripts/validate-repo-quality-gates.sh
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  scripts/validate-agent-roster-currentness.py \
  tests/fixtures/agent-roster-currentness.json \
  scripts/validate-repo-quality-gates.sh \
  scripts/README.md \
  tests/README.md \
  docs/00.agent-governance/harness-catalog.md
```

Expected: fixture self-test, real repository validation, shell syntax, quality
gate, and changed-file hooks all PASS.

- [ ] **Step 8: Commit**

```bash
git add \
  scripts/validate-agent-roster-currentness.py \
  tests/fixtures/agent-roster-currentness.json \
  scripts/validate-repo-quality-gates.sh \
  scripts/README.md \
  tests/README.md \
  docs/00.agent-governance/harness-catalog.md
git commit -m "fix(governance): enforce canonical roster and owner pointers"
```

---

### Task 6: Close Evidence, Lifecycle, and RMD-004

**Files:**

- Modify: `docs/03.specs/025-governance-owner-and-roster-currentness/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: commits and validation output from T-001 through T-005.
- Produces: done Spec/Plan/Task lifecycle, RMD-004 closure evidence, and a clean
  branch ready for finishing review.

- [ ] **Step 1: Run the failing closure assertion**

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('docs/03.specs/025-governance-owner-and-roster-currentness/spec.md'),
    Path('docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md'),
    Path('docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md'),
]
for path in paths:
    assert 'status: done' in path.read_text(), path
task = paths[2].read_text()
for task_id in range(1, 7):
    assert f'RCR-00{task_id}' in task
assert '| Todo |' not in task
roadmap = Path('docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md').read_text()
assert 'RMD-004 closure evidence' in roadmap
PY
```

Expected: FAIL because lifecycle and evidence are not closed yet.

- [ ] **Step 2: Record exact task evidence**

Update the Task table so RCR-001 through RCR-006 are `Done`. Add a verification
summary containing:

```text
commit hash per logical task
fixture self-test result
real roster validation result
repository quality-gate result
pre-commit --all-files result
git diff --check result
optional-tool skips, if any
no-live/no-secret/no-remote boundary
```

Do not write PASS for a command that was not executed.

- [ ] **Step 3: Close lifecycle and indexes**

Set Spec 025, this Plan, and the same-topic Task to `status: done`. Update the
Spec, Plan, and Task README rows to `Done` and `2026-07-11`. In the remediation
roadmap, add a concise `RMD-004 closure evidence` note linking Spec 025, the
Plan, the Task, the harness catalog, and the focused validator. Do not rewrite
the original audit finding or score.

Append a progress-ledger entry with layer `agent-governance`, tags
`#roster #currentness #spec #plan #audit-ia #validation`, the six logical
commits, validation commands, and safety boundary.

- [ ] **Step 4: Run the full closeout bundle**

```bash
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

Expected: all required checks PASS. Optional unavailable tools may report
SKIP, but must not be recorded as PASS.

- [ ] **Step 5: Review the complete branch diff**

```bash
git status --short --branch
git diff --stat main...HEAD
git diff --check main...HEAD
git log --oneline main..HEAD
```

Expected: only approved audit, Spec, Plan, Task, Stage 00, validator, test,
index, and memory paths changed; logical commits are visible; no unstaged
files remain after the final commit.

- [ ] **Step 6: Commit**

```bash
git add \
  docs/03.specs/025-governance-owner-and-roster-currentness/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md \
  docs/04.execution/tasks/README.md \
  docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md \
  docs/00.agent-governance/memory/progress.md
git commit -m "docs(governance): close roster currentness evidence"
```

## Completion Criteria

- [ ] Audit parent README has one Current pointer and one row per dated pack.
- [ ] Every dated audit pack has a compact README and an explicit pack role.
- [ ] The completed audit integration Plan and Task live in Stage 04.
- [ ] Twenty baseline Specs and Spec 025 match the approved disposition ledger.
- [ ] Forty-one baseline Plans retain done evidence and resolve a Task.
- [ ] No known candidate was archived without passing all five Archive gates.
- [ ] Harness catalog states ten shared roles and thirty provider adapters.
- [ ] Canonical owner pointers match the Spec 025 allowlist.
- [ ] Valid fixture and actual repository pass; four negative fixtures fail for
  their expected reason.
- [ ] Spec 025, its Plan, and its Task are done with reciprocal links.
- [ ] Full repository quality gates, `git diff --check`, and
  `pre-commit run --all-files` pass or environmental limitations are recorded.

## Traceability

- **Spec**:
  [../../03.specs/025-governance-owner-and-roster-currentness/spec.md](../../03.specs/025-governance-owner-and-roster-currentness/spec.md)
- **Task**:
  [../tasks/2026-07-11-governance-owner-and-roster-currentness.md](../tasks/2026-07-11-governance-owner-and-roster-currentness.md)
- **Current Audit Pack**:
  [../../90.references/audits/2026-07-11-weia/README.md](../../90.references/audits/2026-07-11-weia/README.md)
- **Remediation Roadmap**:
  [../../90.references/audits/2026-07-11-weia/remediation-roadmap.md](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
- **Harness Catalog**:
  [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
