---
title: "Requirement Owner Crosswalk Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0154-PLAN-0001"
parent_ids: ["SPEC-0154"]
---

# Requirement Owner Crosswalk Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two execution constraints. First, no repository file changes outside this package, the Stage 03 README, and one back-link sentence in the Traceability section of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#traceability) that the cross-document validator requires, and `.secrets.baseline` entries that mark this Task's reviewed SHA-256 document digests as non-secret, following the reviewed-digest precedent of commit `f3dcab6d`. Second, the read-only reviewers and the supervising session write nothing to the repository; their working files stay in the session scratchpad.

## Overview

Produce and verify the [SPEC-0154](spec.md) requirement crosswalk: 109 package IDs mapped to current repository owners, observations, actions and next stage owners, with each conflict dispositioned. [Task 0001](tasks/tsk-0001-requirement-owner-crosswalk.md) owns the execution evidence, the crosswalk table and criterion acceptance.

## Context

Observed on 2026-11-11, before this draft:

- Workspace: the repository root checkout, branch `dev`, HEAD `b7497ee1f086870b7841b8b3f7c960fa5a40312e`, clean index and worktree, one worktree.
- `origin/main` and `origin/dev` both point at `b7497ee1`, matching the package's three remote observations. Local `main` is `f6c1c875`, 12 commits behind `origin/main`.
- PR #220 is merged with merge commit `b7497ee1`. It changed 26 files, all 5 checks passed, and it had no formal review. No PR is open.
- All six candidate paths the package names exist.
- Four read-only reviewers produced the crosswalk rows, and the supervising session ran the completeness check.

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrain the design. This plan changes no interface, migration or rollback surface beyond this package.

## Goals & In-Scope

- Record the baseline Git, PR and remote observations, together with the package input hashes.
- Record the full 109-row crosswalk, the completeness check and its negative fixture in the Task.
- Run an independent read-only semantic review of the crosswalk.
- Record the conflict dispositions and the handoffs of every non-PASS row to stages W01–W11.
- Add this package to the Stage 03 README and link it from REQ-0003 Traceability.

## Non-Goals & Out-of-Scope

- Implementing any GAP: each one belongs to its named stage owner and package.
- Changing `.agents/governance/git.md` for the `dev` branch decision. That belongs to W06.
- Restoring archive-wide checks, permanent catalogs or a progress ledger.
- Any commit, push, PR, merge, local `main` update, branch deletion, cluster access or secret read without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TRACE-001](spec.md#success-criteria--verification-plan), [VAL-TRACE-002](spec.md#success-criteria--verification-plan), [VAL-TRACE-003](spec.md#success-criteria--verification-plan) | Record the baseline and the 109-row crosswalk; check completeness; obtain the independent review; record conflict dispositions and handoffs. | Approved Spec and Plan; the package input files as hashed in the Task. | [Task 0001](tasks/tsk-0001-requirement-owner-crosswalk.md) | Completeness check with negative fixture, independent review, strict document checks. |

## Verification Plan

- Rerun the completeness check against the hashed inputs at the current HEAD, including the negative fixture.
- Have an independent reviewer that did not produce the rows sample-check owners and observations against the cited lines, covering every non-PASS row and the PARTIAL-read PASS rows.
- Run the strict document checks and `python3 scripts/validate-document-lifecycle.py --root . --mode staged`.
- Run `python3 scripts/qa.py staged` on the exact index before any authorized commit.
- Architecture compliance: confirm that no policy, ADR or AD file changed. Any such change returns the Spec to review.

## Risks & Mitigations

- **A reviewer misreads a row.** Mitigation: independent review, and any correction goes in a new evidence entry that keeps the original.
- **Relying on the package's ID scheme could turn its ledgers into a parallel authority.** Mitigation: the crosswalk maps package IDs to repository owners only. Repository contracts win every conflict.
- **Base drift.** If HEAD or the package inputs change, the affected rows are re-observed before acceptance.

## Completion Criteria

All three criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, and the operator's acceptance. Completion closes W00–W01 only. Each handed-off GAP stays open with its stage owner.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
