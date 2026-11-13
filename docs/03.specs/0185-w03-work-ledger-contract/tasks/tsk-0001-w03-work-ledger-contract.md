---
title: "W03 Work Ledger Contract"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0185-TSK-0001"
parent_ids: ["SPEC-0185-PLAN-0001"]
---

# Task: W03 Work Ledger Contract

## Overview

This Task records the first half of handoff W03-H30 (W03-D25): requirement, architecture and governance text, `ADR-0060` and the work residue ledger clarifications, for [SPEC-0185](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-work-ledger-contract` from `c54eed50` (`main` after PR #249, SPEC-0184); checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D25 and W03-H30.
- **Decision recorded with this package:** W03-D37 to W03-D40 (residue-only JSON ledger; on-demand view with pruning; seed now with exempt history; new ADR plus REQ and AD edits); user answers of 2026-11-13 to the GOV-06 ledger questions.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | Write `ADR-0060` as `proposed` with its README entry and the four dated clarifications; amend REQ-0003 and AD-0006. | platform | in-progress | PASS | EVD-006, EVD-007, EVD-010 |
| WORK-002 | [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | Governance and knowledge-map sentences; the superseding EVD row and refreshed state cells; regression and exact-index QA; then the Task Evidence row with the user's ADR-0060 acceptance answer and the `proposed` to `accepted` flip alone. | platform | in-progress | NOT_RUN | EVD-008, EVD-009, EVD-010, EVD-011; exact-index QA and ADR-0060 acceptance pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | FAIL | REJECT over spec.md `cd019398…` and plan.md `320267ca…`: BLOCK B1 (ADR creation and acceptance in one commit) and FIXes F1 to F9, applied to the drafts. | no | none |
| EVD-002 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"6a7a72e3fa3ea31195e5e6c00256e5c5c2d0b2e66dabc5ba83d9be8854bcf19a","plan_sha256":"5b36ab60875afbb91c12a52fcf6fe9773e1f13a0c1220e2115c3d7380e86fe2d"} | PASS | Same reviewer: round 2 APPROVE over the revised bytes with NIT-A (the `rg` criterion scope) and NIT-B (the route wording), both left to implementation and this Task. The approved bytes are the bytes named here; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 approval question naming spec.md 6a7a72e3 and plan.md 5b36ab60 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0185","SPEC-0185-PLAN-0001"],"reviewed_spec_sha256":"6a7a72e3fa3ea31195e5e6c00256e5c5c2d0b2e66dabc5ba83d9be8854bcf19a","reviewed_plan_sha256":"5b36ab60875afbb91c12a52fcf6fe9773e1f13a0c1220e2115c3d7380e86fe2d","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"90163654d94d30f15561eea10c65e3dff6cd1bf573c7759a193aa3189dc85019","plan_sha256":"90d0066eb5073abdea51ef31ea8b18e2a62502fb205340dd0674b3746d775dca"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-13: the only difference from the bytes approved in EVD-003 is the deleted frontmatter `layer` line in each file, required by SPEC-0184 (W03-D22) and announced by the open-package layer rule these bytes already named; facts re-checked on `main` `c54eed50` with line drift only. APPROVE. | yes | none |
| EVD-005 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md 90163654 and plan.md 90d0066e dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0185","SPEC-0185-PLAN-0001"],"reviewed_spec_sha256":"90163654d94d30f15561eea10c65e3dff6cd1bf573c7759a193aa3189dc85019","reviewed_plan_sha256":"90d0066eb5073abdea51ef31ea8b18e2a62502fb205340dd0674b3746d775dca","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-006 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Four strict document validators before the edit | Working tree over `2f2f9b7f`, uncommitted, 2026-11-13; `validate-document-contract-registry.py`, `validate-markdown-profiles.py`, `validate-links-and-owners.py` and `validate-document-lifecycle.py`, each `--root . --mode strict` | PASS | All four PASS (294 registry paths) before any edit; output kept in the session scratch record, not in the tree. | yes | none |
| EVD-007 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | ADR-0060, README entry, four ADR clarifications, REQ-0003 and AD-0006 text written | Working tree over `2f2f9b7f`, uncommitted, 2026-11-13; the Spec Contracts for the new ADR, REQ-0003 and AD-0006 | PASS | `ADR-0060` created `proposed` without a `layer` key, with its Korean README entry; a dated 2026-11-13 clarification added in ADR-0031, ADR-0036, ADR-0047 and ADR-0048 with version patch bumps; REQ-0003 FR-0019, FR-0022 with check cells, Scope and Non-goals, Evaluation Expectation and Traceability amended (minor bump); AD-0006 lines for the ledger disclaimer, central roster, memory paragraph, FR-0019 and FR-0022 rows and Archived Lineage entry amended (minor bump). The lineage entry does not say accepted. ADR-0060 acceptance is not recorded here. | yes | none |
| EVD-008 | [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Governance and knowledge-map sentences written | Working tree over `2f2f9b7f`, uncommitted, 2026-11-13; `work-lifecycle.md`, `context-and-memory.md`, `quality.md`, `document-authoring.md` and the knowledge-map Outputs | PASS | One clarifying sentence each (two in `work-lifecycle.md`, `context-and-memory.md` and `document-authoring.md` at the cited places) with patch bumps. `work-lifecycle.md` and `context-and-memory.md` name `ADR-0060` in plain text: a link from a governance file into Stage 02 is refused by `LINK-STAGE-BOUNDARY`, so the Spec's "cite it by link" is satisfied by the ID. | yes | none |
| EVD-009 | [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | SPEC-0161 Task superseding row and state cells | Working tree over `2f2f9b7f`, uncommitted, 2026-11-13; SPEC-0161 Task | PASS | One EVD row appended after EVD-045 with `Resolves` none citing EVD-006 to EVD-011; only the state cells of the `LEDGER` conflict row and the W03-H30 row refreshed; version patch bump; no earlier row, decision or handoff edited. | yes | none |
| EVD-010 | [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict validators, suites, quality gate and markdownlint after the edit | Working tree over `2f2f9b7f`, uncommitted, 2026-11-13; the same four validators, `run-contract-tests.py` suites `document`, `document-lifecycle` and `agent-governance`, `quality.py --root .`, `markdownlint-cli2` over the 14 edited files; run in a copy of the tree whose index added the new ADR, because the link validator reads tracked files only | PASS | Validator output equals EVD-006 except the registry path count (295, the new ADR); suites PASS (667, 24 and 105 tests, 3 skipped in `document`); quality gate PASS; markdownlint 0 issues. In the unstaged tree the link validator reports `BODY-LINK-BROKEN` for the untracked ADR until it is tracked; exact-index QA and commit hooks are not run. | yes | none |
| EVD-011 | [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | `rg` ledger checks read | Working tree over `2f2f9b7f`, uncommitted, 2026-11-13; `rg -n -i ledger docs .agents` and `rg -n -i "work residue ledger" docs .agents` | PASS | Every hit outside Stage 90 and the Task package forbids a progress, competing, separate, recovery or inventory ledger, names the retired progress or migration ledgers, or is a Contracts sentence; Stage 90 hits are excluded evidence. The `work residue ledger` list holds exactly the Contracts sentences plus ADR-0060, this package and the SPEC-0161 rows. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`ADR-0060` and its README entry, REQ-0003, AD-0006, the four dated ADR clarifications, five governance or skill sentences), this package, `docs/03.specs/README.md`, the W03-D37 to W03-D40 rows, evidence rows, the state cells of the `LEDGER` conflict row and the W03-H30 row, and the frontmatter `version` and `updated` of the SPEC-0161 Task, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: the ledger file, its schema, script and validator (package 2), any Stage 90 document, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; the acceptance of `ADR-0060` (a separate user answer recorded as Task Evidence before the `proposed` to `accepted` flip); push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, the `rg` checks of the Spec, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit (set `ADR-0060` back to `proposed` if only the flip is wrong); before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). After SPEC-0184 removed the `layer` key, the bytes without that line were reviewed (EVD-004) and approved by the user again (EVD-005); these are the committed bytes. The implementation text is written in the working tree and checked (EVD-006 to EVD-011); exact-index QA, the commit, the user's ADR-0060 acceptance and the `proposed` to `accepted` flip are not done.
