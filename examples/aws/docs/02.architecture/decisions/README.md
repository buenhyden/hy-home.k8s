# 02.architecture/decisions (Architecture Decision Records)

> 마이그레이션 핵심 기술에 대한 의사결정 기록

## Overview

이 디렉토리는 인프라 구축 및 서비스 전환 과정에서 발생한 주요 설계 결정 사항을 저장합니다. Karpenter 선정 이유, Managed DB 채택 배경 등 기술적 트레이드오프 분석을 포함합니다.

## Audience

이 README의 주요 독자:

- Cloud Architects
- Platform Engineers
- AI Agents

## Scope

### In Scope

- AWS 전환 과정의 주요 기술 결정
- 결정 맥락, 대안, 결과
- ARD/Spec/Plan으로 이어지는 근거 링크

### Out of Scope

- 전체 아키텍처 설명
- 상세 구현 명세
- 운영 절차

## Structure

```text
02.architecture/decisions/
├── 0001-aws-managed-services-selection.md              # AWS managed services 선택 결정
├── 2026-03-31-replace-vault-with-secrets-manager.md    # Secrets Manager 전환 결정
└── README.md                                           # This file
```

## How to Work in This Area

1. 결정의 상위 맥락을 [02.architecture/requirements](../requirements/README.md)에서 확인합니다.
2. 새 ADR은 `../../../../docs/99.templates/adr.template.md`를 기준으로 작성합니다.
3. 결정이 구현 계약을 바꾸면 [03.specs](../../03.specs/README.md)를 함께 갱신합니다.

## Link Basis

이 README의 링크 기준 위치는 `examples/aws/docs/02.architecture/decisions/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [02.architecture/requirements](../requirements/README.md) - 아키텍처 참조 모델
- [03.specs](../../03.specs/README.md) - 상세 기술 명세
