---
title: "W03 Skill Form"
version: "0.1.0"
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
| WORK-001 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | Registry form, extension, template profile, TemplateDefinitions, tables and bindings; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-SKILL-002](../spec.md#success-criteria--verification-plan) | 19 documents and two templates moved with the map; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `f2e990df…`, plan.md `85e0646a…`, with a scratch simulation of the registry design and a mechanical application of the meaning map; 2026-11-13 | FAIL | REJECT: BLOCK the native twin's unquoted boolean constant fails `FM-QUOTE` under template mode, so a validator change is needed; FIXes on two synthetic-skill tests and the extension rows, heading levels under an H2 kept as H4, the `Output Format` heading cited by name, the authority line before the H1, `template_source` on the source, route escaping and placeholder grammar, policy sentences, and pointer lines for authored workflows and five skills without intro text. | no | none |
| EVD-002 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"b203a9713335b21c2fbbf3afc6d12369689bc0b3280b884a656a8df69f910583","plan_sha256":"a7c27239c2fd5fb367d670a9e5777fa5bc1151c288f0438dbcab73341e9481aa"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding verified fixed in the scratch simulation; no other change in meaning; verdict APPROVE with three optional NITs for the Task map (the exemption admits any boolean and `FM-VALUE-CONSTANT` enforces equality; the Roles README link is a responsibility router; `Output Format` is the H4 exception in `rca-methodology`). This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-SKILL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0177 approval question naming spec.md b203a971 and plan.md a7c27239 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0177","SPEC-0177-PLAN-0001"],"reviewed_spec_sha256":"b203a9713335b21c2fbbf3afc6d12369689bc0b3280b884a656a8df69f910583","reviewed_plan_sha256":"a7c27239c2fd5fb367d670a9e5777fa5bc1151c288f0438dbcab73341e9481aa","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

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

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
