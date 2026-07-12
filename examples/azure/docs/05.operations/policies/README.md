# 05.operations/policies (Operational Policies)

> 이 경로는 Azure 마이그레이션 프로젝트의 운영 정책, 거버넌스 및 통제 기준을 관리한다.

## Overview

본 디렉토리는 시스템의 지속적인 안정성과 보안을 보장하기 위한 "운영 표준 및 정책"을 관리한다. 패치 관리, 비용 통제, 접근 권한 관리, 확장성 정책 등을 규정하며, 이는 기술적인 결정(ADR)을 넘어선 관리적 기준을 제공한다.

### Audience

이 README의 주요 독자:

- Operations Teams
- IT Compliance Officers
- Security Administrators
- AI Agents

### Scope

#### In Scope

- Azure 리소스 운영 및 유지보수 정책 (Operations Policy)
- 패치 관리 및 업데이트 주기 (Maintenance Window)
- 비용 추적 및 리소스 할당 거버넌스
- 리소스 사용 중단 및 권한 회수 절차

#### Out of Scope

- 기술적 아키텍처 및 상세 설계 (02.architecture/requirements, 03.specs 참조)
- 긴급 상황 대응 절차 (05.operations/runbooks 참조)
- 장애 처리 기록 (05.operations/incidents 참조)

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 Azure 마이그레이션 예시다. 기반 마이그레이션 기록은 2026-03-31 기준이고, 2026-05-09 지원 상태 언급은 해당 날짜의 주석으로만 유지하며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
05.operations/policies/
├── azure-maintenance-policy.md    # 인프라 유지보수 및 운영 정책
└── README.md                    # 본 문서
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/azure`로의 후속 통합을 소유한다. Azure 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/azure/`에 둔다.

1. [azure-maintenance-policy.md](azure-maintenance-policy.md)를 통해 기본 운영 정책을 숙지한다.
2. 정책 수립 시 [policy.template.md](../../../../../docs/99.templates/templates/sdlc/operations/policy.template.md) 템플릿을 준수한다.
3. 모든 정책은 실제 인프라 환경과 컴플라이언스 기준(SOC2, HIPAA 등)에 맞게 정기적으로 갱신해야 한다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live Azure 구독, AKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/azure/docs/05.operations/policies/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../../02.architecture/requirements/0001-azure-migration-architecture.md)
- **Runbook**: [../05.operations/runbooks/README.md](../runbooks/README.md)
- **Monitoring**: Azure Monitor Dashboards

### AI Agent Guidance

1. 모든 운영 변경 사항은 정의된 정책의 범위 내에 있어야 한다.
2. 정책 위반 사항 발견 시 이슈(Task)를 생성하고 보고한다.
3. 정책 문서는 "어떻게(How-to)"보다는 "무엇이(What is required)"에 집중하여 작성한다.
