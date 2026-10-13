---
title: "Agent Evaluation Evidence"
version: "0.2.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---

# Agent Evaluation Evidence

## Overview

이 디렉터리는 같은 작업을 실제로 짝지어 실행한 근거로 안내한다. 한 번은
`noSkill` 기준선, 한 번은 `withSkill` 실행이다. 평가는
[agent evaluator](../roles/agent-evaluator.md)가, 근거의 의미는
[quality policy](../governance/quality.md#agent-evaluation-evidence)가, 문서
양식은 [Stage 99](../../docs/99.templates/README.md)가 소유한다. 저장된 응답만으로는
native skill 적재, 명령 실행, 권한 강제, 저장소 QA 관문 통과를 증명하지 못한다.

## Scope

작업, 실제 출력 두 개, 채점 근거를 관측된 세션에 연결할 수 있을 때만 cycle을
받아들인다. cycle 하나에는 짝 실행 하나만 두고, 추가 실행은 별도 cycle
디렉터리를 쓴다. 집계를 주장하기 전에 신호, 채점자와 기준 ID, 한 쌍 단위 점수,
부분 결과, 사람 보정을 기록한다. 관측이 없으면 `NOT_OBSERVED`, 짝 비교를
실행하지 않았으면 `NOT_RUN`으로 남긴다. 작업 승인과 실행 상태는 원래 Task가,
provider·native·runtime 주장은 원래 근거 소유자가 가진다.

이전의 합성 사례와 응답은 Git과 Task의 과거 근거일 뿐 이 디렉터리의 실제 짝
실행이 아니다. 합성 fixture에 기대값이 없다고 해서 그것이 skill 없는 응답이
되지는 않는다. fixture 개수도 이 라우터도 상시 채점기나 QA 관문을 등록하지
않는다. 작업 공간에 없는 사용자 제공 skill 정의는 참고 기준일 뿐이며, 이
경로는 그것을 설치하거나 만들지 않는다.

## Structure

| Path | Purpose |
| --- | --- |
| [harnesses/](harnesses/) | 같은 작업에 맞춘 실행 입력과 관측된 원시 출력으로 안내한다. |
| [templates/](templates/) | Stage 99의 작업·점수·결과 양식으로 안내하며 그 권한을 복사하지 않는다. |
| [results.md](results.md) | 완결된 실제 cycle이 받아들여졌을 때의 유일한 집계 소유자. 빈 상태에는 점수가 없다. |

## Usage

### Configuration Boundary

실행 전에 두 조건에 같은 작업과 기준선을 선언한다. 실제 prompt, skill 판본,
provider·세션 식별, 한 쌍 실행 선언, 채점자와 기준 ID를 cycle과 함께 보관한다.
작업이나 rubric이 바뀌면 새 비교 입력이 되며, 이전 점수를 조용히 고치지 않는다.

### Validation

실제 입력에서 현재 Stage 99 profile, 링크, 선언된 짝의 완결성, 점수 계산을
확인한다. 포함되는 모든 cycle에 완결된 실제 짝이 있을 때만 결과를 기록하고,
불완전한 짝은 미완료로 남긴다. 집계는 고정 품질 임계값 없이 실제 cycle 수를
보고한다. 저장소 QA, 독립 의미 검토, provider runtime 관측은 서로 다른 lane이다.

### Operations

원시 출력과 세션 출처는 관측된 실행과 함께 두고, 선언된 rubric에 따라 채점을
기록한 뒤 `results.md`에서 한 번만 집계한다. provider·세션을 쓸 수 없거나
skill 또는 응답이 없으면 원래 Task 소유자에게 보고한다. 행을 채우려고 출력을
합성하지 않는다.

## Related Documents

- [Common agent governance](../README.md)
- [Agent evaluator responsibility](../roles/agent-evaluator.md)
- [Quality policy](../governance/quality.md#agent-evaluation-evidence)
- [Stage 99 profiles and templates](../../docs/99.templates/README.md)
- [Stage 03 Spec navigation](../../docs/03.specs/README.md)
