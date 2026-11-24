---
title: "Task Artifact Cleanup Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0238-PLAN-0001"
parent_ids: ["SPEC-0238"]
---

# Task Artifact Cleanup Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P15 change for [SPEC-0238](spec.md). The platform owner
and reviewers use it to follow the work unit, its checks and its rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-task-artifact-cleanup.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the P15 request recorded in the Spec, the analysis module and
its regressions, the quality policy, the work lifecycle, the local scratch
area and `_workspace/`.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 removes the finished one-off code and its test, writes the cleanup
rule, and deletes this work's finished temporary material and the approved
1.1.0 package.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md).

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. No persistent store,
other workspace's material or P16 and P17 input is deleted, and no denied
command is worked around.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A persistent item is taken for temporary | Sort by real consumer; stores, regressions, timers, reports and other tasks' material stay | platform |
| An untracked package deletion cannot be undone | Delete only the package the operator approved, after confirming no current owner reads it | platform |

###### Escalation

Stop before deleting anything whose owner is unclear, and keep it.

#### Dependencies

##### Prerequisites

The operator's approval for the 1.1.0 package and the pinned validation
environment.

##### Shared Resources

`scripts/session_analysis.py` is written by this one unit only.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria) | One-off code removal, cleanup rule and local deletions | None | [Task](01.tasks/tsk-0001-task-artifact-cleanup.md) | analysis regressions, staged QA and local observation |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Finished temporary material is gone and the cleanup rule is stated | none | platform | `scripts/session_analysis.py`, `tests/test_session_analysis.py`, `.agents/governance/context-and-memory.md`, `.agents/workflows/work-lifecycle.md`, `docs/00.workspace/04.quality/quality.md`, `docs/03.specs/README.md`, this package; locally the session scratch area and `_workspace/workspace_governance_remediation_1_1_0_20261120/` | AC-0001, AC-0002, AC-0003 | CHK-ANALYSIS, CHK-DOCS, CHK-LOCAL |

###### Change and Rollback

Revert the commit for the code and rule; the deleted scratch and package are
not recoverable from Git, which the operator accepted for the package.

##### Dependency Edges

None; there is one work unit.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-ANALYSIS | The install contract | Temporary home directory | Module only | Analysis changes | `session-analysis-regressions` |
| CHK-DOCS | Profile, links and lifecycle | Staged index | Repository static | Document changes | Staged QA |
| CHK-LOCAL | Deleted and kept local material | Local host | Local host only | Once | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
route of the pull request; local deletions are recorded in the Task.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P15-CLEANUP-RULE | [Work lifecycle](../../../.agents/workflows/work-lifecycle.md) | Completion step 3 applies the QUAL-R025 sort and records kept recovery material | Text in this change |

##### Consumer Updates

QUAL-R025 states the sort; CTX-R023 no longer mentions the retired legacy
unit.

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
| implements | [SPEC-0238](spec.md) |

### 외부 근거

No external source is adopted.
