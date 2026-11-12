---
title: "W03 Root README Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0172-TSK-0001"
parent_ids: ["SPEC-0172-PLAN-0001"]
---

# Task: W03 Root README Form

## Overview

This Task records the fourth phase-2 package of W03, the Root README form, for [SPEC-0172](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-readme-forms` from `40b44bd4` (SPEC-0171 closure; PR #236 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08, W03-D10 and W03-D11; handoff W03-H10; EVD-018 (current v14.7 requirements prevail).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Root README (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[11]); read-only input.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinition, table and navigation section; navigation rule and reader; optional trailing columns; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-ROOTREADME-002](../spec.md#success-criteria--verification-plan) | `README.md` and template moved with the map; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `92ac2a6e…`, plan.md `35a9061f…`; 2026-11-13 | FAIL | APPROVE in substance but five FIXes changed text: README counts (44, 26, 17 H3), the reader level and duplicate-title ambiguity, the policy text targets (the Common forms bullet), the optional-column order rule in the registry, and the risk-report scale; notes on navigation coverage, the cloud-example paragraph, the Support and Ownership none-line, a raw registry without `common_forms` and the terminal-contract consumer. | no | none |
| EVD-002 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"e8802a7dfd7603906e7ffd95b073cecd3e88638bf25386e2daa3e15b5f80189a","plan_sha256":"df5879f83595fe95ea68633f5df355b151333e8a0e3358027afc55208b24a603"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: round 2 confirmed the round-1 fixes and asked two more (the navigation link count four to one, and a reader that needs no form data: first H2, else first H3); the author applied them and four notes; round 3 confirmed both hashes and that only those edits changed, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0172 approval question naming spec.md e8802a7d and plan.md df5879f8 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0172","SPEC-0172-PLAN-0001"],"reviewed_spec_sha256":"e8802a7dfd7603906e7ffd95b073cecd3e88638bf25386e2daa3e15b5f80189a","reviewed_plan_sha256":"df5879f83595fe95ea68633f5df355b151333e8a0e3358027afc55208b24a603","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-ROOTREADME-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

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
