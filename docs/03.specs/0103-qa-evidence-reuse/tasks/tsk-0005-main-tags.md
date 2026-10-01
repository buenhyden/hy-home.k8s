---
title: "Protected immutable main tag publisher"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0005"
---

# Task: Protected immutable main tag publisher

## Overview

Execute [Plan WP-0005](../plan.md) against the approved [SPEC-0103](../spec.md). This record starts queued; no implementation or hosted result is claimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-010.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-005 | VAL-QER-010 | Follow Plan Task 5 RED, GREEN, review, and handoff steps | platform | Queued | Not executed | This record; fill actual commits, commands, run IDs and reviewer on execution. |

## Approval and Safety Boundaries

- **Allowed Paths**: .github/workflows/qa-verifier.yml; .github/repository-surface.md; scripts/publish_main_tag.py; tests/test_publish_main_tag.py; tests/test_ci_qa_workflow.py
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: Operator review before separate publisher App installation, contents:write permission, main-only key environment, or creation/update/delete tag rulesets
- **Static Validation**: python3 -m unittest tests.test_publish_main_tag tests.test_ci_qa_workflow; python3 scripts/qa.py quick
- **Live Validation**: Authenticated ruleset and publisher App/environment read-back; verifier App contents:write denial, denied update/delete, one exact-SHA tag and retry; DEFER until configured
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Disable publication; never move or delete existing main-* tags automatically.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

Queued. Preserve distinct PASS, SKIP, FAIL, and DEFER results when executed. A static fixture is not a hosted or provider observation.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-005](../plan.md#work-breakdown) | Queued | Plan Task 5; actual evidence pending. |
