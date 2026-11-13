---
title: "W03 Policy Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0175-PLAN-0001"
parent_ids: ["SPEC-0175"]
---

# W03 Policy Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes outside the 14 Policy documents and two templates, with anchor-only link edits in three named files, and the output of the four strict document validators over the tree is equal before and after.

## Overview

Add the Policy form with its local extension, TemplateDefinitions and tables; empty the four profiles' lists; move the body contract; add the template-twin table rule; move the 14 documents and two templates form-only; repoint the removed H2 anchors; update the policy texts. [Task 0001](tasks/tsk-0001-w03-policy-form.md) owns execution and evidence.

## Context

SPEC-0174 gave the Service README its form (PR #239 open). This branch `claude/w03-policy-form` starts from `3d9428b9`, the SPEC-0174 closure, and is stacked on PR #239; before delivery it is checked against the current `main`. A read at `3d9428b9` found:

- nine `governance/rule` documents (99 to 359 lines; Overview, Authority Boundary, Governance Context, Current Contract, Validation and Refresh, Related Documents; English) and five `operation/policy` documents (118 to 207 lines; Purpose, Scope, Controls, Exceptions and Escalation, Verification and Review, Related Documents; Korean-first);
- a `Lifecycle Traceability` H3 under Related Documents in all five operations policies and the policy template, which the `operation/policy` body contract reads;
- an H3 `Responsibilities` under Controls in POL-0001, POL-0005 and the policy template;
- an HTML anchor `exceptions` in POL-0001;
- nine links to removed H2 anchors: `document-lifecycle.md#current-contract` (in `document-authoring.md` and `sdlc.md`), `document-authoring.md#current-contract` (in `agent-execution.md`), and `0001-k8s-gitops-operations-policy.md#exceptions-and-escalation` (in `docs/05.operations/README.md`, runbook 0004 and POL-0003, POL-0004, POL-0005 and POL-0007); the link validator checks no cross-file fragment, so a whole-tree fragment search stands in;
- no table in the 14 documents whose first header is `Rule`;
- the table inheritance in `scripts/document_contracts.py`, where a later twin naming the same source would replace the earlier one's tables without a diagnostic (W03-H10).

## Goals & In-Scope

- Registry: form and extension, TemplateDefinitions and tables, empty lists, body-contract section.
- Code: `REGISTRY_TABLE_TWIN`.
- 14 documents and two templates moved per the Spec's map; the nine anchor edits with a whole-tree fragment search before and after; policy texts.
- Tests: registry, form, table and extension cases.

## Non-Goals & Out-of-Scope

- `AGENTS.md`, `SKILL.md` and workflows; the Workspace and Reference Pack README roles; phase 3 and the Plan part of W03-H10.
- New rules, exceptions or ownership statements.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-POLICY-001](spec.md#success-criteria--verification-plan) | Registry form, extension, TemplateDefinitions, tables, lists and body contract; `REGISTRY_TABLE_TWIN`; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-policy-form.md) | Failing tests first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-POLICY-002](spec.md#success-criteria--verification-plan) | 14 documents and two templates moved with the map; anchor edits; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-policy-form.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators over the whole tree before any change.
- Show each changed test failing before its change, then passing.
- Record per document in the Task: where each H2 and H3 went and every added line; run a line comparison per document.
- The link validator never fails on a stale cross-file fragment, so equal validator output is no evidence for the nine anchor edits; the before and after fragment search from the Spec's Verification Commands is that evidence.
- Commit order: the package commit with this package's entry in `docs/03.specs/README.md`; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, one registry rule, tests, nine governance policies that agents load and five operations policies; no permission, trigger, hook, workflow or protected action) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **Meaning drift in governance policies that agents read as rules.** Possible, Moderate: MEDIUM, monitor; the form-only rule, the per-document line comparison and the user's acceptance keep a drift to a reviewable, revertible edit. Owner: W03 author. Line comparison per document, no paragraph split, and the map in the Task; the user accepts the placements. Review cue: a removed or reworded rule sentence. Signal that raises it: any changed sentence in the comparison. Rollback: revert the implementation commit.
- **A link or body-contract check stops reading a moved heading.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Anchor edits named in the Spec, the body contract moved to Ownership, and validator output equal to the before run. Review cue: a link or body-contract diagnostic. Signal that raises it: any change in validator output. Rollback: revert the implementation commit.
- **The template-twin rule refuses an existing registry.** Unlikely, Minor: LOW, accept. Owner: W05 code. Policy has one twin per source; the strict registry check runs before commit. Review cue: a `REGISTRY_TABLE_TWIN` diagnostic on the real registry. Signal that raises it: a later role with two tabled twins. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Policy form, its local extension and the template-twin table rule | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; machine form in `docs/99.templates/registry.json`; rule in `scripts/document_contracts.py` |
