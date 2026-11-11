---
title: "Package Exit Shape Check"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0159"
---

# Package Exit Shape Check Technical Specification (Spec)

## Overview

This approved change contract covers stage W02 of the externally supplied v14.2 execution package, which stays git-ignored evidence and never repository authority. The W02 intake found one gap (ARC-02): nothing refuses a Stage 03 package leaving the tree in the wrong shape. Deleting an unfinished package, deleting only some of its files, deleting it without an Archived Lineage entry, or reusing a finished package's Spec or Plan as live scope all pass every check today. [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) Decision 6 keeps disposition manual, and its Consequences say enforcement needs a separately designed follow-up. This change is that follow-up. It adds one event-scoped rule to the existing lifecycle comparison and amends ADR-0056 only for that rule, through a proposed successor ADR. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the governance requirements. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-package-exit-shape-check.md) records execution and acceptance.

## Strategic Boundaries & Non-goals

- Scope:
  - a `LIFECYCLE-PACKAGE-EXIT` rule in `scripts/document_lifecycle.py`, wired in `scripts/validate-document-lifecycle.py` for `staged` mode only;
  - its regression module `tests/test_document_lifecycle_package_exit.py`, registered in the `document-lifecycle` suite of `scripts/run-contract-tests.py` and routed by one exact entry in `scripts/validation/registry.json`;
  - [ADR-0057](../../02.architecture/decisions/0057-package-exit-shape-check.md), a proposed amendment of ADR-0056 Decision 6 for this rule only, accepted only by the user, with its entry in the decisions README and, once accepted, in the AD-0006 decision list with that file's patch `version` bump and `updated` date;
  - one sentence in the Validation and Refresh section of `.agents/governance/document-lifecycle.md`, with its patch version bump and `updated` date;
  - rule 7 of `docs/03.specs/AGENTS.md`, adding the Task freeze, the Archived Lineage proof and deferral;
  - this package with its Stage 03 README entry and REQ-0003 back-link.
- The rule checks the shape of one staged change only. It does not check whether a finished package still exists, how long it has existed, or whether a deferral is justified. It adds no deferral marker or field, and never reads `docs/98.archive/` or history beyond the one base.
- Recovery proof, hold review and authority stay manual (ADR-0056 Decision 6); the rule only checks that the lineage owner names the package path.
- No CI or explicit-ref coverage: in those modes the base is the merge base, so a package created and closed in one range is invisible. Per-commit replay is left to W05.
- No change to the registry schema, Stage 99 forms, profiles or other governance text.
- Open question: none. On 2026-11-11 the user chose the event-scoped rule over a presence gate or no check.

## Contracts

- A package is a folder `docs/03.specs/<####-slug>/`. It is finished at the base when every `tasks/*.md` file it has is `completed` or `cancelled` and either it has at least one such Task or its `spec.md` is `cancelled` (a withdrawn package without a Task). A cancelled Spec with an unfinished Task is not finished, so unfinished evidence cannot leave with it.
- In `staged` mode the rule fails, as `LIFECYCLE-PACKAGE-EXIT`, when the staged change:
  - **R1** deletes any file of a package that is not finished at the base;
  - **R2** deletes some but not all tracked files of a package;
  - **R3** deletes a whole package while no Stage 01 Requirement document changed in the same change has an `Archived Lineage` heading (level 2 or 3) whose section contains the literal `docs/03.specs/<####-slug>/`;
  - **R4** modifies the `spec.md` or `plan.md` of a package that has at least one Task, all terminal at the base, and is still present. A package without a Task keeps ordinary Spec and Plan edits.
- Admitted: appending to a terminal Task, the whole-package closure with lineage text, any change that does not touch a package, a Spec or Plan `cancelled` transition with its Task, and new packages. Cancelling and deleting a package in one change is refused by R1: a withdrawal records the cancellation first and the deletion, with its Archived Lineage summary, in a later change, which keeps the lifecycle policy's same-change summary and deletion.
- Each diagnostic names the package path, the rule letter and what was expected; the exit code is 1. Other modes are unchanged.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance system view. The rule is one pure function over the full base and proposed snapshots and their texts (`base_snapshot`, `proposed_snapshot`, `base_texts`, `proposed_texts`) that the staged comparison already builds, called from the staged path of the lifecycle validator; the changed-path document maps are not enough, because an unchanged Task must still be judged. It reads no Git object beyond those maps, so it adds no subprocess or read. ADR-0057 records the narrow amendment: Decision 6 stays manual for recovery, hold and authority, and the staged shape of a package exit becomes checked.

## Data Modeling & Storage Strategy

No stored data changes. The rule reads the base and proposed snapshots only.

## Interfaces & Data Structures

The validator's command line and modes are unchanged; one rule ID can appear in its existing diagnostic form.

## Edge Cases & Error Handling

- A package with several Task files is finished only when all are terminal.
- A package without a Task at the base is finished only when its Spec is `cancelled`; otherwise deleting it is R1.
- A package whose Spec is `cancelled` but whose Task is still open is not finished; its Task must reach a terminal state first.
- A rename of a package file is already refused by `LIFECYCLE-RENAME`; this rule does not change that.
- Lineage text in a Requirement that is not staged does not satisfy R3, because the closure must update its lineage owner in the same change.

## Failure Modes & Fallback / Human Escalation

If the rule refuses a legitimate change, the change is stopped and returned to Spec review; the rule is not weakened. A newly found conflict with an accepted contract is shown to the user.

## Verification Commands

- Focused tests: `python3 -m unittest tests.test_document_lifecycle_package_exit`, failing before the implementation and passing after it, on isolated temporary Git fixtures.
- `python3 scripts/run-contract-tests.py --root . --suite document-lifecycle`.
- The strict document validators, the staged lifecycle check and the active commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-EXIT-001 | Focused tests fail before and pass after the change: R1 to R4 are each refused, including cancel-and-delete in one change and a cancelled Spec with an open Task; a Task append, a whole-package closure with lineage text under a level-2 or level-3 heading, a withdrawn Task-less package with a cancelled Spec, a Task-less package's Spec or Plan edit and an unrelated change while a finished package stays are admitted. |
| VAL-EXIT-002 | The existing lifecycle suites stay green, other modes are unchanged, and the policy sentence, rule 7 and ADR-0057 state the rule and keep recovery, hold and authority manual. |
| VAL-EXIT-003 | An independent review finds no blocking issue, the user decides on ADR-0057, and the strict document checks and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EXIT-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused RED/GREEN deterministic negative tests on isolated fixtures. |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EXIT-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Existing suites, policy and rule-7 review. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EXIT-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Independent review, strict document checks and commit hooks. |
