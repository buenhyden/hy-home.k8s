---
title: "Task Table Row Width"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0148"
---

# Task Table Row Width Technical Specification (Spec)

## Overview

AUD-0001 finding F-07: a Task whose Task Table held a nine-cell evidence row
passed every strict check. On 2026-11-06 the operator asked to review F-07
and proceed. A validator behavior change needs this package. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-task-table-row-width.md) records it.

## Strategic Boundaries & Non-goals

- In scope: `scripts/validate-markdown-profiles.py` body-contract table
  checks and a focused regression in `tests/test_task_execution_contract.py`.
- Non-goals: changing the work-item ID pattern (`EVD-004` is a valid ID
  shape), the registry, any other validator, or the Stage 03 history of
  SPEC-0146.
- Open questions: none that change a criterion.

## Contracts

- A row in any body-contract Lifecycle Traceability table whose cell count
  differs from the header is refused with `BODY-CONTRACT-ROW-WIDTH`.
- The Task contract check is no longer skipped without a diagnostic: a
  mismatched row now produces that diagnostic.
- Every current document still passes the strict checks.

## Core Design

Root cause: `_body_contract_diagnostics` pads or truncates each row to the
header width without a finding, and the Task acceptance-graph check runs only
when every row already has the header width. One nine-cell row therefore
disabled the Task status, result and evidence checks silently. The fix adds
one width diagnostic in the shared table check, so every caller fails
closed. Constraining architecture: [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) assigns document-form enforcement
to the validators that consume the Stage 99 registry.

## Data Modeling & Storage Strategy

No data or schema changes.

## Interfaces & Data Structures

One new diagnostic rule ID, `BODY-CONTRACT-ROW-WIDTH`, in the existing
text and JSON output of `validate-markdown-profiles.py`.

## Edge Cases & Error Handling

- Normal: rows with the header width produce no new finding.
- Error: a wider or narrower row is refused with its row number and widths.
- Boundary: a row that is too short also keeps its existing
  `BODY-CONTRACT-CELL` finding for the missing cells.

## Failure Modes & Fallback / Human Escalation

If a current document fails after the change, it held a malformed row that
was previously hidden; fix that document rather than relax the check.
Rollback is reverting the implementing commit.

## Verification Commands

- `python3 -m unittest tests.test_task_execution_contract`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-ROW-001 | A focused test fails before and passes after the fix: a nine-cell Task Table row is refused with `BODY-CONTRACT-ROW-WIDTH` |
| VAL-ROW-002 | Strict document checks and the document and Task-contract unit tests PASS on every current document |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ROW-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused test red then green |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ROW-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict checks and unit tests |
