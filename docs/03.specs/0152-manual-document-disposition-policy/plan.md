---
title: "Manual Document Disposition Review Implementation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-10"
layer: "specs"
artifact_id: "SPEC-0152-PLAN-0001"
parent_ids: ["SPEC-0152"]
---

# Manual Document Disposition Review Implementation Plan

## Global Constraints

This approved Plan follows the [approved Spec's boundaries](spec.md#strategic-boundaries--non-goals). No source document is disposed of in this change. The proposed ADR must be reviewed and separately accepted before it becomes durable decision authority. The user's approval of this Spec and Plan authorizes their current contract and local commits, not implementation completion or criterion acceptance.

## Overview

Deliver the current-document disposition policy and manual operating steps under [SPEC-0152](spec.md). [Task 0001](tasks/tsk-0001-manual-document-disposition-policy.md) owns actual results and criterion acceptance.

## Context

[ADR-0053](../../02.architecture/decisions/0053-unvalidated-archive.md) and [ADR-0055](../../02.architecture/decisions/0055-governance-decision-current-state-amendment.md) currently allow Git-history-only recovery without a per-disposition proof record. Proposed [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) narrows that condition. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) is the structure owner. The user's later narrow contract authorization adds only conditional first-record Spec/Plan approval validation, with receipt and exact-byte review at the existing Task and Stage 99 owners. Existing completed decisions and evidence are dated records, not inputs to rewrite.

### Deferred Roadmap

The following stages are future work, outside WORK-001. Each begins only after a concrete difference and owner are confirmed; the other repositories and unretrieved external sources are not universal prerequisites.

| Order | Scope | Next deliverable |
| --- | --- | --- |
| 1 | W00–W01 | Link requirement-level current owners, evidence and differences in existing work records; keep satisfied contracts. |
| 2 | W02 follow-up | Use actual manual disposition results to design a narrow deletion-event check; do not restore archive-wide or one-time cutover gates. |
| 3 | W03–W04 | Repair only observed profile, language, state and traceability gaps; preserve accepted SPEC-0149–0151 and numbering. |
| 4 | W05–W06 | Compare check callers, unique guarantees, Git and release ownership; retain the existing exit-zero-with-FAIL and missing-PASS refusals. |
| 5 | W07 and W09 | Review current settings, role projections and seven workspace READMEs; gather separate runtime evidence for Codex instruction delivery and Claude compaction/resume. |
| 6 | W08 | Design a hard total memory-capacity bound and selective retrieval; identify actual access and revocation actors before deciding their controls. |
| 7 | W10–W11 | Correct root README guidance for token input, optional PostgreSQL and required Valkey; connect quality targets to actual Argo CD sync and recovery observations. |

## Goals & In-Scope

- State manual disposition preconditions and recovery evidence at the current lifecycle owner.
- Align authoring and SDLC guidance, REQ-0003, the reference runbook and current navigation with the ADR's scoped decision.
- Translate remaining Korean prose under `.agents/governance/` to English and align the agent-language boundary there with the author's language guidance.
- Record the scoped first-record Spec/Plan approval in the existing Task after independent review of exact approved parent bytes, and validate its narrow Stage 99/lifecycle exception with focused positive and negative cases.
- Validate changed documents and report static, review and acceptance states separately.

## Non-Goals & Out-of-Scope

- No actual deletion, move, historical restoration or retroactive acceptance.
- No archive catalog, ledger, archive-disposition schema or gate, CI or unrelated code change. The narrow first-record approval marker, lifecycle reader and focused regressions are in scope.
- No native provider or live environment claim.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DISP-001](spec.md#success-criteria--verification-plan), [VAL-DISP-002](spec.md#success-criteria--verification-plan), [VAL-DISP-003](spec.md#success-criteria--verification-plan) | Draft scoped ADR; update current policy, requirement, runbook and navigation; add the conditional initial approval reader and receipt; review the resulting diff. | Current REQ-0003 and AD-0006; proposed ADR reviewed before acceptance; actual user approval and final-byte independent review for the new parent pair. | [Task 0001](tasks/tsk-0001-manual-document-disposition-policy.md) | Selected document QA, focused receipt regressions, manual contradiction review and independent semantic review. |

## Verification Plan

Inspect `git diff --check` and the final changed paths. Run `python3 scripts/qa.py quick` for changed working-tree bytes and focused document-contract tests for the first-record exception. Inspect the exact staged index and let the active hook run staged QA before the authorized local commit. Review a held document, a missing source object, a byte mismatch and invalid approval receipts as negative scenarios. Record each observed result under Task 0001. No static check can certify a future operator's actual disposition or authenticate the chat approval source.

## Risks & Mitigations

- Policy language could imply an automatic archive gate; compare the final text with ADR-0053's retained unvalidated archive boundary.
- A new procedure could imply past deletions were invalid; scope it to future dispositions of current documents and preserve dated history.
- The proposed ADR could be mistaken for accepted authority; retain its proposed status and record review and acceptance separately.
- A first-record approval receipt could overstate user consent; bind separate user approval and independent review to exact Spec/Plan bytes, and keep Task criterion and ADR acceptance pending.

## Completion Criteria

Each Spec criterion has an accepted verdict with applicable PASS evidence, no unresolved required failure, and an independent review without blocking findings. The approved ADR and current durable owners contain the accepted rule. Task 0001 records final scope, snapshot, rollback and next owner. Repository-static evidence does not satisfy remote or live observation.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Manual current-document disposition preconditions and Git recovery proof | [Document Lifecycle Policy](../../../.agents/governance/document-lifecycle.md) | Current Contract |
| Reference disposition steps | [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md) | Procedure and Recovery and Escalation |
