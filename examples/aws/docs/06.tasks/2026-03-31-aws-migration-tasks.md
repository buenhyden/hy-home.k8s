# Task: AWS Migration Execution List

## Overview (KR)

이 문서는 hy-home.k8s 시스템의 AWS 마이그레이션을 위한 세부 실행 태스크 목록이다. Spec 및 Plan에서 정의된 단계별 작업을 구체적인 실행 단위로 분해하여 추적한다.

## Inputs

- **Parent Spec**: [../04.specs/aws-migration/spec.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/04.specs/aws-migration/spec.md)
- **Parent Plan**: [../05.plans/2026-03-31-aws-migration-roadmap.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/05.plans/2026-03-31-aws-migration-roadmap.md)

## Task Table

| Task ID | Description | Type | Parent Spec Section | Parent Plan Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TSK-AWS-001 | AWS VPC 및 서브넷 구조 생성 (Terraform) | impl | Network Contract | Phase 1 | `terraform apply` log | DevOps | Todo |
| TSK-AWS-002 | EKS 클러스터 및 IAM Role 생성 | impl | Compute Contract | Phase 1 | `aws eks list-clusters` | DevOps | Todo |
| TSK-AWS-003 | Karpenter v1.0+ 설치 및 설정 | impl | Compute Contract | Phase 2 | `kubectl get pods -n karpenter` | Platform | Todo |
| TSK-AWS-004 | RDS Aurora Serverless v2 생성 | impl | Storage Strategy | Phase 3 | AWS Console / CLI check | DB Admin | Todo |
| TSK-AWS-005 | App 워크로드 배포 (GitOps) | ops | Core Design | Phase 4 | `kubectl get pods` | SRE | Todo |
| TSK-AWS-006 | 서비스 전환 및 DNS 업데이트 | ops | Network Contract | Phase 5 | DNS lookup check | SRE | Todo |

## Verification Summary

- **Test Commands**:
  - `kubectl get nodes -o wide`
  - `terraform plan`
  - `aws rds describe-db-clusters`
- **Logs / Evidence Location**:
  - `examples/aws/logs/` (if applicable)
  - CI/CD 파이프라인 빌드 로그
