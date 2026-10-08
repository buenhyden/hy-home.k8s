---
title: "Stage 99 Lifecycle Normalization"
version: "1.13.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0106"
---

# Stage 99 Lifecycle Normalization Technical Specification (Spec)

## Overview

P02 makes the existing Stage 99 document contract describe lifecycle and
execution traceability consistently across its registry, forms, validators,
and current consumers. The request owner approved this local change plan;
source implementation and local finish are accepted from the observed Task
evidence. The later P01 follow-up rechecked the historical closing candidate
and the current P02 index; EVD-P02-014 records staged, completion and
independent review acceptance while preserving EVD-P02-013 as the original
unrun result. This package follows the
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

The following exclusions describe original WORK-001 and its local finish.
No new requirement, AD, ADR, progress ledger, native-provider
claim, or permanent inventory count is needed. Do not modify frozen archive
bodies, sealed records, historical contracts, private/global state, cluster,
or secrets. The original WORK-001 did not change remote Git. The earlier P02
finish instruction authorized local
P01/P02 integration into main and removal of their development branches after
verified integration; the original Task records that observed finish. The
current `VAL-P02-002` follow-up retains the P01 worktree and its own feature
worktree during implementation. The request owner's later instruction
authorizes work-unit commits, push and merge after required review and hosted
checks. Worktree removal, archive mutation and live action remain outside this
scope. This authorization does not claim current remote state or an
authenticated operator action.

## Contracts

### Current shared-profile migration

VAL-P02-016 implements the current user's P02 request from actual main
`c9faa9f00fdf61c9286b4dc6df264de35106b611`. Use the one P01
WGOV-CORE/3.0.0-draft.3 review candidate, with its corrected first-establishment
route, as the common input for C02/C03/C04/C05/C12. The Registry identifies
this candidate and local adapter; absent common-source commit and final
approval remain null, not invented prerequisites or approval evidence.
Final edition approval, local adoption and four-repository adoption remain
distinct decisions owned by buenhyden. The current request authorizes local
policy, consumer, form and document changes and normal commits, without
extending earlier exact P01 server or cleanup authorization.

Migrate Guide, Policy and Runbook to that candidate's six role sections,
preserving native operating modules, identity, active state, owner, actual
approval and evidence. Move their existing Lifecycle Traceability relationship
table to Related Documents with the same columns and cardinality. Require
substantive section bodies for these current roles: nested headings, comments,
empty fences and placeholder-only content cannot satisfy a role. Templates
retain author prompts and the created document's initial draft state; their
support and revision belong to the Registry and Git. Frozen history keeps its
observed generation and bytes.

Retain the existing six-key grammar, role-specific extensions, native
envelopes and router/reference-anchor distinction. Single-row Task execution
is authored only in frontmatter; multi-row execution is authored only in rows,
with the existing explicit writer generating the required frontmatter summary.
Do not hand-maintain a second status. Existing role states and local language
rules remain the migration adapter pending P03's shared state/provenance and
language decisions; no new local enum or status reset is introduced.

Review each current operating document separately for profile, form, content,
owner, references, state and actual evidence, and hand unresolved product/live
verification to P08. Local checks are selected from changed inputs plus
synthetic failure/boundary regressions, exact-index lint/format, actual message
checks and independent review. Full, live and hosted execution are not claimed
by this migration.

Document-reader implementation and its focused fixtures select document gates,
not unrelated Archive or Kubernetes corpus execution. Give the central route
Registry its own static routing/quality checks. Preserve other implementation
routes and add the actual product gates when product paths also change.

### User-directed hosted QA removal

VAL-P02-015 applies the latest explicit request to remove failing GitHub QA
execution, integrate the local result and reflect it to origin/main without
waiting for remote QA. Earlier work-unit hosted requirements describe their
historical delivery contracts; this follow-up records the changed CI contract.
Keep only branch-policy, qa-isolated and ci-summary in the CI workflow. Its
summary inspects only the surviving event-appropriate results and explicitly
reports full QA NOT_RUN. Remove qa/qa-source and their full QA invocations; the observed historical
qa step took 25m08s and also satisfies the later actual-duration removal criterion.
A configured timeout is not an observed duration. Make provenance verification explicitly inactive while retaining its strict
Python proof validation and dependent publisher gating. No absent full report
may become signed provenance or a QA PASS.

