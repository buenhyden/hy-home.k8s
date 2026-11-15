---
title: "W02 3.0.1 Disposition"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0219-TSK-0001"
parent_ids: ["SPEC-0219-PLAN-0001"]
---

# Task: W02 3.0.1 Disposition

## Scope

### Objective and Parent

This Task executes WORK-001 and WORK-002 of the [Plan](../plan.md) for [SPEC-0219](../spec.md) criteria VAL-W02D-001 and VAL-W02D-002.

### Inputs and Authority

- **Request:** on 2026-11-15 (Asia/Seoul) the user pasted the PKG W02-DISPOSITION prompt (sha256 `4a529ddbfcc08a28…`) and approved the withdrawal of groups A, B, C and D (answer "A: closed audit questions, B: superseded old-package surveys, C: cross-repository checks, D: rule_id binding"). This approves no Spec or Plan bytes and no criterion.
- **Base:** `main` at `c6513839`; branch `claude/w02-disposition`.
- **Survey:**
  - the 57 ledger entries with their live rows;
  - the PKG requirement mapping (U23 and R13 to W02; U27 to W05-GATES; U55 and R20 to Q07-CUTOVER);
  - W11-ACCEPT, which has no cross-repository step;
  - a read-only subagent audit of history dependencies in `scripts/` and `tests/`, which ran no check;
  - `git ls-remote`, `gh release list` and `gh pr list` counts.
- **Design summary:**
  - Reference designs: D00, D14 and D15, edition 3.0.1, with S25 and S28.
  - Current difference: closed and superseded items are still active, and obligations are stated as legacy rows.
  - Choice: close only the user-approved items and the two transfers; state the rest by function; prepare the cutover targets.
  - Rejected alternatives: close everything historical without approval, which breaks Q04; leave the audit questions active, which breaks R13.
  - Interface: the ledger and the SPEC-0161 Task tables.
  - Failure: the ledger gate refuses drift.
  - Risk: a withdrawal read as completion, mitigated by the closure wording.
  - Acceptance: VAL-W02D-001 and VAL-W02D-002.

- **Allowed Paths**: `docs/03.specs/0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md` (the 18 live rows, the two seeds, appended tables and rows, frontmatter `version` and `updated`), `docs/03.specs/work-residue-ledger.json`, `docs/03.specs/0219-w02-disposition/`, `docs/03.specs/README.md`, `.secrets.baseline` (reviewed entries only)
- **Forbidden Paths**: `_workspace/`, `scripts/`, `tests/`, `.agents/`, `.claude/`, `.codex/`, `docs/99.templates/`, every other repository
- **Approval Required**: Spec and Plan approval; criterion acceptance
- **Static Validation**: ledger gate after each step; four strict document validators; `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface in scope
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: delete the branch `claude/w02-disposition`; `main` is unchanged
- **Evidence Location**: this Task

## Execution Log

### Work Performed

Read-only survey on 2026-11-15. No file outside this package is edited yet.

### Blockers and Decisions

Waiting for Spec and Plan approval.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W02D-001](../spec.md#criteria) | Close the 18 approved or transferred entries. | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-W02D-002](../spec.md#criteria) | Seeds, disposition table and cutover targets. | platform | draft | NOT_RUN | EVD-002 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-W02D-001](../spec.md#criteria) | WORK-001 | Ledger gate after each closure step | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-W02D-002](../spec.md#criteria) | WORK-002 | Ledger gate and strict document validators | Implementation snapshot | NOT_RUN | Pending | yes | none |

### Resolution Links

No earlier failure is open.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-W02D-001](../spec.md#criteria) | pending | none | Run WORK-001 after approval | platform |
| [VAL-W02D-002](../spec.md#criteria) | pending | none | Run WORK-002 after approval | platform |

### Remaining Conditions

Spec and Plan approval, the two work units and criterion acceptance remain.

## Handoff

### Promotion Receipt

The Plan promotes none.

### Next Owner

The user, for Spec and Plan approval; then platform.
