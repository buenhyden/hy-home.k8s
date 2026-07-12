# 02.architecture/requirements (Architecture Requirements Document)

> AWS 클라우드 네이티브 아키텍처 설계 및 참조 모델 정의

## Overview

이 디렉토리는 마이그레이션 대상 시스템의 전반적인 구조를 정의합니다. Managed Node Group, Karpenter, Pod Identity 등 최신 기술이 적용된 아키텍처 다이어그램 및 품질 속성을 포함합니다.

### Audience

이 README의 주요 독자:

- Cloud Architects
- Platform Engineers
- AI Agents

### Scope

#### In Scope

- AWS 마이그레이션 참조 아키텍처
- 품질 속성, 네트워크 경계, 보안/운영성 요구
- 하위 ADR 및 Spec으로 이어지는 구조 설명

#### Out of Scope

- 단일 기술 결정 기록
- Bicep/Terraform 같은 구현 코드
- 작업 상태 추적

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 AWS 마이그레이션 예시다. 기반 마이그레이션 기록은 하위 문서가 다른 날짜를 명시하지 않는 한 2026-03-31 기준이며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
02.architecture/requirements/
├── 0001-aws-cloud-native-architecture.md  # AWS cloud-native 참조 아키텍처
├── 2026-03-31-aws-migration-ard.md        # AWS 마이그레이션 ARD
└── README.md                              # This file
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/aws`로의 후속 통합을 소유한다. AWS 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/aws/`에 둔다.

1. [01.requirements](../../01.requirements/README.md)의 요구사항을 먼저 확인합니다.
2. 새 ARD는 `../../../../docs/99.templates/templates/sdlc/architecture/ard.template.md`를 기준으로 작성합니다.
3. 아키텍처 결정은 [02.architecture/decisions](../decisions/README.md)에 별도 기록합니다.
4. 구현 계약은 [03.specs](../../03.specs/README.md)와 연결합니다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live AWS 계정, EKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/aws/docs/02.architecture/requirements/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [01.requirements](../../01.requirements/README.md) - 제품 요구사항
- [02.architecture/decisions](../decisions/README.md) - 기술 의사결정
- [03.specs](../../03.specs/README.md) - 상세 명세
