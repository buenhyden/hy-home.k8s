---
title: "W03 Skill Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0177-PLAN-0001"
parent_ids: ["SPEC-0177"]
---

# W03 Skill Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading changes outside the 17 `SKILL.md` packages, the two workflows and the two templates, and the output of the four strict document validators and the agent-governance validator over the tree is equal before and after.

## Overview

Add the Skill form with its local extension, the native template and its profile, both TemplateDefinitions and tables; bind the four profiles; move the 19 documents and two templates form-only; update the policy texts. [Task 0001](tasks/tsk-0001-w03-skill-form.md) owns execution and evidence.

## Context

SPEC-0176 gave the AGENTS role its form; its PR #241 is merged (`1ed9bf63`), and this branch `claude/w03-skill-form` starts from that `main` commit. A read at `1ed9bf63` found:

- 17 `SKILL.md` packages (47 to 158 lines, native frontmatter `name`, `description`, `metadata`, `disable-model-invocation`), with 28 distinct H2 titles; `When NOT to Use` in all 17 and `Workflow Steps` in 15; H3s only in `incident-postmortem` and `workspace-harness-audit`; one H1 each outside fenced examples;
- two workflows on `governance/skill` with the six H2 headings Overview, Authority Boundary, Governance Context, Current Contract, Validation and Refresh and Related Documents, and an existing template;
- the only fragment into these files, `work-lifecycle.md#completion`, used by 17 role files and pointing to an H3;
- no code that reads skill or workflow headings; `scripts/validate-agent-governance.py` checks skill frontmatter, bundle reachability and projections;
- no table in the 19 documents whose first header is `Step`;
- an authority sentence between the frontmatter and the H1 in every `SKILL.md`;
- `Output Format` in `rca-methodology` cited by name in its own text and in `incident-postmortem`;
- the frontmatter quote exemption in `scripts/validate-markdown-profiles.py` limited to native profiles, which a template twin of a native skill needs too.

## Goals & In-Scope

- Registry: form and extension, new template profile, TemplateDefinitions and tables, bindings and empty lists.
- Code: the frontmatter quote exemption for template profiles.
- 19 documents and two templates moved per the Spec's map; policy texts.
- Tests: registry, form, extension and table cases.

## Non-Goals & Out-of-Scope

- Skill reference files and assets; provider links and projections; skill names, descriptions and invocation flags; the Workspace and Reference Pack README roles; phase 3.
- New steps, rules, permissions or commands.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SKILL-001](spec.md#success-criteria--verification-plan) | Registry form, extension, template profile, TemplateDefinitions, tables and bindings; the frontmatter quote exemption; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-skill-form.md) | Failing tests first, then passing, including the quote-exemption regression; strict registry and agent-governance checks; the baseline line moved in its own commit first. |
| WORK-002 | [VAL-SKILL-002](spec.md#success-criteria--verification-plan) | 19 documents and two templates moved with the map; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-skill-form.md) | Strict validators, agent-governance, fragment search, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators, the agent-governance validator and the fragment search before any change.
- Show each changed test failing before its change, then passing.
- Record per document in the Task: where each H2 went and every added line; run a line comparison per document.
- Commit order: the package commit with this package's entry in `docs/03.specs/README.md`; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after any code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, one frontmatter rule, tests, 17 procedures agents invoke and two workflows they load; no permission, trigger, hook or workflow file) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **Meaning drift in procedures agents invoke.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. Line comparison per document, no list split, frontmatter untouched and the map in the Task; the user accepts the placements. Review cue: a removed or reworded step. Signal that raises it: any changed step line in the comparison. Rollback: revert the implementation commit.
- **A skill stops loading or a bundle file becomes unreachable.** Unlikely, Moderate: LOW, monitor. Owner: W03 author with W07. Frontmatter, names and links stay; the agent-governance validator checks bundles and projections and must equal the before run. Review cue: an agent-governance diagnostic. Signal that raises it: a W07 observation of a missing skill. Rollback: revert the implementation commit.
- **The widened quote exemption admits a wrong value.** Unlikely, Minor: LOW, accept. Owner: W05 code. The exemption still requires the value to equal the profile's boolean constant; the regression refuses a quoted or different value. Review cue: an `FM-QUOTE` or `FM-VALUE-CONSTANT` gap in tests. Signal that raises it: a template carrying a wrong boolean. Rollback: revert the implementation commit.
- **Pointer lines read as new steps.** Possible, Minor: LOW, accept with review. Owner: W03 author. Each line names existing text or says none; the Task lists them. Review cue: the acceptance question. Signal that raises it: the user asks to reword a line. Rollback: a follow-up edit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Skill form, its local extension and the native template | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; machine form in `docs/99.templates/registry.json` |
