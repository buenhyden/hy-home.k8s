---
title: "W03 Closing Records Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0209-PLAN-0001"
parent_ids: ["SPEC-0209"]
---

# W03 Closing Records Implementation Plan

## Overview

### Goal and Boundary

Record the decision row W03-D67, then write the `common_forms` candidate record with its refusal test, append the adoption facts, the approval evidence request, the writer delegation and current writer state and the disposition input, correct the 14 stale registry strings with their failing-first pin, append the corrections and the closing summary, and close W03-H19, W03-H21 and W03-H31 through the ledger cycle. [Task 0001](tasks/tsk-0001-w03-closing-records.md) owns execution and evidence.

In scope:

- The `common_forms` record, its refusal test and the four-fact table; the six-field evidence request; the writer delegation table and current writer state; the corrections, the 14 string corrections and the closing summary; the closure of W03-H19, W03-H21 and W03-H31.

Out of scope:

- The W03-H20 closing report and the old-obligation classification; any rewrite of a recorded row; any invented approval; cross-repository adoption (W11); any form, profile or template change; Q-07; tags and hosted CI.

#### Global Constraints

This draft work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds four constraints: no recorded Task row, evidence row, decision, handoff or cell is rewritten, and the SPEC-0161 Task changes by appended lines, the `State` and `Closure` cells of the residue rows this package closes, and its frontmatter `version` and `updated`; no approval, approver, date, scope, migration or rollback is invented, and a fact without a record stays `unverified`; no registry value is copied into the ledger or into a second Task owner; and the diagnostics of the four strict document validators over the tree are equal before and after.

### Assumptions

Read at `main` `81096a83` (a base to re-read at commit time):

