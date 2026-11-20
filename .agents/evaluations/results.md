---
title: "Agent Evaluation Results"
version: "1.0.0"
type: "evaluation/results"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Evaluation Results

## 문서 개요

### 목적과 독자

이 결과 문서는 agent 평가의 paired trial 집계를 확인하는 평가자와 검토자를 위한 기록이다. 범위는 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 집계를 유지한다. 개별 쌍의 포함 상태는 [Pair Coverage](#pair-coverage), 총합은 [Aggregate](#aggregate)에서 확인한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

This is the sole aggregate owner for actual, same-task `noSkill` and
`withSkill` paired evaluations. As of 2026-10-07, no observed cycle has been
admitted. This draft establishes capacity under the current
[evaluation router](README.md), without claiming a provider session or a
repository QA result.

#### Pair Coverage

| Cycle ID | Trial ID | Declared pairs | Complete pairs | Task | Score | Partial reason |
| --- | --- | --- | --- | --- | --- | --- |

No actual pair is recorded. Enter one row per admitted cycle only after its
task, baseline output, with-skill output and score identify the same declared
one-pair trial. Additional trials use distinct cycle IDs; incomplete attempts
remain with their own evidence owners and are not counted as complete pairs.

#### Aggregate

| Scope | Actual pairs | Criterion ID | Baseline summary | With-skill summary | Calibration reference |
| --- | --- | --- | --- | --- | --- |

No denominator or score is reported. Aggregate only complete, declared cycles
with an identified scorer, criterion IDs, score granularity and human
calibration disposition. Report the actual count and measured scope; no fixed
performance threshold is inferred from an empty form.

#### Limitations

Historical synthetic fixtures and missing expectations are not observed
paired outputs. The two user-provided Skill definitions are absent from this
workspace. No paired session, skill loading, command execution, permission
enforcement, score truth or human calibration was observed for this draft.

#### Related Documents

- [Evaluation router](README.md)
- [Quality policy](../../docs/00.workspace/04.quality/quality.md#agent-evaluation-evidence)
- [Stage 99 template navigation](../../docs/99.templates/02.templates/README.md)
- [Agent evaluator responsibility](../roles/agent-evaluator.md)

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
