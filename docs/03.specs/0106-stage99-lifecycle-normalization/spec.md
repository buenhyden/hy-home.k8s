---
title: "Stage 99 Lifecycle Normalization"
version: "1.0.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106"
---

# Stage 99 Lifecycle Normalization Technical Specification (Spec)

## Overview

P02 makes the existing Stage 99 document contract describe lifecycle and
execution traceability consistently across its registry, forms, validators,
and current consumers. The request owner approved this local change plan;
source implementation and local finish are accepted from the observed Task
evidence. This completed document candidate still needs its separate closing
checks and read-only review. This package follows the
completed [P01 package](../0105-authority-and-safe-authoring/spec.md) and does
not reopen the historical SPEC-0104 package.

## Strategic Boundaries & Non-goals

Use the existing six-key governed frontmatter prefix and only the extensions
declared by each profile. Stage 99 remains the sole machine owner of profile,
identity, relationship, lifecycle, and form shape; common governance owns
meaning and authorization. Stable documents retain `artifact_id`; Plans and
Tasks declare one direct structural `parent_ids` value (Plan to Spec, Task to
Plan) without a duplicate `spec_id`. Review, approval and implementation are
distinct states; Task `ready` records readiness, not permission to act.

No new requirement, AD, ADR, progress ledger, native-provider
claim, or permanent inventory count is needed. Do not modify frozen archive
bodies, sealed records, historical contracts, private/global state, cluster,
secrets, or remote Git. The latest explicit user instruction authorizes local
P01/P02 integration into main and deletion of the two development branches and
any linked development worktrees after verified integration. Retain the primary
workspace. Push, PR, remote merge/publication, archive mutation and live action
remain outside scope; this instruction does not authenticate an approving actor.

## Contracts

- Requirements express durable needs; ADs express current structure; ADRs
  express durable choices; Specs express behavior; Plans express order; Tasks
  own execution state and evidence. The existing six-key prefix remains in its
  declared order for each governed Markdown profile.
- The [Plan form](../../99.templates/templates/specs/plan.template.md) has one
  work mapping under `## Work Breakdown` with columns `Work Unit | Criteria |
  Work | Dependencies | Task | Verification`. The [Task form](../../99.templates/templates/specs/task.template.md)
  has one Work/Lifecycle table under `## Task Table`, a
  `### Lifecycle Traceability` heading, and columns `ID | Upstream criterion |
  Work item | Owner | Status | Result | Acceptance | Evidence`. Its separate
  `## Task Evidence` attachment uses `Evidence | Criteria | Work Unit | Check |
  Input | Result | Location | Acceptance`; check outcomes do not copy Task
  execution state. The registry's optional `task_execution` binding owns the
  Task row semantics with `single_status_marker: frontmatter`,
  `summary_rule: task-items-v2`, `result_states`, and `acceptance_states`.
  Its secondary `evidence_section`, `evidence_columns` and
  `evidence_result_states` bind the existing attachment through the same
  parser; the four acceptance states are shared. A malformed attachment,
  invented result or accepted NOT_RUN fails without copying execution state.
- A Task frontmatter `status` is the single status marker. For a one-row Task,
  the row Status cell is literal `frontmatter`; the actual state comes only
  from the frontmatter marker. For a
  multi-row Task, the checker derives the expected frontmatter status from row
  statuses, then compares without rewriting. `blocked` dominates; otherwise
  any `in-progress` row or completed plus ready/draft work yields
  `in-progress`; remaining draft/ready rows retain an unfinished summary;
  all completed rows yield `completed`; all terminal rows with cancellation
  yield `cancelled`. Invalid row values or state/result/acceptance combinations
  fail. A cancelled row retains its actual observed result.
- Work results use `NOT_RUN`, `PASS`, `FAIL`, `DEFER`, and `NOT_APPLICABLE`;
  acceptance uses `pending`, `accepted`, `rejected`, and `not-required`.
  Completed required work needs PASS, accepted and concrete evidence. A
  completed explicitly nonrequired item may use NOT_APPLICABLE/not-required,
  but never satisfies a required Spec criterion. These do not replace QA lane
  results from [quality policy](../../../.agents/governance/quality.md).
- A read-only completion mode checks the Git index and requires one or more
  `--include-path` current Spec anchors. It follows each required Spec criterion
  through the Plan and Task to an assigned row with `Status: completed`,
  `Result: PASS`, `Acceptance: accepted`, and concrete evidence. A row with `Status: in-progress` and
  `Result: PASS` is still incomplete. Missing, failed, blocked, unexecuted, or
  required cancelled work cannot produce completion handoff.
  A completed Spec or Plan can receive follow-up Task evidence without
  reopening its stable approval state. A nonrequired cancellation cannot waive
  a required criterion; it can make a multi-row Task header `cancelled` while
  completed required rows remain eligible. Valid archived history remains
  distinguishable.
- Shared Markdown/link/lifecycle checks retain their independent failure
  meanings. Lifecycle checks compare Git snapshots and legal edges, including
  deletion, hiding, and reopening attempts. They do not edit documents.
- Route records retain `retired_route`, singular `successor` path or actual
  null, `reason`, `moved_scope`, and `current_owner` as applicable. Existing
  scalar/unique-array supersession forms remain admitted. Frozen `change_id`
  stays historical evidence, not new capacity.
