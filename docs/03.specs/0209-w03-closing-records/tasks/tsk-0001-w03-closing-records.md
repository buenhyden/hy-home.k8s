---
title: "W03 Closing Records"
version: "0.2.3"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0209-TSK-0001"
parent_ids: ["SPEC-0209-PLAN-0001"]
---

# Task: W03 Closing Records

## Scope

### Objective and Parent

This Task will record the COMMON-DOC-FORM-1 candidate record and its refusal test, the adoption facts, the approval evidence request for the six `WGOV-CORE` facts, the writer delegation record, the stale tracking corrections and the criterion decisions for [SPEC-0209](../spec.md) under its [Plan](../plan.md). It is a stub: nothing has run.

### Inputs and Authority

- **Request:** the user asked on 2026-11-14 (Asia/Seoul) for the W03 closing records (handoffs W03-H19, W03-H21 and W03-H31, the six `unverified` approval facts and the old-obligation classification) to be drafted as a package. The request approves no Spec bytes, no criterion and no commit, push or merge.
- **Base:** set at commit time; the Spec was drafted against `main` `81096a83`.
- **Form move:** the user decided on 2026-11-15 (Asia/Seoul), W03-D84, "Mechanical move + check, blanket OK (Recommended)": since SPEC-0200 every Spec and Plan uses the common forms, so this package's approved Spec and Plan move to those forms by the SPEC-0200 heading map at version 2.0.0 (W03-D59 Q4). The move adds only headings, label lines and the table columns the forms name; the approved contract text is unchanged. EVD-008 records the check and EVD-009 the approval.
- **Decisions reused:** SPEC-0161 W03-D05, W03-D02, W03-D47 and W03-H19, W03-H20, W03-H21 and W03-H31.
- **Decisions of 2026-11-15 (Asia/Seoul):** "Accept scripts scope (Recommended)": this package keeps its edits to `scripts/document_contracts.py`, `tests/test_shared_contract_binding.py` and `tests/test_common_form_tree.py`, and its `Current Writer State` list hands them to W05 (EVD-021). "Pre-accept when green (Recommended)": the remaining W03 packages are accepted in advance once their checks and CI pass; a failure, a new decision or a scope change still goes to the user.
- **Decision recorded with this package:** W03-D67 (the user's answers of 2026-11-14 to Questions 1, 2, 4, 5 and 6, each the recommended option, and the settlement of Question 3 by the user's SPEC-0191 decision), appended to the SPEC-0161 Task with the package commit. Open question: none.

