---
title: "Validate Offline Render and Kubernetes Schemas"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0104-TSK-0002"
---

# Task: Validate Offline Render and Kubernetes Schemas

## Overview

Add one full/CI offline Kustomize build and built-in Kubernetes API-schema
gate using standalone Kustomize 5.8.1, existing jsonschema 4.26.0, and
vendored strict Kubernetes 1.35.0 built-in schemas from upstream commit
`8df8a883b68a24a104b4a9e43c1288090ae60b3b`. The Kustomize Linux amd64
release SHA-256 is
`029a7f0f4e1932c52a0476cf02a0fd855c0bb85694b82c338fc648dcb53a819d`.
Known custom resources have explicitly named schema
limitations; unknown/malformed input cannot silently pass.

## Inputs

[Plan](../plan.md), [Spec](../spec.md), current
[manifest validator](../../../../scripts/validate-k8s-manifests.sh),
[registry](../../../../scripts/validation/registry.json), and
[AD-0007](../../../02.architecture/descriptions/0007-current-local-gitops-platform.md).

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-002 | VAL-PVA-002 | Pin offline tool/schema inputs, render declared roots, reject invalid/missing inputs, and prove lane selection | quality-engineer / ci-workflow-engineer | Queued | Not executed | Focused negative fixtures, pinned source/digest, hosted full/CI run |

## Approval and Safety Boundaries

- **Allowed Paths**: affected `scripts/validation/` and `scripts/validate-k8s-manifests.sh`, fixed schema assets/lock, focused `tests/`, `.github/` pinned tool installation by its CI owner, this Task.
- **Forbidden Paths**: live cluster, secret values, unreviewed runtime downloads.
- **Approval Required**: CI permission/trigger expansion or external mutation follows the current approval policy; neither is presumed.
- **Static Validation**: positive/negative offline build, schema source and missing-tool tests; staged exact-index and hosted full/CI.
- **Live Validation**: DEFER; no API-server admission claim.
- **Secret / Vault Handling**: Do not read or print values.
- **Rollback Plan**: Revert the scoped deep gate and pinned installation as one change; existing syntax/policy gates remain required.
- **Evidence Location**: this Task's Verification Summary and Traceability.

## Verification Summary

Queued; record the fixed upstream commit/digests, actual covered roots/kinds,
known CR schema DEFER list, commands, and result when executed.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-002](../plan.md#work-breakdown) | Queued | [VAL-PVA-002](../spec.md#success-criteria--verification-plan) and WP-002 |