Repair only directly obsolete topology consumers and current delivery guidance.
Preserve remaining pin, permission, bootstrap, isolated validation, shell and
provenance refusal controls, the local validation registry and passing production
regressions. Four normal Task states and actual-index checks precede local
integration. Local full/affected execution remains NOT_RUN; any remote rejection
is an observed delivery limitation, not authority to force or rewrite history.
The latest explicit finish instruction permits removal of the four named owned
development refs and three development worktrees only after local/origin-main
integration is observed, commits are main-reachable, clean state is checked and
known structured evidence has been preserved with hash audit. Exact targets and
owners belong in Task0015; unrelated or private data is not deletion scope.

### Hosted compatibility follow-up

The request owner's later work-unit push and merge instruction also authorizes
the bounded VAL-P02-003 compatibility repair needed by the observed PR gates.
It preserves the current production Registry, schemas, validator semantics,
frozen archive bytes and historical Task evidence. Current public migration
proof fixtures compile the actual published generation-10 Registry and its
current schema/templates, with bounded synthetic migration routes declared only
inside their temporary fixture Registry. Independent historical asset tests
use the same immutable generation as the frozen Registry; missing objects fail
rather than substituting current bytes. Required hosted
checks gate the exact PR head before normal merge; integrated main is checked
after merge before integration acceptance. Local full and affected execution
remain excluded for this follow-up. No live, credential, native trust,
cleanup, force push or history rewrite is authorized.

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

### Follow-up: explicit multi-row Task summary

`VAL-P02-002` closes the manual copy of a multi-row Task's derived status.
Extract the existing `task-items-v1`/`task-items-v2` aggregation into one pure
helper shared by the read-only checker and a separate authoring command.
The command `python3 scripts/sync-task-status.py --root <repository>
--path <task>` previews
the current and derived status; `--write` opts in to changing only the top-level
frontmatter `status` scalar. A one-row Task continues to use literal
`frontmatter` in its Status cell and is never rewritten by this command.

