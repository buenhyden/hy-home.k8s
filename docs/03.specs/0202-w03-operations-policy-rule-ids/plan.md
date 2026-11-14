---
title: "W03 Operations Policy Rule IDs Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0202-PLAN-0001"
parent_ids: ["SPEC-0202"]
---

# W03 Operations Policy Rule IDs Implementation Plan

## Overview

### Goal and Boundary

Amend the coverage floor with its tests first; then, for each of the four operations policies, issue the IDs of the binding table, add the definition tokens and the Rules table, list the map for review and set the registry record to `adopted`; prove that the prose and the anchors are unchanged; and record W03-D62, the W03-H29 state and the evidence. [Task 0001](tasks/tsk-0001-w03-operations-policy-rule-ids.md) owns execution, the binding unit table and evidence.

Goals and in-scope:

- Validator and tests: the amended coverage floor.
- Four policies: tokens, one Rules table each, `version` and `updated`.
- Registry: four `state` values.
- The W03-D62 row, the state cell and the evidence row of the SPEC-0161 Task, the ledger entry and the unit maps.

Non-goals and out-of-scope:

- POL-0007 and the gate retirement (the following package); the governance policies; the history check and code permanence; control registers and control IDs; the body contract of the profile; any other rule of SPEC-0194; any existing prose, heading, runbook, guide or manifest.

#### Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no existing sentence, heading or line break of a policy changes; the coverage floor is the only validator behavior that changes, and the adoption gate stays; and the diagnostics of the four strict document validators outside the scope are equal before and after.

### Assumptions

A read of `main` at `4bcda456` (after SPEC-0188) and of the approved texts of SPEC-0194, SPEC-0199 and SPEC-0201 found the following; every count and name is re-read at implementation time, because SPEC-0189 to SPEC-0201 merge first and SPEC-0194 is not yet implemented at that commit.

