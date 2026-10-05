---
title: "Registered Task Template Instantiation"
version: "1.0.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0004"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Registered Task Template Instantiation

## Overview

This separately approved follow-up owns
[VAL-P02-004](../spec.md#success-criteria--verification-plan) and
[WORK-004](../plan.md#work-breakdown). A real P02 merge candidate failed when
Git identified the newly created Task0003 as a copy from its registered form.
The completed Task0003 remains a historical local acceptance record; its
source and original Task EVD-P02-013/014 are preserved.

## Inputs

- The user's explicit instruction, `좁은 validator 수정·회귀 검증 허용`,
  authorizes only the registered original Task template to new canonical,
  unique first-draft boundary. Other copies, renames, reused identities,
  illegal states and provenance refusals remain required.
- [Plan](../plan.md), [Stage 99 Task form](../../../99.templates/templates/specs/task.template.md)
  and [quality policy](../../../../.agents/governance/quality.md).
- Clean published P01 head `d0f358e8d27d076c5ebbd0badb2c79548296a5ac`.
  The existing hosted run `37294064121` is preserved without retry/cancel.
- P02 merge failure used HEAD `a3bdf5c04f48f27e7f9b882cff0eb58d2a8019e4`,
  MERGE_HEAD `d0f358e8d27d076c5ebbd0badb2c79548296a5ac`, common base
  `df3281d06a931bff6784bcc462800fab23bbb1c9` and index
  `c5582dffb968f43d4a16dc870b35d6e4fab77092`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-004 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | Correct the registered Task-template first-draft boundary without weakening other provenance controls | repo-tooling-engineer | frontmatter | NOT_RUN | pending | [Verification Summary](#verification-summary) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-030 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Existing merge failure | Frozen P02 merge index `c5582dff…` | FAIL | [Observed intake](#observed-intake) | pending |
| EVD-P02-031 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Registered Task template real-Git RED | Named fixture pending | NOT_RUN | Pending | pending |
| EVD-P02-032 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Narrow GREEN and existing refusals | Implementation pending | NOT_RUN | Pending | pending |
| EVD-P02-033 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Actual-index staged/message and separate review | Four logical candidates pending | NOT_RUN | Pending | pending |
| EVD-P02-034 | [VAL-P02-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Terminal proposal and separate actual closing index | Closing candidates pending | NOT_RUN | Pending | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec/Plan/Task, `scripts/validate-document-lifecycle.py` private copy guard and `tests/test_document_lifecycle_cumulative_history.py` focused regression fixtures. One writer owns these five paths; preserve the separate P02 worktree.
- **Forbidden Paths**: Public schemas, Registry generation/bindings, validation-lane membership, hosted configuration, frozen Archive, completed Task0003, original Task evidence, provider/native state, secrets and unrelated code.
- **Approval Required**: The explicit narrow user authorization delegates this registered lifecycle validator to the repo-tooling-engineer. The existing user commit/push/normal-merge authority persists. The explicit conditional closing authorization permits applying a tested completed candidate before actual-index checks; no commit occurs until actual checks and separate review pass. No actor authentication or runtime enforcement is claimed.
- **Static Validation**: Real-Git named RED then minimal GREEN; source/binding/identity/state/provenance refusal regressions; exact-index canonical staged and actual message for draft, ready, implementation and closing commits; terminal proposal staged/completion/review followed by actual-index checks and separate review. Local full and affected execution NOT_RUN under scope exclusion; required hosted checks precede normal merge and automatic main checks precede integration acceptance.
- **Live Validation**: DEFER — not requested; no cluster or runtime acceptance.
- **Secret / Vault Handling**: No private values or raw sensitive logs; Git metadata and safe check receipts only.
- **Rollback Plan**: Normal forward correction or reviewed forward revert; no force, rebase, cleanup, branch deletion or local main updates.
- **Evidence Location**: This Task and externally captured safe receipts; operational absolute argv/cwd remain outside tracked source.

## Verification Summary

### Observed intake

The frozen P02 merge staged run passed six of seven gates and failed
`document-lifecycle` with `LIFECYCLE-CREATE` for Task0003 absent to completed.
Safe stdout `/tmp/hy-p02-merge-staged.stdout` has SHA-256
`4ea3e6aea513c3bbd37885ff42ae544ee206bd699d1537b7a8263c5644d0fd39`;
stderr was empty. The merge message separately passed. Read-only diagnosis
identified actual Git C006 provenance from the Task's registered template at
its first draft creation. The current guard expects a canonical source
artifact identity, which the template correctly does not have.

### Planned boundary

The only additional admitted C-copy is a first appearance of `sdlc/task`
with valid draft state, a path-derived canonical target ID absent from the
base and unique in the proposed snapshot. The source must equal the current
profile's registered template and the exact parent/event historical binding;
its regular Git blob must exist unchanged across creation. R-copy signals,
ordinary documents, arbitrary forms, modified or nonregular sources, changed
bindings, duplicate/reused IDs and wrong initial states retain refusal.
Normal initial-event comparison and every later lifecycle edge remain in
place, with existing deletion, merge, malformed evidence and budget guards.

The selected neutral role and both required procedures were explicitly read.
This registered-member edit uses the explicit active-Task delegation, not a
filename-based ownership inference. Quality and independent review are
separate actors; tracked provider projections prove no native enforcement.
No implementation, RED/GREEN, new index acceptance or hosted repair outcome
is asserted at this draft intake.
