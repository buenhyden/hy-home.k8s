---
title: "W03 Remove the Layer Frontmatter Key"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0184-TSK-0001"
parent_ids: ["SPEC-0184-PLAN-0001"]
---

# Task: W03 Remove the Layer Frontmatter Key

## Overview

This Task records handoff W03-H25, the removal of the frontmatter `layer` key from documents other than accepted ADRs, for [SPEC-0184](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-remove-layer-key` from `8e23dc1f` (the SPEC-0183 closure; PR #248 open), stacked on that PR and checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D22 and W03-H25.
- **Decision recorded with this package:** W03-D32, a one-use exemption in the package-exit check and the published Stage 90 rewrite check for the `layer` line only; user answer "One-use exemption (Recommended)" on 2026-11-13 to the freeze-gate question.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | Gate exemptions, `FM-LAYER-ADR`, registry, documents, templates, tests and fixtures. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | Policy texts; open-package evidence rows; regression and exact-index QA; exemption retirement in the final source commit. | platform | in-progress | PASS | EVD-005, EVD-006, EVD-007, EVD-009 (resolves EVD-008), EVD-010 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over spec.md `3a8bcf66…` and plan.md `b8246699…`; 2026-11-13 | FAIL | REJECT: BLOCK R4 of the package-exit check refuses the `layer` edit on SPEC-0161; BLOCK the registry refuses rewriting published Stage 90 members; BLOCK `TEMPLATE_OMITTED_KEYS` must keep `layer`; FIXes F1 to F5 on the drafts. The decision W03-D32 (a one-use exemption) followed. | no | none |
| EVD-002 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"9d029adc9cb773357d5e1a99fe61163c37b4ceb980d9150d0ca9aa5c81b27185","plan_sha256":"a82ae68957145fe85e7dbdb962acb4fd79973401e9f744757da04b6e435e7f20"} | PASS | Same reviewer: round 2 APPROVE with FIX-1 to FIX-3 over spec.md `76eda90e…` and plan.md `03e4492d…`; round 3 APPROVE over spec.md `d6152191…` and plan.md `6fefd7cc…`. The author then applied the three wording NITs of round 3 (closure changed to final source commit; the SPEC-0161 version and updated exception added to the scope; a duplicate anchor clause removed), giving the bytes named here. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0184 approval question naming spec.md 9d029adc and plan.md a82ae689 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0184","SPEC-0184-PLAN-0001"],"reviewed_spec_sha256":"9d029adc9cb773357d5e1a99fe61163c37b4ceb980d9150d0ca9aa5c81b27185","reviewed_plan_sha256":"a82ae68957145fe85e7dbdb962acb4fd79973401e9f744757da04b6e435e7f20","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | One-use exemptions, `FM-LAYER-ADR`, registry and `layer` removal, red then green | Working tree over `aaca5a9c`; implementer quality-engineer subagent, staged and re-checked by the author; 2026-11-13 | PASS | Red: 2 exemption tests failed (published rewrite, R4) before the code, and 11 key-contract tests before the profile change. Green: 15 exemption tests and 50 key-contract tests pass. Both exemptions allow only deleting the whole frontmatter `layer` line; a blanked line, a value edit, a deletion with a body or `version` edit (R4), another deleted key and a body `layer` line stay refused. `FM-LAYER-ADR` refuses `layer` on a proposed, rejected, superseded or deprecated ADR; an accepted ADR passes with or without it; other profiles refuse it through `FM-KEYSET`; `TEMPLATE_OMITTED_KEYS` keeps `layer`. 79 files lost their `layer` line (82 named in the Spec less SPEC-0181's three, which left the tree); `git grep -n '^layer: '` lists only the 34 accepted ADRs. Deviations: the exemptions allow deletion only, tighter than the Spec's set-aside comparison; the document authoring sentence was at line about 68; the Stage 99 README drops the `layer` table row and names the ADR exception in its paragraph. | yes | none |
| EVD-005 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Policy texts and open-package metadata edits | Staged diff over `3ae0b2c3` | PASS | `document-authoring.md`, `document-lifecycle.md`, `docs/90.references/AGENTS.md` and `docs/99.templates/README.md` name the accepted-ADR exception and the one-use exemption until this package retires it. Open-package Spec and Plan changed by their `layer` line only (sha256 prefixes): SPEC-0161 spec `5b304a9dfdc19075`→`698da2d295ae2d6b`, plan `e388f9e724ba5bea`→`7395a09a86e2e4e6`; SPEC-0184 spec `9d029adc9cb77335`→`01b56ac77a2d40e1`, plan `a82ae68957145fe8`→`ad2a933afd65cec6`; metadata only, no scope change (W03-D22); the first-record receipt above names the bytes as approved before this edit. | yes | none |
| EVD-006 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Implementer runs in a staged scratch clone, then the author's staged checks, 2026-11-13 | PASS | The four strict document validators match the before run at `aaca5a9c`; the staged lifecycle check passes with both exemptions on the real SPEC-0161 and Stage 90 edits. Suites: `document` 668, `document-lifecycle` 25, `agent-governance` 105, `validation-routing` 173, `tooling` 166 OK; `quality.py` PASS; `ruff check` and `ruff format --check` clean; markdownlint 0 issues over the 82 edited Markdown files; `graphify update .` done. `.secrets.baseline` moved 12 shifted lines in `3ae0b2c3`. | yes | none |
| EVD-007 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 94 files over `3ae0b2c3` | PASS | Risk class `medium`. Checklist: no accepted ADR changed; frozen records changed by the `layer` line only; the exemptions are retired in this package's final source commit; no body text beyond the named policy sentences changed; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow file changed. | yes | none |
| EVD-008 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index `python3 scripts/qa.py staged` | Index tree `7d9a731c` over `3ae0b2c3` (94 staged paths); system interpreter `/usr/bin/python3` 3.12 first on `PATH`; 2026-11-13 | FAIL | exit 1: `agent-governance` and `document-contract-tests` (27 loader errors) failed on import, `ModuleNotFoundError: No module named 'ruamel'`. Cause: the interpreter lacked the hashed-lock `ruamel-yaml==0.19.1` that SPEC-0183's loader needs; it was not the pinned environment `hyhome.validationVenv` that `.agents/governance/git.md` names for staged QA and the hooks. No repository defect; no code, check or baseline changed. | yes | none |
| EVD-009 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index `python3 scripts/qa.py staged` | Final index of the implementation commit (tree `7d9a731c` plus these two rows); pinned validation environment `$HOME/.venvs/hyhome-validation/bin` first on `PATH` (`ruamel.yaml` 0.19.1); 2026-11-13 | PASS | exit 0; 12 lanes PASS, none failed or skipped. | yes | EVD-008 |
| EVD-010 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | WORK-002 | One-use exemption retirement, final source commit | Working tree over `c3196040`; pinned validation environment; 2026-11-13 | PASS | `git grep -n '^layer: '` outside accepted ADRs is empty, so the exemptions had no remaining use. `scripts/document_lifecycle.py`, `tests/test_document_lifecycle_package_exit.py`, `tests/test_reference_pack_routes.py`, `.agents/governance/document-lifecycle.md` and `docs/90.references/AGENTS.md` are restored to their `aaca5a9c` bytes; `scripts/validate-document-contract-registry.py` loses the exemption and keeps only the `TEMPLATE_OMITTED_KEYS` comment; `git grep W03-D32` outside Stage 03 is empty. The two removed exemption tests, run once against the retired code, fail on their layer-only case: R4 refuses `docs/03.specs/0042-sample-change/spec.md` and `REFERENCE_PUBLISHED_REWRITE` refuses the published example member, so both gates refuse a `layer`-only change again. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D32 row, evidence rows and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: the 34 accepted ADRs, `.github/workflows/`, document body text other than the named policy sentences, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance`, `ci-metadata`, `validation-routing` and `tooling` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); exact-index QA failed with the system interpreter, which lacks `ruamel.yaml` (EVD-008), and passed in the pinned validation environment (EVD-009); the final source commit retires both exemptions and both gates refuse a `layer`-only change again (EVD-010); criterion acceptance pending. Risk class `medium`.
