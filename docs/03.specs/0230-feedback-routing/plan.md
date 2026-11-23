---
title: "Feedback Routing Repair Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-23"
artifact_id: "SPEC-0230-PLAN-0001"
parent_ids: ["SPEC-0230"]
---

# Feedback Routing Repair Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the R01 routing repair for [SPEC-0230](spec.md). The
platform owner and reviewers use it to follow the work unit, its checks and
its rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-feedback-routing.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the R01 request recorded in the Spec, the current validation
registry and the PR341 timing evidence. No live environment is needed.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 delivers suite registration data files with per-suite routes, the
engine route including every suite, a general workspace guide route and their
regressions. Validator code, aggregation and other workspaces stay
unchanged.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md):
the registry remains the one routing owner. No interface or migration beyond
moving suite lists into data files is involved.

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. No check is weakened and
no failure is skipped to shorten a run.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A guide later read by name by the document suite is routed as general | Drift guard test refuses it | platform |
| A registration-only move skips a check the moved module needs | Module files keep their own suite routes; registration validity runs | platform |

###### Escalation

Stop if a routing narrowing would hide a detected defect; the owner decides
whether to keep the broad route.

#### Dependencies

##### Prerequisites

The current registry, `scripts/validate-affected-surfaces.py` and the
pinned validation environment.

##### Shared Resources

`scripts/validation/registry.json` and
`tests/test_validate_affected_surfaces.py` are written by this one unit only.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria) | Suite data split, guide route, regressions and measurement | None | [Task](01.tasks/tsk-0001-feedback-routing.md) | validation-routing suite, mutation results and recorded timing |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Proportional routing for suite registration and general workspace guides | none | platform | `scripts/run-contract-tests.py`, `scripts/validation/contract-suites/`, `scripts/validation/registry.json`, `tests/test_validate_affected_surfaces.py`, `tests/fixtures/validation-surfaces.json`, `scripts/AGENTS.md`, `scripts/README.md`, `tests/AGENTS.md`, `tests/README.md`, this package | AC-0001, AC-0002, AC-0003 | CHK-ROUTE, CHK-DETECT, CHK-TIME |

###### Change and Rollback

Revert the single implementation commit; the suite lists return to the
runner and the registry to its previous routes.

##### Dependency Edges

None; there is one work unit.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-ROUTE | Selection of registration, engine, guide and consumer paths | Registry and fixture | Selection only | Routing data changes | validation-routing suite |
| CHK-DETECT | Selected checks fail on sampled registration and guide defects | Reverted mutations | One defect per class | Once | Task Results |
| CHK-TIME | Before and after cost on the same input | PR341 leaf times, local suite run | Single samples | Once | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
affected route of the pull request; they are not repeated at merge.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |

##### Consumer Updates

`scripts/AGENTS.md`, `scripts/README.md`, `tests/AGENTS.md` and
`tests/README.md` name the suite files as the registration location.

## 적용과 확인

### 적용 방법

Follow WORK-001 in the Task and record each check there.

### 확인 기준

Completion needs the three criteria's evidence and the operator's criterion
decisions.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| implements | [SPEC-0230](spec.md) |

### 외부 근거

No external source is adopted.
