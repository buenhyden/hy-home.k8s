---
title: "Agent Evaluation Form Router"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Agent Evaluation Form Router

## 문서 개요

### 목적과 독자

이 README는 .agents/evaluations/templates에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 .agents/evaluations/templates의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

정규 평가 작업, 점수, 집계 양식은 [Stage 99](../../../docs/99.templates/README.md)에
있다. 이 디렉터리는 작성자를 그 양식으로 안내할 뿐이며, schema를 복제하거나
예시 결과를 실제 근거로 제공하지 않는다.

###### Inputs and Outputs

평가 문서를 작성하기 전에 현재 Stage 99 profile을 고른다. 점수를 매기는 한 번의
실행 cycle에는 작업 맥락과 실제 출력 두 개가 먼저 있어야 하고, 집계 전에는
선언된 rubric, 기준 ID, 신호 단위, 채점자 ID, 사람 보정이 있어야 한다. 유일한
집계 소유자는 [평가 root](../README.md)가 유지한다. 양식은 실행, 게시, native
runtime 권한을 주지 않는다.

##### Excluded Responsibilities

이 디렉터리는 평가 양식의 사본이나 schema를 소유하지 않으며, 정규 양식은 Stage 99에 있고 작성자를 그곳으로 안내할 뿐이다. 유일한 집계 소유자는 평가 root가 유지하고, 실제 근거를 둘 위치는 Trial Evidence 라우터다. 양식은 실행, 게시, native runtime 권한을 주지 않으며, 빈 결과 양식은 측정 점수, 짝 실행, 저장소 QA 결과가 아니다.

#### Current Contents

##### Paths

###### Item Index

이 라우터에는 로컬 양식 사본이 없다. 현재 작업·점수·결과 양식은
[Stage 99 template 라우터](../../../docs/99.templates/02.templates/README.md)에서,
실제 근거를 둘 위치는 [Trial Evidence 라우터](../harnesses/README.md)에서 확인한다.
Stage 99는 이 정규 파일을 `evaluation-task.template.md`,
`evaluation-score.template.md`, `evaluation-results.template.md`로 부르며, 이
라우터는 단계를 건너 개별 양식 파일로 링크하지 않는다.

| Path | Purpose |
| --- | --- |

##### Owners

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

#### Usage

##### Entry Points

###### Add and Find

대상 경로에는 Stage 99의 정확한 profile과 판본을 쓴다. 기준과 채점자 식별을
채점 입력과 함께 보존하고, rubric을 고치면 점수를 조용히 다시 쓰지 말고 판본이
붙은 새 비교를 만든다. 집계 전에 profile, 링크, 출처 근거를 검증한다. 빈 결과
양식은 자리일 뿐 측정 점수, 짝 실행, 저장소 QA 결과가 아니다. 실행과 검토는
[quality policy](../../../docs/00.workspace/04.quality/quality.md#agent-evaluation-evidence)와 원래
Task를 따르고, 쓸 수 없는 세션과 빠진 응답은 비교가 아니라 근거 공백으로
넘긴다.

###### Upstream and Downstream

- [Evaluation root](../README.md)
- [Trial Evidence router](../harnesses/README.md)
- [Stage 03 Spec navigation](../../../docs/03.specs/README.md)

###### Policy and Templates

- [Stage 99 profiles](../../../docs/99.templates/README.md)
- [Stage 99 template navigation](../../../docs/99.templates/02.templates/README.md)

##### Checks

상태와 종료 규칙은 위 Add and Find에 함께 있다.

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
