---
title: "W03 AGENTS Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0176-PLAN-0001"
parent_ids: ["SPEC-0176"]
---

# W03 AGENTS Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes outside the 16 `AGENTS.md` files and the new template, and the output of the four strict document validators and the agent-governance validator over the tree is equal before and after.

## Overview

Add the AGENTS form, its template profile and TemplateDefinition; bind the folder profile, widen it to the root file and narrow the root shim to `CLAUDE.md`; make the gateway rule count content lines; move the 16 files form-only; record W03-D18; update the policy texts. [Task 0001](tasks/tsk-0001-w03-agents-form.md) owns execution and evidence.

## Context

SPEC-0175 gave the Policy role its form; its PR #240 is merged (`094eb1c6`), so `main` contains `8df46a30`, the SPEC-0175 closure, from which this branch `claude/w03-agents-form` starts; before delivery it is checked against the current `main`. A read at `8df46a30` found:

- the root `AGENTS.md` on `common/root-provider-shim` (24 lines, with two `Read ... before acting.` lines before the H1) and 15 folder `AGENTS.md` files on `common/folder-agents-guide` (H2 Purpose, Responsibilities and Projections, Rules and Checks; `docs/AGENTS.md` has no Checks and `examples/azure/AGENTS.md` has Folder Rules instead);
- both profiles `native`, without frontmatter, H2 lists or a template; `common/root-provider-shim` also selects the root `CLAUDE.md`;
- `scripts/validate-agent-governance.py` refusing a root gateway over 30 lines (`AGENT-NATIVE-REFERENCE`), with no test that pins the count;
- `scripts/validation/repository/quality.py` checking only that a folder `AGENTS.md` has a sibling README and a one-line `@AGENTS.md` import, and `scripts/provider_write_guard.py` reading folder files whole;
- no table in the 16 files whose first header is `Rule`;
- a paragraph between the H1 and the first H2 in every folder file, whose chain markers `tests/test_k8s_pre_edit_hook.py` pins;
- staged QA routing that sends some folder `AGENTS.md` files to surfaces without the markdown-profile or registry validator (handed to W05 as W03-H12).

## Goals & In-Scope

- Registry: form, template profile and TemplateDefinition, path patterns, role binding.
- Code: the gateway content-line rule.
- 16 files moved per the Spec's map; the new template; policy texts; W03-D18, W03-H12 and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: registry, form, table, language-route and gateway cases.

## Non-Goals & Out-of-Scope

- Root and folder `CLAUDE.md`; `SKILL.md` and workflows; native loading evidence (W07); provider settings; the Workspace and Reference Pack README roles; phase 3.
- New rules, permissions or commands in any `AGENTS.md`.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AGENTS-001](spec.md#success-criteria--verification-plan) | Registry form, template profile, TemplateDefinition, table, patterns and binding; gateway rule; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-agents-form.md) | Failing tests first, then passing; strict registry and agent-governance checks; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-AGENTS-002](spec.md#success-criteria--verification-plan) | 16 files and the template moved with the map; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-agents-form.md) | Strict validators, agent-governance, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators and the agent-governance validator over the whole tree before any change.
- Show each changed test failing before its change, then passing.
- Record per document in the Task: where each H2 went and every added line; run a line comparison per document.
- Commit order: the package commit with this package's entry in `docs/03.specs/README.md` and the W03-D18 rows; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, one provider gate, tests and the 16 instruction files agents load; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **Meaning drift in instruction files agents load.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Line comparison per file, no list split, and the map in the Task; the user accepts the placements. Review cue: a removed or reworded rule line. Signal that raises it: any changed rule line in the comparison. Rollback: revert the implementation commit.
- **The root gateway stops loading or stops being thin.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author with W07. The loader lines keep their exact text and place, the required references and catalog ban stay, and only blank and heading lines leave the count. Review cue: an `AGENT-NATIVE-REFERENCE` diagnostic. Signal that raises it: a W07 observation that Codex reads the gateway differently. Rollback: revert the implementation commit.
- **Pointer lines read as new rules.** Possible, Minor: LOW, accept with review. Owner: W03 author. Each line names existing text or says none; the Task lists them for the user. Review cue: the acceptance question. Signal that raises it: the user asks to reword a line. Rollback: a follow-up edit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| AGENTS form, its template and the gateway content-line rule | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; machine form in `docs/99.templates/registry.json`; rule in `scripts/validate-agent-governance.py` |
