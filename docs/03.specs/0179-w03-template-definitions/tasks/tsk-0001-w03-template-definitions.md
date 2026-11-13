---
title: "W03 TemplateDefinitions for Templates Without a Common Role"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0179-TSK-0001"
parent_ids: ["SPEC-0179-PLAN-0001"]
---

# Task: W03 TemplateDefinitions for Templates Without a Common Role

## Overview

This Task records handoff W03-H06, the TemplateDefinitions for the fourteen templates without a common role, for [SPEC-0179](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to follow the requirements where a choice or correction is needed, to present decisions with options, to check existing work before the next task, to do now anything due before W03, and approved commit, push, PR and merge. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-template-definitions` from `1282f0c0` (`main` merge of PR #243); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08, W03-D09 and W03-D10; EVD-018 (current v14.7 requirements prevail).
- **Decisions taken in this package:** asked how to group the fourteen templates into roles, the user answered "Group same form (Recommended)" (W03-D20); asked how to resolve the m0001 research `Sources` table that conflicts with its template table, the user answered "Migrate to template (Recommended)" (W03-D21); both on 2026-11-13.
- **Requirement basis:** DOC-05, DOC-11, R45-10 and the TEMPLATE-DEFINITION-CONTRACT note that the role table is not a closed list; read-only inputs under `_workspace/workspace_execution_tasks/`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TPLDEF-001](../spec.md#success-criteria--verification-plan) | Role list and schema; bindings; table checks; TemplateDefinitions and tables; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-TPLDEF-002](../spec.md#success-criteria--verification-plan) | m0001 `Sources` table; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-TPLDEF-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `2e51f304…`, plan.md `8ec3c7b3…`, with scratch simulations of the bindings, every table against every current source document and the heading-line design; 2026-11-13 | FAIL | REJECT: BLOCK the table count is eighteen, not sixteen; BLOCK the six SDLC templates also lack a TemplateDefinition and no row carried them; FIXes on the form enum and a typed form identifier, the tests that break, where the registry reads a template body, ADR-0059's H2-list removal clause, a false Plan base fact, the Task file and the README wording; NITs on unread tables, wording and the Relevance meaning. The reviewer confirmed the counts, that only the m0001 `Sources` table conflicts, and that nothing else assumes a role has a form. | no | none |
| EVD-002 | [VAL-TPLDEF-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"a2a57276d21cc87b4be37680c13d2b53fad6f919567c0f2cacdfa7d59dfd4358","plan_sha256":"c61cb26a3678fe898a8700e6c32909d5d330437c7d0923c28a58eda6b44e55f6"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: every round-1 finding verified fixed, with W03-H13 appended to the SPEC-0161 Task; round 2 asked two wording fixes (the Plan risk row names the `BODY-TABLE-SECTION` check; the Task Allowed Paths name W03-H13), which round 3 verified as the only Plan change; no other change in meaning; verdict APPROVE. Open NIT not applied: the Plan risk row's review cue still says "a registry diagnostic". This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-TPLDEF-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0179 approval question naming spec.md a2a57276 and plan.md c61cb26a dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0179","SPEC-0179-PLAN-0001"],"reviewed_spec_sha256":"a2a57276d21cc87b4be37680c13d2b53fad6f919567c0f2cacdfa7d59dfd4358","reviewed_plan_sha256":"c61cb26a3678fe898a8700e6c32909d5d330437c7d0923c28a58eda6b44e55f6","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-TPLDEF-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-TPLDEF-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D20, W03-D21, W03-H13 and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every template body, every other document body, `_workspace/workspace_execution_tasks/`, `.github/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's standing 2026-11-13 instruction
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
