---
title: "W03 Policy Rule ID History Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0206-PLAN-0001"
parent_ids: ["SPEC-0206"]
---

# W03 Policy Rule ID History Implementation Plan

## Overview

### Goal and Boundary

Add the three history rules to the document lifecycle check with their tests first, expose the one Rules table reader to it, run and record the landing audit, state the permanence in the policy texts under their new rule IDs, record W03-D64 and close W03-H29. [Task 0001](tasks/tsk-0001-w03-policy-rule-id-history.md) owns execution and evidence.

Goals and in-scope:

- Lifecycle check: three rules, the base rows and the base code section; one shared Rules table reader.
- Tests over Git snapshots and their registration.
- The landing audit, recorded and not committed as a check.
- Policy texts with their new rule IDs; the W03-D64 row; the closure of W03-H29.

Non-goals and out-of-scope:

- Existing rule IDs, rows and codes; the rules of SPEC-0194; the meaning of an active rule; the artifact identity and Task row rules; a walk of old commits at every run, a recorded high-water mark and a committed audit script; hosted CI.

#### Global Constraints

This work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no existing rule ID, Rules table row or code changes; no existing lifecycle rule, base mode or test is weakened; and the diagnostics of the four strict document validators outside the scope are equal before and after.

### Assumptions

A read of `main` at `81096a83` (after SPEC-0189) and of the Spec texts of SPEC-0194, SPEC-0199, SPEC-0201, SPEC-0202 and SPEC-0204 found the following; every name is re-read at implementation time, because none of those packages is implemented at that commit and SPEC-0190 to SPEC-0204 merge first.

