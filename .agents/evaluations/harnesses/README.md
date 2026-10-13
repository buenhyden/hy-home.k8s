---
title: "Agent Evaluation Trial Evidence"
version: "0.2.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---

# Agent Evaluation Trial Evidence

## Overview

이 라우터는 같은 작업과 기준선에서 관측한 `noSkill`, `withSkill` 출력의
진입점이다. 안내는 [평가 root](../README.md)가, 승인과 실제 실행 상태는 원래
Task가 소유한다.

## Scope

실제 cycle마다 작업과 기준선 식별, 두 조건의 입력과 원시 출력, provider·세션
출처, 한 번의 짝 실행, 신호, 기준 ID, 불완전한 시도를 보관한다. 생성된 예시,
실행하지 않은 조건, 과거 합성 응답은 관측된 실행이 아니다. native skill 적재,
명령 실행, 권한 관측은 각각 직접적인 세션 근거가 필요하다.

## Structure

### Item Index

받아들인 직접 cycle 디렉터리를 여기에 한 번씩 색인한다. cycle 하나는 정확히
한 번의 짝 실행에 대해 `task.md`, `baseline.md`, `with-skill.md`, `score.md`를
담는다. 두 원시 출력 파일은 관리용 frontmatter로 감싸지 않고 관측한 원래
내용을 그대로 둔다. 재평가는 새 cycle 디렉터리를 쓰고 이전 근거를 보존한다.
추가 실행도 별도 cycle 디렉터리를 쓴다. 유일한 집계 결과 소유자는
[상위 라우터](../README.md)가 밝히고, [양식](../templates/README.md)은 schema를
복사하지 않고 Stage 99를 가리킨다. 실행하지 않은 시도를 나타내는 자리표시
행은 두지 않는다.

## Usage

### Add and Find

두 조건을 수집하기 전에 작업과 기준선을 고정한다. 비교를 재현할 수 있도록
skill과 판본, provider·세션 입력을 보존한다. 주장된 점수마다 원시 관측과 선언된
기준 ID에 대조한다. 출력이 없으면 `NOT_OBSERVED`, 실행하지 않았으면
`NOT_RUN`으로 소유 Task에 기록하고, 부분 시도는 보존하되 완료된 짝이나 집계
결과로 넣지 않는다. 완결된 cycle을 받아들이면 그 디렉터리 링크를 Item Index에
추가하고, rubric이 요구하면 사람 보정과 함께 점수를 유일한 집계 소유자에게
넘긴다.

## Related Documents

- [Evaluation root](../README.md)
- [Evaluation forms router](../templates/README.md)
- [Agent evaluator responsibility](../../roles/agent-evaluator.md)
- [Quality policy](../../governance/quality.md#agent-evaluation-evidence)
