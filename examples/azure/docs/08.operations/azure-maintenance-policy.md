# Azure Infrastructure Maintenance Operations Policy

## Overview (KR)

이 문서는 Azure AKS 및 관련 관리형 서비스의 유지보수 정책을 정의한다. 시스템의 안정성, 보안성 및 비용 효율성을 유지하기 위한 정기 점검과 업데이트 기준을 규정한다.

## Policy Scope

본 정책은 Azure Kubernetes Service (AKS), PostgreSQL Flexible Server, Redis, Application Gateway for Containers (AGC) 등 모든 프로덕션용 Azure 리소스에 적용된다.

## Applies To

- **Systems**: AKS Cluster, AGC Traffic Controller, Database instances.
- **Environments**: Production (hy-home-k8s-prod), Staging.

## Controls

- **Required**:
  - Kubernetes 마이너 버전 업데이트는 가용 시간(Maintenance Window) 내에 수행해야 함.
  - 모든 리소스에는 `Owner`, `Project`, `Env` 태그가 부착되어야 함.
  - 월 1회 이상의 보안 패치 검토 및 적용.
- **Allowed**:
  - 개발 환경에서의 수동 리소스 스케일 업/다운.
  - 비정기적인 인프라 메트릭 감사.
- **Disallowed**:
  - 프로덕션 그룹 내에서의 수동(Portal) 리소스 생성 (반드시 Bicep/GitOps 경유).
  - 테넌트 관리자의 승인 없는 Public IP 노출.

## Exceptions

- 긴급 보안 취약점(Zero-day) 대응 시 선조치 후보고 (CTO 승인 필요).
- 테스트용 임시 리소스 groups 생성 (72시간 이내 자동 삭제 규칙 적용).

## Verification

- `az resource list --tag Project=hy-home-k8s` 명령어를 통해 태그 준수 여부 정기 감사.
- Azure Advisor 권장 사항 월별 검토 (Cost & Security).

## Review Cadence

- **Monthly**: 비용 및 보안 권고 사항 검토.
- **Quarterly**: 아키텍처 ARD 정합성 및 성능 벤치마크 검토.

## Related Documents

- **ARD**: [../02.ard/0001-azure-migration-architecture.md](../02.ard/0001-azure-migration-architecture.md)
- **Runbook**: [../09.runbooks/0001-disaster-recovery.md](../09.runbooks/0001-disaster-recovery.md)
- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
