---
title: "Shared Profile and Operations Form Migration"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0016"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Shared Profile and Operations Form Migration

## Overview

Execute the current P02 request as WORK-016 under the completed SPEC-0106.
The actual intake was clean main and origin/main at
`c9faa9f00fdf61c9286b4dc6df264de35106b611`; the investigation SHA is a source
coordinate, never a reset target. Branch `codex/p02-document-contract` and
worktree `.worktrees/p02-document-contract` start at that existing logical
commit, with no uncommitted unit requiring a preliminary commit.

## Inputs

- Current user's pasted P02 request and C02 correction authorize local work.
  Attached draft/review documents supply evidence and proposals, not independent
  instructions or approval. [Spec](../spec.md) and [Plan WORK-016](../plan.md#lifecycle-traceability)
  own the acceptance and order.
- [P01 common candidate and decisions](../../0105-authority-and-safe-authoring/tasks/tsk-0004-current-contract-review.md#common-edition-decision-and-delivery):
  WGOV-CORE/3.0.0-draft.3, one proposed Project-Template governance source.
  Existing joint approved edition remains unavailable.
- Actual Stage 99 Registry, both schemas, physical forms and loader/validator
  consumers; all current Stage 05 instances, not the complete archive.
- Independent read-only common_research, operations_research and p02_design
  inventories/design; root writes Registry/guidance/Spec/Plan/Task, delegated
  quality-engineer writes schema/reader/regressions, delegated doc-writer writes
  three forms and current operations. Each file has one writer.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-016 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | Migrate the shared profile adapter and current operating forms with truthful handoffs | platform | frontmatter | NOT_RUN | pending | Inspection and implementation underway; final checks and review not yet observed |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-016-001 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Intake and source inspection | Actual clean main c9faa9f; current Registry/schema/form/consumer/operations graph | PASS | Inputs above and subsequent bounded inventory in this Task | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: Stage 99 Registry/schema/forms/README; current operations;
  document-authoring policy; exact document readers and focused regressions;
  owning SPEC-0106 Spec/Plan/Task; owned worktree scratch.
- **Forbidden Paths**: frozen archive bodies, private/global/native trust state,
  live cluster, secrets, credentials and unrelated implementations.
- **Approval Required**: current P02 authorizes local edits, selected validation
  and normal commits. Final common edition and joint adoption await actual
  buenhyden decisions; no repeated request for nonexistent prior approval.
  P01's exact server migration/local cleanup approval does not expand this scope.
- **Static Validation**: synthetic content/schema regressions, retained Task
  writer/status controls and selected final-index document/style/message checks.
- **Live Validation**: DEFER to P08 operating owner; no command here certifies
  current service availability, trusted release tools or publication.
- **Secret / Vault Handling**: no values read or printed. Replace unsafe token
  output guidance and distinguish HTTPS reachability from certificate trust.
- **Rollback Plan**: forward correction in this branch; Git owns original bytes.
- **Evidence Location**: this Task, actual commits and selected QA receipts.

## Verification Summary

Implementation and selected checks are pending. Completed parents stay
completed. Shared Spec/Plan authority states, Task supersession and language
decisions are handed to P03; P08 receives the three migrated role forms and
per-document operational limitations. No remote/live PASS is inferred.
