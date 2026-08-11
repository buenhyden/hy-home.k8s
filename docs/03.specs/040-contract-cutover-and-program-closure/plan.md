---
title: 'Contract Cutover and Program Closure Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-28
---

# Contract Cutover and Program Closure Implementation Plan

## Overview

This completed Plan executes [Spec 040](spec.md)
as the final PRD-006 repository-static tranche. It activated a reciprocal
[Task](tasks.md), removes
active compatibility-reader behavior, proves the final repository contract,
and closes PRD-006, AD-0009, ADR-0020, the Spec, Plan, Task, indexes, and
program relation in exact terminal closure commit
`c5adc27b13893d7cbd1266c9225372cfb7df79e9`. Deterministic precommit validation
passes, and independent terminal reviewers approved staged diff SHA-256
`e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888` with no
findings. Explicit-ref lifecycle from parent
`35d8552ba423e3e2d92294ddeb81674392b8f333` to the closure commit and
clean-tree repository-static aggregate passed. This evidence-update commit is
unidentified and unclaimed.

## Context

Spec 039 closed in commit `e1d1e910840337327a557ab4b84e86f8fced11d6`.
Its activation-to-closure
explicit-ref lifecycle and clean-tree repository-static postflight passed.
Commit `11a020d9b299ae91b7af9278c22ed89ffccb5cfc` records that observed result
without claiming its own identity in the earlier evidence proposal. Hosted run
`29982910320` remains a historical FAIL for its older SHA, while current
hosted, provider, and live evidence remains `DEFER`.

The active production gates already invoke strict document validation, but
the validator CLIs and current support/inventory prose still expose
compatibility-era behavior and wording. Finite fixtures that prove a closed
historical transition remain necessary regression evidence; they are not
active compatibility readers. The final cutover must preserve that distinction
and must not rewrite completed historical execution records merely to make
their terminology current.

This Plan, its Task, the Spec backlink, both Stage 04 indexes, and the shared
progress handoff formed the exact six-path activation package committed as
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`. No registry or
migration-ledger change belonged to activation. Explicit-ref lifecycle from
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` to that observed activation
commit and the clean-tree repository-static aggregate passed.

## Goals & In-Scope

- Activate the reciprocal Spec 040 Plan/Task pair and direct backlinks as one
  lifecycle-valid package.
- Make the active registry, Markdown-profile, and owner/link readers
  strict-only while retaining bounded historical-transition proof fixtures.
- Remove stale current compatibility and registry-version claims from active
  support, script, test, and audit surfaces.
- Produce a criterion-level closure matrix and update the Current audit with
  repository-static results, explicit limitations, owners, and rollback.
- Run focused, affected, strict, lifecycle, aggregate, all-files, and
  whole-branch review lanes.
- Close PRD-006, AD-0009, Spec 040, this Plan, its Task, and the final program
  relation atomically, then run explicit-ref and clean-tree postflight checks.

## Non-Goals & Out-of-Scope

- Rewriting immutable or completed historical evidence solely to replace
  accurate compatibility-era terminology.
- Removing finite archive-cutover, registry-version, or transition fixtures
  that fail closed and prove a bounded historical event.
- Implementing Specs 041-046, provider adapters, model routing, roster changes,
  shared provider memory, or `.github/ABOUT.md` renaming.
- Pushing, merging, dispatching GitHub Actions, modifying repository settings,
  publishing, installing dependencies, or mutating provider, Kubernetes,
  GitOps, Vault, ESO, Argo CD, cloud, credential, or secret state.
