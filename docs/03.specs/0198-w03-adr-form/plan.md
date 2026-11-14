---
title: "W03 ADR Form Plan"
version: "1.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0198-PLAN-0001"
parent_ids: ["SPEC-0198"]
---

# W03 ADR Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: 35 accepted ADRs are byte-identical before and after (ADR-0001 to ADR-0061 is the retained list, W03-D69), and ADR-0059 changes only by one dated clarification paragraph with its `version` and `updated`; the retained lists move from the profile to the extension unchanged; and the diagnostics of the four strict document validators over the tree are equal before and after. The `layer` rule follows W03-D22 and W03-D52 as the Spec states it.

## Overview

Add the ADR form with its local H3 extension and its retained form to the registry, give a retained form a closed identity bound and select it by status and identity, bind the decision profile and its template twin to the form, give the twin its TemplateDefinition and full record, move the decision template, write ADR-0062 in the common form, obtain the user's acceptance of it and add the dated clarification to ADR-0059 with that acceptance, and update the tests and texts. [Task 0001](tasks/tsk-0001-w03-adr-form.md) owns execution and evidence.

## Context

A read of `main` at `8daf643f` found `sdlc/architecture-decision` and its template twin with seven required H2 (Overview, Context, Decision, Explicit Non-goals, Consequences, Alternatives, Traceability), no form and no TemplateDefinition, while the registry holds 18 forms. The tree holds 35 ADRs, 284 KB together, all `accepted`, ADR-0002 to ADR-0060; all carry the seven H2 in that order, 34 carry `layer` and six carry `supersedes`. The body contract enforces `Lifecycle Traceability` under `Traceability` for `proposed` only. `scripts/document_contracts.py` defines the `retained_form` extension kind with `statuses` and `retained_sections`, and `CommonForm.retained_headings` selects it by status; `scripts/validate-markdown-profiles.py` then checks the retained lists in place of the tree, and `tests/test_common_form_tree.py` pins that an accepted document in the tree form fails. No form in the registry uses the kind. `FM-LAYER-ADR` refuses `layer` on an ADR that is not accepted, and the `layer` entry of `frontmatter_keys` says the key is never added to a new document. ADR-0059 Decision 5 says the H2 lists stay only for profiles whose role has no form yet and that the change that moves the last role removes them and their checks. ADR-0059 and ADR-0060 were each created `proposed`, accepted in a commit of their own and had their affected-Spec cell rewritten at the package exit; under SPEC-0185 each ADR that ADR-0060 narrowed gained a dated `Current-state clarification` paragraph and a patch raise (W03-D40). No pending package uses ADR-0062. No script names an ADR section; the link validator's lifecycle evidence reader derives heading validity from the form lists and that flag is read only for Tasks.

## Goals & In-Scope

- Registry and schema: the form, the local H3 extension, the retained form with its identity bound, the profiles' lists, the TemplateDefinition with `contract_version` and two tables, and the schema property.
- Code and tests: the retained-form selection by status and identity, its registry check, the identity-bound `layer` rule, and failing-first tests.
- Documents: the decision template; ADR-0062 and its README row; the dated clarification paragraph in ADR-0059; the document authoring policy sentences, the Stage 99 README bullet and sentence, and the Stage 02 `AGENTS.md` rules; the SPEC-0161 Task rows and ledger entries.

## Non-Goals & Out-of-Scope

