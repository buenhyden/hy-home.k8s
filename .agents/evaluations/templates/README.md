---
title: "Agent Evaluation Form Router"
version: "0.2.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---

# Agent Evaluation Form Router

## Overview

정규 평가 작업, 점수, 집계 양식은 [Stage 99](../../../docs/99.templates/README.md)에
있다. 이 디렉터리는 작성자를 그 양식으로 안내할 뿐이며, schema를 복제하거나
예시 결과를 실제 근거로 제공하지 않는다.

## Scope

평가 문서를 작성하기 전에 현재 Stage 99 profile을 고른다. 점수를 매기는 한 번의
실행 cycle에는 작업 맥락과 실제 출력 두 개가 먼저 있어야 하고, 집계 전에는
선언된 rubric, 기준 ID, 신호 단위, 채점자 ID, 사람 보정이 있어야 한다. 유일한
집계 소유자는 [평가 root](../README.md)가 유지한다. 양식은 실행, 게시, native
runtime 권한을 주지 않는다.

## Structure

### Item Index

이 라우터에는 로컬 양식 사본이 없다. 현재 작업·점수·결과 양식은
[Stage 99 template 라우터](../../../docs/99.templates/templates/README.md)에서,
실제 근거를 둘 위치는 [실행 라우터](../harnesses/README.md)에서 확인한다.
Stage 99는 이 정규 파일을 `evaluation-task.template.md`,
`evaluation-score.template.md`, `evaluation-results.template.md`로 부르며, 이
라우터는 단계를 건너 개별 양식 파일로 링크하지 않는다.

## Usage

### Add and Find

대상 경로에는 Stage 99의 정확한 profile과 판본을 쓴다. 기준과 채점자 식별을
채점 입력과 함께 보존하고, rubric을 고치면 점수를 조용히 다시 쓰지 말고 판본이
붙은 새 비교를 만든다. 집계 전에 profile, 링크, 출처 근거를 검증한다. 빈 결과
양식은 자리일 뿐 측정 점수, 짝 실행, 저장소 QA 결과가 아니다. 실행과 검토는
[quality policy](../../governance/quality.md#agent-evaluation-evidence)와 원래
Task를 따르고, 쓸 수 없는 세션과 빠진 응답은 비교가 아니라 근거 공백으로
넘긴다.

## Related Documents

- [Evaluation root](../README.md)
- [Trial evidence router](../harnesses/README.md)
- [Stage 99 profiles](../../../docs/99.templates/README.md)
- [Stage 99 template navigation](../../../docs/99.templates/templates/README.md)
- [Stage 03 Spec navigation](../../../docs/03.specs/README.md)
