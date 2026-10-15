---
title: "r10 Local Governance and Delivery Remediation Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0115-PLAN-0001"
parent_ids: ["SPEC-0115"]
---

# r10 Local Governance and Delivery Remediation Implementation Plan

## Global Constraints

Preserve terminal evidence and sealed Archive bytes. Do not read secrets or
private memory data, mutate live or remote state, edit global configuration,
or claim a new WGOV edition, local adoption or sandbox enforcement without
its actual decision and observation. A protected action needs its own current
authority and reviewed target.

## Overview

Execute [SPEC-0115](spec.md) through the single
[Task](tasks/tsk-0001-r10-local-remediation.md). P01 to P08 are purposes and
order, not eight new packages. The Task is the only findings and progress
owner for this request. Independent review and the user's scoped local
authorization approve this local execution plan; common-edition, remote,
native-sandbox and live decisions remain at their respective owners.

## Context

The r10 comparison coordinate is `a45da94c9573c2613943c4881f85b80e4dfa65dc`;
actual Git state is re-observed before dependent edits. SPEC-0114 and much of
SPEC-0107 are already completed. Stage 99 records WGOV-CORE 3.0.0 approval,
source verification and C07 local acceptance, while its adapter remains
`candidate`. SPEC-0105 Task 0004 holds pending full-core adoption. The Codex
session observed hook delivery and dummy-variable absence but a failed local
`bwrap` sandbox, so static config is not runtime isolation evidence.

## Goals & In-Scope

- Inventory material P01 to P08 findings with exact sources, classifications,
  dispositions and owners, including unchanged and inaccessible candidates.
- Implement confirmed scoped local corrections at existing document, policy,
  validation, CI, provider and GitOps owners with affected consumers.
- Validate each changed logical unit on its actual input and obtain an
  independent read-only review before local delivery.
- Record residual remote, runtime, common-edition and live boundaries without
  promoting their claims from local checks.

## Non-Goals & Out-of-Scope

No new common WGOV approval, four-repository adoption, remote ruleset or
Project mutation, Release publication, live cluster/Vault/backup operation,
memory-store cleanup, bulk document restyling or Archive move without its
actual closure and disposition prerequisites.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-R10-001](spec.md#success-criteria--verification-plan) | Re-observe baseline, WGOV evidence, authority and finding ownership | None | [Task](tasks/tsk-0001-r10-local-remediation.md) | Git/source/decision comparison and findings review |
| WORK-002 | [VAL-R10-002](spec.md#success-criteria--verification-plan) | Audit current profiles, first-recorded Task state, direct reviewed Spec/Plan approval and document/consumer drift | WORK-001 | [Task](tasks/tsk-0001-r10-local-remediation.md) | Initial in-progress/blocked/ready and terminal-refusal cases; local candidate direct draft-to-approved positive/negative cases; selected profile, language, link and lifecycle checks |
| WORK-003 | [VAL-R10-003](spec.md#success-criteria--verification-plan) | Reconcile actual Task evidence and stale current summaries | WORK-001 | [Task](tasks/tsk-0001-r10-local-remediation.md) | Evidence-to-criterion review and selected document checks |
| WORK-004 | [VAL-R10-004](spec.md#success-criteria--verification-plan) | Appraise Archive readiness and one-use QA consumer retirement | WORK-002, WORK-003 | [Task](tasks/tsk-0001-r10-local-remediation.md) | Closure/hold/consumer review; Archive validator if moved |
| WORK-005 | [VAL-R10-005](spec.md#success-criteria--verification-plan) | Reconcile local/hosted QA and make mandatory hooks fail closed; default pre-commit invokes one staged QA without worktree-writing file hooks | WORK-001 | [Task](tasks/tsk-0001-r10-local-remediation.md) | Hook error/unset, missing tool, recursion/dedup, old/new config projection and affected producer regressions; selected QA |
| WORK-006 | [VAL-R10-006](spec.md#success-criteria--verification-plan) | Review commit/release producer and current remote protection evidence | WORK-001, WORK-005 | [Task](tasks/tsk-0001-r10-local-remediation.md) | Local source tests and dated remote read-only observations |
| WORK-007 | [VAL-R10-007](spec.md#success-criteria--verification-plan) | Repair memory retry, worktree/ref, page-bound and backup safety; separate provider config/hook/sandbox evidence | WORK-001 | [Task](tasks/tsk-0001-r10-local-remediation.md) | Same-key conflict, external symlink, linked-worktree refresh, reconnect and serialized backup failure regressions; actual runtime only when available |
| WORK-008 | [VAL-R10-008](spec.md#success-criteria--verification-plan) | Repair verifier readiness/health/sync, TLS trust or stated bound, unused ESO grant and current readers | WORK-001 | [Task](tasks/tsk-0001-r10-local-remediation.md) | Negative NotReady/unhealthy/OutOfSync cases, TLS and grant/consumer checks, selected render/security checks; live state only from authorized observation |

## Verification Plan

Choose named checks from the affected paths and purpose. For a code or
contract behavior change, reproduce one focused failing case and its passing
repair, then run applicable selected validation on the actual staged index.
For narrative documents, run selected profile, relationship, link and state
checks plus common style. Review final scope and record exact input, result,
limitations and reviewer disposition in the Task. Do not rerun an identical
leaf merely because local delivery advances.

## Risks & Mitigations

- A proposed WGOV change could be misrepresented as approved: leave it pending
  with the common owner and keep the local `candidate` state.
- A completed or held unit could lose evidence during cleanup: require
  consumer-zero, exact source object, current owner and disposition proof
  before any move or removal.
- Static or hosted green results could overstate native or live behavior:
  record each lane with its own input, trust boundary and unresolved owner.
- Sandbox/tool failures could hide a missing check: use supported narrow
  execution approval, preserve the error and classify an unrun result.

## Completion Criteria

Every assigned criterion has one Task acceptance decision supported by
matching concrete evidence and no unresolved required adverse result; changed
owners and consumers pass their selected checks and independent review. Any
remaining protected, common-edition, native or live operation has a named next
owner and a candid `DEFER` boundary. Normal logical commits and their local
integration are reported from actual Git results.
