---
title: "Traefik Ingress Cutover Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0121-PLAN-0001"
parent_ids: ["SPEC-0121"]
---

# Traefik Ingress Cutover Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- Each pull request has its own independent review, staged QA and rollback.
- Live checks are operator-run. A live change outside Argo CD sync needs
  operator approval.

## Overview

This plan executes [SPEC-0121](spec.md) from main `8686ca24`. It has three
pull requests (preparation and side by side in WORK-001, then the cutover), a
live verification and the revert evidence.

## Context

The live router is ingress-nginx controller v1.15.1 (chart 4.15.1). The
first Argo CD sync of it was observed on 2026-10-20 as Synced and Healthy,
with both admission hook Jobs succeeded and `verify-ingress-tls.sh` passing.
SPEC-0119 put the validator's controller identity in one `CONTROLLER`
declaration.

## Goals & In-Scope

Close VAL-TC-001 to VAL-TC-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TC-001](spec.md#success-criteria--verification-plan) | Preparation pull request (neutral IngressClass, ingress-nginx class and webhook off), then side-by-side pull request (Traefik namespace, AppProject entries, Application) | None | [Task](tasks/tsk-0001-traefik-ingress-cutover.md) | Chart render, staged QA, live class check, live Argo CD status |
| WORK-002 | [VAL-TC-002](spec.md#success-criteria--verification-plan) | Live per-route verification through a port-forward | WORK-001 | [Task](tasks/tsk-0001-traefik-ingress-cutover.md) | Operator-run live checks |
| WORK-003 | [VAL-TC-003](spec.md#success-criteria--verification-plan) | Cutover in the stated order: removal, router Service, apex redirects, validators, documents | WORK-002 | [Task](tasks/tsk-0001-traefik-ingress-cutover.md) | Validator tests, staged QA, live router checks |
| WORK-004 | [VAL-TC-004](spec.md#success-criteria--verification-plan) | Revert evidence for the cutover | WORK-003 | [Task](tasks/tsk-0001-traefik-ingress-cutover.md) | Live revert or render with the stated order |

## Verification Plan

Each pull request of WORK-001 and WORK-003 runs focused tests, the chart render and
`qa.py staged`, and get one independent read-only review. WORK-002, the live
checks after each pull request, and WORK-004 are operator-run, recorded in the
Task.

## Risks & Mitigations

- Both controllers claim the same Ingress during the overlap. Traefik has a
  ClusterIP Service only and publishes no Ingress status, so clients and
  `status.loadBalancer` see one controller.
- The IngressClass disappears during its handover. The preparation is its own
  pull request, and its class check passes before the side-by-side pull
  request.
- The router NodePorts and MetalLB address collide at the cutover. The Spec
  states the order, the expected short outage and the revert order.
- An nginx default behaves differently on Traefik. WORK-002 lists each
  behavior as a check, and cutover waits for all of them.
- The cutover fails live. One revert of the cutover pull request restores
  ingress-nginx.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
