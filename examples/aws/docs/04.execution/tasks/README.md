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
2. 새 Task 문서는 `../../../../docs/99.templates/task.template.md`를 기준으로 작성합니다.
3. 검증 명령, 증거 위치, 상태를 함께 기록합니다.

## Related References

- [04.execution/plans](../plans/README.md) - 마이그레이션 실행 계획
- [05.operations/guides](../../05.operations/guides/README.md) - 운영 가이드
- [03.specs](../../03.specs/README.md) - 구현 계약