- **Allowed Paths**: `docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `scripts/document_contracts.py`, `scripts/document_authority.py` and `scripts/provider_write_guard.py` (the registry MAJOR step of ADR-0061, a requirement-driven item for the user's acceptance), `tests/test_shared_contract_binding.py`, `tests/test_common_form_tree.py`, this package, `docs/03.specs/README.md`, in the SPEC-0161 Task appended rows, the `State` and `Closure` cells of the residue rows this package closes and the frontmatter `version` and `updated`, the work residue ledger entries this package closes, `.secrets.baseline` (reviewed digest entries only)
- **Forbidden Paths**: any recorded Task row, evidence row, decision or handoff rewrite, any invented approval fact, writes to `_workspace/` and anything copied from it into `docs/90.references/` or `docs/98.archive/`, `.github/workflows/`, `.claude/`, `.codex/`, hooks, any accepted ADR
- **Approval Required**: Spec and Plan approval; criterion acceptance; any commit, push, PR or merge; any statement of an approval fact by the user is recorded as a user answer with its date
- **Static Validation**: strict document validators, `python3 scripts/validate-document-contract-registry.py --root .`, the `work-residue-ledger` gate, the `document` and `document-lifecycle` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task, and the appended tables of the SPEC-0161 Task

## Execution Log

### Work Performed

The work of this Task is recorded in the rows of [Lifecycle Traceability](#lifecycle-traceability) below and in the evidence rows under Verification Evidence.

### Blockers and Decisions

No separate blocker or decision list is kept here; a blocker and its resume condition are recorded in the Result and Location cells of the evidence rows under Verification Evidence, and each decision in the Inputs and Authority list above.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CLOSING-001](../spec.md#criteria) | The `common_forms` candidate record, schema properties, reader and refusal test; the adoption facts and the approval evidence request; the ledger closure of W03-H19. | platform | draft | NOT_RUN | Pending |
| WORK-002 | [VAL-CLOSING-002](../spec.md#criteria) | The writer delegation table and current writer state, the 14 `meaning_map` corrections, the corrections and closing summary, the ledger closure of W03-H21 and W03-H31. | platform | draft | NOT_RUN | Pending |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Counts and figures re-read from the tree and the Git diffs | `main` at the base named in Inputs | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"35edf2594b645df9e093b35aaa4f07f04485aff87e12187ecb9fb06fd05f3d57","plan_sha256":"7c432f26f16256a96cea865ab3629267c33a3fcc7fb5f44c4db7158163cbac39"} | PASS | Independent review, two rounds on 2026-11-14 (W03-D67 and W03-D68 drafts): all round-1 and round-2 items applied and confirmed over the bytes named here; APPROVE. This row records a review, not an approval. | yes | none |
| EVD-003 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve both to the SPEC-0208 and SPEC-0209 approval question naming spec.md 35edf259 and plan.md 7c432f26 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0209","SPEC-0209-PLAN-0001"],"reviewed_spec_sha256":"35edf2594b645df9e093b35aaa4f07f04485aff87e12187ecb9fb06fd05f3d57","reviewed_plan_sha256":"7c432f26f16256a96cea865ab3629267c33a3fcc7fb5f44c4db7158163cbac39","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"fede852c381e0c0eb55d6c36a0f47da6f1f618fdaa6a739c54cb6b405a58d486","plan_sha256":"43a7ed21bf9e474ec026d4416710f8eaeaebc3d8eed4039f567a28946f5e647e"} | PASS | Read-only audit of the pending packages against main 035143d1 and decisions W03-D70 to W03-D76, 2026-11-14: stale statements corrected (fixed registry version value, stale baseline or merge order); every other byte unchanged (checked by diff). | yes | none |
| EVD-005 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Re-approve all three (Recommended) to the re-approval question naming the new bytes of SPEC-0196, SPEC-0205 and SPEC-0209, here spec.md fede852c and plan.md 43a7ed21, 2026-11-14","review_ref":"EVD-004","scope":["SPEC-0209","SPEC-0209-PLAN-0001"],"reviewed_spec_sha256":"fede852c381e0c0eb55d6c36a0f47da6f1f618fdaa6a739c54cb6b405a58d486","reviewed_plan_sha256":"43a7ed21bf9e474ec026d4416710f8eaeaebc3d8eed4039f567a28946f5e647e","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-006 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"b73d31c44287797fbef0528a132cfc6975169b937cf5d3d8b1fc5813db5f534a","plan_sha256":"43a7ed21bf9e474ec026d4416710f8eaeaebc3d8eed4039f567a28946f5e647e"} | PASS | Read-only edit for user decision W03-D81 (SPEC-0213 classification table overlap), 2026-11-14: one Spec sentence changed; every other byte unchanged (checked by diff). | yes | none |
| EVD-007 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Re-approve both (Recommended) to the re-approval question naming the new bytes of SPEC-0209 and SPEC-0211, here spec.md b73d31c4 and plan.md 43a7ed21, 2026-11-14","review_ref":"EVD-006","scope":["SPEC-0209","SPEC-0209-PLAN-0001"],"reviewed_spec_sha256":"b73d31c44287797fbef0528a132cfc6975169b937cf5d3d8b1fc5813db5f534a","reviewed_plan_sha256":"43a7ed21bf9e474ec026d4416710f8eaeaebc3d8eed4039f567a28946f5e647e","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-008 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"189e12ca9483efbfe4342469466de06cc685b23346c13b2a2dc07645a52ffd36","plan_sha256":"db6a643074cd410a65408e41f118c7988cb9a5f545a8533b44cc98561cbf4068"} | PASS | Form move of the approved Spec and Plan to the SPEC-0200 common forms (W03-D84), 2026-11-15: the sorted non-heading lines of the approved bytes (spec b73d31c4, plan 43a7ed21) and of the moved files are equal except the added label lines (`Data modeling and storage:`, `Interfaces and data structures:`, `In scope:`, `Out of scope:`), the two sentences each of Prerequisites, Dependency Order, Change and Rollback, Escalation and Durable Meaning, the two References sentences, the renamed Criteria header, the repointed Work Breakdown anchors (`spec.md#criteria`) and the Promotion table whose Acceptance column is new; the headings follow the SPEC-0200 map; checked by script and by diff. This row records a review of the move, not an approval. | yes | none |
| EVD-009 | [VAL-CLOSING-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Mechanical move + check, blanket OK (Recommended) to the form-move question for all pending packages (W03-D84), 2026-11-15 Asia/Seoul","review_ref":"EVD-008","scope":["SPEC-0209","SPEC-0209-PLAN-0001"],"reviewed_spec_sha256":"189e12ca9483efbfe4342469466de06cc685b23346c13b2a2dc07645a52ffd36","reviewed_plan_sha256":"db6a643074cd410a65408e41f118c7988cb9a5f545a8533b44cc98561cbf4068","validity":"confirmed","revocation":"none"} | PASS | Approves the moved Spec and Plan bytes only; accepts no criterion. | yes | none |

### Resolution Links

The Resolves column of the evidence table under Results names the earlier evidence row that each PASS row closes.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-CLOSING-001](../spec.md#criteria) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-CLOSING-002](../spec.md#criteria) | pending | none | Implement WORK-002 and record PASS evidence | platform |

### Remaining Conditions

No separate remaining-condition list is kept here; the Disposition and Current owner columns of the criterion decisions state what remains and who owns it.

## Handoff

### Promotion Receipt

No separate promotion receipt is kept here; the receipt of the Plan promotion row is recorded in the evidence rows under Results once the criteria are accepted.

### Next Owner

Draft; no check has run. Next owner: the user, for the records that would verify the six `WGOV-CORE` approval facts.
