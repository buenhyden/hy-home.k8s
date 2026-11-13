---
title: "W03 Remove the Layer Frontmatter Key Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0184-PLAN-0001"
parent_ids: ["SPEC-0184"]
---

# W03 Remove the Layer Frontmatter Key Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no accepted ADR file and no body text other than the named policy sentences changes; frozen records change only by their `layer` line; and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Add the one-use exemptions to the two freeze gates and `FM-LAYER-ADR`, remove the `layer` line from every document and template that carries it except accepted ADRs, change the profiles and key entry to match, update the tests, fixtures and policy texts, record the open packages' metadata-only edits, and retire both exemptions in the final source commit. [Task 0001](tasks/tsk-0001-w03-remove-layer-key.md) owns execution and evidence.

## Context

A read of the tree at `e6ec3d3f` and the pre-approval review's simulations found `layer` in 113 tracked Markdown files, plus this package's three: the 34 accepted ADRs, `decisions/README.md` (a router), five architecture descriptions, four requirements, the stage READMEs, Stage 05 guides, incidents, policies and runbooks, Stage 90 packs, reports and data (13 published members among them), 17 templates (two with the `{{LAYER}}` placeholder) and the open Stage 03 packages. The registry names `layer` on 114 profile lines (28 required, 32 order, 28 constants, 22 forbidden, 4 optional) plus the `frontmatter_keys` entry SPEC-0181 adds. No script reads its value except the generic constant check and the template parity rule, whose `TEMPLATE_OMITTED_KEYS` must keep `layer` for the ADR template. Two freeze gates refuse the edit on frozen records: package-exit R4 on SPEC-0161's Spec and Plan, and `REFERENCE_PUBLISHED_REWRITE` on the 13 published Stage 90 members. Eleven `layer:` lines in three test modules, two `layer:` insertion anchors in a fourth, `tests/fixtures/completion-package.json` and SPEC-0181's key-contract tests write or test it.

## Goals & In-Scope

- Documents and templates: one frontmatter line in each of 82 files.
- Registry and code: profile lists, the key entry, `FM-LAYER-ADR`, the two one-use exemptions and their retirement, the `TEMPLATE_OMITTED_KEYS` comment.
- Tests, fixtures and policy texts; the W03-D32 row and evidence rows in the SPEC-0161 Task; metadata-only evidence rows in the affected open Tasks.

## Non-Goals & Out-of-Scope

- Accepted ADRs; ADR-0033's stale sentence; other body text; other keys; Q-07; the wider W03-D02 exception.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LAYER-001](spec.md#success-criteria--verification-plan) | Gate exemptions, `FM-LAYER-ADR`, registry, documents, templates, tests and fixtures. | Approved Spec and Plan; SPEC-0181 implemented and merged. | [Task 0001](tasks/tsk-0001-w03-remove-layer-key.md) | Failing tests first, then passing; the `layer` search. |
| WORK-002 | [VAL-LAYER-002](spec.md#success-criteria--verification-plan) | Policy texts; open-package evidence rows; regression and exact-index QA; exemption retirement in the final source commit. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-remove-layer-key.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators and the `layer` search before any change.
- Show the new rule and exemption tests failing first, then passing; show any non-`layer` change to a frozen record still refused.
- Record in the Task the number of files changed by group, the before and after hashes of each frozen record and open Spec and Plan, and confirm that no accepted ADR changed and that `git grep -n '^layer: '` lists only the 34 accepted ADRs.
- In the final source commit, before the Task freezes, remove both exemptions, their tests and their policy sentences, and record in the Task the gates refusing a `layer`-only change again.
- Commit order: the package commit; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Record the risk class (`medium`: 82 files' frontmatter, the registry, the lifecycle and registry freeze gates, one rule and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval review's evidence.

- **An accepted ADR is edited.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The edit selects files by status and the Task confirms none changed. Review cue: the core-diff checklist. Signal that raises it: an ADR path in the diff. Rollback: restore the file.
- **A frontmatter edit breaks a document's other keys.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. Only the one line is removed and the strict validators compare before and after. Review cue: a frontmatter diagnostic. Signal that raises it: any new diagnostic. Rollback: revert the implementation commit.
- **The freeze gates refuse the edit.** Likely, Moderate: HIGH; it blocks the implementation commit. Owner: W05 code. The review reproduced both refusals; the one-use exemptions land with failing-first tests before the documents change. Review cue: the staged lifecycle and registry checks. Signal that raises it: a gate diagnostic on a `layer`-only change. Rollback: revert the implementation commit.
- **The exemptions weaken a freeze gate.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. Only the `layer` line is set aside, tests show any other change still refused, and the final source commit retires both exemptions. Review cue: any non-`layer` byte change to a frozen record still refused. Signal that raises it: an exemption left after closure. Rollback: retire the exemption.
- **Approved bytes of open packages change.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Each affected Task records the before and after hashes and the metadata-only reason. Review cue: the acceptance question. Signal that raises it: a receipt hash compared with later bytes. Rollback: none needed.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| `layer` retained only on accepted ADRs | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Frontmatter paragraph; profile lists in `docs/99.templates/registry.json` |
