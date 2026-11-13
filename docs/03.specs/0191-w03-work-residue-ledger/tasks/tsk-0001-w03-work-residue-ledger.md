---
title: "W03 Work Residue Ledger"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0191-TSK-0001"
parent_ids: ["SPEC-0191-PLAN-0001"]
---

# Task: W03 Work Residue Ledger

## Overview

This Task records the second half of handoff W03-H30 (W03-D25): the work residue ledger, its schema, the drift and closure gate, the on-demand view and the seed from current truth, for [SPEC-0191](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 and 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items and approved commit, push, PR and merge for this work. The requests approve no Spec bytes or criterion.
- **Base:** set at commit time (the branch and the `main` commit it starts from); the Spec and Plan were drafted against `main` `8231f782` and are checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D25, W03-D37 to W03-D40 and W03-H30.
- **Decision recorded with this package:** W03-D47 (ledger location, live `Residue Handoff` table, registration in the Stage 99 registry, recognition of residue tables, entries without a Task row, seed scope, refusal of a package exit with open residue, copied-value check, identity, closure row result, script and suite layout); user answer of 2026-11-13 adopting the recommended option of each of the eleven questions.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RESIDUE-001](../spec.md#success-criteria--verification-plan) | Schema, registry block, gate, view, tests, suite row, validator entry, surfaces and carve-outs; the seed that the gate needs to pass (entries, the appended table and the historical registrations). | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-RESIDUE-002](../spec.md#success-criteria--verification-plan) | The seed record per kind and table; the check cells, AD-0006 and policy sentences; regression and exact-index QA; the closure of W03-H30 and `LEDGER` through the ledger cycle. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RESIDUE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | FAIL | APPROVE-WITH-FIX over spec.md `defe25c0…` and plan.md `0e9778a1…`: FIX 1 (the Stage 03 README index row for the ledger is a requirement, because the stage index is declared complete), FIX 2 (the H2 that hosts `Residue Handoff` and the exact first-cell pattern of handoff rows), NIT 1 (adoption entry identities reuse recorded handoff IDs; a copied-value scan case for seeded text) and NIT 2 (merge order with SPEC-0186 to SPEC-0190 and SPEC-0192; W03-D46 to W03-D48 numbering), all applied to the drafts. | no | none |
| EVD-002 | [VAL-RESIDUE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"d24be3f577cdefceb3817f696ed4e90f1b638970ed68bf341d37a19b793e6742","plan_sha256":"c064f0b8fcfa517ac1cc2e98ace759d17b6c24871005be92de2b9f47f452dee0"} | PASS | Same reviewer: the round-1 verdict was APPROVE-WITH-FIX, and FIX 1, FIX 2, NIT 1 and NIT 2 are applied in the bytes named here; round 2 on 2026-11-14 confirmed every FIX resolved and gave APPROVE over these bytes. The approved bytes are the bytes named here; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-RESIDUE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0191 approval question naming spec.md d24be3f5 and plan.md c064f0b8 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0191","SPEC-0191-PLAN-0001"],"reviewed_spec_sha256":"d24be3f577cdefceb3817f696ed4e90f1b638970ed68bf341d37a19b793e6742","reviewed_plan_sha256":"c064f0b8fcfa517ac1cc2e98ace759d17b6c24871005be92de2b9f47f452dee0","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RESIDUE-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-RESIDUE-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (the ledger and its schema, the `work_residue` registry block and its registry-schema property, the gate and view scripts, the test module and its suite row, the validation registry entries with their routing fixture and tests, the Task template prompt, the work lifecycle and Stage 03 `AGENTS.md` sentences, the README entries, the REQ-0003 check cells and the AD-0006 sentence), this package, `docs/03.specs/README.md`, in the SPEC-0161 Task the W03-D47 row, the appended `Residue Handoff` table with the `State` and `Closure` cells of its rows, appended evidence rows and the frontmatter `version` and `updated`, `.secrets.baseline` (this Task's reviewed digests and lines moved by the registry edit only)
- **Forbidden Paths**: any Stage 90 document, any recorded Task row, EVD row, decision or handoff rewrite including the legacy handoff and conflict tables, any accepted ADR, a committed view, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's requests in Inputs
- **Static Validation**: strict document validators, the `work-residue-ledger` gate, `python3 scripts/validate-affected-surfaces.py --root .`, the `document`, `document-lifecycle`, `validation-routing` and `tooling` suites, the quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
