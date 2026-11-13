---
title: "W03 Registry Schema Version Mapping"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0207-TSK-0001"
parent_ids: ["SPEC-0207-PLAN-0001"]
---

# Task: W03 Registry Schema Version Mapping

## Overview

This Task records the Registry Schema Version package (W03-D65, fourth resolution; REQ:862 and REQ:890): the survey of every reader of `schema_version`, the history of the integer generations, the meaning-preserving mapping to a SemVer value, the choice of the current version and the four-level bump rule, for [SPEC-0207](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-14 (Asia/Seoul) the user decided W03-D65 ("`W03 프롬프트에 작성된대로`") and asked for this package to be drafted. The request approves no Spec bytes or criterion; an approval of push, PR or merge is recorded here when the user gives it.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `81096a83` (after PR #255, SPEC-0189) and are checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D45, W03-D46, W03-D52, W03-D63 (superseded by W03-D66 for the version), W03-D65 (recorded by SPEC-0193) and W03-D69 (the retained ADR bound).
- **Decision recorded with this package:** W03-D66 (a SemVer string; generation 10 is `10.0.0` and this package's change is MAJOR so the registry lands at `11.0.0`; an additive optional key is MINOR only when every consumer tolerates it; Stage 99 registry only, other integer versions handed to W01, W05 and the SPEC-0191 owner; its own ADR; landing right after SPEC-0191) and W03-D69 (the retained accepted-ADR list becomes ADR-0001 to ADR-0061, so this package's ADR is ADR-0061 in the ADR form of its day and SPEC-0198's becomes ADR-0062); user answers of 2026-11-14.
- **Merge order:** right after SPEC-0191 and before SPEC-0192 and every later package (W03-D66); each later registry change applies its own bump at its implementation commit and records the level and reason in its Task; SPEC-0205 is revised by its drafter before its approval.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REGVER-001](../spec.md#success-criteria--verification-plan) | `registry_schema_version`, the registry value and schema property, the loader, the strict check, `registry_at`, the write guard and the tests that pin them, with the new test module registered. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-REGVER-002](../spec.md#success-criteria--verification-plan) | The glossary row, the version paragraph, the amending ADR, the SPEC-0161 Task evidence row and ledger closure, the end condition of the transitional branch, regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-REGVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval reader and history survey | `main` `81096a83`; `git log -S` and `git log -G` over `docs/99.templates/registry.json` and its predecessor `docs/99.templates/support/document-profiles.json`; `grep -rn "schema_version"` over `scripts`, `tests`, `docs/99.templates` and the other registries | PASS | The Spec tables hold the ten generations, the three runtime pins, the three pinning tests and the five other integer versions. This row records a survey, not a review or an approval. | no | none |
| EVD-002 | [VAL-REGVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"8f98be522ab33833a2291caca83f1e6b8dd265e463a1aab201deb9e89764ed7b","plan_sha256":"3c61496e8d76a2907167ccaa8d91ff787f7d0a81d1b3246a12adc796b78b0a67"} | PASS | Independent review, three rounds on 2026-11-14 (W03-D65, W03-D66 and W03-D69 revisions): every FIX and NIT item applied and confirmed over the bytes named here; APPROVE. This row records a review, not an approval. | yes | none |
| EVD-003 | [VAL-REGVER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all four to the SPEC-0193, SPEC-0196, SPEC-0198 and SPEC-0207 approval question naming spec.md 8f98be52 and plan.md 3c61496e dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0207","SPEC-0207-PLAN-0001"],"reviewed_spec_sha256":"8f98be522ab33833a2291caca83f1e6b8dd265e463a1aab201deb9e89764ed7b","reviewed_plan_sha256":"3c61496e8d76a2907167ccaa8d91ff787f7d0a81d1b3246a12adc796b78b0a67","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-REGVER-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-REGVER-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json` (the `schema_version` value), `docs/99.templates/contracts/document-profile.schema.json` (that property), `scripts/document_authority.py`, `scripts/document_contracts.py`, `scripts/validate-document-lifecycle.py`, `scripts/provider_write_guard.py`, `tests/test_common_form_tree.py`, `tests/test_k8s_pre_edit_hook.py`, `tests/test_document_lifecycle_cumulative_history.py`, `tests/test_registry_schema_version.py`, `scripts/run-contract-tests.py`, `scripts/validation/registry.json`, the Registry Schema Version row of `.agents/knowledge/glossary.md`, the version paragraph of `.agents/governance/document-authoring.md`, one amending ADR, ADR-0061 (W03-D69), and its Stage 02 README row), this package, `docs/03.specs/README.md`, the W03-D66 and W03-D69 rows, the evidence row, the ledger closure and the frontmatter `version` and `updated` of the SPEC-0161 Task, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any profile, form, template, section list, body contract or lifecycle domain, the integer versions of other files, any accepted ADR body, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `python3 scripts/validate-document-contract-registry.py --root .`, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit, which restores the integer in every reader together; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed in three rounds and first-recorded (EVD-002/003); implementation not started.
