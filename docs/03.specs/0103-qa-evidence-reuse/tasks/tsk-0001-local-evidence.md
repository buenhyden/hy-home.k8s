---
title: "Local exact-input QA evidence"
version: "0.1.2"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0001"
---

# Task: Local exact-input QA evidence

## Overview

Execute [Plan WP-0001](../plan.md) against the approved [SPEC-0103](../spec.md). Implementation is committed at `bc763fba9fd8ea073dce5ba186291ec88a60e443`. Focused, quick, and exact-index staged checks passed. Independent review accepted corrective commit `a18d1ed92a9d76eda07e71cc90a4689a24427b8e`; the local work is complete. No hosted result is claimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-001, VAL-QER-002.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-QER-001, VAL-QER-002 | Implement exact local gate identity and reuse | platform | Completed | Local checks and independent review PASS; hosted unclaimed | Implementation `bc763fba9fd8ea073dce5ba186291ec88a60e443`; commands and limitations below. |

## Approval and Safety Boundaries

- **Allowed Paths**: scripts/qa.py; scripts/run-validation-lane.py; scripts/validate-affected-surfaces.py; scripts/validation/registry.json; scripts/validation/registry.schema.json; tests/test_qa_runner.py; tests/test_run_validation_lane.py; tests/test_validation_profiles.py
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: None beyond approved Plan; no remote mutation
- **Static Validation**: python3 -m unittest tests.test_qa_runner tests.test_run_validation_lane tests.test_validation_profiles; python3 scripts/qa.py quick
- **Live Validation**: DEFER until PR/main workflow work; local evidence is not hosted proof
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Revert `bc763fba9fd8ea073dce5ba186291ec88a60e443` as one reviewed unit; remove only its local cache file if the operator wants to reclaim space. No remote rollback is needed.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

- **Scope and snapshot**: `codex/qa-evidence-implementation` started at `b5206db877ab6a95aca15f4020e20e7f95e90f64`, with base `0ed105b832d85c88b1000ad58959531d1ae23cae`. The exact staged code tree and implementation commit tree are `58f4deda2956276e8c9509b261e8ffd1b6b2196d`. Changed implementation paths are the eight files in Plan WP-0001. The subsequent Task/Plan evidence commit is a document-only snapshot and does not change the checked code bytes.
- **RED / GREEN**: New identity/store and reuse tests initially failed before implementation; the first broad RED attempt was interrupted after test-class inheritance unintentionally ran unrelated cases. The corrected focused fixtures passed after implementation: seven new local/reuse/profile cases, then three runner cases after the final unknown-metadata guard. The complete focused command `python3 -m unittest tests.test_qa_runner tests.test_run_validation_lane tests.test_validation_profiles` passed 129 tests in 242.666 s on the implementation snapshot; the final two-line unknown-metadata guard was separately checked with `ReuseCandidateTest` (3 tests PASS).
- **Working tree / exact index**: `python3 scripts/qa.py quick` passed eight selected gates, and `python3 scripts/qa.py staged` passed eight selected gates on tree `58f4deda2956276e8c9509b261e8ffd1b6b2196d`. `pre-commit run ruff-check` and `ruff-format` over the six Python files passed. `git diff --check` and `git diff --cached --check` passed before commit. The normal commit hook chain ran for the implementation commit. Final full QA was deferred to the integration owner; Task 6 records the new frozen implementation result. The earlier baseline does not prove later code bytes.
- **Disposition**: VAL-QER-001 and VAL-QER-002 are locally PASS after the independent repair review recorded below. The registry still owns gate membership/argv, and full/ci parity tests passed. The initial opted-in gate was `external-service-contracts`; corrective commit `a18d1ed9` replaced it with the audited stdlib-only `agent-evaluation-cases`. All other gates execute normally. Local evidence is scoped to quick/staged and cannot satisfy hosted full/ci. Hosted CI, provider runtime, and live validation are DEFER to later work packages. No optional-tool SKIP or failed/deferred child was stored.
- **Review and residual risk**: Author self-review found and repaired malformed non-object record handling, mode/owner read races, missing-tool reuse, and unknown reuse metadata. Independent `review_task1` initially requested dependency-byte and negative-execution-count repairs. Commit `a18d1ed9` restricts reuse to the stdlib/snapshot-only evaluator and strengthens execution assertions; focused 133, quick 8/8 and staged 8/8 passed. Scoped re-review was clean, with both findings addressed and zero open; the controller recorded Task 1 complete over `b5206db8..a18d1ed9`. A same-user actor can rewrite a user-owned local record; the record is only a local optimization and is never hosted authority. The first document-only quick QA failed because this Task used the unsupported status `active`; the state was corrected to `in-progress` and the affected lane rerun. Final frozen-code QA and the independent whole-branch code/security review are reconciled in [Task 6](tsk-0006-integration.md); the supervisor owns delivery.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Completed: local criteria and independent repair review PASS | Implementation `bc763fba`, corrective `a18d1ed9`; focused 133, quick/staged 8/8; final integration evidence in Task 6. |
