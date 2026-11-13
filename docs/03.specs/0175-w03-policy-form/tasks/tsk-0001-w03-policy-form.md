---
title: "W03 Policy Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0175-TSK-0001"
parent_ids: ["SPEC-0175-PLAN-0001"]
---

# Task: W03 Policy Form

## Overview

This Task records the seventh phase-2 package of W03, the Policy form, for [SPEC-0175](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-policy-form` from `3d9428b9` (SPEC-0174 closure; PR #239 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D04, W03-D06, W03-D08 and W03-D11; W03-H10 (Policy part); SPEC-0168 (one policy role); EVD-018 (current v14.7 requirements prevail).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Policy (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[8]); conditional content from `TEMPLATE-DEFINITION-CONTRACT.md`; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | Registry form, extension, TemplateDefinitions, tables, lists and body contract; `REGISTRY_TABLE_TWIN`; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | 14 documents and two templates moved with the map; anchor edits; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review rounds 1 to 3 | Read-only code-reviewer that wrote none of the package, over spec.md `1b28926f…`, `b3bb7df5…`, `cad60e62…` and plan.md `dec757e4…`, `d31280b5…`, `ebbac4aa…`; 2026-11-13 | FAIL | REJECT three times. Round 1: BLOCK four of nine links into removed H2 anchors unnamed (the link validator checks no cross-file fragment); FIXes on test pins and the per-form loop, the twin body contract, the Stage 99 README bullets, Related Documents link typing, none lines that would deny existing text, and the risk rating. Round 2: BLOCK link kinds without one destination; FIXes to list the fragment search as a command and as the evidence for the anchor edits. Round 3: BLOCK a contradiction on `sdlc.md`; FIX for the document-profile registry link. The author applied each. | no | none |
| EVD-002 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"6168372e9a5b2e613eda16bbe4f1ecc3d065e52f371f1c53aebadb59a4af52f4","plan_sha256":"ebbac4aa9474b067b69423ecdf51cf502ffa2ce89f7fb2402eb5810787e2bfaa"} | PASS | Same reviewer, round 4, 2026-11-13: only the round-3 line changed, every Related Documents link of the 14 documents has one destination, every earlier finding is closed; verdict APPROVE. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0175 approval question naming spec.md 6168372e and plan.md ebbac4aa dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0175","SPEC-0175-PLAN-0001"],"reviewed_spec_sha256":"6168372e9a5b2e613eda16bbe4f1ecc3d065e52f371f1c53aebadb59a4af52f4","reviewed_plan_sha256":"ebbac4aa9474b067b69423ecdf51cf502ffa2ce89f7fb2402eb5810787e2bfaa","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003). Implementation not started.
