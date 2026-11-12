---
title: "W03 Root README Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0172-PLAN-0001"
parent_ids: ["SPEC-0172"]
---

# W03 Root README Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes outside `README.md` and the root README template, and the output of the four strict document validators over the tree is equal before and after.

## Overview

Add the Root README form, TemplateDefinition and table; let README navigation name an H3 section of a form; allow omitted trailing optional table columns; move `README.md` and its template form-only; update the policy texts. [Task 0001](tasks/tsk-0001-w03-root-readme-form.md) owns execution and evidence.

## Context

SPEC-0169 to SPEC-0171 gave Guide, Runbook, Incident and Postmortem their forms (PR #234 and #235 merged; PR #236 open). This branch `claude/w03-readme-forms` starts from `40b44bd4`, the SPEC-0171 closure, and is stacked on PR #236; before delivery it is checked against the current `main`. A read at `40b44bd4` found:

- 44 README-kind documents in scope of the three README packages: the root README, 26 Stage README kind (seven stage, fifteen collection and four agent or provider READMEs, by W03-D10) and 17 Service README kind (sixteen implementation READMEs and `.github/repository-surface.md`);
- `readme_navigation` naming the H2 `Structure` for the root profile, read only by `_readme_section` in `scripts/validate-links-and-owners.py`, which matches H2 headings, and checked by `REGISTRY_README_NAVIGATION`, which requires a required H2 of the profile lists;
- `scripts/validation/document_content.py` reading only the root README's link to the Stage 99 guide;
- a root README of 262 lines with eight H2 and seventeen H3 sections and no Path and Purpose table.

## Goals & In-Scope

- Registry: the Root README form, TemplateDefinition and table; the root profiles' lists; the navigation section.
- Code: the navigation registry rule and section reader; optional trailing table columns.
- `README.md` and template moved per the Spec's map; policy texts.
- Tests: navigation, table and repository-registry cases.

## Non-Goals & Out-of-Scope

- The Stage, Service, Workspace and Reference Pack README roles; the retirement of the `README_H2_*` list rules; phase 3.
- New README content or links.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ROOTREADME-001](spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinition, table and navigation section; navigation rule and reader; optional trailing columns; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-root-readme-form.md) | Failing tests first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-ROOTREADME-002](spec.md#success-criteria--verification-plan) | `README.md` and template moved with the map; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-root-readme-form.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators over the whole tree before any change.
- Show each changed test failing before its change, then passing.
- Record the `README.md` meaning map and a word comparison in the Task.
- Commit order: the package commit; then the `.secrets.baseline` line move alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, validator code, tests and the repository entry document; no permission, trigger, hook, workflow or protected action) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **The root navigation section reads fewer links.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. The Canonical Owners links leave `Directories` by design, so the section's link targets go from four to one (`./examples/`, from the moved cloud-example paragraph); none is a deep path today. Review cue: a link added under Canonical Entry Points or References is checked only by `README-NAV-ENUMERATION`, not `README-NAV-DEPTH`. Signal that raises it: a deep link appears outside the Directories section. Rollback: revert the implementation commit.
- **Optional columns weaken the table check.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. Only trailing columns marked not required may be omitted, and the registry refuses a required column after an optional one. Review cue: a README package that adds an optional column. Rollback: revert the implementation commit.
- **Meaning drift in the repository entry document.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Word comparison and the map in the Task. Review cue: any word removed other than a heading. Signal that raises it: a removed or changed sentence in the word comparison. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Root README form and README navigation in a form section | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms paragraph; machine form in `docs/99.templates/registry.json` |
