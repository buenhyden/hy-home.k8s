---
title: "W03 Retired Identity Reservation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0180-PLAN-0001"
parent_ids: ["SPEC-0180"]
---

# W03 Retired Identity Reservation Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document text changes other than the one policy sentence, the SPEC-0161 Task rows named in the Spec and this package's README entry, and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Derive retired identities from `Archived Lineage` first cells, pass them to the identity reuse check from every caller, refuse a new document that reuses one or a child of one, add the refusal tests and update the policy sentence. [Task 0001](tasks/tsk-0001-w03-retired-identity-reservation.md) owns execution and evidence.

## Context

The SPEC-0161 Task recorded the gap (EVD-023) and observed it with a synthetic probe (EVD-024): a new document reusing `SPEC-0165`, which left through Git history, returned no diagnostic. A read of the current tree found:

- six documents with an `Archived Lineage` table, whose first cells name about 200 identities in three shapes: a bare identity, an identity with `(superseded)`, and a title with the identity in parentheses;
- three current requirements (`REQ-0001`, `REQ-0002`, `REQ-0003`) whose identities `REQ-0004`'s lineage names as superseded, all unchanged at their paths;
- `artifact_identity_reuse_diagnostics` called by `compare_lifecycle`, which holds no text, and by two cumulative-history calls that hold snapshot texts; `_evidence_context` receives both text maps and builds the context `compare_lifecycle` reads;
- `_archived_lineage_text`, which the package-exit check already uses to find lineage sections.

## Goals & In-Scope

- Code: one public lineage-identity helper; the evidence-context field; the reuse check and its callers; a per-commit memo in the history cache.
- Tests: the refusal and pass cases the Spec lists.
- Policy: one sentence in the lifecycle policy.
- Tracking: in the SPEC-0161 Task, with the package commit, the decision rows W03-D22 to W03-D24, the 2026-11-13 gap-audit tracking rows and evidence rows.

## Non-Goals & Out-of-Scope

- Lineage rows and other documents; a registry key; implementing W03-H04, the generator, H07 or the audit rows' work; phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RETIRED-001](spec.md#success-criteria--verification-plan) | Lineage-identity helper; reuse check and callers; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-retired-identity-reservation.md) | Failing test first, then passing; lifecycle suite. |
| WORK-002 | [VAL-RETIRED-002](spec.md#success-criteria--verification-plan) | Policy sentence; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-retired-identity-reservation.md) | Strict validators, suites, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators before any change.
- Show the retired-identity case passing the old check (no diagnostic), then failing the new one; show the existing documents and a package exit passing.
- Commit order: the package commit with this package's entry in `docs/03.specs/README.md` and the SPEC-0161 rows; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006 and ADR-0056 unchanged.
- Record the risk class (`medium`: a lifecycle validator and its tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **The check refuses a legitimate new document.** Possible, Minor: LOW, monitor. Owner: W05 code. A lineage first cell already names live identities (`REQ-0001` to `REQ-0003`), but only identities new at a path are judged; the pre-approval review's replay over 120 recent commits found no hit, and the implementation re-runs it as Task evidence. Review cue: a new diagnostic in the tree run. Signal that raises it: a stray token in a first cell. Rollback: revert the implementation commit.
- **A comparison path misses the retired set.** Unlikely, Minor: LOW, monitor. Owner: W05 code. The set travels on the evidence context and the two direct calls read cached texts; end-to-end tests cover a comparison and a history call. Review cue: those tests. Signal that raises it: a new caller of the reuse check. Rollback: a follow-up change.
- **The cumulative-history path slows down.** Possible, Minor: LOW, monitor. Owner: W05 code. The review measured about 26 ms to scan one snapshot's texts, which the implementation re-measures as Task evidence, so the set is memoized per commit. Review cue: suite run time. Signal that raises it: a budget diagnostic. Rollback: revert the implementation commit.
- **A reservation is lost when its lineage row is deleted later.** Possible, Moderate: MEDIUM, accept with review. Owner: W03 author. Lineage rows are manual under ADR-0056; the Spec states the limit. Review cue: a lineage row removal in review. Signal that raises it: a deleted lineage row. Rollback: restore the row from Git history.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Retired identities reserved by `Archived Lineage` | [Document lifecycle policy](../../../.agents/governance/document-lifecycle.md) | Identity sentence; check in `scripts/document_lifecycle.py` |
