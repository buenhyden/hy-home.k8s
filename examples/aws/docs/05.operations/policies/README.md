# 05.operations/policies (System Operations & Governance)

> AWS 클라우드 인프라 자산 운영 정책 및 관리 표준

## Overview

이 디렉토리는 마이그레이션 이후의 지속 가능한 운영 거버넌스를 정의합니다. AWS 비용 최적화 전략, 클라우드 리소스 태깅 표준, 백업 및 데이터 보관 정책을 포함합니다.

### Audience

이 README의 주요 독자:

- Cloud Operators
- Platform Engineers
- AI Agents

### Scope

#### In Scope

- AWS 운영 정책과 통제 기준
- 비용, 태깅, 백업, 보안 운영 표준
- Runbook과 Incident로 이어지는 운영 참조

#### Out of Scope

- 상세 구현 명세
- 실행 순서 중심 장애 대응 절차
- 프로젝트 작업 상태 추적

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 AWS 마이그레이션 예시다. 기반 마이그레이션 기록은 하위 문서가 다른 날짜를 명시하지 않는 한 2026-03-31 기준이며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
05.operations/policies/
├── aws-management.md           # AWS 관리 기준
├── aws-operations-policy.md    # AWS 운영 정책
└── README.md                   # This file
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/aws`로의 후속 통합을 소유한다. AWS 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/aws/`에 둔다.

1. [03.specs](../../03.specs/README.md)의 기술 계약과 현재 운영 기준을 비교합니다.
2. 새 Operation 문서는 `../../../../docs/99.templates/templates/sdlc/operations/policy.template.md`를 기준으로 작성합니다.
3. 반복 실행 절차는 [05.operations/runbooks](../runbooks/README.md)에 분리합니다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live AWS 계정, EKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/aws/docs/05.operations/policies/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [01.requirements](../../01.requirements/README.md) - 마이그레이션 목표
- [05.operations/guides](../guides/README.md) - 운영 실무 가이드
- [05.operations/runbooks](../runbooks/README.md) - 장애 조치 지침
