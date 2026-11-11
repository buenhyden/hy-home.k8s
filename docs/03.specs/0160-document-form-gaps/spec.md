---
title: "Document Form Gaps"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0160"
---

# Document Form Gaps Technical Specification (Spec)

## Overview

This approved change contract covers stage W03 of the externally supplied v14.2 execution package, which stays git-ignored evidence and never repository authority. A read-only W03 intake re-checked the three W03 handoffs from the W00 crosswalk and found all three still open. The front-matter rules of the Markdown profile validator have no regression test. The audit form records a finding without its requirement, fact or hypothesis, action or acceptance. Two texts restate rules their owners already state and drift unchecked. This change closes those gaps with the options the user chose on 2026-11-11. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the requirements. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-document-form-gaps.md) records execution and acceptance.

## Strategic Boundaries & Non-goals

- Scope:
  - **DOC-04:** a new test module `tests/test_document_frontmatter_negatives.py` for `FM-DUPLICATE-KEY`, `FM-DATE`, `FM-FUTURE-DATE`, `FM-FORBIDDEN`, `FM-KEYSET` and `FM-KEY-ORDER`, registered in the `document` suite of `scripts/run-contract-tests.py` and routed in `scripts/validation/registry.json`;
  - **SCOPE-03:** new columns in the Findings and Gaps table of `docs/99.templates/templates/references/audit.template.md`, with a form test in the same module;
  - **DOC-10:** the hand-kept "Today:" folder list in `.agents/governance/document-authoring.md` replaced by a pointer to the registry profile `common/folder-agents-guide`, and the Task Status Authoring, Spec·Plan Direct Approval and Spec·Plan First-Record Approval subsections of `docs/99.templates/README.md` replaced by one pointer paragraph to the document lifecycle policy, each file with its patch `version` bump and `updated` date; because those subsections were the only prose list of the first-record receipt JSON keys, one sentence naming the exact keys moves into `.agents/governance/document-lifecycle.md`, with one clause stating the two Task status rules only that text stated (a multi-row Task that carries `status` must equal the derived value, and an unreadable current-column table fails as a missing status), with its patch `version` bump and `updated` date; the `(Stage 99 Task Status Authoring)` reference in `document-authoring.md` and the Task form's author prompt in `docs/99.templates/templates/specs/task.template.md` point to the lifecycle policy instead, so no pointer loops back;
  - **W03-A, Q-03:** a comparison of the package's 19-role candidate table (an unapproved draft) with the current approved registry profiles, recorded in the Task with each candidate type's current profile, live-document count, required H2 sets, differences and affected consumers, including current profiles outside the candidate list;
  - this package with its Stage 03 README entry and REQ-0003 back-link.
- The candidate table is not adopted by this package: no template, profile, validator or live document changes to match it. Adopting any candidate form is a separate user decision on a named Q-03 row and a separate change.
- No validator, registry profile or body contract changes. The audit columns are a form change only: the two published audits under `docs/90.references/audits/` are frozen history and keep their form, so no body contract enforces the columns.
- Not adopted, as already recorded in REQ-0003 Scope and Non-goals: a generated reverse index in place of hand-written reciprocal links, and Stage 03 renumbering. The direct `BODY-LINK-RECIPROCAL` test stays with W05.
- Open question: none. The user chose audit-form columns and pointer replacement on 2026-11-11.

## Contracts

- Each of the six front-matter rules has at least one deterministic test that builds a synthetic document violating only that rule and observes the rule ID, and one passing control document. A mutation run that disables a rule in a disposable copy makes its test fail.
- The audit form's Findings and Gaps table has the columns `ID`, `Finding or gap`, `Requirement`, `Fact or hypothesis`, `Severity`, `Evidence`, `Action` and `Acceptance`, in that order, each with an author prompt; a test asserts the header.
- `document-authoring.md` no longer lists folder `AGENTS.md` paths; it names the registry profile that governs them and says how to list them. The Stage 99 README keeps its other sections and points to the document lifecycle policy for Task status and Spec/Plan approval rules. The lifecycle policy names the exact JSON keys of the first-record review row and approval receipt and states the two Task status rules, and no reference points from an owner back to the README, so no rule loses its only prose owner.
- The Q-03 comparison covers every candidate type, excludes the two protected domains as the package itself does, and lists the current profiles the candidate list omits.
- No rule changes meaning; the strict document validators pass.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; this change adds tests and edits a form and two texts, and changes no architecture. Tests call the existing validator functions on in-memory text or temporary files, as the current document tests do.

## Data Modeling & Storage Strategy

No stored data changes.

## Interfaces & Data Structures

No interface changes. The audit form gains five columns.

## Edge Cases & Error Handling

- A rule that cannot be isolated by one synthetic document is tested with the smallest document that triggers it, and the test names any second diagnostic it also sees.
- The published audits are not edited; a new audit starts from the new form.

## Failure Modes & Fallback / Human Escalation

If a test shows a rule does not fire as its ID claims, that is a validator defect: record it and hand it to W05, and do not weaken the test. A conflict with an accepted contract is shown to the user.

## Verification Commands

- `python3 -m unittest tests.test_document_frontmatter_negatives` and the mutation run on a disposable copy.
- `python3 scripts/run-contract-tests.py --root . --suite document`.
- The strict document validators, the staged lifecycle check and the active commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-FORM-001 | Each of the six front-matter rules is observed by its test, a control document passes, and a mutation run disabling each rule fails its test. |
| VAL-FORM-002 | The audit form has the eight columns in order with author prompts, the form test passes, and the published audits are unchanged. |
| VAL-FORM-003 | The folder list and the README restatement are replaced by pointers, the receipt keys are named in the lifecycle policy, the Q-03 comparison is recorded in the Task, an independent review finds no blocking issue, and the strict document checks and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORM-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Deterministic negative tests and a mutation run. |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORM-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Form header test; published audits unchanged. |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORM-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | One owner per rule; independent review, strict document checks and commit hooks. |
