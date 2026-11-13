---
title: "W03 Explained Empty Sections Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0182-PLAN-0001"
parent_ids: ["SPEC-0182"]
---

# W03 Explained Empty Sections Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no heading, no frontmatter key other than `version` and `updated` where the file has frontmatter, and no sentence with content changes, and the diagnostics of the four strict document validators over the tree are equal before and after, the new rule refusing nothing.

## Overview

Replace each bare line from the reviewed reason table or with a listed document-specific sentence, correct the seven wrong pointers, add `BODY-SECTION-BARE` and its tests, and update the policy sentence. [Task 0001](tasks/tsk-0001-w03-explained-empty-sections.md) owns execution and evidence.

## Context

A read of the tree on 2026-11-13, and the pre-approval review's sole-body scan, found 151 bare lines, each the only body of a required, always-present H3: 57 in the 17 native skills, 4 in `work-lifecycle.md` and `delegated-development.md`, 43 in the 16 folder `AGENTS.md` files, 17 in governance and operations policies (8 English statements and 9 `Exclusions` lines) and 30 in Korean READMEs. Three lines already carry a reason or a pointer and stay. A sample of about 35 pointer lines found every target present, except seven AGENTS lines that cite a "Purpose text" the AGENTS form does not have. The root `AGENTS.md` has 23 content and 16 heading lines against the gateway limits of 30 and 16. The validator refuses only bare `TBD`, `TODO`, `N/A`, `NA` and `pending`, and two `agents_body()` test fixtures use bare lines.

## Goals & In-Scope

- Documents: 148 of the 151 lines (three already explained stay) and the seven pointers.
- Code and tests: `BODY-SECTION-BARE`; the fixtures.
- Policy: one sentence; an evidence row in the SPEC-0161 Task.

## Non-Goals & Out-of-Scope

- Form requiredness; sections with content; other frontmatter keys; skill bundles; the gateway limits; accepted ADR bodies; completed evidence.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EMPTY-001](spec.md#success-criteria--verification-plan) | Reason-table rewrites, document-specific sentences, pointers, `BODY-SECTION-BARE`, tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-explained-empty-sections.md) | The rule's refusals on the unchanged tree, then none; a per-line list in the Task. |
| WORK-002 | [VAL-EMPTY-002](spec.md#success-criteria--verification-plan) | Policy sentence; gateway counts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-explained-empty-sections.md) | Strict validators, agent governance, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators and the root gateway counts before any change.
- Run the new rule on the unchanged tree and record its refusals, then none after the rewrite.
- Record each line's file, section, old text and new text, marking table sentences and document-specific ones, and each corrected pointer, in the Task; the document-specific sentences go to the user in the acceptance question.
- Commit order: the package commit; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Record the risk class (`medium`: about 60 governed documents including native skills, a workflow every session loads and folder agent rules, one validator and tests; no permission, trigger, hook or workflow file) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval review's evidence.

- **A rewrite reads as a new obligation in loaded context.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The new text lands in `work-lifecycle.md`, skills and folder rules that sessions load; the reason table only restates what the owners say and is reviewed with the Spec, and document-specific sentences are listed for acceptance. Review cue: the acceptance question. Signal that raises it: an agent treating a follow-up sentence as a rule. Rollback: revert the line.
- **The root gateway exceeds its line limit.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. Seven lines of headroom; each rewrite stays on one physical line and the counts are recorded. Review cue: `AGENT-NATIVE-REFERENCE`. Signal that raises it: a wrapped rewrite. Rollback: shorten the line.
- **The rule is evaded by rewording.** Likely, Minor: MEDIUM, accept with review. Owner: W05 code. The Spec states the limit and leaves sufficiency to semantic review. Review cue: semantic review of new documents. Signal that raises it: a reworded bare line found in review. Rollback: widen the rule in a later change.
- **Existing fixtures fail.** Likely, Minor: MEDIUM, mitigate. Owner: W05 code. The `agents_body()` fixtures are in scope and change with the rule. Review cue: the form tests. Signal that raises it: a red form test. Rollback: none needed beyond the fixture edit.
- **The rule refuses legitimate prose.** Unlikely, Minor: LOW, monitor. Owner: W05 code. It matches only closed bare shapes with no further clause. Review cue: the rule tests. Signal that raises it: a refusal on an explained none. Rollback: narrow the rule.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Explained empty sections and accurate pointers | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Empty-section sentence; rule in `scripts/validate-markdown-profiles.py` |
