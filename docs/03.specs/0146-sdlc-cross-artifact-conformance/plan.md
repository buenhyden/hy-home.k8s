---
title: "SDLC Cross-Artifact Conformance Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0146-PLAN-0001"
parent_ids: ["SPEC-0146"]
---

# SDLC Cross-Artifact Conformance Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No registry, schema or validator change.

## Overview

This plan executes [SPEC-0146](spec.md) on branch
`docs/sdlc-cross-artifact-conformance` from `main` at `3ec90be8`.

## Context

The audit observed the repository at `3ec90be8`. Constraining architecture is
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md);
no interface or migration is touched. Rollback is reverting the commits.

## Goals & In-Scope

Close VAL-SDLC-001 to VAL-SDLC-003.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SDLC-001](spec.md#success-criteria--verification-plan) | Add the Cross-artifact conformance subsection to `sdlc.md` | None | [Task](tasks/tsk-0001-sdlc-cross-artifact-conformance.md) | Strict document and link checks |
| WORK-002 | [VAL-SDLC-002](spec.md#success-criteria--verification-plan) | Add the Spec, Plan and ADR template prompts | WORK-001 | [Task](tasks/tsk-0001-sdlc-cross-artifact-conformance.md) | Strict profile checks and document unit tests |
| WORK-003 | [VAL-SDLC-003](spec.md#success-criteria--verification-plan) | Write the audit pack and route it from the audits README | WORK-002 | [Task](tasks/tsk-0001-sdlc-cross-artifact-conformance.md) | Strict checks and independent review |

## Verification Plan

Run the strict profile, link and lifecycle checks and the document unit tests
after all work units, then an independent read-only review. Architecture
compliance check: every work unit edits only `.agents/governance/` prose,
Stage 99 templates and Stage 90 evidence, the split AD-0006 assigns.

## Risks & Mitigations

- A prompt could duplicate a rule already owned elsewhere; the review
  compares the new text with `document-lifecycle.md` and `quality.md`.
- New rules could burden small changes; the subsection scopes itself to the
  Stage 03 change kinds.

## Completion Criteria

VAL-SDLC-001 to VAL-SDLC-003 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Cross-artifact conformance rules | [Software Development Lifecycle](../../../.agents/governance/sdlc.md) | Current Contract, `Cross-artifact conformance` |
