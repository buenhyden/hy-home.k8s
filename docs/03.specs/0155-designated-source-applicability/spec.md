---
title: "Designated Source Applicability"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0155"
---

# Designated Source Applicability Technical Specification (Spec)

## Overview

This approved change contract closes the three W00 obligations that completed SPEC-0154 did not cover. SPEC-0154 mapped the 109 requirement IDs of the externally supplied v14.2 execution package to current owners; its Task is committed, accepted and complete, so it cannot take new rows. The remaining obligations are the package supplements SUP-01 (lineage of earlier requests and work packages) and SUP-02 (12 designated external sources reviewed from six perspectives), and consolidated requirement USER22-21 (official-source research). The package stays git-ignored evidence, never repository authority. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the governance requirements. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-designated-source-applicability.md) records execution, the result tables and acceptance.

## Strategic Boundaries & Non-goals

- Scope is three survey tables recorded in this package's Task:
  - SUP-02: one row per designated source and perspective (12 × 6 = 72 rows), each with the access level actually achieved, what the source says or why it does not address the perspective, the current repository owner, and a decision.
  - SUP-01: one row per hy-home-k8s legacy work package (52 rows), each linked to the SPEC-0154 crosswalk IDs and current state, plus SHA-256 identities of the preserved history files.
  - USER22-21: one row per official source cited by W00 (RS-09, RS-18, RS-22, RS-39).
- This package changes no policy, validator, test, setting, hook, workflow, manifest or README outside the package, its Stage 03 router and the REQ-0003 back-link. A new gap it finds is handed to its stage owner, not implemented here.
- Not redone: the earlier atomization of the 400-, 409- and 441-line requests, the 168-row crosswalk and the 14,028-pair semantic candidate classification. SUP-01 links and preserves them; it does not re-analyze, certify or close them.
- An external source never decides a repository question. A source recommendation that conflicts with an accepted repository contract is recorded as not adopted with the contract cited.
- No remote push, PR, merge, secret read, cluster access or paid external call. External reading is limited to public pages fetched without personal or repository-identifying data.
- Open question: none that changes a criterion.

## Contracts

- Every SUP-02 row records the access level actually achieved in this revision (direct relevant content, README only, search only, or not retrieved with its error). An unread perspective is UNVERIFIED, never NOT_SPECIFIED or N/A.
- NOT_SPECIFIED requires a stated reason that the source does not address the perspective.
- Every decision is one of ALREADY_COVERED (with the owner cited), REFERENCE_FOR_STAGE (with the stage and SPEC-0154 crosswalk row), NOT_ADOPTED (with the reason or conflicting contract) or UNVERIFIED.
- Every SUP-01 row names its crosswalk IDs and current state (KEEP, DELTA, RETIRED_ALIAS or BLOCKED/UNMAPPED); preserved history files are identified by SHA-256.
- Results live only in this package's Task, as REQ-0003-FR-0019 and FR-0022 require.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance system view, and accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrains disposition; this design changes neither. Three read-only research agents each read four designated sources directly, and a fourth linked the legacy work packages and the official sources. The supervising session merges their rows, checks completeness mechanically and obtains an independent review.

## Data Modeling & Storage Strategy

No persistent data structure is introduced. The three tables are Markdown tables in the Task; their working CSV files stay outside the repository and are identified by SHA-256 in Task evidence. Git history recovers this package after its exit.

## Interfaces & Data Structures

SUP-02 columns: designated ID, source, perspective, access, retrieved, source says, repository owner, decision, stage or crosswalk row, limitation. SUP-01 columns: legacy key, title, crosswalk IDs, repository owner, current state, stage, note. USER22-21 columns: source ID, URL, access, retrieved, claim, repository owner, decision, limitation. These are survey labels, not lifecycle states.

## Edge Cases & Error Handling

- A source that cannot be fetched keeps its rows UNVERIFIED with the error; a search snippet is labelled search only and never treated as the full source.
- A fetch tool that returns a model-written summary rather than verbatim text is recorded as such in the row's limitation.
- A legacy work package with no matching crosswalk row is BLOCKED/UNMAPPED with what is missing, never silently dropped.
- A missing or duplicate designated ID, legacy key or source ID fails the completeness check.

## Failure Modes & Fallback / Human Escalation

If the independent review finds a wrong row, correct it in a new evidence entry and keep the original. A newly found repository gap is handed to its stage owner. A source finding that would change an accepted contract is shown to the user and does not change that contract here.

## Verification Commands

- Completeness: an inline check of the three tables against the package's `DESIGNATED-12x6.csv`, the 52 `hy-home-k8s:` rows of `LEGACY-208.csv` and the four W00 source IDs, plus a negative fixture.
- Document checks: the strict document validators listed in `docs/AGENTS.md`, `python3 scripts/validate-document-lifecycle.py --root . --mode staged`, and the active commit hooks on the exact index.
- Independent read-only review of the tables against the cited sources and owners.

These are repository-static checks. External page contents can change after retrieval; each row keeps its retrieval date.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SRC-001 | The completeness check passes: 72 SUP-02 rows, 52 SUP-01 rows and 4 USER22-21 rows, each ID once, with no empty access, decision or current state; a negative fixture shows each injected defect is detected. |
| VAL-SRC-002 | An independent read-only review finds no blocking error: access levels match what was actually read, NOT_SPECIFIED is never used for an unread perspective, and no source overrides an accepted repository contract. |
| VAL-SRC-003 | Every UNVERIFIED, REFERENCE_FOR_STAGE, DELTA and BLOCKED/UNMAPPED row names a next owner, and any newly found repository gap is handed to a stage owner. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRC-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Completeness check with negative fixture over dated source rows mapped to claims and owners. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRC-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Independent read-only review of access levels and evidence classes. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRC-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Task review of handoffs; no ledger outside the Task. |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRC-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Task review: the source and lineage tables live only in this Task, with no progress ledger or memory entry. |
