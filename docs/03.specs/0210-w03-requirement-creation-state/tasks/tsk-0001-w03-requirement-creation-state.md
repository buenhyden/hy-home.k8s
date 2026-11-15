---
title: "W03 Requirement Creation State"
version: "0.1.8"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0210-TSK-0001"
parent_ids: ["SPEC-0210-PLAN-0001"]
---

# Task: W03 Requirement Creation State

## Scope

### Objective and Parent

This Task will record the survey of creation states, the failing-first and passing results of the creation-state, registry check, lifecycle creation and generator cases, the Registry Schema Version level and reason, and the criterion decisions for [SPEC-0210](../spec.md) under its [Plan](../plan.md), which repairs residue W03-H43. It is a stub: nothing has run.

### Inputs and Authority

- **Request:** the user decided on 2026-11-14 (Asia/Seoul) a small W03 package after SPEC-0206 that adds a creation state to the `requirement` lifecycle domain with failing-first tests (W03-D71, answer "Small W03 package (Recommended)"), decided its three design choices as recommended (W03-D73, below), and asked for its bytes to be sent for approval. The request approves no Spec bytes, no criterion and no commit, push or merge.
- **Base:** set at commit time; the Spec was drafted against `main` `eb017bfe`, whose registry `schema_version` is `12.0.0`.
- **Decisions reused:** SPEC-0161 W03-D48 (question 3), W03-H43 and EVD-058; ADR-0061 for the Registry Schema Version rule.
- **Decisions reused:** W03-D71 (the intake answer) and W03-D73 ("Declare initial_states (Recommended)"; "MAJOR, after 0206 (Recommended)"), both recorded in the SPEC-0161 Task by the SPEC-0194 implementation commit before this package lands. No decision row is appended by this package. Open question: none.

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json` for the `requirement` entry and `schema_version`, `docs/99.templates/contracts/document-profile.schema.json` for its version value, `scripts/document_contracts.py`, `scripts/document_authority.py`, `scripts/provider_write_guard.py`, `tests/test_document_artifact_identity.py`, `tests/test_document_generator.py`, `tests/test_task_acceptance_contract.py`, `tests/test_document_lifecycle_cumulative_history.py`, any policy sentence the survey finds), this package, `docs/03.specs/README.md`, this package's evidence row(s), the W03-H43 closure and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entry of `docs/03.specs/work-residue-ledger.json` at acceptance, the completed-spec lineage row of this package in `docs/01.requirements/0003-workspace-agent-governance-platform.md` at closure (with that document's frontmatter `version` and `updated`), `.secrets.baseline` (reviewed digest entries only)
- **Forbidden Paths**: the `states`, `transitions` and `profile_ids` of any domain, any other family, any template, profile, form or relationship, `scripts/document_lifecycle.py` and `scripts/document-generator.py` beyond a refusal the tests prove necessary (which stops the work), any existing Requirement document, the work residue ledger design, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, `.claude/`, `.codex/`, hooks, writes to `_workspace/`, `docs/98.archive/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; any commit, push, PR or merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle` and `validation-routing` suites, `python3 scripts/validate-affected-surfaces.py --root .`, `python3 scripts/validate-work-residue-ledger.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Execution Log

### Work Performed

