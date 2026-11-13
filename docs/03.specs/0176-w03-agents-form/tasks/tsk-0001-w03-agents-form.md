---
title: "W03 AGENTS Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0176-TSK-0001"
parent_ids: ["SPEC-0176-PLAN-0001"]
---

# Task: W03 AGENTS Form

## Overview

This Task records the eighth phase-2 package of W03, the AGENTS form, for [SPEC-0176](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items and said W03 must be complete before W04. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-agents-form` from `8df46a30` (SPEC-0175 closure, contained in `main` after PR #240 merged as `094eb1c6`); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08 and W03-D10; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** asked whether the root `AGENTS.md` takes the AGENTS form although the 30-line thin-gateway rule would refuse it, the user answered on 2026-11-13 "follow the requirements"; DOC-02 and COMMON-DOC-FORM-1 give every `AGENTS.md` the AGENTS role, so the root file takes the form and the gateway rule counts content lines (W03-D18). A staged QA routing gap found in review is handed to W05 (W03-H12), following the work split the requirements set.
- **Required form:** COMMON-DOC-FORM-1 1.0.0 AGENTS (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[14]); conditional content from `COMMON-ROLE-FORMS`; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | Registry form, template profile, TemplateDefinition, table, patterns and binding; gateway rule; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | 16 files and the template moved with the map; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `3e70d053…`, plan.md `bf299adc…`, with a scratch simulation of the proposed registry, template, formed root file and gateway rule; 2026-11-13 | FAIL | REJECT: BLOCK six document-suite failures from test pins the Spec did not name (form constants and loop, the policy-role test, the template placeholder grammar, the root-file residue assertion); FIXes on the template twin's frontmatter, the folder preamble paragraph, the exact gateway count with a heading cap, two stale policy sentences, PR #240 being merged, a staged QA routing gap, consumer paths and the stated reading of the requirements. The reviewer confirmed that the requirements bind the root file, that native profiles can carry the form and template, and that a formed root file passes with the changed count. | no | none |
| EVD-002 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"4efeeba527de43cbb6ca836ad2bf2e03be7845dc569516e444bef9e6528caf20","plan_sha256":"b094721c76ad01dc39e360fd4552b555792faa3cc18e32486ee4fb862bf5c858"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 item closed (the routing gap by the requirements' work split, handed to W05 as W03-H12); one wording fix in the Interfaces bullet, applied without changing meaning; verdict APPROVE. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0176 approval question naming spec.md 4efeeba5 and plan.md b094721c dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0176","SPEC-0176-PLAN-0001"],"reviewed_spec_sha256":"4efeeba527de43cbb6ca836ad2bf2e03be7845dc569516e444bef9e6528caf20","reviewed_plan_sha256":"b094721c76ad01dc39e360fd4552b555792faa3cc18e32486ee4fb862bf5c858","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D18 and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, root and folder `CLAUDE.md`, `.claude/`, `.codex/`, `.github/` other than `.github/AGENTS.md`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, agent-governance validator, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface; native loading is W07 evidence
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
