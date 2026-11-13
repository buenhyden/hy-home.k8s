---
title: "W03 Retired Identity Reservation"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0001"
parent_ids: ["SPEC-0180-PLAN-0001"]
---

# Task: W03 Retired Identity Reservation

## Overview

This Task records handoff W03-H03 (from W02-H01), the reservation of retired identities named in `Archived Lineage`, for [SPEC-0180](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to investigate remaining, unverified, unreviewed, unconfirmed, unstarted, conflicting and missing items, to follow the W00 to W03 requirements where a choice or correction is needed, to present decisions with options, to check existing work first, to do now anything due before W03, to start work that can run in parallel, and approved commit, push, PR and merge. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-retired-identity` from `9308095a` (`main` merge of PR #244); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W02-H01, W03-H03 and EVD-018 (current v14.7 requirements prevail); EVD-023 and EVD-024 observed the gap.
- **Decisions recorded with this package:** W03-D22 (`layer`), W03-D23 (`title`) and W03-D24 (generator), from the user's 2026-11-13 answers, and the rows W03-H14 to W03-H24 from the 2026-11-13 read-only W03 gap audit; all appended to the SPEC-0161 Task.
- **Requirement basis:** the lifecycle policy rule that stable identities are append-only and never reused; REQ-0003-FR-0023; read-only inputs under `_workspace/workspace_execution_tasks/`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | Lineage-identity helper; evidence-context field; reuse check and callers; history memo; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | Policy sentence; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `7d0a1563…`, plan.md `a29f3710…`, with scratch simulations of the lineage tokens over the tracked tree and a replay over 120 first-parent commits; 2026-11-13 | FAIL | REJECT: BLOCK `compare_lifecycle` holds no text, so the retired set must travel on `LifecycleEvidenceContext` filled by `_evidence_context`; FIXes on the identity grammar (schema `terminalArtifactId` plus historical prefixes), a dangling decision reference, end-to-end tests, a per-commit memo and the risk scoring; NITs on the reservation source, table parsing, the keyword-only argument and the Task text. The reviewer found six lineage documents, about 200 tokens in three shapes, no live identity newly refused and no replay hit. | no | none |
| EVD-002 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"8d43328200a7f60f050eee01bffe239eda247130fe1a17b267852820e4a25464","plan_sha256":"ba7e926a3cb13eb987ca28bc841aae0433b9e49623e92930f6e89a5af47c60df"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: every round-1 finding verified fixed; round 2 asked the Plan to name the SPEC-0161 rows and the Spec to define them, both verified in round 3 with no other change in meaning; verdict APPROVE. The package commit must append W03-D22 to W03-D24, which the Spec cites. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0180 approval question naming spec.md 8d433282 and plan.md ba7e926a dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0180","SPEC-0180-PLAN-0001"],"reviewed_spec_sha256":"8d43328200a7f60f050eee01bffe239eda247130fe1a17b267852820e4a25464","reviewed_plan_sha256":"ba7e926a3cb13eb987ca28bc841aae0433b9e49623e92930f6e89a5af47c60df","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RETIRED-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-RETIRED-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D22 to W03-D24, W03-H14 and later and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: every `Archived Lineage` row and other document body, `_workspace/workspace_execution_tasks/`, `.github/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's standing 2026-11-13 instruction
- **Static Validation**: strict document validators, `document-lifecycle`, `document` and `validation-routing` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started. When accepted, this package closes W03-H03 and W02-H01.
