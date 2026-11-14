---
title: "W03 Spec and Plan Forms Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0200-PLAN-0001"
parent_ids: ["SPEC-0200"]
---

# W03 Spec and Plan Forms Implementation Plan

## Overview

### Goal and Boundary

Add the Spec and Plan forms to the registry and bind the four profiles, move both body contracts and add the Spec's design constraint link, give both templates their TemplateDefinition and record, make the Plan and completion readers take their headings from the registry so that the Plan and Task rules stay active, add the two one-use exemptions, move the templates, the frozen Spec and Plan of SPEC-0161 and the Spec and Plan of every open package, repoint every link to the removed Spec anchor, update the tests and texts, and retire both exemptions. [Task 0001](tasks/tsk-0001-w03-spec-plan-forms.md) owns execution and evidence.

In scope:

- Registry: two forms, one local extension, four profiles' lists, both body contracts, two TemplateDefinitions with four tables, and the `relationship_contract` entries that name a heading or the design constraint gap.
- Code and tests: three readers with a form shape and the old shape; two one-use exemptions and their retirement; failing-first tests for each; the anchor strings in the seven consumer test modules and the fixture.
- Documents: both templates and the Task template's link fragments; the frozen Spec and Plan of SPEC-0161; the link fragments of the SPEC-0161 Task; the Spec, Plan and Task link fragments of every open package; the texts; the SPEC-0161 Task rows and ledger entries.

Out of scope:

- The Task form and Task headings; the Requirement, Architecture and ADR forms; the removal of the H2-list model; any change to what a finished package's Spec or Plan says; Q-07.

#### Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds five constraints: `PLAN-PROMOTION`, `PLAN-GLOBAL-CONSTRAINTS` and `TASK-PARENT-APPROVAL` are active in every commit of this package and none checks less than it does today (line 113 of the W03 prompt), so the reader learns the form shape before the registry binds the forms and no commit binds a form with a rule switched off; the frozen Spec and Plan of SPEC-0161 change only to the bytes the user reviews; a recorded evidence row changes at most by the mapped link fragment; no gate is left weaker when the package closes, because both one-use exemptions are removed in the final source commit; and the diagnostics of the four strict document validators over the tree are equal before and after. The design choices follow W03-D59, W03-D65 and W03-D66 as the Spec states them.

### Assumptions

