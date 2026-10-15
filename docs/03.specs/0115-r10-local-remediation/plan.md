---
title: "r10 Local Governance and Delivery Remediation Plan"
version: "0.5.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-16"
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

Execute [SPEC-0115](spec.md) through [Task 0001](tasks/tsk-0001-r10-local-remediation.md)
for completed r10 work, [Task 0002](tasks/tsk-0002-r13-follow-up.md) for the
completed r13 local repair, and
[Task 0003](tasks/tsk-0003-r13-residual-verification.md) for the later bounded
residual verification, and
[Task 0004](tasks/tsk-0004-r13-protection-and-integration.md) for the subsequent
protected remote integration. P01 to P08 are purposes and order, not eight new
packages. Each Task owns only its assigned execution and criterion decisions.
The Task 0003 authorization applied to exact remote and read-only live targets;
the subsequent Task 0004 authorization covers a further exact push, main PR,
CI, reviewed protection decision and conditional merge. Common-edition and
native-sandbox decisions remain with their respective owners.

## Context

The r10 comparison coordinate is `a45da94c9573c2613943c4881f85b80e4dfa65dc`;
actual Git state is re-observed before dependent edits. SPEC-0114 and much of
SPEC-0107 are already completed. Stage 99 records WGOV-CORE 3.0.0 approval,
source verification and C07 local acceptance, while its adapter remains
`candidate`. SPEC-0105 Task 0004 holds pending full-core adoption. The Codex
session observed hook delivery and dummy-variable absence but a failed local
`bwrap` sandbox, so static config is not runtime isolation evidence.

The r13 comparison coordinate is local `main` HEAD
`8488e1098c2eac8c0db469c4eb59457d471575a8` on 2026-10-16, observed
clean before creating `codex/r13-follow-up`. PR #148's dated remote merge is a
separate recorded event. New local checks use the changed source/index input;
the previous accepted r10 receipts are historical evidence only.

The later residual-verification input is local commit
`8d8fa1e54e1032476fb98215747b5d3579a33322`, with an authorized push and
main-targeting draft PR plus two selected read-only live GET verifiers. Their
actual hosted and live outcomes are recorded only in Task 0003; the completed
Task 0002 acceptance is not reopened.

The subsequent integration starts from local commit
`81d76f2d0194505948c3241d2761e90e19ac0429`. The user approved a remote
push, main-targeting PR, CI, protection-setting change if needed and merge
within their reviewed targets. The user clarified that this is a one-person
project, so the existing strict protection may be retained without mutation
while its independent-review HIGH risk remains recorded. Task 0004 records
each actual remote result; prior Task 0003 hosted results applied to
`8d8fa1e5`, not this revision.

## Goals & In-Scope

- Inventory material P01 to P08 findings with exact sources, classifications,
  dispositions and owners, including unchanged and inaccessible candidates.
- Implement confirmed scoped local corrections at existing document, policy,
  validation, CI, provider and GitOps owners with affected consumers.
- Validate each changed logical unit on its actual input and obtain an
  independent read-only review before local delivery.
- Record residual remote, runtime, common-edition and live boundaries without
  promoting their claims from local checks.
- Verify the exact authorized PR's named hosted leaves and two selected live
  checks; record the observed input and output and hand off other lanes without
  widening their assurance.
- Verify the subsequent exact pushed revision, hosted leaves and reviewed
  protection decision; record the user's one-person operation and the
  independent-review gap before any merge, then record an actual integration
  identity only if the protected operation occurs.

## Non-Goals & Out-of-Scope

No new common WGOV approval, four-repository adoption, remote ruleset or
Project mutation, Release publication, live cluster/Vault/backup mutation,
memory-store cleanup, bulk document restyling or Archive move without its
actual closure and disposition prerequisites. Task 0003's authority covered
its exact push, draft PR/CI and two read-only live verifier runs. The subsequent
authority is bounded to Task 0004's reviewed protection and integration target;
it does not authorize weaker protection, self-approval or deployment.

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
| WORK-009 | [VAL-R13-001](spec.md#success-criteria--verification-plan) | Compare r13 candidates with current owners, completed r10 receipts and dated PR #148 evidence; record P01–P08 dispositions | Prior r10 delivery | [Task 0002](tasks/tsk-0002-r13-follow-up.md) | Current Git/source comparison and bounded finding review |
| WORK-010 | [VAL-R13-002](spec.md#success-criteria--verification-plan) | Repair confirmed local source and direct consumers, including QA/CI selectors where their actual inputs change | WORK-009 finding for each affected slice | [Task 0002](tasks/tsk-0002-r13-follow-up.md) | Focused failing/passing behavior, selected checks on changed input, independent review |
| WORK-011 | [VAL-R13-003](spec.md#success-criteria--verification-plan) | Reconcile current documentation, actual delivery, and whole-unit retention; distinguish unobserved common/remote/native/live lanes | Relevant WORK-009/010 results | [Task 0002](tasks/tsk-0002-r13-follow-up.md) | Current-owner/link/lifecycle review, exact Git results and separately dated lane evidence |
| WORK-012 | [VAL-R13-004](spec.md#success-criteria--verification-plan) | Record exact authorized remote delivery and named CI leaves, selected live GET results, and independent residual-lane owner handoff | Completed local commit `8d8fa1e5` and later scoped user authorization | [Task 0003](tasks/tsk-0003-r13-residual-verification.md) | Remote SHA/PR identity and actual `ci-summary`/`style-pr` leaf results; kubeconfig/context-confirmed selected live verifier output; separate DEFER/FAIL boundaries |
| WORK-013 | [VAL-R13-005](spec.md#success-criteria--verification-plan) | Verify the newly authorized exact revision and CI, appraise reviewed protection including a justified no-op for one-person operation, and decide conditional integration with residual HIGH risk explicit | Local `81d76f2d`, subsequent user approval and Task 0003's distinct terminal handoff | [Task 0004](tasks/tsk-0004-r13-protection-and-integration.md) | Remote SHA/PR and named hosted leaves for final head; protection snapshot, no-op rationale or reviewed before/after change, solo decision and actual merge identity if performed |

## Verification Plan

Choose named checks from the affected paths and purpose. For a code or
contract behavior change, reproduce one focused failing case and its passing
repair, then run applicable selected validation on the actual staged index.
For narrative documents, run selected profile, relationship, link and state
checks plus common style. Review final scope and record exact input, result,
limitations and reviewer disposition in the Task. Do not rerun an identical
leaf merely because local delivery advances.

For WORK-012, use the actual remote PR SHA/run and named job/leaf outcomes,
plus the two read-only live verifier results from the explicitly supplied
kubeconfig and verified context. A green API status does not prove deployment of
`8d8fa1e5` or every cluster contract. Keep native startup, common-source,
global-hook and workflow-protection observations in separate lanes with current
owners. A required hosted leaf left unobserved or failed prevents Task 0003
acceptance.

For WORK-013, distinguish the new pushed SHA and hosted run from PR #149's
earlier `8d8fa1e5` run. Record the admin-readable protection snapshot before a
change, reviewed exact setting delta, post-change verification and a bounded
rollback route. If retained unchanged, record the no-op rationale and verify
the effective settings. A configured required context or zero-review rule is
not an independent reviewer; the user's one-person decision leaves that HIGH
risk visible. Keep merge pending until the final head's required hosted leaves,
protection decision and current approval are evidenced; record the resulting
merge SHA and branch state only after execution. A Task 0004 factual closeout
may be delivered by a separate documentation PR; do not make its own merge
receipt a circular prerequisite for VAL-R13-005.

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
