---
title: "W03 Service README Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0174-PLAN-0001"
parent_ids: ["SPEC-0174"]
---

# W03 Service README Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes outside the 21 Service README documents and two templates, and the output of the four strict document validators over the tree is equal before and after.

## Overview

Add the Service README form, TemplateDefinitions and tables; bind the four profiles; read navigation from `Service Role`; move the 21 documents and two templates form-only; record W03-D17; update the policy texts. [Task 0001](tasks/tsk-0001-w03-service-readme-form.md) owns execution and evidence.

## Context

SPEC-0173 gave the Stage and collection READMEs their form and made the document-content reader accept H4; its PR #238 is merged into `main` (`bfbb1bdf`). This branch `claude/w03-service-readme-form` starts from `0f60ce3b`, the SPEC-0173 closure, which `main` contains; before delivery it is checked against the current `main`. A read at `0f60ce3b` found:

- 20 READMEs on `common/readme-implementation` (56 to 260 lines; the shared Overview, Scope, Structure, Usage, Verification and Related Documents core) and `.github/repository-surface.md` on `common/readme-runtime-governance` (123 lines);
- several READMEs with an `Audience` and a `Scope` H3 under Overview besides the Scope H2, and In Scope and Out of Scope already at H4, which move one level down;
- `scripts/validation/document_content.py` reading fourteen matrices in `gitops/` (six), `gitops/platform/`, `gitops/workloads/`, `infrastructure/` (three), `infrastructure/verify/`, `examples/` and `.github/repository-surface.md` by title, all at H3 today;
- `tests/test_repository_quality_rules.py` mutating the `Example Role Matrix` heading of `examples/README.md` by a pattern that matches only H2 and H3;
- the owner-reference check of `.github/repository-surface.md` reading the whole text;
- no table in the 21 documents whose first header is `Command`;
- COMMON-ROLE-FORMS naming the Service README conditional content as troubleshooting and a command/output table.

## Goals & In-Scope

- Registry: form, TemplateDefinitions and tables, role bindings, navigation section, empty lists.
- 21 documents and two templates moved per the Spec's map; policy texts; the W03-D17 row and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: registry, navigation and the document-content mutation cases.

## Non-Goals & Out-of-Scope

- The Workspace and Reference Pack README roles; `AGENTS.md`, `SKILL.md` and Policy; the retirement of the `README_H2_*` list rules; phase 3.
- New README content, links or child listings.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SERVICEREADME-001](spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinitions, tables, bindings and navigation; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-service-readme-form.md) | Failing tests first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-SERVICEREADME-002](spec.md#success-criteria--verification-plan) | 21 documents and two templates moved with the map; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-service-readme-form.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators over the whole tree before any change.
- Show each changed test failing before its change, then passing.
- Record per document in the Task: where each H2 and H3 went and every added line; run a word comparison per document.
- Commit order: the package commit, which adds this package's entry to `docs/03.specs/README.md` and the W03-D17 rows; then the `.secrets.baseline` line move alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after a code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, tests and 21 router documents including `.github/repository-surface.md`; no permission, trigger, hook, workflow file or protected action) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **Meaning drift across 21 documents.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Word comparison per document and the map in the Task. Review cue: a removed word other than a heading. Signal that raises it: a changed sentence in the comparison. Rollback: revert the implementation commit.
- **Content or navigation checks stop reading a moved matrix or child link.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The reader accepts H4, navigation reads `Service Role`, and validator output must equal the before run. Review cue: a matrix rule that no longer reports on a seeded defect in tests. Signal that raises it: any change in validator output. Rollback: revert the implementation commit.
- **A placement reads as a new claim.** Possible, Minor: LOW, accept with review. Owner: W03 author. A matrix under Interfaces or a link under Inputs and Outputs keeps its own text; the Task lists judgement placements for the user. Review cue: the user's acceptance question. Signal that raises it: the user asks to move a placement. Rollback: move the heading back in a follow-up edit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Service README form and its navigation section | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; machine form in `docs/99.templates/registry.json` |
