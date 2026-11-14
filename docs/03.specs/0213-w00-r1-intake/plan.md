---
title: "W00 r1 Intake and Residue Correction Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0213-PLAN-0001"
parent_ids: ["SPEC-0213"]
---

# W00 r1 Intake and Residue Correction Implementation Plan

## Global Constraints

This draft work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds four constraints: it writes only appended rows and tables, the listed in-place cells of the live `Residue Handoff` table with their ledger entries, one REQ-0003 sentence and one Stage 03 README sentence, and no recorded Task row, evidence row, decision or legacy cell is rewritten; it reads `_workspace/` only and writes nothing there; no code, test, registry, template or policy file changes; and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Re-read the tree, hash the r1 inputs, append the edition and correction tables, classify every live obligation and ledger entry, seed the still-missing lost handoffs, close W00-H01 and W01-H01 only where their reads are evidenced, edit twelve cells, thirteen if the W00-H01 owner edit applies (W03-H02, GOV-04, R147-03, OPEN-01, OPEN-02, OPEN-03, OPEN-04, OPEN-06, W03-H15, W03-H29, SDLC-07, R45-12), record the SPEC-0161 lifetime and the six decisions, and check the gate on a scratch negative copy. [Task 0001](tasks/tsk-0001-w00-r1-intake.md) owns execution and evidence.

## Context

Read at `main` `035143d1`:

- The SPEC-0161 Task holds the Inputs of the v14.7 edition, the legacy handoff tables (registered historical in the Stage 99 registry) and the live `Residue Handoff` table (83 rows, 76 open, 7 terminal); the ledger `docs/03.specs/work-residue-ledger.json` holds 76 open entries. The gate refuses a table with "Handoff" or "Conflicts" in its heading or an H-ID in its first column unless it is the live table or registered historical, a terminal row whose `Closure` is not a PASS row, an open row without an entry, an entry without a row, and a row and entry that differ in state, owner or resume condition.
- The r1 root holds the W00 prompt (`fb8e6305`), the r1 `REQUIREMENTS.json` (`21371ac5`) and the diff `reports/TASK-CHANGES.diff`; the v14.7 root is gone, so the Task takes changed requirement rows from the diff only.
- The frozen SPEC-0166 and SPEC-0167 Tasks (`579280f2`, `3270cb00`) name the handoffs the seeds restate. SPEC-0209 (approved) assigned the classification to the W03 closing report; W03-D77 moves its creation here and the closing report re-reads it.

## Goals & In-Scope

- The `r1 Edition Delta`, `Input Corrections` and `Change Contract Classification` tables; the seeds; the closures; the twelve cell edits; the lifetime record; the decision rows W03-D77 to W03-D82.

## Non-Goals & Out-of-Scope

