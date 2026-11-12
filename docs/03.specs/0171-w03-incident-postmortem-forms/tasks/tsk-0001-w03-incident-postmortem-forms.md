---
title: "W03 Incident and Postmortem Forms"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0171-TSK-0001"
parent_ids: ["SPEC-0171-PLAN-0001"]
---

# Task: W03 Incident and Postmortem Forms

## Overview

This Task records the third phase-2 package of W03, the Incident and Postmortem forms, for [SPEC-0171](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-incident-forms` from `7cf95a2f` (SPEC-0170 closure; PR #235 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D08 and W03-D12; EVD-018 (current v14.7 requirements prevail); W03-H10 (covered by derived heading lists).
- **Decisions taken in this package:** on 2026-11-13 the user answered "Combine (Recommended)" to doing Incident and Postmortem in one package as an exception to W03-H01 (W03-D14), and "Register local H3 (Recommended)" to keeping What Went Well as a registered local H3 under Impact (W03-D15).
- **Required forms:** COMMON-DOC-FORM-1 1.0.0 Incident and Postmortem (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[9] and roles[10]); read-only input.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | Registry forms, extensions, TemplateDefinitions and tables; repository-registry and terminal-contract tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | Resolution-evidence lookup and its test; templates moved with the maps; consumer texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `c5cc649a…`, plan.md `c3551cf9…`; 2026-11-13 | FAIL | REJECT with no BLOCK: FIXes for unmapped incident instructions (affected environment, allowed status values, observed event), the Traceability H2 prompts, What Went Well and What Went Wrong placement (a user question, as for W03-D13), Lifecycle Traceability row identities, missing consumer paths (`quality.py`, `docs/05.operations/AGENTS.md`), decision citations (D11 does not apply; cite H01 and H10) and the W03-H01 departure as a user question. | no | none |
| EVD-002 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"e54e2cc30d920dd9f9ecf39017acb3c9184f8fda6400a5c9d9cb0b247502f2da","plan_sha256":"fb889f8ae4b595a22fda2a43b4f7229625d3212fd5298148239c83c40cb3dd45"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding closed, including the user's W03-D14 (one package) and W03-D15 (`What Went Well` local H3, checked against the registry extension and tree checks); verdict APPROVE with no BLOCK or FIX; three optional NOTEs, of which the SPEC-0161 Task `updated` date was applied outside the reviewed bytes. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0171 approval question naming spec.md e54e2cc3 and plan.md fb889f8a dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0171","SPEC-0171-PLAN-0001"],"reviewed_spec_sha256":"e54e2cc30d920dd9f9ecf39017acb3c9184f8fda6400a5c9d9cb0b247502f2da","reviewed_plan_sha256":"fb889f8ae4b595a22fda2a43b4f7229625d3212fd5298148239c83c40cb3dd45","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (including the W03-D14 and W03-D15 rows of the SPEC-0161 Task), this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle` and `agent-governance` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003). Implementation not started.
