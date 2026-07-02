# 04.execution/tasks (Implementation Tasks)

> 마이그레이션 실행 및 검증을 위한 세부 작업 단위 관리

## Overview

이 디렉토리는 `04.execution/plans`에서 정의된 로드맵을 달성하기 위한 구체적인 작업(WBS)을 관리합니다. 인프라 프로비저닝, 데이터 싱크 개시, 트래픽 전환 등 단계별 동작을 트래킹합니다.

## Audience

이 README의 주요 독자:

- Cloud Migration Engineers
- Platform Engineers
- AI Agents

## Scope

### In Scope

- AWS 전환 실행 작업
- 검증 기준, 증거, 상태
- 상위 Plan/Spec 링크

### Out of Scope

- 요구사항 정본
- 아키텍처 결정 기록
- 운영 정책 또는 런북

## Structure

```text
04.execution/tasks/
├── 2026-03-31-aws-migration-tasks.md  # AWS 마이그레이션 작업 목록
├── 2026-03-31-bootstrap-aws.md        # AWS 부트스트랩 작업
└── README.md                          # This file
```

## How to Work in This Area

1. [04.execution/plans](../plans/README.md)의 단계와 연결된 작업만 추가합니다.
2. 새 Task 문서는 `../../../../docs/99.templates/templates/sdlc/execution/task.template.md`를 기준으로 작성합니다.
3. 검증 명령, 증거 위치, 상태를 함께 기록합니다.

## Link Basis

이 README의 링크 기준 위치는 `examples/aws/docs/04.execution/tasks/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [04.execution/plans](../plans/README.md) - 마이그레이션 실행 계획
- [05.operations/guides](../../05.operations/guides/README.md) - 운영 가이드
- [03.specs](../../03.specs/README.md) - 구현 계약
