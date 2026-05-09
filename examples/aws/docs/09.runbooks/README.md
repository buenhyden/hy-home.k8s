# 09.runbooks (Incident Response Runbooks)

> AWS 클라우드 장애 대응 및 반복 운영 작업 실행 지침

## Overview

이 디렉토리는 시스템 장애 발생 시 즉각적인 조치와 복구를 위한 단계별 가이드라인을 저장합니다. RDS 장애 조치(failover), EKS 클러스터 고갈 대응, 데이터 복구 절차 등 예측 가능한 시나리오를 정의합니다.

## Audience

이 README의 주요 독자:

- Cloud Operators
- Incident Responders
- AI Agents

## Scope

### In Scope

- AWS 장애 대응 및 반복 운영 절차
- 검증 명령, 성공 기준, 롤백/복구 단계
- Incident 기록으로 이어지는 후속 링크

### Out of Scope

- 운영 정책 자체
- 아키텍처 결정 기록
- 요구사항 또는 구현 명세

## Structure

```text
09.runbooks/
├── aws-disaster-recovery.md  # AWS 재해 복구 절차
├── aws-recovery.md           # AWS 복구 절차
└── README.md                 # This file
```

## How to Work in This Area

1. [08.operations](../08.operations/README.md)의 운영 정책을 먼저 확인합니다.
2. 새 Runbook은 `../../../../docs/99.templates/runbook.template.md`를 기준으로 작성합니다.
3. 사고 사실 기록이나 회고는 root [10.incidents](../../../../docs/10.incidents/README.md)에 연결합니다.

## Related References

- [07.guides](../07.guides/README.md) - 운영 실무 가이드
- [08.operations](../08.operations/README.md) - 운영 거버넌스
- [10.incidents](../../../../docs/10.incidents/README.md) - 사고 기록 저장소
