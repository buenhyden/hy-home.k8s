# AWS Migration Technical Specification (Spec)

## Overview (KR)

이 문서는 hy-home.k8s 로컬 환경을 AWS로 마이그레이션하기 위한 세부 기술 명세를 정의한다. VPC 네트워크 설계, EKS 클러스터 구성, 관리형 서비스(RDS, ElastiCache)의 스펙 및 보안 정책을 구체화한다.

## Strategic Boundaries & Non-goals

- `Owns`: AWS 리소스 정의 (VPC, EKS, RDS, IAM), EKS Add-ons 설정.
- `Does Not Own`: 애플리케이션 비즈니스 로직, 외부 도메인 관리 (Route53 호스팅 영역만 포함).

## Related Inputs

- **PRD**: [../../01.prd/2026-03-31-aws-migration-prd.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/01.prd/2026-03-31-aws-migration-prd.md)
- **ARD**: [../../02.ard/0001-aws-cloud-native-architecture.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/02.ard/0001-aws-cloud-native-architecture.md)
- **Related ADRs**: [../../03.adr/0001-aws-managed-services-selection.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/03.adr/0001-aws-managed-services-selection.md)

## Contracts

- **Network Contract**:
  - VPC CIDR: `10.100.0.0/16`
  - AZs: 3 (ap-northeast-2a, 2b, 2c)
  - Subnet Typing:
    - Public: `10.100.1.0/24`, `10.100.2.0/24`, `10.100.3.0/24` (ALB, NAT GW)
    - Private: `10.100.11.0/24`, `10.100.12.0/24`, `10.100.13.0/24` (EKS Nodes/Pods)
    - Database (Isolated): `10.100.21.0/24`, `10.100.22.0/24`, `10.100.23.0/24` (RDS, Cache)
- **Compute Contract**:
  - EKS Version: `1.31`
  - Authentication: IAM Pod Identity (v2026 update)
  - Node Management: Karpenter (Provisioner with Spot/On-demand mix)

## Core Design

- **Key Dependencies**:
  - Terraform v1.8+
  - AWS Provider v5.0+
  - Helm v3.14+
- **Tech Stack**:
  - AWS EKS, AWS RDS Aurora Serverless v2, AWS ElastiCache Serverless, AWS Secrets Manager

## Data Modeling & Storage Strategy

- **RDS Aurora PostgreSQL Spec**:
  - Engine: Aurora PostgreSQL 16.x compatible
  - Instance Class: Serverless v2 (Scaling: 0.5 - 4.0 ACU)
  - Storage: Cluster storage (Elastic)
- **ElastiCache Redis Spec**:
  - Type: Serverless (Managed Capacity)
  - Compatibility: Redis OSS 7.x

## Verification

인프라 구축 후 다음 명령어를 통해 상태를 검증한다.

```bash
# EKS 클러스터 접속 확인
aws eks update-kubeconfig --name hyhome-cluster --region ap-northeast-2
kubectl get nodes

# Managed Service 엔드포인트 도달 확인
nc -zv <rds-endpoint> 5432
nc -zv <redis-endpoint> 6379

# External Secrets 동기화 확인
kubectl get externalsecrets -A
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: EKS 클러스터 내의 Pod가 IAM Pod Identity를 통해 Secrets Manager에 접근 가능한지 검증.
- **VAL-SPC-002**: ALB Ingress를 통해 외부 트래픽이 애플리케이션 Pod로 정상 전달되는지 검증.

## Related Documents

- **Plan**: [../../05.plans/2026-03-31-aws-migration-roadmap.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/05.plans/2026-03-31-aws-migration-roadmap.md)
- **Tasks**: [../../06.tasks/2026-03-31-aws-migration-tasks.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/06.tasks/2026-03-31-aws-migration-tasks.md)
