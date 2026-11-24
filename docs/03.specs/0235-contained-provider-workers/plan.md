---
title: "Contained Provider Workers Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0235-PLAN-0001"
parent_ids: ["SPEC-0235"]
---

# Contained Provider Workers Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P12 change for [SPEC-0235](spec.md). The platform owner
and reviewers use it to follow the work units, their checks and rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-contained-provider-workers.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the P12 request recorded in the Spec, the existing dispatcher
and request brief modules with their regressions, the installed `claude` and
`codex` CLIs, bwrap 0.9.0 and the user systemd manager.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 adds provider units, brief freshness and the scope and bwrap
boundary with regressions, runs two real Claude workers that update the
dispatcher's two documentation consumers, and runs one Codex worker once its
quota returns.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md):
one shared dispatcher and one brief store per Git common directory.

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. No new paid service, no
worker output executed outside its boundary, and no full-service start.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A descendant escapes the killed group | The whole scope is stopped and its absence gates the lease release | platform |
| A worker writes outside its clone | bwrap binds only the clone and a private `/tmp` writable | platform |
| A worker reads host secrets or uses the network | Host reads and the network stay open and are recorded as residual risk | platform |
| A live run spends without bound | Claude takes `--max-budget-usd`; every unit has a timeout and the scope a run-time cap | platform |

###### Escalation

Stop if a scope survives its stop, and keep the lease.

#### Dependencies

##### Prerequisites

The pinned validation environment, bwrap, the user systemd manager and a
current request brief.

##### Shared Resources

`scripts/work_parallel.py` and `scripts/request_brief.py` are written by
WORK-001 only; each live worker owns one documentation file.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria), [AC-0004](spec.md#criteria) | Provider units, brief freshness, scope and bwrap boundary and regressions; then two live Claude workers that update the two consumers, reviewed and applied; then one live Codex worker | None | [Task](01.tasks/tsk-0001-contained-provider-workers.md) | dispatcher and brief regressions and recorded live runs |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Provider workers start under a current brief inside the boundary, and real workers of both providers return integrated results | none | platform | `scripts/work_parallel.py`, `scripts/request_brief.py`, `tests/test_work_parallel.py`, `tests/test_request_brief.py`, `scripts/README.md`, `.agents/workflows/delegated-development.md`, `docs/03.specs/README.md`, this package | AC-0001, AC-0002, AC-0003, AC-0004 | CHK-PARALLEL, CHK-BRIEF, CHK-LIVE |

###### Change and Rollback

Revert the commits; a running scope is stopped with `systemctl --user stop`
and `sweep` reclaims a dead dispatcher's scopes.

##### Dependency Edges

None; there is one work unit. Its live runs follow its code change.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-PARALLEL | Plan, argv, parsing, freshness, containment and reclaim | Temporary repositories and a stand-in CLI | Local host | Dispatcher changes | `work-parallel-regressions` |
| CHK-BRIEF | Brief freshness for dispatch | Temporary repositories | Module only | Brief changes | `tests.test_request_brief` |
| CHK-LIVE | Real workers, overlap and integration | Live account and user systemd | Local host only | Once per provider | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
route of the pull request; the containment cases skip where no user systemd
manager or bwrap exists. Live runs are recorded in the Task.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P12-PROVIDER-WORKERS | [Delegated development](../../../.agents/workflows/delegated-development.md) | Step 5 states provider units, brief freshness and the boundary | Text written by a WORK-001 live worker |

##### Consumer Updates

The delegated development workflow and the scripts index describe provider
workers.

## 적용과 확인

### 적용 방법

Follow the work units in the Task and record each check there.

### 확인 기준

Completion needs the four criteria's evidence and the operator's criterion
decisions.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| implements | [SPEC-0235](spec.md) |

### 외부 근거

No external source is adopted.
