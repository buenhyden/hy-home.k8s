---
title: "Work Residue Handoff Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0223-PLAN-0001"
parent_ids: ["SPEC-0223"]
---

# Work Residue Handoff Implementation Plan

## Overview

### Outcome

This Plan executes the [Spec](spec.md): the open residue moves here, then
SPEC-0161, SPEC-0221 and SPEC-0222 leave the tree, then the transition adapter
whose removal condition is their exit is deleted. Renumbering, path moves and
history removal stay with Q07-CUTOVER.

### Constraints

No architecture view or ADR changes. ADR-0063 only gets a link update.

#### Global Constraints

Every unit inherits the approved [Spec](spec.md). The three Tasks freeze their consumer, hold,
authority and method decision before the source commit their recovery proof
names.

#### Risks and Mitigations

- **A consumer of a deleted file is missed.** The full tree is searched for
  each package path and ID before the exit, and every selected check runs on
  the exit commit.
- **The adapter is still read.** The lifecycle check compares the exit commit
  with its base, whose Tasks carry the recorded header, so the adapter leaves
  only in a later commit.

#### Escalation

A consumer that cannot be updated in this change defers that package's exit
and is reported to the user.

## Dependencies

### Prerequisites

The user's decision of 2026-11-19 to delete the three packages now and move
the residue.

### Shared Resources

`docs/03.specs/work-residue-ledger.json` and `docs/99.templates/registry.json`
change in order: WORK-001, then WORK-002, then WORK-003.

## Work Breakdown

### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RESIDUE-001](spec.md#criteria) | Move the open residue and freeze the three Tasks | None | [Task](tasks/tsk-0001-work-residue-handoff.md) | Ledger gate |
| WORK-002 | [VAL-RESIDUE-002](spec.md#criteria) | Exit the three packages and update their consumers | WORK-001 | [Task](tasks/tsk-0001-work-residue-handoff.md) | Lifecycle, registry and contract checks |
| WORK-003 | [VAL-RESIDUE-003](spec.md#criteria) | Remove the Task header transition adapter, its readers' branches and its tests | WORK-002 | [Task](tasks/tsk-0001-work-residue-handoff.md) | `run-contract-tests.py --suite document` before and after, and staged QA |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Open residue hosted here; three Tasks frozen | none | platform | `docs/03.specs/` | VAL-RESIDUE-001 | work-residue-ledger, document-lifecycle |
| WORK-002 | Three packages deleted with lineage | WORK-001 | platform | `docs/03.specs/`, `docs/01.requirements/0003-*`, `docs/02.architecture/decisions/0063-*`, `docs/99.templates/registry.json`, `.secrets.baseline`, `tests/` | VAL-RESIDUE-002 | Staged QA selection |
| WORK-003 | Adapter, its readers' branches and its tests removed | WORK-002 | platform | `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `tests/` | VAL-RESIDUE-003 | document suite, staged QA selection |

#### Change and Rollback

Each unit is one commit; reverting a commit restores its unit, newest first.

### Dependency Edges

WORK-002 needs the commit of WORK-001 as the recovery source. WORK-003 is a
later commit whose base is the WORK-002 commit, because the lifecycle check
reads the base Tasks, which carry the recorded header until they leave.

## Verification Plan

### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| qa-staged | Every selected gate passes on the exact index | Staged index | Repository-static only | Every commit | Staged QA log |

### Evidence Plan

Staged QA runs before each commit and again in the pre-commit hook; hosted
checks run once on the pull request.

## Promotion Map

### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |

### Consumer Updates

The ledger gate and Q07-CUTOVER read the live residue table here.
