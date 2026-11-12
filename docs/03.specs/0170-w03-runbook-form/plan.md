---
title: "W03 Runbook Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0170-PLAN-0001"
parent_ids: ["SPEC-0170"]
---

# W03 Runbook Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: outside the ten runbooks and the runbook template no document or template heading changes, and the output of the four strict document validators over the rest of the tree is equal before and after.

## Overview

Add the Runbook form, its two extensions, TemplateDefinition and tables to the registry; move the runbook template and the ten runbooks form-only; update the policy, Stage 99 README and ops-runbook skill texts. [Task 0001](tasks/tsk-0001-w03-runbook-form.md) owns execution and evidence.

## Context

SPEC-0169 gave Guide its form and added the derived heading lists, the TemplateDefinition `tables` contract and the table checks; it closed at `8b9d54a6`, which PR #234 merged into `main`. This branch `claude/w03-runbook-form` starts from `8b9d54a6`; before delivery it is checked against the current `main` and opened as a pull request to `main`. A read at `8b9d54a6` found:

- ten runbooks (about 2,200 lines) with the H2s Purpose, Trigger and Preconditions, Procedure, Verification, Recovery and Escalation, Related Documents, and H3 subsections but no H4;
- no link from another file to an anchor inside a runbook, one intra-document anchor in 0010 (`#recovery-and-escalation`), two textual pointers to a Procedure step (0002, 0007), and no Requirement or Spec link in any runbook;
- recovery procedures as H3 under Recovery and Escalation in five runbooks (0001, 0002, 0003, 0004, 0010), which the user placed in a registered `Recovery Procedures` local H3 (W03-D13);
- `Related Documents` lists of architecture, ADR, index, control-surface and tooling links;
- four prose consumers of the runbook headings: `.agents/governance/document-authoring.md`, `docs/99.templates/README.md`, `.agents/skills/ops-runbook/SKILL.md` and `docs/05.operations/runbooks/README.md` (whose Usage Instructions already name nonexistent headings);
- a four-column step table in the template and in runbook 0012 that differs from the W03-D08 table.

## Goals & In-Scope

- Registry: the Runbook form, the `runbook-recovery-procedures` and `runbook-lifecycle-traceability` extensions, the runbook TemplateDefinition with the Triggers and Lifecycle Traceability tables; empty H2 lists and `body_contract.section` `Validation` on both runbook profiles.
- Template and ten runbooks: form-only move per the Spec's meaning map.
- Policy, Stage 99 README, runbooks README and skill text.
- Tests: the repository-registry assertions in `tests/test_common_form_tree.py` name exactly the Guide and Runbook forms.

## Non-Goals & Out-of-Scope

- Every other role's form, the `SKILL.md` form, README rule IDs and phase 3.
- New runbook content, commands or approvals; any live check.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RUNBOOKFORM-001](spec.md#success-criteria--verification-plan) | Registry form, extensions, TemplateDefinition and tables; repository-registry tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-runbook-form.md) | Failing test first, then passing; strict registry check; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-RUNBOOKFORM-002](spec.md#success-criteria--verification-plan) | Template and ten runbooks moved form-only with the meaning map; policy, README and skill text; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-runbook-form.md) | Strict validators, suites, quality gate, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators over the whole tree before any change.
- Show the changed repository-registry test failing before the registry change, then passing.
- Record the meaning map per runbook in the Task: where each source H2's content went, every H3 that became H4 or H5, every moved link, and every added none-with-reason line listed separately for the user.
- The W03-D13 row and an evidence row land in the SPEC-0161 Task with this package's first commit.
- Commit order: (1) the `.secrets.baseline` line move for the shifted `registry.json` line, alone; (2) the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit, and `graphify update .` if code changes.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, test and governed document change across ten operating documents; no permission, trigger, hook, workflow or protected action) and the core-diff checklist.

## Risks & Mitigations

Risks are scored by judgement, not measurement.

- **Meaning drift across ten runbooks.** Likelihood medium, impact high, level medium; disposition mitigate. Owner: W03 author. Mitigation: per-runbook meaning map reviewed before commit; a word-multiset comparison per runbook shows only headings, list markers and the listed added lines differ. Rollback: revert the implementation commit.
- **A command loses its boundary marker or its order.** Likelihood low, impact high, level medium; disposition mitigate. Owner: W03 author. Mitigation: commands move with their surrounding paragraph; the repository quality gate checks the markers. Rollback: revert the implementation commit.
- **Stop or evidence sections filled with invented content.** Likelihood medium, impact medium, level medium; disposition mitigate. Owner: W03 author. Mitigation: only existing sentences move there; otherwise a none-with-reason line that the user reviews. Rollback: revert the implementation commit.
- **Recovery procedures misfiled as rollback.** Likelihood medium, impact medium, level medium; disposition mitigate. Owner: W03 author. Mitigation: only undo and rollback content goes to Rollback; other recovery goes to the registered Recovery Procedures H3. Rollback: revert the implementation commit.
- **Heading levels skipped or anchors dead.** Likelihood medium, impact medium, level medium; disposition mitigate. Owner: W03 author. Mitigation: markdownlint MD001 over the eleven files; the 0010 anchor and the two textual pointers are updated and listed. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Runbook form and Lifecycle Traceability placement | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Guide, Policy and Runbook paragraph; machine form in `docs/99.templates/registry.json` |
