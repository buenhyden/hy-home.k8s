---
title: "W03 Skill Form"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0177-TSK-0001"
parent_ids: ["SPEC-0177-PLAN-0001"]
---

# Task: W03 Skill Form

## Overview

This Task records the ninth phase-2 package of W03, the Skill form, for [SPEC-0177](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to follow the requirements where a choice is needed, to check existing work before the next task, and approved commit, push, PR and merge. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-skill-form` from `main` at `1ed9bf63` (PR #241 merged); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D07, W03-D08, W03-D10 and W03-D11; EVD-018 (current v14.7 requirements prevail).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Skill (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[15]); conditional content from `COMMON-ROLE-FORMS`; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | Registry form, extension, template profile, TemplateDefinitions, tables and bindings; tests. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-SKILL-002](../spec.md#success-criteria--verification-plan) | 19 documents and two templates moved with the map; policy texts; regression and exact-index QA. | platform | in-progress | PASS | EVD-005, EVD-006, EVD-007; exact-index QA at the implementation commit |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `f2e990df…`, plan.md `85e0646a…`, with a scratch simulation of the registry design and a mechanical application of the meaning map; 2026-11-13 | FAIL | REJECT: BLOCK the native twin's unquoted boolean constant fails `FM-QUOTE` under template mode, so a validator change is needed; FIXes on two synthetic-skill tests and the extension rows, heading levels under an H2 kept as H4, the `Output Format` heading cited by name, the authority line before the H1, `template_source` on the source, route escaping and placeholder grammar, policy sentences, and pointer lines for authored workflows and five skills without intro text. | no | none |
| EVD-002 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"b203a9713335b21c2fbbf3afc6d12369689bc0b3280b884a656a8df69f910583","plan_sha256":"a7c27239c2fd5fb367d670a9e5777fa5bc1151c288f0438dbcab73341e9481aa"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding verified fixed in the scratch simulation; no other change in meaning; verdict APPROVE with three optional NITs for the Task map (the exemption admits any boolean and `FM-VALUE-CONSTANT` enforces equality; the Roles README link is a responsibility router; `Output Format` is the H4 exception in `rca-methodology`). This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0177 approval question naming spec.md b203a971 and plan.md a7c27239 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0177","SPEC-0177-PLAN-0001"],"reviewed_spec_sha256":"b203a9713335b21c2fbbf3afc6d12369689bc0b3280b884a656a8df69f910583","reviewed_plan_sha256":"a7c27239c2fd5fb367d670a9e5777fa5bc1151c288f0438dbcab73341e9481aa","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, extension, template profile, tables, bindings, quote exemption and tests, red then green | Working tree over `15c42849`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_common_form_tree` 205 tests with 29 failures and 10 errors before the registry change; the quote regression failed with `FM-QUOTE` on the template twin before the code change; the two synthetic-skill tests failed with `BODY-HEADING-REQUIRED` once the profile was bound. Green: all OK (two skipped abstract bases); the regression also refuses quoted `"true"`, `false` and `yes` and keeps `FM-QUOTE` for authored profiles. The Skill form is built from COMMON-DOC-FORM-1 1.0.0 roles[15] by the mapping that reproduces the `agents` form; extension `skill-authority-boundary`; four profiles bound to `skill` with empty lists; `common/template-native-skill` with frontmatter equal to its source and `common/native-skill-package` naming it as `template_source`; both twins carry `Steps`; the FM-QUOTE exemption covers native and template profiles. | yes | none |
| EVD-005 | [VAL-SKILL-002](../spec.md#success-criteria--verification-plan) | WORK-002 | 19 documents and two templates meaning map | Implementer map (doc-writer subagent) and a multiset line comparison of every file against `HEAD`, read by the author | PASS | Removed lines are only old H2 headings, version and updated values, and the workflow Related Documents link bullets, whose links now sit in one line under When to Use; frontmatter and the authority sentence before each H1 are unchanged; fenced headings unchanged; `Output Format` kept as an H4 in `rca-methodology`; phases nested at H5 in `incident-postmortem` and `workspace-harness-audit`; `#### Completion` kept. The author restored `#### Workflow Steps` (four skills) and `#### Execution Mode` (`incident-postmortem`), which the implementer had dropped, so every source section under Steps keeps its heading as the Spec requires, and read each workflow pointer against its target text. Placement calls for owner review: empty skill H3s carry "None is stated in this document."; the five skills without intro text point When to Use to the frontmatter description; the workflows' Related Documents links, including the Roles responsibility router, all go to When to Use; workflow Failure Handling and Completion and Handoff point to named steps. | yes | none |
| EVD-006 | [VAL-SKILL-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, fragments, suites and lint | Author run over the staged index after `62df7117`, 2026-11-13 | PASS | The four strict document validators and `validate-agent-governance.py` exit 0 with output equal to the before run at `15c42849`. Fragment search: the only new line is this package's own Plan text; the 17 `work-lifecycle.md#completion` links resolve. `quality.py` PASS; markdownlint 0 issues; `ruff check scripts tests` and `ruff format --check scripts tests` clean; `graphify update .` rc 0. Suites: `agent-governance` 105, `ci-metadata` 87, `cluster-gate` 72, `document` 542, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK; `qa-runner` not re-run (known W03-H11 error). `.secrets.baseline` registry line 7054 moved to 7266 in `62df7117`. | yes | none |
| EVD-007 | [VAL-SKILL-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 29 files over `62df7117` | PASS | Risk class `medium` (registry, one frontmatter rule, tests, 17 procedures agents invoke and two workflows they load). Checklist: scope matches the Spec; one writer per file; the form equals the external contract; W03-D07 and W03-D10 applied; skill names, descriptions, invocation flags, bundle files and provider links unchanged; the quote exemption still needs the constant value; policy text `document-authoring.md` 3.15.0 and `docs/99.templates/README.md` 0.27.0; the ignored read-only contract input was read only; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow file changed. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-SKILL-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, skill reference files and assets, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's standing 2026-11-13 instruction
- **Static Validation**: strict document validators, agent-governance validator, fragment search, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface; native skill discovery is W07 evidence
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); criterion acceptance pending. Risk class `medium`.