- The Registry contains one bounded `migration_admission` for this approved
  generation-9 to generation-10 cutover. It identifies this Spec and Task,
  the actual 2026-10-05 migration date, and exact current path/profile/state
  entries. The checker admits an entry only for an actual generation-9 base
  and generation-10 proposal with both exact source and target observations.
  Classless source pack/native/router states are null; their observed
  frontmatter values stay historical facts. Missing references, unknown
  generations, unlisted paths, mismatched observations and terminal reopening
  fail. Ordinary generation-10 transitions and immutable history are unchanged.
  Spec/Task references locate the scoped record and do not authenticate approval.
- Current governed roles use the approved generation 10 state vocabulary.
  A cancelled document carries `cancellation` with reason, authorization
  reference and criterion disposition; the reference does not authenticate
  approval. A resolved Incident carries actual `resolved_at` and resolution
  evidence. Native Skills keep `name` and `description` while the common
  envelope lives in `metadata`. Navigation README routes use
  `common/readme` and the five shared core sections; research pack anchors
  retain stable `RES-####` IDs as authored reference packs. The archive index
  has its separate `archive/catalog` route and a current route record uses
  `archive/route` draft/sealed.

## Core Design

Extend the current registry and its two schemas only where a new declarative
binding is necessary, then update the existing Stage 99 forms and exact
validator consumers. Use the current parser, link resolver, and Git snapshot
flow. Keep the Task status consistency calculation in the lifecycle checker
and invoke the same parsing for completion mode. Current documents, including
this package, are normalized to the new contract in the implementation commit;
historical fixtures prove old frozen generations remain readable without
format rewrites.

## Data Modeling & Storage Strategy

`artifact_id` remains the stable identity for Spec, Plan, and Task, with
package membership derived from their canonical paths. Registry declarations
own optional Task body binding; Task rows carry execution status and evidence.
Git remains the source of historical transitions and rollback. Existing
Stage 99 inventory was observed in planning as 81 profiles, 37 physical forms,
and two schemas; these are a snapshot for coverage review, not invariants or
hard-coded targets. The actual implementation must inventory registry entries,
forms, and their consuming validators at its own reviewed snapshot.

## Interfaces & Data Structures

Keep current validator entry points and affected-path routing. The completion
invocation is `python3 scripts/validate-document-lifecycle.py --mode completion
--include-path docs/03.specs/0106-stage99-lifecycle-normalization/spec.md`.
Its output names the criterion, missing link or non-PASS Task result,
and checked snapshot; it never mutates the index or working tree. Existing
`scripts/validate-policy-gates.sh` consumes the fixed Conftest identity at
line 57; this work does not repin it.

## Edge Cases & Error Handling

Reject absent or duplicate Task Table headers, malformed rows, duplicate IDs,
unsupported statuses/results, contradictory frontmatter, ambiguous criterion
links, missing required Task evidence, and unknown completion targets. Preserve
historical accepted spellings only in their valid frozen generation; current
documents use current profile values. A legitimate nonrequired cancelled item
does not make required criteria pass by implication. An absent or inaccessible
Git comparison base is a failure or visible defer, never a synthetic PASS.

## Failure Modes & Fallback / Human Escalation

An implementation finding that changes document ownership, approval, or
historical meaning returns to the owning scope before that dependent edit.
Preserve existing evidence and apply reviewed forward changes for rollback;
never rewrite frozen bytes or branch history to make a gate pass. Unavailable
tools or native execution limits are recorded as such in the Task, with the
next owner named.

## Verification Commands

Demonstrate focused RED and GREEN cases for Task status aggregation and
completion refusal, including historical fixtures. Run the affected quick
profile, exact-index staged QA and actual commit-message validation for each
logical commit. The latest explicit user instruction removes full QA from the
required acceptance set and prohibits another full run or an all-files/unit
substitute. Preserve earlier interrupted full observations; an unexecuted full
check is NOT_RUN with acceptance not-required, never PASS. After closing
documentation, refresh affected/index/message and completion-mode evidence.
Independent read-only review checks the final meaning. At the intake snapshot,
P02 implementation full, unit, fixture and completion-mode checks had not run;
the Task owns all later execution observations.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-P02-001 | One atomic acceptance set: all six frontmatter/profile extensions and parent identity derivation; Task Table binding, exact heading/columns and status/result calculation; read-only index-target completion trace and refusal cases; shared Markdown/link/lifecycle Git-snapshot edges; route/supersession compatibility; current corpus normalization with frozen history intact; focused RED/GREEN negative and historical fixtures; affected, staged, message, closing-doc, completion and independent review evidence in the Task; local main integration and development-branch/worktree cleanup after observed checks. Full QA is excluded by the latest explicit user scope, with unexecuted checks NOT_RUN/not-required and prior observations preserved. |

## Traceability

The direct P02 request and approved implementation plan are the scoped input.
Relevant existing requirements are REQ-0003-FR-0005, FR-0006, FR-0012,
FR-0013, FR-0014, FR-0018, FR-0019, FR-0020 and FR-0027; this direct
package-local work does not change their reciprocal requirement map at intake.
Existing architecture is [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
[ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md),
and [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).
No new structural decision is required. [Plan](plan.md) owns order and
[Task](tasks/tsk-0001-lifecycle-normalization.md) owns execution evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — direct approved P02 package-local change; existing REQ-0003 meaning is unchanged | VAL-P02-001 | Registry/form/consumer, Task completion, route, historical and Git-edge checks |
