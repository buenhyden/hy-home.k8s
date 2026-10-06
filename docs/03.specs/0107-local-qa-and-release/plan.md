---
title: "Local Quality and Release Lifecycle Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0107-PLAN-0001"
parent_ids: ["SPEC-0107"]
---

# Local Quality and Release Lifecycle Implementation Plan

## Global Constraints

Use the [Spec](spec.md) contract and current [Task](tasks/tsk-0001-local-qa-and-release.md)
for this request. Preserve frozen Archive and completed Task evidence, unique
negative contracts, secret and live boundaries. No check, authorization,
independent review or external publication is presumed from file presence.
The user authorizes local repair, normal logical commits, push/main integration
and cleanup of owned development refs after preservation. Release publication,
remote Project settings and live/native trust changes need their actual
operator route. Update one current owner and its direct consumers per rule.

## Overview

Execute SPEC-0107 in one Task with one execution row. Work packages describe
dependency order only; current status, commands, checks and acceptance are
recorded in that Task. The proposed delivery uses draft, ready, in-progress
and completed Task transitions in distinct normal commits.

## Context

Intake base is clean `main` at `2c9c5546bc10502284fc3c67150e33f090371223`,
with isolated branch `codex/qa-local-lifecycle` and worktree
`.worktrees/qa-local-lifecycle`. Source inspection found a validation-registry
`ciJobs` entry for a nonexistent hosted `qa` job, old hosted-final-full prose,
an inactive QA verifier/tag producer, and historic `NOT_RUN` evidence. These
are source-audit findings, not results of current checks. Current upstream
REQ-0003-FR-0029 still requires SHA tags and must be revised in the owned
requirement slice before the SemVer acceptance contract can be validated.

## Goals & In-Scope

- Retire proven one-off and obsolete QA only after unique ongoing coverage and
  current consumers are accounted for.
- Route local QA by delivery stage and input identity, preserving repository
  document, GitOps, infrastructure and external-service contract coverage.
- Make Commitizen, SemVer Release/tag production and main changelog ownership
  coherent across policy, workflow, scripts and tests.
- Connect Issue/Spec/Task/Project by distinct responsibility and direct links.

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
local selection and exact-index/message checks, resolve full-run preflight,
review independently, record actual evidence and integrate only accepted work.

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LOCAL-QA-001](spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-002](spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-003](spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-004](spec.md#success-criteria--verification-plan) | Audit consumers, transfer continuous coverage, retire obsolete callers, align local delivery, commit/release and Issue/Project owners, then hand off observed evidence | Current REQ-0003/AD-0006 links; selected tools and budget; disjoint writers; independent review | [SPEC-0107-TSK-0001](tasks/tsk-0001-local-qa-and-release.md) | Changed-behavior RED/GREEN, quick selection, exact-index staged and message, final local full if preflight resolved, current anchor completion, semantic review |

## Verification Plan

Before behavior edits, read active validation registry, selected gate commands,
tool identities, hooks and limits. Execute focused failing and passing cases
for changed rules. Use `python3 scripts/qa.py quick` on affected current bytes;
each logical commit gets a reviewed actual index, staged QA and actual message
check. Run local `full` once on the final tree if the selected prerequisite
and budget envelope is available. Record a required unresolved check as FAIL,
NOT_RUN or DEFER with its next owner, never PASS. The separate read-only
reviewer inspects final diff, contract and results. Do not replay an identical
leaf simply because delivery moved from commit to push.

## Risks & Mitigations

Removing a historical test might discard an ongoing guarantee: map current
consumer, preserve distinct negative behavior and recovery evidence first.
Local versus hosted inputs may differ: bind every result to bytes, config,
tool, mode and trust. SemVer migration conflicts with old FR-0029: update
requirement and direct consumer in the same review slice. Remote protection
settings or Release features may differ from tracked files: keep that lane
DEFER until directly observed. Rollback uses forward correction while retaining
Task, Git and Archive evidence.

## Completion Criteria

Every criterion has a Task record with exact input, command, result,
acceptance and remaining owner. Required local checks and independent review
pass on their actual snapshots, no material finding remains, and normal
logical commits are recorded. External Release/Project and live states are
asserted only if independently observed and authorized. Main integration and
owned-worktree cleanup are separately recorded as actual Git outcomes.
