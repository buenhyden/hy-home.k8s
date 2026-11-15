---
title: "W01 3.0.1 Governance Contract Fit Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0217-PLAN-0001"
parent_ids: ["SPEC-0217"]
---

# W01 3.0.1 Governance Contract Fit Implementation Plan

## Overview

### Goal and Boundary

This Plan executes [SPEC-0217](spec.md). When it is complete:

- the glossary carries vocabulary 3.0.1;
- the four named duplicates have one author each, and the facts only they held stay in place;
- EXEC-R012 is retired;
- the SPEC-0161 Task holds the W01 rule-fit record, the requirement dispositions and the W00 owner correction;
- W01-H02 waits for the user's per-item decision, with its live row and ledger entry agreeing;
- three violation cases have been refused.

Every item that the Spec assigns to another stage is excluded.

#### Global Constraints

Every work unit inherits the constraints of the approved [Spec](spec.md). Additional constraints:

- No rule meaning changes except where the Spec names it.
- The diagnostics of the knowledge, governance and four strict document validators are equal before and after, apart from the intended fixes.
- `_workspace/` is read, never written.

### Assumptions

- `main` is `588257c9`, and the ledger holds 57 entries. The draft package commit is `59db20f1`.
- No validator or test pins the text of EXEC-R004, EXEC-R006, EXEC-R012, AUTHOR-R007 or the `.claude/provider.md` read-only bullet. A search of `scripts/` and `tests/` found none.
- `TERM-HISTORICAL-AUDIT` has no consumer outside the glossary.
- ADR-0058 and AD-0006 are touched by no work unit.

## Dependencies

### Prerequisites

- Spec and Plan approval with an independent review, because the risk class is `high`.
- PKG present with its manifest hashes unchanged.

### Dependency Order

WORK-001 (glossary) and WORK-002 (single author) are independent. WORK-003 (records) and WORK-004 (violation cases) run after them, so they read the final text.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W01C-001](spec.md#criteria) | Rewrite the glossary rows to vocabulary 3.0.1: meanings, owner roles, three new terms, removed audit term, numeric versions. | Approval | [Task 0001](tasks/tsk-0001-w01-contract-3-0-1.md) | Knowledge validator; row-by-row comparison with `repository-vocabulary.json`. |
| WORK-002 | [VAL-W01C-002](spec.md#criteria) | Reduce EXEC-R004, EXEC-R006, AUTHOR-R007 and the `.claude/provider.md` read-only bullet to one author each; retire EXEC-R012. | Approval | [Task 0001](tasks/tsk-0001-w01-contract-3-0-1.md) | Governance validator, lifecycle validator with its rule-ID history check, link check. |
| WORK-003 | [VAL-W01C-003](spec.md#criteria) | Append `W01 3.0.1 Rule Fit` (with the requirement dispositions and the KEEP list), `W00 Verdict Owner Corrections` and one EVD row to the SPEC-0161 Task; edit the W01-H02 live row and ledger entry together. | WORK-001, WORK-002 | [Task 0001](tasks/tsk-0001-w01-contract-3-0-1.md) | Ledger gate at 57 entries after the edit; strict validators. |
| WORK-004 | [VAL-W01C-004](spec.md#criteria) | Confirm the rule explanation and the absence of restated common rules in the provider notes; run the three violation cases on scratch copies outside the repository. | WORK-001, WORK-002 | [Task 0001](tasks/tsk-0001-w01-contract-3-0-1.md) | Each case refused with its named diagnostic; scratch copies deleted. |

### Change and Rollback

Each work unit is a text edit. Undo one by restoring its files from `main`; undo all by deleting the branch, or by reverting the merge commit after merge.

## Verification Plan

### Verification Matrix

| Work Unit | Check | Lane |
| --- | --- | --- |
| WORK-001 | `scripts/validate-knowledge-surface.py --root .` | local static |
| WORK-002 | `scripts/validate-agent-governance.py --root .`; `scripts/validate-document-lifecycle.py --root . --mode strict` | local static |
| WORK-003 | `scripts/validate-work-residue-ledger.py --root .` | local static |
| WORK-004 | Lifecycle, knowledge and link validators on three scratch copies | local static, negative |
| All | Four strict document validators; `scripts/qa.py staged` through the commit hooks | local static, at commit |

Architecture compliance: no AD, ADR, registry, validator or test changes.

### Stage Placement

The validators run before and after the edits. The staged QA runs once per commit in the hooks. The independent review reads the recorded results and doesn't run them again.

## Risks

### Risks and Mitigations

- **A rewritten definition drifts from the 3.0.1 meaning.** Possible, Moderate: MEDIUM, mitigate. Owner: platform. The independent review compares each changed row with the PKG row.
- **A link replacing a duplicate loses a fact that only the duplicate held.** Possible, Moderate: MEDIUM, mitigate. Owner: platform. Each removed sentence is checked against its owner before removal, and the review checks it again.
- **The glossary and AUTHOR-R015 disagree on prerelease until W03-VERSION.** Likely, Minor: MEDIUM, monitor. Owner: W03-VERSION. Recorded under GOV-07.

### Escalation

Stop and ask if an owner lacks a fact that the duplicate held, or if a 3.0.1 meaning conflicts with a confirmed decision.

## Promotion Map

### Durable Meaning

The glossary and policy edits are themselves the durable owners. Nothing else is promoted.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |
