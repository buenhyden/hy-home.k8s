---
title: "Local QA Rightsizing Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0117-TSK-0001"
parent_ids: ["SPEC-0117-PLAN-0001"]
---

# Task: Local QA Rightsizing Execution

## Overview

Execute [SPEC-0117](../spec.md) through [WORK-001–005](../plan.md#work-breakdown):
repair failing tests and remove over-applied, duplicated, conflicting and
stale local checks found by the 2026-10-16 audit.

## Inputs

- The operator's 2026-10-16 request to review the local full test surface for
  over-applied, duplicated, conflicting or stale checks and to fix them; the
  operator chose to start with phase one.
- Start: main `f062294c` (PR #155 merge), branch
  `refactor/spec-0117-local-qa-rightsizing` (renamed from
  `qa/spec-0117-local-qa-rightsizing` after PR #156 failed the hosted
  branch-prefix policy).
- A per-module test timing run on `main` in the session scratch directory.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | Repair the three failing test modules | platform | completed | PASS | EVD-010 tests resolving EVD-001 and EVD-002, EVD-011 staged QA, EVD-012 review |
| WORK-002 | [VAL-QR-002](../spec.md#success-criteria--verification-plan) | CI Python contract consistency checks | platform | completed | PASS | EVD-003 tests and validator, EVD-007 staged QA, EVD-013 review |
| WORK-003 | [VAL-QR-003](../spec.md#success-criteria--verification-plan) | Ingress validator without chart versions | platform | completed | PASS | EVD-004 tests and validator, EVD-008 staged QA, EVD-014 review |
| WORK-004 | [VAL-QR-004](../spec.md#success-criteria--verification-plan) | Quality and registry cleanup | platform | completed | PASS | EVD-005 tests and quick QA, EVD-009 staged QA, EVD-015 review |
| WORK-005 | [VAL-QR-005](../spec.md#success-criteria--verification-plan) | Delivery procedure and README alignment | platform | completed | PASS | EVD-006 staged QA, EVD-016 review |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Per-module test timing | Every `tests/test_*.py` module on main `f062294c`, run one module at a time with the pinned validation environment | FAIL | `test_completed_state_migration` (3 failures), `test_generic_migration_recovery` (1 error) and `test_document_lifecycle_cumulative_history` (5 failures) fail on `main` | yes | none |
| EVD-002 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Per-module test timing | Same run completed: 76 modules, 1,503 tests, 1,880.8 s serial on main `f062294c` | FAIL | A fourth module, `test_task_execution_contract` (3 failures, 9 errors), also fails. Slowest modules: `test_qa_runner` 492 s, `test_archive_validation` 481 s, `test_documentation_link_boundary` 297 s | yes | none |
| EVD-003 | [VAL-QR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and validator | `scripts/validate-ci-python-contract.py`, `tests/test_validate_ci_python_contract.py` at commit `9daa4edc` | PASS | New bump tests (consistent `.in`/lock bump, pre-commit rev and tag bump, action SHA bump) failed before the change and pass after; `Ran 77 tests ... OK`; validator on the repository `[PASS] ... hosted-installs=1`; Ruff check and format clean. Removed `EXPECTED_PINS`, `EXPECTED_RESOLVED_PINS`, `EXPECTED_PRE_COMMIT_REVISIONS`, `EXPECTED_PRE_COMMIT_SOURCE_TAGS`, `CHECKOUT_ACTION`, `SETUP_PYTHON_ACTION`; malformed pins, missing hashes, short revs, missing frozen comments, `.in`/lock disagreement and tag or mixed action refs still fail. No longer caught here: a dropped transitive lock entry or a changed lock version or hash, which the `--require-hashes` install and lock regeneration own. Net -118 lines | yes | none |
| EVD-004 | [VAL-QR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Focused tests and validator | `scripts/validation/platform/ingress.py`, `tests/test_platform_ingress.py` at commit `9487c7ec` | PASS | `test_chart_version_bump_is_not_pinned` failed first (4 subtests) and passes after the version argument was removed; `test_wrong_chart_repo_or_namespace_fails` keeps repository, chart and namespace drift failing; `Ran 12 tests ... OK`; `scripts/validation/platform/assurance.py --root .` reported `product-semantic` PASS for every target; Ruff clean. The Application manifest owns the chart version | yes | none |
| EVD-005 | [VAL-QR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused tests and quick QA | `quality.py`, `registry.json`, `registry.schema.json`, `validate-affected-surfaces.py`, `tests/fixtures/validation-surfaces.json` at commit `091a0afe` | PASS | Removed prose phrase lists (PR template, `docs/README.md`, `ci-summary` and secret-scan internals, sample ExternalSecret), retired path and phrase denylists, the CODEOWNERS requirement, the `traefik` surface, the `vault-external.yaml` route and the unused `inventory` and `ci` evidence lanes; security-relevant workflow checks, LAN pins (separate Spec) and policy-named lanes were kept. Six focused modules OK (`test_validate_affected_surfaces` 21, `test_run_validation_lane` 90, `test_repository_quality_rules` 10, `test_validation_tooling_ownership` 16, `test_current_executable_references` 12, `test_archive_registry_contract` 17); `qa.py quick` 16 gates PASS; Ruff clean. Net about -339 lines. `test_qa_runner` was not run | yes | none |
| EVD-006 | [VAL-QR-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Selected staged QA | Commit `fdc58e81`: `quality.md`, `git.md`, `repository-surface.md`, `README.md` | PASS | Delivery sequence names `independent-review` from review App `5341483` through RUN-0013 and merge on all three checks; README `.github/` lines list the actual contents. Staged QA passed document-contract, lifecycle, links-and-owners, markdown-profiles, repository-quality and selected style gates; markdownlint passed | yes | none |
| EVD-007 | [VAL-QR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Commit `9daa4edc` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-008 | [VAL-QR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selected staged QA | Commit `9487c7ec` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-009 | [VAL-QR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Selected staged QA | Commit `091a0afe` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-010 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Per-module test timing | Commit `d49e9585`: fixture alignment in `test_completed_state_migration`, `test_generic_migration_recovery`, `test_document_lifecycle_cumulative_history`; `document_contracts.py` reads `korean_allowed_markdown_roots` with `.get` for older committed registries; `document_lifecycle.py` and `validate-document-lifecycle.py` skip the new-work `PLAN-PROMOTION` and `TASK-PARENT-APPROVAL` guards only for paths admitted at a 9 -> 10 generation boundary whose bytes are unchanged | PASS | Nine modules OK: `test_task_execution_contract` 40, `test_completed_state_migration` 6, `test_generic_migration_recovery` 42, `test_document_lifecycle_cumulative_history` 28, `test_document_language` 35, `test_task_acceptance_contract` 17, `test_document_lifecycle_migration` 24, `test_document_lifecycle_archive_cutover` 36, `test_archive_disposition_lifecycle` 46. New `test_plan_edited_after_generation_boundary_keeps_new_work_guards` shows an edited Plan still fails `PLAN-PROMOTION`. Causes: commits `6327c3d3`, `5d0d9aef`, `55cd3415` and `92849f15` changed contracts without running these modules, which no registered lane executes | yes | EVD-001, EVD-002 |
| EVD-011 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Selected staged QA | Commit `d49e9585` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-012 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff f062294c cbd370b4`, head `cbd370b46c55c1f6d095035fbc20d4683757e5c3` | PASS | `approve`, no critical, high or medium finding; the reviewer reran eight focused modules OK. Lifecycle exemption admits only real 9 -> 10 boundary paths with unchanged bytes; an edited Plan keeps the guards. LOW: misleading `ready` variable in the copied-Task test and a missing safety comment on the `compare_lifecycle` filter, both fixed in `5547da76` | yes | none |
| EVD-013 | [VAL-QR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff f062294c cbd370b4`, head `cbd370b46c55c1f6d095035fbc20d4683757e5c3` | PASS | `approve`, no critical, high or medium finding; the reviewer reran eight focused modules OK. Remaining owners confirmed: `validate-github-actions-security.py` for SHA-pinned actions, the `--require-hashes` install from the trusted-base lock and the trusted-base pre-commit config in hosted `style-pr`. LOW: a PR may now add a hook repository with any full rev and frozen comment and pass locally; recorded as residual risk | yes | none |
| EVD-014 | [VAL-QR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff f062294c cbd370b4`, head `cbd370b46c55c1f6d095035fbc20d4683757e5c3` | PASS | `approve`, no critical, high or medium finding; the reviewer reran eight focused modules OK. Repository, chart, release, namespace and server checks remain | yes | none |
| EVD-015 | [VAL-QR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff f062294c cbd370b4`, head `cbd370b46c55c1f6d095035fbc20d4683757e5c3` | PASS | `approve`, no critical, high or medium finding; the reviewer reran eight focused modules OK. Removed items had no current consumer or were prose checks; workflow permission and secret checks were untouched | yes | none |
| EVD-016 | [VAL-QR-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff f062294c cbd370b4`, head `cbd370b46c55c1f6d095035fbc20d4683757e5c3` | PASS | `approve`, no critical, high or medium finding; the reviewer reran eight focused modules OK. Claims match the repository. LOW: `.github/repository-surface.md` still described fixed pin checks; fixed in `5547da76` | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-QR-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-001, EVD-002, EVD-010, EVD-011, EVD-012 | Four failing modules repaired at their root; EVD-001 and EVD-002 are resolved by EVD-010 | platform |
| [VAL-QR-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-003, EVD-007, EVD-013 | Copied pins replaced by consistency checks; the local hook-repository residual is stated in the Verification Summary | platform |
| [VAL-QR-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-004, EVD-008, EVD-014 | Chart versions are owned by the Application manifests | platform |
| [VAL-QR-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-009, EVD-015 | Prose, retired, CODEOWNERS, dead-surface and unused-lane checks removed with owners named | platform |
| [VAL-QR-005](../spec.md#success-criteria--verification-plan) | accepted | EVD-006, EVD-016 | Delivery procedure names all three required checks | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0117-local-qa-rightsizing/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/validate-ci-python-contract.py`, `scripts/validation/**`,
  `scripts/validate-affected-surfaces.py` (its lane constants mirror the
  registry schema), `scripts/document_contracts.py`,
  `scripts/document_lifecycle.py`,
  `tests/**`, `.agents/governance/quality.md`, `.agents/governance/git.md`,
  `.github/repository-surface.md`, `.github/CODEOWNERS`, `README.md`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**: The operator's request ("review, analyze, fix,
  supplement and improve") and the phase-one choice are recorded as approval
  of SPEC-0117 and its Plan as written on 2026-10-16; the operator may revoke
  or amend it. Push, pull request and merge follow RUN-0013.
- **Static Validation**: Focused tests, Ruff and `qa.py staged` on the exact
  index.
- **Live Validation**: None.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

All five criteria are accepted. Four focused modules that failed on `main`
now pass with their root causes repaired (VAL-QR-001). The CI Python contract
checks pin consistency instead of copied values (VAL-QR-002), the ingress
validator no longer pins chart versions (VAL-QR-003), and repository quality
and the registry lost prose, retired-path, CODEOWNERS, dead-surface and
unused-lane checks (VAL-QR-004). The delivery procedure names
`independent-review` (VAL-QR-005). Each commit passed staged QA and the branch
passed an independent review whose four LOW notes were applied or recorded.

Residual risk: a pull request may add a pre-commit hook repository with any
full revision and frozen comment and still pass the local contract; hosted
`style-pr` runs only the trusted-base configuration, so the exposure is a
local run of that pull request's checkout. The four repaired modules belong to
no registered lane, which is how they went unnoticed; selecting them is a
phase-two item. `test_qa_runner` was not rerun. Next owner: platform, for
phase two.
