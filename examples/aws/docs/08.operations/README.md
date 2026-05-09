# 08.operations (System Operations & Governance)

> AWS 클라우드 인프라 자산 운영 정책 및 관리 표준

## Overview

이 디렉토리는 마이그레이션 이후의 지속 가능한 운영 거버넌스를 정의합니다. AWS 비용 최적화 전략, 클라우드 리소스 태깅 표준, 백업 및 데이터 보관 정책을 포함합니다.

## Audience

이 README의 주요 독자:

- Cloud Operators
- Platform Engineers
- AI Agents

## Scope

### In Scope

- AWS 운영 정책과 통제 기준
- 비용, 태깅, 백업, 보안 운영 표준
- Runbook과 Incident로 이어지는 운영 참조

### Out of Scope

- 상세 구현 명세
- 실행 순서 중심 장애 대응 절차
- 프로젝트 작업 상태 추적

## Structure

```text
08.operations/
├── aws-management.md           # AWS 관리 기준
├── aws-operations-policy.md    # AWS 운영 정책
└── README.md                   # This file
```

## How to Work in This Area

1. [04.specs](../04.specs/README.md)의 기술 계약과 현재 운영 기준을 비교합니다.
2. 새 Operation 문서는 `../../../../docs/99.templates/operation.template.md`를 기준으로 작성합니다.
3. 반복 실행 절차는 [09.runbooks](../09.runbooks/README.md)에 분리합니다.

## Related References

- [01.prd](../01.prd/README.md) - 마이그레이션 목표
- [07.guides](../07.guides/README.md) - 운영 실무 가이드
- [09.runbooks](../09.runbooks/README.md) - 장애 조치 지침
