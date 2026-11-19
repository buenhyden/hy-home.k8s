---
title: "Q07 History-Bound Check Conversion Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0225-PLAN-0001"
parent_ids: ["SPEC-0225"]
---

# Q07 History-Bound Check Conversion Implementation Plan

## Overview

### Outcome

This Plan executes the [Spec](spec.md): four units convert the checks that
Q07-H01 names, and the residue records what stays as cutover data.

### Constraints

Accepted ADR bodies, published reference members and completed Task evidence
do not change; only the 36 retained ADRs gain a frontmatter marker.

#### Global Constraints

Every unit inherits the approved [Spec](spec.md). No check or test is weakened:
a removed test covered only removed behavior, and every converted guard keeps
a regression that fails against the `cabab987` code.

#### Risks and Mitigations

- **A removed reader was still needed.** The comparison base of every current
  check is a MAJOR 21 registry; an older blob now falls back to the current
  registry, which a regression shows.
- **A reset opens without approval.** A baseline change is a registry edit in
  a user-approved change; within one baseline every refusal holds, which a
  regression shows.
- **The marker drifts from the form.** The registry refuses an ADR retained
  form without the marker or with a bound, and `FM-RETAINED-FORM` refuses the
  marker on a document that is not accepted.

#### Escalation

A check that cannot be converted without weakening a guarantee is reported to
the user and recorded in Q07-H01.

## Dependencies

### Prerequisites

The user's choices of 2026-11-19 for items 2 to 5 and the read of SPEC-0223
EVD-008.

### Shared Resources

`docs/99.templates/registry.json`, its schemas and `scripts/document_contracts.py`
change together.

## Work Breakdown

### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HISTORY-001](spec.md#criteria) | Read only the current registry MAJOR; remove the older-generation reads and the tests of them | None | [Task](01.tasks/tsk-0001-q07-history-bound-checks.md) | Registry schema version, cumulative history and form tree suites |
| WORK-002 | [VAL-HISTORY-001](spec.md#criteria) | Find requirement documents by route in tests | None | [Task](01.tasks/tsk-0001-q07-history-bound-checks.md) | Terminal contract, identity and scope suites |
| WORK-003 | [VAL-HISTORY-002](spec.md#criteria) | Add the policy rule ID baseline | None | [Task](01.tasks/tsk-0001-q07-history-bound-checks.md) | Policy rule history suite |
| WORK-004 | [VAL-HISTORY-003](spec.md#criteria), [VAL-HISTORY-004](spec.md#criteria) | Select the retained ADR form by marker; record Q07-H01 | WORK-001 | [Task](01.tasks/tsk-0001-q07-history-bound-checks.md) | Form tree and key contract suites, staged QA |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | One registry generation read | none | platform | `scripts/`, `tests/` | VAL-HISTORY-001 | document-contract-tests, document-lifecycle-tests |
| WORK-002 | No fixed requirement path in tests | none | platform | `tests/` | VAL-HISTORY-001 | document-contract-tests |
| WORK-003 | Declared baseline for codes | none | platform | `scripts/`, `docs/99.templates/`, `docs/00.workspace/03.process/`, `tests/` | VAL-HISTORY-002 | document-lifecycle-tests |
| WORK-004 | Marker-selected retained ADR form; residue recorded | WORK-001 | platform | `scripts/`, `docs/99.templates/`, ADR frontmatter, `docs/03.specs/`, `tests/` | VAL-HISTORY-003, VAL-HISTORY-004 | Staged QA selection |

#### Change and Rollback

The units land as one commit, because the registry, schema and readers move
together; reverting it restores the bound checks.

### Dependency Edges

WORK-004 follows WORK-001, which removes the reads it would otherwise extend.

## Verification Plan

### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| qa-staged | Every selected gate passes on the exact index | Staged index | Repository-static only | Every commit | Staged QA log |

### Evidence Plan

Staged QA runs before each commit and in the pre-commit hook; hosted checks run
once on the pull request.

## Promotion Map

### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| Rule ID baseline | [Document lifecycle](../../00.workspace/03.process/document-lifecycle.md) | DOCLIFE-R022 names the registry baseline. | Rules, DOCLIFE-R022 |

### Consumer Updates

The Q07-H01 row of the SPEC-0223 Task names what stays as cutover data.
