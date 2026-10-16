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
| WORK-001 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | Workflow rule single ownership | platform | completed | PASS | EVD-002, EVD-015 tests, EVD-007, EVD-016 staged QA, EVD-020 review resolving EVD-011 |
| WORK-002 | [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | CI metadata test rename | platform | completed | PASS | EVD-003 tests, EVD-008 staged QA, EVD-012 review |
| WORK-003 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | Narrowed script and test surfaces | platform | completed | PASS | EVD-004, EVD-017 selection tests, EVD-009, EVD-018 staged QA, EVD-013, EVD-021 review |
| WORK-004 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | Lifecycle module gate | platform | completed | PASS | EVD-005, EVD-019 gate runs, EVD-006 selection tests, EVD-010 staged QA, EVD-022 review resolving EVD-014 |

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
| EVD-011 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff 2e27681d ce429c00`, head `ce429c00251272dc35929789d70356a6b2a62ff5` | FAIL | `request_changes`. MEDIUM: the forbidden live-mutation workflow scan (`kubectl apply`/`patch`, `argocd app sync`/`set`, `vault kv`, `docker push`, `git push`) was removed from `quality.py` with no remaining owner. LOW: labeler concurrency and duplicate step labels are no longer enforced | yes | none |
| EVD-012 | [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff 2e27681d ce429c00`, head `ce429c00251272dc35929789d70356a6b2a62ff5` | PASS | The deleted cases are covered by `validate-ci-python-contract.py`, and behavior tests are kept; the reviewer reran `test_ci_branch_metadata` 2 and `test_validate_ci_python_contract` 77 OK | yes | none |
| EVD-013 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff 2e27681d ce429c00`, head `ce429c00251272dc35929789d70356a6b2a62ff5` | PASS | Classification is exact (1,357 paths, uncovered 0, ambiguous 0), and unknown scripts and tests stay broad. LOW: the `archive_*.py` and `bounded_io.py` under-selection predates this branch; dropping `agent-governance` from `tests` skips its check that a retired fixture is not recreated; `github-actions-security` was not selected by its own inputs | yes | none |
| EVD-014 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff 2e27681d ce429c00`, head `ce429c00251272dc35929789d70356a6b2a62ff5` | FAIL | `request_changes`. The gate is registered correctly and fails closed on import errors, but it is MEDIUM-not-selected by its direct inputs: the document-reader scripts, the `archive_*.py` modules and three shared test helpers | yes | none |
| EVD-015 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests and validators | Commit `5f00157a`: the live-mutation scan moved to `validate-github-actions-security.py` | PASS | Two new fixture cases (`kubectl apply`, `git push`) failed first and pass after. The scan uses the same seven tokens over every workflow. `test_validate_github_actions_security` 5 OK; the validator passes on the repository | yes | none |
| EVD-016 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Selected staged QA | Commit `5f00157a` by the delegated `quality-engineer` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed (agent-reported) | yes | none |
| EVD-017 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selection tests and classification | Commit `060d6346`: `document-reader-implementation` and `archive-scripts` select `document-contract-tests`; `archive-scripts` also selects `document-lifecycle` and `links-and-owners`; three lifecycle helpers move to `shared-document-history-readers`; the actions security script, test and fixture move to `ci-metadata-contract`, which now selects `github-actions-security` | PASS | 26 subtests failed first and pass after. `test_validate_affected_surfaces` 25, `test_document_scope_selection` 21, `test_archive_registry_contract` 17, `test_validation_profiles` 17, `test_affected_surface_migration` 16 and `test_validation_tooling_ownership` 16, all OK. Classification: 1,357 paths, uncovered 0, ambiguous 0 | yes | none |
| EVD-018 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selected staged QA | Commit `060d6346` by the delegated `quality-engineer` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed (agent-reported) | yes | none |
| EVD-019 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Lifecycle module gate run | `python scripts/run-document-contract-tests.py --root .` at head `060d6346` | PASS | `[PASS] document contract regressions passed: modules=4 tests=91`, rc 0 | yes | none |
| EVD-020 | [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff ce429c00 060d6346`, head `060d634674146e4c4388e752ede5631e7ae3ead5` | PASS | `approve`: the live-mutation tokens match the removed scan and apply to every workflow. LOW: only two of the seven tokens have a fixture case | yes | EVD-011 |
| EVD-021 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff ce429c00 060d6346`, head `060d634674146e4c4388e752ede5631e7ae3ead5` | PASS | `approve`: the new routes are exclusive and the catch-alls exclude them. The reviewer reran classification and 51 focused tests, all OK | yes | none |
| EVD-022 | [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff ce429c00 060d6346`, head `060d634674146e4c4388e752ede5631e7ae3ead5` | PASS | `approve`: the gate is now selected by the document readers, the `archive_*.py` modules and the three shared helpers | yes | EVD-014 |
| EVD-023 | [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | WORK-003 | QA runner tests | `python -m unittest tests.test_qa_runner` in the branch worktree, run while the review fixes were being written | PASS | `Ran 38 tests in 551.690s`, OK. This is supporting evidence only, because the run overlapped the fix commits | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-QP2-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-002, EVD-007, EVD-011, EVD-015, EVD-016, EVD-020 | Each workflow rule has one owner in the actions security validator; EVD-011 is resolved by EVD-020 | platform |
| [VAL-QP2-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-003, EVD-008, EVD-012 | CI metadata test renamed with its behavior tests kept | platform |
| [VAL-QP2-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-004, EVD-009, EVD-013, EVD-017, EVD-018, EVD-021, EVD-023 | Narrowed surfaces classify every path once and select the gates that read them | platform |
| [VAL-QP2-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-001, EVD-005, EVD-006, EVD-010, EVD-014, EVD-019, EVD-022 | Lifecycle modules run on their inputs; EVD-001 is resolved by EVD-005 and EVD-014 by EVD-022 | platform |

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

All four criteria are accepted. Workflow pinning, permissions, `timeout-minutes`
and the live-mutation command scan now have one owner,
`validate-github-actions-security.py` (VAL-QP2-001). The CI metadata test has
a current name and keeps its behavior tests (VAL-QP2-002). Script and test
surfaces select only the gates that read them, cluster scripts now select their
own validators, and every tracked path classifies once (VAL-QP2-003).
`document-contract-tests` runs the four lifecycle modules when their inputs
change (VAL-QP2-004). The first independent review requested changes; its two
MEDIUM findings were fixed, and a second review approved the fix commits.

Residual risk:
- Workflow-level `concurrency` and duplicate step labels are no longer checked.
- Dropping `agent-governance` from `tests` skips its check that a retired
  fixture is not recreated.
- `bounded_io.py` and `json_schema_validation.py` still under-select their
  importers; this predates the branch.
- Only two of the seven live-mutation tokens have a fixture case.
- `test_run_validation_lane` has a timing-sensitive case that fails under load.
- Actions security inputs also select `ci-python-contract`.
- 63 test modules still have no gate; that is a separate Spec.

Next owner: platform.
