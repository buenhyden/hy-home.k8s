---
title: "W03 Workspace and Reference Pack README Forms Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0178-PLAN-0001"
parent_ids: ["SPEC-0178"]
---

# W03 Workspace and Reference Pack README Forms Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes other than the decided renames in the three pack READMEs and three pack templates, and the output of the four strict document validators over the tree is equal before and after.

## Overview

Add the two local roles to the role list and schema; add their forms, local H3s and TemplateDefinitions; bind the eight profiles; rename the pack sections; read pack navigation from `Pack Index`; record W03-D19; update the policy texts. [Task 0001](tasks/tsk-0001-w03-workspace-pack-readme-forms.md) owns execution and evidence.

## Context

SPEC-0177 gave the Skill role its form (PR #242 open). This branch `claude/w03-workspace-pack-readme-form` starts from `ed91d165`, the SPEC-0177 closure, and is stacked on PR #242; before delivery it is checked against the current `main`. A read at `ed91d165` found:

- seven Workspace READMEs and their template, all with the same headings: Overview, Scope (Permitted Artifacts, Forbidden Local State), Structure, Usage (Promotion and Cleanup, Tracking Rules), Related Documents;
- one audit pack and two research pack READMEs and three pack templates with the headings Overview, Scope, the kind's Contract, Structure, the kind's Index, Usage, the kind's closure section, Evidence Boundary and Related Documents; research pack 0001 also has the H3s External Finding Vocabulary and Separate Evidence Axes under its Contract; no data pack exists;
- index contents that differ by pack: a list in the audit pack and tables with different headers in the research packs;
- the `DocumentRole` literal in `scripts/document_contracts.py` and the schema enums closed at the sixteen COMMON-DOC-FORM-1 roles, with `ROLE_IDS` in the tests and a parity test between code and schema;
- three sentences that name an old pack heading literally (two in the audit pack README, one in the research collection README);
- a link-only `Related Documents` in research pack 0001, which an authored profile's empty-section check refuses unless the section is `link_only`;
- the form tree check refusing an H3 that the form does not register;
- no link in the tree naming a pack contract or index anchor.

## Goals & In-Scope

- Code and schema: two role identifiers.
- Registry: two forms, two local H3s, four TemplateDefinitions, eight bindings with empty lists, three navigation sections.
- Three pack READMEs and three pack templates renamed, and the three sentences that name an old heading; policy texts; W03-D19 and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: registry, form, navigation and route cases.

## Non-Goals & Out-of-Scope

- Workspace README text; the read-only input folder; Stage 90 reports; H06, H07 and phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LOCALREADME-001](spec.md#success-criteria--verification-plan) | Role list and schema; forms, local H3s, TemplateDefinitions, bindings and navigation; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-workspace-pack-readme-forms.md) | Failing tests first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-LOCALREADME-002](spec.md#success-criteria--verification-plan) | Pack renames; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-workspace-pack-readme-forms.md) | Strict validators, fragment search, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators and the fragment search before any change.
- Show each changed test failing before its change, then passing.
- Record per pack document in the Task the renamed headings and confirm the bodies are unchanged; confirm the seven Workspace READMEs are byte-identical.
- Commit order: the package commit with this package's entry in `docs/03.specs/README.md` and the W03-D19 rows; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, schema, the role list, tests and three reference documents; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **A widened role list admits an unintended role.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. Only the two named identifiers are added, each with a form and bindings that tests pin. Review cue: a role without a form in the registry check. Signal that raises it: a later role added without review. Rollback: revert the implementation commit.
- **Navigation or links stop resolving after the renames.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The fragment search is empty before and after, and navigation reads `Pack Index`. Review cue: a navigation diagnostic. Signal that raises it: any change in validator output. Rollback: revert the implementation commit.
- **A pack loses its kind's required closure section.** Possible, Minor: LOW, accept with review. Owner: W03 author. The three closure sections are conditional in one form, so the tree check enforces none; review and the Task check each pack's own section. Review cue: a pack without its closure section in review. Signal that raises it: a new pack that omits it. Rollback: a follow-up edit or a later conditional check.
- **A local H3 hides a section the common form should own.** Possible, Minor: LOW, accept with review. Owner: W03 author. The two H3s keep research pack 0001's present text and record removal when the form gains a matching section. Review cue: the acceptance question. Signal that raises it: a second pack needing the same H3. Rollback: a follow-up edit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Workspace and Reference Pack README forms and the pack navigation section | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; machine forms in `docs/99.templates/registry.json` |
