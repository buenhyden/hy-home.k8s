---
title: "Ingress Controller Identity in Validators Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0119-PLAN-0001"
parent_ids: ["SPEC-0119"]
---

# Ingress Controller Identity in Validators Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change under `gitops/**`, `infrastructure/**` or `policy/**`.

## Overview

This plan executes [SPEC-0119](spec.md) on branch
`refactor/spec-0119-ingress-controller-identity` from main `ad3e187f`.

## Context

A read-only scoping review on 2026-10-16 found the nginx literals only in
`ingress.py` and `validate-infrastructure-contracts.sh`; `policy/`,
`.kube-linter.yaml` and the validation registry hold none.

## Goals & In-Scope

Close VAL-ICI-001 and VAL-ICI-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ICI-001](spec.md#success-criteria--verification-plan) | Declare the controller identity and read it everywhere in `ingress.py` | None | [Task](tasks/tsk-0001-ingress-controller-identity.md) | Focused tests, assurance, staged QA |
| WORK-002 | [VAL-ICI-002](spec.md#success-criteria--verification-plan) | Remove shell assertions duplicated by `ingress.py` | WORK-001 | [Task](tasks/tsk-0001-ingress-controller-identity.md) | Mutation proof, shell validator, review |

## Verification Plan

WORK-001 runs the ingress tests before and after and the platform assurance
entry. WORK-002 mutates each manifest field a removed assertion covered and
shows `ingress.py` fails, then runs the shell validator. The branch receives
one independent read-only review.

## Risks & Mitigations

- The declaration drifts from the manifests: the Application, Service and
  Ingress checks compare them on every run.
- A removed shell assertion was not covered: mutation proof before removal.

## Completion Criteria

Both criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
