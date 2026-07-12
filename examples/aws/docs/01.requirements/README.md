# 01.requirements (Product Requirements Document)

> AWS 마이그레이션 프로젝트의 비전 및 비즈니스 요구사항 정의

## Overview

이 디렉토리는 로컬 K3s 인프라를 AWS 클라우드 네이티브 환경으로 전환하기 위한 전략적 요구사항을 담고 있습니다. 비즈니스 가치 창출, 사용자 경험 개선, 그리고 마이그레이션 성공 기준을 정의합니다.

### Audience

이 README의 주요 독자:

- Product Managers
- Cloud Architects
- Business Stakeholders
- AI Agents

### Scope

#### In Scope

- 마이그레이션 비전 및 목표 정의
- 핵심 비즈니스 요구사항 및 제약 사항
- 마이그레이션 성공 지표 (KPI)

#### Out of Scope

- 상세 기술 구현 명세 (03.specs 참조)
- 실행 태스크 리스트 (04.execution/tasks 참조)

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 AWS 마이그레이션 예시다. 기반 마이그레이션 기록은 하위 문서가 다른 날짜를 명시하지 않는 한 2026-03-31 기준이며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
01.requirements/
├── 2026-03-31-aws-migration-prd.md  # 핵심 요구사항 정의서
└── README.md                       # This file
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/aws`로의 후속 통합을 소유한다. AWS 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/aws/`에 둔다.

1. [2026-03-31-aws-migration-prd.md](2026-03-31-aws-migration-prd.md)를 통해 프로젝트 전반의 요구사항을 먼저 파악하십시오.
2. `../../../../docs/99.templates/templates/sdlc/requirements/prd.template.md`를 사용하여 새로운 요구사항을 추가합니다.
3. 요구사항 변경 시 `04.execution/plans` 및 `04.execution/tasks`와의 정렬을 확인하십시오.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live AWS 계정, EKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/aws/docs/01.requirements/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [AWS Docs README](../README.md)
- [02.architecture/requirements](../02.architecture/requirements/README.md) - 아키텍처 참조 모델
- [04.execution/plans](../04.execution/plans/README.md) - 실행 로드맵
