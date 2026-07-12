# 05.operations/guides (Operational Guides)

> AWS EKS 및 관리형 서비스 설정 및 운영 지침

## Overview

이 디렉토리는 마이그레이션이 완료된 인프라 환경을 안전하고 효과적으로 사용하기 위한 실무 지침서를 보관합니다. EKS 인증 설정(aws-auth), ArgoCD 연동 가이드, 로컬 개발 환경 구성 가이드 등을 다룹니다.

### Audience

이 README의 주요 독자:

- Platform Engineers
- Operators
- AI Agents

### Scope

#### In Scope

- AWS/EKS 운영 how-to 가이드
- 설정 절차, 선행 조건, 검증 방법
- Operations/Runbook으로 이어지는 링크

#### Out of Scope

- 정책 통제 기준
- 장애 대응 절차
- 실행 작업 상태 추적

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 AWS 마이그레이션 예시다. 기반 마이그레이션 기록은 하위 문서가 다른 날짜를 명시하지 않는 한 2026-03-31 기준이며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
05.operations/guides/
├── aws-setup-guide.md  # AWS/EKS 설정 가이드
└── README.md           # This file
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/aws`로의 후속 통합을 소유한다. AWS 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/aws/`에 둔다.

1. [03.specs](../../03.specs/README.md)의 기술 계약을 먼저 확인합니다.
2. 새 Guide는 `../../../../docs/99.templates/templates/sdlc/operations/guide.template.md`를 기준으로 작성합니다.
3. 운영 정책과 복구 절차는 [05.operations/policies](../policies/README.md), [05.operations/runbooks](../runbooks/README.md)에 연결합니다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live AWS 계정, EKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/aws/docs/05.operations/guides/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [02.architecture/requirements](../../02.architecture/requirements/README.md) - 아키텍처 참조 모델
- [04.execution/tasks](../../04.execution/tasks/README.md) - 실행 작업 목록
- [05.operations/policies](../policies/README.md) - 거버넌스 정책
