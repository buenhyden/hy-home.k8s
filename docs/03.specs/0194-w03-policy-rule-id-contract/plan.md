---
title: "W03 Policy Rule ID Contract Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0194-PLAN-0001"
parent_ids: ["SPEC-0194"]
---

# W03 Policy Rule ID Contract Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no policy body gains a rule ID, a Rules table or any other change, apart from the one Policy sentence of the document authoring policy; no section of the shared Policy form changes; and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Add the `policy_rule_ids` registry section with its schema, authority key, loader and registry check; change the `Rules` table of the two Policy TemplateDefinitions and templates to the four common columns with the optional `Status`, record the table's condition and register the `Status` extension (W03-D65); add the six document rules with the adoption gate; register the fifteen codes as `pending`; add the tests and their registration; update the policy texts; and record W03-D53, the W03-H29 state and the unit inventory. [Task 0001](tasks/tsk-0001-w03-policy-rule-id-contract.md) owns execution and evidence.

## Context

A read of `main` at `de64c58d` and of the SPEC-0187 package at `362f59c4` found the following; every line number and count is re-read at implementation time, because SPEC-0187 to SPEC-0193 merge first.

- The Policy form has five H2 and ten H3 sections and one local H3; `policy-rules-requirements` states `안정 규칙 ID·조건·필수/권고/선택`. Both Policy TemplateDefinitions carry a `Rules` table under that section with the columns Rule, Condition and Evidence, `minimum_rows` 0 and row identity Rule, and both templates tell the author to delete the table when it does not help.
- No policy holds a table headed `Rule`, and no token of the grammar `<CODE>-R<NNN>` exists in the tree. The external requirement IDs `GIT-09` and `SDLC-04` share a prefix with the proposed codes `GIT` and `SDLC` and differ by the `-R`.
- The table check of `scripts/validate-markdown-profiles.py` finds a table by its first header cell, and `validate_document_text` receives one profile and no registry, so the code record reaches the check through the loaded profile.
- POL-0001 and POL-0005 each hold a `Control Register` table of six rows (`PLAT-001` to `PLAT-006`, `OBS-001` to `OBS-006`); the glossary keeps TERM-RULE and TERM-CONTROL apart.
- `tests/test_common_form_tree.py` pins the Policy table as (Rule, Condition, Evidence), unpacks three columns in the shared column test and pins the admitted top-level registry keys; `scripts/document_authority.py` lists them in `OPTIONAL_TOP_LEVEL_KEYS`.
- The W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md` (REQ, by line), lists rule, condition and evidence as conditional content of the Policy role (REQ:310, REQ:742), gives a rule its stable ID, condition and level (REQ:486), keeps a product difference only as a conditional extension with condition, owner, verification, review and removal criteria (REQ:37) and keeps the ban on reusing past numbers (REQ:143). W03-D65 rests on these lines. `shared_contract.extensions` already holds seven entries of that shape, and a table definition has no field for a condition, in the registry schema or in the package's TemplateDefinition schema, so the condition is recorded in `policy_rule_ids`.
- Estimated rule units under `Requirements` (top-level list items, table rows and H4 groups without a list or table; the upper figure adds paragraphs that may need a unit): `agent-execution` 12, `approval-and-safety` 20 to 23, `context-and-memory` 19 to 20, `document-authoring` 14 to 23, `document-lifecycle` 21, `formatting-and-linting` 12, `git` 11, `model-selection` 7, `quality` 45 to 56, `sdlc` 33 to 39 (read from its `Current Contract` section before SPEC-0187), POL-0001 18, POL-0003 11, POL-0004 9, POL-0005 7, POL-0007 46 to 59; about 195 to 225 for governance and 90 to 105 for operations. These are estimates for sizing packages 3 and 4 and no part of the contract.

## Goals & In-Scope

- Registry and schema: the `policy_rule_ids` section with the table's condition, the fifteen `pending` records, the `Status` entry of `shared_contract.extensions` and the `Rules` table of both definitions with four required columns and the optional `Status`.
- Code: the authority key, the loader, `REGISTRY_POLICY_RULE_CODE` and the six document rules.
- Templates, tests and their registration, the policy texts, the SPEC-0161 Task rows and the ledger entry.

## Non-Goals & Out-of-Scope

- Rule IDs and Rules tables in the fifteen policies (packages 3 and 4); the no-reuse check across history (package 5); the shared form sections; control registers and control IDs; the glossary; the generator's code.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RULEID-001](spec.md#success-criteria--verification-plan) | The registry section and its schema, the authority key, the loader, `REGISTRY_POLICY_RULE_CODE`, the fifteen records, the table's condition, the `Status` extension, the conditional table in both definitions and both templates, and the changed Policy table tests. | Approved Spec and Plan; SPEC-0187 to SPEC-0193 merged. | [Task 0001](tasks/tsk-0001-w03-policy-rule-id-contract.md) | Failing tests first, then passing; registry check; template parity. |
| WORK-002 | [VAL-RULEID-002](spec.md#success-criteria--verification-plan) | The six document rules and the adoption gate; `tests/test_policy_rule_ids.py`, its suite membership and its surface route; the generator's recorded authoring set if a rule reaches it. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-policy-rule-id-contract.md) | A passing and a refused case for each rule, in English and Korean; the `document` suite. |
| WORK-003 | [VAL-RULEID-003](spec.md#success-criteria--verification-plan) | Policy texts; W03-D53, the W03-H29 state cell and the ledger entry; the unit inventory; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-policy-rule-id-contract.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators before any change.
- Show the new registry and document tests failing first, then passing; show the fifteen real policies drawing no new diagnostic while their records are `pending`.
- Run the coverage reader over the fifteen policies without asserting IDs and record in the Task, for each, the top-level items, table rows, H4 groups and control rows it reads; this unit inventory sizes packages 3 and 4 and shows that the reader copes with the real documents.
- Record that no policy body changed, by the before and after hashes of the fourteen untouched policies and the one-sentence diff of the document authoring policy.
- Commit order: the package commit with the W03-D53 row; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Record the risk class (`medium`: the registry, its schema and guard, the loader, one validator and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **The coverage floor misreads a real policy.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. No policy is adopted here, so the rules run only on synthetic documents; the unit inventory runs the reader over the fifteen policies. Review cue: the inventory against the estimates in Context. Signal that raises it: a policy that needs rewording to pass. Rollback: revert the implementation commit.
- **The adoption gate outlives package 4.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The W03-H29 row and its ledger entry name the retirement, and the registry shows every `pending` record. Review cue: the W03 closing (W03-H20). Signal that raises it: a `pending` record or `POLICY-RULE-ADOPTION` after the last adoption. Rollback: none needed; the retirement is a later commit.
- **A generated policy draws a new rule and the generator test fails.** Likely, Minor: MEDIUM, monitor. Owner: W05 code. The recorded authoring set is in scope. Review cue: the `document` suite. Signal that raises it: a generator test failure outside that set. Rollback: revert the implementation commit.
- **The base moves under the shared files.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0193 adds another top-level section to the same registry, schema, guard and loader; this package merges after it and re-reads every fact. Review cue: the base hash in the Task. Signal that raises it: a conflict or a changed count. Rollback: rebase before the implementation commit.
- **A code proves wrong after adoption.** Possible, Minor: LOW, monitor. Owner: W03 author. A code may change while `pending` and the user reviews the fifteen codes with W03-D53. Review cue: package 3 and 4 approval. Signal that raises it: a request to rename an adopted code. Rollback: none; an adopted code is permanent until a user-approved new baseline under the Q-07 contract (REQ:143).
- **A rule ID is read as a control ID or an external requirement ID.** Possible, Minor: LOW, monitor. Owner: W03 author. The grammar requires `-R`, `PLAT` and `OBS` are reserved, and tests show a control row is never a rule unit. Review cue: the code list. Signal that raises it: a code equal to a control prefix. Rollback: change the pending code.
- **A policy evades the floor by writing rules as prose.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. A `Requirements` section that holds only prose paragraphs counts, for the check, as stating no rule, so neither the Rules table nor the coverage floor applies to it (W03-D65); the semantic review judges whether such prose states a rule. Review cue: a policy without a Rules table. Signal that raises it: a prose paragraph under `Requirements` that states an obligation. Rollback: none needed; the review sends the rule to a unit that takes an ID.
- **An existing document gains a diagnostic.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. Every record is `pending` and the validators are compared before and after. Review cue: the strict validators. Signal that raises it: any new diagnostic. Rollback: revert the implementation commit.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Rule ID grammar, Rules table, definition token and registered code | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Form paragraph; `policy_rule_ids` and the Policy TemplateDefinitions in `docs/99.templates/registry.json` |