- Any code, test or policy change; the closure of GOV-04 and R147-03 (SPEC-0205; their owner cell is edited here); the owner edits of OPEN-07, DOC-12 and DOC-S99 (SPEC-0211); the closing report; the delegation and stale-tracking corrections (SPEC-0209); the work of the seeded rows; a package exit; hosted CI.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-INTAKE-001](spec.md#success-criteria--verification-plan) | Hash the r1 inputs and read the r1 W00 diff; append `r1 Edition Delta` and `Input Corrections`; classify every live row and entry in `Change Contract Classification`; append W03-D77 to W03-D82. | The decisions of W03-D77 to W03-D82; SPEC-0191 and SPEC-0195 merged. | [Task 0001](tasks/tsk-0001-w00-r1-intake.md) | Hashes re-read; counts re-read; one class and one owner per row; validators equal before and after. |
| WORK-002 | [VAL-INTAKE-002](spec.md#success-criteria--verification-plan) | Seed the still-missing lost handoffs (seven at draft; covered items are recorded as covered); close W00-H01 and W01-H01 through the ledger cycle only where their reads are evidenced; edit the twelve cells, thirteen if the W00-H01 owner edit applies (W03-H02, GOV-04, R147-03, OPEN-01, OPEN-02, OPEN-03, OPEN-04, OPEN-06, W03-H15, W03-H29, SDLC-07, R45-12); record the lifetime in the Task, REQ-0003 and the README; negative copy. | WORK-001. | [Task 0001](tasks/tsk-0001-w00-r1-intake.md) | Gate PASS at each step and at the recorded counts; negative copy refused; strict validators, staged lifecycle check, exact-index QA and hooks. |

## Verification Plan

- Record the four strict document validators and the gate before any change.
- Re-hash each r1 file the table names; read the live rows, the ledger entries and the next free numbers (decisions, EVD, stage-numbered handoff IDs) from the tree, not from the Spec.
- For W01-H01 show, from the SPEC-0166 frozen Task and its commits, that each of the four files of the row (`document-authoring.md`, `sdlc.md`, `quality.md`, `git.md`) was read and edited; if one is not shown, keep that row open and report it.
- For OPEN-04 search the r1 root by file name and content for the two originals and record the result.
- Ledger cycle per closure (W00-H01 and W01-H01 only): make the entry and row terminal with the new PASS EVD, run the gate, delete the entry, run the gate; seeds: add the entry and row together, run the gate.
- Build the negative copy in a scratch tree, show the four refusals, and delete it.
- Architecture compliance: no AD, ADR, governance policy, registry, template or code file changes.
- Commit order: lands right after SPEC-0195 and before the other pending W03 packages (W03-D77); the package commit appends W03-D77 to W03-D82 (re-read the next free numbers; W03-D74 to W03-D76 are already recorded by the SPEC-0195 package commit), rebases on `main` and re-counts rows and entries first. SPEC-0209's `Disposition Input` then appends status rows only and SPEC-0211's report cites this table; both are edited and re-approved separately (W03-D81).
- Record the risk class (`low`: records and ledger data, one sentence in a requirement and one in a README; no code, permission, secret handling, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor). Each MEDIUM row names a review cue and the signal that raises it.

- **A closure PASS is read as more than its read or survey.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The two closure rows (W00-H01, W01-H01) state what the PASS records and nothing beyond it. Review cue: any `Location` cell without its evidenced read. Signal that raises it: a later row or report citing a closure as evidence of a wider review.
- **The four open historical rows (OPEN-01, OPEN-02, OPEN-04, OPEN-06) are read as live blockers, or stay without a single owner.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. Each gets owner W00 and the resume "only on a shown owner difference" (W03-D82), treated as `HISTORICAL_AUDIT_NOT_GLOBAL_BLOCKER`; ADR-0060 refuses a package exit with an open entry, so SPEC-0161's W11 exit change must close them with PASS rows naming verdict and unclaimed scope. Review cue: the W11 gate or closing report treating one as blocking. Signal that raises it: the SPEC-0161 exit change not closing them.
- **A classification is read as proof that the W00 completion test holds.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The Spec ties the test to the last W03 package and SPEC-0211. Review cue: a row marked complete for OPEN-07. Signal that raises it: SPEC-0211 not citing this table.
- **A seed restates what the tree already covers.** Likely, Minor: MEDIUM, mitigate. Owner: W05, W07, W04 or W01 per row. Observed: `tests/test_shared_contract_binding.py` (438 lines) already covers the approved and adopted stages and the approval facts, so the `shared_contract` item is compared by test name and not seeded unless a field is uncovered; the W04 row is checked against R147-07. Review cue: a seed without its survey result in the Task. Signal that raises it: a second seed found covered.
- **The single owner chosen for GOV-04, R147-03, OPEN-03 or the four OPEN rows is contested.** Possible, Minor: LOW, mitigate. Owner: W03 author. The basis cites the PKG line and the SPEC-0166 trace; a different owner is one correction row.
- **A concurrent package edits the live table or the ledger.** Possible, Minor: LOW, mitigate. Owner: W03 author. Rebase, re-read counts, rerun the gate.
- **Digests in the Task trip the secret scan.** Likely, Minor: MEDIUM, mitigate. Owner: W03 author. Reviewed `.secrets.baseline` entries only. Review cue: every added baseline entry matches a hash this package wrote. Signal that raises it: a hook failure on the exact index.
- **Residual: the v14.7 `REQUIREMENTS.json` bytes are absent.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Changed requirement rows are taken from the r1 diff and the Task says the delta is partial. Review cue: the Task's statement of how many rows the diff names. Signal that raises it: a requirement row that r1 changes and no diff hunk shows.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` with its approval receipt; the decisions are recorded as W03-D77 to W03-D82.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| SPEC-0161 stays the residue owner until W11 and exits when the ledger is empty (single exception to the active-only rule) | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | The Scope and Non-goals paragraph that names SPEC-0161 (PATCH step; operator approval is the W03-D80 answer and the Spec approval) |

The same statement is also written, for readers of the stage, in the sentence of the [Stage 03 README](../README.md) that says how long SPEC-0161 stays; that README is a reader view and not a durable-contract owner, so it has no Promotion row.
