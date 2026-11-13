---
title: "W03 Governance Role Forms Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0188-PLAN-0001"
parent_ids: ["SPEC-0188"]
---

# W03 Governance Role Forms Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document heading, sentence or table changes (the role template's eight H3 are the only template edit), and the diagnostics of the four strict document validators over the tree are equal before and after. SPEC-0186 and SPEC-0187 land first.

## Overview

Add the `governance-role` role and two form identifiers to the literals and schema; add the `governance-role` and `governance-document` forms; empty the four profiles' H2 lists and rebind the role pair; add the eight H3 with author prompts to the role template; update the two TemplateDefinitions and the policy texts. [Task 0001](tasks/tsk-0001-w03-governance-role-forms.md) owns execution and evidence.

## Context

SPEC-0186 gives six roles their forms and SPEC-0187 moves `sdlc.md` to `governance/rule`; this branch starts from the current W03 stack and is checked against the current `main` before delivery. A read of the tree found:

- 17 role files (`.agents/roles/*.md` without the README), all bound by `governance/role`, each with the six H2 titles and, under `Current Contract`, exactly the eight H3 `Role`, `When to Use`, `Inputs`, `Outputs`, `Guardrails`, `Capability and Evidence`, `Handoff / Escalation` and `Postflight` in that order, no H4, and a `Related Documents` of links only;
- two provider files, each with the six H2 titles, no H3 and a link-only `Related Documents`;
- six profiles bound to `governance-document` at HEAD (`governance/contract`, `governance/provider`, `governance/role` and their three twins), all with the same six-title H2 list and no form; after SPEC-0187 the contract pair no longer binds it;
- a role template with six H2 sections and one author prompt under `Current Contract`, and a template-mode author-prompt check that reads the H2 section body (levels up to H3 included);
- the role literal at 27, the form literal and enum closed at 18 (24 after SPEC-0186), and tests that pin 27 roles, the form counts and `form is None` for these roles;
- a SPEC-0161 Task with W03-H28 and decisions up to W03-D26 and W03-D30 to W03-D31 recorded, and W03-D34 added by SPEC-0186's commit.

## Goals & In-Scope

- Code and schema: one role and two form identifiers.
- Registry: two forms with 20 sections, four profiles with empty lists, the role pair rebound, two changed definitions.
- Role template: eight H3 with author prompts.
- Policy texts and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: role-parity, form-identifier parity and form tree cases.

## Non-Goals & Out-of-Scope

- Any change to the 17 role files, the two provider files or `.agents/roles/README.md`; the six SPEC-0186 roles; `reference-report`, `provider-native` and the research H3 titles; the binding of `sdlc.md`; the full TemplateDefinition record; phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GOVROLE-001](spec.md#success-criteria--verification-plan) | Role and form literals and schema; two forms; profile lists and role rebind; role template H3; definition texts; tests. | Approved Spec and Plan; SPEC-0186 and SPEC-0187 landed. | [Task 0001](tasks/tsk-0001-w03-governance-role-forms.md) | Failing tests first, then passing; strict registry check; the Task review-digest baseline lines moved in step 1 of the commit order. |
| WORK-002 | [VAL-GOVROLE-002](spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document proof; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-governance-role-forms.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators, the list of the 17 role files with their H3 titles and the two provider files before any change.
- Show each changed test failing before its change, then passing.
- Confirm in the Task that the 17 role files, the two provider files and the roles README are byte-identical before and after, and that the role template differs only by the eight H3 and their prompts.
- Commit order, four steps: (1) the baseline of the Task review digests alone; (2) the package commit with this package's entry in `docs/03.specs/README.md`; (3) the move of any shifted registry baseline line alone; (4) the implementation with the Task evidence. SPEC-0186 and SPEC-0187 land first; this package's own three files fall under the open-package layer rule of SPEC-0184. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- If a document gains a diagnostic, stop: fix the form, not the document; report as a repository defect after two failed attempts with no new information.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, schema, the role and form literals, one template and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval inventory's evidence.

- **A role file differs from the eight-H3 order the form fixes.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. A script over all 17 files found the same eight H3 in the same order and no H4; the strict validators run before and after. Review cue: a heading-order diagnostic on a role file. Signal that raises it: a new or edited role file with another H3. Rollback: revert the implementation commit.
- **The role template fails the template-mode author-prompt check after its H3 change.** Unlikely, Minor: LOW, monitor. Owner: W03 author. The check reads the H2 section body, which holds the H3 text, and the skill template already carries H3 with prompts and passes; each new H3 gets a prompt. Review cue: "must contain a useful Author prompt". Signal that raises it: a prompt comment removed. Rollback: revert the implementation commit.
- **SPEC-0187 leaves a profile bound to `governance-document` beyond the provider pair.** Possible, Minor: LOW, monitor. Owner: W05 code. At HEAD six profiles bind the role and two (the profile and its twin) belong to `governance/contract`; the Task re-lists the bindings before step 4 and stops if another remains. Review cue: a profile listing at the start of the Task. Signal that raises it: SPEC-0187 changing its scope. Rollback: revert the implementation commit.
- **Role, form-identifier and schema parity drift between code, schema and tests.** Possible, Minor: LOW, monitor. Owner: W05 code. `test_typed_stage_and_document_role_match_the_schema` and `test_typed_form_identifier_matches_the_schema_form_enum` compare literal and enum and fail first when one side changes; three counts (27 to 28, 24 to 26, 18 to 20) move together. Review cue: those tests. Signal that raises it: a role or form added in one place only. Rollback: revert the implementation commit.
- **Empty-section checks reject a document or the template in progress with SPEC-0182.** Unlikely, Minor: LOW, monitor. Owner: W03 author. The forms use `explain_none_or_not_applicable`, as the other forms do, no `BODY-SECTION-BARE` is recorded for the 19 documents at the base used for this draft, and the strict validators are compared before and after on the same base. Review cue: a `BODY-SECTION-BARE` diagnostic. Signal that raises it: a rebase onto a changed rule. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The governance role and governance document forms | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentences; machine forms in `docs/99.templates/registry.json` |
