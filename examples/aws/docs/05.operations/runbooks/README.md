# 05.operations/runbooks (Incident Response Runbooks)

> AWS 클라우드 장애 대응 및 반복 운영 작업 실행 지침

## Overview

이 디렉토리는 시스템 장애 발생 시 즉각적인 조치와 복구를 위한 단계별 가이드라인을 저장합니다. RDS 장애 조치(failover), EKS 클러스터 고갈 대응, 데이터 복구 절차 등 예측 가능한 시나리오를 정의합니다.

### Audience

이 README의 주요 독자:

- Cloud Operators
- Incident Responders
- AI Agents

### Scope

#### In Scope

- AWS 장애 대응 및 반복 운영 절차
- 검증 명령, 성공 기준, 롤백/복구 단계
- Incident 기록으로 이어지는 후속 링크

#### Out of Scope

- 운영 정책 자체
- 아키텍처 결정 기록
- 요구사항 또는 구현 명세

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 AWS 마이그레이션 예시다. 기반 마이그레이션 기록은 하위 문서가 다른 날짜를 명시하지 않는 한 2026-03-31 기준이며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
05.operations/runbooks/
├── aws-disaster-recovery.md  # AWS 재해 복구 절차
├── aws-recovery.md           # AWS 복구 절차
└── README.md                 # This file
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/aws`로의 후속 통합을 소유한다. AWS 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/aws/`에 둔다.

1. [05.operations/policies](../policies/README.md)의 운영 정책을 먼저 확인합니다.
2. 새 Runbook은 `../../../../docs/99.templates/templates/sdlc/operations/runbook.template.md`를 기준으로 작성합니다.
3. 사고 사실 기록이나 회고는 root [05.operations/incidents](../../../../../docs/05.operations/incidents/README.md)에 연결합니다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live AWS 계정, EKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/aws/docs/05.operations/runbooks/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [05.operations/guides](../guides/README.md) - 운영 실무 가이드
- [05.operations/policies](../policies/README.md) - 운영 거버넌스
- [05.operations/incidents](../../../../../docs/05.operations/incidents/README.md) - 사고 기록 저장소
