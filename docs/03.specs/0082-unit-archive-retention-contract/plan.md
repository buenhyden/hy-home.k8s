---
title: "Unit Archive Retention Contract Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0082-PLAN-0001"
---

# Unit Archive Retention Contract Implementation Plan

## Global Constraints

No frozen Stage 98 record, ledger, retained package, manifest comment, frozen
record table row, or ADR-0038 retained body changes. One document takes one
state edge per integration. A formatter never rewrites frozen content or a
region outside the intended change. Push, pull request, and merge follow the
request owner. No live cluster, provider runtime, or secret action is
authorized.

## Overview

This Plan executes [Spec 0082](spec.md) in three integrations: the proposal, the
acceptance with the machine cutover, and the retention of ADR-0038.

## Context

On 2026-09-15 the request owner chose to adopt the common Archive target in
full: exact-byte retention, a citation table narrowing the Incident exemption,
identity-tracked internal moves, and a work branch with logical commits. The
owner also approved superseding ADR-0038 as a whole over a clause-by-clause
amendment and approved the design sections for the registry, gates, tests, and
evidence placement. Accepting ADR-0039 and retaining ADR-0038 remain separate
decisions.

## Goals & In-Scope

Deliver the proposal on the work branch, prepare the cutover under test, and
retain ADR-0038 through the new machine path once both earlier integrations
land.

## Non-Goals & Out-of-Scope

No frozen rewrite, no retention of SPEC-0079, no public URL routing, and no
adoption of an external preservation standard.

## Work Breakdown

| ID     | Work package                                                                                                                                | Depends on                  | Entry gate                                                         | Exit evidence                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------ | ---------------------------------- |
| WP-001 | Record the survey judgment and correct stale current statements                                                                             | None                        | Approved design                                                    | Staged QA on the correction commit |
| WP-002 | Record the external evidence as research pack 0002                                                                                          | None                        | Approved design                                                    | Strict document gates              |
| WP-003 | Propose ADR-0039 and this package, note the proposed successor in ADR-0038, and update the indexes                                          | WP-001                      | Approved design                                                    | Staged QA on the proposal commit   |
| WP-004 | Activate SPEC-0080 and SPEC-0081 for closure                                                                                                | None                        | Their Tasks record completed work                                  | Lifecycle gate                     |
| WP-005 | Accept ADR-0039, supersede ADR-0038, activate this package, and close SPEC-0080 and SPEC-0081                                               | WP-001 to WP-004 integrated | The request owner accepts ADR-0039                                 | Lifecycle gate                     |
| WP-006 | Declare units, modes, the citation table, and the legacy set in the registry, schema, and loader                                            | WP-005                      | Failing registry regressions                                       | Registry regressions               |
| WP-007 | Decide citation in the shared resolver and consume it in the link and archive validators                                     | WP-006                      | Failing citation regressions for both validators | Link and archive regressions       |
| WP-008 | Compare units as Git objects, admit by anchor state, check envelope objects, admit identity moves, and re-verify every row on the full lane | WP-006                      | Failing lifecycle regressions                                      | Lifecycle and cutover regressions  |
| WP-009 | State the adopted contract in governance, indexes, the skill, and forms, and add the fast gate                                              | WP-007, WP-008              | Green regressions                                                  | Staged and full QA                 |
| WP-010 | Retain ADR-0038 exactly, repoint its current consumers, and close this package                                                              | WP-005 to WP-009 integrated | The request owner approves the disposition                         | Staged and full QA                 |

## Verification Plan

Each work package runs its focused regressions first. Each logical commit runs
`git diff --check`, `git diff --cached --check`, and `python3 scripts/qa.py
staged` over the exact index. Each integration's final tree runs one
`python3 scripts/qa.py full`. Hosted CI, provider runtime, and live evidence are
recorded only when observed.

## Risks & Mitigations

| Risk                                                                 | Mitigation                                                                                        |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| An editor formatter rewrites a whole document, including frozen rows | Rebuild the file from its base bytes and apply only the intended edit, then review the diff scope |
| A state edge lands twice in one integration                          | Keep the three integrations separate and check the lifecycle gate against the merge base          |
| Two citation checks drift apart              | Both validators consume one decision, and a regression exercises each  |
| A shallow clone cannot resolve envelopes                             | Full validation fails rather than skips, and hosted CI fetches full history                       |
| The legacy set grows                                                 | The registry schema pins the sixteen paths and a regression rejects a seventeenth                 |
| ADR-0039 is rejected                                                 | It takes the rejected edge, this package is withdrawn through its `active` and `withdrawn` edges, and the statement corrections stay valid   |

## Completion Criteria

WP-001 to WP-010 pass their exit evidence, every frozen file is unmodified, and
each integration's final tree passes staged and full QA.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion                                             | Work package | Expected Task                                                     |
| ---------------------------------------------------------- | ------------ | ----------------------------------------------------------------- |
| [VAL-UAR-001](spec.md#success-criteria--verification-plan) | WP-003       | [tsk-0001](tasks/tsk-0001-propose-the-unit-retention-contract.md) |
| [VAL-UAR-002](spec.md#success-criteria--verification-plan) | WP-001       | [tsk-0001](tasks/tsk-0001-propose-the-unit-retention-contract.md) |
| [VAL-UAR-003](spec.md#success-criteria--verification-plan) | WP-002       | [tsk-0001](tasks/tsk-0001-propose-the-unit-retention-contract.md) |
| [VAL-UAR-004](spec.md#success-criteria--verification-plan) | WP-006       | [tsk-0002](tasks/tsk-0002-cut-over-registry-and-validators.md)    |
| [VAL-UAR-005](spec.md#success-criteria--verification-plan) | WP-008       | [tsk-0002](tasks/tsk-0002-cut-over-registry-and-validators.md)    |
| [VAL-UAR-006](spec.md#success-criteria--verification-plan) | WP-007       | [tsk-0002](tasks/tsk-0002-cut-over-registry-and-validators.md)    |
| [VAL-UAR-007](spec.md#success-criteria--verification-plan) | WP-008       | [tsk-0002](tasks/tsk-0002-cut-over-registry-and-validators.md)    |
| [VAL-UAR-008](spec.md#success-criteria--verification-plan) | WP-008       | [tsk-0002](tasks/tsk-0002-cut-over-registry-and-validators.md)    |
| [VAL-UAR-009](spec.md#success-criteria--verification-plan) | WP-009       | [tsk-0002](tasks/tsk-0002-cut-over-registry-and-validators.md)    |
| [VAL-UAR-010](spec.md#success-criteria--verification-plan) | WP-010       | [tsk-0003](tasks/tsk-0003-retain-adr-0038-and-close.md)           |
| [VAL-UAR-011](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-propose-the-unit-retention-contract.md) |
| [VAL-UAR-011](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0002](tasks/tsk-0002-cut-over-registry-and-validators.md) |
