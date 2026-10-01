---
title: "Main gate-wise reuse"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0004"
---

# Task: Main gate-wise reuse

## Overview

Execute [Plan WP-0004](../plan.md) against the approved [SPEC-0103](../spec.md). This record starts queued; no implementation or hosted result is claimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-005, VAL-QER-006, VAL-QER-007.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-004 | VAL-QER-005, VAL-QER-006, VAL-QER-007 | Follow Plan Task 4 RED, GREEN, review, and handoff steps | platform | Queued | Not executed | This record; fill actual commits, commands, run IDs and reviewer on execution. |

## Approval and Safety Boundaries

- **Allowed Paths**: scripts/qa.py; scripts/run-validation-lane.py; scripts/validation/registry.json; scripts/validation/registry.schema.json; .github/workflows/ci.yml; scripts/qa_provenance.py; tests/test_qa_runner.py; tests/test_run_validation_lane.py; tests/test_ci_qa_workflow.py; tests/test_validation_profiles.py
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: Activation requires observed protected PR/main App check and operator read-back; otherwise full main
- **Static Validation**: python3 -m unittest tests.test_qa_runner tests.test_run_validation_lane tests.test_ci_qa_workflow tests.test_validation_profiles; python3 scripts/qa.py quick
- **Live Validation**: Observed exact PR/main run and per-gate verdict; DEFER until protected check active
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Turn reuse off first, then restore ordinary full QA main route.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

Queued. Preserve distinct PASS, SKIP, FAIL, and DEFER results when executed. A static fixture is not a hosted or provider observation.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-004](../plan.md#work-breakdown) | Queued | Plan Task 4; actual evidence pending. |
