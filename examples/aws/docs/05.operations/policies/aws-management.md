# AWS Infrastructure Operations Policy

## Overview (KR)

이 문서는 AWS 클라우드 기반 인프라의 운영 관리를 위한 정책과 표준을 정의한다. 리소스의 안정성, 보안성 및 비용 효율성을 유지하기 위한 통제 기준을 제공한다.

## Policy Scope

이 정책은 VPC, EKS, RDS, ElastiCache 등 AWS 내의 모든 관리형 서비스 및 관련 네트워크 자산을 대상으로 한다.

## Applies To

- **Systems**: AWS EKS, RDS, ElastiCache, Secrets Manager, Route53, ALB.
- **Agents**: CI/CD Pipelines, Infrastructure Automation Tools (Terraform).
- **Environments**: Production (PRD), Staging (STG), Development (DEV).

## Controls

- **Required**:
  - 모든 리소스는 Terraform(IaC)을 통해 관리되어야 함.
  - 모든 인바운드 트래픽은 Security Group 및 Network ACL을 통한 명시적 허용 없이는 차단됨.
  - 리소스에는 `Project`, `Environment`, `Owner`, `CostCenter` 태그가 반드시 부여되어야 함.
- **Allowed**:
  - 개발 환경에서의 Spot Instance 사용.
  - IAM IRSA를 통한 세밀한 Pod 권한 할당.
- **Disallowed**:
  - AWS Console을 통한 수동 리소스 생성 및 변경.
  - 퍼블릭 서브넷에 데이터베이스 및 캐시 서버 배치.
  - 루트 계정(Root User)의 직접 사용.

## Exceptions

- **Emergency Deployment**: 장애 대응 등 긴급 상황 시 관리자 승인 하에 Console을 통한 수동 변경 가능 (단, 사후 Terraform 코드 업데이트 필수).
- **Approval Path**: CTO 또는 인프라 운영 팀장 승인.

## Verification

- **Compliance Check**: AWS Config 및 Trusted Advisor를 통해 분기별 보안 정책 준수 확인.
- **IaC Drift Check**: 정기적인 `terraform plan` 실행으로 실제 인프라와 코드 간의 정합성 확인.

## Review Cadence

- **Quarterly**: 매 분기별 정책 유효성 검토 및 클라우드 비용 분석.

## Related Documents

- **AARD**: [../02.architecture/requirements/2026-03-31-aws-migration-ard.md](../../02.architecture/requirements/2026-03-31-aws-migration-ard.md)
- **Runbook**: [../05.operations/runbooks/aws-recovery.md](../runbooks/aws-recovery.md)
- **Guide**: [../05.operations/guides/aws-setup-guide.md](../guides/aws-setup-guide.md)
