---
title: "W03 Form Target Adoption"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-17"
artifact_id: "SPEC-0221-PLAN-0001"
parent_ids: ["SPEC-0221"]
---

# W03 Form Target Adoption Implementation Plan

## Overview

### Goal and Boundary

This Plan executes [SPEC-0221](spec.md). The completion state: the twelve role forms, their 17 templates and their current documents use the target heading trees, and the four approved Spec and Plan identities keep a retained form. It delivers the registry, template, document, validator, test and policy-prose changes that the Spec names, one role group per work unit. It excludes table columns, the task role's section IDs, other roles, `docs/98.archive/` and every protected remote action.

#### Global Constraints

Every work unit inherits the [Spec](spec.md#non-goals) constraints. Also:

- Each work unit is one commit, and the commit passes `python3 scripts/qa.py staged` on its exact index. A form and every document and test that reads it move together.
- No alias, fallback or dual reading of an old section ID or title stays in code, per `scripts/AGENTS.md` rule 3.

### Assumptions

The current forms are the ones that SPEC-0169 to SPEC-0203 put in place. Each role's current documents share one or two heading trees, so the move follows the Spec map for each document. This Plan touches ADR-0059's registry model, the document lifecycle policy, the document authoring policy and the Stage 99 README. It changes no architecture view and no ADR.

## Dependencies

### Prerequisites

- Spec and Plan approval by the user, with the exact bytes recorded in the Task.
- The `hyhome-validation` environment for the validators, the `document` suite and staged QA.
- The registry's existing `retained_form` extension kind and its identity bound.

### Dependency Order

WORK-001 moves the spec and plan forms first. The package's own Spec and Plan then sit on the retained form for the rest of the work. WORK-002 to WORK-005 each need only WORK-001 and may run in any order. WORK-006 needs all of them.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORM-001](spec.md#criteria), [VAL-FORM-003](spec.md#criteria) | Spec and plan forms, their two templates, the retained form for the four identities, and the lifecycle and link code and tests that read their section IDs. Stage 03 and lifecycle prose that names a moved heading. | Approval | [Task](tasks/tsk-0001-w03-form-target-adoption.md) | RED and GREEN focused tests; strict validators; staged QA |
| WORK-002 | [VAL-FORM-001](spec.md#criteria), [VAL-FORM-002](spec.md#criteria) | Requirement and architecture forms, two templates, 4 Requirements and 4 Architecture Descriptions, and their code and tests. | WORK-001 | [Task](tasks/tsk-0001-w03-form-target-adoption.md) | Same, plus per-document sentence counts |
| WORK-003 | [VAL-FORM-001](spec.md#criteria), [VAL-FORM-002](spec.md#criteria) | Guide, runbook, incident, postmortem and policy forms, six templates, 1 guide, 10 runbooks, 5 operations policies and 10 governance rules, and the policy rule ID binding. | WORK-001 | [Task](tasks/tsk-0001-w03-form-target-adoption.md) | Same |
| WORK-004 | [VAL-FORM-001](spec.md#criteria), [VAL-FORM-002](spec.md#criteria) | Skill form, two templates and 19 skills and workflows. | WORK-001 | [Task](tasks/tsk-0001-w03-form-target-adoption.md) | Same |
| WORK-005 | [VAL-FORM-001](spec.md#criteria), [VAL-FORM-002](spec.md#criteria) | Root, stage and service README forms, five templates, and 43 READMEs. | WORK-001 | [Task](tasks/tsk-0001-w03-form-target-adoption.md) | Same |
| WORK-006 | [VAL-FORM-003](spec.md#criteria) | Out-of-scope differences recorded as residue; the independent review; the `document` suite. | WORK-002 to WORK-005 | [Task](tasks/tsk-0001-w03-form-target-adoption.md) | Ledger gate; review record; suite result |

### Change and Rollback

Each work unit changes the registry form entries, TemplateDefinitions and body contracts of its roles, then their templates, documents, code, tests and prose. To undo a work unit, revert its commit. Revert later units first, because each unit leaves a consistent tree.

## Verification Plan

### Verification Matrix

- Normal case: every document of the role passes the strict registry, markdown profile, link and lifecycle validators under its new form.
- Violation cases:
  - the former tree of the role is refused;
  - a heading placed only inside a fence, quote or HTML block is refused;
  - a missing required H3 is refused;
  - a fifth Spec or Plan in the old tree is refused.
- Regression: the focused modules that name the role's sections. The `document` suite runs once in WORK-006.
- Architecture compliance: every change stays within ADR-0059's registry model. A change outside it returns the Spec to in-review.
- No live evidence is in scope.

### Stage Placement

Each work unit's commit runs `qa.py staged` through the hooks on its exact index. The `document` suite runs once on the final tree in WORK-006. The pull request runs the hosted `ci-summary` and `style-pr` checks once. Push and merge do not repeat an identical leaf.

## Risks

### Risks and Mitigations

- **A sentence lost in a move.** Record a sentence count before and after for each document, and have the independent review sample one document per role.
- **A new section without a source fact.** The Task records it. The section's requiredness is then reconsidered, and nothing is filled in to pass.
- **A broken anchor link.** The link check refuses it, and the link is repointed in the same unit.
- **The suite's long run time.** It runs once, at the end.

### Escalation

The work stops and asks the user in two cases: a role's map cannot keep a sentence's meaning, or a validator would have to be weakened to pass. It resumes after the user's answer.

## Promotion Map

### Durable Meaning

The adopted heading trees and section IDs of the twelve forms, and the retained form for the four approved identities, stay in the Stage 99 registry after the work.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| FORM-TREES | [Document Authoring](../../../.agents/governance/document-authoring.md) | The authoring policy delegates the exact form rules to the Stage 99 registry, and the registry holds the twelve new form trees. | Stage 99 `common_forms` |
