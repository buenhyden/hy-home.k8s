---
title: "Single-Maintainer Review Path Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0162-PLAN-0001"
parent_ids: ["SPEC-0162"]
---

# Single-Maintainer Review Path Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds one constraint: only the files named in the Spec scope, this package and the Stage 03 README change.

## Overview

Replace the mandatory agent review with the GIT-09 checklist path in the quality, Git, work-lifecycle and document-lifecycle policies and in REQ-0003 FR-0018. [Task 0001](tasks/tsk-0001-single-maintainer-review-path.md) owns execution and evidence.

## Context

The user adopted GIT-09 on 2026-11-12 (SPEC-0161 EVD-018). This branch continues `claude/w00-v14-7-intake` after `af7484ec`. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0052](../../02.architecture/decisions/0052-single-main-trunk-branch-strategy.md) constrain the design; no ADR, interface or validator changes.

## Goals & In-Scope

- Rewrite the quality policy's Semantic review section, Pull request row and handoff reviewer field, and the Stage 03 role row.
- Update the Git policy's pull-request completion, the work lifecycle's Completion step 1 and the document lifecycle's first-record review row wording.
- Amend REQ-0003 FR-0018, its Traceability row, its Evaluation Expectation and the rejected-clause sentence.

## Non-Goals & Out-of-Scope

- Validators, tests, hooks, workflows, registry and templates.
- The other adopted conflicts (DOC-09, CI-SCOPE, DOC-12) and the Repository Vocabulary.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REVIEW-001](spec.md#success-criteria--verification-plan), [VAL-REVIEW-002](spec.md#success-criteria--verification-plan) | Edit the six owners, search for remaining agent-review obligations, record the checklist review. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-single-maintainer-review-path.md) | Repository search, owner checklist, strict document checks and commit hooks. |

## Verification Plan

- Search current owners for agent-review obligations; each remaining hit is optional or historical.
- Record the risk class (`high`: pull-request completion and merge-direction wording) and the core-diff checklist, including recovery, in the Task.
- Run the strict document checks, the staged lifecycle check and the commit hooks on the exact index.
- Architecture compliance: confirm no AD or ADR file changed.

## Risks & Mitigations

- **A hidden owner keeps requiring an agent reviewer.** Mitigation: the repository search covers all instruction surfaces, and the Task lists each hit.
- **Weaker review.** Mitigation: the checklist names the same meaning checks the agent review covered, and `BLOCK` still blocks.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Single-maintainer review path | [Quality policy](../../../.agents/governance/quality.md) | Semantic review |
