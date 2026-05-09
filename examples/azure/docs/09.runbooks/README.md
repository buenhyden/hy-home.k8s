# 09.runbooks (Operational Runbooks)

> 이 경로는 Azure 마이그레이션 프로젝트의 특정 운영 상황 및 장애 발생 시 즉시 실행 가능한 절차서를 관리한다.

## Overview

본 디렉토리는 시스템 장애, 보안 사고, 정기 정검 또는 특정 운영 워크플로 중단 시 운영자가 즉시 따라 할 수 있는 "단계별 절차(Step-by-step Procedure)"를 관리한다. 가이드(07.guides)보다 긴급도가 높으며, 정책(08.operations)을 준수하여 작성한다.

## Audience

이 README의 주요 독자:

- On-call Engineers
- Incident Responders
- Lead Operations
- AI Agents

## Scope

### In Scope

- 재해 복구 및 클러스터 재구축 절차 (Disaster Recovery)
- 데이터베이스 백업 복원 및 PITR 수행 방법
- AGC 인증서 및 주요 보안 자격 증명 갱신 절차
- 대규모 트래픽 유입 시의 긴급 스케일링 절치

### Out of Scope

- 일반적인 시스템 이해 및 교육 (07.guides 참조)
- 상세 이행 계획 및 마일스톤 (05.plans 참조)
- 장애 발생 후의 사후 분석 문서 (`docs/10.incidents` 참조)

## Structure

```text
09.runbooks/
├── 0001-disaster-recovery.md        # 리전 장애 및 시스템 복구 런북
└── README.md                         # 본 문서
```

## How to Work in This Area

1. [0001-disaster-recovery.md](./0001-disaster-recovery.md)를 통해 긴급 상황 대응 절차를 숙지한다.
2. 런북 작성 시 [runbook.template.md](../../../../docs/99.templates/runbook.template.md) 템플릿을 준수한다.
3. 모든 단계는 명령어를 포함하여 즉시 실행 가능해야 하며, 실행 결과의 기댓값을 명시한다.

## Related References

- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
- **Operation**: [../08.operations/azure-maintenance-policy.md](../08.operations/azure-maintenance-policy.md)
- **Incidents**: [Root 10.incidents](../../../../docs/10.incidents/README.md)

## AI Agent Guidance

1. 런북 내의 모든 명령어는 실제 환경과 버전(2026.03 기준)에 맞는지 검증한다.
2. 실행 단계(Step)는 번호로 표시하며, 가역적인 작업은 롤백 절차를 포함한다.
3. 런북 실행은 비난 금지(Blameless) 원칙하에 사고 대응과 복구에만 집중한다.
