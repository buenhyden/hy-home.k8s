---
title: "Survey Status and Local Gaps"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0125"
---

# Survey Status and Local Gaps Technical Specification (Spec)

## Overview

The operator's repository survey specification defines 148 atomic
requirements, CR-01.01 to CR-21.05, and asks under STATE-01 that their status
be derived from evidence and kept in an existing Task rather than a new
ledger. A read-only audit of main `bc7da828` classified every CR. This Spec
records that classification in its Task and closes the small local gaps that
need no operator decision. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-survey-status-and-local-gaps.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the 148-row status table in the Task;
  - local gap fixes: `.gitignore` entries for personal agent files, a memory
    restore test and procedure sentence, provider-note non-adoption lines, a
    corrected `_workspace/diagnostics` README, an SSDF edition check in
    `m0012`, and handoff and research-contract sentences.
- Non-goals:
  - architecture views, a branch-strategy ADR and template prompts, which
    are later slices;
  - adopting any source content, a first release, Archive consumer migration
    or changes in the other three repositories, which need operator decisions
    or other repositories;
  - touching the unregistered folders under `.worktrees/`.

## Contracts

- Each CR has exactly one status: `KEEP` (met, cited), `DONE_THIS_CYCLE`
  (met by a pull request merged 2026-10-20 to 2026-10-27), `GAP`, `PARTIAL`,
  `EXTERNAL` (needs the other repositories, a live system or an operator
  decision) or `PROCESS` (a working-method rule with no static artifact).
- The status is the audit result at `bc7da828`; the disposition column says
  what this Spec fixed and what remains with which next slice or decision.
- No CR is marked met without a citation, and the table is not a new
  permanent ledger: later slices update their own Tasks.

## Core Design

Four read-only reviewers audited CR-01–04, 05–08, 09–14 and 15–21. Their
results were combined, rechecked where a fix depends on them, and corrected
where a claim did not hold: the Claude projection validator already requires
an exact key set, so a `memory:` key is already rejected.

## Data Modeling & Storage Strategy

No stored data. The memory restore uses the existing single backup file.

## Interfaces & Data Structures

- `tests/test_workspace_memory.py`: a restored backup reads the same records.
- `.gitignore`: `CLAUDE.local.md`, `AGENTS.override.md`,
  `.claude/agent-memory/`, `.claude/agent-memory-local/`,
  `.codex/config.local.toml`.

## Edge Cases & Error Handling

- Inserting lines above recorded hashes in `m0012` moves their baseline line
  numbers; the baseline change is committed first, on its own.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request restores every changed file. The status table is
a dated observation; a later slice that changes a CR records it in its own
Task.

## Verification Commands

- `python3 -m unittest tests.test_workspace_memory`.
- `git check-ignore --no-index` for each new ignore entry.
- `python3 scripts/validate-document-lifecycle.py --mode strict`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-CS-001 | The Task lists all 148 CRs once, each with one status, a citation and a disposition, and an independent reviewer confirms a sample against the repository. |
| VAL-CS-002 | The local gap fixes are in place: the new ignore entries match, the restore test passes, and the notes, README and research sentences state only observed facts. |
| VAL-CS-003 | Staged QA passes on every commit and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CS-001 | Status table and independent sample |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CS-002 | Ignore checks and restore test |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CS-003 | Staged QA and hosted checks |