- The other 35 accepted ADRs and every other part of ADR-0059; the ADR lifecycle domain and `rejected`; the other SDLC forms; the removal of the H2-list model and of the list-mode checks for profiles; Q-07.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ADRFORM-001](spec.md#success-criteria--verification-plan) | The form, both extensions, the identity bound in schema and code, the retained-form selection, the registry check, the profile lists, the TemplateDefinition and record, the `layer` rule and the tests. | Approved Spec and Plan; ADR-0061 of SPEC-0207 accepted by the user (a precondition: the retained form applies to accepted ADRs only); SPEC-0191, SPEC-0207, then SPEC-0188, SPEC-0189 and SPEC-0192 to SPEC-0197 merged in that order, then this package; rebase on `main` and renumber appended rows before each commit. | [Task 0001](tasks/tsk-0001-w03-adr-form.md) | Failing tests first, then passing; the strict registry validator with `REGISTRY_TEMPLATE_RECORD`. |
| WORK-002 | [VAL-ADRFORM-002](spec.md#success-criteria--verification-plan) | The decision template with every former prompt placed; ADR-0062 in the common form, its README row and the user's acceptance, with the dated paragraph in ADR-0059; the texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | WORK-001; the user's recorded approval of ADR-0062. | [Task 0001](tasks/tsk-0001-w03-adr-form.md) | The ADR byte comparison; strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Apply the MAJOR bump of the Spec (the registry value, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and `DOC_REGISTRY_MAJOR`) at the implementation commit and record the level and the reason in the Task; the version-pinning tests derive from the constants (SPEC-0207).
- Record the four strict document validators and the sha256 of each of the 36 accepted ADRs (35 plus ADR-0061 of SPEC-0207) before any change; 35 of them must be equal afterwards.
- Show each retained-form case failing first, then passing: inside and outside the range, in both forms, for `accepted` and `proposed`; and the registry check refusing a bad pattern. The case that expects the tree to fail for every accepted ADR is rewritten into the two identity cases, and the Task records both versions so the review can see nothing was weakened.
- Move the retained lists into the extension first and show the tree of 36 ADRs passing with empty profile lists before the template changes.
- Record in the Task where each former author prompt of the template went.
- Write ADR-0062 as `proposed` with the implementation; record the user's approval and set it `accepted` in a commit of its own, which also adds the dated clarification paragraph and the patch raise to ADR-0059; the package completes only after that.
- Confirm that `git diff --stat` over `docs/02.architecture/decisions/` shows only ADR-0062, the README and ADR-0059, that the other 35 hashes are equal, and that the diff of ADR-0059 is the one paragraph with its `version` and `updated`.
- Before each commit, rebase on `main`, take the next free ADR identity if ADR-0062 was used, and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit; then `.secrets.baseline` changes alone; then the implementation with ADR-0062 `proposed` and the Task evidence; then the acceptance of ADR-0062. Run `graphify update .` after the code change.
- Record the risk class (`medium`: the registry, its schema, two validators, a template, one new ADR and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **The retained form selects the wrong documents.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. A wrong bound gives 36 accepted ADRs a diagnostic or lets a new ADR keep the old form; the four identity and status cases fail first, and the strict validators are compared over the tree. Review cue: the retained-form tests and the before and after validator output. Signal that raises it: a diagnostic on an accepted ADR, or a common-form ADR that fails once accepted. Rollback: revert the implementation commit.
- **An existing test is weakened while it is rewritten.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. The case that expects an accepted ADR in the tree form to fail no longer holds for every identity; it is replaced by one case inside and one outside the range, and both versions are recorded. Review cue: the test diff in the core-diff checklist. Signal that raises it: fewer assertions about accepted ADRs than before. Rollback: restore the test and repeat.
- **An accepted ADR is edited.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. Only ADR-0059 is in scope, for one dated paragraph, and the other 35 hashes are compared. Review cue: the hash list, the diff stat and the ADR-0059 diff. Signal that raises it: another accepted ADR in the diff, or more than the one paragraph in ADR-0059. Rollback: restore the file.
- **ADR-0062 is not accepted.** Possible, Minor: LOW, monitor. Owner: the user. The retained lists would then contradict ADR-0059 Decision 5 when the last role moves; the package does not complete without the acceptance. Review cue: the acceptance row in the Task. Signal that raises it: the implementation merged with ADR-0062 still `proposed`. Rollback: none; the author stops and asks the user.
- **An earlier package changes the registry, the tests or the ADR numbering first.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Nine packages merge before this one and several change the form count, the record tests and the same test modules. Review cue: the base commit recorded in the Task. Signal that raises it: a merge conflict, or ADR-0062 already taken. Rollback: rebase the package.
- **The generator and the template disagree.** Possible, Minor: LOW, monitor. Owner: W05 code. The generator of SPEC-0192 fills this template, so its tests for an ADR run against the new template. Review cue: the generator tests in the `document` suite. Signal that raises it: a generated ADR that fails the profile check. Rollback: revert the template.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The ADR form, its retained form for ADR-0001 to ADR-0061 and its table contracts | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence and accepted-ADR sentence; `common_forms` and the decision TemplateDefinition in `docs/99.templates/registry.json`; the narrowing of ADR-0059 Decision 5 is recorded by ADR-0062 under `docs/02.architecture/decisions/`, which this package adds and the user accepts |
