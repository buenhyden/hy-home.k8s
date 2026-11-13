---
title: "W00 v14.7 Delta Intake"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
artifact_id: "SPEC-0161"
---

# W00 v14.7 Delta Intake Technical Specification (Spec)

## Overview

This approved change contract records stage W00 of the externally supplied v14.7 execution package against this workspace. The package stays git-ignored evidence and never repository authority. Completed SPEC-0154, SPEC-0155, SPEC-0156 and SPEC-0158 already recorded W00 for package v14.2. The original input report is byte-identical in v14.7, and so are the 106 requirement IDs and the profile requirements. This package records only what changed since v14.2:

- the implementation or verification text of 16 requirement rows (18 field changes);
- clauses R45-01 to R45-12 (v14.5) and R147-01 to R147-20 (v14.7);
- three new contracts: common H2/H3 document forms (COMMON-DOC-FORM-1), stage QA placement (QA-STAGES-1) and the QA change protocol;
- the dispositions of the historical OPEN-08 to OPEN-14 identifiers, which SPEC-0158 did not judge.

For each change it names the current owner file, the difference, the primary writer stage and the open decisions. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the governance requirements. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-w00-v14-7-delta-intake.md) records the tables, evidence and acceptance.

## Strategic Boundaries & Non-goals

- Scope is the delta tables in this package's Task: edition delta, requirement-change links, related pull requests #220–#227, the document-form and stage-QA handoff tables, the OPEN-01..14 dispositions, conflicts, and the read denominator for the files those tables cite plus every tracked file under `scripts/`, `tests/`, `scripts/githooks/` and `.github/workflows/`.
- Outside this package it changes only the Stage 03 README, one back-link sentence in REQ-0003 Traceability and, if the secret scan flags them, `.secrets.baseline` entries for this Task's reviewed digests. It changes no policy, registry, template, validator, test, hook, workflow or manifest. Each gap stays with its stage writer (W01 to W07, W10); this package names the writer and the exact files.
- The 1,250-line atomization, the 14,028-pair classification and the 208 legacy packages are not reopened; SPEC-0158 dispositions are reused unless a newer observation changes them.
- A clause that conflicts with an accepted requirement and has a same-scope user decision reuses that decision and is not asked again.
- No remote push, PR, merge, package exit, secret read or cluster access.
- Open question: none for this package. The hosted-CI QA scope conflict in the Task is a W01 decision and does not change a criterion here.

## Contracts

- Every changed requirement row, R45 clause and R147 clause appears once with its package source, the current owner file, a state (COVERED, OPEN, REJECTED_BY_CONTRACT or DECISION_NEEDED) and a stage writer when not covered.
- Every file named in a handoff row has exactly one primary writer stage in the Task's Primary Writers table; other stages are interface consumers.
- Every OPEN-01..14 identifier gets one of the package verdicts (UNVERIFIED, RESIDUAL_CONFIRMED, CLOSED_BY_EVIDENCE, SUPERSEDED, NOT_APPLICABLE, BLOCKED_EVIDENCE) with its basis. The identifier is not a current state.
- The read denominator distinguishes read, partial and listed-only files. A listed-only file is never reported as semantically reviewed.
- Results live only in this Task, as REQ-0003-FR-0019 and FR-0022 require.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance system view and accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrains disposition; this design changes neither. Two read-only agents surveyed the document-form and stage-QA differences; the supervising session compared package editions, collected pull-request data and judged the OPEN items.

## Data Modeling & Storage Strategy

No data structure changes. Extracted earlier package editions stay in the session scratchpad and are identified by SHA-256 in Task evidence.

## Interfaces & Data Structures

No interface changes. Table values are survey labels, not lifecycle states.

## Edge Cases & Error Handling

- The exact v14.2 `REQUIREMENTS.json` (SHA-256 prefix `8af753f1`) is not in the package history; the delta is taken from v14.1, the nearest preserved earlier edition, and the Task says so.
- A cited file that changes after the evidence HEAD is judged again before its row is reused.
- A clause carried only by a rejected rule is REJECTED_BY_CONTRACT.

## Failure Modes & Fallback / Human Escalation

If the independent review finds a wrong row, correct it in a new evidence entry and keep the original. A newly found conflict with an accepted contract is shown to the user and does not change that contract here.

## Verification Commands

- Completeness: an inline check that every changed row, R45 and R147 clause and OPEN-01..14 identifier appears exactly once with a state, that every non-covered row names a writer stage, and that every cited path is tracked; a negative copy is detected.
- The strict document validators, the staged lifecycle check and the active commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-DELTA-001 | The completeness check passes on all tables and detects a negative copy. |
| VAL-DELTA-002 | An independent read-only review finds no blocking error in the change links, handoff writers and OPEN dispositions, and the strict document checks and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DELTA-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Completeness check with a negative copy over dated tables. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DELTA-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Independent review; strict document checks and commit hooks. |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DELTA-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Task review: the tables live only in this Task, with no ledger. |
