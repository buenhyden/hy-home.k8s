---
title: "Derived Reverse Traceability Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0164-PLAN-0001"
parent_ids: ["SPEC-0164"]
---

# Derived Reverse Traceability Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds one constraint: only the files the Spec names by writer change.

## Overview

Remove the reciprocal back-link obligation from the registry, schema, validators, tests, policies and REQ-0003, and add a tool that derives back-links on demand. [Task 0001](tasks/tsk-0001-derived-reverse-traceability.md) owns execution and evidence.

## Context

The user adopted DOC-09 on 2026-11-12 (SPEC-0161 EVD-018). SPEC-0162 and SPEC-0163 each had to hand-write REQ-0003 and Spec back-links only to satisfy `BODY-LINK-RECIPROCAL`. This branch continues `claude/w00-v14-7-intake` after `e6157654`. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) constrains the design; two of its traceability rows change wording, and no ADR changes.

## Goals & In-Scope

- Backlinks tool and its tests, test-first.
- Remove the reciprocal field, check, branch, helper and their tests; schema negative case for a leftover key.
- REQ-0003, `sdlc.md`, the requirements-to-design skill, AD-0006 and Stage 05 exclusion-cell wording; remove the three back-link sentences.

## Non-Goals & Out-of-Scope

- Parent-side link columns of the current forms (SPEC-0161 handoff W03, common forms).
- Supersession reciprocity and its policy sentences.
- Self-containedness checks (none depends on reciprocal links).

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REVERSE-002](spec.md#success-criteria--verification-plan) | Backlinks tool, test-first. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-derived-reverse-traceability.md) | `tooling` suite before and after. |
| WORK-002 | [VAL-REVERSE-001](spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](spec.md#success-criteria--verification-plan) | Remove the reciprocal rule everywhere; reword the traceability owners. | WORK-001. | [Task 0001](tasks/tsk-0001-derived-reverse-traceability.md) | Repository search, `document` suite, strict document checks, commit hooks. |

## Verification Plan

- Show the backlinks tests failing before the tool exists, then passing.
- Add a schema negative case for a leftover `reciprocal_evidence` key; keep the broken-link and disallowed-profile cases passing.
- Run the `document` and `tooling` suites, the registry validator and the strict document checks.
- Record the risk class (`medium`: registry, validator and test change) and the core-diff checklist.
- Run the Spec's repository search and list every remaining hit in the Task as supersession or history.
- Architecture compliance: no ADR changes; AD-0006 changes only its IF-0001 and criterion 02 rows.

## Risks & Mitigations

- **A forward check depended on the reciprocal helper.** Mitigation: the `document` suite and strict checks run on the full tree.
- **Readers lose the parent-side view.** Mitigation: the backlinks tool derives it; the SPEC-0161 handoff W03 common-forms work adds derived downstream links to the forms.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Single-write traceability with derived back-links | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Traceability and relationships |
