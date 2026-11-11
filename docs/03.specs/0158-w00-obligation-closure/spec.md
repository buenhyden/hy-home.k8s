---
title: "W00 Obligation Closure"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0158"
---

# W00 Obligation Closure Technical Specification (Spec)

## Overview

This approved change contract closes the W00 obligations of the externally supplied v14.2 execution package that completed SPEC-0154 and SPEC-0155 did not record. The package stays git-ignored evidence and never repository authority. A re-check of both committed W00 Tasks against every section of the W00 prompt found five open items: links for 21 of the 22 consolidated user requirements (USER22), the table of related pull requests, four untested negative cases, the dispositions of the carried-over open items OPEN-01 to OPEN-07, and a per-file read inventory. It also found six files handed to more than one stage, while the prompt requires one writer per file. This package records all of them. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the governance requirements. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-w00-obligation-closure.md) records the tables, evidence and acceptance.

## Strategic Boundaries & Non-goals

- Scope is six tables in this package's Task: the 22 USER22 links, the related pull-request table (#219–#222), the negative-case results, the primary writer for each file handed to several stages, the OPEN-item dispositions, and the inventory of the 85 tracked files cited as owners in the W00 tables.
- This package changes no policy, validator, test, setting, hook, workflow or manifest. Gaps stay with their stage owners; the writer table assigns ownership and does not edit those files.
- The earlier 1,250-line atomization and the 14,028-pair classification are not reopened; their preservation is recorded as a disposition, not certified.
- The inventory covers files cited as owners only, by the user's decision; a whole-tree inventory is not selected.
- The negative cases run only on disposable copies outside the repository or on recorded evidence; no repository file is altered to test them.
- No remote push, PR, merge, package exit, secret read or cluster access.
- Open question: none.

## Contracts

- Every USER22 item 01–22 appears once with its package source, the package requirement IDs that carry it, the SPEC-0154/0155/0156 rows, a current state (COVERED, OPEN, REJECTED_BY_CONTRACT or UNMAPPED) and a stage owner when not covered.
- The pull-request table records only what was read: metadata, changed-file count, checks and reviews. A diff that was not reviewed is labelled so.
- Each negative case records the unchanged input first passing and the injected fault being detected, with the check that detected it.
- Each file handed to several stages gets exactly one primary writer; the other stages are interface consumers.
- Each OPEN item names its disposition and the package closing condition it was judged against; BLOCKED and not-certified items are never reported as complete.
- Results live only in this Task, as REQ-0003-FR-0019 and FR-0022 require.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance system view and accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrains disposition; this design changes neither. A read-only agent linked the USER22 items; the supervising session collected the pull-request data, ran the negative cases, built the inventory and judged the OPEN items. Primary writers follow each stage's main writing scope as the package defines it.

## Data Modeling & Storage Strategy

No data structure changes. Working CSV files and the single-use checker stay in the session scratchpad and are identified by SHA-256 in Task evidence.

## Interfaces & Data Structures

No interface changes. Table columns are listed in the Task; their values are survey labels, not lifecycle states.

## Edge Cases & Error Handling

- A cited file that changed after the evidence HEAD is listed as changed since, and is judged before its row is reused.
- An injected fault that is not detected is recorded as a finding, not hidden.
- A USER22 item whose only carrying rule is a rejected clause is REJECTED_BY_CONTRACT; one that also has other open rows stays OPEN.

## Failure Modes & Fallback / Human Escalation

If the independent review finds a wrong row, correct it in a new evidence entry and keep the original. A newly found conflict with an accepted contract is shown to the user and does not change that contract here.

## Verification Commands

- Completeness: an inline check that the USER22 table has items 01–22 once each, every OPEN or UNMAPPED item names a stage, every OPEN item a disposition, and every inventory path is tracked; a negative copy is detected.
- The negative cases as recorded in the Task, with their commands and results.
- The strict document validators, the staged lifecycle check and the active commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-CLOSE-001 | The completeness check passes on all six tables and detects a negative copy. |
| VAL-CLOSE-002 | The four negative cases each show the unchanged input passing and the injected fault detected; the duplicate-writer finding has a primary-writer table. |
| VAL-CLOSE-003 | An independent read-only review finds no blocking error in the USER22 links, OPEN dispositions and writer assignments, and the strict document checks and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CLOSE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Completeness check with a negative copy over dated tables. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CLOSE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct negative cases on disposable copies and recorded evidence. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CLOSE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Independent review; strict document checks and commit hooks. |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CLOSE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Task review: the tables live only in this Task, with no ledger. |
