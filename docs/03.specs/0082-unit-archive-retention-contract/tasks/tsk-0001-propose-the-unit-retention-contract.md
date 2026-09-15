---
title: "Propose the Unit Retention Contract"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0082-TSK-0001"
---

# Task: Propose the Unit Retention Contract

## Overview

This Task records the first integration: the survey of the Stage 98 contract,
the correction of stale current statements, the external evidence, and the
proposal of ADR-0039. It records observed results only and never promotes a
repository-static result to hosted, provider-runtime, or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Survey snapshot: branch `main` at `8a76bd3b05c5f34fa8f0cd0a46bf631098f79306`,
  equal to `origin/main`, clean, full history.
- Work branch: `docs/archive-disposition-contract-v2`.
- On 2026-09-15 the request owner chose full adoption of the common Archive
  target, exact-byte retention, the narrowed Incident exemption, identity
  tracking for internal moves, whole supersession of ADR-0038, three
  integrations, and logical commits on a work branch, and approved the three
  design sections. Accepting ADR-0039, retaining ADR-0038, push, pull request,
  and merge were not approved.

## Task Table

| ID       | Upstream criterion | Work item                                                                              | Owner    | Status | Result                                                  | Evidence                     |
| -------- | ------------------ | -------------------------------------------------------------------------------------- | -------- | ------ | ------------------------------------------------------- | ---------------------------- |
| WORK-001 | VAL-UAR-002        | Record the survey judgment and correct stale current statements                        | platform | Done   | Judgment below; eight statements in six files corrected | Commit `c07ee272`, staged QA |
| WORK-002 | VAL-UAR-003        | Record the external evidence as research pack 0002                                     | platform | Done   | Fourteen sources fetched, PREMIS unreachable            | Research pack 0002           |
| WORK-003 | VAL-UAR-001        | Propose ADR-0039 and this package, note the proposed successor, and update the indexes | platform | Done   | Proposed decision, package, and index rows              | Commit `cd3139e6`, staged QA   |
| WORK-004 | VAL-UAR-011        | Activate SPEC-0080 and SPEC-0081 for closure                                           | platform | Done   | Spec and Plan `active`, Task `in-progress`, index rows `Active`                                            | Lifecycle gate               |

## Approval and Safety Boundaries

- **Allowed Paths**: the proposal scope named in the [Spec](../spec.md).
- **Forbidden Paths**: frozen records, ledgers, and retained packages under
  `docs/98.archive/`, the manifest comment and frozen record table of
  `docs/98.archive/README.md`, the sixteen ADR-0038 retained bodies,
  `docs/99.templates/registry.json`, `gitops/`, `infrastructure/`, `policy/`,
  `secrets/`, `.github/`.
- **Approval Required**: logical commits on the work branch are approved. Push,
  pull request, merge, accepting ADR-0039, and any disposition are not.
