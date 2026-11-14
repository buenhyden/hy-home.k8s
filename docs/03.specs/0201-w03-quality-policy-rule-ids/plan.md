---
title: "W03 Quality Policy Rule IDs Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0201-PLAN-0001"
parent_ids: ["SPEC-0201"]
---

# W03 Quality Policy Rule IDs Implementation Plan

## Overview

### Goal and Boundary

Map the rule units of `.agents/governance/quality.md`, add the definition tokens and the Rules table, set the `QUAL` record to `adopted`, prove that the prose and every anchor are unchanged, and record W03-D60, the unit map and the W03-H29 state. [Task 0001](tasks/tsk-0001-w03-quality-policy-rule-ids.md) owns execution, the binding unit table and evidence.

Goals and in-scope:

- The policy: tokens, one Rules table, `version` and `updated`.
- Registry: one `state` value.
- The W03-D60 row, the state cell and the evidence row of the SPEC-0161 Task, the ledger entry and the unit map.

Non-goals and out-of-scope:

- The other policies; the history check; the gate retirement; any code, template, form or other registry content; any existing prose, heading or linking document.

#### Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no existing sentence, heading or line break of the policy changes; no validator, schema, template or form changes; and the diagnostics of the four strict document validators outside the policy are equal before and after.

### Assumptions

A read of `main` at `8daf643f` (after SPEC-0187) found the following; every count is re-read at implementation time, because SPEC-0188 to SPEC-0200 merge first.

- `Requirements` of the policy opens directly with its first H4 heading and holds eleven H4 groups: 33 top-level list items, 7 table rows, 5 groups without a list or table, 6 mixed groups and no paragraph outside a group. With a group token on each mixed group (W03-D60) that is 51 rule IDs, `QUAL-R001` to `QUAL-R051`; the [Task](tasks/tsk-0001-w03-quality-policy-rule-ids.md) holds the binding table.
- In each of the six mixed groups at least one paragraph of its own states an obligation that its items or rows do not state (for example the leaf reuse rule after the lane list and the no-commit rule after the completion steps), which is the reading W03-D60 settles: each takes a group token, one ID identifies a group and no group is split.
- The preliminary reading of the wording finds no unit whose sole obligation is a should or a permission, so every row would read `required`; the final reading is recorded for each ID.
- 34 Markdown fragment links from 25 documents target nine of the eleven H4 headings; `QA admission and retirement` and `Supply-chain identity` have none. The sources include the work lifecycle, eight role bodies, six other governance policies, the handoff prompt and two files under `.github/`. No tracked file other than Markdown names a fragment of the policy.
- The policy's `Enforcement` section names one owner, the validation routing registry, so the Evidence cells cite only existing checks looked up in `scripts/validation/registry.json`, `scripts/run-contract-tests.py` or the tree, or name the review that judges the rule (W03-D60).
- The policy holds 388 lines and 22,266 bytes; 51 rows and tokens add an estimated 7 to 9 kilobytes.
- Scripts and tests name the policy's path in path sets and fixtures; whether any pins a sentence that a token would split is shown by the suites.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-QUALRULE-001](spec.md#criteria) | Tokens, the Rules table and the `adopted` state for the policy. | Approved Spec and Plan; SPEC-0194 implemented; SPEC-0199 merged. | [Task 0001](tasks/tsk-0001-w03-quality-policy-rule-ids.md) | Profile check refusing first, then passing. |
| WORK-002 | [VAL-QUALRULE-002](spec.md#criteria) | The map of each ID to its unit with its Level, Condition and Evidence; the stripped-body comparison; the anchor and slug checks; the lookup of every named check; the version step. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-quality-policy-rule-ids.md) | Byte comparison and hashes; link and agent governance checks; fragment search; heading slug comparison; map against the binding table. |
| WORK-003 | [VAL-QUALRULE-003](spec.md#criteria) | W03-D60, the W03-H29 state cell and the ledger entry; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-quality-policy-rule-ids.md) | Strict validators, suites, quality gate, markdownlint, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators, the base hash and size of the policy, its heading slugs and the two consumer searches before any change.
- Flip the record, show the refusal, add the tokens and table one H4 group at a time, show the pass, then run the stripped-body comparison by the exact removals the Spec defines and the heading slug comparison.
- Record in the Task the unit map against the binding table, each Level other than `required`, the lookup of every named check and the size of the policy after the change; a unit that needs the user's reading is listed and the record stays `pending`.
- Confirm that the five operations policies are unchanged and `pending` and that the nine policies of SPEC-0199 are unchanged.
- Record the risk class (`medium`: one governance policy and one registry value; no rule meaning, code, permission, trigger, hook or workflow) and the core-diff checklist.

Completion criteria:

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

### Stage Placement

- Commit order: the package commit with the W03-D60 row; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the change.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **A Condition, Level or Evidence cell adds or changes meaning.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The cells are new text for 51 rules of the policy that defines evidence itself; they restate the rule, every named check is looked up, and the Task lists every reading. Review cue: the unit map. Signal that raises it: a cell that names a check absent from the tree. Rollback: set the record back to `pending` with the body.
- **One ID covers several obligations.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Eleven IDs identify a whole group or its own paragraphs; no group is split (W03-D60), because that would shorten a linked section. Review cue: the Condition and Level of those eleven rows. Signal that raises it: a reader who cannot cite one obligation by its ID. Rollback: none needed; a later package may refine a group with the user's decision.
- **A link into the policy stops resolving.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. No heading text changes and no heading is added at this base; the link validator and the slug comparison show it. Review cue: the 34 links. Signal that raises it: a fragment diagnostic or a changed slug. Rollback: revert the implementation commit.
- **A validator or test pins a sentence that a token splits.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Tokens are added one group at a time with the suites run after. Review cue: the `agent-governance`, `tooling` and `qa-runner` suites. Signal that raises it: a failure that names a policy sentence. Rollback: revert the implementation commit.
- **The policy grows and costs context in every agent session.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. The table adds an estimated 35 to 40 percent; cells are short phrases and no prose is repeated. Review cue: the size before and after. Signal that raises it: growth beyond half. Rollback: none needed; shorten the cells.
- **Prose changes by accident.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The stripped-body comparison is byte for byte. Review cue: the two hashes. Signal that raises it: unequal hashes. Rollback: revert the implementation commit.
- **The base moves under the policy.** Possible, Minor: LOW, monitor. Owner: W03 author. SPEC-0188 to SPEC-0200 merge first and may edit this policy. Review cue: the base hash in the Task. Signal that raises it: a unit that no longer matches the binding table, or a paragraph outside a group. Rollback: stop and ask the user before any ID is issued.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| The rule IDs of the quality policy | [Quality policy](../../../.agents/governance/quality.md) | The `QUAL` record is `adopted` and the policy carries its Rules table and tokens, with PASS evidence for VAL-QUALRULE-001 | The Rules table and definition tokens under `Requirements`; the `adopted` record in `docs/99.templates/registry.json` |
