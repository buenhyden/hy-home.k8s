---
title: "W03 Stage README Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0173-PLAN-0001"
parent_ids: ["SPEC-0173"]
---

# W03 Stage README Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes outside the 22 Stage README documents and two templates, and the output of the four strict document validators over the tree is equal before and after.

## Overview

Add the Stage README form, TemplateDefinitions and tables; bind the collection profile; read navigation from `Current Items`; let the document-content reader find H4 tables; move the 22 documents and two templates form-only; record W03-D16; update the policy texts. [Task 0001](tasks/tsk-0001-w03-stage-readme-form.md) owns execution and evidence.

## Context

SPEC-0172 gave the Root README its form and made README navigation read a form H3 (PR #237 open). This branch `claude/w03-stage-readme-form` starts from `a34539c2`, the SPEC-0172 closure, and is stacked on PR #237; before delivery it is checked against the current `main`. A read at `a34539c2` found:

- seven stage READMEs (96 to 274 lines, five H2 each) and fifteen collection READMEs (five H2 each);
- every index table in these 22 documents headed `Path | Purpose`;
- three of the four agent and provider READMEs (`.agents/`, `.claude/`, `.codex/`) naming some direct children only in code spans, which the complete-listing check of a collection profile would refuse (ten diagnostics, found by the pre-approval review); the user deferred their binding (W03-D16);
- the classification matrices and boundary tables sitting under Overview or Scope, not Structure;
- `scripts/validation/document_content.py` reading `Operations Routing Matrix`, `Incident Boundary Matrix` and the Korean-titled document index tables of the guides, policies and runbooks READMEs, in five of the 22 documents, by an H2 or H3 title.

## Goals & In-Scope

- Registry: form, TemplateDefinitions and tables, role binding, navigation sections, empty lists.
- Code: the document-content table reader accepts H4.
- 22 documents and two templates moved per the Spec's map; policy texts; the W03-D16 row and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: registry, navigation and reader cases, including the rewritten `RepositoryContractTests`.

## Non-Goals & Out-of-Scope

- The four agent and provider READMEs (W03-D16); the Service, Workspace and Reference Pack README roles; the retirement of the `README_H2_*` list rules; phase 3.
- New README content, links or child listings.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-STAGEREADME-001](spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinitions, tables, binding and navigation; the H4 table reader; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-stage-readme-form.md) | Failing tests first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-STAGEREADME-002](spec.md#success-criteria--verification-plan) | 22 documents and two templates moved with the map; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-stage-readme-form.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators over the whole tree before any change.
- Show each changed test failing before its change, then passing.
- Record per document in the Task: where each H2 and H3 went and every added line; run a word comparison per document.
- Commit order: the package commit, which adds this package's entry to `docs/03.specs/README.md` in its current form so its complete listing holds, and the W03-D16 rows; then the `.secrets.baseline` line move alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, one reader, tests and 22 router documents; no permission, trigger, hook, workflow or protected action) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **Meaning drift across 22 documents.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Word comparison per document and the map in the Task. Review cue: a removed word other than a heading. Signal that raises it: a changed sentence in the comparison. Rollback: revert the implementation commit.
- **Navigation or content checks stop reading a moved table.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The reader accepts H4, navigation reads `Current Items`, and validator output must equal the before run. Review cue: a navigation or content rule that no longer reports on a seeded defect in tests. Signal that raises it: any change in validator output. Rollback: revert the implementation commit.
- **The deferred agent and provider READMEs stay unbound.** Likely, Minor: MEDIUM, monitor. Owner: W03. They keep their current form on `common/readme-implementation` until the user decides their binding. Review cue: the Service README package, which must not take them as Service READMEs without that decision. Signal that raises it: W03 phase 2 closing with them unbound. Rollback: not applicable.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Stage README form and its navigation section | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; machine form in `docs/99.templates/registry.json` |