The command accepts only current, regular repository files classified exactly
as `sdlc/task`. It reuses the Registry loader and the existing comment/fence-aware
Task parser, validates the candidate with the current strict contract, and
rejects malformed rows, results, acceptance, evidence, or an illegal current
to candidate lifecycle edge before writing. It preserves all other bytes and
file permissions, detects a changed source before replacement, and preserves
the original on a failed replacement. Invalid inputs and writes have stable
diagnostic IDs and exit 2; successful preview, change, and no-op exit 0.
Neither validator nor Git hook invokes this opt-in writer.
The follow-up Task's `completed` state denotes observed local source acceptance;
PR and merged-SHA integration remain separate until their hosted results are
observed.

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
original P02 logical commit. Its finish instruction removed full QA from the
required acceptance set and prohibited another full run or an all-files/unit
substitute. Preserve earlier interrupted full observations; an unexecuted full
check is NOT_RUN with acceptance not-required, never PASS. The current P01
follow-up selected affected gates without executing that lane; it rechecked
the historical P02 candidate and a later changed closing index separately.
EVD-P02-014 records the observed checks and their input revision.
Independent read-only review checks the final meaning. At the intake snapshot,
P02 implementation full, unit, fixture and completion-mode checks had not run;
the Task owns all later execution observations.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-P02-016 | One identified common candidate and truthful adoption tuple; Registry/schema/forms/readers agree on the three six-section operating roles, with substantive-content refusals and preserved relationships. All current Guide/Policy/Runbook instances are migrated and individually reviewed while state, identity, native boundaries and frozen bytes are preserved. Single Task status and generated multi-row summary have one authoring source; existing README router/anchor and native/language contracts retain their current consumers. Task0016 records focused RED/GREEN, exact-index lint/format/message, independent review, P03/P08 handoffs and actual unexecuted boundaries; final common approval and four-repository adoption are reported separately. |
| VAL-P02-015 | The hosted CI topology contains only branch-policy, qa-isolated and ci-summary; full QA is explicitly NOT_RUN, removed execution is not QA PASS, and missing full proof cannot create provenance. Direct topology/guide consumers match the new contract while isolated validation, pin/permission/bootstrap/shell and provenance refusal controls remain. Registered-form creation, scoped RED/GREEN, exact-index staged/message, completion and independent review are recorded in Task0015. Preserve local validation registration, production regressions, original evidence and normal local/main delivery history. |
| VAL-P02-014 | Generation-admission fixtures read authentic immutable generation-9 and generation-10 boundary documents together, preserving absent-source, same-generation, invalid declaration, terminal reopening, later completion, cumulative replay and fixed budget refusals. Whitespace fixture expectations use the existing typed Registry-bound retention classification alongside frozen lifecycle states, retaining current-record and nonarchive negatives. Three observed named REDs, all four shared generation methods and one whitespace method, registered-form provenance, hook-first final bytes, each actual-index staged/message, scoped completion and independent review are recorded in Task0014. Production contracts, schemas, Registry, hooks, limits and retained archive bytes remain unchanged; hosted and integrated-main admission are separate. |
| VAL-P02-013 | Reference pack route fixtures expect the current authored reference pack identities and their unchanged registered templates. Existing numbered member routes, uncovered loose/date paths and topology/drift refusals remain required. Two named REDs, final-byte focused controls, scoped hooks, registered-form creation metadata, each actual-index staged/message, completion and independent review are recorded in Task0013. Published Registry, templates, reference corpus and production contracts remain unchanged; hosted acceptance is separate. |
| VAL-P02-012 | Synthetic QA and reference navigation fixtures use the current report envelope, pack profile and collection section. Typed synthetic non-Git results preserve all four full/CI orchestration scenarios, complete gate counts, deliberate failure, platform parsing and no local evidence reuse; actual temporary Git remains bounded. Collection depth and missing-member/valid controls remain required. Named RED/GREEN, scoped hooks, registered-form creation metadata, each actual-index staged/message, completion and independent review are recorded in Task0012; production contracts and hosted acceptance remain separate. |
| VAL-P02-011 | Authority lifecycle fixtures use the current Spec maintenance/supersession states and the audit's own publication vocabulary. Draft/current/terminal body maintenance, invalid reference states, noninitial publication creation and missing/exact reciprocal evidence remain discriminating controls. Three named RED/GREEN methods, scoped hooks, registered-form creation metadata, each actual-index staged/message, completion and independent review are recorded in Task0011. Production contracts and completed evidence remain unchanged; hosted acceptance is separate. |
| VAL-P02-010 | Completed-state and navigation fixtures follow the current published predecessor and domainless collection route. Historical replay uses a faithful declared generation and preserves current-invalid done, terminal, no-reopen and direct-create refusals. Named RED/GREEN and related controls, scoped hooks, registered-form creation metadata, each actual-index staged/message, completion and independent review are recorded in Task0010. Production contracts and completed evidence remain unchanged; hosted acceptance is separate. |
| VAL-P02-009 | A new unique Task draft originates from the unchanged registered Task form, with actual first-appearance metadata observed before commit. The common authority fixture follows its published six-state governance domain and native metadata envelope while preserving every routing and invocation-control refusal. Retained Task8 observations are historical after the separate reviewed forward rollback. Named fixture evidence, scoped hooks, each actual-index staged/message, completion and independent review remain required; production contracts and hosted acceptance stay separate. |
| VAL-P02-007 | Governance and Spec navigation fixtures follow the actual published current-state and section declarations while preserving owner membership and malformed navigation refusals. The archive Git-process budget retains its measured fixed-cost corpus meaning; any correction requires immutable causal accounting and preserves batching and the sixty-second bound. Named failures, changed-input controls, scoped hooks, each actual-index staged/message, completion and independent review are recorded in Task0007. Production contracts and completed evidence remain unchanged; hosted acceptance remains separate. |
| VAL-P02-006 | The additive sealed-disposition recovery fixture records the exact frozen generation-9 Registry, original source and immediate successor together at the authenticated source revision. Existing missing-proof, wrong-disposition, source-identity, terminal-edge and cutover refusals remain required. Observed named RED, all 21 shared recovery-fixture methods, scoped hooks, each actual-index staged/message, terminal completion and independent review are recorded in Task0006. Production validators, published Registry/schema, frozen Archive and completed evidence remain unchanged; hosted and integrated-main acceptance are separate. |
| VAL-P02-005 | Current artifact identity, authority lifecycle and migration fixtures consume the actual published generation-10 profile/domain declarations. Restore Task0004's new all-mode first-appearance metadata eligibility to trusted sdlc/task targets only, preserving prior ordinary-copy eligibility and refusal order for other profiles. Existing wrong-ID, illegal-edge, trusted-policy-before-pattern, default/schema-null and migration provenance refusals remain required. Observed failures, changed-input named GREEN and related controls, scoped hooks, each actual-index staged/message, terminal completion and independent code/security review are recorded in Task0005. Other production behavior, schemas, Registry and completed evidence remain unchanged; hosted PR and integrated-main results are separate. |
| VAL-P02-004 | A copied first draft of a new canonical, unique `sdlc/task` may originate only from its current and historically registered Task template, present as the same regular source blob before and after creation. Template binding changes, nonregular or changed sources, ID reuse, wrong initial state, ordinary copy/rename and invalid later edges remain refused. Focused real-Git RED/GREEN and negative regressions, exact-index staged/message, terminal completion and independent review are recorded in Task0004. Public schema, Registry generation, other provenance guards and hosted requirements are unchanged. |
| VAL-P02-003 | Current migration-proof fixtures use the complete actual generation-10 Registry/schema/template graph and test-only synthetic routes without bypassing compilation or proof checks. Cumulative-history fixtures use required current headers and explicit review transitions while retaining illegal-transition and provenance refusals. Independent historical asset tests prove exact immutable bytes and missing-object refusal. Scoped formatting and verified Git-identity annotations, focused RED/GREEN, staged/message, completion and independent review are recorded in the new Task. Hosted PR and integrated-main checks remain separate from local acceptance. |
| VAL-P02-001 | One atomic acceptance set: all six frontmatter/profile extensions and parent identity derivation; Task Table binding, exact heading/columns and status/result calculation; read-only index-target completion trace and refusal cases; shared Markdown/link/lifecycle Git-snapshot edges; route/supersession compatibility; current corpus normalization with frozen history intact; focused RED/GREEN negative and historical fixtures; affected, staged, message, closing-doc, completion and independent review evidence in the Task; local main integration and development-branch/worktree cleanup after observed checks. Full QA is excluded by the latest explicit user scope, with unexecuted checks NOT_RUN/not-required and prior observations preserved. |
| VAL-P02-002 | The existing Task summary rules have one shared implementation. An explicit command previews and optionally synchronizes only the frontmatter status of a valid multi-row current Task, preserves the one-row marker and every other byte, refuses unsafe paths, invalid content and illegal transitions without partial writes, and keeps validation read-only. Focused RED/GREEN, exact-index staged and message checks, completion and independent review are recorded in the follow-up Task. Local full and affected execution are excluded for this follow-up only; required hosted checks govern authorized PR and merge. |

