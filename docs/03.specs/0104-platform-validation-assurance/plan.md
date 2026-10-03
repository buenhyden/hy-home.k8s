---
title: "Platform Validation Assurance Delivery Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0104-PLAN-0001"
---

# Platform Validation Assurance Implementation Plan

## Global Constraints

Use the existing validation registry, bounded runner, and product validators.
Keep quick/staged checks short; run deep offline render/schema at full/CI.
Missing required tools or schema coverage fail, and static evidence never
claims live readiness. Preserve required policy, GitOps, secret, and Vault/ESO
gates and the current ingress-nginx/ADR-0043 topology. No live mutation or
secret values enter this work unit.

## Overview

Implement [SPEC-0104](spec.md) and close the scoped repository-static gaps of
REQ-0004-FR-0008 and REQ-0004-FR-0010. The evidence Task records the exact
implementation, reviewed tool/schema source, validation, and residual limits.

## Context

The existing manifest check parses tracked YAML; structural, policy, secret,
Vault/ESO, and product checks already run through the registry. The current
unfinished coverage identified by [REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md)
and [AD-0007](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
is offline render/API schema, per-target depth/tool/fallback/lane/result, and
full GVK/Ingress cross-reference. The withdrawn Traefik-dependent Spec is not
an implementation input. Pinned tool/schema selection and generated-resource
boundaries are resolved from executable source and independent review before
the relevant gate is enabled.

## Goals & In-Scope

- Extend existing evidence output with required per-target classification.
- Add one standalone Kustomize 5.8.1 render and Kubernetes 1.35 built-in
  API-schema gate at the full/CI lane, reusing jsonschema 4.26.0.
- Close bounded GVK/Ingress-reference gaps using current ingress-nginx and
  explicit chart/operator declaration ownership.
- Prove negative cases and complete reciprocal requirement/architecture trace
  without conflating static and live evidence.

## Non-Goals & Out-of-Scope

Live cluster admission, external host/DNS/TLS observation, secret values,
cloud deployment, blanket chart validation outside the declared roots,
provenance/SBOM expansion, and resurrecting withdrawn Specs.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Extend per-target runner/registry evidence and result fixtures | None | Current registry/result contract reviewed | Focused metadata/fallback/required-tool results in [Task 1](tasks/tsk-0001-evidence.md) |
| WP-002 | Select pinned offline tool/schema source, render declared roots, and verify covered API kinds | WP-001 | Tool/source and root inventory reviewed | Positive/negative build/schema fixtures and full/CI result in [Task 2](tasks/tsk-0002-render-schema.md) |
| WP-003 | Resolve full GVK, tracked Ingress references, chart-managed destinations, and transport exception boundaries | WP-001, WP-002 | Current AD/ADR and chart declaration ownership reviewed | Broken-reference/GVK fixtures and existing-gate parity in [Task 3](tasks/tsk-0003-platform-references.md) |
| WP-004 | Reconcile documentation, exact-index/hosted checks, independent review, and delivery | WP-001–WP-003 | All focused checks pass | Handoff and lane-limited acceptance in [Task 4](tasks/tsk-0004-integration.md) |

## Verification Plan

Each behavior change starts with a focused failing case and ends with its
passing case. WP-001 proves reporting and fallback without silently promoting
depth. WP-002 proves offline success and required-tool/schema failure; WP-003
proves broken tracked and chart-owned reference cases and reruns the retained
policy/secret/structure contracts. WP-004 uses exact-index staged QA, hosted
full/CI for PR delivery, and one independent read-only semantic review. Live
checks are DEFER with operator and retry condition. Reuse hosted evidence only
when common QA identity requirements prove the same input and contract.

## Risks & Mitigations

| Risk | Mitigation / owner |
| --- | --- |
| A chart-managed controller Service is mistaken for absent tracked state | Platform validator checks reviewed pinned chart values/template declarations; quality engineer records source and that generated output was not observed. |
| Missing API schema is reported as success or a network download changes validation | Required covered kinds fail without the pinned offline schema; quality engineer owns fixed source and negative fixture. |
| Deep validation slows every local edit | Registry places it at full/CI; quick/staged keep existing scoped checks. |
| CI tool installation widens permissions or control-plane trust | CI workflow engineer makes a scoped pinned install only if needed; security reviewer checks it. |
| Static result is mistaken for live readiness | Integration Task separates repo-static, hosted, provider and live lanes; operator owns any future observation. |

## Completion Criteria

All four Spec criteria have reproducible evidence in Task records, affected
gates and hosted CI pass for final bytes, independent read-only review
dispositions are recorded, and REQ-0004/AD-0007 current links name the new
owner. The Task records any unavailable external/live evidence as DEFER and
its retry owner. Terminal lifecycle and archive cutover occur only after
their own registry gates and consumer-zero assessment.

## Traceability

[SPEC-0104](spec.md) supplies acceptance; the four Tasks below own actual
commands and outcomes.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-PVA-001](spec.md#success-criteria--verification-plan) | WP-001 | [SPEC-0104-TSK-0001](tasks/tsk-0001-evidence.md) |
| [VAL-PVA-002](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0104-TSK-0002](tasks/tsk-0002-render-schema.md) |
| [VAL-PVA-003](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0104-TSK-0003](tasks/tsk-0003-platform-references.md) |
| [VAL-PVA-004](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0104-TSK-0004](tasks/tsk-0004-integration.md) |
