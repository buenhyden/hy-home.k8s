---
title: "Local QA Phase Two Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0118-TSK-0001"
parent_ids: ["SPEC-0118-PLAN-0001"]
---

# Task: Local QA Phase Two Execution

## Overview

Execute [SPEC-0118](../spec.md) through [WORK-001–004](../plan.md#work-breakdown):
a single owner for each workflow rule, a correctly named CI metadata test,
narrowed script and test surfaces, and a gate for the lifecycle modules.

## Inputs

- The operator's 2026-10-16 instruction to proceed as recommended with phase
  two. The recommended defaults are: keep `agent-governance` on its current
  surfaces, and leave the other unrun modules to a separate Spec.
- Start: main `2e27681d` (PR #158 merge; first drafted on `ad3e187f`), branch `refactor/spec-0118-qa-phase-two` in a
  separate worktree.
- The read-only phase-two scoping report of the same date.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | Workflow rule single ownership | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | CI metadata test rename | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | Narrowed script and test surfaces | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | Lifecycle module gate | platform | in-progress | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Lifecycle module gate run | `scripts/run-document-contract-tests.py` on this branch | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests and validators | Commit `1ff0ca46`: `validate-github-actions-security.py`, `quality.py`, their tests and fixture | PASS | New `missing-timeout` fixture case failed first and passes after `timeout-minutes` moved to the actions security validator for every job; `test_validate_github_actions_security` 5 OK, `test_repository_quality_rules` 10 OK; both validators PASS on the repository. Removed from `quality.py`: duplicate step labels, forbidden-command scan, labeler-only concurrency, `needs.*.result` and the old timeout rule; removed the `.github/zizmor.yml` guard for a file that does not exist. Remaining owners: `validate-ci-python-contract.py` forbids `needs` on `ci-summary`; all three workflows still declare `concurrency` | yes | none |
| EVD-003 | [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests | Commit `d08208df`: `tests/test_ci_branch_metadata.py` (renamed from `test_ci_qa_workflow.py`), new `tests/test_validate_k8s_manifests.py`, registry and selection test references | PASS | The PR event-type test and the checkout step-shape asserts were removed, because `test_validate_ci_python_contract` (77 OK) owns those shapes. The branch-policy behavior test and the behavioral half of the PR-title and commit-range test were kept, because nothing else executes those inline scripts. The k8s manifest roots test moved. `test_ci_branch_metadata` 2 OK, `test_validate_k8s_manifests` 1 OK, `test_validate_affected_surfaces` 21 OK | yes | none |
| EVD-004 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selection tests and classification | Commit `eec2559a`: `registry.json`, `tests/fixtures/validation-surfaces.json`, `tests/test_validate_affected_surfaces.py` | PASS | Seven surface cases, five selection cases and `test_narrowed_script_surfaces_do_not_select_unrelated_gates` failed first. They pass after adding `cluster-gate-scripts`, `archive-scripts` and `tooling-scripts` and narrowing `tests` to `archive-contract-tests` and `repository-quality`. Cluster scripts now select `gitops-change-set`, `vault-eso-contracts` and `platform-assurance`. `select-affected-surfaces.py`, `run-validation-lane.py`, `validate-selected-style.py`, `bounded_io.py` and `registry.schema.json` stay on `scripts`, because shared consumers read them. `validate-affected-surfaces.py --root .` PASS with 1,357 paths, uncovered 0 and ambiguous 0; `classify_path` classified all 1,356 tracked paths. Tests: `test_validate_affected_surfaces` 22, `test_document_scope_selection` 21, `test_archive_registry_contract` 17, `test_validation_profiles` 17, `test_affected_surface_migration` 16 and `test_validation_tooling_ownership` 16, all OK | yes | none |
| EVD-005 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Lifecycle module gate run | Commit `d72363e5`: `scripts/run-document-contract-tests.py` and `scripts/run-archive-contract-tests.py` | PASS | Document runner PASS with 4 modules and 91 tests in 174 s serial. Archive runner PASS with 7 modules (now including `test_generic_migration_recovery`) and 183 tests in 87 s | yes | EVD-001 |
| EVD-006 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Selection tests and triage | Commit `d72363e5`: `document-contract-tests` validator (affected and staged lanes, quick and staged profiles, timeout 900 s) on `shared-document-history-readers`, `stage99-machine-contracts` and `template-documents` | PASS | 13 subtests of `test_document_contract_tests_follow_their_real_inputs` and the fixture cases failed first and pass after. `test_validate_affected_surfaces` 23 OK and `test_document_scope_selection` 21 OK; the registry tests are unchanged and OK. `test_run_validation_lane` `test_escaping_descendant_identity_is_reported` passed 3 of 3 serially and failed 3 of 4 under 36 busy loops, so it is timing-sensitive under load, not a defect | yes | none |
| EVD-007 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Selected staged QA | Commit `1ff0ca46` by the delegated `quality-engineer` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed (agent-reported; no `--no-verify`) | yes | none |
| EVD-008 | [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Commit `d08208df` by the delegated `quality-engineer` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed (agent-reported; no `--no-verify`) | yes | none |
| EVD-009 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selected staged QA | Commit `eec2559a` by the delegated `quality-engineer` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed (agent-reported; no `--no-verify`) | yes | none |
| EVD-010 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Selected staged QA | Commit `d72363e5` by the delegated `quality-engineer` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed (agent-reported; no `--no-verify`) | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | pending | none | Validator and test change remains | platform |
| [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | pending | none | Test rename remains | platform |
| [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | pending | none | Registry change remains | platform |
| [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | pending | none | Gate registration remains | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0118-qa-phase-two/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/validation/**`, `scripts/validate-github-actions-security.py`,
  `scripts/validate-affected-surfaces.py`, `scripts/run-archive-contract-tests.py`,
  `scripts/run-document-contract-tests.py`, `scripts/README.md`, `tests/**`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**: The operator's "proceed as recommended" is recorded
  as approval of SPEC-0118 and its Plan as written on 2026-10-16. The operator
  may revoke or amend it. Push, pull request and merge follow RUN-0013.
- **Static Validation**: Focused tests, Ruff and `qa.py staged` on the exact
  index.
- **Live Validation**: None.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

Pending.