## Traceability

VAL-P02-016 maps to WORK-016 and
[Task0016](tasks/tsk-0016-shared-profile-migration.md) in the current Plan.
This follow-up preserves the completed parents and all prior evidence.

VAL-P02-015 maps to WORK-015 in the [Plan](plan.md) and
[Task0015](tasks/tsk-0015-hosted-qa-cleanup.md). The explicit latest user request
changes hosted execution and its direct consumers; it does not falsify previous
observations or authorize a provenance PASS without full proof.

VAL-P02-014 maps to WORK-014 in the [Plan](plan.md) and
[Task0014](tasks/tsk-0014-generation-boundary-and-retention-fixtures.md).
The three bounded REDs expose current-body substitution at a historical
boundary and a status-only frozen oracle. Later admission and replay controls
were not reached; thirty local whitespace subcase failures are not an
exhaustive hosted failure count. Available structured/public-source review
passed; private raw direct audit remains NOT_OBSERVED/DEFER after automatic
approval rejection.

VAL-P02-013 maps to WORK-013 in the [Plan](plan.md) and
[Task0013](tasks/tsk-0013-reference-pack-route-fixtures.md).
The capped hosted preview and two bounded REDs identify obsolete expected pack
profiles; unreached template and corpus checks remain unobserved in that RED.

