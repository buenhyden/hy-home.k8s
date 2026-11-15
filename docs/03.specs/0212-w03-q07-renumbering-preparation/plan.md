---
title: "W03 Q-07 Renumbering Preparation Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0212-PLAN-0001"
parent_ids: ["SPEC-0212"]
---

# W03 Q-07 Renumbering Preparation Implementation Plan

## Overview

### Goal and Boundary

Survey every number space, allocator, reference and consumer; record the transition design; rehearse it on a scratch copy and record the output; confirm the SPEC-0180 reservation and complete it only if the survey shows a hole; record this package's evidence rows and, at closure, the REQ-0003 lineage row. [Task 0001](tasks/tsk-0001-w03-q07-renumbering-preparation.md) owns execution and evidence. The package lands before SPEC-0211 (the closing report) and after SPEC-0210 and the phase-3 registry packages, so the survey reads the final W03 tree.

Goals and in-scope:

- The survey record, the design record, the rehearsal record and the non-reuse confirmation in the Task; the Registry Schema Version level (NO_CHANGE); on the conditional path only, the completed reservation with failing-first tests.
- This package's evidence rows in the SPEC-0161 Task and the REQ-0003 completed-spec lineage row at closure. No decision row: W03-D75 and W03-D76 are recorded by an earlier commit.

Non-goals and out-of-scope:

- Any real renumbering, the reform of the old rule and the next-number guard (Q-07 task, W03-D76), removal of `Archived Lineage`, a committed mapping or rehearsal script, the DOC-12 closure or reassignment (SPEC-0211), a SemVer reset, a registry change, the Q-07 task itself, hosted CI.

#### Global Constraints

This draft work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds four constraints: no real path, document ID, anchor, allocation bound or Stage directory name changes, and no new real number (`SPEC-0001` included) is consumed; the rehearsal runs only on a scratch copy outside the repository and nothing of it is committed; the live DOC-12 row, its ledger entry, W03-H20 and W03-H24 are not touched (the row stays stale until SPEC-0211 edits it); and the diagnostics of the four strict document validators over the tree are equal before and after.

### Assumptions

