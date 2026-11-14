---
title: "W03 SemVer Version Tests"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0208-TSK-0001"
parent_ids: ["SPEC-0208-PLAN-0001"]
---

# Task: W03 SemVer Version Tests

## Overview

This Task will record the survey of version-bearing objects, the failing-first and passing results of the downgrade, unchanged, tampered-edition, producer and consumer, and numbering cases, and the criterion decisions for [SPEC-0208](../spec.md) under its [Plan](../plan.md). It is a stub: nothing has run.

## Inputs

- **Request:** the user asked on 2026-11-14 (Asia/Seoul) for the W03 SemVer tests of the task file lines 856 and 898 to be drafted as a package. The request approves no Spec bytes, no criterion and no commit, push or merge.
- **Base:** set at commit time; the Spec was drafted against `main` `81096a83`.
- **Decisions reused:** SPEC-0161 W03-D45 and W03-D46 (SPEC-0190).
- **Decision recorded with this package:** W03-D68 (the four answers of the user, 2026-11-14, each the recommended option), appended to the SPEC-0161 Task with the package commit. Open question: none.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SEMVERTEST-001](../spec.md#success-criteria--verification-plan) | The survey and mapping, the shared `precedence` function and the downgrade, unchanged and tampered-edition comparison. | platform | draft | NOT_RUN | Pending |
| WORK-002 | [VAL-SEMVERTEST-002](../spec.md#success-criteria--verification-plan) | The producer and consumer matrix, the numbering separation case, the policy sentence, the suite row and routes. | platform | draft | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SEMVERTEST-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Version survey rows and situation-to-test mapping | `main` at the base named in Inputs | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-SEMVERTEST-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"59758e5a1cac3b3dc5d589430f0c0b926bc84d8243a08155309b833d7bbe84cd","plan_sha256":"fdf3f7e7e6ca1e5f7445fcad8507e6ea9c914808548ab43bed79103c809a3682"} | PASS | Independent review, two rounds on 2026-11-14 (W03-D67 and W03-D68 drafts): all round-1 and round-2 items applied and confirmed over the bytes named here; APPROVE. This row records a review, not an approval. | yes | none |
| EVD-003 | [VAL-SEMVERTEST-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve both to the SPEC-0208 and SPEC-0209 approval question naming spec.md 59758e5a and plan.md fdf3f7e7 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0208","SPEC-0208-PLAN-0001"],"reviewed_spec_sha256":"59758e5a1cac3b3dc5d589430f0c0b926bc84d8243a08155309b833d7bbe84cd","reviewed_plan_sha256":"fdf3f7e7e6ca1e5f7445fcad8507e6ea9c914808548ab43bed79103c809a3682","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SEMVERTEST-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-SEMVERTEST-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`scripts/semver_grammar.py`, `scripts/release.py`, `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py`, `tests/test_semver_versions.py`, `tests/test_release.py`, `scripts/run-contract-tests.py`, `scripts/validation/registry.json`, the version paragraph of `.agents/governance/document-authoring.md`, the FR-0027 check cell of `docs/01.requirements/0003-workspace-agent-governance-platform.md`), this package, `docs/03.specs/README.md`, `.secrets.baseline` (reviewed digest entries only)
- **Forbidden Paths**: any existing version value, `CHANGELOG.md`, tags, `.agents/governance/document-lifecycle.md` (W04), `.github/workflows/`, `.claude/`, `.codex/`, hooks, writes to `_workspace/`, `docs/98.archive/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; any commit, push, PR or merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `release` and `validation-routing` suites, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Draft; no check has run. Next owner: platform, for the Spec and Plan approval.