VAL-P02-012 maps to WORK-012 in the [Plan](plan.md) and
[Task0012](tasks/tsk-0012-qa-and-reference-navigation-fixtures.md).
The capped hosted preview and three bounded REDs establish fixture prerequisites;
the synthetic RED did not capture internal output or reach later CI subcases.

VAL-P02-011 maps to WORK-011 in the [Plan](plan.md) and
[Task0011](tasks/tsk-0011-authority-lifecycle-state-fixtures.md).
The executed hosted preview exposed three new fixture prerequisites; the entire
implicated class was reviewed without treating that preview as an exhaustive inventory.

VAL-P02-010 maps to WORK-010 in the [Plan](plan.md) and
[Task0010](tasks/tsk-0010-completed-state-and-navigation-fixtures.md).
It addresses named failures from the executed hosted complement; its sanitized
failure excerpt is not an exhaustive unit-test inventory.

VAL-P02-009 maps to WORK-009 in the [Plan](plan.md) and
[Task0009](tasks/tsk-0009-common-authority-fixture-reinstantiation.md).
It follows the separate reviewed Task8 rollback, retaining all original
commits and external observations without reusing its withdrawn identity.

The current-owner fixture follow-up maps VAL-P02-007 to WORK-007 in the
[Plan](plan.md) and
[Task0007](tasks/tsk-0007-current-owner-fixture-conformance.md).
Its process-budget diagnosis is distinct from any proposed correction;
no measured regression may be relabeled a fixture mismatch.

The bounded sealed-source fixture follow-up maps VAL-P02-006 to WORK-006 in
the [Plan](plan.md) and
[Task0006](tasks/tsk-0006-sealed-source-revision-fixture.md). It supplies the
existing historical reader's real source-revision prerequisites; it changes
no production rule or completed Task evidence.

The separately bounded current-fixture consumer follow-up maps VAL-P02-005
to WORK-005 in the [Plan](plan.md) and
[Task0005](tasks/tsk-0005-current-registry-fixture-consumers.md).
It follows the completed narrow Task-template correction and preserves its
source and evidence. The existing failed hosted run is historical input.

The separately approved Task-template creation boundary maps VAL-P02-004 to
WORK-004 in the [Plan](plan.md) and
[Task0004](tasks/tsk-0004-registered-task-template-instantiation.md).
The completed Task0003 and original Task evidence remain historical.

The current compatibility follow-up maps VAL-P02-003 to WORK-003 in the
[Plan](plan.md) and its new
[Task](tasks/tsk-0003-ci-fixture-and-format-follow-up.md).

