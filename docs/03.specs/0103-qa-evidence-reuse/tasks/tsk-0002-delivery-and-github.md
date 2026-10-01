---
title: "Delivery policy, scripts, and GitHub routes"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0002"
---

# Task: Delivery policy, scripts, and GitHub routes

## Overview

Execute [Plan WP-0002](../plan.md) against the approved [SPEC-0103](../spec.md). This record starts queued; no implementation or hosted result is claimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-003, VAL-QER-009, VAL-QER-011.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-002 | VAL-QER-003, VAL-QER-009, VAL-QER-011 | Follow Plan Task 2 RED, GREEN, review, and handoff steps | platform | Queued | Not executed | This record; fill actual commits, commands, run IDs and reviewer on execution. |

## Approval and Safety Boundaries

- **Allowed Paths**: .agents/governance/quality.md; .agents/governance/git.md; .agents/workflows/work-lifecycle.md; scripts/README.md; .github/ISSUE_TEMPLATE/config.yml; .github/PULL_REQUEST_TEMPLATE.md; .github/dependabot.yml; .github/labeler.yml; .github/SECURITY.md; .github/repository-surface.md; tests/test_ci_qa_workflow.py
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: Authenticated GitHub settings are read-only evidence; no repository setting mutation in this task
- **Static Validation**: python3 -m unittest tests.test_ci_qa_workflow tests.test_validation_profiles tests.test_validation_tooling_ownership; python3 scripts/qa.py quick
- **Live Validation**: Read back destination/label/private-reporting settings; labeler fork behavior remains a separate hosted observation
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Revert policy and consumer routes together; retain independent script checks unless transfer was proved.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

Queued. Preserve distinct PASS, SKIP, FAIL, and DEFER results when executed. A static fixture is not a hosted or provider observation.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-002](../plan.md#work-breakdown) | Queued | Plan Task 2; actual evidence pending. |
