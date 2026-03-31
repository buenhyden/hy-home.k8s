# 09.runbooks (Incident Response Runbooks)

> AWS 클라우드 장애 대응 및 반복 운영 작업 실행 지침

## Overview

이 디렉토리는 시스템 장애 발생 시 즉각적인 조치와 복구를 위한 단계별 가이드라인을 저장합니다. RDS 장애 조치(failover), EKS 클러스터 고갈 대응, 데이터 복구 절차 등 예측 가능한 시나리오를 정의합니다.

## Structure

```text
09.runbooks/
├── rds-failover-runbook.md  # RDS 장애 복구 절차
└── README.md                # This file
```

## Related References

- [07.guides](../07.guides/README.md) - 운영 실무 가이드
- [08.operations](../08.operations/README.md) - 운영 거버넌스
- [10.incidents](../../../docs/10.incidents/README.md) - 사고 기록 저장소
