---
title: "Selected Session Content Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0233-PLAN-0001"
parent_ids: ["SPEC-0233"]
---

# Selected Session Content Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P10 change for [SPEC-0233](spec.md). The platform owner
and reviewers use it to follow the work unit, its checks and its rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-selected-session-content.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the P10 request recorded in the Spec, the current capture and
analysis modules with their regressions, the live local stores and the user
systemd manager.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 adds selected content, retention, capacity and failure identity to
capture, classified rules and candidate expiry to analysis, and the
per-workspace timer, with regressions, policy text and live observation.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md):
one store per Git common directory and one shared implementation.

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. No raw copy, export,
hidden reasoning or new paid analysis. The stores only gain a table; the
existing cursor and record transaction is kept.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A secret pattern escapes redaction | Redaction runs on the whole value before any cut and again after it; a remaining match becomes a gap | platform |
| Long agentic turns use up the 4 KiB summary | The final response and failed results stay selected; the rest records a `summary_cap` gap | platform |
| Retiring the legacy unit removes another clone's timer | Only a service file equal to this checkout's is retired | platform |

###### Escalation

Stop if a live store fails its integrity check, and keep its backup.

#### Dependencies

##### Prerequisites

The pinned validation environment, the live stores and the user systemd
manager.

##### Shared Resources

`scripts/session_capture.py` and `scripts/session_analysis.py` are written
by this one unit only.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria) | Selected content, retention, failure identity, classified rules, candidate expiry, per-workspace timer and live observation | None | [Task](01.tasks/tsk-0001-selected-session-content.md) | capture and analysis regressions and recorded live observation |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Capture keeps bounded redacted selected content and each workspace runs its own analysis | none | platform | `scripts/session_capture.py`, `scripts/session_analysis.py`, `tests/test_session_capture.py`, `tests/test_session_analysis.py`, `.agents/governance/context-and-memory.md`, `docs/03.specs/README.md`, this package | AC-0001, AC-0002, AC-0003 | CHK-CAPTURE, CHK-ANALYSIS, CHK-LIVE |

###### Change and Rollback

Revert the implementation commit and reinstall the timer from the reverted
checkout; the added tables stay harmless and `expire` or `forget` removes
their content.

##### Dependency Edges

None; there is one work unit.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-CAPTURE | Selection, redaction order, caps, idempotency, expiry and gaps | Temporary transcripts | Module only | Capture changes | `session-capture-regressions` |
| CHK-ANALYSIS | Classified rules, candidate expiry, unit naming and retirement | Temporary stores | Module only | Analysis changes | `session-analysis-regressions` |
| CHK-LIVE | Live scan, residue, registration and one unit run | Live stores and user systemd | Local host only | Once | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
affected route of the pull request; live observations are recorded in the
Task.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P10-SESSION-RULES | [Context and memory](../../../.agents/governance/context-and-memory.md) | CTX-R006, R022 and R023 state the changed capture and analysis behavior | Policy text in this change |

##### Consumer Updates

The context and memory policy carries the changed capture, retention and
timer rules.

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
| implements | [SPEC-0233](spec.md) |

### 외부 근거

No external source is adopted.
