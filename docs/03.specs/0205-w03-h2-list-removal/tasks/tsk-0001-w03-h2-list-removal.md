---
title: "W03 H2-List Model Removal"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0205-TSK-0001"
parent_ids: ["SPEC-0205-PLAN-0001"]
---

# Task: W03 H2-List Model Removal

## Scope

### Objective and Parent

This Task records the last part of handoff W03-H02 and the list part of W03-H13: the removal of the `sections` lists from every registry profile, of the heading lists derived from a form and of the list checks no current document can reach, with every heading rule kept active, the Registry Schema Version raised by one MAJOR step under the bump rule of SPEC-0207, with a history reading of earlier registries kept for replay, and the retained ADR lists of ADR-0001 to ADR-0061 kept under ADR-0062, for [SPEC-0205](../spec.md) under its [Plan](../plan.md).

### Inputs and Authority

- **Request:** on 2026-11-14 (Asia/Seoul) the user asked to continue W03 phase 3 in the order of W03-D49. On 2026-11-15 (Asia/Seoul) the user decided for every remaining package, "Mechanical move + check, blanket OK (Recommended)" (W03-D84): since SPEC-0200 every Spec and Plan uses the common Spec and Plan forms, so this package's approved Spec and Plan were moved to them with version 2.0.0 and a mechanical check (EVD-005, EVD-006). The request approves no criterion; an approval of push, PR or merge is recorded here when the user gives it.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `81096a83` (after PR #255, SPEC-0189) and are checked against `main` before delivery; the worktree for the implementation was cut from `origin/main` `aa3cce7c` (SPEC-0191 to SPEC-0204 merged, registry 17.0.0).
- **Decisions reused:** SPEC-0161 W03-H02, W03-H13, W03-D02, W03-D30, W03-D33, W03-D49, W03-D50, W03-D51, W03-D40, W03-D52, W03-D56, W03-D59, W03-D61, W03-D69, W03-D70, W03-D83 and W03-D84 (ADR-0061 is the amending ADR of SPEC-0207, the ADR of SPEC-0198 is ADR-0062, and the retained range is ADR-0001 to ADR-0061).
- **Decision recorded with this package:** W03-D63, the user's answer `w03 프롬프트에 작성된대로` of 2026-11-14 to the three questions this package raised, resolved from the task file `tasks/TASK-hy-home-k8s-W03.md` of the v14.7 package. The `sections` key leaves every current profile and the current schema and the strict registry check refuses it (line 757, no permanent compatibility layer; line 878, no permanent deprecation layer; rule 3 of `scripts/AGENTS.md`). A removed required key is a breaking change that needs a version increase (lines 877 and 878); the third answer, an integer raise of `schema_version` from 10 to 11, is superseded by W03-D66. `REGISTRY_FORM_REQUIRED` requires a form of an `authored`, `router` or `template` profile, except the `provider-native` role (line 759, a no-change conclusion needs proof for each registry entry; lines 113 and 875, no surface is forced on a role it does not apply to).
- **Decisions reused, superseding the third answer of W03-D63:** W03-D65, recorded by the SPEC-0193 package commit, the user's answer `W03 프롬프트에 작성된대로` of 2026-11-14 to the findings of a requirement audit against the same task file: the value of `schema_version` is not chosen by this package, because an existing integer moves only by an explicit mapping after a reader analysis (lines 862 and 890). W03-D66, recorded by the SPEC-0207 package commit: `schema_version` is a SemVer string, generation 10 maps to `10.0.0`, SPEC-0207 lands the registry at `11.0.0` right after SPEC-0191, and every later registry change applies the bump rule of lines 877 to 882. Under it this package is a MAJOR step from the version the registry carries when it lands, with MINOR and PATCH at 0, the implemented MAJOR is held by `REGISTRY_MAJOR` in `scripts/document_authority.py` with the guard's copy `DOC_REGISTRY_MAJOR`, `registry_at` reads every generation in `READABLE_REGISTRY_MAJORS` through `registry_schema_version`, whose integer branch serves replay only, and the version tests of SPEC-0207 read the constants, so this package edits no test for the bump.
- **Requirement applied to the history reader:** line 778 keeps the cumulative-history replay until the transition, so the replay-only history reading of earlier registries, with its removal condition, is required and is not a compatibility branch under rule 3 of `scripts/AGENTS.md`.

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `scripts/document_authority.py`, `scripts/document_contracts.py`, `scripts/validate-document-lifecycle.py`, `scripts/provider_write_guard.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/validate-document-contract-registry.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py`, the named tests, and the named sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`), this package, `docs/03.specs/README.md`, the W03-D63 row, the handoff closures, evidence rows and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entries of the work residue ledger, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any form, section, extension or governed document body, the retained ADR form and its checks, the old-shape branches of the lifecycle readers apart from the one accessor function of the Plan branch, every ADR, the SemVer form, mapping function, reader rule and bump rule of SPEC-0207, hook registration and permissions, any recorded Task row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Reviews routed before merge**: a `security-auditor` read of the staged diff of `scripts/provider_write_guard.py`, whose `git diff --cached` output is recorded here as proof that the guard changes `DOC_REGISTRY_MAJOR` alone and holds one MAJOR
- **Approval Required**: Spec and Plan bytes (current bytes approved by EVD-006); criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
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
| WORK-001 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | Transfer first: the table that maps each list rule to the tree rule or retained form that covers the same documents; the accessor; the four readers and the accessor function of the old-shape Plan branch on it; the renamed field; the recorded replays of a commit of the retired MAJOR and of a commit that holds the integer; the tests that show each reader and each role still refused. | platform | draft | NOT_RUN | Pending |
| WORK-002 | [VAL-LISTREMOVAL-001](../spec.md#criteria) | Callers and registration: the `sections` key of every profile, the schema property, the guard entry, `_form_headings`, the two registry rules, the three README identifiers, `REGISTRY_FORM_REQUIRED`; the MAJOR step of `schema_version` in the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the guard's `DOC_REGISTRY_MAJOR`, with the history reading of earlier registries in `registry_at`; the bump level and its reason recorded as evidence. | platform | draft | NOT_RUN | Pending |
| WORK-003 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | Helpers, fixtures and tests that lost their last consumer, each after a recorded search; the two policy texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | platform | draft | NOT_RUN | Pending |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"09a4a113b3ff778b849fc12770ad84d67e399b3612952170a553b909ab53407c","plan_sha256":"3fc2fe96f1e28f2c003d0773547ffbbbca32b45553023979cede28b25277b748"} | PASS | Independent review, two rounds on 2026-11-14 (W03-D65 and W03-D66 revisions): every FIX item and the round-2 notes applied and confirmed over the bytes named here; APPROVE. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all three to the SPEC-0200, SPEC-0203 and SPEC-0205 approval question naming spec.md 09a4a113 and plan.md 3fc2fe96 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0205","SPEC-0205-PLAN-0001"],"reviewed_spec_sha256":"09a4a113b3ff778b849fc12770ad84d67e399b3612952170a553b909ab53407c","reviewed_plan_sha256":"3fc2fe96f1e28f2c003d0773547ffbbbca32b45553023979cede28b25277b748","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"78f08335729dc94f6ca19b9d6b357afe1b3b7fa534efc561e89179126c3b8028","plan_sha256":"3fc2fe96f1e28f2c003d0773547ffbbbca32b45553023979cede28b25277b748"} | PASS | Read-only audit of the pending packages against main 035143d1 and decisions W03-D70 to W03-D76, 2026-11-14: stale statements corrected (fixed registry version value, stale baseline or merge order); every other byte unchanged (checked by diff). | yes | none |
| EVD-004 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Re-approve all three (Recommended) to the re-approval question naming the new bytes of SPEC-0196, SPEC-0205 and SPEC-0209, here spec.md 78f08335 and plan.md 3fc2fe96, 2026-11-14","review_ref":"EVD-003","scope":["SPEC-0205","SPEC-0205-PLAN-0001"],"reviewed_spec_sha256":"78f08335729dc94f6ca19b9d6b357afe1b3b7fa534efc561e89179126c3b8028","reviewed_plan_sha256":"3fc2fe96f1e28f2c003d0773547ffbbbca32b45553023979cede28b25277b748","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-005 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | WORK-001 | Independent semantic review | {"spec_sha256":"bf66fd96dc9c60a19bffb1e04da8fe85e3eabfb2008fd0fec1cab109a4b72730","plan_sha256":"3190a496172cf29e54a1746d01bea5d34a28681aba987cb09cb1c22af52da6a9"} | PASS | Mechanical move of the approved Spec and Plan to the common Spec and Plan forms (W03-D84). Both files moved by SPEC-0200's heading map with version 1.0.0 raised to 2.0.0 (W03-D59 Q4) and `updated` 2026-11-15, status `approved` unchanged. Converter `convert.py` of SPEC-0200 through its wrapper `conv.py` of SPEC-0201 and SPEC-0203, which adds a label line where two lists or a list and a paragraph merge under one heading; the Spec's three-item boundary list split as In Scope (first item) and Non-goals (the other two); the sorted non-heading, non-blank lines before and after are equal except for: frontmatter `version` and `updated`; the Spec criteria header (`Criterion`, `Acceptance evidence`) mapped to `Criterion ID`, `Expected Result`; the added label lines `Contracts:`, `Data modeling and storage strategy:`, `Interfaces and data structures:`, `Edge cases and error handling:` and `Failure modes and fallback or human escalation:` (Spec) and `Goals and in-scope:`, `Non-goals and out-of-scope:` and `Completion criteria:` (Plan); two explained-none lines under Spec References; two pointer lines under Plan Dependencies, one under Change and Rollback, one under Escalation and one under Durable Meaning; the three Plan Work Breakdown rows whose Spec link fragment became `spec.md#criteria`; and the Plan promotion table header mapped to the four common names with one added `Acceptance` cell for its one row, which restates the condition the Plan's Promotion table already gives. In this Task, the evidence table header takes the common names (`Evidence` to `Evidence ID`, `Check` to `Command`, `Criteria` to `Consumer`) and every Spec link fragment becomes `#criteria`; the Consumer cell of EVD-001 to EVD-004 reads VAL-LISTREMOVAL-002 instead of VAL-LISTREMOVAL-001, because the common Task check `TASK-EVIDENCE-WORK` maps each check to the criterion of its work unit and WORK-001 carries VAL-LISTREMOVAL-002 (the one cell change beyond the heading map, reported for approval). No other line differs. | yes | none |
| EVD-006 | [VAL-LISTREMOVAL-002](../spec.md#criteria) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer \"Mechanical move + check, blanket OK (Recommended)\" to the question on moving every remaining package's approved Spec and Plan to the common Spec and Plan forms (W03-D84), covering the SPEC-0205 move of spec.md and plan.md to the bytes named here, dated 2026-11-15 Asia/Seoul","review_ref":"EVD-005","scope":["SPEC-0205","SPEC-0205-PLAN-0001"],"reviewed_spec_sha256":"bf66fd96dc9c60a19bffb1e04da8fe85e3eabfb2008fd0fec1cab109a4b72730","reviewed_plan_sha256":"3190a496172cf29e54a1746d01bea5d34a28681aba987cb09cb1c22af52da6a9","validity":"confirmed","revocation":"none"} | PASS | Approves the moved Spec and Plan bytes only (the content of the approved bytes is unchanged, W03-D84); accepts no criterion. | yes | none |

### Resolution Links

The Resolves column of the evidence table under Results names the earlier evidence row that each PASS row closes.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LISTREMOVAL-001](../spec.md#criteria) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-LISTREMOVAL-002](../spec.md#criteria) | pending | none | Implement WORK-001 and WORK-003 and record PASS evidence | platform |

### Remaining Conditions

No separate remaining-condition list is kept here; the Disposition and Current owner columns of the criterion decisions state what remains and who owns it.

## Handoff

### Promotion Receipt

No separate promotion receipt is kept here; the receipt of each Plan promotion row, where the Plan has one, is recorded in the evidence rows under Results.

### Next Owner

The Spec and Plan keep `status: approved`, are in the common Spec and Plan forms at version 2.0.0, and carry the review and approval receipts of EVD-005 and EVD-006. Implementation is not started. The three WORK rows keep their status.
