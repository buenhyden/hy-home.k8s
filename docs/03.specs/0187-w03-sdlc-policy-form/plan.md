---
title: "W03 SDLC Policy Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0187-PLAN-0001"
parent_ids: ["SPEC-0187"]
---

# W03 SDLC Policy Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: `sdlc.md` changes in form and in the one sentence the Spec names, and in nothing else; no rule ID, Rules table, Level or Status column is added (W03-D42 to W03-D44 are recorded only); and the diagnostics of the four strict document validators over the tree are equal before and after. SPEC-0182 must be present in the base (`534ddae7` or later), which it is at `a8da75e5`; its frozen source is `574e8e601a6757efdaf258d9d7be424e0fd928e4:docs/03.specs/0182-w03-explained-empty-sections/spec.md`. This package's own three files fall under the open-package layer rule of SPEC-0184.

## Overview

Move `.agents/governance/sdlc.md` to the Policy form; fold it into `governance/rule`; remove `governance/contract`, its template twin and template; retarget the 21 test lines and one comment; drop `contract` from the templates README; record W03-D41 to W03-D44. [Task 0001](tasks/tsk-0001-w03-sdlc-policy-form.md) owns execution and evidence.

## Context

A read of the tree at `a8da75e5` and a scratch trial of the whole change (a `git archive` copy of that HEAD with the change applied) found:

- `sdlc.md` is the only document of `governance/contract` (registry profile index 14, `path_pattern` `^\.agents/governance/sdlc\.md$`); its twin is `common/template-governance-contract` (index 70) with the template `contract.template.md`; `lifecycle_domains` names the profile once; `governance/rule` (index 20) matches nine policies;
- 21 test lines name the profile or twin: 17 in `tests/test_document_lifecycle_cumulative_history.py` (the seed selection, a `path_pattern` override, a frontmatter fixture and the profile arguments), 3 in `tests/test_common_form_tree.py` (lines 100, 130 and 160) and 1 in `tests/test_task_execution_contract.py` (line 1044);
- `docs/99.templates/templates/README.md` line 46 lists `contract` under `governance/`, and the comment at `tests/test_common_form_tree.py` line 113 counts "fourteen templates" of the local roles, which becomes thirteen;
- one anchor consumer, `.agents/governance/document-authoring.md` line 275 (`sdlc.md#ownership-and-placement`), and no other anchor link into `sdlc.md`;
- `sdlc.md` has no empty required section after the mapping except three with no source text, and two that point to existing content;
- in the scratch trial, after the change and the retargeting the three strict document validators and the registry check pass, `tests.test_common_form_tree` (253 tests), `tests.test_document_lifecycle_cumulative_history` (42) and `tests.test_task_execution_contract` (32) pass and the `document` suite passes; run against the registry change before the retargeting, the first two modules fail. The `.secrets.baseline` registry entry at `docs/99.templates/registry.json` line 8809 moves to line 8631 with the removal.

## Goals & In-Scope

- `sdlc.md` in the Policy form with explained-none texts and the one edit; registry consolidation; the removed template; the test retargeting.
- Tracking: in the SPEC-0161 Task, with the package commit, the rows W03-D41 to W03-D44 (D41 supersedes the D20 and D06 members and counts; no D06 or D20 row is edited), the refreshed state cell of W03-H29 and an evidence row; row numbers are re-read at commit time (D32 from SPEC-0184, D33 to D36 from SPEC-0186, D37 to D40 from SPEC-0185).

## Non-Goals & Out-of-Scope

