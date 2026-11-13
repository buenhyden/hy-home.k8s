---
title: "W03 SemVer Vocabulary and Version Fields Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0190-PLAN-0001"
parent_ids: ["SPEC-0190"]
---

# W03 SemVer Vocabulary and Version Fields Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no existing version value changes; no existing glossary row changes; and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Add `scripts/semver_grammar.py` with the SemVer 2.0.0 grammar, make `scripts/release.py`, the skill envelope check and the four schema patterns use or equal it, add the eight common glossary terms and the version rules, and test it with the revision's cases. [Task 0001](tasks/tsk-0001-w03-semver-vocabulary.md) owns execution and evidence.

## Context

A read of `main` at `c54eed50` found the grammars named in the Spec (one in the frontmatter schema, three in the profile schema, one in the skill envelope check, one in `release.py`), all 205 Markdown `version` values in strict SemVer core form, the registry contract versions `3.0.0` (WGOV-CORE) and `1.0.0` (COMMON-DOC-FORM-1), the registry `schema_version` 10, and the glossary common rows at `repository-vocabulary v14.5` without the eight terms. `scripts/release.py` already refuses `v01.2.3`, `v1.02.3`, `v1.2.03`, `v1.2.3-01` and `v1.2.3-alpha.01` in `tests/test_release.py`.

## Goals & In-Scope

- Code: `scripts/semver_grammar.py`, `scripts/release.py`, `scripts/validate-agent-governance.py`.
- Schemas: the `version` pattern of `frontmatter.schema.json` and the three of `document-profile.schema.json` (lines 48, 163 and 845).
- Text: eight glossary rows; the version paragraph; `scripts/README.md`.
- Tests: `tests/test_semver_grammar.py` in the `document` suite with the revision's valid, invalid and precedence cases against the module, each schema pattern, the skill envelope check and `release.py`; a pin test that each schema pattern equals the module's anchored grammar; the `release` suite unchanged.

## Non-Goals & Out-of-Scope

- Existing version values, the registry `schema_version`, identities, edition labels, version comparison for documents, tags and releases.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SEMVER-001](spec.md#success-criteria--verification-plan) | Module, release tag pattern, skill envelope check, schema patterns and tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-semver-vocabulary.md) | Case tests fail first, then pass; release tests pass unchanged. |
| WORK-002 | [VAL-SEMVER-002](spec.md#success-criteria--verification-plan) | Glossary terms, version paragraph, scripts README; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-semver-vocabulary.md) | Knowledge surface check, strict validators, the `document`, `agent-governance`, `release` and `tooling` suites, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators before any change.
- Show the case tests failing first on the old grammars, then passing.
- Commit order: the package commit with this Task, the Stage 03 README entry and the decision row W03-D45; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Record the risk class (`low`: one new module, four schema patterns and the skill envelope check made stricter with no current value affected, documentation text; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **A stricter pattern refuses a current value.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The survey found none and the strict validators compare before and after. Rollback: revert the implementation commit.
- **The schema copies drift from the module.** Possible, Minor: LOW, monitor. Owner: W05 code. The pin test fails on any difference. Rollback: none needed.
- **The release tag check changes behavior.** Unlikely, Moderate: LOW, monitor. Owner: W06. Its tests run unchanged. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| One SemVer 2.0.0 grammar for version values | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Version paragraph; `scripts/semver_grammar.py` |
| SemVer vocabulary | [Glossary](../../../.agents/knowledge/glossary.md) | Repository Vocabulary rows |
