# AWS Migration Operations Policy

## Overview (KR)

이 문서는 hy-home.k8s AWS 인프라의 운영 정책을 정의한다. 리소스 관리의 일관성을 유지하고, 비용을 최적화하며, 보안 규정을 준수하기 위한 통제 기준을 제공한다.

## Policy Scope

이 정책은 AWS 계정 내의 모든 리소(VPC, EKS, RDS, S3 등)와 이를 관리하는 자동화 도구 및 에이전트의 활동을 규정한다.

## Applies To

- **Systems**: AWS Production/Staging 환경
- **Agents**: IaC 실행 에이전트, 모니터링 자동화 봇
- **Environments**: All AWS Regions used by hy-home.k8s

## Controls

- **Required**:
  - 모든 리소스는 `Project`, `Env`, `Owner` 태그를 필수로 포함해야 한다.
  - 모든 데이터 저장소는 KMS를 통한 암호화가 활성화되어야 한다.
- **Allowed**:
  - Karpenter를 통한 Spot 인스턴스 활용 (비용 절감 목적).
- **Disallowed**:
  - Public Subnet 내 데이터베이스 배치.
  - IAM User 기반의 장기 인증키(Access Key) 사용 (IAM Roles/Pod Identity 권장).

## Exceptions

- 긴급 장애 복구 시, SRE 팀의 승인 하에 일시적으로 수동 리소스 수정이 허용된다. (사후 IaC 동기화 필수)

## Verification

- AWS Config 및 AWS Security Hub를 통해 정책 준수 여부를 상시 점검한다.
- 매월 1일 비용 보고서를 검토하여 예산 초과 여부를 확인한다.

## Review Cadence

- Quarterly (매 분기별 운영 정책 최신화)

## AI Agent Policy Section

- **Log / Trace Retention**: 모든 에이전트의 실행 로그는 S3에 90일간 보관한다.
- **Safety Incident Thresholds**: 예기치 않은 리소스 삭제 명령 발생 시 즉시 실행을 차단하고 인간 승인(Human-in-the-loop)을 요청한다.

## Related Documents

- **ARD**: [../02.ard/0001-aws-cloud-native-architecture.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/02.ard/0001-aws-cloud-native-architecture.md)
- **Runbook**: [../09.runbooks/aws-disaster-recovery.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/09.runbooks/aws-disaster-recovery.md)
