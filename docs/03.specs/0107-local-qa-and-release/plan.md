---
title: "Local Quality and Release Lifecycle Plan"
version: "1.3.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0107-PLAN-0001"
parent_ids: ["SPEC-0107"]
---

# Local Quality and Release Lifecycle Implementation Plan

## Global Constraints

Use the [Spec](spec.md) contract, completed
[Task 0001](tasks/tsk-0001-local-qa-and-release.md) and
[Task 0002](tasks/tsk-0002-archive-and-qa-retirement.md) as history, and current
[Task 0003](tasks/tsk-0003-purpose-qa-and-ci.md) for the P05 follow-up.
Preserve frozen Archive and completed Task evidence, unique
negative contracts, secret and live boundaries. No check, authorization,
independent review or external publication is presumed from file presence.
The original WORK-001 instruction authorized local repair, normal logical commits, push/main integration
and cleanup of owned development refs after preservation. Release publication,
remote Project settings and live/native trust changes need their actual
operator route. Update one current owner and its direct consumers per rule.
That original scope is historical and is not standing P04 external authority.
The persisted user instruction authorizes local P04 work, normal commits,
local main integration and owned branch/worktree cleanup after preserving
evidence. No current push, PR, server-setting, tag or live authority is
inferred from the original WORK-001 wording.
The current P05 instruction authorizes investigation, planning, local source
and consumer repair, selected local validation, normal logical commits, local
main integration and cleanup of its owned branch and worktree. It does not
grant remote write or dispatch, deployment, secret access, settings changes or
an expanded live authority.
The current P06 instruction authorizes bounded local investigation, source and
consumer repair, selected validation, normal logical commits, local main
integration and owned-worktree cleanup for commit, release and work tracking.
It does not authorize tag or Release publication, remote Issue or Project
mutation, server settings, workflow dispatch, secrets, deployment or live
operation. Keep prior completed Task records intact.

## Overview

The original SPEC-0107 delivery used one completed Task and WORK-001. The
completed reappraisal used WORK-002 and its own Task. Completed P05 execution,
checks and acceptance belong only to WORK-003 and Task 0003. P06 execution
belongs to WORK-004 and Task 0004. Only actual terminal original SPEC-0107 closing
checks, commit and delivery facts go to its referenced non-authoritative
handoff receipt. Its draft, ready, in-progress and completed transitions
use distinct normal commits; the Task links the actual evidence and delivery
boundary.

## Context

Intake base is clean `main` at `2c9c5546bc10502284fc3c67150e33f090371223`,
with isolated branch `codex/qa-local-lifecycle` and worktree
`.worktrees/qa-local-lifecycle`. Source inspection found a validation-registry
`ciJobs` entry for a nonexistent hosted `qa` job, old hosted-final-full prose,
an inactive QA verifier/tag producer, and historic `NOT_RUN` evidence. These
are source-audit findings, not results of current checks. At intake,
REQ-0003-FR-0029 required SHA tags; the owned current Requirement slice
revises that contract for SemVer acceptance and its direct consumers.

## Goals & In-Scope

- Retire proven one-off and obsolete QA only after unique ongoing coverage and
  current consumers are accounted for.
- Route local QA by delivery stage and input identity, preserving repository
  document, GitOps, infrastructure and external-service contract coverage.
- Make Commitizen, SemVer Release/tag production and main changelog ownership
  coherent across policy, workflow, scripts and tests.
- Connect Issue/Spec/Task/Project by distinct responsibility and direct links.
- Preserve a profile-routed, actual paired agent-evaluation evidence capacity
  without turning synthetic fixtures into a standing QA gate or measured result.

## Non-Goals & Out-of-Scope

No broad deletion by filename or test duration, full Spec/Task copies into
Issues, bidirectional Project synchronization, frozen-body edits, cluster or
Vault actions, credentials, native trust changes or unobserved remote-success
claims. A checked-in release workflow is not authorization to publish a
specific GitHub Release.

## Work Breakdown

