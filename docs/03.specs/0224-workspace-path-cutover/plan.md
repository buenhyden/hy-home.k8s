---
title: "Workspace Path Cutover Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0224-PLAN-0001"
parent_ids: ["SPEC-0224"]
---

# Workspace Path Cutover Implementation Plan

## Overview

### Outcome

This Plan executes the [Spec](spec.md): one change moves the W documents and
numbers the category folders, with every consumer updated in place.

### Constraints

Document IDs, rule IDs and historical bodies do not change; history is not
rewritten.

#### Global Constraints

Every unit inherits the [Spec](spec.md). Two active copies of one meaning never
exist, so the move and its consumers land in one commit.

#### Risks and Mitigations

- **A reader keeps an old path segment.** Every path component and regex in
  `scripts/` and `tests/` is searched, and every suite runs on the change.
- **A historical body is rewritten.** ADRs, published reference members,
  Archived Lineage and completed Task evidence get link destinations only.
- **A move hides an identity change.** The lifecycle comparison admits a move
  only with an unchanged profile and artifact ID; a regression proves a rename
  to a new ID stays refused.

#### Escalation

A consumer that cannot move in this change stops the commit and is reported
to the user.

## Dependencies

### Prerequisites

The user's adoption of `docs/00.workspace/` (SDLC-H01, 2026-11-18) and the
path plan (DOC-H01, 2026-11-19), and the request of 2026-11-19.

### Shared Resources

`docs/99.templates/registry.json`, `scripts/validation/registry.json` and the
lifecycle validator change together.

## Work Breakdown

### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CUTOVER-001](spec.md#criteria) | Move the W documents and split SAFE and GIT | None | [Task](01.tasks/tsk-0001-workspace-path-cutover.md) | Registry and policy rule checks |
| WORK-002 | [VAL-CUTOVER-002](spec.md#criteria) | Number the category folders and update profiles, readers, tests and links; add the move rule | WORK-001 | [Task](01.tasks/tsk-0001-workspace-path-cutover.md) | Lifecycle, link and profile checks and suites |
| WORK-003 | [VAL-CUTOVER-003](spec.md#criteria) | Point the knowledge check at the workspace glossary and run the selected checks | WORK-002 | [Task](01.tasks/tsk-0001-workspace-path-cutover.md) | Staged QA |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | W documents moved, SAFE and GIT split | none | platform | `docs/00.workspace/`, `.agents/governance/`, `docs/99.templates/` | VAL-CUTOVER-001 | document-contract-registry, markdown-profiles |
| WORK-002 | Numbered folders with working consumers | WORK-001 | platform | `docs/`, `scripts/`, `tests/`, tracked links | VAL-CUTOVER-002 | document-lifecycle, links-and-owners, contract suites |
| WORK-003 | Glossary checked at its new path; QA green | WORK-002 | platform | `scripts/validate-knowledge-surface.py`, `tests/` | VAL-CUTOVER-003 | knowledge-surface, staged QA |

#### Change and Rollback

The three units land as one commit, because a split state would leave two
active owners or broken readers; reverting that commit restores the old tree.

### Dependency Edges

WORK-001, then WORK-002, then WORK-003, in one commit.

## Verification Plan

### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| qa-staged | Every selected gate passes on the exact index | Staged index | Repository-static only | Every commit | Staged QA log |

### Evidence Plan

Staged QA runs before the commit and in the pre-commit hook; hosted checks run
once on a pull request when the user asks for one.

## Promotion Map

### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| Document move rule | [Document lifecycle](../../00.workspace/03.process/document-lifecycle.md) | The policy states DOCLIFE-R023. | Rules, DOCLIFE-R023 |

### Consumer Updates

The registry `policy_rule_ids` records of SAFE and GIT list their rule IDs per
policy; the residue rows SDLC-H01 and DOC-H01 name this package.