The direct P02 request and approved implementation plan are the scoped input.
Relevant existing requirements are REQ-0003-FR-0005, FR-0006, FR-0012,
FR-0013, FR-0014, FR-0018, FR-0019, FR-0020 and FR-0027; this direct
package-local work does not change their reciprocal requirement map at intake.
Existing architecture is [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
[ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md),
and [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).
No new structural decision is required. [Plan](plan.md) owns order and
[Task](tasks/tsk-0001-lifecycle-normalization.md) owns execution evidence.
The follow-up [Task](tasks/tsk-0002-task-summary-writer.md) owns `VAL-P02-002`
execution evidence without changing the first Task's historical observations.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — current explicit P02 profile/template/consumer migration request reuses existing Requirement and architecture scope | VAL-P02-016 | WORK-016 / Task0016; same candidate identity, coupled operating forms/readers/current instances, synthetic boundaries, exact index/message and independent review; P03/P08 and common approval separated |
| N/A — explicit user instruction to retire failing or observed >=600-second hosted QA execution, integrate local/origin main and preserve owned cleanup evidence | VAL-P02-015 | WORK-015 and Task0015 in the Plan; registered-form provenance, scoped contract controls and hooks, actual-index staged/message checks, prospective and actual scoped completion plus independent review; full QA NOT_RUN, provenance inactive/fail-closed and cleanup outcomes observed separately |
| N/A — necessary bounded fixture repair under the explicit normal unit-commit/push/merge instruction | VAL-P02-014 | Genuine registered-form provenance; authentic immutable boundary and typed retention controls; original full declared inputs and inventories; scoped hooks, five named methods, each actual-index staged/message, prospective completion/review and fresh actual closing checks; private raw direct audit deferred and hosted admission separate |
| N/A — necessary bounded fixture repair under the explicit normal unit-commit/push/merge instruction | VAL-P02-013 | Registered-form creation metadata; current pack/template and numbered-member/uncovered-path controls; scoped hooks, each actual-index staged/message, prospective completion/review and fresh actual closing checks; hosted observations separate |
| N/A — necessary bounded fixture repair under the explicit normal unit-commit/push/merge instruction | VAL-P02-012 | Registered-form creation metadata; synthetic QA and reference collection/pack controls plus knowledge missing-member/valid control; scoped hooks, each actual-index staged/message, prospective completion/review and fresh actual closing checks; hosted observations separate |
| N/A — necessary bounded fixture repair under the explicit normal unit-commit/push/merge instruction | VAL-P02-011 | Registered-form creation metadata; three named maintenance, reference-publication and reciprocal-supersession methods with preserved refusal boundaries; scoped hooks, each actual-index staged/message, prospective completion/review and fresh actual closing checks; hosted observations separate |
| N/A — necessary bounded fixture repair under the explicit normal unit-commit/push/merge instruction | VAL-P02-010 | Registered-form creation metadata; named completed-state, own-generation replay and domainless-navigation controls with preserved refusals; scoped hooks, each actual-index staged/message, prospective completion/review and fresh actual closing checks; hosted observations separate |
| N/A — necessary bounded fixture reinstantiation under the explicit normal unit-commit/push/merge instruction and reviewed rollback plan | VAL-P02-009 | Registered-form first-appearance metadata; named routing/native controls with exact-input evidence attribution; scoped hooks, each actual-index staged/message, prospective completion/review and fresh actual closing checks; hosted observations separate |
| N/A — necessary bounded current-contract fixture repair under the explicit normal unit-commit/push/merge instruction | VAL-P02-007 | Named failure evidence; declaration-based governance and navigation controls; immutable archive call accounting before any corpus-budget correction; scoped hooks, actual-index staged/message, prospective completion/review and fresh actual closing checks; hosted observations separate |
| N/A — necessary bounded fixture repair under the explicit normal commit/push/merge instruction | VAL-P02-006 | Exact named RED; 21 explicit shared recovery-fixture methods and preserved refusal assertions; scoped hooks, actual-index staged/message, prospective completion/review and fresh actual closing checks; hosted and integrated-main observations separate |
| N/A — direct approved fixture repair and restoration of the narrow Task-template boundary for normal delivery | VAL-P02-005 | Observed named failures and same-pattern causal RED; bounded Task-template and migration refusal controls plus identity/authority fixtures; scoped hooks, actual-index staged/message, terminal completion and independent code/security review; hosted and integrated-main observations separate |
| N/A — direct approved narrow registered Task-template instantiation correction; other provenance controls remain required | VAL-P02-004 | Real-Git registered-template creation RED/GREEN and boundary negatives, all later lifecycle edges, exact-index staged/message, terminal completion and independent review |
| N/A — direct approved hosted compatibility follow-up; existing requirement meanings are unchanged | VAL-P02-003 | Focused current proof/header and negative regressions, frozen asset refusal, scoped hooks, staged/message, completion and independent review; required hosted and integrated-main observations remain separate |
| N/A — direct approved P02 package-local change; existing REQ-0003 meaning is unchanged | VAL-P02-001 | Registry/form/consumer, Task completion, route, historical and Git-edge checks |
| N/A — direct approved P02 follow-up; existing REQ-0003 meaning is unchanged | VAL-P02-002 | Shared summary and explicit writer focused checks, staged QA, completion and independent review |
