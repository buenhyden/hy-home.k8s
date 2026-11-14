---
title: "W03 Governance Policy Rule IDs Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0199-PLAN-0001"
parent_ids: ["SPEC-0199"]
---

# W03 Governance Policy Rule IDs Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no existing sentence, heading or line break of a policy changes; no validator, schema, template or form changes; and the diagnostics of the four strict document validators outside the nine policies are equal before and after.

## Overview

For each of the nine governance policies, map the rule units, add the definition tokens, the Rules table and the H4 headings the unit rule requires, set the registry record to `adopted`, and prove that the prose is unchanged; then record W03-D58, the W03-H29 state and the final unit map. [Task 0001](tasks/tsk-0001-w03-governance-policy-rule-ids.md) owns execution, the reviewed inventory and evidence.

## Context

A read of `main` at `8daf643f` (after SPEC-0187) found the following; every count is re-read at implementation time, because SPEC-0188 to SPEC-0198 merge first and SPEC-0194 adds one sentence to the document authoring policy.

- The ten governance policies hold 143 top-level list items and 35 table rows under `Requirements`, 16 H4 groups without a list or table, 11 H4 groups that hold items or rows and paragraphs of their own, and 10 paragraphs outside every unit (nine in `document-authoring.md`, one in `sdlc.md`). That yields 196 to 215 rule IDs; the [Task](tasks/tsk-0001-w03-governance-policy-rule-ids.md) holds the count for each policy.
- `quality.md` alone holds 45 to 51 units in eleven H4 groups, six of them mixed, and 34 of the 42 Markdown fragment links found from other documents into the ten policies target it; `.agents/roles/registry.json` adds 17 `capability_tier_ref` JSON references to `model-selection.md#top` and `model-selection.md#worker`.
- An approximate reading of the wording of 224 units found 188 that state an imperative, a prohibition or a must-like word, 28 that join such a requirement with a should or a may, 2 worded only with should and 6 only with may; no policy uses reserved keywords, so the Level is a reading and not a pattern match.
- Lines are wrapped near 80 columns and line length is not linted, so a token lengthens one line and no line is re-wrapped.
- Scripts and tests name the policy paths, and `scripts/validation/repository/quality.py` reads `approval-and-safety.md`; whether any of them pins a sentence that a token would split is shown by the suites.

## Goals & In-Scope

- Nine policies: tokens, one Rules table each, headings over ruled paragraphs outside a unit, `version` and `updated`.
- Registry: nine `state` values.
- The SPEC-0161 Task rows, the ledger entry and the final unit map.

## Non-Goals & Out-of-Scope

- `quality.md`; the operations policies; the history check; the gate retirement; any code, template, form or other registry content; any existing prose.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GOVRULE-001](spec.md#success-criteria--verification-plan) | Tokens, Rules table, added headings and the `adopted` state for each of the nine policies. | Approved Spec and Plan; SPEC-0194 implemented and merged; SPEC-0198 merged. | [Task 0001](tasks/tsk-0001-w03-governance-policy-rule-ids.md) | Profile check refusing first, then passing, for each policy. |
| WORK-002 | [VAL-GOVRULE-002](spec.md#success-criteria--verification-plan) | The final map of each ID to its unit with its Level, Condition and Evidence reading; the stripped-body comparison; the version steps. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-governance-policy-rule-ids.md) | Byte comparison and hashes; link and agent governance checks; heading slug comparison; map against the reviewed inventory. |
| WORK-003 | [VAL-GOVRULE-003](spec.md#success-criteria--verification-plan) | W03-D58, the W03-H29 state cell and the ledger entry; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-governance-policy-rule-ids.md) | Strict validators, suites, quality gate, markdownlint, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators and the base hash of each policy before any change.
- Work one policy at a time, the smallest first: flip its record, show the refusal, add the tokens and table, show the pass, run the stripped-body comparison by the exact removals the Spec defines and the heading slug comparison.
- Record in the Task the final unit map of each policy and each judgment on a mixed group, a paragraph outside a unit and a Level other than `required`; a unit that needs the user's reading is listed and its policy stays `pending`.
- Confirm that `quality.md` and the five operations policies are unchanged and `pending`.
- Commit order: the package commit with the W03-D58 row; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the change.
- Record the risk class (`medium`: nine governance policies and nine registry values; no rule meaning, code, permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **A Condition, Level or Evidence cell adds or changes meaning.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The cells are new text for 151 to 164 rules; they restate the rule and name only checks that exist, and the Task lists every reading for review. Review cue: the unit map. Signal that raises it: a cell that names a check absent from the tree, or a Level the wording does not support. Rollback: revert that policy to `pending`.
- **A validator or test pins a sentence that a token splits.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Policies are done one at a time with the suites run after each. Review cue: the `agent-governance` and `tooling` suites. Signal that raises it: a failure that names a policy sentence. Rollback: revert that policy.
- **Prose changes by accident.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The stripped-body comparison is byte for byte. Review cue: the two hashes for each policy. Signal that raises it: unequal hashes. Rollback: revert that policy.
- **The policies grow and cost context in every agent session.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Each rule adds one table row; cells stay short and no prose is repeated. Review cue: the size of each policy before and after, recorded in the Task. Signal that raises it: a policy that grows by more than half. Rollback: none needed; shorten the cells.
- **The unit map departs from the reviewed inventory.** Possible, Minor: LOW, monitor. Owner: W03 author. The inventory gives a range and the map records each judgment. Review cue: the count for each policy. Signal that raises it: a count outside the range. Rollback: stop and ask the user.
- **The base moves under the policies.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0188 to SPEC-0198 merge first, and SPEC-0194 edits the document authoring policy. Review cue: the base hashes in the Task. Signal that raises it: a changed count. Rollback: re-read and correct the inventory before the implementation commit.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The rule IDs of the nine governance policies | [Agent execution policy](../../../.agents/governance/agent-execution.md) and the eight other adopted policies | The Rules table and definition tokens under `Requirements`; the `adopted` records in `docs/99.templates/registry.json` |
