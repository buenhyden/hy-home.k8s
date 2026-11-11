---
title: "Rejected Package Clauses Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0156-PLAN-0001"
parent_ids: ["SPEC-0156"]
---

# Rejected Package Clauses Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two execution constraints. First, no repository file changes outside this package, the Stage 03 README, the "Scope and Non-goals" sentence, version, `updated` and one Traceability back-link sentence of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), and `.secrets.baseline` entries marking this Task's reviewed SHA-256 document digests as non-secret, following commit `f3dcab6d`. Second, REQ-0003 is edited only after the Spec and Plan are approved.

## Overview

Record the four rejected package clauses in REQ-0003 "Scope and Non-goals" as defined in [SPEC-0156](spec.md), and record the W01 intake survey. [Task 0001](tasks/tsk-0001-rejected-package-clauses.md) owns execution evidence and criterion acceptance.

## Context

Completed SPEC-0154 (commit `fafd7a09`) recorded the GOV-06, GIT-09 and DOC-12 dispositions only in its Task's Conflict Dispositions, and its Plan promoted no durable contract. The W01 intake survey on branch `claude/w01-governance-standards` (base `ff6bcdb2`, merged into `main` by PR #221 as `6949179f`) found no other W01 difference. On 2026-11-11 the user answered Q-W01-01 by keeping the checked back-links. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrain the design; no interface, migration or rollback surface beyond REQ-0003 and this package changes.

## Goals & In-Scope

- Add one sentence to REQ-0003 "Scope and Non-goals" naming the four rejected clauses with their conflicting accepted requirements.
- Move REQ-0003 to version 3.0.3, set `updated`, and add a Traceability back-link to this Spec.
- Record the 23-item W01 intake survey and its handoffs in the Task.
- Add this package to the Stage 03 README.

## Non-Goals & Out-of-Scope

- Any governance policy, registry, template, validator, test, provider, hook, workflow or manifest change.
- GOV-08 permission allow rules (stage W07).
- Changing the reverse-traceability contract (Q-W01-01 kept it).
- Any push, PR, merge or package exit without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REJ-001](spec.md#success-criteria--verification-plan), [VAL-REJ-002](spec.md#success-criteria--verification-plan), [VAL-REJ-003](spec.md#success-criteria--verification-plan) | Record the intake survey; add the REQ-0003 non-goals sentence, version and back-link; obtain independent review. | Approved Spec and Plan; completed SPEC-0154; the user's Q-W01-01 decision. | [Task 0001](tasks/tsk-0001-rejected-package-clauses.md) | Inline sentence check with a negative copy, independent review, strict document checks and commit hooks. |

## Verification Plan

- Check that the REQ-0003 sentence names all four clauses and cites FR-0019, FR-0022, FR-0018, FR-0023 and IF-0001, and that a negative copy missing one clause is detected.
- Have an independent read-only reviewer confirm the sentence restates accepted contracts only.
- Run the strict document checks, the staged lifecycle check and the active commit hooks on the exact index.
- Architecture compliance: confirm no AD, ADR or governance policy file changed.

## Risks & Mitigations

- **The sentence reads as a new rule.** Mitigation: it cites only accepted requirements and adds no obligation; review checks this.
- **A later stage needs a rejected clause.** Mitigation: that stage must amend the accepted requirement first, as the Spec states.

## Completion Criteria

All three criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, and the operator's acceptance. Completion closes W01's differences only; GOV-08 stays with W07.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Rejected external package clauses and the accepted contracts they conflict with | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#scope-and-non-goals) | Scope and Non-goals |
