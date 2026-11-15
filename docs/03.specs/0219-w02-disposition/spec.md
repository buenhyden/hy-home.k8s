---
title: "W02 3.0.1 Disposition"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0219"
---

# W02 3.0.1 Disposition Technical Specification (Spec)

## Overview

### Intent

This Spec applies the W02-DISPOSITION stage of the external workspace governance package 3.0.1 (`_workspace/governance/workspace_governance_3_0_1_20261115/`, called PKG below) to this repository. Its goal is that finished facts are not implemented again and that real unfinished work stays with its current owner. The consumer is every stage owner that reads the work residue ledger and the SPEC-0161 Task. The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-w02-disposition.md) records execution.

A read of `main` at `c6513839` on 2026-11-15 found the following:

- **Open work.** The only open package is SPEC-0161. Its live `Residue Handoff` table and the work residue ledger hold 57 open entries. Many state their residue as a legacy table row of an earlier package, not as a function with a completion condition.
- **Closed or superseded items still active.** Five entries are closed audit questions or requests for comparison with original text: OPEN-01, OPEN-02, OPEN-04, OPEN-06 and W00-H01. Six are surveys of an earlier package that the 3.0.1 stage prompts and the work-lifecycle Intake now cover: OPEN-03, OPEN-07, W05-H02, W05-H03, W06-H01 and W07-H01. Three ask for checks across four repositories, which D00 and every 3.0.1 prompt place outside this workspace's authority: R45-12, W03-H09 and W03-H32. Two carry a rule_id binding with no basis in the 3.0.1 requirements: W01-H02 and DOC-S00.
- **Duplicates.** OPEN-09 repeats DOC-S99 (hard-coded headings in tests), and PR-DURING repeats the CI-SCOPE decision.
- **Unrecorded obligations.** A read-only audit of `scripts/` and `tests/` found two groups that no ledger entry carries. The first is checks of finished one-time transitions and compatibility branches for older registry generations, which U27 assigns to W05-GATES. The second is checks bound to history or numbering that break at the final cutover: ADR, SPEC and REQ number reservations, `reserved_codes`, `git log --all` lookups of historical paths, and the registered historical tables of the ledger gate. U55, R20 and D14 assign these to Q07-CUTOVER.
- **Final cutover targets.** The remote has 4 branches, 10 tags, 1 Release and 285 pull requests. Locally there are 5 branches, 1 worktree and three scratch clones in the session scratchpad.

### Owning Requirements

PKG W02 requirements U23 (re-evaluate closed audit identifiers and current owners) and R13 (remove closed audit questions from active prompts and gates), with Q04 (withdraw unfinished work only by explicit per-item approval) and D14 (prepare the final cutover targets only). In this repository they apply through [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md), the residue and handoff record. [ADR-0060](../../02.architecture/decisions/0060-work-residue-ledger-amendment.md) owns the ledger. This change conforms to it and amends nothing.

## Scope

### In Scope

- In the SPEC-0161 Task:
  - the closure of 18 live `Residue Handoff` rows with their EVD rows;
  - two seeded rows, W05-H09 and Q07-H01;
  - an appended `W02 Disposition` table, an appended `Q07 Target Preparation` table, one EVD row;
  - its frontmatter `version` and `updated`.
- `docs/03.specs/work-residue-ledger.json`: the matching 18 terminal entries, which are then deleted, and the 2 new entries.
- This package, the Stage 03 README entry, and reviewed `.secrets.baseline` entries.

Decision. On 2026-11-15 the user approved the withdrawal of four groups (answer "A: closed audit questions, B: superseded old-package surveys, C: cross-repository checks, D: rule_id binding"):

- A: OPEN-01, OPEN-02, OPEN-04, OPEN-06 and W00-H01.
- B: OPEN-03, OPEN-07, W05-H02, W05-H03, W06-H01 and W07-H01.
- C: R45-12, W03-H09 and W03-H32.
- D: W01-H02 and DOC-S00.

