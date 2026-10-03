---
title: "Validate Offline Render and Kubernetes Schemas"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
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
| WORK-002 | VAL-PVA-002 | Pin offline tool/schema inputs, render declared roots, reject invalid/missing inputs, and prove lane selection | quality-engineer / ci-workflow-engineer | In progress | Focused offline tests and pinned-binary local probe pass; hosted full/CI pending | `scripts/validation/platform/assurance.py`, `tests/test_platform_assurance.py`, `.github/workflows/ci.yml` |

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

The quality engineer reports a reproduced RED for conflicting identity and
AppProject scope cases, followed by
`python3 -m unittest tests.test_platform_assurance -q` with seven passing
focused tests. A local
probe used the downloaded official Kustomize archive after verifying SHA-256
`029a7f0f4e1932c52a0476cf02a0fd855c0bb85694b82c338fc648dcb53a819d`;
the binary ran from a temporary path because root-owned installation was
unavailable without `sudo` credentials. Its 92 result rows were 46 `PASS`, 45
`DEFER`, and one `SKIP` (sample-app product semantics). The versioned offline
schema corpus is pinned to upstream commit
`8df8a883b68a24a104b4a9e43c1288090ae60b3b`, and source/license plus
per-file hashes are included. Hosted CI's pinned installer must prove the
required full/CI gate on the actual PR checkout before completion. Custom
resource schemas and live admission remain explicit DEFER, not schema PASS.
The reviewed CR set is Argo CD Application, ApplicationSet, AppProject; Argo
Rollouts Rollout and AnalysisTemplate; cert-manager ClusterIssuer; ESO
ClusterSecretStore and ExternalSecret; Istio DestinationRule, VirtualService,
and PeerAuthentication. The code's full GVK table is the executable identity
owner; this list names the current schema limitation, not an API admission
result.
The implementation author and read-only security reviewer are separate; the
reviewer approved the current code snapshot, with final PR evidence pending.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-002](../plan.md#work-breakdown) | In progress | [VAL-PVA-002](../spec.md#success-criteria--verification-plan); seven tests and temporary pinned-binary probe PASS, hosted pending |
