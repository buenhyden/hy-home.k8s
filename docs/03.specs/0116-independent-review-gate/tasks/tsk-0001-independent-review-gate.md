---
title: "Independent Review Merge Gate Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0116-TSK-0001"
parent_ids: ["SPEC-0116-PLAN-0001"]
---

# Task: Independent Review Merge Gate Execution

## Overview

Execute [SPEC-0116](../spec.md) through [WORK-001–004](../plan.md#work-breakdown):
a local publisher, its runbook, the operator-created review App and the
required `independent-review` check on `main`. Completion closes the PR-edited
workflow forgery path behind SPEC-0115 Task 0005 EVD-012.

## Inputs

- The operator's 2026-10-16 request: research a resolution for EVD-012, write
  its Spec and proceed. A follow-up instruction excluded any AI model API. The
  operator then chose the review App and check-run route over a second
  machine-user account.
- Start: main `26508fe2fd5ba6fc4daaaec2fe7a883a2d8d102d` (PR #151 merge),
  branch `codex/evd-012-independent-review`.
- Research (EVD-001) and the retired SPEC-0107 `qa-provenance` design, which
  bound a check to verifier App `5156553` and was retired with hosted QA, not
  for a defect.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | Publisher script and focused tests | platform | completed | PASS | EVD-009 and EVD-018 tests, EVD-007 staged QA, EVD-005 review resolved by EVD-006 |
| WORK-002 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | RUN-0013 and README routes | platform | completed | PASS | EVD-010 and EVD-022 independent reviews, EVD-011, EVD-017 and EVD-021 staged QA |
| WORK-003 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | Review App creation, installation and first check run | operator | completed | PASS | EVD-013 App and installation, EVD-014 first check run resolving EVD-003 and EVD-012, EVD-016 bootstrap copy |
| WORK-004 | [VAL-IR-004](../spec.md#success-criteria--verification-plan) | Main protection requirement and EVD-012 disposition | operator and platform | completed | PASS | EVD-024 approval, EVD-015 protection update, EVD-023 blocked and mergeable observations and merge |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Mitigation research | GitHub documentation read on 2026-10-16 by a `docs-researcher` agent, plus read-only `gh api` GETs of rulesets, main protection and environments | NOT_RUN | Pending | no | none |
| EVD-002 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Publisher focused tests | `scripts/independent_review.py`, `tests/test_independent_review.py` on branch `codex/evd-012-independent-review` | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review App check run | Operator-created App, single-repository installation, this package's PR head | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-IR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Main protection read-back | Before/after `branches/main/protection` and PR merge state | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent security review | `security-auditor` agent, read-only, fresh context, `git diff 26508fe2 b4c4f266` | FAIL | `request_changes`: one HIGH (the runbook ran the key-holding publisher from the PR worktree, so a PR could force success or take the key), three MEDIUM (reviewer prompt injection unstated, key path not denied, no `publish()`/`main()` tests) and six LOW findings | yes | none |
| EVD-006 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent security review | Same reviewer, `git diff b4c4f266 e6fc44d6`, head `e6fc44d69a1a13b903b3fe718963426083cf7885` | PASS | `approve`: HIGH, MEDIUM and LOW findings resolved or recorded as residual. Remaining MEDIUM (same-user PR code can read the key) and three LOW items (generic worktree command, `git cat-file` extraction, approval record) were applied in the following commit | yes | EVD-005 |
| EVD-007 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Selected staged QA | Normal commits `b4c4f266` and `e6fc44d6` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed for both commits | yes | none |
| EVD-008 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Mitigation research | GitHub documentation read on 2026-10-16 by a `docs-researcher` agent, plus read-only `gh api` GETs of rulesets, main protection and environments | PASS | Ruleset "require workflows" is documented for organizations, not verified for personal accounts; required checks can bind an expected App; App/Copilot approvals are not documented to count toward required reviews; CODEOWNERS cannot gate a solo author. Repository: four tag rulesets only, classic main protection with `ci-summary`/`style-pr` App `15368`, environments `qa-control` and `qa-tag-publish`. Design inputs only, not remote evidence of the new gate | no | none |
| EVD-009 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Publisher focused tests | `scripts/independent_review.py`, `tests/test_independent_review.py` at commit `e6fc44d6` | PASS | Pinned `/tmp/hyhome-r10-validation/bin/python -m unittest tests/test_independent_review.py`: 13 tests OK covering verdict shape and conclusion, rendering and truncation, key mode and owner, an openssl-verified JWT and claim window, `publish()` head/base refusal, token scope, check body and revocation, and `main()` error exits; Ruff check and format passed. The reviewer reran the same 13 tests independently. No network call was made | yes | EVD-002 |
| EVD-010 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent PR-head review | Fresh `security-auditor` session, read-only, `git diff 26508fe2 4305b4f7`, head `4305b4f73ddce23f5d43f842953f7cee61172e7d` | PASS | `approve`, no critical or high finding. One MEDIUM: the tracked `core.hooksPath` lets a checked-out PR run hook code that can read the key or repoint `origin/main`; five LOW items (silent revocation, test gaps, evidence inconsistencies, unpinned bootstrap copy). All were applied in the following commit | yes | none |
| EVD-011 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Normal commits `4305b4f7` and `09bcf738` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed for both commits | yes | none |
| EVD-012 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review App check run | First operator publish on PR #152 head `6907f0d0` with App `5341483` | FAIL | `FAIL: GitHub GET` of `repos/buenhyden/hy-home.k8s/installation` `returned 404`: the App JWT was accepted but the repository installation was not yet visible. No token was issued and no check run was created | yes | none |
| EVD-013 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review App installation | Operator-run App-JWT `GET /app` and `GET /app/installations` on 2026-10-16, plus the operator's installation settings report | PASS | App `5341483`, slug `hy-home-independent-review`, owner `buenhyden`; one installation `171987966` on `buenhyden` with `repository_selection: selected` and permissions exactly `checks: write`, `metadata: read`, `pull_requests: read`. The operator reported `Only select repositories` with `buenhyden/hy-home.k8s` alone; the repository list itself was not read through the API | yes | none |
| EVD-014 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review App check run | Second operator publish on PR #152 head `6907f0d01ba2e7903581127eb43ca859e39a77db` with the `approve` verdict of the independent re-review of that head | PASS | Publisher output `independent-review id=116853906432 app=5341483 … conclusion=success`; read-only `commits/6907f0d0/check-runs` showed `independent-review` from App `5341483` (`hy-home-independent-review`) completed `success`, beside `ci-summary` and `style-pr` from App `15368` | yes | EVD-003, EVD-012 |
| EVD-015 | [VAL-IR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Main protection update | `gh api` by `buenhyden`: GET at `2026-10-16T07:03:23Z`, approved `PATCH branches/main/protection/required_status_checks`, GET at `07:03:24Z` | PASS | Before: strict, `ci-summary`/`style-pr` App `15368`. After: strict, plus `independent-review` App `5341483`. A JSON diff of every field outside `required_status_checks` was empty: `enforce_admins` true, conversation resolution true, zero approving reviews, force pushes and deletion blocked | yes | none |
| EVD-016 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Bootstrap publisher copy | `git cat-file blob 6907f0d0:scripts/independent_review.py` to a scratch file outside the repository | PASS | Copy blob `0ad8bf05e3b86bcaf4e6919215dee99df22e3631` equals the reviewed commit's blob. This is the one-time PR #152 exception named in RUN-0013; later PRs use the `origin/main` copy | no | none |
| EVD-017 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Normal commit `6907f0d0` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | Staged QA, Commitizen and the generated-message exception hook passed | yes | none |
| EVD-018 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Publisher focused tests | Working tree after `6907f0d0` with the revocation-warning test added | PASS | Pinned interpreter: 16 tests OK, including a failed `DELETE /installation/token` that warns on stderr without the token and keeps the check-run result | yes | none |
| EVD-019 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review App installation | Operator-run read-only `GET /installation/repositories` with a metadata-read installation token, revoked after use | PASS | `total 1 ['buenhyden/hy-home.k8s']`: the installation covers only this repository | no | none |
| EVD-020 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Publisher focused tests | Commit `e3a4b71377843321c5520cdcae5558b4ecf969f7` | PASS | The independent reviewer ran the 16 tests on a `git archive` copy of that commit: OK. This binds EVD-018 to the commit where the revocation-warning test landed | yes | none |
| EVD-021 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Normal commit `e3a4b713` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | Staged QA, Commitizen and the generated-message exception hook passed | yes | none |
| EVD-022 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent PR-head review | Same `security-auditor` reviewer, `git diff 6907f0d0 e3a4b713` and re-reviews of `6907f0d0` | PASS | `approve` on both heads, no critical, high or medium finding. Remaining LOW items (SEC-P01-001 level, approval record, commit-bound evidence, API repository list) are applied in this closeout | yes | none |
| EVD-023 | [VAL-IR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Main protection read-back | PR #152 head `e3a4b713` after EVD-015; read-only `gh pr view` and `commits/<head>/check-runs` by `buenhyden` | PASS | `2026-10-16T07:18:34Z`: `BLOCKED` with `ci-summary` and `style-pr` from App `15368` `success` and no `independent-review`. Operator published check run `116860817539` from App `5341483` (`success`). `07:20:59Z`: `CLEAN`/`MERGEABLE`. PR #152 merged as `7c7e6e8110f031194d7e2c5e3a39b11ead7de677` | yes | EVD-004 |
| EVD-024 | [VAL-IR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Protection change approval | Operator answer on 2026-10-16 before EVD-015 to the exact proposal: `PATCH branches/main/protection/required_status_checks`, strict `true`, checks `ci-summary@15368`, `style-pr@15368`, `independent-review@5341483`, no other field | PASS | The operator selected "approve, apply now". The approval covers this one PATCH and its read-back; it is not standing authority for later protection changes | yes | none |
| EVD-025 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Reviewer procedure | The `security-auditor` session reviewing `e3a4b713` | FAIL | The reviewer disclosed one plain `git fetch -q origin` in the PR worktree without `-c core.hooksPath=/dev/null`, the pattern RUN-0013 forbids. The worktree held this package's own authored branch, so no hostile hook was present; the lapse is recorded, not repeated | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-IR-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006, EVD-007, EVD-009, EVD-018, EVD-020 | Tests, staged QA and independent review passed; EVD-005 is resolved by EVD-006 | platform |
| [VAL-IR-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-010, EVD-011, EVD-017, EVD-021, EVD-022 | Documents pass staged QA and independent review. Accepted notwithstanding EVD-025 by explicit platform decision: the lapse touched only remote-tracking refs in this package's own authored worktree, rests on the reviewer's disclosure, and RUN-0013 already forbids it | platform |
| [VAL-IR-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-012, EVD-013, EVD-014, EVD-016, EVD-019 | App `5341483` is installed with the scoped permissions on this repository only (EVD-019 supersedes the operator report in EVD-013) and produced a `success` check run on a real PR head; EVD-012 is resolved by EVD-014 | operator |
| [VAL-IR-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-015, EVD-023, EVD-024 | Approved protection update, observed blocked and mergeable states and merge; EVD-004 is resolved by EVD-023 | operator and platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0116-independent-review-gate/**`,
  `docs/03.specs/README.md`, `docs/05.operations/runbooks/0013-independent-review-check-runbook.md`,
  `docs/05.operations/runbooks/README.md`, `scripts/independent_review.py`,
  `scripts/README.md`, `tests/test_independent_review.py`,
  `.github/rulesets/main-protection.md`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other
  Spec packages, credentials and any file holding the review App key.
- **Approval Required**: The operator's request covers repository work and
  research. Its wording ("research a resolution for EVD-012, write its Spec
  and proceed") is recorded as approval of SPEC-0116 and its Plan as
  written on 2026-10-16; the operator may revoke or amend it. App creation and
  installation are operator UI actions. The
  `main` protection update needs the operator's exact approval of the target
  field set after WORK-003, with before/after read-back. No model API key is
  requested or stored.
- **Static Validation**: Focused tests, Ruff, `qa.py staged` on the exact
  index and selected document checks.
- **Live Validation**: Remote observation only: check-run App ID and protection
  read-back. No cluster access.
- **Secret / Vault Handling**: The App private key stays in the operator's
  local file with mode `0600`; agents neither read nor print it. Installation
  tokens are never logged.
- **Rollback Plan**: Revert the repository commits through Git. Remove the
  required check by a reviewed operator decision with read-back; uninstall or
  delete the App if abandoned.
- **Evidence Location**: This Task.

## Verification Summary

All four criteria are accepted. The publisher, its 16 tests, staged QA and
independent reviews pass (VAL-IR-001, VAL-IR-002). App `5341483` is installed
only on this repository and produced `success` check runs after one
installation-visibility failure (VAL-IR-003). `main` requires
`independent-review` from that App; PR #152 was observed `BLOCKED` without it
and `CLEAN` with it, then merged (VAL-IR-004). Required-check forgery by a
PR-edited workflow is closed; the PR-editable workflow body remains a separate,
owner-accepted HIGH risk in the main protection record. The operator's own key access,
reviewer prompt injection and same-user execution of hostile PR code remain
residual risks, and EVD-025 records one reviewer procedure lapse. The
non-required EVD-001 stays `NOT_RUN` as history; its research is EVD-008.