- The four policies hold 43 top-level list items, 54 nested items and 12 control rows under `Requirements`, in two H4 groups without a list or table, with no mixed group, no empty heading and no paragraph outside a group; the [Task](tasks/tsk-0001-w03-operations-policy-rule-ids.md) holds the binding table.
- POL-0001 holds 18 items under the headings `Required`, `Allowed` and `Disallowed`, and POL-0005 holds 5 items and 2 prose groups: 18 and 7 IDs.
- In POL-0003 and POL-0004, 17 of the 20 top-level items are the label lines `Required`, `Allowed` or `Disallowed`, and the 54 nested items state the rules; with the three items of `CI Governance` that gives 30 and 27 IDs (W03-D62). The coverage floor of SPEC-0194 reads top-level items only, so it is amended before these two policies adopt.
- All four are Korean-first; the labels and headings already sort the rules into required, allowed and disallowed, which the Level reading follows (W03-D62).
- The `Enforcement` sections name the owning runbooks and, in POL-0001, one guide, and the two control registers name an enforcement surface and evidence for each control; Evidence cites them by ID in the order W03-D62 sets.
- The language check of the profile judges plain paragraphs only; list items, table lines and headings are not judged.
- Six Markdown fragment links target these policies, all the `exceptions` heading of POL-0001; no tracked file other than Markdown names a fragment. Scripts and tests name the policy paths in path sets and fixtures, and `scripts/validation/repository/quality.py` scans the folder for commands.
- The four policies hold 34,454 bytes together, and no provider baseline lists them among the files to read before acting. POL-0003 and POL-0004 are the smallest and take the most rows.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-OPSRULE-001](spec.md#criteria) | The amended coverage floor and its six tests; the sentence that states the floor, where one exists. | Approved Spec and Plan; SPEC-0194 implemented; SPEC-0201 merged. | [Task 0001](tasks/tsk-0001-w03-operations-policy-rule-ids.md) | The label acceptance failing first, then all six tests passing; profile check over the ten governance policies. |
| WORK-002 | [VAL-OPSRULE-002](spec.md#criteria) | Tokens, Rules table and the `adopted` state for each of the four policies, as the binding table lists them. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-operations-policy-rule-ids.md) | Profile check refusing first, then passing, for each policy. |
| WORK-003 | [VAL-OPSRULE-003](spec.md#criteria) | The map of each ID to its unit with its Level, Condition and Evidence, listed for review before each record flips; the stripped-body comparison; the anchor and slug checks; the lookup of every named control, artifact and check; the version steps. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-operations-policy-rule-ids.md) | Byte comparison and hashes; link check; fragment search; heading slug comparison; map against the binding table. |
| WORK-004 | [VAL-OPSRULE-004](spec.md#criteria) | W03-D62, the W03-H29 state cell and the ledger entry; regression and exact-index QA. | WORK-003. | [Task 0001](tasks/tsk-0001-w03-operations-policy-rule-ids.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators, the base hash and size of each policy, its heading slugs and the two consumer searches before any change.
- Amend the floor first: write the six nested-list tests, show the label acceptance failing and the other five holding, change the rule, show all six and the ten governance policies passing.
- Work one policy at a time, POL-0005 and POL-0001 first: list its map for review, flip its record, show the refusal, add the tokens and table, show the pass, then run the stripped-body comparison by the exact removals the Spec defines and the heading slug comparison.
- Record in the Task each Level other than `required`, the lookup of every named control, artifact and check, and the size of each policy after the change; a unit that needs the user's reading is listed and its policy stays `pending`.
- Confirm that POL-0007, the ten governance policies and the two control registers are unchanged and that POL-0007 is still `pending`.
- Record the risk class (`medium`: four operations policies, four registry values, one validator rule and its tests; no rule meaning, permission, trigger, hook or workflow) and the core-diff checklist.

Completion criteria:

All four criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

### Stage Placement

- Commit order: the package commit with the W03-D62 row; then `.secrets.baseline` changes alone; then the floor amendment with its tests; then the adoptions with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **The amended floor weakens the check.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. It accepts an untokened top-level item only when its text is exactly one of the registered labels `Required`, `Allowed` or `Disallowed` with one colon and every nested item carries a token; tests show a partly tokened list, an untokened list, a sentence ending in a colon and an inner-colon label refused, and a tokened parent over untokened nested items still accepted. Review cue: the six tests. Signal that raises it: a label with an untokened nested item, or an untokened parent with any text beyond a registered label, passing. Rollback: revert the amendment commit; POL-0003 and POL-0004 then stay `pending`.
- **A Condition, Level or Evidence cell adds or changes meaning.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The cells are new text for 82 rules, in Korean, about a live cluster; every named control, artifact and check is looked up, every reading is listed for review before the flip, and no cluster evidence is claimed. Review cue: the unit map. Signal that raises it: a cell that names something absent from the tree. Rollback: set that policy back to `pending` with its body.
- **A unit at the base no longer matches the binding table.** Possible, Minor: LOW, monitor. Owner: W03 author. IDs are permanent, so the table is compared with the base before the first ID. Review cue: the Task's table. Signal that raises it: a changed item count in a group. Rollback: stop and ask the user before any ID is issued.
- **A validator or test pins a line that a token splits.** Possible, Minor: LOW, monitor. Owner: W03 author. Policies are done one at a time with the suites run after each. Review cue: the `tooling` suite and the quality gate. Signal that raises it: a failure that names a policy line. Rollback: revert that policy.
- **Prose changes by accident.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The stripped-body comparison is byte for byte. Review cue: the two hashes for each policy. Signal that raises it: unequal hashes. Rollback: revert that policy.
- **The policies grow.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. 82 rows are added to 34,454 bytes, 30 of them to the 7,899 bytes of POL-0003; cells stay short phrases and no control or runbook text is copied. Review cue: the size of each policy before and after. Signal that raises it: a policy that grows by more than half. Rollback: none needed; shorten the cells.
- **The base moves.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0189 to SPEC-0201 merge first, and the names of SPEC-0194 are read from its approved text. Review cue: the base hashes in the Task. Signal that raises it: a changed count or name. Rollback: stop and ask the user before any ID is issued.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| The rule IDs of four operations policies | [K8s GitOps platform operations policy](../../05.operations/policies/0001-k8s-gitops-operations-policy.md) and the three other adopted policies | The four records are `adopted` and each policy carries its Rules table and tokens, with PASS evidence for VAL-OPSRULE-002 | The Rules table and definition tokens under `Requirements`; the `adopted` records in `docs/99.templates/registry.json` |
| The coverage floor that accepts a registered label (`Required`, `Allowed`, `Disallowed`) over a fully tokened nested list | [Document authoring policy](../../../.agents/governance/document-authoring.md) | `POLICY-RULE-COVERAGE` accepts a registered label over a fully tokened nested list, with PASS evidence for VAL-OPSRULE-001 | Form paragraph, where it states the floor; `POLICY-RULE-COVERAGE` in `scripts/validate-markdown-profiles.py` |
