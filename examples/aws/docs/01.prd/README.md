# 01.prd (Product Requirements Document)

> AWS 마이그레이션 프로젝트의 비전 및 비즈니스 요구사항 정의

## Overview

이 디렉토리는 로컬 K3s 인프라를 AWS 클라우드 네이티브 환경으로 전환하기 위한 전략적 요구사항을 담고 있습니다. 비즈니스 가치 창출, 사용자 경험 개선, 그리고 마이그레이션 성공 기준을 정의합니다.

## Audience

이 README의 주요 독자:

- Product Managers
- Cloud Architects
- Business Stakeholders
- AI Agents

## Scope

### In Scope

- 마이그레이션 비전 및 목표 정의
- 핵심 비즈니스 요구사항 및 제약 사항
- 마이그레이션 성공 지표 (KPI)

### Out of Scope

- 상세 기술 구현 명세 (04.specs 참조)
- 실행 태스크 리스트 (06.tasks 참조)

## Structure

```text
01.prd/
├── 2026-03-31-aws-migration-prd.md  # 핵심 요구사항 정의서
└── README.md                       # This file
```

## How to Work in This Area

1. [2026-03-31-aws-migration-prd.md](./2026-03-31-aws-migration-prd.md)를 통해 프로젝트 전반의 요구사항을 먼저 파악하십시오.
2. `../../../../docs/99.templates/prd.template.md`를 사용하여 새로운 요구사항을 추가합니다.
3. 요구사항 변경 시 `05.plans` 및 `06.tasks`와의 정렬을 확인하십시오.

## Related References

- [AWS Docs README](../README.md)
- [02.ard](../02.ard/README.md) - 아키텍처 참조 모델
- [05.plans](../05.plans/README.md) - 실행 로드맵
