# 04.execution/plans (Implementation Plans)

> 단계별 마이그레이션 실행 로드맵 및 이관 계획

## Overview

이 디렉토리는 실제 서비스 중단 최소화를 위한 단계별 이행 계획을 담고 있습니다. 무중단 DB 이관 계획, 클러스터 전환 시나리오, 검증 전략 및 리스크 관리 계획을 포함합니다.

## Audience

이 README의 주요 독자:

- Project Maintainers
- Cloud Migration Engineers
- AI Agents

## Scope

### In Scope

- AWS 마이그레이션 단계와 일정
- 위험, 완화 전략, 검증 게이트
- 하위 Task로 이어지는 실행 계획

### Out of Scope

- 상세 구현 명세
- 작업별 상태 증거
- 장애 대응 런북

## Structure

```text
04.execution/plans/
├── 2026-03-31-aws-migration-plan.md     # AWS 마이그레이션 실행 계획
├── 2026-03-31-aws-migration-roadmap.md  # 단계별 전환 로드맵
└── README.md                            # This file
```

## How to Work in This Area

1. [03.specs](../../03.specs/README.md)의 구현 계약을 먼저 확인합니다.
2. 새 Plan은 `../../../../docs/99.templates/plan.template.md`를 기준으로 작성합니다.
3. 실행 단위는 [04.execution/tasks](../tasks/README.md)에 연결합니다.

## Link Basis

이 README의 링크 기준 위치는 `examples/aws/docs/04.execution/plans/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [01.requirements](../../01.requirements/README.md) - 마이그레이션 목표
- [03.specs](../../03.specs/README.md) - 인프라 명세
- [04.execution/tasks](../tasks/README.md) - 개별 실행 작업 단위
