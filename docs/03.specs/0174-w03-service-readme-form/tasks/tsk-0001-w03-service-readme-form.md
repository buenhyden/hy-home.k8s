---
title: "W03 Service README Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0174-TSK-0001"
parent_ids: ["SPEC-0174-PLAN-0001"]
---

# Task: W03 Service README Form

## Overview

This Task records the sixth phase-2 package of W03, the Service README form, for [SPEC-0174](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-service-readme-form` from `0f60ce3b` (SPEC-0173 closure, contained in `main` after PR #238 merged as `bfbb1bdf`); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08, W03-D10, W03-D11 and W03-D16; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** on 2026-11-13 the user answered "Service README (Recommended)" to the W03-D16 question of which form the four agent and provider READMEs use; they move with the implementation READMEs to the Service README form, amending W03-D10 for them (W03-D17).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Service README (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[13]); conditional content from `COMMON-ROLE-FORMS`; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinitions, tables, bindings and navigation; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | 21 documents and two templates moved with the map; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `224d5334…`, plan.md `5fc062ab…`; 2026-11-13 | FAIL | REJECT: BLOCK `tests/test_repository_quality_rules.py` mutates the `Example Role Matrix` heading by an H2-to-H3 pattern and would fail once the matrix is H4, and was not in scope; FIXes on the matrix count (fourteen, including `infrastructure/verify/`), PR #238 being merged, inventories placed by two rules, the old H2 disposition and unplaced headings, the named test changes, and the child-link wording. The reviewer confirmed the form equals roles[13], the navigation rule accepts `Service Role`, and no current table starts with `Command`. | no | none |
| EVD-002 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"7223bfca11e5b4c103871a5e48e15482a3e2f6a7a205dee8096e40792680b9d4","plan_sha256":"f6aba0350835c5fd19312448b9b22a9b03a83882401d8cb9a9db00c14383c6bb"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: round 2 confirmed every round-1 fix against the repository and every heading of the 21 documents and two templates placed by one rule, and asked one fix (the level of `Working Procedure` under Local Workflow); the author applied it; round 3 confirmed both hashes and that only that sentence changed, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0174 approval question naming spec.md 7223bfca and plan.md f6aba035 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0174","SPEC-0174-PLAN-0001"],"reviewed_spec_sha256":"7223bfca11e5b4c103871a5e48e15482a3e2f6a7a205dee8096e40792680b9d4","reviewed_plan_sha256":"f6aba0350835c5fd19312448b9b22a9b03a83882401d8cb9a9db00c14383c6bb","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D17 and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/` other than `repository-surface.md`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed; `secrets/README.md` is a tracked router document and holds no secret value
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003). Implementation not started.