- `scripts/document_lifecycle.py` already keeps identities across Git: `_task_item_edge_diagnostics` compares the base Task rows with the proposed rows and refuses a removed work ID (`TASK-ITEM-DELETE`), a hidden table (`TASK-ITEM-HIDE`) and a backward state, and `artifact_identity_reuse_diagnostics` refuses an artifact identity that the base or a retired lineage reserves (`LIFECYCLE-IDENTITY-REUSE`). The evidence context carries the base Task rows for them.
- `scripts/validate-document-lifecycle.py` picks the comparison base by mode: `staged` compares the index with `HEAD`, `ci` a ref with its merge base, `explicit-ref` two named refs, and `snapshot` has none. The registered `document-lifecycle` validator of the `affected` and `staged` lanes runs the default `strict` mode, which compares the index with `HEAD` as `staged` does, so every commit that passes staged QA is one compared step.
- The comparison classifies the base with the current registry and parses no historical registry (W03-D54). A separate reader, `registry_at`, loads the registry a commit carried for the cumulative-history rules, and falls back to the current registry when the schema version differs. The code rule uses neither: under W03-D64 it reads one section of the base registry blob as plain JSON.
- SPEC-0194 requires each Rules table to ascend from `R001` without a gap and to carry its document's code, and refuses a reserved code for a policy; its reader of the table lives in the profile check. Within one document those rules cannot see the deletion of the last row.
- SPEC-0204 removes `state`, so after it no record is `pending` and a code can no longer change under the sentence of SPEC-0194.
- Under W03-D65 the Rules table is conditional content whose condition is that the policy states normative rules (REQ:310, REQ:742), and `Status` is a registered conditional extension in `shared_contract.extensions` (REQ:37, REQ:143); the reissue rule is added to the verification that entry records.
- The document lifecycle policy does not count a shallow clone, a reflog-only object or a squashed history as retained history, and the quality policy says hosted CI runs no document check.
- The W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md`, keeps the ban on reusing past numbers and the history reservation in force until the transition (line 143), keeps recorded acceptance and current failures (lines 149 and 173), preserves the reserved history and the stable IDs (line 226) and forbids a standing gate over historical bodies that contradicts the new contract (line 778). `scripts/AGENTS.md` keeps no check of a finished one-time transition (rule 3) and bounds every subprocess, file read and output (rule 4). W03-D64 rests on these lines.
- Between the adoption commits of SPEC-0199 to SPEC-0204 and this package, nothing checks history; the window is a few merges long and holds between 329 and 342 issued IDs under the binding tables and ranges of those packages: 151 to 164 for the nine governance policies, 51 for the quality policy, 82 for four operations policies and 45 for the onboarding policy.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RULEHIST-001](spec.md#criteria) | `POLICY-RULE-DELETE` and `POLICY-RULE-REISSUE` in the lifecycle check, the base Rules tables in the evidence context, the shared reader, and their tests. | Spec and Plan approval; SPEC-0194 implemented; SPEC-0204 merged. | [Task 0001](tasks/tsk-0001-w03-policy-rule-id-history.md) | Tests over Git snapshots failing first, then passing; lifecycle suites unchanged. |
| WORK-002 | [VAL-RULEHIST-002](spec.md#criteria) | `POLICY-CODE-CHANGE`, the base code section, the rule for a departing policy and the reserved list, and their tests; suite membership and surface route of the new module. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-policy-rule-id-history.md) | Refusal tests failing first, then passing; the `document-lifecycle` suite. |
| WORK-003 | [VAL-RULEHIST-003](spec.md#criteria) | The landing audit; the policy texts with their new rule IDs and rows; W03-D64, the closure of W03-H29 and its ledger entry; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-policy-rule-id-history.md) | Audit result for fifteen policies; strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators and the lifecycle suites before any change.
- Write the tests first, each over two real Git snapshots as the lifecycle tests build them, and show each refusal failing before its rule exists.
- Record the risk class (`medium`: the lifecycle check, one exposed reader, tests and three policy texts; no permission, trigger, hook or workflow) and the core-diff checklist.

Completion criteria:

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

### Stage Placement

- Run the landing audit before the policy texts change: for each of the fifteen policies, list the commits from its adoption to the base, read the Rules table at each, and record the ID set, the retired rows and the code at each step; record a finding as a stop, and keep the audit script out of the index.
- Add the policy sentences under their next rule IDs and show the staged lifecycle check and the profile check passing on that commit, which is the first change the new rules judge.
- Commit order: the package commit with the W03-D64 row; then `.secrets.baseline` changes alone; then the rules with their tests; then the policy texts and the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **A commit escapes the check.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. The rules are inductive and run in local staged QA; a commit made without the hooks, or a rewritten history, is not seen later, and hosted CI runs no document check. The `ci` and `explicit-ref` modes can compare any range on demand. Review cue: the pull request diff of a policy's Rules table. Signal that raises it: a table with fewer rows than at its last reviewed commit. Rollback: none; restore the row from Git history with the user's decision.
- **Reading the base registry breaks base loading.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. W03-D54 keeps the typed parse of a historical registry out of the comparison; under W03-D64 the code rule reads one section as plain JSON, builds no typed registry and treats an absent section as no rule. Review cue: the test with a base that lacks the section. Signal that raises it: a lifecycle failure on an old base. Rollback: revert the code rule; the ID rules stay.
- **A rule refuses an allowed change.** Possible, Minor: LOW, monitor. Owner: W05 code. Tests cover a rename, a retirement, an appended row, a moved rule and a departing policy. Review cue: the passing cases. Signal that raises it: a refusal on a change the contract allows. Rollback: fix the rule; no test is relaxed.
- **A second reader of the Rules table drifts.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. The lifecycle check calls the reader of the profile check. Review cue: one definition of the table grammar. Signal that raises it: a table one check accepts and the other cannot read. Rollback: remove the copy.
- **The landing audit finds a loss.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The window is a few merges long. Review cue: the audit record. Signal that raises it: an ID absent at a later commit. Rollback: stop and ask the user.
- **The base moves.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0190 to SPEC-0204 merge first and five of them define the names this package uses. Review cue: the base hash in the Task. Signal that raises it: a changed name or field. Rollback: re-read before the first commit.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| Rule IDs and codes are permanent until a user-approved new baseline under the Q-07 contract | [Document authoring policy](../../../.agents/governance/document-authoring.md) | The `AUTHOR` policy states the permanence of a rule ID and a code under a new rule ID with its Rules table row, and the history rules run in the lifecycle check, with PASS evidence for VAL-RULEHIST-003 | The rule ID sentences under `Requirements`, with a rule ID of that policy; the history rules of `scripts/document_lifecycle.py` |
| What a departing policy owes | [Document lifecycle policy](../../../.agents/governance/document-lifecycle.md) | The `DOCLIFE` policy states the disposition of a departing policy under a new rule ID with its Rules table row, with PASS evidence for VAL-RULEHIST-003 | A disposition rule under `Requirements`, with a rule ID of that policy |
