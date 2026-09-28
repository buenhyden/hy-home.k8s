---
title: "Archive Lifecycle Standardization Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0100-PLAN-0001"
---

# Archive Lifecycle Standardization Implementation Plan

## Global Constraints

Inherit the [Spec](spec.md)'s non-destructive scope. The user approved changing current Spec/Plan/Task `done` to `completed` on 2026-09-28; migrate that spelling without changing terminal meaning or other states. The original implementation scope did not authorize accepting an ADR, removing or rewriting Archive material, accessing live systems or secrets, or pushing/merging; the later publication is recorded in the Task. Preserve unrelated work, exact frozen Git objects and the existing QA gates. Repository-static evidence never proves live behavior.

## Overview

Inspect and align the current implementation of [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md), repair reproduced defects, improve current documentation and record exact validation. The [Task](tasks/tsk-0001-standardize-archive-lifecycle.md) holds executed results; this Plan does not declare them in advance.

## Context

The original implementation baseline was `d2296de9ea66ea80c27fcc965c21d552febb057d` on a managed detached worktree; the Task records later publication. The baseline Registry families use `done`; the user has since approved `completed` as the same terminal meaning for current Spec/Plan/Task. ADR-0040's Archive disposition semantics stay intact. The Incident profile includes `closed`. Stage 90 research pack `0002-archive-retention-and-provenance` owns external-source evidence; SPEC-0099 owns workspace-engineering research, and SPEC-0095–0098 concern other retention/provider work.

## Goals & In-Scope

Recheck policy, profiles, schema, validators, tests, catalog and all relevant callers; fix an actual defect where its shared rule lives; migrate the approved current Spec/Plan/Task terminal spelling and historical compatibility; remove Incident form's duplicate state enumeration; reconcile stale current README and REQ/AD guidance with current ownership; add dated external-source findings to the existing research owner; execute bounded regression and final QA. Provide S01–S16 and V01–V40 disposition and evidence without inventing results.

## Non-Goals & Out-of-Scope

No new state meaning, Incident transition or conditional metadata field is approved by the spelling decision. No change to frozen bodies, sealed capture rows, archived SPEC-0054, secret material, cluster or service state, remote Git state, provider model settings or a second Archive registry. Completed units stay intact in the source stage until their own disposition approval.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Observe Git/index/history and classify existing policy, registry, caller and test contracts | None | Exact baseline and owner paths | Source map and actual mismatch disposition in Task |
| WP-002 | Reproduce and repair approved implementation defects through existing shared validators, including V27 ancestor loss | WP-001 | Focused failing case; target-reachable ancestor including merges, unrelated-branch exclusion and valid history-only removal | Regression PASS with unchanged safety gates |
| WP-003 | Update current form, policy explanation, current documents and navigation | WP-001 | Selected profiles and exact consumer paths | Reviewable scoped diff; owner and link checks |
| WP-004 | Integrate external evidence, then migrate approved current `completed` spelling and historical validation | WP-001 | User approval, exact current/historical instance and consumer inventory | Dated addendum, same transition semantics, preserved frozen bytes and focused migration checks |
| WP-005 | Run targeted, quick, exact-index if committed, full QA and independent review | WP-002, WP-003, WP-004 | Final scoped diff | Commands, counts, snapshots, failures and review in Task |
| WP-006 | Reconcile S/V bindings, residual risks and handoff | WP-005 | Evidence returned from each owner | Task records actual and deferred criteria; legal lifecycle state retained |

WP-002 and WP-003 may be independent after WP-001, with non-overlapping file ownership. The supervisor integrates evidence; a reviewer checks the final diff. The doc writer owns this package, Incident template, current REQ/AD/lifecycle wording and research addendum. Wiki curator owns READMEs. Tooling/quality owners own validator repair and QA.

## Verification Plan

First reproduce each claimed defect with the existing smallest relevant test or fixture. Run profile/template, link/owner, lifecycle, Archive cutover and changed validator checks over affected paths. Then run `python3 scripts/qa.py quick --root . --base-ref HEAD`; if committing is separately authorized, review the exact staged diff and run `python3 scripts/qa.py staged --root . --base-ref HEAD` plus actual-message validation. Run `python3 scripts/qa.py full --root . --base-ref HEAD` once on final working bytes. Check `git diff --check`, frozen-path diff, selected profile matches and Task evidence. Treat required unavailable tools, empty discovered target sets and failing required gates as FAIL or DEFER according to the quality policy; record exact result instead of assuming PASS.

## Risks & Mitigations

| Risk | Mitigation and owner |
| --- | --- |
| `completed` renaming accidentally changes terminal or retention meaning | Architect checks spelling-only mapping; validators prove current rejection of `done` and historical acceptance without changing disposition rules |
| Protected Archive source or catalog bytes change | Reviewer checks exact diff; quality engineer exercises existing immutable-object gates |
| Default-branch reachability cannot be proven in local history | Quality engineer records DEFER/FAIL and next operator; never treats a SHA string as proof |
| Current README hides a residual ownerless obligation | Wiki curator traces REQ/AD/Task owner before editing |
| Tool or full QA failure is reported as completion | Supervisor records each required lane and leaves package open |

Rollback is a reviewed forward correction of only this work's mutable current files. Frozen records remain untouched, so no restoration from a modified Archive body is planned.

## Completion Criteria

Every in-scope acceptance criterion has actual, snapshot-specific evidence; S01–S16 and V01–V40 have applied/deferred/not-applicable dispositions; independent review and required full QA have no unresolved failure. Otherwise the acceptance remains open with a named next owner. The published SPEC-0100 files retain their legal initial draft/draft/queued frontmatter until real lifecycle transitions are evidenced; publication alone neither promotes them nor approves Archive disposition.

## Traceability

One Task records all work packages and evidence, using the existing Spec package rather than a parallel ledger.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-ARC-001](spec.md#success-criteria--verification-plan) | WP-001, WP-002 | [Archive lifecycle Task](tasks/tsk-0001-standardize-archive-lifecycle.md) |
| [VAL-ARC-002](spec.md#success-criteria--verification-plan) | WP-003 | [Archive lifecycle Task](tasks/tsk-0001-standardize-archive-lifecycle.md) |
| [VAL-ARC-003](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-005 | [Archive lifecycle Task](tasks/tsk-0001-standardize-archive-lifecycle.md) |
| [VAL-ARC-004](spec.md#success-criteria--verification-plan) | WP-004, WP-006 | [Archive lifecycle Task](tasks/tsk-0001-standardize-archive-lifecycle.md) |
| [VAL-ARC-005](spec.md#success-criteria--verification-plan) | WP-005 | [Archive lifecycle Task](tasks/tsk-0001-standardize-archive-lifecycle.md) |
| [VAL-ARC-006](spec.md#success-criteria--verification-plan) | WP-004 | [Archive lifecycle Task](tasks/tsk-0001-standardize-archive-lifecycle.md) |
