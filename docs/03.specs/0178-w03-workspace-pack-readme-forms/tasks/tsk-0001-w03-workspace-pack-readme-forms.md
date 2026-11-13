---
title: "W03 Workspace and Reference Pack README Forms"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0178-TSK-0001"
parent_ids: ["SPEC-0178-PLAN-0001"]
---

# Task: W03 Workspace and Reference Pack README Forms

## Overview

This Task records the last phase-2 package of W03, the Workspace and Reference Pack README forms, for [SPEC-0178](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to follow the requirements where a choice or correction is needed, to check existing work before the next task, and approved commit, push, PR and merge. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-workspace-pack-readme-form` from `ed91d165` (SPEC-0177 closure; PR #242 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D09 and W03-D10; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** asked which single index title the Reference Pack form uses, given `Report Index` in research and audit packs and `Item Index` in data packs, the user answered on 2026-11-13 "follow the requirements"; DOC-01 requires one form per README role, so following the W03-D10 `Pack Contract` pattern the title is `Pack Index` (W03-D19).
- **Requirement basis:** DOC-01 (same-role READMEs share one form) and the TEMPLATE-DEFINITION-CONTRACT note that the role table is not a closed list; read-only inputs under `_workspace/workspace_execution_tasks/`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | Role list and schema; forms, local H3s, TemplateDefinitions, bindings and navigation; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-LOCALREADME-002](../spec.md#success-criteria--verification-plan) | Pack renames; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `7a4d9d23…`, plan.md `146a3cea…`, with a scratch simulation of both forms, the role additions, the bindings and the renames; 2026-11-13 | FAIL | REJECT: BLOCK research pack 0001's link-list `Related Documents` fails the empty-section check unless the section is `link_only`; BLOCK three sentences name a renamed heading in prose; FIXes on review-only closure enforcement, the `DocumentRole` literal and its parity test, a missing schema-enum test, and the form-level fields and local-form marking. The reviewer confirmed the requirements support two local roles and the `Pack Index` choice. | no | none |
| EVD-002 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"a102d0add1b7293f416a38e1ed6fbf49fdceae0d507164f6f0aebe24c300b466","plan_sha256":"59412d600de7fdade38bb420e0b2f774b7b12f9783a19502a517d69bf8671810"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding verified fixed in the simulation, including the author's narrowing of the text search to the pack folders because `Item Index` is also an unrelated `.agents/` collection heading; no other change in meaning; verdict APPROVE. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0178 approval question naming spec.md a102d0ad and plan.md 59412d60 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0178","SPEC-0178-PLAN-0001"],"reviewed_spec_sha256":"a102d0add1b7293f416a38e1ed6fbf49fdceae0d507164f6f0aebe24c300b466","reviewed_plan_sha256":"59412d600de7fdade38bb420e0b2f774b7b12f9783a19502a517d69bf8671810","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-LOCALREADME-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D19 and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, the seven Workspace README bodies, `_workspace/workspace_execution_tasks/`, Stage 90 report documents, `.github/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's standing 2026-11-13 instruction
- **Static Validation**: strict document validators, fragment search, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
