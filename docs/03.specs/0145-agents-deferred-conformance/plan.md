---
title: "Agent Surface Deferred Conformance Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0145-PLAN-0001"
parent_ids: ["SPEC-0145"]
---

# Agent Surface Deferred Conformance Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- The failing regression test is written before the validator change.

## Overview

This plan executes [SPEC-0145](spec.md) on branch `docs/agents-deferred`
from `main` at `18b76c17`.

## Context

SPEC-0144 (REQ-0003 Archived Lineage) deferred these items. The CIS source is
the kube-bench encoding of CIS Kubernetes Benchmark v1.9
(`cfg/cis-1.9/policies.yaml`); the sibling source is the local
`hy-home.docker` checkout. Rollback is reverting the implementing commits.

## Goals & In-Scope

Close VAL-DEF-001 to VAL-DEF-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DEF-003](spec.md#success-criteria--verification-plan) | Test first, then derive projections in the validator and remove the per-role fields | None | [Task](tasks/tsk-0001-agents-deferred-conformance.md) | Regression FAIL then PASS; agent-governance validator |
| WORK-002 | [VAL-DEF-001](spec.md#success-criteria--verification-plan) | Rewrite the three shared sections of each role body | None | [Task](tasks/tsk-0001-agents-deferred-conformance.md) | Strict document checks, agent-governance tests |
| WORK-003 | [VAL-DEF-002](spec.md#success-criteria--verification-plan) | Add Item Index and Add and Find to the collection-index READMEs | None | [Task](tasks/tsk-0001-agents-deferred-conformance.md) | Strict document checks |
| WORK-004 | [VAL-DEF-004](spec.md#success-criteria--verification-plan) | State the `sdlc.md` contract invariant, renumber CIS references, refresh the sibling pin | None | [Task](tasks/tsk-0001-agents-deferred-conformance.md) | Source comparison, strict document checks |

## Verification Plan

Run the regression red then green, the agent-governance validator and tests,
the strict document checks, an independent review and `python3 scripts/qa.py staged`
on each commit.

## Risks & Mitigations

- A consumer outside the validator could read `projections`; the 2026-11-06
  search found only the validator and tests.
- A role-body rewrite could change a role's scope; the review compares each
  body with its registry entry.

## Completion Criteria

VAL-DEF-001 to VAL-DEF-004 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
