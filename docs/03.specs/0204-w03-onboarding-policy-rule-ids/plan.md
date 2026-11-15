---
title: "W03 Onboarding Policy Rule IDs Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0204-PLAN-0001"
parent_ids: ["SPEC-0204"]
---

# W03 Onboarding Policy Rule IDs Implementation Plan

## Overview

### Goal and Boundary

Issue the 45 IDs of the binding table to the app GitOps onboarding policy, add the definition tokens and the Rules table, list the map for review and set the `ONBOARD` record to `adopted`; prove that the prose and the anchors are unchanged; then retire the adoption gate with its refusal tests first, and record the W03-H29 state and the evidence. [Task 0001](tasks/tsk-0001-w03-onboarding-policy-rule-ids.md) owns execution, the binding unit table and evidence.

Goals and in-scope:

- The policy: tokens, one Rules table, `version` and `updated`.
- Registry, schema, loader, validator and tests: one `state` value, then the gate retirement.
- The state cell and the evidence row of the SPEC-0161 Task, the ledger entry and the unit map.

Non-goals and out-of-scope:

- The fourteen policies adopted earlier; the history check and code permanence; the coverage floor and every other rule of SPEC-0194; the body contract of the profile; any existing prose, heading, runbook or manifest.

#### Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no existing sentence, heading, table padding or line break of the policy changes; the gate is retired only in the final source commit, after all fifteen records are `adopted`; and the diagnostics of the four strict document validators outside the scope are equal before and after.

### Assumptions

A read of `main` at `4bcda456` (after SPEC-0188) and of the approved texts of SPEC-0194, SPEC-0199, SPEC-0201 and SPEC-0202 found the following; every count and name is re-read at implementation time, because SPEC-0189 to SPEC-0202 merge first and SPEC-0194 is not yet implemented at that commit.