- **Static Validation**: `git diff --check`, `git diff --cached --check`, and
  `python3 scripts/qa.py staged` per logical commit, and one
  `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action other than fetching public documentation is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Revert the proposal commits before integration.
- **Evidence Location**: This Task record.

### Survey judgment

Consistency values: consistent, stale statement, policy–implementation gap,
policy conflict, ambiguous, not applicable. Confidence values: source read,
static code read, test reproduced, command observed. The survey used three
read-only delegated searches; each claim used below was re-read in source. One
delegated claim was corrected: the archive validator checks only `active` and
`accepted` documents, so it never evaluates an Incident, and the two citation
checks differ in scope rather than contradicting each other on Incidents.

| Item | Topic                     | Observed at `8a76bd3b`                                                                                                                                                                                                                                                                   | Consistency                  | Confidence       | Disposition                                                                  |
| ---- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ---------------- | ---------------------------------------------------------------------------- |
| A01  | Authority                 | Policy, ADR-0038, and the Stage 98 index each restate the six dispositions; the responsibilities router called Stage 98 a minimal recovery index                                                                                                                                         | Policy conflict              | Source read      | Router corrected in `c07ee272`; meaning moves to the registry in the cutover |
| A02  | Six dispositions          | `completed/`, `superseded/`, `migrations/` hold content; `retired/`, `resolved/`, `tombstones/` are unused and have no directory                                                                                                                                                         | Consistent                   | Command observed | Kept                                                                         |
| A03  | Retention modes           | Git-history-only is named in policy and bound to no profile                                                                                                                                                                                                                              | Policy–implementation gap    | Static code read | ADR-0039 binds modes; cutover                                                |
| A04  | Stage boundary            | Stage 99 forms are said to retire by Git-history-only disposition, in prose only                                                                                                                                                                                                         | Policy–implementation gap    | Source read      | ADR-0039 binds it to Stage 99 forms; cutover                                 |
| A05  | Paths and first use       | Registry path patterns carry mirrored alternatives; directories appear on first use                                                                                                                                                                                                      | Consistent                   | Static code read | Kept; first-use fixtures in the cutover                                      |
| A06  | Unit membership           | No check compares a package's members with the base; only a resolved Incident needs its Postmortem to exist                                                                                                                                                                              | Policy–implementation gap    | Static code read | ADR-0039 units and tree envelopes; cutover                                   |
| A07  | State and class           | `cancelled` is admitted by `completed` and `retired`, judged per document                                                                                                                                                                                                                | Ambiguous                    | Static code read | Anchor-state admission; cutover                                              |
| A08  | Completion and approval   | SPEC-0080 and SPEC-0081 stay `draft` and `queued` with finished work, by the one-edge rule                                                                                                                                                                                               | Transition incomplete        | Source read      | WORK-004 activates; the cutover closes                                       |
| A09  | Promotion receipt         | What a completed body promoted is a review obligation, not a validated field                                                                                                                                                                                                             | Consistent                   | Source read      | Kept as a review obligation                                                  |
| A10  | Atomicity                 | The lifecycle gate compares a pull request with its merge base, so one document takes one edge per integration                                                                                                                                                                           | Consistent                   | Static code read | Three integrations                                                           |
| A11  | Closure evidence          | A superseded body needs `superseded_by`; Incident closure is checked only by sibling existence                                                                                                                                                                                           | Policy–implementation gap    | Static code read | Anchor state `closed` with `published`; cutover                              |
| A12  | Catalog                   | Sixteen rows, one per file; parity requires one row per current-generation file                                                                                                                                                                                                          | Consistent                   | Command observed | Unit rows; cutover                                                           |
| A13  | Git provenance            | The envelope check proves ancestry and object ID equality, not object type or mode; rows are not re-verified                                                                                                                                                                             | Policy–implementation gap    | Static code read | Envelope object checks and full-lane re-verification; cutover                |
| A14  | Freeze and transformation | Retained bodies compare after link rebasing by a regex that is not fence-aware; the index said payload links are never recomputed without naming the generation                                                                                                                          | Stale statement and gap      | Static code read | Index qualified in `c07ee272`; exact retention in the cutover                |
| A15  | Frozen generations        | Twenty-five sealed records and twenty-three ledgers route by exact path; the legacy registry fixture passes                                                                                                                                                                              | Consistent                   | Test reproduced  | Kept; the sixteen rebased bodies become a finite legacy set                  |
| A16  | Target citability         | `CITABLE_NAMINGS` stipulates citable namings while the policy calls it derived                                                                                                                                                                                                           | Policy conflict              | Static code read | Registry citation table; cutover                                             |
| A17  | Source exceptions         | The link gate exempts Incident and Postmortem sources for every archive path; the enumerated consumers exist only in Task prose                                                                                                                                                          | Policy conflict              | Static code read | Narrowed exemption, no consumer exception; cutover                           |
| A18  | Link syntax               | The link gate parses inline and reference links, decodes `%20`, strips query and fragment, masks code spans; the rebasing parser is separate                                                                                                                                             | Consistent for the link gate | Static code read | Rebasing parser retires with exact retention                                 |
| A19  | Link integrity            | Outgoing links of retained bodies are skipped, and the skip comment still named migration rows                                                                                                                                                                                           | Stale statement              | Source read      | Comment corrected in `c07ee272`; snapshot reading in the cutover             |
| A20  | Forms and identifiers     | `TOMB-####` and `MIG-####` route forms exist with templates                                                                                                                                                                                                                              | Consistent                   | Source read      | Kept                                                                         |
| A21  | Enforcement lanes         | Archive unit tests run only in full and ci; staged runs the lifecycle and link gates                                                                                                                                                                                                     | Consistent                   | Static code read | Fast archive gate in the cutover                                             |
| A22  | Publishing and search     | No documentation site or search build exists; the knowledge map does not route the archive                                                                                                                                                                                               | Not applicable               | Source read      | None                                                                         |
| A23  | Security and routes       | A route envelope rejects `:`, so a public URL route cannot be recorded; secret handling is a separate process                                                                                                                                                                            | Policy–implementation gap    | Static code read | ADR-0039 limits routes to repository paths                                   |
| A24  | Stale facts and counts    | Stale statements in the Stage 98, Stage 02, and Stage 01 indexes, the responsibilities router, AD-0006, and one validator comment. Counts at `8a76bd3b`: 376 files in 52 packages under `completed/`, 41 files under `superseded/` (25 sealed, 16 retained), 23 ledgers, 16 catalog rows | Stale statement              | Command observed | Corrected in `c07ee272`; dated Task and ADR history kept                     |
| A25  | Integration               | SPEC-0079 is done but still cited, so it is not retained; SPEC-0080 and SPEC-0081 await closure                                                                                                                                                                                          | Consistent                   | Source read      | Not retained; WORK-004 and the cutover close them                            |

