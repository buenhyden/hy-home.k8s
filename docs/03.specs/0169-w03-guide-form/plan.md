---
title: "W03 Guide Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0169-PLAN-0001"
parent_ids: ["SPEC-0169"]
---

# W03 Guide Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: outside GDE-0010 and the guide template no document or template heading changes, and the diagnostic counts of the four strict document validators over the rest of the tree are equal before and after.

## Overview

Add the Guide form, its extension, TemplateDefinition and table contract to the registry; add the table checks; move the guide template and GDE-0010 form-only. [Task 0001](tasks/tsk-0001-w03-guide-form.md) owns execution and evidence.

## Context

SPEC-0168 (closed; recovery in REQ-0003 Archived Lineage) added the form model with no role form. The SPEC-0161 Task records W03-D01 to W03-D12 and the phase-2 order, Guide first: one document and one template, no README navigation code, and the first use of W03-D11 link placement. This branch `claude/w03-phase2-forms` starts from `de5c31b0` (the SPEC-0168 closure, PR #233 open) plus the SPEC-0161 decision commits up to `0373439b`; it is stacked on PR #233, so its pull request is opened after #233 merges or against its branch. A read at `0373439b` found no anchor link into GDE-0010 and two prose consumers of the Guide placement rule: `.agents/governance/document-authoring.md` (the Guide, Policy and Runbook paragraph) and `docs/99.templates/README.md` (Operations forms). `tests/test_operations_section_contract.py` and `tests/test_operations_lineage_contract.py` build profiles from the registry's `operation/guide` entry but overwrite its section lists or body-contract section, so they stay valid. Four consumers read profile heading lists (`REGISTRY_BODY_SECTION`, the template author-prompt check, the generic-residue scope and the heading-validity projection); the derived lists keep them working. `.secrets.baseline` records a `registry.json` line that this change shifts.

## Goals & In-Scope

- Schema: `tables` in `template_definition`.
- Registry: the Guide form, the `guide-lifecycle-traceability` extension, the guide TemplateDefinition with the Steps and Lifecycle Traceability tables; empty H2 lists and `body_contract.section` `Verification` on both guide profiles.
- Parser and validators: heading lists derived from the form; table contract parsing, copy onto source profiles and registry checks; the document table check.
- Template and GDE-0010: form-only move per the Spec's meaning map.
- Policy text: the Guide paragraph and one table-contract sentence in `document-authoring.md`, and the Operations forms entry in `docs/99.templates/README.md`, each with its `version` and `updated`.
- Tests: registry and table negatives in `tests/test_common_form_tree.py`, whose three no-form assertions are rewritten to assert the Guide form exactly; the two operations tests re-run unchanged.

## Non-Goals & Out-of-Scope

- Every other role's form, README rule IDs, and the phase-3 removal of the H2-list model.
- New guide content, a generator, and any live check.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GUIDEFORM-001](spec.md#success-criteria--verification-plan) | Schema, registry form, extension, TemplateDefinition, derived heading lists and table registry checks. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-guide-form.md) | Failing tests first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-GUIDEFORM-002](spec.md#success-criteria--verification-plan) | Document table check. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-guide-form.md) | Failing tests first, then passing. |
| WORK-003 | [VAL-GUIDEFORM-003](spec.md#success-criteria--verification-plan) | Template and GDE-0010 moved form-only with the meaning map; policy text; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-guide-form.md) | Strict validators, suites, ruff, staged QA and hooks. |

## Verification Plan

- Record the diagnostic counts of the four strict document validators over the whole tree before any change.
- Show each new test failing before its code, then passing.
- Record the GDE-0010 meaning map in the Task: each source sentence or list item with its new section; additions limited to none-with-reason statements, each listed.
- Commit order: (1) the `.secrets.baseline` line move for the shifted `registry.json` line, alone, because the non-style gate scans against the HEAD baseline; (2) the implementation (registry, schema, code, tests, template, GDE-0010, policy text) with the Task evidence. Run the commands in the Spec's Verification Commands, including the staged lifecycle check before each commit, and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged; the registry stays the single form owner.
- Record the risk class (`medium`: registry, validator, test and governed document change; no permission, trigger, hook, workflow or protected action) and the core-diff checklist.

## Risks & Mitigations

Risks are scored by judgement, not measurement.

- **Meaning drift in GDE-0010.** Likelihood medium, impact medium, level medium; disposition mitigate. Owner: W03 author. Mitigation: sentence-level meaning map reviewed before commit; none-with-reason statements listed for the user. Rollback: revert the implementation commit.
- **Table check catches an unrelated table.** Likelihood low, impact low, level low; disposition mitigate. Owner: W03 author. Mitigation: only a table whose first header cell equals the contract's first key is checked; a test shows other tables ignored. Rollback: revert the implementation commit.
- **Body-contract finder misses the moved table.** Likelihood low, impact medium, level low; disposition mitigate. Owner: W03 author. Mitigation: the finder already locates the H3 inside the named H2; GDE-0010 passes the body-contract check after the move. Rollback: revert the implementation commit.
- **A heading-list consumer silently loses its check.** Likelihood medium, impact high, level medium; disposition mitigate. Owner: W03 author. Mitigation: the loader derives the lists from the form; a test shows the derived lists and the registry body-section check for the guide profiles; the residue and author-prompt checks are re-run over GDE-0010 and the template. Rollback: revert the implementation commit.
- **Phase-1 model did not cover a form profile with a body contract.** Likelihood certain without the fix, impact high, level high; disposition mitigate. Owner: W03 author. Mitigation: `REGISTRY_BODY_SECTION` reads the derived required list; a negative test names a section outside the form. Rollback: revert the implementation commit.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Guide form and Lifecycle Traceability placement | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Guide, Policy and Runbook paragraph; machine form in `docs/99.templates/registry.json` |
| Table contract and its checks | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Validated by `scripts/document_contracts.py` and `scripts/validate-markdown-profiles.py` |