Prepare a bounded consumer and coverage map; transfer any ongoing rule before
removing its old caller and dedicated fixtures. Update policy and machine
contracts with their direct consumers, then run focused regressions. Perform
local selection and exact-index/message checks, resolve selected-gate preflight,
route the empty evaluation evidence domain through Stage 99, review
independently, record actual evidence and integrate only accepted work.

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LOCAL-QA-001](spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-002](spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-003](spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-004](spec.md#success-criteria--verification-plan) | Audit consumers, transfer continuous coverage, retire obsolete callers, align local delivery, commit/release and Issue/Project owners, route actual paired evaluation capacity, then hand off observed evidence | Current REQ-0003/AD-0006/FR-0031 links; selected tools and budget; disjoint writers; independent review | [SPEC-0107-TSK-0001](tasks/tsk-0001-local-qa-and-release.md) | Changed-behavior RED/GREEN, evaluation profile/link and empty-result checks, conditional quick selection, exact-index staged and message, named purpose/unit gates after retirement, current anchor completion, semantic review |
| WORK-002 | [VAL-LOCAL-QA-005](spec.md#success-criteria--verification-plan) | Inventory current QA leaf/caller/import/discovery/fixture/consumer graph and Archive policy/catalog/route consumers; decide keep, transfer or retire by current purpose; implement only supported, authorized local changes | Existing quality and Archive owners; immutable historical Task and Archive payloads; specific disposition approval, hold and recovery proof before any whole-unit removal | [SPEC-0107-TSK-0002](tasks/tsk-0002-archive-and-qa-retirement.md) | Intake and consumer map, focused changed-rule regression, selected actual-index document/style and purpose checks, independent review, bounded disposition and remaining-owner evidence recorded in the Task |
| WORK-003 | [VAL-LOCAL-QA-006](spec.md#success-criteria--verification-plan) | Map current purpose QA, scripts/tests/hooks and hosted producer/consumer inputs; remove proven duplicate or completed-only work with unique protection retained; select affected checks and exact-index style; measure representative executions and route local versus hosted outcomes | Completed WORK-001/002 records; existing quality/validation/CI owners; source and trust boundary proof before reuse; separate authority for remote settings, dispatch or live execution | [SPEC-0107-TSK-0003](tasks/tsk-0003-purpose-qa-and-ci.md) | Exact caller and input map, focused changed-rule failure/boundary regression, selected final-index document/purpose/style and actual-message checks, measured comparison, independent review and Task-owned acceptance |
| WORK-004 | [VAL-LOCAL-QA-007](spec.md#success-criteria--verification-plan) | Align the one authored/generated commit grammar, effective hook and prompt consumers; audit release preview/write/publish boundaries and public compatibility/history/asset checks; keep Issue/Spec/Task/Project links and state ownership one-way | Completed WORK-001–003 history; current `.cz.toml`, Git policy, release Runbook, hook connection and actual read-only hosted settings; distinct operator authority for tags, Releases and Project writes | [SPEC-0107-TSK-0004](tasks/tsk-0004-commit-release-and-work-tracking.md) | Current owner/consumer map, focused positive/refusal and boundary cases, selected exact-index and actual-message checks, independent review, actual local integration and Task's single local criterion verdict; remote publication and Project scope separately observed or deferred |

WORK-002 follows this dependency order: trace active producer and reader
surfaces; classify continuing and obsolete guarantees; transfer any unique
continuing coverage; remove proven duplicate caller/registration and then
its dedicated support; inspect current Archive policy and inbound links;
record any separate protected whole-unit disposition decision. A historic
cutover census, old completed Task or prior successful PR run does not prove
the current changed input. No Archive payload, catalog unit or route is removed
without the exact approval, hold and recovery evidence. The joint
`WGOV-CORE / 3.0.0-draft.3` C06/C09/C11 comparison is a candidate review,
not a final edition or four-repository adoption.

WORK-003 follows the actual source map: inspect leaves, callers, discovery,
fixtures, hooks, workflow jobs, inputs and result consumers; classify continuing
purpose guarantees; transfer unique protection before removing duplicate
callers or dedicated support; repair impact closure and shared parsing/Git
reads where measurement supports it; then run named changed-rule regressions,
selected local checks and independent review. Keep the already observed
`ci-summary` and `style-pr` route unless a current input exposes a real defect.
Read back any required-check producer or ruleset decision on its own remote
input. An earlier PR run is historical evidence, not WORK-003 execution.
The `WGOV-CORE / 3.0.0-draft.3` C01/C06/C07/C12 comparison remains a common
candidate without source revision, approval or joint adoption evidence.

WORK-004 starts from the actual Commitizen, Git, Runbook, Issue and hosted
consumers. Preserve already coherent `main`/`codex/` routing and completed
Task evidence. Repair only proven grammar, prompt, hook, release or link
inconsistencies with their direct tests and readers. Verify authored and
generated-message behavior before changing policy text. Treat local release
preview, tracked changelog write and remote publication as separate steps,
and leave unavailable Project or immutable-Release settings unresolved. The
common C02/C05/C07/C10 comparison uses the same draft.3 candidate, without
claiming final common approval or local/joint adoption.

## Verification Plan

For WORK-004, inspect the exact current Commitizen config, active hook path,
message draft builder, release CLI, selected workflow and Issue/Project
consumers. Changed rules receive focused positive, negative and boundary
regressions; document edits receive the applicable Stage 99 profile, link,
relation and state checks. Run selected read-only lint/format and purpose
gates on the exact final index, validate the actual candidate message, and
record normal commits and local integration on their own snapshots. An
observed main-push check or earlier PR success is not P06's hosted PR result.
Tag/Release publication, remote Project state, native hook delivery, immutable
Release setting and deployment/live results need direct authorized evidence;
otherwise Task 0004 records `DEFER` or `NOT_RUN` with the next owner.

For WORK-003, derive the exact affected gate and named unit set from the
current validation registry and measured caller map. Use focused RED/GREEN for
changed executable behavior, then selected profile/relationship/link/state
checks for authored documents. Run read-only lint and format over the final
index before each normal commit and validate the actual message. Record any
different local working tree, index, hosted PR candidate and main tree as
separate inputs. Reuse a leaf only when bytes/history, config, tool, scope,
mode and trust agree. Measure representative before/after leaf, parsing and
Git-query counts before claiming a reduction. A failure or unavailable tool
retains its actual result, location and next owner. The Task owns the single
criterion acceptance decision and independent review result. No full/ci sweep
or blanket discovery is selected merely because the QA contract changed.

For WORK-002, use current Registry and quality policy to select affected
document, Archive, security and purpose checks after the actual consumer map
and changed paths exist. A focused negative/boundary regression is required
for changed validators or selectors; ordinary document edits select the
relevant profile, relationship, link, state and style checks. Keep static
source, local, hosted PR and live evidence separate. Prior PR 136 success is
evidence only for its earlier input. The new Task records actual inputs,
results, reviews and unresolved HIGH workflow-control risk. This Plan does
not authorize a destructive Archive operation or claim QA completion.

Before behavior edits, read active validation registry, selected gate commands,
tool identities, hooks and limits. Execute focused failing and passing cases
for changed rules. Select `python3 scripts/qa.py quick` during iterations only
when changed working-tree bytes need separate evidence. If the final actual-index
`staged` check covers an identical leaf with equivalent bytes, configuration,
tool, scope, mode and trust, record quick as `NOT_RUN` (not required for this
change); do not repeat that leaf. Each logical commit gets a reviewed actual
index, staged QA and actual message check. Select final named behavior,
Archive and security regressions and purpose gates actually affected by this
global-QA change; do not use retired `full`/`ci` sweeps or blanket unit
discovery as a completion shortcut. Resolve their prerequisite and budget
envelope. Record a required unresolved check as FAIL,
NOT_RUN or DEFER with its next owner, never PASS. The separate read-only
reviewer inspects final diff, contract and results. Do not replay an identical
leaf simply because delivery moved from commit to push.
The final local index also receives required lint and format checks immediately
before each commit; do not repeat an identical successful local style leaf.
The selected hosted style job remains a required PR defense. Verify its own
merge SHA/run when an actual PR run is observed; otherwise record that hosted
lane as `DEFER` without blocking acceptance of distinct local implementation
and trusted-base source checks. A deployment style result depends on a real deployment workflow and
execution, which are not established by this Plan; do not infer it from a PR
style configuration or local PASS.
For the evaluation route, validate its Stage 99 profile, reciprocal links and
empty aggregate shape. No actual paired output or scored criterion is supplied
in this change, so trial execution, score truth and native skill loading are
`NOT_RUN` or `NOT_OBSERVED` as applicable, never inferred from form validity.

## Risks & Mitigations

For WORK-004, a broader message regex could accept unsupported authored
syntax or reject generated Git messages: test the exact Commitizen tool and
real candidate file before changing the shared grammar. A release script
could move a prior tag or publish before assets are verified: retain
history/target checks and keep execution behind the operator boundary. An
Issue/Project view could become a second acceptance ledger: keep only direct
IDs or short links and the Task as execution owner. Review current server
settings separately from tracked workflow prose.

Removing a historical test might discard an ongoing guarantee: map current
consumer, preserve distinct negative behavior and recovery evidence first.
Local versus hosted inputs may differ: bind every result to bytes, config,
tool, mode and trust. SemVer migration conflicts with old FR-0029: update
requirement and direct consumer in the same review slice. Remote protection
settings or Release features may differ from tracked files: keep that lane
DEFER until directly observed. Rollback uses forward correction while retaining
Task, Git and Archive evidence.

## Completion Criteria

WORK-004 reaches local acceptance only when its Task records the bounded
source and consumer map, relevant changed-rule regressions, exact-index and
actual-message PASS, independent review, normal local commits, and one
VAL-LOCAL-QA-007 decision with unresolved required failures explicitly
resolved. The Task closing commit and local main integration receive actual
later delivery evidence rather than a prospective OID. A local acceptance
does not close remote publication, Project access, immutable Release settings,
native enforcement, common-edition approval or live operation.

WORK-003 reaches local acceptance only when its Task links actual source and
consumer changes, selected named regressions, final-index QA/style and actual
message results, measured comparison, independent review, normal commits and
local integration to its single VAL-LOCAL-QA-006 verdict. Any required adverse
result remains until a matching later PASS explicitly resolves it. Remote
protection, hosted run, common edition, native enforcement and live/deployment
claims remain separate from that local verdict. `SEC-P01-001` HIGH remains
with its security/CI owner until independently resolved on its own input.

Every criterion has a Task record with exact input, command, result,
acceptance and remaining owner. Required local checks and independent review
pass on their actual snapshots, no material finding remains, and normal
logical commits are recorded. External Release/Project and live states are
asserted only if independently observed and authorized. Main integration and
owned-worktree cleanup are separately recorded as actual Git outcomes. For
this package's closing-document commit, the controller records exact changed
index checks, review and post-commit delivery only after observation in the
Task-referenced handoff receipt, avoiding a self-referential evidence/OID edit.
This does not replace Task ownership of implementation acceptance.
