---
title: "W01 3.0.1 Follow-up Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "in-review"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0218-PLAN-0001"
parent_ids: ["SPEC-0218"]
---

# W01 3.0.1 Follow-up Implementation Plan

## Overview

### Goal and Boundary

This Plan executes [SPEC-0218](spec.md). When it is complete:

- the skill-authority, progress-ledger and intake rules each have one author;
- the provider note and two role bodies link to their canon;
- the vocabulary form matches the glossary;
- the SPEC-0161 Task holds the follow-up record.

Everything the Spec assigns to later stages is excluded.

#### Global Constraints

Every work unit inherits the constraints of the approved [Spec](spec.md). Additional constraints:

- Each edit replaces restated text with a link and keeps native facts.
- The validators give equal results before and after, apart from the intended fixes.

### Assumptions

- `main` is `c0af5a76`, and the ledger holds 57 entries.
- No script or test pins the skill-authority sentence, the progress-ledger sentences or the vocabulary template text. A search found only stale `.pyc` files.
- Role projections under `.claude/agents/` and `.codex/agents/` are checked by the governance validator.

## Dependencies

### Prerequisites

- Spec and Plan approval with an independent review.
- The one-time run of the named evidence checks (started on `c0af5a76`).

### Dependency Order

WORK-001 (one canon) and WORK-002 (vocabulary form) are independent. WORK-003 (record) runs after both and after the evidence run.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W01F-001](spec.md#criteria) | EXEC-R005 canon sentence; EXEC-R001 link; skill, `AGENTS.md`, workflow, skill-ledger, provider-note and role-body links. | Approval | [Task 0001](tasks/tsk-0001-w01-followup.md) | Governance, profile and link validators. |
| WORK-002 | [VAL-W01F-002](spec.md#criteria) | Registry vocabulary meaning and template to the link form. | Approval | [Task 0001](tasks/tsk-0001-w01-followup.md) | Contract registry, `document` contract tests, links. |
| WORK-003 | [VAL-W01F-003](spec.md#criteria) | Append the `W01 Follow-up Record` and one EVD row to the SPEC-0161 Task. | WORK-001, WORK-002, evidence run | [Task 0001](tasks/tsk-0001-w01-followup.md) | Ledger gate; strict validators. |

### Change and Rollback

Each work unit is a text edit. Undo by deleting the branch, or by reverting the merge commit after merge.

## Verification Plan

### Verification Matrix

| Work Unit | Check | Lane |
| --- | --- | --- |
| WORK-001 | `validate-agent-governance.py`; markdown profiles; links and owners | local static |
| WORK-002 | contract registry; `run-contract-tests.py --suite document`; links and owners | local static |
| WORK-003 | ledger gate; four strict validators | local static |
| All | `qa.py staged` through the hooks | local static, at commit |

Architecture compliance: no AD or ADR change, and no validator, test or schema change.

### Stage Placement

The checks run before and after, and the staged QA runs once per commit. The review reads the recorded results.

## Risks

### Risks and Mitigations

- **A link replaces a fact that only the restating place held.** Possible, Moderate: MEDIUM, mitigate. Owner: platform. Each replaced sentence is compared with its canon, and the review checks it.
- **A projection drifts from an edited role body.** Possible, Moderate: MEDIUM, mitigate. Owner: platform. The governance validator compares projections.
- **The registry text change trips a contract test.** Possible, Minor: LOW, mitigate. Owner: platform. The `document` suite runs before commit.

### Escalation

Stop and ask if a canon lacks a fact that the restating place held.

## Promotion Map

### Durable Meaning

The edited canonical files are the durable owners.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |
