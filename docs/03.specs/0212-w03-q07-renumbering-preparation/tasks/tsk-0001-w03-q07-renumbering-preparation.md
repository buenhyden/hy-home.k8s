---
title: "W03 Q-07 Renumbering Preparation"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0212-TSK-0001"
parent_ids: ["SPEC-0212-PLAN-0001"]
---

# Task: W03 Q-07 Renumbering Preparation

## Scope

### Objective and Parent

This Task will record, for [SPEC-0212](../spec.md) under its [Plan](../plan.md), the survey of number spaces, allocators, references and consumers read at the implementation base, the transition design record, the scratch rehearsal output and its eight cases, the non-reuse confirmation, the Registry Schema Version level and the criterion decisions. The survey, design and rehearsal records are appended here as plain tables under Verification Evidence, in the shape the Task form leaves, and assume no extra heading. Part of the survey, design, rehearsal and non-reuse records are in the Task Evidence below; the non-reuse remainder is closed by lineage rows for all 55 identities. No real path, document ID or allocation bound has changed or will change in this package.

### Inputs and Authority

- **Request:** the user decided on 2026-11-14 (Asia/Seoul) to follow the requirement with one Q-07 preparation package that lands before the W03 closing report (W03-D75, answer "Follow REQ: prep package (Recommended)"; it amends W03-D30). The request approves no Spec bytes, no criterion and no commit, push or merge.
- **Base:** set at commit time; the Spec was drafted against `main` `eb017bfe`.
- **Decisions reused:** W03-D75 (recorded in the SPEC-0161 Task by an earlier commit before this package lands), W03-D30 as amended, W03-D74 (DOC-12 reassigned to Q07 by SPEC-0211, not here), EVD-018 (display renumbering, then superseded in part by the requirement), and the SPEC-0180 retired-identity reservation recorded in the REQ-0003 Archived Lineage.
- **External requirement (read-only):** `REQ:141`, `REQ:672`, `REQ:823`, `REQ:129`, `REQ:137`, `REQ:143`, `REQ:147`, `REQ:918`, `REQ:815`, `REQ:285`, `REQ:776`, `REQ:864`, `REQ:890` of the W03 task file of the `_workspace` package, and its cutover contract `Q07-FINAL-CUTOVER.md` stages A to E.
- **Decisions reused (continued):** W03-D76 (answers "Next-number rule (Recommended)" and "With Q-07 after W11 (Recommended)"), recorded in the SPEC-0161 Task by an earlier commit; no decision row is appended here. Precondition: decision rows W03-D74 to W03-D76 are recorded on `main` (the SPEC-0195 package commit; not on `main` at `035143d1`). Open question: none.

