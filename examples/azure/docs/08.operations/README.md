# 08.operations (Operational Policies)

> 이 경로는 Azure 마이그레이션 프로젝트의 운영 정책, 거버넌스 및 통제 기준을 관리한다.

## Overview

본 디렉토리는 시스템의 지속적인 안정성과 보안을 보장하기 위한 "운영 표준 및 정책"을 관리한다. 패치 관리, 비용 통제, 접근 권한 관리, 확장성 정책 등을 규정하며, 이는 기술적인 결정(ADR)을 넘어선 관리적 기준을 제공한다.

## Audience

이 README의 주요 독자:

- Operations Teams
- IT Compliance Officers
- Security Administrators
- AI Agents

## Scope

### In Scope

- Azure 리소스 운영 및 유지보수 정책 (Operations Policy)
- 패치 관리 및 업데이트 주기 (Maintenance Window)
- 비용 추적 및 리소스 할당 거버넌스
- 리소스 사용 중단 및 권한 회수 절차

### Out of Scope

- 기술적 아키텍처 및 상세 설계 (02.ard, 04.specs 참조)
- 긴급 상황 대응 절차 (09.runbooks 참조)
- 장애 처리 기록 (10.incidents 참조)

## Structure

```text
08.operations/
├── azure-maintenance-policy.md    # 인프라 유지보수 및 운영 정책
└── README.md                    # 본 문서
```

## How to Work in This Area

1. [azure-maintenance-policy.md](./azure-maintenance-policy.md)를 통해 기본 운영 정책을 숙지한다.
2. 정책 수립 시 [operation.template.md](../../../../docs/99.templates/operation.template.md) 템플릿을 준수한다.
3. 모든 정책은 실제 인프라 환경과 컴플라이언스 기준(SOC2, HIPAA 등)에 맞게 정기적으로 갱신해야 한다.

## Related References

- **ARD**: [../02.ard/0001-azure-migration-architecture.md](../02.ard/0001-azure-migration-architecture.md)
- **Runbook**: [../09.runbooks/README.md](../09.runbooks/README.md)
- **Monitoring**: Azure Monitor Dashboards

## AI Agent Guidance

1. 모든 운영 변경 사항은 정의된 정책의 범위 내에 있어야 한다.
2. 정책 위반 사항 발견 시 이슈(Task)를 생성하고 보고한다.
3. 정책 문서는 "어떻게(How-to)"보다는 "무엇이(What is required)"에 집중하여 작성한다.