A read of `main` at `a8c689e5` found `sdlc/spec` with eleven required H2 and `sdlc/plan` with eight required and two optional H2 (`Global Constraints`, `Promotion`), no form and no TemplateDefinition for either, while the registry holds 21 forms. The Spec body contract reads `Lifecycle Traceability` under `Traceability` and the Plan body contract reads it under `Work Breakdown`; the Spec `Architecture` column has no link column behind it. `scripts/validate-document-lifecycle.py` names Spec and Plan headings on seven lines: the guard `"Promotion" not in plan_profile.headings.allowed` (676), `## Promotion` with its three-column header (688, 698), `## Global Constraints` (753, 776) and `## Success Criteria & Verification Plan` with its header (2764, 2769). The promotion header `Durable contract`, `Promoted to`, `Where` occurs on line 698 of that script, in three places of `tests/test_task_execution_contract.py`, in one fixture, in the Plan template and in the SPEC-0161 Plan, whose one recorded row is the explicit none row. The guard returns before the Plan and Task loops, so the Plan form would switch off `PLAN-PROMOTION`, `PLAN-GLOBAL-CONSTRAINTS` and `TASK-PARENT-APPROVAL` silently. `_exact_heading_section` in `scripts/validate-links-and-owners.py` (line 2522) ends a section only at the next heading of the same or a higher level, so an H4 placed first under Goal and Boundary would take every body after it, up to `### Assumptions`, as its own. The cumulative-history check calls the same reader with each old commit's registry. No other script names a Spec or Plan heading. The tree holds one package, SPEC-0161: its Task is `completed`, so `package_exit_diagnostics` refuses any edit to its Spec and Plan under R4, and `_task_evidence_retention_diagnostics` compares the `Criteria` cell of each of its 55 recorded evidence rows as text. 65 places in that package name `spec.md#success-criteria--verification-plan` (58 links in evidence rows, 2 in the Task Table, 2 in Criterion Acceptance, one code-span mention under `### OPEN Dispositions` and 2 links in the Plan), and 4 placeholder links do, 1 in the Plan template and 3 in the Task template. The `Architecture` cells of the SPEC-0161 Spec already link an architecture description or an ADR. Four test modules and one fixture name Spec or Plan headings, and five test modules and that fixture hold the anchor string in 17 places. Three of those five are not among the four: `tests/test_task_acceptance_contract.py` (1 place), `tests/test_task_acceptance_boundaries.py` (2) and `tests/test_documentation_link_boundary.py` (1). That makes seven consumer test modules and one fixture. Five texts name a Spec or Plan section (the lifecycle policy, the `risk-report` skill, the Stage 99 README, the Stage 03 README and rule 7 of the Stage 03 `AGENTS.md`, which names the Plan's `Promotion` table). SPEC-0184 is the model for a one-use exemption with its retirement (`git show fab903a3:docs/03.specs/0184-w03-remove-layer-key/spec.md`).

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SPECPLAN-001](spec.md#criteria) | The three readers with the form shape and their tests first, so the Plan and Task rules stay active; then the forms, the extension, the profile lists, the body contracts with the design constraint link, and the TemplateDefinitions and records. | Approved Spec and Plan; SPEC-0207 and SPEC-0192 to SPEC-0199 merged in that order after SPEC-0191, which has merged, then this package; rebase on `main` and renumber appended rows before each commit. | [Task 0001](tasks/tsk-0001-w03-spec-plan-forms.md) | Failing tests first, then passing; the three rules shown active on the bound registry; the strict registry validator with `REGISTRY_TEMPLATE_RECORD`. |
| WORK-002 | [VAL-SPECPLAN-002](spec.md#criteria) | The two one-use exemptions with their tests; the templates; the frozen Spec and Plan after the user's review; the repointed links, with the anchor strings of `tests/test_task_acceptance_contract.py`, `tests/test_task_acceptance_boundaries.py`, `tests/test_documentation_link_boundary.py` and the other consumer tests; the Spec and Plan of each open package with the inventory. | WORK-001; the user's review of the two moved files. | [Task 0001](tasks/tsk-0001-w03-spec-plan-forms.md) | The frozen-file and evidence-row comparisons; strict validators and markdownlint. |
| WORK-003 | [VAL-SPECPLAN-002](spec.md#criteria) | The texts; the SPEC-0161 Task rows and ledger entries; the retirement of both exemptions in the final source commit; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-spec-plan-forms.md) | The gates refusing the same edits again; suites, quality gate, ruff, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators, the list of links to the old anchor and the inventory of open packages before any change.
- Show the placement defect first: a Plan in the form whose `Global Constraints` H4 stands first under Goal and Boundary with an empty body, followed by goal text that links the parent Spec, passes, because the section reader takes the goal text as constraints. Then place the H4 last in the heading map and the template, make the rule fail a Plan whose H4 has no goal or scope text before it, and show that Plan failing and the prose under `### Assumptions` not read as constraints; the test stays in the suite. For every moved Plan, record that the text the rule reads after the move equals the body of the old `## Global Constraints` section.
- Produce the moved Spec and Plan of SPEC-0161 outside the tree first. Record for each the sorted non-heading, non-blank lines before and after, every added line and its sha256, and give both files to the user. Only the reviewed hashes enter the R4 exemption; show the reviewed file passing and a one-byte variant refused. For the Plan, record the promotion table before and after: three mapped headers, the three recorded cells unchanged, and the one added `Acceptance` cell, which states the condition the Plan already gives or `none` on the none row. Show `PLAN-GLOBAL-CONSTRAINTS` refusing a Plan without the `Global Constraints` H4 and one whose H4 does not link the parent Spec, as it refuses them today.
- Show an evidence row that differs only by the mapped fragment passing and one that differs in its criterion identifier or link path refused; then repoint the links and record, for each of the evidence rows counted after the rebase (55 at `a8c689e5`), that nothing else changed, and record the carve-out from rule 4 of `docs/03.specs/AGENTS.md` with the number of repointed fragments.
- Record the registry bump as evidence: the level NO_CHANGE under the rule of SPEC-0207, the reason (no key, type, requiredness or enumeration of the registry changes and the schema file is untouched) and the unchanged value of `schema_version`. Stop if the schema file must change.
- Record the risk class (`medium`: the registry, the lifecycle readers, two freeze gates with one-use exemptions, templates, frozen records and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. `PLAN-PROMOTION`, `PLAN-GLOBAL-CONSTRAINTS` and `TASK-PARENT-APPROVAL` must be shown active on the final tree, after both exemptions are retired.

### Stage Placement

- Keep the three rules active, in this order. First show, on a synthetic registry with the Plan form bound and the reader unchanged, that a changed Plan without a valid promotion table passes; that is the defect. Then change the reader so it takes its headings from the form by section id and fails closed when a Plan form lacks a section it needs, and show the same Plan failing `PLAN-PROMOTION`, a Plan without shared constraints failing `PLAN-GLOBAL-CONSTRAINTS` and an executable Task without an approved parent failing `TASK-PARENT-APPROVAL`. Only then bind the forms in the repository registry, in the same commit, and run those three cases against the repository registry; they stay in the suite as regression tests. Show each reader on a form registry, an old-list registry and a registry with neither, and the cumulative-history suite unchanged. The old-shape branch reads the allowed H2 through one accessor function; a test that replaces the accessor shows that no other line reads the list field, so SPEC-0205 can rename it.
- Before each commit, run the staged lifecycle check with a deliberately invalid Plan in a temporary copy and record that `PLAN-PROMOTION` refuses it, so no commit of this package leaves the rules off.
- Move the frozen pair, the SPEC-0161 Task links, this package and any other open package in one commit, so no link names a removed anchor between commits; each open Task gains an appended row with the before and after hashes of its Spec and Plan.
- In the final source commit, before the Task freezes, remove both exemptions, their tests and their policy sentences, and record R4 refusing an edit to the frozen pair and the retention rule refusing a fragment change again.
- Before each commit, rebase on `main`, take the inventory of open packages again and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit with the W03-D59 row; then `.secrets.baseline` changes alone; then the implementation with the Task evidence; then the retirement. Run the staged lifecycle check before each commit and `graphify update .` after the code change.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **The Plan and Task rules switch off when the form binds.** Without a control this is Likely, Moderate: HIGH, because the guard on line 676 returns as soon as the form removes `Promotion` from the lists, and it would block the implementation commit. This Plan closes it: the first Global Constraint keeps `PLAN-PROMOTION`, `PLAN-GLOBAL-CONSTRAINTS` and `TASK-PARENT-APPROVAL` active in every commit; the reader takes its headings from the form by section id before the forms bind; a Plan form that lacks a needed section fails the rule instead of skipping it; three regression tests on the repository registry stay in the suite; and Completion requires the rules shown active on the final tree. With those controls the residual is Unlikely, Moderate: LOW, monitor. Owner: W05 code. Review cue: the three regression tests and the per-commit refusal record. Signal that raises it: a changed Plan without a promotion table that passes, or one of the three tests removed. Rollback: revert the implementation commit, which also unbinds the forms.
- **The constraints heading takes other text as constraints.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. The section reader ends an H4 section only at the next heading of the same or a higher level, so an H4 placed first under Goal and Boundary would read the goal and scope bodies as constraints and let a Plan without constraints pass. The heading map and the template place the H4 last, the rule fails a Plan whose H4 has no goal or scope text before it, a regression test stays in the suite, and the text read for each moved Plan is compared with the old section body. Review cue: that test and the per-Plan comparison. Signal that raises it: a Plan with an empty constraints body that passes. Rollback: revert the implementation commit.
- **An exemption admits more than the reviewed change.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. R4 admits two exact files by hash and the retention route one fragment pair; tests show every other change refused, and the final source commit removes both. Review cue: the refusal tests and the retirement evidence. Signal that raises it: an exemption left after closure. Rollback: remove the exemption.
- **A frozen record or an evidence row changes in meaning.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The two frozen files are compared line by line and reviewed by the user before their hashes are admitted, and each evidence row is compared cell by cell. Review cue: the two comparisons in the Task. Signal that raises it: a difference that is not a listed line or the mapped fragment. Rollback: restore the file from the base commit.
- **A history replay reads an old Plan with the new shape.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. Each reader takes its shape from the registry of the commit it judges, the old-shape branch reads the list field through one accessor that SPEC-0205 re-points, and the cumulative-history suite runs unchanged. Review cue: that suite. Signal that raises it: a diagnostic on a past commit. Rollback: revert the implementation commit.
- **A link names the removed anchor after the move.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. 68 links and one code-span mention are known at `a8c689e5`, counted again after each rebase, and `LINK-FRAGMENT` refuses any link that remains, so the links move in the same commit as the Specs. Review cue: the anchor search before and after. Signal that raises it: a link validator diagnostic. Rollback: repoint the link.
- **Approved bytes of open packages change.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Each open Task records the before and after hashes and the reason. Review cue: the inventory in the Task. Signal that raises it: an open package without that row, or a second finished package in the tree. Rollback: none needed.
- **An earlier package changes the registry, the readers or the tests first.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0207 and SPEC-0192 to SPEC-0199 merge before this one. Review cue: the base commit recorded in the Task. Signal that raises it: a merge conflict. Rollback: rebase the package.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| The Spec and Plan forms, their body contracts and table contracts | [Document authoring policy](../../../.agents/governance/document-authoring.md) | The Document authoring policy names the Spec and Plan forms and the registry holds both forms with their TemplateDefinitions. | Forms sentence; `common_forms` and both TemplateDefinitions in `docs/99.templates/registry.json` |
| The Plan's shared constraints under Goal and Boundary and its promotion table under Owner and Receipt | [Document lifecycle policy](../../../.agents/governance/document-lifecycle.md) | The Document lifecycle policy names Global Constraints under Goal and Boundary and the promotion table under Owner and Receipt, and PLAN-GLOBAL-CONSTRAINTS and PLAN-PROMOTION read them. | The Plan sentence that now names `Global Constraints`; `PLAN-GLOBAL-CONSTRAINTS` and `PLAN-PROMOTION` |