- Rule IDs, the Rules table, the Level and Status columns and their check (packages 2 to 5); the Policy form and its template; the explained-empty-sections rule; the local forms; renumbering (W03-D30); history documents that name the removed profile.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SDLCPOL-001](spec.md#success-criteria--verification-plan) | Move `sdlc.md` to the Policy form; write the explained-none texts; make the one edit; check the anchor. | Approved Spec and Plan; SPEC-0182 present in the base. | [Task 0001](tasks/tsk-0001-w03-sdlc-policy-form.md) | Strict Markdown profile and link checks over the form; the before and after sentence comparison; the anchor resolves. |
| WORK-002 | [VAL-SDLCPOL-002](spec.md#success-criteria--verification-plan) | Registry consolidation; remove the template; retarget the tests; record W03-D41 to W03-D44. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-sdlc-policy-form.md) | Failing tests first, then passing; registry check; suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators before any change.
- Show the existing tests of the three modules failing after the registry change and before the retargeting, then passing.
- Record in the Task the sentence-by-section comparison of `sdlc.md` before and after, the final explained-none texts for review and the anchor check of `document-authoring.md` line 275.
- Commit order, four steps: (1) the `.secrets.baseline` digests for this package's Task alone; (2) the package commit with the Spec, Plan and Task, this package's entry in `docs/03.specs/README.md` and the SPEC-0161 rows; (3) the shifted-line move alone, the `.secrets.baseline` registry entry from 8809 to 8631 (confirm the number on the final bytes); (4) the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the test change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 bodies unchanged.
- Record the risk class (`medium`: registry, a governance document and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the scratch trial and the tree read.

- **Tests and maps name the removed profile.** Likely, Minor: MEDIUM, monitor. Owner: W05 tests. The trial reproduced failures in `tests/test_document_lifecycle_cumulative_history.py` (the seed selection, override and fixtures) and two in `tests/test_common_form_tree.py` (role, table and source maps), cleared by retargeting and dropping the three entries; both fail only after the registry change and before the retargeting. Review cue: those modules. Signal that raises it: an error naming a missing profile. Rollback: revert the implementation commit.
- **A consumer of the removed profile is missed.** Possible, Minor: LOW, monitor. Owner: W03 author. The read found `governance/contract` in the registry, three test modules, the templates README, `sdlc.md` and history documents only; a suite not run in the trial could name it. Review cue: a grep of the final tree and the four suites. Signal that raises it: a diagnostic naming the profile or template. Rollback: revert the implementation commit.
- **The move changes the meaning of a rule that every owner consumes.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Only two phrases change and the rest moves unchanged; the Task compares each sentence by section and the user accepts the before and after. Review cue: the comparison. Signal that raises it: a changed sentence outside the named edit. Rollback: revert the implementation commit.
- **An explained-none text is untrue for `sdlc.md`.** Possible, Minor: LOW, monitor. Owner: W03 author. `BODY-SECTION-BARE` is already in the base and refuses a bare statement, but cannot judge sufficiency; the three reason-table sentences are true because the policy states no exception or adoption step of its own, and the two pointers target existing text. Review cue: the Task list of final texts. Signal that raises it: a reviewer disputing a sentence. Rollback: correct the text.
- **The anchor in `document-authoring.md` stops resolving.** Unlikely, Minor: LOW, monitor. Owner: W03 author. The heading text is unchanged and the trial's strict link validator passed. Review cue: the link validator. Signal that raises it: a `LINK` diagnostic on line 275. Rollback: restore the heading text.
- **Overlap with SPEC-0186 on `tests/test_common_form_tree.py` and the governance-document twin.** Possible, Minor: LOW, monitor. Owner: W03 author. Both packages edit that module and the `governance-document` role's maps; the second to land rebases and re-runs the module. Review cue: the merge order. Signal that raises it: a conflict in that file or a count mismatch. Rollback: revert the implementation commit.
- **Concurrent packages append to the SPEC-0161 Task and edit the same test file.** Possible, Minor: LOW, monitor. Owner: W03 author. Row numbers are re-read at commit time and appended rows keep the others' order; the registry and test edits are re-read before dependent writes. Review cue: the Task diff at commit. Signal that raises it: a duplicate row number. Rollback: renumber before commit.
- **The base moves before this package lands.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. HEAD moved from `b1e8cea7` to `a8da75e5` while this was drafted and the registry line of the baseline entry depends on it. Review cue: the base at commit. Signal that raises it: a changed line number or test count. Rollback: re-run the trial on the new base and correct the numbers.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The SDLC flow as a Policy on `governance/rule` | [SDLC flow](../../../.agents/governance/sdlc.md) | Frontmatter type and section form; machine data in `docs/99.templates/registry.json` |
