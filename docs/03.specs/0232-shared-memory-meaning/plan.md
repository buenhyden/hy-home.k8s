---
title: "Shared Memory Meaning Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0232-PLAN-0001"
parent_ids: ["SPEC-0232"]
---

# Shared Memory Meaning Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P09 change for [SPEC-0232](spec.md). The platform owner
and reviewers use it to follow the work unit, its checks and its rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-shared-memory-meaning.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the P09 request recorded in the Spec, the current memory and
analysis modules with their regressions, and the live local stores.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 adds the common view, source statuses, conflicted exclusion and
typed digests to the memory store, and the review receipt and promotion
outbox to the analysis store, with regressions, policy text and one live
read observation.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md):
one store per Git common directory and one shared implementation for both
providers.

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. The memory schema does
not change; the analysis store only gains tables. No real memory content is
deleted.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| Hiding conflicted items surprises a reader | The flag `--include-conflicted` and history keep them reachable | platform |
| The live analysis store changes shape | Only create-if-missing tables; a consistent backup precedes the first open | platform |
| A reviewed candidate reviewed before this change has no receipt | The live store has no accepted, unpromoted candidate; a new review supplies one | platform |

###### Escalation

Stop if the live store fails its integrity check or its counts change, and
keep the backup.

#### Dependencies

##### Prerequisites

The pinned validation environment and the local live stores.

##### Shared Resources

`scripts/workspace_memory.py` and `scripts/session_analysis.py` are written
by this one unit only.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria) | Common view, typed digests, promotion outbox, regressions, policy and live read | None | [Task](01.tasks/tsk-0001-shared-memory-meaning.md) | memory and analysis regressions and the recorded live read |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | The store exposes the common meaning and promotions are atomic | none | platform | `scripts/workspace_memory.py`, `scripts/session_analysis.py`, `tests/test_workspace_memory.py`, `tests/test_session_analysis.py`, `.agents/governance/context-and-memory.md`, `docs/03.specs/README.md`, this package | AC-0001, AC-0002, AC-0003 | CHK-MEMORY, CHK-PROMOTION, CHK-LIVE |

###### Change and Rollback

Revert the implementation commit. The two analysis tables stay harmlessly
in the live store; older code ignores them.

##### Dependency Edges

None; there is one work unit.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-MEMORY | Common view, source states, exclusion and typed digests | Temporary repositories | Module only | Store changes | `workspace-memory-regressions` |
| CHK-PROMOTION | Review binding, outbox, retry and erase | Temporary stores | Module only | Promotion changes | `session-analysis-regressions` |
| CHK-LIVE | Live stores read through the changed code | Local live stores | Local read only | Once | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
affected route of the pull request; the live read is recorded in the Task.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P09-MEMORY-RULES | [Context and memory](../../../.agents/governance/context-and-memory.md) | CTX-R012, R014, R015, R021 and R023 state the changed behavior | Policy text in this change |

##### Consumer Updates

The context and memory policy carries the changed store and promotion rules.

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
| implements | [SPEC-0232](spec.md) |

### 외부 근거

No external source is adopted.
