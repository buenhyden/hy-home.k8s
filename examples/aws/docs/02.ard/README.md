# 02.ard (Architecture Requirements Document)

> AWS 클라우드 네이티브 아키텍처 설계 및 참조 모델 정의

## Overview

이 디렉토리는 마이그레이션 대상 시스템의 전반적인 구조를 정의합니다. Managed Node Group, Karpenter, Pod Identity 등 최신 기술이 적용된 아키텍처 다이어그램 및 품질 속성을 포함합니다.

## Audience

이 README의 주요 독자:

- Cloud Architects
- Platform Engineers
- AI Agents

## Scope

### In Scope

- AWS 마이그레이션 참조 아키텍처
- 품질 속성, 네트워크 경계, 보안/운영성 요구
- 하위 ADR 및 Spec으로 이어지는 구조 설명

### Out of Scope

- 단일 기술 결정 기록
- Bicep/Terraform 같은 구현 코드
- 작업 상태 추적

## Structure

```text
02.ard/
├── 0001-aws-cloud-native-architecture.md  # AWS cloud-native 참조 아키텍처
├── 2026-03-31-aws-migration-ard.md        # AWS 마이그레이션 ARD
└── README.md                              # This file
```

## How to Work in This Area

1. [01.prd](../01.prd/README.md)의 요구사항을 먼저 확인합니다.
2. 새 ARD는 `../../../../docs/99.templates/ard.template.md`를 기준으로 작성합니다.
3. 아키텍처 결정은 [03.adr](../03.adr/README.md)에 별도 기록합니다.
4. 구현 계약은 [04.specs](../04.specs/README.md)와 연결합니다.

## Related References

- [01.prd](../01.prd/README.md) - 제품 요구사항
- [03.adr](../03.adr/README.md) - 기술 의사결정
- [04.specs](../04.specs/README.md) - 상세 명세
