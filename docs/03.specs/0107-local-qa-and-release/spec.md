---
title: "Local Quality and Release Lifecycle"
version: "0.1.0"
type: "sdlc/spec"
status: "in-progress"
owner: "platform"
updated: "2026-10-07"
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
Implementation and actual results belong to this package's [Task](tasks/tsk-0001-local-qa-and-release.md).

## Strategic Boundaries & Non-goals

The user authorizes a scoped repair of local QA, GitHub workflows and their
direct consumers, standard commit and release preparation, normal logical
commits, push and main integration after valid local evidence. That instruction
also covers cleanup of development branches and owned worktrees after their
history and evidence are preserved. It does not establish a successful check,
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

The public repository runs QA locally. Select focused regressions for changed
behavior, affected document contracts for ordinary edits, and exact-index
staged checks for logical commits. Local full QA is selected for a change to
the global QA contract or an explicit bounded audit; this package changes that
contract and therefore requires one final local full run after tools, time and
native execution approval are resolved. A push, PR, main integration and
postmerge step must not repeat a successful leaf for identical bytes, config,
tool, scope, mode and trust. Distinct index, working-tree, integrated-main and
external observations remain separate evidence. The first optimization order
is duplicate leaf removal, then content versus implementation regression,
shared parsing and Git reads within a run, affected selection, and finally
narrow proven reuse. No speed claim is accepted without measurement.

Retire hosted `qa-isolated` execution together with its direct callers and
dedicated regressions. Keep the PR branch-policy check and `ci-summary` as
branch and delivery metadata only. An unknown, failed or missing applicable
branch result fails the summary; the PR-only branch check is
`NOT_APPLICABLE` on main. The hosted QA field remains `NOT_RUN`, never a
local-result proxy. Remove or repair stale hosted proof and tag publication
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

The [Plan](plan.md) orders four bounded slices: inventory and succession, local validation
and Git stage routing, release and commit consumers, and final evidence/review.
Each source owner updates its current contract and direct consumers together.
Maintain distinct static, local runner, hosted, provider-native, and live
evidence lanes. The [Task](tasks/tsk-0001-local-qa-and-release.md) is the
only execution state and check-result record. The current
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
quality policy before invoking checks. The current canonical entry points are
`python3 scripts/qa.py quick`, `python3 scripts/qa.py staged`, and
`python3 scripts/qa.py full`; the changed-input selection and exact command
result are recorded only in the Task. Use named focused regressions for changed
behavior, the configured actual commit-message validation and an independent
read-only semantic review. A `completion` check, if selected, uses the current
Spec anchor and actual index. No test result is asserted by this draft.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-LOCAL-QA-001 | Consumer graph and focused regression show ongoing coverage before obsolete callers, dedicated helpers and tests are retired; Archive integrity and past cutover proof remain distinct. Official primary sources are dated and traced from claim to local decision in Task evidence. |
| VAL-LOCAL-QA-002 | Local stage matrix, exact-index checks, full preflight/result and independent review show bounded selection without duplicate same-input leaves or a hosted QA claim. Official primary sources are dated and traced from claim to local decision in Task evidence. |
| VAL-LOCAL-QA-003 | Commitizen, SemVer release producer and main `CHANGELOG.md` contracts have focused positive and refusal evidence; actual remote publication is recorded separately. |
| VAL-LOCAL-QA-004 | Issue/Spec/Task/Project ownership, current links and no-copy/no-bidirectional rules are reviewed; the evaluation route and empty aggregate capacity preserve separate evidence authority without fabricating a run; final Task records commands, lanes, limits, approvals, integration and remaining owner. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-001 | Registry owner, caller/coverage map and focused regression. |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-001 | Consumer-zero and compatibility retirement review. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-001 | Archive integrity and past cutover evidence remain distinct. |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-001 | Active script, test and workflow consumer inventory. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-002 | Local and hosted lane boundary review. |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-002 | Proportionate selected checks and independent review. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-002 | Distinct local, hosted and live evidence labels. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-002 | Focused, staged and final local input evidence. |
| [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-001 | Dated primary source, claim, scope and local decision in Task evidence. |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-003 | SemVer producer and existing-tag refusal. |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-003 | Commit/release consumer inventory. |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-004 | Unique work-tracking owner review. |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-004 | Task-only command/result and handoff evidence. |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-004 | Current owner links and retired-consumer succession. |
| [REQ-0003-FR-0031](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCAL-QA-004 | Actual paired evaluation route, form ownership and empty aggregate boundary. |
