---
title: "Local exact-input QA evidence"
version: "0.1.1"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0001"
---

# Task: Local exact-input QA evidence

## Overview

Execute [Plan WP-0001](../plan.md) against the approved [SPEC-0103](../spec.md). Implementation is committed at `bc763fba9fd8ea073dce5ba186291ec88a60e443`. Focused, quick, and exact-index staged checks passed. Independent code and security review is pending the supervising owner; no hosted result is claimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-001, VAL-QER-002.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-QER-001, VAL-QER-002 | Implement exact local gate identity and reuse | platform | In review | Local checks PASS; hosted DEFER | Implementation `bc763fba9fd8ea073dce5ba186291ec88a60e443`; commands and limitations below. |

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
- **Working tree / exact index**: `python3 scripts/qa.py quick` passed eight selected gates, and `python3 scripts/qa.py staged` passed eight selected gates on tree `58f4deda2956276e8c9509b261e8ffd1b6b2196d`. `pre-commit run ruff-check` and `ruff-format` over the six Python files passed. `git diff --check` and `git diff --cached --check` passed before commit. The normal commit hook chain ran for the implementation commit. Final full QA is DEFER to the integration owner; the supervisor's pre-implementation baseline does not prove these new code bytes.
- **Disposition**: VAL-QER-001 and VAL-QER-002 are locally PASS subject to independent review. The registry still owns gate membership/argv, and full/ci parity tests passed. The sole opted-in gate is `external-service-contracts`; all other gates execute normally. Local evidence is scoped to quick/staged and cannot satisfy hosted full/ci. Hosted CI, provider runtime, and live validation are DEFER to later work packages. No optional-tool SKIP or failed/deferred child was stored.
- **Review and residual risk**: Author self-review found and repaired malformed non-object record handling, mode/owner read races, missing-tool reuse, and unknown reuse metadata. Independent code/security review is pending the supervising owner and is not claimed PASS. A same-user actor can rewrite a user-owned local record; the record is only a local optimization and is never hosted authority. The first document-only quick QA failed because this Task used the unsupported status `active`; the state was corrected to `in-progress` and the affected lane rerun. The next owner is the supervisor for independent review and integration of WP-001.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Queued | Plan Task 1; actual evidence pending. |