- `Requirements` of the policy holds an opening paragraph and 17 H4 headings: 4 chapter headings with no content of their own, 4 groups without a list or table, 5 mixed groups, 3 groups that hold only a table and 1 that holds only a list; 19 top-level list items, 19 table rows, no nested item and no control register.
- Under W03-D62 that is 45 rule IDs: 17 items, 19 rows, 4 whole groups and 5 group tokens. The two items labelled `Required evidence` and the opening paragraph take none. The [Task](tasks/tsk-0001-w03-onboarding-policy-rule-ids.md) holds the binding table.
- The policy is Korean-first; `권장` appears in one table row and `선택` in one list item, and one group lists what is forbidden.
- Its `Enforcement` section names one runbook for the executable checks and names static checks of GitOps structure, manifests and secret handling; the policy has no control register, so Evidence starts from the runbook (W03-D62).
- No Markdown fragment link targets the policy and no tracked file other than Markdown names a fragment of it. `scripts/validation/repository/quality.py` scans the folder for commands, and one forbidden item names a command.
- The policy holds 242 lines and 13,952 bytes; 45 rows and tokens add an estimated 6 to 8 kilobytes. No provider baseline lists it among the files to read before acting.
- The gate consists, by the approved text of SPEC-0194, of the `state` field of fifteen records with its schema property and loader field, and the `POLICY-RULE-ADOPTION` rule and its tests. The `minimum_rows` value 0 of the Rules table in the two Policy TemplateDefinitions is no part of it: W03-D65 keeps the table conditional (REQ:310, REQ:742), and the minimum of one row is recorded with the table's condition in `rules_table`.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ONBRULE-001](spec.md#criteria) | Tokens, the Rules table and the `adopted` state for the policy, as the binding table lists them. | Approved Spec and Plan; SPEC-0194 implemented; SPEC-0202 merged. | [Task 0001](tasks/tsk-0001-w03-onboarding-policy-rule-ids.md) | Profile check refusing first, then passing. |
| WORK-002 | [VAL-ONBRULE-002](spec.md#criteria) | The map of each ID to its unit with its Level, Condition and Evidence, listed for review before the record flips; the stripped-body comparison; the anchor and slug checks; the lookup of every named artifact and check; the version step. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-onboarding-policy-rule-ids.md) | Byte comparison and hashes; link check; fragment search; heading slug comparison; map against the binding table. |
| WORK-003 | [VAL-ONBRULE-003](spec.md#criteria) | The gate retirement in the final source commit: `state`, `POLICY-RULE-ADOPTION` and their tests removed, the sentences that name the gate, the three refusal tests and the acceptance of a policy without normative rules. | WORK-002; all fifteen records `adopted`. | [Task 0001](tasks/tsk-0001-w03-onboarding-policy-rule-ids.md) | Refusal tests failing first, then passing; profile check over the fifteen policies. |
| WORK-004 | [VAL-ONBRULE-004](spec.md#criteria) | The W03-H29 state cell and the ledger entry; regression and exact-index QA. | WORK-003. | [Task 0001](tasks/tsk-0001-w03-onboarding-policy-rule-ids.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators, the base hash and size of the policy, its heading slugs and the two consumer searches before any change, and compare the policy with the binding table.
- List the map for review, with the opening paragraph as a no-ID reading, flip the record, show the refusal, add the tokens and table one H4 group at a time, show the pass, then run the stripped-body comparison by the exact removals the Spec defines and the heading slug comparison.
- Record in the Task each Level other than `required`, the lookup of every named artifact and check, and the size of the policy after the change; a unit that needs the user's reading is listed and the record stays `pending`.
- Retire the gate last: write the three refusal tests, show them failing, remove the field, the rule and the gate tests, leave `minimum_rows` at 0, show the tests and all fifteen policies passing, and record that the ongoing protection moved to the rules that read the table's condition and no state.
- Confirm that the fourteen policies adopted earlier are unchanged.
- Record the risk class (`medium`: one operations policy, the registry, its schema and loader, one validator and tests; no rule meaning, permission, trigger, hook or workflow) and the core-diff checklist.

Completion criteria:

All four criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

### Stage Placement

- Commit order: the package commit; then `.secrets.baseline` changes alone; then the adoption with the Task evidence; then the gate retirement as the final source commit. Run the staged lifecycle check before each commit and `graphify update .` after the code change.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **The gate retirement breaks a policy or a reader.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. It lands last, with refusal tests first and all fifteen policies checked without the gate. Review cue: the profile check over the fifteen. Signal that raises it: a diagnostic on an adopted policy or a registry reader that refuses the removed key. Rollback: revert the final source commit; the adoption stays.
- **A Condition, Level or Evidence cell adds or changes meaning.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The cells are new text for 45 rules, in Korean, about a live cluster; every named artifact and check is looked up, every reading is listed for review before the flip, and no cluster evidence is claimed. Review cue: the unit map. Signal that raises it: a cell that names something absent from the tree. Rollback: set the record back to `pending` with the body.
- **One ID covers several sentences.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Nine IDs identify a whole group or its own paragraphs, and two evidence items sit under a group token; W03-D62 binds that reading. Review cue: the Condition and Level of those nine rows. Signal that raises it: a reader who cannot cite one obligation by its ID. Rollback: none needed; a later package may refine a group with the user's decision.
- **A unit at the base no longer matches the binding table.** Possible, Minor: LOW, monitor. Owner: W03 author. IDs are permanent, so the table is compared with the base before the first ID. Review cue: the Task's table. Signal that raises it: a changed item or row count in a group. Rollback: stop and ask the user before any ID is issued.
- **A validator or test pins a line that a token splits.** Possible, Minor: LOW, monitor. Owner: W03 author. Tokens are added one group at a time with the suites run after. Review cue: the `tooling` suite and the quality gate. Signal that raises it: a failure that names a policy line. Rollback: revert the adoption commit.
- **Prose changes by accident.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The stripped-body comparison is byte for byte and no table is re-aligned. Review cue: the two hashes. Signal that raises it: unequal hashes. Rollback: revert the adoption commit.
- **The base moves.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0189 to SPEC-0202 merge first, and the names of SPEC-0194 are read from its approved text. Review cue: the base hash in the Task. Signal that raises it: a changed count or name. Rollback: stop and ask the user before any ID is issued.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| The rule IDs of the onboarding policy | [App GitOps onboarding policy](../../05.operations/policies/0007-app-gitops-onboarding-policy.md) | The `ONBOARD` record is `adopted` and the policy carries its Rules table and 45 tokens, with PASS evidence for VAL-ONBRULE-001 | The Rules table and definition tokens under `Requirements` |
| The Rules table required of every policy that states normative rules | [Document authoring policy](../../../.agents/governance/document-authoring.md) | The `ONBOARD` record is `adopted` and the policy carries its Rules table and 45 tokens, with PASS evidence for VAL-ONBRULE-001 | Form paragraph; `policy_rule_ids` and the Policy TemplateDefinitions in `docs/99.templates/registry.json` |