- `docs/03.specs/` holds one package, SPEC-0161, whose Task is `completed`, carries sections appended after completion and has no Writer Delegation, Corrections or Adoption Facts section; its `W03 Decisions` table holds W03-H19, W03-H21 and W03-H31 as open handoffs.
- SPEC-0191 (approved, branch `claude/w03-work-residue-ledger`, not merged) adds the ledger, the gate and the `Residue Handoff` table, which lives in the SPEC-0161 Task; its seed lists `W03-H19` (`adoption`, `common_forms`), and the `shared_contract` entry is withdrawn by commit `842389de` on its branch (EVD-054 and EVD-018 of the SPEC-0191 Task) under the user's 2026-11-14 decision (Decision 3 of the Spec).
- The registry `common_forms` object is closed with three properties; the `shared_contract` object carries the candidate fields and the conditional rule that admits `unverified` only beside an `approval_ref`; the registry holds 32 `migration.meaning_map` strings, 14 of them ending "the Task records it".
- `git diff --name-only f4abea64 81096a83` (`f4abea64` is the parent of the SPEC-0168 implementation commit) lists 213 files: 117 that are W03's own, 26 W05 files (five scripts and 21 tests), six W01 files, `document-lifecycle.md` (W04) and 63 that no `Primary Writers` row names; no W06, W07 or W10 row file was edited.
- ADR-0060 is accepted without `layer`; 35 ADRs are accepted and 34 carry `layer`. REQ-0003 holds a recovery proof for every exited package SPEC-0169 to SPEC-0185 that the stale strings name.
- The packages SPEC-0192 to SPEC-0208 are drafts or approved and unmerged; their merged state decides the final counts, so every count is re-read at implementation.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CLOSING-001](spec.md#criteria) | The `common_forms` candidate record, schema properties, reader and failing-first refusal test; the `Common Form Adoption Facts` and `Approval Evidence Request` tables; the ledger closure of W03-H19. | The decisions of W03-D67; SPEC-0191 merged; SPEC-0208 merged. | [Task 0001](tasks/tsk-0001-w03-closing-records.md) | Failing test first, then passing; strict registry validator; the ledger gate; append-only diff. |
| WORK-002 | [VAL-CLOSING-002](spec.md#criteria) | The `Writer Delegation` table and current writer state from the Git diffs; the 14 `meaning_map` corrections; the `Corrections` table and closing summary; the closure of W03-H21 and W03-H31; regression and exact-index QA. | WORK-001; the packages that write `migration` strings merged. | [Task 0001](tasks/tsk-0001-w03-closing-records.md) | Strict validators, suites, the ledger gate, append-only diff, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators before any change.
- Read every figure again from the tree and the Git diffs before writing it; record each observed count beside the figure of the Spec.
- Show the refusal test and the string pin failing before the schema, reader and registry changes and passing after, on temporary trees; no test runs a gate over the repository.
- Run the ledger gate before and after the closure commit and confirm the diff of the SPEC-0161 Task has added lines, the two closure cells per row and the frontmatter only.
- Count the stale strings before and after the registry edit and confirm the `SPEC-nnnn` tokens remain.
- Architecture compliance: the work stays within AD-0006 and the shared-contract record shape and adds no gate, validator or CLI option.
- Record the risk class (`medium`: a registry, schema and reader change and appended Task records; no permission, secret-handling, hook or workflow) and the core-diff checklist.

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` with its approval receipt; the decisions are recorded as W03-D67. The six `WGOV-CORE` facts may stay `unverified` at completion: that is the recorded state, not a failure.

### Stage Placement

- Merge order: SPEC-0191, SPEC-0207, SPEC-0192 to SPEC-0204 as their dependencies allow, SPEC-0205, SPEC-0206 after SPEC-0204, SPEC-0208, SPEC-0210, SPEC-0212, this package, then the W03-H20 report (SPEC-0211) (the Spec lists the steps).
- Commit order: (1) the package commit with this Task, the Korean Stage 03 README entry and the decision row W03-D67 (re-read the next free number at commit time); (2) `.secrets.baseline` changes alone, for the reviewed digests of this Task and of the appended rows; (3) the registry commit: the `common_forms` record, schema, reader, test and the 14 string corrections; (4) the SPEC-0161 Task commit: appended tables, evidence rows and the closing summary; (5) after the user's acceptance, the closing commit that appends the `PASS` closure rows, changes the closure cells and deletes the terminal entries; (6) the package exit. Run the staged lifecycle check before each commit.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **An approval is recorded that no record proves.** Possible, Severe: HIGH, mitigate. Owner: W03 author. Every fact row names its record, a fact with none stays `unverified`, and the evidence list is a request to the user. Review cue: each row of the two fact tables. Signal that raises it: a date or name without a cited record. Rollback: revert the Task commit.
- **The Task part lands before the final counts exist.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The package merges after every package that changes a form, a TemplateDefinition, a writer file or an ADR; counts are re-read at commit time. Review cue: the diff against current HEAD.
- **A registry edit conflicts with a concurrent form package.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The edit is last in the order and changes strings in place, so line counts and baselined lines do not move. Review cue: the strict registry validator and the secret-scan baseline.
- **The corrections are read as rewriting history.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. Only appended rows and the two closure cells change; the append-only diff is recorded. Review cue: the `git diff` of the SPEC-0161 Task.
- **The digest cannot be recomputed from the repository.** Likely, Minor: LOW, monitor. Owner: the user. The source file is untracked; the digest is recorded as the reviewed bytes and the limit is stated. Review cue: any request to verify the digest.
- **Not scored:** whether the other repositories hold a record that would make the approval verifiable. No evidence in this workspace shows it; W11 is the first review cue.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| The adoption record of COMMON-DOC-FORM-1 as a shared-contract candidate | [Document authoring](../../../.agents/governance/document-authoring.md) | The Document authoring policy paragraph on the shared contract names the COMMON-DOC-FORM-1 candidate record that `common_forms` holds, beside the registry's `shared_contract` record. | The paragraph on the shared contract and the registry's `shared_contract` record |
