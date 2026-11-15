---
title: "W03 Task Form Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0203-PLAN-0001"
parent_ids: ["SPEC-0203"]
---

# W03 Task Form Implementation Plan

## Overview

### Goal and Boundary

Make the Task readers take their sections from the registry of the side they read, show every `TASK-` rule active on the form, add the Task form and bind the Task profile and its template twin, give the twin its TemplateDefinition and record, move the template and the headings of every Task in the tree without touching a row, follow the work residue host, and update the template check, the tests and the texts. [Task 0001](tasks/tsk-0001-w03-task-form.md) owns execution and evidence.

In scope:

- Code and tests: the evidence reader and its six call sites; the header map with its one function and its replay test; the ledger validator's read of the evidence rows; the two-registry read of base rows; the registry check of the binding sections; the Task template check; three messages; a first test that shows the defect and regression tests that stay.
- Registry: the column extension kind in the schema; the MAJOR step of `schema_version` with `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the guard's `DOC_REGISTRY_MAJOR`; the form, its local extensions, two profiles' lists, the body contract and `task_execution` binding, the TemplateDefinition with three tables, and the `work_residue` host.
- Documents: the Task template; the headings of every Task in the tree with each added line listed; eight texts; the SPEC-0161 Task rows and ledger entries.

Out of scope:

- Any cell of a recorded Task row; the columns of the work-row and decision tables; the other SDLC forms; the removal of the H2-list model; the ledger's design; Q-07.

#### Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds five constraints: every `TASK-` rule that is active before this package is active in every commit of it, so the readers learn the form before the registry binds it and no commit binds the form with a rule switched off; no recorded data row of any Task changes, in any table, and the evidence table changes only its header line by the recorded map; no exemption or one-use route is added to any rule; the Registry Schema Version rises by exactly one MAJOR step under the bump rule of SPEC-0207, and the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the guard's `DOC_REGISTRY_MAJOR` change in one commit, with no commit that holds a write guard for two MAJOR numbers; and the diagnostics of the four strict document validators over the tree are equal before and after. The design choices follow W03-D61, W03-D65 and W03-D66 as the Spec states them.

### Assumptions

A read of `main` at `a8c689e5` found `sdlc/task` and `common/template-sdlc-task` with seven required H2 (Overview, Inputs, Task Table, Task Evidence, Criterion Acceptance, Approval and Safety Boundaries, Verification Summary), no form and no TemplateDefinition, while the registry holds 21 forms. The body contract reads `Lifecycle Traceability` under `Task Table`; the `task_execution` binding names `Task Evidence` and `Criterion Acceptance`, and its readers take the first table of that H2. The 32 `TASK-` rule identifiers live in `scripts/document_contracts.py`, `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py` and `scripts/validate-markdown-profiles.py`. `task_base_evidence_rows` in `scripts/validate-links-and-owners.py` reads the literal `## Task Evidence` and is called on six lines of `scripts/validate-document-lifecycle.py`: for the base and proposed rows of `TASK-EVIDENCE-RETENTION`, inside the Task loop of the local contract check, and for the first-record approval receipt. `_evidence_context` reads a base Task's work rows with the profile of the one registry it is given, and `_task_item_edge_diagnostics` returns nothing when it finds no base rows. So a bound form with unchanged readers would, in the moving commit, report all recorded evidence rows as deleted and skip the four `TASK-ITEM-` rules, and afterwards find no evidence row at all: the retention rule would pass on nothing and no new package could record its approval. `_task_doc` in `scripts/validate-work-residue-ledger.py`, which SPEC-0191 added, calls the same reader without a registry, reads `Evidence` and `Result` by literal name and turns a missing table into an empty mapping. `scripts/validation/repository/quality.py` requires nine phrases in the Task template, one of them the H2 `## Approval and Safety Boundaries`. The tree holds one Task, the SPEC-0161 Task: 121 KB, `completed`, version 0.1.33, 55 evidence rows, 14 H3 under `Task Evidence`. Five test modules and one fixture name a Task heading in 24 places, one template in five heading lines and eight texts in 20 places, the reference maintenance runbook among them; no link names a Task anchor. The nine evidence column names are read by name in five scripts, bound on two profiles, written in the template, in five test modules and one fixture, and named in three text sentences. SPEC-0191, which has merged, registers the Task's `Residue Handoff` table and its historical tables in `work_residue`; SPEC-0192 generates a Task from the template, SPEC-0196 checks the full TemplateDefinition record and SPEC-0200 moves the Spec and Plan and makes the Plan reader registry-driven, and none of those three is on `main` at this base.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TASKFORM-001](spec.md#criteria) | The readers first: the evidence reader by binding, the two-registry read, the registry check and the tests that show every `TASK-` rule active on the form; then the form, the extensions with the column extension, the profile lists, the body contract and binding with the mapped evidence columns, and the TemplateDefinition and record; the MAJOR step of `schema_version` in the same commit. | Approved Spec and Plan; SPEC-0207 and SPEC-0192 to SPEC-0200 merged in that order after SPEC-0191, which has merged, then this package; rebase on `main` and renumber appended rows before each commit. | [Task 0001](tasks/tsk-0001-w03-task-form.md) | The defect test failing first, then passing; one failing case for each rule on the bound registry; the strict registry validator with `REGISTRY_TEMPLATE_RECORD`. |
| WORK-002 | [VAL-TASKFORM-002](spec.md#criteria) | The Task template and its quality check; the headings of the SPEC-0161 Task and of every other Task in the tree with the inventory; the `work_residue` host; the eight texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-task-form.md) | The per-row comparison of every moved Task; strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators, the inventory of Tasks and, for each Task, the sha256 of the ordered data rows of each of its tables before any change.
- Keep the rules active, in this order. First show the defect on a synthetic registry with the Task form bound and the readers unchanged: a later commit that edits a recorded evidence row passes, a moving commit skips the work-row rules, and a new package's approval receipt is not found. Then change the readers so each side is read with its own registry, and show one failing case for each of `TASK-EVIDENCE-RETENTION`, `TASK-ITEM-DELETE`, `TASK-ITEM-HIDE`, `TASK-ITEM-EDGE`, `TASK-ITEM-RESET`, `TASK-TERMINAL-EVIDENCE`, `TASK-DISPOSITION` and `TASK-PARENT-APPROVAL`, one for each profile-validator family, and the approval receipt found. Only then bind the form in the repository registry, in the same commit, and run those cases against the repository registry; they stay in the suite as regression tests.
- Show the header map: a Task whose base holds the old evidence header and whose proposed text holds the mapped header with identical rows passes; the same pair with one changed cell in each of `Consumer`, `Work Unit`, `Command`, `Input`, `Result`, `Location`, `Required` and `Resolves` fails `TASK-EVIDENCE-RETENTION` once for each; a table that keeps the old header under the new registry fails; the approval receipt is found by its `Command` cell; and the registry refuses a `Results` column that is neither common nor in the extension.
- Show the header map on history: a replay test whose earlier commit holds a registry of an earlier MAJOR that binds the old column names and a Task with the old header, and whose later commit holds the new registry and the moved Task. `registry_at` reads the earlier registry with its own typed reading; identical rows pass and one edited cell fails `TASK-EVIDENCE-RETENTION`. Record the map's consumer list and its removal condition, the day `READABLE_REGISTRY_MAJORS` holds no MAJOR below the one this package sets.
- Show the ledger validator first on a moved Task with its reader unchanged: it finds no evidence row and reports nothing. Then pass it the binding, and show it reading the rows of the moved SPEC-0161 Task by `Evidence ID` and `Result` and failing a Task whose evidence table or either column is missing.
- Show the form-only route of W03-D01 as a pair of cases: an old-form base with a form proposed text and identical rows passes, and the same pair with one changed, removed or reordered evidence cell fails.
- Show each reader on a form registry, an old-list registry and a registry without the evidence binding, and the cumulative-history suite unchanged.
- Add the staged-mode test of the two-registry read: a temporary repository whose base commit holds the old registry and an old-form Task and whose index holds the bound form and the moved Task, with the base registry read from the base commit and not from the working tree. Identical rows pass; an edited recorded evidence cell fails `TASK-EVIDENCE-RETENTION`; a removed work row fails `TASK-ITEM-DELETE`.
- Move the Tasks smallest first and the SPEC-0161 Task last, and run the profile validator after each. After each move compare the row hashes of every table and the sorted non-heading, non-blank lines, and record every added line in that Task. In each Task place the pointer H3 Resolution Links before `Residue Handoff`, so the section reads Results, Resolution Links, `Residue Handoff`. Run `python3 scripts/validate-work-residue-ledger.py --root .` before and after the move of the SPEC-0161 Task and record that the five registered historical tables and the live table still resolve.
- Raise the MAJOR in one working-tree step that leaves the write guard usable. The guard judges every structured write against the registry in the tree, so the order is: let the guard accept the earlier and the new MAJOR in the working tree only; set the registry, the schema `const` and `REGISTRY_MAJOR` to the new MAJOR and append it to `READABLE_REGISTRY_MAJORS`; set `DOC_REGISTRY_MAJOR` to the new MAJOR alone; and commit once, in the commit that adds the column extension. Record the three steps, that no commit holds the guard for two, the level MAJOR with its reason under line 878 of the W03 prompt, and the value before and after with MINOR and PATCH at 0. Search for the earlier and the new version value over `docs/99.templates`, `scripts` and `tests` and record that the new MAJOR stands only in the registry, the schema `const` and the three constants. Record the output of `git diff --cached -- scripts/provider_write_guard.py` as proof that the staged guard changes `DOC_REGISTRY_MAJOR` alone and holds one MAJOR, and route a `security-auditor` read of that diff before merge. The derived tests of SPEC-0207 then pass unedited, the guard accepting the new MAJOR, refusing the earlier one and holding a copy equal to `REGISTRY_MAJOR`; a registry of the earlier MAJOR at the current path is refused, and the cumulative-history suite still replays earlier commits with their own registries.
- Record the risk class as `high`, because the MAJOR step changes which registry the write guard, the pre-action hook program, accepts; the rest is the registry, the Task readers of two validators, the Task template check, every Task in the tree and tests. Complete the core-diff checklist: no permission, trigger, hook registration or workflow changes, and the one protected behaviour that changes is the MAJOR the guard accepts.

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. Every `TASK-` rule must be shown active on the final tree, and every recorded row of every moved Task must be shown byte-identical. The write guard must accept the new MAJOR and refuse the earlier one.

### Stage Placement

- Before each commit, run the staged lifecycle check against a temporary copy that holds a Task with one edited recorded evidence row and record that `TASK-EVIDENCE-RETENTION` refuses it, so no commit of this package leaves the rules off.
- Before each commit, rebase on `main`, take the inventory of Tasks again, repeat the move of a Task another package appended to, and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit with the W03-D61 row, which notes that W03-D65 supersedes its first choice; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run `graphify update .` after the code change.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **The Task rules switch off when the form binds.** Without a control this is Likely, Moderate: HIGH, because the evidence reader holds a literal heading, the work-row rules return nothing when they find no base rows, and the retention rule compares a missing column as an empty cell, so a column read by its old name would compare equal, and it would block the implementation commit. This Plan closes it: the first Global Constraint keeps every `TASK-` rule active in every commit; each side of a comparison is read with its own registry before the form binds; a Task that had rows and shows none fails instead of passing; rows are read through the header map and a row that lacks a column a rule reads is an error; the registry refuses a binding that names no form section; one regression test for each rule stays in the suite; the staged check must refuse an edited evidence row before each commit; and Completion requires the rules shown active on the final tree. With those controls the residual is Unlikely, Moderate: LOW, monitor. Owner: W05 code. Review cue: the regression tests and the per-commit refusal record. Signal that raises it: an edited recorded row that passes, or one of the regression tests removed. Rollback: revert the implementation commit, which also unbinds the form.
- **The write guard and the registry disagree on the MAJOR.** Without a control this is Likely, Moderate: HIGH, because the guard fails closed for a MAJOR it does not implement, so a registry at the new MAJOR with the old guard, or the reverse, refuses every structured write in that tree, and it would block the implementation commit. This Plan closes it: the fourth Global Constraint moves the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and `DOC_REGISTRY_MAJOR` in one commit; the working-tree order keeps the guard usable while the registry changes; the committed guard accepts the new MAJOR only; the derived tests of SPEC-0207, unedited, show the guard accepting it and refusing the earlier one and `DOC_REGISTRY_MAJOR` equal to `REGISTRY_MAJOR`; and the change is reviewed as risk class `high`. With those controls the residual is Unlikely, Moderate: LOW, monitor. Owner: W05 code. Review cue: the recorded three steps and the derived tests. Signal that raises it: a `HOOK-DOC-REGISTRY` refusal on a tree whose registry and guard are both committed. Rollback: revert the implementation commit, which restores both.
- **The work residue ledger validator reads no evidence rows.** Without a control this is Likely, Moderate: HIGH, because `_task_doc` calls the evidence reader without a registry and turns a missing table into an empty mapping, so after the move it would check every residue entry against no evidence and say nothing, and it would block the implementation commit. This Plan closes it: the validator takes the binding from the registry it already loads; a missing evidence table or column is an error; a first test shows the silent result and then the failure; and `python3 scripts/validate-work-residue-ledger.py --root .` runs before and after the move of the SPEC-0161 Task. With those controls the residual is Unlikely, Moderate: LOW, monitor. Owner: W05 code. Review cue: the ledger test and the two validator runs. Signal that raises it: a ledger run that reports no evidence for a Task that has rows. Rollback: revert the implementation commit.
- **A recorded row changes during the move.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. Only heading lines move, pointer lines are added and the header line of the evidence table is mapped; the rows of every table are hashed before and after for each Task, and the retention rule compares them as well. Review cue: the hash pairs in each Task. Signal that raises it: a differing hash. Rollback: restore the Task from the base commit and repeat.
- **A history replay reads an old Task with the new shape.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. Each side takes its section from the registry of its own commit, and a registry without the binding keeps the old literal; the cumulative-history suite runs unchanged. Review cue: that suite. Signal that raises it: a diagnostic on a past commit. Rollback: revert the implementation commit.
- **A new package cannot record its approval.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. The first-record approval reads the same evidence rows; a test shows it found in the form and refused without its receipt. Review cue: that test. Signal that raises it: a package commit refused for a receipt that is present. Rollback: revert the implementation commit.
- **The work residue ledger loses its host.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. SPEC-0191 planned a registry edit for this move, and the ledger tests run in the same commit. Review cue: the ledger suite. Signal that raises it: a residue row the ledger no longer finds. Rollback: restore the host entry.
- **Another package appends to the SPEC-0161 Task during the work.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Every package commit and exit appends rows there; this package merges after SPEC-0200 and repeats the move on the rebased file. Review cue: the base commit recorded in the Task. Signal that raises it: a merge conflict in that Task. Rollback: rebase and repeat the move.
- **Approved bytes of open packages change.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Each open Task records its before and after hashes and the reason. Review cue: the inventory. Signal that raises it: an open Task without that row. Rollback: none needed.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| The Task form, its local H3 extensions, its body contract and evidence binding | [Document authoring policy](../../../.agents/governance/document-authoring.md) | The Document authoring policy names the Task form and the registry holds the form, its local H3 extensions, the `sdlc/task` binding and the Task TemplateDefinition. | Forms sentence; `common_forms`, the `sdlc/task` binding and the Task TemplateDefinition in `docs/99.templates/registry.json` |
| Where a Task records its inputs, authority, evidence, decisions and handoff | [Work lifecycle](../../../.agents/workflows/work-lifecycle.md) | The work lifecycle names the form sections where Intake step 4 and Resume now name the old Task sections. | Intake step 4 and Resume, which now name the old Task sections |