## Verification Summary

Baseline at `8a76bd3b`: `python3 -m unittest` over ten archive and link test
modules ran 293 tests, `OK`, in 351 seconds. The three fast modules ran 23, 14,
and 25 tests, `OK`, each in under two seconds.

Commit `c07ee272`: `git diff --check` and `git diff --cached --check` returned 0. `python3 scripts/qa.py staged` passed 12 of 12 gates over the exact index of
six paths, exit 0, and the commit hooks passed, including commitizen.

An editor formatter rewrote whole documents after each edit, including
regions of `docs/98.archive/README.md` outside the intended sentences. Each
corrected file was rebuilt from its base bytes with only the intended
replacements, and the committed diff is twenty insertions and nineteen
deletions. Research source PREMIS returned HTTP 403 on two official URLs and is
recorded as unreachable with no claim.

Commit `cd3139e6`: the first `python3 scripts/qa.py staged` run failed one
gate of six. `links-and-owners` reported `BODY-LINK-SOURCE` because the
proposed ADR-0039 named ADR-0038 in `Decision lineage` without a repository
link, which the body contract enforces for a proposed decision; the cell now
links ADR-0038, as the ADR-0038 proposal linked ADR-0032. The rerun passed 6 of
6. The commit hook then rejected two MD033 findings in research member
`m0001`, where a quoted `<object>` read as inline HTML; the placeholder is now
code. The rerun over the changed index passed 6 of 6, and the commit hooks
passed. No gate or contract was weakened.

The activation commit moves SPEC-0080 and SPEC-0081 one edge each: Spec and
Plan `draft` to `active`, Task `queued` to `in-progress`. Their closure is the
cutover integration's first work item.

Commit `97a2101b`: staged QA passed 6 of 6 and the commit hooks passed.
`python3 scripts/qa.py ci --base-ref 8a76bd3b05c5f34fa8f0cd0a46bf631098f79306`
then ran the full gate set once on that clean tree, comparing lifecycle state
with the merge base as a pull request would: 22 of 22 gates `PASS`, exit 0, in
491 seconds. That is local evidence, not a hosted CI result.

Review: one independent read-only review of the three commits confirmed the
unchanged frozen bytes, the survey claims against the code at `8a76bd3b`, the
counts, and the corrections. It reported one MEDIUM finding: WORK-004 and the
cutover's closure item cited criteria that do not cover package activation or
closure, and the Plan mapped no criterion to WP-004. Criterion VAL-UAR-011 now
covers both, and the Plan and both Tasks cite it. Its LOW observation, this
Task staying `queued` with finished items, is intended: a document created in
an integration keeps its creation state until the next one, as SPEC-0078
recorded. The final tree after this repair runs the ci profile once more and
is recorded in the handoff rather than here.

Hosted CI, provider runtime, and live evidence were not observed.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item                 | Result        | Evidence                         |
| ------------------------------------- | ------------- | -------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done.         | Commit `c07ee272` and staged QA. |
| [WORK-002](../plan.md#work-breakdown) | Done.         | Research pack 0002.              |
| [WORK-003](../plan.md#work-breakdown) | Done.         | Commit `cd3139e6` and staged QA.   |
| [WORK-004](../plan.md#work-breakdown) | Done. | Activation commit and staged QA.                  |
