---
title: "Hosted CI Lock Check"
version: "0.2.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0123"
---

# Hosted CI Lock Check Technical Specification (Spec)

## Overview

The CI Python lock `.github/requirements/ci-validation.txt` must keep exactly
one `--only-binary :all:` directive and wheel-only hashes;
`scripts/validate-ci-python-contract.py` enforces that in the local `affected`
and `staged` QA lanes. A Dependabot security update is authored on GitHub, so
it never passes local staged QA, and the hosted `ci-summary` and `style-pr`
jobs do not run the lock check. Twice (PR #164 and PR #172) a Dependabot lock
dropped the directive and still showed green checks; only the independent
review caught it. This Spec adds one hosted step that runs the reviewed base's
lock check against a pull request's files when the pull request changes
`.github/requirements/`. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-hosted-lock-check.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - one conditional step in the `style-pr` job of `.github/workflows/ci.yml`;
  - the reviewed `style-pr` topology in
    `scripts/validate-ci-python-contract.py` and its tests;
  - the hosted lane wording in `.agents/governance/quality.md`.
- Non-goals:
  - running local purpose, unit or document-content QA on hosted runners;
  - a new job or a new required status check;
  - changing `.github/dependabot.yml` or the lock itself;
  - executing pull-request code: the step runs only reviewed-base scripts.

## Contracts

- The step runs only when the pull request's changed paths include a path
  under `.github/requirements/`; otherwise it does nothing and passes.
- It runs `python -I ../trusted-base/scripts/validate-ci-python-contract.py
  --root .` in the `candidate` checkout: the program comes from the reviewed
  base, and the pull request supplies data only.
- A failure fails `style-pr`, which `main` already requires, so no branch
  protection change is needed.
- The hosted result reports only this lock contract on the pull request's
  files. It does not run or certify local QA (REQ-0003-FR-0017).

## Core Design

`style-pr` already checks out the reviewed base as `trusted-base` and the pull
request merge as `candidate` and installs the base's pinned lock. A seventh
step lists every changed path with an unfiltered `git diff --name-only -z`
into `$RUNNER_TEMP/pr-lock-paths.z`, so a deleted or retyped lock still
matches, and a failed `git diff` stops the job instead of skipping the check.
When a requirements path changed, it runs the base validator against the
candidate root. `validate-ci-python-contract.py` reads files only and
starts no subprocess, so a candidate cannot make it execute its code. The
validator's reviewed `style-pr` step list gains the same seventh step.

## Data Modeling & Storage Strategy

No stored data. The step reads the changed-path list the job already writes.

## Interfaces & Data Structures

- `.github/workflows/ci.yml` `style-pr` step 7, `Validate a changed CI lock`.
- `_validate_style_pr_job` in `scripts/validate-ci-python-contract.py`: seven
  reviewed steps.

## Edge Cases & Error Handling

- A pull request that changes the lock and `style-pr` together is checked
  against the base's reviewed topology and fails until the workflow change
  lands first.
- A pull request that changes no requirements path skips the check.

## Failure Modes & Fallback / Human Escalation

If the hosted step blocks a valid lock, the lock is regenerated with the
recorded `pip-compile` command, as commit `7195e74e` did. Reverting this
Spec's pull request restores the six-step job.

## Verification Commands

- `python3 -m unittest tests.test_validate_ci_python_contract`.
- `python3 scripts/validate-ci-python-contract.py --root .`.
- `python3 scripts/validate-github-actions-security.py --root .`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-HL-001 | The reviewed topology admits exactly the seven-step `style-pr` job, and the base validator fails a candidate lock without the `--only-binary :all:` directive. |
| VAL-HL-002 | The pull request's hosted `style-pr` passes with the new step skipped, and staged QA passes on the exact index. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0004-FR-0012](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-HL-001 | Validator tests and a failing candidate lock |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HL-002 | Hosted run and staged QA |
