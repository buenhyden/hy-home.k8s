---
title: "W03 Common Form Model Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0168-PLAN-0001"
parent_ids: ["SPEC-0168"]
---

# W03 Common Form Model Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no current document or template heading changes, and the diagnostic counts of the four strict document validators over the current tree are equal before and after.

## Overview

Add the section-tree model, role binding, TemplateDefinition and shared-contract fields to the registry, schema and parser; add the heading-tree checks to the Markdown profile validator; prove both with isolated tests. [Task 0001](tasks/tsk-0001-w03-common-form-model.md) owns execution and evidence.

## Context

SPEC-0161 recorded the W03 gaps (Document Form Handoff) and the user's decisions W03-D01 to W03-D05. A read-only inventory at `0281409b` found 84 profiles, a registry that models H2 lists only, a frontmatter parser that already rejects duplicate keys, invalid dates and unregistered keys, a heading scanner that already skips fences and HTML comments, and no Release role. This branch starts from `main` at `0281409b`. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) are unchanged.

## Goals & In-Scope

- ADR-0059 (proposed in the package commit; accepted by the operator before the implementation commit).
- Authority guard: optional profile keys `document_role` and `template_definition`; optional top-level `common_forms`.
- Schema: `section` (with local `link_only`), `form_extension`, `common_forms` with a `forms` list, profile `document_role` and `template_definition`, shared-contract stage and fields.
- Registry: `schema_version` unchanged at 10; `document_role` on profiles with a clear common role and their template twins (`policy` on `governance/rule` and `operation/policy`); shared-contract fields and extension objects per W03-D05; `common_forms` with no forms.
- Parser and validators: form classes and registry checks; one extension-name accessor used by every consumer; heading-tree diagnostics; template parity for role and form.
- Policy: the shared-contract sentence in `document-authoring.md`.
- Tests: `tests/test_common_form_tree.py` (new), and updates to `test_shared_contract_binding.py`, `test_task_acceptance_contract.py`, `test_document_terminal_contract.py` and any test pinning generation 10, registered in the `document` suite and the validation registry.

## Non-Goals & Out-of-Scope

- Any role form in the repository registry, table column contracts, and any document or template heading change (phases 2 and 3).
- A generator; the retired-identity check; the ADR `rejected` state; editing ADR-0033's body.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORMMODEL-001](spec.md#success-criteria--verification-plan) | Schema, registry and parser model with registry negative tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-common-form-model.md) | Failing tests first, then passing; strict registry check. |
| WORK-002 | [VAL-FORMMODEL-002](spec.md#success-criteria--verification-plan) | Heading-tree diagnostics with positive and negative tests. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-common-form-model.md) | Failing tests first, then passing. |
| WORK-003 | [VAL-FORMMODEL-003](spec.md#success-criteria--verification-plan) | Regression over the current tree, handoffs and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-common-form-model.md) | Strict validators, suites, ruff, staged QA and hooks. |

## Verification Plan

- Record the diagnostic counts of the four strict document validators over the whole tree before any change.
- Show each new test failing before its code, then passing.
- Run the commands in the Spec's Verification Commands, including the staged lifecycle check before each commit; the after counts equal the before counts.
- Architecture compliance: AD-0006 and ADR-0033 unchanged; the registry stays the single form owner.
- Record the risk class (`medium`: registry, validator and test change; no permission, trigger, hook, workflow or protected action) and the core-diff checklist.

## Risks & Mitigations

- **Two heading models at once.** Owner: W03 author. Mitigation: bounded by the phase-3 exit written in the Spec; no current profile uses the tree. Rollback: revert the implementation commit.
- **Shared-contract extension shape change breaks a consumer.** Owner: W03 author. Mitigation: one name accessor used at every consumer (`document_contracts.py` lifecycle-domain checks and record parsing, `document_lifecycle.py` first-record approval, `test_task_acceptance_contract.py`); a regression shows the local extensions still enabled. Rollback: revert the implementation commit.
- **Authority guard widened.** Owner: W03 author. Mitigation: only three named optional keys; the agent-field ban and exact required key set stay; a negative test keeps rejecting `role`. Rollback: revert the implementation commit.
- **ADR-0059 not accepted.** Owner: operator. Mitigation: the implementation commit waits for acceptance. Rollback: none needed.
- **Empty-section rule rejects link-only sections in later phases.** Owner: W03 author. Mitigation: link-only treatment for Traceability and References in the model now. Rollback: revert the implementation commit.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Section tree, form extensions, role binding, TemplateDefinition and shared-contract fields | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Shared-contract paragraph; machine form in `docs/99.templates/registry.json` and its schema, decided by ADR-0059 |
| Heading-tree checks | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Validated by `scripts/validate-markdown-profiles.py` |