- **Allowed Paths**: this package, `docs/03.specs/README.md`, this package's evidence row(s) and the frontmatter `version` and `updated` of the SPEC-0161 Task, the completed-spec lineage row of this package in `docs/01.requirements/0003-workspace-agent-governance-platform.md` at closure (with that document's frontmatter `version` and `updated`), `.secrets.baseline` (reviewed digest entries only); on the conditional path only, the `Archived Lineage` rows of the owning Stage 01 and 02 documents and the identity tests named in the Spec; a temporary directory outside the repository for the rehearsal copy
- **Forbidden Paths**: any real path, document ID, anchor, allocation bound or Stage directory name change, any new real number (`SPEC-0001` included), any committed mapping or rehearsal script, the live DOC-12 row, its ledger entry, W03-H20 and W03-H24, `Archived Lineage` removal, any registry, template, profile or form change on the recommended path, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, `.claude/`, `.codex/`, hooks, writes to `_workspace/`, `docs/98.archive/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; any change beyond the Spec's named scope or any immovable consumer, hold or authority conflict, which stops the work and goes to the user; an install of the hashed validator lock if the tool is absent; any commit, push, PR or merge
- **Static Validation**: strict document validators, the `document` and `document-lifecycle` suites, `python3 scripts/validate-work-residue-ledger.py --root .`, markdownlint over the edited Markdown, `ruff check scripts tests` if code changed, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed; the survey counts references and reads no secret file
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit; delete the scratch copy
- **Evidence Location**: this Task

## Execution Log

### Work Performed

The work of this Task is recorded in the rows of [Lifecycle Traceability](#lifecycle-traceability) below and in the evidence rows under Verification Evidence.

### Blockers and Decisions

No separate blocker or decision list is kept here; a blocker and its resume condition are recorded in the Result and Evidence cells of the work rows, and each decision in the evidence rows under Verification Evidence.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-Q07PREP-001](../spec.md#criteria) | The survey record of number spaces, allocators, references and consumer classes, with denominators, exclusions, absences and the sentences the transition must amend. | platform | draft | NOT_RUN | Pending |
| WORK-002 | [VAL-Q07PREP-001](../spec.md#criteria), [VAL-Q07PREP-002](../spec.md#criteria) | The transition design record and the scratch rehearsal with eight cases; proof the real tree is unchanged. | platform | draft | NOT_RUN | Pending |
| WORK-003 | [VAL-Q07PREP-002](../spec.md#criteria) | The non-reuse confirmation (coverage, enforcement, limit), the conditional completion if a hole is found, the Registry Schema Version record, the SPEC-0161 Task rows and regression and exact-index QA. | platform | draft | NOT_RUN | Pending |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-001 | Survey of number spaces, allocators, references and consumers | `main` at the base named in Inputs: registry patterns, tree and Git history numbers and gaps per space, references by kind, consumer classes A to D with counts, absences and amendable sentences | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-002 | Transition design record | Mapping rules, mapping contract, move procedure, reservation after the transition, SemVer position, with the next-number guard of W03-D76 (designed here, implemented by the Q-07 task) | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-Q07PREP-002](../spec.md#criteria) | WORK-002 | Scratch rehearsal | Command text, per-space counts, per-rule diagnostic counts of the unmodified strict validators, eight case results (case 6 unguarded and guarded), and the unchanged real tree (`git status --porcelain --ignored`, `git for-each-ref`, `git worktree list`, `HEAD`, no `SPEC-0001`, equal status, ref and worktree records) | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-Q07PREP-002](../spec.md#criteria) | WORK-003 | Non-reuse confirmation | Coverage remainder per space, existing identity suites, reserved sample per space refused by the generator and the lifecycle check; failing-first and passing results only if the conditional path ran | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-Q07PREP-002](../spec.md#criteria) | WORK-003 | Registry Schema Version level | The value at the base, the level (NO_CHANGE) and the reason | NOT_RUN | Pending | yes | none |
| EVD-006 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-001 | Independent semantic review | Read-only reviewer that wrote none of the package, over the Spec and Plan bytes | NOT_RUN | Pending | yes | none |
| EVD-007 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | The user's direct answer to the SPEC-0212 approval question naming the Spec and Plan bytes | NOT_RUN | Pending | yes | none |
| EVD-008 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"5d83be6759df488663a17fc78e463ed832f8a68ee69fad7c4ab0101710ed0101","plan_sha256":"9b80f84310a108dcd306db6e087412ca3420160e587627e1fda4fc882bf7a14f"} | PASS | Independent review by the code-reviewer role: round 1 APPROVE WITH FIXES (F1 to F6: REQ:823 reading, consumer preparation, git clone scratch copy, case 6 guarded and unguarded, Q07 stage D refusals, decision-row precondition, plus NITs), round 2 APPROVE with four NITs, applied; read-only, 2026-11-14. | yes | none |
| EVD-009 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes (Recommended) to the SPEC-0212 approval question naming spec.md 5d83be67 and plan.md 9b80f843, 2026-11-14","review_ref":"EVD-008","scope":["SPEC-0212","SPEC-0212-PLAN-0001"],"reviewed_spec_sha256":"5d83be6759df488663a17fc78e463ed832f8a68ee69fad7c4ab0101710ed0101","reviewed_plan_sha256":"9b80f84310a108dcd306db6e087412ca3420160e587627e1fda4fc882bf7a14f","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-010 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"0f620689ab73b669c3e6d91d6822068b3473ccefa7015df34f96763defdb5e01","plan_sha256":"88fd3cb2dfe22c78c8b171b7166783dfa0e230fe9a92f380d01b4365c5227b43"} | PASS | Mechanical form move of the approved Spec and Plan (5d83be67, 9b80f843) to the SPEC-0200 forms by its heading map, version 1.0.0 to 2.0.0 and updated 2026-11-15 (W03-D59 Q4, W03-D84). The sorted non-heading lines of the old and new files are equal except the listed added or changed lines: in the Spec the criteria table header (Criterion, Acceptance evidence to Criterion ID, Expected Result), five label lines (Contracts, Data modeling and storage strategy, Interfaces and data structures, Edge cases and error handling, Failure modes and fallback or human escalation) and two References pointer lines; in the Plan two label lines (Goals and in-scope, Non-goals and out-of-scope), the Completion criteria label line, the Dependencies, Change and Rollback, Escalation and Durable Meaning pointer lines, the Work Breakdown criterion anchors repointed to spec.md#criteria, and the Promotion table moved to the four-column form; its two rows named no current `.agents/` or Stage 01, 02 or 05 owner (the SPEC-0161 Task, an unlinked policy), which the Plan form refuses, so it holds the explicit `none` row (no durable contract was introduced; the survey, design and rehearsal records stay Task content). The Lifecycle Traceability row that named two requirement members in one cell is split into two rows (one member per row, as the body contract requires). Five Spec lines quoting the Korean requirement text have the quotation in inline code so the english-first check passes. The H3 subsections of the Spec Contracts and the Decisions subsection of the Spec boundaries are one level deeper (H4) so that they sit under their form sections; no sentence was reworded. Task links to the Spec criteria are repointed to #criteria. This row records a mechanical check, not an approval. | yes | none |
| EVD-011 | [VAL-Q07PREP-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Mechanical move + check, blanket OK (Recommended) to the question on moving each remaining package's approved Spec and Plan to the SPEC-0200 forms with a major raise to 2.0.0 and a mechanical check (W03-D84), dated 2026-11-15 Asia/Seoul","review_ref":"EVD-010","scope":["SPEC-0212","SPEC-0212-PLAN-0001"],"reviewed_spec_sha256":"0f620689ab73b669c3e6d91d6822068b3473ccefa7015df34f96763defdb5e01","reviewed_plan_sha256":"88fd3cb2dfe22c78c8b171b7166783dfa0e230fe9a92f380d01b4365c5227b43","validity":"confirmed","revocation":"none"} | PASS | Approves the form move of the Spec and Plan bytes only; accepts no criterion. | yes | none |

### Resolution Links

The Resolves column of the evidence table under Results names the earlier evidence row that each PASS row closes.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-Q07PREP-001](../spec.md#criteria) | pending | none | Implement WORK-001 and WORK-002 and record PASS evidence | platform |
| [VAL-Q07PREP-002](../spec.md#criteria) | pending | none | Implement WORK-002 and WORK-003 and record PASS evidence | platform |

### Remaining Conditions

No separate remaining-condition list is kept here; the Disposition and Current owner columns of the criterion decisions state what remains and who owns it.

## Handoff

### Promotion Receipt

The Plan promotes no durable contract (its Promotion table holds the `none` row), so there is no promotion receipt.

### Next Owner

The survey, design record, rehearsal cases 1 to 8, the real-tree check, the registry level and the lineage rows for 41 identities are recorded; the non-reuse remainder is empty (EVD-025, EVD-026). No criterion is accepted. Next owner: the user, for criterion acceptance, after the replay onto the new main.
