---
title: "Close Platform Resource and Ingress References"
version: "1.1.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-04"
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
| WORK-003 | VAL-PVA-003 | Reject invalid GVK/Ingress references and regressions in structure, policy, secret, ESO, and local transport gates | quality-engineer | Completed | Focused references and hosted required gates PASS | `scripts/validation/platform/ingress.py`, `tests/test_platform_ingress.py`, sample-app Service/Ingress; hosted run 37133944612 |

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

The quality engineer reports
`python3 -m unittest tests.test_platform_ingress -q` with 11 passing focused
Ingress tests, including 14 mutations
of reviewed chart-owned declarations, default backend, and snippet cases.
Sample-app backend ports were aligned with the actual Service and its built-in
Kubernetes schema passes in the pinned local probe. The author reproduced
schema failure for the two placeholder ports before replacing them with
numeric values and naming the target port. The check covers tracked
declarations and reviewed chart values, not generated resources observed from
a cluster. Retained GitOps, policy, secret, and ESO gates passed the 14-gate
exact-index implementation staged check and hosted PR #131
[run 37133944612](https://github.com/buenhyden/hy-home.k8s/actions/runs/37133944612).
A separate read-only security reviewer approved the reviewed code snapshot.
The generated controller Service and live ingress path remain unobserved;
an authorized platform operator owns a later render/runtime check when a
specific cluster target is available.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-003](../plan.md#work-breakdown) | Completed | [VAL-PVA-003](../spec.md#success-criteria--verification-plan); 11 focused tests and hosted run 37133944612 PASS, generated/live checks DEFER |
