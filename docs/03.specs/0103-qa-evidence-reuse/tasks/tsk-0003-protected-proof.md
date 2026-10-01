---
title: "Protected App PR proof"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0003"
---

# Task: Protected App PR proof

## Overview

Execute [Plan WP-0003](../plan.md) against the approved [SPEC-0103](../spec.md). This record starts queued; no implementation or hosted result is claimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-004, VAL-QER-007, VAL-QER-008.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-003 | VAL-QER-004, VAL-QER-007, VAL-QER-008 | Follow Plan Task 3 RED, GREEN, review, and handoff steps | platform | Queued | Not executed | This record; fill actual commits, commands, run IDs and reviewer on execution. |

## Approval and Safety Boundaries

- **Allowed Paths**: .github/workflows/qa-verifier.yml; .github/workflows/ci.yml; scripts/qa_provenance.py; tests/test_qa_provenance.py; tests/test_ci_qa_workflow.py
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: Operator review before verifier App creation/install, main-only environment secret, required-check settings, or control-code bootstrap
- **Static Validation**: python3 -m unittest tests.test_qa_provenance tests.test_ci_qa_workflow; python3 scripts/qa.py quick
- **Live Validation**: Authenticated verifier App ID and permission ceiling, environment policy, required-check source, hostile PR and control-change trials; DEFER until configured
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Disable App-sourced reuse, retain full main QA; never remove a required check without protected replacement.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

Queued. Preserve distinct PASS, SKIP, FAIL, and DEFER results when executed. A static fixture is not a hosted or provider observation.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-003](../plan.md#work-breakdown) | Queued | Plan Task 3; actual evidence pending. |