Read at `main` `eb017bfe` (after pull request #262, SPEC-0208) and refreshed at `035143d1` (SPEC-0194 merged); every fact below and in the Spec is re-read on the implementation base.

- The identity machinery and its single reservation rule, the generator's derivation of the identity from the path number, and the absence of any allocator or stored bound are listed in the Spec Overview with their line references at `eb017bfe`.
- SPEC-0180 (completed) is the existing retired-identity reservation: `LIFECYCLE-IDENTITY-REUSE` reads the base and the `Archived Lineage` first cells; its tests are `LineageRetiredIdentityTest` and `RetiredArtifactIdentityTest` in `tests/test_document_artifact_identity.py` and the generator identity case in `tests/test_document_generator.py`. At `eb017bfe` the Archived Lineage tables already name deleted `ADR` and `AD` numbers in the first column; the survey measures whether every deleted identity of every space is covered.
- The external requirement (REQ:141, REQ:672, REQ:823) and the cutover contract (stages A to E) are read-only inputs; the Q-07 task executes the transition after W11 and owns the code reform of the old rule and the next-number guard (W03-D76), the amendment of `REQ-0003-FR-0023` and of the never-reused sentence of the lifecycle policy, and the removal of `Archived Lineage`.
- DOC-12 is a live row of the SPEC-0161 Task with a ledger entry (owner W03, resume "last, after open packages close"); SPEC-0211 moves it to Q07 after W11 under W03-D74. W03-D74 to W03-D76 are recorded as decision rows by an earlier commit (the SPEC-0195 package commit; not on `main` at `035143d1`).
- The validators need `ruamel.yaml` from the hashed lock; its availability is resolved by quality preflight at implementation.

Migration is none: no document changes. Rollback is the revert of the implementation commit; the scratch copy is deleted.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-Q07PREP-001](spec.md#criteria) | The survey record of number spaces, allocators, references and consumer classes with denominators and exclusions; the list of sentences the transition must amend; the narrow questions for any immovable consumer or hold. | Approved Spec and Plan; main after SPEC-0210; decision rows W03-D74 to W03-D76 recorded on `main` (explicit precondition). | [Task 0001](tasks/tsk-0001-w03-q07-renumbering-preparation.md) | Counts re-derived by a second command; strict validators equal before and after. |
| WORK-002 | [VAL-Q07PREP-001](spec.md#criteria), [VAL-Q07PREP-002](spec.md#criteria) | The design record (mapping rules, mapping contract, move procedure, reservation after the transition, SemVer position) and the scratch rehearsal with its eight cases; the proof that the real tree is unchanged. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-q07-renumbering-preparation.md) | Recorded command text, per-space counts, per-rule diagnostic counts, case results; clean status, same `HEAD`, equal status, ref and worktree records. |
| WORK-003 | [VAL-Q07PREP-002](spec.md#criteria) | The non-reuse confirmation (coverage, enforcement, limit) and, only if it finds a hole, the completed reservation with failing-first tests; the Registry Schema Version record; this package's SPEC-0161 Task rows and, at closure, the REQ-0003 lineage row; regression and exact-index QA. | WORK-001, WORK-002. | [Task 0001](tasks/tsk-0001-w03-q07-renumbering-preparation.md) | Existing identity suites, ledger gate, ruff and markdownlint, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators before any change and re-read the base: `HEAD`, the registry value, the profile patterns, the lines named in the Spec Overview and the tree counts.
- Survey: derive each space's numbers, gaps and counts from the tree and from the deleted paths of Git history by two independent commands; classify the consumers of the 97 (re-counted) files into classes A to D with the exclusions stated; search `.agents/knowledge/`, `.github/`, the CI paths, the residue ledger and the workspace memory index for numbered references.
- Rehearsal: build the scratch copy by `git clone --no-hardlinks` outside the repository; apply the throwaway renumbering there; run the unmodified strict validators and the eight cases; record the output; delete the copy; then show `git status --porcelain --ignored`, `git for-each-ref` and `git worktree list` equal before and after (ignored `__pycache__` noted), `HEAD` unchanged, no `SPEC-0001` and no renamed path, and the status records equal.
- Non-reuse confirmation: run the read-only coverage comparison (deleted identities minus tree minus lineage-reserved) per space; run the existing identity suites; try a reserved sample of each space through the generator and the lifecycle check in the scratch copy. On the conditional path show each new test failing first on the base and then passing, and list the regression cases already passing.
- Registry Schema Version: record NO_CHANGE with the reason (W03-D76: no registry key; no registry byte changes) or, if the conditional path changes a registry byte, the base value, the level and the reason under ADR-0061.
- Ledger: this package appends only evidence rows; if it finds an unowned follow-up, a `Residue Handoff` row and its ledger entry are written in the same change; `python3 scripts/validate-work-residue-ledger.py --root .` before and after.
- Architecture compliance: the work stays within AD-0006 and adds no gate, script or reader.
- Record the risk class (`low` unless the conditional path edits code: Task records only, scratch work and no code, permission, secret-handling, hook or workflow; `medium` if the conditional path edits code) and the core-diff checklist.

Completion criteria:

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` with its approval receipt; the design questions are answered by W03-D76. DOC-12 stays open under the closing report's reassignment; this package's acceptance is not DOC-12's closure.

### Stage Placement

- Commit order: the package commit (documents only); then `.secrets.baseline` changes alone, if any; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and, if code changed, `graphify update .`. Merge before SPEC-0211 and rebase on `main` before each commit.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **The rehearsal touches the real tree or consumes a real number.** Unlikely, Severe: MEDIUM, mitigate. Owner: W03 author. The copy is made by `git clone --no-hardlinks` into a directory outside the repository, the script takes the copy path as its only target, and the Task shows clean status, same `HEAD`, no `SPEC-0001` and equal status, ref and worktree records afterwards. Review cue: the before and after status lines. Signal that raises it: any path under the repository in the script output.
- **The survey misses a consumer and the Q-07 task breaks it.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The survey counts by two commands, names its denominator and exclusions, and classes C and D are stated rather than skipped. Review cue: the reference count against the 97 files observed at `035143d1`. Signal that raises it: a consumer found only by the rehearsal.
- **The rehearsal's pass is read as the Q-07 pre-cutover PASS.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The record says scratch only, dated at the SHA it read; the Q-07 task re-surveys and re-runs (Q07-FINAL-CUTOVER stage D). Review cue: the record's SHA and date.
- **The package is read as starting Q-07 or as a W11 pass.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. Spec Non-goals and Task limits say no real number changes; the Q-07 task owns the transition. Review cue: the Verification Summary.
- **A hole in the old reservation is found late.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. Check 1 runs before the design is finalized, and the conditional path completes it before the transition. Signal that raises it: a nonempty remainder.
- **The next-number rule rehearses fine but breaks a workflow the scratch copy does not show.** Possible, Minor: LOW, monitor. Owner: W03 author. W03-D76 fixed the rule; the rehearsal runs it (case 6 and the concurrent case 4) and records the diagnostics, and the Q-07 task implements it. Review cue: the merge-time renumbering behaviour in case 4.
- **Not scored:** the state of W04 to W11 and of other repositories; Git objects, tags and releases are outside any renumbering.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |
