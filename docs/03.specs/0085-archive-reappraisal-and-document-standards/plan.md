---
title: "Archive Reappraisal and Document Standards Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-17"
layer: "specs"
artifact_id: "SPEC-0085-PLAN-0001"
---

# Archive Reappraisal and Document Standards Implementation Plan

## Global Constraints

- No frozen body, sealed record, ledger, or existing catalog row changes.
- No real retained unit is reappraised or removed, and no `purged` value is
  written.
- One lifecycle state edge per document per integration; no intermediate state
  is claimed that did not happen.
- No gate, contract, or test pin is weakened to pass.
- Local logical commits are approved; push, pull request, and merge are not.
- No live cluster, Helm, Argo CD, Vault, secret, kubeconfig, network, or storage
  action.

## Overview

This Plan executes [SPEC-0085](spec.md). Its completion state is ADR-0040
accepted and cut over with regression evidence, current navigation matching the
tree, and the two vocabulary work packages ordered and gated on their own
decisions.

## Context

The survey at `980c5458` found no active owner for this work, three README
indexes that still describe ADR-0038 as current, a lifecycle gate with no
approved exit for a retained unit, no current judgment of retained evidence, and
envelope reachability checked from `HEAD` although ADR-0039 names the default
branch. All thirty-four catalog envelopes are reachable from both `main` and
`origin/main`, so the reachability change breaks no existing row.

The lifecycle vocabulary survey found collisions that rule out textual
replacement: `resolved` is today both a current Incident state and a retention
class, `retired` and `withdrawn` coexist in one family, `completed` is the
current audit state and a retention class, and pinned historical checks compare
the old spellings.

## Goals & In-Scope

- WP-001 through WP-004 in this round, as the request owner selected on
  2026-09-17.
- WP-005 and WP-006 ordered with entry gates, not executed.

## Non-Goals & Out-of-Scope

The dispositions of ADR-0039, SPEC-0054, SPEC-0062, and SPEC-0084; operator
evidence for SPEC-0072; and every item the Spec lists out of scope.

## Work Breakdown

| ID     | Work package                                                                                                                                                     | Depends on | Entry gate                                               | Exit evidence                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------- | ---------------------------------------------------------- |
| WP-001 | Survey, propose ADR-0040, create this package                                                                                                                    | None       | Request owner's 2026-09-17 scope selection               | Proposal Task; staged QA on the proposal commit            |
| WP-002 | Correct current navigation drift in the documentation indexes                                                                                                    | WP-001     | Survey findings                                          | Link gate; review of each index                            |
| WP-003 | Accept ADR-0040; supersede ADR-0039; amend REQ-0003-FR-0020; add the assessment contract, table, removal transition, and citation rule with RED then GREEN tests | WP-001     | Request owner approves the written ADR-0040              | Archive contract tests; lifecycle, link, and cutover gates |
| WP-004 | Default-branch reachability, object-format length, and shallow, type, mode, symlink, native-member, and empty-tree fixtures                                      | WP-003     | ADR-0040 accepted                                        | Git fixture tests; full QA                                 |
| WP-005 | Common lifecycle vocabulary                                                                                                                                      | WP-003     | Its own ADR accepted and a per-document mapping reviewed | Lifecycle gate over the mapping; historical alias tests    |
| WP-006 | Common validation result vocabulary                                                                                                                              | WP-003     | Quality policy change approved                           | Runner and summary tests                                   |

### WP-005 mapping rules

The mapping is decided per document from its recorded evidence, never by
spelling. Frozen bodies keep their states and are read through a read-only
historical alias; new writers produce only the new values.

| Profile family | Current value                             | Target                              | Evidence condition                                                                                    |
| -------------- | ----------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
| spec-plan      | `done`                                    | `completed`                         | Accepted closure recorded in its Task                                                                 |
| spec-plan      | `active`                                  | `in-progress` or `approved`         | `in-progress` only with recorded execution; a current contract such as SPEC-0008 needs its own review |
| spec-plan      | `withdrawn`                               | `retired`                           | No successor exists                                                                                   |
| task           | `queued`                                  | `draft` or `ready`                  | `ready` only with a recorded approval to start                                                        |
| task           | `done`                                    | `completed`                         | Recorded result                                                                                       |
| incident       | `open`, `mitigated`, `resolved`, `closed` | `detected`, `mitigated`, `resolved` | No Incident document exists; the registry, template, and retention binding change together            |
| audit          | `invalidated`                             | stays                               | An evidence-profile extension, never reduced to `cancelled`                                           |

### WP-006 mapping rules

`DEFER` becomes `BLOCKED` when a required authority, environment, or evidence is
missing and `NOT_RUN` when a check simply has not run yet. `N/A` needs a stated
reason. Evidence is recorded along scope (`targeted`, `affected`, `full`),
snapshot (`worktree`, `index`, `commit`), and place (`local`, `hosted-ci`,
`live`); the `quick`, `staged`, and `full` profile names stay as local adapters.
Past Task evidence keeps `DEFER`.

## Verification Plan

Each work package runs its focused tests first, then the quick profile on the
working tree, then the staged profile on the exact index of each logical commit.
One full profile runs on the final tree. Hosted CI and live evidence are not
produced in this round and are reported as not run.

## Risks & Mitigations

| Risk                                                                 | Mitigation                                                                                               | Owner         |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------- |
| The removal transition widens into a general immutability exemption  | Keep every unapproved-change regression and add one negative test per removal condition                  | platform      |
| Citation judges drift apart                                          | Change only `citation_decision` and the registry rule; both callers keep consuming it                    | platform      |
| Default-branch resolution differs between local and hosted checkouts | Resolve the remote tracking reference first and fail when none resolves; CI already fetches full history | platform      |
| A vocabulary change rewrites frozen evidence or breaks pinned checks | Gate WP-005 on its own decision with a read-only historical alias                                        | platform      |
| A Decision document is present but its approval is not real          | Record the mechanical limit and keep approval review with the request owner                              | request owner |

## Completion Criteria

WP-001 through WP-004 are complete with committed evidence, WP-005 and WP-006
are recorded with their entry gates, every criterion carries an observed result
or a named deferral, and the final full profile passes on the final tree.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package          | Expected Task                          |
| -------------- | --------------------- | -------------------------------------- |
| [VAL-ARS-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-propose-archive-reappraisal-and-document-standards.md) |
| [VAL-ARS-002](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-propose-archive-reappraisal-and-document-standards.md) |
| [VAL-ARS-003](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-propose-archive-reappraisal-and-document-standards.md) |
| [VAL-ARS-004](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0002](tasks/tsk-0002-cut-over-archive-reappraisal-and-verifiable-sources.md) |
| [VAL-ARS-005](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0002](tasks/tsk-0002-cut-over-archive-reappraisal-and-verifiable-sources.md) |
| [VAL-ARS-006](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0002](tasks/tsk-0002-cut-over-archive-reappraisal-and-verifiable-sources.md) |
| [VAL-ARS-007](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0002](tasks/tsk-0002-cut-over-archive-reappraisal-and-verifiable-sources.md) |
| [VAL-ARS-008](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0002](tasks/tsk-0002-cut-over-archive-reappraisal-and-verifiable-sources.md) |
| [VAL-ARS-009](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0002](tasks/tsk-0002-cut-over-archive-reappraisal-and-verifiable-sources.md) |
| [VAL-ARS-010](spec.md#success-criteria--verification-plan) | WP-005 | N/A — its Task is created when this work package is approved |
| [VAL-ARS-011](spec.md#success-criteria--verification-plan) | WP-006 | N/A — its Task is created when this work package is approved |
| [VAL-ARS-012](spec.md#success-criteria--verification-plan) | WP-001 through WP-004 | [tsk-0002](tasks/tsk-0002-cut-over-archive-reappraisal-and-verifiable-sources.md) |
