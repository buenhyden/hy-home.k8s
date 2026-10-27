---
title: "Change Kinds and Authoring Prompts"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0128-TSK-0001"
parent_ids: ["SPEC-0128-PLAN-0001"]
---

# Task: Change Kinds and Authoring Prompts

## Overview

Add the change-kind table and authoring prompts and reject link-only
instruction sections. It executes [SPEC-0128](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request: the operator said on 2026-10-27 to proceed as recommended; slice
  C of the SPEC-0125 status table covers CR-06.04, 06.07, 06.09, 06.10 and
  07.04.
- Start: main `71c59deb`, branch `feat/sdlc-change-kinds-and-prompts`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CK-001](../spec.md#success-criteria--verification-plan) | Add the change-kind table and touchpoint sentences | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-CK-002](../spec.md#success-criteria--verification-plan) | Add the Spec, Plan and Task prompts | platform | in-progress | PASS | EVD-005 closes EVD-002 |
| WORK-003 | [VAL-CK-003](../spec.md#success-criteria--verification-plan) | Reject link-only instruction sections | platform | in-progress | PASS | EVD-006 closes EVD-003 |
| WORK-004 | [VAL-CK-004](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CK-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Governance review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CK-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template tests | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-CK-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Profile validator tests | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-CK-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-CK-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template tests | Branch `feat/sdlc-change-kinds-and-prompts`: `python3 scripts/validate-document-contract-registry.py`, `python3 -m unittest tests.test_repository_form_contracts` | PASS | The Spec template asks for normal, error and boundary scenarios with their requirements; the Plan template asks for architecture views or ADRs, interfaces, migration and rollback; the Task evidence prompt asks for command, tool version, exit code and UTC time. The registry passes 976 paths and the form tests pass | yes | EVD-002 |
| EVD-006 | [VAL-CK-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Profile validator tests | Same branch: `python3 -m unittest tests.test_operations_section_contract` with the previous and the new `scripts/validate-markdown-profiles.py`; `python3 scripts/validate-markdown-profiles.py` over the repository | PASS | With the previous validator the link-only test failed for all three bodies (a bare link, a link list and an autolink). With the change all eight module tests pass: link-only bodies are empty, a sentence with an instruction and a link fills the section, and Related Documents may hold links only. The repository-wide profile run reports no violations; ruff check and format pass | yes | EVD-003 |
| EVD-007 | [VAL-CK-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Governance review | PR #183 independent review of `04ee94b2` | FAIL | The table stated rules its owners do not contain: an independent security review, a mandatory return of operations learning to its Requirement, a Stage 03 package for every Archive disposition, and break-glass safety checks; the approval column mixed authoring and delivery approval. The review also noted that reference-style links and bare URLs still count as content, an accepted gap like the `See` sentence, and that EVD-005's registry count of 976 paths was taken before this package's files; the current count is 979 | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-CK-001](../spec.md#success-criteria--verification-plan) | pending | none | Table and review remain | platform |
| [VAL-CK-002](../spec.md#success-criteria--verification-plan) | pending | none | Prompts remain | platform |
| [VAL-CK-003](../spec.md#success-criteria--verification-plan) | pending | none | Validator change remains | platform |
| [VAL-CK-004](../spec.md#success-criteria--verification-plan) | pending | none | Staged QA and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `.agents/governance/sdlc.md`,
  `docs/99.templates/templates/specs/spec.template.md`,
  `docs/99.templates/templates/specs/plan.template.md`,
  `docs/99.templates/templates/specs/task.template.md`,
  `scripts/validate-markdown-profiles.py` and
  `tests/test_operations_section_contract.py`.
- **Forbidden Paths**: existing Specs, Plans, Tasks and operations documents,
  provider settings and credentials.
- **Approval Required**: the operator said on 2026-10-27 to proceed as
  recommended. Push, pull request and merge follow RUN-0013.
- **Static Validation**: focused tests and `qa.py staged`.
- **Live Validation**: none.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