The work of this Task is recorded in the rows of [Lifecycle Traceability](#lifecycle-traceability) below and in the evidence rows under Verification Evidence.

### Blockers and Decisions

No separate blocker or decision list is kept here; a blocker and its resume condition are recorded in the Result and Evidence cells of the work rows, and each decision in the evidence rows and tables under Verification Evidence.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REQCREATE-001](../spec.md#criteria) | The survey; the failing-first creation-state, registry check and `LIFECYCLE-CREATE` tests; the registry entry; the two clauses of the registry check. | platform | draft | NOT_RUN | Pending |
| WORK-002 | [VAL-REQCREATE-002](../spec.md#criteria) | The Requirement sample and completeness assertion of the generator tests; the MAJOR raise; the policy survey; the SPEC-0161 Task rows and, at acceptance, the ledger cycle; regression and exact-index QA. | platform | draft | NOT_RUN | Pending |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Survey of creation states and policy sentences | `main` at the base named in Inputs: `creation_states` of every lifecycle domain; the policy files and the stage 01 README searched for a sentence that states the gap | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | Read-only reviewer that wrote none of the package, over the Spec and Plan bytes | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | The user's direct answer to the SPEC-0210 approval question naming the Spec and Plan bytes | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-REQCREATE-002](../spec.md#criteria) | WORK-002 | Registry Schema Version level | The value at the base, the value after, the level MAJOR and the reason of the Spec; the MAJOR constants and the schema value | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"78ceaa81ba26e75402aeed8e221bf7bee9163cadb830b5222925290c5841ef1f","plan_sha256":"0fddcbf5eb3d8f84754116fac4beb94ebc9172cd28ead2ec05ee5fefb990436e"} | PASS | Independent review by the code-reviewer role: round 1 APPROVE WITH FIXES (six fixes: generator authoring set, decision naming W03-D71/W03-D73, open questions replaced by Decisions, REQ:877/878 citation, exact test files, failing-first wording), round 2 APPROVE with two cosmetic notes; read-only, 2026-11-14. | yes | none |
| EVD-006 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answers Approve these bytes (Recommended) to the SPEC-0210 approval question on the draft bytes and Approve these bytes (Recommended) to the question naming spec.md 78ceaa81 and plan.md 0fddcbf5, the same bytes with status approved and version 1.0.0, 2026-11-14","review_ref":"EVD-005","scope":["SPEC-0210","SPEC-0210-PLAN-0001"],"reviewed_spec_sha256":"78ceaa81ba26e75402aeed8e221bf7bee9163cadb830b5222925290c5841ef1f","reviewed_plan_sha256":"0fddcbf5eb3d8f84754116fac4beb94ebc9172cd28ead2ec05ee5fefb990436e","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-019 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"5882466fd6d2a4700dc5b25497ba51c92fff5bd693fecc577aa35b8bc3d4cefa","plan_sha256":"e90797d47cc65bb4a5c2d0fbe89d7b7554347d95460643a5510861f4a59217fe"} | PASS | Mechanical form move of the approved Spec and Plan (78ceaa81, 0fddcbf5; EVD-005, EVD-006) to the SPEC-0200 forms by its heading map, version 1.0.0 to 2.0.0 and updated 2026-11-15 (W03-D59 Q4, W03-D84). The sorted non-heading lines of the old and new files are equal except the listed added or changed lines: in the Spec the criteria table header (Criterion, Acceptance evidence to Criterion ID, Expected Result), six label lines (Contracts, Data modeling and storage strategy, Interfaces and data structures, Edge cases and error handling, Failure modes and fallback or human escalation, and Decisions (W03-D73), which was an H3 the Spec form has no place for) and two References pointer lines, and the Traceability row that named REQ-0003-FR-0027 and REQ-0003-FR-0028 split into one row for each ID with its other cells unchanged (BODY-CONTRACT-IDENTIFIER); in the Plan two label lines (Goals and in-scope, Non-goals and out-of-scope), the Completion criteria label, the Dependencies, Change and Rollback, Escalation and Durable Meaning pointer lines, the Work Breakdown criterion anchors repointed to spec.md#criteria, and the Promotion table moved to the four-column form with one Acceptance cell added and its Target Owner changed from the Stage 99 registry and its registry check to a link to the Document authoring policy, because PLAN-PROMOTION accepts only a linked .agents or Stage 01, 02 or 05 owner (the registry entry stays named in the Where cell, and the Acceptance cell names the generator sentence of that policy). No other sentence was reworded. Task links to the Spec criteria are repointed to #criteria. This row records a mechanical check, not an approval. | yes | none |
| EVD-020 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Mechanical move + check, blanket OK (Recommended) to the question on moving each remaining package's approved Spec and Plan to the SPEC-0200 forms with a major raise to 2.0.0 and a mechanical check, dated 2026-11-15 Asia/Seoul","review_ref":"EVD-019","scope":["SPEC-0210","SPEC-0210-PLAN-0001"],"reviewed_spec_sha256":"5882466fd6d2a4700dc5b25497ba51c92fff5bd693fecc577aa35b8bc3d4cefa","reviewed_plan_sha256":"e90797d47cc65bb4a5c2d0fbe89d7b7554347d95460643a5510861f4a59217fe","validity":"confirmed","revocation":"none"} | PASS | Approves the form move of the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-024 | [VAL-REQCREATE-001](../spec.md#criteria) | WORK-001 | Move of this Task to the SPEC-0203 Task form | The Task before (version 0.1.4) and after (version 0.1.5) the SPEC-0203 heading map, replayed onto `main` `8d0700e1`; the moved SPEC-0161 Task as the model | PASS | Form-only move by the SPEC-0203 heading map: the old H2 removed, every body under its form H3 and the evidence header line renamed (`Evidence`, `Criteria`, `Check` to `Evidence ID`, `Consumer`, `Command`). The data rows of all three tables are byte-identical and in the same order (table data-row hashes equal before and after) and five pointer lines were added (Work Performed, Blockers and Decisions, Resolution Links, Remaining Conditions, Promotion Receipt). The `status` frontmatter key reads `draft`, as the two WORK rows do. No recorded row was rewritten. | no | none |

### Resolution Links

The Resolves column of the evidence table under Results names the earlier evidence row that each PASS row closes.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-REQCREATE-001](../spec.md#criteria) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-REQCREATE-002](../spec.md#criteria) | pending | none | Implement WORK-002 and record PASS evidence | platform |

### Remaining Conditions

No separate remaining-condition list is kept here; the Disposition and Current owner columns of the criterion decisions state what remains and who owns it.

## Handoff

### Promotion Receipt

No separate promotion receipt is kept here; the receipt of each Plan promotion row, where the Plan has one, is recorded in the evidence rows under Results.

### Next Owner

Draft; no check has run. Next owner: platform, for the Spec and Plan approval.