- Promoting a repository-static PASS to hosted, provider, remote, or live PASS.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| CCPC-000 | Activate reciprocal Spec 040 planning | Spec 039 closure and evidence update | Closure `e1d1e910…` and evidence update `11a020d9…` are observed | Intentional Plan-only `LIFECYCLE-CREATE` RED; exact six-path lifecycle GREEN; one observed logical activation commit; no registry or migration-ledger drift |
| CCPC-001 | Cut active document readers over to strict-only operation | CCPC-000 | Reciprocal Plan/Task pair is active | Tests prove strict default/no-mode PASS and retired compatibility invocation rejection; active current prose and retirement guard are consistent; finite historical proof fixtures remain bounded |
| CCPC-002 | Build the final closure matrix and Current audit overlay | CCPC-001 | Strict-only active reader contract is green | Every Spec 040 criterion and PRD-006 requirement has repository evidence, result class, owner, limitation, rollback, and final disposition; no unowned current finding remains |
| CCPC-003 | Run whole-branch QA and independent reviews | CCPC-002 | Closure matrix is complete and the proposal is stable | Focused, affected, strict, lifecycle, aggregate, all-files, formatter, and diff gates pass; independent requirements and quality/security reviews approve the exact proposal |
| CCPC-004 | Close the program lifecycle atomically and record postflight | CCPC-003 | Observed validator compatibility prerequisite commit `35d8552` is the closure parent | Exact 14-path terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` transitions PRD-006, AD-0009, ADR-0020, Spec/Plan/Task, six indexes, progress, and registry relation together; required precommit gates pass and final frontier is `0/0·6/3·3`; independent terminal reviewers approved staged diff SHA-256 `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888` with no findings; parent-to-closure explicit-ref lifecycle and clean-tree aggregate passed; this evidence-update commit remains unclaimed |

### CCPC-000 — Reciprocal activation

1. Preserve the settled migration ledger as a read-only input.
2. Prepare the Spec backlink, this Plan, its reciprocal Task, both Stage 04
   indexes, and shared progress entry as exactly six changed paths.
3. Stage the Plan alone and require exit `1` with `LIFECYCLE-CREATE`, Plan
   count `1`, and Task count `0`.
4. Stage exactly all six activation paths and require lifecycle, registry,
   strict document, link/owner, aggregate, and diff gates to pass.
5. Obtain independent requirements and quality review before creating one
   logical activation commit. Record its identity only after Git returns it.

### CCPC-001 — Strict-only active readers

1. Add or update focused tests first so no-mode validation exercises strict
   behavior and a compatibility-mode request fails at the CLI boundary.
2. Remove compatibility execution branches from current registry,
   Markdown-profile, and owner/link validators without weakening strict
   diagnostics.
3. Retain `template-compatibility.json` as the bounded no-growth retirement
   guard it already is; do not delete or rename that finite historical proof,
   and do not recreate the retired semantic-debt fixture.
4. Update current Stage 99 support, script inventory, test inventory, and
   Current audit wording to the current registry and strict-only contract.
5. Preserve private finite historical conversion/read fixtures only when they
   are pinned, fail closed outside the exact transition, and are not reachable
   as an active production fallback.

### CCPC-002 — Closure matrix and Current audit

1. Map VAL-CCPC-001 through VAL-CCPC-006 and every PRD-006 requirement to
   commands, result class, changed path or commit, reviewer, limitation,
   rollback, and follow-up owner.
2. Re-run archive integrity, historical-link, execution-disposition,
   reference, generated-output, workflow, selector, and residue checks.
3. Update the Current audit overlay with observed repository-static facts.
   Preserve current hosted/provider/live `DEFER` rows and their triggers.
4. Confirm every migration row has a terminal disposition and rollback
   reference without modifying the settled ledger during activation.

### CCPC-003 — Whole-branch QA and review

1. Run focused tests and all affected-surface validators for the cumulative
   branch diff.
2. Run lifecycle self-tests and staged validation, strict registry/profile/link
   validation, the repository aggregate, and `pre-commit run --all-files`.
3. Review formatter changes, rerun any mutated lane, and require both staged
   and unstaged diff checks to pass.
4. Give independent reviewers the exact proposal digest, merge-base range,
   criteria, limitations, and rollback chain. Remediate every blocking finding
   and obtain fresh verdicts.

### CCPC-004 — Atomic closure and postflight

1. Committed one terminal lifecycle closure that changes PRD-006 from `active`
   to `done`, AD-0009 from `active` to `accepted`, and Spec 040, this Plan,
   its Task, their indexes, and the final registry relation from `active` to
   `done`. Updated the accepted decision evidence required by the lifecycle
   contract in the same proposal.
2. Passed terminal lifecycle, strict document, residue, reference, aggregate,
   unqualified all-files, formatter, and diff gates for the exact staged
   proposal.
3. Recorded independent terminal review for staged diff SHA-256
   `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`:
   `/root/ccpc004_terminal_requirements_review` returned `REQUIREMENTS
   COMPLIANT`, `/root/ccpc004_terminal_quality_review` returned `QUALITY
   APPROVED`, and `/root/ccpc004_terminal_security_review` returned `SECURITY
   APPROVED`; all reported no findings.
4. Observed exact terminal closure commit
   `c5adc27b13893d7cbd1266c9225372cfb7df79e9` with parent
   `35d8552ba423e3e2d92294ddeb81674392b8f333`.
5. Recorded explicit-ref lifecycle and clean-tree repository-static aggregate
   PASS for the parent-to-closure interval. An initial over-wide
   activation-to-closure comparison
   `5c7bb820d9b424577eda3eb3a5c368f0c7cfc656..c5adc27b13893d7cbd1266c9225372cfb7df79e9`
   failed because it combined ADR/AD creation with terminal transition; the
   correct atomic terminal interval passed. Remote/live lanes remain `DEFER`
   until separately authorized and executed. This evidence-update commit is
   unidentified and unclaimed.

## Verification Plan

| Lane | Commands or method | Required result |
| --- | --- | --- |
| Focused strict cutover | Focused unit tests for the three active readers and retirement guard | No-mode strict behavior passes; compatibility invocation is rejected; finite pinned history remains fail closed |
| Lifecycle | `python3 scripts/validate-document-lifecycle.py --root . --self-test`; staged mode during proposals; explicit-ref mode after closure | Self-test, reciprocal activation, atomic closure, and observed-ref postflight pass |
| Registry and document contracts | `python3 scripts/validate-document-contract-registry.py --self-test`; strict registry, Markdown-profile, and owner/link commands | Zero uncovered/ambiguous routes, profile violations, duplicate current owners, or broken current links |
| Archive and migration | Archive integrity, historical-link, active-corpus residue, and final-disposition suites | Every governed archive and baseline execution record passes; settled evidence remains protected |
| Reference and generated surfaces | Reference IA, generated-output, workflow, and selector self-tests and production checks | Every current owned surface passes with stable ownership |
| Repository QA | `bash scripts/validate-repo-quality-gates.sh .`; `pre-commit run --all-files`; formatter/status review; `git diff --check`; `git diff --cached --check` | Aggregate final marker and every applicable hook pass; optional no-file lanes are explicit SKIP; no unreviewed formatter mutation |
| Independent review | Requirements and quality/security reviewers inspect the exact cumulative and terminal proposals | No unresolved Critical or Important finding |
| External evidence | Hosted CI, provider, remote, and live systems | `DEFER` unless separately authorized and observed; no inference from repository-static PASS |

## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| Removing a historical proof reader breaks the bounded transition regression | Separate active fallback behavior from pinned, private, fail-closed historical fixtures; test both boundaries before deletion | platform |
| Strict default changes silently alter diagnostics | Start with focused RED tests; preserve stable rule IDs and exit semantics; review exact output contracts | platform |
| Final status changes are split across commits | Use the lifecycle validator's complete-product, accept-architecture, complete-specification, and execution-pair predicates in one terminal proposal | platform |
| Closure prose overstates remote evidence | Keep local PASS, historical hosted FAIL, and current hosted/provider/live DEFER in separate result rows | platform |
| Completed historical bodies are rewritten | Limit currentness edits to active contracts, indexes, inventories, and Current audit surfaces; retain immutable historical evidence | platform |
| Formatter or generated output mutates the proposal after review | Reinspect status and diffs, rerun affected and all-files gates, and refresh reviews for the final digest | platform |
| Rollback would overwrite unrelated work | Revert newest logical units only; never reset, clean, or rewrite shared history | platform |

## Completion Criteria

- CCPC-000 through CCPC-004 each have an observed result and durable Task
  evidence.
- Active document readers have one strict contract; compatibility requests do
  not select a fallback path.
- Finite historical-transition fixtures remain only where pinned, bounded,
  private, and fail closed outside their exact event.
- VAL-CCPC-001 through VAL-CCPC-006 and every PRD-006 requirement have
  traceable repository-static evidence, review disposition, rollback, and
  honest limitation.
- The full branch passes focused, affected, lifecycle, strict document,
  archive, migration, reference, generated-output, workflow, aggregate,
  all-files, formatter, and diff gates.
- CCPC-003 independent requirements and quality/security reviews approve the
  whole-branch implementation; CCPC-004 independent terminal requirements,
  quality, and security reviews approve the exact staged terminal proposal
  without findings.
- PRD-006, AD-0009, ADR-0020, Spec 040, Plan, Task, indexes, progress, and the
  final registry relation transition atomically in exact 14-path closure commit
  `c5adc27b13893d7cbd1266c9225372cfb7df79e9`.
- Parent-to-closure explicit-ref lifecycle and clean-tree repository-static
  postflight are observed. This evidence-update commit itself remains
  unidentified and unclaimed. Current hosted, provider, remote, and live lanes
  remain `DEFER` unless separately authorized and observed.

## Traceability

- **Spec**: Contract Cutover and Program Closure Technical Specification
- **Task**: Contract Cutover and Program Closure Task
- **Program PRD**:
  [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **Program AD**:
  [AD-0009](../../02.architecture/descriptions/ad-0009-document-lifecycle-evidence-operating-model.md)
- **Decisions**:
  [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md),
  [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md),
  and
  [ADR-0020](../../02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md)
- **Predecessor evidence**: Spec 039 closure
  `e1d1e910840337327a557ab4b84e86f8fced11d6` and evidence update
  `11a020d9b299ae91b7af9278c22ed89ffccb5cfc`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CCPC-001](spec.md#success-criteria--verification-plan) | CCPC-001 | [Strict-only reader and bounded historical-proof evidence](tasks.md#task-table) |
| N/A — VAL-CCPC-002 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-001, CCPC-002 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-003 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-002 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-004 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-002 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-005 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-002, CCPC-003 | N/A — the paired Task is linked in VAL-CCPC-001 |
| N/A — VAL-CCPC-006 shares the Spec 040 source linked in VAL-CCPC-001 | CCPC-003, CCPC-004 | N/A — the paired Task is linked in VAL-CCPC-001 |
