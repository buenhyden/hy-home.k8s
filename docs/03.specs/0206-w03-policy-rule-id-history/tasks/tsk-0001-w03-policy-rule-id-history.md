---
title: "W03 Policy Rule ID History"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0206-TSK-0001"
parent_ids: ["SPEC-0206-PLAN-0001"]
---

# Task: W03 Policy Rule ID History

## Scope

### Objective and Parent

This Task records Policy package 5, the last package of handoff W03-H29 (W03-D42 to W03-D44, W03-D53, W03-D64): the history rules that keep a rule ID from leaving its table or being issued again and a registered code from changing, with the landing audit and the closure of W03-H29, for [SPEC-0206](../spec.md) under its [Plan](../plan.md).

### Inputs and Authority

- **Request:** on 2026-11-13 and 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items and approved commit, push, PR and merge in those requests. The requests approve no Spec bytes or criterion.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `81096a83` (after PR #255, SPEC-0189) and from the Spec texts of SPEC-0194, SPEC-0199, SPEC-0201, SPEC-0202 and SPEC-0204, and are checked against `main` before delivery. The package needs SPEC-0194 implemented and merges after SPEC-0204.
- **Decisions reused:** SPEC-0161 W03-D27, W03-D42, W03-D43, W03-D44, W03-D53, W03-D54, W03-D65 and W03-H29; the note the user deferred from the SPEC-0194 review to this package, that a code changes only while its record is `pending`.
- **Decision recorded with this package:** W03-D64, five resolutions taken from the W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md`, under the user's standing instruction of 2026-11-14, `선택이 필요할 경우, 요구사항을 따른다` (when a choice is needed, follow the requirements): history is read step by step, base against proposal, in the existing lifecycle check (line 778; `scripts/AGENTS.md` rule 4); one landing audit is recorded in this Task, its script is not committed and a finding stops the package (lines 143, 149 and 173; `scripts/AGENTS.md` rule 3); a retired rule never becomes active again until a user-approved new baseline under the Q-07 contract (line 143); the code of a policy that leaves the tree moves to `reserved_codes`, which never shrinks until a user-approved new baseline under the Q-07 contract (line 226); and the code rule reads only the `policy_rule_ids` section of the base registry blob as plain JSON, which keeps W03-D54 because no typed historical registry is parsed (line 143). The appended W03-D64 row carries the Q-07 clause of both resolutions.

- **Allowed Paths**: `scripts/document_lifecycle.py` and `scripts/validate-document-lifecycle.py` for the three history rules and their base inputs; `scripts/validate-markdown-profiles.py` only to expose the Rules table reader; `tests/test_policy_rule_history.py`, `scripts/run-contract-tests.py` and `scripts/validation/registry.json` for its registration; the description of `reserved_codes` in `docs/99.templates/contracts/document-profile.schema.json`; the `verification` text of the `Status` entry of `shared_contract.extensions` in `docs/99.templates/registry.json`; the permanence sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md` and the disposition rule of `.agents/governance/document-lifecycle.md`, each new rule with its next rule ID, its Rules table row and the frontmatter `version` and `updated`; this package, `docs/03.specs/README.md`, the W03-D64 row, the closure row, an evidence row, the W03-H29 state cell and the frontmatter `version` and `updated` of the SPEC-0161 Task, the W03-H29 entry of `docs/03.specs/work-residue-ledger.json`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any existing rule ID, Rules table row, code or rule text of the fifteen policies, the grammar, the six document rules, the coverage floor and the registry records of SPEC-0194, any existing lifecycle rule, base mode or test, any committed audit script, the shared Policy form, the glossary, any recorded Task row, EVD row, decision or handoff rewrite, `.github/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any repair of a table that the landing audit finds wrong; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge are approved by the user's requests in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance`, `validation-routing` and `tooling` suites, `python3 scripts/validate-document-contract-registry.py --root .`, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the commit of the rules and their tests, or the commit of the policy texts; before that, delete the package commit
- **Evidence Location**: this Task

## Execution Log

### Work Performed

The work of this Task is recorded in the rows of [Lifecycle Traceability](#lifecycle-traceability) below and in the evidence rows under Verification Evidence.

### Blockers and Decisions

No separate blocker or decision list is kept here; a blocker and its resume condition are recorded in the Result and Evidence cells of the work rows, and each decision in the evidence rows under Verification Evidence.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RULEHIST-001](../spec.md#criteria) | `POLICY-RULE-DELETE` and `POLICY-RULE-REISSUE` in the lifecycle check, the base Rules tables in the evidence context, the shared reader, and their tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-RULEHIST-002](../spec.md#criteria) | `POLICY-CODE-CHANGE`, the base code section, the rule for a departing policy and the reserved list, and their tests; suite membership and surface route of the new module. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-RULEHIST-003](../spec.md#criteria) | The landing audit; the policy texts with their new rule IDs and rows; W03-D64, the closure of W03-H29 and its ledger entry; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RULEHIST-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"821ef56d948cdd5cb4aeb10710939658ab960ed0b5633b9122677fa65c94c8ce","plan_sha256":"b779c57a35476c2ebe08b65e997afdc8874bdd2014b6742a9f897e96000b89c4"} | PASS | Independent review on 2026-11-14 of the W03-D65 revision (conditional Rules table with four common columns and a registered Status extension per REQ:37, 310, 486, 742; Q-07 bound on permanence per REQ:143): APPROVE, with the reviewers' FIX and NIT items applied and confirmed over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-RULEHIST-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all six to the policy package re-approval question naming spec.md 821ef56d and plan.md b779c57a dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0206","SPEC-0206-PLAN-0001"],"reviewed_spec_sha256":"821ef56d948cdd5cb4aeb10710939658ab960ed0b5633b9122677fa65c94c8ce","reviewed_plan_sha256":"b779c57a35476c2ebe08b65e997afdc8874bdd2014b6742a9f897e96000b89c4","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-RULEHIST-001](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"b2feb7fae5216ece1914516d0c21fd355de81bce5b3d50630fe822d9d426e337","plan_sha256":"89e7d72d25898fc9ed842a547874919fe1687f37cb386c45c8c9a5edf21ed1f2"} | PASS | Mechanical form move of the approved Spec and Plan (821ef56d, b779c57a) to the SPEC-0200 forms by its heading map, version 1.0.0 to 2.0.0 and updated 2026-11-15 (W03-D59 Q4, W03-D84). The sorted non-heading lines of the old and new files are equal except the listed added or changed lines: in the Spec the criteria table header (Criterion, Acceptance evidence to Criterion ID, Expected Result), five label lines (Contracts, Data modeling and storage strategy, Interfaces and data structures, Edge cases and error handling, Failure modes and fallback or human escalation) and two References pointer lines; in the Plan three label lines (Goals and in-scope, Non-goals and out-of-scope, Completion criteria), the Dependencies, Change and Rollback, Escalation and Durable Meaning pointer lines, the Work Breakdown criterion anchors repointed to spec.md#criteria, and the Promotion table moved to the four-column form with one Acceptance cell added per row. No sentence was reworded. Task links to the Spec criteria are repointed to #criteria. This row records a mechanical check, not an approval. | yes | none |
| EVD-004 | [VAL-RULEHIST-001](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Mechanical move + check, blanket OK (Recommended) to the question on moving each remaining package's approved Spec and Plan to the SPEC-0200 forms with a major raise to 2.0.0 and a mechanical check, dated 2026-11-15 Asia/Seoul","review_ref":"EVD-003","scope":["SPEC-0206","SPEC-0206-PLAN-0001"],"reviewed_spec_sha256":"b2feb7fae5216ece1914516d0c21fd355de81bce5b3d50630fe822d9d426e337","reviewed_plan_sha256":"89e7d72d25898fc9ed842a547874919fe1687f37cb386c45c8c9a5edf21ed1f2","validity":"confirmed","revocation":"none"} | PASS | Approves the form move of the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-005 | [VAL-RULEHIST-001](../spec.md#criteria) | WORK-001 | Move of this Task to the SPEC-0203 Task form | SPEC-0203 Task form (`docs/99.templates/templates/specs/task.template.md`; the moved SPEC-0161 Task as model); this Task before (file 2075fd851ee52961, version 0.2.0 draft) and after the heading map | PASS | Form-only move: Overview under Objective and Parent, Inputs and the Approval and Safety Boundaries fields under Inputs and Authority, the Task Table as Lifecycle Traceability, the Task Evidence table under Results with the header `Evidence`, `Criteria`, `Check` read as `Evidence ID`, `Consumer`, `Command`, Criterion Acceptance as Criterion Decisions and the Verification Summary under Next Owner. Every data row of the work, evidence and criterion tables is identical; pointer lines were added for Work Performed, Blockers and Decisions, Resolution Links, Remaining Conditions and Promotion Receipt. Links to the Spec criteria use `#criteria`; frontmatter `status` is `ready`, matching the WORK rows. This row records a form move, not an approval. | no | none |

### Resolution Links

No earlier required failure is open; each Resolves cell is `none`.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RULEHIST-001](../spec.md#criteria) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-RULEHIST-002](../spec.md#criteria) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-RULEHIST-003](../spec.md#criteria) | pending | none | Implement WORK-003 and record PASS evidence | platform |

### Remaining Conditions

No separate remaining-condition list is kept here; the Disposition and Current owner columns of the criterion decisions state what remains and who owns it.

## Handoff

### Promotion Receipt

No separate promotion receipt is kept here; the Plan's promotion rows are reflected when the package exits.

### Next Owner

Spec and Plan approved with the W03-D64 resolutions written in and moved to the SPEC-0200 forms (EVD-003 to EVD-005); no implementation is recorded yet. Next owner: platform, WORK-001.
