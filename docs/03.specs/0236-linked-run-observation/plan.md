---
title: "Linked Run Observation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0236-PLAN-0001"
parent_ids: ["SPEC-0236"]
---

# Linked Run Observation Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P13 change for [SPEC-0236](spec.md). The platform owner
and reviewers use it to follow the work unit, its checks and its rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-linked-run-observation.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the P13 request recorded in the Spec, the forecast, parallel
and analysis modules with their regressions, the live local stores and the
SPEC-0223 residue handoff.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 adds the read-only join, the candidate effect, the cost labels and
raw-output deletion, updates CTX-R023 and the two dispatcher consumers, and
closes W10-H04 from the live rechecks.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md):
one store per Git common directory and no new store.

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. No new store, no copy
of hosted logs or provider output, and no repeated paid observation.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A missing source reads as zero | Each missing source is null with its reason and nothing is summed | platform |
| A CLI estimate reads as a bill | The report names it `cost_estimate_usd` and keeps the charge null with a note | platform |
| An effect reads as user acceptance | The label is `effect`, and policy text says it is not acceptance | platform |

###### Escalation

Stop if a forecast digest check refuses a record, and keep the store.

#### Dependencies

##### Prerequisites

The pinned validation environment and the live local stores.

##### Shared Resources

`scripts/session_analysis.py` and `scripts/work_parallel.py` are written by
this one unit only.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria), [AC-0004](spec.md#criteria) | Join, effect, cost labels, raw-output deletion, policy text and the W10-H04 closure | None | [Task](01.tasks/tsk-0001-linked-run-observation.md) | join, analysis and dispatcher regressions and recorded live observation |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Run facts are joined and every unmeasured fact stays visible | none | platform | `scripts/work_observe.py`, `scripts/session_analysis.py`, `scripts/work_parallel.py`, `scripts/validation/registry.json`, `tests/test_work_observe.py`, `tests/test_session_analysis.py`, `tests/test_work_parallel.py`, `scripts/README.md`, `.agents/governance/context-and-memory.md`, `.agents/workflows/delegated-development.md`, `docs/03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md`, `docs/03.specs/work-residue-ledger.json`, `docs/03.specs/README.md`, this package | AC-0001, AC-0002, AC-0003, AC-0004 | CHK-OBSERVE, CHK-EFFECT, CHK-COST, CHK-LIVE |

###### Change and Rollback

Revert the commit; the stores keep their schemas and the join writes nothing.

##### Dependency Edges

None; there is one work unit.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-OBSERVE | Join, key matching, null reasons, no store creation | Temporary stores | Module only | Join changes | `work-observe-regressions` |
| CHK-EFFECT | Effect states and reasons | Temporary stores | Module only | Analysis changes | `session-analysis-regressions` |
| CHK-COST | Cost labels and raw-output deletion | Temporary repositories and a stand-in CLI | Local host | Dispatcher changes | `work-parallel-regressions` |
| CHK-LIVE | Live join and the W10-H04 recheck | Live local stores | Local host only | Once | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
route of the pull request; live observations are recorded in the Task.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P13-RUN-OBSERVATION | [Context and memory](../../../.agents/governance/context-and-memory.md) | CTX-R023 states the candidate effect and the read-only join | Policy text in this change |

##### Consumer Updates

The delegated development workflow and the scripts index describe the cost
labels, raw-output deletion and the join.

## 적용과 확인

### 적용 방법

Follow WORK-001 in the Task and record each check there.

### 확인 기준

Completion needs the four criteria's evidence and the operator's criterion
decisions.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| implements | [SPEC-0236](spec.md) |

### 외부 근거

No external source is adopted.
