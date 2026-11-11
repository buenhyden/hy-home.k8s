---
title: "Document Form Gaps Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0160-PLAN-0001"
parent_ids: ["SPEC-0160"]
---

# Document Form Gaps Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two execution constraints. First, no repository file changes outside this package, the Stage 03 README, one back-link sentence in the Traceability section of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#traceability), `tests/test_document_frontmatter_negatives.py`, `scripts/run-contract-tests.py`, one exact route in `scripts/validation/registry.json`, the Findings and Gaps table of `docs/99.templates/templates/references/audit.template.md`, the folder list in `.agents/governance/document-authoring.md` and three subsections of `docs/99.templates/README.md`, one sentence in `.agents/governance/document-lifecycle.md` naming the first-record receipt JSON keys and one clause there stating the two Task status rules the README alone stated, the `(Stage 99 Task Status Authoring)` reference in `.agents/governance/document-authoring.md`, the Task Table author prompt in `docs/99.templates/templates/specs/task.template.md`, each file with its patch `version` bump and `updated` date, and `.secrets.baseline` entries marking this Task's reviewed SHA-256 document digests as non-secret. Second, mutation runs use disposable copies outside the repository.

## Overview

Close the three W03 gaps defined in [SPEC-0160](spec.md). [Task 0001](tasks/tsk-0001-document-form-gaps.md) owns execution evidence and criterion acceptance.

## Context

W02 closed on branch `claude/w02-package-exit` at `78bab1dd`; this branch, `claude/w03-document-forms`, starts there. The W03 intake re-checked the W00 handoffs DOC-04, SCOPE-03 and DOC-10 and found them open. On 2026-11-11 the user chose audit-form columns and pointer replacement. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) constrains the design; no interface, migration or rollback surface beyond these files changes.

## Goals & In-Scope

- Write the front-matter tests and the audit form test, and show each rule's test fails under a mutation.
- Add the five audit columns to the form.
- Replace the folder list and the README restatement with pointers, and name the receipt JSON keys in the lifecycle policy.
- Record the Q-03 comparison of the 19-role candidate table with the current profiles in the Task, without adopting any candidate form.
- Add this package to the Stage 03 README and link it from REQ-0003 Traceability.

## Non-Goals & Out-of-Scope

- Validator, registry profile or body contract changes; edits to published audits.
- A generated reverse index, Stage 03 renumbering, and the `BODY-LINK-RECIPROCAL` test (W05).
- Any push, PR, merge or package exit without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORM-001](spec.md#success-criteria--verification-plan), [VAL-FORM-002](spec.md#success-criteria--verification-plan) | Write the test module, register and route it, add the audit columns, run the mutation check. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-document-form-gaps.md) | Focused tests, mutation run and the `document` suite. |
| WORK-002 | [VAL-FORM-003](spec.md#success-criteria--verification-plan) | Replace the folder list and the README restatement; record the Q-03 comparison; obtain independent review; run commit checks. | WORK-001. | [Task 0001](tasks/tsk-0001-document-form-gaps.md) | Independent review, strict document checks and commit hooks. |

## Verification Plan

- The six front-matter tests and the form test pass; a mutation disabling each rule fails its test.
- `python3 scripts/run-contract-tests.py --root . --suite document` stays green.
- An independent read-only reviewer checks the tests, the form, the pointer edits, the lifecycle sentence and clause, and the Q-03 table.
- Strict document checks, the staged lifecycle check and the active commit hooks run on the exact index.
- Architecture compliance: confirm no AD, ADR, validator or registry profile changed.

## Risks & Mitigations

- **A pointer loses information a reader needed.** Mitigation: the review checks that each removed rule is stated by its owner; the receipt JSON keys, which only the removed README text listed, move into the lifecycle policy.
- **A test passes for the wrong reason.** Mitigation: the mutation run.

## Completion Criteria

All three criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
