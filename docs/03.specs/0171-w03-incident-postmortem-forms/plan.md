---
title: "W03 Incident and Postmortem Forms Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0171-PLAN-0001"
parent_ids: ["SPEC-0171"]
---

# W03 Incident and Postmortem Forms Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes outside the two templates, and the output of the four strict document validators over the tree is equal before and after.

## Overview

Add the Incident and Postmortem forms, extensions, TemplateDefinitions and tables to the registry; move the two templates; move the incident resolution-evidence lookup to Recovery Verification; update the consumer texts and tests. [Task 0001](tasks/tsk-0001-w03-incident-postmortem-forms.md) owns execution and evidence.

## Context

SPEC-0169 and SPEC-0170 gave Guide and Runbook their forms (PR #234 merged; PR #235 open). This branch `claude/w03-incident-forms` starts from `7cf95a2f`, the SPEC-0170 closure, and is stacked on PR #235; before delivery it is checked against the current `main`. A read at `7cf95a2f` found:

- no incident or postmortem document, only `docs/05.operations/incidents/README.md`;
- the two templates with ten and twelve H2 sections and their Lifecycle Traceability tables;
- `scripts/validate-markdown-profiles.py` reading `## Closure` for `INCIDENT-RESOLUTION-EVIDENCE`, tested in `tests/test_native_skill_envelope.py` from the incident template;
- `tests/test_document_terminal_contract.py` pinning incident and postmortem H2 names in the raw lists;
- section names in the incidents README Expected Record Shape and in the `incident-postmortem` skill (Phase 5).

## Goals & In-Scope

- Registry: two forms, three extensions (two Lifecycle Traceability, one What Went Well), two TemplateDefinitions with tables, four profiles' lists and body-contract sections.
- Templates moved per the Spec's maps.
- Validator rule lookup and its test; the terminal-contract and repository-registry tests.
- Policy, Stage 99 README, incidents README and skill text.

## Non-Goals & Out-of-Scope

- Other roles, README rule IDs and phase 3.
- Status domains, frontmatter keys and lifecycle rules of incidents and postmortems.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-INCIDENTFORM-001](spec.md#success-criteria--verification-plan) | Registry forms, extensions, TemplateDefinitions and tables; repository-registry and terminal-contract tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-incident-postmortem-forms.md) | Failing tests first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-INCIDENTFORM-002](spec.md#success-criteria--verification-plan) | Resolution-evidence lookup and its test; templates moved with the maps; consumer texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-incident-postmortem-forms.md) | Failing rule test first, then passing; strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators over the whole tree before any change.
- Show each changed test failing before its change, then passing.
- Record the template maps in the Task: every old H2 and its author instruction with its new H3.
- The W03-D14 and W03-D15 rows and an evidence row land in the SPEC-0161 Task with this package's first commit.
- Commit order: (1) the `.secrets.baseline` line move for the shifted `registry.json` line, alone; (2) the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit, and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, one validator rule, tests and templates; no permission, trigger, hook, workflow or protected action) and the core-diff checklist.

## Risks & Mitigations

Risks are scored by judgement, not measurement.

- **Resolution rule loses its evidence check.** Likelihood low, impact high, level medium; disposition mitigate. Owner: W03 author. Mitigation: the test shows the rule failing without Recovery Verification evidence and passing with it. Rollback: revert the implementation commit.
- **A template instruction is lost.** Likelihood medium, impact medium, level medium; disposition mitigate. Owner: W03 author. Mitigation: the Task map lists every old instruction with its new place; What Went Well keeps a registered H3 and What Went Wrong an H4 under Contributing Factors, each with its prompt. Rollback: revert the implementation commit.
- **Two roles in one change hides a defect.** Likelihood low, impact low, level low; disposition accept. Owner: W03 author. Mitigation: separate tests per role; no document exists for either. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Incident and Postmortem forms and Lifecycle Traceability placement | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms paragraph; machine form in `docs/99.templates/registry.json` |
