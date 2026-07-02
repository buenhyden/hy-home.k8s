# 03.specs (Technical Specifications)

> AWS 리소스 및 인프라 컴포넌트 상세 명세

## Overview

이 디렉토리는 아키텍처 설계를 실제 구현하기 위한 세부 기술적 수치를 명시합니다. VPC CIDR 설계, IAM Role 정책 명세, EKS Add-on 설정 등을 다룹니다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- Cloud Engineers
- AI Agents

## Scope

### In Scope

- AWS 인프라와 플랫폼 구성의 상세 기술 계약
- 네트워크, IAM, EKS, 관리형 서비스 설정 기준
- 검증 기준과 하위 작업으로 이어지는 링크

### Out of Scope

- 비즈니스 요구사항
- 단일 기술 결정 기록
- 운영 정책과 장애 대응 절차

## Structure

```text
03.specs/
├── aws-migration/
│   └── spec.md  # AWS 마이그레이션 기술 명세
└── README.md    # This file
```

## How to Work in This Area

1. [02.architecture/requirements](../02.architecture/requirements/README.md)와 [02.architecture/decisions](../02.architecture/decisions/README.md)를 먼저 확인합니다.
2. 새 Spec은 `../../../../docs/99.templates/templates/sdlc/specs/spec.template.md`를 기준으로 작성합니다.
3. 실행 계획과 검증 작업은 [04.execution/plans](../04.execution/plans/README.md), [04.execution/tasks](../04.execution/tasks/README.md)에 연결합니다.

## Link Basis

이 README의 링크 기준 위치는 `examples/aws/docs/03.specs/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [02.architecture/requirements](../02.architecture/requirements/README.md) - 아키텍처 참조 모델
- [02.architecture/decisions](../02.architecture/decisions/README.md) - 기술 의사결정
- [04.execution/plans](../04.execution/plans/README.md) - 마이그레이션 실행 계획
