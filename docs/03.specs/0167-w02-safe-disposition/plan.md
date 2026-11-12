---
title: "W02 Safe Disposition Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0167-PLAN-0001"
parent_ids: ["SPEC-0167"]
---

# W02 Safe Disposition Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds one constraint: only the three W02 files the Spec names, this package, the Stage 03 README and reviewed baseline digests change.

## Overview

Add the four missing disposition rules to the lifecycle owner, align the two routers with it, and record the handoffs. [Task 0001](tasks/tsk-0001-w02-safe-disposition.md) owns execution and evidence.

## Context

SPEC-0161 recorded ARC-05 and R147-08 as covered; SPEC-0159 delivered `LIFECYCLE-PACKAGE-EXIT`, and SPEC-0162 to SPEC-0166 used that exit. This branch starts from `main` at `b4925358`. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) is unchanged. No ADR changes: [ADR-0053](../../02.architecture/decisions/0053-unvalidated-archive.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) and [ADR-0057](../../02.architecture/decisions/0057-package-exit-shape-check.md) keep governing.

## Goals & In-Scope

- `document-lifecycle.md`: retained-history exclusions, frozen text, disposition scope, rejected ADR exit.
- `docs/01.requirements/README.md`: owning current document's `Archived Lineage`.
- `docs/02.architecture/AGENTS.md`: rejected ADR exit.

## Non-Goals & Out-of-Scope

- Registry, validator, test and workflow changes (W03, W04, W05).
- A presence, age, archive-body, retention-catalog or migration check.
- Any disposition of a current document.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DISPOSE-001](spec.md#success-criteria--verification-plan), [VAL-DISPOSE-002](spec.md#success-criteria--verification-plan) | Edit the three W02 files. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w02-safe-disposition.md) | Anchor and phrase search, strict document checks, suite. |
| WORK-002 | [VAL-DISPOSE-003](spec.md#success-criteria--verification-plan) | Record the handoffs and the exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w02-safe-disposition.md) | Exact-index QA and commit hooks. |

## Verification Plan

- Run the anchor search after (one hit each) and the README phrase search before (hits) and after (none).
- Run the commands in the Spec's Verification Commands.
- Architecture compliance: AD-0006 unchanged; ADR-0053, ADR-0056 and ADR-0057 followed.
- Record the risk class (`medium`: policy change) and the core-diff checklist; no permission, trigger or protected action changes.

## Risks & Mitigations

- **A new rule reads as a new automatic gate.** Owner: W02 author. Mitigation: each rule states a manual deferral condition and names no check. Rollback: revert the implementation commit.
- **The rejected-ADR rule conflicts with the registry state.** Owner: W02 author. Mitigation: the state stays valid; W03 and W04 decide whether to keep it. Rollback: revert the implementation commit.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Retained history, frozen text, disposition scope and rejected ADR exit | [Document lifecycle policy](../../../.agents/governance/document-lifecycle.md) | Current Contract |
