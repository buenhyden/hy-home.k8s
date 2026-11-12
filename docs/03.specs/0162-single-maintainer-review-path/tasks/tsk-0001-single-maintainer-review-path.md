---
title: "Single-Maintainer Review Path"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0162-TSK-0001"
parent_ids: ["SPEC-0162-PLAN-0001"]
---

# Task: Single-Maintainer Review Path

## Overview

This Task records the GIT-09 review-path change for [SPEC-0162](../spec.md) under its [Plan](../plan.md). The user approved the Spec and Plan on 2026-11-12 and confirmed the exact reviewed bytes (EVD-002, EVD-003).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user asked to continue every remaining item and, where an existing rule conflicts with the current v14.7 requirement, to change it to match ([SPEC-0161](../../0161-w00-v14-7-delta-intake/spec.md) Task, EVD-018). GIT-09 is the first adopted conflict. The user answered "Approve and proceed" to the draft and "Confirm approval" to the exact revised bytes. Neither answer accepts a criterion or authorizes a push, PR or merge.
- **Base:** branch `claude/w00-v14-7-intake` after `af7484ec`.
- **Requirement source:** package `REQUIREMENTS.json` GIT-09 (SHA-256 of the file `4c9da241ba185310048f3231815c04ed42dc7ce54c44e201f97e469f5945084b`).

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REVIEW-001](../spec.md#success-criteria--verification-plan), [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | Edit the six owners, search for remaining agent-review obligations, record the checklist review. | platform | frontmatter | PASS | EVD-006 (search, resolves EVD-004) and EVD-007 with EVD-008 (checklist and exact-index QA, resolve EVD-005) pass; criterion acceptance is the operator's decision. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-REVIEW-001](../spec.md#success-criteria--verification-plan), [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review rounds | Read-only code-reviewer that wrote none of the package, over spec.md `9615e814…` and plan.md `c0ba3195…` (round 1) and spec.md `c0ff7557…` and plan.md `fd4dd57b…` (round 2); 2026-11-12 | PASS | Round 1 REJECT: GIT-09 recovery and records missing, search pattern too narrow, the handoff reviewer field and the Stage 03 role row out of scope, ADR-0052's retired `independent-review` App check unexplained, second-approval rule too narrow, proxy prohibition missing, risk class too low. Round 2 APPROVE with one FIX (Core Design wording), applied. | no | none |
| EVD-002 | [VAL-REVIEW-001](../spec.md#success-criteria--verification-plan), [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"dcc79e34c67f9adc81d05a6b6a0d1ef4fd3cea8af0e8a7bb8fc261fa30eedfe6","plan_sha256":"fd4dd57b63ea9461f38acccf81eb9a7225ba2fd6e1ac8b3ba14879e4d19ddcc7"} | PASS | Same reviewer, round 3, 2026-11-12: both hashes matched; reverse-substituting the one changed sentence reproduces the round-2 Spec bytes; verdict APPROVE, no BLOCK. The reviewer is independent of the author, not of the approver; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-REVIEW-001](../spec.md#success-criteria--verification-plan), [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Confirm approval to the SPEC-0162 exact-byte question dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0162","SPEC-0162-PLAN-0001"],"reviewed_spec_sha256":"dcc79e34c67f9adc81d05a6b6a0d1ef4fd3cea8af0e8a7bb8fc261fa30eedfe6","reviewed_plan_sha256":"fd4dd57b63ea9461f38acccf81eb9a7225ba2fd6e1ac8b3ba14879e4d19ddcc7","validity":"confirmed","revocation":"none"} | PASS | The user first answered "Approve and proceed" to the draft, then confirmed these exact revised bytes. No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-REVIEW-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Agent-review obligation search | The Spec's search terms over the current owners after the edits | NOT_RUN | Pending the edits. | yes | none |
| EVD-005 | [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Core-diff checklist and exact-index QA | The implementation commit's exact index | NOT_RUN | Pending the edits. | yes | none |
| EVD-006 | [VAL-REVIEW-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Agent-review obligation search | `git grep` for `independent read-only`, `independent review`, `new-context review`, `separate agent identity`, `reviewer identity`, `second reviewer`, `read-only agent`, `Independent change review` over `.agents`, `.claude`, `.codex`, `docs/AGENTS.md`, `docs/*/AGENTS.md`, REQ-0003 and `docs/02.architecture/decisions`, on the edited worktree after `2402a7c1`; 2026-11-12 | PASS | Changed: `quality.md` Semantic review, Pull request row and handoff field; `git.md` completion and offset sentence; `work-lifecycle.md` Completion 1; `document-lifecycle.md` review row; REQ-0003 FR-0018 rows, Evaluation Expectation and Scope sentence; `docs/03.specs/AGENTS.md` role row. Remaining hits: optional review and optional reviewer identity (`quality.md`), the offset sentence now naming checks, checklist and owner merge (`git.md`), `document-authoring.md` evidence kind, ADR-0047/0052/0056/0057 generic "independent review" (defined by `quality.md`; ADR-0052's App check retired 2026-11-03), REQ-0003 closure history. No current rule requires an agent reviewer. | yes | EVD-004 |
| EVD-007 | [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Core-diff checklist and exact-index QA | Implementation diff of six owners (64 insertions, 49 deletions); risk class `high`; `python3 scripts/qa.py staged` and the commit hooks on the implementation commit's exact index with the scratch venv; 2026-11-12 | PASS | Checklist: acceptance matches VAL-REVIEW-001/002; one writer (W01) per file; consistent with GIT-09 and the Spec contracts; no check removed or weakened (`BLOCK` still blocks, missing automation stays a gap); no secret; permissions, triggers and protected actions unchanged, only the completion wording; recovery: revert this commit. Findings: none open. QA result recorded below in EVD-008 after the commit. | yes | none |
| EVD-008 | [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Core-diff checklist and exact-index QA | Implementation commit `f0aa80cf` (tree `0908582282a7e6d5f2c97900b6c78246c430406f`); `python3 scripts/qa.py staged` and the commit hooks with the scratch venv (pre-commit 4.6.1, jsonschema 4.26.0); 2026-11-12 | PASS | Staged QA passed agent-governance, document-contract-registry, document-lifecycle, knowledge-surface, links-and-owners, markdown-profiles, repository-quality, selected-nonstyle and selected-style; the Staged QA Snapshot, commitizen and commit-message-exception hooks passed. With the EVD-007 checklist this closes EVD-005. | yes | EVD-005 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-REVIEW-001](../spec.md#success-criteria--verification-plan) | pending | none | Run the search after the edits | platform |
| [VAL-REVIEW-002](../spec.md#success-criteria--verification-plan) | pending | none | Checklist and exact-index QA after the edits | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `docs/03.specs/README.md`, `docs/03.specs/AGENTS.md` (role row only), `.agents/governance/quality.md`, `.agents/governance/git.md`, `.agents/governance/document-lifecycle.md`, `.agents/workflows/work-lifecycle.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md` (FR-0018 rows, Evaluation Expectation, Scope sentence, Traceability back-link), `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: validators, tests, hooks, workflows, registry, templates and ADRs
- **Approval Required**: criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; the package commit can be reverted separately
- **Evidence Location**: this Task

## Verification Summary

The edits are in `f0aa80cf`; the search (EVD-006) and the checklist with exact-index QA (EVD-007, EVD-008) pass; criterion acceptance is pending the operator. Risk class `high` (pull-request completion and merge-direction wording).
