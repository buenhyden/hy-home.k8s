---
title: "Refresh External Workspace Engineering Research"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0099-TSK-0001"
---

# Task: Refresh External Workspace Engineering Research

## Overview

Single execution evidence owner for external research refresh, document integration, ordered validation and local commits under the direct user request dated 2026-09-27. This initial queued record establishes the approved boundary; it does not claim research or QA completion.

## Inputs

- [Spec](../spec.md) and [Plan](../plan.md).
- [Existing research pack](../../../90.references/research/0001-workspace-engineering/README.md); origin/main baseline `fc469fd139e6b92d98cc8aabeb3f3e7141f18a54`.
- User attachment requesting the hy-home.k8s external research refresh and single Research Pack maintenance, including U01–U39, topic detail, source contracts and retained branch/worktree finish selection.
- Current Stage 99 profiles/forms and common authoring, lifecycle, quality, Git and delegation procedures. These are authoring inputs, not targets of a conformance audit.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-WER-001 | Establish canonical execution scope and routing | integration owner | Queued | Filled initial contract; bootstrap validation/commit pending | Spec, Plan, Stage 03 routing |
| WORK-002 | VAL-WER-002, VAL-WER-003 | Research topic details using primary external sources | researchers | Queued | Findings not integrated | Assigned m0001–m0011 evidence |
| WORK-003 | VAL-WER-001, VAL-WER-003, VAL-WER-005 | Author member bodies after source handoff | doc writers | Queued | No completion claimed | Member source records and dispositions |
| WORK-004 | VAL-WER-002, VAL-WER-004, VAL-WER-005 | Integrate U coverage, scope questions and navigation | integration owner | Queued | Reconciliation pending | README, m0012 and m0013 |
| WORK-005 | VAL-WER-006 | Review and validate each coherent local commit | independent reviewer / integration owner | Queued | Required evidence pending | Exact snapshot command results and Git |
| WORK-006 | VAL-WER-006 | Close acceptance and preserve branch/worktree handoff | integration owner | Queued | Final full and handoff pending | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/90.references/research/0001-workspace-engineering/**`; `docs/90.references/research/README.md` and `docs/90.references/README.md` only when navigation changes; `docs/03.specs/0099-workspace-engineering-research-refresh/spec.md`, `plan.md`, `tasks/tsk-0001-refresh-external-research.md`; `docs/03.specs/README.md` solely for the new package route. Exact additional active link consumers require advance path/reason disclosure.
- **Forbidden Paths**: all policy/provider/agent/skill/hook/CI, infrastructure, application, manifest, script, test, template and validator changes; `docs/98.archive/**`; the separate research pack and any parallel authoring/ledger tree.
- **Approval Required**: direct user request already authorizes bounded research/edit/local commits. Scope expansion, runtime investigation, secret access, external state writes, push, PR, merge, history rewrite, destructive cleanup and branch/worktree removal are outside this authorization.
- **Static Validation**: targeted profile/link/lifecycle and scope review → quick affected working tree → every logical exact-index staged check and actual-message validation → final full. Commands and precise snapshots are recorded below when run; no assumed PASS.
- **Live Validation**: DEFER — workspace/provider-runtime/hosted CI/live investigations are excluded. All workspace research results are `not observed in this cycle`.
- **Secret / Vault Handling**: no private config, logs, memory, authentication or secret collection; no Vault/live contact.
- **Rollback Plan**: preserve branch/worktree; inspect exact branch-owned paths and reverse selected logical commits through reviewed forward commits, preserving unrelated work. No reset, amend, rebase or blanket clean.
- **Evidence Location**: this Task for execution; m0012 for source/claim/U mapping and dispositions; m0013 for follow-up scope questions; Git for committed recovery.

### Authorization and structure rulings

Exact execution-management paths and routing reason were disclosed before writes. Direct user authorization supplies the scoped approval; no new approval stop is inferred. Repository lifecycle overrides external skill suggestions for `docs/superpowers/` or duplicate ledgers. Existing pack and all thirteen member identities are retained. Research source assessment and document authoring remain separate responsibilities; integration owns shared IDs/navigation/coverage and commits. No current workspace verdict is derived from historical pack evidence or document QA. Git policy lookup identified an effective user-global hook directory; no private configuration contents were inspected or changed. The integration owner will validate the actual message with pinned pre-commit Commitizen before normal Git commit, preserving active hooks.

## Verification Summary

| Lane / step | Snapshot and result | Limitation / next owner |
| --- | --- | --- |
| Baseline | Origin/main `fc469fd139e6b92d98cc8aabeb3f3e7141f18a54`; branch `codex/research-refresh` in isolated research worktree | Original checkout/index preserved; integration owner records tool results |
| Targeted baseline | PASS — all 14 unchanged pack Markdown files at base fc469fd139e6b92d98cc8aabeb3f3e7141f18a54; validation runner affected lane with NUL-delimited target list | Six selected gates passed; integration owner holds command log. New package checks remain separate |
| Acceptance baseline | Expected RED — read-only individual-table-row check found all U01–U39 rows absent from m0012 at the base | Diagnostic process exited 0; this is unmet requested coverage, not a failed document-format gate. Final mapping/source/question review must prove GREEN |
| Quick | Pending | Affected working-tree QA not yet recorded |
| Staged / message | Pending | No commit SHA or validated index claimed |
| Final full | Pending | Full includes unit discovery and manual all-files pre-commit once |
| Independent review | Pending | Reviewer and disposition must be recorded before completion |
| Hosted CI / provider-runtime / live | DEFER — excluded by user scope | No observed implementation outcome |

Final handoff must record actual baseline/branch, adopted structure, changed documents and reasons, U coverage, major external corrections and unresolved conflicts, scope question entrypoints, exact command/snapshot outcomes and limitations, reviewer identity/disposition, commit SHA/content list, final Git status, bounded rollback, residual research risks and next owner. Initial authoring is not the final handoff. Do not insert a self-referential final SHA or repeat full QA merely to rewrite timing metadata.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WP-001](../plan.md#work-breakdown) | Bootstrap documentation prepared; verification pending | [VAL-WER-001](../spec.md#success-criteria--verification-plan) |
| [WP-002](../plan.md#work-breakdown) | Research handoff pending | [VAL-WER-002](../spec.md#success-criteria--verification-plan), VAL-WER-003 |
| [WP-003](../plan.md#work-breakdown) | Authoring pending | [VAL-WER-003](../spec.md#success-criteria--verification-plan), VAL-WER-005 |
| [WP-004](../plan.md#work-breakdown) | Integration pending | [VAL-WER-004](../spec.md#success-criteria--verification-plan), VAL-WER-002, VAL-WER-005 |
| [WP-005](../plan.md#work-breakdown) | Required QA/review/commits pending | [VAL-WER-006](../spec.md#success-criteria--verification-plan) |
| [WP-006](../plan.md#work-breakdown) | Final acceptance/handoff pending | [VAL-WER-006](../spec.md#success-criteria--verification-plan) |
