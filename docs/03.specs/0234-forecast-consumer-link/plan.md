---
title: "Forecast Consumer Link Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0234-PLAN-0001"
parent_ids: ["SPEC-0234"]
---

# Forecast Consumer Link Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P11 change for [SPEC-0234](spec.md). The platform owner
and reviewers use it to follow the work unit, its checks and its rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-forecast-consumer-link.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the P11 request recorded in the Spec, the existing forecast
tool with its regressions, the live forecast store and SDLC-R038.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 keeps the forecast tool, states its meaning, key and cutover reset
in SDLC-R038, and runs one real forecast round trip for this change.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md):
one store per Git common directory and one shared implementation.

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. No calculator rewrite,
no forecast gate and no new paid service.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A small N is read as calibration | The tool labels every forecast uncalibrated and the score reports N | platform |
| Trial runs bias the next baseline | The cutover sets the store aside and starts at N=0 | platform |

###### Escalation

Stop if the live store refuses a digest check, and keep the store.

#### Dependencies

##### Prerequisites

The pinned validation environment and the live forecast store.

##### Shared Resources

`docs/00.workspace/03.process/sdlc.md` is written by this one unit only.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria) | Keep the tool, state meaning, key and reset in SDLC-R038, and run one live round trip | None | [Task](01.tasks/tsk-0001-forecast-consumer-link.md) | forecast regressions and recorded live observation |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | The forecast reaches a real work unit through its brief key and the cutover reset is stated | none | platform | `docs/00.workspace/03.process/sdlc.md`, `docs/03.specs/README.md`, this package | AC-0001, AC-0002 | CHK-FORECAST, CHK-LIVE |

###### Change and Rollback

Revert the commit; the live record stays in the ignored store, which never
rewrites rows.

##### Dependency Edges

None; there is one work unit.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-FORECAST | Quantiles, censoring, scoring and immutability | Temporary stores | Module only | Forecast changes | `work-forecast-regressions` |
| CHK-LIVE | One real round trip and its score | Live forecast store | Local host only | Once | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
route of the pull request; the live round trip is recorded in the Task.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P11-FORECAST-RULE | [SDLC flow](../../00.workspace/03.process/sdlc.md) | SDLC-R038 states completion probability, the brief and work-unit key and the cutover reset | Policy text in this change |

##### Consumer Updates

SDLC-R038 carries the changed forecast rule.

## 적용과 확인

### 적용 방법

Follow WORK-001 in the Task and record each check there.

### 확인 기준

Completion needs the two criteria's evidence and the operator's criterion
decisions.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| implements | [SPEC-0234](spec.md) |

### 외부 근거

No external source is adopted.
