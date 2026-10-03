---
title: "Close Platform Resource and Ingress References"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0104-TSK-0003"
---

# Task: Close Platform Resource and Ingress References

## Overview

Check full group/version/kind and tracked Ingress destinations against
current ingress-nginx desired state, with explicit ownership of generated
chart/operator resources and bounded local-only transport exceptions.

## Inputs

[Plan](../plan.md), [Spec](../spec.md),
[AD-0007](../../../02.architecture/descriptions/0007-current-local-gitops-platform.md),
[ADR-0043](../../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md),
and current platform validators.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-003 | VAL-PVA-003 | Reject invalid GVK/Ingress references and regressions in structure, policy, secret, ESO, and local transport gates | quality-engineer | Queued | Not executed | Focused negative fixtures and existing gate results |

## Approval and Safety Boundaries

- **Allowed Paths**: affected existing platform validation scripts, focused `tests/`, this Task.
- **Forbidden Paths**: retired Traefik implementation, live runtime, secret values.
- **Approval Required**: external mutation is outside this Task; no approval assumed.
- **Static Validation**: focused GVK/reference failures and current structure/policy/secret/Vault-ESO checks.
- **Live Validation**: DEFER; operator-owned host/controller observation remains separate.
- **Secret / Vault Handling**: Inspect references only.
- **Rollback Plan**: Revert the scoped validator change without disabling existing required gates.
- **Evidence Location**: this Task's Verification Summary and Traceability.

## Verification Summary

Queued; record actual files, chart-output evidence, results, and limitations
during execution.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-003](../plan.md#work-breakdown) | Queued | [VAL-PVA-003](../spec.md#success-criteria--verification-plan) and WP-003 |
