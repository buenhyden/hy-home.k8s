---
title: "W03 Runbook Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0170-TSK-0001"
parent_ids: ["SPEC-0170-PLAN-0001"]
---

# Task: W03 Runbook Form

## Overview

This Task records the second phase-2 package of W03, the Runbook form, for [SPEC-0170](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user again asked to investigate every remaining, unverified, unreviewed, unconfirmed, unprogressed, conflicting and missing W03 item, review each and continue, fixing existing rules that conflict with current requirements. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-runbook-form` from `8b9d54a6` (SPEC-0169 closure, merged into `main` by PR #234); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D04, W03-D08 and W03-D11; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** W03-D13, the user's direct answer "Register local H3 (Recommended)" on 2026-11-12 to the question of where non-rollback recovery procedures go: a registered conditional local H3 `Recovery Procedures` under Recovery.
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Runbook (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[7]); read-only input.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | Registry form, extension, TemplateDefinition and tables; repository-registry tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-RUNBOOKFORM-002](../spec.md#success-criteria--verification-plan) | Template and ten runbooks moved form-only with the meaning map; policy, README and skill text; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `be71c941…`, plan.md `bcd402f9…`; 2026-11-12 | FAIL | REJECT: BLOCK recovery procedures as H4 directly under the Recovery H2 fail markdownlint MD001 (reproduced) in five runbooks; BLOCK the claim of no anchor link is false (0010 links `#recovery-and-escalation`, which the link validator skips); FIXes: PR #234 stated open but merged, heading-level rule too narrow, troubleshooting placement, untyped control-surface and tooling links, Korean none-lines and markdownlint command; NOTEs on named tests, executor sentences, H3 count and the stale runbooks README. | no | none |
| EVD-002 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"c82ae4154f804acc002a6d5dd2e49a9d3aa32b70029b8bdb0a3e377731d6d3b1","plan_sha256":"252b893e1b41d628685bd464307b039f3b6b007a12adf432e56187b8e39acecc"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-12: round 2 confirmed every round-1 finding closed, including the user's W03-D13 `Recovery Procedures` local H3 (checked against the tree and registry extension checks), and APPROVE with four wording items; the author applied them; round 3 confirmed both hashes and that only those edits changed, verdict APPROVE; the first package commit was then refused by `LANG-ENGLISH-FIRST` because spec.md quoted Korean runbook text on two lines, which the author replaced with English descriptions; round 4 confirmed only those two lines changed with unchanged meaning, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0170 re-approval question naming spec.md c82ae415 and plan.md 252b893e dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0170","SPEC-0170-PLAN-0001"],"reviewed_spec_sha256":"c82ae4154f804acc002a6d5dd2e49a9d3aa32b70029b8bdb0a3e377731d6d3b1","reviewed_plan_sha256":"252b893e1b41d628685bd464307b039f3b6b007a12adf432e56187b8e39acecc","validity":"confirmed","revocation":"none"} | PASS | The earlier answer approving spec.md `db5c7b5e…` lapsed when those bytes changed; this receipt names the current bytes. Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-RUNBOOKFORM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (including the W03-D13 row of the SPEC-0161 Task), this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle` and `agent-governance` suites, repository quality gate, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface and no runbook command is run
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003). Implementation not started.
