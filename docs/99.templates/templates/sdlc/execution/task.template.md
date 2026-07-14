---
title: 'Task: {Task Name}'
type: sdlc/task
status: draft
owner: platform
updated: YYYY-MM-DD
---

# Task: [Task Name]

## Overview

<!-- Author prompt: identify the bounded execution stream and its completion evidence. -->

## Inputs

<!-- Author prompt: link the approved Plan, Spec, decisions, and required evidence inputs. -->

## Task Table

<!-- Author prompt: keep one row per executable item and update result and evidence as work advances. -->

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-FEATURE-001 | One bounded change | platform | Queued | Not executed | Named repository evidence |

## Approval and Safety Boundaries

- **Allowed Paths**: `<repository-relative paths>`
- **Forbidden Paths**: `<repository-relative paths or none>`
- **Approval Required**: `<approval boundary>`
- **Static Validation**: `<commands and expected evidence>`
- **Live Validation**: `<approved lane or DEFER with reason>`
- **Secret / Vault Handling**: `<no-read/no-print boundary and owner>`
- **Rollback Plan**: `<reversible steps or commit>`
- **Evidence Location**: `<durable repository path>`

<!-- Author prompt: add GitOps, Kubernetes, or Runbook impact fields only when applicable. -->

## Verification Summary

<!-- Author prompt: summarize per-lane outcomes, limitations, review disposition, and residual risk. -->

## Traceability

<!-- Author prompt: map each criterion or work item to its result and durable evidence. -->

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| WORK-001 | State the observed result. | Name the test, review, or commit evidence. |
