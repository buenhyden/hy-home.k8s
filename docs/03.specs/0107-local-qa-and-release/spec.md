---
title: "Local Quality and Release Lifecycle"
version: "1.2.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0107"
---

# Local Quality and Release Lifecycle Technical Specification (Spec)

## Overview

This package contracts the requested local quality and release workflow for
the public repository. It succeeds the current delivery guidance without
rewriting completed [SPEC-0106](../0106-stage99-lifecycle-normalization/spec.md)
or its historical `NOT_RUN` evidence. The current requirement owner is
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md),
and [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
owns the architectural separation of validation, execution, and evidence.
[ADR-0048](../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md)
records the durable local QA and SemVer release ownership decision.
Original implementation and actual results remain in [Task 0001](tasks/tsk-0001-local-qa-and-release.md).
The completed QA and Archive reappraisal remains in
[Task 0002](tasks/tsk-0002-archive-and-qa-retirement.md). The new purpose-based
QA and CI execution belongs to [Task 0003](tasks/tsk-0003-purpose-qa-and-ci.md).

## Strategic Boundaries & Non-goals

The original WORK-001 instruction authorized a scoped repair of local QA, GitHub workflows and their
direct consumers, standard commit and release preparation, normal logical
commits, push and main integration after valid local evidence. That instruction
also covers cleanup of development branches and owned worktrees after their
history and evidence are preserved. This describes the original delivery and
grants no standing external authority for WORK-002. The persisted user
instruction authorizes P04 local work, normal commits, local main integration
and cleanup of owned development refs after their evidence is preserved;
P04 does not infer push, PR, server-setting, tag or live authorization.
The original instruction did not establish a successful check,
authenticated remote setting, published Release, Project field update, native
hook delivery, or live GitOps/Vault operation. Protected external actions need
their actual target and operator route. A static workflow file cannot serve as
hosted execution evidence.

No frozen Archive body, completed Task, sealed source or original cutover
proof is rewritten. Retiring a one-use script or test requires transfer of any
ongoing protection and a consumer-zero check; historical `NOT_RUN` remains
the factual result for its original input. A passing local result cannot be
promoted to a different hosted or live lane. Registry generation 10 document
profiles, native skill envelopes, and the existing GitOps/runtime boundary
remain under their current owners.

## Contracts

### Current QA selection and retirement

The validation registry owns gate identity, profile membership, path routing,
and argv. Quality policy owns lane, result, budget, reuse, and delivery meaning;
validators own each independent failure rule. Audit every active registration,
script, fixture, test discovery path, hook, and GitHub job against its caller,
purpose, input, mode, trust and ongoing consumer. Retire proven one-off,
legacy, deprecated, duplicate, conflicting or excessive checks in the order:
transfer unique ongoing coverage; remove caller and registration; remove its
dedicated helper, fixture and test; retain necessary past results in the
existing Task or Archive evidence owner. Preserve document profile, relation,
link and state validation and repository-purpose GitOps, Kubernetes, Docker,
project-template, web and Vault contract tests where those surfaces actually
exist. Do not delete a valid regression solely because it failed or ran slowly.

At intake base `2c9c5546`, the validation registry advertised a `qa` CI job
through `ciJobs`, while the hosted CI had no job of that name. Resolve the machine projection
and all of its schema, selector, output and test consumers in one contract
slice; do not rename the advertised job to a different test that proves less.
The `ci` CLI alias is a local profile contract and is assessed separately.
General Archive integrity remains an ongoing validation rule; past cutover
completion proof is a historical record, not a recurring gate unless a distinct
current consumer demonstrates its necessity.

### Current QA and Archive reappraisal

The follow-up [Plan unit WORK-002](plan.md#work-breakdown) inventories actual
validation leaves, callers, imports, discovery paths, fixtures, hooks and
hosted jobs before a retirement decision. Classify each by current DOC, WEB,
VAULT, TEMPLATE, DOCKER or K8S purpose, unique parser/selector/security
guarantee, input identity, trust boundary and durable consumer. Keep supported
older-version contracts when they still have a consumer. Where a guarantee
continues, transfer its unique coverage to the current owner before removing
a duplicate leaf, caller or registration, then dedicated helper, fixture and
test. Where the guarantee itself has ended, document consumer-zero evidence
and remove its coupled surfaces without inventing a replacement. A name,
duration, previous failure, completed-document count or historical status/hash
is not a disposal verdict. Current negative and recovery checks remain where
they protect a supported contract.

Review current Archive policy, catalog and inbound consumers separately from
frozen historical execution and cutover records. Promote a still-current rule
at its existing owner; preserve cited historical facts without treating their
old procedure text as current policy. Any whole-unit Git-history-only
disposition requires actual value and consumer analysis, specific approval,
hold clearance and a reachable recovery coordinate before the unit changes.
An unchanged original payload is not permission to delete its catalog or route.
No Archive move or deletion follows merely from this Spec amendment.

The same `WGOV-CORE / 3.0.0-draft.3` candidate is a review input for C06,
C09 and C11, with proposed common owner `buenhyden` and proposed
Project-Template path `.agents/governance/shared-standard.md`. Its inspected
file digest is `3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271`;
that identifies draft content, not approval. A final joint edition, local
adoption and four-repository adoption require separate actual decisions and
evidence. This repository's existing QA and Archive owners remain authoritative
for local implementation while that common decision is pending.

### Purpose-based QA and CI follow-up

[WORK-003](plan.md#work-breakdown) and
[Task 0003](tasks/tsk-0003-purpose-qa-and-ci.md) own the new P05 execution.
Inventory the actual Git hooks, validation leaves, imports, subprocess callers,
test discovery and fixtures, workflow jobs, input identity and result consumers.
Classify continuing DOC, WEB, VAULT, TEMPLATE, DOCKER and K8S guarantees by
their current repository purpose. Retire a duplicate or completed-only check
only after its unique continuing protection and callers have an owner. Measure
representative before/after leaf executions, parsing and Git reads before
claiming a reduction. The current Archive reader and supported historical
compatibility remain governed by their existing owners.

Local purpose QA selects the affected dependency closure, including parent,
links, deletion/rename and generated consumers. A changed validator, schema or
selector gets named failure and boundary regressions; ordinary documents get
their applicable profile, relation, link, state and content checks. Execute
read-only lint and format on the final logical Git index before a local commit,
and validate the actual commit message. Explicit writers repair findings and
produce a new input. Reuse a leaf only when its bytes and history, config,
tool, scope, mode and trust are identical; a phase label or path match alone
does not establish that identity. Business deadlines and validation reserve
approvals do not gate the work. Actual command limits, cancellation and child
cleanup remain bounded by the validation runner and their observed result.

The public repository's hosted PR route checks narrow branch metadata and
selected style on the actual server candidate with trusted base configuration.
Its required check producer, source App, branch ruleset and failure path require
read-back at the relevant PR input before claiming hosted success. Historical
PR runs cannot prove this Task's changed input. Local purpose QA does not run
untrusted public PR code on a credentialed homelab runner. A deployment style
result requires an actual deployment workflow, candidate and run. Remote
settings, dispatch, deployment, credentials and live checks retain their
separate operator authority. `SEC-P01-001` HIGH remains an open CI/security
finding until the owning security review resolves its actual workflow control
input. The same `WGOV-CORE / 3.0.0-draft.3` is only the C01/C06/C07/C12
review candidate for this follow-up; no final common approval or joint
adoption is inferred.

### Actual agent evaluation evidence

Keep agent evaluation evidence as an authored evidence domain, separate from
recurring repository QA. A comparable cycle fixes one task and baseline for
both `noSkill` and `withSkill` conditions, then preserves their actual raw
outputs and session provenance. One cycle is one paired trial: its single
`baseline.md` and `with-skill.md` each hold one condition's raw output. The
task and both outputs must exist before a score is entered. Declare that
one-trial granularity, observable signals, criterion and scorer IDs,
partial-trial treatment and human calibration before aggregation. Additional
or repeated trials use distinct cycle identities; previous observed outputs
and scores are not overwritten. The aggregate reports only the actually
completed cycle count and its declared scope, without a blanket performance
threshold.

The [evaluation router](../../../.agents/evaluations/README.md) points to
Stage 99 task, score and results forms. One results owner holds only aggregates
supported by complete declared pairs. Empty capacity is not an observed run
or a zero score. The agent evaluator owns assessment; original Task, provider
and runtime owners retain their authorization and direct observation. Historical
synthetic fixtures and absent expected outputs are not paired run evidence.
User-provided skill definitions that are absent from this workspace can guide
criteria but are not installed, invoked or made native by this contract.
This domain has no registered grader gate without a separately demonstrated
ongoing consumer and admission under quality policy.

### Delivery boundary and cost

The public repository runs purpose QA locally, with selected hosted PR style
as a distinct final defense. Select focused named regressions for changed
behavior, continuing Archive and security protections, affected document
contracts for ordinary edits, and exact-index staged checks for logical
commits. The long local full/ci sweep and blanket unit discovery are retired
from completion; a change to shared QA code selects its actual affected gates
and named units after tools, time and native execution approval are resolved.
A push, PR, main integration and
postmerge step must not repeat a successful leaf for identical bytes, config,
tool, scope, mode and trust. Distinct index, working-tree, integrated-main and
external observations remain separate evidence. The first optimization order
is duplicate leaf removal, then content versus implementation regression,
shared parsing and Git reads within a run, affected selection, and finally
narrow proven reuse. No speed claim is accepted without measurement.

Required lint and format checks run against the final logical index immediately
before each local commit. They share one declared style-rule owner with the
selected hosted PR style check, but the PR merge SHA and run are a distinct
input and trust boundary. An identical successful local style leaf is not
replayed by a second local caller. A deployment style check is conditional on an
actual deployment workflow; no deployment workflow or hosted run is inferred
from this contract.

Retire hosted `qa-isolated` execution together with its direct callers and
dedicated regressions. Keep the PR branch-policy check and `ci-summary` as
branch and delivery metadata only. Add only the selected style check as a
separate PR final defense on its actual merge input. An unknown, failed or
missing applicable branch result fails the summary; the PR-only branch check
is `NOT_APPLICABLE` on main. Historical hosted full, unit and document-content
QA remain `NOT_RUN` when unexecuted, never a local-result or style proxy or a
current completion gate. Remove or
repair stale hosted proof and tag publication
paths coherently, preserving limited permissions, immutable Action identities
and distinct provenance when a current consumer still exists.
`PASS`, `FAIL`, `NOT_RUN`, `NOT_APPLICABLE` and `DEFER` remain separate from
acceptance, authorization, integration and retention. A failed required local
gate or unresolved independent review blocks completion.

### Git, release and work tracking

Use one Commitizen contract based on `.cz.toml` and `.gitmessage` for authored
Conventional Commits and the active commit-message hook. Keep generated
message exceptions explicitly bounded. Use one SemVer tag and GitHub Release
producer, with an exact reviewed main commit as its source; it never moves an
existing tag or uses a development push to publish. The canonical
`CHANGELOG.md` is main release history, updated in a release-preparation PR
from actual integrated changes. A seven-day generated artifact may aid review
but cannot replace that committed owner. If immutable Releases are enabled,
attach required assets to the draft before publication. Do not infer the
remote immutable-release setting from repository files.

Release versioning tracks the public compatibility contract: supported CLI
commands and options, machine JSON schemas, governed document profiles and
frontmatter, GitOps desired state, and external-service interfaces. A breaking
change to a released 1.0-or-later contract raises the major version, an
additive compatible capability raises minor, and a compatible correction
raises patch. For a first 0.y release, the operator selects and records the
initial version and compatibility promise from the reviewed release scope;
history alone does not authorize an arbitrary first tag. Preserve existing
`main-<full SHA>` tags as historical refs without moving or republishing
them. A release label describes the repository contract, not deployment,
provider runtime acceptance or live infrastructure certification.

An Issue owns request and priority, this Spec owns acceptance, the Task owns
execution evidence, and a Project displays work state. The reference between
them is one-way metadata or navigation; no full Spec/Task copy or bidirectional
status overwrite is introduced. Remote Issue and Project state is checked
only when observed through an authorized interface.

## Core Design

The [Plan](plan.md) records the original four bounded slices: inventory and succession, local validation
and Git stage routing, release and commit consumers, and final evidence/review.
WORK-002 adds a separate current QA and Archive reappraisal after those
historical slices.
WORK-003 adds a separate purpose-based QA and CI follow-up after the completed
WORK-002 record. Its own Task carries current commands, results and acceptance.
Each source owner updates its current contract and direct consumers together.
Maintain distinct static, local runner, hosted, provider-native, and live
evidence lanes. [Task 0001](tasks/tsk-0001-local-qa-and-release.md) is the
sole WORK-001 work-state and implementation-acceptance owner and records C16 source
checks. Only terminal C17 closing-index, commit and post-commit facts use the
non-authoritative handoff receipt described below. The current
[main release Runbook](../../05.operations/runbooks/0012-main-release-preparation-runbook.md)
applies this Spec's SemVer and operator boundary to a reviewed main release.

## Data Modeling & Storage Strategy

The existing validation registry and schema own machine gate records;
Stage 99 owns document forms. Git owns exact source and release history;
`CHANGELOG.md` holds committed main release notes. Task evidence identifies
the actual revision, input, command, result, reviewer and remaining owner.
No additional progress registry, Spec-local fixture suite, or second archive
recovery ledger is created.

## Interfaces & Data Structures

Keep the current profile and CLI surfaces until actual consumers are traced.
Any registry or schema change must update the loader, affected selector,
contract tests and documented output together. A release entry binds a strict
SemVer value, the main commit, canonical changelog content and the GitHub
Release/tag identity under one producer; implementation must refuse a mismatched
or pre-existing moving tag. Issue/Project integration uses IDs or links rather
than duplicating bodies or acceptance state.

## Edge Cases & Error Handling

Missing tools or a required budget fail or defer the applicable lane with an
owner; they never become a pass. Invalid registry or commit messages fail
before a commit. A changed snapshot invalidates only the evidence that actually
depended on it. A deleted historical gate with an active recovery reader or
unique negative meaning is retained until that reader is transferred. A
missing hosted job, failed local gate, nonmain release source, invalid SemVer,
or tag collision must not publish a Release or claim completion.

## Failure Modes & Fallback / Human Escalation

Preserve the earlier passing source and historical evidence with forward
correction. Stop dependent completion or publication on a failed required gate
or material independent finding; continue independent safe repairs. Route
remote settings, Release publication, Project writes, credentials and live
operations to their operator with the exact target and reviewed revision.

## Verification Commands

Read selected prerequisites and runner limits from the active registry and
quality policy before invoking checks. The current selected entry points are
`python3 scripts/qa.py quick` and `python3 scripts/qa.py staged` plus named
purpose/unit commands; implementation changed-input selection and exact
results are recorded in the Task. Use named focused regressions for changed
behavior, the configured actual commit-message validation and an independent
read-only semantic review. A `completion` check, if selected, uses the current
Spec anchor and actual index. The original [Task 0001](tasks/tsk-0001-local-qa-and-release.md)
owns WORK-001 execution and acceptance through the substantive C16
input; this Spec does not promote evidence from another input or lane. For
the original SPEC-0107 closing delivery only, the controller records terminal
closing-index checks and the closing commit and post-commit delivery facts
after observation in an ignored handoff receipt referenced by the Task and
final response. That receipt supports delivery verification; it is not a
second work-state owner, approval source or substitute for Task acceptance.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-LOCAL-QA-001 | Consumer graph and focused regression show ongoing coverage before obsolete callers, dedicated helpers and tests are retired; Archive integrity and past cutover proof remain distinct. Official primary sources are dated and traced from claim to local decision in Task evidence. |
| VAL-LOCAL-QA-002 | Local stage matrix, exact-index pre-commit style checks, selected affected and named behavior/Archive/security results, and independent review show bounded selection without a retired full/ci sweep, blanket unit discovery, duplicate same-input leaves or an unobserved hosted result claim. The selected hosted PR style check remains a required PR defense: when an actual PR run is observed, evaluate it at its own merge SHA/run; otherwise record `DEFER` for that hosted lane. Local implementation may be accepted from its distinct source and trusted-base checks. Absent deployment routing stays unobserved. Official primary sources are dated and traced from claim to local decision in Task evidence. |
| VAL-LOCAL-QA-003 | Commitizen, SemVer release producer and main `CHANGELOG.md` contracts have focused positive and refusal evidence; actual remote publication is recorded separately. |
| VAL-LOCAL-QA-004 | Issue/Spec/Task/Project ownership, current links and no-copy/no-bidirectional rules are reviewed; the evaluation route and empty aggregate capacity preserve separate evidence authority without fabricating a run; final Task records commands, lanes, limits, approvals, integration and remaining owner. |
| VAL-LOCAL-QA-005 | The current leaf/caller/import/discovery/fixture/consumer inventory supports each QA keep, transfer or retirement decision and focused regression on its actual input. Current Archive policy, retained historical evidence and any proposed whole-unit disposition have distinct owners and proof; no frozen payload, catalog unit or route is removed without specific approval, hold and recovery evidence. The Task records source, command, result, review and remaining owner without converting prior PR success, local checks or a draft common edition into current hosted, live or joint-adoption PASS. |
| VAL-LOCAL-QA-006 | On the actual P05 input, a leaf/caller/consumer map supports DOC, WEB, VAULT, TEMPLATE, DOCKER and K8S purpose selection, safe affected closure and any retirement or result reuse. Changed rules have focused failure and boundary regression; the final local index has selected read-only style, document and purpose checks, actual-message validation, independent review and a single Task acceptance decision. A representative before/after measurement states actual leaf, parsing and Git-read counts without an inferred speed claim. Hosted required checks and selected PR style are verified only at their own SHA/run and protection input; unavailable remote, native, deployment and live evidence stays separately unresolved. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-001 | Registry owner, caller/coverage map and focused regression; [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) consumer-zero and compatibility retirement; [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) continuing Archive integrity distinct from past cutover proof; [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) active script, test and workflow inventory; [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) dated source, claim, scope and local decision in Task evidence. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-002 | Local and hosted lane boundary review; [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) proportionate selected checks and independent review; [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) distinct local, hosted and live evidence labels; [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) focused, staged and final local input evidence. |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-003 | SemVer producer and existing-tag refusal; [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) commit and release consumer inventory. |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-004 | Unique work-tracking owner review; [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) Task-owned implementation result and acceptance, with only terminal SPEC-0107 delivery facts in its referenced non-authoritative handoff receipt; [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) current owner links and retired-consumer succession; [REQ-0003-FR-0031](../../01.requirements/0003-workspace-agent-governance-platform.md) paired evaluation route, form ownership and empty aggregate boundary. |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-005 | Current consumer and unique coverage disposition before retirement; [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) current Archive integrity versus historical cutover proof; [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) actual active script/test/workflow inventory; [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) dated source and claim-to-local-decision evidence. |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-006 | Current purpose/leaf/caller mapping and uniquely owned negative checks; [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) separate local and hosted execution; [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) impact selection and measured reuse; [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) exact-input evidence boundaries; [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) active script, test, hook and workflow consumers; [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) final local index and selected checks. |
