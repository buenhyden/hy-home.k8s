---
title: "Archive Final Units"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0134"
---

# Archive Final Units Technical Specification (Spec)

## Overview

After [SPEC-0132](../0132-archive-registry-and-test-consumers/spec.md), nine
Archive units stay `retained` and `unreviewed`. On 2026-10-28 the operator
decided two things:
- move SPEC-0080 and SPEC-0103, which only tests read, to Git history;
- record a `usable` assessment with a reason for each of the other seven.

That gives every remaining unit a recorded rationale, the gap CR-04.02 and
CR-08.03 named. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-archive-final-units.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - three tests that read SPEC-0080 or SPEC-0103 from the working tree:
    - `test_archive_disposition_lifecycle` and `test_task_acceptance_contract`
      read their bodies from the last `main` commit that holds them;
    - `test_documentation_link_boundary` uses the retained SPEC-0072 for its
      saved-backlink case;
  - the links to the two units in REQ-0003 and the SPEC-0105 Task 0003 Inputs;
  - removing the two units with `git-history-only` rows;
  - `usable` rows for ADR-0032, SPEC-0004, SPEC-0005, SPEC-0008, SPEC-0054,
    SPEC-0072 and SPEC-0104.
- Non-goals:
  - removing any of the seven, changing a frozen Archive record, a validator
    or the registry;
  - changing what any test asserts.

## Contracts

- A test that read a removed body reads the same bytes from a pinned commit,
  or uses a retained unit with the same property, and asserts the same thing.
- A unit is removed only whole, only with Hold `none`, only when nothing
  outside Stage 98 links to or reads it, and only when its envelope resolves.
- A `usable` row keeps availability `retained` and names this Task as its
  Decision; the Task states the reason the unit stays.

## Core Design

The rows use the ADR-0040 assessment table. The tests follow the pinned
read already used for ADR-0035 in SPEC-0132.

## Data Modeling & Storage Strategy

Nine rows in the Retention Assessment table of `docs/98.archive/README.md`.

## Interfaces & Data Structures

Row columns follow the registry `archive_assessment` contract.

## Edge Cases & Error Handling

- A pinned read needs the commit in the checkout; local QA has full history.
- A unit with a consumer outside this repository cannot be observed; removal
  stays recoverable from Git history.

## Failure Modes & Fallback / Human Escalation

A removed unit returns only as a new unit under a new decision, recovered with
`git archive <envelope commit> <original path>`.

## Verification Commands

- The three changed test modules, before and after removal.
- `validate-archive-integrity.py`, `validate-document-lifecycle.py --mode strict`
  and `validate-links-and-owners.py --mode strict` on the removal commit.
- `python3 scripts/qa.py staged` on each exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-AF-001 | The three tests pass with SPEC-0080 and SPEC-0103 removed and assert what they asserted before, and no tracked file outside Stage 98 links to the two units. |
| VAL-AF-002 | Both envelopes equal the current trees and restore with the expected file count. |
| VAL-AF-003 | The two units are absent with `git-history-only` rows, the seven have `usable` rows with a reason in the Task, the validators pass, and staged QA passes on every commit. |
| VAL-AF-004 | An independent reviewer confirms the changes, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AF-001 | Test runs and link search |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AF-002 | Isolated recovery |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AF-003 | Assessment validation and staged QA |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AF-004 | Independent review and hosted checks |