The answer is the per-item approval Q04 requires. OPEN-09 into DOC-S99 and PR-DURING into CI-SCOPE are transfers, because the obligation stays open in the receiving row; they are not withdrawals. Open question: none.

### Non-goals

- No change to code, tests, policies, registry or forms. The class C removals are W05-GATES's; the class B conversions are Q07-CUTOVER's.
- No remote history removal, renumbering, branch, tag, Release or pull request deletion (PKG W02 step 6).
- No closure of any entry the user did not approve, and no change to other repositories (W02 step 4).
- No write to `_workspace/`.

## Behavior Contract

### Normal Behavior

- **Closure cycle.** Each of the 18 rows gets State `terminal` and a Closure that names one PASS EVD row of the SPEC-0161 Task, with one row per group (A, B, C, D, transfer).
  - The row is withdrawn by the user's approval or transferred, and it is not marked as completed work.
  - The matching ledger entry is made terminal, the gate runs, the entry is deleted, and the gate runs again.
  - The ledger goes from 57 entries to 39, then to 41 with the two seeds.
- **Seeds.** Each new entry has a matching live row (kind `handoff`, State `open`, Closure `none`).
  - W05-H09, owner W05: remove the checks of finished one-time transitions and the older-generation compatibility branches the audit names, with their tests, and replace any guarantee they still give with a current contract. Resume: when W05 starts.
  - Q07-H01, owner Q07: convert or remove the checks bound to history or numbering before the final cutover rewrites history and renumbers documents. Resume: in the Q07-CUTOVER task, after W11.
- **W02 Disposition.** One row for each of the 41 open entries, with columns No., ID, Function, Owner, Completion condition and Kept because.
  - The first column is a running number, never a residue ID, and the heading names no residue table.
  - It states each remaining obligation by function, owner and completion condition, as W02 step 3 asks. The live rows keep their pointers.
- **Q07 Target Preparation.** The remote branches, tags, Release and pull-request refs, local branches, worktrees, scratch clones, the class B code dependencies, and the residue that the cutover itself must not leave behind (D14, S25).
  - Each target has a count or list and an owner.
  - Nothing is deleted.

### Failure and Edge Cases

- A closure row or seed edited alone is refused by the gate (`RESIDUE-DRIFT`, `RESIDUE-JSON-ONLY`, `RESIDUE-MARKDOWN-ONLY`, `RESIDUE-CLOSURE`).
- An entry the user did not name is never closed.
- Rollback before merge is deleting the branch; after merge, reverting the merge commit.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-W02D-001 | The 18 rows are terminal, each closed by a PASS row that names the user's approval or the receiving row. Their ledger entries are deleted, and no other entry is closed. |
| VAL-W02D-002 | W05-H09 and Q07-H01 exist as a live row and ledger entry that agree. The `W02 Disposition` table states function, owner and completion for all 41 open entries. The `Q07 Target Preparation` table lists every target with its owner and deletes nothing. The ledger gate passes at 41 entries. |

### Evidence Requirements

- The ledger gate after each step, the four strict document validators, and `python3 scripts/qa.py staged` through the hooks.
- Risk class `low` (records and ledger data only): focused checks and the author's self-check (Q08).
- Limits: repository-static only.

## References

### Normative and Evidence

- [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [ADR-0060](../../02.architecture/decisions/0060-work-residue-ledger-amendment.md), the [work residue ledger](../work-residue-ledger.json) and the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md).
- PKG W02 prompt `prompts/W02-DISPOSITION.md` (`4a529ddb…`) and D14 (`1de9bc09…`).

### Historical and Navigation

- SPEC-0213 (exited) recorded the earlier change contract classification of these entries.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W02D-001 | [ADR-0060](../../02.architecture/decisions/0060-work-residue-ledger-amendment.md) | Ledger gate after each closure step. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W02D-002 | [ADR-0060](../../02.architecture/decisions/0060-work-residue-ledger-amendment.md) | Ledger gate at 41 entries; tables read against the ledger. |
